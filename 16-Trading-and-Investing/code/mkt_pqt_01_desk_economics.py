"""Desk economics: every number in the desk-roles note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Quant-Prop-Trading/01-Desk-Roles-and-Economics.md`.
Independent routes used here:
- Example 1 total PnL from a cash-and-inventory ledger (cash flows plus the final inventory marked at the
  mid), against the sum of the attribution terms (spread capture, one-second adverse selection components, later drift, fees)
  computed from the mid path; the two routes share only the inputs;
- the attribution identity PnL = spread + inventory PnL + fees on 2,000 random sessions with random fills
  and a random mid path, where inventory PnL is accumulated step by step as q_t * dS_t (not from the
  closed-form sum over fills), so a sign or bookkeeping error in either route fails the check;
- Example 2 ratios in exact decimal arithmetic (Python's decimal module at 40 digits) against the quoted
  literals, and the square-root-of-time scaling of volatility by a seeded simulation of 252-day sums
  with a tolerance of five standard errors.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_pqt_01_desk_economics.py`.
"""

from __future__ import annotations

from decimal import Decimal, getcontext

import numpy as np

SEED = 11


def rounded(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{float(value):,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"    {label} = {shown}")


def example_1() -> None:
    print("Example 1: three-trade attribution")
    rebate, taker = 0.0020, 0.0030
    # (time s, signed size, price, mid at fill, passive?)
    fills = [(10, +1000, 99.98, 100.00, True), (25, -1000, 100.02, 100.00, True), (40, -1000, 99.95, 99.97, False)]
    mid_path = {10: 100.00, 11: 99.96, 25: 100.00, 26: 100.00, 40: 99.97}  # mid at each time point
    t_mark, s_mark = 40, 99.97

    # Route A: ledger
    cash = sum(-n * p for _, n, p, _, _ in fills)
    fees = sum(abs(n) * (rebate if passive else -taker) for _, n, _, _, passive in fills)
    inventory = sum(n for _, n, _, _, _ in fills)
    ledger_pnl = cash + inventory * s_mark + fees
    for i, (lit, (_, n, p, _, _)) in enumerate(zip(("-99,980.00", "100,020.00", "99,950.00"), fills, strict=True), 1):
        rounded(f"cash leg, trade {i}", -n * p, lit)
    rounded("cash from trades", cash, "99,990.00")
    rounded("final inventory (shares)", inventory, "-1,000")
    rounded("net fees and rebates", fees, "1.00")
    rounded("mark-to-market PnL, ledger", ledger_pnl, "21.00")

    # Route B: attribution from the mid path
    spread = sum(n * (s - p) for _, n, p, s, _ in fills)
    tau = 1
    markouts, later = [], []
    for t, n, _, s, _ in fills:
        t_tau = min(t + tau, t_mark)
        markouts.append(n * (mid_path[t_tau] - s))
        later.append(n * (s_mark - mid_path[t_tau]))
    for i, m in enumerate(markouts, 1):
        print(f"    one-second adverse selection component, trade {i} = {m + 0.0:.2f}")
    assert [round(m, 6) for m in markouts] == [-40.0, 0.0, 0.0]
    rounded("adverse selection component total", sum(markouts), "-40.00")
    for i, (lit, (t, n, p, s, _), adverse) in enumerate(zip(("-20.00", "20.00", "-20.00"), fills, markouts, strict=True), 1):
        fill_markout = n * (mid_path[min(t + tau, t_mark)] - p)
        rounded(f"one-second fill-price markout, trade {i}", fill_markout, lit)
        assert abs(fill_markout - (n * (s - p) + adverse)) < 1e-9
    rounded("later drift total", sum(later), "40.00")
    rounded("later drift, trade 1", later[0], "10.00")
    rounded("later drift, trade 2", later[1], "30.00")
    inventory_pnl = sum(markouts) + sum(later)
    rounded("inventory drift (adverse selection + later drift)", inventory_pnl, "0.00")
    rounded("gross spread capture", spread, "20.00")
    rounded("spread capture, trade 1", fills[0][1] * (fills[0][3] - fills[0][2]), "20.00")
    rounded("spread capture, trade 2", fills[1][1] * (fills[1][3] - fills[1][2]), "20.00")
    rounded("spread cost, trade 3", fills[2][1] * (fills[2][3] - fills[2][2]), "-20.00")
    rounded("mark-to-market PnL, attribution", spread + inventory_pnl + fees, "21.00")
    round_trip = sum(-n * p for _, n, p, _, _ in fills[:2]) + 2 * 1000 * rebate
    open_short = fills[2][1] * (fills[2][3] - fills[2][2]) - 1000 * taker
    rounded("round trip of trades 1 and 2 (cash plus rebates)", round_trip, "44.00")
    rounded("open short marked at the mid", open_short, "-23.00")
    rounded("rebate per passive fill", 1000 * rebate, "2.00")
    rounded("taker fee on trade 3", 1000 * taker, "3.00")


def attribution_identity(rng: np.random.Generator, sessions: int = 2000) -> None:
    print("Attribution identity on random sessions")
    worst = 0.0
    for _ in range(sessions):
        steps = 200
        mid = 100 + np.cumsum(rng.choice([-0.01, 0.0, 0.01], size=steps))
        fill_at = np.sort(rng.choice(steps - 1, size=12, replace=False))
        sizes = rng.choice([-300, -100, 100, 300], size=12)
        half = rng.choice([-0.01, 0.0, 0.01], size=12)  # fill price = mid - sign * half
        prices = mid[fill_at] - np.sign(sizes) * half
        fee = rng.normal(0, 1, size=12)
        # ledger
        cash = float(np.sum(-sizes * prices))
        ledger = cash + float(sizes.sum()) * mid[-1] + float(fee.sum())
        # attribution: spread capture plus step-by-step inventory PnL
        spread = float(np.sum(sizes * (mid[fill_at] - prices)))
        q = np.zeros(steps)
        for t, n in zip(fill_at, sizes, strict=True):
            q[t:] += n
        inv = float(np.sum(q[:-1] * np.diff(mid)))
        worst = max(worst, abs(ledger - (spread + inv + float(fee.sum()))))
    print(f"    sessions = {sessions}, worst |ledger - attribution| = {worst:.2e}")
    assert worst < 1e-6


def example_2(rng: np.random.Generator) -> None:
    print("Example 2: desk risk metrics")
    getcontext().prec = 40
    equity, pnl, dd = Decimal(5_000_000), Decimal(1_500_000), Decimal(250_000)
    rf, sd_d, down_d, n = Decimal("0.04"), Decimal("0.0075"), Decimal("0.0040"), Decimal(252)
    mu = pnl / equity
    sig = sd_d * n.sqrt()
    down = down_d * n.sqrt()
    print(f"    input: equity $5,000,000, GMV $20,000,000, PnL ${pnl:,}, daily sd 0.75%, downside sd {down_d * 100:.2f}%")
    rounded("leverage (GMV / equity)", 20_000_000 / 5_000_000, "4")
    rounded("annual return (%)", mu * 100, "30.0")
    rounded("drawdown on equity (%)", dd / equity * 100, "5.0")
    rounded("daily risk-free rate (%)", rf / n * 100, "0.01587")
    rounded("annualized volatility (%)", sig * 100, "11.906")
    rounded("Sharpe ratio", (mu - rf) / sig, "2.184")
    rounded("annualized downside deviation (%)", down * 100, "6.350")
    rounded("Sortino ratio", (mu - rf) / down, "4.095")
    rounded("RoMaD", mu / (dd / equity), "6.00")
    # the old literal 11.905 and 4.094 must not survive the rounding test
    assert f"{float(sig * 100):.3f}" != "11.905" and f"{float((mu - rf) / down):.3f}" != "4.094"

    # sqrt-time scaling: std of 252-day sums of iid daily returns with sd 0.75%
    paths = 20_000
    sums = rng.normal(0.0, 0.0075, size=(paths, 252)).sum(axis=1)
    sd_sim = float(sums.std(ddof=1))
    se = sd_sim / np.sqrt(2 * (paths - 1))  # standard error of a normal sample standard deviation
    print(f"    simulated annual sd (seed {SEED}) = {sd_sim:.5f} +/- {se:.5f}")
    assert abs(sd_sim - float(sig)) < 5 * se


def cards() -> None:
    print("Cards")
    print("    cited: Rule 610(c) access-fee cap $0.003 per share; 2024 amendment $0.001 (Release 34-101070)")
    print("    cited: IEX speed bump 350 microseconds")
    sizes, child_fills = np.array([1.0, 2.0, 4.0, 8.0]), 20_000
    total_cost = []
    for q in sizes:
        dq = q / child_fills
        executed = (np.arange(child_fills) + 0.5) * dq
        total_cost.append(float(np.sum(np.sqrt(executed) * dq)))
    slope = np.polyfit(np.log(sizes), np.log(total_cost), 1)[0]
    print(f"    exponent fitted to {child_fills:,} child fills with marginal impact sqrt(executed) = {slope:.6f}")
    assert abs(slope - 1.5) < 1e-3
    rounded("square-root impact: exponent of total liquidation cost in size", slope, "1.5")


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    example_1()
    attribution_identity(rng)
    example_2(rng)
    cards()
    print("all desk-economics numbers check out")
