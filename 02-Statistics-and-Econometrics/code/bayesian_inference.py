"""Bayesian inference: conjugate updates, shrinkage, empirical Bayes, ridge as a posterior mean, Metropolis.

Backs every number in ``07-Bayesian-Inference.md``.
Run ``uv run --no-project --with numpy python 02-Statistics-and-Econometrics/code/bayesian_inference.py``;
each printed number is asserted, so drift in the note fails CI.
Simulations and MCMC runs use fixed seeds; their results are quoted in the note as "about".
"""

from __future__ import annotations

import math
from collections.abc import Callable
from statistics import NormalDist

import numpy as np

PHI = NormalDist()


def check(name: str, value: float, expected: float, tol: float) -> float:
    """Print a named result and assert it is within ``tol`` of the value quoted in the note."""
    print(f"{name:<62s} {value:12.4f}")
    assert abs(value - expected) <= tol, f"{name}: got {value}, expected {expected} +/- {tol}"
    return value


# ---------------------------------------------------------------- beta distribution helpers


def beta_logpdf(p: np.ndarray, a: float, b: float) -> np.ndarray:
    log_norm = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    return log_norm + (a - 1) * np.log(p) + (b - 1) * np.log1p(-p)


def beta_cdf(x: float, a: float, b: float, grid: int = 2_000_001) -> float:
    """Beta CDF by trapezoidal integration of the density (accurate to about 1e-9 for a, b >= 1)."""
    p = np.linspace(0.0, 1.0, grid)[1:-1]
    f = np.exp(beta_logpdf(p, a, b))
    mask = p <= x
    dx = 1.0 / (grid - 1)
    return float(np.sum(f[mask]) * dx)


def beta_quantile(q: float, a: float, b: float) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if beta_cdf(mid, a, b, grid=200_001) < q:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def beta_binomial_pmf(k: int, m: int, a: float, b: float) -> float:
    """P(K = k) for K | p ~ Bin(m, p), p ~ Beta(a, b): the posterior predictive of a beta-binomial model."""
    log_c = math.lgamma(m + 1) - math.lgamma(k + 1) - math.lgamma(m - k + 1)
    log_b = math.lgamma(k + a) + math.lgamma(m - k + b) - math.lgamma(m + a + b)
    log_b -= math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    return math.exp(log_c + log_b)


def binomial_pmf(k: int, m: int, p: float) -> float:
    return math.comb(m, k) * p**k * (1 - p) ** (m - k)


# ---------------------------------------------------------------- MCMC


def metropolis(
    log_target: Callable[[np.ndarray], float],
    x0: np.ndarray,
    step: np.ndarray,
    n_iter: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, float]:
    """Random-walk Metropolis with independent Gaussian proposals; returns the chain and the acceptance rate."""
    x = np.array(x0, dtype=float)
    lp = log_target(x)
    chain = np.empty((n_iter, x.size))
    accepted = 0
    for i in range(n_iter):
        prop = x + step * rng.standard_normal(x.size)
        lp_prop = log_target(prop)
        if math.log(rng.random()) < lp_prop - lp:
            x, lp = prop, lp_prop
            accepted += 1
        chain[i] = x
    return chain, accepted / n_iter


def effective_sample_size(x: np.ndarray) -> float:
    """ESS = n / (1 + 2 sum rho_k), truncating with Geyer's initial positive sequence."""
    n = x.size
    xc = x - x.mean()
    f = np.fft.rfft(xc, 2 * n)
    acov = np.fft.irfft(f * np.conj(f))[:n] / n
    rho = acov / acov[0]
    s = 0.0
    for k in range(1, n - 1, 2):
        pair = rho[k] + rho[k + 1]
        if pair < 0:
            break
        s += pair
    return n / (1.0 + 2.0 * s)


# ---------------------------------------------------------------- sections


