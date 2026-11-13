"""Expectation, variance and linearity: every mean and variance in the note, without the indicator shortcut.

Backs every number in `01-Probability/04-Expectation-Variance-and-Linearity.md`.
The note gets its answers from indicators, tail sums, Wald and the total-variance formula; this script
gets them another way: exhaustive enumeration with `fractions.Fraction` where the sample space is
finite (dice, permutations, coin sequences, the hypergeometric PMF), an exact occupancy recursion for the
empty-boxes count, the full distribution of the coupon-collector time by dynamic programming, and seeded
simulation for the continuous and unbounded cases, each with a stated tolerance.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 01-Probability/code/prob_04_expectation.py`.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

import numpy as np

SEED = 20261019


def exact(label: str, value: Fraction | int, expected: Fraction | int) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol})")


def moments(dist: dict[int, Fraction]) -> tuple[Fraction, Fraction]:
    mean = sum((k * p for k, p in dist.items()), Fraction(0))
    return mean, sum(((k - mean) ** 2 * p for k, p in dist.items()), Fraction(0))


def hypergeometric_aces() -> None:
    print("Aces in a 5-card hand (card prob-exp-hypergeometric-aces-variance), from the hypergeometric PMF")
    total = math.comb(52, 5)
    dist = {k: Fraction(math.comb(4, k) * math.comb(48, 5 - k), total) for k in range(5)}
    mean, var = moments(dist)
    exact("E[aces]", mean, Fraction(5, 13))
    exact("Var[aces]", var, Fraction(940, 2873))
    approx("Var[aces]", float(var), 0.327, 3)
    exact("2652 = 52*51", 52 * 51, 2652)
    exact("binomial variance times (52-5)/(52-1)", 5 * Fraction(1, 13) * Fraction(12, 13) * Fraction(47, 51), var)


def fixed_points() -> None:
    print("Example 1 - fixed points of a random permutation (card prob-exp-fixed-points-mean-variance)")
    for n in range(2, 9):
        counts: dict[int, Fraction] = {}
        perms = list(itertools.permutations(range(n)))
        for p in perms:
            k = sum(p[i] == i for i in range(n))
            counts[k] = counts.get(k, Fraction(0)) + Fraction(1, len(perms))
        mean, var = moments(counts)
        assert mean == 1 and var == 1, (n, mean, var)
        both = Fraction(sum(1 for p in perms if p[0] == 0 and p[1] == 1), len(perms))
        assert both - Fraction(1, n * n) == Fraction(1, n * n * (n - 1))
    print("    mean = variance = 1 and Cov(I_i, I_j) = 1/(n^2(n-1)) by enumeration for n = 2..8")
    exact("n = 1: variance", moments({1: Fraction(1)})[1], 0)


def coupon_collector() -> None:
    print("Example 2 - coupon collector with a die (card prob-exp-coupon-collector-die), exact distribution by DP")
    horizon = 600
    state = np.zeros(7)
    state[0] = 1.0  # number of distinct faces seen
    pmf = np.zeros(horizon + 1)
    for t in range(1, horizon + 1):
        new = np.zeros(7)
        for k in range(6):
            new[k] += state[k] * k / 6
            new[k + 1] += state[k] * (6 - k) / 6
        pmf[t] = new[6]
        new[6] = 0.0
        state = new
    t = np.arange(horizon + 1)
    assert abs(pmf.sum() - 1) < 1e-12
    mean = float((t * pmf).sum())
    var = float((t**2 * pmf).sum()) - mean**2
    approx("E[rolls to see all six faces]", mean, 14.7, 9)
    approx("Var[rolls to see all six faces]", var, 38.99, 2)
    exact("6 H_6", 6 * sum(Fraction(1, k) for k in range(1, 7)), Fraction(147, 10))
    exact("stage means 6/(7-k)", [Fraction(6, 7 - k) for k in range(1, 7)], [Fraction(6, d) for d in (6, 5, 4, 3, 2, 1)])
    gamma = float(sum(1 / k for k in range(1, 2_000_001)) - math.log(2_000_000))  # Euler-Mascheroni, from H_n - ln n
    approx("Euler-Mascheroni constant from H_n - ln n", gamma, 0.577, 3)
    approx("n ln n + 0.577 n + 1/2 at n=6", 6 * math.log(6) + gamma * 6 + 0.5, 14.71, 2)


def random_number_of_dice() -> None:
    print("Example 3 - a random number of dice (card prob-exp-random-sum-of-dice), exact distribution of S")
    die = {k: Fraction(1, 6) for k in range(1, 7)}
    dist: dict[int, Fraction] = {}
    conv = {0: Fraction(1)}
    for _ in range(1, 7):
        nxt: dict[int, Fraction] = {}
        for s, p in conv.items():
            for f, q in die.items():
                nxt[s + f] = nxt.get(s + f, Fraction(0)) + p * q
        conv = nxt
        for s, p in conv.items():
            dist[s] = dist.get(s, Fraction(0)) + p / 6
    mean, var = moments(dist)
    exact("E[S]", mean, Fraction(49, 4))
    approx("E[S]", float(mean), 12.25, 2)
    exact("Var[S]", var, Fraction(735, 16))
    approx("Var[S]", float(var), 45.94, 2)
    mu, s2 = moments(die)
    exact("die mean", mu, Fraction(7, 2))
    exact("die variance", s2, Fraction(35, 12))
    exact("within part sigma^2 E[N]", s2 * mu, Fraction(245, 24))
    exact("between part mu^2 Var[N]", mu**2 * s2, Fraction(1715, 48))
    assert mu**2 * s2 > s2 * mu
    print("    the between-group term (35.73) dominates the within-group term (10.21)")


def dice_extremes_and_rolls(rng: np.random.Generator) -> None:
    print("Example 4 - maximum of two dice (card prob-exp-max-two-dice)")
    pairs = list(itertools.product(range(1, 7), repeat=2))
    e_max = Fraction(sum(max(p) for p in pairs), 36)
    e_min = Fraction(sum(min(p) for p in pairs), 36)
    exact("E[max of two dice] (enumerated)", e_max, Fraction(161, 36))
    approx("E[max of two dice]", float(e_max), 4.47, 2)
    exact("E[min of two dice] (enumerated)", e_min, Fraction(91, 36))
    exact("0+1+4+9+16+25", sum(k * k for k in range(6)), 55)

    print("Example 5 - sum of rolls until the first six (card prob-exp-sum-until-first-six)")
    # exact series: P(N = n) = (5/6)^(n-1)/6 and E[sum | N = n] = 3(n-1) + 6, summed with Fractions until the tail is negligible
    series = sum((Fraction(5, 6) ** (n - 1) / 6 * (3 * (n - 1) + 6) for n in range(1, 400)), Fraction(0))
    approx("E[sum until first 6] (series)", float(series), 21, 9)
    rolls = rng.integers(1, 7, size=(400_000, 120))
    first_six = np.argmax(rolls == 6, axis=1)
    assert np.all(rolls[np.arange(len(rolls)), first_six] == 6)
    totals = np.where(np.arange(120) <= first_six[:, None], rolls, 0).sum(axis=1)
    simulated("E[sum until first 6], simulated", float(totals.mean()), 21, 0.15)
    exact("E[non-six roll]", Fraction(sum(range(1, 6)), 5), 3)


def indicator_cards(rng: np.random.Generator) -> None:
    print("Shared birthday pairs (card prob-exp-shared-birthday-pairs)")
    bdays = rng.integers(0, 365, size=(200_000, 30))
    srt = np.sort(bdays, axis=1)
    pairs = np.zeros(len(srt))
    for d in range(1, 30):  # count equal pairs: sum over values of C(multiplicity, 2)
        pairs += (srt[:, d:] == srt[:, :-d]).sum(axis=1)
    exact("C(30,2)", math.comb(30, 2), 435)
    approx("435/365", 435 / 365, 1.19, 2)
    simulated("E[shared-birthday pairs among 30], simulated", float(pairs.mean()), 435 / 365, 0.01)

    print("Empty boxes (card prob-exp-empty-boxes), exact occupancy recursion")
    n = 10
    dist = {0: Fraction(1)}  # number of occupied boxes after each ball
    for _ in range(n):
        nxt: dict[int, Fraction] = {}
        for k, p in dist.items():
            nxt[k] = nxt.get(k, Fraction(0)) + p * Fraction(k, n)
            nxt[k + 1] = nxt.get(k + 1, Fraction(0)) + p * Fraction(n - k, n)
        dist = nxt
    e_empty = sum(((n - k) * p for k, p in dist.items()), Fraction(0))
    exact("E[empty boxes], 10 balls into 10 boxes", e_empty, n * Fraction(n - 1, n) ** n)
    approx("E[empty boxes], 10 balls into 10 boxes", float(e_empty), 3.49, 2)
    approx("n/e at n=10", n / math.e, 3.68, 2)

    print("Runs and overlapping HH (cards prob-exp-runs-in-coin-flips, prob-exp-overlapping-hh-count)")
    for m in range(1, 13):
        seqs = list(itertools.product("HT", repeat=m))
        runs = Fraction(sum(1 + sum(s[i] != s[i - 1] for i in range(1, m)) for s in seqs), len(seqs))
        assert runs == Fraction(m + 1, 2), (m, runs)
    print("    E[runs] = (n+1)/2 by enumerating all 2^n sequences, n = 1..12")
    seqs = list(itertools.product("HT", repeat=10))
    hh = Fraction(sum(sum(s[i] == s[i + 1] == "H" for i in range(9)) for s in seqs), len(seqs))
    exact("E[HH occurrences in 10 flips] (enumerated)", hh, Fraction(9, 4))

    print("Distinct faces in six rolls (card prob-exp-distinct-faces-six-rolls)")
    distinct = Fraction(sum(len(set(r)) for r in itertools.product(range(6), repeat=6)), 6**6)
    exact("E[distinct faces] (enumerated over 6^6 outcomes)", distinct, 6 * (1 - Fraction(5, 6) ** 6))
    approx("E[distinct faces]", float(distinct), 3.99, 2)

    print("E|U1 - U2| and the mixture variance (cards prob-exp-abs-diff-uniforms, prob-exp-total-variance-mixture)")
    u = rng.random((2_000_000, 2))
    simulated("E|U1 - U2|, simulated", float(np.abs(u[:, 0] - u[:, 1]).mean()), 1 / 3, 0.001)
    comp = rng.integers(0, 2, 2_000_000)
    draws = rng.standard_normal(2_000_000) + 2 * comp
    simulated("variance of the 50/50 mixture of N(0,1) and N(2,1), simulated", float(draws.var()), 2.0, 0.01)
    exact("E[Var | component] + Var(E | component)", 1 + moments({0: Fraction(1, 2), 2: Fraction(1, 2)})[1], 2)

    print("Best mean-square predictor (card prob-exp-best-mse-predictor)")
    y = rng.standard_normal(1_000_000)
    x = y**2 + rng.standard_normal(1_000_000)  # E[X|Y] = Y^2, nonlinear; best linear predictor is the constant 1
    mse_cond = float(((x - y**2) ** 2).mean())
    b = float(np.cov(x, y)[0, 1] / y.var())
    a = float(x.mean() - b * y.mean())
    mse_lin = float(((x - a - b * y) ** 2).mean())
    simulated("MSE of E[X|Y] = Y^2 (noise variance 1)", mse_cond, 1.0, 0.01)
    simulated("MSE of the best linear predictor (1 + Var(Y^2) = 3)", mse_lin, 3.0, 0.03)
    simulated("residual X - E[X|Y] is uncorrelated with Y^2", float(np.corrcoef(x - y**2, y**2)[0, 1]), 0.0, 0.003)


def main() -> None:
    rng = np.random.default_rng(SEED)
    hypergeometric_aces()
    fixed_points()
    coupon_collector()
    random_number_of_dice()
    dice_extremes_and_rolls(rng)
    indicator_cards(rng)
    print("All expectation checks passed.")


if __name__ == "__main__":
    main()
