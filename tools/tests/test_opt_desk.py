"""Unit tests for tools/qp/lab/opt_desk.py OptionsDeskEngine."""

import math
import statistics
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

    def hedged_pnls(self, n_seeds: int, **kwargs) -> list[float]:
        return [self.engine.run(scenario="gamma_scalp", seed=seed, **kwargs).metrics["net_hedged_pnl"] for seed in range(n_seeds)]

    def test_hedging_error_matches_derman_kamal_discrete_hedging_formula(self):
        # Oracle: Derman-Kamal, the P&L of a straddle delta-hedged N times at realized = implied vol has
        # standard deviation sqrt(pi / 4) * vega * sigma / sqrt(N). Rejects an unhedged or mis-hedged book
        # (far wider spread) and a schedule that ignores hedge_frequency_hours=16 by hedging every 24 hours.
        s, sigma, r, days = 100.0, 0.25, 0.04, 32
        t = days / 365.0
        d1 = (r + 0.5 * sigma * sigma) * t / (sigma * math.sqrt(t))
        straddle_vega = 2.0 * s * math.sqrt(t) * math.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi)
        for hedge_hours in (1, 16):
            with self.subTest(hedge_hours=hedge_hours):
                n_hedges = days * 24 / hedge_hours
                expected_sd = math.sqrt(math.pi / 4.0) * straddle_vega * sigma / math.sqrt(n_hedges)
                pnls = self.hedged_pnls(
                    200,
                    spot=s,
                    strike=s,
                    implied_vol=sigma,
                    realized_vol=sigma,
                    risk_free_rate=r,
                    days_to_expiry=days,
                    hedge_frequency_hours=hedge_hours,
                )
                self.assertAlmostEqual(statistics.pstdev(pnls) / expected_sd, 1.0, delta=0.15)

    def test_rebalances_follow_a_non_divisor_hedge_interval(self):
        # 13 days hedged every 13 hours gives ceil(312 / 13) = 24 intervals, so 23 hedge dates before expiry.
        # Rejects stepping by 24 // 13 = 1 hedge per day, which allows at most 13 over 13 days.
        res = self.engine.run(
            scenario="gamma_scalp", implied_vol=1.0, realized_vol=1.0, days_to_expiry=13, hedge_frequency_hours=13, seed=3
        )
        self.assertLessEqual(res.metrics["total_rebalances"], 23)
        self.assertGreater(res.metrics["total_rebalances"], 13)

    def test_hedged_straddle_mean_pnl_is_zero_when_realized_equals_implied_with_carry(self):
        # Oracle: under Black-Scholes, a delta-hedged option whose cash account earns r is self-financing, so at
        # realized = implied vol its expected terminal P&L is zero. Rejects an unfunded hedge account, which
        # loses about 14 per straddle on this one-year, 25% rate setup.
        pnls = self.hedged_pnls(200, implied_vol=0.25, realized_vol=0.25, risk_free_rate=0.25, days_to_expiry=365, hedge_frequency_hours=24)
        std_err = statistics.stdev(pnls) / math.sqrt(len(pnls))
        self.assertLess(abs(statistics.mean(pnls)), 4.0 * std_err)

    def test_dollar_pnl_is_homogeneous_in_spot_and_strike(self):
        # Oracle: Black-Scholes is homogeneous of degree one in (S, K); scaling both by 100 on the same log-return
        # path scales every dollar P&L by 100. Rejects rounding gamma or spot inside the simulation, which bites
        # at the tiny per-dollar gamma of a 10000 strike.
        kwargs = dict(scenario="gamma_scalp", implied_vol=1.5, realized_vol=1.5, days_to_expiry=365, hedge_frequency_hours=24, seed=7)
        small = self.engine.run(spot=100.0, strike=100.0, **kwargs).metrics
        large = self.engine.run(spot=10000.0, strike=10000.0, **kwargs).metrics
        for key in ("gross_gamma_pnl", "total_theta_decay_cost", "net_hedged_pnl"):
            with self.subTest(metric=key):
                self.assertAlmostEqual(large[key], 100.0 * small[key], delta=0.51)

    def test_crush_vega_pnl_has_the_short_straddle_sign_and_size(self):
        # Oracle: the short straddle's IV-only repricing, -(straddle(post IV) - straddle(pre IV)), from closed-form
        # Black-Scholes. A near-zero realized vol keeps the earnings gap negligible, so the straddle P&L is all vega.
        # Rejects booking the short straddle as long vega (opposite sign).
        s, k, sigma, r, days = 150.0, 150.0, 0.55, 0.04, 7
        res = self.engine.run(
            scenario="earnings_crush",
            spot=s,
            strike=k,
            implied_vol=sigma,
            realized_vol=0.01,
            risk_free_rate=r,
            days_to_expiry=days,
            seed=10,
        )
        post_iv = res.metrics["post_earnings_iv_pct"] / 100.0
        t = days / 365.0
        iv_only_pnl = bs_straddle(s, k, t, r, sigma) - bs_straddle(s, k, t, r, post_iv)
        vega_pnl = res.metrics["vega_pnl_attribution"]
        self.assertGreater(iv_only_pnl, 0.0)
        self.assertGreater(vega_pnl, 0.0)
        self.assertGreater(res.metrics["short_straddle_pnl"], 0.0)
        self.assertAlmostEqual(vega_pnl / iv_only_pnl, 1.0, delta=0.05)

    def test_crush_never_raises_a_low_implied_vol(self):
        # Rejects a 12% floor that lifts an 8% pre-earnings IV to 12% after the "crush".
        res = self.engine.run(scenario="earnings_crush", implied_vol=0.08)
        self.assertLessEqual(res.metrics["post_earnings_iv_pct"], res.metrics["pre_earnings_iv_pct"])

    def test_large_earnings_gap_keeps_spot_positive(self):
        # Seed 261 draws a gap below -100% under an additive gap at 300% realized vol, which made spot negative
        # and crashed the log in d1. A lognormal gap keeps the jump above -100%.
        res = self.engine.run(scenario="earnings_crush", implied_vol=1.0, realized_vol=3.0, seed=261)
        self.assertGreater(res.metrics["underlying_jump_pct"], -100.0)
        self.assertGreaterEqual(res.metrics["post_straddle_price"], 0.0)

    def test_25_delta_put_strike_has_put_delta_minus_quarter(self):
        # Oracle: closed-form put delta -N(-d1) at the reported strike and its smile vol. Rejects labelling the
        # fixed 0.90-moneyness strike as the 25-delta put.
        s, r, days = 100.0, 0.04, 30
        t = days / 365.0
        res = self.engine.run(scenario="skew_shift", spot=s, implied_vol=0.25, risk_free_rate=r, days_to_expiry=days)
        for regime in ("calm", "stressed"):
            with self.subTest(regime=regime):
                k = res.metrics[f"25d_put_strike_{regime}"]
                sigma = res.metrics[f"25d_put_vol_{regime}"]
                d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
                self.assertAlmostEqual(-norm_cdf(-d1), -0.25, delta=1e-3)
        self.assertGreater(res.metrics["25d_put_vol_stressed"], res.metrics["25d_put_vol_calm"])

    def test_dispersion_follows_implied_correlation_relation(self):
        # Oracle: for a large equal-weight basket, index variance = rho * component variance, so
        # rho_implied = (index vol / component vol)^2, and long dispersion pays component variance times
        # (rho_implied - rho_realized). Rejects constant outputs that ignore realized index vol.
        for realized, status in ((0.15, "PROFITABLE_LONG_DISPERSION"), (0.32, "LOSING_LONG_DISPERSION")):
            with self.subTest(realized_vol=realized):
                m = self.engine.run(scenario="dispersion", implied_vol=0.25, realized_vol=realized).metrics
                index_vol = m["index_implied_vol_pct"] / 100.0
                component_vol = m["component_implied_vol_pct"] / 100.0
                rho_implied = (index_vol / component_vol) ** 2
                rho_realized = (realized / component_vol) ** 2
                self.assertAlmostEqual(m["priced_implied_correlation"], rho_implied, places=4)
                self.assertAlmostEqual(m["realized_correlation"], rho_realized, places=4)
                expected_pnl = component_vol**2 * (rho_implied - rho_realized)
                self.assertAlmostEqual(m["long_dispersion_variance_pnl"], expected_pnl, places=4)
                self.assertEqual(m["strategy_edge_status"], status)


def norm_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def bs_straddle(s: float, k: float, t: float, r: float, sigma: float) -> float:
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    call = s * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d2)
    put = k * math.exp(-r * t) * norm_cdf(-d2) - s * norm_cdf(-d1)
    return call + put


if __name__ == "__main__":
    unittest.main()
