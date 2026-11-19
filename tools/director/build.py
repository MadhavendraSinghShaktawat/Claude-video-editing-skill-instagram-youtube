#!/usr/bin/env python3
"""Build a HyperFrames project for a full explainer edit from a plan.

    python tools/director/build.py work/<slug>/edit/edit.json

edit.json:
  {"project": "work/<slug>/edit/hf",        # HyperFrames folder (node_modules with hyperframes, gsap, hugeicons)
   "speaker": "assets/media/speaker.mp4",   # the graded cut, re-encoded with 1 s keyframes (inside project)
   "words": "work/<slug>/cut/check_pieces.json",   # word timings on the cut timeline
   "faces": "work/<slug>/edit/faces.json",  # face boxes every 0.2 s (edit/faces.py)
   "edl": "work/<slug>/cut/edl.json",       # to know which camera setup each moment comes from
   "setups": [{"clips": ["C0696", ...], "base": 1.18, "card": 1.0}, ...],
   "insert": {"after_phrase": "watch it", "from": 600, "src": "assets/media/short.mp4", "dur": 54.0},
   "media": [{"id": "short", "src": "...", "start": .., "dur": .., "media_start": 0, "audio": false}],
   "plan": "work/<slug>/edit/plan.js"}

Writes <project>/index.html, assets/director.{js,css}, assets/icons.js, assets/edit_data.js.
The plan is plain JavaScript run in the page after director.js: it calls D.speaker, D.scene, D.words ...
"""
import json, os, re, shutil, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
cfgp = sys.argv[1]
# --range a b: only put footage that overlaps [a, b] (output seconds) into the page, for a chunked render
RANGE = None
if "--range" in sys.argv:
    k = sys.argv.index("--range"); RANGE = (float(sys.argv[k + 1]) - 2, float(sys.argv[k + 2]) + 2)
keep = lambda s0, d: RANGE is None or (s0 < RANGE[1] and s0 + d > RANGE[0])
C = json.load(open(cfgp))
base = os.path.dirname(os.path.abspath(cfgp))
rp = lambda p: p if os.path.isabs(p) else os.path.normpath(os.path.join(os.getcwd(), p))
PRJ = rp(C["project"]); A = os.path.join(PRJ, "assets")
os.makedirs(A, exist_ok=True)

words = [w for w in json.load(open(rp(C["words"])))["words"]]
edl = json.load(open(rp(C["edl"])))
cut_total = sum(s["t1"] - s["t0"] for s in edl["segments"])
fps = edl["fps"]

# camera setups: time spans on the cut and the measured face centre in each
faces = json.load(open(rp(C["faces"])))["faces"]
spans, t = [], 0.0
for s in edl["segments"]:
    d = s["t1"] - s["t0"]; spans.append((t, t + d, s["clip"])); t += d
setups = []
for su in C["setups"]:
    ts = [(a, b) for a, b, c in spans if c in su["clips"]]
    if not ts: continue
    lo, hi = min(a for a, b in ts), max(b for a, b in ts)
    F = np.array([f for f in faces if f[1] is not None and lo <= f[0] < hi])
    cx = float(np.median(F[:, 1] + F[:, 3] / 2)); cy = float(np.median(F[:, 2] + F[:, 4] / 2)); fh = float(np.median(F[:, 4]))
    setups.append({"from": lo, "to": hi, "cx": round(cx, 4), "cy": round(cy, 4), "face_h": round(fh, 4), "base": su["base"], "card": su.get("card", 1.0)})
setups.sort(key=lambda s: s["from"]); setups[0]["from"] = 0; setups[-1]["to"] = 1e9

