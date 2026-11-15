"""Order types and algorithmic execution: every number in 08-Execution-Microstructure/01-Order-Types-and-Algorithmic-Execution.md.

Independent routes used here:
- implementation shortfall is computed component by component and, separately, from the direct cash formula
  (filled cost plus unfilled shares marked at the final price minus the paper cost); the two must agree to the cent;
- the Almgren-Chriss discrete-time optimal schedule is found by solving the first-order conditions of the
  mean-variance objective as a linear system, and compared with the closed-form hyperbolic-sine trajectory;
  with zero risk aversion the same solver must return the straight-line (TWAP) schedule;
- the square-root-law scaling factors are computed from the impact formula at two order sizes.
Run: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_exec_01_execution.py
"""

from __future__ import annotations

import math

import numpy as np
from mkt_assets_lib import close, q


def implementation_shortfall() -> None:
    print("Example 1: implementation shortfall of a 10,000-share buy")
    Q, Pd, P0, fill_q, fill_px, Pn, fees = 10_000, 100.00, 100.20, 8_000, 100.80, 101.50, 160.00
    delay = Q * (P0 - Pd)
    impact = fill_q * (fill_px - P0)
    opportunity = (Q - fill_q) * (Pn - P0)
    total = delay + impact + opportunity + fees
    q("delay cost", delay, "2,000.00")
    q("realized impact", impact, "4,800.00")
    q("opportunity cost", opportunity, "2,600.00")
    q("total implementation shortfall", total, "9,560.00")
    direct = fill_q * fill_px + (Q - fill_q) * Pn - Q * Pd + fees
    q("filled cost", fill_q * fill_px, "806,400")
    q("unfilled marked at close", (Q - fill_q) * Pn, "203,000")
    close("component sum vs direct cash formula", total, direct, 1e-6)
    q("shortfall in basis points of the paper notional", 1e4 * total / (Q * Pd), "95.6")


def almgren_chriss() -> None:
    print("Almgren-Chriss: the optimal discrete schedule is a hyperbolic sine; with lambda = 0 it is a straight line")
    X, T, N = 1_000_000.0, 1.0, 20
    tau = T / N
    sigma, eta, gamma = 0.95, 2.5e-6, 2.5e-7  # hypothetical inputs ($/share/sqrt(day), temporary and permanent impact)
    eta_t = eta - 0.5 * gamma * tau

    def solve(lam: float) -> np.ndarray:
        # objective in the interior holdings x_1..x_{N-1}: (eta_t / tau) sum (x_{k-1} - x_k)^2 + lam sigma^2 tau sum x_k^2
        m = N - 1
        a = np.zeros((m, m))
        b = np.zeros(m)
        for i in range(m):
            a[i, i] = 2 * eta_t / tau * 2 + 2 * lam * sigma**2 * tau
            if i > 0:
                a[i, i - 1] = -2 * eta_t / tau
            if i < m - 1:
                a[i, i + 1] = -2 * eta_t / tau
        b[0] = 2 * eta_t / tau * X  # x_0 = X; x_N = 0
        return np.concatenate([[X], np.linalg.solve(a, b), [0.0]])

    twap = solve(0.0)
    close("lambda = 0 solution vs straight line (max abs, shares)", float(np.max(np.abs(twap - X * (1 - np.arange(N + 1) / N)))), 0.0, 1e-6)
    lam = 2e-6
    x = solve(lam)
    kappa = math.acosh(1 + 0.5 * lam * sigma**2 * tau**2 / eta_t) / tau
    t = np.arange(N + 1) * tau
    closed = X * np.sinh(kappa * (T - t)) / math.sinh(kappa * T)
    close("lambda > 0 solution vs X sinh(kappa (T - t)) / sinh(kappa T) (max abs, shares)", float(np.max(np.abs(x - closed))), 0.0, 1e-4)
    assert x[1] < twap[1], "a risk-averse trader sells more in the first interval than TWAP"


def square_root_law() -> None:
    print("Square-root law scaling")

    def impact(Qv: float, Y: float = 1.0, sig: float = 0.02) -> float:
        return Y * sig * math.sqrt(Qv)

    q("impact ratio when order size doubles", impact(0.02) / impact(0.01), "1.414")
    q("impact ratio when order size quadruples", impact(0.04) / impact(0.01), "2")


if __name__ == "__main__":
    implementation_shortfall()
    almgren_chriss()
    square_root_law()
    print("all execution numbers verified")
