# Learning from reference videos

Use this when the user gives reference videos, a channel they want to match, or their own old videos. The output is a style in `memory/styles/<name>/` that every later edit follows, or a concept card for a motion-graphics clip.

Two kinds of reference, two outputs:

| Reference | Has a speaker and a script | Output |
| --- | --- | --- |
| Explainer, tutorial, the user's own old video | yes | `reference/analysis/<slug>/analysis.md` + a style in memory |
| Motion-graphics reel, agency showcase, product explainer | no speaker, or the speaker is not the point | `reference/motion-graphics/<slug>/concept.md` |

Do not analyse every clip the user sends if they say "a few": pick some, say which, and do those properly.

## 1. Measure

```bash
python tools/analyze.py <url-or-file> --slug <slug>          # explainer
python tools/analyze.py <file> --slug <slug> --out reference/motion-graphics --skip sheets   # then even sheets, below
```

`analyze.py` runs, in order:

| Tool | Measures | Writes |
| --- | --- | --- |
| `fetch.py` | downloads a URL with yt-dlp; title, chapters, most-replayed curve | `reference/source/<slug>.mp4`, `.info.json` |
| `visual.py` | every frame: change from the last frame, colour histogram, global zoom and pan from tracked corners, what changed besides the camera, the largest face four times a second. From those: cuts by kind, shots, camera moves, motion events, flatness, palette | `frames.npz`, `shots.json` |
| `transcribe.py` | word-timed transcript (faster-whisper) | `words.json`, `transcript.txt` |
| `ocr.py` | every on-screen text, read at each picture change and once a second, linked into tracks with size, position and colour | `text.json` |
| `audio.py` | loudness; voice and bed stems (Demucs); voice pauses; music level; sound events in the bed | `audio.json` |
| `shot_sheets.py` | contact sheets, a few labelled frames per shot | `shots/*.jpg` |
| `timeline.py` | joins everything per shot; counts the style numbers | `timeline.md`, `timeline.json`, `summary.json` |

For a clip with no cuts to speak of (a reel, a UI animation) use even sampling instead of shot sheets:

```bash
python tools/make_sheets.py <file> <out>/sheets --fps 10 --cols 5 --rows 5 --tile-w 300   # short clips
python tools/ocr.py <file> <out> --fps 5 --even
```

If the video has a second audio track in a language you can read, fetch it with `--also-lang en` and transcribe it to `words.en.json`: the timeline shows those words, while pause and cut timing still come from the original speech.

## 2. Look

Numbers say what happened and when. Only frames say what a graphic is and what it is for.

1. Read `timeline.md` from top to bottom beside every sheet in `shots/`.
2. For exact timing build dense sheets and read them: `python tools/make_sheets.py <video> <out>/dense --fps 30 --start A --end B --cols 8 --rows 5 --tile-w 240 --prefix tA`. Do at least: three transitions, three camera moves, two text builds, two strong sound events.
3. Check the numbers against the frames and write down every disagreement. Known weak spots are listed in `reference/README.md`.

## 3. Write the analysis

`reference/analysis/<slug>/analysis.md`, sections as in the four built-in ones: facts, script structure, the rough cut, camera on the speaker, layouts, motion-graphics catalogue, script-to-picture table (40 or more rows), why each cut is there (50 or more sampled cuts with counts), on-screen text, transitions, sound, rules to reproduce (20 to 30, each with its number), what could not be determined. Also `graphics.json`: every graphic instance with its time, type, layout, the line said, its job, how it enters and leaves.

Rules:
- Every statement is a measurement or something seen on a named frame. Give the time.
- Label what is inferred. List what cannot be known.
- Do not name fonts, software or sounds unless the name is legible on screen.

For a motion-graphics clip write `concept.md` instead, sections as in `reference/motion-graphics/*/concept.md`: concept in one paragraph, look, scene list, motion vocabulary with frame counts, pacing, patterns to reuse in a talking-head explainer, what could not be determined.

## 4. Save the style

```bash
python tools/learn_style.py <name> reference/analysis/<slug> [more analysis folders] --desc "one line"
python tools/memory.py use <name>
```

This writes the numbers. Then fill in "Look and use of graphics" in `memory/styles/<name>/style.md` from your analysis: the graphic system (canvas, accent, type, cards), which camera system (`skills/camera.md` A, B, C or a mix), the transition into and out of graphics, text habits, the sound setting, recurring pieces. Running `learn_style.py` again keeps that section.

Several videos in one style: the table shows the median and each video's value. Where they disagree widely, say in the look section which video wins for that choice. Videos that are different kinds of edit (a talking head and a screen tutorial) belong in separate styles.

## 5. The user's own old videos

Same steps. In addition:
- Take brand colours from the measured palettes and text colours (`shots.json` `palette`, `text.json` `text_colour`), show them to the user as hex values and save the confirmed ones with `python tools/memory.py set brand.colors '{...}'`.
- Save their framing (`face_height_share`, `face_centre`) so new footage is scaled to match.
- Ask what they would change about those old videos and save the answer with `memory.py note`. The style is what they did; the notes are what they want.

## Do not

- Keep or publish other people's videos. `reference/source/` is git-ignored. Analyses, numbers and small contact sheets are kept; say where they came from.
- Present a reference as a rule. One video is one editor's choices. The built-in guides state how many of the four references do each thing.
