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

Usage:
  python scripts/gate_status.py --run-dir out/2026-07-25
  python scripts/gate_status.py --run-dir out/2026-07-25 --require   # ship gate
  python scripts/gate_status.py --run-dir out/2026-07-25 --json

Read-only. Stdlib only. Exit 0 when no gate row is FAIL (WARN rows are fine),
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
    thr = first(sc, "threshold_applied", "threshold", "ship_threshold", default="?")
    passes = first(sc, "passes_as_scored", "passes", "ship", "ships")
    detail = "%s / 10 vs threshold %s, scorer says passes=%s" % (weighted, thr, passes)
    if sc.get("cap_reason"):
        detail += " (capped: %s)" % str(sc["cap_reason"])[:80]
    rows.add("score", "PASS" if passes else "WARN", detail)


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--render-dir", default=None,
                    help="defaults to <run-dir>/render")
    ap.add_argument("--require", action="store_true",
                    help="ship gate: a missing or unparseable artifact is a FAIL")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

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
    scanner_sync_row(rows)
    docket_dates_row(rows)
    site_fresh_row(rows, run)
    assemble_row(rows, run, rep, fdir)
    score_row(rows, run)
    artifacts_row(rows, run, rdir, rep)

    fails = [r for r in rows.rows if r["status"] == "FAIL"]
    if args.json:
        print(json.dumps({"run_dir": str(run), "rows": rows.rows,
                          "fails": len(fails)}, indent=2))
    else:
        print("GATE STATUS -- generated by scripts/gate_status.py from the artifacts "
              "in %s. Do not hand-write these lines." % run)
        for r in rows.rows:
            print("[%-4s] %-14s %s" % (r["status"], r["gate"], r["detail"]))
        print(">> %d FAIL row(s). %s" % (
            len(fails),
            "Paste this block verbatim into the run record." if not fails
            else "Fix the artifact, not the sentence."))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
