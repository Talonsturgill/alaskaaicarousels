# STORYBOARD HEADER, DRAFT — No.57 — 2026-09-12

Written from two of three treatments plus the measured prototype. The
systems-illustrator's pitch amends this before it becomes `storyboard.md`.

## THE SYNTHESIS, and what each room won

**The chassis and the descent are the field-documentarian's**, because a camera
that only goes down makes the swipe a physical act rather than a sequence of
crops, and because it ties the deck's light budget to its argument. Windows,
palette arc and the riser chain come from that treatment nearly intact.

**The thesis image is the historian's**, which is that depth is distance from
what is known, and that the record's own series is the subject rather than the
mechanism.

**Two frames are transplanted whole and neither is negotiable.**

1. **THE UNATTENDED YEAR** (field-documentarian, the frame it said it would
   fight for). 2,190 hairline ticks, six a day for 365 days, of which 132 are
   lit, six a day for the 22 days a ship is there. No chart furniture, no
   plate, no explanatory sentence. It is the frame that gets screenshotted into
   a meeting.
2. **THE RAIL THAT RUNS OUT OF TICKS.** The deepest depth either notice states
   is 2,000 metres. Below that the depth rail continues as a phantom dash
   carrying no ticks at all. It is a second carrier of the thesis, it costs
   nothing, and it is drawn rather than said.

**THE COLOUR LAW, and this is the one place both treatments are overruled.**
The field-documentarian made gold the machine's position. The historian made
gold the term of the instrument. Both are single-meaning and both are good, and
each has one frame where it leaks. So the law is one step up from either:

> **GOLD IS WHAT THE RECORD KNOWS. The undetermined ink is what it does not.**

`#FFC72C` appears only on the fix cross, the range arcs that produce it, the 132
attended ticks, and the Polaris at the close. `#7D8F94` appears only on the
2,058 unattended ticks, the phantom dash below 2,000 metres, the ghost marks of
a coefficient of variation, and the word UND. Nothing else in the deck is warm
and nothing else in the deck is that grey. A pixel critic can audit the whole
deck against one sentence, and if gold has landed on anything the record is
vague about, the deck has lost its own argument.

That law also resolves the historian's worry that a reader entering at the
abundance frame sees a gold cross with no legend. Under this law the cross needs
no legend, because it is the only precise thing in a frame whose subject is
imprecision.

## THE THESIS

The permit knows the machine's position and does not know the animal's number.

## HERO STRUCTURE

**NEW: THE OCCUPIED STATION, DESCENDED.** One column of Arctic water at one
station, drawn as a continuous vertical section that nine frames descend through
on a single shared depth-to-pixel mapping, with every string of type set INSIDE
the water and kept legible by measurement rather than by a fence.

Divergence from all four forbidden structures, stated as the ledger requires. It
traverses no geography and never pans, so it is not No.53's curved transect as a
nine frame camera move. It contains no printed surface of any kind, so it is
neither No.54's stamped field and printed page nor No.55's struck register on
laid paper. It has no neatline, no margin and no annotation gutter, so it is not
No.56's sheet and its margin, and that is the deliberate inversion: No.56 made
type safe by fencing it out of the art and then spent its whole detail budget on
the fence. Here the type is in the water and `akfit.js` plus a basin reserve pay
for it, so the detail budget goes where the picture is.

## ATMOSPHERE

**"First dark under new ice."** The end of the melt season, a lid recently
formed, the last workable daylight of the year coming through it and dying inside
the first 500 metres.

One light, declared once, never varied. **Azimuth 12 clockwise from up,
elevation 62, downwelling, key to fill 5.0 to 1.** The lee of every form falls
just to its lower left and every cast is short. A steep key flattens a swelled
line, which is why this deck does not lean on surface swell for its modelling:
the modelling is the value ladder of depth, `AKICE.contrast(y)`, and
`AKICE.profile`'s third rank, which is a LIGHTING rank rather than an importance
rank.

Additive budget, so no second light can sneak in. `AKICE.daylight` peak 0.16 on
frames 01 to 03, 0.09 on 04, zero from 05 down. `AKICE.litPool` peak 0.26, used
on frame 08 only. Gold is ink and a signal, never illumination.

## PALETTE, family "new ice over black water"

| hex | role |
|---|---|
| `#D8ECEE` | ice crust, the one genuinely lit surface, frames 01 to 03 |
| `#9FC2C8` | ice body |
| `#5E838C` | the keel, the ice underside |
| `#E8F6F7` | the arris, the deck's hardest edge |
| `#1A4C57` `#123E49` `#0C2E38` `#08202A` `#061821` `#04111A` `#03090C` `#02080D` `#02060F` | the value ladder, one hex per window boundary, each frame's top being the previous frame's bed |
| `#F4F8FF` | display type |
| `#D8ECEE` | body type |
| `#BAD6DA` | rail ink, mono labels, units, mitigation circles |
| `#7D8F94` | **THE UNDETERMINED INK.** Phantom dashes, UND, the unattended ticks, ghost marks. The only desaturated hue in the deck |
| `#6EA5FF` | forget-me-not, the two beluga stocks, the species that have numbers |
| `#3CE6B4` | aurora green, exactly one use, the glider's lit upper surface on 04 |
| `#46545F` | the `alaskaaihq.com` watermark, every frame |
| **`#FFC72C`** | **the one gold. What the record knows.** The fix cross, the range arcs that make it, the 132 attended ticks, the Polaris |

