"""Operational risk (OPE25), leverage, liquidity (LEV, LCR, NSF, LEX) and IRRBB (SRP31) reference implementation.

Backs notes 14 (operational risk standardised approach), 15 (leverage ratio, LCR and NSFR) and
16 (interest rate risk in the banking book).
Every parameter is quoted from the consolidated Basel Framework (bis.org/basel_framework, versions in
force on 2026-10-16; SRP31 is the version in force from 1 January 2026 with the shocks recalibrated on
16 July 2024) and cited by chapter and paragraph next to the constant that holds it.

`run_tests()` reproduces the Committee's own worked numbers (OPE25.7 footnote 363, the OPE25.18 FAQ3
loss-threshold examples, the SRP31.92 shock examples) and computes, prints and asserts every number
quoted in notes 14, 15 and 16 to within half a unit of its last quoted decimal.
Run it with `python 17-Regulatory-Capital-Basel-and-FRTB/code/basel_liquidity_irrbb.py`.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

QUOTED_LOG: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number a note quotes and assert it rounds to the quoted figure (half a unit in the last decimal)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED_LOG.append(label)
    print(f"    {label}: {value:,.{decimals}f}")
    return value


# ============================================================================
# 1. Operational risk: the standardised approach (OPE10, OPE25)
# ============================================================================

ILDC_ASSET_CAP = 0.0225  # OPE25.5: min(|II - IE|, 2.25% x IEA), each averaged over three years
BIC_BUCKETS = ((1_000.0, 0.12), (30_000.0, 0.15), (math.inf, 0.18))  # OPE25.7 Table 1, EUR millions
LC_MULTIPLE = 15.0  # OPE25.8: LC = 15 x average annual losses over 10 years
LOSS_THRESHOLD = 0.020  # OPE25.18: EUR 20,000 (in EUR millions); national discretion EUR 100,000 for buckets 2 and 3
LOSS_THRESHOLD_HIGH = 0.100
RWA_SCALAR = 12.5  # OPE25.2: RWA = 12.5 x ORC


@dataclass(frozen=True)
class BIYear:
    """One financial year of Business Indicator items (OPE10.2 Table 1), EUR millions."""

    interest_income: float
    interest_expense: float
    interest_earning_assets: float
    dividend_income: float
    fee_income: float
    fee_expense: float
    other_operating_income: float
    other_operating_expense: float
    net_pl_trading_book: float
    net_pl_banking_book: float


@dataclass(frozen=True)
class BIResult:
    ildc: float
    sc: float
    fc: float
    bi: float
    ildc_cap_binds: bool


def _avg(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs)


def business_indicator(years: Sequence[BIYear]) -> BIResult:
    """OPE25.4 to OPE25.5 with footnote 362: absolute values of net items year by year, then the three-year average."""
    if len(years) != 3:
        raise ValueError("OPE25.5 averages over t, t-1 and t-2")
    net_interest = _avg([abs(y.interest_income - y.interest_expense) for y in years])
    cap = ILDC_ASSET_CAP * _avg([y.interest_earning_assets for y in years])
    ildc = min(net_interest, cap) + _avg([y.dividend_income for y in years])
    sc = max(_avg([y.other_operating_income for y in years]), _avg([y.other_operating_expense for y in years])) + max(
        _avg([y.fee_income for y in years]), _avg([y.fee_expense for y in years])
    )
    fc = _avg([abs(y.net_pl_trading_book) for y in years]) + _avg([abs(y.net_pl_banking_book) for y in years])
    return BIResult(ildc, sc, fc, ildc + sc + fc, cap < net_interest)


def bic(bi: float) -> float:
    """OPE25.7: marginal coefficients 12% up to EUR 1bn, 15% from 1bn to 30bn, 18% above (EUR millions)."""
    total, lower = 0.0, 0.0
    for upper, alpha in BIC_BUCKETS:
        total += alpha * max(0.0, min(bi, upper) - lower)
        lower = upper
    return total


def ilm(lc: float, bic_value: float) -> float:
    """OPE25.8: ILM = ln(exp(1) - 1 + (LC / BIC)^0.8)."""
    return math.log(math.e - 1.0 + (lc / bic_value) ** 0.8)


def dilm_dratio(ratio: float) -> float:
    """Derivative of the ILM with respect to LC / BIC."""
    return 0.8 * ratio**-0.2 / (math.e - 1.0 + ratio**0.8)


def orc(bi: float, avg_annual_loss: float | None, ilm_one: bool = False) -> tuple[float, float]:
    """OPE25.2, OPE25.9 to OPE25.11: ORC = BIC x ILM; ILM = 1 in bucket 1, without loss data, or under the national discretion."""
    b = bic(bi)
    if ilm_one or bi <= BIC_BUCKETS[0][0] or avg_annual_loss is None:
        return b, 1.0
    m = ilm(LC_MULTIPLE * avg_annual_loss, b)
    return b * m, m


def event_in_dataset(impacts: Sequence[tuple[int, float]], window: tuple[int, int], threshold: float = LOSS_THRESHOLD) -> bool:
    """OPE25.18 FAQ3: sum the event's loss impacts minus recoveries dated inside the window and compare with the threshold."""
    lo, hi = window
    return sum(a for year, a in impacts if lo <= year <= hi) >= threshold


