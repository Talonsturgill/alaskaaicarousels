#!/usr/bin/env python3
"""Rotating Alaska AI, energy and technology headlines, selected without a language model.

Publisher feeds provide titles and source dates. We rank recent coverage from named newsrooms,
group sister outlets, and retain the publisher's headline verbatim. Only headline metadata and bounded excerpts are retained from feeds or official indexes; article pages are never fetched. See knowledge/NEWS_CHIP.md.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import email.utils
import xml.etree.ElementTree as ET
import datetime as dt
import hashlib
import html
import json
import math
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import news_feeds
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'ledger/news/latest.json'
CONFIG = json.loads((ROOT / 'config/news_sources.json').read_text())
NEWS_FEED_URL = CONFIG['public_feed']
SOURCES = CONFIG['sources']
RSS_FEEDS = tuple(CONFIG['feeds'])
UTC = dt.timezone.utc
MAX_AGE = dt.timedelta(days=14)
TRENDING_AGE = dt.timedelta(hours=72)
MAX_CHECK_AGE = dt.timedelta(hours=18)
FIRST_PARTY_GROUPS = frozenset(CONFIG.get('first_party_groups', []))
EDITION_LENGTH = dt.timedelta(hours=6)
STORIES_PER_EDITION = 10
# Matches the existing 01:23, 07:23, 13:23, 19:23 UTC collection schedule.
EDITION_ANCHOR = dt.datetime(1970, 1, 1, 1, 23, tzinfo=UTC)
UA = 'AlaskaAIHQ/1.0 (+https://alaskaaihq.com)'
ALASKA = re.compile(r'\b(?:alaska|alaskan|alaskans|anchorage|fairbanks|juneau|kenai|'
                    r'cook inlet|railbelt|north slope|prudhoe bay|mat[- ]su|'
                    r'palmer|wasilla|kodiak|valdez|ketchikan|sitka|nome|bethel|'
                    r'kotzebue|utqiagvik|eielson|jber|beluga[- ]healy|UAF|UAA)\b', re.I)
BRAND_ONLY = re.compile(r'\bAlaska Airlines?\b', re.I)
TECH = re.compile(r'\b(?:AI|artificial intelligence|machine learning|data[- ]cent(?:er|re)s?|'
                  r'tech(?:nology|nologies)?|semiconductors?|microchips?|robot\w*|'
                  r'autonomous|self[- ]driving|cyber\w*|software|quantum|computing|'
                  r'chatbots?|drones?|unmanned|broadband|surveillance|'
                  r'Flock (?:Safety|cameras?)|Flock[- ]branded|interactive (?:(?:tsunami|hazard|earthquake) )?(?:maps?|tools?))\b', re.I)
ENERGY = re.compile(r'\b(?:energy|electricity|electrical|utilities|natural gas|LNG|'
                    r'gas (?:pipelines?|supply|storage|production|imports?)|'
                    r'power (?:grids?|plants?|lines?|supply|generation|costs?|outages?|links?)|'
                    r'transmission|intertie|hydropower|hydroelectric|geothermal|'
                    r'solar|wind (?:power|farms?|projects?)|renewables?|nuclear|microreactors?|'
                    r'oil (?:and gas|fields?|pipelines?|drilling|production)|battery storage)\b', re.I)

AI = re.compile(r'\b(?:AI|artificial intelligence|machine learning|neural networks?|'
                r'LLMs?|large language models?|OpenAI|ChatGPT|GPT[- ]?\d|'
                r'Anthropic|DeepSeek|Claude Code|generative|deep learning|inference|MLPerf)\b', re.I)
JUNK = re.compile(r'\b(?:stock|shares|price target|earnings|buy rating|sponsored|press release|'
                  r'scholarship|obituary|football|basketball|baseball|betting|webinar|newscast|this day in|time capsule|'
                  r'register now|join theCUBE|\w+ vs\.? \w+)\b', re.I)
STOP = set('a an and are as at be by for from has in into is it of on or over s that the their '
           'this to with alaska alaskan alaskans anchorage fairbanks juneau kenai new'.split())


def stamp(value: dt.datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec='seconds').replace('+00:00', 'Z')


def instant(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('timestamp must include its timezone')
    return parsed.astimezone(UTC)


def source(url: str) -> tuple[str, str] | None:
    """Only named public newsrooms; a suffix must begin at a DNS label boundary."""
    try:
        p = urllib.parse.urlsplit(url)
        if p.scheme not in ('http', 'https') or p.username or p.password or p.port not in (None, 80, 443):
            return None
        if any(ord(c) < 33 for c in url) or '\\' in url:
            return None
        host = p.hostname or ''
        for domain, info in SOURCES.items():
            if host == domain or host.endswith('.' + domain):
                return tuple(info)
    except ValueError:
        pass
    return None


def canonical(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    query = urllib.parse.urlencode([(k, v) for k, v in urllib.parse.parse_qsl(p.query)
                                   if not k.lower().startswith(('utm_', 'fbclid', 'gclid'))])
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, query, ''))


def tokens(title: str) -> set[str]:
    text = title.lower()
    for pattern, replacement in [(r'air[- ]tax(?:is|ies|i)\b|air taxis', 'airtaxi'),
                                  (r'artificial intelligence', 'ai'),
                                  (r'data[- ]cent(?:er|re)s?', 'datacenter'),
                                  (r'\b(?:testing|tests)\b', 'test')]:
        text = re.sub(pattern, replacement, text)
    return {t.rstrip('s') if len(t) > 4 else t for t in re.findall(r'[a-z0-9]+', text)
            if t not in STOP and len(t) > 1}


def related(a: dict, b: dict) -> bool:
    left, right = tokens(a['title']), tokens(b['title'])
    common = left & right
    return len(common) >= 3 and len(common) / math.sqrt(len(left) * len(right)) >= .45


def topics(article: dict) -> tuple[bool, bool]:
    text = article['title'] + ' ' + article.get('summary', '')
    # Alaska Airlines' brand alone is not evidence of an Alaska location.
    alaska = bool(ALASKA.search(BRAND_ONLY.sub('', text)))
    return alaska, bool(AI.search(text))


def eligible(article: dict, now: dt.datetime) -> bool:
    try:
        title = article['title']
        if not isinstance(title, str) or not 20 <= len(title) <= 220 or len(title.split()) > 32:
            return False
        newsroom = source(article['url'])
        summary = article.get('summary', '')
        if not isinstance(summary, str) or len(summary) > 1000 or '<' in summary or '>' in summary:
            return False
        alaska, ai = topics(article)
        if (not newsroom or not article['url'].startswith('https://') or not (alaska and (ai or ENERGY.search(title + ' ' + summary) or TECH.search(title))) or JUNK.search(title)):
            return False
        age = now - instant(article['first_seen_at'])
        if not dt.timedelta(0) <= age < MAX_AGE:
            return False
        # A newly indexed archive article is not new coverage. Reject old dates when the
        # publisher exposes one in the URL. A discovery observation is not a publication date.
        date = re.search(r'/(20\d{2})/(\d{2})/(\d{2})/', article['url'])
        if date:
            day = dt.date(*(int(n) for n in date.groups()))
            if not dt.timedelta(0) <= now.date() - day <= MAX_AGE:
                return False
        return True
    except (KeyError, TypeError, ValueError, OverflowError):
        return False


def rank(articles: list[dict], now: dt.datetime) -> list[dict]:
    unique = {}
    for article in articles:
        if eligible(article, now):
            url = canonical(article['url'])
            # Earliest observation wins even when a feed repeats or re-indexes a URL.
            if url not in unique or article['first_seen_at'] < unique[url]['first_seen_at']:
                unique[url] = {**article, 'url': url}
    rows = list(unique.values())
    scored = []
    for article in rows:
        matches = [a for a in rows if a is article or related(article, a)]
        groups = {source(a['url'])[1] for a in matches if source(a['url'])[1] not in FIRST_PARTY_GROUPS}
        # Identical wire copy carried by many groups is still one piece of reporting.
        distinct = {tuple(sorted(tokens(a['title']))) for a in matches}
        coverage = max(1, min(len(groups), len(distinct)))
        age = (now - instant(article['first_seen_at'])).total_seconds() / 3600
        score = round((1 + math.log2(coverage)) * 2 ** (-age / 24), 6)
        alaska, ai = topics(article)
        priority = (0 if ai else 1 if ENERGY.search(article['title'] + ' ' + article.get('summary', '')) else 2) + (3 if age >= 72 else 0)
        scored.append({**article, 'publisher': source(article['url'])[0],
                       'coverage': coverage, 'score': score, 'priority': priority})
    return sorted(scored, key=lambda a: (a['priority'], source(a['url'])[1] in FIRST_PARTY_GROUPS,
                                         -a['score'], a['first_seen_at'], a['url']))


def edition_start(now: dt.datetime) -> dt.datetime:
    return EDITION_ANCHOR + ((now - EDITION_ANCHOR) // EDITION_LENGTH) * EDITION_LENGTH


def edition_story(data: dict, now: dt.datetime) -> dict | None:
    started = [entry for entry in data.get('editions', []) if instant(entry['starts_at']) <= now]
    return started[-1]['selected'] if started else data.get('selected')


def rotation(articles: list[dict], now: dt.datetime, previous: dict) -> dict:
    """Reconsider the best reusable Alaska stories each slot; vary leads within that pool."""
    start = edition_start(now)
    history = []
    for entry in previous.get('history', [])[-32:]:
        try:
            if (isinstance(entry.get('title'), str) and source(entry['url']) and
                    now - MAX_AGE <= instant(entry['shown_at']) <= now):
                history.append({key: entry[key] for key in ('url', 'title', 'shown_at')})
        except (KeyError, TypeError, ValueError):
            continue
    old_editions = []
    for entry in previous.get('editions', [])[:4]:
        try:
            if not eligible(entry['selected'], now):
                continue
            instant(entry['starts_at'])
            old_editions.append(entry)
            if instant(entry['starts_at']) <= now:
                history.append({'url': entry['selected']['url'], 'title': entry['selected']['title'],
                                'shown_at': entry['starts_at']})
        except (KeyError, TypeError, ValueError):
            continue
    if not old_editions and not history and previous.get('selected') and previous.get('checked_at'):
        history.append({'url': previous['selected']['url'], 'title': previous['selected']['title'],
                        'shown_at': previous['checked_at']})
    history = sorted({(entry['shown_at'], entry['url']): entry for entry in history}.values(),
                     key=lambda entry: (entry['shown_at'], entry['url']))[-32:]
    editions, used = [], list(history)
    for offset in range(4):
        begins = start + offset * EDITION_LENGTH
        at = max(now, begins)
        # Quality and source age choose membership, never how many times a story ran.
        # The same strong reporting can fill every edition without exhausting the pool.
        pool = []
        for row in rank(articles, at):
            if not any(row['url'] == old['url'] or related(row, old) for old in pool):
                pool.append(row)
            if len(pool) == STORIES_PER_EDITION:
                break
        if not pool:
            break
        old = next((entry for entry in old_editions if entry['starts_at'] == stamp(begins)), None)
        # Retain a queued lead only while it still earns a place in the best current pool.
        chosen = next((row for row in pool if old and row['url'] == old['selected']['url']), None) if offset == 0 else None
        if chosen is None:
            # Repeats are welcome. Least-recently led wins only WITHIN the best pool.
            # Two stories alternate every six hours and can lead again after twelve.
            def last_shown(row):
                return max((entry['shown_at'] for entry in used
                            if row['url'] == entry['url'] or related(row, entry)), default='')
            chosen = min(pool, key=last_shown)
        previous_pool = old.get('stories', []) if old else []
        if (offset == 0 and previous.get('checked_at') and
                edition_start(instant(previous['checked_at'])) == start and
                {row['url'] for row in previous_pool} == {row['url'] for row in pool}):
            # Identical input on a retry keeps the links in the same order.
            by_url = {row['url']: row for row in pool}
            pool = [by_url[row['url']] for row in previous_pool]
        pool = [chosen] + [row for row in pool if row['url'] != chosen['url']]
        editions.append({'starts_at': stamp(begins), 'selected': chosen, 'stories': pool})
        used.append({'url': chosen['url'], 'title': chosen['title'], 'shown_at': stamp(begins)})
    return {'rotation_version': 1, 'carousel_version': 1, 'editions': editions, 'history': history}


def snapshot(payload: dict, now: dt.datetime, previous: dict | None = None, *, rotate=False) -> dict:
    now = instant(stamp(now))
    if not isinstance(payload, dict) or not isinstance(payload.get('articles'), list):
        raise ValueError('news source did not return an article list')
    known = {a['url']: a['first_seen_at'] for a in (previous or {}).get('articles', [])}
    rows = []
    for raw in payload['articles']:
        try:
            if not isinstance(raw, dict) or not isinstance(raw.get('url'), str) or not isinstance(raw.get('title'), str):
                continue
            url = canonical(raw['url'])
            seen = dt.datetime.strptime(raw['seendate'], '%Y%m%dT%H%M%SZ').replace(tzinfo=UTC)
            row = {'title': html.unescape(' '.join(raw['title'].split())), 'url': url,
                   'first_seen_at': min(known.get(url, stamp(seen)), stamp(seen))}
            if isinstance(raw.get('summary'), str):
                row['summary'] = raw['summary']
            if raw.get('feed') in RSS_FEEDS:
                row['feed'] = raw['feed']
            if raw.get('language') == 'English' and eligible(row, now):
                rows.append(row)
        except (KeyError, TypeError, ValueError):
            continue
    # Retain observations for two weeks to keep a repeated URL from resetting its own clock.
    for old in (previous or {}).get('articles', []):
        if eligible(old, now):
            rows.append(old)
    unique = {}
    for article in rows:
        current = unique.setdefault(article['url'], dict(article))
        current['first_seen_at'] = min(current['first_seen_at'], article['first_seen_at'])
    rows = sorted(unique.values(), key=lambda a: a['url'])
    ranked = rank(rows, now)
    selected = ranked[0] if ranked else None
    result = {'_spec': 2, 'checked_at': stamp(now), 'provider': 'Publisher feeds and news indexes',
            'response_sha256': hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(),
            'articles': rows, 'selected': selected,
            'expires_at': stamp(instant(selected['first_seen_at']) + MAX_AGE) if selected else None}
    if rotate:
        result.update(rotation(rows, now, previous or {}))
        result['selected'] = result['editions'][0]['selected'] if result['editions'] else None
        result['expires_at'] = stamp(instant(result['selected']['first_seen_at']) + MAX_AGE) if result['selected'] else None
    return result


def observation_history(data: dict) -> dict:
    """Import source observations without trusting an older schema's derived ranking."""
    if not isinstance(data, dict) or not isinstance(data.get('articles'), list):
        raise ValueError('news history must contain an article list')
    rows = []
    for raw in data['articles']:
        try:
            if not isinstance(raw, dict) or not isinstance(raw.get('title'), str):
                continue
            url = canonical(raw['url'])
            if not url.startswith('https://') or not source(url) or not 20 <= len(raw['title']) <= 220:
                continue
            row = {'title': raw['title'], 'url': url,
                   'first_seen_at': stamp(instant(raw['first_seen_at']))}
            if isinstance(raw.get('summary'), str):
                row['summary'] = raw['summary']
            if raw.get('feed') in RSS_FEEDS:
                row['feed'] = raw['feed']
            rows.append(row)
        except (KeyError, TypeError, ValueError, AttributeError):
            continue
    history = {'articles': rows}
    for key in ('checked_at', 'selected', 'rotation_version', 'carousel_version', 'editions', 'history', 'feed_state'):
        if key in data:
            history[key] = data[key]
    return history


