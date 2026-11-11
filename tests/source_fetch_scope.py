"""Archive rebuilding stays offline; old citations and live work remain intact.

The agent fetch policy lives in the daily prompt, not in a URL crawler. These
checks pin the existing code behavior that makes skipping archival refetches
safe. They do not claim to measure or enforce the agent's billed token usage.
"""
import copy
import datetime as dt
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import docket_staleness
import site_build
import site_signoff


class SourceFetchScopeTests(unittest.TestCase):
    def test_archive_keeps_old_and_recent_citations_without_network(self):
        today = dt.date(2026, 11, 11)
        runs = []
        for age in (0, 29, 30, 120):
            runs.append({
                "date": (today - dt.timedelta(days=age)).isoformat(),
                "claims": {"C01": {
                    "claim": "A recorded source claim",
                    "source_url": f"https://example.invalid/record/{age}",
                    "source_outlet": "Example Agency",
                    "source_is_primary": True,
                    "date_of_source": "2025-01-01",
                }},
            })
        before = copy.deepcopy(runs)
        with patch("socket.socket.connect", side_effect=AssertionError("network forbidden")), \
                patch("urllib.request.urlopen", side_effect=AssertionError("fetch forbidden")):
            html = site_build.sources_page(today, "https://alaskaaihq.com", runs)
        self.assertEqual(runs, before)
        for age in (0, 29, 30, 120):
            self.assertEqual(html.count(f'href="https://example.invalid/record/{age}"'), 1)
        self.assertIn("4 VERIFIED CLAIMS &middot; 4 DOCUMENTS", html)
        self.assertNotIn("example.invalid", " ".join(site_signoff.internal_links(html)))

    def test_multiple_claims_keep_one_source_link_and_all_claim_counts(self):
        claims = {f"C{n}": {"claim": f"Claim {n}",
                             "source_url": "https://example.invalid/shared",
                             "source_outlet": "Example Agency",
                             "source_is_primary": True,
                             "date_of_source": "2025-01-01"}
                  for n in range(1, 4)}
        html = site_build.sources_page(dt.date(2026, 11, 11), "https://alaskaaihq.com",
                                      [{"date": "2026-01-01", "claims": claims}])
        self.assertEqual(html.count('href="https://example.invalid/shared"'), 1)
        self.assertIn("3 VERIFIED CLAIMS &middot; 1 DOCUMENTS", html)

    def test_old_live_docket_item_is_not_retired_by_archive_age(self):
        item = {"id": "ongoing-permit", "status": "pending-decision",
                "last_updated": "2026-11-01",
                "key_dates": [{"date": "2026-01-01", "kind": "milestone"}]}
        row = docket_staleness.assess(item, dt.date(2026, 11, 11))
        self.assertTrue(row["rotten"])
        self.assertTrue(row["reasons"])
        self.assertTrue(row["no_scheduled_event"])

    def test_near_deadline_remains_due(self):
        item = {"id": "open-comments", "status": "open-for-comment",
                "last_updated": "2026-11-10",
                "key_dates": [{"date": "2026-11-12", "kind": "deadline"}]}
        row = docket_staleness.assess(item, dt.date(2026, 11, 11))
        self.assertIn("key date in 1d", row["reasons"])


if __name__ == "__main__":
    unittest.main()
