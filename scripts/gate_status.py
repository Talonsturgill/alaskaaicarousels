#!/usr/bin/env python3
"""gate_status.py -- print the run's GATE STATUS block straight from the
artifacts, so no hand-written sentence can contradict what is on disk.

Why this exists (2026-07-25): the first hand-written BUILD RECONCILIATION of
that run claimed "qa.py PASS, zero warns" while machine_qa.json on disk said
WARN with 5, and the scorer had to catch it. The same run's completion gate
false-flagged a VALID caption_report.json because it tested the file with a
200-byte size threshold and the valid file is 196 bytes. Both are the same
mistake: a human sentence or a byte count standing in for the artifact. This
script reads the artifacts (JSON is PARSED, never measured; binaries are
checked by magic bytes) and emits the block verbatim.

And why --verify-pasted exists (2026-08-05): printing "Do not hand-write these
lines" was not enough. Run No.26 pasted the block once, ran four more render
rounds under it, and shipped a run record contradicting its own artifacts on
four rows plus an unresolved [FAIL] site_fresh row -- caught by the SCORER, at
the ship gate. --verify-pasted regenerates the block and diffs it against the
one in the run record, so staleness is a check rather than a habit.

And why --sync exists (2026-08-07): making staleness a check was still not
enough. Run No.28 violated the same instinct TWICE in one run, at 0.95
confidence, and its scorer read a record claiming 29 qa warns and a missing
score report on a deck measuring 20 that had scored. The check only ran at the
completion gate, after every reader it could have protected, and the refresh
itself was a hand copy-paste -- the one step a re-render cannot re-run for you.
--sync writes the fresh block into the run record itself. It is idempotent, so
"run it again after every round" is a rule with no cost to obey.

Usage:
  python scripts/gate_status.py --run-dir out/2026-07-25
  python scripts/gate_status.py --run-dir out/2026-07-25 --require   # ship gate
  python scripts/gate_status.py --run-dir out/2026-07-25 --json
  python scripts/gate_status.py --run-dir out/2026-08-07 \
      --sync out/2026-08-07/storyboard.md          # after every round + pre-scorer
  python scripts/gate_status.py --run-dir out/2026-08-05 \
      --verify-pasted out/2026-08-05/storyboard.md                   # ship gate
  python scripts/gate_status.py --self-test        # hermetic block-plumbing test

Read-only apart from --sync (which rewrites only the block inside the file it is
given). Stdlib only. Exit 0 when no gate row is FAIL (WARN rows are fine),
1 when any row FAILs (with --require, a missing or unparseable artifact FAILs).
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def load_json(path):
    """Return (obj, note). A JSON artifact is judged by PARSING it, never by
    its size: a valid 196-byte report is valid (2026-07-25 false flag)."""
    if not path.exists():
        return None, "missing"
    try:
        return json.loads(path.read_text()), None
    except Exception as e:
        return None, "unparseable (%s)" % type(e).__name__


def binary_ok(path, magic):
    if not path.exists():
        return False, "missing"
    b = path.read_bytes()[:8]
    if not b:
        return False, "empty"
    if magic and not b.startswith(magic):
        return False, "not a %s file (bad magic)" % magic.decode("latin-1").strip("%")
    return True, None


def image_ok(path, magic):
    """A magic-byte check passes a truncated slide: a WebP keeps its RIFF header
    and a PNG its signature no matter where the file was cut. This reads the
    whole file and checks it terminates the way the format requires, so a slide
    truncated mid-stream fails the ship gate instead of merging to main and
    404-ing nothing while displaying half an image. Pillow verifies it fully
    when present; the structural checks stand alone when it is not."""
    ok, note = binary_ok(path, magic)
    if not ok:
        return ok, note
    b = path.read_bytes()
    if magic == b"\x89PNG":
        # PNG must end with the IEND chunk and its CRC.
        if not b.rstrip(b"\x00").endswith(b"IEND\xaeB`\x82"):
            return False, "truncated PNG (no IEND trailer)"
    elif magic == b"RIFF":
        # RIFF stores total size at bytes 4..8; it must match the file.
        if len(b) < 12:
            return False, "truncated WebP (%d bytes)" % len(b)
        import struct
        declared = struct.unpack("<I", b[4:8])[0] + 8
        if declared != len(b):
            return False, "truncated WebP (RIFF says %d bytes, file is %d)" % (declared, len(b))
    try:
        from PIL import Image
        with Image.open(path) as im:
            im.verify()
    except ImportError:
        pass
    except Exception:
        return False, "corrupt image (failed to decode)"
    return True, None


def pdf_ok(path):
    """%PDF magic passes a 64-byte stub. A real carousel PDF is hundreds of KB
    and ends with an %%EOF trailer; require both so a truncated or empty-shell
    PDF fails rather than shipping as the email's download link."""
    ok, note = binary_ok(path, b"%PDF")
    if not ok:
        return ok, note
    b = path.read_bytes()
    if len(b) < 4096:
        return False, "PDF only %d bytes (truncated)" % len(b)
    if b"%%EOF" not in b[-2048:]:
        return False, "truncated PDF (no %%EOF trailer)"
    return True, None