# ============================================================================
# 2. Leverage ratio (LEV20, LEV30, LEV40) and large exposures (LEX20)
# ============================================================================

LEVERAGE_MIN = 0.03  # LEV20.7
LEVERAGE_GSIB_SHARE = 0.50  # LEV40.2
LEV_ALPHA = 1.4  # LEV30.16(1)
OBS_CCF = {  # LEV30.49 to LEV30.54
    "direct credit substitutes": 1.00,
    "note issuance and revolving underwriting facilities": 0.50,
    "transaction-related contingent items": 0.50,
    "commitments": 0.40,
    "short-term self-liquidating trade letters of credit": 0.20,
    "unconditionally cancellable commitments": 0.10,
}
LARGE_EXPOSURE_LIMIT = 0.25  # LEX20.1
LARGE_EXPOSURE_GSIB_LIMIT = 0.15  # LEX20.1, LEX40


def leverage_derivative_exposure(v: float, cvm_received: float, cvm_provided: float, addon: float) -> float:
    """LEV30.15 to LEV30.16: 1.4 x (RC + PFE), RC = max(V - CVMr + CVMp, 0), PFE = add-on with the multiplier fixed at one."""
    return LEV_ALPHA * (max(v - cvm_received + cvm_provided, 0.0) + addon)


# ============================================================================
# 3. Liquidity Coverage Ratio (LCR20, LCR30, LCR40)
# ============================================================================

L2A_HAIRCUT = 0.15  # LCR30.43
L2B_RMBS_HAIRCUT = 0.25  # LCR30.45(1)
L2B_OTHER_HAIRCUT = 0.50  # LCR30.45(2) corporate debt, LCR30.45(3) equities
INFLOW_CAP = 0.75  # LCR40.1, LCR40.77
RUN_OFF = {  # minimum outflow rates, LCR40
    "stable retail deposits": 0.05,  # LCR40.7 (3% under LCR40.11)
    "less stable retail deposits": 0.10,  # LCR40.13 minimum
    "operational deposits": 0.25,  # LCR40.26
    "non-financial corporate non-operational, uninsured": 0.40,  # LCR40.40
    "non-financial corporate non-operational, fully insured": 0.20,  # LCR40.41
    "financial institution unsecured": 1.00,  # LCR40.42
    "committed facilities to retail and small business": 0.05,  # LCR40.64(1)
    "committed credit facilities to non-financial corporates": 0.10,  # LCR40.64(2)
    "committed liquidity facilities to non-financial corporates": 0.30,  # LCR40.64(3)
    "committed facilities to banks": 0.40,  # LCR40.64(4)
    "committed credit facilities to other financial institutions": 0.40,  # LCR40.64(5)
    "committed liquidity facilities to other financial institutions": 1.00,  # LCR40.64(6)
    "committed facilities to SPEs and conduits": 1.00,  # LCR40.64(7)
}
INFLOW_RATE = {  # LCR40.86 to LCR40.88
    "retail and small business loan payments": 0.50,  # LCR40.86
    "non-financial wholesale loan payments": 0.50,  # LCR40.87(2)
    "financial institution and central bank inflows": 1.00,  # LCR40.87(1)
}


@dataclass(frozen=True)
class HQLAResult:
    level1: float
    level2a: float
    level2b: float
    adj15: float
    adj40: float
    stock: float


def hqla_stock(
    level1: float,
    level2a_mv: float,
    l2b_rmbs_mv: float = 0.0,
    l2b_other_mv: float = 0.0,
    adjusted: tuple[float, float, float] | None = None,
) -> HQLAResult:
    """LCR30.38 to LCR30.39 with the haircuts of LCR30.43 and LCR30.45.

    `adjusted` gives the post-haircut adjusted Level 1, 2A and 2B amounts after unwinding short-term secured
    funding, secured lending and collateral swaps (LCR30.37); by default no such transactions exist.
    """
    l2a = (1 - L2A_HAIRCUT) * level2a_mv
    l2b = (1 - L2B_RMBS_HAIRCUT) * l2b_rmbs_mv + (1 - L2B_OTHER_HAIRCUT) * l2b_other_mv
    a1, a2a, a2b = adjusted if adjusted is not None else (level1, l2a, l2b)
    adj15 = max(a2b - 15 / 85 * (a1 + a2a), a2b - 15 / 60 * a1, 0.0)
    adj40 = max(a2a + a2b - adj15 - 2 / 3 * a1, 0.0)
    return HQLAResult(level1, l2a, l2b, adj15, adj40, a1 + a2a + a2b - adj15 - adj40)


def net_cash_outflows(outflows: dict[str, float], inflows: dict[str, float]) -> tuple[float, float, float]:
    """LCR40.1 and LCR40.77: outflows minus inflows, inflows capped at 75% of outflows."""
    out = sum(RUN_OFF[k] * v for k, v in outflows.items())
    inn = sum(INFLOW_RATE[k] * v for k, v in inflows.items())
    return out, inn, out - min(inn, INFLOW_CAP * out)


