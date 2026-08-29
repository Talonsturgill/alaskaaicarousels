"""Regression for the Docket Ask payload's HTML-script boundary."""

import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import site_build


hostile = "Robot </script><script>window.__ask_pwned=1</script> & record"
payload = {
    "index": [{"id": "hostile", "title": hostile}],
    "facets": {},
    "views": [],
    "try": [],
    "near": {"places": []},
}

original = site_build.ask_answers.build
try:
    site_build.ask_answers.build = lambda _today: payload
    html = site_build.ask_html(date(2026, 8, 28))
finally:
    site_build.ask_answers.build = original

assert "</script><script>window.__ask_pwned" not in html
match = re.search(r'<script type="application/json" id="qdata">(.*?)</script>', html, re.S)
assert match, "qdata script was not emitted"
assert json.loads(match.group(1))["index"][0]["title"] == hostile
assert html.count('<script type="application/json" id="qdata">') == 1

print("Ask payload stays inside its inert JSON script")
