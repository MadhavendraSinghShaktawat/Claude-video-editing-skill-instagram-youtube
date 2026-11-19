# clean-icons: icon row, light to dark

- Source: `reference/source/mg/clean-icons.mp4`. 736x414, 30 fps, 280 frames, 9.33 s of video (container 9.52 s). Values from `shots.json` and `sheets/sheet_index.json`.
- Sheets read: `sheets/sheet_001`-`004` (10 fps, all of them) and 30 fps sheets `sheets30/t0.0`, `t1.5`, `t2.5`, `t4.2`, `t5.9`, `t7.1` (frames 0-29, 45-74, 75-104, 126-155, 177-206, 213-242).
- Frame numbers below are source frames (f); time = f / 30.

## Concept in one paragraph
A short brand sting. On-screen text: "teamble", "The People Success Platform" (0.7 s), five labelled icons "Objectives, Feedback, Engagement, Performance, Learning" (1.8-3.3 s), "Now supercharged with AI" (4.6 s), "teamble ai" (6.4-6.8 s), "Unlock high performance with smarter feedback" (7.3-7.9 s). The single idea: one centred column that never changes layout. A logo, then a row of five icons that pop in one by one, then the same row is redrawn in a dark theme to say "this now has AI", then the row collapses into the new logo. The light-to-dark switch is the only big event.

## Look
- 2D layout. The light-theme icons are shaded like glossy 3D balls (highlight at top, darker rim, soft shadow, seen 2.5-4.2 s) but they only scale; no rotation seen. The dark-theme icons are flat outlined glass circles with line icons (4.8 s).
- Light palette (0-4.3 s): background near-white `#f4edfb` / `#fcfafd` (corner sample f40); a large blurred magenta-violet blob in the centre `#be73ee` (sampled f40), with lilac `#d0aff6` and pink `#e9b0eb` (shots.json shot 0); icon ball `#a034ec` (sampled f110); text white `#fcfbff` (text.json).
- Dark palette (4.6-9.3 s): background near-black `#0d0b1a` / `#0d0c18` (sampled f160), purple glow `#270f35` - `#32134a` in the centre (shots 1-2), text white; accent words in purple, text.json gives `#9610b3` for "teamble ai" (average of the white and purple parts); the "ai" and the words "with AI" / "smarter feedback" read as violet-magenta (4.8 s, 7.0 s, 8.0 s).
- Typography: lowercase logo in a bold geometric sans; taglines in a regular-to-medium sans, Sentence/Title case. Box heights as share of frame (text.json): logo 0.220 at f0 while blurred and oversized, 0.093 after settling; tagline 0.063-0.069; icon labels 0.041-0.044 (they look smaller than that on the sheets; the box includes padding); "Now supercharged with AI" 0.061; end logo 0.126; end tagline 0.046. Everything centred.
- Shapes: circles only. Five icons in a tight row, almost touching (3.5 s). Glyphs: mountain with flag, star, heart, document lines, book.
- Blur is used as a tool: the logo starts out of focus (f0-f4), the blob is always soft, the end logo is written on with a glowing blurred leading edge (f191-f203). A faint vertical banding is visible in the dark frames (7.5 s), most likely video compression.

## Scene list
| Time | On screen | How it enters | How it leaves | What it explains |
|---|---|---|---|---|
| 0.00-0.63 (f0-f19) | "teamble" on white with magenta blob | Starts huge and blurred, scales down and sharpens f0-f6 | Stays | Brand name |
| 0.67-1.50 (f20-f45) | Logo + tagline "The People Success Platform" | Tagline appears at f20 and slides up a little f20-f27 | Both move up f45-f52 | What the product is |
| 1.77-4.27 (f53-f128) | Logo, tagline, row of 5 purple icon balls with labels | Balls pop in left to right, one every 8 frames (f53-f92) | Balls shrink away left to right f129-f137 | The five product areas |
| 4.27-4.67 (f128-f140) | Background fades light -> grey -> near-black | Cross-dissolve over about 12 frames | - | "Now" moment |
| 4.67-6.33 (f140-f190) | Dark theme: "Now supercharged with AI", same five icons as outlined glass circles | Circles pop in left to right f135-f143 | Group shrinks f186-f190 and is gone at f191 | Same features, now with AI |
| 6.37-9.33 (f191-f280) | "teamble ai" then the line "Unlock high performance with smarter feedback" | Logo written on left to right f191-f204; subline revealed left to right f219-f236 | Clip ends on it | New product name and promise |

