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

And (2026-08-19) it cross-checks the CONTACT-SHADOW PROMISE. qa.py has a
fitted contact gate -- known-bad dL 1.24, known-good dL 8.1, FAIL under 4.0 --
and it is OPT-IN, so a slide that never writes `data-contacts` is not judged
rather than judged clean. Run No.37 promised a contact shadow in writing in all
nine dossiers, declared it on four slides, and machine_qa reported no contacts
at all on the other five. Two of those five (03 and 06) had the shadow DRAWN in
their own canvas code and simply never declared it; the scorer then marked the
deck down for bare-plate bands and floating objects, and artwork craft was the
weakest criterion for the eighth time in eleven runs. A gate nobody is required
to point at the evidence is not a gate: if the plan promises a contact shadow,
the slide must declare where it is, so the measurement actually runs.

And (2026-08-29) it FAILS any <body> JSON declaration that does not parse:
data-contacts, data-scale, data-encodes. Run No.44's slide 05 wrote
`data-scale='[... "means":"2011, the method's publication (C22)" ...]'`, and
because the attribute is single-quote delimited the apostrophe closed it at
character 154 and truncated the JSON. qa.py logged the SyntaxError and warned,
this gate's contacts probe fell back to counting `"shadow"` substrings, and that
slide's two declared axes went unaudited for the entire run until a human read a
log. A gate a slide OPTS INTO and that then silently does not run is worse than
no gate: the record claims a check happened that did not. Caught here, it costs
a keystroke; caught after a render, it costs a round.

And (2026-09-07) it CROSS-CHECKS EVERY FIGURE IN THE PLANNED COPY AGAINST
claims.json, which is the one place a fact can enter a deck without anyone
noticing. brand.yaml has always said "every factual on-slide number/claim
carries a claim-id in the dossier" and nothing enforced it, because every gate
we own checks the claims that EXIST rather than the figures a dossier quotes:
claims_check verifies each claim has a source, aggregate_check re-derives
declared arithmetic, plan_drift compares the plan to the build. Run No.53's
slide 08 planned and printed "102 SIGNATURES" plus a 102-mark struck field on
the strength of a scout paragraph the first claims pass never turned into a
claim and never killed, and all three of those gates passed. It was found by
reading, during the Phase 8 pixel rounds, and verifying it late also CORRECTED
it (shareholders and descendants, an early-December snapshot, 20 non-shareholder
signatures excluded), which is three corrections that cost a re-render because
the check happened after the art.

And the same pass reads the claim's NOTES separately, because a number that
lives only there is not verified. The same run printed "1971" twice in mono on
its Alaska-facing frame for four scoring rounds; C35 verifies "3,400
shareholders at incorporation" and the year existed only in the fact-checker's
note as "consistent with 1971". It was almost certainly wrong (ANCSA was signed
in 1971, the regional corporations incorporated in 1972), it capped round 3, and
round 5 dropped a second inference of the same shape ("2019 JOINT ARTIFICIAL
INTELLIGENCE CENTER", where the JAIC-named contract in the record is a 2020
one). A note is the fact-checker reasoning. A claim is the fact-checker
verifying. Only the second may print.

