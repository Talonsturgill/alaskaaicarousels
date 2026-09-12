# SHOWRUNNER INCIDENT NOTES — 2026-09-12 (No.57)

Running list for Phase 12. Written as they are found, not reconstructed at the end.

## 1. The master prompt still orders a string the owner deleted

`prompts/routine_instructions.md:728` (Phase 5 step 4) requires the close slide to
carry `"sources in comments"`. CAROUSEL_CRAFT was changed by the owner on
2026-09-11 to say the opposite, twice, in plain terms: "Do NOT print 'sources in
comments' on any slide: removed by the owner on 2026-09-11" and "NO SOURCE NOTE."
Nothing in `scripts/` or the engine enforces either the old requirement or the new
ban, so the only thing standing between the deck and a rule violation is whether
the showrunner happened to read the doctrine file after the master prompt.

Severity is real. A run that follows its own master prompt to the letter ships a
string the owner removed, on the close slide, in artwork that cannot be edited
after the post. This run read CAROUSEL_CRAFT and will not print it.

Fix, Phase 12, reactive. Strike the phrase from the master prompt's step 4, and
add the ban to a gate so it does not depend on reading order.

## 2. The watermark on every slide is an owner rule with nothing watching it

CAROUSEL_CRAFT, same 2026-09-11 change, makes `alaskaaihq.com` a fixture on EVERY
slide rather than only the close, with the owner's reason given, that a reader who
stops on slide 04 should still see where the deck came from. A grep of
`scripts/dossier_check.py`, `scripts/caption_check.py` and the engine's `qa.py`
for `alaskaaihq.com` returns nothing. So the newest fixture rule in the house is
enforced entirely by care, on nine slides, every day.

Fix, Phase 12, reactive, and cheap. One check over `render_report.json`'s text
nodes per slide. It is a tighten and not a loosen, so it is inside the hard rules.

## 3. Phase 3.6 found one thing it is forbidden to repair

`ledger/gaswatch.jsonl` has no record dated 2026-09-08, immediately after a seven
run collector outage repaired by PR #347. Cron-written, off limits under
non-negotiable 19, so it is reported in the draft and nothing was touched. Written
up in full in `out/2026-09-12/site_signoff.md`.

## 4. A scout returned a docket "correction" that was not one

The Beat A scout reported that this repo's docket "mislabeled AO 2026-108 as a
data center ordinance." It does not. `ledger/docket.json` calls that item
"Anchorage's surveillance rules for its police crime center" and always has. The
scout was reading the showrunner's own brief, which listed AO 2026-108 among live
dates to verify in a brief that also discussed data centers, and inferred a claim
the docket never made. No docket change was made on the strength of it.

The process note worth keeping. A scout is an adversarial researcher pointed at
the world, and this one pointed a correction at our own record from a paraphrase
of a brief rather than from the record itself. Briefs that name docket items
should quote the item's own title, so a scout has the actual string to check
against.

## 5. A SLIDE WHOSE RENDER THREW PRODUCES A qa.py PASS. Found by reconstruction.

Found while verifying `assets/js/akfit.js`, by rendering a deliberate reconstruction
of No.56's defect. The reconstruction worked exactly as intended, render.py hard
failed the slide and printed the diagnostic. Then `qa.py` on the same render
directory printed this:

    [FAIL] slide-01.html  fails=1 warns=0
        FAIL: png missing
    verdict: PASS  (report -> .../machine_qa.json)

and exited 0. `machine_qa.json` reads `{"fails": 0, "warns": 0, "verdict": "PASS"}`.

THE CAUSE, and it is three lines. `.claude/skills/carousel-engine/qa.py` around
line 2628 handles a missing PNG like this:

    if not png.exists():
        res["fails"].append("png missing")
        out["slides"].append(res)
        continue

The `continue` jumps the whole per-slide body, including the rollup at the bottom
of the loop where `out["fails"] += len(res["fails"])` actually happens. So the FAIL
is written into the slide row, printed to the terminal, and never counted. The
totals stay zero, the verdict is computed from the totals, and `sys.exit(1 if
out["fails"] else 0)` returns 0.

