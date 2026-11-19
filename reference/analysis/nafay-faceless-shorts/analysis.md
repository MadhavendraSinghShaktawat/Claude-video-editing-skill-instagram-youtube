# Edit analysis: nafay-faceless-shorts

"I Found a way To Make Faceless YouTube Shorts for free (No subscription)", Nafay 3D, 672.6 s (11:13), 1920x1080, 60 fps.

Sources used: `summary.json`, `shots.json`, `audio.json`, `text.json`, `timeline.md`, `words.en.json` (English dub, times approximate), all 9 `shots/` sheets, all 10 `overview/` sheets (1 frame / 2 s), 8 sheets of the first 25 s at 15 fps (`dense/i15_*`), 30 fps sheets `dense/tA tB tC tD zA zB zC oc fc trA trB yt pu jA jB jC`, plus my own measurements on the source file: full-resolution frame grabs, a read of the Windows taskbar clock before and after every cut, a per-frame pixel-difference pass, and RMS level of the audio track. Where a statement rests on my own measurement it says "measured".

All times are seconds from the start of the file. "Dub" means the English dub transcript; its word times can be off by 1-2 s against the Hindi original, so every lead/lag against words is approximate.

**The one-paragraph summary:** this is a 22.5 s designed intro (speaker + motion graphics, 5 animated layout changes) followed by 650 s of completely raw, full-frame screen recording with live narration. After 22.5 s there is no speaker picture, no editor zoom, no box, no arrow, no blur, no music and exactly one added text overlay (0.75 s). The editing work after the intro is invisible: silence and waiting are cut out while the screen is static, and the recording jumps between five recording sessions.

---

## 1. Facts

| Item | Value | Source |
|---|---|---|
| Duration | 672.63 s | summary.json |
| Frame rate / size | 60 fps, 1920x1080 | summary.json, ffprobe |
| Views | 272,493 | summary.json |
| Detected cuts | 68 (6.1 / min): 26 hard, 20 pop, 14 jump, 7 transition, 1 punch | summary.json |
| Of those, real edits (my classification, section 9) | 17 proven, 1 unclear, 50 are only the screen changing | section 9 |
| Shot length | median 4.97 s, p10 0.84 s, p90 21.98 s, max 81.9 s | summary.json |
| Longest stretch between proven edits | 121.6 s (483.52-605.10) | summary.json `picture_change_every_s.max`, clock check |
| Transition length | median 0.38 s, p90 0.88 s (the 5 real ones: 0.32-0.52 s) | summary.json, shots.json |
| Picture classes (tool) | flat graphic 81.1 %, no face 11.4 %, small face 4.2 %, face 3.3 % | summary.json |
| Speaker actually on screen | 0.00-22.53 s only = 3.35 % of runtime | sheets |
| Raw full-frame screen recording | 22.53-672.63 s = 96.65 % of runtime | sheets |
| Frames identical to previous frame | 89.5 % (whole file) | shots.json `duplicate_frame_share` |
| Frames with no pixel change after the intro (taskbar excluded) | 65.5 % | measured |
| Eased zoom moves (tool) | 23: 14 are intro layout transitions/graphics, 9 are the Windows photo viewer zooming inside the recording. Editor zooms on the screen recording: 0 | shots.json + sheets zA/zB/zC |
| Big on-screen text tracks | 13 (1.2 / min); only the intro titles and one overlay at 218.9 s are added by the editor | summary.json, text.json, sheets |
| Loudness | -18.5 LUFS integrated, LRA 4.7 LU, true peak 0.0 dBTP | summary.json |
| Speech | 2528 dub words, 225 wpm overall, 260 wpm while speaking, voice active 86.6 % of runtime | summary.json |
| Voice pauses | 229 (20.4 / min), median 0.33 s, p90 0.43 s, max 0.89 s, 15 over 0.5 s, 0 over 1 s | summary.json |
| Music bed | none detected: bed -48.9 dB below voice (median), `bed_on_spans` empty, audible 5 % | summary.json |
| Sound-event candidates | 8 (0.7 / min), 3 strong; 6 of 8 are inside the first 19 s | audio.json |

---

## 2. Script structure

Lines are the English dub. "Mark" = what the edit does at that boundary.

| Start | Beat | Line (dub) | How the edit marks it |
|---|---|---|---|
| 0.0 | Hook | "If you want to make shorts like these, but you don't have a Claude subscription or ... you hit your limit super fast" | Opens on the speaker full frame for 0.33 s, then animated change to graphic layout with 4 example shorts (0.27-0.63) |
| 6.2 | Promise | "today's video is going to be perfect for you ... make shorts like this without using Claude" | Animated change back to full-frame speaker (6.97-7.40); big 2-line title builds word by word (10.13-11.87) |
| 11.9 | Tool | "We're going to use OpenCode ... a free alternative to Claude Code" | Animated change to graphic layout (12.53-12.97), comparison cards |
| 15.2 | Bonus | "I'm going to give you an OpenCode skill that lets you generate and automatically post videos like this every single day" | Graphic panel swaps inside the same layout (15.93-16.27), week calendar fills |
| 20.6 | Like CTA | "So drop a like on this video and let's get started" | Animated change to full-frame speaker (20.83-21.27) |
| 22.5 | Step 1: install OpenCode | "our very first step will be downloading an AI agent" | Hard cut speaker -> raw screen at 22.533. No title card, no step label |
| 50.1 | Step 2: get the skill from his site | "Next, you want to head over to naf3d.com" | Instant change of web page at 50.22 (cut or tab switch, not provable) |
| 66.1 | Step 3: open OpenCode, pick the free model | "After that, open up OpenCode ... select our model" | Hard cut at 65.25 (clock flips on the cut frame) |
| 97.7 | Step 3b: connect the free account | "Click the settings icon ... OpenCode console" | No edit; dialog opens in the recording |
| 122.8 | Step 4: drop the zip, write the prompt | "Once that's done, your model is connected. Now ... take that zip file" | Hard cut at 121.95 (clock 8:36 -> 8:37 on the cut frame) |
| 168.5 | It runs | "I'm going to hit send, and it's already started working" | Jump cut at 170.25: chat already holds long output and a second user message |
| 186.4 | Aside: the 6 styles | "By the way, I thought I'd quickly show you what styles you actually get" | Hard cut at 186.25 to a different recording (photo viewer, clock 6:32 AM, date 11/4 instead of 11/2) |
| 225.3 | Back: plan, "build it", voice note | "And then after that, it picked a topic and laid out the whole plan" | Hard cut back at 225.55 (clock 8:39 AM) |
| 253.8 | Wait | "So let's wait for it to finish, and I'll catch up with you then" | Hard cut at 256.48, clock 8:40 AM -> 11:49 AM |
| 256.7 | Result 1: the short | "And just like that ... our video is ready" | Same cut; the short is played in the app preview 269.4-284.5 with the speaker almost silent |
| 304.4 | Bridge to part 2 | "Now I want to show you something really interesting. How you can automate this entire process" | No edit; spoken over a static chat window (still 305.2-311.0 and 311.0-316.2) |
| 320.2 | Step 5: Zapier account + MCP server | "Okay, first you need to go to Zapier. Link's in the description" | Hard cut at 319.93, dark app -> white web page, clock 11:50 -> 12:01 |
| 387.1 | Step 6: paste config into OpenCode | "start a new session and tell it add this to OpenCode config" | Hard cut at 386.93, clock 12:03 -> 12:09 |
| 449.0 | Step 7: add the YouTube app in Zapier | "Our OpenCode setup is done. Now, we need to connect the YouTube app" | Hard cut at 449.58, clock 12:15 -> 12:17 |
| 483.9 | Step 8: tell it to upload | "And our entire setup is complete. Now, simply head back to OpenCode" | Hard cut at 483.52, clock 12:18 PM -> 7:08 AM (another session) |
| 508.4 | Explanation of the daily workflow | "Now, the automation works like this ..." | No edit for 80 s; agent output scrolls behind the talk |
| 605.4 | Result 2: uploaded | "And look, it uploaded the video" | Hard cut at 605.10 (clock flips on the cut frame), YouTube page opens in the app |
| 620.5 | Wrap | "And that was pretty much the entire automation" | none |
| 625.3 | Comment CTA | "If you have any questions ... let me know down in the comments" | none |
| 630.1 | Extra tip | "Also, one more thing ... long form videos too" | Browser panel closes at 629.47 (screen change) |
| 657.7 | Final CTA | "Go download that skill. That's the most important part" | none |
| 665.3 | Outro | "Thank you so much for watching ... Goodbye" (last word 672.0) | File ends 0.6 s later on the raw screen. No end card, no speaker, no fade |

