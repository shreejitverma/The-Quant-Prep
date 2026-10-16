"""FRTB internal models approach (IMA) reference implementation.

Standard library only. Every regulatory constant is quoted from the consolidated Basel Framework
(chapters MAR30 to MAR33 and MAR99, versions effective 1 January 2023) and cites its paragraph.

Covers:
1. Liquidity horizons (MAR33.12) and the liquidity-horizon cascade (MAR33.4).
2. Expected shortfall estimators and the normal-distribution benchmark (MAR33.3).
3. Stress calibration with the reduced set of risk factors (MAR33.5 to MAR33.7).
4. The internally modelled capital charge IMCC (MAR33.14 to MAR33.15).
5. The risk factor eligibility test RFET (MAR31.12 to MAR31.18) and the SES for NMRFs (MAR33.16 to MAR33.17).
6. Backtesting at bank-wide and desk level (MAR32.4 to MAR32.19, MAR99.9 to MAR99.21).
7. The P&L attribution test (MAR32.34 to MAR32.44).
8. Capital aggregation: C_A, DRC averaging, the amber-zone surcharge and ACR_total (MAR33.22, MAR33.41 to MAR33.46).

Run `python 17-Regulatory-Capital-Basel-and-FRTB/code/frtb_ima.py`; the self-check prints every number used in
the IMA notes (10, 11 and 12 in this section) and asserts it.
"""

from __future__ import annotations

import bisect
import math
import random
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from statistics import NormalDist

STD_NORMAL = NormalDist()

# ============================================================================
# Regulatory constants
# ============================================================================

ES_CONFIDENCE = 0.975  # MAR33.3: 97.5th percentile, one-tailed
BASE_HORIZON_DAYS = 10  # MAR33.4: T, the base horizon
LIQUIDITY_HORIZONS = (10, 20, 40, 60, 120)  # MAR33.4 Table 1: LH_1 to LH_5

# MAR33.12 Table 2: liquidity horizon n (days) by risk factor category; footnote 309 lists the specified FX pairs.
LH_BY_CATEGORY: dict[str, int] = {
    "interest rate: specified currencies": 10,  # EUR, USD, GBP, AUD, JPY, SEK, CAD and the bank's domestic currency
    "interest rate: unspecified currencies": 20,
    "interest rate: volatility": 60,
    "interest rate: other types": 60,
    "credit spread: sovereign IG": 20,
    "credit spread: sovereign HY": 40,
    "credit spread: corporate IG": 40,
    "credit spread: corporate HY": 60,
    "credit spread: volatility": 120,
    "credit spread: other types": 120,
    "equity price: large cap": 10,
    "equity price: small cap": 20,
    "equity price: large cap volatility": 20,
    "equity price: small cap volatility": 60,
    "equity: other types": 60,
    "fx rate: specified currency pairs": 10,
    "fx rate: currency pairs": 20,
    "fx: volatility": 40,
    "fx: other types": 40,
    "energy and carbon emissions trading price": 20,
    "precious metals and non-ferrous metals price": 20,
    "other commodities price": 60,
    "energy and carbon emissions trading price: volatility": 60,
    "precious metals and non-ferrous metals price: volatility": 60,
    "other commodities price: volatility": 120,
    "commodity: other types": 120,
}

REDUCED_SET_MIN_COVERAGE = 0.75  # MAR33.5(2)(b) and MAR33.5 FAQ3: 12-week average of ES_R,C / ES_F,C
IMCC_RHO = 0.5  # MAR33.15(2): weight on the unconstrained IMCC(C)
SES_RHO = 0.6  # MAR33.17(4): correlation parameter for the non-idiosyncratic NMRF term
NMRF_MIN_LH_DAYS = 20  # MAR33.16(1): stress-scenario liquidity horizon is max(LH from MAR33.12, 20)

RFET_MIN_OBS_PER_YEAR = 24  # MAR31.13(1)
RFET_MIN_OBS_PER_90_DAYS = 4  # MAR31.13(1): no 90-day period with fewer than four observations
RFET_ALT_MIN_OBS = 100  # MAR31.13(2): at least 100 observations over the previous 12 months
RFET_WINDOW_DAYS = 365  # "12 months" / "per year" implemented as 365 calendar days (implementation choice)
RFET_GAP_WINDOW_DAYS = 90

# MAR31.16 Table 1: regulatory bucketing approach, lower bucket edges (upper edge of last bucket is infinity).
RFET_BUCKET_EDGES: dict[str, tuple[float, ...]] = {
    "A": (0.0, 0.75, 1.5, 4.0, 7.0, 12.0, 18.0, 25.0, 35.0),  # IR, FX, commodity: one maturity dimension (years)
    "B": (0.0, 0.75, 4.0, 10.0, 18.0, 30.0),  # IR, FX, commodity: several maturity dimensions
    "C": (0.0, 1.5, 3.5, 7.5, 15.0),  # credit spread and equity maturities; vol expiry
    "D": (0.0, 0.05, 0.3, 0.7, 0.95),  # strike dimension expressed as option delta, upper edge 1.00
}

MC_BASE = 1.5  # MAR33.42: multiplication factor m_c fixed at 1.5 before add-ons
# MAR32.9 Table 1 (and MAR99 Table 2): bank-wide backtesting multiplier by number of 99% exceptions over 250 days.
BANKWIDE_MULTIPLIER = {0: 1.50, 1: 1.50, 2: 1.50, 3: 1.50, 4: 1.50, 5: 1.70, 6: 1.76, 7: 1.83, 8: 1.88, 9: 1.92}
BANKWIDE_RED_MULTIPLIER = 2.00  # 10 or more exceptions
BACKTEST_WINDOW = 250  # MAR32.3(3) and MAR32.9: 12 months, 250 trading days
DESK_MAX_EXCEPTIONS_99 = 12  # MAR32.19: more than 12 exceptions at 99% -> standardised approach
DESK_MAX_EXCEPTIONS_975 = 30  # MAR32.19: more than 30 exceptions at 97.5% (the text reads "or 30 exceptions")

PLA_WINDOW = 250  # MAR32.35
PLA_ECDF_STEP = 0.004  # MAR32.39 and MAR32.40: 0.004 x count, ie 1/250
PLA_GREEN_MIN_SPEARMAN = 0.80  # MAR32.42(1): correlation metric above 0.80
PLA_GREEN_MAX_KS = 0.09  # MAR32.42(1): KS metric below 0.09 (p-value 0.264)
PLA_RED_SPEARMAN = 0.70  # MAR32.42(2): red if correlation metric less than 0.70
PLA_RED_KS = 0.12  # MAR32.42(2): red if KS metric above 0.12 (p-value 0.055)

