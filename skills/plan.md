# The edit plan, rendering and review

## Where things stand

| Part | State |
| --- | --- |
| Measuring any video (`tools/analyze.py` and the tools under it) | built and used on nine videos |
| Memory: brand answers, styles, notes | built |
| Rough cut: cut list, review file, render of the cut | built; retake detection needs a human check every time |
| Renderer: speaker camera, layouts, motion graphics, sound (`tools/director/`) | built; first full edit made with it (video1, 12:04) |

## The director (`tools/director/`)

The edit is a JavaScript plan run in a HyperFrames page. `director.js` gives the plan its vocabulary; every visible change is a tween on one paused GSAP timeline, so any frame renders on its own.

```bash
# 0. once per project: a HyperFrames folder with the free packages
mkdir -p work/<slug>/edit/hf && cd work/<slug>/edit/hf && npm init -y && npm i hyperframes@0.9.41 gsap@3.13.0 @hugeicons/core-free-icons@4.4.0
# 1. the graded cut, re-encoded with a keyframe every second (HyperFrames seeks it frame by frame)
ffmpeg -i graded.mp4 -an -c:v libx264 -crf 12 -g 25 -bf 0 -pix_fmt yuv420p work/<slug>/edit/speaker.mp4
# 2. face position for every 0.2 s (camera anchors and speaker-card crops)
.venv/bin/python work/<slug>/edit/faces.py graded.mp4         # see work/video1/edit/faces.py
# 3. write work/<slug>/edit/plan.js and edit.json (see build.py's docstring), then build and check
.venv/bin/python tools/director/build.py work/<slug>/edit/edit.json
node tools/director/check.mjs work/<slug>/edit/hf            # phrases not found, missing icons, page errors, sound cues
# 4. render the picture in chunks, then mix the sound onto it
PY=.venv/bin/python tools/director/render.sh work/<slug>/edit/edit.json work/<slug>/edit/hf work/<slug>/edit/renders/final_picture.mp4 180
.venv/bin/python tools/director/mix.py work/<slug>/edit/mix.json
```

What the plan can call (all in `director.js`):

| Call | Does |
| --- | --- |
| `D.at("phrase", from)` | output time of the first word of a spoken phrase, from the cut's word timings. Always pass `from` when the phrase could have been said earlier. Speech recognition mishears ("Cloud" for Claude, "sword" for Short): `SYN` maps the common ones; otherwise anchor on the words as heard |
| `D.speaker(t, layout, {zoom, dur})` | move the speaker: `full`, `right`/`left` (38.2 % card beside a 61.8 % graphic), `pip`, `small`, `halfL`/`halfR`, `circle`, `gone`. The face stays at the measured spot inside the window |
| `D.punch(t, levels)`, `D.ease(t, levels)`, `D.drift(t0, t1, rate)` | x1.047 cut per level; 0.46 s eased zoom; slow drift that alternates in and out so no held shot is still |
| `D.scene(t0, t1, area)` | a graphic stage beside the current layout; it fades out on its end and drifts while held |
| `D.words`, `D.card`, `D.pill`, `D.tile`, `D.counter`, `D.strike`, `D.terminal`, `D.image`, `D.phone`, `D.browser` + `D.focus`/`D.mark`/`D.spot`, `D.cursor`, `D.timer` | the parts: word-by-word text, cards, labels, icon tiles, counters, strike-throughs, typed terminals, images, phone frames, captured web pages with camera moves and highlights, a clicking cursor, a running timer |
| `D.cue(t, name, gainDb)` | a sound effect for the mix (`mix.json` maps names to free files) |

The look is `director.css`: tokens for canvas, ink, accent, type steps and radii. Change the tokens, not the plan, to restyle.

Web pages go in as captures, not live (`tools/director/capture`: `npm i` there once, then `node capture.js pages.json out_dir`): a headless browser saves each page at 2x with the boxes of the elements that matter (titles, rows, buttons), and the plan zooms and pans the image. This stays sharp and every frame is reproducible.

