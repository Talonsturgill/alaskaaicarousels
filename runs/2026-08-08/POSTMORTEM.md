# POST-MORTEM — Run 2026-08-08 — Carousel No. 29 — NO DECK SHIPPED

## VERDICT

The run did not produce a deck. It produced a complete, gated plan and three of
nine slides, then stopped because the showrunner's context budget was spent.
**Nothing was merged to main.** The branch `claude/carousel-2026-08-08` carries
the evidence and the PR stays open, per the delivery policy for a failed run.

This was a deliberate stop, not a crash. Non-negotiable 6 says to degrade
gracefully and say so, and never to silently ship garbage. Six slides written in
whatever budget remained, with no pixel critics, no flow critic and no scorer,
would have been garbage with a run number on it.

## WHAT ACTUALLY WENT WRONG

**The failure is one of allocation, not of any phase.** Every phase that ran,
passed. The showrunner spent its budget on research breadth and planning depth
and had nothing left for production, which is the expensive half.

Concretely, where it went:

1. **Six scouts returned about 490,000 tokens of findings between them**, and
   four of the six led with the same story, which was already ruled out on
   dedupe before the sweep finished. The convergence was real editorial signal
   and it was also four beats of redundant work. Beat B and Beat E carried the
   run; the other four could have been two.
2. **Three treatment-directors returned about 224,000 tokens**, all three
   excellent, all three complete decks. The synthesis used one chassis and two
   grafts. That is the room working as designed, and it is also two full decks
   of planning thrown away at a cost the run could not afford.
3. **The storyboard is about 1,000 lines.** It is the best artifact this run
   produced and it is worth every line, but it was written by the same context
   that then had to write nine slides.

## WHAT SURVIVED AND IS WORTH KEEPING

This run is not a loss. Five things are committed and real:

1. **A Gas Watch bug found and fixed.** Phase 3.6's daily read caught the live
   page publishing "134.1 percent of the region's gas arriving from sources no
   public feed reports daily". A share of the region's gas caps at one hundred
   percent, so the page was asserting something impossible. The number was
   right and the noun was wrong: it is a ratio to MODELED DEMAND, and on a
   summer injection day the residual necessarily exceeds demand. It would have
   read correctly all winter and wrongly all summer. Fixed in presentation only,
   with the explaining clause now computed from the sign of the measured
   withdrawal. Self-test clean. **This alone justifies the run.**
2. **The docket refreshed**, four items re-verified against primaries, one
   material change recorded on the AKLNG session.
3. **38 verified claims, claims_check PASS, 18 primary**, with seven claims
   killed and the reasoning recorded. The fact-checker caught the run about to
   write that a $200,000 installation grant funds the weir, which would have
   directly contradicted the central quote.
4. **A 9-slide storyboard that passes dossier_check 9 of 9**, with worked camera
   arithmetic and a genuinely novel device.
5. **A validated aksdf hero scene** that renders in 10 to 12 seconds and
   produces real craft, plus two engineering findings recorded in NEXT_RUN.md
   so they are never rediscovered.

## THE ONE THING THAT WAS ATTACKED AND THE HONEST SCORE ON IT

The run's declared target was artwork craft, weakest in 7 of the last 10 runs,
and specifically **RENDERED LADDER DECLARED AND NOT REACHED**, four decks in six.

**Partial credit, and it is worth being precise about which part.**

The ladder WAS reached. Three slides are genuinely raymarched, not a Canvas 2D
fallback wearing a dossier claim, and the structural reason the plan gave holds
up: aksdf has no GL context to fail, so there was no fallback to slide into. The
frames have real cast shadows, a real lit ground and a real lit aperture.

The EVIDENCE CONTRACT failed, and it failed in an instructive way. The plan
required luminance probes proving the 05 and 06 separation. The probe rectangles
were authored from the storyboard's PREDICTED screen coordinates rather than
measured off a render, so they landed off the aperture, and the measured
separation came out backwards, with slide 06 reading brighter than slide 05.

That is the same defect class this run set out to kill, one level up. The old
failure was asserting a rung without checking it. The new failure is building a
check and not verifying the check points at the thing. **A gate authored from a
prediction is not a gate.** Measure the region off a real render, then write the
rectangle. This belongs in FIELD_NOTES and in NEXT_RUN.md, and it is recorded in
both.

## WHAT THE NEXT RUN SHOULD DO DIFFERENTLY

1. **Take the queued brief.** Almost all the expensive work is done. The next
   run starts at slide production with a passed storyboard and passed claims.
2. **Budget production before planning.** The planning phases are cheap to make
   luxurious and expensive to pay for. If the storyboard is complete and gated,
   the remaining budget belongs to slides and critics.
3. **Six scouts is the wrong number when four of them converge.** Nothing in the
   routine allows fewer, so this is a note for Phase 12 rather than an action:
   consider whether beats that return the same lead should be collapsed.
4. **Measure a probe region off a render before writing it into a slide.**

## WHAT WAS NOT DONE, STATED PLAINLY

No slides 02, 03, 04, 07, 08, 09. No assemble, so no PDF, no contact sheet, no
thumbs. No pixel critics. No flow critic. No aggregates declaration. No scorer
and no score report. No site rebuild. No merge to main. No subscriber alerts.
No Phase 12 upgrade pass. The caption room ran and its verdict is recorded.
