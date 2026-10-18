"""Risk factor modelling: return conventions, EWMA, PCA of a curve, shrinkage, noise eigenvalues, PSD repair, proxies.

Backs every number in 11-Risk-and-Trading/10-Risk-Factor-Modelling.md.

All covariances, curves and positions are labelled teaching inputs or simulations with fixed seeds, not market data.
The Ledoit-Wolf estimator follows Ledoit and Wolf (2004), J. Multivariate Analysis 88(2), eq. (14) with the
norm ||A||^2 = tr(A A') / p; the nearest-correlation algorithm is Higham (2002), alternating projections with
Dykstra's correction.

Run: python 11-Risk-and-Trading/code/risk_factors.py
"""

from __future__ import annotations

import math

import numpy as np


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a value and assert it matches the literal quoted in the note to within tol (absolute)."""
    print(f"  {label}: {value:.6f}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, note quotes {expected} (tol {tol})"
    return value


# ---------------------------------------------------------------------------
# Return conventions and EWMA
# ---------------------------------------------------------------------------


def section_conventions() -> None:
    print("\n[Core concepts: return conventions]")
    y0, y1 = 0.0050, 0.0005
    check("relative change of a yield from 50bp to 5bp", y1 / y0 - 1.0, -0.90, 1e-12)
    check("absolute change (bp)", (y1 - y0) * 1e4, -45.0, 1e-9)
    # The same relative 'volatility' applied to two yield levels produces very different bp moves.
    for level in (0.05, 0.005):
        print(f"  a 10% relative shock at {level:.1%} is {0.10 * level * 1e4:.1f}bp")
    check("10% relative shock at 5% (bp)", 0.10 * 0.05 * 1e4, 50.0, 1e-9)
    check("10% relative shock at 0.5% (bp)", 0.10 * 0.005 * 1e4, 5.0, 1e-9)


def ewma_update(cov: np.ndarray, r: np.ndarray, lam: float) -> np.ndarray:
    return lam * cov + (1.0 - lam) * np.outer(r, r)


def section_ewma() -> None:
    print("\n[Worked example 1: EWMA update and Cholesky]")
    prev = np.array([[0.000100, -0.000020], [-0.000020, 0.000025]])
    r = np.array([-0.020, -0.0006])
    cov = ewma_update(prev, r, 0.94)
    chol = np.linalg.cholesky(cov)
    print(f"  Sigma_t = {cov.tolist()}")
    print(f"  L = {chol.tolist()}")
    check("Sigma_t[0,0]", cov[0, 0], 0.000118, 1e-15)
    check("Sigma_t[0,1]", cov[0, 1], -0.00001808, 1e-15)
    check("Sigma_t[1,1]", cov[1, 1], 0.0000235216, 1e-15)
    check("L00", chol[0, 0], 0.0108628, 5e-8)
    check("L10", chol[1, 0], -0.0016644, 5e-8)
    check("L11", chol[1, 1], 0.0045554, 5e-8)
    check("updated correlation", cov[0, 1] / math.sqrt(cov[0, 0] * cov[1, 1]), -0.3432, 5e-5)
    check("previous correlation", -0.000020 / math.sqrt(0.000100 * 0.000025), -0.40, 1e-12)
    lam = 0.94
    check("EWMA half-life in days, ln 0.5 / ln 0.94", math.log(0.5) / math.log(lam), 11.20, 5e-3)
    check("effective number of observations (1 + lambda) / (1 - lambda)", (1.0 + lam) / (1.0 - lam), 32.33, 5e-3)
    check("weight left beyond 75 days, 0.94^75", lam**75, 0.0097, 5e-5)


# ---------------------------------------------------------------------------
# PCA of a model yield curve covariance
# ---------------------------------------------------------------------------

TENORS = np.array([0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0])
CURVE_VOL_BP = np.array([5.0, 5.5, 6.0, 6.5, 6.8, 7.0, 6.9, 6.7, 6.2, 5.9])  # daily bp vols, hypothetical


def curve_cov(rho_inf: float = 0.5, kappa: float = 0.05) -> np.ndarray:
    """Hypothetical daily covariance: rho(Ti, Tj) = rho_inf + (1 - rho_inf) exp(-kappa |Ti - Tj|)."""
    gap = np.abs(TENORS[:, None] - TENORS[None, :])
    corr = rho_inf + (1.0 - rho_inf) * np.exp(-kappa * gap)
    return corr * np.outer(CURVE_VOL_BP, CURVE_VOL_BP)


def sign_changes(v: np.ndarray) -> int:
    s = np.sign(v[np.abs(v) > 1e-12])
    return int(np.sum(s[1:] != s[:-1]))


def section_pca() -> None:
    print("\n[Core concepts and worked example 2: PCA of a model curve]")
    cov = curve_cov()
    vals, vecs = np.linalg.eigh(cov)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    vecs = vecs * np.sign(vecs[-1, :])  # sign convention: positive loading at 30y
    share = vals / vals.sum()
    print(f"  variance shares of PC1..PC4: {np.round(share[:4], 4)}")
    for j in range(3):
        print(f"  PC{j + 1} loadings {np.round(vecs[:, j], 3)} (sign changes {sign_changes(vecs[:, j])})")
    check("PC1 share", share[0], 0.8546, 5e-5)
    check("PC2 share", share[1], 0.0716, 5e-5)
    check("PC3 share", share[2], 0.0327, 5e-5)
    check("first three together", share[:3].sum(), 0.9590, 5e-5)
    assert [sign_changes(vecs[:, j]) for j in range(3)] == [0, 1, 2], "level, slope, curvature shapes"
    i2, i10 = 3, 7
    shock = 2.0 * math.sqrt(vals[1]) * vecs[:, 1]
    print(f"  +2 sd PC2 shock (bp): {np.round(shock, 2)}")
    check("2y move under a +2 sd PC2 shock (bp)", shock[i2], -2.45, 5e-3)
    check("10y move (bp)", shock[i10], 1.94, 5e-3)
    check("2s10s change (bp)", shock[i10] - shock[i2], 4.40, 5e-3)
    check("PC2 shock is orthogonal to PC1", float(shock @ vecs[:, 0]), 0.0, 1e-12)
    check("PC2 loading at 3 months", vecs[0, 1], -0.19, 5e-3)
    check("PC2 loading at 30 years", vecs[-1, 1], 0.64, 5e-3)
    # A rounded eigenvector is no longer orthogonal: the level leak of the draft's example.
    v1 = np.array([0.55, 0.60, 0.58])
    v2 = np.array([-0.70, -0.10, 0.70])
    check("dot product of the rounded vectors", float(v1 @ v2), -0.039, 1e-12)


# ---------------------------------------------------------------------------
# Covariance estimation: Ledoit-Wolf, Marchenko-Pastur, PSD repair
# ---------------------------------------------------------------------------


def ledoit_wolf(x: np.ndarray) -> tuple[np.ndarray, float]:
    """Ledoit-Wolf (2004) shrinkage to m I; returns (estimator, intensity b^2/d^2). Rows of x are observations."""
    n, p = x.shape
    xc = x - x.mean(axis=0)
    s = xc.T @ xc / n
    m = np.trace(s) / p
    d2 = np.sum((s - m * np.eye(p)) ** 2) / p
    b_bar2 = sum(np.sum((np.outer(row, row) - s) ** 2) / p for row in xc) / n**2
    b2 = min(b_bar2, d2)
    return (b2 / d2) * m * np.eye(p) + (1.0 - b2 / d2) * s, b2 / d2


def one_factor_cov(p: int, rng: np.random.Generator) -> np.ndarray:
    """Annualised one-factor covariance: market vol 20%, betas U(0.5, 1.5), idiosyncratic vols U(20%, 40%)."""
    beta = rng.uniform(0.5, 1.5, p)
    idio = rng.uniform(0.20, 0.40, p)
    return 0.20**2 * np.outer(beta, beta) + np.diag(idio**2)


def section_shrinkage() -> None:
    print("\n[Core concepts: sample covariance against Ledoit-Wolf, p = 50 assets, n = 60 days, 200 trials]")
    rng = np.random.default_rng(7)
    p, n = 50, 60
    true = one_factor_cov(p, rng)
    chol = np.linalg.cholesky(true)
    w_opt = np.linalg.solve(true, np.ones(p))
    var_opt = 1.0 / float(np.ones(p) @ w_opt)
    loss_s, loss_lw, mv_s, mv_lw, cond_s, cond_lw, inten = [], [], [], [], [], [], []
    for _ in range(200):
        x = rng.standard_normal((n, p)) @ chol.T
        xc = x - x.mean(axis=0)
        s = xc.T @ xc / n
        lw, delta = ledoit_wolf(x)
        loss_s.append(np.linalg.norm(s - true))
        loss_lw.append(np.linalg.norm(lw - true))
        for est, out in ((s, mv_s), (lw, mv_lw)):
            w = np.linalg.solve(est, np.ones(p))
            w /= w.sum()
            out.append(float(w @ true @ w) / var_opt)
        cond_s.append(np.linalg.cond(s))
        cond_lw.append(np.linalg.cond(lw))
        inten.append(delta)
    print(f"  Frobenius error: sample {np.mean(loss_s):.4f}, Ledoit-Wolf {np.mean(loss_lw):.4f}")
    print(f"  min-variance portfolio true variance / optimum: sample {np.mean(mv_s):.3f}, Ledoit-Wolf {np.mean(mv_lw):.3f}")
    print(f"  median condition number: sample {np.median(cond_s):.0f}, Ledoit-Wolf {np.median(cond_lw):.1f}")
    print(f"  mean shrinkage intensity {np.mean(inten):.3f}")
    check("mean Frobenius error, sample", float(np.mean(loss_s)), 0.891, 5e-4)
    check("mean Frobenius error, Ledoit-Wolf", float(np.mean(loss_lw)), 0.854, 5e-4)
    check("MV variance ratio, sample", float(np.mean(mv_s)), 6.77, 5e-3)
    check("MV variance ratio, Ledoit-Wolf", float(np.mean(mv_lw)), 1.62, 5e-3)
    check("mean shrinkage intensity", float(np.mean(inten)), 0.160, 5e-4)
    check("median condition number, sample", float(np.median(cond_s)), 2975, 1.0)
    check("median condition number, Ledoit-Wolf", float(np.median(cond_lw)), 91.8, 0.05)
    check("MV variance ratio, sample / Ledoit-Wolf", float(np.mean(mv_s) / np.mean(mv_lw)), 4.19, 5e-3)
    assert np.mean(loss_lw) < np.mean(loss_s) and np.mean(mv_lw) < np.mean(mv_s)
    # Sanity: when the truth is a multiple of I, the estimator should shrink almost all the way.
    _, delta_iid = ledoit_wolf(np.random.default_rng(8).standard_normal((60, 50)))
    assert delta_iid > 0.8, f"Ledoit-Wolf intensity on iid data should be close to 1, got {delta_iid}"
    # p > n: the sample covariance is singular.
    x = rng.standard_normal((40, p))
    xc = x - x.mean(axis=0)
    rank = int(np.linalg.matrix_rank(xc.T @ xc / 40))
    check("rank of a 50 x 50 sample covariance from 40 observations", rank, 39, 0)
    print("\n[Core concepts: Marchenko-Pastur edges, N = 100, T = 400]")
    big_n, big_t = 100, 400
    q = big_n / big_t
    lam_plus, lam_minus = (1 + math.sqrt(q)) ** 2, (1 - math.sqrt(q)) ** 2
    noise = rng.standard_normal((big_t, big_n))
    ev = np.linalg.eigvalsh(np.corrcoef(noise, rowvar=False))
    check("MP upper edge (1 + sqrt q)^2", lam_plus, 2.25, 1e-12)
    check("MP lower edge (1 - sqrt q)^2", lam_minus, 0.25, 1e-12)
    print(f"  pure noise: largest eigenvalue {ev.max():.4f}, smallest {ev.min():.4f}")
    check("largest noise eigenvalue (seed 7 stream)", float(ev.max()), 2.149, 5e-4)
    market = 0.5 * rng.standard_normal((big_t, 1)) + math.sqrt(0.75) * rng.standard_normal((big_t, big_n))
    ev_m = np.linalg.eigvalsh(np.corrcoef(market, rowvar=False))
    print(f"  one-factor returns (pairwise correlation 0.25): top eigenvalue {ev_m.max():.2f}, next {np.sort(ev_m)[-2]:.3f}")
    check("population top eigenvalue 1 + (N - 1) rho", 1.0 + 99 * 0.25, 25.75, 1e-12)
    check("sample top eigenvalue", float(ev_m.max()), 24.55, 5e-3)
    assert np.sort(ev_m)[-2] < lam_plus * 0.8, "the rest of the spectrum sits inside the noise band"


def nearest_correlation(a: np.ndarray, tol: float = 1e-12, max_iter: int = 10_000) -> np.ndarray:
    """Higham (2002): alternating projections onto PSD and unit-diagonal sets, with Dykstra's correction."""
    y = a.copy()
    ds = np.zeros_like(a)
    for _ in range(max_iter):
        r = y - ds
        vals, vecs = np.linalg.eigh(r)
        x = (vecs * np.maximum(vals, 0.0)) @ vecs.T
        ds = x - r
        y_new = x.copy()
        np.fill_diagonal(y_new, 1.0)
        if np.linalg.norm(y_new - y) < tol:
            return y_new
        y = y_new
    return y


