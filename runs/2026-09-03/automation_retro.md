# AUTOMATION RETRO — run 2026-09-03 (No.49)

Written in Phase 12 by the upgrade-engineer, before the merge and before the
Gmail draft. Score 8.81 against a threshold of 8.30, on the fourth scoring
after three revision rounds.

## 0. THE STANDING REPEAT OFFENDER, ANSWERED

`python scripts/trend_check.py --window 10`:

```
weakest  8/10  mean 6.7  last 7.0  Artwork craft and genuine detail   worked 2026-08-31 (3 runs ago)  <-- STALE
weakest  1/10  mean 7.7  last 8.0  Story arc and swipe momentum       worked 2026-07-30 (29 runs ago)
weakest  1/10  mean 8.1  last 9.0  Deliverable completeness           worked never
```

**Artwork craft is WORKED this run, not deferred.** Upgrade 2 below is an
artwork-craft upgrade and nothing else: it names, in the engine, the single
geometric fault that produced four separate artwork defects in this one deck
(slides 01, 06, 08 and 09; the run diagnosed each one on its own and only the
fourth found the cause). The scorer's own weakest-criterion note for the shipped
deck reads "three genuinely different ground materials on 01, 07 and 09 instead
of one swelled-contour lay at three scales", which is the same bench.

Worth stating plainly, because it is the honest measure of the upgrade: the
probe run against the SHIPPED nine slides reports slides 05 and 08 still
carrying a fully collapsed lay (alignment 1.00 of 1.00). The deck shipped at
8.81 with two regions of art that draw one stroke a hundred and seventy times.
Next run gets told that at render time instead of after five critic reports.

## 1. DEVIATIONS, PHASE BY PHASE, WITH EVIDENCE

Read from `out/2026-09-03/run_state.json`, the render and QA reports, and the
showrunner's incident notes.

| # | Phase | Deviation | Evidence | Cost |
|---|---|---|---|---|
| 1 | art_build | `AKNIGHT.veil` ADDED two crossed alpha ramps where the operator had to be a PRODUCT, printing the flat plate the function exists to prevent behind type on 6 of 9 slides | run_state `artifacts/veil_defect`; five pixel-critic reports on the symptom, one on the cause; fixed in `assets/js/aknight.js` during the run | one render cycle, one repair round |
| 2 | art_build | Three successive repairs to that module changed no pixels, because all nine call sites passed `{alpha: 0.74, feather: 26}` and overrode every tuned default | incident notes 2 | two wasted render cycles |
| 3 | art_build | An engrave form varying in one axis only makes the lay knot; diagnosed four times as four defects | incident notes 3; run_state `weakest_criterion` | four diagnoses of one cause |
| 4 | pixel_review | Contact shadows repaired TO THE GATE FLOOR measured dL 35 to 45 against a known-good 8.1 and read as stage spotlights; only a human look caught it | incident notes 4; FIELD_NOTES 2026-09-03 "a gate floor is not a target" | one repair round |
| 5 | scoring r1 | `gate_status.reconciled` read PASS while BUILD RECONCILIATION held only the template's instruction to write one (3 lines, 228 chars, over a 40-char floor). The scorer hard-failed it | incident notes 5; run_state `artifacts/score_round_1` | one full scoring cycle |
| 6 | render/qa | qa.py demoted a text collision to WARN whenever either party carried `data-decorative`; the scoring rubric's hard fail for overlapping text has no such exemption | incident notes 6; slide 06 gold estimate label under the shot log at 39% (round 2), slide 05 shot log on the page counter's baseline (round 3) | two capped scoring rounds |
| 7 | scoring r2-3 | Editing the run record to match a build that was then edited again introduced four new record defects in one round; no gate reads the reconciliation's PROSE against the build it describes | incident notes 7 | one round |
| 8 | docket | The BASIS legislature sweep returned HTTP 503, so an empty bills list proved nothing | run_state `artifacts/docket_note` | none, correctly recorded as unknown rather than as absence |

The pattern the whole list points at, and it is not "the gates are too weak":
**three of this run's four scoring rounds were capped by a defect a machine gate
had already looked at and passed.** Deviations 5 and 6 are two instruments
disagreeing about one artifact, and the instrument that stops a ship is the one
that was right both times. Each blind spot is cheap to close once named, which
is what this phase spent its budget on.

