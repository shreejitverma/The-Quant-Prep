"""Capital definition, buffers, output floor, Basel history and the trading book boundary.

Reference implementation for notes 01 (capital, RWA and the Basel Framework), 02 (Basel I to the
2017 reforms) and 06 (the FRTB trading book and banking book boundary).
Every parameter is quoted from its primary source with the paragraph that sets it:

* the consolidated Basel Framework (bis.org/basel_framework, versions in force on 2026-10-16):
  RBC20 minima and output floor, RBC30 conservation and countercyclical buffers, RBC40 and SCO40
  G-SIB buffers and scores, RBC90 floor phase-in, CAP10 and CAP30 capital definition and deductions,
  LEV20 and LEV40 leverage requirements, RBC25 boundary, MAR11 structural FX, MAR99 backtesting;
* the historical standards on bis.org: the 1988 Accord (updated to April 1998), the January 1996
  market risk amendment and backtesting framework, Basel II (June 2006 comprehensive version) and the
  July 2009 market risk revisions.

`run_tests()` reproduces the Committee's own worked numbers (RBC20.13, RBC90.2, RBC30.4, RBC30.18,
LEV40.5, CAP30.33 FAQ1, SCO40.10 and the MAR99 Table 2 binomial probabilities) and computes,
prints and asserts every number quoted in notes 01, 02 and 06 to within half a unit of its last
quoted decimal.
Run it with `python 17-Regulatory-Capital-Basel-and-FRTB/code/basel_capital_framework.py`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import NormalDist

from basel_credit_saccr import (
    OUTPUT_FLOOR,
    OUTPUT_FLOOR_PHASE_IN,
    TRANSITIONAL_CAP,
    floored_rwa,
    sa_bank_rw_ecra,
    sa_corporate_rw,
    sa_residential_re_rw,
)
from frtb_sbm import GIRR, SCENARIOS, WeightedSensitivity, girr_risk_weight, girr_tenor_correlation, risk_class_capital

QUOTED_LOG: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number a note quotes and assert it rounds to the quoted figure (half a unit in the last decimal)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED_LOG.append(label)
    print(f"    {label}: {value:,.{decimals}f}")
    return value


# ============================================================================
# 1. Minimum requirements and buffers (RBC20, RBC30, RBC40, LEV20, LEV40)
# ============================================================================

CET1_MIN = 0.045  # RBC20.1(1)
TIER1_MIN = 0.06  # RBC20.1(2)
TOTAL_MIN = 0.08  # RBC20.1(3)
CCB = 0.025  # RBC30.2, met with CET1
CCYB_RECIPROCITY_MAX = 0.025  # RBC30.9 and footnote 78: 0 to 2.5% for reciprocity purposes
LEVERAGE_MIN = 0.03  # LEV20.7
LEVERAGE_GSIB_SHARE = 0.50  # LEV40.2: leverage buffer = 50% of the G-SIB higher loss absorbency requirement
RWA_SCALAR = 12.5  # reciprocal of the 8% minimum; MAR and OPE capital requirements are converted with it (OPE25.2)

# RBC40.4 Table 1: bucket -> (score range in bps, higher loss absorbency as % of RWA, met with CET1).
GSIB_BUCKETS = {1: ((130, 229), 0.010), 2: ((230, 329), 0.015), 3: ((330, 429), 0.020), 4: ((430, 529), 0.025), 5: ((530, 629), 0.035)}
GSIB_CUTOFF_BPS = 130  # RBC40.4
SUBSTITUTABILITY_CAP_BPS = 500  # SCO40.8

# MDA payout limits by quartile of the buffer range (RBC30.4, RBC30.17): 100%, 80%, 60%, 40% conservation, 0% above.
CONSERVATION_BY_QUARTILE = (1.00, 0.80, 0.60, 0.40)


def mda_ratio_for_buffer_test(cet1: float, at1: float, tier2: float) -> float:
    """CET1 ratio used for the buffer test (RBC30.4): exclude CET1 needed to meet the 6% Tier 1 and 8% total minima.

    Ratios are fractions of RWA.  AT1 above 1.5% may fill a Tier 2 shortfall, because the 8% test is on total capital.
    """
    at1_short = max(0.0, (TIER1_MIN - CET1_MIN) - at1)
    t2_short = max(0.0, (TOTAL_MIN - TIER1_MIN) - tier2 - max(0.0, at1 - (TIER1_MIN - CET1_MIN)))
    return cet1 - at1_short - t2_short


@dataclass(frozen=True)
class MdaResult:
    combined_buffer: float
    quartile_bounds: tuple[float, float, float, float, float]  # CET1 ratios bounding the four quartiles
    quartile: int | None  # 1..4, or None above the buffer
    min_conservation: float  # share of earnings that must be retained
    max_payout: float


def mda(cet1_for_test: float, ccyb: float = 0.0, gsib_hla: float = 0.0) -> MdaResult:
    """RBC30.4, RBC30.17 and RBC40.2: the CCyB and G-SIB requirement extend the conservation buffer in four equal bands."""
    buffer = CCB + ccyb + gsib_hla
    step = buffer / 4.0
    bounds = tuple(CET1_MIN + i * step for i in range(5))
    if cet1_for_test > bounds[4]:
        return MdaResult(buffer, bounds, None, 0.0, 1.0)
    if cet1_for_test < CET1_MIN:
        raise ValueError("below the CET1 minimum: a breach of RBC20.1, not a buffer question")
    q = 1 + min(3, int((cet1_for_test - CET1_MIN) / step + 1e-12))
    if cet1_for_test == bounds[q - 1] and q > 1:  # bands are (lower, upper], RBC30.4 Table
        q -= 1
    cons = CONSERVATION_BY_QUARTILE[q - 1]
    return MdaResult(buffer, bounds, q, cons, 1.0 - cons)


def leverage_mda(tier1_leverage: float, gsib_hla: float) -> float:
    """LEV40.3 to LEV40.5: the G-SIB leverage buffer in four equal ranges above 3%; returns the minimum conservation ratio."""
    buffer = LEVERAGE_GSIB_SHARE * gsib_hla
    if tier1_leverage > LEVERAGE_MIN + buffer:
        return 0.0
    step = buffer / 4.0
    q = 1 + min(3, int((tier1_leverage - LEVERAGE_MIN) / step + 1e-12))
    return CONSERVATION_BY_QUARTILE[q - 1]


def ccyb_bank_specific(exposures: dict[str, tuple[float, float]]) -> float:
    """RBC30.13 to RBC30.14: average of jurisdiction rates weighted by private-sector credit risk charges."""
    total = sum(charge for charge, _ in exposures.values())
    return sum(charge * min(rate, CCYB_RECIPROCITY_MAX) for charge, rate in exposures.values()) / total


def gsib_score(shares: dict[str, dict[str, float]]) -> tuple[dict[str, float], int]:
    """SCO40.7 to SCO40.10: indicator share x 10,000 bps, weighted within category, simple average across five categories.

    Substitutability weights are 6.67/6.67/3.33/3.33 (of 20) and the category is capped at 500 bps (SCO40.8);
    the final score is rounded half up to a whole bp (SCO40.10 footnote 7).
    """
    weights = {
        "cross_jurisdictional": {"claims": 0.5, "liabilities": 0.5},
        "size": {"total_exposures": 1.0},
        "interconnectedness": {"ifs_assets": 1 / 3, "ifs_liabilities": 1 / 3, "securities_outstanding": 1 / 3},
        "substitutability": {"assets_under_custody": 1 / 3, "payments": 1 / 3, "underwriting": 1 / 6, "trading_volume": 1 / 6},
        "complexity": {"otc_notional": 1 / 3, "level3_assets": 1 / 3, "trading_afs_securities": 1 / 3},
    }
    cats = {}
    for cat, ind in weights.items():
        cats[cat] = sum(w * shares[cat][name] * 10_000 for name, w in ind.items())
    cats["substitutability"] = min(cats["substitutability"], SUBSTITUTABILITY_CAP_BPS)
    total = sum(cats.values()) / 5.0
    return cats, int(math.floor(total + 0.5))


def gsib_bucket(score_bps: int) -> tuple[int | None, float]:
    for b, ((lo, hi), hla) in GSIB_BUCKETS.items():
        if lo <= score_bps <= hi:
            return b, hla
    return (None, 0.0) if score_bps < GSIB_CUTOFF_BPS else (5, GSIB_BUCKETS[5][1])


# ============================================================================
# 2. Definition of capital (CAP10, CAP30)
# ============================================================================

AT1_TRIGGER_MIN = 0.05125  # CAP10.11(11): liability-classified AT1 converts or writes down at >= 5.125% CET1
T2_AMORTISATION_YEARS = 5.0  # CAP10.16(4): straight-line recognition over the final five years
GENERAL_PROVISIONS_CAP = 0.0125  # CAP10.18: 1.25% of SA credit RWA
IRB_EXCESS_PROVISIONS_CAP = 0.006  # CAP10.19: 0.6% of IRB credit RWA
THRESHOLD_INDIVIDUAL = 0.10  # CAP30.32
THRESHOLD_AGGREGATE = 0.15  # CAP30.33 (15% of CET1 after all deductions = 15/85 of CET1 net of the items)
THRESHOLD_RW = 2.50  # CAP30.34


def tier2_recognised(nominal: float, years_to_maturity: float) -> float:
    """CAP10.16(4)(2): straight-line amortisation in the last five years; full recognition before that."""
    return nominal * max(0.0, min(1.0, years_to_maturity / T2_AMORTISATION_YEARS))


@dataclass(frozen=True)
class ThresholdResult:
    recognised: dict[str, float]
    deduction: float
    cet1_after: float
    rwa_250: float


def threshold_deductions(cet1_before: float, items: dict[str, float]) -> ThresholdResult:
    """CAP30.32 to CAP30.34 for significant investments, MSRs and temporary-difference DTAs.

    Step 1: each item is recognised up to 10% of CET1 after CAP30.7 to CAP30.30 adjustments.
    Step 2: the recognised total may not exceed 15% of CET1 after all deductions, computed per the
    CAP30.33 FAQ as 15/85 (17.65%) of CET1 net of a full deduction of the three items.
    The excess is allocated to the items pro rata; what stays recognised is risk weighted at 250%.
    """
    step1 = {k: min(v, THRESHOLD_INDIVIDUAL * cet1_before) for k, v in items.items()}
    hypothetical = cet1_before - sum(items.values())
    cap15 = THRESHOLD_AGGREGATE / (1.0 - THRESHOLD_AGGREGATE) * hypothetical
    total1 = sum(step1.values())
    scale = min(1.0, cap15 / total1) if total1 > 0 else 1.0
    recognised = {k: v * scale for k, v in step1.items()}
    deduction = sum(items.values()) - sum(recognised.values())
    return ThresholdResult(recognised, deduction, cet1_before - deduction, THRESHOLD_RW * sum(recognised.values()))


def rwa_density_breakeven(leverage_req: float, tier1_req_risk_based: float) -> float:
    """Average risk weight below which the leverage ratio needs more Tier 1 than the risk-based requirement."""
    return leverage_req / tier1_req_risk_based


# ============================================================================
# 3. History: Basel I, the 1996 amendment, Basel II, Basel 2.5
# ============================================================================

BASEL_I_RATIO = 0.08  # 1988 Accord para 44 (core capital at least 4%)
BASEL_I_WEIGHTS = (0.0, 0.10, 0.20, 0.50, 1.00)  # 1988 Accord para 28: 0, 10, 20, 50 and 100%
BASEL_II_CORPORATE = {"AAA to AA-": 0.20, "A+ to A-": 0.50, "BBB+ to BB-": 1.00, "Below BB-": 1.50, "Unrated": 1.00}  # Basel II para 66
MRA_MIN_MULTIPLIER = 3.0  # 1996 amendment B.4(j); Basel 2.5 para 718(Lxxvi)(l) for mc and ms
PLUS_FACTOR_1996 = {**dict.fromkeys(range(5), 0.0), 5: 0.40, 6: 0.50, 7: 0.65, 8: 0.75, 9: 0.85}  # 1996 backtesting Table 2
MAR99_MULTIPLIER = {**dict.fromkeys(range(5), 1.50), 5: 1.70, 6: 1.76, 7: 1.83, 8: 1.88, 9: 1.92}  # MAR99.17 Table 2


def plus_factor_1996(exceptions: int) -> float:
    return PLUS_FACTOR_1996.get(exceptions, 1.00)  # red zone: +1, "from three to four"


def binomial_cdf(k: int, n: int = 250, p: float = 0.01) -> float:
    return sum(math.comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k + 1))


def mra_capital(var_prev: float, var_avg60: float, multiplier: float) -> float:
    """1996 amendment B.4(i): max(previous day VaR, multiplier x average of the last 60 business days)."""
    return max(var_prev, multiplier * var_avg60)


def basel25_capital(var_prev: float, var_avg: float, svar_prev: float, svar_avg: float, mc: float, ms: float) -> float:
    """July 2009 revisions para 718(Lxxvi)(k): c = max(VaR_t-1, mc VaR_avg) + max(sVaR_t-1, ms sVaR_avg)."""
    return max(var_prev, mc * var_avg) + max(svar_prev, ms * svar_avg)


# ============================================================================
# 4. Boundary (RBC25) and structural FX (MAR11.3)
# ============================================================================


def switch_surcharge(capital_before: float, capital_after: float) -> float:
    """RBC25.15: any capital reduction from a switch becomes a disclosed Pillar 1 surcharge, fixed at the switch date."""
    return max(0.0, capital_before - capital_after)


def cet1_ratio_after_fx(cet1_domestic: float, cet1_foreign_ccy: float, rwa_domestic: float, rwa_foreign_ccy: float, fx: float) -> float:
    """CET1 ratio in reporting currency when part of CET1 and part of RWA are in a foreign currency."""
    return (cet1_domestic + cet1_foreign_ccy * fx) / (rwa_domestic + rwa_foreign_ccy * fx)


def girr_irt_desk(pv01_by_tenor: dict[float, float]) -> dict[str, float]:
    """Stand-alone GIRR delta capital of a USD IRT desk (RBC25.25(3)) with the frtb_sbm engine; MAR21.4, MAR21.42 to MAR21.46."""
    ws = []
    for tenor, pv01 in pv01_by_tenor.items():
        rw = girr_risk_weight("USD", "rate", tenor, domestic="USD", sqrt2_discretion=False)
        ws.append(WeightedSensitivity("USD", ("rate", "SOFR", tenor), rw * pv01 / 0.0001))
    return {sc: risk_class_capital(GIRR, ws, sc).capital for sc in SCENARIOS}


# ============================================================================
# 5. Self-checks and every number quoted in notes 01, 02 and 06
# ============================================================================


def _check_framework_examples() -> None:
    q = quoted
    print("  Basel Framework worked numbers")
    # RBC20.13 Table 1 and RBC90.2.
    q("RBC20.13 floored RWA", floored_rwa(76, 140), 101.5, 1)
    q("RBC90.2 capped floored RWA", floored_rwa(76, 140, cap=TRANSITIONAL_CAP), 95, 0)
    q("RBC20.13 RWA increase from the floor (%)", (floored_rwa(76, 140) / 76 - 1) * 100, 33.55, 2)
    q("RWA of a 100 market risk charge", RWA_SCALAR * 100, 1_250, 0)
    assert OUTPUT_FLOOR == 0.725 and OUTPUT_FLOOR_PHASE_IN[2028] == OUTPUT_FLOOR
    # RBC30.4: 8% CET1, no AT1 or T2, all minima met with CET1 -> zero buffer -> 100% constraint.
    test = mda_ratio_for_buffer_test(0.08, 0.0, 0.0)
    q("RBC30.4 CET1 left for the buffer test (%)", test * 100, 4.5, 1)
    assert mda(test).min_conservation == 1.00
    # RBC30.4 Table bounds (no CCyB) and RBC30.18 with a 2.5% CCyB.
    for got, want in zip(mda(0.05).quartile_bounds, (0.045, 0.05125, 0.0575, 0.06375, 0.07), strict=True):
        assert abs(got - want) < 1e-12
    for got, want in zip(mda(0.05, ccyb=0.025).quartile_bounds, (0.045, 0.0575, 0.07, 0.0825, 0.095), strict=True):
        assert abs(got - want) < 1e-12
    assert mda(0.0550).min_conservation == 0.80 and mda(0.0710).quartile is None  # RBC30.4: 5.125-5.75 band -> 80%
    # LEV40.5: G-SIB bucket 1 (1% HLA): leverage bands 3-3.125-3.25-3.375-3.5%.
    assert leverage_mda(0.0310, 0.01) == 1.00 and leverage_mda(0.0320, 0.01) == 0.80
    assert leverage_mda(0.0330, 0.01) == 0.60 and leverage_mda(0.0340, 0.01) == 0.40 and leverage_mda(0.0351, 0.01) == 0.0
    # CAP30.33 FAQ1: EUR 85 of CET1 net of the items -> at most 15 recognised -> 100 of CET1 with 15% specified items.
    # Three items of 5 each, all inside their 10% individual limits, as the FAQ assumes.
    r = threshold_deductions(85 + 15, {"significant investments": 5.0, "MSRs": 5.0, "temporary-difference DTAs": 5.0})
    assert abs(sum(r.recognised.values()) - 15.0) < 1e-9 and abs(r.cet1_after - 100.0) < 1e-9
    q("CAP30.33 FAQ1 multiplier 15/85 (%)", 15 / 85 * 100, 17.65, 2)
    # SCO40.10: a 3% share of the sample is a 300 bps indicator score.
    q("SCO40.10 indicator score for a 3% share (bps)", 0.03 * 10_000, 300, 0)


def _check_note_01() -> dict[str, float]:
    q = quoted
    print("  Note 01: capital stack, buffers, MDA, leverage")
    q("RWA scalar 1 / 8%", 1 / TOTAL_MIN, 12.5, 1)
    q("CET1 requirement with 2.5% CCB, 1% CCyB, 1.5% G-SIB (%)", (CET1_MIN + CCB + 0.01 + 0.015) * 100, 9.5, 1)

    # CCyB: three jurisdictions weighted by private-sector credit risk charges (RBC30.14).
    ccyb = ccyb_bank_specific({"A": (400.0, 0.02), "B": (200.0, 0.01), "C": (400.0, 0.0)})
    q("bank-specific CCyB (%)", ccyb * 100, 1.0, 2)

    # G-SIB score from indicator shares (SCO40.7 to SCO40.10) -> bucket 2 -> 1.5% (RBC40.4).
    shares = {
        "cross_jurisdictional": {"claims": 0.030, "liabilities": 0.026},
        "size": {"total_exposures": 0.028},
        "interconnectedness": {"ifs_assets": 0.025, "ifs_liabilities": 0.029, "securities_outstanding": 0.031},
        "substitutability": {"assets_under_custody": 0.040, "payments": 0.035, "underwriting": 0.020, "trading_volume": 0.030},
        "complexity": {"otc_notional": 0.020, "level3_assets": 0.025, "trading_afs_securities": 0.030},
    }
    cats, score = gsib_score(shares)
    q("G-SIB category score: cross-jurisdictional (bps)", cats["cross_jurisdictional"], 280, 0)
    q("G-SIB category score: size (bps)", cats["size"], 280, 0)
    q("G-SIB category score: interconnectedness (bps)", cats["interconnectedness"], 283.33, 2)
    q("G-SIB category score: substitutability (bps)", cats["substitutability"], 333.33, 2)
    q("G-SIB category score: complexity (bps)", cats["complexity"], 250, 0)
    q("G-SIB total score (bps)", score, 285, 0)
    bucket, hla = gsib_bucket(score)
    assert bucket == 2
    q("G-SIB higher loss absorbency (%)", hla * 100, 1.5, 1)
    q("G-SIB leverage buffer (%)", LEVERAGE_GSIB_SHARE * hla * 100, 0.75, 2)
    # Substitutability cap: a 6% custody, 6% payments, 6% underwriting, 6% trading share would score 600 -> capped 500.
    capped, _ = gsib_score({**shares, "substitutability": dict.fromkeys(shares["substitutability"], 0.06)})
    for name, want in (("assets_under_custody", 400), ("payments", 350), ("underwriting", 200), ("trading_volume", 300)):
        q(f"substitutability indicator score {name} (bps)", shares["substitutability"][name] * 10_000, want, 0)
    q("substitutability at 6% shares, uncapped (bps)", 0.06 * 10_000 * (1 / 3 + 1 / 3 + 1 / 6 + 1 / 6), 600, 0)
    q("substitutability capped (bps)", capped["substitutability"], 500, 0)
    q("capped substitutability contribution to the total (bps)", capped["substitutability"] / 5, 100, 0)

    # Capital stack (EUR millions).
    gross = 6_000 + 1_500 + 8_000 - 200
    q("gross CET1 elements", gross, 15_300, 0)
    goodwill_net = 1_800 - 100  # CAP30.7: net of the DTL that would be extinguished on impairment
    nol_dta = 400  # CAP30.9: DTAs from tax-loss carry-forwards deducted in full
    pension_net = 300 - 60  # CAP30.16
    c0 = gross - goodwill_net - nol_dta - pension_net
    q("goodwill net of DTL", goodwill_net, 1_700, 0)
    q("pension asset net of DTL", pension_net, 240, 0)
    q("CET1 before threshold deductions", c0, 12_960, 0)
    q("sum of threshold items", 1_500 + 200 + 900, 2_600, 0)
    q("CET1 net of a full deduction of the items", c0 - 2_600, 10_360, 0)
    q("investments above the 10% limit", 1_500 - THRESHOLD_INDIVIDUAL * c0, 204, 0)
    th = threshold_deductions(c0, {"significant investments": 1_500.0, "MSRs": 200.0, "temporary-difference DTAs": 900.0})
    q("10% individual threshold", THRESHOLD_INDIVIDUAL * c0, 1_296, 0)
    q("15% aggregate cap (15/85 of 10,360)", 15 / 85 * (c0 - 2_600), 1_828.24, 2)
    q("threshold deduction", th.deduction, 771.76, 2)
    q("CET1", th.cet1_after, 12_188.24, 2)
    q("recognised items as share of CET1 (%)", sum(th.recognised.values()) / th.cet1_after * 100, 15.0, 2)
    q("RWA of recognised threshold items at 250%", th.rwa_250, 4_570.59, 2)
    credit_sa = 100_000 + th.rwa_250
    market_rwa = RWA_SCALAR * 1_200
    op_rwa = RWA_SCALAR * 1_000
    rwa = credit_sa + market_rwa + op_rwa
    q("market RWA = 12.5 x 1,200", market_rwa, 15_000, 0)
    q("operational RWA = 12.5 x 1,000", op_rwa, 12_500, 0)
    q("total RWA", rwa, 132_070.59, 2)
    at1 = 1_500.0
    q("SA credit RWA including the 250% items", credit_sa, 104_570.59, 2)
    q("Tier 2 bond with 3 years left counts (EUR m)", tier2_recognised(2_000, 3.0), 1_200, 0)
    q("share recognised with 3 years left (%)", tier2_recognised(1.0, 3.0) * 100, 60, 0)
    t2_debt = tier2_recognised(2_000, 3.0) + tier2_recognised(1_000, 8.0)
    q("Tier 2 debt recognised (2,000 at 3y + 1,000 at 8y)", t2_debt, 2_200, 0)
    gp_cap = GENERAL_PROVISIONS_CAP * credit_sa
    q("general provisions cap 1.25% of SA credit RWA", gp_cap, 1_307.13, 2)
    t2 = t2_debt + min(1_600, gp_cap)
    q("Tier 2", t2, 3_507.13, 2)
    t1 = th.cet1_after + at1
    total = t1 + t2
    c, a, t = th.cet1_after / rwa, at1 / rwa, t2 / rwa
    q("CET1 ratio (%)", c * 100, 9.23, 2)
    q("Tier 1 ratio (%)", t1 / rwa * 100, 10.36, 2)
    q("total capital ratio (%)", total / rwa * 100, 13.02, 2)
    q("AT1 ratio (%)", a * 100, 1.14, 2)
    q("Tier 2 ratio (%)", t * 100, 2.66, 2)
    q("Tier 1 capital (EUR m)", t1, 13_688.24, 2)
    q("leverage buffer quarter (%)", LEVERAGE_GSIB_SHARE * 0.015 / 4 * 100, 0.1875, 4)
    q("CET1 needed to fill the AT1 gap (%)", (TIER1_MIN - CET1_MIN - a) * 100, 0.36, 2)
    test = mda_ratio_for_buffer_test(c, a, t)
    q("CET1 ratio for the buffer test (%)", test * 100, 8.86, 2)
    m = mda(test, ccyb=0.01, gsib_hla=0.015)
    assert m.quartile == 4
    q("combined buffer (%)", m.combined_buffer * 100, 5.0, 1)
    q("fourth-quartile lower bound (%)", m.quartile_bounds[3] * 100, 8.25, 2)
    q("maximum payout, risk-based (%)", m.max_payout * 100, 60, 0)
    q("CET1 to clear the buffer (EUR m)", (m.quartile_bounds[4] - test) * rwa, 839.53, 2)
    lev_exposure = 400_000.0
    lev = t1 / lev_exposure
    q("Tier 1 leverage ratio (%)", lev * 100, 3.42, 2)
    q("leverage requirement with G-SIB buffer (%)", (LEVERAGE_MIN + LEVERAGE_GSIB_SHARE * hla) * 100, 3.75, 2)
    lev_cons = leverage_mda(lev, hla)
    q("minimum conservation, leverage (%)", lev_cons * 100, 60, 0)
    q("binding payout limit, higher of the two constraints (%)", (1 - max(lev_cons, m.min_conservation)) * 100, 40, 0)
    q("Tier 1 to clear the leverage buffer (EUR m)", (LEVERAGE_MIN + LEVERAGE_GSIB_SHARE * hla) * lev_exposure - t1, 1_311.76, 2)

    # Where the leverage ratio binds: average risk weight below which 3% of exposure exceeds the risk-based Tier 1 need.
    q("risk-based Tier 1 requirement with the CCB (%)", (TIER1_MIN + CCB) * 100, 8.5, 1)
    q("breakeven RWA density, non-G-SIB 3% / 8.5% (%)", rwa_density_breakeven(0.03, TIER1_MIN + CCB) * 100, 35.29, 2)
    q("breakeven RWA density, bucket 2 G-SIB 3.75% / 10.0% (%)", rwa_density_breakeven(0.0375, TIER1_MIN + CCB + 0.015) * 100, 37.5, 1)
    q("breakeven RWA density, minima only 3% / 6% (%)", rwa_density_breakeven(0.03, TIER1_MIN) * 100, 50.0, 1)
    q("bank RWA density (%)", rwa / lev_exposure * 100, 33.02, 2)

    return {"rwa": rwa, "t1": t1}


def _check_note_02() -> None:
    q = quoted
    print("  Note 02: Basel history")
    # Basel I: capital per 100 of exposure.
    for w in BASEL_I_WEIGHTS:
        assert abs(100 * w * BASEL_I_RATIO - {0.0: 0, 0.10: 0.8, 0.20: 1.6, 0.50: 4, 1.00: 8}[w]) < 1e-12
    q("Basel I capital per 100 corporate loan", 100 * 1.00 * BASEL_I_RATIO, 8, 0)
    q("Basel I capital per 100 residential mortgage", 100 * 0.50 * BASEL_I_RATIO, 4, 0)
    q("Basel I capital per 100 OECD bank claim", 100 * 0.20 * BASEL_I_RATIO, 1.6, 1)
    q("Basel II SA capital per 100 AA corporate", 100 * BASEL_II_CORPORATE["AAA to AA-"] * 0.08, 1.6, 1)
    q("Basel II SA capital per 100 B corporate", 100 * BASEL_II_CORPORATE["Below BB-"] * 0.08, 12, 0)
    q("Basel II RBA senior AAA securitisation capital per 100", 100 * 0.07 * 0.08, 0.56, 2)
    q("Basel III final SA capital per 100 BBB corporate (CRE20.42)", 100 * sa_corporate_rw("BBB") * 0.08, 6, 0)
    q("Basel III final SA capital per 100 AA corporate", 100 * sa_corporate_rw("AA") * 0.08, 1.6, 1)
    q("Basel III final SA capital per 100 B corporate", 100 * sa_corporate_rw("B") * 0.08, 12, 0)
    q("Basel II capital per 100 residential mortgage (35%, para 72)", 100 * 0.35 * 0.08, 2.8, 1)
    q("Basel III capital per 100 mortgage at LTV 50%", 100 * sa_residential_re_rw(0.50) * 0.08, 1.6, 1)
    q("Basel III capital per 100 mortgage at LTV above 100%", 100 * sa_residential_re_rw(1.10) * 0.08, 5.6, 1)

    # 1996 backtesting: binomial probabilities of MAR99 Table 2 / 1996 Table 2.
    published = {0: 8.11, 1: 28.58, 2: 54.32, 3: 75.81, 4: 89.22, 5: 95.88, 6: 98.63, 7: 99.60, 8: 99.89, 9: 99.97}
    for k, v in published.items():
        assert abs(binomial_cdf(k) * 100 - v) < 0.005 + 1e-9, (k, binomial_cdf(k))
    q("P(at most 4 exceptions | 99% model) (%)", binomial_cdf(4) * 100, 89.22, 2)
    q("P(at most 9 exceptions | 99% model) (%)", binomial_cdf(9) * 100, 99.97, 2)
    q("P(at most 10 exceptions | 99% model) (%)", binomial_cdf(10) * 100, 99.99, 2)
    q("P(5 or more exceptions | 99% model) (%)", (1 - binomial_cdf(4)) * 100, 10.78, 2)
    q("expected exceptions in 250 days", 250 * 0.01, 2.5, 1)
    ratio = NormalDist().inv_cdf(0.99) / NormalDist().inv_cdf(0.98)
    q("z at 99%", NormalDist().inv_cdf(0.99), 2.326, 3)
    q("z at 98%", NormalDist().inv_cdf(0.98), 2.054, 3)
    q("normal 99th / 98th percentile", ratio, 1.133, 3)
    q("normal ratio minus one", ratio - 1, 0.133, 3)
    q("P(at most 5 exceptions | 99% model) (%)", binomial_cdf(5) * 100, 95.88, 2)
    q("implied plus factor for multiplier 3", 3 * (ratio - 1), 0.40, 2)
    # MAR99 multipliers are the 1996 ones rescaled from 3 to 1.5, except 6 exceptions (1.75 would be the rescale).
    for k in range(10):
        rescaled = 1.5 * (3 + plus_factor_1996(k)) / 3
        assert abs(rescaled - MAR99_MULTIPLIER[k]) <= (0.0101 if k == 6 else 0.005 + 1e-12), (k, rescaled)
    q("1996 multiplier rescaled to the MAR99 base at 6 exceptions", 1.5 * 3.5 / 3, 1.75, 2)

    # 1996 amendment and Basel 2.5 capital.
    mult = MRA_MIN_MULTIPLIER + plus_factor_1996(6)
    q("multiplier with 6 exceptions", mult, 3.5, 2)
    mra = mra_capital(42.0, 38.0, mult)
    q("1996 VaR charge max(42, 3.5 x 38)", mra, 133, 0)
    c = basel25_capital(42.0, 38.0, 115.0, 124.0, mult, mult)
    q("Basel 2.5 VaR + sVaR charge", c, 567, 0)
    q("stressed term max(115, 3.5 x 124)", max(115.0, mult * 124.0), 434, 0)
    q("IRC + CRM", 65.0 + 20.0, 85, 0)
    total = c + 65.0 + 20.0
    q("Basel 2.5 total with IRC 65 and CRM 20", total, 652, 0)
    q("Basel 2.5 market RWA", RWA_SCALAR * total, 8_150, 0)
    q("sVaR share of the total (%)", max(115.0, mult * 124.0) / total * 100, 66.56, 2)
    q("ratio of the Basel 2.5 charge to the 1996 charge", total / mra, 4.90, 2)

    # Output floor case (EUR millions).
    internal, standardised, cet1 = 280_000.0, 450_000.0, 39_200.0
    fl = floored_rwa(internal, standardised)
    q("floored RWA at 72.5%", fl, 326_250, 0)
    q("RWA increase (%)", (fl / internal - 1) * 100, 16.52, 2)
    q("CET1 ratio before the floor (%)", cet1 / internal * 100, 14.00, 2)
    q("CET1 ratio after the floor (%)", cet1 / fl * 100, 12.02, 2)
    q("CET1 to restore 14% (EUR m)", 0.14 * fl - cet1, 6_475, 0)
    q("CET1 ratio points lost to the floor", (cet1 / internal - cet1 / fl) * 100, 1.98, 2)
    q("calibration at which the floor starts to bind (%)", internal / standardised * 100, 62.22, 2)
    by_year = {y: floored_rwa(internal, standardised, cal) for y, cal in OUTPUT_FLOOR_PHASE_IN.items()}
    assert by_year[2025] == internal and by_year[2026] > internal
    q("floored RWA in 2026 at 65%", by_year[2026], 292_500, 0)
    q("floored RWA in 2027 at 70%", by_year[2027], 315_000, 0)
    q("2026 RWA with the 25% transitional cap", floored_rwa(internal, standardised, 0.65, cap=TRANSITIONAL_CAP), 292_500, 0)
    q("transitional cap level (EUR m)", (1 + TRANSITIONAL_CAP) * internal, 350_000, 0)


def _check_note_06() -> None:
    q = quoted
    print("  Note 06: boundary, IRTs, switching, structural FX")
    # RBC25.15 switch surcharge: total capital before 50, after 45 -> disclosed Pillar 1 surcharge 5.
    q("total capital before the switch", 38 + 12, 50, 0)
    q("total capital after the switch", 38 + 7, 45, 0)
    q("total capital after a switch into a 15 banking book charge", 38 + 15, 53, 0)
    q("switch surcharge", switch_surcharge(38 + 12, 38 + 7), 5, 0)
    assert switch_surcharge(38 + 12, 38 + 15) == 0.0

    # RBC25.21 credit IRT: USD 100m unrated corporate loan hedged through the credit desk with an A-rated bank.
    loan = 100.0
    rw_loan, rw_bank = sa_corporate_rw(None), sa_bank_rw_ecra("A")
    q("unrated corporate RW (%)", rw_loan * 100, 100, 0)
    q("A-rated bank RW, ECRA (%)", rw_bank * 100, 30, 0)
    q("credit RWA, hedge recognised (USD m)", loan * rw_bank, 30, 0)
    q("credit RWA, hedge not recognised (USD m)", loan * rw_loan, 100, 0)
    q("capital at 8%, hedge recognised (USD m)", loan * rw_bank * TOTAL_MIN, 2.4, 1)
    q("capital at 8%, hedge not recognised (USD m)", loan * rw_loan * TOTAL_MIN, 8.0, 1)
    q("over-hedge: banking book short credit (USD m)", 120.0 - loan, 20, 0)

    # RBC25.25 GIRR IRT desk: internal leg receives fixed at 10y (PV01 -80,000); external hedge pays fixed.
    matched = girr_irt_desk({10.0: -80_000.0 + 80_000.0})
    assert all(v == 0.0 for v in matched.values())
    mism = girr_irt_desk({10.0: -80_000.0, 5.0: 80_000.0})
    q("WS at 10y (USD m)", 0.011 * -80_000 / 0.0001 / 1e6, -8.8, 1)
    q("rho(5y, 10y)", girr_tenor_correlation(5.0, 10.0), 0.9704, 4)
    q("IRT desk K, medium (USD m)", mism["medium"] / 1e6, 2.14, 2)
    q("IRT desk K, low (USD m)", mism["low"] / 1e6, 3.03, 2)
    q("IRT desk K, high (USD m)", mism["high"] / 1e6, 0.00, 2)
    q("IRT desk GIRR delta capital, max over scenarios (USD m)", max(mism.values()) / 1e6, 3.03, 2)
    unhedged = girr_irt_desk({10.0: -80_000.0})
    q("IRT desk K, no external hedge (USD m)", max(unhedged.values()) / 1e6, 8.8, 1)

    # MAR11.3 structural FX: CET1 position that neutralises the ratio.
    rwa_dom, rwa_eur, fx0, cet1 = 60_000.0, 40_000.0, 1.10, 12_480.0
    r0 = cet1_ratio_after_fx(cet1, 0.0, rwa_dom, rwa_eur, fx0)
    q("CET1 ratio before the FX move (%)", r0 * 100, 12.0, 2)
    q("EUR RWA in USD at 1.10", rwa_eur * fx0, 44_000, 0)
    neutral_usd = r0 * rwa_eur * fx0
    q("neutral structural long EUR position (USD m)", neutral_usd, 5_280, 0)
    q("neutral structural long EUR position (EUR m)", neutral_usd / fx0, 4_800, 0)
    fx1 = fx0 * 0.90
    unhedged_r = cet1_ratio_after_fx(cet1, 0.0, rwa_dom, rwa_eur, fx1)
    hedged_r = cet1_ratio_after_fx(cet1 - neutral_usd, neutral_usd / fx0, rwa_dom, rwa_eur, fx1)
    q("CET1 ratio after EUR -10%, all CET1 in USD (%)", unhedged_r * 100, 12.53, 2)
    q("CET1 ratio after EUR -10%, structural hedge (%)", hedged_r * 100, 12.00, 2)
    up = cet1_ratio_after_fx(cet1, 0.0, rwa_dom, rwa_eur, fx0 * 1.10)
    q("CET1 ratio after EUR +10%, all CET1 in USD (%)", up * 100, 11.51, 2)


def run_tests() -> None:
    print("Basel capital framework self-checks")
    _check_framework_examples()
    _check_note_01()
    _check_note_02()
    _check_note_06()
    print(f"  {len(QUOTED_LOG)} numbers quoted in notes 01, 02 and 06 computed, printed and asserted")
    print("All Basel capital framework checks passed.")


if __name__ == "__main__":
    run_tests()
