#!/usr/bin/env python3
"""dossier_truncated_verify.py -- the reconstruction behind the 2026-09-21
repair to dossier_check.py's early exits and to gate_status.py's dossier row.
One defect from run No.65, four fixtures, no browser.

THE DEFECT, in two halves that only bite together.

  1. `dossier_check.py --json` had two exits that fired before it could build a
     report -- storyboard.md missing, and no "## SLIDE NN" dossiers in it -- and
     both printed PROSE on the --json path.
  2. `gate_status.py`'s dossier row runs that script and `json.loads` its
     stdout. The JSONDecodeError landed in an `except` that called `absent()`,
     which is the helper for an artifact that has not been written yet: it
     prints "[n/a ]" until --require. So the loudest failure the gate can
     produce arrived as the quietest row it can print.

WHAT IT COST. No.65's storyboard reached round three with its deck header, its
continuity tables and its BUILD RECONCILIATION section intact and ZERO dossiers
between them. `[n/a ] dossier_check could not run (JSONDecodeError)` printed for
two rounds and stopped nothing. All six human-proxy critics in round two
reported that they had judged the frames against the deck header because the
per-slide contracts were not on disk, so two rounds of acceptance checklists
were never checked, and the `reconciled` row passed throughout because it tests
for PRESENCE.

WHAT IS CHECKED HERE:

  1. truncated storyboard  -> dossier_check --json emits JSON, verdict FAIL, and
                              the sentence says TRUNCATED rather than "no
                              dossiers found", because a reconciliation section
                              with nothing to reconcile is only ever that
  2. missing storyboard    -> dossier_check --json still emits JSON (FAIL)
  3. truncated storyboard  -> the gate_status row is FAIL, NOT n/a, without
                              --require, and the row quotes the sentence
  4. no run dir at all     -> the gate_status row is still n/a without --require
                              (this is the case `absent()` is for, and the
                              repair must not swallow it)

Fixture 4 is the control: "the check could not run" and "the artifact is not
written yet" are different sentences, and the repair separates them rather than
turning every n/a into a FAIL.

Usage: python tests/dossier_truncated_verify.py   (exit 0 = all four hold)
No network, no browser. Writes only into a temp directory.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHECK = REPO / "scripts" / "dossier_check.py"

TRUNCATED = """# STORYBOARD -- run 2026-09-21, Carousel No. 65

Deck header, continuity tables, everything but the dossiers.

## CONTINUITY

| slide | ink | camera |
|---|---|---|
| 01 | gold | 0.0 |

## BUILD RECONCILIATION

| slide | dossier CAM | built CAM |
|---|---|---|
| 01 | 0.0 | 0.0 |

Nothing diverged on slide 01.
"""


def load_gate_status():
    spec = importlib.util.spec_from_file_location(
        "gate_status_undertest", REPO / "scripts" / "gate_status.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dossier_row_status(gs, run):
    rows = gs.Rows(False)          # NOT --require: this is the mid-run print
    gs.dossier_row(rows, Path(run))
    r = [x for x in rows.rows if x["gate"] == "dossier_check"]
    return (r[0]["status"], r[0]["detail"]) if r else ("MISSING", "no row")


def main():
    tmp = Path(tempfile.mkdtemp(prefix="dossiertrunc_"))
    trunc = tmp / "truncated"
    trunc.mkdir()
    (trunc / "storyboard.md").write_text(TRUNCATED)
    nosb = tmp / "no_storyboard"
    nosb.mkdir()
    absent = tmp / "never_created"

    results = []
    try:
        p = subprocess.run([sys.executable, str(CHECK), "--run-dir", str(trunc),
                            "--json"], capture_output=True, text=True, timeout=60)
        try:
            rep = json.loads(p.stdout)
        except Exception as e:
            rep = {"_err": "%s: %r" % (type(e).__name__, p.stdout[:120])}
        fails = [f for s in rep.get("slides", []) for f in s.get("fails", [])]
        results.append((
            "truncated storyboard: --json emits a FAIL report",
            rep.get("verdict") == "FAIL" and any("TRUNCATED" in f for f in fails),
            rep.get("_err") or (fails[0][:150] if fails else str(rep)[:150])))

        p = subprocess.run([sys.executable, str(CHECK), "--run-dir", str(nosb),
                            "--json"], capture_output=True, text=True, timeout=60)
        try:
            rep2 = json.loads(p.stdout)
        except Exception as e:
            rep2 = {"_err": "%s: %r" % (type(e).__name__, p.stdout[:120])}
        results.append((
            "missing storyboard: --json still emits JSON",
            rep2.get("verdict") == "FAIL",
            rep2.get("_err") or str(rep2.get("slides"))[:150]))

        gs = load_gate_status()
        st, detail = dossier_row_status(gs, trunc)
        results.append((
            "gate_status row on it is FAIL, not n/a, without --require",
            st == "FAIL" and "TRUNCATED" in detail, "%s: %s" % (st, detail[:150])))

        st2, detail2 = dossier_row_status(gs, absent)
        results.append((
            "an artifact not written yet is still n/a (the control)",
            st2 == "n/a", "%s: %s" % (st2, detail2[:150])))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    ok = True
    for name, good, note in results:
        ok &= good
        print("[%s] %-56s -> %s" % ("HOLD" if good else "BROKE", name, note))
    print("dossier_truncated_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
