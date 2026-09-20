# AUTOMATION RETRO -- run 2026-08-20, Carousel No. 38, "Alaska Bought American. The Tariff Found a Seam."

Score 8.39 against a threshold of 7.7, at revision round 4 (7.62, 7.99, then
8.39 capped to 6.9 by one text overlap, then 8.39 clean). Shipped and merged.
Phase 12, upgrade engineer. Budget spent: 3 of 3, ALL REACTIVE.

`trend_check --window 10` still names **"Artwork craft and genuine detail"** the
weakest criterion in 7 of the last 10 runs, mean 6.5, last worked 2026-08-07 and
marked STALE. Two of this run's three upgrades land on it directly: the wrong
MATERIAL on two slides (upgrade 1) and the annotation that encloses nothing
(upgrade 3) are both artwork-craft defects that the pixel critics scored and no
gate could see.

---

## 1. REACTIVE RETRO -- deviations, with evidence

**D1. NINE PIXEL CRITICS RETURNED A MEAN OF 4.28 WHILE MACHINE QA WAS WARN WITH
ZERO FAILS.** (run_state.json `round_1_pixel_scores`: 3.5, 4.0, 5.0, 6.0, 4.0,
2.5, 4.0, 5.0, 4.5.) Every defect they found was invisible to the machine and
nearly all were one shape, A DECLARATION POINTING AT NOTHING:

- S06's four dashed gold origin contours, the deck's central accuracy device,
  were HARDCODED SCREEN ELLIPSES while the parts they name were placed by a 3D
  camera. Every one enclosed bare foam. Repaired in-run by deriving each contour
  from its part's projected bounding box (slide-06.html `bboxOf`).
- S09's declared inspection window sat on the lid at BH+0.032 with its own snow
  cap at BH+0.040, i.e. under its own snow.
- S09's and S05's contact shadows were composited in multiply AFTER their
  objects, so the shadow was painted across the object's own faces and a solid
  read as glass.
- S08's rate bars stood ON a rail whose x is a DECLARED date axis. `data-scale`
  checks ink INSIDE its band and has no opinion about what stands on it.
- Four `data-encodes` / `data-contacts` rects had to be re-measured off the
  rendered PNG after objects moved; several originally pointed at background.

**D2. AN ENGINE CONTRACT DEFECT, and it is worse than the field note recorded.**
`AK.reliefShade` writes ImageData straight into its region: it REPLACES what is
under it and has no blend/alpha/mix option at all. Two slides passed
`mix: 0.30` / `mix: 0.34`, silently ignored, so an intended 30 percent finish was
a 100 percent overwrite; slide 05's cold white bond printed as kraft with every
printed line erased under a gold marker highlighting a blank sheet, and slide
07's anodize printed as a cardboard carton.

Found today, and NOT previously recorded: the SHIPPED deck still carries the
defect. `out/2026-08-20/slides/slide-07.html:261` still passes `mix: 0.20`, and
BOTH slides pass `light: [-0.55,-0.68,0.48]` when the option is
`lights: [{az,el,w}]`. Three silently ignored options survived nine pixel
critics, four revision rounds, every gate and the merge.

**D3. PLAN-VERSUS-PIXEL DRIFT, flagged by the scorer in all three scoring rounds
and never fully caught.** Also worse than recorded: the storyboard that SHIPPED
still assigns C03 to slide 08, C07 to slide 07, C10 to slides 06 and 08, and C24
to slide 06, where copy.json does not carry them and the render prints no such
tag. Slide 08's dossier still says "FIVE declared marks" (three are declared in
the markup and drawn) and "TWO DECLARED MEASURED AXES" (one `data-scale` entry
in the build). Every instance was found by a human-equivalent reader.

**D4. COLLISION WHACK-A-MOLE.** Slide 03 lost its axis label to the scope flag,
then lost the flag's LAST WORD to the 40x bracket after a re-break, which is
what capped round 3 at 6.9, then broke the leader gate when the label moved
clear. Not gated today: see the PARK below, which is where the honest answer to
this one sits.

**D5. Not a defect, recorded for the trend.** The final machine QA was PASS with
zero fails AND zero warns on all nine slides, the first clean pass in some time,
which is precisely why D1-D3 matter: the gates were all green while the deck was
scoring 4.28 by eye.

---

## 2. FRONTIER SCAN

Focus **(d) typography and layout craft**, aimed at the collision defect D4.
The stalest legal slot (last scanned 2026-08-07, 13 days) and distinct from the
last three logged foci (2026-08-19 self-improving pipelines, 2026-08-18
editorial dataviz, 2026-08-16 procedural art). 3 searches, 4 fetches, 3 read.

