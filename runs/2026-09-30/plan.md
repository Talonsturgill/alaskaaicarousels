# PLAN — run 2026-09-30, Carousel No.73

Run date 2026-09-30 is the Anchorage date at wake (22:15 AKDT). run_guard.py
defaults to UTC and printed 2026-10-01; `--run-date 2026-09-30` is CLEAR and
runs/2026-09-30 does not exist, so the run takes the Anchorage date.
Effort in effect: `high` (CLAUDE_EFFORT=high). The setting took.

## Queued assignment
`prompts/NEXT_RUN.md` (NPFMC 2027 Annual Deployment Plan, queued by No.65) is
dated "DO NOT USE BEFORE OCTOBER 14TH". This run is September 30th, so the brief
stays PARKED in place and this run selects its own story. Say so in the ship note.

## Top instincts (confidence >= 0.7), injected into every subagent brief
1. A REPAIR CAN LAND A BIGGER DEFECT THAN THE ONE IT FIXED; only a fresh adversarial read catches it. (0.98)
2. A lit ground is SCREENED over the surface, never painted on it; the cast is an ATTACHED subtraction thrown down-light. A painted radial pool centred on an object's own base is the hole in a spotlight. (0.98)
3. qa.py's text-collision check is DOM-only; labels against canvas/SVG geometry can collide freely and pass. Art-band labels ship on an opaque knockout plate by default. (0.98)
4. Before rendering, sanity-check long serif/body copy line counts against fixed-position labels, bars or plates; DOM text overlaps pass machine QA and fail the eye. (0.99)
5. Grain is a small repeating tile (AK.grainTile returns a DATA URL for a CSS background, never a createPattern input), never a full-frame feTurbulence rect. (0.99)

## Variety constraints (from ledger/artwork.json)
- FORBIDDEN hero structures (last 4): the focus-pull set (09-26), the Lobeck block (09-27), the night strobe shot list (09-28), the cut-and-paste notice (09-29).
- FORBIDDEN atmospheres (last 3): low sun short day (raking afternoon sun az 240); off-camera strobe in falling snow; copy-desk rake (one lamp upper left az 305 with a pool).
- FORBIDDEN continuity devices (last 2): weather clock; screenplay slate; the record stack; paper/ink alternation; the ink law AS a continuity device (data-ink declarations stay required as QA).
- FORBIDDEN hook archetypes (last 3): the promise and its date; the sized door; the quoted question.
- FORBIDDEN palette families (last 3): glacial flour and low sun; strobe on black spruce and tamarack; bleached newsprint and press black.
- FORBIDDEN type pairings (last 2): Instrument Serif over Manrope; Fraunces over Space Grotesk.
- Light deck: No.72 was half paper; no light deck this run (dark arctic register).

## Variance dials (vary the dials themselves)
Recent: (3,2,5) (4,5,2) (5,3,3) (4,3,3). This run: DESIGN_VARIANCE 3, VISUAL_DENSITY 4,
TYPE_TEMPERATURE 4 (warm serif lean without the 5 of No.69). Directors may argue one notch.

## Seasonal Alaska context (late September to early October)
- Federal fiscal year ends September 30th; FY2027 begins October 1st (grant and contract awards land in the last week; continuing resolution or shutdown risk).
- PFD: 2026 amount announced in September, payments in October.
- Election November 3rd (governor and ballot measures); AFN Convention mid-October.
- Legislature out of session (zero hearings normal).
- NPFMC meets October 5th to 13th in Anchorage (parked brief); Bering Sea crab opens October 15th.
- Freeze-up beginning in the Interior and Arctic, termination dust in Southcentral, first winter storms in western Alaska; Cook Inlet gas injection season ending, winter withdrawal season starting (Gas Watch shows injection restriction active).
- Moose and caribou seasons closing; fall sea ice minimum just passed.

## Trend check (scripts/trend_check.py --window 10)
```
REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  weakest  7/10  mean 7.15   last 8.0    Artwork craft and genuine detail        worked 2026-09-28 (1 run(s) ago)
  weakest  1/10  mean 7.3    last 7.0    Legibility and platform fitness         worked never (never)  <-- STALE
  weakest  1/10  mean 7.45   last 8.5    Variety vs ledger                       worked 2026-08-15 (38 run(s) ago)  <-- STALE
  weakest  1/10  mean 7.6    last 8.0    Deliverable completeness                worked never (never)  <-- STALE
HARD FAILS (0 of 10 run(s) carried one)
DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   2 run(s)  warns:art touching glyphs                             latest 2026-09-29
   2 run(s)  warns:busy art under text                             latest 2026-09-29
   2 run(s)  warns:outside safe zone                               latest 2026-09-29
SCORE, most recent runs
  09-21 7.98  09-23 8.67  09-24 8.34  09-25 8.69  09-26 8.16  09-27 8.47  09-28 8.23  09-29 8.79
```

## The ONE standing weakness this run attacks
ARTWORK CRAFT (weakest in 7 of 10). How: the CRAFT PLAN is written before any dossier,
with the largest object on every frame named and modelled; no text frame is allowed to be
"labels over a gradient" (No.71's 04, deferred); the masterful depth frame is built FIRST
and reviewed before the rest; every type block over art gets its reserve designed in, not
added at a gate (attacks the two recurring warn classes, art touching glyphs and busy art
under text). The per-slide dossier ambition for each frame is set to "survives the zoom
test" rather than "passes its own checklist" (No.71 lesson).
