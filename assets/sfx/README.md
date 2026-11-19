# Free sound effects

Everything in this folder may be used in monetised videos **and redistributed**, so it ships with the repo.

| Folder | Files | What | Licence |
| --- | --- | --- | --- |
| `kenney-interface-sounds` | 98 | clicks, toggles, confirmations, errors, scrolls | CC0 1.0, by Kenney (kenney.nl) |
| `kenney-ui-audio` | 51 | clicks, switches, rollovers | CC0 1.0, by Kenney |
| `kenney-digital-audio` | 62 | lasers, phasers, power-ups, tones | CC0 1.0, by Kenney |
| `kenney-impact-sounds` | 130 | footsteps, knocks, metal, wood, glass and plate impacts | CC0 1.0, by Kenney |
| `earshot-bank` | 252 | cut hits, sub drops, whooshes, risers, reverse swells, dings, pops, clicks, taps, typing, shutters, glitches | MIT (earshot, `LICENSE-earshot-MIT.txt`); made in code, the `fit__*` sounds are fitted from CC0 recordings (`vendor/earshot/docs/CREDITS_FIT.md`) |

`catalogue.json` measures every file (`tools/director/sfx_library.py`): length, peak time, attack, tail, rise,
centroid, low-end share, stereo width, tonality, loudness. Pick by those numbers, then check with earshot
(`skills/sound.md`).

The earshot bank was rendered with seed 1 at default length (`api.sfx_render(name, out, seed=1)`); render other
lengths, pitches or seeds yourself from `vendor/earshot`. Crediting Kenney is optional and appreciated.
