#!/usr/bin/env python3
"""Build the answering corpus for the docket's ask box.

WHY THERE IS NO RETRIEVAL HERE. The whole public record is about 33,000 tokens.
That fits in one model context with room left over, so there is no embedding
step, no vector store, no chunking, and no similarity threshold to tune. The
single biggest source of wrong answers in a retrieval chatbot is retrieving the
wrong passage, and a corpus this size lets us delete that failure mode rather
than manage it. Every answer is written with the entire docket in view.

WHAT THIS FILE ACTUALLY GUARANTEES. Two things the answering layer cannot
provide for itself:

  authorised_numerals  every numeral that appears anywhere in the record.
                       A reply may not contain a numeral outside this set, so
                       an invented figure is refused rather than published.
                       This is the page's own numeral lint (gaswatch_build.py)
                       moved from build time to answer time.

  slugs                every docket item id. A citation to anything else is a
                       failed check, so a plausible-looking link to an item
                       that does not exist cannot be returned.

The gas watch half is taken from gaswatch_build.feed(), which is the exact
structure published at /gas-watch.json. Building it from the same function
rather than re-deriving it means the corpus can never disagree with the page,
and a figure the page is allowed to show is a figure the answer is allowed to
quote. Nothing here writes to ledger/gaswatch.jsonl or the model config; both
are read-only to everything except the collector.
"""

import argparse
import json
import os
import re
import sys
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

import gaswatch_build as gw  # noqa: E402
import gaswatch_collect as gc  # noqa: E402

DOCKET = os.path.join(REPO, "ledger", "docket.json")
OUT = os.path.join(REPO, "docs", "ask-corpus.json")

# Mirrors site_build's GAS_WATCH_META so the embedded feed is byte-comparable
# with the published one.
GAS_META = {
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "license_label": "CC BY 4.0",
    "attribution": "Alaska AI",
    "publisher": "Alaska AI",
    "spatial_coverage": "Alaska",
    "docket_item_id": "enstar-cook-inlet-gas-storage",
}

# Fields worth answering from. Deliberately not the whole item: internal
# bookkeeping adds tokens without adding answers, and every extra field is
# more numerals admitted to the allow-list, which loosens the numeral check.
ITEM_FIELDS = ("id", "title", "kind", "status", "decider", "public_access",
               "access_note", "summary", "key_dates", "location", "sources",
               "first_seen", "last_updated", "history")

# A numeral, in any of the shapes the record actually uses: 715.4, 50-year,
# $57M, 4:30, 2026-07-17, 50.3 percent, 4,700.
#
# A THOUSANDS SEPARATOR IS PART OF THE NUMBER, NOT A BREAK IN IT. This used to
# be \d+(?:\.\d+)?, which read "4,700" as a 4 and a 700 and authorised both.
# The pack carries 35 comma grouped figures, and splitting them admitted six
# numerals that appear nowhere in the record on their own: 150, 300, 566, 700,
# 950 and 967. Those are exactly the round figures a model invents, so the
# guard was quietly licensing the most likely kind of wrong answer.
NUMERAL_RE = re.compile(r"\d(?:[\d,]*\d)?(?:\.\d+)?")


def normalise(tok):
    """One spelling per number, so 07 and 7 and 7th are the same token.

    The record writes dates as 2026-07-17 and a reader asks about July 17th.
    Without this, every zero-padded date component in the corpus would fail to
    authorise the same number written the way a person writes it, and the
    check would reject correct answers. Trailing zeros after a decimal point
    go too, so 6.50 and 6.5 agree.

    Commas go, so a model shown 4,700 may write 4700 and still pass. The zero
    in FRONT of a decimal point stays, because stripping it left .8469, which
    NUMERAL_RE cannot match at all, so a figure written back that way would
    have gone through this gate unchecked.
    """
    tok = tok.replace(",", "")
    tok = ("0" + tok.lstrip("0")) if tok.startswith("0.") else (tok.lstrip("0") or "0")
    if "." in tok:
        tok = tok.rstrip("0").rstrip(".") or "0"
    return tok


def numerals(blob):
    """Every distinct number in a JSON structure or string, normalised."""
    if not isinstance(blob, str):
        blob = json.dumps(blob, sort_keys=True)
    return {normalise(m) for m in NUMERAL_RE.findall(blob)}


def docket_items(path=DOCKET):
    raw = json.loads(open(path).read())
    items = raw["items"] if isinstance(raw, dict) and "items" in raw else raw
    return [{k: it[k] for k in ITEM_FIELDS if k in it} for it in items]


def build(today=None, site_url="https://alaskaaihq.com"):
    today = today or date.today()
    items = docket_items()
    series = gw.load_series()
    model = gc.load_model(gw.MODEL_CONFIG)
    gas = gw.feed(series, model, site_url, today, GAS_META)

    corpus = {
        "generated": today.isoformat(),
        "docket": {
            "count": len(items),
            "items": items,
        },
        "gas_watch": gas,
    }

    # The allow-list from the corpus alone. published() widens it to cover what
    # the pack actually renders, and that is the one the worker reads.
    corpus["authorised_numerals"] = sorted(numerals(corpus))
    corpus["slugs"] = sorted(it["id"] for it in items)
    return corpus


