# RUN PLAN — 2026-07-26 — Carousel No. 18

## Wake state

- Run date (America/Anchorage): 2026-07-26. Research window: last 10 days
  (2026-07-16 to 2026-07-26).
- carousel_no = 17 topic entries + 1 = **18**.
- Bootstrap: OK (playwright/chromium ok, pypdf repaired by bootstrap).

## Top instincts injected into every subagent this run

1. Machine QA PASS is never composition approval. The eye gates (pixel
   critics, flow critic) judge hierarchy, collision and story-art fusion at
   full size AND at 432px thumb. (0.99)
2. qa.py's text-collision check is DOM-only. Any label positioned against
   Canvas or SVG geometry can collide freely and still return PASS, so plan
   clearances by arithmetic, not by trust. (0.97)
3. Sanity-check long serif/body copy line counts against fixed-position
   labels, bars and plates BEFORE rendering. DOM text overlaps pass machine
   QA and fail the eye. (0.99)
4. Grain is a small repeating tile (AK.grainTile), never a full-frame
   feTurbulence rect. (0.99)
5. Read dedupe_check.py output IN FULL, never through head/tail: its
   strongest LIKELY DUPLICATE can print anywhere in the list. (0.95)
6. Plan every 3D camera with the ak3d.js horizonY arithmetic before
   rendering; never eyeball camera placement. (0.90)
7. Nothing ships that claims.json does not carry. A thin true deck beats a
   rich invented one. (house rule)

## Variety constraints derived from ledger/artwork.json

FORBIDDEN hero structures (last 4, decks 14 to 17):
- cadastral hillshade relief + gold parcel state machine (14)
- rendered gold authority seal state machine (15)
- the Adjudicated Margin op-ed chassis + migrating pen (16)
- THE MILLED REGISTER, one bone limestone slab, cut/scored state machine (17)

FORBIDDEN atmospheres (last 3):
- deep-arctic charter navy (15)
- op-ed warm ink-black paper (16)
- gallery-lit bone LIGHT GROUND (17)

FORBIDDEN continuity devices (last 2):
- the adjudicated margin / comment stack + migrating pen (16)
- the CUT state machine + the sundial key-light rotation (17)

FORBIDDEN hook archetypes (last 3):
- authority / order-of-operations declarative (15)
- reclaimed quote as a dare (16)
- asymmetry couplet about the record itself (17)

FORBIDDEN palette families (last 3):
- deep-night navy + forget-me-not + aurora green + gold authority (15)
- warm ink-black paper + forget-me-not + oxblood + slate (16)
- bone dominant + groove brown + fireweed + navy chips (17)

FORBIDDEN type pairings (last 2):
- Instrument Serif + Manrope + JetBrains Mono (16)
- Fraunces + Bricolage Grotesque + JetBrains Mono (17)

Also note: 07-25 spent the light-ground allowance (1 per 8 runs), so this
run returns to the dark arctic base register.

## VARIANCE DIALS (chosen deliberately, diverging from the last four)

- DESIGN_VARIANCE = 4 (last four: 3, 4, 4, 5)
- VISUAL_DENSITY = 5 (last four: 4, 3, 4, 2 — density 5 is unspent in the
  recent window; this run earns its keep as an information-dense,
  instrument-heavy deck a reader saves and returns to)
- TYPE_TEMPERATURE = 1 (last four: 2, 3, 3, 5 — hard swing back to cool
  grotesk/mono after yesterday's warm serif bone deck)

Reading: a cold, dense, instrument-voiced deck on a dark ground. Yesterday
was warm, sparse, serif and light. Nobody will confuse the two in a feed.

## Caption variety constraints (ledger/captions.json)

- Opening moves barred (last 6): LEGACY STANDARD, DEFINITION SUBVERSION,
  LEDGER TALLY, COLD NUMBER. Additionally the 07-25 note bars a THIRD
  consecutive numeric opening on sight.
- Structures barred (last 3): PUNCH THEN PROOF, INVERTED PYRAMID, COUNTDOWN.
- Closing move barred (last 1): stake.
- Grafting candidate carried forward from 07-25's losing candidate: "One
  list exists because a law demanded it. The other because a reporter
  asked." Use only if the story genuinely earns it.

## Seasonal Alaska context (late July 2026) for the scouts

- Peak WILDFIRE season. Interior smoke, AFS/BLM Alaska Fire Service
  activity, fire-detection and fire-behavior modeling angles are live.
- Commercial FISHING season at full tilt. Bristol Bay sockeye run past
  peak, Yukon/Kuskokwim chinook restrictions, NOAA/NMFS in-season
  management and bycatch monitoring.
- AKLNG THIRD SPECIAL SESSION is convening around July 27 (tracked in
  FIELD_NOTES from the 07-21 run). Gas supply and any AI/data-center load
  argument attached to it is in window.
- Alaska PRIMARY ELECTION is Aug 18, 2026 (26 days after wake). Election
  administration, deepfake/synthetic-media rules and campaign money are
  live but 07-25 already shipped the AI-money-in-the-2026-race deck, so
  that exact frame is a dedupe collision.
- Peak TOURISM and construction season; road work; cruise traffic.
- Military: summer exercise season in the Alaska ranges (RED FLAG-Alaska
  cycle), plus the ongoing Arctic ISR build-out.
- Permafrost thaw season, coastal erosion surveys, sea-ice minimum
  approaching in September; subsistence harvest documentation.
- School districts are writing AI policy ahead of the August start (the
  07-20 deck's follow-on; an ADOPTION vote would be a legitimate UPDATE).

## Recent topic exclusions (90-day dedupe, hot list)

Cook Inlet gas storage/RCA (07-11), autonomous wildfire-fighting XPRIZE
(07-12), GVEA turbine vote (07-13), ReconCraft autonomous defense boats
(07-14), NSF critical-minerals engine (07-15), Quinhagak/Nalaquq drones
(07-17), data-center power-bill economics (07-18), Utqiagvik permafrost
digital twin (07-19), school AI policy / KPBSD (07-20), Cook Inlet beluga
acoustic AI (07-21), DNR ADL 234762 land conveyance (07-22), tribal health
AI governance (07-23), STAK North Slope data-center comment revolt (07-24),
AI money in the 2026 governor's race (07-25). Plus the older set in
ledger/topics.json (data centers Nos 1, 4, 6, 10; salmon CV; volcano;
Navy; SAR).

The binding constraint at daily cadence: this run needs a genuinely
distinct story or an honest UPDATE reframe.

## Phase order note

Scouts (Phase 2) were launched first and the Phase 1 craft refresh ran
concurrently while they worked. The two do not feed each other; this is a
wall-clock optimization, recorded here so the Phase 12 retro sees it as
deliberate rather than as a skipped phase.
