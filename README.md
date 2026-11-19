# Explainer Editor

A Claude Code skill that edits talking-head explainer and tutorial videos the way an editor would, and learns your style.

It does four things to footage that is already colour graded:

1. **Rough cut**: removes dead space, filler words and retakes.
2. **Camera motion**: punch cuts, eased zooms and slow drift on the speaker.
3. **Motion graphics and text**: only where the script lists, explains, proves or marks a section.
4. **Sound**: music and effects tied to movement on screen.

Nothing in it is a guess about "YouTube style". Four explainer videos and five motion-graphics clips were measured frame by frame (cuts, zoom factors, face size, every on-screen text, pauses, music level, every sound event), then every shot was looked at and written up. The same tools run on any video you give it, so you can point it at references you like, or at your own old videos, and it will edit to match.

Everything is free and local: ffmpeg, OpenCV, faster-whisper, RapidOCR, Demucs, yt-dlp. No API keys.

## State of the project

| Part | State |
| --- | --- |
| Measuring tools (`tools/`) | working |
| Reference library: 4 video analyses, 5 concept cards (`reference/`) | done |
| Memory: brand answers, styles, feedback (`memory/`) | working |
| Rough cut with a review file | working; retake detection must be checked by a person |
| Guides for camera, graphics, text, sound (`skills/`) | written from the measurements |
| Renderer for camera moves, graphics and sound (`tools/director/`) | working: plan.js on HyperFrames, chunked render, sound mix (`skills/plan.md`) |

## Install

```bash
git clone <this repo> ~/.claude/skills/explainer-editor
cd ~/.claude/skills/explainer-editor
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Needs Python 3.10 or newer and ffmpeg. First runs download a speech model (about 480 MB) and a separation model (about 80 MB).

## Use

In Claude Code:

```
/explainer-editor ~/Videos/raw-take.mp4
/explainer-editor learn my-style from https://youtu.be/... and ~/Videos/old-video.mp4
```

The first time, it asks what an editor would ask (brand colours, fonts, format, how tight to cut, what kind of graphics, captions or not, music or not) and saves the answers. Later edits ask only what is new.

Or run the tools yourself:

```bash
# measure any video: cuts, camera moves, text, pauses, sound
.venv/bin/python tools/analyze.py https://youtu.be/XXXX --slug my-reference
open reference/analysis/my-reference/timeline.md

# turn measured videos into a style the edits follow
.venv/bin/python tools/learn_style.py my-style reference/analysis/my-reference
.venv/bin/python tools/memory.py use my-style

# rough cut of raw footage
.venv/bin/python tools/transcribe.py raw.mp4 work/ep1 --verbatim
.venv/bin/python tools/audio.py raw.mp4 work/ep1
.venv/bin/python tools/rough_cut.py raw.mp4 work/ep1          # read work/ep1/cut/cutlist.md
.venv/bin/python tools/rough_cut.py raw.mp4 work/ep1 --render
```

## What is in the box

```
SKILL.md              the editor's instructions and workflow
skills/               context, rough-cut, camera, graphics, text, sound, plan, references
assets/sfx/           593 free sound effects you may redistribute (Kenney CC0, earshot bank MIT) + catalogue.json
vendor/earshot/       earshot (MIT): lets the agent describe, rank and review sound it cannot hear
tools/                analyze.py and the tools under it; rough_cut.py; select_takes.py (multi-take, script-based rough cut); director/ (the renderer: plan.js -> HyperFrames page -> chunked render -> sound mix); memory.py; learn_style.py
memory/               intake questions; five built-in styles; your brand.json, notes.md and styles (git-ignored)
reference/analysis/   four explainer videos: analysis.md, timeline.md, summary.json, graphics.json, sheets
reference/motion-graphics/   five clips: concept.md each
```

Built-in styles: `kallaway-dark-studio`, `joseph-clean-canvas`, `ritesh-white-diagram`, `nafay-screen-tutorial`, and `reference-explainers` (the range across the three talking heads).

## A few things the measurements showed

- None of the four videos runs word-by-word captions. Text is used for chosen phrases: 2 words on median, about 5 % of frame height.
- Speech is cut until no pause is longer than about 0.35 s (median 0.14 to 0.23 s), except where the speaker stops on purpose.
- Graphics build one element per spoken noun, within about 0.3 s of the word.
- Where sound effects exist, they sit on camera moves and on moves inside graphics, not on plain cuts or on text.
- The three talking heads use three different camera systems, so camera motion is a style choice. `skills/camera.md` gives the numbers for each.

## Limits

The measurements have known weak spots (cut kinds inside animation and screen recordings, faces on cards counted as the speaker, text read while it animates, sounds measured but never heard). They are listed in `reference/README.md`, and each analysis ends with what could not be determined.

The reference videos belong to their creators and are not included. The analyses describe them; small contact sheets are kept as evidence. Remove `reference/analysis/*/shots/` and `reference/motion-graphics/*/sheets/` if you would rather not publish frames.

## Licence

Choose one before publishing (MIT is the usual choice for a skill). Third-party parts keep their own licences; see `requirements.txt` and `skills/graphics.md` for the component libraries.
