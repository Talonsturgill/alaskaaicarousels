#!/usr/bin/env python3
"""bespoke_check.py -- prove the deck's art is written per slide, not templated.

WHY THIS EXISTS (2026-08-05, maintainer).

    "your artwork craft is regressing, you are now making each slide with the
     same template instead of custom coding every single one one by one, cause
     that's our whole strength, humans can't do that as much as you"

CLAUDE.md and the engine's SKILL.md have both said "the engine is a HARNESS,
not a template, every deck's art is bespoke code written per run" since the
beginning. Nothing measured it, so on 2026-08-05 run No.26 shipped nine slides
generated from one build script in which every frame called the same six
drawing functions with different arguments, and the run wrote a justification
for it into its own artifact ("this is not a template either, it is this deck's
own build, written once"). That sentence is what a regression sounds like when
it is allowed to grade itself.

The evidence was already in the run and was filed as a composition note instead
of as the structural defect it was. The scorer said five of nine frames read as
the same picture. A pixel critic called slide 06 a broken render. Measured
afterwards, the deck's median pairwise art-code similarity was 0.966, against
0.049 for examples/demo-deck, which is four genuinely bespoke slides. One pair
was byte-identical.

WHAT IS MEASURED, and what is deliberately NOT.

This gate does not ban a build script. A generator is a fine tool and the
question is never how the HTML got written, it is whether the nine slides
actually contain nine different pieces of art. So it measures the OUTCOME:
pairwise similarity of each slide's own drawing code, with the shared harness
(font links, library tags, the counter and footer fixtures) stripped first, so
a deck is never punished for using the house furniture.

THRESHOLDS, fitted against the two real decks above rather than guessed:

    examples/demo-deck, bespoke      median 0.049
    run 2026-08-05, generator-built  median 0.966, one pair at 1.000

FAIL_MEDIAN is set at 0.60, an enormous margin above the bespoke reference and
far below the templated one, so a deck that legitimately revisits one object
across nine frames still has room to pass while a deck that is one function
called nine times cannot. FAIL_PAIR catches the other shape of the same defect,
two slides whose art is effectively the same code even when the deck's median
looks acceptable.

Usage:
    python scripts/bespoke_check.py --slides-dir out/2026-08-05/slides
    python scripts/bespoke_check.py --slides-dir ... --json

Read-only. Stdlib only. Exit 0 clean, 1 on any FAIL, 2 if it cannot look.
"""
from __future__ import annotations

import argparse
import difflib
import itertools
import json
import re
import statistics
import sys
from pathlib import Path

FAIL_MEDIAN = 0.60      # median pairwise similarity of per-slide art code
WARN_MEDIAN = 0.35
FAIL_PAIR = 0.95        # any single pair this alike is the same slide twice

# THE SECOND DIMENSION (2026-08-05, same maintainer report):
#
#   "ur artwork on the last two seems like blocky, almost like a kid was drag
#    and dropping shapes into the slides, as opposed to before when you made
#    them from scratch and custom to the stories"
#
# Also literally true and also measurable. Run No.26's nine slides make 126
# axis-aligned rectangle calls against 37 marks that are drawn, sampled or
# generated. examples/demo-deck makes 2 against 9. A deck built out of
# fillRect with a gradient in it is a deck of boxes however good the palette
# is, and the technique library's whole bench (flow fields, contours, stipple,
# hachure, relief, raymarch, PBR) sat unused while this shipped.
#
# Rectangles are not banned. Knockout plates are rectangles and are required,
# and a parallel-projection bar chart is rectangles by doctrine. Those are DOM
# and SVG here, so they are not counted; only canvas drawing code is read.
BLOCKY = ("fillRect", "strokeRect", "rect(")
DRAWN = ("bezierCurveTo", "quadraticCurveTo", "arc(", "arcTo",
         "createRadialGradient", "putImageData", "getImageData",
         "fbm2", "simplex2", "simplex3", "warp2", "reliefShade",
         "AKSDF", "AKT.", "d3.contours", "d3.geoPath", "hachure",
         "stipple", "contour", "setTransform", "clip(")
FAIL_DRAWN_SHARE = 0.45   # demo-deck 0.82, run 2026-08-05 0.23
WARN_DRAWN_SHARE = 0.60

# Stripped before comparing, so the house harness never counts as sameness.
HARNESS = (
    re.compile(r"<link[^>]*>"),
    re.compile(r'<script src="[^"]*"></script>'),
    re.compile(r"<style>.*?</style>", re.S),
    re.compile(r'<div class="abs mon counter">[^<]*</div>'),
    re.compile(r'<div class="abs mon foot"[^>]*>[^<]*</div>'),
    re.compile(r"AKPOST\.grade\(.*?\}\);", re.S),
    re.compile(r"AK\.grainTile\([^)]*\)"),
)


