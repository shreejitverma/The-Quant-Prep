"""Inflation-linked products: TIPS reference CPI and index ratio, cash flows, deflation floor, breakevens, ZCIS, seasonality.

Backs every number in `06-Fixed-Income-and-Asset-Classes/21-Inflation-Linked-Products.md`.
- Example 1 and card fi-inflation-index-ratio: Ref CPI interpolation and Index Ratio under 31 CFR Part 356 Appendix B
  (truncate to six decimals, round to five), on published CPI-U values.
- Examples 2 and 3 and card fi-inflation-deflation-floor: coupon on the adjusted principal and the par floor at maturity
  (31 CFR 356.30).
- Example 4: exact and approximate Fisher breakeven.
- Example 5 and card fi-inflation-zcis-structure: zero-coupon inflation swap payoff and breakeven index ratio.
- Example 6 and card fi-inflation-seasonality-impact: month-on-month seasonality of non-seasonally adjusted CPI-U, 2006 to 2024.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_inflation.py`.
"""

from __future__ import annotations

import calendar
import math
import statistics

QUOTED: list[str] = []

# CPI-U, US city average, all items, not seasonally adjusted (BLS series CUUR0000SA0, 1982-84 = 100), as published by
# the BLS public API (retrieved 2026-10). TIPS and US inflation swaps reference this series.
CPI_U_NSA: dict[int, tuple[float, ...]] = {
    2005: (190.7, 191.8, 193.3, 194.6, 194.4, 194.5, 195.4, 196.4, 198.8, 199.2, 197.6, 196.8),
    2006: (198.3, 198.7, 199.8, 201.5, 202.5, 202.9, 203.5, 203.9, 202.9, 201.8, 201.5, 201.8),
    2007: (202.416, 203.499, 205.352, 206.686, 207.949, 208.352, 208.299, 207.917, 208.490, 208.936, 210.177, 210.036),
    2008: (211.080, 211.693, 213.528, 214.823, 216.632, 218.815, 219.964, 219.086, 218.783, 216.573, 212.425, 210.228),
    2009: (211.143, 212.193, 212.709, 213.240, 213.856, 215.693, 215.351, 215.834, 215.969, 216.177, 216.330, 215.949),
    2010: (216.687, 216.741, 217.631, 218.009, 218.178, 217.965, 218.011, 218.312, 218.439, 218.711, 218.803, 219.179),
    2011: (220.223, 221.309, 223.467, 224.906, 225.964, 225.722, 225.922, 226.545, 226.889, 226.421, 226.230, 225.672),
    2012: (226.665, 227.663, 229.392, 230.085, 229.815, 229.478, 229.104, 230.379, 231.407, 231.317, 230.221, 229.601),
    2013: (230.280, 232.166, 232.773, 232.531, 232.945, 233.504, 233.596, 233.877, 234.149, 233.546, 233.069, 233.049),
    2014: (233.916, 234.781, 236.293, 237.072, 237.900, 238.343, 238.250, 237.852, 238.031, 237.433, 236.151, 234.812),
    2015: (233.707, 234.722, 236.119, 236.599, 237.805, 238.638, 238.654, 238.316, 237.945, 237.838, 237.336, 236.525),
    2016: (236.916, 237.111, 238.132, 239.261, 240.229, 241.018, 240.628, 240.849, 241.428, 241.729, 241.353, 241.432),
    2017: (242.839, 243.603, 243.801, 244.524, 244.733, 244.955, 244.786, 245.519, 246.819, 246.663, 246.669, 246.524),
    2018: (247.867, 248.991, 249.554, 250.546, 251.588, 251.989, 252.006, 252.146, 252.439, 252.885, 252.038, 251.233),
    2019: (251.712, 252.776, 254.202, 255.548, 256.092, 256.143, 256.571, 256.558, 256.759, 257.346, 257.208, 256.974),
    2020: (257.971, 258.678, 258.115, 256.389, 256.394, 257.797, 259.101, 259.918, 260.280, 260.388, 260.229, 260.474),
    2021: (261.582, 263.014, 264.877, 267.054, 269.195, 271.696, 273.003, 273.567, 274.310, 276.589, 277.948, 278.802),
    2022: (281.148, 283.716, 287.504, 289.109, 292.296, 296.311, 296.276, 296.171, 296.808, 298.012, 297.711, 296.797),
    2023: (299.170, 300.840, 301.836, 303.363, 304.127, 305.109, 305.691, 307.026, 307.789, 307.671, 307.051, 306.746),
    2024: (308.417, 310.326, 312.332, 313.548, 314.069, 314.175, 314.540, 314.796, 315.301, 315.664, 315.493, 315.605),
}


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def cpi(year: int, month: int) -> float:
    while month < 1:
        year, month = year - 1, month + 12
    return CPI_U_NSA[year][month - 1]


def treasury_round(x: float) -> float:
    """31 CFR 356 Appendix B: truncate to six decimal places, then round to five."""
    truncated = math.floor(x * 1e6 + 1e-7) / 1e6
    return round(truncated, 5)


def ref_cpi(year: int, month: int, day: int) -> float:
    """Ref CPI for a date: CPI of the third preceding month, interpolated toward the second preceding month."""
    days_in_month = calendar.monthrange(year, month)[1]
    lo, hi = cpi(year, month - 3), cpi(year, month - 2)
    return treasury_round(lo + (day - 1) / days_in_month * (hi - lo))


