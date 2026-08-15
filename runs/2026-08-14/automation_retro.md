# AUTOMATION RETRO — run No. 33, 2026-08-14

Phase 12's analysis half, written by the showrunner. The upgrade-engineer takes
this as its incident notes.

## THE STANDING REPEAT OFFENDER, and what this run did with it

```
weakest  7/10  mean 6.0    last 6.0    Artwork craft and genuine detail   worked 2026-08-07 (4 runs ago)  <-- STALE
weakest  3/10  mean 5.95   last 6.0    Legibility and platform fitness    worked never  <-- STALE
```

The routine allows exactly two answers to the top repeat offender, work on it or
say plainly why it is being deferred again. **This run worked on it**, and did so
structurally rather than by trying harder.

What was done, in order:
1. plan.md named artwork craft as the one weakness this run was attacking and
   made three commitments before any art existed, a technique bench rather than a
   single technique, a drawn share above 65 percent, and the bottom band designed
   before the hero.
2. **Six prototypes were rendered through the real engine and gate-tested BEFORE
   the storyboard was written.** `qa.py` failed all four map compositions for
   top-loaded composition, at 0, 49, 38 and 0 percent of average bottom-third
   craft density, and passed the two that carried a worked lower band at zero
   fails and zero warns.
3. The winning treatment was chosen partly because its lower neatline margin
   makes the fix structural. A chart's marginalia is required by the form, so the
   band cannot be built empty.
4. Shipped result, `bespoke_check` PASS at 66 percent drawn share and 0.329 median
   pairwise similarity, and `qa.py` PASS with zero fails and zero warns on all
   nine, including zero top-loaded-composition warnings.

The prototype round is the transferable part and it is the upgrade candidate
below.

## DEVIATIONS FROM THE MASTER ROUTINE, with evidence

**1. The WebSearch budget was exhausted mid-run.** The six parallel scouts
consumed all 200 calls of a session-wide budget. Beats C, E and F all reported
hitting the ceiling and finished by fetching outlet indexes directly. The claims
phase then ran entirely on WebFetch, which worked, but the routine never told
anyone this budget exists or that it is shared across subagents. Two beats
reported lanes as UNSEARCHED rather than empty, which is honest and is also a
coverage hole nobody planned for.

**2. The caption assignment brief missed a standing burn.** The showrunner barred
only the previous run's closing move. The caption-critic then killed candidate A
because its price close had been burned on 2026-07-30 and restated on 2026-08-06,
and because its phrasing was the 2026-07-24 close with the nouns swapped. That is
the fifth occurrence of the same failure. The ledger holds the burn list; the
brief was written without reading it.

**3. A device string was silently truncated on five slides.** The projection note
was shortened purely to fit, which deleted the clause that made it an argument on
the one slide whose job was the argument. Two pixel-critics flagged it
independently and both called it systemic. Nothing in the pipeline compares a
rendered device string against the storyboard's declared state table.

**4. Two critics agreed on a measurement that was wrong.** Both reported the
deck's 48 px ring as inconsistent across slides. Every ring is
`cx.arc(x, y, 24, ...)` on a 2x context, proven by grep. They were measuring
anti-aliased stroke edges at three different weights. The deck's one declared
invariant had no machine assertion behind it, so the only available check was an
eye, and two eyes got it wrong in the same direction.

**5. A slide shipped into review drawing the inverse of its own thesis.**
Slide 06's 4x detail row magnified the states but not the rings, so small states
filled or overflowed their own awards. Every machine gate passed it. A critic
caught it by reading the picture.

**6. Render/patch ordering cost two silent no-ops.** Two projection-note fixes
were applied to source and then not re-rendered, because the following render
call named a different slide subset. The flow-critic read the stale contact sheet
and reported both as still broken. `--only` is a sharp tool and nothing warns
when an edited slide is not in the list.

## ENVIRONMENT

Bootstrap repaired a broken `pypdf` import automatically (a cryptography rust
binding panic) and reported it. Chromium fine. `alaskabeacon.com`,
`congress.gov`, `aws.state.ak.us` browse endpoints and several others returned
403 to WebFetch, which the scouts routed around and reported honestly.

## UPGRADE CANDIDATES, ranked

**A. Assert the deck's declared invariants (attacks the top repeat offender's
verification gap, and directly answers deviation 4).** A deck that declares a
constant should not rely on a critic's ruler. `window.__akAssert` already exists
and is used on two slides this run; the gap is that nothing encourages declaring
a REPEATED constant once and checking every instance.

**B. Compare rendered device strings against the storyboard's declared state
table (answers deviation 3).** The storyboard carries an explicit per-slide table
for the continuity devices. Nothing reads it. A check that diffs the declared
string against the rendered text node would have caught five slides at once.

**C. Warn when an edited slide is not in the `--only` set (answers deviation 6).**
render.py knows the mtime of every slide file and the mtime of every PNG it is
not rebuilding. A one-line warning would have saved two silent no-ops and one
misinformed critic round.

**D. Put the caption ledger's burn list in front of the assignment step (answers
deviation 2).** The information existed and was not read.

**E. Make the prototype round part of the routine.** This run invented it and it
found the standing weakness before the plan was written. It is currently a
showrunner improvisation with no home in the master prompt.

The upgrade-engineer picks from these under the usual bar, 0 to 3 bounded and
verified changes, reactive first, gates never weakened.

## ADDED AFTER SCORING, from the scorer's report card (8.45, ship, zero hard fails)

**7. A defect class no machine gate can currently see.** The scorer found three
annotation elements that ship without their terminal value, S01's leader running
off the Rhode Island ring into void, S07's dimension call printing none of the
values its own type spec declares, and S08's stamp leader descending into bare
sheet. The pixel round claimed to fix leaders on 01, 06 and 08 and only 06's was
actually fixed. `qa.py`'s leader check verifies that the leader's START lands on
its target and never that the far end carries a label, so the gate is structurally
blind to this. It pairs with candidate A, because both are cases where a declared
property had no assertion behind it.

**8. The run's own weakness target was set below its own recent performance.**
plan.md committed to a drawn share above 65 percent. No. 31 shipped 100 percent
and No. 32 shipped 99. The run then cleared its target by one point and recorded
that as the weakness being attacked. Nothing in the planning step reads the last
few artwork ledger entries for the measure being targeted, so a target can be
written that a pass would represent a regression. This is cheap to fix and it
falsifies the run's own self-assessment when it is not.

**9. The storyboard's device state table drifted from the shipped strings** on
S01 (ROT 154W dropped) and S03 (rewritten), which is candidate B measured from
the other end. The scorer found it by reading; nothing compared them.

**10. Two brand.yaml constellation fixtures went absent without a decision.**
Gold #FFC72C does not appear on slides 01 through 07 although brand.yaml says it
"appears deliberately on every slide", argued in the storyboard as a gold budget,
and S09's coordinates footer was removed during the pixel round to clear a margin.
Neither is a hard fail and both are per-run decisions made against a standing
spec, which is the kind of drift that becomes the new normal without anyone
choosing it.
