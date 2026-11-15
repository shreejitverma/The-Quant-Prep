"""Unit tests for tools/qp/lab/mm_quote.py and games.py."""

import itertools
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


def _mean_and_se(values: list[float]) -> tuple[float, float]:
    n = len(values)
    mean = sum(values) / n
    sd = math.sqrt(sum((v - mean) ** 2 for v in values) / (n - 1))
    return mean, sd / math.sqrt(n)


class TestInterviewGamesFairness(unittest.TestCase):
    """Seeds 0-299 are fixed in advance; every claim is a mean or share with three computed standard errors."""

    SEEDS = range(300)

    @classmethod
    def setUpClass(cls):
        engine = get_engine("games")
        cls.runs = {
            (game, style, rounds): [engine.run(game_type=game, quoting_style=style, num_rounds=rounds, seed=s) for s in cls.SEEDS]
            for game in ("dice_sum", "card_sum")
            for style in ("optimal", "wide_conservative", "naive_static")
            for rounds in (20,)
        }
        for game in ("dice_sum", "card_sum"):
            cls.runs[(game, "optimal", 100)] = [engine.run(game_type=game, num_rounds=100, seed=s) for s in cls.SEEDS]

    def test_cards_are_drawn_without_replacement_from_a_52_card_deck(self):
        # Oracle: enumerate the deck. After c1 the other 51 cards hold 364 - c1 points, so
        # E[c2 | c1] = (364 - c1) / 51, and a pair of equal ranks has probability 3/51 (1/13 with replacement).
        deck = [rank for rank in range(1, 14) for _ in range(4)]
        pairs = 0
        same_rank = 0
        for res in self.runs[("card_sum", "optimal", 20)]:
            for rnd in res.data["rounds"]:
                c1, c2 = rnd["cards"]
                rest = list(deck)
                rest.remove(c1)
                enumerated = c1 + sum(rest) / len(rest)
                self.assertAlmostEqual(enumerated, c1 + (364 - c1) / 51, places=12)
                self.assertAlmostEqual(rnd["quotes"][0]["fair_value"], 14.0, places=6)
                self.assertAlmostEqual(rnd["quotes"][1]["fair_value"], enumerated, places=6)
                pairs += 1
                same_rank += c1 == c2
        share = same_rank / pairs
        se = math.sqrt((3 / 51) * (48 / 51) / pairs)
        self.assertLess(abs(share - 3 / 51), 3 * se)
        self.assertGreater(abs(share - 1 / 13), 3 * se)

    def test_dice_fair_value_is_the_posterior_mean_of_the_revealed_dice(self):
        for res in self.runs[("dice_sum", "optimal", 20)][:20]:
            for rnd in res.data["rounds"]:
                dice = rnd["dice"]
                for stage, quote in enumerate(rnd["quotes"]):
                    unknown = 3 - stage
                    outcomes = [sum(dice[:stage]) + sum(rest) for rest in itertools.product(range(1, 7), repeat=unknown)]
                    self.assertAlmostEqual(quote["fair_value"], sum(outcomes) / len(outcomes), places=6)

    def test_optimal_style_has_positive_edge_and_beats_the_wide_style(self):
        # The counterparty must not see hidden dice or cards: against one that does, no width makes money.
        for game in ("dice_sum", "card_sum"):
            with self.subTest(game=game):
                opt = [r.metrics["total_pnl"] for r in self.runs[(game, "optimal", 20)]]
                wide = [r.metrics["total_pnl"] for r in self.runs[(game, "wide_conservative", 20)]]
                mean_opt, se_opt = _mean_and_se(opt)
                mean_wide, se_wide = _mean_and_se(wide)
                self.assertGreater(mean_opt - 3 * se_opt, 0.0)
                self.assertGreater(mean_opt - mean_wide, 3 * math.sqrt(se_opt**2 + se_wide**2))
                # The exact enumerated expectation the score is normalized by agrees with the simulation.
                expected = self.runs[(game, "optimal", 20)][0].data["expected_optimal_pnl"]
                self.assertLess(abs(mean_opt - expected), 3 * se_opt)

    def test_optimal_width_maximizes_the_enumerated_edge(self):
        # Oracle: enumerate every information state and outcome. A quote of half-width h around the posterior
        # mean earns h from a noise trader whose N(0, s) valuation error exceeds h (either side), and loses the
        # overshoot (X - h)^+ or (-X - h)^+ to an informed trader, X being the true sum minus the posterior mean.
        engine = get_engine("games")
        deck = [rank for rank in range(1, 14) for _ in range(4)]

        def states(game):
            if game == "dice_sum":
                for k in range(3):
                    for rolls in itertools.product(range(1, 7), repeat=k):
                        yield 6.0**-k, [sum(rolls) + sum(rest) for rest in itertools.product(range(1, 7), repeat=3 - k)]
            else:
                yield 1.0, [deck[i] + deck[j] for i in range(52) for j in range(52) if i != j]
                for c1 in range(1, 14):
                    rest = list(deck)
                    rest.remove(c1)
                    yield 4 / 52, [c1 + c for c in rest]

        def edge_per_round(game, k, p_informed, noise_multiple):
            total = 0.0
            for prob, outcomes in states(game):
                mean = sum(outcomes) / len(outcomes)
                sd = math.sqrt(sum((o - mean) ** 2 for o in outcomes) / len(outcomes))
                h = k * sd
                lost = sum(max(0.0, o - mean - h) + max(0.0, mean - o - h) for o in outcomes) / len(outcomes)
                gained = 2.0 * h * 0.5 * math.erfc(h / (noise_multiple * sd) / math.sqrt(2.0))
                total += prob * ((1.0 - p_informed) * gained - p_informed * lost)
            return total

        for game in ("dice_sum", "card_sum"):
            with self.subTest(game=game):
                res = engine.run(game_type=game, num_rounds=5)
                p_informed = res.data["informed_fraction"]
                quote = res.data["rounds"][0]["quotes"][0]
                outcomes = next(states(game))[1]
                mean = sum(outcomes) / len(outcomes)
                k = (quote["ask"] - quote["fair_value"]) / math.sqrt(sum((o - mean) ** 2 for o in outcomes) / len(outcomes))
                exact = edge_per_round(game, k, p_informed, 0.6)
                self.assertAlmostEqual(res.data["theoretical_edge_per_round"], exact, places=3)
                grid = [edge_per_round(game, j / 100, p_informed, 0.6) for j in range(10, 200, 5)]
                self.assertGreaterEqual(exact, max(grid) - 1e-3)
                self.assertGreater(exact, 0.0)

    def test_track_0_gate_is_reachable_by_optimal_play_and_not_by_naive_play(self):
        # markets.py passes the games requirement at performance_score >= 60.
        for game in ("dice_sum", "card_sum"):
            for style, rounds, reachable in (("optimal", 20, True), ("optimal", 100, True), ("naive_static", 20, False)):
                with self.subTest(game=game, style=style, rounds=rounds):
                    scores = [r.metrics["performance_score"] for r in self.runs[(game, style, rounds)]]
                    self.assertTrue(all(0.0 <= s <= 100.0 for s in scores))
                    share = sum(s >= 60.0 for s in scores) / len(scores)
                    se = math.sqrt(max(share * (1 - share), 1.0 / len(scores)) / len(scores))
                    if reachable:
                        self.assertGreater(share - 3 * se, 0.5)
                    else:
                        self.assertLess(share + 3 * se, 0.5)


if __name__ == "__main__":
    unittest.main()
