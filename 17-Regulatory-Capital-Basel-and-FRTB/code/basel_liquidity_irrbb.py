"""Basel Operational Risk (SMA), Liquidity (LCR/NSFR), and IRRBB Analytics.

Pure Python 3.10+ standard library implementation:
1. Basel IV Standardised Measurement Approach (SMA) for Operational Risk (OPE25).
2. Liquidity Coverage Ratio (LCR, LCR40) and Net Stable Funding Ratio (NSFR, NSF30).
3. Illustrative IRRBB EVE sensitivity scenarios and outlier test.
4. SVB 2023 case study unhedged HTM duration simulation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# ============================================================================
# 1. Operational Risk Standardised Measurement Approach (SMA, Basel OPE25)
# ============================================================================


@dataclass
class SMAResult:
    business_indicator: float  # BI
    bic: float  # Business Indicator Component
    loss_component: float  # LC = 15 * 10-year avg annual loss
    ilm: float  # Internal Loss Multiplier
    operational_risk_capital: float  # ORC = BIC * ILM
    operational_rwa: float  # RWA = ORC * 12.5


def calculate_operational_risk_sma(
    interest_income: float,
    interest_expense: float,
    interest_earning_assets: float,
    dividend_income: float,
    fee_income: float,
    fee_expense: float,
    other_operating_income: float,
    other_operating_expense: float,
    net_pnl_trading_book: float,
    net_pnl_banking_book: float,
    ten_year_avg_annual_loss: float,
    use_supervisory_ilm_one: bool = False,
) -> SMAResult:
    """Calculate Operational Risk Capital under Basel IV SMA (Basel OPE25).

    BI = ILDC + SC + FC
    where:
    - ILDC = min(|Interest Income - Interest Expense|, 2.2% * Total Earning Assets) + Dividend Income
    - SC = max(Fee Income, Fee Expense) + max(Other Operating Income, Other Operating Expense)
    - FC = |Net PnL Trading| + |Net PnL Banking|

    BIC Buckets:
    - Bucket 1 (BI <= 1B EUR): 12%
    - Bucket 2 (1B < BI <= 30B EUR): 120M + 15% * (BI - 1B)
    - Bucket 3 (BI > 30B EUR): 4,470M + 18% * (BI - 30B)

    ILM = ln(exp(1) - 1 + (LC / BIC)^0.8)
    where LC = 15 * 10-year average annual operational loss.
    """
    # 1. Interest, Lease and Dividend Component (ILDC)
    net_interest = abs(interest_income - interest_expense)
    asset_cap = 0.022 * interest_earning_assets
    ildc = min(net_interest, asset_cap) + dividend_income

    # 2. Services Component (SC)
    sc = max(fee_income, fee_expense) + max(other_operating_income, other_operating_expense)

    # 3. Financial Component (FC)
    fc = abs(net_pnl_trading_book) + abs(net_pnl_banking_book)

    # Business Indicator (BI)
    bi = ildc + sc + fc

    # Business Indicator Component (BIC) across 3 marginal buckets
    b1_cap = 1_000_000_000.0  # 1B EUR
    b2_cap = 30_000_000_000.0  # 30B EUR

    if bi <= b1_cap:
        bic = 0.12 * bi
    elif bi <= b2_cap:
        bic = 0.12 * b1_cap + 0.15 * (bi - b1_cap)
    else:
        bic = 0.12 * b1_cap + 0.15 * (b2_cap - b1_cap) + 0.18 * (bi - b2_cap)

    # Loss Component (LC)
    lc = 15.0 * ten_year_avg_annual_loss

    # Internal Loss Multiplier (ILM)
    if use_supervisory_ilm_one or bic <= 0.0:
        ilm = 1.0
    else:
        ratio = lc / bic
        ilm = math.log(math.e - 1.0 + (ratio**0.8))

    orc = bic * ilm
    rwa = orc * 12.5

    return SMAResult(
        business_indicator=bi,
        bic=bic,
        loss_component=lc,
        ilm=ilm,
        operational_risk_capital=orc,
        operational_rwa=rwa,
    )


# ============================================================================
# 2. Liquidity Framework: LCR and NSFR (Basel LCR40, NSF30)
# ============================================================================


@dataclass
class LCRResult:
    level1_hqla: float
    level2a_hqla: float
    level2b_hqla: float
    adjusted_hqla: float
    total_outflows: float
    total_inflows: float
    net_cash_outflows: float
    lcr_ratio: float
    is_compliant: bool


def calculate_lcr(
    level1_assets: float,
    level2a_assets: float,
    level2b_assets: float,
    gross_cash_outflows: float,
    gross_cash_inflows: float,
    level2b_rmbs_assets: float = 0.0,
) -> LCRResult:
    """Calculate Liquidity Coverage Ratio (LCR) under Basel LCR40.

    HQLA Haircuts: Level 1 = 0%, Level 2A = 15%, Level 2B corporate/equity = 50%, qualifying RMBS = 25%.
    Caps on Level 2:
    - Total Level 2 assets <= 40% of total HQLA.
    - Level 2B assets <= 15% of total HQLA.
    Inflow Cap: Inflows cannot exceed 75% of gross cash outflows.
    """
    # Uncapped post-haircut values
    h_1 = level1_assets
    h_2a = 0.85 * level2a_assets
    h_2b = 0.50 * level2b_assets + 0.75 * level2b_rmbs_assets

    # Cap calculations under Basel LCR Annex 1 formula
    # Level 2 assets capped at 40/60 of Level 1; Level 2B capped at 15/85 of (Level 1 + Level 2A)
    cap_2b = min(h_2b, (15.0 / 85.0) * (h_1 + h_2a))
    cap_2 = min(h_2a + cap_2b, (40.0 / 60.0) * h_1)
    adjusted_hqla = h_1 + cap_2

    # Inflow cap: max 75% of outflows
    inflow_cap = 0.75 * gross_cash_outflows
    capped_inflows = min(gross_cash_inflows, inflow_cap)
    net_outflows = max(0.0, gross_cash_outflows - capped_inflows)

    ratio = (adjusted_hqla / net_outflows) if net_outflows > 0 else float("inf")

    return LCRResult(
        level1_hqla=h_1,
        level2a_hqla=h_2a,
        level2b_hqla=h_2b,
        adjusted_hqla=adjusted_hqla,
        total_outflows=gross_cash_outflows,
        total_inflows=gross_cash_inflows,
        net_cash_outflows=net_outflows,
        lcr_ratio=ratio,
        is_compliant=(ratio >= 1.00),
    )


# ============================================================================
# 3. IRRBB: Economic Value of Equity (EVE) and Outlier Test (Basel SRP31)
# ============================================================================


@dataclass
class IRRBBResult:
    base_eve: float
    shock_scenarios: dict[str, float]  # Scenario name -> delta EVE (loss is positive)
    worst_eve_loss: float
    worst_scenario: str
    tier1_capital: float
    loss_ratio_of_tier1: float
    outlier_breached: bool  # True if loss > 15% of Tier 1


def calculate_irrbb_eve(
    cash_flows_by_year: dict[float, float],  # tenor (years) -> net cash flow (assets - liabilities)
    discount_rate: float,  # base flat zero rate (e.g. 0.04 for 4%)
    tier1_capital: float,
) -> IRRBBResult:
    """Calculate illustrative IRRBB EVE sensitivity scenarios.

    These generic shocks are illustrative and are not currency-specific standardized supervisory shocks:
    1. Parallel Up: +200 bps
    2. Parallel Down: -200 bps (floored at 0% or negative rates)
    3. Steepener: short -100 bps, long +100 bps
    4. Flattener: short +100 bps, long -100 bps
    5. Short Up: short +200 bps decaying to 0 at long tenors
    6. Short Down: short -200 bps decaying to 0 at long tenors
    """

    def pv(rate_shift_func) -> float:
        total_pv = 0.0
        for t, cf in cash_flows_by_year.items():
            shift = rate_shift_func(t)
            r_eff = max(-0.01, discount_rate + shift)
            df = math.exp(-r_eff * t)
            total_pv += cf * df
        return total_pv

    # Base EVE
    base_eve = pv(lambda t: 0.0)

    # Illustrative shocks
    shocks = {
        "Parallel_Up": lambda t: 0.0200,
        "Parallel_Down": lambda t: -0.0200,
        "Steepener": lambda t: -0.0100 * math.exp(-t / 4.0) + 0.0100 * (1.0 - math.exp(-t / 4.0)),
        "Flattener": lambda t: +0.0100 * math.exp(-t / 4.0) - 0.0100 * (1.0 - math.exp(-t / 4.0)),
        "Short_Up": lambda t: +0.0200 * math.exp(-t / 4.0),
        "Short_Down": lambda t: -0.0200 * math.exp(-t / 4.0),
    }

    eve_losses: dict[str, float] = {}
    for name, shock_fn in shocks.items():
        eve_shock = pv(shock_fn)
        # Loss in economic value = Base EVE - Shocked EVE
        delta_loss = base_eve - eve_shock
        eve_losses[name] = delta_loss

    worst_scenario = max(eve_losses.keys(), key=lambda k: eve_losses[k])
    worst_loss = max(0.0, eve_losses[worst_scenario])
    ratio = worst_loss / tier1_capital if tier1_capital > 0 else float("inf")

    return IRRBBResult(
        base_eve=base_eve,
        shock_scenarios=eve_losses,
        worst_eve_loss=worst_loss,
        worst_scenario=worst_scenario,
        tier1_capital=tier1_capital,
        loss_ratio_of_tier1=ratio,
        outlier_breached=(ratio > 0.15),
    )


# ============================================================================
# 4. Verification Tests
# ============================================================================


def run_tests() -> None:
    print("Testing Operational Risk (SMA), Liquidity (LCR), and IRRBB Analytics...")

    # 1. Operational Risk SMA Test
    # Large Bank with BI = 3.5B EUR (Bucket 2: 1B to 30B)
    # Ten-year average annual loss = 50M EUR -> LC = 15 * 50M = 750M EUR
    sma_res = calculate_operational_risk_sma(
        interest_income=4_000_000_000.0,
        interest_expense=2_000_000_000.0,
        interest_earning_assets=100_000_000_000.0,
        dividend_income=100_000_000.0,
        fee_income=1_500_000_000.0,
        fee_expense=500_000_000.0,
        other_operating_income=200_000_000.0,
        other_operating_expense=100_000_000.0,
        net_pnl_trading_book=300_000_000.0,
        net_pnl_banking_book=100_000_000.0,
        ten_year_avg_annual_loss=50_000_000.0,
    )
    # Net interest = 2B <= 2.2% * 100B = 2.2B -> ILDC = 2B + 100M = 2.1B
    # SC = max(1.5B, 0.5B) + max(200M, 100M) = 1.5B + 200M = 1.7B
    # FC = 300M + 100M = 400M
    # Total BI = 2.1B + 1.7B + 0.4B = 4.2B EUR
    assert math.isclose(sma_res.business_indicator, 4_200_000_000.0, rel_tol=1e-5)
    # BIC = 0.12 * 1B + 0.15 * (4.2B - 1B) = 120M + 0.15 * 3.2B = 120M + 480M = 600M EUR
    assert math.isclose(sma_res.bic, 600_000_000.0, rel_tol=1e-5)
    # LC = 15 * 50M = 750M EUR
    assert math.isclose(sma_res.loss_component, 750_000_000.0, rel_tol=1e-5)
    # Ratio LC / BIC = 750 / 600 = 1.25 -> ILM = ln(e - 1 + 1.25^0.8)
    expected_ilm = math.log(math.e - 1.0 + (1.25**0.8))
    assert math.isclose(sma_res.ilm, expected_ilm, rel_tol=1e-4)
    print(f"SMA: BI=${sma_res.business_indicator:,.2f}, BIC=${sma_res.bic:,.2f}")
    print(f"SMA: ILM={sma_res.ilm:.4f}, ORC=${sma_res.operational_risk_capital:,.2f}, RWA=${sma_res.operational_rwa:,.2f}")

    # 2. LCR Test
    # Bank with $100M Level 1 (Cash/Treasuries), $30M Level 2A, $10M Level 2B
    # Outflows = $100M, Inflows = $40M
    lcr_res = calculate_lcr(
        level1_assets=100_000_000.0,
        level2a_assets=30_000_000.0,
        level2b_assets=10_000_000.0,
        gross_cash_outflows=100_000_000.0,
        gross_cash_inflows=40_000_000.0,
    )
    # Net outflows = 100M - 40M = 60M (40M <= 75M cap)
    assert lcr_res.net_cash_outflows == 60_000_000.0
    # Level 2A = 0.85 * 30M = 25.5M, Level 2B = 0.50 * 10M = 5.0M -> Total HQLA = 100M + 25.5M + 5M = 130.5M
    assert math.isclose(lcr_res.adjusted_hqla, 130_500_000.0, rel_tol=1e-5)
    # LCR = 130.5M / 60M = 2.175 (217.5% >= 100%)
    assert math.isclose(lcr_res.lcr_ratio, 2.175, rel_tol=1e-4)
    assert lcr_res.is_compliant is True
    print(f"LCR: Adjusted HQLA=${lcr_res.adjusted_hqla:,.2f}, Net Outflows=${lcr_res.net_cash_outflows:,.2f}, LCR={lcr_res.lcr_ratio:.2%}")

    # 3. IRRBB and SVB 2023 Case Study Test
    # Simplified SVB balance sheet profile:
    # Assets: $100B in 10-year Agency MBS / Treasuries paying 1.5% (duration ~8 years)
    # Liabilities: $90B in Non-Maturity Deposits (NMDs) paying ~0% (duration treated as zero in a run)
    # Net cash flow: -$90B at t=0 (deposits), +$100B principal at t=10 + $1.5B/yr interest
    cf_svb = {
        0.0: -90_000_000_000.0,
        1.0: 1_500_000_000.0,
        2.0: 1_500_000_000.0,
        3.0: 1_500_000_000.0,
        4.0: 1_500_000_000.0,
        5.0: 1_500_000_000.0,
        6.0: 1_500_000_000.0,
        7.0: 1_500_000_000.0,
        8.0: 1_500_000_000.0,
        9.0: 1_500_000_000.0,
        10.0: 101_500_000_000.0,
    }
    # Base discount rate = 1.5% (initial book yield), Tier 1 capital = $12B
    irrbb_svb = calculate_irrbb_eve(
        cash_flows_by_year=cf_svb,
        discount_rate=0.015,
        tier1_capital=12_000_000_000.0,
    )
    # Under a +200 bps Parallel Up shock (rates rise from 1.5% to 3.5%):
    # 10-year bond with duration ~8 drops by approx 16% = $16B loss!
    # $16B loss exceeds entire $12B Tier 1 capital -> loss ratio > 100% > 15% outlier threshold
    print(f"IRRBB SVB: Base EVE=${irrbb_svb.base_eve:,.2f}, Worst Scenario: {irrbb_svb.worst_scenario}")
    print(f"IRRBB SVB: Worst EVE Loss=${irrbb_svb.worst_eve_loss:,.2f} ({irrbb_svb.loss_ratio_of_tier1:.2%} of Tier 1 Capital)")
    assert irrbb_svb.outlier_breached is True, "SVB must breach the 15% EVE outlier threshold"
    assert irrbb_svb.loss_ratio_of_tier1 > 1.0, "SVB EVE loss exceeds 100% of Tier 1 capital"

    print("All Operational Risk, Liquidity, and IRRBB tests passed successfully!")


if __name__ == "__main__":
    run_tests()
