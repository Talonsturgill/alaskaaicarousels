"""Production failures must stay visible despite green tests or stale evidence."""
import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import cron_health as health
import gate_status


class CronHealthTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 9, 18, 18, tzinfo=timezone.utc)
        self.name = "power.yml"
        self.crons = ["30 15 25 * *"]
        self.run = {"id": 1, "event": "schedule", "head_branch": "main",
                    "created_at": "2026-08-25T16:00:00Z", "status": "completed",
                    "conclusion": "success", "html_url": "https://github.com/example/run/1"}
        self.jobs = [{"name": "refresh", "conclusion": "success", "steps": [
            {"name": "collect", "conclusion": "success"}]}]

    def audit(self, runs=None, state="active"):
        return health.assess_workflow(self.name, self.crons, state,
                                      runs or [self.run], self.jobs, self.now)

    def test_monthly_is_not_expected_daily(self):
        self.assertTrue(all(r["status"] == "PASS" for r in self.audit()))
        self.now = datetime(2026, 9, 26, 1, tzinfo=timezone.utc)
        self.assertEqual(self.audit()[1]["status"], "FAIL")

    def test_own_cadence_and_grace(self):
        cutoff = datetime(2026, 9, 18, 10, tzinfo=timezone.utc)
        self.assertEqual(health.last_due(["40 8 3 * *", "40 8 18 * *"], cutoff),
                         cutoff.replace(hour=8, minute=40))
        self.assertEqual(health.last_due(["17 9 * * 1"], cutoff).isoformat(), "2026-09-14T09:17:00+00:00")
        self.assertEqual(health.last_due(["*/15 * * * *"], cutoff).minute, 0)
        self.assertEqual(health.last_due(["0 0 29 2 *"], cutoff).year, 2024)
        with self.assertRaises(ValueError):
            health.last_due(["61 9 * * *"], cutoff)

    def test_green_pr_and_push_do_not_hide_failed_collection(self):
        self.run["conclusion"] = "failure"
        for event in ("push", "pull_request"):
            green = dict(self.run, event=event, created_at="2026-09-18T17:00:00Z", conclusion="success")
            self.assertEqual(self.audit([green, self.run])[2]["status"], "FAIL")
        repair = dict(self.run, event="workflow_dispatch", created_at="2026-09-18T17:00:00Z", conclusion="success")
        self.assertTrue(all(r["status"] == "PASS" for r in self.audit([repair, self.run])))

    def test_manual_run_does_not_mask_stopped_scheduler(self):
        self.now += timedelta(days=10)
        repair = dict(self.run, event="workflow_dispatch", created_at=health.iso(self.now - timedelta(hours=1)))
        self.assertEqual(self.audit([repair, self.run])[1]["status"], "FAIL")
        self.assertEqual(self.audit(state="disabled_inactivity")[0]["status"], "FAIL")

    def test_continued_step_failure_and_skipped_refresh_are_caught(self):
        self.jobs[0]["steps"][0]["conclusion"] = "failure"
        self.assertEqual(self.audit()[3]["status"], "FAIL")
        self.jobs[0]["steps"][0]["conclusion"] = "skipped"
        self.jobs[0]["conclusion"] = "skipped"
        self.assertEqual(self.audit()[3]["status"], "FAIL")

    def test_retry_must_complete_and_stuck_jobs_fail(self):
        running = dict(self.run, event="workflow_dispatch", created_at=health.iso(self.now - timedelta(minutes=10)),
                       status="in_progress", conclusion=None)
        self.assertEqual(self.audit([running, self.run])[2]["status"], "WARN")
        self.run["conclusion"] = "failure"
        self.assertEqual(self.audit([running, self.run])[2]["status"], "FAIL")
        self.run["conclusion"] = "success"
        running["created_at"] = health.iso(self.now - timedelta(hours=3))
        self.assertEqual(self.audit([running, self.run])[2]["status"], "FAIL")

    def test_new_schedules_are_discovered(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / ".github/workflows"
            path.mkdir(parents=True)
            (path / "new.yml").write_text('name: future\non:\n  schedule:\n    - cron: "0 6 * * *"\n')
            (path / "test.yml").write_text('name: tests\non: [push]\n')
            with patch.object(health, "REPO", Path(td)):
                self.assertEqual(health.inventory(), {"new.yml": ["0 6 * * *"]})

    def test_current_deployment_with_stale_gas_inputs_is_not_healthy(self):
        model = {"base_mmcfd": 80, "backtests": [{"expect_mmcfd": 169}]}
        history = {"end_date": "2026-09-17", "days": 4643}
        eia = {"latest_month": "202606"}
        feed = {"model": dict(model, hdd_history_end=history["end_date"], hdd_history_days=history["days"]),
                "crosscheck": {"eia_latest_month": eia["latest_month"]}}
        self.assertTrue(health.gas_model_published(feed, model, eia, history))
        for mutate in (lambda f: f["model"].update(base_mmcfd=81),
                       lambda f: f["model"].update(hdd_history_end="2026-08-04"),
                       lambda f: f["crosscheck"].update(eia_latest_month="202605")):
            stale = copy.deepcopy(feed)
            mutate(stale)
            self.assertFalse(health.gas_model_published(stale, model, eia, history))

    def test_missing_stale_incomplete_and_blanket_waivers_fail(self):
        workflows = {self.name: self.crons}
        report = {"schema_version": 1, "repository": health.REPOSITORY,
                  "site_url": health.SITE, "checked_utc": health.iso(self.now), "workflows": workflows,
                  "checks": [health.row(i, True, "checked") for i in sorted(health.expected_ids(workflows))]}
        self.assertEqual(health.gate(report, None, workflows, self.now)[0], "PASS")
        for mutate in (lambda d: d.update(checked_utc=health.iso(self.now-timedelta(days=2))),
                       lambda d: d["checks"].pop(),
                       lambda d: d["checks"].append(d["checks"][0]),
                       lambda d: d.update(site_url="http://localhost:8796")):
            bad = copy.deepcopy(report)
            mutate(bad)
            self.assertEqual(health.gate(bad, None, workflows, self.now)[0], "FAIL")
        report["checks"][0]["status"] = "FAIL"
        report["checks"][1]["status"] = "FAIL"
        incident = {"audit_checked_utc": report["checked_utc"], "blocker": "upstream",
                    "reason": "upstream unavailable", "attempts": ["retried source"],
                    "evidence_urls": ["https://example.org/source"], "check_ids": [report["checks"][0]["id"]]}
        self.assertEqual(health.gate(report, [incident], workflows, self.now)[0], "FAIL")
        incident["check_ids"].append(report["checks"][1]["id"])
        self.assertEqual(health.gate(report, [incident], workflows, self.now)[0], "WARN")
        incident["audit_checked_utc"] = health.iso(self.now-timedelta(days=1))
        self.assertEqual(health.gate(report, [incident], workflows, self.now)[0], "FAIL")

    def test_daily_gate_requires_the_new_artifact_without_rewriting_history(self):
        with tempfile.TemporaryDirectory() as td:
            for date, expected in [("2026-09-18", []), ("2026-09-19", ["FAIL"])]:
                run = Path(td) / date
                run.mkdir()
                rows = gate_status.Rows(True)
                gate_status.cron_health_row(rows, run)
                self.assertEqual([r["status"] for r in rows.rows], expected)


if __name__ == "__main__":
    unittest.main()
