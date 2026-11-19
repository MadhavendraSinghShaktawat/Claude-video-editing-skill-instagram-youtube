#!/usr/bin/env python3
"""Check a sound plan against the voice before it goes into the editor (nothing by ear, all measured).

    python tools/director/sfx_check.py <sfx_plan.json> <video with voice> [preview.wav]

  - alignment: each printed file's aligned point really lands on its event time (ms error)
  - level: short-term loudness (3 s) of the effects alone vs the voice; while the voice speaks the effects
    must stay at least 8 LU under it (lists the seconds where they do not)
  - peaks: true-peak-ish sample peak of voice + effects together
  - density: effects starting per 10 s
Writes a preview mix (voice + effects, gains and pans applied) when a path is given.
"""
import json, subprocess, sys
import numpy as np
from scipy.signal import lfilter
SR = 48000
def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
def kw(x):
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    return lfilter(b2, a2, lfilter(b1, a1, x, axis=0), axis=0)
def st(x, win=3.0, hop=0.5):
    y = kw(x) ** 2; e = y.sum(1); c = np.concatenate([[0], np.cumsum(e)]); w = int(win * SR); h = int(hop * SR)
    idx = np.arange(0, len(e) - w, h); return idx / SR + win / 2, -0.691 + 10 * np.log10((c[idx + w] - c[idx]) / w + 1e-12)
P = json.load(open(sys.argv[1])); fps = P["fps"]
V = load(sys.argv[2]); N = len(V); S = np.zeros_like(V)
errs = []
for c in P["clips"]:
    x = load(c["print"]); g = 10 ** (c["gain"] / 20); th = (c["pan"] / 100 + 1) * np.pi / 4
    i0 = int(round(c["frame"] / fps * SR)); i1 = min(N, i0 + len(x))
    S[i0:i1] += x[:i1 - i0] * g * np.array([np.cos(th), np.sin(th)]) * np.sqrt(2)
    if c["layer"] not in ("typing", "drone"):
        env = np.convolve(np.abs(x).mean(1), np.ones(960) / 960, "same")
        lo = max(0, int((c["t"] - c["frame"] / fps - 0.3) * SR)); hi = min(len(env), int((c["t"] - c["frame"] / fps + 0.3) * SR))
        if hi > lo: errs.append((abs((lo + np.argmax(env[lo:hi])) / SR + c["frame"] / fps - c["t"]) * 1000, c["layer"], c["t"], c["file"]))
errs.sort(reverse=True)
print(f"alignment: median {np.median([e[0] for e in errs]):.1f} ms, worst {errs[0][0]:.1f} ms ({errs[0][1]} at {errs[0][2]})")
tv, lv = st(V); ts, ls = st(S)
speak = lv > -30
gap = lv - ls
bad = [(round(t, 1), round(g, 1)) for t, g, s in zip(tv, gap, speak) if s and g < 8]
print(f"voice vs effects while speaking: median {np.median(gap[speak]):.1f} LU under, min {gap[speak].min():.1f} LU")
print("seconds with effects < 8 LU under the voice:", bad[:40], "..." if len(bad) > 40 else "")
M = V + S
print(f"peak voice {20*np.log10(np.abs(V).max()):.1f} dBFS, peak voice+fx {20*np.log10(np.abs(M).max()):.1f} dBFS")
starts = np.array([c["frame"] / fps for c in P["clips"]])
h, _ = np.histogram(starts, bins=np.arange(0, N / SR + 10, 10))
print("effects per 10 s: median", int(np.median(h)), "max", int(h.max()), "at", int(np.argmax(h)) * 10, "s")
if len(sys.argv) > 3:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f64le", "-ac", "2", "-ar", str(SR), "-i", "-", "-c:a", "pcm_s24le", sys.argv[3]], input=M.tobytes(), check=True)
    print("wrote", sys.argv[3])
