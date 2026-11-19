#!/usr/bin/env python3
"""Rough cut of a multi-take recording against its script: pick the best take of every
line, drop restarts, fillers and dead space, render one file. Use this when the raw
footage is several files with lines said more than once. (tools/rough_cut.py is for
one continuous take.)

    # 1. word timings of every raw file (fillers kept)
    python tools/transcribe.py raw/C0001.MP4 work/ep1/C0001 --verbatim --lang en
    # 2. plan the cut (writes work/ep1/cut/cutlist.md and edl.json; nothing rendered)
    python tools/select_takes.py work/ep1/script.txt work/ep1 raw/C0001.MP4 raw/C0002.MP4 ...
    # 3. READ cutlist.md, add fixes to work/ep1/cut/overrides.json, run step 2 again
    # 4. render. This also checks the render piece by piece, drops every repeat it finds and
    #    renders again (up to --rounds 3), then writes cut/script_vs_edit.md and cut/check.json
    python tools/select_takes.py work/ep1/script.txt work/ep1 raw/*.MP4 --render
    # 5. resolve what it prints as FIX BY HAND / LOOK AT, read script_vs_edit.md, then deliver

Files are taken in the order given; that is assumed to be recording order (camera file
names usually are). Each file's words must be in work/<ep>/<file stem>/words.json.

How takes are chosen (all measured, nothing listened to):
  - the script is split into lines of at least 7 words (short sentences join a neighbour)
  - every line is aligned (local alignment, fuzzy word match) against all words of all
    files; every place it was said is an attempt, with coverage = share of script words heard
  - the LAST attempt with coverage >= 0.85 is used (speakers repeat a line until it is right);
    if none reaches that, the best one is used and flagged
  - inside the chosen attempt: a run of words that repeats the words right before or after
    it is a restart (the earlier try is dropped), filler sounds (um, uh) are dropped,
    off-script words are kept and listed
  - unscripted speech of 4+ words that directly follows a chosen line in the same take, and
    is not part of any attempt of another line, is kept and listed (ad-libs); everything
    else between chosen lines (false starts, "okay again", chatter) is removed
  - cut points are moved into silence measured on the audio; pauses longer than
    --max-pause are shortened to --keep-pause; every boundary sits on a frame

overrides.json: {"drop": [["C0699", 12.3, 14.0], ...],          # source file stem, seconds
                 "force_take": {"<line number>": ["C0698", 74.0]},   # attempt starting near this time
                 "drop_line": [12, ...], "keep_unscripted": false,
                 "line_spans": {"<line number>": [["C0712", 35.88, 39.5], ...]}}   # exact spans, set by hand
"""
import argparse, difflib, json, os, re, subprocess, sys, wave
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from common import probe, jload, jdump, ROOT

ap = argparse.ArgumentParser()
ap.add_argument("script"); ap.add_argument("work"); ap.add_argument("videos", nargs="+")
ap.add_argument("--max-pause", type=float, default=None)
ap.add_argument("--keep-pause", type=float, default=None)
ap.add_argument("--style", default=None)
ap.add_argument("--render", action="store_true")
ap.add_argument("--codec", default="hevc", choices=["hevc", "prores", "h264"])
ap.add_argument("--bitrate", default="50M")
ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--check", default=None, help="words.json of a render: compare with the script")
ap.add_argument("--apply-check", action="store_true", help="add the repeats found by --check to overrides.json")
ap.add_argument("--check-pieces", action="store_true",
                help="transcribe the render piece by piece (in cut/check_pieces.json) and check that: speech recognition on a long file merges a phrase said twice; piece by piece it cannot")
ap.add_argument("--no-check", action="store_true", help="skip the automatic piece-by-piece check after --render (not recommended)")
ap.add_argument("--rounds", type=int, default=3, help="most render -> check -> drop repeats -> render rounds after --render")
ap.add_argument("--round", type=int, default=1, help=argparse.SUPPRESS)
a = ap.parse_args()

MEM = os.environ.get("EXPLAINER_EDITOR_HOME") or os.path.join(ROOT, "memory")
brand = jload(os.path.join(MEM, "brand.json"), {})
sname = a.style or brand.get("default_style")
style = jload(os.path.join(MEM, "styles", sname, "style.json")) if sname else None
if style:
    a.max_pause = a.max_pause or style["speech"]["pause_p90_s"]["median"]
    a.keep_pause = a.keep_pause or style["speech"]["pause_median_s"]["median"]
a.max_pause = a.max_pause or 0.35; a.keep_pause = a.keep_pause or 0.2
OUT = os.path.join(a.work, "cut"); os.makedirs(OUT, exist_ok=True)
ov = jload(os.path.join(OUT, "overrides.json"), {})

SYN = {"cloud": "claude", "clod": "claude", "sort": "short", "sorts": "shorts", "gonna": "going"}
STOP = set("the a an of to in on at is are was it its it's thats that this and or but so i im ive you your we my me for with which what be do does just".split())
FILL = {"um", "umm", "uh", "uhh", "uhm", "er", "erm", "ah", "ahh", "hmm", "mm", "mhm", "eh"}


