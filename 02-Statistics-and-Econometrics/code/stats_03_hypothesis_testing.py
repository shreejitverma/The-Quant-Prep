"""Hypothesis testing and multiple comparisons: every p-value, power and correction in the note.

Backs every number in `02-Statistics-and-Econometrics/03-Hypothesis-Testing-and-Multiple-Comparisons.md`.
Independent routes used here:
- normal quantiles and tails from `statistics.NormalDist`, never quoted from a table;
- power by seeded simulation of daily return paths, against the closed form Phi(S sqrt(T) - z);
- the expected maximum of N normals by quadrature of N x Phi^(N-1) phi, cross-checked by simulation;
- Bonferroni, Holm and Benjamini-Hochberg decisions by their step-by-step definitions, and adjusted p-values by
  a separate monotone-minimum route that must reach the same rejection set;
- the FWER and FDR guarantees by seeded simulation under independence and positive equicorrelation (PRDS);
- positive predictive values by counting ideas in a population of 1,000.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 02-Statistics-and-Econometrics/code/stats_03_hypothesis_testing.py`.
"""

from __future__ import annotations

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


def expected_max_normal(n: int) -> float:
    """E[max of n iid N(0,1)] = int x n Phi(x)^(n-1) phi(x) dx by Simpson on [-12, 12]."""
    x = np.linspace(-12.0, 12.0, 24001)
    phi = np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
    cdf = np.array([N01.cdf(v) for v in x])
    y = x * n * cdf ** (n - 1) * phi
    h = x[1] - x[0]
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))


# ---------------------------------------------------------------- multiple-testing procedures by definition


def bonferroni(p: list[float], alpha: float) -> int:
    return sum(1 for x in p if x <= alpha / len(p))


def holm(p: list[float], alpha: float) -> int:
    m, k = len(p), 0
    for i, x in enumerate(sorted(p)):
        if x <= alpha / (m - i):
            k += 1
        else:
            break
    return k


def step_up(p: list[float], q: float, c: float = 1.0) -> int:
    """Largest k with p_(k) <= k q / (m c); c = sum 1/i gives Benjamini-Yekutieli."""
    m, s = len(p), sorted(p)
    return max((k for k in range(1, m + 1) if s[k - 1] <= k * q / (m * c)), default=0)


def bh_adjusted(p: list[float]) -> list[float]:
    s, m = sorted(p), len(p)
    raw = [s[j] * m / (j + 1) for j in range(m)]
    return [min(raw[j:]) for j in range(m)]


def basics() -> None:
    print("TL;DR, Example 4 and cards stat-ht-fwer-twenty-tests: chance of at least one false positive")
    approx("1 - 0.95^20", 1 - 0.95**20, 0.642, 3)
    approx("1 - 0.95^20 (%)", 100 * (1 - 0.95**20), 64, 0)
    approx("1 - 0.95^100", 1 - 0.95**100, 0.994, 3)
    print("Expected maximum of N standard normals (Data snooping bullet, Example 4, card stat-ht-expected-max-null-sharpe)")
    e10, e100, e1000 = (expected_max_normal(n) for n in (10, 100, 1000))
    approx("E[max of 10]", e10, 1.54, 2)
    approx("E[max of 100]", e100, 2.508, 3)
    approx("E[max of 100] (two decimals)", e100, 2.51, 2)
    approx("E[max of 1000]", e1000, 3.24, 2)
    approx("best of 100 null Sharpes over 5 years, 2.508/sqrt(5)", e100 / math.sqrt(5), 1.12, 2)
    approx("best of 100 null Sharpes, one decimal", e100 / math.sqrt(5), 1.1, 1)