A CITATION IS NOT A QUANTITY, though, and the first deck this ran on proved it:
`43 U.S.C. 1606(i)` was read as the figures 43 and 1606 and failed as
unverified, on a line whose claim was read at uscode.house.gov and whose SUBJECT
is that citation. A title and a section number are an address in a book, and so
are a CFR cite, a Federal Register volume and page, a public law number, an FCC
or FERC docket and a notice id, all of which this project prints routinely and
none of which is a measurement. They are recognised by SHAPE and blanked out of
BOTH sides before any number is read: out of the copy, so the gate does not ask
who verified a section number, and out of the claims, so a claim that merely
mentions a statute cannot make a bare 1606 a verified figure somewhere else in
the deck. Every other figure on the same line is still judged.

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
# Matched on WORD BOUNDARIES, not as substrings. Bare "ground" is deliberately
# not a hint: "bare ground" and "the ground plane is left flat" describe the
# empty lower band this gate exists to catch, and as a substring "ground" also
# passed on "background". The modeled ways of treating the ground are named
# explicitly (foreground, graded, relief, hillshade, terrain, contour,
# topograph), so a real modeled ground still clears while an empty one does not.
# Word boundaries also stop "lit" matching "quality"/"facility" and "3d"
# matching an id.
MODELED_HINTS = (
    "anchor", "terrain", "gradient", "graded", "foreground",
    "relief", "hillshade", "fog", "haze", "atmosphere", "shadow", "light",
    "lit", "texture", "grain", "stipple", "dither", "contour", "field",
    "particle", "mesh", "extrud", "depth", "render", "3d", "volumetric",
    "ramp", "wash", "glow", "mass", "silhouette", "topograph", "noise",
    "leader line", "annotation furniture", "scale bar", "tick",
)
_MODELED_RE = re.compile(
    "|".join(r"(?<![a-z])" + re.escape(h) + r"(?![a-z])" for h in MODELED_HINTS))
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
# Any top-level heading (# or ##, never ###+). A dossier's own fields are ###
# and deeper, so this only ever finds where the DECK starts talking again.
TOP_HEAD_RE = re.compile(r"^#{1,2}(?!#)[ \t]+\S.*$", re.M)
# THE EMPHASIS MAY OPEN BEFORE THE NUMBER (2026-08-19). The pattern demanded the
# "4a" sit OUTSIDE the bold, i.e. `4a. **Lower-third treatment.**`, and run No.37
# wrote all nine dossiers as `**4a. Lower-third treatment.**`, which is the same
# field with the asterisks one word earlier and is what SLIDE_DOSSIER_SPEC's own
# line 34 looks like when an author bolds the whole label. Every dossier failed
# with "no field 4a", the least informative failure this gate can produce, and it
# cost a full authoring pass to re-format nine paragraphs that were already
# correct. Leading `**` or `__` is now consumed before the number. This does not
# soften anything: a field the gate cannot FIND is a blanket fail, and finding it
# is what subjects it to the thinness and modeled-tone tests that are the actual
# gate.
F4A_RE = re.compile(
    r"^\s*(?:\*{1,2}|_{1,2})?\s*4a[.)]?\s*\*{0,2}\s*Lower[- ]third treatment"
    r"\s*[.:-]?\s*\*{0,2}\s*[.:-]?\s*(.*)$",
    re.I | re.M)


# A CONTACT SHADOW PROMISED IN WRITING MUST BE DECLARED IN THE MARKUP.
# Matched on the dossier body only (the deck-level preamble above "## SLIDE 01"
# is never read), so a header sentence about the deck's depth language does not
# put nine slides on the hook.
CONTACT_PROMISE_RE = re.compile(r"contact[- ]shadow|two[- ]part shadow", re.I)
BODY_TAG_RE = re.compile(r"<body\b[^>]*>", re.I | re.S)
DATA_CONTACTS_RE = re.compile(r"data-contacts\s*=\s*(['\"])(.*?)\1", re.I | re.S)

# EVERY JSON DECLARATION ON <body>, NOT JUST THE ONE THIS GATE GREW UP AROUND
# (2026-08-29). qa.py fails an unparseable declaration, but only after a render,
# and run No.44 paid three revision rounds on a deck whose slide 05 carried
#   data-scale='[... "means":"2011, the method's publication (C22)" ...]'
# The attribute is single-quote delimited, so the apostrophe closed it at
# character 154 and truncated the JSON; the axis census never ran on that slide
# all run. This gate already reads the built slide sources, so it can say so
# before a render round is spent. The regex ends an attribute at its own
# delimiter exactly as an HTML parser does, so it sees the same truncated text
# the browser sees.
BODY_JSON_ATTRS = ("data-contacts", "data-scale", "data-encodes")

# A DECLARATION ON THE RIGHT SURFACE AT THE WRONG TIME (2026-09-09). render.py
# reads the LIVE dom after renderReady resolves, so a slide that ends its draw
# with document.body.setAttribute('data-contacts', ...) is measured by qa.py
# exactly as if the attribute had been in the markup. This gate reads the body
# TAG out of the source file, because it is meant to run BEFORE any render, and
# it is blind to a runtime write. Run No.54 set the attribute that way on slides
# 02, 04, 07 and 10: the render report carried their contacts, qa.py measured
# them, and this gate failed all four for "declaring nothing". Both tools were
# right about their own surface and nothing told the author which one wanted
# what. So the runtime write is now NAMED, and the remedy is one edit.
# The JSON parse check above is blind to it as well, which matters more: a
# malformed runtime declaration is not caught until a render has been spent.
_DATASET_KEY = {"data-contacts": "contacts", "data-scale": "scale",
                "data-encodes": "encodes"}
