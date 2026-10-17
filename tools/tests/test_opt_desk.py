"""Unit tests for tools/qp/lab/opt_desk.py OptionsDeskEngine."""

import math
import unittest

from tools.qp.lab.opt_desk import OptionsDeskEngine
from tools.qp.lab.registry import get_engine


class TestOptionsDeskEngine(unittest.TestCase):
    def setUp(self):
        self.engine = get_engine("opt_desk")
        self.assertIsNotNone(self.engine)

    def test_put_call_parity(self):
        s = 100.0
        k = 105.0
        t = 0.5
        r = 0.05
        sigma = 0.20

        call_p = OptionsDeskEngine.bsm_price(s, k, t, r, sigma, "call")
        put_p = OptionsDeskEngine.bsm_price(s, k, t, r, sigma, "put")

        # Put-Call Parity: C - P = S - K * exp(-r * t)
        lhs = call_p - put_p
        rhs = s - k * math.exp(-r * t)
        self.assertAlmostEqual(lhs, rhs, places=4)

    def test_greeks_finite_differences(self):
        s = 100.0
        k = 100.0
        t = 1.0
        r = 0.04
        sigma = 0.25
        eps = 1e-4

        greeks = OptionsDeskEngine.bsm_greeks(s, k, t, r, sigma, "call")
        delta_ana = greeks["delta"]
        gamma_ana = greeks["gamma"]
        vega_unit_ana = greeks["vega_unit"]

        # Finite difference Delta
        c_up = OptionsDeskEngine.bsm_price(s + eps, k, t, r, sigma, "call")
        c_down = OptionsDeskEngine.bsm_price(s - eps, k, t, r, sigma, "call")
        delta_fd = (c_up - c_down) / (2.0 * eps)
        self.assertAlmostEqual(delta_ana, delta_fd, places=3)

        # Finite difference Gamma
        c_mid = OptionsDeskEngine.bsm_price(s, k, t, r, sigma, "call")
        gamma_fd = (c_up - 2.0 * c_mid + c_down) / (eps**2)
        self.assertAlmostEqual(gamma_ana, gamma_fd, places=3)

        # Finite difference Vega
        c_vol_up = OptionsDeskEngine.bsm_price(s, k, t, r, sigma + eps, "call")
        c_vol_down = OptionsDeskEngine.bsm_price(s, k, t, r, sigma - eps, "call")
        vega_fd = (c_vol_up - c_vol_down) / (2.0 * eps)
        self.assertAlmostEqual(vega_unit_ana, vega_fd, places=3)

    def test_gamma_scalping_simulation(self):
        res = self.engine.run(
            scenario="gamma_scalp",
            spot=100.0,
            strike=100.0,
            implied_vol=0.25,
            realized_vol=0.35,  # higher realized vol -> positive gamma PnL
            days_to_expiry=15,
            hedge_frequency_hours=4,
            seed=42,
        )
        self.assertEqual(res.engine_id, "opt_desk")
        self.assertTrue(res.metrics["delta_neutrality_verified"])
        self.assertGreater(res.metrics["gross_gamma_pnl"], 0.0)
        self.assertGreater(res.metrics["total_theta_decay_cost"], 0.0)
        # Higher realized vol than implied vol -> net profit
        self.assertGreater(res.metrics["net_hedged_pnl"], 0.0)

    def test_earnings_crush_scenario(self):
        res = self.engine.run(
            scenario="earnings_crush",
            spot=150.0,
            strike=150.0,
            implied_vol=0.55,
            days_to_expiry=7,
            seed=10,
        )
        self.assertIn("short_straddle_pnl", res.metrics)
        self.assertIn("pre_earnings_iv_pct", res.metrics)
        self.assertIn("post_earnings_iv_pct", res.metrics)
        self.assertLess(res.metrics["post_earnings_iv_pct"], res.metrics["pre_earnings_iv_pct"])


if __name__ == "__main__":
    unittest.main()
