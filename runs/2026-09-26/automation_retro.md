# Automation retro, 2026-09-26 (No.69)

Phase 12, upgrade engineer. Inputs: out/2026-09-26/run_state.json, score_report_cycle1.json,
score_report.json, flow_review.json, render/machine_qa.json, WORKLOG.md, the showrunner's six
incident notes, and `python scripts/trend_check.py --window 10`.

## 1. Trend check and the top repeat offender

`trend_check --window 10` (2026-09-15 to 2026-09-26):

- Artwork craft and genuine detail: weakest in 8 of 10, mean 7.05, last 7.0, last worked
  2026-09-25 (the CRAFT FLOOR, one run ago).
- Deliverable completeness: weakest in 1 of 10, flagged STALE (never worked).
- Variety vs ledger: weakest in 1 of 10, flagged STALE (last worked 2026-08-15).
- Hard fails: none in the window. No defect class recurs in the final machine_qa.

**Decision: WORK ON the top offender, artwork craft.** This was the first run under the CRAFT FLOOR,
and it showed the floor's weakest point: the cycle it demands can make the art worse, and nothing
between the repair and the scorer would notice. The cycle moved art from 7 to 7, and the scorer's
one-sentence fix for cycle 2 was a defect the cycle had introduced itself: slide 08's lamp glow,
drawn on a 760 px layer, left a hard vertical edge at x 492 that was visible at thumb. So this run's
single upgrade is a check that catches that defect class at render time, while the repair is still
cheap. That is incident 2 below.

The two STALE rows are deferred. Each was weakest once in ten runs. Deliverable completeness was 7
here because of the caption and slide 09 asking different questions, which is copy and not
machinery. Neither pattern justifies a daily-cadence slot over an offender that has been weakest
8 of 10. Take them up when either is weakest in 3 or more of 10.

The deck-level half of the art problem is also deferred: brass rendered five ways and walnut three
ways across the deck (incident 1). What would have to be true to tackle it: a way to declare a
substance once, for example a `data-material="brass:<id>"` on each frame with a shared
`assets/js/` material table that akthree and aksdf both read, so a check could compare material
ids across frames. That is a cross-library material registry, which is a redesign, not a
bounded upgrade. The instinct the showrunner logged ("one material per substance across the
deck, fixed once") and the flow critic's deck-level craft block are the working controls until
then.

## 2. Deviations, phase by phase

| # | Phase | Deviation | Evidence | Class |
|---|---|---|---|---|
| 1 | Pixel review r1 to r4 | Every frame shipped against its own dossier while the deck carried brass in five materials and walnut in three. Only the flow critic's craft block and the scorer saw it. | score_report_cycle1.json artwork notes ("Walnut is rendered three different ways... Brass is five different materials"); flow_review.json cross_frame findings | Gate passed a defect a later reviewer caught (process: per-slide critics can't see deck-level material drift) |
| 2 | Scoring, CRAFT FLOOR cycle (round 5) | The craft repair on slide 08 introduced a regression: a dithered glow drawn on a 760 px offscreen canvas and composited in `screen` left a hard vertical edge at x 492 (and a tone step), visible at thumb. render, qa and every gate passed. The re-scorer found it, and the showrunner fixed it after the card by spanning the layer across the frame. | score_report.json weakest_criterion fix and artwork_weakest_frames[0]; post_score_fix; slide-08.html lines 170 to 185 | **Gate passed a defect a later reviewer caught. FIXED THIS PHASE (upgrade 1).** |
| 3 | Pixel review r4, qa | qa.py `marks_reach_frame` reads ink spread at each declared centre, so physically correct bokeh discs (smooth centre, hot rim) failed 30 of 88 until points were declared on each disc's rim. | instincts.json 2026-09-26 "A PROBE READS INK" | Gate behaviour that invites a workaround. Not a false fail to loosen: declaring the mark where it draws itself is the honest fix. Deferred; a docstring note is a later doc task, not today's slot. |
| 4 | Art build, slide 09 | aksdf raymarch at 1260 x 1575 needed bounding-sphere culling to fit render.py's hard 30 s renderReady timeout. An optional `rim` material scale was added to aksdf.js mid-run (committed c0f171ee, default unchanged). | run_state pixel_review r4 note; FIELD_NOTES 2026-09-26 retro ("21 s at 720 x 900 to 15 s at 1260 x 1575"); slide-09.html deadlineMs 27000 | Environment limit (time budget). Frontier scan targeted it; parked with measurements (section 4). |
| 5 | Art build, slide 07 | The AM halftone breaks into dashes and x marks where row pitch (from sy0) and dot size (from y) come from different coordinates. The generator lived in /tmp, so no committed helper could be fixed. | score_report.json artwork_weakest_frames (slide 7); flow_review craft slide 7 | Technique defect in uncommitted code. Deferred: nothing committed to repair. The honest control is a committed halftone helper, which is a build task for a deck that uses one. |
| 6 | Phase 3.6 gas watch | Live audit FAILED for about 2.5 h because GitHub dispatched the scheduled collector late. A manual `workflow_dispatch` through the GitHub MCP returned 403 (Resource not accessible by integration). It cleared at 09:44 UTC and cron_health refreshed PASS at 09:45Z. | WORKLOG gas watch rows; gaswatch_health_first.json against gaswatch_health.json | Environment breakage (GitHub scheduling plus integration permission). Off limits to editorial upgrades by rule. No incident file was needed because it cleared. Recommendation for the maintainer: if the routine is meant to be able to re-dispatch a late collector, the GitHub integration needs `actions: write`. That is a credentials decision and not this routine's. |
| 7 | Revision budget | The run reached the five-round cap (revision_rounds 5) with art still at 7, so the post-card fix to slide 08 was made after the last card. ship_gate passed correctly (the cap licenses shipping). | run_state revision_rounds 5; score_report post_score_fix | Process working as specified. Upgrade 1 moves this class of repair to before the card. |
| 8 | Workspace | The session branch was tsturg/zen-goodall-076n3j and not the routine's claude/carousel-<date>, as recorded in WORKLOG. | WORKLOG header | Session-designated, disclosed. No action. |

