"""Backtest overfitting and multiple testing: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/60-Systems/04-Backtest-Overfitting-and-Multiple-Testing.md`.
Independent routes used here:
- the inverse normal CDF by bisection on ``math.erfc``, cross-checked against ``statistics.NormalDist``;
- the expected maximum of N standard normals by numerical integration of x n phi(x) Phi(x)^(n-1), against
  which the Bailey-Lopez de Prado approximation is compared (the note quotes the approximation);
- the expected best null Sharpe ratio by seeded simulation of N skill-less strategies, drawing each
  sample Sharpe ratio exactly from its (mean, standard deviation) sampling distribution, against the
  expected maximum of N Student-t(T-1) variables by numerical integration;
- the Mertens (2002) variance of the Sharpe estimator by seeded simulation of skewed, fat-tailed returns;
- the Bonferroni haircut, MinBTL and BHY constant by direct arithmetic on the stated inputs.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 16-Trading-and-Investing/code/mkt_sys_04_overfitting.py`.
"""

from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np

SEED = 20261114
EULER_GAMMA = 0.5772156649015329


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, expected {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.5f} (expected {expected:.5f}, tolerance {tol:.2g})")


def norm_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def norm_ppf(p: float) -> float:
    """Inverse normal CDF by bisection on erfc; independent of statistics.NormalDist."""
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    x = 0.5 * (lo + hi)
    assert abs(x - NormalDist().inv_cdf(p)) < 1e-9
    return x


def bracket(n: int) -> float:
    """(1 - gamma) Phi^-1(1 - 1/N) + gamma Phi^-1(1 - 1/(N e)), Bailey and Lopez de Prado (2014)."""
    return (1 - EULER_GAMMA) * norm_ppf(1 - 1 / n) + EULER_GAMMA * norm_ppf(1 - 1 / (n * math.e))


def exact_expected_max(n: int) -> float:
    """E[max of n iid N(0,1)] by trapezoidal integration of x * n phi(x) Phi(x)^(n-1)."""
    x = np.linspace(-12.0, 12.0, 240_001)
    phi = np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
    cdf = 0.5 * np.array([math.erfc(-v / math.sqrt(2.0)) for v in x[::100]])
    cdf = np.interp(x, x[::100], cdf)
    f = x * n * phi * cdf ** (n - 1)
    return float(np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(x)))


def expected_max_t(n: int, df: int) -> float:
    """E[max of n iid Student-t(df)] by trapezoidal integration, the CDF built by cumulating the density."""
    x = np.linspace(-14.0, 14.0, 280_001)
    log_c = math.lgamma((df + 1) / 2) - math.lgamma(df / 2) - 0.5 * math.log(df * math.pi)
    pdf = np.exp(log_c - (df + 1) / 2 * np.log1p(x * x / df))
    cdf = np.concatenate([[0.0], np.cumsum(0.5 * (pdf[1:] + pdf[:-1]) * np.diff(x))])
    assert abs(cdf[-1] - 1.0) < 1e-9, cdf[-1]
    f = x * n * pdf * cdf ** (n - 1)
    return float(np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(x)))


def null_max_sharpe(rng: np.random.Generator, n_trials: int, t_days: int, reps: int) -> np.ndarray:
    """Max of n_trials sample daily Sharpe ratios of iid N(0,1) returns, drawn exactly.

    The sample mean is N(0, 1/T) and the sample variance is chi2(T-1)/(T-1), independent (normal theory),
    so the sample Sharpe ratio is drawn without generating T returns per trial; sqrt(T) times it is Student-t(T-1).
    """
    mean = rng.standard_normal((reps, n_trials)) / math.sqrt(t_days)
    sd = np.sqrt(rng.chisquare(t_days - 1, size=(reps, n_trials)) / (t_days - 1))
    return (mean / sd).max(axis=1)


