# AUTOMATION RETRO, run No.67, 2026-09-24

Phase 12, written after Phase 11 opened PR #397 and before the merge. ONE
upgrade (a reactive fix aimed at the standing repeat offender), three frontier
findings parked, one maintainer proposal (the rubric's weight sum). Evidence is
`out/2026-09-24/run_state.json`, `WORKLOG.md`, the storyboard's BUILD
RECONCILIATION (rounds 1 to 5 and the Phase 10 repair), `score_report.json`,
the showrunner's incident notes, and measurements taken during this retro.

---

## 0. THE STANDING OFFENDER: worked on

`python3 scripts/trend_check.py --window 10`, run first:

    weakest  8/10  mean 7.0  last 7.0  Artwork craft and genuine detail  worked 2026-09-14 (8 run(s) ago)  <-- STALE
    weakest  1/10  mean 7.5  last 8.0  Deliverable completeness          worked never                      <-- STALE
    weakest  1/10  mean 8.2  last 8.0  Alaska authenticity ...            worked 2026-09-20 (3 run(s) ago)  <-- STALE

Top offender: ARTWORK CRAFT, weakest in 8 of the last 10, and weakest again
today (scorer: 7, named slide 08). DECISION: WORK ON IT, and this run's own
incident is the most direct handle on it the machine has had in a while,
because today's artwork shortfall has a MEASURABLE cause rather than a taste
one. Slide 08 went through five critic rounds plus a scoring repair (dashes,
then a void, then blocks, then a blur) and never cleared, and the defect was
the camera STATION, a reverse shot over flats whose relief lay outside the DEM
crop. Every round answered it with a renderer parameter. The upgrade below
makes the station's ground a number that can be read before a pixel is drawn.

Honest scope: this attacks one proximate cause of one engine's artwork
shortfall. It does not touch the offender's general form (the scorer's
artwork notes across the window are mostly about genuine detail density),
and it will not move the mean on its own. What would have to be true to
tackle the general form: a structured `defect_class` on every pixel-critic
finding, so the machine can see WHICH artwork defect recurs across decks
rather than that artwork is low. That prerequisite is parked below.

## 1. REACTIVE RETRO, phase by phase against the spec

### wake, craft_refresh
Clean. Run date resolved correctly (runs/2026-09-23 already No.66). Effort
recorded `high`. NEXT_RUN.md correctly left PARKED. Craft refresh: two searches,
nothing new, FIELD_NOTES untouched, per spec.

### research (Phase 2), claims (Phase 3)
Environment breakage, RECURRING and not fixable here: `akleg.gov` BASIS 403 to
three scouts (A, F on SB 250), `eielson.af.mil` 403, UAA news 403, Alaska
Beacon 403 (read through its alaskapublic.org and KTOO republications). All
routed around through secondary or republished sources, and the cron-side
`docket_watch.py` still reads BASIS, so the 403 is specific to the scout's
fetch path. Nothing to fix in the machine; noted so it is not re-diagnosed.
58 claims, `plan_drift` 0 drifts, aggregate_check 17 declared.

### docket (3.5), gas watch / cron / site (3.6)
Handled per protocol. CINGSA has published no reading since 09/13 21:00, three
days past its own announced maintenance window; the collector failed loudly as
designed, carried nothing forward, and the run wrote `gaswatch_incident.json`
and `cron_incidents.json` (blocker `upstream`) with evidence. Gate rows WARN,
not PASS, as the policy requires. One site fix (halo, fa7bfadb).

### selection, directors room, copy (4 to 6)
Clean. Caption PASS at 878 chars.

### art build (Phase 7): a new engine built in-run
`assets/js/akvalley.js` (technique 96) was written this run. That is within the
spec (the variety law pushes for it) but it means the camera stations were
solved by guess-and-render: the showrunner only wrote a node probe harness in
scratch partway through. Stations measurably lost rounds:
- 04, round 1: re-solved 70 km north, OFF the DEM (it ends at 65.00 N). V.camera
  silently assumed 100 m of ground (`heightAt(...) || 100`), cropDepth collapsed
  to 1 km, and the haze took the whole frame. Critic 5.6. Nothing in the machine
  said "off the DEM"; the downstream symptoms were all anyone saw.
