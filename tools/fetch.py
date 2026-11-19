#!/usr/bin/env python3
"""Download a reference video (YouTube or any yt-dlp site) for analysis.

    python tools/fetch.py <url> <slug> [--dir reference/source] [--height 1080] [--also-lang en]

Writes <dir>/<slug>.mp4 (H.264 video + the ORIGINAL-language audio track) and
<dir>/<slug>.info.json (title, chapters, duration, channel - the measured facts
YouTube publishes). With --also-lang it also saves <slug>.<lang>.m4a when the
video carries a second audio track in that language (dubbed uploads).

Local files need no fetch: pass them straight to tools/analyze.py.
"""
import argparse, json, os, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("url")
ap.add_argument("slug")
ap.add_argument("--dir", default="reference/source")
ap.add_argument("--height", type=int, default=1080)
ap.add_argument("--also-lang", default=None)
a = ap.parse_args()

os.makedirs(a.dir, exist_ok=True)
ytdlp = [sys.executable, "-m", "yt_dlp", "--no-playlist", "--no-warnings"]
out = os.path.join(a.dir, a.slug + ".mp4")

if not os.path.exists(out):
    fmt = (f"bv[height<={a.height}][vcodec^=avc1]+ba[ext=m4a]/"
           f"bv[height<={a.height}]+ba/b[height<={a.height}]/b")
    subprocess.check_call(ytdlp + ["-f", fmt, "--merge-output-format", "mp4", "-o", out, a.url])

meta = json.loads(subprocess.check_output(ytdlp + ["-J", "--skip-download", a.url]))
keep = {k: meta.get(k) for k in (
    "id", "title", "description", "channel", "channel_follower_count", "upload_date", "duration",
    "view_count", "like_count", "comment_count", "chapters", "language", "width", "height", "fps",
    "heatmap", "webpage_url")}
keep["audio_languages"] = sorted({f.get("language") for f in meta.get("formats", [])
                                  if f.get("vcodec") == "none" and f.get("language")})
json.dump(keep, open(os.path.join(a.dir, a.slug + ".info.json"), "w"), indent=1)

if a.also_lang and a.also_lang in keep["audio_languages"] and a.also_lang != (meta.get("language") or ""):
    alt = os.path.join(a.dir, f"{a.slug}.{a.also_lang}.m4a")
    if not os.path.exists(alt):
        subprocess.call(ytdlp + ["-f", f"ba[language={a.also_lang}][ext=m4a]/ba[language={a.also_lang}]",
                                 "-o", alt, a.url])
print(out)
