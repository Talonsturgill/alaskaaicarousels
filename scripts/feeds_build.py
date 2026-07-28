#!/usr/bin/env python3
"""
Machine-readable surfaces for alaskaaihq.com: feeds, plaintext mirrors, llms.txt.

Imported by site_build.py, which owns the page HTML. This module owns
everything a machine reads instead of a page.

The competitive case for it, measured in July 2026: the Anchorage Daily News
and Alaska's News Source both block every AI crawler, Alaska's News Source
publishes no RSS at all, and The Alaska Story ships a stock WordPress feed with
no structured data. Nobody in the state publishes a subscribable feed of AI
policy changes. That lane is empty and costs nothing to hold.

Feeds carry full content, not teasers. A truncated feed protects page views for
a publication that sells page views; this one wants to be quoted correctly.
"""
from __future__ import annotations

import json
import re
from datetime import date as ddate, datetime, timezone
from xml.sax.saxutils import escape as xesc

# Decks ship in the afternoon Alaska time. No run records a wall-clock publish
# time, so feeds state a consistent 17:00 UTC (about 9am Alaska) rather than
# inventing per-item precision the record does not support.
PUBLISH_HOUR_UTC = 17
MAX_ITEMS = 50


def _dt(iso: str) -> datetime:
    return datetime.fromisoformat(iso).replace(
        hour=PUBLISH_HOUR_UTC, tzinfo=timezone.utc)


def rfc822(iso: str) -> str:
    return _dt(iso).strftime("%a, %d %b %Y %H:%M:%S +0000")


def rfc3339(iso: str) -> str:
    return _dt(iso).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sources(r) -> list[dict]:
    """Distinct sources behind a deck, primary documents first."""
    seen, out = set(), []
    for c in sorted((r.get("claims") or {}).values(),
                    key=lambda c: (not c.get("source_is_primary"), c.get("id", ""))):
        url = c.get("source_url")
        if url and url not in seen:
            seen.add(url)
            out.append(c)
    return out


# ---------- plaintext mirrors ----------

def deck_markdown(r, site_url: str) -> str:
    """One deck as Markdown.

    An LLM fetching a URL would rather have this than parse 60 KB of HTML for
    the 11 KB of story inside it, and a Markdown mirror costs one file per run.
    Everything here already exists in the run record."""
    lines = [f"# {r['title']}", ""]
    if r.get("hook"):
        lines += [f"> {r['hook']}", ""]
    lines += [f"Published {r['date']} by Alaska AI. {r['slides']} slides.",
              f"Canonical: {site_url}/archive/{r['date']}/", ""]

    if r.get("article_text"):
        lines += ["## The story", "", r["article_text"], ""]

    claims = sorted((r.get("claims") or {}).values(),
                    key=lambda c: (not c.get("source_is_primary"), c.get("id", "")))
    if claims:
        lines += ["## What we verified", ""]
        for c in claims:
            claim = (c.get("claim") or "").strip().rstrip(".")
            if not claim:
                continue
            kind = "primary document" if c.get("source_is_primary") else "report"
            outlet = c.get("source_outlet") or "source"
            url = c.get("source_url") or ""
            when = f", {c['date_of_source']}" if c.get("date_of_source") else ""
            cite = f"[{outlet}]({url})" if url else outlet
            lines.append(f"- {claim}. {cite}, {kind}{when}.")
        lines.append("")

    lines += [f"Slides and the deck PDF are linked from the canonical page.", ""]
    return "\n".join(lines).rstrip() + "\n"


