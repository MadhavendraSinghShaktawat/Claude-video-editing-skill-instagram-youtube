#!/usr/bin/env python3
"""Turn analysed videos into a style memory the editor follows.

    python tools/learn_style.py <name> <analysis_dir> [<analysis_dir> ...] [--desc "one line"]

Each <analysis_dir> is an output folder of tools/analyze.py (it must hold summary.json).
Use it for reference videos you admire, or for your own old videos so the next edit
matches them. Writes memory/styles/<name>/:
  style.json   the numbers the edit follows: each is the median across the videos,
               with the per-video values kept beside it so disagreement is visible
  style.md     the same numbers as an editing brief, with a section the editor
               fills in after LOOKING at the sheets (what graphics are used for)
  sources.json where the numbers came from
Run `python tools/memory.py use <name>` to make it the default.
"""
import argparse, json, os, sys, datetime
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
MEM = os.environ.get("EXPLAINER_EDITOR_HOME") or os.path.join(ROOT, "memory")
ap = argparse.ArgumentParser()
ap.add_argument("name"); ap.add_argument("dirs", nargs="+"); ap.add_argument("--desc", default="")
a = ap.parse_args()
S = [json.load(open(os.path.join(d, "summary.json"))) for d in a.dirs]


def dig(s, path):
    for k in path.split("."):
        if not isinstance(s, dict) or s.get(k) is None: return None
        s = s[k]
    return s


def stat(path, nd=2):
    v = [dig(s, path) for s in S]
    ok = [x for x in v if isinstance(x, (int, float))]
    return {"median": round(float(np.median(ok)), nd) if ok else None, "per_video": v}


FIELDS = {
 "cut": {
  "cuts_per_min": "cuts.per_min", "hard_per_min": "cuts.by_kind_per_min.hard", "jump_per_min": "cuts.by_kind_per_min.jump",
  "punch_per_min": "cuts.by_kind_per_min.punch", "pop_per_min": "cuts.by_kind_per_min.pop", "transition_per_min": "cuts.by_kind_per_min.transition",
  "shot_len_median_s": "cuts.shot_len_s.median", "shot_len_p90_s": "cuts.shot_len_s.p90",
  "picture_change_every_median_s": "cuts.picture_change_every_s.median", "picture_change_every_p90_s": "cuts.picture_change_every_s.p90",
  "longest_without_picture_change_s": "cuts.picture_change_every_s.max", "transition_len_median_s": "cuts.transition_len_s.median",
  "same_picture_cuts_inside_voice_pause": "cut_vs_speech.same_picture_cuts_inside_voice_pause_share",
  "picture_changes_inside_voice_pause": "cut_vs_speech.picture_changes_inside_voice_pause_share",
  "chance_inside_voice_pause": "cut_vs_speech.chance_inside_voice_pause_share",
  "picture_changes_after_sentence_end": "cut_vs_speech.picture_changes_after_sentence_end_share"},
 "speech": {
  "wpm": "audio.voice.wpm_overall", "wpm_while_speaking": "audio.voice.wpm_while_speaking", "voice_active_share": "audio.voice.active_share",
  "pauses_per_min": "audio.pause_stats.per_min", "pause_median_s": "audio.pause_stats.median_s", "pause_p90_s": "audio.pause_stats.p90_s",
  "pause_max_s": "audio.pause_stats.max_s", "speech_run_median_s": "audio.pause_stats.speech_run_s.median",
  "pauses_share_of_runtime": "audio.pause_stats.share_of_runtime"},
 "camera": {
  "face_height_share_median": "camera_on_face_shots.face_height_share.median", "face_centre_x": "camera_on_face_shots.face_centre.x_median",
  "face_centre_y": "camera_on_face_shots.face_centre.y_median", "punch_in_scale": "camera_on_face_shots.punch_cut_scale.in_median",
  "punch_out_scale": "camera_on_face_shots.punch_cut_scale.out_median",
  "face_size_changes_between_shots_share": "camera_on_face_shots.face_size_step_between_face_shots.changed_over_5pct_share",
  "face_size_step_median": "camera_on_face_shots.face_size_step_between_face_shots.median_step_when_changed",
  "eased_zooms_per_min": "camera_on_face_shots.eased_zoom_moves.per_min", "eased_zoom_factor": "camera_on_face_shots.eased_zoom_moves.factor_median",
  "eased_zoom_dur_s": "camera_on_face_shots.eased_zoom_moves.dur_median_s", "slow_push_pct_per_s": "camera_on_face_shots.slow_push_pct_per_s_median"},
 "text": {
  "big_text_per_min": "text.big_per_min", "on_screen_s": "text.on_screen_s_median", "words": "text.words_median", "words_p90": "text.words_p90",
  "height_share": "text.height_share_median", "repeats_spoken_words_share": "text.repeats_spoken_words_share",
  "appears_vs_word_s": "text.appears_vs_word_s.median", "built_on_share": "text.built_on_share"},
 "sound": {
  "integrated_LUFS": "audio.loudness.integrated_LUFS", "true_peak_dBTP": "audio.loudness.true_peak_dBTP", "LRA_LU": "audio.loudness.LRA_LU",
  "bed_rel_voice_dB": "audio.bed.median_rel_voice_dB", "bed_audible_share": "audio.bed.audible_bed_share", "bed_duck_dB": "audio.bed.duck_dB",
  "strong_sfx_per_min": "sfx.strong_per_min", "strong_sfx_on_picture_event_share": "sfx.strong_on_picture_event_share",
  "strong_sfx_chance_share": "sfx.strong_chance_share", "strong_sfx_rel_voice_dB": "sfx.strong_rel_voice_dB_median", "hard_cuts_with_sfx": "sfx.cuts_with_sfx_share.hard", "transitions_with_sfx": "sfx.cuts_with_sfx_share.transition",
  "pops_with_sfx": "sfx.cuts_with_sfx_share.pop", "any_moment_with_sfx_chance": "sfx.cuts_with_sfx_chance_share"},
}
style = {"name": a.name, "description": a.desc, "made": datetime.date.today().isoformat(),
         "sources": [{"dir": os.path.relpath(d, ROOT), "video": s.get("video"), "title": s.get("title"), "channel": s.get("channel"),
                      "duration_s": s.get("duration_s")} for d, s in zip(a.dirs, S)]}
