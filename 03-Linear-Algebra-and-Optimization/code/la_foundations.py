"""Linear maps, eigendecomposition and SVD: every number quoted in notes 01, 02 and 03.

Run: uv run --no-project --with numpy python 03-Linear-Algebra-and-Optimization/code/la_foundations.py

Each figure is printed and asserted, so a change in the maths or in numpy shows up as a failure.
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
# Note 01: rank, null space, replication and projection
# ---------------------------------------------------------------------------


def replication_complete_market() -> None:
    """Three states, three assets (bond, stock, call K=100): solve for an Arrow security and state prices."""
    print("\n[01] complete three-state market")
    payoff = np.array([[1.0, 80.0, 0.0], [1.0, 100.0, 0.0], [1.0, 120.0, 20.0]])  # rows = states, cols = assets
    prices = np.array([1.0, 100.0, 8.0])
    check("rank of payoff matrix", np.linalg.matrix_rank(payoff), 3, 0)
    arrow_mid = np.linalg.solve(payoff, np.array([0.0, 1.0, 0.0]))
    check("mid Arrow: bonds", arrow_mid[0], -4.0, 1e-12)
    check("mid Arrow: shares", arrow_mid[1], 0.05, 1e-12)
    check("mid Arrow: calls", arrow_mid[2], -0.1, 1e-12)
    check("mid Arrow price", arrow_mid @ prices, 0.2, 1e-12)
    state_prices = np.linalg.solve(payoff.T, prices)
    for name, q, want in zip(("down", "mid", "up"), state_prices, (0.4, 0.2, 0.4), strict=True):
        check(f"state price {name}", q, want, 1e-12)
    assert np.all(state_prices > 0), "positive state prices <=> no arbitrage"


def replication_incomplete_market() -> None:
    """Drop the call: rank 2 in 3 states; project the mid Arrow payoff onto span{bond, stock}."""
    print("\n[01] incomplete market: least squares as projection")
    x = np.array([[1.0, 80.0], [1.0, 100.0], [1.0, 120.0]])
    y = np.array([0.0, 1.0, 0.0])
    check("rank of two-asset payoff matrix", np.linalg.matrix_rank(x), 2, 0)
    beta = np.linalg.solve(x.T @ x, x.T @ y)  # fine here: tiny, well scaled
    check("best bonds", beta[0], 1 / 3, 1e-12)
    check("best shares", beta[1], 0.0, 1e-12)
    resid = y - x @ beta
    check("residual norm", np.linalg.norm(resid), math.sqrt(6) / 3, 1e-12)
    check("residual orthogonal to columns (max |X'r|)", np.abs(x.T @ resid).max(), 0.0, 1e-12)
    hat = x @ np.linalg.solve(x.T @ x, x.T)
    check("trace of hat matrix", np.trace(hat), 2.0, 1e-12)
    check("idempotence error |P^2 - P|", np.abs(hat @ hat - hat).max(), 0.0, 1e-12)
    # state prices consistent with bond = 1 and stock = 100 form a line q = (t, 1 - 2t, t)
    null = np.array([1.0, -2.0, 1.0])
    check("null direction of X' (max |X' n|)", np.abs(x.T @ null).max(), 0.0, 1e-12)
    prices = np.array([1.0, 100.0])
    for t in (1e-9, 0.25, 0.5 - 1e-9):
        q = np.array([t, 1 - 2 * t, t])
        assert np.abs(x.T @ q - prices).max() < 1e-12 and np.all(q > 0)
    vertices = []
    for basis in ((0, 1), (0, 2), (1, 2)):
        q = np.zeros(3)
        q[list(basis)] = np.linalg.solve(x[list(basis)].T, prices)
        if np.all(q >= -1e-12):
            vertices.append(q)
    mid = [q[1] for q in vertices]
    check("mid Arrow price upper bound (max q_2 over vertices, not attained by q > 0)", max(mid), 1.0, 1e-12)
    check("mid Arrow price lower bound (min q_2 over vertices, not attained by q > 0)", min(mid), 0.0, 1e-12)


def min_variance_hedge() -> None:
    """Hedge ratio as the projection of the asset return onto the hedge return."""
    print("\n[01] minimum-variance hedge")
    sig_s, sig_f, rho = 0.20, 0.25, 0.9
    h = rho * sig_s / sig_f
    check("hedge ratio h*", h, 0.72, 1e-12)
    check("hedge effectiveness R^2", rho**2, 0.81, 1e-12)
    check("residual vol", sig_s * math.sqrt(1 - rho**2), 0.0871780, 1e-6)
    check("residual vol as a fraction of the original", math.sqrt(1 - rho**2), 0.43589, 1e-5)


def one_factor_sherman_morrison() -> None:
    """Sigma = s_m^2 b b' + D: inverse by Sherman-Morrison, det by the matrix determinant lemma, GMV in O(N)."""
    print("\n[01] one-factor covariance: Sherman-Morrison")
    beta = np.array([0.8, 1.0, 1.2])
    s_m = 0.2
    d = np.array([0.10, 0.15, 0.20]) ** 2
    check("D_22 = 0.15^2", d[1], 0.0225, 1e-15)
    sigma = s_m**2 * np.outer(beta, beta) + np.diag(d)
    dinv_b = beta / d
    denom = 1 + s_m**2 * beta @ dinv_b
    sigma_inv = np.diag(1 / d) - s_m**2 * np.outer(dinv_b, dinv_b) / denom
    check("max |SM inverse - numpy inverse|", np.abs(sigma_inv - np.linalg.inv(sigma)).max(), 0.0, 1e-9)
    det_lemma = np.prod(d) * denom
    check("det via lemma (x1e6)", det_lemma * 1e6, np.linalg.det(sigma) * 1e6, 1e-9)
    check("1 + s_m^2 b'D^-1 b", denom, 6.777778, 1e-6)
    check("b'D^-1 b", beta @ dinv_b, 144.4444, 1e-4)
    check("b'D^-1 b term 1", beta[0] ** 2 / d[0], 64.0, 1e-9)
    check("b'D^-1 b term 2", beta[1] ** 2 / d[1], 44.4444, 1e-4)
    check("b'D^-1 b term 3", beta[2] ** 2 / d[2], 36.0, 1e-9)
    check("det D (x1e6)", np.prod(d) * 1e6, 9.0, 1e-9)
    check("det Sigma (x1e5)", det_lemma * 1e5, 6.1, 1e-9)
    ones = np.ones(3)
    w = sigma_inv @ ones / (ones @ sigma_inv @ ones)
    for i, want in enumerate((0.9445, 0.1372, -0.0818)):
        check(f"GMV weight {i + 1}", w[i], want, 1e-4)
    check("GMV vol", math.sqrt(w @ sigma @ w), 0.18675, 1e-5)


