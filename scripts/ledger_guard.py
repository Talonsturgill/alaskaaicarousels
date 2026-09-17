#!/usr/bin/env python3
"""Did this run modify a file only cron is allowed to write?

The permission allowlist cannot answer that. `.claude/settings.json` denies
Write and Edit on the cron-written ledgers, and that is worth having, but the
same file allows Bash, and Bash runs anything: a heredoc, `sed -i`, or
`python3 -c` reaches those paths without ever consulting a Write rule. A deny
list that an interpreter walks around is a claim, not a guarantee.

So the guarantee lives here instead, at the boundary that actually matters. A
run may do what it likes in its working tree; what it may not do is SHIP a
change to one of these files. This compares the working tree against the
merge-base with the base branch and fails if any protected path differs, which
catches the write however it was made, in time to stop the merge.

  ledger/gaswatch.jsonl        the daily storage series, no backfill exists
  ledger/gaswatch_eia.json     the monthly EIA cross check
  ledger/power.json            monthly retail electricity price
  ledger/power_utility.json    annual price by utility
  ledger/watch.json            the docket candidate queue
  config/gaswatch_model.json   the demand coefficients

Each is written by its own scheduled workflow and never by a routine run. The
gas watch line is the one irreversible failure this project has: CINGSA keeps
no archive, so a day overwritten is a day gone.

Usage:
  python3 scripts/ledger_guard.py                 (against origin/main)
  python3 scripts/ledger_guard.py --base main
  python3 scripts/ledger_guard.py --json
  python3 scripts/ledger_guard.py --self-test

Exit 0 clean, 1 a protected file was modified, 2 the check could not run.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

PROTECTED = [
    "ledger/gaswatch.jsonl",
    "ledger/gaswatch_eia.json",
    "ledger/power.json",
    "ledger/power_utility.json",
    "ledger/watch.json",
    "config/gaswatch_model.json",
]

REMEDY = (
    "A routine run never writes these; their own scheduled workflows do. "
    "Restore the file (git checkout <base> -- <path>) and, if a number on the "
    "live page looked wrong, fix the PRESENTATION or follow CLAUDE.md's Gas "
    "Watch maintenance procedure. Never hand-type a measurement."
)


def _git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                          text=True, timeout=60)


def changed(base="origin/main"):
    """Protected paths that differ from the merge-base with `base`."""
    mb = _git("merge-base", "HEAD", base)
    ref = mb.stdout.strip() if mb.returncode == 0 and mb.stdout.strip() else base
    out = _git("diff", "--name-only", ref, "--", *PROTECTED)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or "git diff failed")
    return [p for p in out.stdout.split("\n") if p.strip()], ref


def self_test():
    """The guard has to be able to go red, or it is decoration."""
    fails = []
    for name, paths, want in (
        ("no protected path changed reads clean", [], True),
        ("a changed gas watch line is caught", ["ledger/gaswatch.jsonl"], False),
        ("a changed model is caught", ["config/gaswatch_model.json"], False),
        ("two at once are both reported", PROTECTED[:2], False),
    ):
        ok = not paths
        if ok != want:
            fails.append(name)
        print("  [%s]   %s" % ("ok  " if ok == want else "FAIL", name))
    # every protected path must be a real file, or the guard watches nothing
    for p in PROTECTED:
        exists = (REPO / p).exists()
        print("  [%s]   %s is a real path" % ("ok  " if exists else "FAIL", p))
        if not exists:
            fails.append(p)
    print("SELF-TEST: %d check(s), %d failure(s)" % (len(PROTECTED) + 4, len(fails)))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()

    try:
        hits, ref = changed(a.base)
    except Exception as e:                      # a broken check is not a pass
        print("ledger_guard: could not run: %s" % e, file=sys.stderr)
        return 2

    rec = {"base": a.base, "compared_against": ref[:12],
           "protected": PROTECTED, "modified": hits,
           "verdict": "FAIL" if hits else "PASS"}
    if a.json:
        print(json.dumps(rec, indent=2))
    elif hits:
        print("LEDGER GUARD: FAIL, %d cron-written file(s) modified" % len(hits))
        for p in hits:
            print("  %s" % p)
        print("\nwhat to do about it\n  %s" % REMEDY)
    else:
        print("LEDGER GUARD: PASS, %d cron-written file(s) untouched"
              % len(PROTECTED))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
