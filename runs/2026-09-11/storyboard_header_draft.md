# DECK HEADER (constraints block, written before the directors room)

These are the showrunner's constraints, set in Phase 0 from ledger/artwork.json.
They bind every treatment. The concept itself is the room's to propose.

## VARIETY LEDGER CHECK, and this deck's REQUIRED divergence

FORBIDDEN hero structures, last 4 decks:
- 2026-09-06 the waterline as progress meter, one water body read at nine depths
- 2026-09-07 the curved transect as a camera move, one geodesic crawled across
  nine frames as a single continuous camera crawl
- 2026-09-09 the stamped field and the printed page, struck versus printed
- 2026-09-10 the struck register, intaglio pressed into damp laid stock

READ THAT LIST AS A SHAPE, NOT AS A LIST OF WORDS. Three of the last four are
ONE CONTINUOUS MEDIUM crawled or read across nine frames. A strip chart, a core
sample, a tape, a seam, a pipeline run and a timeline ribbon are all the same
topology and all are OUT this run, whatever they are made of. This deck needs a
different topology, not a different material.

FORBIDDEN atmospheres, last 3:
- terminator graze, key az 142 el 4
- sodium lamp and galvanized steel, yard at night, az 118 el 34
- printer's bench under a north window, cool key az 296 el 26

Note that two of those three are NIGHT or near-night. A daylight deck is
available and is the cheapest real divergence on the board.

FORBIDDEN continuity devices, last 2:
- a gold datum holding y=900 across all frames
- two struck squares carried in the footer gutter

FORBIDDEN hook archetypes, last 3:
- the search that returns two answers
- the sentence that isn't there
- timeline collapse

FORBIDDEN palette families, last 3:
- terminator blue and limestone
- sodium-zinc
- laid-paper-and-burin

FORBIDDEN type pairings, last 2:
- Fraunces + Space Grotesk + JetBrains Mono
- Instrument Serif + Bricolage Grotesque + JetBrains Mono

## THIS DECK'S DECLARED DIVERGENCE

- **Type pairing: Archivo (width axis 62 to 125) + Manrope + JetBrains Mono
  tabular lining.** Cool grotesk throughout, which serves type_temperature 2 and
  has not run in the last two decks. Archivo's width axis is available as a
  variable-axis device if a treatment wants one.
- **Register: DAYLIGHT.** After two night decks and a north-window bench, the
  divergence that costs nothing and reads instantly is to put the deck in cold
  overcast daylight.
- **Topology: NOT a continuous medium.** See above.

## VARIANCE DIALS

- design_variance 4. The standing weakness is craft and craft is where variance
  pays. Held high deliberately.
- visual_density 3. The last two decks ran dense and both drew the recurring
  warn trio. A mid-density deck with more modelled tone per element beats
  another crowded one.
- type_temperature 2. Cool and technical.

## THE ONE STANDING WEAKNESS THIS DECK ATTACKS, and the machinery for it

Artwork craft and genuine detail. Weakest in 7 of the last 10 runs, mean 6.7,
last reading 6.0. The recurring machine warns, busy art under text, canvas mark
near reserved text and art touching glyphs, are one problem wearing three
labels. This studio builds a field first and then negotiates with it for
somewhere to put the words.

**THE ATTACK IS A PLANNING MOVE AND IT IS MADE IN THE DOSSIERS.** Every slide
declares its TYPE GROUND before it declares its field, and the reserve is a term
in the field's own generator rather than a hole punched afterwards, so the quiet
band still carries the field's grain and still fills the bottom third.

The committed machinery for exactly this already exists and three of these
modules are NOT indexed in TECHNIQUE_LIBRARY.md, which is why recent decks have
not reached for them:

- `assets/js/akstipple.js`, `AKSTIPPLE.field(cx, {height, ramp, radius, alpha,
  count, seed, box, clip})`. Density, radius and alpha are three SEPARATE
  functions of the same height field, so a region can't be flat unless the
  story's quantity is flat there. `height` is required and has no default, on
  purpose. `AKSTIPPLE.reserve(selector)` measures per LINE BOX after
  `document.fonts.ready` and suppresses the sampler inside the ink, with the
  hole at `max(14, fontSize * 0.45)` and the fade ramped at `pad * 1.8`.
  `AKSTIPPLE.reserved(x, y)` is exported so every OTHER art layer honours the
  same reserve, which is the bug that shipped when d3 strokes ignored it.
