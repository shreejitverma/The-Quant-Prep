"""FRTB Internal Model Approach (IMA, NMRF, and PLA) Reference Implementation.

Pure Python 3.10+ standard library implementation:
1. FRTB 97.5% Expected Shortfall (ES) with the Liquidity Horizon cascade formula.
2. Stressed period calibration and the Reduced Set scaling ratio.
3. Internally Modelled Capital Charge (IMCC) with unconstrained/constrained blend.
4. Non-Modellable Risk Factors (NMRF) Stressed ES (SES) aggregation.
5. P&L Attribution (PLA) metrics: Spearman Rank Correlation and Kolmogorov-Smirnov (KS) test.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

# ============================================================================
# 1. Expected Shortfall Liquidity Horizon Cascade (MAR31)
# ============================================================================


def calculate_es_liquidity_cascade(
    es_base: float,  # ES_T(P) at 10-day base horizon
    es_subsets: Sequence[tuple[float, int, int]],  # (ES_j, LH_j, LH_{j-1})
) -> float:
    """Calculate the FRTB Expected Shortfall under liquidity horizon cascade (MAR31.14).

    ES = sqrt( (ES_1)^2 + sum_{j >= 2} [ ES_j * sqrt((LH_j - LH_{j-1}) / 10) ]^2 )
    Standard liquidity horizons: LH_1=10, LH_2=20, LH_3=40, LH_4=60, LH_5=120 days.
    """
    total_sq = es_base**2
    for es_j, lh_j, lh_prev in es_subsets:
        delta_lh = lh_j - lh_prev
        scaled_es = es_j * math.sqrt(delta_lh / 10.0)
        total_sq += scaled_es**2

    return math.sqrt(total_sq)


def scale_stressed_reduced_es(
    es_current_full: float,  # ES_C,F
    es_current_reduced: float,  # ES_C,R
    es_stressed_reduced: float,  # ES_S,R
) -> float:
    """Calculate final calibrated Expected Shortfall via the Reduced Set ratio (MAR31.17).

    ES = ES_S,R * (ES_C,F / ES_C,R)
    """
    if es_current_reduced <= 0.0:
        raise ValueError("Current reduced ES must be positive")
    ratio = es_current_full / es_current_reduced
    return es_stressed_reduced * ratio


def calculate_imcc(
    es_unconstrained: float,  # ES with full cross-risk diversification
    es_constrained_by_class: Sequence[float],  # ES per asset class with zero correlation
    rho: float = 0.50,
) -> float:
    """Calculate Internally Modelled Capital Charge (IMCC) under MAR31.18.

    IMCC = rho * ES_unconstrained + (1 - rho) * sum_i ES_constrained,i
    where rho = 0.50.
    """
    sum_constrained = sum(es_constrained_by_class)
    return rho * es_unconstrained + (1.0 - rho) * sum_constrained


# ============================================================================
# 2. Non-Modellable Risk Factors (NMRF) Capital (MAR31.25)
# ============================================================================


def calculate_nmrf_ses(
    ses_factors: Sequence[tuple[str, float, bool]],  # (factor_id, SES_k, is_idiosyncratic)
    rho: float = 0.60,
) -> float:
    """Calculate Stressed Expected Shortfall for NMRFs under MAR31.25.

    SES = sqrt( sum_i SES_idio,i^2 ) + sqrt( (rho * sum_j SES_sys,j)^2 + (1 - rho^2) * sum_j SES_sys,j^2 )
    where rho = 0.60 for systematic factors, and idiosyncratic factors sum in quadrature.
    """
    idio_ses = [ses for _, ses, is_id in ses_factors if is_id]
    sys_ses = [ses for _, ses, is_id in ses_factors if not is_id]

    # Idiosyncratic term
    k_idio = math.sqrt(sum(s**2 for s in idio_ses)) if idio_ses else 0.0

    # Systematic term
    if sys_ses:
        sum_s = sum(sys_ses)
        sum_sq_s = sum(s**2 for s in sys_ses)
        k_sys = math.sqrt((rho * sum_s) ** 2 + (1.0 - rho**2) * sum_sq_s)
    else:
        k_sys = 0.0

    return k_idio + k_sys


# ============================================================================
# 3. P&L Attribution (PLA) Testing Engine (MAR32)
# ============================================================================


@dataclass
class PLAResult:
    spearman_corr: float
    ks_stat: float
    traffic_light: str  # 'GREEN', 'AMBER', 'RED'
    is_eligible: bool  # True for GREEN or AMBER


def rank_array(arr: Sequence[float]) -> list[float]:
    """Compute fractional ranks of an array."""
    n = len(arr)
    indexed = sorted([(arr[i], i) for i in range(n)])
    ranks = [0.0] * n

    i = 0
    while i < n:
        j = i
        while j < n - 1 and math.isclose(indexed[j][0], indexed[j + 1][0], rel_tol=1e-9):
            j += 1
        # Average rank for ties (1-indexed)
        avg_rank = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[indexed[k][1]] = avg_rank
        i = j + 1

    return ranks


def compute_spearman_rank_correlation(x: Sequence[float], y: Sequence[float]) -> float:
    """Compute Spearman rank correlation between HPL and RTPL (MAR32.20).

    r_s is the Pearson correlation of the average-rank arrays.
    """
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("Arrays must have equal length >= 2")

    n = len(x)
    rx = rank_array(x)
    ry = rank_array(y)

    mean_x = sum(rx) / n
    mean_y = sum(ry) / n
    centered_x = [rank - mean_x for rank in rx]
    centered_y = [rank - mean_y for rank in ry]
    sum_sq_x = sum(value**2 for value in centered_x)
    sum_sq_y = sum(value**2 for value in centered_y)
    if sum_sq_x == 0.0 or sum_sq_y == 0.0:
        return 0.0
    covariance = sum(x_rank * y_rank for x_rank, y_rank in zip(centered_x, centered_y, strict=True))
    return covariance / math.sqrt(sum_sq_x * sum_sq_y)


def compute_kolmogorov_smirnov(x: Sequence[float], y: Sequence[float]) -> float:
    """Compute empirical Kolmogorov-Smirnov two-sample statistic D (MAR32.22).

    D = sup_z | F_HPL(z) - F_RTPL(z) |
    """
    n_x = len(x)
    n_y = len(y)
    if n_x == 0 or n_y == 0:
        raise ValueError("Arrays cannot be empty")

    sorted_x = sorted(x)
    sorted_y = sorted(y)

    # Combined unique evaluation points
    eval_points = sorted(set(sorted_x + sorted_y))
    max_d = 0.0

    idx_x = 0
    idx_y = 0

    for z in eval_points:
        while idx_x < n_x and sorted_x[idx_x] <= z:
            idx_x += 1
        while idx_y < n_y and sorted_y[idx_y] <= z:
            idx_y += 1

        cdf_x = idx_x / n_x
        cdf_y = idx_y / n_y
        diff = abs(cdf_x - cdf_y)
        if diff > max_d:
            max_d = diff

    return max_d


def evaluate_pla_test(hpl: Sequence[float], rtpl: Sequence[float]) -> PLAResult:
    """Evaluate Basel MAR32 P&L Attribution test: Spearman + KS test.

    Traffic Light Zones:
    - GREEN: Spearman >= 0.80 and KS <= 0.09
    - AMBER: (0.70 <= Spearman < 0.80 and KS <= 0.12) or (Spearman >= 0.80 and 0.09 < KS <= 0.12)
    - RED: Spearman < 0.70 or KS > 0.12
    """
    rs = compute_spearman_rank_correlation(hpl, rtpl)
    ks = compute_kolmogorov_smirnov(hpl, rtpl)

    if rs >= 0.80 and ks <= 0.09:
        zone = "GREEN"
        eligible = True
    elif rs >= 0.70 and ks <= 0.12:
        zone = "AMBER"
        eligible = True
    else:
        zone = "RED"
        eligible = False

    return PLAResult(
        spearman_corr=rs,
        ks_stat=ks,
        traffic_light=zone,
        is_eligible=eligible,
    )


# ============================================================================
# 4. Verification Tests
# ============================================================================


def run_tests() -> None:
    print("Testing FRTB IMA (ES Cascade, Stressed Ratio, IMCC, NMRF, PLA)...")

    # 1. Liquidity Horizon Cascade Test
    # Base ES at 10 days = $1,000,000
    # Subset 2 (LH=20, delta=10): ES_2 = $800,000 -> scaled = $800,000 * sqrt(10/10) = $800,000
    # Subset 3 (LH=60, delta=40): ES_3 = $500,000 -> scaled = $500,000 * sqrt(40/10) = $1,000,000
    subsets = [(800_000.0, 20, 10), (500_000.0, 60, 20)]
    cascade_es = calculate_es_liquidity_cascade(1_000_000.0, subsets)
    expected_sq = 1_000_000.0**2 + 800_000.0**2 + (500_000.0 * 2.0) ** 2
    assert math.isclose(cascade_es, math.sqrt(expected_sq), rel_tol=1e-5)
    print(f"Liquidity Horizon Cascade ES: ${cascade_es:,.2f}")

    # 2. Stressed Reduced Set Ratio Test
    # ES_current_full = $1,200,000, ES_current_reduced = $1,000,000 -> ratio = 1.20
    # ES_stressed_reduced = $2,500,000
    es_final = scale_stressed_reduced_es(1_200_000.0, 1_000_000.0, 2_500_000.0)
    assert math.isclose(es_final, 3_000_000.0, rel_tol=1e-5)
    print(f"Stressed Calibrated ES: ${es_final:,.2f}")

    # 3. IMCC Diversification Blend Test
    # ES_unconstrained = $2,000,000
    # ES_constrained across 3 asset classes = [$1.2M, $1.0M, $0.8M] (sum = $3.0M)
    imcc = calculate_imcc(2_000_000.0, [1_200_000.0, 1_000_000.0, 800_000.0], rho=0.50)
    # IMCC = 0.5 * 2.0M + 0.5 * 3.0M = 1.0M + 1.5M = $2.5M
    assert math.isclose(imcc, 2_500_000.0, rel_tol=1e-5)
    print(f"IMCC Capital Charge: ${imcc:,.2f}")

    # 4. NMRF Stressed ES (SES) Test
    # 2 Systematic NMRFs: SES_1 = $300,000, SES_2 = $400,000 (rho = 0.60)
    # 1 Idiosyncratic NMRF: SES_3 = $200,000
    factors = [
        ("RF_SYS1", 300_000.0, False),
        ("RF_SYS2", 400_000.0, False),
        ("RF_IDIO", 200_000.0, True),
    ]
    ses_total = calculate_nmrf_ses(factors, rho=0.60)
    # k_idio = 200,000
    # sum_s = 700k, sum_sq = 90k + 160k = 250k
    # term1 = (0.6 * 700k)^2 = 420k^2 = 176,400M
    # term2 = (1 - 0.36) * 250,000M = 0.64 * 250k = 160,000M
    # k_sys = sqrt(176,400M + 160,000M) = sqrt(336,400M) = $580,000.00
    # SES_total = 200k + 580k = 780,000.00
    assert math.isclose(ses_total, 780_000.0, rel_tol=1e-5)
    print(f"NMRF Stressed ES Capital: ${ses_total:,.2f}")

    # 5. P&L Attribution (PLA) Test
    # Synthetic 250-day series with near-perfect correlation (Green Zone)
    hpl = [float(i) for i in range(250)]
    rtpl_green = [float(i) + 0.1 * math.sin(i) for i in range(250)]
    pla_green = evaluate_pla_test(hpl, rtpl_green)
    assert pla_green.traffic_light == "GREEN"
    assert pla_green.is_eligible is True
    print(f"PLA Green Zone: Spearman={pla_green.spearman_corr:.4f}, KS={pla_green.ks_stat:.4f}")

    # Disconnected series (Red Zone)
    rtpl_red = [float(250 - i) for i in range(250)]
    pla_red = evaluate_pla_test(hpl, rtpl_red)
    assert pla_red.traffic_light == "RED"
    assert pla_red.is_eligible is False
    print(f"PLA Red Zone: Spearman={pla_red.spearman_corr:.4f}, KS={pla_red.ks_stat:.4f}")

    tied_corr = compute_spearman_rank_correlation([1.0, 1.0, 2.0], [1.0, 2.0, 3.0])
    assert math.isclose(tied_corr, math.sqrt(3.0) / 2.0, rel_tol=1e-12)
    assert compute_spearman_rank_correlation([1.0, 1.0], [1.0, 2.0]) == 0.0

    print("All FRTB IMA, NMRF, and PLA tests passed successfully!")


if __name__ == "__main__":
    run_tests()