# ============================================================================
# 4. Net Stable Funding Ratio (NSF20, NSF30)
# ============================================================================

ASF_FACTOR = {  # NSF30.10 to NSF30.14
    "regulatory capital": 1.00,
    "funding with residual maturity of one year or more": 1.00,
    "stable retail deposits": 0.95,
    "less stable retail deposits": 0.90,
    "non-financial corporate funding under one year": 0.50,
    "operational deposits": 0.50,
    "financial institution funding under six months": 0.0,
}
RSF_FACTOR = {  # NSF30.25 to NSF30.32, NSF30.34 Table 1
    "central bank reserves": 0.0,
    "unencumbered Level 1": 0.05,
    "loans to financial institutions under six months secured by Level 1": 0.10,
    "unencumbered Level 2A": 0.15,
    "other loans to financial institutions under six months": 0.15,
    "unencumbered Level 2B": 0.50,
    "loans to non-financials under one year": 0.50,
    "residential mortgages one year or more at RW 35% or lower": 0.65,
    "other performing loans one year or more": 0.85,
    "non-performing loans": 1.00,
    "undrawn committed facilities": 0.05,
}


def nsfr(liabilities: dict[str, float], assets: dict[str, float]) -> tuple[float, float, float]:
    asf = sum(ASF_FACTOR[k] * v for k, v in liabilities.items())
    rsf = sum(RSF_FACTOR[k] * v for k, v in assets.items())
    return asf, rsf, asf / rsf


# ============================================================================
# 5. IRRBB: standardised shocks and the standardised EVE framework (SRP31.90 to SRP31.129)
# ============================================================================

# SRP31.96 Table 3: 19 time bucket midpoints in years.
MIDPOINTS = (0.0028, 0.0417, 0.1667, 0.375, 0.625, 0.875, 1.25, 1.75, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 12.5, 17.5, 25.0)
_UPPER = (1 / 365, 1 / 12, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 15.0, 20.0, math.inf)
SHOCK_DECAY_X = 4.0  # SRP31.91 footnote 525
# SRP31.90 Table 2 (in force from 1 January 2026): currency -> (parallel, short, long) in basis points.
SHOCKS_BP = {
    "ARS": (400, 500, 300), "AUD": (350, 425, 300), "BRL": (400, 500, 300), "CAD": (200, 275, 175), "CHF": (175, 250, 200),
    "CNY": (225, 300, 150), "EUR": (225, 350, 200), "GBP": (275, 425, 250), "HKD": (225, 375, 200), "IDR": (400, 500, 300),
    "INR": (325, 475, 225), "JPY": (100, 100, 100), "KRW": (225, 350, 225), "MXN": (400, 500, 200), "RUB": (400, 500, 300),
    "SAR": (275, 375, 250), "SEK": (275, 425, 200), "SGD": (175, 250, 225), "TRY": (400, 500, 300), "USD": (200, 300, 225),
    "ZAR": (325, 500, 300),
}  # fmt: skip
SCENARIOS = ("parallel up", "parallel down", "steepener", "flattener", "short up", "short down")
NMD_CAPS = {"retail transactional": (0.90, 5.0), "retail non-transactional": (0.70, 4.5), "wholesale": (0.50, 4.0)}  # SRP31.112 Table 4
CPR_MULTIPLIER = dict(zip(SCENARIOS, (0.8, 1.2, 0.8, 1.2, 0.8, 1.2), strict=True))  # SRP31.119 Table 5
TDRR_MULTIPLIER = dict(zip(SCENARIOS, (1.2, 0.8, 0.8, 1.2, 1.2, 0.8), strict=True))  # SRP31.125 Table 6
OUTLIER_THRESHOLD = 0.15  # SRP31.82: max delta EVE over the six scenarios against 15% of Tier 1
MATERIAL_CURRENCY = 0.05  # SRP31.129: currencies above 5% of banking book assets or liabilities


def bucket_midpoint(t: float) -> float:
    """SRP31.96(1): a repricing cash flow is slotted to the midpoint of the bucket that contains its date."""
    for upper, mid in zip(_UPPER, MIDPOINTS, strict=True):
        if t <= upper + 1e-12:
            return mid
    raise ValueError(t)


def alpha_short(t: float) -> float:
    return math.exp(-t / SHOCK_DECAY_X)  # SRP31.91(2)


def shock(currency: str, scenario: str, t: float) -> float:
    """SRP31.91: shift in decimal at tenor t for one of the six prescribed scenarios."""
    par, sh, lo = (x / 10_000 for x in SHOCKS_BP[currency])
    s_short = sh * alpha_short(t)
    s_long = lo * (1.0 - alpha_short(t))
    return {
        "parallel up": par,
        "parallel down": -par,
        "steepener": -0.65 * s_short + 0.9 * s_long,  # SRP31.91(4)
        "flattener": 0.8 * s_short - 0.6 * s_long,
        "short up": s_short,
        "short down": -s_short,
    }[scenario]


