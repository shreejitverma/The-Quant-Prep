"""XVA: unilateral and bilateral CVA, DVA, wrong-way risk, FVA, MVA and KVA on a simulated swap.

Backs every number in 11-Risk-and-Trading/15-XVA.md (and problems in 17-Risk-Problem-Set.md).

Exposure comes from risk_ccr_analytics.py: a 10m 5-year quarterly payer swap at par under a one-factor Hull-White model
(upward-sloping zero curve from 2% to about 3.2% at 5 years, mean reversion 5%, volatility 1%), 50,000 paths,
quarterly grid.  Discounted EE and ENE are also available in closed form (Jamshidian swaption prices), which gives a
semi-analytic CVA to check the Monte Carlo.
Credit curves are flat hazard rates; recoveries, spreads, cost of capital and the counterparty's sector are labelled
illustrative inputs.  Wrong-way risk uses the Hull and White (2012) hazard-rate model lambda(t) = exp(a(t) + b V(t)),
recalibrating a(t) so the survival curve is unchanged: only b moves between runs.
Capital for KVA is SA-CCR (CRE52) for the counterparty credit charge plus reduced BA-CVA (MAR50.14 to MAR50.16).

Run: python 11-Risk-and-Trading/code/risk_xva_pricing.py
"""

from __future__ import annotations

import math

import numpy as np
from risk_ccr_analytics import GRID, HW, N_PATHS, Swap, profile, simulate_book, swap_book

Z99 = 2.3263478740408408
LAM_C, LGD_C = 0.025, 0.60  # counterparty: flat hazard 2.5%, so a CDS spread of about 150bp
LAM_B, LGD_B = 0.015, 0.60  # bank: flat hazard 1.5%, about 90bp
NOTIONAL = 10e6


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a value and assert it matches the literal quoted in the note to within tol (absolute)."""
    print(f"  {label}: {value:.10g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, note quotes {expected} (tol {tol})"
    return value


def surv(lam: float, t: np.ndarray) -> np.ndarray:
    return np.exp(-lam * t)


def cva_from_dee(dee: np.ndarray, lam: float, lgd: float, other_lam: float = 0.0) -> float:
    """LGD x sum over intervals of the average discounted EE times the default probability in the interval; with
    other_lam > 0 each interval is also weighted by the other party's survival at its midpoint (first-to-default)."""
    s = surv(lam, GRID)
    mid = 0.5 * (GRID[1:] + GRID[:-1])
    weight = surv(other_lam, mid) if other_lam > 0.0 else np.ones(len(mid))
    return float(lgd * np.sum(0.5 * (dee[1:] + dee[:-1]) * (s[:-1] - s[1:]) * weight))


def funding_integral(profile_: np.ndarray, spread: float, lam_c: float = 0.0, lam_b: float = 0.0) -> float:
    """spread x integral of a discounted profile over time (trapezoid), optionally weighted by both survivals."""
    mid = 0.5 * (GRID[1:] + GRID[:-1])
    w = surv(lam_c, mid) * surv(lam_b, mid)
    return float(spread * np.sum(0.5 * (profile_[1:] + profile_[:-1]) * np.diff(GRID) * w))


def annuity0() -> float:
    prev, ann = 0.0, 0.0
    for d in [0.25 * i for i in range(1, 21)]:
        ann += (d - prev) * float(HW.p0(d))
        prev = d
    return ann


# ---------------------------------------------------------------------------
# Worked example 1: unilateral and bilateral CVA, DVA (cards risk-unilateral-vs-bilateral-cva, risk-cva-semi-analytic-check,
# risk-credit-triangle-cva, risk-dva-paradox-explanation, risk-xva-unilateral-vs-bilateral-integral, risk-cva-credit-spread-delta-hedging)
# ---------------------------------------------------------------------------


