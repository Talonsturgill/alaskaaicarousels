# AUTOMATION RETRO, run No.66, 2026-09-23

Phase 12. Written after the merge, before the Gmail draft. Three upgrades made,
one frontier finding parked, three candidates declined with the measurement
written down so a later run does not re-attempt them.

---

## 1. REACTIVE RETRO, phase by phase against the spec

Evidence is `out/2026-09-23/run_state.json`, the run's own FIELD_NOTES entry,
the shipped artifacts, and measurements taken during this retro.

### wake, craft_refresh
Clean. `run_guard` CLEAR, bootstrap ran, plan.md carries the trend block.

DEVIATION FOUND HERE BY MEASUREMENT, not by the run. The trend block the plan
was built on was WRONG. `scripts/trend_check.py --window 10` printed four
repeat-offender rows, and one of them named a criterion called `{'name'` with a
dash for its mean and its last score. That row is not a criterion. It is
`runs/2026-09-14/score_report.json`'s `weakest_criterion`, which the scorer
wrote as an object where the schema declares a string:

    {"name": "Artwork craft and genuine detail", "score": 7,
     "one_sentence_fix": "Fill and shade slide 03's mail tote ..."}

trend_check took the container as a name, `str()`ed it and sliced it to 38
characters. Two consequences, and the second is the one that matters: the junk
row reads like data, and the run it came from had its REAL weakest criterion
tallied under that garbage key. Artwork craft, the house's standing weakness,
was being reported as weakest in 7 of the last 10 runs when the corpus says 8.
Phase 0 reads this report to pick the one weakness it attacks, so a criterion
that lands in a junk row is a criterion no run ever works on.

Two other readers of the same field were exposed to the same shape:
`scripts/ship_gate.py` prints it on the STOP path, and `scripts/gmail_draft.py`
renders it into the maintainer's email. Neither was reached on 2026-09-14
because that run passed, so this was luck rather than safety.

### research (Phase 2)
SIX SCOUTS, 142 searches, and NONE OF THEM COULD RUN THE PDF READER.

This is the run's largest deviation and the sweep found it itself. Four of six
scouts said in `dead_ends` that they could not execute
`scripts/fetch_pdf_text.py`, and the primary documents that went unread include
the DNR preliminary decision for ADL 234762, AIDEA's development plan and fact
sheet, the AI3 NOFO, and the 36 MB draft 2027-2030 STIP. The cause is exact and
embarrassing: `.claude/agents/scout.md` granted `WebSearch, WebFetch, Read`, and
none of those executes a script. The routine spec has named that script in every
scout brief since run No.62 built it. NAMING A SCRIPT IN A BRIEF IS NOT THE SAME
AS HANDING OVER THE TOOL THAT RUNS IT.

The showrunner ran the identical command by hand and it worked first time on
both Mat-Su documents, which is the only reason this deck had primary sources at
all. A claim that is never made can't fail the claims gate, so an unreadable
primary document is a silent hole in that gate rather than a visible one: this
run's `claims_check` passed 38 of 38 while four beats were reading secondary
coverage of documents they had already located.

### claims, docket
Clean. 38 claims, 34 primary, `claims_check` PASS. Docket refreshed, Mat-Su
decided, Anchorage held to October 20th, 7 items re-verified.

### gas_watch / cron (Phase 3.6)
FAIL on both audits with incident JSON written for both
(`gaswatch_incident.json`, `cron_incidents.json`), `site_signoff` WARN from the
same upstream cause. This is the documented external-blocker path working as
designed, not a machine deviation, and it is not Phase 12's to fix.

### directors_room, copy
The room caught a showrunner title defect and the deck was retitled. Good.

ONE DEVIATION, recorded and NOT taken this run. The caption room's own critic
recorded the deck-summary VERB-SLOT OPENER family as barred four times and then
let the candidate through as a burn-forward note. It was repaired at ship. A
burn list that only warns the NEXT room is not a burn list. This is a real
machinery gap in `caption_check.py`/the critic contract and it belongs in a slot
of its own; it did not get one because three reactive fixes outranked it.

### art_build, pixel_review
`qa.py` PASS, 0 fails and 0 warns across nine frames, which this studio has not
managed before on a deck built from one generative idiom.

