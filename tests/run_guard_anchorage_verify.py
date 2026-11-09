#!/usr/bin/env python3
"""run_guard_anchorage_verify.py -- run_guard names the Anchorage date beside its
UTC default (2026-11-08, weekly pass; queue item 2026-10-24, repeat 5).

THE DEFECT. The routine's run date is the America/Anchorage date and the trigger
wakes at about 06:05Z, the previous evening in Anchorage all winter. With no
--run-date, run_guard read the UTC date, so it named tomorrow on every November
run (No.109 at 06:07Z, Anchorage 21:07 on November 8th), and a re-fire of a
deck that had shipped that evening would read CLEAR for tomorrow and start a
second deck. The default and exit code stay as they were (owner's call); the
Anchorage date is now printed with its own verdict.

THE FIXTURES, in a scratch repo under out/ (gitignored), run_guard's REPO
pointed at it, the clock fixed at 2026-11-09 06:07Z:
  1. nothing shipped for either date -> exit 0, NOTE names 2026-11-08 CLEAR
  2. runs/2026-11-08 holds nine slides (a re-fire) -> exit 0 as before, and the
     NOTE reads ALREADY_SHIPPED with the RE-FIRE line; --json carries
     anchorage_verdict ALREADY_SHIPPED
  3. --run-date 2026-11-08 given -> exit 3, no NOTE (an explicit date is final)
  4. a clock at 2026-11-09 20:00Z (both dates agree) -> no NOTE

  python3 tests/run_guard_anchorage_verify.py     # exit 0 = all hold
"""
import contextlib
import datetime as dt
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_guard  # noqa: E402

WAKE = dt.datetime(2026, 11, 9, 6, 7, tzinfo=dt.timezone.utc)


def call(argv, now=WAKE):
    buf = io.StringIO()
    code = None
    with contextlib.redirect_stdout(buf):
        try:
            run_guard.main(argv, now=now)
        except SystemExit as e:
            code = e.code
    return code, buf.getvalue()


def main():
    scratch = ROOT / "out"
    scratch.mkdir(exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="runguard_", dir=str(scratch)))
    ok = True

    def hold(name, cond, extra=""):
        nonlocal ok
        ok &= bool(cond)
        print("[%s] %s%s" % ("HOLD" if cond else "BROKE", name, "" if cond else "  " + extra[:300]))

    real = run_guard.REPO
    try:
        (tmp / "ledger").mkdir()
        (tmp / "ledger" / "topics.json").write_text(json.dumps({"entries": [{}] * 108}))
        (tmp / "runs").mkdir()
        run_guard.REPO = tmp

        code, out = call([])
        hold("1. nothing shipped: exit %s, NOTE names 2026-11-08 CLEAR" % code,
             code == 0 and "2026-11-09 -> CLEAR" in out
             and "Anchorage is on 2026-11-08, which reads CLEAR" in out, out)

        d = tmp / "runs" / "2026-11-08"
        d.mkdir()
        for n in range(1, 10):
            (d / ("slide-%02d.webp" % n)).write_bytes(b"x")
        (d / "run_state.json").write_text(json.dumps({"status": "complete"}))
        code, out = call([])
        hold("2. a re-fire: exit %s as before, NOTE reads ALREADY_SHIPPED with the RE-FIRE line" % code,
             code == 0 and "which reads ALREADY_SHIPPED" in out and "RE-FIRE" in out, out)
        code, out = call(["--json"])
        js = json.loads(out)
        hold("2. --json carries anchorage_verdict %s" % js.get("anchorage_verdict"),
             js.get("anchorage_date") == "2026-11-08"
             and js.get("anchorage_verdict") == "ALREADY_SHIPPED"
             and js.get("utc_date") == "2026-11-09", out)

        code, out = call(["--run-date", "2026-11-08"])
        hold("3. explicit --run-date: exit %s, no NOTE" % code, code == 3 and "NOTE" not in out, out)

        code, out = call([], now=dt.datetime(2026, 11, 9, 20, 0, tzinfo=dt.timezone.utc))
        hold("4. both dates agree: no NOTE", "NOTE" not in out and code == 0, out)
    finally:
        run_guard.REPO = real
        shutil.rmtree(tmp, ignore_errors=True)
    print("run_guard_anchorage_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
