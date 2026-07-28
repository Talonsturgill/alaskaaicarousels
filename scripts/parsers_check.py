#!/usr/bin/env python3
"""
Fixture tests for the tolerant readers in site_build.

normalize_claims() and slide_entries() absorb every shape eighteen runs have
invented, and until this file existed they were exercised only by running the
whole build against real runs. That is a bad place to find out a shape stopped
parsing: the build succeeds, the page renders, and the verification record is
just quietly empty. That is exactly how 14 of 18 decks shipped blank.

Every fixture below is a real shape taken from the back catalogue, named by the
run it came from. Add one whenever a run invents a new shape.

Usage:  python scripts/parsers_check.py
Exit 0 all pass, 1 on any failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_build as sb  # noqa: E402

FAILS: list[str] = []


def eq(label, got, want):
    if got != want:
        FAILS.append(f"{label}\n      got  {got!r}\n      want {want!r}")
        print(f"  FAIL {label}")
    else:
        print(f"  ok   {label}")


# ---------- claims.json shapes ----------

CLAIM_SHAPES = {
    # 2026-07-26, the shape the fact-checker spec now pins
    "flat/current": (
        {"claims": [{"id": "C01", "claim": "A thing is true", "value": "23 governors",
                     "source_url": "https://a.test/x", "source_outlet": "RGA",
                     "source_is_primary": True, "date_of_source": "2026-07-23"}]},
        {"n": 1, "id": "C01", "outlet": "RGA", "primary": True, "date": "2026-07-23"}),
    # 2026-07-10, text/source_date, no outlet
    "text+source_date": (
        {"claims": [{"id": "c01", "text": "A thing is true", "source_url": "https://a.test/x",
                     "source_date": "2026-07-09", "credibility": "primary"}]},
        {"n": 1, "id": "c01", "outlet": "", "primary": True, "date": "2026-07-09"}),
    # 2026-07-20, url/published/source_outlet
    "url+published": (
        {"claims": [{"id": "c1", "text": "A thing", "url": "https://a.test/x",
                     "source_outlet": "KDLG", "published": "2026-07-18"}]},
        {"n": 1, "id": "c1", "outlet": "KDLG", "primary": False, "date": "2026-07-18"}),
    # 2026-07-08, evidence nested as a list of objects
    "nested evidence": (
        {"claims": [{"id": "c01", "claim": "A thing",
                     "evidence": [{"url": "https://a.test/x", "outlet": "Northern Journal",
                                   "pub_date": "2026-07-07"}]}]},
        {"n": 1, "id": "c01", "outlet": "Northern Journal", "primary": False,
         "date": "2026-07-07"}),
    # 2026-07-18, container named verified_claims, statement not claim
    "verified_claims": (
        {"verified_claims": [{"claim_id": "V1", "statement": "A thing",
                              "source_url": "https://a.test/x", "outlet": "ADN"},
                             {"claim_id": "V2", "statement": "Another",
                              "source_url": "https://b.test/y", "outlet": "ADN"}]},
        {"n": 2, "id": "V1", "outlet": "ADN", "primary": False, "date": ""}),
    # 2026-07-21, container named for the story's codename
    "codename container": (
        {"beluga": [{"id": "b1", "text": "A thing", "source_url": "https://a.test/x",
                     "outlet": "KTOO"},
                    {"id": "b2", "text": "Another", "source_url": "https://b.test/y",
                     "outlet": "KTOO"}]},
        {"n": 2, "id": "b1", "outlet": "KTOO", "primary": False, "date": ""}),
    # 2026-07-24, claims nested inside stories
    "nested in stories": (
        {"stories": [{"story_id": "s1", "claims": [
            {"id": "n1", "text": "A thing", "source_url": "https://a.test/x", "outlet": "AP"},
            {"id": "n2", "text": "Another", "source_url": "https://b.test/y", "outlet": "AP"}]}]},
        {"n": 2, "id": "n1", "outlet": "AP", "primary": False, "date": ""}),
}


def test_claims():
    print("normalize_claims")
    for name, (doc, want) in CLAIM_SHAPES.items():
        got = sb.normalize_claims(doc)
        eq(f"{name}: count", len(got), want["n"])
        if not got:
            continue
        first = got.get(want["id"])
        if first is None:
            eq(f"{name}: id {want['id']} present", sorted(got), [want["id"]])
            continue
        eq(f"{name}: outlet", first["source_outlet"], want["outlet"])
        eq(f"{name}: primary", first["source_is_primary"], want["primary"])
        eq(f"{name}: date", first["date_of_source"], want["date"])

    print("normalize_claims, things it must refuse")
    # A kill log is not a claim list. Publishing dropped claims as verified
    # would be a lie, and the container is discovered by shape.
    eq("kill_log excluded", sb.normalize_claims(
        {"kill_log": [{"claim": "wrong", "source_url": "https://a.test/",
                       "why_killed": "unverifiable"}]}), {})
    eq("dropped excluded", sb.normalize_claims(
        {"dropped": [{"claim": "wrong", "source_url": "https://a.test/"}]}), {})
    # 2026-07-25 recorded a derived ratio with source_url "DERIVED". A section
    # headed "each re-fetched from its source" must not carry it.
    eq("non-URL source refused", sb.normalize_claims(
        {"claims": [{"id": "d1", "claim": "A ratio", "source_url": "DERIVED"}]}), {})
    eq("javascript: refused", sb.normalize_claims(
        {"claims": [{"id": "j1", "claim": "x", "source_url": "javascript:alert(1)"}]}), {})
    eq("unsourced refused", sb.normalize_claims(
        {"claims": [{"id": "u1", "claim": "x"}]}), {})
    eq("empty doc", sb.normalize_claims({}), {})
    # The nested descent must answer the question it was asked.
    eq("nested outlet is not the url", sb._first(
        {"source": {"url": "https://evil.test/", "outlet": "Real Outlet"}},
        sb.CLAIM_FIELDS["outlet"], "outlet"), "Real Outlet")


# ---------- copy.json slide shapes ----------

SLIDE_SHAPES = {
    "list, n/headline/body": (
        [{"n": 1, "headline": "H one", "body": "B one"},
         {"n": 2, "headline": "H two", "body": "B two"}], 2, "H one"),
    "list, head not headline": (
        [{"n": 1, "head": "H one", "body": "B one"}], 1, "H one"),
    "dict keyed 01": ({"01": {"headline": "H one"}, "02": {"headline": "H two"}}, 2, "H one"),
    "dict keyed S1": ({"S1": {"headline": "H one"}, "S2": {"headline": "H two"}}, 2, "H one"),
    "dict keyed slide-01": (
        {"slide-01": {"headline": "H one"}, "slide-02": {"headline": "H two"}}, 2, "H one"),
    # 2026-07-25: each slide is the flat list of strings set on it
    "dict of raw string lists": (
        {"S1": ["Alaska governor 2026, 24 days to the primary", "AUG 18 2026",
                "ALASKA.AI", "01 / 10", "58 deg 18'N 134 deg 25'W",
                "Campaign finance reports, week of July 20 2026"]},
        1, "Alaska governor 2026, 24 days to the primary"),
}


def test_slides():
    print("slide_entries")
    for name, (data, n, first_head) in SLIDE_SHAPES.items():
        got = sb.slide_entries({"slide_data": data})
        eq(f"{name}: count", len(got), n)
        if got:
            eq(f"{name}: slide 1 headline",
               sb._slide_text(got[min(got)], sb.HEAD_KEYS), first_head)
    eq("ordered by slide number", list(sb.slide_entries(
        {"slide_data": {"03": {"headline": "c"}, "01": {"headline": "a"},
                        "02": {"headline": "b"}}})), [1, 2, 3])
    eq("no slide data", sb.slide_entries({"slide_data": None}), {})
    # Furniture must not be mistaken for prose.
    eq("furniture dropped", sb._prose_lines(
        ["01 / 10", "ALASKA.AI", "AUG 18 2026", "58 deg 18'N 134 deg 25'W",
         "a real sentence with words"]), ["a real sentence with words"])


# ---------- house style ----------

def test_house():
    print("house()")
    gate = re.compile(r"https?://\S+|\d{1,2}:\d{2}")
    for raw in ("Note:x is true", "SB 250:the vote died", "a: b", "Sources:",
                "See https://a.test/x:8080/p for it", "Doors at 4:30 p.m."):
        out = sb.house(raw)
        left = ":" in gate.sub(" ", out)
        eq(f"gate-clean {raw!r}", left, False)
    eq("clock kept", sb.house("Doors at 4:30 p.m."), "Doors at 4:30 p.m.")
    eq("em dash", sb.house("a - b".replace("-", "—")), "a, b")
    eq("curly quotes", sb.house("“x” and ‘y’"), '"x" and \'y\'')
    eq("emoji stripped", sb.house("hot \U0001F525 take"), "hot take")
    eq("empty", sb.house(""), "")
    eq("none", sb.house(None), "")


def main() -> int:
    test_claims()
    test_slides()
    test_house()
    print()
    if FAILS:
        print(f"FAIL, {len(FAILS)} assertion(s):")
        for f in FAILS:
            print(f"  - {f}")
        return 1
    print("parsers_check: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
