# Edit analysis: joseph-learn-editing

"How I'd Learn Video Editing in 2026 (Before AI Replaces You)", Joseph | Video Editing, 846.3 s (14:06), 30 fps.

Sources: `summary.json`, `shots.json`, `text.json`, `audio.json`, `words.json`, `timeline.md` (all 296 rows read), all 24 shot sheets, and 24 dense sheets in `dense/` (listed in section 13). Times are seconds from the start unless written m:ss. "Dense" means I checked single frames; "sheet" means a shot-sheet tile near that time.

**Read this first.** The `picture` class in the JSON is misleading for this video. The algorithm calls a shot "face" whenever a face is detected, and this video puts example clips of other people (a bearded man, women in skincare clips) inside phone-shaped cards on a light canvas. Splitting "face" shots by brightness (`luma` < 0.35 = the dark studio, > 0.7 = the light canvas) gives the real split used in this document:

| What is really on screen | Seconds | Share of runtime |
|---|---|---|
| Speaker in the dark studio (alone or with overlays) | 317 | 37.5% |
| Light-canvas or other full-screen graphics (with or without a face inside a card) | 528 | 62.5% |

## 1. Facts

| Measure | Value | Note |
|---|---|---|
| Length | 846.3 s, 30 fps, 1.7% duplicate frames | |
| Cuts | 295, 20.9 per min | algorithmic kinds below |
| hard | 100, 7.1/min | most are blur-dip cuts, see section 10 |
| transition (multi-frame) | 73, 5.2/min | median length 0.73 s, p90 0.90 s |
| pop | 70, 5.0/min | element appears in part of the frame |
| jump | 44, 3.1/min | many are overlay swaps or 1-2 frame artefacts |
| punch | 8, 0.6/min | 3 in (median x1.181), 5 out (median x0.869) |
| Shot length | median 2.18 s, p10 0.48 s, p90 5.93 s, max 18.2 s | |
| Time between picture changes | median 3.83 s, p90 9.77 s, max 21.0 s | |
| Picture share (JSON) | face 64.4%, flat graphic 32.4%, small face 3.0%, no face 0.3% | wrong for this video; corrected: speaker 37.5%, graphics 62.5% |
| Speaker face height | median 37.5% of frame height on true speaker shots (range 13-49%) | JSON all-face median 35.6% |
| Speaker face centre | x 0.50, y 0.38 | 86 of 99 speaker shots centred |
| Words | 3,728; 264 wpm overall, 278 wpm while speaking | per 30 s: 224-306 wpm |
| Voice active | 95.1% of runtime | |
| Pauses in voice | 78 (5.5/min), total 11.7 s = 1.4% of runtime | median 0.14 s, p90 0.19 s, max 0.22 s; none over 0.5 s |
| Speech run between pauses | median 1.12 s, p90 3.83 s, max 12.7 s | |
| Word gaps | 190, median 0.22 s, p90 0.32 s, max 0.74 s | |
| Loudness | -18.0 LUFS integrated, LRA 4.3 LU, true peak -1.4 dBTP | |
| Voice stem | -21.0 dBFS RMS | |
| Music bed | audible 98% of runtime (0-355 s and 360-850 s); median -24.7 dB below voice (p10 -33.6, p90 -18.0) | |
| Sound events | 425 candidates = 30.1/min; 368 "strong" = 26.1/min | strong median -7.8 dB below voice, 0.23 s long |
| Sound on a picture event | 37% of strong events vs 18% by chance | |
| Cuts that have a sound | hard 44%, punch 25%, transition 22%, pop 21%, jump 18%; chance 10% | sound lands a median 0.03 s after the cut |
| On-screen text | 432 big tracks = 30.6/min; median 2 words, on screen 1.4 s; 35% repeat spoken words | includes text inside example clips and the mic logo |
| Silences | 0 | |

## 2. Script structure

| Start | Beat | One line | How the edit marks it |
|---|---|---|---|
| 0:00 | Hook | "Right now is the most confusing time" to get into editing | Opens on blurred speaker that sharpens (0.03-0.40 s, x0.90 settle); punch-in x1.204 at 1.77 s; first caption builds from 1.77 s |
| 0:04.7 | Problem | "AI is becoming better", "everyone is claiming video editing is dead" | White bloom flash (4.50-5.30 s) into a collage of thumbnails and headline quotes |
| 0:12.9 | Counter-proof | Three students made $1,500 / $2,000 per month / $700 with AI editing | Back to speaker shifted right (x 0.73); post screenshots fade in on the left, one per student (14.8, 18.1, 21.4 s) |
| 0:23.8 | Reframe | "Video editing is actually now more important than ever" | Hard cut to light canvas, sentence builds word by word |
| 0:28.4 | Stakes | "95% of editors ... learned the wrong skills, and now AI can do their job" | Fast phone-card carousel, then speaker with big title behind his head (32.6 s) |
| 0:34.1 | Promise | "I'm going to show you the exact roadmap" | Punch-in x1.111, caption, small roadmap line drawn over his chest |
| 0:40.1 | Agenda | First / Then / Finally (18.2 s, one continuous graphic) | White wipe rising from the bottom (40.0-40.8 s) |
| 0:59.6 | Section 1 title | "Chapter One - Why editors get paid" | Speaker blurs and darkens, white title fades in (59.50-59.93 s). The only chapter title card in the video |
| 1:02.6 | Section 1 body | Businesses need marketing; raw video flops; that person is a "video editor"; you get paid for results | Alternates speaker and flow diagrams |
| 1:53.1 | Two skills | "Video engineering" and "editing knowledge" | Speaker with a mini diagram, then a two-column diagram (138.7-149.2 s) |
| 2:29.2 | AI claim | AI only executes the human vision; "this is the best thing that's happened" | Speaker run with small overlay cards |
| 2:57.4 | The question | "So the real question you need to ask yourself is..." | Punch-out x0.869 through a blur dip; later a dark quote card (184.2 s) |
| 3:07.1 | What to do | Master video engineering; execute with AI; become "the dream editor" | Icon + label chips on his chest; pipeline diagram 209-221 s |
| 3:44.8 | Bridge | "So how do you learn...?" | Roadmap line graphic (228.4 s), white bloom back to speaker (230.9-231.9 s) |
| 3:56.0 | Offer 1 (mid-roll) | Ultimate Editors program, 5 styles, AI course, masterclass | Course thumbnail card, module tiles; CTA pill at 301.0 s |
| 5:04.0 | Section 2 open | "Where should you get started?" three questions | Floating question lines around the speaker |
| 5:12.9 | Days 1-3 | Learn the AI tools (Claude 5:24, Remotion 5:37, Higgsfield 5:45) | Day-range pill card; each tool gets a logo card |
| 6:01.2 | Days 4-6 | Good design: typography, colours, layouts, effects | Day-range pill card (the previous pills slide out, new ones in) |
| 6:55.5 | Days 7-9 | Animation psychology | Day-range pill card after a punch-out x0.807 at 413.9 s |
| 7:36.8 | Day 10 | First edit | No card; hard cut back to speaker, x1.31 total zoom during the shot |
| 8:22.4 | Days 11-19 | Mastering video engineering (8 viral videos, recreate one a day) | Day-range pill card |
| 9:25.0 | Day 20 | "Create a wow edit" | Single-pill card "Day 20" |
| 10:13.9 | Days 21-30 | Acquire clients: find prospects, free edit, DM, post on your brand | Day-range pill card; numbered captions "1. Find prospects." (622.9 s), "Step 2: Upload your edit." (663.7 s) |
| 11:54.9 | Money | $30-$100 per short, $200-$600 per long video, weekly totals | Scattered price numbers around speaker, then price-tag grids and counters |
| 12:31.1 | Callback | "this is how the editors I mentioned early ... made the money" | Same post screenshots from 0:14 float beside the speaker |
| 12:36.1 | Recap + objections | Roadmap recap; most quit day 2-3; no community; YouTube overload | Roadmap line, people icons disappearing, wall of thumbnails |
| 12:59.7 | Offer 2 | "$2,000 to $4,000 per month" then the full program stack | Counter to $4,000/month, white bloom, 54 s of continuous graphics |
| 13:53.7 | Deadline + price | "closes down forever on November 15th", "$299" | Speaker; circled date in the caption; price card with struck-through $1,200/year |
| 14:00.4 | CTA | "Join Ultimate Editors 2.0. The link is down below." | White pill button "Click the link down below" stays to the end |
| 14:05.5 | End | "I'll see you guys inside." | Last frame 846.3 s; no end card |

Section changes inside the 30-day plan are always the same graphic (the day-range pill card, 6 uses). Everything else is marked by a return to the speaker at the start of a new sentence.

## 3. The rough cut