# insert (another video played in full in the middle of the cut): find the phrase end on the cut
ins = None
if C.get("insert"):
    I = C["insert"]
    q = I["after_phrase"].lower().split()
    nw = [re.sub(r"[^a-z0-9]", "", w["w"].lower()) for w in words]
    for i in range(len(words)):
        if words[i]["start"] < I.get("from", 0): continue
        if nw[i:i + len(q)] == q:
            end = words[i + len(q) - 1]["end"]; break
    else: sys.exit("insert phrase not found")
    # cut at the next frame boundary after the phrase plus a breath of 0.35 s
    nxt = words[i + len(q)]["start"] if i + len(q) < len(words) else end + 1
    at = round(np.floor(min(end + 0.35, (end + nxt) / 2) * fps) / fps, 4)   # in the silence before the next word
    ins = {"at": at, "dur": I["dur"], "src": I["src"]}
total = cut_total + (ins["dur"] if ins else 0)

for f in ("director.js", "director.css"):
    shutil.copy(os.path.join(HERE, f), os.path.join(A, f))
os.makedirs(os.path.join(A, "fonts"), exist_ok=True)
for f in os.listdir(os.path.join(HERE, "fonts")):
    shutil.copy(os.path.join(HERE, "fonts", f), os.path.join(A, "fonts", f))

# icons used by the plan (any "SomethingIcon" string) -> svg inner markup
plan_src = open(rp(C["plan"])).read() + open(os.path.join(HERE, "director.js")).read() + "".join(open(os.path.join(HERE, f)).read() for f in C.get("theme_files", []) if f.endswith(".js"))
names = sorted(set(re.findall(r'"([A-Z][A-Za-z0-9]*Icon)"', plan_src)))
js = """
const m = require(process.argv[1] + '/node_modules/@hugeicons/core-free-icons/dist/cjs/index.js');
const out = {}; const miss = [];
for (const n of process.argv.slice(2)) {
  const ic = m[n]; if (!ic) { miss.push(n); continue; }
  out[n] = ic.map(([tag, a]) => '<' + tag + ' ' + Object.entries(a).filter(([k]) => k !== 'key').map(([k, v]) => k.replace(/[A-Z]/g, c => '-' + c.toLowerCase()) + '="' + v + '"').join(' ') + '/>').join('');
}
console.log(JSON.stringify({out, miss}));
"""
r = json.loads(subprocess.check_output(["node", "-e", js, PRJ, *names]))
if r["miss"]: print("ICONS NOT FOUND:", r["miss"])
open(os.path.join(A, "icons.js"), "w").write("window.ICONS=" + json.dumps(r["out"]) + ";\n")

# captured web pages (PNG + JSON with element boxes in image pixels) -> assets/img/cap, boxes embedded
caps = {}
if C.get("captures"):
    cd = rp(C["captures"]); od = os.path.join(A, "img", "cap"); os.makedirs(od, exist_ok=True)
    for f in sorted(os.listdir(cd)):
        if not f.endswith(".png"): continue
        n = f[:-4]; jp = os.path.join(cd, n + ".json")
        dst = os.path.join(od, n + ".jpg")
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(os.path.join(cd, f)):
            subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(cd, f), "-q:v", "2", dst])
        meta = json.load(open(jp)) if os.path.exists(jp) else {}
        from PIL import Image
        iw, ih = Image.open(os.path.join(cd, f)).size
        caps[n] = {"src": f"assets/img/cap/{n}.jpg", "w": iw, "h": ih, "boxes": meta.get("boxes", [])}

for f in C.get("theme_files", []):        # theme css/js that live with the tool
    shutil.copy(os.path.join(HERE, f), os.path.join(A, os.path.basename(f)))
cfg = {"center": C.get("center_speaker", False), "center_y": C.get("center_y", 0.42), "total": round(total, 4), "cut_total": round(cut_total, 4), "fps": fps, "insert": ins, "setups": setups}
open(os.path.join(A, "edit_data.js"), "w").write(
    "window.EDIT_CONFIG=" + json.dumps(cfg) + ";\nwindow.CAPS=" + json.dumps(caps) + ";\nwindow.EDIT_WORDS=" + json.dumps([{"w": w["w"], "start": w["start"], "end": w["end"]} for w in words]) + ";\n")
shutil.copy(rp(C["plan"]), os.path.join(A, "plan.js"))

