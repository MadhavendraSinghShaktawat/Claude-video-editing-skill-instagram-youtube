# Step 1: the rough cut

Cuts only. Remove dead space, filler words and retakes. No zooms, graphics or sound yet. The output is `work/<slug>/cut/rough.mp4` and everything later is timed against it.

## What the references measure

Voice pauses measured on a separated voice stem (a pause = 0.12 s or more with the voice 20 dB under its median):

| | Joseph | Kallaway | Ritesh | Nafay (screen tutorial) |
| --- | --- | --- | --- | --- |
| Median pause | 0.14 s | 0.23 s | 0.20 s | 0.33 s |
| 90th percentile | 0.19 s | 0.33 s | 0.36 s | 0.43 s |
| Longest | 0.22 s | 3.26 s | 1.60 s | 0.89 s |
| Pauses over 0.5 s | 0 | 8 | 5 | few |
| Pauses as share of runtime | 1.4 % | 9.2 % | 8.0 % | - |
| Words per minute | 264 | 225 | 234 | 226 |

- Every pause over 0.5 s in Kallaway sits where he stops to let an example clip play (1067 to 1166 s). Every one in Ritesh is inside a screen demo. They are kept on purpose.
- In the screen tutorial about half of the recorded time is removed: one minute on the on-screen clock lasts 18 to 49 s of video, at normal playback speed. Waiting is always cut, never sped up, and bridged in speech ("let's wait for it to finish" / "and just like that it's ready").

## Do it

```bash
python tools/transcribe.py raw.mp4 work/<slug> --verbatim     # keeps um, uh, false starts
python tools/audio.py raw.mp4 work/<slug>                     # voice pauses from the voice stem
python tools/rough_cut.py raw.mp4 work/<slug> --fillers sounds
```

`rough_cut.py` takes its targets from the default style: pauses longer than the style's 90th-percentile pause are cut down to the style's median pause. Override with `--max-pause` and `--keep-pause`. From `brand.json`:

| `cut.pace` | `--max-pause` | `--keep-pause` |
| --- | --- | --- |
| very tight | 0.20 | 0.14 |
| tight | 0.35 | 0.22 |
| natural | 0.60 | 0.35 |

### Several raw files with lines said many times, and a script

The usual case for a scripted video: the speaker says a line, stops, says it again, sometimes over ten camera files. Use `select_takes.py` instead of `rough_cut.py`:

```bash
for f in raw/*.MP4; do python tools/transcribe.py "$f" work/<slug>/$(basename "${f%.*}") --verbatim --lang en; done
python tools/select_takes.py work/<slug>/script.txt work/<slug> raw/*.MP4        # files in recording order
# read work/<slug>/cut/cutlist.md, fix with overrides.json, run again, then:
python tools/select_takes.py work/<slug>/script.txt work/<slug> raw/*.MP4 --render
```

`--render` does not stop at the render. It transcribes the render piece by piece, adds every repeat it finds to `overrides.json` as a drop, and renders again, up to three rounds. Then it prints what is left for you: `FIX BY HAND` (a repeat across two files) and `LOOK AT` (short pieces that do not follow the script). Never pass `--no-check` for a cut you deliver.

It aligns every script line against every word of every file and uses the last attempt that covers at least 85 % of the line. Inside that take it drops restarts ("you stitch the, you stitch the clips"), filler sounds and fragments made of script words. Off-script words of two or more content words inside a line are removed, and so is unscripted speech between lines; only what fills a `[PLACEHOLDER]` stays (set `"keep_unscripted": true` in overrides.json to keep ad-libs). Breaths (0.2 s or more with no pitch and a flat spectrum) count as silence, so they are trimmed before and after every take and inside pauses. Cut points are moved into measured silence. A stretch is split wherever two kept words are more than 0.8 s apart, because speech recognition skips mutters. The cut list shows every attempt of every line, the take used, lines flagged WEAK (under 85 % coverage), every restart removed and every ad-lib kept: read all of them. `--check` (on a fresh transcript of the render) writes `script_vs_edit.md`, a line-by-line comparison with the time of each line in the edit, and lists lines that are missing and word runs that are said twice.

Rendering keeps the source resolution and frame rate: each piece is cut frame-accurately, encoded once (HEVC 10-bit by default; `--codec prores` for a master to keep editing), joined without re-encoding, with 12 ms audio fades at every cut against clicks.

The render is checked piece by piece (automatically after `--render`; on its own with `--check-pieces --apply-check`), never only as one long transcript: speech recognition on a long file hears a phrase said twice in a row once ("rule number three. Really sur- rule number three really surprised me"). Piece by piece it cannot merge them. The check flags a piece, or run of pieces, whose words are said again at the start of what follows, and lists every short piece whose words do not follow the script ("look at"). A lone word heard in isolation is often misheard, so look at those against the audio before dropping them. When a sentence needs a hand edit, give its exact source spans in overrides.json: `"line_spans": {"82": [["C0712", 35.88, 39.5], ["C0712", 42.5, 45.1]]}`.

