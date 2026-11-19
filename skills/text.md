# On-screen text

None of the four references runs word-by-word captions through the video. Text is placed for chosen phrases. What `brand.json` `captions.mode` says overrides this; if the user wants always-on captions, build them, and say that the references do not use them.

Measured on text at least 3.5 % of frame height that stayed half a second or more:

| | Joseph | Kallaway | Ritesh |
| --- | --- | --- | --- |
| Text items per minute | 30.6 | 11.9 | 9.5 |
| Words per item, median / 90th percentile | 2 / 7 | 2 / 7 | 2 / 6 |
| Line height, share of frame height | 4.9 % | 4.2 % | 4.8 % |
| Time on screen, median | 1.4 s | 3.0 s | 3.1 s |
| Items that repeat the spoken words | 35 % | 30 % | 44 % |

About two thirds of on-screen text is not a transcript of the voice: it is a label, a heading, a paraphrase or a number.

## Kinds of text

| Kind | Size (share of frame height) | Where | Words | How it arrives | Stays | Seen |
| --- | --- | --- | --- | --- | --- | --- |
| Hook caption | small line 4 to 5 %, heavy line 6 % | beside the face, two blocks | the first sentence | typed word by word, 0.10 to 0.13 s per word, starting 0.10 s after the first word | to the end of the sentence | ritesh 0.1 to 4.3 |
| Key-sentence caption | 4.8 % | centred, y 0.87, lower frame darkened | 7 median | word by word, each within 0.2 s of speech, 1 to 3 key words in the accent colour | 2.0 s | joseph, about 25 in 14 min |
| Lower-third takeaway | heading small, lines about 3 % | left edge x 0.10, y 0.77 to 0.88 | 1 to 2 lines that paraphrase the point, key phrase bold | types on in under 1 s | 8 s (5 to 13) | kallaway, about one per 90 s of speaker time |
| Term | 7.6 to 16 % | behind or beside the head | 1 to 2 | whole word in one frame, 0.05 to 0.2 s after the spoken onset | 2 to 7 s | kallaway 62.7 |
| Side labels | 3 to 7 % | mid-height, left and right of the head | 1 to 3 short lines each | left first | 2 to 17 s | kallaway 299.5, joseph 304.0 |
| Full-screen sentence | 6 to 9 % (Joseph), 5 to 12 % (Ritesh) | centred on the canvas | one sentence, two lines | word by word within 0.1 s of speech | to the end of the sentence, about 1.8 to 3.5 s | joseph 23.8, ritesh text page |
| Question or maxim | 3 to 7 % | centred on the blurred, dimmed picture | 1 to 3 lines | typed in step with the voice | 2.5 to 8 s | kallaway 106.5, joseph 108.5 |
| Big title over the speaker | cap height about 11 % | lower third, two lines | the promise | word by word, 0.07 to 0.13 s per word | 2.3 s | nafay 7.2 |
| Section title | number 10 %, name 6.5 to 8 % (Ritesh); 12.6 % with a 6.3 % subtitle (Joseph) | centred | 2 to 5 | builds in up to 1.9 s | 1.1 to 5.3 s | ritesh "N/10", joseph 59.6 |
| Labels inside graphics | 3 to 6 % | on the part they name | 1 to 3 | with the part | with the part | all |
| Number | 11 to 19 % | centre or beside the head | the figure and a small unit | counts up or appears on the word | 1 to 3 s | joseph 57.0 |
| Correction | box about 26 % of frame width | centre | the right word with an asterisk | hard on and off | 0.75 s | nafay 218.9 |

## Rules

1. **One emphasis device.** Key words take the accent colour (Joseph light blue, Kallaway violet), or a heavy italic (Ritesh). Never both, never underline plus colour plus size.
2. **Short.** Half of all text items are 2 words or fewer. Nine in ten are 7 or fewer. If it needs more, it is a caption for one sentence, not a paragraph.
3. **Timed to the voice.** A word that repeats the speech appears with it: measured medians are -0.02 to +0.35 s after the word. Text that leads the voice by more than about 0.5 s gets read before it is said and steals the line; only hook captions (0.5 to 0.9 s ahead) and section names (up to 2 s ahead) do this.
4. **Readable.** Nothing under 3 % of frame height (32 px at 1080p). Captions over footage get a darkened band or a dimmed, blurred picture behind them, not an outline.
5. **Clear of the face.** Measured positions sit below y 0.77, or beside the head at mid-height after a zoom-out, or on a canvas. Never across the eyes or mouth.
6. **Captions over footage belong to the hook and to chosen sentences.** After the hook Ritesh puts all text on pages and panels.
7. **Type**: one family from `brand.fonts`. Free fonts only (Google Fonts or the user's own files); list them in the credits.

## Checking

Run `tools/ocr.py` on the render. Every planned text should come back spelled correctly in `text.json`, at the planned size (`h`) and time; compare `appears_vs_word_s` in `summary.json` with the style.
