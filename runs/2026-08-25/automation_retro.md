# AUTOMATION RETRO, run No.40, 2026-08-25

Deck shipped at 8.66 against a threshold of 7.7, over four revision rounds, zero
hard fails, nine slides, every machine gate green at the ship gate, PR #318 with
all six checks green at 05ac661.

This retro walks `out/2026-08-25/run_state.json` phase by phase against
`prompts/routine_instructions.md`, lists every deviation with its evidence, and
names which ones became machine changes today.

## PHASE WALK

| phase | spec | what happened | deviation |
|---|---|---|---|
| wake | run date is the first date with no `runs/<date>/` | 2026-08-25 was free; latest shipped on disk was 2026-08-21 (`date_note`) | none |
| craft_refresh | read the knowledge base before building | done, FIELD_NOTES deliberately unchanged; it ran BEFORE the scouts by ordering luck, not by rule | **D1** |
| research | six scouts in parallel | six beats merged; four of them reported hitting the WebSearch ceiling mid-sweep | **D1**, **D2** |
| claims | claims_check PASS | PASS 36/36 usable, 3 primary, 36 with outlet | none |
| docket 3.5 | maintain `ledger/docket.json` | 18 live items at a raised budget (12 had been deferred, 4 rotten after no run since 08-21), 8 refreshed, 1 new item, 2 new AIDEA meetings; ran with ZERO searches available | **D2**, **D3** |
| site 3.6 | read-only sign-off, presentation fixes only | PASS 83 pages, 18 checks; gas watch PASS, 21 days on record; one reader-facing repair made (the docket call to action) | **D4** |
| selection | dedupe_check | clean | none |
| directors_room | dossier_check PASS | PASS 9 dossiers, 0 fails, 0 warns | none |
| copy | caption_check with the ledger | PASS, winner A, two demerits recorded for the ledger | none |
| art_build | qa.py exit 0 before Phase 8 | 0 fails, but five defects were built and cleared inside the phase, and no slide declared a single `__akAssert` | **D6**, **D7** |
| pixel_review | loop until every slide ships | rounds 1 and 2 recorded in `fix_rounds`; three motifs found DRAWN AND INVISIBLE, one count found short by a whole row | **D5**, **D7** |
| flow_review | max 2 rounds | caught the thumbnail that inverted the argument on slide 07 | **D8** |
| assemble | vector PDF | re-run after fix round 1; shipped | none |
| scoring | a low score is a work order | 8.66 over 7.7 in four rounds, weakest criterion artwork craft at 7 | none |
| ship | merge before the email | PR #318, six checks green, merged | none |

## DEVIATIONS, WITH EVIDENCE