No install failures, no API limits and no fetch failures on the editorial path this run. Research
used 134 searches across six scouts without exhausting the budget.

## 3. Upgrades (1, reactive, targets the top offender)

**Upgrade 1 (fix, engine): A LIT LAYER WITH A LIVE EDGE.**

- render.py's GRADIENT_CLIP_HOOK_JS now also wraps `drawImage`. Every ADDITIVE (`screen`,
  `lighter`, `plus-lighter`, `lighten`, `color-dodge`) draw of a CANVAS source onto an on-page
  canvas records, for each destination edge that lands inside the target canvas, whether the
  source's outermost row or column still carries light: max over the border of
  max(r,g,b) x alpha x globalAlpha, with a record kept only at 0.01 or more. The record goes in
  design px, with its span along the edge, the op and the filter, in `render_report.json` as
  `lit_edges`. The border is read through a scratch canvas with the unwrapped drawImage, so the
  source is never touched and there is no recursion. The hook observes and forwards and never
  changes a drawn pixel.
- qa.py's `lit_edge_step()` confirms each record on the FINAL canvas layer (slide-NN.canvas.png,
  falling back to the full render). It takes the lit side's mean luminance minus the dark side's
  in a 3 design px band on each side of the line, skips 1 px of anti-aliasing, and smooths over
  5 design px along the edge. It then finds the longest consecutive run at a step of 1.0 levels
  or more. A run of 40 design px or more is a WARN that names the line, the step, the span and
  the one-line remedy (span the frame, or feather every in-frame edge to zero over 150 px or
  more). Something drawn later that covers the line makes the run vanish, so an occluded edge
  says nothing.
- WHY A WARN AND NOT A FAIL: it follows the precedent of the ellipse-clip check, where an author
  MAY want a hard edge of light. The routine already says to fix every warning you can't justify.
  Promoting it to a FAIL is the maintainer's call once the corpus has run clean. It is not
  weakened anywhere: no existing gate, threshold or rule changed.
