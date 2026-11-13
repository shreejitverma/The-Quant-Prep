"""Bootstrap and resampling: every number in the note, by an independent route.

Backs every number in `02-Statistics-and-Econometrics/12-Bootstrap-and-Resampling.md`.
Independent routes used here:
- inclusion probabilities by exact enumeration of every resample (n = 5) and by simulation (n = 252);
- the number of distinct resamples by enumerating multisets;
- the ideal bootstrap standard error of a mean by enumerating all 5^5 ordered resamples;
- the exact permutation p-value by enumerating all 70 labellings with exact fractions;
- the true standard error of an AR(1) mean from the exact autocovariance sum and from simulated paths,
  and the iid and stationary bootstraps re-run with the note snippet's own seeds;
- percentile versus bootstrap-t coverage by seeded simulation of skewed data, changing only the interval method.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 02-Statistics-and-Econometrics/code/stats_12_bootstrap.py`.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction
from statistics import NormalDist

import numpy as np

SEED = 20261112
N01 = NormalDist()


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol:.4f})")


def inclusion(rng: np.random.Generator) -> None:
    print("Example 1, Example 6 and cards stat-boot-632, stat-boot-fails-max: the 0.632 rule")
    hits = sum(1 for r in itertools.product(range(5), repeat=5) if 0 in r)
    exact("resamples of 5 containing a given point, out of 3125", hits, 2101)
    approx("n = 5", hits / 3125, 0.672, 3)
    approx("n = 10", 1 - 0.9**10, 0.651, 3)
    p252 = 1 - (251 / 252) ** 252
    approx("n = 252", p252, 0.6329, 4)
    approx("n = 252 (three decimals)", p252, 0.633, 3)
    approx("limit 1 - 1/e", 1 - math.exp(-1), 0.6321, 4)
    approx("miss probability e^-1", math.exp(-1), 0.368, 3)
    draws = rng.integers(0, 252, size=(200000, 252))
    contains = np.any(draws == 0, axis=1)
    simulated("simulated share of n = 252 resamples containing a given point", float(contains.mean()), 0.6329, 4 * math.sqrt(0.25 / 200000))
    approx("n = 1000", 1 - 0.999**1000, 0.632, 3)
    exact("distinct resamples, n = 5", sum(1 for _ in itertools.combinations_with_replacement(range(5), 5)), 126)
    exact("distinct resamples, n = 10", sum(1 for _ in itertools.combinations_with_replacement(range(10), 10)), 92378)
    exact("binom(2n-1, n) for n = 10", math.comb(19, 10), 92378)


def mean_se() -> None:
    print("Example 2: bootstrap SE of a mean by full enumeration")
    x = [2, -1, 4, 0, 5]
    mean = Fraction(sum(x), 5)
    ss = sum((v - mean) ** 2 for v in x)
    exact("mean", mean, 2)
    approx("s", math.sqrt(ss / 4), 2.550, 3)
    approx("textbook SE s/sqrt(5)", math.sqrt(ss / 4) / math.sqrt(5), 1.140, 3)
    approx("plug-in sigma", math.sqrt(ss / 5), 2.280, 3)
    means = [Fraction(sum(r), 5) for r in itertools.product(x, repeat=5)]
    m = sum(means) / len(means)
    var = sum((v - m) ** 2 for v in means) / len(means)
    exact("variance of the resample mean over all 3125 resamples", var, ss / 25)
    approx("ideal bootstrap SE", math.sqrt(var), 1.020, 3)
    approx("ratio sqrt((n-1)/n)", math.sqrt(4 / 5), 0.894, 3)


def sharpe_interval(rng: np.random.Generator) -> None:
    print("Example 3 and card stat-boot-sharpe-3y: Sharpe 1.0 over three years")
    t = 756
    srd = 1 / math.sqrt(252)
    se = math.sqrt(252) * math.sqrt((1 + srd**2 / 2) / (t - 1))
    z = N01.inv_cdf(0.975)
    approx("Lo SE of annualised Sharpe", se, 0.578, 3)
    approx("lower", 1 - z * se, -0.13, 2)
    approx("upper", 1 + z * se, 2.13, 2)
    zz = rng.standard_normal(t)
    r = (zz - zz.mean()) / zz.std(ddof=1) * 0.01 + 0.01 * srd  # exactly Sharpe 1.0 annualised
    approx("constructed series annualised Sharpe", r.mean() / r.std(ddof=1) * math.sqrt(252), 1.0, 10)
    idx = rng.integers(0, t, size=(5000, t))
    rb = r[idx]
    sr = rb.mean(axis=1) / rb.std(axis=1, ddof=1) * math.sqrt(252)
    approx("iid bootstrap SE (B = 5000)", float(sr.std(ddof=1)), 0.59, 2)
    approx("percentile lower", float(np.quantile(sr, 0.025)), -0.14, 2)
    approx("percentile upper", float(np.quantile(sr, 0.975)), 2.16, 2)
    approx("share of resampled Sharpes at or below zero (%)", 100 * float(np.mean(sr <= 0)), 4.6, 1)
    approx("t = sqrt(3)", math.sqrt(3), 1.73, 2)
    approx("one-sided p", 1 - N01.cdf(math.sqrt(3)), 0.04, 2)
    approx("shortcut SE 1/sqrt(3)", 1 / math.sqrt(3), 0.58, 2)


def stationary_bootstrap_idx(n: int, mean_block: float, rng: np.random.Generator) -> np.ndarray:
    idx = np.empty(n, dtype=int)
    idx[0] = rng.integers(n)
    new_block = rng.random(n) < 1.0 / mean_block
    starts = rng.integers(n, size=n)
    for t in range(1, n):
        idx[t] = starts[t] if new_block[t] else (idx[t - 1] + 1) % n
    return idx


def boot_se(x: np.ndarray, B: int = 2000, mean_block: float | None = None, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    n = len(x)
    draws = [
        np.mean(x[rng.integers(n, size=n)] if mean_block is None else x[stationary_bootstrap_idx(n, mean_block, rng)]) for _ in range(B)
    ]
    return float(np.std(draws, ddof=1))


def dependent(rng: np.random.Generator) -> None:
    print("Example 4 and card stat-boot-iid-on-ar1: iid versus stationary bootstrap on AR(1), the snippet's seeds")
    snip = np.random.default_rng(42)
    n, phi = 1000, 0.3
    e = snip.standard_normal(n + 100)
    x = np.zeros(n + 100)
    for t in range(1, n + 100):
        x[t] = phi * x[t - 1] + e[t]
    x = x[100:]
    approx("naive iid formula", float(x.std() / math.sqrt(n)), 0.034, 3)
    approx("iid bootstrap", boot_se(x), 0.034, 3)
    approx("stationary bootstrap, mean block 10", boot_se(x, mean_block=10), 0.042, 3)
    gamma0 = 1 / (1 - phi**2)
    k = np.arange(1, n)
    exact_var = gamma0 / n * (1 + 2 * float(np.sum((1 - k / n) * phi**k)))
    approx("true SE from the exact autocovariance sum", math.sqrt(exact_var), 0.045, 3)
    approx("asymptotic formula", math.sqrt(gamma0 * (1 + phi) / (1 - phi) / n), 0.045, 3)
    paths = np.zeros((20000, n + 100))
    eps = rng.standard_normal((20000, n + 100))
    for t in range(1, n + 100):
        paths[:, t] = phi * paths[:, t - 1] + eps[:, t]
    means = paths[:, 100:].mean(axis=1)
    sd = float(means.std())
    simulated("sd of the mean over 20,000 simulated paths", sd, 0.045, 4 * sd / math.sqrt(2 * 20000) + 0.0005)
    approx("variance ratio (1 + phi)/(1 - phi)", (1 + phi) / (1 - phi), 1.857, 3)
    approx("SE understatement sqrt(1.857)", math.sqrt((1 + phi) / (1 - phi)), 1.36, 2)
    approx("n^(1/3) for n = 1000", n ** (1 / 3), 10, 6)


def permutation() -> None:
    print("Example 5 and cards stat-boot-permutation-exact, stat-boot-permutation-pvalue")
    on = [Fraction(9, 10), Fraction(4, 10), Fraction(12, 10), Fraction(7, 10)]
    off = [Fraction(1, 10), Fraction(-3, 10), Fraction(5, 10), Fraction(2, 10)]
    pool = on + off
    obs = sum(on) / 4 - sum(off) / 4
    exact("on mean", sum(on) / 4, Fraction(4, 5))
    exact("off mean", sum(off) / 4, Fraction(1, 8))
    exact("observed difference", obs, Fraction(27, 40))
    count, total, extreme = 0, 0, []
    for chosen in itertools.combinations(range(8), 4):
        a = [pool[i] for i in chosen]
        b = [pool[i] for i in range(8) if i not in chosen]
        total += 1
        if sum(a) / 4 - sum(b) / 4 >= obs:
            count += 1
            extreme.append(sorted(a))
    exact("labellings", total, 70)
    exact("labellings at least as extreme", count, 2)
    assert sorted(on) in extreme and sorted([Fraction(9, 10), Fraction(5, 10), Fraction(12, 10), Fraction(7, 10)]) in extreme
    print("    the two are the observed labelling and the one that swaps 0.4 for 0.5")
    approx("p = 2/70", count / total, 0.029, 3)
    approx("p with 999 permutations and none beating the observed", (1 + 0) / (999 + 1), 0.001, 6)


def percentile_failure(rng: np.random.Generator) -> None:
    print("When the percentile interval fails: mean of 20 Exp(1) draws, one-sided 95% upper bounds (card stat-boot-percentile-skewed)")
    n, datasets, b = 20, 4000, 999
    cover_pct = cover_t = 0
    for _ in range(datasets // 200):
        x = rng.exponential(1.0, size=(200, n))
        xbar = x.mean(axis=1)
        se = x.std(axis=1, ddof=1) / math.sqrt(n)
        idx = rng.integers(0, n, size=(200, b, n))
        xb = np.take_along_axis(np.repeat(x[:, None, :], b, axis=1), idx, axis=2)
        mb = xb.mean(axis=2)
        seb = xb.std(axis=2, ddof=1) / math.sqrt(n)
        upper_pct = np.quantile(mb, 0.95, axis=1)
        tstar = (mb - xbar[:, None]) / np.where(seb > 0, seb, np.inf)
        upper_t = xbar - np.quantile(tstar, 0.05, axis=1) * se
        cover_pct += int(np.sum(upper_pct >= 1.0))
        cover_t += int(np.sum(upper_t >= 1.0))
    cp, ct = cover_pct / datasets, cover_t / datasets
    se_cov = math.sqrt(0.95 * 0.05 / datasets)
    simulated("coverage of the percentile 95% upper bound", cp, 0.88, 4 * se_cov + 0.005)
    simulated("coverage of the bootstrap-t 95% upper bound", ct, 0.93, 4 * se_cov + 0.005)
    assert ct - cp > 0.02


def main() -> None:
    rng = np.random.default_rng(SEED)
    inclusion(rng)
    mean_se()
    sharpe_interval(rng)
    dependent(rng)
    permutation()
    percentile_failure(rng)
    print("all bootstrap checks passed")


if __name__ == "__main__":
    main()
