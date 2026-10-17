"""Unit tests for tools/qp/lab/mm_quote.py and games.py."""

import unittest

from tools.qp.lab.games import InterviewTradingGamesEngine
from tools.qp.lab.mm_quote import MarketMakerEngine
from tools.qp.lab.registry import get_engine


class TestMarketMakerAndGames(unittest.TestCase):
    def test_avellaneda_stoikov_inventory_skew(self):
        mid = 100.0
        gamma = 0.1
        sigma = 0.20
        kappa = 1.5
        time_left = 1.0

        # Long inventory (q = +10): reservation price must be lower than mid
        res_long, bid_long, ask_long = MarketMakerEngine.avellaneda_stoikov_quotes(mid, 10, gamma, sigma, kappa, time_left)
        self.assertLess(res_long, mid)
        self.assertLess(bid_long, mid)

        # Short inventory (q = -10): reservation price must be higher than mid
        res_short, bid_short, ask_short = MarketMakerEngine.avellaneda_stoikov_quotes(mid, -10, gamma, sigma, kappa, time_left)
        self.assertGreater(res_short, mid)
        self.assertGreater(ask_short, mid)

    def test_mm_pnl_attribution_sum(self):
        engine = get_engine("mm_quote")
        self.assertIsNotNone(engine)
        self.assertIsInstance(engine, MarketMakerEngine)

        res = engine.run(
            initial_price=100.0,
            gamma=0.1,
            sigma=0.20,
            kappa=1.5,
            informed_fraction=0.15,
            n_steps=80,
            strategy="avellaneda_stoikov",
            seed=42,
        )

        m = res.metrics
        total_pnl = m["total_pnl"]
        spread = m["spread_capture"]
        inv = m["inventory_pnl"]
        adverse = m["adverse_selection"]
        fees = m["exchange_fees"]

        # Exact attribution formula check: Total = Spread + Inventory + Adverse - Fees
        expected_total = round(spread + inv + adverse - fees, 2)
        self.assertAlmostEqual(total_pnl, expected_total, places=2)

    def test_interview_games_dice_and_cards(self):
        engine = get_engine("games")
        self.assertIsNotNone(engine)
        self.assertIsInstance(engine, InterviewTradingGamesEngine)

        # Dice sum game
        res_dice = engine.run(game_type="dice_sum", num_rounds=15, quoting_style="optimal", seed=10)
        self.assertEqual(res_dice.metrics["rounds_completed"], 15)
        self.assertIn("performance_score", res_dice.metrics)
        self.assertGreater(res_dice.metrics["performance_score"], 0.0)

        # Card sum game
        res_cards = engine.run(game_type="card_sum", num_rounds=15, quoting_style="wide_conservative", seed=20)
        self.assertEqual(res_cards.metrics["rounds_completed"], 15)
        self.assertIn("performance_score", res_cards.metrics)


if __name__ == "__main__":
    unittest.main()
