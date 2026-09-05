#!/usr/bin/env python3
"""plan_drift_check.py -- the plan and the build have to agree about the build.

WHY THIS EXISTS (2026-08-20, run No.38)

    Plan-versus-pixel drift was flagged by the scorer in ALL THREE of that
    run's scoring rounds and was the one defect class the run never got ahead
    of. Every instance was the storyboard describing a deck that had stopped
    existing four fix passes earlier:

      - the claims index kept assigning claim ids to slides that never printed
        them (C13, C17, C29, C28 during the run; C03, C07, C10 and C24 were
        STILL over-assigned in the storyboard that shipped);
      - a dossier said FIVE declared marks after three shipped, and TWO
        DECLARED MEASURED AXES with one declared in the markup;
      - aggregates.json quoted a mono note the render had stopped printing.

    Every one was found by a human-equivalent reader -- a pixel critic or the
    scorer -- never by a gate, because no gate compared the PLAN against the
    BUILD. copy_sync_check compares copy.json to the render, aggregate_check
    re-derives declared numbers, dossier_check reads the plan alone. The
    storyboard is the document the scorer grades and the next run learns from,
    so a storyboard that describes a different deck is a defect in the record
    even when the pixels are right.

WHAT IT CHECKS. Three things, all mechanical, none of them a judgment.

    1. THE CLAIMS INDEX AGREES WITH copy.json. SLIDE_DOSSIER_SPEC requires the
       storyboard header to carry a claims index (claim-id -> slide(s) where
       used). Every assignment in it must match the claim_ids copy.json carries
       for that slide, in BOTH directions, and a claim the index marks NOT USED
       must appear on no slide. Where the render prints claim tags, the printed
       tags are reported as EVIDENCE of which of the two artifacts drifted --
       never as a source of pass or fail, because a slide is allowed to carry a
       claim without stencilling its id.

    2. A DECLARED COUNT IN A DOSSIER MATCHES THE MARKUP. The house writes
       counts as "FIVE declared marks", "THREE DECLARED LEADERS", "TWO DECLARED
       MEASURED AXES". Those five nouns (marks, leaders, axes/scales,
       encodings, contact shadows) are all things the slide body declares in
       machine-readable form and the render report counts, so the sentence and
       the build are directly comparable. A mismatch is a FAIL: either the plan
       is stale or a declaration the plan promised never made it into the
       markup, and the second case silently switches off a qa.py gate.
       Any other noun after "declared" is reported and not judged.

    3. THE BODY COPY THE DOSSIER QUOTES IS STILL IN THE DECK. A dossier quotes
       its slide's body copy verbatim in backticks. When copy.json's body for
       that slide is the dossier's sentences MINUS one or more, the copy was
       CUT and the plan still promises what was cut. That is a FAIL. A rewrite
       (any sentence copy.json carries that the plan does not) is reported and
       not judged, because a rewrite adds rather than removes and the corpus
       says runs edit wording often and drop sentences rarely.

    Nothing here is loosened by a fix elsewhere: reconcile by correcting the
    stale artifact, never by deleting the sentence that disagrees.

WHAT IT DOES NOT READ (2026-09-04). Only the DOSSIERS, never the generated
    record. gate_status.py --sync writes a GATE STATUS block into the same
    storyboard, and that block quotes this check's own failures back at it: run
    No.50 reworded the sentence a count drift named, re-synced, and the check
    found the same words again in the block it had just caused to be written.
    A slide's dossier now also ends at the next top-level heading that is not a
    slide, the way dossier_check's has since 2026-08-26, so a BUILD
    RECONCILIATION written after slide 09 is the deck's prose and not slide
    09's plan.

USAGE
    python scripts/plan_drift_check.py --run-dir out/2026-08-20
    python scripts/plan_drift_check.py --run-dir out/2026-08-20 --json

EXIT CODES
    0  plan and build agree
    1  drift found
    2  the check could not look (missing storyboard, copy.json, render report,
       or no parseable claims index). A check that can't look is a FAIL at the
       ship gate, like its siblings.

Read-only. Stdlib only.
"""

import argparse
import json
import re
import sys
from pathlib import Path

HEAD_RE = re.compile(r"^##\s+SLIDE\s+(\d+)\b(.*)$", re.I | re.M)
TOP_HEAD_RE = re.compile(r"^\s{0,3}#{1,2}\s+\S.*$", re.M)
INDEX_HEAD_RE = re.compile(
    r"^(?:#{2,4}\s*|\*{0,2})claims index\b[^\n]*$", re.I | re.M)
