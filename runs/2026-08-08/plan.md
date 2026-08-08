# RUN PLAN — 2026-08-08 — Carousel No. 29

## RUN DATE, and why it is not the Anchorage date

The trigger fired at 07:13 UTC, which is 23:13 AKDT on August 7th. The
Anchorage calendar date is therefore 2026-08-07, and `runs/2026-08-07/`
already holds a shipped deck (No.28, merged this morning at 01:56 AKDT).
Reusing that date would overwrite shipped run artifacts, which CLAUDE.md
forbids without asking. This run takes **2026-08-08**, the date it will be
in Anchorage within the hour and the date every prior run has occupied in
sequence. Every gate, path and URL in this run uses 2026-08-08.

## CAROUSEL NUMBER

ledger/topics.json holds 28 entries. carousel_no = **29**.

## QUEUED ASSIGNMENT (Phase 0 step 0)

`prompts/NEXT_RUN.md` exists. It was written by the 2026-08-07 showrunner,
NOT by the maintainer, and it says so itself: a strong runner-up handed
forward, to be overridden freely if this run's own sweep turns up something
better. Default story is the Sitka Tribe of Alaska's AI video escapement
counter at Redoubt Falls. It carries four explicit traps, all of which bind:

1. The dedupe problem is the hard part. No.2 (Wood River drone counting,
   thesis VALIDATION) and No.9 (Nalaquq Quinhagak, thesis OWNERSHIP) are
   both in the 30-day window. Neither thesis may be written again.
2. The available thesis is RATIONING: the escapement count sets a household
   subsistence limit, and the instrument that produces it has no committed
   funding.
3. The two accuracy numbers (a director's loose "about a 95% confidence
   interval" in an interview, and SalmonVision's published 80.2 percent mean
   average precision) measure different things. Averaging, comparing or
   implying either validates the other is a hard fail.
4. A 2026 Redoubt count near 229,000 sockeye appears in search snippets only
   and must not ship. The USFWS grant amount is unknown and must not be
   invented.

Beat B was assigned to re-verify it and to hunt the missing primary
(ADF&G / USFWS / Sitka Tribe on the weir program and its funding). The five
other beats sweep normally. Selection is made in Phase 4 on the merits.

At ship: `git mv prompts/NEXT_RUN.md runs/2026-08-08/next_run_brief.md`.

## TOP INSTINCTS INJECTED THIS RUN (confidence >= 0.7)

1. (0.99) Grain is a small repeating tile (AK.grainTile), never a full-frame
   feTurbulence rect.
2. (0.99) A machine_qa PASS is never composition approval. qa.py's text
   collision check is DOM-ONLY; any label against Canvas or SVG geometry can
   collide freely and still return PASS with zero warns. Every art-band label
   ships on an opaque knockout plate by default.
3. (0.99) A GENERATED GATE BLOCK GOES STALE THE MOMENT ANOTHER ROUND RUNS.
   Re-sync with `gate_status.py --sync` after EVERY round that changes an
   artifact, not once. Confirmed twice, on 2026-08-05 and 2026-08-07.
4. (0.97) Never nest a colour helper. lerpHex returns an rgb() string, so
   nesting feeds rgb(...) into a hex parser, every channel is NaN, canvas
   silently keeps the previous fillStyle, and a region renders the wrong
   colour with a clean gate. Precompute endpoints as hex literals.
5. (0.95) Size every plate from the MEASURED string. JetBrains Mono at 24px
   with 0.10em tracking advances exactly 16.8px per character; the eye
   estimates about 14, and a hand-sized plate loses about 3 characters per 20.
6. (0.95) AKPOST.grade costs ~34 seconds on a 2D canvas that has already had
   a WebGL canvas composited into it, and ~0.9s before that composite. Grade
   the 2D atmosphere FIRST, then composite the GL render on top.
7. (0.95) Never read dedupe_check.py output with head or tail. Read all of it.

## VARIETY CONSTRAINTS DERIVED FROM ledger/artwork.json

FORBIDDEN hero structures (last 4, No.25 to No.28):
  THE HEAD SHEET, THE OPEN BLOCK, THE TRAVERSE, THE UNBOUNDED POPULATION.
  Note THE CUT BLOCK (No.24) is one step outside the window but four of the
  last five heroes are a rigid manufactured object under a fixed or nearly
  fixed camera. A fifth is a variety failure in spirit even where the letter
  allows it. The brief says the same thing independently.

FORBIDDEN atmospheres (last 3): BINDERY AIR, BURNER BLUE AT ALTITUDE,
  REPLY AS KEY LIGHT.

FORBIDDEN continuity devices (last 2): THE TRAVERSE LOG, THE PHANTOM
  SEGMENT, THE HOLLOW FIGURE and No.28's second device.

FORBIDDEN hook archetypes (last 3): THE ANSWERED OBJECTION, THE SCALE SHOCK,
  THE SILENT MAJORITY.

FORBIDDEN palette families (last 3): OFFSET STOCK AND BUCKRAM, METHANE FLAME
  AND DIESEL LAMP, CARD STOCK AND VOID.