## TYPE SYSTEM

Display **Fraunces**, cover 118 px wght 640 opsz 96 SOFT 24 WONK 1, headlines 72
px wght 600 SOFT 12 WONK 0, leading 0.97 to 1.02, tracking minus 1.5 to 2
percent. Every headline fitted with `AK.fitText`.
Support **Space Grotesk** 500 at 34 px, leading 1.38, max width 560 px, which
lands body lines at 30 to 38 characters.
Instrument **JetBrains Mono** 500, labels 25 px caps tracked plus 8 percent, rail
numerals 25 px tabular lining, counter 22 px, watermark 18 px.

Pairing is Fraunces over Space Grotesk over JetBrains Mono, which clears both
forbidden pairings (No.55's Instrument Serif and No.56's Archivo). Body type
never goes below 32 px. The only sub-floor element in the deck is the 18 px
watermark, which the brand spec licenses as a fixture.

**THE TOP BAND IS LIT ICE, SO HEADER TYPE IS DARK**, measured on the prototype:
the wordmark was authored light at 1.7 contrast, brightened, and measured worse
at 1.0. On frames 01 to 03 the wordmark and counter are `#16333B` on ice. From
frame 04 down, where the lid is gone, they return to `#BAD6DA`.

## VARIANCE DIALS

design_variance 5, visual_density 5, type_temperature 3.

## CONTINUITY SYSTEM, four devices

**D1, the descending window.** `AKICE.setWindow` per slide on one shared mapping.
`d0` never decreases and `d1` always increases, so the camera cannot double back
and nothing needs aligning by hand.

**D2, the gold fix.** Above the ice on 01, rebuilt out of three intersecting
range arcs on 02, eight source ticks on 03, one faint arc on 04, the common
centre of four mitigation circles on 05, full strength over the pulse field on
06, a single 6 px cross beside three columns on 07, the only bright mark above
the bed on 08, resolving into the Polaris on 09.

**D3, the riser chain.** Declared once as a list where every exit is the next
entry. 01 exits 980, 02 enters 980 exits 742, 03 enters 742 exits 1,106, 04
enters 1,106 exits 610, 05 enters 610 exits 928, 06 enters 928 exits 1,192, 07
enters 1,192 exits 520, 08 enters 520 exits 860, 09 enters 860 and dead-ends on
the anchor shackle. Exactly one frame terminates and it is the ninth.

**D4, the palette arc.** Each frame's water top hex is the previous frame's bed
hex, so the ladder is one continuous ramp across nine frames and is checkable
with one pixel sample per frame.

## THE ARC

| # | beat | window, m | temperature |
|---|---|---|---|
| 01 | HOOK. The duration asymmetry, at the rail | -6 to 30 | cool |
| 02 | PAYS OFF. What the sound is for | 0 to 120 | |
| 03 | What goes in, and on what cycle | 20 to 400 | |
| 04 | **BREATHER**, declared. The place itself | 380 to 1,000 | |
| 05 | Every zone in the permit at one true scale | 500 to 2,000 | |
| 06 | **THE TURN.** The unattended year | 800 to 2,600 | cold |
| 07 | **KEEPABLE.** Three columns of the same water | 1,000 to 3,000 | coldest |
| 08 | What the record is | 1,200 to 3,400 | |
| 09 | CLOSE. One ask | 1,200 to 3,400 | |

Breather 04. Keepable data slides 06 and 07. Temperature turns at 06.

Nine slides, which is inside the 8 to 10 default. Eight descending frames give
the mapping enough travel to read as a descent rather than as three arbitrary
crops, and the ninth holding the eighth's window is the camera's full stop.

## COVER

**Hook archetype, NEW: THE UNATTENDED MACHINE.** An establishing frame in which
the human working surface is at the very top edge and already leaving, and the
copy states the duration asymmetry between the people and the thing they left.
It is not the sentence that isn't there, because something is there. It is not
timeline collapse, because the frame holds one moment at one depth. It is not the
object you can see and can't read, because every mark in it is labelled.

> The ship leaves after 22 days. The sound stays 12 months.

Eleven words. C31 and C16.

## WHAT THE PROTOTYPE ALREADY SETTLED, so no dossier relitigates it

- The reserve is a BASIN handed to the field generators, never a punch. The punch
  shipped three hard-edged black rectangles on the first build and
  `AKENGRAVE.punchReserves` is out of this deck. Both treatments specified the
  punch; both are overruled by the render.
- `AKICE.rays` fills the column with the story's own geometry. Its parameters are
  `[design]` and every dossier bullet quoting a number from it says so.
- Depth labels are placed by `AKICE.railLabels` from the mapping and clamped.
- Every declared mark on the rail is drawn at findable weight, because two of
  five minor ticks read at or under the band's own texture on the first build.