def examples(rng: np.random.Generator) -> None:
    print("Example 1 and card stat-ht-sharpe-t-stat")
    t = 0.8 * math.sqrt(5)
    approx("t = 0.8 sqrt(5)", t, 1.789, 3)
    approx("two-sided p", 2 * (1 - N01.cdf(t)), 0.074, 3)
    approx("one-sided p", 1 - N01.cdf(t), 0.037, 3)
    approx("years for t = 3 at Sharpe 0.8, 9/0.64", 9 / 0.64, 14, 0)
    approx("years for t = 3 at Sharpe 0.8 (one decimal)", 9 / 0.64, 14.1, 1)

    print("Example 2 and card stat-ht-power-sharpe-half")
    z95 = N01.inv_cdf(0.95)
    approx("z_0.95", z95, 1.645, 3)
    approx("0.5 sqrt(5) - 1.645", 0.5 * math.sqrt(5) - z95, -0.527, 3)
    approx("0.5 sqrt(5) - 1.645 (card)", 0.5 * math.sqrt(5) - z95, -0.53, 2)
    power_half = N01.cdf(0.5 * math.sqrt(5) - z95)
    approx("power at Sharpe 0.5", power_half, 0.30, 2)
    power_one = N01.cdf(math.sqrt(5) - z95)
    approx("power at Sharpe 1", power_one, 0.72, 2)
    approx("rejection rate of a true Sharpe-0.5 strategy (%)", 100 * (1 - power_half), 70, 0)
    approx("sqrt(5)", math.sqrt(5), 2.236, 3)
    for k, thr in enumerate((0.005, 0.010, 0.015, 0.020, 0.025, 0.030), start=1):
        approx(f"BH threshold k = {k}", k * 0.05 / 10, thr, 6)
    days, paths = 1260, 20000
    for s, quoted in ((0.5, power_half), (1.0, power_one)):
        r = s / math.sqrt(252) + rng.standard_normal((paths, days))
        tstat = r.mean(axis=1) / (r.std(axis=1, ddof=1) / math.sqrt(days))
        rej = float(np.mean(tstat > z95))
        simulated(
            f"simulated rejection rate at Sharpe {s}, 20,000 five-year daily paths",
            rej,
            quoted,
            4 * math.sqrt(quoted * (1 - quoted) / paths),
        )

    print("Example 3 and card stat-ht-bh-step-up-example: Bonferroni, Holm, BH, BY on ten p-values")
    p = [0.001, 0.0052, 0.012, 0.021, 0.024, 0.041, 0.09, 0.2, 0.5, 0.8]
    exact("Bonferroni rejections", bonferroni(p, 0.05), 1)
    exact("Holm rejections", holm(p, 0.05), 2)
    approx("Holm threshold 2: 0.05/9", 0.05 / 9, 0.00556, 5)
    approx("Holm threshold 3: 0.05/8", 0.05 / 8, 0.00625, 5)
    exact("BH rejections", step_up(p, 0.05), 5)
    adj = bh_adjusted(p)
    for j, quoted in enumerate((0.010, 0.026, 0.040, 0.048, 0.048, 0.068)):
        approx(f"BH-adjusted p_({j + 1})", adj[j], quoted, 3)
    exact("BH rejections from adjusted p-values", sum(1 for a in adj if a <= 0.05), 5)
    exact("BH with p_(6..10) replaced by values above 0.05", step_up(p[:5] + [0.051, 0.2, 0.5, 0.8, 0.9], 0.05), 5)
    exact("Holm with the same replacement", holm(p[:5] + [0.051, 0.2, 0.5, 0.8, 0.9], 0.05), 2)
    h10 = float(sum(Fraction(1, i) for i in range(1, 11)))
    approx("sum_{i<=10} 1/i", h10, 2.929, 3)
    exact("Benjamini-Yekutieli rejections", step_up(p, 0.05, h10), 1)
    approx("BY threshold for k = 1, 0.05/(10 x 2.929)", 0.05 / (10 * h10), 0.0017, 4)
    approx("BY threshold for k = 2", 2 * 0.05 / (10 * h10), 0.0034, 4)

    print("Example 4: best of 100 zero-edge backtests, simulated")
    paths = 4000
    best = np.empty(paths)
    for i in range(paths):
        sharpe_hat = rng.standard_normal(100) / math.sqrt(5)  # annualised Sharpe estimate ~ N(0, 1/5)
        best[i] = sharpe_hat.max()
    simulated("mean best annualised Sharpe of 100 null strategies", float(best.mean()), 1.12, 4 * float(best.std()) / math.sqrt(paths))

    print("Example 5 and card stat-ht-ppv-base-rate: positive predictive value by counting 1,000 ideas")
    real, null = 1000 * Fraction(5, 100), 1000 * Fraction(95, 100)
    ppv = real * Fraction(1, 2) / (real * Fraction(1, 2) + null * Fraction(5, 100))
    approx("PPV, 5% real, 50% power", float(ppv), 0.345, 3)
    approx("PPV (%)", 100 * float(ppv), 34.5, 1)
    approx("0.025 + 0.0475", 0.025 + 0.0475, 0.0725, 10)
    real, null = 1000 * Fraction(10, 100), 1000 * Fraction(90, 100)
    ppv2 = real * Fraction(8, 10) / (real * Fraction(8, 10) + null * Fraction(5, 100))
    approx("PPV, 10% real, 80% power", float(ppv2), 0.64, 10)
    approx("true-positive share 0.1 x 0.8", 0.1 * 0.8, 0.08, 10)
    approx("false-positive share 0.9 x 0.05", 0.9 * 0.05, 0.045, 10)


