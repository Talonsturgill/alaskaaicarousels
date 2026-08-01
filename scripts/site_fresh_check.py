#!/usr/bin/env python3
"""
Proves the committed docs/ is what site_build.py produces from committed data.

A run ships two things that can silently disagree: the run record under runs/
and ledger/, and the built site under docs/. Nothing checked that they matched,
so a build that ran too early, or ran with the wrong --date, shipped a site
that looked fine and was wrong.

Both failures are real:

  2026-08-01  The run tagged its deck to three beats (land and permitting,
              defense and federal, state policy) and committed a docs/ build
              that credited only state policy. The live beat counts
              under-reported by one and the article page linked one beat
              instead of three. Nobody noticed, because a stale page renders
              exactly as well as a fresh one.

  2026-08-01  A development session rebuilt with --date 2026-07-29 while main
              was at 2026-08-01, rolling the whole site back three days. Caught
              only because the diff was bigger than the change that produced
              it, which is luck, not a process.

The build is deterministic (the grain PRNG is seeded, the date is an argument,
nothing else varies), so "rebuild and compare" is an exact test rather than a
heuristic one. Run it AFTER site_build.py in Phase 11, with the same --date.

Files that live in docs/ but that site_build.py does not emit (committed fonts,
logo.png, the og images, awesomeproposal/) are reported and ignored. They are
hand-managed by design. The failure this catches is a page that IS generated
and does not match its own generator.

Usage:  python scripts/site_fresh_check.py --date <YYYY-MM-DD>
Exit 0 when docs/ is exactly a fresh build, 1 otherwise.
"""
from __future__ import annotations

import argparse
import filecmp
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def walk(root: Path) -> set[str]:
    return {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True,
                    help="the run date, the SAME one passed to site_build.py")
    ap.add_argument("--docs", default=str(ROOT / "docs"))
    args = ap.parse_args()

    docs = Path(args.docs)
    if not docs.is_dir():
        print(f"FAIL: {docs} is not a directory", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        fresh = Path(tmp) / "site"
        r = subprocess.run(
            [sys.executable, str(HERE / "site_build.py"),
             "--date", args.date, "--out", str(fresh)],
            capture_output=True, text=True)
        if r.returncode != 0:
            print("FAIL: the rebuild itself failed, so docs/ cannot be trusted "
                  "either.", file=sys.stderr)
            print(r.stderr.strip()[-2000:], file=sys.stderr)
            return 1

        built, have = walk(fresh), walk(docs)
        missing = sorted(built - have)
        differ = sorted(p for p in (built & have)
                        if not filecmp.cmp(fresh / p, docs / p, shallow=False))
        untracked = sorted(have - built)

    if untracked:
        print(f"note: {len(untracked)} file(s) in docs/ that site_build.py does "
              f"not emit, ignored (hand-managed assets)")

    if not missing and not differ:
        print(f"OK: docs/ is exactly a fresh build at --date {args.date} "
              f"({len(built)} generated files)")
        return 0

    print(f"FAIL: docs/ is not what site_build.py builds from the committed "
          f"data at --date {args.date}.", file=sys.stderr)
    if missing:
        print(f"  {len(missing)} generated page(s) absent from docs/:",
              file=sys.stderr)
        for p in missing[:20]:
            print(f"    {p}", file=sys.stderr)
    if differ:
        print(f"  {len(differ)} page(s) differ from their generator:",
              file=sys.stderr)
        for p in differ[:20]:
            print(f"    {p}", file=sys.stderr)
    print("  Rebuild with the RUN date and commit the result. If you meant to "
          "change the site, change site_build.py, not docs/.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
