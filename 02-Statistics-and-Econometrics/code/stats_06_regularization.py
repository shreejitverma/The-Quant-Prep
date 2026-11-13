"""Regularization: every ridge, lasso and shrinkage number in the note, by an independent route.

Backs every number in `02-Statistics-and-Econometrics/06-Regularization-Ridge-Lasso.md`.
Independent routes used here:
- quoted ridge solutions checked by solving the normal equations on an explicit design and through the SVD;
- quoted lasso solutions checked against a from-scratch cyclic coordinate-descent solver and against the
  KKT (subgradient) conditions, never by applying the soft-threshold formula to itself;
- the optimal scalar shrinkage by a grid search over lambda and by seeded simulation;
- the Laplace-prior variance by quadrature, and the Hoerl-Kennard existence result by evaluating the exact
  ridge MSE on random designs.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 02-Statistics-and-Econometrics/code/stats_06_regularization.py`.
"""

from __future__ import annotations

import math

import numpy as np

SEED = 20261112


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def vec(label: str, value: np.ndarray, expected: tuple[float, ...], decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert np.all(np.abs(np.asarray(value) - np.asarray(expected)) <= tol), f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = ({', '.join(f'{v:.{decimals}f}' for v in value)})")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol:.4f})")


def lasso_cd(xtx: np.ndarray, xty: np.ndarray, lam: float, iters: int = 20000) -> np.ndarray:
    """Cyclic coordinate descent for 0.5 ||y - Xb||^2 + lam ||b||_1, using only X'X and X'y."""
    b = np.zeros(len(xty))
    for _ in range(iters):
        old = b.copy()
        for j in range(len(b)):
            rho = xty[j] - xtx[j] @ b + xtx[j, j] * b[j]
            b[j] = np.sign(rho) * max(abs(rho) - lam, 0.0) / xtx[j, j]
        if np.max(np.abs(b - old)) < 1e-15:
            break
    return b


def kkt_ok(xtx: np.ndarray, xty: np.ndarray, b: np.ndarray, lam: float) -> bool:
    grad = xty - xtx @ b  # X'(y - Xb)
    for j, bj in enumerate(b):
        if bj != 0 and abs(grad[j] - lam * np.sign(bj)) > 1e-9:
            return False
        if bj == 0 and abs(grad[j]) > lam + 1e-9:
            return False
    return True


def orthonormal_example(rng: np.random.Generator) -> None:
    print("Example 1 and cards stat-ridge-orthonormal-ridge-lasso, stat-ridge-lambda-max")
    n, beta_ols = 40, np.array([3.0, 1.0, -0.5, 0.2])
    X, _ = np.linalg.qr(rng.standard_normal((n, 4)))
    noise = rng.standard_normal(n)
    noise -= X @ (X.T @ noise)  # residual orthogonal to the columns, so OLS is exactly beta_ols
    y = X @ beta_ols + noise
    ridge = np.linalg.solve(X.T @ X + 1.0 * np.eye(4), X.T @ y)
    vec("ridge, lambda = 1, from (X'X + I)^-1 X'y", ridge, (1.5, 0.5, -0.25, 0.1), 10)
    lasso_quoted = np.array([2.2, 0.2, 0.0, 0.0])
    assert kkt_ok(X.T @ X, X.T @ y, lasso_quoted, 0.8)
    vec("lasso, lambda = 0.8, coordinate descent", lasso_cd(X.T @ X, X.T @ y, 0.8), tuple(lasso_quoted), 10)
    print("    KKT conditions hold at the quoted lasso solution")
    lam_max = float(np.max(np.abs(X.T @ y)))
    approx("lambda_max = max |x_j'y|", lam_max, 3, 10)
    assert np.all(lasso_cd(X.T @ X, X.T @ y, lam_max * (1 + 1e-9)) == 0)
    assert np.any(lasso_cd(X.T @ X, X.T @ y, 2.999) != 0)
    print("    all coefficients are zero at lambda = lambda_max (1 + 1e-9) and not at lambda = 2.999")


def collinear_example() -> None:
    print("Example 2 and card stat-ridge-collinear-lasso-picks-one")
    xtx = 250 * np.array([[1.0, 0.95], [0.95, 1.0]])
    xty = np.array([200.0, 190.0])
    eig = np.linalg.eigvalsh(xtx)
    approx("small eigenvalue d^2 (difference direction)", eig[0], 12.5, 10)
    approx("large eigenvalue d^2 (average direction)", eig[1], 487.5, 10)
    se = np.sqrt(np.diag(np.linalg.inv(xtx)))
    approx("OLS SE of each coefficient, unit noise", se[0], 0.203, 3)
    approx("SE if uncorrelated, 1/sqrt(250)", 1 / math.sqrt(250), 0.063, 3)
    vec("OLS", np.linalg.solve(xtx, xty), (0.8, 0.0), 10)
    ridge = np.linalg.solve(xtx + 12.5 * np.eye(2), xty)
    vec("ridge, lambda = 12.5", ridge, (0.59, 0.19), 10)
    # SVD route: build an explicit X with this X'X and check the shrinkage factors and df
    L = np.linalg.cholesky(xtx)
    X = L.T  # 2 x 2 design with X'X = L L' = xtx
    d = np.linalg.svd(X, compute_uv=False)
    approx("shrink factor 487.5/500", max(d**2 / (d**2 + 12.5)), 0.975, 10)
    approx("shrink factor 12.5/25", min(d**2 / (d**2 + 12.5)), 0.5, 10)
    hat = X @ np.linalg.inv(xtx + 12.5 * np.eye(2)) @ X.T
    approx("ridge df = trace of the hat matrix", float(np.trace(hat)), 1.475, 10)
    lasso = lasso_cd(xtx, xty, 12.5)
    vec("lasso, lambda = 12.5, coordinate descent", lasso, (0.75, 0.0), 10)
    approx("KKT check for signal 2: |190 - 237.5 x 0.75|", abs(190 - 237.5 * 0.75), 11.9, 1)
    assert abs(190 - 237.5 * 0.75) <= 12.5 and kkt_ok(xtx, xty, np.array([0.75, 0.0]), 12.5)