def section_cva_dva(sim: dict[str, np.ndarray]) -> dict[str, float]:
    print("\n[Worked example 1: CVA and DVA of the 10m 5y payer swap]")
    disc = sim["disc"]
    prof = profile(sim["v5"], disc, GRID)
    payer5, _ = swap_book()
    receiver_twin = Swap(payer5.notional, payer5.fixed, payer5.pay_dates, payer=False)
    dee_cf = np.array([payer5.swaption_today(HW, t) for t in GRID])
    dene_cf = np.array([receiver_twin.swaption_today(HW, t) for t in GRID])
    check("hazard 2.5% x LGD 60% = spread (bp)", LAM_C * LGD_C * 1e4, 150.0, 1e-9)
    check("counterparty 5y default probability", 1.0 - math.exp(-LAM_C * 5.0), 0.117503, 5e-7)
    check("bank 5y default probability", 1.0 - math.exp(-LAM_B * 5.0), 0.072257, 5e-7)
    cva_cf = cva_from_dee(dee_cf, LAM_C, LGD_C)
    dva_cf = cva_from_dee(dene_cf, LAM_B, LGD_B)
    cva_mc = cva_from_dee(prof.dee, LAM_C, LGD_C)
    dva_mc = cva_from_dee(prof.dene, LAM_B, LGD_B)
    check("unilateral CVA, semi-analytic (Jamshidian EE)", cva_cf, 8_994, 1.0)
    check("unilateral CVA, Monte Carlo (about)", cva_mc, 8_965, 30)
    check("DVA, semi-analytic", dva_cf, 2_925, 1.0)
    check("DVA, Monte Carlo (about)", dva_mc, 2_934, 20)
    check("Monte Carlo minus semi-analytic CVA, relative", cva_mc / cva_cf - 1.0, -0.0032, 5e-4)
    check("bilateral (CVA - DVA), semi-analytic", cva_cf - dva_cf, 6_069, 1.0)
    cva_ftd = cva_from_dee(dee_cf, LAM_C, LGD_C, other_lam=LAM_B)
    dva_ftd = cva_from_dee(dene_cf, LAM_B, LGD_B, other_lam=LAM_C)
    check("first-to-default CVA", cva_ftd, 8_712, 1.0)
    check("first-to-default DVA", dva_ftd, 2_778, 1.0)
    check("first-to-default bilateral", cva_ftd - dva_ftd, 5_934, 1.0)
    tri = funding_integral(dee_cf, LAM_C * LGD_C)
    check("credit-triangle approximation: spread x integral of discounted EE", tri, 9_491, 1.0)
    check("credit-triangle approximation / CVA - 1", tri / cva_cf - 1.0, 0.055, 5e-4)
    cs01 = cva_from_dee(dee_cf, LAM_C + 0.0001 / LGD_C, LGD_C) - cva_cf
    check("CVA change for +1bp counterparty spread", cs01, 56.74, 0.01)
    dva_wide = cva_from_dee(dene_cf, 0.05, LGD_B)
    check("DVA with the bank's hazard at 5% (about 300bp)", dva_wide, 9_074, 1.0)
    check("DVA gain from the bank's own widening", dva_wide - dva_cf, 6_149, 1.0)
    ann = annuity0()
    check("annuity, sum tau P(0, t_i)", ann, 4.6295, 5e-4)
    check("bilateral adjustment as running spread (bp)", (cva_cf - dva_cf) / (NOTIONAL * ann) * 1e4, 1.31, 0.005)
    return {"cva": cva_cf, "dva": dva_cf, "dee": dee_cf, "dene": dene_cf}


# ---------------------------------------------------------------------------
# Worked example 2: wrong-way risk with the survival curve held fixed (cards risk-wrong-way-risk-classification,
# risk-wwr-hull-white-control)
# ---------------------------------------------------------------------------


def cva_hazard_model(sim: dict[str, np.ndarray], b: float) -> tuple[float, float]:
    """Hull and White (2012): lambda_k = exp(a_k + b V(t_k-1) / N) on each interval; a_k is solved so that the average
    survival matches exp(-LAM_C t_k).  Exposure is taken at the end of the interval.  Returns (CVA, max calibration error)."""
    v, disc = sim["v5"], sim["disc"]
    n_paths = v.shape[1]
    s_path = np.ones(n_paths)
    cva, worst = 0.0, 0.0
    for k in range(1, len(GRID)):
        dt = GRID[k] - GRID[k - 1]
        target = math.exp(-LAM_C * GRID[k])
        driver = b * v[k - 1] / NOTIONAL
        lo, hi = -30.0, 5.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if float(np.mean(s_path * np.exp(-np.exp(mid + driver) * dt))) > target:
                lo = mid
            else:
                hi = mid
        a_k = 0.5 * (lo + hi)
        s_new = s_path * np.exp(-np.exp(a_k + driver) * dt)
        worst = max(worst, abs(float(s_new.mean()) - target))
        cva += LGD_C * float(np.mean(disc[k] * np.maximum(v[k], 0.0) * (s_path - s_new)))
        s_path = s_new
    return cva, worst


