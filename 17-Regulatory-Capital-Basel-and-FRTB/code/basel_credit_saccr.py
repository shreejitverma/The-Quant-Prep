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
It also computes, prints and asserts every number quoted in notes 03 (credit risk capital) and 04 (SA-CCR),
each to within half a unit of its last quoted decimal.
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
    Applying the 1.25 multiplier before the SME deduction is an ordering choice of this implementation:
    CRE31.7 and CRE31.8 do not say how to combine them (a financial institution with sales below EUR 50m is rare).
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
    basis: str = ""  # CRE52.46: the specific basis (pair of risk factors); each basis is its own hedging set at half the factor
    volatility: bool = False  # CRE52.47: separate hedging set and five times the supervisory factor

    def __post_init__(self) -> None:
        if self.basis and self.volatility:
            raise ValueError(f"{self.trade_id}: a trade is either a basis or a volatility transaction, not both")


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


def option_d(trade: Trade) -> float:
    """CRE52.40: d = (ln((P + lambda) / (K + lambda)) + 0.5 sigma^2 T) / (sigma sqrt(T)) with the supervisory volatility."""
    if trade.option is None:
        raise ValueError(f"{trade.trade_id} is not an option")
    o = trade.option
    vol = SUPERVISORY[(trade.asset_class, trade.subclass)][2]
    return (math.log((o.underlying + o.shift) / (o.strike + o.shift)) + 0.5 * vol**2 * o.expiry) / (vol * math.sqrt(o.expiry))


def supervisory_delta(trade: Trade) -> float:
    """CRE52.39 to CRE52.41: +1/-1 for linear trades, Black-Scholes style delta for options, tranche formula for CDOs."""
    if trade.option is not None:
        o = trade.option
        d = option_d(trade)
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


def _hs_key(trade: Trade) -> tuple[str, str, bool]:
    """Hedging set: currency, pair or commodity group, split by specific basis (CRE52.46) and volatility (CRE52.47)."""
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

    Non-basis, non-volatility trades share one hedging set (CRE52.45); each specific basis is a separate hedging set
    (CRE52.46) and volatility trades form one more (CRE52.47); hedging-set add-ons are summed.
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


# CRE99.40, CRE99.58, CRE99.76, CRE99.79 and CRE99.97 print each sample EAD rounded to USD thousands.
CRE99_PUBLISHED_EAD = {"ex1": 569, "ex2": 381, "ex3": 5_406, "ex4": 936, "ex5": 1_879}