def validate(data: dict) -> None:
    if data.get('_spec') != 2 or data.get('provider') not in ('GDELT and publisher RSS', 'Publisher feeds and news indexes'):
        raise ValueError('unknown news snapshot')
    now = instant(data['checked_at'])
    if data.get('carousel_version') not in (None, 1) or (data.get('carousel_version') == 1 and data.get('rotation_version') != 1):
        raise ValueError('unknown carousel snapshot')
    ranked = rank(data['articles'], now)
    selected = ranked[0] if ranked else None
    if data.get('rotation_version') == 1:
        editions = data.get('editions')
        if not isinstance(editions, list) or len(editions) > 4:
            raise ValueError('invalid rotation queue')
        for offset, entry in enumerate(editions):
            begins = edition_start(now) + offset * EDITION_LENGTH
            at = max(now, begins)
            story = entry['selected']
            if (entry['starts_at'] != stamp(begins) or story not in rank(data['articles'], at) or
                    at - instant(story['first_seen_at']) >= MAX_AGE):
                raise ValueError('rotation contains an invalid or stale headline')
            if data.get('carousel_version') == 1:
                pool = entry.get('stories')
                if not isinstance(pool, list) or not 1 <= len(pool) <= STORIES_PER_EDITION or pool[0] != story:
                    raise ValueError('invalid edition story pool')
                if offset and len(pool) > 1 and (story['url'] == editions[offset - 1]['selected']['url'] or
                        related(story, editions[offset - 1]['selected'])):
                    raise ValueError('consecutive leads repeat despite available alternatives')
                ranked_at = rank(data['articles'], at)
                for index, candidate in enumerate(pool):
                    if candidate not in ranked_at or at - instant(candidate['first_seen_at']) >= MAX_AGE:
                        raise ValueError('carousel contains an invalid or stale headline')
                    if any(candidate['url'] == old['url'] or related(candidate, old) for old in pool[:index]):
                        raise ValueError('carousel repeats a headline or story')
        selected = editions[0]['selected'] if editions else None
    if selected != data['selected']:
        raise ValueError('selected story disagrees with the recorded candidates and ranking')
    expected = stamp(instant(selected['first_seen_at']) + MAX_AGE) if selected else None
    if data['expires_at'] != expected:
        raise ValueError('headline expiry disagrees with its first observation')


