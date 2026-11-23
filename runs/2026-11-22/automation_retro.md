# Automation retro, run 2026-11-22, Carousel No.122

## Standing weakness (trend_check --window 10)
Artwork craft and genuine detail: weakest in 8 of the last 10 scored runs, mean 7.05, last 6.5, last worked 2026-11-11 (STALE). The weekly machine pass is not due today (last pass 2026-11-17, due at 7 days), so the offender is queued for that pass rather than worked here; that is the answer this phase owes. What would have to be true to tackle it in the pass: the week digest's craft causes (largest object least modelled, texture artifacts) counted across No.118 to No.124, and a measurable change to a shared idiom rather than one deck's slide code. This run attacked it inside the deck: the CRAFT PLAN named every largest object's modelling, the masterful depth frame (08) was built first, every object stands on a lit ground, and the shared core module took three material rounds.

## Deviations, phase by phase, with evidence
- **Wake.** CLAUDE_EFFORT read `medium` although .claude/settings.json carries `high` (same reading as No.121). Noted in plan.md and in the email's editor notes. Not fixable from a run.
- **Research.** All six scouts reported a thin window and used 24 to 25 searches each (149 of 200). The story came from a 15-month-old primary document plus an in-window appointment; the fact-checker used 17 WebFetch calls (8 distinct URLs succeeded, 1 justified repeat of the AO 359 page whose first response was summarised rather than quoted). Showrunner fetches: the AO 359 page and the ADN piece by curl (both quoted verbatim into S-claims), omb.alaska.gov twice (503 both times).
- **Docket.** The staleness worklist deferred 7 items past the budget of 6 for the second day running, so the budget was raised to cover all 13 (rule: raise the budget rather than let the tail rot). The AEA CIPLink page returned 503 and its note says so. No item changed.
- **Gas Watch.** gaswatch_health WARN at wake (late_post: CINGSA reposted its November 22nd reading at 04:47Z after the 00:20Z collection). Dispatched gaswatch.yml on main (run 45122407452, success); the Pages deploy then sat in its token-blip retry wait for several minutes before publishing; re-audit PASS. The remedy text was right and took one dispatch.
- **Art build.** Five defects cost renders before any critic saw the deck: (1) every `__akLeaders.label` was written as a selector instead of the label's text, which qa.py FAILed on 7 slides; (2) the AKPOST.grade call on 08 ran under an identity transform (console contract error, fixed with setTransform(2,...)); (3) radial gradients built in untransformed coordinates and painted under cx.scale() put the lit pools on 03 and 04 off frame for a whole pixel round (queued); (4) a hand-typed Bayer matrix was indexed by cell position rather than looked up, printing scanlines on 05; (5) aggregate_check parsed "AO 359 stays" as a count, so 08's body was reworded (queued).
- **Pixel review.** Round 1 sent all nine back; the common cause was one shared idiom (the core read as PVC pipe), fixed once in assets/js/akcore.js (transmissive ice with interior bubbles, softer irregular strata). Round 2 shipped 05 and 06. The flow critic named the cradle (a black rail) as the strongest pipeline cue across 01, 08 and 09, again fixed once in the module.
- **Caption room.** Two directors and a critic; A won with one fix to the deck summary line. caption_check PASS at 879 characters.

## Machine changes queued (knowledge/MACHINE_QUEUE.md)
- New: gradient centre under a scale transform (qa/authoring), a committed 9:16 story frame helper (social), order numbers as identifiers in aggregate_check.
- Raised: the site fixture contrast item to repeat 2 (critics named alaskaaihq.com at about 3:1 on 05, 06 and 07), which makes the weekly pass due tomorrow.

## Fixed in this run
- New house module assets/js/akcore.js (the dated ice core, the lit freezer table and a modelled caliper), used by three frames; its own TECHNIQUE_LIBRARY entry is written at ship.

## Upgrades
No upgrades: the weekly pass is not due (machine_due.py exit 1); 81 items queued.
