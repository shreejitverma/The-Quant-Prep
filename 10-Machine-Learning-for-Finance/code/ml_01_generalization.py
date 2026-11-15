"""ML fundamentals and generalisation: every number in the note, by an independent route.

Backs every number in `10-Machine-Learning-for-Finance/01-ML-Fundamentals-and-Generalization.md`.
Independent routes used here:
- the bias-variance decomposition by exhaustive enumeration of every training sample and test draw with
  `fractions.Fraction` (the direct expected loss against noise + bias^2 + variance), then by seeded simulation for ridge;
- the training-error optimism 2 p sigma^2 / n by simulation on a fixed design against the trace of its hat matrix;
- the Sharpe of trading a correlated forecast by Gauss-Hermite quadrature of E[f r] and E[f^2 r^2], and by simulation;
- the shrunk sample mean by simulating 252 daily returns per year and by a golden-section search for the best factor;
- OLS on noise features, its out-of-sample R^2 and its break-even sample size by simulation against the closed forms;
- the ridge table by simulating noise and designs, cross-checked against the expected loss with the noise integrated
  exactly through the SVD of each design;
- hit-rate expectancy with exact fractions.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 10-Machine-Learning-for-Finance/code/ml_01_generalization.py`.
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
    print(f"    {label} ~ {estimate:.6f} (expected {expected:.6f}, tolerance {tol:.6f})")


# ------------------------------------------------------------------ bias-variance


def bias_variance_exact() -> None:
    print("Bias-variance decomposition by exhaustive enumeration (card ml-fundamentals-bias-variance)")
    # y = mu + eps with eps = +-1 equally likely (sigma^2 = 1); estimator c * mean of n = 3 training draws.
    mu, c, n = Fraction(1, 2), Fraction(1, 2), 3
    noise = (Fraction(-1), Fraction(1))
    direct = Fraction(0)
    preds = []
    for train in itertools.product(noise, repeat=n):
        fhat = c * sum((mu + e for e in train), Fraction(0)) / n
        preds.append(fhat)
        for e_new in noise:
            direct += (mu + e_new - fhat) ** 2
    direct /= 2**n * 2
    mean_f = sum(preds, Fraction(0)) / len(preds)
    var_f = sum(((f - mean_f) ** 2 for f in preds), Fraction(0)) / len(preds)
    decomposed = Fraction(1) + (mu - mean_f) ** 2 + var_f
    exact("E[(y - fhat)^2] by enumeration", direct, Fraction(55, 48))
    exact("bias = mu - E[fhat]", mu - mean_f, Fraction(1, 4))
    exact("variance of fhat", var_f, Fraction(1, 12))
    exact("sigma^2 + bias^2 + variance", decomposed, direct)

    # Ridge at one test point, by simulation: the cross terms vanish only on average, so compare within a standard error.
    rng = np.random.default_rng(SEED)
    n_obs, p, lam, reps = 40, 5, 20.0, 40_000
    beta = np.linspace(0.5, -0.5, p)
    x0 = np.ones(p) / math.sqrt(p)
    f0 = float(x0 @ beta)
    preds = np.empty(reps)
    for r in range(reps):
        x = rng.standard_normal((n_obs, p))
        y = x @ beta + rng.standard_normal(n_obs)
        preds[r] = x0 @ np.linalg.solve(x.T @ x + lam * np.eye(p), x.T @ y)
    loss = (f0 + rng.standard_normal(reps) - preds) ** 2
    se = loss.std() / math.sqrt(reps)
    simulated(
        "ridge: E[(y - fhat)^2] against 1 + bias^2 + variance", float(loss.mean()), 1 + (f0 - preds.mean()) ** 2 + preds.var(), 4 * se
    )


def optimism() -> None:
    print("Optimism of training error, 2 p sigma^2 / n (ESL section 7.4)")
    rng = np.random.default_rng(SEED + 1)
    n, p, reps = 500, 50, 4000
    x = rng.standard_normal((n, p))
    hat = x @ np.linalg.solve(x.T @ x, x.T)
    approx("trace of the hat matrix", float(np.trace(hat)), 50, 9)
    f = x @ rng.standard_normal(p)
    gaps = np.empty(reps)
    for r in range(reps):
        y = f + rng.standard_normal(n)
        fit = hat @ y
        y_new = f + rng.standard_normal(n)  # same x, fresh noise: in-sample prediction error
        gaps[r] = np.mean((y_new - fit) ** 2) - np.mean((y - fit) ** 2)
    simulated("optimism Err_in - err_train", float(gaps.mean()), 2 * 50 / 500, 4 * gaps.std() / math.sqrt(reps))
    approx("2 p sigma^2 / n", 2 * 50 / 500, 0.2, 3)


# ------------------------------------------------------------------ forecast Sharpe


def forecast_sharpe() -> None:
    print("Sharpe of holding a position proportional to a correlated forecast (cards ml-fundamentals-r2-to-sharpe, ...)")
    nodes, weights = np.polynomial.hermite_e.hermegauss(40)
    weights = weights / weights.sum()
    z1, z2 = np.meshgrid(nodes, nodes, indexing="ij")
    w = np.outer(weights, weights)
    rng = np.random.default_rng(SEED + 2)
    results = {}
    for rho in (0.05, 0.10):
        f = z1
        r = rho * z1 + math.sqrt(1 - rho * rho) * z2
        m1 = float(np.sum(w * f * r))
        m2 = float(np.sum(w * (f * r) ** 2))
        per = m1 / math.sqrt(m2 - m1 * m1)
        results[rho] = per
        assert abs(per - rho / math.sqrt(1 + rho * rho)) < 1e-12, rho
        approx(f"rho = {rho}: R^2 in percent", 100 * rho * rho, 0.25 if rho == 0.05 else 1.0, 2)
        n_sim = 2_000_000
        a = rng.standard_normal(n_sim)
        b = rho * a + math.sqrt(1 - rho * rho) * rng.standard_normal(n_sim)
        pnl = a * b
        simulated(f"rho = {rho}: simulated per-period Sharpe", float(pnl.mean() / pnl.std()), per, 4 / math.sqrt(n_sim))
    approx("rho = 0.05: per-period Sharpe (quadrature)", results[0.05], 0.0499, 4)
    approx("rho = 0.05: annualised Sharpe", results[0.05] * math.sqrt(252), 0.79, 2)
    approx("rho = 0.10: annualised Sharpe", results[0.10] * math.sqrt(252), 1.58, 2)
    approx("rho = 0.05: annualised Sharpe, one decimal", results[0.05] * math.sqrt(252), 0.8, 1)


# ------------------------------------------------------------------ worked example 1


def shrink_mean() -> None:
    print("Shrinking a mean return (card ml-fundamentals-zero-beats-mean)")
    mu, sigma, n = 4e-4, 0.01, 252
    rng = np.random.default_rng(SEED + 3)
    reps = 100_000
    xbar = np.empty(reps)
    for start in range(0, reps, 10_000):
        xbar[start : start + 10_000] = (mu + sigma * rng.standard_normal((10_000, n))).mean(axis=1)

    def mse_sim(c: float) -> tuple[float, float]:
        err = (c * xbar - mu) ** 2
        return float(err.mean()), float(err.std() / math.sqrt(reps))

    def mse_closed(c: float) -> float:
        return (1 - c) ** 2 * mu * mu + c * c * sigma * sigma / n

    # golden-section search on the closed-form MSE: a numerical optimum, not the c* formula
    lo, hi = 0.0, 1.0
    g = (math.sqrt(5) - 1) / 2
    for _ in range(200):
        a, b = hi - g * (hi - lo), lo + g * (hi - lo)
        if mse_closed(a) < mse_closed(b):
            hi = b
        else:
            lo = a
    c_star = 0.5 * (lo + hi)
    m1, s1 = mse_sim(1.0)
    simulated("MSE of the sample mean (c = 1) x 1e7, simulated", 1e7 * m1, 3.97, 1e7 * 4 * s1)
    approx("sigma^2 / n x 1e7", sigma * sigma / n * 1e7, 3.97, 2)
    approx("MSE of predicting zero (c = 0) = mu^2 x 1e7", mu * mu * 1e7, 1.6, 1)
    approx("MSE ratio zero / sample mean (less than half)", mu * mu / (sigma * sigma / n), 0.403, 3)
    approx("best shrinkage factor c* (golden section)", c_star, 0.287, 3)
    approx("c* to two decimals", c_star, 0.29, 2)
    ms, ss = mse_sim(c_star)
    simulated("MSE at c* x 1e7, simulated", 1e7 * ms, 1.14, 1e7 * 4 * ss)
    approx("MSE at c* x 1e7 (closed form at the searched c*)", mse_closed(c_star) * 1e7, 1.14, 2)
    approx("t-stat mu sqrt(n) / sigma", mu * math.sqrt(n) / sigma, 0.63, 2)
    assert mu * mu < sigma * sigma / n  # zero beats c = 1 exactly when t < 1
    print("    zero beats the sample mean: mu^2 < sigma^2/n, equivalently t < 1")


# ------------------------------------------------------------------ worked example 3 and the TL;DR


def ols_noise() -> None:
    print("OLS on noise features (cards ml-fundamentals-noise-r2, ml-fundamentals-ols-breakeven)")
    rng = np.random.default_rng(SEED + 4)
    n, p, reps = 500, 50, 2000
    r2_in = np.empty(reps)
    r2_out = np.empty(reps)
    for r in range(reps):
        x = rng.standard_normal((n, p))
        y = rng.standard_normal(n)
        xc = np.column_stack([np.ones(n), x])
        coef, *_ = np.linalg.lstsq(xc, y, rcond=None)
        resid = y - xc @ coef
        r2_in[r] = 1 - resid @ resid / np.sum((y - y.mean()) ** 2)  # centred R^2 with an intercept
        b, *_ = np.linalg.lstsq(x, y, rcond=None)
        r2_out[r] = 1 - (1 + b @ b) / 1  # pure noise, no intercept: population test MSE is 1 + ||b||^2
    simulated("pure noise: mean in-sample R^2 (Beta mean p/(n-1))", float(r2_in.mean()), 50 / 499, 4 * r2_in.std() / math.sqrt(reps))
    approx("p/(n-1)", 50 / 499, 0.100, 3)
    simulated("pure noise: mean OOS R^2 against -p/(n-p-1)", float(r2_out.mean()), -50 / 449, 4 * r2_out.std() / math.sqrt(reps))
    approx("pure noise OOS R^2 in percent", -100 * 50 / 449, -11, 0)
    oos_1pct = 0.01 - 0.99 * 50 / 449
    approx("R^2 = 1%: 0.01 - 0.99 x 50/449", oos_1pct, -0.100, 3)
    # break-even: smallest n with positive expected OOS R^2, by scanning n, then checked by simulation at that n
    n_be = next(m for m in range(p + 2, 100_000) if Fraction(1, 100) - Fraction(99, 100) * Fraction(p, m - p - 1) >= 0)
    exact("break-even n, first n with expected OOS R^2 >= 0 (exact scan)", n_be, 5001)
    exact("p + 1 + p(1-R^2)/R^2", p + 1 + Fraction(p * 99, 1), 5001)
    b2 = 0.01 / 0.99
    for m, sign in ((5001, 0), (2500, -1)):
        vals = np.empty(300)
        for r in range(300):
            beta = rng.standard_normal(p)
            beta *= math.sqrt(b2) / np.linalg.norm(beta)
            x = rng.standard_normal((m, p))
            y = x @ beta + rng.standard_normal(m)
            b, *_ = np.linalg.lstsq(x, y, rcond=None)
            vals[r] = 1 - (1 + np.sum((beta - b) ** 2)) / (1 + b2)
        se = vals.std() / math.sqrt(300)
        if sign == 0:
            simulated(f"n = {m}: simulated OOS R^2 is zero within 4 se", float(vals.mean()), 0.0, 4 * se)
        else:
            assert vals.mean() < -4 * se, vals.mean()
            print(f"    n = {m}: simulated OOS R^2 = {vals.mean():.4f}, negative")


# ------------------------------------------------------------------ worked example 4


def ridge_table() -> None:
    print("Ridge at low signal-to-noise: the table (card ml-fundamentals-ridge-lambda)")
    rng = np.random.default_rng(SEED + 5)
    n, p, reps = 500, 50, 2000
    b2 = Fraction(1, 99)  # population R^2 = b2 / (1 + b2) = 1%
    exact("population R^2", b2 / (1 + b2), Fraction(1, 100))
    lam_star = p * 1 / b2
    exact("lambda* = p sigma^2 / ||beta||^2", lam_star, 4950)
    lams = [0, 100, 1000, 5000, 10_000, 100_000]
    fine = np.geomspace(500, 50_000, 201)
    ins = np.empty((reps, len(lams)))
    oos = np.empty((reps, len(lams)))
    ana = np.empty((reps, len(lams)))
    ana_fine = np.zeros(len(fine))
    for r in range(reps):
        beta = rng.standard_normal(p)
        beta *= math.sqrt(float(b2)) / np.linalg.norm(beta)
        x = rng.standard_normal((n, p))
        y = x @ beta + rng.standard_normal(n)
        u, d, vt = np.linalg.svd(x, full_matrices=False)
        uty, vb = u.T @ y, vt @ beta

        def expected_oos(lam, d=d, vb=vb):  # noise integrated exactly: bias ||(I - A) beta||^2 plus variance trace
            shrink = d * d / (d * d + lam)
            return 1 - (1 + np.sum(((1 - shrink) * vb) ** 2) + np.sum(d * d / (d * d + lam) ** 2)) / (1 + float(b2))

        for j, lam in enumerate(lams):
            b = vt.T @ (d * uty / (d * d + lam))
            ins[r, j] = 1 - np.sum((y - x @ b) ** 2) / np.sum(y**2)
            oos[r, j] = 1 - (1 + np.sum((beta - b) ** 2)) / (1 + float(b2))  # Gaussian test design: MSE = 1 + ||beta - b||^2
            ana[r, j] = expected_oos(lam)
        ana_fine += np.array([expected_oos(lam) for lam in fine]) / reps
    quoted_in = [11.0, 10.6, 6.0, 1.9, 1.0, 0.1]
    quoted_out = [-10.0, -6.2, -0.52, 0.09, 0.07, 0.01]
    out_decimals = [1, 1, 2, 2, 2, 2]
    for j, lam in enumerate(lams):
        approx(f"lambda = {lam}: in-sample R^2 (%)", 100 * float(ins[:, j].mean()), quoted_in[j], 1)
        se = float(oos[:, j].std() / math.sqrt(reps))
        simulated(f"lambda = {lam}: simulated OOS R^2 against noise-integrated", float(oos[:, j].mean()), float(ana[:, j].mean()), 4 * se)
        approx(f"lambda = {lam}: OOS R^2 (%), noise-integrated", 100 * float(ana[:, j].mean()), quoted_out[j], out_decimals[j])
    simulated(
        "OLS in-sample R^2 against 1 - (1-R^2)(n-p)/n", float(ins[:, 0].mean()), 1 - 0.99 * 450 / 500, 4 * ins[:, 0].std() / math.sqrt(reps)
    )
    simulated(
        "OLS OOS R^2 against 0.01 - 0.99 p/(n-p-1)", float(oos[:, 0].mean()), 0.01 - 0.99 * 50 / 449, 4 * oos[:, 0].std() / math.sqrt(reps)
    )
    best = int(np.argmax(ana.mean(axis=0)))
    approx("1 - (1-R^2)(n-p)/n in percent", 100 * (1 - 0.99 * 450 / 500), 10.9, 1)
    exact("best lambda on the table grid", lams[best], 5000)
    lam_opt = float(fine[int(np.argmax(ana_fine))])
    approx("best lambda on a geometric grid of 201 points from 500 to 50,000", lam_opt, 5000, 6)
    print(f"    best lambda on a fine grid = {lam_opt:.0f}, near lambda* = 4950")
    approx("best OOS R^2 in percentage points of the 1 available", 100 * float(ana_fine.max()), 0.09, 2)


# ------------------------------------------------------------------ worked example 5 and metrics


def hit_rate_and_ic() -> None:
    print("Hit rate against payoff, and the standard error of an IC (cards ml-fundamentals-hit-rate, ...)")
    exact("55% hit rate, +1.0 / -1.5", Fraction(55, 100) * 1 - Fraction(45, 100) * Fraction(3, 2), Fraction(-1, 8))
    exact("0.45 x 1.5", Fraction(45, 100) * Fraction(3, 2), Fraction(675, 1000))
    exact("48% hit rate, +2.0 / -1.0", Fraction(48, 100) * 2 - Fraction(52, 100), Fraction(44, 100))
    exact("0.48 x 2.0 and 0.52 x 1.0", (Fraction(48, 100) * 2, Fraction(52, 100)), (Fraction(96, 100), Fraction(52, 100)))
    exact("break-even loss ratio at 55%", Fraction(55, 45), Fraction(11, 9))
    rng = np.random.default_rng(SEED + 6)
    reps, n = 20_000, 500
    a = rng.standard_normal((reps, n))
    b = rng.standard_normal((reps, n))
    a -= a.mean(axis=1, keepdims=True)
    b -= b.mean(axis=1, keepdims=True)
    ic = np.sum(a * b, axis=1) / np.sqrt(np.sum(a * a, axis=1) * np.sum(b * b, axis=1))
    sd = float(ic.std())
    simulated("sd of a null IC over 500 names", sd, 1 / math.sqrt(500), 4 * sd / math.sqrt(2 * reps))
    approx("1/sqrt(500)", 1 / math.sqrt(500), 0.045, 3)


def main() -> None:
    bias_variance_exact()
    optimism()
    forecast_sharpe()
    shrink_mean()
    ols_noise()
    ridge_table()
    hit_rate_and_ic()
    print("All ML fundamentals numbers verified.")


if __name__ == "__main__":
    main()
