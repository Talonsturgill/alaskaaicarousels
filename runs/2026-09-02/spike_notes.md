# SPIKE — the paper edge medium, run before the storyboard

Built and rendered a single frame to test the run's declared craft attack, a
hero whose ground is a CONTINUOUS MEDIUM rather than a lit stage. Result is a
qualified pass and it changes the plan in three ways.

## What worked
- `AK.reliefShade` with a CUSTOM `height(u,v)` gives genuine per-pixel material.
  A sawtooth at sheet pitch, a rounded ridge profile `sin(pi*f)^0.55`, per sheet
  deterministic lean, fibre fbm and a lateral falloff produced real Lambert
  shading with self shadowing. Two lights, `{az:0,el:58,w:1.0}` and
  `{az:90,el:22,w:0.35}`, at strength 9, ambient 0.20.
- The dead zone problem IS solved. There is no region of the frame that is
  nothing; every square inch is material at some density.
- Bricolage Grotesque at 750 weight sets beautifully at 120px and is clearly
  distinct from the last four decks' faces.
- Render cost 6.4s per slide, which is affordable for nine.

## What FAILED, and this is the useful half

**1. A uniform medium is wallpaper.** The frame reads as corduroy or woven
cloth, not as a stack of ballots. Solving the dead zone by making everything
equally busy trades one doctrine failure for another, and the doctrine is
explicit that zero anchors equals wallpaper equals fail. THE MEDIUM NEEDS
STRUCTURE: varying sheet thickness, occasional gaps and blocks, a top and an
end to the stack, something occluding something else, and a literal anchor with
annotation furniture. Density must VARY across the frame and mean something.

**2. The sheet pitch was too fine to survive the feed.** 150 sheets over 1350
design px is 9 px per sheet, which at 432 px wide becomes about 3.6 px. At that
size the sheets stop being sheets and become a texture frequency. The medium
has to read AS ITS MATERIAL at thumb size or it is just noise. Target 60 to 80
sheets in a full height column, about 7 to 9 px per sheet at feed scale, and
carry the finer sheets only in a defocused far layer.

**3. The type reserve was a scrim, which is the exact thing this run said it
would not do.** A dark linear gradient in a fillRect over the lower third is a
plate laid on top of the medium, not a lane modelled into it, and a gradient
inside a fillRect is still a box as far as bespoke_check is concerned. The
reserve has to be made of the material: a region where the stack is genuinely
lower, or thinner, or turned away from the light, or where sheets have been
lifted out, so the tone falls because of something physical.

Also caught: the mono kicker at 0.8 opacity over the lit medium was close to
illegible, which is the DOM-only collision gate's blind spot showing up exactly
where the instinct ledger says it does.

## Carried into the storyboard
Every dossier must name what its weakest region carries AND must not answer the
question with uniform busyness. A medium with no structure is as dead as a hole.

## SPIKE V2, and the mistake is the finding

Rebuilt with 72 sheets per stack at 11.4 px pitch, two stacks, a table with a
lit pool, drawn polyline re-scoring per sheet, contact shadows and a film grade.

**The material problem is SOLVED.** Sheets read as sheets at full size, the
edges have real self shadow, the occasional proud sheet reads, and the pitch
survives the thumb. Cost 7.0s per slide.

**The composition regressed into the exact defect this run exists to attack.**
Two stacks standing on a table in the lower half left the top 35 percent as
empty room and both side margins bare, which is a textbook top-loaded
composition with dead zones, and the headline then had to be laid straight
across the art because there was no reserve anywhere else. I built the thing I
wrote the plan against.

The cause is worth naming exactly, because it is the trap the whole studio keeps
falling into. **A medium stops being a medium the moment you make it an
OBJECT.** Two rectangles of paper texture standing on a stage are objects, and
the frame around them is stage, and stage is where dead zones live. The
rectangles also read as slabs rather than stacks because their silhouettes are
razor straight, which is a fillRect wearing a texture.

