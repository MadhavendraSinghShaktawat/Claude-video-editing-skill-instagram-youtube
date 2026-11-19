#!/usr/bin/env python3
"""Read every piece of on-screen text and track when it appears and disappears.

    python tools/ocr.py <video> <out_dir> [--fps 4] [--even]

If <out_dir>/shots.json exists (run visual.py first) text is read where the picture
changes: just after every cut, just after every motion event, at the end of every
shot, and once a second in between. That catches each text within about 0.1 s of
appearing at a fraction of the cost of reading every frame. Without shots.json it
samples evenly at --fps.
Runs RapidOCR (free, local, ONNX) and links the same text across samples into
tracks. Writes <out_dir>/text.json:
  tracks[]  text, t0 (first seen), t1 (first sample where it is gone), box (0-1),
            line height as a share of frame height, text colour and background
            colour, whether the text grew while on screen (typed on / built up)
  density[] [time, number of text lines] per sample (high = screen recording or UI)
"""
import argparse, os, subprocess, sys, difflib
import numpy as np, cv2
from common import probe, jdump

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("out"); ap.add_argument("--fps", type=float, default=4); ap.add_argument("--grid", type=float, default=10)
ap.add_argument("--even", action="store_true", help="ignore shots.json and sample evenly at --fps (use for pure motion graphics)")
a = ap.parse_args()
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
info = probe(a.video)
long_side = 960
if info["width"] >= info["height"]:
    W = long_side; H = int(round(info["height"] * W / info["width"] / 2) * 2)
else:
    H = long_side; W = int(round(info["width"] * H / info["height"] / 2) * 2)
from common import jload
sh = None if a.even else jload(os.path.join(a.out, "shots.json"))
if sh:
    G = a.grid; want = set()
    for s_ in sh["shots"]:
        ts = [s_["start"] + 0.12, s_["end"] - 0.08] + [e["end"] + 0.08 for e in s_.get("motion_events", [])] + [e["start"] + 0.15 for e in s_.get("motion_events", [])]
        k = s_["start"] + 1.0
        while k < s_["end"]: ts.append(k); k += 1.0
        for t in ts:
            if s_["start"] <= t <= s_["end"]: want.add(int(round(t * G)))
    # never two samples closer than 0.2 s
    keep, last = set(), -99
    for g in sorted(want):
        if g - last >= max(1, int(0.2 * G)): keep.add(g); last = g
    want = keep
else:
    G = a.fps; want = None
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.video, "-an", "-vf", f"fps={G},scale={W}:{H}",
                      "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE, bufsize=W * H * 3 * 4)


def colours(img, box):
    x0, y0, x1, y1 = [int(v) for v in box]
    crop = img[max(0, y0):y1, max(0, x0):x1].reshape(-1, 3).astype(np.float32)
    if len(crop) < 20: return None, None
    lum = crop @ np.array([0.114, 0.587, 0.299], np.float32)
    thr = (lum.min() + lum.max()) / 2
    hi, lo = crop[lum >= thr], crop[lum < thr]
    if len(hi) == 0 or len(lo) == 0: return None, None
    text, bg = (hi, lo) if len(hi) < len(lo) else (lo, hi)
    hx = lambda c: "#%02x%02x%02x" % (int(c[2]), int(c[1]), int(c[0]))
    return hx(np.median(text, 0)), hx(np.median(bg, 0))