def section_wwr(sim: dict[str, np.ndarray]) -> None:
    print("\n[Worked example 2: wrong-way risk, lambda = exp(a(t) + b V / N), survival curve recalibrated for each b]")
    disc, v = sim["disc"], sim["v5"]
    s = surv(LAM_C, GRID)
    indep = LGD_C * sum(float(np.mean(disc[k] * np.maximum(v[k], 0.0))) * (s[k - 1] - s[k]) for k in range(1, len(GRID)))
    res = {}
    for b in (-20.0, 0.0, 20.0, 40.0):
        res[b] = cva_hazard_model(sim, b)
        print(f"  b = {b:+.0f}: CVA {res[b][0]:,.0f} (calibration error {res[b][1]:.1e})")
    check("b = 0 reproduces the independent CVA (same discretisation), relative gap", res[0.0][0] / indep - 1.0, 0.0, 1e-6)
    check("independent CVA, end-of-interval exposure (about)", indep, 8_990, 40)
    check("right-way, b = -20 (about)", res[-20.0][0], 4_870, 40)
    check("wrong-way, b = +20 (about)", res[20.0][0], 14_510, 60)
    check("wrong-way, b = +40 (about)", res[40.0][0], 20_310, 80)
    check("ratio b = +40 to independent (about)", res[40.0][0] / indep, 2.26, 0.01)
    check("largest calibration error of the survival curve", max(r[1] for r in res.values()), 0.0, 1e-10)


# ---------------------------------------------------------------------------
# Worked example 3: FVA, the FBA-DVA overlap, MVA and KVA (cards risk-fva-mechanics-dealer, risk-fca-vs-fba-asymmetry,
# risk-mva-calculation-driver, risk-kva-cost-of-capital-driver, risk-xva-running-spread, risk-fca-vs-fba-asymmetric-pricing,
# risk-kva-capital-hurdle-coc, risk-isda-simm-mva-sensitivities-driver)
# ---------------------------------------------------------------------------


def im_profile(sim: dict[str, np.ndarray], mpor_days: int = 10) -> np.ndarray:
    """Delta-normal initial margin proxy: 99% one-tailed over the MPOR (MGN20.9), IM = z99 |dV/dx| sd(x over 10 days).
    A labelled stand-in for ISDA SIMM, which aggregates prescribed sensitivities and risk weights instead."""
    payer5, _ = swap_book()
    x = sim["x"]
    d = mpor_days / 250.0
    sd_x = HW.sigma * math.sqrt((1.0 - math.exp(-2.0 * HW.a * d)) / (2.0 * HW.a))
    h = 1e-6
    im = np.zeros_like(x)
    for k, t in enumerate(GRID):
        dv = (payer5.value_at_reset(HW, t, x[k] + h) - payer5.value_at_reset(HW, t, x[k] - h)) / (2 * h)
        im[k] = Z99 * np.abs(dv) * sd_x
    return im


def saccr_ead_paths(v: np.ndarray) -> np.ndarray:
    """SA-CCR EAD of the single unmargined payer swap on each path and date (CRE52.10, CRE52.20 to CRE52.23, CRE52.34,
    CRE52.48): delta +1 (receive floating is long rates), maturity factor sqrt(min(M, 1)), M and SD floored at 10 days."""
    ead = np.zeros_like(v)
    for k, t in enumerate(GRID):
        m = max(5.0 - t, 10.0 / 250.0)
        if 5.0 - t <= 1e-12:
            continue
        sd = max((1.0 - math.exp(-0.05 * (5.0 - t))) / 0.05, 10.0 / 250.0)
        addon = 0.005 * NOTIONAL * sd * math.sqrt(min(m, 1.0))
        mult = np.minimum(1.0, 0.05 + 0.95 * np.exp(v[k] / (2.0 * 0.95 * addon)))
        ead[k] = 1.4 * (np.maximum(v[k], 0.0) + mult * addon)
    return ead


