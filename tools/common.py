"""Shared helpers for the analysis tools. Needs ffmpeg/ffprobe on PATH, numpy."""
import json, os, subprocess, wave
import numpy as np

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def probe(path):
    o = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                 "stream=codec_type,width,height,r_frame_rate,nb_frames:format=duration",
                                 "-of", "json", path])
    j = json.loads(o)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    out = {"duration": float(j["format"]["duration"]),
           "has_audio": any(s["codec_type"] == "audio" for s in j["streams"])}
    if v:
        n, d = v["r_frame_rate"].split("/")
        out.update(width=v["width"], height=v["height"], fps=float(n) / float(d))
    return out


def jload(p, default=None):
    return json.load(open(p)) if os.path.exists(p) else default


def jdump(obj, p, indent=1):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    json.dump(obj, open(p, "w"), indent=indent, ensure_ascii=False)


def load_audio(video, out_dir, audio=None):
    """(L, R) float arrays at 44.1 kHz. Extracted once to <out_dir>/_tmp/mix.wav."""
    p = os.path.join(out_dir, "_tmp", "mix.wav")
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", audio or video, "-vn",
                               "-ac", "2", "-ar", str(SR), p])
    w = wave.open(p)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2) / 32768.0
    return x[:, 0], x[:, 1]


def stft(x, n=1024, hop=441):
    """Hann STFT magnitude, 10 ms hop. Returns (mag[frames, bins], freqs). Chunked to bound memory."""
    win = np.hanning(n).astype(np.float32)
    pad = np.concatenate([np.zeros(n // 2), x, np.zeros(n)]).astype(np.float32)
    nfr = 1 + len(x) // hop
    out = np.empty((nfr, n // 2 + 1), np.float32)
    for a in range(0, nfr, 20000):
        b = min(nfr, a + 20000)
        idx = np.arange(n)[None, :] + hop * np.arange(a, b)[:, None]
        out[a:b] = np.abs(np.fft.rfft(pad[idx] * win, axis=1)) / (win.sum() / 2)
    return out, np.fft.rfftfreq(n, 1 / SR)


def band_db(mag, freqs, lo, hi):
    m = (freqs >= lo) & (freqs < hi)
    return 10 * np.log10((mag[:, m] ** 2).sum(1) / 1.5 / 2 + 1e-14)


def runmed(a, w):
    """Running median with window w (odd), edge padded. Subsampled for speed on long arrays."""
    h = w // 2
    p = np.pad(a, h, mode="edge")
    step = max(1, w // 40)
    idx = np.arange(0, len(a), step)
    med = np.array([np.median(p[i:i + w]) for i in idx])
    return np.interp(np.arange(len(a)), idx, med)


def runs(mask, min_len=1):
    """[(start, end_exclusive)] of True runs."""
    m = np.concatenate([[False], np.asarray(mask, bool), [False]])
    d = np.diff(m.astype(np.int8))
    s, e = np.where(d == 1)[0], np.where(d == -1)[0]
    return [(int(a), int(b)) for a, b in zip(s, e) if b - a >= min_len]
