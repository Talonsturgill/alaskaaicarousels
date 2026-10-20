# Automation retro, run No.90 (2026-10-19)

The weekly machine pass is not due (machine_due.py: last pass 2026-10-17, due at 7 days; no queued item at repeat 2). This run fixed what broke in it and queued the rest.

## Top repeat offender (trend_check --window 10)
Artwork craft and genuine detail, weakest in 7 of the last 10 runs, mean 7.03. This run's artwork went 7.0 to 7.5 with the craft cycle. It is QUEUED for the weekly pass (due 2026-10-24), which owns recurring themes; the evidence this run adds: the largest object read as least modelled on 02 and 06 until rounds 2 and 4; a texture artifact (crossline triangles on 03, sphere seam creases on 08, stepped arris on 01, knockout boxes on 06) named in every round; the kerf read as a decal until its light came from inside the cut. Tackling it needs the weekly digest, not one run's guess.

## Deviations, phase by phase
- Phase 0: bootstrap's Pillow C core was broken (Debian dist-packages PIL), so site_build failed with "no grain texture". FIXED IN RUN: reinstalled with pip --ignore-installed and added a probe to bootstrap.sh (commit 637af960).
- Phase 3.6: gaswatch.yml dispatch returned 403 "Resource not accessible by integration" (known). The 19:20Z slot ran at 22:55Z, before the source's evening reading; the 04:40Z slot started about 09:40Z. The live audit then passed at 09:42Z, so no incident was filed. cron_health PASS at 06:15Z.
- Phase 6: caption round 1 returned "neither"; one rewrite passed. The copywriter caught an accuracy drift ("Alaska uses about 70" overstated C36, in-state demand) and a missing "roughly" on C38; both fixed before render.
- Phase 7: qa FAILed the cover's fitText (min authored above what the 560 px box could hold); dossier_check FAILed undeclared contacts on 01 and 09 and a technique-name drift on 04; plan_drift and aggregate needed declarations. All fixed at the source.
- Phase 8: five pixel rounds (four edit rounds plus the craft cycle). Round 1 sent all nine frames back. Two flow-critic rounds; the first restructured 03's body to plant the deed dispute. The critic for 01 and 02 caught the kerf reading as a ribbon; the scorer caught 08's grains reading as clay.
- Phase 8: dropping a separator dot before a display:block span FAILed qa's leader check (textContent fused the words). Worked around by keeping a space; QUEUED (qa leaders).
- Phase 8: critics repeatedly could not open the 432 px thumbs because critic_brief never names them (assemble writes slide-NN-thumb.png). QUEUED (critic_brief).
- Phase 8: a brief inverted akengrave's tone direction; the fixer caught it. QUEUED (akengrave docs).
- Phase 10: the craft cycle regressed 06 (a text box); the pre-cycle version was kept and the scorer re-judged artwork with it (7.5).
- Phase 11: main's docs had been rebuilt by the gas watch cron at 2026-10-20 during the run, so the site was built at 2026-10-20 per the rule (never earlier than main). docket_alerts sent one subscriber email (KPB weather modification code, deadline tomorrow).

## Queued in knowledge/MACHINE_QUEUE.md
1. critic_brief: print the thumb path.
2. qa leaders: match labels on innerText.
3. akengrave docs: one line on tone direction.

No upgrade commit this run; the pass is weekly.