RUNTIME_SET_RE = {
    a: re.compile(
        r"setAttribute\s*\(\s*['\"]%s['\"]" % re.escape(a)
        + r"|dataset\s*\.\s*%s\s*=[^=]" % k
        + r"|dataset\s*\[\s*['\"]%s['\"]\s*\]\s*=[^=]" % k, re.I)
    for a, k in _DATASET_KEY.items()}

# json.dumps(..., separators=(',', ' ')) WRITES A SPACE WHERE THE KEY SEPARATOR
# BELONGS (2026-09-09). It emits {"what" "x"} and json.loads answers
# "Expecting ':' delimiter", which reads like a hand-typing slip rather than
# like the one-character argument it is. Run No.54 put it into four
# data-contacts attributes in a single generation pass, and it was only findable
# because a gate printed the tail of the attribute it could not parse. The right
# call is separators=(',', ':').
SEPARATOR_HINT = (
    " The error is 'Expecting :' and the attribute has a SPACE where the key "
    "separator belongs, which is what json.dumps(..., separators=(',', ' ')) "
    "emits -- the second element of that tuple is the KEY separator, not a "
    "space to pad with. Write separators=(',', ':').")


def attr_raw(body_tag, attr):
    """The raw text of a body attribute, or None if it is not there."""
    m = re.search(r"%s\s*=\s*(['\"])(.*?)\1" % re.escape(attr),
                  body_tag, re.I | re.S)
    return m.group(2) if m else None


def declaration_parse_fails(no, src):
    """FAIL lines for any <body> JSON declaration on this slide that does not
    parse. A declaration a slide OPTS INTO and that then silently does not run
    is worse than no declaration, because the record claims a check happened."""
    out = []
    b = BODY_TAG_RE.search(src)
    if not b:
        return out
    for attr in BODY_JSON_ATTRS:
        raw = attr_raw(b.group(0), attr)
        if raw is None:
            continue
        try:
            json.loads(raw)
        except Exception as e:
            sep = SEPARATOR_HINT if "Expecting ':' delimiter" in str(e) else ""
            out.append(
                f"slide {no:02d}: {attr} does not parse as JSON ({e}), so the "
                "gate it feeds runs on nothing and reports nothing while the "
                f"slide's row still prints. The attribute reads {raw[-40:]!r} "
                "at its end. The usual cause is an apostrophe inside a "
                "single-quoted attribute (\"the method's publication\"), which "
                "ends the attribute early and truncates the JSON: write it as "
                "&#39; or spell the prose without it. Fix the declaration or "
                "delete it, but do not leave a check that only looks like it ran"
                + sep)
    return out


def runtime_declarations(src):
    """Which body-JSON contracts this slide writes at RUNTIME instead of putting
    in the markup. See RUNTIME_SET_RE for why that splits this gate from qa.py.
    An attribute present on the <body> tag is never reported, whatever else the
    script does to it: this gate can read it, which is the whole point."""
    b = BODY_TAG_RE.search(src)
    tag = b.group(0) if b else ""
    return [a for a in BODY_JSON_ATTRS
            if attr_raw(tag, a) is None and RUNTIME_SET_RE[a].search(src)]


def runtime_warn(runtime):
    """ONE deck-level line for every contract written at runtime, not one per
    slide. Measured over three shipped decks this fires on most slides of most
    of them (10 declarations across 8 slides in run No.54, 8 across 7 in
    No.53), and a warn that prints on nearly every row is wallpaper. The
    aggregate keeps every location and costs one line."""
    named = [f"slide {no:02d} {a}" for no in sorted(runtime) for a in runtime[no]]
    if not named:
        return []
    return ["%d body declaration(s) are set at RUNTIME (setAttribute or "
            "dataset) rather than on the <body> tag: %s. render.py reads the "
            "LIVE dom after renderReady, so qa.py DOES measure them and the "
            "render report carries them -- but this gate reads the body TAG out "
            "of the source, so it is blind to them, and so is its JSON parse "
            "check, which means a malformed declaration does not surface until "
            "a render round has been spent. Both tools are right about their "
            "own surface. A static attribute, <body data-contacts='[...]'>, is "
            "the one surface both can read." % (len(named), ", ".join(named))]

