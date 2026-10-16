"""Basel Credit Risk Capital and SA-CCR Analytics Reference Implementation.

Pure Python 3.10+ standard library implementation:
1. Vasicek Asymptotic Single Risk Factor (ASRF) Credit Risk Capital Model (Basel IRB).
2. Standardised Approach for Counterparty Credit Risk (SA-CCR, Basel CRE52).
3. Basic Approach for CVA Capital (BA-CVA, Basel CRE54).
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_ppf(p: float) -> float:
    """Inverse standard normal cumulative distribution function (quantile).

    Acklam's rational approximation with absolute error < 1.15e-9.
    """
    if p <= 0.0 or p >= 1.0:
        raise ValueError("Probability p must be in (0, 1)")

    # Coefficients in rational approximations
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

    # Limits of central region
    p_low = 0.02425
    p_high = 1.0 - p_low

    if p < p_low:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0
        )
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        return ((((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q) / (
            ((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0
        )
    else:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0
        )


# ============================================================================
# 1. Vasicek ASRF Model (Basel IRB Capital)
# ============================================================================


@dataclass
class VasicekResult:
    pd: float
    lgd: float
    maturity: float
    asset_correlation: float
    conditional_pd: float
    maturity_adj: float
    capital_requirement_k: float  # Capital charge per dollar EAD
    rwa: float  # Risk-Weighted Assets


def calculate_vasicek_irb(
    pd: float,
    lgd: float,
    maturity: float = 2.5,
    ead: float = 1_000_000.0,
    confidence: float = 0.999,
    firm_size_m_eur: float = 50.0,  # Turnover >= 50M EUR -> large corporate
) -> VasicekResult:
    """Calculate Basel IRB credit risk capital requirement under Vasicek ASRF model.

    Implements Basel CRE31 corporate/bank/sovereign formulas:
    - Asset correlation rho(PD) with exponential decay between 12% and 24%.
    - Maturity adjustment factor b(PD).
    - 99.9% 1-year conditional default probability.
    - Capital requirement K = [LGD * CondPD - LGD * PD] * MaturityAdj.
    - RWA = K * 12.5 * EAD.
    """
    if pd <= 0.0 or pd >= 1.0:
        raise ValueError(f"PD must be in (0, 1), got {pd}")
    if lgd <= 0.0 or lgd > 1.0:
        raise ValueError(f"LGD must be in (0, 1], got {lgd}")

    # 1. Asset Correlation rho(PD)
    exp_factor = (1.0 - math.exp(-50.0 * pd)) / (1.0 - math.exp(-50.0))
    rho = 0.12 * exp_factor + 0.24 * (1.0 - exp_factor)

    # Firm-size adjustment for SME (turnover S between 5M and 50M EUR)
    if firm_size_m_eur < 50.0:
        s_clamped = max(5.0, firm_size_m_eur)
        sme_adj = 0.04 * (1.0 - (s_clamped - 5.0) / 45.0)
        rho -= sme_adj

    # 2. Maturity adjustment b(PD) and maturity multiplier
    b = (0.11852 - 0.05478 * math.log(pd)) ** 2
    mat_adj = (1.0 + (maturity - 2.5) * b) / (1.0 - 1.5 * b)

    # 3. Conditional default probability under 99.9% systemic factor shock
    z_alpha = norm_ppf(confidence)
    numerator = norm_ppf(pd) + math.sqrt(rho) * z_alpha
    denominator = math.sqrt(1.0 - rho)
    conditional_pd = norm_cdf(numerator / denominator)

    # 4. Capital requirement K (per unit EAD)
    k = (lgd * conditional_pd - lgd * pd) * mat_adj
    k = max(0.0, k)

    # 5. Risk-Weighted Assets (RWA = K * 12.5 * EAD)
    rwa = k * 12.5 * ead

    return VasicekResult(
        pd=pd,
        lgd=lgd,
        maturity=maturity,
        asset_correlation=rho,
        conditional_pd=conditional_pd,
        maturity_adj=mat_adj,
        capital_requirement_k=k,
        rwa=rwa,
    )


# ============================================================================
# 2. Standardised Approach for Counterparty Credit Risk (SA-CCR, Basel CRE52)
# ============================================================================


@dataclass
class SACCRTrade:
    asset_class: str  # 'IR' or 'FX'
    notional: float
    supervisory_delta: float  # +1.0 for payer/long, -1.0 for receiver/short
    start_time: float  # in years
    end_time: float  # in years
    maturity: float  # residual maturity M_i in years
    currency_pair: str | None = None


@dataclass
class SACCRNettingSet:
    trades: list[SACCRTrade]
    is_margined: bool
    current_mtm: float  # Current portfolio mark-to-market V
    collateral: float  # Current collateral C held by bank
    threshold: float = 0.0  # Collateral threshold TH
    mta: float = 0.0  # Minimum Transfer Amount MTA
    nica: float = 0.0  # Net Independent Collateral Amount
    mpor_days: int = 10  # Margin Period of Risk in business days


@dataclass
class SACCRResult:
    replacement_cost: float
    pfe_multiplier: float
    addon_ir: float
    addon_fx: float
    addon_aggregate: float
    pfe: float
    ead: float


def calculate_saccr(netting_set: SACCRNettingSet) -> SACCRResult:
    """Calculate SA-CCR Exposure at Default (EAD) under Basel CRE52.

    EAD = 1.4 * (RC + PFE)
    where:
    - RC is Replacement Cost under margined or unmargined CSA.
    - PFE = Multiplier * AddOn_aggregate.
    - AddOn computed across Interest Rate and FX hedging sets.
    """
    v = netting_set.current_mtm
    c = netting_set.collateral

    # 1. Replacement Cost (RC)
    if not netting_set.is_margined:
        rc = max(0.0, v - c)
    else:
        th = netting_set.threshold
        mta = netting_set.mta
        nica = netting_set.nica
        rc = max(0.0, v - c, th + mta - nica)

    # 2. AddOn Calculation
    # Interest Rate Hedging Set: 3 maturity buckets (<1y, 1-5y, >5y)
    # Supervisory factor SF = 0.50%
    sf_ir = 0.0050
    # Buckets: 1: M <= 1, 2: 1 < M <= 5, 3: M > 5
    bucket_d = [0.0, 0.0, 0.0]

    for t in netting_set.trades:
        if t.asset_class == "IR":
            # Adjusted notional: d_i = Notional * [exp(-0.05*S) - exp(-0.05*E)] / 0.05
            duration_factor = (math.exp(-0.05 * t.start_time) - math.exp(-0.05 * t.end_time)) / 0.05
            adj_notional = t.notional * duration_factor

            # Maturity factor MF
            if netting_set.is_margined:
                # Margined MF = 1.5 * sqrt(MPOR / 250)
                mf = 1.5 * math.sqrt(netting_set.mpor_days / 250.0)
            else:
                # Unmargined MF floors residual maturity at 10 business days.
                mf = math.sqrt(min(max(t.maturity, 10.0 / 250.0), 1.0))

            eff_notional = adj_notional * t.supervisory_delta * mf

            if t.end_time <= 1.0:
                bucket_d[0] += eff_notional
            elif t.end_time <= 5.0:
                bucket_d[1] += eff_notional
            else:
                bucket_d[2] += eff_notional

    # Effective bucket AddOns
    a1 = sf_ir * abs(bucket_d[0])
    a2 = sf_ir * abs(bucket_d[1])
    a3 = sf_ir * abs(bucket_d[2])

    # Hedging set correlation aggregation across buckets:
    # AddOn_IR = sqrt(A1^2 + A2^2 + A3^2 + 1.4*A1*A2 + 1.4*A2*A3 + 0.6*A1*A3)
    addon_ir_sq = a1**2 + a2**2 + a3**2 + 1.4 * a1 * a2 + 1.4 * a2 * a3 + 0.6 * a1 * a3
    addon_ir = math.sqrt(max(0.0, addon_ir_sq))

    # Foreign Exchange Hedging Set: SF = 4.0%
    sf_fx = 0.040
    eff_fx_notionals: dict[str, float] = {}
    for t in netting_set.trades:
        if t.asset_class == "FX":
            if not t.currency_pair:
                raise ValueError("FX trades must specify a currency pair")
            if netting_set.is_margined:
                mf = 1.5 * math.sqrt(netting_set.mpor_days / 250.0)
            else:
                mf = math.sqrt(min(max(t.maturity, 10.0 / 250.0), 1.0))
            eff_fx_notionals[t.currency_pair] = eff_fx_notionals.get(t.currency_pair, 0.0) + t.notional * t.supervisory_delta * mf

    addon_fx = sf_fx * sum(abs(notional) for notional in eff_fx_notionals.values())

    addon_aggregate = addon_ir + addon_fx

    # 3. PFE Multiplier
    # Multiplier = min(1.0, 0.05 + 0.95 * exp((V - C) / (2 * 0.95 * AddOn)))
    v_minus_c = v - c
    if addon_aggregate > 0.0:
        exp_arg = v_minus_c / (2.0 * 0.95 * addon_aggregate)
        # Numerical safeguard against math overflow
        exp_arg = min(exp_arg, 50.0)
        multiplier = min(1.0, 0.05 + 0.95 * math.exp(exp_arg))
    else:
        multiplier = 1.0

    pfe = multiplier * addon_aggregate

    # 4. Exposure at Default (alpha = 1.4)
    alpha = 1.4
    ead = alpha * (rc + pfe)

    return SACCRResult(
        replacement_cost=rc,
        pfe_multiplier=multiplier,
        addon_ir=addon_ir,
        addon_fx=addon_fx,
        addon_aggregate=addon_aggregate,
        pfe=pfe,
        ead=ead,
    )


# ============================================================================
# 3. Basic Approach for CVA Capital (BA-CVA, Basel CRE54)
# ============================================================================


@dataclass
class CounterpartyCVARecord:
    counterparty_name: str
    rating_bucket: int  # 1 to 6 (1: AAA/AA, 2: A, 3: BBB, 4: BB, 5: B, 6: CCC)
    ead: float
    effective_maturity: float  # M_c in years


def calculate_reduced_ba_cva(
    counterparties: Sequence[CounterpartyCVARecord],
    alpha: float = 1.4,
) -> float:
    """Calculate Reduced Basic Approach for CVA Capital (BA-CVA) under Basel CRE54.

    K_CVA_reduced = sqrt( (rho * sum S_cva)^2 + (1 - rho^2) * sum S_cva^2 )
    where rho = 0.50, and S_cva,c = RW_c * (M_c / alpha) * EAD_c * DF_c.
    Supervisory risk weights RW_c:
    - Bucket 1 (AAA/AA): 0.50%
    - Bucket 2 (A): 0.70%
    - Bucket 3 (BBB): 1.00%
    - Bucket 4 (BB): 2.00%
    - Bucket 5 (B): 4.00%
    - Bucket 6 (CCC): 8.00%
    """
    rw_table = {
        1: 0.0050,
        2: 0.0070,
        3: 0.0100,
        4: 0.0200,
        5: 0.0400,
        6: 0.0800,
    }

    rho = 0.50
    s_cva_list: list[float] = []

    for c in counterparties:
        if c.rating_bucket not in rw_table:
            raise ValueError(f"Unsupported rating bucket: {c.rating_bucket}")
        rw = rw_table[c.rating_bucket]
        # Discount factor DF_c = (1 - exp(-0.05 * M_c)) / (0.05 * M_c)
        m = max(0.1, c.effective_maturity)
        df = (1.0 - math.exp(-0.05 * m)) / (0.05 * m)
        s_c = rw * (m / alpha) * c.ead * df
        s_cva_list.append(s_c)

    sum_s = sum(s_cva_list)
    sum_sq_s = sum(s**2 for s in s_cva_list)

    k_cva = math.sqrt((rho * sum_s) ** 2 + (1.0 - rho**2) * sum_sq_s)
    return k_cva


# ============================================================================
# 4. Verification Tests
# ============================================================================


def run_tests() -> None:
    print("Testing Basel Credit Capital, SA-CCR, and BA-CVA Analytics...")

    # 1. Vasicek ASRF Model Test
    # Test Corporate: PD = 1.0%, LGD = 45% (Standard FIRB), M = 2.5 years, EAD = $10,000,000
    res = calculate_vasicek_irb(
        pd=0.010,
        lgd=0.45,
        maturity=2.5,
        ead=10_000_000.0,
        confidence=0.999,
        firm_size_m_eur=50.0,
    )
    # Expected rho(0.01):
    exp_factor = (1.0 - math.exp(-0.50)) / (1.0 - math.exp(-50.0))
    expected_rho = 0.12 * exp_factor + 0.24 * (1.0 - exp_factor)
    assert math.isclose(res.asset_correlation, expected_rho, rel_tol=1e-4)

    # Maturity adjustment at M=1.0 is exactly 1.0: (1 + (1 - 2.5)*b) / (1 - 1.5*b) = (1 - 1.5*b)/(1 - 1.5*b) = 1.0
    res_1y = calculate_vasicek_irb(
        pd=0.010,
        lgd=0.45,
        maturity=1.0,
        ead=10_000_000.0,
    )
    assert math.isclose(res_1y.maturity_adj, 1.0, rel_tol=1e-5)
    # At M=2.5: mat_adj = 1.0 / (1.0 - 1.5 * b) > 1.0
    assert res.maturity_adj > 1.0

    # Conditional PD check: Z=3.09023, PD=0.01 -> Phi^-1(0.01) = -2.32635
    print(f"Corporate (PD=1.0%, LGD=45%): Asset Correlation={res.asset_correlation:.4f}")
    print(f"99.9% Conditional PD={res.conditional_pd:.4f}, Capital K={res.capital_requirement_k:.4%}")
    print(f"Total RWA=${res.rwa:,.2f} ({(res.rwa / 10_000_000.0):.2%} of EAD)")
    assert 0.05 < res.capital_requirement_k < 0.15, "Corporate K must be between 5% and 15%"
    assert math.isclose(res.capital_requirement_k, 0.07385344097, rel_tol=1e-8)
    assert res.rwa > 0.0

    # 2. SA-CCR Netting Set Test
    # Netting set with 2 IR swaps:
    # Trade 1: 5-year payer swap (Notional $10M, delta = +1.0)
    # Trade 2: 2-year receiver swap (Notional $10M, delta = -1.0)
    # Uncollateralized, V = $200k, C = $0
    trade1 = SACCRTrade(
        asset_class="IR",
        notional=10_000_000.0,
        supervisory_delta=1.0,
        start_time=0.0,
        end_time=5.0,
        maturity=5.0,
    )
    trade2 = SACCRTrade(
        asset_class="IR",
        notional=10_000_000.0,
        supervisory_delta=-1.0,
        start_time=0.0,
        end_time=2.0,
        maturity=2.0,
    )
    netting_set_uncol = SACCRNettingSet(
        trades=[trade1, trade2],
        is_margined=False,
        current_mtm=200_000.0,
        collateral=0.0,
    )
    saccr_res = calculate_saccr(netting_set_uncol)
    assert saccr_res.replacement_cost == 200_000.0
    assert 0.0 < saccr_res.pfe_multiplier <= 1.0
    assert saccr_res.addon_ir > 0.0
    print(f"SA-CCR Unmargined: RC=${saccr_res.replacement_cost:,.2f}, PFE Multiplier={saccr_res.pfe_multiplier:.4f}")
    print(f"AddOn IR=${saccr_res.addon_ir:,.2f}, Total EAD=${saccr_res.ead:,.2f}")

    short_fx_trades = [
        SACCRTrade("FX", 10_000_000.0, 1.0, 0.0, 0.0, 5.0 / 250.0, "EUR/USD"),
        SACCRTrade("FX", 10_000_000.0, -1.0, 0.0, 0.0, 5.0 / 250.0, "USD/JPY"),
    ]
    fx_result = calculate_saccr(SACCRNettingSet(short_fx_trades, False, 0.0, 0.0))
    assert math.isclose(fx_result.addon_fx, 160_000.0)

    # Margined netting set: C = $180k, TH = $50k, MTA = $10k
    netting_set_col = SACCRNettingSet(
        trades=[trade1, trade2],
        is_margined=True,
        current_mtm=200_000.0,
        collateral=180_000.0,
        threshold=50_000.0,
        mta=10_000.0,
        mpor_days=10,
    )
    saccr_col_res = calculate_saccr(netting_set_col)
    # RC = max(200k - 180k, 50k + 10k) = max(20k, 60k) = 60k
    assert saccr_col_res.replacement_cost == 60_000.0
    # Margined EAD must be significantly smaller than unmargined EAD due to MPOR factor 0.3
    assert saccr_col_res.ead < saccr_res.ead
    print(f"SA-CCR Margined: RC=${saccr_col_res.replacement_cost:,.2f}, Total EAD=${saccr_col_res.ead:,.2f}")

    # 3. BA-CVA Capital Test
    c1 = CounterpartyCVARecord(
        counterparty_name="Bank A",
        rating_bucket=2,  # Rating A -> RW = 0.70%
        ead=saccr_res.ead,
        effective_maturity=3.0,
    )
    c2 = CounterpartyCVARecord(
        counterparty_name="Corporate B",
        rating_bucket=3,  # Rating BBB -> RW = 1.00%
        ead=5_000_000.0,
        effective_maturity=2.5,
    )
    k_cva = calculate_reduced_ba_cva([c1, c2], alpha=1.4)
    assert k_cva > 0.0
    assert math.isclose(k_cva, 85_741.56948, rel_tol=1e-8)
    print(f"Reduced BA-CVA Capital Requirement: ${k_cva:,.2f}")

    print("All Basel credit capital, SA-CCR, and BA-CVA tests passed successfully!")


if __name__ == "__main__":
    run_tests()
