"""Unit tests for Futures Desk and Portfolio Allocator Trading Lab engines."""

import unittest

from tools.qp.lab.fut_desk import FuturesDeskEngine
from tools.qp.lab.port_alloc import PortfolioAllocatorEngine


class TestFuturesDeskEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FuturesDeskEngine()

    def test_engine_metadata(self):
        self.assertEqual(self.engine.engine_id, "fut_desk")
        self.assertIn("Futures", self.engine.name)
        self.assertEqual(self.engine.asset_class, "Futures & Derivatives")

    def test_contango_term_structure(self):
        res = self.engine.run(
            spot_price=100.0,
            sim_regime="contango",
            maturities_days="30,60,90",
            seed=42,
        )
        self.assertEqual(res.metrics["curve_structure"], "Contango")
        self.assertGreater(res.metrics["front_future_price"], 100.0)
        self.assertGreater(res.metrics["calendar_spread_dollar"], 0.0)
        self.assertIn("term_structure", res.data)
        self.assertEqual(len(res.data["term_structure"]), 3)

    def test_backwardation_term_structure(self):
        res = self.engine.run(
            spot_price=100.0,
            sim_regime="backwardation",
            maturities_days="30,60",
            seed=42,
        )
        self.assertEqual(res.metrics["curve_structure"], "Backwardation")
        self.assertLess(res.metrics["front_future_price"], 100.0)
        self.assertLess(res.metrics["calendar_spread_dollar"], 0.0)

    def test_cash_and_carry_arbitrage(self):
        res = self.engine.run(
            spot_price=50.0,
            arbitrage_capital=50000.0,
            sim_regime="equity_index",
            seed=42,
        )
        self.assertIn("arb_net_pnl", res.metrics)
        self.assertIn("convergence_path", res.data)
        self.assertTrue(len(res.data["convergence_path"]) > 0)


class TestPortfolioAllocatorEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PortfolioAllocatorEngine()

    def test_engine_metadata(self):
        self.assertEqual(self.engine.engine_id, "port_alloc")
        self.assertIn("Portfolio", self.engine.name)
        self.assertEqual(self.engine.asset_class, "Portfolio & Multi-Asset")

    def test_60_40_strategy_risk_concentration(self):
        res = self.engine.run(
            strategy="60_40",
            macro_scenario="baseline",
            n_years=3,
            seed=42,
        )
        self.assertEqual(res.metrics["strategy"], "60_40")
        # In a 60/40 portfolio, equities account for the vast majority of total risk
        self.assertGreater(res.metrics["equity_risk_contribution_pct"], 75.0)
        self.assertIn("asset_breakdown", res.data)
        self.assertEqual(len(res.data["asset_breakdown"]), 7)

    def test_risk_parity_strategy(self):
        res = self.engine.run(
            strategy="risk_parity",
            macro_scenario="baseline",
            n_years=3,
            seed=42,
        )
        self.assertEqual(res.metrics["strategy"], "risk_parity")
        # In risk parity, equity risk is balanced down significantly compared to 60/40
        self.assertLess(res.metrics["equity_risk_contribution_pct"], 40.0)

    def test_all_weather_stagflation_stress(self):
        res = self.engine.run(
            strategy="all_weather",
            macro_scenario="stagflation",
            n_years=3,
            seed=42,
        )
        self.assertEqual(res.metrics["scenario"], "stagflation")
        self.assertIn("equity_curve", res.data)
        self.assertEqual(len(res.data["equity_curve"]), 37)  # 36 months + initial


if __name__ == "__main__":
    unittest.main()
