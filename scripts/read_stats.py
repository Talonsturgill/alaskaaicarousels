#!/usr/bin/env python3
"""read_stats.py reports what people actually read on alaskaaihq.com.

Before this existed there was no measurement of readership at all. Nineteen
decks, a video feed and a subscriber list had shipped with nobody able to say
whether any of it was read, which meant every editorial decision was a guess and
ledger/instincts.json was the machine grading its own homework with no audience
input.

NEEDS NO CREDENTIALS. The figures come from a public aggregate endpoint, so the
routine, this script and any reader all get them the same way with no key to
set, rotate or leak. That is deliberate rather than lazy: a publication that
already publishes its source archive and its correction log has no reason to
treat its own traffic as a secret.

The endpoint returns aggregates only, and the table behind it holds nothing
personal in the first place, no cookie, no visitor id, no IP, no user agent (see
/privacy/). So this can report which pages were read and where readers came
from, and can never report who. There are no unique-visitor counts because
there is deliberately nothing to count them with.

  python scripts/read_stats.py --days 7
  python scripts/read_stats.py --days 7 --json

Exit 0 always unless --strict is passed and the fetch fails.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

STATS = "https://gsuvfpnyzebycqhsekus.supabase.co/functions/v1/stats"

# Paths that are not journalism, so the "most read" lists stay about the work
# rather than about the front door.
CHROME = {"/", "/archive/", "/topics/", "/docket/", "/sources/", "/data/",
          "/questions/", "/privacy/", "/about/", "/services/", "/scan/",
          "/videos/"}


def fetch(days):
    req = urllib.request.Request(f"{STATS}?days={days}",
                                 headers={"accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def block(s):
    """The plain-text block the Gmail draft carries. Deliberately small; a
    number nobody reads is the problem being fixed, not the solution."""
    days, views = s.get("days", "?"), s.get("views", 0)
    L = [f"READERSHIP, LAST {days} DAYS", f"  {views} pages read"]
    if isinstance(views, int) and days:
        L[-1] += f", about {round(views / days, 1)} a day"
    if not views:
        L.append("  nothing recorded yet. If this stays at zero a day after the"
                 " counter shipped, the beacon is not firing.")
        return "\n".join(L)

    def rows(label, items, keyname):
        if not items:
            return
        L.append(f"  {label}")
        for it in items:
            L.append(f"    {it['views']:>4}  {it[keyname]}")

    arts = [x for x in s.get("top_articles") or [] if x["path"] not in CHROME]
    rows("most read articles", arts, "path")
    rows("most read docket decisions", s.get("top_decisions") or [], "path")
    rows("where they came from", s.get("referrers") or [], "host")
    L.append(f"    {s.get('direct', 0):>4}  direct or withheld")
    rows("campaigns", s.get("campaigns") or [], "campaign")
    dev = s.get("devices") or {}
    if dev:
        L.append("  " + ", ".join(f"{k} {v}" for k, v in sorted(dev.items())))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="exit nonzero if the fetch fails (default is to warn)")
    a = ap.parse_args()
    try:
        s = fetch(a.days)
    except (urllib.error.URLError, OSError, ValueError) as e:
        print(f"read_stats: could not reach the stats endpoint "
              f"({type(e).__name__})", file=sys.stderr)
        return 1 if a.strict else 0
    print(json.dumps(s, indent=2) if a.json else block(s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
