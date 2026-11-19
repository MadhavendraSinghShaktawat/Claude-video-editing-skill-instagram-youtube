#!/usr/bin/env python3
"""Audio measurement. Nothing is listened to; everything is measured.

    python tools/audio.py <video> <out_dir> [--audio other-track.m4a] [--no-stems]

The mix is first split into a voice stem and a bed stem (music + effects + room)
with Demucs htdemucs (free, local). A separation is an estimate: expect about
+-2 dB on stem levels, and breaths or laughs can leak into the bed.
Writes <out_dir>/audio.json:
  loudness   integrated LUFS, loudness range, true peak of the delivered mix
  voice      level, share of runtime with voice, words per minute (needs words.json)
  pauses     every stretch >= 0.12 s where the voice stem is 20 dB under its median:
             count, lengths, share of runtime. This is how tight the cut is.
  word_gaps  the same from transcript word times (less exact at the edges)
  bed        music/ambience level relative to the voice, per 30 s; share of runtime
             with a bed; level while the voice is on versus in pauses (ducking)
  silences   stretches where the whole mix is under -55 dBFS for >= 0.15 s
  sfx        events in the bed stem: BB (broadband burst: whoosh, hit, click, riser)
             and LOW (20-200 Hz thump or boom), with level relative to the voice.
             Names of sounds are never claimed here; timeline.py checks each event
             against the picture.
"""
import argparse, os, re, subprocess, sys, wave
import numpy as np
from common import load_audio, stft, band_db, runmed, runs, jload, jdump, HERE, SR

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("out"); ap.add_argument("--audio", default=None)
ap.add_argument("--no-stems", action="store_true")
a = ap.parse_args()
src = a.audio or a.video
tmp = os.path.join(a.out, "_tmp")

pr = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-vn", "-i", src, "-af", "ebur128=peak=true", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
summ = pr[pr.rfind("Summary:"):]
g = lambda k: float(re.search(k + r":\s*(-?[\d.]+)", summ).group(1))
loud = {"integrated_LUFS": g("I"), "LRA_LU": g("LRA"), "true_peak_dBTP": g("Peak")}

L, R = load_audio(a.video, a.out, a.audio)
M = (L + R) / 2
dur = len(M) / SR


def rd(p):
    w = wave.open(p)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2) / 32768.0
    return (x[:, 0] + x[:, 1]) / 2


