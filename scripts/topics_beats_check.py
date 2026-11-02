#!/usr/bin/env python3
"""Check ledger/topics.json's `beats` against the site's beat slugs, at append time.

WHY (2026-11-01, weekly machine pass; queue item 2026-10-29, repeat 1). A
topics.json entry may carry `beats`, a list of beat slugs, and site_build's
topic_index raises "beats must name known beat slugs" on one it doesn't know.
That is the right rule in the wrong place: it fires at the final site build,
after the runs/ copy and the ledger append. No.99 wrote federal-policy,
models-and-public-numbers and north-slope and met it there; No.101 wrote
broadband-and-connectivity and federal-policy and caught them only by hand. The
slugs live in site_build.TOPICS, which nothing in the ship step names.

So Phase 11 step 4 runs this straight after the append. It reads the SAME list
site_build reads (it imports TOPICS rather than copying it) and applies the
SAME rule (a present `beats` must be a non-empty list of known slugs; an entry
without `beats` is matched by terms and is fine), prints the known slugs, and
exits 1 naming each bad entry, so the fix is a one-line ledger edit before
anything is built.

    python3 scripts/topics_beats_check.py                 # every entry
    python3 scripts/topics_beats_check.py --date 2026-11-01   # this run's entry only
    python3 scripts/topics_beats_check.py --list          # just print the slugs

Exit 0 clean, 1 an unknown or empty `beats`, 2 the ledger can't be read.
Read only.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from site_build import TOPICS  # noqa: E402  the one list the site builds from


def problems(ledger, date=None):
    """[(run_date, beats, reason)] for every entry whose `beats` site_build
    would refuse. Mirrors site_build.topic_index's rule exactly."""
    slugs = {t["slug"] for t in TOPICS}
    out = []
    for e in (ledger or {}).get("entries", []):
        d = e.get("run_date")
        if date and d != date:
            continue
        if e.get("beats") is None:
            continue
        beats = e["beats"]
        if not isinstance(beats, list) or not beats:
            out.append((d, beats, "beats must be a non-empty list of slugs"))
            continue
        bad = [b for b in beats if b not in slugs]
        if bad:
            out.append((d, beats, "unknown slug(s) %s" % ", ".join(map(repr, bad))))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ledger", default=str(ROOT / "ledger" / "topics.json"))
    ap.add_argument("--date", help="check only the entry with this run_date")
    ap.add_argument("--list", action="store_true", help="print the known slugs and exit")
    args = ap.parse_args()
    known = [t["slug"] for t in TOPICS]
    print("known beat slugs (scripts/site_build.py TOPICS): " + ", ".join(known))
    if args.list:
        return 0
    try:
        ledger = json.loads(Path(args.ledger).read_text())
    except Exception as exc:
        print("FAIL: can't read %s (%s)" % (args.ledger, exc))
        return 2
    if args.date and not any(e.get("run_date") == args.date for e in ledger.get("entries", [])):
        print("FAIL: no topics.json entry has run_date %s; append it first" % args.date)
        return 1
    bad = problems(ledger, args.date)
    for d, beats, why in bad:
        print("FAIL: topics.json %s: beats %r: %s. Use only the slugs above, or drop "
              "`beats` and let the deck be matched by its terms." % (d, beats, why))
    if not bad:
        print("PASS: every `beats` checked names known slugs")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
