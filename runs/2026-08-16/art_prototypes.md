# ART PROTOTYPES — 2026-08-16 — run through the REAL gates before any dossier

Per instinct 0.90 and the No.33 precedent, scratch slides were rendered and gated
BEFORE the storyboard existed. These findings are BINDING on every dossier.

Prototypes live in `out/2026-08-16/proto/`. They are scratch and are not shipped.

## THE BRIEF THESE ANSWER

plan.md section 7 commits this run to attacking ARTWORK CRAFT AND GENUINE DETAIL,
weakest in 8 of the last 10 scored runs, mean 6.1, 6.0 last run. The declared
attack is a DRAWN SUBSTRATE that produces marks across the whole frame by
construction, rather than a smooth render decorated with annotation furniture
afterwards. No.34 climbed to rung 1 of the rendered ladder, real GPU PBR, and
still scored 6.0, so reaching for a more expensive renderer has already been
tried and did not move the number.

The bench also had to be one the last five decks have NOT used. No.30 and No.33
used akrelief, No.32 used akengrave across all nine frames, No.33 also used
akhachure on six slides, No.34 used akthree. That leaves weighted stipple and
aksdf, and both were tested.

## P0 — WEIGHTED STIPPLE SUBSTRATE, full frame. VERDICT: ADOPT.

Secord-style darkness-weighted stipple by rejection sampling against a height
field, 52,000 dots, six-step OKLCH-adjacent ramp, radius and alpha both driven by
the local height.

    render.py   OK, 1140 ms
    qa.py       fails=0  warns=0   verdict PASS

Findings, all binding:

1. **It clears `frame_balance` BY CONSTRUCTION when the height field's mass sits
   low.** The gate fails a slide whose bottom third carries under 60 percent of
   the frame's own craft density, where a cell only counts if it is both live
   (luminance spread or gradient) and MODELED (histogram entropy >= threshold).
   A stipple cell is both by definition, so the ratio follows the field. Put the
   field's mass in the lower half and the deck's single worst recurring machine
   warn, top-loaded composition, present in 5 of the last 10 runs and latest on
   2026-08-15, cannot fire.
2. **The detail is non-uniform because the DATA is non-uniform**, which is the
   akhachure docstring's whole diagnosis generalized. Density, dot radius and
   alpha are three separate functions of the same height, so a region cannot be
   flat unless the story's quantity is flat there. This is what the zoom test in
   DESIGN_DOCTRINE 5 is actually asking for.
3. **The height field must be SMOOTH plus one warp term.** A slow plane plus two
   broad gaussian lobes plus a single fbm warp at 0.10 amplitude reads as modeled
   light. This is the No.32 lesson (an engraved lay is the gradient of its form,
   so form must be smooth) carried across to stipple, where a high-frequency
   field would produce noise rather than tone.
4. **The top of the frame goes genuinely empty at low field values**, which
   `frame_balance` permits and the eye does not. Every real slide needs
   structure and a literal anchor up there, not a dot gradient. P0 is a
   substrate, never a composition.
5. Cost is trivial, about 1.1 s, so it can run on all nine slides.

## P1 — aksdf RAYMARCHED HERO on the stipple ground. VERDICT: ADOPT for ONE hero.

A carved slab with three shelves cut out of it, quadratic smin, single soft
shadow ray, two-tone warm-key and cool-shadow ramp, 460x575 internal upscaled
into a box on the slide canvas.

    render.py   OK, 2441 ms total for the slide
    Real modeled form, soft contact shadow, genuine material.

Findings, all binding:

1. **It is CHEAP.** 2.4 s for the whole slide against the library's stated 5 to
   15 s. Rung 2 of the rendered ladder is affordable here, and it is the rung no
   deck in the last five runs has used.
2. **THE RENDER BOX LEAVES A HARD RECTANGULAR SEAM.** `AKSDF.render` fills its
   destination rect with its own sky, so the box edge reads as a pasted panel
   against the slide ground. THE FIX IS NOT A BORDER. Either run the box
   full-bleed so there is no seam, or feather the composite through a mask, or
   make the rectangle a DELIBERATE declared frame with its own edge treatment.
   Any dossier using aksdf must state which of the three it does.
