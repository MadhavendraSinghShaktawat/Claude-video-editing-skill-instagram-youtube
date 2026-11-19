#!/usr/bin/env python3
"""Learn a reference video's sound design: find every sound effect under the voice, measure it, say what picture
event it sits on, and shortlist the closest sounds in a local library.

    python tools/director/sfx_learn.py reference/analysis/<slug> [--library work/x/sfx_library.json ...] [--earshot]

Needs the analysis folder written by tools/analyze.py (the Demucs stems in _tmp/stems, shots.json, words.json).
Sound effects in short-form edits are often 25-35 dB under the voice: a whole-mix onset detector (audio.py) misses
them, so this works on the voice-free stem, band by band.

Writes <analysis>/sfx_learned.json and sfx_learned.md:
  events   time, peak, length, level (dBFS and relative to the voice), band shares, centroid, dominant pitch,
           tonality, rise/fall, a class (sub / whoosh / ding / pop / click / riser / texture), the nearest picture
           event (cut, pop, motion, caption change) and the offset of the sound's peak from it
  rules    per class: count, rate per minute, median level under the voice, median offset to its picture event,
           which picture events carry it (share), median length and pitch
  matches  per class, the closest library sounds by measured shape (and by earshot's CLAP ranking with --earshot)
"""
import argparse, glob, json, os, subprocess, sys
import numpy as np
from scipy.signal import stft

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def portable(path):
    """A path safe to commit: relative to the repo when inside it, else with the home folder as ~."""
    ap = os.path.abspath(path)
    if ap.startswith(ROOT + os.sep): return os.path.relpath(ap, ROOT)
    home = os.path.expanduser("~")
    return "~" + ap[len(home):] if ap.startswith(home + os.sep) else path

SR = 48000
CLASS_QUERY = {
    "sub": "a deep low sub boom or bass drop", "whoosh": "a fast air whoosh swish transition",
    "ding": "a short bright notification ding chime", "pop": "a short soft bubble pop", "click": "a crisp mouse click tick",
    "riser": "a rising tension riser build", "texture": "a soft ambient texture", "impact": "a cinematic hit impact",
}


def load(path, mono=True):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1" if mono else "2", "-ar", str(SR), "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def db(x): return 20 * np.log10(np.maximum(x, 1e-9))


def band_env(x, hop):
    f, t, Z = stft(x, SR, nperseg=2048, noverlap=2048 - hop, boundary=None)
    P = np.abs(Z) ** 2
    bands = {"sub": (20, 120), "low": (120, 500), "mid": (500, 2500), "high": (2500, 8000), "air": (8000, 20000)}
    E = {k: P[(f >= a) & (f < b)].sum(0) for k, (a, b) in bands.items()}
    return f, t, P, E


BANDS = {"sub": (20, 100), "low": (100, 500), "tone": (500, 2500), "high": (2500, 8000), "air": (8000, 20000)}


def detect(x, v, prom=18.0, leak=-6.0):
    """Per band, peaks that stand >= prom dB above their surroundings in the voice-free stem AND are not voice
    leakage (stem band energy >= voice band energy + leak dB at that instant). Peaks in several bands within
    0.12 s are one event."""
    from scipy.signal import find_peaks
    hop = 960  # 20 ms
    f, t, Z = stft(x, SR, nperseg=4096, noverlap=4096 - hop, boundary=None)
    P = np.abs(Z) ** 2
    Q = None
    if v is not None:
        _, _, Zv = stft(v[:len(x)], SR, nperseg=4096, noverlap=4096 - hop, boundary=None); Q = np.abs(Zv) ** 2
    hits = []
    for name, (a, b) in BANDS.items():
        sel = (f >= a) & (f < b)
        e = 10 * np.log10(P[sel].sum(0) + 1e-14)
        ve = 10 * np.log10(Q[sel].sum(0) + 1e-14) if Q is not None else e - 99
        pk, pr = find_peaks(e, prominence=prom, distance=5)
        for i, p in zip(pk, pr["prominences"]):
            if e[i] - ve[min(i, len(ve) - 1)] < leak: continue
            j = i
            while j < len(e) - 1 and e[j] > e[i] - 20: j += 1
            k = i
            while k > 0 and e[k] > e[i] - 20 and i - k < 50: k -= 1
            hits.append((t[i], t[k], t[j], name, float(p)))
    hits.sort()
    ev = []
    for tp, t0, t1, n, p in hits:
        if ev and tp - ev[-1]["peak"] < 0.12:
            m = ev[-1]; m["bands"].add(n); m["end"] = max(m["end"], t1); m["t"] = min(m["t"], t0)
            if p > m["prom"]: m["prom"], m["peak"] = p, tp
        else:
            ev.append({"t": t0, "peak": tp, "end": t1, "bands": {n}, "prom": p})
    return ev, (f, t, P)