def section_funding_capital(sim: dict[str, np.ndarray], base: dict[str, float]) -> None:
    print("\n[Worked example 3: FVA, MVA, KVA]")
    disc = sim["disc"]
    s_f = 0.0080  # unsecured funding spread over the collateral rate
    fca = funding_integral(base["dee"], s_f)
    fba = funding_integral(base["dene"], s_f)
    check("FCA, 80bp on discounted EE", fca, 5_062, 1.0)
    check("FBA, 80bp on discounted ENE", fba, 2_683, 1.0)
    check("symmetric FVA = FCA - FBA", fca - fba, 2_379, 1.0)
    fca_s = funding_integral(base["dee"], s_f, LAM_C, LAM_B)
    check("FCA weighted by both survivals", fca_s, 4_647, 1.0)
    fba_own = funding_integral(base["dene"], LAM_B * LGD_B, lam_b=LAM_B)
    check("FBA at the bank's own credit spread, own-survival weighted", fba_own, 2_925, 1.0)
    # The two continuous integrals are identical; this checks only that the two quadratures agree.
    check("same, relative to DVA, minus 1", fba_own / base["dva"] - 1.0, 0.0, 1e-6)

    im = im_profile(sim)
    dim = (disc * im).mean(axis=1)
    check("initial margin today, delta-normal proxy", float(im[0].mean()), 191_334, 1.0)
    check("MGN20.16 schedule IM, 2% of notional (2-5 year duration)", 0.02 * NOTIONAL, 200_000, 0.0)
    check("expected discounted IM at 2.5y (about)", float(dim[10]), 97_300, 300)
    s_im = 0.0080
    mva = funding_integral(dim, s_im)
    check("MVA, 80bp on expected discounted IM (about)", mva, 3_871, 10)

    ead = saccr_ead_paths(sim["v5"])
    k_ccr = 0.08 * 1.0 * ead  # 100% risk weight (unrated corporate), 8% minimum
    m_eff = np.array([max(5.0 - t, 1.0) for t in GRID])
    df = (1.0 - np.exp(-0.05 * m_eff)) / (0.05 * m_eff)
    scva = (1.0 / 1.4) * 0.03 * (m_eff * df)[:, None] * ead  # MAR50.16: consumer goods and services, IG: 3%
    k_cva = 0.65 * scva  # one counterparty: K_reduced = SCVA
    cap = k_ccr + k_cva
    dcap = (disc * cap).mean(axis=1)
    check("SA-CCR EAD today", float(ead[0].mean()), 309_679, 1.0)
    check("CCR capital today", float(k_ccr[0].mean()), 24_774, 1.0)
    check("BA-CVA capital today", float(k_cva[0].mean()), 19_082, 1.0)
    coc = 0.10
    kva = funding_integral(dcap, coc)
    check("KVA at a 10% hurdle (about)", kva, 18_130, 60)
    total = base["cva"] - base["dva"] + (fca - fba) + mva + kva
    check("total XVA charge (about)", total, 30_450, 100)
    check("as running spread (bp, about)", total / (NOTIONAL * annuity0()) * 1e4, 6.58, 0.02)


# ---------------------------------------------------------------------------
# Core concepts "Incremental XVA" (cards risk-incremental-xva-pricing, risk-pre-trade-incremental-xva-workflow)
# ---------------------------------------------------------------------------


def section_incremental(sim: dict[str, np.ndarray]) -> None:
    print("\n[Incremental CVA of adding the 2y receiver swap to the netting set]")
    net = profile(sim["v5"] + sim["v2"], sim["disc"], GRID)
    alone = profile(sim["v5"], sim["disc"], GRID)
    two = profile(sim["v2"], sim["disc"], GRID)
    c_net = cva_from_dee(net.dee, LAM_C, LGD_C)
    c5 = cva_from_dee(alone.dee, LAM_C, LGD_C)
    c2 = cva_from_dee(two.dee, LAM_C, LGD_C)
    check("CVA of the netting set after the trade (about)", c_net, 7_870, 30)
    check("incremental CVA of the 2y receiver (about)", c_net - c5, -1_100, 15)
    check("stand-alone CVA of the 2y receiver (about)", c2, 528, 10)


def main() -> None:
    sim = simulate_book()
    assert sim["v5"].shape == (len(GRID), N_PATHS)
    base = section_cva_dva(sim)
    section_wwr(sim)
    section_funding_capital(sim, base)
    section_incremental(sim)
    print("\nAll XVA checks passed.")


if __name__ == "__main__":
    main()
