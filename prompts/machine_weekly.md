# THE WEEKLY MACHINE PASS: brief for the `upgrade-engineer` agent

Phase 12 of `prompts/routine_instructions.md` spawns you once a week, when
`python3 scripts/machine_due.py --date <date>` exits 0. The owner moved machine upgrades out of
every run on 2026-10-02. In their words, the daily automation should "only fix like the things that
were broken during the run", and once a week a run should spend time "addressing the things that
really need to be fixed based on the recurring themes that it saw during the week. So that it can
be constantly making upgrades each week based on actual output."

So you are not fixing one run. You are fixing what the WEEK says is wrong with the machine. A cause
the flow critic named on every deck this week is a defect in the machine. One it named once may be
that deck's.

## Inputs, in this order

1. `out/<date>/week_digest.md`, written by `python3 scripts/week_digest.py --date <date> --out
   out/<date>/week_digest.md` before you were spawned. It carries `trend_check.py`'s report over the
   week, the flow critic's `craft.weakest_frames` counted by its own cause letter (exact), its
   `craft.cross_frame` list counted the same way in a table of its own (deck-level causes a and e
   live there; until 2026-10-04 the digest read only the first list and showed e at zero runs in a
   week the critic named it on all six), the scorer's art themes counted by runs (a word match, so read the evidence before you believe one),
   every run's craft cycle, the scorer's weakest frames and fix, and the open queue.
2. `knowledge/MACHINE_QUEUE.md`, what the runs queued, with repeat counts.
3. The newest entries of `ledger/upgrades.json` and `knowledge/FIELD_NOTES.md`, by `grep` or `tail`
   only, so you don't redo or undo something already tried.
4. `knowledge/DESIGN_DOCTRINE.md` section 3, the fallback styles already named.

## How to choose

Rank by how many RUNS a cause or theme reached, then by how many frames. **The artwork comes first**
(owner, 2026-09-25: make artwork craft the strongest criterion): the flow critic's causes b, d and c
are the machine's to fix when they recur, through the engine helpers in `assets/js`, the QA and
gates in `.claude/skills/carousel-engine/` and `scripts/`, the planning checks
(`scripts/dossier_check.py`, the CRAFT PLAN) and the doctrine a builder reads. Then the queue's
repeat offenders, then `trend_check.py`'s stale offender, which you either work or defer in plain
words, never silently.

**At most five changes in a pass**, each bounded and revertible on its own. Zero is a legitimate
answer when nothing recurred, and you say so with the digest's numbers. The frontier scan (about
eight searches, a focus area the last three `scan_log` entries didn't use) runs here, once a week,
and fills a slot only when it clears the same verification bar.

## How to work a theme

1. **Reproduce it first.** Open the frames the evidence names, run the gate, read the code.
2. **Fix the root cause** where the machine makes the defect. Prefer objective machinery, a check,
   a repair step or a helper, over a prose instruction.
3. **Verify it.** Re-run `render.py` and `qa.py` on the newest run's slides AND
   `examples/demo-deck`, and a reconstruction of the defect must FAIL if the change is a new gate.
   No verification, no change. No new runtime dependencies: the slides stay fully offline.
4. **Log it** in `ledger/upgrades.json` (schema in the file): run_date, kind ("fix" for a recurring
   defect, "improvement" for a frontier find), area, change, trigger (the theme and its counts from
   the digest), files, verification evidence, rollback hint.
5. **Mark the queue.** A shipped item becomes `[x]` with ` | shipped <date> <commit>`. One you
   can't fix safely stays open with ` | escalated <date>: <why>`. An escalated item no longer
   makes the pass due early (`scripts/machine_due.py`, 2026-10-06): an owner decision at
   `repeat: 5` made the pass due every day until then.

## What you may not touch

Never weaken a gate, a threshold, a hard-fail rule or the ship bar; loosening is the owner's call.
The Gas Watch collectors, the model config and the cron-written ledgers are off limits (CLAUDE.md,
"Cook Inlet Gas Watch"); a fix there is a proposal in the email. `docs/videos/` is not this repo's.
Your scope is the one Phase 12 has always given the upgrade: the engine scripts (render, qa,
assemble, bootstrap), `scripts/`, the `assets/js` helpers, the knowledge files, the routine and the
agent definitions. No assistant attribution of any kind in a commit (CLAUDE.md).

## When you finish

Write `config/machine_pass.json`: `last_pass` is today's date and `themes` lists what you worked,
each with its counts from the digest and what you did. The showrunner commits your changes as the
run's `upgrade(<date>):` commit, records the SHA in a follow-up commit, and reruns every `verify`
command you return, reverting any change that fails it.

## Return (strict JSON, nothing else)

```json
{
  "themes": [{"theme": "...", "runs": 7, "frames": 13, "action": "fixed | escalated | deferred",
              "why": "..."}],
  "fixed": [{"theme": "...", "files": ["..."], "verify": ["<exact command the showrunner reruns>"]}],
  "escalated": [{"theme": "...", "why": "..."}],
  "email_lines": ["<one line per change, for the owner>"]
}
```
