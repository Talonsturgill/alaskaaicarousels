# AUTOMATION RETRO — 2026-09-11 — Carousel No. 56

Written live as the run proceeds, per the rule that a retro assembled from
memory at Phase 12 loses the evidence. Phase 12's engineer gets this plus
whatever the later phases add.

## THE STANDING REPEAT OFFENDER, and what this run did about it

`scripts/trend_check.py --window 10` names **Artwork craft and genuine detail**,
weakest in 7 of the last 10 runs, mean 6.7, last reading 6.0, and records that it
was "worked 2026-09-10 (0 run(s) ago)".

This phase must do ONE of exactly two things with that and say which. **This run
WORKED IT**, in planning rather than in repair, and the finding below is the
concrete result.

## FINDING 1. THREE COMMITTED ART MODULES ARE INVISIBLE TO THE DIRECTORS ROOM

`assets/js/` holds twenty-two modules. `knowledge/TECHNIQUE_LIBRARY.md` indexes
akengrave as #93, akhachure as #92, aksnow as #91, aknight as #94 and the AKNIGHT
family as 94a to 94d. It does NOT index:

    akstipple.js   committed 2026-08-16 for No.35
    akparcel.js    committed 2026-09-04 for No.50
    akrail.js      committed 2026-08-16 for No.35
    akcolumn.js    committed 2026-08-27 for No.42
    akseam.js      committed 2026-09-02 for No.48

TECHNIQUE_LIBRARY entry 93 already diagnoses this exact failure, in its own
words, about itself: akengrave "was committed 2026-07-31 for No.21 and then LOST,
because it was never given a number here and the directors room reads this file.
Five consecutive decks did not use it and artwork craft was the weakest criterion
in four of them. That is the lesson. A capability that exists in code and not in
the index does not exist."

The lesson was written down and then the same thing happened five more times.

**Why it matters for the standing weakness specifically.** `akstipple.js` was
built to attack this exact criterion and says so in its own docstring, that
artwork craft had been weakest in 8 of 10 runs and that the cause is a smooth
rendered material having no marks in it while the whole detail budget lands in
annotation furniture that concentrates where the labels are, which are up top,
"which is also, precisely, why top-loaded composition is the number one recurring
machine warn. The two findings are one finding." `akparcel.band` implements the
order rule that fixes the flat mid band the scorer has named in 8 of the last 10
runs. Neither was reachable from the file the directors room reads.

**PROPOSED UPGRADE, kind fix**, for Phase 12 to implement and verify. Index all
five in `knowledge/TECHNIQUE_LIBRARY.md` with numbers, the API surface, the
contract rules each enforces and the run each was built for. Then add a check
that FAILS when a module exists in `assets/js/` and no line in
TECHNIQUE_LIBRARY.md mentions its filename, so this can't silently recur a
seventh time. The check is the real deliverable; the index entries are the thing
it protects.

## FINDING 2. A MACHINE-QA PASS AT ZERO WARNS PASSED A SLIDE WHOSE RESERVE READ AS THREE BLACK PLATES

Measured this run, on a throwaway prototype built before any slide was planned.
A slide calling `AKSTIPPLE.reserve('[data-reserve]')` and nothing else returned
`verdict: PASS, fails=0, warns=0` and rendered three hard-edged dark rectangles
where the type sat. akstipple's own docstring predicts it, that a hard hole
"reads as a black rectangle at feed size, which is the very thing plates were
supposed to avoid", and records that prototype P6 shipped exactly that on No.35.

The fix that worked is a basin term inside `height()` so the field's own density
falls where the words go, with the suppression pass only finishing the job. It
is written up in full, with the code and the measured constants, in
`out/2026-09-11/storyboard_header_draft.md`.

**This is a candidate for machinery rather than prose.** The honest version of
the check is hard, because a correctly ramped basin and a hard punched hole differ
in gradient rather than in presence, and a threshold fitted to one deck's field
density would cry wolf on the next. NOT proposing a gate on it today. Proposing
instead that the basin idiom go into akstipple.js as an exported helper, so the
right thing is the easy thing, and that the docstring's warning be promoted from
a paragraph to a named function.

## FINDING 3. BEAT D DID NOT RETURN BEFORE SELECTION

