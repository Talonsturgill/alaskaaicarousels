# AUTOMATION RETRO -- run 2026-08-19, Carousel No. 37, "A Poll Is Not a Ballot"

Score 8.07 against a threshold of 8.0. Shipped and merged at 815dfd4.
Phase 12, upgrade engineer. Budget spent: 3 of 3 upgrades, all reactive.

---

## 0. THE STANDING REPEAT OFFENDER: WORKED, HALF OF IT

`trend_check.py --window 10` names **"Artwork craft and genuine detail"** the
weakest criterion in 7 of the last 10 scored runs, mean 6.55, last worked
2026-08-07, marked STALE. It scored 6.5 again here, so it is 8 of 11.

The mandate was to work it or say plainly why not. **It was worked, on one of
its two named halves, and the other half is parked with measurements.** The
scorer's one-sentence fix has two clauses and they are not equally tractable:

> "Re-cut the three line fields that dissolved in the render ... **and fill the
> bare-plate bands on 03, 05, 06 and 07 with the engraved relief those dossiers
> already promise in writing.**"

**The second clause is now machinery** (upgrade 2 below). The dossiers promised
a contact shadow on all nine slides; four slides declared one; machine_qa
reported no contacts at all on the other five. qa.py's contact gate is FITTED
(known-bad dL 1.24, known-good dL 8.1, FAIL under 4.0) and it is OPT-IN, so a
slide that never writes `data-contacts` is not judged rather than judged clean.
Five of nine slides skipped it silently. Two of those five, slides 03 and 06,
had the shadow DRAWN in their own canvas code and merely never declared it. The
proof: declaring slide 03's comb shadow and re-running the untouched qa.py
produces

    warn: contact shadow: 'the comb block standing on the plate':
          shadow L* 3.2 vs ground L* 9.4, dL 6.2 at 432w
          -- under the 8.0 L* comfort band; it reads, barely

That warn existed in the pixels of the shipped deck and no artifact in the run
ever printed it. From now on a contact shadow promised in the plan must be
declared in the markup or the promise struck from the plan.

**The first clause, the dissolved line fields, is PARKED with the measurements
that a future attempt should start from, not deferred silently.** What was
tried and what it cost is in section 4, and the numbers are in FIELD_NOTES
under 2026-08-19. The short version: a metric that separates the defect at
REGION level exists and is clean (the 605-stroke comb puts 71 percent of its
ink structure above the feed's Nyquist limit against 0.07 to 0.15 for every
piece of art in this deck the scorer praised), but run BLIND over tiles, which
is the only way it could ever fire without a declaration, it flags two tiles on
`examples/demo-deck` slide 03 and three on this deck's slide 08, both of which
are reference-quality art. A new FAIL fitted on one deck of ground truth, that
false-positives on the studio's own bespoke reference, is worse than no gate.
What would have to be true to tackle it: either (a) a `data-fields` declaration
across enough of the back catalogue to FIT a threshold the way
`encoding_reads` and `contact_reads` were fitted, which is a corpus exercise
and not an end-of-run slot, or (b) the arithmetic subset, which needs no
fitting at all: a slide that declares N countable marks in a band must give
them at least 2N feed pixels of span, and 605 marks across 339 feed pixels is
provably uncountable before any pixel is read. (b) is the recommended next
attempt and it is cheap once a mark-count declaration exists.

One thing to stop assuming: the pixel critics ALREADY receive the 432px thumb
(routine_instructions Phase 9 step 2, `assemble.py` thumbs/). They saw the
picture and passed the defect three rounds running. The missing instrument is a
number, not a smaller image.

---

## 1. REACTIVE RETRO, phase by phase against the spec

Evidence source: `out/2026-08-19/run_state.json`, `score_report.json`,
`render/machine_qa.json`, the storyboard, the slide sources, and the
showrunner's incident notes.

### D1. Date collision at wake (spec gap, no defect)
Anchorage read 2026-08-18 23:15 and `runs/2026-08-18/` already held No.36.
Overwriting shipped artifacts is forbidden by CLAUDE.md, so the run took
2026-08-19 and wrote its reasoning into `run_state.json.date_note`. Correct
call. **Nothing in the master prompt told it that**, and the same wake at the
same hour is now a daily-cadence certainty rather than an accident. Improvised
correctness is a coin flip repeated nightly. FIXED, upgrade 3.

