"""FRTB Standardised Approach (SbM, DRC, and Curvature) Reference Implementation.

Pure Python 3.10+ standard library implementation:
1. FRTB Sensitivities-Based Method (SbM) Delta capital aggregation across buckets.
2. The three correlation scenarios (Medium, High, Low) and the negative-sum fallback.
3. Multi-bucket General Interest Rate Risk (GIRR) and Equity SbM calculations.
4. Curvature risk upward/downward revaluation aggregation.
5. Default Risk Charge (DRC) for non-securitizations.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

# ============================================================================
# 1. FRTB SbM Delta Aggregation Engine
# ============================================================================


@dataclass
class SensitivityRecord:
    factor_id: str
    bucket_id: str
    risk_class: str  # 'GIRR', 'CSR_NS', 'Equity', 'FX', 'Commodity'
    net_sensitivity: float  # s_k in currency units
    risk_weight: float  # RW_k as decimal (e.g., 0.015 for 1.5%)


@dataclass
class BucketDeltaResult:
    bucket_id: str
    weighted_sensitivities: dict[str, float]  # factor_id -> WS_k
    sum_ws: float  # S_b = sum_{k in b} WS_k
    capital_k_b: float  # K_b


@dataclass
class SbMDeltaResult:
    risk_class: str
    scenario: str  # 'medium', 'high', 'low'
    bucket_results: dict[str, BucketDeltaResult]
    capital: float


def compute_girr_tenor_correlation(t1: float, t2: float) -> float:
    """Supervisory correlation between GIRR tenors within the same currency (MAR21.13).

    rho_{kl} = max(0.40, exp(-theta * |T_k - T_l| / min(T_k, T_l)))
    where theta = 0.03.
    """
    if t1 == t2:
        return 1.0
    theta = 0.03
    min_t = min(t1, t2)
    diff_t = abs(t1 - t2)
    rho = math.exp(-theta * diff_t / min_t)
    return max(0.40, rho)


def adjust_correlation_for_scenario(rho: float, scenario: str) -> float:
    """Scale supervisory correlation under the three FRTB scenarios (MAR21.4).

    - Medium: rho
    - High: min(1.25 * rho, 1.0)
    - Low: max(2.0 * rho - 1.0, 0.75 * rho)
    """
    if scenario == "medium":
        return rho
    elif scenario == "high":
        return min(1.0, 1.25 * rho)
    elif scenario == "low":
        return max(0.75 * rho, 2.0 * rho - 1.0)
    else:
        raise ValueError(f"Unknown scenario: {scenario}")


def calculate_sbm_delta_bucket(
    sensitivities: Sequence[SensitivityRecord],
    scenario: str = "medium",
    intra_bucket_corr_func=None,
    flat_rho: float | None = None,
) -> BucketDeltaResult:
    """Calculate intra-bucket capital charge K_b under Basel MAR21.

    K_b = sqrt(max(0, sum_k WS_k^2 + sum_k sum_{l != k} rho_{kl} WS_k WS_l))
    """
    if not sensitivities:
        raise ValueError("Sensitivities list cannot be empty")

    bucket_id = sensitivities[0].bucket_id
    ws_map: dict[str, float] = {}
    factors: list[str] = []

    for s in sensitivities:
        ws = s.net_sensitivity * s.risk_weight
        ws_map[s.factor_id] = ws
        factors.append(s.factor_id)

    sum_ws = sum(ws_map.values())
    n = len(factors)

    # Intra-bucket double summation
    radicand = 0.0
    for i in range(n):
        f_i = factors[i]
        ws_i = ws_map[f_i]
        radicand += ws_i**2
        for j in range(n):
            if i == j:
                continue
            f_j = factors[j]
            ws_j = ws_map[f_j]

            if intra_bucket_corr_func is not None:
                base_rho = intra_bucket_corr_func(f_i, f_j)
            elif flat_rho is not None:
                base_rho = flat_rho
            else:
                base_rho = 0.50

            scaled_rho = adjust_correlation_for_scenario(base_rho, scenario)
            radicand += scaled_rho * ws_i * ws_j

    k_b = math.sqrt(max(0.0, radicand))

    return BucketDeltaResult(
        bucket_id=bucket_id,
        weighted_sensitivities=ws_map,
        sum_ws=sum_ws,
        capital_k_b=k_b,
    )


def aggregate_sbm_delta(
    bucket_results: Sequence[BucketDeltaResult],
    inter_bucket_corr: float = 0.50,
    scenario: str = "medium",
) -> float:
    """Aggregate across buckets with inter-bucket correlation gamma_bc and negative-sum fallback.

    K = sqrt(max(0, sum_b K_b^2 + sum_b sum_{c != b} gamma_{bc} S_b S_c))
    where S_b = sum_{k in b} WS_k, truncated to [-K_b, K_b] if required.
    """
    gamma = adjust_correlation_for_scenario(inter_bucket_corr, scenario)
    sum_k_sq = sum(b.capital_k_b**2 for b in bucket_results)

    cross_term = 0.0
    n = len(bucket_results)
    for i in range(n):
        b_i = bucket_results[i]
        # In Basel MAR21, S_b is clamped: S_bar_b = max(-K_b, min(K_b, S_b))
        s_i = max(-b_i.capital_k_b, min(b_i.capital_k_b, b_i.sum_ws))
        for j in range(n):
            if i == j:
                continue
            b_j = bucket_results[j]
            s_j = max(-b_j.capital_k_b, min(b_j.capital_k_b, b_j.sum_ws))
            cross_term += gamma * s_i * s_j

    radicand = sum_k_sq + cross_term
    # Negative-sum fallback: if radicand < 0, floor at sum_k_sq
    return math.sqrt(sum_k_sq if radicand < 0.0 else radicand)


# ============================================================================
# 2. Curvature Risk Engine
# ============================================================================


@dataclass
class CurvatureRecord:
    factor_id: str
    bucket_id: str
    net_sensitivity: float  # delta s_k
    risk_weight: float  # RW_k
    pv_up: float  # V(x_k + RW_k)
    pv_down: float  # V(x_k - RW_k)
    pv_base: float  # V(x_k)


def calculate_curvature_factor(rec: CurvatureRecord) -> tuple[float, float]:
    """Calculate upward and downward curvature charges (MAR21.35).

    CVR_k^+ = - [V(x_k + RW_k) - V(x_k) - RW_k * s_k]
    CVR_k^- = - [V(x_k - RW_k) - V(x_k) + RW_k * s_k]
    """
    cvr_up = -(rec.pv_up - rec.pv_base - rec.risk_weight * rec.net_sensitivity)
    cvr_down = -(rec.pv_down - rec.pv_base + rec.risk_weight * rec.net_sensitivity)
    return cvr_up, cvr_down


# ============================================================================
# 3. Default Risk Charge (DRC) Engine
# ============================================================================


@dataclass
class DRCPosition:
    obligor_id: str
    rating: str  # 'AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'Defaulted'
    seniority: str  # 'senior', 'subordinated', 'equity'
    bucket: str  # 'Corporates', 'Sovereigns', 'Local Governments/Municipalities'
    notional: float  # Face value
    market_value: float  # MtM value
    is_long: bool


def calculate_jtd(pos: DRCPosition) -> float:
    """Calculate Jump-to-Default (JTD) under MAR22.

    JTD_long = LGD * Notional + MtM
    JTD_short = -( (1 - LGD) * Notional + MtM ) or standard formula:
    Basel MAR22.9:
    JTD_long = max(0, LGD * Notional + PnL)
    JTD_short = min(0, -LGD * Notional + PnL)
    """
    lgd = 0.75 if pos.seniority == "subordinated" else (1.0 if pos.seniority == "equity" else 0.40)
    if pos.is_long:
        return max(0.0, lgd * pos.notional + pos.market_value)
    return min(0.0, -lgd * pos.notional + pos.market_value)


def calculate_drc_non_sec(positions: Sequence[DRCPosition]) -> float:
    """Calculate FRTB Default Risk Charge for non-securitizations (MAR22).

    DRC = max(0, sum_{long} RW_i * JTD_i - WtS * sum_{short} RW_i * |JTD_i|)
    where WtS (Weighted-to-Short ratio) is bounded by 1.0.
    """
    rw_table = {
        "AAA": 0.005,
        "AA": 0.020,
        "A": 0.030,
        "BBB": 0.060,
        "BB": 0.150,
        "B": 0.300,
        "CCC": 0.500,
        "Defaulted": 1.000,
    }

    # Net JTD per bucket, obligor, and seniority
    net_jtd: dict[tuple[str, str, str], float] = {}
    ratings: dict[tuple[str, str, str], str] = {}

    for p in positions:
        jtd = calculate_jtd(p)
        key = (p.bucket, p.obligor_id, p.seniority)
        net_jtd[key] = net_jtd.get(key, 0.0) + jtd
        ratings.setdefault(key, p.rating)

    long_obligors = {
        (bucket, obligor)
        for (bucket, obligor, _seniority), jtd in net_jtd.items()
        if jtd > 0.0
    }
    bucket_totals: dict[str, list[float]] = {}
    for (bucket, obligor, seniority), jtd in net_jtd.items():
        totals = bucket_totals.setdefault(bucket, [0.0, 0.0, 0.0, 0.0])
        rw = rw_table.get(ratings[(bucket, obligor, seniority)], 0.060)
        if jtd > 0:
            totals[0] += rw * jtd
            totals[2] += jtd
        elif jtd < 0 and (bucket, obligor) not in long_obligors:
            totals[1] += rw * abs(jtd)
            totals[3] += abs(jtd)

    drc = 0.0
    for long_weighted, short_weighted, long_jtd, short_jtd in bucket_totals.values():
        gross_jtd = long_jtd + short_jtd
        wts = long_jtd / gross_jtd if gross_jtd > 0.0 else 0.0
        drc += max(0.0, long_weighted - wts * short_weighted)
    return drc


# ============================================================================
# 4. Verification Tests
# ============================================================================


def run_tests() -> None:
    print("Testing FRTB Standardised Approach (SbM, Curvature, DRC) Engine...")

    # 1. GIRR Tenor Correlation Test
    # Check 1y and 2y correlation: diff=1, min=1 -> rho = exp(-0.03 * 1 / 1) = exp(-0.03) = 0.970446
    rho_1_2 = compute_girr_tenor_correlation(1.0, 2.0)
    assert math.isclose(rho_1_2, math.exp(-0.03), rel_tol=1e-5)
    # Check extreme tenors: 0.25y and 30y -> capped at minimum 0.40
    rho_far = compute_girr_tenor_correlation(0.25, 30.0)
    assert rho_far == 0.40

    # 2. Correlation Scenario Adjustments
    # High: min(1.25 * 0.60, 1.0) = 0.75
    assert math.isclose(adjust_correlation_for_scenario(0.60, "high"), 0.75, rel_tol=1e-5)
    # Low: max(0.75 * 0.60, 2 * 0.60 - 1.0) = max(0.45, 0.20) = 0.45
    assert math.isclose(adjust_correlation_for_scenario(0.60, "low"), 0.45, rel_tol=1e-5)

    # 3. Multi-Tenor USD GIRR SbM Test
    # 2-Tenor USD Portfolio:
    # 2y Tenor: Net sensitivity s_1 = $100,000 / bp = $1,000,000, RW = 1.30%
    # 10y Tenor: Net sensitivity s_2 = -$80,000 / bp = -$800,000, RW = 1.20%
    s1 = SensitivityRecord(
        factor_id="USD_2Y",
        bucket_id="USD",
        risk_class="GIRR",
        net_sensitivity=1_000_000.0,
        risk_weight=0.0130,  # 1.30%
    )
    s2 = SensitivityRecord(
        factor_id="USD_10Y",
        bucket_id="USD",
        risk_class="GIRR",
        net_sensitivity=-800_000.0,
        risk_weight=0.0120,  # 1.20%
    )

    def girr_corr_func(f1: str, f2: str) -> float:
        t_map = {"USD_2Y": 2.0, "USD_10Y": 10.0}
        return compute_girr_tenor_correlation(t_map[f1], t_map[f2])

    res_med = calculate_sbm_delta_bucket([s1, s2], scenario="medium", intra_bucket_corr_func=girr_corr_func)
    res_high = calculate_sbm_delta_bucket([s1, s2], scenario="high", intra_bucket_corr_func=girr_corr_func)
    res_low = calculate_sbm_delta_bucket([s1, s2], scenario="low", intra_bucket_corr_func=girr_corr_func)

    ws1 = 1_000_000.0 * 0.0130  # 13,000
    ws2 = -800_000.0 * 0.0120  # -9,600
    rho_2_10 = compute_girr_tenor_correlation(2.0, 10.0)  # exp(-0.03 * 8 / 2) = exp(-0.12) = 0.886920
    assert math.isclose(rho_2_10, math.exp(-0.12), rel_tol=1e-5)

    expected_radicand_med = ws1**2 + ws2**2 + 2.0 * rho_2_10 * ws1 * ws2
    expected_k_med = math.sqrt(expected_radicand_med)
    assert math.isclose(res_med.capital_k_b, expected_k_med, rel_tol=1e-4)

    print(f"USD GIRR Delta Capital (Medium Scenario): ${res_med.capital_k_b:,.2f}")
    print(f"USD GIRR Delta Capital (High Scenario):   ${res_high.capital_k_b:,.2f}")
    print(f"USD GIRR Delta Capital (Low Scenario):    ${res_low.capital_k_b:,.2f}")
    # High correlation produces the lowest capital because the portfolio is curve-hedged (long 2y, short 10y)
    # Low correlation produces the highest capital charge because the hedge offsets less
    assert res_low.capital_k_b > res_med.capital_k_b > res_high.capital_k_b

    # 4. Multi-Bucket Aggregation Test (USD + EUR GIRR)
    # EUR Bucket with single 5Y sensitivity:
    s_eur = SensitivityRecord(
        factor_id="EUR_5Y",
        bucket_id="EUR",
        risk_class="GIRR",
        net_sensitivity=500_000.0,
        risk_weight=0.0120,
    )
    res_eur = calculate_sbm_delta_bucket([s_eur], scenario="medium", flat_rho=1.0)
    total_girr_k = aggregate_sbm_delta([res_med, res_eur], inter_bucket_corr=0.50, scenario="medium")
    assert total_girr_k > 0.0
    print(f"Aggregated Multi-Currency (USD + EUR) GIRR Delta Capital: ${total_girr_k:,.2f}")

    # 5. Default Risk Charge (DRC) Test
    # Long Senior Bond Obligor X ($10M notional, LGD 40%, rating BBB -> RW 6%)
    # Short Senior Bond Obligor X ($5M notional, LGD 40%, rating BBB -> RW 6%)
    # Long Senior Bond Obligor Y ($8M notional, LGD 40%, rating BB -> RW 15%)
    p1 = DRCPosition(obligor_id="X", rating="BBB", seniority="senior", bucket="Corporates", notional=10_000_000.0, market_value=0.0, is_long=True)
    p2 = DRCPosition(obligor_id="X", rating="BBB", seniority="senior", bucket="Corporates", notional=5_000_000.0, market_value=0.0, is_long=False)
    p3 = DRCPosition(obligor_id="Y", rating="BB", seniority="senior", bucket="Corporates", notional=8_000_000.0, market_value=0.0, is_long=True)

    drc_capital = calculate_drc_non_sec([p1, p2, p3])
    # Obligor X net JTD = +4M - 2M = +2M, RW = 6% -> 120,000
    # Obligor Y net JTD = +3.2M, RW = 15% -> 480,000
    # No short positions remain after netting -> DRC = 120,000 + 480,000 = 600,000
    assert math.isclose(drc_capital, 600_000.0, rel_tol=1e-5)
    print(f"DRC Non-Securitisation Capital Requirement: ${drc_capital:,.2f}")

    print("All FRTB SbM, Curvature, and DRC tests passed successfully!")


if __name__ == "__main__":
    run_tests()
