"""Behaviour tests for the web lab runner (tools/qp/lab/web/app.js), run in Node."""

from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path

from tools.qp.lab import get_engine
from tools.qp.lab.registry import list_engines

APP_JS = Path(__file__).resolve().parents[1] / "qp" / "lab" / "web" / "app.js"

# Loads app.js in a sandbox with a stand-in document, then evaluates one expression.
HARNESS = r"""
const fs = require("fs");
const vm = require("vm");
const [appPath, expr] = process.argv.slice(1);
const ctx = { document: { addEventListener: () => {}, getElementById: () => null } };
ctx.window = ctx;
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(appPath, "utf8"), ctx);
process.stdout.write(JSON.stringify(vm.runInContext(expr, ctx)));
"""


def run_js(expr: str):
    out = subprocess.run(
        ["node", "-e", HARNESS, str(APP_JS), expr],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(out.stdout)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class LabFormBoundsTest(unittest.TestCase):
    def test_every_form_value_is_accepted_by_the_backend(self):
        # Oracle: the backend Param schema. A form min below the backend min lets the learner submit
        # a value that /api/lab/run rejects with 400 (pos_sizing Monte Carlo Paths 30 < 50).
        configs = run_js("Object.fromEntries(Object.entries(ENGINE_CONFIGS).map(([k, v]) => [k, v.params]))")
        for engine_id, fields in configs.items():
            engine = get_engine(engine_id)
            self.assertIsNotNone(engine, engine_id)
            for field in fields:
                name = field["id"].removeprefix("p-").replace("-", "_")
                with self.subTest(engine=engine_id, param=name):
                    param = engine.params[name]
                    if field["type"] == "select":
                        self.assertTrue(set(field["options"]) <= set(param.choices or field["options"]))
                        continue
                    if field["type"] == "text":
                        self.assertEqual(param.param_type, "str")
                        self.assertEqual(param.cast(field["value"]), field["value"])
                        continue
                    if param.min_val is not None:
                        self.assertGreaterEqual(field["min"], param.min_val)
                    if param.max_val is not None:
                        self.assertLessEqual(field["max"], param.max_val)
                    # HTML step validity: the default must sit on the grid min + k * step.
                    steps = (field["value"] - field["min"]) / field["step"]
                    self.assertAlmostEqual(steps, round(steps), places=9)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class LabMetricFormatTest(unittest.TestCase):
    def fmt(self, key: str, value) -> str:
        return run_js(f"formatMetric({json.dumps(key)}, {json.dumps(value)})")

    def test_whole_float_keeps_its_decimals(self):
        # JSON delivers profit_factor 2.0 as 2; it must still render like 2.25 does.
        self.assertEqual(self.fmt("profit_factor", 2.0), "2.000")
        self.assertEqual(self.fmt("payoff_ratio", 2.25), "2.250")

    def test_pct_and_dollar_metrics_are_formatted_consistently(self):
        self.assertEqual(self.fmt("win_rate_pct", 47.0), "47.00%")
        self.assertEqual(self.fmt("max_drawdown_pct", 4.6), "4.60%")
        self.assertEqual(self.fmt("net_pnl_dollars", 26928.42), "$26,928.42")
        self.assertEqual(self.fmt("net_pnl_dollars", -1500.5), "-$1,500.50")

    def test_engine_integer_metrics_render_without_decimals(self):
        # Oracle: the Python type of each metric from a default run of every engine.
        int_metrics = {}
        for meta in list_engines():
            for key, value in get_engine(meta["id"]).run().metrics.items():
                if isinstance(value, int) and not isinstance(value, bool):
                    int_metrics[key] = value
        self.assertIn("total_trades", int_metrics)
        rendered = run_js("Object.fromEntries(Object.entries(" + json.dumps(int_metrics) + ").map(([k, v]) => [k, formatMetric(k, v)]))")
        for key, value in int_metrics.items():
            with self.subTest(metric=key):
                self.assertEqual(rendered[key], f"{value:,}")

    def test_time_and_sales_function_is_defined(self):
        self.assertEqual(run_js("typeof renderTimeAndSales"), "function")


if __name__ == "__main__":
    unittest.main()
