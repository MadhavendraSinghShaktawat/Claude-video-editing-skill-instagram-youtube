#!/usr/bin/env python3
"""Mix the sound of a director edit and put it on the rendered picture.

    python tools/director/mix.py work/<slug>/edit/mix.json

mix.json:
  {"voice": "<graded cut with its sound>",
   "project": "work/<slug>/edit/hf",             # reads assets/edit_data.js (insert) and cues.json (check.mjs)
   "insert_audio": "<the inserted video's own sound>",
   "music": {"under_voice_LU": 20, "xfade": 2.5,
             "sections": [{"file": "...", "from": 0, "to": 107.8, "offset": 0}, ...],   # output seconds
             "swells": [[t0, t1, dB], ...]},       # lift the bed where nobody speaks (section markers)
   "sfx": {"<cue name>": {"files": [...], "rel_LU": -14, "align": "start|peak|end", "max": 2.0, "gap": 0.12}},
   "target_lufs": -14, "true_peak": -2.2,
   "video": "<rendered picture>", "out": "<final mp4>"}

How it is placed (all measured on the files, nothing by ear):
  - every effect is loudness-matched: its level is set relative to the voice (rel_LU), not left at
    whatever level the file came in at;
  - "peak" effects (whooshes) are shifted so their loudest 20 ms lands on the cue, "end" effects
    (risers) so they finish on it; "start" effects begin on it;
  - variants of a sound are used in turn so no effect repeats back to back;
  - a cue is panned to where its element is on screen (equal-power);
  - an effect is skipped if one of the same kind already sounds within `gap` seconds, and no more than
    three effects may start inside any 0.35 s, so moments never pile up;
  - the music bed is set once under the voice, crossfades between sections, swells only where the
    voice is silent, stops while an inserted video plays its own sound.
"""
import json, os, re, subprocess, sys, tempfile
import numpy as np

SR = 48000
C = json.load(open(sys.argv[1]))
rp = lambda p: p if os.path.isabs(p) else os.path.join(os.getcwd(), p)


def load(path, ch=2):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", rp(path), "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, ch).copy()


def write(path, x):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-", "-c:a", "pcm_f32le", path], input=x.astype(np.float32).tobytes(), check=True)


def lufs(x):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f: tmp = f.name
    write(tmp, x)
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", "ebur128=framelog=quiet", "-f", "null", "-"], capture_output=True, text=True).stderr
    os.remove(tmp)
    v = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    return float(v[-1]) if v else -70.0


def fades(x, fin=0.004, fout=0.08):
    a, b = int(fin * SR), int(fout * SR)
    if len(x) > a + b:
        x[:a] *= np.linspace(0, 1, a)[:, None]; x[-b:] *= np.linspace(1, 0, b)[:, None]
    return x


prj = rp(C["project"])
cfg = json.loads(re.search(r"window\.EDIT_CONFIG=(\{.*?\});", open(os.path.join(prj, "assets/edit_data.js")).read()).group(1))
cues = sorted(json.load(open(os.path.join(prj, "cues.json"))), key=lambda c: c["t"])
total = cfg["total"]; ins = cfg.get("insert")
N = int(round(total * SR))
out = np.zeros((N, 2), np.float32)

# ---- voice, with the inserted video's own sound spliced in
v = load(C["voice"])
# A one-mic recording often lands on one channel only (video1: left -87 dB, right -14 dB), which plays in one
# ear and gets buried under centred effects. Measure both channels; if one is more than 20 dB under the other,
# use the live channel for both (dual mono, centred). Never trust a source's channel layout without measuring.
_rms = [20 * np.log10(np.sqrt(np.mean(v[:, k].astype(np.float64) ** 2)) + 1e-12) for k in (0, 1)]
if abs(_rms[0] - _rms[1]) > 20:
    live = int(np.argmax(_rms))
    print(f"voice is on one channel only (L {_rms[0]:.1f} dB, R {_rms[1]:.1f} dB): using {'LR'[live]} for both")
    v = np.repeat(v[:, live:live + 1], 2, axis=1)
voice_track = np.zeros((N, 2), np.float32)
if ins:
    a = int(round(ins["at"] * SR)); d = int(round(ins["dur"] * SR))
    voice_track[:a] = v[:a]
    rest = v[a:a + N - a - d]; voice_track[a + d:a + d + len(rest)] = rest
    out += voice_track
    ia = load(C["insert_audio"])[:d]
    out[a:a + len(ia)] += ia