### D2. dossier_check FAILED 9 of 9 on a formatting detail (defect, cost a pass)
`F4A_RE` demanded the field number sit OUTSIDE the emphasis
(`4a. **Lower-third treatment.**`). All nine dossiers were authored
`**4a. Lower-third treatment.**`, which is what SLIDE_DOSSIER_SPEC's own line
34 looks like when an author bolds the whole label. Every dossier failed with
"no field 4a", the least informative failure this gate can produce, and nine
correct paragraphs were re-formatted to satisfy a regex. FIXED, upgrade 1.

### D3. The encoding gate measures a MEDIAN and nothing said so (diagnosis cost)
Four slides measured 0.0 to 3.3 dE on `data-encodes` regions that differ
obviously to the eye, because `encoding_reads` compares the MEDIAN CIELAB of
each region and the median of a sparse stroke field is bare plate. Diagnosing
it needed a bespoke Playwright probe replicating qa's own measurement.
NOT FIXED THIS RUN, deliberately, and it is the strongest candidate for the
next run's slot. It is already instinct #130 and a FIELD_NOTES entry, so the
knowledge is captured; what is missing is one line of self-description in the
failure message. Recommended shape, which weakens nothing: keep the 4.0 floor
and the FAIL exactly as they are, and add to the failure text the region's INK
COVERAGE beside its median, plus the sentence "this is a median: a sparse
stroke field's median is its plate, so a density claim must be declared on the
inked marks and not on the band that holds them." Cost is small; it was not
taken because the two upgrades above and the wake fix are this run's whole
budget and the reactive-first rule ranks a shipped defect over a diagnosis
cost.

### D4. Round 1 returned "revise" on all nine slides, two systemic classes
(a) Every cast shadow in the deck was a `fillRect`, which welds into one hard
black plinth when objects sit closer than twice the shadow width and states a
light direction (straight down) contradicting the objects' own shading.
(b) Large flat fills where the deck's own line system forbids them, including
slide 08's two register front faces on the one slide whose palette rule also
says oxide is for small areas only.
Both were repaired by hand across eight slides. Neither is machinery yet.
Note (a) is the same family as the contact-shadow hole: the fitted contact gate
that would have measured a `fillRect` plinth as a shadow was not running on
five of the nine slides. Upgrade 2 makes it run. (b) is a palette-rule check
against `config/brand.yaml` and is written up as a recommendation, not built:
"large" and "small area" have no committed numeric definition anywhere in the
repo, and inventing one at the end of a run is exactly the guess the encoding
docstring exists to prevent.

### D5. A continuity device was specified that can't be built (defect, caught late)
Device B promised to cut a DATA OBJECT with the right frame edge on five
junctions. The plate ends at x1040 and the frame at x1080, so any such mark
leaves the sheet it stands on. Caught by a pixel critic in round 2, after the
storyboard had shipped the promise into five dossiers. This is a plan-time
geometry contradiction and it is checkable: the plate and frame extents are
constants. Not built this run (budget), and it is the cleanest application of
the frontier finding in section 3. RECOMMENDED as the next frontier slot.

### D6. Stamp geometry drifted across nine sheets (defect, caught by two critics)
Device C is declared a FIXED drafting title block and shipped round 2 at eight
different heights, jumping corners between slides 03 and 04. Two critics found
it independently, which is the signature of something a machine should own: a
device declared FIXED is a claim about coordinates, and coordinates are the one
thing a checker never gets wrong. Also not built this run; same family as D5
and the same recommendation.

### D7. Environment: clean
No installs, no 403s, no API limits, no retries. Playwright needed the explicit
`executable_path=/opt/pw-browsers/chromium-1194/chrome-linux/chrome` for one
scratch probe, already in FIELD_NOTES. The engine itself never needed it.

### D8. Gates that passed defects a later reviewer caught
- `machine_qa` PASS, 0 fails, 0 warns on all nine slides, while the scorer
  named three dissolved line fields and four bare-plate bands. The contact half
  of that is D-above and now closed; the field half is parked.