DECLARE_HOWTO = (
    "Declare it so qa.py's fitted contact gate can measure it: "
    "<body data-contacts='[{\"what\":\"<the object standing on the plate>\","
    "\"shadow\":[[x,y,w,h]],\"ground\":[[x,y,w,h]]}]'>, rects in design px, "
    "the ground rect on the SAME plate a little clear of the shadow. If the "
    "slide has no object standing on anything, strike the promise from the "
    "dossier instead -- but do not leave the plan saying one thing and the "
    "markup saying nothing, which is how five of run No.37's nine slides "
    "skipped the check entirely")


def contacts_declared(src):
    """How many contact regions a slide's <body> declares. None if it declares
    no attribute at all; -1 if the attribute is there but carries no shadow;
    -2 if the attribute is there and does not parse."""
    b = BODY_TAG_RE.search(src)
    if not b:
        return None
    m = DATA_CONTACTS_RE.search(b.group(0))
    if not m:
        return None
    raw = m.group(2)
    try:
        val = json.loads(raw)
    except Exception:
        # WAS A SUBSTRING COUNT UNTIL 2026-08-29, and that was the same silent
        # skip this file exists to prevent: counting `"shadow"` in truncated
        # text let a malformed declaration satisfy the promise check, so the
        # dossier's promise was "kept" by markup no measurement could read.
        # -2 is its own fail, raised by declaration_parse_fails().
        return -2
    if isinstance(val, dict):
        val = [val]
    if not isinstance(val, list) or not val:
        return -1
    n = sum(1 for e in val if isinstance(e, dict) and e.get("shadow"))
    return n or -1


def slide_sections(text):
    """Split the storyboard into (slide_no, heading, body) dossier sections.

    THE LAST DOSSIER ENDS WHERE THE DECK RESUMES (2026-08-26). Every section but
    the last was bounded by the next "## SLIDE NN"; the last one ran to end of
    file, so ANY deck-level section written after the final slide was read as
    part of that slide's dossier. Run No.41 put a BUILD RECONCILIATION section
    at the foot of its storyboard, describing the contact-shadow repairs made
    across the deck, and slide 09 failed for promising a contact shadow it never
    promised: the gate was reading the deck's prose as slide 09's plan. The
    showrunner worked around it by moving the section above "## SLIDE 01",
    which fixes the symptom by rearranging the author's document.
    A dossier now also ends at the next TOP-LEVEL heading that is not a slide,
    so the tail of a storyboard belongs to the deck again. This tightens the
    gate rather than loosening it: less text is attributed to a slide, and text
    that is genuinely inside a dossier (### and #### subheadings, which is how
    the dossier spec's own fields are written) is untouched.
    """
    heads = list(HEAD_RE.finditer(text))
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        for t in TOP_HEAD_RE.finditer(text, m.end(), end):
            if not HEAD_RE.match(t.group(0)):
                end = t.start()
                break
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


# --- EVERY FIGURE IN THE PLANNED COPY, AGAINST claims.json (2026-09-07) ------
# The field is the dossier's COPY block, the unit is a backticked string, which
# is how SLIDE_DOSSIER_SPEC has the house quote the copy that will print, and
# the token is a number NOT flanked by letters or digits, so a PIID
# (140D0419C0047), a task order (70CDCR26FR0000034) and a docket number are
# never shredded into fragments that mean nothing.
COPY_FIELD_RE = re.compile(
    r"^\s*(?:\*{1,2}|_{1,2})?\s*2[.)]?\s*\*{0,2}\s*COPY\b", re.I | re.M)
NEXT_FIELD_RE = re.compile(
    r"^\s*(?:\*{1,2}|_{1,2})?\s*(?:2[a-z]|3)[.)]", re.I | re.M)