Deviation 8 is not a machine fault. Deviations 1, 2 and 7 are process faults
with no bounded machinery behind them this run; see section 4.

## 2. FRONTIER SCAN — focus (c), procedural art portable to offline Canvas/SVG

Rotation check: the last three logged foci are 2026-09-02 (e) headless
Chromium, 2026-09-01 (a) LinkedIn platform, 2026-08-31 (d) typography. (c) is
both legal and the stalest slot, last scanned 2026-08-26 (8 days), and it is the
area the standing repeat offender lives in. 8 searches, 3 fetch attempts, 2
substantive reads, plus one local simulation of the engine's own code.

Both substantive sources land on the same joint of `akengrave`, from opposite
directions:

1. **A Primitive for Manual Hatching**, Philbrick and Kaplan, ACM TOG 2022.
   https://cs.uwaterloo.ca/~csk/publications/Papers/philbrick_kaplan_2022.pdf
   A hatching shape is a mask plus three FIELDS, width, spacing and direction,
   plus barrier curves marks may not cross, with marks placed by streamline
   advection. akengrave has the mask, the width field and the direction field.
   Its spacing is one scalar `gap` on a fixed raster and it has no barriers.
2. **Creating Evenly-Spaced Streamlines of Arbitrary Density**, Jobard and
   Lefer 1997, with an MIT JS implementation at
   https://github.com/anvaka/streamlines (`dSep`, `dTest`, RK4). Seed each new
   line at `dSep` from the accepted set, integrate, stop within `dTest` of a
   neighbour, query through a uniform grid sized `dSep`. Under that rule this
   run's collapse is impossible by construction, because the second seed on a
   shared iso-line is rejected before it draws.

OUTCOME: PARKED, in knowledge/FIELD_NOTES.md under 2026-09-03 with both URLs.
Replacing raster seeding with a spacing field and a separation test is a
redesign of the drawing core: every deck that used the bench would re-render
differently, and it can't be verified by the pixel-identity check that made
today's engine change safe. Parking it also cost nothing this run, because the
budget was already full of reactive fixes that outrank a frontier improvement.
What would have to be true to apply it is written into the parked entry.

## 3. UPGRADES MADE — 3, all reactive fixes

Three, not the usual one, because deviations 5 and 6 each cost a scoring cycle
and deviation 3 is the standing repeat offender.

**1. qa.py stops exempting `data-decorative` from the text-collision gate.**
(deviation 6). `data-decorative` means "do not judge this as primary copy": it
exempts a slug from the 24px floor, the contrast check and the unsized-type
check, and it should. It has never meant "this type may be printed through other
type", and the rubric that stops a ship has never granted it. The attribute for
deliberate layering is a different one, `data-overlap-ok`, and that still
demotes to WARN. This is a tightening (WARN becomes FAIL), never a loosening,
and the message now says which of the pair is decorative and what to mark
instead.

**2. akengrave measures its own lay before it draws it** (deviation 3, and the
standing artwork-craft offender). `_layCheck` probes the mean |cos| between the
walk direction and the seeding raster over a 12x12 grid of the region and
console.errors above 0.90, which qa.py already records as a WARN. Simulating the
module's own `_walk` off the file proved the mechanism: with a form that falls
along x only, all 170 seeds sit on ONE iso-line and the pass draws one swelled
ribbon 170 times. `angOff` can't rescue it, because the raster is `angOff + 90`
and the walk is `isoAngle + angOff`, so both rotate together. The new optional
`seedDeg` turns the seeding raster alone and leaves the modelling untouched;
defaulting it to null keeps every previously shipped engraving pixel-identical,
which was measured and not assumed.

**3. gate_status.reconciled can see the difference between an answer and the
question** (deviation 5). The 40-char floor is a test of presence and the
failure that actually happened was a section holding the template's own
instruction, at 228 chars. The row now also requires the section to be
SPECIFIC: it names a slide, or lays out a table with a data row, or says
outright that nothing diverged. Boilerplate does none of the three and no honest
reconciliation fails all three, so this does not teach a run to pad. Staleness
is still not checked and still not claimed.

## 4. NOT DONE, AND WHY