### Rules learned on the first full edit

- HyperFrames refuses a render whose working folder passes 2 GB, extracts every frame of every clip in the page whatever `--start`/`--end` say, and copies the whole project folder. So: footage is split into 100 s segment files, each chunk renders from a page holding only the segments it overlaps (`build.py --range`), and renders are written outside the project folder. `render.sh` does all three.
- Times for anything on screen come from words, never typed seconds. Every phrase the plan uses must be found (`check.mjs` lists the misses) and must be the right occurrence: a common phrase ("the characters", "speech model") also appears earlier in the video, so pass `from`.
- An inserted video (the result the speaker says "let's watch" about) is placed in the silence between two words, never on the next word's onset.
- A number on screen must be the one that is said, even when the live page now shows a different figure; say so to the user.
- Real artefacts beat illustrations: the actual report, credits file, code, contact sheets and measured data were used wherever the script names them.

### Motion, sound and quality rules from the second pass (user feedback on video1)

- **Springs, not eases.** Every arrival and camera move is a closed-form spring (`D.spring(damping, response)`), a pure function of time. Measured on an Apple UI morph (refs/apple_timer.mp4): the pill grows almost linearly for 0.26 s while untilting from -11 deg, overshoots its final size by about 7 %, settles in about 0.4 s with one small second bounce, so damping about 0.68. Use that (`SP.apple`) for things that pop or morph; `SP.smooth` (critically damped) for cameras, pages and the world; `SP.layout` for the speaker window. Never scale from zero, never fade without a blur, never a flat `power2.out` on everything.
- **Continuous transitions.** A scene never fades out to an empty canvas: the next one pushes in while the last one leaves the same way and the dot-grid world pans with them (refs/explainer.mp4: a picture change about every 1.2 s with motion inside every shot). Section markers are a panel that slides through with large type over a moving soft colour wave.
- **Text must fit its box.** After fonts load (`window.__hf.buildReady`), every text element in a card is measured and shrunk to its box; `check.mjs` lists what shrank. Nothing may rely on `overflow: hidden` or an ellipsis.
- **Phrase search starts at the current scene.** `D.at` without a start searches from the scene being built; `check.mjs` lists phrases that were also said earlier so they can be confirmed. A label that appears before the thing it labels ("-10 s" before its row) is this bug.
- **Timers are Apple islands** (`D.island`, `D.clock`): a pill tilts in, springs level, morphs into a clock whose digits roll like wheels over the last 30 % of each second.
- **Render at 4K** (`HF_EXTRA="--resolution landscape-4k --video-frame-format png"`): the same 1920x1080 layout is drawn at 2x, so type and edges are sharp, and YouTube serves 4K uploads at a much higher bitrate than 1080p ones, which removes the soft, dull look on playback. The footage itself is only as sharp as the graded export: ask for a high-bitrate export (ProRes 422 or 40+ Mbps), a 2 Mbps export looks soft whatever the edit does.
- **Sound design** (`mix.py`): the user's own effects library first. Every effect is loudness-matched relative to the voice by type; whooshes are aligned on their loudest moment, risers end on their hit; variants rotate; cues pan to where the element is; same-kind effects closer than their gap are skipped and at most three start within 0.35 s. Music: one track per section, chosen by genre and measured energy (skip quiet intros and breakdowns), crossfaded, about 20 LU under the voice, swelling only under section markers, off while an inserted video plays its own sound. Keep effects to about 20-30 a minute.
- **Type:** Inter (optical sizes) and JetBrains Mono, both SIL OFL; display sizes at weight 600-700 with tight tracking.

### Themes

