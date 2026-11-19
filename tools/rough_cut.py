#!/usr/bin/env python3
"""Step 1 of an edit: the rough cut. Removes dead space, filler words and retakes. Nothing else.

    python tools/transcribe.py raw.mp4 work/ --verbatim        # words with fillers kept
    python tools/audio.py raw.mp4 work/                        # voice pauses from the voice stem
    python tools/rough_cut.py raw.mp4 work/ [--style <name>] [--max-pause 0.45] [--keep-pause 0.2]
                              [--pad 0.06] [--fillers all|sounds|none] [--render]

Writes work/cut/:
  cutlist.md   every proposed removal with its time, length, reason and the words
               around it. READ IT and fix it before rendering. Retakes are guesses.
  keep.json    the spans of the source that stay (source seconds, frame aligned)
  rough.mp4    with --render: the spans joined, picture and sound, no effects
Edit keep.json or pass --drop / --restore lines in work/cut/overrides.json
({"restore": [[t0, t1], ...], "drop": [[t0, t1], ...]}) and run again.

How long a pause to keep comes from the style memory (median and 90th-percentile
pause of the reference videos) unless given on the command line.
"""
import argparse, difflib, json, os, re, subprocess, sys
from common import probe, jload, jdump, ROOT

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("work")
ap.add_argument("--style", default=None)
ap.add_argument("--max-pause", type=float, default=None, help="pauses longer than this are shortened")
ap.add_argument("--keep-pause", type=float, default=None, help="what a shortened pause is cut down to")
ap.add_argument("--pad", type=float, default=0.06, help="air kept before and after speech at a cut")
ap.add_argument("--fillers", default="sounds", choices=["all", "sounds", "none"])
ap.add_argument("--render", action="store_true")
a = ap.parse_args()

MEM = os.environ.get("EXPLAINER_EDITOR_HOME") or os.path.join(ROOT, "memory")
brand = jload(os.path.join(MEM, "brand.json"), {})
sname = a.style or brand.get("default_style")
style = jload(os.path.join(MEM, "styles", sname, "style.json")) if sname else None
if style:
    a.max_pause = a.max_pause or style["speech"]["pause_p90_s"]["median"]
    a.keep_pause = a.keep_pause or style["speech"]["pause_median_s"]["median"]
a.max_pause = a.max_pause or 0.45; a.keep_pause = a.keep_pause or 0.2

info = probe(a.video); fps, dur = info["fps"], info["duration"]
words = jload(os.path.join(a.work, "words.json"))["words"]
aj = jload(os.path.join(a.work, "audio.json"))
if not aj: sys.exit("run tools/audio.py first (voice pauses are measured on the voice stem)")
norm = lambda s: re.sub(r"[^a-z0-9' ]", "", s.lower()).strip()

SOUNDS = {"um", "umm", "uh", "uhh", "uhm", "er", "erm", "ah", "ahh", "hmm", "mm", "mhm", "eh"}
PHRASES = [["you", "know"], ["i", "mean"], ["kind", "of"], ["sort", "of"]]
SINGLE = {"like", "basically", "actually", "literally", "so", "right", "okay"}
removals = []  # (t0, t1, reason, text)

# ---- 1. dead space: voice-stem pauses longer than max_pause
for p in aj["pauses"]:
    if p["dur"] > a.max_pause:
        cut = p["dur"] - a.keep_pause
        t0 = p["t"] + a.keep_pause / 2; t1 = t0 + cut
        removals.append((t0, t1, f"pause {p['dur']:.2f}s -> {a.keep_pause:.2f}s", ""))
first = words[0]["start"] if words else 0
last = words[-1]["end"] if words else dur
if first > a.pad + 0.1: removals.append((0, first - a.pad, "before first word", ""))
if dur - last > 0.4: removals.append((last + 0.3, dur, "after last word", ""))

# ---- 2. fillers
if a.fillers != "none":
    nw = [norm(w["w"]) for w in words]
    for i, w in enumerate(words):
        if nw[i] in SOUNDS:
            removals.append((w["start"] - 0.02, w["end"] + 0.02, "filler sound", w["w"]))
        elif a.fillers == "all":
            gap_b = w["start"] - words[i - 1]["end"] if i else 1; gap_a = words[i + 1]["start"] - w["end"] if i + 1 < len(words) else 1
            if nw[i] in SINGLE and (gap_b > 0.12 or gap_a > 0.12):      # only when set apart by a pause
                removals.append((w["start"] - 0.02, w["end"] + 0.02, "filler word (check)", w["w"]))
            for ph in PHRASES:
                if nw[i:i + len(ph)] == ph and (gap_b > 0.12 or (i + len(ph) < len(words) and words[i + len(ph)]["start"] - words[i + len(ph) - 1]["end"] > 0.12)):
                    removals.append((w["start"] - 0.02, words[i + len(ph) - 1]["end"] + 0.02, "filler phrase (check)", " ".join(ph)))

# ---- 3. retakes: a phrase whose opening words are said again in one of the next three phrases
phr, cur = [], []
for i, w in enumerate(words):
    cur.append(i)
    gap = words[i + 1]["start"] - w["end"] if i + 1 < len(words) else 9
    if gap >= 0.3 or w["w"][-1:] in ".?!":
        phr.append(cur); cur = []
