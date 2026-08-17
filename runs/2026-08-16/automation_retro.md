# AUTOMATION RETRO — run No.35, 2026-08-16

Written by the upgrade-engineer (Phase 12) after the merge, before the Gmail
draft. Scope: the MACHINE. The editorial retro (Phase 14) owns the content brain.

## 0. THE STANDING REPEAT OFFENDER (trend_check --window 10)

```
weakest  8/10  mean 6.1  last 6.0  Artwork craft and genuine detail  worked 2026-08-07 (6 runs ago)  <-- STALE
weakest  2/10  mean 6.15 last 7.0  Legibility and platform fitness   worked never                    <-- STALE
```

DECISION: worked, and stated plainly rather than claimed. The frontier scan slot
was spent on procedural art precisely because that is where this offender lives
(see section 2), and it returned nothing new: the one live candidate, streamline
placement for akhachure, remains parked because neither substantive source
publishes parameters. So the offender got the scan and not an upgrade this run.
What would have to be true to tackle it: a readable implementation of evenly
spaced streamline placement, or a trial slide judged at 432px against the
existing hachure field. Both are corpus/trial work, not an end-of-run slot.

The three upgrades below are all reactive, and reactive fixes outrank a frontier
improvement by this phase's own rule. Two of them (the axis census, the probe
scale) are artwork-integrity machinery, which is adjacent to the offender
without being a claim to have moved it.

## 1. DEVIATIONS, phase by phase, with evidence

run_state.json shows phases 0 through 9 done, flow review in progress, scoring
and ship pending at the time of writing. No phase was skipped, no degraded
fallback was taken, no environment breakage was recorded in the run state, and
qa.py returned PASS at 0 fails / 0 warns on the shipped nine. The deviations are
therefore all of one kind: DEFECTS THAT PASSED EVERY GATE and were caught by a
human reader (pixel critics, the caption critic), plus process gaps that cost
render cycles.

D1. A DECORATIVE MARK ON A QUANTITATIVE AXIS READ AS A QUANTITY, twice.
    Slide 07: three gold place ticks under a rail whose x means DOLLARS, so
    three REGIONS were printed at three dollar positions. Slide 02: thirteen
    blue division ticks on a money rail, implying twelve equal months across a
    budget period that runs ten. Both passed render, qa, bespoke_check and the
    first pixel round. Caught by a pixel critic reading the picture.
    STATUS: FIXED IN THE MACHINE (upgrade 3).

D2. WHEN A REGION IS SMALL RELATIVE TO THE FRAME, THE SAMPLER IS THE BUG.
    akstipple rejection-samples over the whole 1080x1350 frame, so an 11px band
    wins about 0.06 percent of throws; slide 03 drew "19 funded of 1,800" as
    literally nothing and slide 07's Aleutian arc came out bare, and both read
    as art decisions rather than as failures.
    STATUS: fixed in-run by the showrunner (optional sampling box, 33c4111 /
    4298da6). Out of scope here by the run's fence; no further machine work.

D3. A LIGHTING DEVICE THAT RANK-ORDERS THE DATA IS AN ENCODING. Slide 06's
    descending height stair put Spearman 1.00 between block height and award
    amount forty pixels above a printed line reading HEIGHT ENCODES NOTHING.
    STATUS: knowledge only (FIELD_NOTES 2026-08-16). Nothing mechanical can see
    an accidental correlation between a composition decision and a data order;
    the defence is procedural (shuffle the decorative dimension against the data
    order, or hold it constant).

D4. A CONSTRUCTION DELETED FOR READING BADLY WAS DELETED IN ONE PLACE ONLY.
    The stroke-over-a-dot that read as an exclamation mark went from slide 07's
    place ticks and stayed, at 2.5x the height, as the gold terminus on five
    other slides.
    STATUS: knowledge only (FIELD_NOTES 2026-08-16). Considered and rejected as
    a gate: a cross-slide "same construction" detector needs a shape vocabulary
    the engine does not have, and guessing one would fire on legitimate house
    furniture.

