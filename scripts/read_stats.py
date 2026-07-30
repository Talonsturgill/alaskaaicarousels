#!/usr/bin/env python3
"""read_stats.py reports what people actually read on alaskaaihq.com.

Before this existed there was no measurement of readership at all. Nineteen
decks, a video feed and a subscriber list had shipped with nobody able to say
whether any of it was read, which meant every editorial decision was a guess and
ledger/instincts.json was the machine grading its own homework with no audience
input.

The point of running it here rather than on a hosted dashboard is that a
dashboard is a thing somebody has to remember to open. This prints a block the
daily routine drops into the Gmail draft, so the numbers arrive whether or not
anyone goes looking.

It reads the page_views table in the alaska-ai-dashboard Supabase project, which
by design holds no reader identifier, no IP and no user agent (see /privacy/).
So this can report pages read and where they came from, and can never report who.
There are no unique-visitor counts because there is deliberately nothing to
count them with.

  python scripts/read_stats.py --days 7
  python scripts/read_stats.py --days 7 --json

Needs SUPABASE_READ_KEY (a service-role key, since the table is RLS-closed to
browser keys). Without it this prints SKIP and exits 0, so a missing key can
never break a run.

Exit 0 always unless --strict is passed and the query fails.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date, timedelta

PROJECT = "gsuvfpnyzebycqhsekus"
REST = f"https://{PROJECT}.supabase.co/rest/v1/page_views"

# Paths that are not articles, so the "most read" list is about journalism
# rather than about the front door.
CHROME = {"/", "/archive/", "/topics/", "/docket/", "/sources/", "/data/",
          "/questions/", "/privacy/", "/about/", "/services/", "/scan/",
          "/videos/"}


def key():
    for name in ("SUPABASE_READ_KEY", "SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_KEY"):
        v = (os.environ.get(name) or "").strip()
        if v:
            return v
    return ""


def fetch(days, k):
    since = (date.today() - timedelta(days=days)).isoformat()
    q = urllib.parse.urlencode({
        "select": "at,path,ref_host,campaign,device",
        "at": f"gte.{since}",
        "order": "at.desc",
        "limit": "50000",
    })
    req = urllib.request.Request(
        f"{REST}?{q}",
        headers={"apikey": k, "authorization": f"Bearer {k}",
                 "accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def summarize(rows, days):
    total = len(rows)
    paths = Counter(r["path"] for r in rows)
    # Decisions get their own list below, so keep them out of this one rather
    # than reporting the same path twice under two headings.
    articles = Counter({p: n for p, n in paths.items()
                        if p not in CHROME and not p.startswith("/docket/")})
    refs = Counter(r["ref_host"] for r in rows if r.get("ref_host"))
    direct = sum(1 for r in rows if not r.get("ref_host"))
    camps = Counter(r["campaign"] for r in rows if r.get("campaign"))
    devices = Counter(r["device"] for r in rows if r.get("device"))
    decisions = Counter({p: n for p, n in paths.items()
                         if p.startswith("/docket/") and p != "/docket/"})
    return {
        "days": days, "views": total,
        "per_day": round(total / days, 1) if days else 0,
        "top_pages": paths.most_common(8),
        "top_articles": articles.most_common(5),
        "top_decisions": decisions.most_common(5),
        "referrers": refs.most_common(6),
        "direct": direct,
        "campaigns": camps.most_common(5),
        "devices": devices.most_common(),
    }


def block(s):
    """The plain-text block the Gmail draft carries. Deliberately small; a
    number nobody reads is the problem this is fixing, not the solution."""
    L = [f"READERSHIP, LAST {s['days']} DAYS",
         f"  {s['views']} pages read, about {s['per_day']} a day"]
    if not s["views"]:
        L.append("  nothing recorded yet. If this stays at zero for a day after"
                 " the counter shipped, the beacon is not firing.")
        return "\n".join(L)
    if s["top_articles"]:
        L.append("  most read articles")
        for p, n in s["top_articles"]:
            L.append(f"    {n:>4}  {p}")
    if s["top_decisions"]:
        L.append("  most read docket decisions")
        for p, n in s["top_decisions"]:
            L.append(f"    {n:>4}  {p}")
    if s["referrers"]:
        L.append("  where they came from")
        for h, n in s["referrers"]:
            L.append(f"    {n:>4}  {h}")
    L.append(f"    {s['direct']:>4}  direct or withheld")
    if s["campaigns"]:
        L.append("  campaigns")
        for c, n in s["campaigns"]:
            L.append(f"    {n:>4}  {c}")
    if s["devices"]:
        L.append("  " + ", ".join(f"{d} {n}" for d, n in s["devices"]))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="exit nonzero if the query fails (default is to SKIP)")
    a = ap.parse_args()

    k = key()
    if not k:
        print("read_stats: SKIP, no SUPABASE_READ_KEY set")
        return 0
    try:
        rows = fetch(a.days, k)
    except (urllib.error.URLError, OSError, ValueError) as e:
        msg = f"read_stats: could not read page_views ({type(e).__name__})"
        print(msg, file=sys.stderr)
        return 1 if a.strict else 0

    s = summarize(rows, a.days)
    print(json.dumps(s, indent=2) if a.json else block(s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
