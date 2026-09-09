#!/usr/bin/env python3
"""declaration_surface_verify.py -- the reconstruction behind dossier_check.py's
2026-09-09 declaration-surface checks. Run No.54, two defects, four fixtures.

THE FIRST DEFECT. `dossier_check.py` reads `data-contacts` off the <body> TAG in
the slide source, because it is meant to run BEFORE any render exists. `qa.py`
reads what render.py measured off the LIVE dom after renderReady. Four of run
No.54's slides set the attribute with `document.body.setAttribute(...)` at the
end of their draw: the render report carried their contacts, qa.py measured
them, and dossier_check failed all four for "declaring no data-contacts". Both
tools were right about their own surface and the message named neither, so the
author had no way to know which one wanted what.

THE SECOND DEFECT. The same run built four of those attributes with
`json.dumps(..., separators=(',', ' '))`, whose second element is the KEY
separator. That writes `{"what" "x"}`, json.loads answers "Expecting ':'
delimiter", and the whole thing reads like a hand-typing slip rather than like
the one-character argument it is. It went into four attributes in one pass and
was only findable because a gate printed the tail of what it could not parse.

THE FIXTURES, all four with the same dossier, which promises a contact shadow:

  1. data-contacts set at runtime         -> FAILS, and names the RUNTIME write
  2. data-contacts static on <body>       -> no declaration-surface finding
  3. static but written with separators=(',', ' ')
                                          -> FAILS the parse check AND names
                                             the json.dumps argument
  4. static and well formed               -> clean, and no runtime warn

Fixture 2 is the repair for 1 and fixture 4 is the repair for 3, so the test
also proves neither check fires on a correct declaration.

Usage: python tests/declaration_surface_verify.py   (exit 0 = all four hold)
Stdlib only, no network, writes only into a temp directory.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GATE = REPO / "scripts" / "dossier_check.py"

CONTACTS = [{"what": "the rating plate standing proud of the tank flank",
             "shadow": [[80, 700, 26, 10]], "ground": [[30, 700, 26, 10]]}]

DOSSIER = """## SLIDE %02d — the plate on the flank

### 4. Artwork
4a. Lower-third treatment. The tank's lower flank carries a graded ground with
a foreground plane of stipple and a hillshade relief reading down to the
skirt, so the bottom third holds modeled tone rather than flat furniture. The
rating plate sits proud of it and throws a two-part contact shadow onto the
lit pool beneath, with the terrain texture and its own grain running under
the annotation furniture and the leader line to the datum. Depth is carried by
an atmosphere wash over the far end of the tank, a silhouette on the near rim
and a noise field across the whole ground, so nothing in the lower band is
bare plate. The contact shadow is the anchor of the whole frame and the
gradient beneath it is what makes the object stand rather than float.

### 5. Copy
- head, Fraunces 92px, `THE PLATE`
"""


def slide(mode):
    """One slide, four ways of declaring the same contacts."""
    if mode == "runtime":
        body, tail = "<body>", (
            "document.body.setAttribute('data-contacts', JSON.stringify(%s));"
            % json.dumps(CONTACTS))
    elif mode == "separator":
        body, tail = ("<body data-contacts='%s'>"
                      % json.dumps(CONTACTS, separators=(",", " ")), "")
    else:
        body, tail = ("<body data-contacts='%s'>"
                      % json.dumps(CONTACTS, separators=(",", ":")), "")
    return ("<!doctype html><html><head><meta charset=\"utf-8\"></head>\n"
            + body + "\n<canvas id=\"art\" width=\"2160\" height=\"2700\"></canvas>\n"
            "<script type=\"module\">\n"
            "  const cx = document.getElementById('art').getContext('2d');\n"
            "  cx.scale(2, 2);\n  cx.fillStyle = '#1B1712';\n"
            "  cx.fillRect(0, 0, 1080, 1350);\n" + tail + "\n</script>\n"
            "</body></html>\n")


# (name, mode, needle, should_be_clean)
CASES = [
    ("data-contacts set at runtime", "runtime", "sets it at RUNTIME", False),
    ("data-contacts static on <body>", "static", "sets it at RUNTIME", True),
    ("static, built with separators=(',', ' ')", "separator",
     "separators=(',', ':')", False),
    ("static and well formed", "static", "separators=(',', ':')", True),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="declsurface_"))
    sl = tmp / "slides"
    sl.mkdir()
    story = []
    for i, (_, mode, _n, _c) in enumerate(CASES, 1):
        (sl / f"slide-0{i}.html").write_text(slide(mode))
        story.append(DOSSIER % i)
    (tmp / "storyboard.md").write_text("\n".join(story))
    try:
        r = subprocess.run([sys.executable, str(GATE), "--run-dir", str(tmp),
                            "--json"], capture_output=True, text=True, timeout=120)
        out = json.loads(r.stdout)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    by = {s["slide"]: s for s in out["slides"]}
    ok = True
    for i, (name, _mode, needle, should_pass) in enumerate(CASES, 1):
        s = by.get(i, {"fails": ["slide never read"], "warns": []})
        hits = [f for f in s["fails"] if needle in f]
        good = (not hits) if should_pass else bool(hits)
        # the runtime FAIL must NOT be the old "declares no data-contacts" line
        if good and hits and i == 1:
            good = "declares no data-contacts" not in hits[0]
        ok &= good
        print("[%s] %-42s -> %s" % ("HOLD" if good else "BROKE", name,
                                    "clean" if not hits else hits[0][:130]))
    # the deck-level runtime warn is one line, not one per slide
    warns = [w for s in out["slides"] for w in s["warns"] if "set at RUNTIME" in w]
    one = len(warns) == 1 and "slide 01 data-contacts" in warns[0]
    ok &= one
    print("[%s] %-42s -> %s" % ("HOLD" if one else "BROKE",
                                "one deck-level runtime warn",
                                warns[0][:130] if warns else "none"))
    print("declaration_surface_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
