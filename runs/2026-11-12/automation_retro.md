# Automation retro, 2026-11-12, No.113

## Trend check (window 10)
Artwork craft is the top repeat offender again: weakest on 7 of 10, mean 7.1, last worked 2026-11-11 by the weekly pass. Today it was the weakest at 6.5 before the CRAFT FLOOR cycle and 7 after it. It is not worked today: the weekly pass ran yesterday (machine_due exit 1, next due 2026-11-18) and the offender is queued for it with today's evidence. What would let it move: the flow critic and scorer named the same three causes on this deck (the lower face reads as rippled water with closed contour loops, the largest object under-modelled at thumb on 07 and 01, jamb strips reading as texture bands), which is the week's craft causes again.

## Deviations, phase by phase
- Research and claims: only the lead story survived the claims gate; the runners-up died under the single-source rule. The sweep was not re-run at 21 days (recorded in selection.md).
- Gas watch and cron: gaswatch.yml run 612 has sat queued at GitHub since 2026-11-11T20:43Z with no job; cancel refused HTTP 409 twice. Runs 613 to 620 all succeeded and the live page matches main. Kept as a github-blocker incident (cron_incidents.json, re-stamped to the 2026-11-13T08:24Z audit). The gas watch late post was repaired in-run by dispatching run 620.
- Art build: AKT.lathe silently produced NaN geometry when given Vector2 points (it takes [r, y] arrays). Logged in FIELD_NOTES.
- Review: five rounds used, the cap. Round 3 was the flow critic's work order; round 4 the CRAFT FLOOR cycle (art 6.5 to 7); round 5 a single regression fix (the round 4 ebony lift read as brass).
- QA: slide 05 FAILed the axis census for an undeclared mark at 987.5 that was the rule's own end shading. Cause: the declared gold sliver end carried no luminance against ivory, so the threshold fell to texture. Two edits aimed at the reported location changed nothing. Fixed by an etched dark cut at the sliver end. Queued: raises the 2026-10-04 census item to repeat 1.
- Scoring: the scorer caught a first-comment URL whose slug named a governor's race candidate as leading; no gate reads slugs. Fixed in-run by re-sourcing C50 to the Alaska Constitution. Queued as a new item.
- Scoring: the rubric weights still sum to 1.10 (8.355 literal, 7.60 normalised against 7.7). Already escalated to the owner; repeat raised to 4.
- Plan drift: two FAILs after round 3 copy cuts (C17, C25 indexed to slides that no longer printed them); fixed by regenerating the CLAIMS INDEX from copy.json.

## Queue
63 items were queued before today; one new item added (URL slug guard) and two repeats raised (axis census weak-mark threshold, rubric weight sum). The machine is upgraded weekly; no upgrade commit today.
