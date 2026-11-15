"""Interview Trading Games Engine (`games`).

Simulates proprietary trading firm interview market-making games:
1. Sequential dice roll sum game (Optiver/IMC style): three dice, one revealed after each quote.
2. Card-deck game (Jane Street/Flow Traders style): two cards drawn without replacement from a 52-card deck.

Each stage the quoter posts a two-sided market on the final sum and one counterparty arrives, as in
`tools/qp/drills.py` MarketMakingGame: with probability INFORMED_FRACTION it is informed and values the
sum at its true value, otherwise it is a noise trader that values it at the posterior mean given only the
revealed information plus Gaussian noise of 0.6 remaining standard deviations. It lifts the ask when its
value is above the ask and hits the bid when its value is below the bid; positions settle at the true sum.

The expected P&L of a quote with half-width h, X = true sum - posterior mean and noise sd s is
    E = (1 - p_informed) * 2 h * P(Z > h / s) - p_informed * E[(X - h)^+ + (-X - h)^+],
computed exactly by enumerating the dice or the deck. performance_score is the share of that theoretical
edge, under the optimal style, that the run captured: 100 * P&L / (rounds * edge per round), clipped to
[0, 100], so it does not grow with the number of rounds.
"""

from __future__ import annotations

import itertools
import math
import random
from functools import cache
from typing import Any

from .base import LabResult, Param, TradingLabEngine
from .registry import register

INFORMED_FRACTION = 0.10
NOISE_SD_MULTIPLE = 0.6  # noise trader valuation error, in remaining standard deviations of the sum
# Half-width in remaining standard deviations that maximizes the exact expected edge per round (0.01 grid)
OPTIMAL_HALF_WIDTH_SD = {"dice_sum": 0.50, "card_sum": 0.51}
WIDE_HALF_WIDTH_SD = 1.5  # a fixed half-width of 1.5 opening standard deviations, never narrowed

DICE = 3
DIE_FACES = range(1, 7)
DECK = tuple(rank for rank in range(1, 14) for _ in range(4))  # Ace = 1 ... King = 13, four suits


def _upper_tail(x: float) -> float:
    return 0.5 * math.erfc(x / math.sqrt(2.0))


@cache
def _remaining(game_type: str, revealed: tuple[int, ...]) -> tuple[float, tuple[float, ...]]:
    """Posterior mean of the final sum given the revealed values, and the equally likely outcomes of the sum."""
    if game_type == "dice_sum":
        unknown = DICE - len(revealed)
        outcomes = [float(sum(revealed) + sum(rest)) for rest in itertools.product(DIE_FACES, repeat=unknown)]
    elif not revealed:
        outcomes = [float(DECK[i] + DECK[j]) for i in range(len(DECK)) for j in range(len(DECK)) if i != j]
    else:
        deck = list(DECK)
        deck.remove(revealed[0])
        outcomes = [float(revealed[0] + card) for card in deck]
    return sum(outcomes) / len(outcomes), tuple(outcomes)


def posterior_mean(game_type: str, revealed: tuple[int, ...]) -> float:
    """E[final sum | revealed]; for cards E[c2 | c1] = (364 - c1) / 51 since 364 is the deck total."""
    return _remaining(game_type, revealed)[0]


@cache
def remaining_sd(game_type: str, revealed: tuple[int, ...]) -> float:
    mean, outcomes = _remaining(game_type, revealed)
    return math.sqrt(sum((o - mean) ** 2 for o in outcomes) / len(outcomes))


def stage_edge(game_type: str, revealed: tuple[int, ...], half_width: float) -> float:
    """Exact expected P&L of one quote of the given half-width around the posterior mean."""
    mean, outcomes = _remaining(game_type, revealed)
    noise_sd = NOISE_SD_MULTIPLE * remaining_sd(game_type, revealed)
    picked_off = sum(max(0.0, o - mean - half_width) + max(0.0, mean - o - half_width) for o in outcomes) / len(outcomes)
    noise_gain = 2.0 * half_width * _upper_tail(half_width / noise_sd)
    return (1.0 - INFORMED_FRACTION) * noise_gain - INFORMED_FRACTION * picked_off


def _stage_infos(game_type: str) -> list[list[tuple[float, tuple[int, ...]]]]:
    """Per stage, the (probability, revealed values) information states the quoter can face."""
    if game_type == "dice_sum":
        return [[(1.0 / 6**k, rolls) for rolls in itertools.product(DIE_FACES, repeat=k)] for k in range(DICE)]
    return [[(1.0, ())], [(DECK.count(rank) / len(DECK), (rank,)) for rank in range(1, 14)]]


@cache
def optimal_edge_per_round(game_type: str) -> float:
    """Exact expected P&L per round of the optimal style, the benchmark behind performance_score."""
    k = OPTIMAL_HALF_WIDTH_SD[game_type]
    return sum(
        prob * stage_edge(game_type, revealed, k * remaining_sd(game_type, revealed))
        for stage in _stage_infos(game_type)
        for prob, revealed in stage
    )


