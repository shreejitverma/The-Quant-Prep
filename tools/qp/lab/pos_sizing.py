"""Position Sizing and Risk of Ruin Engine (`pos_sizing`).

Calculates Full Kelly, Half Kelly, growth rate curves, time under water,
and runs Monte Carlo path simulations over Bernoulli or fat-tailed trade distributions.
"""

from __future__ import annotations

import math
import random
from typing import Any

from .base import LabResult, Param, TradingLabEngine
from .registry import register

# Paths that compound past this stop there: it exceeds global financial wealth, and compounding
# further overflows float equity to inf, which turns drawdowns and the summary statistics into NaN.
EQUITY_CEILING = 1e15


class PositionSizingEngine(TradingLabEngine):
    @property
    def engine_id(self) -> str:
        return "pos_sizing"

    @property
    def name(self) -> str:
        return "Position Sizing and Risk of Ruin Engine"

    @property
    def description(self) -> str:
        return "Evaluates Kelly criterion, growth curve, fat-tailed ruin, and time-under-water risk."

    @property
    def asset_class(self) -> str:
        return "Risk Management / Cross-Asset"

    @property
    def params(self) -> dict[str, Param]:
        return {
            "account_capital": Param(
                name="account_capital",
                param_type="float",
                default=100000.0,
                min_val=100.0,
                description="Starting capital in base currency units",
            ),
            "win_rate": Param(
                name="win_rate",
                param_type="float",
                default=0.55,
                min_val=0.01,
                max_val=0.99,
                description="Historical trade win probability (0.0 to 1.0)",
            ),
            "win_loss_ratio": Param(
                name="win_loss_ratio",
                param_type="float",
                default=1.5,
                min_val=0.1,
                description="Ratio of average winning trade size to average losing trade size (b)",
            ),
            "risk_per_trade_pct": Param(
                name="risk_per_trade_pct",
                param_type="float",
                default=0.02,
                min_val=0.001,
                max_val=0.50,
                description="Fraction of current account equity risked per trade",
            ),
            "distribution": Param(
                name="distribution",
                param_type="str",
                default="bernoulli",
                choices=["bernoulli", "fat_tailed"],
                description="Trade outcome distribution: 'bernoulli' or 'fat_tailed' (occasional slippage jumps)",
            ),
            "num_trades": Param(
                name="num_trades",
                param_type="int",
                default=100,
                min_val=10,
                max_val=1000,
                description="Number of sequential trades per simulation path",
            ),
            "num_simulations": Param(
                name="num_simulations",
                param_type="int",
                default=500,
                min_val=50,
                max_val=5000,
                description="Number of Monte Carlo paths generated",
            ),
            "ruin_drawdown_pct": Param(
                name="ruin_drawdown_pct",
                param_type="float",
                default=0.50,
                min_val=0.10,
                max_val=0.99,
                description="Equity drawdown threshold defining account ruin (e.g. 0.50 = 50%)",
            ),
            "seed": Param(
                name="seed",
                param_type="int",
                default=42,
                description="Pseudo-random number generator seed for reproducibility",
            ),
        }

    @staticmethod
    def calculate_growth_rate(f: float, p: float, b: float) -> float:
        """Geometric compound growth rate: g(f) = p * ln(1 + b*f) + (1 - p) * ln(1 - f)."""
        if f <= 0.0:
            return 0.0
        if f >= 1.0:
            return -float("inf")
        term_win = p * math.log(1.0 + b * f)
        term_loss = (1.0 - p) * math.log(1.0 - f)
        return term_win + term_loss

    def run(self, **kwargs: Any) -> LabResult:
        p = self.validate_params(kwargs)
        capital = float(p["account_capital"])
        p_win = float(p["win_rate"])
        b = float(p["win_loss_ratio"])
        f_risk = float(p["risk_per_trade_pct"])
        dist_mode = str(p["distribution"])
        n_trades = int(p["num_trades"])
        n_sims = int(p["num_simulations"])
        ruin_thresh = float(p["ruin_drawdown_pct"])
        seed = int(p["seed"])

        # Kelly Formula: f* = p - (1 - p) / b = (p*(b + 1) - 1) / b
        f_kelly = p_win - (1.0 - p_win) / b
        f_half_kelly = 0.5 * f_kelly

        # Calculate Growth Rate Curve points across fractions
        growth_curve: list[dict[str, float]] = []
        if f_kelly > 0:
            max_eval_f = min(0.90, max(0.10, f_kelly * 2.5))
            steps = 25
            for i in range(1, steps + 1):
                f_val = round((max_eval_f / steps) * i, 4)
                g_val = self.calculate_growth_rate(f_val, p_win, b)
                growth_curve.append({"f": f_val, "growth_rate": round(g_val, 6)})

        # Monte Carlo Simulation
        rng = random.Random(seed)
        final_equities = []
        max_drawdowns = []
        time_under_water_list = []
        ruin_count = 0
        capped_count = 0
        sample_paths = []

        for sim_idx in range(n_sims):
            equity = capital
            peak = capital
            sim_max_dd = 0.0
            equity_curve = [equity]

            time_under_water = 0
            current_under_water = 0

            for _ in range(n_trades):
                bet_size = equity * f_risk
                if rng.random() < p_win:
                    pnl = bet_size * b
                else:
                    if dist_mode == "fat_tailed" and rng.random() < 0.05:
                        # 5% probability of gap/slippage causing 2.5x standard loss
                        pnl = -bet_size * 2.5
                    else:
                        pnl = -bet_size

                equity += pnl
                if equity <= 0:
                    equity = 0.0
                capped = equity >= EQUITY_CEILING
                if capped:
                    equity = EQUITY_CEILING

                if equity > peak:
                    peak = equity
                    current_under_water = 0
                else:
                    current_under_water += 1
                    if current_under_water > time_under_water:
                        time_under_water = current_under_water

                dd = (peak - equity) / peak if peak > 0 else 1.0
                if dd > sim_max_dd:
                    sim_max_dd = dd

                equity_curve.append(equity)
                if equity <= 0 or capped:
                    capped_count += capped
                    break

            final_equities.append(equity)
            max_drawdowns.append(sim_max_dd)
            time_under_water_list.append(time_under_water)
            if sim_max_dd >= ruin_thresh:
                ruin_count += 1

            if sim_idx < 5:
                sample_paths.append([round(v, 2) for v in equity_curve])

        final_equities.sort()
        max_drawdowns.sort()
        time_under_water_list.sort()

        median_equity = final_equities[len(final_equities) // 2]
        mean_equity = sum(final_equities) / len(final_equities)
        mean_dd = sum(max_drawdowns) / len(max_drawdowns)
        p95_dd = max_drawdowns[int(len(max_drawdowns) * 0.95)]
        median_tuw = time_under_water_list[len(time_under_water_list) // 2]
        ruin_probability = ruin_count / n_sims

        metrics: dict[str, float | int | str] = {
            "kelly_fraction": round(f_kelly, 4),
            "half_kelly_fraction": round(f_half_kelly, 4),
            "median_final_equity": round(median_equity, 2),
            "mean_final_equity": round(mean_equity, 2),
            "mean_max_drawdown": round(mean_dd, 4),
            "p95_max_drawdown": round(p95_dd, 4),
            "median_time_under_water_bars": median_tuw,
            "ruin_probability": round(ruin_probability, 4),
            "simulations_run": n_sims,
            "paths_capped_at_ceiling": capped_count,
        }

        summary = (
            f"Kelly fraction is {f_kelly * 100:.1f}%. At {f_risk * 100:.1f}% risk per trade ({dist_mode}), "
            f"median terminal equity is {median_equity:,.0f} with a {ruin_probability * 100:.1f}% "
            f"probability of suffering a >={ruin_thresh * 100:.0f}% drawdown."
        )

        return LabResult(
            engine_id=self.engine_id,
            metrics=metrics,
            data={
                "params": p,
                "growth_curve": growth_curve,
                "sample_paths": sample_paths,
            },
            summary=summary,
        )


# Self-register upon import
register(PositionSizingEngine())
