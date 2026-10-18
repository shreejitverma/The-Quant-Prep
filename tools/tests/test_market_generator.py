"""Unit tests for tools/qp/lab/market.py and upgraded pos_sizing."""

import math
import statistics
import unittest

from tools.qp.lab.market import REGIME_PARAMS, SyntheticMarketGenerator
from tools.qp.lab.pos_sizing import PositionSizingEngine


class TestSyntheticMarketGenerator(unittest.TestCase):
    def test_gbm_determinism(self):
        gen1 = SyntheticMarketGenerator(seed=123)
        gen2 = SyntheticMarketGenerator(seed=123)
        gen3 = SyntheticMarketGenerator(seed=999)

        p1 = gen1.generate_gbm(s0=100.0, n_steps=50)
        p2 = gen2.generate_gbm(s0=100.0, n_steps=50)
        p3 = gen3.generate_gbm(s0=100.0, n_steps=50)

        self.assertEqual(len(p1), 51)
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)

    def test_ar1_mean_reversion(self):
        gen = SyntheticMarketGenerator(seed=42)
        # Start far below theta=100 (at s0=50) with strong mean reversion kappa=10.0
        prices = gen.generate_ar1_mean_reversion(s0=50.0, theta=100.0, kappa=10.0, sigma=0.05, n_steps=100)
        # Price should pull up toward 100
        self.assertGreater(prices[-1], prices[0])
        self.assertGreater(prices[-1], 80.0)

    def test_regime_path_bars_invariants(self):
        gen = SyntheticMarketGenerator(seed=777)
        bars = gen.generate_regime_path(s0=100.0, n_bars=30, sub_steps=5)
        self.assertEqual(len(bars), 30)

        for b in bars:
            self.assertGreaterEqual(b.high, b.open)
            self.assertGreaterEqual(b.high, b.close)
            self.assertGreaterEqual(b.high, b.low)
            self.assertLessEqual(b.low, b.open)
            self.assertLessEqual(b.low, b.close)
            self.assertLessEqual(b.low, b.high)
            self.assertGreater(b.volume, 0.0)
            self.assertIn(b.regime, ("bull", "bear", "consolidation"))

    def test_garch_long_run_variance(self):
        # Bollerslev (1986): a stationary GARCH(1,1) has unconditional variance omega / (1 - alpha - beta).
        omega, alpha, beta = 2e-6, 0.08, 0.90
        prices = SyntheticMarketGenerator(seed=5).generate_garch(omega=omega, alpha=alpha, beta=beta, n_steps=200000)
        log_rets = [math.log(prices[i] / prices[i - 1]) for i in range(1, len(prices))]
        sample_var = statistics.fmean(r * r for r in log_rets)
        self.assertAlmostEqual(sample_var / (omega / (1.0 - alpha - beta)), 1.0, delta=0.08)
        with self.assertRaises(ValueError):
            SyntheticMarketGenerator(seed=5).generate_garch(alpha=0.2, beta=0.8)

    def test_regime_path_realizes_declared_regime_volatility(self):
        # Per-step omega is set for sub-step returns, so each regime's realized annual vol must sit near
        # its declared long-run vol; sizing omega per bar instead put the old path near 94% annual vol.
        bars = SyntheticMarketGenerator(seed=2).generate_regime_path(s0=100.0, n_bars=20000, sub_steps=10)
        by_regime: dict[str, list[float]] = {}
        for i in range(2, len(bars)):
            if bars[i].regime == bars[i - 1].regime == bars[i - 2].regime:
                by_regime.setdefault(bars[i].regime, []).append(math.log(bars[i].close / bars[i].open))
        self.assertEqual(set(by_regime), set(REGIME_PARAMS))
        for regime, rets in by_regime.items():
            realized = statistics.pstdev(rets) * math.sqrt(252.0)
            with self.subTest(regime=regime):
                self.assertAlmostEqual(realized / REGIME_PARAMS[regime]["vol"], 1.0, delta=0.15)

    def test_oracle_probability(self):
        gen = SyntheticMarketGenerator(seed=1)
        # Zero drift (mu = 0.5 * sigma^2): P(S_h > S_0) should be exactly 0.50
        prob_neutral = gen.oracle_probability_higher(100.0, horizon_steps=10, mu=0.02, sigma=0.20)
        self.assertAlmostEqual(prob_neutral, 0.50, places=4)

        # High positive drift: P should be > 0.50
        prob_bull = gen.oracle_probability_higher(100.0, horizon_steps=10, mu=0.50, sigma=0.20)
        self.assertGreater(prob_bull, 0.60)

    def test_kelly_growth_peak(self):
        p_win = 0.60
        b = 1.5
        # f* = p - (1-p)/b = 0.60 - 0.40/1.5 = 0.60 - 0.266667 = 0.333333
        f_star = p_win - (1.0 - p_win) / b
        g_peak = PositionSizingEngine.calculate_growth_rate(f_star, p_win, b)

        # Check peak: growth rate at f* must be higher than at f* - 0.05 and f* + 0.05
        g_below = PositionSizingEngine.calculate_growth_rate(f_star - 0.05, p_win, b)
        g_above = PositionSizingEngine.calculate_growth_rate(f_star + 0.05, p_win, b)
        self.assertGreater(g_peak, g_below)
        self.assertGreater(g_peak, g_above)

        # Check overbetting trap: at f = 2.5 * f*, growth rate should become negative
        g_overbet = PositionSizingEngine.calculate_growth_rate(f_star * 2.5, p_win, b)
        self.assertLess(g_overbet, 0.0)

    def test_fat_tailed_ruin_simulation(self):
        engine = PositionSizingEngine()
        res_normal = engine.run(
            account_capital=100000.0,
            win_rate=0.52,
            win_loss_ratio=1.1,
            risk_per_trade_pct=0.05,
            distribution="bernoulli",
            num_trades=100,
            num_simulations=200,
            seed=42,
        )
        res_fat = engine.run(
            account_capital=100000.0,
            win_rate=0.52,
            win_loss_ratio=1.1,
            risk_per_trade_pct=0.05,
            distribution="fat_tailed",
            num_trades=100,
            num_simulations=200,
            seed=42,
        )

        self.assertIn("median_time_under_water_bars", res_normal.metrics)
        self.assertIn("growth_curve", res_normal.data)
        # Fat-tailed distribution should yield higher average drawdown due to negative jump risk
        self.assertGreaterEqual(res_fat.metrics["mean_max_drawdown"], res_normal.metrics["mean_max_drawdown"])


if __name__ == "__main__":
    unittest.main()
