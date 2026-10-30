# Automation retro, 2026-10-29, No.99

Weekly machine pass: NOT due (machine_due: last pass 2026-10-25, due at 7 days; 37 items queued, 0 repeat offenders before this run). Everything below that is not a mid-run fix is queued in knowledge/MACHINE_QUEUE.md for the next weekly pass.

## Top repeat offender (trend_check --window 10)

Artwork craft is the weakest criterion on 7 of the last 10 runs (mean 7.26), flagged STALE (last worked 2026-10-04). Today it scored 7.0 again, under the 8.5 craft floor, and the craft cycle stood down because the deck reached the five-round cap. Deferred to the weekly pass, which is the right place for it: this run's evidence for that pass is that most of round 1 went to two causes no gate saw before the critics did, a front-lit hero landform (01, 04) and a far terrain mesh z-fighting through the near one (01, 05). Both are now queued with a concrete fix (a key-versus-hero-normal check in dossier_check, a default far-mesh offset in AKBLUFF or an AKT terrain helper). What would have to be true to tackle the art theme directly: a planning-stage check that catches a flat key before the build, which is the first queued item.

## Deviation walk

- wake: run_guard defaulted to the UTC date (October 30th) on a 22:0x AKDT wake; passed --run-date 2026-10-29. Queued item raised to repeat 2 (the policy question is already escalated there).
- gas watch live: the first audit FAILED on the evening slot (published 2026-10-28 against CINGSA's 2026-10-29T16:00 reading). Dispatched gaswatch.yml on main (run 41012615703), Pages deployed, re-audit PASS. The evening-slot repeat was already queued earlier this run (repeat 16).
- research: FERC DownloadP8File answered 401/405, so the run used the keyless search census instead; a browser-UA fetch of alaskabeacon.com was refused by the harness as bot-check circumvention and was not retried.
- build: render.py has no positional `--only-exact N`; the form is `--only-exact --only N` (operator error, no machine change).
- copy: the copywriter caught two honesty issues the claims gate could not see (04's "a second error" reversed the rule's own numbering; 06 and 09 needed FWS attribution for C48 and C44). Fixed before the critics.
- pixel review: four per-slide rounds plus one flow round (the five-round cap). Round 1 failed all nine frames. Root causes: head-on moonlight on a north-facing lee (01, 04), far-mesh z-fight (01, 05), flat 2D strips standing in for pressure ridges (09), hard reserves under labels (02, 03, 08), a reserve edge across 06's plan. Round 2 introduced a defect of its own: a modular pixel hash used as sensor noise on 06 printed a 45-degree hatch; found in round 5, fixed in place at the cap and verified at 100 percent by the showrunner, not re-reviewed by a critic (disclosed in the email).
- plan drift: the claims index lagged the build twice (01 and 02 claim ids, then C12, then C13, C14, C24 after 04's body cut); plan_drift_check caught each one.
- flow critic: declined its "stale contact sheet" finding (assemble had run after the round 3 renders and the gate row read PASS); declined a pixel critic's request to start 08's rule line at the Colville, on the rule's own region text (Point Barrow to the western boundary of ANWR).
- scoring: 8.225 against the round-5 ladder threshold 7.7, below the base 8.3; art 7.0. One caption clarity fix applied after scoring ("The model says 22 denning bears."), caption_check re-run PASS.
- ship: the first site build failed because this run's topics row named beat slugs that don't exist (federal-policy, models-and-public-numbers, north-slope). Replaced with known slugs and rebuilt. Nothing tells the showrunner the slug list before the build; a one-line note is queued.

## Queued this run (knowledge/MACHINE_QUEUE.md)

1. akbluff/akthree far-mesh z-fight default (new).
2. dossier key-versus-hero-normal check (new).
3. run_guard UTC default (repeat raised to 2).
4. topics.json beats: print the known slug list in the ship step or validate the row before site_build (new, below).
