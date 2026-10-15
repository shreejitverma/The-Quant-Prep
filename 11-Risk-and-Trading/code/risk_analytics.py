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


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / SQRT_TWO))


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
    historical_vols: Sequence[Sequence[float]],
    current_vols: Sequence[float],
) -> list[list[float]]:
    """Per-factor volatility-scaled filtered historical simulation (Hull-White).

    Scenario t, factor j becomes r[t][j] * current_vols[j] / historical_vols[t][j].
    Shape mismatches raise ValueError via zip(strict=True).
    """
    if any(v <= 0.0 for v in current_vols):
        raise ValueError("current_vols must be strictly positive")

    filtered: list[list[float]] = []
    for returns, vols in zip(historical_returns, historical_vols, strict=True):
        if any(v <= 0.0 for v in vols):
            raise ValueError("historical_vols must be strictly positive")
        filtered.append([r * c / v for r, c, v in zip(returns, current_vols, vols, strict=True)])

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
        if s <= 0.0 or vol <= 0.0:
            raise ValueError(f"Spot and vol must be positive: S={s}, vol={vol}")
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
    # N'(0.35) = exp(-0.35^2 / 2) / sqrt(2*pi) ≈ 0.37524 / 20 = 0.01876
    assert abs(hessian[0][0] - 0.01876) < 1e-4, f"Gamma mismatch: {hessian[0][0]}"

    # Analytical BS vega: S * N'(d1) * sqrt(T) ≈ 100 * 0.37524 = 37.52
    assert abs(grad[2] - 37.524) < 1e-2, f"Vega mismatch: {grad[2]}"

    try:
        black_scholes_call([100.0, 0.05, -0.10])
    except ValueError:
        pass
    else:
        raise AssertionError("Pricing at negative vol must be rejected")

    # 2. Bump engine and Taylor proxy on a quadratic, where both are exact.
    # q(x) = c.x + 0.5 x^T A x has gradient c + A x and Hessian A.
    c_lin = [1.0, -3.0]
    a_quad = [[2.0, 0.5], [0.5, 1.0]]

    def quadratic(x: Sequence[float]) -> float:
        lin = c_lin[0] * x[0] + c_lin[1] * x[1]
        quad = a_quad[0][0] * x[0] ** 2 + 2.0 * a_quad[0][1] * x[0] * x[1] + a_quad[1][1] * x[1] ** 2
        return lin + 0.5 * quad

    x0 = [1.0, 2.0]
    # c + A x0 = [1 + 2 + 1, -3 + 0.5 + 2] = [4.0, -0.5]
    exact_grad = [4.0, -0.5]
    q_grad = compute_gradient(quadratic, x0, [0.1, 0.1])
    q_hess = compute_hessian(quadratic, x0, [0.1, 0.1])
    for i in range(2):
        assert abs(q_grad[i] - exact_grad[i]) < 1e-9, f"Quadratic gradient mismatch: {q_grad}"
        for j in range(2):
            assert abs(q_hess[i][j] - a_quad[i][j]) < 1e-9, f"Quadratic Hessian mismatch: {q_hess}"
    dx_q = [0.3, -0.7]
    exact_pnl = quadratic([x0[0] + dx_q[0], x0[1] + dx_q[1]]) - quadratic(x0)
    taylor_pnl = evaluate_taylor_pnl(exact_grad, a_quad, dx_q)
    assert abs(taylor_pnl - exact_pnl) < 1e-12, f"Taylor P&L mismatch: {taylor_pnl} vs {exact_pnl}"

    # 3. Covariance and Cholesky
    # Shock SDs: spot $5.00 (5% of S), rate 25 bp, vol 2 vol points.
    # Correlations: spot-rate +0.20, spot-vol -0.50, rate-vol 0.
    cov = [
        [25.0, 0.0025, -0.05],
        [0.0025, 0.00000625, 0.0],
        [-0.05, 0.0, 0.0004],
    ]
    chol = cholesky_decomposition(cov)
    for i in range(3):
        for j in range(3):
            rebuilt = sum(chol[i][k] * chol[j][k] for k in range(3))
            assert abs(rebuilt - cov[i][j]) < 1e-12, f"L L^T mismatch at ({i}, {j})"

    # 4. Parametric scenario generation
    scenarios = generate_parametric_scenarios(cov, num_scenarios=2000, seed=123)
    assert len(scenarios) == 2000
    assert len(scenarios[0]) == 3

    # Sample variance check for factor 0 (should be close to 25.0)
    s0_vals = [s[0] for s in scenarios]
    s0_var = sum(x * x for x in s0_vals) / len(s0_vals)
    assert 22.5 < s0_var < 27.5, f"Scenario variance mismatch: {s0_var}"

    # 5. Compare Full Revaluation vs Taylor Proxy
    v0 = black_scholes_call(base)
    comp = compare_full_vs_proxy(black_scholes_call, base, grad, hessian, scenarios)
    print(f"Base call value V0: {v0:.4f}")
    print(f"MAE Full vs Delta-Gamma Proxy: {comp.mae:.4f}")
    print(f"RMSE Full vs Proxy: {comp.rmse:.4f}")
    print(f"Max abs error Full vs Proxy: {comp.max_error:.4f}")
    print(f"Full 99% VaR: {comp.full_var_99:.2f}, Proxy 99% VaR: {comp.proxy_var_99:.2f}")
    print(f"Full 99% ES: {comp.full_es_99:.2f}, Proxy 99% ES: {comp.proxy_es_99:.2f}")
    # A long call is worth at least zero, so no full-revaluation loss can exceed V0.
    assert max(-p for p in comp.full_reval_pnl) < v0, "Full-revaluation loss exceeds premium"
    assert comp.full_es_99 >= comp.full_var_99, "ES below VaR"

    # 6. Filtered historical simulation, per-factor scaling.
    # Note 11 Example 1: -0.022 * 0.024 / 0.011 = -0.048.
    # Second factor (rates): 0.0010 * 0.0010 / 0.0005 = 0.0020.
    fhs = filter_historical_scenarios([[-0.022, 0.0010]], [[0.011, 0.0005]], [0.024, 0.0010])
    assert abs(fhs[0][0] - (-0.048)) < 1e-12, f"FHS equity mismatch: {fhs[0][0]}"
    assert abs(fhs[0][1] - 0.0020) < 1e-12, f"FHS rates mismatch: {fhs[0][1]}"
    try:
        filter_historical_scenarios([[-0.022]], [[0.0]], [0.024])
    except ValueError:
        pass
    else:
        raise AssertionError("FHS must reject a zero historical vol")
    try:
        filter_historical_scenarios([[-0.022, 0.0010]], [[0.011]], [0.024, 0.0010])
    except ValueError:
        pass
    else:
        raise AssertionError("FHS must reject a vol row with the wrong number of factors")

    # 7. Stress scenarios match their names: steepeners widen 2s10s,
    # flatteners narrow it, parallel shifts move every tenor equally.
    # Tenors: [2y, 5y, 10y, 30y].
    stresses = standard_rates_stress_scenarios()
    for sc in stresses:
        spread_change = sc.shocks[2] - sc.shocks[0]
        if "Steepener" in sc.name:
            assert spread_change > 0.0, f"{sc.name} does not steepen 2s10s"
        if "Flattener" in sc.name:
            assert spread_change < 0.0, f"{sc.name} does not flatten 2s10s"
        if "Parallel" in sc.name:
            assert len(set(sc.shocks)) == 1, f"{sc.name} is not parallel"
    print(f"Loaded {len(stresses)} standard rates stress scenarios.")

    print("All risk analytics, scenario generation, and bump engine tests passed!")


if __name__ == "__main__":
    run_tests()
