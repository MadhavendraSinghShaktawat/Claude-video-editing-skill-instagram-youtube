# Step 2: camera motion on the speaker

All camera motion here is made in the edit by scaling and moving the footage. The camera on set is locked. Motion is measured as a scale factor: x1.10 means the picture is 10 % larger.

How much to move comes from `brand.json` `camera.motion` and the style memory. The three talking-head references use three different systems. Pick one and stay in it for the whole video.

## System A: fixed levels (Kallaway)

Measured by matching the background between shots: the speaker only ever appears at four sizes, each x1.047 apart.

| Level | Scale |
| --- | --- |
| wide | 0.953 |
| base | 1.000 |
| close | 1.047 |
| closest | 1.095 |

- **Punch cut**: at a take join that starts a new sentence, change one level, instantly. 27 times in 22 minutes, 15 in and 11 out, mixed so the size stays within the four levels. No sound.
- **Eased zoom**: inside a shot, move two levels (x1.09 in or x0.915 out) over 0.46 s (11 frames at 24 fps). About once every 37 s of speaker time. Gets a short low sound (`skills/sound.md`).
- **Zoom out to make room**: every eased zoom-out comes 0.2 to 9 s before text or icons appear beside the head; the zoom-in follows when they leave, or on a turning line ("Now, here's a big pro tip").
- Otherwise the frame is still. Something changes on the speaker picture (cut, zoom, overlay in or out) every 2.1 s on median; the longest untouched stretch is 17.6 s.
- Framing: face 31 % of frame height, centre at x 0.51, y 0.37.

## System B: blur-and-scale entry and exit (Joseph)

- **Entry**: 58 of 99 speaker shots start blurred and at about 92 % size, then sharpen over 5 to 12 frames while scaling up x1.086 in 0.33 s.
- **Exit**: 40 of 99 end with a x1.107 push over the last 0.33 s while blurring out, leading into a graphic.
- **Hold**: between entry and exit the frame is still, or drifts in at about 1.1 to 1.3 % per second on shots that carry a caption. Only 19 mid-shot zooms in 99 shots.
- **Punch-in**, instant, x1.11 to x1.20: only on the sentence that states the stakes or the promise (1.77, 34.10, 698.13 s).
- **Punch-out** through a blur dip, x0.81 to x0.87, 4 frames out and 5 in: on a pivot sentence ("So...", "After...", "Now...").
- **Zoom out for overlays**: x0.71 to x0.90 over 0.5 to 2.6 s with the background dimmed, before cards appear around the speaker.
- Framing: face 37.5 % of frame height, centre at x 0.50, y 0.38. Speaker stretches run 4.6 s on median, 18 s at most.

## System C: visible jumps and slow drift (Ritesh)

- 20 take joins are left as plain jump cuts at the same framing.
- Only 6 punches in 16 minutes: in x1.17 on "here's a reframe", out x0.81 to x0.89 at the start of a new instruction.
- **Slow drift** on long shots: 0.2 to 0.8 % per second, in or out, 1 to 7 % in total. 13 of 58 full-frame shots are fully static.
- **Closing argument**: step slightly tighter at each jump cut and keep drifting in, about +15 % over 35 s.
- Framing: face 33 to 37 % of frame height, centre at x 0.45 to 0.51, y 0.35 to 0.41.

## If the user wants the camera never still

That is beyond what two of the three references do, so build it from their measured parts rather than inventing a move:

1. Base: System C drift on every speaker shot, 0.3 to 0.8 % per second, alternating in and out so the size stays inside the limits below. Start each shot already moving; never ease in from still.
2. Joins: System A punch, one level of x1.047 (or the style's `punch_in_scale`).
3. Emphasis: one instant punch of x1.11 to x1.20 on the stakes line and on each section's key claim. Keep it rare.
4. Before an overlay: an eased zoom-out, 0.46 s, to make room.

## Limits

- **Largest size** = `brand.json` `camera.max_zoom`. Without it: source pixel width divided by timeline width, less 5 %. 4K footage on a 1080p timeline allows about x1.9; 1080p footage on a 1080p timeline should stay at or under x1.2, the largest punch any reference uses.
- **Scale about the face**, not the frame centre, when the face is off centre: keep the eyes at the same height through the move (measured face centre y stays 0.35 to 0.41 in all three).
- Never show the frame edge on a zoom-out: the wide level needs the base framing to be scaled up first (Kallaway's base is already 1/0.953 of his widest picture).
- An eased move is 0.33 to 0.46 s. A drift is under 1.3 % per second. Nothing in between was measured.

## Speaker layouts other than full frame

| Layout | Measured | Used for |
| --- | --- | --- |
| Portrait card on a page, graphic beside it | Ritesh: card 26 % of frame width, 71 % of height, rounded, at x 0.685 to 0.948, graphic in the left 65 %. Shrinks from full frame in 0.55 to 0.95 s, ease-out | the speaker stays visible beside a small graphic, about 6 s at a time |
| Portrait picture-in-picture | Nafay: 21 % x 53 % of the frame, right edge, radius about 24 px at 1080p, 3 px light border, moves in 0.37 to 0.43 s | sentences that name something drawable |
| Half frame beside a panel | Ritesh: a white panel slides over the left 50 % in 0.9 s, out in 0.7 s | a quick list of 3 or 4 items |
| Corner card | Kallaway: face about 10 % of frame height, clip in the centre, checklist at the side | a worked example |
| Round inset | Ritesh: 20 % of frame height, bottom right, over a screen recording at 88 % size | screen demos |
| Blurred and dimmed behind text | Kallaway: blur over 10 frames, back over 10 | the question the video answers |

Never hard-cut between two speaker layouts in the same sentence: scale the clip itself (0.37 to 0.95 s, ease-out).

## Planning it

For each speaker span in the cut write to `edit.json`: start level, the move (none, drift rate, eased zoom with start and factor, punch at a join) and the word that triggers it. Check afterwards with `tools/visual.py` on the render: its `zoom_moves` and `cut_in_scale` should match what you planned.
