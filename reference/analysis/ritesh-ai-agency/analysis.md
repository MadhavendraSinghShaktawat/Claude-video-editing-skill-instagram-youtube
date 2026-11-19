# Edit analysis: ritesh-ai-agency

Source: reference/source/ritesh-ai-agency.mp4 ("How To Start an AI Marketing Agency with Claude in 30 Days", Ritesh Verma, 971.6 s, 3840x2160, 59.94 fps file holding 29.97 fps content, 52.6% duplicate frames).
Evidence: timeline.md, summary.json, shots.json, text.json, audio.json, words.json; shots/shots_001-017.jpg; overview/ov_001-005.jpg (440-760 s at 0.5 fps); dense sheets in dense/ (30 fps unless noted): hook_001-005 (0-12 s), t33 (33.2-38.0), t44 (44.4-45.6), t49 (49.1-51.5), t61 (61.1-63.5), t101 (101.4-102.95), t120 (120.8-121.5), t132 (132.4-133.0), t136 (135.9-138.1), d138_001-003 (138.8-160 at 10 fps), t165 (164.9-166.5), t190 (190.2-191.5), t288 (288.3-288.9), t384 (384.4-385.0), t773 (773.4-775.8), t837 (836.8-838.4), d859_001 (858.9-866 at 10 fps). All times are seconds from the start of the file. "By eye" means read from frames; everything else is from the measurement files.

## 1. Facts

| Item | Value | Source |
|---|---|---|
| Length | 971.6 s (16:12) | summary.json |
| Detected cuts | 178 = 11.0 per min | summary.json |
| Cuts by kind | hard 106 (6.5/min), jump 29 (1.8/min), pop 24 (1.5/min), transition 11 (0.7/min), punch 8 (0.5/min) | summary.json |
| Real edits vs screen changes | About 40 of the 53 jump/pop events fall inside screen recordings (296-354, 387-460, 483-703 s) and are windows changing, not edits (by eye) | shot sheets 6-12 |
| Shot length | median 3.52 s, p10 0.79 s, p90 12.1 s, max 33.4 s (583.9-617.3 s, screen recording) | summary.json |
| Longest gap between hard cuts | 61.1 s starting 576.1 s; 56.2 s starting 482.8 s (both screen recording); 41.3 s starting 911.6 s (speaker, jump cuts only) | shots.json |
| Picture share as measured | face 83.9%, flat graphic 15.5%, pip 0.4%, no face 0.3% | summary.json (wrong, see 15) |
| Picture share by eye (every shot classified from the sheets) | screen recording with round speaker inset 36.0% (349.8 s, 49 detected shots); speaker full frame 27.7% (269.6 s, 58 shots); speaker card beside a graphic 11.6% (112.7 s, 18); full-screen diagram 10.6% (102.6 s, 11); b-roll of the creator 4.2% (40.6 s, 14); chapter title cards 4.0% (38.5 s, 10); side bullet panel + speaker 2.8% (27.5 s, 5); screenshots / clips full frame 2.8% (26.7 s, 12); big-text page 0.4% (3.7 s, 2) | shots.json durations + sheets |
| Speech rate | 233.5 wpm overall, 267.6 wpm while speaking, 3782 words; per-30 s range 186-274 (last partial window 96) | audio.json |
| Pauses (voice stem) | 333 = 20.6/min, 8% of runtime, median 0.20 s, p75 0.28 s, p90 0.36 s, max 1.6 s; 5 over 0.5 s, 2 over 1 s, 0 over 2 s | audio.json |
| Speech runs between pauses | median 0.67 s, p90 2.04 s, max 4.7 s | audio.json |
| Loudness | -15.7 LUFS integrated, LRA 2.8 LU, true peak -0.2 dBTP | audio.json |
| Music | Present only in bed_on_spans 5-15 s and 25-35 s; first 30 s averages -39.6 dB relative to voice; every later 30 s window is -48.6 to -52.7 dB (inaudible) | audio.json |
| Sound events | 31 candidates, 28 strong, all between 4.24 and 35.47 s; 1.7 strong per min averaged over the video, 0 per min after 36 s | audio.json |
| On-screen text | 154 big tracks = 9.5/min; median 2 words, on screen 3.1 s, 4.8% of frame height; 44% repeat spoken words | summary.json |

## 2. Script structure

| Start | Beat | What is said (1 line) | How the edit marks it |
|---|---|---|---|
| 0.0 | Hook claim | "Building a one person business with Claude AI is the biggest opportunity heading to 2027" | Speaker full frame, two caption blocks type on from 0.10 s |
| 4.3 | Problem | "but the problem is 99% ... are selling AI automations which businesses are no longer buying" | Punch cut 4.30, speaker shrinks into the card 4.37-5.33, icon grid |
| 10.1 | Pain | "And that's probably why you can't get clients anymore" | Full-screen big-text page 10.07-11.90 |
| 11.9 | Solution tease | "But there is an AI business that's so simple to start and sell..." | Card + orbit diagram |
| 18.0 | Credibility | "land clients bi-weekly each paying minimum $1400 a month" | Speaker full frame, no graphic, music pulse audible |
| 25.5 | Promise | "So in this video, I'm going to show you exactly..." | Card + 7-line list "By the end of this video" |
| 35.4 | Proof | "it's helped my client ... make $25,000 a month" | White flash 35.27-35.40, then 4 proof items (38.0, 42.5, 44.7, 46.4) |
| 49.2 | 1/10 What is an AI marketing agency | definition + three services | Title card |
| 106.8 | 2/10 Why this opportunity is so lucrative | creators boom, what you build | Title card |
| 173.9 | 3/10 Pick your target customer | three customer types, his pick | Title card |
| 199.0 | 4/10 Pick your offer | content / ads / AEO | Title card |
| 252.0 | 5/10 Build a content strategy with claude | example client, live prompt demo 296.6-354.0 | Title card |
| 365.3 | 6/10 Learn to edit videos with claude | record, let Claude edit, demo 387.8-459.8 | Title card |
| 459.8 | 7/10 Editing reels in instagram edits | connect the Edits app, demo 482.9-703.1, trial reels | Title card |
| 749.5 | 8/10 Send the strategy and sample videos | outreach message | Title card |
| 809.2 | 9/10 Run the sales call | find the pain, match the offer, upsell | Title card |
| 889.3 | 10/10 Pricing your offers | three prices, start cheap | Title card |
| 911.6 | Wrap-up | "nobody's buying AI anymore, they're buying results" | Speaker full frame, slow push, jump cuts only |
| 948.9 | CTA | "I invite you to work with me one on one..." | 6-clip montage of client calls 952.9-960.9, big-text page 960.9-962.7 |
| 962.7 | End / next video | "I recommend watching this video where..." | Speaker full frame to the last frame (971.5); no end-screen graphic is visible in the sampled frames |

Section changes are always marked the same way: a hard cut to a white title card with "N/10" and the chapter name, placed on the first words of the bridging sentence ("So why is opportunity so lucrative?" 106.8; "Now once you've figured out your customer..." 199.0). No sound marks any section change.

## 3. The rough cut