def determinant_trace_facts() -> None:
    print("\n[01] determinant and trace identities")
    rng = np.random.default_rng(0)
    a = rng.standard_normal((4, 4))
    b = rng.standard_normal((4, 4))
    check("det(AB) - det(A)det(B)", np.linalg.det(a @ b) - np.linalg.det(a) * np.linalg.det(b), 0.0, 1e-9)
    check("tr(AB) - tr(BA)", np.trace(a @ b) - np.trace(b @ a), 0.0, 1e-12)
    check("det(2A) / det(A) for 4x4", np.linalg.det(2 * a) / np.linalg.det(a), 16.0, 1e-9)
    a3 = np.triu(rng.standard_normal((4, 4)), 1) + np.diag([1.0, 1.0, 1.0, 3.0])  # det = 3
    check("card: det A", np.linalg.det(a3), 3.0, 1e-9)
    check("card: det 2A", np.linalg.det(2 * a3), 48.0, 1e-9)
    check("card: det A^-1", np.linalg.det(np.linalg.inv(a3)), 1 / 3, 1e-9)
    check("card: det A'A", np.linalg.det(a3.T @ a3), 9.0, 1e-9)
    m = np.array([[4.0, 2.0], [2.0, 3.0]])
    check("card: det [[4,2],[2,3]]", np.linalg.det(m), 8.0, 1e-12)
    check("card: max |inverse - [[3,-2],[-2,4]]/8|", np.abs(np.linalg.inv(m) - np.array([[3, -2], [-2, 4]]) / 8).max(), 0.0, 1e-15)
    low_rank = rng.standard_normal((5, 3)) @ rng.standard_normal((3, 8))
    check("card: rank of a 5 x 8 product of rank 3", np.linalg.matrix_rank(low_rank), 3, 0)
    check("card: null space dimension 8 - 3", low_rank.shape[1] - np.linalg.matrix_rank(low_rank), 5, 0)
    check("card: left null space dimension 5 - 3", low_rank.shape[0] - np.linalg.matrix_rank(low_rank), 2, 0)


