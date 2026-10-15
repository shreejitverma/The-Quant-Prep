"""Risk Factor Modelling, Scenario Generation, and Sensitivity Analytics.

Pure Python 3.10+ standard library implementation:
1. Finite difference bump engine for Greeks: Delta, Gamma, and Cross-Gamma.
2. Taylor series valuation proxies (Linear, Delta-Gamma, Cross-Gamma).
3. Historical scenario generation and volatility-scaled filtered simulation.
4. Parametric Monte Carlo scenario generation via Cholesky factorization.
5. Macroeconomic stress scenario generation (Parallel, Steepener, Historical Crises).
6. Portfolio revaluation comparison: Full Revaluation vs Delta-Gamma proxy,
   computing VaR, Expected Shortfall, and Taylor approximation error metrics.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass

SQRT_TWO = math.sqrt(2.0)
SQRT_TWO_PI = math.sqrt(2.0 * math.pi)


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / SQRT_TWO))


def norm_inv(p: float) -> float:
    """Acklam's approximation for inverse standard normal CDF."""
    if p <= 0.0 or p >= 1.0:
        raise ValueError("Probability must be strictly between 0 and 1.")

    a = [
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    ]
    b = [
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464968e00,
        2.938163982698783e00,
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e00,
        3.754408661907416e00,
    ]

    q_low = 0.02425
    q_high = 1.0 - q_low

    if q_low <= p <= q_high:
        q = p - 0.5
        r = q * q
        return (
            (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5])
            * q
            / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0)
        )
    elif p < q_low:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0
        )
    else:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0
        )


# ============================================================================
# 1. Finite Difference Bump Engine
# ============================================================================


def compute_gradient(
    pricing_fn: Callable[[Sequence[float]], float],
    base_factors: Sequence[float],
    bump_sizes: Sequence[float],
) -> list[float]:
    """Compute first-order sensitivities (Delta / gradient) via central difference."""
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
    """Compute second-order sensitivities (Gamma / Hessian) including cross terms."""
    n = len(base_factors)
    hessian = [[0.0] * n for _ in range(n)]
    v_base = pricing_fn(base_factors)

    # Diagonal terms: (V(x+h) - 2V(x) + V(x-h)) / h^2
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

    # Off-diagonal cross terms:
    # (V(++ ) - V(+- ) - V(-+ ) + V(-- )) / (4 * h_i * h_j)
    for i in range(n):
        for j in range(i + 1, n):
            hi = bump_sizes[i]
            hj = bump_sizes[j]
            xi = base_factors[i]
            xj = base_factors[j]

            # (+, +)
            factors_work[i] = xi + hi
            factors_work[j] = xj + hj
            v_pp = pricing_fn(factors_work)

            # (+, -)
            factors_work[j] = xj - hj
            v_pm = pricing_fn(factors_work)

            # (-, +)
            factors_work[i] = xi - hi
            factors_work[j] = xj + hj
            v_mp = pricing_fn(factors_work)

            # (-, -)
            factors_work[j] = xj - hj
            v_mm = pricing_fn(factors_work)

            cross_gamma = (v_pp - v_pm - v_mp + v_mm) / (4.0 * hi * hj)
            hessian[i][j] = cross_gamma
            hessian[j][i] = cross_gamma

            factors_work[i] = xi
            factors_work[j] = xj

    return hessian


# ============================================================================
# 2. Taylor Series Valuation Proxies
# ============================================================================


def evaluate_taylor_pnl(
    delta: Sequence[float],
    gamma: Sequence[Sequence[float]] | None,
    delta_x: Sequence[float],
) -> float:
    """Evaluate estimated P&L using Taylor expansion: delta^T dx + 0.5 * dx^T Gamma dx."""
    pnl = 0.0
    n = len(delta)

    # First order
    for i in range(n):
        pnl += delta[i] * delta_x[i]

    # Second order
    if gamma is not None:
        second_order = 0.0
        for i in range(n):
            for j in range(n):
                second_order += delta_x[i] * gamma[i][j] * delta_x[j]
        pnl += 0.5 * second_order

    return pnl


# ============================================================================
# 3. Covariance and Cholesky Factorization
# ============================================================================


def cholesky_decomposition(matrix: Sequence[Sequence[float]]) -> list[list[float]]:
    """Compute Lower triangular Cholesky factor L such that A = L L^T."""
    n = len(matrix)
    lower = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1):
            sum_val = 0.0
            for k in range(j):
                sum_val += lower[i][k] * lower[j][k]

            if i == j:
                diff = matrix[i][i] - sum_val
                if diff <= 0.0:
                    raise ValueError(f"Matrix is not positive definite at index {i}: value {diff}")
                lower[i][j] = math.sqrt(diff)
            else:
                lower[i][j] = (matrix[i][j] - sum_val) / lower[j][j]

    return lower


# ============================================================================
# 4. Scenario Generation: Historical & Parametric
# ============================================================================