- `bespoke_check` drawn share 54 percent against the storyboard's own declared
  72 percent target. The gate's FAIL line is 45 percent, so 54 passed. The gate
  is doing what it was fitted to do; the STORYBOARD stated a target and nothing
  compared the outcome to it. Recommendation, not built: have the storyboard's
  declared drawn-share target be read by `bespoke_check` and reported as a
  variance line. It should stay a report, not a FAIL, because a target authored
  by the same run that is judged by it is the anchoring defect named in
  section 3.

---

## 2. THE RUBRIC'S WEIGHTS SUM TO 1.10 -- A PROPOSAL FOR THE MAINTAINER, NOT A PATCH

`config/scoring_rubric.yaml` carries ten criteria whose weights sum to 1.10,
not 1.00. The scorer noticed, reported the literal weighted sum (8.07) because
that is what the rubric instructs and because it is the only figure comparable
against every prior run, and raised it rather than silently correcting it. The
normalised figure would be 7.34.

**Nothing was changed here and nothing should be changed by a run.** This is a
positioning question with three possible answers and only the maintainer can
pick one:

1. **Leave it.** Every score in `ledger/` since the rubric shipped is on the
   1.10 scale, and the thresholds (8.0 at three iteration rounds, 8.3 at fewer)
   were set by watching decks scored on that same scale. The scale is
   internally consistent and 10 percent hot in a way that cancels out of every
   run-to-run comparison. Cost: the number is not what it says it is, and a
   reader who assumes a 10-point scale reads every run as better than it is.
2. **Normalise the weights AND raise the thresholds by the same factor** in one
   commit, so no run's ship decision changes and the back catalogue gets a
   restated column. This is the only option that is not a loosening: dividing
   the weights by 1.10 without moving the threshold would drop every future
   score by 10 percent against an unchanged bar, which would make the machine
   fail runs it currently ships, and doing it the other way round is worse.
3. **Publish both figures**, literal and normalised, in the score report and
   the email, and change nothing else. Cheapest, honest, and defers the choice.

The upgrade engineer's recommendation is (3) now and (2) at a moment when no
run is in flight, because (2) touches a threshold and thresholds are the
maintainer's call by the hard rules of this phase. **A run must never adjust
its own weights or its own threshold**, whichever way the arithmetic points.

---

## 3. FRONTIER SCAN

**Focus: (f) agent/automation workflow patterns for self-improving pipelines.**
The stalest rotation slot, last scanned 2026-08-05 (14 days), and distinct from
the last three logged foci: 2026-08-18 editorial dataviz, 2026-08-16 procedural
art, 2026-08-14 headless rendering. The two art slots that would most directly
stock the artwork-craft shelf, (b) and (c), are both blocked by the
no-repeat-in-3 rule, which is why the artwork work this run is reactive rather
than frontier.

**WebSearch was unavailable for the third time in six runs**: the session had
spent its entire 200-call budget before Phase 12, the same failure as
2026-08-14 and 2026-08-16, and the research phase is where it goes. There was
no discovery step. The scan ran on WebFetch alone against two indexes, which is
a narrower instrument and is recorded as such. 0 searches, 4 fetches, 2 papers
read.

**FINDING, and it is a good one: ORACLE ANCHORING.**
"Oracles That Cannot Fail: Anchoring and the Expectation That Moves With the
Fault", arXiv:2608.17214. The thesis in one line: *a test oracle that obtains
its expected value from the system it is judging cannot fail, because a fault
moves the measurement and the expectation together and the comparison cancels
exactly.* The paper distinguishes SPECIFICATION-ANCHORED expectations (composed
from values fixed OUTSIDE the code under test) from STATE-ANCHORED ones (values
that flow, directly or transitively, from that code), and measures the
difference on a deployed air-traffic simulator: re-anchoring one oracle on
published procedure, changing no production code, recovered 8 of 46 missed
mutants; state-anchoring a healthy oracle cost 4 of 19.

This names the deepest recurring defect in this studio's review loop, and it
names it better than the studio has. `dossier_check.py`'s own 2026-07-26
docstring already describes the mechanism without having the word for it: *"the
pixel critics grade each slide against its OWN dossier, so a slide that
executed a bad plan passes its acceptance checklist."* That is a state-anchored
oracle. This run produced two textbook instances:

