#!/usr/bin/env python3
"""caption_check_noblock_verify.py -- caption_check never waits on stdin, never
writes FAIL for a deck summary the run already declared, and never rewrites a
shipped report (2026-11-08, weekly pass; queue items 2026-10-31).

THE DEFECTS.
  - `caption_check.py --copy out/<date>/copy.json` with no caption path fell
    through to sys.stdin.read(). In a routine's shell stdin is an open pipe that
    never closes, so No.101 hung for the 120 s tool timeout and No.108 for 300 s,
    both stopped by hand.
  - a re-check without --deck-summary wrote FAIL over a passing report (No.101).
  - checking a caption under runs/<date>/ wrote caption_report.json over the
    shipped one (the 2026-11-08 pass did it by accident and restored it from git).

THE FIXTURES, built in a scratch run directory under out/ (gitignored) from a
shipped deck's caption.txt and copy.json (runs/2026-11-07), with its
deck_summary_line written to deck_summary.txt as a run writes it. stdin is an
OPEN PIPE throughout, which is the shape that hung:
  1. no caption path, --copy beside caption.txt -> returns in under 20 s and
     writes the same verdict as the explicit call
  2. no caption path, --copy in a directory with no caption.txt -> exit 2 at
     once, no report written
  3. explicit path, no --deck-summary, deck_summary.txt present -> no
     'no --deck-summary given' FAIL
  4. explicit path, no --deck-summary, no deck_summary.txt -> that FAIL stays
     (nothing loosened)
  5. the caption under runs/2026-11-07 -> verdict printed, the shipped report's
     bytes unchanged
  6. the script before this pass (cdb8d61b), case 1's call -> still running at
     5 s (the hang, reconstructed). Skipped with a note without git history.

  python3 tests/caption_check_noblock_verify.py     # exit 0 = all hold
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "caption_check.py"
SHIPPED = ROOT / "runs" / "2026-11-07"
BEFORE = "cdb8d61b"


def call(args, timeout=20, script=SCRIPT, cwd=ROOT):
    """Run with stdin an OPEN pipe that is never written or closed (communicate()
    would close it and hand the script an EOF, which is not the shape that hung)."""
    with tempfile.TemporaryFile("w+") as fo, tempfile.TemporaryFile("w+") as fe:
        p = subprocess.Popen([sys.executable, str(script)] + args, cwd=str(cwd),
                             stdin=subprocess.PIPE, stdout=fo, stderr=fe, text=True)
        try:
            rc = p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
            rc = None
        finally:
            p.stdin.close()
        fo.seek(0)
        fe.seek(0)
        return rc, fo.read(), fe.read()


def main():
    scratch = ROOT / "out"
    scratch.mkdir(exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="capnoblock_", dir=str(scratch)))
    ok = True

    def hold(name, cond, extra=""):
        nonlocal ok
        ok &= bool(cond)
        print("[%s] %s%s" % ("HOLD" if cond else "BROKE", name, "" if cond else "  " + extra))

    try:
        run = tmp / "2026-11-07"
        run.mkdir()
        for n in ("caption.txt", "copy.json"):
            shutil.copy(SHIPPED / n, run / n)
        line = json.loads((run / "copy.json").read_text())["deck_summary_line"]
        (run / "deck_summary.txt").write_text(line + "\n")
        led = ["--ledger", "ledger/captions.json"]

        rc, out, err = call([str(run / "caption.txt")] + led + ["--deck-summary", line,
                                                                "--copy", str(run / "copy.json")])
        want = json.loads((run / "caption_report.json").read_text())["verdict"]
        (run / "caption_report.json").unlink()

        rc, out, err = call(led + ["--copy", str(run / "copy.json")])
        rep = run / "caption_report.json"
        got = json.loads(rep.read_text())["verdict"] if rep.exists() else None
        hold("1. no path, --copy beside caption.txt: returned, verdict %s (explicit %s)" % (got, want),
             rc is not None and got == want, "rc %s" % rc)

        bare = tmp / "bare"
        bare.mkdir()
        shutil.copy(run / "copy.json", bare / "copy.json")
        rc, out, err = call(["--copy", str(bare / "copy.json")], cwd=bare)
        hold("2. no path, no caption.txt: exit %s, no report" % rc,
             rc == 2 and not (bare / "caption_report.json").exists(), err[-200:])

        rc, out, err = call([str(run / "caption.txt")] + led)
        rep = json.loads((run / "caption_report.json").read_text())
        hold("3. no --deck-summary, deck_summary.txt present: no missing-summary FAIL",
             not any("no --deck-summary given" in f for f in rep["fails"]), str(rep["fails"])[:200])

        (run / "deck_summary.txt").unlink()
        rc, out, err = call([str(run / "caption.txt")] + led)
        rep = json.loads((run / "caption_report.json").read_text())
        hold("4. no --deck-summary, no file: the missing-summary FAIL stays",
             any("no --deck-summary given" in f for f in rep["fails"]) and rc == 1)

        before = (SHIPPED / "caption_report.json").read_bytes()
        rc, out, err = call([str(SHIPPED / "caption.txt")])
        hold("5. a caption under runs/: verdict printed, shipped report unchanged",
             (SHIPPED / "caption_report.json").read_bytes() == before and "not written" in out,
             out[-200:])
        if (SHIPPED / "caption_report.json").read_bytes() != before:
            (SHIPPED / "caption_report.json").write_bytes(before)   # never leave it changed

        try:
            old = subprocess.run(["git", "-C", str(ROOT), "show", BEFORE + ":scripts/caption_check.py"],
                                 capture_output=True, text=True, check=True).stdout
        except (subprocess.CalledProcessError, OSError):
            old = None
        if old:
            # beside the real scripts so its sibling imports resolve; removed in finally
            oldp = ROOT / "scripts" / ("_caption_check_before_%s.py" % BEFORE)
            oldp.write_text(old)
            try:
                rc, out, err = call(["--ledger", str(ROOT / "ledger" / "captions.json"), "--copy",
                                     str(run / "copy.json")], timeout=5, script=oldp, cwd=bare)
            finally:
                oldp.unlink()
            hold("6. the pre-pass script on case 1's call is still waiting at 5 s (the hang)", rc is None,
                 "rc %s" % rc)
        else:
            print("(git history for %s not available: check 6 skipped)" % BEFORE)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("caption_check_noblock_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
