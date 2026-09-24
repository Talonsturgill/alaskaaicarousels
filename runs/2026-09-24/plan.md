# RUN PLAN — Alaska.Ai Carousel No. 67 — September 24th

## Wake state

- Woke 2026-09-23 23:15 AKDT (07:15 UTC 2026-09-24). `runs/2026-09-23/` already holds No.66,
  shipped, merged (PR #393) and drafted by the previous daily firing about 22 hours earlier, so
  this firing is a new day and not a re-fire. The Anchorage date is taken, so per CONTEXT the run
  date is the first date with no `runs/<date>/`, **2026-09-24**. run_guard for 2026-09-24: CLEAR.
- carousel_no = 66 topics entries + 1 = **67**.
- effort: `$CLAUDE_EFFORT` = **high**. The setting took.
- `prompts/NEXT_RUN.md` is **PARKED** (DO NOT USE BEFORE OCTOBER 14TH). It stays in place, is not
  archived this run, and this run selects its own story.

## Standing weakness, and what this run does about it

`trend_check.py --window 10` (2026-09-12 to 2026-09-23):

```
REPEAT OFFENDERS
  weakest  8/10  mean 7.0  last 8.0  Artwork craft and genuine detail   worked 2026-09-14 (7 runs ago)  <-- STALE
  weakest  1/10  mean 7.5  last 7.0  Deliverable completeness           worked never  <-- STALE
  weakest  1/10  mean 8.2  last 9.0  Alaska authenticity and relevance  worked 2026-09-20
HARD FAILS: none in this window
DEFECT CLASSES THAT KEEP SHIPPING: none recurring in this window
SCORE: 09-14 8.76  09-15 8.61  09-17 8.79  09-18 8.76  09-19 8.36  09-20 8.50  09-21 7.98  09-23 8.67
```

**THE ONE STANDING WEAKNESS THIS RUN ATTACKS: artwork craft and genuine detail**, weakest in 8 of
the last 10. No.66 lifted it to 8.0 with contour hatching, which says the answer is DRAWN MARKS
carrying tone, not filled shapes. This run keeps that lesson and changes the idiom:

1. **The tone is carried by a field of drawn marks with meaning** (stipple, hatch, flow lines,
   contour lines), never by fills. Every region carries marks at zoom. Drawn share targeted well
   above the 45 percent floor.
2. **Every frame gets its own drawing function.** Shared projection or noise helpers are furniture;
   no shared slide composer.
3. **The hero climbs the rendered ladder or argues flat in the dossier.** The last three decks were
   all frontal/orthographic with no camera. This deck should put a camera back in (a perspective
   terrain or an oblique map), which is itself a variety move.
4. **Contact shadows and lower thirds designed in at build time**, measured with contact_probe.py
   off a real render, never computed.

## Variety constraints, derived from ledger/artwork.json

FORBIDDEN this run:
- hero structures (last 4): the season disc (No.63), the jurisdiction section (No.64), the waterline
  hold (No.65), the reading frame plate (No.66).
- atmospheres (last 3): Kachemak stratus at low sun (No.64), flood tide under high overcast (No.65),
  interior plate light (No.66).
- continuity devices (last 2): No.65's docket staff, render state, edge tease; No.66's reading
  frame state, engraved ground, struck slot, scale ladder.
- hook archetypes (last 3): the vector (No.64), the state of matter (No.65), the enacted limit (No.66).
- palette families (last 3): cold navy over warm cut earth; extinction to specular through water,
  silt and flour; ink and plate with #7D4A45 struck reach.
- type pairings (last 2): Unbounded / Instrument Serif / JetBrains Mono (No.65); Fraunces / Manrope /
  JetBrains Mono (No.66).
- Carried forward: edge tease ran three consecutive decks through No.65 and is treated as burned.
  No camera / no horizon has now run three decks (No.64, No.66 and largely No.63); a CAMERA is the
  divergence this deck should take.

## Variance dials, chosen deliberately

- design_variance **3** (No.66 ran 5; a camera-and-terrain deck is closer to the house center and
  that is the point, after three extreme abstractions)
- visual_density **4** (a field of drawn marks is dense by nature)
- type_temperature **2** (No.66 ran 4, warm Fraunces; swing cool)

## Caption room, burns carried forward

From `caption_check.py --burns`: opening move not COUNTED AUTHORITY THEN THE ABSENT BODY, COUNTED
THINGS THEN A COUNTED ABSENCE, THE DIRECTIONAL QUESTION, DEFINITION SUBVERSION, CONTRADICTION,
SECOND PERSON STAKE. Structure not INVERTED PYRAMID, three specifications then the absence..., Q AND
A then three beats. Closing move not WHICH CLAUSE SURVIVES THE HYPOTHETICAL. First four words differ
from the last 12. Every closing-move name in the burn table is spent. Count-then-absence is burned as
a SHAPE, not just a name.

## Seasonal Alaska context handed to every scout

Freeze-up approaching; termination dust; Legislature out of session; fall hunts and subsistence;
Bering Sea crab ahead of October 15th; PFD paid early October; AFN mid October; North Pacific Council
October 5th to 13th; sea ice minimum; Cook Inlet winter gas (CINGSA dashboard stale since September
13th); RCA rate cases; federal fiscal year end September 30th; October 6th municipal elections;
November 3rd general election.

## Research sweep

Six scouts, one per beat, each capped at 25 WebSearch calls with the reason stated, each told how to
record a PDF primary for the showrunner, each given the 403 host list with routes, and each given the
full 30-day avoid list plus the parked NPFMC brief.

## Phase 3.6 state at plan time

- CRON HEALTH: FAIL on `gaswatch.yml:completion` and `gaswatch.yml:steps` only; 33 of 35 PASS across
  all 6 scheduled workflows. Same upstream cause as No.66: CINGSA's dashboard still reads
  `09/13/2026 21:00` (verified in the raw bytes at about 07:20 UTC), three days past its own announced
  return date of September 21st. Job log for run 35927882616 shows the designed loud failure (status
  3). `cron_incidents.json` and `gaswatch_incident.json` written, blocker upstream; both rows WARN.
- GAS WATCH LIVE: FAIL on source freshness (242.3 hours) and the collector job; 10 of 12 PASS.
- SITE SIGN-OFF: WARN, 120 pages, 18 checks, the one UNFIXED row is gaswatch.jsonl is current (same
  upstream cause). 5,086 links resolve.
- Visual pass at desktop and phone (home, docket, gas watch): no horizontal overflow anywhere. One
  presentation defect found and FIXED: at phone width the modeled peak and non-CINGSA supply lines
  struck through their own endpoint numerals (142, 128.6). The label now carries a halo in the panel
  ground; verified on a rebuilt page. Committed as `site(2026-09-24)`.