def clip_and_rescale(a: np.ndarray, floor: float = 1e-8) -> np.ndarray:
    vals, vecs = np.linalg.eigh(a)
    c = (vecs * np.maximum(vals, floor)) @ vecs.T
    d = np.sqrt(np.diag(c))
    return c / np.outer(d, d)


def section_psd_repair() -> None:
    print("\n[Core concepts: repairing a correlation matrix that is not PSD]")
    a = np.array([[1.0, 0.9, 0.7], [0.9, 1.0, 0.3], [0.7, 0.3, 1.0]])
    check("determinant of the broken matrix", float(np.linalg.det(a)), -0.012, 1e-12)
    check("its smallest eigenvalue", float(np.linalg.eigvalsh(a).min()), -0.00735, 5e-6)
    hig = nearest_correlation(a)
    clip = clip_and_rescale(a)
    print(f"  Higham:  {np.round(hig, 4).tolist()}")
    print(f"  clipped: {np.round(clip, 4).tolist()}")
    d_h, d_c = float(np.linalg.norm(hig - a)), float(np.linalg.norm(clip - a))
    check("Frobenius distance, Higham", d_h, 0.00973, 5e-6)
    check("Frobenius distance, clip and rescale", d_c, 0.01002, 5e-6)
    assert d_h <= d_c and np.linalg.eigvalsh(hig).min() > -1e-10 and np.allclose(np.diag(hig), 1.0)


