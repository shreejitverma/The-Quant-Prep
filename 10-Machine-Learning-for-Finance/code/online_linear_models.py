"""Online learning for linear models: recursive least squares, forgetting factors, LMS/SGD and sharded fits.

Backs 10-Machine-Learning-for-Finance/04-Online-Learning-and-Linear-Models-at-Scale.md.

1. Scalar RLS by hand: three observations, each step equals the batch ridge fit.
2. Multivariate RLS: equals batch ridge (lambda = 1) and exponentially weighted ridge (lambda < 1).
3. Forgetting factor arithmetic: memory 1/(1 - lambda), half-life, effective sample size (1 + lambda)/(1 - lambda).
4. LMS / SGD on squared loss: mean bound 2/lambda_max, the tighter mean-square bound for Gaussian inputs
   (Feuer and Weinstein 1985's closed-form condition, and the spectral radius of the second-moment recursion,
   whose one-step map is itself checked by Monte Carlo), per-mode contraction, the cost of an ill-conditioned
   design, and steady-state excess error against the small-step formula eta*sigma^2*tr(R)/2 and the exact one.
5. Tracking a random-walk beta: grid of forgetting factors and rolling windows against the Kalman filter,
   the steady-state Kalman gain that predicts the best forgetting factor, and a one-change control.
6. Sharded sufficient statistics: summing X'X and X'y over shards reproduces the full ridge fit.
7. Feature hashing: probability that a feature shares its bucket.

Run: uv run --no-project --with numpy python 10-Machine-Learning-for-Finance/code/online_linear_models.py
"""

from __future__ import annotations

import math

import numpy as np


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> float:
    """Print a result and assert it matches the literal the note quotes, to tolerance and to printed rounding."""
    printed = f"{value:{fmt}}"
    print(f"{label} = {printed}")
    quoted = f"{expected:{fmt}}"
    assert abs(value - expected) <= tol + 1e-12, f"{label}: got {value}, expected {expected} +/- {tol}"
    assert printed.lstrip("-") == quoted.lstrip("-") or printed == quoted, f"{label}: prints {printed}, note quotes {quoted}"
    return value


def check_below(label: str, value: float, bound: float) -> None:
    """Assert an error-type quantity is below the bound the note quotes."""
    print(f"{label} = {value:.2e}")
    print(f"{label} bound = {bound:g}")
    assert value < bound, f"{label}: {value} is not below {bound}"


# ---------------------------------------------------------------------------
# RLS
# ---------------------------------------------------------------------------


def rls(x: np.ndarray, y: np.ndarray, lam: float, delta: float) -> tuple[np.ndarray, np.ndarray]:
    """Recursive least squares with forgetting factor lam and prior P_0 = I/delta; returns the path of w and final P."""
    n, p = x.shape
    w = np.zeros(p)
    pm = np.eye(p) / delta
    path = np.empty((n, p))
    for t in range(n):
        xt = x[t]
        px = pm @ xt
        k = px / (lam + xt @ px)
        w = w + k * (y[t] - xt @ w)
        pm = (pm - np.outer(k, px)) / lam
        pm = 0.5 * (pm + pm.T)  # keep P symmetric against rounding
        path[t] = w
    return path, pm


def weighted_ridge(x: np.ndarray, y: np.ndarray, lam: float, delta: float) -> np.ndarray:
    """argmin sum_s lam^(n-1-s) (y_s - x_s w)^2 + lam^n delta |w|^2, the objective RLS minimises."""
    n, p = x.shape
    wts = lam ** np.arange(n - 1, -1, -1)
    a = (x * wts[:, None]).T @ x + lam**n * delta * np.eye(p)
    return np.linalg.solve(a, (x * wts[:, None]).T @ y)


def section_scalar_rls() -> None:
    # Backs: Worked example 1; cards ml-online-rls-by-hand, ml-online-rls-equals-ridge.
    print("\n== 1. Scalar RLS by hand ==")
    x = np.array([[1.0], [2.0], [1.0]])
    y = np.array([2.0, 3.0, 1.0])
    path, pm = rls(x, y, lam=1.0, delta=1.0)
    # Batch ridge after each step: w_t = sum x y / (1 + sum x^2).
    for t in range(3):
        batch = float((x[: t + 1, 0] @ y[: t + 1]) / (1.0 + x[: t + 1, 0] @ x[: t + 1, 0]))
        assert abs(path[t, 0] - batch) < 1e-14
    check("rls scalar w1", path[0, 0], 1.0000, 1e-12)
    check("rls scalar w2", path[1, 0], 1.3333, 1e-4)
    check("rls scalar w3", path[2, 0], 1.2857, 1e-4)
    check("rls scalar w3 times 7", 7 * path[2, 0], 9.0000, 1e-12)
    check("rls scalar final P times 7", 7 * pm[0, 0], 1.0000, 1e-12)


