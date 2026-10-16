# PLAN, run No.87, 2026-10-15

Effort in effect: `high` (CLAUDE_EFFORT=high, as the repo settings intend).

Run date note: woke 2026-10-16 06:14 UTC, which is 2026-10-15 22:14 in Anchorage. No
`runs/2026-10-15/` exists, so the run date is the Anchorage date. run_guard --run-date 2026-10-15
printed CLEAR. No `prompts/NEXT_RUN.md` is queued (No.86 archived the last one).

## Ledger reads

- carousel_no 87 (86 entries in topics.json).
- Top instincts (confidence >= 0.7), injected into every subagent brief:
  1. A constraint you can't point at is one you invented; there is no context budget (0.99).
  2. grain-as-tile: grain as a small repeating tile (AK.grainTile is a DATA URL for a CSS background, never createPattern), never a full-frame feTurbulence rect.
  3. machine-qa-is-not-taste: a machine_qa PASS is not composition approval.
  4. verify-body-line-count: check serif/body line counts against fixed labels and plates before rendering.
  5. A generated gate block goes stale when another round runs; regenerate it at the last render.

## Variety constraints (forbidden this run)

- Hero structures of the last 4: THE MARGIN WALK (10-10), THE PAINT LAW (10-11),
  THE ROOM AND THREE ADDRESSES (10-12), THE EXHIBITS (10-14).
- Atmospheres of the last 3: FIRST SNOW UNDER LED, THE ROOM LIT BY ITS SCREEN,
  SEA SMOKE AT THE RAIL.
- Continuity devices of the last 2: motif the door light, camera flight booth to doors, projector
  palette arc (10-12); camera move below/above the mast, night-sodium to dawn palette arc,
  edge-teases cable / scrub bar / lamp spill (10-14).
- Hook archetypes of the last 3: CODE OR POLICY, THE ADDRESS, BETTER EYES SAME BILL.
- Palette families of the last 3: LOT LIGHT/WET ASPHALT/TRAFFIC PAINT; PROJECTOR SPILL/SLATE
  VELVET/LOWLAND TINT; GALVANIZED ZINC/TARRED GROUNDLINE/GULF SEA SMOKE.
- Type pairings of the last 2: Instrument Serif roman + Manrope + JetBrains Mono; Fraunces display
  and text (opsz) + JetBrains Mono.

## Variance dials (chosen, revisited at selection)

- design_variance 5 (last seven: 3, 4, 4, 2, 4, 5, 3). The last two runs sat at 3 and 4; push the
  composition off house centre.
- visual_density 2 (last: 4, 2, 3, 4). Fewer, larger objects is also the standing-weakness attack.
- type_temperature 2 (last: 5, 3, 1, 4). Cool, after No.86's warm serif.

## Seasonal Alaska context, mid October

- Alaska Day October 18th. General election November 3rd; early and absentee in-person voting
  opens about October 19th. AFN convention late October.
- Bering Sea crab seasons open October 15th. NPFMC October meeting just closed; EM opt-in deadline
  November 1st.
- PFD payments in October. Freeze-up starting on the North Slope and interior rivers. Cook Inlet gas
  storage in withdrawal season (Gas Watch shows injection restriction active, inventory declining).
- Federal fiscal year 2027 began October 1st. Arctic Circle Assembly mid October.
- Legislature out of session (zero hearings normal).

## STANDING WEAKNESS (trend_check --window 10)

```
REPEAT OFFENDERS
  weakest  7/10  mean 6.88   last 6.5    Artwork craft and genuine detail   worked 2026-10-04  STALE
  weakest  2/10  mean 7.08   last 7.5    Variety vs ledger                  worked 2026-08-15  STALE
  weakest  1/10  mean 7.77   last 8.0    Thumb-stop cover                   worked 2026-09-02  STALE
HARD FAILS: none in window
DEFECT CLASSES THAT KEEP SHIPPING
   3 run(s)  warns:contact shadow                latest 2026-10-14
   3 run(s)  warns:busy art under text           latest 2026-10-11
   3 run(s)  warns:art touching glyphs           latest 2026-10-12
   2 run(s)  warns:top-loaded composition        latest 2026-10-12
   2 run(s)  warns:outside safe zone             latest 2026-10-14
SCORES 10-06 8.27, 10-07 8.74, 10-08 8.41, 10-09 8.20, 10-10 8.60, 10-11 8.26, 10-12 8.62, 10-14 8.51
```

THE ONE WEAKNESS THIS RUN ATTACKS: artwork craft (weakest 7 of 10, last 6.5). The scorers' most
repeated cause is "the largest object is the least modelled thing on the frame". How:

1. Fewer, larger objects (visual_density 2). Each frame's largest object gets ONE named modelling
   method in the CRAFT PLAN, built at the highest rung that suits it; nothing on a frame the plan
   does not model.
2. Build order: the cover and the masterful depth frame FIRST, closed by round 3.
3. One EVENT per lower third, never a texture.
4. Text reserves designed into the ground before the first render (busy art under text, art
   touching glyphs). Contact shadows only where an object sits, measured with contact_probe.
5. No objects near the safe-zone edge (outside safe zone shipped twice).

Weekly machine pass NOT due (last 2026-10-11; machine_due exit 1, 14 queued, 0 repeat offenders).
Queue anything new in knowledge/MACHINE_QUEUE.md.