CLAIM_RE = re.compile(r"\bC\s?(\d{1,3})\b", re.I)
SLIDE_NUM_RE = re.compile(r"\bS?(\d{1,2})\b")

WORD_NUM = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
}
COUNT_RE = re.compile(
    r"\b(" + "|".join(WORD_NUM) + r"|\d{1,2})\s+(?:\*{0,2})declared(?:\*{0,2})\s+"
    r"([A-Za-z][A-Za-z ]{2,32})", re.I)

# noun keyword -> (render_report field, how to count it, human name)
NOUNS = [
    ("mark", "marks", "declared marks on measured axes"),
    ("leader", "leaders", "declared leader lines"),
    ("axes", "scales", "declared measured axes (data-scale)"),
    ("axis", "scales", "declared measured axes (data-scale)"),
    ("scale", "scales", "declared measured axes (data-scale)"),
    ("encoding", "encodings", "declared wordless encodings (data-encodes)"),
    ("encodes", "encodings", "declared wordless encodings (data-encodes)"),
    ("contact", "contacts", "declared contact shadows (data-contacts)"),
    ("shadow", "contacts", "declared contact shadows (data-contacts)"),
]

REMEDY = ("Reconcile the STALE artifact, never the sentence that disagrees: if "
          "the build is right, edit the storyboard; if the plan is right, the "
          "declaration is missing from the slide markup and a qa.py gate is "
          "switched off on that slide.")


def slide_no(fname):
    m = re.search(r"slide-(\d+)", fname or "")
    return int(m.group(1)) if m else None


NOT_USED_RE = re.compile(
    r"not used|unused|background only|does not ship|never printed|no slide", re.I)
ARROW_RE = re.compile(r"\bC\s?(\d{1,3})\s*(?:->|-->|→|:)\s*((?:S?\d{1,2}\s*[,/]?\s*)+)",
                      re.I)


def _slides_of(cell):
    return set(int(n) for n in SLIDE_NUM_RE.findall(cell) if 1 <= int(n) <= 30)


def _add(out, cid, slides):
    # COPY, never alias. One row's slide set is shared by every claim id on that
    # row, so a later in-place |= against one claim mutated the set every other
    # claim on that row was still holding, and slide numbers leaked sideways
    # across the whole index (caught on runs/2026-08-09: 33 drifts reported, 0
    # of them real).
    if cid in out and out[cid] is not None and slides is not None:
        out[cid] = out[cid] | slides
    else:
        out[cid] = set(slides) if slides is not None else None


def parse_claims_index(text):
    """Return {claim_id: set(slide numbers) or None for NOT USED}, or None when
    no index can be found.

    FOUR SHAPES, because the house has written all four and a gate that reads
    only the one this week's run happened to use is a gate that silently does
    not run. Surveyed over the shipped corpus (runs/*/storyboard.md):

      claim-first table   | C01 proclamation title | 01, 02 |
      slide-first table   | Slide | Claim ids |  ->  | 01 | C18 C19 C20 |
      bullet              - c1/c2 ($875M award): S2, S8
      arrow block         C01 -> S1, S3        C02 -> S1, S3
    """
    m = INDEX_HEAD_RE.search(text)
    if not m:
        return None
    seg = text[m.end():]

    # THE INDEX IS THE CONTIGUOUS BLOCK UNDER ITS OWN HEADING, and nothing
    # else. Ending it at "the next heading" was wrong on the first storyboard
    # it met: run No.31's index is followed by a bold paragraph rather than a
    # heading, so the reader ran on through the whole document and picked up
    # every later table, which put slide 06 on all 52 claims. Consume index
    # lines while they keep coming; the first line that is not one ends it.
    out = {}
    transposed = False
    started = False
    for line in seg.splitlines():
        s = line.strip()
        if re.match(r"^\s{0,3}#{1,6}\s", line):
            break
        if not s:
            if started:
                break
            continue
        if s.startswith("|") and s.count("|") >= 3:
            started = True
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) < 2 or set(cells[0]) <= set("-: "):
                continue                                    # rule row
            head = cells[0].lower()
            if "slide" in head and "claim" in cells[1].lower():
                transposed = True                           # header row
                continue
            if "claim" in head and "slide" in cells[1].lower():
                transposed = False
                continue
            left, right = (cells[1], cells[0]) if transposed else (cells[0], cells[1])
        elif s.startswith(("-", "*")) and ":" in s and CLAIM_RE.search(s.split(":", 1)[0]):
            started = True
            left, right = s.lstrip("-* ").split(":", 1)
        elif ARROW_RE.search(s):
            started = True
            for cid_n, tail in ARROW_RE.findall(s):
                _add(out, "C%02d" % int(cid_n), _slides_of(tail))
            continue
        elif started:
            break                    # the block ended; everything after is prose
        else:
            continue

        ids = ["C%02d" % int(n) for n in CLAIM_RE.findall(left)]
        if not ids:
            continue
        slides = None if NOT_USED_RE.search(right) else _slides_of(right)
        # "C04 to C08" names a RANGE of claims; expand it so the row is not
        # read as two claims with a hole between them.
        if len(ids) == 2 and re.search(r"\bto\b|–|-", left):
            a, b = int(ids[0][1:]), int(ids[1][1:])
            if b > a:
                ids = ["C%02d" % n for n in range(a, b + 1)]
        for cid in ids:
            _add(out, cid, slides)
    return out or None


