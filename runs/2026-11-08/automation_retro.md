# Automation retro, 2026-11-08 (No.109)

## The weekly pass ran today, inside this run

`machine_due.py` was due at wake (seven days since the last pass), so the upgrade engineer
ran the weekly pass and shipped one commit, `5d22240f upgrade(2026-11-08)`. It made five
bounded changes: an opt-in akthree soft-shadow radius, AKPOST grain at size 1 by default,
caption_check never waiting on stdin, run_guard printing the Anchorage date, and a
fetch_pdf_text diagnosis for a host-chain TLS failure plus sources routes. The SHA is
recorded in ledger/upgrades.json in its own follow-up commit. After that commit,
`machine_due.py --date 2026-11-08` exits 1 (last pass 0 days ago), so no second pass runs today.

## Trend check, top repeat offender

`trend_check.py --window 10`: Artwork craft and genuine detail was weakest in 5 of 10 runs
(mean 7.1), marked STALE because it was last worked on 2026-10-04 by text match. That is an
under-report. Today's weekly pass aimed two of its five changes at it (soft GPU casts, white
grain), both named for the Artwork criterion in their trigger lines. **Worked on today, in the
weekly pass.** Thumb-stop cover (2 of 10) is next, and it's deferred to the next weekly pass.
The digest has no recurring cover defect, and any fix written today would be a guess rather
than a measured repair.

## Deviations, phase by phase

- **Wake.** I called run_guard with `--date`; its flag is `--run-date`, and the second call
  worked. The weekly pass's run_guard change prints the Anchorage date, which was the
  confusing part (woke 06:07Z on November 9th for an Anchorage run date of November 8th).
- **Research.** `fetch_pdf_text.py` failed TLS on alaska.edu with SSL_CERT_FILE set, and
  alaska.edu then answered 503 all day. The diagnosis message is fixed in the weekly pass.
  The underlying gap is real and stays real: the regents' November 5th vote outcome could not be
  confirmed from a primary source, so the deck is written around the documented dispute
  and not around the result. That goes in the draft as an editor note.
- **Phase 3.6.** The Gas Watch daily post was late. I dispatched gaswatch.yml on main, and
  the re-audit passed (gas_watch_live PASS at 2026-11-09T06:20Z). Cron health PASS, 7 workflows.
- **Phase 5.** On its first pass, dossier_check failed thin 4a fields and coordinates without
  `[design]` markers. It warned on cast promises for 03 and 07. All of these were fixed in the
  dossiers before the build. The gate worked as intended.
- **Phase 7 to 8, the art.** A new shared module, `assets/js/aklaid.js` (laid-paper field read
  in reflected and transmitted light), took three review rounds:
  - **Round 1** (mean 6.3): the critics named corduroy laid lines, flat sheets and a weak
    watermark. That's the week's recurring texture-artifact theme again, fixed at the root in
    the module: warped, jittered, floc-modulated laid phase, key ramp, rims, floc tone.
  - **Round 2** (flow critic revise, art about 6.5): local regressions on 02 and 08.
  - **Round 3:** the flow critic's work order. Density cuts on 04 and 05, brighter
    transmission on 01 and 03, a fibre term in the module.
- **Gates during rounds.**
  - qa.py caught a stale contact declaration after slide 02's re-layout. I re-probed every
    contact and wrote them to contacts.json.
  - plan_drift caught four claims (C07, C15, C17, C21) that the round-3 cuts removed from the
    slides while the storyboard index still assigned them. I reconciled the storyboard, not
    the slides.
  - aggregate_check counted "all three" as a subset early on; the KTOO entry was reworded.
    It was later cut anyway.
- **My error.** I redirected caption_check's stdout onto caption_report.json, which the
  script already writes itself. The JSON was corrupted, and a clean re-run fixed it. I've
  queued an atomic write so a stray redirect can't do it again.

## Queued (the pass is weekly)

One new item in knowledge/MACHINE_QUEUE.md: caption_check should write its report through a
temp file and os.replace. That makes 57 items queued. The next weekly pass is due 2026-11-15,
or sooner if an item reaches repeat 2.

## Score

The round 3 score was 8.30 with art at 7.0, so the run owed one craft cycle on frames 9, 7, 6, 4 and 1. After the cycle (round 4) the score is 8.45 against a threshold of 7.7, and art rose from 7.0 to 7.5. That's still under the 8.5 floor, and the email says so. What's left is the shared aklaid streak texture (03, 01, 08), 09's flat close, 06's soft focal sheet, and 07's overlap watermarks. This is the evidence for the next weekly pass on Artwork craft: the paper texture is the largest object on seven frames, and it was the last thing that would not clear.
