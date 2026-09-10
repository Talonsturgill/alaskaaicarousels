# RUN PLAN — 2026-09-10 — Carousel No. 55

## Wake state
- carousel_no = 55 (54 entries in ledger/topics.json)
- run date free: runs/ holds through 2026-09-09, nothing at 2026-09-10
- prompts/NEXT_RUN.md: absent. No queued assignment. Story selection is this run's own.
- .claude/WORKLOG.md: absent.
- Branch: claude/carousel-2026-09-10 off main at d01d09a.

## Variety constraints (derived from ledger/artwork.json, 54 entries)

FORBIDDEN HERO STRUCTURES (last 4: 09-05, 09-06, 09-07, 09-09)
- the retention sheet (one absorbent sheet at nine declared magnifications)
- the waterline as progress meter (one water body read at nine depths)
- the curved transect as a camera move (one geodesic crawled across nine frames)
- the stamped field and the printed page (alternating struck steel and printed page)

FORBIDDEN ATMOSPHERES (last 3)
- downwelling key at elevation 76 through particulate
- terminator graze, key at az 142 el 4
- sodium lamp and galvanized steel, low warm key from lower right az 118 el 34

FORBIDDEN CONTINUITY DEVICES (last 2)
- the four-device rail (t/mileage readout, arc state, coordinate string, column alternation)
- the gold datum holding y=900 across all frames

FORBIDDEN HOOK ARCHETYPES (last 3)
- the bill nobody has priced
- the search that returns two answers
- the sentence that isn't there

FORBIDDEN PALETTE FAMILIES (last 3)
- diatom green and wet steel
- terminator blue and limestone
- sodium-zinc

FORBIDDEN TYPE PAIRINGS (last 2)
- Unbounded + Manrope + JetBrains Mono
- Fraunces + Space Grotesk + JetBrains Mono

## Variance dials (chosen deliberately, varied from recent runs)
- design_variance: 4
- visual_density: 3
- type_temperature: 2

Reasoning. The last four decks all ran a single continuous object or field across
nine frames (sheet, water column, geodesic, alternating pair). That is a high
design_variance idea executed as a low-variance sequence, and it is exactly the
shape the artwork-craft criterion keeps punishing: nine frames that share one
drawing problem, so nine frames share one drawing weakness. Dial 4 here means
each frame gets its own composition problem, and the continuity is carried by a
motif rather than by a camera. visual_density 3 is a deliberate step DOWN from
the recent decks: the standing warn list is led by "busy art under text" (5 of
10 runs) and "canvas mark near reserved text" (4 of 10). Less ink in the type
bands is the cheapest structural fix available. type_temperature 2 keeps the
type cool and instrumental so the warmth in the frame is the artwork's alone.

## STANDING WEAKNESS — the one thing this run attacks

`scripts/trend_check.py --window 10` (2026-08-30 to 2026-09-09):

```
REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  weakest  7/10  mean 6.8    last 6.0    Artwork craft and genuine detail        worked 2026-08-31 (8 runs ago)  <-- STALE
  weakest  2/10  mean 7.6    last 8.0    Deliverable completeness                worked never  <-- STALE
  weakest  1/10  mean 6.7    last 7.0    Legibility and platform fitness         worked never  <-- STALE

HARD FAILS (0 of 10 runs carried one)
  none in this window

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   5 runs  warns:busy art under text            latest 2026-09-09
   5 runs  warns:top-loaded composition         latest 2026-09-07
   4 runs  warns:contact shadow                 latest 2026-09-09
   4 runs  warns:canvas mark near reserved text latest 2026-09-09
   3 runs  warns:outside safe zone              latest 2026-09-06
   3 runs  warns:art touching glyphs            latest 2026-09-09

SCORE, most recent runs
  09-01 8.89  09-02 8.52  09-03 8.81  09-04 8.76  09-05 8.77  09-06 8.08  09-07 9.07  09-09 8.47
```

THE ONE WEAKNESS THIS RUN ATTACKS: **Artwork craft and genuine detail**, weakest
in 7 of the last 10 runs, mean 6.8, and 6.0 on the most recent scored run, which
is the lowest figure on the board. It has not been worked in 8 runs.

