#!/usr/bin/env python3
"""Join picture, words, on-screen text and sound into one timeline and count everything.

    python tools/timeline.py <out_dir> [--info reference/source/<slug>.info.json]

Reads shots.json, words.json, text.json, audio.json from <out_dir>. Writes:
  timeline.json  one row per shot: what is said, what is on screen, how the camera
                 moves, which text appears and whether it repeats the spoken words,
                 which sound events land on the cut or on a motion event
  timeline.md    the same as a readable table - read this beside the shot sheets
  summary.json   the measured style numbers (cut rate, shot lengths, camera moves,
                 text habits, pause lengths, sound-effect sync). learn_style.py
                 averages these across videos into a style memory.
Nothing here is a judgement: every figure is a count or a median of measurements.
"""
import argparse, os, re
import numpy as np
from common import jload, jdump

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--info", default=None)
a = ap.parse_args()
J = lambda n: jload(os.path.join(a.out, n))
sh, wj, tj, aj = J("shots.json"), J("words.json") or {"words": []}, J("text.json") or {"tracks": [], "density": [], "sample_fps": 4}, J("audio.json") or {}
info = jload(a.info) if a.info else None
shots, cuts, fps, dur = sh["shots"], sh["cuts"], sh["fps"], sh["duration"]
words = wj["words"]                      # timing of the ORIGINAL speech
wtext = (J("words.en.json") or wj)["words"]  # words used for reading/matching (a dub or translation, if present)
ts_ = np.array([w["start"] for w in wtext] or [0.0])
pz = aj.get("pauses", [])
pz_s = np.array([p["t"] for p in pz] or [-9.0]); pz_e = np.array([p["t"] + p["dur"] for p in pz] or [-9.0])
def in_pause(t, tol=0.04):
    k = np.searchsorted(pz_s, t + tol) - 1
    return bool(k >= 0 and pz_e[k] >= t - tol)
ws = np.array([w["start"] for w in words] or [0.0]); we = np.array([w["end"] for w in words] or [0.0])
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).split()
med = lambda x, nd=2: round(float(np.median(x)), nd) if len(x) else None
pct = lambda x, q, nd=2: round(float(np.percentile(x, q)), nd) if len(x) else None

# ---------- cut vs speech
for c in cuts:
    t = c["t"]
    i = int(np.searchsorted(ws, t))            # first word starting at/after t
    prev_end = we[i - 1] if i > 0 else 0.0
    nxt = ws[i] if i < len(ws) else dur
    inside = i > 0 and we[i - 1] > t + 0.04    # a word is still sounding across the cut
    c["in_word"] = bool(inside)
    c["in_pause"] = in_pause(c["t"])
    c["gap_before"] = round(float(t - prev_end), 2); c["gap_after"] = round(float(nxt - t), 2)
    c["after_sentence_end"] = bool(0 < i <= len(words) and words[i - 1]["w"][-1:] in ".?!" and not inside)

# ---------- text tracks: snap start to a frame-accurate picture event, match to speech
events = []  # (t, box or None)
for c in cuts: events.append((c.get("start", c["t"]), None))
for s in shots:
    for e in s.get("motion_events", []): events.append((e["start"], e["box"]))