def beta_binomial() -> None:
    print("\n# 1. Beta-binomial: 60 wins in 100 trades")
    print("#    backs: Worked examples 1, 2, 8; cards stat-bayes-hit-rate-60-100, stat-bayes-sceptical-prior,")
    print("#    stat-bayes-posterior-predictive, stat-bayes-map-vs-mean, stat-bayes-map-not-invariant, stat-bayes-rule-of-succession")
    k, n = 60, 100
    # frequentist
    p_hat = k / n
    se = math.sqrt(p_hat * (1 - p_hat) / n)
    check("MLE", p_hat, 0.6, 1e-12)
    check("Wald 95% CI lower", p_hat - 1.96 * se, 0.5040, 1e-4)
    check("Wald 95% CI upper", p_hat + 1.96 * se, 0.6960, 1e-4)
    z = (p_hat - 0.5) / math.sqrt(0.25 / n)
    check("z under H0 p=0.5 (null SE)", z, 2.0, 1e-12)
    check("one-sided p-value", 1 - PHI.cdf(z), 0.0228, 1e-4)
    check("two-sided p-value", 2 * (1 - PHI.cdf(z)), 0.0455, 1e-4)
    # flat prior Beta(1,1) -> Beta(61, 41)
    a, b = 1 + k, 1 + n - k
    check("flat prior: posterior mean 61/102", a / (a + b), 0.5980, 1e-4)
    check("flat prior: MAP 60/100", (a - 1) / (a + b - 2), 0.6, 1e-12)
    check("flat prior: posterior sd", math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1))), 0.0483, 1e-4)
    check("flat prior: P(p <= 0.5 | data)", beta_cdf(0.5, a, b), 0.0230, 1e-4)
    # exact cross-check: P(Beta(a,b) <= x) = P(Binomial(a+b-1, x) >= a) for integer a, b
    exact = sum(math.comb(a + b - 1, j) for j in range(a, a + b)) / 2 ** (a + b - 1)
    check("flat prior: same via P(Bin(101, 0.5) >= 61)", exact, 0.0230, 1e-4)
    check("flat prior: 2.5% posterior quantile", beta_quantile(0.025, a, b), 0.5017, 1e-4)
    check("flat prior: 97.5% posterior quantile", beta_quantile(0.975, a, b), 0.6907, 1e-4)
    # informative prior Beta(50,50): 'most traders are coin flips'
    a2, b2 = 50 + k, 50 + n - k
    check("Beta(50,50) prior: posterior mean 110/200", a2 / (a2 + b2), 0.55, 1e-12)
    check("Beta(50,50) prior: MAP 109/198", (a2 - 1) / (a2 + b2 - 2), 0.5505, 1e-4)
    check("Beta(50,50) prior: posterior sd", math.sqrt(a2 * b2 / ((a2 + b2) ** 2 * (a2 + b2 + 1))), 0.0351, 1e-4)
    check("Beta(50,50) prior: P(p > 0.5 | data)", 1 - beta_cdf(0.5, a2, b2), 0.9220, 1e-4)
    # posterior predictive for the next 10 trades
    pp6 = sum(beta_binomial_pmf(j, 10, a, b) for j in range(6, 11))
    plug6 = sum(binomial_pmf(j, 10, p_hat) for j in range(6, 11))
    check("predictive P(>= 6 wins of next 10), flat prior", pp6, 0.6238, 1e-4)
    check("plug-in Binomial(10, 0.6) P(>= 6)", plug6, 0.6331, 1e-4)

    def pmf_variance(pmf: list[float]) -> float:
        mean = sum(j * q for j, q in enumerate(pmf))
        return sum((j - mean) ** 2 * q for j, q in enumerate(pmf))

    var_pred = pmf_variance([beta_binomial_pmf(j, 10, a, b) for j in range(11)])
    check("predictive variance of wins in next 10 (enumerated)", var_pred, 2.6139, 1e-4)
    closed = 10 * (a / (a + b)) * (b / (a + b)) * (a + b + 10) / (a + b + 1)
    assert abs(var_pred - closed) < 1e-10  # beta-binomial closed form agrees with the enumeration
    check("plug-in variance (enumerated Binomial(10, 0.6))", pmf_variance([binomial_pmf(j, 10, p_hat) for j in range(11)]), 2.4, 1e-12)
    # Laplace rule of succession: 0 losing months out of 12; posterior mean of p by numerical integration
    grid = np.linspace(0.0, 1.0, 2_000_001)[1:-1]
    for name, a0, b0, exp in (("flat Beta(1,1)", 1.0, 1.0, 0.0714), ("Jeffreys Beta(1/2,1/2)", 0.5, 0.5, 0.0385)):
        dens = np.exp(beta_logpdf(grid, a0, b0 + 12))
        check(f"P(loss next month) after 0 of 12, {name} prior", float(np.sum(grid * dens) / np.sum(dens)), exp, 1e-4)
    # MAP depends on parametrisation: mode of logit(p) is a/(a+b)
    check("MAP of logit(p), mapped back: a/(a+b)", a / (a + b), 0.5980, 1e-4)


