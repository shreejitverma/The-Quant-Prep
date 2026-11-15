"""Klarman and distressed debt: every computed number in the note.

Backs `16-Trading-and-Investing/Investing/Value Investing/05-Klarman-Margin-of-Safety-and-Distressed-Debt-Discipline.md`.
Independent routes used here:
- the absolute-priority waterfall by a tranche-by-tranche loop, against closed-form min and max expressions
  for each tranche's recovery;
- the break-even enterprise value by bisection on the trade's profit as a function of EV, against the sum of
  price paid and the senior claim;
- the annualized return over 18 months by closed form, against bisection on (1 + r)^1.5 = value / cost;
- the thrift-conversion book value per share and the one-third blocking threshold of 11 U.S.C. 1126(c)
  in exact fractions.
Every quoted number is printed and asserted at the precision the note quotes.
Run from the repo root: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_vi_05_klarman.py
"""

from __future__ import annotations

from fractions import Fraction as F


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"{label:64s} {float(value):16.6f}  quoted {quoted}")
    assert abs(float(value) - float(quoted)) <= tol, f"{label}: {float(value)} does not round to {quoted}"
    return float(value)


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"  check {label:58s} |diff| = {abs(a - b):.2e} (tol {tol:.1e})")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def bisect(f, lo: float, hi: float, iters: int = 200) -> float:
    """Root of an increasing function f on [lo, hi]."""
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


CLAIMS = (("first lien", 400.0), ("senior unsecured", 800.0), ("subordinated", 300.0))


def waterfall(ev: float) -> list[float]:
    """Absolute priority: pay each tranche in order until value runs out."""
    remaining, paid = ev, []
    for _, claim in CLAIMS:
        take = min(claim, remaining)
        paid.append(take)
        remaining -= take
    return paid + [remaining]  # last element goes to the old equity


def closed_form(ev: float) -> list[float]:
    t1 = min(400.0, ev)
    t2 = max(0.0, min(800.0, ev - 400.0))
    t3 = max(0.0, min(300.0, ev - 1200.0))
    return [t1, t2, t3, max(0.0, ev - 1500.0)]


def transglobal() -> None:
    print("TransGlobal Telecom (hypothetical inputs, $M)")
    ev = 200 * 5.0
    q("reorganized EV 200 x 5.0", ev, "1000.0")
    for test_ev in (600.0, 736.0, 1000.0, 1300.0, 1600.0):
        for a, b in zip(waterfall(test_ev), closed_form(test_ev), strict=True):
            close(f"loop vs closed form at EV {test_ev:.0f}", a, b, 1e-9)
    t1, t2, t3, equity = waterfall(ev)
    q("first lien recovery", t1, "400")
    q("EV remaining after first lien", ev - t1, "600")
    q("value to the fulcrum (senior unsecured)", t2, "600.0")
    q("fulcrum recovery per dollar of face (cents)", 100 * t2 / 800, "75.0")
    q("subordinated recovery", t3, "0.00")
    q("old equity recovery", equity, "0.00")
    cost = 800 * F(42, 100)
    q("cost of the notes at 42 cents", cost, "336.0")
    q("old equity market cap 50M x $0.50", 50 * F(1, 2), "25")
    q("profit 600 - 336", 600 - cost, "264.0")
    q("return on investment (%)", 100 * (F(600) / cost - 1), "78.6")
    eff_ev = cost + 400
    q("effective EV paid 336 + 400", eff_ev, "736.0")
    q("effective EV / EBITDA (x)", eff_ev / 200, "3.68")
    breakeven = bisect(lambda e: waterfall(e)[1] - 336.0, 400.0, 1200.0)
    close("break-even EV by bisection vs cost plus senior claim", breakeven, float(eff_ev), 1e-9)
    q("cushion before loss, 1 - 736 / 1000 (%)", 100 * (1 - breakeven / ev), "26.4")
    for test_ev, value_q, ret_q in ((800.0, "400", "19.0"), (700.0, "300", "-10.7")):
        got = waterfall(test_ev)[1]
        q(f"fulcrum value at EV {test_ev:.0f}", got, value_q)
        q(f"return at EV {test_ev:.0f} (%)", 100 * (got / 336 - 1), ret_q)
    gross = 600 / 336
    closed = gross ** (1 / 1.5) - 1
    root = bisect(lambda r: (1 + r) ** 1.5 - gross, 0.0, 2.0)
    close("annualized closed form vs bisection", closed, root, 1e-12)
    q("annualized return over 18 months (%)", 100 * closed, "47.2")


def thrift_and_votes() -> None:
    print("Thrift conversion (hypothetical) and plan voting")
    existing, raised, price = F(50), F(100), F(10)
    shares = raised / price
    book_ps = (existing + raised) / shares
    q("pro forma book per share ($)", book_ps, "15")
    q("offer price / pro forma book (x)", price / book_ps, "0.67")
    q("blocking stake, more than 1 - 2/3 of the amount voted (%)", 100 * (1 - F(2, 3)), "33.3")


def main() -> None:
    transglobal()
    thrift_and_votes()
    print("all Klarman checks passed")


if __name__ == "__main__":
    main()
