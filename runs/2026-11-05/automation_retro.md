# Automation retro, 2026-11-05 (No.106)

Weekly machine pass: NOT due today (`machine_due.py`: last pass 2026-11-01, four days ago, due at seven;
56 items queued, 0 repeat offenders after this run closed the bootstrap item). Steps 2 to 4 of the weekly
pass do not run; the in-run fixes below are breakage repairs under the FAILURE PROTOCOL.

## Top repeat offender (trend_check --window 10)
Artwork craft, weakest on 5 of 10, mean 7.15, last worked 2026-10-04 by text match. Not worked today
beyond this deck's own craft cycles; it is QUEUED for the weekly pass due 2026-11-08, which reads the
week's digest. What would have to be true to tackle it: the digest naming one recurring craft cause across
most of the week's decks, so the fix lands at its root (a helper or a gate) and not on one frame.

## Deviations, phase by phase
- Wake: the bootstrap pip install of an unpinned python playwright hung and was killed; pinned by hand to
  1.63.0 to match the node playwright and the image's chromium-1243. Third run bitten (No.103, No.105,
  No.106). FIXED IN RUN: bootstrap.sh pins python playwright to `playwright --version` (upgrade commit,
  ledger/upgrades.json entry, MACHINE_QUEUE item closed).
- Phase 3.6: the Gas Watch page posted late; a production dispatch and a Pages wait resolved it, audit
  PASS on re-run. No code change.
- Phase 4: muni.org returned 404 for every Assembly page and PDF, so the as-amended text is unread and
  the deck carries the substitute as filed, labelled so. Single outlet for the vote tallies (attributed).
- Phase 7: render.py `--only-exact` is a flag, not a value (usage slip, no change); aksdf needs
  `setTransform(2, ...)` before `render` or it draws into a quarter frame (documented already).
- Phase 8: round 2 critics found three engine-level causes, each fixed at its root for this deck:
  akthree's PCFSoft shadow map ignores `shadow.radius`, so a soft cast needs VSM (two slides drew a hard
  slab); akletter's 18-segment joint spheres poked through its cylinders as dotted seams (helper now 32
  radial segments, open cylinders); aksdf's two-material stripe figure aliased into hard stripes (figure
  drawn in 2D over one material instead).
- QUEUED for the weekly pass: akthree could expose a `softShadows` option that switches to VSM when a
  slide asks for a radius, since a radius that silently does nothing is a trap (evidence: No.106 slides
  01 and 09, round 2).
