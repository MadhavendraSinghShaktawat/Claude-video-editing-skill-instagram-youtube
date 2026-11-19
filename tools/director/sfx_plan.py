#!/usr/bin/env python3
"""Plan layered, cinematic sound effects from what is on screen, and print frame-aligned copies.

    python tools/director/sfx_plan.py <sfx.json>

sfx.json:
  {"events": "work/<slug>/edit/events4.json",     # tools/director/events.mjs
   "library": "work/<slug>/edit/sfx_library.json", # tools/director/sfx_library.py
   "voice": "<the finished video with the voice mix>",
   "fps": 25, "out_dir": "work/<slug>/edit/sfx_print", "plan": "work/<slug>/edit/sfx_plan.json",
   "pools": {...}, "skip": [[t0, t1], ...]}        # pools: name -> list of library file names

How a moment is built (all from measured events, nothing typed by hand):
  panel arrives      main whoosh (peak on the motion) + low air layer for the big layout changes
  panel leaves       softer air whoosh as the speaker takes the frame back
  cutout begins      reverse suction that ends exactly on the cut + sub hit + mid impact
  cutout ends        air burst
  title card         riser ending on the title word + sub ramp + impact + sub; each further word a smaller hit
  big number         short suction into it + impact (the opening and closing numbers also get the sub)
  punch / shake      impact + sub tail
  list / pill / icon small whips, panned to where the element is
  click / screenshot click / shutter + flash;  typing: quiet keyboard under the typing
  opening / ending   low drone bed, riser into the first reveal, thunder on the last line
Each sound is aligned by a measured point (whoosh and hit: loudest 20 ms; riser and suction: where it
peaks, at its end), printed as its own WAV with silence in front so that point lands on the exact
sample (Resolve places clips on whole frames), and given a clip gain so its loudness sits a set number
of LU under the voice. Pools are used in turn so the same file is not heard twice in a row.
"""
import json, os, subprocess, sys
import numpy as np

SR = 48000


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def write(path, x):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-", "-c:a", "pcm_s24le", path],
                   input=x.astype(np.float32).tobytes(), check=True)


# level of each layer: its loudest 400 ms (momentary loudness, BS.1770) this many LU under the voice's
# integrated loudness; beds (typing, drone) by their integrated loudness. A file's integrated loudness is
# not used for hits: a long reverb tail makes a loud hit measure quiet and it would be set far too hot.
LAYER = {
    "whoosh": (-12, 2.6), "whoosh_low": (-15, 2.4), "air": (-16, 2.0), "whip": (-20, 1.0),
    "suction": (-14, 2.0), "riser": (-11, 4.0), "subrise": (-14, 2.6), "impact": (-9, 3.4),
    "sub": (-10, 3.2), "thunder": (-9, 5.0), "glitch": (-17, 0.9), "scrape": (-20, 0.6),
    "click": (-16, 0.3), "shutter": (-14, 0.6), "flash": (-18, 1.0), "typing": (-26, 6.0),
    "drone": (-24, 60.0), "boom_riser": (-10, 8.0),
    # interface palette (premium UI sounds: notification dings, pops, message pops, counters)
    "ding": (-15, 1.4), "pop": (-19, 0.6), "msg": (-15, 0.8), "counter": (-24, 1.2), "success": (-16, 1.2),
    "ui": (-18, 1.2), "zoom": (-17, 1.6),
}
BED = ("typing", "drone")


def momentary_max(y):
    from scipy.signal import lfilter
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    e = (lfilter(b2, a2, lfilter(b1, a1, y, axis=0), axis=0) ** 2).sum(1)
    w = int(0.4 * SR)
    if len(e) <= w: return -0.691 + 10 * np.log10(e.mean() + 1e-12)
    c = np.concatenate([[0], np.cumsum(e)]); m = (c[w:] - c[:-w]) / w
    return float(-0.691 + 10 * np.log10(m.max() + 1e-12))