DEVIATION: THE TERRAIN BAN WAS A MEMORY AND IT FAILED AS ONE. The rule that an
engraved surface must never read as landform was prototyped before the dossiers,
written into the dossiers, and stated in the plan. It STILL reached two finished
frames, and pixel critics caught it on the render rather than the machine
catching it at build. The cause is known exactly: a noise term inside an
AKENGRAVE `form` callback drives the direction field, so the burin walks the
noise iso-lines and the region prints as contour-mapped ground. Noise inside
`tone` is the deck's legitimate idiom and had to keep working.

DEVIATION, SECOND ORDER: `_layCheck`'s warning text sends the reader to the
wrong remedy. Round four spent two attempts on the prose remedies it suggests
(second-axis variation, trial `seedDeg`) before someone opened the function and
computed the answer. Not taken this run; see DECLINED below.

### flow_review, assemble, scoring, ship
Clean. Flow critic 8.2 ship. Vector PDF 5.64 MB, inside the house band for once.

---

## 2. FRONTIER SCAN

FOCUS (b), editorial dataviz and cartography technique. The stalest legal slot,
last read 2026-09-14, and distinct from the last three logged foci: 2026-09-21
(g) accessibility and PDF, 2026-09-20 (c) generative and procedural art,
2026-09-19 (e) headless Chromium. Relevant as well as stale: artwork craft is
the standing weakness in 8 of the last 10 runs, and this run's own third-ranked
candidate was a cartographic defect, five frames carrying a typed "20 KM" or
"50 KM" chip with no bar and nothing measuring it on maps built from a live
projection.

Five searches, four fetches, two of which 403'd (gijn.org and
danielroelfs.com both refuse this container; add them to the
`refuses_automated_fetch` record next time that file is touched).

FOUND, and PARKED as a knowledge/FIELD_NOTES.md candidate:

- **A shipped reference implementation for the scale bar this run had to
  improvise.** `HarryStevens/d3-geo-scale-bar` computes the bar from the
  projection itself rather than from a typed number, and it carries two
  parameters worth stealing outright: it picks the smallest of 1, 2, 4 or 5
  times a power of ten that renders the bar at least 80 px wide, and it converts
  through a stated Earth radius (6371.0088 km mean) so the number on the bar is
  a geodesic and not a screen measurement.
  https://github.com/HarryStevens/d3-geo-scale-bar
- **And the caveat that makes it a design decision rather than a utility.** On a
  projected map covering a range of latitudes, a scale bar is only correct along
  one line. Esri and the OS cartography guide both state it plainly, and it is
  the reason the bar has to be drawn WHERE it is measured rather than parked in
  a corner chip. https://www.esri.com/arcgis-blog/products/product/mapping/back-to-the-issue-of-scale-bars
  , https://docs.os.uk/more-than-maps/geographic-data-visualisation/guide-to-cartography/scale
- **One editorial technique noted and not parked, because it is doctrine we
  already hold:** the annotation layer carries the conclusion, not the data
  label ("this is where prices broke", not "June 2022"). Our DESIGN_DOCTRINE and
  the dossier spec already require exactly this of every callout, so there is
  nothing new to write down.

Parked rather than applied because all three upgrade slots went to reactive
fixes, and because an `AK.scaleBar()` helper plus the check that would enforce
it is a bounded but non-trivial piece of work that deserves a run of its own
rather than a fourth change riding on three others.

---

## 3. UPGRADES MADE (3 of 3)

### U1, fix, agents + scripts. The scout can read a PDF, and can do nothing else.
`.claude/agents/scout.md` now grants `Bash` AND attaches
`scripts/scout_bash_guard.py` as an agent-level `PreToolUse` hook on the `Bash`
matcher. The guard allows exactly one command shape,
`python3 scripts/fetch_pdf_text.py <url> [--pages|--max-chars|--max-mb|--timeout|--json|--self-test]`,
and denies everything else, including `--out`, which is the only flag that makes
that script write a file.

The option space was considered rather than the first option taken:

- Plain `Bash` on the scout was REJECTED. Six leaf workers run at once, `Bash`
  is allowed outright in `.claude/settings.json`, and an unrestricted shell lets
  a leaf worker write anywhere in the repo, drive git, or start another agent
  process, which is the uncapped fan-out non-negotiable 7 was written after.