- Speech is cut very tight. The longest pause in the voice stem is 0.22 s; 78 pauses in 14 minutes, median 0.14 s, total 11.7 s (1.4% of runtime). No pause over 0.5 s. Longest word gap 0.74 s.
- Pace is 264 wpm overall and 278 wpm while speaking. Whether the audio was sped up or only cut tight cannot be told from the files.
- The speaker is on screen for 37.5% of the runtime, in 54 separate stretches (median 4.6 s, longest 17.8 s at 149.2-166.9 s). The other 62.5% is graphics, so most speech edits cannot be seen at all.
- When two speaker takes meet, the join is hidden in three ways:
  1. **Blur dip plus scale change.** Dense 177.1: the outgoing take blurs for 3-4 frames (177.27-177.33 s), cut at 177.37 s to a different scale (x0.869), the incoming take is blurred and sharpens over 4-5 frames (to 177.50 s). The cut falls between "ever." and "So the real question".
  2. **Plain punch cut.** Dense 1.5: at 1.77 s the picture jumps to x1.204 in one frame with no blur, between "right" and "now". Dense 198.4: at about 200.93 s an instant jump of about x1.25 (the JSON lists it as a zoom move, not a cut).
  3. **Going to a graphic.** 23 of the 59 sampled cuts in section 8 are a switch between speaker and graphic at a sentence start.
- Jumps left bare: timeline lists same-scale "jump" cuts on the speaker at 113.13 s ("which brings me directly into my next point"), 132.67 s, 191.30 s, 207.77 s, 224.77 s, 309.97 s, 368.40 s, 370.70 s, 425.40 s, 500.40 s, 561.87 s, 608.10 s, 691.40 s, 755.47 s. I did not dense-check each one; the one I did check that was labelled "jump" (75.63 s) was not a cut in the speaker footage at all but one of three overlay cards swapping its picture.
- `cut_vs_speech`: 42% of same-picture cuts and 43% of picture changes fall between words; 23% and 33% fall after a sentence end; 8% fall inside a measured pause (chance 2%).

## 4. Camera on the speaker

Measured on the 99 true speaker shots (dark studio, longer than 0.3 s; total 317 s; median shot 3.0 s, longest 11.4 s at 196.4 s).