def llms_txt(site_url: str, runs: list, docket: dict | None = None,
             topics: list | None = None) -> str:
    """The curated map at /llms.txt (llmstxt.org).

    Expanded from a five-link stub to something an agent can actually work
    from: the feeds, the open data, the standing topic pages, and the most
    recent decks by name so a crawler that reads only this file still learns
    what the publication covers."""
    out = [
        "# Alaska AI",
        "",
        "> Alaska AI is the daily publication on Alaska's AI beat and an AI studio in",
        "> Anchorage that builds AI systems for Alaska businesses. Every fact on the",
        "> site is verified against a fetched primary source, and every deck page",
        "> publishes that verification record with the claim, the outlet, the date,",
        "> and whether the source is a primary document.",
        "",
        "Content here may be read, indexed and cited by AI systems. Attribution to",
        "Alaska AI with a link to the page is requested. No crawler is blocked.",
        "",
        "## Core pages",
        "",
        f"- [AI consulting for Alaska businesses]({site_url}/services/)",
        f"- [The Bottleneck Scanner, an honest free read of where AI would and would "
        f"not help a business]({site_url}/scan/)",
        f"- [The Alaska AI Docket, every AI infrastructure decision in the state]"
        f"({site_url}/docket/)",
        f"- [Articles, one verified Alaska and AI story a day]({site_url}/archive/)",
        f"- [About Alaska AI]({site_url}/about/)",
        "",
        "## Feeds",
        "",
        f"- [Articles, RSS]({site_url}/feed.xml) full content, one deck a day",
        f"- [Articles, Atom]({site_url}/atom.xml)",
        f"- [Articles, JSON Feed]({site_url}/feed.json)",
        f"- [Docket changes, RSS]({site_url}/docket/feed.xml) every tracked Alaska AI "
        f"decision as it moves",
        "",
        "## Data",
        "",
        f"- [The docket as open JSON]({site_url}/docket.json)",
        f"- [Every deck as plain Markdown]({site_url}/llms-full.txt)",
    ]
    if topics:
        out += ["", "## Standing topics", ""]
        out += [f"- [{t['title']}]({site_url}/topics/{t['slug']}/) {t.get('blurb', '')}".rstrip()
                for t in topics]
    if runs:
        out += ["", "## Recent articles", ""]
        for r in runs[:20]:
            md = f"{site_url}/archive/{r['date']}/index.md"
            out.append(f"- [{r['title']}]({site_url}/archive/{r['date']}/) "
                       f"{r['date']}. Markdown: {md}")
    return "\n".join(out) + "\n"


def llms_full_txt(site_url: str, runs: list) -> str:
    """Every deck's Markdown in one file, newest first. One fetch, whole corpus."""
    head = [f"# Alaska AI, full text corpus",
            "",
            f"Every article published by Alaska AI, newest first, generated "
            f"{ddate.today().isoformat()}.",
            f"Canonical pages live under {site_url}/archive/.",
            ""]
    return "\n".join(head) + "\n\n---\n\n".join(
        deck_markdown(r, site_url) for r in runs) + "\n"


# ---------- feeds ----------

def _item_html(r, site_url: str) -> str:
    """Full article HTML for a feed item. Feed readers get the whole story."""
    parts = []
    if r.get("hook"):
        parts.append(f"<p><em>{xesc(r['hook'])}</em></p>")
    parts.append(
        f'<p><img src="{xesc(r["cover"])}" alt="{xesc(r["title"])} cover slide" '
        f'width="1080" height="1350"></p>' if r.get("cover") else "")
    for para in (r.get("article_text") or "").split("\n\n"):
        if para.strip():
            parts.append(f"<p>{xesc(para.strip())}</p>")
    srcs = _sources(r)
    if srcs:
        parts.append("<h3>Sources</h3><ul>")
        for c in srcs:
            outlet = xesc(c.get("source_outlet") or "source")
            kind = "primary document" if c.get("source_is_primary") else "report"
            parts.append(f'<li><a href="{xesc(c["source_url"])}">{outlet}</a>, {kind}</li>')
        parts.append("</ul>")
    parts.append(f'<p><a href="{site_url}/archive/{r["date"]}/">'
                 f"Read the full deck with all {r['slides']} slides</a></p>")
    return "".join(p for p in parts if p)


def rss(site_url: str, runs: list) -> str:
    items = []
    for r in runs[:MAX_ITEMS]:
        url = f"{site_url}/archive/{r['date']}/"
        items.append(f"""<item>
<title>{xesc(r['title'])}</title>
<link>{url}</link>
<guid isPermaLink="true">{url}</guid>
<pubDate>{rfc822(r['date'])}</pubDate>
<description>{xesc(r.get('summary') or r.get('hook') or '')}</description>
<content:encoded><![CDATA[{_item_html(r, site_url)}]]></content:encoded>
<dc:creator>Alaska AI</dc:creator>
</item>""")
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>Alaska AI</title>
<link>{site_url}/</link>
<atom:link href="{site_url}/feed.xml" rel="self" type="application/rss+xml"/>
<description>One verified Alaska and AI story a day. Every fact checked against a fetched primary source.</description>
<language>en-us</language>
<copyright>Alaska AI</copyright>
<lastBuildDate>{now}</lastBuildDate>
<generator>site_build.py</generator>
{chr(10).join(items)}
</channel>
</rss>
"""


def atom(site_url: str, runs: list) -> str:
    entries = []
    for r in runs[:MAX_ITEMS]:
        url = f"{site_url}/archive/{r['date']}/"
        entries.append(f"""<entry>
<title>{xesc(r['title'])}</title>
<link href="{url}"/>
<id>{url}</id>
<updated>{rfc3339(r['date'])}</updated>
<published>{rfc3339(r['date'])}</published>
<author><name>Alaska AI</name></author>
<summary>{xesc(r.get('summary') or r.get('hook') or '')}</summary>
<content type="html">{xesc(_item_html(r, site_url))}</content>
</entry>""")
    updated = rfc3339(runs[0]["date"]) if runs else datetime.now(
        timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<title>Alaska AI</title>
<subtitle>One verified Alaska and AI story a day.</subtitle>
<link href="{site_url}/atom.xml" rel="self"/>
<link href="{site_url}/"/>
<id>{site_url}/</id>
<updated>{updated}</updated>
<author><name>Alaska AI</name></author>
{chr(10).join(entries)}
</feed>
"""


