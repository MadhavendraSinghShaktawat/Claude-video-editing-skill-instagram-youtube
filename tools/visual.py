#!/usr/bin/env python3
"""Frame-by-frame visual measurement. Every frame of the video is read.

    python tools/visual.py <video> <out_dir>

Pass 1 (every frame, 320x180 grey + colour histogram):
  d      mean absolute pixel change from the previous frame (0-255)
  hist   colour-histogram distance from the previous frame (0-1)
  scale, tx, ty, inl   global similarity transform prev->cur from tracked corners
                       (Lucas-Kanade + RANSAC). scale>1 = picture grew = zoom in.
  resid  share of pixels still different after undoing that transform (things that
         appeared, disappeared or animated, as opposed to the camera moving)
  rbox   bounding box of those changed pixels
  face   largest face every 0.25 s (YuNet; Haar fallback): box + score
Pass 2 derives, with no human judgement:
  cuts        hard (new picture) / punch (same picture, instant scale jump) /
              jump (same picture, instant shift) / pop (instant change in part of
              the frame: a graphic appearing) / transition (multi-frame)
  shots       spans between cuts, each with camera move, face size and position,
              motion events inside the shot, flatness (graphic vs footage) and colours
  zooms       eased zoom segments inside shots (start, end, factor, peak position)
Writes <out_dir>/frames.npz, shots.json.
"""
import os, subprocess, sys, urllib.request
import numpy as np
import cv2
from common import probe, jdump, runs, HERE

W, H = 320, 180
FW, FH = 640, 360
YUNET_URL = "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"


def face_detector():
    p = os.path.join(HERE, "models", "face_detection_yunet_2023mar.onnx")
    try:
        if not os.path.exists(p):
            os.makedirs(os.path.dirname(p), exist_ok=True)
            urllib.request.urlretrieve(YUNET_URL, p)
        det = cv2.FaceDetectorYN.create(p, "", (FW, FH), 0.6, 0.3, 50)

        def f(img):
            _, r = det.detect(img)
            if r is None: return []
            return [(float(x[0]), float(x[1]), float(x[2]), float(x[3]), float(x[14])) for x in r]
        return f, "yunet"
    except Exception as e:  # offline or API missing
        print("YuNet unavailable (%s); using Haar cascade" % e, file=sys.stderr)
        cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        def f(img):
            g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return [(float(x), float(y), float(w), float(h), 0.5) for x, y, w, h in cas.detectMultiScale(g, 1.1, 5, minSize=(30, 30))]
        return f, "haar"


