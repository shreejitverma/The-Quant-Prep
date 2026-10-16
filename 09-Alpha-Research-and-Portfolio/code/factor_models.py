"""Cross-sectional factor models on synthetic data with known true factors.

Every number quoted in 04-Cross-Sectional-Factor-Models.md is printed and asserted here.

Model: r_it = sum_k X_ikt f_kt + u_it, with 10 industry dummies (no intercept, so industries carry
the market), three standardised style exposures (size, value, momentum) that drift slowly, and
specific volatility that is higher for small names.

1. Cross-sectional regressions each month: OLS versus WLS with 1/specific-variance weights versus
   WLS with sqrt(market cap) weights (the Barra convention); recovery error against the truth.
2. Fama-MacBeth premia and t-statistics.
3. Factor-mimicking (pure factor) portfolios: rows of (X'WX)^-1 X'W, unit own exposure, zero others.
4. Specific risk estimated from residuals.
5. Risk decomposition of a signal-weighted book, before and after neutralisation.
6. Statistical (PCA) factor model: how much of each true factor's return the top principal
   components span.

Run: uv run --no-project --with numpy python 09-Alpha-Research-and-Portfolio/code/factor_models.py
"""

from __future__ import annotations

import numpy as np

N, T, N_IND = 1000, 120, 10
STYLES = ["size", "value", "momentum"]
STYLE_MEAN = np.array([-0.001, 0.003, 0.005])
STYLE_VOL = np.array([0.015, 0.015, 0.020])


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> float:
    print(f"{label}: {value:{fmt}}")
    assert abs(value - expected) <= tol, f"{label}: {value} not within {tol} of {expected}"
    if expected != 0:  # the printed value must equal the literal the note quotes, at the printed rounding
        assert f"{value:{fmt}}" == f"{expected:{fmt}}", f"{label}: prints {value:{fmt}}, note quotes {expected:{fmt}}"
    return value


def simulate(seed: int = 42) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    industry = rng.integers(0, N_IND, N)
    ind_dummies = np.eye(N_IND)[industry]  # N x 10
    styles = np.empty((T, N, 3))
    styles[0] = rng.standard_normal((N, 3))
    phi = 0.95
    for t in range(1, T):
        styles[t] = phi * styles[t - 1] + np.sqrt(1 - phi**2) * rng.standard_normal((N, 3))
    X = np.concatenate([np.broadcast_to(ind_dummies, (T, N, N_IND)), styles], axis=2)  # T x N x 13
    market = rng.normal(0.006, 0.045, T)
    f_ind = market[:, None] + rng.normal(0.0, 0.02, (T, N_IND))
    f_sty = STYLE_MEAN + STYLE_VOL * rng.standard_normal((T, 3))
    f = np.concatenate([f_ind, f_sty], axis=1)  # T x 13
    size0 = styles[0, :, 0]
    spec_vol = 0.09 * np.exp(-0.25 * size0)  # small names are more volatile
    cap = np.exp(1.2 * size0)
    u = spec_vol * rng.standard_normal((T, N))
    r = np.einsum("tnk,tk->tn", X, f) + u
    return {"X": X, "f": f, "r": r, "spec_vol": spec_vol, "cap": cap, "industry": industry}