def art_code(path: Path) -> str:
    """A slide's own drawing code: inline scripts plus positioned markup,
    with the shared harness removed and whitespace flattened."""
    h = path.read_text()
    for rx in HARNESS:
        h = rx.sub(" ", h)
    # A SLIDE'S ART CODE CAN LIVE IN A MODULE SCRIPT (2026-08-15). The pattern
    # was `<script>` with no attributes, so every slide that loads akthree, and
    # therefore every deck that climbs to rung 1 of the rendered ladder, matched
    # ZERO inline script and was compared on its <div> list alone. Such a deck
    # measured 0.810 median with drawn share 0 percent and 0 drawn marks against
    # 0 blocky ones, which is the signature of a checker that cannot see rather
    # than of a deck that is templated. The engine's own SKILL.md requires
    # `<script type="module">` for akthree, so the gate was blind to the exact
    # decks it most needed to read. Attribute-tolerant, and src-only tags are
    # still stripped by HARNESS above, so a vendored library is never read.
    body = "\n".join(re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", h, re.S))
    body += "\n" + "\n".join(re.findall(r'<(?:div|svg|text|path)[^>]*>', h))
    return re.sub(r"\s+", " ", body).strip()


def check(slides_dir: Path):
    files = sorted(slides_dir.glob("slide-*.html"))
    res = {"slides_dir": str(slides_dir), "slides": len(files),
           "fails": [], "warns": [], "pairs": []}
    if len(files) < 2:
        res["fails"].append(
            "cannot look: %d slide file(s) in %s" % (len(files), slides_dir))
        res["verdict"] = "FAIL"
        return res, 2

    codes = {f.name: art_code(f) for f in files}
    empty = [n for n, c in codes.items() if len(c) < 40]
    if empty:
        res["fails"].append(
            "cannot look: no readable art code in %s" % ", ".join(empty))
        res["verdict"] = "FAIL"
        return res, 2

    sims = []
    for a, b in itertools.combinations(files, 2):
        r = difflib.SequenceMatcher(None, codes[a.name], codes[b.name]).ratio()
        sims.append(r)
        res["pairs"].append({"a": a.name, "b": b.name, "similarity": round(r, 3)})
        if r >= FAIL_PAIR:
            res["fails"].append(
                "%s and %s are %.0f%% the same art code. That is one slide "
                "drawn twice, not two slides." % (a.name, b.name, r * 100))

    # --- how much of the art is DRAWN rather than dropped ------------------
    blocky = drawn = 0
    for f in files:
        # same blindness as art_code() above, and it is why the drawn share of
        # a module-script deck read 0 drawn against 0 blocky, which is not a
        # measurement of anything.
        s = "\n".join(re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>",
                                 f.read_text(), re.S))
        blocky += sum(s.count(k) for k in BLOCKY)
        drawn += sum(s.count(k) for k in DRAWN)
    total = blocky + drawn
    share = (drawn / total) if total else 0.0
    res["blocky_calls"] = blocky
    res["drawn_calls"] = drawn
    res["drawn_share"] = round(share, 3)
    if total and share < FAIL_DRAWN_SHARE:
        res["fails"].append(
            "BLOCKY DECK: %d axis-aligned rectangle calls against %d drawn or "
            "generated marks, a drawn share of %.0f%% under the %.0f%% line "
            "(bespoke reference: 82%%). This is shapes dropped onto a page, not "
            "art made for the story. Reach into the technique bench."
            % (blocky, drawn, share * 100, FAIL_DRAWN_SHARE * 100))
    elif total and share < WARN_DRAWN_SHARE:
        res["warns"].append(
            "drawn share %.0f%% is low; the deck leans on rectangles."
            % (share * 100))

    med = statistics.median(sims)
    res["median_similarity"] = round(med, 3)
    res["max_similarity"] = round(max(sims), 3)
    res["fail_threshold"] = FAIL_MEDIAN
    if med >= FAIL_MEDIAN:
        res["fails"].append(
            "TEMPLATED DECK: median pairwise art-code similarity is %.3f, over "
            "the %.2f line. The bespoke reference (examples/demo-deck) measures "
            "0.049. These slides are the same drawing code with different "
            "arguments, which is the one thing the engine's contract forbids. "
            "Write each slide's art for that slide." % (med, FAIL_MEDIAN))
    elif med >= WARN_MEDIAN:
        res["warns"].append(
            "median pairwise art-code similarity %.3f is high; the deck is "
            "leaning on shared drawing code. Check that each frame earns its "
            "own art." % med)

    res["verdict"] = "FAIL" if res["fails"] else ("WARN" if res["warns"] else "PASS")
    return res, (1 if res["fails"] else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slides-dir", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    d = Path(a.slides_dir)
    if not d.is_dir():
        print("bespoke_check: cannot look, no such directory %s" % d,
              file=sys.stderr)
        return 2
    res, code = check(d)
    if a.json:
        print(json.dumps(res, indent=2))
        return code
    for f in res["fails"]:
        print("FAIL: " + f)
    for w in res["warns"]:
        print("warn: " + w)
    if "median_similarity" in res:
        print("bespoke_check: %s -- %d slides, median pairwise art similarity "
              "%.3f (fail at %.2f), max pair %.3f, drawn share %.0f%% "
              "(%d drawn vs %d blocky, fail under %.0f%%)"
              % (res["verdict"], res["slides"], res["median_similarity"],
                 FAIL_MEDIAN, res["max_similarity"], res.get("drawn_share", 0) * 100,
                 res.get("drawn_calls", 0), res.get("blocky_calls", 0),
                 FAIL_DRAWN_SHARE * 100))
    return code


if __name__ == "__main__":
    sys.exit(main())
