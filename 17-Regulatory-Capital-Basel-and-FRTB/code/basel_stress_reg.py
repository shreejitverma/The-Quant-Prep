"""Stress testing, data aggregation quality, jurisdiction rules, KVA, and comprehensive problem set.

Reference implementation for notes:
* 13 (FRTB implementation challenges and desk strategy)
* 17 (stress testing: CCAR, DFAST, and EBA)
* 18 (BCBS 239 risk data aggregation and reporting)
* 19 (implementation status by jurisdiction)
* 20 (capital-aware trading: KVA and RWA limits)
* 21 (regulatory capital problem set)

Computes, prints, and asserts every number quoted in notes 13, 17, 18, 19, 20, and 21.
Run it with:
    python3 17-Regulatory-Capital-Basel-and-FRTB/code/basel_stress_reg.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass

QUOTED_LOG: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number a note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-7
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED_LOG.append(label)
    print(f"    {label}: {value:,.{decimals}f}")
    return value


# ============================================================================
# 1. Note 13: FRTB Implementation Challenges and Desk Strategy
# ============================================================================


def frtb_compute_sizing(
    n_positions: int,
    n_scenarios: int,
    n_liquidity_horizons: int,
    n_runs: int,
    batch_hours: float,
) -> tuple[int, float]:
    """Calculate total overnight full valuations and sustained throughput."""
    total_valuations = n_positions * n_scenarios * n_liquidity_horizons * n_runs
    batch_seconds = batch_hours * 3600.0
    throughput = total_valuations / batch_seconds
    return total_valuations, throughput


@dataclass(frozen=True)
class DeskImaDecision:
    capital_sa: float
    imcc: float
    drc_ima: float
    ses: float
    cost_of_equity: float
    it_annual_cost: float

    @property
    def capital_ima(self) -> float:
        return self.imcc + self.drc_ima + self.ses

    @property
    def gross_capital_savings(self) -> float:
        return self.capital_sa - self.capital_ima

    @property
    def savings_pct(self) -> float:
        return self.gross_capital_savings / self.capital_sa

    @property
    def annual_capital_benefit(self) -> float:
        return self.cost_of_equity * self.gross_capital_savings

    @property
    def net_annual_economic_value(self) -> float:
        return self.annual_capital_benefit - self.it_annual_cost


def amber_pla_surcharge(
    c_ima: float,
    c_sa: float,
    k_factor: float,
    cost_of_equity: float,
) -> tuple[float, float]:
    """EBA RTS Amber PLA formula capital surcharge and annual PnL drag."""
    delta_capital = k_factor * max(0.0, c_sa - c_ima)
    annual_drag = cost_of_equity * delta_capital
    return delta_capital, annual_drag


# ============================================================================
# 2. Note 17: Stress Testing: CCAR, DFAST, and EBA
# ============================================================================


@dataclass(frozen=True)
class StressCapitalBufferResult:
    starting_cet1: float
    starting_rwa: float
    starting_cet1_ratio: float
    trough_cet1: float
    trough_rwa: float
    trough_cet1_ratio: float
    peak_to_trough_depletion: float
    planned_annual_dividends: float
    avg_projected_rwa: float
    dividend_add_on: float
    scb: float
    g_sib_surcharge: float
    ccyb: float
    pillar1_minimum: float
    total_cet1_requirement: float
    capital_cushion: float


def compute_scb(
    starting_cet1: float,
    starting_rwa: float,
    trough_after_tax_loss: float,
    trough_rwa: float,
    planned_annual_dividends: float,
    avg_projected_rwa: float,
    g_sib_surcharge: float = 0.02,
    ccyb: float = 0.0,
    pillar1_min: float = 0.045,
    scb_floor: float = 0.025,
) -> StressCapitalBufferResult:
    """Compute the US Stress Capital Buffer (SCB) and resulting CET1 capital stack."""
    starting_ratio = starting_cet1 / starting_rwa
    trough_cet1 = starting_cet1 - trough_after_tax_loss
    trough_ratio = trough_cet1 / trough_rwa
    depletion = starting_ratio - trough_ratio
    dividend_add_on = planned_annual_dividends / avg_projected_rwa
    scb = max(scb_floor, depletion + dividend_add_on)
    total_req = pillar1_min + scb + g_sib_surcharge + ccyb
    cushion = starting_ratio - total_req
    return StressCapitalBufferResult(
        starting_cet1=starting_cet1,
        starting_rwa=starting_rwa,
        starting_cet1_ratio=starting_ratio,
        trough_cet1=trough_cet1,
        trough_rwa=trough_rwa,
        trough_cet1_ratio=trough_ratio,
        peak_to_trough_depletion=depletion,
        planned_annual_dividends=planned_annual_dividends,
        avg_projected_rwa=avg_projected_rwa,
        dividend_add_on=dividend_add_on,
        scb=scb,
        g_sib_surcharge=g_sib_surcharge,
        ccyb=ccyb,
        pillar1_minimum=pillar1_min,
        total_cet1_requirement=total_req,
        capital_cushion=cushion,
    )


@dataclass(frozen=True)
class Ifrs9StagingResult:
    baseline_stage1_prov: float
    baseline_stage2_prov: float
    total_baseline_prov: float
    stressed_stage1_prov: float
    stressed_stage2_prov: float
    total_stressed_prov: float
    net_provision_spike: float
    spike_pct: float


def compute_ifrs9_staging_stress(
    total_portfolio: float,
    stage1_share: float,
    stage2_share: float,
    base_s1_pd: float,
    base_s1_lgd: float,
    base_s2_pd: float,
    base_s2_lgd: float,
    s1_migration_rate: float,
    stressed_s1_pd: float,
    stressed_s1_lgd: float,
    stressed_s2_pd: float,
    stressed_s2_lgd: float,
) -> Ifrs9StagingResult:
    """Model IFRS 9 staging transitions and ECL spikes under macroeconomic stress."""
    s1_exposure = total_portfolio * stage1_share
    s2_exposure = total_portfolio * stage2_share

    base_s1_prov = s1_exposure * base_s1_pd * base_s1_lgd
    base_s2_prov = s2_exposure * base_s2_pd * base_s2_lgd
    tot_base = base_s1_prov + base_s2_prov

    migrated = s1_exposure * s1_migration_rate
    rem_s1 = s1_exposure - migrated
    stress_s2_exp = s2_exposure + migrated

    str_s1_prov = rem_s1 * stressed_s1_pd * stressed_s1_lgd
    str_s2_prov = stress_s2_exp * stressed_s2_pd * stressed_s2_lgd
    tot_str = str_s1_prov + str_s2_prov
    spike = tot_str - tot_base
    spike_pct = spike / tot_base

    return Ifrs9StagingResult(
        baseline_stage1_prov=base_s1_prov,
        baseline_stage2_prov=base_s2_prov,
        total_baseline_prov=tot_base,
        stressed_stage1_prov=str_s1_prov,
        stressed_stage2_prov=str_s2_prov,
        total_stressed_prov=tot_str,
        net_provision_spike=spike,
        spike_pct=spike_pct,
    )


# ============================================================================
# 3. Note 18: BCBS 239 Risk Data Aggregation and Reporting
# ============================================================================


def compute_dqi(
    weights: dict[str, float],
    scores: dict[str, float],
) -> float:
    """Calculate multi-dimensional Data Quality Index (DQI)."""
    assert abs(sum(weights.values()) - 1.0) < 1e-9
    return sum(weights[dim] * scores[dim] for dim in weights)


def euc_reconciliation_loss(
    gross_exposure: float,
    reported_exposure: float,
    recovery_rate: float,
    bank_rwa: float,
    p2r_addon_pct: float,
) -> tuple[float, float, float, float]:
    """Calculate loss gap and capital add-on from EUC manual failure."""
    lgd = 1.0 - recovery_rate
    expected_loss = reported_exposure * lgd
    actual_loss = gross_exposure * lgd
    unanticipated_loss = actual_loss - expected_loss
    capital_penalty = bank_rwa * p2r_addon_pct
    return expected_loss, actual_loss, unanticipated_loss, capital_penalty


# ============================================================================
# 4. Note 19: Implementation Status by Jurisdiction
# ============================================================================


def illustrative_cva_charge(
    ead: float,
    maturity: float,
    rw: float,
    alpha: float = 0.5,
    rwa_multiplier: float = 12.5,
    cet1_target_ratio: float = 0.12,
    cost_of_equity: float = 0.12,
) -> tuple[float, float, float, float]:
    """Calculate illustrative reduced BA-CVA capital, RWA, CET1, and annual drag."""
    k_cva = alpha * rw * maturity * ead
    rwa_cva = rwa_multiplier * k_cva
    req_capital = cet1_target_ratio * rwa_cva
    annual_drag = cost_of_equity * req_capital
    return k_cva, rwa_cva, req_capital, annual_drag


# ============================================================================
# 5. Note 20: Capital-Aware Trading: KVA and RWA Limits
# ============================================================================


@dataclass(frozen=True)
class KvaDealSchedule:
    years: list[int]
    discount_factors: list[float]
    stressed_rwas: list[float]
    capital_ratio: float
    hurdle_rate: float

    @property
    def required_capitals(self) -> list[float]:
        return [self.capital_ratio * rwa for rwa in self.stressed_rwas]

    @property
    def holding_costs(self) -> list[float]:
        return [self.hurdle_rate * k for k in self.required_capitals]

    @property
    def pv_of_costs(self) -> list[float]:
        return [df * cost for df, cost in zip(self.discount_factors, self.holding_costs, strict=True)]

    @property
    def total_kva(self) -> float:
        return sum(self.pv_of_costs)

    @property
    def avg_rwa(self) -> float:
        return sum(self.stressed_rwas) / len(self.stressed_rwas)


def compute_eva(
    pv: float,
    cva: float,
    fva: float,
    costs: float,
    kva: float,
) -> float:
    """Calculate Economic Value Added (EVA) incorporating CVA, FVA, and KVA."""
    economic_pnl = pv - abs(cva) - abs(fva) - abs(costs)
    return economic_pnl - kva


# ============================================================================
# 6. Note 21: Regulatory Capital Problem Set
# ============================================================================


@dataclass(frozen=True)
class OutputFloorCheck:
    rwa_internal: float
    rwa_standardized: float
    floor_pct: float
    cet1: float
    at1: float
    tier2: float
    p1_cet1_min: float
    p2r: float
    p2r_cet1_share: float
    ccb: float
    gsib: float
    ccyb: float

    @property
    def floor_threshold(self) -> float:
        return self.floor_pct * self.rwa_standardized

    @property
    def binding_rwa(self) -> float:
        return max(self.rwa_internal, self.floor_threshold)

    @property
    def rwa_delta(self) -> float:
        return self.binding_rwa - self.rwa_internal

    @property
    def rwa_delta_pct(self) -> float:
        return self.rwa_delta / self.rwa_internal

    @property
    def target_cet1_ratio(self) -> float:
        return self.p1_cet1_min + (self.p2r * self.p2r_cet1_share) + self.ccb + self.gsib + self.ccyb

    @property
    def target_total_ratio(self) -> float:
        return 0.08 + self.p2r + self.ccb + self.gsib + self.ccyb

    @property
    def actual_cet1_ratio(self) -> float:
        return self.cet1 / self.binding_rwa

    @property
    def actual_total_capital(self) -> float:
        return self.cet1 + self.at1 + self.tier2

    @property
    def actual_total_ratio(self) -> float:
        return self.actual_total_capital / self.binding_rwa

    @property
    def cet1_surplus_pct(self) -> float:
        return self.actual_cet1_ratio - self.target_cet1_ratio

    @property
    def cet1_surplus_dollars(self) -> float:
        return self.cet1_surplus_pct * self.binding_rwa

    @property
    def total_surplus_pct(self) -> float:
        return self.actual_total_ratio - self.target_total_ratio

    @property
    def total_surplus_dollars(self) -> float:
        return self.total_surplus_pct * self.binding_rwa


def saccr_swap_duration(t_start: float, t_end: float) -> float:
    """Supervisory duration SD = (exp(-0.05*S) - exp(-0.05*E)) / 0.05."""
    return (math.exp(-0.05 * t_start) - math.exp(-0.05 * t_end)) / 0.05


def saccr_multiplier(v: float, c: float, add_on: float) -> float:
    """SA-CCR PFE multiplier = min(1, 0.05 + 0.95 * exp((V - C) / (2 * 0.95 * AddOn)))."""
    val = (v - c) / (2.0 * 0.95 * add_on)
    return min(1.0, 0.05 + 0.95 * math.exp(val))


# ============================================================================
# Assertions and Test Suite
# ============================================================================


def run_tests() -> None:
    """Verify and assert all numbers across notes 13, 17, 18, 19, 20, and 21."""
    print("=== Testing Note 13: FRTB Implementation Challenges ===")
    v_total, thr = frtb_compute_sizing(500_000, 250, 5, 3, 3.0)
    quoted("sizing_derivation_total_valuations", float(v_total), 1_875_000_000.0, 0)
    quoted("sizing_derivation_throughput", thr, 173_611.11, 0)

    # Example 1
    v_ex1, thr_ex1 = frtb_compute_sizing(400_000, 250, 5, 3, 2.5)
    quoted("note13_ex1_total_valuations", float(v_ex1), 1_500_000_000.0, 0)
    quoted("note13_ex1_throughput", thr_ex1, 166_666.67, 0)
    cpu_cores = thr_ex1 / 2000.0
    quoted("note13_ex1_cpu_cores", cpu_cores, 83.33, 0)
    complex_val = 0.20 * v_ex1
    quoted("note13_ex1_complex_valuations", complex_val, 300_000_000.0, 0)
    complex_thr = complex_val / (2.5 * 3600.0)
    quoted("note13_ex1_complex_throughput", complex_thr, 33_333.33, 0)
    complex_cores = complex_thr / 50.0
    quoted("note13_ex1_complex_cpu_cores", complex_cores, 666.67, 0)

    # Example 2
    desk = DeskImaDecision(
        capital_sa=250_000_000.0,
        imcc=120_000_000.0,
        drc_ima=40_000_000.0,
        ses=80_000_000.0,
        cost_of_equity=0.12,
        it_annual_cost=1_700_000.0,
    )
    quoted("note13_ex2_capital_ima", desk.capital_ima, 240_000_000.0, 0)
    quoted("note13_ex2_savings", desk.gross_capital_savings, 10_000_000.0, 0)
    quoted("note13_ex2_savings_pct", desk.savings_pct * 100.0, 4.0, 1)
    quoted("note13_ex2_annual_benefit", desk.annual_capital_benefit, 1_200_000.0, 0)
    quoted("note13_ex2_net_economic_value", desk.net_annual_economic_value, -500_000.0, 0)

    # Question 9 (Amber PLA surcharge)
    amber_delta, amber_drag = amber_pla_surcharge(100_000_000.0, 200_000_000.0, 0.25, 0.12)
    quoted("note13_q9_amber_delta_capital", amber_delta, 25_000_000.0, 0)
    quoted("note13_q9_amber_drag", amber_drag, 3_000_000.0, 0)

    print("=== Testing Note 17: Stress Testing CCAR, DFAST, and EBA ===")
    scb_res = compute_scb(
        starting_cet1=50_000.0,
        starting_rwa=400_000.0,
        trough_after_tax_loss=9_500.0,
        trough_rwa=425_000.0,
        planned_annual_dividends=2_000.0,
        avg_projected_rwa=410_000.0,
        g_sib_surcharge=0.02,
        ccyb=0.0,
    )
    quoted("note17_starting_cet1_ratio", scb_res.starting_cet1_ratio * 100.0, 12.50, 2)
    quoted("note17_trough_cet1", scb_res.trough_cet1, 40_500.0, 0)
    quoted("note17_trough_cet1_ratio", scb_res.trough_cet1_ratio * 100.0, 9.53, 2)
    quoted("note17_depletion", scb_res.peak_to_trough_depletion * 100.0, 2.97, 2)
    quoted("note17_div_add_on", scb_res.dividend_add_on * 100.0, 0.49, 2)
    quoted("note17_scb", scb_res.scb * 100.0, 3.46, 2)
    quoted("note17_required_cet1", scb_res.total_cet1_requirement * 100.0, 9.96, 2)
    quoted("note17_cushion", scb_res.capital_cushion * 100.0, 2.54, 2)

    # Note 17 Example 2 (IFRS 9 Staging)
    ifrs9_res = compute_ifrs9_staging_stress(
        total_portfolio=10_000.0,
        stage1_share=0.90,
        stage2_share=0.10,
        base_s1_pd=0.008,
        base_s1_lgd=0.40,
        base_s2_pd=0.060,
        base_s2_lgd=0.45,
        s1_migration_rate=0.25,
        stressed_s1_pd=0.016,
        stressed_s1_lgd=0.40,
        stressed_s2_pd=0.140,
        stressed_s2_lgd=0.50,
    )
    quoted("note17_base_s1_prov", ifrs9_res.baseline_stage1_prov, 28.8, 1)
    quoted("note17_base_s2_prov", ifrs9_res.baseline_stage2_prov, 27.0, 1)
    quoted("note17_base_tot_prov", ifrs9_res.total_baseline_prov, 55.8, 1)
    quoted("note17_str_s1_prov", ifrs9_res.stressed_stage1_prov, 43.2, 1)
    quoted("note17_str_s2_prov", ifrs9_res.stressed_stage2_prov, 227.5, 1)
    quoted("note17_str_tot_prov", ifrs9_res.total_stressed_prov, 270.7, 1)
    quoted("note17_net_spike", ifrs9_res.net_provision_spike, 214.9, 1)
    quoted("note17_spike_pct", ifrs9_res.spike_pct * 100.0, 385.1, 0)

    print("=== Testing Note 18: BCBS 239 Risk Data Aggregation ===")
    dqi_weights = {"C": 0.30, "A": 0.25, "T": 0.20, "S": 0.15, "V": 0.10}
    dqi_scores = {
        "C": 1_243_750 / 1_250_000,
        "A": 1_225_100 / 1_243_750,
        "T": 45 / 50,
        "S": 11_400 / 12_000,
        "V": (1_243_750 - 12_438) / 1_243_750,
    }
    quoted("note18_score_c", dqi_scores["C"] * 100.0, 99.50, 2)
    quoted("note18_score_a", dqi_scores["A"] * 100.0, 98.50, 2)
    quoted("note18_score_t", dqi_scores["T"] * 100.0, 90.00, 2)
    quoted("note18_score_s", dqi_scores["S"] * 100.0, 95.00, 2)
    quoted("note18_score_v", dqi_scores["V"] * 100.0, 99.00, 2)
    dqi_composite = compute_dqi(dqi_weights, dqi_scores)
    quoted("note18_dqi_composite", dqi_composite * 100.0, 96.625, 3)

    exp_l, act_l, unant_l, p2r_pen = euc_reconciliation_loss(480.0, 330.0, 0.20, 200_000.0, 0.0025)
    quoted("note18_euc_expected_loss", exp_l, 264.0, 0)
    quoted("note18_euc_actual_loss", act_l, 384.0, 0)
    quoted("note18_euc_unanticipated_loss", unant_l, 120.0, 0)
    quoted("note18_euc_capital_penalty", p2r_pen, 500.0, 0)

    print("=== Testing Note 19: Implementation Status by Jurisdiction ===")
    k_cva, rwa_cva, req_cap, ann_drag = illustrative_cva_charge(
        ead=18_500_000.0,
        maturity=3.5,
        rw=0.014,
        alpha=0.5,
        rwa_multiplier=12.5,
        cet1_target_ratio=0.12,
        cost_of_equity=0.12,
    )
    quoted("note19_cva_k", k_cva, 453_250.0, 0)
    quoted("note19_cva_rwa", rwa_cva, 5_665_625.0, 0)
    quoted("note19_cva_req_cap", req_cap, 679_875.0, 0)
    quoted("note19_cva_ann_drag", ann_drag, 81_585.0, 0)

    # Example 2
    erba_rwa = 410_000.0 + 45_000.0 + 60_000.0
    quoted("note19_erba_rwa", erba_rwa, 515_000.0, 0)
    sa_ratio = 60_000.0 / 500_000.0
    quoted("note19_sa_ratio", sa_ratio * 100.0, 12.00, 2)
    erba_ratio = 60_000.0 / 515_000.0
    quoted("note19_erba_ratio", erba_ratio * 100.0, 11.65, 2)

    print("=== Testing Note 20: Capital-Aware Trading: KVA and RWA Limits ===")
    kva_deal = KvaDealSchedule(
        years=[1, 2, 3, 4, 5],
        discount_factors=[0.960, 0.920, 0.880, 0.840, 0.800],
        stressed_rwas=[3_200_000.0, 3_800_000.0, 3_500_000.0, 2_600_000.0, 1_400_000.0],
        capital_ratio=0.12,
        hurdle_rate=0.10,
    )
    quoted("note20_kva_cost_y1", kva_deal.pv_of_costs[0], 36_864.0, 0)
    quoted("note20_kva_cost_y2", kva_deal.pv_of_costs[1], 41_952.0, 0)
    quoted("note20_kva_cost_y3", kva_deal.pv_of_costs[2], 36_960.0, 0)
    quoted("note20_kva_cost_y4", kva_deal.pv_of_costs[3], 26_208.0, 0)
    quoted("note20_kva_cost_y5", kva_deal.pv_of_costs[4], 13_440.0, 0)
    quoted("note20_total_kva", kva_deal.total_kva, 155_424.0, 0)

    eva = compute_eva(pv=250_000.0, cva=-45_000.0, fva=-35_000.0, costs=-10_000.0, kva=kva_deal.total_kva)
    quoted("note20_eva", eva, 4_576.0, 0)
    quoted("note20_avg_rwa", kva_deal.avg_rwa, 2_900_000.0, 0)
    annual_profit = 160_000.0 / 5.0
    quoted("note20_annual_profit", annual_profit, 32_000.0, 0)
    rorwa = annual_profit / kva_deal.avg_rwa
    quoted("note20_rorwa", rorwa * 100.0, 1.103, 3)

    # Example 2: Negative incremental KVA
    delta_kva = 360_000.0 - 480_000.0
    quoted("note20_ex2_delta_kva", delta_kva, -120_000.0, 0)
    eva_ex2 = -10_000.0 - delta_kva
    quoted("note20_ex2_eva", eva_ex2, 110_000.0, 0)

    print("=== Testing Note 21: Regulatory Capital Problem Set ===")
    floor_check = OutputFloorCheck(
        rwa_internal=485_000.0,
        rwa_standardized=720_000.0,
        floor_pct=0.725,
        cet1=44_000.0,
        at1=6_000.0,
        tier2=8_000.0,
        p1_cet1_min=0.045,
        p2r=0.015,
        p2r_cet1_share=0.5625,
        ccb=0.025,
        gsib=0.015,
        ccyb=0.005,
    )
    quoted("note21_p1_floor_threshold", floor_check.floor_threshold, 522_000.0, 0)
    quoted("note21_p1_binding_rwa", floor_check.binding_rwa, 522_000.0, 0)
    quoted("note21_p1_rwa_delta", floor_check.rwa_delta, 37_000.0, 0)
    quoted("note21_p1_rwa_delta_pct", floor_check.rwa_delta_pct * 100.0, 7.63, 2)
    quoted("note21_p1_target_cet1_ratio", floor_check.target_cet1_ratio * 100.0, 9.84, 2)
    quoted("note21_p1_actual_cet1_ratio", floor_check.actual_cet1_ratio * 100.0, 8.43, 2)
    quoted("note21_p1_cet1_surplus_pct", floor_check.cet1_surplus_pct * 100.0, -1.41, 2)
    quoted("note21_p1_cet1_surplus_dollars", floor_check.cet1_surplus_dollars, -7_384.4, 1)
    quoted("note21_p1_total_cap", floor_check.actual_total_capital, 58_000.0, 0)
    quoted("note21_p1_actual_total_ratio", floor_check.actual_total_ratio * 100.0, 11.11, 2)
    quoted("note21_p1_total_surplus_pct", floor_check.total_surplus_pct * 100.0, -2.89, 2)
    quoted("note21_p1_total_surplus_dollars", floor_check.total_surplus_dollars, -15_080.0, 0)

    # Problem 2: SA-CCR
    sd1 = saccr_swap_duration(0.0, 5.0)
    sd2 = saccr_swap_duration(0.0, 10.0)
    sd3 = saccr_swap_duration(0.0, 2.0)
    quoted("note21_p2_sd1", sd1, 4.4240, 4)
    quoted("note21_p2_sd2", sd2, 7.8694, 4)
    quoted("note21_p2_sd3", sd3, 1.9033, 4)

    d_b2 = (-1.0 * 100.0 * sd1) + (-1.0 * 80.0 * sd3)
    d_b3 = 1.0 * 50.0 * sd2
    quoted("note21_p2_d_bucket2", d_b2, -594.66, 2)
    quoted("note21_p2_d_bucket3", d_b3, 393.47, 2)

    d_usd = math.sqrt(d_b2**2 + d_b3**2 + 1.4 * d_b2 * d_b3)
    quoted("note21_p2_d_usd", d_usd, 425.28, 2)

    addon_ir = 0.005 * 425.28 * 1_000_000.0
    quoted("note21_p2_addon_ir", addon_ir, 2_126_400.0, 0)

    # Unmargined
    rc_unmargined = 1_000_000.0
    mult_unmargined = saccr_multiplier(1_000_000.0, 0.0, addon_ir)
    quoted("note21_p2_mult_unmargined", mult_unmargined, 1.0, 1)
    pfe_unmargined = mult_unmargined * addon_ir
    quoted("note21_p2_pfe_unmargined", pfe_unmargined, 2_126_400.0, 0)
    ead_unmargined = 1.4 * (rc_unmargined + pfe_unmargined)
    quoted("note21_p2_ead_unmargined", ead_unmargined, 4_376_960.0, 0)

    # Margined
    rc_margined = max(1_000_000.0 - 800_000.0, 50_000.0, 0.0)
    quoted("note21_p2_rc_margined", rc_margined, 200_000.0, 0)
    mf = 1.5 * math.sqrt(10.0 / 250.0)
    quoted("note21_p2_mf", mf, 0.30, 2)
    addon_margined = mf * addon_ir
    quoted("note21_p2_addon_margined", addon_margined, 637_920.0, 0)
    pfe_margined = 1.0 * addon_margined
    quoted("note21_p2_pfe_margined", pfe_margined, 637_920.0, 0)
    ead_margined = 1.4 * (rc_margined + pfe_margined)
    quoted("note21_p2_ead_margined", ead_margined, 1_173_088.0, 0)

    ead_reduction = ead_unmargined - ead_margined
    quoted("note21_p2_ead_reduction", ead_reduction, 3_203_872.0, 0)
    ead_red_pct = ead_reduction / ead_unmargined
    quoted("note21_p2_ead_red_pct", ead_red_pct * 100.0, 73.2, 1)

    print(f"\nAll {len(QUOTED_LOG)} calculations passed assertions!")


if __name__ == "__main__":
    run_tests()
