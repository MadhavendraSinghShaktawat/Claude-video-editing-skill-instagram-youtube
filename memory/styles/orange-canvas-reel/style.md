# Style: orange-canvas reel (vertical 1080×1920, from reference/analysis/ig-reel-ref, 2026-11-18)

The default style for the user's reels (Instagram / Shorts). Measured on the reference (29 s, 30 fps): 23 cuts/min
(9 hard, 1 jump, 1 pop), voice 287 wpm with one 0.12 s pause, no music to speak of (bed −42.5 dB), −14.2 LUFS, and
25 sound effects 17 to 28 dB under the voice (`reference/analysis/ig-reel-ref/sfx_learned.md`; the whole-mix
detector missed them all).

## Layouts
| name | what | reference time |
|---|---|---|
| split | orange "design canvas" (gradient #C9592B→#7C2915, faint 90 px grid, ruler ticks on both edges, a dashed arc, "R10"/"30°" labels); top panel 850×460 at y 470 with a white frame, round corner handles, pill mid-edge handles and a cursor; speaker card 864 wide from y 1380 bleeding off the bottom, head cut out (RVM) so it rises above the card's top edge | 0–4.8, 11.4–21 |
| full screen | a screen, website or the product itself; captions at y≈0.74 over a dark gradient | 4.8–11.4 |
| phone | iPhone mockup on the orange canvas | 21–24.5 |
| face | full-frame close-up for the call to action: script "comment" over an orange box with the keyword | 25–29 |

## Type and captions
- One to three words at a time, lower case except names, Inter 800 about 78 px, white with a soft shadow.
- About one word per sentence in a handwritten script (Caveat) as the accent.
- Captions enter with blur, fade and a slight rise (0.16 s) and are replaced, not animated out.
- Split layout: captions sit in the gap between panel and card (y ≈ 1060). Title on the first beat: one bold line
  plus a second line in a translucent box with text-selection handles.

## Rules learned building video1's reel
- Pick lines by the reference's structure: hook with a number → "this one is mine" → what it is not → what it is →
  how it works (one command, approve three things) → proof (time) → closing line + comment keyword.
- Cut on the quietest 10 ms near each word edge (`work/video1/reel/snap.py`), then re-transcribe the joined voice
  to confirm no stray word survived.
- Section containers holding <video> must be hidden with opacity, not visibility: HyperFrames makes active clips
  visible, which beats a hidden parent.
- A GSAP fromTo placed later on the timeline renders its from-state at build time; give entrance tweens on
  always-present elements `immediateRender: false`.
- If inserted footage has its own burned-in captions (the user's Short), put the reel's captions at the top over a
  top gradient so the two never sit on top of each other.
- Loudness: limiter at 192 kHz, then gain; a mono voice panned to dual mono reads +3 LU louder.
- The renderer ignores `object-fit` and rounded-corner clipping on <video> frames: size a video inside a mockup
  explicitly to cover its screen and clip the screen with `clip-path: inset(0 round R)` (phone fix, v2).
- Pace: the user found the natural talk "way too slow" for a reel and asked for 1.15× overall. Do it without
  dropped animation frames: render the composition at `--fps 500/23` (25 / 1.15), retime to 25 fps with
  `setpts=PTS*(500/23)/25`, and speed the voice with `atempo=1.15` before mastering. Default new reels to 1.15×.

## Safe zone (Instagram)
Keep every word, panel and call to action inside y 220 to 1500 and clear of x > 940 between y 960 and 1500 (the
like / comment / share column). The speaker card may bleed off the bottom; text may not. v1 put the CTA at y 1470 to
1700 and the user flagged it. Positions that pass: title from y 250, split captions at 1062, editor 220 to 1280 with
its caption at 1370, timer 230 and phone 440 to 1400 with the caption at 1475, close-up caption 1150 and CTA 1240.

## Sound effects (learned from the reference, checked on video1's reel)
| picture event | sound | level under the voice | placement |
|---|---|---|---|
| every hard section cut, and the first frame | sub thud + reverse swell (bright air) | thud −19, swell −23 (plan rel) | the thud's and the swell's peaks on the cut |
| cursor click, checkbox tick | mouse click | −14 to −16 | peak on the click frame |
| reveal (highlight, pill, timer done) | short beep, ladder 0 / +2 / +4 semitones in runs; a success chime for the big ones | −12 to −14 | peak on the reveal |
| strike-through | pop stepping down 0 / −2 / −4 | −16 | on the strike |
| typing on screen | keyboard run | −21 (−25 under talk-heavy code) | starts with the typing |
Plan rel values are `sfx_reel.py` levels; measured by `sfx_learn.py` on the render they read clicks −22, dings −16,
sub hits −26.5 against the reference's −20, −18, −27. Pick sounds with `sfx_rank.py`, which ranks them against the
reference's own clips.
