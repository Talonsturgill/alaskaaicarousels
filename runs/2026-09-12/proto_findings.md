# CHASSIS PROTOTYPE, READ BEFORE BUILDING ANY SLIDE — 2026-09-12

One frame built on `akunderice.js` plus `akfit.js`, rendered, gated and LOOKED AT
before the directors room reported. `out/2026-09-12/proto/`.

**The machine says PASS, fails 0, warns 0. The picture has four defects.** That
gap is the whole reason this exists, and it is the oldest instinct in the ledger
at confidence 0.99: never treat a machine_qa PASS as composition approval.

## 1. THE RESERVE IS A BLACK RECTANGLE, and it is a documented trap I walked into

`AKENGRAVE.punchReserves` did exactly what it says, a destination-out punch of
blurred rectangles, and the result is three hard-edged near-black boxes sitting
behind the headline, the chip and the body. At feed size they read as plates.

This is written down. `aksheet.js`'s own docstring records the identical finding
from 2026-09-11, that a suppression-only reserve "returned qa.py PASS, fails 0,
warns 0, and rendered three hard-edged dark rectangles where the type sat, which
is exactly the 'reads as a black rectangle at feed size' failure akstipple's own
docstring predicts." I read that file this morning and reached for the punch
anyway, because the punch is the idiom SKILL.md documents for a field the slide's
own loop drew.

**THE RULE FOR EVERY SLIDE IN THIS DECK.** A reserve is a BASIN in the field's own
density, multiplied into the population's `height` term LAST, so the field THINS
where the words go and still has marks in it. Never a hole cut out of a painted
field. Where a basin is not enough, the second tool is `AKNIGHT.veil`'s idiom, a
subtraction whose strength follows a MEASURED reading of the ink actually under
each line box, so quiet water is left alone. The punch stays available for one
case only, a small mono stamp over genuinely busy ink, and even there it needs the
field to continue faintly across it.

## 2. THE MIDDLE OF THE FRAME IS EMPTY, which is the wallpaper finding arriving on schedule

The upper half is a gradient with sparse motes. That is a region covering roughly
40 percent of the frame carrying a fill and a scatter, which is the exact sentence
No.56's brief uses for what not to ship. Density dial 5 is declared and unpaid.

**THE FIX IS THE STORY'S OWN GEOMETRY, and it is better than texture.** Draw the
SOUND. Acoustic paths in an ice-covered water column refract and reflect off the
underside of the ice, so a family of ray traces from a source curves up, turns at
the lid and comes back down, filling the whole column with dense curved marks
whose spacing and turning depth are parameters rather than decoration. That is
DESIGN_DOCTRINE section 6 point 3, the field carrying the data, and it puts the
marks where the picture is instead of in the furniture.

HONESTY CONSTRAINT ON IT. The ray geometry is a property of the DRAWING and not a
published profile, so every dossier that uses it marks the bullet `[design]` and
`aggregates.json` says so again at build time. The deck may not imply the notice
publishes a sound speed profile. It does not.

## 3. THE OBJECTS ARE CUT BY THE BOTTOM EDGE AND READ AS TINY

The three moorings sit at y 1286 with their anchor blocks running off the frame,
so the deck's one class of physical object is a sliver. The contact triple is
drawn correctly and is wasted on 20 px of visible block.

**FIX.** Bring the bed up so an object stands COMPLETELY inside the frame with its
lit pool and cast beside its foot, and let the deck's descent carry the bed lower
only on the frames where the bed is the subject. An object worth lighting is worth
seeing.

## 4. THE WATERMARK AND THE 400 m LABEL BOTH LAND ON ART

`alaskaaihq.com` is sitting across a gold ring and is nearly unreadable, and the
0 m rail label is half off the top of the frame. Both are fixtures, so both are
every slide's problem rather than this slide's.

**FIX.** The fixtures get their own reserved lane, and the rail's end labels are
placed from the mapping with a clamp so they can never sit outside the frame.
`AKFIT.clamp` exists for exactly this and the prototype did not use it.

## WHAT WENT RIGHT, and is worth keeping

- The ICE reads. The keeled underside with brine channels draining down from the
  crust is the best thing in the frame and it is a real form rather than a band.
- The light-keyed profile works. The anchor blocks have a visibly heavier, darker
  lower edge and it reads as weight rather than as outline.
- The rings are built out of stops and carry no flat core, so the additive
  composite is clean. No.53's limb defect is not reproduced here.
- The depth rail generates its own declared scale from the marks it actually drew,
  and `data-scale` passed the axis census once the minor ticks were made findable.
- `AKFIT.guard` caught its own false positive twice and both were fixed in the
  helper rather than worked around in the slide. A guard that cries wolf costs a
  round, so the guard now fires only where a clip is possible.

## TWO DECK-LEVEL RULES THIS FRAME TAUGHT

**THE TOP BAND IS LIT ICE, SO HEADER TYPE IS DARK.** The ice crust fills the frame
from y 0 to the waterline in near-white, and the wordmark was authored light,
measured at 1.7 contrast, brightened, and measured WORSE at 1.0. Every fixture in
the top band is dark ink on ice for the whole deck.

**A MINOR TICK ON A MEASURED AXIS COMPETING WITH A SCREEN BLEND IS A MARK THE
CENSUS CANNOT FIND.** Two of five declared marks read at or under the band's own
texture, because the gold rings lift the local ground where they cross the rail.
The chassis now draws every declared mark at findable weight, and the rail carries
three strong marks rather than five of two ranks.

---

# SECOND ROUND, AND BOTH FIXES ARE MEASURED RATHER THAN ASSERTED

## THE BASIN RESERVE WORKS, and the punch is now banned in this deck

`AKICE.basins()` takes the measured line boxes from `AKFIT.reserveBoxes` and
returns an attenuation function that the field GENERATORS consult, so the marine
population and the ray field simply put fewer marks where the words go. Nothing is
cut out of a painted field.

The three hard-edged black rectangles are gone. The headline now sits on the same
graded water as the rest of the frame, quieter, with the value ladder running
unbroken behind it and no edge anywhere. qa.py still reports fails 0 warns 0, and
this time the picture agrees with it.

THE RULE, and it now binds every slide. Reserve by basin. `AKENGRAVE.punchReserves`
is not used in this deck. The one case that could still justify it, a small mono
stamp over genuinely busy ink, has not arisen.

## THE RAY FIELD IS THE ANSWER TO THE EMPTY MIDDLE

`AKICE.rays()` traces sound from a source, curving upward at a constant rate,
turning at the underside of the ice and coming back down. Twenty six rays at
`curve 0.0026` fill the column from the lid to the bed with nested arcs, and the
upper half of the frame went from a gradient with a scatter over it to a region a
reader can look INTO.

It is also the story rather than texture, which is the difference the doctrine
asks for. The marks in the water are the thing the permit is about.

HONESTY, restated because it matters. The ray geometry is a property of the
DRAWING. Neither notice publishes a sound speed profile, a turning depth or a
bounce count, and every dossier bullet carrying a number from it is marked
`[design]`.

## WHAT IS STILL WRONG IN THE PROTOTYPE, carried into the dossiers

- The moorings still read small and the leftmost is clipped by the bottom edge.
  An object worth lighting is worth seeing whole. The bed comes up further, or the
  object comes forward.
- The 0 m rail label still clips the top of the frame. `AKFIT.clamp` exists for
  exactly this and the prototype has not been made to use it yet. Every rail end
  label in the deck gets clamped.
- The watermark still lands on art rather than in a reserved lane.
