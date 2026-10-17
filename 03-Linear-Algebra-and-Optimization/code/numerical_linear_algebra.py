"""Numerical linear algebra: every number quoted in note 06.

Run: uv run --no-project --with numpy python 03-Linear-Algebra-and-Optimization/code/numerical_linear_algebra.py

Rounding-error results depend on the BLAS build only in the last digits; the asserts use
order-of-magnitude bounds for those and tight tolerances for everything exact.
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


def check_between(label: str, value: float, lo: float, hi: float) -> float:
    """Print a labelled number and assert it lies in [lo, hi] (for rounding-error magnitudes)."""
    print(f"{label} = {float(value) + 0.0:.3g}")
    assert lo <= value <= hi, f"{label}: {value} not in [{lo}, {hi}]"
    return value


# ---------------------------------------------------------------------------
# Factorisations written out
# ---------------------------------------------------------------------------


def lu_no_pivot(a: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    n = a.shape[0]
    u = a.astype(float).copy()
    low = np.eye(n)
    for k in range(n - 1):
        for i in range(k + 1, n):
            low[i, k] = u[i, k] / u[k, k]
            u[i, k:] -= low[i, k] * u[k, k:]
    return low, u


def lu_partial_pivot(a: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """PA = LU with row swaps choosing the largest pivot in each column."""
    n = a.shape[0]
    u = a.astype(float).copy()
    low = np.eye(n)
    perm = np.arange(n)
    for k in range(n - 1):
        p = k + int(np.argmax(np.abs(u[k:, k])))
        if p != k:
            u[[k, p], k:] = u[[p, k], k:]
            low[[k, p], :k] = low[[p, k], :k]
            perm[[k, p]] = perm[[p, k]]
        for i in range(k + 1, n):
            low[i, k] = u[i, k] / u[k, k]
            u[i, k:] -= low[i, k] * u[k, k:]
    return perm, low, u


def forward_sub(low: np.ndarray, b: np.ndarray) -> np.ndarray:
    y = np.zeros_like(b, dtype=float)
    for i in range(len(b)):
        y[i] = (b[i] - low[i, :i] @ y[:i]) / low[i, i]
    return y


def back_sub(u: np.ndarray, y: np.ndarray) -> np.ndarray:
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - u[i, i + 1 :] @ x[i + 1 :]) / u[i, i]
    return x


def householder_qr(a: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Full QR by Householder reflections: Q is m x m orthogonal, R is m x n upper triangular."""
    m, n = a.shape
    r = a.astype(float).copy()
    q = np.eye(m)
    for k in range(min(m - 1, n)):
        x = r[k:, k]
        v = x.copy()
        v[0] += math.copysign(np.linalg.norm(x), x[0])  # sign choice avoids cancellation
        norm_v = np.linalg.norm(v)
        if norm_v == 0:
            continue
        v /= norm_v
        r[k:, :] -= 2.0 * np.outer(v, v @ r[k:, :])
        q[:, k:] -= 2.0 * np.outer(q[:, k:] @ v, v)
    return q, r


def gram_schmidt(a: np.ndarray, modified: bool) -> np.ndarray:
    m, n = a.shape
    q = np.zeros((m, n))
    for j in range(n):
        v = a[:, j].astype(float).copy()
        for i in range(j):
            coeff = q[:, i] @ (v if modified else a[:, j])
            v -= coeff * q[:, i]
        q[:, j] = v / np.linalg.norm(v)
    return q


