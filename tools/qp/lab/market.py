"""Synthetic market data engine for Trading Lab simulators.

Generates realistic price paths and OHLCV bars using:
1. Geometric Brownian Motion (GBM)
2. Mean-Reverting Ornstein-Uhlenbeck / AR(1) in log price
3. GARCH(1,1) volatility clustering
4. Merton jump diffusion
5. Hidden Markov regime switching (Calm Trending, Choppy Consolidation, Volatile Crash)

Standard-library only, fully deterministic from (version, seed, params).
Includes an Oracle conditional probability evaluator for forecast calibration.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any

GENERATOR_VERSION = 2

# Per-regime GARCH(1,1) dynamics; "vol" is the annualized long-run volatility, from which
# omega is set so the stationary variance omega / (1 - alpha - beta) matches it per sub-step.
REGIME_PARAMS: dict[str, dict[str, float]] = {
    "bull": {"mu": 0.15, "vol": 0.16, "alpha": 0.08, "beta": 0.88, "jump_prob": 0.01, "jump_mu": 0.01},
    "bear": {"mu": -0.25, "vol": 0.32, "alpha": 0.15, "beta": 0.80, "jump_prob": 0.04, "jump_mu": -0.03},
    "consolidation": {"mu": 0.0, "vol": 0.12, "alpha": 0.05, "beta": 0.90, "jump_prob": 0.005, "jump_mu": 0.0},
}

# Bar-boundary regime transition probabilities: rows are the current state, entries the next state.
REGIME_TRANSITIONS: dict[str, list[tuple[str, float]]] = {
    "bull": [("bull", 0.92), ("consolidation", 0.06), ("bear", 0.02)],
    "bear": [("bear", 0.85), ("consolidation", 0.12), ("bull", 0.03)],
    "consolidation": [("consolidation", 0.90), ("bull", 0.06), ("bear", 0.04)],
}
REGIME_JUMP_SD = 0.02


@dataclass(frozen=True)
class Bar:
    index: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    regime: str = "normal"

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "open": round(self.open, 4),
            "high": round(self.high, 4),
            "low": round(self.low, 4),
            "close": round(self.close, 4),
            "volume": round(self.volume, 2),
            "regime": self.regime,
        }


class SyntheticMarketGenerator:
    """Generates deterministic synthetic financial price series with stylized facts."""

    def __init__(self, seed: int = 42, version: int = GENERATOR_VERSION):
        self.seed = seed
        self.version = version
        self.rng = random.Random(seed)

    def reseed(self, seed: int) -> None:
        self.seed = seed
        self.rng = random.Random(seed)

    def generate_gbm(
        self,
        s0: float = 100.0,
        mu: float = 0.05,
        sigma: float = 0.20,
        n_steps: int = 252,
        dt: float = 1.0 / 252.0,
    ) -> list[float]:
        """Classic Geometric Brownian Motion: dS = mu*S*dt + sigma*S*dW."""
        prices = [s0]
        drift = (mu - 0.5 * sigma**2) * dt
        vol_step = sigma * math.sqrt(dt)

        for _ in range(n_steps):
            z = self.rng.gauss(0.0, 1.0)
            ret = drift + vol_step * z
            prices.append(prices[-1] * math.exp(ret))

        return prices

    def generate_ar1_mean_reversion(
        self,
        s0: float = 100.0,
        theta: float = 100.0,
        kappa: float = 2.0,
        sigma: float = 0.15,
        n_steps: int = 252,
        dt: float = 1.0 / 252.0,
    ) -> list[float]:
        """Ornstein-Uhlenbeck process in log price: d(ln S) = kappa*(ln theta - ln S)*dt + sigma*dW."""
        log_theta = math.log(theta)
        log_p = math.log(s0)
        prices = [s0]
        vol_step = sigma * math.sqrt(dt)

        for _ in range(n_steps):
            z = self.rng.gauss(0.0, 1.0)
            d_log_p = kappa * (log_theta - log_p) * dt + vol_step * z
            log_p += d_log_p
            prices.append(math.exp(log_p))

        return prices

    def generate_garch(
        self,
        s0: float = 100.0,
        omega: float = 0.000002,
        alpha: float = 0.08,
        beta: float = 0.90,
        n_steps: int = 252,
    ) -> list[float]:
        """GARCH(1,1) log returns: h_t = omega + alpha * eps_{t-1}^2 + beta * h_{t-1}, per-step variance units.

        Starts at the stationary variance omega / (1 - alpha - beta), which requires alpha + beta < 1.
        """
        if omega <= 0.0 or alpha < 0.0 or beta < 0.0 or alpha + beta >= 1.0:
            raise ValueError(f"GARCH(1,1) needs omega > 0, alpha, beta >= 0 and alpha + beta < 1, got {omega}, {alpha}, {beta}")
        variance = omega / (1.0 - alpha - beta)
        prices = [s0]
        for _ in range(n_steps):
            eps = math.sqrt(variance) * self.rng.gauss(0.0, 1.0)
            prices.append(prices[-1] * math.exp(eps))
            variance = omega + alpha * eps**2 + beta * variance
        return prices

    def generate_regime_path(
        self,
        s0: float = 100.0,
        n_bars: int = 200,
        sub_steps: int = 10,
        dt: float = 1.0 / 252.0,
    ) -> list[Bar]:
        """Multi-regime market generator with GARCH volatility, jumps, and intrabar sub-steps."""
        regimes = REGIME_PARAMS

        current_regime = "bull"
        current_price = s0
        bars: list[Bar] = []
        sub_dt = dt / sub_steps
        current_variance = 0.04 * sub_dt  # (20% annualized)^2 per sub-step

        for bar_idx in range(n_bars):
            # Transition state at bar boundary
            roll = self.rng.random()
            cum_p = 0.0
            for next_state, prob in REGIME_TRANSITIONS[current_regime]:
                cum_p += prob
                if roll <= cum_p:
                    current_regime = next_state
                    break

            r_params = regimes[current_regime]
            omega = r_params["vol"] ** 2 * sub_dt * (1.0 - r_params["alpha"] - r_params["beta"])
            bar_open = current_price
            bar_high = current_price
            bar_low = current_price
            bar_volume = 1000.0 * (1.0 + self.rng.random() * 0.5)

            for _ in range(sub_steps):
                # GARCH update for sub-step variance
                z = self.rng.gauss(0.0, 1.0)
                sub_vol = math.sqrt(max(1e-8, current_variance))
                ret = (r_params["mu"] * sub_dt) + (sub_vol * z)

                # Merton jump
                if self.rng.random() < r_params["jump_prob"] / sub_steps:
                    jump = self.rng.gauss(r_params["jump_mu"], REGIME_JUMP_SD)
                    ret += jump
                    bar_volume += 5000.0  # volume spike on jumps

                # Update GARCH variance
                resid_sq = (sub_vol * z) ** 2
                current_variance = omega + r_params["alpha"] * resid_sq + r_params["beta"] * current_variance

                current_price *= math.exp(ret)
                if current_price > bar_high:
                    bar_high = current_price
                if current_price < bar_low:
                    bar_low = current_price

            bar_close = current_price
            abs_ret = abs((bar_close - bar_open) / bar_open)
            bar_volume += abs_ret * 50000.0

            bars.append(
                Bar(
                    index=bar_idx,
                    open=bar_open,
                    high=bar_high,
                    low=bar_low,
                    close=bar_close,
                    volume=bar_volume,
                    regime=current_regime,
                )
            )

        return bars

    def oracle_probability_higher(
        self,
        current_price: float,
        horizon_steps: int = 5,
        mu: float = 0.05,
        sigma: float = 0.20,
        dt: float = 1.0 / 252.0,
    ) -> float:
        """Analytic Oracle probability under GBM: P(S_{t+h} > S_t) = N( drift / total_vol )."""
        total_dt = horizon_steps * dt
        drift = (mu - 0.5 * sigma**2) * total_dt
        total_vol = sigma * math.sqrt(total_dt)
        if total_vol <= 0:
            return 1.0 if drift > 0 else 0.5

        # Normal CDF using erf
        d = drift / total_vol
        return 0.5 * (1.0 + math.erf(d / math.sqrt(2.0)))