def copy_claim_ids(copy):
    """{claim_id: set(slide numbers)} from copy.json, whichever shape it is."""
    slides = copy.get("slides")
    items = []
    if isinstance(slides, dict):
        for k, v in slides.items():
            n = re.sub(r"[^0-9]", "", str(k))
            items.append((int(n) if n else None, v))
    elif isinstance(slides, list):
        for i, v in enumerate(slides):
            n = None
            if isinstance(v, dict):
                for key in ("slide", "n", "no", "index"):
                    if isinstance(v.get(key), int):
                        n = v[key]
                        break
            items.append((n if n else i + 1, v))
    out = {}
    for n, v in items:
        if not isinstance(v, dict) or n is None:
            continue
        for cid in v.get("claim_ids") or []:
            m = CLAIM_RE.search(str(cid))
            if m:
                out.setdefault("C%02d" % int(m.group(1)), set()).add(n)
    return out


def printed_tags(report):
    """{slide no: set(claim ids printed as text)} -- evidence only."""
    out = {}
    for s in report.get("slides", []):
        n = slide_no(s.get("file"))
        if n is None:
            continue
        parts = []
        for node in s.get("text_nodes", []):
            parts.append(node.get("text", "") or "")
            parts.extend(node.get("texts") or [])
        blob = " ".join(parts)
        out[n] = set("C%02d" % int(x) for x in CLAIM_RE.findall(blob))
    return out


def build_counts(report):
    """{slide no: {field: count}} straight off the render report."""
    out = {}
    for s in report.get("slides", []):
        n = slide_no(s.get("file"))
        if n is None:
            continue
        scales = s.get("scales") or []
        out[n] = {
            "scales": len([x for x in scales if not x.get("error")]),
            "marks": sum(len(x.get("marks") or []) for x in scales),
            "leaders": len([x for x in (s.get("leaders") or []) if not x.get("error")]),
            "encodings": len([x for x in (s.get("encodings") or []) if not x.get("error")]),
            "contacts": len([x for x in (s.get("contacts") or []) if not x.get("error")]),
        }
    return out


# THE GENERATED BLOCK IS NOT THE PLAN (2026-09-04). gate_status.py --sync
# writes its GATE STATUS block into the run record, the block says in its own
# first line "Do not hand-write these lines", and this check was reading it as
# storyboard prose. Run No.50's count drift quoted the offending sentence into
# a row, --sync wrote the row into the storyboard, and the next pass found the
# words again inside the block it had itself caused to be written: rewording
# the real sentence did not clear the row, and it had to be cleared by hand.
# The boundary is gate_status's own: the head line, its [STATUS] rows, and the
# ">> N FAIL row(s)" tail.
BLOCK_HEAD = "GATE STATUS -- generated by scripts/gate_status.py"
BLOCK_ROW_RE = re.compile(r"^\s*\[\s*(?:PASS|WARN|FAIL|n/a)\s*\]\s+\S+\s+.*$")
BLOCK_TAIL_RE = re.compile(r"^\s*>>\s+\d+\s+FAIL row\(s\)\.")


