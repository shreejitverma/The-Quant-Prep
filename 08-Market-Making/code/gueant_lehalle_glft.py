"""Gueant-Lehalle-Fernandez-Tapia market making: exact finite-inventory quotes versus the closed forms.

Backs every number in ``04-Gueant-Lehalle-and-Extensions.md``.
Run ``uv run --no-project --with numpy python 08-Market-Making/code/gueant_lehalle_glft.py``;
each printed number is asserted, so drift in the note fails CI.

Model (Gueant, Lehalle and Fernandez-Tapia 2013): mid dS = mu dt + sigma dW, fill intensity A exp(-k delta)
on each side, CARA utility with risk aversion gamma, inventory kept in [-Q, Q], no terminal penalty.
With u = -exp(-gamma (x + q s)) v_q(t)^(-gamma / k) the HJB reduces to the linear system

    v_q'(t) = (alpha q^2 - k mu q) v_q(t) - eta (v_{q+1}(t) + v_{q-1}(t)),  v_q(T) = 1,
    alpha = k gamma sigma^2 / 2,  eta = A (1 + gamma / k)^(-(1 + k / gamma)),

(the v_{Q+1} and v_{-Q-1} terms are absent), so v(t) = exp(-M (T - t)) 1 with M tridiagonal and symmetric.
The quotes are delta_b = ln(v_q / v_{q+1}) / k + ln(1 + gamma / k) / gamma and
delta_a = ln(v_q / v_{q-1}) / k + ln(1 + gamma / k) / gamma.

The default parameters are those of the repo Avellaneda-Stoikov simulator (avellaneda_stoikov_mm.py):
sigma = 2, gamma = 0.1, k = 1.5, A = 140, horizon T = 1.
"""

from __future__ import annotations

import math

import numpy as np

SIGMA, GAMMA, K, A_RATE = 2.0, 0.1, 1.5, 140.0


def check(name: str, value: float, expected: float, tol: float) -> float:
    """Print a named result and assert it is within ``tol`` of the value quoted in the note."""
    print(f"{name:<64s} {value:12.4f}")
    assert abs(value - expected) <= tol, f"{name}: got {value}, expected {expected} +/- {tol}"
    return value


def alpha_eta(sigma: float = SIGMA, gamma: float = GAMMA, k: float = K, a: float = A_RATE) -> tuple[float, float]:
    return k * gamma * sigma**2 / 2.0, a * (1.0 + gamma / k) ** (-(1.0 + k / gamma))


def base_half_spread(gamma: float = GAMMA, k: float = K) -> float:
    """The risk-adjusted market-power term ln(1 + gamma / k) / gamma that every quote contains."""
    return math.log1p(gamma / k) / gamma


def closed_form_c(sigma: float = SIGMA, gamma: float = GAMMA, k: float = K, a: float = A_RATE) -> float:
    """GLFT asymptotic inventory coefficient sqrt(sigma^2 gamma / (2 k A) (1 + gamma / k)^(1 + k / gamma))."""
    return math.sqrt(sigma**2 * gamma / (2.0 * k * a) * (1.0 + gamma / k) ** (1.0 + k / gamma))


def tridiagonal(diag: np.ndarray, off: float) -> np.ndarray:
    n = len(diag)
    return np.diag(diag) - off * (np.eye(n, k=1) + np.eye(n, k=-1))


def propagate(m: np.ndarray, start: np.ndarray, tau: float) -> np.ndarray:
    """exp(-m tau) start, normalised to max 1 (quotes depend only on ratios of v).

    m has non-positive off-diagonal entries, so with c = max diag(m) the matrix p = c I - m is non-negative and
    exp(-m tau) = exp(-c tau) exp(p tau).  The Taylor series of exp(p h) applied to a positive vector has only
    non-negative terms, so there is no cancellation: tiny entries of v (large |q|) keep full relative accuracy on
    every platform, which an eigendecomposition does not guarantee.  Steps of size h keep ||p h|| <= 1/2.
    """
    p = np.max(np.diag(m)) * np.eye(len(m)) - m
    assert np.all(p >= 0), "off-diagonal entries of m must be non-positive"
    steps = max(1, math.ceil(np.abs(p).sum(axis=1).max() * tau / 0.5))
    h = tau / steps
    v = np.asarray(start, dtype=float).copy()
    for _ in range(steps):
        term, acc = v.copy(), v.copy()
        for j in range(1, 80):
            term = (p @ term) * (h / j)
            acc += term
            if np.all(term <= 1e-17 * acc):
                break
        else:
            raise RuntimeError("Taylor series did not converge")
        v = acc / acc.max()
    assert np.all(v > 0), "v must stay positive"
    return v