def load() -> dict:
    if not STATE.exists():
        return {}
    data = json.loads(STATE.read_text())
    validate(data)
    return data


def public_snapshot(data: dict) -> dict:
    keys = ('_spec', 'checked_at', 'selected', 'expires_at', 'rotation_version', 'carousel_version', 'editions')
    return {key: data[key] for key in keys if key in data}


def markup(today: str, data: dict | None = None) -> str:
    data = load() if data is None else data
    selected = data.get('selected')
    build_start = dt.datetime.combine(dt.date.fromisoformat(today), dt.time(), UTC)
    if selected and build_start >= instant(data['expires_at']):
        selected = None
    e = html.escape
    recent = selected and (build_start - instant(selected['first_seen_at']) >= TRENDING_AGE or
                           build_start - instant(data['checked_at']) > MAX_CHECK_AGE)
    status = ('recent' if recent else 'current') if selected else 'empty'
    label = 'Recent' if recent else 'Trending'
    title = (selected['title'] if selected else 'Explore the latest Alaska reporting')
    publisher = selected['publisher'] if selected else ''
    date = ''
    if selected:
        observed = instant(selected['first_seen_at']).astimezone(ZoneInfo('America/Anchorage'))
        day = observed.day
        suffix = 'th' if 10 <= day % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        date = f'{observed:%B} {day}{suffix}'
    url = selected['url'] if selected else '/archive/'
    first_seen = selected['first_seen_at'] if selected else ''
    description = ('Alaska AI and energy headlines rotate every five seconds and refresh every six hours. '
                   'The date is the publisher date or first observation. Opens the source in a new tab.')
    relevance = {name: pattern.pattern for name, pattern in
                 [('alaska', ALASKA), ('brand', BRAND_ONLY), ('energy', ENERGY),
                  ('tech', TECH), ('ai', AI), ('junk', JUNK)]}
    return (f'<div class="tele news-chip" role="region" aria-roledescription="carousel" '
            f'aria-label="Trending headlines" data-news-status="{status}" '
            f'data-news-feed="{NEWS_FEED_URL}" data-news-max-age-hours="{int(MAX_AGE.total_seconds() / 3600)}" '
            f'data-news-sources="{e(json.dumps(SOURCES), quote=True)}" '
            f'data-news-relevance="{e(json.dumps(relevance), quote=True)}" '
            f'data-news-initial="{e(json.dumps(public_snapshot(data)), quote=True)}" '
            f'data-checked-at="{e(data.get("checked_at", ""), quote=True)}" '
            f'data-first-seen-at="{e(first_seen)}" data-expires-at="{e(data.get("expires_at") or "")}" '
            f'title="{description}"><div class="news-header"><span class="news-label">{label}</span>'
            '<div class="news-controls" hidden>'
            '<button type="button" class="news-prev" aria-label="Previous headline" title="Previous headline">'
            '<svg aria-hidden="true" viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5">'
            '<path d="m10 3-5 5 5 5"/></svg></button>'
            '<button type="button" class="news-next" aria-label="Next headline" title="Next headline">'
            '<svg aria-hidden="true" viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5">'
            '<path d="m6 3 5 5-5 5"/></svg></button></div></div>'
            '<div class="news-slides" aria-live="off">'
            '<div class="news-slide" role="group" aria-roledescription="slide" aria-hidden="false">'
            f'<a class="news-link" href="{e(url, quote=True)}" target="_blank" rel="noopener noreferrer">'
            f'<cite class="news-title">{e(title)}</cite><span class="news-meta">'
            f'<cite class="news-source">{e(publisher)}</cite>'
            f'<time class="news-date" datetime="{e(first_seen)}">{date}</time></span>'
            '<svg class="news-arrow" aria-hidden="true" viewBox="0 0 24 24" width="18" height="18" '
            'fill="none" stroke="currentColor" stroke-width="1.6"><path d="M7 17 17 7M7 7h10v10"/></svg>'
            '</a></div></div></div><script>' + (ROOT / 'scripts/news_runtime.js').read_text() + '</script>')


