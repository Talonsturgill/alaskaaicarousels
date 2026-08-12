# RUN PLAN — 2026-08-12 — Carousel No. 31

## Run date

Wake fired at 2026-08-11 23:19 AKDT, forty minutes short of midnight. The run
date is **2026-08-12**, because every artifact this run writes, commits, merges
and emails will carry a clock that reads August 12th in Anchorage. Dating the
run 08-11 would put the whole of it in a day that ends before Phase 2 finishes.
The last shipped deck was No.30 on 2026-08-09; 08-10 and 08-11 were development
sessions and produced no deck, so there is no queued backlog to reconcile.

carousel_no = 30 entries in ledger/topics.json + 1 = **31**.

## Queued assignment

`prompts/NEXT_RUN.md` does not exist. No maintainer directive is in force.
Story selection is this run's own call.

## Top instincts injected into every subagent this run

1. (0.99) A machine_qa PASS is never composition approval. The pixel critics
   judge composition, hierarchy and collision at full size and at thumb size.
2. (0.99) Sanity-check long serif or body copy line counts against fixed
   labels, bars and plates before rendering. DOM text overlaps pass machine QA
   and fail the eye.
3. (0.99) A generated gate block pasted into a run record goes stale the moment
   another round runs. Re-sync after every round that changes an artifact.
4. (0.99) A constraint you cannot point at is a constraint you invented. This
   routine has no context budget and no token budget. Nothing measures one.
5. (0.98) qa.py's text-collision check is DOM only. A label positioned against
   Canvas or SVG geometry can collide freely and the gate still returns PASS.

## Variety constraints (from ledger/artwork.json)

FORBIDDEN hero structures (last 4): THE TRAVERSE (27), THE UNBOUNDED POPULATION
(28), THE LIT APERTURE (29), THE OPEN TREAD (30). Note the family beneath them,
decks 24 to 30 have all been a bounded instrument, sheet, object or field under
one fixed camera or one traverse of stations. Breaking the family is worth more
than breaking the four names.

FORBIDDEN atmospheres (last 3): REPLY AS KEY LIGHT (28), TANNIN BACKLIGHT (29),
NORTH WINDOW HIGH KEY (30). 30 was the first light-register deck in nine runs,
so a return to near-black is available and is not a regression.

FORBIDDEN continuity devices (last 2): THE SINGLE TAKE and THE FALLING KEY (29),
THE FLOOR DATUM and THE TWO MATERIALS (30). Any mono shot-log or station-counter
fixture is spent for now; four of the last five decks carried one.

FORBIDDEN hook archetypes (last 3): THE SILENT MAJORITY (28), THE DISQUALIFYING
VIRTUE (29), THE MEASURE THAT STOPS (30).

FORBIDDEN palette families (last 3): CARD STOCK AND VOID (28), TANNIN WATER AND
CHUTE WHITE (29), BIRCH FLOOR AND NORTH WINDOW (30).

FORBIDDEN type pairings (last 2): Instrument Serif + Archivo + JetBrains Mono
(29), Bricolage Grotesque + Fraunces italic + JetBrains Mono (30). JetBrains
Mono has been the instrument face on every deck since 27; if a mono is needed
this run it should be a different one, and the deck should consider carrying no
mono at all.

## Variance dials for No.31

- design_variance: **4**
- visual_density: **5** (last four ran 4, 3, 3, unstated; density has not been
  pushed to 5 in the recorded window)
- type_temperature: **5**

## Standing weakness this run attacks

`scripts/trend_check.py --window 10` (2026-07-31 to 2026-08-09):

```
REPEAT OFFENDERS (criterion, times weakest, mean, last worked on)
  weakest  6/10  mean 6.0    last 5.0    Artwork craft and genuine detail   worked 2026-08-07
  weakest  3/10  mean 5.94   last 4.0    Legibility and platform fitness    worked never  <-- STALE
  weakest  1/10  mean 6.0    last 6.0    Legibility & platform fitness      worked never  <-- STALE
HARD FAILS (1 of 10 runs)
   1x text against geometry 2026-07-31 | 1x contrast 2026-07-31
DEFECT CLASSES THAT KEEP SHIPPING
   6 runs warns:top-loaded composition   latest 2026-08-08
   5 runs warns:outside safe zone        latest 2026-08-09
   3 runs warns:art touching glyphs      latest 2026-08-08
   2 runs warns:busy art under text      latest 2026-08-07
   2 runs warns:text collision           latest 2026-08-06
   2 runs warns:tiny-text                latest 2026-08-08
SCORES 08-02 8.37 | 08-03 6.90 | 08-04 7.25 | 08-05 7.27 | 08-06 7.93 | 08-07 8.55 | 08-08 8.02 | 08-09 7.57
```

THE ONE THIS RUN ATTACKS: **legibility and platform fitness**, and the reason is
that it is the only criterion in the table that has NEVER been worked on. Read
the two rows as one criterion split by a punctuation change in its own name and
it is weakest 4 of 10 with a most recent value of 4.0, which is the lowest
number anywhere in the report, lower than artwork craft's 5.0. It has stayed
invisible because artwork craft is the louder headline and because the two
spellings split its count in half.

It also has the only machine-visible signature in the table. Top-loaded
composition, text outside the safe zone and art touching glyphs are not opinions,
they are qa.py warn strings, and they have shipped in 6, 5 and 3 of the last ten
decks. A criterion whose failure mode is already instrumented is the cheapest one
in the report to actually move.