for grp, fields in FIELDS.items():
    style[grp] = {k: stat(p) for k, p in fields.items()}
pics = sorted({k for s in S for k in s["picture_share_of_runtime"]})
style["picture_share_of_runtime"] = {k: stat("picture_share_of_runtime." + k, 3) for k in pics}
mv = sorted({k for s in S for k in s["camera_on_face_shots"]["share_of_face_time_by_move"]})
style["face_time_by_camera_move"] = {k: stat("camera_on_face_shots.share_of_face_time_by_move." + k) for k in mv}
style["text"]["position_grid_3x3_share"] = {"per_video": [dig(s, "text.position_grid_3x3_share") for s in S]}
style["text"]["colours"] = {"per_video": [dig(s, "text.text_colours_top") for s in S]}

out = os.path.join(MEM, "styles", a.name); os.makedirs(out, exist_ok=True)
json.dump(style, open(os.path.join(out, "style.json"), "w"), indent=1, ensure_ascii=False)
json.dump(style["sources"], open(os.path.join(out, "sources.json"), "w"), indent=1, ensure_ascii=False)

L = [f"# Style: {a.name}", "", a.desc, "", f"Learned {style['made']} from {len(S)} video(s):"]
L += [f"- {s['title'] or s['video']} ({s['channel'] or 'local file'}, {s['duration_s']:.0f} s) - `{s['dir']}`" for s in style["sources"]]
L += ["", "Numbers are medians across the videos; the values in brackets are each video, in the order above. Where the videos disagree, the bracket is the range to stay inside, and the look section below says which video to follow.", ""]
names = {"cut": "Cut", "speech": "Speech and pauses", "camera": "Camera on the speaker", "text": "On-screen text", "sound": "Sound"}
for grp in FIELDS:
    L += [f"## {names[grp]}", "", "| Measure | Median | Each video |", "| --- | --- | --- |"]
    for k, v in style[grp].items():
        if "median" in v: L.append(f"| {k} | {v['median']} | {v['per_video']} |")
    L.append("")
L += ["## Share of runtime by picture type", "", "| Picture | Median | Each video |", "| --- | --- | --- |"]
L += [f"| {k} | {v['median']} | {v['per_video']} |" for k, v in style["picture_share_of_runtime"].items()]
L += ["", "## Share of speaker time by camera move", "", "| Move | Median | Each video |", "| --- | --- | --- |"]
L += [f"| {k} | {v['median']} | {v['per_video']} |" for k, v in style["face_time_by_camera_move"].items()]
L += ["", "## Look and use of graphics (fill in after reading the sheets)", "",
      "The numbers above cannot say what a graphic is for. Read `timeline.md` beside `shots/*.jpg` for each source and write here:",
      "- what the graphics look like (canvas, palette, type, cards, icons, 2D or 3D)",
      "- what kind of sentence gets a graphic and what kind stays on the speaker",
      "- how graphics enter and leave, and what the speaker does meanwhile",
      "- caption habits", "- recurring pieces (intro, chapter cards, lower thirds, end screen)", ""]
p = os.path.join(out, "style.md")
if os.path.exists(p) and "## Look and use of graphics" in open(p).read():
    old = open(p).read(); tail = old[old.index("## Look and use of graphics"):]
    if "(fill in after reading the sheets)" not in tail:  # keep a look section that was already written
        L = L[:next(i for i, x in enumerate(L) if x.startswith("## Look and use of graphics"))] + [tail.rstrip(), ""]
open(p, "w").write("\n".join(L))
print("style saved ->", out)
