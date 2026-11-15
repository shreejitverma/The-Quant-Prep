"""ML problem set: every number in the worked examples and cards, by an independent route.

Backs every number in `10-Machine-Learning-for-Finance/11-ML-Problem-Set.md`.
Independent routes used here:
- OLS on 50 features with one real one by simulating 2,000 training sets, scoring each fit by its exact population
  test MSE, against the closed forms;
- overlapping-label variance inflation by summing the exact covariance matrix and by simulating null t-statistics;
- the purge and embargo sets by a brute-force loop over every day's return window;
- false discoveries with exact binomial arithmetic, the expected largest |t| by quadrature and by simulation, and the
  Bonferroni threshold by bisection on the normal tail;
- the ridge estimate as a posterior mean by numerical integration over beta;
- the accuracy, IC and information-ratio arithmetic, with the accuracy standard error checked by simulation;
- CPCV splits and paths by enumerating every combination.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 10-Machine-Learning-for-Finance/code/ml_11_problem_set.py`.
"""

from __future__ import annotations

import itertools
import math
import os
from fractions import Fraction

# Thousands of small least-squares fits: one BLAS thread is as fast natively, avoids thread oversubscription
# (which made this script crawl under amd64 emulation) and keeps every reduction in a fixed order.
for _var in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_var, "1")

import numpy as np  # noqa: E402

SEED = 20261114


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, expected {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (expected {expected:.4f}, tolerance {tol:.4f})")


def norm_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2))


def useless_features(rng: np.random.Generator) -> None:
    print("Example 1: OLS with 49 useless features (cards ml-pset-oos-r2-negative, ml-pset-insample-r2)")
    n, p, r2_true, reps = 2520, 50, 0.005, 2000
    closed_oos = r2_true - (1 - r2_true) * p / (n - p - 1)
    approx("closed-form OOS R^2", closed_oos, -0.015, 3)
    approx("50/2469", p / (n - p - 1), 0.02025, 5)
    approx("in-sample rule of thumb 0.005 + p/n", r2_true + p / n, 0.025, 3)
    approx("p/n", p / n, 0.02, 2)
    b2 = r2_true / (1 - r2_true)  # one real feature with coefficient sqrt(b2) and unit noise
    ins, oos = np.empty(reps), np.empty(reps)
    for r in range(reps):
        x = rng.standard_normal((n, p))
        beta = np.zeros(p)
        beta[0] = math.sqrt(b2)
        y = x @ beta + rng.standard_normal(n)
        b, *_ = np.linalg.lstsq(x, y, rcond=None)
        ins[r] = 1 - np.sum((y - x @ b) ** 2) / np.sum(y**2)
        oos[r] = 1 - (1 + np.sum((beta - b) ** 2)) / (1 + b2)  # Gaussian test design: MSE = 1 + ||beta - b||^2
    simulated("simulated OOS R^2 against the closed form", float(oos.mean()), closed_oos, 4 * oos.std() / math.sqrt(reps))
    approx("simulated OOS R^2", float(oos.mean()), -0.0151, 4)
    approx("simulated in-sample R^2", float(ins.mean()), 0.025, 3)
    simulated("in-sample against 1 - (1-R^2)(n-p)/n", float(ins.mean()), 1 - (1 - r2_true) * (n - p) / n, 4 * ins.std() / math.sqrt(reps))
    approx("in-sample over true R^2", float(ins.mean()) / r2_true, 5, 0)
    approx("estimation cost 0.995 x 50/2469", (1 - r2_true) * p / (n - p - 1), 0.020, 3)
    approx("estimation cost over signal, 0.995 x 50/2469 / 0.005", (1 - r2_true) * p / (n - p - 1) / r2_true, 4, 0)


