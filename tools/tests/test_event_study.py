"""Unit tests for Event Case Files & Event Study Lab Engine."""

from __future__ import annotations

import math
import statistics
import unittest

from tools.qp.lab import get_engine
from tools.qp.lab.event_study import CRISIS_CATALOG, EventStudyEngine


class TestEventStudyEngine(unittest.TestCase):
    """Validates historical crisis simulations, CAR metrics, and hedging models."""

    def setUp(self) -> None:
        self.engine = get_engine("event_study")

    def test_engine_registration(self) -> None:
        self.assertIsNotNone(self.engine)
        self.assertIsInstance(self.engine, EventStudyEngine)
        self.assertEqual(self.engine.engine_id, "event_study")
        self.assertEqual(self.engine.asset_class, "Cross-Asset / Event-Driven")

    def test_crisis_catalog_completeness(self) -> None:
        expected_crises = [
            "1929_great_crash",
            "1987_black_monday",
            "1998_ltcm",
            "2000_dotcom",
            "2008_lehman",
            "2010_flash_crash",
            "2015_chf_unpeg",
            "2020_covid_oil",
            "2021_gamestop",
            "2022_uk_gilt_ldi",
        ]
        for crisis_id in expected_crises:
            self.assertIn(crisis_id, CRISIS_CATALOG)
            meta = CRISIS_CATALOG[crisis_id]
            self.assertTrue(len(meta["title"]) > 0)
            self.assertTrue(len(meta["primary_sources"]) >= 2)
            self.assertTrue(len(meta["daily_returns"]) >= 15)
            self.assertIn("peak_drop_pct", meta)

    def test_default_black_monday_run(self) -> None:
        res = self.engine.run(event_id="1987_black_monday", strategy="unhedged_long")
        metrics = res.metrics
        self.assertEqual(metrics["event_id"], "1987_black_monday")
        self.assertEqual(metrics["strategy"], "unhedged_long")
        self.assertLess(metrics["final_return_pct"], 0.0)
        self.assertGreater(metrics["max_drawdown_pct"], 15.0)
        self.assertIn("timeline", res.data)
        self.assertGreater(len(res.data["timeline"]), 10)
        self.assertIn("pre_mortem_score", metrics)

    def test_tail_hedge_reduces_drawdown(self) -> None:
        unhedged = self.engine.run(event_id="2008_lehman", strategy="unhedged_long")
        hedged = self.engine.run(event_id="2008_lehman", strategy="tail_hedged_put")

        self.assertLess(
            hedged.metrics["max_drawdown_pct"],
            unhedged.metrics["max_drawdown_pct"],
        )
        self.assertGreater(
            hedged.metrics["pre_mortem_score"],
            unhedged.metrics["pre_mortem_score"],
        )

    def test_same_seed_is_reproducible(self) -> None:
        # The old engine drew market noise from the unseeded global random module, so car_pct changed run to run.
        first = self.engine.run(event_id="2008_lehman", seed=7)
        second = self.engine.run(event_id="2008_lehman", seed=7)
        self.assertEqual(first.metrics, second.metrics)
        self.assertEqual(first.data["timeline"], second.data["timeline"])

    def test_different_seeds_draw_different_noise(self) -> None:
        cars = {self.engine.run(event_id="2008_lehman", seed=seed).metrics["car_pct"] for seed in range(5)}
        self.assertGreater(len(cars), 1)

    def test_equity_never_negative_and_trading_stops_at_ruin(self) -> None:
        # A -102.5% WTI day at 3x exposure, or the GME squeeze short-vol leg, would push equity below zero.
        # Limited liability: equity floors at 0 and a ruined account holds no further position.
        for event_id in ("2020_covid_oil", "2021_gamestop"):
            for strategy in ("unhedged_long", "short_volatility", "trend_follower"):
                with self.subTest(event_id=event_id, strategy=strategy):
                    res = self.engine.run(event_id=event_id, strategy=strategy, position_size_pct=300.0)
                    timeline = res.data["timeline"]
                    self.assertGreaterEqual(min(day["portfolio_equity"] for day in timeline), 0.0)
                    self.assertTrue(res.metrics["ruined"])
                    ruin_idx = next(i for i, day in enumerate(timeline) if day["ruined"])
                    self.assertTrue(all(day["portfolio_equity"] == 0.0 for day in timeline[ruin_idx:]))
                    self.assertEqual(res.metrics["final_return_pct"], -100.0)
                    self.assertEqual(res.metrics["max_drawdown_pct"], 100.0)

    def test_estimation_window_fit_recovers_market_model(self) -> None:
        # The estimation window is generated as R_i = alpha + beta R_m + e with sd(R_m) = 0.75 s and sd(e) = sqrt(1 - 0.75^2) s,
        # where s = sample sd of the event returns / vol_multiplier. OLS over L = 500 days has SE(beta) = sd(e) / (sd(R_m) sqrt(L))
        # and relative SE(residual sd) ~ 1 / sqrt(2 (L - 2)); tolerances are 4 SE. Rejects the hard-coded 1.5% residual vol.
        meta = CRISIS_CATALOG["2008_lehman"]
        normal_vol = statistics.stdev(meta["daily_returns"]) / meta["vol_multiplier"]
        idio_vol = math.sqrt(1.0 - 0.75**2) * normal_vol
        window = 500
        res = self.engine.run(event_id="2008_lehman", estimation_window=window, alpha=0.002, beta=1.5, seed=3)
        se_beta = idio_vol / (0.75 * normal_vol * math.sqrt(window))
        self.assertLess(abs(res.metrics["estimated_beta"] - 1.5), 4.0 * se_beta)
        self.assertLess(abs(res.metrics["estimated_alpha"] - 0.002), 4.0 * idio_vol / math.sqrt(window))
        resid_vol = res.metrics["estimation_residual_vol_pct"] / 100.0
        self.assertLess(abs(resid_vol / idio_vol - 1.0), 4.0 / math.sqrt(2.0 * (window - 2)))

    def test_estimation_window_length_changes_the_fit(self) -> None:
        short = self.engine.run(event_id="2008_lehman", estimation_window=50, seed=3).metrics
        long = self.engine.run(event_id="2008_lehman", estimation_window=500, seed=3).metrics
        self.assertNotEqual(short["estimated_beta"], long["estimated_beta"])
        self.assertNotEqual(short["patell_z_score"], long["patell_z_score"])

    def test_all_catalog_crises_execute_cleanly(self) -> None:
        for crisis_id in CRISIS_CATALOG:
            res = self.engine.run(event_id=crisis_id, strategy="cash_buffer_50pct")
            self.assertIn("car_pct", res.metrics)
            self.assertIn("patell_z_score", res.metrics)
            self.assertIsInstance(res.metrics["patell_z_score"], float)

    def test_toon_and_summary_output(self) -> None:
        res = self.engine.run(event_id="2010_flash_crash", strategy="stop_loss_5pct")
        toon = res.to_toon()
        self.assertIn("engine: event_study", toon)
        self.assertIn("metrics", toon)
        self.assertIn("summary:", toon)


if __name__ == "__main__":
    unittest.main()
