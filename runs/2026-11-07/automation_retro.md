# Automation retro, run 2026-11-07, No.108

## Weekly pass
Not due. `machine_due.py`: last pass 2026-11-01, six days ago, due at seven. 61 items are queued and none is an unescalated repeat offender. No upgrades this run. Three new items were queued, one item was raised, and one duplicate was folded (below).

## Trend check (window 10), and the top repeat offender
Artwork craft and genuine detail was the weakest criterion in 5 of 10 runs, with a mean of 7.1. It was last worked on 2026-10-04 and is marked STALE. This run is another instance: art scored 7, and the one craft cycle left it at 7. **Deferred to the weekly pass due 2026-11-08, not dropped.** This run's evidence for that pass:
- The three frames that held the art score down all used a renderer feature this run had to work around by hand:
  - akthree ground patches seam and saw-tooth (01, 09)
  - corrugation reads as a barcode under grazing light (01, 09)
  - aksdf has no ambient term, so a covered interior is a void (04)
- Two of those are now queued as library fixes (AKT.groundPatch, an aksdf ambient term). Tackling the criterion means fixing renderer defaults so a run doesn't spend three pixel rounds rediscovering them.

## Deviations, phase by phase
- **Phase 3.6, Gas Watch live:** FAILED on a late post. Repaired the same run: gaswatch.yml dispatched on main (run 42453689744), then Pages (42453842175), then a re-audit PASS. No incident file needed.
- **Phase 7, art build:**
  - akthree's default camera far plane (200) clipped the feet-scaled world on 01 until far was set to 4000. AKT.audit's far_clip WARN exists; the frame was fixed before qa ran.
  - Labels landing in margins, and knockout plates, needed three passes.
- **Phase 8, pixel review (four rounds, the cap):**
  - Round 1: all nine revise.
  - Round 3: one critic (07, 08) handed back only the word "placeholder". Matching slide numbers caught it and a fresh critic reviewed both in the same round. Queued as a hand-back parser.
  - After round 4, 01, 04 and 09 were holdouts.
  - The rut saw-tooth took two rounds to diagnose. It was mesh interpenetration, not shadow aliasing.
  - The 09 seam took three more rounds: a fine-only fbm term at the patch edge, fixed only when the edge left the frame.
- **Flow critic:**
  - Caught a real unit error on 03. "SQ FT OF FLOOR AREA" sat under numerals 0 to 60 and had passed four pixel rounds and every gate.
  - Caught 07's shell being off-scale against 02 and 04.
  - Declined, on geometry: its reading that 06's stripe runs parallel to the racks (the rack rows end on it, perpendicular).
- **Phase 10, scoring:**
  - 8.44 by the rubric's literal formula, 7.67 normalised. The weight sum of 1.10 is the standing escalated owner decision.
  - Its duplicate entry from 2026-11-04 was folded into the escalated item, so the repeat count no longer forces a pass.
- **Tooling:**
  - `caption_check.py --copy` without a caption path blocked on stdin inside a chained command (300 s, stopped).
  - Redirecting its stdout to caption_report.json then clobbered the report. It was regenerated with the documented invocation.
  - The existing queue item was raised to repeat 1.
- **Environment:** none. Renders were stable: the GPU frames took 25 to 38 s, and the aksdf frame at 2160 x 2700 took 37 s with no degrade.

## Queued this run (knowledge/MACHINE_QUEUE.md)
- NEW: aksdf ambient or bounce term for covered volumes.
- NEW: a parser for subagent hand-backs (verdict JSON plus assigned slide numbers).
- NEW: AKT.groundPatch, the two-resolution ground with sink, edge fade and an in-frame edge warning.
- RAISED: caption_check stdin hang (repeat 1).
- FOLDED: the rubric weight-sum duplicate, into the escalated owner item (repeat 3).

## Upgrades
No upgrades.