- 06, round 2: a re-aim put the camera beside the hills north of town.
- 08, rounds 1 to 5: see section 0.

DEVIATION FOUND BY MEASUREMENT IN THIS RETRO, invisible to every gate. The
BUILD RECONCILIATION says "Cameras are solved, not typed" for 03 to 09. Probing
the shipped `V.aim` calls with the new probe: 04 misses its `yFar` by 0.4 px,
but 03 misses by 81 px, 05 by 130 px and 09 by 215 px. `V.aim` holds the target
row exactly and returns its best try at the far row WITHOUT SAYING SO. The
dossier numbers for those three frames' far ground are therefore not what
shipped. No visible defect resulted (the slides were judged on pixels), but it
is a written-versus-built drift of exactly the kind the reconciliation exists
to catch, and it could not be caught because the number was never printed.

### pixel review, flow review (Phase 8)
Five edit rounds, the cap. Critic ranges 5.9-7.2, 5.6-7.6, 6.9-8.3, 7.0-8.4,
then 02 8.0 / 03 8.1 / 08 6.9. EVERY round named flat ground as ruled paper,
and every round's answer was a renderer option: spacing/minGap,
relief/contrast, haze, quietFlat, shadeSmooth, tonal. Those options are real
and are now documented craft (technique 96), but on 08 they were treating a
station problem. The machine measures ground at the station now (upgrade U1);
the loop-level rule ("two rounds naming the same defect on the same slide means
change the plan, not a parameter") is PARKED below with its prerequisite.

GATES THAT CAUGHT REAL THINGS, credited so a later run does not loosen them:
- qa's ink census caught fog and tonal quantisation over the 160-ink cap
  (fog quantised to eighths; tonal quantised in steps of 6 per channel).
- The stale-render check caught renders older than a shared asset.
- An on-canvas knockout laid over an axis on 05 cut a gap that qa read,
  CORRECTLY, as an undeclared mark. Fixed by knocking out before drawing the
  axis; the rule is already in FIELD_NOTES and technique 96.

### assemble (9), scoring (10)
Vector PDF 9.91 MB. Scorer cycle 1 8.29, cycle 2 8.34 as written.

DEVIATION: the Phase 10 repair shipped a state no critic reviewed. The spec's
scoring-cycle revision is "fix, re-render, re-review touched slides, re-score".
08 was re-reviewed at 7.2, and THEN the Nenana fade was added. The scorer says
so in its email notes. Small, but it is exactly the "best round, not last
round" problem parked below.

DEVIATION IN THE SCORER'S EMAIL TEXT, to fix at Phase 13 rather than in code:
the scorer wrote "on a true 10-point scale this is 7.58, BELOW 7.7". That
compares a normalised score against an as-written threshold. On one basis:
8.34 as written against 7.7 as written, or 7.58 normalised against 7.00
normalised (7.7 / 1.10). The deck clears on either basis. The draft should
not tell the maintainer the deck is below threshold.

### WORKLOG
P10 still reads IN PROGRESS and P11 TODO while run_state says both done.
Cosmetic; the showrunner updates it at the upgrade commit.

## 2. MAINTAINER PROPOSAL: the rubric's weights sum to 1.10 (NOT changed)

Measured, not taken on trust: `config/scoring_rubric.yaml` has had three
revisions (c70f6042 July 8th, 4afc86cd July 11th, 5197f1ca July 30th) and all
three sum to 1.10 over the same ten criteria:

    0.14 + 0.14 + 0.16 + 0.14 + 0.12 + 0.10 + 0.08 + 0.07 + 0.05 + 0.10 = 1.10

So the scale runs 0 to 11.0, every shipped score since run No.1 is on that
basis, and so are the thresholds. On a true 10-point scale they are:

    ladder 0-2 rounds  8.3 / 1.10 = 7.545
    ladder 3 rounds    8.0 / 1.10 = 7.273
    ladder 4+ rounds   7.7 / 1.10 = 7.000
    this run           8.34 / 1.10 = 7.58   (cycle 1: 8.29 / 1.10 = 7.536)

Effective weight shares are each weight / 1.10: artwork 14.5 percent, cover,
arc and fusion 12.7 each, authenticity 10.9, insight and completeness 9.1 each,
variety 7.3, legibility 6.4, copy 4.5. The ranking of criteria is unchanged by
the sum, and trend_check's per-criterion means are raw scores, unaffected.

Three options, all the maintainer's (a scoring-basis change is a threshold
change, and Phase 12 does not move thresholds):
- (A) RECOMMENDED. Document the basis: a comment in the rubric stating the sum
  is 1.10 and the thresholds are on that basis. Zero behaviour change, keeps 67
  runs of history comparable. Optionally a check that fails if the sum moves
  from the DOCUMENTED value, so the next edit to a weight is deliberate. Not
  wired this run, per instruction.
