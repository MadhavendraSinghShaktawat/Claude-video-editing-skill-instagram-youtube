# launch-video: talking head goes in and out of cards

- Source: `reference/source/mg/launch-video.mp4`. 720x1280 vertical, 30 fps, 1046 frames, 34.87 s of video (container 35.06 s). Values from `shots.json` and `sheets/sheet_index.json`.
- Sheets read: `sheets/sheet_001`-`006` (5 fps, all of them) and 30 fps crops of the middle panel `sheets30/mid_f0000`, `f0060`, `f0102`, `f0150`, `f0186`, `f0240`, `f0285`, `f0318`, `f0378`, `f0420`, `f0450`, `f0546`, `f0585`, `f0636`, `f0700`, `f0735`, `f0768`, `f0810`, `f0852`, `f0890`, `f0930` (40 consecutive frames each, starting at the frame in the name; rows 406-818 of the frame, made with OpenCV because `make_sheets.py` cannot crop). `mid_f0970` and `mid_f1000` exist but were not read; 32.3-34.9 s is described from the 5 fps sheet only.
- **Layout of the file itself**: the frame is three stacked 16:9 panels (seen in every tile). Top = the raw talking-head footage. Middle (rows about 406-818, y 0.32-0.64) = the finished edit. Bottom = a screen recording of a layer timeline with a badge "Video Created by Bijoy Chandra". Everything below describes the middle panel. Frame numbers are source frames (f); time = f / 30.

## Concept in one paragraph
A before/after breakdown of an edited talking-head video. One speaker, one camera angle. The single idea: the footage is treated as a movable object. It plays full-frame with graphics behind and in front of the speaker, then shrinks into a rounded card on a cream-and-lime page, then is replaced by full-screen type, then comes back through a shaped wipe. One lime accent colour and one dark olive carry every graphic, so the piece holds together while the layout changes about every 1-2.5 s.

## Look
- Palette: page background cream `#f4fed2` / `#f8fcea` (shots.json, sampled `#f6ffe0` at f100) with soft, slowly moving lime blobs (0.6 s); accent lime `#cafd4c` (shots.json shot 10; sampled `#caff45` at f700); text dark olive `#29360d` (sampled f725); white `#fdfdfd` for inverted type (f735). The dark greys `#141516` / `#262b2d` in shots.json belong to the timeline panel, not the edit.
- Typography: a sans family, medium to bold, Sentence case. Sizes from text.json are shares of the full 1280 px frame; multiply by about 3.1 for share of the edit panel. Statement line "Why that is happening" 0.034 (about 11% of panel); lower-third lines 0.019-0.023 (6-7%); "Breakthrough" 0.083 (26%); "2026" 0.16-0.18 (about half the panel); "Most people" / "One thing" 0.079-0.111 (25-34%); "Focus" 0.145 (45%); pill labels 0.016-0.027 (5-8%). Centred, except callout pills that attach to a card edge.
- Shapes: rounded-rectangle video cards (radius about 6-8% of card width, 0.8 s and 29.3 s); pills with a small icon; a thick lime ribbon stroke with round ends (18.3 s, 25.9 s); concentric translucent rings behind the head (12.8 s); a four-point sparkle (9.5 s).
- 3D elements: lime coins with a black "$" that spin (5.2-6.0 s); a lime-and-dark twisted cone (8.4-9.7 s); paper bills as confetti (13.4 s); the portrait card flips about its vertical axis (30.0 s). The rest is 2D.
- Depth: graphics go behind the speaker (coins 5.3 s, "2026" 7.0 s, rings 12.8 s), so the speaker is cut out from his background. The ribbon passes both behind and in front of him (19.2 s). Flying tags are blurred when far from the focal plane (27.6-28.3 s). Lower thirds sit on a dark-green-to-lime glow rising from the bottom edge (4.2 s). Motion blur on fast moves (f557, f786).

