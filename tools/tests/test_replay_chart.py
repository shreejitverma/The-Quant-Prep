"""Unit tests for tools/qp/lab/replay_chart.py ChartReplayEngine."""

import unittest

from tools.qp.lab.registry import get_engine
from tools.qp.lab.replay_chart import ChartReplayEngine


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
        self.assertIn("brier", decomp)
        self.assertIn("reliability", decomp)
        self.assertIn("resolution", decomp)
        self.assertIn("uncertainty", decomp)

        # Expected uncertainty for base rate 2/5 = 0.4 -> 0.4 * 0.6 = 0.24
        self.assertAlmostEqual(decomp["uncertainty"], 0.24, places=2)
        # Brier is strictly bounded between 0 and 1
        self.assertGreaterEqual(decomp["brier"], 0.0)
        self.assertLessEqual(decomp["brier"], 1.0)

    def test_determinism_and_oracle_level1(self):
        res1 = self.engine.run(level=1, num_trials=5, seed=42)
        res2 = self.engine.run(level=1, num_trials=5, seed=42)

        self.assertEqual(res1.metrics["mean_brier_score"], res2.metrics["mean_brier_score"])
        self.assertEqual(res1.metrics["expected_calibration_error"], res2.metrics["expected_calibration_error"])

        # In Level 1 (random walk), every trial oracle probability should be exactly 0.50
        for trial in res1.data["trials"]:
            self.assertEqual(trial["oracle_p"], 0.50)

    def test_multilevel_execution(self):
        for lvl in (1, 2, 3, 4):
            res = self.engine.run(level=lvl, num_trials=3, seed=100 + lvl)
            self.assertIn("mean_brier_score", res.metrics)
            self.assertIn("expected_calibration_error", res.metrics)
            self.assertEqual(len(res.data["trials"]), 3)


if __name__ == "__main__":
    unittest.main()