AMBER_SURCHARGE_SCALE = 0.5  # MAR33.45(1): k = 0.5 x sum(SA amber) / sum(SA green or amber)
MIN_IMA_SHARE = 0.10  # MAR32.2: at least 10% of aggregate market risk capital from IMA-qualifying desks
RWA_MULTIPLIER = 12.5  # MAR33.46
DRC_CONFIDENCE = 0.999  # MAR33.20(5): one-year horizon, 99.9 percentile
DRC_PD_FLOOR = 0.0003  # MAR33.24(2): PDs floored at 0.03%
IMCC_AVERAGE_DAYS = 60  # MAR33.41: weighted average of the previous 60 days
DRC_AVERAGE_WEEKS = 12  # MAR33.22: average over the previous 12 weeks


# ============================================================================
# 1. Liquidity horizons and the cascade (MAR33.4, MAR33.12)
# ============================================================================


def next_liquidity_horizon(days: float) -> int:
    """Smallest regulatory horizon (10, 20, 40, 60, 120) that is at least `days`."""
    for lh in LIQUIDITY_HORIZONS:
        if days <= lh:
            return lh
    return LIQUIDITY_HORIZONS[-1]


def liquidity_horizon(category: str, maturity_days: float | None = None) -> int:
    """Liquidity horizon for a risk factor category, capped at instrument maturity (MAR33.12(3) and FAQ4).

    FAQ4: if the instrument matures before the prescribed horizon, use the next longer horizon length
    (out of 10, 20, 40, 60, 120) compared with the maturity, eg IR volatility (60) on a 30-day option -> 40.
    """
    lh = LH_BY_CATEGORY[category]
    if maturity_days is not None and maturity_days < lh:
        return next_liquidity_horizon(maturity_days)
    return lh


def index_liquidity_horizon(weights: Sequence[float], horizons: Sequence[int]) -> int:
    """Liquidity horizon of a multi-sector credit or equity index (MAR33.12 FAQ5).

    Weighted average of constituent horizons, then the shortest regulatory horizon at least that long.
    """
    if len(weights) != len(horizons) or not weights:
        raise ValueError("weights and horizons must be non-empty and of equal length")
    total = sum(weights)
    avg = sum(w * h for w, h in zip(weights, horizons, strict=True)) / total
    return next_liquidity_horizon(avg)


def cascade_es(es_by_level: Sequence[float]) -> float:
    """Liquidity-adjusted ES from base-horizon partial ES values (MAR33.4).

    es_by_level[j-1] = ES_T(P, j): 10-day ES shocking only risk factors with LH >= LH_j (es_by_level[0] = ES_T(P)).
    ES = sqrt( ES_T(P)^2 + sum_{j>=2} ( ES_T(P, j) * sqrt((LH_j - LH_{j-1}) / T) )^2 )
    """
    if len(es_by_level) != len(LIQUIDITY_HORIZONS):
        raise ValueError("need one partial ES per liquidity horizon (5 values)")
    total = es_by_level[0] ** 2
    for j in range(1, len(LIQUIDITY_HORIZONS)):
        step = (LIQUIDITY_HORIZONS[j] - LIQUIDITY_HORIZONS[j - 1]) / BASE_HORIZON_DAYS
        total += (es_by_level[j] * math.sqrt(step)) ** 2
    return math.sqrt(total)


BROAD_RISK_CLASSES = ("interest rate", "credit spread", "equity", "fx", "commodity")  # MAR33.14


def broad_class(category: str) -> str:
    """Map a MAR33.12 category to its MAR33.14 broad regulatory risk class."""
    for cls in ("interest rate", "credit spread", "equity", "fx"):
        if category.startswith(cls):
            return cls
    return "commodity"


def daily_es_runs() -> tuple[dict[str, int], int]:
    """Count the distinct ES calculations behind IMCC (the "up to 63" in the MAR33.15 FAQ).

    For a set of horizons H the nested subsets Q(j) take |H| distinct values, so a book spanning every
    category needs |H| partial ES values per scope, for each of ES_F,C, ES_R,C and ES_R,S.
    """
    per_class = {c: len({lh for cat, lh in LH_BY_CATEGORY.items() if broad_class(cat) == c}) for c in BROAD_RISK_CLASSES}
    whole = len(set(LH_BY_CATEGORY.values()))
    return per_class, 3 * (whole + sum(per_class.values()))


def cascade_scaling_factors() -> list[float]:
    """sqrt((LH_j - LH_{j-1}) / T) for j = 2..5 (MAR33.4)."""
    return [math.sqrt((LIQUIDITY_HORIZONS[j] - LIQUIDITY_HORIZONS[j - 1]) / BASE_HORIZON_DAYS) for j in range(1, len(LIQUIDITY_HORIZONS))]


# ============================================================================
# 2. Expected shortfall
# ============================================================================


def normal_var(alpha: float, sigma: float = 1.0) -> float:
    """VaR at confidence alpha of a zero-mean normal loss."""
    return sigma * STD_NORMAL.inv_cdf(alpha)


def normal_es(alpha: float, sigma: float = 1.0) -> float:
    """ES at confidence alpha of a zero-mean normal loss: sigma * phi(z_alpha) / (1 - alpha)."""
    return sigma * STD_NORMAL.pdf(STD_NORMAL.inv_cdf(alpha)) / (1.0 - alpha)


def mixture_cdf(x: float, weights: Sequence[float], sigmas: Sequence[float]) -> float:
    return sum(w * STD_NORMAL.cdf(x / s) for w, s in zip(weights, sigmas, strict=True))


def mixture_var(alpha: float, weights: Sequence[float], sigmas: Sequence[float]) -> float:
    """Quantile of a zero-mean scale mixture of normals, by bisection."""
    lo, hi = 0.0, 50.0 * max(sigmas)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mixture_cdf(mid, weights, sigmas) < alpha:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def mixture_es(alpha: float, weights: Sequence[float], sigmas: Sequence[float]) -> float:
    """ES of a zero-mean normal scale mixture: E[L; L > q] = sum w_i sigma_i phi(q / sigma_i)."""
    q = mixture_var(alpha, weights, sigmas)
    tail = sum(w * s * STD_NORMAL.pdf(q / s) for w, s in zip(weights, sigmas, strict=True))
    return tail / (1.0 - alpha)