- **A ceiling or a comfort BAND on the contact-shadow gate** (deviation 4). The
  gate has a floor and a "comfort band" message and no upper bound, so repairing
  to the number produced six stage spotlights. This is the fourth candidate and
  the budget is three; more importantly, choosing the top of the band is a
  judgement about what a lit wet road looks like, not an arithmetic repair, and
  the known-good reading is a single sample (8.1). RECOMMENDED to the
  maintainer: a WARN above roughly 20 dL, calibrated on more than one deck.
- **A lint for a module default that no call site can reach** (deviation 2). A
  real defect, three wasted repairs, and every sketch of the check is either a
  grep discipline (prose, not machinery) or a JS call-graph analysis (not
  bounded). Written up rather than coded.
- **A gate reading the reconciliation's prose against the build** (deviation 7).
  That is a semantic diff of English against HTML. Not bounded, not attempted.
- **Nothing near the Gas Watch.** No collector, no coefficient, no ledger, no
  parser was touched, and no upgrade this run goes anywhere near
  `scripts/gaswatch_build.py`, so its self-test and the page check were not
  required and were not run.

## 5. VERIFICATION

Every change was run before it counted.

- `scripts/gate_status.py --self-test`: 25 checks, 0 failures, including two NEW
  reconstructions: the No.49 defect (the template's instruction alone) now
  FAILS, and the same boilerplate with one real slide note under it PASSES. The
  older No.39 reconstructions still pass unchanged.
- `scripts/gate_status.py --run out/2026-09-03`: `[PASS] reconciled BUILD
  RECONCILIATION present, 117 line(s), 8692 chars`, 0 FAIL rows. The tightened
  row does not retroactively break this run's own record.
- DEFECT RECONSTRUCTION for upgrade 1: slide 05 rebuilt with its decorative shot
  log slid under the page counter. Under the OLD code, two `warn: text collision
  (45% overprint) [decorative involved]`, verdict WARN, exit 0. Under the new
  code, two `FAIL`, verdict FAIL, exit 1, one of them a decorative-on-decorative
  pair. With `data-overlap-ok` added to the same slide, back to two WARNs and 0
  fails, so the escape hatch still works.
- `render.py` + `qa.py` on THIS RUN'S nine slides: 9/9 rendered, 0 errors, 0
  fails, and all 18 PNGs (9 slides + 9 canvas layers) byte-identical by md5 to
  the run's own pre-change render.
- PIXEL NEUTRALITY, PROVED A/B RATHER THAN BY MEMORY. Midway through this phase
  the same nine slides started rendering differently between two runs of
  identical code, and the cause was the tree moving underneath: the showrunner
  was still editing `out/2026-09-03/slides/` (slide-04.html changed during one
  of the renders, which briefly reported a motif FAIL on a half-saved file). So
  the check was redone properly, against drift: the nine slides were FROZEN to a
  snapshot, rendered once with the new `akengrave.js` and once with
  `git show HEAD:assets/js/akengrave.js`, with the snapshot's md5s verified
  unchanged across both. **18 of 18 PNGs identical.** Upgrade 2 changes no
  pixels, and that is measured rather than argued.
- On that same frozen snapshot: 0 fails under both the old and the new qa.py,
  and warns go from 3 to 6, the three new ones being the lay probe naming slide
  05's main lay and slide 08's main and cross lays, all at alignment 1.00.
- `render.py` + `qa.py` on `examples/demo-deck`: 4/4 rendered, 0 errors, 0 fails,
  warns unchanged from the pre-change baseline (the demo deck does not load
  akengrave and carries no text collisions).
- Calibration for the 0.90 threshold is measured, not guessed: 1.00 for a
  one-axis fall, 0.66 for a form falling in both, 0.00 for a fall along the
  other axis or a flat region, and 0.00, 0.11, 0.19, 0.21, 0.51 across the seven
  healthy passes of this deck.

## 6. FILES TOUCHED

```
.claude/skills/carousel-engine/qa.py        upgrade 1 + its header contract
.claude/skills/carousel-engine/SKILL.md     what data-decorative does and does not exempt
scripts/gate_status.py                      upgrade 3 + 2 new self-test reconstructions
assets/js/akengrave.js                      upgrade 2, _layCheck + seedDeg
knowledge/TECHNIQUE_LIBRARY.md              technique 93, the collapse and its two cures
knowledge/FIELD_NOTES.md                    the measured cause, and the parked scan finding
ledger/upgrades.json                        3 entries + 1 scan_log entry
out/2026-09-03/automation_retro.md          this file
```
