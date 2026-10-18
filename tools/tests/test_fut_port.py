"""Unit tests for Futures Desk and Portfolio Allocator Trading Lab engines."""

import math
import statistics
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

    def test_equity_index_cost_of_carry(self):
        # Hull: a financial future on an asset with continuous yield q is F = S * exp((r - q) * T).
        spot, r, q = 4200.0, 0.05, 0.018
        res = self.engine.run(
            spot_price=spot,
            risk_free_rate=r,
            dividend_yield=q,
            sim_regime="equity_index",
            maturities_days="30,91,182,365",
        )
        curve = res.data["term_structure"]
        self.assertEqual([c["days"] for c in curve], [30, 91, 182, 365])
        for c in curve:
            expected = spot * math.exp((r - q) * c["days"] / 365.0)
            self.assertAlmostEqual(c["theoretical_future"], expected, places=3)
        self.assertAlmostEqual(res.metrics["net_carry_rate_pct"], (r - q) * 100.0, places=3)

    def test_crypto_funding_replaces_carry_and_keeps_borrow_rate(self):
        # The perpetual's 8h funding, paid 3 times a day, sets the whole premium: F = S * exp(f * 1095 * T).
        # Spot crypto has no dividend, so q must not be subtracted, while the arbitrageur still borrows at r.
        spot, r, f8h, capital = 30000.0, 0.06, 0.0001, 300000.0
        res = self.engine.run(
            spot_price=spot,
            risk_free_rate=r,
            dividend_yield=0.05,
            crypto_funding_rate_8h=f8h,
            arbitrage_capital=capital,
            sim_regime="crypto_funding",
            maturities_days="30,90",
        )
        funding_annual = f8h * 3.0 * 365.0
        for c in res.data["term_structure"]:
            self.assertAlmostEqual(c["theoretical_future"], spot * math.exp(funding_annual * c["days"] / 365.0), places=3)
        self.assertAlmostEqual(res.metrics["net_carry_rate_pct"], funding_annual * 100.0, places=3)

        # Buy capital / S units of spot with money borrowed at r, deliver them into the short future.
        front = res.data["term_structure"][0]
        expected_pnl = capital / spot * front["market_future"] - capital * math.exp(r * front["years"])
        self.assertAlmostEqual(res.metrics["arb_net_pnl"], expected_pnl, delta=0.05)

    def test_rejects_invalid_maturities(self):
        # A zero maturity divided by zero, junk silently fell back to the default curve,
        # and a negative maturity priced a contract that expired in the past.
        for bad in ("0,30", "abc", "-5,30", "30,,60", "30,30", "30.5", "", "99999"):
            with self.subTest(maturities_days=bad), self.assertRaises(ValueError):
                self.engine.run(maturities_days=bad)
        res = self.engine.run(maturities_days=" 90, 30 ")
        self.assertEqual([c["days"] for c in res.data["term_structure"]], [30, 90])


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

    def test_vol_target_never_exceeds_leverage_cap(self):
        # min_variance is mostly cash, so hitting 10% vol needs far more than 1x; the cap must hold.
        res = self.engine.run(strategy="min_variance", leverage=1.0, vol_target=0.10, n_years=3)
        gross = sum(a["weight_pct"] for a in res.data["asset_breakdown"]) / 100.0
        self.assertLessEqual(res.metrics["leverage"], 1.0)
        self.assertAlmostEqual(gross, res.metrics["leverage"], delta=0.01)

        # With room under the cap, portfolio vol is linear in the scale, so the ex-ante vol is the target.
        res = self.engine.run(strategy="60_40", leverage=3.0, vol_target=0.10, n_years=3)
        self.assertAlmostEqual(res.metrics["ex_ante_volatility_pct"], 10.0, places=2)
        self.assertLess(res.metrics["leverage"], 3.0)

        # Without a target the gross exposure is exactly the requested leverage.
        res = self.engine.run(strategy="60_40", leverage=1.5, vol_target=0.0, n_years=3)
        self.assertEqual(res.metrics["leverage"], 1.5)

    def test_reported_volatility_is_realized(self):
        # Annual vol must come from the simulated monthly returns, not the covariance-model forecast.
        res = self.engine.run(strategy="60_40", leverage=3.0, vol_target=0.10, n_years=5, seed=3)
        realized = statistics.stdev(res.data["monthly_returns"]) * math.sqrt(12.0) * 100.0
        self.assertAlmostEqual(res.metrics["annual_volatility_pct"], realized, delta=0.05)
        self.assertNotAlmostEqual(res.metrics["annual_volatility_pct"], res.metrics["ex_ante_volatility_pct"], delta=0.05)


if __name__ == "__main__":
    unittest.main()