- Tightness: median pause 0.20 s, p90 0.36 s, pauses are 8% of the runtime, 233.5 wpm overall. Word gaps: median 0.24 s, p90 0.38 s.
- The pauses over 0.45 s are all inside screen recordings: 323.3 (0.80 s, waiting on Claude), 339.8 (0.46), 402.2 (0.65) and 403.6 (1.27, raw clip playing), 456.8 (1.60, end of the sample video), 573.6 (0.77), 702.8 (0.47, just before cutting back to the speaker). In talking-head sections no pause above 0.45 s survives.
- Cut position against speech: 54% of same-picture cuts and 47% of picture changes fall between words; 41% and 45% fall inside a measured voice pause (chance would be 11%). 30% / 36% land right after a sentence end.
- Jump cuts are mostly left visible. Among the 58 full-frame speaker shots, 20 start on a cut from another full-frame speaker shot with no scale change (measured 0.993-1.013): e.g. 123.22, 126.61, 191.34, 195.71, 238.22, 474.06, 763.91, 765.47, 770.64, 828.81, 919.70, 948.87. Others in this group are labelled "pop" but are the same thing by eye (276.59, 375.48, 467.25, 790.44, 812.10, 922.49, 934.02, 946.61).
- Jump cuts hidden by a punch: 6 on the speaker. 101.67 (x1.168 in, on "So here's a reframe"), 121.03 (x0.813 out, "But because of this dream"), 384.60 (x0.885 out, "And let Claude code edit them"), 288.57 (x0.98, barely visible), 4.30 (x0.958) and 836.97 (x0.953), the last two leading straight into the card shrink.
- Jump cuts hidden by a graphic or b-roll: most sentence joins sit under a layout change. Examples: 61.16 (speaker to list diagram), 132.62 (speaker to b-roll), 138.87 (speaker to flowchart), 859.06 (speaker to card + price table).
- Longest unbroken speaker stretches (no cut of any kind): 13.8 s at 238.2-252.0, 12.8 s at 736.7-749.5, 12.6 s at 934.0-946.6, 11.5 s at 922.5-934.0, 11.1 s at 703.1-714.3.

## 4. Camera on the speaker

Framing (58 full-frame shots, shots.json): face height 33-37% of frame height in the standard framing (examples 0.347 at 0 s, 0.345 at 55 s, 0.358 at 737 s); face centre x 0.45-0.51, y 0.35-0.41. The speaker is close to centre, 1-5% left of it, with the microphone in the top-left corner and a lamp at the left edge. The summary's x 0.57 is pulled right by the card shots (card face at x 0.79-0.83).

| Move | Count (of 58) / time | Measured size | Example times | Trigger |
|---|---|---|---|---|
| Static (drift under 1%) | 13 shots, 35.6 s | zoom 0.99-1.01 | 118.8, 123.2, 191.3, 203.1, 361.0, 724.8, 825.8, 887.4 | none |
| Slow push in | 18 shots, 102.7 s | +1.2% to +5.4% over the shot, 0.2-0.8 %/s (median 0.5 %/s) | 55.1 (+4.7% in 6.1 s), 703.1 (+2.6% in 11.1 s), 911.6 (+3.4% in 8.1 s), 922.5 (+5.4% in 11.5 s), 962.7 (+4.9% in 8.8 s) | long uncut explanations and the closing argument; confirmed by eye at 703.3 vs 714.1 and 911.8 vs 952.7 |
| Slow pull out | 12 shots, 77.6 s | -1.3% to -6.6%, 0.3-0.7 %/s | 126.6 (-4.3% in 6.0 s), 238.2 (-3.8% in 13.8 s), 736.7 (-6.6% in 12.8 s), 839.3 (-3.6% in 8.3 s), 853.2, 875.5 | same kind of line as the push; confirmed by eye at 736.8 vs 749.3 |
| Stepped push across cuts | 911.6-952.9 | face height 0.368 -> 0.364 -> 0.374 -> 0.397 -> 0.425 -> 0.410 across shots at 911.6, 919.7, 922.5, 934.0, 946.6, 948.9 (about +15% in 35 s) | 934.02, 946.61 | each jump cut in the wrap-up lands slightly tighter while a slow push runs inside each shot |
| Punch in (instant) | 1 | x1.168, face 0.346 -> 0.44, 1 frame | 101.67 | "So here's a reframe" |
| Tight framing after a graphic | 1 | face 0.449 (about 1.3x the standard) | 118.77 | "I mean, that is kind of true" (an aside) |
| Punch out (instant) | 3 clear | x0.813, x0.885, x0.98 | 121.03, 384.60, 288.57 | first words of the next sentence ("But because...", "And let Claude...", "So the first offer...") |
| Eased zoom out after a flash | 1 | starts about 1.25x tight and over-exposed, eases to standard: factor 0.795 over 0.87 s (35.52-36.4) | 35.43 | "Now to prove that this AI business model doesn't just work for me" |
| Small eased zoom steps | 5 flagged | factor 0.964-1.041 in 0.15-0.30 s | 97.61, 197.38, 235.97, 764.78, 287.44 | by eye 97.5 vs 97.9 is a jump cut, so these are probably cuts, not moves |
| Sideways slide when the panel enters/leaves | 5 | footage shifts right by about 15-17% of frame width in 0.7-0.9 s | 165.03, 190.37, 277.81, 287.3 | start or end of a bullet list |

How often static: 13 of 58 full-frame shots (35.6 of 269.6 s = 13% of full-frame time). The summary's "static 46%" includes the card and inset shots, which never move.

## 5. Layouts