- (B) Normalise the weights (divide each by 1.10) AND the ladder (7.55 / 7.27 /
  7.00). Outcomes identical to today; every historical score in runs/ then
  needs a /1.10 when compared, and trend_check's SCORE line would need a
  basis switch at the cut-over date.
- (C) Normalise the weights and KEEP 8.3 / 8.0 / 7.7. That is a 10 percent
  tightening of every threshold (8.3 on the true scale is 9.13 as written).
  Legitimate, but it is raising the bar, and every one of the last ten runs
  would have failed the base threshold under it.

## 3. FRONTIER SCAN, focus (f) self-improving pipelines

Focus choice: the last three scan_log entries are 2026-09-23 (b), 2026-09-21 (g),
2026-09-20 (c). Legal slots (a), (d), (e), (f); (f) is the stalest, last read
2026-09-15. Relevant as well as stale: today's biggest loss was a critic loop
that repeated one diagnosis for five rounds. 6 searches, 6 fetches.

Found:
- Refine-render-judge loops where repeated failures "permit progressively
  broader changes, from local field edits to element regrouping and full scene
  re-planning"; more rounds give diminishing returns (average rounds to PASS
  2.04 to 2.31 when the cap goes from 4 to 8). https://arxiv.org/html/2607.29679
- Iterative LLM bug fixing damages correct code faster than it repairs buggy
  code and falls into "pseudo-bug-fixing" cycles. https://arxiv.org/abs/2609.10123
- Semantic early stopping for writer/critic loops: 38 percent fewer tokens at
  parity, but "which round is best" stays open; an oracle choosing the best
  round beat every practical policy. https://arxiv.org/abs/2606.27009
- Tool-making from repeated diagnoses: 94.5 percent pass@1 where retrying
  without reflection plateaued near 92.5 percent "because additional rounds
  repeat the same diagnostic errors". https://arxiv.org/html/2607.08010

Outcome: the tool-making finding SUPPORTS U1 (promoting a scratch diagnostic
into a committed, tested tool) but U1 is a reactive fix and is logged as one.
Repeated-defect escalation and best-round shipping are PARKED in
knowledge/FIELD_NOTES.md with their shared prerequisite (structured per-finding
defect classes and per-round per-slide scores). Neither is safely boundable as
code today; as prose they would be one more sentence a run can skip.

## 4. UPGRADES (1)

### U1, fix, area assets + scripts + knowledge: the camera station is measured before it is rendered

- `scripts/akv_probe.js` (new, node, no dependencies): the scratch harness,
  committed and self-tested. Takes the exact `aim` or `camera` options a slide
  passes and prints onDem, cropDepthKm, bottomRowKm (left/centre/right, by ray
  march against the DEM), nearReliefM and nearTextureM (p10 to p90 of the
  ground the bottom edge opens onto, raw and minus its 1.6 km box mean), each
  named target's screen point, depth, inFrame and line of sight, `solve.errPx`
  for aims, and a `problems` list (off the DEM, far row missed, pitch clamped at
  the search edge, lens shift off the frame, bottom row finds no ground, crop
  edge in the lower third, target out of frame or hidden). It reports and
  decides nothing. `--expr` keeps the scratch harness's free-form mode.