def strip_generated(text):
    """Return (text without every generated GATE STATUS block, blocks removed).

    Removal keeps the line count and the byte offsets of everything else
    unchanged (each removed line becomes empty), so nothing downstream shifts.
    """
    lines = text.splitlines()
    removed = 0
    i = 0
    while i < len(lines):
        if BLOCK_HEAD not in lines[i]:
            i += 1
            continue
        removed += 1
        lines[i] = ""
        i += 1
        while i < len(lines):
            if BLOCK_ROW_RE.match(lines[i]):
                lines[i] = ""
                i += 1
            elif BLOCK_TAIL_RE.match(lines[i]):
                lines[i] = ""
                i += 1
                break
            else:
                break
    return "\n".join(lines), removed


def slide_sections(text):
    """(slide_no, body) per dossier.

    A dossier ends at the next slide OR at the next top-level heading that is
    not a slide, which is dossier_check's 2026-08-26 rule and is here for the
    same reason: a BUILD RECONCILIATION or a GATE STATUS section written after
    the last slide is the DECK's prose, and reading it as slide 09's plan
    attributes the run's own repair notes to a dossier.
    """
    heads = list(HEAD_RE.finditer(text))
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        for t in TOP_HEAD_RE.finditer(text, m.end(), end):
            if not HEAD_RE.match(t.group(0)):
                end = t.start()
                break
        out.append((int(m.group(1)), text[m.end():end]))
    return out


def check_claims_index(sb_text, copy, report):
    fails, notes = [], []
    idx = parse_claims_index(sb_text)
    if idx is None:
        return None, ["no parseable claims index in storyboard.md. "
                      "SLIDE_DOSSIER_SPEC requires one in the deck header "
                      "(claim-id -> slide(s) where used); write it as a "
                      "'### Claims index' markdown table (| C01 title | 01, 02 |) "
                      "or a bullet list (- C01 title: 01, 02), and mark an "
                      "unused claim NOT USED."], []
    cp = copy_claim_ids(copy)
    tags = printed_tags(report) if report else {}
    for cid in sorted(set(idx) | set(cp), key=lambda c: int(c[1:])):
        planned = idx.get(cid, "absent")
        carried = cp.get(cid, set())
        if planned == "absent":
            fails.append("%s is on %s in copy.json and is missing from the "
                         "claims index. %s" % (
                             cid, fmt_slides(carried), REMEDY))
            continue
        if planned is None:
            if carried:
                fails.append("%s is marked NOT USED in the claims index but "
                             "copy.json carries it on %s. %s"
                             % (cid, fmt_slides(carried), REMEDY))
            continue
        if planned == carried:
            continue
        over = sorted(planned - carried)
        under = sorted(carried - planned)
        bits = []
        if over:
            ev = []
            for n in over:
                if n in tags:
                    ev.append("%s does not print it" % fmt_slides([n])
                              if cid not in tags[n] else
                              "%s prints its tag, so copy.json is the stale one"
                              % fmt_slides([n]))
            bits.append("the index assigns it to %s where copy.json does not "
                        "carry it%s" % (fmt_slides(over),
                                        " (" + "; ".join(ev) + ")" if ev else ""))
        if under:
            bits.append("copy.json carries it on %s where the index does not "
                        "list it" % fmt_slides(under))
        fails.append("%s: %s. %s" % (cid, "; and ".join(bits), REMEDY))
    notes.append("claims index: %d claims, copy.json: %d claims"
                 % (len(idx), len(cp)))
    return len(idx), fails, notes


def fmt_slides(ns):
    ns = sorted(ns)
    if not ns:
        return "no slide"
    return ("slide " if len(ns) == 1 else "slides ") + ", ".join("%02d" % n for n in ns)


def check_declared_counts(sb_text, counts):
    fails, notes = [], []
    checked = 0
    for no, body in slide_sections(sb_text):
        built = counts.get(no)
        for m in COUNT_RE.finditer(body):
            raw, noun = m.group(1), m.group(2).strip().lower()
            said = WORD_NUM.get(raw.lower(), None)
            if said is None:
                try:
                    said = int(raw)
                except ValueError:
                    continue
            field = human = None
            for key, f, name in NOUNS:
                if re.search(r"\b" + key, noun):
                    field, human = f, name
                    break
            if field is None:
                notes.append("slide %02d: '%s declared %s' names nothing this "
                             "check counts; not judged" % (no, raw, noun[:28]))
                continue
            if built is None:
                notes.append("slide %02d: not in the render report, so '%s "
                             "declared %s' was not checked" % (no, raw, noun[:28]))
                continue
            checked += 1
            got = built.get(field, 0)
            if got != said:
                fails.append(
                    "slide %02d: the dossier says %s declared %s, the build has "
                    "%d %s. %s" % (no, raw.upper(), noun[:34], got, human, REMEDY))
    return checked, fails, notes


