# AUTOMATION RETRO — No. 18, 2026-07-26

Phase 12. The machine, not the content. Written by diffing
`out/2026-07-26/run_state.json`, `storyboard.md` (BUILD RECONCILIATION,
PIXEL REVIEW ROUND 1, FLOW REVIEW), `score_report.json` and the
showrunner's incident notes against `prompts/routine_instructions.md`.

Phase completion per run_state.json: wake, craft_refresh, research,
claims, docket, selection, directors_room, copy, art_build, pixel_review,
flow_review, assemble, scoring all `done`; ship/upgrade/gmail/retro
pending at the time of writing. Every named artifact exists and parses.
No phase was skipped. The deviations are all inside phases that reported
success.

---

## D1 (DOMINANT). One defect class shipped past a green gate five times,
## and twice the fix for one instance manufactured the next.

Evidence: `machine_qa.json` = PASS, 0 fails, 0 warns, and the generated
GATE STATUS block shows `[PASS] qa.py PASS, 0 fails, 0 warns` — while all
of the following were live in the render:

| # | Slide | Defect | Caught by |
|---|-------|--------|-----------|
| 1 | S03 | only FOUR of five insulator bells countable, the fifth occluded by a label plate, against a printed list of five commitments | pixel critic |
| 2 | S05 | the twelve parcel ISOTYPE tiles clipped out of their own frame; the slide asserted TWELVE PARCELS and showed four slivers | pixel critic |
| 3 | S05 | a scotch rule crossing the headline's final period, rendering as a DASH appended to "kilowatts." on a deck whose house rule forbids dashes | pixel critic |
| 4 | S06 | an opaque `.dead` plate overprinting the bottom third of `STATE AGENCY AI AND ELECTION DEEPFAKES` (scoring cycle 1 HARD FAIL). A first repair SHORTENED the string, reduced the overlap and did not clear it, and qa still said PASS | scorer |
| 5 | S02 | the counter note widened to 540px ran 62px past the adjacent opaque `.callout` plate, clipping one line and overprinting another, while a span added for the flow critic struck through a third (scoring cycle 2 HARD FAIL, NEW, created by the cycle 1 repair to that same block) | scorer |

Two structural facts about this list:

1. **The engine had two gates aimed at this neighbourhood and both were
   blind to it.** `text_collisions()` compares GLYPH LINE BOXES only, so
   an opaque element's BACKGROUND is invisible to it. Measured on the
   reconstruction: the `.dead` plate covers the subtitle's line box by
   113 x 17px, but the two elements' *text* line boxes intersect at a
   ratio of ~0.21 against `min_overlap = 0.30`. It is not that the
   threshold was too loose; the plate's ink was never in the comparison.
   `glyph_ink_contamination()` (added 2026-07-25) measures a ring around
   glyph ink for foreign ink OF THE GLYPHS' OWN VALUE — a plate that
   *covers* glyphs removes the ink instead of touching it, so that gate
   is structurally silent here too.
2. **A positional fix DELETED a feature in another region.** Raising
   S04's pull-quote plate in the pixel round buried the slide's lit
   point, so the deck's declared spine read ABSENT at the exact midpoint
   of the filmstrip and two of slide 4's own acceptance checks failed.
   The pixel critic had already signed off on that slide; only the FLOW
   critic caught it. The repair loop has no gate that re-asserts a
   slide's own acceptance checks after a positional edit.

Deviation from spec: none of the Phase 8/9 instructions were violated.
This is a gate-coverage hole, which is exactly what Phase 12 exists to
close. FIXED THIS RUN for the plate-over-type half (see UPGRADE 1); the
countability half (bells, tiles) is NOT machine-checkable today and stays
a critic responsibility.

---

## D2. An AKPOST call with the wrong parameter shapes silently blanked an
## entire art canvas, and BOTH engine gates passed it.

The first S01 render reported `errors=0` and produced a fully black art
canvas: `AKPOST.grade` was called with `contrast` as an object
`{amount, pivot}` and `lift`/`gain` as hex strings inside an undocumented
`split` wrapper, where the contract wants a number and two 3-element
arrays. NaN propagated through the tone LUT and every pixel wrote 0.

