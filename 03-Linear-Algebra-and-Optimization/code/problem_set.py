"""Linear algebra and optimization problem set: every number quoted in note 11.

Run: uv run --no-project --with numpy python 03-Linear-Algebra-and-Optimization/code/problem_set.py

Each block names the card ids it backs: the la-ps cards of note 11, plus the cards of notes 01, 02, 05 and 10
whose numbers are asserted here.
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


def equicorrelation_cards() -> None:
    print("\n[la-ps-ones-matrix-eigenvalues, la-ps-equicorrelation-det, la-ps-equicorrelation-bound]")
    j = np.ones((5, 5))
    lam = np.linalg.eigvalsh(j)
    check("J_5 largest eigenvalue", lam[-1], 5.0, 1e-12)
    check("J_5 number of zero eigenvalues", int((np.abs(lam) < 1e-12).sum()), 4, 0)
    c = 0.5 * np.eye(4) + 0.5 * np.ones((4, 4))
    check("det((1 - 0.5) I + 0.5 J), n = 4", np.linalg.det(c), 0.3125, 1e-12)
    check("0.5^3 x 2.5", 0.5**3 * 2.5, 0.3125, 1e-12)
    inv = np.linalg.inv(c)
    check("inverse diagonal 2(1 - 0.2)", inv[0, 0], 1.6, 1e-12)
    check("inverse off-diagonal -2 x 0.2", inv[0, 1], -0.4, 1e-12)
    check("rho / (1 + (n - 1) rho)", 0.5 / (1 + 3 * 0.5), 0.2, 1e-12)
    check("eigenvalue 1 + (n - 1) rho", np.linalg.eigvalsh(c)[-1], 2.5, 1e-12)
    check("eigenvalue 1 - rho", np.linalg.eigvalsh(c)[0], 0.5, 1e-12)
    vol = np.full(4, 0.2)
    w = np.linalg.solve(c * np.outer(vol, vol), np.ones(4))
    w /= w.sum()
    check("GMV of equal-vol equicorrelated assets: max |w - 1/4|", np.abs(w - 0.25).max(), 0.0, 1e-12)

    def equicorr(rho: float) -> np.ndarray:
        return (1 - rho) * np.eye(4) + rho * np.ones((4, 4))

    def min_eig(rho: float) -> float:
        return float(np.linalg.eigvalsh(equicorr(rho))[0])

    lo, hi = -1.0, 0.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (lo, mid) if min_eig(mid) >= 0 else (mid, hi)
    check("n = 4 lower bound: most negative rho with min eigenvalue >= 0 (bisection)", hi, -0.333333, 1e-6)
    check("min eigenvalue at rho = -1/3", min_eig(-1 / 3), 0.0, 1e-12)
    check("min eigenvalue at rho = -1/3 - 0.01 (negative)", min_eig(-1 / 3 - 0.01), -0.03, 1e-12)
    check("equal-weight variance 1'C1/16 at rho = -1/3", np.ones(4) @ equicorr(-1 / 3) @ np.ones(4) / 16, 0.0, 1e-12)


def correlation_cards() -> None:
    print("\n[la-ps-third-correlation, la-ps-valid-correlation-matrix]")
    r12, r13 = 0.6, 0.8
    hw = math.sqrt((1 - r12**2) * (1 - r13**2))
    check("rho23 lower (0.6, 0.8)", r12 * r13 - hw, 0.0, 1e-12)
    check("rho23 upper (0.6, 0.8)", r12 * r13 + hw, 0.96, 1e-12)
    c = np.array([[1.0, 0.9, 0.2], [0.9, 1.0, 0.6], [0.2, 0.6, 1.0]])
    lo, hi = 0.9 * 0.6 - math.sqrt(0.19 * 0.64), 0.9 * 0.6 + math.sqrt(0.19 * 0.64)
    check("centre 0.9 x 0.6", 0.9 * 0.6, 0.54, 1e-12)
    check("half-width sqrt(0.19 x 0.64)", math.sqrt(0.19 * 0.64), 0.3487, 1e-4)
    check("half-width for (0.6, 0.8)", hw, 0.48, 1e-12)
    check("feasible rho13 lower given 0.9 and 0.6", lo, 0.1913, 1e-4)
    check("feasible rho13 upper", hi, 0.8887, 1e-4)
    check("det of the candidate matrix", np.linalg.det(c), 0.006, 1e-12)
    check("min eigenvalue of the candidate", np.linalg.eigvalsh(c)[0], 0.00337, 1e-5)
    c_bad = c.copy()
    c_bad[0, 2] = c_bad[2, 0] = 0.1
    check("det with rho13 = 0.1 (outside the range)", np.linalg.det(c_bad), -0.072, 1e-12)


def spectral_cards() -> None:
    print(
        "\n[la-ps-det-trace-from-eigenvalues, la-eig-trace-det, la-eig-two-by-two, la-ps-two-by-two-eigenvectors, "
        "la-ps-householder-reflector, la-ps-product-of-pd, la-ps-rotation-eigenvalues]"
    )
    lam = np.array([1.0, 2.0, 3.0])
    check("tr A", lam.sum(), 6.0, 1e-12)
    check("det A", np.prod(lam), 6.0, 1e-12)
    check("det(A^2 + I)", np.prod(lam**2 + 1), 100.0, 1e-12)
    check("tr(A^-1)", np.sum(1 / lam), 11 / 6, 1e-12)
    check("tr(A^-1) decimal", np.sum(1 / lam), 1.833333, 1e-6)
    m = np.array([[4.0, 1.0], [2.0, 3.0]])
    check("trace of [[4,1],[2,3]]", np.trace(m), 7.0, 1e-12)
    check("det of [[4,1],[2,3]]", np.linalg.det(m), 10.0, 1e-12)
    ev = np.sort(np.real(np.linalg.eigvals(m)))
    check("eigenvalue of [[4,1],[2,3]] (small)", ev[0], 2.0, 1e-12)
    check("eigenvalue of [[4,1],[2,3]] (large)", ev[1], 5.0, 1e-12)
    for lam_k, v in ((5.0, np.array([1.0, 1.0])), (2.0, np.array([1.0, -2.0]))):
        check(f"[[4,1],[2,3]] v = {lam_k:.0f} v residual", np.abs(m @ v - lam_k * v).max(), 0.0, 1e-12)
    u = np.array([1.0, 2.0, 2.0]) / 3.0
    householder = np.eye(3) - 2 * np.outer(u, u)
    check("det of Householder reflector I - 2uu'", np.linalg.det(householder), -1.0, 1e-12)
    ev = np.linalg.eigvalsh(householder)
    check("Householder eigenvalue min", ev[0], -1.0, 1e-12)
    check("Householder eigenvalue max", ev[-1], 1.0, 1e-12)
    pd_a = np.array([[2.0, 1.0], [1.0, 2.0]])
    pd_b = np.array([[1.0, 0.0], [0.0, 3.0]])
    ab = pd_a @ pd_b
    check("AB symmetric? max |AB - (AB)'|", np.abs(ab - ab.T).max(), 2.0, 1e-12)
    ev = np.sort(np.real(np.linalg.eigvals(ab)))
    check("AB eigenvalue min (positive)", ev[0], 4 - math.sqrt(7), 1e-12)
    check("AB eigenvalue max", ev[1], 4 + math.sqrt(7), 1e-12)
    check("4 - sqrt 7", 4 - math.sqrt(7), 1.354249, 1e-6)
    rot = np.array([[0.0, -1.0], [1.0, 0.0]])
    ev = np.linalg.eigvals(rot)
    check("90-degree rotation eigenvalue modulus", np.abs(ev).max(), 1.0, 1e-12)
    check("90-degree rotation eigenvalue imaginary part", np.abs(ev.imag).max(), 1.0, 1e-12)
    check("90-degree rotation eigenvalue real part", np.abs(ev.real).max(), 0.0, 1e-12)


def projection_and_trace_cards() -> None:
    print("\n[la-ps-hat-matrix-trace, la-ps-quadratic-form-expectation]")
    x = np.random.default_rng(0).standard_normal((100, 5))
    hat = x @ np.linalg.solve(x.T @ x, x.T)
    check("trace of hat matrix, n = 100, p = 5", np.trace(hat), 5.0, 1e-10)
    check("residual degrees of freedom tr(I - P)", np.trace(np.eye(100) - hat), 95.0, 1e-10)
    lam = np.linalg.eigvalsh(hat)
    check("eigenvalues equal to 1", int((np.abs(lam - 1) < 1e-8).sum()), 5, 0)
    a = np.diag([1.0, 2.0, 3.0])
    mu = np.ones(3)
    sigma = np.eye(3)
    check("E[x'Ax] = tr(A Sigma) + mu'A mu", np.trace(a @ sigma) + mu @ a @ mu, 12.0, 1e-12)
    z = np.random.default_rng(0).standard_normal((400_000, 3)) + mu
    check("simulated E[x'Ax] (fresh seed 0)", float(np.mean(np.einsum("ij,jk,ik->i", z, a, z))), 12.00, 5e-3)


def markov_and_recurrence_cards() -> None:
    print("\n[la-ps-three-state-markov, la-ps-fibonacci-closed-form, la-ps-ar2-stationarity]")
    p = np.array([[0.5, 0.5, 0.0], [0.25, 0.5, 0.25], [0.0, 0.5, 0.5]])
    lam, vec = np.linalg.eig(p.T)
    k = int(np.argmin(np.abs(lam - 1)))
    check("selected eigenvalue of P'", np.real(lam[k]), 1.0, 1e-12)
    pi = np.real(vec[:, k] / vec[:, k].sum())
    for i, want in enumerate((0.25, 0.5, 0.25)):
        check(f"stationary pi_{i + 1}", pi[i], want, 1e-12)
    ev = np.sort(np.real(lam))
    check("eigenvalues of P: smallest", ev[0], 0.0, 1e-12)
    check("eigenvalues of P: middle (mixing rate)", ev[1], 0.5, 1e-12)
    f50 = np.linalg.matrix_power(np.array([[1, 1], [1, 0]], dtype=object), 50)[0, 1]
    check("F_50", f50, 12586269025, 0)
    phi = (1 + math.sqrt(5)) / 2
    check("round(phi^50 / sqrt 5)", round(phi**50 / math.sqrt(5)), 12586269025, 0)
    roots = np.sort(np.real(np.roots([1.0, -0.5, -0.3])))
    check("AR(2) 0.5, 0.3: root 1", roots[0], -0.3521, 1e-4)
    check("AR(2) 0.5, 0.3: root 2", roots[1], 0.8521, 1e-4)


def portfolio_cards() -> None:
    print("\n[la-ps-two-asset-gmv, la-ps-zero-variance-hedge, la-ps-equal-weight-diversification]")
    s1, s2, rho = 0.2, 0.3, 0.5
    w1 = (s2**2 - rho * s1 * s2) / (s1**2 + s2**2 - 2 * rho * s1 * s2)
    check("GMV w1", w1, 6 / 7, 1e-12)
    check("GMV w1 decimal", w1, 0.857143, 1e-6)
    var = w1**2 * s1**2 + (1 - w1) ** 2 * s2**2 + 2 * w1 * (1 - w1) * rho * s1 * s2
    check("GMV vol", math.sqrt(var), 0.196396, 1e-6)
    check("zero-variance weight sigma2/(sigma1 + sigma2) at rho = -1", s2 / (s1 + s2), 0.6, 1e-12)
    w = np.array([0.6, 0.4])
    cov = np.array([[s1 * s1, -s1 * s2], [-s1 * s2, s2 * s2]])
    check("variance at that weight", w @ cov @ w, 0.0, 1e-15)
    sig, rho, n = 0.2, 0.3, 50
    var_n = sig**2 * (rho + (1 - rho) / n)
    check("equal-weight variance, n = 50", var_n, 0.01256, 1e-12)
    check("rho + (1 - rho)/n", rho + (1 - rho) / n, 0.314, 1e-12)
    check("equal-weight vol, n = 50", math.sqrt(var_n), 0.112071, 1e-6)
    check("limit vol sigma sqrt(rho)", sig * math.sqrt(rho), 0.109545, 1e-6)


def rayleigh_and_quadratic_cards() -> None:
    print("\n[la-ps-courant-fischer-second, la-ps-xy-nonconvex, la-ps-uv-plus-vu-rank]")
    a = np.array([[2.0, 1.0], [1.0, 2.0]])
    check("max x'Ax on the unit circle", np.linalg.eigvalsh(a)[-1], 3.0, 1e-12)
    check("min x'Ax on the unit circle", np.linalg.eigvalsh(a)[0], 1.0, 1e-12)
    q = np.linalg.qr(np.array([[1.0, 1.0], [1.0, -1.0]]))[0][:, 1:]
    lam_c, vec_c = np.linalg.eigh(q.T @ a @ q)
    x_c = q @ vec_c[:, -1]
    check("max x'Ax over unit x orthogonal to (1, 1)", lam_c[-1], 1.0, 1e-12)
    check("maximiser |x_1 + x_2| (orthogonal to (1, 1))", abs(x_c.sum()), 0.0, 1e-12)
    check("maximiser |x_1 - x_2| = sqrt 2", abs(x_c[0] - x_c[1]), math.sqrt(2), 1e-12)
    h = np.array([[0.0, 1.0], [1.0, 0.0]])
    check("Hessian of x1 x2: eigenvalue min", np.linalg.eigvalsh(h)[0], -1.0, 1e-12)
    u = np.array([1.0, 0.0, 0.0])
    v = np.array([1.0, 1.0, 0.0])
    m = np.outer(u, v) + np.outer(v, u)
    check("rank of uv' + vu'", np.linalg.matrix_rank(m), 2, 0)
    ev = np.linalg.eigvalsh(m)
    check("eigenvalue u'v - |u||v|", ev[0], 1 - math.sqrt(2), 1e-12)
    check("eigenvalue u'v + |u||v|", ev[2], 1 + math.sqrt(2), 1e-12)
    check("1 + sqrt 2", 1 + math.sqrt(2), 2.414214, 1e-6)


def sherman_morrison_card() -> None:
    print("\n[la-ps-inverse-identity-plus-ones]")
    n = 3
    m = np.eye(n) + np.ones((n, n))
    check("max |(I + J)^-1 - (I - J/4)|", np.abs(np.linalg.inv(m) - (np.eye(n) - np.ones((n, n)) / 4)).max(), 0.0, 1e-12)
    check("det(I + J) = 1 + n", np.linalg.det(m), 4.0, 1e-12)


def numerical_cards() -> None:
    print(
        "\n[la-ps-near-singular-condition, la-opt-newton-sqrt2, la-opt-bisection-count, la-ps-newton-reciprocal, "
        "la-ps-gd-step-size, la-ps-cholesky-2x2]"
    )
    m = np.array([[1.0, 1.0], [1.0, 1.0001]])
    check("cond_2 of [[1,1],[1,1.0001]]", np.linalg.cond(m), 40002.0, 1.0)
    ev = np.linalg.eigvalsh(m)
    check("eigenvalue small", ev[0], 0.00005, 1e-7)
    check("eigenvalue large", ev[1], 2.00005, 1e-7)
    check("digits lost log10(cond)", math.log10(np.linalg.cond(m)), 4.6, 0.01)
    x, path = 1.0, []
    for _ in range(4):
        x = 0.5 * (x + 2 / x)
        path.append(x)
    for k, want in enumerate((1.5, 1.416667, 1.414216, 1.41421356)):
        check(f"Newton sqrt 2 iterate {k + 1}", path[k], want, 5e-7 if k < 3 else 5e-9)
    check("Newton sqrt 2 iterate 4 error", abs(path[3] - math.sqrt(2)), 1.6e-12, 1e-13)
    for tol, want in ((1e-6, 20), (1e-12, 40)):
        lo, hi, steps = 1.0, 2.0, 0
        while hi - lo > tol:
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if mid * mid < 2 else (lo, mid)
            steps += 1
        check(f"bisection steps to {tol:g} from width 1", steps, want, 0)
    x, recip = 0.3, []
    for _ in range(3):
        x = x * (2 - 3 * x)
        recip.append(x)
    for k, want in enumerate((0.33, 0.3333, 0.33333333)):
        check(f"Newton reciprocal of 3, iterate {k + 1}", recip[k], want, 1e-12)
    check("error after 3 steps 1/3 - x_3", 1 / 3 - recip[2], 3.33e-9, 1e-11)
    a_gd = np.diag([1.0, 100.0])
    check("max stable gradient step 2/lambda_max for lambda_max = 100", 2 / np.linalg.eigvalsh(a_gd)[-1], 0.02, 1e-12)

    def gd_norm(eta: float, steps: int = 2000) -> float:
        x = np.ones(2)
        for _ in range(steps):
            x = x - eta * (a_gd @ x)
        return float(np.linalg.norm(x))

    check("gradient descent on diag(1, 100), eta = 0.019: |x_2000| (converges)", gd_norm(0.019), 0.0, 1e-12)
    check("eta = 0.021: log10 |x_2000| (diverges, |1 - 2.1| = 1.1 per step)", math.log10(gd_norm(0.021)), 2000 * math.log10(1.1), 1e-9)
    low = np.linalg.cholesky(np.array([[4.0, 2.0], [2.0, 3.0]]))
    check("Cholesky L11", low[0, 0], 2.0, 1e-12)
    check("Cholesky L21", low[1, 0], 1.0, 1e-12)
    check("Cholesky L22 = sqrt 2", low[1, 1], math.sqrt(2), 1e-12)


def counting_cards() -> None:
    print("\n[la-pca-factor-param-count, la-ps-sample-cov-rank]")
    n, k = 500, 10
    check("free parameters in a 500 x 500 covariance", n * (n + 1) // 2, 125250, 0)
    check("K = 10 factor model: N K + K(K+1)/2 + N", n * k + k * (k + 1) // 2 + n, 5555, 0)
    rng = np.random.default_rng(1)
    s = np.cov(rng.standard_normal((60, 100)), rowvar=False)
    check("rank of sample covariance, N = 100, T = 60", np.linalg.matrix_rank(s), 59, 0)
    check("zero eigenvalues, N = 100, T = 60", int((np.linalg.eigvalsh(s) < 1e-10).sum()), 41, 0)


def optimization_cards() -> None:
    print("\n[la-ps-lagrange-xy, la-ps-projection-onto-line, la-ps-kkt-halfspace]")

    def best_on_line(c: float) -> tuple[float, float]:
        xs = np.linspace(0.0, c, 100_001)
        vals = xs * (c - xs)
        i = int(np.argmax(vals))
        return float(xs[i]), float(vals[i])

    x_opt, value = best_on_line(10.0)
    check("grid along x + y = 10: argmax x", x_opt, 5.0, 1e-12)
    check("max xy s.t. x + y = 10", value, 25.0, 1e-12)
    check("multiplier from stationarity d(xy)/dx = y = lambda", 10.0 - x_opt, 5.0, 1e-12)
    check("dV/dc by finite difference of the grid optimum", (best_on_line(10.1)[1] - best_on_line(9.9)[1]) / 0.2, 5.0, 1e-9)
    a = np.array([1.0, 2.0])
    point = 5 * a / (a @ a)
    check("closest point to origin on x + 2y = 5: x", point[0], 1.0, 1e-12)
    check("closest point: y", point[1], 2.0, 1e-12)
    check("distance sqrt 5", np.linalg.norm(point), math.sqrt(5), 1e-12)
    ones = np.ones(2)

    def halfspace_projection(b: float) -> np.ndarray:
        return max(b, 0.0) / (ones @ ones) * ones

    x_star = halfspace_projection(2.0)
    check("min x^2 + y^2 s.t. x + y >= 2: x", x_star[0], 1.0, 1e-12)
    check("min x^2 + y^2 s.t. x + y >= 2: y", x_star[1], 1.0, 1e-12)
    check("optimal value", x_star @ x_star, 2.0, 1e-12)
    g = np.linspace(-3.0, 3.0, 601)
    gx, gy = np.meshgrid(g, g)
    f = np.where(gx + gy >= 2 - 1e-12, gx**2 + gy**2, np.inf)
    k = np.unravel_index(np.argmin(f), f.shape)
    check("grid search optimum x (step 0.01)", gx[k], 1.0, 1e-9)
    check("grid search optimum y", gy[k], 1.0, 1e-9)
    h = 1e-6
    lam = (halfspace_projection(2 + h) @ halfspace_projection(2 + h) - halfspace_projection(2 - h) @ halfspace_projection(2 - h)) / (2 * h)
    check("KKT multiplier for x + y >= 2 (dV/db)", lam, 2.0, 1e-6)
    check("stationarity residual max |2x - lambda (1, 1)|", np.abs(2 * x_star - lam * ones).max(), 0.0, 1e-6)


def taylor_cards() -> None:
    print("\n[la-ps-taylor-mental-math]")
    check("e^0.05", math.exp(0.05), 1.051271, 1e-6)
    check("x^2/2 at 0.05", 0.05**2 / 2, 0.00125, 1e-15)
    check("1 + x + x^2/2 at 0.05", 1 + 0.05 + 0.00125, 1.05125, 1e-12)
    check("ln 1.02", math.log(1.02), 0.0198026, 1e-7)
    check("x - x^2/2 at 0.02", 0.02 - 0.0002, 0.0198, 1e-12)
    check("sqrt(1.04)", math.sqrt(1.04), 1.019804, 1e-6)
    check("1 + x/2 - x^2/8 at 0.04", 1 + 0.02 - 0.0002, 1.0198, 1e-12)


def main() -> None:
    equicorrelation_cards()
    correlation_cards()
    spectral_cards()
    projection_and_trace_cards()
    markov_and_recurrence_cards()
    portfolio_cards()
    rayleigh_and_quadratic_cards()
    sherman_morrison_card()
    numerical_cards()
    counting_cards()
    optimization_cards()
    taylor_cards()
    print("\nall problem_set checks passed")


if __name__ == "__main__":
    main()
