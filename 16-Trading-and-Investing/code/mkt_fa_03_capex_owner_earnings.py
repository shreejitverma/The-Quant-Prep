"""Maintenance capex, owner earnings and leases: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/Investing/Fundamental-Analysis/03-Capex-Maintenance-vs-Growth-and-Owner-Earnings.md`.
Independent routes used here:
- owner earnings built line by line from Buffett's (a) + (b) - (c) definition, and again as standard free
  cash flow plus the growth capex that free cash flow deducts, in exact fractions;
- the implied inflation rate behind a $10M asset costing $25M to replace after 10 years, in closed form
  and by bisection on the compounding equation;
- the lease present value as the closed-form annuity factor and as an explicit sum of five discounted
  payments, and the year-1 interest and principal by running the full five-year amortization schedule
  (the liability must reach zero after the fifth payment).
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_fa_03_capex_owner_earnings.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction as F


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    items = value if isinstance(value, tuple) else (value,)
    shown = ", ".join(f"{float(v):g}" if isinstance(v, F) and v.denominator != 1 else str(v) for v in items)
    print(f"    {label} = {shown}")


def rounded(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{value:,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"    {label} = {shown}")


def owner_earnings() -> None:
    print("Example 1: freight railroad owner earnings ($M)")
    ni, da, noncash, capex, d_nwc = F(450), F(320), F(30), F(480), F(40)
    maintenance = F(300)
    growth = capex - maintenance
    exact("growth capex", growth, 180)
    cfo = ni + da + noncash - d_nwc
    exact("CFO", cfo, 760)
    fcf = cfo - capex
    exact("standard FCF", fcf, 280)
    a_plus_b = ni + da + noncash  # Buffett (a) + (b)
    c = maintenance + d_nwc  # (c), with the working-capital increment assumed needed for unit volume
    oe = a_plus_b - c
    exact("owner earnings, (a) + (b) - (c)", oe, 460)
    exact("owner earnings, FCF + growth capex", fcf + growth, 460)


def inflation() -> None:
    print("Inflation and historical-cost depreciation (hypothetical asset)")
    cost, life, replacement = 10_000_000, 10, 25_000_000
    exact("annual straight-line depreciation", cost // life, 1_000_000)
    exact("cumulative depreciation over the life", life * (cost // life), 10_000_000)
    exact("replacement shortfall", replacement - cost, 15_000_000)
    closed = (replacement / cost) ** (1 / life) - 1
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if cost * (1 + mid) ** life < replacement:
            lo = mid
        else:
            hi = mid
    assert abs(lo - closed) < 1e-12
    rounded("implied annual inflation (percent, closed form)", 100 * closed, "9.6")
    rounded("implied annual inflation (percent, bisection)", 100 * lo, "9.6")


def lease() -> None:
    print("Example 2: 5-year lease, $10M a year in arrears at 6%")
    pay, r, n = 10_000_000.0, 0.06, 5
    factor = (1 - (1 + r) ** -n) / r
    explicit = sum((1 + r) ** -k for k in range(1, n + 1))
    assert math.isclose(factor, explicit, rel_tol=1e-14)
    rounded("annuity factor", factor, "4.212364")
    pv = pay * explicit
    rounded("PV of payments (ROU asset and liability)", pv, "42,123,638")
    rounded("straight-line ROU depreciation", pv / n, "8,424,728")
    liability, schedule = pv, []
    for _ in range(n):
        interest = liability * r
        principal = pay - interest
        liability -= principal
        schedule.append((interest, principal))
    assert abs(liability) < 1e-6, "liability must amortize to zero"
    interest1, principal1 = schedule[0]
    rounded("year-1 interest", interest1, "2,527,418")
    rounded("year-1 principal", principal1, "7,472,582")
    total_interest = sum(i for i, _ in schedule)
    rounded("total interest over the lease", total_interest, "7,876,362")
    rounded("ASC 842 straight-line operating lease cost", (total_interest + pv) / n, "10,000,000")


if __name__ == "__main__":
    owner_earnings()
    inflation()
    lease()
    print("all capex and owner-earnings numbers check out")
