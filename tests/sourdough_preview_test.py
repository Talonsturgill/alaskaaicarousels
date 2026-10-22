"""Narrow boundary for one independently authored, unlisted synthetic concept.

No ordinary publication gate is bypassed or modified. The page is a standalone
artifact in the existing foreign awesomeproposal surface, not site_build output.
Its opaque path is discovered only in test memory, never emitted as a catalog.
"""
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
MARKER = "sourdough-terminal-handoff-v1"
EXPECTED_SHA256 = "efeea8f2c1cd807f4bbba6913a63769397e52d46b81a16924d86aa8ffa29d470"


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.meta, self.external = {}, []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta":
            key = attrs.get("name", attrs.get("http-equiv", "")).lower()
            self.meta[key] = attrs.get("content", "")
        for key in ("src", "href", "action", "data"):
            if key in attrs and not attrs[key].startswith(("#", "data:")):
                self.external.append((tag, key, attrs[key]))


def validate_page(relative, data):
    if not re.fullmatch(r"awesomeproposal/[a-f0-9]{36}/index\.html", relative):
        raise ValueError("Preview must use a dedicated 144-bit random path")
    html = data.decode("utf-8")
    p = Page(html)
    if p.meta.get("alaska-ai-concept") != MARKER:
        raise ValueError("Exact concept marker required")
    if set(p.meta.get("robots", "").split(",")) != {"noindex", "nofollow", "noarchive"}:
        raise ValueError("All three no-discovery directives are required")
    csp = p.meta.get("content-security-policy", "")
    for directive in ["default-src 'none'", "connect-src 'none'", "object-src 'none'", "form-action 'none'"]:
        if directive not in csp:
            raise ValueError("Offline connection policy required")
    if p.external:
        raise ValueError("Concept must not load external assets or send forms")
    for label in ["ALASKA AI", "SOURDOUGH EXPRESS", "SYNTHETIC SCENARIO", "No live AI", "dispatch authority", "No official affiliation", "Session-local data only"]:
        if label not in html:
            raise ValueError("A required authorship or safety label is missing")
    return relative.split("/")[1]


def disclosures(files, token, exempt):
    # Exempt exactly the validated page, never the whole proposal directory.
    return [name for name, data in files.items()
            if name != exempt and (token.encode() in data or MARKER.encode() in data)]


class BoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        candidates = []
        for p in (ROOT / "docs" / "awesomeproposal").rglob("index.html"):
            data = p.read_bytes()
            if ('name="alaska-ai-concept" content="' + MARKER + '"').encode() in data:
                candidates.append((p, data))
        if len(candidates) != 1:
            raise AssertionError("Exactly one registered Sourdough concept is required")
        cls.path, cls.data = candidates[0]
        cls.relative = cls.path.relative_to(ROOT / "docs").as_posix()
        cls.token = validate_page(cls.relative, cls.data)

    def test_registered_artifact_matches_tested_bytes(self):
        self.assertEqual(hashlib.sha256(self.data).hexdigest(), EXPECTED_SHA256)

    def test_current_public_outputs_do_not_disclose_the_route(self):
        files = {p.relative_to(ROOT / "docs").as_posix(): p.read_bytes()
                 for p in (ROOT / "docs").rglob("*") if p.is_file()}
        self.assertFalse(disclosures(files, self.token, self.relative))

    def test_gate_rejects_each_missing_crawler_directive(self):
        for word in ("noindex", "nofollow", "noarchive"):
            with self.assertRaises(ValueError):
                validate_page(self.relative, self.data.replace(word.encode(), b""))

    def test_gate_rejects_guessable_path_and_remote_dependency(self):
        with self.assertRaises(ValueError):
            validate_page("awesomeproposal/sourdough-express/index.html", self.data)
        with self.assertRaises(ValueError):
            validate_page(self.relative, self.data.replace(b"</head>", b'<script src="https://example.invalid/run.js"></script></head>'))

    def test_no_public_index_or_robots_exception_can_hide_a_leak(self):
        for ordinary in ("index.html", "sitemap.xml", "feed.json", "llms.txt", "search.json", "robots.txt", "awesomeproposal/index.html"):
            self.assertEqual(disclosures({ordinary: self.token.encode()}, self.token, self.relative), [ordinary])
        self.assertEqual(disclosures({self.relative: self.data}, self.token, self.relative), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
