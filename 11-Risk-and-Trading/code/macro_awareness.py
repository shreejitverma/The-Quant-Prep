"""Macro and market awareness: the calculations a trader does when policy, inflation or growth news hits.

Backs every number in ``08-Macro-and-Market-Awareness.md``.
Run ``uv run --no-project --with numpy python 11-Risk-and-Trading/code/macro_awareness.py``;
each printed number is asserted, so drift in the note fails CI.

Section 1 uses the FOMC target-range history published by the Federal Reserve at
https://www.federalreserve.gov/monetarypolicy/openmarket.htm (retrieved 2026-10-17, page dated 2026-09-16).
Every other input (prices, yields, rates, vols, sensitivities) is hypothetical and chosen for the examples.
"""

from __future__ import annotations

import math

import numpy as np

# (year, month, day, change in bp, upper bound of the new range in percent), from the Fed page above
FOMC_CHANGES = [
    (2022, 3, 17, 25, 0.50),
    (2022, 5, 5, 50, 1.00),
    (2022, 6, 16, 75, 1.75),
    (2022, 7, 28, 75, 2.50),
    (2022, 9, 22, 75, 3.25),
    (2022, 11, 3, 75, 4.00),
    (2022, 12, 15, 50, 4.50),
    (2023, 2, 2, 25, 4.75),
    (2023, 3, 23, 25, 5.00),
    (2023, 5, 4, 25, 5.25),
    (2023, 7, 27, 25, 5.50),
    (2024, 9, 19, -50, 5.00),
    (2024, 11, 8, -25, 4.75),
    (2024, 12, 19, -25, 4.50),
    (2025, 9, 18, -25, 4.25),
    (2025, 10, 30, -25, 4.00),
    (2025, 12, 11, -25, 3.75),
    (2026, 9, 17, 25, 4.00),
]
START_UPPER = 0.25  # range 0-0.25 set on 2020-03-16


def check(name: str, value: float, expected: float, tol: float) -> float:
    """Print a named result and assert it is within ``tol`` of the value quoted in the note."""
    print(f"{name:<70s} {value:16.6f}")
    assert abs(value - expected) <= tol, f"{name}: got {value}, expected {expected} +/- {tol}"
    return value


def section_policy_history() -> None:
    """Backs the policy table in Core concepts, Example 1 and card risk-macro-hiking-cycle."""
    print("\n1. FOMC target range, 2022 to 2026 (Federal Reserve data)")
    level = START_UPPER
    for _, _, _, bp, upper in FOMC_CHANGES:
        level += bp / 100
        assert abs(level - upper) < 1e-9, "changes must chain to the published levels"
    hikes = [c for c in FOMC_CHANGES if c[0] in (2022, 2023)]
    check("2022-23 hiking cycle: number of hikes", len(hikes), 11, 0)
    check("2022-23 hiking cycle: total bp", sum(c[3] for c in hikes), 525, 0)
    check("2022-23 hiking cycle: 75 bp hikes", sum(1 for c in hikes if c[3] == 75), 4, 0)
    cuts = [c for c in FOMC_CHANGES if c[3] < 0]
    check("2024-25 easing: number of cuts", len(cuts), 6, 0)
    check("2024-25 easing: 50 bp cuts", sum(1 for c in cuts if c[3] == -50), 1, 0)
    check("2024-25 easing: total bp", -sum(c[3] for c in cuts), 175, 0)
    check("upper bound after the 2025-12-11 cut (percent)", START_UPPER + sum(c[3] for c in FOMC_CHANGES[:-1]) / 100, 3.75, 1e-9)
    check("upper bound after the 2026-09-17 change (percent)", START_UPPER + sum(c[3] for c in FOMC_CHANGES) / 100, 4.00, 1e-9)


def section_fed_funds_futures() -> None:
    """Backs Example 2 and card risk-macro-meeting-probability."""
    print("\n2. meeting probabilities from fed funds futures (hypothetical prices)")
    effr, days, meeting_day, price = 3.88, 30, 17, 96.165
    avg = check("implied average EFFR = 100 - price", 100 - price, 3.835, 1e-9)
    before, after = meeting_day - 1, days - meeting_day + 1  # new rate effective the day after the decision
    r1 = (avg * days - effr * before) / after
    check("days at the old rate", before, 16, 0)
    check("implied post-meeting rate", r1, 3.7836, 5e-5)
    check("implied change (bp)", (r1 - effr) * 100, -9.6429, 5e-4)
    check("implied probability of a 25 bp cut", -(r1 - effr) / 0.25, 0.3857, 5e-5)
    # sensitivity: the same price move means more when the meeting is late in the month
    late = (avg * days - effr * 27) / 3
    check("implied change if the new rate applied only from day 28 (bp)", (late - effr) * 100, -45.0, 1e-6)