**THE CORRECTION, and it is the original plan stated more strictly.** Get the
camera CLOSE ENOUGH THAT THE PAPER IS THE FRAME. Edge to edge, corner to
corner, with the room present only as a sliver or not at all. The two channels
become two columns of sheets meeting at a seam that runs the height of the
frame, not two objects with air around them. Then there is no stage, so there is
nowhere for a dead zone to be, and the reserve is a band where the sheets sit
lower or turn away from the key, which is a physical fact rather than a plate.

Three further corrections for the build:
- The silhouette of a stack must be IRREGULAR. Sheets jut and recess; a straight
  vertical edge reads as a slab. Vary the per-sheet x extent as well as its lean.
- The perspective convergence I wrote (0.012 of the vanishing offset) was far
  too weak to read and looked level. Either commit to a real projection or drop
  the pretence and shoot the stack square on.
- A radial "lit pool" under an object does not survive a film grade at 0.42
  alpha over a dark table. If a contact shadow is needed, the ground has to be
  genuinely lit first, and the pair has to be MEASURED with contact_probe.py off
  the render rather than computed, per the 2026-08-26 rule.

## SPIKE V3 and V4, and one genuine engine finding

**V3 solved the composition.** Paper edge to edge, two columns meeting at a
seam, no room and no stage anywhere in the frame. The single best move was
giving each sheet its own REACH toward the seam, so the central edge is ragged
rather than straight. That one line is what makes the field read as stacked
paper rather than as woven cloth, and it costs nothing.

**V4 found an engine gotcha that is not in SKILL.md.**
`AK.reliefShade` CANNOT BE CLIPPED. It writes with `putImageData`, and
putImageData ignores the canvas clip path entirely, so a `CX.clip()` around it
does nothing at all and fails SILENTLY. V4 clipped both columns to a ragged
bottom edge to make the stacks end; the clip was ignored, the paper ran to the
bottom of the frame, and the only trace of the intended edge was the contact
shadow drawn afterwards, which now sits across unbroken paper like a torn line.
The file's own header does say it replaces pixels including alpha, so this is
implied, but "it has no blend" and "it ignores your clip path" are different
sentences and only the first one is written down.

THE TWO CORRECT ROUTES, both already in the API:
- pass `mask(u,v)` returning silhouette alpha 0 to 1, which is the option that
  exists for exactly this, or
- render the relief into an offscreen canvas and composite THAT through the
  clip with drawImage.

Candidate Phase 12 upgrade, small and bounded: extend the `AK.optionContract`
notes so that passing `clip` (or calling it inside an active clip, if that is
detectable) is named, and add one line to SKILL.md's akrelief entry. A silent
no-op that survives a green render is exactly the class of defect the motif and
leader contracts were added for.

## WHAT THE BUILD TAKES FROM ALL FOUR SPIKES

1. Paper fills the frame. No stage, therefore no dead zone.
2. Per-sheet REACH makes the silhouette ragged and is what sells the material.
3. Sheet pitch about 60 to 78 over the full height, which is 17 to 22 design px
   and survives 432 px.
4. Density must vary across x (an fbm at about 3 cycles) or the field reads as
   a uniform weave.
5. The reserve is a SECOND MATERIAL at a different angle under a different key,
   reached with `mask`, never with a clip and never with a scrim gradient.
6. `strength` 13 with lights at az 345 el 56 plus a weak az 120 fill gives paper
   that reads as paper. Grade at exposure -0.04, contrast 1.08, vignette 0.17.

## SPIKE V5 — the mechanism is proven

Replacing the ignored `CX.clip()` with reliefShade's own `mask(u,v)` works
exactly as documented. The paper now genuinely ENDS on a ragged bottom edge, the
region below it is a different material, and the headline sits on it with wide
contrast and no scrim anywhere. Normal canvas draws (the seam gradient, the
sheet scoring) still respect a clip, so the pattern is: MASK the relief, CLIP
the drawing, and do both to the same edge function.