Reconstructed against the PRE-upgrade engine this run (scratch dir
`akrecon_old`):

```
[OK ] slide-01.html -> slide-01.png  5088ms  warnings=0  errors=0
page_errors: []   console_errors: []
canvas health: [{'w':1080,'h':1350,'area_frac':1,'mean':1.5,'variance':5.1,'sample_ok':True}]
qa.py: [ok  ] slide-01.html  fails=0 warns=0   verdict: PASS
```

Two findings sharper than the incident note. (a) `render.py` was silent,
as recorded. (b) **`qa.py` would ALSO have passed it**: the dead-canvas
FAIL fires below `variance < 3.0`, and the blanked frame measured
variance 5.1 (the +-1 LSB IGN dither and a few surviving pixels lift it
over the line). The canvas-health block the showrunner read by eye was
the only signal in the machine, and even it did not cross a threshold.
`akpost` had no argument validation at all: a wrong shape was coerced,
and an unknown key (`split`) was silently ignored. FIXED (UPGRADE 2).

---

## D3. The copywriter, not a gate, caught two killed claims sneaking back
## as superlatives.

`Alaska's working AI load` (S05 headline) and `Alaska's working data
center` (S04 annotation) both reached slide HTML. The underlying Alaska
data-center count had been explicitly killed by the fact-checker
(`claims.json.killed`: "Alaska has 8 data centers, fourth fewest, against
Virginia's 639 ... No underlying source reachable ... Killed entirely").
`claims.json` carries a machine-readable `killed` array and nothing
checks slide text against it. `copy_sync_check.py` verifies the reverse
direction (authored strings present in the render) and cannot see this.

NOT FIXED THIS RUN, deliberately. The `killed` entries are prose
(`scout_claim` + `why_killed`), and the two offending strings share no
n-gram with the killed claim they descend from ("Alaska's working AI
load" vs "Alaska has 8 data centers"), so no text-matching gate built on
today's schema would have caught them; it would only have produced noise.
The bounded fix is a SCHEMA change first (see RECOMMENDATIONS).

---

## D4. Ordering, budgets and a second consecutive network dead end.

- **Scouts launched before the Phase 1 craft refresh.** The spec orders
  Phase 1 (craft refresh) before Phase 2 (research sweep). plan.md
  records the inversion as deliberate (parallelism), and the refresh did
  land in FIELD_NOTES before the directors' room consumed it. Cost this
  run: none observable. Worth leaving alone until it costs something.
- **Two scouts exhausted a 200-call WebSearch budget mid-beat.** Beats
  degraded gracefully; no claim rests on a truncated beat.
- **Reddit was 100 percent unreachable to Beat F** (every domain, every
  proxy; WebSearch refuses the domain). Beat F ran on newsletters and
  Hacker News. This is the SECOND consecutive run to hit it, so it is
  now a standing environment fact rather than an incident. No code fix
  is available from inside this repo (it is proxy/robots policy); the
  honest response is doctrine, and the spec already permits Beat F to
  source elsewhere. Recorded so the third occurrence is not re-discovered
  from scratch.
- **Playwright/browser drift (new, environment).** The installed
  Playwright expects `chromium_headless_shell-1228` (Playwright >= 1.57
  switched the default `chromium` channel to Chrome for Testing /
  chrome-headless-shell), which is NOT present; `/opt/pw-browsers` has
  `chromium-1194`. Every render this run therefore ran through
  `render.py`'s `launch_chromium()` fallback, on Chromium 141.0.7390.37.
  The fallback did its job silently and pixels are stable, but the
  browser build is not recorded in `render_report.json`, so a future
  pixel shift caused by a browser swap would be undiagnosable from the
  artifacts. See RECOMMENDATIONS.

---

## D5. Two scoring cycles spent, and the deck was never re-priced.

Cycle 1: 6.9 vs threshold 8.3, one hard fail (S06). Cycle 2: confirmed
the S06 repair, found a NEW hard fail (S02) created by the cycle 1
repair. Both are now fixed and verified by hand, but the score of record
is 6.9 because `Max 2 scoring cycles` was reached. The spec has no
provision for "the only thing between here and a real score is one
verified repair."

NOT FIXED THIS RUN. Raising or bypassing the cap is loosening a control,
which Phase 12 may not do. The maintainer's call, framed in
RECOMMENDATIONS.

---

# UPGRADES SHIPPED (2, both reactive)

## UPGRADE 1 (fix, engine) — TEXT UNDER AN OPAQUE PLATE is now a FAIL.

`render.py` gained an occlusion probe in its in-page QA pass: it collects
every element with a provably OPAQUE box (background alpha >= 0.9, or a
background image, or an `<img>`; opacity >= 0.9; no blend mode; not
full-bleed), intersects those boxes with each recorded text node's LINE
BOXES (skipping ancestors and descendants, so a label's own knockout
plate is never its own occluder), and confirms PAINT ORDER with
`document.elementsFromPoint` — the full stack, topmost first, so a
full-frame `.grain`/`.edge` overlay cannot decide the answer, which
singular `elementFromPoint` let it do (that bug made the first draft of
this probe report zero everywhere, including on the reconstructions). A
temporary `*{pointer-events:auto !important}` sheet makes the hit test
see decorative layers; it is removed before the screenshot and does not
touch a pixel (verified: all 9 re-rendered PNGs are byte-identical to the
shipped ones).

`qa.py` consumes `text_nodes[].occluded` and FAILs a non-decorative node
when a foreign opaque plate covers >= 20 x 6 px of a line box, WARNs at
>= 12 x 4 px, and demotes the FAIL to a WARN under `data-overlap-ok`.
Deliberately conservative: canvas/SVG/GL ink, blended layers, sub-0.9
alpha and full-bleed ground planes are NOT treated as occluders, so the
gate only speaks when something opaque provably covers type.

Known boundary, stated honestly: if the TEXT paints above the plate the
glyphs are visible and the gate stays silent by design. That case is
text-on-text and belongs to `text_collisions()`.

## UPGRADE 2 (fix, assets) — `AKPOST.grade` validates its arguments.

Wrong shapes now THROW a named `TypeError` (page error -> `render.py`
hard fail) instead of being coerced into NaN; unknown keys are reported
via `console.error` (a `qa.py` WARN) instead of being silently ignored;
and a 3-lookup NaN sentinel on the built tone LUT throws before the grade
can write a blank frame, which catches any future NaN path, not just this
one.

---

# RECOMMENDATIONS FOR THE MAINTAINER (not implemented; outside Phase 12's
# authority or unboundable this run)

1. **A confirmation re-score that is not a revision cycle.** The 2-cycle
   cap is correct and must not be raised. What is missing is a distinct,
   cheaper move: when a post-cap repair is VERIFIED by the gates and
   changes nothing but the defect, allow ONE re-price with no new
   revision permitted (score-only, no fixes accepted). Today an honest
   6.9 is published for a deck whose two hard fails are repaired.
2. **Make killed claims machine-checkable at the source.** Have the
   fact-checker emit, per killed claim, a `banned_strings` array (the
   exact phrasings the deck may not use, e.g. "Alaska's working data
   center", "only data center in Alaska") alongside `why_killed`. A
   10-line `killed_claims_check.py` then becomes exact instead of fuzzy,
   and no-ops on old claims files. Schema change first, gate second.
3. **Record the browser build in `render_report.json`** (`browser.version`
   from the launched instance) so a pixel shift from a Playwright /
   Chrome-for-Testing swap is diagnosable from the artifacts rather than
   guessed at. Two lines; deliberately not spent as a third upgrade slot
   this run to keep the revert set small.
4. **A post-repair acceptance re-check.** Every positional fix in the
   pixel round should re-run the touched slide's OWN acceptance checks
   from its dossier (S04 lost its terminus to a plate move and only the
   flow critic noticed). This is a prompt/agent change with real design
   surface, not a one-run edit.