def overlapping_t(rng: np.random.Generator) -> None:
    print("Example 2: overlapping 20-day labels over 1,000 days (card ml-pset-overlap-tstat)")
    T, h = 1000, 20
    exact("returns shared by adjacent labels", len(set(range(1, h + 1)) & set(range(2, h + 2))), 19)
    exact("effective observations T/h", T // h, 50)
    exact("long-run factor 1 + 2 sum (h-k)/h", 1 + 2 * sum(Fraction(h - k, h) for k in range(1, h)), 20)
    approx("sqrt(20)", math.sqrt(20), 4.5, 1)
    ratio = sum((T - abs(k)) * (h - abs(k)) for k in range(-(h - 1), h)) / (T * h)
    approx("exact finite-sample inflation of the mean, T = 1000", ratio, 19.87, 2)
    approx("its square root", math.sqrt(ratio), 4.46, 2)
    reps = 10_000
    t_naive, t_known = np.empty(reps), np.empty(reps)
    for i in range(reps):
        c = np.cumsum(np.concatenate([[0.0], rng.standard_normal(T + h)]))
        lab = c[h + 1 : T + h + 1] - c[1 : T + 1]
        t_naive[i] = lab.mean() / (lab.std(ddof=1) / math.sqrt(T))
        t_known[i] = lab.mean() / (math.sqrt(h) / math.sqrt(T))  # control, one change: the true label sd sqrt(h)
    sd_known = float(t_known.std())
    simulated(
        "sd of t with the true label sd, against sqrt(exact inflation)", sd_known, math.sqrt(ratio), 4 * sd_known / math.sqrt(2 * reps)
    )
    sd = float(t_naive.std())
    approx("sd of the naive t (sample sd), simulated", sd, 4.6, 1)
    paired = t_naive**2 - t_known**2  # same samples, so the difference is measured far more precisely than either sd
    assert paired.mean() > 4 * paired.std() / math.sqrt(reps), (paired.mean(), paired.std())
    print("    estimating the label sd from the same overlapping data pushes the naive t a little further")


def purge_sets() -> None:
    print("Example 3: purge and embargo sets (card ml-pset-purge-count)")
    days = range(2500)
    window = {t: set(range(t + 1, t + 6)) for t in days}  # label at t uses returns t+1 .. t+5
    test = set(range(500, 600))
    test_returns = set().union(*(window[t] for t in test))
    purged = sorted(t for t in days if t not in test and (window[t] & test_returns or window[t] & test))
    before = [t for t in purged if t < 500]
    after = [t for t in purged if t > 599]
    exact("purged before the fold", (before[0], before[-1], len(before)), (495, 499, 5))
    exact("purged after the fold", (after[0], after[-1], len(after)), (600, 603, 4))
    exact("last return used by the test fold", max(test_returns), 604)
    embargo = round(0.01 * 2500)
    exact("1% embargo in days", embargo, 25)
    emb = list(range(after[-1] + 1, after[-1] + 1 + embargo))
    exact("embargoed days", (emb[0], emb[-1]), (604, 628))
    train = [t for t in days if t not in test and t not in purged and t not in emb]
    exact("training set", (train[0], max(t for t in train if t < 500), min(t for t in train if t > 599)), (0, 494, 629))


def multiple_testing(rng: np.random.Generator) -> None:
    print("Example 4: 200 useless features (card ml-pset-false-discoveries)")
    m = 200
    exact("expected false discoveries", Fraction(5, 100) * m, 10)
    p_any = 1 - Fraction(95, 100) ** m
    approx("P(at least one)", float(p_any), 1.0, 4)
    # E[max |Z|] = integral of 1 - P(|Z| <= x)^m, by the trapezoid rule
    xs = np.linspace(0, 12, 120_001)
    cdf_abs = np.array([math.erf(x / math.sqrt(2)) for x in xs])
    integrand = 1 - cdf_abs**m
    e_max = float(np.sum((integrand[1:] + integrand[:-1]) * np.diff(xs)) / 2)
    approx("E[max |t|] over 200 nulls (quadrature)", e_max, 2.97, 2)
    approx("E[max |t|], one decimal", e_max, 3.0, 1)
    sims = np.abs(rng.standard_normal((50_000, m))).max(axis=1)
    simulated("E[max |t|], simulated", float(sims.mean()), e_max, 4 * sims.std() / math.sqrt(len(sims)))
    lo, hi = 0.0, 10.0
    target = 0.05 / m / 2
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if 1 - norm_cdf(mid) > target else (lo, mid)
    approx("Bonferroni two-sided threshold", lo, 3.66, 2)
    exact("two-sided p threshold", Fraction(5, 100) / m, Fraction(25, 100_000))


def ridge_prior() -> None:
    print("Example 5: ridge as a prior (cards ml-pset-ridge-shrink, ml-pset-ridge-prior)")
    n, sxy, tau = 1000, 30.0, 0.02
    lam = 1 / tau**2
    approx("lambda = sigma^2 / tau^2", lam, 2500, 9)
    approx("OLS beta", sxy / n, 0.03, 12)
    approx("shrinkage n / (n + lambda)", n / (n + lam), 0.2857, 4)
    approx("shrinkage, two decimals", n / (n + lam), 0.29, 2)
    # posterior mean by integrating over beta: likelihood exp(-(n/2)(beta - 0.03)^2) times prior N(0, tau^2)
    b = np.linspace(-0.2, 0.2, 400_001)
    logpost = -0.5 * n * (b - sxy / n) ** 2 - 0.5 * b**2 / tau**2
    w = np.exp(logpost - logpost.max())
    post_mean = float(np.sum(b * w) / np.sum(w))
    approx("posterior mean by quadrature", post_mean, 0.0086, 4)
    approx("ridge estimate sxy / (sxx + lambda)", sxy / (n + lam), 0.0086, 4)
    approx("0.03 x 0.2857", 0.03 * 0.2857, 0.00857, 5)


def accuracy_ic_ir(rng: np.random.Generator) -> None:
    print("Examples 6 and 7 and the IC cards (ml-pset-accuracy-baseline, ml-pset-ic-to-ir, ml-pset-ic-significance)")
    se = math.sqrt(0.53 * 0.47 / 1000)
    approx("standard error of accuracy", se, 0.016, 3)
    approx("standard error in points", 100 * se, 1.6, 1)
    approx("z for a 1-point lift", 0.01 / se, 0.63, 2)
    approx("z, one decimal", 0.01 / se, 0.6, 1)
    acc = rng.binomial(1000, 0.53, size=200_000) / 1000
    simulated("simulated sd of accuracy", float(acc.std()), se, 4 * se / math.sqrt(2 * 200_000))
    approx("IR = 0.02 sqrt(500)", 0.02 * math.sqrt(500), 0.45, 2)
    approx("IR = 0.02 sqrt(50)", 0.02 * math.sqrt(50), 0.14, 2)
    approx("IC t-stat 0.05 sqrt(1000)", 0.05 * math.sqrt(1000), 1.58, 2)
    assert 0.05 * math.sqrt(1000) < 1.96


def cpcv() -> None:
    print("CPCV with 6 groups and 2 test groups (card ml-pset-cpcv-paths)")
    splits = list(itertools.combinations(range(6), 2))
    exact("splits", len(splits), 15)
    tested = [sum(1 for s in splits if g in s) for g in range(6)]
    exact("times each group is tested", tested, [5] * 6)
    exact("k/N x C(N, k)", Fraction(2, 6) * 15, 5)


def main() -> None:
    rng = np.random.default_rng(SEED)
    useless_features(rng)
    overlapping_t(rng)
    purge_sets()
    multiple_testing(rng)
    ridge_prior()
    accuracy_ic_ir(rng)
    cpcv()
    print("All ML problem set numbers verified.")


if __name__ == "__main__":
    main()
