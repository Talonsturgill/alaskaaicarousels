# AUTOMATION RETRO, 2026-09-12, run No.57 (Phase 12)

Walked `out/2026-09-12/run_state.json` and the run's artifacts phase by phase
against `prompts/routine_instructions.md`, with the showrunner's
`out/2026-09-12/incidents.md`, the FIELD_NOTES entry for today, the last two
instincts and the storyboard's ROUND 2 section.

Three upgrades made, all reactive, all verified against real renders or real
shipped decks. One frontier scan run and parked. Three candidates refused with
reasons.

## 1. DEVIATIONS, WITH EVIDENCE

**D1. A slide whose render threw produced a qa.py PASS.** Incident 5.
`.claude/skills/carousel-engine/qa.py`'s missing-PNG branch appended its FAIL and
then `continue`d past the rollup at the foot of the loop, so `machine_qa.json`
read `{"fails": 0, "warns": 0, "verdict": "PASS"}` and the process exited 0.
Reconstructed on disk: render.py hard failed a broken slide-01, qa.py printed
`FAIL: png missing` and, two lines later, `verdict: PASS`. Nothing downstream
reads the terminal. FIXED, upgrade 1.

**D2. The deck broke its own colour law in three places and every gate passed
it.** `AKICE.rays` defaulted to `[255,199,44]`; the provenance mark was set in
the undetermined ink on all nine frames; slide 03's eight gold ticks rendered as
zero gold pixels. claims, dossier, aggregate, plan-drift, copy-sync and machine
QA all returned zero fails and zero warns. Found by pixel critics and by counting
law-bearing pixels by hand. FIXED, upgrade 2, though not the way the instinct
proposed: see the measurements below.

**D3. Two owner rules made on 2026-09-11 were enforced by nothing, and the
master prompt ordered the opposite of one of them.** Incidents 1 and 2.
`prompts/routine_instructions.md:728` required `"sources in comments"` on the
close, which CAROUSEL_CRAFT bans outright; the `alaskaaihq.com` fixture on every
slide appears in no script and in no gate. A run following its own master prompt
to the letter prints a string the owner deleted, in artwork nobody can edit after
the post. FIXED, upgrade 3.

**D4. run_state.json says seven finished phases are pending, and no gate reads
it.** `runs/2026-09-12/run_state.json`, the SHIPPED copy, records `copy`,
`art_build`, `pixel_review`, `flow_review`, `assemble`, `scoring` and `ship` as
`pending`, while commits 304457e (art round two), 4fb97ae (score 8.72) and
438e369 (ship) prove all of them ran. Phase 11 step 5 says the completion gate
verifies that run_state shows every prior phase done; `scripts/gate_status.py`
reads `run_state.json` only through `load_json` in `artifacts_row`, for
parseability, and never looks at the phases dict. NOT FIXED, out of budget, and
it is the first recommendation below.

**D5. `AKENGRAVE.drawOffscreen` returns a 1x surface and the fix was a
docstring.** Incident 7: three rounds of repairs aimed at arcs, basin pad and
field threshold, all missing, because a hand-walked buffer consulted its reserve
at half the real position. NOT FIXED, second recommendation below.

**D6. Four chassis defects, each reported by more than one review room.** The
rays default, a rail tick that read as an em dash, `AKFIT.plate` painting hard
edged rectangles, and a sub-pixel mote. Round 1 scored per-slide 4.5 to 6.5
against a threshold of 8.3 and the run paid two further rounds. Three of the four
were DEFAULTS in a shared chassis, which is the cheapest possible place to catch
a defect and the most expensive place to ship one. The showrunner fixed all four
in the chassis during the run.

**D7. Recurring machine_qa classes, from `trend_check.py --window 10`.** 'canvas
mark near reserved text' in 5 of 10 runs (six instances in this run alone, every
one a leader or a field crossing a measured line box) and 'contact shadow' in 4
of 10. NOT FIXED: no bounded general instrument found this run. Third
recommendation.

**D8. Environment: a concurrent writer, and the merge had not happened.** This
upgrade pass was launched while the run was still in its round-3 loop: between
16:50 and 17:20 another hand added 55 lines to `assets/js/akfit.js` (the
band-gap guard), committed d441ab4 and 4fb97ae, and re-rendered
`out/2026-09-12/render`, and `main` does not yet contain the ship commit. No
collision resulted (the files I touched were untouched by it) but two renders of
the same source minutes apart are not comparable while the chassis is moving, and
one early measurement here had to be discarded for that reason.

**D9. Prune deletions sat uncommitted.** 16 deletions under `runs/2026-08-12/`
from `prune_runs.py --apply` were in the working tree when this pass began, after
the ship commit rather than in it. The run has since committed them. Worth one
line in the prompt eventually: prune before the ship commit, not after, so the
upgrade commit stays a clean revert.

## 2. FRONTIER SCAN

