# RUN PLAN — Alaska.Ai Carousel No. 54 — 2026-09-09

## Wake

- Run date 2026-09-09 (America/Anchorage). `runs/2026-09-09/` did not exist at
  wake, so the run takes today. Note for the record: there is no
  `runs/2026-09-08/`, so no deck shipped on the 8th; the last shipped deck is
  No.53 on 2026-09-07. This run does NOT backfill the 8th. The standing rule
  says take the first free date and today is free.
- carousel_no = 54 (53 entries in ledger/topics.json + 1).
- `prompts/NEXT_RUN.md` does not exist. No queued assignment.
- Working tree clean at wake, branch `tsturg/wonderful-maxwell-r1lccr`, level
  with `origin/main` at 98e8bb6.
- bootstrap.sh: complete. pypdf import needed its documented repair; chromium ok.

## Top instincts injected into every subagent this run

1. A machine_qa PASS is not composition approval. qa.py's text-collision check
   is DOM-ONLY, so any label set against Canvas or SVG geometry can collide
   freely and the gate still returns PASS with zero warns.
2. A lit ground is SCREENED over the surface, never painted on it, and the cast
   is an ATTACHED subtraction thrown down-light. A radial pool centred on an
   object's own base puts the brightest and darkest values concentrically, which
   is a hole in a spotlight rather than a contact.
3. A generated block pasted into the run record goes stale the moment another
   round runs. Regenerate with `gate_status.py --sync` after every round.
4. A change made to answer a critic is a change like any other. Round N+1's hard
   fails are frequently round N's own repairs. Re-render and re-read every frame
   you touch.
5. A constraint you cannot point at is a constraint you invented. There is no
   context or token budget in this routine. If the work feels expensive, write
   the next slide.

## Variety constraints derived from ledger/artwork.json

FORBIDDEN this run:

- hero structures (last 4): THE CURVED TRANSECT AS A CAMERA MOVE (No.53), THE
  WATERLINE AS PROGRESS METER (No.52), THE RETENTION SHEET (No.51), THE RULED
  WORLD AND THE UNRULED ONE (No.50).
- atmospheres (last 3): TERMINATOR GRAZE AZ 142 EL 4 (No.53), DOWNWELLING KEY AT
  ELEVATION 76 THROUGH PARTICULATE (No.52), COAXIAL READ ON DAMP RAG (No.51).
- continuity devices (last 2): the four-device instrument rail plus arc-state
  (No.53), THE FIVE STRAND SHOT LINE THROUGH SIX STATES (No.52).
- hook archetypes (last 3): THE SEARCH THAT RETURNS TWO ANSWERS (No.53), THE
  BILL NOBODY HAS PRICED (No.52), THE MATCH THAT TAKES 105 PEOPLE (No.51).
- palette families (last 3): terminator blue and limestone (No.53), diatom green
  and wet steel (No.52), peat and mineral (No.51).
- type pairings (last 2): Unbounded + Manrope + JetBrains Mono (No.53),
  Instrument Serif + Archivo + JetBrains Mono (No.52).

VARIANCE DIALS THIS RUN: design_variance 3, visual_density 4,
type_temperature 5.

Chosen deliberately against the recent record rather than by taste. The last
eight runs read 4/3/5, 4/2/3, 4/4/2, 5/3/4, 4/3/2, 3/5/5, 5/2/3, 4/2/2, which is
a machine that has been reaching for structural novelty (design_variance 4 and 5
in seven of eight) while running THIN (visual_density 2 or 3 in six of eight).
Artwork craft is the standing weakest criterion, and a deck that is structurally
inventive and materially sparse is exactly the deck that scores 6.8 on craft. So
this run inverts it. Design variance drops to 3, meaning the deck may use a
familiar structural family, and the budget that buys goes into DENSITY at 4 and
a hot type setting at 5. The instruction to the directors room is fewer new
ideas, more finished surface.

## Standing weakness this run is deliberately attacking

`scripts/trend_check.py --window 10` (2026-08-29 to 2026-09-07):

```
REPEAT OFFENDERS (criterion, times weakest, mean, last worked on)
  weakest  7/10  mean 6.85   last 8.0  Artwork craft and genuine detail   worked 2026-08-31 (7 runs ago)  <-- STALE
  weakest  2/10  mean 7.6    last 8.0  Deliverable completeness           worked never  <-- STALE
  weakest  1/10  mean 6.7    last 7.0  Legibility and platform fitness    worked never  <-- STALE

HARD FAILS (0 of 10 runs carried one)
  none in this window

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   6 run(s)  warns:top-loaded composition          latest 2026-09-07
   5 run(s)  warns:busy art under text             latest 2026-09-07
   4 run(s)  warns:outside safe zone               latest 2026-09-06
   4 run(s)  warns:contact shadow                  latest 2026-09-03
   3 run(s)  warns:tiny-text                       latest 2026-09-02
   3 run(s)  warns:canvas mark near reserved text  latest 2026-09-06

SCORE, most recent runs
  08-31 7.79  09-01 8.89  09-02 8.52  09-03 8.81  09-04 8.76  09-05 8.77
  09-06 8.08  09-07 9.07
```

