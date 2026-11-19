# Edit analysis: kallaway-dopamine-ladders

"How to Become a Storytelling Genius (Dopamine Ladders)", Kallaway, 22:26, 23.976 fps, 1920x1080, 687,550 views.

Sources: `summary.json`, `shots.json`, `text.json`, `audio.json`, `words.json`, `timeline.md`, all 19 shot sheets, 30 dense 24 fps sheets in `dense/` (t0.3, t2.6, t7.0, t23.8, t28.0, t48.4, t62.4, t64.0, t71.3, t82.0, t84.4, t92.6, t96.7, t104.9, t106.3, t113.9, t146.0, t155.8, t280.0, t331.9, t520.6, t561.9, t586.9, t639.0, t769.7, t808.4, t1054.9, t1166.0, t1286.9, t1288.6), single full-size frames, and two extra checks run on the source file: (a) a background feature match between frame pairs to measure true camera scale, (b) a scan of every frame for black frames. All times are seconds from the start unless written m:ss.

Words used below: "speaker" = the talking-head footage. "Canvas" = the dark graphic background. "Level" = one step of speaker scale (see section 4).

---

## 1. Facts

| Measure | Value | Source |
|---|---|---|
| Length | 1345.05 s (22:25) | summary.json |
| Frame rate | 23.976 fps, 1.2% duplicate frames | shots.json |
| Detected cuts | 170 total, 7.6 per min | summary.json |
| Cuts per min by kind | hard 3.4, jump 1.3, punch 1.3, pop 0.8, transition 0.8 | summary.json |
| Cut counts by kind | hard 76, jump 29, punch 29, pop 19, transition 17 | summary.json |
| Shot length | median 4.92 s, p10 0.83 s, p90 17.1 s, max 89.3 s | summary.json |
| Time between changes of picture | median 7.95 s, p90 30.2 s | summary.json |
| Transition length | median 0.5 s, p90 0.9 s | summary.json |
| Runtime share: speaker | 61.2% (823.8 s) | summary.json |
| Runtime share: full-screen graphic / clip / screen recording | 38.5% | summary.json |
| Speaker time with overlay text on it | 241.6 s = 29% of speaker time = 18% of runtime | text.json tracks over face shots (hoodie print excluded) |
| Speaker segments / graphic segments | 40 / 39, median length 9.5 s / 9.8 s | shots.json |
| Speech rate | 225 wpm overall, 253 wpm while speaking, 5054 words | summary.json |
| Voice active | 89.2% of runtime | summary.json |
| Pauses (voice stem) | 472, 21.1 per min, median 0.23 s, p75 0.28 s, p90 0.33 s, max 3.26 s | summary.json |
| Pauses over 0.5 s / 1 s / 2 s | 8 / 7 / 5 (all between 1067 and 1166 s) | audio.json |
| Speech run between pauses | median 1.27 s, p90 3.17 s, max 5.6 s | summary.json |
| Loudness | -14.2 LUFS integrated, LRA 1.8 LU, true peak -0.4 dBTP | summary.json |
| Music bed level | median -47.6 dB below voice (p90 -41.0 dB); 8% of runtime flagged audible | summary.json |
| Sound-event candidates | 648 (28.9 per min), of which strong 63 (2.8 per min) | summary.json |
| Strong events: level and length | median -4.6 dB relative to voice, median 0.2 s | summary.json |
| Strong events on a picture event | 43% (chance 7%) | summary.json |
| Big on-screen text tracks | 267, 11.9 per min; median 2 words, on screen 3.0 s median | summary.json |
| Text height (OCR box) | median 4.2% of frame height, p90 6.3% | summary.json |
| Text that repeats spoken words | 30%; median +0.2 s after the word | summary.json |
| Face height | median 31% of frame height (p10 29%, p90 35.5%); centre x 0.51, y 0.37 | summary.json |

Per chapter (summary.json):

| Chapter | Start | Cuts/min | Speaker share | Big text/min |
|---|---|---|---|---|
| Intro | 0 | 13.8 | 52% | 22.5 |
| What is the Dopamine Ladder | 48 | 10.7 | 69% | 11.6 |
| Level 1 Stimulation | 115 | 5.1 | 77% | 4.7 |
| Level 2 Captivation | 256 | 4.6 | 78% | 12.5 |
| Level 3 Anticipation | 453 | 10.4 (movie clip) | 81% | 9.4 |
| Level 4 Validation | 626 | 7.0 | 39% | 28.1 |
| Level 5 Affection | 720 | 7.3 | 56% | 19.7 |
| Level 6 Revelation | 909 | 6.1 | 90% | 6.6 |
| Live Example | 1036 | 5.1 | 28% | 3.4 |
| Summary | 1282 | 21.9 (screen recording) | 37% | 21.9 |

The first 48 s are cut about three times faster and carry about four times more text than Levels 1 and 2.

---

## 2. Script structure