QUOTED_LOG: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number that a note quotes and assert that it rounds to the quoted figure.

    The tolerance is half a unit in the last quoted decimal place, so a figure quoted as 82.06 must lie in [82.055, 82.065].
    """
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED_LOG.append(label)
    print(f"    {label}: {value:,.{decimals}f}")
    return value


def _close(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def maturity_adjustment(pd: float, maturity: float) -> float:
    """CRE31.5: (1 + (M - 2.5) b) / (1 - 1.5 b)."""
    b = maturity_b(pd)
    return (1.0 + (maturity - 2.5) * b) / (1.0 - 1.5 * b)


def _check_cre99_table_1() -> None:
    """All 144 risk weights of CRE99.2 Table 1: 141 within the 0.005 rounding of the table, 3 off by at most 0.006."""
    worst = 0.0
    within_rounding = 0
    beyond: dict[tuple[float, int], float] = {}
    for pd, published in CRE99_TABLE_1.items():
        for col, (mine, theirs) in enumerate(zip(cre99_table_1_row(pd), published, strict=True)):
            diff = abs(mine - theirs)
            worst = max(worst, diff)
            assert diff <= 0.006, (pd, col, mine, theirs)
            if diff <= 0.005:
                within_rounding += 1
            else:
                beyond[(pd, col)] = mine
    print(f"  CRE99 Table 1: {within_rounding} of 144 IRB risk weights within 0.005 pct points, {len(beyond)} beyond, max {worst:.4f}")
    quoted("Table 1 cells within 0.005 pct points", within_rounding, 141, 0)
    quoted("Table 1 max abs difference (pct points)", worst, 0.006, 3)
    # Columns: 2 = mortgage LGD 45%, 4 = other retail LGD 45%, 5 = other retail LGD 85%.
    assert set(beyond) == {(0.015, 2), (0.001, 5), (0.013, 4)}, beyond
    quoted("PD 1.5% mortgage LGD 45% RW (published 73.45)", beyond[(0.015, 2)], 73.444, 3)
    quoted("PD 0.1% other retail LGD 85% RW (published 21.08)", beyond[(0.001, 5)], 21.086, 3)
    quoted("PD 1.3% other retail LGD 45% RW (published 50.80)", beyond[(0.013, 4)], 50.794, 3)


def _check_credit_note() -> None:
    """Every computed number quoted in 03-Credit-Risk-Capital-SA-and-IRB.md."""
    q = quoted
    print("  Note 03, core concepts")
    q("RWA scalar 1 / 8%", 1.0 / 0.08, 12.5, 1)
    q("8% capital per 100 at RW 100%", 100 * 1.00 / 12.5, 8, 0)
    q("corporate R at PD 0 (%)", corporate_correlation(0.0) * 100, 24, 0)
    q("corporate R at PD 1 (%)", corporate_correlation(1.0) * 100, 12, 0)
    q("large financial R at PD 0 (%)", corporate_correlation(0.0, large_or_unregulated_fi=True) * 100, 30, 0)
    q("large financial R at PD 1 (%)", corporate_correlation(1.0, large_or_unregulated_fi=True) * 100, 15, 0)
    q("HVCRE R at PD 0 (%)", hvcre_correlation(0.0) * 100, 30, 0)
    q("HVCRE R at PD 1 (%)", hvcre_correlation(1.0) * 100, 12, 0)
    q("other retail R at PD 0 (%)", retail_correlation(0.0, "other") * 100, 16, 0)
    q("other retail R at PD 1 (%)", retail_correlation(1.0, "other") * 100, 3, 0)
    q("maximum SME deduction (sales <= EUR 5m)", corporate_correlation(0.01) - corporate_correlation(0.01, sales_eur_m=1.0), 0.04, 2)
    q("MA at PD 0.1%, M 2.5", maturity_adjustment(0.001, 2.5), 1.588, 3)
    q("MA at PD 0.1%, M 5", maturity_adjustment(0.001, 5.0), 2.569, 3)
    q("MA at PD 10%, M 2.5", maturity_adjustment(0.10, 2.5), 1.099, 3)
    q("MA at PD 10%, M 5", maturity_adjustment(0.10, 5.0), 1.263, 3)
    assert _close(maturity_adjustment(0.01, 1.0), 1.0, 1e-15)
    q("K at LGD 45%, M 2.5, PD 0.05%", irb_corporate(0.0005, 0.45, 1.0).k, 0.0157, 4)
    q("K at LGD 45%, M 2.5, PD 30%", irb_corporate(0.30, 0.45, 1.0).k, 0.1991, 4)
    q("K at LGD 45%, M 2.5, PD 50%", irb_corporate(0.50, 0.45, 1.0).k, 0.1743, 4)
    peak = max(range(1, 1000), key=lambda i: irb_corporate(i / 1000, 0.45, 1.0).k) / 1000
    q("PD at which K peaks, LGD 45%, M 2.5 (%)", peak * 100, 30, 0)

    print("  Note 03, Example 1: F-IRB corporate PD 1%, LGD 40%, M 2.5, EAD 10,000,000")
    pd, lgd, ead = 0.01, 0.40, 10_000_000
    w = _pd_weight(pd, 50.0)
    r = corporate_correlation(pd)
    g_pd, g_q = norm_ppf(pd), norm_ppf(CONFIDENCE)
    numerator = g_pd + math.sqrt(r) * g_q
    arg = numerator / math.sqrt(1.0 - r)
    q("w50", w, 0.393469, 6)
    q("1 - w50", 1.0 - w, 0.606531, 6)
    q("R", r, 0.192784, 6)
    q("G(0.01)", g_pd, -2.326348, 6)
    q("G(0.999)", g_q, 3.090232, 6)
    q("sqrt(R)", math.sqrt(r), 0.439071, 6)
    q("sqrt(1 - R)", math.sqrt(1.0 - r), 0.898452, 6)
    q("numerator", numerator, -0.969515, 6)
    q("argument", arg, -1.079095, 6)
    q("stressed PD", norm_cdf(arg), 0.140273, 6)
    q("unexpected loss per unit", lgd * norm_cdf(arg) - pd * lgd, 0.052109, 6)
    q("ln 0.01", math.log(pd), -4.605170, 6)
    q("b", maturity_b(pd), 0.137486, 6)
    q("MA", maturity_adjustment(pd, 2.5), 1.259810, 6)
    corp = irb_corporate(pd, lgd, ead)
    q("K", corp.k, 0.065648, 6)
    q("RW (%)", corp.risk_weight * 100, 82.06, 2)
    q("RWA", corp.rwa, 8_205_938, 0)
    q("capital K x EAD", corp.k * ead, 656_475, 0)
    assert _close(0.08 * corp.rwa, corp.k * ead, 1e-6)
    q("EL", corp.expected_loss, 40_000, 0)
    q("SA RWA, BBB", sa_corporate_rw("BBB") * ead, 7_500_000, 0)
    q("SA RWA, unrated", sa_corporate_rw(None) * ead, 10_000_000, 0)
    fi = irb_corporate(pd, FIRB_LGD_SENIOR_FINANCIAL, ead, large_or_unregulated_fi=True)
    q("large bank R", fi.correlation, 0.240980, 6)
    q("large bank RW (%)", fi.risk_weight * 100, 117.95, 2)
    q("large bank RWA", fi.rwa, 11_794_939, 0)

    print("  Note 03, Example 2: SME with sales EUR 10m")
    sme = irb_corporate(pd, lgd, 1.0, sales_eur_m=10.0)
    arg_sme = (g_pd + math.sqrt(sme.correlation) * g_q) / math.sqrt(1.0 - sme.correlation)
    q("SME deduction", 0.04 * (1.0 - (10.0 - 5.0) / 45.0), 0.035556, 6)
    q("SME R", sme.correlation, 0.157228, 6)
    q("sqrt(R)", math.sqrt(sme.correlation), 0.396520, 6)
    q("sqrt(1 - R)", math.sqrt(1.0 - sme.correlation), 0.918026, 6)
    q("argument", arg_sme, -1.199322, 6)
    q("stressed PD", norm_cdf(arg_sme), 0.115201, 6)
    q("unexpected loss per unit", lgd * norm_cdf(arg_sme) - pd * lgd, 0.042081, 6)
    for m, large, small in ((1.0, 65.14, 52.60), (2.5, 82.06, 66.27), (5.0, 110.26, 89.04)):
        q(f"large corporate RW at M {m} (%)", irb_corporate(pd, lgd, 1.0, m).risk_weight * 100, large, 2)
        q(f"SME RW at M {m} (%)", irb_corporate(pd, lgd, 1.0, m, sales_eur_m=10.0).risk_weight * 100, small, 2)
    rw1, rw5 = irb_corporate(pd, lgd, 1.0, 1.0).risk_weight, irb_corporate(pd, lgd, 1.0, 5.0).risk_weight
    q("RW increase from M 1 to M 5 (%)", (rw5 / rw1 - 1.0) * 100, 69, 0)
    q("SME saving at M 2.5 (%)", (1.0 - sme.risk_weight / corp.risk_weight) * 100, 19, 0)

    print("  Note 03, Example 3: revolver 20,000,000 limit, 5,000,000 drawn, PD 2%")
    drawn, undrawn = 5_000_000, 15_000_000
    ead_sa = drawn + SA_CCF["commitment"] * undrawn
    q("SA and F-IRB EAD", ead_sa, 11_000_000, 0)
    q("EAD if unconditionally cancellable", drawn + SA_CCF["unconditionally_cancellable"] * undrawn, 6_500_000, 0)
    ead_floor = drawn + 0.5 * SA_CCF["commitment"] * undrawn
    q("A-IRB EAD floor", ead_floor, 8_000_000, 0)
    rev = irb_corporate(0.02, lgd, ead_sa)
    q("R", rev.correlation, 0.164146, 6)
    q("b", rev.b, 0.110770, 6)
    q("K", rev.k, 0.081674, 6)
    q("RW (%)", rev.risk_weight * 100, 102.09, 2)
    q("RW (fraction)", rev.risk_weight, 1.020926, 6)
    q("F-IRB RWA", rev.rwa, 11_230_191, 0)
    q("RWA at the A-IRB EAD floor", irb_corporate(0.02, lgd, ead_floor).rwa, 8_167_412, 0)
    q("SA unrated RWA", sa_corporate_rw(None) * ead_sa, 11_000_000, 0)

    print("  Note 03, Example 4: retail IRB mortgage PD 0.5%, LGD 10%, LTV 55%")
    mort = irb_retail(0.005, 0.10, 1_000_000, "mortgage")
    q("stressed PD", conditional_pd(0.005, mort.correlation), 0.067363, 6)
    q("K", mort.k, 0.006236, 6)
    q("RW (%)", mort.risk_weight * 100, 7.80, 2)
    q("RWA", mort.rwa, 77_954, 0)
    q("SA RW at 55% LTV (%)", sa_residential_re_rw(0.55) * 100, 25, 0)
    q("72.5% of SA RW (%)", OUTPUT_FLOOR * sa_residential_re_rw(0.55) * 100, 18.125, 3)
    q("RW at the 5% LGD floor (%)", irb_retail(0.005, 0.05, 1.0, "mortgage").risk_weight * 100, 3.90, 2)
    q("floored RWA, RBC20.13", floored_rwa(76, 140), 101.5, 1)
    q("floored RWA with the RBC90.2 cap", floored_rwa(76, 140, cap=TRANSITIONAL_CAP), 95, 0)
    q("floored RWA at the 2026 calibration", floored_rwa(76, 140, calibration=OUTPUT_FLOOR_PHASE_IN[2026]), 91, 0)

    print("  Note 03, Example 5 and pitfalls")
    rw_05, rw_3 = irb_corporate(0.005, lgd, 1.0).risk_weight, irb_corporate(0.03, lgd, 1.0).risk_weight
    q("RW at PD 0.5% (%)", rw_05 * 100, 61.88, 2)
    q("RW at PD 3% (%)", rw_3 * 100, 114.17, 2)
    q("ratio", rw_3 / rw_05, 1.845, 3)
    for p, uplift in ((0.0005, 36), (0.01, 28), (0.10, 17)):
        base = irb_corporate(p, 0.45, 1.0).risk_weight
        multiplied = irb_corporate(p, 0.45, 1.0, large_or_unregulated_fi=True).risk_weight
        q(f"1.25 multiplier RW uplift at PD {p:.2%} (%)", (multiplied / base - 1.0) * 100, uplift, 0)

    print("  Note 03, interview cards")
    q("w50 at PD 7%", _pd_weight(0.07, 50.0), 0.97, 2)
    q("MA at PD 1%, M 2.5", maturity_adjustment(pd, 2.5), 1.2598, 4)
    q("R at PD 1%", corp.correlation, 0.1928, 4)
    q("stressed PD at PD 1% (%)", conditional_pd(pd, corp.correlation) * 100, 14.03, 2)
    q("stressed PD at PD 1%", conditional_pd(pd, corp.correlation), 0.14027, 5)
    q("unexpected loss per unit", lgd * norm_cdf(arg) - pd * lgd, 0.05211, 5)
    q("PD x LGD", pd * lgd, 0.004, 3)
    q("b at PD 1%", corp.b, 0.1375, 4)
    q("K at PD 1%", corp.k, 0.06565, 5)
    q("RW at PD 1% with the pre-2017 LGD 45% (%)", irb_corporate(pd, 0.45, 1.0).risk_weight * 100, 92.32, 2)
    q("SME R at sales EUR 10m", sme.correlation, 0.1572, 4)
    e_s, e_u = 60.0 * (1.0 - 0.40), 100.0 - 60.0 * (1.0 - 0.40)
    q("E_S", e_s, 36, 0)
    q("E_U", e_u, 64, 0)
    q("F-IRB LGD* with 60 of real estate (%)", firb_secured_lgd(100.0, 0.0, 60.0, 0.40, 0.20, FIRB_LGD_SENIOR_CORPORATE) * 100, 32.8, 1)


def _check_saccr_note(p: dict[str, NettingSet]) -> None:
    """Every computed number quoted in 04-Counterparty-Credit-Risk-SA-CCR.md (USD thousands)."""
    q = quoted
    print("  Note 04, core concepts")
    mf10 = maturity_factor_margined(10)
    q("margined MF at the 10-day MPOR floor", mf10, 0.30, 2)
    q("add-on removed by daily margining for M >= 1y (%)", (1.0 - mf10 / maturity_factor_unmargined(5.0)) * 100, 70, 0)
    q("multiplier one add-on out of the money (%)", pfe_multiplier(-1.0, 0.0, 1.0) * 100, 61.1, 1)
    q("SD as E grows with S = 0", supervisory_duration(0.0, 1_000.0), 20, 0)
    q("minimum EAD per unit add-on, alpha x floor", ALPHA * MULTIPLIER_FLOOR, 0.07, 2)
    # Margined MF exceeds unmargined MF while M < 2.25 x MPOR: 22.5 business days at the 10-day floor (CRE52.2 FAQ1).
    crossover_days = (mf10 / 1.0) ** 2 * BUSINESS_DAYS_PER_YEAR
    q("margined MF > unmargined MF below M (business days)", crossover_days, 22.5, 1)
    assert mf10 > maturity_factor_unmargined(22 / BUSINESS_DAYS_PER_YEAR)
    assert mf10 < maturity_factor_unmargined(23 / BUSINESS_DAYS_PER_YEAR)
    assert maturity_factor_margined(14) > maturity_factor_unmargined(31 / BUSINESS_DAYS_PER_YEAR)  # 2.25 x 14 = 31.5

    print("  Note 04, Example 1: IR swaps and a swaption, unmargined")
    ir = p["ex1"].trades
    r1 = saccr_ead(p["ex1"])
    for t, sd in zip(ir, (7.8694, 3.6254, 7.4856), strict=True):
        q(f"{t.trade_id} supervisory duration", supervisory_duration(t.start, t.end), sd, 4)
    for t, d in zip(ir, (78_694, 36_254, 37_428), strict=True):
        q(f"{t.trade_id} adjusted notional", adjusted_notional(t), d, 0)
    q("swaption d", option_d(ir[2]), 0.614643, 6)
    q("swaption delta", supervisory_delta(ir[2]), -0.2694, 4)
    for t, d in zip(ir, (78_694, -36_254, -10_083), strict=True):
        q(f"{t.trade_id} effective notional", effective_notional(t, False, 10), d, 0)
    usd = r1.detail["IR"][("USD", "", False)]
    eur = r1.detail["IR"][("EUR", "", False)]
    q("V", r1.v, 60, 0)
    q("RC", r1.rc, 60, 0)
    q("multiplier", r1.multiplier, 1, 0)
    q("EN_USD", usd["EN"], 59_270, 0)
    q("AddOn_USD", usd["AddOn"], 296.35, 2)
    q("EN_EUR", eur["EN"], 10_083, 0)
    q("AddOn_EUR", eur["AddOn"], 50.41, 2)
    q("AddOn_IR", r1.addon_aggregate, 346.8, 1)
    q("EAD", r1.ead, 569.5, 1)
    no_offset = saccr_ead(p["ex1"], ir_offset=False)
    q("AddOn_IR without cross-bucket offset", no_offset.addon_aggregate, 625.2, 1)
    q("EAD without cross-bucket offset", no_offset.ead, 959.2, 1)
    q("USD net D_B3 + D_B2 (card)", usd["DB"][2] + usd["DB"][1], 42_440, 0)
    q("10-year SD (card)", supervisory_duration(0.0, 10.0), 7.87, 2)
    q("4-year SD (card)", supervisory_duration(0.0, 4.0), 3.63, 2)

    print("  Note 04, Example 2: credit default swaps")
    cr_trades = p["ex2"].trades
    r2 = saccr_ead(p["ex2"])
    cr = r2.detail["CREDIT"][("", False)]
    q("V", r2.v, -20, 0)
    q("RC", r2.rc, 0, 0)
    for t, sd in zip(cr_trades, (2.7858, 5.1836, 4.4240), strict=True):
        q(f"{t.trade_id} supervisory duration", supervisory_duration(t.start, t.end), sd, 4)
    for t, d in zip(cr_trades, (27_858, -51_836, 44_240), strict=True):
        q(f"{t.trade_id} effective notional", effective_notional(t, False, 10), d, 0)
    for e, a in (("Firm A", 105.9), ("Firm B", -279.9), ("CDX.IG", 168.1)):
        q(f"AddOn {e}", cr["entities"][e], a, 1)
    q("systematic term", cr["systematic"], 47.5, 1)
    q("systematic term squared", cr["systematic"] ** 2, 2_253, 0)
    q("idiosyncratic term", cr["idiosyncratic"], 77_344, 0)
    q("AddOn_Credit", r2.addon_aggregate, 282.1, 1)
    q("multiplier", r2.multiplier, 0.9652, 4)
    q("PFE", r2.pfe, 272.3, 1)
    q("EAD", r2.ead, 381.2, 1)

    print("  Note 04, Example 3: commodity forwards")
    co_trades = p["ex3"].trades
    r3 = saccr_ead(p["ex3"])
    co = r3.detail["COMMODITY"]
    q("V", r3.v, 20, 0)
    q("RC", r3.rc, 20, 0)
    q("multiplier", r3.multiplier, 1, 0)
    q("MF at 9 months", maturity_factor_unmargined(0.75), 0.8660, 4)
    for t, d in zip(co_trades, (8_660, -20_000, 10_000), strict=True):
        q(f"{t.trade_id} effective notional", effective_notional(t, False, 10), d, 0)
    q("EN_crude", sum(effective_notional(t, False, 10) for t in co_trades[:2]), -11_340, 0)
    q("AddOn_energy", co[("ENERGY", "", False)]["AddOn"], 2_041.2, 1)
    q("AddOn_metals", co[("METALS", "", False)]["AddOn"], 1_800, 0)
    q("AddOn_Commodity", r3.addon_aggregate, 3_841.2, 1)
    q("EAD", r3.ead, 5_405.6, 1)

    print("  Note 04, Example 4: Examples 1 and 2 in one netting set")
    r4 = saccr_ead(p["ex4"])
    assert _close(r4.addon_aggregate, r1.addon_aggregate + r2.addon_aggregate, 1e-9)
    q("V", r4.v, 40, 0)
    q("RC", r4.rc, 40, 0)
    q("AddOn", r4.addon_aggregate, 628.9, 1)
    q("multiplier", r4.multiplier, 1, 0)
    q("EAD", r4.ead, 936.5, 1)
    q("EAD of the two sets separately", r1.ead + r2.ead, 950.7, 1)

    print("  Note 04, Example 5: Examples 1 and 3 margined weekly")
    ns5 = p["ex5"]
    r5 = saccr_ead(ns5)
    q("V", r5.v, 80, 0)
    q("V - C", r5.v - ns5.collateral, -120, 0)
    q("TH + MTA - NICA", ns5.threshold + ns5.mta - ns5.nica, -145, 0)
    q("RC", r5.rc, 0, 0)
    q("MPOR (business days)", ns5.mpor_days, 14, 0)
    q("MF", maturity_factor_margined(ns5.mpor_days), 0.354965, 6)
    q("MF (card)", maturity_factor_margined(ns5.mpor_days), 0.355, 3)
    for t, d in zip(ir, (27_934, -12_869, -3_579), strict=True):
        q(f"{t.trade_id} effective notional", effective_notional(t, True, ns5.mpor_days), d, 0)
    q("EN_USD", r5.detail["IR"][("USD", "", False)]["EN"], 21_039, 0)
    q("AddOn_USD", r5.detail["IR"][("USD", "", False)]["AddOn"], 105.2, 1)
    q("AddOn_EUR", r5.detail["IR"][("EUR", "", False)]["AddOn"], 17.9, 1)
    q("AddOn_IR", r5.addons["IR"], 123.1, 1)
    for t, d in zip(co_trades, (3_550, -7_099, 3_550), strict=True):
        q(f"{t.trade_id} effective notional", effective_notional(t, True, ns5.mpor_days), d, 0)
    # CRE99.90 prints -7,100 for trade 2 because it applies MF rounded to 0.355: 0.355 x 20,000 = 7,100.
    assert round(round(maturity_factor_margined(ns5.mpor_days), 3) * co_trades[1].notional) == 7_100
    q("AddOn_energy", r5.detail["COMMODITY"][("ENERGY", "", False)]["AddOn"], 638.94, 2)
    q("AddOn_metals", r5.detail["COMMODITY"][("METALS", "", False)]["AddOn"], 638.94, 2)
    q("AddOn_Commodity", r5.addons["COMMODITY"], 1_277.87, 2)
    q("AddOn aggregate", r5.addon_aggregate, 1_401.0, 1)
    q("multiplier", r5.multiplier, 0.9581, 4)
    q("PFE", r5.pfe, 1_342.3, 1)
    q("EAD", r5.ead, 1_879.2, 1)
    unm = saccr_ead(NettingSet(ns5.trades, collateral=ns5.collateral))
    q("EAD of the same set unmargined", unm.ead, 5_779.7, 1)
    q("EAD reduction from the CSA (%)", (1.0 - r5.ead / unm.ead) * 100, 67, 0)
    assert r5.ead < unm.ead  # the CRE52.2 cap does not bind

    print("  Note 04, Example 6: CRE99.98 to CRE99.115 margin examples (V, C, TH, MTA, NICA)")
    cases = (
        ("VM received, IA 10", 80, 90, 0, 1, 10, -9, 0),
        ("MTA 1, IM 10 each way unsegregated", 80, 79.5, 0, 1, 0, 1, 1),
        ("bankruptcy-remote IM at CCP", -50, -50, 0, 0, 0, 0, 0),
        ("IM at CCP not bankruptcy remote", -50, -60, 0, 0, -10, 10, 10),
        ("maintenance margin 140%", 50, 80, 0, 0, 20, -20, 0),
    )
    for name, v, c, th, mta, nica, level, rc in cases:
        q(f"{name}: TH + MTA - NICA", th + mta - nica, level, 0)
        q(f"{name}: RC", replacement_cost(v, c, True, th, mta, nica), rc, 0)
    q("card: V - C with VM 79.5", 80 - 79.5, 0.5, 1)

    print("  Note 04, Example 7: CDO tranche deltas")
    tranche = {}
    for a, dd, quote, decimals in ((0.03, 0.07, 5.335, 3), (0.0, 0.03, 10.56, 2), (0.15, 1.0, 0.323, 3)):
        t = Trade("T", "CREDIT", "INDEX_IG", 1.0, 0.0, 5.0, end=5.0, entity="CDX", cdo_attach_detach=(a, dd))
        tranche[(a, dd)] = supervisory_delta(t)
        q(f"delta {a:.0%} to {dd:.0%} bought protection", tranche[(a, dd)], quote, decimals)
    q("15% to 100% senior tranche delta (card)", tranche[(0.15, 1.0)], 0.32, 2)
    q("equity / senior delta ratio", tranche[(0.0, 0.03)] / tranche[(0.15, 1.0)], 33, 0)

    print("  Note 04, CRE99 sample EADs against the published figures (rounded to USD thousands)")
    for key, published in CRE99_PUBLISHED_EAD.items():
        ead = saccr_ead(p[key]).ead
        assert abs(ead - published) <= 0.5, (key, ead, published)
        QUOTED_LOG.append(f"{key} EAD against CRE99")
        print(f"    {key} EAD: {ead:,.2f}, published {published:,}")


def _check_basis_hedging_sets() -> None:
    """CRE52.46: a separate hedging set for each specific basis, each at half the supervisory factor."""
    a = Trade("B1", "CREDIT", "A", 10_000, 0.0, 5.0, end=5.0, entity="Firm C", basis="Firm C bond vs CDS")
    b = Trade("B2", "CREDIT", "A", 10_000, 0.0, 5.0, end=5.0, entity="Firm C", basis="Firm C senior vs subordinated")
    total, detail = addon_credit_or_equity((a, b), margined=False, mpor_days=10)
    assert len(detail) == 2, detail
    single = addon_credit_or_equity((a,), margined=False, mpor_days=10)[0]
    # Each basis is alone in its hedging set, so no systematic offset between them and the add-ons simply add.
    assert _close(total, 2.0 * single, 1e-9)
    unscaled = Trade("B3", "CREDIT", "A", 10_000, 0.0, 5.0, end=5.0, entity="Firm C")
    assert _close(single, 0.5 * addon_credit_or_equity((unscaled,), margined=False, mpor_days=10)[0], 1e-9)
    # Two trades on the same basis share one hedging set and net.
    short = Trade("B4", "CREDIT", "A", 10_000, 0.0, 5.0, direction=-1, end=5.0, entity="Firm C", basis="Firm C bond vs CDS")
    same_total, same_detail = addon_credit_or_equity((a, short), margined=False, mpor_days=10)
    assert len(same_detail) == 1 and _close(same_total, 0.0, 1e-9)
    # The same rule for interest rates: two bases in one currency are two hedging sets.
    ir_a = Trade("I1", "IR", "", 10_000, 0.0, 5.0, end=5.0, hedging_set="USD", basis="3M Libor vs 6M Libor")
    ir_b = Trade("I2", "IR", "", 10_000, 0.0, 5.0, end=5.0, hedging_set="USD", basis="1M Libor vs OIS")
    assert len(addon_ir((ir_a, ir_b), margined=False, mpor_days=10)[1]) == 2
    print("  CRE52.46: two different credit bases give two hedging sets at half the factor; one basis nets in one set")


def run_tests() -> None:
    print("Basel credit risk and SA-CCR self-checks")

    # --- SA risk weights and CCFs -------------------------------------------------
    sov = [sa_sovereign_rw(r) for r in ("AA-", "A+", "BBB-", "BB+", "B-", "CCC", None)]
    assert sov == [0.0, 0.20, 0.50, 1.00, 1.00, 1.50, 1.00], sov
    assert [sa_bank_rw_ecra(r) for r in ("AA-", "A", "BBB", "BB", "B", "CCC")] == [0.20, 0.30, 0.50, 1.00, 1.00, 1.50]
    assert [sa_bank_rw_ecra(r, short_term=True) for r in ("AA-", "A", "BBB", "BB", "B", "CCC")] == [0.20, 0.20, 0.20, 0.50, 0.50, 1.50]
    assert sa_bank_rw_scra("A", cet1_ge_14_and_lev_ge_5=True) == 0.30 and sa_bank_rw_scra("B") == 0.75
    assert [sa_bank_rw_scra(g) for g in "ABC"] == [0.40, 0.75, 1.50]
    assert [sa_bank_rw_scra(g, short_term=True) for g in "ABC"] == [0.20, 0.50, 1.50]
    assert [sa_corporate_rw(r) for r in ("AA-", "A", "BBB", "BB-", "B+", "CCC", None)] == [0.20, 0.50, 0.75, 1.00, 1.50, 1.50, 1.00]
    assert sa_corporate_rw(None, sme=True) == 0.85
    assert [sa_retail_rw(k) for k in ("regulatory", "transactor", "other")] == [0.75, 0.45, 1.00]
    ltv = [sa_residential_re_rw(x) for x in (0.50, 0.55, 0.80, 0.85, 1.00, 1.10)]
    assert ltv == [0.20, 0.25, 0.30, 0.40, 0.50, 0.70], ltv
    # CRE20.83 footnote 120: EUR 70,000 loan on EUR 100,000 property, loan splitting -> RWA 22,250.
    assert _close(0.20 * 55_000 + 0.75 * (70_000 - 55_000), 22_250, 1e-9)

    # --- IRB -----------------------------------------------------------------------
    _check_cre99_table_1()
    # 1.25 multiplier for large financials (CRE31.7) at PD 1%.
    corp = irb_corporate(0.01, 0.40, 1.0)
    fi = irb_corporate(0.01, 0.45, 1.0, 2.5, large_or_unregulated_fi=True)
    assert _close(fi.correlation, 1.25 * corp.correlation, 1e-12)
    # PD floor (CRE32.4) binds for a corporate but not for a sovereign.
    assert irb_corporate(0.0001, 0.45, 1.0).pd == 0.0005 and irb_corporate(0.0001, 0.45, 1.0, sovereign=True).pd == 0.0001
    # At M = 1 the full maturity adjustment (1 + (M - 2.5) b) / (1 - 1.5 b) is exactly 1.
    k1 = irb_corporate(0.01, 0.40, 1.0, 1.0).k
    assert _close(k1, 0.40 * conditional_pd(0.01, corp.correlation) - 0.01 * 0.40, 1e-15)

    # --- SA-CCR: the CRE99 sample portfolios, structural checks ---------------------
    p = cre99_portfolios()
    r2 = saccr_ead(p["ex2"])
    cr = r2.detail["CREDIT"][("", False)]
    assert [round(cr["entities"][e]) for e in ("Firm A", "Firm B", "CDX.IG")] == [106, -280, 168]  # CRE99.52
    r3 = saccr_ead(p["ex3"])
    assert round(r3.detail["COMMODITY"][("ENERGY", "", False)]["types"]["Crude oil"]) == -2_041  # CRE99.70
    assert rc_shared_margin_agreement([30, -10], 15) == 15.0

    # --- Multiplier behaviour (CRE52.23) and MPOR floors (CRE52.50 to CRE52.51) -------
    assert pfe_multiplier(10, 0, 100) == 1.0
    assert _close(pfe_multiplier(-1e9, 0, 100), MULTIPLIER_FLOOR, 1e-12)
    assert mpor_floor_days() == 10 and mpor_floor_days(daily_margin=False, remargin_period_days=5) == 14
    assert mpor_floor_days(trades_in_netting_set=6000) == 20 and mpor_floor_days(disputes_exceeding_mpor_last_two_quarters=3) == 20
    _check_basis_hedging_sets()

    # --- Every number quoted in notes 03 and 04 --------------------------------------
    _check_credit_note()
    _check_saccr_note(p)
    print(f"  {len(QUOTED_LOG)} numbers quoted in notes 03 and 04 computed, printed and asserted")
    print("All Basel credit risk and SA-CCR checks passed.")


if __name__ == "__main__":
    run_tests()