def historical_es(pnl: Sequence[float], alpha: float = ES_CONFIDENCE) -> float:
    """Historical-simulation ES of losses (-P&L) at confidence alpha.

    MAR33 does not prescribe the discrete estimator.
    This uses the tail-weighted estimator: with m = n(1 - alpha), average the floor(m) worst losses plus
    a fractional weight (m - floor(m)) on the next one, so the estimate is continuous in alpha.
    """
    losses = sorted((-x for x in pnl), reverse=True)
    m = len(losses) * (1.0 - alpha)
    whole = int(math.floor(m))
    frac = m - whole
    total = sum(losses[:whole])
    if frac > 0.0:
        total += frac * losses[whole]
    return total / m


def gaussian_partial_es(sigmas: Sequence[float], corr: Sequence[Sequence[float]], subset: Iterable[int]) -> float:
    """10-day 97.5% ES of the sum of linear Gaussian P&L components restricted to `subset`."""
    idx = list(subset)
    var = sum(sigmas[i] * sigmas[k] * corr[i][k] for i in idx for k in idx)
    return normal_es(ES_CONFIDENCE, math.sqrt(var)) if var > 0.0 else 0.0


def gaussian_cascade_levels(sigmas: Sequence[float], corr: Sequence[Sequence[float]], horizons: Sequence[int]) -> list[float]:
    """ES_T(P, j) for j = 1..5 where component i moves only when its horizon >= LH_j (MAR33.4(4) and (6))."""
    return [gaussian_partial_es(sigmas, corr, [i for i, h in enumerate(horizons) if h >= lh_j]) for lh_j in LIQUIDITY_HORIZONS]


# ============================================================================
# 3. Stress calibration and the reduced set (MAR33.5 to MAR33.7)
# ============================================================================


def stress_scaling_ratio(es_full_current: float, es_reduced_current: float) -> float:
    """ES_F,C / ES_R,C floored at 1 (MAR33.6(2))."""
    if es_reduced_current <= 0.0:
        raise ValueError("ES_R,C must be positive")
    return max(1.0, es_full_current / es_reduced_current)


def stress_calibrated_es(es_reduced_stressed: float, es_full_current: float, es_reduced_current: float) -> float:
    """ES = ES_R,S x max(1, ES_F,C / ES_R,C) (MAR33.6)."""
    return es_reduced_stressed * stress_scaling_ratio(es_full_current, es_reduced_current)


def reduced_set_coverage(es_reduced_current: Sequence[float], es_full_current: Sequence[float]) -> float:
    """Average over the preceding 12 weeks of ES_R,C / ES_F,C (MAR33.5(2)(b) and FAQ3); must be >= 0.75."""
    if len(es_reduced_current) != len(es_full_current) or not es_full_current:
        raise ValueError("need matching non-empty weekly series")
    ratios = [r / f for r, f in zip(es_reduced_current, es_full_current, strict=True)]
    return sum(ratios) / len(ratios)


# ============================================================================
# 4. IMCC (MAR33.13 to MAR33.15)
# ============================================================================


def imcc(imcc_unconstrained: float, imcc_by_class: Sequence[float], rho: float = IMCC_RHO) -> float:
    """IMCC = rho * IMCC(C) + (1 - rho) * sum_i IMCC(C_i) (MAR33.15).

    IMCC(C) and each IMCC(C_i) are stress-calibrated ES values: ES_R,S x ES_F,C / ES_R,C for the whole
    portfolio and for each broad risk class with all other risk factors held constant (MAR33.14).
    """
    return rho * imcc_unconstrained + (1.0 - rho) * sum(imcc_by_class)


# ============================================================================
# 5. RFET and SES (MAR31.12 to MAR31.18, MAR33.16 to MAR33.17)
# ============================================================================


@dataclass(frozen=True)
class RfetResult:
    observation_days: int  # distinct days in the 12-month window (one observation per day counts)
    min_obs_in_90_days: int  # fewest observations in any 90-day period inside the window
    passes_24_rule: bool  # MAR31.13(1)
    passes_100_rule: bool  # MAR31.13(2)

    @property
    def modellable(self) -> bool:
        return self.passes_24_rule or self.passes_100_rule


def rfet(observations: Iterable[date], assessment: date) -> RfetResult:
    """Risk factor eligibility test on real price observation dates (MAR31.13).

    Window: the 365 calendar days ending on the assessment date.
    Only one observation per day counts.
    Criterion 1: >= 24 observations and no 90-day period inside the window with fewer than 4.
    Criterion 2: >= 100 observations.
    """
    start = assessment - timedelta(days=RFET_WINDOW_DAYS - 1)
    days = sorted({d for d in observations if start <= d <= assessment})
    min_90 = len(days)
    first_start = start
    last_start = assessment - timedelta(days=RFET_GAP_WINDOW_DAYS - 1)
    s = first_start
    while s <= last_start:
        e = s + timedelta(days=RFET_GAP_WINDOW_DAYS - 1)
        count = bisect.bisect_right(days, e) - bisect.bisect_left(days, s)
        min_90 = min(min_90, count)
        s += timedelta(days=1)
    passes_24 = len(days) >= RFET_MIN_OBS_PER_YEAR and min_90 >= RFET_MIN_OBS_PER_90_DAYS
    passes_100 = len(days) >= RFET_ALT_MIN_OBS
    return RfetResult(len(days), min_90, passes_24, passes_100)


def regulatory_bucket(row: str, value: float) -> int:
    """1-based bucket index under the regulatory bucketing approach (MAR31.16 Table 1)."""
    edges = RFET_BUCKET_EDGES[row]
    if value < 0.0 or (row == "D" and value >= 1.0):
        raise ValueError("value outside the bucket range")
    return bisect.bisect_right(edges, value)


def nmrf_liquidity_horizon(lh_days: int) -> int:
    """Stress-scenario liquidity horizon for an NMRF: max(LH, 20) (MAR33.16(1))."""
    return max(lh_days, NMRF_MIN_LH_DAYS)


def ses_aggregate(
    idio_credit: Sequence[float],
    idio_equity: Sequence[float],
    other: Sequence[float],
    rho: float = SES_RHO,
) -> float:
    """Aggregate NMRF capital (MAR33.17).

    SES = sqrt(sum ISES_i^2) + sqrt(sum ISES_j^2) + sqrt( (rho * sum SES_k)^2 + (1 - rho^2) * sum SES_k^2 )
    I: idiosyncratic credit spread NMRFs and J: idiosyncratic equity NMRFs shown to be fit for zero
    correlation; K: all other NMRFs.
    """
    term_i = math.sqrt(sum(x * x for x in idio_credit))
    term_j = math.sqrt(sum(x * x for x in idio_equity))
    s = sum(other)
    sq = sum(x * x for x in other)
    term_k = math.sqrt((rho * s) ** 2 + (1.0 - rho * rho) * sq)
    return term_i + term_j + term_k