- `assets/js/akvalley.js`: `V.camera` console.errors `AKVALLEY: camera at ...
  is OFF the DEM ...` (qa records a WARN) and sets `cam.onDem`. `V.aim` passes
  `silent` through its pitch search so only the kept camera can warn.
- `knowledge/TECHNIQUE_LIBRARY.md` #96: the "twenty-line harness" prose is now
  the command, with the two numbers to read and their measured calibration.

Calibration on the shipped stations (nearTextureM, true metres): 01 51.0,
02 61.7, 03 12.1, 04 11.8, 05 1.5, 08 1.9, 09 51.5. 08's flats and 05's flats
read under 2 m; the frames the critics praised for relief read about 50 m. 05
shipped at critic 8.2 with 1.5 m because its ground is a chart floor, which is
why this is a REPORT and not a gate: a threshold here would fail a correct
frame (the 2026-09-17 lesson).

Verification:
- `node scripts/akv_probe.js --self-test`: PASS, 7 stations, 3 reconstructed
  defects. (1) 04 round 1 (70 km north) is reported off the DEM with the
  problem named; 04 as shipped (48 km) is on the DEM with ENN in frame, seen,
  and on row 860 within 3 px. (2) 08's near texture is under 5 m and 01's is
  more than 5x it (1.9 vs 51.0). (3) 09's unmet yFar is reported (residual
  214.9 px) while its target row holds. Plus a straight-down camera sees ground
  under itself and a sky-pitched one finds none.
- render.py + qa.py on this run's nine slides (out/2026-09-24/slides): 9/9 OK,
  qa PASS, 0 fails 0 warns, and ALL NINE PNGs byte-identical by sha256 to the
  shipped out/2026-09-24/render, so the engine change costs no pixel and adds
  no warn to a correct deck.
- render.py + qa.py on examples/demo-deck: 4/4 OK, qa 0 fails / 14 warns
  (3, 5, 5, 1), the known pre-existing baseline recorded by the 2026-09-20 and
  2026-09-21 entries; the demo does not load akvalley.
- DEFECT RECONSTRUCTION through the real render path: slide 04 with round 1's
  station (distKm 70, fov 50) renders and qa now carries `warn: console error:
  AKVALLEY: camera at -149.031, 65.181 is OFF the DEM (-150.20 to -147.90 E,
  64.05 to 65.00 N) ...` alongside the two symptom FAILs the existing gates
  already raised (dead lower zone; the slide's own "four corners in frame"
  assertion). Before this change those symptoms had no named cause.
- Rollback: revert the upgrade(2026-09-24) commit; or by path,
  `git checkout <commit>^ -- assets/js/akvalley.js knowledge/TECHNIQUE_LIBRARY.md
  knowledge/FIELD_NOTES.md` and `git rm scripts/akv_probe.js`.

Not done, deliberately: making `V.aim` itself console.error on a missed
`yFar`. It would be true, but it would turn three of today's reviewed, shipped
slides WARN on re-render for a row whose miss produced no visible defect. The
probe reports it where the station is chosen, which is where it is useful.

## 5. PARKED (knowledge/FIELD_NOTES.md, 2026-09-24 Phase 12)

- Repeated-defect escalation for Phase 8 (arXiv 2607.29679, 2609.10123).
- Best round, not last round, per slide (arXiv 2606.27009).
- Shared prerequisite: pixel critics emit a structured `defect_class` per
  finding and a per-slide score per round, in a file a check can read.

## 6. FOR THE EMAIL

- One upgrade: `scripts/akv_probe.js` + akvalley off-DEM WARN.
- Maintainer decision requested: the rubric's 1.10 weight sum (section 2).
- Do not tell the maintainer 7.58 is below 7.7; those are two different bases.
- Slide 08's shipped state (the fade) was not critic-reviewed.
