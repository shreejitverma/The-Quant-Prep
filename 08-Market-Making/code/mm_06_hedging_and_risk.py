"""Hedging and risk for market makers: every number in `08-Market-Making/06-Hedging-and-Risk-for-Market-Makers.md`.

Independent routes used here:
- the minimum-variance hedge ratio by a grid search over the hedged variance, and by least squares on
  seeded simulated correlated returns (tolerance three standard errors), never by the closed form alone;
- the break-even waiting time by bisection on the cost difference;
- normal quantiles and tail probabilities by Simpson quadrature of the normal density with bisection,
  not by the error function;
- the short-gamma rehedge by repricing a linear delta, the VaR limit by brute force over integer positions.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 08-Market-Making/code/mm_06_hedging_and_risk.py`.
"""

from __future__ import annotations

import math

import numpy as np

SEED = 20261114


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, expected {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.5f} (expected {expected}, tolerance {tol:.5f})")


def lower_tail(z: float, n: int = 200_000) -> float:
    """P(Z < z) for z < 0 by composite Simpson on [-40, z] of the normal density."""
    x = np.linspace(-40.0, z, n + 1)
    w = np.ones_like(x)
    w[1:-1:2], w[2:-1:2] = 4.0, 2.0
    return float(np.sum(w * np.exp(-0.5 * x * x))) * (x[1] - x[0]) / 3.0 / math.sqrt(2.0 * math.pi)


def quantile_upper(p: float) -> float:
    """z with P(Z > z) = p, by bisection on the quadrature tail."""
    lo, hi = 0.0, 10.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if lower_tail(-mid) > p else (lo, mid)
    return 0.5 * (lo + hi)


def min_variance(rng: np.random.Generator) -> None:
    print("Minimum-variance hedge (cards mm-hedge-min-variance-ratio, mm-hedge-rho-06-reduction, mm-hedge-rho-09-reduction)")
    for rho, lit in ((0.6, 20), (0.9, 56), (0.95, 69), (0.99, 86)):
        h = np.linspace(0.0, 1.0, 200_001)
        var = 1 - 2 * h * rho + h * h  # sigma_A = sigma_H = 1
        resid = math.sqrt(float(var.min()))
        approx(f"volatility removed at rho = {rho} (percent, grid search)", 100 * (1 - resid), lit, 0)
        if rho in (0.9, 0.99):
            approx(f"residual fraction at rho = {rho}", resid, {0.9: 0.436, 0.99: 0.141}[rho], 3)
    print("Example 1: hedging a stock with index futures (card mm-hedge-futures-example)")
    s_a, s_h, rho, n = 0.02, 0.01, 0.6, 400_000
    z1, z2 = rng.standard_normal(n), rng.standard_normal(n)
    hedge = s_h * z1
    stock = s_a * (rho * z1 + math.sqrt(1 - rho * rho) * z2)
    beta = float(np.dot(hedge - hedge.mean(), stock - stock.mean()) / np.dot(hedge - hedge.mean(), hedge - hedge.mean()))
    se_beta = math.sqrt(1 - rho * rho) * s_a / (s_h * math.sqrt(n))
    simulated("regression beta of stock on futures", beta, 1.2, 3 * se_beta)
    resid = stock - beta * hedge
    resid_sd = float(resid.std(ddof=1))
    simulated("residual daily sd", resid_sd, 0.016, 3 * resid_sd / math.sqrt(2 * n))
    notional = 1_000_000
    approx("futures to short (dollars), rho sigma_A / sigma_H x notional", rho * s_a / s_h * notional, 1_200_000, 0)
    approx("unhedged daily sd (dollars)", s_a * notional, 20_000, 0)
    approx("hedged daily sd (dollars)", s_a * math.sqrt(1 - rho * rho) * notional, 16_000, 0)


def bands() -> None:
    print("Whalley-Wilmott band (card mm-hedge-bandwidth-cost-doubling)")
    approx("band widening when costs double, 2^(1/3) - 1 (percent)", 100 * (2 ** (1 / 3) - 1), 26, 0)


def example2() -> None:
    print("Example 2: when to cross to hedge (cards mm-hedge-passive-vs-aggressive, mm-hedge-breakeven-wait)")
    n, gamma = 10_000, 0.001
    aggressive = n * (0.005 + 0.003)
    passive = n * (0.005 + 0.002 - 0.004)
    approx("aggressive cost", aggressive, 80, 0)
    approx("passive net edge", passive, 30, 0)
    approx("swing", aggressive + passive, 110, 0)
    for sigma in (0.00392, 40 * 0.015 / math.sqrt(23_400)):
        rate = 0.5 * gamma * n * n * sigma * sigma
        approx(f"risk cost per second (sigma = {sigma:.6f})", rate, 0.77, 2)
        lo, hi = 0.0, 10_000.0
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if rate * mid < aggressive + passive else (lo, mid)
        approx(f"break-even wait by bisection (sigma = {sigma:.6f})", lo, 143, 0)
    approx("shown working: 110 / 0.77 as in the card", 110 / 0.77, 143, 0)
    approx("risk cost ratio for a ten-times position", (0.5 * gamma * (10 * n) ** 2) / (0.5 * gamma * n**2), 100, 0)


def example3() -> None:
    print("Example 3: delta and gamma of a short call position (card mm-hedge-short-gamma-rehedge)")
    contracts, mult, delta0, gamma = -100, 100, 0.40, 0.05
    pos_delta = contracts * mult * delta0
    pos_gamma = contracts * mult * gamma
    approx("position delta", pos_delta, -4000, 0)
    approx("position gamma", pos_gamma, -500, 0)
    delta_after = contracts * mult * (delta0 + gamma * 2.0)  # option delta repriced after +2
    approx("position delta after +2", delta_after, -5000, 0)
    approx("extra shares to buy", -(delta_after - pos_delta), 1000, 0)


def example4() -> None:
    print("Example 4: a position limit from a VaR budget (card mm-hedge-var-position-limit)")
    z = quantile_upper(0.01)
    approx("z_0.99 by quadrature and bisection", z, 2.326, 3)
    sd = 50 * 0.02
    approx("one-day sd per share", sd, 1.0, 2)
    limit = max(q for q in range(0, 40_000) if q * z * sd <= 50_000)
    approx("maximum position (hundreds of shares)", limit / 100, 215, 0)
    approx("shown working: 50,000 / (2.326 x 1)", 50_000 / 2.326, 21_496, 0)


def example5() -> None:
    print("Example 5: calibrating a daily stop (cards mm-hedge-stop-calibration, mm-hedge-stop-3sd)")
    approx("(-40,000 - 20,000) / 15,000", (-40_000 - 20_000) / 15_000, -4, 6)
    p4 = lower_tail(-4.0)
    approx("P(Z < -4) x 1e5", p4 * 1e5, 3.2, 1)
    approx("years between breaches at 252 days", 1 / p4 / 252, 125, 0)
    approx("(-25,000 - 20,000) / 15,000", (-25_000 - 20_000) / 15_000, -3, 6)
    p3 = lower_tail(-3.0)
    approx("P(Z < -3) (percent)", 100 * p3, 0.135, 3)
    approx("trading days between breaches", 1 / p3, 741, 0)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    min_variance(rng)
    bands()
    example2()
    example3()
    example4()
    example5()
    print("all hedging and risk checks passed")
