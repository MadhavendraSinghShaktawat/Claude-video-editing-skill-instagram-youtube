# Style: joseph-clean-canvas

Dense light-canvas graphics, blur-and-scale camera, music and effects throughout (Joseph | Video Editing)

Learned 2026-11-15 from 1 video(s):
- How I’d Learn Video Editing in 2026 (Before AI Replaces You) (Joseph | Video Editing, 846 s) - `reference/analysis/joseph-learn-editing`

Numbers are medians across the videos; the values in brackets are each video, in the order above. Where the videos disagree, the bracket is the range to stay inside, and the look section below says which video to follow.

## Cut

| Measure | Median | Each video |
| --- | --- | --- |
| cuts_per_min | 20.9 | [20.9] |
| hard_per_min | 7.1 | [7.1] |
| jump_per_min | 3.1 | [3.1] |
| punch_per_min | 0.6 | [0.6] |
| pop_per_min | 5.0 | [5.0] |
| transition_per_min | 5.2 | [5.2] |
| shot_len_median_s | 2.18 | [2.18] |
| shot_len_p90_s | 5.93 | [5.93] |
| picture_change_every_median_s | 3.83 | [3.83] |
| picture_change_every_p90_s | 9.77 | [9.77] |
| longest_without_picture_change_s | 21.0 | [21.0] |
| transition_len_median_s | 0.73 | [0.73] |
| same_picture_cuts_inside_voice_pause | 0.08 | [0.08] |
| picture_changes_inside_voice_pause | 0.08 | [0.08] |
| chance_inside_voice_pause | 0.02 | [0.02] |
| picture_changes_after_sentence_end | 0.33 | [0.33] |

## Speech and pauses

| Measure | Median | Each video |
| --- | --- | --- |
| wpm | 264.3 | [264.3] |
| wpm_while_speaking | 278.0 | [278.0] |
| voice_active_share | 0.95 | [0.951] |
| pauses_per_min | 5.5 | [5.5] |
| pause_median_s | 0.14 | [0.14] |
| pause_p90_s | 0.19 | [0.19] |
| pause_max_s | 0.22 | [0.22] |
| speech_run_median_s | 1.12 | [1.12] |
| pauses_share_of_runtime | 0.01 | [0.014] |

## Camera on the speaker

| Measure | Median | Each video |
| --- | --- | --- |
| face_height_share_median | 0.37 | [0.372] |
| face_centre_x | 0.5 | [0.5] |
| face_centre_y | 0.38 | [0.38] |
| punch_in_scale | 1.18 | [1.181] |
| punch_out_scale | 0.87 | [0.869] |
| face_size_changes_between_shots_share | 0.66 | [0.66] |
| face_size_step_median | 1.13 | [1.134] |
| eased_zooms_per_min | 19.9 | [19.9] |
| eased_zoom_factor | 1.09 | [1.094] |
| eased_zoom_dur_s | 0.33 | [0.33] |
| slow_push_pct_per_s | 1.1 | [1.1] |

## On-screen text

| Measure | Median | Each video |
| --- | --- | --- |
| big_text_per_min | 30.6 | [30.6] |
| on_screen_s | 1.4 | [1.4] |
| words | 2.0 | [2.0] |
| words_p90 | 7.0 | [7.0] |
| height_share | 0.05 | [0.049] |
| repeats_spoken_words_share | 0.35 | [0.35] |
| appears_vs_word_s | 0.35 | [0.35] |
| built_on_share | 0.2 | [0.2] |

## Sound

| Measure | Median | Each video |
| --- | --- | --- |
| integrated_LUFS | -18.0 | [-18.0] |
| true_peak_dBTP | -1.4 | [-1.4] |
| LRA_LU | 4.3 | [4.3] |
| bed_rel_voice_dB | -24.7 | [-24.7] |
| bed_audible_share | 0.98 | [0.98] |
| bed_duck_dB | 5.3 | [5.3] |
| strong_sfx_per_min | 26.1 | [26.1] |
| strong_sfx_on_picture_event_share | 0.37 | [0.37] |
| strong_sfx_chance_share | 0.18 | [0.18] |
| strong_sfx_rel_voice_dB | -7.8 | [-7.8] |
| hard_cuts_with_sfx | 0.44 | [0.44] |
| transitions_with_sfx | 0.22 | [0.22] |
| pops_with_sfx | 0.21 | [0.21] |
| any_moment_with_sfx_chance | 0.1 | [0.1] |

## Share of runtime by picture type

| Picture | Median | Each video |
| --- | --- | --- |
| flat graphic | 0.273 | [0.273] |
| no face (b-roll / screen / graphic) | 0.003 | [0.003] |
| page with a face on it | 0.288 | [0.288] |
| small face (inset / wide shot) | 0.03 | [0.03] |
| speaker | 0.407 | [0.407] |

## Share of speaker time by camera move

| Move | Median | Each video |
| --- | --- | --- |
| eased zoom in | 0.68 | [0.68] |
| eased zoom out | 0.12 | [0.12] |
| pan/slide | 0.04 | [0.04] |
| slow pull out | 0.0 | [0.0] |
| slow push in | 0.09 | [0.09] |
| static | 0.06 | [0.06] |

## Look and use of graphics

Written from `reference/analysis/joseph-learn-editing/analysis.md` (every shot sheet read). Speaker time by eye is 37.5 %; the tables above count faces on cards too.

- **Graphic system**: off-white canvas `#ebeae9` with a faint grid and a soft blue centre glow; one accent blue `#2151cd`; body text dark grey `#222` in a light geometric sans; white rounded cards with soft shadows; flat 2D. Example clips always sit in a portrait phone card.
- **Camera**: system B in `skills/camera.md`. Speaker shots start blurred at about 92 % and scale x1.086 in 0.33 s; shots that lead into a graphic end with a x1.107 push over 0.33 s. Still in between. Instant punch-in x1.11 to x1.20 only for the stakes or promise line; punch-out x0.81 to x0.87 through a blur dip on pivot sentences.
- **Into a graphic**: soft white wipe rising from the bottom, 24 to 33 frames. **Back to the speaker**: blur dip, 2 to 4 frames out, cut, 5 to 6 frames in. White bloom flash only for the opening and the offer blocks.
- **What gets a graphic**: lists (one item per word), processes (card, dashed line, icon tile, result card, then a x1.6 push into the named part), numbers (11 to 19 % of frame height in blue, or a count-up over 1.7 s), counts (exactly that many items), proof (screenshot in a rounded window, 2 to 5 s). 30 graphic types are catalogued.
- **Text**: no running captions. About 25 chosen sentences get a white word-by-word caption (4.8 % line height, y 0.87, 7 words, 2.0 s, key words light blue). The biggest claim of a section is built word by word on a cleared canvas at 6 to 9 %.
- **Sections**: one "Day N" card (two circles joined by a labelled pill), held 3 to 6 s, for each stage of the plan.
- **Sound**: the "full" setting in `skills/sound.md`. Music under 98 % of the video about 25 dB below the voice; about 26 strong sound events a minute, on moves inside graphics and on scene changes.
