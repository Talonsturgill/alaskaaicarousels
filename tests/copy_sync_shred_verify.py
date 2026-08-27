#!/usr/bin/env python3
"""Can copy_sync_check see a TRUNCATED or a SHREDDED string? (2026-08-27)

Run No.42 built copy.json out of render_report twice and lost both ways, and
this gate passed both times:

  TRUNCATED. `text` is the element's whole string cut at 80 characters. Four
  bodies were pasted in at the cut. A truncated string IS present in the
  render, so a presence check can never see it.

  SHREDDED. `texts` is the element's DIRECT text children, so a <span> holding
  a unit is not in it. "1 DOT = 0.1 g OF SILVER IODIDE (C05)" came back as
  "1 DOT = 0.1 OF SILVER IODIDE (C05)", the gram gone. The old matcher joined
  every entry of `texts` into one per-slide blob, so the shredded string
  matched the join of the very entries it was built from.

Both fixtures below are the real strings, taken off this run's own render.
The PRE-FIX matcher is reconstructed here (the blob join, verbatim from the
old build_blobs) so the red cases are proved red rather than asserted, and the
last two checks prove the fix costs nothing: a <br>-separated body still
matches through `full`, and a shipped run's archived copy/render pair, written
before `full` existed, still passes.

    python3 tests/copy_sync_shred_verify.py

Exit 0 HOLDS, exit 1 BROKEN.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import copy_sync_check as cs  # noqa: E402

WHOLE_LABEL = "1 DOT = 0.1 g OF SILVER IODIDE (C05)"
SHREDDED = "1 DOT = 0.1 OF SILVER IODIDE (C05)"
WHOLE_BODY = ("The company says its software picks the seeding window, and the "
              "operations log records nineteen flares between 06:38 and 09:12 "
              "UTC on August 22nd.")
TRUNCATED = WHOLE_BODY[:80]


def node(full, texts):
    return {"full": full, "text": full[:80], "texts": texts,
            "x": 0, "y": 0, "w": 100, "h": 20}


def report(nodes):
    return {"slides": [{"file": "slide-03.html", "text_nodes": nodes}]}


def old_matcher(copy, rr, window=cs.WINDOW):
    """The pre-fix check, reconstructed: one alnum blob per slide, built by
    joining `text` and every entry of `texts` with a space."""
    per_slide, deck = {}, []
    for s in rr["slides"]:
        idx = cs.slide_index(s["file"])
        parts = []
        for n in s["text_nodes"]:
            parts.append(n.get("text", ""))
            parts.extend(n.get("texts", []) or [])
        blob = cs.alnum(" ".join(parts))
        per_slide["S%d" % idx] = blob
        deck.append(blob)
    deck = "".join(deck)
    misses = []
    for skey, sval in cs.normalize_slides(copy["slides"]).items():
        blob = per_slide.get(skey, "")
        for path, s in cs.collect(sval, ""):
            a = cs.alnum(s)
            if not a:
                continue
            needle = a if len(a) <= window else a[:window]
            if needle not in blob and needle not in deck:
                misses.append((skey, path, s))
    return misses


def main():
    fails = []

    # --- 1. THE SHREDDED LABEL -------------------------------------------
    rr = report([node(WHOLE_LABEL, ["1 DOT = 0.1", "OF SILVER IODIDE (C05)"])])
    copy = {"slides": [{"n": 3, "labels": [SHREDDED]}]}
    if old_matcher(copy, rr):
        fails.append("the reconstructed pre-fix matcher REJECTS the shredded "
                     "label, so this test is no longer reproducing the defect")
    checked, misses, _, _, trunc = cs.check(copy, rr)
    if not misses:
        print("BROKEN: the shredded label still passes")
        fails.append("shredded label passes")
    else:
        print("RED CASE HELD: %r is reported missing (the render's element "
              "says %r)" % (SHREDDED, WHOLE_LABEL))

    # --- 2. THE 80-CHARACTER PASTE ---------------------------------------
    rr = report([node(WHOLE_BODY, [WHOLE_BODY])])
    copy = {"slides": [{"n": 3, "body": TRUNCATED}]}
    if old_matcher(copy, rr):
        fails.append("the reconstructed pre-fix matcher REJECTS the truncated "
                     "body, so this test is no longer reproducing the defect")
    checked, misses, _, _, trunc = cs.check(copy, rr)
    if misses:
        fails.append("the truncated body is reported as MISSING; it is present, "
                     "and reporting it as absent would send the run looking for "
                     "the wrong defect")
    if not trunc:
        print("BROKEN: the 80-character paste still passes")
        fails.append("truncated body passes")
    else:
        print("RED CASE HELD: %d-char paste reported, the element carries "
              "%d chars" % (len(TRUNCATED), len(WHOLE_BODY)))

    # --- 3. THE SAME COPY, WRITTEN WHOLE ---------------------------------
    rr = report([node(WHOLE_LABEL, ["1 DOT = 0.1", "OF SILVER IODIDE (C05)"]),
                 node(WHOLE_BODY, [WHOLE_BODY])])
    copy = {"slides": [{"n": 3, "labels": [WHOLE_LABEL], "body": WHOLE_BODY}]}
    checked, misses, _, _, trunc = cs.check(copy, rr)
    if misses or trunc or checked != 2:
        fails.append("correct copy does not pass: checked=%d misses=%s trunc=%s"
                     % (checked, misses, trunc))
    else:
        print("GREEN: the same two strings, written whole, pass")

    # --- 4. A <br> BODY STILL MATCHES (2026-08-16 stays fixed) -----------
    lines = ["Nineteen flares burned.", "The log names each one.",
             "One number reached the reader."]
    rr = report([node(" ".join(lines), lines)])
    copy = {"slides": [{"n": 3, "body": " ".join(lines)}]}
    checked, misses, _, _, trunc = cs.check(copy, rr)
    if misses or trunc:
        fails.append("a multi-line block authored as one string no longer "
                     "matches: %s %s" % (misses, trunc))
    else:
        print("GREEN: a <br>-separated block authored as one string still matches")

    # --- 5. A SHIPPED RUN, ARCHIVED BEFORE `full` EXISTED ----------------
    c = ROOT / "runs" / "2026-08-12" / "copy.json"
    r = ROOT / "runs" / "2026-08-12" / "render_report.json"
    if c.exists() and r.exists():
        checked, misses, _, _, trunc = cs.check(json.loads(c.read_text()),
                                                json.loads(r.read_text()))
        if misses or trunc or checked == 0:
            fails.append("shipped run 2026-08-12 no longer passes: checked=%d "
                         "misses=%d trunc=%d" % (checked, len(misses), len(trunc)))
        else:
            print("GREEN: shipped run 2026-08-12, %d strings, no report on a "
                  "render made before `full` existed" % checked)
    else:
        print("note: runs/2026-08-12 artifacts absent, false-positive check skipped")

    if fails:
        print("\nBROKEN")
        for f in fails:
            print("  -", f)
        return 1
    print("\nHOLDS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
