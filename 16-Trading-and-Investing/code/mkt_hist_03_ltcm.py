"""Case File 03: LTCM 1998, every number on the page.

Backs `16-Trading-and-Investing/20-History-and-Events/03-1998-LTCM-Collapse-and-Relative-Value-Arbitrage.md`.
Independent routes used here:
- the modified duration of a 30-year 5.5% semiannual par bond comes from the closed-form annuity
  expression (1/y)(1 - (1 + y/2)^-60) and is checked against a central finite difference of the explicit
  60-coupon price sum, which never uses the closed form;
- the hypothetical losses and sigma multiple follow from the stated inputs;
- the PWG and Federal Reserve History capital figures are recomputed in exact rational arithmetic and
  printed beside the sources' wording (leverage, "about fifteen percent", "44 percent", "over fifty
  percent", and the gross notional sum exceeding $1.4 trillion).
Every quoted number is printed as ``label = value`` and asserted.
"""

from __future__ import annotations

from fractions import Fraction


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def bond_price(y: float, coupon: float = 0.055, years: int = 30, face: float = 100.0) -> float:
    """Explicit sum of semiannual coupons and principal."""
    i = y / 2
    n = 2 * years
    pv = 0.0
    for k in range(1, n + 1):
        pv += face * coupon / 2 / (1 + i) ** k
    return pv + face / (1 + i) ** n


def duration() -> float:
    print("30-year par bond, 5.5% semiannual")
    y = 0.055
    closed = (1 / y) * (1 - (1 + y / 2) ** -60)
    h = 1e-6
    numeric = -(bond_price(y + h) - bond_price(y - h)) / (2 * h) / bond_price(y)
    assert abs(closed - numeric) < 1e-5, f"closed {closed} vs finite difference {numeric}"
    assert abs(bond_price(y) - 100.0) < 1e-9, "par bond must price at 100"
    approx("modified duration (closed form)", closed, 14.61, 2)
    approx("modified duration (finite difference)", numeric, 14.61, 2)
    return 14.61


def losses(d: float) -> None:
    print("Hypothetical convergence trade, N = $20bn")
    notional, sigma_bps = 20e9, 0.8
    move3 = 3 * sigma_bps
    approx("3-sigma move (bps)", move3, 2.4, 1)
    approx("3-sigma loss ($m)", notional * d * move3 / 1e4 / 1e6, 70.1, 1)
    approx("18 bp widening in sigmas", 18 / sigma_bps, 22.5, 1)
    approx("18 bp widening loss ($m)", notional * d * 18 / 1e4 / 1e6, 526.0, 1)


def fund_figures() -> None:
    print("PWG and Federal Reserve History figures")
    assets, eq_jan, eq_jul, aug_loss = Fraction(125), Fraction(48, 10), Fraction(41, 10), Fraction(18, 10)
    lev = assets / eq_jan
    approx("balance-sheet leverage, PWG 'more than 25-to-1' (x)", float(lev), 26.04, 2)
    eq_aug = eq_jul - aug_loss
    assert eq_aug == Fraction(23, 10), "PWG: $4.1bn less $1.8bn leaves $2.3bn"
    print(f"    end-August capital ($bn) = {float(eq_aug)}")
    jul_fall = float((1 - eq_jul / eq_jan) * 100)
    approx("fall to July 31, PWG 'about fifteen percent' (%)", jul_fall, 14.58, 2)
    aug_fall = float(aug_loss / eq_jul * 100)
    approx("August loss (%)", aug_fall, 43.90, 2)
    approx("August loss, Federal Reserve History rounding (%)", aug_fall, 44, 0)
    ytd = float((1 - eq_aug / eq_jan) * 100)
    approx("loss for the year at end-August, PWG 'over fifty percent' (%)", ytd, 52.08, 2)
    returned = Fraction(27, 10)
    cut = float(returned / (eq_jan + returned) * 100)
    assert abs(cut - 36) < 1, f"PWG: capital cut by about 36 percent, computed {cut:.2f}"
    print(f"    capital returned as share of pre-return base (%) = {cut:.2f}")
    gross = 500 + 750 + 150
    assert gross == 1400, "futures + swaps + options lower bounds"
    print(f"    gross notional lower bound ($bn) = {gross}")


def main() -> None:
    d = duration()
    losses(d)
    fund_figures()
    print("all LTCM checks passed")


if __name__ == "__main__":
    main()