Five of six scouts returned inside the window the showrunner used to merge and
select. Beat D, policy and money, returned afterwards, and it was carrying the
run's best primary-sourced find, the FERC notice of September 4th accepting
DeepGreen's application and opening a comment and intervention window that closes
November 2nd.

No harm this run. The story was already tracked in `ledger/docket.json` from
yesterday and the selection did not need it. The process risk is real though: the
showrunner wrote `scout_merge.md` with a "Beat D did not return" section in it
and had to amend the record minutes later.

**NOT PROPOSING A FIX YET.** The obvious one, block until all six return, is
worse than the disease, because it would have idled the run behind its slowest
scout for the whole sweep. The better shape is for the merge step to record which
beats it actually had, which this run did by hand. Flagging it for Phase 12 to
judge rather than prescribing.

## GATE AND ENVIRONMENT OBSERVATIONS, no action proposed

- `bootstrap.sh` reported "pypdf import broken (likely cryptography rust-binding
  panic); repairing..." and then "pypdf import: repaired". Self-healing worked.
- GPU PBR was probed live today against `examples/proof-3d` and renders in 5.1s
  to 7.6s per slide with zero render errors, so akthree is available to this
  deck. The example's own slide 03 carries a pre-existing FAIL for canvas ink
  inside a reserved line box, which is the example's content and not the engine.
- `scripts/dedupe_check.py` did most of this run's editorial selecting, screening
  five candidates and clearing exactly one. It is doing its job well.
- `gate_status.py` read `site_fresh` PASS and `docket_dates` PASS immediately
  after Phase 3.5 and 3.6, which is the cheapest confirmation available that
  those phases landed consistently.

## THE ONE THING TO CARRY INTO THE FRONTIER SCAN

The scan focus must differ from the last 3 runs' `scan_log` entries. 2026-09-09
was focus (a), LinkedIn platform. 2026-09-10 was mezzotint and printmaking craft,
plus a LinkedIn secondary sweep. The rotation suggests procedural art portable to
offline Canvas or SVG, typography craft, headless-rendering capabilities, or
accessibility and PDF changes. Given Finding 1, a scan on self-improving-pipeline
patterns would be self-serving and probably right.

## FINDING 4. THE CONTACT TRIPLE HAS NO SAFE DEFAULT, AND SIX SLIDES GOT IT WRONG THE SAME WAY

Measured this run at Phase 7. Six slides declared a `data-contacts` pair with
the shadow rect stacked 46 design px ABOVE the ground rect, which is the shape a
reader of the rule "shadow and ground within 96 design px" naturally writes. All
six failed, and all six failed identically, with the shadow reading 12.9 to 15.2
L* LIGHTER than the ground it is supposed to sit on.

The cause is geometric and it is not obvious from the rule. `S.litPool` is a
radial gradient brightest at its centre. A ground rect stacked below the shadow
lands on the pool's dark outer edge, so the pair measures the pool's falloff
rather than the cast, and the sign comes out backwards. `contact_probe.py`
diagnoses this in one line and the line is exact, that the two rects belong side
by side at the object's own base line. Nothing in aksheet.js, the slide contract
or the dossier spec says so.

There was a second, independent error underneath it. The casts were placed at
`foot+14` with `dy:2` while the tight cast term is only about 7.5 design px in
half-height, so at the base line the cast contributed almost nothing and the
probe measured a 1.8 L* separation on a correctly signed pair. Lifting each cast
to `foot+2` and dropping each pool centre to `foot+14` took the six to between
12.6 and 14.9 L*.

**PROPOSED UPGRADE, kind fix, for Phase 12 to judge.** The knowledge is already
in `contact_probe.py` and it is only reachable by a run that has already failed.
Two candidates, in preference order. First, an `S.contact(cx, {cxm, foot, w})`
helper in aksheet.js that draws the triple in the measured geometry and RETURNS
the two rects to declare, so the declaration is a product of the drawing rather
than a second guess at it. Second, failing that, `qa.py`'s contact failure text
should name the stacked-rect case explicitly the way contact_probe does, because
qa.py is what a run reads first and its current remedy ("light the ground first")
sends the author to the pool when the pool was never the problem.

The measured constants and the before and after numbers are in the BUILD
RECONCILIATION section of `out/2026-09-11/storyboard.md`.