def integrated(y):
    from scipy.signal import lfilter
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    e = (lfilter(b2, a2, lfilter(b1, a1, y, axis=0), axis=0) ** 2).sum(1)
    blk, hop = int(0.4 * SR), int(0.1 * SR)
    ms = np.array([e[i:i + blk].mean() for i in range(0, max(1, len(e) - blk), hop)])
    l = -0.691 + 10 * np.log10(ms + 1e-12); g = ms[l > -70]
    return float(-0.691 + 10 * np.log10(g.mean() + 1e-12)) if len(g) else -70.0
TRACK = {  # Resolve track for each layer (lanes are added when clips overlap)
    "whoosh": "SFX Whoosh", "whoosh_low": "SFX Whoosh Low", "air": "SFX Whoosh Low", "whip": "SFX Detail",
    "suction": "SFX Riser", "riser": "SFX Riser", "subrise": "SFX Sub", "boom_riser": "SFX Riser",
    "impact": "SFX Impact", "sub": "SFX Sub", "thunder": "SFX Sub",
    "glitch": "SFX Detail", "scrape": "SFX Detail", "click": "SFX Detail", "shutter": "SFX Detail",
    "flash": "SFX Detail", "typing": "SFX Texture", "drone": "SFX Texture",
    "ding": "SFX UI", "pop": "SFX UI", "msg": "SFX UI", "success": "SFX UI", "ui": "SFX UI",
    "counter": "SFX Texture", "zoom": "SFX Whoosh Low",
}
ALIGN = {"riser": "peak", "suction": "peak", "subrise": "peak", "boom_riser": "peak", "typing": "start", "drone": "start", "counter": "start"}