| Layout | Share / count | What it looks like | Example times |
|---|---|---|---|
| A. Speaker full frame | 27.7%, 58 shots | Dark warm room, white T-shirt, mic top-left, face 33-37% high near centre. Captions only in the first 4.3 s | 18.0-25.5, 55.1-61.2, 911.6-952.9 |
| B. Speaker card + graphic | 11.6%, 18 shots | White page with a soft vignette (#fefefe centre to #d0d0d0 corners). Portrait speaker card with rounded corners and a thin dark edge at x 0.685-0.948, y 0.141-0.852 (26.3% x 71.1% of the frame, about 2:3). Face in the card is 26-27% of frame height at x 0.79-0.83. Graphic occupies the left 65% | 4.7-10.0, 11.9-18.0, 25.5-35.4, 38.0-46.4, 102.8-106.8, 112.3-118.8, 176.5-184.8, 265.8-269.1, 728.6-736.7, 752.8-760.7, 837.2-839.3, 859.1-875.5, 892.9-911.6 |
| C. Side bullet panel | 2.8%, 5 shots | White panel covers the left 50% of the frame; the speaker footage is pushed right so the face sits at x 0.68-0.72 at full size (33-34%) | 108.5-112.3, 165.0-173.9, 184.8-191.1, 277.8-288.0 |
| D. Full-screen diagram | 10.6%, 11 shots | Page is #ffffff at the top fading to #bdbdbd at the bottom (vertical gradient, no vignette). Thin-line wireframe boxes, pills, circles. No speaker | 61.2-91.9, 138.9-158.9, 206.4-234.6, 354.0-361.0, 714.3-724.8, 881.2-887.4 |
| E. Chapter title card | 4.0%, 10 | Vignette page, "N/10" above a black bar with white chapter name | 49.2, 106.8, 173.9, 199.0, 252.0, 365.3, 459.8, 749.5, 809.2, 889.3 |
| F. Big-text page | 0.4%, 2 | Vignette page, two centred lines, no speaker | 10.07-11.90, 960.9-962.7 |
| G. Screen recording + round inset | 36.0%, 3 blocks | Recording window at x 0.06-0.94, y 0.06-0.94 (88% scale) on the gradient page; round speaker inset (different camera, light room) bottom-right, about 20% of frame height, face 13-15% | 296.6-354.0, 387.8-459.8, 482.9-703.1 |
| H. B-roll of the creator | 4.2%, 14 detected shots in 8 inserts | Full-frame clips of him in other places (cafe, street, desk, sofa) | 132.6-137.7, 158.9-163.2, 376.7-378.1, 380.7-383.1, 773.6-776.0, 800.0-809.2, 815.6-825.8, 847.6-853.2 |
| I. Screenshot / clip full frame | 2.8%, 12 | Testimonial video, logo, video-call split screen, Instagram profile, doc text, website, call recordings | 46.4-49.2, 257.7-260.2, 262.6-265.8, 269.1-273.5, 378.1-380.7, 476.2-479.4, 952.9-960.9 |
| J. Card over a screen window | 1 use | Layout B with a dark Claude window on the page behind the card | 776.0-783.6 |

## 6. Motion-graphics catalogue

Common style (by eye + sampled pixels): flat 2D, black/grey on white, one accent red (#bb201f on the icon grid at 8.0 s; dark red #4e1212 as a card outline at 905 s). One sans-serif family throughout; the heavy italic cut is used for emphasis lines. Icons are solid black silhouettes (person, briefcase person, film strip) or thin-line outlines (database, magnifier, document, play). No 3D, no drop shadows except on screenshots.

**6.1 Chapter title card** (10 uses). Vignette page. "N/10" black, 10.2-10.6% of frame height, centred at y 0.39. Below it a black bar (#090909) with the chapter name in white (#e6e6e6-#f9f9f9), 6.5-8.2% high, at y 0.50. Dense sheet 49.1-51.5: hard cut to blank page at 49.20; "1/10" fades in 49.47-49.60; a thin cursor line appears at 49.70 and widens into the bar until about 50.2; words fade in left to right 50.23-51.07. Build about 1.9 s. Total time on screen 1.75-5.87 s (median about 3.9 s). Leaves by hard cut. Triggers: "So what is this new AI business model..." (49.3), "So why is opportunity so lucrative?" (106.9), "here's how to properly conduct the sales call" (809.2). The spoken sentence is a bridge, not a reading of the title; where the title words are spoken the text is up to 2.9 s early (252.0) or 1.7 s late (49.2).

**6.2 Hook captions on the footage** (0.10-4.27). See section 11.

**6.3 Icon grid** (4.37-10.03). Card layout. Ten solid person icons in 2 rows of 5 pop in one at a time, each fading from grey to black in 2-3 frames, one about every 0.13 s from 4.53 to 5.93 (spoken "99" at 5.06). At 6.03 a small round badge appears beside every icon. At 7.03-7.50 nine icons turn dark red then bright red; one stays black ("AI automations" spoken 7.16-7.50). At 7.93-8.90 a two-line caption types on above ("99% selling AI which business / are no longer buying"; spoken 8.20-9.42). Leaves 9.57-10.00: everything slides down with heavy motion blur; card removed by cut at 10.07.

**6.4 Big-text page** (10.07-11.90; 960.93-962.71). Vignette page, no speaker. Line 1 regular weight 5.2-7.2%; line 2 bold italic 6.9% (first use) / 11.7% (second use), dark grey #2d2d2d-#2e2e2e, centred at y 0.45-0.53. Words fade in one at a time, new word in grey then dark: 10.10 "and" to 11.00 "anymore" (0.9 s for 9 words; spoken 10.14-11.50). Holds 0.9 s complete. Hard cut in and out. Triggers: "And that's probably why you can't get clients anymore" (10.14); "if you don't get clients I don't get paid" (961.1).

**6.5 Orbit diagram** (11.93-17.98). Card layout. A small round icon labelled "AI Business" (3.2%) appears first, then three thin concentric circles draw outward, then small person icons appear on the rings (8 motion events over 6 s). Trigger: "But there is an AI business that's so simple to start and sell..." Hard cut out.

**6.6 Numbered text list beside the card** (25.49-35.40). Heading "By the end of this video" 8.3%, bold, left-aligned at x 0.10. Seven numbered lines at 4.8-6.7% (OCR; by eye about 2.5% each), each typed on as its item is spoken: line 2 lags its words by 0.09 s, line 3 leads by 0.10 s; lines 4-7 (Strategy, Delivery, Outreach, Sales) appear at about 33.2, 33.5, 33.7, 33.95 against spoken 33.12, 33.68, 34.18, 34.64, so the last items run up to 0.7 s ahead. The heading leads its words by 4.57 s because it is a paraphrase ("So in this video" is said; "By the end of this video" is shown).

**6.7 Proof cards** (38.02-46.36). Card layout. A photo or screenshot with rounded corners and a soft shadow, plus a bold italic caption: "Aman / $25,000/mo" (7.3% and 8.8%), "1k/mo -> $20k/mo in 90 days" (6.1%). The image scales up from small and blurred (42.54-43.58). Change between two proofs: blur + fade cross-dissolve, 44.53-44.90 (11 frames), with the caption staying. One proof per sentence, 1.7-4.5 s each.

**6.8 Numbered list diagram** (61.16-75.17 and 82.10-84.47). Gradient page. Heading 6.1% grey #484848 centred at y 0.27. Three small numbered circles stacked at x 0.33; all three are visible as faint ghosts from the first frame. Dense sheet 61.1-63.5: cut at 61.17; heading fades in 61.40-61.60 (spoken "three things" 61.60-61.82); circle 1 fills black and "Content" appears 63.13-63.23 (spoken "content" 63.24). A small grey sub-label ("ideas, scripts, editing, tracking", 4.0%) follows. When item 2 becomes active, item 1 dims to grey. Trigger: "So you do three things with clients. One is content..."

**6.9 Connector pills** (75.17-82.10). Gradient page. Black pill "Claude" (white text 6.3%), a line draws to an outlined pill "Facebook Ads" (5.2%), then three small outlined pills "Targeting / Location / Budgeting" (4.2-4.8%) appear on their words (lags +0.39, -0.11, +0.31 s). Enters and leaves as an instant page swap. Trigger: "But now Claude can connect directly with Facebook ads...".

**6.10 Mock chat window** (84.47-91.86). Gradient page; white rounded card with a thin border; header "ChatGPT / Claude"; black bubble "Who's the best barber in town?"; rows 1-3 with "Your barber shop" in row 1; black tag "Top 3". Elements appear in spoken order over about 6 s. Trigger: "when someone asks ChatGPT or Claude, who's the best barber in town...".

**6.11 Word-reveal behind an icon** (102.79-106.79). Card layout. A black person icon at 102.80; a small "AI Agency" label; then the word "Marketing" in red, about 20% of frame height, wipes in behind the icon and a grey block appears under it; small round icons orbit at the end. Trigger: "You're not an AI agency. You're a marketing agency with an unfair AI engine." Cut-in is on "You're" (102.92), 0.12 s early.

**6.12 Side bullet panel** (4 uses, see layout C). Heading bold 5.3-9.1% (#1b1b1b-#3f3e3e), bullets 4.7-6.4% grey-to-black, left-aligned at x 0.05. Dense sheet 164.9-166.5: panel edge enters at 165.03 and reaches half-frame by about 166.0 (0.9 s) while the speaker footage slides right; heading words type on during the slide (165.3-165.7); bullet 1 at 165.77, bullet 2 words 166.10-166.47 (spoken "local business owners" 165.88-166.38). Exit, dense sheet 190.2-191.5: 190.37-191.10 (0.7 s), text motion-blurred, speaker slides back to centre; a jump cut follows at 191.33. Triggers are lists of 3-4 parallel items: "moms, dads, brothers, sisters" (108.5), "local business owners, every single AI startup founder..., any coach" (165.2), "get him more views... more clients" (277.8).

**6.13 Thumbnails with a dashed line** (112.30-118.77). Card layout. "Make content" at left, a dashed line draws to "Brand/money" (4.1-4.7%); three portrait video thumbnails fade in under it. Trigger: "everybody's trying to create content because they've been promised...".

**6.14 Flowchart with a moving camera** (138.87-158.90, dense sheet at 10 fps). Gradient page. Heading "What you build with Claude" 5.4% (#484848) fades in 139.2-139.5. Four rounded boxes in a row with a thin-line icon, a title (4.4-4.6%) and a two-line sub-label; arrows between them. All four boxes are visible as faint ghosts at the cut (138.9).
- Box 1 "2 databases" activates 139.8 (spoken "two databases" 139.90); sub-lines at 141.1 and 142.7.
- Box 2 "Research agent" 144.3 (spoken "research" 144.38); box 1 dims to grey; arrow draws 144.4-144.7.
- Box 3 "Scripting agent" 147.0 (spoken "scripting" 147.18).
- Box 4 "Video editing" 151.1 (spoken "video editing" 153.26, so 2.1 s early; the line about editing starts at 150.6).
- Camera: from 140.3 the page scales up about 1.15x and pans right so the active box stays near centre; box 1 leaves the left edge by 148.4. At 155.5-156.4 it zooms back out to show all four boxes at full contrast.
- Pay-off line "Clients pay $5K $10K $15K" (4.0%, amounts bold) types on 155.5-156.8 (spoken "pay five, 10k, 15k" 155.46-156.64).
- Hard cut out at 158.9. Total 20.05 s.

**6.15 Tree diagram** (176.49-184.80). Card layout. Person icon at top, three curved lines draw down to three black icon tiles (local business, creator, AI founder), each on its word.

**6.16 Three offer cards** (203.14-234.55). Gradient page. Three tall rounded cards; the active card has a dark outline and black text, the others are pale grey. Small tag "Offer 1/2/3" (3.7-3.9%), title (4.5-5.6%), 3-5 lines (3.0-5.1%) added one per spoken word ("Ideas / Scripts / Editing / Posting / Tracking" lags -0.19 to +0.59 s), and a bold bottom line ("Client just hit record", "$2K / month"). The view shifts slightly when the active card changes (215.53 and 229.55, measured x0.971). 31.4 s on screen, the longest single graphic.

**6.17 Document-to-person diagram** (354.00-361.01). Gradient page. Outlined document icon with "Content strategy" (4.8%, lag +0.04 s), an arrow draws right, an outlined person circle with a black "Ty" tag and "Your ideal customer" (3.5%).

**6.18 Trial-reels diagram** (714.28-724.79). Heading 6.5% (lag +0.06 s). Two phone outlines with play triangles ("New angle" 716.0, "New hook" 718.0), an arrow labelled "Instagram tests" (720.0), a grid of outlined people "Not following yet" (722-724).

**6.19 Branch diagram** (728.63-736.65). Card layout. "You" icon, a bracket line to two pills ("Hook", "Unique style", 4.4-4.6%), lines converge on a small bar-chart icon "Blow up your content" (3.4-3.5%).

**6.20 People and samples** (752.77-760.66). Card layout. Two large black person icons labelled "Ty" and "You" (8.0%), a small 4-icon cluster between them, two film-strip icons "Sample 1 / Sample 2" (4.1%) above, and a dark red cursor arrow that moves to a sample.

**6.21 Strike-through pills** (837.03-839.30, dense sheet). Card layout. Pill "AEO" above a person icon; a red line strikes it through 837.60-838.30 ("don't try to sell them on AEO", AEO spoken 837.82); pill "Ads" appears 838.5-839.3 (spoken 838.76).

**6.22 Price table** (859.06-875.49, dense sheet at 10 fps). Card layout. Rows at 9-10% of frame height, dark #272727: "Retainer ....... $1,000". Page is empty for 1.7 s after the cut; "Retainer" fades in 860.8 (spoken 860.32, +0.5 s); dotted leader types dot by dot 861.2-862.2; "$1,000" fades in 861.8. "Ads" 863.8 (spoken 864.00); "$2,000" 864.8. "Content" 865.8 (spoken 866.14). A rule and "+" then "Total $5,000" by about 870 (spoken "five thousand" 868.66).

**6.23 Triangle diagram** (881.20-887.37). Gradient page. Three outlined circles (AEO top, Content and Ads below, 3.9-4.1%), centre label "AI marketing agency" (4.9%), lines join the circles. Ghost circles first, darkening as named (lags +0.3 to +1.3 s).

**6.24 Price cards** (892.88-911.61). Card layout. Three dark cards (#1a1a1a) with a dark red outline, white icon, title (4.1-4.8%), large white price (8.3-8.7%), small description (3.3%). Each card fades in as a pale grey placeholder, then turns dark when its offer is named (892.9, 898.9, 902.9). The middle price is bold "$3,000 / +$1,000 a month to manage it".

**6.25 Screenshot with hand-drawn arrow** (265.75-269.12). Card layout. Dark YouTube channel header card; bold italic "17,000 subscribers" (5.7%) with a curved arrow that draws on from the right.

## 7. B-roll

All b-roll is footage of the creator himself in other locations and clothes; no stock footage was seen. Every insert enters and leaves by hard cut with no sound.

| Time | Length | What it shows | Line it covers |
|---|---|---|---|
| 132.62-136.14 | 3.5 s | Cafe table, he lifts and sips a coffee | "But most of them, because they're beginners and they're just trying out for the first time" |
| 136.14-137.74 | 1.6 s | Low angle, him looking up between office towers | "they don't really know how to run the show well" |
| 158.93-161.65 | 2.7 s | At a desk with laptop and curved monitor, teal grade | "And you can even upcharge them a monthly retainer to coach them" |
| 161.65-163.18 | 1.5 s | Same idea, different desk, warm/purple light | "on how to create better content" |
| 376.66-378.11 | 1.45 s | Sitting down on a sofa in front of the camera | "First record a few videos" |
| 380.68-383.07 | 2.4 s | Talking to camera outdoors with a laptop | "film them on your phone, and they don't need to be perfect" |
| 773.59-775.98 | 2.4 s | Typing on a laptop in a cafe at night | "want to send a personalized outreach to the client" |
| 800.03-809.21 | 9.2 s | Side view at a desk, on a video call | "book a call with you... the actual sales call" |
| 815.60-825.77 | 10.2 s | Same desk, arms folded, listening to a call | "let them talk about whether they're struggling..." |
| 847.58-849.92 | 2.3 s | Side view at a bright desk, gesturing at a screen | "guess what, I can run ads for you" |
| 849.92-853.22 | 3.3 s | Same desk, from behind | "I can create content for you and get you even more leads" |

Pattern: 8 inserts of 1-2 clips; clip length 1.45-10.2 s (median about 2.4 s). The clip shows the action being described (recording, typing outreach, being on a sales call) or simply breaks up a speaker-only stretch (132.6). Sections 9/10 uses b-roll where earlier sections use diagrams. Each insert cuts in on the first word of the clause it covers (132.62 on "But", 773.59 on "want", 800.03 on "know").

The CTA montage (952.90-960.93) is a separate case: 6 screen recordings of client calls, 0.68-2.20 s each (2.20, 1.67, 0.80, 1.07, 1.60, 0.68), hard cuts, under "I will personally guide you on building, launching and scaling...".

## 8. Screen-recording treatment

- Blocks: 296.58-354.00 (57.4 s), 387.75-459.79 (72.0 s), 482.85-703.14 (220.3 s) = 36% of the video. A fourth short use at 775.98-783.60 puts a screen window behind the speaker card.
- Framing: the recording is not full-bleed. It sits at x 0.06-0.94, y 0.06-0.94 on the white-to-grey gradient page with a soft shadow.
- Speaker inset: a circle about 20% of frame height at the bottom-right corner of the window (centre about x 0.86, y 0.80), overlapping the window edge; different camera and a bright room. It moves to the top-right (y 0.21) for 583.93-617.32 while the terminal on the right is in use, then returns. During 459.1-459.8 the inset is a small rectangle instead of a circle.
- Zooms and highlights: none added. The measured "eased zoom" values in these blocks (x1.77 at 400.3, x0.62 at 407.5, x0.45 at 448.4) are windows opening and video playing inside the window. No cursor highlight, callout, box or arrow was seen on any sheet.
- Cuts inside the blocks: some hard time-skips (e.g. 413.75 back to the project page; 428.6 from the prompt to the finished video, "So Claude just finished"; 617.3 "All right, Claude has edited our reel"). Most other detected cuts are app or window changes in the live recording.
- Waiting: not sped up visibly; it is cut out. At 607-617 he says "I'll literally leave this on and let it do its magic" and the next shot (617.32) is the finished result.
- Pace: detected shots median much longer than elsewhere; the longest are 33.4 s (583.9-617.3), 26.6 s (512.5-539.1), 24.4 s (678.8-703.1), 22.6 s (551.6-574.2). The speaker narrates continuously; the only pauses over 0.5 s in the whole video are here.
- The demo output (the black animated sample video, 433.4-459.0) is played inside the same window with the inset still on top, not cut in full frame.
- Text is small and unreadable at normal size (OCR found 20-220 small lines per shot); nothing is enlarged for the viewer.

## 9. Script -> picture table

Lead/lag: negative = picture first. Values from dense sheets are marked (d); others are from timeline.md (about ±0.3 s).

| Time | Spoken line | What the picture does | Job | Lead / lag |
|---|---|---|---|---|
| 0.0 | "Building a one person business with Claude AI" | Speaker full frame; left caption block types on 0.10-0.80 | State the topic in text at once | first word +0.10 s; block finishes 0.7 s before "AI" is said (d) |
| 1.6 | "is the biggest opportunity heading to 2027" | Right caption block types on 1.83-2.63 | Second half of the claim | "is" +0.2 s; "2027" -0.9 s (d) |
| 4.4 | "but the problem" | Punch cut 4.30, captions gone, speaker starts shrinking 4.37 | Turn from claim to problem | -0.08 s (d) |
| 5.1 | "is 99%..." | Card settles 5.33; person icons pop one per 0.13 s | Make "99%" countable | icons start 0.5 s before "99" (d) |
| 7.2 | "selling AI automations" | 9 of 10 icons turn red 7.03-7.50 | Mark the crowd as wrong | -0.13 s (d) |
| 8.2 | "which businesses are no longer buying" | Caption types above the icons 7.93-8.90 | Repeat the claim in text | -0.27 s start, ends 0.5 s early (d) |
| 10.1 | "And that's probably why you can't get clients anymore" | Full-screen text page types on | Land the pain | -0.07 s start; done 0.5 s early (d) |
| 12.0 | "But there is an AI business that's so simple..." | Cut to card + orbit diagram | Tease the solution | -0.09 s |
| 18.0 | "In fact, it's how I've been able to land clients bi-weekly..." | Speaker full frame, no graphic, 7.5 s | Personal credibility, eye contact | cut +0.01 s |
| 26.1 | "I'm going to show you exactly what this AI business model is" | Card + heading, list line 1 | Promise | heading -0.5 s |
| 28.3 | "how to run it end to end with Claude" | List line 2 types on | Promise item | +0.09 s |
| 33.1 | "strategy, delivery, outreach, sales" | Lines 4-7 appear 33.2-33.95 | Rapid list | 0 to -0.7 s (d) |
| 35.4 | "all of it. Now to prove..." | White flash 35.27-35.40; over-exposed tight speaker eases out to 36.4 | Reset attention before proof | flash 0.2 s before "Now" (d) |
| 38.0 | "it's helped my client ... make $25,000 a month" | Card + photo + "Aman $25,000/mo" | Proof with a number | cut on "it's" |
| 42.5 | "I have landed a $2,000 upfront..." | Call screenshot scales in + "1k/mo -> $20k/mo in 90 days" | Proof 2 | on the sentence start |
| 46.4 | "My client ... land a $61,000 client" | Full-frame testimonial clip | Proof 3 | on the sentence start |
| 49.3 | "So what is this new AI business model..." | Title card 1/10 | Section marker | cut -0.14 s; title complete +1.7 s (d) |
| 55.1 | "It's an AI marketing agency that does exactly what a normal marketing agency does" | Speaker full frame, slow push +4.7% | Definition, direct | cut on "It's" |
| 61.3 | "So you do three things with clients" | Cut to list diagram; heading 61.40-61.60 | Set up a list of 3 | -0.11 s cut; heading on "three things" (d) |
| 63.2 | "One is content" | Circle 1 fills, "Content" appears 63.13-63.23 | List item | -0.1 s (d) |
| 70.2 | "Step two is ads" | Circle 2 fills, item 1 dims | List item | +0.39 s |
| 75.4 | "But now Claude can connect directly with Facebook ads" | Page swaps to pill connector | Show the connection | "Claude" -0.23 s, "Facebook Ads" +0.03 s |
| 79.7 | "targeting, location, budgeting" | Three small pills appear | Sub-items | +0.39, -0.11, +0.31 s |
| 83.0 | "answer engine optimization" | Back to list, item 3 fills | List item | +0.02 s |
| 84.5 | "when someone asks ChatGPT or Claude, who's the best barber in town" | Mock chat window builds | Act out the example | by eye within 0.5 s |
| 91.9 | "These services are helping a business get seen..." | Speaker full frame 9.8 s | Summary of why it matters | cut on the sentence |
| 101.8 | "So here's a reframe" | Punch in x1.168 | Flag an important line | -0.11 s (d) |
| 102.9 | "You're not an AI agency. You're a marketing agency..." | Card + icon, red "Marketing" wipes in | Visualise the reframe | cut -0.13 s (d) |
| 108.5 | "there's an explosion of creators, moms, dads..." | Side panel "Everyone can be creators:" bullets | Parallel list | bullets not word-matched (paraphrase) |
| 118.8 | "I mean, that is kind of true" | Tight speaker (face 45%) | Aside, candid | on the sentence |
| 132.6 | "But most of them, because they're beginners..." | B-roll cafe, then towers | Pattern break | on "But" (d) |
| 139.9 | "two databases" | Flowchart box 1 activates | Step 1 | -0.1 s (d) |
| 144.4 | "then a research agent" | Box 2 activates, arrow draws, camera pans | Step 2 | -0.1 s (d) |
| 147.2 | "a scripting agent" | Box 3 activates | Step 3 | -0.2 s (d) |
| 153.3 | "video editing AI employee" | Box 4 active from 151.1 | Step 4 | -2.1 s (d) |
| 155.5 | "people literally pay five, 10k, 15k" | Camera zooms out; price line types | Pay-off | 0 to +0.1 s (d) |
| 165.2 | "you can sell this to local business owners..." | Side panel slides in 165.03-166.0 | Customer list | panel -0.15 s; bullet 2 +0.2 s (d) |
| 177 | "pick one of these three" | Card + tree diagram | 1 of 3 choice | tiles on their words (by eye) |
| 184.8 | "AI startup founders are my favorite" | Side panel "My pick: AI founders" | Reasons list | bullets -0.4 to -2.7 s |
| 206.5 | "content production ... ideas, scripts, editing, posting, tracking" | Offer card 1 fills line by line | Offer contents | -0.19 to +0.59 s per line |
| 215.6 | "The other offer you can do is ads" | Card 2 becomes active | Next offer | +0.36 s |
| 229.7 | "And the next offer is AEO" | Card 3 becomes active | Next offer | by eye within 0.3 s |
| 257.8 | "I'm going to use an actual company" | Full-screen logo | Name the example | on the sentence |
| 265.8 | "I've helped him personally grow a big YouTube channel" | Card + channel screenshot + arrow "17,000 subscribers" | Evidence | on the sentence |
| 269.1 | "he has a very small Instagram presence" | Instagram profile screenshot | Evidence | on the sentence |
| 296.6 | "This is the prompt you enter" | Screen recording starts | Demo | on the sentence |
| 354.0 | "You're going to send this document..." | Document -> person diagram | What to do with the output | "Content strategy" +0.04 s |
| 376.7 | "First record a few videos" | B-roll sofa | Show the action | on "First" |
| 384.6 | "And let Claude code edit them" | Punch out x0.885 | New instruction; hides a cut | on "And" (d) |
| 428.6 | "So Claude just finished and here is a final output" | Time-skip to the finished video | Skip the wait | on "So" |
| 476.2 | "Instagram Edits just recently dropped a desktop app" | Website screenshot | Show the product | "app" text -2.7 s |
| 714.3 | "the Instagram trial reel is a great way..." | Trial-reels diagram | Explain the mechanism | heading +0.06 s |
| 752.8 | "you got a custom content strategy and ... two edited sample videos" | Card + Ty/You icons, samples | Who gets what | "You" label +0.97 s |
| 773.6 | "want to send a personalized outreach" | B-roll typing | Show the action | on "want" (d) |
| 800.0 | "book a call with you" | B-roll on a call | Show the action | on the clause |
| 837.0 | "don't try to sell them on AEO, sell them on ads" | Punch 836.97, shrink to card 837.03-837.60, red strike 837.6-838.3, "Ads" pill 838.5 | Wrong vs right | AEO pill -0.7 s, strike -0.2 s, Ads -0.3 s (d) |
| 859.3 | "that 1k a month retainer..." | Card; table row 1 at 860.8 | Do the sum | row +0.5 s (d) |
| 864.0 | "2k a month for ads" | Row 2 at 863.8 | Sum | -0.2 s (d) |
| 868.7 | "a five thousand dollar a month client" | Total row | Result | by eye about +1 s |
| 883.8 | "AEO, ads, content, they all complement each other" | Triangle diagram | Three parts of one | +0.3 to +1.3 s |
| 892.5 | "content production you can do a 5k setup" | Price card 1 turns dark | Price | by eye within 0.5 s |
| 911.6 | "as you have more case studies you can increase your prices" | Speaker full frame, slow push to the end | Closing argument, direct | cut on the sentence |
| 952.9 | "invite you to work with me one on one" | Call-recording montage | CTA proof | on "invite" |
| 961.1 | "if you don't get clients I don't get paid" | Big-text page | Guarantee | line 2 -0.28 s |

## 10. Why each cut is there

Sample: every 3rd row of timeline.md (#0, #3, ... #177) = 60 cuts.

| Reason | Count | Examples |
|---|---|---|
| Start a graphic / screenshot / screen demo | 14 | #3 10.06 (text page on "And that's probably"), #72 354.00 (document diagram); also #6, #15, #54, #57, #78, #102, #129, #132, #141, #159, #162, #177 |
| Screen changing in a recording (not an edit, or a time-skip inside the demo) | 14 | #105 539.07 (new project opens), #123 661.79 (share dialog); also #63, #66, #69, #84, #87, #90, #93, #108, #111, #114, #117, #120 |
| End a graphic, back to the speaker | 8 | #18 91.86, #153 839.30; also #24, #39, #51, #75, #126, #165 |
| Visible jump cut at a new sentence or clause (same framing) | 8 | #27 126.61, #135 765.47; also #48, #60, #99, #147, #150, #168 |
| B-roll in or out | 6 | #30 137.74 (out), #144 800.03 (in); also #33, #156, #171, #174 |
| Section change (title card) | 5 | #12 49.20, #96 459.79; also #21, #36, #42 |
| List item (next proof / next card) | 2 | #9 42.51, #45 215.53 |
| Hide a jump cut with a punch | 1 | #81 384.60 (x0.885) |
| Other | 2 | #0 start; #138 773.81 (detected inside one b-roll clip, no visible cut) |

Reading: outside the screen recordings, about two thirds of the sampled cuts start or end a graphic, b-roll or section; the rest are plain jump cuts. Emphasis-word punches are rare (1 in the sample, 6 in the whole video).

Longest stretches with no picture change:
- 583.93-617.32 (33.4 s), screen recording: "one that I had was outdated... now just watch it literally edit for us... I'll literally leave this on and let it do its magic".
- 512.51-539.07 (26.6 s), screen recording: "you'll see Claude directly synced with your Instagram edits app...".
- 678.76-703.14 (24.4 s), screen recording: "Now what you can do is you can send these edited videos to your lead...".
- 551.63-574.19 (22.6 s), terminal: the dictated prompt "check the new project... make four different variations".
- Outside recordings: 859.06-875.49 (16.5 s, card with the price table building), 238.22-252.02 (13.8 s, speaker: "you would hope that if your client is a barber... top three dentists in the vicinity").
- By hard cuts only: 911.6-952.9 (41.3 s) has nothing but same-framing jump cuts while he gives the closing argument.

## 11. On-screen text and captions

There are no running subtitles. After 4.3 s no caption is ever laid over the speaker footage; all text lives on white pages or panels.

| Kind | Size (% of frame height) | Position | Colour | Case / weight | Words | Animation | Duration | Repeats speech? Timing |
|---|---|---|---|---|---|---|---|---|
| Hook captions on footage (0.10-4.27) | small line 4.1-4.8%, big line 6.0-6.1% | Two blocks either side of the face: left x 0.05-0.37, right x 0.63-0.95, y 0.45-0.55 | White (#ede9e7 measured); newest word enters semi-transparent | Sentence case; small line medium weight, big line heavy italic ("with Claude AI", "heading into 2027"); "biggest opportunity" italic inside the small line | 4+3 and 4+3 | Word by word, each word fades in over 2-3 frames, about 0.10-0.13 s per word | 4.2 s and 2.4 s | Yes (with "1-person" for "one person" and "into" for "to"). First word +0.10 s; typing is faster than speech so each block completes 0.5-0.9 s early |
| Text on the card page (icon caption, 7.93-9.5) | 6.1% | Above the icons, x 0.36, y 0.28-0.34 | #2d2d2d; new words grey #666 | Sentence case, heavy; "selling", "no longer buying" italic | 9 | Word by word | 1.5 s | Yes, shortened; starts 0.27 s early |
| Big-text page | 5.2-7.2% line 1; 6.9-11.7% line 2 | Centred, y 0.45-0.53 | #2d2d2d-#2e2e2e; grey #888 while entering | Sentence case; line 1 medium, line 2 heavy italic | 3+6; 6+4 | Word by word | 1.8 s each | Yes, word for word; -0.07 to -0.28 s |
| Chapter title | number 10.2-10.6%; name 6.5-8.2% | Centred, y 0.39 and 0.50 | Number black #090909; name white on black bar | Number bold; name sentence case bold (written "claude", "instagram" in lower case) | 3-6 | Fade, bar wipe, word fade (1.9 s) | 1.1-5.3 s complete | Not a transcript; -2.9 s to +1.7 s where words match |
| List heading on card page | 8.3% | Left, x 0.10, y 0.35 | #656565 measured mid-fade; black by eye | Sentence case bold | 6 | Word by word | 9.9 s | Paraphrase |
| List lines on card page | 4.8-6.7% (OCR line boxes) | Left, under the heading | #333-#8a8a8a | Sentence case regular | 1-9 | Word by word | 2-7 s | Yes; -0.10 to +0.09 s, last items up to -0.7 s |
| Side-panel heading | 5.3-9.1% | Left, x 0.05, y 0.34-0.43 | #1b1b1b-#3f3e3e | Sentence case bold | 3-6 | Types on during the slide | 3.7-8.5 s | Paraphrase |
| Side-panel bullets | 4.7-6.4% | Left, y 0.47-0.68, round bullet | #1e1e1e-#646464 | Sentence case regular | 1-4 | Word by word | 1.4-7.9 s | 44% overall repeat words; -2.7 to +1.3 s |
| Diagram heading | 5.4-6.5% | Centred, y 0.25-0.27 | #484848 | Sentence case medium | 3-6 | Fade 0.2 s | 10-19 s | +0.06 to +1.4 s |
| Diagram labels | 3.0-5.6% | In boxes / beside icons | Active #333-#5a5a5a; dimmed #8c8c8c-#bebebe | Sentence case regular; pay-off lines bold | 1-4 | Fade on the spoken word | 1-28 s | Usually the spoken noun; median -0.02 s, p10 -2.1 s, p90 +0.6 s |
| Price table | 8.9-10.3% | Left 60% of the card page, y 0.27-0.76 | #1b1b1b-#282828 | Regular | 2 per row | Label fade, dotted leader types, amount fade | 5.6-14.6 s | Amounts as said; +0.5 / -0.2 s |
| Price cards | price 8.3-8.7%; title 4.1-4.8%; note 3.3% | Three cards, x 0.02-0.63, y 0.25-0.75 | White on #1a1a1a, red outline | Price bold | 1-12 | Card fades grey then dark | 8-18 s | Prices as said |
| Proof captions | 6.1-8.8% | Beside / under the image | #2f2f2f-#343434 | Heavy italic | 2-6 | Fade / build | 2.6-3.0 s | Figures as said |

## 12. Transitions

| Kind | Frames / time | Where |
|---|---|---|
| Hard cut | 1 frame | 106 detected; every title card, diagram, b-roll and screenshot enters and leaves this way |
| Speaker shrinks into the card | 4.37-5.33 (about 0.95 s, most of the move done by 4.80); 837.03-837.60 (0.57 s) | 2 uses. The full frame scales down and moves right with an ease-out while the white page and first graphic elements are already visible under it. Both are preceded by a small punch out one cut earlier (x0.958 at 4.30; x0.953 at 836.97) |
| Side panel slide in | 165.03-166.0 (0.9 s) | 165.0, 277.8 (and present from the cut at 108.5 and 184.8). White panel enters from the left edge to 50% width; speaker footage slides right; text types during the move |
| Side panel slide out | 190.37-191.10 (0.7 s) | 190.4, about 287.2. Panel exits left, text motion-blurred, speaker returns to centre |
| Graphic slides off with blur | 9.57-10.00 (0.45 s) | Once, before the big-text page |
| Blur cross-dissolve between two images on the card page | 44.53-44.90 (11 frames) | Once, between proof screenshots |
| White flash + over-exposed landing + eased zoom out | flash 35.27-35.40 (4 frames), landing 35.43-35.57 (4 frames), zoom settles by 36.4 | Once, promise to proof |
| Instant page swap inside a diagram | 1 frame | 75.17, 82.10 (labelled "pop") |
| Screen window fade-in | about 0.5 s | 776.0 |
| Window slides / cross-moves in the recordings | 0.4-0.75 s | 312.2, 576.1, 637.2, 651.1; these are the operating system's own animations, not edits |

Measured transition length overall: median 0.42 s, p90 0.75 s (11 detected).

## 13. Sound

Music: audio.json flags a bed only at 5-15 s and 25-35 s. The first 30 s averages -39.6 dB relative to the voice; 30-60 s is -48.6 dB; every window after 60 s is -50.4 to -52.7 dB, which is the noise floor of the stem. A regular low pulse (centroid 59-76 Hz, 0.07-0.09 s long, -10.6 to -13.1 dB relative to voice) runs every 0.545 s from 19.54 to 32.10 s (24 hits; about 110 per minute). The same kind of low hit is at 1.54 s. This reads as a kick-style beat under the credibility and promise lines. After 35.6 s there is no music.

Strong events and what is on screen:

| Time | Kind, level rel. voice | On screen at that instant |
|---|---|---|
| 4.24 (peak 4.29) | broadband, -12.2 dB, voice silent | The punch cut at 4.30 that removes the hook captions, 2 frames before the speaker starts shrinking into the card |
| 11.75 (peak 11.93) | broadband, 0.28 s, slow 180 ms attack, -12.9 dB | Rises under the end of the big-text page and peaks on the hard cut to the orbit diagram (11.93) |
| 19.54-25.04 (10 hits) | low pulse, -11.3 to -12.6 dB | Speaker full frame, no picture event (one coincides with a motion event at 23.90 by chance) |
| 25.52 | broadband + low, -11.9 dB, voice silent | Hard cut to the card + "By the end of this video" (25.49) |
| 26.09-32.10 (12 hits) | low pulse, -10.6 to -12.6 dB | List lines typing on; 4 fall within 0.12 s of a text/motion event, consistent with a regular beat rather than placed effects |
| 33.58 | broadband low (48 Hz), -7.2 dB | List line "5. Delivery" appearing (33.5-33.7) |
| 34.06 | broadband + low (30 Hz), +1.7 dB, 0.27 s | List line "7. Sales" appearing (33.95-34.1) |
| 34.50-35.64 (peak 35.47) | low swell, 0.97 s attack, +4.4 dB | Rises under "all of it", peaks on the white flash and cut at 35.43 |

Which picture events get a sound: only events in the first 36 s. Cut with a sound: punch 12%, hard 1%, transition 0%, pop 0%, jump 0% (summary.json). The 10 title cards, every diagram build, every b-roll cut, the side panels, the second card shrink (837.0) and all text typing after 36 s are silent.

Silences and pauses: 100 silences detected; the longest are 0.83 s at 456.8 and 0.75 s at 457.6 (end of the sample video, before title card 7/10), 0.75 s at 323.4, 0.61 s at 402.2. Longest voice pause 1.6 s at 456.8. No silence is used as a deliberate beat in talking-head sections.

## 14. Rules to reproduce this edit

1. Cut speech to a median pause of 0.20 s and keep 90% of pauses under 0.36 s; allow nothing over 0.45 s outside screen demos. Target 230-270 wpm.
2. Open on the speaker full frame with the first sentence on screen as two caption blocks beside the face (small line 4-5% of frame height, heavy italic line 6%), typed word by word at about 0.10-0.13 s per word starting 0.10 s after the first word. Remove them on a cut at the end of the sentence (4.3 s here).
3. Use captions over the footage only in the hook. After that, put all text on white pages or panels.
4. On the "but" of the hook, punch out about 4% (x0.958), then shrink the speaker into a portrait card over 0.6-0.95 s with an ease-out.
5. Card geometry: 26% of frame width, 71% of frame height (about 2:3), rounded corners, at x 0.685-0.948, y 0.141-0.852, on a white page with a vignette (#fefefe centre, #d0d0d0 corners). Graphic goes in the left 65%.
6. Use the card layout when the speaker should stay visible beside a small graphic (18 uses, median about 5.8 s). Use a full-screen gradient page (#ffffff top to #bdbdbd bottom, no speaker) for multi-step diagrams that run 6-31 s.
7. Start every section with a title card: "N/total" at 10% of frame height, a black bar wiping out from a cursor line, the chapter name in white at 6.5-8% inside the bar; build 1.9 s, total 1.75-5.9 s, hard cut in and out, placed on the first word of the bridging sentence.
8. Give the video numbered sections (10 here in 16 minutes; sections last 26-290 s).
9. In diagrams, show all parts as faint ghost outlines at the cut, then turn each part dark within ±0.3 s of its spoken noun and dim the previous part to grey.
10. In a wide flowchart, zoom about 1.15x and pan so the active box stays centred; zoom back out to show the whole chart for the pay-off line.
11. End a system diagram with a bold pay-off line that types on with the words (for example the price: "Clients pay $5K $10K $15K" at 155.5-156.8).
12. For a list of 3-4 parallel items said quickly, slide a white panel over the left 50% of the frame in 0.9 s, push the speaker to the right half, and type one bullet (5-6% of frame height) per item. Slide it out in 0.7 s.
13. For sums and prices, build a table at 9-10% of frame height one row per sentence with a typing dotted leader, or dark cards with prices at 8.5%.
14. For proof, show one image or clip per claim for 1.7-4.5 s with a bold italic caption of the figure; cross-dissolve with blur (11 frames) between two proofs in the same layout.
15. For a single strong sentence, cut to a text-only white page: line 1 at 5-7%, line 2 heavy italic at 7-12%, typed word by word, about 1.8 s total (2 uses).
16. Use hard cuts for everything else. Keep multi-frame transitions to the card shrink, the panel slide and at most one flash (4 white frames) per video.
17. Leave jump cuts between speaker shots visible at the same framing (20 here). Use an instant punch only for a marked line: in x1.17 for "here's a reframe", out x0.81-0.89 at the start of a new instruction (6 punches in 16 minutes).
18. Keep a slow drift on long speaker shots: 0.2-0.8 %/s in or out, 1-7% in total; about 1 in 4 shots (13 of 58) may be static.
19. In the closing argument, step slightly tighter at each jump cut and keep pushing in, about +15% over 35 s.
20. Frame the speaker with the face 33-37% of frame height, centre at x 0.45-0.51, y 0.35-0.41.
21. Use b-roll of the creator doing the thing being described: 1-2 clips per insert, usually 1.5-3.5 s each (up to 10 s for a "sales call" scene), hard cut in on the first word of the clause, no sound. 8 inserts in 16 minutes, mostly in sections without diagrams.
22. Show screen recordings at 88% scale on the gradient page with a round speaker inset (20% of frame height) in the bottom-right corner; move the inset if it covers the working area.
23. Do not add zooms or highlights to the recording; cut out waiting time with a hard time-skip and a spoken bridge ("So Claude just finished").
24. After a screen demo, return to the speaker full frame for at least one sentence before the next graphic (703.1-714.3, 361.0-365.3).
25. Change the picture about every 5 s outside demos (median gap between picture changes 5.18 s; median shot 3.52 s).
26. Put music only under the hook and promise (here 5-15 s and 25-35 s, a steady low pulse at about 110 per minute, about -12 dB under the voice per hit), then none.
27. Use sound effects only in the first 36 s: a short hit on the first punch cut (4.24), a rise into the cut after the text page (11.75-11.93), a hit on the cut to the promise list (25.52), and a low swell of about 1 s peaking on the flash cut into proof (34.5-35.5, up to +4 dB over the voice). No sound on any later graphic.
28. Master at about -15.7 LUFS with a narrow loudness range (2.8 LU) and peaks at -0.2 dBTP.
29. Keep the palette to black, greys and white with one red accent used for "wrong" (red icons, red strike-through, red card outline).
30. End on the speaker full frame pointing to the next video after a short CTA: 6 proof clips of 0.7-2.2 s and one text-only guarantee line.

## 15. Not determinable / measurement problems

- Picture class in summary.json ("face 83.9%") is not usable: it fired on the round inset, the speaker card, b-roll and call screenshots. Shares in section 1 are from my own shot-by-shot classification of the sheets.
- "Pop" and "jump" events between 296 and 703 s are almost all windows changing inside the screen recording. Which of them are real time-skips was judged by eye and by the narration; some may be misjudged.
- Three "jump" cuts inside the cafe b-roll (773.81, 774.56, 775.59) show no visible cut on the 30 fps sheet; cause unknown (possibly dropped frames or a speed change).
- "Punch x0.971" at 215.53 and 229.55 is the diagram's own view shift, not a speaker punch. The eight-punch count in summary.json therefore includes 2 non-speaker events.
- Title cards are labelled "eased zoom in x1.04-1.21"; no zoom is visible on the dense sheet at 49-51.5 s. Probably the bar wipe was read as zoom. Not confirmed for the other nine cards.
- Small "eased zoom" steps on the speaker (0.15-0.30 s, factor 0.96-1.04) look like jump cuts by eye at 97.5-97.9; the others were not checked frame by frame.
- Slow push/pull was confirmed by eye at 703-714, 736-749, 238-252 and 911-953 only; the other labelled shots rely on the measurement.
- Face-centre x 0.57 in summary.json is a mix of full-frame and card shots; full-frame shots measure 0.45-0.51.
- OCR text heights are line-box heights and include descenders; small list lines beside the card measure 4.8-6.7% but look closer to 2.5% by eye. Text colours were sampled mid-fade in several tracks (grey values for text that ends black).
- Lead/lag from timeline.md is good to about ±0.3 s; the hook's "-0.15 s" understates the lead because the captions type faster than speech. Word times come from an automatic transcript with errors ("sold per newers", "Uman", "cluster", "reduction").
- Font names cannot be determined; only "sans-serif, with a heavy italic cut" can be said.
- Names and sources of the music and sound effects cannot be known. Whether the low pulse at 19.5-32.1 s is a music track or placed hits cannot be proven; its regular 0.545 s spacing suggests music.
- Whether the screen recordings were sped up could not be determined.
- The exact end of the first card shrink (settling between 4.80 and 5.33 s) is approximate; the panel slide at 277.8 and its exit near 287.2 were read from shot sheets, not a dense sheet.
- Not read at 30 fps: the six client-call clips at 952.9-960.9, the proof image scale-ins at 38.0 and 42.5, the remaining nine title cards, and the list items after 63.5 s.
- No end-screen cards or subscribe graphics were seen in the sampled frames (962.7-971.5), but the last 9 s were sampled at only 4 frames.
