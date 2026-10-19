"""Stress testing, risk data quality, jurisdiction comparisons, KVA and the regulatory capital problem set.

Reference implementation for the section 17 notes:
* 13 FRTB implementation challenges and desk strategy
* 17 stress testing: CCAR, DFAST and EBA
* 18 BCBS 239 risk data aggregation
* 19 implementation status by jurisdiction
* 20 capital-aware trading: KVA and RWA limits
* 21 regulatory capital problem set

Regulatory formulas are not re-implemented here when a verified engine in this folder already has them:
SA-CCR, the output floor and IRB come from `basel_credit_saccr.py` (CRE31, CRE32, CRE52, RBC20, RBC90),
BA-CVA from `basel_cva.py` (MAR50), IMA aggregation, the amber-zone surcharge and the ES run count from `frtb_ima.py`
(MAR31 to MAR33), the SMA and LCR run-off rates from `basel_liquidity_irrbb.py` (OPE25, LCR40)
and the MDA bands from `basel_capital_framework.py` (RBC30, RBC40).
Every engine result that a note quotes is cross-checked against an independent computation written out here
(a closed form, an enumeration, a roll-forward or an attribution), and every quoted number is printed and asserted.

US stress-test rules follow 12 CFR 225.8(f)(2) (stress capital buffer), 12 CFR 252.44(c) (capital action assumptions)
and the Board's aggregation-model documentation (constant balance sheet and RWA); see note 17 for the dated sources.

Run with:
    python3 17-Regulatory-Capital-Basel-and-FRTB/code/basel_stress_reg.py
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

from basel_capital_framework import mda
from basel_credit_saccr import OUTPUT_FLOOR_PHASE_IN, NettingSet, Trade, floored_rwa, irb_corporate, saccr_ead
from basel_cva import Counterparty, NettingSetExposure, ba_cva, ba_cva_rw, supervisory_df
from basel_liquidity_irrbb import RUN_OFF, bic, ilm
from frtb_ima import (
    BROAD_RISK_CLASSES,
    LH_BY_CATEGORY,
    LIQUIDITY_HORIZONS,
    aggregate_capital,
    amber_surcharge,
    binomial_sf,
    broad_class,
    daily_es_runs,
)

QUOTED_LOG: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number a note quotes and assert that it rounds to the quoted figure (half a unit in the last place)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED_LOG.append(label)
    print(f"    {label}: {value:,.{decimals}f}")
    return value


def agree(label: str, a: float, b: float, tol: float = 1e-9) -> None:
    """Assert that two independently computed values agree."""
    assert abs(a - b) <= tol * max(1.0, abs(a), abs(b)), f"{label}: {a!r} != {b!r}"


# ============================================================================
# Note 13: FRTB implementation challenges and desk strategy
# ============================================================================


def es_runs_by_hand() -> int:
    """Independent count of the MAR33.15 ES runs: for each scope (all classes, then each broad class) the number of
    distinct nested liquidity-horizon subsets equals the number of distinct horizons present, times three calibrations."""
    horizons_by_class: dict[str, set[int]] = {c: set() for c in BROAD_RISK_CLASSES}
    for category, lh in LH_BY_CATEGORY.items():
        horizons_by_class[broad_class(category)].add(lh)
    all_horizons = set(LH_BY_CATEGORY.values())
    return 3 * (len(all_horizons) + sum(len(v) for v in horizons_by_class.values()))


def revaluation_budget(
    n_positions: int, n_scenarios: int, n_lh_subsets: int, n_calibrations: int, window_hours: float
) -> tuple[int, float]:
    """Full revaluations per night for the ES cascade and the sustained rate needed to finish inside the window."""
    total = n_positions * n_scenarios * n_lh_subsets * n_calibrations
    return total, total / (window_hours * 3600.0)


def revaluation_budget_by_loops(n_positions: int, n_scenarios: int, n_lh_subsets: int, n_calibrations: int) -> int:
    """Count the same revaluations by walking the loop nest one level at a time (no multiplication of the four sizes)."""
    per_position = 0
    for _calibration in range(n_calibrations):
        for _subset in range(n_lh_subsets):
            per_position += n_scenarios
    return per_position * n_positions


@dataclass(frozen=True)
class DeskCase:
    """Annual economics of seeking IMA for one desk (all inputs hypothetical, in USD millions)."""

    sa_capital: float
    imcc_avg: float  # 60-day average IMCC
    multiplier: float  # m_c, MAR33.42
    ses: float
    drc: float
    hurdle: float
    running_cost: float

    @property
    def ima_capital(self) -> float:
        """C_A + DRC with the averages binding: m_c x IMCC_avg + SES_avg + DRC (MAR33.41, MAR33.43)."""
        return self.multiplier * self.imcc_avg + self.ses + self.drc

    @property
    def saving(self) -> float:
        return self.sa_capital - self.ima_capital

    @property
    def net_annual(self) -> float:
        return self.hurdle * self.saving - self.running_cost


def annuity(rate: float, years: int) -> float:
    return sum((1.0 + rate) ** -t for t in range(1, years + 1))


def check_note13() -> None:
    print("=== Note 13: FRTB implementation challenges and desk strategy ===")
    per_class, runs = daily_es_runs()
    quoted("note13_es_runs", float(runs), 63.0, 0)
    agree("note13_es_runs_independent", float(runs), float(es_runs_by_hand()))
    quoted("note13_lh_subsets", float(len(LIQUIDITY_HORIZONS)), 5.0, 0)
    quoted("note13_class_subsets", float(sum(per_class.values())), 16.0, 0)

    # Example 1: compute sizing (hypothetical inputs, labelled in the note).
    total, rate = revaluation_budget(400_000, 250, 5, 3, 2.5)
    agree("note13_ex1_loop_count", float(total), float(revaluation_budget_by_loops(400_000, 250, 5, 3)))
    quoted("note13_ex1_total_revaluations", float(total), 1_500_000_000.0, 0)
    quoted("note13_ex1_rate_per_second", rate, 166_666.67, 2)
    quoted("note13_ex1_cores_all_simple", rate / 2_000.0, 83.33, 2)
    simple_cores = 0.80 * total / 9_000.0 / 2_000.0
    complex_cores = 0.20 * total / 9_000.0 / 50.0
    quoted("note13_ex1_cores_simple_share", simple_cores, 66.67, 2)
    quoted("note13_ex1_cores_complex_share", complex_cores, 666.67, 2)
    quoted("note13_ex1_cores_mixed", float(math.ceil(simple_cores + complex_cores)), 734.0, 0)
    # The mixed book is dominated by the slow 20%: share of core time spent on it.
    quoted("note13_ex1_complex_core_share_pct", 100.0 * complex_cores / (simple_cores + complex_cores), 90.91, 2)

    # AAD versus bumping (card reg-aad-in-frtb-systems): M factors, assumed reverse-sweep cost c = 4 valuations.
    m_factors, c_aad = 10_000, 4.0
    bumps_one_sided = m_factors + 1
    bumps_central = 2 * m_factors + 1
    quoted("note13_bump_one_sided", float(bumps_one_sided), 10_001.0, 0)
    quoted("note13_bump_central", float(bumps_central), 20_001.0, 0)
    quoted("note13_aad_speedup", bumps_one_sided / c_aad, 2_500.25, 2)

    # Example 2: corporate credit desk (USD millions).
    desk = DeskCase(sa_capital=250.0, imcc_avg=80.0, multiplier=1.5, ses=80.0, drc=40.0, hurdle=0.12, running_cost=1.7)
    quoted("note13_ex2_mc_imcc", desk.multiplier * desk.imcc_avg, 120.0, 1)
    quoted("note13_ex2_ima_capital", desk.ima_capital, 240.0, 1)
    quoted("note13_ex2_saving", desk.saving, 10.0, 1)
    quoted("note13_ex2_saving_pct", 100.0 * desk.saving / desk.sa_capital, 4.0, 1)
    quoted("note13_ex2_capital_benefit", desk.hurdle * desk.saving, 1.2, 2)
    quoted("note13_ex2_net_annual", desk.net_annual, -0.5, 2)
    ann = annuity(0.10, 5)
    agree("note13_annuity_closed_form", ann, (1.0 - 1.1**-5) / 0.10)
    quoted("note13_ex2_annuity", ann, 3.7908, 4)
    quoted("note13_ex2_npv", desk.net_annual * ann, -1.895, 3)
    breakeven_saving = desk.running_cost / desk.hurdle
    quoted("note13_ex2_breakeven_saving", breakeven_saving, 14.17, 2)
    quoted("note13_ex2_breakeven_ima", desk.sa_capital - breakeven_saving, 235.83, 2)
    quoted("note13_ex2_ses_share_pct", 100.0 * desk.ses / desk.ima_capital, 33.33, 2)

    # Example 3: amber-zone surcharge (card reg-pla-amber-zone-business-impact), USD millions.
    sa_by_desk = {"rates_green": 150.0, "credit_amber": 50.0}
    ima_ga, sa_ga, c_u, sa_all = 120.0, 200.0, 30.0, 230.0
    k, surcharge = amber_surcharge(sa_by_desk, {"credit_amber"}, ima_ga, sa_ga)
    k_hand = 0.5 * 50.0 / (150.0 + 50.0)
    agree("note13_amber_k_independent", k, k_hand)
    quoted("note13_amber_k", k, 0.125, 3)
    quoted("note13_amber_surcharge", surcharge, 10.0, 1)
    acr = aggregate_capital(ima_ga, surcharge, c_u, sa_all, sa_ga)
    agree("note13_acr_independent", acr, min(ima_ga + k_hand * (sa_ga - ima_ga) + c_u, sa_all) + max(0.0, ima_ga - sa_ga))
    quoted("note13_amber_acr", acr, 160.0, 1)
    quoted("note13_amber_acr_without_surcharge", aggregate_capital(ima_ga, 0.0, c_u, sa_all, sa_ga), 150.0, 1)
    quoted("note13_amber_annual_drag", 0.12 * surcharge, 1.2, 2)
    # A second amber desk raises k: both desks amber gives k = 0.5.
    k_all, s_all = amber_surcharge(sa_by_desk, {"rates_green", "credit_amber"}, ima_ga, sa_ga)
    quoted("note13_amber_k_all_amber", k_all, 0.5, 3)
    quoted("note13_amber_surcharge_all_amber", s_all, 40.0, 1)
    # The SA cap binds once IMA + surcharge + C_U exceeds SA for all desks.
    quoted("note13_amber_acr_all_amber", aggregate_capital(ima_ga, s_all, c_u, sa_all, sa_ga), 190.0, 1)

    # Output floor and desk-level relief (card reg-output-floor-neutralizing-ima), RWA in USD billions.
    for label, internal, saving, expected in (
        ("note13_floor_relief_bound", 485.0, 10.0, 0.0),
        ("note13_floor_relief_headroom", 560.0, 10.0, 10.0),
        ("note13_floor_relief_capped", 560.0, 50.0, 38.0),
    ):
        before = floored_rwa(internal, 720.0)
        after = floored_rwa(internal - saving, 720.0)
        agree(label + "_independent", before - after, max(internal, 0.725 * 720.0) - max(internal - saving, 0.725 * 720.0))
        quoted(label, before - after, expected, 1)
    quoted("note13_floor_level", 0.725 * 720.0, 522.0, 1)

    # Desk backtesting (MAR32.19): probability that a correct model breaches each limit over 250 days.
    p99 = binomial_sf(12, 250, 0.01)
    p975 = binomial_sf(30, 250, 0.025)
    agree("note13_p99_complement", p99, 1.0 - sum(math.comb(250, i) * 0.01**i * 0.99 ** (250 - i) for i in range(13)), 1e-9)
    quoted("note13_p_exceed_12_at_99_per_million", 1e6 * p99, 1.94, 2)
    quoted("note13_p_exceed_30_at_975_per_1e13", 1e13 * p975, 3.89, 2)
    quoted("note13_p_exceed_12_true_p3_pct", 100.0 * binomial_sf(12, 250, 0.03), 4.02, 2)
    quoted("note13_p_exceed_12_true_p2_pct", 100.0 * binomial_sf(12, 250, 0.02), 0.18, 2)
    quoted("note13_expected_exceptions_99", 250 * 0.01, 2.5, 1)
    quoted("note13_expected_exceptions_975", 250 * 0.025, 6.25, 2)


# ============================================================================
# Note 17: stress testing, CCAR, DFAST and EBA
# ============================================================================


@dataclass(frozen=True)
class ScbResult:
    start_ratio: float
    min_ratio: float
    trough_quarter: int
    decline: float
    dividend_add_on: float
    scb: float


def scb(
    start_cet1: float, rwa: Sequence[float], cum_net_income: Sequence[float], dividends_q4_q7: float, floor: float = 0.025
) -> ScbResult:
    """12 CFR 225.8(f)(2): SCB = max(floor, start ratio - lowest projected ratio + dividends Q4..Q7 / RWA at the trough).

    `rwa[0]` is the jump-off RWA and `rwa[q]` the projected RWA in quarter q; the supervisory test assumes no
    common dividends (12 CFR 252.44(c)), so projected CET1 is jump-off CET1 plus cumulative net income.
    """
    start_ratio = start_cet1 / rwa[0]
    ratios = [(start_cet1 + ni) / rwa[q + 1] for q, ni in enumerate(cum_net_income)]
    q_min = min(range(len(ratios)), key=ratios.__getitem__)
    decline = start_ratio - ratios[q_min]
    add_on = dividends_q4_q7 / rwa[q_min + 1]
    return ScbResult(start_ratio, ratios[q_min], q_min + 1, decline, add_on, max(floor, decline + add_on))


def roll_forward(start_cet1: float, quarterly_net_income: Sequence[float]) -> list[float]:
    """Independent quarter-by-quarter capital roll-forward (no cumulative sums)."""
    path, capital = [], start_cet1
    for ni in quarterly_net_income:
        capital = capital + ni
        path.append(capital)
    return path


@dataclass(frozen=True)
class Ifrs9:
    stage1_base: float
    stage2_base: float
    stage1_stress: float
    stage2_stress: float

    @property
    def base(self) -> float:
        return self.stage1_base + self.stage2_base

    @property
    def stress(self) -> float:
        return self.stage1_stress + self.stage2_stress


def ifrs9_stage_stress(exposure: float, s1_share: float, migrate: float, base: tuple, stress: tuple) -> Ifrs9:
    """ECL = EAD x PD x LGD per stage (12-month PD in stage 1, lifetime PD in stage 2), undiscounted for teaching.

    base = (pd1, lgd1, pd2, lgd2) before stress; stress = the same after stress.  A share `migrate` of stage 1 moves
    to stage 2 (significant increase in credit risk).
    """
    s1, s2 = exposure * s1_share, exposure * (1.0 - s1_share)
    pd1, lgd1, pd2, lgd2 = base
    spd1, slgd1, spd2, slgd2 = stress
    moved = s1 * migrate
    return Ifrs9(s1 * pd1 * lgd1, s2 * pd2 * lgd2, (s1 - moved) * spd1 * slgd1, (s2 + moved) * spd2 * slgd2)


def check_note17() -> None:
    print("=== Note 17: stress testing ===")
    # Example 1: SCB for a hypothetical bank (USD millions), constant RWA as in the Board's supervisory test.
    start_cet1, rwa0, tax = 50_000.0, 400_000.0, 0.21
    pre_tax = [-3_300.0, -3_900.0, -3_000.0, -1_650.0, -500.0, 380.0, 890.0, 1_140.0, 1_390.0]
    after_tax = [(1.0 - tax) * x for x in pre_tax]
    cum = [sum(after_tax[: q + 1]) for q in range(len(after_tax))]
    rwa = [rwa0] * (len(pre_tax) + 1)
    res = scb(start_cet1, rwa, cum, dividends_q4_q7=4 * 500.0)
    path = roll_forward(start_cet1, after_tax)
    trough_capital = min(path)
    agree("note17_trough_roll_forward", trough_capital / rwa0, res.min_ratio)
    agree("note17_trough_quarter_roll_forward", float(path.index(trough_capital) + 1), float(res.trough_quarter))
    quoted("note17_cum_pre_tax_9q", sum(pre_tax), -8_550.0, 0)
    quoted("note17_cum_after_tax_9q", cum[-1], -6_754.5, 1)
    quoted("note17_trough_cum_loss", -cum[res.trough_quarter - 1], 9_756.5, 1)
    quoted("note17_trough_quarter", float(res.trough_quarter), 5.0, 0)
    quoted("note17_trough_cet1", trough_capital, 40_243.5, 1)
    quoted("note17_start_ratio_pct", 100.0 * res.start_ratio, 12.50, 2)
    quoted("note17_min_ratio_pct", 100.0 * res.min_ratio, 10.06, 2)
    quoted("note17_decline_pct", 100.0 * res.decline, 2.44, 2)
    quoted("note17_dividend_add_on_pct", 100.0 * res.dividend_add_on, 0.50, 2)
    quoted("note17_scb_pct", 100.0 * res.scb, 2.94, 2)
    requirement = 0.045 + res.scb + 0.020 + 0.0
    quoted("note17_cet1_requirement_pct", 100.0 * requirement, 9.44, 2)
    quoted("note17_cushion_pct", 100.0 * (res.start_ratio - requirement), 3.06, 2)
    quoted("note17_end_ratio_pct", 100.0 * path[-1] / rwa0, 10.81, 2)
    quoted("note17_end_minus_trough_pp", 100.0 * (path[-1] / rwa0 - res.min_ratio), 0.75, 2)
    # Card reg-17-07: the same trough capital over 10% more RWA.
    quoted("note17_trough_ratio_rwa_up10_pct", 100.0 * trough_capital / (1.10 * rwa0), 9.15, 2)
    # Same bank, half the losses: the 2.5% floor binds.
    half = scb(start_cet1, rwa, [0.5 * x for x in cum], dividends_q4_q7=2_000.0)
    quoted("note17_half_loss_decline_pct", 100.0 * half.decline, 1.22, 2)
    quoted("note17_half_loss_unfloored_pct", 100.0 * (half.decline + half.dividend_add_on), 1.72, 2)
    quoted("note17_half_loss_scb_pct", 100.0 * half.scb, 2.50, 2)
    # Averaging from the SCB effective 1 January 2029: average the two declines, add dividends, then floor.
    avg_decline = 0.5 * (res.decline + 0.0160)
    quoted("note17_averaged_decline_pct", 100.0 * avg_decline, 2.02, 2)
    quoted("note17_averaged_scb_pct", 100.0 * max(0.025, avg_decline + res.dividend_add_on), 2.52, 2)
    # Fed 2026 results, aggregate: 12.8% to a minimum of 11.2%.
    quoted("note17_fed2026_aggregate_decline_pp", 12.8 - 11.2, 1.6, 1)

    # Example 2: IFRS 9 staging (EUR millions).
    r = ifrs9_stage_stress(10_000.0, 0.90, 0.25, (0.008, 0.40, 0.060, 0.45), (0.016, 0.40, 0.140, 0.50))
    quoted("note17_s1_base", r.stage1_base, 28.8, 1)
    quoted("note17_s2_base", r.stage2_base, 27.0, 1)
    quoted("note17_base", r.base, 55.8, 1)
    quoted("note17_s1_stress", r.stage1_stress, 43.2, 1)
    quoted("note17_s2_stress", r.stage2_stress, 227.5, 1)
    quoted("note17_stress", r.stress, 270.7, 1)
    quoted("note17_spike", r.stress - r.base, 214.9, 1)
    quoted("note17_spike_pct", 100.0 * (r.stress - r.base) / r.base, 385.1, 1)
    # Independent attribution of the spike by loan group.
    stay = 6_750.0 * (0.016 * 0.40 - 0.008 * 0.40)
    moved = 2_250.0 * (0.140 * 0.50 - 0.008 * 0.40)
    old_s2 = 1_000.0 * (0.140 * 0.50 - 0.060 * 0.45)
    quoted("note17_migrated_exposure", 9_000.0 * 0.25, 2_250.0, 0)
    quoted("note17_stage1_remaining", 9_000.0 * 0.75, 6_750.0, 0)
    quoted("note17_stage2_stressed_exposure", 1_000.0 + 9_000.0 * 0.25, 3_250.0, 0)
    quoted("note17_attr_stage1_stay", stay, 21.6, 1)
    quoted("note17_attr_migrated", moved, 150.3, 1)
    quoted("note17_attr_old_stage2", old_s2, 43.0, 1)
    agree("note17_attribution_sums", stay + moved + old_s2, r.stress - r.base)
    quoted("note17_migration_share_pct", 100.0 * moved / (r.stress - r.base), 69.9, 1)


# ============================================================================
# Note 18: BCBS 239 data quality
# ============================================================================


def dqi(weights: dict[str, float], scores: dict[str, float]) -> float:
    if abs(sum(weights.values()) - 1.0) > 1e-12:
        raise ValueError("weights must sum to one")
    return sum(weights[d] * scores[d] for d in weights)


def dimension_scores_by_enumeration() -> dict[str, float]:
    """Rebuild the five dimension scores by counting flags on synthetic records, not by dividing the quoted totals."""
    front_office, missing = 1_250_000, 6_250
    ingested = [{"match": True, "valid": True} for _ in range(front_office - missing)]
    for rec in ingested[:18_650]:
        rec["match"] = False
    for rec in ingested[-12_438:]:
        rec["valid"] = False
    feeds_on_time = [True] * 45 + [False] * 5
    parents_agree = [True] * 11_400 + [False] * 600
    n = len(ingested)
    return {
        "C": n / front_office,
        "A": sum(r["match"] for r in ingested) / n,
        "T": sum(feeds_on_time) / len(feeds_on_time),
        "S": sum(parents_agree) / len(parents_agree),
        "V": sum(r["valid"] for r in ingested) / n,
    }


def check_note18() -> None:
    print("=== Note 18: BCBS 239 ===")
    weights = {"C": 0.30, "A": 0.25, "T": 0.20, "S": 0.15, "V": 0.10}
    direct = {
        "C": 1_243_750 / 1_250_000,
        "A": 1_225_100 / 1_243_750,
        "T": 45 / 50,
        "S": 11_400 / 12_000,
        "V": (1_243_750 - 12_438) / 1_243_750,
    }
    enumerated = dimension_scores_by_enumeration()
    for d in weights:
        agree(f"note18_score_{d}_enumeration", direct[d], enumerated[d])
    quoted("note18_score_c", 100.0 * direct["C"], 99.50, 2)
    quoted("note18_score_a", 100.0 * direct["A"], 98.50, 2)
    quoted("note18_score_t", 100.0 * direct["T"], 90.00, 2)
    quoted("note18_score_s", 100.0 * direct["S"], 95.00, 2)
    quoted("note18_score_v", 100.0 * direct["V"], 99.00, 2)
    composite = dqi(weights, direct)
    quoted("note18_dqi", 100.0 * composite, 96.625, 3)
    quoted("note18_dqi_shortfall_pp", 98.0 - 100.0 * composite, 1.375, 3)
    quoted("note18_min_dimension", 100.0 * min(direct.values()), 90.00, 2)
    # What timeliness alone would have to reach for the composite to hit 98% with the other scores unchanged.
    needed_t = (0.98 - (composite - weights["T"] * direct["T"])) / weights["T"]
    quoted("note18_timeliness_needed_pct", 100.0 * needed_t, 96.87, 2)
    quoted("note18_late_feeds_allowed", math.floor((1.0 - needed_t) * 50 + 1e-9), 1.0, 0)

    # Example 2: spreadsheet aggregation error (USD millions).
    true_exposure, reported, recovery = 480.0, 330.0, 0.20
    quoted("note18_dropped_exposure", true_exposure - reported, 150.0, 0)
    quoted("note18_expected_loss", reported * (1.0 - recovery), 264.0, 0)
    quoted("note18_actual_loss", true_exposure * (1.0 - recovery), 384.0, 0)
    quoted("note18_unanticipated_loss", (true_exposure - reported) * (1.0 - recovery), 120.0, 0)
    add_on = 200_000.0 * 0.0025
    quoted("note18_p2r_add_on_capital", add_on, 500.0, 0)
    quoted("note18_add_on_annual_cost", 0.10 * add_on, 50.0, 0)
    # Understated limit utilisation: a 400 single-name limit looked 82.5% used and was 120% used.
    quoted("note18_reported_utilisation_pct", 100.0 * reported / 400.0, 82.5, 1)
    quoted("note18_true_utilisation_pct", 100.0 * true_exposure / 400.0, 120.0, 1)


# ============================================================================
# Note 19: implementation status by jurisdiction
# ============================================================================


def check_note19() -> None:
    print("=== Note 19: implementation by jurisdiction ===")
    # Example 1: reduced BA-CVA for an unrated airline netting set (MAR50.14 to MAR50.16).
    rw = ba_cva_rw("consumer_transport_admin", investment_grade=False)
    quoted("note19_rw_pct", 100.0 * rw, 8.5, 1)
    ead, m = 18_500_000.0, 3.5
    res = ba_cva([Counterparty("airline", rw, (NettingSetExposure(ead, m),))])
    df = supervisory_df(m)
    scva = rw * m * ead * df / 1.4
    agree("note19_df_closed_form", df, (1.0 - math.exp(-0.175)) / 0.175)
    agree("note19_single_name_k_reduced", res.k_reduced, scva)  # one counterparty: sqrt(rho^2 + 1 - rho^2) = 1
    quoted("note19_df", df, 0.9174, 4)
    quoted("note19_df_unrounded", df, 0.91738845, 8)
    quoted("note19_scva", scva, 3_606_483.0, 0)
    quoted("note19_k_cva", res.capital, 2_344_214.0, 0)
    quoted("note19_k_cva_1dp", res.capital, 2_344_214.2, 1)
    quoted("note19_rwa_cva", res.rwa, 29_302_677.0, 0)
    quoted("note19_cet1_at_12pct", 0.12 * res.rwa, 3_516_321.0, 0)
    quoted("note19_annual_cost_at_12pct", 0.12 * 0.12 * res.rwa, 421_959.0, 0)
    # Investment-grade mapping (MAR50.16 allows mapping internal ratings with supervisory approval): 3%.
    ig = ba_cva([Counterparty("airline_ig", 0.03, (NettingSetExposure(ead, m),))])
    quoted("note19_k_cva_ig", ig.capital, 827_370.0, 0)
    quoted("note19_ig_to_nr_ratio", res.capital / ig.capital, 2.8333, 4)

    # Example 2: the same bank under different output-floor calibrations (RWA, USD billions).
    internal, standardised = 485.0, 720.0
    table = {
        "basel_2026": OUTPUT_FLOOR_PHASE_IN[2026],
        "basel_2027": OUTPUT_FLOOR_PHASE_IN[2027],
        "basel_2028": OUTPUT_FLOOR_PHASE_IN[2028],
        "eu_2027": 0.60,
        "canada_now": 0.675,
    }
    expected = {"basel_2026": 485.0, "basel_2027": 504.0, "basel_2028": 522.0, "eu_2027": 485.0, "canada_now": 486.0}
    floor_only = {"basel_2026": 468.0, "basel_2027": 504.0, "basel_2028": 522.0, "eu_2027": 432.0, "canada_now": 486.0}
    for key, factor in table.items():
        value = floored_rwa(internal, standardised, factor)
        agree(f"note19_floor_{key}_independent", value, max(internal, factor * standardised))
        quoted(f"note19_floor_rwa_{key}", factor * standardised, floor_only[key], 1)
        quoted(f"note19_floor_{key}", value, expected[key], 1)
    quoted("note19_canada_bind_margin", floored_rwa(internal, standardised, 0.675) - internal, 1.0, 1)
    quoted("note19_breakeven_factor_pct", 100.0 * internal / standardised, 67.36, 2)
    # RBC90.2 transitional cap: 25% of pre-floor RWA.
    quoted("note19_cap_example", floored_rwa(400.0, 720.0, 0.725, cap=0.25), 500.0, 1)
    quoted("note19_uncapped_example", floored_rwa(400.0, 720.0, 0.725), 522.0, 1)
    # Same CET1 under each RWA: 60 billion.
    quoted("note19_cet1_ratio_485_pct", 100.0 * 60.0 / 485.0, 12.37, 2)
    quoted("note19_cet1_ratio_522_pct", 100.0 * 60.0 / 522.0, 11.49, 2)


# ============================================================================
# Note 20: capital-aware trading, KVA
# ============================================================================


@dataclass(frozen=True)
class KvaInputs:
    notional: float
    maturity_years: int
    capital_ratio: float
    hurdle: float
    rate: float  # continuously compounded discount rate
    cva_rw: float
    ccr_rw: float = 1.0  # SA risk weight of an unrated corporate (CRE20.42, Table 10)


def swap_trade(notional: float, remaining: float, direction: int, trade_id: str) -> Trade:
    return Trade(trade_id, "IR", "", notional, 0.0, remaining, direction=direction, start=0.0, end=remaining, hedging_set="USD")


def capital_profile_engine(inp: KvaInputs, legs: Sequence[tuple[float, int]], t: int) -> tuple[float, float, float]:
    """(EAD, CVA capital, RWA) at the start of year t for swaps (notional, direction) valued at par (V = 0), via the engines."""
    remaining = inp.maturity_years - t
    trades = tuple(swap_trade(n, remaining, d, f"leg{i}") for i, (n, d) in enumerate(legs))
    ead = saccr_ead(NettingSet(trades)).ead
    cva = ba_cva([Counterparty("client", inp.cva_rw, (NettingSetExposure(ead, remaining),))]).capital
    return ead, cva, inp.ccr_rw * ead + 12.5 * cva


def capital_profile_closed_form(inp: KvaInputs, net_notional: float, t: int) -> tuple[float, float, float]:
    """Same profile from the formulas written out by hand: EAD = 1.4 x 0.5% x |N| x SD (multiplier 1, MF 1, RC 0)."""
    tau = inp.maturity_years - t
    sd = (1.0 - math.exp(-0.05 * tau)) / 0.05
    ead = 1.4 * 0.005 * abs(net_notional) * sd * math.sqrt(min(tau, 1.0))
    df = (1.0 - math.exp(-0.05 * tau)) / (0.05 * tau)
    cva = 0.65 * inp.cva_rw * tau * ead * df / 1.4
    return ead, cva, inp.ccr_rw * ead + 12.5 * cva


def kva(inp: KvaInputs, legs: Sequence[tuple[float, int]]) -> tuple[float, list[tuple[float, ...]]]:
    """KVA = sum_t D(t + 1) x hurdle x capital_ratio x RWA(t): capital set at the start of each year, cost paid at its end."""
    rows, total = [], 0.0
    for t in range(inp.maturity_years):
        ead, cva, rwa = capital_profile_engine(inp, legs, t)
        cap = inp.capital_ratio * rwa
        cost = inp.hurdle * cap
        d = math.exp(-inp.rate * (t + 1))
        rows.append((ead, cva, rwa, cap, cost, d, cost * d))
        total += cost * d
    return total, rows


def kva_monthly(inp: KvaInputs, net_notional: float) -> float:
    """Finer grid (monthly capital, monthly cost) with the closed-form profile, to show the discretisation effect."""
    total = 0.0
    for i in range(inp.maturity_years * 12):
        t = i / 12.0
        tau = inp.maturity_years - t
        sd = (1.0 - math.exp(-0.05 * tau)) / 0.05
        ead = 1.4 * 0.005 * abs(net_notional) * sd * math.sqrt(min(tau, 1.0))
        df = (1.0 - math.exp(-0.05 * tau)) / (0.05 * tau)
        rwa = inp.ccr_rw * ead + 12.5 * 0.65 * inp.cva_rw * tau * ead * df / 1.4
        total += inp.hurdle * inp.capital_ratio * rwa / 12.0 * math.exp(-inp.rate * (t + 1.0 / 12.0))
    return total


def check_note20() -> None:
    print("=== Note 20: KVA ===")
    inp = KvaInputs(notional=100e6, maturity_years=5, capital_ratio=0.12, hurdle=0.10, rate=0.04, cva_rw=0.07)
    total, rows = kva(inp, [(100e6, -1)])
    for t in range(inp.maturity_years):
        ead_e, cva_e, rwa_e = capital_profile_engine(inp, [(100e6, -1)], t)
        ead_c, cva_c, rwa_c = capital_profile_closed_form(inp, 100e6, t)
        agree(f"note20_ead_y{t}_closed_form", ead_e, ead_c)
        agree(f"note20_rwa_y{t}_closed_form", rwa_e, rwa_c)
    expected_rows = [
        (3_096_789.0, 445_255.0, 8_662_473.0, 1_039_497.0, 103_950.0, 0.960789, 99_874.0),
        (2_537_769.0, 299_013.0, 6_275_428.0, 753_051.0, 75_305.0, 0.923116, 69_515.0),
        (1_950_088.0, 176_561.0, 4_157_096.0, 498_852.0, 49_885.0, 0.886920, 44_244.0),
        (1_332_276.0, 82_409.0, 2_362_387.0, 283_486.0, 28_349.0, 0.852144, 24_157.0),
        (682_788.0, 21_645.0, 953_350.0, 114_402.0, 11_440.0, 0.818731, 9_366.0),
    ]
    names = ("ead", "k_cva", "rwa", "capital", "cost", "df", "pv")
    for t, (row, exp) in enumerate(zip(rows, expected_rows, strict=True)):
        for name, value, e in zip(names, row, exp, strict=True):
            quoted(f"note20_y{t}_{name}", value, e, 6 if name == "df" else 0)
    quoted("note20_kva", total, 247_157.0, 0)
    ann = sum(math.exp(-inp.rate * (t + 1)) for t in range(5))
    quoted("note20_annuity", ann, 4.4417, 4)
    quoted("note20_kva_running_bp", 1e4 * total / (inp.notional * ann), 5.56, 2)
    monthly = kva_monthly(inp, 100e6)
    quoted("note20_kva_monthly", monthly, 205_832.0, 0)
    quoted("note20_annual_grid_overstatement_pct", 100.0 * (total / monthly - 1.0), 20.0, 0)
    quoted("note20_capital_y4_over_y0_pct", 100.0 * rows[4][3] / rows[0][3], 11.0, 0)
    quoted("note20_ccr_share_y0_pct", 100.0 * rows[0][0] / rows[0][2], 35.75, 2)

    # EVA of the deal (USD): costs are positive numbers subtracted from the client margin.
    margin, cva_cost, fva_cost, ops = 300_000.0, 45_000.0, 35_000.0, 10_000.0
    pre_kva = margin - cva_cost - fva_cost - ops
    quoted("note20_pre_kva", pre_kva, 210_000.0, 0)
    quoted("note20_eva", pre_kva - total, -37_157.0, 0)
    quoted("note20_extra_spread_bp", 1e4 * (total - pre_kva) / (inp.notional * ann), 0.84, 2)
    avg_capital = sum(r[3] for r in rows) / 5.0
    quoted("note20_avg_capital", avg_capital, 537_858.0, 0)
    quoted("note20_return_on_capital_pct", 100.0 * (pre_kva / ann) / avg_capital, 8.79, 2)

    # Example 2: incremental KVA of an offsetting payer swap on 60m.
    after, _ = kva(inp, [(100e6, -1), (60e6, 1)])
    alone, _ = kva(inp, [(60e6, 1)])
    quoted("note20_kva_after", after, 98_863.0, 0)
    quoted("note20_incremental_kva", after - total, -148_294.0, 0)
    quoted("note20_standalone_kva_new", alone, 148_294.0, 0)
    # Independent: with V = 0 and one hedging-set bucket, EAD is linear in |net notional|, so KVA scales with it.
    agree("note20_linearity_after", after, total * 40e6 / 100e6, 1e-9)
    quoted("note20_ead_before_y0", rows[0][0], 3_096_789.0, 0)
    quoted("note20_ead_after_y0", capital_profile_engine(inp, [(100e6, -1), (60e6, 1)], 0)[0], 1_238_716.0, 0)
    # Same trade added to a netting set that is already short 60m in the same direction: incremental KVA is positive.
    same_way, _ = kva(inp, [(100e6, -1), (60e6, -1)])
    quoted("note20_incremental_same_direction", same_way - total, 148_294.0, 0)
    # Constant-capital card: 1m of capital for 3 years at a 10% hurdle, undiscounted and discounted at 4%.
    quoted("note20_card_kva_undiscounted", 0.10 * 1e6 * 3, 300_000.0, 0)
    quoted("note20_card_kva_annual_cost", 0.10 * 1e6, 100_000.0, 0)
    quoted("note20_card_kva_discounted", sum(0.10 * 1e6 * math.exp(-0.04 * t) for t in (1, 2, 3)), 277_083.0, 0)


# ============================================================================
# Note 21: regulatory capital problem set
# ============================================================================


@dataclass(frozen=True)
class CapitalStack:
    cet1: float
    at1: float
    tier2: float
    p2r: float
    ccb: float
    gsib: float
    ccyb: float
    p2r_cet1_share: float = 0.5625  # EU convention, CRD Article 104a(4): 56.25% CET1, 75% Tier 1
    p2r_t1_share: float = 0.75

    def targets(self) -> tuple[float, float, float]:
        buffers = self.ccb + self.gsib + self.ccyb
        return (
            0.045 + self.p2r * self.p2r_cet1_share + buffers,
            0.06 + self.p2r * self.p2r_t1_share + buffers,
            0.08 + self.p2r + buffers,
        )

    def ratios(self, rwa: float) -> tuple[float, float, float]:
        return self.cet1 / rwa, (self.cet1 + self.at1) / rwa, (self.cet1 + self.at1 + self.tier2) / rwa


def check_note21() -> None:
    print("=== Note 21: problem set ===")
    # Problem 1: output floor and capital stack (USD millions).
    internal = 280_000.0 + 35_000.0 + 45_000.0 + 12.5 * 10_000.0
    standardised = 420_000.0 + 55_000.0 + 45_000.0 + 12.5 * 16_000.0
    quoted("note21_p1_internal", internal, 485_000.0, 0)
    quoted("note21_p1_cva_rwa_internal", 12.5 * 10_000.0, 125_000.0, 0)
    quoted("note21_p1_standardised", standardised, 720_000.0, 0)
    binding = floored_rwa(internal, standardised)
    quoted("note21_p1_floor", 0.725 * standardised, 522_000.0, 0)
    quoted("note21_p1_binding", binding, 522_000.0, 0)
    quoted("note21_p1_delta", binding - internal, 37_000.0, 0)
    quoted("note21_p1_delta_pct", 100.0 * (binding - internal) / internal, 7.63, 2)
    stack = CapitalStack(cet1=44_000.0, at1=6_000.0, tier2=8_000.0, p2r=0.015, ccb=0.025, gsib=0.015, ccyb=0.005)
    t_cet1, t_t1, t_total = stack.targets()
    quoted("note21_p1_p2r_cet1_pct", 100.0 * 0.015 * 0.5625, 0.84375, 5)
    quoted("note21_p1_target_cet1_pct", 100.0 * t_cet1, 9.84375, 5)
    quoted("note21_p1_target_t1_pct", 100.0 * t_t1, 11.625, 3)
    quoted("note21_p1_p2r_t1_pct", 100.0 * 0.015 * stack.p2r_t1_share, 1.125, 3)
    quoted("note21_p1_target_total_pct", 100.0 * t_total, 14.0, 1)
    r_cet1, r_t1, r_total = stack.ratios(binding)
    quoted("note21_p1_cet1_pct", 100.0 * r_cet1, 8.43, 2)
    quoted("note21_p1_t1_pct", 100.0 * r_t1, 9.58, 2)
    quoted("note21_p1_total_pct", 100.0 * r_total, 11.11, 2)
    quoted("note21_p1_cet1_gap_pct", 100.0 * (r_cet1 - t_cet1), -1.41, 2)
    quoted("note21_p1_cet1_gap", (r_cet1 - t_cet1) * binding, -7_384.4, 1)
    agree("note21_p1_cet1_gap_direct", (r_cet1 - t_cet1) * binding, 44_000.0 - t_cet1 * binding)
    quoted("note21_p1_t1_gap", (r_t1 - t_t1) * binding, -10_682.5, 1)
    quoted("note21_p1_total_gap", (r_total - t_total) * binding, -15_080.0, 0)
    pre = stack.ratios(internal)
    quoted("note21_p1_pre_floor_cet1_pct", 100.0 * pre[0], 9.07, 2)
    quoted("note21_p1_pre_floor_t1_pct", 100.0 * pre[1], 10.31, 2)
    quoted("note21_p1_pre_floor_total_pct", 100.0 * pre[2], 11.96, 2)
    quoted("note21_p1_cet1_needed_at_floor", t_cet1 * binding, 51_384.4, 1)

    # Problem 2: SA-CCR, three USD swaps, via the engine and by hand.
    trades = (
        Trade("t1", "IR", "", 100e6, 2.5e6, 5.0, direction=-1, end=5.0, hedging_set="USD"),
        Trade("t2", "IR", "", 50e6, -1.8e6, 10.0, direction=1, end=10.0, hedging_set="USD"),
        Trade("t3", "IR", "", 80e6, 0.3e6, 2.0, direction=-1, end=2.0, hedging_set="USD"),
    )
    unm = saccr_ead(NettingSet(trades))
    mar = saccr_ead(NettingSet(trades, collateral=0.8e6, margined=True, threshold=0.0, mta=0.05e6, nica=0.0, mpor_days=10))
    sd = {e: (1.0 - math.exp(-0.05 * e)) / 0.05 for e in (5.0, 10.0, 2.0)}
    d2 = -100.0 * sd[5.0] - 80.0 * sd[2.0]
    d3 = 50.0 * sd[10.0]
    en = math.sqrt(d2 * d2 + d3 * d3 + 1.4 * d2 * d3)
    addon = 0.005 * en * 1e6
    agree("note21_p2_addon_engine", unm.addon_aggregate, addon)
    quoted("note21_p2_sd5", sd[5.0], 4.4240, 4)
    quoted("note21_p2_sd10", sd[10.0], 7.8694, 4)
    quoted("note21_p2_sd2", sd[2.0], 1.9033, 4)
    quoted("note21_p2_d_bucket2", d2, -594.66, 2)
    quoted("note21_p2_d_bucket3", d3, 393.47, 2)
    quoted("note21_p2_en", en, 425.28, 2)
    quoted("note21_p2_en_4dp", en, 425.2823, 4)
    quoted("note21_p2_addon", addon, 2_126_412.0, 0)
    quoted("note21_p2_addon_1dp", addon, 2_126_411.6, 1)
    quoted("note21_p2_v", unm.v, 1_000_000.0, 0)
    quoted("note21_p2_unm_exponent", 1e6 / (2 * 0.95 * addon), 0.2475, 4)
    quoted("note21_p2_unm_multiplier", unm.multiplier, 1.0, 4)
    quoted("note21_p2_unm_ead", unm.ead, 4_376_976.0, 0)
    agree("note21_p2_unm_ead_hand", unm.ead, 1.4 * (1e6 + addon))
    quoted("note21_p2_mar_rc", mar.rc, 200_000.0, 0)
    quoted("note21_p2_mf", 1.5 * math.sqrt(10 / 250), 0.30, 2)
    quoted("note21_p2_mar_addon", mar.addon_aggregate, 637_923.0, 0)
    quoted("note21_p2_mar_addon_1dp", mar.addon_aggregate, 637_923.5, 1)
    quoted("note21_p2_mar_multiplier", mar.multiplier, 1.0, 4)
    quoted("note21_p2_mar_ead", mar.ead, 1_173_093.0, 0)
    agree("note21_p2_mar_ead_hand", mar.ead, 1.4 * (0.2e6 + 0.3 * addon))
    quoted("note21_p2_reduction", unm.ead - mar.ead, 3_203_883.0, 0)
    quoted("note21_p2_reduction_pct", 100.0 * (unm.ead - mar.ead) / unm.ead, 73.2, 1)
    # Card reg-21-27: split the reduction into the maturity-factor part and the replacement-cost part.
    addon_cut = unm.addon_aggregate - mar.addon_aggregate
    from_mf = 1.4 * addon_cut
    from_rc = 1.4 * (unm.rc - mar.rc)
    agree("note21_p2_split_sums", from_mf + from_rc, unm.ead - mar.ead)
    quoted("note21_p2_addon_cut", addon_cut, 1_488_488.0, 0)
    quoted("note21_p2_ead_cut_from_mf", from_mf, 2_083_883.0, 0)
    quoted("note21_p2_ead_cut_from_rc", from_rc, 1_120_000.0, 0)
    quoted("note21_p2_mf_share_pct", 100.0 * from_mf / (unm.ead - mar.ead), 65.0, 1)
    quoted("note21_card_exp_minus_half", math.exp(-0.5), 0.60653, 5)

    # Card answers.
    over = 0.05 + 0.95 * math.exp(-1e6 / (2.0 * 0.95 * addon))
    quoted("note21_card_multiplier_overcollateralised", over, 0.7917, 4)
    irb = irb_corporate(pd=0.01, lgd=0.45, ead=1.0, maturity=2.5)
    quoted("note21_card_irb_r", irb.correlation, 0.1928, 4)
    quoted("note21_card_irb_k_pct", 100.0 * irb.k, 7.39, 2)
    quoted("note21_card_irb_rw_pct", 100.0 * irb.risk_weight, 92.32, 2)
    quoted("note21_card_bic", bic(35_000.0), 5_370.0, 0)
    agree("note21_card_bic_hand", bic(35_000.0), 0.12 * 1_000 + 0.15 * 29_000 + 0.18 * 5_000)
    quoted("note21_card_ilm_equal", ilm(1.0, 1.0), 1.0, 4)
    quoted("note21_card_ilm_double", ilm(2.0, 1.0), 1.2411, 4)
    outflow = 100.0 * RUN_OFF["operational deposits"]
    outflow += 100.0 * RUN_OFF["non-financial corporate non-operational, uninsured"]
    outflow += 100.0 * RUN_OFF["financial institution unsecured"]
    quoted("note21_card_lcr_outflows", outflow, 165.0, 0)
    band = mda(0.068, ccyb=0.0, gsib_hla=0.015)
    quoted("note21_card_mda_quartile", float(band.quartile), 3.0, 0)
    quoted("note21_card_mda_band3_low_pct", 100.0 * band.quartile_bounds[2], 6.5, 1)
    quoted("note21_card_mda_band3_high_pct", 100.0 * band.quartile_bounds[3], 7.5, 1)
    quoted("note21_card_mda_payout_pct", 100.0 * band.max_payout, 40.0, 0)
    quoted("note21_card_leverage_pct", 100.0 * 50.0 / 1_500.0, 3.33, 2)
    quoted("note21_card_leverage_req_pct", 100.0 * (0.03 + 0.5 * 0.015), 3.75, 2)
    quoted("note21_card_scb_pct", 100.0 * max(0.025, (0.13 - 0.105) + 1.0 / 200.0), 3.0, 1)
    quoted("note21_card_floor_2027_pct", 100.0 * OUTPUT_FLOOR_PHASE_IN[2027], 70.0, 1)
    k, s = amber_surcharge({"a": 30.0, "b": 90.0}, {"a"}, 80.0, 120.0)
    quoted("note21_card_amber_k", k, 0.125, 3)
    quoted("note21_card_amber_surcharge", s, 5.0, 1)


def run_tests() -> None:
    check_note13()
    check_note17()
    check_note18()
    check_note19()
    check_note20()
    check_note21()
    print(f"\nAll {len(QUOTED_LOG)} quoted numbers passed their assertions.")


if __name__ == "__main__":
    run_tests()
