# Context: what the references do

Four explainer videos were measured frame by frame and then looked at shot by shot. Full write-ups are in `reference/analysis/<slug>/analysis.md`; the numbers are in `summary.json` beside them.

| Slug | Video | Kind | Length |
| --- | --- | --- | --- |
| `joseph-learn-editing` | Joseph, "How I'd Learn Video Editing in 2026" | talking head, graphics-heavy, light canvas | 14:07 |
| `kallaway-dopamine-ladders` | Kallaway, "How to Become a Storytelling Genius" | talking head, dark studio, one signature diagram | 22:26 |
| `ritesh-ai-agency` | Ritesh Verma, "How To Start an AI Marketing Agency" | talking head, white diagrams, b-roll, screen demo | 16:12 |
| `nafay-faceless-shorts` | Nafay 3D, "Faceless YouTube Shorts for free" | designed 22 s intro, then raw screen recording | 11:13 |

## What all of them do

| Fact | Joseph | Kallaway | Ritesh | Nafay |
| --- | --- | --- | --- | --- |
| Words per minute | 264 | 225 | 234 | 226 (dub count) |
| Median pause in speech | 0.14 s | 0.23 s | 0.20 s | 0.33 s |
| 90 % of pauses shorter than | 0.19 s | 0.33 s | 0.36 s | 0.43 s |
| Running word-by-word captions | none | none | none | none |
| Speaker alone on screen (by eye) | 37.5 % | 61 % | 28 % (+12 % as a card) | 3.3 % |
| Median time between picture changes | 3.8 s | 8.0 s | 5.2 s | 53 s after the intro |
| Canvas and accent | off-white `#ebeae9`, blue `#2151cd` | near-black, violet `#b577f3` | white to grey, black, red for "wrong" | off-white `#f6f4f2`, blue `#4a96ee` |

1. **Speech is cut very tight.** No pause over about 0.35 s survives in the talking heads, except where the speaker stops on purpose to let a clip play. Details: `skills/rough-cut.md`.
2. **Nobody runs captions.** Text appears for chosen phrases only: 10 to 31 text items a minute, 2 words on median, about 5 % of frame height. Details: `skills/text.md`.
3. **One graphic system per video.** One canvas, one accent colour, one type family, the same cards and corner radius from the first frame to the last.
4. **Graphics build with the voice.** One element per spoken noun, landing within about 0.3 s of the word. Lists never appear whole.
5. **Sections are marked the same way every time.** Kallaway returns to one ladder diagram 12 times. Ritesh opens each of 10 sections with the same "N/10" title card. Joseph uses one "Day N" card for each stage of his plan.
6. **Cuts follow the script.** Picture changes start a sentence, a list item, an example or a section. None of the sampled cuts was there only to break a pattern.
7. **Sound follows movement.** Where effects exist they sit on camera moves and on moves inside graphics, not on plain cuts or text. Details: `skills/sound.md`.
8. **The first seconds are the most edited.** Kallaway shows his first graphic at 0.47 s; Nafay's first layout move starts at 0.27 s; Ritesh puts captions, a punch, a card shrink and all his music and effects into the first 36 s.

## Where they disagree (the style memory decides)

| Choice | Joseph | Kallaway | Ritesh |
| --- | --- | --- | --- |
| Camera on the speaker | blur-and-scale entry and exit on most shots | locked, four fixed size levels | visible jump cuts, slow drift |
| Into a graphic | soft white wipe, 0.8 to 1.1 s | hard cut to an empty canvas | hard cut, or the speaker shrinks into a card |
| Back to the speaker | blur dip, about 10 frames | hard cut | hard cut |
| Music | under 98 % of the video, 25 dB below the voice | none | first 36 s only |
| Sound effects | 26 a minute | about 3 a minute, on zooms | only in the hook |
| Loudness | -18.0 LUFS | -14.2 LUFS | -15.7 LUFS |

The user said the camera should never feel stale. Two of the three talking heads hold the speaker still for about half of the time, so that is a preference, not a rule of the genre: take it from `brand.json` (`camera.motion`).

## Script to picture: what each kind of sentence gets

Use this when planning graphics. Each row is something at least two references do; the times are examples to look up in the shot sheets.

| The sentence... | The picture | Seen at |
| --- | --- | --- |
| opens the video | speaker full frame, first words as large text beside or under the face, a move inside the first half second | ritesh 0.1 to 4.3, kallaway 0.47, nafay 0.27 |
| states the promise or the stakes | instant punch-in, or large title over the speaker | joseph 1.77 and 34.10, nafay 7.2 |
| names a new term | the term in heavy caps beside or behind the speaker, on the word | kallaway 62.7 "PAVLOVIAN EFFECT" |
| lists things | one item per named word, each in its own row, card or box | joseph, kallaway 145.4 to 146.8, ritesh panel list |
| describes a process or system | flow diagram built box by box, camera follows the active box | ritesh 138.9 to 160, joseph flow |
| gives a number | the number large in the accent colour, or counting up | joseph 11 to 19 % height, launch-video counters |
| gives a count ("eight videos") | exactly that many items | joseph |
| claims a result | a real screenshot or clip in a rounded card, 2 to 5 s | joseph, ritesh 1.7 to 4.5 s per proof |
| cites a person, study or story | photo, source screenshot, simple drawing; mark each noun as said | kallaway 67.2 to 79.2 |
| shows someone else's video | the clip inside a card, never full frame | joseph phone card, kallaway rounded card |
| asks the question the video will answer | speaker blurred and dimmed, the question typed in the centre | kallaway 106.7, joseph maxim card |
| makes the biggest claim of a section | screen cleared, the sentence built word by word | joseph, ritesh text-only page |
| starts a new section | the same title card or diagram every time | all three |
| explains, argues, tells a personal aside | stay on the speaker | all three |
| walks through software | screen recording; cut the waiting, narrate the gap | ritesh 459 to 749, nafay |
| ends | proof clips, the offer in a card, speaker for the last lines | kallaway, ritesh |

## Why a cut is there

From the cut samples in the four analyses (section "Why each cut is there"):

- **Speaker to graphic, graphic to speaker**: at the first word of a sentence. Largest group in every video.
- **List item**: the item's row or box appears on its word.
- **Take join** (a pause, filler or retake was removed): left as a visible jump, or covered by a punch cut, or covered by cutting to a graphic.
- **Emphasis**: an instant punch-in on a marked line. Rare: 3 to 6 in a whole video for two of the references.
- **Section change**: the title card or diagram.
- **Not edits**: a window opening in a screen recording, a clip's own cuts, animation steps inside a graphic. The measuring tools count some of these as cuts; check by eye.

## What is not known

- Font names, exact easing curves, the software used.
- What any sound actually is. Sounds were measured (time, length, level, frequency band), never heard.
- How much raw footage was shot, how many takes are hidden under graphics, whether speech was sped up.
- Whether these choices caused the videos' performance. The only audience signal is Kallaway's most-replayed curve (peaks at a section title, at a flow diagram and at the start of the worked example).

## Limits of the measurements

Stated in full in `reference/README.md`. The ones that matter when reading numbers: a face detector cannot tell the speaker from a face in b-roll or on a card; cut kinds are algorithmic and over-count inside animated graphics and screen recordings; zoom numbers are reliable on speaker shots only; OCR misreads text while it animates; sound events in videos with music include musical hits.
