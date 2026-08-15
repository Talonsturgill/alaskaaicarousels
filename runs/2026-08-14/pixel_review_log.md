# PIXEL REVIEW — run No. 33, round 1

Five pixel-critics across nine slides. **Every one returned `revise`**, with
per-slide scores between 3.5 and 6.0. That is the harshest round this deck could
have had and it was worth every token. What follows is what they found, what was
fixed, and what was refused.

## WHAT WAS REFUSED, and why

**"The 48 px ring is not constant across slides."** Two critics measured ring
diameters off the rendered PNGs and reported 78, 81 and 89 render px against the
required 96, concluding the deck's central invariant was broken. It is not.
Every ring in the deck is drawn by a single call shape, `cx.arc(x, y, 24, ...)`
on a context at `scale(2,2)`, which is 48 CSS px by construction, and a grep
across all nine slide files confirms there is no other radius in use for a ring
anywhere. What the critics measured was the anti-aliased outer edge of a 1.4 to
2.0 px stroke at three different weights, which is not a reliable ruler. The
finding is recorded here rather than silently dropped, because two independent
critics reaching the same wrong number is worth knowing about, and the honest
lesson is that the invariant should be machine-asserted rather than eyeballed.
That is written up as a Phase 12 candidate.

## WHAT WAS FIXED

**The projection note was truncated on five slides.** I had shortened the Device
B strings to make them fit, which quietly gutted the deck's continuity system on
slides 03, 05, 06, 07 and 08. Two critics caught it independently and both called
it systemic rather than a one-off. All five restored to their declared strings;
slide 03's now wraps to two lines rather than being cut.

**Slide 03's regulated areas were STACKED, not NESTED.** The slide's whole
declared semantics is that an institution sits inside a state, so the inner
boundary has to lie wholly inside the outer one. As built they were two boxes one
above the other, which draws nothing. Rebuilt as a true nesting.

**Slide 03's stamp box was empty.** The dashed magenta box that replaces the
scale bar carried no type at all, so the string "SCALE NOT PRESERVED" appeared
nowhere on the one slide whose point is that the projection went flat. It is now
set as real SVG text on a measured plate, not canvas raster.

**Slide 04 printed an unqualified scale bar on a slide with no map.** On a deck
whose entire thesis is that the margin declares what the projection preserves,
that is a self-inflicted honesty error, and it is the one piece of marginalia a
chart reader trusts without checking. The bar is now struck through and labelled
NOT TO SCALE / OBJECT VIEW.

**Slide 06's 4x detail row drew the opposite of the slide's thesis.** It
magnified the STATES by four while leaving the rings at 48 px, so small states
filled or overflowed their own awards. A reader would have taken away exactly the
inverse of the argument. A false picture is worse than no picture, so the row was
cut, and the recovered height went into the strip and the band.

**Three leaders terminated in void** (slides 01, 06, 08). This is the defect
class DESIGN_DOCTRINE names in capitals, and the one No. 28 shipped twice past
four reviewers. Slide 06's now lands on the first overlapping ring pair with a
label reading RINGS OVERLAP FROM HERE; slide 08's now runs to the correction
stamp instead of into empty water.

**Slide 09 had dropped the deck's own closing move.** The Device B terminal
string, ONE MERIDIAN, 154W. SHEET CLOSED., was absent, as was any source line or
claim-id, so the nine-slide state machine simply stopped instead of closing.
Both restored, and the decorative coordinate string that was breaking the safe
margin came out to make room.

**Slide 06's rings buried the land.** Fifty magenta rings drawn over fifty
silhouettes read as a pink coil with the subject underneath it. The rings now
draw UNDER the land, so a state large enough to cover its own award hides it and
a state smaller than its award cannot. The overlap became an outcome of the
geometry rather than a pattern laid over it.

Plus: slide 02's body corrected from "Ten will be awarded" to "NSF anticipates
ten awards per cycle" (the copywriter caught this one), slide 07's source line
un-collided from its counter and its "1,034" given back its unit, slide 04's
headline hard-broken so "cycle." stops being an orphan, and four safe-zone
violations cleared.

## WHAT IS KNOWINGLY LEFT

- **Slide 06's strip is still dense.** At true relative area every state after
  Alaska is small, so the rings overlap from about rank three onward. That is the
  honest picture and the critics are right that it costs legibility. The leader
  and its label now name where the overlap starts, and the rings sit under the
  land, which is as far as this round took it.
- **Light direction is not perfectly coherent on slides 01 and 07.**
  `AK.reliefShade` runs its own NW key (azimuth 315) and does not accept the
  deck's declared 118/26. Changing that is a library change, not a slide change,
  and it is logged as a Phase 12 candidate rather than hacked in at review time.
- **The graticule edge-tease (Device C) is not visibly running.** It is declared
  in the storyboard and several critics could not find it. It is the deck's third
  continuity device and the weakest of the three; the two that carry the argument
  both read.
