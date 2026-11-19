# Step 4: sound

Nobody listened to the references. Sound was measured: loudness of the mix, and after splitting each mix into a voice stem and a bed stem (music, effects, room), the level of the bed and every event in it with its time, length, level and frequency band. What an effect sounds like (click, whoosh, riser) is not known. Each event was matched against the picture at that instant.

## What was measured

| | Joseph | Kallaway | Ritesh | Nafay |
| --- | --- | --- | --- | --- |
| Loudness of the mix | -18.0 LUFS | -14.2 LUFS | -15.7 LUFS | -18.5 LUFS |
| Loudness range | 4.3 LU | 1.8 LU | 2.8 LU | 4.7 LU |
| True peak | -1.4 dBTP | -0.4 dBTP | -0.2 dBTP | 0.0 dBTP |
| Music | under 98 % of the video | none | 5 to 15 s and 25 to 35 s only | none |
| Music level under the voice | 25 dB below; 19 to 21 dB below in the last minute | - | about 12 dB below per beat | - |
| Strong sound events per minute | 26 | 2.8 | 1.7, all in the first 36 s | 6 candidates in the 22 s intro (not confirmed), then none |
| Typical event | 0.23 s, 8 dB below the voice | 0.2 s, 50 to 90 Hz, 3 to 6 dB below the voice | short hit; one swell of about 1 s | 0.03 to 0.3 s, 8 to 23 dB below the voice |

"Strong" means within 13 dB of the voice level. In these four long-form videos the weaker events were mostly voice leaking into the bed stem.

**Short-form edits are different.** In the reel reference (`reference/analysis/ig-reel-ref`) every effect sits 17 to 28 dB under the voice, so the whole-mix detector in `tools/audio.py` reported 0 effects while 25 were there. For any reel or Short, learn the effects with `tools/director/sfx_learn.py` (below), which works per frequency band on the voice-free stem and tests each peak against the voice stem for leakage.

## Sound follows movement

This is the one rule the references share.

- **Kallaway**: 22 of 26 eased zooms carry a short low sound starting within 0.3 s of the zoom. Fast camera moves inside graphics (snap reframes, whips, slides) carry the same sound. Punch cuts, hard cuts and text appearing carry none.
- **Joseph**: 21 of the 24 loudest events sit on a camera push or pull inside a graphic, a re-flow of the layout, a wipe, a "send" action or a drawn circle. 44 % of scene-change cuts carry a sound, against 10 % expected by chance; about 20 % of pop-ins and transitions do. Events are denser over graphics (30 a minute) than over the speaker (20 a minute).
- **Ritesh**: four placed effects, all in the hook: a hit on the first punch cut (4.24 s), a rise into the cut after the text page (11.75 to 11.93), a hit on the cut into the promise list (25.52), a swell of about 1 s peaking on the flash cut into proof (34.5 to 35.5, up to 4 dB over the voice). The other 15.6 minutes have none.
- **Nafay**: six quiet candidates in the intro, each on a graphic event (they overlap speech, so they are not confirmed); nothing over the screen recording.

So: put a sound where something on screen moves through space. Do not put one on every cut or on every word of text.

## Three settings

Take `audio.music`, `audio.sfx` and `audio.loudness` from `brand.json`; where they are empty, follow the style memory.

| Setting | Music | Effects | Follows |
| --- | --- | --- | --- |
| Dry | none | one low, short sound on each eased zoom and each fast move inside a graphic, 3 to 6 dB under the voice, about 3 a minute | Kallaway |
| Hook only | under the hook and the promise, then out | 3 to 5 placed effects in the first 40 s, none after | Ritesh, Nafay |
| Full | a bed all the way through, 25 dB under the voice | a short sound on moves inside graphics and on scene changes, about 8 dB under the voice, 20 to 30 a minute | Joseph |

## Levels

- Voice is the reference. Measure it with `tools/audio.py` (`voice.stem_rms_dBFS`).
- Music bed: 25 dB under the voice while it talks. No ducking was found that could be confirmed (pauses are too short to measure it), so set the bed once and leave it. Lift it 4 to 6 dB only for the closing minute or a stretch with no speech.
- Effects: 3 to 13 dB under the voice. Only a swell into a section change may reach the voice level.
- Final mix: the style's loudness, or -14 LUFS for YouTube, loudness range under 5 LU, true peak at or below -1 dBTP. Check with `tools/audio.py` on the render.
- Speech that deliberately stops (a clip plays, a result is shown) is the only place the bed or the clip's own sound carries the track.

## Placing an effect