How this run attacks it, in the plan rather than in a Phase 9 repair pass:

1. Every dossier declares a BOTTOM-THIRD MASS target, the fraction of visual
   weight below y=900 of 1350, with a floor of 0.30, and names the drawn element
   that carries it. Top-loaded composition is the number one defect class and it
   is caused by planning the top of the frame and letting the bottom happen.
2. Every text block's anchor box is stated in design pixels in the dossier with
   its distance to the nearest frame edge, and no block sits closer than 72 px.
   Five of the last ten decks shipped text outside the safe zone.
3. Nothing is set against live geometry without a declared separation. Where a
   label must sit on drawn art, the dossier names the SUBTRACTION that clears it
   (a lit pool, a scrim with a measured alpha, a knockout), never a plate dropped
   on top after the fact, and never nothing. qa.py's collision check is DOM only
   and cannot see this class, so it has to be planned.
4. Thumb-first review. Every slide is judged at 432 px before it is judged at
   full size, because platform fitness is a feed-scale property and the deck is
   consumed at feed scale.

SECONDARY, carried but not the headline: artwork craft stays gated by
bespoke_check (drawn share floor 45 percent, bespoke median ceiling 0.60) and
this run targets a drawn share at or above 62 percent. Phase 12 owns the
question of whether artwork craft gets worked on again or is explicitly
deferred, and it must say which.

## Seasonal Alaska context (for the scouts)

- The Alaska statewide PRIMARY ELECTION is Tuesday August 18th, 2026, six days
  out. Election administration, voter rolls, mis and disinformation, ballot
  counting technology and campaign spending are all live and time-boxed.
- The Legislature is in interim. Committees can and do meet; BASIS shows zero
  scheduled hearings for the committees holding tracked bills, which is normal
  from June to December and is not a collector failure.
- Cook Inlet is in injection season and the storage field is at 51.9 percent of
  design capacity with both an injection restriction and a withdrawal
  restriction flagged. Winter gas supply is the standing Southcentral story and
  it is the fuel behind every data centre conversation in the Railbelt.
- Federal fiscal year ends September 30th, so grant, solicitation and
  procurement windows are closing through August and September.
- Late season salmon (pink and coho), Bristol Bay sockeye wrapping, the tail of
  wildfire season, the Alaska State Fair opening in Palmer around August 20th,
  school year starting, and the run-up to the September sea ice minimum.
- PFD amount announcement lands in September, distribution in October.

## Dedupe pressure

Thirty topics on the ledger, fourteen of them inside the last thirty days.
Heavily worked ground that a new candidate must clear: Alaska data centre land
and power (18, 27), Cook Inlet and Railbelt energy for AI (20, 25, 27), the
Division of Elections voter roll citizenship check (22, 28), Alaska AI
procurement notices (23), campaign finance and the governor's race (17, 21),
fisheries computer vision (19, 29), school and district AI policy (30), federal
tribal program money (26), Graphite One (24).

At this cadence the binding constraint is the 30-day semantic dedupe, so a
candidate that is a fourth visit to voter rolls or a fifth visit to data centre
acreage has to be an explicit UPDATE with a material new development or it does
not ship.

## Phase order for this run

Standard. Phases 0 through 14 as written in prompts/routine_instructions.md.
No degradations planned at wake.

## Round 1 review findings (2026-08-12, after the first pixel-critic pass)

All nine slides came back `revise`. Scores: 01 6.0, 02 5.0, 03 5.5, 04 6.0,
05 5.0, 06 6.5, 07 5.5, 08 2.5, 09 5.0. Three of the findings were not
slide-local, and those are the ones worth keeping.

**1. The post chain's `exposure` is in STOPS and every slide passed a
multiplier.** Nine slides passed `exposure: 1.02` to `1.05` meaning "about
three percent". akpost.js reads it as stops, so `2^1.03 = 2.04x`, a full
stop over. That single defect produced most of what five independent critics
reported as separate faults: copper #B8703C blooming into something they
could not separate from gold #FFC72C at 432 px, partner-block lids reading
near-white, and the deck's gold law appearing broken on six slides at once.
It is now ~0.03 on all nine. Candidate Phase 12 upgrade: akpost.js should
refuse, or at least console.error, on an exposure above about 1.5 stops,
because nothing in this house's grade ever wants that and the failure is
silent and deck-wide.

**2. `AK.fitText` silently exceeds its own `maxLines`.** On slides 02, 03,
05, 06 and 08 the block ran to more lines than declared, because `min` was
set higher than the width could ever hold. Slide 08 lost the sentence that
carries the deck's thesis to a three-line clamp. The failure mode is
authored, not a library bug: `min` and `width` were chosen independently.
The fix each time was to widen the box and lower `min`.

**3. Slide 05's dimension was metrically perfect over a scene that
contradicted it.** The 840 px rule was exact and the two masses it named
were 266 px apart, so the deck's one load-bearing measurement, the twenty
feet, was drawn as about six. The rig is now solved FROM the lock: one world
unit is one foot and the camera distance is computed so one foot is 42 px.
The dimension can no longer disagree with the room, because the same number
produces both. Slide 08 inherits the corrected rig byte for byte, which is
also what makes its substitution provable.

A fourth, smaller: continuity device A shipped at two thirds of its declared
form. The nine-rung ladder was in the storyboard and on no slide. It is now
on all nine.