### Mistakes already made on real footage: never ship these again

Each of these reached a user in a delivered cut. The tool now handles them, but check for them every time:

| Mistake | Why it happened | What prevents it |
| --- | --- | --- |
| A phrase said twice in a row ("Rule number three. Really sur- Rule number three really surprised me", "And one went- And one went hunting") | Speech recognition on a long file, raw or rendered, hears the repeat once and returns one clean sentence | The automatic piece-by-piece check after `--render`. Never trust a whole-file transcript to prove there are no repeats |
| A loud breath of 0.3 to 0.6 s before a take | A breath is as loud as speech, so a loudness threshold keeps it | Breath detector (no pitch, flat spectrum, 0.2 s or more) counts breaths as silence. After rendering, no breath-like run over 0.26 s may remain |
| The first word of a line cut off ("I built this" heard as "I will list", "Remotion" heard as "The motion") | The misheard first word did not match the script, so the line started one word late | Line start and end are extended over misheard words that touch the line. Read the first words of every line in `script_vs_edit.md` |
| A fragment left at a cut ("un" from "under the") | A repeat was cut at the word's reported start, which can be 0.1 to 0.3 s off | Drops cut at the quietest 10 ms near the word, not at its reported time |
| A cut into the start of a word ("And" clipped) | The previous word's end time ran late, past the next word's onset | A clear onset after silence overrides the previous word's end time |
| A two-frame silent sliver between drops | Two drops left a tiny piece between them | Silent pieces under 0.2 s are removed |
| Ad-libs and retake chatter kept ("okay, again", half-lines) | Unscripted speech after a line was treated as a deliberate ad-lib | Unscripted speech is removed unless it fills a `[PLACEHOLDER]` in the script; fragments made of script words are retakes, not ad-libs |
| Pauses up to 0.64 s | A mouth click split one silence into two short ones | Clicks under 50 ms are ignored when measuring silence |

The rough cut is done only when:

1. The check prints no repeats, and every `FIX BY HAND` is fixed.
2. Every `LOOK AT` piece has been checked against the audio. A single word heard on its own is often misheard ("No" for "now"), so don't drop it on the transcript alone.
3. `script_vs_edit.md` has been read line by line. Every line under 75 % has a reason: a misheard name or number, or the speaker's own wording with no better take.
4. The longest pause is no longer than `--max-pause` plus a frame, and there is no breath over 0.26 s.
5. The user has been told what you could not fix and why, with a time in the edit for each.

### Reading the cut list

Then read `work/<slug>/cut/cutlist.md` against the transcript:

1. **Retakes.** The tool flags a phrase whose opening words are said again within the next three phrases and drops the earlier one. Confirm each: a repeated opening can be deliberate ("Not X. Not Y."). Keep the later take unless the earlier one is clearly complete and better.
2. **Fillers.** Sounds (um, uh, er) are removed. Words such as "like", "so", "right", "you know" are only proposed with `--fillers all`, marked "(check)", and only when set apart by a pause. Remove them one by one, not in bulk.
3. **Meaning.** Read the kept text straight through. If a removal breaks a sentence, restore it in `overrides.json`.
4. **Deliberate pauses.** Restore a pause where the speaker waits for something on screen, lands a joke, or asks a question.
5. **Never cut** what `brand.json` `cut.keep` lists.

Show the user: seconds removed by reason, the list of retakes, anything you restored. After approval run again with `--render`.

## Where the cut lands

- Cut in the pause, not in a word: the tool pads 0.06 s of air on each side of speech.
- Prefer sentence boundaries for take joins. About a third of picture changes in every reference fall right after a sentence ends.
- After rendering, transcribe `rough.mp4` again so every later step uses word times from the cut, not from the raw file. Use that transcript for timing only, never as proof that nothing is repeated (see above).

## What happens to the joins

A join between two takes of the same framing is a jump cut. The references treat it three ways; the style memory says which:

| Treatment | Who | Numbers |
| --- | --- | --- |
| Leave it visible, same framing | Ritesh (20 of them), Kallaway (about 13, some mid-sentence) | scale change under 1.5 % |
| Punch: change the speaker's size at the join | Kallaway (27 joins) | one step of x1.047 in or out |
| Cover it: go to a graphic at the join and come back later | Kallaway (39), Joseph (most) | the graphic starts on the sentence |

Mark each join in `edit.json` with the treatment; the camera step (`skills/camera.md`) fills in the scale.

## Screen recordings

- Cut silence while the screen is static, so the cut cannot be seen.
- Remove each wait with one hard cut. Keep the speaker's line before it and after it.
- Keep playback at 1.0x unless the user asks otherwise.
- Skip sign-in and account screens by cutting and saying so, not by blurring.