- `assets/js/akparcel.js`, `AKPARCEL.band(cx, opts)`. THE ORDER RULE MADE
  STRUCTURAL. A depth band is drawn at FULL CONTRAST into its own offscreen
  canvas and only then compressed toward the far value and composited once, so a
  slide physically can't attenuate first and then draw into the compressed
  value. That is the flat mid band the scorer has named in 8 of the last 10
  runs, and it is the same finding as this run's Phase 1 craft note on aerial
  perspective, arrived at from the other direction.
- `AKPARCEL.W`, the five-token weight system, hair 0.75, fine 1.25, std 2.0,
  bold 3.5, hero 5.5, assigned by MEANING. Uniform line weight is the number one
  amateur tell.

## THE LINE GRAMMAR THIS DECK ARGUES IN, and it carries the honesty constraint

`AKPARCEL.LINE` already distinguishes SOLID from PHANTOM, and this deck's
accuracy structure maps onto it exactly:

- **solid** the number is MEASURED, or the words appear in a document
- **phantom** the number is a characterisation, a projection or a model output

That is the deck's whole honesty structure carried by stroke weight and dash,
legible at 432px thumb, without a caveat sentence anywhere. The measured storage
level is solid. The eighteen days is phantom, because it is a characterisation.
The modeled demand curve is phantom, because it is a model. The order of cuts is
solid or phantom depending on what the fact-checker says it rests on, and the
deck must follow that verdict rather than decide it.

## WHAT MUST NOT HAPPEN

This deck does not predict a shortage and must not read as one. No slide may
assert a state the data could flip. The comparison belongs in the numbers, not
in an adjective. If a treatment's concept requires the reader to conclude that
Southcentral will run out of gas, that treatment is wrong and gets rejected.

## THE RESERVE IDIOM, PROTOTYPED AND MEASURED BEFORE ANY SLIDE WAS PLANNED

Built a throwaway slide in `out/proto/` and rendered it three times. Four
findings, all of them cheap here and expensive at Phase 8.

**1. A SUPPRESSION-ONLY RESERVE READS AS A PLATE, and machine QA passes it at
zero warns.** The first build called `AKSTIPPLE.reserve('[data-reserve]')` and
nothing else. qa.py returned PASS, fails 0, warns 0, and the render shows three
hard-edged dark rectangles where the type sits, which is exactly the
"reads as a black rectangle at feed size" failure akstipple's own docstring
warns about. Instinct 0.99 confirmed live: a machine_qa PASS is never
composition approval.

**2. THE FIX IS A BASIN TERM IN `height()`, and the suppression pass is only the
last of the job.** Each text block declares a soft basin the field's own density
falls into, so the quiet band still carries the field's grain and still has
modelled tone in it.

```js
var BASINS = [[x, y, w, h, depth], ...];          // design px, depth 0 to 1
function basin(x, y) {                            // distance to the rect, ramped
  var k = 0;
  for (var i = 0; i < BASINS.length; i++) {
    var b = BASINS[i];
    var dx = Math.max(b[0] - x, 0, x - (b[0] + b[2]));
    var dy = Math.max(b[1] - y, 0, y - (b[1] + b[3]));
    k = Math.max(k, b[4] * Math.max(0, 1 - Math.sqrt(dx*dx + dy*dy) / 190));
  }
  return k;
}
// inside height(), LAST, after the form and the warp
h *= (1 - 0.82 * basin(x, y));
```

Ramp radius 190 design px and depth 0.82 measured well against this field. The
plates are gone and the quiet zones read as tonal basins in the same material.

**3. STILL TO IMPROVE, and it goes in the dossiers.** The basin is built from a
RECTANGLE and still carries a faintly rectangular feel. Building it from the
LINE BOXES instead, the way `AKSTIPPLE.reserve` already measures them, would let
the basin follow the rag. Use per-line rects where a block is ragged.

**4. THREE GATE LESSONS, all learned on the throwaway.**
- **No full-frame wrapper div over the canvas.** A positioned `div.wrap`
  spanning the frame made qa.py FAIL a declared motif as "buried, only 0 percent
  of the rect it declares is clear of opaque DOM (div.wrap)". Position each text
  block absolutely and independently.
- **Declare line counts and then fit them.** A two-line `<br>` headline rendered
  three lines and qa.py caught the wrap drift. `AK.fitText(el, {min, max,
  maxLines})` after `document.fonts.ready` is not optional on a display line.
- **Bottom type must END by y=1270.** A mono line at top 1215 with a 31px box
  clears the 80px safe margin; at 1250 it does not.
