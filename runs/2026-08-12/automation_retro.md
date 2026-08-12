# AUTOMATION RETRO — 2026-08-12 — Carousel No. 31

## 0. The headline

`runs/2026-08-12/machine_qa.json` reads `PASS`, **0 fails, 0 warns, all nine
slides**. Two pixel-critic rounds and a flow critic returned `revise` on all
nine slides twice, scoring 2.5 to 6.5 and then 4.5 to 7.5, and the run cost
roughly three full fix passes over nine slides. Every objective gate in the
machine had nothing to say about the deck that needed the most repair in the
recorded window.

That is the deviation. The rest of this file is the evidence for where the
gate set is blind, phase by phase.

## 1. Deviations against prompts/routine_instructions.md

### D1. `AKPOST.grade` exposure authored as a multiplier — 9 of 9 slides, and it had already happened once

Evidence, round 1 of this run (`out/2026-08-12/plan.md`, "Round 1 review
findings" #1): all nine slides passed `exposure: 1.02` to `1.05` meaning "about
three percent". akpost.js reads STOPS, so `2^1.03` is 2.04x. The deck shipped a
full stop over; copper `#B8703C` bloomed until five independent critics could
not separate it from gold `#FFC72C` at 432 px, and each reported it as a
different fault on a different slide.

The part that makes it machinery rather than an anecdote: **it is not the first
time.** `runs/2026-08-08/slides/*.html` (No.30, the only other run with slides
committed) reads

    slide-01: AKPOST.grade(cx, {exposure:1.02, saturation:0.95, contrast:1.06});
    slide-05: AKPOST.grade(cx, {exposure:1.06, saturation:0.98, contrast:1.05});
    slide-09: AKPOST.grade(cx, {exposure:1.0,  saturation:0.92, contrast:1.05});

Eighteen consecutive slides across two runs, nine days apart, with a header
comment in akpost.js that says "stops" in the usage block. The root cause is
named in the run's own field note: `AKT.setup({exposure})` in akthree.js is a
MULTIPLIER on `three.js` `toneMappingExposure`, and slides 05 and 08 of this
deck call both libraries. One word, two meanings, side by side.

Gate that should have caught it: none exists. Nothing in the engine has ever
looked at a grade option's VALUE, only its SHAPE (the 2026-07-26 validator).

### D2. `AK.fitText` exceeded its declared `maxLines` in silence — 5 of 9 slides

Evidence (`plan.md` #2): slides 02, 03, 05, 06 and 08 set more lines than
declared, because `min` was authored higher than the box width could ever hold.
On slide 08 the three-line clamp swallowed **"It is for the grid."**, the
sentence carrying the deck's whole thesis, and the slide shipped arguing only
the negative half of its own argument. `qa.py` passed it.

The damning detail is in `assets/js/aktype.js` line 100: the helper has ALWAYS
set `data-fit-overflow="1"` on the element when it bottoms out, and

    grep -rn "fit-overflow" --include=*.py --include=*.js .

returns three hits, all three inside aktype.js itself. Nothing has ever read it.
An explicitly declared constraint has been failing in silence for the life of
the engine.

### D3. A metrically exact measurement over a scene that contradicted it

Evidence (`plan.md` #3): slide 05's 840 px dimension rule was exact to the
pixel; the two masses it named were 266 px apart. The deck's one load-bearing
measurement, twenty feet, was drawn as about six. Every gate passed. The repair
was structural — solve the 3D rig FROM the lock so one world unit is one foot
and the camera distance makes one foot 42 px — and slide 08 inherits the
corrected rig, which is what makes its substitution provable.

### D4. Printed constants disagreeing with the projection that drew the map

Evidence (`plan.md`, closing paragraph and the FIELD_NOTES entry committed at
9bc6990): two printed frame widths were typed constants, wrong by 7 and 25
percent against the projections that actually drew the maps. Now derived from
`proj.invert` at render time. Same defect class as D3: a number in type and the
geometry it names, computed independently.

### D5. A declared deck-wide continuity device drawn on zero slides

Continuity device A, the nine-rung ladder, was declared in the storyboard and
appeared on none of the nine slides until round 2. `dossier_check` passed 9/9.
Nothing compares a device the deck header DECLARES against artwork that
CONTAINS it.

### D6. The run record is incomplete

- `out/2026-08-12/run_state.json` at Phase 12 still reads `copy: in_progress`,
  `pixel_review: in_progress`, `flow_review: pending`, `scoring: pending`,
  `ship: pending` on a run that has shipped and merged (commit 2fcf71c).
- `runs/2026-08-12/` contains **no `run_state.json`**. `runs/2026-08-09/` ships
  one. (`score_report.json` was missing when this retro opened and landed with
  the ship commit 96b3b0a while Phase 12 was running; the state file did not.)
- `runs/2026-08-12/critique/` holds four round-1 pixel files covering slides
  01 through 08. There is **no critique record for slide 09**, no round-2 pixel
  record and no flow-critic record, although `plan.md` cites round-1 and round-2
  scores for all nine slides. The most expensive review in the series left the
  thinnest evidence.
- `ledger/upgrades.json` has **no `scan_log` entry for 2026-08-09**. That is the
  third silent lapse (after 2026-08-03 and 2026-08-04) of the rule the
  2026-07-31 entry exists to prevent.

### D7. Environment, retries, degradations

No environment breakage this run. No install failures, no fetch failures, no API
limits, no degraded fallbacks. The vector PDF path held (12.43 MB, 9 pages).
`site_signoff` PASS across 73 pages / 18 checks and the gas watch page check
PASS. The cost of this run was entirely craft rework, which is why every
candidate upgrade below is a gate and not a repair.

## 2. What was fixed, and what was deliberately not

D1, D2 and the general shape of D3/D4 are now machinery — see
`ledger/upgrades.json` for the three entries and their verification.

NOT taken, with reasons:

- **D5 (declared device absent).** A gate would have to read the storyboard's
  prose and decide whether artwork "contains a ladder". That is semantics, and
  the 2026-07-29 `encoding_reads()` calibration is the standing evidence that a
  colour statistic cannot answer a semantic question here. Recommended instead
  as a Phase 7 authoring rule: a deck-wide continuity device names, per slide,
  the element that carries it, in the dossier, so `dossier_check` can count
  nine declarations rather than judge nine pictures.
- **Loosening anything.** Nothing was loosened. All three changes add refusals.
- **The record gaps (D6).** Real, and worth the maintainer's attention, but the
  fix is a showrunner discipline (write `run_state.json` into `runs/`, keep every
  critique round) rather than an engine change, and inventing a ship-time gate
  for it inside a budget already spent on three craft defects would be the
  frontier-over-reactive mistake in reverse. Recommended in the email.

## 3. Frontier scan

Focus: **(g) accessibility and PDF/document-format changes** — the stalest
rotation slot (last scanned 2026-07-25, 18 days) and distinct from the last three
logged foci (2026-08-08 LinkedIn platform, 2026-08-07 typography, 2026-08-05
agent workflows). 6 searches, 3 fetches, 2 read. Nothing applied; two findings
parked to `knowledge/FIELD_NOTES.md`. See the `scan_log` entry for the detail.
