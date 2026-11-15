"""Trading intuition and judgement: every number in the note.

Backs every number in `11-Risk-and-Trading/09-Trading-Intuition-and-Judgement.md`.
Independent routes used here:
- win-rate significance from the exact binomial tail with fractions, beside the normal approximation;
- normal quantiles and tails by bisection on erfc, never recalled;
- the expected best of 100 zero-skill Sharpe ratios by numerical integration of n x Phi^(n-1) phi, cross-checked by
  seeded simulation;
- the Bayes update by exact fractions and by seeded simulation of thesis and price-move draws;
- the Kelly fraction by numerically maximising expected log growth, and the losing streak by exact fractions.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 11-Risk-and-Trading/code/risk_09_trading_judgement.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261114


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol})")


def norm_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def norm_ppf(p: float) -> float:
    lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def binom_upper_tail(n: int, k: int) -> Fraction:
    """P(X >= k) for X ~ Bin(n, 1/2), exactly."""
    return Fraction(sum(math.comb(n, j) for j in range(k, n + 1)), 2**n)


# ------------------------------------------------------------------ sections


def index_inclusion() -> None:
    print("Example 1: index-inclusion sizing, hypothetical inputs (card risk-judgement-inclusion-sharpe)")
    sd = 0.015 * math.sqrt(5)
    approx("five-day idiosyncratic sd (percent)", 100 * sd, 3.4, 1)
    approx("expected Sharpe of the trade", 0.02 / sd, 0.6, 1)


def win_rate() -> None:
    print("Example 2: is a 55% win rate skill (cards risk-judgement-win-rate, risk-judgement-win-rate-exact)")
    se = math.sqrt(0.25 / 100)
    approx("standard error of the win rate, n = 100", se, 0.05, 12)
    approx("z for 55 of 100", 0.05 / se, 1.0, 12)
    approx("one-sided normal p-value", 1 - norm_cdf(1.0), 0.16, 2)
    tail = binom_upper_tail(100, 55)
    approx("exact binomial P(X >= 55 | n = 100, p = 1/2)", float(tail), 0.184, 3)
    approx("normal with continuity correction, z = 0.9", 1 - norm_cdf(4.5 / 5), 0.184, 3)
    z1000 = 0.05 / math.sqrt(0.25 / 1000)
    approx("z for 550 of 1,000", z1000, 3.2, 1)
    tail1000 = binom_upper_tail(1000, 550)
    approx("exact binomial P(X >= 550 | n = 1000) (percent)", float(100 * tail1000), 0.09, 2)
    exact("EV of 40% wins at 3 to 1, per unit risked", Fraction(2, 5) * 3 - Fraction(3, 5), Fraction(3, 5))
    exact("break-even win rate at 3 to 1", Fraction(1, 1 + 3), Fraction(1, 4))


def sharpe_years() -> None:
    print("Example 3: years of data for a t-statistic of 1.96 (TL;DR, card risk-judgement-sharpe-years)")
    z = norm_ppf(0.975)
    approx("z_0.975", z, 1.96, 2)
    for s, years, decimals in [(0.5, 15.4, 1), (1.0, 3.8, 1), (2.0, 1.0, 1)]:
        approx(f"years for t = 1.96 at Sharpe {s}", (z / s) ** 2, years, decimals)
    approx("years for t = 2 at Sharpe 1", (2.0 / 1.0) ** 2, 4.0, 12)
    approx("card: Sharpe 0.5 needs about 15 years", (z / 0.5) ** 2, 15.0, 0)


def best_of_many(rng: np.random.Generator) -> None:
    print("Example 4: the best of 100 lucky traders (card risk-judgement-best-of-many)")
    p2 = 1 - norm_cdf(2.0)
    approx("P(Z > 2) (percent)", 100 * p2, 2.3, 1)
    approx("P(Z > 2) to five decimals", p2, 0.02275, 5)
    approx("P(at least one of 100 above 2) (percent)", 100 * (1 - (1 - p2) ** 100), 90, 0)
    # E[max of 100 standard normals] = int x * 100 Phi(x)^99 phi(x) dx by Simpson on [-10, 10]
    n_grid = 20_000
    x = np.linspace(-10.0, 10.0, n_grid + 1)
    phi = np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
    cdf = np.array([norm_cdf(v) for v in x])
    y = x * 100 * cdf**99 * phi
    h = 20.0 / n_grid
    e_max = float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))
    approx("expected best Sharpe, numerical integration", e_max, 2.51, 2)
    draws = rng.standard_normal((200_000, 100)).max(axis=1)
    se = float(draws.std(ddof=1) / math.sqrt(len(draws)))
    simulated("expected best Sharpe, simulated", float(draws.mean()), 2.51, 5 * se + 0.005)
    simulated("P(best above 2), simulated", float((draws > 2).mean()), 0.90, 5 * math.sqrt(0.09 / len(draws)) + 0.005)


def bayes(rng: np.random.Generator) -> None:
    print("Example 5: updating on an adverse move (card risk-judgement-adverse-move)")
    post = Fraction(6, 10) * Fraction(3, 10) / (Fraction(6, 10) * Fraction(3, 10) + Fraction(4, 10) * Fraction(6, 10))
    exact("posterior", post, Fraction(3, 7))
    num = Fraction(6, 10) * Fraction(3, 10)
    den = num + Fraction(4, 10) * Fraction(6, 10)
    exact("numerator and denominator", (num, den), (Fraction(18, 100), Fraction(42, 100)))
    approx("posterior", float(post), 0.43, 2)
    n = 2_000_000
    thesis = rng.random(n) < 0.6
    drop = np.where(thesis, rng.random(n) < 0.3, rng.random(n) < 0.6)
    est = float(thesis[drop].mean())
    simulated("posterior, simulated", est, 0.43, 5 * math.sqrt(0.25 / drop.sum()) + 0.005)


def asymmetric() -> None:
    print("Example 6: sizing an asymmetric trade (cards risk-judgement-asymmetric, risk-judgement-losing-streak)")
    exact("EV per unit risked", Fraction(2, 5) * 3 - Fraction(3, 5), Fraction(3, 5))
    g = lambda f: 0.4 * math.log1p(3 * f) + 0.6 * math.log1p(-f)  # noqa: E731
    lo, hi = 0.0, 0.99
    for _ in range(200):
        a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if g(a) < g(b):
            lo = a
        else:
            hi = b
    approx("Kelly fraction by numerical maximisation", (lo + hi) / 2, 0.2, 6)
    approx("half Kelly", (lo + hi) / 4, 0.1, 6)
    streak = Fraction(3, 5) ** 6
    exact("P(six losses in a row)", streak, Fraction(729, 15625))
    approx("P(six losses in a row) (percent)", float(100 * streak), 4.7, 1)
    approx("loss after six straight losses at 10% of current capital (percent)", 100 * (1 - 0.9**6), 47, 0)
    approx("2 / 3.354", 2 / 3.354, 0.6, 1)


def main() -> None:
    rng = np.random.default_rng(SEED)
    index_inclusion()
    win_rate()
    sharpe_years()
    best_of_many(rng)
    bayes(rng)
    asymmetric()
    print("All trading-judgement numbers check.")


if __name__ == "__main__":
    main()