# ============================================================================
# 6. Backtesting (MAR32.4 to MAR32.19, MAR99)
# ============================================================================


def count_exceptions(pnl: Sequence[float | None], var: Sequence[float | None]) -> int:
    """Days on which the loss exceeds VaR; a missing P&L or VaR counts as an outlier (MAR32.5(2), MAR32.18(2))."""
    n = 0
    for p, v in zip(pnl, var, strict=True):
        if p is None or v is None or -p > v:
            n += 1
    return n


def backtest_exceptions(apl: Sequence[float | None], hpl: Sequence[float | None], var: Sequence[float | None]) -> int:
    """Overall exceptions: max of APL and HPL counts, each counted separately (MAR32.5(1), MAR99.8)."""
    return max(count_exceptions(apl, var), count_exceptions(hpl, var))


def bankwide_zone(exceptions: int) -> tuple[str, float]:
    """Bank-wide backtesting zone and multiplier from 99% exceptions over 250 days (MAR32.9 Table 1)."""
    if exceptions >= 10:
        return "red", BANKWIDE_RED_MULTIPLIER
    zone = "green" if exceptions <= 4 else "amber"
    return zone, BANKWIDE_MULTIPLIER[exceptions]


def desk_backtest_ok(exceptions_99: int, exceptions_975: int) -> bool:
    """Desk passes unless > 12 exceptions at 99% or > 30 at 97.5% over 12 months (MAR32.19)."""
    return exceptions_99 <= DESK_MAX_EXCEPTIONS_99 and exceptions_975 <= DESK_MAX_EXCEPTIONS_975


def binomial_cdf(k: int, n: int, p: float) -> float:
    return sum(math.comb(n, i) * p**i * (1.0 - p) ** (n - i) for i in range(k + 1))


# ============================================================================
# 7. P&L attribution test (MAR32.34 to MAR32.44)
# ============================================================================


