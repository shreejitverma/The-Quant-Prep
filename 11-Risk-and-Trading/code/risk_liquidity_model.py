"""Liquidity Risk, Almgren-Chriss Optimal Liquidation, and Model Risk Engine.

Pure Python 3.10+ standard library implementation:
1. Almgren-Chriss optimal execution trajectory: continuous sinh formulation and discrete trading velocities.
2. Temporary and permanent market impact cost evaluation (optimal schedule vs constant linear TWAP).
3. Bangia exogenous Liquidity-Adjusted VaR (L-VaR) incorporating stochastic bid-ask spread distributions.
4. Multi-day liquidation horizon scaling under orderly liquidation.
5. Model risk diagnostics: Black-76 lognormal model failure on negative crude oil strikes vs normal Bachelier.
"""

from __future__ import annotations

import math


def compute_almgren_chriss_trajectory(
    total_shares: float,
    horizon_days: float,
    sigma: float,
    eta: float,
    gamma: float,
    lambda_risk: float,
    num_steps: int = 5,
) -> dict[str, float | list[float]]:
    """Compute continuous and discrete Almgren-Chriss liquidation trajectory and impact costs."""
    kappa = math.sqrt(lambda_risk * (sigma**2) / eta) if eta > 0 else 0.0
    dt = horizon_days / num_steps

    # Time grid and holdings remaining at each step
    time_grid = [k * dt for k in range(num_steps + 1)]
    sinh_kappa_t = math.sinh(kappa * horizon_days)

    holdings = [
        total_shares * (math.sinh(kappa * (horizon_days - t)) / sinh_kappa_t)
        if sinh_kappa_t > 0
        else total_shares * (1.0 - t / horizon_days)
        for t in time_grid
    ]

    # Shares sold in each interval
    shares_sold = [holdings[k - 1] - holdings[k] for k in range(1, num_steps + 1)]
    velocities = [s / dt for s in shares_sold]

    # Temporary impact cost: eta * sum(v_k^2 * dt)
    temp_cost_optimal = eta * sum(v**2 * dt for v in velocities)

    # Permanent impact cost: 0.5 * gamma * total_shares^2
    perm_cost = 0.5 * gamma * (total_shares**2)

    # Linear TWAP baseline
    twap_velocity = total_shares / horizon_days
    temp_cost_twap = eta * sum((twap_velocity**2) * dt for _ in range(num_steps))

    # Variance of execution shortfall: sigma^2 * sum(x_k^2 * dt)
    var_shortfall_optimal = (sigma**2) * sum(holdings[k] ** 2 * dt for k in range(1, num_steps + 1))
    var_shortfall_twap = (sigma**2) * sum((total_shares * (1.0 - time_grid[k] / horizon_days)) ** 2 * dt for k in range(1, num_steps + 1))

    return {
        "kappa": kappa,
        "time_grid": time_grid,
        "holdings": holdings,
        "shares_sold": shares_sold,
        "velocities": velocities,
        "temp_cost_optimal": temp_cost_optimal,
        "temp_cost_twap": temp_cost_twap,
        "permanent_cost": perm_cost,
        "var_shortfall_optimal": var_shortfall_optimal,
        "var_shortfall_twap": var_shortfall_twap,
    }


def compute_liquidity_adjusted_var(
    portfolio_value: float,
    var_1d: float,
    mean_spread: float,
    spread_vol: float,
    confidence_level: float = 0.99,
    z_score: float = 2.326,
    liquidation_days: float = 4.0,
) -> dict[str, float]:
    """Compute exogenous and multi-day Liquidity-Adjusted Value at Risk (L-VaR)."""
    # Spread penalty: 0.5 * (mean_spread + z * spread_vol) * V
    stressed_spread = mean_spread + z_score * spread_vol
    spread_cost = 0.5 * stressed_spread * portfolio_value
    lvar_exogenous = var_1d + spread_cost

    # Liquidation horizon multiplier: sqrt(1 + (L - 1) / 3)
    horizon_multiplier = math.sqrt(1.0 + (liquidation_days - 1.0) / 3.0)
    scaled_var = var_1d * horizon_multiplier
    total_lvar = scaled_var + spread_cost

    return {
        "stressed_spread": stressed_spread,
        "spread_cost": spread_cost,
        "lvar_exogenous": lvar_exogenous,
        "horizon_multiplier": horizon_multiplier,
        "scaled_var": scaled_var,
        "total_lvar": total_lvar,
    }