- A showrunner-side pre-fetch was REJECTED on the acceptance test: the scout has
  to be able to turn a PDF URL into text without the showrunner in the loop.
- An MCP server exposing one read-only tool was REJECTED on a harder ground than
  taste. Introducing a server risks a trust or approval prompt, and in this
  routine a prompt is a stop and a stop is a failed run.
- A `permissions.deny` rule in `.claude/settings.json` was REJECTED because deny
  rules apply to the main conversation as well, so denying the showrunner's own
  Python to protect a scout is a cure worse than the disease.

Blast radius after the change: the scout has no `Task` tool, so it can't spawn
a subagent whatever the shell says; it has no `Write` or `Edit`; and the one
command it can run writes nothing. Verified below.

### U2, fix, scripts + agents. One reader for the scorer's weakest criterion.
`weakest_criterion_name()` lives in `scripts/trend_check.py` and is imported by
`scripts/ship_gate.py` and `scripts/gmail_draft.py`. It accepts the string the
schema declares, the `{"name": ...}` mapping 2026-09-14 wrote, and a list, and
it REPORTS any shape it does not understand through trend_check's existing
`[unreadable]` channel instead of stringifying a container into a criterion.
`.claude/agents/scorer.md` now states the shape inline in the JSON it returns.

It does NOT gate. `--require` was deliberately left alone: `runs/2026-09-14` is
a shipped artifact and this repo does not rewrite those, so gating on shape
would fail every future run over a file nobody is allowed to fix.

### U3, fix, assets. The engraver names a terrain form at build time.
`assets/js/akengrave.js` reads the `form` callback's own source in `surface()`
and, when it finds a direct `AK.fbm2/fbm3/simplex2/simplex3/warp2/grainTile`
call, console.errors under the `AK ENGRAVE:` prefix that `qa.py` records as a
WARN. The message names the region, says why the lay will read as terrain, and
gives the two real remedies.

WARN AND NOT A HARD FAIL, ON MEASUREMENT. A landform is the CORRECT read for
some decks in this studio's corpus; the ban is this deck's, not the house's.
CLAUDE.md records what a hard fail built on a misdiagnosis costs, and a gate
that blocks a correct future deck is the exact shape of that mistake. A deck
that really is drawing ground declares `landformIntended: true` on the surface
call, which also puts the intent in the slide source where the next reader sees
it. Noise in `tone` is untouched and is proven untouched below.

LIMIT, stated in the code: the check reads the callback's own text, so a form
that delegates to a helper which calls noise is invisible to it. It catches the
shape the defect actually takes.

---

## 4. DECLINED THIS RUN, with the measurement, so a later run does not re-open them blind

- **`_layCheck` should print the safe `seedDeg`.** NOT declined on merit; it is
  the strongest remaining candidate and it should be the first thing the next
  Phase 12 picks up. The arithmetic is already derived and recorded in this
  run's FIELD_NOTES entry: alignment is the mean |cos| between the seeding
  raster and the walk direction, the walk runs at `atan2(gx,-gy) + angOff`,
  `angOff` is 0 on the main channel and `crossDeg` on the cross channel, so one
  `eng.surface` call has TWO angles to avoid at 90 degrees off each and the safe
  `seedDeg` is the midpoint between the two perpendiculars. `_layCheck` already
  samples every `ang` it needs; minimising `mean |cos(ang - theta)|` over theta
  is a coarse scan in the same loop. Held back only because the budget is three
  and three reactive fixes outranked it.
- **A gate on the typed scale figure.** Parked with its frontier source above.
  The honest reason is that the fix is a helper plus a check and this run had no
  slot left; the honest second reason is that a check for "a chip says KM and no
  bar was drawn" can't be written from the render alone without the helper
  existing first.
