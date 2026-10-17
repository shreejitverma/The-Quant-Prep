"""Regression diagnostics and robust inference: HC, HAC and clustered errors, leverage, VIF, Huber.

Backs every number in ``05-Regression-Diagnostics-and-Robust-Inference.md``.
Run ``uv run --no-project --with numpy python 02-Statistics-and-Econometrics/code/robust_inference.py``;
each printed number is asserted, so drift in the note fails CI.
Simulations use fixed seeds; their results are quoted in the note as "about".
"""

from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np

PHI = NormalDist()


def check(name: str, value: float, expected: float, tol: float) -> float:
    """Print a named result and assert it is within ``tol`` of the value quoted in the note."""
    print(f"{name:<58s} {value:12.4f}")
    assert abs(value - expected) <= tol, f"{name}: got {value}, expected {expected} +/- {tol}"
    return value


# ---------------------------------------------------------------- estimators


def ols(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """OLS coefficients, residuals and (X'X)^{-1}."""
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta, y - X @ beta, np.linalg.inv(X.T @ X)


def cov_classical(X: np.ndarray, e: np.ndarray, xtx_inv: np.ndarray) -> np.ndarray:
    """s^2 (X'X)^{-1}, valid only under spherical errors."""
    n, p = X.shape
    return (e @ e / (n - p)) * xtx_inv


def cov_hc(X: np.ndarray, e: np.ndarray, xtx_inv: np.ndarray, kind: str = "HC0") -> np.ndarray:
    """White sandwich (X'X)^{-1} X' diag(w_i e_i^2) X (X'X)^{-1} with the MacKinnon-White variants."""
    n, p = X.shape
    if kind == "HC0":
        u2 = e**2
    elif kind == "HC1":
        u2 = e**2 * n / (n - p)
    elif kind == "HC3":
        h = np.einsum("ij,jk,ik->i", X, xtx_inv, X)
        u2 = (e / (1.0 - h)) ** 2
    else:
        raise ValueError(kind)
    meat = X.T @ (u2[:, None] * X)
    return xtx_inv @ meat @ xtx_inv


def hac_meat(scores: np.ndarray, lags: int, kernel: str = "bartlett") -> np.ndarray:
    """Long-run covariance of the score vectors g_t = x_t e_t (rows of ``scores``).

    Bartlett weights 1 - l/(L+1) (Newey-West, always PSD) or truncated uniform weights
    (Hansen-Hodrick, exact for an MA(L) score but not guaranteed PSD).
    """
    s = scores.T @ scores
    for lag in range(1, lags + 1):
        w = 1.0 - lag / (lags + 1.0) if kernel == "bartlett" else 1.0
        gamma = scores[lag:].T @ scores[:-lag]
        s += w * (gamma + gamma.T)
    return s


def cov_hac(X: np.ndarray, e: np.ndarray, xtx_inv: np.ndarray, lags: int, kernel: str = "bartlett") -> np.ndarray:
    return xtx_inv @ hac_meat(X * e[:, None], lags, kernel) @ xtx_inv


def cov_cluster(X: np.ndarray, e: np.ndarray, xtx_inv: np.ndarray, groups: np.ndarray) -> np.ndarray:
    """Liang-Zeger cluster-robust covariance with the usual G/(G-1) (n-1)/(n-p) small-sample factor."""
    n, p = X.shape
    n_groups = int(groups.max()) + 1
    g_scores = np.zeros((n_groups, p))
    np.add.at(g_scores, groups, X * e[:, None])
    c = n_groups / (n_groups - 1) * (n - 1) / (n - p)
    return c * xtx_inv @ (g_scores.T @ g_scores) @ xtx_inv


def nw_rule_of_thumb(t: int) -> int:
    """floor(4 (T/100)^(2/9)): the pilot lag of Newey and West (1994), widely used as a default."""
    return math.floor(4.0 * (t / 100.0) ** (2.0 / 9.0))


def andrews_bartlett_bandwidth(rho: float, t: int) -> float:
    """Andrews (1991) plug-in bandwidth for the Bartlett kernel with an AR(1) score: 1.1447 (alpha(1) T)^(1/3)."""
    alpha1 = 4.0 * rho**2 / ((1.0 - rho) ** 2 * (1.0 + rho) ** 2)
    return 1.1447 * (alpha1 * t) ** (1.0 / 3.0)


def bartlett_lrv_ar1(phi: float, lags: int) -> float:
    """Bartlett-weighted long-run variance of a unit-variance AR(1), using its true autocorrelations."""
    return 1.0 + 2.0 * sum((1.0 - k / (lags + 1.0)) * phi**k for k in range(1, lags + 1))


def huber_irls(X: np.ndarray, y: np.ndarray, c: float = 1.345, iters: int = 100) -> np.ndarray:
    """Huber M-estimator by iteratively reweighted least squares, scale re-estimated by the normalised MAD."""
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    for _ in range(iters):
        r = y - X @ beta
        scale = np.median(np.abs(r - np.median(r))) / 0.6745
        u = np.abs(r) / scale
        w = np.where(u <= c, 1.0, c / np.maximum(u, 1e-12))
        sw = np.sqrt(w)
        new, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
        if np.max(np.abs(new - beta)) < 1e-10:
            return new
        beta = new
    return beta


def huber_efficiency(c: float) -> float:
    """Asymptotic efficiency of the Huber location estimator at the normal: P(|Z|<c)^2 / E[psi(Z)^2]."""
    inside = 2.0 * PHI.cdf(c) - 1.0
    # E[Z^2 1{|Z|<c}] = inside - 2 c phi(c)
    e_psi2 = inside - 2.0 * c * PHI.pdf(c) + c**2 * (1.0 - inside)
    return inside**2 / e_psi2


# ---------------------------------------------------------------- sections


def heteroskedasticity() -> None:
    print("\n# 1. Heteroskedasticity: Var(e|x) = x^2, x ~ N(0,1), true slope 0")
    print("#    backs: Core concepts (HC family), Worked example 1; cards stat-diag-hetero-size-distortion, stat-diag-breusch-pagan")
    rng = np.random.default_rng(11)
    n, reps = 500, 4000
    slopes, se_c, se_0, se_3, rej_c, rej_0, rej_3 = [], [], [], [], 0, 0, 0
    for _ in range(reps):
        x = rng.standard_normal(n)
        y = 1.0 + np.abs(x) * rng.standard_normal(n)
        X = np.column_stack([np.ones(n), x])
        b, e, xi = ols(X, y)
        sc = math.sqrt(cov_classical(X, e, xi)[1, 1])
        s0 = math.sqrt(cov_hc(X, e, xi, "HC0")[1, 1])
        s3 = math.sqrt(cov_hc(X, e, xi, "HC3")[1, 1])
        slopes.append(b[1])
        se_c.append(sc)
        se_0.append(s0)
        se_3.append(s3)
        rej_c += abs(b[1] / sc) > 1.96
        rej_0 += abs(b[1] / s0) > 1.96
        rej_3 += abs(b[1] / s3) > 1.96
    true_sd = float(np.std(slopes))
    # E[x^2] and E[x^4] of N(0,1) by quadrature, not recalled
    grid = np.linspace(-12.0, 12.0, 240_001)
    dens = np.exp(-0.5 * grid**2) / math.sqrt(2 * math.pi)
    m2, m4 = float(np.trapezoid(grid**2 * dens, grid)), float(np.trapezoid(grid**4 * dens, grid))
    ratio = check("asymptotic SE ratio sqrt(E[x^4]/E[x^2]^2) (quadrature)", math.sqrt(m4 / m2**2), 1.7321, 1e-4)
    check("theoretical classical-t rejection 2(1-Phi(1.96/ratio))", 2 * (1 - PHI.cdf(1.96 / ratio)), 0.2578, 1e-4)
    check("MC sd of slope x sqrt(n)", true_sd * math.sqrt(n), 1.736, 0.002)
    check("mean classical SE x sqrt(n)", float(np.mean(se_c)) * math.sqrt(n), 0.998, 0.002)
    check("mean White HC0 SE x sqrt(n)", float(np.mean(se_0)) * math.sqrt(n), 1.705, 0.002)
    check("mean HC3 SE x sqrt(n)", float(np.mean(se_3)) * math.sqrt(n), 1.725, 0.002)
    check("rejection rate at 5%, classical SE", rej_c / reps, 0.262, 0.003)
    check("rejection rate at 5%, HC0", rej_0 / reps, 0.057, 0.003)
    check("rejection rate at 5%, HC3", rej_3 / reps, 0.054, 0.003)

    # Koenker (studentised Breusch-Pagan) LM test on one sample: n R^2 of e^2 on [1, x^2]
    x = rng.standard_normal(n)
    y = 1.0 + np.abs(x) * rng.standard_normal(n)
    X = np.column_stack([np.ones(n), x])
    _, e, _ = ols(X, y)
    Z = np.column_stack([np.ones(n), x**2])
    _, u, _ = ols(Z, e**2)
    r2 = 1.0 - (u @ u) / np.sum((e**2 - np.mean(e**2)) ** 2)
    check("Koenker-BP LM = n R^2 (one sample)", n * r2, 129.4, 0.1)
    check("chi2_1 5% critical value = z_0.975^2", PHI.inv_cdf(0.975) ** 2, 3.841, 0.0005)


def newey_west_kernel() -> None:
    print("\n# 2. Newey-West kernel, truncation bias and bandwidth rules")
    print("#    backs: Core concepts (Newey-West), Worked example 7; cards stat-diag-nw-truncation-bias, stat-diag-nw-bandwidth-rule")
    check("Bartlett LRV, AR(1) phi=0.5, L=2", bartlett_lrv_ar1(0.5, 2), 1.8333, 1e-4)
    check("Bartlett LRV, AR(1) phi=0.5, L=5", bartlett_lrv_ar1(0.5, 5), 2.34375, 1e-9)
    check("Bartlett LRV, AR(1) phi=0.5, L=20", bartlett_lrv_ar1(0.5, 20), 2.8095, 1e-4)
    true_lrv = 1.0 + 2.0 * sum(0.5**k for k in range(1, 200))  # untruncated, unweighted sum of autocorrelations
    check("true LRV sum of all autocorrelations = (1+phi)/(1-phi), phi=0.5", true_lrv, 3.0, 1e-12)
    check("NW rule of thumb floor(4 (T/100)^(2/9)), T=500", nw_rule_of_thumb(500), 5, 0)
    check("NW rule of thumb, T=2500", nw_rule_of_thumb(2500), 8, 0)
    check("Stock-Watson 0.75 T^(1/3), T=2500", 0.75 * 2500 ** (1 / 3), 10.1790, 1e-4)
    check("Andrews Bartlett bandwidth, rho=0.5, T=500", andrews_bartlett_bandwidth(0.5, 500), 11.0063, 1e-4)
    se_factor = math.sqrt(true_lrv / bartlett_lrv_ar1(0.5, 2))
    check("SE understatement factor sqrt(3 / 1.833) at L=2", se_factor, 1.2792, 1e-4)


def overlapping_returns() -> None:
    print("\n# 3. Overlapping 20-day returns on a persistent signal (null: no predictability)")
    print("#    backs: Core concepts (overlapping returns), Worked example 2; cards stat-diag-overlapping-lags, stat-diag-hansen-hodrick")
    rng = np.random.default_rng(2024)
    t_obs, h, phi, reps = 2500, 20, 0.95, 1000
    inflation = 1.0 + 2.0 * sum(phi**k * (1.0 - k / h) for k in range(1, h))
    check("theoretical score variance inflation 1+2 sum phi^k (1-k/h)", inflation, 14.6225, 1e-4)
    check("implied sd of the OLS t-stat, sqrt(inflation)", math.sqrt(inflation), 3.8239, 1e-4)
    limit = 1.0 + 2.0 * sum(1.0 - k / h for k in range(1, h))  # the inflation sum at phi = 1
    check("limit phi -> 1: inflation sum equals h", limit, 20.0, 1e-9)
    check("limit phi -> 1: t-stat sd sqrt(inflation)", math.sqrt(limit), 4.4721, 1e-4)
    l_rule = nw_rule_of_thumb(t_obs)
    names = ["OLS", f"NW L={l_rule}", "NW L=20", "NW L=40", "HH L=19", "non-overlap OLS"]
    rejections = dict.fromkeys(names, 0)
    abs_t: dict[str, list[float]] = {k: [] for k in names}
    tstats_ols = []
    for _ in range(reps):
        n_total = t_obs + h + 200
        x = np.empty(n_total)
        x[0] = rng.standard_normal() / math.sqrt(1 - phi**2)
        eps = rng.standard_normal(n_total) * 1.0
        for i in range(1, n_total):
            x[i] = phi * x[i - 1] + eps[i]
        r = rng.standard_normal(n_total)
        csum = np.concatenate([[0.0], np.cumsum(r)])
        idx = np.arange(200, 200 + t_obs)
        y = csum[idx + h + 1] - csum[idx + 1]  # r_{t+1} + ... + r_{t+h}
        X = np.column_stack([np.ones(t_obs), x[idx]])
        b, e, xi = ols(X, y)
        se = {
            "OLS": cov_classical(X, e, xi),
            f"NW L={l_rule}": cov_hac(X, e, xi, l_rule),
            "NW L=20": cov_hac(X, e, xi, 20),
            "NW L=40": cov_hac(X, e, xi, 40),
            "HH L=19": cov_hac(X, e, xi, h - 1, kernel="uniform"),
        }
        tvals = {k: b[1] / math.sqrt(max(v[1, 1], 1e-300)) for k, v in se.items()}
        sub = np.arange(0, t_obs, h)
        bn, en, xin = ols(X[sub], y[sub])
        tvals["non-overlap OLS"] = bn[1] / math.sqrt(cov_classical(X[sub], en, xin)[1, 1])
        tstats_ols.append(tvals["OLS"])
        for k, tv in tvals.items():
            rejections[k] += abs(tv) > 1.96
            abs_t[k].append(abs(tv))
    check("MC sd of OLS t-stat", float(np.std(tstats_ols)), 3.84, 0.01)
    expected = {
        "OLS": (0.606, 7.48),
        f"NW L={l_rule}": (0.202, 2.99),
        "NW L=20": (0.110, 2.36),
        "NW L=40": (0.088, 2.18),
        "HH L=19": (0.061, 2.00),
        "non-overlap OLS": (0.053, 1.97),
    }
    for k in names:
        check(f"rejection rate at 5%, {k}", rejections[k] / reps, expected[k][0], 0.003)
        check(f"95th percentile of |t| under the null, {k}", float(np.quantile(abs_t[k], 0.95)), expected[k][1], 0.01)


def leverage_and_influence() -> None:
    print("\n# 4. Leverage, LOO residual and Cook's distance: x=(1,2,3,4,10), y=(1,2,3,4,5)")
    print("#    backs: Worked example 3; cards stat-diag-masking-hand, stat-diag-loo-identity, stat-diag-cooks-distance")
    x = np.array([1.0, 2.0, 3.0, 4.0, 10.0])
    y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    X = np.column_stack([np.ones(5), x])
    b, e, xi = ols(X, y)
    n, p = X.shape
    h = np.einsum("ij,jk,ik->i", X, xi, X)
    s2 = e @ e / (n - p)
    cook = e**2 * h / (p * s2 * (1 - h) ** 2)
    check("S_xx", float(np.sum((x - x.mean()) ** 2)), 50.0, 1e-12)
    check("S_xy", float(np.sum((x - x.mean()) * (y - y.mean()))), 20.0, 1e-12)
    for i, r in enumerate([-0.8, -0.2, 0.4, 1.0, -0.4]):
        check(f"residual {i + 1}", e[i], r, 1e-12)
    check("RSS", e @ e, 2.0, 1e-12)
    check("(x_5 - xbar)^2", (x[4] - x.mean()) ** 2, 36.0, 1e-12)
    check("e_5^2", e[4] ** 2, 0.16, 1e-12)
    check("1 - h_55", 1 - h[4], 0.08, 1e-12)
    check("intercept", b[0], 1.4, 1e-12)
    check("slope", b[1], 0.4, 1e-12)
    check("residual of x=10 point", e[4], -0.4, 1e-12)
    check("leverage h_55 = 1/n + (x-xbar)^2/Sxx", h[4], 0.92, 1e-12)
    check("leverage threshold 2p/n", 2 * p / n, 0.8, 1e-12)
    check("LOO (PRESS) residual e/(1-h)", e[4] / (1 - h[4]), -5.0, 1e-9)
    check("s^2", s2, 2 / 3, 1e-12)
    check("Cook's distance of x=10 point", cook[4], 17.25, 1e-9)
    check("Cook's distance of x=4 point (largest residual)", cook[3], 0.234375, 1e-9)
    bl, *_ = np.linalg.lstsq(X[:4], y[:4], rcond=None)
    check("slope without x=10 point", bl[1], 1.0, 1e-12)
    # LOO identity: beta - beta_(i) = (X'X)^{-1} x_i e_i / (1 - h_i)
    delta = xi @ X[4] * e[4] / (1 - h[4])
    check("LOO identity: beta - beta_(5), slope component", delta[1], -0.6, 1e-9)
    check("internally studentised residual e/(s sqrt(1-h))", e[4] / math.sqrt(s2 * (1 - h[4])), -1.7321, 1e-4)


def collinearity() -> None:
    print("\n# 5. Multicollinearity and VIF")
    print("#    backs: Core concepts (VIF), Worked example 4; cards stat-diag-vif, stat-diag-collinear-sum-diff")
    # VIF and contrast variances from the inverse of the regressor correlation matrix (not the closed forms)
    for rho, vif in [(0.9, 5.2632), (0.95, 10.2564), (0.99, 50.2513)]:
        check(f"VIF = [R^-1]_11, rho={rho}", float(np.linalg.inv(np.array([[1.0, rho], [rho, 1.0]]))[0, 0]), vif, 1e-4)
    r_inv = np.linalg.inv(np.array([[1.0, 0.9], [0.9, 1.0]]))
    check("SE inflation sqrt(VIF), rho=0.9", math.sqrt(r_inv[0, 0]), 2.2942, 1e-4)
    ones, diff = np.array([1.0, 1.0]), np.array([1.0, -1.0])
    check("var factor of b1+b2, c' R^-1 c, rho=0.9 (closed form 2/(1+rho))", float(ones @ r_inv @ ones), 1.0526, 1e-4)
    check("var factor of b1-b2, c' R^-1 c, rho=0.9 (closed form 2/(1-rho))", float(diff @ r_inv @ diff), 20.0, 1e-9)
    rng = np.random.default_rng(5)
    n, reps, rho = 250, 2000, 0.95
    b1, bsum, neg = [], [], 0
    vifs = []
    for _ in range(reps):
        z1 = rng.standard_normal(n)
        z2 = rho * z1 + math.sqrt(1 - rho**2) * rng.standard_normal(n)
        y = 0.5 * z1 + 0.5 * z2 + rng.standard_normal(n)
        X = np.column_stack([np.ones(n), z1, z2])
        b, _, _ = ols(X, y)
        b1.append(b[1])
        bsum.append(b[1] + b[2])
        neg += b[1] < 0
        r = np.corrcoef(z1, z2)[0, 1]
        vifs.append(1 / (1 - r**2))
    check("rho=0.95, n=250: MC sd of b1", float(np.std(b1)), 0.2029, 0.0005)
    check("theory sd of b1 sqrt(VIF/n)", math.sqrt(1 / (1 - rho**2) / n), 0.2025, 1e-4)
    check("MC sd of b1+b2", float(np.std(bsum)), 0.0646, 0.0005)
    check("theory sd of b1+b2 sqrt(2/((1+rho) n))", math.sqrt(2 / (1.95 * n)), 0.0641, 1e-4)
    check("share of samples with b1 < 0 (true b1 = 0.5)", neg / reps, 0.0045, 0.0005)
    check("theory P(b1 < 0) = Phi(-0.5/0.2025)", PHI.cdf(-0.5 / math.sqrt(1 / (1 - rho**2) / n)), 0.0068, 1e-4)
    check("mean sample VIF", float(np.mean(vifs)), 10.33, 0.01)


def clustered() -> None:
    print("\n# 6. Clustered errors: 100 periods x 50 stocks, common time shocks in x and e")
    print("#    backs: Worked example 5; cards stat-diag-moulton, stat-diag-white-in-panel, stat-diag-fama-macbeth-vs-cluster")
    rng = np.random.default_rng(99)
    g, m, rho_x, rho_u, reps = 100, 50, 0.5, 0.25, 1000
    moulton = 1 + (m - 1) * rho_x * rho_u
    check("Moulton factor 1+(m-1) rho_x rho_u", moulton, 7.125, 1e-12)
    check("implied SE ratio sqrt(Moulton)", math.sqrt(moulton), 2.6693, 1e-4)
    groups = np.repeat(np.arange(g), m)
    slopes, se_ols, se_cl, se_fm = [], [], [], []
    rej = {"OLS": 0, "White": 0, "cluster": 0, "Fama-MacBeth": 0}
    for _ in range(reps):
        x = math.sqrt(rho_x) * np.repeat(rng.standard_normal(g), m) + math.sqrt(1 - rho_x) * rng.standard_normal(g * m)
        u = math.sqrt(rho_u) * np.repeat(rng.standard_normal(g), m) + math.sqrt(1 - rho_u) * rng.standard_normal(g * m)
        y = u  # true slope 0
        X = np.column_stack([np.ones(g * m), x])
        b, e, xi = ols(X, y)
        s_o = math.sqrt(cov_classical(X, e, xi)[1, 1])
        s_w = math.sqrt(cov_hc(X, e, xi, "HC1")[1, 1])
        s_c = math.sqrt(cov_cluster(X, e, xi, groups)[1, 1])
        xs, ys = x.reshape(g, m), y.reshape(g, m)
        xc = xs - xs.mean(1, keepdims=True)
        fm = (xc * (ys - ys.mean(1, keepdims=True))).sum(1) / (xc**2).sum(1)
        s_f = fm.std(ddof=1) / math.sqrt(g)
        slopes.append(b[1])
        se_ols.append(s_o)
        se_cl.append(s_c)
        se_fm.append(s_f)
        rej["OLS"] += abs(b[1] / s_o) > 1.96
        rej["White"] += abs(b[1] / s_w) > 1.96
        rej["cluster"] += abs(b[1] / s_c) > 1.96
        rej["Fama-MacBeth"] += abs(fm.mean() / s_f) > 1.96
    check("MC sd of pooled slope / mean OLS SE", float(np.std(slopes) / np.mean(se_ols)), 2.57, 0.01)
    check("mean cluster SE / mean OLS SE", float(np.mean(se_cl) / np.mean(se_ols)), 2.61, 0.01)
    for k, v in {"OLS": 0.448, "White": 0.449, "cluster": 0.052, "Fama-MacBeth": 0.058}.items():
        check(f"rejection rate at 5%, {k}", rej[k] / reps, v, 0.003)


def robust_regression() -> None:
    print("\n# 7. Huber M-estimation and its limits")
    print(
        "#    backs: Core concepts (robust regression), Worked example 6; cards stat-diag-huber-efficiency, stat-diag-m-estimator-leverage"
    )
    check("Huber efficiency at the normal, c=1.345", huber_efficiency(1.345), 0.9500, 1e-4)
    check("MAD normalising constant Phi^{-1}(0.75)", PHI.inv_cdf(0.75), 0.6745, 1e-4)
    rng = np.random.default_rng(3)
    n = 200
    x = rng.standard_normal(n)
    y = 1.0 + 2.0 * x + rng.standard_normal(n)
    X = np.column_stack([np.ones(n), x])
    # vertical outliers: the 10 points with the largest x have y shifted by +20 (x itself is ordinary)
    yv = y.copy()
    yv[np.argsort(x)[-10:]] += 20.0
    # bad leverage: 10 points moved to x = 5 with y = -10
    xl, yl = x.copy(), y.copy()
    xl[:10], yl[:10] = 5.0, -10.0
    Xl = np.column_stack([np.ones(n), xl])
    check("clean data, OLS slope", ols(X, y)[0][1], 2.03, 0.005)
    check("vertical outliers, OLS slope", ols(X, yv)[0][1], 4.07, 0.005)
    check("vertical outliers, Huber slope", huber_irls(X, yv)[1], 2.26, 0.005)
    check("vertical outliers, OLS intercept", ols(X, yv)[0][0], 1.92, 0.005)
    check("vertical outliers, Huber intercept", huber_irls(X, yv)[0], 1.13, 0.005)
    check("bad leverage, OLS slope", ols(Xl, yl)[0][1], -0.38, 0.005)
    check("bad leverage, Huber slope", huber_irls(Xl, yl)[1], 1.47, 0.005)
    lo, hi = np.quantile(yv, [0.05, 0.95])
    check("vertical outliers, OLS slope on y winsorised at 5/95%", ols(X, np.clip(yv, lo, hi))[0][1], 1.97, 0.005)


if __name__ == "__main__":
    heteroskedasticity()
    newey_west_kernel()
    overlapping_returns()
    leverage_and_influence()
    collinearity()
    clustered()
    robust_regression()
    print("\nall robust_inference checks passed")