THE ONE WEAKNESS THIS RUN ATTACKS: artwork craft, through the two defect classes
that are its most persistent symptoms, top-loaded composition (6 of 10) and busy
art under text (5 of 10). Those two are the same bug seen twice. A deck top-loads
because the display type lands at the top and the art is authored to clear it,
which starves the bottom of the frame; the art then crowds back in under the type
because the reserve was cut after the art was drawn rather than before.

THE MECHANISM, and it is an authoring-ORDER change rather than a new technique:

1. THE RESERVE IS DRAWN FIRST AND IS PART OF THE PICTURE, and the house idiom
   currently works against that. Read No.53's slide 04. Its reserve is a
   `RESERVE` array and a `clipOut()` evenodd clip, so every art call is masked
   out of the type's box and what sits behind the words is BARE GROUND. That is
   correct for legibility and it is the mechanism behind both defect classes at
   once. A clipped hole has no tone in it, so its cells score zero on the
   entropy term below, and when the type is at the bottom of the frame the deck
   pays for its own reserve twice, once as an empty band and once as a
   top-loaded ratio.

   So this deck keeps the clip and PAINTS INSIDE IT. Each reserve is a real
   surface in the world with modelled tone of its own, established before the
   surrounding art runs, and the type is set on that surface. Not a plate laid
   over the world; a thing the world contains.
2. EVERY DOSSIER DECLARES ITS FRAME BALANCE, IN THE GATE'S OWN UNITS. Read
   `frame_balance()` in qa.py before planning a slide. It box-downsamples the
   render, scores each 27 design px cell as LIVE when its robust luminance
   spread or peak gradient clears 8.0, scores that cell as MODELED when the
   normalized entropy of its tonal histogram clears 0.55, drops the safe-margin
   ring, and returns the bottom third's craft density divided by the whole
   frame's. FAIL under 0.60, WARN under 0.80.

   So field 4a states a TARGET RATIO of at least 1.00, meaning the bottom third
   carries at least as much modeled craft as the frame average, and names the
   object that carries it. Planning in the gate's units rather than in a
   percentage of "mass" means the plan and the measurement are the same number,
   and a dossier can be wrong before a render exists.

   The entropy term is the part that decides this deck. A flat plate is bimodal
   and scores about 0.2, so a label plate, a hairline and a footer in the bottom
   band are worth nothing to this measure however much area they cover. Only
   graded, textured, lit or rendered tone counts. That is why the deck's own
   surfaces have to be materials rather than fills.
3. THE LIGHT IS PROBED OFF THE RENDER, NOT ASSERTED. No.53's whole score turned
   on one gradient line that erased the terminator on seven of nine slides, and
   five critics read the symptom before one cause was found. Any slide claiming a
   directional key gets its terminator read out of the rendered PNG before it
   leaves Phase 7.
4. DENSITY IS THE BUDGET, NOT AN ACCIDENT. visual_density 4 means the frames are
   worked. The zoom test is the standard.

## Seasonal Alaska context (for the scouts)

Second week of September 2026.

- The Legislature is OUT OF SESSION and returns in January 2027. Interim
  committee work and task forces only, so zero hearings in the BASIS sweep is
  normal and is not a broken collector.
- FEDERAL FISCAL YEAR ENDS SEPTEMBER 30TH. This is the loudest procurement
  window of the year: end-of-year obligations, solicitations closing, award
  notices, and use-it-or-lose-it contract actions. Anything AI-adjacent with an
  Alaska performance address is likeliest to appear right now.
- October 6th municipal and borough elections across Fairbanks North Star,
  Mat-Su, Kenai and Juneau. Ballot propositions and assembly races are live.
  NOTE: FNSB Proposition 3 was No.48 on 2026-09-02 and FNSB Resolution 2026-25
  was No.47 on 2026-09-01. Both are burned.
- PFD season. The 2026 dividend figure and the distribution schedule land around
  now, with first payments early October.
- Freeze-up approaching. Utilities are contracting winter gas, Cook Inlet supply
  and LNG import work is in its annual decision window, and the Railbelt's winter
  adequacy filings run now.
- Fisheries: silvers winding down, Bering Sea crab and groundfish openings ahead
  in October, and the post-season survey and observer decisions land in the fall.
- Wildfire season closing out; the season's own numbers get published.
- AFN convention is next month, so Alaska Native organizations are publishing
  policy positions now.
