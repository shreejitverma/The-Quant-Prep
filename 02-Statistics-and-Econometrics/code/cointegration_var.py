"""Spurious regression, Engle-Granger, Johansen, VECM, VAR, impulse responses and Granger causality.

Backs every number in ``10-Cointegration-and-VAR.md``.
Run ``uv run --no-project --with numpy python 02-Statistics-and-Econometrics/code/cointegration_var.py``;
each printed number is asserted, so drift in the note fails CI.
Simulations use fixed seeds; prose quotes their results as "about" and their tables carry a caption naming the seed.

Critical values are not recalled: the Engle-Granger ones come from MacKinnon (2010), "Critical Values for
Cointegration Tests", Queen's Economics Department Working Paper 1227, Table 2 (tau_c rows, response surface
C(T) = b_inf + b1/T + b2/T^2 + b3/T^3, T = observations in the unit-root regression); the Johansen ones are the
MacKinnon, Haug and Michelis (1999) values for an unrestricted constant, as tabulated in statsmodels
(``coint_tables.py``, p = 0). The script also re-derives each by simulation.
"""

from __future__ import annotations

import math

import numpy as np

# MacKinnon (2010) Table 2, tau_c: (b_inf, b1, b2, b3) by (N, level)
MACKINNON_TAU_C = {
    (1, 0.01): (-3.43035, -6.5393, -16.786, -79.433),
    (1, 0.05): (-2.86154, -2.8903, -4.234, -40.040),
    (1, 0.10): (-2.56677, -1.5384, -2.809, 0.0),
    (2, 0.01): (-3.89644, -10.9519, -22.527, 0.0),
    (2, 0.05): (-3.33613, -6.1101, -6.823, 0.0),
    (2, 0.10): (-3.04445, -4.2412, -2.720, 0.0),
}
MACKINNON_TAU_CT_N2_5 = -3.78057  # MacKinnon (2010) Table 3, tau_ct, N=2, 5%: use when the data drift
# MacKinnon-Haug-Michelis (1999), unrestricted constant, 95% critical values indexed by n - r
JOHANSEN_TRACE_95 = {1: 3.8415, 2: 15.4943}
JOHANSEN_MAXEIG_95 = {1: 3.8415, 2: 14.2639}


def check(name: str, value: float, expected: float, tol: float) -> float:
    """Print a named result and assert it is within ``tol`` of the value quoted in the note."""
    print(f"{name:<64s} {value:12.4f}")
    assert abs(value - expected) <= tol, f"{name}: got {value}, expected {expected} +/- {tol}"
    return value


def cite(name: str, value: float) -> None:
    """Print a published constant quoted in the note; it is cited, not computed, so it is not asserted."""
    print(f"{name:<64s} {value:12.4f}  (cited)")


def mackinnon_cv(n_vars: int, level: float, t: int) -> float:
    b_inf, b1, b2, b3 = MACKINNON_TAU_C[(n_vars, level)]
    return b_inf + b1 / t + b2 / t**2 + b3 / t**3


# ---------------------------------------------------------------- batched simple regressions