def measure(x, voice_rms_db, e, spec):
    f, t, P = spec
    i0 = max(0, int((e["peak"] - 0.06) * SR)); i1 = min(len(x), int((max(e["end"], e["peak"] + 0.08) + 0.05) * SR))
    seg = x[i0:i1]
    if len(seg) < 256: return None
    h = int(0.005 * SR)
    env = np.sqrt(np.convolve(seg ** 2, np.ones(h) / h, "same")) + 1e-9
    ip = int(np.argmax(env)); pk = db(env[ip])
    after = np.where(db(env[ip:]) < pk - 20)[0]
    length = (ip + (after[0] if len(after) else len(env) - ip)) / SR
    spec_s = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2 + 1e-18
    ff = np.fft.rfftfreq(len(seg), 1 / SR)
    tot = spec_s.sum()
    share = {k: float(spec_s[(ff >= a) & (ff < b)].sum() / tot) for k, (a, b) in
             {"sub": (20, 120), "low": (120, 500), "mid": (500, 2500), "high": (2500, 8000), "air": (8000, 20000)}.items()}
    cen = float((spec_s * ff).sum() / tot)
    band = (ff > 80) & (ff < 12000)
    flat = float(np.exp(np.mean(np.log(spec_s[band]))) / np.mean(spec_s[band]))
    pitch = float(ff[band][np.argmax(spec_s[band])])
    n3 = max(1, len(seg) // 3)
    rise = float(10 * np.log10((np.mean(seg[-n3:] ** 2) + 1e-14) / (np.mean(seg[:n3] ** 2) + 1e-14)))
    level = float(db(np.sqrt(np.mean(seg[max(0, ip - h * 10):ip + h * 10] ** 2))))
    return {"peak_t": round((i0 + ip) / SR, 3), "length": round(length, 3), "level_dbfs": round(level, 1),
            "rel_voice_db": round(level - voice_rms_db, 1), "shares": {k: round(v, 3) for k, v in share.items()},
            "centroid": int(cen), "pitch_hz": int(pitch), "tonal": round(flat, 3), "rise_db": round(rise, 1)}


def leakage(x, v, m):
    """Energy of the voice-free stem against the voice stem in the event's own strongest band, over the event.
    Demucs leaves consonants and breaths in the voice-free stem about 20-30 dB down; a real effect stands out."""
    if v is None: return 99.0
    i0 = max(0, int((m["peak_t"] - 0.04) * SR)); i1 = int((m["peak_t"] + max(0.06, min(m["length"], 0.4))) * SR)
    a, b = x[i0:i1], v[i0:i1]
    if len(a) < 256 or len(b) < len(a): return 99.0
    w = np.hanning(len(a)); A = np.abs(np.fft.rfft(a * w)) ** 2; B = np.abs(np.fft.rfft(b[:len(a)] * w)) ** 2
    ff = np.fft.rfftfreq(len(a), 1 / SR)
    best = max({"sub": (20, 120), "low": (120, 500), "mid": (500, 2500), "high": (2500, 8000), "air": (8000, 20000)}.items(),
               key=lambda kv: A[(ff >= kv[1][0]) & (ff < kv[1][1])].sum())[1]
    sel = (ff >= best[0]) & (ff < best[1])
    return float(10 * np.log10((A[sel].sum() + 1e-14) / (B[sel].sum() + 1e-14)))


def classify(m, bands):
    s = m["shares"]
    if m["rise_db"] > 8 and m["length"] > 0.6: return "riser"
    if "air" in bands and m["length"] < 0.12 and not ({"sub", "tone"} & bands): return "click"
    if "tone" in bands and m["tonal"] < 0.1 and 500 < m["pitch_hz"] < 4000: return "ding"
    if "sub" in bands and s["sub"] + s["low"] > 0.5: return "sub"
    if "air" in bands or "high" in bands:
        return "click" if m["length"] < 0.12 else "whoosh"
    if "tone" in bands: return "ding" if m["tonal"] < 0.2 else "pop"
    if s["sub"] > 0.25: return "impact"
    return "pop" if m["length"] < 0.16 else "texture"


def picture_events(an):
    sh = json.load(open(os.path.join(an, "shots.json")))
    pe = [{"t": c["t"], "kind": "cut_" + c["kind"]} for c in sh.get("cuts", [])]
    for s in sh.get("shots", []):
        for me in s.get("motion_events", []) or []: pe.append({"t": me["start"], "kind": "motion"})
    tj = os.path.join(an, "text.json")
    if os.path.exists(tj):
        tx = json.load(open(tj)); seen = set()
        for tr in tx.get("tracks", []):
            t0 = tr.get("t0", tr.get("start"))
            if t0 is None: continue
            k = round(t0, 1)
            if k in seen: continue
            seen.add(k); pe.append({"t": t0, "kind": "text"})
    pe.sort(key=lambda p: p["t"])
    return pe


def nearest(pe, t, kinds=None, win=0.6):
    best = None
    for p in pe:
        if kinds and not any(p["kind"].startswith(k) for k in kinds): continue
        d = t - p["t"]
        if abs(d) <= win and (best is None or abs(d) < abs(best[1])): best = (p, d)
    return best


def lib_features(item):
    return np.array([np.log10(max(item.get("centroid", 1000), 50)), np.log10(max(item.get("dur", 0.3), 0.02)),
                     item.get("low", 0.1), min(item.get("tonal", 0.2), 1.0), np.clip(item.get("rise", 0) / 20, -1, 1)])


def ev_features(m):
    return np.array([np.log10(max(m["centroid"], 50)), np.log10(max(m["length"], 0.02)), m["shares"]["sub"] + m["shares"]["low"] * 0.3,
                     min(m["tonal"], 1.0), np.clip(m["rise_db"] / 20, -1, 1)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("analysis"); ap.add_argument("--library", nargs="*", default=[])
    ap.add_argument("--earshot", action="store_true", help="also tag each class with earshot (CLAP/AST) and rank library folders")
    ap.add_argument("--leak-db", type=float, default=-6, help="drop peaks whose band is this far under the voice stem at that instant (leakage)")
    ap.add_argument("--prom", type=float, default=18, help="how far (dB) a peak must stand above its surroundings in its band")
    ap.add_argument("--min-rel", type=float, default=-48, help="ignore events quieter than this under the voice (dB)")
    a = ap.parse_args()
    an = a.analysis.rstrip("/")
    nv = glob.glob(os.path.join(an, "_tmp/stems/**/no_vocals.wav"), recursive=True)
    vo = glob.glob(os.path.join(an, "_tmp/stems/**/vocals.wav"), recursive=True)
    if not nv: sys.exit("no voice-free stem: run tools/analyze.py (audio step) first")
    x = load(nv[0]); v = load(vo[0]) if vo else None
    h = int(0.4 * SR)
    vr = np.array([np.sqrt(np.mean(v[i:i + h] ** 2)) for i in range(0, len(v) - h, h)]) if v is not None else np.array([0.1])
    voice_db = float(np.median(db(vr[vr > np.percentile(vr, 40)])))
    raw, spec = detect(x, v, a.prom, a.leak_db)
    pe = picture_events(an)
    words = []
    wj = os.path.join(an, "words.json")
    if os.path.exists(wj):
        w = json.load(open(wj)); words = w if isinstance(w, list) else w.get("words", [])
    events = []
    for e in raw:
        m = measure(x, voice_db, e, spec)
        if not m or m["rel_voice_db"] < a.min_rel: continue
        m["class"] = classify(m, e["bands"]); m["t"] = round(e["t"], 3); m["bands"] = sorted(e["bands"]); m["prominence_db"] = round(e["prom"], 1)
        nb = nearest(pe, m["peak_t"], ["cut"], 0.7) or nearest(pe, m["peak_t"], None, 0.35)
        if nb: m["picture"] = {"kind": nb[0]["kind"], "t": round(nb[0]["t"], 3), "offset": round(nb[1], 3)}
        if words:
            wd = min(words, key=lambda q: abs(q["start"] - m["peak_t"]))
            if abs(wd["start"] - m["peak_t"]) < 0.25: m["word"] = wd.get("w", wd.get("word", "")).strip()
        events.append(m)
    # one sound, one row: peaks of several bands at the same instant are layers of one effect
    events.sort(key=lambda e: e["peak_t"]); ded = []
    for e in events:
        if ded and abs(e["peak_t"] - ded[-1]["peak_t"]) < 0.06:
            d = ded[-1]; d["bands"] = sorted(set(d["bands"]) | set(e["bands"]))
            if e["prominence_db"] > d["prominence_db"]: e["bands"] = d["bands"]; ded[-1] = e
        else: ded.append(e)
    events = ded
    for e in events: e["layers"] = "+".join(b for b in BANDS if b in e["bands"])
    dur = len(x) / SR
    cut_layers = {}
    for e in events:
        if e.get("picture", {}).get("kind", "").startswith("cut") and abs(e["picture"]["offset"]) < 0.15:
            cut_layers[e["layers"]] = cut_layers.get(e["layers"], 0) + 1
    rules = {}
    for c in sorted({e["class"] for e in events}):
        es = [e for e in events if e["class"] == c]
        offs = [e["picture"]["offset"] for e in es if "picture" in e]
        kinds = {}
        for e in es:
            k = e["picture"]["kind"] if "picture" in e else "none"; kinds[k] = kinds.get(k, 0) + 1
        rules[c] = {"count": len(es), "per_min": round(len(es) / dur * 60, 1),
                    "rel_voice_db_median": round(float(np.median([e["rel_voice_db"] for e in es])), 1),
                    "length_median": round(float(np.median([e["length"] for e in es])), 3),
                    "pitch_median_hz": int(np.median([e["pitch_hz"] for e in es])),
                    "centroid_median": int(np.median([e["centroid"] for e in es])),
                    "picture_offset_median": round(float(np.median(offs)), 3) if offs else None,
                    "on_picture_share": round(len(offs) / len(es), 2), "picture_kinds": kinds,
                    "times": [e["peak_t"] for e in es]}
    matches = {}
    lib = []
    for lp in a.library:
        for it in json.load(open(lp)): lib.append(it)
    if lib:
        F = np.array([lib_features(i) for i in lib]); sd = F.std(0) + 1e-6
        for c in rules:
            es = [e for e in events if e["class"] == c]
            q = np.median(np.array([ev_features(e) for e in es]), 0)
            d = np.sqrt((((F - q) / sd) ** 2).sum(1))
            matches[c] = [{"path": portable(lib[k]["path"]), "dist": round(float(d[k]), 2)} for k in np.argsort(d)[:6]]
    tags = {}
    if a.earshot:
        try:
            from earshot import api
            for c in rules:
                es = sorted([e for e in events if e["class"] == c], key=lambda e: -e["rel_voice_db"])[:3]
                tags[c] = []
                for e in es:
                    r = api.describe(nv[0], start=max(0, e["t"] - 0.03), end=e["t"] + max(e["length"], 0.15) + 0.05)
                    tags[c].append({"t": e["peak_t"], "tags": (r.get("tags") or r.get("top") or r.get("summary")) if isinstance(r, dict) else str(r)[:200]})
        except Exception as ex:
            tags["error"] = str(ex)[:300]
    out = {"source": an, "duration": round(dur, 2), "voice_rms_dbfs": round(voice_db, 1), "events": events,
           "rules": rules, "cut_layers": cut_layers, "matches": matches, "earshot_tags": tags, "class_queries": CLASS_QUERY}
    json.dump(out, open(os.path.join(an, "sfx_learned.json"), "w"), indent=1)
    L = [f"# Sound effects learned from {os.path.basename(an)}", "",
         f"{len(events)} events in {dur:.1f} s ({len(events) / dur * 60:.0f}/min) on the voice-free stem; voice RMS {voice_db:.1f} dBFS.", "",
         "| class | count | /min | under voice (dB) | length (s) | pitch (Hz) | on picture | offset to picture (s) | picture events |",
         "|---|---|---|---|---|---|---|---|---|"]
    for c, r in rules.items():
        L.append(f"| {c} | {r['count']} | {r['per_min']} | {r['rel_voice_db_median']} | {r['length_median']} | {r['pitch_median_hz']} | {r['on_picture_share']} | {r['picture_offset_median']} | {r['picture_kinds']} |")
    nc = len([c for c in json.load(open(os.path.join(an, "shots.json")))["cuts"] if c["kind"] == "hard"])
    L += ["", f"Sounds within 0.15 s of a cut, by layer ({sum(cut_layers.values())} on {nc} hard cuts): {cut_layers}"]
    L += ["", "## Events", "", "| peak | class | layers | len | dB vs voice | pitch | picture | word |", "|---|---|---|---|---|---|---|---|"]
    for e in events:
        p = e.get("picture"); ps = f"{p['kind']} {p['offset']:+.2f}" if p else ""
        L.append(f"| {e['peak_t']:.2f} | {e['class']} | {e['layers']} | {e['length']:.2f} | {e['rel_voice_db']} | {e['pitch_hz']} | {ps} | {e.get('word', '')} |")
    if matches:
        L += ["", "## Closest library sounds (by measured shape)", ""]
        for c, ms in matches.items(): L.append(f"- **{c}**: " + "; ".join(os.path.basename(m['path']) + f" ({m['dist']})" for m in ms))
    open(os.path.join(an, "sfx_learned.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L[:12 + len(rules)]))


if __name__ == "__main__":
    main()
