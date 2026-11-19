#!/usr/bin/env python3
"""Cut the speaker out of the footage (background removal), for layouts that put graphics behind them.

    python tools/director/matte.py <video> <out.webm> --start S --dur D [--down 0.375]

RobustVideoMatting (MobileNetV3, free, runs locally on Apple GPU / CPU) gives a temporally stable alpha matte.
Output: VP9 WebM with an alpha channel (yuva420p), same size and frame rate as the source span. Chrome plays it
with transparency, so the page can put anything behind the person.
"""
import argparse, subprocess, sys, numpy as np, torch
ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("out")
ap.add_argument("--start", type=float, default=0); ap.add_argument("--dur", type=float, required=True)
ap.add_argument("--down", type=float, default=0.375); ap.add_argument("--w", type=int, default=1920); ap.add_argument("--h", type=int, default=1080)
ap.add_argument("--fps", type=float, default=25)
a = ap.parse_args()
dev = "mps" if torch.backends.mps.is_available() else "cpu"
model = torch.hub.load("PeterL1n/RobustVideoMatting", "mobilenetv3", trust_repo=True, verbose=False).eval().to(dev)
W, H = a.w, a.h
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{a.start:.4f}", "-i", a.video, "-t", f"{a.dur:.4f}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(a.fps), "-i", "-",
                        "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "8M", "-auto-alt-ref", "0", "-row-mt", "1", "-deadline", "realtime", "-cpu-used", "8", a.out], stdin=subprocess.PIPE)
rec = [None] * 4; n = 0
with torch.no_grad():
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        src = torch.from_numpy(f).to(dev).permute(2, 0, 1)[None].float() / 255
        fgr, pha, *rec = model(src, *rec, downsample_ratio=a.down)
        alpha = (pha[0, 0].clamp(0, 1) * 255).byte().cpu().numpy()
        rgba = np.dstack([f, alpha])
        enc.stdin.write(rgba.tobytes()); n += 1
enc.stdin.close(); enc.wait(); print("frames", n)
