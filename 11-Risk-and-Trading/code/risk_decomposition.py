"""Risk Decomposition, Euler Allocation, and Risk Parity Engine.

Pure Python 3.10+ standard library implementation:
1. Multi-asset covariance matrix construction from volatilities and correlations.
2. Portfolio volatility and Gaussian Parametric Value at Risk (VaR).
3. Euler risk decomposition: asset betas, Marginal VaR, Component VaR, and percentage shares.
4. Incremental VaR for block trades (first-order marginal approximation vs full exact re-evaluation).
5. Risk Parity / Equal Risk Contribution (ERC) iterative cyclical coordinate descent optimizer.
"""

from __future__ import annotations

import math
from collections.abc import Sequence


def compute_portfolio_variance(weights: Sequence[float], cov: Sequence[Sequence[float]]) -> float:
    """Compute portfolio variance sigma_p^2 = w^T Sigma w."""
    n = len(weights)
    var = 0.0
    for i in range(n):
        for j in range(n):
            var += weights[i] * weights[j] * cov[i][j]
    return var


def compute_asset_covariances_with_portfolio(
    weights: Sequence[float],
    cov: Sequence[Sequence[float]],
) -> list[float]:
    """Compute Cov(r_i, r_p) = (Sigma w)_i for each asset."""
    n = len(weights)
    return [sum(cov[i][j] * weights[j] for j in range(n)) for i in range(n)]


def compute_betas(
    weights: Sequence[float],
    cov: Sequence[Sequence[float]],
) -> tuple[float, list[float]]:
    """Compute portfolio variance and asset betas beta_i = Cov(r_i, r_p) / sigma_p^2."""
    var_p = compute_portfolio_variance(weights, cov)
    if var_p <= 0.0:
        raise ValueError("Portfolio variance must be strictly positive")
    cov_p = compute_asset_covariances_with_portfolio(weights, cov)
    betas = [cov_p[i] / var_p for i in range(len(weights))]
    return var_p, betas


def compute_euler_var_decomposition(
    weights: Sequence[float],
    portfolio_value: float,
    cov: Sequence[Sequence[float]],
    confidence_level: float = 0.95,
    z_score: float | None = None,
) -> dict[str, float | list[float]]:
    """Perform full Euler risk decomposition into Marginal and Component VaR."""
    if z_score is None:
        # Standard normal inverse CDF approximation or exact standard z-scores
        if abs(confidence_level - 0.95) < 1e-4:
            z_score = 1.6448536269514722
        elif abs(confidence_level - 0.99) < 1e-4:
            z_score = 2.3263478740408408
        else:
            z_score = 1.6449

    var_p, betas = compute_betas(weights, cov)
    sigma_p = math.sqrt(var_p)
    var_dollar = portfolio_value * z_score * sigma_p

    n = len(weights)
    mvar_dollar = [betas[i] * var_dollar for i in range(n)]
    mvar_pct = [mvar_dollar[i] / portfolio_value for i in range(n)]
    cvar_dollar = [weights[i] * mvar_dollar[i] for i in range(n)]
    cvar_shares = [cvar_dollar[i] / var_dollar for i in range(n)]

    return {
        "portfolio_variance": var_p,
        "portfolio_volatility": sigma_p,
        "portfolio_var": var_dollar,
        "betas": betas,
        "marginal_var_dollar": mvar_dollar,
        "marginal_var_pct": mvar_pct,
        "component_var_dollar": cvar_dollar,
        "component_shares": cvar_shares,
    }