## FINDING 5. THE CONTACT GATE MEASURES A DIFFERENCE AND A DIFFERENCE HAS TWO SIDES

This is the sharpest machine finding of the run and it is a direct sequel to
Finding 4.

`qa.py`'s contact check measures `dL = ground - shadow` against a 4.0 floor and
an 8.0 comfort band. Having fixed the geometry in Finding 4, this run widened dL
the cheap way, by raising the lit pool's alpha, and every one of the nine slides
returned PASS. Then five pixel critics read the nine slides independently, in
five separate sessions with no knowledge of each other, and every one of them
called the pool a lens flare, a bloom, a glow sticker or a blob. Nine of nine.
The words were nearly interchangeable.

**A machine PASS was not merely uninformative here. It was the failure wearing
the gate's own badge.** The gate exists to catch an object that floats. A ground
lit brighter than the object standing on it is an object floating over a light
source, which is the same defect, and the measurement cannot tell the two apart
because it only reads a difference.

`TECHNIQUE_LIBRARY` entry 94a already carries the warning, in these words, about
No.49: tuned until they measured dL 35 to 45, "the pools read as stage
spotlights". The entry is correct, it is indexed, and this run read it, and the
run still did it, because 94a reads as advice about overshooting a number and
the actual rule is about WHICH TERM you move.

**PROPOSED UPGRADE, kind fix, for Phase 12.** Add an absolute ceiling to the
contact check, independent of dL. The ground patch's L* must not exceed the
sheet's own margin median by more than a fixed margin (the six corrected slides
here sit 6 to 11 L* over their margin, and the versions the critics rejected sat
20 to 30 over). It is one extra sample per slide, the margin median is already
computed for other checks, and it converts an aesthetic judgement five critics
made in parallel into one number the run cannot argue with. The remedy string
should name the term to move, because `qa.py`'s current text says "light the
ground first" and sends the author to the pool when the pool is the problem.

The fix as shipped is in `assets/js/aksheet.js`: `litPool` peaks at 0.28 and is
documented as a lift rather than a lamp, `cast` gained `k` so separation is
earned from the shadow side, and the cast is biased along `S.LIGHT.azDeg` by
default, because a symmetric shadow is a vignette and not a shadow. The usable
band is narrow in both directions and is written into the module: under about
0.18 the ground has no headroom left and the cast has nothing to subtract from,
which is the same failure from the other side.

## FINDING 6. A DATA-IN-ART ENCODING WAS DRIVEN BY NOISE AND NO GATE LOOKED

Slide 06's thirty four struck cells each carried a short rule whose length came
from `AK.fbm2`. It looked exactly like a small multiple of a daily reading. It
encoded nothing. `dossier_check`, `aggregate_check`, `plan_drift_check` and
`qa.py` all passed the slide, because every one of them checks that a DECLARED
quantity is present and correct, and none of them can ask whether an undeclared
mark that LOOKS like data is data.

Fixed here by driving the bars from `ledger/gaswatch.jsonl`, the real series,
frozen into the slide as literals with the window stated on the sheet. That is
the right fix for this slide. The general problem is open, and it is the one
worth Phase 12's attention: the deck's law is that art encodes a story number,
and a run can satisfy every gate while drawing a number it made up.

No check proposed, because the honest one is hard. Flagging it as the most
valuable unguarded surface currently in the machine.

## FINDING 7. THREE CRITICS REPORTED A CURLY APOSTROPHE THAT IS NOT IN THE SOURCE

Three pixel critics, in three separate sessions, independently reported U+2019
in the rendered type and marked it a hard fail against the house straight-quote
rule. All nine slide sources were scanned for U+2018, U+2019, U+201C, U+201D and
the en and em dash. All nine carry zero. The glyph they are reading is Manrope's
own design for U+0027, which has a slight comma form at display sizes.

**This costs real budget.** It is a hard-fail report, it arrives from several
independent reviewers at once, which is exactly the pattern that normally means
a finding is true, and it takes a run several minutes and a scan to refute. It
will recur on every deck that sets Manrope, which is most of them.

