"""Comprehensive Risk and Trading Problem Set Numerical Calculation Engine.

Pure Python 3.10+ standard library implementation:
Asserts every single numerical figure across all 16 problems in Note 17:
- Problem 1: Kelly Criterion and Position Sizing (leverage, drawdown probabilities)
- Problem 2: Parametric VaR vs Expected Shortfall Gaussian
- Problem 3: Filtered Historical Simulation (FHS) return updating
- Problem 4: Reverse Stress Testing & Mahalanobis Distance
- Problem 5: Expected Maximum Drawdown Analytics (Magdon-Ismail & Atiya)
- Problem 6: Derivatives Greek P&L Attribution & Residual
- Problem 7: Black-Scholes PDE Theta vs Gamma Break-Even Move
- Problem 8: Euler Risk Allocation and Component VaR
- Problem 9: Almgren-Chriss Optimal Liquidation Trajectory
- Problem 10: Liquidity-Adjusted VaR (L-VaR)
- Problem 11: Counterparty Exposure Profiles and Effective EPE
- Problem 12: Bilateral CVA and DVA Calculation
- Problem 13: PCA Yield Curve Factor Shocks
- Problem 14: Funding Valuation Adjustment (FVA / FCA)
- Problem 15: Margin Valuation Adjustment (MVA)
- Problem 16: Capital Valuation Adjustment (KVA)
"""

from __future__ import annotations

import math


