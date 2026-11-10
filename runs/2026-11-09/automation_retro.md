# Automation retro, run 2026-11-09 (No.110)

Weekly machine pass NOT due (machine_due: last pass 2026-11-08, 1 day ago, due at 7; 57 queued, 0 repeat offenders). This run fixed what broke in it and queued the rest.

## Trend check (window 10), and what this run does with the top offender
Artwork craft was the weakest criterion in 5 of 10 runs (mean 7.15), and again here at 7.0. It is QUEUED for the weekly pass, not worked today, and here is why: today's art defects were frame-specific (an SDF petal form, stray meshes on 04, a flat plaque) apart from one shared-helper cause that was fixed in-run (the rail). The recurring deck-level cause on this run is new: a shared rail band repeated across eight frames that the flow critic called an eventless lower band (cause c). The weekly pass should take it up only if a second deck shows it.

## Deviations, with evidence
1. Pixel review took four rounds plus a sequence round, which reached the five-round cap. Round 1 scored 5.0 to 7.0 and every frame revised. The shared rail carried two defects onto all eight frames: the lip's brushed lay ran across the lip, and pockets under 4 px aliased. One fix in akweb.js cleared both.
2. assemble.py raced renderReady against a fixed 30 s. Slide 05's raymarch takes about 95 s, so the deck silently fell to a raster PDF. FIXED IN RUN: assemble.py takes `--timeout` (commit fix(2026-11-09)).
3. The comb softening added in the sequence round made stepped seams on 09, which the re-review caught. Fixed with a smoothed per-column weight and an end lip.
4. Slide 05's torn-petal SDF failed three rebuilds and ships as a logged holdout at 7.1.
5. The routine text contradicts itself on the cap. Phase 8 step 3 says "max 4 rounds", while Phase 10 and ship_gate count a five-round cap that includes the flow round. This run used 4 plus 1.
6. Phase 3.5 pre-flight hit three gates on one new docket item: a missing agency rule (added), "Statewide" refused as a location (dropped), and the ask pack ceiling. The pack measured 32,085 tokens against 32,000, and the item had to be trimmed. Inline payload headroom is now 1,327 bytes, under the 5,000 the routine asks to report.
7. Scouts were handed the ALREADY COVERED block as a file to Read rather than pasted (20.7 KB). All six reported already_covered_read true. Worth writing into the routine.
8. The caption room needed one rewrite round. Both first candidates were rejected (spent pairs, an overstatement of C17, a burned hashtag).
9. A curl call with a custom User-Agent was refused by the harness classifier. WebFetch worked.

## Queued (knowledge/MACHINE_QUEUE.md)
- ask pack ceiling crossed by one new docket item (2026-11-09)
- routine text: the round cap contradiction (Phase 8 says 4, the gates count 5)
- aksdf: no safe primitive for a bent sheet; ad hoc bent-space distances terrace and alias
- akthree: promote the shadow catcher (blurred-texture cast plane) into AKT so flat objects ground without per-slide code
- scout brief: hand ALREADY COVERED as a file path, not a paste
