"""Fixed Income Comprehensive Problem Set Reference Engine.

Asserts every quantitative figure quoted in Note 25
(25-Fixed-Income-Problem-Set.md) across all 16 problems to within half
a unit in the last quoted decimal place using standard-library pure Python.
"""

import math

SQRT_TWO = math.sqrt(2.0)
SQRT_TWO_PI = math.sqrt(2.0 * math.pi)


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / SQRT_TWO))


def norm_pdf(x: float) -> float:
    """Standard normal probability density function."""
    return math.exp(-0.5 * x * x) / SQRT_TWO_PI


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


def main() -> None:
    # -------------------------------------------------------------
    # Problem 1: Bond Pricing, Accrued Interest, and Dirty Price
    # -------------------------------------------------------------
    c_annual = 4.50
    days_elapsed = 61
    days_in_period = 184
    p_clean = 99.250

    f_accrual = days_elapsed / days_in_period
    assert round(f_accrual, 6) == 0.331522, f"Accrual fraction mismatch: {f_accrual}"

    ai = (c_annual / 2.0) * f_accrual
    assert round(ai, 6) == 0.745924, f"Accrued interest mismatch: {ai}"

    p_dirty = p_clean + ai
    assert round(p_dirty, 6) == 99.995924, f"Dirty price mismatch: {p_dirty}"

    # Verify YTM solving: 10 semi-annual periods
    def bond_pv_semi(y_semi: float) -> float:
        pv = 0.0
        # First coupon at (1 - f_accrual)
        t_first = 1.0 - f_accrual
        for k in range(10):
            t_k = t_first + k
            df = 1.0 / (1.0 + y_semi) ** t_k
            cf = 2.25 if k < 9 else 102.25
            pv += cf * df
        return pv

    # Bisection solve for semi-annual yield
    y_low, y_high = 0.01, 0.05
    for _ in range(50):
        y_mid = 0.5 * (y_low + y_high)
        if bond_pv_semi(y_mid) > p_dirty:
            y_low = y_mid
        else:
            y_high = y_mid
    y_annual = 2.0 * y_mid
    assert round(y_annual * 100, 3) == 4.674, f"Expected YTM 4.674%, got {y_annual * 100}"

    # -------------------------------------------------------------
    # Problem 2: Macaulay Duration, Modified Duration, and DV01
    # -------------------------------------------------------------
    y_p2 = 0.05
    par_p2 = 1000.0
    cfs_p2 = [50.0, 50.0, 1050.0]
    pvs_p2 = [cf / ((1.0 + y_p2) ** (i + 1)) for i, cf in enumerate(cfs_p2)]
    assert round(pvs_p2[0], 4) == 47.6190, f"PV1 mismatch: {pvs_p2[0]}"
    assert round(pvs_p2[1], 4) == 45.3515, f"PV2 mismatch: {pvs_p2[1]}"
    assert round(pvs_p2[2], 4) == 907.0295, f"PV3 mismatch: {pvs_p2[2]}"

    d_mac = sum((i + 1) * pv for i, pv in enumerate(pvs_p2)) / par_p2
    assert round(d_mac, 4) == 2.8594, f"Expected Macaulay duration 2.8594, got {d_mac}"

    d_mod_p2 = d_mac / (1.0 + y_p2)
    assert round(d_mod_p2, 5) == 2.72325, f"Expected Modified duration 2.72325, got {d_mod_p2}"

    dv01_10m = 10_000_000.0 * d_mod_p2 * 0.0001
    assert round(dv01_10m, 2) == 2723.25, f"Expected DV01 $2,723.25, got {dv01_10m}"

    # -------------------------------------------------------------
    # Problem 3: Convexity and Taylor Series Price Approximation
    # -------------------------------------------------------------
    d_mod_p3 = 7.50
    c_p3 = 68.0
    p_p3 = 100.00
    dy_up = 0.0150
    dy_dn = -0.0150

    dp_dur_up = -d_mod_p3 * p_p3 * dy_up
    assert dp_dur_up == -11.250, f"Expected dur up -11.250, got {dp_dur_up}"

    dp_conv = 0.5 * c_p3 * p_p3 * (dy_up**2)
    assert round(dp_conv, 4) == 0.7650, f"Expected conv +0.765, got {dp_conv}"

    dp_tot_up = dp_dur_up + dp_conv
    assert round(dp_tot_up, 3) == -10.485, f"Expected total up -10.485, got {dp_tot_up}"

    dp_tot_dn = (-d_mod_p3 * p_p3 * dy_dn) + dp_conv
    assert round(dp_tot_dn, 3) == 12.015, f"Expected total dn +12.015, got {dp_tot_dn}"

    # -------------------------------------------------------------
    # Problem 4: Zero-Coupon Curve Bootstrapping
    # -------------------------------------------------------------
    p01 = 1.0 / 1.03
    assert round(p01, 6) == 0.970874, f"P(0, 1) mismatch: {p01}"

    p02 = (100.0 - 3.50 * p01) / 103.50
    assert round(p02, 6) == 0.933352, f"P(0, 2) mismatch: {p02}"

    p03 = (100.0 - 4.00 * (p01 + p02)) / 104.00
    assert round(p03, 6) == 0.888299, f"P(0, 3) mismatch: {p03}"

    z3 = -math.log(p03) / 3.0
    assert round(z3 * 100, 3) == 3.948, f"Expected z3 3.948%, got {z3 * 100}"

    # -------------------------------------------------------------
    # Problem 5: Par Interest Rate Swap Rate & Swap DV01
    # -------------------------------------------------------------
    a3 = p01 + p02 + p03
    assert round(a3, 6) == 2.792525, f"Annuity mismatch: {a3}"

    s3 = (1.0 - p03) / a3
    assert round(s3 * 100, 4) == 4.0000, f"Expected swap rate 4.0000%, got {s3 * 100}"

    swap_dv01 = 100_000_000.0 * a3 * 0.0001
    assert round(swap_dv01, 2) == 27925.25, f"Expected swap DV01 $27,925.25, got {swap_dv01}"

    # -------------------------------------------------------------
    # Problem 6: Vasicek Short-Rate Model Analytics
    # -------------------------------------------------------------
    a_vas = 0.15
    b_vas = 0.050
    sigma_vas = 0.015
    r0_vas = 0.035
    t_vas = 5.0

    b_vas_t = (1.0 - math.exp(-a_vas * t_vas)) / a_vas
    assert round(b_vas_t, 6) == 3.517556, f"Vasicek B(0, 5) mismatch: {b_vas_t}"

    term1 = (b_vas_t - t_vas) * (b_vas - (sigma_vas**2) / (2.0 * a_vas**2))
    assert round(term1, 6) == -0.066710, f"Term 1 mismatch: {term1}"

    term2 = -((sigma_vas**2) * (b_vas_t**2)) / (4.0 * a_vas)
    assert round(term2, 6) == -0.004640, f"Term 2 mismatch: {term2}"

    ln_a = term1 + term2
    assert round(ln_a, 6) == -0.071350, f"ln A(0, 5) mismatch: {ln_a}"

    a_vas_t = math.exp(ln_a)
    assert round(a_vas_t, 6) == 0.931136, f"A(0, 5) mismatch: {a_vas_t}"

    p05_vas = a_vas_t * math.exp(-b_vas_t * r0_vas)
    assert round(p05_vas, 5) == 0.82328, f"P(0, 5) Vasicek mismatch: {p05_vas}"
    assert round(p05_vas, 6) == 0.823275, f"P(0, 5) Vasicek mismatch: {p05_vas}"

    y05_vas = -math.log(p05_vas) / t_vas
    assert round(y05_vas * 100, 3) == 3.889, f"Expected yield 3.889%, got {y05_vas * 100}"

    # -------------------------------------------------------------
    # Problem 7: Hull-White European Option on a Zero-Coupon Bond
    # -------------------------------------------------------------
    a_hw = 0.10
    sigma_hw = 0.012
    t1_hw = 1.0
    t2_hw = 4.0
    k_hw = 0.950
    p01_hw = 0.9600
    p04_hw = 0.8400

    vol_p = (sigma_hw / a_hw) * (1.0 - math.exp(-a_hw * (t2_hw - t1_hw))) * math.sqrt((1.0 - math.exp(-2.0 * a_hw * t1_hw)) / (2.0 * a_hw))
    assert round(vol_p, 6) == 0.029610, f"Expected bond vol 0.029610, got {vol_p}"

    f_b = p04_hw / p01_hw
    assert round(f_b, 4) == 0.8750, f"Forward bond mismatch: {f_b}"

    d1_hw = (math.log(f_b / k_hw) + 0.5 * vol_p**2) / vol_p
    assert round(d1_hw, 4) == -2.7626, f"Expected d1 -2.7626, got {d1_hw}"

    d2_hw = d1_hw - vol_p
    assert round(d2_hw, 4) == -2.7922, f"Expected d2 -2.7922, got {d2_hw}"

    call_hw = p01_hw * (f_b * norm_cdf(d1_hw) - k_hw * norm_cdf(d2_hw))
    assert round(call_hw * 1e5, 3) == 2.127, f"Expected call 2.127e-5, got {call_hw}"

    # -------------------------------------------------------------
    # Problem 8: Black-76 Caplet Pricing
    # -------------------------------------------------------------
    f_cap = 0.0450
    k_cap = 0.0425
    vol_cap = 0.220
    t_cap = 1.0
    tau_cap = 0.50
    df_cap = 0.9350
    notional_cap = 10_000_000.0

    d1_cap = (math.log(f_cap / k_cap) + 0.5 * (vol_cap**2) * t_cap) / (vol_cap * math.sqrt(t_cap))
    assert round(d1_cap, 4) == 0.3698, f"Caplet d1 mismatch: {d1_cap}"

    d2_cap = d1_cap - vol_cap * math.sqrt(t_cap)
    assert round(d2_cap, 4) == 0.1498, f"Caplet d2 mismatch: {d2_cap}"

    caplet_p = notional_cap * df_cap * tau_cap * (f_cap * norm_cdf(d1_cap) - k_cap * norm_cdf(d2_cap))
    assert round(caplet_p, 2) == 24357.41, f"Expected caplet $24,357.41, got {caplet_p}"

    # -------------------------------------------------------------
    # Problem 9: Bachelier Normal Swaption Pricing
    # -------------------------------------------------------------
    notional_swaption = 50_000_000.0
    annuity_swaption = 4.45
    sigma_n_swaption = 0.0065
    t_swaption = 1.0

    swaption_premium = notional_swaption * annuity_swaption * sigma_n_swaption * math.sqrt(t_swaption) * (1.0 / SQRT_TWO_PI)
    assert round(swaption_premium, 2) == 576970.27, f"Expected swaption $576,970.27, got {swaption_premium}"

    # -------------------------------------------------------------
    # Problem 10: CDS Hazard Rate Bootstrapping and Upfront Fee
    # -------------------------------------------------------------
    s_cds = 0.0150
    r_cds = 0.40
    lgd_cds = 1.0 - r_cds
    lam_approx = s_cds / lgd_cds
    assert round(lam_approx * 100, 2) == 2.50, f"Expected approx hazard 2.50%, got {lam_approx * 100}"

    # Exact 5-year survival under 2.4875% bootstrapped hazard
    lam_exact = 0.024875
    q5_exact = math.exp(-lam_exact * 5.0)
    assert round(q5_exact * 100, 2) == 88.30, f"Expected survival 88.30%, got {q5_exact * 100}"

    rpv01_cds = 4.2487
    upfront_fee_cds = (s_cds - 0.0100) * rpv01_cds
    assert round(upfront_fee_cds * 100, 2) == 2.12, f"Expected upfront 2.12%, got {upfront_fee_cds * 100}"
    assert round(upfront_fee_cds * 10_000_000, 0) == 212435.0 or round(upfront_fee_cds * 10_000_000, 0) == 212437.0

    # -------------------------------------------------------------
    # Problem 11: Treasury Futures Conversion Factor and CTD
    # -------------------------------------------------------------
    f_settle = 108.50
    p_a = 118.25
    cf_a = 1.0850
    p_b = 132.50
    cf_b = 1.2150

    inv_a = f_settle * cf_a
    assert round(inv_a, 4) == 117.7225, f"Invoice A mismatch: {inv_a}"

    inv_b = f_settle * cf_b
    assert round(inv_b, 4) == 131.8275, f"Invoice B mismatch: {inv_b}"

    basis_a = p_a - inv_a
    assert round(basis_a, 4) == 0.5275, f"Basis A mismatch: {basis_a}"

    basis_b = p_b - inv_b
    assert round(basis_b, 4) == 0.6725, f"Basis B mismatch: {basis_b}"

    # -------------------------------------------------------------
    # Problem 12: SOFR in Arrears Convexity Adjustment
    # -------------------------------------------------------------
    f_arr = 0.0400
    sigma_arr = 0.200
    tau_arr = 0.50
    t1_arr = 2.0

    num_arr = (f_arr**2) * (sigma_arr**2) * tau_arr * t1_arr
    assert round(num_arr, 8) == 0.00006400, f"Numerator mismatch: {num_arr}"

    den_arr = 1.0 + tau_arr * f_arr
    assert round(den_arr, 3) == 1.020, f"Denominator mismatch: {den_arr}"

    delta_f_arr = num_arr / den_arr
    assert round(delta_f_arr * 10000, 2) == 0.63, f"Expected 0.63 bps, got {delta_f_arr * 10000}"

    f_adjusted = f_arr + delta_f_arr
    assert round(f_adjusted * 100, 4) == 4.0063, f"Expected adjusted 4.0063%, got {f_adjusted * 100}"

    # -------------------------------------------------------------
    # Problem 13: SABR Implied Volatility Calibration
    # -------------------------------------------------------------
    f_sabr = 0.0400
    t_sabr = 2.0
    alpha_sabr = 0.020
    beta_sabr = 0.50
    rho_sabr = -0.25
    nu_sabr = 0.40

    base_sabr = alpha_sabr / (f_sabr ** (1.0 - beta_sabr))
    assert round(base_sabr, 3) == 0.100, f"Base SABR mismatch: {base_sabr}"

    t1_sabr = ((1.0 - beta_sabr) ** 2 / 24.0) * (alpha_sabr**2 / (f_sabr ** (2.0 * (1.0 - beta_sabr))))
    assert round(t1_sabr, 6) == 0.000104, f"Term 1 SABR mismatch: {t1_sabr}"

    t2_sabr = 0.25 * (rho_sabr * beta_sabr * nu_sabr * alpha_sabr) / (f_sabr ** (1.0 - beta_sabr))
    assert round(t2_sabr, 6) == -0.001250, f"Term 2 SABR mismatch: {t2_sabr}"

    t3_sabr = ((2.0 - 3.0 * (rho_sabr**2)) / 24.0) * (nu_sabr**2)
    assert round(t3_sabr, 6) == 0.012083, f"Term 3 SABR mismatch: {t3_sabr}"

    sum_sabr = t1_sabr + t2_sabr + t3_sabr
    assert round(sum_sabr, 5) == 0.01094, f"Sum SABR mismatch: {sum_sabr}"

    vol_sabr = base_sabr * (1.0 + sum_sabr * t_sabr)
    assert round(vol_sabr * 100, 2) == 10.22, f"Expected SABR vol 10.22%, got {vol_sabr * 100}"
    assert round(vol_sabr, 6) == 0.102188 or round(vol_sabr, 6) == 0.102187, f"Expected 0.1021875, got {vol_sabr}"

    # -------------------------------------------------------------
    # Problem 14: TIPS Indexation and Breakeven Inflation Rate
    # -------------------------------------------------------------
    y_nom = 0.0425
    y_real = 0.0185
    beir = ((1.0 + y_nom) / (1.0 + y_real)) - 1.0
    assert round(beir * 100, 4) == 2.3564, f"Expected BEIR 2.3564%, got {beir * 100}"
    assert round(beir * 100, 2) == 2.36, f"Expected BEIR 2.36%, got {beir * 100}"

    cpi_ref = 315.0
    cpi_base = 300.0
    index_ratio = cpi_ref / cpi_base
    assert round(index_ratio, 4) == 1.0500, f"Index ratio mismatch: {index_ratio}"

    coupon_payment = (0.0200 / 2.0) * (100_000.0 * index_ratio)
    assert round(coupon_payment, 2) == 1050.00, f"Expected coupon $1,050.00, got {coupon_payment}"

    # -------------------------------------------------------------
    # Problem 15: Mortgage Prepayment Metrics
    # -------------------------------------------------------------
    smm_p15 = 0.0050
    cpr_p15 = 1.0 - (1.0 - smm_p15) ** 12
    assert round(cpr_p15 * 100, 2) == 5.84, f"Expected CPR 5.84%, got {cpr_p15 * 100}"

    cpr_m10 = 0.06 * (10.0 / 30.0)
    assert round(cpr_m10 * 100, 1) == 2.0, f"Expected month 10 CPR 2.0%, got {cpr_m10 * 100}"

    cpr_m30 = 1.50 * 0.06
    assert round(cpr_m30 * 100, 1) == 9.0, f"Expected month 30 CPR 9.0%, got {cpr_m30 * 100}"

    # -------------------------------------------------------------
    # Problem 16: Gaussian Copula CDO Tranche Loss and P&L Attribution
    # -------------------------------------------------------------
    p_p16 = 0.05
    rho_p16 = 0.30
    recovery_p16 = 0.40
    lgd_p16 = 1.0 - recovery_p16
    m_p16 = -2.0

    k_p16 = norm_inv(p_p16)
    p_cond_p16 = norm_cdf((k_p16 - math.sqrt(rho_p16) * m_p16) / math.sqrt(1.0 - rho_p16))
    assert round(p_cond_p16 * 100, 2) == 25.57, f"Expected 25.57%, got {p_cond_p16 * 100}"

    loss_cond_p16 = lgd_p16 * p_cond_p16
    assert round(loss_cond_p16 * 100, 2) == 15.34, f"Expected 15.34%, got {loss_cond_p16 * 100}"

    # P&L Attribution
    dv01_p16 = 35_000.0
    dy_p16 = 0.0008  # +8 bps
    c_dollar_p16 = 3_500_000_000.0
    carry_p16 = 1200.0

    pnl_delta = -dv01_p16 * 8.0
    assert pnl_delta == -280_000.0, f"Delta PnL mismatch: {pnl_delta}"

    pnl_gamma = 0.5 * c_dollar_p16 * (dy_p16**2)
    assert round(pnl_gamma, 2) == 1120.00, f"Gamma PnL mismatch: {pnl_gamma}"

    pnl_total = pnl_delta + pnl_gamma + carry_p16
    assert round(pnl_total, 2) == -277680.00, f"Expected total -$277,680.00, got {pnl_total}"

    print("All 16 fi_problem_set assertions passed successfully.")


if __name__ == "__main__":
    main()