**D1. The WebSearch budget is a real, undocumented ceiling, and this is the
fifth run it has bitten.** The session's 200 calls were fully consumed by the six
parallel scouts; beats B, D, E and F each reported hitting it partway through
their own sweep. Nothing in the routine mentioned the budget, nothing measured
it, and the scouts were spawned with no per-agent cap. The cost to the deck was
nil, because WebFetch was unaffected and the docket's primary URLs were already
on file. The cost to the MACHINE is on the record and is not nil: the Phase 12
`scan_log` shows zero searches available on 2026-08-14, 2026-08-16, 2026-08-19
and 2026-08-21, four runs in which this studio could not look at the frontier at
all, and one of those entries already wrote the conclusion down ("if Phase 12
needs the frontier, the budget has to be reserved in Phase 2"). This run also
ran Phase 1 before Phase 2 by luck of ordering rather than by rule. FIXED TODAY,
as prompt and data, not as machinery.

**D2. The 403 tax is now standing.** Refused automated fetch this run:
`alaskabeacon.com`, `newsminer.com`, `rca.alaska.gov`, `sam.gov`, `gvea.com`,
`miningnewsnorth.com`, `muni.org`, `anchorage.legistar.com`. Two scouts
independently rediscovered that Alaska Public Media republishes the Beacon,
which is the same discovery paid for twice in one day. `muni.org` and
`anchorage.legistar.com` cost the deck the Anchorage ordinance's own text and
its AO number, which shipped as an explicit caveat in the deck, the caption and
the sources comment. That is the honest outcome and a permanent hole for any
future Anchorage municipal story. FIXED TODAY as a dated record in
`config/sources.yaml`.

**D3. The docket worklist had rotted and the budget default hid it.**
`docket_staleness.py --budget 6` nominated 6 and deferred 12, with 4 past twice
their limit, because no run had fired since 2026-08-21. The run raised the
budget to 20 and worked the whole list, which is what the routine already says
to do, and the script announced its deferrals, which is what made it visible. The
gap is that nothing scales the default to days-since-last-run. NOT FIXED TODAY:
the machinery worked and the operator instruction worked; an automatic scaling
rule is a change to a cadence assumption and belongs to the maintainer.

**D4. A reader-facing string was generated from a constant that was true only
until it was not.** The docket's gold button read `COMMENT NOW, CLOSES SEP 1` on
an item whose open room is a public hearing where a person speaks. The verb and
the date word were constants written out in full in two files. FIXED IN-RUN and
already logged; carried here because the class matters and the ask box produced
three more of the same class the same day (a frozen ghost-numeral list, a
card-count check that measured a display cap, a hardcoded `/20 decisions/`).

**D5. DOM PAINTS OVER CANVAS, three times, and every gate was green.** Cell 0016
was drawn correctly and then covered by the `.lane` plate on slide 07, covered by
the `.guard` plate on slide 03, and painted out by the channel's own void fill on
slide 06. Each time the code was right and the picture was empty, and TWICE a
repair note recorded the element as visible when nothing was on the slide at all.
`qa.py` had a text-under-an-opaque-plate check and a label-crossed-by-art check,
and both look at TEXT. FIXED TODAY.

**D6. A hook that is a count was never counted.** The cover printed 750 and drew
24 rows of 30, because row 0's centre sat past the bottom edge. A pixel critic
counted the rows by hand. FIXED TODAY.

**D7. The assertion contract went unused on a deck whose hook is a number.** All
nine slides declared zero `__akAssert` entries, verified by re-rendering them:
`asserts: []` on every slide. The 2026-08-12 contract can't catch what nobody
declares. NOT FIXED TODAY, because the honest repair is either a prompt that says
"a printed measurement declares itself" (already written, twice) or a gate that
requires a declaration whenever copy contains a numeral, which would false-fail
on dates, claim-ids and slide numbers. It is named here so the next build knows.

**D8. The thumb inverted the argument while the full size was correct.** Slide
07's retention lanes mixed tone on the absolute day, so the current-practice lane
was fully grey by day 10 and vanished at 432px, leaving a thumbnail in which
practice ends at day 5 against the proposed rule's 14. A reader would have
concluded the ordinance TRIPLES retention, which is the inverse of the slide's
headline and of the deck. The flow critic caught it; no gate did. NOT FIXED
TODAY, deliberately: the general form is "does the artwork's argument survive
the 432px thumb", and the honest instrument is a semantic read of a downsampled
image, which is a reviewer's job and not a threshold. `data-encodes` already
measures declared regions at feed scale and would have caught it IF the lanes had
been declared as a `differ` pair, so the cheap move is authoring, not code.

**D9. The claims index and the copy agreed only because one agent wrote both.**
The storyboard listed C17 on slide 04 where nothing prints it, and listed C34 on
slide 08 only, when slide 06 prints it too. The copywriter noticed while
assembling `claim_ids`. `plan_drift_check` passes now, but it compares the index
against `copy.json`'s `claim_ids`, which were written BY the agent that spotted
the drift; had the copywriter copied the index, both artifacts would have agreed
and both would have been wrong. NOT FIXED TODAY: closing it means deriving
`claim_ids` from the RENDERED text (does this slide actually print C17's
subject), which is a semantic match, not a string match, and needs a design
before it needs code. Recorded as the strongest open candidate for the next
Phase 12.

## WHAT BECAME MACHINERY TODAY

Three upgrades, all reactive, all logged in `ledger/upgrades.json` with a
rollback. Reactive-first as the method requires: the frontier scan produced a
NEGATIVE result that shaped upgrade 1 rather than competing with it.

1. **Declared artwork has to reach the slide** (D5). `window.__akMotifs`,
   an `elementsFromPoint` census plus a canvas-vs-composite ink comparison,
   verified by `tests/motif_survives_verify.py` and by a reconstruction on this
   run's own slide 07.
2. **A hook that is a count is counted in the frame** (D6). `points` on
   `__akAssert`, verified by `tests/count_assert_verify.py`.
3. **The research phase's two standing taxes are written where the scouts read
   them** (D1, D2). A 25-call per-scout cap and Phase 1 pinned ahead of Phase 2
   in the routine; a dated `refuses_automated_fetch` block in
   `config/sources.yaml`. Prompt and data, not machinery, and logged as such.

## WHAT WAS PARKED

- **The draw-time snapshot**, which is what would close the third shape of D5 (a
  motif painted out and then covered by a non-flat wash). Measured: slide 06's
  rect reads 62.9 dE with and without the motif, so today's gate passes it either
  way. Parked with its unblocking condition in `knowledge/FIELD_NOTES.md`.
- **The frontier scan itself, focus (e)**, produced no capability to adopt: no
  browser API answers "did this canvas-drawn feature survive compositing".
  Written up with sources in FIELD_NOTES and in the `scan_log`.

## RECOMMENDED TO THE MAINTAINER, NOT DONE HERE

- Scale `docket_staleness.py --budget` to days-since-last-run (D3). It is a
  cadence assumption, and cadence assumptions are yours.
- D9 is the next real gate and it needs a design first.