def scalar_shrinkage(rng: np.random.Generator) -> None:
    print("Example 3, TL;DR and card stat-ridge-optimal-shrinkage-scalar")

    def mse(beta: float, s: float, lam: float) -> float:
        c = 1 / (1 + lam)
        return c * c * s * s + (1 - c) ** 2 * beta * beta

    grid = np.linspace(0, 5, 500001)
    vals = np.array([mse(0.5, 0.5, lam) for lam in grid[::100]])
    approx("argmin lambda for beta = s = 0.5 (grid)", float(grid[::100][np.argmin(vals)]), 1.0, 3)
    approx("MSE of OLS", mse(0.5, 0.5, 0.0), 0.25, 10)
    approx("MSE at lambda = 1", mse(0.5, 0.5, 1.0), 0.125, 10)
    approx("MSE at lambda = 0.5", mse(0.5, 0.5, 0.5), 0.139, 3)
    approx("MSE at lambda = 2", mse(0.5, 0.5, 2.0), 0.139, 3)
    vals1 = np.array([mse(1.0, 0.5, lam) for lam in grid[::100]])
    approx("argmin lambda for beta = 1 (grid)", float(grid[::100][np.argmin(vals1)]), 0.25, 3)
    approx("MSE at lambda = 0.25, beta = 1", mse(1.0, 0.5, 0.25), 0.20, 10)
    approx("shrink factor beta^2/(beta^2 + s^2) at t = 1", 0.25 / 0.5, 0.5, 10)
    draws = 0.5 + 0.5 * rng.standard_normal(1_000_000)
    sq = (draws / 2 - 0.5) ** 2
    simulated("simulated MSE of beta_hat/2", float(sq.mean()), 0.125, 4 * float(sq.std()) / 1000)


def prior_to_penalty() -> None:
    print("Example 4 and card stat-ridge-prior-to-penalty")
    sigma2, tau2, n = 1.0, 0.01, 400
    lam = sigma2 / tau2
    approx("ridge lambda = sigma^2/tau^2", lam, 100, 10)
    approx("shrink factor n/(n + lambda)", n / (n + lam), 0.8, 10)
    b = math.sqrt(tau2 / 2)
    x = np.linspace(-2, 2, 400001)
    dens = np.exp(-np.abs(x) / b) / (2 * b)
    var = float(np.sum(x * x * dens) * (x[1] - x[0]))
    approx("Laplace variance by quadrature equals 0.01 at b = 0.0707", var, 0.01, 6)
    approx("b", b, 0.0707, 4)
    lam_l = sigma2 / b
    approx("lasso lambda = sigma^2/b", lam_l, 14.1, 1)
    thr = lam_l / n
    approx("soft threshold on beta_OLS, lambda/n", thr, 0.035, 3)
    approx("soft threshold (four decimals)", thr, 0.0354, 4)
    # one-regressor lasso solved by coordinate descent: zero exactly when |beta_OLS| <= lambda/n
    for b_ols, expect_zero in ((0.0353, True), (0.0355, False)):
        sol = lasso_cd(np.array([[float(n)]]), np.array([n * b_ols]), lam_l)
        assert (sol[0] == 0.0) == expect_zero, (b_ols, sol)
    print("    one-regressor lasso is zero at beta_OLS = 0.0353 and non-zero at 0.0355")
    approx("t-stat threshold, 0.0354 x sqrt(400)", thr * math.sqrt(n), 0.71, 2)


def hoerl_kennard(rng: np.random.Generator) -> None:
    print("Hoerl and Kennard (1970): some lambda > 0 beats OLS on total MSE (card stat-ridge-hoerl-kennard)")
    for trial in range(200):
        X = rng.standard_normal((30, 5)) @ np.diag(rng.uniform(0.1, 3, 5))
        beta = rng.standard_normal(5) * rng.uniform(0.1, 10)
        _, d, Vt = np.linalg.svd(X, full_matrices=False)
        a = Vt @ beta

        def total_mse(lam: float, d=d, a=a) -> float:
            return float(np.sum(d**2 / (d**2 + lam) ** 2) + lam**2 * np.sum(a**2 / (d**2 + lam) ** 2))

        lam_small = 1e-4 * float(np.min(d**2)) / (1 + float(np.max(a**2)))
        assert total_mse(lam_small) < total_mse(0.0), trial
    print("    200 random designs and coefficients: MSE(small lambda) < MSE(0) every time (sigma = 1)")


def main() -> None:
    rng = np.random.default_rng(SEED)
    orthonormal_example(rng)
    collinear_example()
    scalar_shrinkage(rng)
    prior_to_penalty()
    hoerl_kennard(rng)
    print("all regularization checks passed")


if __name__ == "__main__":
    main()