def compute_incremental_var_trade(
    initial_weights: Sequence[float],
    portfolio_value: float,
    cov_extended: Sequence[Sequence[float]],
    trade_dollars: float,
    trade_asset_idx: int,
    confidence_level: float = 0.95,
    z_score: float = 1.6449,
) -> tuple[float, float]:
    """Compute linear marginal IVaR approximation and exact non-linear IVaR."""
    # Linear approximation using marginal VaR of trade asset relative to initial portfolio
    var_p = compute_portfolio_variance(initial_weights, cov_extended[: len(initial_weights)])
    sigma_p = math.sqrt(var_p)
    var_initial = portfolio_value * z_score * sigma_p

    cov_trade_p = sum(initial_weights[j] * cov_extended[trade_asset_idx][j] for j in range(len(initial_weights)))
    beta_trade = cov_trade_p / var_p
    mvar_trade_dollar = beta_trade * var_initial
    linear_ivar = trade_dollars * (mvar_trade_dollar / portfolio_value)

    # Exact non-linear IVaR: re-evaluate portfolio with new dollar holdings
    n_new = len(cov_extended)
    new_holdings = [initial_weights[i] * portfolio_value for i in range(len(initial_weights))]
    if len(new_holdings) < n_new:
        new_holdings.append(0.0)
    new_holdings[trade_asset_idx] += trade_dollars
    new_total_value = sum(new_holdings)
    new_weights = [new_holdings[i] / new_total_value for i in range(n_new)]

    new_var_p = compute_portfolio_variance(new_weights, cov_extended)
    new_sigma_p = math.sqrt(new_var_p)
    var_new = new_total_value * z_score * new_sigma_p
    exact_ivar = var_new - var_initial

    return linear_ivar, exact_ivar


def solve_risk_parity_weights(
    cov: Sequence[Sequence[float]],
    max_iter: int = 1000,
    tol: float = 1e-8,
) -> list[float]:
    """Solve Equal Risk Contribution (Risk Parity) weights via cyclical coordinate descent."""
    n = len(cov)
    # Start from inverse volatility heuristic
    inv_vols = [1.0 / math.sqrt(cov[i][i]) for i in range(n)]
    sum_inv = sum(inv_vols)
    w = [v / sum_inv for v in inv_vols]

    target_rc = 1.0 / n

    for _ in range(max_iter):
        var_p = compute_portfolio_variance(w, cov)
        # Compute component risk contributions: RC_i = w_i * (Sigma w)_i / sigma_p^2
        sigma_w = [sum(cov[i][j] * w[j] for j in range(n)) for i in range(n)]
        rc = [w[i] * sigma_w[i] / var_p for i in range(n)]

        max_dev = max(abs(rc[i] - target_rc) for i in range(n))
        if max_dev < tol:
            break

        # Multiplicative coordinate update
        w = [w[i] * math.sqrt(target_rc / max(rc[i], 1e-12)) for i in range(n)]
        sum_w = sum(w)
        w = [x / sum_w for x in w]

    return w