def normal_normal() -> None:
    print("\n# 2. Normal-normal: manager alpha and strategy Sharpe")
    print(
        "#    backs: Worked examples 3, 4; cards stat-bayes-manager-alpha, stat-bayes-years-for-half-shrinkage, stat-bayes-sharpe-shrinkage"
    )
    prior_mean, prior_var = 0.0, 2.0**2
    xbar, te, years = 6.0, 8.0, 3.0
    s_var = te**2 / years
    shrink = s_var / (s_var + prior_var)
    post_var = 1.0 / (1.0 / prior_var + 1.0 / s_var)
    post_mean = post_var * (prior_mean / prior_var + xbar / s_var)
    check("sampling variance of 3-year alpha, 64/3", s_var, 21.3333, 1e-4)
    check("sampling sd", math.sqrt(s_var), 4.6188, 1e-4)
    check("denominator s^2 + tau^2", s_var + prior_var, 25.3333, 1e-4)
    check("shrinkage factor B = s^2/(s^2+tau^2)", shrink, 0.8421, 1e-4)
    check("weight kept on the data, 1 - B", 1 - shrink, 0.1579, 1e-4)
    check("posterior mean alpha (%)", post_mean, 0.9474, 1e-4)
    check("posterior sd (%)", math.sqrt(post_var), 1.8353, 1e-4)
    check("P(alpha > 0 | data)", 1 - PHI.cdf(-post_mean / math.sqrt(post_var)), 0.6971, 1e-4)
    check("raw t-stat 6/4.62", xbar / math.sqrt(s_var), 1.2990, 1e-4)
    check("predictive sd of next-year alpha sqrt(post_var + 64)", math.sqrt(post_var + te**2), 8.2078, 1e-4)
    lo, hi = 0.1, 100.0  # solve B(T) = (te^2/T) / (te^2/T + tau^2) = 0.5 by bisection
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if (te**2 / mid) / (te**2 / mid + prior_var) > 0.5 else (lo, mid)
    check("years of track record for B = 0.5 (closed form te^2/tau^2)", 0.5 * (lo + hi), 16.0, 1e-9)
    # Sharpe: observed 1.5 over 2 years, prior N(0, 0.5^2), sampling var ~ 1/T
    s2, t2 = 1.0 / 2.0, 0.25
    pm = 1.5 * t2 / (t2 + s2)
    psd = math.sqrt(1 / (1 / t2 + 1 / s2))
    check("Sharpe: posterior mean", pm, 0.5, 1e-12)
    check("Sharpe: posterior sd", psd, 0.4082, 1e-4)
    check("Sharpe: P(SR > 0 | data)", 1 - PHI.cdf(-pm / psd), 0.8897, 1e-4)
    check("Sharpe: frequentist one-sided p, z = 1.5 sqrt(2)", 1 - PHI.cdf(1.5 * math.sqrt(2)), 0.0169, 1e-4)


