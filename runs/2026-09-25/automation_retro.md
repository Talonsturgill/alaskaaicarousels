# Automation retro, 2026-09-25 (No.68)

Phase 12, upgrade engineer. Inputs: run_state.json, WORKLOG.md, storyboard.md (BUILD
RECONCILIATION, rounds 1 to 3 and flow 1 to 2), score_report.json, the showrunner's ten incident
notes, gate_status block (0 FAIL rows, one WARN: gas_watch_live).

## 1. trend_check --window 10, and what this phase did with the top offender

```
weakest  8/10  mean 7.05  last 7.5  Artwork craft and genuine detail   worked 2026-09-14 (9 run(s) ago)  <-- STALE
weakest  1/10  mean 7.4   last 7.0  Deliverable completeness           worked never                      <-- STALE
weakest  1/10  mean 7.7   last 6.5  Variety vs ledger                  worked 2026-08-15                 <-- STALE
```

TOP OFFENDER: artwork craft. WORKED ON. The one upgrade this run is aimed at it: the scorer held
artwork at 7.5 partly because the scribed strokes "read as fur", and slide 04 lost three pixel
rounds to exactly that. See section 3.

The "worked 2026-09-14 (9 runs ago)" figure is WRONG, and measurably so. The 2026-09-23 (AKENGRAVE)
and 2026-09-24 (akv_probe) upgrades both name artwork craft in their triggers. Cause:
`trend_check.upgrade_touches()` runs each entry's whole change+trigger text through `canon()`,
which was written for criterion NAMES and cuts at the first "(" and the first ":". 160 of 183
ledger entries are cut to under half their length, so the matcher mostly reads the first clause of
`change` and almost never reads `trigger`. NOT FIXED, deliberately: the obvious repair (match the
whole text) swings the other way. Measured over the ledger, an any-word match credits artwork craft
with 38 entries (any mention of "craft" or "detail"), which would hide a real stale offender. That
is the dangerous direction for this instrument, and an all-words match finds only 4. The right fix
is structural, an optional `criterion` field on each upgrade entry that trend_check prefers over
text matching. That is a schema change, so it is a RECOMMENDATION for the maintainer, not code. The
flag is advisory (no gate calls `trend_check --require`), so leaving it costs no ship.

Variety vs ledger was this run's weakest (6.5; real DEM ground repeats No.67, the Polaris close
repeats No.64 and No.67, the data center lane's seventh deck in 30 days). That is an editorial
selection matter for Phase 14 and the directors room, not a machine defect. Deliverable
completeness has been weakest once in ten; deferred, nothing in this run pointed at a machine cause.

## 2. Deviations, phase by phase, with evidence

1. PIXEL REVIEW, slide 04: three critic rounds on scribed relief that read as fur (reconciliation,
   round 3: "s0 3, 9, 14, 22 and a long-stroke variant were all rendered and looked at"). No machine
   signal existed before a critic looked. The only fix was turning strokes off. Measured today:
   those variants claim a median 5 to 21 m of fall per stroke against 180 to 489 m on every shipped
   scribed frame. FIXED this phase (section 3).
2. GATE PASSED A DEFECT, pen contact rects (07, 09): `data-contacts` went stale twice when the pen
   moved; qa measured wherever the rects pointed and passed with a plausible dL. A pixel critic
   caught it. DEFERRED, and it is the strongest candidate for the next run's slot. The bounded
   build: AKPEN.render already returns `tip`, `tail` and `radius`; have it also return the shadow's
   screen footprint under the key light so the slide derives `data-contacts` from the object and
   never types them, then a qa cross-check that a declared shadow rect lies within N px of a
   non-transparent pixel of a declared object canvas. Deferred because today's budget went to the
   standing offender, and the reconstruction needs a stale-rect variant of 07 built carefully
   against qa's `_contact_aim` logic, which is more than one bounded change.
3. Dashed federal rings vanished under coasts, grid and the pen's cast on four frames (round 1).
   Fixed in-run with the AKS.ring coat-dark bed and draw-last order, and technique 97 already
   records it. No further machinery: a counted-mark visibility check would need a per-mark
   contrast probe, which is a redesign.
4. Locator windows typed in the plan were wrong on 09 by more than 2 degrees. Fixed in-run
   (`proj.invert` of the frame edges), and technique 97 already says "never typed numbers". The
   rail span still varied per frame until flow round 1 pinned it. No machinery added.
5. `render.py --only` takes slide NUMBERS; the first call with filenames errored. Cost one retry.
   The error was loud, not silent. Not worth a slot; a one-line argparse help change could accept
   both forms later.
6. qa caught a leftover discarded full-frame path on 07. A gate working as designed. No action.
7. Gas Watch: GitHub did not dispatch the 04:40 and 07:20 UTC schedules; workflow_dispatch from
   the session returns 403 on both REST and the connector. gaswatch_health WARN, incident written
   (out/2026-09-25/gaswatch_incident.json). Environment and GitHub service, out of scope for
   editorial upgrades by rule 19. No action here.
8. The scorer again found the rubric's weights sum to 1.10 (score_report: 8.69 as written, 7.90
   normalised). Already recorded as NOT DONE on purpose in FIELD_NOTES (the thresholds were
   calibrated against the literal sum). Unchanged: rescaling or renormalising moves every score
   against its threshold, which is the maintainer's call. RECOMMENDATION repeated for the email:
   write the convention into config/scoring_rubric.yaml, or renormalise the weights and the
   thresholds together.
