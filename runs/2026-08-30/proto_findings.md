# PROTOTYPE FINDINGS — 2026-08-30, before the storyboard

Two primitives were built and rendered before any dossier was written, so the storyboard
commits to things that have been measured rather than assumed. This is the five-round cap's
"get it right on the first build" applied one phase earlier than usual.

## 1. THE BOROUGH MAP IS FEASIBLE AND EXACT

`d3.geoConicEqualArea().parallels([55,65]).rotate([154,0]).fitExtent([[60,180],[1020,1170]], geo)`
over `assets/geo/alaska-boroughs.geo.json` renders all 29 polygons cleanly, and every one of
the twelve boroughs and census areas this story needs highlights by exact `properties.name`
match. No fuzzy matching, no missing geometry.

Southern Southeast (Ketchikan Gateway, Petersburg, Prince of Wales-Hyder, Wrangell) reads as
a distinct archipelago cluster at the lower right. The Interior drone region (Denali,
Fairbanks North Star, North Slope, Southeast Fairbanks, Yukon-Koyukuk) is an enormous
contiguous mass across the top. Kodiak Island is a small separate object. That contrast, one
huge region and one small island both getting a machine, is real and drawable.

CAUTION MEASURED: at this fitExtent the Aleutian chain sweeps far left and the composition
sits high, leaving the bottom third empty. Any map slide must either crop, rotate the frame,
or move the mass down. The default framing is top loaded, which is one of the two defect
classes this run is attacking.

## 2. THE 185 CELL FIELD READS AT FEED SCALE, WHICH IS THE WHOLE CONCEPT

185 cells laid 15 across, 8 of them filled, rendered and then downsampled to the true 432px
feed width. **The eight read instantly and unmistakably at thumb size.** The coarse scale is
a true aggregation of the fine one, which is exactly the property the craft refresh named as
the mechanism behind eight runs of weak artwork scores. The ratio does not need a caption to
land.

So the cell field is confirmed as a load-bearing device and the storyboard may build on it.

## 3. TWO DEFECTS THE PROTOTYPE EXPOSED, BOTH NOW DESIGN INSTRUCTIONS

**a. The empty cells have no zoom payload.** At 100 percent the 177 unfilled cells are plain
hairline rectangles. That is the maintainer's "blocky, almost like a kid was drag and
dropping shapes" defect in its purest form, and a gradient inside a fillRect would not fix
it. Every cell must carry information at the fine scale. The obvious and honest encoding is
already in the record: each award has a Friday (four rounds), an initiative (six), a project
type (Implementation or Planning) and an amount. Give the empty cells a mark that MEANS one
of those, so zooming rewards the reader with structure rather than boxes. Whatever is chosen
must satisfy the measured axis contract if position carries a number.

**b. The prototype composition is top loaded with a dead bottom third.** Both the map and
the field defaulted to sitting high. That is 4 of 10 runs' warning class and the scorer's
six-time note. Every dossier's field 4a has to name real modeled tone down there, and the
field or map has to be positioned to allow it.

## 4. ONE ENGINE FACT RELEARNED THE CHEAP WAY

A slide cannot `fetch` a run artifact. `@@ASSETS@@` resolves only to committed assets, and a
relative escape out of it is `net::ERR_FILE_NOT_FOUND`, which surfaces as a render hard fail.
**All award data must be INLINED into each slide as a literal.** Caught here for the price of
one prototype render rather than mid-build.

## 5. THE COUNT ASSERTION WORKS AS DOCUMENTED

`window.__akAssert` with `points` correctly counts the 185 drawn cell centres in frame. The
deck's headline count can therefore be gated by the frame itself rather than by the loop
bound, which is what No.40's 750 versus 720 incident requires.

## 6. THE THREE SCALE RULE, NOW PROVEN ON A RENDER RATHER THAN ASSERTED

A second prototype was built to close finding 3a, and it works. Rendered, then measured at
all three scales:

- **432px feed thumb.** Eight dark cells in a field of 185. The ratio lands with no caption
  and no zooming. Unchanged from the first prototype, so the zoom payload did not cost the
  coarse reading, which was the risk.
- **1080 full size.** The field resolves into four blocks, because the awards are ordered by
  notification date and the four Fridays are contiguous runs of 19, 37, 105 and 24. The
  field read in order IS a timeline, which was not designed and was discovered by sorting.
  A nine pixel band shift per round makes it visible.
- **100 percent zoom.** Every cell carries a group of one to six short rules standing on its
  own floor, and the count is that award's initiative. Health Care Access, Spark Technology
  and Innovation, Strengthen Workforce, Healthy Communities, Healthy Beginnings, Pay for
  Value. The 177 unfilled cells stopped being empty boxes and became records.

Each scale is a true aggregation of the finer one and none of them contradicts another,
which is the property the craft refresh named. The encoding is CATEGORICAL, a rule count
standing for a category, so no position in it carries a number and the measured axis
contract is not engaged. That was deliberate. A bar length encoding dollars inside each of
185 cells would have been prettier and would have required declaring 185 marks.

**Ground.** The sheet carries modeled tone from a north light pool built as a circle inside
a `scale()` transform, never as an elliptical radial gradient, per the 2026-08-26 rule.

## 7. WHAT IS STILL WRONG IN THE PROTOTYPE, AND IS THE STORYBOARD'S JOB

The bottom band is still the weakest part of the frame. The light pool reaches into it and
the source line sits there, but a source line is furniture and field 4a says furniture does
not count. Every dossier has to name real modeled tone in the lower third, and the field's
vertical placement has to leave room for it. This is the run's declared standing weakness and
the prototype confirms it does not fix itself.

## 8. THE SOUTHERN SOUTHEAST ZOOM IS THE DECK'S FREE DETAIL

