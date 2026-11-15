"""Case File 01: the 1929 crash, every number on the page.

Backs `16-Trading-and-Investing/20-History-and-Events/01-1929-Wall-Street-Crash-and-Great-Depression.md`.
Independent routes used here:
- each percentage decline is recomputed from the cited Dow closes in exact decimal arithmetic and checked
  against the quoted percentage, against the separately cited point change (close difference), and
  against the rounded figures published by the Brady Report (12.8 and 11.7 percent), and is printed
  beside Federal Reserve History's wording ("almost half", "nearly 13", "nearly 12");
- the FDIC suspension total is summed from the yearly counts and printed beside "about 9,000";
- the margin example is evaluated on an explicit balance sheet (assets minus debt) and checked against
  the leverage identity (a fall of 1/L wipes out equity at L times leverage).
Every quoted number is printed as ``label = value`` and asserted.
"""

from __future__ import annotations

from decimal import Decimal as D
from fractions import Fraction


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def exact(label: str, value: object, expected: object) -> None:
    assert value == expected, f"{label}: computed {value!r}, quoted {expected!r}"
    print(f"    {label} = {value}")


def pct_fall(old: D, new: D) -> float:
    return float((old - new) / old * 100)


def index_moves() -> None:
    print("Dow closes (cited)")
    peak, nov13, low32 = D("381.17"), D("198.69"), D("41.22")
    oct26, oct28, oct29 = D("298.97"), D("260.64"), D("230.07")
    approx("peak to Nov 13 1929 fall, Federal Reserve History 'almost half' (%)", pct_fall(peak, nov13), 47.87, 2)
    approx("peak to Jul 8 1932 fall (%)", pct_fall(peak, low32), 89.19, 2)
    # Point changes are cited separately; they must equal the close differences.
    exact("Oct 28 point change", oct26 - oct28, D("38.33"))
    exact("Oct 29 point change", oct28 - oct29, D("30.57"))
    approx("Oct 28 fall (%)", pct_fall(oct26, oct28), 12.82, 2)
    approx("Oct 28 fall, Brady rounding, Federal Reserve History 'nearly 13 percent' (%)", pct_fall(oct26, oct28), 12.8, 1)
    approx("Oct 29 fall (%)", pct_fall(oct28, oct29), 11.73, 2)
    approx("Oct 29 fall, Brady rounding, Federal Reserve History 'nearly 12 percent' (%)", pct_fall(oct28, oct29), 11.7, 1)
    # Six-fold rise from 63 (August 1921) to 381 (September 1929).
    approx("1921-1929 multiple", 381 / 63, 6.0, 0)


def bank_suspensions() -> None:
    print("FDIC bank suspensions 1930-1933")
    yearly = {1930: 1350, 1931: 2293, 1932: 1453, 1933: 4000}
    total = 0
    for year in sorted(yearly):
        total += yearly[year]
    exact("total 1930-1933, FDIC 'approximately 9,000'", total, 9096)


def margin_example() -> None:
    print("10% margin balance sheet (hypothetical)")
    s0, debt = Fraction(100), Fraction(90)
    equity0 = s0 - debt
    exact("initial equity", equity0, Fraction(10))
    leverage = s0 / equity0
    exact("leverage (x)", leverage, Fraction(10))
    # Price at which equity hits zero from the leverage identity, independent of the balance sheet.
    wipeout_fall = 1 / leverage
    exact("fall that wipes out equity", wipeout_fall, Fraction(1, 10))
    for price, quoted in ((Fraction(90), Fraction(0)), (Fraction(82), Fraction(-8))):
        assets = price
        exact(f"equity at S = {price}", assets - debt, quoted)
    exact("margin at S0 (%)", (s0 - debt) / s0 * 100, Fraction(10))


def main() -> None:
    index_moves()
    bank_suspensions()
    margin_example()
    print("all 1929 checks passed")


if __name__ == "__main__":
    main()
