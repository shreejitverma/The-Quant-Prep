"""Unit tests for Event Case Files & Event Study Lab Engine."""

from __future__ import annotations

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