- **D5, Device B.** The dossier said cut the data object with the right frame
  edge; the acceptance checklist said the same; the critic graded against it.
  Nothing in the loop held the value that would have killed the plan at plan
  time, which is the committed geometry: plate ends x1040, frame x1080.
- **D6, the stamp.** "Fixed drafting title block" was the expectation, and the
  expectation was re-read off each sheet as it was drawn.

The companion finding supports what upgrade 2 does: "Grounding AI Agents in
Contracts: An Empirical Evaluation of Spec-Driven Test Generation",
arXiv:2608.17177, measures that making an agent write down pre-conditions and
post-conditions BEFORE generating tests improves bug detection by 9.8
percentage points (p = 0.0352) and beats human-authored tests 56.7 percent of
the time. Declare the contract, then measure against it, is the pattern that
just closed the contact hole.

**PARKED, not applied**, because the machinery it implies is a new committed
geometry module plus a plan-time checker and that is not boundable in this
run's remaining budget: **a GEOMETRY ORACLE anchored outside the storyboard.**
The frame, plate, and safe-zone extents move into one committed constants file;
`dossier_check` reads a dossier's stated coordinates against those constants;
a device declared FIXED must state its box once and every slide's rendered
stamp must land there. Both D5 and D6 die at plan time, from values no run
authored. Full entry in `knowledge/FIELD_NOTES.md` under 2026-08-19, with URLs.

`scan_log` entry appended to `ledger/upgrades.json`.

---

## 4. WHAT WAS TRIED AND NOT SHIPPED (the dissolved-fields probe)

Measured on this run's own PNGs, design 1080 wide, feed 432 wide, so one feed
pixel is 2.5 design px and the finest cycle the feed can carry is 5 design px.
"hi share" below is the fraction of a region's ink structure that lives above
that limit, i.e. the fraction the downsample destroys. It is a Nyquist split,
nothing fitted.

    KNOWN BAD (scorer named these)
      S03 605-stroke comb, pitch 1.4px    hi_rms 7.88   hi share 0.71
      S04 hachure territory               hi_rms 6.58   hi share 0.15
      S05 stroke runs band                hi_rms 4.03   hi share 0.09
    KNOWN GOOD (scorer praised these)
      S08 registers                       hi_rms 5.77   hi share 0.10
      S07 feather wash                    hi_rms 6.03   hi share 0.11
      S01 streamline field                hi_rms 7.60   hi share 0.13
      S02 roll call                       hi_rms 5.97   hi share 0.11
      S09 count bar                       hi_rms 6.07   hi share 0.15
      S06 column band                     hi_rms 3.70   hi share 0.11
    CONTROLS
      S08 empty margin (grain only)       hi_rms 3.99   hi share 0.27
      S03 kicker, DOM text                hi_rms 4.48   hi share 0.17

Read honestly: the metric nails the worst offender with a 2.6x margin over the
noisiest non-defect, and it does NOT see the other two named failures, because
they are different defects wearing the same complaint. Slide 04's hachure reads
as fuzz for a tonal reason, not a resolution one, and slide 05's runs are
uncountable because the axis gives 5.7px per point, which is an arithmetic
problem and not a spectral one. One metric, one of three defects, one deck of
ground truth, and false positives on `examples/demo-deck` when run blind. Not
shipped. Parked with these numbers so the next attempt starts from evidence.

---

## 5. UPGRADES APPLIED (3, all reactive, all verified)

### 1. FIX -- the emphasis may open before the number (`scripts/dossier_check.py`)
`F4A_RE` now consumes an optional leading `**` or `__` before the field number,
so `**4a. Lower-third treatment.**` is found. This is not a loosening: a field
the gate can't FIND is a blanket fail with no information in it, and finding
it is what subjects it to the thinness floor and the modeled-tone test that are
the actual gate.

VERIFICATION. Reconstruction of the exact defect, the storyboard re-written to
the form the run actually authored: HEAD dossier_check FAILS 9 of 9 with "no
field 4a", exit 1. New dossier_check PASSES 9 of 9, exit 0. NEGATIVE CONTROLS
in the new form: a 28-character field 4a still fails on the 200-character floor,
and a 200-plus-character field naming only plate, hairline, rule, caption,
footer, fixture, label, counter and chip still fails on modeled tone, with the
flat furniture named. BACK CATALOGUE: `runs/2026-08-13`, `-14`, `-15`, `-16`,
`-18` all still PASS 9 of 9, unchanged.

