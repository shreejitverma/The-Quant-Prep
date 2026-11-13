"""Confidence intervals and sampling: every quantile, interval and sample size in the note.

Backs every number in `02-Statistics-and-Econometrics/02-Confidence-Intervals-and-Sampling.md`.
Independent routes used here:
- Student-t and chi-square quantiles by Simpson quadrature of the density and bisection, never quoted from a table;
- the chi-square quantiles cross-checked by simulating sums of squared normals;
- the Sharpe-ratio standard error (Lo and Mertens) against seeded simulations of normal and skewed returns;
- the AR(1) variance inflation against the exact finite-sample variance of the mean from the autocovariances;
- coverage claims (fat tails break the chi-square interval) by seeded simulation, changing only the return law.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 02-Statistics-and-Econometrics/code/stats_02_confidence_intervals.py`.
"""

from __future__ import annotations

import math
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


def simpson(f, a: float, b: float, n: int = 4000) -> float:
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return float((b - a) / (3 * n) * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))


def t_cdf(x: float, df: float) -> float:
    c = math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(df * math.pi)
    half = simpson(lambda t: c * (1 + t * t / df) ** (-(df + 1) / 2), 0.0, abs(x))
    return 0.5 + math.copysign(half, x)


def chi2_cdf(x: float, k: int) -> float:
    c = 1.0 / (2 ** (k / 2) * math.gamma(k / 2))
    return simpson(lambda u: c * u ** (k / 2 - 1) * np.exp(-u / 2), 0.0, x, 20000)


def bisect(f, lo: float, hi: float, target: float) -> float:
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def t_ppf(p: float, df: float) -> float:
    return bisect(lambda x: t_cdf(x, df), -50.0, 50.0, p)


def chi2_ppf(p: float, k: int) -> float:
    return bisect(lambda x: chi2_cdf(x, k), 1e-9, 400.0, p)


def sharpe_se_sim(rng: np.random.Generator, draw, n: int, paths: int) -> float:
    r = draw(rng, (paths, n))
    sr = r.mean(axis=1) / r.std(axis=1, ddof=1)
    return float(sr.std())


def distributions() -> None:
    print("Core concepts: t, chi-square and rule of three (cards stat-ci-t-distribution-origin, stat-ci-rule-of-three)")
    t59 = t_ppf(0.975, 59)
    approx("t_{59, 0.975}", t59, 2.001, 3)
    approx("t_{59, 0.975} (card)", t59, 2.00, 2)
    approx("z_{0.975}", N01.inv_cdf(0.975), 1.96, 2)
    c5 = 8 / (3 * math.pi * math.sqrt(5))  # t_5 density constant
    var_t5 = 2 * simpson(lambda t: t * t * c5 * (1 + t * t / 5) ** -3, 0, 2000, 400000)
    approx("Var(t_5) = k/(k-2) by quadrature of t^2 f(t)", var_t5, 5 / 3, 4)
    approx("-ln(0.05), the rule-of-three constant", -math.log(0.05), 3.0, 1)
    approx("exact bound 1 - 0.05^(1/100) (%)", 100 * (1 - 0.05 ** (1 / 100)), 2.95, 2)


