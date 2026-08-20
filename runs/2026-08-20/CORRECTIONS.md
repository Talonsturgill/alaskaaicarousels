# Corrections found AFTER No.38 shipped

The deck merged to `main` at 8.39 with every gate green. Phase 12 then built two
new gates, and both immediately found real defects in the deck that had just
shipped. Nothing here changes a pixel, a claim, a caption or the score. It is
recorded rather than quietly patched, and the original shipped artifacts are
left exactly as they were.

## 1. Three library options that were never applied

`AK.reliefShade` refuses unknown options as of this run's Phase 12 upgrade.
Re-run against the shipped slides it fails two of them:

- slide 05 passed `light: [-0.55, -0.68, 0.48]`
- slide 07 passed `light: [-0.6, -0.66, 0.45]` and `mix: 0.20`

The option is `lights`, an array of compass `{az, el, w}`, not a direction
vector; and `reliefShade` writes ImageData and has no blend of any kind, so
`mix` never existed. All three were silently ignored, which means the shading
on those two slides used the library's DEFAULT light and always had. The
pixels that were reviewed, scored and shipped are the pixels the defaults
produced.

They have been REMOVED from the source rather than corrected. Correcting
`light` to `lights` would relight two slides that have already been scored on
these pixels, and a re-light is a change that has to earn its own review.
Removing an option that was never read cannot change a pixel.

This is also, uncomfortably, the exact defect this run wrote a field note
about. The note said "never pass `mix`", and one `mix` survived on slide 07
through nine pixel critics, four revision rounds, every gate and the merge.
That is why the gate now refuses rather than warns.

## 2. An encoding declaration that stopped holding

Slide 05 declares `data-encodes` "the two documents are marked in different
colours because the voices differ". When the gold marker was realigned onto a
printed line in round 2, its declared rect was left behind, so the probe was
measuring two samples of the same paper: dE 1.9 against a 4.0 floor. Both
rects have been re-measured off the rendered PNG. Metadata only, no pixel
change.

## 3. Seven plan-versus-build drifts in the storyboard

`scripts/plan_drift_check.py` (new this run) found the shipped storyboard
assigning claim ids to slides that never printed them, and two dossier counts
that disagreed with the build:

| drift | shipped | truth |
| --- | --- | --- |
| C03 | slides 05, 08 | slide 05 |
| C07 | slides 03, 07 | slide 03 |
| C10 | slides 02, 06, 08 | slide 02 |
| C24 | slides 01, 06 | slide 01 |
| slide 08 measured axes | TWO | ONE |
| slide 08 declared marks | FIVE | THREE |
| slide 08 marks in band | five, band y 672-696 | three, band y 696-748 |

`storyboard.md` in this directory is the artifact as it shipped and has NOT
been edited. `storyboard.corrected.md` beside it is the reconciled copy, and
it is the one to read. Overwriting a shipped run artifact is one of the three
things this project stops and asks about, so the correction is added rather
than substituted.

After reconciliation `plan_drift_check` passes at 0 drifts and the full gate
block is 16 rows green.
