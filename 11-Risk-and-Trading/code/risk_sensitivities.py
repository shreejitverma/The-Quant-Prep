"""Sensitivities and Portfolio Revaluation Engine.

Pure Python 3.10+ standard library implementation:
1. Optimal finite difference step sizes balancing truncation and cancellation error.
2. Central difference bump engine for first-order (Delta) and second-order (Gamma, Cross-Gamma) Greeks.
3. Parametric correlated scenario generation via Cholesky decomposition.
4. Full Revaluation versus Delta-Gamma Taylor proxy comparison.
5. Distribution tail diagnostics: MAE, RMSE, Max Error, 99% VaR, and 99% Expected Shortfall.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable, Sequence

SQRT_TWO = math.sqrt(2.0)
EPS_MACH = 2.220446049250313e-16


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / SQRT_TWO))


def black_scholes_call(factors: Sequence[float], k: float = 100.0, t: float = 1.0) -> float:
    """Black-Scholes European call price for factors [S, r, sigma]."""
    s, r, sigma = factors[0], factors[1], factors[2]
    if s <= 0.0 or sigma <= 0.0 or t <= 0.0:
        return max(0.0, s - k * math.exp(-r * t))
    vol_sqrt_t = sigma * math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * t) / vol_sqrt_t
    d2 = d1 - vol_sqrt_t
    return s * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d2)


def compute_optimal_bump_sizes(spot: float) -> tuple[float, float]:
    """Calculate theoretically optimal central difference bump sizes for delta and gamma."""
    h_delta = (EPS_MACH ** (1.0 / 3.0)) * spot
    h_gamma = (EPS_MACH ** (1.0 / 4.0)) * spot
    return h_delta, h_gamma


def compute_gradient(
    pricing_fn: Callable[[Sequence[float]], float],
    base_factors: Sequence[float],
    bump_sizes: Sequence[float],
) -> list[float]:
    """Compute central difference gradient (Delta vector)."""
    n = len(base_factors)
    grad = [0.0] * n
    factors_up = list(base_factors)
    factors_dn = list(base_factors)

    for i in range(n):
        h = bump_sizes[i]
        orig = base_factors[i]

        factors_up[i] = orig + h
        v_up = pricing_fn(factors_up)

        factors_dn[i] = orig - h
        v_dn = pricing_fn(factors_dn)

        grad[i] = (v_up - v_dn) / (2.0 * h)

        factors_up[i] = orig
        factors_dn[i] = orig

    return grad


def compute_hessian(
    pricing_fn: Callable[[Sequence[float]], float],
    base_factors: Sequence[float],
    bump_sizes: Sequence[float],
) -> list[list[float]]:
    """Compute central difference Hessian matrix (Gamma and Cross-Gamma)."""
    n = len(base_factors)
    hessian = [[0.0] * n for _ in range(n)]
    v_base = pricing_fn(base_factors)

    factors_work = list(base_factors)
    for i in range(n):
        h = bump_sizes[i]
        orig = base_factors[i]

        factors_work[i] = orig + h
        v_up = pricing_fn(factors_work)

        factors_work[i] = orig - h
        v_dn = pricing_fn(factors_work)

        hessian[i][i] = (v_up - 2.0 * v_base + v_dn) / (h * h)
        factors_work[i] = orig

    for i in range(n):
        for j in range(i + 1, n):
            hi = bump_sizes[i]
            hj = bump_sizes[j]
            xi = base_factors[i]
            xj = base_factors[j]

            factors_work[i] = xi + hi
            factors_work[j] = xj + hj
            v_pp = pricing_fn(factors_work)

            factors_work[i] = xi + hi
            factors_work[j] = xj - hj
            v_pm = pricing_fn(factors_work)

            factors_work[i] = xi - hi
            factors_work[j] = xj + hj
            v_mp = pricing_fn(factors_work)

            factors_work[i] = xi - hi
            factors_work[j] = xj - hj
            v_mm = pricing_fn(factors_work)

            cross = (v_pp - v_pm - v_mp + v_mm) / (4.0 * hi * hj)
            hessian[i][j] = cross
            hessian[j][i] = cross

            factors_work[i] = xi
            factors_work[j] = xj

    return hessian


def cholesky_decomposition(matrix: Sequence[Sequence[float]]) -> list[list[float]]:
    """Compute Cholesky lower triangular matrix L where A = L L^T."""
    n = len(matrix)
    l_mat = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(l_mat[i][k] * l_mat[j][k] for k in range(j))
            if i == j:
                val = matrix[i][i] - s
                if val <= 0.0:
                    raise ValueError(f"Matrix not positive definite at ({i}, {i})")
                l_mat[i][j] = math.sqrt(val)
            else:
                l_mat[i][j] = (matrix[i][j] - s) / l_mat[j][j]
    return l_mat


def generate_correlated_scenarios(
    cov: Sequence[Sequence[float]],
    num_scenarios: int = 2000,
    seed: int = 123,
) -> list[list[float]]:
    """Generate correlated multivariate normal scenarios using Box-Muller."""
    rng = random.Random(seed)
    lower = cholesky_decomposition(cov)
    n = len(cov)
    scenarios: list[list[float]] = []

    for _ in range(num_scenarios):
        z = [0.0] * n
        for i in range(0, n, 2):
            u1 = rng.random()
            u2 = rng.random()
            while u1 <= 1e-12:
                u1 = rng.random()
            mag = math.sqrt(-2.0 * math.log(u1))
            z0 = mag * math.cos(2.0 * math.pi * u2)
            z[i] = z0
            if i + 1 < n:
                z1 = mag * math.sin(2.0 * math.pi * u2)
                z[i + 1] = z1

        # Correlated shock: dx = L * z
        dx = [0.0] * n
        for i in range(n):
            val = 0.0
            for k in range(i + 1):
                val += lower[i][k] * z[k]
            dx[i] = val
        scenarios.append(dx)

    return scenarios


def evaluate_taylor_pnl(
    gradient: Sequence[float],
    hessian: Sequence[Sequence[float]],
    shock: Sequence[float],
) -> float:
    """Evaluate second-order Taylor expansion P&L: delta * dx + 0.5 * dx^T Gamma dx."""
    n = len(shock)
    pnl = sum(gradient[i] * shock[i] for i in range(n))
    quad = 0.0
    for i in range(n):
        for j in range(n):
            quad += hessian[i][j] * shock[i] * shock[j]
    pnl += 0.5 * quad
    return pnl


def calculate_var_and_es(
    losses: Sequence[float],
    confidence_level: float = 0.99,
) -> tuple[float, float]:
    """Calculate empirical VaR and Expected Shortfall from loss vector."""
    if not losses:
        return 0.0, 0.0

    sorted_losses = sorted(losses)
    n = len(sorted_losses)
    idx = int(math.floor(confidence_level * n))
    idx = min(idx, n - 1)

    var_val = sorted_losses[idx]
    tail_losses = sorted_losses[idx:]
    es_val = sum(tail_losses) / len(tail_losses) if tail_losses else var_val
    return var_val, es_val


def run_sensitivities_verification() -> None:
    """Assert all figures quoted in Note 12."""
    s0 = 100.0
    h_opt_delta, h_opt_gamma = compute_optimal_bump_sizes(s0)

    # Note 12 Step 1 and Step 2 optimal bump sizes
    assert abs(h_opt_delta - 0.000605553) < 1e-6, f"Optimal delta bump mismatch: {h_opt_delta}"
    assert abs(h_opt_gamma - 0.0122074) < 1e-6, f"Optimal gamma bump mismatch: {h_opt_gamma}"

    base = [100.0, 0.05, 0.20]
    bumps = [0.01, 0.0001, 0.0001]
    v0 = black_scholes_call(base)
    assert abs(v0 - 10.45058) < 1e-4, f"Base call value mismatch: {v0}"

    grad = compute_gradient(black_scholes_call, base, bumps)
    hessian = compute_hessian(black_scholes_call, base, bumps)

    # Note 12 base Greeks
    assert abs(grad[0] - 0.6368) < 1e-3, f"Delta mismatch: {grad[0]}"
    assert abs(hessian[0][0] - 0.0188) < 1e-3, f"Gamma mismatch: {hessian[0][0]}"
    assert abs(grad[2] - 37.52) < 0.1, f"Vega mismatch: {grad[2]}"

    # Vertex of quadratic delta-gamma proxy: -delta / gamma
    vertex = -grad[0] / hessian[0][0]
    assert abs(vertex - (-33.94)) < 0.2, f"Quadratic vertex mismatch: {vertex}"

    # Covariance for 3 factors: [S, r, sigma]
    # S_sd = 5.0, r_sd = 0.0025, vol_sd = 0.02
    # corr(S, r) = +0.20, corr(S, vol) = -0.50, corr(r, vol) = 0.0
    cov = [
        [25.0, 0.0025, -0.05],
        [0.0025, 0.00000625, 0.0],
        [-0.05, 0.0, 0.0004],
    ]

    scenarios = generate_correlated_scenarios(cov, num_scenarios=2000, seed=123)
    assert len(scenarios) == 2000

    full_pnls: list[float] = []
    proxy_pnls: list[float] = []
    abs_errors: list[float] = []
    sq_errors: list[float] = []

    for sc in scenarios:
        shocked_factors = [base[i] + sc[i] for i in range(3)]
        full_pnl = black_scholes_call(shocked_factors) - v0
        proxy_pnl = evaluate_taylor_pnl(grad, hessian, sc)
        err = abs(full_pnl - proxy_pnl)

        full_pnls.append(full_pnl)
        proxy_pnls.append(proxy_pnl)
        abs_errors.append(err)
        sq_errors.append(err * err)

    mae = sum(abs_errors) / len(abs_errors)
    rmse = math.sqrt(sum(sq_errors) / len(sq_errors))
    max_err = max(abs_errors)

    full_losses = [-p for p in full_pnls]
    proxy_losses = [-p for p in proxy_pnls]
    full_var, full_es = calculate_var_and_es(full_losses, 0.99)
    proxy_var, proxy_es = calculate_var_and_es(proxy_losses, 0.99)

    # Assert Note 12 Example 2 diagnostics
    assert abs(mae - 0.0197) < 0.001, f"MAE mismatch: {mae}"
    assert abs(rmse - 0.0442) < 0.001, f"RMSE mismatch: {rmse}"
    assert abs(max_err - 0.7452) < 0.001, f"Max error mismatch: {max_err}"
    assert abs(full_var - 5.38) < 0.02, f"Full 99% VaR mismatch: {full_var}"
    assert abs(proxy_var - 5.32) < 0.02, f"Proxy 99% VaR mismatch: {proxy_var}"
    assert abs(full_es - 5.88) < 0.02, f"Full 99% ES mismatch: {full_es}"
    assert abs(proxy_es - 5.91) < 0.02, f"Proxy 99% ES mismatch: {proxy_es}"

    print(f"Optimal bump delta: {h_opt_delta:.6f}, gamma: {h_opt_gamma:.4f}")
    print(f"Base call value V0: {v0:.4f}, Delta: {grad[0]:.4f}, Gamma: {hessian[0][0]:.4f}")
    print(f"MAE: {mae:.4f}, RMSE: {rmse:.4f}, Max Error: {max_err:.4f}")
    print(f"Full 99% VaR: {full_var:.2f}, Proxy 99% VaR: {proxy_var:.2f}")
    print(f"Full 99% ES: {full_es:.2f}, Proxy 99% ES: {proxy_es:.2f}")
    print("All sensitivity and revaluation tests passed successfully!")


if __name__ == "__main__":
    run_sensitivities_verification()