def first(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and k in d and d[k] is not None:
            return d[k]
    return default


class Rows:
    def __init__(self, require):
        self.rows = []
        self.require = require

    def add(self, name, status, detail):
        self.rows.append({"gate": name, "status": status, "detail": detail})

    def absent(self, name, note):
        # A gate whose artifact does not exist yet is n/a mid-run and a FAIL at
        # the ship gate, where every artifact must be present and parseable.
        self.add(name, "FAIL" if self.require else "n/a", note)


def render_row(rows, rdir):
    rep, note = load_json(rdir / "render_report.json")
    if rep is None:
        rows.absent("render", "render/render_report.json %s" % note)
        return None
    slides = rep.get("slides", [])
    ok = sum(1 for s in slides if s.get("ok"))
    errs = sum(len(s.get("page_errors", [])) for s in slides)
    warns = sum(len(s.get("overflow_warnings", [])) for s in slides)
    warns += sum(1 for s in slides if s.get("body_overflow"))
    status = "FAIL" if (errs or ok != len(slides) or not slides) else ("WARN" if warns else "PASS")
    rows.add("render", status, "%d/%d slides OK, %d page errors, %d overflow warnings"
             % (ok, len(slides), errs, warns))
    return rep


def qa_row(rows, rdir):
    qa, note = load_json(rdir / "machine_qa.json")
    if qa is None:
        rows.absent("qa.py", "render/machine_qa.json %s" % note)
        return
    verdict = str(qa.get("verdict", "?")).upper()
    detail = "%s, %s fails, %s warns" % (verdict, qa.get("fails", "?"), qa.get("warns", "?"))
    named = [s["file"] for s in qa.get("slides", []) if s.get("fails")]
    if named:
        detail += " (fails on %s)" % ", ".join(named)
    # Honor the verdict and the per-slide fail lists, not the top-level counter
    # alone. A machine_qa.json with a stale fails:0 but verdict FAIL, or a slide
    # carrying a fail with the counter never incremented, used to stamp PASS
    # while the row itself spelled out the failing slide. This gate exists
    # because a summary once disagreed with the artifact; it must not repeat
    # that with a summary field.
    fail = qa.get("fails") or named or verdict == "FAIL"
    warn = qa.get("warns") or verdict == "WARN"
    status = "FAIL" if fail else ("WARN" if warn else "PASS")
    rows.add("qa.py", status, detail)


def dossier_row(rows, run):
    """The planning-time lower-third gate (2026-07-26). Run by the storyboard
    gate in Phase 5; surfaced here so the GATE STATUS block shows whether the
    plan itself cleared field 4a, not just whether the pixels did."""
    sb = run / "storyboard.md"
    if not sb.exists():
        rows.absent("dossier_check", "storyboard.md missing")
        return
    try:
        p = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "dossier_check.py"),
             "--run-dir", str(run), "--json"],
            capture_output=True, text=True, timeout=60)
        rep = json.loads(p.stdout)
    except Exception as e:
        rows.absent("dossier_check", "could not run (%s)" % type(e).__name__)
        return
    rows.add("dossier_check", rep.get("verdict", "?"),
             "%s, %d dossiers, %s fails, %s warns" % (
                 rep.get("verdict", "?"), len(rep.get("slides", [])),
                 rep.get("fails", "?"), rep.get("warns", "?")))


def caption_row(rows, run):
    cap, note = load_json(run / "caption_report.json")
    if cap is None:
        rows.absent("caption_check", "caption_report.json %s" % note)
        return
    verdict = cap.get("verdict", "?")
    detail = "%s, %s chars, hook %s, %d hashtags" % (
        verdict, cap.get("chars", "?"), cap.get("hook_len", "?"),
        len(cap.get("hashtags") or []))
    if cap.get("fails"):
        detail += " (%d fail: %s)" % (len(cap["fails"]), cap["fails"][0][:60])
    status = "FAIL" if cap.get("fails") else ("WARN" if cap.get("warns") else "PASS")
    # THE REPORT HAS TO HAVE LOOKED AT THE SLIDES (2026-08-15). caption_check
    # only walks copy.json when it is given --copy, and this row simply read
    # whatever report was lying there. A run that invoked it without --copy got
    # a green caption row while the slide bodies had never been scanned for a
    # banned phrase or a bare date at all, which is how run No.34 carried a
    # hard fail ('actionable', slide 02) to within one phase of the email, and
    # three no-ordinal dates in first_comment alongside it. copy_fields_checked
    # is written only on the --copy path, so its absence IS the evidence.
    if "copy_fields_checked" not in cap:
        status = "FAIL"
        detail += (" -- written WITHOUT --copy, so copy.json's slide bodies "
                   "and first_comment were never scanned; re-run caption_check "
                   "with --copy out/<date>/copy.json")
    rows.add("caption_check", status, detail)


def copy_sync_row(rows, run, rdir):
    copyj, cnote = load_json(run / "copy.json")
    script = REPO / "scripts" / "copy_sync_check.py"
    if copyj is None:
        rows.absent("copy_sync", "copy.json %s" % cnote)
        return
    if not (rdir / "render_report.json").exists() or not script.exists():
        rows.absent("copy_sync", "render_report.json or copy_sync_check.py missing")
        return
    try:
        p = subprocess.run([sys.executable, str(script), "--copy", str(run / "copy.json"),
                            "--render-report", str(rdir / "render_report.json")],
                           capture_output=True, text=True, timeout=120)
    except Exception as e:
        # A check that could not run is a FAIL at the ship gate, not a pass.
        # This was the only row that hard-coded n/a on a subprocess failure, so
        # a timeout or launch error let a stale copy.json ship with the
        # record-sync tripwire silently never having run. Its siblings
        # (scanner_sync, docket_dates) use absent() for exactly this reason.
        rows.absent("copy_sync", "could not run copy_sync_check (%s)" % type(e).__name__)
        return
    line = (p.stdout.strip().splitlines() or [""])[-1] if p.returncode else \
        (p.stdout.strip().splitlines() or [""])[0]
    rows.add("copy_sync", "PASS" if p.returncode == 0 else "FAIL", line[:140])


