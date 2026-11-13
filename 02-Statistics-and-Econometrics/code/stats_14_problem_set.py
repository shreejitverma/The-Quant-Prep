"""Statistics problem set: every number in the drill set, by an independent route.

Backs every number in `02-Statistics-and-Econometrics/14-Statistics-Problem-Set.md`.
Independent routes used here:
- normal quantiles from `statistics.NormalDist`, Student-t and chi-square quantiles by quadrature and bisection;
- the exact binomial p-value by summing the pmf with integer arithmetic;
- Lo's autocorrelation-adjusted Sharpe by simulating AR(1) monthly returns and measuring annual sums;
- the overlapping-label inflation by simulating a regression of 20-day forward returns on a persistent signal;
- the median's efficiency and the standard error of a correlation by simulation;
- slopes, VIF, omitted-variable bias and attenuation by simulating the stated models;
- GARCH and EWMA numbers by iterating the recursions; bootstrap and permutation numbers by enumeration.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 02-Statistics-and-Econometrics/code/stats_14_problem_set.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction
from statistics import NormalDist

import numpy as np

SEED = 20261112
N01 = NormalDist()


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol:.4f})")


def ols_slope(x: np.ndarray, y: np.ndarray) -> float:
    xc = x - x.mean()
    return float(xc @ (y - y.mean()) / (xc @ xc))


def chi2_ppf(p: float, k: int) -> float:
    grid = np.linspace(0, 200, 2_000_001)
    dens = grid ** (k / 2 - 1) * np.exp(-grid / 2) / (2 ** (k / 2) * math.gamma(k / 2))
    cdf = np.concatenate([[0.0], np.cumsum((dens[1:] + dens[:-1]) / 2) * (grid[1] - grid[0])])
    return float(np.interp(p, cdf, grid))


def numbers_table(rng: np.random.Generator) -> None:
    print("Numbers worth knowing cold")
    approx("z 90% two-sided", N01.inv_cdf(0.95), 1.645, 3)
    approx("z 95% two-sided", N01.inv_cdf(0.975), 1.960, 3)
    approx("z 99% two-sided", N01.inv_cdf(0.995), 2.576, 3)
    approx("z for 80% power", N01.inv_cdf(0.8), 0.842, 3)
    approx("2/pi", 2 / math.pi, 0.64, 2)
    x = rng.standard_normal((20000, 101))
    eff = float(np.var(x.mean(axis=1)) / np.var(np.median(x, axis=1)))
    # SE of a ratio of two sample variances is about ratio * sqrt(2/N + 2/N); allow 0.01 for the finite-n gap to 2/pi
    simulated("simulated efficiency of the median, n = 101", eff, 0.64, 4 * eff * math.sqrt(4 / 20000) + 0.01)
    a, b = rng.standard_normal((20000, 100)), rng.standard_normal((20000, 100))
    ac, bc = a - a.mean(axis=1, keepdims=True), b - b.mean(axis=1, keepdims=True)
    r = np.sum(ac * bc, axis=1) / np.sqrt(np.sum(ac * ac, axis=1) * np.sum(bc * bc, axis=1))
    # exact null sd is 1/sqrt(n-1) = 0.1005; the SE of a sample sd is sd/sqrt(2N)
    simulated("sd of a sample correlation near zero, n = 100, vs 1/sqrt(n)", float(r.std()), 0.1, 4 * 0.1 / math.sqrt(40000) + 0.001)
    approx("-ln 0.05 (rule of three)", -math.log(0.05), 3.0, 1)
    approx("1 - 1/e", 1 - math.exp(-1), 0.632, 3)


def worked_examples(rng: np.random.Generator) -> None:
    print("Example 1 and card stat-ps-power-sharpe-years")
    z95, z975, z80 = N01.inv_cdf(0.95), N01.inv_cdf(0.975), N01.inv_cdf(0.8)
    one, two = ((z95 + z80) / 0.5) ** 2, ((z975 + z80) / 0.5) ** 2
    approx("one-sided years", one, 24.7, 1)
    approx("one-sided years (card, rounded)", one, 25, 0)
    approx("two-sided years", two, 31.4, 1)
    approx("Sharpe 2, one-sided years", one / 16, 1.5, 1)
    approx("Sharpe 2, two-sided years", two / 16, 2.0, 1)

    print("Example 2 and cards stat-ps-mean-estimation-years, stat-ps-vol-estimation-se")
    approx("years for a 2% SE on the mean", (16 / 2) ** 2, 64, 6)
    approx("se of vol from one year (%)", 16 / math.sqrt(504), 0.71, 2)
    approx("se of vol from one year (%), card", 16 / math.sqrt(504), 0.7, 1)

    print("Example 3 and card stat-ps-bayes-discovery-rate")
    real_pass, null_pass = 100 * Fraction(1, 2), 900 * Fraction(5, 100)
    approx("real passes", float(real_pass), 50, 6)
    approx("null passes", float(null_pass), 45, 6)
    ppv = real_pass / (real_pass + null_pass)
    approx("P(real | significant)", float(ppv), 0.526, 3)
    approx("P(real | significant) (%)", 100 * float(ppv), 53, 0)
    approx("share of discoveries that are false (%)", 100 * float(1 - ppv), 47, 0)
    approx("5% real, 30% power: 15/(15 + 47.5)", 15 / (15 + 47.5), 0.24, 10)

    print("Example 4 and cards stat-ps-omitted-variable, stat-ps-errors-in-variables")
    n = 400000
    x1 = rng.standard_normal(n)
    x2 = 0.6 * x1 + rng.standard_normal(n)
    y = 1.0 * x1 + 0.5 * x2 + rng.standard_normal(n)
    simulated("short-regression slope", ols_slope(x1, y), 1.3, 0.01)
    approx("overstatement (%)", 100 * 0.5 * 0.6 / 1.0, 30, 6)
    x_obs = x1 + math.sqrt(0.5) * rng.standard_normal(n)
    simulated("slope with noise variance half the regressor's", ols_slope(x_obs, 1.0 * x1 + rng.standard_normal(n)), 0.67, 0.01)
    approx("1/1.5", 1 / 1.5, 0.67, 2)

    print("Example 5 and card stat-ps-sharpe-autocorrelation: Lo (2002) with AR(1) monthly returns")
    rho, sr = 0.2, 0.3
    factor = 12 / math.sqrt(12 + 2 * sum((12 - k) * rho**k for k in range(1, 12)))
    approx("Lo factor", factor, 2.88, 2)
    approx("adjusted annual Sharpe", sr * factor, 0.86, 2)
    approx("naive 0.3 sqrt(12)", sr * math.sqrt(12), 1.04, 2)
    approx("overstatement (%)", 100 * (math.sqrt(12) / factor - 1), 20, 0)
    years, burn = 200000, 50
    eps = rng.standard_normal((years, 12 + burn))
    m = np.zeros_like(eps)
    for t in range(1, 12 + burn):
        m[:, t] = rho * m[:, t - 1] + eps[:, t]
    monthly = m[:, burn:] * math.sqrt(1 - rho**2) + sr  # unit-variance monthly returns with Sharpe 0.3
    annual = monthly.sum(axis=1)
    simulated("annual Sharpe of simulated AR(1) monthly returns", float(annual.mean() / annual.std()), 0.86, 0.01)

    print("Example 6 and cards stat-ps-flaw-best-of-200, stat-ps-bonferroni-threshold, stat-ps-flaw-overlapping-daily")
    p = 2 * (1 - N01.cdf(3.1))
    approx("two-sided p at t = 3.1", p, 0.0019, 4)
    approx("two-sided p at t = 3.1 (five decimals)", p, 0.00194, 5)
    approx("Bonferroni-adjusted 200 p", 200 * p, 0.39, 2)
    approx("per-test p threshold 0.05/200", 0.05 / 200, 0.00025, 6)
    approx("per-test |t| threshold", N01.inv_cdf(1 - 0.05 / 400), 3.66, 2)
    approx("sqrt(20)", math.sqrt(20), 4.5, 1)
    approx("honest t near 3.1/sqrt(20)", 3.1 / math.sqrt(20), 0.7, 1)
    reps, days, h = 1000, 3000, 20
    tstats = np.empty(reps)
    for i in range(reps):
        r = rng.standard_normal(days + h)
        sig = np.zeros(days)
        e = rng.standard_normal(days)
        for t in range(1, days):
            sig[t] = 0.99 * sig[t - 1] + e[t]
        fwd = np.convolve(r, np.ones(h), mode="valid")[1 : days + 1]  # sum of the next 20 returns
        sc = sig - sig.mean()
        b = sc @ (fwd - fwd.mean()) / (sc @ sc)
        res = fwd - fwd.mean() - b * sc
        tstats[i] = b / math.sqrt(res @ res / (days - 2) / (sc @ sc))
    sd_t = float(tstats.std())
    simulated("sd of the naive OLS t-stat under no predictability (signal AR(1) 0.99)", sd_t, 4.3, 4 * sd_t / math.sqrt(2 * reps) + 0.05)


def card_numbers() -> None:
    print("Cards: confidence intervals")
    z = N01.inv_cdf(0.975)
    n_poll = (z * 0.5 / 0.03) ** 2
    approx("poll n unrounded", n_poll, 1067.1, 1)
    assert math.ceil(n_poll) == 1068
    srd = 1.5 / math.sqrt(252)
    se = math.sqrt((1 + srd**2 / 2) / 1008) * math.sqrt(252)
    approx("Lo SE, Sharpe 1.5 over four years", se, 0.501, 3)
    approx("lower", 1.5 - z * se, 0.5, 1)
    approx("upper", 1.5 + z * se, 2.5, 1)
    approx("-ln(0.05)/100 (%)", -math.log(0.05), 3.0, 1)
    lo_q, hi_q = chi2_ppf(0.025, 29), chi2_ppf(0.975, 29)
    approx("chi2_{29, 0.025}", lo_q, 16.05, 2)
    approx("chi2_{29, 0.975}", hi_q, 45.72, 2)
    approx("variance CI lower factor", 29 / hi_q, 0.63, 2)
    approx("variance CI upper factor", 29 / lo_q, 1.81, 2)

    print("Cards: hypothesis testing")
    approx("coin z", (60 - 50) / 5, 2.0, 10)
    approx("coin two-sided normal p", 2 * (1 - N01.cdf(2.0)), 0.046, 3)
    tail = Fraction(sum(math.comb(100, k) for k in range(60, 101)), 2**100)
    approx("coin exact two-sided binomial p", float(2 * tail), 0.057, 3)
    approx("P(at least one of 100 false positives)", 1 - 0.95**100, 0.994, 3)
    approx("expected false positives", 100 * 0.05, 5, 10)
    approx("0.05/0.095", 0.05 / 0.095, 0.526, 3)

    print("Cards: regression")
    approx("slope rho sigma_y/sigma_x", 0.5 * 2 / 1, 1.0, 10)
    approx("R^2 = rho^2", 0.5**2, 0.25, 10)
    approx("rho^2 from slopes 0.5 and 1.2", 0.5 * 1.2, 0.6, 10)
    approx("|rho|", math.sqrt(0.6), 0.77, 2)
    approx("t from R^2 = 1%, n = 252", math.sqrt(250 * 0.01 / 0.99), 1.59, 2)
    n_needed = 2 + (2 * math.sqrt(1 - 0.01) / 0.1) ** 2
    approx("n for t = 2 at correlation 0.1", n_needed, 398, 0)
    approx("VIF at correlation 0.9", 1 / (1 - 0.81), 5.3, 1)
    approx("t inflation from duplicated rows (large n)", math.sqrt(2), 1.41, 2)

    print("Cards: time series and volatility")
    approx("half-life ln 0.5/ln 0.9 (weeks)", math.log(0.5) / math.log(0.9), 6.58, 2)
    approx("half-life (one decimal)", math.log(0.5) / math.log(0.9), 6.6, 1)
    v = 0.0
    for _ in range(20000):
        v = 1e-6 + 0.95 * v  # fixed point of the GARCH variance recursion
    approx("GARCH long-run variance (x1e5)", v * 1e5, 2.0, 6)
    approx("long-run daily vol (%)", 100 * math.sqrt(v), 0.447, 3)
    approx("long-run annual vol (%)", 100 * math.sqrt(252 * v), 7.1, 1)
    approx("half-life ln 0.5/ln 0.95", math.log(0.5) / math.log(0.95), 13.5, 1)
    s2 = 0.94 * 0.02**2 + 0.06 * 0.05**2
    approx("EWMA variance", s2, 0.000526, 6)
    approx("EWMA vol (%)", 100 * math.sqrt(s2), 2.29, 2)

    print("Cards: bootstrap and permutation")
    approx("inclusion probability, n = 1000", 1 - 0.999**1000, 0.632, 3)
    approx("permutation p with 1999 permutations", 1 / 2000, 0.0005, 6)


def main() -> None:
    rng = np.random.default_rng(SEED)
    numbers_table(rng)
    worked_examples(rng)
    card_numbers()
    print("all problem-set checks passed")


if __name__ == "__main__":
    main()
