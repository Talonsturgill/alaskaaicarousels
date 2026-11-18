#!/usr/bin/env python3
"""dedupe_earlier_verify.py -- dedupe_check.py scans the 31 to 120 days that
ledger/topics.json's _spec binds, not only the routine's 30 (2026-11-17, weekly
machine pass; queue items 2026-10-24 and 2026-11-17).

  python3 tests/dedupe_earlier_verify.py      # exit 0 = every check holds

Hermetic: builds its own ledger in a temp dir, then re-checks the real one.
  spec      ledger/topics.json's _spec still says 90 days and 120 days, the two
            numbers the script hard-codes (fails if the owner moves either).
  44 days   a repeat of an entry 44 days back (No.117 vs No.77's shape) is a
            LIKELY DUPLICATE in the earlier section and exits 1; with
            --earlier-window 0 (the old behaviour) it exits 0 and prints CLEAR.
  100 days  the same repeat at 100 days prints, tagged matching scan only,
            and exits 0.
  30 days   an in-window repeat behaves exactly as before (exit 1, no earlier
            section needed).
  brief     --scout-brief prints an EARLIER block with the 44-day entry and
            not the 130-day one.
  real      on the real ledger at 2026-11-17, the Wood River/Bristol Bay
            candidate names No.77 and exits 1.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dedupe_check.py"
sys.path.insert(0, str(ROOT / "scripts"))


def run(*args):
    r = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout


def entry(date, no, headline):
    return {"run_date": date, "carousel_no": no, "headline": headline,
            "topic": "Kuskokwim sonar escapement counting with a drone camera pilot",
            "angle": "count methods", "entities": ["Kuskokwim River", "Bethel sonar station",
                                                   "Orutsararmiut Native Council"],
            "keywords": ["salmon escapement", "sonar", "drone counting"]}


def main():
    import dedupe_check as dc
    checks = []
    spec = json.loads((ROOT / "ledger" / "topics.json").read_text())["_spec"]
    checks.append(("spec: topics.json still binds %d days" % dc.SPEC_REPEAT_DAYS,
                   ("within %d days" % dc.SPEC_REPEAT_DAYS) in spec.get("purpose", ""), ""))
    checks.append(("spec: topics.json still scans %d days" % dc.SPEC_MATCH_DAYS,
                   ("last %d days" % dc.SPEC_MATCH_DAYS) in spec.get("matching", ""), ""))
    cand = ["--entities", "Kuskokwim River, Bethel sonar station", "--keywords", "salmon escapement, sonar",
            "--date", "2026-11-17"]
    with tempfile.TemporaryDirectory() as td:
        led = Path(td) / "topics.json"

        def write(*entries):
            led.write_text(json.dumps({"_spec": spec, "entries": list(entries)}))

        write(entry("2026-10-04", 77, "Forty-four days back"))
        code, out = run(*cand, "--topics", str(led))
        checks.append(("44 days: LIKELY DUPLICATE in the earlier section, exit 1",
                       code == 1 and "EARLIER COVERAGE" in out and "inside the 90-day repeat rule" in out
                       and "No.77" in out.split("STRONGEST MATCH")[-1], "exit %d" % code))
        code, out = run(*cand, "--topics", str(led), "--earlier-window", "0")
        checks.append(("44 days, old behaviour (--earlier-window 0): exit 0, CLEAR",
                       code == 0 and "CLEAR to proceed" in out, "exit %d" % code))
        code, out = run(*cand, "--topics", str(led), "--json")
        js = json.loads(out)
        checks.append(("44 days, --json carries it under 'earlier' and exits 1",
                       code == 1 and js["matches"] == [] and js["earlier"][0]["carousel_no"] == 77, ""))

        write(entry("2026-08-09", 40, "A hundred days back"))
        code, out = run(*cand, "--topics", str(led))
        checks.append(("100 days: printed as matching scan only, exit 0",
                       code == 0 and "91 to 120 days, matching scan only" in out and "No.40" in out,
                       "exit %d" % code))

        write(entry("2026-11-01", 112, "Sixteen days back"))
        code, out = run(*cand, "--topics", str(led))
        checks.append(("16 days: in-window LIKELY DUPLICATE as before, exit 1, no earlier section",
                       code == 1 and "EARLIER COVERAGE" not in out and "[LIKELY DUPLICATE] No.112" in out,
                       "exit %d" % code))

        write(entry("2026-10-04", 77, "Forty-four days back"), entry("2026-07-10", 3, "One-thirty back"),
              entry("2026-11-10", 115, "Seven days back"))
        code, out = run("--scout-brief", "--date", "2026-11-17", "--topics", str(led))
        head, _, early = out.partition("\nEARLIER, 31 to 120 days back")
        checks.append(("brief: the 7-day entry stays in the main block",
                       "No.115" in head and "No.115" not in early, ""))
        checks.append(("brief: EARLIER block has the 44-day entry and not the 130-day one",
                       code == 0 and "No.77" in early and "No.3" not in out, ""))
    code, out = run("--desc", "Wood River drone salmon counting sonar Bristol Bay", "--date", "2026-11-17")
    checks.append(("real: the No.117 candidate names No.77 (44 days) and exits 1",
                   code == 1 and "No.77 2026-10-04, 44 days ago" in out, "exit %d" % code))
    bad = [c for c in checks if not c[1]]
    for name, ok, det in checks:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  -- " + det) if det and not ok else ""))
    print("%d/%d checks hold" % (len(checks) - len(bad), len(checks)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
