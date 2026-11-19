# Reference library

Nine videos, measured frame by frame and then looked at. Use these files instead of re-watching anything.

The source videos are other people's work and are not in the repo (`reference/source/` is git-ignored). To rebuild anything, fetch them again with `tools/fetch.py` under the slugs below.

## Explainer videos (`analysis/<slug>/`)

| Slug | Video | Size | Length | Shots | What it is a reference for |
| --- | --- | --- | --- | --- | --- |
| `joseph-learn-editing` | Joseph, "How I'd Learn Video Editing in 2026 (Before AI Replaces You)", youtu.be/QVNpbEy87tw | 1080p, 30 fps | 846 s | 296 | dense light-canvas graphics, blur transitions, music and effects throughout |
| `kallaway-dopamine-ladders` | Kallaway, "How to Become a Storytelling Genius (Dopamine Ladders)", youtu.be/jtmstMt4WLc | 1080p, 24 fps | 1345 s | 171 | locked camera with fixed zoom levels, one signature diagram, no music |
| `ritesh-ai-agency` | Ritesh Verma, "How To Start an AI Marketing Agency with Claude in 30 Days", youtu.be/aZ0TP-AGGkU | 1080p, 30 fps content in a 60 fps file | 972 s | 179 | speaker card beside white diagrams, numbered section cards, b-roll, screen demo |
| `nafay-faceless-shorts` | Nafay 3D, "I Found a way To Make Faceless YouTube Shorts for free", youtu.be/a6ZApl1ZEY0 | 1080p, 60 fps file, 89 % repeated frames | 673 s | 69 | a designed 22 s intro, then an untreated screen recording |

In each folder:

| File | Holds |
| --- | --- |
| `analysis.md` | The write-up: facts, script structure, rough cut, camera, layouts, motion-graphics catalogue, script-to-picture table, why each cut is there, text, transitions, sound, 30 rules to reproduce, what is not known |
| `graphics.json` | Every graphic instance found: time, type, layout, the line that triggered it, its job, how it enters and leaves (126, 71, 48 and 40 entries) |
| `timeline.md` / `timeline.json` | One row per shot: how it starts, picture class, face size, camera move, the words spoken, text that appears, sound events |
| `summary.json` | The counted style numbers; `tools/learn_style.py` turns these into a style memory |
| `shots.json` | Per shot: cut kind, camera move with zoom segments, motion events with boxes, face, flatness, palette |
| `text.json` | Every on-screen text track: text, on and off time, box, height, colours |
| `audio.json` | Loudness, voice pauses, music level per 30 s, every sound event |
| `words.json`, `transcript.txt` | Word-timed transcript (`words.en.json` for Nafay is YouTube's English dub; `words.json` is the Hindi original) |
| `shots/shots_NNN.jpg`, `shots_index.json` | Contact sheets: a few frames of every shot, each labelled `#shot time` |

To see second 62.7 of Kallaway: open `shots/shots_index.json`, find the sheet whose `t_start` to `t_end` holds 62.7, read that image; or find shot #12 in `timeline.md`.

## Motion-graphics clips (`motion-graphics/<slug>/`)

Five of the ten clips supplied were analysed; one concept card each.

| Slug | Clip | Length | Concept |
| --- | --- | --- | --- |
| `launch-video` | "Launch Videos That Turn Viewers Into Buyers" (before/after breakdown of a talking-head edit, three stacked panels) | 34.9 s | the talking head goes in and out of cards |
| `vaylens-explainer` | "Explainer - Vaylens" | 72 s | every phrase gets its own type gag |
| `airbank-explainer` | "Vidico x Airbank - Explainer Video" | 62 s | one black square becomes everything |
| `myna-ui` | "SaaS Motion Design For Myna" | 8.4 s | one screen, continuous pull-back |
| `clean-icons` | "Clean Icon Animation for SaaS Interface" | 9.5 s | icon row, light to dark |

Each folder has `concept.md` (concept, look, scene list, motion vocabulary with frame counts, pacing, patterns to reuse), `shots.json`, `text.json`, and `sheets/` with every sampled frame. Not analysed: GoFractional explainer, the collage animation, the minimal animation tutorial, the fiverr SaaS explainer, and the clip with the encoded file name.

## Known limits

Read these before quoting a number.

- **Cut kinds are algorithmic.** `hard` = the picture changed in one frame; `punch` = same picture, instant size change; `jump` = same picture, instant shift; `pop` = an instant change in part of the frame; `transition` = the picture 0.2 s before differs from the picture 0.2 s after with no instant cut. Inside animated graphics and screen recordings these fire on things that are not edits: in the screen tutorial only 17 of 68 detected cuts were edits, and three real edits were missed. In pure motion graphics most "cuts" are morphs.
- **Soft cuts.** In Joseph the four "hard" cuts checked frame by frame all had 2 to 4 frames of blur on each side.
- **Picture class** uses a face detector, which cannot tell the speaker from a face in b-roll, on a card or in a screenshot. Speaker time in the analyses was corrected by eye.
- **Zoom numbers** come from tracked corners. They are good on speaker shots (Kallaway's eased zooms read x1.085 against x1.087 to x1.095 measured directly) and unreliable on full-screen animation. A slow drift is reported only when the face grows or shrinks with it.
- **On-screen text** was read at every picture change and once a second, so times are within about 0.3 s unless a dense sheet was checked. Text is misread while it animates or is blurred, and text in the filmed scene (a logo on a microphone, a print on a hoodie) is picked up; scenery that keeps returning in one place is filtered.
- **Sound** was measured, never heard. Stems come from a Demucs separation (about 2 dB uncertainty; breaths and plosives leak into the bed). In a video with music, sound events include musical hits. Only events within 13 dB of the voice are counted as strong.
- **Duplicate frames.** Two files hold repeated frames (30 fps content in 60 fps, a rarely changing screen). Detection runs on distinct frames only.
- **Nafay's speech timing** against text uses the English dub, which drifts from the original by up to a second or two.
- **The reasons for cuts** in section 8 of each analysis are a reading of the frames and the transcript, not a measurement.

## Rebuilding

```bash
python tools/fetch.py https://youtu.be/jtmstMt4WLc kallaway-dopamine-ladders
python tools/analyze.py reference/source/kallaway-dopamine-ladders.mp4 --slug kallaway-dopamine-ladders --lang en
```

The tools also run on your own renders, which is the way to compare a new edit with a reference (`skills/plan.md`).
