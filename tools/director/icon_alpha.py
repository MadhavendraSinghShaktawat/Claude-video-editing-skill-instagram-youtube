#!/usr/bin/env python3
"""Give 3D icons a real transparent background.

    python tools/director/icon_alpha.py <folder with *.webp>

The free 3dicons.co renders come down as RGB on pure white, which shows as a white square on any coloured
panel. The white that touches the border is the background: it is found by connected regions (so white
parts inside the icon stay), its edge is softened from how white each pixel is, and the white fringe is
taken back out of the colour (un-premultiplied). Files are rewritten as RGBA WebP, already-alpha files skipped.
"""
import sys, glob
import numpy as np
from PIL import Image
from scipy import ndimage

for f in sorted(glob.glob(sys.argv[1].rstrip("/") + "/*.webp")):
    im = Image.open(f)
    if im.mode == "RGBA" and np.array(im)[..., 3].min() < 250: continue
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    mn = a.min(2)
    near = mn >= 238
    lab, n = ndimage.label(near)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    band = ndimage.binary_dilation(bg, iterations=3) & ~bg
    alpha = np.ones(mn.shape, np.float32)
    alpha[bg] = 0
    # soft edge: how far from white the pixel is (a white fringe pixel is mostly background)
    alpha[band] = np.clip((255 - mn[band]) / 60.0, 0, 1)
    alpha = np.maximum(alpha, 0)
    k = np.maximum(alpha, 1e-3)[..., None]
    rgb = np.clip((a - (1 - k) * 255) / k, 0, 255)
    out = np.dstack([rgb, alpha * 255]).astype(np.uint8)
    Image.fromarray(out, "RGBA").save(f, "WEBP", quality=92, method=6)
    print("alpha", f.split("/")[-1], f"{bg.mean():.0%} background")
