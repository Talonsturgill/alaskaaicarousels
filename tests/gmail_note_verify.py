#!/usr/bin/env python3
"""Prove gmail_draft.py renders the editor note as prose, not as a Python repr.

WHY THIS EXISTS
    Run No.42 (2026-08-27) shipped a draft whose Editor's note section read:

      ["The argument is that one operation produced three published widths of
      the same figure...", 'The deck never says 19 million gallons of rain
      fell...']

    brackets, quotes and commas included. `_note_from` ended in `str(v)`, and
    both the scorer's report and the copywriter's copy.json carry
    `editor_notes_for_email` as an ARRAY of sentences, which is the shape their
    own briefs ask for. `str()` on a list is its repr.

    Nothing downstream looks at this section, and it is the one part of the
    email the maintainer reads before deciding whether to post, so the only
    thing that can catch it is a test that reads the rendered bytes.

    This is the same defect class as the five field-spelling bugs the function
    already carries comments about, one layer down: there the agent's field
    NAME drifted from the reader's, here its VALUE SHAPE did.

WHAT IT CHECKS
    1. RED CASE, the exact No.42 payload. A list-valued note must not put a
       bracket, a Python quote or a repr comma into the body, and each sentence
       must appear as its own <li>.
    2. The string form still works, and its newlines still become <br>.
    3. Both sources are still read and printed in order (scorer first), which
       is what the 2026-08-07 fix bought.
    4. An empty note still renders "None." and not "[]".
    5. The real shipped artifacts for a run render clean, so the check is run
       against something that actually exists rather than only against
       fixtures.

USAGE
    python3 tests/gmail_note_verify.py                 # fixtures + latest run
    python3 tests/gmail_note_verify.py --run 2026-08-27

Exit 0 = HOLDS, 1 = a defect is present.
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_gmail_draft():
    spec = importlib.util.spec_from_file_location(
        "gmail_draft", ROOT / "scripts" / "gmail_draft.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def render_notes(mod, score, copy):
    """Re-run just the note block the way build_html does, off the real code."""
    esc = mod.html.escape

    def _note_from(src):
        for k in ("editor_notes_for_email", "notes_for_the_email",
                  "notes_for_email", "editor_note",
                  "shortfall_note_for_email", "shortfall_note",
                  "honest_note_for_the_email", "honest_note"):
            v = src.get(k)
            if v is None or v == "":
                continue
            if isinstance(v, (list, tuple)):
                items = [str(x).strip() for x in v if str(x).strip()]
                if items:
                    return items
                continue
            s = str(v).strip()
            if s:
                return s
        return None

    src = (ROOT / "scripts" / "gmail_draft.py").read_text()
    if "_note_html" not in src:
        raise AssertionError(
            "gmail_draft.py has no _note_html: the list-shaped editor note is "
            "being rendered with str(), which is the 2026-08-27 defect.")

    def _note_html(v):
        if isinstance(v, list):
            return ('<ul class="check">'
                    + "".join("<li>%s</li>" % esc(x).replace("\n", "<br>")
                              for x in v)
                    + "</ul>")
        return esc(v).replace("\n", "<br>")

    parts = [p for p in (_note_from(score), _note_from(copy)) if p]
    return "<br>".join(_note_html(p) for p in parts) or "None."


REPR_MARKS = [
    ("[&quot;", "an HTML-escaped opening bracket and quote"),
    ("[&#x27;", "an HTML-escaped opening bracket and apostrophe"),
    ("&quot;, &quot;", "a repr comma between two double-quoted items"),
    ("&#x27;, &#x27;", "a repr comma between two single-quoted items"),
    ("&#x27;]", "an HTML-escaped closing apostrophe and bracket"),
    ("&quot;]", "an HTML-escaped closing quote and bracket"),
]


def assert_no_repr(html, where, fails):
    for mark, why in REPR_MARKS:
        if mark in html:
            fails.append("%s: rendered %s, so the note is a Python repr: %s"
                         % (where, why, html[:160]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=None)
    args = ap.parse_args()
    mod = load_gmail_draft()
    fails, checks = [], 0

    # 1. RED CASE: the exact No.42 shape.
    n42 = [
        "The argument is that one operation produced three published widths of "
        "the same figure, and each retelling was narrower than the last.",
        "The deck never says 19 million gallons of rain fell. Slide 07 labels "
        "that figure as a headline and converts it to 58.31 acre feet.",
        "No client, contract or motive appears anywhere.",
    ]
    html = render_notes(mod, {"editor_notes_for_email": n42}, {})
    assert_no_repr(html, "list-valued note", fails)
    checks += 1
    if html.count("<li>") != 3:
        fails.append("list-valued note: expected 3 <li>, got %d"
                     % html.count("<li>"))
    checks += 1
    for s in n42:
        head = mod.html.escape(s)[:40]
        if head not in html:
            fails.append("list-valued note: lost a sentence starting %r" % head)
    checks += 1

    # 2. The string form still renders, and keeps its line breaks.
    html = render_notes(mod, {"editor_note": "One line.\nTwo line."}, {})
    if "<li>" in html:
        fails.append("string note was wrapped in a list")
    if "One line.<br>Two line." not in html:
        fails.append("string note lost its newline-to-<br>: %r" % html)
    assert_no_repr(html, "string note", fails)
    checks += 1

    # 3. Both sources, scorer first (the 2026-08-07 fix).
    html = render_notes(mod, {"editor_note": "SCORER SAYS"},
                        {"editor_notes_for_email": ["COPY SAYS"]})
    if not ("SCORER SAYS" in html and "COPY SAYS" in html):
        fails.append("a source was dropped: %r" % html)
    elif html.index("SCORER SAYS") > html.index("COPY SAYS"):
        fails.append("copy note printed before the scorer note")
    checks += 1

    # 4. Empty stays "None.", never "[]".
    for empty in ({}, {"editor_notes_for_email": []},
                  {"editor_notes_for_email": ["", "  "]}):
        html = render_notes(mod, empty, {})
        if html != "None.":
            fails.append("empty note rendered %r, expected 'None.'" % html)
    checks += 1

    # 5. The real artifacts of a shipped run.
    runs = sorted(p for p in (ROOT / "runs").iterdir()
                  if p.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name))
    targets = [ROOT / "runs" / args.run] if args.run else runs[-3:]
    for rd in targets:
        sc, cp = rd / "score_report.json", rd / "copy.json"
        if not (sc.exists() and cp.exists()):
            continue
        html = render_notes(mod, json.loads(sc.read_text()),
                            json.loads(cp.read_text()))
        assert_no_repr(html, "shipped run %s" % rd.name, fails)
        if html == "None.":
            fails.append("shipped run %s: the editor note rendered 'None.'"
                         % rd.name)
        checks += 1

    # 6. END TO END, off the real script. Steps 1 to 5 re-run the note block,
    #    so they would still pass if build_html rendered it some other way.
    #    This runs gmail_draft.py for real and reads the section it produced.
    #    gmail_draft expects the out/<date> shape (render/, final/), not the
    #    flat runs/<date> one, so the fixture is assembled from a shipped run.
    e2e = args.run or (targets[-1].name if targets else None)
    src = ROOT / "runs" / (e2e or "")
    if e2e and (src / "copy.json").exists() and (src / "assemble_report.json").exists():
        import shutil
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            rd = Path(td) / e2e
            (rd / "render").mkdir(parents=True)
            (rd / "final").mkdir(parents=True)
            for f in ("copy.json", "score_report.json"):
                if (src / f).exists():
                    shutil.copy(src / f, rd / f)
            shutil.copy(src / "assemble_report.json", rd / "final" / "assemble_report.json")
            if (src / "carousel.pdf").exists():
                shutil.copy(src / "carousel.pdf", rd / "final" / "carousel.pdf")
            out = Path(td) / "payload.json"
            r = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "gmail_draft.py"),
                 "--run-dir", str(rd), "--run-date", e2e,
                 "--carousel-no", "0", "--preview-mode", "remote",
                 "--branch", "test", "--raw-base", "https://example.invalid",
                 "--payload-out", str(out)],
                capture_output=True, text=True, cwd=str(ROOT))
            if r.returncode != 0:
                fails.append("end to end: gmail_draft.py exited %d: %s"
                             % (r.returncode, (r.stderr or "")[-300:]))
            else:
                body = json.loads(out.read_text())["html_body"]
                m = re.search(r"Editor(?:&#x27;|\')s note</h2>\s*(.*?)\s*<h2",
                              body, re.S)
                if not m:
                    fails.append("end to end: no Editor's note section in the "
                                 "rendered body")
                else:
                    sec = m.group(1)
                    assert_no_repr(sec, "end to end (%s)" % e2e, fails)
                    if "None." in sec:
                        fails.append("end to end (%s): note rendered 'None.'"
                                     % e2e)
                    elif "<li>" not in sec:
                        fails.append("end to end (%s): a list note rendered "
                                     "without bullets" % e2e)
        checks += 1

    if fails:
        print("gmail_note_verify: DEFECT (%d)" % len(fails))
        for f in fails:
            print("  " + f)
        return 1
    print("gmail_note_verify: HOLDS (%d checks, runs: %s)"
          % (checks, ", ".join(p.name for p in targets) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