else:
    voice_track[:min(N, len(v))] = v[:N]; out += voice_track
voice_lufs = lufs(v)
print("voice", round(voice_lufs, 1), "LUFS")

# ---- music: sections with crossfades, one level under the voice, swells where nobody speaks
if C.get("music"):
    MC = C["music"]; X = MC.get("xfade", 2.5); xf = int(X * SR)
    bed = np.zeros((N, 2), np.float32)
    for s in MC["sections"]:
        m = load(s["file"]); off = s.get("offset", 0)
        ref = m[int(off * SR):int((off + 120) * SR)]
        g = 10 ** ((voice_lufs - MC["under_voice_LU"] + s.get("gain", 0) - lufs(ref)) / 20)
        t0 = max(0.0, s["from"] - X / 2); t1 = min(total, s["to"] + X / 2)
        o0 = int(max(0.0, off - (s["from"] - t0)) * SR)
        a0, a1 = int(t0 * SR), int(t1 * SR)
        seg = m[o0:o0 + (a1 - a0)].copy() * g
        if len(seg) < a1 - a0: seg = np.concatenate([seg, np.zeros((a1 - a0 - len(seg), 2), np.float32)])
        r = min(xf, len(seg) // 3)
        if s["from"] > 0:
            ri = min(int(s.get("fade_in", X) * SR), len(seg) // 3)   # a section may come in on a hit (short fade)
            seg[:ri] *= np.sqrt(np.linspace(0, 1, ri))[:, None]
        seg[-r:] *= np.sqrt(np.linspace(1, 0, r))[:, None]
        bed[a0:a1] += seg
    env = np.ones(N, np.float32)
    for t0, t1, db in MC.get("swells", []):
        i0, i1 = int(t0 * SR), min(N, int(t1 * SR)); r = min(int(0.4 * SR), (i1 - i0) // 3)
        k = np.full(i1 - i0, 10 ** (db / 20), np.float32)
        k[:r] = np.linspace(1, k[0], r); k[-r:] = np.linspace(k[0], 1, r)
        env[i0:i1] *= k
    if MC.get("duck_dB"):
        # the bed dips while the voice talks (measured on the reference: 4.5 dB), attack 0.12 s, release 0.45 s
        vm = np.abs(voice_track).mean(1); fr = int(0.02 * SR); nfr = len(vm) // fr
        lev = 20 * np.log10(np.sqrt((vm[:nfr * fr].reshape(nfr, fr) ** 2).mean(1)) + 1e-9)
        on = (lev > np.median(lev[lev > -60]) - 14).astype(np.float32)
        g = np.zeros(nfr, np.float32); a_, r_ = 1 - np.exp(-1 / (0.12 / 0.02)), 1 - np.exp(-1 / (0.45 / 0.02))
        for i in range(1, nfr): g[i] = g[i - 1] + (on[i] - g[i - 1]) * (a_ if on[i] > g[i - 1] else r_)
        duck = 10 ** (-MC["duck_dB"] * g / 20)
        env[:nfr * fr] *= np.repeat(duck, fr)
    if ins:
        a = int(round((ins["at"] - 0.5) * SR)); b = int(round((ins["at"] + ins["dur"] + 0.1) * SR)); r = int(0.6 * SR)
        env[a:a + r] *= np.linspace(1, 0, r); env[a + r:b] = 0; env[b:b + r] *= np.linspace(0, 1, r)
    lift = MC.get("lift_last_s", 0)
    if lift:
        l0 = N - int(lift * SR); env[l0:] *= np.linspace(1, 10 ** (5 / 20), N - l0)
        fo = int(1.5 * SR); env[-fo:] *= np.linspace(1, 0, fo)
    out += bed * env[:, None]
    if C.get("bed_out"):
        # the music bed alone (sections, crossfades, ducking under the voice, out for the inserted video), for an
        # editor track: the voice and effects stay where they are
        write_bed = bed * env[:, None]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-", "-c:a", "pcm_s24le", rp(C["bed_out"])],
                       input=write_bed.astype(np.float32).tobytes(), check=True)
        print("bed", round(lufs(write_bed), 1), "LUFS, voice", round(voice_lufs, 1), "LUFS, peak", round(20 * np.log10(np.abs(write_bed).max() + 1e-9), 1), "dBFS ->", C["bed_out"])
        sys.exit(0)

# ---- effects
lib, rr = {}, {}
def variant(name):
    spec = C["sfx"][name]
    if name not in lib:
        vs = []
        for f in spec["files"]:
            x = load(f)
            mx = int(spec.get("max", 3.0) * SR); x = fades(x[:mx].copy(), fout=min(0.25, spec.get("max", 3.0) / 4))
            l = lufs(x) if len(x) > SR * 0.4 else 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
            x *= 10 ** ((voice_lufs + spec.get("rel_LU", -12) - l) / 20)
            env = np.convolve(np.abs(x).mean(1), np.ones(960) / 960, "same")
            vs.append((x, int(np.argmax(env))))
        lib[name] = vs; rr[name] = 0
    k = rr[name] % len(lib[name]); rr[name] += 1
    return lib[name][k], spec

last, starts, used, skipped = {}, [], {}, 0
for c in (cues if C.get("sfx") else []):     # "sfx": {} or missing = no effects at all (voice-only mix)
    name = c["name"]
    if name not in C["sfx"]: print("no sound for cue", name); continue
    spec = C["sfx"][name]
    if ins and ins["at"] - 0.3 <= c["t"] < ins["at"] + ins["dur"]: continue
    if c["t"] - last.get(name, -9) < spec.get("gap", 0.12): skipped += 1; continue
    if sum(1 for s in starts if abs(s - c["t"]) < 0.35) >= 3 and not spec.get("always"): skipped += 1; continue
    (x, pk), spec = variant(name)
    if c.get("len") and spec.get("loop"):
        need = int((c["len"] + 0.1) * SR)
        while len(x) < need: x = np.concatenate([x, x])
        x = fades(x[:need].copy(), fout=0.06)
    off = {"start": 0, "peak": pk, "end": len(x)}[spec.get("align", "start")]
    i = int(round(c["t"] * SR)) - off
    g = 10 ** (c.get("gain", 0) / 40)          # the plan's gain, at half strength around the matched level
    p = max(-1, min(1, c.get("pan", 0))) * spec.get("pan_amt", 0.6)
    lr = np.array([np.cos((p + 1) * np.pi / 4), np.sin((p + 1) * np.pi / 4)], np.float32) * np.sqrt(2)
    j0, j1 = max(0, i), min(N, i + len(x))
    if j1 <= j0: continue
    out[j0:j1] += x[j0 - i:j1 - i] * g * lr
    last[name] = c["t"]; starts.append(c["t"]); used[name] = used.get(name, 0) + 1
print("effects", used, "skipped", skipped)

def master(td, extra):
    """limit, normalise, encode; extra = dB of headroom added below the true-peak target for the AAC encoder"""
    pre0 = os.path.join(td, "pre0.wav"); write(pre0, out)
    gain = C.get("target_lufs", -14) - lufs(out)
    tgt, tp = C.get("target_lufs", -14), C.get("true_peak", -1.0) - extra
    lim = 10 ** ((tp - 0.8) / 20)
    pre = os.path.join(td, "pre.wav")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", pre0, "-af",
                           f"volume={gain:.2f}dB,aresample=192000,alimiter=limit={lim:.4f}:attack=2:release=60:level=false,aresample={SR}",
                           "-c:a", "pcm_f32le", pre])
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", pre, "-af", f"loudnorm=I={tgt}:TP={tp}:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    final = rp(C["out"]); mixwav = os.path.splitext(final)[0] + "_mix.wav"
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af",
                           f"loudnorm=I={tgt}:TP={tp}:LRA=9:measured_I={st['input_i']}:measured_TP={st['input_tp']}:measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true,aresample={SR}",
                           "-c:a", "pcm_s24le", mixwav])
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", rp(C["video"]), "-i", mixwav, "-map", "0:v:0", "-map", "1:a:0",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", final])
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", final, "-af", "ebur128=peak=true:framelog=quiet", "-f", "null", "-"], capture_output=True, text=True).stderr
    return final, float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)[-1])

# the AAC encoder overshoots the true peak of the WAV (measured about +1 dB on video1 v4): measure the encoded
# file and master again with that overshoot as extra headroom, until the delivered file meets the target
with tempfile.TemporaryDirectory() as td:
    extra, want = 0.0, C.get("true_peak", -1.0)
    for _ in range(3):
        final, li, tpk = master(td, extra)
        print(f"final: {li} LUFS, true peak {tpk} dBTP (extra headroom {extra:.1f} dB)")
        if tpk <= want + 0.05: break
        extra += tpk - want + 0.1
    print("wrote", final)
