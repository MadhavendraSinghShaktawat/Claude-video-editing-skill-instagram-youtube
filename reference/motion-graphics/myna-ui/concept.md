# myna-ui: one screen, continuous pull-back

- Source: `reference/source/mg/myna-ui.mp4`. 736x414, 30 fps, 245 frames, 8.17 s of video (container 8.36 s). Values from `shots.json` and `sheets/sheet_index.json`.
- Sheets read: `sheets/sheet_001`-`004` (10 fps, all of them) and 30 fps sheets `sheets30/t0.9`, `t3.2`, `t4.3`, `t5.3`, `t6.9` (frames 27-56, 96-125, 129-158, 159-188, 207-236).
- Frame numbers below are source frames (f); time = f / 30.

## Concept in one paragraph
A product teaser for a tool whose on-screen name is "myna" (logo text at 0.0 s) with the headline "The No-Code Platform" (0.3 s). The single idea: the picture never cuts away to something unrelated. Each scene turns out to be an object inside the next one. A dashboard becomes a chart, the chart turns out to be on a monitor (1.13-1.47 s), the monitor scene turns out to be a card on a pastel page (4.4-4.7 s), the card collapses to a line (5.3-5.9 s) and the panel behind it becomes a "Create Agent" form (6.1-6.5 s). The canvas is always drifting or zooming out, so the viewer is always being shown "one level up".

## Look
- 2D flat UI with one faux-3D object (the monitor is a flat drawing with a stand; no perspective change seen on it). The dragged file chip is tilted about 10 degrees and levels out (7.1-7.7 s), still 2D.
- Palette, scene 1 (0-1.1 s): UI white `#fbfbfc` (55% share, shots.json shot 0), deep blue background `#0a3058` / `#113a67`, lighter blue glow `#386fac`. Headline text light blue `#99c9f6` on `#235386` (text.json).
- Palette, scene 2 (1.1-4.7 s): blue-to-violet diagonal gradient, sampled `#0442ed` top-left and `#4d00e0` bottom-right at f75; dark navy `#0a1335` / `#122650` (monitor bezel, vignette); screen white `#f4f2fc`. Label text reads as near-white on the gradient (seen 2.5 s); text.json gives `#7ca1f3`-`#9f9ffa` for these, which is the anti-aliased average.
- Palette, scene 3 (4.7-8.2 s): pastel lilac/periwinkle `#d3d3fc`, `#eee5fc`, `#b6ccfc`, `#e4d7fc` (shots 2-3); card near-white `#f0eeff` (sampled f240); file-name text dark indigo `#363373`; a thin purple outline on the file chip (seen 7.3-8.1 s).
- Typography: one sans family throughout, medium weight, Title Case, no all-caps except the tiny field label (OCR "KNOWLADGEBASE", 6.6 s, exact spelling not readable). Sizes as text.json box height share of frame: headline 0.087-0.093; "Design/Deploy/Scale" 0.076-0.100; "Smart" 0.126, "Agents" 0.167; "Create Agent" 0.074; file name 0.072. Headline centred above the card; side labels sit left and right of the monitor.
- Shapes: rounded rectangles everywhere. Dashboard card and pastel panel have medium radii (roughly 5% of their width, seen 0.5 s and 5.0 s); pills for the "Create Agent" header (fully rounded, 6.3 s). Four-point sparkle glyph before each label word (2.0 s).
- Light and depth: soft glow from the monitor screen onto the background (1.2-1.5 s); soft drop shadow under the white form card (6.5 s) and a wide glow around it at the end (7.9-8.0 s); the pastel panel looks like frosted glass (pink left, blue right, 5.0 s). No visible grain.

## Scene list
| Time | On screen | How it enters | How it leaves | What it explains |
|---|---|---|---|---|
| 0.00-1.10 (f0-f33) | White dashboard card (sidebar, tables) on blue; headline "The No-Code Platform" | Card rises from the lower half (f0-f12); headline fades in left to right (f3-f9) | Single-frame switch at f33 -> f34 | What the product is |
| 1.13-3.40 (f34-f102) | Chart card "Conversation Performance" filling the frame, revealed to be on a monitor; labels "Design", "Deploy", "Scale" | Fast zoom-out f34-f44, then slow; labels slide/fade in one by one (f44, f54, f63) | Labels fly outward with blur f102-f108 | Three things you do with it |
| 3.60-4.40 (f108-f131) | Same monitor, big words "Smart" (left) and "Agents" (right) | Fade in f109-f113 | Cropped off by the shrinking card f131-f146 | Names the feature |
| 4.40-5.30 (f131-f159) | Dark scene is now a rounded card on a pastel page, a frosted panel behind it | Whole scene scales down, corners round (f131-f141) | Card squashes vertically to a line f159-f177 | Bridge: old scene put away |
| 5.90-7.00 (f177-f210) | Frosted panel turns into a white form: "Create Agent" header, knowledge-base upload box | Panel shrinks and whitens f177-f184; header blurs in f185-f188; upload box grows f190-f195 | Stays | First step of using the feature |
| 7.00-8.17 (f210-f245) | File chip "Business_Info.txt, File Size: 125KB" dragged by a hand cursor into the upload box | Enters from bottom-right, tilted (f210-f222) | Drops into the box f232-f236; cursor leaves; card glows f237-f240 | Upload a file to the agent |