def bond_price(y: float, coupon: float, years: int, freq: int = 2) -> float:
    n = years * freq
    c = 100 * coupon / freq
    d = 1 + y / freq
    return sum(c / d**k for k in range(1, n + 1)) + 100 / d**n


def section_bonds() -> None:
    """Backs Examples 3 and 4 and cards risk-macro-duration-convexity, risk-macro-dv01-steepener."""
    print("\n3. duration, convexity and a DV01-neutral curve trade (hypothetical par bonds)")
    y, h = 0.04, 1e-6
    p0 = bond_price(y, 0.04, 10)
    check("10y 4% bond price at 4%", p0, 100.0, 1e-9)
    dmod = -(bond_price(y + h, 0.04, 10) - bond_price(y - h, 0.04, 10)) / (2 * h) / p0
    conv = (bond_price(y + 1e-4, 0.04, 10) - 2 * p0 + bond_price(y - 1e-4, 0.04, 10)) / (1e-4**2 * p0)
    check("10y modified duration", dmod, 8.1757, 5e-5)
    check("10y convexity", conv, 78.90, 5e-3)
    dy = 0.0025
    exact = (bond_price(y + dy, 0.04, 10) / p0 - 1) * 100
    check("10y exact price change for +25 bp (percent)", exact, -2.0195, 5e-5)
    check("10y duration-only estimate (percent)", -dmod * dy * 100, -2.0439, 5e-5)
    check("10y duration + convexity estimate (percent)", (-dmod * dy + 0.5 * conv * dy**2) * 100, -2.0193, 5e-5)
    dv01_10 = check("10y DV01 (cents per 100 face)", dmod * p0 * 1e-4 * 100, 8.1757, 5e-5)
    p2 = bond_price(0.039, 0.039, 2)
    d2 = -(bond_price(0.039 + h, 0.039, 2) - bond_price(0.039 - h, 0.039, 2)) / (2 * h)
    dv01_2 = check("2y 3.9% par bond DV01 (cents per 100 face)", d2 * 1e-4 * 100, 1.9062, 5e-5)
    assert abs(p2 - 100) < 1e-9
    ratio = check("2y face per 1 of 10y face for DV01 neutrality", dv01_10 / dv01_2, 4.2891, 5e-4)
    # steepener: long 2y (ratio x face), short 10y (1 x face), per 10m 10y face
    face10 = 10_000_000
    face2 = ratio * face10
    dv = dv01_10 / 100 * face10 / 100  # dollars per bp on the 10y leg
    check("dollar DV01 per leg for 10m 10y face", dv, 8175.72, 0.005)
    # bear flattener: 2y +20 bp, 10y +5 bp -> steepener loses
    pnl = -face2 / 100 * dv01_2 / 100 * 20 + face10 / 100 * dv01_10 / 100 * 5
    check("steepener P&L in a bear flattener 2y +20, 10y +5 (dollars, linear)", pnl, -122_635.75, 0.005)
    check("same P&L as -DV01 x (change in 2s10s)", -dv * (20 - 5), -122_635.75, 0.005)


