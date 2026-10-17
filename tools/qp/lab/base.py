"""Base classes and analytics helpers for Trading Lab engines.

Standard-library only. Provides parameter schemas, performance metric calculators
(Sharpe, Sortino, Max Drawdown, Win Rate, Profit Factor, Expectancy), and TOON output.
"""

from __future__ import annotations

import json
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Param:
    name: str
    param_type: str  # "float", "int", "str", "bool"
    default: Any
    description: str
    min_val: float | None = None
    max_val: float | None = None
    choices: list[Any] | None = None

    def cast(self, raw_val: Any) -> Any:
        if raw_val is None:
            return self.default
        if self.param_type == "int":
            val = int(raw_val)
            if self.min_val is not None and val < self.min_val:
                raise ValueError(f"Param '{self.name}' must be >= {self.min_val}, got {val}")
            if self.max_val is not None and val > self.max_val:
                raise ValueError(f"Param '{self.name}' must be <= {self.max_val}, got {val}")
            return val
        if self.param_type == "float":
            val = float(raw_val)
            if self.min_val is not None and val < self.min_val:
                raise ValueError(f"Param '{self.name}' must be >= {self.min_val}, got {val}")
            if self.max_val is not None and val > self.max_val:
                raise ValueError(f"Param '{self.name}' must be <= {self.max_val}, got {val}")
            return val
        if self.param_type == "bool":
            if isinstance(raw_val, bool):
                return raw_val
            return str(raw_val).lower() in ("true", "1", "yes")
        if self.param_type == "str":
            val = str(raw_val)
            if self.choices and val not in self.choices:
                raise ValueError(f"Param '{self.name}' must be one of {self.choices}, got {val!r}")
            return val
        return raw_val


@dataclass
class LabResult:
    engine_id: str
    metrics: dict[str, float | int | str]
    data: dict[str, Any] = field(default_factory=dict)
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "engine_id": self.engine_id,
            "metrics": self.metrics,
            "summary": self.summary,
            "data": self.data,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def to_toon(self) -> str:
        lines = [f"engine: {self.engine_id}"]
        if self.summary:
            lines.append(f"summary: {self.summary}")
        lines.append(f"metrics[{len(self.metrics)}]{{metric,value}}:")
        for k, v in sorted(self.metrics.items()):
            lines.append(f"  {k},{v}")
        return "\n".join(lines)


class TradingLabEngine(ABC):
    """Abstract base class for all Trading Lab engines."""

    @property
    @abstractmethod
    def engine_id(self) -> str:
        """Unique snake_case engine identifier, e.g. 'lob_sim'."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human readable title."""

    @property
    @abstractmethod
    def description(self) -> str:
        """One-line concise summary of what this engine models."""

    @property
    @abstractmethod
    def asset_class(self) -> str:
        """Primary asset class or domain."""

    @property
    @abstractmethod
    def params(self) -> dict[str, Param]:
        """Dictionary of configurable parameters."""

    def validate_params(self, raw_kwargs: dict[str, Any]) -> dict[str, Any]:
        out = {}
        for p_name, param in self.params.items():
            if p_name in raw_kwargs:
                out[p_name] = param.cast(raw_kwargs[p_name])
            else:
                out[p_name] = param.default
        return out

    @abstractmethod
    def run(self, **kwargs) -> LabResult:
        """Execute the simulation or analytics model."""

    # --- Common performance calculation utilities (stdlib pure-python) ---

    @staticmethod
    def calculate_returns_metrics(equity_curve: list[float], risk_free_rate: float = 0.0, periods_per_year: int = 252) -> dict[str, float]:
        """Compute CAGR, Sharpe, Sortino, Max Drawdown, and Calmar ratio from an equity curve."""
        if len(equity_curve) < 2 or equity_curve[0] <= 0:
            return {
                "cagr": 0.0,
                "sharpe": 0.0,
                "sortino": 0.0,
                "max_drawdown": 0.0,
                "calmar": 0.0,
            }

        returns = []
        for i in range(1, len(equity_curve)):
            prev = equity_curve[i - 1]
            curr = equity_curve[i]
            returns.append((curr - prev) / prev if prev > 0 else 0.0)

        n_periods = len(returns)
        years = n_periods / periods_per_year
        final_equity = equity_curve[-1]
        start_equity = equity_curve[0]

        cagr = (final_equity / start_equity) ** (1.0 / years) - 1.0 if years > 0 and final_equity > 0 else 0.0

        # Mean and standard deviation
        mean_r = sum(returns) / n_periods
        var_r = sum((r - mean_r) ** 2 for r in returns) / (n_periods - 1) if n_periods > 1 else 0.0
        std_r = math.sqrt(var_r)

        ann_mean = mean_r * periods_per_year
        ann_std = std_r * math.sqrt(periods_per_year)
        sharpe = (ann_mean - risk_free_rate) / ann_std if ann_std > 0 else 0.0

        # Downside deviation for Sortino
        downside_returns = [min(0.0, r) for r in returns]
        downside_var = sum(r**2 for r in downside_returns) / n_periods
        downside_std = math.sqrt(downside_var) * math.sqrt(periods_per_year)
        sortino = (ann_mean - risk_free_rate) / downside_std if downside_std > 0 else 0.0

        # Maximum Drawdown
        peak = equity_curve[0]
        max_dd = 0.0
        for val in equity_curve:
            if val > peak:
                peak = val
            dd = (peak - val) / peak if peak > 0 else 0.0
            if dd > max_dd:
                max_dd = dd

        calmar = cagr / max_dd if max_dd > 0 else 0.0

        return {
            "cagr": round(cagr, 4),
            "sharpe": round(sharpe, 4),
            "sortino": round(sortino, 4),
            "max_drawdown": round(max_dd, 4),
            "calmar": round(calmar, 4),
        }

    @staticmethod
    def calculate_trade_metrics(trades_pnl: list[float]) -> dict[str, float | int]:
        """Compute win rate, profit factor, average win/loss, and trade expectancy."""
        if not trades_pnl:
            return {
                "total_trades": 0,
                "win_rate": 0.0,
                "profit_factor": 0.0,
                "expectancy": 0.0,
                "avg_win": 0.0,
                "avg_loss": 0.0,
            }

        wins = [p for p in trades_pnl if p > 0]
        losses = [p for p in trades_pnl if p < 0]
        n_total = len(trades_pnl)
        n_wins = len(wins)
        n_losses = len(losses)

        win_rate = n_wins / n_total if n_total > 0 else 0.0
        sum_gains = sum(wins)
        sum_losses = abs(sum(losses))
        profit_factor = sum_gains / sum_losses if sum_losses > 0 else (99.0 if sum_gains > 0 else 0.0)

        avg_win = sum_gains / n_wins if n_wins > 0 else 0.0
        avg_loss = sum(losses) / n_losses if n_losses > 0 else 0.0
        expectancy = (win_rate * avg_win) + ((1.0 - win_rate) * avg_loss)

        return {
            "total_trades": n_total,
            "win_rate": round(win_rate, 4),
            "profit_factor": round(profit_factor, 4),
            "expectancy": round(expectancy, 4),
            "avg_win": round(avg_win, 4),
            "avg_loss": round(avg_loss, 4),
        }