A theme is a CSS + JS pair in `tools/director/themes/` listed in `edit.json` `theme_files`; it adds its own parts
on top of `director.js`. `bluehour` (memory/styles/bluehour/style.md) gives `BH.stage` (full-bleed navy world with a
camera rig that keeps pulling back), `BH.tile`, `BH.pill`, `BH.wire`, `BH.say` (MagicUI and Componentry text
presets), `BH.morph`, `BH.roll`, `BH.chips`, `BH.caption`, `BH.frame`, `BH.img`, `BH.card`, and paper scenes with
`BH.marker`. `center_speaker` in `edit.json` keeps the speaker centred in full frame; `D.shake` adds a decaying
camera shake.

`studio` (memory/styles/studio/style.md) keeps the speaker on screen most of the time. Its layouts follow the
golden ratio and come from the user's references:
- `splitR`/`splitRm`: a panel plus a speaker card on a cream canvas;
- `splitL`: the speaker on the left, a dark lime-edged panel inside a white frame;
- `pip`: a dark stage with the speaker picture-in-picture;
- `ST.cut`: the speaker cut out with words behind them.

Its parts are reusable components: `ST.list` (AnimatedList), `ST.orbit`, `ST.tweet`, `ST.safari`, `ST.iphone`,
`ST.cursor`, `ST.pill`, `ST.odo`, `ST.flicker`, `ST.aurora`, and the text animations `ST.type`, `ST.rotate`,
`ST.morph`, `ST.flip`, `ST.dia`, `ST.hl` and `ST.kinetic`. It also has the four title stacks `ST.titleA`–`D`.
`ST.frame` never uses the same entrance twice in a row.

Cutouts (`ST.cut`), as the user corrected on video1:
- **Layering.** The person is never put on a flat or black canvas. The layers are, bottom to top: the real footage,
  the words and graphics, then the same footage with its background removed.
- **Making the mattes.** `tools/director/matte.py` (RobustVideoMatting, free, runs on the Mac GPU) makes one alpha
  WebM per span. `make_cutouts.py` makes them from `hf/cutouts.json`, which `check.mjs` writes. Re-run it whenever a
  cut's times change.
- **Alignment.** `ST.finish` holds the camera still at zoom 1.0 under a cutout, and settles to 1.0 just before one,
  so the person lines up pixel for pixel. A `D.punch` inside a cutout is reported as an error. `D.shake` moves the
  footage and the cutout together.
- **Placement.** Use `ST.head(t)` to put the words above the head or beside it, never where the head hides letters.

3D icons from 3dicons.co (CC0) download as RGB on white. Run `tools/director/icon_alpha.py <folder>` once to make
the backgrounds transparent, otherwise they show as white squares.

`D.h` style objects may hold CSS variables (`"--k": 1.3`); they are set with `setProperty`.

`check.mjs` also scans the timeline, without rendering, every 0.5 s. It reports:
- text whose glyphs leave the frame or are clipped by their panel, allowing the line box about 0.2 em of slack;
- text sitting on the speaker's card or picture-in-picture (words behind a cutout don't count);
- panels that stay empty for more than 1.2 s after they arrive, with the plan line that made them;
- panels that `ST.finish` ended early. A panel ends once nothing new has arrived in it for `ST.HOLD` (4.5 s), and the
  speaker takes the whole frame back.

Fix everything it lists that lasts more than one sample; one-sample flags happen mid-transition. A JavaScript error in
the plan stops the check with an error, so a broken page can never look clean.

On video1 the user noticed, and these checks now catch:
- panels holding one static picture for 15–25 s;
- empty stages with only a small kicker before the title;
- browser views cut mid-column. Frame captures from gap to gap, measured on the capture image.

Review every render at 5 frames a second, not one: `tools/director/qa_sheets.sh <video> <dir> <offset>` writes
12-second sheets of 60 frames each. Things it caught on video1 that 1 fps sheets missed: centred titles wrapping,
empty stages before their first element, a label appearing on the wrong occurrence of a word, a camera framing that
cut a tile in half.

### Sound design in DaVinci Resolve (video1 v4)

