"""Interview Trading Games Engine (`games`).

Simulates proprietary trading firm interview market-making games:
1. Sequential dice roll sum game (Optiver/IMC style)
2. Card-deck continuous market game (Jane Street/Flow Traders style)

Evaluates pricing accuracy, width discipline, inventory control, and edge capture.
"""

from __future__ import annotations

import random
from typing import Any

from .base import LabResult, Param, TradingLabEngine
from .registry import register


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
                "Game mode: 'dice_sum' (3 dice sequential) or 'card_sum' (2 cards drawn)",
                choices=["dice_sum", "card_sum"],
            ),
            "num_rounds": Param("num_rounds", "int", 20, "Number of game rounds played", min_val=5, max_val=100),
            "quoting_style": Param(
                "quoting_style",
                "str",
                "optimal",
                "Quoting agent: 'optimal' (mathematical expected value) or 'wide_conservative'",
                choices=["optimal", "wide_conservative"],
            ),
            "seed": Param("seed", "int", 42, "Random seed"),
        }

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

        if game_type == "dice_sum":
            # 3 six-sided dice: Expected value = 3 * 3.5 = 10.5
            for r in range(n_rounds):
                d1 = rng.randint(1, 6)
                d2 = rng.randint(1, 6)
                d3 = rng.randint(1, 6)
                true_final_sum = d1 + d2 + d3

                # Stage 1: Before any dice rolled (E[Sum] = 10.5)
                # Stage 2: After d1 revealed (E[Sum] = d1 + 7.0)
                # Stage 3: After d2 revealed (E[Sum] = d1 + d2 + 3.5)
                stages = [
                    ("unrevealed", 10.5),
                    ("d1_revealed", float(d1 + 7.0)),
                    ("d2_revealed", float(d1 + d2 + 3.5)),
                ]

                round_trades = []
                for _stage_name, expected_val in stages:
                    half_width = 0.75 if style == "optimal" else 1.50
                    bid = expected_val - half_width
                    ask = expected_val + half_width

                    total_spread_quoted += ask - bid
                    total_quotes += 1

                    # Simulated counterparty arrival:
                    # Counterparty has noisy perception of true final sum
                    noise = rng.gauss(0.0, 1.2)
                    cp_perceived_val = true_final_sum + noise

                    # If counterparty thinks it's higher than our ask, they buy our ask
                    if cp_perceived_val > ask:
                        # We sold at ask, settle at true_final_sum
                        trade_pnl = ask - true_final_sum
                        total_pnl += trade_pnl
                        round_trades.append({"action": "sold_ask", "price": ask, "pnl": trade_pnl})
                        trades_filled += 1
                        if ask > true_final_sum:
                            correct_direction_count += 1
                    # If counterparty thinks it's lower than our bid, they sell to our bid
                    elif cp_perceived_val < bid:
                        # We bought at bid, settle at true_final_sum
                        trade_pnl = true_final_sum - bid
                        total_pnl += trade_pnl
                        round_trades.append({"action": "bought_bid", "price": bid, "pnl": trade_pnl})
                        trades_filled += 1
                        if true_final_sum > bid:
                            correct_direction_count += 1

                round_history.append(
                    {
                        "round": r + 1,
                        "dice": [d1, d2, d3],
                        "sum": true_final_sum,
                        "trades": round_trades,
                    }
                )

        else:  # card_sum
            # 52 cards: Aces=1, 2-10 face, J=11, Q=12, K=13. Avg card = 7.0
            for r in range(n_rounds):
                c1 = rng.randint(1, 13)
                c2 = rng.randint(1, 13)
                true_final_sum = c1 + c2

                stages = [
                    ("unrevealed", 14.0),
                    ("card1_revealed", float(c1 + 7.0)),
                ]

                round_trades = []
                for _stage_name, expected_val in stages:
                    half_width = 1.0 if style == "optimal" else 2.0
                    bid = expected_val - half_width
                    ask = expected_val + half_width

                    total_spread_quoted += ask - bid
                    total_quotes += 1

                    noise = rng.gauss(0.0, 2.0)
                    cp_val = true_final_sum + noise

                    if cp_val > ask:
                        trade_pnl = ask - true_final_sum
                        total_pnl += trade_pnl
                        round_trades.append({"action": "sold_ask", "price": ask, "pnl": trade_pnl})
                        trades_filled += 1
                        if ask > true_final_sum:
                            correct_direction_count += 1
                    elif cp_val < bid:
                        trade_pnl = true_final_sum - bid
                        total_pnl += trade_pnl
                        round_trades.append({"action": "bought_bid", "price": bid, "pnl": trade_pnl})
                        trades_filled += 1
                        if true_final_sum > bid:
                            correct_direction_count += 1

                round_history.append(
                    {
                        "round": r + 1,
                        "cards": [c1, c2],
                        "sum": true_final_sum,
                        "trades": round_trades,
                    }
                )

        avg_spread = total_spread_quoted / total_quotes if total_quotes > 0 else 0.0
        accuracy = (correct_direction_count / trades_filled) * 100 if trades_filled > 0 else 0.0
        score = max(0.0, min(100.0, 50.0 + (total_pnl * 2.0) + (accuracy * 0.5)))

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
            f"Total PnL: ${total_pnl:+,.2f}, Avg Spread: {avg_spread:.2f}, "
            f"Pricing Accuracy: {accuracy:.1f}%, Score: {score:.1f}/100."
        )

        return LabResult(
            engine_id=self.engine_id,
            metrics=metrics,
            data={"rounds": round_history[:5]},
            summary=summary,
        )


# Self-register
register(InterviewTradingGamesEngine())