def eve(
    cash_flows: dict[float, float], curve: Callable[[float], float], shift: Callable[[float], float], floor: float | None = None
) -> float:
    """SRP31.129(2) to (3): sum of CF(t_k) exp(-R(t_k) t_k); the optional post-shock floor is the SRP31.93 discretion."""
    total = 0.0
    for t, cf in cash_flows.items():
        r = curve(t) + shift(t)
        if floor is not None:
            r = max(r, min(floor, curve(t)))
        total += cf * math.exp(-r * t)
    return total


def delta_eve(
    cash_flows: dict[float, float], curve: Callable[[float], float], currency: str, floor: float | None = None
) -> dict[str, float]:
    """SRP31.129(4): EVE under the current curve minus EVE under scenario i (positive = loss); option add-on KAO = 0 here."""
    base = eve(cash_flows, curve, lambda t: 0.0)
    return {s: base - eve(cash_flows, curve, lambda t, s=s: shock(currency, s, t), floor) for s in SCENARIOS}


def standardised_eve_measure(by_currency: dict[str, dict[str, float]]) -> tuple[str, float]:
    """SRP31.129(5): max over scenarios of max(0, sum of the currency losses that are positive)."""
    best = ("", -math.inf)
    for s in SCENARIOS:
        v = max(0.0, sum(d[s] for d in by_currency.values() if d[s] > 0))
        if v > best[1]:
            best = (s, v)
    return best


def slot(flows: Sequence[tuple[float, float]]) -> dict[float, float]:
    out: dict[float, float] = {}
    for t, cf in flows:
        k = bucket_midpoint(t)
        out[k] = out.get(k, 0.0) + cf
    return out


def net(*parts: dict[float, float]) -> dict[float, float]:
    out: dict[float, float] = {}
    for p in parts:
        for k, v in p.items():
            out[k] = out.get(k, 0.0) + v
    return out


def duration_of(cash_flows: dict[float, float], r: float) -> float:
    pv = sum(cf * math.exp(-r * t) for t, cf in cash_flows.items())
    return sum(t * cf * math.exp(-r * t) for t, cf in cash_flows.items()) / pv


def repricing_gap_dnii(gaps: dict[float, float], shift: float, horizon: float = 1.0) -> float:
    """Constant balance sheet NII change over the horizon: each repricing gap earns the shift from its repricing time."""
    return sum(g * shift * (horizon - t) for t, g in gaps.items() if t < horizon)


# ============================================================================
# 6. Self-checks and every number quoted in notes 14, 15 and 16
# ============================================================================


