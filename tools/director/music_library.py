#!/usr/bin/env python3
"""Measure candidate music for a bed under speech (nothing chosen by title alone).

    python tools/director/music_library.py <folder> <out.json>

Per track: length, integrated loudness, how steady it is (share of 3 s windows within 3 LU of the median, and the
spread), how much of its energy sits in the voice band (1-4 kHz, where it would mask speech), sub weight, brightness,
tempo (onset autocorrelation, 70-160 BPM), and a 10 s energy profile (to see builds, drops, intros and endings).
"""
import json, os, subprocess, sys
import numpy as np
from scipy.signal import lfilter, butter, sosfilt
SR = 22050
def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)
def band(x, lo, hi):
    sos = butter(4, [lo, hi], btype="band", fs=SR, output="sos"); return sosfilt(sos, x)
res = []
for f in sorted(os.listdir(sys.argv[1])):
    if not f.lower().endswith((".mp3", ".wav")): continue
    x = load(os.path.join(sys.argv[1], f)); n = len(x)
    w = 3 * SR; h = SR // 2
    st = np.array([10 * np.log10(np.mean(x[i:i + w] ** 2) + 1e-12) for i in range(0, n - w, h)])
    med = np.median(st[st > -50]) if (st > -50).any() else -60
    steady = float(np.mean(np.abs(st[st > -50] - med) < 3))
    tot = np.mean(x ** 2) + 1e-12
    vb = float(np.mean(band(x, 1000, 4000) ** 2) / tot); low = float(np.mean(band(x, 30, 150) ** 2) / tot)
    seg = x[: min(n, 60 * SR)]
    sp = np.abs(np.fft.rfft(seg)) ** 2; fr = np.fft.rfftfreq(len(seg), 1 / SR); cen = float((sp * fr).sum() / sp.sum())
    # tempo: onset strength = positive spectral flux of a 2048/512 STFT, autocorrelation over 70-160 BPM
    hop = 512; win = np.hanning(2048)
    frames = np.lib.stride_tricks.sliding_window_view(seg, 2048)[::hop] * win
    mag = np.abs(np.fft.rfft(frames, axis=1)); flux = np.maximum(0, np.diff(np.log1p(mag), axis=0)).sum(1)
    flux -= flux.mean(); ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
    fps = SR / hop; lags = np.arange(len(ac)); bpm = 60 * fps / np.maximum(lags, 1)
    ok = (bpm >= 70) & (bpm <= 160); tempo = float(bpm[ok][np.argmax(ac[ok])]) if ok.any() else 0
    # calmness: hits per second (onset peaks well above the local flux level) and how strong the regular beat is
    # (autocorrelation at the tempo lag relative to lag 0). Calm beds: few hits, weak pulse.
    fl = np.maximum(0, np.diff(np.log1p(mag), axis=0)).sum(1)
    thr = np.convolve(fl, np.ones(43) / 43, "same") * 1.6 + 1e-9
    pk = (fl[1:-1] > thr[1:-1]) & (fl[1:-1] > fl[:-2]) & (fl[1:-1] >= fl[2:])
    hits = float(pk.sum() / (len(fl) / fps))
    pulse = float(ac[ok].max() / (ac[0] + 1e-12)) if ok.any() else 0.0
    prof = [round(10 * np.log10(np.mean(x[i:i + 10 * SR] ** 2) + 1e-12), 1) for i in range(0, n, 10 * SR)]
    res.append({"file": f, "path": os.path.abspath(os.path.join(sys.argv[1], f)), "dur": round(n / SR, 1), "level": round(med, 1),
                "steady": round(steady, 2), "spread": round(float(np.percentile(st, 90) - np.percentile(st, 10)), 1),
                "voiceband": round(vb, 3), "low": round(low, 3), "centroid": int(cen), "bpm": round(tempo), "hits_per_s": round(hits, 2), "pulse": round(pulse, 2), "profile10s": prof})
json.dump(res, open(sys.argv[2], "w"), indent=1)
for r in sorted(res, key=lambda r: (r["pulse"], r["hits_per_s"])):
    print(f"{r['file'][:40]:40} {r['dur']:6.1f}s bpm{r['bpm']:4} hits/s{r['hits_per_s']:5.2f} pulse{r['pulse']:5.2f} steady{r['steady']:5.2f} vband{r['voiceband']:6.3f} low{r['low']:6.3f} cen{r['centroid']:5}")
