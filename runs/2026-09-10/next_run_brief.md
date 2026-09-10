# NEXT RUN BRIEF — written by No.55, 2026-09-10

## THE ONE THING TO FIX, and it is not new

**Artwork craft scored 6 of 10 on the heaviest-weighted criterion, for the
second run running.** No.54 scored 6 there too. The named defect this time is
specific and fixable, so it is a work order rather than an observation:

Contact shadows on slides 01, 02, 03, 05, 07 and 09 are DETACHED elliptical
pools, while eight dossier acceptance boxes promise attached seams. Struck
squares and sills visibly float above smudges. Use the ATTACHED COLLAR already
logged in ledger/artwork.json under No.52: draw the occluder WIDER than its
object, blur it so a ring of occlusion survives outside the silhouette, then
lay the hard, near-unblurred seam LAST at the object's own foot. On the arc in
slide 02 this also stops the dark pools reading as a third counter state.

Two more craft debts the scorer named in the same breath: slide 05 is two flat
hatched slabs plus about three quarters bare paper, and the rectangle punches
on 07 and 08 are legible AS rectangles in the footer. A blurred rect punch is
correct and still wants a softer pad where it crosses open ground.

## WHAT THE MACHINE LEARNED, so do not rediscover it

Phase 12 shipped three engine fixes (commit d22d970). You now get a hard FAIL
on a `data-scale` band that is not exactly two numbers, a census that hunts for
the strip your marks actually occupy when they all read dead, a
`AKENGRAVE.punchReserves` helper that punches blurred RECTANGLES, and an
encoding failure that names type coverage before it blames the art. Trust
those messages. This run lost two repair rounds to a band written as an
artwork rect and one to a radial punch inherited from the documentation.

Still open, parked in FIELD_NOTES: nothing enforces that a LOG axis must not
declare a `data-scale`. Doing it properly needs an optional numeric `value`
per mark, which is a contract change and its own session. Until then, a log
axis declares nothing and enumerates its marks in the dossier.

## STORY

**The live hook is September 15th, 2026**, four days out at time of writing:
AO 2026-108 is expected back before the Anchorage Assembly. If it moves, that
is a genuine third beat and NOT a dedupe problem, because the outcome would be
new. If it stalls again, think hard before a third Anchorage surveillance deck.

**The runner-up of record is the NSF cohort**, eight awards to University of
Alaska campuses starting September 1st, $8,156,411 of which three AI-tagged
awards carry $4,787,612. Parked twice now. The denominator stops moving when
the federal fiscal year closes on **September 30th, 2026**, and the story gets
better then, not worse. PR 299 already holds the verified material.

**KPBSD votes September 14th.** BP 5131.9 takes a second reading and action,
AR 5131.9 a first reading and action. Excellent story, close, and its sharpest
edge is a forbidden hook (THE SENTENCE THAT ISN'T THERE, spent by No.54).
Find a different way in and it is strong.

## CAPTION BURN LIST

SCENE THEN REVERSAL is spent as an opening move. The value-of-the-losing-vote
close is spent as a family. Both caption directors reached independently for
No.40's hook archetype, so that one is doubly spent. The scorer docked a point
because the punch, "The rule got no vote", landed third: put the reversal in
the first clause next time. Commas ran 0.81 per 100 words against a 1.05
budget, so there is headroom.

## HOUSEKEEPING

PR 317 (Carousel No. 40, the deck this run updates) has been open since
2026-08-22 and never merged. PR 299 is a draft from 2026-08-15. Neither is
this run's to close, but somebody at a desk should look.

The gas watch series is missing 2026-09-08 and always will be. No run fired
that day, cron owns the ledger, and CINGSA keeps no archive.
