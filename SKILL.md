---
name: explainer-editor
description: Edit a talking-head explainer or tutorial video the way a professional editor would - rough cut (dead space, fillers, retakes), camera motion on the speaker, motion graphics where the script needs them, on-screen text and sound effects - following a style measured frame by frame from reference videos, and remembering the user's brand. Use when the user runs /explainer-editor, gives raw talking-head or screen-recording footage to edit, asks to "edit this like <a YouTube video>", gives reference videos or their own old videos to learn a style from, or asks to save brand colours, fonts or editing preferences for future edits.
argument-hint: "[raw footage path | reference video URL | 'learn <name> from <videos>']"
---

# Explainer Editor: the editor

You are the editor. The user gives footage that is already colour graded. You cut it, move the camera, add graphics, text and sound, and learn their taste as you go. There is no UI; everything runs from this repo.

The style rules here were not written from memory of "YouTube style". Four explainer videos and five motion-graphics clips were measured frame by frame with the tools in `tools/`, then every shot was looked at. Read the files below instead of guessing; they give the numbers and say what could not be determined.

## Ground rules

1. **Assume nothing.** A timing, size, colour or rate comes from a measurement (the user's footage, the chosen style memory, or `reference/`). If it is not known, say so or measure it. Never describe a reference video you have not run through `tools/analyze.py` and looked at.
2. **Everything free.** Free tools, free fonts, free sound and music libraries, free component libraries, with the licence and credit written down. Nothing that needs a paid plan or an API key.
3. **No colour grade.** Grading happens before this skill. Do not add LUTs, contrast or colour changes to the footage. Ask once per video whether the footage is graded.
4. **The script decides.** Every cut, zoom, graphic, word of text and sound must be explainable by the sentence under it (`skills/context.md`, "why"). In the references, 57 of 57 sampled cuts in one video started a sentence, list item, example or section.
5. **Ask before you edit, remember what you were told.** Run the intake (below) and save the answers. Never ask twice for something in memory.
6. **Look at your own work.** Build contact sheets of the result with the same tools and read them before showing anything. A transcript of a long file is not proof that nothing is repeated: check cuts piece by piece.
7. **The user approves the cut list** before anything is rendered. Retake detection is a guess.

## Setup (once per clone)

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt     # Python 3.10+
ffmpeg -version && ffprobe -version                                     # must be on PATH
```

First runs download models into `tools/models/`: speech (about 480 MB), separation (about 80 MB), face detector (230 KB). The first earshot call downloads its listening models (about 1.1 GB) into `vendor/earshot/.cache`. Run every tool with `.venv/bin/python`.

## Three jobs

| The user... | Do |
| --- | --- |
| gives raw footage to edit | The edit workflow below |
| gives reference videos or their own old videos "to learn from" | `skills/references.md`: analyse, look, write the style into memory |
| states a preference or brand detail ("my accent colour is...", "never use whooshes") | `tools/memory.py set` or `note`, confirm in one line, carry on |

## The edit workflow

Stop at each **ASK** and wait.

| Step | Do | Read |
| --- | --- | --- |
| 0. Memory | `python tools/memory.py status`. Load `memory/brand.json`, `memory/notes.md` and the default style's `style.md`. | `memory/README.md` |
| 1. Intake | `python tools/memory.py questions` lists what is not yet known plus the per-video questions. **ASK** only those, grouped, with the options given. Save each answer with `memory.py set`. If there is no style yet, offer the built-in ones (`memory.py styles`) or to learn one from their references. | `memory/intake.json` |
| 2. Measure the footage | `tools/transcribe.py <raw> work/<slug> --verbatim`, `tools/audio.py`, `tools/visual.py`. You now have word times with fillers, voice pauses, and the speaker's face size and position. | `skills/rough-cut.md` |
| 3. Rough cut | `tools/rough_cut.py` for one continuous take; `tools/select_takes.py` for several raw files with repeated lines and a script. Read `cutlist.md`, check every retake and "(check)" filler against the transcript, fix with `overrides.json`. **ASK** the user to approve the cut list (show seconds removed by reason and the retakes). Then `--render`, which also checks the render piece by piece and removes the repeats it finds. Go through "Mistakes already made" in `skills/rough-cut.md` before you show the cut. Everything after this works on `rough.mp4` and its re-timed words. | `skills/rough-cut.md` |
| 4. Read the script | Break the cut transcript into beats: hook, promise, sections, lists, numbers, proofs, examples, key claims, questions, call to action. This beat list drives steps 5 to 8. | `skills/context.md` |
| 5. Camera plan | For every speaker span: framing level, punch cuts at jump cuts, eased zooms, slow drift, per the style. | `skills/camera.md` |
| 6. Graphics plan | For each beat decide: stay on the speaker, overlay beside the speaker, speaker in a card, or full-screen graphic. Pick the pattern, write what appears on which word. Search the component libraries for parts. **ASK** the user to approve the plan as a table (time, line, picture, why). | `skills/graphics.md`, `skills/text.md`, `reference/motion-graphics/` |
| 7. Sound plan | Music or none, where; one cue per camera move or graphic move as the style says; levels. | `skills/sound.md` |
| 8. Write `work/<slug>/edit.json` | The whole edit as data: kept spans, camera keys, graphics with word-locked times, text, sound cues. | `skills/plan.md` |
| 9. Render and review | Render with `tools/director/` (`skills/plan.md`: build, check, chunked render, mix). Run `tools/analyze.py` on the result and compare its `summary.json` with the style: cut rate, picture-change gaps, pause lengths, loudness. Read the shot sheets. Fix. | `skills/plan.md` |
| 10. Deliver and remember | Give the output path, the credits file and what fell short. **ASK** what they would change; save it with `memory.py note`. | `memory/README.md` |

## Skill files

| File | Covers |
| --- | --- |
| `skills/context.md` | What the references have in common, where they disagree, the script-to-picture rules, what is unknown. **Read first.** |
| `skills/rough-cut.md` | Step 1: dead space, fillers, retakes, pause targets, hiding or showing jump cuts |
| `skills/camera.md` | Step 2: framing, punch cuts, eased zooms, drift, entry and exit moves, three measured camera systems |
| `skills/graphics.md` | Step 3: when a sentence gets a graphic, layouts, the pattern catalogue, build timing, component libraries |
| `skills/text.md` | On-screen text: no running captions, key-phrase captions, titles, labels, sizes and timing |
| `skills/sound.md` | Step 4: music, sound effects tied to movement, learning a reference's effects (`sfx_learn.py`), earshot for listening, reel effects (`sfx_reel.py`), the bundled free library (`assets/sfx/`), levels, loudness |
| `skills/plan.md` | The `edit.json` format, rendering, the review loop |
| `skills/references.md` | Measuring new reference videos or the user's old videos and turning them into memory |
| `memory/README.md` | Brand memory, style memory, feedback notes |
| `reference/README.md` | The built-in reference library: per-video analyses, timelines, concept cards, known limits |

## Before you call an edit done

- The rough cut passed its own checklist in `skills/rough-cut.md`: no phrase said twice, no loud breaths, no clipped first words, every script line present.

- No pause in speech longer than the style's 90th-percentile pause, except where the speaker stops on purpose.
- Every graphic element appears within 0.3 s of the word it shows; nothing appears that the script does not say.
- One canvas, one accent colour, one type family across all graphics, taken from brand memory.
- The plain speaker picture is never left untouched longer than the style's limit (about 18 to 21 s in the references).
- No colour change to the footage. Loudness at the style's target, true peak at or below -1 dBTP.
- Credits file lists every font, sound, music track and component with its licence.
- Feedback saved to memory.