FORBIDDEN type pairings (last 2): Fraunces + Archivo + JetBrains Mono,
  Fraunces + Manrope + JetBrains Mono. **Fraunces is out this run.**

## VARIANCE DIALS

design_variance **5**, visual_density **3**, type_temperature **4**.

Deliberately different from the last three runs (4/4/3, 4/3/2, 4/3/2). Dial
the design variance to its ceiling because the standing weakness below is a
craft problem that four consecutive runs have tried to solve inside a
conservative envelope and have not solved. Hold density at 3 so the extra
variance buys depth rather than clutter, since three of the last three runs
shipped "busy art under text" and "art touching glyphs" warns.

## SEASONAL ALASKA CONTEXT

Alaska state primary election **August 18th**, ten days out, so elections
administration, candidate filings and ballot questions are live. Peak salmon
season, Southeast pink and coho running, Bristol Bay winding down. Wildfire
season. Legislature in interim. Caribou hunts open August 10th, moose
September 1st. Arctic sea ice heading to its September minimum. Cruise season
at peak and the friction that brings in Juneau and Sitka. School starts
mid-August. Federal fiscal year ends September 30th, so solicitations and
grant deadlines cluster now.

## TREND — generated by scripts/trend_check.py --window 10, 2026-07-29 to 2026-08-07

```
REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  weakest  7/10  mean 6.0    last 7.0    Artwork craft and genuine detail   worked 2026-08-07 (0 run(s) ago)
  weakest  2/10  mean 6.17   last 8.0    Legibility and platform fitness    worked never  <-- STALE
  weakest  1/10  mean 6.0    last 6.0    Legibility & platform fitness      worked never  <-- STALE

HARD FAILS (2 of 10 run(s) carried one)
   2x  text against geometry       2026-07-29, 2026-07-31  <-- RECURRING
   1x  contrast                    2026-07-31

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   6 run(s)  warns:top-loaded composition        latest 2026-08-07
   4 run(s)  warns:outside safe zone             latest 2026-08-07
   3 run(s)  warns:busy art under text           latest 2026-08-07
   3 run(s)  warns:art touching glyphs           latest 2026-08-07
   2 run(s)  warns:text collision                latest 2026-08-06

SCORE, most recent runs
  07-31 6.90  08-01 7.92  08-02 8.37  08-03 6.90  08-04 7.25  08-05 7.27  08-06 7.93  08-07 8.55
```

## THE ONE STANDING WEAKNESS THIS RUN IS ATTACKING, AND HOW

**Artwork craft and genuine detail**, weakest in 7 of the last 10 runs at a
mean of 6.0. It has been worked on repeatedly and it keeps coming back, so
the useful question is not whether to attack it but which specific failure
inside it to attack, and there is a precise one on the record.

No.28's own shortfall field names it: *RENDERED LADDER DECLARED AND NOT
REACHED* on its hero, akthree GPU PBR argued at length in the dossier and a
Canvas 2D fallback shipped. It says **fourth deck in six** and lists No.23,
No.24 and No.26. The scorer's one_sentence_fix for that deck was to build the
hero on the ladder for real. DESIGN_DOCTRINE section 4 calls a rendered hero
with a graded finish the craft floor, and this machine has been writing that
sentence into dossiers and then not executing it two runs out of three.

**The attack: the hero slide reaches a real rung of the rendered ladder and
is verified to have done so before any critic sees it.** Concretely:

1. The hero is built on **aksdf (CPU raymarch, #88)** rather than akthree,
   chosen deliberately. akthree is the rung that keeps getting declared and
   dropped, and the reason is structural: it needs a live GL context in a
   headless build, so the fallback path is always sitting right there and
   always wins under time pressure. aksdf raymarches on the CPU, so there is
   no context to fail and no fallback to fall into. It either renders or it
   errors, which is exactly the property this failure mode has been missing.
   If the story's form genuinely suits akthree better, akthree is allowed,
   but then the akthree snapshot sentinel is checked and reported as evidence
   in the run record, not asserted.
2. The dossier declares the rung AND the evidence that will prove it: which
   file, which sentinel, which measured value. A declaration with no evidence
   line is what four decks shipped.
3. **AKPOST.grade runs on the 2D atmosphere BEFORE any GL or raymarch
   composite** (instinct 6), because the 34-second cost is what actually
   forced two of those fallbacks.
4. Drawn share target **65 percent** against bespoke_check's 45 percent floor.
   No.27 targeted 70 and hit 61, so 65 is the honest target, and it is stated
   here so the retro can grade it rather than discovering it.

Secondary, and cheap: the six-run **top-loaded composition** warn. It is
handled at Phase 5 by dossier field 4a, the lower-third treatment, which
`dossier_check.py` now gates. Every dossier names what its bottom band
carries and names something with modeled tone, not a plate and not a
hairline. This costs one paragraph per slide here and cannot be bought back
at Phase 9.

## PHASES

Phase 0 wake done. Six scouts spawned in parallel on beats A through F.