Framing: face height median 37.5% of frame height, centre x 0.50, y 0.38. Dark set (dominant colour #0c0d0e), green plant top-left, black microphone on a boom arm entering from bottom-left.

| Move | How many | Size | Duration | Examples (s) | Trigger |
|---|---|---|---|---|---|
| Entry settle: shot starts blurred and slightly small, sharpens while scaling up | 58 of 99 shots | median x1.086 (range x0.90-x1.118) | median 0.33 s; blur clears in 5-12 frames | 58.33-58.70 x1.093 (dense: sharp by 58.47); 72.63-73.10 x1.092; 128.67-129.10 x1.104 (dense: sharp by 128.83); 221.17-221.47 x1.082; 32.67-33.23 x1.092 (dense: sharp by 33.03) | Every return to the speaker from a graphic |
| Exit push: scale up while blurring out before leaving | 40 of 99 shots | median x1.107 | median 0.33 s | 78.73-79.03 x1.094; 133.73-134.07 x1.106; 235.77-236.03 x1.105; 328.70-329.17 x1.134; 374.77-375.17 x1.123; dense 119.7: blur starts 119.83, gone by 120.47 | Last third of a second before a graphic |
| Punch-in cut (instant) | 3 listed + 1 unlisted | x1.204, x1.111, x1.181 (median x1.181); about x1.25 at 200.93 | 1 frame | 1.77 "now is the most confusing time"; 34.10 "So in this video, I'm going to show you the exact roadmap"; 698.13 "why it's much more important for you to become a good editor"; 200.93 "And the truth is" | The line that states the stakes or the promise |
| Punch-out cut (through a blur dip) | 4 on speaker | x0.869, x0.807, x0.946, x0.96 | 7-9 frames of blur around the cut | 177.37 "So the real question you need to ask yourself"; 413.87 "After you've done this, by day six"; 714.87 "Now, once you do land your first client"; 251.47 | A pivot sentence starting with "So", "After", "Now" |
| Slow push-in through the shot | 12 shots | median 1.33% per second | whole shot | 1.77-4.73 x1.032; 34.10-40.07 x1.034; 304.0-309.97 x1.060; 698.13-702.60 x1.022; 714.87-718.30 x1.088 | Shots that carry a caption or floating text |
| Eased zoom-out to make room for overlays | 5 | x0.71 to x0.90 | 0.5-2.6 s | 151.90-152.70 x0.791 (cards appear below at about 155.3); 198.57-199.17 x0.897 (dense: icon chip and "How to execute with AI" build in from 199.3); 496.47-499.07 x0.712 over 2.6 s (dense: seven cards pop in around him one by one); 611.20-611.70 x0.799 ("You are now a high-quality editor" caption) | Overlays are about to appear |
| Mid-shot eased push | 4 | x1.07 to x1.32 | 0.3-1.2 s | 488.93-489.63 x1.319 "then you're on track to success"; 547.03-548.23 x1.316 "recreate these animations"; 460.70-461.00 x1.072; 608.70-609.17 x1.076 | End of a point, payoff word |
| Side reframe (speaker placed left or right, card on the other side) | 13 shots | face x 0.73 or 0.24-0.30 | whole shot | 14.17-23.80 (speaker right, post screenshots left); 569.13-574.87 (speaker left, phone card right); 597.17-599.77; 607.10-608.10; 836.83-840.43 (price card right) | Proof or example shown beside him |

How often is he static: one of 99 speaker shots is tagged static. In practice the frame holds still between the entry settle and the exit push in most shots: only 19 zoom moves happen mid-shot across all 99 shots, and 12 shots have a slow push. So the rule is "always move on the way in and on the way out, mostly hold in between".

Check of numbers against frames: the x1.204 punch at 1.77 s, the x0.712 pull-out at 496.5-499.1 s, the x0.897 pull-out at 198.6-199.2 s and the entry settles at 58.3 and 128.6 s all look right in dense frames.

## 5. Layouts

| # | Layout | Share / count | Examples (s) | What the speaker is doing |
|---|---|---|---|---|
| 1 | Speaker full frame, centred, nothing else | part of the 37.5% speaker time; the plain version is short stretches | 62.6-64.6, 111.3-119.6, 128.6-134.1, 173.5-179.3, 410.7-415.5, 694.8-702.6 | Talking to lens, hand gestures |
| 2 | Speaker + caption in the lower third, lower part of frame darkened | 25 caption instances | 1.8-4.6, 35.1-40.0, 73.6-79.0, 95.9-98.7, 177.5-179.2, 247.3-251.4, 287.0-290.3, 657.2-660.0, 834-836.8 | Talking; caption builds word by word |
| 3 | Speaker centred + floating elements (cards, icon chips, word labels, numbers) on a dimmed background | about 20 instances | 72.6-79.0 (3 phone cards under his chin); 149.2-156.2 (mini flow diagram at chest height); 189-191 and 199.4-200.9 and 226.5-228.4 (icon chip + label on chest); 203.9-208.9 and 496.5-502.3 and 690.3-694.8 (cards scattered all round him); 304-312.9 (three question lines); 358.9-361.2 (three tool logos); 367.9-375.2 (script lines beside head, words highlighted); 382.4-387.1 (four words along the bottom); 421.0-427.1 (card left, card right, arrow over his head); 552.1-563.0 (row of 8 cards along the bottom); 716.6-719.3 (price numbers) | Talking; background is darkened so the overlays read |
| 4 | Speaker on one side + card on the other | 13 shots | 14.2-23.8; 544.5-548.2; 569.1-574.9; 597.2-599.8; 607.1-608.1; 836.8-840.4 | Talking; card holds a post screenshot, a phone clip, or a price |
| 5 | Big title behind the speaker's head | 1 | 32.6-34.1 "Now AI can do their job" | Talking in front of the text |
| 6 | Speaker blurred and darkened as a backdrop for a title | 1 | 59.6-62.6 "Chapter One" | Still talking (voice continues), unreadable |
| 7 | Full-screen light canvas graphic | most of the 62.5% | 23.8-32.6, 40.1-58.3, 64.6-72.6, 79.0-108.5, 120.2-128.6, 134.1-149.2, 209.1-221.1, 236.0-247.2, 251.5-260.6, 264.9-286.0, 290.3-301.0 and most of 5:13-13:54 | Not visible; voice only |
| 8 | Dark quote card (previous graphic blurred and darkened, text on top) | 2 | 108.5-111.3; 184.2-187.1 | Not visible |
| 9 | Screenshot or screen recording in a window on the canvas | 10 | pricing page 329.2-332.8; YouTube watch page 332.8-337.3, 342.9-345.5, 575.7-579.1, 773.1-776.0; Pinterest board 377.4-382.4; Claude chat 406.0-410.7; Instagram search and profile 624.0-631.2; DM thread 648.2-662.7; upload dialog 666.6-669.4 | Not visible |
| 10 | Illustrated metaphor, full frame | 1 | 321.2-324.4 paintbrush + Mona Lisa on a parchment canvas (#e9e4da) | Not visible |

Not used: a shrunken speaker inside a card, split screen with live speaker and full graphic, live-action b-roll of the outside world. Every clip that is not the speaker is an example edit shown inside a portrait phone card.

## 6. Motion-graphics catalogue

Common look, seen on every light graphic: off-white canvas (dominant colour #ebeae9 to #edecec) with a faint square grid and a soft blue glow in the centre; flat 2D; white rounded cards with soft shadows; one accent blue (measured #214dc3 to #2252cd) for key words, numbers and active icons; body text dark grey (#1b1b21 to #262523) in a light-weight geometric sans; phone-shaped portrait cards with rounded corners hold example clips. Nothing is 3D. Elements enter by fading in from a blur with a small scale-up over roughly 8-14 frames (dense 14.6: post card 14.77-15.20 s); text enters one word at a time, each word resolving from blur in 3-4 frames (dense 23.8).

| # | Type | Looks like | Triggered by (real lines) | Enter / build / leave | Hold | Where |
|---|---|---|---|---|---|---|
| G1 | Word-by-word statement | One or two centred lines on the canvas, 6-9% of frame height, key words bold blue | "The truth is, video editing is actually now more important than ever" (23.8); "In 2026, there are these businesses that all want to make money" (64.6); "what you need to do is become the dream editor" (209.1); "If you don't want to be replaced as a video editor in 2026" (290.3) | Hard cut to empty canvas; each word appears within about 0.1 s of being spoken (dense 23.8: "truth" said 23.88, sharp 23.93; "more" said 25.72, shown 25.80; "important" said 26.22, shown 26.20); then the line shrinks and moves to the top to become a header (211.0-211.8) or letters scatter out (28.1) | 2-4 s as main subject, up to 9.6 s as header | 23.8, 64.6, 209.1, 290.3, 786.9 |
| G2 | Thumbnail collage around a centre title | "AI Video Editing" pill title in the middle, portrait cards and YouTube thumbnails filling in around it, edges blurred | "AI is becoming better and better at editing by the day" (4.7) | White flash, title words fade in 5.30-5.60, cards add from 5.5 to 7.0 (dense 5.73), camera drifts | 5 s | 5.3-10.2 |
| G3 | Headline quote over blurred collage | A sentence in quotation marks, dark grey, 8.7% tall, collage blurred behind | "Everyone is claiming that video editing is dead" (8.0); "it feels like the whole world is crumbling down" (10.2) | Letters resolve from scattered blur; quote scrambles into the next quote (10.9-11.8) | 1.5-2.5 s each | 10.2-12.9 |
| G4 | Post screenshot card (proof) | White card with a social post and image, about 35% of frame width, beside the speaker or scattered on canvas | "one of our students made $1,500 in a day with AI editing" (14.2); "another one crushed the $2,000 per month mark" (17.5); "made $700 in a day" (21.4); "this is how the editors that I mentioned early in the video have made the money" (751.1) | Fades in from blur and dark over 14 frames; next card pushes the old one up and out (18.1, 21.4) | 2.5-3.3 s each | 14.8-23.8, 245.5-247.2, 751.1-756.1, 779.7-784 |
| G5 | Phone-card carousel | One portrait card in the centre whose content swaps fast; later a row of four | "95% of editors have spent the last year learning the wrong skills" (28.4); "learn how the viral editing styles of 2026 are made" (294.3) | Card pops in over the fading text, swaps every 0.3-0.6 s, final zoom x1.32 at 31.6-32.6 | 4 s | 28.2-32.6, 290.3-301.0 |
| G6 | Roadmap line | Thin horizontal line, small dots with labels above and below, one pulsing blue dot that travels, ends in "$2,000/month" | "the exact roadmap that every editor needs to follow" (34.1); "A 30-day plan you can implement today" (54.6); "I'm going to show you the full plan ... from day zero" (228.4); "now that you have the full complete roadmap" (756.1); "land your first $2000 per month client" (831.4) | Line draws left to right, camera slides along it, labels fade in as the dot reaches them | 2.4-3.6 s | 37-40 (over speaker), 54.6-58.3, 228.4-231.0, 756.1-759.2, 761.0-763.0, 831.4-833.7 |
| G7 | Flow diagram: card, icon tile, card | Raw clip card on the left, dashed line to a white rounded icon tile (person icon or the orange Claude icon), arrow to an edited design card on the right | "they need someone to turn that raw content into the viral videos" (85.6); "That person, that's what we call a video editor" (92.4); "You get paid to deliver high quality premium viral videos" (101.7); "First, we have a very deep understanding of how content works" (120.2); "You can now take any video that your client has and instantly have the best vision for it" (211) | Left card first, dashed line draws, tile fades in, right card last, each on its phrase; virtual camera pushes into the tile (92.43-93.37, x1.61, dense) and the tile turns solid blue with the label "Video editor" at 94.2-94.8 | 5-10 s | 87.1-94.9, 101.7-108.5, 120.2-128.6, 134.1-138.7, 179.3-184.2, 192.2-196.4, 209.1-221.1 |
| G8 | Chapter title | Speaker blurred and darkened (canvas reads #08080f); "Chapter One" white, 12.6% tall; subtitle "Why editors get paid" light blue (#7a9ab5), 6.3% | "it all starts by understanding why video editors get paid in the first place" (58.3) | Dense 59.4: background blurs and darkens over 8 frames from 59.50; title fades from blur 59.67-59.93; subtitle words one at a time from 60.03 ("why" said 60.06) | 3.0 s | 59.6-62.6 |
| G9 | Icon population | Many small outline icons (briefcases, people) multiply, ring out or drop away | "there are these businesses that all want to make money ... they need to get more clients" (64.6); "every single day you find one new prospect" (684.6); "most people quit on day two or three" (760.9); "they don't have a community of people supporting them" (766.4) | Icons fade in one by one; camera pulls out (68.2-70.5, x0.565) to show concentric rings of people with red pulses | 2-8 s | 64.6-72.6, 684.6-689.9, 760.9-763.0, 766.4-769.7 |
| G10 | Clip plus bullet lines | Large phone clip on the left third, two or three text lines on the right, key word blue | "It doesn't get any views and it doesn't portray the business in a nice way" (82.9) | Camera cut closer to the clip; each line builds as spoken ("Doesn't get views" leads the words by 0.23 s) | 2.7 s | 82.9-85.6, 539.0-544.5 |
| G11 | Dark quote card | Previous graphic blurred and darkened to near black (#2b2b2b to #000000); two centred white lines, 6.7-7% tall, key words light blue | "If it's done right, the client doesn't care" (108.2); "What do I need to do as a video editor in order not to get replaced?" (184.2) | Dense 107.4: blur and darken 108.2-109.3 while words build from 108.13 ("If" said 108.24); fades to black at 110.7 | 2.5-3 s | 108.5-111.3, 184.2-187.1 |
| G12 | Two-column labelled diagram | Two blue headers ("Video engineering", "Editing knowledge", 6% tall) each with an icon tile above and a small flow diagram below | "The terms I use for those skills are video engineering ... and editing knowledge" (138.7) | Left column builds first, right column on its phrase (header lags the words 0.4-0.7 s) | 9.1 s | 138.7-149.2 |
| G13 | Day-range pill card | Two white circles with "Day" in grey (6-7% tall) and a blue number, joined by a thin line with a white pill label in the middle ("Learning the AI editing tools", "Good Design", "Animation Psychology", "Mastering Video Engineering", "Acquire clients"); Day 20 is a single circle | "First, we're going to get started with day 1 through 3 learning the AI editing tools" (312.9); "On days 4 to 6 we need to learn ... good design" (361.2); "from Day 11 to Day 19" (502.4) | Dense 312.5: white wipe rises from the bottom over 33 frames (312.5-313.6); circles ride up with it; label pill fades in 314.3-314.6 (0.3-0.5 s after "learning"); camera eases in x1.12 in the last 0.35 s | 3.1-6.2 s | 312.9, 361.2, 415.5, 502.4, 565.0, 613.9 |
| G14 | App logo card | Colour app icon in a rounded tile in the centre, the app name as a huge pale outlined word behind it | "The first tool we want to learn is Claude" (324.4); "The second tool I would learn about is Remotion" (337.3); "the third thing that I would learn is Higgs Field" (345.5); "loading up Pinterest" (375.2) | Icon fades in from blur, wordmark draws behind; slow push | 1.7-2.2 s | 324.4, 337.3, 345.5, 375.2, 512.0 |
| G15 | Screenshot / screen recording window | Real web page in a rounded window with shadow on the canvas; cursor visible | "sign up for the subscription at least the $20 per month plan" (329.2); "watch how other editors are using Claude to edit videos" (332.8); "gathering a bunch of inspiration" (377.4); "I would go on Instagram and try to find those business owners" (624.0) | Blurred, then sharp, with a push of x1.08-1.12 at the start and end; Pinterest board zooms from a tiny thumbnail to full frame (377.07-378.03) | 2-5 s | see layout 9 |
| G16 | Annotated example board | A design image with hand-written labels and curved arrows ("Font weights", "Sizes", "Cast shadow", "pop up fading", "blur slide-in"), colour swatches, circles on details; a header word top centre | "analyze how the text behaves in all of these designs, what kind of fonts are being used" (386.2); "break down the color palettes" (393.8); "Pay attention to what kinds of animations are being used on the text" (432.2); "the assets, the effects, the elements, and the layout" (527.3) | Board slides sideways to the next example on each list word; labels write on one at a time as each item is named | 3.5-10.5 s | 387.1-406.0, 430.9-440.7, 447.1-456.8, 527.3-537.8 |
| G17 | Card row or grid | 4-30 phone cards or wide thumbnails in a row or grid | "find eight viral videos that really impress you" (508.0); "rank them from the easiest ... to the hardest" (517.3); "anywhere between 3 to 5 short form videos per day" (719.3) | Cards fade in left to right, one per count; row re-sorts for "rank" | 2-8 s | 427.1-430.9, 508.0-511.9, 520.4-522.7, 552.1-563.0 (under speaker), 688.5-689.9, 719.3-728.5, 744.9-751.1 |
| G18 | Number counter | Blue number with small grey unit ("$2,000/month"), 11-19% tall | "someone making $2,000 per month" (57); "at least one of your trendy formatted videos" (710.9, no number spoken); "making $2000 to $4000 per month" (779.7) | Dense 710.6: counts $10 to $2,000 in 1.7 s, fast then slowing (710.6-712.27) | 1-3 s | 57.0-58.3, 708.9-712.6, 733.6-740.3, 746.5-751.1, 779.7-783.8 |
| G19 | Value pill over blurred cards | White pill with a blue range ("$30 to $100", 7.4% tall) while the cards behind blur; bracket line with "per day" under them | "anywhere between $30 to $100 per short form video" (728.5) | Cards blur, pill fades in on the number (lag 0.13 s) | 2.9 s | 728.5-732.2 |
| G20 | Script and clip workspace | White transcript panel beside the raw clip; phrases get highlighted; small design cards appear next to highlighted lines | "grab a raw clip and put the script next to it" (466.3); "pull out the transcript of that clip and plan out your edit" (579.1); "looking at what's happening in the script" (368.4, as lines beside the speaker) | Clip first, panel slides in from the left at 468.5, highlights appear as each skill is named | 6-13.5 s | 367.9-375.2, 466.3-485.2, 522.7-527.3, 579.1-590.0 |
| G21 | Chat mock | Message field with text typing, blue sent bubble, then a clip attachment and a grey reply | "send them a quick message say, Hey, I spent the last few days mastering how viral videos are edited" (648.2); "If they like it, they're going to reach back out" (660.0) | Text types as he reads it; bubble sends at 654.4-654.8 with a camera pull-out x0.73 | 6.6 s + 2.7 s | 648.2-656.2, 660.0-662.7 |
| G22 | Course / product cards | The course thumbnail shrinks to the top; under it a line of text, then tiles for each module (dark gradient cover cards with titles, speech-bubble icons with blue labels) | "that's why we built Ultimate Editors. It's the step by step program" (236.0); "Using our AI editing fundamentals course" (264.9); "you're going to get the Iman Gadzhi skill, the Vox documentary skill" (806.4) | Thumbnail fades in big, eases to the top (237.3-238.1, x0.58), items fade in under it as named | 9-15 s each | 236.0-247.2, 251.5-260.6, 264.9-286.0, 784.4-831.4 |
| G23 | Price card | Dark card beside the speaker: "Ultimate Editors 2.0", "$1,200/year" struck through, "$299" in light blue (12.8% tall), blue button "Get lifetime access" | "you can now get lifetime access for just $299" (836.8) | Card fades in; old price first, strike-through, then $299 (0.31 s after the word) | 3.6 s | 836.8-840.4 |
| G24 | CTA pill | White pill button low centre with a link icon, "Click the link down below" (blue underlined words), small cursor | "Click the link down below before the program closes down forever" (301.0); "The link is down below" (843) | Fades in 0.8 s after the line starts; stays | 2-5.8 s | 301.8-304.0, 840.5-846.3 |
| G25 | Illustrated metaphor | Painterly paintbrush and Mona Lisa on parchment; the painting brushes itself in | "you can't paint the Mona Lisa if you don't know how to use your brush" (321.2) | Hard cut; painting reveals over about 2.5 s; push x1.12 at the end | 3.2 s | 321.2-324.4 |
| G26 | Floating lines around the speaker | Two-line questions or bullet phrases at head height left and right, white with light-blue key words, 5-7% tall, background dimmed | "where should you get started ...? How do you learn to edit good videos and how do you land high paying clients?" (304.0); "they don't know where to learn the new things" (763.0) | Each line builds as spoken, earlier lines blur and drift back | 3-6 s | 304.0-312.9, 763.0-766.4 |
| G27 | Scattered numbers around the speaker | Dollar amounts in light blue (#93ccfc), 7-15% tall, different sizes and depths, some blurred | "there is a lot of money that can be made" (714.9) | Numbers fade in one after another, drift slowly | 2.7 s | 716.6-719.3 |
| G28 | Icon chip on the chest | Small dark rounded tile with a line icon and a one-line label under it (4% tall) at chest height | "master video engineering" (187.1); "learn how to execute it with AI" (199.4); "how Claude, Remotion and Higgs Field all work" (356.8) | Dense 198.4: frame zooms out and dims 198.6-199.2, chip fades in 199.7-200.0, label words build to 200.5 | 1.5-2.5 s | 189.0-191.3, 199.4-200.9, 226.5-228.4, 358.9-361.2 |
| G29 | Thumbnail wall | Full frame packed with YouTube thumbnails, darkened | "trying to learn things on your own on YouTube" (773.1) | Starts as one watch page, zooms out to the wall at 775.9, darkens | 3.9 s | 773.1-777.0 |
| G30 | Vertical-video mock | A blank portrait card on the canvas that fills with what he describes (text "POV: your client paid you for a viral edit", shots of someone at a desk, a 3-2-1 countdown) | "writing out text that says POV, your client paid you for a viral edit" (672.4); "a countdown timer for three seconds" (677.9) | Text types in as spoken (0.07 s before the words); clip swaps on each described step | 8.4 s | 671.7-682.1 |

## 7. Script -> picture table

Lead/lag is picture relative to the spoken word: minus = picture first.

| Time | Spoken line | What the picture does | Job | Lead / lag |
|---|---|---|---|---|
| 0.0 | "If you're trying to get into video editing right" | Blurred speaker sharpens, slight zoom out x0.90 in 0.4 s | open on a face, no title | - |
| 1.77 | "now is the most confusing time to do that ever" | Punch-in x1.204; caption builds, "confusing" in blue | emphasis -> punch-in + caption | caption +0.21 s |
| 4.7 | "AI is becoming better" | White bloom flash, "AI Video Editing" title, collage grows | topic word -> title with examples | title appears 5.30, word "AI" was said at 4.7: +0.6 s |
| 8.0 | "Everyone is claiming that video editing is dead" | Quote "Video editing is dead." over blurred thumbnails | quote -> text in quotation marks | about +1 s |
| 12.9 | "while all of this is happening," | Transition back to speaker | contrast -> return to face | 0 |
| 14.2 | "one of our students made $1,500 in a day" | Speaker moves right; post screenshot fades in left (14.77-15.20) | proof -> screenshot | +0.5 s |
| 18.1 | "the $2,000 per month mark" | Second post replaces the first | proof list -> one card per item | 0 |
| 21.4 | "made $700 in a day" | Third post | proof list | 0 |
| 23.8 | "The truth is, video editing is actually now more important than ever" | Sentence builds word by word on empty canvas | key claim -> full-screen sentence | within 0.1 s of each word |
| 28.4 | "95% of editors have spent the last year learning the wrong skills" | Phone card pops over the dissolving text, content swaps fast | generalisation -> rapid examples | -0.2 s |
| 32.6 | "and now AI can do their job" | Speaker; big title behind his head, "AI" blue | punchline -> title behind subject | within 0.15 s of each word |
| 34.1 | "I'm going to show you the exact roadmap" | Punch-in x1.111; caption; small roadmap line on his chest ending "$2,000/month" | promise -> punch-in + preview graphic | caption +0.84 s |
| 40.1 | "First, I'm going to show you why you get paid" | White wipe up; line "First, why you get paid" + icon tile | agenda item 1 -> text + icon | +0.3 s |
| 45.2 | "Then ... why AI is actually the best thing" | Line swaps; clip, Claude icon, clip | agenda item 2 -> mini diagram | 0 |
| 52.0 | "And finally, I'll take you through a 30-day plan" | Header "A 30-day plan you can implement today"; roadmap line | agenda item 3 -> roadmap | +1.0 s |
| 57.0 | "making $2,000 per month" | Blue "$2,000/month" grows at the end of the line | number -> big number | 0 |
| 59.6 | "why video editors get paid in the first place" | "Chapter One / Why editors get paid" over blurred speaker | new section -> title card | subtitle +0.41 s |
| 64.6 | "in 2026, there are these businesses that all want to make money" | Text builds; three briefcase icon tiles | abstract actors -> icons | text 0 to -0.1 s |
| 68.2 | "they need to get more clients" | Camera pulls out x0.565; rings of people icons, red pulses | scale -> multiply icons | 0 |
| 72.6 | "The most effective method of marketing in 2026 is organic video marketing" | Speaker; caption; three phone cards under his chin | term -> examples beside speaker | caption +0.79 s |
| 79.0 | "when they record raw content and post that" | Canvas; header "Raw video"; one phone clip | noun -> the thing itself | +0.15 s |
| 82.9 | "doesn't get any views and it doesn't portray the business in a nice way" | Close on the clip; two bullet lines build | consequences -> bullets as named | -0.23 s, +0.25 s |
| 87.1 | "turn that raw content into the viral videos" | Clip, dashed line, person tile, designed card | process -> flow diagram | 0 |
| 92.4 | "That person, that's what we call a video editor" | Camera pushes into the person tile (x1.61 in 0.9 s); tile turns blue; label "Video editor" | naming -> zoom to the icon + label | label in sync (94.2 vs word 94.12) |
| 98.5 | "you don't get paid because you know Premiere Pro or After Effects" | Speaker; caption; Pr and Ae app icons under the caption | named tools -> their icons | caption +0.11 s |
| 101.7 | "You get paid to deliver high quality premium viral videos" | Diagram with hand-drawn arrow and "You get paid." pointing at the result card | claim -> annotate the diagram | +0.04 s |
| 108.2 | "If it's done right, the client doesn't care" | Diagram blurs and darkens; two-line quote | maxim -> text on darkened graphic | -0.04 s |
| 113.1 | "which brings me directly into my next point ... two major things" | Speaker; mini diagram (clip, dashed line, card) appears at 119.6 | setup -> plain face | - |
| 120.2 | "First, we have a very deep understanding of how content works" | Blur dissolve to canvas; two icon tiles, sentence, then clip and arrow to designs | list item 1 -> icon + sentence + example | text -0.02 s |
| 128.6 | "It's a lot like an interior designer" | Speaker only | analogy -> no graphic | - |
| 134.1 | "Second, we know how to use Premiere Pro and After Effects" | Canvas; brush icon; cards with arrow; Pr and Ae icons | list item 2 -> matching diagram | 0 |
| 138.7 | "The terms I use for those skills are video engineering ... and editing knowledge" | Two labelled columns build | definitions -> labelled diagram | +0.41 s, +0.69 s |
| 149.2 | "AI is simply getting better at taking the human vision you have and executing it" | Speaker zooms out x0.79; clip, sketches, Claude icon, result card at chest height | claim -> small flow under speaker | result card pops on "executing it" (155.4) |
| 177.4 | "So the real question you need to ask yourself is" | Punch-out x0.869 through blur; caption | pivot -> scale change + caption | caption -0.01 s |
| 184.2 | "What do I need to do as a video editor in order not to get replaced?" | Graphic blurs and dims; question as text | the question -> text on blurred graphic | -0.05 s |
| 187.1 | "The first thing you need to do is master video engineering" | Speaker; icon chip + "Video Engineering" | named skill -> chip | +0.34 s |
| 199.4 | "You also need to learn how to execute it with AI" | Zoom-out x0.897; chip "How to execute with AI" | named skill -> chip | -0.05 s |
| 203.9 | "faster than you, cheaper than you and make better edits" | Cards fly in all around him | list of threats -> surround speaker | 0 |
| 209.1 | "what you need to do is become the dream editor" | Wipe to canvas; sentence; then pipeline builds under it | goal -> headline then diagram | +0.9 s |
| 228.4 | "the full plan on how I would do this from day zero" | Roadmap line, camera travelling along labels | plan -> timeline | 0 |
| 236.0 | "that's why we built Ultimate Editors" | Course thumbnail card, then tagline text | product -> its cover | -0.59 s |
| 247.2 | "almost 48 hours before this program closes down forever" | Speaker; caption, "48 hours" blue | deadline -> caption | +0.03 s |
| 251.5 | "the five viral editing styles of 2026, cinematic videos, minimal animations, ..." | Style title tiles along the top, an example clip under each as it is named | list -> items appear as each is named | -0.8 to +0.35 s |
| 264.9 | "we teach them the fundamental tools, Claude, Remotion and Hicksfield" | Title, then three app icons one by one | list -> icons | +0.27 s |
| 301.0 | "Click the link down below" | Speaker; white pill button with cursor | CTA -> button | +0.81 s |
| 304.0 | "where should you get started ...? How do you learn to edit good videos and how do you land high paying clients?" | Three question lines float around his head | questions -> text beside speaker | -0.1 to -0.8 s |
| 312.9 | "day 1 through 3 learning the AI editing tools" | White wipe up; Day 1 - Day 3 pill card | new section -> section card | pills +0.3 s, label +0.3-0.5 s |
| 321.2 | "can't paint the Mona Lisa if you don't know how to use your brush" | Paintbrush and Mona Lisa painting itself | metaphor -> literal illustration | 0 |
| 324.4 | "The first tool we want to learn is Claude" | Claude logo card | named tool -> logo | 0 |
| 329.2 | "sign up for the subscription at least the $20 per month plan" | Pricing page screenshot, cursor on the Pro plan | instruction -> screenshot | "$20" on screen 2.55 s before the word |
| 332.8 | "watch how other editors are using Claude to edit videos" | His own YouTube tutorial page, playing | instruction -> screen recording | 0 |
| 349.8 | "watching a bunch of tutorials on how people are using Higgs Field" | Row of real tutorial thumbnails scrolling left | "a bunch" -> scrolling row | 0 |
| 356.8 | "how Claude, Remotion and Higgs Field all work" | Three logos appear on his chest, one per name | list -> one icon per name | +0.06 s, +0.38 s |
| 368.4 | "looking at what's happening in the script" | Script lines right of his head, phrases get blue highlights, then icons | process -> show the script | 0 |
| 377.4 | "gathering a bunch of inspiration that I really like" | Pinterest board zooms up from a thumbnail | instruction -> real example | 0 |
| 382.4 | "typography, colors, layouts and effects" | Four words along the bottom, one per word | list -> items as named | -0.21 to +0.71 s |
| 387.1 | "analyze how the text behaves ... what kind of fonts" | Words move to the top as tabs; typography example with labels | list item -> annotated example | 0 |
| 406.0 | "starting to use remotion to build out high-quality designs inside of Cloud" | Claude chat window, prompt types, image result appears | action -> UI demo | 0 |
| 421.0 | "take a still design and turn it into a high-quality animation" | Card left, arrow over his head, animated card right | before/after -> two cards + arrow | 0 |
| 432.2 | "what kinds of animations are being used on the text" | Hand-written labels "pop up fading", "blur slide-in", "soft light drift" with arrows | list -> annotations as named | 0 |
| 456.8 | "if you've made it to Day 10 ... most people quit on Day 2 or 3" | Plain speaker, slow zoom total x1.31 over 9.5 s | direct address -> face only | - |
| 468.6 | "Since you've mastered typography ... create high-quality captions for this clip" | Script panel + clip; caption chip appears; highlights | steps -> workspace mock | 0 |
| 496.5 | "turning these edits from basic videos into better and better videos" | Zoom-out x0.71 over 2.6 s; cards pop in around him | "better and better" -> more and more cards | 0 |
| 508.0 | "find eight viral videos that really impress you" | Eight phone cards fill a row | number -> that many items | 0 |
| 512.0 | "going to Instagram, finding a bunch of editors" | Instagram logo, then four profile grids | named site -> logo + screenshots | 0 |
| 565.0 | "the main focus on day 20 ... create a wow edit" | "Day 20" circle + pill "You need to create a wow edit" | new section -> section card | +0.03 s |
| 597.2 | "Is this edit worth clients paying me money for it?" | Speaker left, phone card right, caption under the card | self-question -> caption beside the example | +0.24 s |
| 622.9 | "The first thing you have to do is find prospects" | Speaker; caption "1. Find prospects." | step -> numbered caption | -0.05 s |
| 648.2 | "send them a quick message say, Hey, I spent the last few days..." | Message types in a chat field, sends | quoted message -> typed chat | 0 |
| 656.2 | "Don't offer anything ... Just give them free value" | Speaker; caption, "free value" larger and blue | rule -> caption | -0.37 s |
| 672.4 | "text that says POV, your client paid you for a viral edit" | Blank phone card, the text types on it | description -> build the thing | -0.07 s |
| 684.6 | "every single day you find one new prospect" | Ten numbered tiles become ten person icons, then ten edit cards | count -> ten items | 0 |
| 708.9 | "at least one of your trendy formatted videos" | Phone clip, arrow, counter to "$2,000/month" | outcome -> counter | not spoken |
| 716.6 | "there is a lot of money that can be made" | Dollar amounts scattered around him | vague amount -> many numbers | +1.7 s |
| 728.5 | "$30 to $100 per short form video" | Cards blur; pill "$30 to $100" | number -> pill | +0.13 s |
| 733.6 | "you could easily make $1000 to $1500 in a single week" | Camera pulls out (x0.52) to a grid of 30 cards each tagged "$50"; header total | multiplication -> grid + total | -0.01 s |
| 766.4 | "they don't have a community of people supporting them" | One person tile in the middle, the people around it fade; "No community." | absence -> icons fade | text about 0 |
| 779.7 | "making $2000 to $4000 per month" | Counter runs up to "$4,000/month" among post cards | number -> counter | +1.54 s |
| 836.8 | "lifetime access for just $299" | Price card: $1,200/year struck through, then $299 | price -> price card | +0.31 s |
| 840.4 | "Join Ultimate Editors 2.0. The link is down below." | Speaker; CTA pill stays to the end | CTA -> button | +0.65 s |

## 8. Why each cut is there

Sample: every 5th row of `timeline.md` from #5 to #295 (59 cuts).

| Reason | Count | Share | Two examples |
|---|---|---|---|
| End a graphic and return to the speaker (always at a sentence start) | 15 | 25% | #20 62.57 "The fundamental thing that you have to understand"; #190 589.97 "Then you can go and execute it using AI" |
| List item (new card, clip or label for the next item named) | 12 | 20% | #10 18.07 second student's post; #80 255.90 "minimal animations, SAS trainers" |
| Start a graphic (at a sentence start) | 8 | 14% | #105 329.17 "I would first go and sign up for the subscription"; #205 634.63 "Once you found that prospect" |
| New sentence on the speaker (join between takes) | 6 | 10% | #70 224.77 "So how do you learn video engineering?"; #160 500.40 "This is why" |
| Other: a change inside an animated graphic counted as a cut | 6 | 10% | #35 107.57 result card swaps; #110 343.63 the video inside the screen recording changes |
| Measurement artefact (shot shorter than 0.35 s, the blurred frames around a transition) | 5 | 8% | #85 274.43 (0.07 s); #240 712.23 (0.33 s, blur-out before the cut at 712.57) |
| Emphasis word | 4 | 7% | #30 94.10 tile turns blue on "video editor"; #155 485.17 background goes dark on "the fundamental objective is" |
| Section change | 2 | 3% | #100 312.87 Day 1-3 card; #285 821.57 white flash before the next module of the offer |
| Demo step | 1 | 2% | #200 625.43 typing in the Instagram search |
| Hide a jump cut only / pattern break only | 0 | 0% | none in the sample had this as its only reason |

Taking out the 11 artefact and in-graphic rows, 48 real cuts remain: 23 are speaker/graphic switches, 12 are list items, 6 are take joins, 4 are emphasis, 3 are section or demo steps.

Longest stretches with no cut (from `shots.json`):

| Start | Length | Picture | What is said |
|---|---|---|---|
| 40.07 | 18.2 s | Agenda graphic, animating the whole time (three headers, diagrams, roadmap, counter) | "First, I'm going to show you why you get paid ... $2,000 per month with AI video editing" |
| 786.80 | 14.6 s | Offer: tagline text, then the five style tiles | "step program to turn you into a viral editor ... the viral talking head style" |
| 468.60 | 13.5 s | Script and clip workspace | "Since you've mastered typography ... turn these designs into high" |
| 196.37 | 11.4 s | Speaker, with a chip, an unlisted punch-in at 200.93 and a card wall from 203.9 | "That's not your client's responsibility ... make better" |
| 634.63 | 11.3 s | Prospect's clip, brand board, finished edit | "Once you found that prospect ... their raw videos and their brand" |
| 274.83 | 11.1 s | Masterclass cover with skill tiles | "Joseph AI editing masterclass ... long form AI editing skills" |
| 156.23 | 10.7 s | Speaker close (face 49%), one small card at 163 s | "This is why it's so stupid to pretend that video editing is dying ..." |

Longest speaker stretch without leaving to a graphic: 17.8 s (149.2-166.9 s), three shots. Longest graphic stretch without the speaker: 54.0 s (779.7-833.7 s, the final offer); next 24.1 s (520.4-544.5 s) and 23.6 s (387.1-410.7 s). The plainest long shot is 456.8-466.3 s (9.5 s of speaker with no overlay until the last second).

## 9. On-screen text and captions

There are no running captions. Text appears only where the editor chose a sentence.

| Kind | Size (% of frame height, OCR line box) | Position | Colour | Case / weight | Words | Animation | Stays | Repeats speech? Timing |
|---|---|---|---|---|---|---|---|---|
| Key-sentence caption on the speaker | median 4.8% (3.9-6.5%) | centred, y 0.87; one line, sometimes two | white (#e6e5e9 to #eeeef0); 1-3 key words light blue (about #84b4da to #93cdfb) and bolder | sentence case, light weight | median 7 (3-12) | words fade in one at a time from blur, 3-4 frames each; lower frame darkens under it; fades out with the shot | median 2.0 s (1.0-3.4 s) | word for word, slightly tidied ("gonna", "In a moment I'll show you exactly how"); each word within about 0.2 s of speech (dense 1.5: "now" said 1.94, shown 1.97-2.00; "most" said 2.58, shown 2.53). 25 instances in 14 minutes |
| Numbered step caption | 5.4-6.5% | same place | white, key word blue | sentence case | 3-5 | same | 1.3-3.0 s | paraphrase: "1. Find prospects." (622.9), "Step 2: Upload your edit." (663.7) |
| Statement on light canvas (G1) | 6-9% | centred, y 0.3-0.55; later moved to y 0.11-0.26 as a header at 4.5-5.9% | dark grey (#1b1b21 to #262523); key words blue (#2249a0 to #264bb3), bold | sentence case, light with bold key words | 5-12 over 1-3 lines | word by word from blur; exits by letters scattering or by shrinking to the top | 2-4 s, headers up to 9.6 s | word for word; within 0.1 s per word (dense 23.8) |
| Quote on dark (G11) | 6.7-7.0% | centred, y 0.46 and 0.55 | off-white (#d6d6d7 to #e8dfde), key words light blue | sentence case | 4-9 per line | word by word while the background blurs and darkens | 2.5-3 s | word for word; -0.04 to +0.16 s |
| Big title behind speaker | 14.2% | top, y 0.14, behind his head | white, "AI" blue | sentence case, medium | 6 | word by word | 1.4 s | word for word, -0.13 s. Used once (32.6 s) |
| Chapter title | 12.6% title, 6.3% subtitle | centred, y 0.44 and 0.57 | white title; light-blue subtitle (#7a9ab5) on #08080f | title case, semi-bold title | 2 + 4 | title fades from blur in 8 frames; subtitle word by word | 3.0 s | subtitle paraphrases the line, +0.41 s. Used once |
| Section card text (G13) | "Day" 6-7.6%, label 4.1-5.9% | centred, y 0.44-0.50 | "Day" grey (#747474), number blue, label dark (#232328 to #28282d) on white pill | title case | 2-4 in the label | pills slide up, label fades in | 3-6 s | label repeats the spoken topic, +0.4 to +0.8 s |
| Big number | 11-19% | centre or right-centre | blue (#2151cd, #214dc3) on light; light blue (#93ccfc) on dark | digits bold, unit small and grey | 1 | counts up or fades in | 0.8-3.3 s | number is spoken in most cases; lag +0.1 to +1.5 s |
| Labels inside graphics | 3-6% | next to their object | blue for headers (#204cd3), grey for small labels | sentence case | 1-4 | fade in with the object | as long as the object | names the object; within about 0.5 s |
| Hand-written annotations (G16) | 5-7% | beside the example, with curved arrows | dark grey (#535251) | lower case, script hand | 1-5 | write on | 2-8 s | paraphrase of each list item as it is said |
| Floating lines by the speaker (G26) | 5-7.4% | left or right of the head, y 0.16-0.49 | white and light blue | sentence case | 4-7 | word by word; older lines blur back | 1-3 s | word for word, -0.8 to +0.9 s |
| CTA pill | 3.6-3.9% | centred, y 0.84 | dark text, blue underlined "down below" (#2848a6) on a white pill | sentence case | 5 | fades in, cursor moves | 2.0 s and 5.8 s | repeats the line, +0.65 to +0.81 s |

Typeface: a geometric sans-serif (round "o", single-storey "a") is used for all of the editor's own text; its name cannot be read from frames. Summary numbers for all OCR text: 35% of tracks repeat spoken words; first appearance is a median 0.35 s after the word (p10 -0.47 s, p90 +1.78 s); 20% of tracks grew while on screen (the word-by-word builds).

## 10. Transitions

| Kind | Frames | What happens | Where |
|---|---|---|---|
| Blur-dip cut (the default; counted as "hard" in the JSON) | out 2-4 frames, in 5-12 frames | Outgoing picture blurs for a few frames, straight cut, incoming picture starts heavily blurred and slightly small and sharpens while scaling to size | Graphic to speaker: 58.30 (out 4 f, in 6 f), 128.63 (out 3 f, in 6 f), 32.63 (in 12 f), 712.60 (out 2 f, in 3 f). Speaker to graphic: 64.63, 134.07, 329.17. Speaker to speaker: 177.37 (out 4 f, in 5 f) |
| White wipe rising from the bottom | 24-33 frames (0.8-1.1 s) | A soft-edged off-white field climbs from the bottom while the speaker blurs; the first graphic elements ride up with it | The standard speaker-to-canvas move: 40.0-40.8, 191.7-192.3, 208.9-209.2, 312.5-313.6 (dense), 386.7-387.2, 502.2-502.4, 520.3-520.5, 574.9-575.6, 666.5-667.2, 684.4-684.7, 702.5-702.7, 719.2-719.4, 755.8-756.2, 766.3-766.5 |
| Blur dissolve | 19 frames (0.63 s) | Speaker blurs, lightens and dissolves into the canvas | 119.83-120.47 (dense) |
| White bloom flash | into white 12 frames, white held about 10 frames, out 10-12 frames; about 0.8-1.0 s in all | Picture blooms to white or pale lavender from the centre, next picture fades out of the white | 4.50-5.30 (dense), 230.87-231.90 (dense), 783.8-784.5, 801.4-802.2, 821.6-822.2. Used for the opening and around the two offers |
| Darken and blur under text | 13 frames to about 1 s | Current picture blurs and drops to near black, text builds on top | 59.50-59.93 (title), 108.2-109.3 (quote), 184.2-185.6, 485.1-486.1 |
| Plain punch cut | 1 frame | Instant scale jump on the speaker, no blur | 1.77 (x1.204), 34.10 (x1.111), 698.13 (x1.181), about 200.93 (x1.25) |
| Virtual camera move inside a graphic | 8-70 frames | Canvas zooms or slides to the next area; cards re-flow | 68.2-70.5 (x0.565), 92.43-93.37 (x1.61), 377.07-378.03 (about x3), 618.97-619.77 (x0.735), 733.6-735.4 (x0.515), 744.97-746.50 (x0.30) |
| Pop / fade-in of an element | 8-14 frames | Card or chip fades in from blur with a small scale-up | 14.77-15.20 (dense), 199.7-200.0 |
| In-card swap | 1-3 frames | The clip inside a phone card changes | 75.63 (dense), 28.4-32.6, 292-300 |

No slide, spin, glitch or whip transitions between scenes were seen.

## 11. Sound

**Music.** A bed is audible for 98% of the runtime (0-355 s and 360-850 s; one gap of about 5 s at 355-360 s, where "by the end of that three day phase" is said). Level is a median 24.7 dB below the voice (p10 -33.6, p90 -18.0). By 30-second block it sits between -30.2 dB (360-390 s) and -19.0 dB (810-840 s); the last 60 seconds are the loudest (-19.0 to -21.4 dB). The files report the bed 5.3 dB higher inside voice pauses (-19.6 dB) than under speech (-24.9 dB), but the pauses are at most 0.22 s long, so this is not good evidence of side-chain ducking (section 13).

**Sound events.** 425 candidates (30.1/min), 368 strong (26.1/min). Strong events are a median 7.8 dB below the voice and 0.23 s long. By band: 205 broadband only, 168 broadband + low, 52 low only. Strong events are denser over graphics (29.9/min) than over the speaker (19.8/min).

The 24 strongest (all within 3.2 dB of the voice), checked on frames in `dense/sfx_top_1.jpg` and `dense/sfx_top_2.jpg`:

| Time | Level vs voice | Band | What is on screen at that instant |
|---|---|---|---|
| 30.39 | -1.8 dB | BB+LOW | Phone-card carousel: the card swaps to a new design |
| 40.30 | -3.1 dB | LOW | White wipe rising over the speaker into the agenda graphic |
| 92.95 | -0.5 dB | BB+LOW | Virtual camera pushing into the person icon tile ("That person") |
| 123.74 | -2.9 dB | BB+LOW | Icon and sentence slide up to make room; clip card fades in below |
| 135.27 | -3.2 dB | BB+LOW | Arrow draws from the stacked cards to the result card |
| 211.33 | -3.0 dB | BB+LOW | "the dream editor" headline shrinks and moves to the top; clip card fades in |
| 267.59 | -2.7 dB | BB+LOW | "AI Editing Fundamentals Course" title starts to move up |
| 293.55 | -3.2 dB | BB+LOW | Header line scrambles from one sentence to the next; card row swaps |
| 331.31 | -0.6 dB | BB+LOW | Static pricing screenshot; cursor near the Pro button (button highlights about 0.4 s later) |
| 341.04 | -0.5 dB | LOW | Speaker talking, nothing changes |
| 350.64 | -0.1 dB | LOW | Thumbnail row scrolling steadily, nothing discrete |
| 377.43 | -3.2 dB | BB+LOW | Pinterest board zooming up from a small thumbnail |
| 468.35 | -2.6 dB | BB+LOW | Just before the script panel slides in beside the clip (468.5) |
| 513.00 | -2.9 dB | BB+LOW | Instagram logo moves up; first profile grid fades in |
| 518.36 | -2.3 dB | BB+LOW | Row of cards re-sorting along the bottom of the speaker shot ("rank them") |
| 524.74 | -2.3 dB | BB+LOW | Transcript text finishing beside the clip; cards starting at left |
| 527.05 | -1.5 dB | LOW | Virtual camera pushing in on the clip and transcript |
| 537.59 | -2.0 dB | BB+LOW | Virtual camera pulling out from one annotated card to the board |
| 619.12 | -3.0 dB | BB+LOW | Day 21-30 card shrinking and moving down as the camera pulls out |
| 654.25 | -2.2 dB | BB+LOW | Typed message being sent (blue bubble appears at 654.35) |
| 686.06 | -2.9 dB | BB+LOW | Row of ten person icons moving up; first edit card fades in |
| 786.80 | -3.1 dB | BB+LOW | Course thumbnail shrinking to the top; tagline starts |
| 801.71 | -1.5 dB | LOW | White bloom flash between offer modules |
| 836.40 | -2.2 dB | BB+LOW | Circle being drawn around "November 15th" in the caption |

So 21 of the 24 strongest sit on a movement inside a graphic (a camera push or pull, a re-flow, a wipe, a send, a drawn circle). Three (331.31, 341.04, 350.64) have nothing matching on screen; two of those are low-band only with a 20-30 ms attack, which fits a drum or bass hit in the music.

**Which picture events get a sound.** By cut kind: hard 44%, punch 25%, transition 22%, pop 21%, jump 18%, against 10% by chance. So returns to the speaker and scene changes (the blur-dip cuts) get a sound a little under half the time; multi-frame transitions and pops about one time in five; the rest pass silently. 63% of strong events are not within 0.12 s of any detected cut or motion event; from the table above many of those are on moves inside graphics that the cut detector does not list, and some are music.

**Silences.** None. Voice is active 95.1% of the time and the bed fills the rest.

## 12. Rules to reproduce this edit

1. Cut the speech until no pause is longer than 0.22 s; aim for a median pause of 0.14 s and about 5.5 pauses per minute. Target 260-280 wpm in the final cut.
2. Keep the speaker on screen for about 38% of the runtime and graphics for about 62%.
3. Change the picture every 3.8 s on median; let 10% of gaps run past 9.8 s; never hold one unchanging picture past about 21 s.
4. Keep speaker stretches to a median of 4.6 s and a maximum of about 18 s before going to a graphic.
5. Frame the speaker centred: face 37.5% of frame height, face centre at x 0.50, y 0.38.
6. Start every speaker shot blurred and at about 92% scale; sharpen over 5-12 frames while scaling up x1.086 in 0.33 s.
7. End a speaker shot that leads to a graphic with a x1.107 push over the last 0.33 s while blurring out.
8. Between the entry and the exit, hold the frame still, or add a slow push of 1.3% per second on shots that carry a caption.
9. Use an instant punch-in of x1.11 to x1.20 on the sentence that states the stakes or the promise (3-4 times in 14 minutes).
10. Use a punch-out of x0.81 to x0.87 through a blur dip (4 frames out, 5 frames in) on a pivot sentence ("So...", "After...", "Now...").
11. Before overlays appear around the speaker, zoom out x0.71 to x0.90 over 0.5-2.6 s and dim the background.
12. Switch between speaker and graphic only at the start of a sentence (23 of 48 real sampled cuts).
13. Go from speaker to canvas with a soft white wipe rising from the bottom over 24-33 frames (0.8-1.1 s).
14. Go from graphic back to speaker with a blur-dip cut: 2-4 frames of blur out, cut, 5-6 frames of blur in.
15. Keep the white bloom flash (about 0.8-1.0 s) for the opening and for entering or leaving an offer block.
16. Build all graphics on one canvas: off-white #ebeae9 with a faint grid and a soft blue centre glow; one accent blue around #2151cd; body text dark grey around #222; white rounded cards with soft shadows; flat 2D only.
17. Put every example clip inside a portrait phone card; never cut to it full frame.
18. For a list, add one item per named word, within about 0.3 s of the word (12 of 48 real sampled cuts are list items).
19. For a process, draw a flow diagram left to right: source card, dashed line, icon tile, result card, each on its phrase; then push the camera x1.6 in 0.9 s into the element being named.
20. For a number, show it at 11-19% of frame height in blue, or count up to it in about 1.7 s, easing out.
21. For a count ("eight videos", "ten days", "20 to 30 videos"), show exactly that many items.
22. For proof, show a real screenshot or screen recording in a rounded window for 2-5 s, with a x1.08-1.12 push at the start and end.
23. Mark each section of a multi-part plan with the same card (two circles "Day N" joined by a labelled pill), held 3-6 s.
24. Do not run captions. Caption about 25 chosen sentences: white, 4.8% line height, centred at y 0.87, 7 words on median, word by word in sync (within 0.2 s), 1-3 key words in light blue, on screen 2.0 s, with the lower frame darkened.
25. For the single biggest claim of a section, clear the screen and build the sentence word by word on the canvas at 6-9% height, key words bold blue, each word within 0.1 s of speech.
26. For a maxim or the central question, blur and darken the current graphic over about 1 s and set two centred lines of white text on it for 2.5-3 s.
27. Make text enter one word at a time, each resolving from blur in 3-4 frames; make cards fade in from blur with a small scale-up over 8-14 frames.
28. Keep a music bed under the whole video about 25 dB below the voice, rising to about 19-21 dB below in the last minute.
29. Add a short sound (about 0.23 s, about 8 dB below the voice) on moves inside graphics and on scene changes: aim for about 26 per minute overall, about 30 per minute over graphics and about 20 per minute over the speaker; cover roughly 44% of scene-change cuts and about 20% of pops and transitions.
30. Put the loudest sounds (within 3 dB of the voice) on camera pushes and pulls inside graphics, wipes, and "send" or "circle" actions.

## 13. Not determinable / measurement problems

Measurement problems found by checking the JSON against frames:

1. **Picture class is wrong for 25% of the runtime.** `picture_share_of_runtime.face = 0.644`, but 213.5 s of "face" shots are light-canvas graphics with someone else's face in a phone card (for example #25-#29 at 82.9-94.1 s, #42 at 120.2 s, #46 at 138.7 s, #67 at 209.1 s, #152 at 468.6 s, #170 at 527.3 s). True speaker time is about 317 s (37.5%).
2. **Camera-move shares include those graphics.** `share_of_face_time_by_move` ("eased zoom in 59%") and `eased_zoom_moves.n = 280` mix speaker shots with virtual camera moves inside graphics. On true speaker shots there are 117 zoom moves: 58 at shot start, 40 at shot end, 19 mid-shot.
3. **"Eased zoom in" on the speaker is mostly the entry settle and exit push,** not a move during the sentence. The shot-level label hides that the middle of the shot is still.
4. **"Hard" cuts are mostly not plain cuts.** The ones dense-checked (32.63, 58.30, 128.63, 712.60) all have blur on both sides.
5. **"Jump" over-counts.** #23 at 75.63 s is an overlay card swap, not a cut in the speaker footage. #54, #78, #83, #85, #253, #256, #281 are 0.07 s (2-frame) shots made of blurred transition frames; #33, #91, #148, #220, #221, #255, #257 are 0.1 s or less.
6. **A punch-in is missing from the cut list.** About 200.93 s the speaker jumps about x1.25 between two frames; the JSON records it as a zoom move 200.73-200.97 inside shot #65.
7. **Face boxes on graphics are not the speaker.** `h_end_over_start` 3.771 (#169) and 0.282 (#276), face height 83% (#171) and 65% (#25-#26) are card faces. Face x 0.746 at 544.5 s is the man in the card; the speaker is on the left.
8. **Zoom factors on graphics are unreliable** as the brief warns: x3.02 on #120, x0.30 on #252.
9. **OCR text includes things that are not the editor's typography:** the "RODE" logo on the microphone (logged at 11-15% height about 20 times), text inside example clips ("Brain fog", "focus", "MITOCHONDRIAL", "ESCAPE"), and web-page text in screenshots. `text.big_per_min = 30.6` and the size and colour statistics are inflated by these. Caption numbers in section 9 come from a filtered subset (dark background, lower third, 3+ words).
10. **OCR colours and strings are wrong during fades:** the white title at 32.6 s is logged as #7b7b7b; scrambling text is logged as nonsense ("tos a tvd oeditng.").
11. **Text size** is the OCR line-box height, which includes ascenders and descenders; letter height is smaller. I could not measure cap height reliably.
12. **Music ducking.** `duck_dB = 5.3` compares speech with pauses of at most 0.22 s; it may be stem-separation leakage. Whether the bed is ducked cannot be told.
13. **Sound events include music.** 341.04 s and 350.64 s (both at the level of the voice, low band only) have no picture event. The number of real sound effects is lower than 425; how much lower cannot be told.
14. **Transcript errors:** "Cloud" for Claude (406-410 s, 440 s), "Hicksfield" / "Higgs Field" for Higgsfield, "SAS trainers" for SaaS trailers, "new rock clip" for raw clip (466 s), "bureau segments" for b-roll (587 s), "Iman Gadji". Word times are still usable.
15. **Section 8 reasons** are my reading of the timeline row plus the shot sheet, not a measurement; only the cuts named in section 10 were checked frame by frame.

Not determinable from the evidence:

- The names of the typeface, the music track and any sound effect; what each sound is (whoosh, click, riser).
- Whether the voice was sped up, or how many takes and cuts are hidden under the 62% of runtime covered by graphics.
- Whether the blur and scale at shot starts are done in the editing program or rendered with the graphics (the video says at 274.8 s that it was edited with the creator's own AI "long form" skill; the frames cannot confirm the tool).
- Exact blur radius and easing curves; only frame counts and start/end scales were measured.
- Colour grade settings on the speaker footage; only the dominant colour (#0c0d0e) is known.
- Whether the same sound is reused for the same kind of move.
- Exact timing of the 14 white-wipe transitions other than 312.5 s and 40.0 s; the rest are read from shot-sheet tiles.

Dense sheets built and read (in `dense/`): t1.5 (punch-in, caption build), t4.4 (white bloom), t5.73 (collage build), t14.6 (card fade-in), t23.8 (text build), t32.5 (blur-dip + title behind head), t58.1 (graphic to speaker), t59.4 (chapter title), t75.2 ("jump" check), t92.4 (camera push, strong sound), t107.4 (dark quote), t119.7 (blur dissolve), t128.3 (graphic to speaker), t177.1 (punch-out with blur dip), t198.4 (zoom-out for chip, unlisted punch), t230.6 (white bloom), t312.5 (white wipe, day card), t330.9, t340.6, t350.2 (strong sounds), t496.3 (long zoom-out), t710.6 (counter), plus sfx_top_1 and sfx_top_2 (six frames around each of the 24 strongest sound events). t17.2 was built but not read.
