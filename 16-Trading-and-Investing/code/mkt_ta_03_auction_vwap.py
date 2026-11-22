"""Auction theory, volume profile and anchored VWAP: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/03-Auction-Theory-Volume-Profile-and-VWAP.md`.
Independent routes used here:
- the value area by the single-level expansion rule stepped out explicitly, checked against a brute-force
  enumeration of every contiguous price range that contains the POC (the narrowest one holding at least 70%
  of volume, ties broken by larger volume), and contrasted with the two-row CBOT expansion rule;
- the normal-distribution facts behind the 70% convention by the error function (math.erf) and, separately,
  by Simpson quadrature of the normal density, with the 70% quantile found by bisection;
- the anchored VWAP in exact rational arithmetic (Fraction) and as a share-by-share average over an explicit
  array of every traded share's price (numpy), so the weighting itself is checked;
- the volume-weighted band formula by checking that the weighted variance equals the variance of the same
  expanded share-by-share array.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_ta_03_auction_vwap.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

LEVELS = [100, 105, 110, 115, 120, 125, 130]
VOLUME = [1_000, 3_000, 7_000, 15_000, 8_000, 4_000, 2_000]


def check(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{value:,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def expand(vol: list[int], target: float, rows: int) -> tuple[int, int, int, list[int]]:
    """Grow the value area from the POC, `rows` levels at a time on each side; return (lo, hi, volume, steps)."""
    poc = int(np.argmax(vol))
    lo = hi = poc
    total = vol[poc]
    steps = [total]
    while total < target:
        above = vol[hi + 1 : hi + 1 + rows]
        below = vol[max(0, lo - rows) : lo][::-1]
        if not above and not below:
            break
        if sum(above) >= sum(below) and above:
            hi += len(above)
            total += sum(above)
        else:
            lo -= len(below)
            total += sum(below)
        steps.append(total)
    return lo, hi, total, steps


def brute_force(vol: list[int], target: float) -> tuple[int, int, int]:
    poc = int(np.argmax(vol))
    best = None
    for lo in range(poc + 1):
        for hi in range(poc, len(vol)):
            v = sum(vol[lo : hi + 1])
            if v >= target:
                key = (hi - lo, -v)
                if best is None or key < best[0]:
                    best = (key, lo, hi, v)
    assert best is not None
    return best[1], best[2], best[3]


def value_area() -> None:
    print(f"input: Example 1 price ladder {LEVELS}")
    print(f"input: Example 1 volume at each level {VOLUME}")
    print("input: value area convention = 70% of session volume")
    total = sum(VOLUME)
    check("total session volume", total, "40,000")
    target = 0.70 * total
    check("70% value-area target", target, "28,000")
    poc = int(np.argmax(VOLUME))
    check("POC price", LEVELS[poc], "115")
    lo, hi, v, steps = expand(VOLUME, target, rows=1)
    check("single-level step 1 running volume", steps[1], "23,000")
    check("single-level running volume at stop", v, "30,000")
    check("single-level VAL", LEVELS[lo], "110")
    check("single-level VAH", LEVELS[hi], "120")
    blo, bhi, bv = brute_force(VOLUME, target)
    assert (blo, bhi, bv) == (lo, hi, v), "single-level rule should give the narrowest range here"
    lo2, hi2, v2, steps2 = expand(VOLUME, target, rows=2)
    vol_at = dict(zip(LEVELS, VOLUME, strict=True))
    check("two-row pair above (120 + 125)", vol_at[120] + vol_at[125], "12,000")
    check("two-row pair below (110 + 105)", vol_at[110] + vol_at[105], "10,000")
    check("two-row level above after the pair (130)", vol_at[130], "2,000")
    check("two-row step 1 running volume", steps2[1], "27,000")
    check("two-row running volume at stop", v2, "37,000")
    check("two-row VAL", LEVELS[lo2], "105")
    check("two-row VAH", LEVELS[hi2], "125")


# Market Profile chart in the note: each 30-minute bracket trades one contiguous price range (low, high).
CHART_TICKS = [101.0 + 0.5 * i for i in range(9)]
CHART_BRACKETS = {
    "A": (103.5, 105.0),
    "B": (102.5, 104.5),
    "C": (101.0, 104.0),
    "D": (102.0, 104.0),
    "E": (102.0, 103.5),
    "F": (102.5, 103.5),
    "G": (102.5, 103.0),
    "H": (102.5, 103.0),
    "I": (103.0, 103.0),
}


def tpo_chart() -> None:
    letters = {p: [b for b, (lo, hi) in CHART_BRACKETS.items() if lo <= p <= hi] for p in CHART_TICKS}
    for p in reversed(CHART_TICKS):
        print(f"chart row {p:.2f}: {' '.join(letters[p])}")
    counts = [len(letters[p]) for p in CHART_TICKS]
    # Independent count: one TPO per (bracket, tick) pair inside the bracket's range, tallied per bracket.
    per_bracket = sum(round((hi - lo) / 0.5) + 1 for lo, hi in CHART_BRACKETS.values())
    assert per_bracket == sum(counts)
    check("chart total TPOs", sum(counts), "33")
    target = 0.70 * sum(counts)
    check("chart 70% target (TPOs)", target, "23.1")
    poc = int(np.argmax(counts))
    assert counts.count(counts[poc]) == 1, "the chart POC must be unique"
    check("chart POC price", CHART_TICKS[poc], "103.00")
    check("chart POC TPOs", counts[poc], "8")
    lo, hi, v, steps = expand(counts, target, rows=1)
    assert [steps[i + 1] - steps[i] for i in range(len(steps) - 1)] == [7, 6, 4]
    check("chart value-area TPOs", v, "25")
    check("chart value-area share (%)", 100 * v / sum(counts), "75.8")
    check("chart VAL", CHART_TICKS[lo], "102.50")
    check("chart VAH", CHART_TICKS[hi], "104.00")
    assert brute_force(counts, target) == (lo, hi, v), "chart value area must be the narrowest range"
    tail = 0
    while counts[tail] == 1:
        tail += 1
    check("chart buying-tail single prints", tail, "2")
    assert counts[-1] == 1 and counts[-2] > 1, "the chart's top is one single print, not a tail"


def normal_mass(z: float) -> float:
    return math.erf(z / math.sqrt(2))


def simpson_mass(z: float, n: int = 2_000) -> float:
    x = np.linspace(-z, z, n + 1)
    f = np.exp(-0.5 * x**2) / math.sqrt(2 * math.pi)
    h = 2 * z / n
    return float(h / 3 * (f[0] + f[-1] + 4 * f[1:-1:2].sum() + 2 * f[2:-1:2].sum()))


def normal_facts() -> None:
    one_sigma = normal_mass(1.0)
    assert abs(one_sigma - simpson_mass(1.0)) < 1e-10
    check("normal mass within 1 sigma (%)", 100 * one_sigma, "68.27")
    lo, hi = 0.5, 1.5
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if normal_mass(mid) < 0.70 else (lo, mid)
    z70 = (lo + hi) / 2
    assert abs(simpson_mass(z70) - 0.70) < 1e-9
    check("z holding 70% of a normal", z70, "1.04")


def anchored_vwap() -> None:
    prices = [Fraction(200), Fraction(208), Fraction(204)]
    volumes = [5_000_000, 2_500_000, 1_500_000]
    print("input: Example 2 anchored VWAP days, prices $200, $208, $204 on 5,000,000, 2,500,000 and 1,500,000 shares")
    dollars = [p * v for p, v in zip(prices, volumes, strict=True)]
    check("day 1 dollar volume", float(dollars[0]), "1,000,000,000")
    check("day 2 dollar volume", float(dollars[1]), "520,000,000")
    check("day 3 dollar volume", float(dollars[2]), "306,000,000")
    check("cumulative dollar volume", float(sum(dollars)), "1,826,000,000")
    check("cumulative volume", sum(volumes), "9,000,000")
    avwap = sum(dollars) / sum(volumes)
    # Independent route: average over every share (scaled down 500x so the array stays small).
    per_share = np.repeat([200.0, 208.0, 204.0], [v // 500 for v in volumes])
    assert abs(per_share.mean() - float(avwap)) < 1e-9
    check("anchored VWAP ($)", float(avwap), "202.89")
    weighted_var = sum(v * (float(p) - float(avwap)) ** 2 for p, v in zip(prices, volumes, strict=True)) / sum(volumes)
    assert abs(weighted_var - per_share.var()) < 1e-9, "band sigma must equal the per-share standard deviation"
    print(f"volume-weighted sigma since anchor = {math.sqrt(weighted_var):.4f}")
    print("cited: Example 2 pullback level $203.00 (hypothetical input, near the anchored VWAP)")
    print("cited: Market Profile conventions, 30-minute TPO brackets, the '80% Rule' (a name, not a tested probability)")
    print("cited: 24-hour electronic sessions; Market Profile chart price ladder 101.00 to 105.00 is illustrative")


if __name__ == "__main__":
    value_area()
    tpo_chart()
    normal_facts()
    anchored_vwap()
    print("all auction-theory numbers check out")