def section_fx_real_credit_equity() -> None:
    """Backs Example 5 and cards risk-macro-cip-forward, risk-macro-breakeven, risk-macro-credit-triangle,
    risk-macro-equity-duration, risk-macro-taylor.
    """
    print("\n4. FX forwards, real yields, credit spreads and equity duration (hypothetical)")
    s, r_usd, r_eur, days = 1.1000, 0.040, 0.020, 90
    fwd = s * (1 + r_usd * days / 360) / (1 + r_eur * days / 360)
    check("3m EURUSD forward by covered interest parity", fwd, 1.105473, 5e-7)
    check("forward points (pips)", (fwd - s) * 1e4, 54.7264, 5e-4)
    check("carry pick-up long USD vs EUR for 3 months (percent, simple)", (r_usd - r_eur) * days / 360 * 100, 0.5, 1e-12)
    nominal, real = 0.042, 0.019
    check("breakeven inflation, simple difference (percent)", (nominal - real) * 100, 2.3, 1e-9)
    check("breakeven inflation, Fisher exact (percent)", ((1 + nominal) / (1 + real) - 1) * 100, 2.2571, 5e-5)
    spread, rec = 0.015, 0.40
    lam = check("credit triangle hazard s / (1 - R) (percent)", spread / (1 - rec) * 100, 2.5, 1e-9)
    check("5y survival probability exp(-5 lambda)", math.exp(-5 * lam / 100), 0.8825, 5e-5)
    check("price change for +50 bp spread on spread duration 4.5 (percent)", -4.5 * 0.005 * 100, -2.25, 1e-12)
    r, g = 0.08, 0.04
    check("Gordon-growth equity duration 1 / (r - g)", 1 / (r - g), 25.0, 1e-9)
    check("exact price change for r +50 bp (percent)", ((r - g) / (r + 0.005 - g) - 1) * 100, -11.1111, 5e-5)
    check("linear duration estimate (percent)", -0.005 / (r - g) * 100, -12.5, 1e-9)
    # Taylor (1993): i = r* + pi + 0.5 (pi - 2) + 0.5 gap, r* = 2, target 2
    pi, gap = 3.0, -0.5
    check("Taylor (1993) rule rate with inflation 3 and gap -0.5", 2 + pi + 0.5 * (pi - 2) + 0.5 * gap, 5.25, 1e-12)


def section_event_vol() -> None:
    """Backs Example 6 and card risk-macro-event-vol."""
    print("\n5. implied event move from the options term structure (hypothetical vols)")
    iv_week, iv_base, n = 0.22, 0.16, 5
    var_event = iv_week**2 * n / 252 - iv_base**2 * (n - 1) / 252
    sd = check("event-day sd implied by 5-day IV 22% and base IV 16% (percent)", math.sqrt(var_event) * 100, 2.3537, 5e-5)
    check("expected absolute event move sd sqrt(2/pi) (percent)", sd * math.sqrt(2 / math.pi), 1.8779, 5e-5)
    check("a normal day's sd at 16% IV (percent)", iv_base / math.sqrt(252) * 100, 1.0079, 5e-5)
    check("event day as multiple of a normal day's variance", var_event / (iv_base**2 / 252), 5.4531, 5e-4)
    rng = np.random.default_rng(29)
    z = rng.standard_normal(1_000_000)
    check("simulated E|move| on event day (percent, seed 29)", float(np.mean(np.abs(sd * z))), 1.8769, 5e-4)


def section_book_shock() -> None:
    """Backs Example 7."""
    print("\n6. a hawkish surprise through a multi-asset book (hypothetical sensitivities and shocks)")
    book = {
        # name: (sensitivity, unit, shock)
        "2y rates DV01 (P&L per +1 bp)": (-50_000.0, 15.0),
        "10y rates DV01 (P&L per +1 bp)": (-20_000.0, 8.0),
        "long EUR 20m vs USD (P&L per +1% EURUSD)": (220_000.0, -0.8),
        "long 30m equity index, beta 1 (P&L per +1%)": (300_000.0, -1.2),
        "credit CS01 (P&L per +1 bp spread)": (-20_000.0, 5.0),
        "long vega (P&L per +1 vol point)": (40_000.0, 2.0),
    }
    pnl = {k: s * x for k, (s, x) in book.items()}
    for k, v in pnl.items():
        print(f"    {k:<50s} {v:14,.0f}")
    total = check("total scenario P&L (dollars)", sum(pnl.values()), -1_466_000.0, 1e-6)
    expected_lines = [-750_000.0, -160_000.0, -176_000.0, -360_000.0, -100_000.0, 80_000.0]
    for (k, v), e in zip(pnl.items(), expected_lines, strict=True):
        check(f"line: {k}", v, e, 1e-6)
    check("share of the loss from the front end (percent)", pnl["2y rates DV01 (P&L per +1 bp)"] / total * 100, 51.1596, 5e-4)
    # a hypothetical desk regression: 2y yield moves 8 bp per 0.1 pp core CPI surprise
    check("2y P&L for a +0.2 pp CPI surprise at 8 bp per 0.1 pp", -50_000 * 8 * 2, -800_000.0, 1e-6)


if __name__ == "__main__":
    section_policy_history()
    section_fed_funds_futures()
    section_bonds()
    section_fx_real_credit_equity()
    section_event_vol()
    section_book_shock()
    print("\nall checks passed")