def plan_drift_row(rows, run, rdir):
    """THE PLAN AND THE BUILD HAVE TO AGREE ABOUT THE BUILD (2026-08-20).
    Run No.38's scorer flagged plan-versus-pixel drift in all three scoring
    rounds and no gate could see any of it: the claims index kept assigning
    ids to slides that never printed them, and a dossier still said FIVE
    declared marks after three shipped. Exit 2 means the check could not
    look, which is a FAIL like its siblings."""
    script = REPO / "scripts" / "plan_drift_check.py"
    if not script.exists():
        rows.absent("plan_drift", "scripts/plan_drift_check.py missing")
        return
    if not (run / "storyboard.md").exists():
        rows.absent("plan_drift", "storyboard.md missing")
        return
    cmd = [sys.executable, str(script), "--run-dir", str(run)]
    if (rdir / "render_report.json").exists():
        cmd += ["--render-report", str(rdir / "render_report.json")]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except Exception as e:
        rows.absent("plan_drift", "could not run plan_drift_check (%s)"
                    % type(e).__name__)
        return
    out = (p.stdout + p.stderr).strip().splitlines() or [""]
    if p.returncode == 2:
        rows.add("plan_drift", "FAIL", "check could not look: %s" % out[0][:120])
        return
    if p.returncode == 0:
        rows.add("plan_drift", "PASS", out[-1][:140])
        return
    first = next((l.strip() for l in out if l.strip().startswith("FAIL:")), out[0])
    rows.add("plan_drift", "FAIL", "%s (%s)" % (out[-1][:80], first[:90]))


def aggregate_row(rows, run, rdir):
    """Every number a slide DERIVES from claims (a count, a span, a duration, a
    ratio) is a fresh factual assertion that claims_check and copy_sync_check
    structurally cannot see. Run 2026-08-02 printed FIVE STATE POSTINGS with a
    federal industry day inside the five and every machine gate passed it. Exit
    2 means the check could not look, which is a FAIL like its siblings."""
    script = REPO / "scripts" / "aggregate_check.py"
    if not script.exists():
        rows.absent("aggregate", "scripts/aggregate_check.py missing")
        return
    if not (rdir / "render_report.json").exists():
        rows.absent("aggregate", "render_report.json missing")
        return
    cmd = [sys.executable, str(script), "--run-dir", str(run),
           "--render-report", str(rdir / "render_report.json"),
           "--report", str(run / "aggregate_report.json")]
    if not (run / "claims.json").exists() and (run.parent / "claims.json").exists():
        cmd += ["--claims", str(run.parent / "claims.json")]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except Exception as e:
        rows.absent("aggregate", "could not run aggregate_check (%s)" % type(e).__name__)
        return
    out = (p.stdout + p.stderr).strip().splitlines() or [""]
    if p.returncode == 2:
        rows.add("aggregate", "FAIL", "check could not run: %s" % out[0][:120])
        return
    line = out[-1] if p.returncode == 0 else out[0]
    rows.add("aggregate", "PASS" if p.returncode == 0 else "FAIL", line[:140])


def bespoke_row(rows, run):
    """The engine is a HARNESS, not a template, and until 2026-08-05 nothing
    measured that. Run No.26 shipped nine slides generated from one build script
    where every frame called the same six drawing functions, median pairwise art
    similarity 0.940 against 0.049 for the bespoke reference, and the run wrote a
    justification for it into its own storyboard. The maintainer caught it by
    looking at the deck and reported engagement falling with it."""
    script = REPO / "scripts" / "bespoke_check.py"
    if not script.exists():
        rows.absent("bespoke", "scripts/bespoke_check.py missing")
        return
    slides = run / "slides"
    if not slides.is_dir():
        rows.absent("bespoke", "slides/ missing")
        return
    try:
        p = subprocess.run([sys.executable, str(script), "--slides-dir",
                            str(slides)], capture_output=True, text=True,
                           timeout=180)
    except Exception as e:
        rows.absent("bespoke", "could not run bespoke_check (%s)" % type(e).__name__)
        return
    out = (p.stdout + p.stderr).strip().splitlines() or [""]
    if p.returncode == 2:
        rows.add("bespoke", "FAIL", "check could not look: %s" % out[0][:120])
        return
    line = out[-1] if p.returncode == 0 else out[0]
    rows.add("bespoke", "PASS" if p.returncode == 0 else "FAIL", line[:140])


