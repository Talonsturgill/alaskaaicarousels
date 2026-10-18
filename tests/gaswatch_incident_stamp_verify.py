#!/usr/bin/env python3
"""gaswatch_incident_stamp_verify.py -- the reconstruction behind gate_status's
gas_watch_live row holding an incident record to the CI bar (2026-10-17, weekly
machine pass).

WHAT IT RECONSTRUCTS. When the live Gas Watch audit fails on an external blocker
the run files out/<date>/gaswatch_incident.json and ships with the row at WARN.
The row accepted any record with blocker, reason, attempts and evidence_urls,
while the PR's `checks` job runs site_signoff --ci, whose incident_allows() also
requires audit_checked_utc (a string with a time and an offset, under 36 hours
old). So a run read WARN at its own gate and met exit 2 on CI: No.86's PR #434,
fixed by hand (c20cb314). Seven of the eleven shipped incident records, from
2026-09-27 to 2026-10-12, carry no stamp at all.

  python3 tests/gaswatch_incident_stamp_verify.py     # exit 0 = the row holds

Drives gate_status.gas_watch_live_row on a scratch run directory with a FAILING
audit and each record below, then runs the same unstamped record through
HEAD's gate_status to show the old row passed it as WARN. No network.
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import gate_status as G  # noqa: E402

NOW = datetime.now(timezone.utc)
STAMP = NOW.strftime("%Y-%m-%dT%H:%M:%SZ")
AUDIT = {"checked_utc": STAMP, "site_url": "https://alaskaaihq.com", "verdict": "FAIL",
         "checks": [{"id": "source reading published", "status": "FAIL"}]}
BASE = {"blocker": "github",
        "reason": "the 04:40Z scheduled collection had not started and workflow_dispatch returns 403",
        "attempts": ["workflow_dispatch from the session, 403"],
        "evidence_urls": ["https://github.com/tsturgill/alaskaaicarousels/actions/workflows/gaswatch.yml"]}


def row(gs, incident, audit=AUDIT):
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "2026-10-17"
        run.mkdir()
        (run / "gaswatch_health.json").write_text(json.dumps(audit))
        if incident is not None:
            (run / "gaswatch_incident.json").write_text(json.dumps(incident))
        rows = gs.Rows(True)
        gs.gas_watch_live_row(rows, run)
        r = rows.rows[0]
        return r["status"], r["detail"]


def head_module():
    src = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:scripts/gate_status.py"],
                         capture_output=True, text=True)
    if src.returncode != 0:
        return None
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
        fh.write(src.stdout)
    spec = importlib.util.spec_from_file_location("gate_status_head", fh.name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    bad = []

    def check(label, got, want, needle=""):
        st, detail = got
        ok = st == want and needle in detail
        print("  %s  %-58s %s: %s" % ("ok  " if ok else "FAIL", label, st, detail[:120]))
        if not ok:
            bad.append(label)

    old = (NOW - timedelta(hours=40)).strftime("%Y-%m-%dT%H:%M:%SZ")
    check("unstamped record FAILs, naming the field", row(G, BASE), "FAIL", "no audit_checked_utc")
    check("stamped from the audit's checked_utc WARNs", row(G, dict(BASE, audit_checked_utc=STAMP)), "WARN",
          "UNRESOLVED github")
    check("a 40 hour old stamp FAILs", row(G, dict(BASE, audit_checked_utc=old)), "FAIL", "over 36h")
    check("a date-only stamp FAILs", row(G, dict(BASE, audit_checked_utc=STAMP[:10])), "FAIL", "malformed")
    check("an unopenable evidence URL FAILs", row(G, dict(BASE, audit_checked_utc=STAMP,
                                                           evidence_urls=["https://"])), "FAIL",
          "field is malformed")
    check("no record at all still FAILs", row(G, None), "FAIL", "repair or document")
    check("a passing audit ignores the record", row(G, BASE, dict(AUDIT, verdict="PASS", checks=[{"id": "source reading published", "status": "PASS"}])),
          "PASS", "")

    # every shipped record, as written, then re-stamped as a run would today
    shipped = sorted(ROOT.glob("runs/*/gaswatch_incident.json"))
    unstamped = 0
    for p in shipped:
        rec = json.loads(p.read_text())
        if "audit_checked_utc" not in rec:
            unstamped += 1
            check("shipped %s, unstamped, FAILs" % p.parent.name, row(G, rec), "FAIL", "no audit_checked_utc")
        check("shipped %s, stamped now, WARNs" % p.parent.name,
              row(G, dict(rec, audit_checked_utc=STAMP)), "WARN", "UNRESOLVED")
    print("  ..   %d shipped records, %d without audit_checked_utc" % (len(shipped), unstamped))

    head = head_module()
    if head is not None and "_incident_why" not in open(head.__file__).read():
        st, detail = row(head, BASE)
        print("  ..   HEAD's row on the unstamped record: %s (%s)" % (st, detail[:80]))
        if st != "WARN":
            bad.append("HEAD reconstruction")
    print("GASWATCH INCIDENT STAMP: " + ("HOLDS" if not bad else "BROKEN: " + "; ".join(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