One residual, and it is a note for the build rather than a failure. The table
material under the reserve reads as a nearly flat dark field, because the film
grade's vignette and log contrast crushed a surface that was only lit to
`high:'#5A6450'`. A reserve made of a second material has to be lit enough to
SURVIVE the grade, or it becomes the flat plate it was supposed to replace.
Raise its high value and give it a real key before grading, then re-check.

The technique is settled and the build can start from it:
  reliefShade(paper, mask=edgeFn) over reliefShade(reserve material, lit)
  then clip the drawn scoring to the same edgeFn, then grade once.

## ROUND 4 — THE FIXES, AND WHAT THEY TAUGHT

Four pixel critics came back `revise` on every slide they were given, with two
factual hard fails and one slide arguing the opposite of its own claims. All
three were the same failure wearing three coats.

**A canvas mark that means "this row" has to READ the row.** Slide 07's spec
plate carries four stamped fields and the fourth is deliberately never struck,
which is how the deck draws "the ordinance carries no fiscal analysis" [C06,
C31] instead of asserting it. The four field markers were counted off the plate
RECTANGLE at a fixed 39 px pitch. The stamp text then wrapped to five lines
inside a 330 px box, every marker slid up one row, and the proud unstruck tab
landed on `AMENDABLE . NO`. The slide shipped a picture that said the ordinance
is unamendable-but-costed, which is the inverse of the claim it was built from,
and every machine gate passed it, because no gate can know what a rectangle
means. The fix is two-part and both parts matter: `white-space:nowrap` so the
line count cannot drift, AND the marker y values measured off
`getBoundingClientRect()` of the type itself at render time. Only the second
part would have survived a copy edit.

**A leader has to arrive at WORDS.** The same slide declared a 10 px leader from
(690,330) to (700,334) whose label was the whole plate's innerText run together,
`"EFFECTIVE . 2027 CYCLETERM . TWO YEARSAMENDABLE . NOCOST ."`. qa.py's
`leader_labelled` tolerance is 32 design px to the label's own box, and the
nearest real text was 800 px away at the bottom of the frame, so the
declaration was true of nothing. `NO PUBLISHED ESTIMATE` is now a real mono
label under the plate and the leader runs up the plate's left gutter, which is
the only column on that slide with no type in it.

**FRAME_BALANCE SEES STEPS, NOT GRADIENTS.** Slide 01's bottom third failed at
60 percent of its own average craft density. The instinct was more modelling, so
a `laneGrade` pass of 34 soft radials went into the near band. The bottom third
fell to 31 percent. `frame_balance` box-downsamples 6x before it measures, and
what survives that is a luminance STEP at cell scale, which a soft radial is
the precise opposite of; the pass added area at one tone and washed out the
arrises that were carrying the band. Heavier arrises did not move it either
(41 percent at 1.1 px, 41 percent at 2.9 px), because they were being drawn
under a bloom ellipse that then covered them.

What actually worked was subtraction. The text bloom's padding was
`half-width + 72` horizontally, which on an 880 px block is a 542 px radius
ellipse, a flat pale lane 1084 px wide across the whole lower frame. Cutting it
to `+58 / +32`, moving the feather stop from 0.66 to 0.50, and narrowing the
block itself to the width its longest line actually needs took the bottom third
from 41 to 46 percent and the ratio from 60 to 65. The dead lower zone was not
short of craft. It was covered.

Candidate Phase 12 upgrades from this round:
- `fanBloom`'s padding should scale with the SHORTER side of the text box, not
  be a flat constant added to the half-width. Every deck that uses a wide chip
  inherits this bug.
- `qa.py` could warn when a `[data-reserve]` block's rendered line count differs
  from its authored `<br>` count, which is the wrap-drift that broke slide 07
  and is invisible today.
