# AUTOMATION RETRO - 2026-09-17, No.61 "THE DRIFT LINE"

One sentence for the whole run: every machine gate was green on the first
render, and the deck was not shippable for four more rounds. Nothing here is
about a gate that fired wrongly. It is about five defects that rendered a
plausible frame and reported nothing.

## 1. REACTIVE RETRO, phase by phase against prompts/routine_instructions.md

Phases 0 through 7 ran to spec. `run_state.json` records every phase through
`assemble` as done, `revision_rounds: 4`, and the gas watch at MAINTENANCE with
site signoff WARN on a CINGSA source four days stale inside its announced
maintenance window, which is the disclosed-warning case the rules already name
and is not a deviation.

The deviation is concentrated in Phase 8 and Phase 9, and it is one deviation
wearing five costumes.

**The evidence of the gap.** Round one: render 9/9 OK, 0 page errors, 0
overflow warnings; qa.py PASS, 0 fails, 0 warns; frame_balance clear on all
nine at 1.00 to 1.18; bespoke PASS; dossier PASS; claims 41/41. The pixel
critics on the same frames returned 4.5 to 6.0. A gate set that returns PASS on
a 4.5 deck is not wrong about what it measures, it is silent about what broke.

| # | defect | what the machine said | why nothing saw it |
|---|---|---|---|
| 1 | mesh rotation: the chassis stepped along (sin yaw, 0, cos yaw) and rotated every mesh by that same yaw, but three.js sends local X to (cos phi, 0, -sin phi), so they agree only at phi = yaw - 90 | PASS | rails ran perpendicular to their own line and read as diagonal bracing; every slat presented its 0.028 m edge, so the Restricted panel drew about 0.45 open against a printed 0.12. The deck's whole data-in-art mapping was inverted and rendered cleanly |
| 2 | ~~`mat.vertexColors = true` set after the material was built, with no `needsUpdate`~~ WITHDRAWN, see the correction below | PASS | the deposits did draw white for a full round, but NOT for this reason. Measured after the fact: deleting the `needsUpdate` line changes nothing, 0 pixels on 4 slides |
| 3 | three planes ending inside the frame: a 300 m ground plane whose edge fell at 150 m, a sky gradient whose last stop was not the fog colour, a drift carrier small enough to show its own rectangle | PASS | a full-width straight seam is a legitimate horizon to every gate here |
| 4 | law-bearing gold and forget-me-not marks moved into 2D at hand-tuned constants | PASS | the move itself was right (it fixed the ink census and 432 px legibility); the marks then floated on open snow on four frames. `D.camera` and `D.snapToSilhouette` were written this run to fix it |
| 5 | slide 05 spaced slats on a 5.4 px width, stroked them at 2.4, and `window.__akAssert` computed the open fraction from 5.4 | PASS, and cited as proof | the assertion agreed with the pitch and not with the picture. The deck's only measurable frame contradicted its own printed ratios under a green assertion row |

Defects 1 and 5 are the same defect from both ends: the drawing said one thing
and the deck's own arithmetic said another, and the arithmetic was derived from
the intention rather than from the drawing.

**A critic verdict declined on measurement.** Round two hard-failed slide 05 for
inverted porosity, and a luminance-run measurement showed the drawing correct
within 0.016. The same verdict reported curly apostrophes that a source sweep
proved absent. Both declines were right and both were written into the BUILD
RECONCILIATION so the next run does not "fix" a correct drawing. The cost is
that both measurements were improvised by hand mid-round; a measurement that
expensive gets skipped, and a skipped measurement means the critic wins by
assertion.

**A gate that truncated a good section.** `gate_status.reconciliation_section`
ended the BUILD RECONCILIATION at the next markdown heading of ANY level, so a
section written with `###` subheads was read as its first three lines and the
row warned on a complete reconciliation. The run flattened its subheads to bold
to get past it. A real trap for the next author, and the gate was wrong, not the
storyboard.

