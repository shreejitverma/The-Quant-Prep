"""Asset-based, liquidation and net-net valuation: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/Investing/Valuation Models/06-Asset-Based-Liquidation-and-Net-Net-Valuation.md`.
Independent routes used here:
- NCAV, NNWC and forced liquidation value in exact rational arithmetic (fractions.Fraction), with
  NCAV cross-checked as total assets minus fixed and intangible assets minus liabilities;
- the cash runway by a month-by-month simulation of the burn, against the closed-form ratio;
- the Graham and Dodd liquidating-value percentages applied in exact fractions at their low, average
  and high values;
- the Graham Number by exact squares, with the product rule P/E x P/B checked at the boundary.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_val_06_net_net.py`.
"""

from __future__ import annotations

from fractions import Fraction as F


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(float(value) - expected) <= tol, f"{label}: computed {float(value)!r}, quoted {expected}"
    print(f"    {label} = {float(value):.{decimals}f}")


CASH, TBILLS, AR, FG, WIP, PPE, GW = F(20), F(10), F(15), F(20), F(10), F(30), F(15)
LIAB = F(12) + F(8) + F(10)
SHARES, PRICE = F(10), F(7, 2)


def microtech() -> None:
    print("Worked case: MicroTech Hardware (cards mkt-val-161, mkt-val-163, mkt-val-166)")
    exact("market cap", SHARES * PRICE, 35)
    ca = CASH + TBILLS + AR + FG + WIP
    exact("current assets", ca, 75)
    exact("total assets", ca + PPE + GW, 120)
    exact("total liabilities", LIAB, 30)
    ncav = ca - LIAB
    exact("NCAV", ncav, 45)
    exact("NCAV by total assets less fixed and intangibles less liabilities", F(120) - PPE - GW - LIAB, 45)
    exact("NCAV per share", ncav / SHARES, F(9, 2))
    exact("two-thirds buy threshold", F(2, 3) * ncav / SHARES, 3)
    exact("margin of safety at two-thirds", 1 - F(2, 3), F(1, 3))
    approx("price / NCAV", PRICE / (ncav / SHARES), 0.78, 2)
    haircut = CASH + TBILLS + AR * F(3, 4) + FG * F(1, 2) + WIP * F(1, 10)
    exact("AR at 75%", AR * F(3, 4), F(45, 4))
    exact("haircut liquid assets", haircut, F(209, 4))
    nnwc = haircut - LIAB
    exact("NNWC", nnwc, F(89, 4))
    approx("NNWC per share", nnwc / SHARES, 2.225, 3)
    gross = haircut + PPE * F(1, 5)
    exact("gross liquidated cash", gross, F(233, 4))
    offbs = F(4) + 3 + 2
    exact("off-balance-sheet wind-down claims", offbs, 9)
    flv = gross - LIAB - offbs
    exact("net forced liquidation value", flv, F(77, 4))
    approx("FLV per share", flv / SHARES, 1.925, 3)


def runway() -> None:
    print("Worked case step 4 and Core concepts 6: burn-rate runway")
    net_cash, burn_m = 30.0 - 10.0, 1.2
    approx("annual burn", 12 * burn_m, 14.4, 1)
    approx("runway (years)", net_cash / (12 * burn_m), 1.39, 2)
    approx("runway (months)", net_cash / burn_m, 16.7, 1)
    # Independent route: burn month by month and count full months covered.
    cash, months = net_cash, 0
    while cash - burn_m >= -1e-9:
        cash -= burn_m
        months += 1
    exact("full months of runway (simulated)", months, 16)
    exact("NCAV 50 burned at 20 a year (years)", F(50) / 20, F(5, 2))


def graham_dodd() -> None:
    print("Card mkt-val-263: Graham and Dodd liquidating-value percentages applied to MicroTech")
    cash = CASH + TBILLS
    lines = {
        "average": (F(1), F(80, 100), F(2, 3), F(15, 100)),
        "low": (F(1), F(75, 100), F(50, 100), F(1, 100)),
        "high": (F(1), F(90, 100), F(75, 100), F(50, 100)),
    }
    quoted = {"average": (66.5, 3.65), "low": (56.55, 2.655), "high": (81.0, 5.10)}
    for name, (wc, wr, wi, wf) in lines.items():
        by_line = cash * wc + AR * wr + FG * wi + WIP * wi + PPE * wf
        approx(f"{name}: liquidating value of assets", by_line, quoted[name][0], 2)
        approx(f"{name}: per share after liabilities", (by_line - LIAB) / SHARES, quoted[name][1], 3)
    avg = cash + AR * F(80, 100) + (FG + WIP) * F(2, 3) + PPE * F(15, 100)
    approx("average, also less wind-down claims, per share", (avg - LIAB - 9) / SHARES, 2.75, 2)


def graham_number() -> None:
    print("Core concepts 5: Graham Number (card mkt-val-175)")
    exact("15 x 1.5", F(15) * F(3, 2), F(45, 2))
    # EPS 2, BVPS 20: sqrt(22.5 x 40) = 30 exactly because 30^2 = 900.
    exact("22.5 x 2 x 20", F(45, 2) * 2 * 20, 900)
    exact("30^2", 30 * 30, 900)
    exact("P/E at $30 with EPS 2", F(30, 2), 15)
    exact("P/B at $30 with BVPS 20", F(30, 20), F(3, 2))
    exact("22.5 x 1 x 40", F(45, 2) * 1 * 40, 900)
    exact("P/E at $30 with EPS 1", F(30, 1), 30)
    exact("P/B at $30 with BVPS 40", F(30, 40), F(3, 4))
    exact("product P/E x P/B at the boundary", F(30) * F(3, 4), F(45, 2))


if __name__ == "__main__":
    microtech()
    runway()
    graham_dodd()
    graham_number()
    print("all net-net numbers check out")