def published(today=None, site_url="https://alaskaaihq.com"):
    """The corpus as it ships, with the pack's own figures authorised.

    WHY THIS IS A SECOND FUNCTION AND NOT PART OF build(). ask_pack is a pure
    function of build(), so build() cannot read the pack without the two
    calling each other forever. The widening happens at the publish step, where
    both already exist.

    WHY IT IS NEEDED AT ALL. The corpus is the SOURCE. The pack is what the
    model is actually handed, and ask_pack computes on the way: a storage
    figure in Mcf is rendered in Bcf beside it, a deliverability figure in
    Mcf/d in MMcf/d. Those conversions appear nowhere in the corpus, so a list
    built from the corpus alone refused figures the model had been shown one
    line earlier. Five were live when this was measured, including the 6.83
    Bcf in the previous-reading line, which is the shape of sentence this box
    writes every day.

    A model cannot state a number it was never given, so what it was given is
    the honest boundary.
    """
    import ask_pack  # here, not at import time, because ask_pack imports this
    corpus = build(today=today, site_url=site_url)
    pack = ask_pack.build(today=today, site_url=site_url)["pack"]
    corpus["authorised_numerals"] = sorted(
        set(corpus["authorised_numerals"]) | numerals(pack))
    return corpus


def write(path=OUT, **kw):
    # published(), not build(). The file the worker reads has to authorise what the
    # model is actually shown, and the pack renders figures the corpus never holds.
    corpus = published(**kw)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(corpus, fh, separators=(",", ":"), sort_keys=True)
    return corpus, path


def self_test():
    print("the corpus")
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    c = build()
    check("every docket item is present",
          c["docket"]["count"] == len(c["docket"]["items"]) == len(c["slugs"]),
          f"{c['docket']['count']} items")
    check("the gas watch feed came through",
          bool(c["gas_watch"].get("series")),
          f"{len(c['gas_watch'].get('series') or [])} day(s)")

    print("numeral normalisation")
    for raw, want in (("07", "7"), ("0", "0"), ("6.50", "6.5"), ("715.4", "715.4"),
                      ("2026", "2026"), ("00", "0"), ("6.00", "6"),
                      # A thousands separator is inside the number, not a break in it.
                      ("4,700", "4700"), ("1,781,547.9", "1781547.9"),
                      # The leading zero of a decimal stays. Without it 0.5 became .5,
                      # which NUMERAL_RE cannot match, so the figure went unchecked.
                      ("0.5", "0.5"), ("0.50", "0.5")):
        check(f"{raw} normalises to {want}", normalise(raw) == want, normalise(raw))
    # The case this function exists for. A zero-padded date component in the
    # record has to authorise the same day written the way a person writes it.
    padded = numerals("Comment window closed 2026-07-17.")
    check("a padded date authorises the unpadded day",
          {"17", "7", "2026"} <= padded, str(sorted(padded)))

    print("the allow-list actually covers the record")
    allowed = set(c["authorised_numerals"])
    # Sample real figures out of the corpus and confirm each one is authorised.
    # A allow-list that did not cover its own source would refuse true answers.
    sampled, missing = 0, []
    for it in c["docket"]["items"]:
        for tok in numerals(it):
            sampled += 1
            if tok not in allowed:
                missing.append(tok)
    check("every numeral in every item is authorised", not missing,
          f"{sampled} sampled, {len(missing)} missing" +
          (f", first {missing[:3]}" if missing else ""))

    gas_missing = [t for t in numerals(c["gas_watch"]) if t not in allowed]
    check("every numeral in the gas watch feed is authorised", not gas_missing,
          str(gas_missing[:3]))

    # And it has to be able to refuse. A check that passes everything proves
    # nothing, so confirm a number the record does not contain is absent.
    invented = [t for t in ("87654321", "99999.7") if t in allowed]
    check("a number the record does not contain is NOT authorised",
          not invented, str(invented))

    print("slugs")
    check("slugs are unique", len(c["slugs"]) == len(set(c["slugs"])))
    check("a slug that does not exist is not listed",
          "not-a-real-docket-item" not in c["slugs"])

    print("the model may state only what it was shown")
    import ask_pack
    pub = published()
    allowed_pub = set(pub["authorised_numerals"])
    shown = numerals(ask_pack.build()["pack"])
    # THE CHECK THAT MATTERS MOST HERE. Every figure the pack renders has to be one the
    # guard will accept back. Eighteen were not when this was written, because the corpus
    # tokeniser split on thousands separators and because ask_pack computes unit
    # conversions that appear nowhere in the corpus. A reader saw an answer stop mid
    # sentence over a number the model had been handed one line earlier.
    check("every figure the pack shows is authorised", not (shown - allowed_pub),
          f"{len(shown - allowed_pub)} unauthorised, e.g. {sorted(shown - allowed_pub)[:4]}")
    # And the ghosts a split tokeniser used to invent. None of these appears in the record
    # on its own, and every one is the kind of round figure a model reaches for.
    ghosts = {"150", "300", "566", "700", "950", "967"} & allowed_pub
    check("no numeral is authorised only as half of a grouped figure", not ghosts,
          str(sorted(ghosts)))

    print("size")
    blob = json.dumps(c, separators=(",", ":"))
    approx = round(len(blob) / 3.8)
    # The whole design rests on the record fitting in one context. If it stops
    # fitting, that is a design change and not a tuning problem, so say so
    # loudly here rather than discovering it as a truncated answer.
    check("the corpus still fits comfortably in one context",
          approx < 250_000, f"{len(blob)} chars, roughly {approx} tokens")

    print()
    print("self-test clean" if ok[0] else "self-test FAILED")
    return 0 if ok[0] else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--date", help="ISO date, America/Anchorage")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    today = date.fromisoformat(args.date) if args.date else date.today()
    corpus, path = write(args.out, today=today)
    blob = json.dumps(corpus, separators=(",", ":"))
    print(f"ask corpus -> {path} ({corpus['docket']['count']} items, "
          f"{len(corpus['authorised_numerals'])} numerals, "
          f"{len(blob)} chars, roughly {round(len(blob) / 3.8)} tokens)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