# COPY CUT TO FIT IS INVISIBLE TO EVERY OTHER GATE (2026-09-04). Run No.50
# shipped three slides whose body copy had been silently shortened to make it
# fit its box (34 words against a declared 46, 23 against 43, 36 against 47),
# and one of the cuts removed the single sentence that the slide's own on-slide
# attribution qualified, leaving claim C15 with no referent in the picture.
# Nothing could see it: copy_sync_check compares copy.json to the RENDER, and a
# build that cut a sentence and a copy.json written from that build agree
# perfectly. The dossier is the only artifact that still holds the sentence.
# Three pixel critics found it by reading.
#
# THE DIRECTION IS THE WHOLE CHECK. Measured over the shipped corpus (34
# dossier body quotes with a copy.json body to compare, runs/2026-08-04 to
# 2026-09-04): 18 are byte identical, 12 are rewrites, and 4 are cuts. Firing
# on rewrites would fail a third of historical dossiers for wording a run is
# allowed to change; firing on cuts alone fires on 9 percent, and every one of
# those four is a sentence a slide promised and did not print.
BODY_RE = re.compile(r"^-\s*(?:\*{0,2})bod(?:y|ies)\b[^`\n]*`([^`]+)`", re.I | re.M)
BODY_MIN_WORDS = 8
SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _sentences(s):
    s = re.sub(r"\s+", " ", s or "").strip()
    return [p.strip() for p in SENT_SPLIT_RE.split(s) if len(p.split()) >= 2]


def _sent_key(s):
    """Compare on words, so a straightened quote or a stray tag is not a cut."""
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def copy_slide_rows(copy):
    """{slide no: the slide object} from copy.json, whichever shape it is."""
    slides = copy.get("slides")
    out = {}
    if isinstance(slides, dict):
        for k, v in slides.items():
            n = re.sub(r"[^0-9]", "", str(k))
            if n and isinstance(v, dict):
                out[int(n)] = v
    elif isinstance(slides, list):
        for i, v in enumerate(slides):
            if not isinstance(v, dict):
                continue
            n = None
            for key in ("slide", "n", "no", "index"):
                if isinstance(v.get(key), int):
                    n = v[key]
                    break
            out[n or i + 1] = v
    return out


def check_body_copy(sb_text, copy):
    """The sentences the dossier quotes are still the sentences the deck says."""
    fails, notes = [], []
    rows = copy_slide_rows(copy)
    checked = 0
    for no, body in slide_sections(sb_text):
        m = BODY_RE.search(body)
        if not m:
            continue
        plan = re.sub(r"\s+", " ", m.group(1)).strip()
        if len(plan.split()) < BODY_MIN_WORDS:
            continue                      # a type token, not a sentence of copy
        got = (rows.get(no) or {}).get("body")
        if isinstance(got, list):
            got = " ".join(str(x) for x in got)
        if not isinstance(got, str) or not got.strip():
            notes.append("slide %02d: the dossier quotes %d words of body copy "
                         "and copy.json carries no `body` for that slide, so "
                         "they were not compared" % (no, len(plan.split())))
            continue
        checked += 1
        ps, gs = _sentences(plan), _sentences(got)
        pk, gk = [_sent_key(x) for x in ps], [_sent_key(x) for x in gs]
        if _sent_key(plan) == _sent_key(got):
            continue
        missing = [x for x in pk if x not in gk]
        added = [x for x in gk if x not in pk]
        if missing and not added:
            lost = "; ".join('"%s"' % ps[pk.index(x)] for x in missing[:3])
            fails.append(
                "slide %02d: the dossier quotes %d words of body copy and "
                "copy.json carries %d of them, with %d sentence(s) dropped and "
                "nothing put in their place: %s. Copy cut to fit is invisible "
                "everywhere else, because copy_sync_check compares copy.json to "
                "the render and both agree once the cut is made. %s"
                % (no, len(plan.split()), len(got.split()), len(missing), lost,
                   REMEDY))
        elif missing or added:
            notes.append("slide %02d: the dossier's body copy and copy.json's "
                         "differ by %d sentence(s) removed and %d added, which "
                         "reads as a rewrite rather than a cut; not judged"
                         % (no, len(missing), len(added)))
    if not checked:
        # SAY WHEN IT DID NOT RUN. Four of the seven decks with a render report
        # on disk write their dossier copy without a backticked quote or ship a
        # copy.json with no `body` key, and this check is silent on all four.
        # A silent check is indistinguishable from a clean one.
        notes.append("no body copy was compared: this check reads the dossier "
                     "line `- body ... `the copy verbatim`` against copy.json's "
                     "`body` for that slide, and this run's dossiers or copy.json "
                     "carry neither. Quote the copy in the dossier if you want "
                     "the plan checked against it.")
    return checked, fails, notes