def generate_parametric_scenarios(
    cov_matrix: Sequence[Sequence[float]],
    num_scenarios: int,
    seed: int = 42,
) -> list[list[float]]:
    """Generate correlated multivariate normal risk factor shocks using Cholesky factor."""
    rng = random.Random(seed)
    lower = cholesky_decomposition(cov_matrix)
    n = len(cov_matrix)
    scenarios: list[list[float]] = []

    for _ in range(num_scenarios):
        # Generate independent standard normals via Box-Muller
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


def filter_historical_scenarios(
    historical_returns: Sequence[Sequence[float]],
    historical_vols: Sequence[float],
    current_vol: float,
) -> list[list[float]]:
    """Volatility-scaled filtered historical simulation (Hull-White / GARCH scaling)."""
    num_scenarios = len(historical_returns)
    num_factors = len(historical_returns[0])
    filtered: list[list[float]] = []

    for t in range(num_scenarios):
        scale = current_vol / max(1e-6, historical_vols[t])
        shock = [historical_returns[t][j] * scale for j in range(num_factors)]
        filtered.append(shock)

    return filtered


# ============================================================================
# 5. Macro Stress Scenarios
# ============================================================================


@dataclass
class StressScenario:
    name: str
    description: str
    shocks: list[float]  # Shock per risk factor (absolute or relative)


def standard_rates_stress_scenarios() -> list[StressScenario]:
    """Define standard yield curve stress scenarios across 2y, 5y, 10y, 30y (in bps)."""
    return [
        StressScenario(
            name="Parallel Up +100bps",
            description="Uniform +100 bp increase across all key tenors",
            shocks=[0.0100, 0.0100, 0.0100, 0.0100],
        ),
        StressScenario(
            name="Parallel Down -100bps",
            description="Uniform -100 bp decrease across all key tenors",
            shocks=[-0.0100, -0.0100, -0.0100, -0.0100],
        ),
        StressScenario(
            name="2s10s Steepener",
            description="2y drops by 50 bps, 10y rises by 50 bps",
            shocks=[-0.0050, -0.0020, 0.0050, 0.0075],
        ),
        StressScenario(
            name="2s10s Flattener",
            description="2y jumps by 75 bps, 10y rises by 15 bps (hiking cycle)",
            shocks=[0.0075, 0.0050, 0.0015, 0.0000],
        ),
        StressScenario(
            name="Lehman 2008 Crash",
            description="Flight to quality: front rates collapse, long rates rally, credit spikes",
            shocks=[-0.0150, -0.0125, -0.0080, -0.0030],
        ),
        StressScenario(
            name="March 2020 COVID Dash for Cash",
            description="Extreme front-end rate plunge followed by intermediate liquidity freeze",
            shocks=[-0.0125, -0.0090, -0.0050, +0.0020],
        ),
    ]


# ============================================================================
# 6. Portfolio Valuation, VaR, and Error Diagnostics
# ============================================================================


def calculate_var_and_es(
    losses: Sequence[float],
    confidence_level: float = 0.99,
) -> tuple[float, float]:
    """Calculate Value at Risk (VaR) and Expected Shortfall (ES/CVaR) from loss vector."""
    if not losses:
        return 0.0, 0.0

    sorted_losses = sorted(losses)
    n = len(sorted_losses)
    idx = int(math.floor(confidence_level * n))
    idx = min(idx, n - 1)

    var = sorted_losses[idx]
    tail_losses = sorted_losses[idx:]
    es = sum(tail_losses) / len(tail_losses) if tail_losses else var

    return var, es


@dataclass
class RevaluationComparison:
    full_reval_pnl: list[float]
    proxy_pnl: list[float]
    mae: float
    rmse: float
    max_error: float
    full_var_99: float
    proxy_var_99: float
    full_es_99: float
    proxy_es_99: float


def compare_full_vs_proxy(
    pricing_fn: Callable[[Sequence[float]], float],
    base_factors: Sequence[float],
    delta: Sequence[float],
    gamma: Sequence[Sequence[float]] | None,
    scenarios: Sequence[Sequence[float]],
) -> RevaluationComparison:
    """Compare Full Revaluation vs Taylor Proxy across all scenarios."""
    v_base = pricing_fn(base_factors)
    full_pnls: list[float] = []
    proxy_pnls: list[float] = []
    errors: list[float] = []

    factors_work = list(base_factors)
    n = len(base_factors)

    for dx in scenarios:
        for i in range(n):
            factors_work[i] = base_factors[i] + dx[i]

        v_shocked = pricing_fn(factors_work)
        pnl_full = v_shocked - v_base
        pnl_proxy = evaluate_taylor_pnl(delta, gamma, dx)

        full_pnls.append(pnl_full)
        proxy_pnls.append(pnl_proxy)
        errors.append(abs(pnl_full - pnl_proxy))

    m = len(scenarios)
    mae = sum(errors) / m if m > 0 else 0.0
    rmse = math.sqrt(sum(e * e for e in errors) / m) if m > 0 else 0.0
    max_err = max(errors) if errors else 0.0

    # Losses are -PnL
    full_losses = [-p for p in full_pnls]
    proxy_losses = [-p for p in proxy_pnls]

    f_var, f_es = calculate_var_and_es(full_losses, confidence_level=0.99)
    p_var, p_es = calculate_var_and_es(proxy_losses, confidence_level=0.99)

    return RevaluationComparison(
        full_reval_pnl=full_pnls,
        proxy_pnl=proxy_pnls,
        mae=mae,
        rmse=rmse,
        max_error=max_err,
        full_var_99=f_var,
        proxy_var_99=p_var,
        full_es_99=f_es,
        proxy_es_99=p_es,
    )


