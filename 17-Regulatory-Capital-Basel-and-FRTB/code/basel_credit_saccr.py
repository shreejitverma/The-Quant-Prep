"""Basel credit risk capital and SA-CCR reference implementation.

Every parameter is quoted from the consolidated Basel Framework (bis.org/basel_framework,
version in force from 1 January 2023) and cited by chapter and paragraph:

1. Standardised approach (SA) risk weights and credit conversion factors (CRE20).
2. IRB risk-weight functions (CRE31) with the PD, LGD and maturity rules of CRE32.
3. The output floor and its phase-in (RBC20.4, RBC20.11 to RBC20.13, RBC90).
4. The standardised approach for counterparty credit risk, SA-CCR (CRE52).

`run_tests()` reproduces the Basel Committee's own published numbers:
all 144 illustrative IRB risk weights in CRE99.2 Table 1, the output floor example in RBC20.13,
the five SA-CCR sample portfolios in CRE99.20 to CRE99.97 and the margin examples in CRE99.98 to CRE99.115.
Run it with `python 17-Regulatory-Capital-Basel-and-FRTB/code/basel_credit_saccr.py`.
"""

from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from statistics import NormalDist

_STD_NORMAL = NormalDist()


def norm_cdf(x: float) -> float:
    """N(x), the standard normal distribution function (CRE31.2(4))."""
    return _STD_NORMAL.cdf(x)


def norm_ppf(p: float) -> float:
    """G(p), the inverse standard normal distribution function (CRE31.2(5))."""
    return _STD_NORMAL.inv_cdf(p)


# ============================================================================
# 1. Standardised approach for credit risk (CRE20)
# ============================================================================