# ---------------------------------------------------------------------------
# Note 02: eigenvalues, spectral theorem, power iteration, Gershgorin, Markov chains
# ---------------------------------------------------------------------------


def two_by_two_powers() -> None:
    print("\n[02] A = [[2,1],[1,2]]")
    a = np.array([[2.0, 1.0], [1.0, 2.0]])
    lam, vec = np.linalg.eigh(a)
    check("lambda_min", lam[0], 1.0, 1e-12)
    check("lambda_max", lam[1], 3.0, 1e-12)
    a10 = vec @ np.diag(lam**10) @ vec.T
    check("A^10 diagonal", a10[0, 0], 29525, 1e-6)
    check("A^10 off-diagonal", a10[0, 1], 29524, 1e-6)
    check("3^10 = lambda_max^10", lam[1] ** 10, 59049, 1e-6)
    assert np.array_equal(np.linalg.matrix_power(a.astype(np.int64), 10), np.array([[29525, 29524], [29524, 29525]]))


def regime_markov_chain() -> None:
    print("\n[02] two-state regime chain")
    p = np.array([[0.9, 0.1], [0.2, 0.8]])
    lam, left = np.linalg.eig(p.T)
    k = int(np.argmin(np.abs(lam - 1)))
    pi = np.real(left[:, k] / left[:, k].sum())
    check("pi calm", pi[0], 2 / 3, 1e-12)
    check("pi stressed", pi[1], 1 / 3, 1e-12)
    second = float(np.sort(np.real(lam))[0])
    check("second eigenvalue", second, 0.7, 1e-12)
    check("deviation factor after 10 steps 0.7^10", second**10, 0.0282475, 1e-7)
    p10 = np.linalg.matrix_power(p, 10)
    check("P^10[calm, calm]", p10[0, 0], 2 / 3 + (1 / 3) * 0.7**10, 1e-12)
    check("half-life of deviation (steps)", math.log(2) / -math.log(second), 1.94335, 1e-5)
    check("mean calm spell 1/(1 - P[calm, calm])", 1 / (1 - p[0, 0]), 10.0, 1e-12)
    check("mean stressed spell 1/(1 - P[stressed, stressed])", 1 / (1 - p[1, 1]), 5.0, 1e-12)


CORR3 = np.array([[1.0, 0.6, 0.3], [0.6, 1.0, 0.5], [0.3, 0.5, 1.0]])


def power_iteration(a: np.ndarray, x0: np.ndarray, tol: float = 1e-10, max_iter: int = 1000) -> tuple[float, np.ndarray, int]:
    """Return (eigenvalue, unit eigenvector, iterations) for the dominant eigenpair."""
    x = x0 / np.linalg.norm(x0)
    lam = x @ a @ x
    for it in range(1, max_iter + 1):
        y = a @ x
        x_new = y / np.linalg.norm(y)
        lam_new = x_new @ a @ x_new
        if abs(lam_new - lam) < tol:
            return lam_new, x_new, it
        x, lam = x_new, lam_new
    raise RuntimeError("power iteration did not converge")


def power_iteration_and_gershgorin() -> None:
    print("\n[02] power iteration and Gershgorin on a 3x3 correlation matrix")
    lam = np.linalg.eigvalsh(CORR3)
    check("lambda_1", lam[2], 1.94378, 1e-5)
    check("lambda_2", lam[1], 0.70688, 1e-5)
    check("lambda_3", lam[0], 0.34934, 1e-5)
    check("trace = sum of eigenvalues", lam.sum(), 3.0, 1e-12)
    check("det = product of eigenvalues", np.prod(lam), np.linalg.det(CORR3), 1e-12)
    check("det", np.linalg.det(CORR3), 0.48, 1e-12)
    check("ratio lambda_2 / lambda_1", lam[1] / lam[2], 0.36366, 1e-5)
    lam_pi, v, iters = power_iteration(CORR3, np.ones(3))
    check("power iteration eigenvalue", lam_pi, lam[2], 1e-9)
    check("power iteration steps to 1e-10", iters, 10, 0)
    for i, want in enumerate((0.5700, 0.6372, 0.5188)):
        check(f"top eigenvector component {i + 1}", abs(v[i]), want, 1e-4)
    radii = np.abs(CORR3).sum(axis=1) - 1
    for i, want in enumerate((0.9, 1.1, 0.8)):
        check(f"Gershgorin radius {i + 1}", radii[i], want, 1e-12)
    check("(lambda_2 / lambda_1)^2", (lam[1] / lam[2]) ** 2, 0.13225, 1e-5)
    check("Gershgorin lower bound", (1 - radii).min(), -0.1, 1e-12)
    check("Gershgorin upper bound", (1 + radii).max(), 2.1, 1e-12)
    check("share of variance on top eigenvector", lam[2] / 3, 0.64793, 1e-5)