- **A rule about repeated marks whose LENGTH varies without a declared
  quantity** (slide 07's eight incised rules). Real craft finding, wrong shape
  for machinery this run. It is a doctrine line, not a check: nothing in the
  render can tell a meaningful length encoding from a decorative one without a
  declaration, and inventing a declaration format is a redesign. Recommended as
  a DESIGN_DOCTRINE sentence in a session that is editing doctrine, which a
  routine run is forbidden to do.

---

## 5. VERIFICATION

Everything below was run in this retro and the output is quoted in the final
report. No gate was weakened, no test disabled, no threshold moved.

- `python3 scripts/trend_check.py --self-test` -> PASS (15 cases), new flag.
- `python3 scripts/trend_check.py --window 10` -> the `{'name'` row is gone and
  artwork craft reads 8/10 where it read 7/10.
- `python3 scripts/ship_gate.py --run-dir <a copy of runs/2026-09-14 forced
  below threshold>` -> prints `weakest criterion : Artwork craft and genuine
  detail` where it would have printed the mapping.
- `scripts/gmail_draft.py` imports clean.
- `python3 scripts/scout_bash_guard.py --self-test` -> PASS, 9 allow, 22 deny,
  plus the wiring check that fails if scout.md loses the hook or gains a write
  or spawn tool.
- The guard exercised as a hook over stdin: the real scout command exits 0, a
  `python3 -c` exits 2 with a reason, malformed stdin exits 2 (fail closed).
- `.claude/agents/scout.md` frontmatter parsed as YAML and checked against the
  hooks schema Claude Code actually enforces; the running binary contains the
  agent-hooks parser.
- `python3 scripts/fetch_pdf_text.py '<the Mat-Su ordinance PDF>' --pages 1
  --max-chars 420` -> returns the ordinance text, exit 0. That is the acceptance
  test, minus the scout process itself.
- `render.py` + `qa.py` on this run's nine slides -> PASS, 0 fails, 0 warns, and
  all nine PNGs are BYTE IDENTICAL to the shipped render (sha256 compared).
- `render.py` + `qa.py` on `examples/demo-deck` -> unchanged behaviour, its
  known pre-existing warns and no new ones.
- DEFECT RECONSTRUCTION, three slides built from this run's slide 08:
  noise injected into `form` -> WARN naming the region and the cause;
  the same slide with `landformIntended: true` -> silent;
  the same noise moved into `tone` -> silent, the house idiom still works.

LIVE TEST ATTEMPTED BY THE SHOWRUNNER, AND IT CAME BACK A THIRD ANSWER.
After the upgrade engineer handed back, the showrunner spawned a real scout and
told it to run five Bash commands, two that the guard must allow and three it
must deny. The scout reported that it had NO BASH TOOL AT ALL, so nothing ran
and nothing could be intercepted. It said so in its first line rather than
reporting the three denials as a pass, which is the right instinct and is worth
keeping.

The cause is almost certainly session scope rather than a broken change: this
session's agent definitions were loaded at wake, before `.claude/agents/scout.md`
was edited, and the tool list a subagent receives is fixed at that point. The
routine wakes in a fresh container cloned from the repo, so the next run is the
first process that can load the new definition, which is also the first run that
needs it.

WHAT THIS MEANS HONESTLY. The acceptance test is NOT passed. It is UNTESTED in a
live scout, and it stays untested until a fresh session runs. Every layer beneath
it is tested and quoted above, and the guard's own self-test asserts the wiring,
but nobody has yet watched a scout be refused. **The first job of the next Phase
12 is to run those five commands in a real scout and record the result**, before
it picks up anything from the declined list. If they all simply run, U1 reverts.

RESIDUAL RISK, stated rather than hidden: I am a subagent and non-negotiable 7
forbids me spawning one, so I could not run a real scout end to end. Every layer
under that is tested. The one untested link is Claude Code loading the
agent-level hook at scout-spawn time; if it silently did not, the scout would
have an unguarded `Bash` rather than none. That is why
`scout_bash_guard.py --self-test` also asserts the wiring, and why scout.md's
own prompt tells the scout in plain words that it never writes and never spawns.

## 5a. ONE THING THE MAINTAINER HAS TO KNOW ABOUT THE COMMIT

The upgrade set is NOT a single revertible commit this run, and that is worth a
sentence because the ledger's own rule says it should be. While this retro was
being written, the showrunner's ship commit `0d7d044e` ran a wide `git add` and
swept six in-flight upgrade files into itself, and that commit is already
pushed. Published history is not rewritten to tidy this up.

So the set reverts in two moves instead of one, and both are recorded in each
ledger entry's `rollback` field:

    git revert <the upgrade(2026-09-23) sha>        # akengrave.js, FIELD_NOTES, ledger
    git checkout 0d7d044e^ -- .claude/agents/scout.md .claude/agents/scorer.md \
        scripts/scout_bash_guard.py scripts/trend_check.py \
        scripts/ship_gate.py scripts/gmail_draft.py

The durable fix is for the ship step to stage paths rather than everything, or
to run Phase 12 to completion before the ship commit. That is a candidate for
the next Phase 12 and it is not one this retro may take, because it is a change
to the showrunner's own procedure in the middle of a run that is using it.

## 6. FILES TOUCHED

    .claude/agents/scout.md
    .claude/agents/scorer.md
    assets/js/akengrave.js
    scripts/scout_bash_guard.py      (new)
    scripts/trend_check.py
    scripts/ship_gate.py
    scripts/gmail_draft.py
    knowledge/FIELD_NOTES.md         (the parked scan entry)
    ledger/upgrades.json
    out/2026-09-23/automation_retro.md

No cron-written ledger, config or collector was read for writing or touched.

---

## 7. WHAT REVIEW CHANGED, AND THE UPGRADE THAT WAS WITHHELD (added at ship)

Codex reviewed this PR five times and found a real defect every round. All of
them are fixed. The last round changed a decision rather than a line, and that
is the part worth recording.

### The rounds, and what each one caught
1. Six findings, two security. The scout guard pinned the COMMAND and never the
   TARGET, so `fetch_pdf_text.py /etc/passwd` was allowed; the reader turns a
   bare path into file:// by itself. And a killed claim, the mover of adoption,
   was still published on the docket page in `key_dates` and `history` after
   the summary prose had been repaired.
2. Legacy numeric hosts. `http://2852039166/` is 169.254.169.254 and was
   ALLOWED, because `ipaddress.ip_address` rejects that spelling and the code
   treated a parse failure as proof of safety. Plus redirects, which a
   PreToolUse hook cannot see at all.
3. Carrier-grade NAT. `is_public` negated a hand-written list of flags and
   100.64.0.0/10 is neither private nor reserved.
4. Deprecated IPv6 site-local, which `is_global` itself calls global.
5. A REPRODUCED DNS rebinding, a transfer with no wall-clock bound, and the
   discovery that the documented rollback did not work.

### The decision
The scout's Bash grant is WITHHELD. `.claude/agents/scout.md` no longer grants
it, and the exact block that restores it sits in a comment at the top of that
file with the order to do it in.

Three facts compounded, and any two of them would have been survivable:

- **It was never exercised end to end.** The live scout this run spawned to
  probe the guard had no Bash tool at all, because the session loaded the agent
  definition before the file was edited. No denial has ever been seen to fire.
- **The fail-safe did not work.** I argued in three separate PR comments that
  shipping an untested capability was acceptable because the rollback was one
  commit. Review tested that claim and it is false: `git revert 444f6cd09171`
  conflicts on six paths. The argument I was relying on was wrong, and I only
  found out because someone checked it.
- **A reproduced bypass remained open.** DNS rebinding needs the socket pinned
  to the address that was validated, and urllib does not hand that over. It is
  real work, not a line.

Its benefit lands on the NEXT run at the earliest, because scouts only run in
Phase 2, so withholding it costs today nothing at all. An untested capability,
a live bypass and a fail-safe that does not fire is not a case for shipping
carefully. It is a case for not shipping.

### What did ship, and is worth keeping
`scripts/url_safety.py`, one address policy called by the reader before the
first request and again on every redirect hop. `scripts/fetch_pdf_text.py`
enforcing it, plus a whole-transfer deadline and `read1` so a server that
trickles one byte per tick cannot outlast a per-read timeout. The guard itself
with a 13 allow / 51 deny battery, inert while the grant is withheld and still
self-tested so it does not rot, and its wiring assertion rewritten as a
CONDITIONAL: if the scout is granted Bash, the hook must be attached. That
version stays useful for the case that actually matters, a future run pasting
the grant back and forgetting the hook.

U2 and U3 ship unchanged and are unaffected by any of this.

### For the next Phase 12, in this order
1. Close the DNS rebinding, connecting to a validated address while keeping the
   hostname for TLS and Host.
2. Paste the grant back.
3. FIRST ACT of that run, before anything else: spawn a real scout, have it run
   two allowed and three denied commands, and read back what happened. If the
   denials do not fire, take the grant out again.
