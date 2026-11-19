# Memory

What the skill remembers between videos. Three kinds, all plain files.

| File | What it holds | Who writes it |
| --- | --- | --- |
| `brand.json` | Your answers to the editor's intake questions: colours, fonts, format, cut pace, graphics taste, captions, sound, recurring pieces | `tools/memory.py set`, after the skill asks you |
| `styles/<name>/` | A style measured from videos: `style.json` (numbers), `style.md` (the brief the edit follows), `sources.json` | `tools/learn_style.py` |
| `notes.md` | Dated feedback: what you approved, what you rejected and why | `tools/memory.py note` after every review |

`intake.json` is the list of questions. It ships with the repo. Your answers do not: `brand.json`, `notes.md` and any style you add are git-ignored.

## Teach it your style

Give it reference videos you like, or your own old videos, and it measures them the same way the built-in references were measured:

```bash
python tools/analyze.py https://youtu.be/XXXX --slug ref-one          # or a local file
python tools/analyze.py ~/Videos/my-old-video.mp4 --slug mine-01
python tools/learn_style.py my-style reference/analysis/ref-one reference/analysis/mine-01 --desc "my channel look"
python tools/memory.py use my-style
```

Then the skill reads `timeline.md` beside the shot sheets for each video and fills in the "Look and use of graphics" section of `styles/my-style/style.md`, because numbers cannot say what a graphic was for.

For motion-graphics clips with no speaker (a reel, an agency showcase), ask for a concept card instead: `reference/motion-graphics/<slug>/concept.md`. See `skills/references.md`.

## What gets asked, and when

`python tools/memory.py questions` prints the intake questions that have no saved answer, plus the ones marked `per_video` (is this footage graded, what extra material is there). The skill asks only those. `python tools/memory.py status` shows everything saved.

To keep memory somewhere else (shared between machines, or outside the skill folder), set `EXPLAINER_EDITOR_HOME` to a folder.