9. Conflict-of-interest disclosure: the scorer's one-sentence fix (the studio runs on an Anthropic
   model; the deck quotes a candidate whom the Beacon reports received Anthropic employees'
   donations). House precedent existed (No.51) but nothing prompted it; applied in-run after
   scoring. DEFERRED as a candidate: a claims-level flag (`coi: anthropic`) set by the fact-checker
   when a claim names Anthropic or its people, and a caption_check rule that a deck carrying such a
   claim has the disclosure paragraph in its first comment. Deferred because it touches the
   fact-checker's schema, caption_check and the copy room at once, and today's slot went to the
   offender.
10. The flow critic caught a headline (07) repeating an earlier slide's sentence that four pixel
    rounds could not see, because pixel critics are per-slide by design. A cross-slide duplicate
    sentence check is objective and small (normalised sentence overlap across copy.json strings).
    DEFERRED, noted as a candidate; the flow room did its job.

Retries and environment: four pixel rounds, two flow rounds, one scoring pass plus the disclosure
fix. Gas Watch dispatch 403 as above. Three fetch summaries in today's scan needed a PDF read
through pypdf, and one fetch summary invented a claim its PDF does not contain (logged in
FIELD_NOTES).

## 3. Upgrades (1, a fix)

**AKSCRIBE fur warn** (`assets/js/akscribe.js`, `knowledge/TECHNIQUE_LIBRARY.md` #97,
`knowledge/FIELD_NOTES.md`). `AKS.scribeRelief` now measures the metres of fall each first-pass
stroke claims (slope in m/km x stroke length in px / pxPerKm), returns it as `drop` {strokes,
medianM, p90M}, and when the median is under 50 m across 300 or more strokes console.errors
`AKSCRIBE: ... will read as FUR`, a qa WARN on the FIRST render, naming why s0 can't fix it and
the two remedies that can. `lowReliefIntended: true` silences it.

Why this number: Imhof's rule 3 for large-scale hachures makes each stroke span one contour
interval, a constant DROP. akscribe's strokes are near-constant in pixels, so on a flat they claim
metres, inside the terrain tiles' own quantisation (Kennelly, https://mbmg.mtech.edu/pdf/gis_hachuretxt.pdf).

Calibration, through the real render path: shipped frames 01 488.6, 02 473.5, 03 438.1, 05 276.9,
06 278.7, 07 180.5, 08 455.3, 09 277.3 m. Rejected 04 variants: s0 3 5.1, s0 9 8.7, s0 14 at
lenScale 1.0 6.6, s0 22 12.9, s0 14 at lenScale 3.2 21.1 m. The 50 m line sits 2.4x over the worst
fur and 3.6x under the flattest shipped frame. Rejected as signals, with numbers: near-threshold
share (0.78 to 0.84 on fur, 0.75 on 03, which shipped as ridges) and neighbour direction coherence
(0.75 to 0.83 on fur, higher than every shipped frame's 0.13 to 0.46).

Verification:
- This run's nine slides, render.py + qa.py: 9/9 OK, qa PASS 0 fails 0 warns, all nine PNGs
  byte-identical by sha256 to out/2026-09-25/render (the measurement draws nothing and consumes no
  random draws).
- Defect reconstruction: the five rejected 04 variants each carry exactly one qa WARN,
  `console error: AKSCRIBE: scribeRelief region [0,0,1080,1350] will read as FUR: its median
  stroke claims 5.1 m of fall (p90 18.4 m, 12570 strokes) ...`. The s0 14 variant with
  `lowReliefIntended: true` is silent.
- examples/demo-deck, render.py + qa.py: 4/4 OK, 0 fails, 14 warns (3, 5, 5, 1), the known
  baseline; it does not load akscribe.
- WARN, not FAIL, on purpose: a deck may mean to draw micro-relief, and 2026-09-17 recorded what a
  hard fail built on a heuristic costs. No gate or threshold was loosened, and there are no new
  dependencies.

What it does NOT fix: the scorer's broader note that the scribed family is "one uniform texture"
on 01, 05, 06 and 09 even at 180 to 490 m. That frames' fall is real; the uniformity is placement
(one stroke per grid cell, Imhof rules 2 and 3 broken), which is the parked item below.

## 4. Frontier scan

Focus (c), procedural art portable to offline Canvas. Legal (last 2026-09-20; the last three were
f, b, g) and chosen over the stalest slot (d) on relevance to the offender and to the 2026-08-15
park's request for a readable streamline-placement implementation. 5 searches, 9 fetches.

- APPLIED as the principle behind the fix: Imhof's five hachure rules via Kennelly.
- PARKED (FIELD_NOTES, "Parked, 2026-09-25 frontier scan, focus (c)"): a contour-row hachure mode.
  It uses Huffman's QGIS seeding and trimming rules
  (https://somethingaboutmaps.wordpress.com/2024/07/07/automated-hachuring-in-qgis/) and ports
  gugray/adaptive-streamlines' two masks (MIT, 633 lines, no dependencies,
  https://github.com/gugray/adaptive-streamlines). Parked because it is a new placement algorithm
  that changes every future scribed frame and needs a deck that wants it.
- Nothing usable: erzberg (React + three.js, https://github.com/sorny/erzberg); Buchin et al.
  beyond the note that its fetch summary was wrong.

## 5. Files touched

- assets/js/akscribe.js
- knowledge/TECHNIQUE_LIBRARY.md
- knowledge/FIELD_NOTES.md
- ledger/upgrades.json (one entry, one scan_log entry)

Not committed by this phase: the showrunner commits these as `upgrade(2026-09-25):`, then records
the SHA in a follow-up commit.
