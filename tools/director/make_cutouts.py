#!/usr/bin/env python3
"""Make the alpha WebM for every cutout span the plan asked for (cutouts.json written by check.mjs).
    python tools/director/make_cutouts.py <edit.json>
Skips spans whose file already matches (same media start and length)."""
import json, os, subprocess, sys
C = json.load(open(sys.argv[1])); prj = C["project"]
src = C["cutout_source"]           # the graded cut (full resolution)
cuts = json.load(open(os.path.join(prj, "cutouts.json")))
here = os.path.dirname(os.path.abspath(__file__))
for k, c in enumerate(cuts):
    out = os.path.join(prj, "assets/media", f"cut_{k:02d}.webm"); stamp = out + ".stamp"
    key = f"{c['media']:.3f}-{c['t1'] - c['t0']:.3f}"
    if os.path.exists(out) and os.path.exists(stamp) and open(stamp).read() == key: continue
    subprocess.check_call([sys.executable, os.path.join(here, "matte.py"), src, out, "--start", f"{c['media']:.3f}", "--dur", f"{c['t1'] - c['t0'] + 0.08:.3f}"])
    open(stamp, "w").write(key); print("cut", k, key)