**Already handled this run, not revisited here:** `aggregate_check.py` learned
calendar months and years as durations (committed, verified adversarially); the
permission prompt that stopped Phase 8 (CLAUDE.md rule plus a
`.claude/settings.json` allowlist).

## 2. FRONTIER SCAN

Focus (d), typography and layout craft: the stalest legal slot, last read
September 7th, and distinct from the last three logged foci (g, b, f). Six
searches, three fetches. Nothing applied. The slot is well mined: the scan
amended an existing park (optical margin alignment now has a shipped reference
implementation, Liiift-Studio/OpticalMargin, measuring each glyph's hang from
canvas metrics rather than a lookup table) and reconfirmed the
`text-wrap: balance` / `pretty` null for the fourth time. Written up in
knowledge/FIELD_NOTES.md with source URLs, and logged in `scan_log`.

## 3. UPGRADES MADE (3, all reactive)

1. **A MATERIAL FLAG THE SHADER WAS NEVER TOLD ABOUT** (defect 2). A new source
   scan in render.py and a new FAIL in qa.py: a recompile-triggering three.js
   material property assigned as a statement after construction, with no
   `needsUpdate` on the same receiver later in the same file. Reads inline
   scripts AND the house libraries a slide loads (`assets/js/ak*.js`), because
   this defect lived in a shared chassis. Narrowed to receivers that look like
   materials, so `scene.fog` and an options object's `map` are never judged.
2. **A SUBHEADING IS PART OF THE SECTION** (the reconciliation trap). A section
   now ends at the next heading of the SAME OR HIGHER level. This can only ever
   read MORE of a section, so nothing that used to fail can start passing.
3. **scripts/measure_frame.py** (the declined verdict). A measuring instrument,
   not a gate: `porosity` reads the open fraction of a region straight off a
   render in luminance runs, and `glyphs` sweeps sources for curly quotes,
   dashes and emoji with addresses. No thresholds, never exits 1.

## 4. WHAT I RAN

- `python3 .claude/skills/carousel-engine/render.py --slides-dir out/2026-09-17/slides`
  then `qa.py`: 9/9 OK, 0 page errors, 0 overflow warnings, **verdict PASS, 0
  fails, 0 warns**. The shipped deck is unchanged by the new gate.
- The same pair on `examples/demo-deck/slides`: 4/4 OK, **verdict WARN, 0
  fails**, the same busy-art warns that deck has always carried.
- **Defect reconstruction.** Deleted the one `mat.needsUpdate = true;` line from
  `assets/js/akdrift.js` and re-rendered: render printed
  `[material] slide-01.html: mat.vertexColors at assets/js/akdrift.js:606 with
  no needsUpdate` and qa.py returned **FAIL, fails=1** on that slide. The
  chassis was restored byte for byte (`git status` clean on that file).
- **False-positive corpus.** `scan_material_flags` over 49 slides on disk
  (out/2026-09-17, examples/demo-deck, the runs/2026-09-1x decks): 1 assignment
  found, correctly paired with its `needsUpdate`, and **0 hits**. With the line
  deleted it fires on 9 of 9.
- `python3 scripts/gate_status.py --self-test`: **27 checks, 0 failures**,
  including two new ones: a section written with `###` subheads is read whole,
  and the same section truncated at its first subhead still FAILs.
- `measure_frame.py porosity` on this run's shipped slide 05, all three panels,
  `--ink light`: 0.6216 against a printed 0.62, 0.2637 against 0.28, 0.1153
  against 0.12. That reproduces the round-two decline (within 0.017) from a
  committed command instead of by hand.
- `measure_frame.py glyphs` on this run's nine slides: **0 findings**, which
  reproduces the other half of the decline. On the demo deck it reports 5 em
  dashes, all inside HTML comments in `examples/demo-deck/slides/*.html`. Those
  are real and pre-existing; not touched here, because editing those files
  changes four render fingerprints for no pixel, and the instrument has no
  authority to fail anything. Worth a separate cleanup.

