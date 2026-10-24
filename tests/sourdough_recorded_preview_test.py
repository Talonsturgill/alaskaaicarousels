"""Exact hosted replay boundary; no exception to ordinary publication gates."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import os
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
MARKER = 'sourdough-recorded-exception-v1'
EXPECTED_SHA256 = '308c7f48f692428b6f0678a88a57b9c8e0e05e7d7ef75333e83b2c1b854d3f34'


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.meta, self.remote, self.scripts = {}, [], []
        self.script = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta':
            self.meta[a.get('name', a.get('http-equiv', '')).lower()] = a.get('content', '')
        for key in ('src', 'href', 'action', 'data'):
            if key in a and not a[key].startswith(('#', 'data:')):
                self.remote.append((tag, key, a[key]))
        if tag == 'script':
            self.script = ''

    def handle_data(self, text):
        if self.script is not None:
            self.script += text

    def handle_endtag(self, tag):
        if tag == 'script' and self.script is not None:
            self.scripts.append(self.script)
            self.script = None


def validate(relative, data):
    if not re.fullmatch(r'awesomeproposal/[a-f0-9]{36}/index\.html', relative):
        raise ValueError('Opaque dedicated 144-bit preview path required')
    text = data.decode('utf-8')
    p = Page(text)
    if p.meta.get('alaska-ai-concept') != MARKER:
        raise ValueError('Exact standalone marker required')
    if set(p.meta.get('robots', '').split(',')) != {'noindex', 'nofollow', 'noarchive'}:
        raise ValueError('Crawler directives missing')
    for directive in ("default-src 'none'", "connect-src 'none'", "form-action 'none'", "object-src 'none'"):
        if directive not in p.meta.get('content-security-policy', ''):
            raise ValueError('Offline browser policy missing')
    if p.remote:
        raise ValueError('External dependency or form action')
    if re.search(r'/Users/|/tmp/|CODEX_HOME|sqlite_home|team-api|localhost|127\.0\.0\.1|BEGIN .*PRIVATE KEY|\bsk-[A-Za-z0-9_-]{20}', text):
        raise ValueError('Local runtime, secret or backend detail')
    for script in p.scripts:
        if script.startswith('const TEAM_DATA='):
            continue
        if re.search(r'fetch\s*\(|XMLHttpRequest|new WebSocket|sendBeacon', script):
            raise ValueError('Network execution in preview script')
    for label in ('Concept for Sourdough Express', 'Synthetic', 'recorded model run', 'no dispatch authority', '8 of 10 pairs', 'Browser memory only', 'Download local packet', 'No live freight'):
        if label not in text:
            raise ValueError('Required proof or safety label missing')
    return relative.split('/')[1], p


def disclosures(directory, token, exempt=None):
    leaks = []
    for path in directory.rglob('*'):
        if path.is_file():
            rel = path.relative_to(directory).as_posix()
            if rel != exempt:
                data = path.read_bytes()
                if token.encode() in data or MARKER.encode() in data:
                    leaks.append(rel)
    return leaks


class RecordedPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        matches = [(p, p.read_bytes()) for p in (ROOT / 'docs/awesomeproposal').rglob('index.html') if MARKER.encode() in p.read_bytes()]
        if len(matches) != 1:
            raise AssertionError('Exactly one registered recorded preview required')
        cls.path, cls.data = matches[0]
        cls.relative = cls.path.relative_to(ROOT / 'docs').as_posix()
        cls.token, cls.page = validate(cls.relative, cls.data)
        source = next(s for s in cls.page.scripts if s.startswith('const TEAM_DATA='))
        cls.recorded = json.loads(source[len('const TEAM_DATA='):-1])

    def test_01_exact_browser_tested_hosting_bytes(self):
        self.assertEqual(hashlib.sha256(self.data).hexdigest(), EXPECTED_SHA256)

    def test_02_all_served_files_exclude_discovery_links(self):
        self.assertEqual(disclosures(ROOT / 'docs', self.token, self.relative), [])

    def test_03_fresh_generated_outputs_exclude_the_route(self):
        directory = os.environ.get('SOURDOUGH_BUILT_SITE')
        if not directory:
            self.skipTest('Fresh builder output is checked in CI')
        p = Path(directory)
        self.assertTrue((p / 'sitemap.xml').is_file())
        self.assertTrue((p / 'index.html').is_file())
        self.assertEqual(disclosures(p, self.token), [])

    def test_04_genuine_retained_cohort_has_honest_limits(self):
        d = self.recorded
        self.assertEqual(d['ledger'], {'used': 24, 'cap': 24})
        self.assertEqual(d['historical_evaluation'], {'completed_pairs': 8, 'required_pairs': 10, 'new_inference': False})
        self.assertEqual(len(d['runs']), 8)
        self.assertEqual(sum(len(r['authoritative']['validated_facts']) for r in d['runs']), 66)
        for r in d['runs']:
            self.assertEqual(r['execution_kind'], 'genuine retained model run')
            self.assertEqual(r['approvals'], [])
            self.assertEqual(r['exports'], [])
            self.assertNotIn('command', json.dumps(r['role_attempts']))

    def test_05_source_hashes_and_every_fact_span_bind(self):
        cases = {c['key']: c for c in self.recorded['cases']}
        for r in self.recorded['runs']:
            sources = {s['source_id']: s for s in cases[r['scenario']]['data']['sources']}
            self.assertEqual(r['source_fingerprint'], cases[r['scenario']]['data']['source_fingerprint'])
            for s in sources.values():
                self.assertEqual(hashlib.sha256(s['content'].encode()).hexdigest(), s['content_hash'])
            for fact in r['authoritative']['validated_facts']:
                self.assertRegex(fact['fact_id'], r'^FACT-\d{3}$')
                for e in fact['evidence']:
                    s = sources[e['source_id']]
                    self.assertEqual(e['source_hash'], s['content_hash'])
                    quote = s['content'].encode('utf-16-le')[e['start'] * 2:e['end'] * 2].decode('utf-16-le')
                    self.assertEqual(quote, e['quote'])

    def test_06_rejects_missing_crawler_directives(self):
        for word in ('noindex', 'nofollow', 'noarchive'):
            with self.assertRaises(ValueError):
                validate(self.relative, self.data.replace(word.encode(), b''))

    def test_07_rejects_guessable_path_remote_asset_backend_and_local_path(self):
        with self.assertRaises(ValueError):
            validate('awesomeproposal/sourdough/index.html', self.data)
        for bad in (b'<script src="https://example.invalid/a.js"></script>', b'<p>/Users/example/private</p>', b'<script>fetch("/team-api/export")</script>'):
            with self.assertRaises(ValueError):
                validate(self.relative, self.data.replace(b'</head>', bad + b'</head>'))

    def test_08_no_public_robots_feed_catalog_or_navigation_exception(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('index.html', 'sitemap.xml', 'robots.txt', 'feed.json', 'search.json', 'llms.txt', 'awesomeproposal/index.html'):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(self.token)
                self.assertIn(name, disclosures(root, self.token, self.relative))
                path.unlink()


if __name__ == '__main__':
    unittest.main(verbosity=2)