- Fall semester underway at UA; new grants and lab launches get announced.

## Dedupe: the 30-day burned list handed to every scout

2026-08-12 AURORA-AI at UAF · 2026-08-13 synthetic Anchorage local-news site ·
2026-08-14 NSF 26-513 regional AI hubs · 2026-08-15 S.5171 AI toy safety ·
2026-08-16 and 2026-08-30 Rural Health Transformation awards · 2026-08-18 Alaska
Airlines Flyways · 2026-08-19 Data for Progress data-center poll · 2026-08-20
Proclamation 11055 drone duty · 2026-08-21 DeepGreen FERC subsea data center ·
2026-08-25 Anchorage Assembly data-center ordinance · 2026-08-26 five NSF awards
to UA · 2026-08-27 Rainmaker cloud seeding · 2026-08-28 Permafrost Discovery
Gateway · 2026-08-29 Chukchi acoustic glider · 2026-08-31 FCC USF notices ·
2026-09-01 FNSB Resolution 2026-25 · 2026-09-02 FNSB Proposition 3 · 2026-09-03
Navy Spruce Cape building and Kodiak Electric · 2026-09-04 DNR Houston land
conveyance to AIDEA · 2026-09-05 Anthropic employee political giving ·
2026-09-06 NOAA Fisheries survey framework · 2026-09-07 FPDS-NG contract search
discrepancy.

## Search budget

Six scouts, 25 WebSearch calls each, hard cap, stated in every brief. Phase 1
spent 4. That leaves roughly 46 for Phase 3's claims work, Phase 3.5's docket
refresh and Phase 12's frontier scan.

## Phase status

Wake: done. Craft refresh: done, one entry appended to FIELD_NOTES about the
LinkedIn first-comment link question, raised as a proposal in the draft rather
than acted on.

## PROTOTYPE, run before the directors room

`out/proto/` (scratch, not shipped). One frame built to test the mechanism above
before any dossier commits to it, because the whole run turns on whether a
modelled reserve actually moves the number.

RESULT: `frame_balance` returns **1.077**, bands `[0.542, 0.689, 0.693]`. The
bottom third is the DENSEST band in the frame, against a FAIL at 0.60 and a WARN
at 0.80. The mechanism holds. A nameplate built as brushed lay plus oil mottle
plus bolt heads with their own contact shadows, with the mono type set ON it,
scores as craft rather than as a hole, and it looks like an object rather than a
plate.

TWO THINGS THE PROTOTYPE ALSO TAUGHT, both for Phase 7.

1. `AKENGRAVE.surface` knotted, exactly as its own header warns. The `form` I
   gave it was smooth and close to one-dimensional, so the seed raster ran
   parallel to the direction field and roughly two hundred strokes retraced one
   iso-line, printing a single contour tangle instead of a modelled tank. Any
   engraved surface in this deck needs a genuinely two-axis form, and the
   equipment BODIES are better served by `AK.reliefShade` with a `height(u,v)`
   callback, which derives per-pixel normals from a Sobel pass and is the right
   tool for a cylinder. Remember its `scale` option must be the canvas backing
   scale or it paints a quarter of the frame.
2. The bolt heads are the cheapest craft in the frame. Four radial gradients and
   four offset ellipse shadows, and they are what makes the plate read as
   fastened to something rather than pasted on. Contact shadows go on every
   object that sits on something, declared and probed, per the standing rule.

### PROTOTYPE 2, a NEGATIVE result worth as much as the first

Second frame, `AK.reliefShade` given a transformer tank as `height(u,v)`, a
half-cylinder across u with a 13-cycle cooling-fin term and a welded belt, at
`strength: 120`.

RESULT: the fins printed as a flat barcode and the cylinder is not visible at
all. The cause is that reliefShade shades from the per-pixel GRADIENT, so one
strength has to serve both the macro form and every high-frequency term riding
on it, and at a strength tuned for a smooth dome (the file's own advice is 60 to
200 for that) a 13-cycle ripple saturates the ramp everywhere and the dome's own
gentle gradient contributes nothing. The frame reads as vertical bars.

THE RULE FOR PHASE 7: one reliefShade pass shades ONE spatial frequency. Put the
macro solid through it at its own strength, and draw the fins, seams, ribs and
fasteners afterwards as lit strokes sharing the same declared key. Do not stack
frequencies inside a single `height` callback and expect one `strength` to serve
them. This is not documented in akrelief.js and is a candidate for Phase 12.

### PROTOTYPE 3, the corrected idiom, and it holds

Same tank, rebuilt to the rule the negative result produced. `AK.reliefShade`
gets ONE smooth two-axis form at `strength: 150` and nothing else. The 13 fins,
the welded belt and the nine fasteners are then drawn over the shaded solid as
lit strokes sharing the one declared key, az 118 el 34, so each fin carries a
dark lee on its upper-left side and a lit lip on its lower-right, with its width
foreshortened by the same cylinder term that shaded the solid.

