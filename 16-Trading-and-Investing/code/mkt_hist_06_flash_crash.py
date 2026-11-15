"""Case File 06: the May 6, 2010 Flash Crash, every number on the page.

Backs `16-Trading-and-Investing/20-History-and-Events/06-2010-Flash-Crash-and-LOB-Evaporation.md`.
Independent routes used here:
- the average E-Mini level is implied from three separately cited contract-count and dollar-value pairs in
  the SEC-CFTC report (75,000 for $4.1bn, 35,000 for $1.9bn, 40,000 for $2.2bn); the three implied levels
  must agree with each other within the rounding of the dollar figures and sit near the cited low of 1056;
- the two pieces of the sell program (35,000 by 2:45 p.m. and the remaining 40,000 or so) must add up to
  the 75,000 total;
- the depth-impact multiple follows from the report's "less than 1% of morning depth".
Every quoted number is printed as ``label = value`` and asserted.
"""

from __future__ import annotations

MULTIPLIER = 50.0


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def implied_levels() -> None:
    print("Implied E-Mini levels from cited contract values")
    pairs = {"full program": (75_000, 4.1e9, 1093.33), "to 2:45 p.m.": (35_000, 1.9e9, 1085.71), "remainder": (40_000, 2.2e9, 1100.00)}
    levels = []
    for label, (contracts, dollars, quoted) in pairs.items():
        level = dollars / (contracts * MULTIPLIER)
        approx(f"implied level, {label}", level, quoted, 2)
        # The dollar figures are rounded to $0.1bn, so each level is only known to within that rounding.
        half_step = 0.05e9 / (contracts * MULTIPLIER)
        levels.append((level - half_step, level + half_step))
    lo = max(a for a, _ in levels)
    hi = min(b for _, b in levels)
    assert lo <= hi, f"implied levels inconsistent: intervals do not overlap ({lo}, {hi})"
    print(f"    common interval for the average level = [{lo:.2f}, {hi:.2f}]")
    assert lo > 1056, "average sale level must lie above the intraday low of 1056"
    assert pairs["to 2:45 p.m."][0] + pairs["remainder"][0] == pairs["full program"][0]


def depth_and_volume() -> None:
    print("Depth and volume shares (SEC-CFTC report)")
    depth_fraction = 0.01
    approx("impact multiple when depth falls to 1% of morning", 1 / depth_fraction, 100.0, 0)
    hft_hot_potato, share = 27_000, 0.49
    total = hft_hot_potato / share
    print(f"    implied total E-Mini volume 2:45:13-2:45:27 (contracts) = {total:,.0f}")
    assert 50_000 < total < 60_000


def main() -> None:
    implied_levels()
    depth_and_volume()
    print("all Flash Crash checks passed")


if __name__ == "__main__":
    main()
