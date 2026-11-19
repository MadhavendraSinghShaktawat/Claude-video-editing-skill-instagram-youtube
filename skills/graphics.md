# Step 3: motion graphics

A graphic is there to explain something, to list things, to prove something, or to mark where the video is. If a sentence does none of those, stay on the speaker.

Evidence: section 6 ("Motion-graphics catalogue") and the script-to-picture table in each `reference/analysis/<slug>/analysis.md`, `graphics.json` beside them (285 catalogued instances with the line that triggered each), and the concept cards in `reference/motion-graphics/`.

## 1. Decide: does this sentence get a graphic?

Go through the beat list from the cut transcript. For each sentence pick the first row that fits.

| The sentence | Picture | Layout |
| --- | --- | --- |
| names 2 or more parallel things | list: one item per word | beside speaker (2 to 4 short items) or full screen |
| describes steps, a system, cause and effect | flow diagram, built box by box | full screen |
| gives a number, price, date or growth | the number itself, large, or counting up | beside speaker, or full screen for the main figure |
| gives a count of things | exactly that many items | full screen |
| claims a result | real screenshot or clip, in a card | beside speaker or full screen |
| names a tool, product, person, company | logo tile, photo with name label | beside speaker or full screen |
| introduces a term | the term as large text | over or behind the speaker |
| is the key claim, maxim or question of a section | the sentence as text | cleared canvas, or speaker blurred and dimmed |
| starts a section | the section marker | full screen |
| talks about another video or post | that clip or post inside a card | full screen or corner card |
| uses a comparison ("you can't paint the Mona Lisa...") | one illustration of it | full screen |
| shows software | screen recording | card on a page, or full frame for tutorials |
| argues, explains why, tells a story about themselves, transitions | nothing | speaker |

How much of the runtime ends up as graphics is a style number, not a goal: 39 % (Kallaway), 62 % (Joseph), 72 % counting cards and screen demos (Ritesh). Check `picture_share_of_runtime` in the style and `graphics.density` in `brand.json`.

Longest stretch of plain speaker in the references: 17.6 s (Kallaway), about 18 s (Joseph). If a speaker stretch in your plan is longer and nothing in the table applies, use a camera move (`skills/camera.md`), not an invented graphic.

## 2. One system for the whole video

Fix these before designing anything, from `brand.json` (`brand.colors`, `brand.fonts`, `brand.graphics_mode`, `graphics.style`) and the style's look section:

| Part | Joseph | Kallaway | Ritesh | Nafay intro |
| --- | --- | --- | --- | --- |
| Canvas | off-white `#ebeae9`, faint grid, soft blue centre glow | near-black `#010101` to `#252227`, violet glow in the bottom corners | white `#ffffff` to grey `#bdbdbd` gradient, or white page with vignette | off-white `#f6f4f2`, one beige diagonal band |
| Accent | blue `#2151cd` | violet `#b577f3` (glow `#5d0bba`) | none; red only for "wrong" | blue `#4a96ee`; green yes, red no |
| Text | dark grey `#222`, light geometric sans | white and light grey sans | black, heavy italic for emphasis | bold serif titles |
| Cards | white, rounded, soft shadow | violet-to-dark gradient, thin light outline | white boxes, thin outline; dark cards for prices | white cards |
| Depth | flat 2D | flat 2D with glow | flat 2D | flat 2D |

All four are flat 2D. 3D appears only in the agency reels (`launch-video`: coins, a twisted cone, a flipping card). Use 3D only if `graphics.three_d` says so.

Other people's clips never go full frame: Joseph puts every example in a portrait phone card, Kallaway in a rounded card with a source label in its top-left corner.

## 3. Layouts

| Layout | When | Measured |
| --- | --- | --- |
| Full-screen graphic | diagrams, lists that need room, section markers, proof | Kallaway segments about 10 s median; Ritesh 6 to 31 s for multi-step diagrams |
| Text or icons beside the speaker | a term, two options, a small number, logos | zoom out first to make room (`skills/camera.md`); labels 3 to 7 % of frame height |
| Speaker as a card beside the graphic | the speaker should stay visible with a small graphic | Ritesh: 18 uses, about 6 s each |
| Panel slides over half the frame | a quick list of 3 or 4 | in 0.9 s, out 0.7 s |
| Graphic behind the speaker | a year, one big word | needs the speaker cut out from the background; only in `launch-video` and one Kallaway title |
| Speaker blurred and dimmed, text on top | the question or maxim | blur over 10 frames, hold 2.5 to 8 s |
| Corner speaker, clip centre, checklist | a worked example | Kallaway: 170 s in 6 stretches |

## 4. Pattern catalogue

Each pattern lists where to see it. `j` = joseph, `k` = kallaway, `r` = ritesh, `n` = nafay; numbers are seconds. Concept cards are named in full.

**Lists and structure**
- **Row per item**: rows or bullets, one per named word. r panel list; j clip plus bullet lines 82.9.
- **Numbered stops on a path**: overview first, then cut to each stop as it is discussed, back to the speaker for the explanation. k 774.8 to 820.5.
- **Staggered icon row**: icons pop from a dot with overshoot in about 4 frames, 8 frames apart, label 3 to 5 frames later, row re-centres. `clean-icons`.
- **Active-row list with a swapping picture**: the active item is highlighted and its image changes. `vaylens-explainer`.
- **Checklist that ticks**: boxes fill as each step is reached. k 1080 to 1225.
- **Section marker**: the same card every time. r "N/10" bar (build 1.9 s, hold 1.1 to 5.3 s); j two "Day N" circles joined by a labelled pill (hold 3 to 6 s); k ladder, camera climbs one rung in 1.4 s.