stem_dir = os.path.join(tmp, "stems", "htdemucs", "mix")
if not a.no_stems and not os.path.exists(os.path.join(stem_dir, "vocals.wav")):
    env = dict(os.environ, TORCH_HOME=os.path.join(HERE, "models", "torch"))
    subprocess.call([sys.executable, "-m", "demucs", "--two-stems", "vocals", "-n", "htdemucs", "-o", os.path.join(tmp, "stems"),
                     os.path.join(tmp, "mix.wav")], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
stems = os.path.exists(os.path.join(stem_dir, "vocals.wav"))
V = rd(os.path.join(stem_dir, "vocals.wav")) if stems else M
B = rd(os.path.join(stem_dir, "no_vocals.wav")) if stems else M
n = min(len(V), len(B), len(M)); V, B, M = V[:n], B[:n], M[:n]


def frame_db(x, hop=441):
    k = len(x) // hop
    return 10 * np.log10((x[:k * hop].reshape(k, hop) ** 2).mean(1) + 1e-14)


fv, fm = frame_db(V), frame_db(M)
nfr = len(fv)
vmed = float(np.median(fv[fv > -45])) if (fv > -45).any() else -30.0
act = fv > vmed - 20
for s, e in runs(~act):          # fill closures under 60 ms
    if e - s < 6 and s > 0 and e < nfr: act[s:e] = True
for s, e in runs(act):           # drop blips under 50 ms
    if e - s < 5: act[s:e] = False
voice_rms = float(10 * np.log10(np.mean(10 ** (fv[act] / 10)))) if act.any() else None

words = (jload(os.path.join(a.out, "words.json")) or {"words": []})["words"]
voice_d = {"stem_rms_dBFS": round(voice_rms, 1) if voice_rms is not None else None, "active_share": round(float(act.mean()), 3),
           "words": len(words), "wpm_overall": round(len(words) / dur * 60, 1),
           "wpm_while_speaking": round(len(words) / max(1e-6, act.sum() / 100) * 60, 1),
           "wpm_per_30s": [round(sum(1 for w in words if t <= w["start"] < t + 30) * 2) for t in range(0, int(dur), 30)]}

# ---- pauses on the voice stem
pz = [(s, e) for s, e in runs(~act, 12) if s > 0 and e < nfr]
pd_ = np.array([(e - s) / 100 for s, e in pz] or [0.0])
pause_stats = {"count": len(pz), "per_min": round(len(pz) / dur * 60, 1), "total_s": round(float(pd_.sum()), 1),
               "share_of_runtime": round(float(pd_.sum() / dur), 3), "median_s": round(float(np.median(pd_)), 2),
               "p25_s": round(float(np.percentile(pd_, 25)), 2), "p75_s": round(float(np.percentile(pd_, 75)), 2),
               "p90_s": round(float(np.percentile(pd_, 90)), 2), "max_s": round(float(pd_.max()), 2),
               "over_0.5s": int((pd_ > 0.5).sum()), "over_1s": int((pd_ > 1).sum()), "over_2s": int((pd_ > 2).sum())}
pauses = [{"t": round(s / 100, 2), "dur": round((e - s) / 100, 2)} for s, e in pz]
# longest run of continuous voice (no pause >= 0.12 s)
sp = np.array([(e - s) / 100 for s, e in runs(act)] or [0.0])
pause_stats["speech_run_s"] = {"median": round(float(np.median(sp)), 2), "p90": round(float(np.percentile(sp, 90)), 2), "max": round(float(sp.max()), 1)}
gaps = np.array([y["start"] - x["end"] for x, y in zip(words, words[1:]) if y["start"] - x["end"] >= 0.15] or [0.0])
word_gaps = {"count": int(len(gaps)), "median_s": round(float(np.median(gaps)), 2), "p90_s": round(float(np.percentile(gaps, 90)), 2), "max_s": round(float(gaps.max()), 2)}

sil = [{"t": round(s / 100, 2), "dur": round((e - s) / 100, 2)} for s, e in runs(fm < -55, 15)]

# ---- bed
mag, f = stft(B)
mag = mag[:nfr]
mus = band_db(mag, f, 250, 8000); full = band_db(mag, f, 20, 16000)
inner = np.zeros(nfr, bool)
for s, e in pz:
    if e - s >= 16: inner[s + 3:e - 3] = True
bed = []
for t in range(0, int(dur), 30):
    sl = slice(t * 100, min(nfr, (t + 30) * 100))
    bed.append({"t": t, "level_dBFS": round(float(np.median(mus[sl])), 1),
                "rel_voice_dB": round(float(np.median(mus[sl]) - voice_rms), 1) if voice_rms is not None else None})
rel = mus - (voice_rms if voice_rms is not None else 0)
bed_summary = {"stems": stems, "median_rel_voice_dB": round(float(np.median(rel)), 1), "p10_rel_voice_dB": round(float(np.percentile(rel, 10)), 1),
               "p90_rel_voice_dB": round(float(np.percentile(rel, 90)), 1),
               "audible_bed_share": round(float((rel > -40).mean()), 2),   # bed within 40 dB of the voice
               "while_voice_rel_dB": round(float(np.median(rel[act])), 1) if act.any() else None,
               "in_pauses_rel_dB": round(float(np.median(rel[inner])), 1) if inner.sum() > 20 else None}
if bed_summary["in_pauses_rel_dB"] is not None:
    bed_summary["duck_dB"] = round(bed_summary["in_pauses_rel_dB"] - bed_summary["while_voice_rel_dB"], 1)
# sections where the bed is clearly present / absent (5 s windows)
on = np.array([np.median(rel[i:i + 500]) > -40 for i in range(0, nfr, 500)])
bed_summary["bed_on_spans"] = [[s * 5, e * 5] for s, e in runs(on)]

# ---- sfx on the bed stem
low = band_db(mag, f, 20, 200)
edges = 300 * 2 ** (np.arange(0, 15) / 3.0)
bb = np.median(np.stack([band_db(mag, f, edges[k], edges[k + 1]) for k in range(len(edges) - 1)], 1), 1)
hi = band_db(mag, f, 2000, 16000); midb = band_db(mag, f, 200, 2000)
m_bb = (bb > runmed(bb, 401) + 8) & (bb > -62)
m_low = (low > runmed(low, 401) + 10) & (low > -38)
mask = m_bb | m_low
ev, i = [], 0
while i < nfr:
    if mask[i]:
        j = i
        while j < nfr and mask[j:j + 15].any(): j += 1
        while j > i and not mask[j - 1]: j -= 1
        if j - i >= 3: ev.append((i, j))
        i = j + 1
    else:
        i += 1
sfx = []
for s, e in ev:
    sl = slice(s, e); pk = s + int(np.argmax(full[sl]))
    P = (mag[sl] ** 2).mean(0)
    relv = float(full[pk] - voice_rms) if voice_rms is not None else None
    dec = next((k for k in range(pk, min(nfr, pk + 300)) if full[k] < full[pk] - 10), pk + 300) - pk
    sfx.append({"t": round(s / 100, 2), "dur": round((e - s) / 100, 2), "peak_t": round(pk / 100, 2),
                "kinds": [k for k, mm in (("BB", m_bb), ("LOW", m_low)) if mm[sl].any()],
                "peak_dBFS": round(float(full[pk]), 1), "rel_voice_dB": round(relv, 1) if relv is not None else None,
                "low_dB": round(float(low[sl].max()), 1), "mid_dB": round(float(midb[sl].max()), 1), "hi_dB": round(float(hi[sl].max()), 1),
                "centroid_Hz": int((P * f).sum() / (P.sum() + 1e-20)), "attack_ms": (pk - s) * 10, "decay10dB_ms": dec * 10,
                "voice_active_share": round(float(act[sl].mean()), 2), "strong": bool(relv is not None and relv >= -13)})

jdump({"source": os.path.basename(src), "duration": round(dur, 2), "stems": stems, "loudness": loud, "voice": voice_d,
       "pause_stats": pause_stats, "word_gaps": word_gaps, "bed": {"summary": bed_summary, "per_30s": bed},
       "silences": sil, "sfx_candidates": sfx, "pauses": pauses}, os.path.join(a.out, "audio.json"))
print(f"{loud} | voice {voice_d['wpm_overall']} wpm active {voice_d['active_share']} | pauses {pause_stats['count']} median {pause_stats['median_s']} max {pause_stats['max_s']} | "
      f"bed {bed_summary['median_rel_voice_dB']} dB rel voice, audible {bed_summary['audible_bed_share']} | sfx {len(sfx)} ({sum(x['strong'] for x in sfx)} strong) | silences {len(sil)}")