## Scene list
| Time | On screen | How it enters | How it leaves | What it explains |
|---|---|---|---|---|
| 0.0-2.2 | Speaker full-frame, then as a card on cream; pills "This Video", "Exactly" | Play icon pops f4-f7; footage shrinks f8-f18 | Card blurs out f66-f68 | "In this video..." |
| 2.2-3.4 | "Why that is happening", last word on a lime highlight | Word by word f68-f88 | Hard cut f104 | Promise 1 |
| 3.5-8.1 | Full-frame speaker; lower third "Importantly / How you can actually get rich with an AI agency"; 2 spinning coins (5.1-6.1); big "2026" behind head (6.1-8.1) | Pill + line f104-f109, glow and text f110-f130; coins pop f154-f159; digits roll f183-f209 | Peel wipe f243-f252 | Promise 2, the year |
| 8.4-9.7 | Twisted cone rotating with sparkle on cream | Revealed by the peel | 1-frame lime flash f291 | Beat before a key word |
| 9.7-10.5 | "Breakthrough" | Letters fly in scattered f292-f305 | Star-shaped opening f316-f330 | Key word |
| 11.0-12.5 | Plain speaker | - | - | Rest |
| 12.6-16.2 | Rings behind head; counters "$10,000", "$50,000", "$100,000 per month" at right, left, upper right, with coins and bills | Rings grow f378-f400; each counter rolls up (below) | Each fades in 3-4 frames | Three income levels |
| 16.0-18.4 | Lower third "others / Can't even get their first client?" | Same build as first lower third (f478-f490) | Fades f546-f550 | The contrast |
| 18.2-21.5 | Ribbon loops around the speaker, footage shrinks to a card; small text rides the ribbon | Ribbon draws f546-f553; shrink f554-f563 | Ribbon retracts f637-f645; card gone at f646 | "The answer is simple" |
| 21.5-23.5 | Lime band with scrolling words "It's not about the opportunity anymore" | Band wipes from left f647-f651 | "anymore" box lifts f704 | Negation |
| 23.5-25.1 | Three rows of huge scrolling type, "Focus" in the middle; colours invert f729-f740 | Blur-in f705-f716 | Hard cut f753 | The answer |
| 25.1-26.2 | Plain speaker, ribbon starts crossing at f770 | - | Smear f785-f787 | Rest |
| 26.3-28.4 | "Most people", then "One thing" with pill tags flying past (Crypto, Amazon FBA, NFT Flipping, Shopify Store, Etsy Shop...) | Word by word | Hard cut f854 | Listing distractions |
| 28.5-29.0 | Plain speaker | - | Shrink f870-f876 | Rest |
| 29.2-34.9 | Small portrait card: speaker, then three b-roll faces after flips at f900, f946, f1002; callouts "Talent", "Hard work", "Consistency" | Flip, then pills extend | Clip ends | Three qualities, last one is the point |

## Motion vocabulary
- **Footage to card**: lime inset border appears f8-f11, then the footage scales from full panel to about 46% of panel width f12-f18, settling by f24 (about 12 frames, 0.4 s, decelerating, OBSERVED). Second time f554-f563 (9 frames) with blur at f557-f558. Third time to a portrait card about 22% of panel width, f870-f876 (6-7 frames), settle to f884.
- **Pill grows from icon**: square icon pops (f4-f7), later widens into a labelled pill f17-f24 (7 frames). Same for the card callouts: dot/badge f906-f913, text types on f918-f929.
- **Word-by-word blur-in + highlight**: "Why" f68-f73, "that" f71-f77, "is" f78-f81, "happening" f83-f88, each 5-6 frames, starts about 5 frames apart; lime box behind the last word is solid by f88. Hold f90-f103.
- **Lower third build**: white chip f104 -> lime pill f106; thin rule extends both ways f106-f109; glow rises and two lines fade in word by word f110-f130 (20 frames).
- **Coin pop and spin**: two coins scale up from behind the shoulders f154-f159 (5 frames), turn edge-on at f177-f179, exit by f186. Speaker stays in front.
- **Slot-machine number**: "2026" digits roll vertically with motion blur f183-f209 (26 frames, 0.87 s); "20" settles about f200, "26" at f208-f209. Hold f209-f243.
- **Counting-up counter**: "$8,2.." f404 -> "$10,000" f412 (8-9 frames); "$49,9.." f437 -> "$50,000" f441; "$59,9" f461 -> "$100,000" f470 (10 frames). Each arrives with a bill burst and a coin, holds 0.5-0.6 s (f412-f430, f441-f449, f470-f485), fades in 3-4 frames. Positions alternate right / left / upper right.
- **Peel wipe**: a cream wedge grows from bottom centre and the footage folds away to both sides, f243-f252 (9 frames).
- **Flash + scattered letters**: full lime frame at f291 (1 frame); letters enter large, rotated, blurred and settle into the word f292-f305 (13 frames); sparkle drops onto the word f309-f315.
- **Shape iris back to footage**: a star-shaped hole with a lime rim opens from the word's centre f316-f330 (14 frames).
- **Ribbon**: stroke draws along a curve f546-f553, keeps travelling into a loop around the head f563-f575, with small text on it from f575. Used again f770-f800 as a wave behind big type.
- **Marquee band**: band wipes in f647-f651; words enter at the right and slide left: "It's" f651, "not" f654, "about" f656, "the" f660, "opportunity" f662, "anymore" f675 (3-13 frames apart). Ends as one word in a small box, the only near-still moment (f697-f700).
- **Type wall + invert**: three rows slide in with heavy blur f705-f716, sharp by f720; f729-f740 (12 frames) background goes solid lime and "Focus" turns white; f741 back.
- **Depth-of-field tags**: pills cross from upper right to lower left, a new one every 4-6 frames (f824-f853), near ones sharp, far ones blurred.
- **Card flip**: f895-f905 (10 frames, 0.33 s), edge-on at f900; again f943-f950 (edge-on f946-f947) and around f1002. Callouts retract 3-4 frames before each flip.
- Easing notes are OBSERVED from tile spacing, not measured.

