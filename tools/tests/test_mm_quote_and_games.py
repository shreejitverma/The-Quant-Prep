"""Unit tests for tools/qp/lab/mm_quote.py and games.py."""

import math
import unittest

from tools.qp.lab.games import InterviewTradingGamesEngine
from tools.qp.lab.mm_quote import MarketMakerEngine
from tools.qp.lab.registry import get_engine

LOT = 100


def as_oracle(mid, lots, gamma_pct, sigma_annual, kappa_pct, tau):
    """Avellaneda-Stoikov (2008) closed form, written out independently of the engine.

    Dollar volatility per square root of a one-day session is sigma * mid / sqrt(252);
    gamma and kappa per 1% of mid become per dollar by dividing by 0.01 * mid.
    """
    sigma_d = sigma_annual * mid / math.sqrt(252.0)
    gamma_d = gamma_pct / (0.01 * mid)
    kappa_d = kappa_pct / (0.01 * mid)
    reservation = mid - lots * gamma_d * sigma_d**2 * tau
    spread = gamma_d * sigma_d**2 * tau + (2.0 / gamma_d) * math.log(1.0 + gamma_d / kappa_d)
    return reservation, spread


class TestMarketMakerAndGames(unittest.TestCase):
    def setUp(self):
        self.engine = get_engine("mm_quote")

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

    def test_quotes_match_avellaneda_stoikov_closed_form(self):
        # Rejects treating fractional sigma as dollars, a horizon that ignores the session clock,
        # and inventory counted in shares instead of lots: each shifts r or the spread off the formula.
        params = {"initial_price": 250.0, "gamma": 0.1, "sigma": 0.20, "kappa": 1.5, "n_steps": 120, "seed": 7}
        res = self.engine.run(**params)
        quotes = res.data["quotes"]
        self.assertEqual(len(quotes), params["n_steps"])
        skewed = 0
        for q in quotes:
            if q["bid"] is None:
                continue
            lots, tau = q["inventory_lots"], q["time_left"]
            reservation, spread = as_oracle(q["mid"], lots, params["gamma"], params["sigma"], params["kappa"], tau)
            self.assertAlmostEqual(q["reservation"], reservation, delta=1e-4 * q["mid"])
            self.assertAlmostEqual(q["ask"] - q["bid"], spread, delta=1e-4 * q["mid"])
            self.assertAlmostEqual((q["ask"] + q["bid"]) / 2.0, reservation, delta=1e-4 * q["mid"])
            skewed += q["inventory_lots"] != 0
        self.assertGreater(skewed, 0, "the run never carried inventory, so the skew term went untested")
        self.assertEqual(quotes[0]["time_left"], 1.0)

    def test_quotes_positive_and_scale_invariant_in_price(self):
        # At $1 with the lowest risk aversion and thinnest book the old dollar-unit formula quoted bid -8.95.
        low = {"gamma": 0.001, "kappa": 0.1, "sigma": 0.20, "seed": 3}
        cheap = self.engine.run(initial_price=1.0, **low)
        rich = self.engine.run(initial_price=10000.0, **low)
        for q in cheap.data["quotes"]:
            self.assertGreater(q["ask"], 0.0)
            if q["bid"] is not None:
                self.assertGreater(q["bid"], 0.0)
        for qc, qr in zip(cheap.data["quotes"], rich.data["quotes"], strict=True):
            self.assertAlmostEqual(qc["ask"] / qc["mid"], qr["ask"] / qr["mid"], delta=1e-5)

        # The same seed at 10000x the price is the same economy in different currency units:
        # every quote in bps and every fill must match, and PnL must scale by exactly 10000.
        for strategy in ("avellaneda_stoikov", "naive_symmetric"):
            a = self.engine.run(initial_price=1.0, strategy=strategy, seed=11)
            b = self.engine.run(initial_price=10000.0, strategy=strategy, seed=11)
            qa, qb = a.data["quotes"][0], b.data["quotes"][0]
            spread_bps_a = (qa["ask"] - qa["bid"]) / qa["mid"] * 1e4
            spread_bps_b = (qb["ask"] - qb["bid"]) / qb["mid"] * 1e4
            self.assertAlmostEqual(spread_bps_a, spread_bps_b, delta=0.01)
            self.assertEqual(a.metrics["trades_executed"], b.metrics["trades_executed"])
            self.assertEqual(a.metrics["final_inventory"], b.metrics["final_inventory"])
            self.assertAlmostEqual(b.metrics["total_pnl"], 10000.0 * a.metrics["total_pnl"], delta=0.01 * 10000.0 + 0.01)

    def test_rejects_configuration_with_non_positive_opening_bid(self):
        # gamma=10, sigma=2.0 imply a half-spread of about 794% of mid at the open.
        _r, spread = as_oracle(100.0, 0, 10.0, 2.0, 1.5, 1.0)
        self.assertGreater(spread / 2.0, 100.0)
        with self.assertRaises(ValueError):
            self.engine.run(gamma=10.0, sigma=2.0, kappa=1.5)

    def test_adverse_selection_is_signed_markout(self):
        # With no informed flow, post-fill moves are pure noise: some markouts must be gains.
        # A sign-blind abs() books every move as a loss and makes the bucket <= 0 on every seed.
        bucket_values = []
        favourable = 0
        for seed in range(8):
            res = self.engine.run(informed_fraction=0.0, seed=seed)
            fills = res.data["fills"]
            recomputed = 0.0
            for f in fills:
                side = 1 if f["side"] == "buy" else -1
                move = side * (f["post_mid"] - f["pre_mid"]) * LOT
                self.assertAlmostEqual(f["markout"], move, delta=1e-3)
                recomputed += move
                favourable += move > 0
            self.assertAlmostEqual(res.metrics["adverse_selection"], recomputed, delta=0.01 + 1e-3 * len(fills))
            bucket_values.append(res.metrics["adverse_selection"])
        self.assertGreater(favourable, 0)
        self.assertGreater(max(bucket_values), 0.0)

        # Glosten-Milgrom: informed flow moves the mid against the fill, so the bucket is a net loss.
        toxic = [self.engine.run(informed_fraction=0.9, seed=seed).metrics["adverse_selection"] for seed in range(8)]
        self.assertLess(sum(toxic), 0.0)
        self.assertLess(sum(toxic), sum(bucket_values))

    def test_mm_pnl_attribution_sum(self):
        self.assertIsNotNone(self.engine)
        self.assertIsInstance(self.engine, MarketMakerEngine)

        res = self.engine.run(
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

        # Total PnL is marked from cash and inventory; the four buckets are accumulated separately
        # per fill and per step, so the identity checks the attribution rather than defining it.
        fees = sum(1e-5 * f["price"] * LOT for f in res.data["fills"])
        self.assertAlmostEqual(m["exchange_fees"], fees, delta=0.01)
        expected_total = m["spread_capture"] + m["inventory_pnl"] + m["adverse_selection"] - m["exchange_fees"]
        self.assertAlmostEqual(m["total_pnl"], expected_total, delta=0.05)

        cash = 0.0
        for f in res.data["fills"]:
            side = 1 if f["side"] == "buy" else -1
            cash -= side * f["price"] * LOT + 1e-5 * f["price"] * LOT
        marked = cash + m["final_inventory"] * m["ending_mid_price"]
        self.assertAlmostEqual(m["total_pnl"], marked, delta=0.01 * len(res.data["fills"]) + 0.01 * abs(m["final_inventory"]))

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

    def test_games_accuracy_counts_only_filled_trades(self):
        # Accuracy is the share of executed trades that made money; quotes nobody hit are not trades.
        # Dividing by every quoting stage drags the score toward zero whenever fills are sparse.
        engine = get_engine("games")
        checked = 0
        for game_type in ("dice_sum", "card_sum"):
            for seed in range(6):
                res = engine.run(game_type=game_type, num_rounds=5, seed=seed)
                trades = [t for rnd in res.data["rounds"] for t in rnd["trades"]]
                self.assertEqual(len(res.data["rounds"]), 5)
                if not trades:
                    self.assertEqual(res.metrics["pricing_accuracy_pct"], 0.0)
                    continue
                expected = round(100.0 * sum(t["pnl"] > 0 for t in trades) / len(trades), 1)
                self.assertEqual(res.metrics["pricing_accuracy_pct"], expected)
                checked += len(trades) < res.metrics["total_quoting_stages"]
        self.assertGreater(checked, 0, "no run had unfilled quotes, so the denominator went untested")


if __name__ == "__main__":
    unittest.main()