def pass1(video, out_dir):
    info = probe(video)
    fps = info["fps"]
    n_est = int(info["duration"] * fps) + 8
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", video, "-an", "-vf", f"scale={FW}:{FH}",
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE, bufsize=FW * FH * 3 * 8)
    d = np.zeros(n_est, np.float32); hd = np.zeros(n_est, np.float32)
    sc = np.ones(n_est, np.float32); tx = np.zeros(n_est, np.float32); ty = np.zeros(n_est, np.float32)
    inl = np.zeros(n_est, np.float32); resid = np.zeros(n_est, np.float32)
    rbox = np.zeros((n_est, 4), np.float32)
    hists = np.zeros((n_est, 48), np.float32)
    luma = np.zeros(n_est, np.float32)
    faces = []  # (frame, x, y, w, h, score, count) normalised
    detect, det_name = face_detector()
    face_every = max(1, int(round(fps * 0.25)))
    lk = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    prev = None; i = 0; sz = FW * FH * 3
    while True:
        buf = p.stdout.read(sz)
        if len(buf) < sz: break
        big = np.frombuffer(buf, np.uint8).reshape(FH, FW, 3)
        small = cv2.resize(big, (W, H), interpolation=cv2.INTER_AREA)
        g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        h = np.concatenate([np.bincount(small[:, :, c].ravel() >> 4, minlength=16) for c in range(3)]).astype(np.float32)
        h /= (W * H)
        if i >= n_est:  # container under-reported; grow
            grow = lambda a: np.concatenate([a, np.zeros_like(a)])
            d, hd, tx, ty, inl, resid, rbox, hists, luma = map(grow, (d, hd, tx, ty, inl, resid, rbox, hists, luma))
            sc = np.concatenate([sc, np.ones_like(sc)]); n_est *= 2
        hists[i] = h; luma[i] = g.mean()
        if prev is not None:
            d[i] = cv2.absdiff(g, prev).mean()
            hd[i] = 0.5 * np.abs(h - hists[i - 1]).sum() / 3
            pts = cv2.goodFeaturesToTrack(prev, 200, 0.01, 7)
            M = None
            if pts is not None and len(pts) >= 12:
                nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev, g, pts, None, **lk)
                ok = st.ravel() == 1
                if ok.sum() >= 12:
                    M, mask = cv2.estimateAffinePartial2D(pts[ok], nxt[ok], method=cv2.RANSAC, ransacReprojThreshold=1.5)
                    if M is not None:
                        s = float(np.hypot(M[0, 0], M[1, 0]))
                        if 0.5 < s < 2.0:
                            sc[i] = s; tx[i] = M[0, 2] + (M[0, 0] - 1) * W / 2 + M[0, 1] * H / 2
                            ty[i] = M[1, 2] + M[1, 0] * W / 2 + (M[1, 1] - 1) * H / 2
                            inl[i] = float(mask.sum()) / len(pts)
                        else:
                            M = None
            ref = cv2.warpAffine(prev, M, (W, H), borderMode=cv2.BORDER_REPLICATE) if M is not None else prev
            ch = cv2.absdiff(g, ref) > 28
            ch[:3] = ch[-3:] = False; ch[:, :3] = ch[:, -3:] = False
            resid[i] = ch.mean()
            if resid[i] > 0.004:
                ys, xs = np.where(ch)
                rbox[i] = (np.percentile(xs, 2) / W, np.percentile(ys, 2) / H, np.percentile(xs, 98) / W, np.percentile(ys, 98) / H)
        if i % face_every == 0:
            fs = detect(big)
            if fs:
                x, y, w, hh, s = max(fs, key=lambda f: f[2] * f[3])
                faces.append((i, x / FW, y / FH, w / FW, hh / FH, s, len(fs)))
            else:
                faces.append((i, 0, 0, 0, 0, 0, 0))
        prev = g; i += 1
    p.wait()
    n = i
    np.savez_compressed(os.path.join(out_dir, "frames.npz"), fps=fps, n=n, d=d[:n], hist=hd[:n], scale=sc[:n], tx=tx[:n] / W,
                        ty=ty[:n] / H, inl=inl[:n], resid=resid[:n], rbox=rbox[:n], hists=hists[:n].astype(np.float16),
                        luma=luma[:n], faces=np.array(faces, np.float32), face_detector=det_name)
    return n


def local_median(a, half):
    from common import runmed
    return runmed(a, 2 * half + 1)


