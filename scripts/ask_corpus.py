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
# $57M, 4:30, 2026-07-17, 50.3 percent. Captures the digits and any decimal
# part, and leaves the surrounding punctuation to the caller.
NUMERAL_RE = re.compile(r"\d+(?:\.\d+)?")


def normalise(tok):
    """One spelling per number, so 07 and 7 and 7th are the same token.

    The record writes dates as 2026-07-17 and a reader asks about July 17th.
    Without this, every zero-padded date component in the corpus would fail to
    authorise the same number written the way a person writes it, and the
    check would reject correct answers. Trailing zeros after a decimal point
    go too, so 6.50 and 6.5 agree.
    """
    tok = tok.lstrip("0") or "0"
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

    # The allow-list is derived from the finished corpus, so it can never drift
    # from what the model was actually shown. Anything the answer may say, it
    # can read here first.
    corpus["authorised_numerals"] = sorted(numerals(corpus))
    corpus["slugs"] = sorted(it["id"] for it in items)
    return corpus


def write(path=OUT, **kw):
    corpus = build(**kw)
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
                      ("2026", "2026"), ("00", "0"), ("6.00", "6")):
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