## Motion vocabulary
- **Focus-pull logo**: logo scales from about 65% of frame width to about 30% and goes from blurred to sharp, f0-f6 (6 frames, 0.2 s); slow residual shrink to about f18 (shots.json: zoom-out factor 0.312 over 0.033-1.167 s). Decelerating (OBSERVED).
- **Tagline in**: absent at f19, present at f20; slides up from y 0.63 to 0.51 over f20-f27 (text.json boxes; 7 frames).
- **Make room**: logo + tagline move up (logo y 0.43 -> 0.22, text.json) f45-f52 (7 frames).
- **Icon pop with overshoot, staggered**: each ball starts as a dot, grows for 3-4 frames to larger than its final size, then settles while the next one arrives. Start frames: f53, f61, f69, f77, f85, so the stagger gap is 8 frames (0.27 s). First ball: dot f53, full with glyph f56, biggest f57-f59, settled about f62. The newest ball is always the largest in the row (f66, f74, f82, f90). The row re-centres as each ball is added (existing balls shift left). Label fades in under each ball 3-5 frames after it lands. All five settled at about f99. Camera: slow drift only.
- **Theme switch**: f128-f140 (12 frames, 0.4 s). Purple balls shrink to dots left to right from f129 (one per about 2 frames); background passes through grey at f132-f135; "teamble" fades out, tagline is replaced by "Now supercharged with AI" at f136; outlined circles pop in left to right f135-f143 (about 2 frames apart) with a small overshoot on the last ones (f138-f140).
- **Collapse to logo**: icon group and headline scale down f186-f190 (shots.json zoom factor 0.784 over 5.867-6.367 s), vanish between f190 and f191.
- **Glow write-on**: "teamble ai" appears left to right f191-f204 (13 frames, 0.43 s). The leading edge is a blurred magenta smear; letters behind it turn crisp white; "ai" stays purple.
- **Subline reveal**: words fade in left to right f219-f236 (17 frames, 0.57 s), last two words tinted purple.
- Easing notes are OBSERVED from tile spacing, not measured.

## Pacing
- shots.json: 2 cuts in 9.33 s (about 13 per minute). Seen: no hard cut at all; one 12-frame theme dissolve (4.27-4.67 s) and one collapse-then-write-on (6.2-6.8 s).
- Holds: logo alone 0.45 s (f6-f19); logo + tagline 0.6 s (f27-f45); five light icons complete f99-f128 (about 1.0 s); dark row complete f143-f186 (1.4 s); final lockup f236-f280 (1.5 s).
- Stillness: background blob and a slow zoom keep every frame changing until the end. My frame-difference measure finds near-still runs only from f230 onward (runs of 0.17-0.37 s, broken by tiny changes). Median difference is low (0.58 grey levels), so the motion is gentle.

## Sound
An AAC audio stream exists (ffprobe). Audio was not analysed.

## Patterns to reuse in a talking-head explainer
- **Staggered icon row** -> speaker lists 3-5 parts, features or options. One circle per item in a centred row; each pops from a dot with a small overshoot in 4 frames, 8 frames apart; label fades in under it 3-5 frames later; re-centre the row as it grows; hold 1 s after the last one.
- **Same layout, new theme** -> script says "now with...", "but here's the upgrade", "before / after". Keep positions fixed; shrink the old items away left to right (2 frames apart), dissolve the background from light to dark in 12 frames, pop restyled items in the same slots, swap the headline.
- **Focus-pull title** -> opening a section or naming a tool. Start the word oversized and blurred, scale down and sharpen in 6 frames, then drift slowly; add a one-line descriptor 0.4-0.5 s later sliding up a few pixels.
- **Glow write-on for the new name** -> the payoff name or final answer. Reveal left to right in about 13 frames with a blurred coloured leading edge; colour only the changed part ("ai").
- **Accent only the key words** -> any caption line. White text, with just the 1-2 words that carry the point in the accent colour ("with AI", "smarter feedback").

## Not determinable
- Font names; exact easing curves; the software used.
- Whether the icon balls are 3D renders or shaded 2D art.
- Exact colour of small text (anti-aliasing at 736 px makes text.json colours averages, e.g. label text reported as pink).
- Whether the subline animates per word or per letter (source too small).
- Audio, music hits, or whether pops are synced to sound.
- Measurement caveats: shots.json marks a "hard" cut at 4.467 s (f134); the 30 fps sheet shows a 12-frame dissolve there, not a cut. shots.json reports a face in shot 1 (face_share 0.25); there is no face anywhere in the clip. text.json merges two labels into one track ("Engagement Performance", grew=True) and drops spaces in the last line; its 5 fps sampling makes t0/t1 accurate to +/-0.2 s only.
