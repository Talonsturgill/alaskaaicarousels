"""Captured malformed CINGSA fields, independent storage and visible failures.

Hermetic: all HTTP calls and the clock are controlled, and writes use tempdirs.
"""
import contextlib
import hashlib
import io
import json
import re
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import gaswatch_collect as gc
import gaswatch_build as gw
import gaswatch_health as health

FIXTURES = Path(__file__).parent / "fixtures" / "cingsa"
META = {"license_label": "CC BY 4.0", "license": "https://creativecommons.org/licenses/by/4.0/",
        "docket_item_id": "cingsa-expansion", "attribution": "Alaska AI",
        "publisher": "Alaska AI", "spatial_coverage": "Southcentral Alaska"}


def replace_cell(raw, label, column, value):
    """Replace one data_item by its source row and numeric column for mutations."""
    row_re = (r'(<tr\b[^>]*>\s*<td\b[^>]*>\s*' + re.escape(label)
              + r'\s*</td>)(.*?)(</tr>)')
    def change(match):
        index = -1
        def cell(item):
            nonlocal index
            index += 1
            return item[1] + value + item[3] if index == column else item[0]
        return match[1] + re.sub(r'(<td class="data_item">)(.*?)(</td>)',
                                 cell, match[2], flags=re.S) + match[3]
    return re.sub(row_re, change, raw, count=1, flags=re.S)


