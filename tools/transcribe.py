#!/usr/bin/env python3
"""Word-timed transcript with faster-whisper (free, runs locally on CPU).

    python tools/transcribe.py <video-or-audio> <out_dir> [--model small] [--lang en] [--verbatim]

--verbatim primes the model to keep fillers ("um", "uh") - use it on RAW footage
for the rough cut. Published references have already had them removed.
Writes <out_dir>/words.json and transcript.txt (one line per sentence with its time).
First run downloads the model (small = about 480 MB) into tools/models/.
"""
import argparse, os, subprocess, wave
import numpy as np
from faster_whisper import WhisperModel
from common import jdump, HERE

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--model", default="small")
ap.add_argument("--lang", default=None)
ap.add_argument("--verbatim", action="store_true")
a = ap.parse_args()

tmp = os.path.join(a.out, "_tmp"); os.makedirs(tmp, exist_ok=True)
wav = os.path.join(tmp, "16k.wav")
subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-vn", "-ac", "1", "-ar", "16000", wav])
m = WhisperModel(a.model, device="cpu", compute_type="int8", download_root=os.path.join(HERE, "models"))
kw = dict(word_timestamps=True, beam_size=5, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=300))
if a.lang: kw["language"] = a.lang
if a.verbatim: kw["initial_prompt"] = "Umm, uh, so, like, you know, I mean, er, ah... okay, wait, let me say that again."
w = wave.open(wav)  # feed samples directly: avoids the PyAV decoder, which breaks across versions
audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
segs, info = m.transcribe(audio, **kw)
words, sents = [], []
for s in segs:
    sents.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()})
    for w in s.words or []:
        words.append({"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3), "p": round(w.probability, 3)})
jdump({"source": os.path.basename(a.src), "language": info.language, "model": a.model, "verbatim": a.verbatim,
       "words": words, "segments": sents}, os.path.join(a.out, "words.json"))
with open(os.path.join(a.out, "transcript.txt"), "w") as f:
    for s in sents:
        f.write(f"[{s['start']:8.2f}] {s['text']}\n")
print(f"{len(words)} words, language {info.language}")
