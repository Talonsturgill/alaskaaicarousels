#!/usr/bin/env python3
"""aggregate_check.py -- re-derive every AGGREGATE number printed on a slide.

WHY THIS EXISTS
    Run 2026-08-02, slide 04 printed "FIVE STATE POSTINGS, 22 TO 31 JUL". It
    counted a federal Air Force industry day (C22, eielson.af.mil) as a state
    posting, and it contradicted slide 09 of the same deck, which said four.
    qa.py PASSED. copy_sync_check PASSED. claims_check PASSED. A pixel critic
    caught it by reading. The same run's fact-checker had already killed an
    "eight days" span for exactly this class of error, so the run knew the
    failure mode and shipped one into a render anyway.

    The general shape: EVERY on-slide string that aggregates verified claims
    into a NEW number -- a count, a span, a duration, a ratio -- is itself a
    fresh factual assertion. claims_check verifies that each claim has a
    source. copy_sync_check verifies that copy.json matches the render.
    NOTHING re-derived the arithmetic on top of them. This gate does.

WHAT IT DOES
    1. DETECT. Scans every rendered text node (render_report.json, which is
       what the browser actually laid out) for four aggregate shapes:
         count     "FOUR STATE POSTINGS", "Eight kinds", "TWO AIR FORCE NOTICES"
         duration  "21 DAYS", "TWO DAYS EARLIER", "three weeks"
         span      "27 TO 31 JUL"
         ratio     "0 OF 5 FOUND"
    2. REQUIRE a declaration for each detection in out/<date>/aggregates.json.
    3. RE-DERIVE the number from the declared claim ids and FAIL when the
       arithmetic disagrees with the printed string.
    4. CROSS-CHECK the deck against itself: two count declarations over the
       same subject with different numbers is the slide-04-vs-slide-09
       contradiction, and it fails whether or not either one is individually
       derivable.

DECLARATION FORMAT -- out/<date>/aggregates.json
    {"run_date": "2026-08-02", "aggregates": [
      {"kind": "count", "slide": 4, "text": "FOUR STATE POSTINGS, 27 TO 31 JUL",
       "subject": "state postings", "members": ["C16","C17","C18","C19"]},
      {"kind": "span", "slide": 4, "text": "FOUR STATE POSTINGS, 27 TO 31 JUL",
       "from": {"claim": "C16", "date": "2026-07-27"},
       "to":   {"claim": "C19", "date": "2026-07-31"}},
      {"kind": "duration", "slide": 4, "text": "21 DAYS",
       "from": {"claim": "C26", "date": "2026-08-02"},
       "to":   {"claim": "C21", "date": "2026-08-23"}},
      {"kind": "ratio", "slide": 6, "text": "0 OF 5 FOUND", "members": ["C05"],
       "items": ["artificial intelligence","machine learning",
                 "automated speech recognition","ASR","AI"], "found": []},
      {"kind": "from_claim", "slide": 5, "text": "3,967 acres at Eielson",
       "member": "C20"},
      {"kind": "design", "slide": 4, "text": "22 PX = 1 DAY",
       "note": "the deck's printed scale constant, a property of the artwork"}
    ]}

    Any entry may carry "fragment", the exact matched substring it answers for,
    which is how two aggregates inside one rendered string ("3,967 acres at
    Eielson. Four sites") stay independently checkable.

    kind semantics, and what each one has to survive:
      count      len(unique members) must equal the printed number, and every
                 member id must exist in claims.json. When the counted things
                 are enumerated INSIDE one claim, give "items" instead: the
                 item count must equal the printed number AND every item must
                 be findable in the member claims' text.
                 Plus SUBJECT/SOURCE COHERENCE: a count whose printed subject
                 says STATE may not include a federally-sourced claim, and one
                 that says FEDERAL may not include a State of Alaska one. That
                 is the 2026-08-02 defect, decidable from source_url alone.
                 Plus COUPLING: when a count and a span are printed in the same
                 string, the span's endpoints must be members of the count.
      duration   |to.date - from.date| in the printed unit must equal the
                 printed number, and each ISO date must actually appear in its
                 named claim.
      span       the two numbers printed in the string must be the day-of-month
                 of from.date and to.date, and any month token in the string
                 must match one of them.
      ratio      "A OF B" needs len(members) == B, len(found) == A, found a
                 subset of members.
      from_claim the number is NOT derived, it is quoted from ONE claim: the
                 number and the head noun must both be present in that claim's
                 text. Verified, not asserted.
      design     a property of the ARTWORK, not of the world (a printed scale,
                 a grid pitch). Not re-derived; requires a note and is reported
                 under NOT RE-DERIVED so a reader can audit the escape hatch.

KNOWN LIMITS (stated so nobody mistakes a pass for proof)
      - counts fire only at N >= 2. An aggregate of one thing is not an
        aggregation, and "one contract" would otherwise flood the report.
      - irregular plurals (people, children, criteria) are not detected.
      - duration matches are skipped inside a printed scale legend ("22 PX =
        1 DAY"), which is the only named exemption in the detector.
      - the gate proves the arithmetic, never the editorial judgement. A count
        of four correctly-listed members that are the wrong four members is
        still wrong, and that is what the fact-checker and the critics are for.
      - it applies to CLAIMS-BACKED decks. examples/demo-deck has no claims.json
        and is engine plumbing, so the gate correctly reports that it cannot
        re-derive anything there; do not run it as part of a demo-deck smoke.

USAGE
    python scripts/aggregate_check.py --run-dir out/<date>
    python scripts/aggregate_check.py --run-dir out/<date> \
        --render-report out/<date>/render/render_report.json

    Writes <run-dir>/aggregate_report.json.
    Exit 0 = PASS, 1 = FAIL, 2 = usage / unreadable input.

This script reads only. It never edits a slide, copy.json or claims.json.
"""

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