SELF_TEST_SB = """# STORYBOARD - self test

### Claims index

| Claim | Slides |
|---|---|
| C01 the first figure | 01, 02 |
| C02 the second figure | 02 |
| C03 the cut one | NOT USED (mark cut in the fix pass) |

**A bold paragraph right after the table, not a heading.** Run No.31's
storyboard ends its index this way and the reader must stop here.

| Slide | Something else entirely |
|---|---|
| 06 | a later table that must not leak slide 06 into every claim |

## SLIDE 01

**8. Data-in-art mapping.** THREE declared marks on the rail, TWO DECLARED
LEADERS, and ONE declared measured axis.

**3. Copy.**
- body (24 words), `The window closes on the 19th. Two decisions ride it. The
land is reported to transfer at no cost. Nobody has published a date.`

## SLIDE 02

**8. Data-in-art mapping.** ONE declared grid violation, which this check
does not count.

### GATE STATUS, pasted into the dossier's own tail by --sync

```
GATE STATUS -- generated by scripts/gate_status.py from the artifacts in out/2026-01-01. Do not hand-write these lines.
[PASS] render         2/2 slides OK, 0 page errors, 0 overflow warnings
[FAIL] plan_drift     slide 02: the dossier says FIVE declared marks, the build has 0 declared marks on measured axes
>> 1 FAIL row(s). Fix the artifact, not the sentence.
```

## BUILD RECONCILIATION

Slide 01 shipped with FIVE declared marks after the rail was rebuilt, and this
paragraph is the deck's prose about the build. It is not slide 01's dossier and
must not be read as one.
"""

SELF_TEST_BODY = ("The window closes on the 19th. Two decisions ride it. The "
                  "land is reported to transfer at no cost. Nobody has "
                  "published a date.")
SELF_TEST_COPY = {"slides": [{"slide": 1, "claim_ids": ["C01"],
                              "body": SELF_TEST_BODY},
                             {"slide": 2, "claim_ids": ["C01", "C02"]}]}
SELF_TEST_REPORT = {"slides": [
    {"file": "slide-01.html",
     "scales": [{"marks": [{"at": 1}, {"at": 2}, {"at": 3}]}],
     "leaders": [{}, {}], "encodings": [], "contacts": [],
     "text_nodes": [{"text": "C01 on the plate"}]},
    {"file": "slide-02.html", "scales": [], "leaders": [], "encodings": [],
     "contacts": [], "text_nodes": [{"text": "C01 C02"}]},
]}


