#!/usr/bin/env python3
"""browser_suites.py -- run the site's browser suites the one safe way
(2026-10-02, run No.75).

WHY THIS EXISTS. CI runs four browser suites against a freshly built site
(tests/ask_engine.mjs, home_ask.mjs and docket_ask.mjs in ask.yml,
power_line.mjs in power-utility.yml), and the documented local recipe was CI's:
build into /tmp/site and run `node tests/<suite>.mjs`. In a routine run both
halves of that recipe leave the project. /tmp is outside it, and the ESM
suites could not find the global playwright, so on 2026-10-01 and again on
2026-10-02 the showrunner linked node_modules to a scratch directory under
/tmp. Every command that then touched the link, and the `rm` to clean it up,
resolved outside the allowed directories, the harness asked permission, and
No.75 sat about nine hours waiting for a human who was not there.

WHAT IT DOES INSTEAD. One command, allowlisted as `Bash(python3:*)`:

  python3 scripts/browser_suites.py [--date YYYY-MM-DD] [--suite NAME ...]

  1. Refuses to start if a node_modules in the repo root or tests/ is a link,
     or resolves outside the repo, and says what it found. It does not delete
     it: a delete is a destructive step and gets its own decision.
  2. Builds the site into out/<date>/site (gitignored scratch, inside the
     project), with scripts/site_build.py exactly as CI does. A --site
     path that does not resolve under the repo's out/ is refused.
  3. Runs each suite with SITE set to that directory. Playwright is found by
     tests/playwright_resolve.mjs (repo node_modules, NODE_PATH, then the
     running node's global root), so nothing is linked or installed.

Exit 0 every suite passed, 1 a suite failed or the build failed, 2 refused.
`--self-test` checks the two refusals without building anything.
"""

import argparse
import datetime as dt
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"
SUITES = ["ask_engine", "home_ask", "docket_ask", "power_line"]


def today_anchorage():
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo("America/Anchorage")).date().isoformat()
    except Exception:
        return dt.date.today().isoformat()


def link_hazards(root=ROOT):
    """node_modules entries that would send a command outside the project."""
    bad = []
    for d in (root, root / "tests"):
        nm = d / "node_modules"
        if not (nm.is_symlink() or nm.exists()):
            continue
        if nm.is_symlink():
            bad.append("%s is a link to %s" % (nm, os.readlink(nm)))
            continue
        real = nm.resolve()
        if not real.is_relative_to(root.resolve()):
            bad.append("%s resolves outside the repo, to %s" % (nm, real))
    return bad


def site_ok(site, out=OUT):
    """A site directory must resolve under the repo's out/ (links followed)."""
    try:
        return Path(site).resolve().is_relative_to(out.resolve())
    except OSError:
        return False


def self_test():
    ok = True
    with tempfile.TemporaryDirectory(dir=OUT if OUT.is_dir() else None) as t:
        t = Path(t)
        (t / "tests").mkdir()
        clean = not link_hazards(t)
        # ANY link is refused, so the test link points at a sibling inside its
        # own scratch tree: this test never makes a link that leaves the repo
        (t / "elsewhere").mkdir()
        (t / "tests" / "node_modules").symlink_to(t / "elsewhere")
        caught = len(link_hazards(t)) == 1
        for name, good in (("clean tree has no hazard", clean),
                           ("a node_modules link out of the repo is refused", caught)):
            print("  %s  %s" % ("ok  " if good else "BAD ", name))
            ok = ok and good
    for path, want in ((OUT / "2026-10-02" / "site", True), (Path("/tmp/site"), False),
                       (OUT / ".." / ".." / "site", False)):
        good = site_ok(path) == want
        print("  %s  site %s %s" % ("ok  " if good else "BAD ", path,
                                     "accepted" if want else "refused"))
        ok = ok and good
    print("BROWSER SUITES SELF-TEST: " + ("HOLDS" if ok else "BROKEN"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--date", default=None, help="build date, default today in Anchorage")
    ap.add_argument("--site", default=None, help="default out/<date>/site; must be under out/")
    ap.add_argument("--suite", action="append", choices=SUITES,
                    help="run only this suite (repeatable); default all four")
    ap.add_argument("--no-build", action="store_true", help="reuse an existing build")
    ap.add_argument("--timeout", type=int, default=900, help="seconds per suite")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()

    date = a.date or today_anchorage()
    site = Path(a.site) if a.site else OUT / date / "site"
    if not site.is_absolute():
        site = ROOT / site
    if not site_ok(site):
        print("REFUSED: %s is not under %s. Build the site inside the project; a path "
              "outside it raises a permission prompt in a routine run." % (site, OUT))
        return 2
    hz = link_hazards()
    if hz:
        print("REFUSED: " + "; ".join(hz) + ". Nothing here needs a node_modules link: "
              "tests/playwright_resolve.mjs finds the global playwright on its own.")
        return 2

    if not a.no_build or not (site / "docket" / "index.html").exists():
        site.mkdir(parents=True, exist_ok=True)
        print("building the site into %s" % site.relative_to(ROOT))
        b = subprocess.run([sys.executable, str(ROOT / "scripts/site_build.py"),
                            "--date", date, "--out", str(site)], cwd=ROOT)
        if b.returncode != 0:
            print("FAIL: site_build exited %d" % b.returncode)
            return 1

    env = dict(os.environ, SITE=str(site))
    results = []
    for name in a.suite or SUITES:
        print("\n== %s" % name, flush=True)
        try:
            r = subprocess.run(["node", str(ROOT / "tests" / (name + ".mjs"))],
                               cwd=ROOT, env=env, timeout=a.timeout)
            code = r.returncode
        except subprocess.TimeoutExpired:
            print("timed out after %d s" % a.timeout)
            code = 124
        results.append((name, code))
    print("\nBROWSER SUITES (site %s)" % site.relative_to(ROOT))
    for name, code in results:
        print("  %s  %s%s" % ("PASS" if code == 0 else "FAIL", name,
                              "" if code == 0 else "  (exit %d)" % code))
    return 0 if all(c == 0 for _, c in results) else 1


if __name__ == "__main__":
    sys.exit(main())
