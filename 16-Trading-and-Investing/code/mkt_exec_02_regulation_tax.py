"""Regulation, tax and trading operations: every number in 08-Execution-Microstructure/02-Regulation-Tax-and-Trading-Operations.md.

Rates and thresholds are cited constants (sources in the note); this script checks the arithmetic built on them.
Independent routes used here:
- the wash-sale window is counted with calendar dates (datetime), not by adding 30 + 1 + 30;
- the wash-sale example is computed by the basis-adjustment rule, and the economic result of both lots is checked
  against the $200 the note says the trader recognises over both sales;
- the Section 1256 blended rate is computed by applying the 60/40 split to a $100,000 gain, not by the formula alone;
- the Indian F&O turnover example sums absolute trade-level differences.
Run: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_exec_02_regulation_tax.py
"""

from __future__ import annotations

import datetime as dt

from mkt_assets_lib import q


def wash_sale() -> None:
    print("Wash-sale window and Example 1")
    sale = dt.date(2026, 4, 10)
    window = [sale + dt.timedelta(days=k) for k in range(-30, 31)]
    q("days in the wash-sale window, counting the sale date", len(window), "61")
    rebuy = dt.date(2026, 4, 25)
    q("days from the April 10 sale to the April 25 repurchase", (rebuy - sale).days, "15")
    assert rebuy in window
    buy1, sell1, buy2, sell2, n = 50.00, 42.00, 45.00, 55.00, 100
    loss = (sell1 - buy1) * n
    q("loss on the April 10 sale", loss, "-800")
    basis2 = buy2 * n - loss
    q("adjusted basis of the replacement lot", basis2, "5,300")
    q("adjusted basis per share", basis2 / n, "53.00")
    gain = sell2 * n - basis2
    q("taxable gain on the June 1 sale", gain, "200")
    q("gain on the replacement lot without the adjustment", (sell2 - buy2) * n, "1,000")
    economic = (sell1 - buy1) * n + (sell2 - buy2) * n
    q("economic result of both lots (-800 + 1,000)", economic, "200")


def section_1256() -> None:
    print("Section 1256 blended rate on a $100,000 net gain (2026 top federal rates)")
    gain, lt, st, niit = 100_000.0, 0.20, 0.37, 0.038
    tax = 0.6 * gain * lt + 0.4 * gain * st
    q("tax on $100,000 under 60/40", tax, "26,800")
    q("blended rate (%)", 100 * tax / gain, "26.8")
    q("blended rate with the 3.8% NIIT (%)", 100 * (tax + niit * gain) / gain, "30.6")
    q("short-term rate for comparison (%)", 100 * st, "37.0")


def reg_sho_deadlines() -> None:
    print("Reg SHO Rule 204 deadlines under T+1 settlement (counted in settlement days from trade date)")
    settlement = 1
    q("short-sale fail: settlement day after settlement date", settlement + 1, "2")
    q("long-sale or market-making fail: third settlement day after settlement date", settlement + 3, "4")


def india_turnover() -> None:
    print("Indian F&O turnover for the tax audit: sum of absolute trade-level differences (hypothetical trades)")
    pnl = [12_000.0, -8_500.0, 3_000.0, -15_000.0, 6_500.0]
    turnover = sum(abs(x) for x in pnl)
    q("turnover = sum |P&L|", turnover, "45,000")
    q("net P&L", sum(pnl), "-2,000")


if __name__ == "__main__":
    wash_sale()
    section_1256()
    reg_sho_deadlines()
    india_turnover()
    print("all regulation and tax numbers verified")