def batch_slope_t(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Row-wise OLS of y on [1, x]: slope, its classical t-stat and R^2."""
    t = x.shape[1]
    xc = x - x.mean(1, keepdims=True)
    yc = y - y.mean(1, keepdims=True)
    sxx = (xc**2).sum(1)
    b = (xc * yc).sum(1) / sxx
    e = yc - b[:, None] * xc
    s2 = (e**2).sum(1) / (t - 2)
    r2 = 1.0 - (e**2).sum(1) / (yc**2).sum(1)
    return b, b / np.sqrt(s2 / sxx), r2


def batch_eg_tstat(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Engle-Granger step 2, row-wise: DF t-stat of du_t = gamma u_{t-1} + e on the step-1 residuals."""
    xc = x - x.mean(1, keepdims=True)
    yc = y - y.mean(1, keepdims=True)
    b = (xc * yc).sum(1) / (xc**2).sum(1)
    u = yc - b[:, None] * xc
    du, ul = np.diff(u, axis=1), u[:, :-1]
    g = (du * ul).sum(1) / (ul**2).sum(1)
    e = du - g[:, None] * ul
    s2 = (e**2).sum(1) / (du.shape[1] - 1)
    return g / np.sqrt(s2 / (ul**2).sum(1))


# ---------------------------------------------------------------- single-series tools


def ols(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ beta
    cov = (e @ e / (len(y) - X.shape[1])) * np.linalg.inv(X.T @ X)
    return beta, e, cov


def johansen(levels: np.ndarray, k: int = 1) -> tuple[np.ndarray, np.ndarray, int]:
    """Johansen reduced-rank regression with an unrestricted constant and k-1 lagged differences.

    Returns eigenvalues (descending), eigenvectors (columns, beta candidates) and the effective sample size.
    """
    dy = np.diff(levels, axis=0)
    t_eff = dy.shape[0] - (k - 1)
    z0 = dy[k - 1 :]
    z1 = levels[k - 1 : -1]
    regs = [np.ones((t_eff, 1))] + [dy[k - 1 - j : -j] for j in range(1, k)]
    Z = np.hstack(regs)
    zz = np.hstack([z0, z1])
    coef, *_ = np.linalg.lstsq(Z, zz, rcond=None)
    r0, r1 = np.hsplit(zz - Z @ coef, [z0.shape[1]])
    s00, s01, s11 = r0.T @ r0 / t_eff, r0.T @ r1 / t_eff, r1.T @ r1 / t_eff
    # solve |lambda S11 - S10 S00^-1 S01| = 0 via the symmetric form with L = chol(S11)
    c = np.linalg.cholesky(s11)
    ci = np.linalg.inv(c)
    m = ci @ s01.T @ np.linalg.inv(s00) @ s01 @ ci.T
    lam, v = np.linalg.eigh(m)
    order = np.argsort(lam)[::-1]
    lam, v = lam[order], v[:, order]
    beta = ci.T @ v
    return lam, beta, t_eff


def johansen_stats(lam: np.ndarray, t_eff: int) -> tuple[list[float], list[float]]:
    n = lam.size
    trace = [-t_eff * float(np.sum(np.log(1 - lam[r:]))) for r in range(n)]
    maxeig = [-t_eff * math.log(1 - lam[r]) for r in range(n)]
    return trace, maxeig


# ---------------------------------------------------------------- sections


def spurious_regression() -> None:
    print("\n# 1. Spurious regression: two independent random walks")
    print("#    backs: Worked example 1; cards stat-coint-spurious-symptoms, stat-coint-spurious-t-growth")
    rng = np.random.default_rng(1974)
    reps = 4000
    expected = {100: (0.752, 0.238, 0.061), 250: (0.838, 0.237, 0.055), 1000: (0.927, 0.234, 0.048)}
    for t in (100, 250, 1000):
        x = np.cumsum(rng.standard_normal((reps, t)), axis=1)
        y = np.cumsum(rng.standard_normal((reps, t)), axis=1)
        _, tl, r2 = batch_slope_t(x, y)
        _, td, _ = batch_slope_t(np.diff(x, axis=1), np.diff(y, axis=1))
        check(f"T={t}: share |t| > 1.96, levels", float(np.mean(np.abs(tl) > 1.96)), expected[t][0], 0.002)
        check(f"T={t}: mean R^2, levels", float(np.mean(r2)), expected[t][1], 0.002)
        check(f"T={t}: share |t| > 1.96, differences", float(np.mean(np.abs(td) > 1.96)), expected[t][2], 0.002)
        if t == 250:
            check("T=250: median |t|, levels", float(np.median(np.abs(tl))), 6.8, 0.005)


def engle_granger_critical_values() -> None:
    print("\n# 2. Engle-Granger critical values: MacKinnon (2010) and a simulation under no cointegration")
    print("#    backs: Core concepts (Engle-Granger table), Worked example 2; cards stat-coint-eg-critical-value, stat-coint-eg-wrong-cv")
    t_obs = 500
    t_df = t_obs - 1
    cv = {lvl: mackinnon_cv(2, lvl, t_df) for lvl in (0.01, 0.05, 0.10)}
    cite("MacKinnon tau_c N=2 asymptotic 5%", MACKINNON_TAU_C[(2, 0.05)][0])
    cite("MacKinnon tau_c N=2 asymptotic 1%", MACKINNON_TAU_C[(2, 0.01)][0])
    cite("MacKinnon tau_c N=2 asymptotic 10%", MACKINNON_TAU_C[(2, 0.10)][0])
    cite("MacKinnon tau_c N=1 (plain DF) asymptotic 1%", MACKINNON_TAU_C[(1, 0.01)][0])
    cite("MacKinnon tau_c N=1 (plain DF) asymptotic 5%", MACKINNON_TAU_C[(1, 0.05)][0])
    cite("MacKinnon tau_c N=1 (plain DF) asymptotic 10%", MACKINNON_TAU_C[(1, 0.10)][0])
    cite("MacKinnon tau_ct N=2 (constant and trend) asymptotic 5%", MACKINNON_TAU_CT_N2_5)
    check("MacKinnon N=2 5% at T=499", cv[0.05], -3.3484, 1e-4)
    check("MacKinnon N=2 1% at T=499", cv[0.01], -3.9185, 1e-4)
    rng = np.random.default_rng(1987)
    stats = []
    for _ in range(16):
        x = np.cumsum(rng.standard_normal((2500, t_obs)), axis=1)
        y = np.cumsum(rng.standard_normal((2500, t_obs)), axis=1)
        stats.append(batch_eg_tstat(x, y))
    s = np.concatenate(stats)
    check("simulated 5% quantile of EG t (40,000 null paths, T=500)", float(np.quantile(s, 0.05)), -3.36, 0.005)
    check("simulated 1% quantile of EG t", float(np.quantile(s, 0.01)), -3.93, 0.005)
    check("null rejection rate if DF's -2.86 is (wrongly) used", float(np.mean(s < -2.86154)), 0.151, 0.001)
    assert abs(np.quantile(s, 0.05) - cv[0.05]) < 0.03 and abs(np.quantile(s, 0.01) - cv[0.01]) < 0.03


def simulate_pair(t: int = 1000, phi: float = 0.9, seed: int = 7, drift: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
    """x a random walk (optionally with drift), y = 2 + 1.5 x + u with u a stationary AR(1)."""
    rng = np.random.default_rng(seed)
    x = np.cumsum(drift + rng.standard_normal(t))
    eps = rng.standard_normal(t)
    u = np.empty(t)
    u[0] = eps[0] / math.sqrt(1 - phi**2)
    for i in range(1, t):
        u[i] = phi * u[i - 1] + eps[i]
    return x, 2.0 + 1.5 * x + u


def engle_granger_example() -> None:
    print("\n# 3. Engle-Granger on a simulated cointegrated pair: y = 2 + 1.5 x + u, u AR(1) phi=0.9, T=1000")
    print("#    backs: Worked examples 3, 4; cards stat-coint-ecm-alpha, stat-coint-power-short-sample")
    rng = np.random.default_rng(8)
    x, y = simulate_pair()
    t = x.size
    b, uh, _ = ols(np.column_stack([np.ones(t), x]), y)
    check("step 1: intercept", b[0], 1.497, 0.0005)
    check("step 1: hedge ratio beta", b[1], 1.492, 0.0005)
    eg_t = float(batch_eg_tstat(x[None, :], y[None, :])[0])
    check("step 2: EG t-stat on residuals", eg_t, -6.88, 0.005)
    check("5% critical value at T=999 (reject if below)", mackinnon_cv(2, 0.05, t - 1), -3.3423, 1e-4)
    # reverse regression: superconsistency makes 1/beta(x on y) close to beta(y on x)
    br, _, _ = ols(np.column_stack([np.ones(t), y]), x)
    check("reverse regression: 1 / slope of x on y", 1.0 / br[1], 1.498, 0.0005)
    # error-correction model: dy_t = c + alpha u_{t-1} + gamma dx_t + e_t
    dy, dx = np.diff(y), np.diff(x)
    ecm, _, ecm_cov = ols(np.column_stack([np.ones(t - 1), uh[:-1], dx]), dy)
    check("ECM: adjustment alpha (true -0.1)", ecm[1], -0.0908, 0.00005)
    check("ECM: t-stat of alpha", ecm[1] / math.sqrt(ecm_cov[1, 1]), -6.88, 0.005)
    check("ECM: short-run gamma (true 1.5)", ecm[2], 1.516, 0.0005)
    check("implied half-life ln 0.5 / ln(1 + alpha) (true 6.58)", math.log(0.5) / math.log(1 + ecm[1]), 7.29, 0.005)
    check("true half-life ln 0.5 / ln 0.9", math.log(0.5) / math.log(0.9), 6.5788, 1e-4)
    # power of the EG test at T = 250 for several spread persistences
    print("  power of the 5% EG test, T = 250, 2000 paths each")
    expected = {0.9: 0.859, 0.95: 0.300, 0.98: 0.094}
    for phi, hl in {0.9: 6.6, 0.95: 13.5, 0.98: 34.3}.items():
        check(f"  phi={phi}: half-life ln 0.5 / ln phi", math.log(0.5) / math.log(phi), hl, 0.05)
    for phi, power in expected.items():
        n, reps = 250, 2000
        xs = np.cumsum(rng.standard_normal((reps, n)), axis=1)
        us = np.zeros((reps, n))
        es = rng.standard_normal((reps, n))
        for i in range(1, n):
            us[:, i] = phi * us[:, i - 1] + es[:, i]
        stat = batch_eg_tstat(xs, 1.5 * xs + us)
        check(f"  phi={phi}: rejection rate", float(np.mean(stat < mackinnon_cv(2, 0.05, n - 1))), power, 0.002)


def johansen_section() -> None:
    print("\n# 4. Johansen trace and max-eigenvalue tests, VECM (x drifts 0.1 per step, so the data trend)")
    print("#    backs: Worked examples 5, 6; cards stat-coint-deterministic-case, stat-coint-weak-exogeneity")
    x, y = simulate_pair(drift=0.1)
    t = x.size
    lam, beta, t_eff = johansen(np.column_stack([y, x]), k=1)
    trace, maxeig = johansen_stats(lam, t_eff)
    check("eigenvalue 1", lam[0], 0.0456, 1e-4)
    check("eigenvalue 2", lam[1], 0.0001, 1e-4)
    check("trace r=0", trace[0], 46.66, 0.005)
    check("trace r<=1", trace[1], 0.07, 0.005)
    check("max-eig r=0", maxeig[0], 46.59, 0.005)
    check("max-eig r=1", maxeig[1], 0.07, 0.005)
    cite("MHM 95% trace cv, n-r=2", JOHANSEN_TRACE_95[2])
    cite("MHM 95% trace cv, n-r=1", JOHANSEN_TRACE_95[1])
    cite("MHM 95% max-eig cv, n-r=2", JOHANSEN_MAXEIG_95[2])
    cite("MHM 95% max-eig cv, n-r=1", JOHANSEN_MAXEIG_95[1])
    b = beta[:, 0] / beta[0, 0]
    check("normalised cointegrating vector: coefficient on x (true -1.5)", b[1], -1.495, 0.0005)
    # alpha by OLS of dy on the cointegration error and a constant (the k=1 VECM)
    ect = np.column_stack([y, x])[:-1] @ b
    dz = np.diff(np.column_stack([y, x]), axis=0)
    Z = np.column_stack([np.ones(t - 1), ect])
    a_y, _, cov_y = ols(Z, dz[:, 0])
    a_x, _, cov_x = ols(Z, dz[:, 1])
    check("VECM alpha_y (true -0.1)", a_y[1], -0.076, 0.0005)
    check("t-stat alpha_y", a_y[1] / math.sqrt(cov_y[1, 1]), -3.37, 0.005)
    check("VECM alpha_x (true 0)", a_x[1], 0.009, 0.0005)
    check("t-stat alpha_x (weak exogeneity of x)", a_x[1] / math.sqrt(cov_x[1, 1]), 0.77, 0.005)

    print("  simulated 95% quantiles under the null (T = 500, 3000 paths each)")
    rng2 = np.random.default_rng(1991)
    tr0, mx0, tr1_drift, tr1_nodrift = [], [], [], []
    for _ in range(3000):
        # r = 0: two independent random walks with drift
        levels = np.cumsum(0.2 + rng2.standard_normal((500, 2)), axis=0)
        lam0, _, t0 = johansen(levels, k=1)
        tr, mx = johansen_stats(lam0, t0)
        tr0.append(tr[0])
        mx0.append(mx[0])
        # r = 1: a cointegrated pair, with and without drift in the common trend
        for drift, store in ((0.2, tr1_drift), (0.0, tr1_nodrift)):
            w = np.cumsum(drift + rng2.standard_normal(500))
            e = rng2.standard_normal(500)
            s = np.empty(500)
            s[0] = e[0]
            for i in range(1, 500):
                s[i] = 0.5 * s[i - 1] + e[i]
            lam1, _, t1 = johansen(np.column_stack([w + s, w]), k=1)
            store.append(johansen_stats(lam1, t1)[0][1])
    check("  trace, n-r=2, r=0 true (MHM asymptotic 15.49)", float(np.quantile(tr0, 0.95)), 15.76, 0.005)
    check("  max-eig, n-r=2, r=0 true (MHM asymptotic 14.26)", float(np.quantile(mx0, 0.95)), 14.39, 0.005)
    check("  trace, n-r=1, r=1 true, data drift (MHM 3.84)", float(np.quantile(tr1_drift, 0.95)), 4.35, 0.005)
    check("  trace, n-r=1, r=1 true, NO drift (wrong case)", float(np.quantile(tr1_nodrift, 0.95)), 8.26, 0.005)
    rej_drift = float(np.mean(np.array(tr1_drift) > JOHANSEN_TRACE_95[1]))
    rej_nodrift = float(np.mean(np.array(tr1_nodrift) > JOHANSEN_TRACE_95[1]))
    check("  rejection rate of true r<=1 at 3.84, data drift", rej_drift, 0.067, 0.0005)
    check("  rejection rate of true r<=1 at 3.84, NO drift", rej_nodrift, 0.298, 0.0005)


def var_section() -> None:
    print("\n# 5. VAR(1): estimation, Granger causality, impulse responses")
    print("#    backs: Worked examples 7, 8; cards stat-coint-irf-ordering, stat-coint-irf-var1, stat-coint-var-stationarity")
    A = np.array([[0.5, 0.2], [0.0, 0.6]])
    S = np.array([[1.0, 0.5], [0.5, 1.0]])
    check("largest eigenvalue of A", float(max(np.linalg.eigvals(A).real)), 0.6, 1e-12)
    check("smallest eigenvalue of A", float(min(np.linalg.eigvals(A).real)), 0.5, 1e-12)
    A2 = A @ A
    check("A^2[0,1]: response of y1 to a y2 shock at h=2", A2[0, 1], 0.22, 1e-12)
    check("A^2[0,0]", A2[0, 0], 0.25, 1e-12)
    check("A^2[1,1]", A2[1, 1], 0.36, 1e-12)
    # stationary covariance: vec(G0) = (I - A kron A)^{-1} vec(S)
    g0 = np.linalg.solve(np.eye(4) - np.kron(A, A), S.reshape(-1)).reshape(2, 2)
    check("stationary var of y1", g0[0, 0], 1.6786, 1e-4)
    check("stationary cov of y1, y2", g0[0, 1], 0.9821, 1e-4)
    check("stationary var of y2", g0[1, 1], 1.5625, 1e-4)
    # orthogonalised impulse responses depend on the Cholesky ordering
    P12 = np.linalg.cholesky(S)
    perm = np.array([[0, 1], [1, 0]])
    P21 = perm @ np.linalg.cholesky(perm @ S @ perm) @ perm
    check("order (y1,y2): impact of y2 shock on y1", P12[0, 1], 0.0, 1e-12)
    check("order (y1,y2): impact of y2 shock on y2", P12[1, 1], 0.8660, 1e-4)
    check("order (y2,y1): impact of y2 shock on y1", P21[0, 1], 0.5, 1e-12)
    check("order (y2,y1): impact of y2 shock on y2", P21[1, 1], 1.0, 1e-12)
    check("order (y2,y1): response of y1 at h=1 to y2 shock", (A @ P21)[0, 1], 0.45, 1e-12)
    check("order (y1,y2): response of y1 at h=1 to y2 shock", (A @ P12)[0, 1], 0.1732, 1e-4)
    # simulate, estimate equation by equation, test Granger causality
    rng = np.random.default_rng(11)
    t = 1000
    L = np.linalg.cholesky(S)
    z = np.zeros((t + 100, 2))
    shocks = rng.standard_normal((t + 100, 2)) @ L.T
    for i in range(1, t + 100):
        z[i] = A @ z[i - 1] + shocks[i]
    z = z[100:]
    X = np.column_stack([np.ones(t - 1), z[:-1]])
    b1, e1, c1 = ols(X, z[1:, 0])
    b2, e2, c2 = ols(X, z[1:, 1])
    check("A_hat[0,0] (true 0.5)", b1[1], 0.468, 0.0005)
    check("A_hat[0,1] (true 0.2)", b1[2], 0.216, 0.0005)
    check("A_hat[1,0] (true 0.0)", b2[1], -0.007, 0.0005)
    check("A_hat[1,1] (true 0.6)", b2[2], 0.600, 0.0005)
    wald_21 = b1[2] ** 2 / c1[2, 2]
    wald_12 = b2[1] ** 2 / c2[1, 1]
    check("Wald: y2 does not Granger-cause y1 (chi2_1 cv 3.841)", wald_21, 43.75, 0.005)
    check("Wald: y1 does not Granger-cause y2", wald_12, 0.05, 0.005)
    resid_corr = float(np.corrcoef(e1, e2)[0, 1])
    check("residual correlation (true 0.5)", resid_corr, 0.504, 0.0005)


if __name__ == "__main__":
    spurious_regression()
    engle_granger_critical_values()
    engle_granger_example()
    johansen_section()
    var_section()
    print("\nall cointegration_var checks passed")
