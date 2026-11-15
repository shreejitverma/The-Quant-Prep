"""Case File 04: the dot-com bubble, every number on the page.

Backs `16-Trading-and-Investing/20-History-and-Events/04-2000-Dot-Com-Bubble-and-Telecom-Crash.md`.
Independent routes used here:
- the Nasdaq decline and the Netscape first-day gain are recomputed from the cited prices in exact
  decimal arithmetic;
- the FOMC tightening is summed from the six individual decisions (June 30, August 24 and November 16,
  1999; February 2, March 21 and May 16, 2000) and checked against the start and end targets;
- the Gordon multiples 1/(r - g) are checked against an explicit sum of discounted growing cash flows,
  truncated where the remaining tail is below 1e-12 of the total;
- the Barron's share "about a quarter" is checked from 51 of 207.
Every quoted number is printed as ``label = value`` and asserted.
"""

from __future__ import annotations

from decimal import Decimal as D


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def explicit_multiple(r: float, g: float) -> float:
    """Sum of (1+g)^(t-1) / (1+r)^t for t = 1.. until the term is negligible."""
    total, term, t = 0.0, 1.0 / (1.0 + r), 1
    q = (1.0 + g) / (1.0 + r)
    while term > 1e-14:
        total += term
        term *= q
        t += 1
    return total


def nasdaq_and_netscape() -> None:
    print("Nasdaq Composite and Netscape (cited prices)")
    peak, trough = D("5048.62"), D("1114.11")
    approx("Nasdaq peak-to-trough fall (%)", float((1 - trough / peak) * 100), 77.93, 2)
    approx("Netscape first-day gain over offer (%)", float((D("58.25") / D("28") - 1) * 100), 108.04, 2)
    approx("Barron's share of companies out of cash (%)", 51 / 207 * 100, 24.6, 1)
    assert 0.2 < 51 / 207 < 0.3, "'about a quarter'"


def fomc() -> None:
    print("FOMC federal funds target moves, June 1999 to May 2000 (bps)")
    moves = [25, 25, 25, 25, 25, 50]
    assert len(moves) == 6, "six increases"
    total = sum(moves)
    assert total == 175
    approx("start + moves (%)", 4.75 + total / 100, 6.50, 2)
    print(f"    total tightening (bps) = {total}")


def gordon() -> None:
    print("Gordon growth multiples (hypothetical inputs)")
    old_closed, new_closed = 1 / (0.16 - 0.15), 1 / (0.20 - 0.08)
    old_sum, new_sum = explicit_multiple(0.16, 0.15), explicit_multiple(0.20, 0.08)
    assert abs(old_closed - old_sum) / old_closed < 1e-9, f"{old_closed} vs {old_sum}"
    assert abs(new_closed - new_sum) / new_closed < 1e-9, f"{new_closed} vs {new_sum}"
    approx("old multiple", old_sum, 100.0, 1)
    approx("old spread (%)", (0.16 - 0.15) * 100, 1.0, 1)
    approx("new spread (%)", (0.20 - 0.08) * 100, 12.0, 1)
    approx("new multiple", new_sum, 8.33, 2)
    ratio = new_sum / old_sum
    approx("price ratio", ratio, 0.0833, 4)
    approx("price change (%)", (ratio - 1) * 100, -91.67, 2)


def main() -> None:
    nasdaq_and_netscape()
    fomc()
    gordon()
    print("all dot-com checks passed")


if __name__ == "__main__":
    main()