**Process and relationships**
- **Flow diagram**: card, dashed line, icon tile, arrow, result card, each on its phrase. Show all parts as faint ghost outlines at the cut, turn each dark on its noun, dim the finished ones to grey. r 138.9 to 160; j flow; k 310.6.
- **Camera follows the active box**: zoom about x1.15 and pan so it stays centred; zoom back out for the pay-off line. r; j pushes x1.6 in 0.9 s; k x1.65.
- **Card tree**: a top card, a curved line to each branch as it is named; return to the same graphic later with one more branch. k 639.1, 665.9.
- **Loop ring around the speaker**: dotted circle with labels appearing in spoken order. k 529.6.
- **One shape becomes the next thing**: a square turns into a dot, a bar chart, a window, the logo. `airbank-explainer`.
- **Scene inside the next scene**: cut in on a detail, pull back to show its container. `myna-ui`.

**Numbers**
- **Big number in the accent colour**, 11 to 19 % of frame height, small grey unit. j 57.0.
- **Count-up**: `$10` to `$2,000` in 1.7 s, fast then slowing. j 710.6. Small counters roll up in 8 to 10 frames and hold 0.5 s; for three figures alternate sides. `launch-video`.
- **Counter badges beside the head**, about 2 s. k 16.3.
- **Bar that fills and changes colour** green, yellow, red. n 4.6 to 5.9.
- **Price card**: old price, strike-through, new price 0.3 s after the word. j 836.8.
- **Table with a typing dotted leader**, one row per sentence. r.

**Proof and examples**
- **Screenshot card**, 2 to 5 s, a x1.08 to x1.12 push at the start and end. j, r (1.7 to 4.5 s each, blur cross-dissolve of 11 frames between two proofs).
- **Clip in a card with a source label**; questions typed over the dimmed clip. k 588.9.
- **Card row or grid**, one card per count, left to right. j 508.0.
- **Photo, source and line drawing**, a hand-drawn circle on each noun as it is said. k 67.2 to 79.2.

**Words as the graphic**
- **Sentence built word by word** on a cleared canvas, 6 to 9 % height, key words in bold accent, each word within 0.1 s of speech. j 23.8.
- **Term in heavy caps** behind or beside the head, 7.6 to 16 % height, in one frame within 0.2 s of the word; the second word on its own beat. k 62.7.
- **Two side labels**: left is the cause or first option, right the effect or second option. k 299.5.
- **Question on the blurred speaker**, typed in step with the voice. k 106.5.
- **Letters act the meaning**: "complicated" scatters then assembles. `vaylens-explainer`. Break the problem word and rebuild it as the product name. `airbank-explainer`.

**Openers and closers**
- **Hook**: first move inside 0.5 s. Speaker shrinks to a card with nodes around it (k 0.47); captions beside the face then a card shrink on "but" (r 4.3); two speaker layouts swapped five times in 22 s (n).
- **Call to action**: pill button with the words and a cursor (j 301.8); offer shown as a screen recording in a card with the URL in a pill (k 1321); subscribe lower third for the last 3 s (k 1341).

## 5. Timing

- **On the word.** Start each element so it is readable within 0.3 s of its word. Key words: 0 to 0.2 s after the spoken onset. Section names may lead by up to 2 s. Take word onsets from the re-transcribed rough cut.
- **Build time**: single element 0.1 to 0.5 s (cards fade in from blur with a small scale-up over 8 to 14 frames; words resolve from blur in 3 to 4 frames). A whole layout 0.3 to 1.2 s.
- **Stagger** repeated items by about 0.13 s (4 frames at 30 fps).
- **Hold** a finished layout at least 0.5 s; reels hold 0.5 to 1.9 s, explainers hold until the sentence ends.
- **Enter** at the first word of the sentence. **Leave** at the first word of the next sentence that does not need it.
- **Transitions**: hard cut to an empty canvas then build (Kallaway, Ritesh), or a soft white wipe from the bottom over 0.8 to 1.1 s in and a blur dip of about 10 frames out (Joseph). Pick one from the style.
- **Nothing sits dead still**: a finished graphic keeps a slow camera drift or one small moving part.

## 6. Building them

Graphics are web pages rendered frame by frame (`skills/plan.md`), so animated React components can be used as parts.

| Library | Licence | Find parts |
| --- | --- | --- |
| Magic UI (magicui.design) | MIT | registry `@magicui` |
| Componentry (componentry.dev) | open source; read the repo licence before shipping | registry `@componentry` |
| React Bits (reactbits.dev) | MIT plus Commons Clause: free to use in a video or product, the components themselves may not be resold or redistributed | copy from the site |

Search with the shoogle MCP (`search_registry_items`, query by what the part does: "number ticker", "typing", "marquee", "border beam", "text morph"). Results give the `npx shadcn@latest add @registry/name` argument. Useful starting points seen there: `@magicui/animated-gradient-text`, `@magicui/animated-shiny-text`, Componentry's Kinetic Text Reveal, Letter Cascade, Split Flap Display and Text Morph.

Rules for using them:
1. Free components only. Skip anything marked Pro or paid. Write each one into the credits file with its licence.
2. These components animate on the wall clock. A video render needs every frame to be a function of time, so drive them from the render clock (`skills/plan.md`), or use them for layout and style and write the motion yourself with the measured timings above.
3. Restyle to the brand system. A component's default colours and fonts never ship.
4. Never add a component because it looks good. It must be one of the patterns above doing a job from the table in section 1.

## 7. The plan the user approves

One row per graphic: time span, the spoken line, pattern, layout, what appears on which word, how it enters and leaves, why it is there. If "why" is empty, delete the row.