_NOTCHES = ("AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "BB-", "B+", "B", "B-")


def _notch(rating: str) -> int:
    """Position of an S&P-style rating in the scale; anything below B- maps past the end."""
    if rating in _NOTCHES:
        return _NOTCHES.index(rating)
    if rating.startswith("CCC") or rating in ("CC", "C", "D"):
        return len(_NOTCHES)
    raise ValueError(f"unknown rating {rating!r}")


def sa_sovereign_rw(rating: str | None) -> float:
    """CRE20.7 Table 1: 0% / 20% / 50% / 100% / 150%, unrated 100%."""
    if rating is None:
        return 1.00
    n = _notch(rating)
    for upper, rw in ((3, 0.00), (6, 0.20), (9, 0.50), (15, 1.00)):
        if n <= upper:
            return rw
    return 1.50


def sa_bank_rw_ecra(rating: str, short_term: bool = False) -> float:
    """CRE20.18 Table 6 (ECRA): base 20/30/50/100/150%; short-term (CRE20.19) 20/20/20/50/150%."""
    n = _notch(rating)
    base = (0.20, 0.30, 0.50, 1.00, 1.50)
    short = (0.20, 0.20, 0.20, 0.50, 1.50)
    band = 0 if n <= 3 else 1 if n <= 6 else 2 if n <= 9 else 3 if n <= 15 else 4
    return (short if short_term else base)[band]


def sa_bank_rw_scra(grade: str, short_term: bool = False, cet1_ge_14_and_lev_ge_5: bool = False) -> float:
    """CRE20.21 Table 7 (SCRA): A 40%, B 75%, C 150%; short-term 20/50/150%; footnote 98 allows 30% for strong Grade A banks."""
    if grade == "A" and cet1_ge_14_and_lev_ge_5 and not short_term:
        return 0.30
    table = {"A": (0.40, 0.20), "B": (0.75, 0.50), "C": (1.50, 1.50)}
    base, short = table[grade]
    return short if short_term else base


def sa_corporate_rw(rating: str | None, sme: bool = False) -> float:
    """CRE20.42 to CRE20.43 Table 10: 20/50/75/100/150%, unrated 100%; unrated SME 85% (CRE20.47)."""
    if rating is None:
        return 0.85 if sme else 1.00
    n = _notch(rating)
    for upper, rw in ((3, 0.20), (6, 0.50), (9, 0.75), (12, 1.00)):
        if n <= upper:
            return rw
    return 1.50


def sa_retail_rw(kind: str) -> float:
    """CRE20.68: regulatory retail 75%, transactors 45%, other retail 100%."""
    return {"regulatory": 0.75, "transactor": 0.45, "other": 1.00}[kind]


def sa_residential_re_rw(ltv: float) -> float:
    """CRE20.82 Table 11, whole-loan approach, not materially dependent on property cash flows."""
    for upper, rw in ((0.50, 0.20), (0.60, 0.25), (0.80, 0.30), (0.90, 0.40), (1.00, 0.50)):
        if ltv <= upper:
            return rw
    return 0.70


SA_CCF = {
    "direct_credit_substitute": 1.00,  # CRE20.95
    "nif_ruf": 0.50,  # CRE20.96
    "transaction_contingent": 0.50,  # CRE20.97
    "commitment": 0.40,  # CRE20.98, regardless of maturity
    "trade_letter_of_credit": 0.20,  # CRE20.99
    "unconditionally_cancellable": 0.10,  # CRE20.100
}


# ============================================================================
# 2. IRB risk-weight functions (CRE31) and risk components (CRE32)
# ============================================================================

PD_FLOOR_CORPORATE_BANK = 0.0005  # CRE32.4, not applied to sovereigns
PD_FLOOR_RETAIL = 0.0005  # CRE32.58
PD_FLOOR_QRRE_REVOLVER = 0.0010  # CRE32.58
FIRB_LGD_SENIOR_CORPORATE = 0.40  # CRE32.6
FIRB_LGD_SENIOR_FINANCIAL = 0.45  # CRE32.6, sovereigns, banks, securities firms and other financials
FIRB_LGD_SUBORDINATED = 0.75  # CRE32.7
AIRB_LGD_FLOOR_UNSECURED_CORPORATE = 0.25  # CRE32.16
CONFIDENCE = 0.999  # the G(0.999) term in CRE31.5


def _pd_weight(pd: float, k: float) -> float:
    """(1 - exp(-k PD)) / (1 - exp(-k)): moves from 0 at PD=0 to 1 at PD=1."""
    return (1.0 - math.exp(-k * pd)) / (1.0 - math.exp(-k))


def corporate_correlation(pd: float, sales_eur_m: float | None = None, large_or_unregulated_fi: bool = False) -> float:
    """Asset correlation R for corporate, sovereign and bank exposures (CRE31.5).

    R = 0.12 w + 0.24 (1 - w), w = (1 - e^{-50 PD}) / (1 - e^{-50}).
    SMEs with consolidated sales S < EUR 50m subtract 0.04 (1 - (S - 5) / 45), S floored at 5 (CRE31.8).
    Large regulated (total assets >= USD 100bn) and all unregulated financials multiply R by 1.25 (CRE31.7).
    """
    w = _pd_weight(pd, 50.0)
    r = 0.12 * w + 0.24 * (1.0 - w)
    if large_or_unregulated_fi:
        r *= 1.25
    if sales_eur_m is not None and sales_eur_m < 50.0:
        s = max(5.0, sales_eur_m)
        r -= 0.04 * (1.0 - (s - 5.0) / 45.0)
    return r


def hvcre_correlation(pd: float) -> float:
    """CRE31.11: R = 0.12 w + 0.30 (1 - w) for high-volatility commercial real estate."""
    w = _pd_weight(pd, 50.0)
    return 0.12 * w + 0.30 * (1.0 - w)


def retail_correlation(pd: float, kind: str) -> float:
    """CRE31.14 mortgages 0.15, CRE31.15 QRRE 0.04, CRE31.16 other retail 0.03 w + 0.16 (1 - w) with k = 35."""
    if kind == "mortgage":
        return 0.15
    if kind == "qrre":
        return 0.04
    if kind == "other":
        w = _pd_weight(pd, 35.0)
        return 0.03 * w + 0.16 * (1.0 - w)
    raise ValueError(f"unknown retail kind {kind!r}")


def maturity_b(pd: float) -> float:
    """CRE31.5 maturity adjustment slope b = (0.11852 - 0.05478 ln PD)^2."""
    return (0.11852 - 0.05478 * math.log(pd)) ** 2


def conditional_pd(pd: float, r: float, q: float = CONFIDENCE) -> float:
    """Vasicek conditional PD at the q-quantile of the systematic factor: N((G(PD) + sqrt(R) G(q)) / sqrt(1 - R))."""
    return norm_cdf(norm_ppf(pd) / math.sqrt(1.0 - r) + math.sqrt(r / (1.0 - r)) * norm_ppf(q))


@dataclass(frozen=True)
class IRBResult:
    pd: float
    lgd: float
    ead: float
    maturity: float | None
    correlation: float
    b: float | None
    k: float  # capital per unit EAD
    risk_weight: float  # K * 12.5
    rwa: float
    expected_loss: float  # PD * LGD * EAD (CRE35)


def irb_k(pd: float, lgd: float, r: float, maturity: float | None) -> tuple[float, float | None]:
    """Capital requirement K per unit of EAD (CRE31.5; retail CRE31.14 to CRE31.16 have no maturity term)."""
    if pd >= 1.0:
        raise ValueError("defaulted exposures use CRE31.3: K = max(0, LGD - best estimate of EL)")
    unexpected = lgd * conditional_pd(pd, r) - pd * lgd
    if maturity is None:
        return unexpected, None
    b = maturity_b(pd)
    return unexpected * (1.0 + (maturity - 2.5) * b) / (1.0 - 1.5 * b), b


def irb_corporate(
    pd: float,
    lgd: float,
    ead: float,
    maturity: float = 2.5,
    sales_eur_m: float | None = None,
    large_or_unregulated_fi: bool = False,
    sovereign: bool = False,
    hvcre: bool = False,
    apply_maturity_bounds: bool = True,
) -> IRBResult:
    """Corporate, sovereign and bank IRB capital.

    PD floor 0.05% except sovereigns (CRE32.4); F-IRB M = 2.5 by default (CRE32.44);
    M floored at 1 and capped at 5 (CRE32.46), switchable off for the CRE32.51 to CRE32.53 short-term exceptions.
    """
    if not sovereign:
        pd = max(pd, PD_FLOOR_CORPORATE_BANK)
    if apply_maturity_bounds:
        maturity = min(max(maturity, 1.0), 5.0)
    r = hvcre_correlation(pd) if hvcre else corporate_correlation(pd, sales_eur_m, large_or_unregulated_fi)
    k, b = irb_k(pd, lgd, r, maturity)
    return IRBResult(pd, lgd, ead, maturity, r, b, k, 12.5 * k, 12.5 * k * ead, pd * lgd * ead)


def irb_retail(pd: float, lgd: float, ead: float, kind: str, qrre_revolver: bool = False) -> IRBResult:
    """Retail IRB capital (CRE31.13 to CRE31.16) with the CRE32.58 PD floors."""
    floor = PD_FLOOR_QRRE_REVOLVER if (kind == "qrre" and qrre_revolver) else PD_FLOOR_RETAIL
    pd = max(pd, floor)
    r = retail_correlation(pd, kind)
    k, _ = irb_k(pd, lgd, r, None)
    return IRBResult(pd, lgd, ead, None, r, None, k, 12.5 * k, 12.5 * k * ead, pd * lgd * ead)


def firb_secured_lgd(e: float, he: float, collateral_value: float, hc: float, lgd_s: float, lgd_u: float) -> float:
    """CRE32.10: LGD* = LGD_U (E_U / (E (1 + H_E))) + LGD_S (E_S / (E (1 + H_E))), E_S = C (1 - H_C) capped at E (1 + H_E)."""
    gross = e * (1.0 + he)
    es = min(collateral_value * (1.0 - hc), gross)
    eu = gross - es
    return (lgd_u * eu + lgd_s * es) / gross


# ============================================================================
# 3. Output floor (RBC20.4, RBC20.11 to RBC20.13, RBC90)
# ============================================================================

OUTPUT_FLOOR = 0.725  # RBC20.4(2)
OUTPUT_FLOOR_PHASE_IN = {2023: 0.50, 2024: 0.55, 2025: 0.60, 2026: 0.65, 2027: 0.70, 2028: 0.725}  # RBC90.1 Table 1
TRANSITIONAL_CAP = 0.25  # RBC90.2, national discretion during phase-in


def floored_rwa(pre_floor_rwa: float, standardised_rwa: float, calibration: float = OUTPUT_FLOOR, cap: float | None = None) -> float:
    """max(nominated-approach RWA, calibration x standardised RWA), optionally capped at (1 + cap) x pre-floor RWA."""
    floored = max(pre_floor_rwa, calibration * standardised_rwa)
    if cap is not None:
        floored = min(floored, (1.0 + cap) * pre_floor_rwa)
    return floored


# ============================================================================
# 4. SA-CCR (CRE52)
# ============================================================================

ALPHA = 1.4  # CRE52.1
MULTIPLIER_FLOOR = 0.05  # CRE52.23
BUSINESS_DAYS_PER_YEAR = 250  # CRE52.49 and CRE52.53 market convention
MIN_MATURITY_YEARS = 10 / BUSINESS_DAYS_PER_YEAR  # CRE52.34 and CRE52.48 to CRE52.49

# CRE52.72 Table 2: (supervisory factor, correlation, supervisory option volatility).
SUPERVISORY = {
    ("IR", ""): (0.005, None, 0.50),
    ("FX", ""): (0.04, None, 0.15),
    ("CREDIT", "AAA"): (0.0038, 0.50, 1.00),
    ("CREDIT", "AA"): (0.0038, 0.50, 1.00),
    ("CREDIT", "A"): (0.0042, 0.50, 1.00),
    ("CREDIT", "BBB"): (0.0054, 0.50, 1.00),
    ("CREDIT", "BB"): (0.0106, 0.50, 1.00),
    ("CREDIT", "B"): (0.016, 0.50, 1.00),
    ("CREDIT", "CCC"): (0.06, 0.50, 1.00),
    ("CREDIT", "INDEX_IG"): (0.0038, 0.80, 0.80),
    ("CREDIT", "INDEX_SG"): (0.0106, 0.80, 0.80),
    ("EQUITY", "SINGLE"): (0.32, 0.50, 1.20),
    ("EQUITY", "INDEX"): (0.20, 0.80, 0.75),
    ("COMMODITY", "ELECTRICITY"): (0.40, 0.40, 1.50),
    ("COMMODITY", "OIL_GAS"): (0.18, 0.40, 0.70),
    ("COMMODITY", "METALS"): (0.18, 0.40, 0.70),
    ("COMMODITY", "AGRICULTURAL"): (0.18, 0.40, 0.70),
    ("COMMODITY", "OTHER"): (0.18, 0.40, 0.70),
}


@dataclass(frozen=True)
class OptionTerms:
    """Inputs to the CRE52.40 supervisory delta; `shift` is the CRE52.40 FAQ2 lambda for negative rates."""

    call: bool
    bought: bool
    underlying: float  # P_i, the forward where appropriate (CRE52.40 FAQ1)
    strike: float  # K_i
    expiry: float  # T_i, latest contractual exercise date in years
    shift: float = 0.0


@dataclass(frozen=True)
class Trade:
    """One derivative in a netting set.

    `direction` is +1 when long the primary risk factor and -1 when short (CRE52.39).
    `hedging_set` is the currency (IR), currency pair (FX) or commodity group (energy, metals, agricultural, other);
    `entity` is the reference name (credit, equity) or commodity type (commodity).
    `notional` is in the reporting currency: for equity and commodity it is price times units (CRE52.36).
    """

    trade_id: str
    asset_class: str  # IR, FX, CREDIT, EQUITY, COMMODITY
    subclass: str  # key into SUPERVISORY together with asset_class
    notional: float
    mtm: float
    maturity: float  # M_i
    direction: int = 1
    start: float = 0.0  # S_i (IR and credit)
    end: float | None = None  # E_i (IR and credit)
    hedging_set: str = ""
    entity: str = ""
    option: OptionTerms | None = None
    cdo_attach_detach: tuple[float, float] | None = None
    basis: bool = False  # CRE52.46: separate hedging set and half the supervisory factor
    volatility: bool = False  # CRE52.47: separate hedging set and five times the supervisory factor


def supervisory_duration(start: float, end: float) -> float:
    """CRE52.34: SD = (exp(-0.05 S) - exp(-0.05 E)) / 0.05, floored at ten business days."""
    sd = (math.exp(-0.05 * start) - math.exp(-0.05 * end)) / 0.05
    return max(sd, MIN_MATURITY_YEARS)


def maturity_factor_unmargined(maturity: float) -> float:
    """CRE52.48: MF = sqrt(min(M, 1) / 1) with M floored at ten business days."""
    return math.sqrt(min(max(maturity, MIN_MATURITY_YEARS), 1.0))


def maturity_factor_margined(mpor_days: float) -> float:
    """CRE52.52: MF = 1.5 sqrt(MPOR / 1 year), with MPOR in business days over 250 (CRE52.53)."""
    return 1.5 * math.sqrt(mpor_days / BUSINESS_DAYS_PER_YEAR)


def mpor_floor_days(
    daily_margin: bool = True,
    remargin_period_days: int = 1,
    trades_in_netting_set: int = 1,
    illiquid_collateral_or_hard_to_replace: bool = False,
    disputes_exceeding_mpor_last_two_quarters: int = 0,
) -> int:
    """Supervisory MPOR floor for a non-centrally-cleared netting set (CRE52.50 to CRE52.51)."""
    floor = 10 if daily_margin else 9 + remargin_period_days
    if trades_in_netting_set > 5000 or illiquid_collateral_or_hard_to_replace:
        floor = max(floor, 20)
    if disputes_exceeding_mpor_last_two_quarters > 2:
        floor *= 2
    return floor


def supervisory_delta(trade: Trade) -> float:
    """CRE52.39 to CRE52.41: +1/-1 for linear trades, Black-Scholes style delta for options, tranche formula for CDOs."""
    if trade.option is not None:
        o = trade.option
        vol = SUPERVISORY[(trade.asset_class, trade.subclass)][2]
        d = (math.log((o.underlying + o.shift) / (o.strike + o.shift)) + 0.5 * vol**2 * o.expiry) / (vol * math.sqrt(o.expiry))
        if o.call:
            delta = norm_cdf(d)
        else:
            delta = -norm_cdf(-d)
        return delta if o.bought else -delta
    if trade.cdo_attach_detach is not None:
        a, dd = trade.cdo_attach_detach
        magnitude = 15.0 / ((1.0 + 14.0 * a) * (1.0 + 14.0 * dd))
        return magnitude if trade.direction > 0 else -magnitude  # +: purchased protection, -: sold protection
    return float(trade.direction)


def adjusted_notional(trade: Trade) -> float:
    """CRE52.34 to CRE52.36: notional x SD for IR and credit, notional for FX, equity and commodity."""
    if trade.asset_class in ("IR", "CREDIT"):
        end = trade.end if trade.end is not None else trade.maturity
        return trade.notional * supervisory_duration(trade.start, end)
    return trade.notional


def effective_notional(trade: Trade, margined: bool, mpor_days: float) -> float:
    """D_i = d_i x MF_i x delta_i (CRE52.30(1))."""
    mf = maturity_factor_margined(mpor_days) if margined else maturity_factor_unmargined(trade.maturity)
    return adjusted_notional(trade) * mf * supervisory_delta(trade)


def _sf_scale(trade: Trade) -> float:
    return 0.5 if trade.basis else 5.0 if trade.volatility else 1.0


def _hs_key(trade: Trade) -> tuple[str, bool, bool]:
    return (trade.hedging_set, trade.basis, trade.volatility)


def ir_maturity_bucket(trade: Trade) -> int:
    """CRE52.57(3): bucket 1 if E_i < 1y, 2 if 1y to 5y, 3 if > 5y."""
    end = trade.end if trade.end is not None else trade.maturity
    return 1 if end < 1.0 else 2 if end <= 5.0 else 3


def addon_ir(trades: Sequence[Trade], margined: bool, mpor_days: float, offset: bool = True) -> tuple[float, dict]:
    """CRE52.57 steps 1 to 7."""
    buckets: dict[tuple, list[float]] = defaultdict(lambda: [0.0, 0.0, 0.0])
    scale: dict[tuple, float] = {}
    for t in trades:
        key = _hs_key(t)
        buckets[key][ir_maturity_bucket(t) - 1] += effective_notional(t, margined, mpor_days)
        scale[key] = _sf_scale(t)
    detail = {}
    total = 0.0
    for key, (d1, d2, d3) in buckets.items():
        if offset:
            en = math.sqrt(max(0.0, d1 * d1 + d2 * d2 + d3 * d3 + 1.4 * d1 * d2 + 1.4 * d2 * d3 + 0.6 * d1 * d3))
        else:
            en = abs(d1) + abs(d2) + abs(d3)
        addon = en * SUPERVISORY[("IR", "")][0] * scale[key]
        detail[key] = {"DB": (d1, d2, d3), "EN": en, "AddOn": addon}
        total += addon
    return total, detail


def addon_fx(trades: Sequence[Trade], margined: bool, mpor_days: float) -> tuple[float, dict]:
    """CRE52.59: full offset within a currency pair, AddOn_HS = |EN_HS| x 4%."""
    en: dict[tuple, float] = defaultdict(float)
    scale: dict[tuple, float] = {}
    for t in trades:
        en[_hs_key(t)] += effective_notional(t, margined, mpor_days)
        scale[_hs_key(t)] = _sf_scale(t)
    detail = {k: {"EN": v, "AddOn": abs(v) * SUPERVISORY[("FX", "")][0] * scale[k]} for k, v in en.items()}
    return sum(d["AddOn"] for d in detail.values()), detail


def _single_factor(addons: Iterable[tuple[float, float]]) -> tuple[float, float, float]:
    """sqrt((sum rho a)^2 + sum (1 - rho^2) a^2) used by CRE52.61(4), CRE52.66(4) and CRE52.70(5)."""
    systematic = 0.0
    idiosyncratic = 0.0
    for rho, a in addons:
        systematic += rho * a
        idiosyncratic += (1.0 - rho * rho) * a * a
    return math.sqrt(systematic * systematic + idiosyncratic), systematic, idiosyncratic


def addon_credit_or_equity(trades: Sequence[Trade], margined: bool, mpor_days: float) -> tuple[float, dict]:
    """CRE52.61 (credit) and CRE52.66 (equity): entity add-ons combined with the single-factor formula.

    Basis and volatility trades form their own hedging sets (CRE52.46 to CRE52.47) whose add-ons are summed.
    """
    by_hs: dict[tuple, dict[str, list]] = defaultdict(dict)
    for t in trades:
        sf, rho, _ = SUPERVISORY[(t.asset_class, t.subclass)]
        entry = by_hs[(t.basis, t.volatility)].setdefault(t.entity, [0.0, sf * _sf_scale(t), rho])
        entry[0] += effective_notional(t, margined, mpor_days)
    total = 0.0
    detail = {}
    for hs, entities in by_hs.items():
        rows = [(rho, en * sf) for en, sf, rho in entities.values()]
        addon, sys_, idio = _single_factor(rows)
        detail[hs] = {"entities": {e: en * sf for e, (en, sf, _) in entities.items()}, "systematic": sys_, "idiosyncratic": idio}
        total += addon
    return total, detail


def addon_commodity(trades: Sequence[Trade], margined: bool, mpor_days: float) -> tuple[float, dict]:
    """CRE52.70: commodity types combined within each of the four hedging sets, hedging sets summed."""
    by_hs: dict[tuple, dict[str, list]] = defaultdict(dict)
    for t in trades:
        sf, rho, _ = SUPERVISORY[("COMMODITY", t.subclass)]
        entry = by_hs[_hs_key(t)].setdefault(t.entity, [0.0, sf * _sf_scale(t), rho])
        entry[0] += effective_notional(t, margined, mpor_days)
    total = 0.0
    detail = {}
    for hs, types in by_hs.items():
        addon, _, _ = _single_factor((rho, en * sf) for en, sf, rho in types.values())
        detail[hs] = {"types": {c: en * sf for c, (en, sf, _) in types.items()}, "AddOn": addon}
        total += addon
    return total, detail


def replacement_cost(v: float, c: float, margined: bool, th: float = 0.0, mta: float = 0.0, nica: float = 0.0) -> float:
    """CRE52.10 unmargined: max(V - C, 0); CRE52.18 margined: max(V - C, TH + MTA - NICA, 0)."""
    if margined:
        return max(v - c, th + mta - nica, 0.0)
    return max(v - c, 0.0)


def pfe_multiplier(v: float, c: float, addon_aggregate: float) -> float:
    """CRE52.23: min(1, Floor + (1 - Floor) exp((V - C) / (2 (1 - Floor) AddOn))), Floor = 5%."""
    if addon_aggregate <= 0.0:
        return 1.0
    f = MULTIPLIER_FLOOR
    return min(1.0, f + (1.0 - f) * math.exp((v - c) / (2.0 * (1.0 - f) * addon_aggregate)))


@dataclass(frozen=True)
class NettingSet:
    trades: tuple[Trade, ...]
    collateral: float = 0.0  # C: haircut net collateral held (+) or posted (-), VM and NICA included (CRE52.10, CRE52.18)
    margined: bool = False
    threshold: float = 0.0
    mta: float = 0.0
    nica: float = 0.0
    mpor_days: float = 10.0


@dataclass(frozen=True)
class SACCRResult:
    v: float
    rc: float
    addons: dict[str, float]
    addon_aggregate: float
    multiplier: float
    pfe: float
    ead: float
    detail: dict


def addon_by_asset_class(trades: Sequence[Trade], margined: bool, mpor_days: float, ir_offset: bool = True) -> tuple[dict, dict]:
    groups: dict[str, list[Trade]] = defaultdict(list)
    for t in trades:
        groups[t.asset_class].append(t)
    addons: dict[str, float] = {}
    detail: dict[str, dict] = {}
    for ac, ts in groups.items():
        if ac == "IR":
            addons[ac], detail[ac] = addon_ir(ts, margined, mpor_days, ir_offset)
        elif ac == "FX":
            addons[ac], detail[ac] = addon_fx(ts, margined, mpor_days)
        elif ac in ("CREDIT", "EQUITY"):
            addons[ac], detail[ac] = addon_credit_or_equity(ts, margined, mpor_days)
        elif ac == "COMMODITY":
            addons[ac], detail[ac] = addon_commodity(ts, margined, mpor_days)
        else:
            raise ValueError(f"unknown asset class {ac!r}")
    return addons, detail


def saccr_ead(ns: NettingSet, ir_offset: bool = True) -> SACCRResult:
    """EAD = alpha (RC + PFE) (CRE52.1); margined EAD capped at the unmargined EAD of the same set (CRE52.2)."""
    v = sum(t.mtm for t in ns.trades)
    rc = replacement_cost(v, ns.collateral, ns.margined, ns.threshold, ns.mta, ns.nica)
    addons, detail = addon_by_asset_class(ns.trades, ns.margined, ns.mpor_days, ir_offset)
    aggregate = sum(addons.values())  # CRE52.25: no diversification across asset classes
    mult = pfe_multiplier(v, ns.collateral, aggregate)
    pfe = mult * aggregate
    ead = ALPHA * (rc + pfe)
    if ns.margined:
        unmargined = saccr_ead(NettingSet(ns.trades, ns.collateral, margined=False), ir_offset)
        ead = min(ead, unmargined.ead)
    return SACCRResult(v, rc, addons, aggregate, mult, pfe, ead, detail)


def rc_shared_margin_agreement(netting_set_values: Sequence[float], collateral: float) -> float:
    """CRE52.75: RC_MA = max(sum max(V_NS, 0) - max(C_MA, 0), 0) + max(sum min(V_NS, 0) - min(C_MA, 0), 0)."""
    first = max(sum(max(v, 0.0) for v in netting_set_values) - max(collateral, 0.0), 0.0)
    second = max(sum(min(v, 0.0) for v in netting_set_values) - min(collateral, 0.0), 0.0)
    return first + second


# ============================================================================
# 5. Self-checks against the Basel Committee's published examples
# ============================================================================

# CRE99.2 Table 1: PD -> risk weights for (corporate LGD 40% S=50, corporate LGD 40% S=5, mortgage 45%, mortgage 25%,
# other retail 45%, other retail 85%, QRRE 50%, QRRE 85%), M = 2.5 where applicable.
CRE99_TABLE_1 = {
    0.0005: (17.47, 13.69, 6.23, 3.46, 6.63, 12.52, 1.68, 2.86),
    0.0010: (26.36, 20.71, 10.69, 5.94, 11.16, 21.08, 3.01, 5.12),
    0.0025: (43.97, 34.68, 21.30, 11.83, 21.15, 39.96, 6.40, 10.88),
    0.0040: (55.75, 43.99, 29.94, 16.64, 28.42, 53.69, 9.34, 15.88),
    0.0050: (61.88, 48.81, 35.08, 19.49, 32.36, 61.13, 11.16, 18.97),
    0.0075: (73.58, 57.91, 46.46, 25.81, 40.10, 75.74, 15.33, 26.06),
    0.0100: (82.06, 64.35, 56.40, 31.33, 45.77, 86.46, 19.14, 32.53),
    0.0130: (89.73, 70.02, 67.00, 37.22, 50.80, 95.95, 23.35, 39.70),
    0.0150: (93.86, 72.99, 73.45, 40.80, 53.37, 100.81, 25.99, 44.19),
    0.0200: (102.09, 78.71, 87.94, 48.85, 57.99, 109.53, 32.14, 54.63),
    0.0250: (108.58, 83.05, 100.64, 55.91, 60.90, 115.03, 37.75, 64.18),
    0.0300: (114.17, 86.74, 111.99, 62.22, 62.79, 118.61, 42.96, 73.03),
    0.0400: (124.07, 93.37, 131.63, 73.13, 65.01, 122.80, 52.40, 89.08),
    0.0500: (133.20, 99.79, 148.22, 82.35, 66.42, 125.45, 60.83, 103.41),
    0.0600: (141.88, 106.21, 162.52, 90.29, 67.73, 127.94, 68.45, 116.37),
    0.1000: (171.63, 130.23, 204.41, 113.56, 75.54, 142.69, 93.21, 158.47),
    0.1500: (196.92, 152.81, 235.72, 130.96, 88.60, 167.36, 115.43, 196.23),
    0.2000: (211.76, 167.48, 253.12, 140.62, 100.28, 189.41, 131.09, 222.86),
}


def cre99_table_1_row(pd: float) -> tuple[float, ...]:
    """Recompute one row of CRE99.2 Table 1 in percent."""
    return (
        irb_corporate(pd, 0.40, 1.0, 2.5, sales_eur_m=50.0).risk_weight * 100,
        irb_corporate(pd, 0.40, 1.0, 2.5, sales_eur_m=5.0).risk_weight * 100,
        irb_retail(pd, 0.45, 1.0, "mortgage").risk_weight * 100,
        irb_retail(pd, 0.25, 1.0, "mortgage").risk_weight * 100,
        irb_retail(pd, 0.45, 1.0, "other").risk_weight * 100,
        irb_retail(pd, 0.85, 1.0, "other").risk_weight * 100,
        irb_retail(pd, 0.50, 1.0, "qrre").risk_weight * 100,
        irb_retail(pd, 0.85, 1.0, "qrre").risk_weight * 100,
    )


def cre99_portfolios() -> dict[str, NettingSet]:
    """The SA-CCR sample netting sets of CRE99.22, CRE99.41, CRE99.59, CRE99.77 and CRE99.80 (USD thousands)."""
    swaption = OptionTerms(call=False, bought=True, underlying=0.06, strike=0.05, expiry=1.0)
    ir = (
        Trade("IR1", "IR", "", 10_000, 30, 10.0, direction=+1, end=10.0, hedging_set="USD"),
        Trade("IR2", "IR", "", 10_000, -20, 4.0, direction=-1, end=4.0, hedging_set="USD"),
        Trade("IR3", "IR", "", 5_000, 50, 11.0, start=1.0, end=11.0, hedging_set="EUR", option=swaption),
    )
    credit = (
        Trade("CR1", "CREDIT", "AA", 10_000, 20, 3.0, direction=+1, end=3.0, entity="Firm A"),
        Trade("CR2", "CREDIT", "BBB", 10_000, -40, 6.0, direction=-1, end=6.0, entity="Firm B"),
        Trade("CR3", "CREDIT", "INDEX_IG", 10_000, 0, 5.0, direction=+1, end=5.0, entity="CDX.IG"),
    )
    commodity = (
        Trade("CO1", "COMMODITY", "OIL_GAS", 10_000, -50, 0.75, direction=+1, hedging_set="ENERGY", entity="Crude oil"),
        Trade("CO2", "COMMODITY", "OIL_GAS", 20_000, -30, 2.0, direction=-1, hedging_set="ENERGY", entity="Crude oil"),
        Trade("CO3", "COMMODITY", "METALS", 10_000, 100, 5.0, direction=+1, hedging_set="METALS", entity="Silver"),
    )
    mpor = 9 + 5  # CRE99.83: weekly re-margining, MPOR = 9 + 5 business days (CRE52.50(2))
    return {
        "ex1": NettingSet(ir),
        "ex2": NettingSet(credit),
        "ex3": NettingSet(commodity),
        "ex4": NettingSet(ir + credit),
        "ex5": NettingSet(ir + commodity, collateral=200, margined=True, threshold=0, mta=5, nica=150, mpor_days=mpor),
    }


def _close(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def run_tests() -> None:
    print("Basel credit risk and SA-CCR self-checks")

    # --- SA risk weights and CCFs -------------------------------------------------
    assert sa_sovereign_rw("AA-") == 0.0 and sa_sovereign_rw("A+") == 0.20 and sa_sovereign_rw("B-") == 1.00
    assert sa_sovereign_rw("CCC") == 1.50 and sa_sovereign_rw(None) == 1.00
    assert sa_bank_rw_ecra("A") == 0.30 and sa_bank_rw_ecra("A", short_term=True) == 0.20
    assert sa_bank_rw_scra("A", cet1_ge_14_and_lev_ge_5=True) == 0.30 and sa_bank_rw_scra("B") == 0.75
    assert sa_corporate_rw("BBB") == 0.75 and sa_corporate_rw("BB-") == 1.00 and sa_corporate_rw("B+") == 1.50
    assert sa_corporate_rw(None, sme=True) == 0.85
    assert sa_residential_re_rw(0.55) == 0.25 and sa_residential_re_rw(0.85) == 0.40 and sa_residential_re_rw(1.10) == 0.70
    # CRE20.83 footnote 120: EUR 70,000 loan on EUR 100,000 property, loan splitting -> RWA 22,250.
    assert _close(0.20 * 55_000 + 0.75 * (70_000 - 55_000), 22_250, 1e-9)

    # --- IRB: all 144 risk weights of CRE99.2 Table 1 ------------------------------
    worst = 0.0
    for pd, published in CRE99_TABLE_1.items():
        for mine, theirs in zip(cre99_table_1_row(pd), published, strict=True):
            worst = max(worst, abs(mine - theirs))
            assert abs(mine - theirs) <= 0.006, (pd, mine, theirs)
    print(f"  CRE99 Table 1: 144 IRB risk weights reproduced, max abs difference {worst:.4f} pct points")

    corp = irb_corporate(0.01, 0.40, 1_000_000, 2.5)
    print(f"  Corporate PD 1% LGD 40% M 2.5: R {corp.correlation:.6f} b {corp.b:.6f} K {corp.k:.6f} RW {corp.risk_weight:.4%}")
    assert _close(corp.risk_weight * 100, 82.06, 0.006)
    # 1.25 multiplier for large financials (CRE31.7) at PD 1%.
    fi = irb_corporate(0.01, 0.45, 1.0, 2.5, large_or_unregulated_fi=True)
    assert _close(fi.correlation, 1.25 * corp.correlation, 1e-12)
    # PD floor (CRE32.4) binds for a corporate but not for a sovereign.
    assert irb_corporate(0.0001, 0.45, 1.0).pd == 0.0005 and irb_corporate(0.0001, 0.45, 1.0, sovereign=True).pd == 0.0001
    # At M = 1 the full maturity adjustment (1 + (M - 2.5) b) / (1 - 1.5 b) is exactly 1.
    k1 = irb_corporate(0.01, 0.40, 1.0, 1.0).k
    assert _close(k1, 0.40 * conditional_pd(0.01, corp.correlation) - 0.01 * 0.40, 1e-15)
    # F-IRB secured LGD (CRE32.10 to CRE32.11): 100 loan, 60 of real estate collateral at 40% haircut, senior corporate.
    # E_S = 60 x 0.6 = 36, E_U = 64, LGD* = (0.40 x 64 + 0.20 x 36) / 100 = 0.328.
    lgd_star = firb_secured_lgd(100.0, 0.0, 60.0, 0.40, 0.20, FIRB_LGD_SENIOR_CORPORATE)
    assert _close(lgd_star, 0.328, 1e-12)
    print(f"  F-IRB LGD* with 60 of real estate on a 100 loan: {lgd_star:.4f}")

    # --- Output floor: RBC20.13 Table 1 and RBC90.2 ------------------------------
    assert _close(floored_rwa(76, 140), 101.5, 1e-9)
    assert _close(floored_rwa(76, 140, cap=TRANSITIONAL_CAP), 95.0, 1e-9)
    assert _close(floored_rwa(76, 140, calibration=OUTPUT_FLOOR_PHASE_IN[2026]), 91.0, 1e-9)
    print("  Output floor RBC20.13: 101.5; with RBC90.2 cap: 95.0; at the 2026 65% calibration: 91.0")

    # --- SA-CCR: the five CRE99 sample portfolios --------------------------------
    p = cre99_portfolios()
    ir_trades = p["ex1"].trades
    assert [round(supervisory_duration(t.start, t.end), 2) for t in ir_trades] == [7.87, 3.63, 7.49]
    assert [round(adjusted_notional(t)) for t in ir_trades] == [78_694, 36_254, 37_428]
    assert round(supervisory_delta(ir_trades[2]), 4) == -0.2694
    assert [round(effective_notional(t, False, 10)) for t in ir_trades] == [78_694, -36_254, -10_083]

    r1 = saccr_ead(p["ex1"])
    usd = r1.detail["IR"][("USD", False, False)]
    eur = r1.detail["IR"][("EUR", False, False)]
    print(f"  Ex1 IR: EN_USD {usd['EN']:,.0f} AddOn_USD {usd['AddOn']:,.1f} AddOn_EUR {eur['AddOn']:,.1f}")
    print(f"  Ex1 IR: V {r1.v:,.0f} RC {r1.rc:,.0f} AddOn {r1.addon_aggregate:,.1f} multiplier {r1.multiplier:.4f} EAD {r1.ead:,.1f}")

    r2 = saccr_ead(p["ex2"])
    cr = r2.detail["CREDIT"][(False, False)]
    assert [round(cr["entities"][e]) for e in ("Firm A", "Firm B", "CDX.IG")] == [106, -280, 168]
    assert round(cr["systematic"], 1) == 47.5 and round(cr["idiosyncratic"]) == 77_344
    assert [round(adjusted_notional(t)) for t in p["ex2"].trades] == [27_858, 51_836, 44_240]
    print(
        f"  Ex2 credit: systematic^2 {cr['systematic'] ** 2:,.0f} idiosyncratic {cr['idiosyncratic']:,.0f}"
        f" AddOn {r2.addon_aggregate:,.1f} multiplier {r2.multiplier:.4f} EAD {r2.ead:,.1f}"
    )

    r3 = saccr_ead(p["ex3"])
    co = r3.detail["COMMODITY"]
    assert round(effective_notional(p["ex3"].trades[0], False, 10)) == 8_660
    assert round(co[("ENERGY", False, False)]["types"]["Crude oil"]) == -2_041
    assert round(co[("METALS", False, False)]["types"]["Silver"]) == 1_800
    print(f"  Ex3 commodity: V {r3.v:,.0f} RC {r3.rc:,.0f} AddOn {r3.addon_aggregate:,.1f} EAD {r3.ead:,.1f}")

    r4 = saccr_ead(p["ex4"])
    assert _close(r4.addon_aggregate, r1.addon_aggregate + r2.addon_aggregate, 1e-9)
    print(f"  Ex4 IR + credit: V {r4.v:,.0f} RC {r4.rc:,.0f} AddOn {r4.addon_aggregate:,.1f} EAD {r4.ead:,.1f}")

    r5 = saccr_ead(p["ex5"])
    mf = maturity_factor_margined(14)
    assert [round(effective_notional(t, True, 14)) for t in p["ex1"].trades] == [27_934, -12_869, -3_579]
    # CRE99.90 prints -7,100 for trade 2; 20,000 x 0.354965 = -7,099.3, so the table rounds to the nearest 50.
    published = [3_550, -7_100, 3_550]
    assert all(_close(effective_notional(t, True, 14), x, 1.0) for t, x in zip(p["ex3"].trades, published, strict=True))
    assert r5.rc == 0.0 and _close(r5.v, 80, 1e-9)
    print(
        f"  Ex5 margined: MF {mf:.6f} RC {r5.rc:,.0f} AddOn_IR {r5.addons['IR']:,.1f} AddOn_COM {r5.addons['COMMODITY']:,.1f}"
        f" multiplier {r5.multiplier:.4f} EAD {r5.ead:,.1f}"
    )

    # --- Replacement cost with margin agreements: CRE99.98 to CRE99.115 -------------
    assert replacement_cost(80, 90, True, 0, 1, 10) == 0.0  # Example 1
    assert replacement_cost(80, 79.5 + 10 - 10, True, 0, 1, 0) == 1.0  # Example 2
    assert replacement_cost(-50, -50, True, 0, 0, 0) == 0.0  # Example 3
    assert replacement_cost(-50, -60, True, 0, 0, -10) == 10.0  # Example 4
    assert replacement_cost(50, 80, True, 0, 0, 20) == 0.0  # Example 5
    assert rc_shared_margin_agreement([30, -10], 15) == 15.0

    # --- Multiplier behaviour (CRE52.23) and MPOR floors (CRE52.50 to CRE52.51) -------
    assert pfe_multiplier(10, 0, 100) == 1.0
    assert _close(pfe_multiplier(-1e9, 0, 100), MULTIPLIER_FLOOR, 1e-12)
    assert mpor_floor_days() == 10 and mpor_floor_days(daily_margin=False, remargin_period_days=5) == 14
    assert mpor_floor_days(trades_in_netting_set=6000) == 20 and mpor_floor_days(disputes_exceeding_mpor_last_two_quarters=3) == 20
    # CDO tranche delta (CRE52.41): 3% to 7% tranche, protection bought.
    cdo = Trade("T1", "CREDIT", "INDEX_IG", 1.0, 0.0, 5.0, direction=+1, end=5.0, entity="CDX", cdo_attach_detach=(0.03, 0.07))
    print(f"  CDO 3-7% tranche supervisory delta (bought protection): {supervisory_delta(cdo):.4f}")
    # Margined EAD never exceeds unmargined EAD (CRE52.2).
    unm = saccr_ead(NettingSet(p["ex5"].trades, collateral=200))
    assert r5.ead <= unm.ead + 1e-9
    print("All Basel credit risk and SA-CCR checks passed.")


if __name__ == "__main__":
    run_tests()
