"""Execution slippage and cost models: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/60-Systems/06-Execution-Slippage-and-Cost-Models.md`.
Independent routes used here:
- implementation shortfall by summing its components in exact decimal arithmetic and, separately, as the
  difference between the paper portfolio's and the real portfolio's value at the end price (Perold 1988);
- square-root impact by direct evaluation, and its scaling claims as ratios of evaluated impacts;
- the Almgren-Chriss trajectory by solving the discrete mean-variance problem as a linear system,
  compared with the closed-form sinh trajectory;
- strategy capacity by a fine grid search over AUM, compared with the closed forms.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 16-Trading-and-Investing/code/mkt_sys_06_execution.py`.
"""

from __future__ import annotations

import math
from decimal import Decimal

import numpy as np


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def shortfall() -> None:
    print("Example 1: implementation shortfall (cards mkt-sys-161, mkt-sys-162)")
    d = Decimal
    p_dec, p_arr, p_end, fees = d("100.00"), d("100.20"), d("101.00"), d("40.00")
    fills = [(4000, d("100.35")), (4000, d("100.55"))]
    order = 10000
    filled = sum(q for q, _ in fills)
    unfilled = order - filled
    exact("executed shares", filled, 8000)
    exact("unexecuted shares", unfilled, 2000)
    exec_cost = sum(q * (p - p_dec) for q, p in fills)
    exact("fill 1 cost", 4000 * (d("100.35") - p_dec), d("1400.00"))
    exact("fill 2 cost", 4000 * (d("100.55") - p_dec), d("2200.00"))
    exact("execution cost", exec_cost, d("3600.00"))
    delay = filled * (p_arr - p_dec)
    impact = sum(q * (p - p_arr) for q, p in fills)
    exact("delay cost 8000 x 0.20", delay, d("1600.00"))
    exact("spread and impact after arrival", impact, d("2000.00"))
    opp = unfilled * (p_end - p_dec)
    exact("opportunity cost", opp, d("2000.00"))
    is_total = exec_cost + opp + fees
    exact("implementation shortfall", is_total, d("5640.00"))
    # Independent route: paper portfolio (all 10,000 at the decision price) minus real portfolio, both marked at P_T.
    paper = order * (p_end - p_dec)
    real = sum(q * (p_end - p) for q, p in fills) - fees
    exact("paper gain minus real gain", paper - real, d("5640.00"))
    exact("IS in bps of 1,000,000", is_total / (order * p_dec) * 10000, d("56.4"))


def sqrt_impact() -> None:
    print("Example 2 and Core concepts 3: square-root impact (cards mkt-sys-164, mkt-sys-262)")
    sigma_d = 0.30 / math.sqrt(252)
    approx("daily volatility", sigma_d, 0.01890, 5)
    part = 100_000 / 2_000_000
    approx("participation Q/V", part, 0.05, 2)
    approx("sqrt(0.05)", math.sqrt(part), 0.2236, 4)
    approx("daily volatility (percent)", 100 * sigma_d, 1.89, 2)
    approx("Y x sigma_daily", 0.60 * sigma_d, 0.011339, 6)
    impact = 0.60 * sigma_d * math.sqrt(part)
    approx("impact (fraction, five significant figures)", impact, 0.0025355, 7)
    approx("impact (fraction)", impact, 0.002535, 6)
    approx("impact (bps)", impact * 1e4, 25.35, 2)
    approx("impact (bps, one decimal)", impact * 1e4, 25.4, 1)
    approx("notional", 100_000 * 50.0, 5_000_000, 0)
    approx("impact cost (dollars)", 5_000_000 * impact, 12_677, 0)

    def per_share(q_over_v: float) -> float:
        return 0.60 * sigma_d * math.sqrt(q_over_v)

    approx("per-share impact ratio, 1% vs 0.01% of ADV", per_share(0.01) / per_share(0.0001), 10.0, 9)
    approx("dollar impact ratio, 1% vs 0.01% of ADV", 0.01 * per_share(0.01) / (0.0001 * per_share(0.0001)), 1000.0, 6)
    approx("Y = 1, Q/V = 1%: impact in units of daily volatility", 1.0 * math.sqrt(0.01), 0.1, 9)