def main():
    C = json.load(open(sys.argv[1]))
    E = json.load(open(C["events"]))
    LIB = {}
    for lib in ([C["library"]] if "library" in C else []) + C.get("libraries", []):
        for m in json.load(open(lib)): LIB.setdefault(m["file"], m)
    pools = {k: [f for f in v if f in LIB] for k, v in C["pools"].items()}
    for k, v in C["pools"].items():
        miss = [f for f in v if f not in LIB]
        if miss: print("not in library:", k, miss)
    voice_lufs = C.get("voice_lufs", -14.8)
    skips = [tuple(s) for s in C.get("skip", [])]
    ins = E.get("insert")
    if ins: skips.append((ins["at"] - 0.05, ins["at"] + ins["dur"] + 0.05))
    total = E["total"]
    rr, recent = {}, {}

    def pick(pool, t):
        lst = pools[pool]; n = len(lst)
        i = rr.get(pool, 0)
        for k in range(n):   # next in turn that was not used in the last 20 s
            f = lst[(i + k) % n]
            if t - recent.get(f, -99) > 20 or k == n - 1:
                rr[pool] = (i + k + 1) % n; recent[f] = t; return f

    P = []

    def place(layer, pool, t, rel=0.0, pan=0.0, why="", length=None, file=None, semis=0.0):
        if any(a <= t <= b for a, b in skips) or t > total - 0.3: return
        f = file or pick(pool, t)
        m = LIB[f]
        al = ALIGN.get(layer, "hit")
        a = 0.0 if al == "start" else m["t_peak"]
        lvl, mx = LAYER[layer]
        P.append({"layer": layer, "file": f, "path": m["path"], "lead": m["lead"], "t": round(t, 3), "align": a,
                  "len": min(length or 1e9, total - (t - a) if t - a > 0 else 1e9, m["dur"], a + (m["tail"] + 0.25 if al == "hit" else 99), a + mx if al != "start" else mx),
                  "target": voice_lufs + lvl + rel, "pan": round(pan, 1), "why": why, "semis": semis})

    ev = E["events"]; frames = sorted(E["frames"], key=lambda f: f["t0"])
    cuts = [f for f in frames if f["kind"] == "cut"]
    in_cut = lambda t: any(c["t0"] - 0.05 <= t < c["t1"] for c in cuts)
    PAN = {"splitR": -25, "splitRm": 25, "splitL": 25, "pip": 0}

    has = lambda k: bool(pools.get(k))
    PANX = lambda e: 0 if e.get("x") is None else max(-45, min(45, (e["x"] / 1920 * 2 - 1) * 45))

    # ---- opening: a logo-intro build that lands on the first big number (or drone + riser), low hit on frame 1
    first_num = next(e for e in ev if e["kind"] == "number")
    if has("open_build"):
        place("boom_riser", "open_build", first_num["t"], rel=-1, why="opening build into " + first_num["label"])
    else:
        place("drone", "drone", 0.0, why="opening bed", length=min(cuts[0]["t1"] + 1.5, 12))
        place("riser", "riser", first_num["t"], rel=1, why="into " + first_num["label"], file=pools["open_riser"][0])
    place("sub", "sub", 0.02, rel=1, why="cold open hit", file=pools["open_sub"][0])
    place("impact", "impact", first_num["t"] + 0.04, rel=1, why="lands " + first_num["label"])
    used_num = {id(first_num)}

    # ---- layouts
    prev_t1 = -9
    last_cut = cuts[-1]
    end_word = next((e for e in ev if e["kind"] in ("bigword", "number") and last_cut["t0"] - 0.05 <= e["t"] <= last_cut["t0"] + 1.2), None)
    for i, f in enumerate(frames):
        k = f["kind"]
        if f is last_cut and end_word:
            prev_t1 = f["t1"]; continue
        if k == "cut":
            first = next((e for e in ev if e["kind"] in ("bigword", "number") and f["t0"] - 0.05 <= e["t"] <= f["t0"] + 1.2), None)
            place("suction", "suction", f["t0"], why="into cutout")
            place("sub", "sub", f["t0"] + 0.02, why="cutout drop")
            if first:
                place("impact", "impact", first["t"] + 0.05, why="cutout word " + first["label"]); used_num.add(id(first))
            else:
                place("impact", "impact", f["t0"] + 0.02, rel=-3, why="cutout")
            nxt = frames[i + 1] if i + 1 < len(frames) else None
            if not (nxt and nxt["t0"] - f["t1"] < 0.6):
                place("air", "air", f["t1"] + 0.12, why="out of cutout")
            prev_t1 = f["t1"]
            continue
        joined = f["t0"] - prev_t1 < 0.6
        place("whoosh", "whoosh", f["t0"] + 0.2, pan=PAN.get(k, 0) * (0.5 if joined else 1), why=k + " in")
        if k in ("pip", "splitL") and not joined and has("whoosh_low"):
            place("whoosh_low", "whoosh_low", f["t0"] + 0.22, rel=-2, why=k + " in (low layer)")
        nxt = frames[i + 1] if i + 1 < len(frames) else None
        if not (nxt and nxt["t0"] - f["t1"] < 1.0):
            place("air", "air", f["t1"] + 0.18, pan=-PAN.get(k, 0) * 0.6, why=k + " out")
        prev_t1 = f["t1"]

    # ---- titles: a whoosh-hit that builds into the word, impact + sub on it; further words a soft pop
    for e in ev:
        if e["kind"] == "title":
            place("riser", "riser", e["t"], why="title " + e["label"])
            place("impact", "impact", e["t"] + 0.06, why="title " + e["label"])
            place("sub", "sub", e["t"] + 0.06, rel=-2, why="title " + e["label"])
        elif e["kind"] == "title2":
            place("pop", "pop", e["t"] + 0.03, rel=2, why="title word " + e["label"])

    # ---- numbers roll with a ticking counter; punches and shakes hit
    last_punch = -9
    for e in ev:
        t, k = e["t"], e["kind"]
        if k == "number":
            place("counter", "counter", t, pan=PANX(e), why="digits roll " + e["label"], length=0.9)
            if id(e) not in used_num: place("pop", "pop", t + 0.55, rel=-1, pan=PANX(e), why="number lands " + e["label"])
        elif k == "punch":
            place("impact", "impact", t, rel=1, why="punch"); last_punch = t
            if not any(abs(t - th) < 0.3 for th, _ in C.get("thunder", [])): place("sub", "sub", t, rel=-1, why="punch")
        elif k == "shake" and t - last_punch > 0.9 and not in_cut(t):
            place("sub", "sub", t + 0.02, rel=-4, why="shake")

    # ---- interface details: notification dings for list items (rising in pitch through each list, like
    # notifications stacking), message pops for cards, light pops for pills / labels / icons
    lists, cur = [], []
    for e in [x for x in ev if x["kind"] == "listitem"]:
        if cur and (e["t"] - cur[-1]["t"] > 12 or e["x"] != cur[-1]["x"]): lists.append(cur); cur = []
        cur.append(e)
    if cur: lists.append(cur)
    LADDER = C.get("ding_ladder", [0, 2, 4, 5, 7, 9])
    for li in lists:
        for n, e in enumerate(li):
            place("ding", "ding", e["t"] + 0.06, pan=PANX(e) * 0.5, semis=LADDER[min(n, len(LADDER) - 1)], why=f"list item {n + 1}: {e['label']}")
    big = sorted(p["t"] for p in P if p["layer"] not in ("ding", "counter"))
    near = lambda t, w: any(abs(t - b) < w for b in big)
    alt = 0
    for e in ev:
        t, k = e["t"], e["kind"]
        if k == "card":
            place("msg", "msg", t + 0.1, pan=PANX(e) * 0.5, why="card " + e["label"])
        elif k == "pill" and not near(t, 0.35):
            alt += 1; place("pop", "pop", t + 0.05, pan=PANX(e), semis=[0, 2, -1][alt % 3], why="pill " + e["label"])
        elif k == "icon" and not near(t, 0.4):
            alt += 1; place("pop", "pop_icon", t + 0.08, pan=PANX(e), rel=-2, semis=[0, 3, 5, 7][alt % 4], why="icon " + e["label"])
        elif k == "device" and not near(t, 0.6):
            place("zoom", "zoom", t + 0.15, pan=PANX(e), why="device " + e["label"])
        elif k == "bigword" and not in_cut(t) and not near(t, 0.4):
            place("whip", "whip", t + 0.1, why="word " + e["label"])
        elif k == "morph" and not near(t, 0.4):
            place("suction", "suction_short", t, rel=-4, why="morph " + e["label"])
        elif k == "click":
            place("click", "click", t, pan=PANX(e), why="click")
        elif k == "mark" and e["label"] not in ("strike", "circle", "box", "underline", "cross", "highlight") and not near(t, 0.4):
            place("pop", "pop", t + 0.05, rel=-2, why="label " + e["label"])
        elif k == "island":
            place("ui", "notify", t + 0.15, why="timer appears")
        elif k == "islandClock":
            place("click", "click", t, rel=-2, why="timer starts")
        big = sorted(p["t"] for p in P if p["layer"] not in ("ding", "counter"))
    tends = [e for e in ev if e["kind"] == "typeEnd"]
    for e in [x for x in ev if x["kind"] == "type"]:
        end = min((x["t"] for x in tends if x["t"] >= e["t"]), default=e["t"] + 1.5)
        if end - e["t"] > 0.6: place("typing", "typing", e["t"], why="typing", length=min(6.0, end - e["t"] + 0.1))
    for t in C.get("screenshots", []):
        place("shutter", "shutter", t, why="screenshot")
    for t, why in C.get("success", []):
        place("success", "success", t, why=why)

    # ---- ending: a suspense build into the last line, impact + sub on it
    last = end_word or max((e for e in ev if e["kind"] == "bigword"), key=lambda e: e["t"])
    place("boom_riser", "end_build", last["t"], why="ending build into " + last["label"])
    place("impact", "impact", last["t"] + 0.05, rel=1, why="last line " + last["label"], file=pools.get("end_hit", [None])[0])
    place("sub", "sub", last["t"] + 0.05, why="last line " + last["label"])
    for t, rel in C.get("thunder", []):
        place("thunder", "thunder", t, rel=rel, why="big moment")

    # ---- print aligned files and assign tracks/lanes
    fps = C.get("fps", 25)
    os.makedirs(C["out_dir"], exist_ok=True)
    P.sort(key=lambda p: p["t"])
    cache, lanes, out = {}, {}, []
    for n, p in enumerate(P):
        ratio = 2 ** (p.get("semis", 0) / 12)        # pitch by resampling: a step up plays faster, so align/len shrink
        start = p["t"] - p["align"] / ratio          # where the file's (trimmed) first sample goes
        skip = max(0.0, -start); start = max(0.0, start)
        F = int(np.floor(start * fps + 1e-6)); pad = start - F / fps
        if p["path"] not in cache: cache[p["path"]] = load(p["path"])
        x = cache[p["path"]]
        s0 = int((p["lead"] + skip * ratio) * SR); s1 = s0 + int(max(0.05, p["len"] - skip) * SR)
        y = x[s0:min(s1, len(x))].copy()
        if ratio != 1:   # band-limited resampling (polyphase), so a pitched-up ding does not alias
            from fractions import Fraction
            from scipy.signal import resample_poly
            fr = Fraction(1 / ratio).limit_denominator(400)
            y = resample_poly(y, fr.numerator, fr.denominator, axis=0).astype(np.float32)
        cut_short = s1 < len(x) - int(0.1 * SR)          # trimmed before its natural end: fade the tail, never chop it
        fi, fo = min(len(y), int(0.004 * SR)), min(len(y) // 2, int((1.5 if p["layer"] == "drone" else 0.45 if cut_short else 0.08) * SR))
        y[:fi] *= np.linspace(0, 1, fi)[:, None]; y[len(y) - fo:] *= np.linspace(1, 0, fo)[:, None]
        if p["layer"] == "drone": y[:int(1.2 * SR)] *= np.linspace(0, 1, min(len(y), int(1.2 * SR)))[:, None]
        ref = integrated(y) if p["layer"] in BED else momentary_max(y)
        p["gain"] = round(float(np.clip(p["target"] - ref, -60, 24)), 1); p["ref_lu"] = round(ref, 1)
        y = np.concatenate([np.zeros((int(round(pad * SR)), 2), np.float32), y])
        name = f"{n:03d} {p['layer']} {p['t']:07.2f} - {os.path.splitext(p['file'])[0][:40]}.wav"
        dst = os.path.join(C["out_dir"], name); write(dst, y)
        dur_f = int(np.ceil(len(y) / SR * fps))
        tr = TRACK[p["layer"]]; L = lanes.setdefault(tr, [])
        lane = next((i for i, end in enumerate(L) if end <= F), None)
        if lane is None: L.append(0); lane = len(L) - 1
        L[lane] = F + dur_f
        out.append({**p, "print": os.path.abspath(dst), "frame": F, "frames": dur_f, "track": tr + ("" if lane == 0 else f" {lane + 1}")})
    json.dump({"fps": fps, "clips": out, "tracks": sorted({o["track"] for o in out}, key=lambda s: list(TRACK.values()).index(s.rsplit(" ", 1)[0] if s[-1].isdigit() else s) * 10 + (int(s[-1]) if s[-1].isdigit() else 0))},
              open(C["plan"], "w"), indent=1)
    from collections import Counter
    print(len(out), "clips;", dict(Counter(o["layer"] for o in out)))
    print("tracks:", dict(Counter(o["track"] for o in out)))
    print("files used:", len({o["file"] for o in out}))


if __name__ == "__main__":
    main()
