"""Covariance matrices, PSD repair, PCA and random-matrix cleaning: every number quoted in notes 03, 04 and 05.

Run: uv run --no-project --with numpy python 03-Linear-Algebra-and-Optimization/code/covariance_pca.py

Simulations use fixed seeds; the notes quote their results as "about" the printed value.
"""

from __future__ import annotations

import math

import numpy as np


def check(label: str, value: float, expected: float, tol: float = 5e-4) -> float:
    """Print a labelled number and assert it matches the value quoted in the notes."""
    v = float(value) + 0.0
    print(f"{label} = {int(v) if v.is_integer() and abs(v) < 1e15 else format(v, '.10g')}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected}"
    return value


# ---------------------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------------------


def third_correlation_range(r12: float, r13: float) -> tuple[float, float]:
    """Feasible [lo, hi] for rho_23 so that the 3x3 correlation matrix is PSD."""
    half_width = math.sqrt((1 - r12**2) * (1 - r13**2))
    return r12 * r13 - half_width, r12 * r13 + half_width


def corr3(r12: float, r13: float, r23: float) -> np.ndarray:
    return np.array([[1.0, r12, r13], [r12, 1.0, r23], [r13, r23, 1.0]])


def cholesky_lower(a: np.ndarray) -> np.ndarray:
    """Textbook Cholesky-Banachiewicz; raises ValueError if a is not positive definite."""
    n = a.shape[0]
    low = np.zeros_like(a, dtype=float)
    for i in range(n):
        for j in range(i + 1):
            s = a[i, j] - low[i, :j] @ low[j, :j]
            if i == j:
                if s <= 0:
                    raise ValueError(f"matrix not positive definite: pivot {i} = {s:.3g}")
                low[i, i] = math.sqrt(s)
            else:
                low[i, j] = s / low[j, j]
    return low


def clip_eigenvalues(c: np.ndarray, floor: float = 0.0) -> np.ndarray:
    """Floor eigenvalues at `floor`, rebuild, then rescale back to unit diagonal."""
    lam, vec = np.linalg.eigh(c)
    fixed = (vec * np.maximum(lam, floor)) @ vec.T
    d = np.sqrt(np.diag(fixed))
    return fixed / np.outer(d, d)


def project_psd(a: np.ndarray) -> np.ndarray:
    lam, vec = np.linalg.eigh((a + a.T) / 2)
    return (vec * np.maximum(lam, 0.0)) @ vec.T


def higham_nearest_correlation(a: np.ndarray, tol: float = 1e-12, max_iter: int = 10_000) -> tuple[np.ndarray, int]:
    """Higham (2002) alternating projections with Dykstra's correction, unit weights.

    Alternates between the PSD cone S and the unit-diagonal affine set U. Dykstra's increment is
    needed only for the cone, because projection onto an affine set is linear.
    """
    y = a.copy()
    ds = np.zeros_like(a)
    for it in range(1, max_iter + 1):
        r = y - ds
        x = project_psd(r)
        ds = x - r
        y_new = x.copy()
        np.fill_diagonal(y_new, 1.0)
        if np.linalg.norm(y_new - y) <= tol * np.linalg.norm(y) and np.linalg.norm(y_new - x) <= 1e-9:
            return y_new, it
        y = y_new
    raise RuntimeError("Higham iteration did not converge")


# ---------------------------------------------------------------------------
# Note 04: covariance and PSD
# ---------------------------------------------------------------------------


def third_correlation_examples() -> None:
    print("\n[04] feasible range of rho_23 given rho_12 and rho_13")
    for r12, r13, lo_want, hi_want in ((0.9, 0.9, 0.62, 1.0), (0.8, 0.6, 0.0, 0.96), (0.5, 0.5, -0.5, 1.0), (0.6, -0.6, -1.0, 0.28)):
        lo, hi = third_correlation_range(r12, r13)
        check(f"rho12={r12}, rho13={r13}: lower", lo, lo_want, 1e-12)
        check(f"rho12={r12}, rho13={r13}: upper", hi, hi_want, 1e-12)
        for edge in (lo, hi):
            assert abs(np.linalg.eigvalsh(corr3(r12, r13, edge))[0]) < 1e-12, "boundary is singular"
    check("angle check: cos(acos 0.9 + acos 0.9)", math.cos(2 * math.acos(0.9)), 0.62, 1e-12)
    check("acos 0.9 in degrees", math.degrees(math.acos(0.9)), 25.842, 1e-3)
    check("maximum angle 2 acos 0.9 in degrees", 2 * math.degrees(math.acos(0.9)), 51.684, 1e-3)
    r12 = r13 = 0.9
    check("rho12 rho13 for (0.9, 0.9)", r12 * r13, 0.81, 1e-12)
    check("sqrt((1 - 0.81)(1 - 0.81))", math.sqrt((1 - r12**2) * (1 - r13**2)), 0.19, 1e-12)


def cholesky_example() -> None:
    print("\n[04] Cholesky of a 3x3 correlation matrix")
    c = corr3(0.5, 0.3, 0.2)
    low = cholesky_lower(c)
    check("L21", low[1, 0], 0.5, 1e-12)
    check("L22", low[1, 1], 0.866025, 1e-6)
    check("L31", low[2, 0], 0.3, 1e-12)
    check("L32", low[2, 1], 0.057735, 1e-6)
    check("L33", low[2, 2], 0.952190, 1e-6)
    check("max |L - numpy cholesky|", np.abs(low - np.linalg.cholesky(c)).max(), 0.0, 1e-12)
    rng = np.random.default_rng(42)
    z = rng.standard_normal((200_000, 3))
    x = z @ low.T
    sample = np.corrcoef(x, rowvar=False)
    check("simulated rho12 (seed 42, 200k)", sample[0, 1], 0.5027, 5e-5)
    check("simulated rho13", sample[0, 2], 0.3019, 5e-5)
    check("simulated rho23", sample[1, 2], 0.2015, 5e-5)
    check("max |simulated - true| correlation", np.abs(sample - c).max(), 0.0, 0.005)
    check("sampling scale 1/sqrt(200000)", 1 / math.sqrt(len(x)), 0.0022, 1e-4)


def equicorrelation_bound() -> None:
    print("\n[04] equicorrelation lower bound")
    for n, want in ((2, -1.0), (5, -0.25), (101, -0.01)):
        check(f"n = {n}: rho_min = -1/(n-1)", -1 / (n - 1), want, 1e-12)
    c = 1.25 * np.eye(5) - 0.25 * np.ones((5, 5))
    check("min eigenvalue at rho = -0.25, n = 5", np.linalg.eigvalsh(c)[0], 0.0, 1e-12)
    c = 1.3 * np.eye(5) - 0.3 * np.ones((5, 5))
    check("min eigenvalue at rho = -0.3, n = 5", np.linalg.eigvalsh(c)[0], -0.2, 1e-12)


def non_psd_repair() -> None:
    print("\n[04] repair of an infeasible matrix: rho12 = rho13 = 0.9, rho23 = 0")
    bad = corr3(0.9, 0.9, 0.0)
    lam = np.linalg.eigvalsh(bad)
    check("eigenvalue min = 1 - 0.9 sqrt 2", lam[0], 1 - 0.9 * math.sqrt(2), 1e-12)
    check("eigenvalue min", lam[0], -0.272792, 1e-6)
    check("eigenvalue mid", lam[1], 1.0, 1e-12)
    check("eigenvalue max", lam[2], 2.272792, 1e-6)
    try:
        cholesky_lower(bad)
    except ValueError as exc:
        print(f"cholesky fails as expected: {exc}")
        l21, l31 = bad[1, 0] / math.sqrt(bad[0, 0]), bad[2, 0] / math.sqrt(bad[0, 0])
        l22 = math.sqrt(bad[1, 1] - l21**2)
        l32 = (bad[2, 1] - l31 * l21) / l22
        check("L22 = sqrt(1 - 0.81)", l22, 0.43589, 1e-5)
        check("L32 = (0 - 0.81) / L22", l32, -1.85826, 1e-5)
        check("third pivot 1 - 0.81 - L32^2", bad[2, 2] - l31**2 - l32**2, -3.2632, 1e-4)
    else:
        raise AssertionError("Cholesky should fail on a non-PSD matrix")

    clipped = clip_eigenvalues(bad, 0.0)
    check("clipped rho12", clipped[0, 1], 0.729330, 1e-6)
    check("clipped rho23", clipped[1, 2], 0.063844, 1e-6)
    check("clipped distance (Frobenius)", np.linalg.norm(clipped - bad), 0.353080, 1e-6)
    near, iters = higham_nearest_correlation(bad)
    check("Higham rho12", near[0, 1], 0.743410, 1e-6)
    check("Higham rho23", near[1, 2], 0.105318, 1e-6)
    check("Higham distance (Frobenius)", np.linalg.norm(near - bad), 0.346792, 1e-6)
    check("Higham min eigenvalue", np.linalg.eigvalsh(near)[0], 0.0, 1e-9)
    check("Higham iterations (tol 1e-12)", iters, 30, 0)
    lo, _ = third_correlation_range(near[0, 1], near[0, 2])
    check("Higham result sits on the PSD boundary (rho23 - lower bound)", near[1, 2] - lo, 0.0, 1e-8)


def scenario_scaling_breaks_psd() -> None:
    print("\n[04] entrywise scenario scaling can break PSD")
    base = corr3(0.8, 0.8, 0.3)
    check("base min eigenvalue", np.linalg.eigvalsh(base)[0], 0.0087, 1e-4)
    off = ~np.eye(3, dtype=bool)
    high = base.copy()
    high[off] = np.minimum(1.25 * base[off], 1.0)
    check("high scenario rho12", high[0, 1], 1.0, 1e-12)
    check("high scenario rho23", high[1, 2], 0.375, 1e-12)
    check("high scenario min eigenvalue", np.linalg.eigvalsh(high)[0], -0.2391, 1e-4)
    low = base.copy()
    low[off] = np.maximum(2 * base[off] - 1, 0.75 * base[off])
    check("low scenario rho12", low[0, 1], 0.6, 1e-12)
    check("low scenario rho23", low[1, 2], 0.225, 1e-12)
    check("low scenario min eigenvalue", np.linalg.eigvalsh(low)[0], 0.2565, 1e-4)
    check("Schur: base o base min eigenvalue", np.linalg.eigvalsh(base * base)[0], 0.1388, 1e-4)


# Basel Framework MAR21.57, Table 5: CSR non-securitisation cross-sector correlations for sectors 1 to 8
# (buckets 1-8 investment grade, 9-15 the same sectors high yield and non-rated, 16 other sector,
# 17 IG indices, 18 HY indices).
CSR_SECTOR_GAMMA = {
    (1, 2): 0.75, (1, 3): 0.10, (1, 4): 0.20, (1, 5): 0.25, (1, 6): 0.20, (1, 7): 0.15, (1, 8): 0.10,
    (2, 3): 0.05, (2, 4): 0.15, (2, 5): 0.20, (2, 6): 0.15, (2, 7): 0.10, (2, 8): 0.10,
    (3, 4): 0.05, (3, 5): 0.15, (3, 6): 0.20, (3, 7): 0.05, (3, 8): 0.20,
    (4, 5): 0.20, (4, 6): 0.25, (4, 7): 0.05, (4, 8): 0.05,
    (5, 6): 0.25, (5, 7): 0.05, (5, 8): 0.15,
    (6, 7): 0.05, (6, 8): 0.20,
    (7, 8): 0.05,
}  # fmt: skip


def csr_inter_bucket_gamma(b: int, c: int) -> float:
    """MAR21.57: gamma_bc = gamma_rating x gamma_sector for CSR non-securitisation buckets 1 to 18."""
    if b == c:
        return 1.0
    rating = 0.5 if b <= 15 and c <= 15 and (b <= 8) != (c <= 8) else 1.0
    sb, sc = (b - 8 if 9 <= b <= 15 else b), (c - 8 if 9 <= c <= 15 else c)
    if sb == sc:
        sector = 1.0
    elif 16 in (sb, sc):
        sector = 0.0
    elif {sb, sc} == {17, 18}:
        sector = 0.75
    elif sb in (17, 18) or sc in (17, 18):
        sector = 0.45
    else:
        sector = CSR_SECTOR_GAMMA[(min(sb, sc), max(sb, sc))]
    return rating * sector


def frtb_csr_matrix_not_psd() -> None:
    print("\n[04] Basel FRTB CSR non-securitisation inter-bucket correlation matrix (MAR21.57)")
    buckets = range(1, 19)
    medium = np.array([[csr_inter_bucket_gamma(b, c) for c in buckets] for b in buckets])
    off = ~np.eye(18, dtype=bool)
    high, low = medium.copy(), medium.copy()
    high[off] = np.minimum(1.25 * medium[off], 1.0)  # MAR21.6(2)
    low[off] = np.maximum(2 * medium[off] - 1, 0.75 * medium[off])  # MAR21.6(3)
    check("CSR gamma, medium scenario: min eigenvalue", np.linalg.eigvalsh(medium)[0], -0.2203, 1e-4)
    check("CSR gamma, high scenario: min eigenvalue", np.linalg.eigvalsh(high)[0], -0.5254, 1e-4)
    check("CSR gamma, low scenario: min eigenvalue", np.linalg.eigvalsh(low)[0], 0.0848, 1e-4)


def sample_covariance_rank() -> None:
    print("\n[04] sample covariance with N > T")
    rng = np.random.default_rng(3)
    n_assets, n_obs = 50, 30
    x = rng.standard_normal((n_obs, n_assets))
    s = np.cov(x, rowvar=False)
    check("rank of sample covariance (N=50, T=30)", np.linalg.matrix_rank(s), 29, 0)
    lam = np.linalg.eigvalsh(s)
    check("number of (numerically) zero eigenvalues", int((lam < 1e-10).sum()), 21, 0)
    check("min eigenvalue > -1e-12 (PSD)", float(lam[0] > -1e-12), 1.0, 0)
    x = rng.standard_normal((250, 500))
    lam = np.linalg.eigvalsh(np.cov(x, rowvar=False))
    tol = lam[-1] * 500 * np.finfo(float).eps
    check("card: rank with N = 500, T = 250", int((lam > tol).sum()), 249, 0)
    check("card: zero eigenvalues with N = 500, T = 250", int((lam <= tol).sum()), 251, 0)


# ---------------------------------------------------------------------------
# Note 05: PCA of a yield curve, Marchenko-Pastur, cleaning
# ---------------------------------------------------------------------------

TENORS = np.array([0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0])
VOLS_BP = np.array([4.0, 4.5, 5.5, 6.5, 7.0, 7.0, 6.8, 6.5, 6.0, 5.8])  # daily bp vols, humped at 3y-5y
RHO_INF, BETA, ETA = 0.3, 0.07, 0.03


def yield_curve_covariance() -> np.ndarray:
    """corr = (1 - eta) K + eta I with K_ij = rho_inf + (1 - rho_inf) exp(-beta (ln t_i - ln t_j)^2).

    K is a constant (rank one, PSD) plus a Gaussian kernel (positive definite by Bochner); eta I adds
    tenor-specific noise. Every piece is PSD, so the result is a valid correlation matrix by construction.
    """
    log_t = np.log(TENORS)
    kernel = RHO_INF + (1 - RHO_INF) * np.exp(-BETA * (log_t[:, None] - log_t[None, :]) ** 2)
    corr = (1 - ETA) * kernel + ETA * np.eye(len(TENORS))
    return corr * np.outer(VOLS_BP, VOLS_BP)


def sign_changes(v: np.ndarray) -> int:
    s = np.sign(v[np.abs(v) > 1e-12])
    return int((s[1:] != s[:-1]).sum())


def yield_curve_pca() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    print("\n[05] PCA of the synthetic yield-curve covariance (bp/day)")
    cov = yield_curve_covariance()
    corr = cov / np.outer(VOLS_BP, VOLS_BP)
    check("corr(2y, 10y)", corr[3, 7], 0.8574, 1e-4)
    check("corr(3m, 30y)", corr[0, 9], 0.4275, 1e-4)
    check("min eigenvalue of correlation > 0", float(np.linalg.eigvalsh(corr)[0] > 0), 1.0, 0)
    lam, vec = np.linalg.eigh(cov)
    lam, vec = lam[::-1], vec[:, ::-1]
    vec = vec * np.sign(vec[-1])  # sign convention: positive 30y loading
    share = lam / lam.sum()
    check("total variance (bp^2/day)", lam.sum(), (VOLS_BP**2).sum(), 1e-9)
    check("total variance (quoted)", lam.sum(), 364.88, 5e-3)
    check("PC1 share", share[0], 0.8634, 1e-4)
    check("PC2 share", share[1], 0.0953, 1e-4)
    check("PC3 share", share[2], 0.0185, 1e-4)
    check("first three PCs share", share[:3].sum(), 0.9772, 1e-4)
    check("PC1 daily vol (bp)", math.sqrt(lam[0]), 17.749, 1e-3)
    for k, want in ((0, 0), (1, 1), (2, 2)):
        check(f"sign changes in PC{k + 1}", sign_changes(vec[:, k]), want, 0)
    want_loadings = (
        (0.162, 0.206, 0.277, 0.349, 0.384, 0.387, 0.374, 0.351, 0.305, 0.281),
        (-0.393, -0.406, -0.389, -0.269, -0.148, 0.040, 0.155, 0.257, 0.391, 0.437),
        (0.529, 0.332, 0.081, -0.204, -0.319, -0.301, -0.202, -0.050, 0.292, 0.491),
    )
    for k, row in enumerate(want_loadings):
        for i, want in enumerate(row):
            check(f"PC{k + 1} loading on tenor {TENORS[i]}", vec[i, k], want, 5e-4)
    check("PC1 loading 5y", vec[5, 0], 0.3872, 1e-4)
    check("PC2 loading 3m", vec[0, 1], -0.3926, 1e-4)
    check("PC2 loading 30y", vec[9, 1], 0.4366, 1e-4)
    return cov, vec, lam


def pca_butterfly(cov: np.ndarray, vec: np.ndarray, lam: np.ndarray) -> None:
    print("\n[05] PC1/PC2-neutral 2s5s10s butterfly (DV01 weights, belly = -1)")
    idx = [3, 5, 7]  # 2y, 5y, 10y
    load = vec[idx, :2]  # 3 x 2
    # x = (a, -1, c): a*load[0] - load[1] + c*load[2] = 0 for PC1 and PC2
    wings = np.linalg.solve(np.column_stack([load[0], load[2]]), load[1])
    x = np.zeros(len(TENORS))
    x[idx] = [wings[0], -1.0, wings[1]]
    fifty = np.zeros(len(TENORS))
    fifty[idx] = [0.5, -1.0, 0.5]
    check("2y wing weight", x[3], 0.4622, 1e-4)
    check("10y wing weight", x[7], 0.6427, 1e-4)
    check("PCA fly: PC1 exposure", x @ vec[:, 0], 0.0, 1e-12)
    check("PCA fly: PC2 exposure", x @ vec[:, 1], 0.0, 1e-12)
    check("50/50 fly: PC1 exposure", fifty @ vec[:, 0], -0.0369, 1e-4)
    check("50/50 fly: PC2 exposure", fifty @ vec[:, 1], -0.0468, 1e-4)
    for name, w, want_vol, want_share in (("PCA fly", x, 1.5535, 0.0), ("50/50 fly", fifty, 1.6591, 0.1835)):
        total = w @ cov @ w
        from_pc12 = sum((w @ vec[:, k]) ** 2 * lam[k] for k in range(2))
        check(f"{name} daily vol (bp x DV01)", math.sqrt(total), want_vol, 1e-4)
        check(f"{name} variance share from PC1 and PC2", from_pc12 / total, want_share, 1e-4)


def low_rank_yield_history(cov: np.ndarray) -> None:
    print("\n[03/05] low-rank approximation of 750 simulated days of yield changes")
    rng = np.random.default_rng(11)
    t_days = 750
    x = rng.standard_normal((t_days, len(TENORS))) @ np.linalg.cholesky(cov).T
    x = x - x.mean(axis=0)
    s = np.linalg.svd(x, compute_uv=False)
    energy = np.cumsum(s**2) / (s**2).sum()
    check("rank-1 energy share (seed 11)", energy[0], 0.8646, 2e-3)
    check("rank-2 energy share", energy[1], 0.9565, 2e-3)
    check("rank-3 energy share", energy[2], 0.9778, 2e-3)
    rms3 = math.sqrt((s[3:] ** 2).sum() / x.size)
    check("rank-3 reconstruction RMS error (bp)", rms3, 0.908, 0.01)


def marchenko_pastur_bounds(q: float, var: float = 1.0) -> tuple[float, float]:
    return var * (1 - math.sqrt(q)) ** 2, var * (1 + math.sqrt(q)) ** 2


def marchenko_pastur_noise() -> None:
    print("\n[05] Marchenko-Pastur for pure noise, N = 100, T = 500")
    n, t = 100, 500
    lo, hi = marchenko_pastur_bounds(n / t)
    check("lambda_minus", lo, 0.305573, 1e-6)
    check("lambda_plus", hi, 2.094427, 1e-6)
    check("sqrt(q) for q = 0.2", math.sqrt(n / t), 0.4472, 1e-4)
    lo1, hi1 = marchenko_pastur_bounds(1.0)
    check("q = 1: lambda_minus", lo1, 0.0, 0)
    check("q = 1: lambda_plus", hi1, 4.0, 0)
    rng = np.random.default_rng(5)
    x = rng.standard_normal((t, n))
    lam = np.linalg.eigvalsh(np.corrcoef(x, rowvar=False))
    check("sample min eigenvalue (seed 5)", lam[0], 0.326, 0.002)
    check("sample max eigenvalue (seed 5)", lam[-1], 2.012, 0.002)


def factor_correlation(rng: np.random.Generator, n: int = 100, n_sectors: int = 4) -> np.ndarray:
    """Market + sector factors with idiosyncratic noise, unit variances."""
    a = rng.uniform(0.35, 0.65, n)  # market loadings
    b = rng.uniform(0.25, 0.45, n)  # sector loadings
    sector = np.repeat(np.arange(n_sectors), n // n_sectors)
    load = np.zeros((n, 1 + n_sectors))
    load[:, 0] = a
    load[np.arange(n), 1 + sector] = b
    c = load @ load.T
    np.fill_diagonal(c, 1.0)
    return c


def gmv(cov: np.ndarray) -> np.ndarray:
    w = np.linalg.solve(cov, np.ones(len(cov)))
    return w / w.sum()


def rmt_cleaning() -> None:
    print("\n[05] random-matrix cleaning: market + 4 sectors, N = 100, T = 250")
    rng = np.random.default_rng(2024)
    true = factor_correlation(rng)
    true_lam = np.linalg.eigvalsh(true)[::-1]
    check("true top eigenvalue", true_lam[0], 27.06, 0.01)
    for i, want in enumerate((27.06, 3.94, 3.72, 3.50, 0.81, 0.79)):
        check(f"true eigenvalue {i + 1}", true_lam[i], want, 5e-3)
    n, t = true.shape[0], 250
    x = rng.standard_normal((t, n)) @ np.linalg.cholesky(true).T
    sample = np.corrcoef(x, rowvar=False)
    lam, vec = np.linalg.eigh(sample)
    lam, vec = lam[::-1], vec[:, ::-1]
    q = n / t
    lam_plus = (1 - lam[0] / n) * (1 + math.sqrt(q)) ** 2
    n_signal = int((lam > lam_plus).sum())
    check("MP edge with market removed (1 - lambda_1/N)(1 + sqrt q)^2", lam_plus, 1.862, 0.002)
    check("eigenvalues above the edge", n_signal, 4, 0)
    for i, want in enumerate((30.15, 4.60, 3.77, 3.17, 1.58, 1.52)):
        check(f"sample eigenvalue {i + 1} (seed 2024)", lam[i], want, 5e-3)
    check("q = N/T", q, 0.4, 1e-12)
    check("plain MP edge (1 + sqrt q)^2", (1 + math.sqrt(q)) ** 2, 2.6649, 1e-4)
    check("eigenvalues above the plain edge (same count here)", int((lam > (1 + math.sqrt(q)) ** 2).sum()), 4, 0)
    check("true eigenvalues above the bulk (market mode and three sector contrasts)", int((true_lam > 1.0).sum()), 4, 0)
    cleaned_lam = lam.copy()
    cleaned_lam[n_signal:] = lam[n_signal:].mean()  # trace preserving
    cleaned = (vec * cleaned_lam) @ vec.T
    d = np.sqrt(np.diag(cleaned))
    cleaned = cleaned / np.outer(d, d)

    def true_var(w: np.ndarray) -> float:
        return float(w @ true @ w)

    best = true_var(gmv(true))
    ratio_sample = true_var(gmv(sample)) / best
    ratio_clean = true_var(gmv(cleaned)) / best
    check("GMV true variance ratio, sample correlation", ratio_sample, 2.069, 0.002)
    check("GMV true variance ratio, cleaned correlation", ratio_clean, 1.214, 0.002)
    assert ratio_clean < ratio_sample
    pc1 = vec[:, 0] * np.sign(vec[:, 0].sum())
    check("PC1 eigenportfolio: share of positive weights", float((pc1 > 0).mean()), 1.0, 0)
    check("PC1 eigenportfolio: smallest unit-norm weight", pc1.min(), 0.055, 5e-4)
    check("PC1 eigenportfolio: largest unit-norm weight", pc1.max(), 0.130, 5e-4)


def main() -> None:
    third_correlation_examples()
    cholesky_example()
    equicorrelation_bound()
    non_psd_repair()
    scenario_scaling_breaks_psd()
    frtb_csr_matrix_not_psd()
    sample_covariance_rank()
    cov, vec, lam = yield_curve_pca()
    pca_butterfly(cov, vec, lam)
    low_rank_yield_history(cov)
    marchenko_pastur_noise()
    rmt_cleaning()
    print("\nall covariance_pca checks passed")


if __name__ == "__main__":
    main()
