"""Unit tests for tools/qp/lab/replay_chart.py ChartReplayEngine."""

import math
import unittest

from tools.qp.lab.market import SyntheticMarketGenerator
from tools.qp.lab.registry import get_engine
from tools.qp.lab.replay_chart import ChartReplayEngine

DT = 1.0 / 252.0


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


class TestChartReplayEngine(unittest.TestCase):
    def setUp(self):
        self.engine = get_engine("replay_chart")
        self.assertIsNotNone(self.engine)
        self.assertIsInstance(self.engine, ChartReplayEngine)

    def test_brier_score_math(self):
        # Perfect forecast
        self.assertAlmostEqual(ChartReplayEngine.compute_brier_score(1.0, 1), 0.0)
        self.assertAlmostEqual(ChartReplayEngine.compute_brier_score(0.0, 0), 0.0)

        # Naive 0.50 forecast
        self.assertAlmostEqual(ChartReplayEngine.compute_brier_score(0.5, 1), 0.25)
        self.assertAlmostEqual(ChartReplayEngine.compute_brier_score(0.5, 0), 0.25)

        # Inverted forecast
        self.assertAlmostEqual(ChartReplayEngine.compute_brier_score(1.0, 0), 1.0)
        self.assertAlmostEqual(ChartReplayEngine.compute_brier_score(0.0, 1), 1.0)

    def test_log_score_math(self):
        log_loss_high = ChartReplayEngine.compute_log_score(0.90, 1)
        log_loss_low = ChartReplayEngine.compute_log_score(0.10, 1)
        self.assertLess(log_loss_high, log_loss_low)

    def test_murphy_brier_decomposition(self):
        forecasts = [0.8, 0.7, 0.6, 0.3, 0.2]
        outcomes = [1, 1, 0, 0, 0]

        decomp = ChartReplayEngine.decompose_brier(forecasts, outcomes, n_bins=3)
        # Hand computation with bins [0, 1/3), [1/3, 2/3), [2/3, 1]: {0.2, 0.3} -> 0/2, {0.6} -> 0/1, {0.7, 0.8} -> 2/2.
        # Reliability = 2/5 * 0.25^2 + 1/5 * 0.6^2 + 2/5 * 0.25^2 = 0.122; uncertainty = 0.4 * 0.6 = 0.24.
        self.assertAlmostEqual(decomp["reliability"], 0.122, places=4)
        self.assertAlmostEqual(decomp["uncertainty"], 0.24, places=4)
        self.assertAlmostEqual(decomp["brier"], (0.04 + 0.09 + 0.36 + 0.09 + 0.04) / 5, places=4)

    def test_ece_is_mean_absolute_gap_not_reliability(self):
        # Same bins as above: ECE = 2/5 * 0.25 + 1/5 * 0.6 + 2/5 * 0.25 = 0.32, while reliability (squared gaps) is 0.122.
        # Rejects reporting the Murphy reliability term under the ECE name.
        ece = ChartReplayEngine.expected_calibration_error([0.8, 0.7, 0.6, 0.3, 0.2], [1, 1, 0, 0, 0], n_bins=3)
        self.assertAlmostEqual(ece, 0.32, places=9)
        res = self.engine.run(level=2, num_trials=20, seed=7)
        trials = res.data["trials"]
        forecasts = [t["forecast_p"] for t in trials]
        expected = ChartReplayEngine.expected_calibration_error(forecasts, [int(t["outcome_higher"]) for t in trials])
        self.assertAlmostEqual(res.metrics["expected_calibration_error"], round(expected, 4), places=9)

    def test_determinism(self):
        res1 = self.engine.run(level=1, num_trials=5, seed=42)
        res2 = self.engine.run(level=1, num_trials=5, seed=42)
        self.assertEqual(res1.metrics, res2.metrics)
        self.assertEqual(res1.data, res2.data)

    def test_driftless_gbm_oracle_matches_closed_form(self):
        # Level 1 is GBM with mu = 0 and sigma = 0.20. ln(S_T / S_0) ~ N(-sigma^2 T / 2, sigma^2 T), so
        # P(S_T > S_0) = N(-sigma sqrt(T) / 2), strictly below 0.50; rejects the hard-coded 0.50 oracle.
        for horizon in (1, 5, 20):
            expected = normal_cdf(-0.5 * 0.20 * math.sqrt(horizon * DT))
            info = self.engine.generate_chart_trial(1, 50, horizon, seed=3)[1]
            self.assertAlmostEqual(info["oracle_probability"], expected, places=4)
            self.assertLess(info["oracle_probability"], 0.4999)

    def test_mean_reversion_oracle_matches_generator_monte_carlo(self):
        # Oracle: frequency of S_{t+h} > S_t over continuations simulated by the engine's own log-OU generator.
        # 40,000 seeded paths give a binomial SE <= 0.0025, so a 4 SE tolerance is 0.01. The old oracle divided
        # a dollar gap by a log-return sigma and returned about 0 here (clamped to 0.05).
        theta, kappa, sigma, horizon = 100.0, 3.0, 0.18, 20
        gen = SyntheticMarketGenerator(seed=2024)
        for s0 in (104.0, 97.0):
            n_paths = 40_000
            ups = sum(1 for _ in range(n_paths) if gen.generate_ar1_mean_reversion(s0, theta, kappa, sigma, horizon, DT)[-1] > s0)
            freq = ups / n_paths
            oracle = ChartReplayEngine.mean_reversion_oracle(s0, theta, kappa, sigma, horizon, DT)
            se = math.sqrt(freq * (1.0 - freq) / n_paths)
            with self.subTest(s0=s0):
                self.assertLess(abs(freq - oracle), 4.0 * se)
                self.assertGreater(abs(oracle - 0.5), 0.05)

    def test_oracle_is_calibrated_against_engine_outcomes(self):
        # A correct oracle is calibrated: among trials whose oracle falls in a bin, the up-frequency equals the mean
        # oracle within sampling error (4 binomial SE; seeded, so deterministic). Rejects the level-4 0.62 / 0.38
        # regime constants (true rates near 0.54 / 0.44) and the clamped level-3 dollar/log oracle.
        for level, n_trials in ((1, 6_000), (2, 6_000), (3, 10_000), (4, 16_000)):
            bins: dict[int, list[tuple[float, int]]] = {}
            for seed in range(n_trials):
                info = self.engine.generate_chart_trial(level, 20, 5, seed)[1]
                p = info["oracle_probability"]
                bins.setdefault(int(p * 20), []).append((p, info["binary_outcome"]))
            tested = 0
            for b, rows in bins.items():
                if len(rows) < 300:
                    continue
                tested += 1
                mean_p = sum(p for p, _ in rows) / len(rows)
                freq = sum(o for _, o in rows) / len(rows)
                se = math.sqrt(mean_p * (1.0 - mean_p) / len(rows))
                with self.subTest(level=level, bin=b, n=len(rows)):
                    self.assertLess(abs(freq - mean_p), 4.0 * se)
            self.assertGreater(tested, 0, level)

    def test_user_forecasts_are_scored(self):
        # All-1.0 forecasts score Brier = share of down trials (definition (f - o)^2); the old engine dropped them.
        res = self.engine.run(level=2, num_trials=6, seed=11, user_forecasts="1, 1,1,1,1, 1")
        trials = res.data["trials"]
        self.assertEqual(res.data["forecast_source"], "user")
        self.assertEqual([t["forecast_p"] for t in trials], [1.0] * 6)
        downs = sum(1 for t in trials if not t["outcome_higher"])
        self.assertAlmostEqual(res.metrics["mean_brier_score"], round(downs / 6, 4), places=9)

    def test_blank_user_forecasts_uses_simulated_forecaster(self):
        res = self.engine.run(level=2, num_trials=4, seed=11, user_forecasts="  ")
        self.assertEqual(res.data["forecast_source"], "simulated")
        self.assertEqual(res.metrics, self.engine.run(level=2, num_trials=4, seed=11).metrics)

    def test_invalid_user_forecasts_are_rejected(self):
        for raw in ("0.5,0.5", "0.5,0.5,0.5,0.5", "0.5,1.2,0.5", "0.5,-0.1,0.5", "0.5,nan,0.5", "0.5,up,0.5", "0.5,,0.5"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.engine.run(num_trials=3, user_forecasts=raw)

    def test_multilevel_execution(self):
        for lvl in (1, 2, 3, 4):
            res = self.engine.run(level=lvl, num_trials=3, seed=100 + lvl)
            self.assertIn("mean_brier_score", res.metrics)
            self.assertIn("expected_calibration_error", res.metrics)
            self.assertEqual(len(res.data["trials"]), 3)


if __name__ == "__main__":
    unittest.main()
