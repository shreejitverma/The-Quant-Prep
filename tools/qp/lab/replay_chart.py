"""Blind Chart Replay and Probability Calibration Engine.

Generates blind synthetic price chart segments across regimes, evaluates
user or automated probability forecasts against an analytical/Monte Carlo oracle,
and computes Murphy's Brier score decomposition, log loss, calibration curves,
and trade plan expectancy.

Standard-library only, fully deterministic.
"""

from __future__ import annotations

import math
import random
from typing import Any

from .base import LabResult, Param, TradingLabEngine
from .market import SyntheticMarketGenerator
from .registry import register


class ChartReplayEngine(TradingLabEngine):
    @property
    def engine_id(self) -> str:
        return "replay_chart"

    @property
    def name(self) -> str:
        return "Blind Chart Replay and Calibration Engine"

    @property
    def description(self) -> str:
        return (
            "Presents blind chart sequences across market regimes, evaluates probability "
            "forecasts against an oracle, and computes Brier scores, calibration error, and trade plan expectancy."
        )

    @property
    def asset_class(self) -> str:
        return "Technical Analysis / Multi-Asset"

    @property
    def params(self) -> dict[str, Param]:
        return {
            "level": Param("level", "int", 1, "Simulation level (1: Random Walk, 2: Trend, 3: Mean Reversion, 4: Regime Switching)", 1, 4),
            "bars_visible": Param("bars_visible", "int", 50, "Number of historical bars revealed to the forecaster", 20, 200),
            "forecast_horizon": Param("forecast_horizon", "int", 5, "Number of future bars to predict (h-step horizon)", 1, 20),
            "num_trials": Param("num_trials", "int", 10, "Number of consecutive chart replay evaluation trials", 1, 50),
            "seed": Param("seed", "int", 42, "Deterministic random seed", 0, 999999),
        }

    @staticmethod
    def compute_brier_score(forecast: float, outcome: int) -> float:
        """Single-event Brier score: (f - o)^2."""
        return (forecast - float(outcome)) ** 2

    @staticmethod
    def compute_log_score(forecast: float, outcome: int) -> float:
        """Single-event negative log likelihood (cross-entropy)."""
        eps = 1e-6
        p = max(eps, min(1.0 - eps, forecast))
        return -math.log(p) if outcome == 1 else -math.log(1.0 - p)

    @classmethod
    def decompose_brier(cls, forecasts: list[float], outcomes: list[int], n_bins: int = 5) -> dict[str, float]:
        """Murphy (1973) Brier score decomposition: Brier = Reliability - Resolution + Uncertainty."""
        n = len(forecasts)
        if n == 0:
            return {"brier": 0.0, "reliability": 0.0, "resolution": 0.0, "uncertainty": 0.0}

        base_rate = sum(outcomes) / n
        uncertainty = base_rate * (1.0 - base_rate)

        # Partition forecasts into bins
        bin_width = 1.0 / n_bins
        bins: list[list[int]] = [[] for _ in range(n_bins)]
        for idx, f in enumerate(forecasts):
            b_idx = min(n_bins - 1, int(f / bin_width))
            bins[b_idx].append(idx)

        reliability = 0.0
        resolution = 0.0

        for b_indices in bins:
            if not b_indices:
                continue
            n_k = len(b_indices)
            f_k_mean = sum(forecasts[i] for i in b_indices) / n_k
            o_k_mean = sum(outcomes[i] for i in b_indices) / n_k

            reliability += (n_k / n) * ((f_k_mean - o_k_mean) ** 2)
            resolution += (n_k / n) * ((o_k_mean - base_rate) ** 2)

        mean_brier = sum(cls.compute_brier_score(f, o) for f, o in zip(forecasts, outcomes, strict=True)) / n

        return {
            "brier": round(mean_brier, 4),
            "reliability": round(reliability, 4),
            "resolution": round(resolution, 4),
            "uncertainty": round(uncertainty, 4),
        }

    def generate_chart_trial(
        self,
        level: int,
        bars_visible: int,
        horizon: int,
        seed: int,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """Generate visible bars, future path, and analytical oracle probability."""
        gen = SyntheticMarketGenerator(seed=seed)
        total_bars = bars_visible + horizon
        dt = 1.0 / 252.0

        if level == 1:
            # Pure Random Walk (GBM with mu = 0.0): Oracle is exactly 0.50
            prices = gen.generate_gbm(s0=100.0, mu=0.0, sigma=0.20, n_steps=total_bars, dt=dt)
            oracle_p = 0.50
            regime_label = "random_walk"
        elif level == 2:
            # Trend Regime: Alternating strong drift up or down
            drift_direction = 1.0 if (seed % 2 == 0) else -1.0
            mu = 0.18 * drift_direction
            sigma = 0.16
            prices = gen.generate_gbm(s0=100.0, mu=mu, sigma=sigma, n_steps=total_bars, dt=dt)
            oracle_p = gen.oracle_probability_higher(prices[bars_visible - 1], horizon, mu=mu, sigma=sigma, dt=dt)
            regime_label = "bull_trend" if drift_direction > 0 else "bear_trend"
        elif level == 3:
            # Mean Reverting AR(1) / Ornstein-Uhlenbeck
            theta = 100.0
            kappa = 3.0
            sigma = 0.18
            prices = gen.generate_ar1_mean_reversion(
                s0=105.0 if (seed % 2 == 0) else 95.0,
                theta=theta,
                kappa=kappa,
                sigma=sigma,
                n_steps=total_bars,
                dt=dt,
            )
            curr_price = prices[bars_visible - 1]
            # If price is above theta, reversion probability of higher is < 0.5; if below, > 0.5
            expected_future = theta + (curr_price - theta) * math.exp(-kappa * horizon * dt)
            oracle_p = 0.5 * (1.0 + math.erf((expected_future - curr_price) / (sigma * math.sqrt(horizon * dt) * math.sqrt(2.0))))
            oracle_p = max(0.05, min(0.95, oracle_p))
            regime_label = "mean_reversion"
        else:
            # Level 4: Hidden Markov Regime Switching with GARCH and jumps
            bars = gen.generate_regime_path(s0=100.0, n_bars=total_bars, dt=dt)
            prices = [b.close for b in bars]
            curr_regime = bars[bars_visible - 1].regime
            if curr_regime == "bull":
                oracle_p = 0.62
            elif curr_regime == "bear":
                oracle_p = 0.38
            else:
                oracle_p = 0.50
            regime_label = f"markov_{curr_regime}"

        visible_prices = prices[:bars_visible]
        future_prices = prices[bars_visible : bars_visible + horizon]
        current_price = visible_prices[-1]
        final_price = future_prices[-1]

        binary_outcome = 1 if final_price > current_price else 0

        chart_data = {
            "visible_series": [round(p, 2) for p in visible_prices],
            "current_price": round(current_price, 2),
            "final_price": round(final_price, 2),
            "binary_outcome": binary_outcome,
            "oracle_probability": round(oracle_p, 4),
            "regime": regime_label,
            "return_pct": round(((final_price - current_price) / current_price) * 100.0, 2),
        }

        return chart_data, chart_data

    def run(self, **kwargs: Any) -> LabResult:
        params = self.validate_params(kwargs)
        level = int(params.get("level", 1))
        bars_visible = int(params.get("bars_visible", 50))
        horizon = int(params.get("forecast_horizon", 5))
        num_trials = int(params.get("num_trials", 10))
        base_seed = int(params.get("seed", 42))

        # Check for user-provided forecasts; if absent, simulate a calibrated technical trader with noise
        user_forecasts_input = params.get("user_forecasts")

        forecasts: list[float] = []
        oracle_probs: list[float] = []
        outcomes: list[int] = []
        trial_records: list[dict[str, Any]] = []

        rng = random.Random(base_seed)

        for trial_idx in range(num_trials):
            trial_seed = base_seed + trial_idx * 1007
            _, trial_info = self.generate_chart_trial(level, bars_visible, horizon, trial_seed)

            oracle_p = trial_info["oracle_probability"]
            outcome = trial_info["binary_outcome"]

            if user_forecasts_input and trial_idx < len(user_forecasts_input):
                f_p = float(user_forecasts_input[trial_idx])
            else:
                # Simulated forecaster: blends oracle with noisy technical chart bias
                chart_noise = rng.gauss(0.0, 0.12)
                f_p = round(max(0.05, min(0.95, oracle_p + chart_noise)), 2)

            f_p = max(0.01, min(0.99, f_p))
            forecasts.append(f_p)
            oracle_probs.append(oracle_p)
            outcomes.append(outcome)

            brier = self.compute_brier_score(f_p, outcome)
            log_loss = self.compute_log_score(f_p, outcome)
            oracle_brier = self.compute_brier_score(oracle_p, outcome)

            # Simulated Trade Plan evaluation:
            # If forecast >= 0.55 -> Long; If forecast <= 0.45 -> Short; Else -> Flat
            plan_action = "long" if f_p >= 0.55 else ("short" if f_p <= 0.45 else "flat")
            ret_pct = trial_info["return_pct"]
            if plan_action == "long":
                plan_pnl_r = 1.0 if ret_pct > 0.5 else (-1.0 if ret_pct < -0.5 else ret_pct / 0.5)
            elif plan_action == "short":
                plan_pnl_r = 1.0 if ret_pct < -0.5 else (-1.0 if ret_pct > 0.5 else -ret_pct / 0.5)
            else:
                plan_pnl_r = 0.0

            trial_records.append(
                {
                    "trial": trial_idx + 1,
                    "regime": trial_info["regime"],
                    "current_price": trial_info["current_price"],
                    "final_price": trial_info["final_price"],
                    "return_pct": ret_pct,
                    "outcome_higher": outcome == 1,
                    "forecast_p": f_p,
                    "oracle_p": oracle_p,
                    "brier_score": round(brier, 4),
                    "oracle_brier": round(oracle_brier, 4),
                    "log_loss": round(log_loss, 4),
                    "plan_action": plan_action,
                    "plan_pnl_r": round(plan_pnl_r, 2),
                }
            )

        decomp = self.decompose_brier(forecasts, outcomes, n_bins=5)
        mean_brier = decomp["brier"]
        oracle_mean_brier = sum(self.compute_brier_score(op, o) for op, o in zip(oracle_probs, outcomes, strict=True)) / len(outcomes)
        mean_log_loss = sum(self.compute_log_score(f, o) for f, o in zip(forecasts, outcomes, strict=True)) / len(outcomes)

        # Brier Skill Score vs naive 0.50 reference
        naive_brier = 0.25
        brier_skill_score = 1.0 - (mean_brier / naive_brier)

        # Expected Calibration Error (ECE)
        ece = decomp["reliability"]

        # Trade Plan metrics
        active_plans = [r for r in trial_records if r["plan_action"] != "flat"]
        avg_r = sum(r["plan_pnl_r"] for r in active_plans) / max(1, len(active_plans))
        win_count = sum(1 for r in active_plans if r["plan_pnl_r"] > 0)
        win_rate = (win_count / max(1, len(active_plans))) * 100.0

        metrics = {
            "level": level,
            "total_trials": num_trials,
            "mean_brier_score": round(mean_brier, 4),
            "oracle_brier_score": round(oracle_mean_brier, 4),
            "brier_skill_score": round(brier_skill_score, 4),
            "expected_calibration_error": round(ece, 4),
            "mean_log_loss": round(mean_log_loss, 4),
            "reliability": decomp["reliability"],
            "resolution": decomp["resolution"],
            "uncertainty": decomp["uncertainty"],
            "trade_plans_executed": len(active_plans),
            "win_rate_pct": round(win_rate, 1),
            "average_plan_r": round(avg_r, 2),
        }

        summary = (
            f"Chart Replay Calibration session complete ({num_trials} trials, Level {level}). "
            f"Brier Score: {mean_brier:.4f} (Oracle: {oracle_mean_brier:.4f}, Skill: {brier_skill_score:+.2f}). "
            f"ECE: {ece:.4f}, Win Rate: {win_rate:.1f}%, Avg Expectancy: {avg_r:+.2f}R."
        )

        return LabResult(
            engine_id=self.engine_id,
            metrics=metrics,
            data={"trials": trial_records, "brier_decomposition": decomp},
            summary=summary,
        )


# Register engine with Trading Lab catalog
register(ChartReplayEngine())
