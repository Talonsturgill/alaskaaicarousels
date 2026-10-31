# Automation retro, run No.100 (2026-10-30)

The weekly machine pass is NOT due (`machine_due.py`: last pass 2026-10-25, five days ago, 40 items queued,
no repeat offender), so this run fixed only what broke in it and queued the rest.

## Trend (trend_check --window 10)

Top repeat offender: Artwork craft, the weakest criterion in 8 of the last 10 scored runs (mean 7.21),
last worked 2026-10-04. It is QUEUED for the weekly pass, not worked here, and that is the answer for this run.
What this run adds to that pass's evidence: the deck spent four pixel rounds and most of its art budget on
defects that shared helpers already solve elsewhere (cell-aligned DEM shading on 05 and 07, exponential fog
under an ortho camera on 01), so the strongest lever for the art criterion this week is reuse of the tested
terrain stack, not another gate.

## Deviations, phase by phase

- Phase 0: run_guard defaulted to the UTC date; passed `--run-date 2026-10-30` (Anchorage). Known behaviour.
- Phase 2/3: an alaska.edu page failed on its certificate chain and the r.jina.ai fallback is denied by the
  classifier; the docket note says the page could not be read. FERC eLibrary was read through its search API.
- Phase 3.6: Gas Watch live audit needed a production dispatch (run 41175507088) before it read PASS.
- Phase 7: `THREE.__aklCache` failed because THREE is a frozen module namespace (moved to `L.__cache`).
  01's first render was uniform haze: FogExp2 counts the ortho camera's 400 m stand-off. QUEUED (ortho fog item).
- Phase 8, four rounds:
  - 07 and 05: cell-aligned stripes and stair-steps from a hand-written smoothstep-bilinear DEM sampler (zero
    slope at every cell centre). Fixed with Catmull-Rom sampling plus a 1.2-cell Gaussian low-pass. QUEUED by
    raising the open "shared relief helpers" item to repeat 1.
  - 02: a cast band "fix" did nothing for a round because a Python edit appended code after a `//` comment on
    the same line. A showrunner slip, not a machine defect; a render diff check after each edit would catch it.
  - qa.py caught a painted light over a declared contact rect on 01 (the gate worked as designed).
- Phase 10: first score 8.11 (art 6.5); the craft cycle (round 5, the cap) on 07, 08, 02, 06, 04 and 03 took it to 8.165 (art 7.0). The 03 environment raise and the 08 sky resolution change read as no visible change to the re-scorer, so the cycle's gain came from 07's tone plate and drainage threads and 02's lit pool. Art stays under the 8.5 floor at the cap.

## Queued (knowledge/MACHINE_QUEUE.md)

- raised: shared relief helpers (repeat 1), with No.100 evidence.
- new: akladder/akthree ortho fog.
