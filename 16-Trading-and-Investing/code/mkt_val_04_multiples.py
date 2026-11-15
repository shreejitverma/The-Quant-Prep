"""Relative valuation and multiples: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/Investing/Valuation Models/04-Relative-Valuation-Multiples-Done-Right.md`.
Independent routes used here:
- the comparative multiples table in exact rational arithmetic (fractions.Fraction) from the raw inputs;
- the justified P/B formula (ROE - g) / (Ke - g) against a year-by-year clean-surplus simulation that
  pays out ROE x B - g x B, grows book at g and discounts 3,000 years of dividends plus the tail;
- the forward P/E formula against the same simulated dividend stream divided by next year's earnings;
- the multiple-expansion contribution per year by bisection on 15 (1 + r)^T = 22 against the closed-form root.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_val_04_multiples.py`.
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


def simulated_equity(book0: float, roe: float, ke: float, g: float, years: int = 3000) -> tuple[float, float]:
    """Clean-surplus stream: earnings ROE x B, dividends ROE x B - g x B, book grows at g. Returns (P0, E1)."""
    book, value = book0, 0.0
    for k in range(1, years + 1):
        earnings = roe * book
        dividend = earnings - g * book
        value += dividend / (1 + ke) ** k
        book += earnings - dividend
    tail = (roe - g) * book / (ke - g) / (1 + ke) ** years
    return value + tail, roe * book0


def table() -> None:
    print("Worked case: Precision Corp vs Heavy Gear (cards mkt-val-098, mkt-val-103)")
    firms = {
        "A": {
            "price": F(80),
            "shares": F(50),
            "debt": F(600),
            "cash": F(200),
            "rev": F(2000),
            "ebitda": F(440),
            "da": F(90),
            "int": F(30),
            "bv": F(2000),
        },
        "B": {
            "price": F(35),
            "shares": F(100),
            "debt": F(2500),
            "cash": F(100),
            "rev": F(3000),
            "ebitda": F(590),
            "da": F(290),
            "int": F(150),
            "bv": F(1500),
        },
    }
    quoted = {
        "A": {
            "mcap": 4000,
            "ev": 4400,
            "ebitda_m": 22.0,
            "ebit": 350,
            "ebit_m": 17.5,
            "ebt": 320,
            "ni": 240.0,
            "ev_s": 2.20,
            "ev_ebitda": 10.00,
            "ev_ebit": 12.57,
            "pe": 16.67,
            "pb": 2.00,
            "roe": 12.00,
            "nd_ebitda": 0.91,
        },
        "B": {
            "mcap": 3500,
            "ev": 5900,
            "ebitda_m": 19.7,
            "ebit": 300,
            "ebit_m": 10.0,
            "ebt": 150,
            "ni": 112.5,
            "ev_s": 1.97,
            "ev_ebitda": 10.00,
            "ev_ebit": 19.67,
            "pe": 31.11,
            "pb": 2.33,
            "roe": 7.50,
            "nd_ebitda": 4.07,
        },
    }
    out = {}
    for name, x in firms.items():
        q = quoted[name]
        mcap = x["price"] * x["shares"]
        ev = mcap + x["debt"] - x["cash"]
        ebit = x["ebitda"] - x["da"]
        ebt = ebit - x["int"]
        ni = ebt * F(3, 4)
        exact(f"{name} market cap", mcap, q["mcap"])
        exact(f"{name} EV", ev, q["ev"])
        approx(f"{name} EBITDA margin (percent)", 100 * x["ebitda"] / x["rev"], q["ebitda_m"], 1)
        exact(f"{name} EBIT", ebit, q["ebit"])
        approx(f"{name} EBIT margin (percent)", 100 * ebit / x["rev"], q["ebit_m"], 1)
        exact(f"{name} EBT", ebt, q["ebt"])
        approx(f"{name} net income", ni, q["ni"], 1)
        approx(f"{name} EV/Sales", ev / x["rev"], q["ev_s"], 2)
        approx(f"{name} EV/EBITDA", ev / x["ebitda"], q["ev_ebitda"], 2)
        approx(f"{name} EV/EBIT", ev / ebit, q["ev_ebit"], 2)
        approx(f"{name} P/E", mcap / ni, q["pe"], 2)
        approx(f"{name} P/B", mcap / x["bv"], q["pb"], 2)
        approx(f"{name} ROE (percent)", 100 * ni / x["bv"], q["roe"], 2)
        approx(f"{name} net debt / EBITDA", (x["debt"] - x["cash"]) / x["ebitda"], q["nd_ebitda"], 2)
        out[name] = {"ev_ebit": ev / ebit, "da_rev": x["da"] / x["rev"], "nd": x["debt"] - x["cash"], "int_ebit": x["int"] / ebit}
    approx("B EV/EBIT premium over A (percent)", 100 * (out["B"]["ev_ebit"] / out["A"]["ev_ebit"] - 1), 56, 0)
    approx("A D&A / revenue (percent)", 100 * out["A"]["da_rev"], 4.5, 1)
    approx("B D&A / revenue (percent)", 100 * out["B"]["da_rev"], 9.7, 1)
    exact("B net debt", out["B"]["nd"], 2400)
    exact("B interest / EBIT", out["B"]["int_ebit"], F(1, 2))


def ebitda_capex() -> None:
    print("Core concepts 4: EBITDA ignores capex (card mkt-val-102)")
    exact("A EBITDA - capex", F(100) - 5, 95)
    exact("B EBITDA - capex", F(100) - 60, 40)
    approx("A EV / (EBITDA - capex)", F(1000) / 95, 10.5, 1)
    approx("B EV / (EBITDA - capex)", F(1000) / 40, 25.0, 1)


def pb_and_pe() -> None:
    print("Core concepts 1 and 5: justified P/E and P/B (cards mkt-val-104, mkt-val-106)")
    p0, e1 = simulated_equity(1.0, 0.04, 0.10, 0.0)
    approx("value trap: ROE 4%, Ke 10%, g 0 (simulated P/B)", p0, 0.40, 2)
    approx("value trap: closed form (ROE - g) / (Ke - g)", (0.04 - 0.0) / (0.10 - 0.0), 0.40, 2)
    p0g, _ = simulated_equity(1.0, 0.04, 0.10, 0.02)
    approx("value trap with g = 2% (simulated P/B)", p0g, 0.25, 2)
    # Forward P/E: a hypothetical ROE 15%, Ke 9%, g 4% firm pays out 1 - g / ROE.
    p0, e1 = simulated_equity(1.0, 0.15, 0.09, 0.04)
    payout = 1 - 0.04 / 0.15
    approx("payout ratio 1 - g / ROE", payout, 0.7333, 4)
    approx("forward P/E simulated", p0 / e1, 14.67, 2)
    approx("forward P/E closed form payout / (Ke - g)", payout / (0.09 - 0.04), 14.67, 2)
    approx("P/B closed form for the same firm", (0.15 - 0.04) / (0.09 - 0.04), 2.20, 2)
    approx("P/B simulated for the same firm", p0, 2.20, 2)


def peg() -> None:
    print("Core concepts 6: PEG failure modes")
    exact("PEG at P/E 10, growth 2%", F(10, 2), 5)
    exact("PEG at P/E 80, growth 100%", F(80, 100), F(4, 5))


def multiple_expansion() -> None:
    print("Card mkt-val-262: contribution of a 15x to 22x re-rating by horizon")
    for years, quoted in [(1, 46.67), (10, 3.90), (20, 1.93)]:
        rate = (22 / 15) ** (1 / years) - 1
        approx(f"{years}-year horizon: annual contribution (percent)", 100 * rate, quoted, 2)
        # Independent route: bisection for the rate r with 15 (1 + r)^T = 22.
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if 15 * (1 + mid) ** years < 22 else (lo, mid)
        approx(f"{years}-year horizon: annual contribution by bisection (percent)", 100 * lo, quoted, 2)


if __name__ == "__main__":
    table()
    ebitda_capex()
    pb_and_pe()
    peg()
    multiple_expansion()
    print("all multiples numbers check out")