def guarantees(rng: np.random.Generator) -> None:
    print("FWER and FDR guarantees by simulation (Core concepts: Family-wise error rate, False discovery rate)")
    m, m0, q, reps = 20, 15, 0.05, 40000
    effects = np.r_[np.zeros(m0), np.full(m - m0, 3.0)]
    for rho, label in ((0.0, "independent"), (0.5, "equicorrelated rho = 0.5 (PRDS)")):
        common = rng.standard_normal((reps, 1))
        z = math.sqrt(rho) * common + math.sqrt(1 - rho) * rng.standard_normal((reps, m)) + effects
        pv = 1 - np.vectorize(N01.cdf)(z)  # one-sided p-values
        fwer_b = fwer_h = fdr_bh = 0.0
        for row in pv:
            order = np.argsort(row)
            k_bh = step_up(list(row), q)
            k_h = holm(list(row), q)
            rej_b = row <= q / m
            fwer_b += bool(rej_b[:m0].any())
            fwer_h += bool((order[:k_h] < m0).any())
            false = int((order[:k_bh] < m0).sum())
            fdr_bh += false / max(k_bh, 1)
            assert k_h >= int(rej_b.sum())
        fwer_b, fwer_h, fdr_bh = fwer_b / reps, fwer_h / reps, fdr_bh / reps
        print(f"    {label}: FWER Bonferroni {fwer_b:.4f}, FWER Holm {fwer_h:.4f}, FDR BH {fdr_bh:.4f}")
        se = math.sqrt(0.05 * 0.95 / reps)
        assert fwer_b <= 0.05 + 4 * se and fwer_h <= 0.05 + 4 * se
        if rho == 0.0:
            simulated("BH FDR under independence vs q m0/m = 0.0375", fdr_bh, q * m0 / m, 4 * se)
            simulated("BH FDR under independence, quoted to three decimals", fdr_bh, 0.037, 4 * se)
        else:
            assert fdr_bh <= q * m0 / m + 4 * se, fdr_bh
            simulated("BH FDR under equicorrelation 0.5", fdr_bh, 0.033, 4 * se)
    approx("q m0 / m for m = 20, m0 = 15, q = 5%", q * m0 / m, 0.0375, 4)


def main() -> None:
    rng = np.random.default_rng(SEED)
    basics()
    examples(rng)
    guarantees(rng)
    print("all hypothesis-testing checks passed")


if __name__ == "__main__":
    main()