## 4b. A CORRECTION TO THIS RETRO, MADE THE SAME DAY

Nine Codex findings arrived on PR #373 five minutes after it merged, so they
landed on `main` rather than on a reviewable branch. Six were real and are
fixed. Two were wrong and were declined on measurement. One had already been
fixed before the merge. The one that matters here retracts defect 2 above.

**Defect 2 was a misdiagnosis, and upgrade 1 was built on it.** Codex objected
that a material flag assigned before a material's FIRST RENDER needs no
`needsUpdate`, because three.js compiles the program lazily. That is correct,
and this run never tested the claim it made: the round-one "proof" only showed
that deleting the line makes the SCANNER fire, which says nothing about pixels.
Measured properly, by deleting `mat.needsUpdate = true` from `akdrift.js` and
re-rendering the four drift-bearing slides:

```
slide-01: max diff 0   mean 0.000   pixels>3: 0 (0.000%)
slide-06: max diff 0   mean 0.000   pixels>3: 0 (0.000%)
slide-07: max diff 0   mean 0.000   pixels>3: 0 (0.000%)
slide-09: max diff 0   mean 0.000   pixels>3: 0 (0.000%)
```

Zero. The line is a no-op in this chassis and the white drift had another
cause, almost certainly the vertex colour attribute that was added in the same
edit and got none of the credit. So the scanner matches the ordinary CORRECT
sequence (construct, set the flag, build the mesh, render), and whether an
assignment precedes first render is not decidable from source. It is now a
WARN. A FAIL on an undecidable question blocks a correct deck, which is a worse
failure than the one it was built to catch, and this house's own rule is that a
run must never be stopped by its own plumbing.

The lesson is narrower than "test your gates" and worth stating exactly: **a
test that shows the DETECTOR fires is not a test that the DEFECT exists.** Both
of this run's other declines were settled by measuring the artifact. This one
shipped a hard gate on an unmeasured story about a bug, and a reviewer had to
catch it.

**Two findings declined, both on measurement.** Codex read the porosity
polarity from the stale commit it reviewed, where it was `(sum(px)/len(px)) >
thr`; the merged version already compares class populations and takes an
explicit `--ink`. And it predicted hard top and bottom edges on `D.footAO`'s
pool ellipses, on the premise that a Canvas2D gradient freezes the transform
from creation time. It does not, the CTM applies at paint time. Measured in
Chromium at `rx 150, ry 45`: alpha runs 252 at the centre, 127 midway, 8 just
inside the top edge and 0 outside, against 3 at the unscaled right edge. A
frozen circular gradient would have read about 178 at that edge.

## 5. WHAT IS NOT FIXED, AND IS A RECOMMENDATION RATHER THAN CODE

- **Defect 1 has no gate.** A mesh whose local axis disagrees with the line it
  was placed along is not decidable from the source in general, and the
  reconstruction that would gate it is a scene-graph invariant check the engine
  does not have a place for. The narrow version that IS available is the one the
  chassis now carries in prose at `akdrift.js:427`: the caller passes the LINE's
  yaw and the mesh turns by `yaw - 90`, in one place, with one helper. If this
  recurs, the fix is a chassis-level `placeAlong(line, mesh)` that no slide can
  bypass, not a check.
- **Defect 3 has no gate either, and should not get a cheap one.** A long
  straight luminance step ending inside the frame is exactly what a horizon, a
  datum rule and a section cut look like, and this house draws all three on
  purpose. A seam detector calibrated to catch the 150 m plane edge would fire on
  half the deck. The durable answer is the doctrine one (a plane is sized past
  the frustum or it is fogged into the sky), not a threshold.
- **Defect 5's structural repair is already in the slide** (the assertion now
  reads `stroke-width` back off the drawn element) and that pattern, READ THE
  NUMBER BACK OFF THE DOM, is the thing worth promoting into SLIDE_DOSSIER_SPEC
  next run.
