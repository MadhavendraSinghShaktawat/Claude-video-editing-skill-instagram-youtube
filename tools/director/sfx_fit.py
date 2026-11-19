#!/usr/bin/env python3
"""Make a sound plan safe against the voice by lowering only the effects that cause a problem.

    python tools/director/sfx_fit.py <sfx_plan.json> <video with voice> [ceiling_dBFS=-1.5] [min_LU_under=8]

Repeats until clean (at most 6 passes):
  - every 50 ms window where voice + effects peaks above the ceiling: the effects sounding there are lowered
    by the overshoot (+0.3 dB);
  - every 3 s window where the voice speaks and the effects come closer than min_LU_under to it: the effects
    starting in that window are lowered by the difference (+0.5 dB).
Gains are written back into the plan; the printed files are not touched.
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
    e = (kw(x) ** 2).sum(1); c = np.concatenate([[0], np.cumsum(e)]); w, h = int(win * SR), int(hop * SR)
    idx = np.arange(0, len(e) - w, h); return idx, -0.691 + 10 * np.log10((c[idx + w] - c[idx]) / w + 1e-12)
plan_p, video = sys.argv[1], sys.argv[2]
ceil = float(sys.argv[3]) if len(sys.argv) > 3 else -1.5; gap_min = float(sys.argv[4]) if len(sys.argv) > 4 else 8.0
P = json.load(open(plan_p)); fps = P["fps"]; V = load(video); N = len(V)
cache = {c["print"]: load(c["print"]) for c in P["clips"]}
iv, lv = st(V)
for it in range(6):
    S = np.zeros_like(V); spans = []
    for c in P["clips"]:
        x = cache[c["print"]]; g = 10 ** (c["gain"] / 20); th = (c["pan"] / 100 + 1) * np.pi / 4
        i0 = int(round(c["frame"] / fps * SR)); i1 = min(N, i0 + len(x)); spans.append((i0, i1))
        if i1 > i0: S[i0:i1] += x[:i1 - i0] * g * np.array([np.cos(th), np.sin(th)]) * np.sqrt(2)
    M = np.abs(V + S).max(1); blk = int(0.05 * SR); nb = N // blk
    pk = 20 * np.log10(M[:nb * blk].reshape(nb, blk).max(1) + 1e-12)
    cuts = {}
    for b in np.where(pk > ceil)[0]:
        a0, a1 = b * blk, (b + 1) * blk
        for k, (i0, i1) in enumerate(spans):
            if i0 < a1 and i1 > a0 and P["clips"][k]["layer"] not in ("typing", "drone"):
                cuts[k] = max(cuts.get(k, 0), pk[b] - ceil + 0.3)
    _, ls = st(S)
    for i, gap, spk in zip(iv, lv - ls, lv > -30):
        if spk and gap < gap_min:
            for k, (i0, i1) in enumerate(spans):
                if i <= i0 < i + 3 * SR: cuts[k] = max(cuts.get(k, 0), gap_min - gap + 0.5)
    print(f"pass {it + 1}: peak {pk.max():.1f} dBFS, {len(cuts)} clips lowered")
    if not cuts: break
    for k, d in cuts.items(): P["clips"][k]["gain"] = round(P["clips"][k]["gain"] - d, 1)
json.dump(P, open(plan_p, "w"), indent=1)
