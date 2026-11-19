#!/usr/bin/env python3
"""Shortlist library sounds for each effect class a reference uses, by listening (earshot's CLAP model):
how close each candidate is to the reference's own effect clips, plus how well it fits a one-line description.

    python tools/director/sfx_rank.py reference/analysis/<slug> <catalogue.json> [more catalogues] \
        [--max-dur 3] [--skip ES_ MEME] [--top 8]

Needs sfx_learned.json (tools/director/sfx_learn.py) and the stems from tools/analyze.py. Writes sfx_rank.json in the
analysis folder. Scores are z-scores within the candidate set: text_z (fits the description) + ref_z (sounds like the
reference's clips of that class); quote them when you report a choice.
"""
import argparse, json, os, subprocess, sys, glob
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "vendor", "earshot"))

ap = argparse.ArgumentParser()
ap.add_argument("analysis"); ap.add_argument("catalogues", nargs="+")
ap.add_argument("--max-dur", type=float, default=3.0); ap.add_argument("--skip", nargs="*", default=["ES_"])
ap.add_argument("--top", type=int, default=8)
a = ap.parse_args()
from earshot import vocab
L = json.load(open(os.path.join(a.analysis, "sfx_learned.json")))
nv = glob.glob(os.path.join(a.analysis, "_tmp/stems/**/no_vocals.wav"), recursive=True)[0]
clips = os.path.join(a.analysis, "_tmp/sfx_clips"); os.makedirs(clips, exist_ok=True)
refs = {}
for k, e in enumerate(L["events"]):
    p = f"{clips}/{e['class']}_{k:02d}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, e['peak_t'] - 0.08):.3f}", "-t", f"{max(0.25, e['length'] + 0.15):.3f}", "-i", nv, p], check=True)
    refs.setdefault(e["class"], []).append(p)
cands = []
for c in a.catalogues:
    base = os.path.dirname(os.path.abspath(c))
    for i in json.load(open(c)):
        p = i["path"] if os.path.isabs(i["path"]) else os.path.join(ROOT, i["path"])
        if i.get("dur", 0) <= a.max_dur and not any(s in p for s in a.skip) and os.path.exists(p): cands.append(p)
v = vocab.get()
A = vocab.embed_files(cands); A /= np.linalg.norm(A, axis=1, keepdims=True)
z = lambda s: (s - s.mean()) / (s.std() + 1e-9)
out = {}
for c, q in L["class_queries"].items():
    if c not in refs: continue
    T = v.embed_text([q])[0]; T /= np.linalg.norm(T)
    R = vocab.embed_files(refs[c]); R /= np.linalg.norm(R, axis=1, keepdims=True)
    tz, rz = z(A @ T), z((A @ R.T).max(1))
    o = np.argsort(-(tz + rz))[:a.top]
    out[c] = [{"path": os.path.relpath(cands[i], ROOT) if cands[i].startswith(ROOT) else cands[i], "text_z": round(float(tz[i]), 2),
               "ref_z": round(float(rz[i]), 2), "score": round(float(tz[i] + rz[i]), 2)} for i in o]
    print(f"{c} ({len(refs[c])} reference clips, '{q}')")
    for r in out[c]: print(f"   {r['score']:5.2f}  text {r['text_z']:5.2f}  ref {r['ref_z']:5.2f}  {r['path']}")
json.dump(out, open(os.path.join(a.analysis, "sfx_rank.json"), "w"), indent=1)