events.sort(key=lambda x: x[0])
ev_t = np.array([e[0] for e in events] or [0.0])
step = 0.25
_d = tj.get("density", []) or [[0, 0]]
if not isinstance(_d[0], list): _d = [[k / tj.get("sample_fps", 4), v] for k, v in enumerate(_d)]
dens_t = np.array([x[0] for x in _d]); dens = np.array([x[1] for x in _d])
tracks = []
for tr in tj["tracks"]:
    tr["h"] = round(tr["box"][3] - tr["box"][1], 3)
    if tr["dur"] < 0.3 or tr["conf"] < 0.7: continue
    t0 = tr["t0"]
    lo, hi = np.searchsorted(ev_t, t0 - step - 0.08), np.searchsorted(ev_t, t0 + 0.04)
    cand = [events[k] for k in range(lo, hi)]
    b = tr["box"]
    hit = [e for e in cand if e[1] is None or not (e[1][2] < b[0] or e[1][0] > b[2] or e[1][3] < b[1] or e[1][1] > b[3])]
    tr["t0_exact"] = round(hit[-1][0], 3) if hit else None
    start = tr["t0_exact"] if tr["t0_exact"] is not None else t0 - step / 2
    tw = norm(tr["text"])
    if tw and len(wtext):
        i0, i1 = np.searchsorted(ts_, start - 4), np.searchsorted(ts_, tr["t1"] + 2)
        near = [(norm(wtext[k]["w"]), wtext[k]["start"]) for k in range(i0, i1)]
        said = {}
        for nw, t in near:
            for x in nw: said.setdefault(x, []).append(t)
        m = [x for x in tw if x in said and len(x) > 1]
        tr["spoken_share"] = round(len(m) / len(tw), 2)
        if m and len(m) / len(tw) >= 0.6:
            first = min(said[m[0]], key=lambda t: abs(t - start))
            tr["appears_vs_word_s"] = round(start - first, 2)   # negative = text arrives before the word is said
    tr["words"] = len(tw)
    k = int(np.searchsorted(dens_t, t0))
    tr["lines_on_screen"] = int(dens[min(k, len(dens) - 1)]) if len(dens) else 0
    tracks.append(tr)
# text that belongs to the filmed scene (a logo on a microphone, a poster) keeps coming back in the same place
seen = {}
for t in tracks:
    k = ("".join(norm(t["text"])), round((t["box"][0] + t["box"][2]) / 2, 1), round((t["box"][1] + t["box"][3]) / 2, 1))
    seen.setdefault(k, []).append(t)
for k, v in seen.items():
    if len(v) >= 4 and sum(t["dur"] for t in v) > 20:
        for t in v: t["scenery"] = True
tracks = [t for t in tracks if not t.get("scenery")]
big = [t for t in tracks if t["h"] >= 0.035 and t["lines_on_screen"] < 14 and t["dur"] >= 0.5 and t["conf"] >= 0.8]

# ---------- sfx vs picture
sfx = aj.get("sfx_candidates", [])
strong = [e for e in sfx if e.get("strong", True)]
cut_t = np.array([c.get("start", c["t"]) for c in cuts] or [-9.0])
mot_t = np.array(sorted(e["start"] for s in shots for e in s.get("motion_events", [])) or [-9.0])
def nearest(arr, t):
    k = np.searchsorted(arr, t); best = 9.0
    for q in (k - 1, k):
        if 0 <= q < len(arr) and abs(arr[q] - t) < abs(best): best = float(arr[q] - t)
    return best
for e in sfx:
    dc, dm = nearest(cut_t, e["t"]), nearest(mot_t, e["t"])
    e["cut_offset_s"] = round(dc, 2) if abs(dc) <= 0.5 else None
    e["motion_offset_s"] = round(dm, 2) if abs(dm) <= 0.5 else None
    e["on_picture_event"] = bool(abs(dc) <= 0.12 or abs(dm) <= 0.12)
sfx_t = np.array([e["t"] for e in strong] or [-9.0])
for c in cuts:
    c["sfx_within_0.12s"] = bool(abs(nearest(sfx_t, c.get("start", c["t"]))) <= 0.12)
# chance level: same test with the sound events shifted by fixed offsets
def hit_rate(shift, ev=None):
    ev = sfx if ev is None else ev
    if not ev: return None
    return float(np.mean([abs(nearest(cut_t, e["t"] + shift)) <= 0.12 or abs(nearest(mot_t, e["t"] + shift)) <= 0.12 for e in ev]))
chance = float(np.mean([hit_rate(s) for s in (0.7, 1.3, 1.9, 2.6, -0.7, -1.3, -1.9, -2.6)])) if sfx else None