3. **ORDER MATTERS AND P1 GOT IT WRONG.** The stipple was laid AFTER the SDF
   composite and the composite covers it, so the hero panel had no drawn
   substrate on it at all. Lay the stipple FIRST, composite the SDF over it, then
   stipple again only outside the hero's silhouette. Same class of error as the
   No.34 grille, where a scrim painted after the GL composite darkened the
   deck's declared brightest light.
4. **NO `Date.now()` ANYWHERE, including a console timing line.** The determinism
   scanner read P1's two timing calls and warned on both. It reads inline scripts,
   so a profiling line that never touches the art still trips it.

## P2 — THE REAL COMPOSITE. Built, FAILED the gate, fixed, re-gated clean.

Stipple ground, then an aksdf hero, then DOM type, then a declared
`__akLeaders` leader and a declared `data-contacts` shadow. This is the one that
earned its keep.

    round 1   qa.py  FAILS=1  warns=1   verdict FAIL
              FAIL: contact shadow does not read, shadow L* 23.2 vs ground
                    L* 22.2, dL -0.9 at 432w, below the 4.0 floor, the object
                    floats
              warn: tiny-text, 22px mono under the 24px mobile floor
    round 2   qa.py  fails=0  warns=0

Findings, all binding:

1. **NEVER KNOCK A RENDERED COMPOSITE OUT BY LUMINANCE.** This is the new one
   and it is worth the whole prototype. To drop the SDF's sky I zeroed alpha
   wherever r+g+b was under 26, which is a perfectly reasonable-looking line of
   code, and it deleted THE CAST SHADOW, because the cast shadow is the darkest
   thing in the frame and therefore the first casualty of any darkness test. The
   render looked plausible and the object hung in mid-air. Four pixel critics
   read exactly this defect on No.26 and could not name the cause; here the gate
   named it in one line, in the first render, before any dossier was written.
   THE FIX IS TO PUT THE GROUND PLANE INSIDE THE SCENE as its own material and
   composite the whole rect, shadow included, so the shadow is real geometry
   rather than something the compositor has to be told to spare.
2. **Feather the composite edge, and feather BOTH ends.** Round 2 masks the box's
   top edge into the stipple with a 150px destination-out gradient and the seam
   disappears. The BOTTOM edge was left hard and it still reads as a horizontal
   cut across the frame. Any dossier using aksdf feathers top and bottom, or runs
   the box to the frame edge.
3. **The leader contract works and is cheap.** A world-coordinate polyline whose
   last point IS the target, a landing tick at that point, a DOM label at the
   `from` end, `AK.svgPlateAll` for the knockout, and the declaration naming all
   four. Gate returned clean on the first try. There is no reason for a slide in
   this deck to carry an undeclared leader.
4. **Mono labels at 25px, never 22.** The 24px floor is a hard edge and the house
   instrument face sits right on it.
5. The lit-ground-then-shadow discipline from SKILL.md is confirmed the hard way.
   A warm pool of light under the object first, the object second, and the shadow
   cut into the pool, is what produces separation. A darker shadow on a dark
   ground produces the 1.2 L* composite that failed No.26.

## WHAT THE DOSSIERS INHERIT

- Substrate is weighted stipple on every slide, driven by that slide's own story
  quantity, with the field's mass low in the frame.
- Exactly ONE aksdf hero panel, full-bleed or deliberately framed, with the
  stipple laid under it and re-laid outside its silhouette.
- Every height field is a slow plane plus broad lobes plus one low-amplitude warp.
- Every object that sits on something gets a lit ground first and a declared
  `data-contacts` second.
- No `Date.now()`, no `Math.random()`, seeds derived from 20260816.

## P3 — THE TEXT-HEAVY DATA SLIDE, the shape most of the deck will be. ADOPT.

