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
    verdict = qa.get("verdict", "?")
    detail = "%s, %s fails, %s warns" % (verdict, qa.get("fails", "?"), qa.get("warns", "?"))
    named = [s["file"] for s in qa.get("slides", []) if s.get("fails")]
    if named:
        detail += " (fails on %s)" % ", ".join(named)
    status = "FAIL" if qa.get("fails") else ("WARN" if qa.get("warns") else "PASS")
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
        rows.add("copy_sync", "n/a", "could not run copy_sync_check (%s)" % type(e).__name__)
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
    ok, bnote = binary_ok(fdir / pdf_name, b"%PDF")
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
        ok, note = binary_ok(png, magic)
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