def empirical_bayes() -> None:
    print("\n# 3. Empirical Bayes and James-Stein on 200 managers")
    print("#    backs: Worked example 5; cards stat-bayes-james-stein, stat-bayes-empirical-bayes-tau, stat-bayes-winners-curse")
    rng = np.random.default_rng(42)
    k, tau, sigma, reps = 200, 2.0, 8.0 / math.sqrt(3.0), 500
    mse_raw, mse_eb, mse_js, tau_hat_all = [], [], [], []
    top_raw, top_true, top_eb = [], [], []
    for _ in range(reps):
        alpha = tau * rng.standard_normal(k)
        obs = alpha + sigma * rng.standard_normal(k)
        tau2_hat = max(0.0, obs.var(ddof=1) - sigma**2)
        b_hat = sigma**2 / (sigma**2 + tau2_hat)
        eb = obs.mean() + (1 - b_hat) * (obs - obs.mean())
        js_factor = max(0.0, 1 - (k - 3) * sigma**2 / np.sum((obs - obs.mean()) ** 2))
        js = obs.mean() + js_factor * (obs - obs.mean())
        mse_raw.append(np.mean((obs - alpha) ** 2))
        mse_eb.append(np.mean((eb - alpha) ** 2))
        mse_js.append(np.mean((js - alpha) ** 2))
        tau_hat_all.append(math.sqrt(tau2_hat))
        top = np.argsort(obs)[-20:]
        top_raw.append(obs[top].mean())
        top_true.append(alpha[top].mean())
        top_eb.append(eb[top].mean())
    check("oracle Bayes risk tau^2 sigma^2/(tau^2+sigma^2)", tau**2 * sigma**2 / (tau**2 + sigma**2), 3.3684, 1e-4)
    check("MSE raw (theory sigma^2 = 21.33)", float(np.mean(mse_raw)), 21.42, 0.01)
    check("MSE empirical Bayes", float(np.mean(mse_eb)), 3.63, 0.01)
    check("MSE James-Stein (positive part)", float(np.mean(mse_js)), 3.63, 0.01)
    check("mean estimated tau", float(np.mean(tau_hat_all)), 1.92, 0.01)
    check("top-decile managers: mean raw alpha", float(np.mean(top_raw)), 8.79, 0.01)
    check("top-decile managers: mean true alpha", float(np.mean(top_true)), 1.39, 0.01)
    check("top-decile managers: mean EB estimate", float(np.mean(top_eb)), 1.39, 0.01)


def ridge_as_posterior() -> None:
    print("\n# 4. Ridge regression is the posterior mean under a Gaussian prior")
    print("#    backs: Worked example 6; card stat-bayes-ridge-prior")
    rng = np.random.default_rng(7)
    n, p, sigma, tau = 60, 5, 1.0, 0.5
    X = rng.standard_normal((n, p))
    beta = tau * rng.standard_normal(p)
    y = X @ beta + sigma * rng.standard_normal(n)
    lam = sigma**2 / tau**2
    # posterior mean from precision form
    prec = X.T @ X / sigma**2 + np.eye(p) / tau**2
    post_mean = np.linalg.solve(prec, X.T @ y / sigma**2)
    # ridge by data augmentation: append sqrt(lam) I rows with zero targets, then plain least squares
    Xa = np.vstack([X, math.sqrt(lam) * np.eye(p)])
    ya = np.concatenate([y, np.zeros(p)])
    ridge, *_ = np.linalg.lstsq(Xa, ya, rcond=None)
    ols, *_ = np.linalg.lstsq(X, y, rcond=None)
    check("lambda = sigma^2/tau^2", lam, 4.0, 1e-12)
    check("max |posterior mean - ridge|", float(np.max(np.abs(post_mean - ridge))), 0.0, 1e-10)
    check("||ridge|| / ||OLS||", float(np.linalg.norm(ridge) / np.linalg.norm(ols)), 0.9329, 1e-4)