Kicker, a two-line display head, four lines of 34px body, and the 864 to 1,800 to
403 to 19 funnel drawn as four bands in the lower half.

    round 1   qa.py  FAILS=1  warns=2
              FAIL: offscreen '1800 LETTERS' (bbox 958,941 198x34 vs 1080x1350)
              warn: outside safe zone x2
    round 2   qa.py  fails=0  warns=0

Findings, all binding:

1. **NEVER PLACE A LABEL AT THE END OF A DATA-DRIVEN BAR.** The label x was
   `80 + barWidth + 18`, so the widest value pushed its own label off the frame,
   and the second widest into the margin. This is the `outside safe zone` warn
   class that `trend_check` names as present in 4 of the last 10 runs, and here
   it is in its purest form. LABELS GO IN FIXED COLUMNS. The name left-aligned at
   a constant x, the value right-aligned to a constant x, both independent of the
   data. The bar is then free to be any length the number demands.
2. **The bars ARE the stipple.** Each band's contribution to the height field is
   a smooth `1 - dy^2` falloff inside its own width, so the bar is not a rectangle
   drawn over a texture, it is a region where the substrate gets denser. That is
   DESIGN_DOCTRINE 6.3, the field carries the data, realized rather than asserted,
   and it means the chart cannot be flat where the data is not.
3. **A text-heavy slide still clears `frame_balance`** as long as the data mass
   sits in the lower half. The head and body occupy the top 60 percent and the
   gate returned clean, because the bottom third carries the four bands.
4. Cost 686 ms. Cheaper than the hero and cheap enough for six body slides.
5. Remaining weakness, for the dossiers to solve rather than the bench: the band
   between the body copy and the first bar is genuinely empty. `frame_balance`
   permits it and the eye still notices. Real slides compose that zone.

## SUMMARY OF WHAT THE FOUR PROTOTYPES BOUGHT

Four gate failures found and fixed BEFORE any dossier was written, each of which
has historically cost a pixel-review round or shipped:

    P1  Date.now() in a profiling line trips the determinism scanner
    P2  a luminance knockout deletes the cast shadow and the object floats
    P2  22px mono is under the 24px floor
    P3  a label placed at the end of a data-driven bar goes offscreen

The contact-shadow defect is the one worth the whole exercise. It is the exact
defect four pixel critics reported on No.26 without being able to name the cause,
and the gate named it in one line on the first render.

## P4 — THE CLOSE SLIDE AND THE CONSTELLATION FIXTURES. Built, FAILED, fixed.

Wordmark, Polaris star, site line, progress counter, coordinates footer, the
single ask in gold, over the stipple substrate. Every slide carries most of this,
so a defect here is a defect nine times.

    round 1   qa.py  FAILS=1  warns=4
              FAIL: label crossed by art, 9 percent of the ring around
                    'SOURCES IN COMMENTS' is ink of the glyphs' own value,
                    spanning 100 percent of the label
              warn: busy art under text on the ask, the source line and the
                    wordmark
              warn: outside safe zone, 'alaskaaihq.com' at 80,1252
    round 2   qa.py  fails=0  warns=0

Findings, and the first is the most important thing the prototypes produced:

1. **A STIPPLE SUBSTRATE CROSSES GLYPHS AND FAILS THE GATE.** This is the
   structural collision between this run's declared craft attack and its type.
   A field that puts marks in every region puts marks through every letterform.
   Left unsolved it would have failed the deck on all nine slides.

   THE FIX IS NOT A SCRIM AND NOT A PLATE. DESIGN_DOCTRINE 3 says to earn it with
   the art, routing quiet zones under text by composition, before reaching for a
   scrim. So the substrate now READS THE DOM and suppresses itself inside every
   element marked `data-reserve`, padded, before a single dot is placed. This is
   the same mechanism `akengrave` exposes as `eng.reserve(AKENGRAVE.boxesFor(...))`
   and it is being carried across to stipple:

       var RES = [].map.call(document.querySelectorAll('[data-reserve]'), el => {
         var r = el.getBoundingClientRect();
         return [r.left-PAD, r.top-PAD, r.right+PAD, r.bottom+PAD];
       });

   It must run inside `document.fonts.ready`, because a box measured before the
   webfont loads is the wrong box. Result, zero fails and zero warns, and the
   holes do not read as rectangles because the field they are cut from is soft.