## Pacing
- shots.json: 19 cuts in 34.87 s (33 per minute). Counting what the middle panel shows, there are about 15 layout changes (4 hard cuts at f104, f753, f854 and the 1-frame flash f291; the rest are morphs, wipes and flips), about 26 per minute.
- Shortest: lime flash 1 frame; colour inversion 12 frames (0.4 s). Longest unchanged composition: ribbon card f578-f636 (1.9 s); plain speaker f330-f376 (1.5 s).
- A finished graphic is held 0.45-1.9 s before the next change (statement line 0.45 s, counters 0.5-0.6 s, "2026" 1.1 s, each flip card about 1.5 s).
- Never fully still except f697-f700 (0.13 s, my frame-difference measure on the middle panel); the speaker and the background blobs are always moving.

## Sound
An AAC audio stream exists (ffprobe). Audio was not analysed.

## Patterns to reuse in a talking-head explainer
- **Shrink the speaker to a card, annotate it** -> "in this video", "here's the thing", any aside. Scale footage to about 45% width in 10-12 frames on a flat page, attach 1-2 pills that grow from an icon in 7 frames; hold 1.5-2 s; return by cut.
- **Statement line with one highlighted word** -> a short claim or question. Full-screen page, words blur in 5-6 frames each, 5 frames apart, highlight box lands with the last word; hold about 0.5 s; hard cut back.
- **Number behind the head / counting counter** -> naming a year, price or growth ("showing a number growing"). Big rolling digits behind the cut-out speaker settling in about 26 frames, or a small counter beside him rolling up in 8-10 frames, held 0.5 s; for three figures alternate sides.
- **Lower third on a rising glow** -> a key takeaway while the speaker stays full-frame. Pill label, thin rule, then 1-2 lines over a dark-to-accent gradient from the bottom; build in about 25 frames.
- **Flip card with callouts** -> listing 3 qualities or options with b-roll. Small portrait card, flip in 10 frames to each new image, two pills extend with the label, about 1.5 s per item.
- **Marquee then type wall** -> "it's not about X, it's about Y". X scrolls small on an accent band; Y fills the frame as three scrolling rows with a 12-frame colour inversion as the hit.

## Not determinable
- What the speaker says, and so whether graphics land on spoken words; music and sound effects.
- Font names; exact easing; the editing software (its name is not readable in the bottom panel).
- Full text on the ribbon (only "...actually really simple" is readable at 19.3 s); some tag labels are blurred.
- Whether the cone, coins and bills are 3D renders or stock elements; how the speaker cut-out was made.
- Whether the source edit is 16:9 at higher resolution (the panel is only 720x412 here).
- Measurement caveats: shots.json and text.json analysed the whole 3-panel frame. Palettes, flat_share, face_share and motion boxes mix raw footage, edit and timeline; "pan/slide" and "slow push in" camera labels are not camera moves in the edit. The "jump" cuts at 16.23, 18.57/18.63, 21.23, 30.1, 31.5/31.63 s are graphic events (lower third, card shrink, ribbon exit, card flips); the hard cuts at 24.3 and 24.7 s are the colour inversion. The third flip (33.4 s) is not listed. The two permanent text tracks are the creator badge in the bottom panel. OCR misreads: "009others", "Wiark Mode", "Most pcople".
