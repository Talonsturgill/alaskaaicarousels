#!/usr/bin/env python3
"""copy_sync_check.py -- catch the record-sync gap between copy.json and the
shipped render.

WHY THIS EXISTS
    During pixel/flow review the showrunner sometimes edits display text
    directly in a slide's HTML (a kicker, a headline, a tag, a label) and
    forgets to sync copy.json back to it. copy.json then goes stale and the
    only thing that notices is the scorer's transcription pass, late in the
    run. Run 2026-07-17: slide-05's kicker was hand-edited "HOW IT STARTED"
    -> "BEFORE THE CLASS" in the HTML but copy.json still said "HOW IT
    STARTED" until the scorer caught it. There was no machine check.

WHAT IT DOES
    For every slide string in copy.json["slides"], verify that the string is
    actually present in that slide's RENDERED text (render_report.json's
    per-slide text_nodes[].text, which is what the browser laid out).

    copy.json["slides"] is accepted in EITHER shape: a dict keyed "S1".."S9"
    (the record form) OR a list of per-slide objects (the copywriter / Phase 6
    form, each item carrying an integer "n" slide number plus kicker/headline/
    body/labels/chips/claim_ids). A list is normalized to the "S<n>" dict keyed
    on each item's "n" field (falling back to 1-based position when "n" is
    absent) BEFORE any comparison, so the exact same one-directional check runs
    on both shapes. This normalization changes no matching logic; it only lets
    the guard run on the real artifact instead of crashing on slides.items().

    The check is
    one-directional by design: every authored slide string must appear in the
    render (copy must not go stale). It does NOT require every rendered node
    to appear in copy (decorative micro-text, coordinates, and progress
    counters live only in the HTML and would be noise).

MATCHING
    Comparison is on letters+digits only (case-insensitive, punctuation and
    whitespace ignored) so straight-quote / spacing / slash-spacing
    differences never trip it. render.py stores each node's text truncated to
    the first 80 characters (.slice(0,80)); to tolerate that truncation for
    long body prose, strings longer than the prefix window are matched on
    their leading WINDOW (default 40) alphanumeric characters. Short display
    strings -- exactly the record-sync risk class -- are matched in full. A
    string is satisfied if its needle appears in its own slide's rendered
    blob OR anywhere in the deck's rendered blob.

    A MATCH IS AGAINST ONE ELEMENT'S OWN STRING (2026-08-27). See build_nodes:
    the per-slide blob used to be the alnum-join of every node's `text` and
    every entry of its `texts`, which manufactured strings no element carried
    and passed four shredded labels in one round. Each candidate string is now
    searched whole. Presence still cannot see a TRUNCATED string, because a
    truncated string is present, so the 80-character paste is caught by its own
    signature instead; see the truncation block in check().

    THE BLOB IS BUILT FROM `texts` AS WELL AS `text` (2026-08-16). An element
    holding several lines (three fact lines separated by <br>) recorded its
    whole content JOINED and cut at 80 characters, so any line beginning past
    that cut was invisible here and reported missing although it was on the
    page. Run No.35's slide 09 hit exactly that and worked around it by
    splitting the div into three elements. render.py now also records `texts`,
    each direct text node on its own at 200 characters, and both fields feed
    the blob. This widens what the check can SEE; it relaxes no matching rule.

EXIT CODES
    0  every authored slide string is present in the render (in sync)
    1  one or more authored slide strings are missing from the render (stale)
    2  usage / missing-file error

This script reads only; it never edits copy.json or any slide. It is a
pre-ship tripwire, not a gate that can be weakened. Fix a reported mismatch
by reconciling copy.json to the shipped render (or vice versa) before ship.
"""

import argparse
import json
import re
import sys

WINDOW = 40

# Keys that hold metadata / bookkeeping, never rendered slide text.
SKIP_KEYS = {"note", "beat", "claim_ids", "claim_id", "words", "lines"}


