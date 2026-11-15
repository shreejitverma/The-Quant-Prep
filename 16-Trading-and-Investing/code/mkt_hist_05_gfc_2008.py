"""Case File 05: the 2008 crisis and Lehman, every number on the page.

Backs `16-Trading-and-Investing/20-History-and-Events/05-2008-Global-Financial-Crisis-and-Lehman-Collapse.md`.
Independent routes used here:
- the hypothetical bank is evaluated line by line (assets, write-down, equity) in exact rational
  arithmetic, with the leverage threshold 1/L (equity is gone once losses reach A/L) beside it;
- the repo haircut collateral is computed in exact rational arithmetic as $100 / (1 - haircut);
- Lehman's leverage is recomputed from the Form 10-K figures in millions and compared with the reported 30.7x;
- the Dow and S&P 500 moves are recomputed from the cited closes in exact decimal arithmetic.
Every quoted number is printed as ``label = value`` and asserted.
"""

from __future__ import annotations

from decimal import Decimal as D
from fractions import Fraction


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def bank_example() -> None:
    print("Hypothetical investment bank ($bn)")
    assets, debt = Fraction(600), Fraction(580)
    equity = assets - debt
    assert equity == 20
    leverage = assets / equity
    approx("leverage (x)", float(leverage), 30.0, 0)
    sub = assets * Fraction(10, 100)
    approx("subprime-linked assets", float(sub), 60.0, 0)
    writedown = Fraction(35, 100) * sub
    approx("write-down", float(writedown), 21.0, 0)
    new_assets = assets - writedown
    approx("new assets", float(new_assets), 579.0, 0)
    new_equity = new_assets - debt
    approx("new equity", float(new_equity), -1.0, 0)
    approx("fall in total assets (%)", float(writedown / assets * 100), 3.5, 1)
    threshold = 1 / leverage
    approx("asset loss that wipes out equity (%)", float(threshold * 100), 3.33, 2)


def haircuts() -> None:
    print("Repo haircut collateral per $100 borrowed")
    for haircut, quoted in ((Fraction(25, 100), 133.33), (Fraction(2, 100), 102.04)):
        collateral = Fraction(100) / (1 - haircut)
        approx(f"collateral at {float(haircut) * 100:g}% haircut", float(collateral), quoted, 2)


def lehman_and_indices() -> None:
    print("Lehman Form 10-K fiscal 2007 ($m) and index closes")
    assets, equity = D("691063"), D("22490")
    lev = float(assets / equity)
    approx("Lehman leverage (x)", lev, 30.73, 2)
    approx("Lehman leverage as reported (x)", lev, 30.7, 1)
    approx("total assets ($bn)", float(assets) / 1000, 691.1, 1)
    approx("stockholders' equity ($bn)", float(equity) / 1000, 22.5, 1)
    approx("Q2 2008 total assets ($bn)", 639432 / 1000, 639.4, 1)
    prev, close = D("11421.99"), D("10917.51")
    assert prev - close == D("504.48"), "cited 504.48-point fall must equal the close difference"
    approx("Dow Sep 15 2008 fall (%)", float((prev - close) / prev * 100), 4.42, 2)
    approx("S&P 500 peak-to-trough fall (%)", float((1 - D("676.53") / D("1565.15")) * 100), 56.78, 2)


def main() -> None:
    bank_example()
    haircuts()
    lehman_and_indices()
    print("all 2008 checks passed")


if __name__ == "__main__":
    main()
