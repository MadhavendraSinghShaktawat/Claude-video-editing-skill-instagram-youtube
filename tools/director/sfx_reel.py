#!/usr/bin/env python3
"""Print a reel's sound effects from a plan and mix them under the voice.

    python tools/director/sfx_reel.py <plan.json>

plan.json:
  voice      the voice track (wav), already on the output clock
  speed      composition-to-output speed (1.15 when the picture was rendered at 25/1.15 fps); event times are
             composition times and are divided by it
  out        mixed and mastered wav (-14 LUFS integrated, -1.5 dBTP ceiling)
  sfx_out    optional: the effects alone (for checking or for a Resolve track)
  sounds     name -> {path, start?, end?}  (a trim of a library file)
  events     [{t, sound, rel, semis?, align?}]
               t     composition seconds of the picture event
               rel   level of the effect against the voice, dB, measured the way tools/director/sfx_learn.py
                     measures a reference: RMS over 100 ms around the effect's loudest 20 ms, against the median
                     RMS of the voice's active 400 ms windows. Reference reels sit at -17 to -28.
               align "peak" (default: the loudest point lands on t) or "start"
               semis pitch shift in semitones (a ding ladder)
  music      optional bed: {path, offset (s into the track at output 0), under_voice_lu (integrated loudness of
             the bed below the voice's, e.g. 20), fade_in, fade_out (s), tail_lift_db (raise over the last
             tail_s seconds, where the voice has stopped), tail_s, ride_db (default 6: ride the bed's gain up to this many dB
             either way so its 3 s loudness stays under_voice_lu under the voice's; a dynamic track otherwise
             swings from 14 to 23 LU under; 0 turns it off)}. Played at its own speed on the output clock.
"""
import json, subprocess, sys
import numpy as np
from math import gcd
from scipy.signal import resample_poly

SR = 48000


def load(path, start=None, end=None):
    cmd = ["ffmpeg", "-v", "error"]
    if start is not None: cmd += ["-ss", f"{start:.4f}"]
    if end is not None: cmd += ["-t", f"{end - (start or 0):.4f}"]
    cmd += ["-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)
    return x


def rms_db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


def voice_ref(v):
    m = v.mean(1); h = int(0.4 * SR)
    r = np.array([np.sqrt(np.mean(m[i:i + h] ** 2)) for i in range(0, len(m) - h, h)])
    r = r[r > np.percentile(r, 40)]
    return float(np.median(20 * np.log10(r + 1e-12)))


def peak_and_level(x):
    m = x.mean(1); w = int(0.02 * SR)
    env = np.sqrt(np.convolve(m ** 2, np.ones(w) / w, "same"))
    ip = int(np.argmax(env)); h = int(0.05 * SR)
    return ip, rms_db(m[max(0, ip - h):ip + h])


def shift(x, semis):
    if not semis: return x
    r = 2 ** (semis / 12); up, down = 1000, int(round(1000 * r)); g = gcd(up, down)
    return resample_poly(x, up // g, down // g, axis=0)


def master(mix, out):
    tmp = out + ".pre.wav"
    import soundfile as sf
    sf.write(tmp, mix.astype(np.float32), SR, subtype="FLOAT")

    def meas(f):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        return json.loads(r[r.rfind("{"):r.rfind("}") + 1])
    gain = -14 - float(meas(tmp)["input_i"])
    for _ in range(4):
        subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af",
                               f"aresample=192000,volume={gain:.2f}dB,alimiter=limit=0.79:attack=1:release=60:level=false,aresample=48000",
                               "-c:a", "pcm_s24le", out])
        m = meas(out); err = -14 - float(m["input_i"])
        if abs(err) < 0.15: break
        gain += err
    import os; os.remove(tmp)
    return m


def main():
    P = json.load(open(sys.argv[1]))
    sp = float(P.get("speed", 1.0))
    v = load(P["voice"])
    vref = voice_ref(v)
    n = len(v)
    fx = np.zeros((n + SR * 2, 2))
    cache = {}
    log = []
    for e in P["events"]:
        s = P["sounds"][e["sound"]]
        key = (e["sound"], e.get("semis", 0))
        if key not in cache:
            x = shift(load(s["path"], s.get("start"), s.get("end")), e.get("semis", 0))
            fade = int(0.006 * SR)
            if len(x) > 2 * fade:
                x[-fade:] *= np.linspace(1, 0, fade)[:, None]
                if s.get("start"): x[:fade] *= np.linspace(0, 1, fade)[:, None]
            ip, lvl = peak_and_level(x); cache[key] = (x, ip, lvl)
        x, ip, lvl = cache[key]
        g = 10 ** ((vref + e["rel"] - lvl) / 20)
        t = e["t"] / sp
        at = int(round(t * SR)) - (ip if e.get("align", "peak") == "peak" else 0)
        a0 = max(0, at); x0 = a0 - at
        seg = x[x0:x0 + len(fx) - a0] * g
        fx[a0:a0 + len(seg)] += seg
        log.append({"t_out": round(t, 3), "sound": e["sound"], "rel": e["rel"], "gain_db": round(20 * np.log10(g), 1)})
    fx = fx[:n]
    if P.get("music"):
        mu = P["music"]
        sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
        from sfx_library import lufs
        b = load(mu["path"], mu.get("offset", 0), mu.get("offset", 0) + n / SR)
        b = np.vstack([b, np.zeros((max(0, n - len(b)), 2))])[:n]
        g = 10 ** ((lufs(v) - mu.get("under_voice_lu", 20) - lufs(b)) / 20)
        env = np.ones(n)
        fi, fo = int(mu.get("fade_in", 0.05) * SR), int(mu.get("fade_out", 0.8) * SR)
        env[:fi] = np.linspace(0, 1, fi); env[n - fo:] *= np.linspace(1, 0, fo)
        if mu.get("tail_lift_db"):
            ts = int(mu.get("tail_s", 1.0) * SR); lift = 10 ** (mu["tail_lift_db"] / 20)
            env[n - ts:] *= np.linspace(1, lift, ts)
        ride = float(mu.get("ride_db", 6))
        if ride > 0:
            hop, win = int(0.25 * SR), int(3.0 * SR)
            ts, gs = [], []
            for c in range(0, n, hop):
                a0, a1 = max(0, c - win // 2), min(n, c + win // 2)
                vl, ml = lufs(v[a0:a1]), lufs(b[a0:a1] * g)
                want = 0.0 if vl < -60 or ml < -65 else np.clip((vl - mu.get("under_voice_lu", 20)) - ml, -ride, ride)
                ts.append(c); gs.append(want)
            gs = np.convolve(np.array(gs), np.ones(4) / 4, "same")     # about 1 s of smoothing
            env *= 10 ** (np.interp(np.arange(n), ts, gs) / 20)
        bed = b * g * env[:, None]
        fx = fx + bed
        log.append({"music": mu["path"], "gain_db": round(20 * np.log10(g), 1), "voice_lufs": round(lufs(v), 1)})
    if P.get("sfx_out"):
        import soundfile as sf; sf.write(P["sfx_out"], fx.astype(np.float32), SR, subtype="FLOAT")
    m = master(v + fx, P["out"])
    json.dump({"voice_ref_rms_db": round(vref, 1), "events": log, "master": {k: m[k] for k in ("input_i", "input_tp")}},
              open(P["out"] + ".log.json", "w"), indent=1)
    print(f"{len(log)} effects, voice ref {vref:.1f} dB RMS, master {m['input_i']} LUFS / {m['input_tp']} dBTP -> {P['out']}")


if __name__ == "__main__":
    main()
