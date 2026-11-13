"""Inequalities and limit theorems: every bound, tail and approximation in the note.

Backs every number in `01-Probability/06-Inequalities-and-Limit-Theorems.md`.
Independent routes used here:
- exact binomial and dice-sum tails come from integer arithmetic (exact binomial coefficients and an
  exact convolution of 100 dice), not from the normal approximation they are compared with;
- normal tails come from Simpson integration of the density, not from `math.erfc`;
- the distribution-free bounds are shown to be attained by explicit extremal distributions;
- the volatility standard error, volatility drag and Cauchy sample mean are reproduced by seeded simulation.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 01-Probability/code/prob_06_limits.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261019


def exact(label: str, value: Fraction | int, expected: Fraction | int) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-15
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def approx_sig(label: str, value: float, expected: float, sig: int) -> None:
    """Assert a small number to `sig` significant figures (for values like 3.9e-5)."""
    scale = 10 ** (math.floor(math.log10(abs(expected))) - sig + 1)
    assert abs(value - expected) <= 0.5 * scale * (1 + 1e-9), f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{sig - 1}e}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol})")


def upper_tail(z: float) -> float:
    """1 - Phi(z) for z >= 0 by composite Simpson integration of the density from z to z + 40."""
    n = 400_000
    x = np.linspace(z, z + 40.0, n + 1)
    y = np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
    h = 40.0 / n
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))


def binom_tail(n: int, p: Fraction, k: int) -> Fraction:
    """Exact P(Bin(n, p) >= k) with integer arithmetic."""
    num, den = p.numerator, p.denominator
    total = sum(math.comb(n, j) * num**j * (den - num) ** (n - j) for j in range(k, n + 1))
    return Fraction(total, den**n)


def bounds() -> None:
    print("Markov and Chebyshev (cards prob-limit-markov-bound, prob-limit-chebyshev-within-k-sd)")
    exact("Markov bound E[X]/a with mean 10, a = 50", Fraction(10, 50), Fraction(1, 5))
    two_point = {0: Fraction(4, 5), 50: Fraction(1, 5)}
    exact("two-point law on {0, 50}: mean", sum(x * p for x, p in two_point.items()), 10)
    exact("two-point law on {0, 50}: P(X >= 50) attains the bound", two_point[50], Fraction(1, 5))
    for k, quoted in ((2, Fraction(3, 4)), (3, Fraction(8, 9))):
        # three-point law on {-k, 0, k} with P(+-k) = 1/(2k^2) has variance 1 and puts exactly 1/k^2 at distance k
        law = {-k: Fraction(1, 2 * k * k), 0: 1 - Fraction(1, k * k), k: Fraction(1, 2 * k * k)}
        var = sum(x * x * p for x, p in law.items())
        assert var == 1
        exact(f"smallest mass within {k} sd (attained by the three-point law)", law[0], quoted)
    approx("8/9 in %", 100 * 8 / 9, 88.9, 1)
    approx("normal mass within 2 sd in %", 100 * (1 - 2 * upper_tail(2)), 95.4, 1)
    approx("normal mass within 3 sd in %", 100 * (1 - 2 * upper_tail(3)), 99.7, 1)


def normal_tails() -> None:
    print("Normal tails table, by Simpson integration of the density (TL;DR and table)")
    rows = [(1, 15.9, 31.7, "pct", 1), (2, 2.28, 4.55, "pct", 2), (3, 0.135, 0.27, "pct", 3)]
    for z, one, two, _, dp in rows:
        t = upper_tail(z)
        approx(f"{z} sigma one-sided in %", 100 * t, one, dp)
        approx(f"{z} sigma two-sided in %", 100 * 2 * t, two, 2 if z == 3 else dp)
    approx_sig("4 sigma one-sided", upper_tail(4), 3.2e-5, 2)
    approx_sig("4 sigma two-sided", 2 * upper_tail(4), 6.3e-5, 2)
    approx_sig("5 sigma one-sided", upper_tail(5), 2.9e-7, 2)
    approx_sig("5 sigma two-sided", 2 * upper_tail(5), 5.7e-7, 2)
    approx("1 sigma one-sided, TL;DR 'about 16%'", 100 * upper_tail(1), 16, 0)
    approx("2 sigma one-sided, TL;DR '2.3%'", 100 * upper_tail(2), 2.3, 1)
    approx("3 sigma one-sided, TL;DR '0.13%'", 100 * upper_tail(3), 0.13, 2)
    approx_sig("4 sigma one-sided, TL;DR '3e-5'", upper_tail(4), 3e-5, 1)


def coin_examples() -> None:
    print("Example 1 - 10,000 coin flips (card prob-limit-clt-coin-5100)")
    n = 10_000
    sd = math.sqrt(n / 4)
    approx("sd of heads", sd, 50, 9)
    approx("2 sigma tail in %", 100 * upper_tail(2), 2.3, 1)
    z = (5100 - 0.5 - n / 2) / sd
    approx("continuity-corrected z", z, 1.99, 2)
    approx("continuity-corrected tail in %", 100 * upper_tail(z), 2.33, 2)
    ex = binom_tail(n, Fraction(1, 2), 5100)
    approx("exact P(heads >= 5100)", float(ex), 0.0233, 4)

    print("Example 2 - comparing the bounds, 100 flips, >= 70 heads (card prob-limit-bounds-seventy-heads)")
    exact("Chebyshev two-sided bound 25/400", Fraction(25, 400), Fraction(1, 16))
    approx("Chebyshev bound", 25 / 400, 0.0625, 4)
    approx("Cantelli bound 25/425", 25 / 425, 0.059, 3)
    approx_sig("Hoeffding e^-8", math.exp(-2 * 20**2 / 100), 3.4e-4, 2)
    approx("CLT continuity-corrected z", 19.5 / 5, 3.9, 1)
    approx_sig("CLT continuity-corrected tail", upper_tail(3.9), 4.8e-5, 2)
    ex70 = float(binom_tail(100, Fraction(1, 2), 70))
    approx_sig("exact P(heads >= 70)", ex70, 3.9e-5, 2)
    approx("Chebyshev / exact: orders of magnitude", math.log10(0.0625 / ex70), 3, 0)
    approx("Hoeffding / exact: orders of magnitude", math.log10(math.exp(-8) / ex70), 1, 0)
    rng = np.random.default_rng(SEED)
    flips = rng.binomial(100, 0.5, 20_000_000)
    simulated("P(heads >= 70) in units of 1e-5, simulated", float((flips >= 70).mean()) * 1e5, 3.9, 0.6)

    print("Hoeffding's lemma and inequality (card prob-limit-hoeffding-statement)")
    for s in (0.1, 0.5, 1.0, 2.0, 4.0):
        mgf = 0.5 * (math.exp(s * 0.5) + math.exp(-s * 0.5))  # centred fair coin on {0,1}
        assert mgf <= math.exp(s * s / 8)
    print("    E[exp(s(X - 1/2))] <= exp(s^2/8) for a fair {0,1} coin at s = 0.1, 0.5, 1, 2, 4")
    for t in (5, 10, 15, 20):
        assert float(binom_tail(100, Fraction(1, 2), 50 + t)) <= math.exp(-2 * t * t / 100)
    print("    exact 100-flip tails sit below exp(-2t^2/n) for t = 5, 10, 15, 20")


def roulette_and_dice() -> None:
    print("Example 3 - roulette (card prob-limit-roulette-ahead)")
    p = Fraction(18, 38)
    n = 1000
    mean_bet = 2 * p - 1
    exact("mean per bet", mean_bet, Fraction(-1, 19))
    approx("expected total", float(n * mean_bet), -52.6, 1)
    approx("total sd", math.sqrt(n * (1 - float(mean_bet) ** 2)), 31.6, 1)
    z_total = float(n * mean_bet) / math.sqrt(n * (1 - float(mean_bet) ** 2))
    approx("z for being ahead", z_total, -1.67, 2)
    approx("normal P(S > 0) in %", 100 * upper_tail(-z_total), 4.8, 1)
    mw, sw = n * float(p), math.sqrt(n * float(p) * (1 - float(p)))
    approx("mean wins", mw, 473.7, 1)
    approx("sd wins", sw, 15.8, 1)
    z = (500.5 - mw) / sw
    approx("continuity-corrected z", z, 1.70, 2)
    approx("continuity-corrected P in %", 100 * upper_tail(z), 4.5, 1)
    ex = binom_tail(n, p, 501)
    approx("exact P(wins >= 501) in %", 100 * float(ex), 4.48, 2)

    print("100 dice over 400 (card prob-limit-hundred-dice-over-400)")
    dist = [1]  # counts of each total, exact integers
    for _ in range(100):
        new = [0] * (len(dist) + 6)
        for s, c in enumerate(dist):
            for f in range(1, 7):
                new[s + f] += c
        dist = new
    total = 6**100
    assert sum(dist) == total
    over = Fraction(sum(dist[401:]), total)
    approx("exact P(sum > 400) in %", 100 * float(over), 0.151, 3)
    sd = math.sqrt(100 * 35 / 12)
    approx("sd of the sum", sd, 17.1, 1)
    approx("continuity-corrected z", 50.5 / sd, 2.96, 2)
    approx("continuity-corrected tail in %", 100 * upper_tail(50.5 / sd), 0.16, 2)
    approx("continuity-corrected tail", upper_tail(50.5 / sd), 0.0016, 4)
    exact("mean of the sum of 100 dice", Fraction(sum(s * c for s, c in enumerate(dist)), total), 350)


def scaling_and_estimation() -> None:
    print("sqrt-time scaling and poll size (cards prob-limit-sqrt-time-vol, prob-limit-poll-sample-size)")
    approx("sqrt(252)", math.sqrt(252), 15.87, 2)
    approx("annualised vol in %", math.sqrt(252) * 1.0, 15.9, 1)
    rng = np.random.default_rng(SEED + 1)
    annual = rng.normal(0, 0.01, size=(50_000, 252)).sum(axis=1)
    simulated("sd of a 252-day sum of 1% daily moves, simulated, in %", 100 * float(annual.std()), 15.87, 0.3)
    n_req = (1.96 * 0.5 / 0.03) ** 2
    approx("required n before rounding", n_req, 1067.1, 1)
    exact("respondents (round up)", math.ceil(n_req), 1068)
    q975 = 1.96
    assert abs(upper_tail(q975) - 0.025) < 1e-4

    print("Example 4 - standard error of an estimated volatility (card prob-limit-delta-method-vol-se)")
    approx("1/sqrt(504) in %", 100 / math.sqrt(504), 4.5, 1)
    approx("one standard error on a 20% vol, in vol points", 20 / math.sqrt(504), 0.9, 1)
    r = rng.standard_normal((40_000, 252))
    sig_hat = r.std(axis=1, ddof=1)
    simulated("relative sd of sigma-hat, 252 normal returns, simulated", float(sig_hat.std() / sig_hat.mean()), 1 / math.sqrt(504), 0.002)

    print("Example 5 - volatility drag (card prob-limit-volatility-drag)")
    approx("median growth rate 10% - 0.2^2/2, in %", 100 * (0.10 - 0.5 * 0.2**2), 8, 6)
    z = rng.standard_normal(2_000_000)
    s1 = np.exp(0.10 - 0.5 * 0.04 + 0.2 * z)
    simulated("E[S1/S0] (arithmetic mean return 10%)", float(s1.mean()), math.exp(0.10), 0.002)
    simulated("median log growth, simulated", float(np.median(np.log(s1))), 0.08, 0.002)
    simulated("E[log S1/S0] below log E[S1/S0] (Jensen)", float(np.log(s1).mean()), 0.08, 0.002)

    print("Cauchy sample mean (card prob-limit-cauchy-sample-mean)")
    for n in (1, 100, 2000):
        means = rng.standard_cauchy((10_000, n)).mean(axis=1)
        q1, q3 = np.quantile(means, [0.25, 0.75])
        simulated(f"interquartile range of the mean of {n} Cauchys (standard Cauchy: 2)", float(q3 - q1), 2.0, 0.12)


def main() -> None:
    bounds()
    normal_tails()
    coin_examples()
    roulette_and_dice()
    scaling_and_estimation()
    print("All limit-theorem checks passed.")


if __name__ == "__main__":
    main()