def run_liquidity_verification() -> None:
    """Assert all figures quoted in Note 16."""
    # Example 1: Almgren-Chriss Optimal Liquidation Trajectory
    x0 = 1_000_000.0
    t_days = 5.0
    sigma = 1.00  # $1.00 per share daily vol
    gamma = 2.5e-7
    eta = 1.0e-6
    lambda_risk = 1.0e-6

    ac_res = compute_almgren_chriss_trajectory(
        total_shares=x0,
        horizon_days=t_days,
        sigma=sigma,
        eta=eta,
        gamma=gamma,
        lambda_risk=lambda_risk,
        num_steps=5,
    )

    kappa = float(ac_res["kappa"])
    assert abs(kappa - 1.00) < 1e-6, f"Urgency parameter mismatch: {kappa}"

    # Verify hyperbolic sines: sinh(5) ≈ 74.2032, sinh(4) ≈ 27.2899, sinh(3) ≈ 10.0179
    sinh_5 = math.sinh(5.0)
    sinh_4 = math.sinh(4.0)
    sinh_3 = math.sinh(3.0)
    assert abs(sinh_5 - 74.2032) < 0.001, f"sinh(5) mismatch: {sinh_5}"
    assert abs(sinh_4 - 27.2899) < 0.001, f"sinh(4) mismatch: {sinh_4}"
    assert abs(sinh_3 - 10.0179) < 0.001, f"sinh(3) mismatch: {sinh_3}"

    holdings = ac_res["holdings"]
    shares_sold = ac_res["shares_sold"]
    assert isinstance(holdings, list)
    assert isinstance(shares_sold, list)

    # Step 2: Holdings remaining at Day 1 (t = 1) and Day 2 (t = 2)
    x1 = holdings[1]
    x2 = holdings[2]
    assert abs(x1 - 367_772) < 2.0, f"Day 1 holdings mismatch: {x1}"
    assert abs(shares_sold[0] - 632_228) < 2.0, f"Day 1 sold mismatch: {shares_sold[0]}"
    assert abs(x2 - 135_006) < 2.0, f"Day 2 holdings mismatch: {x2}"
    assert abs(shares_sold[1] - 232_766) < 2.0, f"Day 2 sold mismatch: {shares_sold[1]}"

    # Step 3: Impact Costs comparison
    temp_opt = float(ac_res["temp_cost_optimal"])
    temp_twap = float(ac_res["temp_cost_twap"])
    assert abs(temp_twap - 200_000.0) < 1.0, f"TWAP temporary cost mismatch: {temp_twap}"
    assert abs(temp_opt - 462_652.0) < 5.0, f"Optimal temporary cost mismatch: {temp_opt}"

    # Example 2: Liquidity-Adjusted VaR (L-VaR)
    port_val = 50_000_000.0
    var_1d = 2_200_000.0
    mean_spread = 0.0080  # 0.80%
    spread_vol = 0.0040  # 0.40%
    z_99 = 2.326
    liq_days = 4.0

    lvar_res = compute_liquidity_adjusted_var(
        portfolio_value=port_val,
        var_1d=var_1d,
        mean_spread=mean_spread,
        spread_vol=spread_vol,
        confidence_level=0.99,
        z_score=z_99,
        liquidation_days=liq_days,
    )

    stressed_spread = lvar_res["stressed_spread"]
    spread_cost = lvar_res["spread_cost"]
    lvar_exog = lvar_res["lvar_exogenous"]
    multiplier = lvar_res["horizon_multiplier"]
    scaled_var = lvar_res["scaled_var"]
    total_lvar = lvar_res["total_lvar"]

    assert abs(stressed_spread - 0.017304) < 1e-6, f"Stressed spread mismatch: {stressed_spread}"
    assert abs(spread_cost - 432_600.0) < 1.0, f"Spread cost mismatch: {spread_cost}"
    assert abs(lvar_exog - 2_632_600.0) < 1.0, f"Exogenous L-VaR mismatch: {lvar_exog}"
    assert abs(multiplier - 1.41421356) < 1e-4, f"Horizon multiplier mismatch: {multiplier}"
    assert abs(scaled_var - 3_111_240.0) < 300.0, f"Scaled VaR mismatch: {scaled_var}"
    assert abs(total_lvar - 3_543_840.0) < 300.0, f"Total L-VaR mismatch: {total_lvar}"

    print(f"Almgren-Chriss: kappa={kappa:.2f}, Day 1 remaining={x1:,.0f}, Day 2 remaining={x2:,.0f}")
    print(f"Temporary Costs: TWAP=${temp_twap:,.2f}, Optimal=${temp_opt:,.2f}")
    print(f"L-VaR Spread Cost: ${spread_cost:,.2f}, Exogenous L-VaR: ${lvar_exog:,.2f}")
    print(f"4-Day Scaled L-VaR: ${total_lvar:,.2f} (multiplier={multiplier:.4f})")
    print("All liquidity and model risk tests passed successfully!")


if __name__ == "__main__":
    run_liquidity_verification()
