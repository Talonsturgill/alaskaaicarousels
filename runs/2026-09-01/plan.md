# RUN PLAN — Alaska.Ai Carousel No. 47 — 2026-09-01

## Wake

- Run date 2026-09-01. Woke 23:13 AKDT on September 1st; `runs/2026-09-01/` did
  not exist, so the Anchorage calendar date is the run date. No collision.
- carousel_no = 46 topics ledger entries + 1 = **47**.
- `prompts/NEXT_RUN.md` does not exist. No queued assignment. No `.claude/WORKLOG.md`.
- Bootstrap clean (playwright, pypdf repaired, chromium ok).

## Top instincts injected into every subagent this run

1. Never read a machine_qa PASS as composition approval. qa.py's text-collision
   check is DOM-only, so any label set against canvas or SVG geometry can
   collide freely and the gate still returns PASS with zero warns.
2. Grain is a small repeating tile (AK.grainTile), never a full-frame
   feTurbulence rect.
3. Sanity-check long body-copy line counts against fixed-position labels, bars
   and plates BEFORE rendering. DOM text overlaps pass machine QA and fail the eye.
4. A generated gate block pasted into the run record goes stale the moment
   another round runs. Re-sync at the LAST render, every round.
5. There is no context budget, no token budget and no remaining-budget gate.
   A constraint you can't point at is a constraint you invented.
6. Load `akcolor.js` before `akengrave.js` or it throws "AKC is not defined".
7. Re-run the dedupe gate whenever the candidate story changes.

## Variety constraints, derived from ledger/artwork.json

FORBIDDEN this run:

- **Hero structures (last 4).** No.43's drain scar and datum board (seeded
  terrain walked across, a prop carrying all type). No.44's underlit bench
  (interior in plan view, key light under the reading surface). No.45's cut
  plate (a sheet of rag paper on a table with boroughs excised and lifted).
  No.46's spine wall (a vertical face of solids seen straight on, no surface).
- **Atmospheres (last 3).** No.44's underlit 02:00 dark review room. No.45's
  north window 10 a.m. high-key paper white. No.46's closing-time rake (one
  hard lamp above and in front, no daylight, dust in the beam).
- **Continuity devices (last 2).** No.45's CUT / SCREEN / PHANTOM fabrication
  distinction. No.46's accession rule and the 2026 slot (a time device panning
  one window per swipe, future ticks never drawn).
- **Hook archetypes (last 3).** No.44's schema shown in advance. No.45's
  address. No.46's pair nobody joined.
- **Palette families (last 3).** Diffuser white on darkroom petrol. High-key
  paper white under a north window. Buckram, brass and unsewn paper.
- **Type pairings (last 2).** Fraunces + Space Grotesk + JetBrains Mono.
  Instrument Serif + Manrope + JetBrains Mono.

Note the shape of the last four decks read together: three of them put the
camera on or over a horizontal working surface and the fourth put it square on
to a wall. All four were INTERIOR or table-top. The cheapest real divergence
available is a deck whose subject has no table under it at all.

## Variance dials, chosen deliberately

- `design_variance` **4** (No.46 ran conservative in structure and scored 7.79)
- `visual_density` **2** — deliberately LOW, and this is the run's main lever
  against its standing weakness, see below
- `type_temperature` **3**

The dials themselves diverge from the recent pattern of pushing density up to
buy detail. Density is not detail. That is the thesis of this run's plan.

## THE STANDING WEAKNESS THIS RUN ATTACKS

`scripts/trend_check.py --window 10` over 2026-08-19 to 2026-08-31:

```
REPEAT OFFENDERS (criterion, times weakest, mean, last worked on)
  weakest  9/10  mean 6.55   last 6.0    Artwork craft and genuine detail   worked 2026-08-31 (0 runs ago)
  weakest  1/10  mean 7.6    last 7.0    Story arc and swipe momentum       worked 2026-07-30 (26 runs ago)  <-- STALE

HARD FAILS (0 of 10 runs carried one)
  none in this window

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   5 runs  warns:busy art under text        latest 2026-08-31
   5 runs  warns:top-loaded composition     latest 2026-08-31
   3 runs  warns:tiny-text                  latest 2026-08-31
   3 runs  warns:outside safe zone          latest 2026-08-29
   3 runs  warns:contact shadow             latest 2026-08-31
   2 runs  warns:art touching glyphs        latest 2026-08-27

SCORE, most recent runs
  08-21 8.54  08-25 8.66  08-26 8.51  08-27 8.67  08-28 7.93  08-29 8.51  08-30 8.79  08-31 7.79
```

**The one weakness this run attacks: Artwork craft and genuine detail.**

Read as a prediction rather than a report, it says today's deck scores about
6.5 on artwork unless something changes, and the two defect classes riding
alongside it name the mechanism. "Busy art under text" and "top-loaded
composition" have each shipped in five of ten runs. They are not two defects.
They are one: the art is designed to fill the frame, the type then has to go
somewhere, the only clear region is the top, and whatever the type lands on is
busier than type wants.

Recent runs answered that by adding machinery, and No.46's own Phase 12 note
records the cost, seven rounds spent on contact shadows and type reflow while
its worst shipped defect was a type reserve erasing two of eight declared
leaves. The reserve grew to protect type from art that should not have been
under the type in the first place.

**So this run's move is subtractive, and it is a planning move, not a repair
move.** Three commitments, written here so Phase 5 has to honor them and Phase
8 is not where they get discovered:

1. **The type reserve is a MODELLED VOID, planned in the dossier, and it is
   the bottom third or a full side column on every slide.** Not a plate laid
   over art. The art is composed to stop at that boundary, so there is nothing
   under the type to be busy. If a dossier cannot say what the reserve IS as a
   physical thing in the scene, the dossier is not done.
2. **Detail is spent where the eye lands, not spread evenly.** One region per
   slide carries genuine material resolution and the rest of the frame is
   allowed to be quiet. `visual_density` 2 is the budget that forces the
   choice. A quiet region is not an undrawn region; it is a region drawn with
   fewer, larger, better marks.
3. **No slide is top-loaded, by construction.** The heaviest mass sits below
   the horizontal midline on at least seven of nine frames, which is only
   possible if the reserve is at the bottom and the subject sits IN it rather
   than above it.

Story arc reads as stale in the report at 26 runs since it was last worked, but
it has been the weakest criterion once in ten and means 7.6. It is not this
run's target. Named here so the deferral is not silent.

## Seasonal Alaska context for the scouts

Early September. The Legislature is out of session and returns in January, so a
bill's status changes only through interim committee work and BASIS filings,
and zero scheduled hearings is normal rather than a failed sweep. Salmon
seasons are closing out and the Bering Sea groundfish and crab picture for the
coming year is being set. Freeze-up is six to ten weeks out and the utilities'
winter gas position is the live question in Southcentral. The Alaska State Fair
in Palmer runs through Labor Day. School and university terms have just
started, so UAF and UAA research announcements cluster now. Fall subsistence
and general hunting seasons are open, which puts aviation, search and rescue
and remote connectivity in the news. Federal fiscal year ends September 30th,
which is the single strongest seasonal signal available today: agency
obligations, grant awards, solicitation closes and end-of-year procurement all
pile into the last four weeks, and several already-tracked docket items carry
September 30th dates. PFD distribution is early October, and the fall borough
and municipal assembly cycle has resumed.

## Search budget discipline

Six scouts, each capped at 25 WebSearch calls, then WebFetch only, and the cap
is stated in every brief with its reason. Phase 1 spent 3 searches before the
scouts, per the ordering rule. That leaves headroom for Phase 3's verification,
Phase 3.5's docket refresh and Phase 12's frontier scan, which recorded ZERO
available searches on four separate runs in August.