def sharpe_formulas(rng: np.random.Generator) -> None:
    print("Sharpe ratio standard errors (Lo 2002, Mertens 2002) against simulation; card stat-ci-sharpe-skew-kurtosis")
    sr, n, paths = 0.1, 252, 40000
    normal = sharpe_se_sim(rng, lambda g, s: sr + g.standard_normal(s), n, paths)
    lo = math.sqrt((1 + sr**2 / 2) / n)
    simulated("normal returns: sd of SR_hat vs Lo sqrt((1 + SR^2/2)/n)", normal, lo, 4 * lo / math.sqrt(2 * paths))
    # negatively skewed returns: 1 - Exp(1) has mean 0, variance 1, skewness -2, kurtosis 9
    skewed = sharpe_se_sim(rng, lambda g, s: sr + 1.0 - g.exponential(1.0, s), n, paths)
    mertens = math.sqrt((1 - (-2) * sr + (9 - 1) / 4 * sr**2) / n)
    simulated("skew -2, kurtosis 9: sd of SR_hat vs Mertens", skewed, mertens, 6 * mertens / math.sqrt(2 * paths))
    approx("Mertens variance factor 1 + 2(0.1) + 2(0.01)", 1 - (-2) * sr + (9 - 1) / 4 * sr**2, 1.22, 10)
    approx("SE ratio skewed/normal sqrt(1.22/1.005)", mertens / lo, 1.10, 2)
    # Lo's autocorrelation correction is Var(sum of q returns) = sigma^2 (q + 2 sum (q-k) rho_k)
    q, rho = 12, 0.2
    cov = rho ** np.abs(np.subtract.outer(np.arange(q), np.arange(q)))
    lo_denominator = q + 2 * sum((q - k) * rho**k for k in range(1, q))
    approx("Var of 12-period sum from the AR(1) covariance matrix vs Lo's denominator", float(cov.sum()), lo_denominator, 10)


def sample_size() -> None:
    print("Sample size for an edge, Example 3 table, card stat-ci-years-to-detect-sharpe")
    zsum = N01.inv_cdf(0.975) + N01.inv_cdf(0.8)
    approx("z_0.8", N01.inv_cdf(0.8), 0.8416, 4)
    approx("z_0.975 + z_0.8", zsum, 2.80, 2)
    approx("(z_0.975 + z_0.8)^2, years at Sharpe 1", zsum**2, 7.85, 2)
    for s, t2, pw, dec in ((2.0, 1, 1.96, 2), (1.0, 4, 7.85, 2), (0.5, 16, 31.4, 1)):
        approx(f"Sharpe {s}: years for t = 2", (2 / s) ** 2, t2, 6)
        approx(f"Sharpe {s}: years for 80% power", (zsum / s) ** 2, pw, dec)
    approx("Sharpe 5: years for t = 2", (2 / 5) ** 2, 0.16, 6)
    approx("Sharpe 5: trading days for t = 2", 252 * (2 / 5) ** 2, 40, 0)
    print("AR(1) effective sample size (card stat-ci-effective-sample-size-ar1)")
    rho, n = 0.3, 1000
    approx("(1 + rho)/(1 - rho)", (1 + rho) / (1 - rho), 1.857, 3)
    approx("n_eff = 1000 / 1.857", n * (1 - rho) / (1 + rho), 538, 0)
    k = np.arange(1, n)
    exact_factor = 1 + 2 * float(np.sum((1 - k / n) * rho**k))
    approx("exact finite-n factor n Var(mean)/gamma_0 at n = 1000", exact_factor, 1.856, 3)