Sponsor: no separate sponsor block. Zapier gets "Link's in the description" (321.7) and "I hope you go check out Zapier too" (669.0); whether that is paid is not determinable. The speaker's own site naf3d.com is the download source (50.1).

---

## 3. The rough cut

**Speech is tight.** From `audio.json` (Hindi voice stem, exact): 229 pauses, median 0.33 s, p75 0.38 s, p90 0.43 s, max 0.89 s, none over 1 s. Speech runs: median 0.92 s, p90 2.7 s, max 8.6 s. Voice is active 86.6 % of the runtime. Only 9 silences of 0.4 s or longer in the whole mix (86.98, 157.19, 160.45, 367.62, 377.25, 406.64, 408.08, 461.78, 471.03).

**The longest pauses sit where the hands are busy**, not between ideas: 160.40 (0.87 s, typing the prompt), 406.31 (0.89 s) and 408.04 (0.69 s) (typing and sending "add it to the global user config"), 394.29 (0.66 s, pasting config), 461.74 (0.63 s, search results loading), 377.23 (0.62 s, dialog opening), 273.21 / 279.51 / 281.91 (0.61 / 0.80 / 0.57 s, while the finished short plays).

**Playback speed is 1.0x.** Measured: the text caret in the app blinks every 0.53 s (e.g. 73.57, 74.07, 74.60, 75.13; 491.98 ... 505.78 in 26 equal steps of 0.531 s). 530 ms is the Windows default blink rate, so the recording is not sped up.

**Real time is nevertheless compressed about 2:1, by cuts.** Measured from the taskbar clock: one clock minute lasts this much video:

| Clock minute | Video span | Video seconds for 60 real seconds |
|---|---|---|
| 8:34 | 41.85-65.25 | 23.4 |
| 8:35 | 65.25-103.5 | 38.3 |
| 8:36 | 103.5-121.95 | 18.5 |
| 8:37 | 121.95-147.65 | 25.7 |
| 8:38 | 147.65-176.47 | 28.8 |
| 12:02 | 333.5-370.0 | 36.5 |
| 12:14 | 401.7-444.15 | 42.5 |
| 7:09 | 487.0-535.8 | 48.8 |
| 7:10 | 535.8-572.57 | 36.8 |
| 7:11 | 572.57-605.10 | 32.5 |

So 19 to 69 % of each real minute is missing even inside stretches where the cut detector found nothing. Because speed is 1.0x, the missing time was removed by cuts made while the screen was static (no visible jump). Two were caught in the act:

- 159.25 -> 159.50: the typed prompt jumps from "...a 20 second sho" to "...a 20 second short. choose a" in under 0.25 s (measured strip of the input box, 147.5-170.5).
- 161.75 -> 162.25: "choose any topic thrat y" becomes "choose any topic that you like" (the typo fix is cut out).

**Waiting is cut out, never sped up and never left in.** Every wait is a hard cut with a spoken bridge:

| Cut | Clock before -> after | What was removed | Spoken bridge (dub) |
|---|---|---|---|
| 65.25 | 8:34 -> 8:35 on the cut frame | download finishing, app launch | "It's about a 10 megabyte download, so it shouldn't take that long. After that, open up OpenCode." |
| 121.95 | 8:36 -> 8:37 on the cut frame | account dialog | "Once that's done, your model is connected." |
| 170.25 | 8:38 both sides | agent starting, a second prompt typed | "it's already started working ... I scrolled down and told it again" |
| 256.48 | 8:40 AM -> 11:49 AM | the whole video render | "So let's wait for it to finish, and I'll catch up with you then." / "And just like that, after a little bit, our video is ready." |
| 397.12 (not in timeline.md) | 12:09 -> 12:13 on the same frame as a 25,520-pixel jump | agent editing the config | "After that, as you can see, it says it has added Zapier MCP." |
| 472.30 (not in timeline.md) | 12:17 -> 12:18 on the same frame as a 16,832-pixel jump | account connect | "Let's connect it." |
| 605.10 | 7:11 -> 7:12 on the cut frame | the upload | "And now our video should actually get uploaded." / "And look, it uploaded the video" |

**Where speech stops while the screen works:** only once for more than a second. 269.4-283.2 the finished short plays in the app preview; dub word gaps there are 4.42 s (from 269.27), 2.97 s (274.01) and 4.45 s (278.82); mix level drops from about -21 dBFS to -33...-42 dBFS (measured, 1 s RMS). That is 14 s of result shown with the narrator out of the way.

**Where the screen stops while speech continues:** longest runs with zero pixel change (measured): 7.0 s from 636.0, 5.8 s from 305.2, 5.2 s from 311.0, 5.0 s from 110.5, 5.0 s from 321.5, 4.5 s from 538.2, 4.4 s from 139.9. The editor leaves these alone.

**Mistakes left in:** the repeated model-menu open/close at 70.35-97.85 (opened, closed at 83.72, reopened at 85.50), "I don't know why the video isn't playing in this browser. Oh, now it is" (610.7-613.6). The cut is for pace, not for polish.

---

## 4. Speaker footage