def almgren_chriss() -> None:
    print("Example 3: Almgren-Chriss trajectory (cards mkt-sys-167, mkt-sys-263)")
    x0, days, n = 1_000_000.0, 5.0, 5
    sigma, eta, gamma, lam = 0.95, 2.5e-6, 2.5e-7, 1e-6
    tau = days / n
    eta_t = eta - 0.5 * gamma * tau
    approx("eta tilde = eta - gamma tau / 2", eta_t, 2.375e-6, 9)
    kappa_t2 = lam * sigma**2 / eta_t
    approx("kappa tilde squared", kappa_t2, 0.3800, 4)
    kappa = math.acosh(1 + 0.5 * kappa_t2 * tau**2) / tau
    approx("kappa (per day)", kappa, 0.6071, 4)
    closed = [x0 * math.sinh(kappa * (days - j * tau)) / math.sinh(kappa * days) for j in range(n + 1)]
    # Independent route: minimise (eta_t/tau) sum (x_{k-1}-x_k)^2 + lam sigma^2 tau sum x_k^2 over x_1..x_{n-1}.
    a = np.zeros((n - 1, n - 1))
    b = np.zeros(n - 1)
    diag = 2 * eta_t / tau + lam * sigma**2 * tau
    for i in range(n - 1):
        a[i, i] = diag
        if i > 0:
            a[i, i - 1] = -eta_t / tau
        if i < n - 2:
            a[i, i + 1] = -eta_t / tau
    b[0] = eta_t / tau * x0
    solved = np.linalg.solve(a, b)
    assert np.allclose(solved, closed[1:n], rtol=1e-10), (solved, closed)
    quoted = [100.0, 54.2, 29.0, 14.8, 6.2, 0.0]
    for j, q in enumerate(quoted):
        approx(f"holdings at end of day {j} (percent)", 100 * closed[j] / x0, q, 1)
    approx("sold on day 1 (percent)", 100 * (1 - closed[1] / x0), 45.8, 1)
    approx("TWAP would sell per day (percent)", 100 / n, 20.0, 1)
    # Risk neutrality: with lam = 0 the linear system gives the straight line (TWAP).
    diag0 = 2 * eta_t / tau
    a0 = a.copy()
    np.fill_diagonal(a0, diag0)
    assert np.allclose(np.linalg.solve(a0, b), [x0 * (1 - (j + 1) / n) for j in range(n - 1)])
    print("    lambda = 0 gives the straight-line (TWAP) schedule")


def capacity() -> None:
    print("Example 4: capacity under square-root costs (cards mkt-sys-173, mkt-sys-174, mkt-sys-264)")
    alpha0 = 0.04
    k = 0.01 / math.sqrt(100e6)  # cost drag of 1% a year at $100M
    approx("k = 1% / sqrt(100M)", k * 1e6, 1.0, 9)
    a_zero = (alpha0 / k) ** 2
    a_hurdle = ((alpha0 - 0.02) / k) ** 2
    a_profit = (alpha0 / (1.5 * k)) ** 2
    grid = np.linspace(1e6, 3e9, 2_999_001)
    net = alpha0 - k * np.sqrt(grid)
    dollars = grid * net
    approx("zero-net-return AUM ($bn)", a_zero / 1e9, 1.6, 6)
    approx("grid: first AUM with net <= 0 ($bn)", grid[np.argmax(net <= 0)] / 1e9, 1.6, 3)
    approx("AUM where net return falls to 2% ($M)", a_hurdle / 1e6, 400, 6)
    approx("grid: first AUM with net <= 2% ($M)", grid[np.argmax(net <= 0.02)] / 1e6, 400, 0)
    approx("dollar-profit-maximising AUM ($M)", a_profit / 1e6, 711, 0)
    approx("grid: argmax of net dollar profit ($M)", grid[np.argmax(dollars)] / 1e6, 711, 0)
    approx("ratio to zero-return capacity", a_profit / a_zero, 4 / 9, 12)
    approx("net return at the profit maximum (percent)", 100 * (alpha0 - k * math.sqrt(a_profit)), 1.33, 2)
    approx("max net profit ($M per year)", a_profit * (alpha0 - k * math.sqrt(a_profit)) / 1e6, 9.48, 2)


if __name__ == "__main__":
    shortfall()
    sqrt_impact()
    almgren_chriss()
    capacity()
    print("all execution-cost numbers check out")