# ---------- rows
rows = []
for s in shots:
    i0, i1 = np.searchsorted(ts_, s["start"] - 0.05), np.searchsorted(ts_, s["end"] - 0.05)
    said = " ".join(w["w"] for w in wtext[i0:i1])
    txt = [t for t in tracks if s["start"] - 0.02 <= t["t0"] < s["end"] - 0.02 and t["dur"] >= 0.45]
    txt_big = sorted([t for t in txt if t["h"] >= 0.03], key=lambda t: -t["h"])[:6]
    sx = [e for e in sfx if s["start"] - 0.12 <= e["t"] < s["end"] - 0.12]
    c = next((c for c in cuts if c["frame"] == s["f0"]), None)
    r = {k: s[k] for k in ("i", "start", "end", "dur", "cut_in", "move", "picture") if k in s}
    for k in ("cut_in_scale", "camera", "zoom_moves", "face", "face_share", "flat_share", "palette", "activity"):
        if k in s: r[k] = s[k]
    if c:
        r["cut"] = {k: c[k] for k in ("in_word", "in_pause", "gap_before", "gap_after", "after_sentence_end", "sfx_within_0.12s", "start", "end") if k in c}
    r["said"] = said; r["words"] = int(i1 - i0)
    r["text_lines_new"] = len(txt)
    r["text"] = [{k: t.get(k) for k in ("text", "t0", "t0_exact", "dur", "h", "box", "text_colour", "bg_colour", "grew", "spoken_share", "appears_vs_word_s")} for t in txt_big]
    r["motion_events"] = len(s.get("motion_events", []))
    r["sfx"] = [{k: e.get(k) for k in ("t", "dur", "kinds", "rel_voice_dB", "strong", "on_picture_event", "cut_offset_s", "motion_offset_s")} for e in sx if e.get("strong", True)]
    r["sfx_weak"] = sum(not e.get("strong", True) for e in sx)
    rows.append(r)
jdump({"video": sh["video"], "fps": fps, "duration": dur, "rows": rows}, os.path.join(a.out, "timeline.json"))

# ---------- markdown
def mmss(t): return f"{int(t // 60)}:{t % 60:05.2f}"
L = [f"# Timeline: {sh['video']}", "",
     "One row per shot. `cut` = how the shot starts (hard = new picture, punch = same picture instant zoom with its scale, jump = same picture instant shift, pop = a graphic appears instantly in part of the frame, transition = multi-frame).",
     "`move` = camera movement measured inside the shot. `T:` on-screen text that first appears in this shot (height as % of frame; `=said` when it repeats spoken words, with seconds text leads(-)/lags(+) the word). `S:` sound-event candidates (★ = lands within 0.12 s of a cut or motion event).", ""]
chap = (info or {}).get("chapters") or []
ci = 0
for r in rows:
    while ci < len(chap) and chap[ci]["start_time"] <= r["start"] + 0.5:
        L += ["", f"## {mmss(chap[ci]['start_time'])} {chap[ci]['title']}", ""]; ci += 1
    cut = r["cut_in"] + (f" x{r['cut_in_scale']}" if "cut_in_scale" in r else "")
    cam = r.get("camera", {})
    mv = r.get("move", "")
    if cam and "static" not in mv: mv += f" x{cam['zoom_total']:.3f}"
    face = f" {int(r['face']['h'] * 100)}%@{r['face']['cx']:.2f},{r['face']['cy']:.2f}" if "face" in r and r.get("face_share", 0) >= 0.5 else ""
    line = f"- **#{r['i']}** {mmss(r['start'])} +{r['dur']:.2f}s | {cut} | {r.get('picture', '?')}{face} | {mv}"
    if r["motion_events"]: line += f" | {r['motion_events']} motion ev"
    L.append(line)
    if r["said"]: L.append(f"  - “{r['said']}”")
    for t in r["text"]:
        ex = ""
        if t.get("spoken_share") is not None and t["spoken_share"] >= 0.6:
            ex = " =said" + (f" {t['appears_vs_word_s']:+.2f}s" if t.get("appears_vs_word_s") is not None else "")
        L.append(f"  - T: “{t['text']}” {t['h'] * 100:.1f}% @{(t['box'][0] + t['box'][2]) / 2:.2f},{(t['box'][1] + t['box'][3]) / 2:.2f} {t['dur']}s {t.get('text_colour')}{' built' if t.get('grew') else ''}{ex}")
    if r["text_lines_new"] > len(r["text"]): L.append(f"  - (+{r['text_lines_new'] - len(r['text'])} more/smaller text lines)")
    if r["sfx"]:
        L.append("  - S: " + ", ".join(f"{'★' if e['on_picture_event'] else ''}{'+'.join(e['kinds'])}@{e['t']:.2f}({e['rel_voice_dB']:+.0f}dB)" for e in r["sfx"]))