class InterviewTradingGamesEngine(TradingLabEngine):
    @property
    def engine_id(self) -> str:
        return "games"

    @property
    def name(self) -> str:
        return "Interview Trading Games Engine"

    @property
    def description(self) -> str:
        return "Simulates Optiver, Jane Street, and IMC interview card and dice quoting games."

    @property
    def asset_class(self) -> str:
        return "Interview Playbook / Trading Games"

    @property
    def params(self) -> dict[str, Param]:
        return {
            "game_type": Param(
                "game_type",
                "str",
                "dice_sum",
                "Game mode: 'dice_sum' (3 dice sequential) or 'card_sum' (2 cards drawn without replacement)",
                choices=["dice_sum", "card_sum"],
            ),
            "num_rounds": Param("num_rounds", "int", 20, "Number of game rounds played", min_val=5, max_val=100),
            "quoting_style": Param(
                "quoting_style",
                "str",
                "optimal",
                "Quoting agent: 'optimal' (posterior mean, width scaled to the remaining uncertainty), "
                "'wide_conservative' (fixed wide width) or 'naive_static' (never updates on revealed values)",
                choices=["optimal", "wide_conservative", "naive_static"],
            ),
            "seed": Param("seed", "int", 42, "Random seed"),
        }

    @staticmethod
    def quote(game_type: str, style: str, revealed: tuple[int, ...]) -> tuple[float, float]:
        """(centre, half-width) of the quote a style posts given the revealed values."""
        opening_sd = remaining_sd(game_type, ())
        if style == "optimal":
            return posterior_mean(game_type, revealed), OPTIMAL_HALF_WIDTH_SD[game_type] * remaining_sd(game_type, revealed)
        if style == "wide_conservative":
            return posterior_mean(game_type, revealed), WIDE_HALF_WIDTH_SD * opening_sd
        return posterior_mean(game_type, ()), OPTIMAL_HALF_WIDTH_SD[game_type] * opening_sd

    def run(self, **kwargs: Any) -> LabResult:
        p = self.validate_params(kwargs)
        game_type = str(p["game_type"])
        n_rounds = int(p["num_rounds"])
        style = str(p["quoting_style"])
        seed = int(p["seed"])

        rng = random.Random(seed)
        total_pnl = 0.0
        total_spread_quoted = 0.0
        total_quotes = 0
        trades_filled = 0
        correct_direction_count = 0
        round_history = []

        for r in range(n_rounds):
            if game_type == "dice_sum":
                values = [rng.randint(1, 6) for _ in range(DICE)]
            else:
                values = rng.sample(DECK, 2)
            true_final_sum = sum(values)

            round_trades = []
            round_quotes = []
            for stage in range(len(values)):
                revealed = tuple(values[:stage])
                fair_value = posterior_mean(game_type, revealed)
                centre, half_width = self.quote(game_type, style, revealed)
                bid = centre - half_width
                ask = centre + half_width
                total_spread_quoted += ask - bid
                total_quotes += 1
                round_quotes.append({"stage": stage + 1, "fair_value": round(fair_value, 6), "bid": round(bid, 4), "ask": round(ask, 4)})

                if rng.random() < INFORMED_FRACTION:
                    counterparty_value = float(true_final_sum)
                else:
                    counterparty_value = fair_value + rng.gauss(0.0, NOISE_SD_MULTIPLE * remaining_sd(game_type, revealed))

                if counterparty_value > ask:
                    # Counterparty lifts our ask: we sold at ask and settle at the true sum
                    trade_pnl = ask - true_final_sum
                    round_trades.append({"action": "sold_ask", "price": round(ask, 4), "pnl": round(trade_pnl, 4)})
                elif counterparty_value < bid:
                    # Counterparty hits our bid: we bought at bid and settle at the true sum
                    trade_pnl = true_final_sum - bid
                    round_trades.append({"action": "bought_bid", "price": round(bid, 4), "pnl": round(trade_pnl, 4)})
                else:
                    continue
                total_pnl += trade_pnl
                trades_filled += 1
                if trade_pnl > 0:
                    correct_direction_count += 1

            key = "dice" if game_type == "dice_sum" else "cards"
            round_history.append({"round": r + 1, key: values, "sum": true_final_sum, "quotes": round_quotes, "trades": round_trades})

        edge_per_round = optimal_edge_per_round(game_type)
        expected_optimal_pnl = n_rounds * edge_per_round
        avg_spread = total_spread_quoted / total_quotes if total_quotes > 0 else 0.0
        accuracy = (correct_direction_count / trades_filled) * 100 if trades_filled > 0 else 0.0
        score = max(0.0, min(100.0, 100.0 * total_pnl / expected_optimal_pnl))

        metrics = {
            "total_pnl": round(total_pnl, 2),
            "average_spread_quoted": round(avg_spread, 2),
            "total_quoting_stages": total_quotes,
            "pricing_accuracy_pct": round(accuracy, 1),
            "performance_score": round(score, 1),
            "rounds_completed": n_rounds,
        }

        summary = (
            f"Completed {n_rounds} rounds of '{game_type}' using '{style}' strategy. "
            f"Total PnL: {'-' if total_pnl < 0 else '+'}${abs(total_pnl):,.2f} "
            f"against an optimal-play expectation of +${expected_optimal_pnl:,.2f}, "
            f"Avg Spread: {avg_spread:.2f}, Pricing Accuracy: {accuracy:.1f}%, Score: {score:.1f}/100."
        )

        return LabResult(
            engine_id=self.engine_id,
            metrics=metrics,
            data={
                "rounds": round_history[:5],
                "theoretical_edge_per_round": round(edge_per_round, 6),
                "expected_optimal_pnl": round(expected_optimal_pnl, 4),
                "informed_fraction": INFORMED_FRACTION,
            },
            summary=summary,
        )


# Self-register
register(InterviewTradingGamesEngine())