2. **PAD SCALES WITH TYPE SIZE.** 16px flat is enough for a 104px display head
   and marginal for 25px mono, where dots still crowd the counters between
   letters. Dossiers use `PAD = max(16, fontSize * 0.6)`.

3. **The bottom safe zone is 80px from the frame bottom, and fixtures stack.**
   The site line at `bottom:64px` put its box at y 1252 to 1286 against a limit
   of 1270. The whole fixture stack moved up 28px. Bottom fixtures now sit at
   bottom 92px (site), 132px (wordmark, counter), 186px (star).

4. Constellation marks all render clean. The four-point Polaris star as a single
   SVG path at 46px, the wordmark in the deck's display face, the site line and
   counter in JetBrains Mono, coordinates marked `data-decorative`.

5. Remaining composition note for the dossier rather than the bench, the middle
   band of this frame is empty while the bottom is busy. The gate permits it and
   the eye still asks for something there.

## P5 — THE ALASKA MAP SLIDE. Built, FAILED twice in one pass, fixed.

Real geodata, canonical projection, boroughs stippled where the record names a
place and left empty where it does not, three regions outlined in gold with
declared leaders.

    round 1   qa.py  FAILS=2  warns=2
              FAIL: text collision, 93 percent overprint, the head against the body
              FAIL: label crossed by art, 19 percent of the ring around the body,
                    spanning 71 percent of the label
              warn: art touching glyphs on the head
              warn: outside safe zone, 'KODIAK' at 661,1282
    round 2   qa.py  fails=0  warns=0

Findings, all binding:

1. **THE RESERVE MUST COVER EVERY ART LAYER, NOT JUST THE SUBSTRATE.** The
   stipple respected the reserve and the borough strokes did not, so d3's path
   strokes ran straight through the body copy and failed the pixel-level gate
   while the DOM-level collision check would never have seen it. Any layer drawn
   after the reserve is computed has to honour it too, by clipping or by placement.
   The fix here was placement, moving the projection's `fitExtent` down to
   `[[104,620],[976,1218]]` so the map cannot reach the copy.
2. **A DISPLAY HEAD'S HEIGHT IS ITS LINE COUNT TIMES ITS LEADING, AND IT MUST BE
   COMPUTED, NOT EYEBALLED.** Two lines at 96px and leading 1.0 is 192px, so a
   head at `top:136` ends at 328 and a body at `top:300` overprints it by 93
   percent. This is the 0.99 instinct about sanity-checking line counts against
   fixed-position blocks, and it cost one render.
3. **The bottom safe zone catches leader LABELS too.** A label at y 1282 is past
   the 1270 limit. Leader label anchors sit at 1176 or above.
4. **The empty-borough treatment works and is the slide's whole argument.** Three
   regions drawn as gold outline with no fill against a stippled interior reads
   instantly, and it is literally true, an absence drawn as an absence.
5. `d3.geoConicEqualArea().parallels([55,65]).rotate([154,0])` on the committed
   `alaska-boroughs.geo.json`, 29 features, renders in 621 ms.

## RUNNING TALLY, six prototypes

Seven gate failures found and fixed before a single dossier was written. Every
one of them is a defect class that has historically shipped or cost a review
round in this series.

    P1  Date.now() in a profiling line trips the determinism scanner
    P2  a luminance knockout deletes the cast shadow, the object floats
    P2  22px mono is under the 24px floor
    P3  a label at the end of a data-driven bar goes offscreen
    P4  the stipple substrate crosses glyphs and FAILS the deck
    P5  a non-substrate art layer ignores the reserve and crosses glyphs
    P5  a display head's computed height overprints the block below it
