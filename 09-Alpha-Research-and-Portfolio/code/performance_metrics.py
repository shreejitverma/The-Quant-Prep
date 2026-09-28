"""Strategy performance metrics with the conventions interviewers check.

- Sharpe: mean excess return over its standard deviation, annualised by sqrt(periods per year).
- Sortino: mean excess return over the downside deviation sqrt(mean(min(r - target, 0)^2)),
  averaged over *all* observations, not the standard deviation of the losing ones.
- Max drawdown: measured from running peaks of the price path including the starting price.
- Calmar: compound annual growth rate over the absolute max drawdown.
Degenerate inputs (zero variance, no downside, no drawdown) return NaN rather than a
misleading number.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class PerformanceMetrics:
    @staticmethod
    def calculate_returns(prices: pd.Series) -> pd.Series:
        """Simple returns r_t = P_t / P_{t-1} - 1."""
        return prices.pct_change().dropna()

    @staticmethod
    def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0, periods_per_year: int = 252) -> float:
        excess = returns - risk_free_rate / periods_per_year
        sd = excess.std(ddof=1)
        return float(np.sqrt(periods_per_year) * excess.mean() / sd) if sd > 0 else float("nan")

    @staticmethod
    def sortino_ratio(returns: pd.Series, target: float = 0.0, periods_per_year: int = 252) -> float:
        """``target`` is the per-period minimum acceptable return (0, or the per-period risk-free rate)."""
        excess = returns - target
        downside_dev = np.sqrt(np.mean(np.minimum(excess, 0.0) ** 2))
        return float(np.sqrt(periods_per_year) * excess.mean() / downside_dev) if downside_dev > 0 else float("nan")

    @staticmethod
    def max_drawdown(prices: pd.Series) -> float:
        """Most negative peak-to-trough move, as a fraction (for example -0.065)."""
        return float((prices / prices.cummax() - 1.0).min())

    @staticmethod
    def cagr(prices: pd.Series, periods_per_year: int = 252) -> float:
        periods = len(prices) - 1
        if periods <= 0:
            return float("nan")
        return float((prices.iloc[-1] / prices.iloc[0]) ** (periods_per_year / periods) - 1.0)

    @staticmethod
    def calmar_ratio(prices: pd.Series, periods_per_year: int = 252) -> float:
        mdd = abs(PerformanceMetrics.max_drawdown(prices))
        return PerformanceMetrics.cagr(prices, periods_per_year) / mdd if mdd > 0 else float("nan")


if __name__ == "__main__":
    prices = pd.Series([100, 102, 104, 103, 105, 108, 101, 103], name="Price", dtype=float)
    returns = PerformanceMetrics.calculate_returns(prices)
    print(f"Sharpe ratio:  {PerformanceMetrics.sharpe_ratio(returns):.4f}")
    print(f"Sortino ratio: {PerformanceMetrics.sortino_ratio(returns):.4f}")
    print(f"Max drawdown:  {PerformanceMetrics.max_drawdown(prices):.4f}")
    print(f"CAGR:          {PerformanceMetrics.cagr(prices):.4f}")
    print(f"Calmar ratio:  {PerformanceMetrics.calmar_ratio(prices):.4f}")
    assert abs(PerformanceMetrics.max_drawdown(pd.Series([100.0, 90.0, 95.0])) + 0.1) < 1e-12  # first-move drawdown counts
