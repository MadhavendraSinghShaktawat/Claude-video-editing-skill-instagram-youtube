#!/usr/bin/env python3
"""Measure a sound-effects library so effects are chosen and placed on numbers, not on file names.

    python tools/director/sfx_library.py "<library folder>" <out.json> [subfolder ...]

For every audio file (wav/mp3/m4a/aif/flac) it measures:
  dur        length in seconds (after trimming leading/trailing digital silence)
  lead       silence before the sound starts (s), trimmed from placement
  lufs       integrated loudness (BS.1770 K-weighting, gated); short files fall back to RMS
  peak_db    sample peak (dBFS); clip = number of samples at full scale
  t_peak     time of the loudest 20 ms (s, from the trimmed start): a whoosh/hit is placed by this point
  attack     time from onset (-30 dB under peak) to t_peak
  tail       time from t_peak until the envelope falls 40 dB (decay/reverb length)
  rise       energy of the last third / energy of the first third (dB): > 6 means it builds (riser)
  centroid   spectral centroid (Hz): low = boomy/sub, high = airy/bright
  low        share of energy under 150 Hz (sub weight)
  width      side/mid energy ratio (dB): how stereo it is
  tonal      spectral flatness (0 = pure tone/music, 1 = noise): music stingers measure low
"""
import json, os, subprocess, sys
import numpy as np
from scipy.signal import lfilter

SR = 48000
EXT = (".wav", ".mp3", ".m4a", ".aif", ".aiff", ".flac", ".ogg")


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
    return x


def kweight(x):
    # BS.1770 pre-filter (high shelf) + RLB high-pass, coefficients for 48 kHz
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    return lfilter(b2, a2, lfilter(b1, a1, x, axis=0), axis=0)


def lufs(x):
    if len(x) < SR * 0.4:
        return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
    y = kweight(x)
    blk, hop = int(0.4 * SR), int(0.1 * SR)
    ms = np.array([np.mean(y[i:i + blk] ** 2, axis=0).sum() for i in range(0, len(y) - blk + 1, hop)])
    l = -0.691 + 10 * np.log10(ms + 1e-12)
    g = ms[l > -70]
    if not len(g): return -70.0
    rel = -0.691 + 10 * np.log10(g.mean()) - 10
    g2 = ms[(l > -70) & (l > rel)]
    return float(-0.691 + 10 * np.log10(g2.mean())) if len(g2) else -70.0


def measure(path):
    x = load(path)
    if len(x) < 480: return None
    mono = x.mean(1)
    a = np.abs(mono)
    nz = np.where(a > 10 ** (-60 / 20))[0]
    if not len(nz): return None
    s0, s1 = nz[0], nz[-1] + 1
    lead = s0 / SR
    x, mono = x[s0:s1], mono[s0:s1]
    win = int(0.02 * SR)
    env = np.sqrt(np.convolve(mono ** 2, np.ones(win) / win, "same")) + 1e-9
    envdb = 20 * np.log10(env)
    ip = int(np.argmax(env)); pk = envdb[ip]
    on = int(np.argmax(envdb > pk - 30))
    after = np.where(envdb[ip:] < pk - 40)[0]
    tail = (after[0] if len(after) else len(env) - ip) / SR
    n3 = max(1, len(mono) // 3)
    e1, e3 = np.mean(mono[:n3] ** 2) + 1e-12, np.mean(mono[-n3:] ** 2) + 1e-12
    seg = mono[max(0, ip - SR // 4): ip + SR // 4] if len(mono) > SR // 2 else mono
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2 + 1e-18
    f = np.fft.rfftfreq(len(seg), 1 / SR)
    cen = float((spec * f).sum() / spec.sum())
    low = float(spec[f < 150].sum() / spec.sum())
    flat = float(np.exp(np.mean(np.log(spec[(f > 50) & (f < 12000)]))) / np.mean(spec[(f > 50) & (f < 12000)]))
    mid, side = (x[:, 0] + x[:, 1]) / 2, (x[:, 0] - x[:, 1]) / 2
    return {
        "dur": round(len(mono) / SR, 3), "lead": round(lead, 3), "lufs": round(lufs(x), 1),
        "peak_db": round(20 * np.log10(np.abs(x).max() + 1e-9), 1), "clip": int((np.abs(x) > 0.999).sum()),
        "t_peak": round(ip / SR, 3), "attack": round((ip - on) / SR, 3), "tail": round(tail, 3),
        "rise": round(10 * np.log10(e3 / e1), 1), "centroid": int(cen), "low": round(low, 3),
        "width": round(10 * np.log10((np.mean(side ** 2) + 1e-12) / (np.mean(mid ** 2) + 1e-12)), 1),
        "tonal": round(flat, 3),
    }


def main():
    root = sys.argv[1]; out = sys.argv[2]; subs = sys.argv[3:] or sorted(os.listdir(root))
    res = []
    for sub in subs:
        d = os.path.join(root, sub)
        if not os.path.isdir(d): continue
        for fn in sorted(os.listdir(d)):
            if not fn.lower().endswith(EXT): continue
            p = os.path.join(d, fn)
            try:
                m = measure(p)
            except Exception as e:
                print("skip", fn, e); continue
            if m: res.append({"folder": sub.strip(), "file": fn, "path": p, **m})
    json.dump(res, open(out, "w"), indent=1)
    print(len(res), "files measured")


if __name__ == "__main__":
    main()