def expected_max(rng: np.random.Generator) -> None:
    print("Expected maximum of N null trials (Core concepts 1, TL;DR, cards mkt-sys-098, mkt-sys-109)")
    approx("Euler-Mascheroni gamma, limit of H_n - ln n at n = 10^7", sum(1 / j for j in range(1, 10**7 + 1)) - math.log(10**7), 0.57722, 5)
    approx("Euler-Mascheroni gamma (four decimals)", EULER_GAMMA, 0.5772, 4)
    quoted = {10: 1.57, 100: 2.53, 1000: 3.26, 10000: 3.86}
    exact = {10: 1.54, 100: 2.51, 1000: 3.24, 10000: 3.85}
    for n, q in quoted.items():
        approx(f"approximation, N = {n}", bracket(n), q, 2)
        approx(f"exact E[max Z], N = {n}", exact_expected_max(n), exact[n], 2)
    approx("sqrt(2 ln N), N = 1000", math.sqrt(2 * math.log(1000)), 3.72, 2)

    se_ann = math.sqrt(252 / (5 * 252))
    approx("standard error of an annualized Sharpe over 5 years, 1/sqrt(5)", se_ann, 0.447, 3)
    approx("expected best annualized null Sharpe, 3.26 / sqrt(5)", bracket(1000) * se_ann, 1.46, 2)
    reps = 4000
    best = null_max_sharpe(rng, 1000, 1260, reps) * math.sqrt(252)
    se = float(best.std(ddof=1)) / math.sqrt(reps)
    simulated(
        "simulated best of 1000 null strategies over 1260 days, annualized",
        float(best.mean()),
        expected_max_t(1000, 1259) * se_ann,
        4 * se,
    )
    print(f"    (seed {SEED}, {reps} replications, standard error {se:.4f}; expected value is E[max of 1000 Student-t(1259)] / sqrt(5))")


def mertens_variance(rng: np.random.Generator) -> None:
    print("Variance of the Sharpe estimator (Core concepts 2, cards mkt-sys-100, mkt-sys-101)")
    # Returns r = mu - (G - k)/sqrt(k), G ~ Gamma(k, 1): unit variance, skewness -2/sqrt(k), kurtosis 3 + 6/k.
    k, mu, t_days, reps = 16.0, 0.10, 1260, 4000
    skew, kurt = -2 / math.sqrt(k), 3 + 6 / k
    approx("skewness of the simulated return law", skew, -0.50, 2)
    approx("kurtosis of the simulated return law", kurt, 3.375, 3)
    srs = np.empty(reps)
    for i in range(reps):
        r = mu - (rng.gamma(k, 1.0, size=t_days) - k) / math.sqrt(k)
        srs[i] = r.mean() / r.std(ddof=1)
    var_sim = float(srs.var(ddof=1))
    var_formula = (1 - skew * mu + (kurt - 1) / 4 * mu * mu) / (t_days - 1)
    # The sample variance of reps draws has relative standard error about sqrt(2/(reps-1)).
    rel_se = math.sqrt(2 / (reps - 1))
    simulated("simulated Var(SR_hat) / Mertens formula", var_sim / var_formula, 1.0, 4 * rel_se)


