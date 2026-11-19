#!/usr/bin/env bash
# Review sheets for a rendered video or chunk: 5 frames a second, 12 s per sheet (10 x 6 tiles), named by
# the output time they start at, so every frame-fifth of the edit can be read.
#   tools/director/qa_sheets.sh <video.mp4> <out_dir> [offset seconds of this file in the edit] [fps=5]
set -euo pipefail
V="$1"; O="$2"; OFF="${3:-0}"; FPS="${4:-5}"
mkdir -p "$O"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
python3 - "$V" "$O" "$OFF" "$FPS" "$DUR" <<'PY'
import sys, subprocess
v, o, off, fps, dur = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
per = 60 / fps  # seconds per sheet (60 tiles)
t = 0.0
while t < dur - 0.05:
    name = f"{o}/t{off + t:07.1f}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-t", f"{per:.3f}", "-i", v, "-vf", f"fps={fps},scale=256:-1,tile=10x6", "-frames:v", "1", name], check=True)
    t += per
PY
ls "$O" | wc -l