def scanner_sync_row(rows):
    """Repo-level, not run-level: the run rebuilds docs/ and ships whatever the
    scanner page currently says, so the contract behind it is a ship gate like
    any other. Exit 2 means the check could not look, which is a FAIL and not a
    pass, because a blind check is how the last drift got through."""
    script = REPO / "scripts" / "scanner_sync_check.py"
    if not script.exists():
        rows.absent("scanner_sync", "scripts/scanner_sync_check.py missing")
        return
    try:
        p = subprocess.run([sys.executable, str(script)],
                           capture_output=True, text=True, timeout=180)
    except Exception as e:
        rows.add("scanner_sync", "FAIL", "could not run scanner_sync_check (%s)" % type(e).__name__)
        return
    out = (p.stdout + p.stderr).strip().splitlines() or [""]
    if p.returncode == 0:
        rows.add("scanner_sync", "PASS", "the live scan page still matches the routine contract")
    elif p.returncode == 2:
        rows.add("scanner_sync", "FAIL", "check could not run: %s" % out[0][:120])
    else:
        rows.add("scanner_sync", "FAIL", out[0][:140])


def docket_dates_row(rows):
    """Repo-level like scanner_sync: the run rebuilds docs/ from the ledger
    Phase 3.5 just edited, so a date rendered into the wrong slot ships with
    the run. This is the gate that would have caught COMMENT NOW, CLOSES AUG 13
    on the AIDEA item, six days before its real close and for a different
    body's vote. Exit 2 means it could not look, which is a FAIL and not a
    pass."""
    script = REPO / "scripts" / "docket_dates_check.py"
    if not script.exists():
        rows.absent("docket_dates", "scripts/docket_dates_check.py missing")
        return
    try:
        p = subprocess.run([sys.executable, str(script)],
                           capture_output=True, text=True, timeout=300)
    except Exception as e:
        rows.add("docket_dates", "FAIL", "could not run docket_dates_check (%s)" % type(e).__name__)
        return
    out = (p.stdout + p.stderr).strip().splitlines() or [""]
    if p.returncode == 0:
        rows.add("docket_dates", "PASS", out[-1][:140])
    elif p.returncode == 2:
        rows.add("docket_dates", "FAIL", "check could not look: %s" % out[0][:120])
    else:
        rows.add("docket_dates", "FAIL", out[0][:140])


def gas_watch_row(rows):
    """Repo-level: the gas watch series is only worth publishing if it is whole.

    CINGSA keeps no archive, so a day that goes uncollected cannot be recovered
    later and a gap is permanent. This checks the three things that make the
    series citable: no missing day between the first and last record, exactly
    one standing record per date, and a latest reading recent enough that the
    page is not quietly serving a number from last week. Staleness is a WARN
    rather than a FAIL because the collector runs on its own schedule and a
    carousel run must never be blocked by it."""
    ledger = REPO / "ledger" / "gaswatch.jsonl"
    if not ledger.exists():
        rows.absent("gas_watch", "ledger/gaswatch.jsonl missing")
        return
    try:
        sys.path.insert(0, str(REPO / "scripts"))
        import gaswatch_build as gwb
        series = gwb.load_series(str(ledger))
        model = gwb.gc.load_model(str(REPO / "config" / "gaswatch_model.json"))
        gwb.figures(series, model)          # every published figure recomputes
    except Exception as e:
        rows.add("gas_watch", "FAIL", "series unreadable (%s) %s"
                 % (type(e).__name__, str(e)[:90]))
        return
    if not series:
        rows.absent("gas_watch", "no readings collected yet")
        return
    # A gap and a run of unverified days are both WARN, never FAIL. CINGSA
    # keeps no archive, so a gap can never be repaired, and the collector
    # refuses to write a second record for a date it already holds. A FAIL
    # here would be unclearable and would block the merge of every future
    # carousel run over a gas outage that has nothing to do with the deck.
    # Data problems are surfaced, not used to hold editorial hostage.
    missing = gwb.continuity(series)
    verified = [r for r in series if r.get("verified")]
    if missing:
        rows.add("gas_watch", "WARN",
                 "%d day(s) on record, %d missing from the series, first %s"
                 % (len(series), len(missing), missing[0]))
        return
    if not verified:
        rows.add("gas_watch", "WARN", "%d day(s) on record, none verified" % len(series))
        return
    from datetime import date as _d
    age = (_d.today() - _d.fromisoformat(verified[-1]["date"])).days
    # The monthly EIA cross check is what keeps the model honest against
    # observed consumption, so a stale or absent one is worth seeing here.
    xc = ""
    try:
        figs = gwb.figures(series, model)
        if figs.get("eia_months_checked"):
            # The aggregate ratio used to go here, and it reads near zero by
            # construction now that the coefficients are fitted to these same
            # months. Mean monthly error is the figure that still moves when a
            # fit degrades, so that is the one worth surfacing.
            miss = figs.get("fit_mean_error_pct")
            xc = (", EIA through %s over %d months, %s"
                  % (figs["eia_latest_month"], figs["eia_months_checked"],
                     "model misses by %s%%" % miss if miss is not None
                     else "no fit error on file"))
        else:
            xc = ", no EIA cross check on file"
    except Exception as e:
        xc = ", EIA cross check unreadable (%s)" % type(e).__name__
    note = ("%d day(s) on record, %d verified, no gaps, latest %s%s"
            % (len(series), len(verified), verified[-1]["date"], xc))
    if age > 2:
        rows.add("gas_watch", "WARN", "%s, which is %d days old" % (note, age))
    else:
        rows.add("gas_watch", "PASS", note)


