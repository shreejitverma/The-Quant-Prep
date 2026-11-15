"""Case File 07: the 2015 SNB unpeg, every number on the page.

Backs `16-Trading-and-Investing/20-History-and-Events/07-2015-Swiss-Franc-Unpeg-and-Broker-Insolvency.md`.
Independent routes used here:
- the hypothetical account is computed in exact rational arithmetic (euro notional from the franc
  notional, P&L in francs) and the deficit multiple is checked against the leverage identity L*x - 1,
  where x is the percentage gap, which does not use the euro notional;
- the franc's appreciation is computed from a 30% EUR/CHF fall and checked by converting a CHF 1.20
  rate both ways (EUR/CHF and CHF/EUR).
Every quoted number is printed as ``label = value`` and asserted.
"""

from __future__ import annotations

from fractions import Fraction as F


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def account() -> None:
    print("Hypothetical CHF account at 200:1")
    deposit, lev = F(10_000), F(200)
    entry, stop, fill = F("1.2005"), F("1.1985"), F("1.0200")
    notional_chf = deposit * lev
    approx("notional (CHF)", float(notional_chf), 2_000_000.0, 0)
    notional_eur = notional_chf / entry
    approx("notional (EUR)", float(notional_eur), 1_665_972.51, 2)
    approx("margin (%)", float(1 / lev * 100), 0.50, 2)
    stop_loss = notional_eur * (entry - stop)
    approx("loss at stop (CHF)", float(stop_loss), 3_331.95, 2)
    approx("loss at stop (% of account)", float(stop_loss / deposit * 100), 33.32, 2)
    loss = notional_eur * (entry - fill)
    approx("price gap (CHF per EUR)", float(entry - fill), 0.1805, 4)
    approx("realized loss (CHF)", float(loss), 300_708.04, 2)
    equity = deposit - loss
    approx("equity after fill (CHF)", float(equity), -290_708.04, 2)
    gap = (entry - fill) / entry
    approx("gap (%)", float(gap * 100), 15.04, 2)
    deficit_multiple = -equity / deposit
    approx("deficit multiple of deposit", float(deficit_multiple), 29.07, 2)
    # Leverage identity: loss / deposit = L * gap, so the deficit multiple is L * gap - 1.
    assert deficit_multiple == lev * gap - 1, "deficit multiple must equal L*x - 1"
    print("Leverage identity at L = 200, gap 20%")
    loss_multiple = lev * F(20, 100)
    approx("loss multiple of deposit", float(loss_multiple), 40.0, 0)
    approx("deficit multiple of deposit", float(loss_multiple - 1), 39.0, 0)


def franc_move() -> None:
    print("EUR/CHF fall versus franc appreciation")
    fall = F(30, 100)
    rise = 1 / (1 - fall) - 1
    approx("franc rise for a 30% EUR/CHF fall (%)", float(rise * 100), 42.86, 2)
    eurchf_before, eurchf_after = F("1.20"), F("1.20") * (1 - fall)
    chfeur_rise = (1 / eurchf_after) / (1 / eurchf_before) - 1
    assert chfeur_rise == rise, "converting the rate both ways must agree"
    approx("EUR/CHF after a 30% fall", float(eurchf_after), 0.84, 2)


def main() -> None:
    account()
    franc_move()
    print("all SNB checks passed")


if __name__ == "__main__":
    main()
