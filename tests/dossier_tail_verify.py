#!/usr/bin/env python3
"""Does the LAST dossier end where the deck starts talking again? (2026-08-26)

Run No.41 wrote a "## BUILD RECONCILIATION" section at the foot of its
storyboard, describing the contact-shadow repairs it had made across the deck.
`slide_sections()` ran the last slide's section to end of file, so that deck
prose was read as SLIDE 09's dossier and slide 09 failed for promising a
contact shadow it never promised. The showrunner shipped by moving the section
above "## SLIDE 01", which repairs the gate by rearranging the author's
document.

This holds the fix to the exact shape of that defect: the same fixture, once
with the deck section at the foot and once with it at the head, must produce
the SAME verdict, and the trailing section's words must not appear in any
slide's body. The pre-fix splitter is reconstructed here (six lines, verbatim
from the old function) so the red case is proved red rather than asserted.

    python3 tests/dossier_tail_verify.py

Exit 0 HOLDS, exit 1 BROKEN.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dossier_check as dc  # noqa: E402

PLAN = (
    "4a. Lower-third treatment. The band sits on the same graded ground the "
    "map above it stands on, so the type has a lit surface under it rather "
    "than a flat plate: the terrain wash runs down past the horizon, the "
    "shadow of the marker crosses the top edge of the band, and the annotation "
    "furniture carries a tick every hundred metres so the reader can measure "
    "the fall. The claim-id sits right, in mono, over the darkest part of the "
    "graded ground where it reads without a scrim behind it."
)

DECK_TAIL = """## BUILD RECONCILIATION

Six slides had their type reserve rebuilt this round and every contact-shadow
declaration was re-measured off the render rather than off camera arithmetic.
"""


def storyboard(tail_at_foot):
    head = "# STORYBOARD -- fixture\n\n"
    slides = ""
    for n in (1, 2):
        slides += "## SLIDE %02d -- FIXTURE\n\n%s\n\n" % (n, PLAN)
    return head + (slides + DECK_TAIL if tail_at_foot else DECK_TAIL + "\n" + slides)


def old_slide_sections(text):
    """The splitter as it stood before 2026-08-26, for the red case."""
    heads = list(dc.HEAD_RE.finditer(text))
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out.append((int(m.group(1)), m.group(2).strip(), text[m.end():end]))
    return out


def run_gate(text):
    """Run the real gate over a fixture run dir. Returns (exit_code, output)."""
    with tempfile.TemporaryDirectory() as d:
        rd = Path(d)
        (rd / "storyboard.md").write_text(text)
        sdir = rd / "slides"
        sdir.mkdir()
        for n in (1, 2):
            # No data-contacts anywhere: the whole point is that a slide which
            # declares none must not be put on the hook by the deck's own prose.
            (sdir / ("slide-%02d.html" % n)).write_text(
                "<html><body><h1>fixture</h1></body></html>")
        p = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "dossier_check.py"),
             "--run-dir", str(rd)],
            capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr


def main():
    bad = []

    foot, head = storyboard(True), storyboard(False)

    # RED: the pre-fix splitter swallows the deck section into slide 02.
    old = old_slide_sections(foot)
    if "contact-shadow" not in old[-1][2]:
        bad.append("red case did not reproduce: the pre-fix splitter did not "
                   "swallow the trailing deck section")
    old_f, _ = dc.check_slide(2, old[-1][1], old[-1][2], None, None, True)
    if not any("promises a contact shadow" in f for f in old_f):
        bad.append("red case did not reproduce: the pre-fix body did not fail "
                   "the contact-promise check")

    # GREEN: the fixed splitter bounds the last dossier at the deck heading.
    new = dc.slide_sections(foot)
    if len(new) != 2:
        bad.append("fixed splitter found %d dossiers, expected 2" % len(new))
    elif "contact-shadow" in new[-1][2] or "BUILD RECONCILIATION" in new[-1][2]:
        bad.append("fixed splitter still swallows the trailing deck section")

    # And the whole gate now returns the same verdict either way round.
    rc_foot, out_foot = run_gate(foot)
    rc_head, out_head = run_gate(head)
    if rc_foot != rc_head:
        bad.append("gate verdict depends on WHERE the deck section sits: "
                   "foot=%d head=%d\n--- foot ---\n%s" % (rc_foot, rc_head, out_foot))
    if rc_foot != 0:
        bad.append("gate FAILs a fixture whose slides promise nothing:\n" + out_foot)
    if "promises a contact shadow" in out_head:
        bad.append("control case is not clean; fixture is wrong:\n" + out_head)

    # FALSE-POSITIVE GUARD: a dossier's own ### subheadings and its numbered
    # fields must still belong to the slide. Only # and ## end a dossier.
    inner = ("# STORYBOARD -- fixture\n\n## SLIDE 01 -- FIXTURE\n\n"
             "### 3. Art direction\n\nA lit ground with a cast shadow.\n\n"
             + PLAN + "\n\n#### notes\n\ncontact-shadow declared in the body.\n")
    sec = dc.slide_sections(inner)
    if len(sec) != 1 or "contact-shadow" not in sec[0][2] or "Art direction" not in sec[0][2]:
        bad.append("a dossier's own ### / #### subsections were cut off the "
                   "slide body; only top-level headings may end a dossier")

    # REGRESSION: the storyboard shape every run actually writes (deck sections
    # above SLIDE 01, nothing after the last slide) must split identically.
    plain = "# S\n\n## PREAMBLE\n\ntext\n\n" + "".join(
        "## SLIDE %02d -- X\n\n%s\n\n" % (n, PLAN) for n in (1, 2, 3))
    if [s[0] for s in dc.slide_sections(plain)] != [1, 2, 3] or \
            dc.slide_sections(plain)[-1][2] != old_slide_sections(plain)[-1][2]:
        bad.append("split changed for a storyboard with no trailing deck section")

    if bad:
        print("BROKEN")
        for b in bad:
            print(" - " + b)
        return 1
    print("HOLDS: the last dossier ends at the next top-level heading; the "
          "gate's verdict no longer depends on where a deck section sits, and "
          "### / #### subsections still belong to their slide.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