The speaker is on screen only during the first 22.53 s. After that there is no camera picture at all (the tool's "small face / pip" rows at 209, 605, 612 and 627 s are cartoon faces inside the recording, checked on the sheets).

| Span | Layout | Face height (share of frame) | Face centre |
|---|---|---|---|
| 0.00-0.27 | full frame | 41 % | 0.53, 0.39 |
| 0.63-6.97 | picture-in-picture, right | 21 % | 0.89, 0.45 |
| 7.40-12.50 | full frame | 41 % | 0.53, 0.40 |
| 12.97-20.83 | picture-in-picture, right | 22 % | 0.90, 0.45 |
| 21.27-22.52 | full frame | 40 % | 0.53, 0.39 |

Total: about 6.7 s full frame, 14.2 s picture-in-picture, 1.6 s in transitions.

**Picture-in-picture (measured on frames at 1.6, 15.6, 19.5 s):** portrait rounded rectangle on the right, about 405 x 574 px at 1920x1080 (21 % of frame width, 53 % of frame height), left edge at x = 0.774, right edge at 0.985 (about 29 px from the frame edge), top at y = 0.236, bottom at 0.767. Corner radius about 24 px. Thin light-blue border (about 3 px, sampled #b2ccef) and a soft shadow. It is a tighter crop of the same camera shot: head and shoulders plus the microphone.

**Camera moves on the speaker:** none that are not layout transitions. All `zoom_moves` in shots 0-5 start or end within 0.3 s of a layout transition (e.g. 0.20-0.43 x0.854, 7.23-7.45 x1.222, 12.52-12.77 x0.788, 21.10-21.35 x1.236); the one in between (11.02-11.32, x1.027) coincides with the text building over the picture. Inside the full-frame spans the framing is static. No punch-in cuts, no slow push.

**Trigger for going to the speaker full frame:** a sentence addressed directly at the viewer with nothing to show: the promise ("today's video is going to be perfect for you", 6.2) and the like request (20.6). **Trigger for shrinking him to picture-in-picture:** a sentence that names a thing that can be drawn ("shorts like these" 0.5; "use OpenCode" 12.1). **Trigger for leaving the speaker for good:** "let's get started" (ends about 22.4), hard cut at 22.533.

---

## 5. Screen-recording treatment

This is 96.65 % of the video and it is untreated.

| Question | Finding | Evidence |
|---|---|---|
| Editor zooms into the screen | 0 in 650 s | All 9 screen `zoom_moves` in shots.json are at 189.5-222.8 and are the Windows photo viewer enlarging the image: title bar, toolbar and taskbar stay the same size while the image grows (sheets zA, zB, zC; full frame at 218.5 shows the viewer's own "133 %" readout) |
| Zooms made inside the recording | 7 zooms on 7 image views (6 style sheets, one revisited), factor 1.19-1.30, 0.33-0.48 s each, 0.75-1.1 s after each image appears (first one 3.2 s after) | shots.json: 189.48-190.28 (x1.119 then x1.06), 196.57-197.05 x1.299, 199.85-200.32 x1.231, 204.65-205.03 x1.231, 210.10-210.47 x1.270, 215.02-215.38 x1.259, 222.42-222.75 x1.278 |
| Highlights, boxes, arrows, blur, spotlights | none | every shot sheet and overview sheet |
| Cursor | standard small Windows arrow, no enlargement, no click ring, no trail | full-resolution crops at 100 s and 160 s |
| Pointing | done live with the mouse; at 163.0-167.75 the speaker drags a text selection (blue) over the words he is reading out: "install this skill and" 163.25-163.5, "make a 20 second short. choo" 164.5-166.25, "choose any topic that you like" 166.75-167.75 | measured strip of the input box |
| Speed changes | none (caret blink 0.53 s throughout) | measured |
| Background, padding, rounded corners, device frame | none: the recording fills 1920x1080 edge to edge, Windows taskbar and clock visible at the bottom | full-resolution frames at 100, 160, 218.5 s |
| Size of text in the recording | body text about 14 px high at 1080p (1.3 % of frame height); nothing is enlarged for the viewer | frame at 160 s |
| Personal data | no blur anywhere; account pages are skipped by cutting ("I already have this connected", 106.8) rather than hidden | sheets, dub |
| How long the screen is left fully still | 65.5 % of post-intro frames have no change; longest fully still runs 7.0 s (636.0), 5.8 s (305.2), 5.2 s (311.0), 5.0 s (110.5, 321.5) | measured |
| Result playback | the finished short is played inside the app's preview pane, a 9:16 player about 14 % of frame width at x = 0.57-0.79; never cut out and shown full screen | sheets 004/005, motion boxes [0.57, 0.22, 0.79, 0.86] |

What changes the picture instead of an editor: scrolling (55.05, 360.3), dialogs opening over a dimmed app (70.35, 97.85, 376.97, 433.83, 458-472), switching application or site (opencode.ai dark page -> naf3d.com light page -> OpenCode dark app -> Zapier white pages). The light/dark alternation of the tools is the only visual variety: palette goes #100e0f (22.5) -> #f3f4f7 (50.2) -> #131313 (65.3) -> #f8f7f5 (319.9) -> #131313 (386.9) -> #f8f7f5 (449.6) -> #131313 (483.5).

---

## 6. Layouts

| # | Layout | Time | Share of runtime | Count | Example times |
|---|---|---|---|---|---|
| A | Speaker full frame, no graphics | 6.7 s incl. C | 1.0 % | 3 spans | 0.00-0.27, 7.40-12.50, 21.27-22.52 |
| B | Graphic layout: off-white canvas, title pill top-centre-left, animated panel on the left 60 %, speaker picture-in-picture on the right | 14.2 s | 2.1 % | 2 spans holding 4 panels | 0.63-6.97 (panels "Shorts Like These", "Claude Free Plan"), 12.97-20.83 (panels "Use OpenCode", "One OpenCode Skill") |
| C | Speaker full frame with 2-line title in the lower third | 2.3 s (inside A) | 0.3 % | 1 | 10.13-12.43 |
| D | Raw full-frame screen recording | 650.1 s | 96.65 % | 1 continuous run, 5 recording sessions | 22.53-672.63 |
| D1 | of which dark desktop app (OpenCode) | about 467 s | about 69 % | | 65.25-186.25, 225.55-319.93, 386.93-449.58, 483.52-672.63 |
| D2 | of which web pages (opencode.ai, naf3d.com, Zapier) | about 144 s | about 21 % | | 22.53-65.25, 319.93-386.93, 449.58-483.52 |
| D3 | of which photo viewer (style sheets) | 39.3 s | 5.8 % | | 186.25-225.55 |
| E | D with one black caption box | 0.75 s | 0.1 % | 1 | 218.88-219.63 |

Transitions between A and B take the remaining 1.6 s.

---

## 7. Motion-graphics catalogue

Everything here is in the first 22.5 s except item 12. Colours sampled from full-resolution frames. Entry/exit times read from 15 fps and 30 fps sheets, so +/- 0.03-0.07 s.

**Canvas (layout B).** Off-white #f6f4f2 with one wide, soft diagonal band in beige #ece5e0 running from lower left to upper right. It does not move.

| # | Type | Looks like | Trigger (dub) | Enter | Hold | Exit | Times |
|---|---|---|---|---|---|---|---|
| 1 | Title pill | White (#ffffff) rounded pill with soft shadow, centre x = 0.38, y = 0.20, 104 px high (9.6 % of frame); 2-3 words in a bold serif, cap height about 5 % of frame; first words near-black #101010, last word(s) blue #4a96ee; Title Case | names the topic of the panel under it | fade in 0.10-0.13 s | 1.6-4.6 s | cross-fades into the next title in about 0.13 s, or leaves with the layout | "Shorts Like These" 0.63-2.33; "Claude Free Plan" 2.47-6.97; "Use OpenCode" 12.83-16.0; "One OpenCode Skill" 16.2-20.9 |
| 2 | Row of example shorts | 4 portrait cards (9:16, about 16 % frame width each, rounded corners, white 6 px frame), each playing a clip of a finished short; dark pill bottom-centre "▶ 2.3M views" in white bold sans | "make shorts like these" (0.5-1.1) | cards arrive one at a time from 0.33, 0.47, 0.60, 0.77 (stagger about 0.13 s): each fades in tilted and settles upright in about 0.25 s; view counts count up (0.9M -> 2.3M) from 0.87 to about 1.6 | to 2.27 | slides left and fades, 0.20 s (2.27-2.47) | 0.33-2.47 |
| 3 | Plan card with struck-out row | White rounded card (x 0.14-0.54, y 0.24-0.42), row 1 "Subscription" in serif with a small icon | "you don't have a Claude subscription" (1.5-2.3) | card fades/scales in 2.60-2.80; at 3.07-3.13 a red line strikes through "Subscription" and a red x circle (#f05858) appears at the right end of the row | to 6.97 | leaves with the layout | 2.60-6.97 |
| 4 | Second row + usage meter | Row 2 "+ Free version"; under it a thin progress bar with "Usage" and a percentage | "if you use the free version of Claude" (3.3-4.4) | row fades in 3.73-3.87; bar fills 4.6-5.9 (1.3 s), colour green until about 55 %, yellow 5.40-5.53 (64-80 %), red from 5.60, 100 % at 5.93; percentage counts up with it | to 6.97 | with layout | 3.73-6.97 |
| 5 | Warning badge | Pale red pill under the card (centre 0.38, 0.80) with a red dot and "Limit reached" in red (#e48588 by OCR) | "you hit your limit super fast" (4.8-5.7) | fades in 6.20-6.33, about 0.3 s after the bar hits 100 % | 0.7 s | with layout | 6.20-6.97 |
| 6 | Full-frame title over the speaker | 2 centred lines in the lower third, bold serif, no box, no shadow visible: "Make Shorts" (white #f8f8f8 + blue #4a96ee), cap height about 11 % of frame, baseline y = 0.75; "without Claude" (white + blue) slightly smaller at y = 0.86. Title Case line 1, lower-case "without". Text spans x = 0.26-0.74 | "how to make shorts like this without using Claude" (9.6-11.4) | word by word, each word a 0.07-0.13 s fade: "Make" 10.13, "Shorts" 10.27, "without" 11.33, "Claude" 11.80 | complete for 0.6 s; whole thing 2.3 s | fades out in about 0.07 s at 12.40-12.47, before the layout change starts at 12.53 | 10.13-12.47 |
| 7 | Comparison cards | Two white rounded cards side by side (each about 28 % frame width): left "OpenCode / Open source coding agent" with a dark terminal icon, right "Claude Code / Anthropic's coding agent" in grey with an orange star (#e08050). Between them "alternative to" over a dashed arrow. Under left: green tick (#308848) + "Free". Under right: red x (#f05858) + "Needs a paid plan" | "use OpenCode ... a free alternative to Claude Code" (12.1-15.0) | staged: left card fades/scales in 13.00-13.27; "Free" badge 14.20-14.27; arrow draws left to right 14.40-14.67; right card 15.00-15.20; "Needs a paid plan" 15.33-15.40 | complete for 0.5 s | slides left and fades 15.93-16.13 (0.20 s) | 13.00-16.13 |
| 8 | Week calendar window | White rounded "app window" (x 0.04-0.72, y 0.26-0.72) with three grey dots, terminal icon and "Daily Shorts" in the title bar; 7 columns MON-SUN, each an empty portrait slot | "an OpenCode skill that lets you generate ..." (16.2-17.7) | fades in 16.53-16.73 | empty until 18.07 | with layout at 20.83 | 16.53-20.9 |
| 9 | Slots fill with shorts | One playing short thumbnail drops into each day | "generate" (17.7) / "and automatically" (18.1-18.4) | one per day at 18.13, 18.27, 18.40, 18.53, 18.67, 18.80, 18.93: stagger 0.13 s (8 frames), all seven in 0.8 s | 1.9 s | with layout | 18.13-20.9 |
| 10 | "Automatically" label | small pill under the window (0.38, 0.80), blue "+" and dark bold serif | "automatically post" (18.4-18.8) | fade 19.53-19.67 | 1.2 s | with layout | 19.53-20.9 |
| 11 | "Posted" ticks | small green tick + grey word under each of the 7 slots | "every single day" (19.9-20.3) | appear left to right 20.20-20.47 (about 0.04 s apart) | 0.4 s | with layout | 20.20-20.9 |
| 12 | Correction caption | Black rounded box about 495 x 130 px, centre 0.50, 0.48, white extra-bold geometric sans "Opencode*", cap height about 7 % of frame | the speaker says "tell Claude the name" (dub 219.2-219.4) while meaning OpenCode | hard on at 218.883 (frame 13133) | 0.75 s (45 frames) | hard off at 219.633 | 218.88-219.63 |

Not present anywhere: lower-third name tag, chapter/step title cards, progress bar, logo bug, subscribe animation, end screen, emoji, memes, b-roll, stock footage.

---

## 8. Script -> picture table

Lead/lag is picture event minus dub word time; dub drift makes anything under about 1 s uncertain. "-" = cannot be judged.

| Time | Spoken line (dub) | What the picture does | Job | Lead/lag |
|---|---|---|---|---|
| 0.0 | "If you want to make" | Speaker full frame, already talking on frame 0 | Start on a face, no logo | - |
| 0.3-1.0 | "shorts like these" | Speaker shrinks to the right; 4 example shorts with view counts pop in one by one | Show the result before anything else | cards start about 0.3 s before "shorts" (dub 0.6) |
| 2.3-3.1 | "you don't have a Claude subscription" | Cards slide out; plan card appears, "Subscription" gets struck through with a red x | Name the viewer's problem as a picture | strike about +0.8 s after the word (dub 2.3) |
| 3.7-3.9 | "if you use the free version of Claude" | Row "Free version" appears | Second problem, same card | about -0.1 s |
| 4.6-5.9 | "where you hit your limit super fast" | Usage bar fills green -> yellow -> red to 100 % | Make "limit" visible, 1.3 s of motion under one clause | bar starts about 0.3 s before "hit" (dub 4.9) |
| 6.2 | (end of clause) | "Limit reached" badge | Punch line of the bar | about +0.5 s after "fast" |
| 7.0-7.4 | "today's video is going to be perfect for you" | Graphic clears, speaker grows to full frame | Direct address = full face | starts about -0.1 s vs "going" (dub 7.1) |
| 10.1-10.3 | "how to make shorts like this" | "Make Shorts" fades in word by word over the speaker | The promise in 2 words | about +0.3 s |
| 11.3-11.9 | "without using Claude" | "without Claude" adds as line 2 | The twist of the title | about +0.5 s |
| 12.5-13.0 | "We're going to use OpenCode" | Title fades out, speaker shrinks right, title pill "Use OpenCode" | Back to show-and-tell | pill about +0.5 s after "use" (dub 12.1) |
| 13.0-14.3 | "which is a free" | OpenCode card, then green "Free" tick | Introduce the tool with its one selling point | "Free" badge about +0.5 s |
| 14.4-15.4 | "alternative to Claude Code" | Arrow draws, Claude Code card, red "Needs a paid plan" | Comparison in one glance | card about +0.3 s after "Claude" (dub 14.7) |
| 16.0-16.7 | "I'm going to give you an OpenCode skill" | Panel swaps; title "One OpenCode Skill"; empty week calendar | Second promise | title about -0.2 s vs "open code skill" (dub 16.3-16.8) |
| 18.1-18.9 | "that lets you generate" | 7 shorts drop into MON-SUN, 0.13 s apart | "Daily" shown as a filled week | about +0.4 s after "generate" (dub 17.7) |
| 19.5-20.5 | "automatically post videos like this every single day" | "Automatically" label, then 7 green "Posted" ticks | Each spoken claim gets its own small element | label about +1.1 s after the word (dub 18.4); ticks land on "every single day" |
| 20.8-21.3 | "So drop a like on this video" | Speaker grows to full frame | Ask face to face | starts about +0.1 s |
| 22.53 | "All right, our very first step" | Hard cut to opencode.ai, raw screen | Tutorial begins; no step card | cut on the first word |
| 33.8-34.7 | "Let's click this download button right here" | He clicks; page changes to the download list at 34.73 | Do what is said | click about +0.9 s after "click" |
| 50.2 | "Next, you want to head over to naf3d.com" | Dark page -> light page | New step = new site; brightness change does the work of a title card | change on "Next" |
| 55.1-58.6 | "just scroll down a bit and right here, you'll see the faceless short skill" | Page scrolls to the skill card | Mouse scroll is the only "camera move" | scroll starts about 0.9 s before "scroll" (dub 56.0) |
| 65.25 | "it shouldn't take that long. After that, open up OpenCode" | Hard cut to the OpenCode app | Skip the download | cut about 0.9 s before "After that" (dub 66.1) |
| 70.4 | "you'll see quite a few model options" | Model list opens | Show the options being talked about | about +0.4 s |
| 85.5-92 | "select the model right here, click on it, search for GLM" | List reopens, "glm" typed, free model chosen | Narrated click-through | - |
| 97.9 | "Click the settings icon right here" | Settings dialog opens | Narrated click-through | about +0.2 s |
| 106.8-121 | "I already have this connected, but ... you just need to create an account" | Dialog stays as it is for about 15 s (still 110.5-115.5) | Sign-up explained in words, not shown | - |
| 121.95 | "Once that's done, your model is connected" | Hard cut to the app's empty start screen | Skip the account step | cut about 0.8 s before the line |
| 128.2-131.9 | "You can see my downloaded file right here. We just drag it right into OpenCode" | Explorer window opens, file is dragged onto the prompt box | Show the physical action | drag ends on "drag" |
| 133.6-146 | "make sure the effort level is set to high" | Effort menu open | Side note shown on the control itself | - |
| 150-162 | "tell it, install this skill ... make a 20-second short. Choose any topic" | The prompt is typed live; two small jump cuts (159.5, 162.0) | Viewer can copy the prompt letter by letter | typing runs with the words |
| 163-168 | "we told it to pick any topic on its own" | Mouse selects the phrases in blue as they are read | Live highlight without any editing | - |
| 170.25 | "it's already started working" | Jump: chat is full of agent output | Skip the wait | cut about +1 s after "send" (dub 169) |
| 186.25 | "By the way, I thought I'd quickly show you what styles you actually get" | Hard cut to a style-sheet image in the photo viewer (other session) | Insert that answers "what will I get" before the long wait | cut about 0.2 s before the line |
| 189.5-222.8 | "this is our first style ... 2D explainer ... Rick's Clips ... mystery ... Zack D films ... Stickman" | A new image every 3.6-9.2 s; each is zoomed about x1.25 in the viewer about 0.8 s after it appears | Six examples in 39 s; the fastest passage of the tutorial | each image change within about 0.5 s of "this one" / "then" |
| 218.9 | "All you have to do is tell Claude the name" | Black box "Opencode*" for 0.75 s | Correct a slip without re-recording | on the wrong word (dub 219.4, about -0.5 s) |
| 223.5-225.5 | "And it'll make your video in that exact style" | Three images flipped in 2 s (223.47, 224.00, 224.58) | Recap by flicking back through | - |
| 225.55 | "And then after that, it picked a topic and laid out the whole plan" | Hard cut back to the chat | Resume the story | cut on "And then" |
| 256.48 | "And just like that, after a little bit, our video is ready" | Hard cut: chat on the left, video preview pane on the right (3 h 9 min later by the clock) | Skip the render | cut about 0.2 s before the line |
| 260.4 | "it even gave us a cover frame" | Cover image appears in the preview | Show the thumbnail | about +0.6 s |
| 269.4-283.2 | (almost nothing said) | The short plays in the small preview pane | Let the result speak; narrator stays out for 14 s | - |
| 304.4-319 | "Now I want to show you something really interesting. How you can automate this entire process" | Static chat window (no change 305.2-316.2) | Part-2 pitch delivered over a dead screen; no graphic | - |
| 319.93 | "Okay, first you need to go to Zapier" | Hard cut, dark app -> white Zapier page | New part marked only by the brightness flip | cut about 0.3 s before the line |
| 356.8-364.6 | "they have tons of apps available" | Jumps to the app directory, fast scroll down and back up | Proof by scrolling a long list | on the line |
| 377.0 | "it'll basically show us the instructions" | Modal with the config opens | Show the thing to copy | about -0.5 s |
| 386.93 | "start a new session and tell it add this to OpenCode config" | Hard cut to the empty app | Change of tool | cut on the line |
| 397.1 | "as you can see, it says it has added Zapier MCP" | Hidden cut: reply is suddenly there | Skip the agent's work | about -0.9 s |
| 449.58 | "Our OpenCode setup is done. Now, we need to connect the YouTube app" | Hard cut to the Zapier server page | Change of tool | cut about +0.6 s into the line |
| 483.52 | "And our entire setup is complete. Now, simply head back to OpenCode" | Hard cut to the chat (another morning by the clock) | Change of tool | cut about 0.4 s before the line |
| 508-588 | "Now, the automation works like this ..." (80 s of explanation and advice) | Chat sits there; agent output arrives at 536.3, 554.6, 572.7, 579.5 | Talk through the wait instead of cutting it | - |
| 588.1-603 | "it's asking what the shorts visibility should be ... Let's go with comedy and then hit submit" | Question card appears in the chat, he clicks answers | Back to action after the talk | card appears on the line |
| 605.10 | "And look, it uploaded the video" | Hard cut: YouTube page inside the app | Payoff of part 2 | cut about 0.3 s before the line |
| 612.0-627 | "Oh, now it is ... our video has been uploaded to our channel" | The short plays on the YouTube page | Proof | - |
| 629.5-672 | "Also, one more thing ... Go download that skill ... Goodbye" | Chat window, slow scrolling, still for 7.0 s from 636.0 | 43 s of outro talk over a nearly static screen | - |

---

## 9. Why each cut is there

All 68 rows of `timeline.md`, numbered by the shot they start. Method: sheets for every cut; taskbar clock read 0.25 s before and after every cut after 22 s; 30 fps sheets for the unclear ones.

### Real edits: 17

| # | Time | Class | Evidence |
|---|---|---|---|
| 1 | 0.43 | go to graphic layout | animated, 0.27-0.63 (sheet tA) |
| 2 | 2.33 | intro montage beat (panel swap inside the layout) | 2.27-2.53 (i15_001) |
| 3 | 7.22 | go to speaker | animated, 6.97-7.40 (tB) |
| 4 | 12.77 | go to graphic layout | animated, 12.53-12.97 (tC) |
| 5 | 21.08 | go to speaker | animated, 20.83-21.27 (tD) |
| 6 | 22.53 | back to screen (first and only time) | hard cut, 1 frame (i15_008) |
| 10 | 65.25 | new step + remove waiting | clock 8:34 -> 8:35 on the cut frame; site -> app |
| 15 | 121.95 | remove waiting (account step skipped) | clock 8:36 -> 8:37 on the cut frame; dialog gone |
| 18 | 170.25 | remove waiting | chat suddenly contains long output and a second user message (sheet 003) |
| 19 | 186.25 | insert starts (style tour) | clock 8:39 AM -> 6:32 AM, date 11/2 -> 11/4 |
| 29 | 225.55 | insert ends | clock 6:33 AM -> 8:39 AM |
| 30 | 256.48 | remove waiting (render) | clock 8:40 AM -> 11:49 AM (jC) |
| 40 | 319.93 | new step (part 2, Zapier) | clock 11:50 AM -> 12:01 PM |
| 49 | 386.93 | new step (back to app) | clock 12:03 -> 12:09 |
| 56 | 449.58 | new step (to Zapier) | clock 12:15 -> 12:17 |
| 57 | 483.52 | new step (back to app) | clock 12:18 PM -> 7:08 AM |
| 62 | 605.10 | remove waiting (upload) | clock 7:11 -> 7:12 on the cut frame |

By class: new step 5 (#10, 40, 49, 56, 57), remove waiting 4 (#15, 18, 30, 62), insert in/out 2 (#19, 29), go to graphic layout 2 (#1, 4), go to speaker 2 (#3, 5), intro montage beat 1 (#2), back to screen 1 (#6). Emphasis zoom: 0.

### Unclear: 1

| # | Time | What | Why unclear |
|---|---|---|---|
| 8 | 50.22 | opencode.ai -> naf3d.com in one frame, at "Next, ..." | clock is 8:34 on both sides; an instant tab switch and a cut look the same |

### Not edits, only the screen changing: 50

| # | Time | What happens on screen |
|---|---|---|
| 7 | 34.73 | click on Download, page changes |
| 9 | 55.05 | smooth page scroll (jA) |
| 11, 13 | 70.35, 85.50 | model list opens over dimmed app |
| 12 | 83.72 | model list closes |
| 14 | 97.85 | settings dialog opens |
| 16 | 128.18 | Explorer window finishes loading thumbnails |
| 17 | 131.20 | file dragged onto the prompt; Explorer window disappears in one frame at 131.83 (jB) - a small cut there is possible |
| 20-28 | 195.45, 199.05, 203.90, 209.32, 214.20, 221.38, 223.47, 224.00, 224.58 | next/previous image in the photo viewer (zoom resets each time; clock stays 6:33) (fc) |
| 31, 32, 33, 39 | 260.37, 266.95, 269.43, 284.55 | preview pane: cover frame loads, goes black, video starts, video back at its first frame |
| 34-38 | 273.65, 276.95, 279.92, 282.38, 283.65 | scene cuts inside the short that is playing |
| 41 | 336.03 | Zapier sidebar expands |
| 42, 43, 45, 46 | 340.13, 356.78, 364.58, 367.33 | page navigation inside Zapier |
| 44 | 360.32 | fast scroll back to top (trA) - flagged "transition" |
| 47 | 374.43 | hover tooltip appears (trB) - flagged "transition" |
| 48 | 376.97 | modal opens over dimmed page |
| 50, 58 | 408.38, 491.52 | message sent, moves into the chat |
| 51-54 | 409.88, 414.85, 415.22, 415.47 | agent reply streaming in |
| 55 | 433.83 | MCP dialog opens over dimmed app |
| 59 | 506.25 | chat reflows (caret blink phase unbroken 491.98-506.85, so no cut) |
| 60, 61 | 588.12, 596.90 | question card appears / next question |
| 63-66 | 611.18, 611.35, 612.32, 612.38 | YouTube player loading, then playing (yt) |
| 67 | 627.18 | chat panel scrolls (flagged "punch x0.977") (pu) |
| 68 | 629.47 | browser panel closed |

### Edits the detector did not list (found by me)

| Time | Evidence | Class |
|---|---|---|
| 16.0-16.3 | "Use OpenCode" panel slides out, "One OpenCode Skill" fades in (i15_005/006) | intro montage beat |
| 159.47 | typed text jumps by 12 characters in under 0.25 s | remove waiting (typing) |
| about 162.0 | typo disappears between 161.75 and 162.25 | remove mistake |
| 397.12 | clock 12:09 -> 12:13 on the same frame as an isolated 25,520-pixel change | remove waiting |
| 472.30 | clock 12:17 -> 12:18 on the same frame as an isolated 16,832-pixel change | remove waiting |
| many more | clock minutes last 18-49 s of video (section 3) | silence/wait removal on a static screen; positions not determinable |

So the honest rate is: 17 visible edits in 672.6 s = 1.5 per minute overall; 5 of them in the first 22.5 s (13 per minute) and 12 in the remaining 650 s (1.1 per minute, one every 54 s).

### Longest stretches with no proven edit

| Span | Length | What is said (dub) |
|---|---|---|
| 483.52-605.10 | 121.6 s | upload command, then "Now, the automation works like this ... OpenCode doesn't have a scheduled task feature ... every morning you open OpenCode and tell it ... your own creativity is that one crucial thing ... The daily limit is enough to get you one short made for free", then the visibility and category questions. By the clock at least 11 s were removed inside it |
| 605.10-672.63 | 67.5 s | result, wrap, comment CTA, long-form tip, final CTA, goodbye |
| 319.93-386.93 | 67.0 s | Zapier account, MCP servers, app directory, create server, copy config |
| 256.48-319.93 | 63.5 s | cover frame, the short plays, "we did it all on a free model", pitch for part 2 |
| 65.25-121.95 | 56.7 s | model choice, free account |
| 397.12-449.58 | 52.5 s | global config, MCP check, authorise |

Longest single detected shot: #59, 506.25-588.12 (81.9 s).

---

## 10. On-screen text and captions

There are no subtitles/captions of the speech anywhere (the caption-like words at 269-285 and 612-627 belong to the short being played).

Added text, complete list:

| Text | Time | Size (share of frame height) | Position (centre) | Colour | Case / weight / face | Animation | On screen | Relation to speech |
|---|---|---|---|---|---|---|---|---|
| "Shorts Like These" | 0.63-2.33 | cap height about 5 %, pill 9.6 % | 0.38, 0.20 | #101010 + #4a96ee on white pill | Title Case, bold serif | fade in about 0.1 s; cross-fade to next | 1.7 s | repeats spoken words; OCR lead -0.29 s |
| "Claude Free Plan" | 2.47-6.97 | same | 0.38, 0.20 | same | same | cross-fade in 0.13 s | 4.5 s | paraphrase ("free version of Claude") |
| "Subscription" (struck), "Free version", "Usage", "100%" | 2.6-6.97 | 3-4.5 % | 0.17-0.60, 0.38-0.58 | #121212 text; strike and x red #f05858 | Sentence case, serif labels, small sans for "Usage" | fade in; strike drawn at 3.07 | 3-4 s | "Free version" lags the word by about +0.4 s (OCR) |
| "Limit reached" | 6.20-6.97 | 3.9 % | 0.38, 0.80 | red #e48588 on pale red pill | Sentence case, bold serif | fade 0.13 s | 0.8 s | paraphrase of "hit your limit" |
| "Make Shorts" | 10.13-12.47 | 12.4 % (OCR), cap height about 11 % | 0.50, 0.70 | #f8f8f8 + #4a96ee, no box | Title Case, bold serif | built word by word, 0.07-0.13 s fade per word | 2.3 s | repeats spoken words, about +0.3 s |
| "without Claude" | 11.33-12.47 | 13.1 % (OCR incl. descenders) | 0.50, 0.86 | #f8f8f8 + #4a96ee | lower-case first word, bold serif | built word by word | 1.1 s | repeats spoken words, about +0.45 s |
| "Use OpenCode" | 12.83-16.0 | cap about 5 % | 0.38, 0.20 | #101010 + #4a96ee | Title Case, bold serif | fade in 0.13 s | 3.2 s | repeats "use OpenCode" |
| card labels "OpenCode / Open source coding agent", "Claude Code / Anthropic's coding agent", "alternative to", "Free", "Needs a paid plan" | 13.0-16.1 | names 5.8 % / 4.8 %, sub-lines about 2.5 % | 0.19, 0.55 and 0.58, 0.55 | #12100f; "Claude Code" grey #8f8b89; tick #308848; x #f05858 | names bold serif, sub-lines regular sans | staged fades (section 7) | 1-3 s | "Claude Code" card about +0.85 s after the word (OCR) |
| "One OpenCode Skill" | 16.2-20.9 | cap about 5 % | 0.36, 0.20 | #100d0c + #4a96ee | Title Case, bold serif | cross-fade 0.13 s | 4.2 s | paraphrase |
| "Daily Shorts", MON-SUN, "Automatically", "Posted" x7 | 16.5-20.9 | 2-4.4 % | window 0.38, 0.49; label 0.38, 0.80 | dark grey; ticks green | sans, day names UPPER CASE; "Automatically" bold serif | fades, ticks staggered | 0.4-4 s | "Automatically" about +1.1 s after the word |
| "Opencode*" | 218.88-219.63 | cap about 7 %, box 12 % | 0.50, 0.48 | white on black rounded box | extra-bold geometric sans, a different face from the intro | hard on, hard off | 0.75 s (45 frames) | corrects the spoken word "Claude" |

Rules that follow from the table: titles are 2-3 words (median 2, p90 3, summary.json); the last word or two carries the single accent colour; nothing is ALL CAPS except the day names; text never sits over the screen recording except the one correction.

---

## 11. Transitions

| Kind | Frames (60 fps) | Where | What happens |
|---|---|---|---|
| Animated layout change, full-frame speaker <-> picture-in-picture | 19-31 frames by the detector (0.32-0.52 s); visibly about 22-26 frames | 0.27-0.63 (to pip), 6.97-7.40 (to full), 12.53-12.97 (to pip), 20.83-21.27 (to full) | The speaker picture itself scales and moves between full frame and the rounded portrait box on the right, with ease in and out; corners round as it shrinks; the off-white canvas is revealed behind it; graphics fade in/out and slide left during the move |
| Panel swap inside the graphic layout | 12 frames out (0.20 s), then next panel fades in 0.13-0.27 s later | 2.27-2.80, 15.93-16.73 | Old panel slides left and fades; title cross-fades; new panel fades/scales in. The picture-in-picture does not move |
| Hard cut | 1 frame | 22.53 and all 11 real edits after it | No dissolve, no wipe, no zoom, no sound |
| Hard pop on/off of a text box | 1 frame | 218.88, 219.63 | - |

The two rows the detector labels "transition" at 360.32 and 374.43 are a browser scroll and a tooltip (sheets trA, trB), not edits.

---

## 12. Sound

**Music:** none found. Non-voice stem level per 30 s is between -66.2 and -72.5 dBFS for the whole video, i.e. 45.6 to 51.9 dB below the voice; `bed_on_spans` is empty; `audible_bed_share` 0.05. The first 30 s are the least quiet (-45.6 dB below voice), which fits the few effects there.

**Level:** integrated -18.5 LUFS, range 4.7 LU. Measured RMS: intro 0-22.5 s -16.8 dBFS, tutorial sections -20.0 to -21.9 dBFS, so the intro is about 3-5 dB louder than the rest.

**Sound-event candidates (all 8):**

| Time | Length | Band | Level vs voice | Strong | On screen at that moment |
|---|---|---|---|---|---|
| 0.43 | 0.03 s | broadband, 835 Hz centre | -23.0 dB | no | middle of the first layout change (0.27-0.63) |
| 7.03 | 0.24 s | broadband, 983 Hz, 120 ms attack | -14.3 dB | no | start of the change to full-frame speaker (6.97-7.40); voice active only 38 % of it |
| 12.77 | 0.10 s | broadband, 1673 Hz | -15.8 dB | no | middle of the change to picture-in-picture (12.53-12.97) |
| 14.27 | 0.04 s | low, 115 Hz | -7.8 dB | yes | green "Free" tick appears (14.20-14.27) |
| 16.16 | 0.05 s | broadband, 1531 Hz | -20.3 dB | no | title swaps to "One OpenCode Skill" (16.13-16.27) |
| 18.17 | 0.30 s | low, 112 Hz | -12.1 dB | yes, ★ | first short drops into the MON slot (18.13) |
| 276.46 | 0.03 s | low, 49 Hz | -12.5 dB | yes | inside the short playing in the preview, no voice; belongs to the recording, not the edit |
| 396.30 | 0.03 s | broadband, 1906 Hz | -15.5 dB | no | message sent in the app (motion 396.25), 0.8 s before the hidden cut; likely a key or click picked up by the microphone |

Six of six intro candidates fall within 0.1 s of a graphic event, so the intro most likely carries quiet whoosh/pop effects at about -8 to -23 dB relative to the voice. All six overlap speech (voice active 38-100 %), so the two low ones could also be plosives; I cannot separate them by ear from data. After 22.5 s there is no added sound at all: `cuts_with_sfx_share` is 0.0 for every cut kind.

**The short's own audio:** during 269.4-283.2 the mix sits at -33 to -42 dBFS (measured), 12-20 dB under the narration level. Whether that is the short's soundtrack captured quietly or room noise is not determinable from the stems.

**Silences:** 82 in the mix, the longest 0.81 s (160.45). No silence of 1 s or more anywhere, including at the 12 hard cuts after the intro.

**Start and end:** speech starts on frame 0; the last word ("Goodbye") starts at 672.0 and the file ends at 672.63. No music sting, no fade.

---

## 13. Rules to reproduce this edit

Each rule carries the number it was measured from.

**Intro (first 22.5 s, 3.3 % of runtime, most of the editing effort)**

1. Start on the speaker's face, full frame, mid-sentence, on frame 0. Hold it 0.3 s or less before the first graphic move (first move starts at 0.27 s).
2. Keep the intro to about 22 s and give it 5 animated layout changes: one every 4.5 s on average (0.3, 2.3, 7.0, 12.5, 20.8).
3. Use two speaker layouts only: full frame (face 41 % of frame height, centre 0.53, 0.39) and a portrait picture-in-picture on the right (405 x 574 px at 1080p = 21 % x 53 % of the frame, left edge at x = 0.774, 29 px from the right edge, radius about 24 px, 3 px light-blue border #b2ccef, soft shadow; face 21 % of frame height).
4. Move between them by scaling the speaker clip itself with easing over 0.37-0.43 s (22-26 frames at 60 fps). Never hard-cut between speaker layouts.
5. Full frame is for sentences aimed at the viewer (promise at 6.2, like request at 20.6). Picture-in-picture is for sentences that name something drawable (examples at 0.5, tool at 12.1, schedule at 16.2).
6. Graphic canvas: off-white #f6f4f2 with one static beige diagonal band #ece5e0. One accent colour, blue #4a96ee, plus near-black #101010, white cards, green #308848 for "yes", red #f05858 for "no".
7. Each graphic panel gets a title pill at (0.38, 0.20): white, 104 px high (9.6 % of frame), 2-3 words in bold serif Title Case, the last word(s) in the accent blue. Cross-fade titles in 0.13 s.
8. Build each panel in stages, one element per spoken phrase, 0.1-0.3 s fade each, landing within about 0.5 s of the phrase (strike-through at 3.07, row at 3.73, bar 4.6-5.9, badge at 6.20; card 13.0, tick 14.2, arrow 14.4, second card 15.0, cross 15.33).
9. Repeated items enter staggered by 0.13 s (8 frames): 4 example cards from 0.33, 7 calendar thumbnails from 18.13.
10. Show a number or a state changing rather than stating it: view counts counting up (0.87-1.6), a usage bar filling over 1.3 s and changing green -> yellow -> red at about 55 % and 85 %.
11. Hold a finished panel 0.5-0.7 s, then clear it by sliding left and fading over 0.20 s.
12. One big title over the full-frame speaker for the promise: 2 lines, bold serif, cap height about 11 % of frame height, lower third (y = 0.70 and 0.86), white with the key noun in blue, built word by word (0.07-0.13 s per word), total 2.3 s, faded out 0.07 s before the next layout move.
13. Put a quiet effect on each graphic event in the intro, about 8-23 dB under the voice and 0.03-0.3 s long (6 candidates in 19 s). No music. Make the intro about 3-5 dB louder than the tutorial (-16.8 vs about -21 dBFS RMS).
14. End the intro with "let's get started" on the full face and hard-cut to the screen on the next word (22.533).

**Tutorial body (650 s, 96.7 % of runtime)**

15. Show the screen recording raw and full frame: no padding, no rounded corners, no background, no speaker inset, no zoom, no boxes, no arrows, no blur, no captions, no music, no effects.
16. Keep playback at 1.0x. Do not speed up typing or waiting (caret blink stays 0.53 s).
17. Cut silence so that no voice pause is longer than 0.9 s; aim for a median of 0.33 s and p90 of 0.43 s. Make these cuts while the screen is static so they cannot be seen. Expect to remove about half of the recorded time (one clock minute = 18-49 s of video).
18. Remove every wait with a single hard cut and let the narration carry it: a line before ("let's wait for it to finish, and I'll catch up with you then", 253.8) and a line after ("just like that, after a little bit, our video is ready", 256.7). Four visible waits were removed this way (121.95, 170.25, 256.48, 605.10) and at least two more invisibly (397.12, 472.30).
19. Mark a new step only by the hard cut to the other tool. 5 step cuts (65.25, 319.93, 386.93, 449.58, 483.52), each within about 1 s of a sentence that starts with "After that", "Okay, first", "Now" or names the next tool. No step title card.
20. Visible edits after the intro: about 1.1 per minute (12 in 650 s). Stretches of 50-120 s with no visible edit are normal (longest 121.6 s).
21. Leave the screen fully still under narration for up to 7 s at a time; 65 % of tutorial frames have no pixel change.
22. Pointing is done in the recording, not in the edit: mouse movement, scrolling, and dragging a text selection across the words being read (163-168 s).
23. When a set of example images must be shown, record them in an image viewer and step through: 6 images in 39 s (3.6-9.2 s each), each enlarged about x1.25 (1.19-1.30) over 0.33-0.48 s roughly 0.8 s after it appears. Place this insert just before the longest wait (186.25-225.55, wait cut at 256.48).
24. Insert pickup recordings with plain hard cuts on both sides (186.25 and 225.55); do not try to hide that it is a different session.
25. Play the finished result inside the tool where it appears, at its real size (preview pane about 14 % of frame width), and stop talking for it: 14 s with the narration out (269.4-283.2).
26. Fix a spoken slip with one text box instead of a re-take: black rounded box about 495 x 130 px in the frame centre, white extra-bold sans with an asterisk, hard on and off, 0.75 s (45 frames), placed on the wrong word (218.88).
27. Leave small mistakes and retries in (model menu opened twice 70-98 s; "why isn't the video playing ... oh, now it is" 610.7-613.6).
28. Skip sign-up and account screens by cutting and saying so ("I already have this connected", 106.8) rather than blurring.
29. Alternate bright and dark tools when the workflow allows it; the brightness flip is the only visual chapter marker (dark 22.5, light 50.2, dark 65.3, light 319.9, dark 386.9, light 449.6, dark 483.5).
30. End on the screen with the last spoken word; cut the file 0.6 s after it (last word 672.0, end 672.63). No end card, no return to the speaker.

---

## 14. Not determinable / measurement problems

**Not determinable**

- Whether narration was recorded live with the screen or added later. The mouse selecting words as they are read (163-168 s) and the live reaction at 610.7 point to live, but this is inference.
- The exact position and number of the invisible silence cuts in the screen recording. Only their total effect (clock compression) and four instances (159.47, about 162.0, 397.12, 472.30) are proven.
- Whether cut #8 at 50.22 is an edit or a tab switch.
- Whether a few frames were removed at 131.83 (Explorer window vanishes in one frame).
- Names and sources of the intro sound effects; whether the two low-band events (14.27, 18.17) are effects or plosives. Only time, length, band and level are known.
- Whether the quiet audio during the short's playback (269.4-283.2) is the short's soundtrack.
- Font names. Described only as "bold serif" (intro) and "extra-bold geometric sans" (correction box).
- Easing curve of the layout transitions beyond "eases in and out"; 30 fps sheets are too coarse for a curve.
- What the speaker actually says in Hindi at any moment; all quoted lines are the English dub.
- Whether Zapier is a paid sponsor.
- How much real time the sessions took. The clock shows the main session at 8:33-8:40 AM, the result at 11:49 AM, part 2 at 12:01-12:18 PM, the last part at 7:08-7:13 AM and the style insert at 6:32-6:33 AM on a later date (11/4 vs 11/2), but dates were read in only two frames.

**Measurement problems found**

- `summary.json` `eased_zoom_moves` (n = 23, 2.1 / min, factor median 1.172) is filed under `camera_on_face_shots` but none is a camera move on the face: 14 are intro layout transitions and graphics, 9 are the photo viewer zooming inside the recording. A future editor must not read this as "zoom into the screen 2 times a minute". The correct figure for editor zooms is 0.
- `picture_share_of_runtime` "small face / pip" 4.2 % and "face" 3.3 %: after 22.5 s every "face" is a cartoon character in the recording or in a thumbnail (shots 23, 62, 66, 67 and face detections in shots 9, 16, 20, 25, 28). Real speaker time is 3.35 % in total, of which picture-in-picture is about 2.1 %.
- Cut kinds: 50 of 68 detected cuts are not edits (all 20 "pop", 12 of 14 "jump", 2 of 7 "transition", the 1 "punch", 15 of 26 "hard"). `cuts.per_min` 6.1 overstates the edit rate about fourfold; the visible edit rate is 1.5 / min.
- The detector missed the panel swap at 16.0-16.3 and the two clock-proven cuts at 397.12 and 472.30.
- `cut_vs_speech` says `timing_words_are_original_speech: true`, but the word file is the English dub. The shares "between words 1.0 / after sentence end 0.0" should not be used.
- `text.repeats_spoken_words_share` (0.38) and `appears_vs_word_s` (median +0.29 s) compare OCR text with dub words; treat as rough. They also mix editor titles with UI text ("opencode", "zapier", "MCP Server").
- `text.big_tracks` = 13 includes UI text and words inside the played short ("NEWSPAPER" 18.7 %, "EMUWAR"). Editor-added big text is 6 titles in the intro plus "Opencode*".
- OCR colours for titles are blends of two-colour text (e.g. "Shorts Like These" #b5b3b2); the hex values in this file were sampled from pixels instead.
- `sfx.strong_on_picture_event_share` 0.33 undercounts: by eye, both strong intro events and all four weak ones sit on graphic events; the third strong event (276.46) is inside the played short.
- `duplicate_frame_share` 0.895 is for the whole file with the tool's threshold; my stricter per-frame pass (taskbar excluded, threshold 14/255 on a half-size frame) gives 65.5 % unchanged frames after the intro because the blinking caret and cursor count as change.
- Dense sheets at 15 fps were used for the intro element timings, so those are +/- 0.07 s; transition boundaries were read from 30 fps sheets (+/- 0.03 s) and from shots.json.