def site_fresh_row(rows, run):
    """Repo-level: proves the committed docs/ is byte-identical to what
    site_build.py makes from the data this run just committed. A stale page
    renders exactly as well as a fresh one, which is why both failures on
    2026-08-01 shipped unnoticed: a run whose deck was tagged to three beats
    committed a build crediting one, and a session rebuilt with a three-day-old
    --date and rolled the whole site backwards. The run dir is named for the
    date, so the gate needs no new argument. Exit non-zero is a FAIL."""
    script = REPO / "scripts" / "site_fresh_check.py"
    if not script.exists():
        rows.absent("site_fresh", "scripts/site_fresh_check.py missing")
        return
    date = run.name
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        rows.absent("site_fresh", "run dir %r is not a date, cannot pick --date" % date)
        return
    try:
        p = subprocess.run([sys.executable, str(script), "--date", date],
                           capture_output=True, text=True, timeout=600)
    except Exception as e:
        rows.add("site_fresh", "FAIL",
                 "could not run site_fresh_check (%s)" % type(e).__name__)
        return
    out = [ln for ln in (p.stdout + p.stderr).strip().splitlines()
           if ln.strip() and not ln.startswith("note:")] or [""]
    rows.add("site_fresh", "PASS" if p.returncode == 0 else "FAIL", out[-1 if p.returncode == 0 else 0][:140])


def assemble_row(rows, run, rep, fdir):
    asm, note = load_json(fdir / "assemble_report.json")
    if asm is None:
        rows.absent("assemble", "assemble_report.json %s" % note)
        return
    mode, mb, n = asm.get("pdf_mode", "?"), asm.get("pdf_mb", "?"), asm.get("slides", "?")
    detail = "%d slides, pdf %s %s MB, %d thumbs" % (
        n if isinstance(n, int) else -1, mode, mb, len(asm.get("thumbs") or []))
    status = "PASS"
    if rep is not None and isinstance(n, int) and n != len(rep.get("slides", [])):
        status = "FAIL"
        detail += " (slide count != render's %d)" % len(rep.get("slides", []))
    if isinstance(mb, (int, float)) and mb >= 90:
        status = "FAIL"
        detail += " (pdf over the 90 MB hard cap)"
    elif mode != "vector":
        status = "WARN"
        detail += " (raster fallback; note pdf_mode in the email)"
    # Resolve the PDF inside the run dir being inspected. assemble_report.json
    # records an absolute path from the machine that built it, which can point
    # at a different copy of the run (or at nothing after a move).
    pdf_name = Path(asm.get("pdf") or "carousel.pdf").name
    ok, bnote = pdf_ok(fdir / pdf_name)
    if not ok:
        status = "FAIL"
        detail += " (carousel.pdf %s)" % bnote
    rows.add("assemble", status, detail)


def score_row(rows, run):
    sc, note = load_json(run / "score_report.json")
    if sc is None:
        rows.absent("score", "score_report.json %s" % note)
        return
    # Report the scorer's own numbers. Never re-derive a verdict here.
    weighted = first(sc, "weighted_score_as_scored", "weighted_score", "weighted_total", default="?")
    # 2026-08-08: No.29's scorer wrote 'threshold_used', so the run record read
    # "8.02 / 10 vs threshold ?" over a genuine pass. Same alias list, same rule
    # as gmail_draft.py: extend it, never hand-write the row.
    thr = first(sc, "threshold_applied", "threshold", "ship_threshold",
                "threshold_used", "ship_threshold_used", default="?")
    passes = first(sc, "passes_as_scored", "passes", "ship", "ships")
    detail = "%s / 10 vs threshold %s, scorer says passes=%s" % (weighted, thr, passes)
    if sc.get("cap_reason"):
        detail += " (capped: %s)" % str(sc["cap_reason"])[:80]
    # A BELOW-THRESHOLD SCORE IS A FAIL ROW, NOT A WARN (2026-08-15). This row
    # was a WARN, and run No.34 read the warn as permission to write a
    # post-mortem, mail a DO NOT POST draft and end the run with a complete deck
    # sitting unshipped and a named, finite list of defects unfixed. A warn is
    # something a run may ship past; not shipping at all is not a warn.
    # scripts/ship_gate.py carries the full argument and the ladder rule.
    rows.add("score", "PASS" if passes else "FAIL", detail)


def ship_gate_row(rows, run):
    """Refuse the move that ended run No.34: stopping on a low score."""
    try:
        p = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "ship_gate.py"),
             "--run-dir", str(run), "--json"],
            capture_output=True, text=True, timeout=60)
        rep = json.loads(p.stdout)
    except Exception as e:
        rows.absent("ship_gate", "could not run (%s)" % type(e).__name__)
        return
    if rep.get("may_ship"):
        rows.add("ship_gate", "PASS", rep.get("reason", "may ship"))
    elif p.returncode == 2:
        rows.add("ship_gate", "WARN", rep.get("reason", "declared blocker"))
    else:
        rows.add("ship_gate", "FAIL",
                 "%s ITERATE, do not stop. weakest: %s"
                 % (rep.get("reason", ""), rep.get("weakest_criterion", "?")))


