#!/usr/bin/env python3
"""Contact sheets with one row of evidence per shot, built from shots.json.

    python tools/shot_sheets.py <video> <out_dir> [--per-shot 3] [--cols 6] [--rows 6] [--tile-w 320]

For every shot: its first frame, middle frame and last frame (one frame for shots
under 0.5 s; long shots get an extra frame every --long-step seconds). Each tile is
labelled "#shot time" in yellow. Writes <out_dir>/shots/shots_NNN.jpg and shots_index.json
(which shots and seconds each sheet covers).
"""
import argparse, json, os
import cv2
from PIL import Image, ImageDraw, ImageFont
from common import jload, jdump

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("out")
ap.add_argument("--cols", type=int, default=6); ap.add_argument("--rows", type=int, default=6)
ap.add_argument("--tile-w", type=int, default=320); ap.add_argument("--long-step", type=float, default=4.0)
a = ap.parse_args()
sh = jload(os.path.join(a.out, "shots.json"))
fps = sh["fps"]
picks = []
for s in sh["shots"]:
    f0, f1 = s["f0"], s["f1"] - 1
    if s["dur"] < 0.5: fr = [(f0 + f1) // 2]
    else:
        n = max(3, int(s["dur"] / a.long_step) + 2)
        fr = sorted({int(round(f0 + 2 + (f1 - 4 - f0) * k / (n - 1))) for k in range(n)})
    picks += [(s["i"], f) for f in fr]

def font(size):
    for p in ("/System/Library/Fonts/Menlo.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", "C:/Windows/Fonts/consola.ttf"):
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

cap = cv2.VideoCapture(a.video)
w, h = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
tw = a.tile_w; th = int(round(tw * h / w / 2) * 2); pad = 4; per = a.cols * a.rows
od = os.path.join(a.out, "shots"); os.makedirs(od, exist_ok=True)
for old in os.listdir(od):                       # sheets from an earlier run would no longer match shots.json
    if old.startswith("shots_") and old.endswith(".jpg"): os.remove(os.path.join(od, old))
fnt = font(max(12, tw // 16)); index = []; last = -10
for si in range(0, len(picks), per):
    chunk = picks[si:si + per]
    sheet = Image.new("RGB", (a.cols * (tw + pad) + pad, a.rows * (th + pad) + pad), (28, 28, 28))
    d = ImageDraw.Draw(sheet)
    for k, (shot, f) in enumerate(chunk):
        if f != last + 1: cap.set(cv2.CAP_PROP_POS_FRAMES, f)
        ok, img = cap.read(); last = f
        if not ok: continue
        img = cv2.cvtColor(cv2.resize(img, (tw, th), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB)
        x = pad + (k % a.cols) * (tw + pad); y = pad + (k // a.cols) * (th + pad)
        sheet.paste(Image.fromarray(img), (x, y))
        label = f"#{shot} {f / fps:.2f}s"
        bb = d.textbbox((x + 3, y + 2), label, font=fnt)
        d.rectangle((bb[0] - 3, bb[1] - 2, bb[2] + 3, bb[3] + 2), fill=(0, 0, 0))
        d.text((x + 3, y + 2), label, font=fnt, fill=(255, 255, 0))
    fn = f"shots_{si // per + 1:03d}.jpg"
    sheet.save(os.path.join(od, fn), quality=85)
    index.append({"file": fn, "shots": [chunk[0][0], chunk[-1][0]], "t_start": round(chunk[0][1] / fps, 2), "t_end": round(chunk[-1][1] / fps, 2)})
jdump({"how_to_read": "tiles left-to-right, top-to-bottom; label = #shot index and time in seconds", "sheets": index}, os.path.join(od, "shots_index.json"))
print(len(index), "shot sheets ->", od)