def examples(rng: np.random.Generator) -> None:
    print("Example 1 and card stat-ci-monthly-mean-return")
    se = 4 / math.sqrt(60)
    t59 = t_ppf(0.975, 59)
    approx("SE = 4/sqrt(60) (%)", se, 0.516, 3)
    approx("lower (%)", 1.0 - t59 * se, -0.03, 2)
    approx("upper (%)", 1.0 + t59 * se, 2.03, 2)
    approx("t-stat", 1.0 / se, 1.94, 2)
    approx("annualised Sharpe 0.25 sqrt(12)", 0.25 * math.sqrt(12), 0.866, 3)
    approx("annualised Sharpe (two decimals)", 0.25 * math.sqrt(12), 0.87, 2)
    approx("0.866 sqrt(5)", 0.25 * math.sqrt(12) * math.sqrt(5), 1.94, 2)
    approx("two-sided p from t_59", 2 * (1 - t_cdf(1.0 / se, 59)), 0.058, 3)

    print("Example 2 and card stat-ci-sharpe-three-years")
    srd, n = 1.5 / math.sqrt(252), 756
    se_d = math.sqrt((1 + srd**2 / 2) / n)
    se_a = se_d * math.sqrt(252)
    approx("daily Sharpe", srd, 0.0945, 4)
    approx("SE daily", se_d, 0.03645, 5)
    approx("SE annualised", se_a, 0.579, 3)
    approx("SE annualised (card)", se_a, 0.58, 2)
    approx("lower", 1.5 - N01.inv_cdf(0.975) * se_a, 0.37, 2)
    approx("upper", 1.5 + N01.inv_cdf(0.975) * se_a, 2.63, 2)
    approx("shortcut 1/sqrt(3)", 1 / math.sqrt(3), 0.577, 3)
    paths = 20000
    sd = sharpe_se_sim(rng, lambda g, s: srd + g.standard_normal(s), n, paths) * math.sqrt(252)
    simulated("sd of annualised Sharpe over 20,000 simulated three-year paths", sd, 0.58, 3 * sd / math.sqrt(2 * paths))

    print("Example 4 and card stat-ci-win-rate-trades-needed")
    se = math.sqrt(0.55 * 0.45 / 400)
    z = N01.inv_cdf(0.975)
    approx("SE of the win rate", se, 0.0249, 4)
    approx("lower", 0.55 - z * se, 0.501, 3)
    approx("upper", 0.55 + z * se, 0.599, 3)
    approx("z against 50%", 0.05 / math.sqrt(0.25 / 400), 2.0, 6)
    n_obs = (z * 0.5 / 0.02) ** 2
    approx("n for z = 1.96 at 52%", n_obs, 2401, 0)
    approx("n for z = 1.96 at 52%, to the nearest hundred", round(n_obs, -2), 2400, 0)
    n_pow = ((z * 0.5 + N01.inv_cdf(0.8) * math.sqrt(0.52 * 0.48)) / 0.02) ** 2
    approx("n for 80% power (unrounded)", n_pow, 4903.2, 1)
    approx("n for 80% power, to the nearest hundred", round(n_pow, -2), 4900, 0)
    assert math.ceil(n_pow) == 4904
    print("    n for 80% power rounded up = 4904")

    print("Example 5 and cards stat-ci-chi-squared-variance-interval")
    lo_q, hi_q = chi2_ppf(0.025, 29), chi2_ppf(0.975, 29)
    approx("chi2_{29, 0.025}", lo_q, 16.05, 2)
    approx("chi2_{29, 0.975}", hi_q, 45.72, 2)
    sims = (rng.standard_normal((200000, 29)) ** 2).sum(axis=1)
    simulated("simulated 2.5% quantile of a sum of 29 squared normals", float(np.quantile(sims, 0.025)), 16.05, 0.15)
    simulated("simulated 97.5% quantile", float(np.quantile(sims, 0.975)), 45.72, 0.3)
    approx("sigma lower (%)", 2 * math.sqrt(29 / hi_q), 1.59, 2)
    approx("sigma upper (%)", 2 * math.sqrt(29 / lo_q), 2.69, 2)
    approx("variance interval factor 29/45.72", 29 / hi_q, 0.63, 2)
    approx("variance interval factor 29/16.05", 29 / lo_q, 1.81, 2)
    # coverage: change only the return law, normal versus Student-t with 5 degrees of freedom (scaled to unit variance)
    reps, n = 100000, 30

    def coverage(x: np.ndarray) -> float:
        s2 = x.var(axis=1, ddof=1)
        return float(np.mean(((n - 1) * s2 / hi_q <= 1.0) & ((n - 1) * s2 / lo_q >= 1.0)))

    cov_norm = coverage(rng.standard_normal((reps, n)))
    cov_t5 = coverage(rng.standard_t(5, (reps, n)) / math.sqrt(5 / 3))
    se_cov = math.sqrt(0.95 * 0.05 / reps)
    simulated("coverage of the 95% chi-square interval, normal returns", cov_norm, 0.95, 4 * se_cov)
    simulated("coverage of the same interval, Student-t(5) returns", cov_t5, 0.83, 4 * se_cov + 0.005)
    assert cov_t5 < cov_norm - 0.1


def main() -> None:
    rng = np.random.default_rng(SEED)
    distributions()
    sharpe_formulas(rng)
    sample_size()
    examples(rng)
    print("all confidence-interval checks passed")


if __name__ == "__main__":
    main()
