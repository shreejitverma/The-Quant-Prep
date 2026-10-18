"""Unit tests for tools/qp/lab/base.py and registry."""

import json
import unittest

from tools.qp.lab.base import Param, TradingLabEngine
from tools.qp.lab.pos_sizing import EQUITY_CEILING, PositionSizingEngine
from tools.qp.lab.registry import get_engine, list_engines


class TestTradingLabBase(unittest.TestCase):
    def test_param_casting_and_bounds(self):
        p_int = Param("trades", "int", 50, "desc", min_val=10, max_val=100)
        self.assertEqual(p_int.cast("40"), 40)
        with self.assertRaises(ValueError):
            p_int.cast("5")
        with self.assertRaises(ValueError):
            p_int.cast("150")

        p_float = Param("risk", "float", 0.02, "desc", min_val=0.01, max_val=0.1)
        self.assertAlmostEqual(p_float.cast("0.05"), 0.05)
        with self.assertRaises(ValueError):
            p_float.cast("0.005")

        p_bool = Param("flag", "bool", False, "desc")
        self.assertTrue(p_bool.cast("true"))
        self.assertFalse(p_bool.cast("false"))

        p_str = Param("mode", "str", "a", "desc", choices=["a", "b", "c"])
        self.assertEqual(p_str.cast("b"), "b")
        with self.assertRaises(ValueError):
            p_str.cast("d")

    def test_calculate_returns_metrics(self):
        # 5% gain then ~14.3% gain: 100 -> 105 -> 120 (CAGR = 20%)
        curve = [100.0, 105.0, 120.0]
        metrics = TradingLabEngine.calculate_returns_metrics(curve, risk_free_rate=0.0, periods_per_year=2)
        self.assertAlmostEqual(metrics["cagr"], 0.20, places=2)
        self.assertGreater(metrics["sharpe"], 0.0)
        self.assertEqual(metrics["max_drawdown"], 0.0)

        # Drawdown curve: 100 -> 80 -> 90
        dd_curve = [100.0, 80.0, 90.0]
        dd_metrics = TradingLabEngine.calculate_returns_metrics(dd_curve, risk_free_rate=0.0, periods_per_year=2)
        self.assertAlmostEqual(dd_metrics["max_drawdown"], 0.20, places=2)

    def test_calculate_trade_metrics(self):
        pnls = [100.0, -50.0, 150.0, -50.0]
        metrics = TradingLabEngine.calculate_trade_metrics(pnls)
        self.assertEqual(metrics["total_trades"], 4)
        self.assertEqual(metrics["win_rate"], 0.5)
        self.assertEqual(metrics["profit_factor"], 2.5)
        self.assertAlmostEqual(metrics["avg_win"], 125.0)
        self.assertAlmostEqual(metrics["avg_loss"], -50.0)
        self.assertAlmostEqual(metrics["expectancy"], 37.5)

    def test_trade_expectancy_counts_breakevens_as_zero(self):
        # Mean of [10, 0, -10] is 0; treating the breakeven as a loss would give -3.33.
        self.assertEqual(TradingLabEngine.calculate_trade_metrics([10.0, 0.0, -10.0])["expectancy"], 0.0)

    def test_param_cast_rejects_non_finite_floats(self):
        p = Param(name="x", param_type="float", default=0.5, description="x", min_val=0.0, max_val=1.0)
        for raw in ("nan", float("nan"), "inf", float("-inf")):
            with self.assertRaises(ValueError):
                p.cast(raw)

    def test_registry_and_pos_sizing(self):
        engines = list_engines()
        self.assertTrue(any(e["id"] == "pos_sizing" for e in engines))

        engine = get_engine("pos_sizing")
        self.assertIsNotNone(engine)
        self.assertIsInstance(engine, PositionSizingEngine)

        # Run with default params
        res = engine.run()
        self.assertIn("kelly_fraction", res.metrics)
        self.assertIn("ruin_probability", res.metrics)
        self.assertAlmostEqual(res.metrics["kelly_fraction"], 0.25)

    def test_pos_sizing_at_web_form_maximums_stays_finite(self):
        # Regression: these are the web form maximums. Compounding 11x per win overflowed equity to
        # inf, and the run returned NaN equity (invalid JSON) and a 94.8% ruin rate at a 99% win rate.
        res = get_engine("pos_sizing").run(
            account_capital=1e7,
            win_rate=0.99,
            win_loss_ratio=20.0,
            risk_per_trade_pct=0.5,
            num_trades=1000,
            num_simulations=1000,
        )
        json.dumps(res.to_dict(), allow_nan=False)  # RFC 8259 has no NaN or Infinity
        self.assertLessEqual(res.metrics["median_final_equity"], EQUITY_CEILING)
        self.assertGreater(res.metrics["paths_capped_at_ceiling"], 0)
        # Oracle: at 50% risk every loss halves equity from at or below its peak, so any loss is a
        # >= 50% drawdown and ruin is P(at least one loss in 1000 trades) = 1 - 0.99**1000 = 0.99996.
        # Stopping a path at the ceiling (after about 8 straight wins) would report about 0.077.
        self.assertGreaterEqual(res.metrics["ruin_probability"], 0.99)

    def test_pos_sizing_counts_drawdowns_after_the_ceiling(self):
        # Every path compounds past the ceiling, yet a 10% risk with 1000 trades still sees deep
        # drawdowns. Oracle: the first 100 trades of each path are a prefix of its 1000-trade path
        # (same seed), so per-path max drawdown, and hence ruin, cannot fall as trades are added.
        engine = get_engine("pos_sizing")
        kwargs = dict(account_capital=100000, win_rate=0.6, win_loss_ratio=3.0, risk_per_trade_pct=0.1, num_simulations=1000)
        short = engine.run(num_trades=100, **kwargs)
        long = engine.run(num_trades=1000, **kwargs)
        self.assertEqual(long.metrics["paths_capped_at_ceiling"], 1000)
        self.assertGreaterEqual(long.metrics["ruin_probability"], short.metrics["ruin_probability"])
        self.assertGreater(long.metrics["ruin_probability"], 0.5)

    def test_validate_params_rejects_unknown_and_off_choice_values(self):
        engine = get_engine("pos_sizing")
        with self.assertRaises(ValueError):
            engine.validate_params({"win_rat": 0.6})
        p_int = Param("blocks", "int", 4, "desc", choices=[4, 6, 8])
        self.assertEqual(p_int.cast("6"), 6)
        with self.assertRaises(ValueError):
            p_int.cast("5")


if __name__ == "__main__":
    unittest.main()