QUOTED_RE = re.compile(r"`([^`]*)`")
NUM_RE = re.compile(r"(?<![A-Za-z0-9])\$?\d[\d,]*(?:\.\d+)?%?(?![A-Za-z0-9])")
# A drawn dimension is a property of the artwork, not an assertion about Alaska.
DESIGN_UNIT_RE = re.compile(r"^\s*(px|pt|deg|em|rem|ch|vw|vh)\b", re.I)
# FIXED FURNITURE CARRIES THE DECK'S OWN GEOMETRY, NOT THE STORY'S FACTS. The
# rail's coordinates, its t value, its arc distance and the progress counter are
# computed from the composition and belong to no claim; they are also the one
# thing on the frame no dossier's acceptance checklist owns. Matched on the
# bullet's LABEL, the text before the colon, so it exempts a line and never a
# document.
FURNITURE_WORD_RE = re.compile(
    r"\b(rail|counter|progress|footer|provenance|coordinates?|slug|wordmark"
    r"|kicker|plate number|page number|site fixture)\b", re.I)
# The author's escape hatch, and it is a declaration rather than a silence: the
# number is a property of the drawing (a printed scale key, a dot-to-people
# ratio). aggregate_check demands the same thing again at build time, in
# aggregates.json, with the same word.
DESIGN_TAG_RE = re.compile(r"\[design\]", re.I)
# Two quoted strings that are never a factual assertion, matched on their whole
# shape so nothing wider is exempted: the progress counter ("05 / 09"), which is
# the deck's own pagination, and a variable-font axis setting ("wdth 88 wght
# 700"), which is a type spec that happens to sit in backticks.
COUNTER_ONLY_RE = re.compile(r"^\s*\d{1,2}\s*/\s*\d{1,2}\s*$")
FONT_AXIS_RE = re.compile(
    r"^\s*(?:(?:wdth|wght|opsz|slnt|ital|GRAD|CASL|MONO)\s+-?[\d.]+\s*)+$", re.I)

# A CITATION IS NOT A QUANTITY (2026-09-07, the same day, from the showrunner's
# first use of this gate). `43 U.S.C. 1606(i)` was read as the figures 43 and
# 1606 and failed as unverified, on a line whose claim C31 was read at
# uscode.house.gov and whose SUBJECT is that citation. A title number and a
# section number are addresses in a book; so are a CFR cite, a public law
# number, a FERC docket like P-15423-000 and a notice id, all of which this
# project prints routinely and none of which is a measurement. They are
# recognised by SHAPE and blanked out of the string before any number is read,
# so every other figure on the same line is still judged: a bare number is never
# skipped merely because a claim nearby mentions a statute.
CITATION_RES = (
    # 43 U.S.C. 1606(i)(1)(A), 43 USC 1606, 25 U.S.C. 3601
    re.compile(r"\b\d+\s*U\.?\s?S\.?\s?C\.?\s*(?:§+\s*)?\d[\w().\-]*", re.I),
    # 18 CFR 385.2010, 43 C.F.R. 2650.5
    re.compile(r"\b\d+\s*C\.?\s?F\.?\s?R\.?\s*(?:§+\s*)?\d[\w().\-]*", re.I),
    # 91 FR 55826, the Federal Register's volume and page
    re.compile(r"\b\d+\s*F\.?\s?R\.?\s+\d[\d,]*", re.I),
    # Public Law 92-203, Pub. L. No. 92-203
    re.compile(r"\b(?:public\s+law|pub\.?\s*l\.?(?:\s*no\.?)?)\s*\d+\s*-\s*\d+", re.I),
    # P-15423-000, EL24-1-000: a letter prefix bound to a number by a hyphen
    re.compile(r"\b[A-Z]{1,4}-\d[\d\-]*"),
    # WC 26-173, WT 17-310: an FCC-style bureau prefix, docket, year and number.
    # The two-digit lead and the hyphen are required, so a spelled range ("22 TO
    # 31") and a unit ("43 MW", which this house writes unit-last) cannot match.
    re.compile(r"\b[A-Z]{2,3}\s\d{2}-\d{1,4}\b"),
    # docket 22-1, id 224879, PIID W519TC26CA019, FR Doc 2026-12345
    re.compile(r"\b(?:docket|piid|rin|fr\s+doc|solicitation|notice\s+id|case\s+no"
               r"|id)\b\.?\s*(?:no\.?\s*)?(?=[\w.\-/]*\d)[\w.\-/]+", re.I),
)