- Why this shape and not a pure pixel scan: a scratch detector for long straight steps in smooth
  fields was built and run first on this run's nine canvas layers. It found the vertical seam in
  the reconstruction (x 246 at half scale = 492 css, 2.75 levels over 147 px). It also found 25
  legitimate HORIZONTAL straight steps across the nine shipped frames (table edges, 03's desk rows
  at up to 540 px, 09's horizon), which can't be told apart from a horizontal layer seam on
  pixels alone. The brush-side record supplies the one fact the pixels lack: a layer of light
  ENDED here. The pixel side supplies the one fact the brush lacks: it was not covered afterwards.

Verification:

- Defect reconstruction, this run's own slide 08 with the glow layer put back to 760 px at x 492:
  qa WARNs at x 492, 4.6 levels over 153 design px. A second reconstruction without the top
  feather also WARNs on the layer's top edge (6.3 levels over 588 px). Its bottom edge was
  recorded, but it lands on a row of page tops (12.3 levels for only 32 px) and stays quiet,
  which is the run-length floor doing its job.
- `tests/lit_edge_verify.py` (new, RED and GREEN fixtures through the real render.py and qa.py):
  HOLDS. The RED fixture WARNs once at x 492. The full-frame layer, the feathered layer, the
  occluded edge and the source-over panel are all silent. Its first draft caught a real seam in
  its own GREEN fixture, a full-width layer starting at y 340 with no feather, and the fixture
  was corrected.
- This run's 9 slides re-rendered with the new engine: pixel-identical to the shipped renders
  (max difference 0 on all 9), and machine_qa unchanged at WARN, 0 fails and 2 warns.
- examples/demo-deck, compared against a baseline rendered with HEAD's render.py and qa.py:
  pixel-identical, and machine_qa identical at WARN, 0 fails and 14 warns.
- 73 historical slides (runs 2026-09-05 to 2026-09-14, extracted from git at 8525cf40) rendered
  and QA'd with the new engine: zero lit-edge records and zero new warnings.
- Existing hook tests still HOLD: gradient_clip, empty_paint, ink_census_evict, overprint,
  reserve_punch, contact_probe, clip_reserve, mark_paints, motif_survives and light_direction.

## 4. Frontier scan, focus (e) headless Chromium rendering

This focus was legal and relevant. The last three foci were (c) on 09-25, (f) on 09-24 and (b) on
09-23, and (e) was last read on 09-19. It was chosen over the stalest slot, (d), because
incident 4 is a render time budget and (d) recorded itself as well mined on 09-17. The scan ran 4
searches and 4 fetches, plus one measured probe in the engine's own browser (HeadlessChrome 141,
4 cores) through render.launch_chromium, on one SDF scene (three smooth-unioned spheres and a
plane, 96 march steps, 32-step soft shadow) at 1260 x 1575:

- main-thread JS 3.9 s; the same kernel split across 4 blob-URL Web Workers 1.6 s, and
  BYTE-IDENTICAL to the main thread (0 of 1,984,500 pixels differ); a WebGL2 fragment shader on
  ANGLE/SwiftShader (Subzero) 0.6 s, mean difference 0.17 levels from the JS result.
- The same JS run through a direct `eval` inside the page took 53 s, which is 13 times slower. No
  committed asset or slide in this run uses eval or new Function (checked). If a future helper
  ever compiles scene code from strings, that is where a 30 s timeout comes from.
- HTML-in-Canvas (drawElementImage) is in origin trial for Chrome 148 to 150. This engine runs 141,
  so it is not available. That is a null result.

Outcome: PARKED in knowledge/FIELD_NOTES.md (2026-09-26 Phase 12 block), with the unblocking
condition. It is not applied because an aksdf worker or GLSL path is a new render route with its
own determinism proof, and the scene is a JS closure that a worker can't receive as-is. That is a
redesign and not a bounded fix. Sources: https://web.dev/articles/offscreen-canvas ,
https://swiftshader.googlesource.com/SwiftShader/+/HEAD/docs/Index.md ,
https://chromium.googlesource.com/chromium/src/+/main/docs/gpu/swiftshader.md ,
https://developer.chrome.com/blog/html-in-canvas-origin-trial

## 5. Recommendations for the maintainer (not done here)

- Consider promoting the lit-edge WARN to a FAIL after about ten runs with no false positive.
- The Gas Watch late dispatch: the routine can't re-dispatch a late collector because the GitHub
  integration lacks permission (403). Granting `actions: write` is a credentials decision.


## After review (showrunner, 13:25 UTC)

The lit-edge upgrade was WITHDRAWN before merge. Codex reviewed it eleven times on PR #402 and found new coverage gaps each round (clips, source bounds, filters, stacking, opacity, CSS transforms including reflection, late-appended and upscaled canvases, tainted readbacks, smoothing edge effects). A Phase 12 upgrade has to be bounded and verified; this one proved unbounded, so zero upgrades shipped. The last version (commit 3adf7a91) and the full list of findings are parked in knowledge/FIELD_NOTES.md as the specification for a dedicated maintenance PR. The aksdf `rim` material option (a run fix that slide 09 uses) stays.
