# PLAN — 2026-11-13 — Carousel No.114

Effort in effect: medium (CLAUDE_EFFORT=medium). The repo setting carries high; this run's session reported medium, so the setting did not take for this session. Disclosed here and in the Gmail editor notes.

Date note: woke 21:04 AKST November 13th (UTC already November 14th). Anchorage date CLEAR, used as run date.

## Top 5 instincts (injected into every subagent brief)
1. (0.99, confirmed 2026-09-26) A GENERATED BLOCK PASTED INTO A RUN RECORD GOES STALE THE MOMENT ANOTHER ROUND RUNS. gate_status.py prints 'do not hand-write these lines' and run 2026-08-05 pasted it once, then rendered four more times, and the scorer caught the block contradicting the shipped artifacts on four rows. Regenerate it at the LAST render, not the first. CONFIRMED 2026-08-07: the block was pasted after the critic round, a third revision round then ran, and the scorer found it reporting 29 qa warns and 'score_report.json missing' on a deck that measured 20 and had scored. The pasted-block verifier only runs at the completion gate, which is AFTER the last chance to be wrong about it in a subagent's eyes.

2. (0.99, confirmed 2026-09-26) AK.grainTile RETURNS A DATA URL, NOT A CANVAS. Passing it to createPattern throws, the page errors, and the slide produces NO PNG AT ALL, which is a hard render failure rather than a warning. It is documented for a repeating CSS background on a DOM div at mix-blend-mode overlay and opacity 0.05 to 0.12, which is also how the demo deck uses it. Grain is a DOM layer over the graded art canvas, never a canvas fill.

3. (0.99, confirmed 2026-07-21) Never treat a machine_qa PASS as composition approval; the pixel critics judge composition, hierarchy, and collision at full size and thumb size.

4. (0.99, confirmed 2026-07-21) Before rendering, sanity-check long serif/body copy line counts against any fixed-position labels, bars, or plates; DOM text overlaps pass machine QA but fail the eye.

5. (0.99, confirmed 2026-07-18) Apply grain as a small repeating tile (AK.grainTile), never a full-frame feTurbulence rect.

