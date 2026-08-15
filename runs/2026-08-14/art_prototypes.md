# ART PROTOTYPES — run No. 33, built before the storyboard

Three prototypes were rendered through the real engine before any dossier was
written, because this run's declared standing weakness is artwork craft and the
cheapest place to find out an image does not work is before it is specified.
Files under `out/2026-08-14/proto/`. They are scratch and do not ship.

## P1, Alaska under the canonical projection with a hachure interior

`d3.geoConicEqualArea().parallels([55,65]).rotate([154,0]).fitExtent(...)` on
`assets/geo/alaska-state.geo.json`, then `AK.hachureField` clipped inside the
silhouette.

WORKS. The coastline resolves down to the Aleutian chain and the Southeast
panhandle at 1080 px wide, and the hachure reads as terrain rather than as a
texture laid over a fill.

LEARNED. At `alpha: 0.10` in `#7FD4C8` over a `#07131C` base the field is
nearly invisible. The shipped value wants roughly `alpha: 0.30` in a much
lighter ink (`#C9F2E8`) at `cell: 7`, `passes: 4`. Sun at azimuth 305,
elevation 28, jitter 12 gives usable stroke-width spread.

## P2, all 50 states through ONE equal-area projection, then packed

Every state projected through the same `d3.geoConicEqualArea()` so relative
areas are TRUE, then each translated into its own cell by its own bounding box.
Sorted by projected area, 7 columns, so the reading order is a ranking.

WORKS, and it is the deck's strongest candidate image. At true relative scale
Alaska overflows its cell and Rhode Island is a speck, and the argument lands
with no words at all. 50 states fill 7 rows of 7 plus one, which puts Rhode
Island alone on the last row for free.

## P3, the corrected version, and the reason it needed correcting

P2 drew an identical gold token under all 50 states. That is a FALSE PICTURE
and drawing it is what exposed the error, which is recorded in selection.md.
One award per state is a CEILING. The solicitation anticipates 10 awards in
each cycle (C12) against 50 states, so most states end the cycle with nothing.

P3 therefore moves the tokens off the states entirely and into a reserved rail
along the bottom band, TEN of them, against a field of fifty. Alaska carries
the hachure interior and a hero-weight coastline, Rhode Island carries a thin
gold ring, and nothing suggests either one has been awarded anything.

The rail doubles as the answer to the bottom-band problem. Ten lit tokens with
two-part contact shadows sitting in a warm pool of light is modelled tone in the
lower third by construction rather than by a repair pass.

LEARNED. The mid-grid states fall too faint once the radial ground falls off;
the shipped version needs a floor on the state stroke value so rows four through
seven do not disappear at feed scale. Alaska also collides with the Texas cell
at `K = 210/maxdim`, which is either scaled down or turned into the one
deliberate grid violation the doctrine allows.

## What these buy the dossiers

The two images the deck turns on are proven to render, to hold at 1080 px, and
to carry their argument without words. The remaining work is composition, type
and the seven other slides, not a gamble on whether the hero is possible.

## P4, the honest scale comparison, Alaska relief against Rhode Island at ONE scale

`AK.reliefShade` onto an offscreen canvas, clipped to Alaska's silhouette under
the canonical projection, then Rhode Island drawn through THE SAME projection
object so the comparison cannot cheat, translated into the lower band.

WORKS, and it is the best single image the run has produced. The relief reads
as real terrain, the Alaska Range and the Brooks Range both resolve, the
Aleutian chain and the Southeast panhandle hold at 1080 px, and Rhode Island at
that scale is a gold speck that needs a 46 px ring to be findable at all. The
argument is made with no words and no chart.

Parameters that produced it, for the dossier to carry verbatim:
`noiseScale 0.011, octaves 5, warp 0.6, strength 4, low #0E2630, high #7FD8C6,
ambient 0.24, diffuse 0.95, seed 20260814`, region `x 80 y 230 w 920 h 650`.

