#!/usr/bin/env python3
"""topics_beats_check_verify.py -- the reconstruction behind
scripts/topics_beats_check.py (2026-11-01 weekly pass, queue item 2026-10-29).

  1. The committed ledger passes, and the check agrees with site_build.
  2. No.99's beats (federal-policy, models-and-public-numbers, north-slope) and
     No.101's (broadband-and-connectivity) FAIL, exit 1, each entry named, and
     site_build.topic_index refuses the same ledger (the two rules agree).
  3. An empty `beats` list FAILs in both; an entry with no `beats` passes.
  4. --date checks only that entry, and a date with no entry exits 1.

  python3 tests/topics_beats_check_verify.py    # exit 0 = all hold
No network. Writes only into a temp directory.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import site_build  # noqa: E402
import topics_beats_check as tb  # noqa: E402

CHECK = [sys.executable, str(ROOT / "scripts" / "topics_beats_check.py")]


def run(*args):
    p = subprocess.run(CHECK + list(args), capture_output=True, text=True)
    return p.returncode, p.stdout


def site_refuses(ledger):
    try:
        site_build.topic_index([], ledger)
    except ValueError:
        return True
    return False


def main():
    bad = []
    real = json.loads((ROOT / "ledger" / "topics.json").read_text())
    code, out = run()
    if code != 0 or tb.problems(real) or site_refuses(real):
        bad.append("1. the committed ledger: exit %d, problems %s, site refuses %s"
                   % (code, tb.problems(real), site_refuses(real)))
    with tempfile.TemporaryDirectory() as d:
        for name, beats, should_fail in [
            ("No.99", ["federal-policy", "models-and-public-numbers", "north-slope"], True),
            ("No.101", ["broadband-and-connectivity", "data-centers"], True),
            ("empty", [], True),
            ("absent", None, False),
            ("known", ["data-centers", "state-policy"], False),
        ]:
            led = {"entries": [dict(real["entries"][-1], run_date="2099-01-01")]}
            if beats is None:
                led["entries"][0].pop("beats", None)
            else:
                led["entries"][0]["beats"] = beats
            p = Path(d) / ("%s.json" % name.replace(".", ""))
            p.write_text(json.dumps(led))
            code, out = run("--ledger", str(p))
            ok = (code == 1 and "2099-01-01" in out) if should_fail else code == 0
            agrees = site_refuses(led) == should_fail
            if not ok or not agrees:
                bad.append("2/3. %s: exit %d (expected %d), site_build agrees %s: %s"
                           % (name, code, 1 if should_fail else 0, agrees, out.strip()[-200:]))
        p = Path(d) / "mixed.json"
        led = {"entries": [dict(real["entries"][-1], run_date="2099-01-01", beats=["north-slope"]),
                           dict(real["entries"][-1], run_date="2099-01-02", beats=["data-centers"])]}
        p.write_text(json.dumps(led))
        if run("--ledger", str(p), "--date", "2099-01-02")[0] != 0:
            bad.append("4. --date did not confine the check to its own entry")
        if run("--ledger", str(p), "--date", "2099-01-01")[0] != 1:
            bad.append("4. --date missed the bad entry")
        if run("--ledger", str(p), "--date", "2099-02-02")[0] != 1:
            bad.append("4. --date with no entry did not exit 1")
    if bad:
        print("BROKEN")
        for b in bad:
            print(" - " + b)
        return 1
    print("ALL HOLD: the committed ledger passes, No.99's and No.101's slugs and an empty "
          "list FAIL at append time, site_build refuses exactly the same ledgers, and "
          "--date checks one entry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