Focus **(c) generative/procedural art technique portable to offline Canvas/SVG**,
the stalest legal slot (last read 2026-09-03) and distinct from the last three
logged foci (2026-09-07 typography, 2026-09-09 LinkedIn platform, 2026-09-10
headless Chromium). Six searches, four fetches, two substantive reads. Both
findings are about point and line DENSITY, which is the weakness three review
rooms named today.

- Weighted sample elimination (Yuksel, EUROGRAPHICS 2015): a blue-noise subset of
  a target size out of any dense seeded candidate set, no radius chosen up front,
  optional density function. Parameters in the FIELD_NOTES entry, read out of the
  reference implementation rather than the abstract.
- Jobard and Lefer evenly-spaced streamline placement (1997): field density
  becomes one parameter, `d_sep`, with `d_test = 0.5 * d_sep`.

PARKED, both, in `knowledge/FIELD_NOTES.md` with source URLs and what each would
take. Neither is applied: the budget filled with reactive fixes, and each wants a
committed `assets/js/` helper plus a before-and-after fit on a real frame.

## 3. UPGRADES MADE (3)

**U1, engine. qa.py's totals are derived, not accumulated.** The verdict is now
summed from the slide rows after the loop, so no early exit can zero it. Verified
both ways on the reconstruction: PASS/exit 0 before, FAIL/exit 1 and `fails=1`
after; identical per-slide counts on this run's nine slides and on
examples/demo-deck.

**U2, engine. A colour law is a checked declaration.** `<body data-ink>` per
frame, an ink census at render time, two verdicts in qa.py, a pre-render JSON
parse in dossier_check, and both documents updated.

THE INSTRUMENT WAS CHOSEN BY MEASUREMENT. The gate the instinct proposed, count
pixels near each law hex, was built first and rejected: gold rays put back on
slides 01 and 08 changed 81k and 242k pixels and moved the count of gold-hued
pixels by zero, because gold at alpha 0.34 over cool ice composites to a
desaturated green; and frames that never used `#7D8F94` carry 1,727 to 40,027
pixels within dE 4 of it. So the forbidden half is judged at the BRUSH, where it
is exact, and the promised half at the FRAME, where the brush can't help.

Fit: the eight renderable shipped frames with the deck's real law declared pass
at 0 fails and 0 warns. The provenance mark in `#7D8F94` on a frame that forbids
it FAILS. Gold ticks drawn as a degenerate subpath FAIL with "reached the frame
as ZERO pixels". The sub-pixel arc variant WARNS at 33 native px^2, "1.3 px^2 in
a 432px thumb". Tolerance fitted: dE 8 hard-failed two CORRECT frames because
`#8FA3A8` sits 7.49 dE from `#7D8F94`, so it is 2.0 with a 2-to-5 warn band.

STATED LIMIT, and it is the honest boundary of this upgrade: a law-bearing ink
used in the wrong PLACE on a frame that legitimately carries it elsewhere is NOT
caught. That is the rays defect, and catching it needs either region-scoped
declarations or call-site attribution in the census. Both are bigger than a
bounded upgrade; the census already records the kind and op count, which is the
half of the evidence a future region check would need.

**U3, scripts. The owner's two 2026-09-11 rules are enforced on the render.**
`copy_sync_check.py` fails a slide that does not print `alaskaaihq.com` and any
slide that prints "sources in comments"; the master prompt's Phase 5 step 4 is
corrected. Fitted on three shipped decks: PASS on 2026-09-12 and 2026-09-11, FAIL
on 2026-09-10 naming S1 to S8 for the fixture and S9 for the banned string. In
copy_sync_check and deliberately not in qa.py, because these are house rules and
examples/demo-deck carries no brand fixture.

## 4. REFUSED, AND WHY

- **A pixels-only colour gate, as the instinct specified it.** Measured, and it
  does not see two of the three defects it was written for. Building it as
  specified would have produced a gate that reads PASS on the two most expensive
  breaches in the run.
- **A pixel threshold for a near-neutral ink.** There is none: the anti-aliased
  edge of every light cool ink passes through `#7D8F94`. The check abstains
  there, silently and on purpose, and the brush census carries it.
- **The `getImageData` guard, the run_state phase row, and a general instrument
  for 'canvas mark near reserved text'.** All three are wanted; the budget is
  three and the first three were reactive and fitted. Recommendations, in order:
  1. A `gate_status.py` row that FAILS when `run_state.json` still shows a
     pending phase at ship. D4 shipped today and nothing saw it. Ten lines.
  2. A render-time hook that flags a `getImageData` whose requested width exceeds
     its source canvas's width. Free, fires on the mistake rather than on the
     reader, and would have saved three wrong diagnoses today.
  3. The leader-routing question behind 'canvas mark near reserved text' in 5 of
     10 runs: every instance today was a leader or a field crossing a measured
     line box. The general instrument is probably a router that takes the
     reserved boxes as obstacles, not another gate.
