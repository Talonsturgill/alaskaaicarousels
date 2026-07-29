#!/usr/bin/env python3
"""dossier_check.py -- the PLANNING-time half of the dead-lower-zone fix.

Why this exists (2026-07-26). "Dead lower zones" was named by the scorer in
six consecutive scored runs (ledger entries 10, 11, 13, 14, 15, 16, 18) and
never fixed, and the reason is a sequencing problem, not a taste problem:

  - DESIGN_DOCTRINE 1 required "at least one generous quiet zone per slide"
    with no ceiling and no address. The cheapest place to spend that licence
    is the bottom band of a top-loaded composition.
  - The dossier then WROTE that empty bottom into the plan.
  - The pixel critics grade each slide against its OWN dossier, so a slide
    that executed a bad plan passes its acceptance checklist.
  - The only reviewer positioned to see it was the scorer, at the ship gate,
    with no budget left to rebuild four slides. So every run it became a
    FIELD_NOTES sentence instead of a fix.

qa.py's frame_balance() now catches the defect in the RENDER, which is much
earlier. This catches it in the PLAN, which is earlier still and where the fix
costs one paragraph. It reads out/<date>/storyboard.md and requires every slide
dossier to carry SLIDE_DOSSIER_SPEC field 4a, the lower-third treatment, and to
name something with modeled tone in it rather than flat furniture.

Also cross-checks the breather escape hatch in both directions, so
`data-breather` can only ever RATIFY a declared plan and never invent one:
a slide whose body carries the attribute must be declared a breather in its
dossier, and a dossier that declares a breather must carry the attribute.

Usage:
  python scripts/dossier_check.py --run-dir out/2026-07-26
  python scripts/dossier_check.py --run-dir out/2026-07-26 --json

Read-only. Stdlib only. Exit 0 clean, 1 on any FAIL.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Field 4a satisfied only by naming something with modeled tone. Flat furniture
# is the defect wearing a costume, so plates/rules/captions do not clear it.
MODELED_HINTS = (
    "anchor", "terrain", "ground", "gradient", "graded", "foreground",
    "relief", "hillshade", "fog", "haze", "atmosphere", "shadow", "light",
    "lit", "texture", "grain", "stipple", "dither", "contour", "field",
    "particle", "mesh", "extrud", "depth", "render", "3d", "volumetric",
    "ramp", "wash", "glow", "mass", "silhouette", "topograph", "noise",
    "leader line", "annotation furniture", "scale bar", "tick",
)
FLAT_ONLY = ("plate", "hairline", "rule", "caption", "footer", "fixture",
             "label", "counter", "chip")

# Minimum length of a field-4a plan, in characters. Raised from 25 to 200 on
# 2026-07-29 together with the continuation-walk repair: 25 was a floor for one
# LINE, and applying it to the whole field would have been a loosening. Every
# field-4a paragraph written since the field existed runs 400 to 900 characters,
# so 200 is well clear of real practice and still refuses a one-sentence
# gesture at the bottom band.
THIN_PLAN_CHARS = 200

HEAD_RE = re.compile(r"^##\s+SLIDE\s+(\d+)\b(.*)$", re.I | re.M)
F4A_RE = re.compile(
    r"^\s*4a[.)]?\s*\*{0,2}\s*Lower[- ]third treatment\s*[.:-]?\s*\*{0,2}\s*[.:-]?\s*(.*)$",
    re.I | re.M)


def slide_sections(text):
    """Split the storyboard into (slide_no, heading, body) dossier sections."""
    heads = list(HEAD_RE.finditer(text))
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out.append((int(m.group(1)), m.group(2).strip(), text[m.end():end]))
    return out


def field_4a(body):
    """Return (whole_field, first_line) for field 4a, or (None, None).

    The continuation walk was broken from the day it shipped (fixed 2026-07-29).
    `m.end()` sits at the END of the matched 4a line, so the slice begins with a
    newline and `splitlines()[0]` is the empty string, which tripped the blank-
    line guard on the very first iteration: the gate read only the field's FIRST
    LINE and was blind to the rest. Measured on run 2026-07-29's storyboard, it
    saw 45 to 183 characters of nine fields that run 400 to 900, and two
    dossiers cleared it on a 45-character fragment. It also distorted the
    authoring: all nine fields were rewritten to LEAD with modeled-tone words to
    satisfy it, leaving dangling markdown mid-sentence.

    Continuation stops at a blank line or at the next field marker, so a field
    is the paragraph the author actually wrote.
    """
    m = F4A_RE.search(body)
    if not m:
        return None, None
    first = m.group(1).strip()
    lines = [first]
    rest = body[m.end():]
    if rest.startswith("\n"):
        rest = rest[1:]
    elif rest.startswith("\r\n"):
        rest = rest[2:]
    for line in rest.splitlines():
        s = line.strip()
        if not s or re.match(r"^\s*(\d+[a-z]?[.)]|[A-Z]\.\s|#|-\s*\[)", line):
            break
        lines.append(s)
    return " ".join(x for x in lines if x).strip(), first


def check_slide(no, heading, body, breather_attr):
    fails, warns = [], []
    declared_breather = False
    text, first = field_4a(body)
    if not text:
        fails.append(
            f"slide {no:02d}: no field 4a (lower-third treatment). "
            "SLIDE_DOSSIER_SPEC requires every dossier to name what the bottom "
            "band carries; an unnamed lower third is how six runs shipped dead ones")
    else:
        low = text.lower()
        # The BREATHER escape hatch is read from the FIRST line and the heading
        # only, deliberately. Now that the whole field is visible, matching
        # "breather" anywhere in a 900-character paragraph would let an
        # incidental mention skip the modeled-tone requirement, which would
        # widen the hatch. Declaring a breather stays a headline act.
        declared_breather = "breather" in (first or "").lower() or "breather" in heading.lower()
        if declared_breather:
            if len(re.sub(r"[^a-z]", "", low.split("breather", 1)[-1])) < 12:
                fails.append(
                    f"slide {no:02d}: declared BREATHER with no reason given. "
                    "The spec requires 'BREATHER -- <why the deck needs a rest here>'")
        elif len(low) < THIN_PLAN_CHARS:
            fails.append(
                f"slide {no:02d}: field 4a is too thin to be a plan "
                f"({len(low)} chars, floor {THIN_PLAN_CHARS}) -- {text!r}")
        elif not any(h in low for h in MODELED_HINTS):
            named_flat = [f for f in FLAT_ONLY if f in low]
            fails.append(
                f"slide {no:02d}: field 4a names nothing with modeled tone"
                + (f" (only flat furniture: {', '.join(named_flat)})" if named_flat else "")
                + f" -- {text[:90]!r}. Extend the anchor, run the annotation "
                  "furniture down, add a foreground plane or a graded ground; a "
                  "plate floating on bare ground is the same defect wearing furniture")

    if breather_attr is not None:
        if breather_attr and not declared_breather:
            fails.append(
                f"slide {no:02d}: slide body sets data-breather but the dossier does "
                "not declare it a breather. The attribute ratifies a plan, it does "
                "not create one")
        elif declared_breather and not breather_attr:
            warns.append(
                f"slide {no:02d}: dossier declares a BREATHER but the slide body has "
                "no data-breather, so qa.py will FAIL it on frame balance")
    return fails, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rdir = Path(args.run_dir)
    sb = rdir / "storyboard.md"
    if not sb.exists():
        print(f"FAIL: {sb} missing")
        sys.exit(1)
    sections = slide_sections(sb.read_text())
    if not sections:
        print(f"FAIL: no '## SLIDE NN' dossiers found in {sb}")
        sys.exit(1)

    # slide sources are optional: this gate is meant to run BEFORE they exist
    sdir = rdir / "slides"
    attrs = {}
    if sdir.is_dir():
        for p in sdir.glob("slide-*.html"):
            m = re.search(r"slide-(\d+)", p.name)
            if m:
                src = p.read_text(errors="replace")
                b = re.search(r"<body\b[^>]*>", src, re.I)
                attrs[int(m.group(1))] = bool(b and "data-breather" in b.group(0))

    out = {"slides": [], "fails": 0, "warns": 0}
    for no, heading, body in sections:
        f, w = check_slide(no, heading, body, attrs.get(no))
        out["slides"].append({"slide": no, "fails": f, "warns": w})
        out["fails"] += len(f)
        out["warns"] += len(w)
    out["verdict"] = "FAIL" if out["fails"] else ("WARN" if out["warns"] else "PASS")

    if args.json:
        print(json.dumps(out, indent=2))
    else:
        for s in out["slides"]:
            flag = "FAIL" if s["fails"] else ("warn" if s["warns"] else "ok  ")
            print(f"[{flag}] slide {s['slide']:02d}")
            for x in s["fails"]:
                print(f"    FAIL: {x}")
            for x in s["warns"]:
                print(f"    warn: {x}")
        print(f"verdict: {out['verdict']}  ({len(sections)} dossiers, "
              f"{out['fails']} fails, {out['warns']} warns)")
    sys.exit(1 if out["fails"] else 0)


if __name__ == "__main__":
    main()
