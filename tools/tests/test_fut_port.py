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
        expected_pnl = capital / spot * front["market_future"] - capital * math.exp(r * front["days"] / 365.0)
        self.assertAlmostEqual(res.metrics["arb_net_pnl"], expected_pnl, delta=0.05)

    def test_cash_and_carry_pnl_is_the_futures_mispricing(self):
        # Hull: buying N = capital / S units financed at r, paying storage c and earning yield q, and delivering
        # them into a short future at F leaves N * (F - S * exp((r + c - q) * T)) at T. A future at its
        # theoretical price is no arbitrage at any maturity; the convenience yield is not cash, so it is excluded.
        cases = [
            ("equity_index", dict(risk_free_rate=0.05, dividend_yield=0.02), 0.05 - 0.02),
            ("contango", dict(risk_free_rate=0.045, storage_cost=0.06), 0.045 + 0.06),
            ("backwardation", dict(risk_free_rate=0.045, convenience_yield=0.15), 0.045 + 0.01),
        ]
        spot, capital = 100.0, 100000.0
        for regime, rates, cash_carry in cases:
            for days in (30, 360, 3650):
                with self.subTest(regime=regime, days=days):
                    res = self.engine.run(
                        spot_price=spot, arbitrage_capital=capital, sim_regime=regime, maturities_days=str(days), seed=7, **rates
                    )
                    front = res.data["term_structure"][0]
                    units = capital / spot
                    expected = units * (front["market_future"] - spot * math.exp(cash_carry * days / 365.0))
                    # market_future is rounded to 4 dp, so the oracle carries up to units * 5e-5 of rounding
                    self.assertAlmostEqual(res.metrics["arb_net_pnl"], expected, delta=units * 5e-5 + 0.01)
                    roi = expected / capital * 365.0 / days * 100.0
                    self.assertAlmostEqual(res.metrics["arb_annualized_roi_pct"], roi, delta=0.01)

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

    def test_risk_parity_equalizes_euler_risk_contributions(self):
        # Maillard, Roncalli and Teiletche (2010): the equal-risk-contribution portfolio has w_i (Sigma w)_i
        # equal for every asset, so each of the 7 assets carries 100 / 7 % of the risk. Inverse-volatility
        # weights meet that only when all correlations are equal, which no scenario here has.
        for scenario in ("baseline", "stagflation", "liquidity_crisis", "recession"):
            with self.subTest(scenario=scenario):
                res = self.engine.run(strategy="risk_parity", macro_scenario=scenario, n_years=1)
                rows = res.data["asset_breakdown"]
                self.assertTrue(all(row["weight_pct"] > 0.0 for row in rows))
                for row in rows:
                    self.assertAlmostEqual(row["trc_pct"], 100.0 / 7.0, delta=0.01)

    def test_min_variance_satisfies_the_long_only_kkt_conditions(self):
        # Minimizing w' Sigma w subject to sum(w) = 1, w >= 0 is convex, so a point is the optimum iff
        # (Sigma w)_i is one common value for every held asset and no smaller for any asset left out.
        # The engine reports MCR_i = (Sigma w)_i / sigma_p, so the conditions read off the MCR column.
        for scenario in ("baseline", "stagflation", "liquidity_crisis", "recession"):
            with self.subTest(scenario=scenario):
                res = self.engine.run(strategy="min_variance", macro_scenario=scenario, vol_target=0.0, n_years=1)
                rows = res.data["asset_breakdown"]
                self.assertAlmostEqual(sum(row["weight_pct"] for row in rows), 100.0, delta=0.02)
                held = [row["mcr"] for row in rows if row["weight_pct"] > 0.005]
                self.assertTrue(all(row["weight_pct"] >= 0.0 for row in rows))
                self.assertLess(max(held) - min(held), 2e-4)
                for row in rows:
                    if row["weight_pct"] <= 0.005:
                        self.assertGreaterEqual(row["mcr"], min(held) - 2e-4)
                # Every risk contribution is then w_i * lambda / sigma_p = w_i, the weight itself.
                for row in rows:
                    self.assertAlmostEqual(row["trc_pct"], row["weight_pct"], delta=0.02)

    def test_wiped_out_account_stays_at_zero(self):
        # 3x gross with annual rebalancing through a liquidity crisis loses more than the equity on this path.
        # A wiped-out account cannot keep trading on negative equity (negative capital times the target weights
        # silently flips every position short), and its CAGR is -100%, not the 0% of an account that broke even.
        res = self.engine.run(
            strategy="equal_weight",
            macro_scenario="liquidity_crisis",
            leverage=3.0,
            vol_target=0.0,
            rebalance_freq="annual",
            n_years=20,
            seed=43,
        )
        curve = res.data["equity_curve"]
        first_zero = curve.index(0.0)
        self.assertTrue(all(value > 0.0 for value in curve[:first_zero]))
        self.assertTrue(all(value == 0.0 for value in curve[first_zero:]))
        self.assertEqual(res.metrics["cagr_pct"], -100.0)
        self.assertEqual(res.metrics["max_drawdown_pct"], 100.0)
        self.assertEqual(res.data["monthly_returns"][first_zero - 1], -1.0)

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