def _check_note_14() -> None:
    q = quoted
    print("  Note 14: operational risk standardised approach")
    q("OPE25.7 fn 363 BIC at BI = EUR 35bn (EUR bn)", bic(35_000) / 1_000, 5.37, 2)
    q("BIC at the bucket 1 boundary (EUR m)", bic(1_000), 120, 0)
    q("BIC at the bucket 2 boundary (EUR m)", bic(30_000), 4_470, 0)
    q("average BIC rate at BI = EUR 35bn (%)", bic(35_000) / 35_000 * 100, 15.34, 2)
    q("ILM at LC = BIC", ilm(1.0, 1.0), 1.0, 4)
    for ratio, want in ((0.5, 0.8297), (2.0, 1.2411), (5.0, 1.6756), (10.0, 2.0829)):
        q(f"ILM at LC / BIC = {ratio}", ilm(ratio, 1.0), want, 4)
    q("ILM as LC -> 0", math.log(math.e - 1), 0.5413, 4)
    q("dILM/d(LC/BIC) at 1 = 0.8 / e", dilm_dratio(1.0), 0.2943, 4)
    q("first-order capital change for +10% LC/BIC at 1 (%)", dilm_dratio(1.0) * 0.10 * 100, 2.94, 2)
    q("ILM floor as share of BIC (%)", math.log(math.e - 1) * 100, 54.13, 2)

    years = [
        BIYear(3_900, 1_700, 95_000, 90, 1_450, 480, 180, 110, 320, 90),
        BIYear(4_000, 2_000, 100_000, 100, 1_500, 500, 200, 100, -150, 110),
        BIYear(4_600, 2_300, 105_000, 110, 1_550, 520, 220, 260, 430, 100),
    ]
    r = business_indicator(years)
    q("average |net interest| (EUR m)", _avg([abs(y.interest_income - y.interest_expense) for y in years]), 2_166.67, 2)
    q("2.25% of average interest earning assets (EUR m)", ILDC_ASSET_CAP * _avg([y.interest_earning_assets for y in years]), 2_250, 0)
    assert not r.ildc_cap_binds
    q("ILDC (EUR m)", r.ildc, 2_266.67, 2)
    q("average dividend income (EUR m)", _avg([y.dividend_income for y in years]), 100, 0)
    q("average other operating income (EUR m)", _avg([y.other_operating_income for y in years]), 200, 0)
    q("average other operating expense (EUR m)", _avg([y.other_operating_expense for y in years]), 156.67, 2)
    q("average fee income (EUR m)", _avg([y.fee_income for y in years]), 1_500, 0)
    q("average fee expense (EUR m)", _avg([y.fee_expense for y in years]), 500, 0)
    q("average |trading book P&L| (EUR m)", _avg([abs(y.net_pl_trading_book) for y in years]), 300, 0)
    q("average |banking book P&L| (EUR m)", _avg([abs(y.net_pl_banking_book) for y in years]), 100, 0)
    q("SC (EUR m)", r.sc, 1_700, 0)
    q("FC (EUR m)", r.fc, 400, 0)
    q("BI (EUR m)", r.bi, 4_366.67, 2)
    q("BI above the EUR 1bn breakpoint (EUR m)", r.bi - 1_000, 3_366.67, 2)
    q("BIC (EUR m)", bic(r.bi), 625, 0)
    netted_fc = abs(_avg([y.net_pl_trading_book for y in years])) + abs(_avg([y.net_pl_banking_book for y in years]))
    q("FC if averaged before the absolute value (wrong) (EUR m)", netted_fc, 300, 0)
    losses = [35, 42, 28, 160, 55, 38, 47, 30, 61, 44]
    avg_loss = _avg(losses)
    q("average annual loss (EUR m)", avg_loss, 54, 0)
    q("LC (EUR m)", LC_MULTIPLE * avg_loss, 810, 0)
    q("LC / BIC", LC_MULTIPLE * avg_loss / bic(r.bi), 1.296, 3)
    cap, m = orc(r.bi, avg_loss)
    q("ILM", m, 1.0814, 4)
    q("ORC (EUR m)", cap, 675.87, 2)
    q("operational RWA (EUR m)", RWA_SCALAR * cap, 8_448.39, 2)
    cap1, _ = orc(r.bi, avg_loss, ilm_one=True)
    q("ORC with ILM = 1 (EUR m)", cap1, 625, 0)
    q("RWA with ILM = 1 (EUR m)", RWA_SCALAR * cap1, 7_812.5, 1)
    # Marginal capital per EUR of average annual loss at the bank's point.
    ratio = LC_MULTIPLE * avg_loss / bic(r.bi)
    q("dORC / d(average annual loss)", LC_MULTIPLE * dilm_dratio(ratio), 3.86, 2)
    q("extra ORC from a one-off EUR 1m loss (EUR m per year, first order)", LC_MULTIPLE * dilm_dratio(ratio) / 10, 0.386, 3)
    q("neutral average annual loss BIC / 15 (EUR m)", bic(r.bi) / LC_MULTIPLE, 41.67, 2)
    # A single EUR 1bn fine: average loss +100 for ten years.
    cap_fine, m_fine = orc(r.bi, avg_loss + 100)
    q("ILM after a EUR 1bn fine", m_fine, 1.5182, 4)
    q("ORC after a EUR 1bn fine (EUR m)", cap_fine, 948.87, 2)
    q("extra ORC per year for ten years (EUR m)", cap_fine - cap, 273.00, 2)
    q("LC after the fine (EUR m)", LC_MULTIPLE * (avg_loss + 100), 2_310, 0)
    q("first-order prediction of the extra ORC (EUR m)", LC_MULTIPLE * dilm_dratio(ratio) * 100, 386, 0)
    # Cap binding: a consumer lender with high margins.
    hi_margin = [BIYear(9_000, 3_000, 100_000, 0, 200, 50, 10, 5, 0, 20) for _ in range(3)]
    rh = business_indicator(hi_margin)
    assert rh.ildc_cap_binds
    q("ILDC of a 6% margin lender, capped (EUR m)", rh.ildc, 2_250, 0)
    q("its uncapped net interest (EUR m)", abs(hi_margin[0].interest_income - hi_margin[0].interest_expense), 6_000, 0)
    # Bucket 1 bank: ILM = 1 regardless of losses (OPE25.11).
    q("bucket 1 ORC at BI = EUR 800m (EUR m)", orc(800, 500)[0], 96, 0)
    # OPE25.18 FAQ3 worked examples, amounts in EUR millions, window 2012 to 2021.
    assert event_in_dataset([(2012, 0.016), (2013, 0.007)], (2012, 2021))
    assert not event_in_dataset([(2010, 1.0), (2013, 0.3), (2015, -0.5)], (2012, 2021))
    q("FAQ3 event 1 net impact in window (EUR)", (0.016 + 0.007) * 1e6, 23_000, 0)
    q("FAQ3 event 2 net impact in window (EUR)", (0.3 - 0.5) * 1e6, -200_000, 0)


