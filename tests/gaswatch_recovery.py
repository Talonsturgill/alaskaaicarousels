"""Regression checks for the September source pause, without network or git writes."""
import contextlib
import io
import json
import re
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import gaswatch_collect as gc
import gaswatch_build as gw


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.raw = re.sub(r"\d{2}/\d{2}/2026 \d{2}:\d{2}",
                          "09/13/2026 21:00", gc.FIXTURE)
        self.raw = self.raw.replace("from 14 Sept.", "from 14; Sept.")
        self.cin = gc.parse_cingsa(self.raw)
        self.now = datetime(2026, 9, 16, 23, tzinfo=timezone.utc)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.ledger = Path(self.temp.name) / "gaswatch.jsonl"
        self.snapshot = Path(self.temp.name) / "snapshot"
        for day in (13, 15, 16):
            gc.append_record(str(self.ledger), {
                "date": f"2026-09-{day}", "verified": day == 13,
                "collected_utc": f"2026-09-{day}T22:00:00Z",
                "cingsa": dict(self.cin), "forecast": [],
                "derived": {"storage_withdrawal_mmcfd": -34.9,
                            "days_cover_at_peak": 55}, "flags": []})

    def fetch(self, probe, **kwargs):
        probe.status, probe.http_status = "ok", 200
        probe.attempts, probe.fetched_utc = 1, gc.iso_z(self.now)
        if probe.name == "cingsa_dashboard":
            return self.raw
        if probe.name == "acis_panc_hdd":
            return json.dumps({"data": [[f"2026-09-{d}", "12"]
                                        for d in (13, 14, 15)]})
        if probe.name == "nws_hourly_forecast":
            return json.dumps({"properties": {"updateTime": gc.iso_z(self.now),
                "periods": [{"startTime": f"2026-09-17T{h:02}:00:00-08:00",
                             "temperature": 45, "temperatureUnit": "F"}
                            for h in range(24)]}})
        raise AssertionError(probe.name)

    def run_collector(self):
        with patch.object(sys, "argv", ["collector", "--ledger", str(self.ledger),
                                        "--snapshot-dir", str(self.snapshot)]), \
                patch.object(gc, "now_utc", return_value=self.now), \
                patch.object(gc, "http", side_effect=self.fetch), \
                contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return gc.main()

    def test_recovery_is_append_only_and_idempotent(self):
        original = self.ledger.read_bytes()
        self.assertEqual(self.run_collector(), 4)
        self.assertTrue(self.ledger.read_bytes().startswith(original))
        records = gc.read_ledger(str(self.ledger))
        for day in (14, 15, 16):
            record = gc.standing(records, f"2026-09-{day}")
            self.assertFalse(record["verified"])
            self.assertNotIn("inventory_mcf", record["cingsa"])
            self.assertIsNone(record["derived"].get("storage_withdrawal_mmcfd"))
            self.assertIsNone(record["derived"].get("days_cover_at_peak"))
        self.assertEqual(gc.standing(records, "2026-09-14")["forecast"], [])
        self.assertIsNone(gc.standing(records, "2026-09-14")["collected_utc"])
        observed = gc.reconciliation_index(records)
        for day in (14, 15):
            block = observed[f"2026-09-{day}"]
            self.assertEqual(block["actual_hdd65"], 12)
            self.assertIsNotNone(block["modeled_demand_mmcfd"])
            self.assertIsNone(block["non_cingsa_supply_mmcfd"])
        self.assertEqual((self.snapshot / "cingsa.html").read_text(), self.raw)
        self.assertEqual(json.loads((self.snapshot / "source.json").read_text())["http_status"], 200)
        saved = self.ledger.read_bytes()
        self.assertEqual(self.run_collector(), 4)
        self.assertEqual(self.ledger.read_bytes(), saved)
        series = gw.load_series(str(self.ledger))
        model = gc.load_model(gc.MODEL_CONFIG)
        table = gw.table_html(series, model)
        for day in (14, 15, 16):
            self.assertIn(f'<tr><td>2026-09-{day}</td><td>Unavailable</td>', table)
        self.assertEqual(gw.source_status(series, self.now.date())["state"], "announced_maintenance")
        self.assertEqual(gw.figures(series, model)["peak_forecast_date"], "2026-09-17")

    def test_return_date_still_fails_a_stale_source(self):
        self.now = datetime(2026, 9, 21, 23, tzinfo=timezone.utc)
        self.assertEqual(self.run_collector(), 2)
        last = gc.standing(gc.read_ledger(str(self.ledger)), "2026-09-21")
        self.assertFalse(last["verified"])
        self.assertNotIn("announced_maintenance_window", last["flags"])

    def test_maintenance_does_not_mask_other_failures(self):
        self.assertTrue(gc.maintenance_pause(self.cin, ["cingsa_stale"], "2026-09-16"))
        self.assertFalse(gc.maintenance_pause(self.cin, [], "2026-09-16"))
        self.assertFalse(gc.maintenance_pause(self.cin, ["cingsa_stale"], "2026-09-21"))
        self.assertFalse(gc.maintenance_pause(dict(self.cin, source_timestamp="2026-08-13T21:00:00"),
                                             ["cingsa_stale"], "2026-09-16"))
        for failure in ("failed", "parse_failed"):
            self.assertFalse(gc.maintenance_pause(dict(self.cin, fetch_status=failure),
                                                 ["cingsa_stale"], "2026-09-16"))
        for note in ("maintenance", self.cin["operational_note"].replace("21 Sept.", "99 Sept."),
                     self.cin["operational_note"].replace("21 Sept.", "13 Sept.")):
            self.assertIsNone(gc.maintenance_window(note))

    def test_source_can_repair_an_unverified_date(self):
        self.assertEqual(gc.what_to_do({"verified": False, "cingsa": {}}, True,
                                      "2026-09-16T09:00:00")[0], "repair")


if __name__ == "__main__":
    unittest.main()