def json_feed(site_url: str, runs: list) -> str:
    return json.dumps({
        "version": "https://jsonfeed.org/version/1.1",
        "title": "Alaska AI",
        "home_page_url": f"{site_url}/",
        "feed_url": f"{site_url}/feed.json",
        "description": "One verified Alaska and AI story a day. Every fact checked "
                       "against a fetched primary source.",
        "language": "en-US",
        "authors": [{"name": "Alaska AI", "url": f"{site_url}/about/"}],
        "items": [{
            "id": f"{site_url}/archive/{r['date']}/",
            "url": f"{site_url}/archive/{r['date']}/",
            "title": r["title"],
            "summary": r.get("summary") or r.get("hook") or "",
            "content_html": _item_html(r, site_url),
            "content_text": r.get("article_text") or "",
            "date_published": rfc3339(r["date"]),
            **({"image": r["cover"]} if r.get("cover") else {}),
            "tags": [t.lstrip("#") for t in (r.get("hashtags") or [])[:8]],
            # The sources behind the item, so an agent consuming the feed can
            # check the work without fetching the page.
            "_alaska_ai": {
                "slides": r["slides"],
                "claims_verified": len(r.get("claims") or {}),
                "sources": [{"url": c["source_url"],
                             "outlet": c.get("source_outlet") or "",
                             "primary": bool(c.get("source_is_primary"))}
                            for c in _sources(r)],
            },
        } for r in runs[:MAX_ITEMS]],
    }, indent=2) + "\n"


def docket_rss(site_url: str, items: list) -> str:
    """Every tracked Alaska AI decision as it moves.

    This is the feed with no competition. The docket is already maintained
    every run and already published as open JSON; this makes it subscribable,
    which is what turns a page people visit into a thing people follow.

    Sorted by last_updated so a subscriber sees movement, not the docket's
    internal ordering. The guid carries the update date, so an item that moves
    resurfaces in a reader instead of staying silently read."""
    rows = []
    for d in sorted(items, key=lambda d: d.get("last_updated") or "", reverse=True):
        did = d.get("id") or ""
        when = (d.get("last_updated") or d.get("first_seen") or "")[:10]
        try:
            pub = rfc822(when)
        except Exception:
            continue
        bits = [b for b in (d.get("status"), d.get("decider"), d.get("location")) if b]
        desc = " ".join(x for x in [d.get("summary") or "", d.get("access_note") or ""] if x)
        if bits:
            desc = f"{desc} Status, {bits[0]}." if desc else f"Status, {bits[0]}."
        rows.append(f"""<item>
<title>{xesc(d.get('title') or did)}</title>
<link>{site_url}/docket/#{xesc(did)}</link>
<guid isPermaLink="false">alaska-ai-docket-{xesc(did)}-{xesc(when)}</guid>
<pubDate>{pub}</pubDate>
<category>{xesc(d.get('kind') or 'decision')}</category>
<description>{xesc(desc.strip())}</description>
</item>""")
    items = rows[:MAX_ITEMS]
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>Alaska AI Docket</title>
<link>{site_url}/docket/</link>
<atom:link href="{site_url}/docket/feed.xml" rel="self" type="application/rss+xml"/>
<description>Every AI infrastructure decision tracked in Alaska, as it moves. Comment windows, deadlines, votes and filings.</description>
<language>en-us</language>
<lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
"""


# ---------- gate ----------

def validate(name: str, text: str, fail) -> None:
    """Refuse to ship a feed that will not parse.

    A malformed feed is worse than no feed: readers cache the failure and stop
    polling. This parses what was actually generated and checks the item count
    is plausible, rather than trusting the template."""
    if name.endswith(".json"):
        try:
            d = json.loads(text)
        except Exception as exc:                                  # noqa: BLE001
            return fail(f"{name} is not valid JSON: {exc}")
        if not d.get("items"):
            return fail(f"{name} has no items")
        return
    try:
        from xml.etree import ElementTree
        root = ElementTree.fromstring(text)
    except Exception as exc:                                      # noqa: BLE001
        return fail(f"{name} is not well-formed XML: {exc}")
    n = len(root.findall(".//item")) or len(
        root.findall("{http://www.w3.org/2005/Atom}entry"))
    if not n:
        return fail(f"{name} parsed but contains no items")
    if re.search(r"[–—‘’“”]", text):
        return fail(f"{name} contains banned punctuation")
