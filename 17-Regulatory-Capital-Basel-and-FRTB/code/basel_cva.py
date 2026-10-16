"""Basel CVA risk capital reference implementation (MAR50, version in force from 1 January 2023).

1. BA-CVA reduced version (MAR50.14 to MAR50.16) and full version with eligible hedges (MAR50.17 to MAR50.26).
2. SA-CVA bucket and cross-bucket aggregation with the hedging disallowance R (MAR50.42 to MAR50.53),
   with the counterparty credit spread delta parameters of MAR50.63 to MAR50.65.

Formulas are transcribed from the Basel Framework formula images for MAR50 and cited by paragraph.
The worked examples reuse the SA-CCR netting sets of `basel_credit_saccr.py` (CRE99.22 to CRE99.59) as EAD inputs,
and `run_tests()` computes, prints and asserts every number quoted in note 05 (CVA capital).
Run with `python 17-Regulatory-Capital-Basel-and-FRTB/code/basel_cva.py`.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

from basel_credit_saccr import QUOTED_LOG, cre99_portfolios, quoted, saccr_ead

RHO = 0.50  # MAR50.14(2)
BETA = 0.25  # MAR50.20
DS_BA_CVA = 0.65  # MAR50.14 and MAR50.20 discount scalar
ALPHA = 1.4  # MAR50.15(5)
HEDGING_DISALLOWANCE_R = 0.01  # MAR50.53(1)
M_CVA = 1.0  # MAR50.41
MATERIALITY_THRESHOLD_EUR = 100e9  # MAR50.9(1): aggregate notional of non-centrally cleared derivatives

# MAR50.16 Table 1: (IG, HY and NR) supervisory risk weights by sector.
BA_CVA_RW = {
    "sovereign": (0.005, 0.020),
    "local_government": (0.010, 0.040),
    "financial": (0.050, 0.120),
    "basic_materials_energy_industrials": (0.030, 0.070),
    "consumer_transport_admin": (0.030, 0.085),
    "technology_telecom": (0.020, 0.055),
    "health_utilities_professional": (0.015, 0.050),
    "other": (0.050, 0.120),
}

# MAR50.26 Table 2: correlation between counterparty spread and single-name hedge spread.
R_HC = {"direct": 1.00, "legally_related": 0.80, "sector_region": 0.50}


def supervisory_df(maturity: float) -> float:
    """MAR50.15(4): DF = (1 - exp(-0.05 M)) / (0.05 M); DF = 1 for IMM banks."""
    return (1.0 - math.exp(-0.05 * maturity)) / (0.05 * maturity)


def ba_cva_rw(sector: str, investment_grade: bool) -> float:
    ig, hy = BA_CVA_RW[sector]
    return ig if investment_grade else hy


@dataclass(frozen=True)
class NettingSetExposure:
    ead: float  # EAD_NS as computed for CCR capital (SA-CCR or IMM)
    maturity: float  # M_NS per CRE32.46 to CRE32.54 (or CRE53.20 to CRE53.21 for IMM) without the 5-year cap
    imm: bool = False


@dataclass(frozen=True)
class SingleNameHedge:
    notional: float  # B_h, positive for bought protection
    maturity: float  # M_h
    rw: float  # RW_h from MAR50.16 for the hedge reference name
    relation: str  # key of R_HC


@dataclass(frozen=True)
class IndexHedge:
    notional: float  # B_i
    maturity: float  # M_i
    rw: float  # RW_i after the MAR50.24(4) 0.7 diversification scaling


@dataclass
class Counterparty:
    name: str
    rw: float
    netting_sets: Sequence[NettingSetExposure]
    hedges: Sequence[SingleNameHedge] = field(default_factory=tuple)


def stand_alone_cva(cp: Counterparty) -> float:
    """MAR50.15: SCVA_c = (1 / alpha) RW_c sum_NS M_NS EAD_NS DF_NS."""
    total = 0.0
    for ns in cp.netting_sets:
        df = 1.0 if ns.imm else supervisory_df(ns.maturity)
        total += ns.maturity * ns.ead * df
    return cp.rw * total / ALPHA


def k_reduced(counterparties: Sequence[Counterparty]) -> float:
    """MAR50.14: sqrt((rho sum SCVA_c)^2 + (1 - rho^2) sum SCVA_c^2)."""
    scva = [stand_alone_cva(c) for c in counterparties]
    return math.sqrt((RHO * sum(scva)) ** 2 + (1.0 - RHO**2) * sum(s * s for s in scva))


def snh(cp: Counterparty) -> float:
    """MAR50.23: SNH_c = sum_h r_hc RW_h M_h B_h DF_h."""
    return sum(R_HC[h.relation] * h.rw * h.maturity * h.notional * supervisory_df(h.maturity) for h in cp.hedges)


def hma(cp: Counterparty) -> float:
    """MAR50.25: HMA_c = sum_h (1 - r_hc^2) (RW_h M_h B_h DF_h)^2."""
    return sum((1.0 - R_HC[h.relation] ** 2) * (h.rw * h.maturity * h.notional * supervisory_df(h.maturity)) ** 2 for h in cp.hedges)


def ih(index_hedges: Sequence[IndexHedge]) -> float:
    """MAR50.24: IH = sum_i RW_i M_i B_i DF_i."""
    return sum(i.rw * i.maturity * i.notional * supervisory_df(i.maturity) for i in index_hedges)


def k_hedged(counterparties: Sequence[Counterparty], index_hedges: Sequence[IndexHedge] = ()) -> float:
    """MAR50.21: sqrt((rho sum (SCVA_c - SNH_c) - IH)^2 + (1 - rho^2) sum (SCVA_c - SNH_c)^2 + sum HMA_c)."""
    net = [stand_alone_cva(c) - snh(c) for c in counterparties]
    systematic = (RHO * sum(net) - ih(index_hedges)) ** 2
    idiosyncratic = (1.0 - RHO**2) * sum(x * x for x in net)
    misalignment = sum(hma(c) for c in counterparties)
    return math.sqrt(systematic + idiosyncratic + misalignment)


@dataclass(frozen=True)
class BACVAResult:
    k_reduced: float
    k_hedged: float | None
    k_full: float | None
    capital: float  # DS x K
    rwa: float  # 12.5 x capital (MAR50.1)


def ba_cva(counterparties: Sequence[Counterparty], index_hedges: Sequence[IndexHedge] = (), full: bool = False) -> BACVAResult:
    """Reduced: DS x K_reduced (MAR50.14). Full: DS x (beta K_reduced + (1 - beta) K_hedged) (MAR50.20)."""
    kr = k_reduced(counterparties)
    if not full:
        cap = DS_BA_CVA * kr
        return BACVAResult(kr, None, None, cap, 12.5 * cap)
    kh = k_hedged(counterparties, index_hedges)
    kf = BETA * kr + (1.0 - BETA) * kh
    cap = DS_BA_CVA * kf
    return BACVAResult(kr, kh, kf, cap, 12.5 * cap)


# ---------------------------------------------------------------------------
# SA-CVA aggregation (MAR50.51 to MAR50.53)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SACVASensitivity:
    factor: str
    bucket: str
    rw: float
    s_cva: float  # sensitivity of aggregate CVA (CVA as a positive loss, MAR50.32(1))
    s_hdg: float  # sensitivity of the market value of eligible hedges


Correlation = Callable[[SACVASensitivity, SACVASensitivity], float]
CrossBucketCorrelation = Callable[[str, str], float]


def sa_cva_bucket(sens: Sequence[SACVASensitivity], rho: Correlation) -> tuple[float, float]:
    """MAR50.53(1): K_b = sqrt(sum WS_k^2 + sum_{k != l} rho_kl WS_k WS_l + R sum (WS_k^Hdg)^2), WS_k = WS^CVA - WS^Hdg."""
    ws = [s.rw * s.s_cva - s.rw * s.s_hdg for s in sens]
    ws_hdg = [s.rw * s.s_hdg for s in sens]
    total = 0.0
    for i, wi in enumerate(ws):
        for j, wj in enumerate(ws):
            total += wi * wj if i == j else rho(sens[i], sens[j]) * wi * wj
    total += HEDGING_DISALLOWANCE_R * sum(w * w for w in ws_hdg)
    return math.sqrt(max(total, 0.0)), sum(ws)


def bucket_s(k_b: float, sum_ws: float) -> float:
    """MAR50.53(3): S_b = max(-K_b, min(sum_k WS_k, K_b))."""
    return max(-k_b, min(sum_ws, k_b))


def sa_cva_risk_class(buckets: dict[str, Sequence[SACVASensitivity]], rho: Correlation, gamma: CrossBucketCorrelation) -> float:
    """MAR50.53(2) to (3): K = m_CVA sqrt(sum K_b^2 + sum_{b != c} gamma_bc S_b S_c), S_b = max(-K_b, min(sum WS_k, K_b))."""
    kb: dict[str, float] = {}
    sb: dict[str, float] = {}
    for b, sens in buckets.items():
        kb[b], s = sa_cva_bucket(sens, rho)
        sb[b] = bucket_s(kb[b], s)
    total = sum(k * k for k in kb.values())
    for b in buckets:
        for c in buckets:
            if b != c:
                total += gamma(b, c) * sb[b] * sb[c]
    return M_CVA * math.sqrt(max(total, 0.0))


def ccs_rho(tenor_k: float, tenor_l: float, same_name: bool, legally_related: bool, same_quality: bool) -> float:
    """MAR50.65(4), buckets 1 to 7: rho = rho_tenor (100% or 90%) x rho_name (100/90/50%) x rho_quality (100% or 80%)."""
    r_tenor = 1.0 if tenor_k == tenor_l else 0.90
    r_name = 1.0 if same_name else 0.90 if legally_related else 0.50
    r_quality = 1.0 if same_quality else 0.80
    return r_tenor * r_name * r_quality


def run_tests() -> None:
    print("Basel CVA capital self-checks")
    q = quoted
    first = len(QUOTED_LOG)

    # Supervisory discount factor: DF(M) is the average of exp(-0.05 t) over [0, M].
    assert abs(supervisory_df(1.0) - (1 - math.exp(-0.05)) / 0.05) < 1e-15
    print("  Note 05, supervisory discount factor (card)")
    for m, df in ((1.0, 0.975), (5.0, 0.885), (10.0, 0.787)):
        q(f"DF at {m:g} years", supervisory_df(m), df, 3)

    # EADs from the CRE99 SA-CCR sample netting sets; M_NS is the notional-weighted maturity (CRE32.49).
    print("  Note 05, Example 1: reduced BA-CVA for three counterparties")
    p = cre99_portfolios()
    ead1, ead2, ead3 = (saccr_ead(p[k]).ead for k in ("ex1", "ex2", "ex3"))
    m1 = (10_000 * 10 + 10_000 * 4 + 5_000 * 11) / 25_000
    m2 = (10_000 * 3 + 10_000 * 6 + 10_000 * 5) / 30_000
    m3 = (10_000 * 0.75 + 20_000 * 2 + 10_000 * 5) / 40_000
    bank = Counterparty("Bank A (financial IG)", ba_cva_rw("financial", True), [NettingSetExposure(ead1, max(m1, 1.0))])
    corp = Counterparty("Corp B (industrial HY)", ba_cva_rw("basic_materials_energy_industrials", False), [NettingSetExposure(ead2, m2)])
    sov = Counterparty("Sovereign C (IG)", ba_cva_rw("sovereign", True), [NettingSetExposure(ead3, m3)])
    cps = [bank, corp, sov]
    scva = [stand_alone_cva(c) for c in cps]
    rows = (
        (bank, 569.5, 569.47, 7.8000, 0.828059, 5.0, 131.36),
        (corp, 381.2, 381.24, 4.6667, 0.891902, 7.0, 79.34),
        (sov, 5_405.6, 5_405.62, 2.4375, 0.941464, 0.5, 44.30),
    )
    for (c, ead_1dp, ead_2dp, m, df, rw, s_c), s in zip(rows, scva, strict=True):
        ns = c.netting_sets[0]
        q(f"{c.name} EAD", ns.ead, ead_1dp, 1)
        q(f"{c.name} EAD (2 dp)", ns.ead, ead_2dp, 2)
        q(f"{c.name} M_NS", ns.maturity, m, 4)
        q(f"{c.name} DF", supervisory_df(ns.maturity), df, 6)
        q(f"{c.name} RW (%)", c.rw * 100, rw, 1)
        q(f"{c.name} SCVA", s, s_c, 2)
    q("DF for Bank A, (1 - exp(-0.39)) / 0.39", (1 - math.exp(-0.39)) / 0.39, 0.828059, 6)
    total = sum(scva)
    sum_sq = sum(s * s for s in scva)
    q("sum SCVA", total, 255.00, 2)
    q("systematic term (rho sum SCVA)^2", (RHO * total) ** 2, 16_256.8, 1)
    q("sum SCVA^2", sum_sq, 25_513.5, 1)
    q("idiosyncratic term (1 - rho^2) sum SCVA^2", (1 - RHO**2) * sum_sq, 19_135.1, 1)
    q("K_reduced^2", (RHO * total) ** 2 + (1 - RHO**2) * sum_sq, 35_392.0, 1)
    red = ba_cva(cps)
    q("K_reduced", red.k_reduced, 188.13, 2)
    q("reduced BA-CVA capital", red.capital, 122.28, 2)
    q("reduced BA-CVA RWA", red.rwa, 1_528.5, 1)
    q("root-sum-square of SCVA", math.sqrt(sum_sq), 159.73, 2)
    # K_reduced lies between the zero-correlation root-sum-square and the plain sum of SCVA_c.
    assert math.sqrt(sum_sq) <= red.k_reduced <= total

    # Full BA-CVA: buy 5y protection directly on Bank A sized to its SCVA.
    print("  Note 05, Example 2: full BA-CVA with a direct and a proxy CDS")
    df5 = supervisory_df(5.0)
    q("DF at 5 years", df5, 0.884797, 6)
    b_direct = scva[0] / (0.05 * 5.0 * df5)  # notional whose SNH equals Bank A's SCVA
    q("direct CDS notional B", b_direct, 593.9, 1)
    hedged_bank = Counterparty(bank.name, bank.rw, bank.netting_sets, [SingleNameHedge(b_direct, 5.0, 0.05, "direct")])
    assert abs(snh(hedged_bank) - scva[0]) < 1e-9 and hma(hedged_bank) == 0.0
    full_direct = ba_cva([hedged_bank, corp, sov], full=True)
    q("unhedged SCVA_B + SCVA_C", scva[1] + scva[2], 123.64, 2)
    q("K_hedged, direct hedge", full_direct.k_hedged, 100.08, 2)
    q("K_full, direct hedge", full_direct.k_full, 122.09, 2)
    q("capital, direct hedge", full_direct.capital, 79.36, 2)
    q("capital reduction, direct hedge (%)", (1 - full_direct.capital / red.capital) * 100, 35, 0)
    # The beta floor: even a perfect hedge of everything leaves beta x K_reduced.
    assert full_direct.k_full >= BETA * full_direct.k_reduced
    # Same notional but a proxy name sharing sector and region (r = 50%): less offset and an HMA term.
    proxy_bank = Counterparty(bank.name, bank.rw, bank.netting_sets, [SingleNameHedge(b_direct, 5.0, 0.05, "sector_region")])
    full_proxy = ba_cva([proxy_bank, corp, sov], full=True)
    q("SNH, proxy hedge", snh(proxy_bank), 65.68, 2)
    q("HMA, proxy hedge", hma(proxy_bank), 12_941.9, 1)
    q("capital, proxy hedge", full_proxy.capital, 116.86, 2)
    q("capital reduction, proxy hedge (%)", (1 - full_proxy.capital / red.capital) * 100, 4, 0)
    assert full_proxy.capital > full_direct.capital
    # Every counterparty hedged directly and exactly: K_hedged = 0 and capital is the beta floor.
    all_hedged = [
        Counterparty(c.name, c.rw, c.netting_sets, [SingleNameHedge(s / (c.rw * 5.0 * df5), 5.0, c.rw, "direct")])
        for c, s in zip(cps, scva, strict=True)
    ]
    floor = ba_cva(all_hedged, full=True)
    assert abs(floor.k_hedged) < 1e-9
    q("capital with every counterparty hedged directly", floor.capital, 30.57, 2)
    q("beta floor 0.65 x 0.25 x K_reduced", DS_BA_CVA * BETA * red.k_reduced, 30.57, 2)

    # Index hedge: IG financials index, RW 5% x 0.7 (MAR50.24(4)(1)), 5y.
    # Sized so IH = rho x sum SCVA_c, it zeroes the systematic term; at 2,000 notional it over-hedges and capital rises.
    print("  Note 05, Example 3: index hedges and over-hedging")
    rw_index = 0.05 * 0.7
    q("index RW (%)", rw_index * 100, 3.5, 1)
    b_right = RHO * total / (rw_index * 5.0 * df5)
    right_hedge, over_hedge = IndexHedge(b_right, 5.0, rw_index), IndexHedge(2_000, 5.0, rw_index)
    q("IH = rho sum SCVA", ih([right_hedge]), 127.50, 2)
    q("IH = rho sum SCVA (card)", ih([right_hedge]), 127.5, 1)
    q("index notional for IH = rho sum SCVA", b_right, 823.4, 1)
    right = ba_cva(cps, [right_hedge], full=True)
    over = ba_cva(cps, [over_hedge], full=True)
    q("K_hedged, right-sized index", right.k_hedged, 138.33, 2)
    q("capital, right-sized index", right.capital, 98.01, 2)
    q("IH at notional 2,000", ih([over_hedge]), 309.68, 2)
    q("IH at notional 2,000 (card)", ih([over_hedge]), 309.7, 1)
    q("K_hedged, over-hedged", over.k_hedged, 228.74, 2)
    q("capital, over-hedged", over.capital, 142.08, 2)
    assert right.capital < red.capital < over.capital

    # SA-CVA: one counterparty credit spread bucket (financials, bucket 2, IG RW 5%), 5y tenor.
    # CVA spread sensitivity 10,000 per unit spread; a direct CDS hedge with sensitivity 10,000.
    print("  Note 05, Example 4: SA-CVA counterparty credit spread bucket")

    def rho(a: SACVASensitivity, b: SACVASensitivity) -> float:
        return ccs_rho(5.0, 5.0, a.factor == b.factor, False, True)

    unhedged = [SACVASensitivity("Bank A 5y", "2", 0.05, 10_000.0, 0.0)]
    hedged = [SACVASensitivity("Bank A 5y", "2", 0.05, 10_000.0, 10_000.0)]
    k_unh, ws_unh = sa_cva_bucket(unhedged, rho)
    k_hed, ws_hed = sa_cva_bucket(hedged, rho)
    q("WS unhedged", ws_unh, 500, 0)
    q("K_b unhedged", k_unh, 500, 0)
    q("WS with a direct CDS", ws_hed, 0, 0)
    q("K_b with a direct CDS", k_hed, 50, 0)
    q("K_b reduction from a perfect hedge (%)", (1 - k_hed / k_unh) * 100, 90, 0)
    q("sqrt(R) (%)", math.sqrt(HEDGING_DISALLOWANCE_R) * 100, 10, 0)

    # Two names in one bucket, same tenor and quality, unrelated names: rho = 1.0 x 0.5 x 1.0 = 0.5.
    two = [SACVASensitivity("Bank A 5y", "2", 0.05, 10_000.0, 0.0), SACVASensitivity("Bank B 5y", "2", 0.05, 0.0, 10_000.0)]
    q("rho for unrelated names, same tenor and quality", rho(two[0], two[1]), 0.5, 1)
    k_two, s_two = sa_cva_bucket(two, rho)
    q("K_b with a different-name hedge", k_two, 502.49, 2)
    assert abs(k_two - math.sqrt(500**2 + 500**2 - 2 * 0.5 * 500 * 500 + 0.01 * 500**2)) < 1e-9
    bucket3 = [SACVASensitivity("Corp 5y", "3", 0.03, 5_000.0, 0.0)]
    k3, ws3 = sa_cva_bucket(bucket3, rho)
    q("bucket 3 WS", ws3, 150, 0)
    q("bucket 3 K_b", k3, 150, 0)
    q("bucket 3 S_b", bucket_s(k3, ws3), 150, 0)
    q("bucket 2 S_b", bucket_s(k_two, s_two), 0, 0)
    k_class = sa_cva_risk_class({"2": two, "3": bucket3}, rho, lambda b, c: 0.05)
    q("SA-CVA counterparty credit spread delta K, gamma 5%", k_class, 524.40, 2)

    print(f"  {len(QUOTED_LOG) - first} numbers quoted in note 05 computed, printed and asserted")
    print("All Basel CVA checks passed.")


if __name__ == "__main__":
    run_tests()