def artifacts_row(rows, run, rdir, rep):
    """Presence AND parseability of the artifact set, never a byte threshold."""
    bad = []
    for name in ("plan.md", "storyboard.md", "selection.md", "caption.txt"):
        p = run / name
        if not p.exists() or not p.read_text().strip():
            bad.append("%s missing or empty" % name)
    for name in ("claims.json", "copy.json", "caption_report.json", "run_state.json"):
        obj, note = load_json(run / name)
        if obj is None:
            bad.append("%s %s" % (name, note))
    if rep is not None:
        pngs = [(s.get("png", ""), rdir / s.get("png", "")) for s in rep.get("slides", [])]
    else:
        # flat runs/<date>/ has no render report; the slides sit beside the
        # other artifacts, so glob them rather than reporting a count of zero.
        # Both extensions, because ship_images.py converts the shipped copies
        # to WebP in Phase 11. The routine points this at out/<date>, which
        # keeps its PNGs, but a gate that silently counts zero slides when
        # aimed at runs/ is a trap worth not leaving lying around.
        pngs = [(p.name, p) for p in sorted(
            list(run.glob("slide-*.png")) + list(run.glob("slide-*.webp")))]
    for name, png in pngs:
        # WebP is RIFF....WEBP, PNG has its own signature. Check whichever
        # this file claims to be, so a truncated slide still fails.
        magic = b"RIFF" if str(name).endswith(".webp") else b"\x89PNG"
        ok, note = image_ok(png, magic)
        if not ok:
            bad.append("%s %s" % (name, note))
    n_png = len(pngs)
    if bad:
        rows.add("artifacts", "FAIL" if rows.require else "WARN",
                 "%d problem(s): %s" % (len(bad), "; ".join(bad[:4])))
    else:
        rows.add("artifacts", "PASS",
                 "every named artifact present, JSON parses, %d slides valid" % n_png)


BLOCK_HEAD = "GATE STATUS -- generated by scripts/gate_status.py"
ROW_RE = re.compile(r"^\s*\[\s*(PASS|WARN|FAIL|n/a)\s*\]\s+(\S+)\s+(.*)$")
TAIL_RE = re.compile(r"^\s*>>\s+\d+\s+FAIL row\(s\)\.")


def parse_pasted(text):
    """Pull the LAST pasted GATE STATUS block out of a markdown file and return
    it as {gate: (status, detail)}. Tolerates the indentation the run record
    uses to hold the block as a code block."""
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if BLOCK_HEAD in ln]
    if not starts:
        return None
    rows = {}
    for ln in lines[starts[-1] + 1:]:
        m = ROW_RE.match(ln)
        if m:
            rows[m.group(2)] = (m.group(1), m.group(3).strip())
        elif ">>" in ln and "FAIL row" in ln:
            break
        elif rows and not ln.strip():
            break
    return rows


def block_lines(run, rows):
    """The GATE STATUS block exactly as the human-readable mode prints it."""
    fails = [r for r in rows if r["status"] == "FAIL"]
    out = ["%s from the artifacts in %s. Do not hand-write these lines."
           % (BLOCK_HEAD, run)]
    for r in rows:
        out.append("[%-4s] %-14s %s" % (r["status"], r["gate"], r["detail"]))
    out.append(">> %d FAIL row(s). %s" % (
        len(fails),
        "Paste this block verbatim into the run record." if not fails
        else "Fix the artifact, not the sentence."))
    return out


def sync_block(path, run, rows):
    """WRITE the freshly generated block into the run record, in place of the
    one already there (2026-08-07).

    Why this exists. --verify-pasted (2026-08-05) made staleness a CHECK, and
    the instinct behind it was logged at 0.95 confidence -- and run No.28
    violated it twice in one run anyway: the block was pasted after the critic
    round, a third revision round ran under it, and the SCORER read a record
    claiming 29 qa warns and a missing score report on a deck measuring 20 that
    had scored; a later site rebuild then staled the site_fresh row the same
    way. An instinct at 0.99 that keeps being violated is a machine problem,
    not a discipline problem: the check ran only at the completion gate, which
    is after every reader who could be misled, and the refresh itself was a
    hand copy-paste, which is the one step a re-render cannot re-run for you.

    This makes the refresh a command. It is idempotent, it rewrites nothing when
    the record is already fresh, and it is cheap enough to run after every
    render round, before the scorer, and before the ship gate.

    Returns (changed, note). The block is located by its LAST head line and
    replaced through its trailing '>>' line, so surrounding prose and code
    fences are untouched. A file with no block at all gets one appended in a
    fenced section, so the first paste is not hand-work either.
    """
    p = Path(path)
    if not p.exists():
        return None, "%s does not exist" % p
    text = p.read_text()
    lines = text.splitlines()
    fresh = block_lines(run, rows)
    starts = [i for i, ln in enumerate(lines) if BLOCK_HEAD in ln]
    if not starts:
        tail = [] if text.endswith("\n\n") or not text else [""]
        new = lines + tail + ["## GATE STATUS, generated by scripts/gate_status.py --sync",
                              "", "```"] + fresh + ["```", ""]
        p.write_text("\n".join(new) + "\n")
        return True, "no block found; appended a fresh one (%d rows)" % len(rows)
    s = starts[-1]
    indent = lines[s][:len(lines[s]) - len(lines[s].lstrip())]
    e = s
    for i in range(s + 1, len(lines)):
        if ROW_RE.match(lines[i]):
            e = i
        elif TAIL_RE.match(lines[i]):
            e = i
            break
        else:
            break
    old = lines[s:e + 1]
    new_block = [indent + ln for ln in fresh]
    if old == new_block:
        return False, "already fresh (%d rows match the artifacts)" % len(rows)
    p.write_text("\n".join(lines[:s] + new_block + lines[e + 1:]) + "\n")
    return True, "rewrote %d line(s) as %d fresh row(s)" % (len(old), len(rows))