## Motion vocabulary
- **Card rise + headline**: dashboard card moves up from mid-frame to its rest position, f0-f12 (12 frames, 0.4 s), decelerating (OBSERVED). Headline appears word by word f3-f9 (6 frames). No overshoot seen.
- **Cut-in then pull-back**: f33 is the dashboard, f34 is the chart card at about 3x size (1 frame). Then zoom-out f34-f44 (10 frames, 0.33 s) reveals bezel and stand; a slow zoom-out continues to about f79 (shots.json: factor 0.709 over 1.367-2.633 s). Fast start, long slow tail (OBSERVED). Camera move is the whole effect.
- **Staggered side labels**: "Design" starts f44 and is solid by f51; "Deploy" starts f54, solid f57; "Scale" starts f63, solid f69. Stagger gap 9-10 frames (0.3 s). Each slides a short distance toward the monitor while fading in. Camera still zooming out underneath.
- **Chart draws itself**: the curve and its tooltip dot move left to right from f34 to about f99 (65 frames, 2.2 s) while everything else happens (dot at left 1.2 s, at top right 3.3 s).
- **Label swap**: three labels exit outward with motion blur f102-f108 (6 frames); "Smart"/"Agents" fade in f109-f113 (4-5 frames) and keep drifting apart slowly to f131.
- **Scene becomes a card**: dark scene scales down inside the frame f131-f141 (10 frames, 0.33 s), corners rounding, pastel page revealed; slow shrink continues f141-f158. The big words are clipped by the card edge as it shrinks.
- **Squash to a line**: card height goes full -> half (f165) -> thin bar (f171) -> hairline (f176) -> gone (f178). 18-19 frames, 0.6 s. Width stays the same. Even speed (OBSERVED).
- **Panel becomes form**: frosted panel shrinks and brightens f177-f184 (7 frames); header pill blurs in f185-f188 (3-4 frames); inner box scales up f190-f195.
- **Drag and drop**: chip plus cursor travel bottom-right -> upload box, f210-f225 (15 frames, 0.5 s), rotation -10 degrees -> 0 by f231; hover f225-f231; drop (chip scales down into the box) f232-f236 (4-5 frames); cursor exits right f235-f237.
- Easing notes above are OBSERVED from tile spacing, not measured.

## Pacing
- shots.json: 3 transitions in 8.17 s (about 22 per minute). Seen: 1 one-frame switch (f33/f34) and 2 morphs (4.4-4.7 s, 5.3-5.9 s).
- Shortest hold: "Smart / Agents" complete for f113-f131 (0.6 s). Longest hold: three labels complete f69-f102 (1.1 s). Final state (file dropped) visible f237-f245 (0.27 s) before the clip ends.
- Never still: lowest frame-to-frame difference in the whole clip is 0.45 grey levels (my measurement, mean absolute difference); shots.json reports an "eased zoom out" in all four shots.

## Sound
An AAC audio stream exists (ffprobe). Audio was not analysed.

## Patterns to reuse in a talking-head explainer
- **"It's inside something bigger" pull-back** -> script says "and that's just one part of...", "zoom out for a second". Start on a detail filling the frame, cut to it in 1 frame, zoom out over 10 frames fast then about 35 frames slow until the container is visible.
- **Three labels around one object** -> script lists 3 verbs or steps about one thing. Object centred; labels at left, top-right, bottom-right; each fades and slides in over 6-7 frames, 9-10 frames apart; hold about 1 s; exit all at once outward in 6 frames.
- **Two-word name split around the subject** -> naming a feature or tool ("Smart Agents"). One word each side of the centred object, fade in over 5 frames, slow outward drift, hold 0.6 s or longer.
- **Put the old scene on a card, then fold it away** -> changing topic. Scale the whole previous scene down to a rounded card in 10 frames, hold about 0.5 s, squash it to a horizontal line in 18 frames, and let the panel behind it become the next scene.
- **Cursor drags a file into a box** -> script says "you just upload your...", "give it your data". Form card centred, tilted chip with cursor arrives in 15 frames, straightens, hovers 6 frames, drops in 5 frames, card glows.
- **Chart that keeps drawing under everything** -> "showing a number growing". Let a line chart animate for about 2 s while labels come and go on top.

## Not determinable
- Font name; exact easing curves; whether the piece was made in 3D or 2D software.
- Exact text of small UI labels (dashboard rows, upload-box caption): too small to read; OCR is unreliable there.
- Whether the headline animates per letter or per word (6 frames only, 736 px wide source).
- Anything about audio or music sync.
- What follows after 8.17 s (clip ends mid-hold).
- Measurement caveats: shots.json calls f33/f34 an 18-frame "transition" (1.1-1.7 s); it is a 1-frame switch followed by a zoom. Its zoom_move with peak 15045 %/s at 1.167 s is that switch, not a real zoom. text.json was sampled at 5 fps so its t0/t1 are +/-0.2 s, and it misreads glyphs ("uDesign", "xDeploy" are the sparkle icon).
