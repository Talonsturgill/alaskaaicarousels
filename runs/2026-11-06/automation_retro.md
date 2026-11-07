# Automation retro, 2026-11-06, No.107

Weekly machine pass: NOT due (machine_due: last pass 2026-11-01, five days ago, due at seven; 56 items queued, 0 repeat offenders before this run). This run fixed what broke in it and queued the rest.

## Trend report's top repeat offender
Artwork craft and genuine detail, weakest in 4 of the last 10 runs, mean 7.25, last worked 2026-10-04. Deferred to the weekly pass, which is due on 2026-11-08. This run's evidence for it: art scored 7 again, and the frames the scorer named (02, 06, 08, 03, 09) share one cause, the largest object left as a flat fill (strands, table, relief) while the land around it is modelled. What would let a run tackle it: a craft budget that is not consumed by texture artifacts. Four of this run's five editing rounds went to artifacts (globe streaks, plate stains, island fog) rather than to modelling the largest objects.

## Deviations, phase by phase
- Phase 3.6: the Gas Watch audit was WARN late_post (CINGSA posted 05:29Z after the 23:44Z collection). Dispatched gaswatch.yml on main, which collected 7.73 Bcf, deployed, and the re-audit passed. No code change.
- Phase 7 and 8: a new shared module (assets/js/akglobe.js) shipped with two latent noise bugs (a float-overflow hash and a noise space sheared by lon x cos(lat) far from the prime meridian) and a shadow-acne setting. Pixel critics named the resulting streaks on 01, 05 and 09 for three rounds before a texture debug page found the cause. Fixed at the source this run (commit 8db94c6f and the run commit), logged as technique 149 and in FIELD_NOTES.
- Phase 8: the site fixture collided with drawn land on five frames. Three fixes were called stains before the keep-under (restore the pre-coast pixels in a feathered ellipse) and moving the art read clean. Queued as a qa check.
- Phase 8: a corner vignette on 04 dimmed two of 146 declared threads under qa's mark census; it was removed. The census caught it, as designed.
- Phase 10: the scorer flagged again that the rubric weights sum to 1.10. Raised the repeat count of the existing OWNER DECISION item; not changed by a run.
- Phase 11: ship_images reached only 3.5x on grain-heavy frames (17.4 MB). Queued. shrink_pdfs declined at 0 percent, the correct outcome.
- Tooling friction, no defect: gate_status --sync takes the storyboard path as its argument.

## Queued this run
Three new items (fixture-zone qa check, distinct cameras for globe frames, ship_images on grain-heavy decks) and two repeat bumps (akpost grain lattice, rubric weights).