## Variety constraints (forbidden)
FORBIDDEN hero_structure (last 4):
  - 2026-11-09 NEW: THE DOLLAR WEB, every Year 1 award as one thermoformed blister web on a shelf rail at one scale (pocket length = dollars), read as an itemised receipt: an axonometric 254-pocket card (01), the seven AI pockets end to end on a ledge ove
  - 2026-11-10 NEW: THE PROJECTED SAND TABLE, a damp-sand terrain model of the real Houston DEM (2.5x vertical, 1:10,000) in an oak tray, the July 19,500-acre outline projected onto it as cool light and the conveyed 6,800 acres staked as one gold cord on 
  - 2026-11-11 NEW: THE PRICE AS LIGHT PILLARS, the STAK surcharge schedule drawn as five ice-crystal light pillars standing on the snow west of the Dalton (width = MWh in the tier at 44 px per million, height = the rate at 10 px per cent, gold hairline c
  - 2026-11-12 NEW: THE INSTRUMENT NICHE, a frontal bodegon window niche with one instrument of checking per frame, each aimed at an absence, on one Southeast slate sill scanned end to end: a GPU nickel reading lens magnifying an empty gold blank (01), en
FORBIDDEN atmosphere (last 3):
  - 2026-11-10 NEW: GRAZING WORK LAMP AND CEILING PROJECTOR IN A DARK MAP ROOM (tungsten lamp az 305, el 20, never moves; projector cool on 01 to 04 and 06, off on 05, 07 and 09)
  - 2026-11-11 NEW: ARCTIC TWILIGHT INTO AURORA NIGHT ON ONE PLAIN (one SSW key, low; rose belt on 01 and 02, deep blue hour 03 to 06, nautical dark 07 and 08, aurora on 09)
  - 2026-11-12 NEW: A RUN OF TALL WINDOWS BEHIND CAMERA LEFT ON A NIGHT NICHE (pale #FFE2B8 key at about 35 degrees, cool #142338 bounce, the key a smooth function of global x with mullion bars on the sill top; peak on 05, a stone pier's shade on 07)
FORBIDDEN continuity_device (last 2):
  - 2026-11-11 motif evolution: the five light pillars, from lit on the plain (01) to alone as a level (03), a zero line (04), measured (05), small and far (06), pools in plan (07), absent behind 20 stakes (08) and faint under the aurora (09)
  - 2026-11-12 motif evolution: the gold line where a number belongs, empty (01, 02, 07), filled (03, 04, 06, 08), measured (05), focused (09)
FORBIDDEN hook_archetype (last 3):
  - 2026-11-10 NEW: THE MAP THAT SHRANK AND THE QUESTION THAT DID NOT
  - 2026-11-11 NEW: THE PRICE THAT FALLS AS THE BUYER GROWS
  - 2026-11-12 NEW: THE RECORD'S OWN WORDS, IN QUOTES
FORBIDDEN palette_family (last 3):
  - 2026-11-10 NEW: DAMP SAND, OAK RAIL AND WOOL UNDER A COOL PROJECTOR (room #070D18, sand #CDBB97, oak #5A3B22, wool #4C7FBF, projector #DCE7F2, basswood #D9C7A3, gold #FFC72C for the land conveyed)
  - 2026-11-11 NEW: ARCTIC BLUE HOUR AND ICE LIGHT (sky #0B1A3A to #2B3F6E, rose belt #C79A9E, snow #CFDAEC / #8E9FC0 / #4C5E86 / #26355A, ice #BFE3F2, aurora #3CE6B4, forget-me-not #6EA5FF for Alaska's output, gold #FFC72C for the lease's price)
  - 2026-11-12 NEW: BODEGON NIGHT, SLATE, BONE AND EBONY (void #04070F, slate #141C26 / #2B3642 / #5E6B78, quartz #C9CFD3, bone #EFE6D4, ebony #16110E to #4A3B30, nickel #D7DCE0, ivory #E6DCC6, vial #9FD9C0, gold #FFC72C for the line where a number belong
FORBIDDEN type_pairing (last 2):
  - 2026-11-11 Space Grotesk 680 display + Space Grotesk 400 body + JetBrains Mono 500 caps
  - 2026-11-12 Instrument Serif 400 display + Bricolage Grotesque 430 body (opsz 36, wdth 90) + JetBrains Mono 500 caps

## Variance dials this run
design_variance 4, visual_density 5, type_temperature 2 (density 5 unused in the last six; temperature 2 last used 11-08).

## Seasonal Alaska context
- Mid-November: freeze-up, short days (Anchorage about 7 hours of daylight), Cook Inlet gas winter draw season begins; CINGSA injection restriction active per Gas Watch.
- November 3rd general election just held: governor (open seat), U.S. Senate, U.S. House, legislature; ranked-choice tabulation lands around November 18th. Legislature convenes January 2027; bill prefiling opens in January.
- Fall Board of Fisheries cycle; North Pacific Fishery Management Council December meeting ahead; federal FY27 appropriations; BOEM/NPR-A lease activity; RCA dockets on Railbelt reliability.

## Trend check (standing weakness)
```
TREND -- generated by scripts/trend_check.py over the last 10 scored run(s), 2026-11-03 to 2026-11-12.

REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  'worked' is a text match over ledger/upgrades.json prose, so it can UNDER-report:
  an upgrade that fixed a criterion without naming it reads as 'never'. Check before acting.
  weakest  7/10  mean 7.1    last 7.0    Artwork craft and genuine detail        worked 2026-11-11 (1 run(s) ago)
  weakest  1/10  mean 7.4    last 7.5    Variety vs ledger                       worked 2026-11-01 (11 run(s) ago)  <-- STALE
  weakest  1/10  mean 7.55   last 7.0    Thumb-stop cover                        worked 2026-10-21 (21 run(s) ago)  <-- STALE
  weakest  1/10  mean 7.8    last 8.0    Insight density and factual weight      worked 2026-09-06 (61 run(s) ago)  <-- STALE

HARD FAILS (0 of 10 run(s) carried one)
  none in this window

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   4 run(s)  warns:tiny-text                                       latest 2026-11-10
   4 run(s)  warns:busy art under text                             latest 2026-11-12
   4 run(s)  warns:contact shadow                                  latest 2026-11-11
   4 run(s)  warns:axis census                                     latest 2026-11-10
   3 run(s)  warns:ragged display line                             latest 2026-11-06
   3 run(s)  warns:outside safe zone                               latest 2026-11-10

SCORE, most recent runs
  11-05 8.25  11-06 8.35  11-07 8.44  11-08 8.45  11-09 8.51  11-10 8.73  11-11 8.57  11-12 8.36
```

## The ONE standing weakness this run attacks
Artwork craft (weakest 7 of 10, mean 7.1). Attack: fewer, larger, fully modelled objects per frame; the largest object on each frame is the one with the most modelling (material, contact shadow, edge light), named in the CRAFT PLAN before code; busy art under text is fenced with a measured quiet zone behind every text block; no tiny text below the engine minimum. Weekly theme (largest object least modelled, texture artifact) is the brief.