def propagate_eig(m: np.ndarray, start: np.ndarray, tau: float) -> np.ndarray:
    """Independent check for symmetric m: eigendecomposition, accurate for entries well above round-off."""
    w, vecs = np.linalg.eigh(m)
    out = vecs @ (np.exp(-(w - w.min()) * tau) * (vecs.T @ start))
    return out / out.max()


def glft_quotes(
    q_max: int, tau: float, mu: float = 0.0, sigma: float = SIGMA, gamma: float = GAMMA, k: float = K, a: float = A_RATE
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Exact bid and ask distances for q in [-Q, Q] with time tau = T - t left (nan where not quoted)."""
    alpha, eta = alpha_eta(sigma, gamma, k, a)
    qs = np.arange(-q_max, q_max + 1)
    v = propagate(tridiagonal(alpha * qs**2 - k * mu * qs, eta), np.ones(len(qs)), tau)
    base = base_half_spread(gamma, k)
    bid = np.full(len(qs), np.nan)
    ask = np.full(len(qs), np.nan)
    bid[:-1] = np.log(v[:-1] / v[1:]) / k + base
    ask[1:] = np.log(v[1:] / v[:-1]) / k + base
    return qs, bid, ask


def glft_stationary(q_max: int, mu: float = 0.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """T - t -> infinity: v is proportional to the eigenvector of the smallest eigenvalue of M."""
    alpha, eta = alpha_eta()
    qs = np.arange(-q_max, q_max + 1)
    w, vecs = np.linalg.eigh(tridiagonal(alpha * qs**2 - K * mu * qs, eta))
    f = np.abs(vecs[:, 0])
    base = base_half_spread()
    bid = np.full(len(qs), np.nan)
    ask = np.full(len(qs), np.nan)
    bid[:-1] = np.log(f[:-1] / f[1:]) / K + base
    ask[1:] = np.log(f[1:] / f[:-1]) / K + base
    return qs, bid, ask


def as_approx(q: float, tau: float) -> tuple[float, float]:
    """Avellaneda-Stoikov (2008) frozen-inventory approximation: distances from the mid."""
    base = base_half_spread()
    return base + (1 + 2 * q) * GAMMA * SIGMA**2 * tau / 2, base + (1 - 2 * q) * GAMMA * SIGMA**2 * tau / 2


def at(qs: np.ndarray, arr: np.ndarray, q: int) -> float:
    return float(arr[int(np.where(qs == q)[0][0])])


# ---------------------------------------------------------------- 1. constants and closed forms


def section_closed_forms() -> None:
    """Backs Core concepts (closed form), Example 1 and cards mm-glft-closed-form, mm-glft-numeric-skew."""
    print("\n1. constants and the closed-form approximation")
    alpha, eta = alpha_eta()
    check("alpha = k gamma sigma^2 / 2", alpha, 0.3, 1e-12)
    check("eta = A (1 + gamma/k)^-(1 + k/gamma)", eta, 49.85, 0.005)
    base = check("base half-spread ln(1 + gamma/k)/gamma", base_half_spread(), 0.6454, 5e-5)
    c = check("inventory coefficient c (skew per unit)", closed_form_c(), 0.0517, 5e-5)
    # c is also sqrt(alpha / eta) / k: the two expressions are independent algebra
    check("c via sqrt(alpha/eta)/k", math.sqrt(alpha / eta) / K, c, 1e-12)
    check("closed-form total spread 2 base + c", 2 * base + c, 1.3425, 5e-5)
    check("closed-form bid distance q = 0", base + 0.5 * c, 0.6712, 5e-5)
    check("closed-form bid distance q = 3", base + 3.5 * c, 0.8264, 5e-5)
    check("closed-form ask distance q = 3", base - 2.5 * c, 0.5161, 5e-5)
    # AS frozen-inventory skew per unit at T - t = 1 for comparison: gamma sigma^2 (T - t)
    check("AS skew per unit at T - t = 1", GAMMA * SIGMA**2 * 1.0, 0.4, 1e-12)
    check("ratio AS skew / GLFT skew", 0.4 / c, 7.73, 0.005)


# ---------------------------------------------------------------- 2. exact quotes and comparison


def section_exact() -> None:
    """Backs Example 2 and cards mm-glft-exact-quotes, mm-glft-stationary."""
    print("\n2. exact quotes (Q = 20, T - t = 1) against the closed form and AS")
    qs, bid, ask = glft_quotes(20, 1.0)
    c, base = closed_form_c(), base_half_spread()
    expected_bid = {0: 0.6716, 1: 0.7241, 2: 0.7764, 3: 0.8285}
    expected_ask = {0: 0.6716, 1: 0.6191, 2: 0.5667, 3: 0.5144}
    for q in range(4):
        b = check(f"exact bid distance q = {q}", at(qs, bid, q), expected_bid[q], 5e-5)
        a = check(f"exact ask distance q = {q}", at(qs, ask, q), expected_ask[q], 5e-5)
        # the closed form is within 0.0022 of the exact quotes for |q| <= 3
        assert abs(b - (base + (2 * q + 1) / 2 * c)) < 0.0022
        assert abs(a - (base - (2 * q - 1) / 2 * c)) < 0.0022
    cf_bid = {0: 0.6712, 1: 0.7230, 2: 0.7747, 3: 0.8264}
    cf_ask = {0: 0.6712, 1: 0.6195, 2: 0.5678, 3: 0.5161}
    for q in range(4):
        check(f"closed-form bid distance q = {q} (table)", base + (2 * q + 1) / 2 * c, cf_bid[q], 5e-5)
        check(f"closed-form ask distance q = {q} (table)", base - (2 * q - 1) / 2 * c, cf_ask[q], 5e-5)
    gap = max(abs(at(qs, bid, q) - (base + (2 * q + 1) / 2 * c)) for q in range(4))
    check("max |exact - closed form| over bid q = 0..3", gap, 0.0021, 5e-5)
    check("exact total spread q = 0", at(qs, bid, 0) + at(qs, ask, 0), 1.3433, 5e-5)
    check("exact skew per unit (bid q=1 minus bid q=0)", at(qs, bid, 1) - at(qs, bid, 0), 0.0524, 5e-5)
    b_as, a_as = as_approx(3, 1.0)
    check("AS approx bid distance q = 3, T - t = 1", b_as, 2.0454, 5e-5)
    check("AS approx ask distance q = 3, T - t = 1", a_as, -0.3546, 5e-5)
    # independent check: the eigendecomposition gives the same interior quotes
    alpha, eta = alpha_eta()
    m20 = tridiagonal(alpha * qs.astype(float) ** 2, eta)
    v_series, v_eig = propagate(m20, np.ones(len(qs)), 1.0), propagate_eig(m20, np.ones(len(qs)), 1.0)
    inner = slice(5, 36)  # |q| <= 15
    assert np.max(np.abs(np.log(v_series[inner] / v_eig[inner]))) < 1e-9
    # symmetry: delta_b(q) = delta_a(-q) when mu = 0
    assert max(abs(at(qs, bid, q) - at(qs, ask, -q)) for q in range(-19, 20)) < 1e-10

    print("\n   stationary limit (eigenvector of the smallest eigenvalue)")
    qs_s, bid_s, ask_s = glft_stationary(20)
    check("stationary bid distance q = 0", at(qs_s, bid_s, 0), 0.6716, 5e-5)
    check("stationary bid distance q = 3", at(qs_s, bid_s, 3), 0.8285, 5e-5)
    diff = max(abs(at(qs_s, bid_s, q) - at(qs, bid, q)) for q in range(-19, 20))
    assert diff < 1e-4, diff
    alpha, eta = alpha_eta()
    w = np.linalg.eigvalsh(tridiagonal(alpha * qs.astype(float) ** 2, eta))
    check("spectral gap lambda_1 - lambda_0", w[1] - w[0], 7.66, 0.005)
    check("Hermite gap 2 sqrt(alpha eta)", 2 * math.sqrt(alpha * eta), 7.73, 0.005)
    check("relaxation time 1 / gap", 1 / (w[1] - w[0]), 0.1306, 5e-5)


def section_horizon() -> None:
    """Backs Example 3 and card mm-glft-as-short-horizon."""
    print("\n3. horizon: exact quotes for q = 1 as T - t grows, against AS frozen inventory")
    rows = {0.01: (0.6514, 0.6434), 0.1: (0.6959, 0.6286), 0.25: (0.7206, 0.6203), 1.0: (0.7241, 0.6191)}
    for tau, (eb, ea) in rows.items():
        qs, bid, ask = glft_quotes(20, tau)
        check(f"exact bid q = 1, T - t = {tau}", at(qs, bid, 1), eb, 5e-5)
        check(f"exact ask q = 1, T - t = {tau}", at(qs, ask, 1), ea, 5e-5)
    as_rows = {0.01: (0.6514, 0.6434), 0.1: (0.7054, 0.6254), 0.25: (0.7954, 0.5954), 1.0: (1.2454, 0.4454)}
    for tau, (eb, ea) in as_rows.items():
        b, a = as_approx(1, tau)
        check(f"AS bid q = 1, T - t = {tau}", b, eb, 5e-5)
        check(f"AS ask q = 1, T - t = {tau}", a, ea, 5e-5)
    # short-horizon limit: the exact quotes agree with AS to O(tau^2)
    qs, bid, _ = glft_quotes(20, 0.01)
    check("|exact - AS| bid q = 1 at T - t = 0.01 (x1e4)", 1e4 * abs(at(qs, bid, 1) - as_approx(1, 0.01)[0]), 0.12, 0.005)


def section_bounds() -> None:
    """Backs Example 4 and card mm-glft-boundary."""
    print("\n4. inventory bound: Q = 5 against Q = 20 (T - t = 1)")
    qs5, bid5, ask5 = glft_quotes(5, 1.0)
    qs20, bid20, _ = glft_quotes(20, 1.0)
    check("Q = 5 bid distance q = 0", at(qs5, bid5, 0), 0.6777, 5e-5)
    check("Q = 5 bid distance q = 3", at(qs5, bid5, 3), 0.9225, 5e-5)
    check("Q = 5 bid distance q = 4", at(qs5, bid5, 4), 1.1259, 5e-5)
    check("Q = 20 bid distance q = 4", at(qs20, bid20, 4), 0.8803, 5e-5)
    assert math.isnan(at(qs5, bid5, 5)), "no bid at the long limit"
    check("Q = 5 ask distance q = 5", at(qs5, ask5, 5), 0.1649, 5e-5)
    # Q = 10, 20 and 40 agree to 1e-3 for |q| <= 3: the bound is not what drives section 2
    for q_max in (10, 40):
        qs, bid, _ = glft_quotes(q_max, 1.0)
        assert max(abs(at(qs, bid, q) - at(qs20, bid20, q)) for q in range(-3, 4)) < 1e-3


def section_drift() -> None:
    """Backs Example 5 and card mm-glft-drift."""
    print("\n5. drift extension: mu = 0.5")
    mu = 0.5
    c, base = closed_form_c(), base_half_spread()
    q0 = check("inventory target mu / (gamma sigma^2)", mu / (GAMMA * SIGMA**2), 1.25, 1e-12)
    qs, bid, ask = glft_quotes(20, 1.0, mu=mu)
    check("exact bid distance q = 0, mu = 0.5", at(qs, bid, 0), 0.6060, 5e-5)
    check("exact ask distance q = 0, mu = 0.5", at(qs, ask, 0), 0.7372, 5e-5)
    check("closed-form bid q = 0: base + (1/2 - q0) c", base + (0.5 - q0) * c, 0.6066, 5e-5)
    check("closed-form ask q = 0: base + (q0 + 1/2) c", base + (q0 + 0.5) * c, 0.7359, 5e-5)
    check("exact bid q = 1 (mu = 0.5)", at(qs, bid, 1), 0.6585, 5e-5)


def section_multi_asset() -> None:
    """Backs Example 6 and card mm-glft-multi-asset."""
    print("\n6. two correlated assets: sigma_1 = sigma_2 = 2, rho = 0.6, Q = 8 per asset, T - t = 1")
    rho, q_max = 0.6, 8
    cov = SIGMA**2 * np.array([[1.0, rho], [rho, 1.0]])
    _, eta = alpha_eta()
    grid = np.arange(-q_max, q_max + 1)
    n = len(grid)
    q1, q2 = np.meshgrid(grid, grid, indexing="ij")
    q1, q2 = q1.ravel(), q2.ravel()
    diag = K * GAMMA / 2 * (cov[0, 0] * q1**2 + 2 * cov[0, 1] * q1 * q2 + cov[1, 1] * q2**2)
    m = np.diag(diag)
    idx = {(a, b): i for i, (a, b) in enumerate(zip(q1, q2, strict=True))}
    for (a, b), i in idx.items():
        for da, db in ((1, 0), (0, 1)):
            j = idx.get((a + da, b + db))
            if j is not None:
                m[i, j] = m[j, i] = -eta
    v = propagate(m, np.ones(n * n), 1.0)
    base = base_half_spread()

    def bid1(a: int, b: int) -> float:
        return math.log(v[idx[(a, b)]] / v[idx[(a + 1, b)]]) / K + base

    # closed form: delta_b_i = base + (1/k) sqrt(k gamma / (2 eta)) [ (Sigma^1/2 q)_i + Sigma^1/2_ii / 2 ]
    w, vecs = np.linalg.eigh(cov)
    root = vecs @ np.diag(np.sqrt(w)) @ vecs.T
    scale = math.sqrt(K * GAMMA / (2 * eta)) / K

    def bid1_cf(a: int, b: int) -> float:
        return base + scale * (float((root @ np.array([a, b]))[0]) + root[0, 0] / 2)

    check("Sigma^1/2 diagonal entry", root[0, 0], 1.8974, 5e-5)
    check("Sigma^1/2 off-diagonal entry", root[0, 1], 0.6325, 5e-5)
    check("exact bid asset 1 at q = (0, 0)", bid1(0, 0), 0.6708, 5e-5)
    check("closed-form bid asset 1 at q = (0, 0)", bid1_cf(0, 0), 0.6699, 5e-5)
    check("exact bid asset 1 at q = (0, 3)", bid1(0, 3), 0.7184, 5e-5)
    check("closed-form bid asset 1 at q = (0, 3)", bid1_cf(0, 3), 0.7190, 5e-5)
    check("exact bid asset 1 at q = (3, 0)", bid1(3, 0), 0.8248, 5e-5)
    check("closed-form bid asset 1 at q = (3, 0)", bid1_cf(3, 0), 0.8171, 5e-5)
    cross = bid1(0, 3) - bid1(0, 0)
    check("cross-skew: asset-1 bid shift from 3 units of asset 2", cross, 0.0477, 5e-5)
    check("own-skew: asset-1 bid shift from 3 units of asset 1", bid1(3, 0) - bid1(0, 0), 0.1540, 5e-5)


def section_adverse_selection() -> None:
    """Backs Example 7 and cards mm-glft-adverse-static, mm-glft-adverse-roundtrip."""
    print("\n7. adverse selection")
    xi = 0.2
    # (a) one fill, risk neutral: maximise A exp(-k d) (d - xi); optimum 1/k + xi
    grid = np.linspace(0.0, 3.0, 300_001)
    g = A_RATE * np.exp(-K * grid) * (grid - xi)
    check("risk-neutral optimum with post-fill move xi = 0.2", float(grid[np.argmax(g)]), 0.8667, 5e-5)
    check("risk-neutral optimum without (1/k)", float(grid[np.argmax(A_RATE * np.exp(-K * grid) * grid)]), 0.6667, 5e-5)
    # (b) GLFT (2013) Section 5.2, Proposition 5: a permanent mid jump of xi in the aggressor's direction after
    # each fill.  With the plain substitution u = -exp(-gamma (x + q s)) v_q^(-gamma / k):
    # v_q' = alpha q^2 v_q - eta (e^{-k (q+1) xi} v_{q+1} + e^{k (q-1) xi} v_{q-1}); D = diag(e^{k xi q^2 / 2})
    # symmetrises it: v = D exp(-S tau) D^{-1} 1 with S = diag(alpha q^2) - eta e^{-k xi / 2} (shift).
    alpha, eta = alpha_eta()
    q_max = 10  # e^{-k xi Q^2 / 2} must stay far above round-off, and RK4 must stay stable
    qs = np.arange(-q_max, q_max + 1)
    base, c = base_half_spread(), closed_form_c()

    def quotes(tau: float) -> tuple[np.ndarray, np.ndarray]:
        dinv = np.exp(-K * xi * qs.astype(float) ** 2 / 2)
        wv = propagate(tridiagonal(alpha * qs.astype(float) ** 2, eta * math.exp(-K * xi / 2)), dinv, tau)
        v = wv / dinv  # D w, up to the normalisation
        bid = (qs[:-1] + 1) * xi + np.log(v[:-1] / v[1:]) / K + base
        ask = (1 - qs[1:]) * xi + np.log(v[1:] / v[:-1]) / K + base
        return bid, ask

    # brute-force check of the symmetrisation: integrate the unsymmetrised ODE with RK4
    tau, steps = 1.0, 20000
    h = tau / steps
    mfull = np.diag(alpha * qs.astype(float) ** 2)
    for i, q in enumerate(qs[:-1]):
        mfull[i, i + 1] = -eta * math.exp(-K * (q + 1) * xi)
        mfull[i + 1, i] = -eta * math.exp(K * q * xi)
    vv = np.ones(len(qs))
    for _ in range(steps):
        k1 = -mfull @ vv
        k2 = -mfull @ (vv + h / 2 * k1)
        k3 = -mfull @ (vv + h / 2 * k2)
        k4 = -mfull @ (vv + h * k3)
        vv = vv + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    bid_rk = (qs[:-1] + 1) * xi + np.log(vv[:-1] / vv[1:]) / K + base
    bid, ask = quotes(1.0)
    assert np.max(np.abs(bid_rk - bid)) < 1e-8
    # GLFT's own form of Proposition 5: w' = alpha q^2 w - eta e^{-k xi / 2} (w_{q+1} + w_{q-1}),
    # w_q(T) = exp(-k xi q^2 / 2), delta_b = ln(w_q / w_{q+1}) / k + xi / 2 + base; the eigendecomposition is
    # independent of the series used in quotes() and accurate here because Q = 10 keeps w well above round-off
    sym = tridiagonal(alpha * qs.astype(float) ** 2, eta * math.exp(-K * xi / 2))
    w = propagate_eig(sym, np.exp(-K * xi * qs.astype(float) ** 2 / 2), 1.0)
    bid_glft = np.log(w[:-1] / w[1:]) / K + xi / 2 + base
    ask_glft = np.log(w[1:] / w[:-1]) / K + xi / 2 + base
    assert np.max(np.abs(bid_glft - bid)) < 1e-8 and np.max(np.abs(ask_glft - ask)) < 1e-8
    i0 = q_max
    check("jump model, T - t = 0: bid q = 0 (base + xi)", float(quotes(0.0)[0][i0]), 0.8454, 5e-5)
    check("jump model, T - t = 1: bid q = 0", float(bid[i0]), 0.7737, 5e-5)
    check("closed form base + xi/2 + c e^{k xi/4} / 2", base + xi / 2 + c * math.exp(K * xi / 4) / 2, 0.7733, 5e-5)
    check("jump model, T - t = 1: total spread q = 0", float(bid[i0] + ask[i0 - 1]), 1.5474, 5e-5)
    check("no-jump total spread q = 0 (section 2)", 2 * float(glft_quotes(20, 1.0)[1][20]), 1.3433, 5e-5)


def section_simulation() -> None:
    """Backs Example 8."""
    print("\n8. simulation: exact GLFT quotes against the AS approximation (seed 11, 4000 paths)")
    rng = np.random.default_rng(11)
    paths, dt, horizon, q_max = 4000, 0.001, 1.0, 20
    steps = int(round(horizon / dt))
    alpha, eta = alpha_eta()
    qs = np.arange(-q_max, q_max + 1)
    m = tridiagonal(alpha * qs.astype(float) ** 2, eta)
    table = [np.ones(len(qs))]  # table[j] = v at T - t = j dt, built by stepping exp(-M dt)
    for _ in range(steps):
        table.append(propagate(m, table[-1], dt))
    base = base_half_spread()
    results = {}
    draws = [(rng.standard_normal((steps, paths)), rng.random((steps, paths)), rng.random((steps, paths)))]
    for name in ("GLFT", "AS"):
        dw, ub, ua = draws[0]
        s = np.full(paths, 100.0)
        q = np.zeros(paths, dtype=int)
        cash = np.zeros(paths)
        for i in range(steps):
            tau = horizon - i * dt
            if name == "GLFT":
                lv = np.log(table[steps - i])
                j = np.clip(q + q_max, 0, 2 * q_max)
                db = np.where(q < q_max, (lv[j] - lv[np.minimum(j + 1, 2 * q_max)]) / K + base, np.inf)
                da = np.where(q > -q_max, (lv[j] - lv[np.maximum(j - 1, 0)]) / K + base, np.inf)
            else:
                db = base + (1 + 2 * q) * GAMMA * SIGMA**2 * tau / 2
                da = base + (1 - 2 * q) * GAMMA * SIGMA**2 * tau / 2
            pb = np.minimum(A_RATE * np.exp(-K * db) * dt, 1.0)
            pa = np.minimum(A_RATE * np.exp(-K * da) * dt, 1.0)
            buy = ub[i] < pb
            sell = ua[i] < pa
            cash += np.where(buy, -(s - db), 0.0) + np.where(sell, s + da, 0.0)
            q += buy.astype(int) - sell.astype(int)
            s = s + SIGMA * math.sqrt(dt) * dw[i]
        wealth = cash + q * s
        ce = -math.log(np.mean(np.exp(-GAMMA * (wealth - wealth.mean())))) / GAMMA + wealth.mean()
        results[name] = (float(wealth.mean()), float(wealth.std(ddof=1)), float(ce), float(q.std(ddof=1)))
        print(f"   {name}: mean {wealth.mean():.2f} sd {wealth.std(ddof=1):.2f} CE {ce:.2f} sd(q_T) {q.std(ddof=1):.2f}")
    check("GLFT mean terminal P&L", results["GLFT"][0], 67.73, 0.01)
    check("GLFT sd of terminal P&L", results["GLFT"][1], 8.20, 0.01)
    check("GLFT certainty equivalent", results["GLFT"][2], 64.48, 0.01)
    check("AS-approx mean terminal P&L", results["AS"][0], 64.17, 0.01)
    check("AS-approx sd of terminal P&L", results["AS"][1], 7.28, 0.01)
    check("AS-approx certainty equivalent", results["AS"][2], 61.60, 0.01)
    check("CE advantage of exact GLFT over the AS approximation", results["GLFT"][2] - results["AS"][2], 2.87, 0.005)
    check("GLFT sd of final inventory", results["GLFT"][3], 3.50, 0.01)
    check("AS-approx sd of final inventory", results["AS"][3], 3.32, 0.01)


if __name__ == "__main__":
    section_closed_forms()
    section_exact()
    section_horizon()
    section_bounds()
    section_drift()
    section_multi_asset()
    section_adverse_selection()
    section_simulation()
    print("\nall checks passed")
