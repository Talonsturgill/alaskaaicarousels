# INCIDENT NOTES — run 2026-08-25, carousel No. 40

Written by the showrunner as it happened, for Phase 12. These are deviations
between what this run DID and what `prompts/routine_instructions.md` says should
happen, plus environment breakage, plus defects a later gate or a human caught.

## 1. THE WEBSEARCH BUDGET IS A REAL, UNDOCUMENTED CEILING

The session's WebSearch budget, 200 calls, was **fully consumed by the six
parallel Phase 2 scouts**. Beats B, D, E and F each reported hitting it partway
through their own sweep, so the last-finishing scouts did the tail of their work
on direct page fetches only. Every later phase in the run had zero searches
available: the Phase 3.5 docket refresh, which normally opens with a search per
item, had to be driven entirely off URLs already in `ledger/docket.json`.

Nothing in the routine mentions this budget, nothing measures it, and the six
scouts are spawned with no per-agent cap. The failure is silent from the
showrunner's side, because a scout that runs out simply returns thinner findings
and says so in `dead_ends` if it happens to notice.

WHAT IT COST THIS RUN: not much, because the docket's primary URLs were already
on file and WebFetch was unaffected. WHAT IT COULD COST: a run whose Phase 3.5
needs to find a NEW notice, or whose Phase 1 craft refresh runs after the scouts
rather than before. This run did Phase 1 first by luck of ordering, not by rule.

Candidate fixes for the engineer to weigh, not prescriptions: a stated per-scout
search budget in the beat brief, a documented note in the routine that Phase 1
must precede Phase 2, or a cheap `scripts/` helper that records the count so a
run can see it coming.

## 2. A DOCKET CALL TO ACTION WAS WRONG FOR A NON-COMMENT-WINDOW ITEM, AND IT
   WAS HARDCODED TWICE

FIXED IN-RUN, and this is the one defect a reader would have seen.

The docket's gold button rendered `COMMENT NOW · CLOSES SEP 1` on the new
Anchorage crime-center ordinance item. That item's open room is a PUBLIC HEARING
where a person speaks, not a written comment window, and no source supports
telling a reader to file something in writing by that date. The verb was the
constant `"COMMENT NOW"` and the date word the constant `"CLOSES"`, written out
in full in TWO places, `scripts/docket_build.py` and again in
`scripts/site_build.py`, which is how one wrong string became wrong in two files
at once.

REPAIR: the verb and the date word are now data on the item, from closed sets
(`CTA_LABELS`, `CTA_WHENS`) validated at build time, and both surfaces render
through a single `docket_build.cta_html`. `docket_dates_check.py`'s `CTA_RE` was
widened to read the date behind either verb, so the gate lost no strength and
still asserts that the button shows this item's own action deadline and no
other. Verified: the two real comment windows still render `COMMENT NOW, CLOSES
AUG 28` and `CLOSES SEP 14` unchanged, the new item renders `TESTIFY, ON SEP 1`,
and `docket_dates_check` passes 291 assertions over 6 fixtures and 22 items.

FOR THE ENGINEER: the general shape is worth a look. This was reader-facing copy
generated from a constant, and the schema had no way to say what the reader is
actually being asked to do. There may be other constants in the site builder
that are true for every item so far and will be wrong for the next one.

## 3. THE DOCKET WORKLIST HAD ROTTED, AND THE BUDGET DEFAULT HID IT

`docket_staleness.py --budget 6` nominated 6 items and DEFERRED 12, with 4 marked
ROTTEN (past twice their limit while still live). Every one of the 18 live items
was over its limit, because no run had fired since 2026-08-21.

The routine already says to raise `--budget` rather than let the tail rot, and
this run raised it to 20 and worked the full list. Worth recording that the
default of 6 is calibrated for a DAILY cadence and silently under-serves any gap.
The script does announce its deferrals, which is what made this visible, so the
machinery worked. The gap is that nothing scales the budget to days-since-last-run.

## 4. RECURRING 403s FROM ALASKA SOURCES, NOW A STANDING TAX

Refused automated fetch this run: `alaskabeacon.com`, `newsminer.com`,
`rca.alaska.gov`, `sam.gov`, `gvea.com`, `miningnewsnorth.com`, `muni.org`,
`anchorage.legistar.com`. The Beacon is routinely recoverable through Alaska
Public Media's republication, which two scouts found independently, and that is
worth writing down somewhere a scout will read it.

`muni.org` and `anchorage.legistar.com` mattered directly: the Anchorage
ordinance's own text and its AO number were never obtainable, so the deck, the
caption and the sources comment all carry an explicit caveat instead. That is the
honest outcome and it is also a permanent hole for any future Anchorage municipal
story.

## 5. DEFECTS THE GATES CAUGHT THAT THE BUILD SHOULD NOT HAVE SHIPPED

All fixed before the critics saw them, listed because the pattern matters.

- `AK.grainTile` returns a data URL for a CSS background, not a canvas. The first
  build passed it to `createPattern` and the slide hard-failed. The SKILL.md
  entry and the instinct both say "small repeating tile" without saying it is a
  URL, so the mistake is available to any future run.
- `AK.fitText` clamped at `min` and set 7 lines against `maxLines: 3` on the
  cover, exactly the documented failure. Caught by qa.py, fixed by widening the
  box and lowering `min`.
- The first contact-shadow declaration on the cover measured dL 0.8 against the
  4.0 floor, because the shadow was cast on ground that was already near black.
  The remedy in SKILL.md, light the ground FIRST then cast into it, worked and
  took the same declaration to dL 38.3.
- `bespoke_check` FAILED the first complete deck on drawn share, 29 percent
  against the 45 percent floor, at a median similarity of 0.124. The deck was
  genuinely bespoke and genuinely rectangle-heavy, which is exactly the split the
  gate was built to separate. The repair, converting pad lids and milled channel
  lips to paths with `arcTo` chamfers and `fbm2`-walked edges, raised it to 65
  percent AND improved the art, because a machined boss does not have square
  corners and a milled lip is not a straight line.

## 6. THE COPYWRITER CAUGHT A CLAIMS-INDEX DRIFT NO GATE WOULD HAVE

The storyboard's claims index listed C17 on slide 04, where nothing prints or
draws it, and listed C34 on slide 08 only when slide 06 prints it too. The
copywriter noticed while assembling `claim_ids` and said so in its notes. Fixed
in the storyboard.

`plan_drift_check` passes now, but it only compares the index against
copy.json's `claim_ids`, and copy.json's `claim_ids` were written BY the agent
that spotted the drift. Had the copywriter simply copied the index, both
artifacts would have agreed with each other and both would have been wrong. That
is a real blind spot in an otherwise good gate, and it is the kind of thing this
phase exists to close.
