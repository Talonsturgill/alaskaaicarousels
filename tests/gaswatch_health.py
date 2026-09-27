"""The daily AI audit must detect the live failures that local builds miss."""
import copy
import json
import re
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import gaswatch_collect as gc
import gaswatch_health as health
import gate_status


class HealthTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 9, 16, 23, tzinfo=timezone.utc)
        raw = re.sub(r"\d{2}/\d{2}/2026 \d{2}:\d{2}", "09/13/2026 21:00", gc.FIXTURE)
        self.source = gc.parse_cingsa(raw)
        self.feed = {"count": 4, "series": [
            {"date": "2026-09-13", "verified": True, "cingsa": self.source},
            *[{"date": f"2026-09-{d}", "verified": False, "cingsa": {}}
              for d in (14, 15, 16)]]}
        self.feed["series"][-1].update({
            "forecast": [{"date": "2026-09-17", "hdd65": 20}], "forecast_source_updated": gc.iso_z(self.now),
            "reconciliation_trueups": [{"date": "2026-09-13", "actual_hdd65": 12,
                                        "non_cingsa_supply_mmcfd": 120},
                                       {"date": "2026-09-14", "actual_hdd65": 10}]})
        self.page = '<div class="gw-hero">49.4</div><p id="gw-source-status">Unavailable</p>'
        self.feed["model"] = gc.load_model(gc.MODEL_CONFIG)
        self.page += (f'<div class="gw-num">{gc.demand(20, self.feed["model"])}</div>'
                      '<div class="gw-lab">MMcf/d modeled peak ahead</div>')
        self.runs = {"workflow_runs": [{"head_branch": "main", "event": "schedule",
            "created_at": gc.iso_z(self.now - timedelta(hours=1)), "status": "completed",
            "conclusion": "success", "html_url": "https://github.com/example/run/1"}]}

    def audit(self):
        return health.assess(self.feed, self.page, self.source, self.runs, self.now)

    def test_disclosed_maintenance_is_not_current_storage(self):
        report = self.audit()
        self.assertEqual(report["verdict"], "MAINTENANCE")
        self.assertFalse(any(c["status"] == "FAIL" for c in report["checks"]))

    def test_each_original_failure_is_detected(self):
        baseline = (copy.deepcopy(self.feed), self.page, copy.deepcopy(self.runs))
        defects = (
            lambda: self.feed["series"].pop(1),
            lambda: self.feed["series"][-1]["cingsa"].update(inventory_mcf=123),
            lambda: setattr(self, "page", self.page.replace('id="gw-source-status"', 'id="missing"')),
            lambda: setattr(self, "page", self.page.replace("49.4", "50.0")),
            lambda: setattr(self, "page", self.page.replace('gw-num">', 'missing-num">')),
            lambda: self.runs["workflow_runs"][0].update(conclusion="failure"),
            lambda: self.runs["workflow_runs"][0].update(created_at="2026-09-14T00:00:00Z"),
            lambda: self.feed["series"][-1].update(forecast_source_updated="2026-09-13T00:00:00Z"),
            lambda: self.feed["series"][-1].update(reconciliation_trueups=[]),
        )
        for i, defect in enumerate(defects):
            with self.subTest(defect=i):
                self.feed, self.page, self.runs = copy.deepcopy(baseline)
                defect()
                self.assertEqual(self.audit()["verdict"], "FAIL")

    def test_upstream_staleness_after_return_date_is_failure(self):
        self.now = datetime(2026, 9, 21, 23, tzinfo=timezone.utc)
        report = self.audit()
        self.assertEqual(next(c for c in report["checks"] if c["name"] == "source freshness")["status"], "FAIL")

    def test_one_blocked_endpoint_does_not_hide_the_others(self):
        """2026-09-27: CINGSA's firewall answered the source fetch with a 307
        and the audit reported one row. Every endpoint that answered must still
        be checked, and the blocked one must FAIL, never read as healthy."""
        names = lambda r: {c["name"]: c["status"] for c in r["checks"]}
        for key, label in (("source", "source reachable"), ("feed", "live JSON reachable"),
                           ("page", "live page reachable"), ("runs", "cron runs reachable")):
            with self.subTest(blocked=key):
                parts = {"feed": self.feed, "page": self.page, "source": self.source, "runs": self.runs}
                parts[key] = None
                report = health.assess(parts["feed"], parts["page"], parts["source"], parts["runs"],
                                       self.now, {key: "HTTPError: HTTP Error 307: Temporary Redirect"})
                got = names(report)
                self.assertEqual(report["verdict"], "FAIL")
                self.assertEqual(got[label], "FAIL")
                self.assertEqual(report["unreachable"], [key])
                if key not in ("page", "feed"):
                    self.assertIn("live headline agrees", got)
                if key != "runs":
                    self.assertIn("cron completed successfully", got)
                if key != "source":
                    self.assertIn("source freshness", got)
                else:
                    self.assertNotIn("source freshness", got)
                    self.assertNotIn("source reading published", got)
                    self.assertIsNone(report["maintenance_window"])

        # a page defect is still caught while the source is blocked
        report = health.assess(self.feed, self.page.replace("49.4", "50.0"), None, self.runs, self.now,
                               {"source": "HTTPError: HTTP Error 307: Temporary Redirect"})
        self.assertEqual(names(report)["live headline agrees"], "FAIL")
        # and a blocked source can't be excused as maintenance
        self.assertEqual(health.assess(self.feed, self.page, None, self.runs, self.now)["verdict"], "FAIL")

    def test_main_reads_each_endpoint_separately(self):
        from urllib.error import HTTPError
        served = {"/gas-watch.json": json.dumps(self.feed, default=str), "/gas-watch/": self.page,
                  "actions/workflows": json.dumps(self.runs)}

        def fake_fetch(url):
            if url == gc.CINGSA_URL:
                raise HTTPError(url, 307, "Temporary Redirect", {}, None)
            return next(v for k, v in served.items() if k in url)

        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "gw.json"
            real, argv = health.fetch, sys.argv
            health.fetch, sys.argv = fake_fetch, ["gaswatch_health.py", "--output", str(out)]
            try:
                self.assertEqual(health.main(), 2)
            finally:
                health.fetch, sys.argv = real, argv
            report = json.loads(out.read_text())
        got = {c["name"]: c["status"] for c in report["checks"]}
        self.assertEqual(got["source reachable"], "FAIL")
        self.assertIn("HTTP Error 307", next(c["detail"] for c in report["checks"]
                                             if c["name"] == "source reachable"))
        for name in ("live dataset", "live headline agrees", "history chart present",
                     "cron is running", "cron completed successfully"):
            self.assertIn(name, got)
        self.assertNotIn("live audit completed", got)

    def test_daily_gate_requires_live_evidence_and_diagnosis(self):
        with tempfile.TemporaryDirectory() as td:
            run = Path(td) / "2026-09-16"
            run.mkdir()

            def verdict():
                rows = gate_status.Rows(True)
                gate_status.gas_watch_live_row(rows, run)
                return rows.rows[0]["status"]

            self.assertEqual(verdict(), "FAIL")
            report = self.audit()
            report.update(checked_utc=gc.iso_z(datetime.now(timezone.utc)), site_url=health.SITE)
            path = run / "gaswatch_health.json"
            path.write_text(json.dumps(report))
            self.assertEqual(verdict(), "WARN")
            report["site_url"] = "http://localhost:8796"
            path.write_text(json.dumps(report))
            self.assertEqual(verdict(), "FAIL")
            report.update(site_url=health.SITE, verdict="FAIL")
            path.write_text(json.dumps(report))
            self.assertEqual(verdict(), "FAIL")
            (run / "gaswatch_incident.json").write_text(json.dumps({
                "blocker": "upstream", "reason": "Source unavailable after retries",
                "attempts": ["retried source and read production job logs"],
                "evidence_urls": [gc.CINGSA_URL]}))
            self.assertEqual(verdict(), "WARN")
            report["checked_utc"] = gc.iso_z(datetime.now(timezone.utc) - timedelta(days=2))
            path.write_text(json.dumps(report))
            self.assertEqual(verdict(), "FAIL")


if __name__ == "__main__":
    unittest.main()