def verify_pasted(path, fresh_rows):
    """STALENESS GATE (2026-08-05). gate_status.py prints "Do not hand-write
    these lines" and the run record still went stale, because the block was
    pasted once and then four more render rounds happened under it. Run No.26
    shipped a block that contradicted the artifacts on four rows (the qa warn
    count, slide 09's percentage, the PDF size, and two artifacts it called
    missing that existed) plus an unresolved [FAIL] site_fresh row nothing ever
    addressed, and the only reviewer who caught it was the SCORER, at the ship
    gate. A generated block has to be regenerated at the LAST render, not the
    first, and that is a check, not a habit.

    Compares the pasted block against a freshly computed one, row by row, on
    BOTH status and detail. Exit 1 on any difference or on a pasted FAIL row.
    """
    p = Path(path)
    if not p.exists():
        print("[FAIL] pasted block: %s does not exist" % p)
        return 1
    pasted = parse_pasted(p.read_text())
    if pasted is None:
        print("[FAIL] pasted block: no '%s...' block found in %s" % (BLOCK_HEAD[:20], p))
        return 1
    fresh = {r["gate"]: (r["status"], r["detail"]) for r in fresh_rows}
    problems = []
    for gate in sorted(set(fresh) | set(pasted)):
        if gate not in pasted:
            problems.append("%-14s MISSING from the pasted block (fresh: [%s] %s)"
                            % (gate, fresh[gate][0], fresh[gate][1][:90]))
            continue
        if gate not in fresh:
            problems.append("%-14s in the pasted block but not generated now "
                            "(pasted: [%s])" % (gate, pasted[gate][0]))
            continue
        ps, pd = pasted[gate]
        fs, fd = fresh[gate]
        # The printed row truncates detail to the column width, so compare on
        # the prefix the block actually carries rather than demanding equality
        # with a longer fresh string.
        if ps != fs:
            problems.append("%-14s STALE status: pasted [%s], fresh [%s] -- %s"
                            % (gate, ps, fs, fd[:90]))
        elif pd and fd and not (fd.startswith(pd) or pd.startswith(fd)):
            problems.append("%-14s STALE detail:\n      pasted: %s\n      fresh:  %s"
                            % (gate, pd[:110], fd[:110]))
    stale_fails = [g for g, (s, _) in pasted.items() if s == "FAIL"]
    print("PASTED-BLOCK CHECK -- %s against a fresh generation" % p)
    for line in problems:
        print("  [STALE] " + line)
    for g in stale_fails:
        print("  [FAIL ] %-14s the pasted block carries an unresolved FAIL row"
              % g)
    if not problems and not stale_fails:
        print("  [PASS ] %d row(s) match the artifacts on disk, no FAIL rows"
              % len(pasted))
        return 0
    print(">> %d stale row(s), %d unresolved FAIL row(s). Regenerate the block "
          "at the LAST render and paste it again." % (len(problems), len(stale_fails)))
    return 1


SELF_TEST_ROWS = [
    {"gate": "render", "status": "PASS", "detail": "9/9 slides OK, 0 page errors"},
    {"gate": "qa.py", "status": "WARN", "detail": "WARN, 0 fails, 20 warns"},
    {"gate": "score", "status": "PASS", "detail": "8.55 / 10 vs threshold 8.0"},
]


