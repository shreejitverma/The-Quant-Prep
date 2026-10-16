"""FRTB standardised approach reference engine: sensitivities-based method, DRC and RRAO.

Every regulatory parameter below is quoted from the Basel Framework chapters MAR20 to MAR23
(version effective 1 January 2023, MAR21 incorporating the FAQs of 5 July 2024 and 23 March 2026),
read from the consolidated framework PDF on bis.org on 2026-10-16.
Paragraph references sit next to each constant so every number can be checked against the text.

Scope and simplifications (deliberate, for a teaching engine):
- Sensitivities are inputs: the engine starts from net sensitivities per regulatory risk factor (MAR21.4(2)),
  except in the worked examples, which build them from small pricing functions.
- DRC covers non-securitisations in full (MAR22.9 to MAR22.26). For the CTP only the cross-index aggregation
  of MAR22.45 is implemented (`drc_ctp_total`, from caller-supplied index-level charges); the securitisation
  non-CTP DRC and the CTP-wide HBR of MAR22.44(1) are not implemented, and their risk weights would come from
  the banking book securitisation framework (MAR22.34, MAR22.42).
- Where the text is silent (a radicand that stays negative after the MAR21.4(5)(b) alternative
  specification), the engine floors it at zero and sets `floored` for escalation; see `across_bucket_capital`.

Run: python 17-Regulatory-Capital-Basel-and-FRTB/code/frtb_sbm.py
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

SCENARIOS = ("medium", "high", "low")

# ---------------------------------------------------------------------------
# Correlation scenarios (MAR21.6)
# ---------------------------------------------------------------------------


def scenario_correlation(rho: float, scenario: str) -> float:
    """MAR21.6: medium as specified; high = min(1.25 rho, 1); low = max(2 rho - 1, 0.75 rho)."""
    if scenario == "medium":
        return rho
    if scenario == "high":
        return min(1.25 * rho, 1.0)
    if scenario == "low":
        return max(2.0 * rho - 1.0, 0.75 * rho)
    raise ValueError(f"unknown correlation scenario {scenario!r}")


# ---------------------------------------------------------------------------
# Generic delta / vega aggregation (MAR21.4)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WeightedSensitivity:
    """WS_k = RW_k * s_k for one regulatory risk factor (MAR21.4(3)); `key` identifies the factor inside its bucket."""

    bucket: str
    key: tuple
    ws: float


@dataclass
class BucketResult:
    bucket: str
    k_b: float  # K_b, MAR21.4(4)
    s_b: float  # S_b = sum of WS_k in the bucket, MAR21.4(5)(a)


def within_bucket_capital(
    ws: Sequence[WeightedSensitivity], rho: Callable[[tuple, tuple], float], scenario: str, abs_sum: bool = False
) -> BucketResult:
    """K_b = sqrt(max(0, sum_k WS_k^2 + sum_k sum_{l != k} rho_kl WS_k WS_l)) (MAR21.4(4)).

    `abs_sum` implements the "other sector" buckets, aggregated as the simple sum of absolute weighted
    sensitivities with no correlation and therefore no scenario dependence (MAR21.56(1), MAR21.69(1), MAR21.79(1)).
    """
    if not ws:
        raise ValueError("empty bucket")
    bucket = ws[0].bucket
    if any(w.bucket != bucket for w in ws):
        raise ValueError("mixed buckets")
    keys = [w.key for w in ws]
    if len(set(keys)) != len(keys):
        raise ValueError(f"bucket {bucket}: sensitivities to the same risk factor must be netted first (MAR21.4(2))")
    s_b = sum(w.ws for w in ws)
    if abs_sum:
        return BucketResult(bucket, sum(abs(w.ws) for w in ws), s_b)
    radicand = sum(w.ws**2 for w in ws)
    for i, wi in enumerate(ws):
        for j, wj in enumerate(ws):
            if i != j:
                radicand += scenario_correlation(rho(wi.key, wj.key), scenario) * wi.ws * wj.ws
    return BucketResult(bucket, math.sqrt(max(0.0, radicand)), s_b)


@dataclass
class AcrossResult:
    capital: float
    alternative_used: bool  # True when MAR21.4(5)(b) was triggered
    floored: bool = False  # True when the radicand stayed negative after MAR21.4(5)(b) and was floored at zero


def across_bucket_capital(buckets: Sequence[BucketResult], gamma: Callable[[str, str], float], scenario: str) -> AcrossResult:
    """Delta (or vega) risk-class capital = sqrt(sum_b K_b^2 + sum_b sum_{c != b} gamma_bc S_b S_c) (MAR21.4(5)(a)).

    If that sum is negative, MAR21.4(5)(b) replaces S_b by max(min(sum WS_k, K_b), -K_b).
    With |S_b| <= K_b the radicand is >= S'G S, so it cannot be negative when the scenario-adjusted
    gamma matrix G (unit diagonal) is positive semidefinite.
    The prescribed matrices are not always PSD (see `gamma_min_eigenvalues`): the CSR non-securitisation matrix
    fails in the medium and high scenarios and the equity matrix in the high scenario.
    The text is silent on a radicand that stays negative, so the engine floors it at zero and flags `floored`
    for escalation rather than inventing a rule.
    """

    def radicand(s: dict[str, float]) -> float:
        total = sum(b.k_b**2 for b in buckets)
        for b in buckets:
            for c in buckets:
                if b.bucket != c.bucket:
                    total += scenario_correlation(gamma(b.bucket, c.bucket), scenario) * s[b.bucket] * s[c.bucket]
        return total

    first = radicand({b.bucket: b.s_b for b in buckets})
    if first >= 0.0:
        return AcrossResult(math.sqrt(first), False)
    second = radicand({b.bucket: max(min(b.s_b, b.k_b), -b.k_b) for b in buckets})
    if second < 0.0:
        return AcrossResult(0.0, True, floored=True)
    return AcrossResult(math.sqrt(second), True)


@dataclass
class RiskClassSpec:
    """Plug-in rules for one risk class: intra-bucket rho, inter-bucket gamma, and which buckets are 'other sector'."""

    name: str
    rho: Callable[[str, tuple, tuple], float]  # (bucket, key_k, key_l) -> rho_kl
    gamma: Callable[[str, str], float]
    abs_sum_buckets: frozenset = field(default_factory=frozenset)
    standalone_buckets: frozenset = field(default_factory=frozenset)  # summed outside the sqrt (MAR21.71)


def risk_class_capital(spec: RiskClassSpec, ws: Sequence[WeightedSensitivity], scenario: str) -> AcrossResult:
    """Full delta (or vega) aggregation for one risk class under one correlation scenario."""
    by_bucket: dict[str, list[WeightedSensitivity]] = {}
    for w in ws:
        by_bucket.setdefault(w.bucket, []).append(w)
    correlated, standalone = [], 0.0
    for b, items in by_bucket.items():
        res = within_bucket_capital(items, lambda k, lk, b=b: spec.rho(b, k, lk), scenario, abs_sum=b in spec.abs_sum_buckets)
        if b in spec.standalone_buckets:
            standalone += res.k_b
        else:
            correlated.append(res)
    if not correlated:
        return AcrossResult(standalone, False)
    res = across_bucket_capital(correlated, spec.gamma, scenario)
    return AcrossResult(res.capital + standalone, res.alternative_used, res.floored)


# ---------------------------------------------------------------------------
# GIRR delta (MAR21.8, MAR21.19, MAR21.41 to MAR21.50)
# ---------------------------------------------------------------------------

GIRR_TENORS = (0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 15.0, 20.0, 30.0)  # MAR21.8(1)
GIRR_RW = dict(zip(GIRR_TENORS, (0.017, 0.017, 0.016, 0.013, 0.012, 0.011, 0.011, 0.011, 0.011, 0.011), strict=True))  # MAR21.42 Table 1
GIRR_RW_INFLATION_XCCY = 0.016  # MAR21.43
SPECIFIED_CURRENCIES = frozenset({"EUR", "USD", "GBP", "AUD", "JPY", "SEK", "CAD"})  # MAR21.44 fn 283, plus domestic currency
GIRR_THETA = 0.03  # MAR21.46 fn 284
GIRR_RHO_FLOOR = 0.40  # MAR21.46 fn 284
GIRR_RHO_DIFFERENT_CURVE = 0.999  # MAR21.45, MAR21.47
GIRR_RHO_INFLATION_RATE = 0.40  # MAR21.48
GIRR_RHO_XCCY = 0.0  # MAR21.49
GIRR_GAMMA = 0.50  # MAR21.50


def girr_tenor_correlation(t_k: float, t_l: float) -> float:
    """Same curve, different tenor: max(exp(-theta |T_k - T_l| / min(T_k, T_l)), 40%) (MAR21.46 fn 284)."""
    if t_k == t_l:
        return 1.0
    return max(math.exp(-GIRR_THETA * abs(t_k - t_l) / min(t_k, t_l)), GIRR_RHO_FLOOR)


def girr_risk_weight(currency: str, kind: str, tenor: float | None, domestic: str, sqrt2_discretion: bool) -> float:
    """Table 1 by tenor, 1.6% for inflation and cross-currency basis, optionally / sqrt(2) for specified currencies."""
    rw = GIRR_RW[tenor] if kind == "rate" else GIRR_RW_INFLATION_XCCY
    if sqrt2_discretion and (currency in SPECIFIED_CURRENCIES or currency == domestic):
        rw /= math.sqrt(2.0)  # MAR21.44
    return rw


def girr_rho(_bucket: str, k: tuple, l_: tuple) -> float:
    """GIRR keys are (kind, curve, tenor) with kind in {'rate', 'inflation', 'xccy'} (MAR21.45 to MAR21.49)."""
    kind_k, curve_k, t_k = k
    kind_l, curve_l, t_l = l_
    if "xccy" in (kind_k, kind_l):
        return GIRR_RHO_XCCY  # MAR21.49: 0% to rate tenors, inflation and other basis curves
    if kind_k == kind_l == "inflation":
        return GIRR_RHO_DIFFERENT_CURVE  # FAQ to MAR21.47: 99.9% between inflation curves of one currency
    if "inflation" in (kind_k, kind_l):
        return GIRR_RHO_INFLATION_RATE  # MAR21.48
    rho = girr_tenor_correlation(t_k, t_l)
    return rho if curve_k == curve_l else rho * GIRR_RHO_DIFFERENT_CURVE  # MAR21.46, MAR21.47 (99.9% if same tenor)


GIRR = RiskClassSpec("GIRR", girr_rho, lambda b, c: GIRR_GAMMA)

# ---------------------------------------------------------------------------
# CSR non-securitisation delta (MAR21.9, MAR21.20, MAR21.51 to MAR21.57)
# ---------------------------------------------------------------------------

CSR_NS_RW = {
    1: 0.005, 2: 0.010, 3: 0.050, 4: 0.030, 5: 0.030, 6: 0.020, 7: 0.015, 8: 0.025, 9: 0.020,
    10: 0.040, 11: 0.120, 12: 0.070, 13: 0.085, 14: 0.055, 15: 0.050, 16: 0.120, 17: 0.015, 18: 0.050,
}  # fmt: skip  # MAR21.53 Table 4 (covered bonds rated AA- or better may use 1.5%, fn 288)
CSR_NS_RHO_NAME = (0.35, 0.80)  # MAR21.54(1) buckets 1 to 15, MAR21.55(1) buckets 17 and 18
CSR_RHO_TENOR = 0.65  # MAR21.54(2), MAR21.55(2)
CSR_RHO_BASIS = 0.999  # MAR21.54(3): bond versus CDS curve of the same name
CSR_GAMMA_RATING = 0.50  # MAR21.57(1)

# MAR21.57 Table 5: gamma_sector between sector groups; buckets 1/9, 2/10, ..., 7/15 share a sector.
_SECTOR_OF = {**{b: b for b in range(1, 9)}, **{b: b - 8 for b in range(9, 16)}, 16: 16, 17: 17, 18: 18}
_TABLE5_ROWS = {
    1: (0.75, 0.10, 0.20, 0.25, 0.20, 0.15, 0.10, 0.0, 0.45, 0.45),
    2: (0.05, 0.15, 0.20, 0.15, 0.10, 0.10, 0.0, 0.45, 0.45),
    3: (0.05, 0.15, 0.20, 0.05, 0.20, 0.0, 0.45, 0.45),
    4: (0.20, 0.25, 0.05, 0.05, 0.0, 0.45, 0.45),
    5: (0.25, 0.05, 0.15, 0.0, 0.45, 0.45),
    6: (0.05, 0.20, 0.0, 0.45, 0.45),
    7: (0.05, 0.0, 0.45, 0.45),
    8: (0.0, 0.45, 0.45),
    16: (0.0, 0.0),
    17: (0.75,),
}
_SECTOR_ORDER = (1, 2, 3, 4, 5, 6, 7, 8, 16, 17, 18)
CSR_GAMMA_SECTOR: dict[tuple[int, int], float] = {}
for _row, _vals in _TABLE5_ROWS.items():
    _cols = _SECTOR_ORDER[_SECTOR_ORDER.index(_row) + 1 :]
    for _col, _v in zip(_cols, _vals, strict=True):
        CSR_GAMMA_SECTOR[(_row, _col)] = CSR_GAMMA_SECTOR[(_col, _row)] = _v


def csr_ns_rho(bucket: str, k: tuple, l_: tuple) -> float:
    """Keys are (name, tenor, curve) with curve in {'bond', 'cds'}; rho = rho_name * rho_tenor * rho_basis."""
    name_corr = CSR_NS_RHO_NAME[1] if int(bucket) in (17, 18) else CSR_NS_RHO_NAME[0]
    r_name = 1.0 if k[0] == l_[0] else name_corr
    r_tenor = 1.0 if k[1] == l_[1] else CSR_RHO_TENOR
    r_basis = 1.0 if k[2] == l_[2] else CSR_RHO_BASIS
    return r_name * r_tenor * r_basis


def csr_ns_gamma(b: str, c: str) -> float:
    """gamma_bc = gamma_rating * gamma_sector (MAR21.57)."""
    bi, ci = int(b), int(c)
    both_rated = bi <= 15 and ci <= 15
    different_rating = both_rated and ((bi <= 8) != (ci <= 8))
    g_rating = CSR_GAMMA_RATING if different_rating else 1.0
    sb, sc = _SECTOR_OF[bi], _SECTOR_OF[ci]
    g_sector = 1.0 if sb == sc else CSR_GAMMA_SECTOR[(sb, sc)]
    return g_rating * g_sector


CSR_NS = RiskClassSpec("CSR non-securitisation", csr_ns_rho, csr_ns_gamma, abs_sum_buckets=frozenset({"16"}))

# CSR securitisation CTP (MAR21.58 to MAR21.61): CSR non-sec structure without buckets 17 and 18.
CSR_CTP_RW = {
    1: 0.04, 2: 0.04, 3: 0.08, 4: 0.05, 5: 0.04, 6: 0.03, 7: 0.02, 8: 0.06,
    9: 0.13, 10: 0.13, 11: 0.16, 12: 0.10, 13: 0.12, 14: 0.12, 15: 0.12, 16: 0.13,
}  # fmt: skip  # MAR21.59 Table 6
CSR_CTP_RHO_BASIS = 0.99  # MAR21.60(1)


def csr_ctp_rho(bucket: str, k: tuple, l_: tuple) -> float:
    r_name = 1.0 if k[0] == l_[0] else CSR_NS_RHO_NAME[0]
    r_tenor = 1.0 if k[1] == l_[1] else CSR_RHO_TENOR
    r_basis = 1.0 if k[2] == l_[2] else CSR_CTP_RHO_BASIS
    return r_name * r_tenor * r_basis


CSR_CTP = RiskClassSpec("CSR securitisation CTP", csr_ctp_rho, csr_ns_gamma, abs_sum_buckets=frozenset({"16"}))

# CSR securitisation non-CTP (MAR21.62 to MAR21.71)
_NONCTP_SENIOR_IG = (0.009, 0.015, 0.020, 0.020, 0.008, 0.012, 0.012, 0.014)  # MAR21.64 Table 8, buckets 1 to 8
CSR_NONCTP_RW = {
    **{b + 1: rw for b, rw in enumerate(_NONCTP_SENIOR_IG)},
    **{b + 9: 1.25 * rw for b, rw in enumerate(_NONCTP_SENIOR_IG)},  # MAR21.65
    **{b + 17: 1.75 * rw for b, rw in enumerate(_NONCTP_SENIOR_IG)},  # MAR21.66
    25: 0.035,  # MAR21.67
}


def csr_nonctp_rho(_bucket: str, k: tuple, l_: tuple) -> float:
    """Keys are (tranche, tenor, curve): rho_tranche 40%, rho_tenor 80%, rho_basis 99.9% (MAR21.68)."""
    r_tranche = 1.0 if k[0] == l_[0] else 0.40
    r_tenor = 1.0 if k[1] == l_[1] else 0.80
    r_basis = 1.0 if k[2] == l_[2] else 0.999
    return r_tranche * r_tenor * r_basis


CSR_NONCTP = RiskClassSpec(
    "CSR securitisation non-CTP",
    csr_nonctp_rho,
    lambda b, c: 0.0,  # MAR21.70
    abs_sum_buckets=frozenset({"25"}),  # MAR21.69(1)
    standalone_buckets=frozenset({"25"}),  # MAR21.71
)

# ---------------------------------------------------------------------------
# Equity delta (MAR21.12, MAR21.21, MAR21.22, MAR21.72 to MAR21.80)
# ---------------------------------------------------------------------------

EQ_RW_SPOT = {1: 0.55, 2: 0.60, 3: 0.45, 4: 0.55, 5: 0.30, 6: 0.35, 7: 0.40, 8: 0.50, 9: 0.70, 10: 0.50, 11: 0.70, 12: 0.15, 13: 0.25}
EQ_RW_REPO = {b: rw / 100.0 for b, rw in EQ_RW_SPOT.items()}  # MAR21.77 Table 10: 0.55% ... 0.25%


def _eq_name_correlation(bucket: int) -> float:
    """MAR21.78(2): 15% large EM (1-4), 25% large AE (5-8), 7.5% small EM (9), 12.5% small AE (10), 80% index (12, 13)."""
    if bucket <= 4:
        return 0.15
    if bucket <= 8:
        return 0.25
    if bucket == 9:
        return 0.075
    if bucket == 10:
        return 0.125
    if bucket in (12, 13):
        return 0.80
    raise ValueError("bucket 11 is aggregated by simple sum (MAR21.79)")


def equity_rho(bucket: str, k: tuple, l_: tuple) -> float:
    """Keys are (issuer, 'spot' | 'repo') (MAR21.78)."""
    same_issuer = k[0] == l_[0]
    same_type = k[1] == l_[1]
    if same_issuer:
        return 0.999  # MAR21.78(1): spot versus repo of the same issuer
    base = _eq_name_correlation(int(bucket))
    return base if same_type else base * 0.999  # MAR21.78(2) to (4)


def equity_gamma(b: str, c: str) -> float:
    """MAR21.80: 15% within 1-10, 0% with bucket 11, 75% between 12 and 13, 45% otherwise."""
    bi, ci = int(b), int(c)
    if 11 in (bi, ci):
        return 0.0
    if bi <= 10 and ci <= 10:
        return 0.15
    if {bi, ci} == {12, 13}:
        return 0.75
    return 0.45


EQUITY = RiskClassSpec("Equity", equity_rho, equity_gamma, abs_sum_buckets=frozenset({"11"}))

# ---------------------------------------------------------------------------
# Commodity delta (MAR21.13, MAR21.23, MAR21.81 to MAR21.85)
# ---------------------------------------------------------------------------

CTY_RW = {1: 0.30, 2: 0.35, 3: 0.60, 4: 0.80, 5: 0.40, 6: 0.45, 7: 0.20, 8: 0.35, 9: 0.25, 10: 0.35, 11: 0.50}  # MAR21.82 Table 11
CTY_RHO = {1: 0.55, 2: 0.95, 3: 0.40, 4: 0.80, 5: 0.60, 6: 0.65, 7: 0.55, 8: 0.45, 9: 0.15, 10: 0.40, 11: 0.15}  # MAR21.83 Table 12


def commodity_rho(bucket: str, k: tuple, l_: tuple) -> float:
    """Keys are (commodity, tenor, location): rho_cty * rho_tenor (99%) * rho_basis (99.9%) (MAR21.83)."""
    r_cty = 1.0 if k[0] == l_[0] else CTY_RHO[int(bucket)]
    r_tenor = 1.0 if k[1] == l_[1] else 0.99
    r_basis = 1.0 if k[2] == l_[2] else 0.999
    return r_cty * r_tenor * r_basis


COMMODITY = RiskClassSpec("Commodity", commodity_rho, lambda b, c: 0.0 if "11" in (b, c) else 0.20)  # MAR21.85

# ---------------------------------------------------------------------------
# FX delta (MAR21.14, MAR21.24, MAR21.86 to MAR21.89)
# ---------------------------------------------------------------------------

FX_RW = 0.15  # MAR21.87
FX_GAMMA = 0.60  # MAR21.89
SPECIFIED_FX_PAIRS = frozenset(
    f"USD/{c}"
    for c in (
        "EUR",
        "JPY",
        "GBP",
        "AUD",
        "CAD",
        "CHF",
        "MXN",
        "CNY",
        "NZD",
        "RUB",
        "HKD",
        "SGD",
        "TRY",
        "KRW",
        "SEK",
        "ZAR",
        "INR",
        "NOK",
        "BRL",
    )
)  # MAR21.88 fn 293; first-order crosses also qualify (fn 294)
FX = RiskClassSpec("FX", lambda b, k, l_: 1.0, lambda b, c: FX_GAMMA)

# ---------------------------------------------------------------------------
# Vega (MAR21.25, MAR21.90 to MAR21.95)
# ---------------------------------------------------------------------------

VEGA_RW_SIGMA = 0.55  # MAR21.92 fn 295
VEGA_LIQUIDITY_HORIZON = {
    "GIRR": 60,
    "CSR non-securitisation": 120,
    "CSR securitisation CTP": 120,
    "CSR securitisation non-CTP": 120,
    "Equity large cap and indices": 20,
    "Equity small cap and other sector": 60,
    "Commodity": 120,
    "FX": 40,
}  # MAR21.92 Table 13
VEGA_ALPHA = 0.01  # MAR21.93


def vega_risk_weight(risk_class: str) -> float:
    """RW_k = min(RW_sigma * sqrt(LH / 10), 100%) (MAR21.92 fn 295)."""
    return min(VEGA_RW_SIGMA * math.sqrt(VEGA_LIQUIDITY_HORIZON[risk_class] / 10.0), 1.0)


def vega_maturity_correlation(t_k: float, t_l: float) -> float:
    """exp(-alpha |T_k - T_l| / min(T_k, T_l)) with alpha = 1% (MAR21.93)."""
    return math.exp(-VEGA_ALPHA * abs(t_k - t_l) / min(t_k, t_l))


def girr_vega_rho(_bucket: str, k: tuple, l_: tuple) -> float:
    """Keys are (option maturity, underlying residual maturity): min(rho_option * rho_underlying, 1) (MAR21.93)."""
    return min(vega_maturity_correlation(k[0], l_[0]) * vega_maturity_correlation(k[1], l_[1]), 1.0)


def non_girr_vega_rho(delta_rho: Callable[[str, tuple, tuple], float]) -> Callable[[str, tuple, tuple], float]:
    """Keys are (option maturity, *delta key): min(rho_delta * rho_option_maturity, 1) (MAR21.94).

    The delta key must contain only the dimensions that vega and delta factors share (FAQ to MAR21.94): the
    issuer and spot/repo type for equity, the name for CSR, the tranche for securitisations and the commodity
    for commodities. Passing a full CSR or commodity delta key would wrongly apply tenor and basis factors.
    """

    def rho(bucket: str, k: tuple, l_: tuple) -> float:
        d = 1.0 if k[1:] == l_[1:] else delta_rho(bucket, k[1:], l_[1:])
        return min(d * vega_maturity_correlation(k[0], l_[0]), 1.0)

    return rho


GIRR_VEGA = RiskClassSpec("GIRR vega", girr_vega_rho, lambda b, c: GIRR_GAMMA)  # MAR21.95
EQUITY_VEGA = RiskClassSpec("Equity vega", non_girr_vega_rho(equity_rho), equity_gamma, abs_sum_buckets=frozenset({"11"}))

# ---------------------------------------------------------------------------
# Curvature (MAR21.5, MAR21.96 to MAR21.101)
# ---------------------------------------------------------------------------


def cvr(v_base: float, v_up: float, v_down: float, rw_curv: float, delta_s: float) -> tuple[float, float]:
    """MAR21.5(2): CVR+ = -(V(x up) - V(x) - RW * s), CVR- = -(V(x down) - V(x) + RW * s).

    For equity and FX `rw_curv` is the relative delta risk weight and `delta_s` the MAR21.21/MAR21.24 sensitivity;
    for GIRR, CSR and commodity `rw_curv` is the largest delta risk weight of the bucket and `delta_s` the sum of the
    delta sensitivities to all tenors of the curve (MAR21.5(2)(f), MAR21.99).
    """
    return -(v_up - v_base - rw_curv * delta_s), -(v_down - v_base + rw_curv * delta_s)


def _psi(a: float, b: float) -> float:
    """psi = 0 if both arguments are negative, 1 otherwise (MAR21.5(3)(b), MAR21.5(4)(b))."""
    return 0.0 if (a < 0.0 and b < 0.0) else 1.0


@dataclass
class CurvatureBucket:
    bucket: str
    k_b: float
    s_b: float
    upward_selected: bool
    k_up: float = 0.0
    k_down: float = 0.0


def curvature_bucket(
    cvr_up: dict[tuple, float], cvr_down: dict[tuple, float], delta_rho: Callable[[tuple, tuple], float], scenario: str, other: bool = False
) -> CurvatureBucket:
    """K_b = max(K_b+, K_b-) with K_b+- = sqrt(max(0, sum max(CVR,0)^2 + sum rho^2 CVR_k CVR_l psi)) (MAR21.5(3), MAR21.100).

    The scenario adjustment is applied to the squared delta correlation (MAR21.100).
    `other` gives the other-sector formula max(sum max(CVR+,0), sum max(CVR-,0)) (MAR21.56(2), MAR21.79(2)).
    """
    keys = list(cvr_up)

    def k_dir(c: dict[tuple, float]) -> float:
        if other:
            return sum(max(c[k], 0.0) for k in keys)
        total = sum(max(c[k], 0.0) ** 2 for k in keys)
        for k in keys:
            for kk in keys:
                if k != kk:
                    total += scenario_correlation(delta_rho(k, kk) ** 2, scenario) * c[k] * c[kk] * _psi(c[k], c[kk])
        return math.sqrt(max(0.0, total))

    k_up, k_down = k_dir(cvr_up), k_dir(cvr_down)
    sum_up, sum_down = sum(cvr_up.values()), sum(cvr_down.values())
    if k_up > k_down:
        up = True
    elif k_down > k_up:
        up = False
    else:
        up = sum_up > sum_down  # MAR21.5(3)(a)(iii)
    return CurvatureBucket("", max(k_up, k_down), sum_up if up else sum_down, up, k_up, k_down)


def curvature_across(buckets: Sequence[CurvatureBucket], delta_gamma: Callable[[str, str], float], scenario: str) -> float:
    """sqrt(max(0, sum K_b^2 + sum gamma_bc^2 S_b S_c psi(S_b, S_c))) (MAR21.5(4), MAR21.101)."""
    total = sum(b.k_b**2 for b in buckets)
    for b in buckets:
        for c in buckets:
            if b.bucket != c.bucket:
                g = scenario_correlation(delta_gamma(b.bucket, c.bucket) ** 2, scenario)
                total += g * b.s_b * c.s_b * _psi(b.s_b, c.s_b)
    return math.sqrt(max(0.0, total))


# ---------------------------------------------------------------------------
# Default risk capital (MAR22)
# ---------------------------------------------------------------------------

DRC_RW = {
    "AAA": 0.005,
    "AA": 0.02,
    "A": 0.03,
    "BBB": 0.06,
    "BB": 0.15,
    "B": 0.30,
    "CCC": 0.50,
    "Unrated": 0.15,
    "Defaulted": 1.0,
}  # MAR22.24
DRC_LGD = {"equity": 1.0, "non-senior": 1.0, "senior": 0.75, "covered": 0.25}  # MAR22.12
SENIORITY_RANK = {"covered": 0, "senior": 1, "non-senior": 2, "equity": 3}  # higher rank = more junior


@dataclass(frozen=True)
class DRCPosition:
    """Notional is signed (+ long credit, - short credit) and P&L = market value - notional (MAR22.11, MAR22.13).

    Direction is a loss-on-default property (MAR22.10); it defaults to the sign of the notional but must be given
    explicitly when the notional is zero, for example a bought call on a bond (MAR22.14(1)(c)), whose JTD is its
    mark-to-market value captured through the P&L term.
    """

    obligor: str
    bucket: str  # corporates | sovereigns | local governments (MAR22.22)
    seniority: str
    rating: str
    notional: float
    market_value: float
    maturity_years: float
    lgd_applies: bool = True  # MAR22.12(4)
    long_credit: bool | None = None  # MAR22.10; None means sign of notional

    def __post_init__(self) -> None:
        if self.notional == 0 and self.long_credit is None:
            raise ValueError("zero-notional position needs an explicit long_credit direction (MAR22.10)")
        if self.seniority == "equity" and not (self.maturity_years == 0.25 or self.maturity_years > 1.0):
            raise ValueError("cash equity takes a maturity of three months or more than one year (MAR22.16)")

    @property
    def is_long(self) -> bool:
        return self.notional > 0 if self.long_credit is None else self.long_credit

    @property
    def gross_jtd(self) -> float:
        """JTD long = max(LGD * notional + P&L, 0); JTD short = min(LGD * notional + P&L, 0) (MAR22.11 to MAR22.14)."""
        lgd = DRC_LGD[self.seniority] if self.lgd_applies else 1.0
        raw = lgd * self.notional + (self.market_value - self.notional)
        return max(raw, 0.0) if self.is_long else min(raw, 0.0)

    @property
    def maturity_weight(self) -> float:
        """Scale by maturity fraction of the one-year horizon, floored at three months (MAR22.15, MAR22.18)."""
        return min(max(self.maturity_years, 0.25), 1.0)


def net_jtd(positions: Sequence[DRCPosition]) -> list[tuple[str, str, float, float]]:
    """Offset longs and shorts of one obligor where the short is the same or lower seniority (MAR22.19).

    Returns residual pieces (bucket, obligor, scaled net JTD, risk weight).
    Shorts are processed from most senior to most junior: every long a senior short may offset is also eligible
    for any more junior short, so this greedy order maximises the permitted offset.
    """
    out: list[tuple[str, str, float, float]] = []
    obligors = {(p.bucket, p.obligor) for p in positions}
    for bucket, obligor in sorted(obligors):
        mine = [p for p in positions if (p.bucket, p.obligor) == (bucket, obligor)]
        longs = [[p, p.gross_jtd * p.maturity_weight] for p in mine if p.is_long]
        shorts = sorted(([p, p.gross_jtd * p.maturity_weight] for p in mine if not p.is_long), key=lambda x: SENIORITY_RANK[x[0].seniority])
        for short in shorts:
            for long in sorted(longs, key=lambda x: -SENIORITY_RANK[x[0].seniority]):
                if SENIORITY_RANK[short[0].seniority] >= SENIORITY_RANK[long[0].seniority] and long[1] > 0 and short[1] < 0:
                    used = min(long[1], -short[1])
                    long[1] -= used
                    short[1] += used
        for p, amt in longs + shorts:
            if abs(amt) > 1e-9:
                out.append((bucket, obligor, amt, DRC_RW[p.rating]))
    return out


def drc_non_securitisation(positions: Sequence[DRCPosition]) -> dict[str, float]:
    """Per bucket: max(sum RW * net long - HBR * sum RW * |net short|, 0); HBR from unweighted amounts (MAR22.23, MAR22.25)."""
    pieces = net_jtd(positions)
    result: dict[str, float] = {}
    for bucket in sorted({p[0] for p in pieces}):
        mine = [p for p in pieces if p[0] == bucket]
        long_sum = sum(p[2] for p in mine if p[2] > 0)
        short_sum = sum(-p[2] for p in mine if p[2] < 0)
        hbr = long_sum / (long_sum + short_sum) if long_sum + short_sum > 0 else 0.0
        weighted_long = sum(p[3] * p[2] for p in mine if p[2] > 0)
        weighted_short = sum(p[3] * -p[2] for p in mine if p[2] < 0)
        result[bucket] = max(weighted_long - hbr * weighted_short, 0.0)
    return result  # summed across buckets with no hedging (MAR22.26)


def drc_ctp_total(index_level_drc: Sequence[float]) -> float:
    """DRC_CTP = max(sum_b [max(DRC_b, 0) + 0.5 * min(DRC_b, 0)], 0); bucket DRC may be negative (MAR22.44, MAR22.45)."""
    return max(sum(max(d, 0.0) + 0.5 * min(d, 0.0) for d in index_level_drc), 0.0)


# ---------------------------------------------------------------------------
# Residual risk add-on (MAR23)
# ---------------------------------------------------------------------------

RRAO_RW = {"exotic": 0.01, "other": 0.001}  # MAR23.8(2)


def rrao(gross_notionals: Sequence[tuple[str, float]]) -> float:
    """Simple sum of gross notional times 1.0% (exotic underlying) or 0.1% (other residual risk) (MAR23.8)."""
    return sum(RRAO_RW[kind] * abs(notional) for kind, notional in gross_notionals)


# ---------------------------------------------------------------------------
# Small pricing helpers used only by the worked examples
# ---------------------------------------------------------------------------


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call(spot: float, strike: float, vol: float, t: float) -> float:
    """Black-Scholes call, zero rates and dividends."""
    d1 = (math.log(spot / strike) + 0.5 * vol * vol * t) / (vol * math.sqrt(t))
    return spot * norm_cdf(d1) - strike * norm_cdf(d1 - vol * math.sqrt(t))


def bs_put(spot: float, strike: float, vol: float, t: float) -> float:
    return bs_call(spot, strike, vol, t) - spot + strike


def bs_vega(spot: float, strike: float, vol: float, t: float) -> float:
    d1 = (math.log(spot / strike) + 0.5 * vol * vol * t) / (vol * math.sqrt(t))
    return spot * math.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi) * math.sqrt(t)


# ---------------------------------------------------------------------------
# Worked examples (numbers quoted in the notes come from this output)
# ---------------------------------------------------------------------------


def fmt(x: float) -> str:
    return f"{x:,.0f}"


def close(a: float, b: float, tol: float = 1e-6) -> bool:
    return math.isclose(a, b, rel_tol=tol, abs_tol=1e-6)


def example_girr_flattener() -> dict[str, float]:
    """USD curve trade: 2y receiver (PV01 -100,000 per bp) against 10y payer (PV01 +80,000 per bp)."""
    print("\n[1] GIRR delta: USD 2y/10y curve trade, one bucket")
    pv01 = {2.0: -100_000.0, 10.0: 80_000.0}
    ws = []
    for tenor, d in pv01.items():
        s = d / 0.0001  # MAR21.19: change in value for +1bp divided by 0.0001
        rw = girr_risk_weight("USD", "rate", tenor, domestic="USD", sqrt2_discretion=False)
        ws.append(WeightedSensitivity("USD", ("rate", "SOFR", tenor), rw * s))
        print(f"  tenor {tenor:>4}y  PV01 {fmt(d):>9}  s_k {fmt(s):>16}  RW {rw:.2%}  WS {fmt(rw * s):>12}")
    rho = girr_tenor_correlation(2.0, 10.0)
    print(f"  rho(2y,10y) = exp(-0.03*8/2) = {rho:.6f}")
    out = {}
    for sc in SCENARIOS:
        k = risk_class_capital(GIRR, ws, sc).capital
        out[sc] = k
        print(f"  {sc:<6} rho={scenario_correlation(rho, sc):.6f}  K = {fmt(k)}")
    assert close(ws[0].ws, -13_000_000.0) and close(ws[1].ws, 8_800_000.0)
    hand = math.sqrt(13e6**2 + 8.8e6**2 - 2 * rho * 13e6 * 8.8e6)
    assert close(out["medium"], hand)
    assert out["low"] > out["medium"] > out["high"]
    sqrt2 = [WeightedSensitivity(w.bucket, w.key, w.ws / math.sqrt(2.0)) for w in ws]
    best = max(risk_class_capital(GIRR, sqrt2, sc).capital for sc in SCENARIOS)
    out["sqrt2"] = best
    print(f"  binding scenario: low, capital {fmt(out['low'])}; with the MAR21.44 sqrt(2) discretion: {fmt(best)}")
    assert close(best, out["low"] / math.sqrt(2.0))
    return out


def example_girr_multi_currency() -> dict[str, float]:
    """USD trade from example 1 plus a EUR book with a second curve, an inflation and a cross-currency basis exposure."""
    print("\n[2] GIRR delta: USD and EUR buckets with ESTR/EURIBOR curves, inflation and cross-currency basis")
    raw = [
        ("USD", ("rate", "SOFR", 2.0), -100_000.0),
        ("USD", ("rate", "SOFR", 10.0), 80_000.0),
        ("EUR", ("rate", "ESTR", 5.0), 60_000.0),
        ("EUR", ("rate", "EURIBOR6M", 5.0), -55_000.0),
        ("EUR", ("rate", "EURIBOR6M", 10.0), 30_000.0),
        ("EUR", ("inflation", "HICPx", None), 20_000.0),
        ("EUR", ("xccy", "EUR/USD", None), -25_000.0),
    ]
    ws = []
    for bucket, key, pv01 in raw:
        rw = girr_risk_weight(bucket, key[0], key[2], domestic="USD", sqrt2_discretion=False)
        ws.append(WeightedSensitivity(bucket, key, rw * pv01 / 0.0001))
        print(f"  {bucket} {key[0]:<9} {key[1]:<10} {key[2]!s:>5}  PV01 {fmt(pv01):>9}  RW {rw:.2%}  WS {fmt(rw * pv01 / 0.0001):>12}")
    out = {}
    for sc in SCENARIOS:
        per = {
            b: within_bucket_capital([w for w in ws if w.bucket == b], lambda k, kk, b=b: girr_rho(b, k, kk), sc) for b in ("USD", "EUR")
        }
        total = risk_class_capital(GIRR, ws, sc)
        out[sc] = total.capital
        line = "  ".join(f"K_{b}={fmt(r.k_b)} S_{b}={fmt(r.s_b)}" for b, r in per.items())
        print(f"  {sc:<6} {line}  GIRR delta = {fmt(total.capital)}")
    eur_same_tenor = girr_rho("EUR", ("rate", "ESTR", 5.0), ("rate", "EURIBOR6M", 5.0))
    assert close(eur_same_tenor, 0.999)
    assert close(girr_rho("EUR", ("rate", "ESTR", 5.0), ("rate", "EURIBOR6M", 10.0)), math.exp(-0.03) * 0.999)
    assert girr_rho("EUR", ("xccy", "EUR/USD", None), ("rate", "ESTR", 5.0)) == 0.0
    return out


def example_csr_alternative_spec() -> dict[str, float]:
    """IG financials sold protection against HY financials bought protection: triggers MAR21.4(5)(b)."""
    print("\n[3] CSR non-securitisation delta: long IG financials (bucket 3) versus short HY financials (bucket 11)")
    ws = []
    for i in range(10):
        s = 6_000.0 / 0.0001  # protection sold: CS01 -6,000 per bp per name, WS = 5% x s
        ws.append(WeightedSensitivity("3", (f"IGBANK{i}", 5.0, "cds"), CSR_NS_RW[3] * -s))
    for i in range(10):
        s = 2_500.0 / 0.0001  # protection bought: CS01 +2,500 per bp per name, WS = 12% x s
        ws.append(WeightedSensitivity("11", (f"HYBANK{i}", 5.0, "cds"), CSR_NS_RW[11] * s))
    print(f"  bucket 3: 10 names, WS each {fmt(ws[0].ws)}; bucket 11: 10 names, WS each {fmt(ws[10].ws)}")
    print(f"  gamma(3,11) = gamma_rating 50% x gamma_sector 1 = {csr_ns_gamma('3', '11'):.2f}")
    out = {}
    for sc in SCENARIOS:
        res = risk_class_capital(CSR_NS, ws, sc)
        b3 = within_bucket_capital(ws[:10], lambda k, kk: csr_ns_rho("3", k, kk), sc)
        out[sc] = res.capital
        print(f"  {sc:<6} K_3={fmt(b3.k_b)} S_3={fmt(b3.s_b)}  capital {fmt(res.capital)}  alternative spec used: {res.alternative_used}")
    w = 3_000_000.0
    k_b = w * math.sqrt(10 + 90 * 0.35)
    assert close(abs(ws[0].ws), w) and close(abs(ws[10].ws), w)
    first = 2 * k_b**2 - 2 * 0.5 * (10 * w) ** 2
    assert first < 0
    assert close(out["medium"], math.sqrt(2 * k_b**2 - 2 * 0.5 * k_b**2), 1e-6)
    return out


def example_equity_vega_and_curvature() -> dict[str, float]:
    """Two single-stock options in equity bucket 8 (large cap, advanced economy, technology): delta, vega and curvature."""
    print("\n[4] Equity: short 1y ATM call on TECHA, long 6m 90-strike put on TECHB (bucket 8, RW 50%)")
    spot, vol = 100.0, 0.25
    book = {
        "TECHA": dict(kind="call", strike=100.0, t=1.0, qty=-100_000.0),
        "TECHB": dict(kind="put", strike=90.0, t=0.5, qty=50_000.0),
    }
    rw = EQ_RW_SPOT[8]

    def value(name: str, s: float, v: float = vol) -> float:
        o = book[name]
        f = bs_call if o["kind"] == "call" else bs_put
        return o["qty"] * f(s, o["strike"], v, o["t"])

    delta_ws, vega_ws, up, down = [], [], {}, {}
    for name, o in book.items():
        v0 = value(name, spot)
        s_delta = (value(name, spot * 1.01) - v0) / 0.01  # MAR21.21
        vega_s = o["qty"] * bs_vega(spot, o["strike"], vol, o["t"]) * vol  # MAR21.25: vega times implied vol
        delta_ws.append(WeightedSensitivity("8", (name, "spot"), rw * s_delta))
        vega_ws.append(WeightedSensitivity("8", (o["t"], name, "spot"), vega_risk_weight("Equity large cap and indices") * vega_s))
        up[(name, "spot")], down[(name, "spot")] = cvr(v0, value(name, spot * (1 + rw)), value(name, spot * (1 - rw)), rw, s_delta)
        print(
            f"  {name}: V0 {fmt(v0)}  delta s {fmt(s_delta)}  WS {fmt(rw * s_delta)}  vega s {fmt(vega_s)}"
            f"  CVR+ {fmt(up[(name, 'spot')])}  CVR- {fmt(down[(name, 'spot')])}"
        )
    print(f"  vega RW = min(55% * sqrt(20/10), 1) = {vega_risk_weight('Equity large cap and indices'):.4%}")
    out = {}
    for sc in SCENARIOS:
        d = risk_class_capital(EQUITY, delta_ws, sc).capital
        v = risk_class_capital(EQUITY_VEGA, vega_ws, sc).capital
        cb = curvature_bucket(up, down, lambda k, kk: equity_rho("8", k, kk), sc)
        cb.bucket = "8"
        c = curvature_across([cb], equity_gamma, sc)
        out[f"{sc}_delta"], out[f"{sc}_vega"], out[f"{sc}_curv"] = d, v, c
        side = "up" if cb.upward_selected else "down"
        print(f"  {sc:<6} delta {fmt(d)}  vega {fmt(v)}  curvature {fmt(c)} (K+ {fmt(cb.k_up)}, K- {fmt(cb.k_down)}, {side} selected)")
    assert close(vega_risk_weight("Equity large cap and indices"), 0.55 * math.sqrt(2.0))
    assert vega_risk_weight("FX") == 1.0 and vega_risk_weight("GIRR") == 1.0
    assert close(non_girr_vega_rho(equity_rho)("8", (1.0, "TECHA", "spot"), (0.5, "TECHB", "spot")), 0.25 * math.exp(-0.01))
    return out


def example_girr_curvature() -> dict[str, float]:
    """Zero-coupon bond 10y, continuous rate 4%: convexity of a long versus a short under the 1.7% parallel shift."""
    print("\n[5] GIRR curvature: 10y zero-coupon bond, notional 100m, flat 4% continuous rate, shift = 1.7% (MAR21.99)")
    rw = max(GIRR_RW.values())
    out = {}
    for label, qty in (("long", 100_000_000.0), ("short", -100_000_000.0)):

        def v(r: float, q: float = qty) -> float:
            return q * math.exp(-r * 10.0)

        s = (v(0.0401) - v(0.04)) / 0.0001
        c_up, c_down = cvr(v(0.04), v(0.04 + rw), v(0.04 - rw), rw, s)
        out[label] = max(c_up, c_down)
        print(f"  {label:<5}: PV {fmt(v(0.04))}  s {fmt(s)}  CVR+ {fmt(c_up)}  CVR- {fmt(c_down)}")
    assert out["long"] < 0 < out["short"]
    return out


def example_drc() -> dict[str, float]:
    print("\n[6] DRC non-securitisation: seniority offsetting, maturity scaling and the hedge benefit ratio")
    book = [
        DRCPosition("ALPHA", "corporates", "senior", "BBB", 10_000_000.0, 9_500_000.0, 5.0),
        DRCPosition("ALPHA", "corporates", "equity", "BBB", -4_000_000.0, -4_000_000.0, 5.0),
        DRCPosition("ALPHA", "corporates", "senior", "BBB", -2_000_000.0, -2_000_000.0, 0.5),
        DRCPosition("BETA", "corporates", "non-senior", "BB", 6_000_000.0, 5_400_000.0, 3.0),
        DRCPosition("BETA", "corporates", "senior", "BB", -5_000_000.0, -5_000_000.0, 3.0),
        DRCPosition("GAMMA", "corporates", "senior", "A", -8_000_000.0, -8_000_000.0, 4.0),
        DRCPosition("SOVX", "sovereigns", "senior", "AA", 20_000_000.0, 20_000_000.0, 0.1),
    ]
    for p in book:
        print(f"  {p.obligor:<5} {p.seniority:<10} {p.rating:<3} notional {fmt(p.notional):>12} MV {fmt(p.market_value):>12}"
              f" M {p.maturity_years:>4}y  gross JTD {fmt(p.gross_jtd):>11}  weight {p.maturity_weight:.2f}")  # fmt: skip
    for bucket, obligor, amt, rwt in net_jtd(book):
        print(f"  net piece {bucket:<10} {obligor:<5} {fmt(amt):>12} RW {rwt:.1%}")
    by_bucket = drc_non_securitisation(book)
    for b, v in by_bucket.items():
        print(f"  DRC[{b}] = {fmt(v)}")
    total = sum(by_bucket.values())
    print(f"  DRC non-securitisation total = {fmt(total)}")
    # ALPHA: long 0.75*10m - 0.5m = 7.0m; short equity -4m*1.0 = -4m (offsets: junior short vs senior long, allowed);
    # short senior 6m: -2m*0.75 = -1.5m scaled 0.5 = -0.75m. Net ALPHA = 7.0 - 4.0 - 0.75 = 2.25m long.
    # BETA: long non-senior 6m*1.0 - 0.6m = 5.4m; short senior -3.75m cannot offset the more junior long.
    # GAMMA: short -6.0m. Corporates: longs 2.25 + 5.4 = 7.65; shorts 3.75 + 6.0 = 9.75; HBR = 7.65 / 17.4.
    hbr = 7.65 / 17.4
    expected_corp = 0.06 * 2.25e6 + 0.15 * 5.4e6 - hbr * (0.15 * 3.75e6 + 0.03 * 6.0e6)
    assert close(by_bucket["corporates"], expected_corp)
    assert close(by_bucket["sovereigns"], 0.02 * 0.75 * 20e6 * 0.25)
    # MAR22.15 FAQ: EUR -10m index future (1M) hedged by +10m stocks, both at three months: 1/4*10 - 1/4*10 = 0.
    print(f"  corporates HBR = 7.65 / 17.40 = {hbr:.5f}")
    # The GAMMA CDS is a short in a different name: it adds 6.0m to the HBR denominator, which cuts the credit
    # given to every short in the bucket (MAR22.23). Removing it shows the hedge raises the charge.
    without_gamma = drc_non_securitisation([p for p in book if p.obligor != "GAMMA"])["corporates"]
    print(f"  corporates DRC without the GAMMA CDS hedge = {fmt(without_gamma)} (HBR {7.65 / 11.40:.5f}); with it {fmt(expected_corp)}")
    assert close(without_gamma, 0.945e6 - (7.65 / 11.40) * 0.15 * 3.75e6) and without_gamma < expected_corp
    # MAR22.14(1)(c): bought call on a bond has zero notional; JTD is its MtM, through the P&L term.
    call = DRCPosition("EPSILON", "corporates", "senior", "BBB", 0.0, 400_000.0, 2.0, long_credit=True)
    print(f"  bought call on a bond, MtM 400,000: gross JTD {fmt(call.gross_jtd)}")
    assert close(call.gross_jtd, 400_000.0)
    assert drc_ctp_total([100.0, -100.0]) == 50.0  # MAR22.45 example: +100 and -100 give max(100 - 50, 0)
    # MAR22.14 Table 1: sold put on a senior bond, notional 10m, strike 95% (strike amount 9.5m), option MtM 0.3m.
    # Bond-equivalent market value = strike amount - |MtM| = 9.2m, so P&L = -0.8m and JTD = 0.75 * 10m - 0.8m.
    sold_put = DRCPosition("DELTA", "corporates", "senior", "BBB", 10_000_000.0, 9_500_000.0 - 300_000.0, 2.0)
    print(f"  sold put on a bond (MAR22.14 Table 1): bond-equivalent MV 9,200,000, gross JTD {fmt(sold_put.gross_jtd)}")
    assert close(sold_put.gross_jtd, 6_700_000.0)
    # Nth-to-default as a tranche (MAR22.38): third-to-default on 10 names attaches at 2/10 and detaches at 3/10.
    assert (3 - 1) / 10 == 0.2 and 3 / 10 == 0.3
    print(f"  CTP aggregation check (MAR22.45): +100 and -100 -> {drc_ctp_total([100.0, -100.0]):.0f}")
    return {"corporates": by_bucket["corporates"], "sovereigns": by_bucket["sovereigns"], "total": total, "hbr": hbr}


def example_rrao() -> float:
    print("\n[7] RRAO")
    book = [("exotic", 50_000_000.0), ("other", 200_000_000.0), ("other", 120_000_000.0)]
    for kind, n in book:
        print(f"  {kind:<6} gross notional {fmt(n):>12} RW {RRAO_RW[kind]:.1%} add-on {fmt(RRAO_RW[kind] * n)}")
    total = rrao(book)
    print(f"  RRAO = {fmt(total)}")
    assert close(total, 500_000.0 + 200_000.0 + 120_000.0)
    return total


def example_total(girr: dict, csr: dict, eq: dict, drc: dict, rrao_total: float) -> dict[str, float]:
    print("\n[8] Total standardised approach capital: SbM per scenario, then DRC and RRAO (MAR20.4, MAR21.7)")
    per = {}
    for sc in SCENARIOS:
        per[sc] = girr[sc] + csr[sc] + eq[f"{sc}_delta"] + eq[f"{sc}_vega"] + eq[f"{sc}_curv"]
        print(f"  {sc:<6} GIRR {fmt(girr[sc])} + CSR {fmt(csr[sc])} + EQ delta {fmt(eq[f'{sc}_delta'])} + vega {fmt(eq[f'{sc}_vega'])}"
              f" + curvature {fmt(eq[f'{sc}_curv'])} = {fmt(per[sc])}")  # fmt: skip
    binding = max(per, key=per.get)
    sbm = per[binding]
    total = sbm + drc["total"] + rrao_total
    print(f"  SbM = max over scenarios = {fmt(sbm)} ({binding})")
    print(f"  SA capital = SbM {fmt(sbm)} + DRC {fmt(drc['total'])} + RRAO {fmt(rrao_total)} = {fmt(total)}")
    print(f"  RWA = 12.5 x SA capital = {fmt(12.5 * total)} (MAR20.1)")
    return {"sbm": sbm, "total": total, "rwa": 12.5 * total, "binding": SCENARIOS.index(binding)}


def self_checks() -> None:
    """Spot-checks of tables against the printed Basel text."""
    assert close(girr_tenor_correlation(1.0, 5.0), math.exp(-0.12))  # MAR21.46 fn 284 example
    assert round(girr_tenor_correlation(0.25, 1.0), 3) == 0.914 and round(girr_tenor_correlation(0.5, 15.0), 3) == 0.419  # Table 2
    assert girr_tenor_correlation(0.25, 30.0) == 0.40
    assert close(scenario_correlation(0.6, "high"), 0.75) and close(scenario_correlation(0.6, "low"), 0.45)
    assert close(scenario_correlation(0.9, "low"), 0.8) and scenario_correlation(0.9, "high") == 1.0
    assert csr_ns_gamma("1", "2") == 0.75 and csr_ns_gamma("1", "10") == 0.5 * 0.75 and csr_ns_gamma("17", "18") == 0.75
    assert csr_ns_gamma("3", "16") == 0.0 and csr_ns_gamma("8", "17") == 0.45 and csr_ns_gamma("6", "7") == 0.05
    assert close(csr_ns_rho("4", ("A", 5.0, "bond"), ("B", 10.0, "cds")), 0.35 * 0.65 * 0.999)  # MAR21.54 fn 289
    assert close(commodity_rho("2", ("BRENT", 1.0, "LeHavre"), ("WTI", 5.0, "Oklahoma")), 0.95 * 0.99 * 0.999)  # MAR21.83 fn 292
    assert close(CSR_NONCTP_RW[9], 0.009 * 1.25) and close(CSR_NONCTP_RW[17], 0.009 * 1.75)  # MAR21.65, MAR21.66
    assert equity_gamma("12", "13") == 0.75 and equity_gamma("5", "12") == 0.45 and equity_gamma("2", "9") == 0.15
    # MAR21.99: GIRR curvature shift is the 0.25y risk weight
    assert max(GIRR_RW.values()) == GIRR_RW[0.25] == 0.017
    # A radicand that stays negative after MAR21.4(5)(b) is floored and flagged, and the flag survives
    # risk_class_capital. Three buckets with pairwise gamma -0.9 (not PSD), each holding two uncorrelated factors:
    # K_b = sqrt(2), S_b = 2; first radicand 6 - 21.6 < 0, clamped radicand 6 - 10.8 < 0.
    flagged = risk_class_capital(
        RiskClassSpec("probe", lambda b, k, l_: 0.0, lambda b, c: -0.9),
        [WeightedSensitivity(b, (f,), 1.0) for b in ("1", "2", "3") for f in ("x", "y")],
        "medium",
    )
    assert flagged.alternative_used and flagged.floored and flagged.capital == 0.0
    # PSD status of the inter-bucket gamma matrices (a property of the Basel tables, see across_bucket_capital)
    eig = gamma_min_eigenvalues()
    assert all(v > 0 for (name, _), v in eig.items() if name == "GIRR")
    assert eig[("CSR non-securitisation", "medium")] < 0 and eig[("CSR non-securitisation", "high")] < 0
    assert eig[("CSR non-securitisation", "low")] > 0
    assert eig[("Equity", "high")] < 0 < eig[("Equity", "medium")] and eig[("Equity", "low")] > 0


def gamma_min_eigenvalues() -> dict[tuple[str, str], float]:
    """Smallest eigenvalue of each scenario-adjusted inter-bucket correlation matrix (unit diagonal)."""
    out = {}
    for spec, buckets in (
        (GIRR, ["USD", "EUR", "GBP"]),
        (CSR_NS, [str(b) for b in range(1, 19)]),
        (EQUITY, [str(b) for b in range(1, 14)]),
    ):
        for sc in SCENARIOS:
            m = [[1.0 if b == c else scenario_correlation(spec.gamma(b, c), sc) for c in buckets] for b in buckets]
            out[(spec.name, sc)] = _min_eigenvalue(m)
    return out


def _min_eigenvalue(m: list[list[float]]) -> float:
    """Smallest eigenvalue of a small symmetric matrix by cyclic Jacobi rotations (no numpy needed)."""
    a = [row[:] for row in m]
    n = len(a)
    for _ in range(100):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-20:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-15:
                    continue
                theta = 0.5 * math.atan2(2 * a[p][q], a[q][q] - a[p][p])
                c, s = math.cos(theta), math.sin(theta)
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return min(a[i][i] for i in range(n))


def main() -> None:
    self_checks()
    print("[0] Smallest eigenvalue of each inter-bucket gamma matrix (negative = not PSD)")
    for (name, sc), v in gamma_min_eigenvalues().items():
        print(f"  {name:<24} {sc:<6} {v:+.5f}")
    girr1 = example_girr_flattener()
    girr = example_girr_multi_currency()
    csr = example_csr_alternative_spec()
    eq = example_equity_vega_and_curvature()
    example_girr_curvature()
    drc = example_drc()
    r = example_rrao()
    example_total(girr, csr, eq, drc, r)
    assert girr1["low"] > 0
    print("\nAll FRTB standardised approach checks passed.")


if __name__ == "__main__":
    main()