NUMWORD = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
           "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
           "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
           "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
           "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50}
_NUM = r"(?:\d[\d,]*|" + "|".join(sorted(NUMWORD, key=len, reverse=True)) + r")"

UNIT_DAYS = {"day": 1, "days": 1, "week": 7, "weeks": 7}
RX_DURATION = re.compile(r"(?i)\b(" + _NUM + r")\s+(days?|weeks?)\b")
RX_RATIO = re.compile(r"(?i)\b(\d+)\s+of\s+(\d+)\b")
RX_SPAN = re.compile(r"(?i)\b(\d{1,2})\s+to\s+(\d{1,2})\b")
RX_COUNT = re.compile(r"(?i)\b(" + _NUM + r")\s+((?:[a-z][a-z-]*\s+){0,2}[a-z][a-z-]*s)\b")
RX_SLIDE_COUNTER = re.compile(r"^\d{1,2}\s*/\s*\d{1,2}$")
RX_SCALE_LEGEND = re.compile(r"(?i)\bpx\s*=")

# Words that end in "s" without being a plural noun, so the count detector does
# not fire on "less time" or "this month".
STOP_PLURAL = set("""as is this its us was has does says gets goes across always
business less unless press class glass plus thus perhaps yes news series species
process access address progress witness illness bass gas mass pass loss boss
miss dismiss discuss focus bonus status campus virus census""".split())

MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7,
          "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}

# Host coherence. "FIVE STATE POSTINGS" shipped with a member sourced at
# eielson.af.mil. A count whose printed subject says STATE cannot be built out
# of federally-sourced claims, and vice versa, and that is decidable from the
# source_url alone.
RX_FEDERAL_HOST = re.compile(r"(?i)(\.mil$|\.mil\b|\bsam\.gov\b|\bsenate\.gov\b|"
                             r"\bhouse\.gov\b|\bcongress\.gov\b|\bwhitehouse\.gov\b|"
                             r"\bfederalregister\.gov\b|\bgsa\.gov\b|\bnoaa\.gov\b|"
                             r"\busgs\.gov\b|\bdoi\.gov\b|\bfaa\.gov\b|\bnsf\.gov\b)")
RX_STATE_HOST = re.compile(r"(?i)(\bstate\.ak\.us\b|\balaska\.gov\b|\bakleg\.gov\b|"
                           r"\b[a-z0-9.-]*\.ak\.us\b)")


# ---------------------------------------------------------------- utilities