def dsr_example(rng: np.random.Generator) -> None:
    print("Example 1: Deflated Sharpe ratio for a 200-trial grid search (cards mkt-sys-103, mkt-sys-104)")
    t_days, n = 1260, 200
    sr_d = 1.60 / math.sqrt(252)
    approx("daily Sharpe 1.60/sqrt(252)", sr_d, 0.10079, 5)
    v = 1 / (t_days - 1)
    approx("null cross-trial variance V = 1/1259", v, 0.0007943, 7)
    approx("sqrt(V)", math.sqrt(v), 0.028183, 6)
    approx("Phi^-1(0.995)", norm_ppf(1 - 1 / n), 2.5758, 4)
    approx("1/(200 e)", 1 / (n * math.e), 0.001839, 6)
    approx("Phi^-1(1 - 1/(200 e))", norm_ppf(1 - 1 / (n * math.e)), 2.9045, 4)
    approx("(1 - gamma) x 2.5758", (1 - EULER_GAMMA) * norm_ppf(1 - 1 / n), 1.0890, 4)
    approx("gamma x 2.9045", EULER_GAMMA * norm_ppf(1 - 1 / (n * math.e)), 1.6765, 4)
    b = bracket(n)
    approx("bracket", b, 2.7655, 4)
    sr0 = math.sqrt(v) * b
    approx("SR_0 daily", sr0, 0.07794, 5)
    approx("SR_0 annualized", sr0 * math.sqrt(252), 1.237, 3)
    skew, kurt = -0.50, 4.50
    approx("-skew x SR", -skew * sr_d, 0.0504, 4)
    approx("(kurt - 1)/4 x SR^2", (kurt - 1) / 4 * sr_d**2, 0.0089, 4)
    num = 1 - skew * sr_d + (kurt - 1) / 4 * sr_d**2
    approx("numerator", num, 1.0593, 4)
    approx("Var(SR_hat)", num / (t_days - 1), 0.0008414, 7)
    sig = math.sqrt(num / (t_days - 1))
    approx("sigma(SR_hat)", sig, 0.02901, 5)
    approx("SR_hat - SR_0", sr_d - sr0, 0.02285, 5)
    z = (sr_d - sr0) / sig
    approx("z", z, 0.788, 3)
    dsr = norm_cdf(z)
    approx("DSR (percent)", 100 * dsr, 78.5, 1)
    approx("1 - DSR (percent)", 100 * (1 - dsr), 21.5, 1)
    # Interpretation check: SR_0 approximates the expected best daily Sharpe of 200 skill-less trials.
    normal_best = exact_expected_max(n) * math.sqrt(v)
    approx("normal-approximation expected best daily Sharpe of 200 null trials, sqrt(V) E[max Z]", normal_best, 0.0774, 4)
    reps = 6000
    best = null_max_sharpe(rng, n, t_days, reps)
    se = float(best.std(ddof=1)) / math.sqrt(reps)
    expected_best = expected_max_t(n, t_days - 1) / math.sqrt(t_days)
    approx("exact expected best daily Sharpe of 200 null trials, E[max t_1259] / sqrt(1260)", expected_best, 0.0775, 4)
    simulated("simulated best daily Sharpe of 200 null trials", float(best.mean()), expected_best, 4 * se)
    approx("approximation error of the bracket vs exact E[max Z] (percent)", 100 * (b / exact_expected_max(n) - 1), 0.7, 1)


def haircut_example() -> None:
    print("Example 2: Bonferroni haircut (cards mkt-sys-105, mkt-sys-106, mkt-sys-118, mkt-sys-119)")
    t = 1.20 * math.sqrt(4.0)
    approx("t = 1.20 x sqrt(4)", t, 2.40, 2)
    approx("Phi(2.40)", norm_cdf(t), 0.9918, 4)
    p = 2 * (1 - norm_cdf(t))
    approx("two-sided p", p, 0.0164, 4)
    pb = min(1.0, 50 * p)
    approx("Bonferroni p", pb, 0.820, 3)
    approx("1 - p_Bonf/2", 1 - pb / 2, 0.590, 3)
    tb = norm_ppf(1 - pb / 2)
    approx("adjusted t", tb, 0.228, 3)
    approx("adjusted t (two decimals)", tb, 0.23, 2)
    srb = tb / 2
    approx("adjusted Sharpe", srb, 0.114, 3)
    approx("adjusted Sharpe (two decimals)", srb, 0.11, 2)
    approx("haircut (percent)", 100 * (1 - srb / 1.20), 90.5, 1)
    approx("two-sided p at t = 3.0", 2 * (1 - norm_cdf(3.0)), 0.0027, 4)
    approx("two-sided p at t = 2.0", 2 * (1 - norm_cdf(2.0)), 0.0455, 4)
    approx("two-sided 5% critical value", norm_ppf(0.975), 1.96, 2)
    approx("BHY constant c(50) = sum 1/j", sum(1 / j for j in range(1, 51)), 4.4992, 4)
    approx("BHY bound for the most significant of 50, 50 c(50) p", 50 * sum(1 / j for j in range(1, 51)) * p, 3.69, 2)


def minbtl() -> None:
    print("Minimum backtest length (Core concepts 5, cards mkt-sys-108, mkt-sys-259)")
    approx("bracket at N = 100", bracket(100), 2.53, 2)
    approx("MinBTL at N = 100, SR = 1 (years)", bracket(100) ** 2, 6.4, 1)
    approx("bracket at N = 45", bracket(45), 2.236, 3)
    approx("MinBTL at N = 45, SR = 1 (years)", bracket(45) ** 2, 5.0, 1)
    approx("upper bound 2 ln N at N = 100 (years)", 2 * math.log(100), 9.2, 1)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    expected_max(rng)
    mertens_variance(rng)
    dsr_example(rng)
    haircut_example()
    minbtl()
    print("all backtest-overfitting numbers check out")