def pass2(video, out_dir):
    z = np.load(os.path.join(out_dir, "frames.npz"))
    src_fps = float(z["fps"]); n_src = int(z["n"])
    faces = z["faces"]
    # Many uploads hold duplicated frames (24 or 30 fps material in a 60 fps file, or a
    # screen recording that only changes now and then). A duplicate carries no information
    # and would make every real frame look like a one-frame spike, so all detection runs on
    # the frames that differ from the one before. F maps back to source frames, T to seconds.
    d_all = z["d"]
    pad = np.pad(d_all, 2, mode="edge")
    near_max = np.max(np.stack([pad[k:k + len(d_all)] for k in range(5)]), 0)
    dup = (d_all < 0.03) | ((d_all < 0.3) & (d_all < 0.05 * near_max))   # exact repeats, or repeats with compression noise
    F = np.concatenate([[0], np.where(~dup[1:])[0] + 1])
    T = F / src_fps
    d, hd, sc, tx, ty, inl, resid, rbox = (z[k][F] for k in ("d", "hist", "scale", "tx", "ty", "inl", "resid", "rbox"))
    hists = z["hists"][F].astype(np.float32)
    n = len(F)
    dt = np.diff(T, prepend=T[0] - 1 / src_fps)
    fps = float(1 / np.median(dt[1:])) if n > 2 else src_fps      # effective frame rate of the content
    dt = np.minimum(dt, 2 / fps)
    half = max(6, int(fps * 0.4))
    base = local_median(d, half)
    ls = np.log(sc)
    tm = lambda k: round(float(T[min(k, n - 1)]), 3)

    # ---- instant cuts: a one-frame spike in pixel change
    cuts = {}
    for i in range(1, n):
        nb = max(d[i - 1] if i > 1 else 0, d[i + 1] if i + 1 < n else 0)
        if d[i] > max(3.5, 3.0 * base[i]) and d[i] > 1.6 * nb:   # 3.5 floor: weaker spikes fall in voice pauses no more often than chance
            if hd[i] > 0.22:
                kind = "hard"
            elif inl[i] >= 0.35 and abs(ls[i]) >= 0.02:
                kind = "punch"
            elif inl[i] >= 0.35 and abs(ls[i]) < 0.02:
                kind = "jump"
            elif inl[i] >= 0.2 and abs(ls[i]) >= 0.03 and hd[i] <= 0.12:
                kind = "punch"
            else:
                kind = "hard" if hd[i] > 0.12 else "jump"
            cuts[i] = {"frame": int(F[i]), "t": tm(i), "kind": kind, "d": round(float(d[i]), 1), "hist": round(float(hd[i]), 3)}
            if kind == "jump":   # an instant change confined to part of the frame is a graphic popping in, not a cut in the footage
                bx = rbox[i]; area = float((bx[2] - bx[0]) * (bx[3] - bx[1]))
                if 0 < area < 0.3:
                    kind = cuts[i]["kind"] = "pop"; cuts[i]["box"] = [round(float(v), 2) for v in bx]
            if kind in ("punch", "jump"):
                cuts[i].update(scale=round(float(sc[i]), 3), shift=[round(float(tx[i]), 3), round(float(ty[i]), 3)])
    # ---- multi-frame transitions: the picture 0.2 s before differs from the picture 0.2 s after
    # (dissolve, blur-through, wipe, morph) with no instant cut between them.
    k = max(2, int(round(fps * 0.2)))
    hw = np.zeros(n, np.float32)
    if n > 2 * k: hw[k:n - k] = 0.5 * np.abs(hists[2 * k:] - hists[:-2 * k]).sum(1) / 3
    w = max(3, int(fps * 0.4))
    instant = sorted(cuts)
    for i in range(k, n - k):
        if hw[i] < 0.2 or hw[i] < hw[max(0, i - w):i + w + 1].max(): continue
        if any(i - k - 2 <= c <= i + k + 2 for c in instant): continue
        if any(abs(i - c) < w for c in cuts if cuts[c]["kind"] == "transition"): continue
        a0, b0 = max(1, i - 3 * k), min(n, i + 3 * k)
        for c in instant:
            if a0 <= c < i: a0 = c + 1
            if i < c < b0: b0 = c
        cs = np.cumsum(hd[a0:b0]); tot = cs[-1] if len(cs) else 0
        if tot <= 0: continue
        ta = a0 + int(np.searchsorted(cs, 0.1 * tot)); tb = min(n - 1, a0 + int(np.searchsorted(cs, 0.9 * tot)) + 1)
        cuts[i] = {"frame": int(F[i]), "t": tm(i), "kind": "transition", "start": tm(ta), "end": tm(tb),
                   "frames": int(round((T[tb] - T[ta]) * fps)), "hist": round(float(hw[i]), 3)}
    cut_idx = sorted(cuts)

    # ---- shots
    bounds = [0] + cut_idx + [n]
    ft = faces[:, 0].astype(int)
    shots = []
    zoom_rate = ls / dt  # log-scale per second
    dur_total = n_src / src_fps
    for q in range(len(bounds) - 1):
        a, b = bounds[q], bounds[q + 1]
        if b - a < 1: continue
        f0 = int(F[a]); f1 = int(F[b]) if b < n else n_src
        t0 = f0 / src_fps; t1 = f1 / src_fps
        s = {"i": len(shots), "start": round(t0, 3), "end": round(t1, 3), "dur": round(t1 - t0, 3),
             "f0": f0, "f1": f1, "cut_in": cuts[a]["kind"] if a in cuts else "start"}
        if a in cuts and "scale" in cuts[a]: s["cut_in_scale"] = cuts[a]["scale"]
        inner = slice(a + 1, b)
        good = inl[inner] >= 0.3
        if good.sum() >= 2:
            tot = float(ls[inner][good].sum())
            px, py = float(tx[inner][good].sum()), float(ty[inner][good].sum())
            jit = float(np.hypot(np.diff(tx[inner][good]), np.diff(ty[inner][good])).mean()) if good.sum() > 3 else 0.0
            s["camera"] = {"zoom_total": round(float(np.exp(tot)), 4), "zoom_pct_per_s": round((np.exp(tot) - 1) * 100 / max(s["dur"], 1e-3), 2),
                           "pan_x": round(px, 4), "pan_y": round(py, 4), "jitter": round(jit, 5), "tracked_share": round(float(good.mean()), 2)}
            zr = np.where(good, zoom_rate[inner], 0)
            segs = []
            for za, zb in runs(np.abs(zr) > 0.06, max(2, int(fps * 0.1))):
                f = float(np.exp(ls[inner][za:zb].sum()))
                if abs(f - 1) < 0.02: continue
                pk = za + int(np.argmax(np.abs(zr[za:zb])))
                segs.append({"start": tm(a + 1 + za), "end": tm(a + 1 + zb), "factor": round(f, 3),
                             "peak_at": round((pk - za) / max(1, zb - za), 2), "peak_pct_per_s": round(float((np.exp(abs(zr[pk])) - 1) * 100), 1)})
            if segs: s["zoom_moves"] = segs
            c = s["camera"]
            if segs: mv = "eased zoom " + ("in" if sum(np.log(x["factor"]) for x in segs) > 0 else "out")
            elif abs(c["zoom_total"] - 1) >= 0.012: mv = "slow push in" if c["zoom_total"] > 1 else "slow pull out"
            elif abs(px) >= 0.012 or abs(py) >= 0.012: mv = "pan/slide"
            else: mv = "static"
            if mv == "static" and jit > 0.0015: mv = "static (handheld jitter)"
            s["move"] = mv
        else:
            s["move"] = "untracked (full-frame animation, still, or too short)"
        # motion events inside the shot (not explained by camera): bursts of residual change
        r = resid[inner]
        rb = local_median(r, int(fps)) if len(r) > 3 else r
        ev = []
        for ea, eb in runs(r > np.maximum(0.012, 3 * rb), 1):
            bb = rbox[inner][ea:eb]; bb = bb[bb[:, 2] > 0]
            if not len(bb): continue
            box = [float(bb[:, 0].min()), float(bb[:, 1].min()), float(bb[:, 2].max()), float(bb[:, 3].max())]
            st, en = tm(a + 1 + ea), tm(a + 1 + eb)
            if ev and st - ev[-1]["end"] < 0.25:
                e = ev[-1]; e["end"] = en; e["peak"] = round(max(e["peak"], float(r[ea:eb].max())), 3)
                e["box"] = [round(min(e["box"][0], box[0]), 2), round(min(e["box"][1], box[1]), 2), round(max(e["box"][2], box[2]), 2), round(max(e["box"][3], box[3]), 2)]
            else:
                ev.append({"start": st, "end": en, "peak": round(float(r[ea:eb].max()), 3), "box": [round(v, 2) for v in box]})
        if ev: s["motion_events"] = ev
        s["activity"] = round(float(np.median(r)) if len(r) else 0.0, 4)
        s["still_share"] = round(float(max(0.0, 1 - (b - a) / max(1.0, (t1 - t0) * fps))), 2)   # share of the shot with no change at all
        # face
        m = (ft >= f0) & (ft < f1)
        fsel = faces[m]
        if len(fsel):
            has = fsel[:, 5] > 0
            s["face_share"] = round(float(has.mean()), 2)
            if has.any():
                f = fsel[has]
                s["face"] = {"h": round(float(np.median(f[:, 4])), 3), "cx": round(float(np.median(f[:, 1] + f[:, 3] / 2)), 3),
                             "cy": round(float(np.median(f[:, 2] + f[:, 4] / 2)), 3), "count": int(np.median(f[:, 6]))}
                if len(f) >= 6:   # independent check of zoom: face height at the end of the shot / at the start
                    q3 = max(1, len(f) // 3)
                    s["face"]["h_end_over_start"] = round(float(np.median(f[-q3:, 4]) / max(1e-6, np.median(f[:q3, 4]))), 3)
                    # a slow drift measured from tracked corners is only believed when the face grows or shrinks with it
                    if s.get("move", "").startswith("slow"):
                        fz = s["face"]["h_end_over_start"] - 1; cz = s["camera"]["zoom_total"] - 1
                        if fz * cz <= 0 or abs(fz) < 0.4 * abs(cz):
                            s["move"] = "static"; s["camera"]["drift_unconfirmed"] = True
        shots.append(s)
    n_frames_src = n_src

    # ---- one representative frame per shot: flatness, palette
    cap = cv2.VideoCapture(video)
    for s in shots:
        mid = (s["f0"] + s["f1"]) // 2
        cap.set(cv2.CAP_PROP_POS_FRAMES, mid)
        ok, fr = cap.read()
        if not ok: continue
        fr = cv2.resize(fr, (W, H), interpolation=cv2.INTER_AREA)
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(np.float32)
        var = cv2.blur(g * g, (5, 5)) - cv2.blur(g, (5, 5)) ** 2
        s["flat_share"] = round(float((var < 4).mean()), 2)
        q = (fr >> 5).reshape(-1, 3).astype(np.int32)
        key = q[:, 0] * 64 + q[:, 1] * 8 + q[:, 2]
        cnt = np.bincount(key, minlength=512)
        top = np.argsort(-cnt)[:4]
        pal = []
        for t in top:
            if cnt[t] / len(key) < 0.04: break
            sel = fr.reshape(-1, 3)[key == t].mean(0)
            pal.append({"hex": "#%02x%02x%02x" % (int(sel[2]), int(sel[1]), int(sel[0])), "share": round(float(cnt[t] / len(key)), 2)})
        s["palette"] = pal
        hsv = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV)
        s["sat"] = round(float(hsv[:, :, 1].mean() / 255), 2); s["luma"] = round(float(g.mean() / 255), 2)
        # measured picture class - a hint, not a label: a face detector cannot tell the speaker from a face in b-roll
        face = s.get("face", {}).get("h", 0) if s.get("face_share", 0) >= 0.5 else 0
        flat = s["flat_share"] >= 0.55
        if face >= 0.12 and not flat: s["picture"] = "speaker"                      # a large face on filmed footage
        elif face > 0 and flat: s["picture"] = "page with a face on it"            # a card, inset or photo on a flat canvas
        elif flat: s["picture"] = "flat graphic"
        elif face > 0: s["picture"] = "small face (inset / wide shot)"
        else: s["picture"] = "no face (b-roll / screen / graphic)"
    cap.release()

    jdump({"video": os.path.basename(video), "fps": src_fps, "content_fps": round(fps, 2), "duplicate_frame_share": round(1 - n / n_src, 3),
           "frames": n_src, "duration": round(dur_total, 3),
           "cuts": [cuts[c] for c in cut_idx], "shots": shots}, os.path.join(out_dir, "shots.json"))
    kinds = {}
    for c in cuts.values(): kinds[c["kind"]] = kinds.get(c["kind"], 0) + 1
    print(f"{n_src} frames ({n} distinct, content {fps:.1f} fps), {len(shots)} shots, cuts {kinds}")


if __name__ == "__main__":
    video, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    if "--pass2" not in sys.argv:
        pass1(video, out)
    pass2(video, out)