The user cleans the voice in Resolve: noise and hiss removal sit on the voice track. Effects go on their own tracks
under that track, never into the picture render, and the voice track is never touched. There is no music unless
the user asks for it.

**Measure the voice's channels first.** video1's camera audio had the mic on the right channel only: left was
−87 dB, right −14 dB. Every export up to v4 played the voice in one ear, and centred effects buried it ("I can't
hear my voice"). `mix.py` now measures both channels and makes a one-sided voice dual mono. Integrated loudness
hides this, so also check L/R levels and their correlation on every delivered file.

1. **Log what is on screen.** `node tools/director/events.mjs <hf> events.json`. Every studio component records
   when it does something visible: panels in and out, cutouts, titles, numbers, words, list items, pills, clicks,
   typing, punches and shakes.
2. **Measure the library.** `python tools/director/sfx_library.py "<library>" sfx_library.json <folders…>`. For
   every file it records:
   - length and lead silence;
   - loudness and sample peak, and whether it clips;
   - where its loudest 20 ms falls, its attack and tail;
   - whether it builds (riser) or decays;
   - brightness, sub weight and stereo width.

   Pick the pools from these numbers, and drop files that clip or are duplicates (identical measurements). In the
   user's 500+ pack, many "Nth Woosh" files are the same file.
3. **Plan and print.** `python tools/director/sfx_plan.py sfx.json`. Each moment is layered:
   - a panel arriving gets a whoosh, plus a low layer for big layout changes;
   - a cutout gets a reverse suction that ends exactly on the cut, a sub drop, and an impact on its first big word;
   - a title gets a riser into the word, a sub ramp, an impact and a sub;
   - small elements get panned whips, only where nothing bigger already sounds;
   - the opening gets a drone and a riser into the first big number;
   - the ending gets a long riser and thunder.

   Each sound is printed as its own WAV, with silence in front so its measured peak lands on the exact sample.
   Resolve places clips on whole frames only, which is 40 ms at 25 fps.
4. **Set levels on the loudest 400 ms.** Gain sets each print's loudest 400 ms (momentary loudness) a set number of
   LU under the voice. Integrated loudness is not used: a hit with a long tail measures quiet and would be set far
   too loud. On video1 the sub hits came out within 1.4 LU of the voice before this change.
5. **Check before importing.** `python tools/director/sfx_check.py sfx_plan.json <video> preview.wav` measures:
   - alignment error;
   - effects vs voice while the voice speaks, at least 8 LU under;
   - the combined peak;
   - effects per 10 s.
**Match each sound to what the thing on screen is.** The user's verdict on the first pass was "not up to the mark":
generic whooshes on everything, plus ghostly, metal and distorted sounds that do not fit a clean tech explainer. The
palette that replaced it (`work/video1/edit/sfx5.json`):

| On screen | Sound | Detail |
|---|---|---|
| List items, which look like notifications | a soft notification bell | rises 0, +2, +4, +5, +7 semitones through each list, like notifications stacking |
| Message / tweet cards | a message pop | |
| Pills and labels | a light "explainer pop" | small pitch variation |
| 3D icons | a bubble pop | |
| Rolling numbers | an electric ticking counter | |
| Clicks, timer, screenshot | interface clicks, a tech notification bleep, a camera shutter | |
| Typing | laptop keys | |
| Panel changes | clean air sweeps | |
| Cutouts and titles | movie-trailer whoosh-hits and impacts with a short bass hit | |
| Opening | a "movie logo intro" build that lands on the first big number | |
| Ending | a suspense build into the last line | |

Free, no-attribution sources that work from a script:
- **Mixkit** (Sound Effects Free License). Get the real file URL from `/free-sound-effects/download/<id>/`. The
  direct `<id>.mp3` path returns 403.
- **Kenney** (CC0). Load the asset page for its cookie, then use `/download-link/<hex of "assets/<name>">`.

Measure the downloads with `sfx_library.py` like any other library. Then run `tools/director/sfx_fit.py`, which
lowers only the effects at moments where voice plus effects pass −1.5 dBFS, or where the effects come within 8 LU of
the voice.

**Music bed (video1 v4).** Measure the candidates with `tools/director/music_library.py`, which reports:
- energy in the voice band (1–4 kHz);
- steadiness;
- tempo;
- a 10 s energy profile.

Choose tracks with little voice-band energy (but not bass only, which vanishes on phones), a steady level and no
vocals, one per part of the video. Then render the bed alone with `mix.py`'s `bed_out`: sections with crossfades,
5 dB ducking under the voice, and silence under the inserted Short. Place it on a "Music" track. The user wants the bed **calm and in the background**: "the tutorial should be more focused on the tutorial
instead of the song." Upbeat picks were rejected, for example Deep Urban (pulse 0.91) and Autofahren (0.85). Choose
by the measured `pulse` (under 0.45) and `hits_per_s` (under 3). Set the level at about 23 LU under the voice while
speaking (`under_voice_LU` 19, `duck_dB` 5). Mixkit's Stock
Music Free License covers monetised YouTube with no attribution, but Content ID immunity is not guaranteed.

**Exporting from Resolve (video1 v5).**
- **Timeline resolution.** The user's timeline was 1080p over 4K media. Set the timeline to 3840×2160
  (`useCustomSettings` plus the resolution settings) before rendering; otherwise a 4K export is an upscale.
- **Render settings.** Pass `SetRenderSettings` one key at a time: a single bad key (for example `AudioBitDepth`
  with AAC) makes the whole call fail and silently drops `VideoQuality`. The first export came out at 9.9 Mbps.
  With `VideoQuality` 45000 (a ceiling), H.264 averaged 14 Mbps, and SSIM against the 4K master was 0.997–0.998.
- **Loudness.** Measure the export. The user's voice processing on Audio 1 lowers the voice path by about 4.7 dB,
  so the export measured −18.9 LUFS. Master the exported audio to −14 LUFS (limiter, then two-pass linear
  `loudnorm`, true peak −1.5) and copy the video stream. The balance set in Resolve stays as it is.

6. **Place in Resolve with the DaVinci Resolve MCP.**
   - Import the prints into a bin.
   - Add the tracks: Riser, Whoosh, Whoosh Low, Impact, Sub, Detail, Texture, plus numbered lanes where clips
     overlap.
   - `AppendToTimeline` places each print at `recordFrame = timeline start + frame`, then set `AudioVolume` and
     `AudioPan`.
   - Run it in batches of about 70; one call is limited to 60 s.
   - Read the timeline back and compare every clip's frame, gain and pan with the plan before saving.

## Render stack

All free, chosen from the benchmark in the sibling skill `faceless-youtube-shorts-3d` (`research/render-stack.md`):

- **HyperFrames** (Apache-2.0) as the host: HTML pages rendered frame by frame through headless Chrome, with multi-track audio and volume envelopes. It gives each frame a time; the page draws that instant.
- **ffmpeg** for the footage: the rough cut, scaling and the final mux.
- Graphics as HTML and React parts (`skills/graphics.md`, section 6) driven by the frame clock, never by wall-clock timers.
- Remotion is not used: its licence is free only for individuals and companies of up to three people, which a public skill cannot assume.

## `work/<slug>/edit.json`

Times are seconds on the rough-cut timeline unless marked `src`. Every timed element names the word it is locked to, so re-cutting moves it.

```json
{
  "source": "raw.mp4",
  "style": "kallaway-dark-studio",
  "format": {"width": 1920, "height": 1080, "fps": 30},
  "keep": [[0.0, 4.2], [4.9, 11.3]],
  "beats": [
    {"t0": 0.0, "t1": 7.4, "kind": "hook", "text": "..."}
  ],
  "camera": [
    {"t0": 0.0, "t1": 7.4, "level": 1.0, "anchor": [0.5, 0.38],
     "moves": [
       {"type": "punch", "at": 3.1, "to": 1.047, "word": "but", "why": "take join at a new sentence"},
       {"type": "ease", "t0": 5.2, "dur": 0.46, "to": 0.953, "word": "three", "why": "make room for side labels"},
       {"type": "drift", "t0": 0.0, "t1": 3.1, "pct_per_s": 0.4}
     ]}
  ],
  "graphics": [
    {"id": "g1", "t0": 5.6, "t1": 9.8, "pattern": "side labels", "layout": "beside speaker",
     "said": "the bigger the question, the bigger the curiosity",
     "why": "two linked ideas: cause left, effect right",
     "elements": [
       {"text": "Bigger question", "on_word": "question", "at": 5.9, "side": "left"},
       {"text": "More curiosity", "on_word": "curiosity", "at": 7.1, "side": "right"}
     ],
     "enter": "type on", "exit": "cut", "components": ["@magicui/typing-animation"]}
  ],
  "text": [
    {"t0": 12.0, "t1": 14.0, "kind": "key-sentence caption", "text": "...", "accent_words": ["tight"]}
  ],
  "audio": {
    "loudness_LUFS": -14, "true_peak_dBTP": -1,
    "music": [{"file": "assets/bed.mp3", "t0": 0, "t1": 36, "rel_voice_dB": -25}],
    "sfx": [{"file": "assets/low-hit.wav", "at": 5.2, "rel_voice_dB": -5, "for": "camera ease at 5.2"}]
  },
  "credits": [{"what": "low-hit.wav", "source": "kenney.nl", "licence": "CC0"}]
}
```

Rules for the plan:
- Every `camera.moves`, `graphics` and `audio.sfx` entry has a `why` or a `for`. No reason, no entry.
- `graphics[].elements[].at` comes from the word onset in the re-transcribed rough cut, not from a guess.
- Colours, fonts and sizes are not in the plan: they come from `brand.json` and the style at render time, so one change restyles the whole video.

## Review loop

After a render, measure the result exactly as the references were measured and compare:

```bash
python tools/analyze.py work/<slug>/out/final.mp4 --slug <slug>-render --out work/<slug>/check
```

| Check in `summary.json` | Against |
| --- | --- |
| `audio.pause_stats.median_s`, `p90_s` | the style's speech numbers |
| `cuts.picture_change_every_s` | the style; no gap past its longest |
| `camera_on_face_shots.punch_cut_scale`, `eased_zoom_moves` | what `edit.json` planned |
| `text.appears_vs_word_s` | within 0.3 s |
| `audio.loudness` | target loudness and peak |
| `sfx.strong_per_min`, `strong_on_picture_event_share` | the sound setting |

Then read `check/<slug>-render/shots/*.jpg`, every sheet, beside `timeline.md`. Look for: text across the face, a graphic that outlives its sentence, two graphic systems in one video, a speaker shot with nothing happening past the limit, any change in the colour of the footage.

Fix, render again, and only then show the user.


## Vertical reel cut from a long-form (video1, 2026-11-18)

Project: `work/video1/reel/` (`segments.json` → `snap.py` → `assemble.py` → `matte.py` on the joined speaker →
`hf/index.html` + `assets/reel.js`, one paused GSAP timeline, 1080×1920 at 25 fps). Style and its lessons:
`memory/styles/orange-canvas-reel/style.md`. Render with `hyperframes render --fps 25 --crf 14`, review with
`tools/director/qa_sheets.sh <mp4> <dir> 0 5`, master the voice to −14 LUFS (limiter first), mux with video copy.
Reels run at 1.15× (render `--fps 500/23`, retime with `setpts=PTS*(500/23)/25`, voice `atempo=1.15`). Effects:
`sfx_learn.py` on the reference → `sfx_rank.py` → a plan for `sfx_reel.py` → `sfx_learn.py` on the render to compare.
Check the Instagram safe zone on snapshots before the full render (style file).
