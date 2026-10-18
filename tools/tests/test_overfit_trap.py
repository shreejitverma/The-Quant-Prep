"""Unit tests for the Overfit Trap and Deflated Sharpe Analyzer engine."""

import json
import math
import unittest
from statistics import NormalDist

from tools.qp.lab import get_engine
from tools.qp.lab.overfit_trap import (
    deflated_sharpe_ratio,
    expected_max_null_sharpe,
    harvey_liu_haircuts,
    min_backtest_length_years,
    norm_cdf,
    norm_inv_cdf,
    norm_isf_log,
    norm_logsf,
    probabilistic_sharpe_ratio,
)

STD_NORMAL = NormalDist()
EULER_GAMMA = 0.5772156649015329


def reference_adjusted_t(p_adj: float) -> float:
    """Two-sided adjusted p-value back to a t-stat, via the stdlib normal quantile."""
    return 0.0 if p_adj >= 1.0 else -STD_NORMAL.inv_cdf(p_adj / 2.0)


def reference_haircut_pct(sharpe: float, years: float, t_adj: float) -> float:
    return max(0.0, (1.0 - (t_adj / math.sqrt(years)) / sharpe) * 100.0)


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


class TestOverfitTrapOracles(unittest.TestCase):
    """Each test checks against a formula computed here, independently of the engine's code path."""

    def test_log_tail_matches_erfc_including_past_the_series_switch(self):
        # Rejects a log tail that loses precision or jumps where the asymptotic branch takes over.
        for x in [0.0, 1.0, 3.0, 8.0, 20.0, 29.9, 30.0, 30.1, 33.0, 37.0]:
            expected = math.log(0.5 * math.erfc(x / math.sqrt(2.0)))
            self.assertAlmostEqual(norm_logsf(x), expected, delta=1e-9 * max(1.0, abs(expected)))
            self.assertAlmostEqual(norm_isf_log(expected), x, delta=1e-9 * max(1.0, x))

    def test_bonferroni_sidak_bhy_match_textbook_formulas(self):
        # Rejects any adjustment that is not p_bonf = N p, p_sidak = 1 - (1 - p)^N, p_bhy = N c(N) p.
        for sharpe, days in [(1.2, 1260), (1.5, 1260), (2.0, 2520)]:
            years = days / 252.0
            t_raw = sharpe * math.sqrt(years)
            p_raw = 2.0 * STD_NORMAL.cdf(-t_raw)
            for n in [1, 10, 100, 1000]:
                hlz = harvey_liu_haircuts(sharpe_ann=sharpe, sample_length_days=days, num_trials=n)
                c_n = sum(1.0 / j for j in range(1, n + 1))
                cases = [
                    ("bonferroni", min(1.0, n * p_raw)),
                    ("sidak", 1.0 - (1.0 - p_raw) ** n),
                    ("bhy", min(1.0, n * c_n * p_raw)),
                ]
                for label, p_adj in cases:
                    with self.subTest(sharpe=sharpe, days=days, n=n, method=label):
                        t_adj = reference_adjusted_t(p_adj)
                        self.assertAlmostEqual(hlz[f"t_{label}"], t_adj, delta=1.5e-3)
                        self.assertAlmostEqual(hlz[f"haircut_{label}_pct"], reference_haircut_pct(sharpe, years, t_adj), delta=0.01)
                self.assertAlmostEqual(hlz["raw_p_value"], p_raw, delta=1e-12 + 1e-9 * p_raw)

    def test_single_trial_has_no_haircut_even_for_huge_t_stats(self):
        # With one trial there is nothing to correct for; a haircut there means the tail p underflowed.
        for sharpe, days in [(0.5, 1260), (1.5, 1260), (5.0, 10000), (10.0, 10000)]:
            hlz = harvey_liu_haircuts(sharpe_ann=sharpe, sample_length_days=days, num_trials=1)
            with self.subTest(sharpe=sharpe, days=days):
                self.assertEqual(hlz["haircut_bonferroni_pct"], 0.0)
                self.assertEqual(hlz["haircut_sidak_pct"], 0.0)
                self.assertEqual(hlz["t_bonferroni"], hlz["t_stat"])
                self.assertAlmostEqual(hlz["t_stat"], sharpe * math.sqrt(days / 252.0), places=3)

    def test_bonferroni_far_tail_follows_mills_ratio_asymptotics(self):
        # For t near 63 the raw p is below the smallest double. The Mills ratio P(Z > x) ~ pdf(x) / x
        # gives the Bonferroni t from x^2 / 2 + ln x = t^2 / 2 + ln t - ln N; a clipped p cannot match it.
        sharpe, days, n = 10.0, 10000, 10
        t_raw = sharpe * math.sqrt(days / 252.0)
        x = t_raw
        for _ in range(50):
            x = math.sqrt(t_raw * t_raw + 2.0 * math.log(t_raw) - 2.0 * math.log(n) - 2.0 * math.log(x))
        hlz = harvey_liu_haircuts(sharpe_ann=sharpe, sample_length_days=days, num_trials=n)
        self.assertAlmostEqual(hlz["t_bonferroni"], x, delta=1e-3)
        self.assertLess(hlz["t_bonferroni"], t_raw)

    def test_hlz_hurdle_applies_to_the_raw_t_stat(self):
        # HLZ (2016) set t > 3.0 as the hurdle a raw t-stat must clear because it already prices in
        # multiple testing; comparing a Bonferroni-adjusted t with 3.0 would double-count the correction.
        engine = get_engine("overfit_trap")
        for sharpe, expected in [(1.5, "PASS"), (1.2, "FAIL")]:
            t_raw = sharpe * math.sqrt(5.0)
            with self.subTest(sharpe=sharpe):
                self.assertEqual(t_raw >= 3.0, expected == "PASS")
                metrics = engine.run(observed_sharpe=sharpe, sample_length_days=1260, num_trials=100, run_mining_demo=False).metrics
                self.assertEqual(metrics["passes_hlz_t3_threshold"], expected)
                self.assertLess(metrics["harvey_liu_t_bonferroni"], 3.0)

    def test_min_backtest_length_closed_form_and_published_example(self):
        # Bailey, Borwein, Lopez de Prado and Zhu (2014): MinBTL = ((1 - g) Z^-1[1 - 1/N] + g Z^-1[1 - 1/(N e)])^2 / SR^2,
        # and with 5 years of data and a target Sharpe of 1 no more than 45 configurations should be tried.
        for n, sharpe in [(2, 1.0), (45, 1.0), (100, 1.5), (1000, 0.8)]:
            bracket = (1.0 - EULER_GAMMA) * STD_NORMAL.inv_cdf(1.0 - 1.0 / n) + EULER_GAMMA * STD_NORMAL.inv_cdf(1.0 - 1.0 / (n * math.e))
            with self.subTest(n=n, sharpe=sharpe):
                self.assertAlmostEqual(min_backtest_length_years(num_trials=n, target_sharpe_ann=sharpe), (bracket / sharpe) ** 2, places=6)
        self.assertAlmostEqual(min_backtest_length_years(num_trials=45, target_sharpe_ann=1.0), 5.0, delta=0.05)
        self.assertEqual(min_backtest_length_years(num_trials=1, target_sharpe_ann=1.0), 0.0)

    def test_non_positive_sharpe_never_satisfies_min_backtest_length(self):
        # MinBTL ~ 1 / SR^2 diverges as SR -> 0; reporting 0 years would pass an unskilled strategy.
        for n in [1, 100]:
            self.assertEqual(min_backtest_length_years(num_trials=n, target_sharpe_ann=0.0), math.inf)
            self.assertEqual(min_backtest_length_years(num_trials=n, target_sharpe_ann=-0.5), math.inf)
        result = get_engine("overfit_trap").run(observed_sharpe=0.0, num_trials=100, run_mining_demo=False)
        self.assertEqual(result.metrics["sufficient_sample_length"], "FAIL")
        self.assertEqual(result.metrics["min_backtest_length_years"], "UNDEFINED")
        self.assertIsNone(result.data["min_backtest_length"]["min_years_required"])

        def reject_constant(name):
            raise ValueError(f"non-standard JSON constant {name}")

        json.loads(result.to_json(), parse_constant=reject_constant)

    def test_cscv_blocks_must_be_an_allowed_even_split(self):
        # CSCV needs S even with S >= 2 to form C(S, S/2) train/test splits; 0 and 1 give no split at all.
        engine = get_engine("overfit_trap")
        for blocks in [0, 1, 2, 5]:
            with self.subTest(blocks=blocks), self.assertRaises(ValueError):
                engine.run(cscv_blocks=blocks, run_mining_demo=False)
        for blocks in [4, 6, 8, 10]:
            with self.subTest(blocks=blocks):
                result = engine.run(cscv_blocks=blocks, sample_length_days=200, mining_trials=10)
                self.assertEqual(result.data["cscv_simulation"]["num_combinations"], math.comb(blocks, blocks // 2))


if __name__ == "__main__":
    unittest.main()