1. List the moves from the camera plan and graphics plan: eased zooms, card shrinks, panel slides, camera moves inside diagrams, wipes, count-ups, section cards.
2. Give each move one sound that starts with the move (within 0.1 s; Kallaway's start within 0.3 s) and is no longer than the move plus 0.2 s.
3. Short and low for small moves (0.2 s). Longer, rising sound only into a section change or the first proof.
4. Keep one family of sounds for the whole video.
5. Thin them where they would exceed the setting's rate. Leave punch cuts, plain cuts and text silent.

## Learning a reference's sound effects

```bash
.venv/bin/python tools/analyze.py <reference> --slug <slug>                  # stems, cuts, text, words
.venv/bin/python tools/director/sfx_learn.py reference/analysis/<slug> \
    --library assets/sfx/catalogue.json [your_pack_catalogue.json]            # -> sfx_learned.md / .json
```

It lists every effect with time, layers (sub / low / tone / high / air), length, level under the voice, pitch and the
picture event it sits on (cut, pop, motion, caption change) with the offset, then a rule per class (count, rate,
level, offset, which picture events carry it), how the cut hits are layered, and the closest library sounds by
measured shape. Run it on your own render too and compare the two tables: that is the check that the effects match
(video1's reel: clicks -22 vs -20 dB, dings -16 vs -18, sub hits -26.5 vs -27 on the cut, all 7 cuts carried).

What the reel reference does (28.9 s): a sub hit with a bright transient exactly on every hard section cut (6 of 9,
offset about 0.00 s, about -27 dB); a crisp click on every on-screen tap or cursor click (about -20 dB); short 1 to
2 kHz beeps, sometimes two or three in a run, on app and phone reveals (about -18 dB). No music to speak of.

A music bed: `"music": {path, offset, under_voice_lu, fade_in, fade_out, tail_lift_db, tail_s, ride_db}` in the same plan.
`ride_db` (default 6) rides the bed so its 3 s loudness stays at the set distance under the voice; without it a
dynamic track swung from 14.6 to 22.6 LU under in one 31 s reel. A track with sung lyrics: separate it with Demucs
and use a stretch without singing, and look for a stop-down and drop (a near-silent gap, then +25 dB) to land on a
key cut (video1: the gap under "19 million views", the drop on the cut to the Short).
Pick the offset so a strong accent of the track lands on the first frame and a section change on a cut (earshot
`timeline` lists both). For an energetic track the user chose, 17 LU under the voice (the bed then measures about
-24 dB in `tools/audio.py`); calm long-form beds sit lower (`skills/plan.md`). With music in the mix,
`sfx_learn.py` on the render also catches music notes: compare effects on the `sfx_out` stem or on a render
without music.

## Ears: earshot

`vendor/earshot` is [earshot](https://github.com/Leonxlnx/earshot) (MIT, vendored at a pinned commit). It lets the
agent judge sound it cannot hear: describe a file, rank a folder against a description, find the best trim, A/B two
candidates, review a mix's timeline against the picture, and render a bank of 252 code-made effects. Its own
instructions are in `vendor/earshot/skills/earshot/SKILL.md`; read them before using it. Setup is part of
`requirements.txt`; the first call downloads two models (about 1.1 GB, free) into `vendor/earshot/.cache`.

Use it for taste decisions, with the numbers quoted:
- choosing: `tools/director/sfx_rank.py reference/analysis/<slug> assets/sfx/catalogue.json [your catalogue]` ranks
  candidates per learned class against the reference's own effect clips and a one-line description, in one process;
- checking a pick: `api.describe(path)` must name the right kind of sound (z above +2.5 is a clear reading);
- reviewing: `api.timeline(video, cues=...)` for sync and loudness. Its onset sync is measured on onsets, so effects
  aligned by their peak (reverse swells) read early: judge those with `sfx_learn.py` on the render.

## Reel effects

`tools/director/sfx_reel.py plan.json` prints the effects of a reel: each sound's loudest 20 ms lands on its picture
event, its level is set against the voice the same way `sfx_learn.py` measures a reference, pitch ladders for
repeated dings, composition times divided by the reel's speed (1.15), then the voice and effects are mastered
together to -14 LUFS with a -1.5 dBTP ceiling. Plan format in the tool's docstring; the effect recipe for the orange-canvas reel style is in `memory/styles/orange-canvas-reel/style.md`.

## Libraries

- **Bundled and free to redistribute**: `assets/sfx/` (see its README): Kenney CC0 interface, UI, digital and impact
  packs, and earshot's bank rendered to files (MIT). `assets/sfx/catalogue.json` holds their measurements.
- **Your own pack**: measure it with `tools/director/sfx_library.py "<pack folder>" <out.json>` and pass the JSON to
  `sfx_learn.py --library`. Keep it outside the repo unless every file in it may be redistributed: packs passed
  around online often hold sounds from paid libraries (file names starting `ES_` are Epidemic Sound) or clips cut
  from films and anime. Those are fine to use only as far as your own licence goes, and never to publish.

## Free sources

Everything must be free to use in a monetised video, with the licence recorded in the credits file.

| Source | What | Licence |
| --- | --- | --- |
| Kenney audio packs (kenney.nl) | interface clicks, impacts, whooshes | CC0 |
| Mixkit (mixkit.co) | sound effects and music as WAV or MP3 | Mixkit free licence; read the current terms on the site |
| Incompetech (incompetech.com) | music, searchable catalogue | CC BY 4.0, credit required |
| Freesound (freesound.org) | everything, filter by CC0 | per item; needs a free account or API key |
| Pixabay audio, YouTube Audio Library | music and effects | manual download; YouTube's library is documented for use on YouTube only |
| React Bits Sound Lab | interface sounds | free to use in a video; may not be redistributed as a pack |

Never generate a voice. Never use a track the user cannot show a licence for. If the user supplies their own music or effects, use those first.

## Checking

Run `tools/audio.py` and `tools/timeline.py` on the render. In `summary.json`: `sfx.strong_per_min` should match the setting, `sfx.strong_on_picture_event_share` should be well above `strong_chance_share`, `audio.bed.median_rel_voice_dB` should be at the planned level, and loudness and peak at target.