class CingsaFieldTests(unittest.TestCase):
    def setUp(self):
        self.raw = (FIXTURES / "2026-10-23-malformed.html").read_bytes().decode("utf-8")
        self.now = datetime(2026, 10, 23, 19, 32, 33, tzinfo=timezone.utc)
        self.model = gc.load_model(gc.MODEL_CONFIG)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.ledger = Path(self.temp.name) / "gaswatch.jsonl"
        self.snapshot = Path(self.temp.name) / "snapshot"
        self.calls = []

    def fetch(self, probe, **kwargs):
        self.calls.append(probe.name)
        probe.status, probe.http_status = "ok", 200
        probe.attempts, probe.fetched_utc = 1, gc.iso_z(self.now)
        if probe.name == "cingsa_dashboard":
            return self.raw
        if probe.name == "acis_panc_hdd":
            request = json.loads(kwargs["data"])
            start, end = date.fromisoformat(request["sdate"]), date.fromisoformat(request["edate"])
            return json.dumps({"data": [[(start + timedelta(days=d)).isoformat(), "20"]
                for d in range((end - start).days + 1)]})
        if probe.name == "nws_hourly_forecast":
            return json.dumps({"properties": {"updateTime": gc.iso_z(self.now), "periods": [
                {"startTime": f"2026-10-24T{h:02}:00:00-08:00", "temperature": 40,
                 "temperatureUnit": "F"} for h in range(24)]}})
        raise AssertionError(probe.name)

    def run_collector(self):
        self.calls = []
        with patch.object(sys, "argv", ["collector", "--ledger", str(self.ledger),
                                        "--snapshot-dir", str(self.snapshot)]), \
                patch.object(gc, "now_utc", return_value=self.now), \
                patch.object(gc, "http", side_effect=self.fetch), \
                contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return gc.main()

    def test_fixture_is_the_exact_archived_http_200_response(self):
        source = json.loads((FIXTURES / "2026-10-23-source.json").read_text())
        self.assertEqual(source["http_status"], 200)
        self.assertEqual(hashlib.sha256(self.raw.encode()).hexdigest(), source["sha256"])
        self.assertEqual(source["sha256"],
                         "a36c4b616fb8a6670282d3f6770bb267abd6c0b15edac104cf9285b9aae4e905")

    def test_exact_malformed_capacity_preserves_independent_fields(self):
        cin = gc.parse_cingsa(self.raw)
        self.assertEqual(cin["inventory_mcf"], 7682346)
        self.assertEqual(cin["inventory_delta_mcf"], -42967)
        self.assertEqual(cin["inventory_pct_of_design"], 59.1)
        self.assertEqual(cin["withdrawal_available_mcfd"], 123033)
        self.assertEqual(cin["withdrawal_operating_mcfd"], 166000)
        self.assertIsNone(cin["injection_available_mcfd"])
        self.assertIsNone(cin["injection_in_progress_mcfd"])
        self.assertEqual(cin["data_status"], "partial")
        self.assertEqual(cin["field_errors"]["injection_available_mcfd"]["raw_value"], "0]")

    def test_valid_historical_input_is_unchanged(self):
        cin = gc.parse_cingsa(gc.FIXTURE)
        self.assertEqual(cin["inventory_mcf"], 6423571)
        self.assertEqual(cin["inventory_delta_mcf"], 34891)
        self.assertEqual(cin["injection_in_progress_mcfd"], 34892)
        self.assertEqual(cin["withdrawal_operating_mcfd"], 132117)
        self.assertEqual(cin["data_status"], "complete")
        self.assertEqual(cin["field_errors"], {})

    def test_full_cells_and_comma_grouping_are_strict(self):
        for value in ("0]", "12,34", "1,,000", "123.7", "NaN", "Infinity",
                      "1e3", "-1", "١٢٣", "", "100x"):
            with self.subTest(value=value):
                cin = gc.parse_cingsa(replace_cell(self.raw, "Available Capacity", 0, value))
                self.assertIsNone(cin["injection_available_mcfd"])
                self.assertEqual(cin["withdrawal_available_mcfd"], 123033)
                self.assertEqual(cin["inventory_mcf"], 7682346)
        for value in ("0", "123033", "123,033"):
            with self.subTest(valid=value):
                cin = gc.parse_cingsa(replace_cell(self.raw, "Available Capacity", 0, value))
                self.assertEqual(cin["injection_available_mcfd"], int(value.replace(",", "")))

    def test_independent_capacity_errors_and_dependent_values(self):
        for label, column, field in (
                ("Operating Capacity", 0, "injection_operating_mcfd"),
                ("Facility Capacity", 1, "withdrawal_facility_mcfd"),
                ("Physical Restrictions", 1, "withdrawal_restriction_mcfd"),
                ("Available Capacity", 1, "withdrawal_available_mcfd")):
            with self.subTest(field=field):
                cin = gc.parse_cingsa(replace_cell(self.raw, label, column, "bad"))
                self.assertIsNone(cin[field])
                self.assertIn(field, cin["field_errors"])
                self.assertEqual(cin["inventory_mcf"], 7682346)

    def test_unknown_missing_or_reversed_headings_fail_closed(self):
        for old, new in (("Storage Volume (Mcf)", "Storage Volume (MMcf)"),
                         ("Storage Volume (Mcf)", "Volumes"),
                         ("Injection (MCFpd)", ""),
                         ("Withdrawal (MCFpd)", "Withdrawal (MMcf/d)")):
            with self.subTest(heading=new), self.assertRaises(ValueError):
                gc.parse_cingsa(self.raw.replace(old, new))
        reversed_ = self.raw.replace("Injection (MCFpd)", "TEMP")
        reversed_ = reversed_.replace("Withdrawal (MCFpd)", "Injection (MCFpd)")
        with self.assertRaises(ValueError):
            gc.parse_cingsa(reversed_.replace("TEMP", "Withdrawal (MCFpd)"))

    def test_missing_capacity_row_does_not_borrow_from_next_row(self):
        cin = gc.parse_cingsa(self.raw.replace(">Available Capacity</td>", ">Renamed Capacity</td>"))
        self.assertIsNone(cin["injection_available_mcfd"])
        self.assertIsNone(cin["withdrawal_available_mcfd"])
        self.assertEqual(cin["inventory_mcf"], 7682346)

    def test_removed_numeric_cell_never_shifts_withdrawal_into_injection(self):
        cin = gc.parse_cingsa(self.raw.replace('<td class="data_item">0]</td>', ""))
        self.assertIsNone(cin["injection_available_mcfd"])
        self.assertIsNone(cin["withdrawal_available_mcfd"])
        self.assertEqual(cin["inventory_mcf"], 7682346)

    def test_missing_inventory_stamp_and_duplicate_tables_fail_closed(self):
        for raw in (self.raw.replace(">Ending Inventory</td>", ">Renamed Inventory</td>"),
                    self.raw.replace("Last Updated:", "Refreshed:"),
                    self.raw + self.raw):
            with self.subTest(), self.assertRaises(ValueError):
                gc.parse_cingsa(raw)

    def test_malformed_inventory_stays_unverified_and_retries_do_not_stack(self):
        for label in ("Beginning Inventory", "Ending Inventory"):
            for value in ("7,682,346]", "7,,682,346", "7682346.5", "-1", "999999999"):
                with self.subTest(label=label, value=value), self.assertRaises(ValueError):
                    gc.parse_cingsa(replace_cell(self.raw, label, 0, value))
        self.raw = replace_cell(self.raw, "Ending Inventory", 0, "7,682,346]")
        self.assertEqual(self.run_collector(), 2)
        saved = self.ledger.read_bytes()
        record = gc.read_ledger(str(self.ledger))[-1]
        self.assertFalse(record["verified"])
        self.assertEqual(record["cingsa"]["fetch_status"], "parse_failed")
        self.assertFalse(any(record["cingsa"].get(k) is not None for k in gc.MEASURED))
        self.assertIsNone(record["derived"]["storage_withdrawal_mmcfd"])
        self.assertEqual(self.run_collector(), 3)
        self.assertEqual(self.ledger.read_bytes(), saved)

    def test_unverified_day_repairs_append_only_but_source_still_fails(self):
        gc.append_record(str(self.ledger), {"date": "2026-10-23", "verified": False,
            "collected_utc": "2026-10-23T19:00:00Z", "cingsa": {"fetch_status": "parse_failed"}})
        original = self.ledger.read_bytes()
        self.assertEqual(self.run_collector(), 5)
        self.assertTrue(self.ledger.read_bytes().startswith(original))
        record = gc.read_ledger(str(self.ledger))[-1]
        self.assertTrue(record["verified"])
        self.assertEqual(record["supersedes_unverified"], "2026-10-23T19:00:00Z")
        self.assertIn("cingsa_fields_unavailable", record["flags"])
        self.assertEqual(record["sources"][0]["fetch_status"], "partial")
        self.assertEqual(record["sources"][0]["sha256"], hashlib.sha256(self.raw.encode()).hexdigest())
        self.assertEqual((self.snapshot / "cingsa.html").read_bytes(), self.raw.encode())
        self.assertEqual(json.loads((self.snapshot / "source.json").read_text())["field_errors"],
                         record["cingsa"]["field_errors"])
        saved = self.ledger.read_bytes()
        self.assertEqual(self.run_collector(), 5)
        self.assertEqual(self.ledger.read_bytes(), saved)
        self.assertEqual(self.calls, ["cingsa_dashboard"])

    def test_same_stamp_field_repair_is_bounded_and_idempotent(self):
        self.assertEqual(self.run_collector(), 5)
        partial = self.ledger.read_bytes()
        # A hypothetical new source value, never a correction of the fixture.
        corrected = replace_cell(self.raw, "Available Capacity", 0, "100")
        conflict = replace_cell(corrected, "Ending Inventory", 0, "7,000,000")
        self.raw = conflict
        self.assertEqual(self.run_collector(), 0)
        self.assertEqual(self.ledger.read_bytes(), partial)
        self.raw = corrected
        self.assertEqual(self.run_collector(), 0)
        record = gc.read_ledger(str(self.ledger))[-1]
        self.assertEqual(record["cingsa"]["injection_in_progress_mcfd"], 137600)
        self.assertEqual(record["supersedes_posting"], "2026-10-23T09:00:00")
        saved = self.ledger.read_bytes()
        self.assertEqual(self.run_collector(), 0)
        self.assertEqual(self.ledger.read_bytes(), saved)

    def test_bumped_and_older_stamps_do_not_duplicate_partial_data(self):
        self.assertEqual(self.run_collector(), 5)
        saved = self.ledger.read_bytes()
        for stamp in ("10:00", "8:00"):
            with self.subTest(stamp=stamp):
                self.raw = self.raw.replace("10/23/2026 9:00", f"10/23/2026 {stamp}")
                self.assertEqual(self.run_collector(), 5)
                self.assertEqual(self.ledger.read_bytes(), saved)
                self.raw = self.raw.replace(f"10/23/2026 {stamp}", "10/23/2026 9:00")

    def test_stale_partial_source_keeps_current_measurements_empty(self):
        self.now += timedelta(days=3)
        self.assertEqual(self.run_collector(), 2)
        record = gc.read_ledger(str(self.ledger))[-1]
        self.assertFalse(record["verified"])
        self.assertEqual(record["cingsa"]["data_status"], "unavailable")
        self.assertEqual(record["last_published_cingsa"]["inventory_mcf"], 7682346)
        self.assertFalse(any(record["cingsa"].get(k) is not None for k in gc.MEASURED))
        self.assertIn("cingsa_stale", record["flags"])

    def test_announced_maintenance_does_not_excuse_malformed_fields(self):
        raw = gc.FIXTURE.replace("08/03/2026", "09/13/2026")
        cin = gc.parse_cingsa(raw)
        self.assertTrue(gc.maintenance_pause(cin, ["cingsa_stale"], "2026-09-16"))
        cin = gc.parse_cingsa(replace_cell(raw, "Available Capacity", 0, "0]"))
        self.assertFalse(gc.maintenance_pause(cin, ["cingsa_stale"], "2026-09-16"))

    def test_unavailable_withdrawal_capacity_renders_without_a_measurement(self):
        self.raw = replace_cell(self.raw, "Operating Capacity", 1, "bad")
        self.assertEqual(self.run_collector(), 5)
        series = gw.load_series(str(self.ledger))
        body = gw.page_body(self.now.date(), "https://example.test", series, self.model, META)
        self.assertRegex(body, r'gw-num">Unavailable</div>\s*<div class="gw-lab">MMcf/d withdrawal capacity')

    def test_page_and_feed_publish_null_rates_and_health_retains_the_error(self):
        self.assertEqual(self.run_collector(), 5)
        series = gw.load_series(str(self.ledger))
        body = gw.page_body(self.now.date(), "https://example.test", series, self.model, META)
        self.assertIn('gw-hero">59.1', body)
        self.assertRegex(body, r'gw-num">Unavailable</div>\s*<div class="gw-lab">MMcf/d injection rate')
        self.assertRegex(body, r'gw-num">166.0</div>\s*<div class="gw-lab">MMcf/d withdrawal capacity')
        self.assertIn('id="gw-capacity-status"', body)
        self.assertIn("validated independently", body)
        self.assertNotIn(">None<", body)
        self.assertNotIn("0]", body)
        figs = gw.figures(series, self.model)
        self.assertIsNone(figs.get("injection_in_progress_mmcfd"))
        self.assertEqual(gw.numeral_lint(body, gw.allowed_numerals(
            figs, self.model, [META["license_label"], gw.SCHEMA_VERSION], series)), [])
        feed = gw.feed(series, self.model, "https://example.test", self.now.date(), META)
        self.assertEqual(feed["version"], "1.1")
        self.assertEqual(feed["source_status"]["capacity_status"], "partial")
        self.assertIsNone(feed["series"][0]["cingsa"]["injection_available_mcfd"])
        runs = {"workflow_runs": [{"head_branch": "main", "event": "schedule",
            "created_at": gc.iso_z(self.now), "status": "completed", "conclusion": "success"}]}
        report = health.assess(feed, body, gc.parse_cingsa(self.raw), runs, self.now)
        checks = {c["name"]: c["status"] for c in report["checks"]}
        self.assertEqual(checks["source reading published"], "PASS")
        self.assertEqual(checks["source capacity fields valid"], "FAIL")
        self.assertEqual(report["verdict"], "FAIL")


if __name__ == "__main__":
    unittest.main()