Read as a prediction rather than a report: unless this run does something
different, today's deck scores about 6.8 on artwork craft too.

HOW, and it is a planning decision made here and not a repair at Phase 9. The
three warn classes that keep shipping (busy art under text, canvas mark near
reserved text, art touching glyphs) are all the SAME defect, which is art and
type competing for the same pixels. Four runs have answered it by muting art
under the type after the fact, which is what produces a flat, thin lower zone and
is precisely what the artwork-craft criterion then marks down. The inverse is the
fix and it belongs in the dossiers:

1. **The type sits in a hole the artwork CUTS, not on a plate laid over it.**
   Every type block's reserve is a subtraction the drawing performs (a scraped
   band, a masked-out trough, a cut-through window with its own edge treatment),
   so the reserve is itself drawn detail rather than an absence of detail. That
   converts the deck's most-punished region into its most-crafted one.
2. **Each frame's detail budget is spent where the eye lands second.** The warn
   list says the recent decks are top-loaded (5 of 10). Every dossier this run
   names ONE lower-third feature carrying modeled tone, per dossier_check field
   4a, and it is a feature of the artwork rather than a caption or a plate.
3. **Nine compositions, not one composition nine times.** Per the dials above,
   the continuity is a motif and a palette, never a shared camera. bespoke_check
   measures this; the point here is to plan for it rather than to pass it.

## Seasonal Alaska context (for the scouts)
- September 10th, 2026. Freeze-up approaching Interior and North Slope; heating
  season begins, which is the live end of the Cook Inlet gas question.
- Legislature OUT of session (returns January). BASIS hearings sparse; this is
  normal June to December and is not a dead collector.
- Municipal elections October 6th, 2026 statewide (Fairbanks North Star Borough
  Proposition 3 already shipped as No.48 on 09-02, hard dedupe risk).
- PFD: 2026 distribution season, amount announcement and October payment window.
- Fall subsistence and moose seasons; fisheries post-season assessment surveys.
- Wildfire season closing out; state fire assessment reporting.
- Federal fiscal year ends September 30th, so procurement, solicitation and
  obligation activity spikes in this exact window. Beat D should look hard here.
- School year underway (district AI policies, UA fall semester).

## Dedupe watch list (last 30 days, do not repeat)
Permafrost Discovery Gateway lake tracker (08-28), Chukchi acoustic glider
(08-29), Rural Health Transformation awards (08-30), FCC USF notices (08-31),
FNSB Assembly Resolution 2026-25 (09-01), FNSB Proposition 3 hand count (09-02),
Navy SPECWAR building (09-03), DNR Houston land conveyance (09-04), Anthropic
employee political giving (09-05), NOAA Fisheries survey framework (09-06),
FPDS-NG Alaska vendor searches (09-07), EO 14421 / 91 FR 55995 reliability
standards (09-09).

Note the density of federal-register and procurement stories in the last two
weeks. A fourth one in a fortnight is a genuine variety problem even when it
clears the dedupe gate, so a non-federal-document story is preferred today
unless the federal one is decisively stronger.

## Instincts injected into every subagent this run (confidence >= 0.7, top 5)
1. Apply grain as a small repeating tile (AK.grainTile), never a full-frame
   feTurbulence rect. (0.99)
2. Never treat a machine_qa PASS as composition approval; the pixel critics
   judge composition, hierarchy and collision at full size and at thumb size.
   (0.99)
3. Before rendering, sanity-check long serif/body copy line counts against any
   fixed-position labels, bars or plates; DOM text overlaps pass machine QA and
   fail the eye. (0.99)
4. A generated block pasted into a run record goes stale the moment another
   round runs. Regenerate it with `gate_status.py --sync` after every round.
   (0.99)
5. A constraint you can't point at is a constraint you invented. This routine
   has no context budget and no token budget. Nothing measures one. (0.99)

Plus two the art build can't afford to relearn:
- qa.py's text-collision check is DOM-ONLY, so a label against Canvas or SVG
  geometry can collide freely and the gate still returns PASS. (0.98)
- A lit ground is SCREENED over the surface and the cast is an ATTACHED
  subtraction thrown down-light. A radial pool centred on the object's own base
  puts the brightest and darkest values concentrically, which is the hole in a
  spotlight. (0.98)