def run_all_problem_set_assertions() -> None:
    """Run exact verification of all 16 problems in Note 17."""
    print("Verifying Problem 1: Kelly Criterion and Position Sizing...")
    mu_minus_r = 0.120
    sigma = 0.160
    f_star = mu_minus_r / (sigma**2)
    assert abs(f_star - 4.6875) < 1e-6, f"Full Kelly mismatch: {f_star}"

    f_half = 0.5 * f_star
    assert abs(f_half - 2.34375) < 1e-6, f"Half Kelly mismatch: {f_half}"

    mu_p_half = f_half * mu_minus_r
    sigma_p_half = f_half * sigma
    assert abs(mu_p_half - 0.28125) < 1e-6, f"Expected return mismatch: {mu_p_half}"
    assert abs(sigma_p_half - 0.3750) < 1e-6, f"Portfolio vol mismatch: {sigma_p_half}"

    # Growth rate comparisons: g(f) = f*mu - 0.5*f^2*sigma^2
    g_full = f_star * mu_minus_r - 0.5 * (f_star**2) * (sigma**2)
    g_half = f_half * mu_minus_r - 0.5 * (f_half**2) * (sigma**2)
    assert abs(g_full - 0.28125) < 1e-6, f"Full growth rate mismatch: {g_full}"
    assert abs(g_half - 0.2109375) < 1e-6, f"Half growth rate mismatch: {g_half}"
    assert abs(g_half / g_full - 0.75) < 1e-6, "Half Kelly must achieve 75% of max growth"

    # 50% drawdown probabilities: (0.50)^a where a = 2/c - 1
    # Full Kelly (c=1.0 -> a=1): 0.50^1 = 0.50 (50%)
    # Half Kelly (c=0.5 -> a=3): 0.50^3 = 0.125 (12.5%)
    prob_dd50_full = 0.50**1
    prob_dd50_half = 0.50**3
    assert abs(prob_dd50_full - 0.50) < 1e-6
    assert abs(prob_dd50_half - 0.125) < 1e-6

    # Halving before doubling: 1 / (2^a + 1)
    p_halve_full = 1.0 / (2**1 + 1)
    p_halve_half = 1.0 / (2**3 + 1)
    assert abs(p_halve_full - 1.0 / 3.0) < 1e-6
    assert abs(p_halve_half - 1.0 / 9.0) < 1e-6

    print("Verifying Problem 2: Parametric VaR vs Expected Shortfall...")
    val_p2 = 50_000_000.0
    daily_vol = 0.0120
    sigma_dollar = val_p2 * daily_vol
    assert abs(sigma_dollar - 600_000.0) < 1e-6

    z_99 = 2.3263478740408408
    var_99 = z_99 * sigma_dollar
    assert abs(var_99 - 1_395_808.7) < 5.0  # Asserts $1,395,810

    # Normal PDF at z_99: phi(z) = exp(-0.5 * z^2) / sqrt(2*pi)
    phi_z99 = math.exp(-0.5 * (z_99**2)) / math.sqrt(2.0 * math.pi)
    assert abs(phi_z99 - 0.026652) < 1e-4

    es_mult = phi_z99 / 0.0100
    assert abs(es_mult - 2.6652) < 0.01
    es_99 = es_mult * sigma_dollar
    assert abs(es_99 - 1_599_120.0) < 50.0  # Asserts $1,599,120

    print("Verifying Problem 3: Filtered Historical Simulation...")
    current_vol = 0.0220
    r_a, vol_a = -0.0300, 0.0100
    r_b, vol_b = -0.0450, 0.0300

    r_a_fhs = r_a * (current_vol / vol_a)
    r_b_fhs = r_b * (current_vol / vol_b)
    assert abs(r_a_fhs - (-0.0660)) < 1e-6  # -6.60%
    assert abs(r_b_fhs - (-0.0330)) < 1e-4  # -3.30%

    print("Verifying Problem 4: Reverse Stress Testing...")
    # Minimize 0.5 * u^T R^-1 u subject to u1 - 2*u2 = -12.5
    # R = [[1.0, 0.20], [0.20, 1.0]], c = [1.0, -2.0]
    # u* = lambda * R * c
    # R * c = [1.0 - 0.40, 0.20 - 2.0] = [0.60, -1.80]
    # c^T (R c) = 1(0.60) - 2(-1.80) = 0.60 + 3.60 = 4.20
    # lambda = -12.5 / 4.20 = -2.976190476
    lam = -12.5 / 4.20
    assert abs(lam - (-2.97619)) < 1e-4

    u1_star = lam * 0.60
    u2_star = lam * (-1.80)
    assert abs(u1_star - (-1.785714)) < 1e-4
    assert abs(u2_star - 5.357143) < 1e-4

    # Convert to physical variables: x1 = u1 * 0.010, x2 = u2 * 8.0
    x1_star = u1_star * 0.010
    x2_star = u2_star * 8.0
    assert abs(x1_star - (-0.017857)) < 1e-4  # -1.79%
    assert abs(x2_star - 42.857) < 0.05  # +42.9 bps

    # Check constraint: PnL = 20M * x1 - 50k * x2 = -2.5M
    pnl_stress = 20_000_000.0 * x1_star - 50_000.0 * x2_star
    assert abs(pnl_stress - (-2_500_000.0)) < 1e-4

    print("Verifying Problem 5: Expected Maximum Drawdown Analytics...")
    sr = 1.20
    vol_p5 = 0.120
    scale = vol_p5 / (2.0 * sr)
    assert abs(scale - 0.050) < 1e-6

    # 2-year horizon:
    s2_t_half_2 = (sr**2) * 2.0 / 2.0
    assert abs(s2_t_half_2 - 1.44) < 1e-6
    mdd_2y = scale * (math.log(1.44) + 1.9635)
    assert abs(mdd_2y - 0.11641) < 1e-4  # 11.64%

    # 10-year horizon:
    s2_t_half_10 = (sr**2) * 10.0 / 2.0
    assert abs(s2_t_half_10 - 7.20) < 1e-6
    mdd_10y = scale * (math.log(7.20) + 1.9635)
    assert abs(mdd_10y - 0.19688) < 1e-4  # 19.69%

    # Zero drift 2-year: sqrt(pi/2) * sigma * sqrt(T)
    mdd_zero_2y = math.sqrt(math.pi / 2.0) * vol_p5 * math.sqrt(2.0)
    assert abs(mdd_zero_2y - 0.2127) < 1e-3  # 21.27%

    print("Verifying Problem 6: Derivatives Greek P&L Attribution...")
    delta_pnl = 10_000.0 * 2.00
    gamma_pnl = 0.5 * 2_500.0 * (2.00**2)
    theta_pnl = -850.0
    vega_pnl = 400_000.0 * (-0.0250)
    vanna_pnl = 15_000.0 * 2.00 * (-0.0250)
    volga_pnl = 0.5 * 800_000.0 * ((-0.0250) ** 2)

    assert abs(delta_pnl - 20_000.0) < 1e-6
    assert abs(gamma_pnl - 5_000.0) < 1e-6
    assert abs(theta_pnl - (-850.0)) < 1e-6
    assert abs(vega_pnl - (-10_000.0)) < 1e-6
    assert abs(vanna_pnl - (-750.0)) < 1e-6
    assert abs(volga_pnl - 250.0) < 1e-6

    pred_pnl = delta_pnl + gamma_pnl + theta_pnl + vega_pnl + vanna_pnl + volga_pnl
    assert abs(pred_pnl - 13_650.0) < 1e-6

    actual_pnl = 14_200.0
    residual = actual_pnl - pred_pnl
    assert abs(residual - 550.0) < 1e-6

    print("Verifying Problem 7: Black-Scholes PDE Theta vs Gamma Break-Even...")
    s_p7 = 500.0
    gamma_p7 = 800.0
    vol_p7 = 0.180
    theta_annual = -0.5 * (vol_p7**2) * (s_p7**2) * gamma_p7
    assert abs(theta_annual - (-3_240_000.0)) < 1e-6

    theta_daily = theta_annual / 252.0
    assert abs(theta_daily - (-12_857.142857)) < 1e-4

    # Break-even move: 0.5 * gamma * (dS)^2 = -theta_daily
    ds_sq = (-theta_daily) / (0.5 * gamma_p7)
    assert abs(ds_sq - 32.142857) < 1e-4
    ds_breakeven = math.sqrt(ds_sq)
    assert abs(ds_breakeven - 5.6695) < 1e-4

    rule_of_16 = (vol_p7 / 16.0) * s_p7
    assert abs(rule_of_16 - 5.6250) < 1e-4

    print("Verifying Problem 8: Euler Risk Allocation and Component VaR...")
    w1, w2 = 0.80, 0.20
    s1_p8, s2_p8 = 0.15, 0.25
    rho_p8 = 0.40
    cov12_p8 = rho_p8 * s1_p8 * s2_p8
    var_p8 = (w1**2) * (s1_p8**2) + (w2**2) * (s2_p8**2) + 2.0 * w1 * w2 * cov12_p8
    assert abs(var_p8 - 0.021700) < 1e-6
    sigma_p8 = math.sqrt(var_p8)
    assert abs(sigma_p8 - 0.147309) < 1e-5

    port_val_p8 = 100_000_000.0
    z_p8 = 1.6449
    var_dollar_p8 = port_val_p8 * z_p8 * sigma_p8
    assert abs(var_dollar_p8 - 24_230_890.0) < 2.0

    cov1_p = w1 * (s1_p8**2) + w2 * cov12_p8
    cov2_p = w2 * (s2_p8**2) + w1 * cov12_p8
    assert abs(cov1_p - 0.02100) < 1e-6
    assert abs(cov2_p - 0.02450) < 1e-6

    beta1_p8 = cov1_p / var_p8
    beta2_p8 = cov2_p / var_p8
    assert abs(beta1_p8 - 0.967742) < 1e-5
    assert abs(beta2_p8 - 1.129032) < 1e-5

    mvar1_p8 = beta1_p8 * var_dollar_p8
    mvar2_p8 = beta2_p8 * var_dollar_p8
    assert abs(mvar1_p8 - 23_449_248.0) < 2.0
    assert abs(mvar2_p8 - 27_357_457.0) < 2.0

    cvar1_p8 = w1 * mvar1_p8
    cvar2_p8 = w2 * mvar2_p8
    assert abs(cvar1_p8 - 18_759_399.0) < 2.0
    assert abs(cvar2_p8 - 5_471_491.0) < 2.0
    assert abs((cvar1_p8 + cvar2_p8) - var_dollar_p8) < 2.0

    print("Verifying Problem 9: Almgren-Chriss Optimal Liquidation Trajectory...")
    x0_p9 = 500_000.0
    t_p9 = 3.0
    sigma_p9 = 2.00
    eta_p9 = 2.0e-6
    lam_p9 = 2.0e-6
    kappa_p9 = math.sqrt(lam_p9 * (sigma_p9**2) / eta_p9)
    assert abs(kappa_p9 - 2.00) < 1e-6

    sinh_6 = math.sinh(kappa_p9 * t_p9)
    sinh_4 = math.sinh(kappa_p9 * (t_p9 - 1.0))
    sinh_2 = math.sinh(kappa_p9 * (t_p9 - 2.0))
    assert abs(sinh_6 - 201.7132) < 0.01
    assert abs(sinh_4 - 27.2899) < 0.01
    assert abs(sinh_2 - 3.6269) < 0.01

    x1_p9 = x0_p9 * (sinh_4 / sinh_6)
    x2_p9 = x0_p9 * (sinh_2 / sinh_6)
    assert abs(x1_p9 - 67_645) < 2.0
    assert abs(x2_p9 - 8_990) < 2.0

    sold_1 = x0_p9 - x1_p9
    sold_2 = x1_p9 - x2_p9
    sold_3 = x2_p9
    assert abs(sold_1 - 432_355) < 2.0
    assert abs(sold_2 - 58_655) < 2.0
    assert abs(sold_3 - 8_990) < 2.0

    print("Verifying Problem 10: Liquidity-Adjusted VaR (L-VaR)...")
    val_p10 = 30_000_000.0
    var_1d_p10 = 1_500_000.0
    mean_s_p10 = 0.0120
    vol_s_p10 = 0.0060
    z_p10 = 2.326
    l_p10 = 3.0

    spread_cost_p10 = 0.5 * (mean_s_p10 + z_p10 * vol_s_p10) * val_p10
    assert abs(spread_cost_p10 - 389_340.0) < 1.0

    multiplier_p10 = math.sqrt(1.0 + (l_p10 - 1.0) / 3.0)
    assert abs(multiplier_p10 - math.sqrt(5.0 / 3.0)) < 1e-6
    assert abs(multiplier_p10 - 1.290994) < 1e-5

    scaled_var_p10 = var_1d_p10 * multiplier_p10
    assert abs(scaled_var_p10 - 1_936_492.0) < 2.0

    total_lvar_p10 = scaled_var_p10 + spread_cost_p10
    assert abs(total_lvar_p10 - 2_325_832.0) < 2.0

    print("Verifying Problem 11: Counterparty Exposure Profiles and Effective EPE...")
    ee_profile = [0.0, 80_000.0, 120_000.0, 160_000.0, 130_000.0, 80_000.0, 0.0]
    eee_profile = [0.0]
    for e in ee_profile[1:]:
        eee_profile.append(max(eee_profile[-1], e))
    assert eee_profile == [0.0, 80_000.0, 120_000.0, 160_000.0, 160_000.0, 160_000.0, 160_000.0]

    # 1-year EEPE: trapezoidal over [0, 0.5] and [0.5, 1.0]
    eepe_1y = (0.5 * 0.5 * (0.0 + 80_000.0) + 0.5 * 0.5 * (80_000.0 + 120_000.0)) / 1.0
    assert abs(eepe_1y - 70_000.0) < 1e-6
    ead_p11 = 1.4 * eepe_1y
    assert abs(ead_p11 - 98_000.0) < 1e-6

    print("Verifying Problem 12: Bilateral CVA and DVA Calculation...")
    ee_p12 = 500_000.0
    ene_p12 = 300_000.0
    df_half = math.exp(-0.04 * 0.5)
    assert abs(df_half - 0.98019867) < 1e-5

    pd_c_p12 = 1.0 - math.exp(-0.030 * 1.0)
    pd_b_p12 = 1.0 - math.exp(-0.015 * 1.0)
    assert abs(pd_c_p12 - 0.0295545) < 1e-5
    assert abs(pd_b_p12 - 0.0148886) < 1e-5

    cva_p12 = 0.60 * df_half * ee_p12 * pd_c_p12
    dva_p12 = 0.60 * df_half * ene_p12 * pd_b_p12
    assert abs(cva_p12 - 8_690.65) < 1.0
    assert abs(dva_p12 - 2_626.78) < 1.0
    net_p12 = dva_p12 - cva_p12
    assert abs(net_p12 - (-6_063.87)) < 1.0

    print("Verifying Problem 13: PCA Yield Curve Factor Shocks...")
    lambdas = [0.000180, 0.000018, 0.000002]
    tot_var = sum(lambdas)
    assert abs(tot_var - 0.000200) < 1e-9
    pcts = [lam / tot_var for lam in lambdas]
    assert abs(pcts[0] - 0.90) < 1e-6
    assert abs(pcts[1] - 0.09) < 1e-6
    assert abs(pcts[2] - 0.01) < 1e-6

    sigma_level = math.sqrt(lambdas[0])
    assert abs(sigma_level - 0.0134164) < 1e-5
    shock_level = 1.50 * sigma_level * 0.577
    assert abs(shock_level - 0.011612) < 1e-4  # +116.1 bps

    print("Verifying Problem 14: Funding Valuation Adjustment (FVA)...")
    ee_p14 = 400_000.0
    s_fund_p14 = 0.0075
    df_p14 = 0.945
    t_p14 = 3.0
    fca_p14 = s_fund_p14 * ee_p14 * df_p14 * t_p14
    assert abs(fca_p14 - 8_505.0) < 1e-6

    print("Verifying Problem 15: Margin Valuation Adjustment (MVA)...")
    im_p15 = 2_000_000.0
    s_margin_p15 = 0.0120
    df_p15 = 0.910
    t_p15 = 5.0
    mva_p15 = s_margin_p15 * im_p15 * df_p15 * t_p15
    assert abs(mva_p15 - 109_200.0) < 1e-6

    print("Verifying Problem 16: Capital Valuation Adjustment (KVA)...")
    capital_p16 = 500_000.0
    coc_p16 = 0.100
    df_p16 = 0.910
    t_p16 = 5.0
    kva_p16 = coc_p16 * capital_p16 * df_p16 * t_p16
    assert abs(kva_p16 - 227_500.0) < 1e-6

    print("All 16 problems in Note 17 verified with exact numerical precision!")


if __name__ == "__main__":
    run_all_problem_set_assertions()