def self_test():
    """Hermetic: no run dir, no network, no subprocess. Covers the shape this
    gate exists for AND the aliasing bug found while building it."""
    import tempfile

    fails = []

    def check(name, cond, extra=""):
        print("  [%s] %s%s" % ("ok  " if cond else "FAIL", name,
                               "" if cond else "  <- " + str(extra)))
        if not cond:
            fails.append(name)

    idx = parse_claims_index(SELF_TEST_SB)
    check("the index parses", idx is not None and len(idx) == 3, idx)
    check("  NOT USED reads as used nowhere", idx.get("C03") is None)
    check("  a claim keeps only its own slides", idx.get("C02") == {2}, idx.get("C02"))
    check("  the block ends at the prose under it (no slide 06 leak)",
          all(6 not in (v or set()) for v in idx.values()), idx)

    # The fixture carries a pasted GATE STATUS block, exactly as --sync leaves
    # one; every check below reads the plan the way main() does, with the
    # generated record removed. The block's own reconstruction is further down.
    stripped, nblocks = strip_generated(SELF_TEST_SB)

    counts = build_counts(SELF_TEST_REPORT)
    check("the build counts come off the render report",
          counts[1] == {"scales": 1, "marks": 3, "leaders": 2,
                        "encodings": 0, "contacts": 0}, counts.get(1))

    n, cfails, _ = check_declared_counts(stripped, counts)
    check("a dossier count that matches the build passes", not cfails, cfails)
    check("  and three countable nouns were actually compared", n == 3, n)

    bad = stripped.replace("THREE declared marks", "FIVE declared marks")
    _, bfails, _ = check_declared_counts(bad, counts)
    check("THE No.38 DEFECT: 'FIVE declared marks' against 3 in the build FAILS",
          len(bfails) == 1 and "slide 01" in bfails[0], bfails)

    _, ifails, _ = check_claims_index(SELF_TEST_SB, SELF_TEST_COPY, SELF_TEST_REPORT)
    check("an index that agrees with copy.json passes", not ifails, ifails)

    over = dict(SELF_TEST_COPY)
    over["slides"] = [{"slide": 1, "claim_ids": ["C01"]},
                      {"slide": 2, "claim_ids": ["C01"]}]
    _, ofails, _ = check_claims_index(SELF_TEST_SB, over, SELF_TEST_REPORT)
    check("THE No.38 DEFECT: an id indexed to a slide that never printed it FAILS",
          len(ofails) == 1 and ofails[0].startswith("C02"), ofails)

    cut = {"slides": [{"slide": 1, "claim_ids": ["C01", "C03"]},
                      {"slide": 2, "claim_ids": ["C01", "C02"]}]}
    _, kfails, _ = check_claims_index(SELF_TEST_SB, cut, SELF_TEST_REPORT)
    check("a claim marked NOT USED that is still carried FAILS",
          len(kfails) == 1 and "NOT USED" in kfails[0], kfails)

    # THE No.50 LOOP: the check reading the record the gates write into the plan.
    check("the generated GATE STATUS block is found and removed", nblocks == 1,
          nblocks)
    check("  and nothing else moves (line count unchanged)",
          len(stripped.splitlines()) == len(SELF_TEST_SB.splitlines()))
    _, rawfails, _ = check_declared_counts(SELF_TEST_SB, counts)
    check("THE No.50 LOOP: the unstripped record feeds this check its own "
          "failure back", len(rawfails) == 1 and "FIVE" in rawfails[0]
          and "slide 02" in rawfails[0], rawfails)
    _, clean, _ = check_declared_counts(stripped, counts)
    check("  and the stripped plan is clean, so rewording the real sentence "
          "clears the row", not clean, clean)
    check("  a section after the last slide is the deck's prose, not a dossier",
          all("RECONCILIATION" not in b for _, b in slide_sections(stripped)))

    # THE No.50 CUT: body copy shortened to fit, with the plan still promising it.
    n_b, bfails, bnotes = check_body_copy(stripped, SELF_TEST_COPY)
    check("a dossier body quote that matches copy.json passes",
          not bfails and n_b == 1, bfails)
    shortened = json.loads(json.dumps(SELF_TEST_COPY))
    shortened["slides"][0]["body"] = SELF_TEST_BODY.replace(
        "Two decisions ride it. ", "")
    _, sfails, _ = check_body_copy(stripped, shortened)
    check("THE No.50 DEFECT: a sentence dropped from the copy but still "
          "promised by the dossier FAILS",
          len(sfails) == 1 and "Two decisions ride it." in sfails[0], sfails)
    rewritten = json.loads(json.dumps(SELF_TEST_COPY))
    rewritten["slides"][0]["body"] = SELF_TEST_BODY.replace(
        "Two decisions ride it.", "Two decisions ride the same window.")
    _, rfails, rnotes = check_body_copy(stripped, rewritten)
    check("  a REWRITE is reported and not judged", not rfails and rnotes,
          rfails)
    tagged = json.loads(json.dumps(SELF_TEST_COPY))
    tagged["slides"][0]["body"] = SELF_TEST_BODY + " (C15)"
    _, tfails, _ = check_body_copy(stripped, tagged)
    check("  a claim tag appended in copy.json is not a cut", not tfails, tfails)
    _, nfails, nnotes = check_body_copy(stripped, {"slides": [{"slide": 1}]})
    check("  no `body` in copy.json is a note, never a silent pass",
          not nfails and any("not compared" in n for n in nnotes), nnotes)

    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "2026-01-01"
        run.mkdir()
        (run / "storyboard.md").write_text(SELF_TEST_SB)
        (run / "copy.json").write_text(json.dumps({"slides": [{"slide": 1}]}))
        (run / "render_report.json").write_text(json.dumps(SELF_TEST_REPORT))
        argv = sys.argv
        sys.argv = ["plan_drift_check", "--run-dir", str(run)]
        try:
            rc = main()
        finally:
            sys.argv = argv
        check("copy.json with no claim_ids at all is CANNOT LOOK (exit 2)", rc == 2, rc)

    print("plan_drift_check self-test: %s (%d failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(
        description="Cross-check the storyboard's plan against the build.")
    ap.add_argument("--run-dir")
    ap.add_argument("--self-test", action="store_true",
                    help="hermetic regression test; no run dir needed")
    ap.add_argument("--render-report")
    ap.add_argument("--copy")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.run_dir:
        ap.error("--run-dir is required (or use --self-test)")

    run = Path(args.run_dir)
    sb = run / "storyboard.md"
    copyp = Path(args.copy) if args.copy else run / "copy.json"
    rrp = Path(args.render_report) if args.render_report else (
        run / "render" / "render_report.json" if (run / "render").is_dir()
        else run / "render_report.json")

    missing = [str(p) for p in (sb, copyp, rrp) if not p.exists()]
    if missing:
        print("plan_drift_check: CANNOT LOOK -- missing %s" % ", ".join(missing),
              file=sys.stderr)
        return 2
    try:
        sb_text = sb.read_text(errors="replace")
        copy = json.loads(copyp.read_text())
        report = json.loads(rrp.read_text())
    except (OSError, ValueError) as e:
        print("plan_drift_check: CANNOT LOOK -- %s" % e, file=sys.stderr)
        return 2

    # ZERO CLAIM IDS COMPARED IS NOT AGREEMENT, IT IS NOTHING TO COMPARE.
    # Same rule copy_sync_check applies to zero authored strings: a run whose
    # copy.json carries no claim_ids at all would score a clean sheet here for
    # the worst possible reason. It also means site_build.py has nothing to
    # join on, so the published deck page ships without its verification
    # record (routine_instructions Phase 11: "joining copy.json slides to
    # claims.json on claim_ids").
    if not copy_claim_ids(copy):
        print("plan_drift_check: CANNOT LOOK -- copy.json carries no claim_ids on "
              "any slide, so the claims index has nothing to be checked against. "
              'Add "claim_ids": ["C01", ...] to every slide object in copy.json; '
              "the site's per-deck verification record is built from that join.",
              file=sys.stderr)
        return 2

    # THE PLAN IS THE DOSSIERS, NOT THE RECORD THE GATES WRITE INTO IT.
    sb_text, blocks = strip_generated(sb_text)

    res = check_claims_index(sb_text, copy, report)
    if res[0] is None:
        _, blocked, _ = res
        print("plan_drift_check: CANNOT LOOK -- %s" % blocked[0], file=sys.stderr)
        return 2
    n_claims, cfails, cnotes = res
    n_counts, dfails, dnotes = check_declared_counts(sb_text, build_counts(report))
    n_body, bfails, bnotes = check_body_copy(sb_text, copy)

    out = {
        "run_dir": str(run),
        "claims_indexed": n_claims,
        "counts_checked": n_counts,
        "bodies_checked": n_body,
        "generated_blocks_skipped": blocks,
        "fails": cfails + dfails + bfails,
        "notes": cnotes + dnotes + bnotes,
    }
    out["verdict"] = "FAIL" if out["fails"] else "PASS"

    if args.json:
        print(json.dumps(out, indent=2))
    else:
        for f in out["fails"]:
            print("  FAIL: %s" % f)
        for n in out["notes"]:
            print("  note: %s" % n)
        print("plan_drift_check: %s -- %d claims indexed, %d declared counts "
              "checked, %d body quote(s) checked, %d drift(s)"
              % (out["verdict"], n_claims, n_counts, n_body, len(out["fails"])))
    return 1 if out["fails"] else 0


if __name__ == "__main__":
    sys.exit(main())