# media elements (the runtime moves them into place; HyperFrames needs them as timed tags in the HTML)
vids = []
spk = C["speaker"]
# The footage is split into short segment files: a range render extracts every frame of each clip it
# touches, so one long clip would make every chunk extract the whole video.
SEG = C.get("speaker_segment_s", 100)
bounds = sorted(set([0.0, cut_total] + [k * SEG for k in range(1, int(cut_total // SEG) + 1) if k * SEG < cut_total] + ([ins["at"]] if ins else [])))
src_abs = os.path.join(PRJ, spk)
for k in range(len(bounds) - 1):
    a, b = bounds[k], bounds[k + 1]
    rel = f"assets/media/spk_{k:03d}.mp4"; dst = os.path.join(PRJ, rel)
    stamp = f"{a:.4f}-{b:.4f}-{os.path.getmtime(src_abs):.0f}"
    if not (os.path.exists(dst) and os.path.exists(dst + ".stamp") and open(dst + ".stamp").read() == stamp):
        subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.4f}", "-i", src_abs, "-t", f"{b - a:.4f}", "-c:v", "libx264", "-preset", "fast",
                               "-crf", "12", "-g", "25", "-bf", "0", "-pix_fmt", "yuv420p", "-an", dst])
        open(dst + ".stamp", "w").write(stamp)
    start = a + (ins["dur"] if ins and a >= ins["at"] else 0)
    if keep(start, b - a): vids.append(f'<video id="spk{k:03d}" class="clip speaker" data-start="{start:.4f}" data-duration="{b - a:.4f}" data-media-start="0" data-track-index="1" muted playsinline src="{rel}"></video>')
for k, m in enumerate(C.get("media", [])):
    start = m["start"] if not isinstance(m["start"], str) else (ins["at"] if m["start"] == "insert" else float(m["start"]))
    if keep(start, m["dur"]): vids.append(f'<video id="{m["id"]}" class="clip media" data-start="{start:.4f}" data-duration="{m["dur"]:.4f}" data-media-start="{m.get("media_start", 0):.4f}" data-track-index="{2 + k}" muted playsinline src="{m["src"]}"></video>')

# cutouts (speaker with the background removed, tools/director/matte.py): one alpha WebM per span
cuts_path = os.path.join(PRJ, "cutouts.json")
if C.get("cutouts") and os.path.exists(cuts_path):
    for k, c in enumerate(json.load(open(cuts_path))):
        rel = f"assets/media/cut_{k:02d}.webm"
        if os.path.exists(os.path.join(PRJ, rel)) and keep(c["t0"], c["t1"] - c["t0"]):
            vids.append(f'<video id="cut_{k:02d}" class="clip cutvid" data-start="{c["t0"]:.4f}" data-duration="{c["t1"] - c["t0"]:.4f}" data-media-start="0" data-track-index="9" muted playsinline src="{rel}"></video>')

html = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<link rel="stylesheet" href="assets/director.css" />
{"".join(f'<link rel="stylesheet" href="assets/{os.path.basename(x)}" />' for x in C.get("theme_files", []) if x.endswith(".css"))}
<script src="assets/gsap.min.js"></script>
</head><body>
<div id="stage" data-composition-id="main" data-start="0" data-duration="{total:.4f}" data-width="1920" data-height="1080">
<div id="media-holder" style="display:none">
{chr(10).join(vids)}
</div>
</div>
<script src="assets/icons.js"></script>
<script src="assets/edit_data.js"></script>
{"".join(f'<script src="{x}"></script>' for x in C.get("scripts", []))}
<script src="assets/director.js"></script>
{"".join(f'<script src="assets/{os.path.basename(x)}"></script>' for x in C.get("theme_files", []) if x.endswith(".js"))}
<script src="assets/plan.js"></script>
<script>D.finish();</script>
</body></html>
"""
open(os.path.join(PRJ, "index.html"), "w").write(html)
print(json.dumps({"total": cfg["total"], "insert": ins, "setups": setups, "icons": len(r["out"])}, indent=1))
