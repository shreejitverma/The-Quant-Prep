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

# Loads app.js in a sandbox with a stand-in document, then evaluates one expression and prints its
# (awaited) value. getElementById hands back one recording element per id; setting innerHTML clears
# an element's children, as in a browser; a canvas context accepts and ignores every drawing call.
HARNESS = r"""
const fs = require("fs");
const vm = require("vm");
const [appPath, expr] = process.argv.slice(1);
function makeElement(id) {
  const el = {
    id, value: "", textContent: "", className: "", style: {}, children: [], attributes: {}, _html: "",
    appendChild(child) { this.children.push(child); return child; },
    setAttribute(name, value) { this.attributes[name] = String(value); },
    getAttribute(name) { return name in this.attributes ? this.attributes[name] : null; },
    addEventListener() {},
    getContext() { return new Proxy({}, { get: () => () => {}, set: () => true }); },
  };
  Object.defineProperty(el, "innerHTML", {
    get() { return this._html; },
    set(v) { this._html = v; this.children = []; },
  });
  return el;
}
const elements = {};
const document = {
  addEventListener: () => {},
  getElementById: (id) => elements[id] || (elements[id] = makeElement(id)),
  createElement: () => makeElement(null),
  querySelectorAll: () => [],
};
const ctx = { document, elements, tapeBody: document.getElementById("tape-body") };
ctx.window = ctx;
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(appPath, "utf8"), ctx);
Promise.resolve(vm.runInContext(expr, ctx)).then((value) => process.stdout.write(JSON.stringify(value)));
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

    def test_equity_and_capital_metrics_render_as_dollars(self):
        # pos_sizing and event_study return account equity and capital in dollars without a _dollars suffix.
        self.assertEqual(self.fmt("median_final_equity", 204748.52), "$204,748.52")
        self.assertEqual(self.fmt("mean_final_equity", 0.0), "$0.00")
        self.assertEqual(self.fmt("final_equity", 98250.0), "$98,250.00")
        self.assertEqual(self.fmt("initial_capital", 100000), "$100,000.00")
        self.assertEqual(self.fmt("equity_risk_contribution_pct", 40.0), "40.00%")

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

    def test_time_and_sales_renders_newest_trade_first(self):
        trades = [
            {"time": "09:30:01.100", "price": 100.25, "size": 40, "side": "buy", "aggressor": "agent"},
            {"time": "09:30:02.200", "price": 99.75, "size": 60, "side": "sell", "aggressor": "market"},
        ]
        rendered = run_js("(renderTimeAndSales(" + json.dumps(trades) + "), tapeBody.children.map(row => row.innerHTML))")
        self.assertEqual(len(rendered), 2)
        self.assertIn("09:30:02.200", rendered[0])
        self.assertIn("$99.75", rendered[0])
        self.assertIn("09:30:01.100", rendered[1])
        self.assertIn("$100.25", rendered[1])


def form_defaults(engine_id: str) -> dict:
    """The params app.js posts for an untouched form: numbers parsed as floats, everything else as text."""
    fields = run_js(f"ENGINE_CONFIGS[{json.dumps(engine_id)}].params")
    return {f["id"].removeprefix("p-").replace("-", "_"): (float(f["value"]) if f["type"] == "number" else f["value"]) for f in fields}


# Fills the form with its defaults, swaps in a fetch stub, runs the engine page and reports what it shows.
RUN_PAGE = """(async () => {{
  const engine = {engine};
  const requests = [];
  fetch = async (url, init) => {{ requests.push({{ url, body: JSON.parse(init.body) }}); {respond} }};
  loadEngine(engine);
  const afterLoad = {{ requests: requests.length, cards: elements["metrics-container"].children.length,
                       summary: elements["summary-text"].textContent }};
  for (const p of ENGINE_CONFIGS[engine].params) document.getElementById(p.id).value = String(p.value);
  await runCurrentEngine();
  const cards = elements["metrics-container"].children.map((card) => ({{
    label: card.children[0].textContent, value: card.children[1].textContent }}));
  return {{ afterLoad, requests, cards, summary: elements["summary-text"].textContent,
           chartShown: elements["chart-container"].style.display !== "none" }};
}})()"""
OFFLINE = 'throw new TypeError("Failed to fetch");'


@unittest.skipUnless(shutil.which("node"), "node not installed")
class LabBackendOnlyTest(unittest.TestCase):
    """The page shows only what the qp engines compute; offline it refuses instead of estimating.

    The old client-side fallbacks disagreed with the engines (the Bernoulli Kelly in fat-tailed mode,
    inverse-vol risk parity, fixed crisis profiles), and loadEngine ran them on every page load.
    """

    def test_loading_an_engine_shows_no_numbers_and_records_no_run(self):
        # Opening a page must not post a run: every backend run is recorded in the learner's lab history.
        for meta in list_engines():
            with self.subTest(engine=meta["id"]):
                page = run_js(RUN_PAGE.format(engine=json.dumps(meta["id"]), respond=OFFLINE))
                self.assertEqual(page["afterLoad"]["requests"], 0)
                self.assertEqual(page["afterLoad"]["cards"], 0)
                self.assertNotRegex(page["afterLoad"]["summary"], r"\d")

    def test_offline_run_refuses_instead_of_estimating(self):
        for meta in list_engines():
            with self.subTest(engine=meta["id"]):
                page = run_js(RUN_PAGE.format(engine=json.dumps(meta["id"]), respond=OFFLINE))
                self.assertEqual(len(page["requests"]), 1)
                self.assertEqual(page["cards"], [])
                self.assertFalse(page["chartShown"])
                self.assertIn("qp serve", page["summary"])
                self.assertNotRegex(page["summary"].replace("./qp serve", ""), r"\d")

    def test_backend_results_are_shown_verbatim(self):
        # Oracle: the Python engine run with the same params the page posts.
        for meta in list_engines():
            engine_id = meta["id"]
            with self.subTest(engine=engine_id):
                params = form_defaults(engine_id)
                result = get_engine(engine_id).run(**params).to_dict()
                respond = "return { ok: true, json: async () => (" + json.dumps(result) + ") };"
                page = run_js(RUN_PAGE.format(engine=json.dumps(engine_id), respond=respond))
                self.assertEqual(page["requests"], [{"url": "/api/lab/run", "body": {"engine": engine_id, "params": params}}])
                expected = run_js(
                    "Object.entries(" + json.dumps(result["metrics"]) + ").map(([k, v]) => "
                    '({ label: k.replace(/_/g, " ").toUpperCase(), value: formatMetric(k, v) }))'
                )
                self.assertEqual(page["cards"], expected)
                self.assertEqual(page["summary"], f"[Backend Engine] {result['summary']}")


if __name__ == "__main__":
    unittest.main()