def norm(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def parse_number(tok):
    t = (tok or "").strip().lower().replace(",", "")
    if t.isdigit():
        return int(t)
    return NUMWORD.get(t)


def singular(noun):
    n = (noun or "").lower().strip()
    if n.endswith("ies") and len(n) > 4:
        return n[:-3] + "y"
    if n.endswith("s") and not n.endswith("ss"):
        return n[:-1]
    return n


def parse_iso(s):
    try:
        return _dt.date(*[int(x) for x in str(s).strip()[:10].split("-")])
    except Exception:
        return None


def date_renderings(d):
    """Every spelling of an ISO date this house actually prints, so a declared
    endpoint can be proven to live inside its claim's own text."""
    mon_abbr = [k for k, v in MONTHS.items() if v == d.month][0]
    mon_full = _dt.date(d.year, d.month, 1).strftime("%B").lower()
    out = {
        "%04d-%02d-%02d" % (d.year, d.month, d.day),
        "%d/%d/%d" % (d.month, d.day, d.year),
        "%02d/%02d/%d" % (d.month, d.day, d.year),
        "%s %d, %d" % (mon_full, d.day, d.year),
        "%s %d %d" % (mon_full, d.day, d.year),
        "%s %d" % (mon_full, d.day),
        "%d %s %d" % (d.day, mon_abbr, d.year),
        "%d %s" % (d.day, mon_abbr),
        "%s %d" % (mon_abbr, d.day),
    }
    return {norm(x) for x in out}


# ---------------------------------------------------------------- detection

def rendered_strings(render_report):
    """[(slide_no, string)] for every rendered text node and canvas string."""
    out = []
    for s in render_report.get("slides", []):
        m = re.search(r"slide-(\d+)", s.get("file", ""))
        if not m:
            continue
        n = int(m.group(1))
        nodes = list(s.get("text_nodes") or [])
        for node in nodes:
            # render.py's node "lines" field holds LAYOUT RECTS, not strings;
            # the laid-out text is node["text"] (line breaks arrive as bare
            # concatenation, which is why the count detector ignores N < 2 and
            # a glued "documentprints" cannot fire).
            out.append((n, re.sub(r"\s+", " ", str(node.get("text", ""))).strip()))
        for c in (s.get("canvas_text") or []):
            txt = c.get("text", "") if isinstance(c, dict) else str(c)
            out.append((n, re.sub(r"\s+", " ", str(txt)).strip()))
    return out


def detect(strings):
    """Return [{slide, kind, fragment, text, n, ...}] aggregate assertions."""
    hits = []
    seen = set()
    for slide, text in strings:
        if not text or RX_SLIDE_COUNTER.match(text):
            continue
        spans = []  # (start, end) already claimed by a stronger kind

        def overlaps(m):
            return any(not (m.end() <= a or m.start() >= b) for a, b in spans)

        for m in RX_DURATION.finditer(text):
            if RX_SCALE_LEGEND.search(text):
                continue
            n = parse_number(m.group(1))
            if n is None:
                continue
            hits.append({"slide": slide, "kind": "duration", "fragment": m.group(0),
                         "text": text, "n": n, "unit": m.group(2).lower()})
            spans.append((m.start(), m.end()))
        for m in RX_RATIO.finditer(text):
            hits.append({"slide": slide, "kind": "ratio", "fragment": m.group(0),
                         "text": text, "n": int(m.group(1)), "of": int(m.group(2))})
            spans.append((m.start(), m.end()))
        for m in RX_SPAN.finditer(text):
            if overlaps(m):
                continue
            hits.append({"slide": slide, "kind": "span", "fragment": m.group(0),
                         "text": text, "from_n": int(m.group(1)), "to_n": int(m.group(2))})
            spans.append((m.start(), m.end()))
        for m in RX_COUNT.finditer(text):
            if overlaps(m):
                continue
            n = parse_number(m.group(1))
            noun = m.group(2).split()[-1].lower()
            if n is None or n < 2 or noun in STOP_PLURAL or len(noun) < 4:
                continue
            hits.append({"slide": slide, "kind": "count", "fragment": m.group(0),
                         "text": text, "n": n, "subject": m.group(2).lower()})
            spans.append((m.start(), m.end()))

    uniq = []
    for h in hits:
        key = (h["slide"], h["kind"], norm(h["fragment"]), norm(h["text"]))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(h)
    return uniq


# ------------------------------------------------------------ re-derivation

def claim_blob(claim):
    parts = [claim.get(k, "") for k in
             ("claim", "value", "verbatim", "date_of_source", "notes")]
    return norm(" ".join(str(p) for p in parts))


def check_endpoint(ep, claims, label, fails, where):
    """An endpoint is {claim, date}. The claim must exist and its own text must
    carry that date in some spelling, so an endpoint cannot be invented."""
    if not isinstance(ep, dict):
        fails.append("%s: '%s' is missing or malformed" % (where, label))
        return None
    cid = str(ep.get("claim", "")).strip()
    d = parse_iso(ep.get("date"))
    if d is None:
        fails.append("%s: %s.date %r is not an ISO date" % (where, label, ep.get("date")))
        return None
    if cid not in claims:
        fails.append("%s: %s.claim %r is not in claims.json" % (where, label, cid))
        return None
    blob = claim_blob(claims[cid])
    if not any(r in blob for r in date_renderings(d)):
        fails.append("%s: %s.date %s does not appear anywhere in claim %s "
                     "(%s). An endpoint has to come from its claim."
                     % (where, label, d.isoformat(), cid,
                        str(claims[cid].get("value", ""))[:60]))
        return None
    return d


def host_class(claim):
    url = str(claim.get("source_url", ""))
    if RX_STATE_HOST.search(url):
        return "state"
    if RX_FEDERAL_HOST.search(url):
        return "federal"
    return None


def check_items(items, members, claims, fails, where):
    """Each enumerated item has to be findable in the text of the claims the
    count rests on, so a list cannot grow an extra member on the slide."""
    blob = " ".join(claim_blob(claims[c]) for c in members if c in claims)
    for it in items:
        if norm(it) and norm(it) not in blob:
            fails.append("%s: item %r is not in the text of the declared claim(s) "
                         "%s, so the count includes something they do not say."
                         % (where, it, ", ".join(members) or "none"))


def verify(decl, claims, fails, warns):
    kind = decl.get("kind")
    where = "S%s %r [%s]" % (decl.get("slide", "?"), str(decl.get("text", ""))[:48], kind)
    # A declaration may name the exact FRAGMENT it covers, which is what gets
    # its arithmetic read, so two aggregates inside one rendered string
    # ("3,967 acres at Eielson. Four sites") stay independently checkable.
    text = str(decl.get("fragment") or decl.get("text", ""))

    if kind == "count":
        members = [str(x) for x in (decl.get("members") or [])]
        items = [str(x) for x in (decl.get("items") or [])]
        n = decl.get("n")
        if n is None:
            m = RX_COUNT.search(text)
            n = parse_number(m.group(1)) if m else None
        if n is None:
            fails.append("%s: no printed number found; give an explicit \"n\"" % where)
            return
        missing = [c for c in members if c not in claims]
        if missing:
            fails.append("%s: member(s) not in claims.json: %s" % (where, ", ".join(missing)))
        if items:
            # The counted things are enumerated INSIDE one or more claims.
            uniq_items = []
            for it in items:
                if it not in uniq_items:
                    uniq_items.append(it)
            if len(uniq_items) != n:
                fails.append("%s: prints %d but enumerates %d distinct item(s) (%s)"
                             % (where, n, len(uniq_items), ", ".join(uniq_items) or "none"))
            check_items(uniq_items, members, claims, fails, where)
            if not members:
                fails.append("%s: enumerated items need at least one member claim "
                             "they can be read out of" % where)
        else:
            uniq = sorted(set(members))
            if len(uniq) != n:
                fails.append("%s: prints %d but declares %d distinct member claim(s) "
                             "(%s). Re-derive the number or name the missing claim."
                             % (where, n, len(uniq), ", ".join(uniq) or "none"))
        # subject / source coherence
        subj = str(decl.get("subject") or text).lower()
        if re.search(r"(?<!united )\bstate\b", subj):
            for c in members:
                if c in claims and host_class(claims[c]) == "federal":
                    fails.append("%s: the printed subject says STATE but member %s is "
                                 "sourced federally (%s). This is the 2026-08-02 "
                                 "defect exactly." % (where, c, claims[c].get("source_url")))
        if re.search(r"\bfederal\b", subj):
            for c in members:
                if c in claims and host_class(claims[c]) == "state":
                    fails.append("%s: the printed subject says FEDERAL but member %s is "
                                 "sourced from the State of Alaska (%s)."
                                 % (where, c, claims[c].get("source_url")))

    elif kind == "duration":
        m = RX_DURATION.search(text)
        n = decl.get("n", parse_number(m.group(1)) if m else None)
        unit = decl.get("unit", (m.group(2).lower() if m else "days"))
        if n is None:
            fails.append("%s: no printed duration found; give an explicit \"n\"" % where)
            return
        a = check_endpoint(decl.get("from"), claims, "from", fails, where)
        b = check_endpoint(decl.get("to"), claims, "to", fails, where)
        if a is None or b is None:
            return
        days = abs((b - a).days)
        per = UNIT_DAYS.get(unit, 1)
        if days % per or days // per != n:
            got = days / per if days % per else days // per
            fails.append("%s: prints %d %s but %s to %s re-derives to %s %s"
                         % (where, n, unit, a.isoformat(), b.isoformat(), got, unit))

    elif kind == "span":
        a = check_endpoint(decl.get("from"), claims, "from", fails, where)
        b = check_endpoint(decl.get("to"), claims, "to", fails, where)
        if a is None or b is None:
            return
        m = RX_SPAN.search(text)
        if not m:
            fails.append("%s: no printed 'X TO Y' span found in the text" % where)
            return
        lo, hi = int(m.group(1)), int(m.group(2))
        if (lo, hi) != (a.day, b.day):
            fails.append("%s: prints %d TO %d but the declared endpoints are "
                         "%s and %s (days %d and %d)"
                         % (where, lo, hi, a.isoformat(), b.isoformat(), a.day, b.day))
        for tok in re.findall(r"(?i)\b(%s)\b" % "|".join(MONTHS), text):
            mon = MONTHS[tok.lower()]
            if mon not in (a.month, b.month):
                fails.append("%s: prints month %s but the endpoints are in %s and %s"
                             % (where, tok.upper(), a.isoformat()[:7], b.isoformat()[:7]))
        if b < a:
            fails.append("%s: declared span runs backwards (%s to %s)"
                         % (where, a.isoformat(), b.isoformat()))

    elif kind == "ratio":
        m = RX_RATIO.search(text)
        if not m:
            fails.append("%s: no printed 'A OF B' found in the text" % where)
            return
        a, b = int(m.group(1)), int(m.group(2))
        members = [str(x) for x in (decl.get("members") or [])]
        items = [str(x) for x in (decl.get("items") or [])]
        found = [str(x) for x in (decl.get("found") or [])]
        universe = items or members
        if len(set(universe)) != b:
            fails.append("%s: prints OF %d but declares %d distinct %s"
                         % (where, b, len(set(universe)), "item(s)" if items else "member(s)"))
        if len(set(found)) != a:
            fails.append("%s: prints %d found but declares %d"
                         % (where, a, len(set(found))))
        stray = [f for f in found if f not in universe]
        if stray:
            fails.append("%s: found entr(ies) not in the declared set: %s"
                         % (where, ", ".join(stray)))
        missing = [c for c in members if c not in claims]
        if missing:
            fails.append("%s: member(s) not in claims.json: %s" % (where, ", ".join(missing)))
        if items:
            if not members:
                fails.append("%s: enumerated items need at least one member claim "
                             "they can be read out of" % where)
            check_items(items, members, claims, fails, where)

    elif kind == "from_claim":
        cid = str(decl.get("member", decl.get("claim", ""))).strip()
        if cid not in claims:
            fails.append("%s: member %r is not in claims.json" % (where, cid))
            return
        blob = claim_blob(claims[cid])
        m = (RX_COUNT.search(text) or RX_DURATION.search(text) or RX_RATIO.search(text)
             or RX_SPAN.search(text))
        if not m:
            fails.append("%s: no number found in the text to verify" % where)
            return
        n = parse_number(m.group(1))
        wordforms = {str(n), "%d" % n} if n is not None else set()
        for w, v in NUMWORD.items():
            if n is not None and v == n:
                wordforms.add(w)
        if n is not None and not any(norm(w) in blob for w in wordforms):
            fails.append("%s: the number %s is not present in claim %s, so it is "
                         "not quoted from it. Use kind 'count'/'duration' and "
                         "declare the members it is derived from." % (where, n, cid))
        noun = None
        mc = RX_COUNT.search(text)
        if mc:
            noun = singular(mc.group(2).split()[-1])
        if noun and len(noun) >= 4 and norm(noun) not in blob:
            # A paraphrase ("kinds" for the claim's "classes") is legitimate, so
            # this is a warn: the NUMBER is the thing this gate proves.
            warns.append("%s: the noun %r does not appear in claim %s; check that "
                         "the number is being attached to what the claim actually "
                         "counts." % (where, noun, cid))

    elif kind == "design":
        note = str(decl.get("note", "")).strip()
        if len(note) < 20:
            fails.append("%s: kind 'design' opts a number out of re-derivation, so "
                         "it needs a real note saying why it is a property of the "
                         "artwork and not of the world" % where)

    else:
        fails.append("%s: unknown kind %r (count|duration|span|ratio|from_claim|design)"
                     % (where, kind))


def covers(decl, hit):
    """A declaration covers a detection when they sit on the same slide and the
    detected fragment is inside the declared string. 'design' and 'from_claim'
    cover any kind (they are the two ways of saying "this number is not derived
    from several claims"); every other kind must match the detected kind, so a
    count declaration can never quietly stand in for a span."""
    try:
        if int(decl.get("slide", -1)) != hit["slide"]:
            return False
    except (TypeError, ValueError):
        return False
    frag = decl.get("fragment")
    if frag:
        if norm(frag) != norm(hit["fragment"]):
            return False
    elif norm(hit["fragment"]) not in norm(decl.get("text", "")):
        return False
    if decl.get("kind") in ("design", "from_claim"):
        return True
    return decl.get("kind") == hit["kind"]


def cross_check(decls, fails):
    """Slide 04 said five state postings, slide 09 said four. Two counts over
    the same subject with different numbers is a contradiction inside one deck,
    and neither one has to be individually wrong for the deck to be."""
    by_subject = {}
    for d in decls:
        if d.get("kind") != "count":
            continue
        subj = norm(d.get("subject") or "")
        if not subj:
            continue
        n = d.get("n")
        if n is None:
            m = RX_COUNT.search(str(d.get("text", "")))
            n = parse_number(m.group(1)) if m else None
        if n is None:
            continue
        by_subject.setdefault(subj, []).append((n, d.get("slide"), sorted(set(d.get("members") or []))))
    # A count and a span printed in the SAME string describe the same set:
    # "FOUR STATE POSTINGS, 27 TO 31 JUL". The shipped 2026-08-02 defect put a
    # 22 JUL federal event on the span while the honest count held four state
    # postings, so the endpoints have to be members of the count.
    counts = [d for d in decls if d.get("kind") == "count"]
    for d in decls:
        if d.get("kind") != "span":
            continue
        for c in counts:
            if c.get("slide") != d.get("slide") or norm(c.get("text")) != norm(d.get("text")):
                continue
            members = set(str(x) for x in (c.get("members") or []))
            if not members:
                continue
            for label in ("from", "to"):
                ep = d.get(label) or {}
                cid = str(ep.get("claim", ""))
                if cid and cid not in members:
                    fails.append("COUPLING: S%s %r prints a count and a span in one "
                                 "string, but the span's %s endpoint %s is not one of "
                                 "the counted members (%s). The span has to run over "
                                 "the things being counted."
                                 % (d.get("slide"), str(d.get("text"))[:48], label, cid,
                                    ", ".join(sorted(members))))

    for subj, rows in by_subject.items():
        nums = {r[0] for r in rows}
        if len(nums) > 1:
            fails.append("CONTRADICTION: subject %r is counted as %s on slides %s. "
                         "One deck, one number." %
                         (subj, " and ".join(str(n) for n in sorted(nums)),
                          ", ".join(str(r[1]) for r in rows)))
        elif len(rows) > 1:
            sets = {tuple(r[2]) for r in rows}
            if len(sets) > 1:
                fails.append("CONTRADICTION: subject %r is counted %d on slides %s but "
                             "from different member claims %s."
                             % (subj, rows[0][0], ", ".join(str(r[1]) for r in rows),
                                " vs ".join(str(list(s)) for s in sets)))


# ------------------------------------------------------------------- driver

def run(run_dir, render_report_path=None, aggregates_path=None, claims_path=None):
    run_dir = Path(run_dir)
    rr_path = Path(render_report_path) if render_report_path else None
    if rr_path is None:
        for cand in (run_dir / "render" / "render_report.json", run_dir / "render_report.json"):
            if cand.exists():
                rr_path = cand
                break
    if rr_path is None or not rr_path.exists():
        return 2, {"error": "render_report.json not found under %s" % run_dir}
    ag_path = Path(aggregates_path) if aggregates_path else run_dir / "aggregates.json"
    cl_path = Path(claims_path) if claims_path else run_dir / "claims.json"

    try:
        rr = json.loads(rr_path.read_text())
    except (OSError, ValueError) as e:
        return 2, {"error": "cannot read %s: %s" % (rr_path, e)}
    claims = {}
    if cl_path.exists():
        try:
            cj = json.loads(cl_path.read_text())
            for c in cj.get("claims", []):
                claims[str(c.get("id"))] = c
        except ValueError as e:
            return 2, {"error": "cannot read %s: %s" % (cl_path, e)}

    hits = detect(rendered_strings(rr))
    fails, warns = [], []

    decls = []
    if ag_path.exists():
        try:
            aj = json.loads(ag_path.read_text())
        except ValueError as e:
            return 2, {"error": "cannot read %s: %s" % (ag_path, e)}
        decls = aj.get("aggregates", aj if isinstance(aj, list) else [])
        if not isinstance(decls, list):
            return 2, {"error": "%s: 'aggregates' must be a list" % ag_path}
    elif hits:
        # A check that cannot look is a FAIL, never a stale pass (the
        # caption_check --ledger precedent, 2026-07-2x).
        fails.append("DECLARATION: %d aggregate assertion(s) are printed on the "
                     "slides but %s does not exist. Every number a slide derives "
                     "from claims has to be declared and re-derivable."
                     % (len(hits), ag_path))

    if not claims and hits:
        fails.append("CLAIMS: %s not found, so no aggregate can be re-derived." % cl_path)

    used = [False] * len(decls)
    undeclared = []
    for h in hits:
        idx = [i for i, d in enumerate(decls) if isinstance(d, dict) and covers(d, h)]
        if not idx:
            if ag_path.exists():
                undeclared.append(h)
            continue
        for i in idx:
            used[i] = True
    for h in undeclared:
        fails.append("UNDECLARED %s on S%d: %r (in %r). An aggregate is a fresh "
                     "factual assertion; declare it in %s with the claims it is "
                     "derived from, or rewrite the slide."
                     % (h["kind"], h["slide"], h["fragment"], h["text"][:70], ag_path.name))
    for i, d in enumerate(decls):
        if not used[i] and isinstance(d, dict):
            warns.append("STALE declaration, no rendered string matches it: S%s %r [%s]"
                         % (d.get("slide", "?"), str(d.get("text", ""))[:50], d.get("kind")))

    for d in decls:
        if isinstance(d, dict):
            verify(d, claims, fails, warns)
        else:
            fails.append("DECLARATION: entry is not an object: %r" % (d,))
    cross_check([d for d in decls if isinstance(d, dict)], fails)

    not_rederived = [{"slide": d.get("slide"), "text": d.get("text"), "note": d.get("note")}
                     for d in decls if isinstance(d, dict) and d.get("kind") == "design"]

    rep = {
        "run_dir": str(run_dir),
        "render_report": str(rr_path),
        "aggregates_file": str(ag_path),
        "detected": len(hits),
        "declared": len(decls),
        "detections": hits,
        "not_rederived": not_rederived,
        "fails": fails,
        "warns": warns,
        "verdict": "FAIL" if fails else "PASS",
    }
    return (1 if fails else 0), rep


def main():
    ap = argparse.ArgumentParser(
        description="Re-derive every aggregate number printed on a slide.")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--render-report")
    ap.add_argument("--aggregates")
    ap.add_argument("--claims")
    ap.add_argument("--report", help="where to write aggregate_report.json "
                                     "(default <run-dir>/aggregate_report.json)")
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    args = ap.parse_args()

    code, rep = run(args.run_dir, args.render_report, args.aggregates, args.claims)
    if code == 2:
        print("aggregate_check: %s" % rep.get("error"), file=sys.stderr)
        return 2

    out = Path(args.report) if args.report else Path(args.run_dir) / "aggregate_report.json"
    try:
        out.write_text(json.dumps(rep, indent=2))
    except OSError as e:
        print("aggregate_check: cannot write %s: %s" % (out, e), file=sys.stderr)

    if args.json:
        print(json.dumps(rep, indent=2))
        return code
    for f in rep["fails"]:
        print("FAIL:", f)
    for w in rep["warns"]:
        print("warn:", w)
    for d in rep["not_rederived"]:
        print("not re-derived (design): S%s %r -- %s"
              % (d.get("slide"), d.get("text"), d.get("note")))
    print("aggregate_check: %s -- %d aggregate assertion(s) detected, %d declared -> %s"
          % (rep["verdict"], rep["detected"], rep["declared"], out))
    return code


if __name__ == "__main__":
    sys.exit(main())
