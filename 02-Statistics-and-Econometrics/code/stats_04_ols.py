"""Linear regression and OLS: every fit, standard error and bias in the note, by an independent route.

Backs every number in `02-Statistics-and-Econometrics/04-Linear-Regression-OLS.md`.
Independent routes used here:
- the hand fit by `numpy.linalg.lstsq` and exact `fractions.Fraction` sums, with the t_3 p-value from the
  closed-form Student-t CDF for three degrees of freedom;
- slopes both ways, omitted-variable bias and attenuation by seeded simulation of the stated models;
- the duplicated-data ratio by refitting the stacked data set;
- the noise-regressor R^2 increase by seeded simulation of the partial R^2, and the adjusted-R^2 rule
  (rises exactly when |t| > 1) checked on random regressions;
- Frisch-Waugh-Lovell and Gauss-Markov checked numerically on random designs.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 02-Statistics-and-Econometrics/code/stats_04_ols.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261112


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


def ols(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta, y - X @ beta


def ols_se(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    beta, e = ols(X, y)
    n, p = X.shape
    s2 = e @ e / (n - p)
    return beta, np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))


def t3_cdf(t: float) -> float:
    """Closed-form CDF of Student-t with 3 degrees of freedom."""
    u = t / math.sqrt(3)
    return 0.5 + (u / (1 + u * u) + math.atan(u)) / math.pi


def hand_fit() -> None:
    print("Example 1 and cards stat-ols-hand-fit, stat-ols-residual-properties")
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]
    xb, yb = Fraction(sum(x), 5), Fraction(sum(y), 5)
    sxy = sum((a - xb) * (b - yb) for a, b in zip(x, y, strict=True))
    sxx = sum((a - xb) ** 2 for a in x)
    syy = sum((b - yb) ** 2 for b in y)
    exact("S_xy", sxy, 6)
    exact("S_xx", sxx, 10)
    exact("S_yy", syy, 6)
    X = np.c_[np.ones(5), np.array(x, float)]
    (b0, b1), se = ols_se(X, np.array(y, float))
    approx("slope (lstsq)", b1, 0.6, 10)
    approx("intercept (lstsq)", b0, 2.2, 10)
    approx("slope times xbar, 0.6 x 3", 0.6 * 3, 1.8, 10)
    beta, e = ols(X, np.array(y, float))
    rss = float(e @ e)
    approx("RSS", rss, 2.4, 10)
    approx("explained SS = TSS - RSS", 6 - rss, 3.6, 10)
    approx("R^2", 1 - rss / 6, 0.6, 10)
    exact("R^2 = S_xy^2/(S_xx S_yy)", sxy**2 / (sxx * syy), Fraction(3, 5))
    approx("s^2", rss / 3, 0.8, 10)
    approx("SE(slope)", se[1], 0.283, 3)
    t = b1 / se[1]
    approx("t", t, 2.12, 2)
    approx("two-sided p on 3 df", 2 * (1 - t3_cdf(t)), 0.124, 3)
    grid = np.linspace(0.0, t, 20001)
    dens = 2 / (math.pi * math.sqrt(3)) * (1 + grid**2 / 3) ** -2  # t_3 density
    area = float((grid[1] - grid[0]) / 3 * (dens[0] + dens[-1] + 4 * dens[1:-1:2].sum() + 2 * dens[2:-1:2].sum()))
    approx("same p by Simpson quadrature of the t_3 density", 1 - 2 * area, 0.124, 3)
    rev, _ = ols(np.c_[np.ones(5), np.array(y, float)], np.array(x, float))
    approx("slope of x on y", rev[1], 1.0, 10)
    approx("product of the two slopes", b1 * rev[1], 0.6, 10)
    approx("sum of residuals", float(e.sum()), 0.0, 10)
    approx("residuals dot fitted values", float(e @ (X @ beta)), 0.0, 10)


def beta_both_ways(rng: np.random.Generator) -> None:
    print("Example 2 and cards stat-ols-stock-beta-from-vols, stat-ols-product-of-slopes-r2, stat-ols-impossible-slope-pair")
    rho, s_stock, s_mkt = 0.6, 0.30, 0.15
    approx("beta stock on market", rho * s_stock / s_mkt, 1.2, 10)
    approx("beta market on stock", rho * s_mkt / s_stock, 0.3, 10)
    approx("1/1.2", 1 / 1.2, 0.83, 2)
    approx("product", 1.2 * 0.3, 0.36, 10)
    approx("idiosyncratic share (%)", 100 * (1 - 0.36), 64, 6)
    n = 400000
    m = s_mkt * rng.standard_normal(n)
    st = 1.2 * m + s_stock * math.sqrt(1 - rho**2) * rng.standard_normal(n)
    b_sm, _ = ols(np.c_[np.ones(n), m], st)
    b_ms, _ = ols(np.c_[np.ones(n), st], m)
    simulated("simulated slope of stock on market", b_sm[1], 1.2, 0.01)
    simulated("simulated slope of market on stock", b_ms[1], 0.3, 0.003)
    approx("R^2 from slopes 0.5 and 0.8", 0.5 * 0.8, 0.4, 10)
    approx("rho = sqrt(0.4)", math.sqrt(0.4), 0.632, 3)
    approx("rho^2 implied by slopes 2 and 0.6", 2 * 0.6, 1.2, 10)


def omitted_variable(rng: np.random.Generator) -> None:
    print("Example 3 and cards stat-ols-ovb-signal-market, stat-ols-omitted-variable-bias, stat-ols-attenuation-bias, stat-ols-fwl-theorem")
    n = 400000
    s = rng.standard_normal(n)
    mkt = 0.4 * s + rng.standard_normal(n)
    r = 0.5 * s + 0.3 * mkt + rng.standard_normal(n)
    short, _ = ols(np.c_[np.ones(n), s], r)
    long, _ = ols(np.c_[np.ones(n), s, mkt], r)
    se = 1 / math.sqrt(n)
    simulated("short-regression slope", short[1], 0.62, 6 * se)
    simulated("long-regression slope on s", long[1], 0.5, 6 * se)
    approx("0.5 + 0.3 x 0.4", 0.5 + 0.3 * 0.4, 0.62, 10)
    approx("market part 0.3 x 0.4", 0.3 * 0.4, 0.12, 10)
    approx("share of 0.62 that is market exposure (%)", 100 * 0.12 / 0.62, 19, 0)
    approx("overstatement relative to the true 0.5 (%)", 100 * 0.12 / 0.5, 24, 6)
    # Frisch-Waugh-Lovell: slope of r on the residual of s after regressing s on [1, mkt]
    _, s_resid = ols(np.c_[np.ones(n), mkt], s)
    fwl, _ = ols(s_resid[:, None], r - r.mean())
    approx("FWL slope equals the long-regression coefficient", float(fwl[0]), float(long[1]), 10)
    # attenuation: measurement noise with the same variance as the regressor
    x_true = rng.standard_normal(n)
    yv = 1.0 * x_true + rng.standard_normal(n)
    x_obs = x_true + rng.standard_normal(n)
    att, _ = ols(np.c_[np.ones(n), x_obs], yv)
    simulated("slope with noise variance equal to the signal variance", att[1], 0.5, 6 * se)


def duplicate_rows(rng: np.random.Generator) -> None:
    print("Example 4 and card stat-ols-duplicate-data")
    n = 50
    x = rng.standard_normal(n)
    y = 0.3 * x + rng.standard_normal(n)
    X = np.c_[np.ones(n), x]
    b1, se1 = ols_se(X, y)
    b2, se2 = ols_se(np.r_[X, X], np.r_[y, y])
    assert np.allclose(b1, b2)
    ratio = se2 / se1
    approx("SE ratio after duplication (both coefficients)", float(ratio[0]), 0.700, 3)
    approx("SE ratio, slope", float(ratio[1]), 0.700, 3)
    approx("sqrt(48/98)", math.sqrt(48 / 98), 0.700, 3)
    approx("t inflation", float(1 / ratio[1]), 1.43, 2)
    approx("large-n limit sqrt(2)", math.sqrt(2), 1.41, 2)


def noise_regressor(rng: np.random.Generator) -> None:
    print("Example 5 and card stat-ols-noise-regressor-r2")
    n, p, r2 = 100, 3, 0.10
    d = (1 - r2) / (n - p)
    approx("E[Delta R^2]", d, 0.0093, 4)
    approx("R^2 after", r2 + d, 0.109, 3)
    adj_before = 1 - (1 - r2) * (n - 1) / (n - p)
    adj_after = 1 - (1 - r2 - d) * (n - 1) / (n - p - 1)
    approx("adjusted R^2 before", adj_before, 0.0814, 4)
    approx("1 - R^2 after", 1 - r2 - d, 0.8907, 4)
    approx("adjusted R^2 after, at the average increase", adj_after, 0.0814, 4)
    approx("1/97", 1 / 97, 0.0103, 4)
    reps = 20000
    X = np.c_[np.ones(n), rng.standard_normal((n, 2))]
    y = X @ np.array([0.0, 0.3, 0.2]) + rng.standard_normal(n)
    _, e0 = ols(X, y)
    partial = np.empty(reps)
    t_abs = np.empty(reps)
    adj_rise = np.empty(reps, dtype=bool)
    tss = float(((y - y.mean()) ** 2).sum())
    for i in range(reps):
        z = rng.standard_normal(n)
        Xz = np.c_[X, z]
        b, se = ols_se(Xz, y)
        _, e1 = ols(Xz, y)
        partial[i] = 1 - (e1 @ e1) / (e0 @ e0)
        t_abs[i] = abs(b[3] / se[3])
        r2a = 1 - (e0 @ e0) / tss
        r2b = 1 - (e1 @ e1) / tss
        adj_rise[i] = (1 - (1 - r2b) * (n - 1) / (n - 4)) > (1 - (1 - r2a) * (n - 1) / (n - 3))
    sd = float(partial.std())
    simulated("mean partial R^2 over 20,000 noise regressors", float(partial.mean()), 0.0103, 3 * sd / math.sqrt(reps))
    assert np.array_equal(adj_rise, t_abs > 1)
    print("    adjusted R^2 rose in exactly the draws with |t| > 1 (20,000 of 20,000 agree)")
    assert np.all(partial >= -1e-12)
    print("    R^2 never fell when the noise regressor was added")


def gauss_markov(rng: np.random.Generator) -> None:
    print("Gauss-Markov: another linear unbiased estimator C = (X'X)^-1 X' + D with DX = 0 has variance + DD'")
    n = 30
    X = np.c_[np.ones(n), rng.standard_normal((n, 2))]
    A = np.linalg.inv(X.T @ X) @ X.T
    M = np.eye(n) - X @ A
    D = rng.standard_normal((3, n)) @ M
    C = A + D
    assert np.allclose(C @ X, np.eye(3))
    gap = C @ C.T - np.linalg.inv(X.T @ X)
    assert np.allclose(gap, D @ D.T) and np.linalg.eigvalsh(gap).min() > -1e-10
    print("    Var(Cy) - Var(OLS) = sigma^2 DD' is positive semi-definite")


def main() -> None:
    rng = np.random.default_rng(SEED)
    hand_fit()
    beta_both_ways(rng)
    omitted_variable(rng)
    duplicate_rows(rng)
    noise_regressor(rng)
    gauss_markov(rng)
    print("all OLS checks passed")


if __name__ == "__main__":
    main()
