"""Unit tests for the Overfit Trap and Deflated Sharpe Analyzer engine."""

import unittest

from tools.qp.lab import get_engine
from tools.qp.lab.overfit_trap import (
    deflated_sharpe_ratio,
    expected_max_null_sharpe,
    harvey_liu_haircuts,
    min_backtest_length_years,
    norm_cdf,
    norm_inv_cdf,
    probabilistic_sharpe_ratio,
)


class TestOverfitTrap(unittest.TestCase):
    def test_norm_cdf_and_inv(self):
        # Symmetry and basic values
        self.assertAlmostEqual(norm_cdf(0.0), 0.5, places=6)
        self.assertAlmostEqual(norm_inv_cdf(0.5), 0.0, places=6)
        self.assertAlmostEqual(norm_cdf(1.95996), 0.975, places=3)
        self.assertAlmostEqual(norm_inv_cdf(0.975), 1.95996, places=3)

        # Inversion round-trip
        for p in [0.001, 0.05, 0.10, 0.50, 0.90, 0.95, 0.999]:
            z = norm_inv_cdf(p)
            self.assertAlmostEqual(norm_cdf(z), p, places=5)

    def test_expected_max_null_sharpe_monotonicity(self):
        var = 0.20
        sr_10 = expected_max_null_sharpe(10, var)
        sr_100 = expected_max_null_sharpe(100, var)
        sr_1000 = expected_max_null_sharpe(1000, var)

        self.assertGreater(sr_100, sr_10)
        self.assertGreater(sr_1000, sr_100)

    def test_probabilistic_and_deflated_sharpe(self):
        # Daily units: SR = 1.5 / sqrt(252) ~ 0.0945
        sample_length = 1260
        psr_high = probabilistic_sharpe_ratio(
            observed_sharpe=0.10,
            benchmark_sharpe=0.0,
            sample_length=sample_length,
            skewness=0.0,
            kurtosis=3.0,
        )
        self.assertGreater(psr_high, 0.99)

        # Negative skewness should reduce PSR
        psr_skewed = probabilistic_sharpe_ratio(
            observed_sharpe=0.10,
            benchmark_sharpe=0.0,
            sample_length=sample_length,
            skewness=-2.0,
            kurtosis=6.0,
        )
        self.assertLess(psr_skewed, psr_high)

        # Deflated Sharpe for 10 trials vs 1000 trials
        dsr_10, exp_10, _ = deflated_sharpe_ratio(
            observed_sharpe_ann=1.5,
            num_trials=10,
            sample_length_days=1260,
            variance_ann=0.20,
        )
        dsr_1000, exp_1000, _ = deflated_sharpe_ratio(
            observed_sharpe_ann=1.5,
            num_trials=1000,
            sample_length_days=1260,
            variance_ann=0.20,
        )
        self.assertGreater(exp_1000, exp_10)
        self.assertGreater(dsr_10, dsr_1000)

    def test_harvey_liu_haircuts(self):
        # 5 years, SR = 1.2
        hlz_10 = harvey_liu_haircuts(sharpe_ann=1.2, sample_length_days=1260, num_trials=10)
        hlz_200 = harvey_liu_haircuts(sharpe_ann=1.2, sample_length_days=1260, num_trials=200)

        self.assertGreater(hlz_200["haircut_bonferroni_pct"], hlz_10["haircut_bonferroni_pct"])
        self.assertLess(hlz_200["sharpe_bonferroni"], hlz_10["sharpe_bonferroni"])
        self.assertGreaterEqual(hlz_10["t_bonferroni"], hlz_200["t_bonferroni"])

    def test_min_backtest_length(self):
        # Higher target Sharpe requires shorter backtest
        btl_low_sr = min_backtest_length_years(num_trials=100, target_sharpe_ann=0.8)
        btl_high_sr = min_backtest_length_years(num_trials=100, target_sharpe_ann=1.5)
        self.assertGreater(btl_low_sr, btl_high_sr)

    def test_engine_run_and_cscv(self):
        engine = get_engine("overfit_trap")
        self.assertIsNotNone(engine)

        result = engine.run(
            observed_sharpe=1.6,
            sample_length_days=756,  # 3 years
            num_trials=50,
            run_mining_demo=True,
            mining_trials=40,
            cscv_blocks=6,
            seed=42,
        )

        metrics = result.metrics
        self.assertIn("deflated_sharpe_ratio", metrics)
        self.assertIn("harvey_liu_haircut_pct", metrics)
        self.assertIn("min_backtest_length_years", metrics)
        self.assertIn("pbo_cscv", metrics)
        self.assertIn("noise_mining_best_sharpe", metrics)
        self.assertIn("noise_oos_decay_pct", metrics)

        # For pure noise, PBO should be close to 0.50
        self.assertGreaterEqual(metrics["pbo_cscv"], 0.20)
        self.assertLessEqual(metrics["pbo_cscv"], 0.90)

        # Check TOON output
        toon = result.to_toon()
        self.assertIn("engine: overfit_trap", toon)
        self.assertIn("deflated_sharpe_ratio", toon)


if __name__ == "__main__":
    unittest.main()