def strip_citations(s):
    """Blank every citation or identifier span, leaving the rest measurable."""
    for rx in CITATION_RES:
        s = rx.sub(" ", s)
    return s


def copy_field(body):
    """The dossier's COPY block, or None."""
    m = COPY_FIELD_RE.search(body)
    if not m:
        return None
    rest = body[m.end():]
    n = NEXT_FIELD_RE.search(rest)
    return rest[:n.start()] if n else rest


def num_tokens(s):
    """(printed, normalised) for every number token in a string."""
    out = []
    for m in NUM_RE.finditer(s):
        raw = m.group(0)
        if DESIGN_UNIT_RE.match(s[m.end():]):
            continue                       # 42px, 24pt: a drawn dimension
        out.append((raw, raw.strip("$%").replace(",", "").rstrip(".")))
    return out


def claim_figures(claims):
    """(verified, noted): every number the claims carry, split by WHERE it lives.

    claim/value/verbatim are the fact-checker's verification. notes are the
    fact-checker's reasoning, and reasoning is not a source."""
    verified, noted = set(), {}
    for c in claims:
        cid = c.get("id", "?")
        # Citations are blanked on THIS side too, so that a claim which merely
        # mentions 43 U.S.C. 1606(i) cannot make a bare 1606 a verified figure
        # somewhere else in the deck.
        for f in ("claim", "value", "verbatim"):
            for _, n in num_tokens(strip_citations(str(c.get(f) or ""))):
                verified.add(n)
        for _, n in num_tokens(strip_citations(str(c.get("notes") or ""))):
            noted.setdefault(n, []).append(cid)
    return verified, noted


def figure_fails(no, body, verified, noted, run_date=""):
    """FAIL lines for figures in this dossier's planned copy that no claim
    verifies. Silent when there is no COPY block to read (field 2 is checked by
    the storyboard gate itself, and a missing one is not this check's finding)."""
    fails = []
    block = copy_field(body)
    if not block:
        return fails
    seen = set()
    for line in block.splitlines():
        label = line.split("`", 1)[0]
        if FURNITURE_WORD_RE.search(label) or DESIGN_TAG_RE.search(line):
            continue
        # ONE FINDING PER LINE. A statute citation is two numbers and one fact
        # ("43 U.S.C. 1606(i)"), and three messages about one line of copy read
        # like three defects.
        nowhere, from_notes = [], {}
        for q in QUOTED_RE.findall(line):
            if COUNTER_ONLY_RE.match(q) or FONT_AXIS_RE.match(q):
                continue
            if run_date:
                q = q.replace(run_date, " ")   # the provenance stamp, not a fact
            q = strip_citations(q)             # an address in a book, not a figure
            for raw, n in num_tokens(q):
                if n in verified or n in seen:
                    continue
                seen.add(n)
                if n in noted:
                    from_notes[raw] = noted[n]
                else:
                    nowhere.append(raw)
        if from_notes:
            cites = sorted({c for v in from_notes.values() for c in v})
            fails.append(
                f"slide {no:02d}: the planned copy prints "
                f"{', '.join(from_notes)} and no claim VERIFIES that figure -- "
                f"it appears only in the NOTES of {', '.join(cites)}, which is "
                f"the fact-checker reasoning rather than the fact-checker "
                f"verifying ({line.strip()[:80]!r}). Run No.53 printed 1971 "
                f"twice in mono off a note reading 'consistent with 1971' and "
                f"was probably wrong, because ANCSA was signed in 1971 and the "
                f"regional corporations incorporated in 1972. Either verify it "
                f"as its own claim or print what the claim carries")
        if nowhere:
            fails.append(
                f"slide {no:02d}: the planned copy prints {', '.join(nowhere)} "
                f"and NO claim in claims.json carries that figure at all "
                f"({line.strip()[:80]!r}). Every factual on-slide number carries "
                f"a claim-id (brand.yaml). Verify it as a claim before the art "
                f"is built, kill the line, or -- if it is a property of the "
                f"drawing rather than of the world -- mark the bullet [design], "
                f"which aggregates.json will have to say again at build time")
    return fails


