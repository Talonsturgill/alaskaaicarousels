#!/usr/bin/env python3
"""Prove the draft's sign-off table prints VERDICTS, never the artifact index.

WHY THIS EXISTS
    Run No.64 (2026-09-20) built a draft whose "The live site, looked at today"
    table read:

      GAS WATCH   ['out/2026-09-20/gaswatch_health.json', 'out/2026-09-20/cron_health.json']

    and carried no SITE SIGN-OFF row at all, on a day the live gas watch audit
    returned MAINTENANCE and the site sign-off returned WARN with an UNFIXED
    finding. Both verdicts existed; both were in run_state.

    Two faults, one section:

    1. run_state's `artifacts` maps each phase to a LIST OF FILENAMES. That is
       the field's documented shape, so artifacts["gas_watch"] is ALWAYS a list
       of paths. `_look` rejected dicts and accepted everything else, so the
       list answered ahead of the real verdict and its repr landed in the cell.
    2. That run recorded Phase 3.6 under run_state["phase_3_6"] with the
       phase's own key names, which no earlier run had used, and nothing read
       it. So the rows that WOULD have been right were invisible.

    This is the fourth costume of the same bug, and the section exists to
    prevent exactly it: a report that omits the warning while still looking
    complete. The UNREPORTED guard could not save it either, because the
    filename list counted as a substantive answer.

WHAT IT CHECKS
    1. RED CASE, the exact No.64 shape. A filename list in artifacts must not
       reach the table, and phase_3_6's own lines must.
    2. The live audit still OUTRANKS the local page check, whichever scope
       each one sits in, including when the local one is in phase_3_6.
    3. A run with no sign-off anywhere still prints UNREPORTED, and neither
       cron_health nor site_fixes can satisfy that guard on its own.
    4. The pre-existing shapes still work: top-level scalars (2026-09-17) and
       the one-dict form (2026-08-25).
    5. Every shipped run under runs/ renders a table with no repr in it, so
       the check runs against artifacts that actually exist.

USAGE
    python3 tests/gmail_signoff_verify.py

Exit 0 = HOLDS, 1 = a defect is present.
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "gmail_draft.py"

# The minimum an out/ run dir needs for gmail_draft.py to build a body. The
# sign-off block is wrapped in its own try, so a thin fixture still exercises
# it; anything richer only adds sections this test does not read.
MIN_COPY = {
    "run_date": "2026-09-20",
    "carousel_no": 64,
    "document_title": "Fixture",
    "post_copy": "A fixture post.\n\n#Alaska",
    "first_comment": "Sources.\nhttps://example.org/",
    "slides": [{"n": 1, "kicker": "K", "headline": "H", "body": "B", "claim_ids": []}],
}

MIN_SCORE = {
    "run_date": "2026-09-20",
    "carousel_no": 64,
    "threshold": 8.3,
    "weighted_total": 8.5,
    "ship": True,
    "hard_fails": [],
    "criteria": [],
}

MIN_ASM = {"pdf_mode": "vector", "pdf_mb": 9.47, "slides": 1, "thumbs": []}

# HERMETIC OR IT IS NOT A TEST (Codex, PR #391). gmail_draft.py's readership
# section shells out to read_stats.py against a public endpoint with a 60
# second timeout. This suite builds a body once per fixture and once per
# archived run, so a slow or half-open endpoint would turn a bounded check into
# a half-hour one issuing dozens of live requests. The script's own
# GMAIL_DRAFT_NO_NETWORK switch skips that section; nothing this suite reads
# comes from it.
ENV = dict(os.environ, GMAIL_DRAFT_NO_NETWORK="1")


def render(run_state):
    """Build a draft against a throwaway run dir and return its plain text."""
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "run"
        (run / "final" / "thumbs").mkdir(parents=True)
        (run / "final" / "carousel.pdf").write_bytes(b"%PDF-1.4\n%%EOF\n")
        (run / "run_state.json").write_text(json.dumps(run_state))
        (run / "copy.json").write_text(json.dumps(MIN_COPY))
        (run / "score_report.json").write_text(json.dumps(MIN_SCORE))
        (run / "final" / "assemble_report.json").write_text(json.dumps(MIN_ASM))
        out = Path(td) / "payload.json"
        r = subprocess.run(
            [sys.executable, str(SCRIPT),
             "--run-dir", str(run), "--run-date", "2026-09-20",
             "--carousel-no", "64", "--branch", "main",
             "--raw-base", "https://raw.githubusercontent.com/o/r/main",
             "--payload-out", str(out), "--preview-mode", "remote"],
            capture_output=True, text=True, cwd=str(ROOT), env=ENV)
        if r.returncode != 0:
            raise RuntimeError("gmail_draft.py failed:\n" + (r.stderr or r.stdout))
        body = json.loads(out.read_text())["html_body"]
    i = body.find("The live site, looked at today")
    if i < 0:
        return ""
    seg = body[i:body.find("</table>", i) + 8]
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", seg))).strip()


def row(text, label):
    """The cell text for one label, or None when the row is absent."""
    m = re.search(re.escape(label) + r" (.*?)(?= SITE SIGN-OFF | GAS WATCH | CRON HEALTH | SITE FIXES | UNREPORTED |$)", text)
    return m.group(1).strip() if m else None


FAILURES = []


def check(name, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + name + (("  -- " + detail) if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def main():
    print("1. RED CASE: run No.64's own shape")
    t = render({
        "artifacts": {
            "gas_watch": ["out/2026-09-20/gaswatch_health.json",
                          "out/2026-09-20/cron_health.json"],
            "ship": ["runs/2026-09-20/"],
        },
        "phase_3_6": {
            "site_signoff": "WARN, 117 pages, 18 checks, UNFIXED gaswatch.jsonl is current",
            "gaswatch_pagecheck": "WARN, published reading 2026-09-13, 7 days old",
            "gaswatch_live": "MAINTENANCE, checked 2026-09-20T07:15:15Z",
            "cron_health": "WARN on output:docket-watch",
            "site_fixes": "none needed on presentation",
        },
    })
    check("no filename reaches the table", "gaswatch_health.json" not in t, t)
    check("no python repr in the table", "[" not in t and "'" not in t, t)
    check("SITE SIGN-OFF present", (row(t, "SITE SIGN-OFF") or "").startswith("WARN, 117 pages"), t)
    check("GAS WATCH is the LIVE verdict", "MAINTENANCE" in (row(t, "GAS WATCH") or ""), t)
    check("CRON HEALTH present", "docket-watch" in (row(t, "CRON HEALTH") or ""), t)
    check("no UNREPORTED banner", "UNREPORTED" not in t, t)

    print("2. the live audit outranks the local page check")
    t = render({
        "artifacts": {"gas_watch": ["x.json"]},
        "gas_watch": "GAS WATCH: PASS, page is current",
        "phase_3_6": {"site_signoff": "PASS, 117 pages",
                      "gaswatch_live": "FAIL, checked 2026-09-20T07:15:15Z"},
    })
    check("live FAIL answers, not the local PASS",
          "FAIL" in (row(t, "GAS WATCH") or "") and "PASS, page is current" not in t, t)

    print("3. the UNREPORTED guard still fires")
    t = render({"artifacts": {"gas_watch": ["x.json"]},
                "phase_3_6": {"cron_health": "WARN", "site_fixes": "none"}})
    check("UNREPORTED when both required lines are missing", "UNREPORTED" in t, t)
    check("it names the site sign-off", "site sign-off" in t, t)
    check("it names the gas watch verdict", "gas watch verdict" in t, t)
    check("cron_health alone does not satisfy the guard", "UNREPORTED" in t, t)

    print("4. the shapes earlier runs used still work")
    t = render({"site_signoff": "PASS, 117 pages", "gas_watch_verdict": "PASS"})
    check("top-level scalars (2026-09-17)",
          (row(t, "SITE SIGN-OFF") or "").startswith("PASS, 117")
          and "UNREPORTED" not in t, t)
    t = render({"artifacts": {"site_signoff": {
        "line": "PASS, 110 pages", "gas_watch_line": "PASS", "fixes": "two links"}}})
    check("the one-dict form (2026-08-25)",
          (row(t, "SITE SIGN-OFF") or "").startswith("PASS, 110")
          and "two links" in t and "UNREPORTED" not in t, t)

    print("5. a single artifact PATH is no more a verdict than a list of them")
    # 2026-09-19's artifacts.cron_health is the bare string
    # "out/2026-09-19/cron_health.json" while its phase_3_6.cron_health is
    # "PASS". Rejecting only list reprs printed the filename and suppressed the
    # verdict (Codex, PR #391).
    t = render(json.loads((ROOT / "runs" / "2026-09-19" / "run_state.json").read_text()))
    check("the 2026-09-19 cron row is its verdict", (row(t, "CRON HEALTH") or "") == "PASS", t)
    t = render({"artifacts": {"site_signoff": "out/x/site_signoff.json",
                              "gas_watch": "out/x/gaswatch_health.json"},
                "phase_3_6": {"site_signoff": "PASS, 117 pages",
                              "gaswatch_live": "MAINTENANCE"}})
    check("a path never answers for a verdict",
          (row(t, "SITE SIGN-OFF") or "").startswith("PASS, 117")
          and "MAINTENANCE" in (row(t, "GAS WATCH") or ""), t)
    t = render({"artifacts": {"site_signoff": "out/x/site_signoff.json"}})
    check("a path alone still reads UNREPORTED", "UNREPORTED" in t, t)

    print("6. every shipped run renders clean")
    seen, pathy = 0, re.compile(r"\S+/\S+\.[A-Za-z0-9]{1,6}\b")
    for st in sorted((ROOT / "runs").glob("*/run_state.json")):
        try:
            rs = json.loads(st.read_text())
        except Exception:
            continue
        t = render(rs)
        seen += 1
        for label in ("SITE SIGN-OFF", "GAS WATCH", "CRON HEALTH", "SITE FIXES"):
            cell = row(t, label)
            if not cell:
                continue
            # No repr, and no bare artifact path standing in for a line. A cell
            # MENTIONING a file in prose is fine; a cell that IS one is not.
            if "[" in cell or (pathy.fullmatch(cell.strip()) is not None):
                check("runs/" + st.parent.name + " " + label + " is a verdict", False, cell)
    check("at least one shipped run was rendered", seen > 0, str(seen))
    print("  (" + str(seen) + " shipped run_state files rendered)")

    print()
    if FAILURES:
        print("DEFECT PRESENT: " + ", ".join(FAILURES))
        return 1
    print("HOLDS: the sign-off table prints verdicts, and says so when it has none.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
