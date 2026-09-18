"""Reproduce the monthly job: extend weather, reject an unchanged fit, validate."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import gaswatch_collect as gc
import gaswatch_fit as fit


class FitRefreshTests(unittest.TestCase):
    def test_unchanged_fit_refreshes_only_backtests_and_is_idempotent(self):
        model = gc.load_model(gc.MODEL_CONFIG)
        metadata, history = gc.load_hdd_history(model, fit.REPO)
        end = date.fromisoformat(history[-1][0])
        extended = history + [((end + timedelta(days=i)).isoformat(), 0.0) for i in range(1, 45)]
        rows = [(30, h, model["base_mmcfd"]*30 + model["slope_mmcfd_per_hdd"]*h)
                for h in range(0, 1800, 30)]
        self.assertIsNone(fit.evaluate(model, rows)[0])
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "model.json"
            path.write_text(json.dumps(model))
            with patch.object(sys, "argv", ["fit", "--model", str(path)]), \
                    patch.object(fit, "observations", return_value=rows), \
                    patch.object(gc, "load_hdd_history", return_value=(metadata, extended)), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(fit.main(), 0)
                new = json.loads(path.read_text())
                self.assertNotEqual(new["backtests"], model["backtests"])
                self.assertEqual({k:v for k,v in new.items() if k != "backtests"},
                                 {k:v for k,v in model.items() if k != "backtests"})
                facts = gc.backtest_facts(new, extended)
                for bt in new["backtests"]:
                    for k, v in bt.items():
                        if k.startswith("expect_") and k[7:] in facts[bt["id"]]:
                            self.assertEqual(v, facts[bt["id"]][k[7:]])
                before = path.stat().st_mtime_ns
                self.assertEqual(fit.main(), 0)
                self.assertEqual(path.stat().st_mtime_ns, before)

    def test_dry_run_preserves_model_bytes(self):
        model = gc.load_model(gc.MODEL_CONFIG)
        model["backtests"][-1]["expect_mmcfd"] = -1
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "model.json"
            path.write_text(json.dumps(model))
            original = path.read_bytes()
            with patch.object(sys, "argv", ["fit", "--model", str(path), "--dry-run"]), \
                    patch.object(fit, "evaluate", return_value=(None, "no change")), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(fit.main(), 0)
            self.assertEqual(path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