def thomas(sub: np.ndarray, diag: np.ndarray, sup: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    """Tridiagonal solve in O(n): sub[i] multiplies x[i-1], sup[i] multiplies x[i+1]."""
    n = len(diag)
    c = np.zeros(n)
    d = np.zeros(n)
    c[0] = sup[0] / diag[0]
    d[0] = rhs[0] / diag[0]
    for i in range(1, n):
        denom = diag[i] - sub[i] * c[i - 1]
        c[i] = sup[i] / denom if i < n - 1 else 0.0
        d[i] = (rhs[i] - sub[i] * d[i - 1]) / denom
    x = np.zeros(n)
    x[-1] = d[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]
    return x


def conjugate_gradient(a: np.ndarray, b: np.ndarray, tol: float = 1e-10) -> tuple[np.ndarray, int]:
    x = np.zeros_like(b)
    r = b - a @ x
    p = r.copy()
    rs = r @ r
    for it in range(1, 10 * len(b)):
        ap = a @ p
        alpha = rs / (p @ ap)
        x += alpha * p
        r -= alpha * ap
        rs_new = r @ r
        if math.sqrt(rs_new) <= tol * np.linalg.norm(b):
            return x, it
        p = r + (rs_new / rs) * p
        rs = rs_new
    raise RuntimeError("CG did not converge")


def hilbert(n: int) -> np.ndarray:
    i = np.arange(n)
    return 1.0 / (i[:, None] + i[None, :] + 1)


# ---------------------------------------------------------------------------
# Demonstrations
# ---------------------------------------------------------------------------


def floating_point_basics() -> None:
    print("\n[06] IEEE double basics")
    eps = np.finfo(float).eps
    check("machine epsilon 2^-52", eps, 2.0**-52, 0)
    check("machine epsilon", eps, 2.220446e-16, 1e-22)
    check("unit roundoff 2^-53", eps / 2, 1.110223e-16, 1e-22)
    check("0.1 + 0.2 == 0.3", float(0.1 + 0.2 == 0.3), 0.0, 0)
    check("(0.1 + 0.2) - 0.3", (0.1 + 0.2) - 0.3, 5.551115e-17, 1e-22)
    check("1 + 2^-53 == 1 (round to even)", float(1.0 + 2.0**-53 == 1.0), 1.0, 0)
    check("2^53 + 1 == 2^53", float(2.0**53 + 1 == 2.0**53), 1.0, 0)
    check("2^53 (x 1e15)", 2.0**53 / 1e15, 9.007199, 1e-6)
    check("largest double", np.finfo(float).max, 1.797693e308, 1e302)


def pivoting_demo() -> None:
    print("\n[06] why partial pivoting: [[1e-20, 1], [1, 1]] x = [1, 2]")
    a = np.array([[1e-20, 1.0], [1.0, 1.0]])
    b = np.array([1.0, 2.0])
    low, u = lu_no_pivot(a)
    check("no pivot: multiplier l21", low[1, 0], 1e20, 1e5)
    check("no pivot: u22 (1 - 1e20 rounds to -1e20)", u[1, 1], -1e20, 1e5)
    x_bad = back_sub(u, forward_sub(low, b))
    check("no pivot: x1 (true value about 1)", x_bad[0], 0.0, 0)
    check("no pivot: x2", x_bad[1], 1.0, 0)
    perm, low_p, u_p = lu_partial_pivot(a)
    x_good = back_sub(u_p, forward_sub(low_p, b[perm]))
    check("pivoted: x1", x_good[0], 1.0, 1e-15)
    check("pivoted: x2", x_good[1], 1.0, 1e-15)
    check("pivoted: max |multiplier|", np.abs(np.tril(low_p, -1)).max(), 1e-20, 1e-25)


def conditioning_demo() -> None:
    print("\n[06] condition numbers and the Hilbert matrix")
    for n, want in ((5, 4.766e5), (10, 1.6025e13)):
        check(f"cond_2(H_{n})", np.linalg.cond(hilbert(n)), want, want * 1e-3)
    h = hilbert(10)
    x_true = np.ones(10)
    b = h @ x_true
    x = np.linalg.solve(h, b)
    rel_err = np.linalg.norm(x - x_true) / np.linalg.norm(x_true)
    check_between("H_10 solve: relative error in x", rel_err, 1e-6, 1e-2)
    rel_res = np.linalg.norm(h @ x - b) / np.linalg.norm(b)
    check_between("H_10 solve: relative residual", rel_res, 1e-18, 1e-14)
    check_between("H_10 digits lost log10(cond)", math.log10(np.linalg.cond(h)), 13.0, 13.4)
    x_inv = np.linalg.inv(h) @ b
    rel_res_inv = np.linalg.norm(h @ x_inv - b) / np.linalg.norm(b)
    check_between("H_10 via explicit inverse: relative residual", rel_res_inv, 1e-12, 1e-2)
    assert rel_res_inv > 10 * rel_res, "explicit inverse should leave a larger residual than a backward-stable solve"


def lauchli_normal_equations() -> None:
    print("\n[06] Lauchli matrix: normal equations versus QR")
    delta = 1e-8
    a = np.array([[1.0, 1.0], [delta, 0.0], [0.0, delta]])
    b = np.array([2.0, delta, delta])  # exact solution (1, 1)
    check("cond_2(A)", np.linalg.cond(a), math.sqrt(2 + delta**2) / delta, 1e-3)
    check("cond_2(A) value", np.linalg.cond(a), 1.414214e8, 1e2)
    kappa_u = check("kappa u", np.linalg.cond(a) * np.finfo(float).eps / 2, 1.57e-8, 1e-10)
    ata = a.T @ a
    check("fl(1 + delta^2) == 1", float(ata[0, 0] == 1.0), 1.0, 0)
    check("rank of computed A'A", np.linalg.matrix_rank(ata), 1, 0)
    q, r = householder_qr(a)
    x_qr = back_sub(r[:2, :2], (q.T @ b)[:2])
    check("QR solution x1 (within kappa u)", x_qr[0], 1.0, kappa_u)
    check("QR solution x2 (within kappa u)", x_qr[1], 1.0, kappa_u)
    check_between("max |Q'Q - I| (Householder)", np.abs(q.T @ q - np.eye(3)).max(), 0.0, 1e-14)


def orthogonality_loss() -> None:
    print("\n[06] loss of orthogonality on H_10 columns")
    a = hilbert(10)
    for name, q, lo, hi in (
        ("classical Gram-Schmidt", gram_schmidt(a, modified=False), 1e-1, 2.0),
        ("modified Gram-Schmidt", gram_schmidt(a, modified=True), 1e-6, 1e-2),
        ("Householder", householder_qr(a)[0], 1e-17, 1e-14),
    ):
        check_between(f"{name}: max |Q'Q - I|", np.abs(q.T @ q - np.eye(10)).max(), lo, hi)


def variance_cancellation() -> None:
    print("\n[06] catastrophic cancellation in the textbook variance formula")
    data = 1e9 + np.array([4.0, 7.0, 13.0, 16.0])
    n = len(data)
    naive = (np.sum(data**2) - np.sum(data) ** 2 / n) / (n - 1)
    mean, m2 = 0.0, 0.0
    for k, x in enumerate(data, 1):
        delta = x - mean
        mean += delta / k
        m2 += delta * (x - mean)
    welford = m2 / (n - 1)
    check("true sample variance", np.var(data - 1e9, ddof=1), 30.0, 1e-12)
    check("Welford sample variance", welford, 30.0, 1e-9)
    check("textbook sum-of-squares formula", naive, -170.6667, 1e-3)
    check("sum of squares magnitude (x 1e18)", np.sum(data**2) / 1e18, 4.0, 1e-6)
    check("double spacing near 4e18", np.spacing(np.sum(data**2)), 512.0, 0)
    two_pass = np.sum((data - data.mean()) ** 2) / (n - 1)
    check("two-pass formula", two_pass, 30.0, 1e-9)


def tridiagonal_demo() -> None:
    print("\n[06] tridiagonal system (-1, 2, -1), n = 100, by the Thomas algorithm")
    n = 100
    sub = np.full(n, -1.0)
    sup = np.full(n, -1.0)
    diag = np.full(n, 2.0)
    rhs = np.ones(n)
    x = thomas(sub, diag, sup, rhs)
    dense = np.diag(diag) + np.diag(sub[1:], -1) + np.diag(sup[:-1], 1)
    check_between("max |Thomas - dense solve|", np.abs(x - np.linalg.solve(dense, rhs)).max(), 0.0, 1e-9)
    check("x_50 (exact i(n + 1 - i)/2)", x[49], 50 * 51 / 2, 1e-9)
    check("cond_2 of the (-1,2,-1) matrix, n = 100", np.linalg.cond(dense), 4133.6, 0.1)
    _, iters = conjugate_gradient(dense, rhs)
    check("CG iterations to 1e-10 (n = 100)", iters, 50, 0)


def cholesky_ldl_cost() -> None:
    print("\n[06] flop counts for n = 1000 (leading terms)")
    n = 1000
    for name, flops, want in (
        ("LU 2n^3/3", 2 * n**3 / 3, 6.667e8),
        ("Cholesky n^3/3", n**3 / 3, 3.333e8),
        ("Householder QR 4n^3/3", 4 * n**3 / 3, 1.333e9),
        ("explicit inverse 2n^3", 2 * n**3, 2.0e9),
        ("matrix-vector 2n^2", 2 * n**2, 2.0e6),
        ("triangular solve n^2", n**2, 1.0e6),
    ):
        check(name, flops, want, want * 1e-3)
    # least squares, m = 10000 rows, n = 100 columns
    m, k = 10_000, 100
    check("normal equations m n^2 + n^3/3", m * k**2 + k**3 / 3, 1.00333e8, 1e4)
    check("Householder least squares 2 m n^2 - 2n^3/3", 2 * m * k**2 - 2 * k**3 / 3, 1.9933e8, 1e4)


def main() -> None:
    floating_point_basics()
    pivoting_demo()
    conditioning_demo()
    lauchli_normal_equations()
    orthogonality_loss()
    variance_cancellation()
    tridiagonal_demo()
    cholesky_ldl_cost()
    print("\nall numerical_linear_algebra checks passed")


if __name__ == "__main__":
    main()