| Start | Beat | What is said (short) | How the edit marks it |
|---|---|---|---|
| 0.0 | Hook | "If you want to get people truly addicted to watching your content, there's one trick" | No intro card. Opens on the speaker mid-gesture; at 0.47 the speaker frame starts shrinking into a rounded card on the purple canvas and avatar icons pop around it (dense t0.3). |
| 3.9 | Name the idea | "It's called the dopamine ladder" | Card drops out 3.3-3.9, one node glows, sentence types at top; 7.0-7.75 fast zoom-out reveals the ladder with labels "Dopamine" / "Ladder" (dense t2.6, t7.0). |
| 8.7 | Payoff + credibility | "you'll become a master of attention overnight... a million followers... billions of views" | Hard cut to speaker; sentence types beside him 10.5; two counter badges 16.4-18.7 (frames 16.6, 17.7). |
| 24.1 | Promise / agenda | "the six levels... how it works, why it works... tactics" | Hard cut to empty canvas at 24.13, ladder assembles 24.3-25.4; three snap reframes (28.83, 29.82, 31.36), one phrase typed per item. |
| 35 | Set-up | "before I explain... the psychology of how attention actually works" | Still on ladder ("What is the Dopamine Ladder?"), cut to speaker 41.04, ladder again 46.9 with "Level 1..6" labels. |
| 57.6 | Goal | "you will create a Pavlovian effect" | Zoom-out 62.27, "PAVLOVIAN EFFECT" behind the head 62.69-64.6; Pavlov illustration 67.2-79.2. |
| 82.2 | Stakes | "the ultimate sign of attention mastery..." | First lower-third caption 83.0-93; two punch-ins in a row at 97.01 and 99.93. |
| 105.4 | Bridge question | "what are the six levels and how do you make your content..." | One black frame at 105.36, speaker blurs and dims 106.5-106.9, question typed in the centre until 114.6. |
| 116.0 | Level 1 Stimulation | "the very first rung... is called stimulation" | Ladder title card 116.0-125.8 (see below). |
| 256.4 | Level 2 Captivation | "level two... is called captivation" | Ladder title card 256.4-259.8. |
| 454.0 | Level 3 Anticipation | "level three... is anticipation" | Ladder title card 454.0-465.4. |
| 626.9 | Level 4 Validation | "level four is called validation" | Ladder title card 626.9-630.7. |
| 693.3 | Recap of 1-4, message vs messenger | "these are kind of like the base levels" | Ladder with four labels, bracket "The message", then "The messenger". |
| 717.9 | Level 5 Affection | "Level five is called affection" | Same ladder shot snaps up to rungs 5/6 at 717.88; speaker from 721.7. |
| 853.8 | Recap of 1-5, then Level 6 Revelation | "let's just recap where we were" | 61 s on the ladder with a description list; "Revelation" label at 911.9; speaker from 915.1. |
| 1037.5 | Live example | "one live example of an actual short form video" | Punch-out at 1037.45; at 1055.2-1056.2 the speaker shrinks to a small card and a vertical clip plus a checklist appear. |
| 1283.7 | Summary | "that is all I've got... As a recap" | Punch-out 1283.7, ladder with all six labels 1286.2-1295.6, ladder + "Your goal:" 1299.1-1312.1. |
| 1312.1 | CTA | "free community called Wavyworld" | Speaker, then screen recording of the community 1321.0-1338.7 with URL pill "skool.com/wavyworld". |
| 1338.7 | Sign-off | "free invite link below... see you on the next video. Peace." | Speaker; subscribe lower third 1341.5-1344.7; picture darkens in the last 0.33 s (shot #170). |

**How every level change is marked** (same recipe six times): the speaker closes the previous level with a one-line recap ("So that's level two of the dopamine ladder", 421.6); the picture hard-cuts to the ladder graphic within 0.2 s of the words "All right"; the camera moves up one rung; the level name appears in violet with "Level N" under it; a low sound lands on the camera move (116.83, 717.84, 860.24, 911.99); 3-11 s later a hard cut returns to the speaker at the widest framing for the definition sentence.

**Most-replayed moments** (`heatmap`, 100 bins of 13.45 s, value 0-1):

| Rank | Time | Value | What is on screen / said |
|---|---|---|---|
| 1 | 444-458 | 1.00 | End of Level 2 "pro tips" (two "?" icons with side labels) and the Level 3 ladder title card at 454.0. The chapter mark "Level 3" is at 453. |
| 2 | 1063-1077 | 0.86 | The example clip has just appeared (1056); checklist appears; speaker stops talking for 2.6 s at 1067.9 while the clip plays; "the first step... is stimulation". |
| 3 | 310-323 | 0.81 | Flow diagram: phone -> comment "I wonder when the aliens are visiting earth?" -> "Curiosity Inducing" -> branch -> red "Viewer leaves". |
| 4 | 498-512 | 0.77 | "The highest level of dopamine is achieved just before the answer comes" - punch-in at 499.6, lower-third caption 504.6-512.6. |
| 5 | 296-310 | 0.74 | Side labels: "Bigger + More non-obvious question" (left) -> "Bigger curiosity + Higher stakes + More dopamine" (right). |
| 6 | 512-525 | 0.68 | "head fake... reset the curiosity loop"; zoom-out at 520.8 before the loop ring appears. |
| 7 | 485-498 | 0.60 | Head silhouette with "?" (483-492); "the more information you give..." |
| 8-16 | 256-296, 323-350, 471-485, 1077-1104, 915-929 | 0.51-0.53 | Start of Level 2, "CURIOSITY LOOP" title, the two tactic questions in bubbles, start of Level 3 body, the viewer-questions typed beside the example clip, start of Level 6. |

Replay is concentrated in Level 2 and Level 3 (256-525 s) and at the start of the live example. Three peaks sit on chapter marks (256, 453, 909), so part of this is viewers jumping to chapters; the data cannot separate that from re-watching. The curve is lowest in the last 2.5 minutes (0.00-0.15 from 1210 s).

---

## 3. The rough cut

- **Speech is continuous.** Median pause 0.23 s, 90% of pauses under 0.33 s. In the first 17:47 there is no pause longer than 0.5 s. The eight pauses over 0.5 s (0.84-3.26 s) are all at 1067.9-1166.8 where the speaker deliberately stops to let the example clip play.
- **Pace.** 225 wpm overall; the 30 s windows range 190-258 wpm. Speech runs between pauses are short (median 1.27 s, max 5.6 s).
- **Cuts sit in the gaps.** 66% of same-picture cuts and 55% of picture changes fall inside a voice pause (chance 12%). 33% of same-picture cuts come right after a sentence end.
- **How speaker-to-speaker cuts are treated** (98 speaker shots):
  - 27 **punch cuts** on the speaker: an instant scale change of one level (x1.047 in or x0.954 out; one of x1.095 at 620.91). All 27 land at a sentence or clause start (examples: 97.01 "This is when you reach King status", 143.27 "Now, dopamine from stimulation comes from", 235.03 "This is why coming up with your own unique visuals", 838.71 "So likability is one of those things"). These hide the cut by changing framing.
  - 11 **same-scale jump cuts** on the speaker, not hidden: 130.34, 421.63, 495.95, 497.50, 748.29, 763.72, 805.89, 968.88, 982.98, 1042.58, 1183.97. Several are mid-sentence (495.95 "...what the answer might be, | the more curious they're going to become"; 968.88 "will tie you with | a consistent source of value"; 1183.97 "moment where | the answer is not what I expected"). They are visible as a small jump of head and hands (shot sheets 007, 014).
  - 2 more partial-frame changes on the plain speaker (804.93, 813.27, labelled "pop") look like jump cuts too (hands change, no graphic appears; sheet 012).
  - The rest of the joins are covered by a cut to a graphic and back: 39 graphic segments, median 9.8 s.
- So roughly: 27 hidden by punch, about 13 left visible, 39 hidden under graphics. Jump cuts are tolerated; they are not all disguised.
- One black frame at 105.36 (frame 2526) sits between "It's that powerful." and "Okay, so the question is". The frame scan found no other black frame in the video, so treat it as a one-off, not a style.

---

## 4. Camera on the speaker

**The camera is locked off.** Background feature matching between the first and last frame of long shots gives scale 1.000 (shots #16, #26, #32, #51, #115, #122). All movement is scaling in the edit, centred on the frame centre (the measured shift divided by the scale change gives a fixed point at x 0.50, y 0.50-0.52).

**Speaker scale comes in fixed levels.** Matching every speaker shot against one reference frame (90.0 s) gives these scales at shot start/end (131 samples): 1.000 (48), 1.047 (40), 1.095 (29), 0.953-0.962 (10), 1.144 (1). Each level is x1.047 of the one below.

| Level | Scale vs reference | Face height | Seen at |
|---|---|---|---|
| -1 | 0.953 | about 28-29% | 259.8-263.9, 1037.5-1048 |
| 0 | 1.000 | about 29-31% | 41.0, 82.2-97.0, 125.8-143.3, 465.4-483.1 |
| +1 | 1.047 | about 31-34% | 97.0-99.9, 193.7-235.0, 742.5-748.3 |
| +2 | 1.095 | about 34-36% | 99.9-105.1, 186.0-193.6, 325.4 start, 1211.6-1221 |
| +3 | 1.144 | - | 156.5-162.2 only |

Moves:

| Move | Size | Duration | Count on speaker | Examples | Sound |
|---|---|---|---|---|---|
| Punch cut (instant, on a cut) | one level: x1.047 in (15) or x0.954 out (11); one of x1.095 | 1 frame | 27 | in: 97.01, 99.93, 143.27, 245.87, 499.62; out: 82.17, 162.25, 193.65, 235.03, 405.40; double: 620.91 | none (0.03 of punches have a sound event, chance 0.01) |
| Eased zoom (inside a shot, no cut) | two levels: x1.08-1.09 in or x0.915-0.926 out (verified 1.087 at 156.0, 0.915 at 520.8, 0.914 at 332.75, 0.917 at 10.26) | 0.42-0.63 s, median 0.46 s (10-11 frames; dense t155.8, t520.6, t331.9) | about 22 | in: 18.48, 114.36, 156.03, 287.08, 352.10, 372.54, 541.67, 733.36, 786.54, 979.35; out: 10.26, 62.27, 279.40, 298.76, 332.75, 362.65, 413.00, 520.81, 555.26, 683.73, 962.79 | 22 of the 26 zoom moves measured in speaker shots longer than 2.5 s have a strong low sound within 0.45 s (see section 11) |
| Slow zoom | 1.047 -> 1.000 over about 12 s (-0.4% per s) | 751-763.7 | 1 confirmed | 751-763.7 (shot #93); a +0.5% drift 763.9-769.7 | none |
| Blur + dim (not a camera move, but changes the speaker picture) | speaker blurred and darkened | ramps over about 10 frames | 3 | 106.5-114.6, 281.8-287.1, 769.9-770.9 | weak or none |
| Frame shrink | full frame -> rounded card | 20-24 frames | 2 | 0.47-1.3, 1055.2-1056.2 | strong low sound at 1055.96 |

**How often is the speaker static?** Between moves, completely: the background does not move at all. A scale change (punch or eased zoom) happens about 49 times in 823.8 s of speaker time, about once every 17 s. Counting cuts, zooms and overlay text appearing or leaving, something changes on the speaker picture every 2.1 s median (p90 8.7 s). The longest stretch of plain speaker with nothing changing is 17.6 s (465.5-483.1, the definition of anticipation); next 15.4 s (264.0-279.4), 15.1 s (838.7-853.8), 14.4 s (983.1-997.5).

`summary.json` says 19% of speaker time is "slow pull out" and 1% "slow push in". Background matching shows scale 1.000 across those shots, so apart from 751-763.7 these are not real (see section 13).

**Framing.** Speaker centred (face centre x 0.51, y 0.37), head and shoulders, microphone bottom centre, dark set with a teal light tube at the right edge. The tube is fully in frame at level 0 and leaves the frame at level +2, which is how the levels can be told apart on the sheets.

**What triggers a move.**
- Punch cut: the start of a new sentence or thought, usually opening with "Now,", "So", "This is", "Okay" (27 of 27 at a sentence/clause start).
- Eased zoom-out: just before text or icons appear beside or behind the speaker, to make room. 10.26 -> sentence at left 10.5; 62.27 -> "PAVLOVIAN" 62.69; 279.40 -> "CURIOSITY" 280.21; 298.76 -> side labels 299.5; 332.75 -> question bubble 334.4; 413.00 -> side labels 418.4; 520.81 -> loop ring 529.6; 555.26 -> split panel 562.0; 683.73 -> three cards 685.2.
- Eased zoom-in: after the overlay has gone, or on a line that turns the argument: 287.08 "Now, the reason curiosity loops work", 352.10 "Now, there's two ways", 541.67 "Now here's a big pro tip", 156.03 "they're going to get a hit of dopamine", 786.54 "the reality is when you're attractive", 979.35 "you equal value".
- Directions mix so the scale stays within the levels above; it never keeps climbing (net of the four zooms in shot #43 is 1.000). Hard cuts back from graphics re-enter at any level.

---

## 5. Layouts

Shares are of the 1345 s runtime, added up from shot and text-track times.

| # | Layout | Share / count | Example times | What the speaker is doing |
|---|---|---|---|---|
| A | Speaker full frame, nothing on it | about 43% (582 s) | 41.0-46.9, 130.3-143.3, 465.4-483.1, 838.7-853.8 | Talking to camera, hands in frame |
| B | Speaker + lower-third caption (heading + 1-2 lines, bottom left, dark gradient under it) | 12 times, about 92 s (6.8%) | 83.0-93, 126.8-130.3, 218.7-226, 504.6-512.6, 744.5-750.3, 931.3-944.3, 964.2-971.5, 1000.5-1007.5; variants: three small labels 145.3-150.3, pill 201.7-213.7, three cards 685.2-693.2 | Talking; caption sums up the point in other words |
| C | Speaker + side labels or icons at mid-height, left and/or right of the head | 10 times, about 76 s (5.6%) | 10.5-13.7, 16.4-18.7 (counters), 299.5-310.5, 334.4-351.4 (bubbles), 356.4-363, 418.4-422, 436-447 ("?" icons), 529.6-541.6 (ring), 955-963 (logos), 979.9-982.9 ("You = Value") | Talking, usually after a zoom-out |
| D | Speaker + big title word behind or beside the head | 2 times | 62.69-64.6 "PAVLOVIAN EFFECT" (behind the head; the head covers the "O"), 280.2-287.1 "CURIOSITY LOOP" (left of the head) | Talking, sharp |
| E | Speaker blurred and dimmed + text | 3 times, about 14 s | 106.5-114.6 (question, centre), 281.8-287.1 (title + small definition, left), 769.9-770.9 ("?" icon, then dissolves to canvas) | Still talking, still moving, but soft and dark |
| F | Split: speaker cropped to the left third, list panel on the right two thirds | 1 time, 25.5 s | 562.0-587.5 | Talking, reads the three questions |
| G | Full-screen graphic on the dark canvas | about 23% (313 s): ladder 12 times / 178 s; other diagrams 11 times / 135 s | Ladder 24.1-41.0, 116.0-125.8, 853.8-915.1; diagrams 67.2-79.2, 164.0-186.0, 310.6-325.4, 374.5-399.9, 638.6-653.3 | Not visible; voice continues without a break |
| H | Clip in a rounded card on the canvas, source label top-left of the card | 2 sequences, 28 s (2.1%) | 588.9-611.8 "Joyride (2001)", 946.2-951.5 "MrBeast YouTube" | Not visible; voice continues |
| I | Live example: vertical clip card centre, six-box checklist right, speaker in a small rounded card bottom right (face 10-11% of frame height at x 0.88, y 0.71), typed questions left of the clip | 6 stretches, 170 s (12.6%) | 1055.2-1131.9, 1137.0-1156.5, 1163.2-1177.9, 1185.9-1211.6, 1221.1-1231.4, 1256.5-1279.1 | Visible small, reacting and narrating; between stretches the edit cuts to layout A for his reaction |
| J | Screen recording in a rounded card on the canvas | 1 sequence, about 15 s | 1321.0-1338.7 | Not visible; voice continues |
| K | Speaker frame as a card inside a graphic | opening only | 0.47-3.9 | Talking |

The speaker is never shown at full frame for more than 96.8 s without a cut to a graphic (492.1-588.9), and inside that stretch there are two lower thirds, the loop ring and the split panel.

---

## 6. Motion-graphics catalogue

**Shared look.** Canvas is near-black in the middle (#010101 to #0f0f10) rising to dark grey at the edges (#1a1a1a to #252227), with a violet glow in the bottom corners (#4c10a8, #5d1eb4, #5d0bba, #6300d9 sampled at 50 s, 573 s, 650 s). Everything is flat 2D with glow; no 3D objects. Accent is one violet (level names OCR #ac6ceb-#b97af4). Text is a geometric sans, white or light grey. Cards are rounded rectangles filled violet-to-dark gradient with a thin lighter outline. Entry is almost always a hard cut to an **empty canvas**, then the parts animate in over 0.3-1.2 s; exit is a hard cut back to the speaker with the graphic fully built.

| # | Type | Looks like | Trigger sentence | Enter / build / leave | Hold | Count / times |
|---|---|---|---|---|---|---|
| 1 | **Ladder** (the video's main diagram) | Two dark vertical rails; each rung is a glowing violet line drawing of a chain of hexagons (a molecule skeleton). Level name in violet bold, "Level N" small in light grey under it. | "I'm going to break down the six levels of the dopamine ladder" (24.8); "There are six stages of a viewer's journey" (46.9); "As a recap, we covered the full dopamine ladder" (1286) | Cut to empty canvas 24.13, rails and rungs slide in 24.3-25.4 (about 26 frames). Inside the shot the camera **snaps** to new framings in 1-5 frames with motion blur (28.83, 29.82, 31.36, 48.77-48.94, 1287.19, 1289.77-1289.97). Leaves by hard cut. | 3.3-61 s | 12: 3.7, 24.1, 46.9, 116.0, 256.4, 454.0, 626.9, 693.3, 853.8, 1024.3, 1286.2, 1299.1 |
| 2 | **Level title card** (ladder framed on the new rung) | Camera sits on two rungs; new level name appears above the previous one | "All right, level two in the dopamine ladder is called captivation" (256.4); "level three in the dopamine ladder is anticipation" (454.0); "the next level... level four is called validation" (626.9) | Hard cut in on "All right"; camera climbs one rung in about 1.4 s (257.0-258.4); name appears within 0.3-0.8 s of the spoken name (Level 1: about 1.9 s before it) | 3.3-11.3 s | 116.0, 256.4, 454.0, 626.9, 717.9, 911.9 |
| 3 | **Ladder with notes** | Ladder moved to one side; text or brackets on the other: phrases ("How it works", "Why it works", "Tactics to use it to your advantage"), white bracket + "The message" / "The messenger", description list per level, "Your goal:" | "How it works, why it works..." (28.6); "We'll call that the message. The last two are more with the messenger" (716); "use these levels... as a checklist" (1300) | Snap reframe, then text types on word by word | 1-55 s | 28.8-41.0, 705.9-721.7, 860.3-911.9, 1299.1-1312.1 |
| 4 | **Lower-third caption** | Short violet bar, small white heading, 1-2 lines of light grey text with the key phrase in bold white; dark gradient band behind; left edge at x 0.10, y 0.77-0.88 | "the ultimate sign of attention mastery is when..." (82.9); "the stimulation step is what happens in the very first one to two seconds" (126.8); "the tactical tip is..." (218.5) | Types on left to right over about 0.6-1 s (83.0-83.6 in dense t82.0); gone by 93.0 | 3.5-13 s, median 8 s | 9 + 3 variants (section 5 row B) |
| 5 | **Side labels** | 1-3 short lines of white text, key words in violet, no box, at mid-height left and/or right of the head | "The bigger and more non-obvious the question, the bigger the curiosity, the higher the stakes" (299); "either not relevant to them or just not interesting enough" (418); "You could literally ask it... or you can imply it" (356) | Types on; left = cause or option 1, right = effect or option 2 | 2-17 s | 10.5, 299.5, 356.4, 418.4, 438.2 |
| 6 | **Speech bubbles beside speaker** | Violet rounded pills with small white text, one left, one right | "First, what is the most curiosity-inducing question... And second, how well will that question map..." (333-347) | Left appears 334.4, right 340.4, both leave 351.4 | 17 s | 1 |
| 7 | **Big title word** | Heavy white caps with a white glow. "PAVLOVIAN" 16% of frame height across the full width behind the head; "EFFECT" under it as a hollow outline. "CURIOSITY / LOOP" 7.6-9.4% left of the head, the OO of LOOP drawn as an infinity sign | "you will create a Pavlovian effect" (62.56); "Many people call this a curiosity loop" (280.16) | Word 1 pops in one frame 0.05-0.13 s after its spoken onset (62.69, 280.21); word 2 at its own onset (63.32, 280.88); infinity draws over 8 frames; flickers out over 9 frames (64.25-64.62) | 1.9 s / 6.9 s | 2 |
| 8 | **Question on blurred speaker** | 1-3 centred lines of small white text (3-3.5%), key words bold | "so the question is, what are the six levels and how do you make your content..." (105.8) | Blur + dim ramp 106.5-106.9; text types word by word from 106.40 in step with the voice; un-blur 114.2-114.6 | 8 s | 106.5, 281.8, 769.9 |
| 9 | **Counter badges** | Violet card "1M+ Followers" left, blue card "999B+ Views" right, with avatar and a tick; digits count up (994K+ at 16.6, 1M+ at 17.7) | "I have a million followers. I've done billions of views" (16.3, 17.3) | Each pops as its number is said; both gone by 18.7 | 2.3 s | 1 |
| 10 | **Photo + article + line drawing** | Black-and-white portrait with name label "Ivan Pavlov"; a web article (logo "healthline") with the title "Classical conditioning definition" on a violet highlight; white line drawing of a dog, bell and food bowl; violet hand-drawn circles | "Pavlov is the famous scientist that proved classical conditioning. Every time he rang this bell, he gave a dog food" (67.2-73) | Cut to empty canvas 67.19; portrait and article in by 70.2; camera slides to the drawing 71.6-72.2; circle draws round the bowl 72.3-72.7 on the word "food" (72.40); ends on "bell = bowl" 79.08 | 12 s | 1 |
| 11 | **Blurred tile test** | Eight phone-shaped tiles in two rows, blurred, some grey and some coloured/moving; then two tiles come forward sharp with labels "More motion / More color / More brightness" | "I'm going to show eight 9x16 images on the screen... tell me exactly which one your attention goes to first" (163.9) | Cut to empty canvas 163.96; tiles fade in 164.3-164.9; two tiles step forward at about 178.9; labels 181.7-186 | 22 s | 1 |
| 12 | **Flow diagram** | Phone card with play button -> comment chip ("Username: I wonder when the aliens are visiting earth?") -> "Curiosity Inducing" -> branch "Interested with aliens" / "Not interested with aliens" -> red "Viewer leaves" | "For example, if you made a video that got a viewer to ask... I wonder when the aliens are visiting Earth?... they're going to churn" (310.6-325) | Builds left to right as the sentence goes; camera follows the line, zooming x1.65 at 322.4-324.8 | 14.8 s | 1 |
| 13 | **Phone scene** | Vertical phone card with a dark figure silhouette and an orange sun that moves; large violet "?" above; quoted hook on the phone; questions typed left and right | "I saw this really attractive person with this red and orange vivid graphic... How does she do her makeup? Why is she doing it like that?" (374.5-396) | Empty canvas 374.5; phone by 378; "?" and quote at about 389-392; questions at 392.6 and 395.2 | 25.4 s | 1 |
| 14 | **Head silhouette** | Dark head-and-shoulders outline with violet rim, "?" inside, then blue dots around it | "as soon as a question pops in someone's head, they immediately are trying to anticipate" (483.2) | Outline 483.2, "?" by 486, dots by 489 | 8.9 s | 1 |
| 15 | **Loop ring around speaker** | Thin dotted violet circle around the head with labels "Question", "Anticipation", "Answer", later "2nd Question" | "The loop is them see-sawing between question, anticipation and answer" (527-534) | Labels appear in spoken order 529.6-535.6; leaves 541.6 just before the zoom-in | 12 s | 1 |
| 16 | **Split-panel list** | Dark panel with a soft violet blob; bold white heading "To build anticipation in your story, ask yourself:"; three numbered circles joined by a line, two-line questions | "you want to ask yourself this. Based on the question the viewer should have in their head..." (562-587) | Panel slides in from the right over 22 frames (561.98-562.9) while the speaker is pushed to the left third; items at 564.6, 570.6, 576.6; slides out 587.44-588.3 | 25.5 s | 1 |
| 17 | **Card tree** | Top card "Validation / Goal: ..."; curved line down to card "Entertainment"; second visit adds "Education" | "the goal with validation is to make sure you reward..." (639.1); "On the education side..." (665.9) | Card fades up over 9 frames (639.0-639.4) on the word "validation" (639.12); branch at 645.8; same graphic returns at 665.9 with the second branch added | 14.7 s + 11.3 s | 2 visits |
| 18 | **Three cards in the lower third** | Violet cards "Curiosity / Question", "Anticipation / Possible answer", "Validation / Actual answer" | "So it's curiosity question, anticipation, what could the answer be? And then validation" (684-690) | Appear right to left as named: 685.2, 686.2, 689.2 | 8 s | 1 |
| 19 | **Numbered path list** | Title "4 Ways to improve likeability"; glowing violet numerals 1-4 on a dotted winding path; each item is a dark box typed with its label | "The first one, attractiveness is a massive factor" (778.5); "The second thing... is your overall vibe" (796.6); "The third thing, smiling" (809.0); "And then fourth..." (820.5) | Overview 774.8; for each item: cut from speaker to the path, whip to the numeral in 5 blurred frames (809.15-809.36), label types word by word from 0.3 s later; cut back to speaker for the explanation | 2.8-8.5 s each | 4 items |
| 20 | **Logo bubbles** | Round badges popping around the head: a red "N", an NFL shield, a photo of a person, a teal logo | "you're competing with Netflix, the NFL, Kai Cenat, MrBeast" (955) | One per name; gone before the zoom-out at 962.8 | about 8 s | 1 |
| 21 | **"You = Value"** | Two thick white bars behind the head forming "="; "You" left, "Value" right | "you've trained that you equal value" (979.9) | "You" at 979.9, bars and "Value" at 980.0-980.6 on the words | 3 s | 1 |
| 22 | **Movie / creator clip card** | Clip in a rounded card (about 68% of frame width) on the canvas, label top-left ("Joyride (2001)", "MrBeast YouTube"); viewer questions typed over the dimmed clip | "those visual hooks where it looks like someone's about to get hit by a car" (588.9); "Mr. Beast has this level of Pavlovian response" (946.2) | Hard cut in; clip keeps its own cuts; clip dims 600.4-604.2 while "Is that person gonna get hit by a car?" / "Is that car really gonna run them over?" type on | 22.9 s / 5.4 s | 2 |
| 23 | **Live example layout** | Layout I in section 5. Checklist boxes fill violet as each level is reached: Stimulation by 1080, Captivation by 1100, Anticipation by 1150, Validation by 1165, Affection by 1200, Revelation by 1225 | "we're going to pull the video up on the side... watch it and then pause it a lot" (1055) | Speaker shrinks to the corner card over 24 frames (1055.2-1056.2); clip card slides down from the top 1055.7-1056.0; questions type at the left (1096-1104, 1113-1131, 1144-1153) | 170 s total | 6 stretches |
| 24 | **Screen recording card** | Browser recording of the community (white UI) in a rounded card; zooms into posts; violet pill "skool.com/wavyworld" bottom centre from about 1337 | "a completely free community called Wavyworld that has 65 other trainings" (1321) | Hard cuts between pages every 0.5-3 s (12 cuts in 17.7 s) | 17.7 s | 1 |
| 25 | **Opening network** | Avatar circles joined by thin lines around the speaker card; then one glowing node | "get people truly addicted to watching your content" (0-3.6) | Nodes pop from 0.68; card slides down 3.3-3.9 | 5 s | 1 |
| 26 | **Subscribe lower third** | Dark blue rounded card, channel avatar, "Kallaway", "SUBSCRIBE" button, handle | "we will see you guys on the next video" (1341) | Appears about 1341.5, there to the end | 3 s | 1 |
| 27 | **Curve on the ladder** | A glowing violet line weaving up through the rungs | "when you can hit this level six state, you have won the attention game" (1024.3) | Line draws upward 1025-1029 | 4.9 s | 1 |

---

## 7. Script -> picture table

Lead/lag: `+` = picture after the word. Values marked (d) were read frame by frame from a dense sheet; values marked (o) come from OCR tracks, which were sampled about once per second, so they are good to about +/-0.5 s.

| Time | Spoken line | What the picture does | Why | Lead / lag |
|---|---|---|---|---|
| 0.0 | "If you want to get people truly addicted to watching your content" | Speaker full frame; from 0.47 the frame shrinks to a card and avatar icons pop around it | abstract "people" -> crowd of icons | +0.47 from first word (d) |
| 3.8 | "there's one trick you should be using every single time" | Card drops away, one node glows, the sentence types at the top | "one" -> a single dot; the hook line as text | text +0.1 after "trick" (d) |
| 6.9 | "It's called the dopamine ladder" | Fast zoom-out from a glowing molecule to the ladder; "Dopamine" and "Ladder" fade in left and right | naming the framework -> reveal of the diagram | labels +0.4 / +0.2 (d) |
| 10.9 | "you'll become a master of attention overnight" | Zoom-out 10.26, sentence types at the left of the speaker | promise -> key sentence as side text | +0.2 (o) |
| 16.3 | "I have a million followers" | Violet badge counts up to "1M+ Followers" | number -> counter | about +0.1 (o) |
| 17.3 | "I've done billions of views" | Blue badge "999B+ Views" on the other side | number -> counter | about +0.4 (o) |
| 24.2 | "So in this video, I'm going to break down the six levels" | Hard cut to empty canvas, ladder assembles | agenda -> title card | cut on "So"; label "6 Levels of Dopamine Ladder" with the words (o) |
| 28.6 | "How it works, why it works, ... the specific tactics" | Ladder snaps to a new place three times; one phrase types each time | list -> one item per snap | 0 to +0.2 (d at 28.83) |
| 41.0 | "Like what is really going on in a viewer's brain" | Hard cut to speaker, widest framing | end of graphic; direct question to camera | on the sentence start |
| 46.9 | "There are six stages of a viewer's journey" | Ladder; snap zoom-out at 48.8 shows "Level 1" to "Level 6" | number -> six labelled rungs | +1.9 after "six" (d) |
| 62.6 | "you will create a Pavlovian effect" | Zoom-out 62.27-62.69, then "PAVLOVIAN" behind the head, then "EFFECT" | new term -> big title word | +0.13 / -0.04 (d) |
| 67.2 | "Pavlov is the famous scientist that proved classical conditioning" | Hard cut: portrait photo, name label, article with the term highlighted | authority -> photo + source screenshot | cut 0.0 (d) |
| 71.2 | "Every time he rang this bell, he gave a dog food" | Camera slides to the line drawing; circle draws round the bowl | story -> drawing, circle on the noun | circle on "food" 0.0 (d) |
| 76.6 | "the dog's mouth would water" | Camera pushes in on the dog; circle on the collecting tube | effect -> highlight | about 0 (o) |
| 82.9 | "the ultimate sign of attention mastery is when you can make dopamine release... just by seeing your name or face" | Punch-out at 82.17; lower third types: "The ultimate level of attention mastery is triggering dopamine in viewers just by your name or face - before they even watch your content." | takeaway -> written summary (not word for word) | text starts +0.1 after "ultimate" (d), full by 83.6 |
| 97.0 | "This is when you reach King status in attention land." | Punch-in x1.047 | emphasis on a new sentence | on the cut |
| 99.9 | "Now, if you can learn to do this on command" | Second punch-in to x1.095 | escalation | on the cut |
| 105.8 | "so the question is, what are the six levels and how do you..." | Speaker blurs and dims; question types in the centre word by word | question the video will answer -> text on blurred speaker | 0.0 (d) |
| 116.0 | "All right, the very first rung in the dopamine ladder" | Hard cut to ladder, snap to the bottom rung at 116.87, "Level 1" then "Stimulation" | new section -> title card | label about 1.9 s before "stimulation" (o) |
| 126.8 | "the stimulation step is what happens in the very first one to two seconds" | Lower third: heading "Stimulation step", line with bold "first 1-2 seconds" | definition -> lower third | +0.55 (o) |
| 145.4 | "comes from colors, motion and brightness" | Three small labels appear left, centre, right, one per word | list -> items appear as named | -0.26 / -0.04 (o), "Brightness" -0.15 (d) |
| 156.0 | "they're going to get a hit of dopamine" | Eased zoom-in x1.09 over 11 frames with a low sound | emphasis -> zoom | starts on "they're" (d) |
| 163.9 | "I'm going to show eight 9x16 images... but I'm going to blur it out" | Cut to canvas, eight blurred tiles fade in | demonstration -> the test itself on screen | tiles +0.4 after "eight" (d/o) |
| 176 | "these were the two that they noticed... more motion, color and brightness" | Two tiles step forward sharp; three labels | reveal -> highlight + labels | +0.4 to +1.4 (o) |
| 202.5 | "It's called bottoms up processing" | Violet pill "1 Bottoms-up Processing" bottom centre | technical term -> label | pill about 0.8 s before the term (o) |
| 218.5 | "the tactical tip is that when you're making your own content..." | Lower third "Tactical tip" + sentence | advice -> lower third | +0.1 (o) |
| 256.4 | "All right, level two in the dopamine ladder is called captivation" | Ladder climbs one rung, "Captivation / Level 2" | new section -> title card | name -0.3 (o) |
| 280.2 | "Many people call this a curiosity loop" | Zoom-out 279.4; "CURIOSITY" pops, "LOOP" draws; at 281.8 the speaker blurs and a one-sentence definition types under the title | term -> title; definition -> text on blurred speaker | +0.05 / +0.22 (d) |
| 299.5 | "The bigger and more non-obvious the question, the bigger the curiosity, the higher the stakes, and the more dopamine" | Zoom-out 298.76; left label (the input), right label stack (the outputs); left swaps to "More relevant question" at 305.5 | cause -> effect as left -> right | +0.5 to +0.7 (o) |
| 310.6 | "For example, if you made a video that got a viewer to ask..." | Hard cut to flow diagram, builds along the sentence | example -> flow diagram | cut on "For example" |
| 323 | "they're going to churn. They won't be captivated." | Diagram ends on red "Viewer leaves" | bad outcome -> red label | about 0 (o) |
| 333.5 | "First, what is the most curiosity-inducing question..." / 340 "And second, how well will that question map..." | Zoom-out 332.75; violet bubble left, then bubble right | two questions -> left and right bubbles | +0.85 (o) |
| 356.4 | "You could literally ask it... or you can imply it with details" | Right label "Literally ask the question", then left "Imply it with details" | two options -> two sides | +0.8 (o) |
| 374.5 | "let's say I was scrolling the feed and I saw this really attractive person with this red and orange vivid graphic behind them that was moving" | Phone card, figure silhouette, orange sun moving | imagined scene -> illustration | cut on "So for example" |
| 389.6 | "here's how you do your makeup for the holidays" | Quote typed on the phone; big "?" above | quote -> text on the phone | +0.4 (o) |
| 392.5 | "How does she do her makeup? Why is she doing it like that?" | Questions typed left and right of the phone | viewer's thoughts -> side text | +0.4 / +1.1 (o) |
| 418.4 | "either not relevant to them or just not interesting enough" | Zoom-out 413.0; "Not relevant to them" left, "Not interesting enough" right | either/or -> two sides | +0.4 / +0.5 (o) |
| 436 | "you can use contrast... or two, you can frame a super shocking or weird premise" | "?" icon + label left, then "?" icon + label right | two tips -> two sides | about +1 (o) |
| 454.0 | "All right, level three in the dopamine ladder is anticipation" | Ladder climbs, "Anticipation / Level 3" | new section -> title card | +0.75 (o) |
| 483.2 | "as soon as a question pops in someone's head, they immediately are trying to anticipate" | Head silhouette, "?" appears inside, dots gather | mental process -> icon | cut on "what happens is" |
| 499.6 | "The highest level of dopamine is achieved just before the answer comes." | Punch-in to level +2; lower third from 504.6 | key claim -> punch-in, then written summary | cut on the sentence |
| 529.6 | "The loop is them see-sawing between question, anticipation and answer" | Dotted ring round the head; labels appear in spoken order | cycle -> ring diagram around the speaker | +0.1 (o) |
| 545.6 | "The viewer is only able to anticipate... if they're clear on the facts" | Lower third: "The viewer can only anticipate your answer if the facts you give them are clear." | pro tip -> lower third | -0.5 (o) |
| 562.0 | "you want to ask yourself this" | Panel slides in from the right, speaker pushed left; three numbered questions appear as each is read (564.6, 570.6, 576.6) | checklist -> numbered list, item per line read | panel 0.0; items within 1 s (o) |
| 588.9 | "those visual hooks where it looks like someone's about to get hit by a car" | Movie clip in a card, label "Joyride (2001)" | example -> clip | cut on "looks like" |
| 600.4 | "is that person going to get hit by a car? Is that car really going to run them over?" | Clip dims; the two questions type over it, left then right | viewer's thought -> text over dimmed clip | -0.18 / +0.22 (o) |
| 626.9 | "the next level... level four is called validation" | Ladder climbs, "Validation / Level 4" | new section -> title card | -0.76 (o) |
| 639.1 | "the goal with validation is to make sure you reward..." | Card "Validation / Goal:" fades up; at 645.8 a line runs to card "Entertainment" | definition -> card; "with entertainment content" -> branch | 0.0 (d) |
| 665.9 | "On the education side, the validation... would be..." | Same tree, second branch "Education" added | second category -> second branch | cut on "On the education side" |
| 685 | "So it's curiosity question, anticipation... And then validation" | Three cards appear in the lower third, one per term | recap -> one card per item | +0.6 to +1.0 (o) |
| 713 | "We'll call that the message. The last two are more with the messenger." | White bracket over levels 1-4 "The message"; snap up to levels 5-6 "The messenger" | grouping -> bracket + label | +0.2 (o) |
| 745.5 | "As the viewer begins to realize they like and trust the person" | Lower third: "When the audience forms trust and affinity with the creator, it triggers more dopamine." | mechanism -> lower third | about +1 (o) |
| 769.9 | "the million-dollar question that everyone asks is, how do I improve my likability" | Speaker blurs with a violet "?" over him, dissolves to canvas; the question types | question -> "?" icon, then typed question | "?" 0.8 s before "how" (d) |
| 778.5 | "The first one, attractiveness is a massive factor" | Path with numerals 1-4; zoom to "1", label types | list of four -> numbered path, one stop per item | +0.2 (d/o) |
| 809.0 | "The third thing, smiling, is great for subconscious likability" | Cut to path at 808.65, whip to "3" 809.15-809.36, label types from 809.65 | list item | whip +0.17 after "third" (d) |
| 860 | "The first level was stimulation... captivation... anticipation... validation... likability" | Ladder on the left, a description list grows on the right, one entry per level | recap -> list builds as each is named | entries lead the name by up to several seconds (o) |
| 931.3 | "Entertainment content can only get to level six if..." | Lower third "Entertainment Content" + sentence | category rule -> lower third | +0.6 (o) |
| 946.2 | "Mr. Beast has this level of Pavlovian response" | Three clips of the creator in a card | named person -> clips | cut 0.7 s before "Beast" |
| 955.4 | "you're competing with Netflix, the NFL, Kai Cenat, MrBeast" | Four logo bubbles pop around the head | names -> logos | +1.0 (o) |
| 979.9 | "you've trained that you equal value" | "You", white "=" behind the head, "Value" | equation -> equation | +0.15 / +0.18 (o) |
| 1002.4 | "deliver non-obvious differentiated value over and over and over" | Lower third "How to Achieve Revelation" + that sentence | how-to -> lower third | -1.35 (o) |
| 1055 | "So we're going to pull the video up on the side" | Speaker shrinks to the corner; clip and checklist appear | proof by example -> the real clip, speaker as commentator | on the phrase (d) |
| 1070-1222 | "the first step... is stimulation" ... "level six... is revelation" | One checklist box fills per level | progress through a list -> ticks | within about 10 s of each name (frames at 1080, 1100, 1150, 1165, 1200, 1225) |
| 1096 | "First, who are these people? Why are they hugging? Do I care?" | Three questions type at the left of the clip | viewer's thoughts -> typed questions | +0.9 / -0.1 / +0.1 (o) |
| 1166.5 | "it hard cut match cuts away to him getting dragged singing a song" | The clip itself cuts to the singer, with its own yellow word captions and audio | let the example play | clip plays inside a 0.84 s voice pause |
| 1286.5 | "As a recap, we covered the full dopamine ladder, all six levels" | Ladder, snap zoom, fast scroll up through all six names | recap -> the diagram once more | cut on "As a recap" |
| 1299.3 | "Your goal... is to use these levels... as a checklist" | Ladder left, "Your goal: Use this framework as a checklist to guide the viewer up each level" right | instruction -> text | -0.08 (o) |
| 1321.0 | "a completely free community called Wavyworld that has 65 other trainings" | Screen recording of the community pages | offer -> screen recording as proof | cut on "a completely free" |
| 1337 | "So if you want a peer group" | URL pill "skool.com/wavyworld" under the recording | call to action -> the address | pill before "link... below" (1340) |

---

## 8. Why each cut is there

Sample: every 3rd row of `timeline.md` (#0, #3, ... #168), 57 cuts.

| Reason | Count | Examples |
|---|---|---|
| End a graphic (hard cut back to the speaker at a new sentence) | 16 | #3 at 8.72 ("And if you can understand this one framework"); #51 at 465.38 ("This next step, anticipation is super powerful") |
| Cut inside a clip or screen recording (the footage's own cut, or next screen) | 12 | #63 at 598.35 (movie clip); #159 at 1327.62 (next community page) |
| New sentence / thought, covered by a punch cut | 9 | #18 at 99.93 ("Now, if you can learn to do this on command"); #111 at 838.71 ("So likability is one of those things") |
| Start a graphic or clip | 7 | #42 at 310.64 ("For example, if you made a video..."); #57 at 588.92 (movie clip) |
| Visible jump cut on the speaker (same scale, mid-sentence) | 4 | #54 at 495.95; #120 at 968.88 |
| List item (camera moves to the next item in a graphic) | 3 | #6 at 28.82 ("How it works"); #105 at 808.64 ("The third thing") |
| Section change (ladder moves to the next level or recap) | 3 | #24 at 116.87 (Level 1); #90 at 717.88 (Level 5) |
| Emphasis word (title text pops, or speaker blurs for a definition) | 2 | #12 at 62.69 ("PAVLOVIAN"); #39 at 281.78 (curiosity loop definition) |
| Other (first frame) | 1 | #0 |
| Pattern break only (no change in the script) | 0 | none found in the sample |

Every sampled cut is tied to the script: a sentence start, a list item, a named example or a section. None is there only to break a long take. Punch cuts happen at sentence starts only. Two punches in the same direction can follow each other (97.01 and 99.93 both in; 1017.27 and 1037.45 both out).

**Longest stretches with no cut to a different picture** (shots.json):

| Span | Length | Picture | What is said | Caveat |
|---|---|---|---|---|
| 492.1-588.9 | 96.8 s | Speaker (shots #53-56) | Anticipation: head fakes, the loop, the pro tip, the three questions | Not plain: lower thirds at 504.6 and 544.6, ring 529.6-541.6, five zooms, split panel 562.0-587.5 |
| 951.5-1024.3 | 72.7 s | Speaker (#119-124) | Entertainment vs education, "you equal value", dating analogy, how to reach level six | Logos, two lower thirds, "You = Value", two zooms, two punches |
| 186.0-256.4 | 70.4 s | Speaker (#31-34) | Greyscale proof, bottoms-up processing, tactical tip, level-one wrap | Pill 201.7-213.7, lower third 218.7-226, three punches |
| 853.8-915.1 | 61.4 s | Ladder recap (#112-113) | Recap of levels 1-5 | The list on the right keeps growing |
| 399.9-454.0 | 54.1 s | Speaker (#45-49) | Makeup example wrap, level-two recap, pro tips | Side labels 418-422 and 436-447, one zoom, three punches |

The `summary.json` maximum of 102.7 s (1029.2-1131.9) is not a real unbroken picture: the change from full-frame speaker to the live-example layout at 1055.2 is an animation inside shot #129, not a cut.

Longest stretch of speaker with nothing at all changing (no cut, zoom, or text): 17.6 s at 465.5-483.1.

---

## 9. On-screen text and captions

**There are no running captions.** No word-by-word subtitles of the speech anywhere (all 19 sheets). Text appears only for selected phrases. 30% of big text tracks repeat spoken words; the rest paraphrase or label.

Sizes are OCR box heights as a share of frame height, so they include ascenders/descenders and are a little larger than the letter height. Colours are OCR averages over the glyphs and are darker than the true fill, which reads as white or light grey on the frames.

| Kind | Size | Position | Colour | Case / weight | Words | Animation | On screen | Matches speech? | Timing |
|---|---|---|---|---|---|---|---|---|---|
| Lower-third caption: heading | 3.5-4.6% | left edge x 0.10, y 0.77-0.81 | OCR #d4d2d7-#d6d6da (reads white) | Title case, medium | 2-4 ("Stimulation step", "Tactical tip", "Entertainment Content", "How to Achieve Revelation") | Appears with a short violet bar above it | 3.5-13 s | Label, not spoken as such (3 of 5 partly said) | +0.1 to +0.6 s after the phrase |
| Lower-third caption: body | 2.8-3.9% per line | x 0.10-0.83, y 0.82-0.89, 1-2 lines | OCR #8a888a-#acabae (light grey), key phrase bold white | Sentence case, regular + bold key phrase | 10-22 | Types on left to right in about 0.6-1 s | 5-11 s, median 8 s | Paraphrase; tighter than the speech | starts 0.1-1.7 s after the spoken sentence begins; one 1.35 s early (1002.4) |
| Side labels beside the speaker | 3.0-4.1% | y 0.47-0.59; left block x 0.05-0.32, right block x 0.68-0.95 | white (OCR #c2bcbe-#e0dbdd); key words violet (OCR #9b74d0, #8461b4) | Sentence case, semi-bold | 2-7 per block | Types on | 2-17 s | Mostly the spoken words | +0.4 to +0.85 s (o) |
| Big title word | 16.3% ("PAVLOVIAN"), 7.6% ("CURIOSITY"), 9.4% ("LOOP") | behind the head across x 0.12-0.92, y 0.27-0.44; or left of the head x 0.04-0.36, y 0.51-0.69 | #fdfdfd with white glow; second word as hollow outline | ALL CAPS, extra bold | 1 + 1 | Pops in one frame; second word on its own beat; flickers out in 9 frames | 1.9 s and 6.9 s | Exact word | +0.05 to +0.22 s (d) |
| Question / definition on blurred speaker | 3.0-3.5% | centred x 0.26-0.74, y 0.48-0.59 (3 lines); definition under the title at x 0.05-0.46, y 0.70-0.77 | OCR #b9b5b6-#d4d3d3 (white), some words bold | Sentence case | 12-30 | Types word by word in step with the voice | 5-8.8 s | Word for word (106.4-114.4) or close paraphrase (282.8) | 0.0 s (d) |
| Ladder labels | name 4.0-8.0% depending on zoom; "Level N" 3.7-5.0% | on the rung, centred on the ladder | name violet #ac6ceb-#b97af4; "Level N" #c3b7d2-#dedee2 | Title case; name bold, "Level N" regular | 1 + 2 | Fades in as the camera arrives | 3-55 s | Exact level name | -1.9 to +0.75 s (o) |
| Text beside the ladder | 3.3-5.0% | opposite side of the ladder, y about 0.5 | white, grey for lead-in words | Sentence case, bold key phrase | 2-6 | Types on; previous word greys out | 1-4 s | Exact ("How it works", "Why it works", "Tactics to use it to your advantage") | -2 to +0.5 s (o) |
| Card text (tree, lower-third cards) | title 3.1-4.3%, body about 2% | inside the card | #ffeeff-#fffaff on violet (#2f106e-#5714b7) | Title bold, body regular | 1-2 title, up to 20 body | Card fades up in 9 frames, body types | 7-15 s | Title exact, body paraphrase | 0 to +1.0 s |
| Split-panel list | heading 3.5%, items 2.8-3.3% | panel x 0.38-0.93; heading y 0.07-0.10; items y 0.20, 0.35, 0.50 | heading #fefdfe bold; items light grey | Sentence case | heading 8, items 20-25 | Item appears when its sentence starts | 11-24 s | Close to word for word | within 1 s (o) |
| Counter badges | number 5.2-5.7% | x 0.10-0.17 and 0.79-0.91, y 0.38-0.44 | white on violet (#522c7d) and on blue (#354577) | Bold digits | 1 + 1 | Digits count up | 1-2 s | Same figure as spoken | about +0.1 to +0.4 s (o) |
| Source label on a clip | 2.8-3.2% | top-left corner of the clip card (x 0.16-0.28, y 0.19-0.22) | OCR #b4bac4 | Title case, regular | 2 | Static | whole clip | Not spoken | - |
| Checklist (live example) | about 2% | x 0.81-0.93, y 0.07-0.30 | white text, violet boxes | Title case, regular | 6 single words | Box fills when the level is reached | 170 s | Level names | within about 10 s |
| Typed viewer questions (clip scenes) | 3.2-4.6% | left of the clip, y 0.43-0.58 | white, italic in the live example | Sentence case | 3-8 each | Types on; older lines dim | 2-7 s | Word for word | -0.2 to +1.1 s (o) |
| URL pill | 3.6% | bottom centre (x 0.50, y 0.86) | #f3d7ff on violet | lower case | 1 | Types on | 3.5 s | Not read aloud | before "link below" |

Position of big text over the whole video (3x3 grid, summary.json): centre 28%, bottom centre 24%, middle left 12%, top centre 10%, bottom left 9%, middle right 8%.

---

## 10. Transitions

| Kind | Frames | Where |
|---|---|---|
| Hard cut, speaker -> empty canvas, graphic then builds | 1 frame cut; build 8-26 frames (ladder 24.3-25.4; card 639.0-639.4) | Start of almost every full-screen graphic: 24.13, 67.19, 163.96, 310.64, 374.50, 483.15, 638.64 |
| Hard cut, built graphic -> speaker | 1 | End of every full-screen graphic: 8.72, 41.04, 79.20, 259.76, 399.90, 915.12, 1029.19 |
| Punch cut (instant scale step on the speaker) | 1 | 27 times, section 4 |
| Eased zoom on the speaker | 10-11 (0.46 s) | about 22 times, section 4 |
| Blur + dim ramp on the speaker | about 10 in (106.5-106.9), about 10 out (114.2-114.6); 5 at 769.9-770.1 | 106.5, 281.8, 769.9 |
| Cross-dissolve from blurred speaker to canvas, one element ("?") staying in place | 12 (770.8-771.3) | 770.8 only |
| Frame shrink (speaker video scales down into a rounded card) | 20-24 | 0.47-1.3; 1055.2-1056.2 |
| Panel slide (split layout) | 22 in (561.98-562.9), 21 out (587.44-588.3) | 562 / 587.5 only |
| Snap / whip camera move inside a graphic | 1-5, with motion blur | 28.83, 29.82, 31.36, 48.77-48.94, 116.87, 717.88, 809.15-809.36, 821.07, 860.28, 1287.19, 1289.77-1289.97 |
| Camera slide / zoom inside a graphic | 14-58 (0.6-2.4 s) | 71.6-72.2, 76.6-77.9, 257.0-258.4, 322.4-324.8 |
| Card slide off | 14 (3.3-3.9) | opening only |
| One black frame | 1 | 105.36 only |
| Darken at the end | last 8 frames | 1344.72-1345.05 |

No wipes, no glitch effects, no whoosh-style blur between speaker and graphic. The summary's 17 "transition" cuts are the blur ramps, the opening and CTA animations, and dims inside clips.

---

## 11. Sound

**Music.** None that the measurement can find. The music+effects stem sits at a median of -47.6 dB below the voice in every 30 s window (range -49.3 to -45.8 dB up to 1320 s). The three "bed on" spans are 1115-1120 (the example clip's own audio) and 1325-1345 (the stem rises to -42.4 dB in the last 25 s; whether that is a faint music bed under the CTA cannot be told from the numbers). There is nothing to duck: the 3 dB "duck" figure is at noise level.

**Sound events.** 648 candidates, of which 585 are weak (about 20 dB under the voice, almost all 20-200 Hz) and are most likely voice leaking into the stem. 63 are strong: median -4.6 dB relative to the voice, median 0.2 s long, 54 of them low band only (centroid about 50-90 Hz), 9 low + broadband.

The 20 strongest and what is on screen at that instant:

| # | Time | Level vs voice | Band, length | On screen (frame checked) |
|---|---|---|---|---|
| 1 | 7.26 | +2.8 dB | BB+LOW, 0.42 s | Fast zoom-out from the molecule close-up to three rungs, 7.0-7.75; "Dopamine" / "Ladder" fade in |
| 2 | 71.68 | +0.8 | LOW, 0.40 s | Camera slides from Pavlov's portrait to the dog drawing, 71.6-72.2 |
| 3 | 1055.96 | +0.4 | LOW, 0.31 s | Speaker frame shrinking to the corner; clip card sliding in, 1055.7-1056.0 |
| 4 | 1166.18 | -1.3 | BB+LOW, 1.21 s | The example clip's own sound: clip cuts at 1166.46 to the singer with yellow word captions; the speaker is silent (0.84 s pause from 1165.94) |
| 5 | 639.18 | -2.6 | LOW, 0.26 s | "Validation" card fading up, 639.0-639.4 |
| 6 | 28.37 | -3.0 | LOW, 0.19 s | Ladder with "6 Levels of Dopamine Ladder"; a brief brightening of the label 28.4-28.5; the snap reframe comes 0.46 s later at 28.83. Match uncertain |
| 7 | 413.11 | -3.0 | BB+LOW, 0.21 s | Eased zoom-out on the speaker, 413.0-413.46 |
| 8 | 31.33 | -3.1 | LOW, 0.19 s | Ladder snaps to a new framing at 31.36; "Tactics to use it" types |
| 9 | 962.95 | -3.1 | LOW, 0.25 s | Eased zoom-out on the speaker, 962.79-963.25 ("But on the education side") |
| 10 | 555.55 | -3.2 | BB+LOW, 0.20 s | Eased zoom-out on the speaker, 555.26-555.72 |
| 11 | 1289.83 | -3.2 | LOW, 0.20 s | Fast scroll up the ladder, 1289.77-1289.97 |
| 12 | 287.13 | -3.3 | LOW, 0.27 s | Speaker un-blurs and zooms in, 287.08-287.58 |
| 13 | 717.84 | -3.3 | BB+LOW, 0.21 s | Ladder snaps up to levels 5-6 at 717.88 |
| 14 | 520.97 | -3.4 | LOW, 0.21 s | Eased zoom-out on the speaker, 520.81-521.27 |
| 15 | 733.57 | -3.6 | LOW, 0.19 s | Eased zoom-in on the speaker, 733.36-733.82 |
| 16 | 809.18 | -3.7 | LOW, 0.20 s | Whip along the path to numeral 3, 809.15-809.36 |
| 17 | 29.79 | -3.8 | LOW, 0.19 s | Ladder snaps at 29.82; "Why it works" types |
| 18 | 48.80 | -3.8 | LOW, 0.20 s | Ladder snap zoom-out, 48.77-48.94 |
| 19 | 76.77 | -3.8 | LOW, 0.32 s | Camera pushes in on the dog drawing from 76.58 |
| 20 | 821.05 | -3.8 | LOW, 0.18 s | Path jumps to numeral 4 at 821.07 |

**Which picture events get a sound.**

| Picture event | Share with a sound | Note |
|---|---|---|
| Eased zoom on the speaker | 22 of 26 measured (85%) get a strong low sound, -3.0 to -6.3 dB vs voice, starting 0.0-0.3 s after the zoom starts | The four without are the 0.17-0.25 s moves at 8.76, 562.77, 587.46 and the second opening move at 2.75 |
| Snap / whip / slide of the camera inside a graphic ("jump" cuts) | 31% of all jump cuts (chance 1%); 9 of the 16 jumps inside graphics | 29.79, 31.33, 116.83, 705.87, 717.84, 796.84, 821.05, 860.24, 1287.21 |
| Large layout animation | yes | 0.78 (frame shrink), 1055.96 |
| A card appearing in a full-screen graphic | sometimes | 639.18 yes |
| Punch cut | 3% (chance 1%) | effectively never |
| Hard cut | 1% | never |
| Text popping or typing (titles, lower thirds, side labels) | 0% of pops | The sound near "PAVLOVIAN" (62.52) and "CURIOSITY" (279.44) belongs to the zoom-out that comes just before the word |
| Blur transitions | 0% strong | weak events at 106.70 (-10 dB) and 769.94 (-4 dB, with the zoom) |

Rule in one line: **sound follows camera movement, not cuts and not text.** The sound is short (0.2 s), low (about 50-90 Hz) and 3-6 dB under the voice.

Other strong events: 1068.5, 1139.6, 1141.3, 1153.2, 1153.9 (-10 to -13 dB) are inside voice pauses while the example clip plays, so they are the clip's audio. 1342.4, 1343.4, 1344.1 (-10 to -13 dB) coincide with the subscribe lower third at the end.

**Silences and pauses.** 16 silences, all 0.15-0.28 s. The only pauses over 0.5 s: 1067.9 (2.64 s), 1091.8 (3.26 s), 1106.9 (2.11 s), 1116.9 (2.51 s), 1139.7 (2.25 s), 1151.9 (1.80 s), 1153.8 (1.18 s), 1165.9 (0.84 s). Each is the speaker stopping so the example clip can play before he comments on it. Everywhere else the gaps between words are 0.28 s median, 0.44 s at p90.

---

## 12. Rules to reproduce this edit

1. Remove every pause over about 0.35 s from the speech (measured: median pause 0.23 s, p90 0.33 s, none over 0.5 s outside the clip-watching section).
2. Add no music bed (measured bed -47.6 dB under the voice). Master to about -14 LUFS, LRA under 2 LU.
3. Add no running captions. Put text on screen only for chosen phrases: about 12 text items per minute overall, 22 per minute in the first 48 s.
4. Open cold on the speaker's first word; start the first graphic within 0.5 s (frame shrink at 0.47) and reach the main diagram within 7 s.
5. Keep the camera locked. Change the speaker's size only in fixed steps of x1.047 (levels 0.953 / 1.000 / 1.047 / 1.095), scaled about the frame centre.
6. At a speaker-to-speaker cut that starts a new sentence, punch one level in or out (27 times; 15 in, 11 out, one double). Mix directions so the scale stays within the four levels.
7. Leave some mid-sentence cuts as plain jump cuts with no scale change (about 13 in 22 minutes).
8. Inside a shot, use an eased zoom of two levels (x1.09 in or x0.915 out) lasting 0.46 s (11 frames) about once every 37 s of speaker time (about 22 times).
9. Zoom out just before text or icons appear beside the speaker (0.2-9 s before); zoom back in after they leave or on a turning line ("Now, here's a big pro tip").
10. Put a short low sound (about 0.2 s, 50-90 Hz, 3-6 dB under the voice) on every eased zoom, starting within 0.3 s of the zoom start. Put none on punch cuts, hard cuts or text.
11. Put the same low sound on fast camera moves inside graphics (snap reframes, whips, slides) and on large layout animations.
12. Change something on the speaker picture (cut, zoom, overlay in or out) every 2 s median; never leave the plain speaker untouched for more than about 18 s.
13. Split the runtime about 61% speaker / 39% full-screen graphic, in alternating segments of about 10 s median each (40 speaker segments, 39 graphic segments).
14. Enter a full-screen graphic with a hard cut to the empty dark canvas at the start of the sentence, then build the parts over 0.3-1.2 s. Leave with a hard cut back to the speaker at the next sentence. No wipes.
15. Build one signature diagram for the framework (here the ladder) and return to it at every section start, at the mid-point recap and at the final recap (12 visits, 13% of runtime).
16. Mark each section change the same way: one-line recap on the speaker, hard cut to the diagram on "All right", move the camera to the next step, show the step name within 1 s of it being said, hold 3-11 s, hard cut back to the speaker at the widest framing.
17. For a new term, pop the word in heavy white caps (7.6-16% of frame height) within 0.05-0.2 s of the word being spoken; second word on its own beat; hold 2-7 s.
18. For a takeaway sentence, add a lower-third caption at x 0.10, y 0.77-0.88: small heading, then 1-2 lines (about 3% high each) that paraphrase the point with the key phrase bold; type it on in under 1 s, hold about 8 s (5-13 s). About one every 90 s of speaker time.
19. For "X leads to Y" or "either A or B", put short labels at mid-height left and right of the head (3-4% high, key words violet), left first.
20. For a list, show each item only when it is named (three labels at 145.4-146.8; four numbered stops at 778.5, 796.6, 809.0, 820.5; three questions at 564.6, 570.6, 576.6). Between items cut back to the speaker for the explanation.
21. For a question the video is about to answer, blur and dim the speaker over 10 frames and type the question in the centre word by word in step with the voice; un-blur over 10 frames (3 times).
22. For a number about the speaker, use a small counter badge beside the head for about 2 s.
23. For a named person, story or study, show a photo, a source screenshot and a simple line drawing, and draw a circle on each noun as it is said (67.2-79.2).
24. For a named outside example, show the real clip in a rounded card on the canvas with a small source label in the card's top-left corner; type the viewer's questions over the dimmed clip.
25. For a worked example, shrink the speaker to a corner card (face about 10% of frame height), put the clip in the centre and a checklist of the framework at the side; tick one box per step; stop talking for 1-3 s to let the clip play; cut to the full-frame speaker for each reaction (6 stretches, 170 s).
26. Keep one accent colour (violet about #b577f3 on text, #5d0bba in glows) on a near-black canvas with a violet glow in the bottom corners; white text; rounded cards.
27. Time text to the voice: key words 0-0.2 s after the spoken onset; captions and labels within about 1 s; section names may lead by up to 2 s.
28. Recap twice: once after two thirds of the content (853.8-915, 61 s on the diagram with a growing list) and once at the end (1286-1312).
29. For the call to action, show a screen recording of the offer in a rounded card with a new screen every 0.5-3 s and the URL in a pill at the bottom; end on the speaker with a subscribe lower third for the last 3 s.
30. Cut on the script only: every cut should start a sentence, a list item, an example or a section (57 of 57 sampled cuts did).

---

## 13. Not determinable / measurement problems

**Measurement problems found by checking against frames**

- **"Slow pull out" / "slow push in" on speaker shots is mostly false.** `summary.json` gives slow pull-out 19% and slow push-in 1% of speaker time, and `shots.json` gives `zoom_total` 0.94-0.99 for shots #16, #26, #32, #110, #111, #115, #122. Background feature matching gives scale 1.000 from start to end of #16, #26, #32, #115, #122, and `face.h_end_over_start` is above 1 in most of them. The tracker is following the speaker's body, not the camera. The only real slow move is 751-763.7 (1.047 -> 1.000).
- **"Static 32%" understates it.** Shots labelled "eased zoom in/out" (41% of speaker time) are static except for one or more 0.46 s zooms.
- **Eased zoom factor is slightly under-read.** JSON median 1.085; direct measurement 1.087-1.095 in, 0.914-0.917 out.
- **"Longest picture change 102.7 s" (1029.2-1131.9) is wrong.** The switch to the live-example layout at 1055.2 is an animation inside shot #129, which is labelled a "punch x1.05" cut from 1048.05. Shots #129-131, #133, #135, #136, #139, #142, #145, #146 are also classed "flat graphic" although the speaker is visible in a corner card.
- **"Pop" cuts are mixed.** 62.69 and 280.20 are title words appearing; 64.40 is the title flickering out; 804.93 and 813.27 look like jump cuts on the speaker; 1092-1266 are changes inside the example clip.
- **"Jump" cuts inside graphics are camera snaps in an animation**, not edits of footage (28.82, 29.82, 31.36, 116.87, 705.91, 717.88, 860.28, 1287.20).
- **Cuts at 594-611 and 946-951 belong to the quoted clips**, and 1321-1338 to the screen recording. They raise the cuts-per-minute of "Level 3" (10.4) and "Summary" (21.9) without being talking-head edits.
- **OCR reads the hoodie.** Tracks "REPRESEN", "REPRESENT", "REPRESEIT" at x 0.61, y 0.84 are the print on the speaker's chest, not graphics. The OCR also reads the example clip's own yellow captions ("OFF", "BABE", "YEAH") and the community screenshots.
- **OCR misreads animated or glowing text**: "PAVL" / "JIAN" for PAVLOVIAN, "LCOP" for LOOP, "00000" (32% height) for the checklist boxes, "952K+/994K+/999B+" while the counters run.
- **OCR timing is coarse.** Text was sampled about once per second plus at picture events, so `=said` lead/lag values are good to about +/-0.5 s. Where a dense sheet was available the frame-accurate value is given instead. Text colours are glyph averages and read darker than the fill.
- **`shots.json` face size at shot #1 (14%) and the "eased zoom out x0.675"** describe the speaker frame shrinking into a card, not a camera move.
- **Weak sound events (585 of 648) should be ignored**: nearly all are 20-200 Hz at about -20 dB with the voice active and no picture event.
- **Event 28.37** could not be tied to a picture change with confidence.

**Not determinable**

- What the sounds are (whoosh, thump, riser). Only time, length, level and band are known.
- Whether there is a very quiet music bed in the last 25 s (stem rises about 5 dB to -42.4 dB under the voice).
- Whether the speech was sped up, and how many cuts in the raw speech are invisible. 225 wpm and 0.23 s median pauses fit either fast delivery or tight cutting.
- The native framing of the camera. Level 0.953 is the widest seen; it is not known whether that is the full sensor image or already a crop.
- Font names. The type is a geometric sans in the graphics and a heavy rounded sans for the big title words.
- How the lower-third captions leave (fade or cut): the text is too small on the dense sheets to see; they are gone within 0.8 s (last seen 92.2, gone by 93.0).
- Who the person in the third logo bubble at 958.5 is; the line names four competitors and the bubble shows a photo.
- Whether the single black frame at 105.36 is intended.
- Why the replay peaks sit where they do (re-watching versus chapter jumps).