def _check_note_15() -> None:
    q = quoted
    print("  Note 15: leverage, LCR, NSFR, large exposures")
    # Leverage exposure (USD millions).
    deriv = leverage_derivative_exposure(v=6_000, cvm_received=0, cvm_provided=0, addon=10_000)
    q("derivative exposure 1.4 x (6,000 + 10,000)", deriv, 22_400, 0)
    one_set = leverage_derivative_exposure(v=50, cvm_received=30, cvm_provided=0, addon=100)
    q("one netting set: 1.4 x (max(50 - 30, 0) + 100)", one_set, 168, 0)
    q("same set if the 30 were securities (no reduction)", leverage_derivative_exposure(50, 0, 0, 100), 210, 0)
    obs = {
        "commitments": 50_000,
        "unconditionally cancellable commitments": 30_000,
        "direct credit substitutes": 5_000,
        "short-term self-liquidating trade letters of credit": 4_000,
    }
    obs_exp = sum(OBS_CCF[k] * v for k, v in obs.items())
    for k, want in zip(obs, (20_000, 3_000, 5_000, 800), strict=True):
        q(f"credit equivalent: {k}", OBS_CCF[k] * obs[k], want, 0)
    q("off-balance sheet exposure", obs_exp, 28_800, 0)
    exposure = 380_000 - 1_800 + deriv + 45_000 + obs_exp
    q("on-balance sheet net of the goodwill deduction", 380_000 - 1_800, 378_200, 0)
    q("derivative RC + add-on", 6_000 + 10_000, 16_000, 0)
    q("one set: RC after cash VM", max(50 - 30, 0), 20, 0)
    q("one set: RC + add-on without the cash VM", 50 + 100, 150, 0)
    q("leverage exposure measure", exposure, 474_400, 0)
    tier1 = 16_000.0
    q("leverage ratio (%)", tier1 / exposure * 100, 3.37, 2)
    req = LEVERAGE_MIN + LEVERAGE_GSIB_SHARE * 0.015
    q("bucket 2 G-SIB leverage requirement (%)", req * 100, 3.75, 2)
    q("Tier 1 shortfall to the leverage requirement", req * exposure - tier1, 1_790, 0)
    q("risk-based Tier 1 ratio on RWA 145,000 (%)", tier1 / 145_000 * 100, 11.03, 2)
    q("RWA density (%)", 145_000 / exposure * 100, 30.56, 2)
    q("exposure per unit of Tier 1 at 3%", 1 / LEVERAGE_MIN, 33.33, 2)
    q("US holding company eSLR, bucket with 3% method 1 surcharge (%)", (LEVERAGE_MIN + 0.5 * 0.03) * 100, 4.5, 1)
    q("US depository institution eSLR cap: 3% + min(1.5%, 1%) (%)", (LEVERAGE_MIN + min(0.5 * 0.03, 0.01)) * 100, 4.0, 1)

    # LCR, simple stock and the cap mechanics.
    s = hqla_stock(100, 30, l2b_other_mv=10)
    q("HQLA, uncapped case", s.stock, 130.5, 1)
    adjusted = hqla_stock(100, 30, adjusted=(80, 10, 0))
    q("HQLA after secured transaction adjustments", adjusted.stock, 90, 0)
    out, inn, nco = net_cash_outflows({"financial institution unsecured": 100}, {"financial institution and central bank inflows": 40})
    q("LCR, simple case (%)", s.stock / nco * 100, 217.5, 1)
    c = hqla_stock(50, 60, l2b_other_mv=40)
    q("Level 2A after haircut", c.level2a, 51, 0)
    q("Level 2B after haircut", c.level2b, 20, 0)
    q("adjusted Level 1 + Level 2A", 50 + c.level2a, 101, 0)
    q("15/85 x (L1 + L2A)", 15 / 85 * (50 + c.level2a), 17.82, 2)
    q("15/60 x L1", 15 / 60 * 50, 12.5, 1)
    q("Level 2 after the 15% adjustment", c.level2a + c.level2b - c.adj15, 63.5, 1)
    q("2/3 x L1", 2 / 3 * 50, 33.33, 2)
    q("adjustment for the 15% cap", c.adj15, 7.5, 1)
    q("adjustment for the 40% cap", c.adj40, 30.17, 2)
    q("HQLA stock with both caps binding", c.stock, 83.33, 2)
    q("Level 2 share of the stock (%)", (c.stock - 50) / c.stock * 100, 40.0, 1)
    q("Level 2B share of the stock (%)", (c.level2b - c.adj15) / c.stock * 100, 15.0, 1)
    q("stock = Level 1 / 0.6 when the 40% cap binds", 50 / 0.6, 83.33, 2)

    outflows = {
        "stable retail deposits": 20_000,
        "less stable retail deposits": 8_000,
        "operational deposits": 6_000,
        "non-financial corporate non-operational, uninsured": 5_000,
        "financial institution unsecured": 3_000,
        "committed credit facilities to non-financial corporates": 10_000,
        "committed liquidity facilities to non-financial corporates": 2_000,
        "committed facilities to SPEs and conduits": 500,
    }
    inflows = {
        "retail and small business loan payments": 1_200,
        "non-financial wholesale loan payments": 2_000,
        "financial institution and central bank inflows": 4_000,
    }
    out, inn, nco = net_cash_outflows(outflows, inflows)
    for k, want in zip(outflows, (1_000, 800, 1_500, 2_000, 3_000, 1_000, 600, 500), strict=True):
        q(f"outflow: {k}", RUN_OFF[k] * outflows[k], want, 0)
    for k, want in zip(inflows, (600, 1_000, 4_000), strict=True):
        q(f"inflow: {k}", INFLOW_RATE[k] * inflows[k], want, 0)
    q("total outflows", out, 10_400, 0)
    q("total inflows", inn, 5_600, 0)
    q("inflow cap", INFLOW_CAP * out, 7_800, 0)
    q("net cash outflows", nco, 4_800, 0)
    h = hqla_stock(4_000, 1_000, l2b_other_mv=600)
    q("Level 2A after the 15% haircut", h.level2a, 850, 0)
    q("Level 2B after the 50% haircut", h.level2b, 300, 0)
    assert h.adj15 == 0.0 and h.adj40 == 0.0
    q("HQLA stock", h.stock, 5_150, 0)
    q("LCR (%)", h.stock / nco * 100, 107.29, 2)
    _, inn2, nco2 = net_cash_outflows(outflows, {**inflows, "financial institution and central bank inflows": 9_000})
    q("inflows if FI inflows were 9,000", inn2, 10_600, 0)
    q("net cash outflows with the cap binding", nco2, 2_600, 0)
    q("floor on NCO as a share of outflows (%)", nco2 / out * 100, 25.0, 1)
    q("stable retail run-off at 3% instead of 5% saves", (0.05 - 0.03) * 20_000, 400, 0)

    # NSFR (USD millions).
    liabilities = {
        "regulatory capital": 15_000,
        "stable retail deposits": 50_000,
        "less stable retail deposits": 20_000,
        "non-financial corporate funding under one year": 10_000,
        "financial institution funding under six months": 15_000,
        "funding with residual maturity of one year or more": 8_000,
    }
    assets = {
        "central bank reserves": 5_000,
        "unencumbered Level 1": 10_000,
        "unencumbered Level 2A": 3_000,
        "residential mortgages one year or more at RW 35% or lower": 40_000,
        "other performing loans one year or more": 45_000,
        "loans to non-financials under one year": 8_000,
        "other loans to financial institutions under six months": 6_000,
        "non-performing loans": 1_000,
        "undrawn committed facilities": 20_000,
    }
    asf, rsf, ratio = nsfr(liabilities, assets)
    for k, want in zip(liabilities, (15_000, 47_500, 18_000, 5_000, 0, 8_000), strict=True):
        q(f"ASF: {k}", ASF_FACTOR[k] * liabilities[k], want, 0)
    for k, want in zip(assets, (0, 500, 450, 26_000, 38_250, 4_000, 900, 1_000, 1_000), strict=True):
        q(f"RSF: {k}", RSF_FACTOR[k] * assets[k], want, 0)
    q("ASF", asf, 93_500, 0)
    q("RSF", rsf, 72_100, 0)
    q("NSFR (%)", ratio * 100, 129.68, 2)
    q("stable funding surplus", asf - rsf, 21_400, 0)
    q("stable retail that could become sub-6m wholesale before 100%", (asf - rsf) / 0.95, 22_526.32, 2)
    # Large exposures.
    q("large exposure limit on Tier 1 16,000", LARGE_EXPOSURE_LIMIT * tier1, 4_000, 0)
    q("G-SIB to G-SIB limit", LARGE_EXPOSURE_GSIB_LIMIT * tier1, 2_400, 0)


