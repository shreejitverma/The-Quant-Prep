"""Estimation, MLE and method of moments: every number in the note, checked by an independent route.

Backs every number in `02-Statistics-and-Econometrics/01-Estimation-MLE-and-Method-of-Moments.md`.
Independent routes used here:
- Fisher information as the variance of the score, by exact summation over the pmf (Bernoulli, Poisson)
  or by quadrature over the density (exponential, normal), never from the table's closed forms;
- uniform(0, theta) moments by exact polynomial integration with `fractions.Fraction`, and a seeded simulation;
- the variance-divisor table by exact rational arithmetic on chi-square moments, a grid search for the
  minimiser, and a seeded simulation;
- the German tank estimator by summing the exact law of the maximum over every possible maximum;
- the exponential-rate bias by quadrature of the Gamma density, and the volatility standard error by simulation.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 02-Statistics-and-Econometrics/code/stats_01_estimation.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction
from statistics import NormalDist

import numpy as np

SEED = 20261112
Z975 = NormalDist().inv_cdf(0.975)


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.5f} (quoted {expected}, tolerance {tol:.5f})")


def simpson(f, a: float, b: float, n: int = 20000) -> float:
    """Composite Simpson rule with an even number of panels."""
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return float((b - a) / (3 * n) * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))


def fisher_information() -> None:
    print("Fisher information table, as Var(score) by summation or quadrature (Core concepts table)")
    p = 0.3
    score_1, score_0 = 1 / p, -1 / (1 - p)  # d/dp log p^x (1-p)^(1-x)
    var_bern = p * score_1**2 + (1 - p) * score_0**2
    approx("I_1 Bernoulli(0.3) = 1/(p(1-p))", var_bern, 1 / (p * (1 - p)), 10)
    lam = 2.5
    ks = np.arange(0, 80)
    pmf = np.exp(ks * math.log(lam) - lam - np.array([math.lgamma(k + 1) for k in ks]))
    var_pois = float(np.sum(pmf * (ks / lam - 1) ** 2))
    approx("I_1 Poisson(2.5) = 1/lambda", var_pois, 1 / lam, 10)
    rate = 0.4
    var_exp = simpson(lambda x: rate * np.exp(-rate * x) * (1 / rate - x) ** 2, 0.0, 200.0)
    approx("I_1 Exponential(rate 0.4) = 1/lambda^2", var_exp, 1 / rate**2, 6)
    mu, s2 = 0.0, 4.0
    dens = NormalDist(mu, math.sqrt(s2)).pdf
    pdf = np.vectorize(dens)
    var_mu = simpson(lambda x: pdf(x) * ((x - mu) / s2) ** 2, -40.0, 40.0)
    var_s2 = simpson(lambda x: pdf(x) * (-1 / (2 * s2) + (x - mu) ** 2 / (2 * s2**2)) ** 2, -40.0, 40.0)
    approx("I_1 Normal mu (sigma^2 = 4) = 1/sigma^2", var_mu, 1 / s2, 8)
    approx("I_1 Normal sigma^2 (sigma^2 = 4) = 1/(2 sigma^4)", var_s2, 1 / (2 * s2**2), 8)


def exponential_rate(rng: np.random.Generator) -> None:
    print("Example 1 and card stat-mle-exponential-rate-estimate: exponential inter-trade times")
    n, xbar = 100, 2.5
    lam_hat = 1 / xbar
    se = lam_hat / math.sqrt(n)
    approx("lambda_hat", lam_hat, 0.4, 10)
    approx("SE = lambda_hat / sqrt(n)", se, 0.04, 10)
    approx("z_0.975", Z975, 1.96, 2)
    approx("Wald lower 0.4 - z se", lam_hat - Z975 * se, 0.322, 3)
    approx("Wald upper 0.4 + z se", lam_hat + Z975 * se, 0.478, 3)
    approx("unbiased (n-1)/(n xbar)", (n - 1) / (n * xbar), 0.396, 3)
    # E[1/xbar] by quadrature: n*xbar ~ Gamma(n, rate), so E[n / S] with S ~ Gamma(n, lambda=1)
    lg = math.lgamma(n)
    e_inv = simpson(lambda s: n / s * np.exp((n - 1) * np.log(s) - s - lg), 1e-9, 400.0, 200000)
    approx("E[1/xbar] / lambda by quadrature = n/(n-1)", e_inv, n / (n - 1), 8)
    sims = rng.exponential(1.0, size=(200000, 10)).mean(axis=1)
    var_mean = float(sims.var())
    se_var = var_mean * math.sqrt(2 / len(sims))
    simulated("Var(xbar) for n = 10, rate 1, equals the CR bound 1/(n lambda^2)", var_mean, 0.1, 4 * se_var)


def uniform_theta(rng: np.random.Generator) -> None:
    print("Example 2 and cards stat-mle-uniform-max-bias, stat-mle-uniform-mom-vs-mle-variance: uniform(0, theta)")
    n = 10
    # E[U] and E[U^2] for U ~ uniform(0,1) by integrating x and x^2 exactly
    var_u = Fraction(1, 3) - Fraction(1, 2) ** 2
    var_mom = 4 * var_u / n
    exact("Var(2 Xbar)", var_mom, Fraction(1, 30))
    approx("Var(2 Xbar)", float(var_mom), 0.0333, 4)
    # density of M is n m^(n-1) on [0,1]: integrate m^k against it exactly
    e_m = Fraction(n, n + 1)  # int n m^n dm
    e_m2 = Fraction(n, n + 2)  # int n m^(n+1) dm
    mse_m = e_m2 - 2 * e_m + 1
    exact("MSE(M) = E[(M-1)^2]", mse_m, Fraction(1, 121) + Fraction(10, 121 * 12))
    exact("MSE(M) = 2/((n+1)(n+2))", mse_m, Fraction(2, (n + 1) * (n + 2)))
    approx("MSE(M)", float(mse_m), 0.0152, 4)
    c = Fraction(n + 1, n)
    var_corr = c**2 * (e_m2 - e_m**2)
    exact("Var((n+1)/n M) = 1/(n(n+2))", var_corr, Fraction(1, n * (n + 2)))
    approx("Var((n+1)/n M)", float(var_corr), 0.0083, 4)
    exact("ratio Var(2 Xbar) / Var((n+1)/n M) = (n+2)/3", var_mom / var_corr, Fraction(n + 2, 3))
    exact("ratio at n = 10", var_mom / var_corr, Fraction(4))
    u = rng.random((400000, n))
    est = {"2 Xbar": 2 * u.mean(axis=1), "M": u.max(axis=1), "(n+1)/n M": (n + 1) / n * u.max(axis=1)}
    for (name, x), quoted in zip(est.items(), (1 / 30, 2 / 132, 1 / 120), strict=True):
        sq = (x - 1.0) ** 2
        mse, se = float(sq.mean()), float(sq.std() / math.sqrt(len(sq)))
        simulated(f"simulated MSE of {name}, 400,000 samples", mse, quoted, 3 * se)


def variance_divisor(rng: np.random.Generator) -> None:
    print("Example 3 and card stat-mle-normal-variance-divisor: which divisor for the sample variance")
    n = 10
    # chi-square_{n-1} moments: mean n-1, second moment (n-1)(n+1); variance 2(n-1)
    m1, m2 = Fraction(n - 1), Fraction((n - 1) * (n + 1))
    # divisor: (quoted bias, decimals quoted, quoted variance, quoted MSE)
    rows = {9: (0.0, 6, 0.2222, 0.2222), 10: (-0.1, 6, 0.18, 0.19), 11: (-0.182, 3, 0.1488, 0.1818)}
    for d, (bias_q, bias_dec, var_q, mse_q) in rows.items():
        bias = m1 / d - 1
        var = (m2 - m1**2) / d**2
        mse = var + bias**2
        approx(f"d = {d}: bias/sigma^2", float(bias), bias_q, bias_dec)
        approx(f"d = {d}: Var/sigma^4", float(var), var_q, 4)
        approx(f"d = {d}: MSE/sigma^4", float(mse), mse_q, 4)
    grid = np.linspace(5, 20, 150001)
    mse_grid = ((n - 1) / grid - 1) ** 2 + 2 * (n - 1) / grid**2
    approx("argmin of MSE(d) over a fine grid", float(grid[np.argmin(mse_grid)]), n + 1, 3)
    x = rng.standard_normal((200000, n))
    ss = ((x - x.mean(axis=1, keepdims=True)) ** 2).sum(axis=1)
    for d, quoted in ((9, 2 / 9), (10, 0.19), (11, 2 / 11)):
        sq = (ss / d - 1.0) ** 2
        simulated(f"simulated MSE with divisor {d}", float(sq.mean()), quoted, 3 * float(sq.std()) / math.sqrt(len(sq)))


def mean_versus_vol(rng: np.random.Generator) -> None:
    print("Example 4 and cards stat-mle-mean-vs-vol-estimation, stat-mle-years-for-mean-precision")
    sig_ann = 0.01 * math.sqrt(252)
    approx("annual vol (%)", 100 * sig_ann, 15.87, 2)
    approx("SE of the annual mean with one year (%)", 100 * sig_ann / math.sqrt(1), 15.87, 2)
    approx("SE of the annual mean with one year (%), card", 100 * sig_ann, 15.9, 1)
    approx("SE(sigma_hat)/sigma = 1/sqrt(504) (%)", 100 / math.sqrt(2 * 252), 4.45, 2)
    approx("SE of annual vol (percentage points)", 100 * sig_ann / math.sqrt(2 * 252), 0.71, 2)
    approx("years for a 2% SE on the mean", (100 * sig_ann / 2) ** 2, 63, 6)
    approx("sqrt of that, 15.87/2", 100 * sig_ann / 2, 7.94, 2)
    r = rng.standard_normal((20000, 252))
    rel = r.std(axis=1, ddof=1)
    sd = float(rel.std())
    simulated("sd of sigma_hat/sigma over one simulated year of normal days", sd, 0.0445, 3 * sd / math.sqrt(2 * len(rel)))
    # delta method card: Var(sigma^2_hat) = 2 sigma^4 / n, g = sqrt, g' = 1/(2 sigma)
    sigma, nn = 0.02, 252
    delta_se = math.sqrt(2 * sigma**4 / nn) / (2 * sigma)
    approx("delta-method SE(sigma_hat)/sigma = 1/sqrt(2n), n = 252", delta_se / sigma, 1 / math.sqrt(504), 12)


def gamma_and_tank(rng: np.random.Generator) -> None:
    print("Example 5 and cards stat-mle-method-of-moments-gamma, stat-mle-german-tank")
    mean, var = 2.0, 0.8
    k, s = mean**2 / var, var / mean
    approx("Gamma shape k", k, 5, 10)
    approx("Gamma scale s", s, 0.4, 10)
    g = rng.gamma(5.0, 0.4, size=1_000_000)
    simulated("mean of Gamma(5, 0.4) draws", float(g.mean()), 2.0, 4 * float(g.std()) / 1000)
    se_var = math.sqrt(float(np.mean((g - g.mean()) ** 4)) - float(g.var()) ** 2) / 1000
    simulated("variance of Gamma(5, 0.4) draws", float(g.var()), 0.8, 4 * se_var)
    kk, m = 5, 60
    exact("German tank estimate m + m/k - 1", m + Fraction(m, kk) - 1, 71)
    for n_true in (60, 71, 100, 137):
        total = math.comb(n_true, kk)
        e_est = sum(Fraction(math.comb(mx - 1, kk - 1), total) * (mx * Fraction(kk + 1, kk) - 1) for mx in range(kk, n_true + 1))
        assert e_est == n_true, (n_true, e_est)
    print("    E[m(1 + 1/k) - 1] = N exactly for N = 60, 71, 100, 137 (k = 5), summing the law of the maximum")


def cards() -> None:
    print("Cards stat-mle-fisher-information-definition and stat-mle-invariance-property")
    approx("SE(p_hat) for p = 0.3, n = 100", math.sqrt(0.3 * 0.7 / 100), 0.0458, 4)
    approx("sqrt(0.0004)", math.sqrt(0.0004), 0.02, 10)


def main() -> None:
    rng = np.random.default_rng(SEED)
    fisher_information()
    exponential_rate(rng)
    uniform_theta(rng)
    variance_divisor(rng)
    mean_versus_vol(rng)
    gamma_and_tank(rng)
    cards()
    print("all estimation checks passed")


if __name__ == "__main__":
    main()