open(os.path.join(a.out, "timeline.md"), "w").write("\n".join(L) + "\n")

# ---------- summary
mins = dur / 60
kinds = {}
for c in cuts: kinds[c["kind"]] = kinds.get(c["kind"], 0) + 1
sd = np.array([s["dur"] for s in shots])
pic = {}
for s in shots: pic[s.get("picture", "?")] = pic.get(s.get("picture", "?"), 0) + s["dur"]
face_sh = [s for s in shots if s.get("picture") == "speaker"]
moves = {}
for s in face_sh:
    m = s.get("move", "?").split(" x")[0]; moves[m] = moves.get(m, 0) + s["dur"]
ftot = sum(moves.values()) or 1
punch = [c["scale"] for c in cuts if c["kind"] == "punch"]
zm = [z for s in shots for z in s.get("zoom_moves", [])]
slow = [abs(s["camera"]["zoom_pct_per_s"]) for s in face_sh if s.get("move", "").startswith("slow") and s["dur"] >= 1]
# picture changes = hard cuts + transitions; visual change of any kind = all cuts
pc = sorted(c["t"] for c in cuts if c["kind"] in ("hard", "transition"))
gaps_pc = np.diff([0] + pc + [dur])
allc = np.diff([0] + [c["t"] for c in cuts] + [dur])
# face scale steps between consecutive face shots
steps = []
for x, y in zip(shots, shots[1:]):
    if x.get("picture") == "speaker" and y.get("picture") == "speaker" and x["face"]["h"] > 0:
        steps.append(y["face"]["h"] / x["face"]["h"])