def mcmc_checks() -> None:
    print("\n# 5. Random-walk Metropolis checked against conjugate answers")
    print("#    backs: Worked example 7; cards stat-bayes-metropolis-tuning, stat-bayes-mcmc-validation, stat-bayes-ess")
    rng = np.random.default_rng(2026)
    a, b = 61.0, 41.0

    def log_beta_post(x: np.ndarray) -> float:
        p = x[0]
        if not 0.0 < p < 1.0:
            return -math.inf
        return 60.0 * math.log(p) + 40.0 * math.log1p(-p)

    sd_true = math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)))
    chain, acc = metropolis(log_beta_post, np.array([0.5]), np.array([2.4 * sd_true]), 60_000, rng)
    draws = chain[2000:, 0]
    check("beta target: acceptance rate (step 2.4 x posterior sd)", acc, 0.446, 0.0005)
    mc_mean = check("beta target: MCMC mean (exact 0.5980)", float(draws.mean()), 0.5985, 0.0001)
    mc_sd = check("beta target: MCMC sd (exact 0.0483)", float(draws.std()), 0.0482, 0.0001)
    mc_tail = check("beta target: MCMC P(p <= 0.5) (exact 0.0230)", float(np.mean(draws <= 0.5)), 0.0220, 0.0001)
    ess = check("beta target: ESS of 58,000 draws", effective_sample_size(draws), 12168, 1)
    # the chain agrees with the conjugate answer within its Monte Carlo error
    mcse = check("beta target: Monte Carlo s.e. of the mean, sd/sqrt(ESS)", sd_true / math.sqrt(ess), 0.0004, 0.00005)
    gap = check("beta target: |MCMC mean - exact mean|", abs(mc_mean - a / (a + b)), 0.0004, 0.00005)
    assert gap < 3 * mcse
    assert abs(mc_sd - sd_true) < 0.001 and abs(mc_tail - 0.0230) < 0.003

    # unknown mean and variance, prior flat in (mu, log sigma): marginal of mu is t_{n-1}(xbar, s^2/n)
    data = 0.05 + 1.0 * rng.standard_normal(30)
    n = data.size
    xbar, s2 = float(data.mean()), float(data.var(ddof=1))

    def log_normal_post(x: np.ndarray) -> float:
        mu, log_sig = x
        return -n * log_sig - float(np.sum((data - mu) ** 2)) / (2.0 * math.exp(2.0 * log_sig))

    chain2, acc2 = metropolis(log_normal_post, np.array([0.0, 0.0]), np.array([0.35, 0.25]), 80_000, rng)
    mu_draws = chain2[2000:, 0]
    sig2_draws = np.exp(2.0 * chain2[2000:, 1])
    exact_mu_sd = math.sqrt(s2 / n * (n - 1) / (n - 3))
    check("normal target: sample mean xbar", xbar, 0.1156, 1e-4)
    check("normal target: sample variance s^2", s2, 0.9094, 1e-4)
    check("normal target: acceptance rate", acc2, 0.305, 0.0005)
    mu_mc = check("normal target: MCMC mean of mu (exact = xbar = 0.1156)", float(mu_draws.mean()), 0.1174, 0.0001)
    check("normal target: exact sd of mu, t_{n-1} scale", exact_mu_sd, 0.1804, 1e-4)
    mu_sd_mc = check("normal target: MCMC sd of mu", float(mu_draws.std()), 0.1813, 0.0001)
    check("normal target: exact E[sigma^2] = (n-1) s^2/(n-3)", (n - 1) * s2 / (n - 3), 0.9768, 1e-4)
    sig_mc = check("normal target: MCMC E[sigma^2]", float(sig2_draws.mean()), 0.9748, 0.0001)
    assert abs(mu_mc - xbar) < 0.005 and abs(mu_sd_mc - exact_mu_sd) < 0.003 and abs(sig_mc - 0.9768) < 0.005


if __name__ == "__main__":
    beta_binomial()
    normal_normal()
    empirical_bayes()
    ridge_as_posterior()
    mcmc_checks()
    print("\nall bayesian_inference checks passed")