def check_slide(no, heading, body, breather_attr, contacts=None, built=False,
                runtime=()):
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
        elif not _MODELED_RE.search(low):
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

    # THE CONTACT-SHADOW PROMISE. One-directional on purpose: data-breather
    # DISABLES a gate, so it is policed both ways, while data-contacts ENABLES
    # one, so declaring a shadow the dossier never mentioned is a gain and is
    # not flagged. Only checked once the slide sources exist; before the build
    # there is nothing to point at.
    if built and CONTACT_PROMISE_RE.search(body):
        if contacts is None and "data-contacts" in (runtime or ()):
            # NOT "declares nothing". The slide declares it at runtime, qa.py
            # measures it, and only this gate cannot see it. Saying the wrong
            # thing here cost run No.54 four rows of a first-pass failure on
            # four slides that were correct.
            fails.append(
                f"slide {no:02d}: the dossier promises a contact shadow and the "
                "slide DOES declare data-contacts, but it sets it at RUNTIME "
                "(setAttribute or dataset) rather than on the <body> tag. qa.py "
                "reads the live dom and measures it; this gate reads the body "
                "tag in the source and cannot. Move the declaration into the "
                "markup as a static attribute and both tools read the same "
                "thing. Nothing about the rects needs to change")
        elif contacts is None:
            fails.append(
                f"slide {no:02d}: the dossier promises a contact shadow and the "
                "slide body declares no data-contacts, so qa.py's contact gate "
                f"never looks at this slide and reports nothing. {DECLARE_HOWTO}")
        elif contacts == -1:
            fails.append(
                f"slide {no:02d}: the slide body carries data-contacts with no "
                "shadow region in it, which measures nothing. "
                f"{DECLARE_HOWTO}")
        # contacts == -2 (the declaration does not parse) is reported once, by
        # declaration_parse_fails(), with the byte the parser stopped on.
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
    contacts = {}
    parse_fails = {}
    runtime = {}
    built = set()
    if sdir.is_dir():
        for p in sdir.glob("slide-*.html"):
            m = re.search(r"slide-(\d+)", p.name)
            if m:
                src = p.read_text(errors="replace")
                b = BODY_TAG_RE.search(src)
                n = int(m.group(1))
                attrs[n] = bool(b and "data-breather" in b.group(0))
                contacts[n] = contacts_declared(src)
                parse_fails[n] = declaration_parse_fails(n, src)
                runtime[n] = runtime_declarations(src)
                built.add(n)

    # THE CLAIMS THE COPY LEANS ON. Read here rather than in check_slide so a
    # run with no claims.json yet (this gate is also run standalone, and on old
    # decks) says so once instead of judging nine dossiers against nothing.
    verified, noted, claims_note = set(), {}, None
    cj = rdir / "claims.json"
    run_date = ""
    if cj.exists():
        try:
            doc = json.loads(cj.read_text())
            verified, noted = claim_figures(doc.get("claims") or [])
            run_date = str(doc.get("run_date") or "")
        except Exception as e:
            claims_note = ("claims.json did not parse (%s), so the figure "
                           "cross-check did not run" % e)
    else:
        claims_note = ("no claims.json beside the storyboard, so the figure "
                       "cross-check did not run")

    out = {"slides": [], "fails": 0, "warns": 0}
    seen = set()
    for no, heading, body in sections:
        seen.add(no)
        f, w = check_slide(no, heading, body, attrs.get(no),
                           contacts.get(no), no in built, runtime.get(no, ()))
        # An unparseable declaration is a fail whether or not the dossier
        # promised anything, so it is merged in outside check_slide().
        f = parse_fails.get(no, []) + f
        if no == sections[0][0]:
            w = runtime_warn({k: v for k, v in runtime.items() if v}) + w
        if claims_note is None:
            f = f + figure_fails(no, body, verified, noted, run_date)
        elif no == sections[0][0]:
            w = w + [claims_note]
        out["slides"].append({"slide": no, "fails": f, "warns": w})
        out["fails"] += len(f)
        out["warns"] += len(w)
    # A BUILT SLIDE WITH NO DOSSIER STILL GETS ITS DECLARATIONS READ, so a
    # numbering mismatch can't hide a truncated attribute.
    for n in sorted(built - seen):
        if parse_fails.get(n):
            out["slides"].append({"slide": n, "fails": parse_fails[n], "warns": []})
            out["fails"] += len(parse_fails[n])
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