### 2. FIX -- a contact shadow promised in writing must be declared in the markup
(`scripts/dossier_check.py`)
New one-directional cross-check. If a slide's dossier promises a contact shadow
and the slide source exists, its `<body>` must carry `data-contacts` with at
least one shadow region. An attribute present but empty (`[]`, or entries with
no `shadow` key) FAILS too, so the loophole is closed at the same time.
Deliberately one-directional: `data-breather` DISABLES a gate and is policed
both ways, while `data-contacts` ENABLES one, so declaring a shadow the dossier
never mentioned is a gain and is never flagged. Skipped entirely before the
build, so the planning-time run of this gate is unchanged. The failure message
carries the full declaration syntax and the alternative remedy (strike the
promise) so the repair is mechanical.

VERIFICATION. Reconstruction against this run's real artifacts: slides 03, 04,
05, 06 and 07 FAIL, naming exactly the five that promised a shadow and declared
none, and 01, 02, 08, 09 pass. Repair paths, all three tested on copies:
declaring slide 03's shadow clears it; declaring `data-contacts='[]'` on slide
04 fails with "carries data-contacts with no shadow region in it"; striking the
promise from slide 05's dossier clears it. END-TO-END: rendering the repaired
slide 03 through untouched render.py + qa.py produces a real measurement that
the shipped run never had, `shadow L* 3.2 vs ground L* 9.4, dL 6.2 at 432w,
under the 8.0 comfort band`. BACK CATALOGUE unaffected: `runs/*/` carries no
`slides/` directory, so the check is skipped there and all five re-checked runs
still PASS.

NOTE FOR THE SHOWRUNNER: `dossier_check` now reports FAIL on THIS run's own
`out/2026-08-19` artifacts, 5 fails. That is the reconstruction, not a
regression, and the deck has shipped. Do not re-sync the gate block into the
shipped run record.

### 3. FIX -- if the run date is already taken, take the next one
(`prompts/routine_instructions.md`)
Phase 0's date rule now says what to do when the run wakes inside the previous
run's date: the run date becomes the first date with no `runs/<date>/`
directory, the reason goes in `run_state.json.date_note`, never write into an
existing `runs/<date>/`, never renumber a shipped carousel, and do not ask.
Prose rather than machinery because the decision happens at wake, before any
gate exists to hold it, and the guardrail it protects (CLAUDE.md's ban on
overwriting shipped artifacts) is already absolute. What was missing was the
answer, not the prohibition.

VERIFICATION. Spec change, no code path. House rules checked on the added text:
no em or en dashes, no "cannot", ordinal date. The rule is a restatement of
what run No.37 actually did, so it is consistent with the shipped record.

### ENGINE REGRESSION CHECK (mandatory, both decks)
Neither upgrade touches `render.py`, `qa.py` or `assemble.py`. Re-run anyway:
this run's nine slides re-rendered 9 of 9 OK, 0 warnings, 0 errors, and qa.py
verdict PASS, 0 fails, 0 warns. `examples/demo-deck` rendered 4 of 4 OK and
qa.py verdict WARN with its usual busy-art-under-text and art-touching-glyphs
warns, unchanged.

---

## 6. RECOMMENDATIONS FOR THE MAINTAINER (not built, ranked)

1. **Rubric weights.** Section 2. Publish both figures now; normalise weights
   and thresholds together later, in a commit with no run in flight.
2. **The geometry oracle.** Section 3. Kills D5 and D6 at plan time from values
   no run authored. Best use of the next frontier slot.
3. **`encoding_reads` says it measures a median.** Section D3. One sentence and
   one extra statistic in an existing failure message; weakens nothing.
4. **Mark-count arithmetic for countable fields.** Section 0. A declared N
   marks needs 2N feed pixels. Needs a declaration, needs no fitting.
5. **The palette rule has no numbers.** D4(b). "Oxide is for small areas only"
   can't be checked while "small" is undefined in `config/brand.yaml`. If the
   maintainer will name a ceiling as a fraction of the plate, it becomes a
   gate; otherwise it stays a critic's job and should stop being written as if
   it were a rule.