def equicorrelation_spectrum() -> None:
    print("\n[02] equicorrelation n = 10, rho = 0.3")
    n, rho = 10, 0.3
    c = (1 - rho) * np.eye(n) + rho * np.ones((n, n))
    lam = np.linalg.eigvalsh(c)
    check("top eigenvalue 1 + (n-1) rho", lam[-1], 3.7, 1e-12)
    check("other eigenvalues 1 - rho", lam[0], 0.7, 1e-12)
    check("market-mode share", lam[-1] / n, 0.37, 1e-12)
    check("det", np.linalg.det(c), 0.7**9 * 3.7, 1e-12)


def ar2_companion() -> None:
    print("\n[02] AR(2) companion matrix")
    comp = np.array([[1.2, -0.35], [1.0, 0.0]])
    lam = np.sort(np.real(np.linalg.eigvals(comp)))
    check("root 1", lam[1], 0.7, 1e-12)
    check("root 2", lam[0], 0.5, 1e-12)


def fibonacci() -> None:
    print("\n[02] Fibonacci by eigen-decomposition")
    phi = (1 + math.sqrt(5)) / 2
    check("golden ratio", phi, 1.618034, 1e-6)
    f30 = np.linalg.matrix_power(np.array([[1, 1], [1, 0]], dtype=np.int64), 30)[0, 1]
    check("F_30", f30, 832040, 0)
    check("phi^30 / sqrt(5)", phi**30 / math.sqrt(5), 832040.0000002, 1e-6)


# ---------------------------------------------------------------------------
# Note 03: SVD, Eckart-Young, pseudo-inverse, ridge shrinkage
# ---------------------------------------------------------------------------


def svd_by_hand() -> None:
    print("\n[03] SVD of [[3,0],[4,5]]")
    a = np.array([[3.0, 0.0], [4.0, 5.0]])
    u, s, vt = np.linalg.svd(a)
    check("sigma_1 = sqrt(45)", s[0], math.sqrt(45), 1e-12)
    check("sigma_2 = sqrt(5)", s[1], math.sqrt(5), 1e-12)
    check("sigma_1", s[0], 6.708204, 1e-6)
    check("sigma_2", s[1], 2.236068, 1e-6)
    check("condition number", s[0] / s[1], 3.0, 1e-12)
    check("Frobenius norm", np.linalg.norm(a), math.sqrt(50), 1e-12)
    check("|det| = product of singular values", abs(np.linalg.det(a)), 15.0, 1e-12)
    sign = np.sign(u[0, 0])
    check("u_1 first component 1/sqrt(10)", sign * u[0, 0], 1 / math.sqrt(10), 1e-12)
    check("u_1 second component 3/sqrt(10)", sign * u[1, 0], 3 / math.sqrt(10), 1e-12)
    check("v_1 components 1/sqrt(2)", abs(vt[0, 0]), 1 / math.sqrt(2), 1e-12)
    check("eigenvalues of A'A: 45", np.linalg.eigvalsh(a.T @ a)[1], 45.0, 1e-12)
    check("eigenvalues of A'A: 5", np.linalg.eigvalsh(a.T @ a)[0], 5.0, 1e-12)
    a1 = s[0] * np.outer(u[:, 0], vt[0])
    for (i, j), want in zip(((0, 0), (0, 1), (1, 0), (1, 1)), (1.5, 1.5, 4.5, 4.5), strict=True):
        check(f"rank-1 approx entry {i}{j}", a1[i, j], want, 1e-12)
    check("rank-1 error, 2-norm", np.linalg.norm(a - a1, 2), math.sqrt(5), 1e-12)
    check("rank-1 error, Frobenius", np.linalg.norm(a - a1), math.sqrt(5), 1e-12)