# ---------------------------------------------------------------------------
# Mapping and proxies
# ---------------------------------------------------------------------------


def section_proxies() -> None:
    print("\n[Core concepts and worked example 3: a beta proxy hides idiosyncratic risk]")
    long_stock, beta, idio_vol, mkt_vol = 10e6, 1.2, 0.25, 0.18
    hedge = -beta * long_stock
    z99 = 2.3263478740408408
    proxy_exposure = beta * long_stock + hedge
    true_sd = math.sqrt((beta * long_stock + hedge) ** 2 * mkt_vol**2 + long_stock**2 * idio_vol**2) / math.sqrt(252.0)
    check("market exposure after the beta hedge", proxy_exposure, 0.0, 1e-6)
    check("1-day 99% VaR, proxy model ($)", z99 * abs(proxy_exposure) * mkt_vol / math.sqrt(252.0), 0.0, 1e-6)
    check("1-day 99% VaR, with idiosyncratic risk ($)", z99 * true_sd, 366_365, 1.0)
    print("\n[Core concepts: PV01 mapping of a 7y cash flow onto the 5y and 10y vertices]")
    w5 = (10.0 - 7.0) / (10.0 - 5.0)
    check("weight on 5y", w5, 0.6, 1e-12)
    check("weight on 10y", 1.0 - w5, 0.4, 1e-12)
    print("\n[Core concepts: parameter count of a full covariance against a factor model, N = 3,000, K = 50]")
    n, k = 3000, 50
    check("full covariance N(N+1)/2", n * (n + 1) / 2, 4_501_500, 0)
    check("factor model NK + K(K+1)/2 + N", n * k + k * (k + 1) / 2 + n, 154_275, 0)