1. **The applicable finding, parked.** "Legible Label Layout for Data
   Visualization" (arXiv 2405.10953) gives a placement algorithm with real
   parameters: an OCCUPANCY BITMAP of already-placed ink plus the 8-POSITION
   candidate model (four corners, four sides) walked greedily in a single pass,
   with a configurable padding for how far a label may extend past the chart
   area and a binary search for the largest same-aspect rectangle inside an
   area. Measured 22 percent faster than particle-based labeling on a 3,320
   airport map for 0.8 to 3.2 percent fewer labels placed. kevinschaul's
   `avoid-overlap` is the readable news-graphics implementation of the same
   problem with simulated annealing (defaults: 10,000 iterations, temperature
   100, cooling 0.995) and the useful vocabulary of nudge / choices / fixed plus
   quadratic priority weighting. This is the machinery D4 wants: place the
   band's three elements against a bitmap of what is already down, rather than
   moving one element and moving the collision. ~100 lines of vanilla JS, no
   dependency. PARKED, not applied: the whole 0-3 budget went reactive-first,
   and a placement engine wants its own commit with its own reconstruction.

2. **Reconfirmed null.** CSS `text-wrap: balance` (Chromium 114+, capped at 6
   lines) and `pretty` (117+, orphans only, not widows) still give no line-count
   or overflow guarantee, so `AK.fitText`'s JS binary-search fit-to-box remains
   the correct headline mechanism. Unchanged since 2026-07-09 and re-checked
   against MDN and the Chrome blog today.

3. **Null result worth recording.** A search for editorial/news-graphics
   typography craft for 2026 returned SEO listicles only ("top infographic
   typography trends"), nothing with a parameter in it. The house's own
   DESIGN_DOCTRINE is ahead of what that query reaches.

---

## 3. UPGRADES (3, all reactive, all verified)

**U1. `AK.reliefShade` refuses an option it does not know, and its ramp is
required.** Unknown key -> `console.error("AK CONTRACT: ...")` then throw; qa.py
now FAILS on the `AK CONTRACT:` prefix instead of warning, because slide code
legitimately wraps art calls in try/catch and a swallowed throw is the same
silent no-op. Messages name the remedy per key (`mix` -> there is no blend, lay
the substrate first or composite a finish yourself; `light` -> the option is
`lights`), with a nearest-key suggestion otherwise.
Verified: reconstruction A (this run's exact shape, throw swallowed by the
author's catch) -> qa FAIL naming both `light` and `mix`; reconstruction B
(unset ramp, uncaught) -> render.py HARD FAIL; control (correct call) -> clean.
Re-rendering THE SHIPPED DECK now FAILS slides 05 and 07 on the real defect they
really carry, with the other seven clean. examples/demo-deck is byte-identical
in verdict before and after (WARN, 0 fails, 11 warns).

**U2. `scripts/plan_drift_check.py`, a new ship gate: the plan and the build
have to agree about the build.** Checks the storyboard's claims index against
copy.json's per-slide `claim_ids` in both directions (NOT USED must appear
nowhere), and every "<N> declared marks / leaders / measured axes / encodings /
contact shadows" sentence in a dossier against what the slide body declares in
the render report. Printed claim tags are reported as evidence of which artifact
drifted, never as a source of pass or fail. Zero claim_ids in copy.json is
CANNOT LOOK (exit 2), like copy_sync_check's zero-strings rule.
Verified: `--self-test` (11 checks, hermetic) covers both No.38 defect shapes
and the aliasing bug found while building it; on this run it reports all seven
real drifts, including "FIVE declared marks" against 3; across the 27 shipped
runs that carry both artifacts it finds 1 to 10 drifts each and no false
positive survived inspection on the three sampled by hand. Row `plan_drift` in
gate_status.py; step 7 in Phase 8.

**U3. `AKT.screenBox` / `AKT.projectPoint`, so screen-space annotation is
derived from the camera.** Returns the projected bounding box of a mesh, group
or array in DESIGN px from each mesh's own local bounding box through its
matrixWorld, plus `behind` and `offscreen`, both of which console.error under
the `AK CONTRACT:` prefix because each returns a reasonable-looking rectangle
that encloses nothing.
Verified against pixels: a rotated box at a known pose reported
`BOX 361.2 522.0 370.6 322.2`; the ink measured off the rendered PNG is
`361.0 522.0 371.0 322.5`, agreement inside half a design pixel on every edge.
Aiming the camera away puts the part behind the lens and produces the contract
FAIL rather than a plausible box.

**Deliberately NOT done.** (a) No gate requiring every `data-encodes` /
`data-contacts` rect to contain non-background ink: the corpus contains honest
ABSENCE claims ("three ticks stand alone with nothing drawn between them", dE
0.4) where an empty region is the correct answer, and a blanket ink floor fails
the successes. The `differ` direction already has a fitted floor. (b) No label
placement engine (the scan's own finding), parked. (c) No change to any
threshold: U1 and U2 only add failures.

---

## 4. FOR THE MAINTAINER

The shipped No.38 deck carries two real defects this machinery now catches, and
neither was repaired here because run artifacts under `runs/` are not rewritten:
slide 07 still passes `mix: 0.20`, slides 05 and 07 still pass `light:`, and the
shipped storyboard's claims index still over-assigns four claim ids. Both are
recorded above rather than quietly fixed. The next run starts clean.
