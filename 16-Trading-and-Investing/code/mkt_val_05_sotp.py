"""Sum-of-the-parts and conglomerates: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/Investing/Valuation Models/05-Sum-of-the-Parts-and-Corporate-Conglomerates.md`.
Independent routes used here:
- the Titan Holdings SOTP in exact rational arithmetic (fractions.Fraction), with the capitalized overhead
  computed twice: as overhead x EBITDA-weighted multiple, and by charging each segment its EBITDA share
  of the overhead and valuing the net segment EBITDA at its own peer multiple;
- the 3Com / Palm per-share stub value from the closing prices and exchange ratio in Lamont and Thaler (2003);
  the -$22 billion total stub is quoted from the paper, not recomputed.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_val_05_sotp.py`.
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


def architecture() -> None:
    print("Core concepts 1 and 3: architecture diagram and overhead example")
    exact("SaaS segment EV 150 x 15", F(150) * 15, 2250)
    exact("hardware segment EV 150 x 7", F(150) * 7, 1050)
    exact("gross EV", F(2250) + 1050, 3300)
    exact("capitalized overhead 50 x 10", F(50) * 10, 500)


def titan() -> None:
    print("Worked case: Titan Holdings SOTP (cards mkt-val-131, mkt-val-132)")
    seg = [(F(120), F(14)), (F(180), F(11)), (F(150), F(11, 2))]
    evs = [e * m for e, m in seg]
    exact("segment EVs", evs, [1680, 1980, F(1650, 2)])
    gross = sum(evs)
    exact("gross segment EV", gross, F(4485))
    ebitda = sum(e for e, _ in seg)
    exact("sum of segment EBITDA", ebitda, 450)
    exact("sum of segment revenue", F(400) + 600 + 1000, 2000)
    w = gross / ebitda
    approx("EBITDA-weighted multiple", w, 9.97, 2)
    approx("EBITDA-weighted multiple (four decimals)", w, 9.9667, 4)
    overhead = 40 * w
    # Independent route: charge each segment its EBITDA share of overhead, value the remainder at its own multiple.
    net_by_segment = sum((e - 40 * e / ebitda) * m for e, m in seg)
    approx("net EV by charging overhead segment by segment", net_by_segment, 4086.3, 1)
    approx("capitalized overhead", overhead, 398.7, 1)
    net_ev = gross - overhead
    approx("net EV", net_ev, 4086.3, 1)
    net_debt = F(1200) - 200
    exact("net debt", net_debt, 1000)
    equity = net_ev - net_debt
    approx("equity value", equity, 3086.3, 1)
    approx("SOTP value per share", equity / 100, 30.86, 2)
    naive = gross - net_debt
    exact("naive equity value", naive, 3485)
    approx("naive value per share", naive / 100, 34.85, 2)
    approx("market premium to naive SOTP (percent)", 100 * (F(38) / (naive / 100) - 1), 9.0, 1)
    approx("market premium to clean SOTP (percent)", 100 * (F(38) / (equity / 100) - 1), 23.1, 1)
    exact("market cap", F(38) * 100, 3800)


def palm() -> None:
    print("Card mkt-val-154: 3Com / Palm stub on 2 March 2000 (Lamont and Thaler 2003)")
    ratio, palm_close, com_close = 1.525, 95.06, 81.81
    approx("Palm value per 3Com share", ratio * palm_close, 145.0, 1)
    approx("3Com stub value per share", com_close - ratio * palm_close, -63, 0)


if __name__ == "__main__":
    architecture()
    titan()
    palm()
    print("all SOTP numbers check out")
