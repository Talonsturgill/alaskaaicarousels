# PLAN, run No.86, 2026-10-14

Effort in effect: `high` (CLAUDE_EFFORT=high, as the repo settings intend).

Run date note: woke 2026-10-15 06:09 UTC, which is 2026-10-14 22:09 in Anchorage. No
`runs/2026-10-14/` exists, so the run date is the Anchorage date. `runs/2026-10-13/` never shipped.

## Queued assignment

`prompts/NEXT_RUN.md` (queued by No.65 on 2026-09-21) is ELIGIBLE today: it may be used from
October 14th, and the electronic-monitoring opt-in deadline of November 1st has not passed. It
assigns the North Pacific Fishery Management Council's October 5th to 13th action on NMFS's 2027
Annual Deployment Plan for observers and electronic monitoring. It overrides selection only. Every
gate binds. Beat C is pointed at it in full; the other five beats sweep normally so the runner-up
and the docket are fed. Re-run dedupe_check before committing to it. Every draft figure in the
brief is re-verified against the FINAL plan or the Council's motion before it prints.

## Ledger reads

- carousel_no 86 (85 entries in topics.json).
- Top instincts (confidence >= 0.7), injected into every subagent brief:
  1. grain-as-tile: grain as a small repeating tile (AK.grainTile / AK.grainOn), never a full-frame feTurbulence rect.
  2. machine-qa-is-not-taste: a machine_qa PASS is not composition approval.
  3. verify-body-line-count: check serif/body line counts against fixed labels and plates before rendering.
  4. a generated gate block goes stale when another round runs; regenerate at the last render.
  5. a constraint you can't point at is one you invented; there is no context budget.

## Variety constraints (forbidden this run)

- Hero structures of the last 4: THE MAGNIFICATION LADDER (10-09), THE MARGIN WALK (10-10),
  THE PAINT LAW (10-11), THE ROOM AND THREE ADDRESSES (10-12).
- Atmospheres of the last 3: COUNTED THINGS GLOW (count room), FIRST SNOW UNDER LED,
  THE ROOM LIT BY ITS SCREEN.
- Continuity devices of the last 2: motif THE PAINT LAW (gold number in an ordinance), motif
  THE DOOR LIGHT (gold for a way still open).
- Hook archetypes of the last 3: THE REMAINDER, CODE OR POLICY, THE ADDRESS.
- Palette families of the last 3: SMOKED ACRYLIC/RIVER ICE/FIREWEED; LOT LIGHT/WET
  ASPHALT/TRAFFIC PAINT; PROJECTOR SPILL/SLATE VELVET/LOWLAND TINT.
- Type pairings of the last 2: Archivo width axis + JetBrains Mono; Instrument Serif roman +
  Manrope + JetBrains Mono.

## Variance dials (chosen)

- design_variance 3 (last six: 4, 5, 3, 2, 4, 4). A documentary register, closer to house centre
  than No.85, because the story is a technical monitoring plan and the art should read as evidence.
- visual_density 4 (last: 2). Monitoring is about counting trips, days and fish; a denser field
  is honest to the subject.
- type_temperature 5 (last: 3, 1, 4). Warm serif display for the first time in a week, against
  cool camera-telemetry mono.

## Seasonal Alaska context, mid October

- NPFMC October meeting in Anchorage just closed (October 5th to 13th): groundfish harvest specs,
  observer ADP, crab. Bering Sea snow crab and red king crab seasons open October 15th.
- Electronic-monitoring pool opt-in deadline November 1st.
- Legislature out of session (zero hearings is normal). General election November 3rd, early
  voting from about October 19th. AFN convention is mid to late October. Alaska Day October 18th.
- Freeze-up beginning on the North Slope and interior rivers; Cook Inlet gas storage withdrawal
  season starting; PFD paid in October.
- Arctic Circle Assembly (Reykjavik) mid October; federal fiscal year 2027 began October 1st.

## STANDING WEAKNESS (trend_check --window 10)

```
REPEAT OFFENDERS
  weakest  7/10  mean 6.98   last 7.0    Artwork craft and genuine detail   worked 2026-10-04  STALE
  weakest  2/10  mean 7.08   last 7.0    Variety vs ledger                   worked 2026-08-15  STALE
  weakest  1/10  mean 7.72   last 8.0    Thumb-stop cover                    worked 2026-09-02  STALE
HARD FAILS: none in window
DEFECT CLASSES THAT KEEP SHIPPING
   3 run(s)  warns:busy art under text          latest 2026-10-11
   3 run(s)  warns:art touching glyphs          latest 2026-10-12
   2 run(s)  warns:contact shadow               latest 2026-10-11
   2 run(s)  warns:top-loaded composition       latest 2026-10-12
SCORES 10-05 8.64, 10-06 8.27, 10-07 8.74, 10-08 8.41, 10-09 8.20, 10-10 8.60, 10-11 8.26, 10-12 8.62
```

THE ONE WEAKNESS THIS RUN ATTACKS: artwork craft, specifically the scorers' most repeated cause,
"the largest object is the least modelled thing on the frame" (No.84 and No.85 both stalled at art
7.0 or under on exactly that, on the cover first). How:

1. Fewer, larger objects, each with ONE modelling method planned in the CRAFT PLAN and built at
   the highest rung that suits it, and no object on a frame that the plan does not model.
2. Build order: the masterful depth frame and the cover FIRST, and close both by round 3 (No.83
   and No.84 lesson: the cover was rebuilt most and reviewed least).
3. One EVENT per lower third, not a texture (No.78 lesson).
4. Text reserves designed into the ground before the first render, so "busy art under text" and
   "art touching glyphs" never appear (the two defect classes that keep shipping).
5. Weekly machine pass is NOT due (last 2026-10-11; machine_due exit 1); queue anything new.