HONESTY NOTE, and it binds the dossier. The relief is FORM shading off a seeded
noise field. It is illustration, not elevation data, and it encodes no
quantity. DESIGN_DOCTRINE is explicit that a magnitude may never be read off a
relief. The only quantity in this image is AREA, which is carried by the
equal-area projection itself and is true by construction. The dossier must say
so and the slide must not label the relief as terrain data.

## Composition learnings the dossiers inherit

- Rhode Island at Alaska's scale needs a ring or a leader. It is genuinely too
  small to find, which is the point, but an unfindable point is not an argument.
- The lower band is where the small thing goes, which solves field 4a for the
  scale slides by construction rather than by adding furniture.
- A radial warm ground reads well but falls off too fast; the mid field needs a
  value floor so nothing disappears at feed scale.

## P5, the type system, and the most important result of the whole exercise

A display headline through `AK.fitText(el, {min:52, max:118, maxLines:3})`, a
mono label on a measured knockout plate through `AK.svgPlateAll`, body copy at
34 px, over a hachure field occupying the bottom half.

TYPE WORKS, zero warns. Bricolage Grotesque at weight 700 and width 88 sets a
three line display headline that holds at feed scale, `fitText` lands it inside
its declared line count, and `svgPlateAll` sizes the gold plate off the label's
own `getBBox` so the plate cannot disagree with the string. The trio is
Bricolage Grotesque (display) plus Manrope (body) plus JetBrains Mono (the
record), with Space Grotesk for the kicker. That retires Instrument Serif,
Archivo, Fraunces and Unbounded, which clears the forbidden pairings of No. 31
and No. 32 with room to spare.

## THE RESULT THAT CHANGES EVERY DOSSIER

Running `qa.py` across all five prototypes returned this:

    slide-01  FAIL  top-loaded, bottom third carries 0% of average craft density
    slide-02  FAIL  top-loaded, bottom third carries 49%
    slide-03  FAIL  top-loaded, bottom third carries 38%
    slide-04  FAIL  top-loaded, bottom third carries 0%
    slide-05  ok    0 fails, 0 warns

**All four map compositions FAIL the frame-balance gate and the one slide with a
field running through its lower third passes clean.** That is this run's
declared standing weakness reproducing itself under laboratory conditions,
found before a single dossier was written instead of at the ship gate where the
scorer has named it six runs running.

P4 is the best image the run has produced AND it scores 0 percent craft density
in the bottom third. Those two facts are not in tension, they are the whole
lesson. A beautiful hero floating in a void is exactly the deck this machine
keeps shipping.

THE RULE THE DOSSIERS NOW CARRY. No map slide is composed as a silhouette on a
plain ground. Every one of them gets a worked lower band, and the proven
mechanism is a hachure or stipple field carrying real data through the bottom
third, with the small comparison object, the token rail, or the annotation
furniture sitting IN that field rather than on bare backdrop. P5 proves the
mechanism satisfies the gate. Field 4a is written before the hero on every
dossier, not after.

Two smaller notes. The hachure at `cell 9` over an undifferentiated fbm height
reads as fur rather than as terrain, so the shipped `height(u,v)` must be
driven by something with structure. And a field that starts on a hard
horizontal line leaves a seam, so the shipped fields feather or are clipped to
a shape.

## P6, the fix, proven on the real hero

P4's composition rebuilt with a worked lower band, and the band is not
decoration. The hachure `height(u,v)` divides the width into fifty lanes and
raises ten of them, so the field's ridges ARE the award arithmetic, ten against
fifty (C01, C12). Rhode Island sits inside that field rather than on bare
ground, at the same projection scale as Alaska.

    qa.py:  slide-06  ok  fails=0  warns=0

The same image that scored 0 percent bottom-third craft density as P4 now
passes clean, with the argument STRONGER rather than merely padded, because the
thing filling the band is the story's own number. That is the difference
between answering the gate and answering the defect.

This is the pattern every map dossier in the storyboard inherits.

(The run-level verdict still reads FAIL because prototypes 01 through 04 remain
in the directory. They are scratch, they do not ship, and they are kept
deliberately as the before half of the comparison.)
