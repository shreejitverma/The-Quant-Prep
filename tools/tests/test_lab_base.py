"""Unit tests for tools/qp/lab/base.py and registry."""

import unittest

from tools.qp.lab.base import Param, TradingLabEngine
from tools.qp.lab.pos_sizing import PositionSizingEngine
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


if __name__ == "__main__":
    unittest.main()