if cur: phr.append(cur)
txt = lambda ix: [norm(words[k]["w"]) for k in ix]
for i in range(len(phr) - 1):
    A = txt(phr[i])
    if len(A) < 2: continue
    for j in range(i + 1, min(len(phr), i + 4)):
        Bw = txt(phr[j])
        k = min(len(A), len(Bw), 6)
        if k < 2: continue
        sim = difflib.SequenceMatcher(None, " ".join(A[:k]), " ".join(Bw[:k])).ratio()
        whole = difflib.SequenceMatcher(None, " ".join(A), " ".join(Bw[:len(A) + 2])).ratio()
        if (k >= 3 and sim >= 0.85) or (len(A) <= 4 and whole >= 0.8 and len(Bw) >= len(A)):
            t0 = words[phr[i][0]]["start"] - a.pad; t1 = words[phr[j][0]]["start"] - a.pad
            removals.append((t0, t1, f"retake (said again at {words[phr[j][0]]['start']:.2f}s, keep the later take)",
                             " ".join(words[q]["w"] for q in phr[i])))
            break

# ---- overrides, merge, invert
ov = jload(os.path.join(a.work, "cut", "overrides.json"), {})
removals += [(x[0], x[1], "manual drop", "") for x in ov.get("drop", [])]
restore = ov.get("restore", [])
removals = [r for r in removals if not any(r[0] < y and r[1] > x for x, y in restore)]
removals = sorted((max(0, r[0]), min(dur, r[1]), r[2], r[3]) for r in removals if r[1] - r[0] > 1.5 / fps)
merged = []
for t0, t1, why, tx in removals:
    if merged and t0 <= merged[-1][1] + 0.05:
        merged[-1][1] = max(merged[-1][1], t1); merged[-1][2] += " + " + why
    else:
        merged.append([t0, t1, why, tx])
snap = lambda t: round(round(t * fps) / fps, 4)
keep, t = [], 0.0
for t0, t1, *_ in merged:
    if t0 - t > 2 / fps: keep.append([snap(t), snap(t0)])
    t = t1
if dur - t > 2 / fps: keep.append([snap(t), snap(dur)])
out = os.path.join(a.work, "cut"); os.makedirs(out, exist_ok=True)
kept = sum(b - x for x, b in keep)
jdump({"source": os.path.abspath(a.video), "fps": fps, "source_duration": dur, "kept_duration": round(kept, 2),
       "settings": {"max_pause": a.max_pause, "keep_pause": a.keep_pause, "pad": a.pad, "fillers": a.fillers, "style": sname},
       "keep": keep}, os.path.join(out, "keep.json"))


def ctx(t0, t1):
    b = [w["w"] for w in words if t0 - 2.5 <= w["start"] < t0][-6:]
    m = [w["w"] for w in words if t0 <= w["start"] < t1]
    af = [w["w"] for w in words if t1 <= w["start"] < t1 + 2.5][:6]
    return f"…{' '.join(b)} ~~{' '.join(m)}~~ {' '.join(af)}…"


by = {}
for r in merged:
    k = r[2].split(" ")[0]; by[k] = by.get(k, 0) + (r[1] - r[0])
L = [f"# Cut list: {os.path.basename(a.video)}", "",
     f"Source {dur:.1f} s -> rough cut {kept:.1f} s ({(1 - kept / dur) * 100:.0f} % removed, {len(merged)} removals, {len(keep)} kept spans).",
     f"Settings: pauses over {a.max_pause:.2f} s cut to {a.keep_pause:.2f} s, pad {a.pad:.2f} s, fillers = {a.fillers}, style = {sname}.",
     "Seconds removed by reason: " + ", ".join(f"{k} {v:.1f}" for k, v in sorted(by.items(), key=lambda kv: -kv[1])), "",
     "Struck-through words are removed. Retakes and '(check)' fillers are guesses: confirm each one. To undo a removal add its span to `overrides.json` under `restore`.", "",
     "| # | from | to | length | reason | context |", "| --- | --- | --- | --- | --- | --- |"]
for i, (t0, t1, why, tx) in enumerate(merged):
    if why.startswith("pause") and "+" not in why and t1 - t0 < 1.0: continue   # routine tightening is summarised, not listed
    L.append(f"| {i} | {t0:.2f} | {t1:.2f} | {t1 - t0:.2f} | {why} | {ctx(t0, t1)} |")
open(os.path.join(out, "cutlist.md"), "w").write("\n".join(L) + "\n")
print(f"{dur:.1f}s -> {kept:.1f}s, {len(merged)} removals; read {out}/cutlist.md")

if a.render:
    sel = "+".join(f"between(t,{x},{y - 0.5 / fps:.4f})" for x, y in keep)
    graph = f"[0:v]select='{sel}',setpts=N/FRAME_RATE/TB[v];[0:a]aselect='{sel}',asetpts=N/SR/TB[a]"
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
                           "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "aac", "-b:a", "256k", os.path.join(out, "rough.mp4")])
    print("rendered", os.path.join(out, "rough.mp4"))