**PROPOSED UPGRADE, cheap, for Phase 12.** A one-line source scan already exists
in spirit in `style_lint.py`. Make it explicit and print its result into the
GATE STATUS block as its own row, something like `quotes  clean, 0 smart quotes
in 9 slide sources`. A critic reading a green row for this will spend its
attention on the picture instead. Better still, say the same thing in the
pixel-critic brief, because the brief is what the critic actually reads.

## FINDING 8. THE DECK'S HARDEST DEFECT THIS RUN WAS INVISIBLE TO EVERY GATE AND OBVIOUS TO A PERSON

Slide 03 drew Yukon as ocean. Everything east of the 141st meridian inherited
the water fill, producing a ruler-straight diagonal that was the most
conspicuous line in the window, on the sheet titled "This is the ground that can
be drawn".

`qa.py`, `dossier_check`, `bespoke_check`, `aggregate_check`, `plan_drift_check`
and `copy_sync_check` all passed that slide. `bespoke_check` even scored the
deck's drawn share at 67 percent, counting those pixels as craft.

The same fault, less severely, is still on slide 05, where the state boundary is
stroked with the coastline and reads as a straight edge across the frame.

**The general shape is worth Phase 12's judgement.** Any sheet that draws
`alaska-state.geo.json` and fills its complement with a water tone asserts that
everything outside Alaska is sea. A check could be cheap: when a slide fills a
non-state region, require either a land tone or a declared ocean clip. There is
a gazetteer and a geodata directory in this repo already, so the ingredients
exist. The reason to prefer a gate here over a note in the doctrine is that this
run had the doctrine and made the mistake anyway.

## FINDING 9. THE RUN'S OWN GATE TABLE WAS STALE WHEN THE SCORER READ IT, AND THE SCORER SCORED THE TABLE

The scorer's third hard fail was "any placeholder, lorem, TODO, or unfinished
element in any artifact", and its evidence was the GATE STATUS block inside
`storyboard.md`, which read `[FAIL] copy_sync` and `>> 2 FAIL row(s)`.

That block was true when `gate_status.py --sync` last wrote it and false by the
time the scorer read it, because the run had fixed copy_sync and had not
re-synced. The scorer was right to fail it. A generated block that says FAIL is
an unfinished artifact whatever the underlying state is, and a reader of the
storyboard has no way to know it is stale.

**This is a sequencing defect and it will recur.** `--sync` is the only thing
that refreshes the block, the routine names it at a couple of points, and any
fix made after the last sync leaves a lie in the record. The run has to
remember; nothing enforces it.