NUMW = {w: str(i) for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                        "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


def norm(s):
    s = re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ").replace(".", " ")).strip()
    s = SYN.get(s, s)
    return NUMW.get(s, s)


# ---------- script -> lines
raw = open(a.script).read()
raw = re.sub(r"\[[^\]]*\]", " PLACEHOLDER ", raw)                      # [PLACEHOLDERS] are said however the speaker likes
lines = []
for para in [p for p in re.split(r"\n\s*\n", raw) if p.strip()]:
    sents = [s for s in re.split(r"(?<=[.?!])\s+", para.strip()) if s.strip()]
    cur = []
    for s in sents:
        toks = [norm(t) for t in s.split()]
        toks = [t for t in sum((x.split() for x in toks), []) if t]
        cur.append((s, toks))
        if sum(len(t) for _, t in cur) >= 7:
            lines.append(cur); cur = []
    if cur:
        if lines and len(lines[-1]) and sum(len(t) for _, t in cur) < 7 and lines[-1][-1][0] in para: lines[-1] += cur
        else: lines.append(cur)
L = [{"n": i, "text": " ".join(s for s, _ in c).replace("PLACEHOLDER", "[...]"), "ph": any("placeholder" in t for _, t in c),
      "toks": [w for w in sum((t for _, t in c), []) if w != "placeholder"]} for i, c in enumerate(lines)]

# ---------- transcript stream (all files, in order)
clips, T = [], []           # T: dicts with clip index, word, norm, start, end
for ci, v in enumerate(a.videos):
    stem = os.path.splitext(os.path.basename(v))[0]
    wj = jload(os.path.join(a.work, stem, "words.json"))
    if not wj: sys.exit(f"missing {a.work}/{stem}/words.json - run tools/transcribe.py first")
    info = probe(v)
    clips.append({"stem": stem, "path": os.path.abspath(v), "fps": info["fps"], "dur": info["duration"],
                  "w": info.get("width"), "h": info.get("height")})
    for w in wj["words"]:
        for k, part in enumerate(norm(w["w"]).split() or [""]):
            T.append({"c": ci, "w": w["w"], "n": part, "s": w["start"], "e": w["end"], "p": w.get("p", 1)})
    T.append({"c": ci, "w": "|", "n": "|", "s": 0, "e": 0, "p": 0})        # barrier between files
N = len(T)
fps = clips[0]["fps"]
vocab = sorted({t["n"] for t in T})
vi = {w: i for i, w in enumerate(vocab)}
Tv = np.array([vi[t["n"]] for t in T])
barrier = np.array([t["n"] == "|" for t in T])
_simc = {}


def simrow(word):
    """score of this script word against every vocabulary word"""
    if word in _simc: return _simc[word]
    r = np.full(len(vocab), -1.0)
    for i, v in enumerate(vocab):
        if v == word: r[i] = 2.0
        elif v and v != "|" and abs(len(v) - len(word)) <= 3 and v[0] == word[0]:
            sm = difflib.SequenceMatcher(None, v, word)
            if sm.real_quick_ratio() >= 0.75 and sm.ratio() >= 0.75: r[i] = 1.2
        elif v.isdigit() and word.isdigit() and (v in word or word in v): r[i] = 1.2
    _simc[word] = r; return r


GI, GD = 0.6, 1.0     # cost of an extra spoken word, of a script word not said


def align(toks, S):
    m = len(toks)
    H = np.zeros((m + 1, N + 1))
    pen = GD * np.arange(1, m + 1)
    for j in range(1, N + 1):
        diag = H[:-1, j - 1] + S[:, j - 1]
        ins = H[1:, j - 1] - GI
        A = np.maximum(0, np.maximum(diag, ins))
        H[1:, j] = np.maximum.accumulate(A + pen) - pen
    return H


def trace(H, S, i, j):
    ops = []    # (kind, script i, transcript j)
    while i > 0 and j > 0 and H[i, j] > 1e-9:
        if np.isclose(H[i, j], H[i - 1, j - 1] + S[i - 1, j - 1]):
            ops.append(("m" if S[i - 1, j - 1] > 0 else "x", i - 1, j - 1)); i -= 1; j -= 1
        elif np.isclose(H[i, j], H[i, j - 1] - GI):
            ops.append(("ins", None, j - 1)); j -= 1
        else:
            ops.append(("del", i - 1, None)); i -= 1
    return ops[::-1]


attempts = {}
covered = np.zeros(N, bool)
for ln in L:
    toks = ln["toks"]; m = len(toks)
    if m == 0: attempts[ln["n"]] = []; continue
    S = np.stack([simrow(t)[Tv] for t in toks]); S[:, barrier] = -50
    out = []
    for _ in range(12):
        H = align(toks, S)
        i, j = np.unravel_index(np.argmax(H), H.shape)
        sc = H[i, j]
        if sc < max(4.0, 0.9 * m): break
        ops = trace(H, S, i, j)
        js = [o[2] for o in ops if o[2] is not None]
        j0, j1 = js[0], js[-1]
        # trim leading/trailing insertions (not part of the line)
        mt = [o for o in ops if o[0] == "m"]
        j0, j1 = mt[0][2], mt[-1][2]
        cov = len({o[1] for o in mt}) / m
        out.append({"j0": j0, "j1": j1, "cov": round(cov, 2), "score": round(float(sc) / (2 * m), 2),
                    "ops": [o for o in ops if o[2] is None or j0 <= o[2] <= j1],
                    "first_i": mt[0][1], "last_i": mt[-1][1]})
        S[:, j0:j1 + 1] = -50
        covered[j0:j1 + 1] = True
    out.sort(key=lambda x: x["j0"])
    attempts[ln["n"]] = out

# ---------- choose
force = {int(k): v for k, v in ov.get("force_take", {}).items()}
stem_i = {c["stem"]: i for i, c in enumerate(clips)}
chosen, report = {}, []
for ln in L:
    at = attempts[ln["n"]]
    if ln["n"] in ov.get("drop_line", []): report.append((ln, None, "dropped by override")); continue
    if not at: report.append((ln, None, "NOT FOUND in any file")); continue
    flag = ""
    if ln["n"] in force:
        st, t = force[ln["n"]]
        pick = min((x for x in at if T[x["j0"]]["c"] == stem_i[st]), key=lambda x: abs(T[x["j0"]]["s"] - t))
        flag = "forced"
    else:
        good = [x for x in at if x["cov"] >= 0.85 and x["score"] >= 0.55]
        if good: pick = good[-1]
        else: pick = max(at, key=lambda x: (x["cov"], x["j0"])); flag = f"WEAK: best take covers {pick['cov']:.0%} of the line"
    chosen[ln["n"]] = pick; report.append((ln, pick, flag))

# ---------- token ranges to keep for each chosen line
def scripted_share(js, n):
    """share of these spoken words that occur in script lines n-1..n+2: high = a retake fragment, not an ad-lib"""
    voc = set(sum((L[k]["toks"] for k in range(max(0, n - 1), min(len(L), n + 3))), []))
    ws = [T[j]["n"] for j in js if T[j]["n"] not in FILL and T[j]["n"] not in STOP]
    if not ws: return 0.0
    hit = sum(1 for w in ws if w in voc or any(len(w) > 3 and difflib.SequenceMatcher(None, w, v).ratio() >= 0.8 for v in voc))
    return hit / len(ws)


def restart_before(run, j0):
    """the speaker stopped and said it again: the run re-says words that came just before it.
    Returns the earlier words (plus any tail of the old try at the start of the run) to drop."""
    best = None
    for r in range(0, min(3, len(run) - 1)):
        for q in range(run[0] - 1, max(j0, run[0] - len(run) - 3) - 1, -1):
            m = run[0] - q
            if m < 2 or r + m > len(run): continue
            x = [T[j]["n"] for j in range(q, run[0])]; y = [T[j]["n"] for j in run[r:r + m]]
            rt = difflib.SequenceMatcher(None, x, y).ratio()
            pos = sum(u == v for u, v in zip(x, y))
            if rt >= 0.7 and (best is None or (rt, pos, m) > best[0]):
                best = ((rt, pos, m), list(range(q, run[0])) + run[:r])
    return best[1] if best else None


def keep_tokens(pick, n):
    """indices of transcript tokens kept from this attempt, with reasons for drops"""
    j0, j1 = pick["j0"], pick["j1"]
    notes = []
    # The alignment starts where the words start to agree. Words said in the same breath just
    # before it are the misheard start of the line ("I will list" for "I built this", "The motion"
    # for "Remotion"): take back as many as the script words it skipped, plus one if the first
    # match is only approximate. Same at the end.
    toks = L[n]["toks"]
    back = pick["first_i"] + (0 if T[j0]["n"] == toks[pick["first_i"]] else 1)
    fwd = len(toks) - 1 - pick["last_i"] + (0 if T[j1]["n"] == toks[pick["last_i"]] else 1)
    while back > 0 and j0 > 0 and T[j0 - 1]["c"] == T[j0]["c"] and T[j0 - 1]["n"] != "|" and not covered[j0 - 1] \
            and T[j0]["s"] - T[j0 - 1]["e"] < 0.25:
        j0 -= 1; back -= 1; notes.append(("line start extended", [j0]))
        if T[j0]["n"] not in toks and j0 > 0 and T[j0 - 1]["c"] == T[j0]["c"] and not covered[j0 - 1] \
                and T[j0]["s"] - T[j0 - 1]["e"] < 0.15 and back == 0:
            back = 1                                       # a split word ("The motion"): take its first half too
    while fwd > 0 and j1 + 1 < N and T[j1 + 1]["c"] == T[j1]["c"] and T[j1 + 1]["n"] != "|" and not covered[j1 + 1] \
            and T[j1 + 1]["s"] - T[j1]["e"] < 0.25:
        j1 += 1; fwd -= 1; notes.append(("line end extended", [j1]))
    keep = set(range(j0, j1 + 1))
    ops = pick["ops"]
    k = 0
    while k < len(ops):
        if ops[k][0] != "ins": k += 1; continue
        r0 = k
        while k < len(ops) and ops[k][0] == "ins": k += 1
        run = [o[2] for o in ops[r0:k]]
        rn = [T[j]["n"] for j in run]
        if all(x in FILL for x in rn):
            keep -= set(run); notes.append(("filler", run)); continue
        Lr = len(run)
        before = [j for j in range(run[0] - Lr, run[0]) if j >= j0]
        after = [j for j in range(run[-1] + 1, run[-1] + 1 + Lr) if j <= j1]
        rs = " ".join(rn)
        sb = difflib.SequenceMatcher(None, rs, " ".join(T[j]["n"] for j in before)).ratio() if len(before) == Lr else 0
        sa = difflib.SequenceMatcher(None, rs, " ".join(T[j]["n"] for j in after)).ratio() if after else 0
        sa_pref = difflib.SequenceMatcher(None, rs, " ".join(T[j]["n"] for j in after[:Lr])).ratio() if after else 0
        if (Lr >= 2 and max(sa, sa_pref) >= 0.7) or (Lr == 1 and after and rn[0] == T[after[0]]["n"]):   # one word: only an exact stutter
            keep -= set(run); notes.append(("restart", run))
        elif Lr >= 2 and (rs_ := restart_before(run, j0)):
            keep -= set(rs_); notes.append(("restart", rs_))
        elif Lr >= 3 and not L[n]["ph"] and scripted_share(run, n) >= 0.6:
            keep -= set(run); notes.append(("retake fragment", run))
        elif not L[n]["ph"] and not ov.get("keep_unscripted", False) and \
                sum(1 for j in run if T[j]["n"] not in STOP and T[j]["n"] not in FILL) >= 2:
            keep -= set(run); notes.append(("not in script, removed", run))
        else:
            notes.append(("off-script kept", [j for j in run if T[j]["n"] not in FILL]))
            keep -= {j for j in run if T[j]["n"] in FILL}
    for j in list(keep):
        if T[j]["n"] in FILL: keep.discard(j)
    return sorted(keep), notes


order = sorted(chosen)
plan = []       # per line: tokens kept
for n in order:
    toks, notes = keep_tokens(chosen[n], n)
    plan.append({"n": n, "toks": toks, "notes": notes})

# unscripted speech right after a chosen line, in the same take
adlibs = []
for p in plan:
    if L[p["n"]]["ph"] or ov.get("keep_unscripted", False):    # only what fills a [PLACEHOLDER], unless asked
        j = chosen[p["n"]]["j1"] + 1; run = []
        while j < N and not covered[j] and T[j]["n"] != "|":
            run.append(j); j += 1
        # take it sentence by sentence; stop at the first one that is a retake of script words
        words, sent = [], []
        for k in run:
            sent.append(k)
            if T[k]["w"][-1:] in ".?!," or k == run[-1]:
                if len([q for q in sent if T[q]["n"] not in FILL]) >= 3 and scripted_share(sent, p["n"]) >= 0.5: break
                words += [q for q in sent if T[q]["n"] not in FILL]; sent = []
        if len(words) >= 4:
            p["toks"] = sorted(set(p["toks"]) | set(words)); adlibs.append((p["n"], words))

# ---------- audio activity per file (for cut points)
act_cache, db_cache, breath_cache = {}, {}, {}


def breaths(x, db, floor, sr=16000):
    """10 ms frames that are an audible breath: loud enough to hear, no pitch (normalised
    autocorrelation peak at 75-400 Hz under 0.4) and no low-frequency weight (2-8 kHz energy
    within 15 dB of 80-1000 Hz), lasting 0.2 s or more. Voiced speech has strong pitch and a
    steep tilt; short fricatives (s, f) are under 0.2 s."""
    hop, win, nfft = 160, 480, 512
    n = max(0, (len(x) - win) // hop)
    f = np.fft.rfftfreq(nfft, 1 / sr); lo_b = (f >= 80) & (f < 1000); hi_b = (f >= 2000) & (f < 8000)
    lag = slice(int(sr / 400), int(sr / 75)); hw = np.hanning(win).astype(np.float32)
    voic = np.zeros(len(db)); tilt = np.full(len(db), -60.0)
    for c0 in range(0, n, 20000):
        c1 = min(n, c0 + 20000)
        fr = x[np.arange(win)[None, :] + hop * np.arange(c0, c1)[:, None]] * hw
        P = np.abs(np.fft.rfft(fr, nfft, axis=1)) ** 2
        tilt[c0:c1] = 10 * np.log10((P[:, hi_b].sum(1) + 1e-12) / (P[:, lo_b].sum(1) + 1e-12))
        ac = np.fft.irfft(P, axis=1)
        voic[c0:c1] = ac[:, lag].max(1) / (ac[:, 0] + 1e-12)
    m = (db > floor + 10) & (voic < 0.4) & (tilt > -15)
    d_ = np.diff(np.concatenate([[0], m.astype(np.int8), [0]]))
    st, en = np.flatnonzero(d_ == 1), np.flatnonzero(d_ == -1)
    for k_ in range(len(st) - 1):                      # bridge gaps under 40 ms
        if st[k_ + 1] - en[k_] < 4: m[en[k_]:st[k_ + 1]] = True
    d_ = np.diff(np.concatenate([[0], m.astype(np.int8), [0]]))
    for s_, e_ in zip(np.flatnonzero(d_ == 1), np.flatnonzero(d_ == -1)):
        if e_ - s_ < 20: m[s_:e_] = False
    return m


def activity(ci):
    if ci in act_cache: return act_cache[ci]
    stem = clips[ci]["stem"]
    wav = os.path.join(a.work, stem, "_tmp", "16k.wav")
    if not os.path.exists(wav):
        os.makedirs(os.path.dirname(wav), exist_ok=True)
        subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", clips[ci]["path"], "-vn", "-ac", "1", "-ar", "16000", wav])
    w = wave.open(wav); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    hop = 160; k = len(x) // hop
    db = 10 * np.log10((x[:k * hop].reshape(k, hop) ** 2).mean(1) + 1e-12)
    vmed = float(np.median(db[db > np.percentile(db, 60)]))
    floor = float(np.percentile(db, 20))
    strict, edge = db > vmed - 20, db > max(vmed - 32, floor + 8)
    br = breaths(x, db, floor)
    strict &= ~br; edge &= ~br                         # an inhale is not speech: it is trimmed and counts as pause
    breath_cache[ci] = br
    for m_ in (strict, edge):                          # clicks and pops under 50 ms are not speech
        d_ = np.diff(np.concatenate([[0], m_.astype(np.int8), [0]]))
        for s_, e_ in zip(np.flatnonzero(d_ == 1), np.flatnonzero(d_ == -1)):
            if e_ - s_ < 5: m_[s_:e_] = False
    act_cache[ci] = (strict, edge, vmed); db_cache[ci] = db; return act_cache[ci]


def silence_runs(mask, t0, t1, minlen):
    a0, a1 = int(t0 * 100), int(t1 * 100)
    seg = ~mask[a0:a1]; out = []; s = None
    for i, v in enumerate(np.append(seg, False)):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= minlen: out.append(((a0 + s) / 100, (a0 + i) / 100))
            s = None
    return out


snap = lambda t: round(round(t * fps) / fps, 4)
HEAD, TAIL = 0.08, 0.10


def bounds(ci, ts, te, lo, hi):
    """refine a kept stretch [ts, te] (word times) to cut points in silence, within (lo, hi)"""
    strict, edge, _ = activity(ci)
    n = len(edge)
    i = int(ts * 100)
    if i < n and not edge[i]:                          # word time starts in silence: move to onset
        k = i
        while k < min(n, i + 40) and not edge[k]: k += 1
        if k < i + 40: i = k
    else:                                             # back up to the onset (breath / soft start)
        k = i
        while k > max(0, i - 60) and edge[k - 1]: k -= 1
        i = k
    if i > 0 and not edge[i - 1] and lo > i / 100 - HEAD:
        lo = max(0, i / 100 - 0.04)       # a clear onset after silence beats the previous word's (often late) end time
    s = max(lo, i / 100 - HEAD)
    e_i = int(te * 100)
    if e_i < n and edge[min(n - 1, e_i)]:
        k = e_i
        while k < min(n, e_i + 40) and edge[k]: k += 1
        e_i = k
    else:
        k = e_i
        while k > max(0, e_i - 30) and not edge[k - 1]: k -= 1
        e_i = k
    e = min(hi, e_i / 100 + TAIL)
    # never more than a short breath of air on either side: hold both ends to the clear speech
    i0, i1 = int(s * 100), min(n, int(e * 100))
    on = np.flatnonzero(strict[i0:i1])
    if len(on):
        s = max(s, (i0 + on[0]) / 100 - 0.12)
        e = min(e, (i0 + on[-1] + 1) / 100 + 0.15)
    return s, max(e, s + 0.1)


segs = []
for p in plan:
    toks = p["toks"]
    if not toks: continue
    groups, g = [], [toks[0]]
    for j in toks[1:]:
        if j == g[-1] + 1 and T[j]["s"] - T[g[-1]]["e"] <= 0.8: g.append(j)    # a longer gap may hide untranscribed sound
        else: groups.append(g); g = [j]
    groups.append(g)
    for g in groups:
        ci = T[g[0]]["c"]
        if len(g) == 1:                                   # a lone word timed into silence is a timing error
            _, edge, _ = activity(ci)
            f0, f1 = int(T[g[0]]["s"] * 100), max(int(T[g[0]]["s"] * 100) + 1, int(T[g[0]]["e"] * 100))
            if edge[f0:f1].mean() < 0.3: p["notes"].append(("mistimed word skipped", g)); continue
        prev_e = T[g[0] - 1]["e"] if g[0] > 0 and T[g[0] - 1]["c"] == ci and T[g[0] - 1]["n"] != "|" else 0
        next_s = T[g[-1] + 1]["s"] if g[-1] + 1 < N and T[g[-1] + 1]["n"] != "|" else clips[ci]["dur"]
        s, e = bounds(ci, T[g[0]]["s"], T[g[-1]]["e"], prev_e + 0.02 if prev_e else 0, next_s - 0.02 if next_s < clips[ci]["dur"] else clips[ci]["dur"])
        segs.append({"line": p["n"], "c": ci, "t0": s, "t1": e, "ja": g[0], "jb": g[-1], "text": " ".join(T[k]["w"] for k in g)})

for n_, spans in ov.get("line_spans", {}).items():      # the editor's own spans for a line replace the automatic ones
    segs = [sg for sg in segs if sg["line"] != int(n_)]
    for k_, (st, x0, x1) in enumerate(spans):
        segs.append({"line": int(n_), "c": stem_i[st], "t0": x0, "t1": x1, "ja": -1000 - 10 * int(n_) - k_, "jb": -1000 - 10 * int(n_) - k_,
                     "text": "(set by hand)"})
segs.sort(key=lambda sg: (sg["line"], sg["t0"] if sg["ja"] < 0 else 0))

# join stretches of the same take that touch, then shorten long pauses inside
merged = []
for sg in segs:
    if merged and sg["ja"] == merged[-1]["jb"] + 1 and T[sg["ja"]]["s"] - T[merged[-1]["jb"]]["e"] <= 0.8:          # next word of the same take: no cut needed
        merged[-1]["t1"] = max(merged[-1]["t1"], sg["t1"]); merged[-1]["jb"] = sg["jb"]; merged[-1]["text"] += " " + sg["text"]
        merged[-1]["lines"].append(sg["line"])
    else:
        merged.append(dict(sg, lines=[sg["line"]]))
final = []
for sg in merged:
    strict, _, _ = activity(sg["c"])
    kh = a.keep_pause / 2
    cuts = [(x + kh, y - kh) for x, y in silence_runs(strict, sg["t0"] + HEAD, sg["t1"] - TAIL, int(a.max_pause * 100))]
    cuts += [(d0, d1) for st, d0, d1 in ov.get("drop", []) if clips[sg["c"]]["stem"] == st and d0 < sg["t1"] and d1 > sg["t0"]]
    t = sg["t0"]; pieces = []
    for x, y in sorted(cuts):
        pieces.append((t, max(t, x))); t = max(t, y)
    pieces.append((t, sg["t1"]))
    for x, y in pieces:
        x, y = snap(x), snap(y)
        if y - x < 0.2 and not strict[int(x * 100):int(y * 100)].any(): continue   # a silent sliver would flash on screen
        if y - x >= 2 / fps: final.append({"clip": clips[sg["c"]]["stem"], "src": clips[sg["c"]]["path"], "t0": x, "t1": y, "lines": sg["lines"]})

total = sum(f["t1"] - f["t0"] for f in final)
raw_total = sum(c["dur"] for c in clips)
jdump({"fps": fps, "settings": {"max_pause": a.max_pause, "keep_pause": a.keep_pause, "style": sname},
       "duration": round(total, 2), "segments": final}, os.path.join(OUT, "edl.json"))

# ---------- report
R = [f"# Cut list: {os.path.basename(a.script)}", "",
     f"{len(clips)} files, {raw_total / 60:.1f} min of footage -> {total / 60:.2f} min ({total:.1f} s), {len(final)} pieces.",
     f"Pauses over {a.max_pause:.2f} s shortened to {a.keep_pause:.2f} s. Lines are numbered; fix with overrides.json.", "",
     "## Lines", "", "| # | take used | attempts | coverage | note | script |", "| --- | --- | --- | --- | --- | --- |"]
for ln, pick, flag in report:
    at = attempts[ln["n"]]
    where = f"{clips[T[pick['j0']]['c']]['stem']} {T[pick['j0']]['s']:.1f}-{T[pick['j1']]['e']:.1f}" if pick else "-"
    alls = ", ".join(f"{clips[T[x['j0']]['c']]['stem'][-3:]}@{T[x['j0']]['s']:.0f}({x['cov']:.0%})" for x in at)
    R.append(f"| {ln['n']} | {where} | {alls} | {pick['cov']:.0%} | {flag} | {ln['text'][:90]} |" if pick else
             f"| {ln['n']} | - | {alls} | - | {flag} | {ln['text'][:90]} |")
R += ["", "## Removed inside a take (restarts, fillers) and kept off-script words", ""]
for p in plan:
    for kind, js in p["notes"]:
        if js: R.append(f"- line {p['n']}, {kind}: \"{' '.join(T[j]['w'] for j in js)}\" ({clips[T[js[0]]['c']]['stem']} {T[js[0]]['s']:.2f})")
R += ["", "## Unscripted speech kept (said right after a chosen line, in the same take)", ""]
for n, js in adlibs:
    R.append(f"- after line {n}: \"{' '.join(T[j]['w'] for j in js)}\" ({clips[T[js[0]]['c']]['stem']} {T[js[0]]['s']:.2f})")
R += ["", "## Pieces in order", "", "| # | file | from | to | length | lines |", "| --- | --- | --- | --- | --- | --- |"]
for i, f in enumerate(final):
    R.append(f"| {i} | {f['clip']} | {f['t0']:.2f} | {f['t1']:.2f} | {f['t1'] - f['t0']:.2f} | {','.join(map(str, f['lines']))} |")
open(os.path.join(OUT, "cutlist.md"), "w").write("\n".join(R) + "\n")
print(f"{raw_total / 60:.1f} min -> {total / 60:.2f} min, {len(final)} pieces; read {OUT}/cutlist.md")

# ---------- check a render against the script
# Speech recognition on a long raw file sometimes hears a repeated phrase once, so a restart can
# survive the cut. A render transcribed on its own shows it. Each repeat is mapped back to its
# source file and time; --apply-check adds those drops to overrides.json for the next run.
if a.check_pieces:
    from faster_whisper import WhisperModel
    from common import HERE
    rend = os.path.join(OUT, "rough.mp4"); wav = os.path.join(OUT, "_render16k.wav")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", rend, "-vn", "-ac", "1", "-ar", "16000", wav])
    w_ = wave.open(wav); xa = np.frombuffer(w_.readframes(w_.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    model = WhisperModel("small", device="cpu", compute_type="int8", download_root=os.path.join(HERE, "models"))
    words_out, t = [], 0.0
    for i, f in enumerate(final):
        d = f["t1"] - f["t0"]
        chunk = xa[int(t * 16000):int((t + d) * 16000)]
        segs_, _ = model.transcribe(np.concatenate([np.zeros(1600, np.float32), chunk, np.zeros(1600, np.float32)]),
                                    language="en", word_timestamps=True, beam_size=5, condition_on_previous_text=False,
                                    vad_filter=False)
        for sg_ in segs_:
            for w in sg_.words or []:
                st = max(0.0, w.start - 0.1)
                words_out.append({"w": w.word.strip(), "start": round(t + st, 3), "end": round(t + min(d, max(st, w.end - 0.1)), 3), "piece": i})
        t += d
    os.remove(wav)
    jdump({"words": words_out}, os.path.join(OUT, "check_pieces.json"))
    a.check = os.path.join(OUT, "check_pieces.json")

if a.check:
    wj = [w for w in jload(a.check)["words"] if norm(w["w"])]
    rw = [norm(w["w"]) for w in wj]
    sc_all = sum((ln["toks"] for ln in L), []); owner = sum(([ln["n"]] * len(ln["toks"]) for ln in L), [])
    sm = difflib.SequenceMatcher(None, sc_all, rw, autojunk=False)
    hit = np.zeros(len(sc_all), bool); used = np.zeros(len(rw), bool)
    for b in sm.get_matching_blocks():
        hit[b.a:b.a + b.size] = True; used[b.b:b.b + b.size] = True
    miss = []
    for ln in L:
        ix = [k for k, o in enumerate(owner) if o == ln["n"]]
        cov = hit[ix].mean() if ix else 1
        if cov < 0.75: miss.append((ln["n"], round(float(cov), 2), ln["text"][:80]))
    # repeats: the same 2+ words said again within a few words, where the script does not repeat them
    sc_txt = " ".join(sc_all)
    cum, t = [], 0.0
    for f in final: cum.append(t); t += f["t1"] - f["t0"]
    def to_src(tt):
        k = max(0, int(np.searchsorted(cum, tt, side="right")) - 1)
        if k + 1 < len(cum) and cum[k + 1] - tt < 0.4: k, tt = k + 1, cum[k + 1]     # word times blur across a cut
        return k, final[k]["clip"], final[k]["t0"] + (tt - cum[k])

    def valley(clip, t):
        """quietest 10 ms just before a word that starts near t (word times can be 0.1-0.3 s off)"""
        activity(stem_i[clip]); db = db_cache[stem_i[clip]]
        a0, a1 = max(0, int((t - 0.3) * 100)), int((t + 0.1) * 100)
        sm_ = np.convolve(db[a0:a1 + 3], np.ones(3) / 3, "same")[:a1 - a0]
        return (a0 + int(np.argmin(sm_))) / 100
    reps, k = [], 0
    while k < len(rw):
        found = None
        for n in range(12, 1, -1):
            g = rw[k:k + n]
            if len(g) < n: continue
            for q in range(k + n, min(len(rw) - n + 1, k + n + 4)):
                same = all(u == v or (len(u) > 3 and difflib.SequenceMatcher(None, u, v).ratio() >= 0.8) for u, v in zip(rw[q:q + n], g))
                if same and (" ".join(g + g) not in sc_txt) and (n >= 3 or q - k <= n + 1):
                    found = (n, q); break
            if found: break
        if found:
            n, q = found
            p0, c0, s0 = to_src(wj[k]["start"]); p1, c1, s1 = to_src(wj[q]["start"])
            reps.append({"render_t": round(wj[k]["start"], 2), "words": " ".join(w["w"] for w in wj[k:q + n]),
                         "clip": c0, "drop": [valley(c0, s0), valley(c1, s1)] if c0 == c1 and s1 > s0 else None})
            k = q
        else: k += 1
    extra = []
    k = 0
    while k < len(rw):
        if not used[k]:
            e = k
            while e < len(rw) and not used[e]: e += 1
            if e - k >= 3: extra.append((round(wj[k]["start"], 1), " ".join(w["w"] for w in wj[k:e])))
            k = e
        else: k += 1
    # piece by piece (needs --check-pieces): a piece, or run of pieces, whose words are said again at the start of
    # what follows is a restart; a short piece whose words do not follow the script is listed to look at
    review = []
    if wj and "piece" in wj[0]:
        P_ = [[k for k, w in enumerate(wj) if w["piece"] == i] for i in range(len(final))]
        cum2 = np.cumsum([0] + [f["t1"] - f["t0"] for f in final])
        for i in range(len(final) - 1):
            for Lp in (1, 2, 3):
                if i + Lp >= len(final) or final[i]["clip"] != final[i + Lp]["clip"]: break
                A = [rw[k] for q in P_[i:i + Lp] for k in q]; B = [rw[k] for q in P_[i + Lp:i + Lp + 3] for k in q]
                if not A: continue
                r_ = difflib.SequenceMatcher(None, A, B[:len(A)], autojunk=False).ratio()
                if ((len(A) >= 2 and r_ >= 0.75) or (len(A) == 1 and B and A[0] == B[0])) and " ".join(A + A) not in sc_txt:
                    f0, f1 = final[i], final[i + Lp - 1]
                    reps.append({"render_t": round(float(cum2[i]), 2), "words": " ".join(wj[k]["w"] for q in P_[i:i + Lp + 1] for k in q),
                                 "clip": f0["clip"], "drop": [round(f0["t0"] - 0.02, 2), round(f1["t1"] + 0.02, 2)]})
                    break
            ix_ = P_[i]
            if len(ix_) <= 3 and final[i]["t1"] - final[i]["t0"] <= 1.5 and (not ix_ or not used[ix_].any()):
                review.append((round(float(cum2[i]), 2), final[i]["clip"], final[i]["t0"], final[i]["t1"], " ".join(wj[k]["w"] for k in ix_)))
        for r_ in review: print(f"  look at  {r_[0]:7.1f} s  {r_[1]} {r_[2]}-{r_[3]}  heard: {r_[4]!r}")
    jdump({"missing_lines": miss, "repeats": reps, "unscripted_runs": extra, "short_pieces_to_look_at": review}, os.path.join(OUT, "check.json"))
    # line-by-line comparison: what the script says, what the edit says, and the word differences
    pair = {}
    for bl in sm.get_matching_blocks():
        for q in range(bl.size): pair[bl.a + q] = bl.b + q
    C = ["# Script against the edit", "",
         "What the edit says is a fresh transcript of the render (speech recognition: names such as Claude may be",
         "heard as \"cloud\", numbers may be written differently). Missing = script words not heard in the edit;",
         "extra = words heard that the script does not have.", "",
         "| # | time in edit | script | edit says | missing | extra |", "| --- | --- | --- | --- | --- | --- |"]
    prev_end = -1; n_same = 0
    for ln in L:
        ix = [k for k, o in enumerate(owner) if o == ln["n"]]
        bs = [pair[k] for k in ix if k in pair]
        if not bs: C.append(f"| {ln['n']} | - | {ln['text']} | (not found) | all | |"); continue
        b0, b1 = prev_end + 1, max(bs)
        said = wj[b0:b1 + 1]; prev_end = b1
        sw = [norm(w["w"]) for w in said]
        d = difflib.SequenceMatcher(None, ln["toks"], sw, autojunk=False)
        mis, ext = [], []
        for op, i1, i2, j1, j2 in d.get_opcodes():
            if op in ("delete", "replace"): mis.append(" ".join(ln["toks"][i1:i2]))
            if op in ("insert", "replace"): ext.append(" ".join(w["w"] for w in said[j1:j2]))
        if not mis and not ext: n_same += 1
        C.append(f"| {ln['n']} | {int(said[0]['start'] // 60)}:{said[0]['start'] % 60:04.1f} | {ln['text']} | "
                 f"{' '.join(w['w'] for w in said)} | {'; '.join(mis)} | {'; '.join(ext)} |")
    C.insert(5, f"{n_same} of {len(L)} lines are word for word the same.")
    C.insert(6, "")
    open(os.path.join(OUT, "script_vs_edit.md"), "w").write("\n".join(C) + "\n")
    print("wrote", os.path.join(OUT, "script_vs_edit.md"))
    print(f"check: {len(miss)} lines under 75 % of their words, {len(reps)} repeats, {len(extra)} unscripted runs of 3+ words")
    for m in miss: print("  missing  line", m)
    for r in reps: print(f"  repeat   {r['render_t']:7.1f} s  {r['clip']} {r['drop']}  {r['words']}")
    for e in extra: print(f"  extra    {e[0]:7.1f} s  {e[1]}")
    if a.apply_check:
        ov.setdefault("drop", [])
        for r in reps:
            if r["drop"] and [r["clip"], *r["drop"]] not in ov["drop"]: ov["drop"].append([r["clip"], *r["drop"]])
        jdump(ov, os.path.join(OUT, "overrides.json"))
        print("added", sum(1 for r in reps if r["drop"]), "drops to overrides.json; run again with --render")

# ---------- render
if a.render:
    seg_dir = os.path.join(OUT, "_segs"); os.makedirs(seg_dir, exist_ok=True)
    for f_ in os.listdir(seg_dir): os.remove(os.path.join(seg_dir, f_))
    if a.codec == "hevc":
        vc = ["-c:v", "hevc_videotoolbox", "-b:v", a.bitrate, "-profile:v", "main10", "-pix_fmt", "p010le", "-tag:v", "hvc1"]
    elif a.codec == "prores":
        vc = ["-c:v", "prores_videotoolbox", "-profile:v", "hq"]
    else:
        vc = ["-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p"]

    def one(i):
        f = final[i]; d = f["t1"] - f["t0"]; nfr = int(round(d * fps))
        p = os.path.join(seg_dir, f"{i:04d}.mov")
        subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-ss", f"{f['t0']:.4f}", "-i", f["src"], "-t", f"{d:.4f}",
                               "-map", "0:v:0", "-map", "0:a:0", "-frames:v", str(nfr), *vc, "-g", "50",
                               "-af", f"afade=t=in:d=0.012,afade=t=out:st={max(0, d - 0.012):.4f}:d=0.012,apad,atrim=0:{d:.4f}",
                               "-c:a", "pcm_s16le", "-ar", "48000", p])
        return p
    with ThreadPoolExecutor(a.jobs) as ex: parts = list(ex.map(one, range(len(final))))
    lst = os.path.join(seg_dir, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    mov = os.path.join(OUT, "rough_master.mov")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", mov])
    mp4 = os.path.join(OUT, "rough.mp4")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", mov, "-c:v", "copy", "-c:a", "aac", "-b:a", "320k",
                           "-movflags", "+faststart", mp4])
    print("rendered", mp4)

    # Always check what was rendered, piece by piece, and fix the repeats it finds, then render again.
    # A whole-file transcript misses a phrase said twice in a row (whisper hears it once); this loop is
    # what keeps "Rule number three. Really sur- Rule number three..." out of a delivered cut.
    if not a.no_check:
        base, skip = [], False
        for x in sys.argv[1:]:
            if skip: skip = False; continue
            if x in ("--round", "--check"): skip = True; continue
            if x in ("--render", "--check-pieces", "--apply-check"): continue
            base.append(x)
        me = [sys.executable, os.path.abspath(__file__), *base]
        n0 = len(ov.get("drop", []))
        print(f"\n== check round {a.round}: transcribing the render piece by piece ==")
        subprocess.check_call([*me, "--check-pieces", "--apply-check"])
        ck = jload(os.path.join(OUT, "check.json"), {})
        added = len(jload(os.path.join(OUT, "overrides.json"), {}).get("drop", [])) - n0
        if added and a.round < a.rounds:
            print(f"round {a.round}: {added} repeats dropped; rendering again")
            sys.exit(subprocess.call([*me, "--render", "--round", str(a.round + 1)]))
        unmapped = [r for r in ck.get("repeats", []) if not r.get("drop")]
        print(f"\n== rough cut check after round {a.round} ==")
        if added: print(f"STILL {added} repeats after {a.rounds} rounds: fix them by hand (overrides.json drop / line_spans)")
        for r in unmapped: print(f"FIX BY HAND  repeat across two files at {r['render_t']} s: {r['words']}")
        if ck.get("short_pieces_to_look_at"):
            print(f"LOOK AT {len(ck['short_pieces_to_look_at'])} short pieces listed above against the audio before delivering")
        if not added and not unmapped: print("no repeats left. Read cut/script_vs_edit.md before delivering.")