def section_async() -> None:
    print("\n[Core concepts: non-synchronous closes understate correlation]")
    rng = np.random.default_rng(11)
    t = 200_000
    f = rng.standard_normal(t)
    a = f + rng.standard_normal(t)
    b = np.empty(t)
    b[0] = 0.6 * f[0]
    b[1:] = 0.6 * f[1:] + 0.4 * f[:-1]
    b += rng.standard_normal(t)
    true_corr = 1.0 / math.sqrt(2.0 * (0.36 + 0.16 + 1.0))
    sync = float(np.corrcoef(a, b)[0, 1])
    two_day = float(np.corrcoef(a[0::2][: t // 2 - 1] + a[1::2][: t // 2 - 1], b[0::2][: t // 2 - 1] + b[1::2][: t // 2 - 1])[0, 1])
    lead_lag = float(np.mean((a[:-1] - a.mean()) * (b[1:] - b.mean())))
    adj = (np.cov(a, b)[0, 1] + lead_lag) / math.sqrt(np.var(a) * np.var(b))
    print(f"  daily corr {sync:.4f}, 2-day corr {two_day:.4f}, daily + lead-lag {adj:.4f}")
    check("daily correlation, population 0.6 / sqrt(2 x 1.52)", 0.6 / math.sqrt(2.0 * 1.52), 0.3441, 5e-5)
    check("correlation if closes were synchronous", true_corr, 0.5735, 5e-5)
    check("daily correlation, simulated", sync, 0.3441, 5e-3)
    check("daily plus lead-lag covariance, simulated", float(adj), 0.5735, 5e-3)
    check("2-day correlation, population 1.6 / sqrt(4 x 3.52)", 1.6 / math.sqrt(4.0 * 3.52), 0.4264, 5e-5)
    check("non-overlapping 2-day correlation, simulated", two_day, 0.4264, 5e-3)


# ---------------------------------------------------------------------------
# Heavy tails: Student t quantiles against the normal
# ---------------------------------------------------------------------------


def t_quantile_std(p: float, nu: float) -> float:
    """Quantile of a Student t scaled to unit variance, by bisection on a Gauss-Legendre CDF."""
    c = math.gamma((nu + 1) / 2) / (math.sqrt(nu * math.pi) * math.gamma(nu / 2))
    nodes, weights = np.polynomial.legendre.leggauss(400)

    def cdf(x: float) -> float:
        z = 0.5 * x * (nodes + 1.0)
        return 0.5 + float(np.sum(0.5 * x * weights * c * (1.0 + z * z / nu) ** (-(nu + 1) / 2)))

    lo, hi = 0.0, 100.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if cdf(mid) < p else (lo, mid)
    return 0.5 * (lo + hi) * math.sqrt((nu - 2) / nu)


def section_tails() -> None:
    print("\n[Core concepts: unit-variance Student t(5) against the normal]")
    check("excess kurtosis of t(5), 6 / (nu - 4)", 6.0 / (5.0 - 4.0), 6.0, 1e-12)
    q99, q999 = t_quantile_std(0.99, 5.0), t_quantile_std(0.999, 5.0)
    check("99% quantile, unit-variance t(5)", q99, 2.606, 5e-4)
    check("99.9% quantile, unit-variance t(5)", q999, 4.565, 5e-4)
    check("99% normal quantile", 2.3263478740408408, 2.326, 5e-4)
    check("99.9% normal quantile", 3.090232306167813, 3.090, 5e-4)
    check("ratio at 99%", q99 / 2.3263478740408408, 1.12, 5e-3)
    check("ratio at 99.9%", q999 / 3.090232306167813, 1.48, 5e-3)


def main() -> None:
    section_conventions()
    section_ewma()
    section_pca()
    section_shrinkage()
    section_psd_repair()
    section_proxies()
    section_async()
    section_tails()
    print("\nAll risk factor checks passed.")


if __name__ == "__main__":
    main()