**PROPOSED UPGRADE, cheap and narrow.** Stamp the block with the time and the
artifact hashes it was generated from, and have `gate_status.py` print a loud
STALE line when the artifacts on disk no longer match that stamp. `assemble`
already does exactly this for renders ("STALE BUILD: slide-02.png changed since
assemble"), and that message is what caught two stale reviews this run, so the
pattern is proven in this codebase. Better still, make the scorer's brief say to
run `gate_status.py` itself rather than read the block, but the stamp is the
real fix because the block is also what a human reads in the ledger afterwards.

## FINDING 10. REVIEWERS READ A MOVING TARGET, TWICE, AND THE RULE THAT CAUSED IT IS A GOOD RULE

Three times this run a reviewer was reading artifacts the run was still
changing. The pixel critics for 04 and 05 returned findings about a version the
flow-critic round had already replaced. The first scorer read a `storyboard.md`
gate block that had gone stale minutes earlier, and correctly failed the run for
it. The second scorer was launched and then the run kept fixing slides 04 and 06
underneath it.

The cause is the routine's own rule, and the rule is right: NEVER END A TURN
WHILE A SUBAGENT IS OUTSTANDING, keep working inside the turn. A run that obeys
it and has independent work available will inevitably touch the artifacts a
reviewer is reading, because the independent work IS the artifacts.

**NOT proposing that the rule be weakened.** Idling a run behind its slowest
reviewer is worse, and this run got a great deal done in those windows.

**PROPOSING a cheap discipline instead, for Phase 12 to judge.** Snapshot what a
reviewer is asked to read. `assemble.py` already writes sha256 for every slide
source into `assemble_report.json`, and `render.py` already prints `STALE:
slide-02.html changed since its PNG was made`, so the machinery exists. A
reviewer brief could name the assemble report's hash, and the run could check
that hash before acting on a returned verdict, so a stale finding is identified
as stale rather than argued with or, worse, re-fixed. Cheaper still: copy the
render dir to `out/<date>/review/<n>/` before spawning a review round, and point
the briefs at the copy. Then the run may edit freely and every verdict names a
version that still exists.

The cost of getting this wrong is not small. This run spent real budget
re-checking findings that were already fixed, and the one time it did NOT check,
it would have re-broken a slide.

## FINDING 11. TWO COMMITTED GEODATA FILES ARE EMPTY STUBS AND A DOSSIER PLANNED AGAINST THEM

`assets/geo/ak-transmission-69kv.geo.json` and `assets/geo/ak-generation-20mw.geo.json`
are both committed, both non-trivial in size (8.4 KB for the transmission file),
and both contain ZERO features and no `type` key.

Slide 03's dossier named them in its technique stack and its layout map, called
for them at `W.hair`, and specified a compilation note crediting them. The slide
loaded them, drew them, credited them, and rendered nothing. The scorer read the
window as "wallpaper" and said the promised layers "are not visible at all",
which was correct, and the reason was not the drawing.

**This is worse than a missing feature.** A run can look at a 8.4 KB file in
`assets/geo/`, see it referenced in `CLAUDE.md`'s asset list, plan a sheet around
it, and get no error at any point, because `fetch` succeeds, `JSON.parse`
succeeds, and `d3.geoPath` of an empty collection draws nothing silently. The
failure mode is a slide that is quietly emptier than its plan, which is exactly
the shape of this deck's standing weakness.

**PROPOSED UPGRADE, cheap, for Phase 12.** A `parsers_check`-style assertion over
`assets/geo/*.geo.json`: every file must parse, carry a `type`, and hold at least
one feature, or the check fails and names the file. It is a few lines, it runs in
milliseconds, and it would have moved this from a scorer's aesthetic finding at
the end of a long run to a red line at the start of one. Either backfill the two
layers or delete them, because a committed empty stub is a trap for every future
dossier that reads the asset list.

## WHERE THIS RUN LANDED ON THE FOUR RECURRING DEFECT CLASSES

`trend_check --window 10` names four classes that keep shipping. This run's
final `machine_qa` carries six warns and no fails, and it is worth saying which
of the four survived and why, because "we warned about it again" is not a
result.

- **canvas mark near reserved text**, in 4 of the last 10. GONE this run, zero
  instances. The chassis is the reason and it is the one place the structural
  bet paid in full: art lives inside a neatline and type lives in the margin, so
  the class is mostly unreachable. The instances that DID appear, twice on slide
  04 and twice on 06, were all margin-plane FURNITURE, a Scotch rule, an axis
  rail, a gold rule, a machined rail, drawn without consulting the reserve. That
  is the chassis's real gap and it is worth a Phase 12 look: `S.marginField`
  knows where the basins are and nothing else in the module does.
- **contact shadow**, in 4 of the last 10. STILL PRESENT, four warns, all of the
  "reads, barely" kind between 6.1 and 7.9 L* against an 8.0 comfort band and a
  4.0 floor. This is now a deliberate position rather than a miss. Findings 4
  and 5 record what happens when a run chases the number: the five slides that
  measured 12.6 to 14.9 L* were the five every critic called lens flares. The
  band between "reads" and "reads as a lamp" is narrower than the rubric
  implies, and this deck sits at the bottom of it on purpose.
- **busy art under text**, in 5 of the last 10. TWO instances, both on objects
  the dossier deliberately puts type on: the gold tab on the tariff volume and
  the model string on its machined rail. Both were adjudicated legible by a
  critic reading the pixels at 432px. This class may simply be a warn the house
  ships past when the object under the type is the point.
- **top-loaded composition**, in 5 of the last 10. ONE instance, slide 06, whose
  bottom third carries 50 percent of its own craft density. Attempted twice: the
  volume was run the full margin width, and the machined rail was extended under
  both mono blocks. The second attempt was REVERTED because the rail's own mid
  value cannot carry either bright or dark type at 4.5:1, and trading a
  composition warn for a contrast warn is not a trade. The honest read is that a
  sheet whose subject is a 36-cell grid has its mass up top by construction.
