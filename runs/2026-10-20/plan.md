# PLAN, run 2026-10-20, carousel No.91

Run date: Anchorage 2026-10-20 (woke 22:05 AKDT; UTC already 2026-10-21). run_guard CLEAR.
Effort: high (CLAUDE_EFFORT=high, as the repo setting intends).
Queued assignment: none (no prompts/NEXT_RUN.md).
Weekly machine pass: not due (last 2026-10-17); Phase 12 retro and queue only.

## Top 5 instincts (confidence >= 0.7), injected into every brief

1. A generated block pasted into a run record goes stale the moment another round runs; re-sync gate_status after every round.
2. AK.grainTile returns a data URL, not a canvas; grain is a DOM layer (overlay, 0.05 to 0.12), never a canvas fill.
3. A constraint you can't point at is one you invented; no context or token budget exists, draw the next slide.
4. A machine_qa PASS is not composition approval; the pixel critics judge composition, hierarchy and collision.
5. Sanity-check long body copy line counts against fixed-position labels and plates before rendering.

## Variety constraints (ledger/artwork.json)

Forbidden hero structures (last 4): THE FRAME IS THE RULER (10-15); THE TRANSCRIPT WITHOUT A WITNESS (10-16); THE ANALYSIS LATTICE (10-17); THE SPLIT SPECIMEN (10-19).
Forbidden atmospheres (last 3): panel light on satin; the break under the ceiling (low stratus); runway night over the core.
Forbidden continuity devices (last 2): camera ALT readout descent and climb; Delta cell motif; pale-break palette arc; kerf motif; orbit camera around one specimen; cover right half cut and completed on 02.
Forbidden hook archetypes (last 3): THE VERBATIM REFUSAL; THE BLANK ON THE MAP; THE TWO READINGS.
Forbidden palette families (last 3): carbon, oxblood and muskeg; silt, stratus and sedge rust; core box sandstone, coal and methane ice on subsurface navy.
Forbidden type pairings (last 2): Bricolage Grotesque + Mono + Instrument Serif italic; Archivo width axis + Mono.

## Variance dials (chosen to differ from the last four: 5/2/2, 3/4/4, 4/3/1, 4/5/3)

design_variance 3, visual_density 3, type_temperature 5 (warmest serif register; no run in the last four sat at 5).

## Seasonal Alaska context

Late October. General election November 3rd (open governor's race, ranked choice; early and absentee voting under way). Legislature out of session (interim committee hearings only). PFD paid in October. Freeze-up starting on Interior rivers; fall storm season on the west coast one year after Halong. Railbelt winter peak load approaching; Cook Inlet gas storage injection season ending (Gas Watch shows injection restriction active). AFN convention season. Bering Sea crab and pollock B season closing. Federal fiscal year began October 1st.

## Standing weakness (trend_check --window 10)

```
REPEAT OFFENDERS
  weakest  7/10  mean 7.03   last 7.5    Artwork craft and genuine detail        worked 2026-10-04 (13 run(s) ago)  <-- STALE
  weakest  2/10  mean 7.18   last 7.5    Variety vs ledger                       worked 2026-08-15 (56 run(s) ago)  <-- STALE
  weakest  1/10  mean 7.67   last 7.0    Legibility and platform fitness         worked never (never)  <-- STALE
HARD FAILS: none in this window
DEFECT CLASSES THAT KEEP SHIPPING
   4 run(s)  warns:contact shadow            latest 2026-10-16
   4 run(s)  warns:outside safe zone         latest 2026-10-19
   3 run(s)  warns:top-loaded composition    latest 2026-10-19
   3 run(s)  warns:busy art under text       latest 2026-10-17
   3 run(s)  warns:art touching glyphs       latest 2026-10-17
   3 run(s)  warns:tiny-text                 latest 2026-10-19
SCORES 10-10 8.60  10-11 8.26  10-12 8.62  10-14 8.51  10-15 8.66  10-16 8.79  10-17 8.74  10-19 8.60
```

THE ONE WEAKNESS THIS RUN ATTACKS: Artwork craft (weakest 7 of 10). How: fewer, better-modelled objects. Each frame's largest object gets the best modelling on the frame (named in the CRAFT PLAN before build), mark-making split so no family exceeds three frames, and type reserves designed into the art from the first build (feathered, not boxed) so "busy art under text" and "art touching glyphs" do not need repair rounds. Secondary: the safe-zone and tiny-text warns, killed at dossier time by keeping every label at 24 px or above and inside 80 px margins.
