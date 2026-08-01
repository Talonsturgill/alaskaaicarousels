#!/usr/bin/env python3
"""indexnow.py pushes changed URLs to the search engines that accept a push.

A new site's problem is not only where it ranks but how long it waits to be
looked at. Crawlers arrive on their own schedule, and for a publication that
ships something every day, "whenever the crawler next wanders past" is a real
cost: the docket can carry a comment deadline that closes before the page
holding it has been fetched.

IndexNow inverts that. One POST and the URL is queued for fetch in minutes.
Ownership is proved by hosting a file named for the key containing the key,
which scripts/site_build.py writes into docs/ on every build.

BE EXACT ABOUT WHAT THIS BUYS. Google does not participate and this will not
move a Google ranking. Bing, Yandex, Seznam and Naver do participate, and Bing's
index is what Copilot and ChatGPT search read, so this is about being findable
and citable by the answer engines. That is the same reason this site publishes
/llms.txt and a page per decision.

  python scripts/indexnow.py --dry-run          # show what would be sent
  python scripts/indexnow.py                    # submit every sitemap URL
  python scripts/indexnow.py --since 2026-08-01 # only URLs changed on or after

Exit 0 unless --strict is passed and the submission fails.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request

HOST = "alaskaaihq.com"
SITE = f"https://{HOST}"
KEY = "a7f3c21e9b8d4e5f6a1c0b3d2e8f7a94"
ENDPOINT = "https://api.indexnow.org/IndexNow"

# The protocol caps a single submission at 10000 URLs. This site is two orders
# of magnitude under that, so the cap is a guard rather than a real constraint.
MAX_URLS = 10000


def sitemap_urls(since=None):
    """Every URL in the published sitemap, optionally only those whose lastmod
    is on or after a date. Read from the LIVE sitemap rather than the local
    build, because submitting a URL the engines cannot fetch yet is worse than
    submitting nothing: it spends the site's credibility on a 404."""
    with urllib.request.urlopen(f"{SITE}/sitemap.xml", timeout=30) as r:
        xml = r.read().decode()
    out = []
    for block in re.findall(r"<url>(.*?)</url>", xml, re.S):
        loc = re.search(r"<loc>(.*?)</loc>", block)
        if not loc:
            continue
        if since:
            mod = re.search(r"<lastmod>(.*?)</lastmod>", block)
            if not mod or mod.group(1) < since:
                continue
        out.append(loc.group(1))
    return out


def verify_key():
    """The key file has to be live before a submission means anything. An
    engine that cannot fetch it rejects the batch, and it does so quietly."""
    try:
        with urllib.request.urlopen(f"{SITE}/{KEY}.txt", timeout=30) as r:
            return r.read().decode().strip() == KEY
    except (urllib.error.URLError, OSError):
        return False


def submit(urls):
    body = json.dumps({"host": HOST, "key": KEY,
                       "keyLocation": f"{SITE}/{KEY}.txt",
                       "urlList": urls[:MAX_URLS]}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                 headers={"content-type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="only URLs with lastmod on or after this date")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="exit nonzero if the submission fails (default is to warn)")
    a = ap.parse_args()

    try:
        urls = sitemap_urls(a.since)
    except (urllib.error.URLError, OSError) as e:
        print(f"indexnow: could not read the sitemap ({type(e).__name__})",
              file=sys.stderr)
        return 1 if a.strict else 0
    if not urls:
        print("indexnow: nothing to submit")
        return 0

    if a.dry_run:
        print(f"would submit {len(urls)} urls to {ENDPOINT}")
        for u in urls[:10]:
            print(f"  {u}")
        if len(urls) > 10:
            print(f"  ... and {len(urls) - 10} more")
        return 0

    if not verify_key():
        print(f"indexnow: {SITE}/{KEY}.txt is not live or does not match, so a "
              f"submission would be rejected. Deploy the site first.",
              file=sys.stderr)
        return 1 if a.strict else 0

    try:
        status = submit(urls)
    except (urllib.error.URLError, OSError) as e:
        print(f"indexnow: submission failed ({type(e).__name__})", file=sys.stderr)
        return 1 if a.strict else 0
    # 200 accepted, 202 accepted but key validation still pending.
    print(f"indexnow: submitted {len(urls)} urls, HTTP {status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
