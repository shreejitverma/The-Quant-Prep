"""Case File 10: the 2022 UK LDI crisis, every number on the page.

Backs `16-Trading-and-Investing/20-History-and-Events/10-2022-UK-LDI-Pension-Crisis-and-Gilt-Spiral.md`.
Independent routes used here:
- the hypothetical LDI loss uses the first-order duration rule -N * D * dy, and the DV01 behind it is
  checked against a central finite difference of an exactly repriced zero-coupon position with duration 22;
  the exact (convex) repricing loss is printed and asserted as well;
- the Bank of England's stylised example (2x leverage, cushion half the gilts, gilts down about 30%) is
  checked on an explicit balance sheet;
- the gilt purchase total is checked against its conventional and index-linked components, and the
  operation's auction days are counted from the calendar (weekdays from September 28 to October 14, 2022);
- Liz Truss's days in office are counted from the dates of appointment and departure.
Every quoted number is printed as ``label = value`` and asserted.
"""

from __future__ import annotations

import datetime as dt
import math
from decimal import Decimal as D


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def zero_value(notional: float, duration: float, dy: float) -> float:
    """Value of a continuously compounded zero position worth `notional` today after a yield shift dy."""
    return notional * math.exp(-duration * dy)


def ldi_example() -> None:
    print("Hypothetical LDI position: GBP 1bn notional, duration 22, collateral GBP 200m")
    n, dur, collateral, dy = 1e9, 22.0, 200e6, 0.015
    h = 1e-6
    dv = -(zero_value(n, dur, h) - zero_value(n, dur, -h)) / (2 * h)
    assert abs(dv - n * dur) / (n * dur) < 1e-9, "finite-difference sensitivity must equal N*D"
    linear = -dv * dy
    approx("linear loss for +150 bp (GBP m)", -linear / 1e6, 330.0, 1)
    approx("collateral after linear loss (GBP m)", (collateral + linear) / 1e6, -130.0, 1)
    approx("leverage on collateral (x)", n / collateral, 5.0, 0)
    exact_loss = n - zero_value(n, dur, dy)
    approx("exact repricing loss (GBP m)", exact_loss / 1e6, 281.1, 1)
    approx("collateral after exact loss (GBP m)", (collateral - exact_loss) / 1e6, -81.1, 1)
    liquid = 30e6
    approx("shortfall after GBP 30m of liquid assets (GBP m)", (-(collateral + linear) - liquid) / 1e6, 100.0, 0)


def boe_stylised() -> None:
    print("Bank of England stylised LDI fund (letter of October 5, 2022)")
    gilts = D(100)
    borrowing = gilts / 2  # 2x leverage: half the gilts funded by repo
    cushion = gilts - borrowing
    print(f"    leverage (gilts / cushion) = {gilts / cushion}")
    fall = D("0.30")
    new_cushion = gilts * (1 - fall) - borrowing
    approx("cushion lost (%)", float((1 - new_cushion / cushion) * 100), 60.0, 0)


def boe_operation() -> None:
    print("Bank of England gilt operation, September 28 to October 14, 2022")
    conventional, index_linked = D("12.1"), D("7.2")
    assert conventional + index_linked == D("19.3"), "Quarterly Bulletin: GBP 19.3bn in total"
    print(f"    total purchases (GBP bn) = {conventional + index_linked}")
    days, day = 0, dt.date(2022, 9, 28)
    while day <= dt.date(2022, 10, 14):
        days += day.weekday() < 5
        day += dt.timedelta(days=1)
    assert days == 13
    print(f"    weekday auctions = {days}")
    approx("initial capacity at GBP 5bn per auction (GBP bn)", 5 * days, 65.0, 0)
    print("Yield moves cited in the letter (bps)")
    print("    Sep 23 rise in long gilt yields (Cunliffe letter, input) = 30")
    print("    Sep 26 rise in 30-year gilt yields (Cunliffe letter, input, 'around') = 50")
    print("    Sep 26 level above the start of Sep 23 (Cunliffe letter wording) = more than 80")
    morning_fall, evening_rise = 20, 67  # Sep 27: fall in the morning, rise by the evening vs the morning
    approx("Sep 27 net move vs the previous close (bps)", float(evening_rise - morning_fall), 47.0, 0)


def truss_days() -> None:
    print("Liz Truss in office")
    start, end = dt.date(2022, 9, 6), dt.date(2022, 10, 25)
    approx("days in office", float((end - start).days), 49.0, 0)


def main() -> None:
    ldi_example()
    boe_stylised()
    boe_operation()
    truss_days()
    print("all LDI checks passed")


if __name__ == "__main__":
    main()
