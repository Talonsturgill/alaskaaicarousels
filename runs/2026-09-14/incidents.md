# SHOWRUNNER INCIDENT NOTES -- 2026-09-14 (No.59)

Running list for Phase 12. Written as they were found, not reconstructed at the end.

## 1. AKHOLD.contact painted the brightest thing on nine frames out of nine

The shared contact routine laid a SCREENED radial blob of rgba(196,216,232)
DOWN-light of every foot in the deck. Five pixel critics reviewed the nine
frames in parallel, in five separate contexts, with no shared state, and five
of them named it. Three of them reached for the same phrase, a glowing
manhole. One stated the physics the routine had inverted: ground down-light of
an object is the ground in shadow, and that is where the brightest paint was
going.

The routine's own comment block argued for it, at length, and the argument was
not stupid. "On a near black floor the cast has nothing to darken and the
object floats" is true, and qa.py's contact rule does fail exactly that. The
mistake was answering a MEASUREMENT problem with PAINT. What the nine frames
were actually missing is the long shallow cast an object throws at elevation
12, and not one of them had one, on any frame, in any run using this routine.

Fixed in this run. The cast is a tapering quad inside a squashed transform and
the lit ground became the slide's to ask for, hard edged and never additive.

**The Phase 12 question is not the fix, it is the detection.** This shipped in
every deck this routine has drawn. qa.py measured the dL between two declared
rects and was satisfied, because a bright pool beside a dark hole passes a
difference test perfectly. A gate that measures a DIFFERENCE cannot see a frame
whose brightest region has no source. Proposal, a qa.py row that finds the
frame's brightest connected region and fails it when it is an unexplained
radial gradient sitting on the ground plane with no emitter declared.

## 2. Five critics, five contexts, one finding: the fan-out is worth its cost

Related to 1 and worth writing down on its own. The five pixel critics were
given disjoint slides and no shared memory. The systemic defect was found five
times independently, which is what made it credible enough to change a shared
library mid-run rather than patch nine slides. A single critic reading all nine
would have found it once, and once reads as an opinion.

## 3. caption_check reads a URL slug as prose

`config/brand.yaml` bans the phrase "cutting-edge". The primary source behind
C13, the $250,000 planning award, is a CMS press release whose URL slug
contains it. `caption_check --copy` hard-failed `first_comment` on the slug.

A banned phrase is a house VOICE rule. A URL is a quoted address and not the
house's words, which is the same reasoning the script already applies to a
brand.yaml phrase inside a straight-quoted verbatim passage, where it warns
rather than fails. The carve-out simply does not extend to URLs.

This run chose to lose the link rather than hand-weaken a gate mid run, and
declared the omission in the Gmail draft's editor notes. That is the wrong
trade to have to make: a correct artifact lost a primary citation to a gate's
model of what counts as prose.

Fix, Phase 12, reactive. Extend the existing verbatim carve-out to URL tokens.

## 4. A dossier acceptance item asked for a string a maintainer rule bans

Slide 08's dossier required the footer to print "BY OUR COUNT" verbatim, and a
pixel critic correctly graded it a hard fail for missing it. `caption_check`
then correctly hard-failed the restored string, because the maintainer rule of
2026-08-05 bans first person in type on a slide, full stop.

Both were right about their own rule and the two rules contradict. The deck now
prints "NOT A STATE CATEGORY.", which names what the qualification IS rather
than who made it, and is the stronger line.

Fix, Phase 12, proactive. The directors room writes acceptance checklists by
hand and nothing checks them against the house rules the gates enforce. A
`dossier_check` row that runs the slide-string rule table over every quoted
acceptance string would have caught this before a frame was drawn.

## 5. Three headlines diverged from their dossiers and nothing noticed until Phase 8

Slides 03, 04 and 06 authored three display lines against dossiers that
specified two. qa.py passed all three, because it checks line ENDS for ragged
breaks and the declared `maxLines`, and all three declared 3. The dossier said
2. Two pixel critics found it by reading the dossier and counting lines in the
picture.

The build was right to diverge on 04 and wrong on 03 and 06, which is exactly
the judgement a reconciliation section exists to record. The point is that the
divergence was invisible to every gate.

Fix, Phase 12, reactive. `copy_sync_check` already compares copy.json to the
render. The same comparison against the dossier's authored line count is cheap
and would fire at the moment of divergence rather than three phases later.

## 6. Slide 04's coastline, left on the table in round 2 and closed in round 3

The dossier's literal anchor for slide 04 is the Alaska coastline through the
aperture, projected true through AKGeo and drawn stroke only. Round 2 shipped a
graded world and a procedural fbm ridge instead, a pixel critic graded it a
major finding, and it was recorded here rather than quietly dropped.

CLOSED IN ROUND 3, after the scorer's one-sentence fix named it. The frame now
draws assets/geo/alaska-state.geo.json through the house conic at parallels 55
and 65, zoomed 5.4x onto Norton Sound, land filled and shore stroked struck
then lit, smeared with the same 14 px flight-vector convolution as everything
else inside that aperture. The second scoring round still reads the result as
two closed blobs rather than as a recognisable coast, which is a framing
question rather than a missing anchor, and it is the next thing to work on
this frame.

## 7. A shared library changed and three frames kept the old render

Round 2 fixed `AKHOLD.contact` in `assets/js/`, then re-rendered with `--only`
listing the slides whose own HTML had changed. Slides 01, 02 and 07 had not
changed, so they were not re-rendered, and three of the nine frames in
`final/` still carried the exact additive pool the round existed to remove.
The contact sheet the flow critic read was two thirds repaired and one third
stale, and it caught it: "the glowing manhole the round 2 fix exists to
remove, still present on the deck's first frame".

`render.py` already prints a STALE warning when a slide's HTML is newer than
its PNG. It has no way to know that a file under `assets/js/` moved
underneath a slide that did not change.

Severity is high and it is not this run's alone. A shared-library fix is
exactly the kind a run makes when a defect is systemic, which is exactly when
a partial re-render is most damaging, and nothing would have caught it if the
flow critic had happened to look at 05 rather than 01.

Fix, Phase 12, reactive and cheap. `render.py` already resolves `@@ASSETS@@`
and knows every asset each slide loads. Hash the resolved asset files into the
staleness test, so a slide whose HTML is unchanged but whose `akhold.js` is
newer than its PNG is reported STALE like any other.

## 8. The lit sliver was propping up nothing

Round 2 answered qa.py's contact floor on near-black frames by adding `o.lit`
to `AKHOLD.contact`, a hard-edged low-alpha sliver up-light of the foot. The
scorer named it as the same defect in a second costume, an unexplained
highlight beside an object, and on slide 04 it was the brightest pixel in the
frame.

Round 3 deleted it from all six frames that used it and every contact still
cleared the floor, because the raised floors and the real directional casts
from round 2 were already doing the work. The sliver had never been load
bearing; it was added in the same breath as the fix that made it unnecessary
and nobody measured whether it was still needed.

The lesson is narrow and worth keeping: when a fix and a workaround ship in
the same round, remove the workaround and re-measure before believing you
need it.