norm = lambda s: "".join(ch for ch in s.lower() if ch.isalnum() or ch == " ").strip()
tracks, live, density = [], [], []
prev_small, prev_items = None, []
i = -1; sz = W * H * 3; nsamp = 0; t_prev = 0.0; mv = memoryview(bytearray(sz))
while True:
    got = p.stdout.readinto(mv)
    while 0 < got < sz:
        r = p.stdout.readinto(mv[got:])
        if not r: break
        got += r
    if got < sz: break
    i += 1
    if want is not None and i not in want: continue
    img = np.frombuffer(mv, np.uint8).reshape(H, W, 3)
    t = i / G; nsamp += 1
    small = cv2.cvtColor(cv2.resize(img, (160, 90)), cv2.COLOR_BGR2GRAY)
    if prev_small is not None and cv2.absdiff(small, prev_small).mean() < 0.35:
        items = prev_items  # frame unchanged: reuse
    else:
        res, _ = ocr(img)
        items = []
        for box, txt, conf in res or []:
            conf = float(conf)
            if conf < 0.6 or len(norm(txt)) < 2: continue
            xs = [q[0] for q in box]; ys = [q[1] for q in box]
            b = (min(xs), min(ys), max(xs), max(ys))
            tc, bc = colours(img, b)
            items.append({"text": txt.strip(), "n": norm(txt), "box": [b[0] / W, b[1] / H, b[2] / W, b[3] / H], "conf": conf, "tc": tc, "bc": bc})
        prev_items = items
    prev_small = small
    density.append([round(t, 2), len(items)])
    used = set()
    for it in items:
        cx, cy = (it["box"][0] + it["box"][2]) / 2, (it["box"][1] + it["box"][3]) / 2
        best, bs = None, 0
        for k, tr in enumerate(live):
            if k in used: continue
            if abs(tr["cy"] - cy) > 0.05: continue
            grew = it["n"].startswith(tr["n"][:max(3, len(tr["n"]) - 2)]) and abs(tr["box"][0] - it["box"][0]) < 0.06
            sim = difflib.SequenceMatcher(None, tr["n"], it["n"]).ratio()
            near = abs(tr["cx"] - cx) < 0.08
            score = sim if near else (0.8 if grew else 0)
            if (near and sim >= 0.7 or grew) and score > bs: best, bs = k, score
        if best is None:
            live.append({"text": it["text"], "n": it["n"], "t0": t, "t1": t, "box": it["box"], "cx": cx, "cy": cy,
                         "h": it["box"][3] - it["box"][1], "conf": it["conf"], "tc": it["tc"], "bc": it["bc"], "samples": 1, "grew": False,
                         "first_text": it["text"]})
            used.add(len(live) - 1)
        else:
            tr = live[best]; used.add(best)
            if len(it["n"]) > len(tr["n"]) + 2: tr["grew"] = True
            if len(it["n"]) >= len(tr["n"]):
                tr["text"], tr["n"], tr["box"] = it["text"], it["n"], it["box"]
                tr["h"] = it["box"][3] - it["box"][1]
            tr["cx"], tr["cy"] = cx, cy
            tr["t1"] = t; tr["samples"] += 1; tr["conf"] = max(tr["conf"], it["conf"])
    keep = []
    for tr in live:
        if tr["t1"] < t - 1e-6:                      # not seen in this sample
            tr["miss"] = tr.get("miss", 0) + 1
            tr.setdefault("gone", t)
            if tr["miss"] >= 2 or t - tr["t1"] > 0.6: tracks.append(tr); continue
        else:
            tr["miss"] = 0; tr.pop("gone", None)
        keep.append(tr)
    live = keep
    t_prev = t
p.wait()
for tr in live: tr.setdefault("gone", t_prev + 0.1)
tracks += live
out = []
for tr in sorted(tracks, key=lambda x: x["t0"]):
    end = tr.get("gone", tr["t1"] + 0.1)
    out.append({"text": tr["text"], "t0": round(tr["t0"], 2), "t1": round(end, 2), "last_seen": round(tr["t1"], 2),
                "dur": round(end - tr["t0"], 2), "samples": tr["samples"], "box": [round(v, 3) for v in tr["box"]],
                "h": round(tr["h"], 3), "conf": round(tr["conf"], 2), "text_colour": tr["tc"], "bg_colour": tr["bc"],
                "grew": tr["grew"], **({"first_text": tr["first_text"]} if tr["grew"] else {})})
jdump({"video": os.path.basename(a.video), "sampling": "picture events + 1/s" if want is not None else f"{a.fps} fps", "samples": nsamp, "tracks": out, "density": density},
      os.path.join(a.out, "text.json"))
print(f"{nsamp} samples, {len(out)} text tracks")