def self_test():
    """Hermetic regression test for the block plumbing (no run dir, no network,
    no subprocesses). Covers exactly the failure this machinery exists for: a
    block written once, then made stale by a later round."""
    import io
    import contextlib
    import tempfile

    def verify(path, rows):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = verify_pasted(path, rows)
        return rc, buf.getvalue()

    fails, ran = [], []

    def check(name, cond, extra=""):
        ran.append(name)
        print("  [%s] %s%s" % ("ok  " if cond else "FAIL", name,
                               "" if cond else "  <- " + str(extra)))
        if not cond:
            fails.append(name)

    rows = [dict(r) for r in SELF_TEST_ROWS]
    stale = [dict(r) for r in SELF_TEST_ROWS]
    stale[1]["detail"] = "WARN, 0 fails, 29 warns"      # the No.28 stale row
    stale[2] = {"gate": "score", "status": "FAIL", "detail": "score_report.json missing"}

    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "2026-01-01"
        run.mkdir()
        doc = Path(td) / "storyboard.md"
        head = ["# STORYBOARD", "", "## SLIDE 01", "prose above the block", "", "```"]
        tail = ["```", "", "## SECOND REVISION ROUND", "prose below the block"]
        doc.write_text("\n".join(head + block_lines(run, stale) + tail) + "\n")

        rc, out = verify(doc, rows)
        check("a block staled by a later round is caught", rc == 1, out.strip()[:80])
        check("  and it names the stale rows", "qa.py" in out and "score" in out)

        changed, note = sync_block(doc, run, rows)
        check("--sync rewrites the stale block", changed is True, note)
        rc, _ = verify(doc, rows)
        check("  after which the record verifies", rc == 0)
        body = doc.read_text()
        check("  prose above and below survives",
              "prose above the block" in body and "prose below the block" in body)
        check("  the code fence survives", body.count("```") == 2)
        check("  exactly one block remains", body.count(BLOCK_HEAD) == 1)

        changed, note = sync_block(doc, run, rows)
        check("--sync is idempotent (no rewrite when fresh)", changed is False, note)

        rows2 = [dict(r) for r in rows]
        rows2[0]["detail"] = "9/9 slides OK, 1 page error"   # another render round
        rc, _ = verify(doc, rows2)
        check("a NEW round stales it again", rc == 1)
        sync_block(doc, run, rows2)
        rc, _ = verify(doc, rows2)
        check("  and --sync re-freshens it", rc == 0)

        indented = Path(td) / "indented.md"
        indented.write_text("\n".join(
            ["prose"] + ["    " + ln for ln in block_lines(run, stale)] + ["", "after"]) + "\n")
        sync_block(indented, run, rows)
        itxt = indented.read_text()
        check("indented blocks keep their indent",
              all(ln.startswith("    ") for ln in itxt.splitlines()
                  if ROW_RE.match(ln)))
        rc, _ = verify(indented, rows)
        check("  and verify clean", rc == 0)

        blank = Path(td) / "no_block.md"
        blank.write_text("# STORYBOARD\n\nno block here yet\n")
        changed, note = sync_block(blank, run, rows)
        check("a record with no block gets one appended", changed is True, note)
        rc, _ = verify(blank, rows)
        check("  and it verifies", rc == 0)

        failing = [dict(r) for r in rows]
        failing[0] = {"gate": "render", "status": "FAIL", "detail": "1 page error"}
        sync_block(doc, run, failing)
        rc, out = verify(doc, failing)
        check("an unresolved FAIL row still refuses to ship", rc == 1,
              out.strip()[:80])

        missing, note = sync_block(Path(td) / "nope.md", run, rows)
        check("a missing target is reported, not created", missing is None, note)

    print("SELF-TEST: %d check(s), %d failure(s)" % (len(ran), len(fails)))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir")
    ap.add_argument("--self-test", action="store_true",
                    help="hermetic regression test for the pasted-block "
                         "plumbing (no run dir needed)")
    ap.add_argument("--render-dir", default=None,
                    help="defaults to <run-dir>/render")
    ap.add_argument("--require", action="store_true",
                    help="ship gate: a missing or unparseable artifact is a FAIL")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--verify-pasted", default=None, metavar="MARKDOWN",
                    help="ship gate: re-generate the block and diff it against "
                         "the one pasted into this file (usually the run's "
                         "storyboard.md). Exit 1 if any row is stale or FAILs.")
    ap.add_argument("--sync", default=None, metavar="MARKDOWN",
                    help="WRITE the fresh block into this file, replacing the "
                         "block already there (appending one if there is none). "
                         "Idempotent; run it after every render round and before "
                         "the scorer, so no reader ever sees a stale record.")
    args = ap.parse_args()
    if args.self_test:
        sys.exit(self_test())
    if not args.run_dir:
        ap.error("--run-dir is required (or use --self-test)")
    if args.sync and args.verify_pasted:
        ap.error("--sync and --verify-pasted are opposites; run --sync to "
                 "refresh, --verify-pasted to check")

    run = Path(args.run_dir)
    # out/<date>/ nests render/ and final/; the shipped runs/<date>/ copy is
    # flat. Resolve both so the block can be regenerated from either.
    rdir = Path(args.render_dir) if args.render_dir else (
        run / "render" if (run / "render").is_dir() else run)
    fdir = run / "final" if (run / "final").is_dir() else run
    rows = Rows(args.require)
    rep = render_row(rows, rdir)
    qa_row(rows, rdir)
    dossier_row(rows, run)
    caption_row(rows, run)
    copy_sync_row(rows, run, rdir)
    aggregate_row(rows, run, rdir)
    plan_drift_row(rows, run, rdir)
    bespoke_row(rows, run)
    scanner_sync_row(rows)
    docket_dates_row(rows)
    gas_watch_row(rows)
    site_fresh_row(rows, run)
    assemble_row(rows, run, rep, fdir)
    score_row(rows, run)
    ship_gate_row(rows, run)
    artifacts_row(rows, run, rdir, rep)

    fails = [r for r in rows.rows if r["status"] == "FAIL"]
    if args.verify_pasted:
        rc = verify_pasted(args.verify_pasted, rows.rows)
        sys.exit(1 if (rc or fails) else 0)
    if args.sync:
        changed, note = sync_block(args.sync, run, rows.rows)
        if changed is None:
            print("[FAIL] sync: %s" % note)
            sys.exit(1)
        print("BLOCK SYNC -- %s: %s" % (args.sync, note))
        for r in rows.rows:
            print("[%-4s] %-14s %s" % (r["status"], r["gate"], r["detail"]))
        print(">> %d FAIL row(s). %s" % (
            len(fails), "Record is now fresh." if not fails
            else "Fix the artifact, not the sentence."))
        sys.exit(1 if fails else 0)
    if args.json:
        print(json.dumps({"run_dir": str(run), "rows": rows.rows,
                          "fails": len(fails)}, indent=2))
    else:
        for ln in block_lines(run, rows.rows):
            print(ln)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