def section_rls_equals_ridge() -> None:
    # Backs: Worked example 1 (8-feature check); cards ml-online-rls-update, ml-online-rls-equals-ridge.
    print("\n== 2. RLS equals (weighted) ridge ==")
    rng = np.random.default_rng(7)
    n, p = 500, 8
    x = rng.standard_normal((n, p))
    beta = rng.standard_normal(p)
    y = x @ beta + rng.standard_normal(n)
    for lam, label in [(1.0, "rls vs ridge max abs diff, lambda 1"), (0.98, "rls vs weighted ridge max abs diff, lambda 0.98")]:
        path, _ = rls(x, y, lam=lam, delta=10.0)
        err = max(float(np.max(np.abs(path[t] - weighted_ridge(x[: t + 1], y[: t + 1], lam, 10.0)))) for t in range(9, n, 7))
        check_below(label, err, 1e-10)


# ---------------------------------------------------------------------------
# Forgetting factor arithmetic
# ---------------------------------------------------------------------------


def section_forgetting() -> None:
    # Backs: Core concepts, forgetting factors table; cards ml-online-forgetting-memory, ml-online-window-vs-ew.
    print("\n== 3. Forgetting factor arithmetic ==")
    for lam, tag, exp_mem, exp_hl, exp_ess in [(0.99, "0.99", 100.0, 68.97, 199.0), (0.995, "0.995", 200.0, 138.28, 399.0)]:
        w = lam ** np.arange(200_000)
        check(f"memory 1/(1-lambda), lambda {tag}", float(w.sum()), exp_mem, 1e-6, ".1f")
        check(f"half-life in observations, lambda {tag}", math.log(0.5) / math.log(lam), exp_hl, 0.005, ".2f")
        check(f"effective sample size, lambda {tag}", float(w.sum() ** 2 / (w**2).sum()), exp_ess, 1e-6, ".1f")
        check(f"mean age of a weight, lambda {tag}", float((np.arange(w.size) * w).sum() / w.sum()), exp_mem - 1.0, 1e-6, ".1f")


# ---------------------------------------------------------------------------
# LMS / SGD
# ---------------------------------------------------------------------------


def lms_mean_square_ok(eta: float, eig: np.ndarray) -> bool:
    """Feuer and Weinstein (1985) eq. (30), written for the step eta = 2 mu: finite weight-error variance."""
    return bool(np.all(eta * eig < 1.0) and np.sum(eta * eig / (2.0 - 2.0 * eta * eig)) < 1.0)


def lms_second_moment_map(eta: float, eig: np.ndarray) -> np.ndarray:
    """Matrix F with diag(E[v_t v_t']) = F diag(E[v_(t-1) v_(t-1)']) (noise-free part) for independent Gaussian inputs.

    Built from the Gaussian fourth-moment identity E[x x' M x x'] = 2 R M R + tr(R M) R (M diagonal),
    not from the closed-form condition above.
    """
    return np.diag(1.0 - 2.0 * eta * eig + 2.0 * eta**2 * eig**2) + eta**2 * np.outer(eig, eig)


def lms_second_moment_radius(eta: float, eig: np.ndarray) -> float:
    """Spectral radius of the second-moment map; above 1 means the weight-error variance is unbounded."""
    return float(np.max(np.abs(np.linalg.eigvals(lms_second_moment_map(eta, eig)))))


def lms_second_moment_map_mc(eta: float, eig: np.ndarray, n: int, seed: int) -> np.ndarray:
    """Monte Carlo of the same map: column j is diag E[(I - eta x x') e_j e_j' (I - eta x x')] over Gaussian x."""
    rng = np.random.default_rng(seed)
    x = rng.standard_normal((n, eig.size)) * np.sqrt(eig)
    cols = []
    for j in range(eig.size):
        # (I - eta x x') e_j = e_j - eta x_j x; its squared entries are the diagonal of the outer product.
        v = -eta * x[:, j : j + 1] * x
        v[:, j] += 1.0
        cols.append((v**2).mean(axis=0))
    return np.column_stack(cols)


