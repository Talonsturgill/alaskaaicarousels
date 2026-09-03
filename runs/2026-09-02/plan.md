# RUN PLAN — 2026-09-02 — Carousel No. 48

## Wake facts

- Run date 2026-09-02 (Anchorage clock read 23:12 AKDT on September 2nd at wake).
  `runs/2026-09-02/` was free, so the date is not contested.
- carousel_no = 47 topics entries + 1 = **48**.
- Engine bootstrapped clean (playwright, pypdf repaired, chromium ok).
- `prompts/NEXT_RUN.md` does not exist. No queued assignment; story selection is
  this run's own.

## Seasonal Alaska context (for the scouts)

Early September. Legislature out of session, so interim committee work and
BASIS filings only, and zero hearings in `watch.json` is normal. Federal fiscal
year ends September 30th, which is the single strongest seasonal driver right
now: grant obligations, solicitation closes, procurement awards and
end-of-year notices all cluster in the next four weeks. Heating season is
beginning, so Cook Inlet withdrawal restarts and utility filings follow it.
Salmon season post-mortems and escapement counts land now. Arctic sea ice
minimum arrives mid-September. School year has started. State fair closed on
Labor Day. PFD amount announcement and October payment are near. Fire season
winding down.

## Variety constraints (derived from ledger/artwork.json)

FORBIDDEN this run:

- Hero structures of the last 4 (No.44 underlit bench in plan view; No.45 cut
  plate on a tabletop; No.46 spine wall of solids seen straight on; No.47 count
  line of survey markers on muskeg at eye height).
- Atmospheres of the last 3 (north window ten a.m. high key paper; closing-time
  rake single hard lamp; first hour under a high cloud lid, contre-jour).
- Continuity devices of the last 2 (the accession rule and the 2026 slot; the
  station line camera and the doubled station).
- Hook archetypes of the last 3 (the pair nobody joined; the address; the
  counting error). No.44's schema shown in advance is also still close.
- Palette families of the last 3 (buckram/brass/unsewn paper; muskeg and
  galvanized steel; diffuser white on darkroom petrol).
- Type pairings of the last 2 (Instrument Serif + Manrope + JetBrains Mono;
  Archivo + Fraunces + JetBrains Mono).

Four of the last five decks were exterior or tabletop scenes lit by a single
solved key. The open ground is an INTERIOR or a MEDIUM, or a frame with no
single lamp in it at all.

## Variance dials (chosen deliberately, and varied from recent runs)

- design_variance **4** (No.47 ran 3; the standing weakness wants more risk)
- visual_density **4** (deliberately up; see the standing weakness below)
- type_temperature **2** (cool and technical, to buy room for a dense field)

## THE ONE STANDING WEAKNESS THIS RUN ATTACKS

`trend_check --window 10` says it plainly:

    weakest  9/10  mean 6.6  last 7.0  Artwork craft and genuine detail
    6 run(s)  warns:busy art under text        latest 2026-09-01
    6 run(s)  warns:top-loaded composition     latest 2026-09-01

Artwork craft has now been the weakest criterion in nine of the last ten runs
and eleven consecutive runs by the field notes' own count. The named defect has
converged on ONE thing across the last four runs, and No.47's notes state it
outright: **dead zones**. No.47 lost the criterion on slide 05's inert top 40
percent, slide 04's left-third smear and slide 03's empty right-centre quadrant.
The instruction the last four runs have been circling is "fill a dead zone with
the deck's own vocabulary, not with more quiet".

The reason quiet keeps winning is structural, not accidental. The two recurring
machine warns are `busy art under text` and `top-loaded composition`. A run that
gets warned for busy art under text learns to empty the region under the text,
and the region under the text is most of the lower frame, so it empties the
lower frame and gets warned for top-loaded composition, and answers THAT by
quieting the top. Quiet is the fixed point of those two gates played against
each other. That is why five straight runs have scored 7.

**So this run does not attack the dead zone at Phase 8. It removes the ability
to make one, at Phase 5, by choosing a hero structure whose ground is a
CONTINUOUS MEDIUM rather than a lit stage holding objects.** In a medium
(fluid, sediment, ice, a fibre, a gas column) every square inch is by
construction made of the same material at some density, so there is no region
that is "nothing"; density varies, but emptiness is not available. The type
reserve is then earned the same way No.44 earned it, by making the reserve a
MODELLED PART OF THE MEDIUM (a clarified band, a settled layer, a cleared
lane) rather than a plate laid on top of it. That answers `busy art under text`
without answering it with absence.

Concretely, this run commits to:

1. A hero structure that is a medium seen in section or in a column, not a
   stage. Nothing in the last five decks is one.
2. Every dossier must name what the WEAKEST region of its frame carries, in
   the deck's own vocabulary, as a positive element with its own technique
   entry and parameters. A dossier that answers "quiet ground" for that field
   is incomplete and gets rewritten at the storyboard gate.
3. High-density mark fields are NOT labelled in place. Labels live in the
   reserve with a numbered key, which is the idiom No.47 settled on for its
   slides 03 and 06 and which the flow critic endorsed. This is the positive
   statement of `busy art under text`.
4. Real hatching and stipple carry the tonal work rather than gradient fills.
   `bespoke_check` measures drawn share against axis-aligned rects for exactly
   this reason and the technique library's hatching, contour and stipple bench
   has been sitting unused.

## Top instincts injected into every subagent this run (confidence >= 0.7)

1. Never treat a machine_qa PASS as composition approval. qa.py's text
   collision check is DOM-ONLY, so any label against canvas or SVG geometry can
   collide freely and still return PASS with zero warns.
2. A constraint you cannot point at is a constraint you invented. There is no
   context or token budget in this routine.
3. Apply grain as a small repeating tile (AK.grainTile), never a full-frame
   feTurbulence rect.
4. Never nest a colour helper. lerpHex returns rgb(), feeding it back into a hex
   parser yields NaN and canvas silently keeps the previous fillStyle.
5. Load `assets/js/akcolor.js` before `akengrave.js` or it throws.
6. Re-run the dedupe gate whenever the candidate story changes; dedupe_check is
   stateless.
7. A generated gate block pasted into a run record goes stale the moment another
   round runs. Re-sync after every round.

## Craft refresh (Phase 1)

Two searches spent. One finding worth carrying, hedged as marketing-blog
sourcing rather than platform documentation, in the 2026-09-02 FIELD_NOTES
entry. Nothing goes into the doctrine files during a run.

## Docket watch queue at wake

`ledger/watch.json` for 2026-09-02: zero bills, zero hearings (normal, the
Legislature is out), one candidate (an Alaska Energy Authority non-capacity
licence amendment at FERC, doc 2026-15691), and **`failed` is non-empty**:
`basis-bills` returned HTTP 503. That goes in the ship note per Phase 3.5 step
0, because an empty bills list after a failed sweep is a broken collector
wearing the costume of a quiet day.