D5. THREE CRITICS EACH PROPOSED A PER-ELEMENT WORKAROUND FOR ONE LIBRARY BUG
    (getBoundingClientRect returning the LAYOUT box, so reserve rectangles
    floated). One fix retired every proposed workaround.
    STATUS: fixed in-run in assets (fenced). The durable lesson is a reviewing
    one: three independent reports of the same visual symptom are evidence of a
    shared cause, and the round should look for it before spending three fixes.

D6. PROBES ARE AUTHORED IN DESIGN PX AND MEASURED AT 432px. Four probes failed
    for that reason alone this run, each costing a render cycle, because a thin
    declared band is sampled through a downscale that can pull its evidence from
    up to 2.5 design px outside the band.
    STATUS: FIXED IN THE MACHINE (upgrade 1).

D7. AN OBJECT APPEARED TO CAST A SHADOW THE RENDERER NEVER TRACED (slide 06's
    mass hung below the slab's front edge where the camera saw it).
    STATUS: knowledge only (FIELD_NOTES 2026-08-16).

D8. THE RENDER REPORT RECORDED A MULTI-LINE BLOCK AS ONE JOINED STRING CUT AT
    80 CHARACTERS, so copy_sync_check could not see slide 09's third fact line
    and reported a FALSE FAIL. Worked around by splitting the div.
    STATUS: FIXED IN THE MACHINE (upgrade 2).

D9. THE CAPTION DATE GATE AND ITS OWN CONFIG DISAGREE. caption_check.py's
    DATE_FORMS rejects "October 30, 2026" although config/brand.yaml says
    `with a year, "August 27, 2026"` and CAPTION_CRAFT says the same.
    STATUS: NOT FIXED, DELIBERATELY. Making them agree means either loosening a
    hard-fail regex, which is the maintainer's call and not this phase's, or
    rewriting two documents the owner wrote. Recommended in the dated email and
    recorded in FIELD_NOTES.

D10. BUILD RECONCILIATION IS WRITTEN ONCE, BEFORE THE CRITICS, AND THE DOSSIER
    HALF OF IT GOES STALE. Three of round 2's majors were the DOSSIER being
    wrong rather than the render: six ticks where five is correct, place ticks
    that had been deliberately deleted, a rail declared present on a slide that
    ships without one. The 2026-07-25 ordering rule is right; the 2026-08-05
    re-sync rule covers the SCRIPT-WRITTEN gate lines and not the hand-written
    dossier deltas.
    STATUS: NOT FIXED THIS RUN. It is a real gap and it is the first candidate
    for the next run's budget; three slots were already spent on defects that
    reached a reader. Recommended in the email.

## 2. FRONTIER SCAN

Focus: (c) generative/procedural art portable to offline Canvas/SVG. Distinct
from the last three logged foci (2026-08-14 headless rendering, 2026-08-12
accessibility/PDF, 2026-08-08 LinkedIn platform) and the stalest slot on the
rotation, last scanned 2026-08-01. Chosen over editorial dataviz because the
standing repeat offender is artwork craft and this is the slot that stocks it.

CONSTRAINT, recorded honestly: WebSearch was unavailable. The session had spent
its entire 200-call budget before Phase 12 (the same failure mode as 2026-08-01,
and the research phase is where it goes). The scan was therefore conducted by
WebFetch against the sources the last procedural-art scan parked, which is a
narrower instrument than a search sweep.

Read: volzo.de's hatching/hachures/contours writeup and Woodruff's sketchy relief
post, both of which the 2026-08-02 and 2026-08-14 entries cite. FINDING: neither
publishes parameters. Both defer to Jobard and Lefer's "Creating Evenly-Spaced
Streamlines of Arbitrary Density" for the placement algorithm, and that PDF does
not extract as text with the tooling available here (custom font encodings; the
extraction produced mojibake). Two candidate mirrors 404'd.

OUTCOME: nothing applied, nothing newly parked. The existing park stands with a
sharpened next step: the next procedural-art scan should hunt a READABLE
implementation of evenly-spaced streamline placement rather than another
overview, because three scans have now found the same two overviews.

D11. THE ON-SLIDE TEXT RULES WERE NOT ENFORCED ON ON-SLIDE TEXT, and this is
    the run's most expensive machine gap. Slide 06 shipped the kicker "AND
    FOURTEEN MORE" through every green gate; brand.yaml bans a slide string
    opening on And or But, twice, under visual.on_slide_text_rules and under
    brand.voice.dont (maintainer, 2026-08-05). The scorer caught it by reading
    the pixels and capped a raw 8.52 at 6.90. Investigating it turned up a
    second, larger hole underneath: caption_check's copy_prose() only walked a
    slide whose value was a DICT, and this deck's copy.json (like the copy
    room's usual output) holds LISTS OF STRINGS, so the 2026-08-08 date
    widening and the 2026-08-15 phrase widening had both been walking past
    every slide in the file. copy_fields_checked read 4 on a nine-slide deck.
    STATUS: FIXED IN THE MACHINE (upgrade 1, which displaced the probe-scale
    fix below).

## 3. UPGRADES MADE (3, all reactive, all verified)

U1. THE ON-SLIDE TEXT RULES NOW RUN ON ON-SLIDE TEXT (caption_check.py).
    copy_prose recurses through list-shaped slides (4 fields checked became 47
    on this run's own copy.json), and brand.yaml's opener rule gets its first
    implementation. Closes D11.

U2. THE RENDER REPORT RECORDS EVERY TEXT NODE, NOT THE FIRST 80 CHARACTERS OF
    THEIR JOIN (render.py, copy_sync_check.py). Closes the false-FAIL hole D8.

U3. THE AXIS CENSUS (render.py, qa.py, SKILL.md, routine_instructions.md). A
    slide with a measured axis declares it and enumerates the marks in its band;
    qa.py fails a mark that means nothing, a mark off its span, and any
    undeclared run of ink in the band as strong as the weakest mark the slide
    itself declared, printing the value that position reads as. Closes D1.

Verification evidence is in ledger/upgrades.json per entry. Headline: this run's
nine slides and examples/demo-deck were re-rendered and re-gated with all three
changes in place, and the fails/warns sets are IDENTICAL to the pre-change
baseline (run35 PASS 0/0, demo WARN 0 fails / 5 warns, same five). Each upgrade
additionally ships a reconstruction of the defect it exists to catch, and the
axis census was tested against a real slide from this deck.

## 4. NOT DONE, ON PURPOSE

- D6 (probe measurement scale) WAS BUILT AND VERIFIED AND THEN SWAPPED OUT, to
  stay inside the 0-3 budget when D11 arrived from the scorer mid-phase. D11
  cost this run 1.62 points of score; D6 cost four render cycles, so D6 loses.
  The work is not lost, it is described precisely enough to re-apply in about
  forty lines: cross-measure a declared probe at NATIVE resolution whenever its
  thinnest declared side is under 15 design px, keep the feed-scale verdict, and
  use the disagreement to say which kind of wrong it is (feed fails and native
  passes = the declaration is unmeasurable as authored, still a FAIL but the
  remedy is "widen or move the band" and not "re-light the slide"; feed passes
  and native fails = a new WARN; a region too small to sample at feed scale
  becomes a native measurement and a real verdict instead of an unmeasurable
  warn, which is a tightening). Measured evidence for the next run to reuse:
  take()'s int() mapping can put a sampled row's centre 2.5 design px outside
  the declared band, LANCZOS adds about one feed row of the neighbour at under
  10 percent, and on this run's own thin probes feed and native disagree by 1.3
  to 4.5 L*, against a 4.0 floor. FIRST IN LINE NEXT RUN, with D10.
- D9 (the caption date contradiction): a gate loosening is the maintainer's call.
- D10 (reconciliation staleness after a revision round): first in line next run.
- D3, D4, D5, D7: knowledge, not machinery. Each was considered as a gate and
  each needs a vocabulary the engine does not have.
- Nothing under out/2026-08-16/ or runs/ was edited, and none of the three
  fenced asset files was touched.