def bisect_bound(stable, hi: float) -> float:
    lo = 0.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if stable(mid) else (lo, mid)
    return lo


def steps_to_shrink(contraction: np.ndarray, factor: float = 1e-3) -> int:
    """Iterate the mean error E[w_t - w*] = (I - eta R)^t (w_0 - w*) from (1, 1) until every mode is below factor."""
    err = np.ones(contraction.size)
    t = 0
    while np.max(np.abs(err)) > factor:
        err = contraction * err
        t += 1
    return t


def section_lms() -> None:
    # Backs: Core concepts (LMS) and Worked examples 3 and 4;
    # cards ml-online-lms-stability, ml-online-conditioning, ml-online-misadjustment.
    print("\n== 4. LMS / SGD on squared loss ==")
    # Ill-conditioned design: independent Gaussian features with variances 1 and 100.
    eig = np.array([1.0, 100.0])
    check("LMS mean-stability bound 2/lambda_max", 2.0 / eig.max(), 0.0200, 1e-12)
    ms_bound = bisect_bound(lambda e: lms_mean_square_ok(e, eig), 1.0 / eig.max())
    ms_bound_radius = bisect_bound(lambda e: lms_second_moment_radius(e, eig) < 1.0, 1.0 / eig.max())
    check("LMS mean-square bound, variances 1 and 100 (Feuer-Weinstein condition)", ms_bound, 0.00666, 5e-6, ".5f")
    check("LMS mean-square bound, same, from the second-moment recursion", ms_bound_radius, 0.00666, 5e-6, ".5f")
    check("conservative mean-square bound 2/(3 tr R)", 2.0 / (3.0 * eig.sum()), 0.0066, 5e-5)
    check("second-moment growth factor at eta 0.01 (above 1 = unbounded variance)", lms_second_moment_radius(0.01, eig), 2.00, 5e-3, ".2f")
    # Independent leg: the fourth-moment identity behind the map, checked by sampling x (seed 17, 2 million draws).
    f_exact = lms_second_moment_map(0.01, eig)
    f_mc = lms_second_moment_map_mc(0.01, eig, 2_000_000, 17)
    check_below("max relative error, second-moment map formula vs Monte Carlo, eta 0.01", float(np.max(np.abs(f_mc / f_exact - 1))), 0.02)
    eta = 0.005
    check("fast-mode contraction per step at eta 0.005", 1.0 - eta * eig.max(), 0.5, 1e-12, ".1f")
    check("slow-mode contraction per step at eta 0.005", 1.0 - eta * eig.min(), 0.995, 1e-12, ".3f")
    check("steps to cut slow-mode error 1000x, closed form", math.log(1e-3) / math.log(1.0 - eta), 1378.1, 0.05, ".1f")
    check("mean-error iteration count, ill-conditioned, eta 0.005", steps_to_shrink(1.0 - eta * eig), 1379, 0, ".0f")
    # Standardised: both variances 1; mean-square bound 2/(p + 2) = 0.5 for p = 2; take half of it.
    std = np.ones(2)
    check("LMS mean-square bound after standardising, p 2", bisect_bound(lambda e: lms_mean_square_ok(e, std), 1.0), 0.5, 1e-9, ".2f")
    check("mean-error iteration count after standardising, eta 0.25", steps_to_shrink(1.0 - 0.25 * std), 25, 0, ".0f")

    # Steady-state excess MSE of LMS against the small-step formula and the exact Gaussian-data result.
    rng = np.random.default_rng(11)
    p, n, eta, sigma = 5, 400_000, 0.01, 1.0
    w_true = rng.standard_normal(p)
    x = rng.standard_normal((n, p))
    noise = sigma * rng.standard_normal(n)
    w = np.zeros(p)
    dev = np.empty(n)
    for t in range(n):
        xt = x[t]
        e = (w_true - w) @ xt + noise[t]
        w = w + eta * e * xt
        dev[t] = (w - w_true) @ (w - w_true)  # excess MSE = (w - w*)' R (w - w*) with R = I
    excess = float(dev[n // 4 :].mean())
    check("LMS excess MSE, small-step theory eta*sigma^2*tr(R)/2", eta * sigma**2 * p / 2, 0.025, 1e-12, ".3f")
    s_fw = float(np.sum(eta * np.ones(p) / (2.0 - 2.0 * eta * np.ones(p))))
    check("LMS excess MSE, exact for Gaussian data sigma^2 S/(1 - S)", sigma**2 * s_fw / (1.0 - s_fw), 0.0259, 5e-5, ".4f")
    check("LMS excess MSE, simulated", excess, 0.0259, 5e-5, ".4f")


# ---------------------------------------------------------------------------
# Tracking a drifting beta
# ---------------------------------------------------------------------------


def kalman_rw_beta(x: np.ndarray, y: np.ndarray, q: float, r: float) -> np.ndarray:
    """Filtered beta_t for y_t = beta_t x_t + eps, beta_t a random walk (scalar Kalman filter)."""
    b, pv = 0.0, 1.0
    out = np.empty(x.size)
    for t in range(x.size):
        pv += q
        f = x[t] * pv * x[t] + r
        k = pv * x[t] / f
        b += k * (y[t] - x[t] * b)
        pv -= k * x[t] * pv
        out[t] = b
    return out


def rls_scalar_path(x: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    num, den = 0.0, 1e-6
    out = np.empty(x.size)
    for t in range(x.size):
        num = lam * num + x[t] * y[t]
        den = lam * den + x[t] * x[t]
        out[t] = num / den
    return out


def rolling_path(x: np.ndarray, y: np.ndarray, window: int) -> np.ndarray:
    cxy = np.concatenate([[0.0], np.cumsum(x * y)])
    cxx = np.concatenate([[0.0], np.cumsum(x * x)])
    idx = np.arange(1, x.size + 1)
    lo = np.maximum(0, idx - window)
    return (cxy[idx] - cxy[lo]) / (cxx[idx] - cxx[lo])


def section_tracking() -> None:
    # Backs: Worked example 2; cards ml-online-optimal-lambda, ml-online-rls-vs-kalman,
    # ml-online-expanding-ols-drift, ml-online-window-vs-ew.
    print("\n== 5. Tracking a random-walk beta ==")
    q, r = 1e-4, 1.0
    # Steady-state Kalman gain for a local level with unit regressor: prior variance P solves P^2 - qP - qr = 0.
    p_prior = (q + math.sqrt(q * q + 4 * q * r)) / 2
    gain = p_prior / (p_prior + r)
    check("steady-state Kalman gain, q 1e-4, r 1", gain, 0.00995, 5e-6, ".5f")
    check("implied forgetting factor 1 - K", 1 - gain, 0.990, 5e-4, ".3f")
    grid = np.linspace(0.9, 0.9999, 99_000)
    approx_mse = r * (1 - grid) / (1 + grid) + q * grid**2 / (1 - grid**2)
    check("forgetting factor minimising the local-level approximation", float(grid[np.argmin(approx_mse)]), 0.990, 5e-4, ".3f")

    rng = np.random.default_rng(2024)
    n, burn = 60_000, 2_000
    beta = 1.0 + np.cumsum(math.sqrt(q) * rng.standard_normal(n))
    x = rng.standard_normal(n)
    eps = math.sqrt(r) * rng.standard_normal(n)
    y = beta * x + eps

    def mse(est: np.ndarray) -> float:
        return float(np.mean((est[burn:] - beta[burn:]) ** 2))

    kal = mse(kalman_rw_beta(x, y, q, r))
    check("tracking MSE x 1e3, Kalman filter (true q)", 1e3 * kal, 10.46, 0.005, ".2f")
    check("Kalman steady-state posterior variance x 1e3 (local level)", 1e3 * p_prior * (1 - gain), 9.95, 0.005, ".2f")
    # Independent route: iterate the Riccati recursion, then evaluate the EW error formula at lambda = 1 - K.
    pp = 1.0
    for _ in range(20_000):
        pp = pp * r / (pp + r) + q
    k_iter = pp / (pp + r)
    lam_k = 1.0 - k_iter
    ew_at_k = r * (1 - lam_k) / (1 + lam_k) + q * lam_k**2 / (1 - lam_k**2)
    check_below("|EW formula at lambda = 1 - K minus Kalman posterior variance|", abs(ew_at_k - pp * (1 - k_iter)), 1e-12)
    # Local-level approximation of the EW estimator: noise r(1-lam)/(1+lam) plus lag q lam^2/(1-lam^2).
    expected = {0.95: (27.74, 26.57), 0.98: (13.00, 12.53), 0.99: (10.49, 9.95), 0.995: (13.20, 12.43), 0.999: (49.31, 50.43)}
    results = {}
    for lam, (exp_sim, exp_approx) in expected.items():
        results[lam] = mse(rls_scalar_path(x, y, lam))
        approx = r * (1 - lam) / (1 + lam) + q * lam**2 / (1 - lam**2)
        check(f"tracking MSE x 1e3, RLS lambda {lam}", 1e3 * results[lam], exp_sim, 0.005, ".2f")
        check(f"tracking MSE x 1e3, local-level approximation, lambda {lam}", 1e3 * approx, exp_approx, 0.005, ".2f")
    results[1.0] = mse(rls_scalar_path(x, y, 1.0))
    check("tracking MSE x 1e3, RLS lambda 1.0 (expanding OLS)", 1e3 * results[1.0], 421.07, 0.005, ".2f")
    best = min(results, key=results.get)
    check("best forgetting factor on the grid", best, 0.990, 1e-12, ".3f")
    for window, exp in [(100, 13.91), (200, 12.47), (400, 17.17)]:
        check(f"tracking MSE x 1e3, rolling window {window}", 1e3 * mse(rolling_path(x, y, window)), exp, 0.005, ".2f")
    check("RLS 0.99 excess over Kalman (%)", 100 * (results[0.99] / kal - 1), 0.3, 0.05, ".1f")
    check("expanding OLS MSE / RLS 0.99 MSE", results[1.0] / results[0.99], 40.1, 0.05, ".1f")
    gaps = [results[lam] / (r * (1 - lam) / (1 + lam) + q * lam**2 / (1 - lam**2)) - 1 for lam in expected]
    check("largest |simulated / formula - 1| over the grid (%)", 100 * max(abs(g) for g in gaps), 6.2, 0.05, ".1f")
    # Control: one change only, the regressor becomes the constant x = 1 (the local-level model the formula
    # assumes); the beta path and the noise draws are reused.
    y_level = beta + eps
    ones = np.ones(n)
    level = mse(rls_scalar_path(ones, y_level, 0.99))
    check("tracking MSE x 1e3, RLS lambda 0.99, constant regressor (control)", 1e3 * level, 9.99, 0.005, ".2f")
    level_formula = r * 0.01 / 1.99 + q * 0.99**2 / (1 - 0.99**2)
    check("control |simulated / formula - 1| (%)", 100 * abs(level / level_formula - 1), 0.4, 0.05, ".1f")


# ---------------------------------------------------------------------------
# Scale
# ---------------------------------------------------------------------------


def section_sharded() -> None:
    # Backs: Worked example 6; card ml-online-sufficient-stats.
    print("\n== 6. Sharded sufficient statistics ==")
    rng = np.random.default_rng(3)
    n, p = 40_000, 20
    x = rng.standard_normal((n, p))
    y = x @ rng.standard_normal(p) + rng.standard_normal(n)
    xtx = np.zeros((p, p))
    xty = np.zeros(p)
    for shard in np.array_split(np.arange(n), 4):
        xtx += x[shard].T @ x[shard]
        xty += x[shard].T @ y[shard]
    w_shard = np.linalg.solve(xtx + 5.0 * np.eye(p), xty)
    w_full = np.linalg.solve(x.T @ x + 5.0 * np.eye(p), x.T @ y)
    check_below("sharded vs full ridge max abs diff", float(np.max(np.abs(w_shard - w_full))), 1e-10)


def section_hashing() -> None:
    # Backs: Worked example 5; card ml-online-hashing.
    print("\n== 7. Feature hashing ==")
    m, n = 2**20, 100_000
    check("P(feature shares its bucket), 1e5 features in 2^20 buckets", 1 - (1 - 1 / m) ** (n - 1), 0.0910, 5e-5)
    # Simulated: hash n distinct features uniformly into m buckets.
    rng = np.random.default_rng(5)
    buckets = rng.integers(0, m, size=n)
    counts = np.bincount(buckets, minlength=m)
    check("simulated fraction of features in a shared bucket", float((counts[buckets] > 1).mean()), 0.0905, 5e-5)


if __name__ == "__main__":
    section_scalar_rls()
    section_rls_equals_ridge()
    section_forgetting()
    section_lms()
    section_tracking()
    section_sharded()
    section_hashing()
    print("\nall checks passed")
