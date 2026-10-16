"""Covariance estimation: sample noise, Ledoit-Wolf shrinkage, factor models, EWMA and RMT cleaning.

Backs the numbers in 11-Covariance-Estimation-and-Shrinkage.md.

1. EWMA bookkeeping: decay <-> half-life, effective sample size, mean age.
2. Parameter counts: full covariance versus a k-factor model.
3. Marchenko-Pastur: sample eigenvalues of pure noise spread over [(1-sqrt q)^2, (1+sqrt q)^2].
4. Constant-correlation target on a 3-asset toy covariance.
5. Ledoit-Wolf analytic shrinkage intensity, identity target (Ledoit and Wolf 2004, JMVA)
   and constant-correlation target (Ledoit and Wolf 2004, "Honey, I Shrunk the Sample Covariance Matrix").
6. Out-of-sample variance of the global minimum variance portfolio built from each estimator,
   measured under the known true covariance of a simulated factor market.

Every printed number is asserted so drift is caught.

Run: uv run --no-project --with numpy python 09-Alpha-Research-and-Portfolio/code/covariance_shrinkage.py
"""

from __future__ import annotations

import math

import numpy as np


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> None:
    print(f"{label}: {value:{fmt}}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected} +/- {tol}"
    if expected != 0:  # the printed value must equal the literal the note quotes, at the printed rounding
        assert f"{value:{fmt}}" == f"{expected:{fmt}}", f"{label}: prints {value:{fmt}}, note quotes {expected:{fmt}}"


# ----------------------------------------------------------------------------
# Estimators
# ----------------------------------------------------------------------------


def sample_cov(x: np.ndarray) -> np.ndarray:
    """Sample covariance with divisor T (the Ledoit-Wolf convention); x is T x p."""
    y = x - x.mean(axis=0)
    return y.T @ y / x.shape[0]


def lw_identity(x: np.ndarray) -> tuple[np.ndarray, float]:
    """Ledoit-Wolf (2004, JMVA) shrinkage toward m*I with m = tr(S)/p and analytic intensity."""
    t, p = x.shape
    y = x - x.mean(axis=0)
    s = y.T @ y / t
    m = np.trace(s) / p
    target = m * np.eye(p)
    d2 = np.sum((s - target) ** 2)
    # b_bar^2 = (1/T^2) sum_t ||y_t y_t' - S||_F^2, using ||yy' - S||^2 = (y'y)^2 - 2 y'Sy + ||S||^2
    yy = np.sum(y**2, axis=1)
    ysy = np.einsum("ti,ij,tj->t", y, s, y)
    b_bar2 = np.sum(yy**2 - 2.0 * ysy + np.sum(s**2)) / t**2
    b2 = min(b_bar2, d2)
    delta = b2 / d2
    return delta * target + (1.0 - delta) * s, float(delta)


def lw_constant_correlation(x: np.ndarray) -> tuple[np.ndarray, float]:
    """Ledoit-Wolf (2004, JPM) shrinkage toward the constant-correlation matrix.

    delta = max(0, min(kappa / T, 1)), kappa = (pi - rho) / gamma.
    """
    t, p = x.shape
    y = x - x.mean(axis=0)
    s = y.T @ y / t
    var = np.diag(s)
    sd = np.sqrt(var)
    corr = s / np.outer(sd, sd)
    r_bar = (corr.sum() - p) / (p * (p - 1))
    f = r_bar * np.outer(sd, sd)
    np.fill_diagonal(f, var)
    # pi_ij = asymptotic variance of sqrt(T) s_ij
    pi_mat = (y**2).T @ (y**2) / t - s**2
    pi_hat = pi_mat.sum()
    # theta_ii_ij = asymptotic covariance of sqrt(T) s_ii and sqrt(T) s_ij
    theta = (y**3).T @ y / t - var[:, None] * s
    np.fill_diagonal(theta, 0.0)
    rho_off = r_bar / 2.0 * (np.sqrt(var[None, :] / var[:, None]) * theta + np.sqrt(var[:, None] / var[None, :]) * theta.T)
    rho_hat = np.trace(pi_mat) + rho_off.sum()
    gamma_hat = np.sum((f - s) ** 2)
    kappa = (pi_hat - rho_hat) / gamma_hat
    delta = max(0.0, min(kappa / t, 1.0))
    return delta * f + (1.0 - delta) * s, float(delta)


def ewma_cov(x: np.ndarray, lam: float) -> np.ndarray:
    """EWMA covariance (zero-mean, RiskMetrics style), weights normalised to sum to one."""
    t = x.shape[0]
    w = lam ** np.arange(t - 1, -1, -1)
    w /= w.sum()
    return (x * w[:, None]).T @ x


def mp_edges(q: float, sigma2: float = 1.0) -> tuple[float, float]:
    return sigma2 * (1.0 - math.sqrt(q)) ** 2, sigma2 * (1.0 + math.sqrt(q)) ** 2


def rmt_clip(x: np.ndarray) -> tuple[np.ndarray, int]:
    """Eigenvalue clipping of the sample correlation matrix (Laloux et al. 1999 style).

    Eigenvalues below the Marchenko-Pastur upper edge are replaced by their average, which
    preserves the trace; the cleaned correlation is rescaled to a unit diagonal.
    """
    t, p = x.shape
    s = sample_cov(x)
    sd = np.sqrt(np.diag(s))
    c = s / np.outer(sd, sd)
    vals, vecs = np.linalg.eigh(c)
    lam_plus = mp_edges(p / t)[1]
    noise = vals < lam_plus
    k = int((~noise).sum())
    vals = vals.copy()
    vals[noise] = vals[noise].mean()
    c_clean = (vecs * vals) @ vecs.T
    d = np.sqrt(np.diag(c_clean))
    c_clean = c_clean / np.outer(d, d)
    return c_clean * np.outer(sd, sd), k


def pca_factor_cov(x: np.ndarray, k: int) -> np.ndarray:
    """Statistical factor model: top-k principal components of S plus a diagonal residual."""
    s = sample_cov(x)
    vals, vecs = np.linalg.eigh(s)
    top = vecs[:, -k:] * np.sqrt(vals[-k:])
    common = top @ top.T
    resid = np.clip(np.diag(s - common), 1e-12, None)
    return common + np.diag(resid)


def gmv(s: np.ndarray) -> np.ndarray:
    w = np.linalg.solve(s, np.ones(s.shape[0]))
    return w / w.sum()


# ----------------------------------------------------------------------------
# Simulated factor market (daily returns in percent)
# ----------------------------------------------------------------------------


def factor_market(p: int, rng: np.random.Generator) -> np.ndarray:
    """True covariance: one market factor, four sector factors, heterogeneous specific risk."""
    n_sectors = 4
    beta = rng.uniform(0.5, 1.5, p)
    sector = np.arange(p) % n_sectors
    b = np.zeros((p, 1 + n_sectors))
    b[:, 0] = beta
    b[np.arange(p), 1 + sector] = 1.0
    f_var = np.array([1.0] + [0.6**2] * n_sectors)
    spec = rng.uniform(1.0, 2.0, p) ** 2
    return b @ np.diag(f_var) @ b.T + np.diag(spec)


def oos_study(p: int, t: int, reps: int, seed: int) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    sigma = factor_market(p, rng)
    chol = np.linalg.cholesky(sigma)
    w_star = gmv(sigma)
    v_star = w_star @ sigma @ w_star
    lam_60 = 0.5 ** (1.0 / 60.0)
    names = ["sample", "lw_identity", "lw_constcorr", "pca5", "rmt_clip", "ewma_hl60", "equal"]
    acc = {n: 0.0 for n in names}
    acc["delta_identity"] = 0.0
    acc["delta_constcorr"] = 0.0
    acc["rmt_k"] = 0.0
    acc["sample_insample"] = 0.0
    for _ in range(reps):
        x = rng.standard_normal((t, p)) @ chol.T
        s = sample_cov(x)
        s_i, d_i = lw_identity(x)
        s_c, d_c = lw_constant_correlation(x)
        s_r, k = rmt_clip(x)
        ests = {
            "sample": s,
            "lw_identity": s_i,
            "lw_constcorr": s_c,
            "pca5": pca_factor_cov(x, 5),
            "rmt_clip": s_r,
            "ewma_hl60": ewma_cov(x - x.mean(0), lam_60),
        }
        for n, est in ests.items():
            w = gmv(est)
            acc[n] += (w @ sigma @ w) / v_star
        w_s = gmv(s)
        acc["sample_insample"] += (w_s @ s @ w_s) / v_star
        ew = np.full(p, 1.0 / p)
        acc["equal"] += (ew @ sigma @ ew) / v_star
        acc["delta_identity"] += d_i
        acc["delta_constcorr"] += d_c
        acc["rmt_k"] += k
    return {n: v / reps for n, v in acc.items()}


def main() -> None:
    print("== 1. EWMA bookkeeping ==")
    lam_rm = 0.94
    check("half-life of lambda 0.94 (days)", math.log(0.5) / math.log(lam_rm), 11.2023, 1e-3)
    check("lambda for a 60-day half-life", 0.5 ** (1 / 60), 0.98851, 1e-5, ".5f")
    check("effective sample size (1+lam)/(1-lam), lambda 0.94", (1 + lam_rm) / (1 - lam_rm), 32.3333, 1e-3)
    lam60 = 0.5 ** (1 / 60)
    check("effective sample size, 60-day half-life", (1 + lam60) / (1 - lam60), 173.1, 0.1, ".1f")
    check("mean age lam/(1-lam), lambda 0.94 (days)", lam_rm / (1 - lam_rm), 15.6667, 1e-3)
    check("mean age, 60-day half-life (days)", lam60 / (1 - lam60), 86.06, 0.01, ".2f")
    # numerical check of the effective-size formula on a long weight vector
    w = (1 - lam_rm) * lam_rm ** np.arange(5000)
    check("effective sample size by summation, lambda 0.94", w.sum() ** 2 / np.sum(w**2), 32.3333, 1e-3)

    print("\n== 2. Parameter counts ==")
    for p, k, exp_full, exp_fac in [(100, 10, 5050, 1155), (3000, 60, 4_501_500, 184_830)]:
        check(f"p={p}: full covariance parameters p(p+1)/2", p * (p + 1) // 2, exp_full, 0, "d")
        check(f"p={p}, k={k}: factor-model parameters pk + k(k+1)/2 + p", p * k + k * (k + 1) // 2 + p, exp_fac, 0, "d")
    check("q = 3000 stocks / 504 days", 3000 / 504, 5.95, 0.005, ".2f")
    check("q for a 60-factor covariance on 504 days", 60 / 504, 0.119, 0.0005, ".3f")
    check("distinct correlations among 100 assets", 100 * 99 // 2, 4950, 0, "d")
    check("maximum rank of a demeaned sample covariance from 504 days", 504 - 1, 503, 0, "d")

    print("\n== 3. Marchenko-Pastur ==")
    p, t = 100, 250
    lo, hi = mp_edges(p / t)
    check("MP lower edge, q = 0.4", lo, 0.1351, 1e-4)
    check("MP upper edge, q = 0.4", hi, 2.6649, 1e-4)
    rng = np.random.default_rng(11)
    x = rng.standard_normal((t, p))
    ev = np.linalg.eigvalsh(sample_cov(x))
    check("pure noise: smallest sample eigenvalue (true 1)", ev[0], 0.13, 0.01, ".2f")
    check("pure noise: largest sample eigenvalue (true 1)", ev[-1], 2.66, 0.01, ".2f")
    check("pure noise: condition number of S (true 1)", ev[-1] / ev[0], 20.3, 0.1, ".1f")
    # true covariance is I, so the true GMV variance is 1/p and the true variance of w is w'w
    oos, ins = [], []
    for _ in range(200):
        xs = rng.standard_normal((t, p))
        sx = sample_cov(xs)
        w = gmv(sx)
        oos.append((w @ w) * p)
        ins.append((w @ sx @ w) * p)
    check("pure noise: OOS variance of sample GMV / optimum (200 draws)", float(np.mean(oos)), 1.68, 0.01, ".2f")
    check("pure noise: in-sample variance of sample GMV / optimum (200 draws)", float(np.mean(ins)), 0.60, 0.01, ".2f")
    check("1/(1-q) for q = 0.4", 1 / (1 - p / t), 1.6667, 1e-4)
    check("1/(1-q)^2 for q = 0.4 (realised over predicted)", 1 / (1 - p / t) ** 2, 2.7778, 1e-4)
    check("simulated realised over predicted", float(np.mean(oos)) / float(np.mean(ins)), 2.8, 0.006, ".2f")

    print("\n== 4. Constant-correlation target, 3 assets ==")
    vol = np.array([0.20, 0.30, 0.25])
    corr = np.array([[1.0, 0.5, 0.3], [0.5, 1.0, 0.4], [0.3, 0.4, 1.0]])
    s3 = corr * np.outer(vol, vol)
    r_bar = (corr.sum() - 3) / 6
    f3 = r_bar * np.outer(vol, vol)
    np.fill_diagonal(f3, vol**2)
    check("average correlation r_bar", r_bar, 0.4, 1e-12)
    check("target F_12 = 0.4*0.20*0.30", f3[0, 1], 0.024, 1e-12)
    check("sample S_12", s3[0, 1], 0.030, 1e-12)
    shr = 0.3 * f3 + 0.7 * s3
    check("shrunk entry (delta 0.3), cov 1-2", shr[0, 1], 0.0282, 1e-12)
    check("shrunk correlation 1-2", shr[0, 1] / (vol[0] * vol[1]), 0.47, 1e-12, ".2f")
    check("shrunk correlation 1-3", shr[0, 2] / (vol[0] * vol[2]), 0.33, 1e-12, ".2f")

    print("\n== 5a. Ledoit-Wolf formulas: vectorised versus explicit loops ==")
    rng = np.random.default_rng(3)
    n_t, n_p = 200, 8
    xs = rng.standard_normal((n_t, n_p)) @ np.linalg.cholesky(factor_market(n_p, rng)).T
    ys = xs - xs.mean(0)
    ss = ys.T @ ys / n_t
    b_loop = sum(np.sum((np.outer(y, y) - ss) ** 2) for y in ys) / n_t**2
    m = np.trace(ss) / n_p
    d2 = np.sum((ss - m * np.eye(n_p)) ** 2)
    _, d_vec = lw_identity(xs)
    check("identity-target intensity on the toy sample", d_vec, 0.051, 0.001, ".3f")
    check("identity-target intensity, vectorised minus loop", d_vec - min(b_loop, d2) / d2, 0.0, 1e-12, ".1e")
    sd = np.sqrt(np.diag(ss))
    rb = ((ss / np.outer(sd, sd)).sum() - n_p) / (n_p * (n_p - 1))
    pi_l = rho_l = 0.0
    for i in range(n_p):
        for j in range(n_p):
            pij = np.mean((ys[:, i] * ys[:, j] - ss[i, j]) ** 2)
            pi_l += pij
            if i == j:
                rho_l += pij
            else:
                th_ii = np.mean((ys[:, i] ** 2 - ss[i, i]) * (ys[:, i] * ys[:, j] - ss[i, j]))
                th_jj = np.mean((ys[:, j] ** 2 - ss[j, j]) * (ys[:, i] * ys[:, j] - ss[i, j]))
                rho_l += rb / 2 * (np.sqrt(ss[j, j] / ss[i, i]) * th_ii + np.sqrt(ss[i, i] / ss[j, j]) * th_jj)
    f = rb * np.outer(sd, sd)
    np.fill_diagonal(f, np.diag(ss))
    d_loop = max(0.0, min((pi_l - rho_l) / np.sum((f - ss) ** 2) / n_t, 1.0))
    _, d_cc = lw_constant_correlation(xs)
    check("constant-correlation intensity on the toy sample", d_cc, 0.439, 0.001, ".3f")
    check("constant-correlation intensity, vectorised minus loop", d_cc - d_loop, 0.0, 1e-12, ".1e")

    print("\n== 5 and 6. Out-of-sample GMV variance, p = 100, factor market ==")
    for t_obs, expect in [
        (
            150,
            {
                "sample": 2.98,
                "lw_identity": 1.69,
                "lw_constcorr": 1.41,
                "pca5": 1.14,
                "rmt_clip": 1.18,
                "ewma_hl60": 3.17,
                "equal": 3.56,
                "sample_insample": 0.34,
                "delta_identity": 0.08,
                "delta_constcorr": 0.44,
                "rmt_k": 3.25,
            },
        ),
        (
            500,
            {
                "sample": 1.25,
                "lw_identity": 1.22,
                "lw_constcorr": 1.18,
                "pca5": 1.05,
                "rmt_clip": 1.08,
                "ewma_hl60": 1.69,
                "equal": 3.56,
                "sample_insample": 0.80,
                "delta_identity": 0.02,
                "delta_constcorr": 0.18,
                "rmt_k": 4.00,
            },
        ),
    ]:
        res = oos_study(100, t_obs, reps=200, seed=7)
        print(f"-- T = {t_obs}, q = {100 / t_obs:.3f}, 1/(1-q) = {1 / (1 - 100 / t_obs):.3f}")
        assert abs(1 / (1 - 100 / t_obs) - {150: 3.0, 500: 1.25}[t_obs]) < 1e-12
        for key, val in expect.items():
            tol = 0.006
            check(f"T={t_obs} {key}", res[key], val, tol, ".2f")


if __name__ == "__main__":
    main()
