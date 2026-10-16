# Automation retro, run 2026-10-15 (No.87)

## Weekly machine pass
Not due. `scripts/machine_due.py --date 2026-10-15` reported: last pass 2026-10-11, 4 days ago, due at 7; 16 items queued, 0 repeat offenders (exit 1). No `upgrade(2026-10-15)` commit exists.

## Standing repeat offender (trend_check --window 10)
Artwork craft and genuine detail was the weakest criterion 7 of 10 times, mean 6.88, last worked 2026-10-04 (STALE). It is queued for the weekly pass, which is the answer the phase allows on a day the pass doesn't run. What this run adds to that pass's evidence: the art moved from about 6.3 to 7.3 on the per-slide critics across four rounds once the chassis itself was fixed (board albedo through the double tone curve, leaf lattice, tooth as an albedo bump, cast-term blur), and the scorer read 7.0 before the craft cycle and 7.5 after it. The weekly pass should look at the board albedo and the leaf first, because both were shared causes that made every frame that used them read flat.

## Fixed in this run because it broke in this run
These are chassis repairs to this deck's own helpers and to an opt-in path in akbench; every existing akbench caller keeps its old output unless it passes the new options.
- `assets/js/akbench.js`: optional `keyMask`, `keyColor`, `ambColor` (window light), an exact early exit on the shadow march (render 18 s to about 12 s a frame), opt-in `dither` (half an 8-bit step, the leaf was contouring into rings), opt-in `visBlur` (a box blur of the shadow term alone, against the penumbra speckle a crinkled or scored top makes) and `visSharp` (materials whose own cast stays crisp).
- `assets/js/akmat.js` (new): this deck's world chassis. Museum board rendered olive and then mid-grey because the warm key and the two tone curves (akbench's v/(1+0.35v) and AKPOST's ACES) compress a lit near-white board to about L* 74; a cool-biased lift [1.50, 1.60, 1.74] brings it back. The tooth went into the albedo as a bump along the sun's direction, because a 0.3 px tooth in the height buffer only feeds the penumbra term and speckles the shade.
- `visSharp` exists because of a measurement: at visBlur 4 the ruler's groove shadows softened, the axis census threshold dropped with them, and board tooth on 08 and 10 then read as undeclared ruler marks (3 and 4 to 5 of them). Keeping the ruler's own cast crisp cleared both without touching the gate.

- `scripts/docket_build.py` (PR #436's red `mobile` check): the Enstar item opening for comment renumbered the docket, the badge relaxation settled with a Southcentral badge 52 units under its dot, and the iPhone 13 landscape home view framed Alaska at 52 percent (main 57, floor 55). A fit-aware pass after the relaxation now moves a displaced badge to another free tethered spot only when the landscape frame's vertical need shrinks and the horizontal need does not grow: 65 percent, 148 of 148 checks on the branch and on main's data. Two narrower tries (a mirrored flip, then relaxation orderings) moved nothing and were reverted.

## Codex on PR #436 (reviewed 413d74f)
- P1, the Enstar COMMENT NOW link pointed at a July ADN story: `cta_html()` uses `sources[0]`, so the DNR public notice now leads the item's sources. Fixed.
- P2, the comment window's Event startDate fell back to first_seen (July 11th): the milestone read "issues", which `window_open_date()`'s pattern doesn't match; it now reads "issued ..., opening public comment". Fixed.
- P2, "What we verified" published the docket and runner-up claims (C56 to C72): runs/2026-10-15/claims.json now carries the story's C01 to C55 and the full record rides beside it as claims_research.json. The site-wide fix (build the section from the claims a deck cites) stays the queued site_build item, because it rewrites every past deck page.
- P2, run_state's upgrade phase read pending: recorded as done with the not-due result. Fixed.

## Deviations, phase by phase
- Phase 0: run_guard defaults to the UTC date, which was already October 16th at wake; `--run-date 2026-10-15` (Anchorage) gave CLEAR.
- Phase 3.6, gas watch: FAIL at wake, 06:26Z, 07:40Z and 08:10Z on 'source reading published' only. CINGSA posted a revised October 15th reading at 16:39 Alaska, after the 22:26Z collection; the 04:40Z and 07:20Z slots had not run and workflow_dispatch returned 403 three times. An incident was filed, then withdrawn when the audit PASSED at 09:28Z after GitHub ran a late slot. Repeat 12 on the queue item (owner decision on schedules or Actions credentials).
- Phase 3.6: curl to the Federal Register needed `-g -L`; aws.state.ak.us refuses curl, read through WebFetch; the AOGCC page returned 403.
- Phase 6: the caption critic returned "neither" on both candidates; one reassigned director round produced the winner. The copywriter's hand-back was not persisted, so copy.json was written from it by hand and checked by copy_sync.
- Phase 7: the prototype's lit mat was too dark (flat Lambert at el 20 is 0.34); fitText miscounted lines with block spans until `authored: true`; an undeclared mark at x 1079 until the 100 MW mark was declared at 1080.
- Phase 8: the round 1 critics returned revise on all ten frames (6.3 to 7.3). Shared causes were fixed once in the chassis instead of ten times: olive board, tiled leaf, 4:1 ruler numerals, a dark AO line on lit sides.
- Phase 8: the showrunner's own edit by row prefix (`| 01 |`) rewrote three tables in storyboard.md, not one, because CONTINUITY SYSTEM and CRAFT PLAN use the same row prefixes. dossier_check caught it; the rows were restored from the transcript. Lesson in FIELD_NOTES: edit a table inside its own section's bounds.
- Phase 8: round 4's scattered vellum drop placed only 10 of 15 sheets at first (the sampler was too strict) and three sheets drawn without a title box read as missing marks to the count probe; every sheet keeps its box.
- Phase 8: contact_probe --verify printed "the DECLARED ground rect is 100 percent the object's own colour" on every declaration in every round, though each ground sat on lit mat with dL 7.6 to 9.6 (queued).
- Phase 10: scored 8.66 at round 4 against 7.7 with art 7.0, so the CRAFT FLOOR owed one cycle; it rebuilt slide 10's ending as one object and worked 01, 02, 05 and 08; re-scored 8.665 with art 7.5. The re-score also showed the caption close was answered inside the caption, so it now ends on the deck's own ask (two commas cut to stay in budget).

## Queued today
- gaswatch: evening collection slots land after the daily audit (repeat 12, owner decision).
- contact_probe --verify: the 'ground is the object's own colour' note fires on lit-mat grounds (new).
- akbench: a crinkled or scored top speckles the marched penumbra; fixed here with opt-in visBlur and visSharp, the weekly pass decides whether they become the default (new).

## Upgrades this run
None (weekly pass not due).