def run_decomposition_verification() -> None:
    """Assert all figures quoted in Note 13."""
    # Example 1: 60/40 Equity/Bond Portfolio
    # Equities: w1 = 0.60, sigma1 = 0.20
    # Bonds:    w2 = 0.40, sigma2 = 0.06
    # Correlation rho = -0.15
    w = [0.60, 0.40]
    s1, s2 = 0.20, 0.06
    rho = -0.15
    cov_12 = rho * s1 * s2  # -0.15 * 0.20 * 0.06 = -0.0018
    cov_mat = [
        [s1 * s1, cov_12],
        [cov_12, s2 * s2],
    ]

    # Step 1: Variance and standard deviation
    w1_sq_s1_sq = (0.60**2) * (0.20**2)  # 0.014400
    w2_sq_s2_sq = (0.40**2) * (0.06**2)  # 0.000576
    cross_term = 2.0 * 0.60 * 0.40 * cov_12  # -0.000864
    var_p_exact = w1_sq_s1_sq + w2_sq_s2_sq + cross_term

    assert abs(w1_sq_s1_sq - 0.014400) < 1e-9
    assert abs(w2_sq_s2_sq - 0.000576) < 1e-9
    assert abs(cross_term - (-0.000864)) < 1e-9
    assert abs(var_p_exact - 0.014112) < 1e-9

    sigma_p = math.sqrt(var_p_exact)
    assert abs(sigma_p - 0.1187939) < 1e-6
    assert abs(sigma_p - 0.1188) < 1e-4

    portfolio_value = 100_000_000.0
    z_095 = 1.6449
    var_95 = portfolio_value * z_095 * sigma_p
    assert abs(var_95 - 19_540_415) < 1.0  # Asserts $19,540,415

    # Step 2: Covariances with portfolio
    cov_1_p = 0.60 * (s1 * s1) + 0.40 * cov_12  # 0.0240 - 0.00072 = 0.02328
    cov_2_p = 0.40 * (s2 * s2) + 0.60 * cov_12  # 0.00144 - 0.00108 = 0.00036
    assert abs(cov_1_p - 0.02328) < 1e-9
    assert abs(cov_2_p - 0.00036) < 1e-9

    # Step 3: Betas
    beta1 = cov_1_p / var_p_exact
    beta2 = cov_2_p / var_p_exact
    assert abs(beta1 - 1.64966) < 1e-4
    assert abs(beta2 - 0.02551) < 1e-4
    weighted_beta = 0.60 * beta1 + 0.40 * beta2
    assert abs(weighted_beta - 1.00000) < 1e-6

    # Step 4: Marginal VaRs
    mvar1 = beta1 * var_95
    mvar2 = beta2 * var_95
    assert abs(mvar1 - 32_235_038) < 2.0  # Asserts $32,235,038 (32.24%)
    assert abs(mvar2 - 498_480) < 2.0  # Asserts $498,480 (0.50%)

    # Step 5: Component VaRs
    cvar1 = 0.60 * mvar1
    cvar2 = 0.40 * mvar2
    assert abs(cvar1 - 19_341_023) < 2.0  # Asserts $19,341,023
    assert abs(cvar2 - 199_392) < 2.0  # Asserts $199,392
    assert abs((cvar1 + cvar2) - var_95) < 2.0

    share1 = cvar1 / var_95
    share2 = cvar2 / var_95
    assert abs(share1 - 0.9898) < 1e-4  # 98.98%
    assert abs(share2 - 0.0102) < 1e-4  # 1.02%

    # Example 2: Adding $5,000,000 Gold position (Asset 3)
    # sigma3 = 0.15, rho31 = 0.10, rho32 = 0.30
    s3 = 0.15
    rho31, rho32 = 0.10, 0.30
    cov31 = rho31 * s3 * s1  # 0.10 * 0.15 * 0.20 = 0.00300
    cov32 = rho32 * s3 * s2  # 0.30 * 0.15 * 0.06 = 0.00270
    assert abs(cov31 - 0.00300) < 1e-9
    assert abs(cov32 - 0.00270) < 1e-9

    cov3_p = 0.60 * cov31 + 0.40 * cov32  # 0.00180 + 0.00108 = 0.00288
    assert abs(cov3_p - 0.00288) < 1e-9

    beta3 = cov3_p / var_p_exact
    assert abs(beta3 - 0.20408) < 1e-4

    mvar3 = beta3 * var_95
    assert abs(mvar3 - 3_987_840) < 5.0  # Asserts $3,987,840

    trade_dollars = 5_000_000.0
    ivar_linear = trade_dollars * (mvar3 / portfolio_value)
    assert abs(ivar_linear - 199_392) < 2.0  # Asserts +$199,392

    # Verify Euler decomposition engine
    res = compute_euler_var_decomposition(w, portfolio_value, cov_mat, z_score=z_095)
    assert abs(float(res["portfolio_volatility"]) - 0.1187939) < 1e-6
    assert abs(float(res["portfolio_var"]) - 19_540_415) < 1.0

    # Risk Parity optimizer verification
    erc_w = solve_risk_parity_weights(cov_mat)
    erc_var_p = compute_portfolio_variance(erc_w, cov_mat)
    erc_sigma_w = [sum(cov_mat[i][j] * erc_w[j] for j in range(2)) for i in range(2)]
    erc_rc = [erc_w[i] * erc_sigma_w[i] / erc_var_p for i in range(2)]
    assert abs(erc_rc[0] - 0.50) < 1e-5
    assert abs(erc_rc[1] - 0.50) < 1e-5

    print(f"Portfolio Volatility: {sigma_p:.4f} (11.88%)")
    print(f"95% Annual VaR: ${var_95:,.2f}")
    print(f"Betas: Equity={beta1:.5f}, Bond={beta2:.5f}")
    print(f"Component VaR: Equity=${cvar1:,.2f} ({share1:.2%}), Bond=${cvar2:,.2f} ({share2:.2%})")
    print(f"Gold Beta: {beta3:.5f}, MVaR: ${mvar3:,.2f}, Linear IVaR: +${ivar_linear:,.2f}")
    print(f"Risk Parity Weights: Equity={erc_w[0]:.2%}, Bond={erc_w[1]:.2%}")
    print("All risk decomposition and Euler allocation tests passed successfully!")


if __name__ == "__main__":
    run_decomposition_verification()
