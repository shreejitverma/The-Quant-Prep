"""Numbers for 12-Microstructure-Problem-Set.md: one function per problem, each printed and asserted.

Run ``python problem_set.py``.
"""

from __future__ import annotations

import math


def check(label: str, value: float, expected: float, tol: float = 1e-9) -> float:
    """Print a labelled result and assert it is within tol of the expected value."""
    print(f"{label}: {value:.8g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected}"
    return value


def p01_roll() -> None:
    c = math.sqrt(0.0004)
    check("P1 Roll half-spread", c, 0.02)
    check("P1 Roll spread", 2 * c, 0.04)


def p02_gm() -> None:
    v_low, v_high, mu = 48.0, 52.0, 0.4
    half = mu * (v_high - v_low) / 2
    check("P2 GM half-spread", half, 0.8)
    check("P2 GM bid", 50 - half, 49.2)
    check("P2 GM ask", 50 + half, 50.8)
    sell_h, sell_l = (1 - mu) / 2, mu + (1 - mu) / 2
    p1 = 0.5 * sell_h / (0.5 * sell_h + 0.5 * sell_l)
    check("P3 P(H | one sell)", p1, 0.3)
    p2 = p1 * sell_h / (p1 * sell_h + (1 - p1) * sell_l)
    check("P3 P(H | two sells)", p2, 0.155172, 5e-7)
    check("P3 P(H | two sells) as 0.09 / 0.58", p2, 0.09 / 0.58, 1e-12)
    check("P3 next bid after one sell", v_low + (v_high - v_low) * p2, 48.62069, 5e-6)


def p04_kyle() -> None:
    sv, su = 1.5, 30_000.0
    lam = sv / (2 * su)
    check("P4 lambda", lam, 2.5e-5, 1e-15)
    check("P4 beta", su / sv, 20_000.0)
    check("P4 insider profit", sv * su / 2, 22_500.0)
    check("P4 price move for 10,000 net shares", lam * 10_000, 0.25)
    check("P5 lambda with 4x noise variance", sv / (2 * 2 * su), 1.25e-5, 1e-15)
    check("P5 profit with 4x noise variance", sv * 2 * su / 2, 45_000.0)
    check("P6 posterior sd with sigma_v = 2", math.sqrt(4 / 2), 1.414214, 5e-7)


def p07_impact() -> None:
    bp = 0.015 * math.sqrt(0.04) * 1e4
    check("P7 square-root impact (bp)", bp, 30.0)
    check("P7 ratio for 9% vs 4% ADV", math.sqrt(0.09 / 0.04), 1.5)
    check("P8 dollar cost of 200,000 x $40 at 30 bp", 200_000 * 40 * bp / 1e4, 24_000.0, 1e-6)
    check("P9 permanent impact under fair pricing (bp, peak 30)", 30 * 2 / 3, 20.0)
    check("P10 power-law beta=1/2 impact left at 4T (continuum)", math.sqrt(4) - math.sqrt(3), 0.267949, 5e-7)
    k = 0.142 * (0.2 / 0.4) ** 0.6 * 200
    check("P11 Almgren et al. temporary cost (bp)", k, 18.7370, 5e-5)


def p12_ac() -> None:
    lam, sigma, eta, x, t_end = 2e-6, 0.5, 1e-6, 500_000.0, 2.0
    kappa = math.sqrt(lam * sigma**2 / eta)
    check("P12 kappa (1/day)", kappa, 0.707107, 5e-7)
    frac = math.sinh(kappa * (t_end - 1)) / math.sinh(kappa * t_end)
    check("P12 fraction left after 1 day", frac, 0.396639, 5e-7)
    check("P12 TWAP fraction left after 1 day", 0.5, 0.5)
    check("P13 TWAP temporary cost eta X^2 / T", eta * x**2 / t_end, 125_000.0, 1e-6)
    check("P13 TWAP cost std sigma X sqrt(T/3)", sigma * x * math.sqrt(t_end / 3), 204_124.1, 0.05)


def p14_tca() -> None:
    delay = 40_000 * (30.05 - 30.00)
    execution = 40_000 * (30.20 - 30.05)
    opportunity = 10_000 * (30.40 - 30.00)
    fees = 40_000 * 0.004
    total = delay + execution + opportunity + fees
    check("P14 paper notional", 50_000 * 30.00, 1_500_000.0, 1e-6)
    check("P14 delay", delay, 2_000.0, 1e-6)
    check("P14 execution", execution, 6_000.0, 1e-6)
    check("P14 opportunity", opportunity, 4_000.0, 1e-6)
    check("P14 fees", fees, 160.0, 1e-9)
    check("P14 total shortfall", total, 12_160.0, 1e-6)
    check("P14 shortfall in bp of 1.5M", total / 1_500_000 * 1e4, 81.0667, 5e-5)
    others = (30.16 - 0.25 * 30.20) / 0.75
    check("P15 others' VWAP", others, 30.146667, 5e-7)
    check("P15 true slippage vs others (cents)", (30.20 - others) * 100, 5.3333, 5e-5)
    check("P16 POV 20% child vs 400,000 others", 0.2 / 0.8 * 400_000, 100_000.0, 1e-6)


def p17_fees() -> None:
    check("P17 maker round trip, 1c spread, 25-mil rebate ($/share)", 0.01 + 2 * 0.0025, 0.015)
    check("P17 per 100 shares ($)", 100 * (0.01 + 2 * 0.0025), 1.5)
    check("P18 all-in price, 30-mil taker venue", 10.05 + 0.003, 10.053)
    check("P18 all-in price, 10-mil taker rebate", 10.05 - 0.001, 10.049)
    check("P19 effective half-spread", 10.05 - 10.04, 0.01)
    check("P19 realized half-spread", 10.05 - 10.06, -0.01)
    check("P19 price impact", 10.06 - 10.04, 0.02)
    check("P20 relative tick on a $2 stock (bp)", 0.01 / 2 * 1e4, 50.0)
    check("P20 30-mil access fee on a $10 stock (bp)", 0.003 / 10 * 1e4, 3.0)


def p21_auction() -> None:
    buys = [(None, 300), (10.02, 1_000), (10.01, 500)]
    sells = [(10.00, 800), (10.01, 600), (10.03, 400)]
    rows = {}
    for p in (10.00, 10.01, 10.02, 10.03):
        d = sum(q for lim, q in buys if lim is None or lim >= p - 1e-12)
        s = sum(q for lim, q in sells if lim <= p + 1e-12)
        rows[p] = (d, s, min(d, s), d - s)
    want = {
        10.00: (1_800, 800, 800, 1_000),
        10.01: (1_800, 1_400, 1_400, 400),
        10.02: (1_300, 1_400, 1_300, -100),
        10.03: (300, 1_800, 300, -1_500),
    }
    assert rows == want, rows
    print("P21 table:", rows)
    best = max(rows, key=lambda p: (rows[p][2], -abs(rows[p][3])))
    check("P21 clearing price", best, 10.01)
    check("P21 volume", rows[best][2], 1_400, 0)
    check("P21 buy imbalance", rows[best][3], 400, 0)
    check("P21 volume at 10.02", rows[10.02][2], 1_300, 0)


def p22_latency() -> None:
    profit = (0.02 - 0.005) * 500
    check("P22 sniper profit", profit, 7.5)
    check("P22 maker expected loss with N = 4", profit * 3 / 4, 5.625)


def p23_misc() -> None:
    i = 300 / (300 + 900)
    check("P23 imbalance", i, 0.25)
    check("P23 weighted mid", i * 50.01 + (1 - i) * 50.00, 50.0025, 1e-9)
    check("P24 markout at 1 s (cents)", (20.005 - 20.00) * 100, 0.5, 1e-9)
    check("P24 markout at 60 s (cents)", (19.98 - 20.00) * 100, -2.0, 1e-9)
    avg = (200 * 15.01 + 300 * 15.02 + 500 * 15.03) / 1_000
    check("P25 ISO sweep average price", avg, 15.023, 1e-9)
    check("P26 Rule 201 trigger", 80 * 0.9, 72.0)
    check("P27 Roll estimate with rho = 0.6 as a share of c", 1 - 0.6, 0.4)
    phi, theta = 0.04, 0.06 - 0.04
    check("P28 transitory phi", phi, 0.04)
    check("P28 adverse selection theta", theta, 0.02, 1e-12)
    check("P28 adverse-selection share", theta / (theta + phi), 1 / 3, 1e-12)


if __name__ == "__main__":
    p01_roll()
    p02_gm()
    p04_kyle()
    p07_impact()
    p12_ac()
    p14_tca()
    p17_fees()
    p21_auction()
    p22_latency()
    p23_misc()
    print("all problem set checks passed")