`AKGeo.zoomTo(proj, geo, [-132.4, 55.9], [540, 700], 7.0)` on the borough file renders the
four Southern Southeast service areas as what they actually are, an archipelago of hundreds
of islands, fjords and channels, at a level of intricacy no invented ornament could match.
No giant fill disc, so the SKILL.md warning about `fitExtent` on a small bbox is correctly
avoided by using `zoomTo`.

This matters editorially and not just decoratively. The reason a $6.5 million surgical robot
in Ketchikan is a story is that Petersburg, Wrangell and Prince of Wales are across water
from it, and the coastline is the argument. The art does not have to say "remote"; the
geometry says it.

Third confirmation of the same composition defect, so it is a pattern and not an accident:
this frame is also top loaded with an empty bottom third at the default framing. Every
dossier must place its mass deliberately.

## 9. A NUMERICAL COINCIDENCE THAT MUST NOT BE USED, FLAGGED BEFORE ANYONE TRIPS ON IT

`assets/geo/alaska-places.json` contains exactly **42 places**. The Tanana Chiefs Conference
drone award serves exactly **42 Interior villages**. These two 42s have nothing to do with
each other. The gazetteer is a general Alaska place list running from Adak to Wrangell; the
award's 42 villages are TCC's own service villages and this run has no verified list of them
and no coordinates for them.

**Do not plot 42 dots and call them the villages.** Do not let the coincidence survive into a
dossier, a slide, a label or a caption. If the deck wants to show 42, show it as a COUNT
somewhere that is not a map, and let the map carry only what is verified, which is the five
service area boroughs and the Fairbanks hub.

Verified points available in the gazetteer that DO correspond to real award geography, with
true lon and lat: Fairbanks (the TCC hub), Kotzebue (in Maniilaq's Northwest Arctic service
area), Ketchikan, Petersburg and Wrangell (three of the four Southern Southeast service
areas), Kodiak, and Wasilla and Palmer for Mat-Su. Prince of Wales-Hyder has no gazetteer
point and should be named by its polygon rather than by a dot.

## 10. A HIGH KEY DECK CANNOT GET ITS FORM FROM RELIEF SHADING, MEASURED

This is the most useful thing the prototypes found, because it kills a plausible plan before
it costs a render round.

`AK.reliefShade` was run over a full sheet with a slack curl heightfield, first at the
sensible setting (`strength:120`, `ambient:0.62`, `low:#CDC2AC`, `high:#FFFCF3`) and then
pushed hard (`strength:260`, `ambient:0.30`, `diffuse:0.95`, `low:#8C7F66`). Measured on the
rendered sheet:

    luminance mean 242.2, standard deviation 16.8, min 170, max 252

Even at full push the sheet never gets below 170 of 255 and the whole form lives in about 17
levels. It reads as a flat white rectangle. That is the "handsome type on empty ground"
failure mode, and it would score exactly the 6 on artwork craft that this run is trying to
beat.

**The reason is structural, not a tuning problem.** A lit surface carries form in tonal
range. A near-white substrate has almost no range below it to spend, so the ramp piles up
against white and the gradient does nothing. Turning the light up does not create range that
the palette does not have.

**So the rule for this deck, if it goes high key, is that FORM COMES FROM INK, NOT FROM
LIGHT.** Depth is carried by the drafting bench rather than the lighting bench: occlusion and
overlap, cast shadow as a drawn object with a hard edge, line weight hierarchy across two to
four weights, hatch and stipple density, and the intricacy of real geometry like the Southern
Southeast coastline. The DESIGN_DOCTRINE depth mandate is satisfied, just from cue 2
(occlusion) and cue 6 (shadow) rather than from a relit heightfield.

This also settles the contact shadow question for a light deck. On a dark deck the note says
a shadow needs a LIT GROUND to subtract from. On a paper deck the ground is already the
brightest thing in the frame, so a cast shadow has the whole range beneath it and reads
easily, which is the one place a high key register is EASIER than the last eight decks.

## 11. akengrave IS THE BENCH FOR THIS DECK, AND THE NUMBERS SETTLE IT

The same near-white sheet, shaded two ways and measured over the same band:

| bench | luminance stddev | min reached |
|---|---|---|
| `AK.reliefShade` at full push | 16.8 | 170 of 255 |
| `AKENGRAVE.surface` | **62.1** | **30 of 255** |

Three and a half times the tonal range, reaching genuine dark, on a ground of the same
value. The reason is exactly finding 10. Relief spends a colour ramp it does not have on a
light substrate, while the engraver spends INK, and ink on paper has the whole range beneath
it. Stroke width is set per stroke by the light, so the form survives even though the ground
is bright.

The technique library says the same thing from the other side and it is worth quoting the
distinction precisely, because it is easy to misread. Its warning is that **a high LIGHT
ELEVATION** flattens every stroke to one width. It is not a warning against a light-valued
GROUND. Those are separate variables. Keeping the key raking at elevation 24 and taking the
brightness from the region's base fill is the correct reading, and both directors who have
reported so far arrived at it independently.

## 12. AN UNDOCUMENTED LOAD ORDER DEPENDENCY, FOUND THE CHEAP WAY

`akengrave.js` calls `AKC` inside `Engraver.surface`, so it requires `akcolor.js` to be
loaded BEFORE it. Nothing says so. The failure is a render hard fail reading
`AKC is not defined` at `akengrave.js:204`, which is legible once you see it and is a wasted
render round if you meet it mid-build.

`akrelief.js` documents its own equivalent ("Load AFTER noise.js") in the technique library
entry. `akengrave` does not. **This is a Phase 12 candidate**, and it is the cheapest kind of
upgrade there is, one line in the library entry and a guarded error message in the file.