def rss_articles(body: bytes) -> list[dict]:
    return news_feeds.articles(body)


def collect() -> int:
    now = dt.datetime.now(UTC).replace(microsecond=0)
    previous = {}
    if STATE.exists():
        try:
            previous = observation_history(json.loads(STATE.read_text()))
        except (ValueError, KeyError, TypeError):
            pass
    saved = previous.get('feed_state', {})
    def read_feed(url):
        return url, news_feeds.read(url, saved.get(url, {}), now, format=CONFIG.get('formats', {}).get(url, 'rss'))
    combined, feeds, feed_state = [], [], {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for url, (rows, report, state) in pool.map(read_feed, RSS_FEEDS):
            combined.extend(rows)
            feeds.append(report)
            feed_state[url] = state
    if not any(feed['status'] in ('ok', 'not_modified') for feed in feeds):
        raise OSError('all news feeds failed; previous published snapshot preserved')
    result = snapshot({'articles': combined}, dt.datetime.now(UTC), previous, rotate=True)
    result['feeds'], result['feed_state'] = feeds, feed_state
    validate(result)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    temp = STATE.with_suffix('.tmp')
    temp.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    temp.replace(STATE)
    print(json.dumps({'eligible': len(result['articles']), 'working_feeds': sum(
        feed['status'] in ('ok', 'not_modified') for feed in feeds),
        'editions': [{'starts_at': entry['starts_at'], 'title': entry['selected']['title'],
                      'publisher': entry['selected']['publisher']} for entry in result['editions']]}, ensure_ascii=False))
    return 0


def health_problems(data: dict, now: dt.datetime) -> list[str]:
    """Operational health is separate from the reproducible snapshot/schema check."""
    problems = []
    selected = edition_story(data, now)
    if not selected or now - instant(selected['first_seen_at']) >= MAX_AGE:
        problems.append('no eligible Alaska AI, energy or technology headline is available')
    if not dt.timedelta(minutes=-5) <= now - instant(data['checked_at']) <= MAX_CHECK_AGE:
        problems.append('news collection is overdue or its clock is invalid')
    if sum(feed.get('status') in ('ok', 'not_modified') for feed in data.get('feeds', [])) < 1:
        problems.append('no news feed is available')
    if data.get('rotation_version') == 1:
        editions = data['editions']
        if len(editions) < 2 or instant(editions[-1]['starts_at']) <= now:
            next_candidates = rank(data['articles'], edition_start(now) + EDITION_LENGTH)
            if not (selected and next_candidates and all(
                    row['url'] == selected['url'] or related(row, selected) for row in next_candidates)):
                problems.append('no eligible headline is ready for the next six-hour edition')
        groups = {source(feed['url'])[1] for feed in data.get('feeds', [])
                  if feed.get('status') in ('ok', 'not_modified') and source(feed.get('url', ''))}
        if len(groups) < 2:
            problems.append('fewer than two independent publisher feeds are available')
    return problems


class PublishedHeadline(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chips = []
        self.current = None
        self.field = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'news-chip' in attrs.get('class', '').split():
            self.current = {'title': '', 'source': ''}
            self.chips.append((tag, attrs, self.current))
        if self.current is not None:
            for name in ('title', 'source'):
                if 'news-' + name in attrs.get('class', '').split():
                    self.field = (tag, name)

    def handle_data(self, data):
        if self.current is not None and self.field:
            self.current[self.field[1]] += data

    def handle_endtag(self, tag):
        if self.field and self.field[0] == tag:
            self.field = None
        if self.current is not None and tag == self.chips[-1][0]:
            self.current = None


def live_problems(body: str, now: dt.datetime, expected_check: str | None = None,
                  feed_data: dict | None = None) -> list[str]:
    """Check the shipped integration and its separately published feed. Browser QA runs too."""
    parser = PublishedHeadline()
    parser.feed(body)
    if len(parser.chips) != 1:
        return ['the published homepage does not contain exactly one news bar']
    tag, chip, text = parser.chips[0]
    if tag not in ('a', 'div') or chip.get('data-news-feed') != NEWS_FEED_URL:
        return ['the published homepage is not connected to the independent news feed']
    if not feed_data:
        return ['the public headline feed is unavailable']
    try:
        validate(feed_data)
        problems = health_problems(feed_data, now)
        if expected_check and instant(feed_data['checked_at']) < instant(expected_check):
            problems.append('the collected headline has not reached the public feed')
        return problems
    except (KeyError, TypeError, ValueError) as error:
        return ['invalid public headline feed: ' + str(error)]


def browser_feed_url(timestamp: float) -> str:
    # Match news_runtime.js exactly. A unique probe URL can bypass a stale CDN entry
    # and certify a refresh that has not yet reached an ordinary reader.
    return NEWS_FEED_URL + '?refresh=' + str(int(timestamp // 300))


def check_live(wait_seconds: int = 0, expected_check: str | None = None) -> int:
    url = 'https://' + (ROOT / 'docs/CNAME').read_text().strip() + '/'
    deadline = time.monotonic() + wait_seconds
    previous = None
    while True:
        try:
            request = urllib.request.Request(url, headers={'User-Agent': UA, 'Cache-Control': 'no-cache'})
            with urllib.request.urlopen(request, timeout=20) as response:
                body = response.read(4_000_001)
                if len(body) > 4_000_000:
                    raise ValueError('homepage exceeded response limit')
            feed_request = urllib.request.Request(browser_feed_url(time.time()),
                                                  headers={'User-Agent': UA, 'Cache-Control': 'no-cache'})
            with urllib.request.urlopen(feed_request, timeout=20) as response:
                feed_body = response.read(500_001)
                if len(feed_body) > 500_000:
                    raise ValueError('headline data exceeded response limit')
            problems = live_problems(body.decode('utf-8'), dt.datetime.now(UTC), expected_check,
                                     json.loads(feed_body))
        except (OSError, ValueError) as error:
            problems = [f'could not verify the published headline: {error}']
        if not problems:
            print('news live: a current attributed headline is published')
            return 0
        if problems != previous:
            print('news live: ' + '; '.join(problems), flush=True)
            previous = problems
        if time.monotonic() >= deadline:
            return 1
        time.sleep(min(20, max(0, deadline - time.monotonic())))


def authored_html(body: str) -> str:
    """Leave attributed publisher headlines outside house-copy lints, verbatim."""
    return re.sub(r'(<cite class="news-title">)[^<]*(</cite>)', r'\1\2', body)


def styles() -> str:
    return (ROOT / 'scripts/news_styles.css').read_text()


def self_test() -> int:
    import importlib.util
    import unittest
    spec = importlib.util.spec_from_file_location('news_selection', ROOT / 'tests/news_selection.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    return 0 if unittest.TextTestRunner().run(suite).wasSuccessful() else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--collect', action='store_true')
    action.add_argument('--check', action='store_true')
    action.add_argument('--self-test', action='store_true')
    action.add_argument('--health', action='store_true')
    action.add_argument('--live-check', action='store_true')
    parser.add_argument('--wait-seconds', type=int, default=0)
    parser.add_argument('--expected-check')
    args = parser.parse_args()
    try:
        if args.self_test:
            sys.exit(self_test())
        if args.collect:
            sys.exit(collect())
        if args.live_check:
            if not 0 <= args.wait_seconds <= 2400:
                parser.error('--wait-seconds must be between zero and 2400')
            sys.exit(check_live(args.wait_seconds, args.expected_check))
        if args.health:
            problems = health_problems(load(), dt.datetime.now(UTC))
            print('news health: ' + ('; '.join(problems) if problems else 'current headline and a working feed available'))
            sys.exit(1 if problems else 0)
        validate(load())
        print('news_headlines: recorded selection and expiry verified')
    except (ValueError, KeyError, OSError) as error:
        print(f'news_headlines: {error}', file=sys.stderr)
        sys.exit(1)