WHY IT MATTERS BEYOND THE TERMINAL. The printed row is the only place this failure
survives, and nothing downstream reads the terminal. `machine_qa.json` is what
`gate_status.py` parses, what the scorer is handed, and what the run record
reports, and all three would be told the deck passed with zero fails while one
slide has no image at all. This is precisely the class the routine names in Phase
11 step 2b, that a check which can't see is not a pass.

WHY THE RUN IS NOT CURRENTLY EXPOSED. render.py hard fails first and exits
non-zero on any render error, so the normal pipeline stops before qa.py is
believed. The exposure is a re-render of a subset with `--only`, or any run of
qa.py against a render directory it did not just produce.

FIX, Phase 12, reactive, and it is a tighten. Roll the totals before the
`continue`, or restructure so the rollup cannot be skipped. The reconstruction is
already on disk at `out/2026-09-12/fittest/bad/` and is the verification: after the
fix, qa.py on `bad_render` must report fails=1 and exit 1.

## 6. akfit.js, the standing-weakness attack, is built and verified

`assets/js/akfit.js` is new this run and is the named attack on Legibility and
platform fitness. It is the measure-then-draw bench: a container is built from the
measured ink box of the text it holds, a cluster is clamped inside the safe zone by
measurement, and `AKFIT.guard()` refuses at renderReady to let a container ship
narrower than its contents.

VERIFIED BOTH WAYS before any slide used it, which is the Phase 12 bar.
- GOOD case, `out/2026-09-12/fittest/good/`. A wrapped mono label inside a fitted
  dashed container, a fitted headline, a body block. render.py reports
  warnings=0 errors=0, qa.py reports fails=0 warns=0 and PASS.
- BAD case, `out/2026-09-12/fittest/bad/`. The identical slide with No.56's defect
  reconstructed, the string lengthened AFTER the container was measured, which is
  exactly how a repair round introduced it. render.py HARD FAILS with
  `AK CONTRACT: AKFIT.guard: 1 fit breach. a fitted container no longer holds its
  text. 'LARGE COMMERCIAL AND INDUSTRIAL AND INSTITUTIO' spills bottom by 92.5px`.

The 92.5px number is the point. That defect shipped past two pixel critics and
into a scoring pass on No.56 and cost the criterion a 4.

## 7. `AKENGRAVE.drawOffscreen` RETURNS A 1x SURFACE AND NOTHING SAID SO (2026-09-12)

Slide 02 built its interference field with `getImageData(0, 0, W*2, H*2)` and read
the pattern at `px/2`, on the reasonable assumption that an offscreen matches the
slide canvas, which is 2160 by 2700 under `ctx.scale(2,2)`. It does not:
`drawOffscreen` is `c.width = w` and nothing else.

The visible symptom was mild, a field drawn at twice its intended scale, which
looked like a design choice. The real one was not. Every pixel asked
`atten(px/2, py/2)` whether it was allowed to paint, so the basin reserve was
consulted for a point half way to the origin, and the field walked straight
through the headline's second line. `qa.py` caught it and named the exact line
box and the exact 88 px^2. Three rounds of fixes aimed at the arcs, the basin pad
and the field threshold all missed, because the arithmetic was wrong rather than
the gating, and a reserve that is consulted at the wrong coordinates fails
silently in both directions: it also suppressed ink where there was no type.

FIXED IN PLACE for this run by using design px throughout, and the finding is
written into `drawOffscreen`'s own docstring.

FOR PHASE 12. A docstring is the weakest instrument available here. Two stronger
ones: have `drawOffscreen` stamp the surface it returns with `__akScale = 1`, and
have the render-time hook flag a `getImageData` whose requested width exceeds the
source canvas's width, which is free and catches this exact class before it
renders. The second is the one worth building, because it fires on the mistake
rather than on the reader.
