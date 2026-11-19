#!/usr/bin/env python3
"""Measure one video end to end. Works on a reference video, or on your own old videos.

    python tools/analyze.py <video-file-or-URL> --slug my-video [--out reference/analysis]
                            [--lang en] [--audio alt-track.m4a] [--ocr-fps 4] [--skip ocr,sheets]

Steps (each writes into <out>/<slug>/ and is skipped if its output exists):
  fetch      URL -> reference/source/<slug>.mp4 + .info.json          (tools/fetch.py)
  visual     every frame: cuts, camera moves, faces, motion events     -> frames.npz, shots.json
  words      word-timed transcript                                     -> words.json, transcript.txt
  text       every on-screen text with its on/off time                 -> text.json
  audio      loudness, pauses, music level, sound-effect candidates    -> audio.json
  sheets     labelled contact sheets, a few frames per shot            -> shots/*.jpg
  timeline   all of it joined per shot + the style numbers             -> timeline.md/json, summary.json

Then LOOK: read timeline.md beside shots/*.jpg. The numbers say what happened and
when; only the frames say what a graphic was for.
"""
import argparse, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("--slug", required=True)
ap.add_argument("--out", default=os.path.join(ROOT, "reference", "analysis"))
ap.add_argument("--lang", default=None); ap.add_argument("--audio", default=None)
ap.add_argument("--ocr-fps", default="4"); ap.add_argument("--skip", default="")
ap.add_argument("--force", action="store_true")
a = ap.parse_args()
skip = set(a.skip.split(","))
out = os.path.join(os.path.abspath(a.out), a.slug); os.makedirs(out, exist_ok=True)   # tools run with cwd=tools/, so make it absolute
py = sys.executable
run = lambda *c: subprocess.check_call([py, *c], cwd=HERE)
have = lambda n: os.path.exists(os.path.join(out, n)) and not a.force

video, info = a.src, None
if a.src.startswith("http"):
    srcdir = os.path.join(ROOT, "reference", "source")
    video = os.path.join(srcdir, a.slug + ".mp4"); info = os.path.join(srcdir, a.slug + ".info.json")
    if not os.path.exists(video): run("fetch.py", a.src, a.slug, "--dir", srcdir)
else:
    video = os.path.abspath(a.src)
    cand = os.path.splitext(video)[0] + ".info.json"
    info = cand if os.path.exists(cand) else None

if not have("shots.json"): run("visual.py", video, out)
if not have("words.json"): run("transcribe.py", a.audio or video, out, *(["--lang", a.lang] if a.lang else []))
if "ocr" not in skip and not have("text.json"): run("ocr.py", video, out, "--fps", a.ocr_fps)
if not have("audio.json"): run("audio.py", video, out, *(["--audio", a.audio] if a.audio else []))
if "sheets" not in skip and not have("shots/shots_index.json"): run("shot_sheets.py", video, out)
run("timeline.py", out, *(["--info", info] if info else []))
print("done ->", out)