def _irrbb_bank() -> dict[str, dict[float, float]]:
    """Illustrative USD bank, USD billions, repricing cash flows slotted per SRP31.96(1)."""
    bonds = slot([(float(t), 1.5) for t in range(1, 10)] + [(10.0, 51.5)])
    mortgages = slot([(1.0, 5.0), (2.0, 4.8), (3.0, 4.6), (4.0, 4.4), (5.0, 4.2)])
    floating = slot([(0.25, 30.0)])
    cash = slot([(1 / 365, 5.0)])
    core_retail = {m: -6.0 for m in (0.875, 1.75, 2.5, 3.5, 4.5, 5.5, 6.5)}
    nmd = net(core_retail, {0.0028: -18.0}, {1.75: -2.0, 2.5: -2.0}, {0.0028: -6.0})
    term = slot([(1.0, -15.0)])
    senior = slot([(5.0, -10.0)])
    return {"assets": net(bonds, mortgages, floating, cash), "liabilities": net(nmd, term, senior)}


def _check_note_16() -> None:
    q = quoted
    print("  Note 16: IRRBB")
    # SRP31.92 worked shocks.
    q("SRP31.92 short-shock scalar at 3.5y", alpha_short(3.5), 0.417, 3)
    q("SRP31.92 +100bp short shock at 3.5y (bp)", 100 * alpha_short(3.5), 41.7, 1)
    q("long scalar at 3.5y x 100 (bp)", 100 * (1 - alpha_short(3.5)), 58.3, 1)
    jpy_like = -0.65 * 100 * alpha_short(3.5) + 0.9 * 100 * (1 - alpha_short(3.5))
    q("SRP31.92 steepener at 3.5y, 100/100 (bp)", jpy_like, 25.4, 1)
    q("SRP31.92 flattener at 3.5y, 100/100 (bp)", 0.8 * 100 * alpha_short(3.5) - 0.6 * 100 * (1 - alpha_short(3.5)), -1.6, 1)
    q("JPY steepener engine at 3.5y (bp)", shock("JPY", "steepener", 3.5) * 10_000, 25.4, 1)
    # USD shocks at a few tenors.
    q("USD short-up at 0.25y (bp)", shock("USD", "short up", 0.25) * 10_000, 281.8, 1)
    q("USD steepener at 0.25y (bp)", shock("USD", "steepener", 0.25) * 10_000, -170.9, 1)
    q("USD steepener at 25y (bp)", shock("USD", "steepener", 25.0) * 10_000, 201.7, 1)
    q("USD flattener at 25y (bp)", shock("USD", "flattener", 25.0) * 10_000, -134.3, 1)
    q("USD short-up at 25y (bp)", shock("USD", "short up", 25.0) * 10_000, 0.6, 1)
    q("steepener zero crossing, USD (y)", _zero_crossing("USD", "steepener"), 2.70, 2)
    q("flattener zero crossing, USD (y)", _zero_crossing("USD", "flattener"), 4.09, 2)

    bank = _irrbb_bank()
    cfs = net(bank["assets"], bank["liabilities"])
    curve = lambda t: 0.04  # noqa: E731 - flat 4% continuously compounded risk-free curve
    q("average maturity of core retail NMDs (y)", sum((0.875, 1.75, 2.5, 3.5, 4.5, 5.5, 6.5)) / 7, 3.59, 2)
    q("core share of retail transactional NMDs (%)", 42 / 60 * 100, 70, 0)
    q("core share of wholesale NMDs (%)", 4 / 10 * 100, 40, 0)
    q("average maturity of core wholesale NMDs (y)", (1.75 + 2.5) / 2, 2.125, 3)
    for cat, (share, mat) in {"retail transactional": (0.70, 3.589), "wholesale": (0.40, 2.125)}.items():
        cap_share, cap_mat = NMD_CAPS[cat]
        assert share <= cap_share and mat <= cap_mat, cat
    pv_a = eve(bank["assets"], curve, lambda t: 0.0)
    pv_l = -eve(bank["liabilities"], curve, lambda t: 0.0)
    q("PV of assets (USD bn)", pv_a, 102.12, 2)
    q("PV of liabilities (USD bn)", pv_l, 86.99, 2)
    q("base EVE (USD bn)", pv_a - pv_l, 15.12, 2)
    q("asset duration (y)", duration_of(bank["assets"], 0.04), 4.31, 2)
    q("liability duration (y)", duration_of({k: -v for k, v in bank["liabilities"].items()}, 0.04), 2.11, 2)
    d = delta_eve(cfs, curve, "USD")
    expected = {"parallel up": 4.59, "parallel down": -5.74, "steepener": 4.70, "flattener": -3.54, "short up": 0.07, "short down": -0.06}
    for s, v in expected.items():
        q(f"delta EVE {s} (USD bn)", d[s], v, 2)
    worst, measure = standardised_eve_measure({"USD": d})
    assert worst == "steepener"
    tier1 = 15.0
    q("outlier ratio (%)", measure / tier1 * 100, 31.31, 2)
    # Hedge: 10y payer swap, pay 4% fixed annually, receive floating repricing quarterly (USD bn notional N).
    n = 25.0
    swap = net(slot([(0.25, n)]), slot([(float(t), -0.04 * n) for t in range(1, 11)]), slot([(10.0, -n)]))
    dh = delta_eve(net(cfs, swap), curve, "USD")
    worst_h, measure_h = standardised_eve_measure({"USD": dh})
    q("hedged delta EVE steepener (USD bn)", dh["steepener"], 1.75, 2)
    q("hedged outlier ratio (%)", measure_h / tier1 * 100, 11.68, 2)
    assert worst_h == "steepener"
    q("hedged delta EVE parallel up (USD bn)", dh["parallel up"], 0.98, 2)
    # Post-shock floor discretion (SRP31.93) at 0%: irrelevant with a 4% base and a 200bp parallel-down shock.
    assert delta_eve(cfs, curve, "USD", floor=0.0) == d
    # NII: constant balance sheet repricing gaps within one year (USD bn).
    gaps = {1 / 365: 5.0 - 24.0, 0.25: 30.0, 0.875: -6.0}
    q("12-month delta NII, +200bp, full pass-through (USD bn)", repricing_gap_dnii(gaps, 0.02), 0.06, 2)
    beta_gaps = {**gaps, 1 / 365: 5.0 - 0.4 * 24.0}
    q("12-month delta NII, +200bp, overnight NMD beta 40% (USD bn)", repricing_gap_dnii(beta_gaps, 0.02), 0.34, 2)
    # SVB, Barr report: HTM duration 6.2 years; first-order value change for the USD parallel shock.
    q("first-order loss of a 6.2y-duration portfolio, +200bp (%)", 6.2 * 0.02 * 100, 12.4, 1)


def _zero_crossing(currency: str, scenario: str) -> float:
    lo, hi = 0.01, 25.0
    f = lambda t: shock(currency, scenario, t)  # noqa: E731
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if (f(lo) < 0) == (f(mid) < 0):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def run_tests() -> None:
    print("Operational risk, leverage, liquidity and IRRBB self-checks")
    _check_note_14()
    _check_note_15()
    _check_note_16()
    print(f"  {len(QUOTED_LOG)} numbers quoted in notes 14, 15 and 16 computed, printed and asserted")
    print("All operational risk, leverage, liquidity and IRRBB checks passed.")


if __name__ == "__main__":
    run_tests()