def eckart_young_random() -> None:
    print("\n[03] Eckart-Young on a random 50 x 30 matrix")
    rng = np.random.default_rng(7)
    a = rng.standard_normal((50, 30))
    u, s, vt = np.linalg.svd(a, full_matrices=False)
    k = 5
    ak = (u[:, :k] * s[:k]) @ vt[:k]
    err = np.linalg.norm(a - ak)
    check("rank-5 Frobenius error = sqrt(sum tail sigma^2)", err, math.sqrt((s[k:] ** 2).sum()), 1e-9)
    check("rank-5 2-norm error = sigma_6", np.linalg.norm(a - ak, 2), s[k], 1e-9)
    check("rank-5 Frobenius error (quoted)", err, 29.76, 5e-3)
    check("rank-5 2-norm error (quoted)", np.linalg.norm(a - ak, 2), 9.33, 5e-3)
    best_random = min(np.linalg.norm(a - q @ (q.T @ a)) for q in (np.linalg.qr(rng.standard_normal((50, k)))[0] for _ in range(200)))
    assert best_random > err, "no random rank-5 projection beats the truncated SVD"
    check("best of 200 random rank-5 projections (seed 7)", best_random, 35.2497, 1e-3)
    check("sigma_1 of the random matrix", s[0], 11.4815, 1e-3)
    check("rank-5 energy share", (s[:k] ** 2).sum() / (s**2).sum(), 0.3879, 1e-4)


def pseudo_inverse_collinear() -> None:
    print("\n[03] pseudo-inverse with duplicated regressor")
    x1 = np.array([1.0, 2.0, 3.0])
    x = np.column_stack([x1, x1])
    y = np.array([2.0, 4.0, 6.3])
    check("rank of design", np.linalg.matrix_rank(x), 1, 0)
    beta = np.linalg.pinv(x) @ y
    single = x1 @ y / (x1 @ x1)
    check("x'y", x1 @ y, 28.9, 1e-12)
    check("x'x", x1 @ x1, 14.0, 1e-12)
    check("single-regressor slope", single, 2.0642857, 1e-6)
    check("min-norm beta_1", beta[0], single / 2, 1e-12)
    check("min-norm beta_2", beta[1], single / 2, 1e-12)
    xp = np.linalg.pinv(x)
    for name, err in (
        ("X X+ X = X", np.abs(x @ xp @ x - x).max()),
        ("X+ X X+ = X+", np.abs(xp @ x @ xp - xp).max()),
        ("(X X+)' = X X+", np.abs((x @ xp).T - x @ xp).max()),
        ("(X+ X)' = X+ X", np.abs((xp @ x).T - xp @ x).max()),
    ):
        check(f"Penrose {name}", err, 0.0, 1e-12)


def ridge_shrinkage() -> None:
    print("\n[03] ridge as SVD shrinkage, sigma = (10, 1, 0.1), lambda = 1")
    s = np.array([10.0, 1.0, 0.1])
    lam = 1.0
    f = s**2 / (s**2 + lam)
    for v, want in zip(f, (0.990099, 0.5, 0.00990099), strict=True):
        check("shrink factor", v, want, 1e-8)
    check("effective degrees of freedom", f.sum(), 1.5, 1e-12)
    check("OLS amplification of the weakest direction 1/sigma_3", 1 / s[2], 10.0, 1e-12)
    check("ridge cut of the weakest direction 1/f_3", 1 / f[2], 101.0, 1e-9)
    # numerical check on a design with these singular values
    rng = np.random.default_rng(1)
    u = np.linalg.qr(rng.standard_normal((20, 3)))[0]
    v = np.linalg.qr(rng.standard_normal((3, 3)))[0]
    x = (u * s) @ v.T
    y = rng.standard_normal(20)
    ridge = np.linalg.solve(x.T @ x + lam * np.eye(3), x.T @ y)
    via_svd = v @ ((s / (s**2 + lam)) * (u.T @ y))
    check("max |ridge normal-eq - ridge SVD|", np.abs(ridge - via_svd).max(), 0.0, 1e-12)


def main() -> None:
    replication_complete_market()
    replication_incomplete_market()
    min_variance_hedge()
    one_factor_sherman_morrison()
    determinant_trace_facts()
    two_by_two_powers()
    regime_markov_chain()
    power_iteration_and_gershgorin()
    equicorrelation_spectrum()
    ar2_companion()
    fibonacci()
    svd_by_hand()
    eckart_young_random()
    pseudo_inverse_collinear()
    ridge_shrinkage()
    print("\nall la_foundations checks passed")


if __name__ == "__main__":
    main()