steps = np.array(steps)
tr_c = [c for c in cuts if c["kind"] == "transition"]
speechcuts = [c for c in cuts if c["kind"] in ("jump", "punch")]
summary = {
    "video": sh["video"], "duration_s": dur, "fps": fps,
    "title": (info or {}).get("title"), "channel": (info or {}).get("channel"), "views": (info or {}).get("view_count"),
    "cuts": {"total": len(cuts), "per_min": round(len(cuts) / mins, 1), "by_kind": kinds,
             "by_kind_per_min": {k: round(v / mins, 1) for k, v in kinds.items()},
             "shot_len_s": {"median": med(sd), "p10": pct(sd, 10), "p90": pct(sd, 90), "max": round(float(sd.max()), 1)},
             "picture_change_every_s": {"median": med(gaps_pc), "p90": pct(gaps_pc, 90), "max": round(float(gaps_pc.max()), 1)},
             "any_cut_every_s": {"median": med(allc), "p90": pct(allc, 90), "max": round(float(allc.max()), 1)},
             "transition_len_s": {"median": med([c["end"] - c["start"] for c in tr_c]), "p90": pct([c["end"] - c["start"] for c in tr_c], 90)} if tr_c else None},
    "cut_vs_speech": {
        "same_picture_cuts_between_words_share": round(float(np.mean([not c["in_word"] for c in speechcuts])), 2) if speechcuts else None,
        "same_picture_cuts_after_sentence_end_share": round(float(np.mean([c["after_sentence_end"] for c in speechcuts])), 2) if speechcuts else None,
        "picture_changes_between_words_share": round(float(np.mean([not c["in_word"] for c in cuts if c["kind"] in ("hard", "transition")])), 2) if pc else None,
        "picture_changes_after_sentence_end_share": round(float(np.mean([c["after_sentence_end"] for c in cuts if c["kind"] in ("hard", "transition")])), 2) if pc else None,
        "same_picture_cuts_inside_voice_pause_share": round(float(np.mean([c["in_pause"] for c in speechcuts])), 2) if speechcuts else None,
        "picture_changes_inside_voice_pause_share": round(float(np.mean([c["in_pause"] for c in cuts if c["kind"] in ("hard", "transition")])), 2) if pc else None,
        "chance_inside_voice_pause_share": round(float(np.mean([in_pause(t) for t in np.arange(0.5, dur, 0.37)])), 2),
        "timing_words_from": "words.json" if words else "none (words.en.json is a dub: speech-timing shares use voice pauses only)"},
    "picture_share_of_runtime": {k: round(v / dur, 3) for k, v in sorted(pic.items(), key=lambda kv: -kv[1])},
    "camera_on_face_shots": {
        "share_of_face_time_by_move": {k: round(v / ftot, 2) for k, v in sorted(moves.items(), key=lambda kv: -kv[1])},
        "punch_cut_scale": {"n": len(punch), "in_median": med([p for p in punch if p > 1], 3), "out_median": med([p for p in punch if p < 1], 3),
                            "in_n": sum(p > 1 for p in punch), "out_n": sum(p < 1 for p in punch)},
        "face_height_share": {"median": med([s["face"]["h"] for s in face_sh], 3), "p10": pct([s["face"]["h"] for s in face_sh], 10, 3), "p90": pct([s["face"]["h"] for s in face_sh], 90, 3)},
        "face_centre": {"x_median": med([s["face"]["cx"] for s in face_sh]), "y_median": med([s["face"]["cy"] for s in face_sh])},
        "face_size_step_between_face_shots": {"changed_over_5pct_share": round(float(np.mean(np.abs(np.log(steps)) > 0.05)), 2) if len(steps) else None,
                                              "median_step_when_changed": med(np.exp(np.abs(np.log(steps[np.abs(np.log(steps)) > 0.05]))), 3) if len(steps) else None},
        "eased_zoom_moves": {"n": len(zm), "per_min": round(len(zm) / mins, 1), "factor_median": med([max(z["factor"], 1 / z["factor"]) for z in zm], 3),
                             "dur_median_s": med([z["end"] - z["start"] for z in zm]), "in_share": round(float(np.mean([z["factor"] > 1 for z in zm])), 2) if zm else None,
                             "peak_position_median": med([z["peak_at"] for z in zm])},
        "slow_push_pct_per_s_median": med(slow)},
    "text": {
        "big_tracks": len(big), "big_per_min": round(len(big) / mins, 1),
        "on_screen_s_median": med([t["dur"] for t in big]), "words_median": med([t["words"] for t in big], 0), "words_p90": pct([t["words"] for t in big], 90, 0),
        "height_share_median": med([t["h"] for t in big], 3), "height_share_p90": pct([t["h"] for t in big], 90, 3),
        "repeats_spoken_words_share": round(float(np.mean([t.get("spoken_share", 0) >= 0.6 for t in big])), 2) if big else None,
        "appears_vs_word_s": {"median": med([t["appears_vs_word_s"] for t in big if t.get("appears_vs_word_s") is not None]),
                              "p10": pct([t["appears_vs_word_s"] for t in big if t.get("appears_vs_word_s") is not None], 10),
                              "p90": pct([t["appears_vs_word_s"] for t in big if t.get("appears_vs_word_s") is not None], 90)},
        "built_on_share": round(float(np.mean([t["grew"] for t in big])), 2) if big else None,
        "position_grid_3x3_share": None, "text_colours_top": None,
        "dense_text_share_of_runtime": round(float(np.sum(np.diff(np.append(dens_t, dur))[dens >= 14]) / dur), 3) if len(dens) else None},
    "audio": {k: aj.get(k) for k in ("loudness", "voice", "pause_stats", "word_gaps")} | {"bed": (aj.get("bed") or {}).get("summary"), "silences_n": len(aj.get("silences", []))},
    "sfx": {"candidates": len(sfx), "per_min": round(len(sfx) / mins, 1), "strong": len(strong), "strong_per_min": round(len(strong) / mins, 1),
            "strong_on_picture_event_share": round(hit_rate(0, strong), 2) if strong else None,
            "strong_chance_share": round(float(np.mean([hit_rate(x, strong) for x in (0.7, 1.3, 1.9, 2.6, -0.7, -1.3, -1.9, -2.6)])), 2) if strong else None,
            "strong_rel_voice_dB_median": med([e["rel_voice_dB"] for e in strong], 1), "strong_dur_s_median": med([e["dur"] for e in strong]),
            "on_picture_event_share": round(float(np.mean([e["on_picture_event"] for e in sfx])), 2) if sfx else None,
            "chance_share": round(chance, 2) if chance is not None else None,
            "by_kind": {k: sum(k in e["kinds"] for e in sfx) for k in ("LOW", "BB")},
            "cuts_with_sfx_share": {k: round(float(np.mean([c["sfx_within_0.12s"] for c in cuts if c["kind"] == k])), 2) for k in kinds},
            "cuts_with_sfx_chance_share": round(float(np.mean([abs(nearest(sfx_t, t)) <= 0.12 for t in np.arange(0.5, dur, 0.37)])), 2),
            "offset_to_cut_s_median": med([e["cut_offset_s"] for e in sfx if e["cut_offset_s"] is not None and abs(e["cut_offset_s"]) <= 0.12])},
}
if big:
    grid = np.zeros((3, 3))
    for t in big:
        cx, cy = (t["box"][0] + t["box"][2]) / 2, (t["box"][1] + t["box"][3]) / 2
        grid[min(2, int(cy * 3)), min(2, int(cx * 3))] += 1
    summary["text"]["position_grid_3x3_share"] = (grid / grid.sum()).round(2).tolist()
    col = {}
    for t in big:
        if t.get("text_colour"):
            c = t["text_colour"]; q = "#" + "".join("%x" % (int(c[i:i + 2], 16) >> 4) for i in (1, 3, 5))  # 12-bit bucket
            col[q] = col.get(q, 0) + 1
    summary["text"]["text_colours_top"] = [{"rgb12": k, "share": round(v / len(big), 2)} for k, v in sorted(col.items(), key=lambda kv: -kv[1])[:6]]
if chap:
    per = []
    for k, c in enumerate(chap):
        a0, a1 = c["start_time"], c["end_time"]
        ss = [s for s in shots if a0 <= s["start"] < a1]
        if not ss: continue
        d = a1 - a0
        per.append({"title": c["title"], "start": a0, "dur": round(d, 1), "cuts_per_min": round(len(ss) / d * 60, 1),
                    "face_share": round(sum(s["dur"] for s in ss if s.get("picture") == "speaker") / d, 2),
                    "big_text_per_min": round(sum(a0 <= t["t0"] < a1 for t in big) / d * 60, 1),
                    "sfx_per_min": round(sum(a0 <= e["t"] < a1 for e in sfx) / d * 60, 1)})
    summary["chapters"] = per
jdump(summary, os.path.join(a.out, "summary.json"))
print(f"{len(rows)} rows | cuts/min {summary['cuts']['per_min']} {kinds} | big text/min {summary['text']['big_per_min']} | sfx/min {summary['sfx']['per_min']} on-picture {summary['sfx']['on_picture_event_share']} (chance {summary['sfx']['chance_share']})")