def wls(X: np.ndarray, r: np.ndarray, w: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Weighted least squares: returns factor returns and the pure-factor-portfolio matrix H."""
    XtW = X.T * w
    H = np.linalg.solve(XtW @ X, XtW)
    return H @ r, H


def section_regressions(d: dict[str, np.ndarray]) -> np.ndarray:
    print("== 1. Cross-sectional regressions ==")
    X, f, r, sv, cap = d["X"], d["f"], d["r"], d["spec_vol"], d["cap"]
    weights = {"ols": np.ones(N), "wls_inv_var": 1 / sv**2, "wls_sqrt_cap": np.sqrt(cap)}
    est = {k: np.array([wls(X[t], r[t], w)[0] for t in range(T)]) for k, w in weights.items()}
    rmse = {k: np.sqrt(((e - f) ** 2).mean(axis=0)) for k, e in est.items()}
    expected = {
        "ols": [0.00308, 0.00281, 0.00290],
        "wls_inv_var": [0.00263, 0.00253, 0.00256],
        "wls_sqrt_cap": [0.00264, 0.00255, 0.00257],
    }
    for k in weights:
        for j, name in enumerate(STYLES):
            check(f"RMSE of {name} factor return, {k}", rmse[k][N_IND + j], expected[k][j], 0.00002, ".5f")
    for j, name in enumerate(STYLES):
        cut = 1 - rmse["wls_inv_var"][N_IND + j] / rmse["ols"][N_IND + j]
        check(f"WLS error reduction versus OLS, {name}", cut, {"size": 0.144, "value": 0.101, "momentum": 0.118}[name], 0.001, ".3f")
    # Theoretical standard error of the WLS estimate with the true weights, averaged over months.
    se = np.mean([np.sqrt(np.diag(np.linalg.inv((X[t].T / sv**2) @ X[t]))) for t in range(T)], axis=0)
    check("theoretical WLS standard error of the value factor return", se[N_IND + 1], 0.00269, 0.00002, ".5f")
    check(
        "correlation of estimated and true value factor returns (WLS)",
        np.corrcoef(est["wls_inv_var"][:, N_IND + 1], f[:, N_IND + 1])[0, 1],
        0.987,
        0.002,
        ".3f",
    )
    check(
        "correlation of estimated and true industry-0 factor returns (WLS)",
        np.corrcoef(est["wls_inv_var"][:, 0], f[:, 0])[0, 1],
        0.9881,
        0.0002,
        ".4f",
    )
    return est["wls_inv_var"]


def section_fama_macbeth(d: dict[str, np.ndarray], f_hat: np.ndarray) -> None:
    print("== 2. Fama-MacBeth ==")
    f = d["f"]
    for j, name in enumerate(STYLES):
        k = N_IND + j
        m, s = f_hat[:, k].mean(), f_hat[:, k].std(ddof=1)
        t_stat = m / (s / np.sqrt(T))
        check(
            f"realised mean of true {name} factor return (% per month)",
            100 * f[:, k].mean(),
            {"size": -0.163, "value": 0.349, "momentum": 0.684}[name],
            0.001,
            ".3f",
        )
        exp_mean = {"size": -0.149, "value": 0.376, "momentum": 0.677}[name]
        exp_t = {"size": -1.04, "value": 2.59, "momentum": 3.56}[name]
        check(f"Fama-MacBeth mean {name} premium (% per month)", 100 * m, exp_mean, 0.001, ".3f")
        check(f"Fama-MacBeth t-stat {name}", t_stat, exp_t, 0.01, ".2f")
    # The population t-stat a 120-month sample delivers on average for value: mean/vol*sqrt(T).
    check("expected value t-stat from population moments", 0.003 / 0.015 * np.sqrt(T), 2.19, 0.01, ".2f")


def section_pure_factor_portfolios(d: dict[str, np.ndarray]) -> None:
    print("== 3. Pure factor portfolios ==")
    X, r, sv, industry = d["X"][-1], d["r"][-1], d["spec_vol"], d["industry"]
    f_hat, H = wls(X, r, 1 / sv**2)
    check("max |H X - I| (unit own exposure, zero to all others)", float(np.abs(H @ X - np.eye(X.shape[1])).max()), 0.0, 1e-10, ".1e")
    value = H[N_IND + 1]
    check("value portfolio return equals its WLS factor return", value @ r - f_hat[N_IND + 1], 0.0, 1e-12, ".1e")
    check("value portfolio net weight", value.sum(), 0.0, 1e-10, ".1e")
    net_by_ind = np.array([value[industry == g].sum() for g in range(N_IND)])
    check("value portfolio max |net weight| within any industry", float(np.abs(net_by_ind).max()), 0.0, 1e-10, ".1e")
    check("value portfolio gross weight", np.abs(value).sum(), 0.814, 0.001, ".3f")
    check("value portfolio long side", value[value > 0].sum(), 0.407, 0.001, ".3f")
    ind0 = H[0]
    check("industry-0 portfolio net weight", ind0.sum(), 1.0000, 1e-10, ".4f")
    check("industry-0 portfolio weight inside industry 0", ind0[industry == 0].sum(), 1.0000, 1e-10, ".4f")


def section_specific_risk(d: dict[str, np.ndarray]) -> None:
    print("== 4. Specific risk ==")
    X, r, sv = d["X"], d["r"], d["spec_vol"]
    resid = np.array([r[t] - X[t] @ wls(X[t], r[t], 1 / sv**2)[0] for t in range(T)])
    sv_hat = resid.std(axis=0, ddof=1)
    check("mean estimated / true specific vol", float((sv_hat / sv).mean()), 0.993, 0.002, ".3f")
    check("cross-sectional sd of estimated / true specific vol", float((sv_hat / sv).std()), 0.065, 0.002, ".3f")
    check("theoretical sd of the ratio, 1/sqrt(2T)", 1 / np.sqrt(2 * T), 0.065, 0.001, ".3f")


def section_risk_decomposition(d: dict[str, np.ndarray], f_hat: np.ndarray) -> None:
    print("== 5. Risk decomposition and neutralisation ==")
    rng = np.random.default_rng(5)
    X, sv, industry = d["X"][-1], d["spec_vol"], d["industry"]
    F = np.cov(f_hat, rowvar=False)  # 13 x 13 factor covariance from estimated factor returns
    signal = 0.5 * X[:, N_IND + 1] + 0.3 * X[:, N_IND + 2] + 0.8 * (industry == 0) + rng.standard_normal(N)

    def book(s: np.ndarray) -> np.ndarray:
        s = s - s.mean()
        return s / np.abs(s).sum() * 2.0  # gross 2: 100% long, 100% short

    def decompose(h: np.ndarray, label: str, exp: list[float]) -> None:
        x = X.T @ h
        fac = x @ F @ x
        spec = (h**2 * sv**2).sum()
        total = fac + spec
        contrib = x * (F @ x) / total  # Euler contributions to variance, sum to the factor share
        check(f"{label}: total vol (% per month)", 100 * np.sqrt(total), exp.pop(0), 0.006, ".2f")
        check(f"{label}: value exposure", x[N_IND + 1], exp.pop(0), 0.0011, ".3f")
        check(f"{label}: momentum exposure", x[N_IND + 2], exp.pop(0), 0.0011, ".3f")
        check(f"{label}: industries share of variance", contrib[:N_IND].sum(), exp.pop(0), 0.0011, ".3f")
        check(f"{label}: size share of variance", contrib[N_IND], exp.pop(0), 0.0011, ".3f")
        check(f"{label}: value share of variance", contrib[N_IND + 1], exp.pop(0), 0.0011, ".3f")
        check(f"{label}: momentum share of variance", contrib[N_IND + 2], exp.pop(0), 0.0011, ".3f")
        check(f"{label}: specific share of variance", spec / total, exp.pop(0), 0.0011, ".3f")

    h_raw = book(signal)
    decompose(h_raw, "raw book", [2.50, 1.036, 0.732, 0.048, 0.005, 0.455, 0.399, 0.093])
    # Neutralise against industries, size and momentum; keep value.
    B = np.delete(X, N_IND + 1, axis=1)
    h_val = book(signal - B @ np.linalg.lstsq(B, signal, rcond=None)[0])
    decompose(h_val, "value-only book", [1.89, 1.088, 0.0, 0.0, 0.0, 0.836, 0.0, 0.164])
    check("value-only book: max |exposure to industries, size, momentum|", float(np.abs(B.T @ h_val).max()), 0.0, 1e-10, ".1e")
    # Neutralise against everything: a pure residual (specific-risk) book.
    h_res = book(signal - X @ np.linalg.lstsq(X, signal, rcond=None)[0])
    decompose(h_res, "fully neutral book", [0.77, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
    check("fully neutral book: max |factor exposure|", float(np.abs(X.T @ h_res).max()), 0.0, 1e-10, ".1e")


def section_pca(d: dict[str, np.ndarray]) -> None:
    print("== 6. Statistical factor model (PCA) ==")
    r, f = d["r"], d["f"]
    R = r - r.mean(axis=0)
    eig, vec = np.linalg.eigh(R @ R.T / N)  # T x T dual problem
    order = np.argsort(eig)[::-1]
    eig, vec = eig[order], vec[:, order]
    sigma2 = float(d["spec_vol"].__pow__(2).mean())
    mp_edge = sigma2 * (1 + np.sqrt(T / N)) ** 2  # Marchenko-Pastur upper edge for the dual T x T matrix
    n_above = int((eig > mp_edge).sum())
    check("Marchenko-Pastur upper edge (dual matrix)", mp_edge, 0.01680, 0.00001, ".5f")
    check("eigenvalues above the noise edge", n_above, 16, 0, "d")
    check("top eigenvalue share of total variance", eig[0] / eig.sum(), 0.170, 0.001, ".3f")
    rng = np.random.default_rng(9)
    counts = []
    for _ in range(20):
        u = d["spec_vol"] * rng.standard_normal((T, N))
        u -= u.mean(axis=0)
        counts.append(int((np.linalg.eigvalsh(u @ u.T / N) > mp_edge).sum()))
    check("pure heteroskedastic noise: mean eigenvalues above the edge (20 draws)", float(np.mean(counts)), 3.95, 0.001, ".2f")
    expected = {
        1: [0.833, 0.037, 0.002, 0.000],
        10: [0.884, 0.471, 0.570, 0.787],
        13: [0.893, 0.523, 0.605, 0.841],
    }
    for k in (1, 10, 13):
        P = vec[:, :k]  # PC time series (orthonormal columns)
        fc = f - f.mean(axis=0)
        r2 = 1 - ((fc - P @ (P.T @ fc)) ** 2).sum(axis=0) / (fc**2).sum(axis=0)
        check(f"k={k}: mean R^2 of industry factors on PCs", float(r2[:N_IND].mean()), expected[k][0], 0.001, ".3f")
        for j, name in enumerate(STYLES):
            check(f"k={k}: R^2 of {name} factor on PCs", float(r2[N_IND + j]), expected[k][j + 1], 0.001, ".3f")


def section_parameter_count() -> None:
    print("== 0. Parameter count ==")
    n, k = 1000, 13
    check("free parameters in a sample covariance, N=1000", n * (n + 1) // 2, 500500, 0, "d")
    check("free parameters in a 13-factor model, N=1000", n * k + k * (k + 1) // 2 + n, 14091, 0, "d")


def main() -> None:
    section_parameter_count()
    d = simulate()
    f_hat = section_regressions(d)
    section_fama_macbeth(d, f_hat)
    section_pure_factor_portfolios(d)
    section_specific_risk(d)
    section_risk_decomposition(d, f_hat)
    section_pca(d)


if __name__ == "__main__":
    main()
