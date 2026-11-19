#!/usr/bin/env bash
# Render a director project to one silent picture file, in chunks (HyperFrames caps a render's working
# folder at 2 GB, which a long talking-head video passes), then join the chunks without re-encoding.
#   tools/director/render.sh <edit.json> <project dir> <out.mp4> [chunk seconds=180] [fps=25] [crf=14]
# HF_EXTRA adds render flags, e.g. HF_EXTRA="--resolution landscape-4k --video-frame-format png" for a 4K master.
# Each chunk gets its own page holding only the footage it overlaps (build.py --range).
set -euo pipefail
CFG="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"; PRJ="$(cd "$2" && pwd)"; OUT="$(cd "$(dirname "$3")" && pwd)/$(basename "$3")"; CH="${4:-180}"; FPS="${5:-25}"; CRF="${6:-14}"
CHD="$(dirname "$OUT")/chunks"
export HYPERFRAMES_NO_TELEMETRY=1
TOTAL=$(python3 -c "import re,json;print(json.loads(re.search(r'window\.EDIT_CONFIG=(\{.*?\});',open('$PRJ/assets/edit_data.js').read()).group(1))['total'])")
# chunk edges on whole frames; the last chunk stops one frame short of the end
EDGES=$(python3 -c "
t=$TOTAL; c=$CH; f=$FPS
n=int(t*f)-1; step=int(c*f); e=list(range(0,n,step))+[n]
print(' '.join(f'{x/f:.4f}' for x in e))")
set -- $EDGES
# ONLY="2 3" re-renders just those chunks and keeps the others from the last run
mkdir -p "$CHD"; [ -z "${ONLY:-}" ] && rm -f "$CHD/"*.mp4; rm -f "$CHD/list.txt"
i=0; prev=""
for e in $EDGES; do
  if [ -n "$prev" ]; then
    f=$(printf "%s/%03d.mp4" "$CHD" $i)
    if [ -n "${ONLY:-}" ] && ! [[ " $ONLY " == *" $i "* ]] && [ -f "$f" ]; then echo "file '$f'" >> "$CHD/list.txt"; i=$((i+1)); prev=$e; continue; fi
    echo "chunk $i: $prev - $e"
    "${PY:-python3}" "$(dirname "$0")/build.py" "$CFG" --range "$prev" "$e" > /dev/null
    (cd "$PRJ" && node_modules/.bin/hyperframes render --output "$f" --fps "$FPS" --crf "$CRF" ${HF_EXTRA:-} --start "$prev" --end "$e" --quiet > "$f.log" 2>&1) || { echo "chunk $i failed, see $f.log"; exit 1; }
    echo "file '$f'" >> "$CHD/list.txt"; i=$((i+1))
  fi
  prev=$e
done
"${PY:-python3}" "$(dirname "$0")/build.py" "$CFG" > /dev/null    # leave the full page in place
ffmpeg -v error -y -f concat -safe 0 -i "$CHD/list.txt" -c copy -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration:stream=nb_frames -of compact "$OUT"
