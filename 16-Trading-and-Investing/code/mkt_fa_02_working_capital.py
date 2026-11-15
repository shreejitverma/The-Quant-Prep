"""Working capital cycles: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/Investing/Fundamental-Analysis/02-Working-Capital-Cycles-and-Cash-Conversion.md`.
Independent routes used here:
- each day count (DSO, DIO, DPO) in exact fractions from the stated balances, and again by simulating a
  steady-state firm that books equal daily flows and holds each for the quoted number of days: the
  time-averaged simulated balance must reproduce the stated balance to within the quote's rounding
  (Little's law, balance = daily flow x days, checked numerically rather than assumed);
- the cash conversion cycle as DSO + DIO - DPO and again by simulating dated events for one unit bought
  each day (supplier paid DPO days after purchase, sold DIO days after purchase, cash collected DSO days
  after the sale) and measuring the time-averaged cash tied up per unit of daily purchases (Little's law
  on the simulated cash balance, negative when suppliers fund the cycle);
- the float business's net working capital by summing the balance sheet lines.
Every quoted number is printed as ``label = value`` and asserted at the decimals the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_fa_02_working_capital.py`.
"""

from __future__ import annotations

from fractions import Fraction as F

import numpy as np


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    items = value if isinstance(value, tuple) else (value,)
    shown = ", ".join(f"{float(v):g}" if isinstance(v, F) and v.denominator != 1 else str(v) for v in items)
    print(f"    {label} = {shown}")


def rounded(label: str, value: F | float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{float(value):.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"    {label} = {shown}")


def simulated_balance(daily_flow: float, days: float, grid: float = 0.01) -> float:
    """Time-average balance of a book that receives `daily_flow` each day and holds each item `days` days."""
    issue = np.arange(0, 2000, dtype=float)  # one booking per day
    settle = issue + days
    t = np.arange(1000.0, 1365.0, grid)  # a year well past the warm-up
    open_items = np.searchsorted(issue, t, side="right") - np.searchsorted(settle, t, side="right")
    return float(daily_flow * open_items.mean())


def check_days(label: str, balance: F, flow: F, quoted: str) -> F:
    days = balance / flow * 365
    rounded(f"{label} (exact fractions)", days, quoted)
    sim = simulated_balance(float(flow) / 365, float(quoted))
    half_step = 0.5 * 10 ** -(len(quoted.split(".")[1]) if "." in quoted else 0)
    tol = float(flow) / 365 * (half_step + 0.02)  # quote rounding plus grid error
    assert abs(sim - float(balance)) <= tol, f"{label}: simulated balance {sim} vs stated {float(balance)}"
    print(f"    {label}: simulated balance at {quoted} days = {sim:,.0f} (stated {float(balance):,.0f})")
    return days


def simulated_cash_gap(dio: float, dso: float, dpo: float, grid: float = 0.01) -> float:
    """Days of daily purchases tied up in cash, from dated payment and collection events of daily units."""
    purchase = np.arange(0, 2000, dtype=float)  # one unit bought each day, at cost 1
    paid = np.sort(purchase + dpo)
    sold = purchase + dio
    collected = np.sort(sold + dso)
    t = np.arange(1000.0, 1365.0, grid)  # a year well past the warm-up
    cash_out = np.searchsorted(paid, t, side="right")
    cash_in = np.searchsorted(collected, t, side="right")
    return float((cash_out - cash_in).mean())


def industrial() -> None:
    print("Example 1: industrial manufacturer ($)")
    rev, cogs = F(730_000_000), F(438_000_000)
    ar = (F(120_000_000) + F(140_000_000)) / 2
    inv = (F(90_000_000) + F(110_000_000)) / 2
    ap = (F(50_000_000) + F(70_000_000)) / 2
    exact("average AR", ar, 130_000_000)
    exact("average inventory", inv, 100_000_000)
    exact("average AP", ap, 60_000_000)
    rounded("AR / revenue", ar / rev, "0.17808")
    rounded("inventory / COGS", inv / cogs, "0.22831")
    rounded("AP / COGS", ap / cogs, "0.13699")
    dso = check_days("DSO", ar, rev, "65.0")
    dio = check_days("DIO", inv, cogs, "83.3")
    dpo = check_days("DPO", ap, cogs, "50.0")
    ccc = dso + dio - dpo
    rounded("CCC", ccc, "98.3")
    rounded("CCC (simulated cash tied up, days)", simulated_cash_gap(float(dio), float(dso), float(dpo)), "98.3")
    exact("hypothetical positive cycle 60 + 45 - 35", 60 + 45 - 35, 70)
    exact("hypothetical negative cycle 15 + 25 - 75", 15 + 25 - 75, -35)


def float_model() -> None:
    print("Example 2: negative working capital marketplace ($M)")
    rev, cogs = F(3650), F(2920)
    ar, inv, ap = F(30), F(160), F(720)
    dso = check_days("DSO", ar, rev, "3.0")
    dio = check_days("DIO", inv, cogs, "20.0")
    dpo = check_days("DPO", ap, cogs, "90.0")
    rounded("CCC", dso + dio - dpo, "-67.0")
    rounded("CCC (simulated cash tied up, days)", simulated_cash_gap(float(dio), float(dso), float(dpo)), "-67.0")
    exact("operating assets", ar + inv, 190)
    exact("net working capital", sum([ar, inv, -ap]), -530)


if __name__ == "__main__":
    industrial()
    float_model()
    print("all working-capital numbers check out")