def average_ranks(values: Sequence[float]) -> list[float]:
    """Ranks 1..n, lowest value first (MAR32.36); ties get their average rank (MAR32 is silent on ties)."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(hpl: Sequence[float], rtpl: Sequence[float]) -> float:
    """r_S = cov(R_HPL, R_RTPL) / (sigma_R_HPL * sigma_R_RTPL) (MAR32.38)."""
    if len(hpl) != len(rtpl) or len(hpl) < 2:
        raise ValueError("series must have equal length >= 2")
    rh, rr = average_ranks(hpl), average_ranks(rtpl)
    mh, mr = sum(rh) / len(rh), sum(rr) / len(rr)
    cov = sum((a - mh) * (b - mr) for a, b in zip(rh, rr, strict=True))
    vh = sum((a - mh) ** 2 for a in rh)
    vr = sum((b - mr) ** 2 for b in rr)
    if vh == 0.0 or vr == 0.0:
        raise ValueError("constant series has no rank correlation")
    return cov / math.sqrt(vh * vr)


def ks_statistic(hpl: Sequence[float], rtpl: Sequence[float]) -> float:
    """Largest absolute difference between the two empirical CDFs (MAR32.39 to MAR32.41).

    The ECDF at x is (1/n) x #{obs <= x}; with n = 250 this is the 0.004 factor in MAR32.39.
    The supremum is attained at an observed point, so evaluating at every observation is exact.
    """
    a, b = sorted(hpl), sorted(rtpl)
    na, nb = len(a), len(b)
    d = 0.0
    for x in sorted(set(a) | set(b)):
        fa = bisect.bisect_right(a, x) / na
        fb = bisect.bisect_right(b, x) / nb
        d = max(d, abs(fa - fb))
    return d


def ks_asymptotic_p_value(d: float, n1: int = PLA_WINDOW, n2: int = PLA_WINDOW) -> float:
    """Asymptotic two-sample KS p-value: Q(lambda) = 2 sum_{k>=1} (-1)^(k-1) exp(-2 k^2 lambda^2).

    lambda = d x sqrt(n1 n2 / (n1 + n2)); reproduces the p-values quoted next to the MAR32.42 thresholds.
    """
    lam = d * math.sqrt(n1 * n2 / (n1 + n2))
    return 2.0 * sum((-1) ** (k - 1) * math.exp(-2.0 * k * k * lam * lam) for k in range(1, 101))


def pla_zone(spearman_metric: float, ks_metric: float) -> str:
    """PLA zone (MAR32.42): green needs r_S > 0.80 and KS < 0.09; red if r_S < 0.70 or KS > 0.12; else amber."""
    if spearman_metric < PLA_RED_SPEARMAN or ks_metric > PLA_RED_KS:
        return "red"
    if spearman_metric > PLA_GREEN_MIN_SPEARMAN and ks_metric < PLA_GREEN_MAX_KS:
        return "green"
    return "amber"


def pla_test(hpl: Sequence[float], rtpl: Sequence[float]) -> tuple[float, float, str]:
    if len(hpl) != PLA_WINDOW or len(rtpl) != PLA_WINDOW:
        raise ValueError("MAR32.35 requires the most recent 250 trading days")
    rs, ks = spearman(hpl, rtpl), ks_statistic(hpl, rtpl)
    return rs, ks, pla_zone(rs, ks)


def next_desk_state(state: str, pla_outcome: str, backtest_ok_12m: bool) -> str:
    """Quarterly desk classification update (MAR32.43, MAR32.44, MAR32.19).

    state and result are one of "green", "amber", "red" (red = out of scope, capitalised under the SA).
    A red desk returns only after a green PLA outcome with backtesting satisfied over the past 12 months.
    An amber desk returns to green only after a green PLA outcome with backtesting satisfied.
    A desk failing desk-level backtesting goes to the standardised approach regardless of PLA.
    """
    if not backtest_ok_12m or pla_outcome == "red":
        return "red"
    if state == "red":
        return "green" if pla_outcome == "green" else "red"
    return pla_outcome


# ============================================================================
# 8. Capital aggregation (MAR33.22, MAR33.41 to MAR33.46)
# ============================================================================


def capital_eligible_desks(imcc_series: Sequence[float], ses_series: Sequence[float], mc: float) -> float:
    """C_A = max(IMCC_{t-1} + SES_{t-1}, m_c x IMCC_avg + SES_avg) over the previous 60 days (MAR33.41).

    The series hold the previous 60 daily values, most recent last.
    The multiplier applies to IMCC only, not to SES.
    """
    if len(imcc_series) != IMCC_AVERAGE_DAYS or len(ses_series) != IMCC_AVERAGE_DAYS:
        raise ValueError("need the previous 60 daily IMCC and SES values")
    latest = imcc_series[-1] + ses_series[-1]
    averaged = mc * sum(imcc_series) / IMCC_AVERAGE_DAYS + sum(ses_series) / IMCC_AVERAGE_DAYS
    return max(latest, averaged)


def drc_capital(weekly_drc: Sequence[float]) -> float:
    """IMA DRC = max(average of the previous 12 weekly measures, most recent measure) (MAR33.22)."""
    if len(weekly_drc) != DRC_AVERAGE_WEEKS:
        raise ValueError("need the previous 12 weekly DRC measures")
    return max(sum(weekly_drc) / DRC_AVERAGE_WEEKS, weekly_drc[-1])


def amber_surcharge(sa_by_desk: dict[str, float], amber_desks: set[str], ima_ga: float, sa_ga: float) -> tuple[float, float]:
    """Capital surcharge = k x max(0, SA_G,A - IMA_G,A), k = 0.5 x SA(amber) / SA(green or amber) (MAR33.45).

    sa_by_desk holds standalone SA capital of every approved desk in the green or amber zone.
    Returns (k, surcharge).
    """
    denom = sum(sa_by_desk.values())
    k = AMBER_SURCHARGE_SCALE * sum(v for d, v in sa_by_desk.items() if d in amber_desks) / denom if denom > 0.0 else 0.0
    return k, k * max(0.0, sa_ga - ima_ga)


def aggregate_capital(ima_ga: float, surcharge: float, c_u: float, sa_all: float, sa_ga: float) -> float:
    """ACR_total = min(IMA_G,A + surcharge + C_U, SA_all desks) + max(0, IMA_G,A - SA_G,A) (MAR33.43)."""
    return min(ima_ga + surcharge + c_u, sa_all) + max(0.0, ima_ga - sa_ga)


# ============================================================================
# Self-check: every number used in the IMA notes
# ============================================================================


def _fmt(x: float) -> str:
    return f"{x:,.2f}"


def _close(a: float, b: float, tol: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def demo_liquidity_horizons() -> None:
    print("== Liquidity horizons (MAR33.12) ==")
    assert liquidity_horizon("interest rate: volatility", maturity_days=30) == 40
    assert liquidity_horizon("credit spread: corporate HY", maturity_days=15) == 20
    assert liquidity_horizon("equity price: large cap", maturity_days=5) == 10
    assert index_liquidity_horizon([0.8, 0.2], [10, 20]) == 20  # weighted average 12 days -> 20 (FAQ5 example)
    print("IR vol on 30-day option -> LH 40; index with weighted average 12 days -> LH 20")
    factors = cascade_scaling_factors()
    print("cascade scaling sqrt((LH_j - LH_{j-1})/10) for j=2..5:", [f"{f:.6f}" for f in factors])
    assert _close(factors[0], 1.0) and _close(factors[1], math.sqrt(2.0)) and _close(factors[3], math.sqrt(6.0))

    # Consistency of the cascade: if every factor has the same horizon LH_j, ES scales by sqrt(LH_j / 10).
    for j, lh in enumerate(LIQUIDITY_HORIZONS):
        levels = [1.0 if k <= j else 0.0 for k in range(5)]
        assert _close(cascade_es(levels), math.sqrt(lh / BASE_HORIZON_DAYS))
    print("single-horizon check: cascade(ES all at LH_j) = ES x sqrt(LH_j/10) for every j")
    per_class, runs = daily_es_runs()
    print(f"distinct horizons per broad class {per_class}; whole book 5; daily ES runs = 3 x (5 + {sum(per_class.values())}) = {runs}")
    assert runs == 63

    # Worked example: a credit and macro desk with five Gaussian linear P&L components (10-day stressed sigma, USD m).
    names = ["USD swap curve", "EUR/USD spot", "IG corporate spreads", "HY corporate spreads", "credit spread vol"]
    horizons = [
        LH_BY_CATEGORY["interest rate: specified currencies"],
        LH_BY_CATEGORY["fx rate: specified currency pairs"],
        LH_BY_CATEGORY["credit spread: corporate IG"],
        LH_BY_CATEGORY["credit spread: corporate HY"],
        LH_BY_CATEGORY["credit spread: volatility"],
    ]
    sigmas = [4.0, 2.0, 3.0, 2.5, 1.0]
    corr = [
        [1.0, 0.1, -0.3, -0.2, 0.0],
        [0.1, 1.0, 0.0, 0.0, 0.0],
        [-0.3, 0.0, 1.0, 0.6, 0.3],
        [-0.2, 0.0, 0.6, 1.0, 0.4],
        [0.0, 0.0, 0.3, 0.4, 1.0],
    ]
    levels = gaussian_cascade_levels(sigmas, corr, horizons)
    es = cascade_es(levels)
    print("components:", ", ".join(f"{n} (LH {h}, sigma {s})" for n, h, s in zip(names, horizons, sigmas, strict=True)))
    for j, (lh, v) in enumerate(zip(LIQUIDITY_HORIZONS, levels, strict=True), start=1):
        print(f"  ES_T(P,{j}) [factors with LH >= {lh}] = {v:.6f}")
    terms = [levels[0] ** 2] + [(levels[j] * factors[j - 1]) ** 2 for j in range(1, 5)]
    print("  squared terms:", [f"{t:.6f}" for t in terms])
    print(f"  liquidity-adjusted ES = {es:.6f}; ratio to 10-day ES = {es / levels[0]:.6f}")
    eff = BASE_HORIZON_DAYS * (es / levels[0]) ** 2
    print(f"  effective horizon 10 x (ES / ES_T)^2 = {eff:.4f} days")
    naive = math.sqrt(sum((normal_es(ES_CONFIDENCE, s) * math.sqrt(h / 10)) ** 2 for s, h in zip(sigmas, horizons, strict=True)))
    print(f"  (not the rule) uncorrelated per-factor sqrt-time scaling would give {naive:.6f}")
    # Hand variances: full book 39.45; LH >= 20 and >= 40 (IG, HY, vol) 16.25 + 2 x (4.5 + 0.9 + 1.0) = 29.05;
    # LH >= 60 (HY, vol) 7.25 + 2 x 1.0 = 9.25; LH >= 120 (vol) 1.
    assert _close(levels[0], normal_es(ES_CONFIDENCE, math.sqrt(39.45)))
    assert _close(levels[1], levels[2]) and _close(levels[2], normal_es(ES_CONFIDENCE, math.sqrt(29.05)))
    assert _close(levels[3], normal_es(ES_CONFIDENCE, math.sqrt(9.25)))
    assert _close(levels[4], normal_es(ES_CONFIDENCE, 1.0))
    assert _close(es, math.sqrt(sum(terms)))


def demo_es_vs_var() -> None:
    print("== ES 97.5 against VaR 99 (MAR33.3) ==")
    z99 = normal_var(0.99)
    es975 = normal_es(0.975)
    z975 = normal_var(0.975)
    print(f"normal: VaR99 = {z99:.6f} sigma, VaR97.5 = {z975:.6f} sigma, ES97.5 = {es975:.6f} sigma, ratio = {es975 / z99:.6f}")
    assert _close(z99, 2.326348, 1e-6) and _close(es975, 2.337803, 1e-6)
    w, s = [0.95, 0.05], [1.0, 3.0]
    sd = math.sqrt(sum(wi * si * si for wi, si in zip(w, s, strict=True)))
    v99 = mixture_var(0.99, w, s)
    e975 = mixture_es(0.975, w, s)
    print(f"mixture 95% N(0,1) + 5% N(0,9): sd = {sd:.6f}, VaR99 = {v99:.6f}, ES97.5 = {e975:.6f}, ratio = {e975 / v99:.6f}")
    print(f"  in units of the mixture sd: VaR99 = {v99 / sd:.6f}, ES97.5 = {e975 / sd:.6f}")
    assert e975 > v99
    assert _close(mixture_cdf(v99, w, s), 0.99, 1e-12)
    # MAR99.21: normal ratio of 99th to 98th percentile.
    print(f"MAR99.21 check: z99 / z98 = {z99 / normal_var(0.98):.6f}")

    rng = random.Random(20260116)
    pnl = [round(rng.gauss(0.0, 1.0) * (3.0 if rng.random() < 0.05 else 1.0), 4) for _ in range(250)]
    worst = sorted((-x for x in pnl), reverse=True)[:7]
    es_hist = historical_es(pnl)
    print("historical sample (250 days, seed 20260116): worst 7 losses", [f"{x:.4f}" for x in worst])
    print(f"  m = 250 x 0.025 = 6.25; ES = (sum of worst 6 + 0.25 x 7th) / 6.25 = {es_hist:.6f}")
    assert _close(es_hist, (sum(worst[:6]) + 0.25 * worst[6]) / 6.25)


def demo_stress_and_imcc() -> None:
    print("== Stress calibration and IMCC (MAR33.5 to MAR33.15) ==")
    weekly_rc = [74.0, 77.0, 80.0, 79.0, 76.0, 73.0, 78.0, 81.0, 80.0, 77.0, 76.0, 79.0]
    weekly_fc = [100.0] * 12
    cov = reduced_set_coverage(weekly_rc, weekly_fc)
    print(f"12-week average ES_R,C / ES_F,C = {cov:.6f} (needs >= 0.75)")
    assert _close(cov, 77.5 / 100.0) and cov >= REDUCED_SET_MIN_COVERAGE

    # Whole portfolio and three broad risk classes (USD m). Each IMCC term is ES_R,S x max(1, ES_F,C / ES_R,C).
    total = (60.0, 40.0, 32.0)  # (ES_R,S, ES_F,C, ES_R,C)
    classes = {
        "interest rate": (45.0, 28.0, 25.0),
        "credit spread": (38.0, 22.0, 20.0),
        "equity": (20.0, 15.0, 16.0),  # reduced set overshoots: ratio 15/16 floored at 1
    }
    imcc_c = stress_calibrated_es(*total)
    by_class = {k: stress_calibrated_es(*v) for k, v in classes.items()}
    value = imcc(imcc_c, list(by_class.values()))
    print(f"IMCC(C) = 60 x 40/32 = {imcc_c:.6f}")
    for k, v in by_class.items():
        r = stress_scaling_ratio(classes[k][1], classes[k][2])
        print(f"  IMCC({k}) = {classes[k][0]} x ratio {r:.6f} = {v:.6f}")
    print(
        f"sum of constrained = {sum(by_class.values()):.6f}; IMCC = 0.5 x {imcc_c:.6f} + 0.5 x {sum(by_class.values()):.6f} = {value:.6f}"
    )
    assert _close(imcc_c, 75.0)
    assert _close(by_class["equity"], 20.0)
    assert _close(value, 0.5 * 75.0 + 0.5 * (50.4 + 41.8 + 20.0))
    print(f"diversification recognised: {sum(by_class.values()) - imcc_c:.6f}; half of it kept: {sum(by_class.values()) - value:.6f}")


def demo_rfet_and_ses() -> None:
    print("== RFET (MAR31.13) ==")
    a = date(2026, 9, 30)
    start = a - timedelta(days=364)
    # Factor A: 26 trades, but none from 1 March to 9 June 2026 except two -> a 90-day period with fewer than 4.
    fa = [start + timedelta(days=14 * i) for i in range(26)]
    fa = [d for d in fa if not (date(2026, 3, 1) <= d <= date(2026, 6, 9))] + [date(2026, 4, 1), date(2026, 5, 15)]
    while len(fa) < 26:
        fa.append(date(2026, 9, 1) + timedelta(days=len(fa)))
    ra = rfet(fa, a)
    print(f"factor A: {ra.observation_days} observation days, min in any 90 days = {ra.min_obs_in_90_days} -> modellable {ra.modellable}")
    # Factor B: one observation every 15 days.
    fb = [start + timedelta(days=15 * i) for i in range(25)]
    rb = rfet(fb, a)
    print(f"factor B: {rb.observation_days} observation days, min in any 90 days = {rb.min_obs_in_90_days} -> modellable {rb.modellable}")
    # Factor C: 115 trades on 23 distinct days, five per day, every 15 days -> only 23 observations count.
    fc = [start + timedelta(days=15 * i) for i in range(23)]
    rc = rfet(fc * 5, a)
    print(f"factor C: {len(fc) * 5} trades on {rc.observation_days} distinct days -> modellable {rc.modellable}")
    # Factor D: 104 observation days clustered in the first half of the window -> fails rule 1, passes rule 2.
    fd = [start + timedelta(days=i) for i in range(0, 208, 2)]
    rd = rfet(fd, a)
    print(
        f"factor D: {rd.observation_days} observation days, min in any 90 days = {rd.min_obs_in_90_days}, "
        f"rule 24 {rd.passes_24_rule}, rule 100 {rd.passes_100_rule} -> modellable {rd.modellable}"
    )
    assert not ra.modellable and ra.observation_days >= 24 and ra.min_obs_in_90_days < 4
    assert rb.modellable and rb.observation_days == 25 and rb.min_obs_in_90_days >= 4
    assert not rc.modellable and rc.observation_days == 23 and rc.min_obs_in_90_days >= 4
    assert rd.modellable and not rd.passes_24_rule and rd.passes_100_rule
    assert regulatory_bucket("C", 5.0) == 3 and regulatory_bucket("A", 30.0) == 8 and regulatory_bucket("D", 0.5) == 3
    print("bucketing: 5y credit spread -> row C bucket 3; 30y rate -> row A bucket 8; 50-delta strike -> row D bucket 3")

    print("== SES aggregation (MAR33.16 to MAR33.17) ==")
    assert nmrf_liquidity_horizon(10) == 20 and nmrf_liquidity_horizon(60) == 60
    idio_credit = [3.0, 4.0]
    idio_equity = [2.0]
    other = [5.0, 3.0, 2.0]
    ses = ses_aggregate(idio_credit, idio_equity, other)
    term_k = math.sqrt((0.6 * 10.0) ** 2 + 0.64 * 38.0)
    print(f"I term sqrt(9+16) = 5; J term = 2; K term sqrt((0.6 x 10)^2 + 0.64 x 38) = {term_k:.6f}; SES = {ses:.6f}")
    print(f"  linear sum would be {sum(idio_credit) + sum(idio_equity) + sum(other):.6f}")
    assert _close(ses, 5.0 + 2.0 + term_k)
    # Edge cases of the K term: one factor -> itself; rho = 1 -> linear sum; rho = 0 -> root sum of squares.
    assert _close(ses_aggregate([], [], [7.0]), 7.0)
    assert _close(ses_aggregate([], [], other, rho=1.0), 10.0) and _close(ses_aggregate([], [], other, rho=0.0), math.sqrt(38.0))

    print("== Capital cliff illustration (simplified: one risk class, ratio 1, averages = latest) ==")
    es_mult = normal_es(ES_CONFIDENCE)
    sa, sb, rho = 10.0, 4.0, -0.5  # 10-day stressed sigma of A and of its partial hedge B, both LH 10
    joint = es_mult * math.sqrt(sa * sa + sb * sb + 2 * rho * sa * sb)
    modellable = MC_BASE * joint
    ses_b = es_mult * sb * math.sqrt(nmrf_liquidity_horizon(10) / BASE_HORIZON_DAYS)
    non_modellable = MC_BASE * es_mult * sa + ses_b
    print(f"B modellable: 1.5 x ES(A+B) = 1.5 x {joint:.6f} = {modellable:.6f}")
    print(f"B an NMRF: 1.5 x ES(A) + SES_B = {MC_BASE * es_mult * sa:.6f} + {ses_b:.6f} = {non_modellable:.6f}")
    print(f"  capital rises by {non_modellable - modellable:.6f} ({non_modellable / modellable - 1:.4%}) with no change in positions")
    assert non_modellable > modellable


def _desk_series(seed: int) -> tuple[list[float], list[float], list[float]]:
    rng = random.Random(seed)
    hpl = [rng.gauss(0.0, 1.0) * (2.5 if rng.random() < 0.04 else 1.0) for _ in range(BACKTEST_WINDOW)]
    apl = [h + rng.gauss(0.0, 0.15) for h in hpl]
    var99 = [normal_var(0.99) * 1.02 for _ in range(BACKTEST_WINDOW)]
    return apl, hpl, var99


def demo_backtesting() -> None:
    print("== Backtesting (MAR32, MAR99) ==")
    table2 = [8.11, 28.58, 54.32, 75.81, 89.22, 95.88, 98.63, 99.60, 99.89, 99.97, 99.99]
    computed = [round(100 * binomial_cdf(k, 250, 0.01), 2) for k in range(11)]
    print("binomial(250, 1%) cumulative probabilities 0..10:", computed)
    assert computed == table2
    print(f"expected exceptions over 250 days: 99% -> {250 * 0.01:.2f}, 97.5% -> {250 * 0.025:.2f}")
    p_fail_99 = 1.0 - binomial_cdf(12, 250, 0.01)
    p_fail_975 = 1.0 - binomial_cdf(30, 250, 0.025)
    print(f"accurate desk model fails MAR32.19 by chance: P(>12 at 99%) = {p_fail_99:.3e}, P(>30 at 97.5%) = {p_fail_975:.3e}")
    p_fail_99_bad = 1.0 - binomial_cdf(12, 250, 0.04)
    print(f"desk model with true 96% coverage at the 99% level: P(>12 exceptions) = {p_fail_99_bad:.6f}")

    apl, hpl, var99 = _desk_series(7)
    e_apl, e_hpl = count_exceptions(apl, var99), count_exceptions(hpl, var99)
    overall = backtest_exceptions(apl, hpl, var99)
    zone, mult = bankwide_zone(overall)
    print(f"bank-wide sample (seed 7): APL exceptions {e_apl}, HPL exceptions {e_hpl}, overall {overall} -> {zone}, m_c = {mult:.2f}")
    assert overall == max(e_apl, e_hpl)
    hpl_missing: list[float | None] = list(hpl)
    hpl_missing[100] = None
    assert count_exceptions(hpl_missing, var99) == e_hpl + (0 if -hpl[100] > var99[100] else 1)
    for n, expect in [(4, ("green", 1.50)), (5, ("amber", 1.70)), (9, ("amber", 1.92)), (10, ("red", 2.00)), (14, ("red", 2.00))]:
        assert bankwide_zone(n) == expect
    assert desk_backtest_ok(12, 30) and not desk_backtest_ok(13, 0) and not desk_backtest_ok(0, 31)


def demo_pla() -> None:
    print("== PLA test (MAR32.34 to MAR32.44) ==")
    rng = random.Random(42)
    hpl = [rng.gauss(0.0, 1.0) for _ in range(PLA_WINDOW)]
    cases = {
        "close model (noise 0.25)": [h + rng.gauss(0.0, 0.25) for h in hpl],
        "missing basis factor (noise 0.75)": [h + rng.gauss(0.0, 0.75) for h in hpl],
        "volatility understated (0.75 x HPL)": [0.75 * h for h in hpl],
        "volatility understated (0.6 x HPL)": [0.6 * h for h in hpl],
        "missing dominant factor (noise 1.2)": [h + rng.gauss(0.0, 1.2) for h in hpl],
        "right distribution, wrong days (HPL permuted)": random.Random(99).sample(hpl, len(hpl)),
    }
    results = {}
    for name, rtpl in cases.items():
        rs, ks, zone = pla_test(hpl, rtpl)
        results[name] = (rs, ks, zone)
        print(f"  {name}: Spearman = {rs:.4f}, KS = {ks:.4f} -> {zone}")
    assert results["close model (noise 0.25)"][2] == "green"
    assert results["missing basis factor (noise 0.75)"][2] == "amber"
    assert _close(results["volatility understated (0.75 x HPL)"][0], 1.0)
    assert results["volatility understated (0.6 x HPL)"][2] == "red"
    assert results["missing dominant factor (noise 1.2)"][2] == "red"
    permuted = results["right distribution, wrong days (HPL permuted)"]
    assert permuted[1] == 0.0 and permuted[2] == "red"
    p09, p12 = ks_asymptotic_p_value(0.09), ks_asymptotic_p_value(0.12)
    print(f"asymptotic KS p-values with n = 250 each: KS 0.09 -> {p09:.4f}, KS 0.12 -> {p12:.4f}")
    assert abs(p09 - 0.264) < 0.0015 and abs(p12 - 0.055) < 0.0015
    assert pla_zone(0.80, 0.05) == "amber" and pla_zone(0.81, 0.09) == "amber" and pla_zone(0.70, 0.12) == "amber"
    assert pla_zone(0.6999, 0.0) == "red" and pla_zone(0.95, 0.1201) == "red" and pla_zone(0.8001, 0.0899) == "green"
    assert _close(spearman([1.0, 1.0, 2.0], [1.0, 2.0, 3.0]), math.sqrt(3.0) / 2.0)
    assert _close(ks_statistic([0.0, 1.0], [0.5, 2.0]), 0.5)
    print("boundaries: r_S = 0.80 is amber (green needs above 0.80); KS = 0.12 is amber (red needs above 0.12)")

    path = []
    state = "green"
    for outcome, bt in [("amber", True), ("green", True), ("red", True), ("amber", True), ("green", False), ("green", True)]:
        state = next_desk_state(state, outcome, bt)
        path.append(state)
    print("quarterly desk states for outcomes amber, green, red, amber, green (backtest failed), green:", path)
    assert path == ["amber", "green", "red", "red", "red", "green"]


def demo_capital() -> None:
    print("== Capital aggregation (MAR33.22, MAR33.41 to MAR33.46) ==")
    imcc_series = [100.0 + 0.5 * i for i in range(60)]  # previous 60 days, most recent last (USD m)
    ses_series = [20.0 + 0.1 * i for i in range(60)]
    imcc_avg = sum(imcc_series) / 60
    ses_avg = sum(ses_series) / 60
    _, mc = bankwide_zone(6)
    c_a = capital_eligible_desks(imcc_series, ses_series, mc)
    print(f"IMCC_t-1 = {imcc_series[-1]:.2f}, SES_t-1 = {ses_series[-1]:.2f}, IMCC_avg = {imcc_avg:.2f}, SES_avg = {ses_avg:.2f}")
    latest, averaged = imcc_series[-1] + ses_series[-1], mc * imcc_avg + ses_avg
    print(f"6 bank-wide exceptions -> m_c = {mc:.2f}; C_A = max({latest:.2f}, {averaged:.4f}) = {c_a:.4f}")
    assert _close(c_a, 1.76 * 114.75 + 22.95)
    weekly_drc = [30.0, 31.0, 29.0, 32.0, 33.0, 30.0, 28.0, 31.0, 34.0, 35.0, 33.0, 32.0]
    drc = drc_capital(weekly_drc)
    print(f"DRC weekly average = {sum(weekly_drc) / 12:.4f}, latest = {weekly_drc[-1]:.2f} -> DRC = {drc:.4f}")
    ima_ga = c_a + drc
    sa_by_desk = {"rates": 180.0, "fx": 60.0, "credit": 140.0}  # standalone SA of each approved desk
    amber = {"credit"}
    sa_ga = 330.0  # SA computed on all green and amber desks together (less than the 380 standalone sum: netting across desks)
    k, surcharge = amber_surcharge(sa_by_desk, amber, ima_ga, sa_ga)
    c_u = 90.0  # SA for out-of-scope and red desks
    sa_all = 400.0  # SA computed on every desk together
    acr = aggregate_capital(ima_ga, surcharge, c_u, sa_all, sa_ga)
    print(f"IMA_G,A = C_A + DRC = {ima_ga:.4f}; k = 0.5 x 140 / 380 = {k:.6f}; surcharge = k x ({sa_ga} - {ima_ga:.4f}) = {surcharge:.4f}")
    capped = ima_ga + surcharge + c_u
    print(f"ACR_total = min({capped:.4f}, {sa_all}) + max(0, {ima_ga - sa_ga:.4f}) = {acr:.4f}; RWA = {acr * RWA_MULTIPLIER:.4f}")
    assert _close(k, 0.5 * 140.0 / 380.0)
    assert _close(acr, min(ima_ga + surcharge + c_u, sa_all))
    share = ima_ga / acr
    print(f"share of capital from IMA-eligible desks = {share:.4%} (MAR32.2 needs at least 10%)")
    assert share >= MIN_IMA_SHARE
    # When IMA exceeds SA for the approved desks the cap cannot reduce capital below IMA + C_U if SA is additive.
    assert _close(aggregate_capital(350.0, 0.0, 90.0, 420.0, 330.0), min(440.0, 420.0) + 20.0)
    print("cap check: IMA_G,A 350 > SA_G,A 330, C_U 90, SA_all 420 -> ACR =", aggregate_capital(350.0, 0.0, 90.0, 420.0, 330.0))


def run_tests() -> None:
    demo_liquidity_horizons()
    demo_es_vs_var()
    demo_stress_and_imcc()
    demo_rfet_and_ses()
    demo_backtesting()
    demo_pla()
    demo_capital()
    print("All FRTB IMA checks passed.")


if __name__ == "__main__":
    run_tests()