The macro curvature now reads, dark at the shadow limb and bright toward the
key, the ribs sit ON the form rather than replacing it, and the fasteners each
carry their own offset contact ellipse. That is the hero material for this deck,
proven before a dossier asked for it.

THE THREE THINGS TO CARRY INTO PHASE 7, all measured rather than asserted:
1. A modelled reserve surface returns frame balance 1.077 where a clipped void
   returns the defect this run is attacking.
2. One reliefShade pass shades one spatial frequency.
3. Detail drawn after the shading has to share the shading's declared key, and
   render.py now prints that key's resolution on every render, so a mismatch is
   visible immediately rather than three rounds later.

### PROTOTYPE 5, the contact shadow, built wrong twice on purpose

Contact shadow is the fourth standing defect class, present in 4 of the last 10
runs, and No.41's retro says the failure is answered by widening pools until the
measure reads plus thirty while five critics call the result a detached black
hole in a spotlight. That failure was reproduced here, deliberately, in scratch,
so the deck never has to.

- **5a.** A pool centred on the object's own base, a soft cast. `contact_probe`
  measured **dL 4.1**, over the 4.0 floor and inside the 8.0 comfort band. The
  frame looked plausible and the contact did not really read.
- **5b.** Pool moved to the lit side and brightened, cast deepened. The probe
  measured **dL 23.9** and printed "dL 23.9 reads". THE PICTURE WAS WORSE. The
  pool had become a bright blob sitting BESIDE the object, the cast read as a
  separate flat quadrilateral, and because the cast was drawn in multiply after
  the object with no clip, it darkened the very thing casting it.
- **5c.** Pool re-centred UNDER the object at 470 by 118 so it extends past every
  edge, cast clipped with an evenodd rect so it can never touch its own object,
  gradient darkest at the seam and gone by 210 px, plus a hard six px anchor
  seam where the object meets the ground. Probe measures **dL 8.6**, just over
  the comfort band, and the object now stands in light rather than beside it.

**THE FINDING, and it is the one worth carrying: the measured dL and the read
came apart in both directions.** 5a passed the floor and did not read. 5b tripled
the number and got worse. Only 5c did both. So the rule for this deck is that
every contact is probed AND looked at, the pool goes UNDER the object and past
its edges, the cast is clipped out of its own object, and the floor is never a
target. `contact_probe --base` wants the point where the object MEETS the ground
on the profile line, not the centre of the pool.

A note on the probe's own advice. It warned about a 46 px gap between the base
point and the cast trough on all three versions, including the good one. That is
geometry, not detachment. A cast thrown at an azimuth is darkest off to one side
along a horizontal profile through the base, so the warning fires on any
directional cast. Read it, then look.

### PROTOTYPE 4, the searched page

The order's own text set as a field of ruled lines on a warm paper block, with
every occurrence of a searched phrase struck as a lit mark, two phrases present
and one absent. Built to test whether an ABSENCE can be drawn honestly and read
at feed scale.

It reads. Seven struck marks in two colours against a third key with nothing
beside it, and the count of marks IS the number, declared through
`window.__akAssert` with `points` so the frame does the counting rather than the
loop bound. That is the honest way to draw a zero.

Two defects in the prototype, both instructive and both fixable in the deck:
- The three-line key at the bottom sits on BARE GROUND, which is exactly the
  defect this run is attacking. In the deck that key goes on a modelled surface.
- The absent phrase reads as merely missing. It needs its own mark for nothing,
  a struck-through null or an empty slot the eye can see was left empty, or the
  reader has to notice a negative, which is the hardest thing to notice.

## THE GATE'S ACTUAL GEOMETRY, computed rather than assumed

Both treatments reason about "the bottom third", and one of them pins a
continuity datum to y 900 on the strength of it. The gate does not measure
thirds of the frame. It measures thirds of the frame MINUS a three-cell safe
margin ring, on a 27 design px grid. Computed from qa.py's own constants:

    grid            50 rows x 40 cols, one cell = 27 design px
    margin ring     3 cells, excluded entirely
    top band        design y   81 to  459
    middle band     design y  459 to  837
    BOTTOM BAND     design y  837 to 1269
    excluded        y 0 to 81, y 1269 to 1350, and 81 px down each side

SO THE NUMBERS THE ART BUILD WORKS TO ARE 837 AND 1269, NOT 900 AND 1350.
Craft below y 1269 does nothing for the ratio at all, which is where the
progress counter and the close slide's site fixture live. A datum drawn at
y 900 sits comfortably inside the measured bottom band and is a legitimate
place to put one, but the band's real top edge is 837 and any dossier that
claims exactness at 900 is claiming something that is not true.