def alnum(s):
    return re.sub(r"[^A-Z0-9]", "", s.upper())


def collect(obj, path):
    """Yield (dotted_path, string) for every rendered-text leaf under a slide,
    skipping metadata keys and the redundant 'lines' mirrors of a parent
    .text field."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in SKIP_KEYS:
                continue
            out += collect(v, path + "." + k if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += collect(v, "%s[%d]" % (path, i))
    elif isinstance(obj, str):
        if re.search(r"[A-Za-z]", obj):
            out.append((path, obj))
    return out


def normalize_slides(raw):
    """Return copy.json['slides'] as a dict keyed 'S<n>' regardless of shape.

    A dict is returned unchanged (the record form). A list (the copywriter /
    Phase 6 form) is keyed by each item's integer 'n' slide number, falling
    back to 1-based position when 'n' is absent or non-numeric. Anything else
    yields an empty dict. Non-rendered bookkeeping fields (claim_ids etc.) are
    left in place; collect() already skips them, so they never cause a miss."""
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, list):
        out = {}
        for i, item in enumerate(raw):
            key = None
            if isinstance(item, dict):
                n = item.get("n")
                if isinstance(n, bool):
                    n = None
                if isinstance(n, int):
                    key = "S%d" % n
                elif isinstance(n, str) and n.strip().isdigit():
                    key = "S%d" % int(n.strip())
            if key is None:
                key = "S%d" % (i + 1)
            out[key] = item
        return out
    return {}


def slide_index(fname):
    m = re.search(r"slide-(\d+)", fname)
    return int(m.group(1)) if m else None


def node_strings(n):
    """Every string this ONE element can honestly be said to carry.

    `full` (2026-08-27) is the element's whole one-line textContent at 400
    characters, spans included, and it is the one that is actually what a
    reader sees. `text` is the same thing cut at 80 and `texts` is its DIRECT
    text children only, so a <span> wrapping a unit is missing from every entry
    of it. Both are still offered as candidates, because a report written
    before `full` existed has to keep checking.
    """
    out = [n.get("full") or "", n.get("text") or ""]
    out.extend(n.get("texts") or [])
    return [t for t in out if t]


def build_nodes(render_report):
    """Return (per_slide_candidates_by_Skey, whole_deck_candidates).

    ONE NODE AT A TIME, NOT ONE BLOB PER SLIDE (2026-08-27). This used to
    alnum-join every node's `text` AND every entry of its `texts` into a single
    per-slide string and search that. Joining is what made the gate blind to a
    SHREDDED string: run No.42 rebuilt copy.json out of `texts`, which dropped
    the <span> holding a unit, and the label "1 DOT = 0.1 g OF SILVER IODIDE"
    became "1 DOT = 0.1OF SILVER IODIDE" -- a string that was never on the page
    and that the gate nonetheless found, because the space-join of the same two
    `texts` entries it came from was sitting in the blob. Four labels shipped
    that way through a PASS. A candidate list keeps each string whole, so a
    match now means one element really carries those words.
    """
    per_slide = {}
    deck = []
    for s in render_report.get("slides", []):
        idx = slide_index(s.get("file", ""))
        if idx is None:
            continue
        cands = []
        for n in s.get("text_nodes", []):
            cands.extend(node_strings(n))
        per_slide["S%d" % idx] = cands
        deck.extend(cands)
    return per_slide, deck


def _find(needle, cands):
    """The first candidate string containing `needle`, or None."""
    for c in cands:
        if needle in alnum(c):
            return c
    return None


def check(copy, render_report, window=WINDOW):
    per_slide, deck = build_nodes(render_report)
    misses = []
    truncated = []
    checked = 0
    slides = normalize_slides(copy.get("slides", {}))
    for skey, sval in slides.items():
        cands = per_slide.get(skey, [])
        for path, s in collect(sval, ""):
            a = alnum(s)
            if not a:
                continue
            checked += 1
            needle = a if len(a) <= window else a[:window]
            hit = _find(needle, cands) or _find(needle, deck)
            if hit is None:
                misses.append((skey, path, s))
                continue
            # THE 80-CHARACTER PASTE (2026-08-27). A truncated string IS
            # present in the render, so presence can never catch it: run No.42
            # pasted four bodies straight out of render_report's `text` field,
            # which is cut at 80, and this gate passed all four. The signature
            # is exact and cannot be anything else -- an authored string at the
            # 80-character cut whose own element carries more words after it.
            raw = " ".join(s.split())
            if len(raw) >= 78 and alnum(hit).startswith(a) and len(alnum(hit)) > len(a):
                truncated.append((skey, path, raw, " ".join(hit.split())))
    return checked, misses, set(per_slide.keys()), deck, truncated


def main():
    ap = argparse.ArgumentParser(description="Verify copy.json slide strings appear in the render.")
    ap.add_argument("--copy", required=True, help="path to copy.json")
    ap.add_argument("--render-report", required=True, help="path to render/render_report.json")
    ap.add_argument("--window", type=int, default=WINDOW,
                    help="alphanumeric prefix window for long strings (default 40)")
    args = ap.parse_args()

    try:
        copy = json.load(open(args.copy))
    except (OSError, ValueError) as e:
        print("copy_sync_check: cannot read copy.json: %s" % e, file=sys.stderr)
        return 2
    try:
        rr = json.load(open(args.render_report))
    except (OSError, ValueError) as e:
        print("copy_sync_check: cannot read render_report.json: %s" % e, file=sys.stderr)
        return 2

    if "slides" not in copy:
        print("copy_sync_check: copy.json has no 'slides' object", file=sys.stderr)
        return 2

    checked, misses, rendered_keys, deck, truncated = check(copy, rr, args.window)
    deck_text = "".join(deck)

    # Zero authored strings compared is not agreement, it is nothing to compare.
    # An empty slides list, or slides under a key this reader does not know,
    # normalizes to {} and the miss list is then trivially empty, which used to
    # read as PASS. If the render carries text, the copy that produced it cannot
    # legitimately have contributed nothing to check.
    if checked == 0 and deck_text.strip():
        print("copy_sync_check: FAIL -- copy.json contributed no slide strings to "
              "compare, but the render carries text. The slides are empty or under "
              "a key this check does not read.", file=sys.stderr)
        return 1

    # Slides authored in copy but with no rendered counterpart are their own
    # (softer) signal; surface them but do not fail on them.
    authored = set(normalize_slides(copy["slides"]).keys())
    orphan = sorted(authored - rendered_keys, key=lambda s: int(s[1:]) if s[1:].isdigit() else 0)
    for o in orphan:
        print("copy_sync_check: WARN slide %s in copy.json has no rendered slide" % o, file=sys.stderr)

    if not misses and not truncated:
        print("copy_sync_check: PASS -- %d authored slide strings all present in the render" % checked)
        return 0

    if misses:
        print("copy_sync_check: FAIL -- %d authored slide string(s) not found in the render:" % len(misses))
        for skey, path, s in misses:
            shown = s if len(s) <= 70 else s[:67] + "..."
            print("  %s  %s  -> %r" % (skey, path, shown))
    if truncated:
        print("copy_sync_check: FAIL -- %d authored slide string(s) stop at the "
              "80-character cut of render_report's `text` field, and the element "
              "carries more words after it:" % len(truncated))
        for skey, path, raw, hit in truncated:
            print("  %s  %s" % (skey, path))
            print("     copy.json says -> %r (%d chars)" % (raw, len(raw)))
            print("     the render says -> %r" % (hit if len(hit) <= 200 else hit[:197] + "..."))
        print("Copy the WHOLE string. render_report's text_nodes[].full is the "
              "one to paste from; `text` is cut at 80 and `texts` drops span "
              "children, and a string built from either reads as present here.")
    print("Reconcile copy.json to the shipped render (or fix the render) before ship.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