def example1_ref_cpi() -> None:
    print("  1. Ref CPI and Index Ratio (Example 1, card fi-inflation-index-ratio)")
    quoted("CPI-U July 2024", cpi(2024, 7), 314.540, 3)
    quoted("CPI-U August 2024", cpi(2024, 8), 314.796, 3)
    quoted("CPI-U April 2024", cpi(2024, 4), 313.548, 3)
    quoted("CPI-U May 2024", cpi(2024, 5), 314.069, 3)
    quoted("August minus July", cpi(2024, 8) - cpi(2024, 7), 0.256, 3)
    ref_settle = ref_cpi(2024, 10, 16)
    quoted("Ref CPI for 16 October 2024", ref_settle, 314.66387, 5)
    ref_base = ref_cpi(2024, 7, 15)
    quoted("Ref CPI for 15 July 2024 (base)", ref_base, 313.78329, 5)
    quoted("Index Ratio", treasury_round(ref_settle / ref_base), 1.00281, 5)
    quoted("Ref CPI on the first of October 2024 = CPI July 2024", ref_cpi(2024, 10, 1), 314.54000, 5)


def example2_3_cash_flows() -> None:
    print("  2. TIPS coupon and the par floor (Examples 2 and 3, card fi-inflation-deflation-floor)")
    par, real_coupon = 1000.0, 0.020
    ratio_up = 315.0 / 300.0
    quoted("index ratio 315 / 300", ratio_up, 1.0500, 4)
    quoted("adjusted principal ($)", par * ratio_up, 1050.00, 2)
    quoted("semi-annual coupon ($)", real_coupon / 2.0 * par * ratio_up, 10.50, 2)
    quoted("final payment if maturing ($)", real_coupon / 2.0 * par * ratio_up + par * max(1.0, ratio_up), 1060.50, 2)
    ratio_down = 285.0 / 300.0
    quoted("index ratio 285 / 300", ratio_down, 0.9500, 4)
    final_coupon = real_coupon / 2.0 * par * ratio_down  # paid on the adjusted principal even when the floor binds
    quoted("final coupon ($)", final_coupon, 9.50, 2)
    quoted("principal with the floor ($)", par * max(1.0, ratio_down), 1000.00, 2)
    quoted("final payment ($)", final_coupon + par * max(1.0, ratio_down), 1009.50, 2)


def example4_breakeven() -> None:
    print("  3. Breakeven inflation (Example 4)")
    y_nom, y_real = 0.0425, 0.0185
    exact = (1.0 + y_nom) / (1.0 + y_real) - 1.0
    quoted("exact breakeven (%)", exact * 100.0, 2.3564, 4)
    quoted("approximate breakeven (%)", (y_nom - y_real) * 100.0, 2.4000, 4)
    quoted("approximation minus exact (bp)", (y_nom - y_real - exact) * 1e4, 4.36, 2)
    quoted("y_real x exact breakeven (bp)", y_real * exact * 1e4, 4.36, 2)


def example5_zcis() -> None:
    print("  4. Zero-coupon inflation swap (Example 5, card fi-inflation-zcis-structure)")
    notional, fixed, years = 10_000_000.0, 0.0240, 5
    fixed_leg = (1.0 + fixed) ** years
    quoted("(1 + K)^T", fixed_leg, 1.125900, 6)
    for ratio, expected in ((1.13, 41_000.93), (1.10, -258_999.07)):
        quoted(f"inflation receiver payoff at index ratio {ratio:.2f} ($)", notional * (ratio - fixed_leg), expected, 2)


def example6_seasonality() -> None:
    print("  5. Seasonality of NSA CPI-U, month-on-month, 2006 to 2024 (Example 6, card fi-inflation-seasonality-impact)")
    changes: dict[int, list[float]] = {m: [] for m in range(1, 13)}
    for year in range(2006, 2025):
        for month in range(1, 13):
            changes[month].append((cpi(year, month) / cpi(year, month - 1) - 1.0) * 100.0)
    means = {m: statistics.mean(v) for m, v in changes.items()}
    negatives = {m: sum(c < 0.0 for c in v) for m, v in changes.items()}
    expected_means = {1: 0.42, 2: 0.44, 3: 0.54, 11: -0.18, 12: -0.15}
    for m, e in expected_means.items():
        quoted(f"mean change {calendar.month_abbr[m]} (%)", means[m], e, 2)
    for m, e in {2: 0, 11: 14, 12: 13}.items():
        quoted(f"years with a fall in {calendar.month_abbr[m]} (of 19)", negatives[m], e, 0)
    quoted("sum of the 12 monthly means (%)", sum(means.values()), 2.50, 2)
    quoted("annualized CPI-U inflation Dec 2005 to Dec 2024 (%)", ((cpi(2024, 12) / cpi(2005, 12)) ** (1.0 / 19.0) - 1.0) * 100.0, 2.52, 2)
    quoted("March mean minus November mean (%)", means[3] - means[11], 0.72, 2)


def main() -> None:
    print("=== fi_inflation: Inflation-Linked Products ===")
    example1_ref_cpi()
    example2_3_cash_flows()
    example4_breakeven()
    example5_zcis()
    example6_seasonality()
    print(f"\nSuccessfully verified {len(QUOTED)} inflation figures.")


if __name__ == "__main__":
    main()