# ============================================================================
# 7. Verification Tests
# ============================================================================


def run_tests() -> None:
    print("Testing Risk Factor Modelling, Bump Engine, and Scenario Generation...")

    # Define a non-linear toy portfolio: European call option with Black-Scholes
    # Factors: [S (Spot), r (Rate), sigma (Vol)]
    # S = 100, K = 100, T = 1.0, r = 0.05, sigma = 0.20
    def black_scholes_call(factors: Sequence[float]) -> float:
        s = factors[0]
        r = factors[1]
        vol = factors[2]
        k = 100.0
        t = 1.0
        d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / (vol * math.sqrt(t))
        d2 = d1 - vol * math.sqrt(t)
        return s * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d2)

    base = [100.0, 0.05, 0.20]
    bumps = [0.01, 0.0001, 0.0001]

    # 1. Bump engine: Gradient and Hessian
    grad = compute_gradient(black_scholes_call, base, bumps)
    hessian = compute_hessian(black_scholes_call, base, bumps)

    # Analytical BS delta: N(d1)
    # d1 = (ln(1) + (0.05 + 0.02) * 1) / 0.20 = 0.07 / 0.20 = 0.35
    # N(0.35) ≈ 0.63683
    assert abs(grad[0] - 0.63683) < 1e-3, f"Delta mismatch: {grad[0]}"

    # Analytical BS gamma: N'(d1) / (S * sigma * sqrt(T))
    # N'(0.35) = exp(-0.35^2 / 2) / sqrt(2*pi) ≈ 0.37524 / 2.50663 ≈ 0.14970 / 20 = 0.01876
    assert abs(hessian[0][0] - 0.01876) < 1e-4, f"Gamma mismatch: {hessian[0][0]}"

    # Analytical BS vega: S * N'(d1) * sqrt(T) ≈ 100 * 0.37524 = 37.52
    assert abs(grad[2] - 37.524) < 1e-2, f"Vega mismatch: {grad[2]}"

    # 2. Covariance and Cholesky
    # 3x3 covariance matrix for [S, r, sigma]
    # S vol: 20%, rate vol: 100 bps (0.01), vol of vol: 40% (0.08)
    cov = [
        [0.0400, -0.0004, -0.0030],
        [-0.0004, 0.0001, 0.00005],
        [-0.0030, 0.00005, 0.0100],
    ]
    chol = cholesky_decomposition(cov)
    assert chol[0][0] == math.sqrt(0.0400) == 0.20
    # Reconstruct cov[0][0]
    assert abs(chol[0][0] ** 2 - cov[0][0]) < 1e-8

    # 3. Parametric scenario generation
    scenarios = generate_parametric_scenarios(cov, num_scenarios=2000, seed=123)
    assert len(scenarios) == 2000
    assert len(scenarios[0]) == 3

    # Sample variance check for factor 0 (should be close to 0.04)
    s0_vals = [s[0] for s in scenarios]
    s0_var = sum(x * x for x in s0_vals) / len(s0_vals)
    assert 0.035 < s0_var < 0.045, f"Scenario variance mismatch: {s0_var}"

    # 4. Compare Full Revaluation vs Taylor Proxy
    comp = compare_full_vs_proxy(black_scholes_call, base, grad, hessian, scenarios)
    print(f"MAE Full vs Delta-Gamma Proxy: {comp.mae:.4f}")
    print(f"RMSE Full vs Proxy: {comp.rmse:.4f}")
    print(f"Full 99% VaR: {comp.full_var_99:.2f}, Proxy 99% VaR: {comp.proxy_var_99:.2f}")
    print(f"Full 99% ES: {comp.full_es_99:.2f}, Proxy 99% ES: {comp.proxy_es_99:.2f}")
    # Non-linear tail divergence: Taylor proxy understates extreme tail convexity
    assert abs(comp.full_var_99 - comp.proxy_var_99) < 2.5, "VaR discrepancy too large"

    # 5. Stress testing macro scenarios
    stresses = standard_rates_stress_scenarios()
    assert len(stresses) == 6
    print(f"Loaded {len(stresses)} standard rates stress scenarios.")

    print("All risk analytics, scenario generation, and bump engine tests passed!")


if __name__ == "__main__":
    run_tests()
