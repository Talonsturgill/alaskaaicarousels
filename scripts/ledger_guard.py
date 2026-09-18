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
    # The observed weather history behind the demand model, written by
    # scripts/gaswatch_hdd.py inside .github/workflows/gaswatch-eia.yml. It was
    # missed on the first pass and it is not hypothetical: the last commit to
    # touch it came in on a routine run's PR, which is the exact leak this
    # guard exists to close.
    "config/gaswatch_hdd_history.json",
]

REMEDY = (
    "A routine run never writes these; their own scheduled workflows do. "
    "Restore the file (git checkout <base> -- <path>) and, if a number on the "
    "live page looked wrong, fix the PRESENTATION or follow CLAUDE.md's "
    "scheduled-job maintenance procedure. Never hand-type a measurement."
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
    """The guard has to be able to go red, and the test has to prove it DOES.

    The first version of this function asserted `ok = not paths` over a
    hard-coded fixture and never called changed() at all, so it stayed green no
    matter what the merge-base, the pathspec or the result parsing did. That is
    the same mistake this repo just spent a day correcting elsewhere: a test
    that shows the detector fires is not a test that the detector works. This
    builds a real git repository in a temporary directory, commits a baseline,
    edits protected and unprotected files, and runs the actual diff against it.
    """
    import tempfile
    global REPO
    fails, checks = [], 0

    def check(name, got, want):
        nonlocal checks
        checks += 1
        ok = got == want
        if not ok:
            fails.append("%s (got %r, wanted %r)" % (name, got, want))
        print("  [%s]   %s" % ("ok  " if ok else "FAIL", name))

    real_repo = REPO
    with tempfile.TemporaryDirectory() as td:
        sand = Path(td)
        REPO = sand                                  # changed() reads REPO
        try:
            _git("init", "-q", "-b", "main")
            _git("config", "user.email", "t@t"); _git("config", "user.name", "t")
            for p in PROTECTED + ["scripts/keep.py", "docs/index.html"]:
                f = sand / p
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text("baseline\n")
            _git("add", "-A"); _git("commit", "-qm", "baseline")
            # Work on a BRANCH, the way a run does. Committing onto main itself
            # makes the merge-base equal HEAD and every diff empty, which is
            # how the first version of this test read green against a guard
            # that was never asked anything.
            _git("checkout", "-q", "-b", "work")

            check("a clean tree reports nothing", changed("main")[0], [])

            (sand / "scripts/keep.py").write_text("an ordinary edit\n")
            (sand / "docs/index.html").write_text("a rebuilt page\n")
            _git("add", "-A"); _git("commit", "-qm", "unprotected work")
            check("editing unprotected files stays clean", changed("main")[0], [])

            (sand / "ledger/gaswatch.jsonl").write_text("a hand-typed reading\n")
            _git("add", "-A"); _git("commit", "-qm", "touch the gas watch")
            check("a changed gas watch line is caught",
                  changed("main")[0], ["ledger/gaswatch.jsonl"])

            (sand / "config/gaswatch_model.json").write_text("{}\n")
            _git("add", "-A"); _git("commit", "-qm", "touch the model")
            check("two at once are both reported", sorted(changed("main")[0]),
                  sorted(["ledger/gaswatch.jsonl", "config/gaswatch_model.json"]))

            # every protected path must be reachable by the pathspec, or the
            # guard silently watches nothing
            for p in PROTECTED:
                (sand / p).write_text("moved\n")
            _git("add", "-A"); _git("commit", "-qm", "touch them all")
            check("every protected path is detectable",
                  sorted(changed("main")[0]), sorted(PROTECTED))
        finally:
            REPO = real_repo

    for p in PROTECTED:                              # back in the real repo
        check("%s is a real file here" % p, (REPO / p).exists(), True)

    print("SELF-TEST: %d check(s), %d failure(s)" % (checks, len(fails)))
    for f in fails:
        print("  %s" % f)
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
