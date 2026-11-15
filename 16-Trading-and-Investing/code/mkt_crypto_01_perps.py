"""Perpetual futures and funding arbitrage: every number in 06-Crypto-and-Digital-Assets/01-Perpetual-Futures-and-Funding-Rate-Arbitrage.md.

Independent routes used here:
- funding cash flows are accumulated interval by interval and compared with the closed-form product, and the
  annualised yield is recomputed from the cash flow rather than from 1,095 x rate;
- the liquidation price of the short perpetual is found by bisection on the account-equity function (equity minus
  maintenance margin at the mark price) and compared with the closed form;
- impermanent loss is computed by simulating the constant-product pool: an arbitrageur's swap through the x y = k
  swap formula is sized by bisection to move the pool to the new price, the LP's holdings are valued against simply
  holding the initial tokens, and the result is compared with 2 sqrt(R) / (1 + R) - 1; a second simulation at 1/R
  checks the symmetry;
- the inverse-contract P&L bound is checked numerically as the price grows without limit.
Run: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_crypto_01_perps.py
"""

from __future__ import annotations

import math

from mkt_assets_lib import bisect, close, q


def funding() -> None:
    print("Funding conventions")
    i8 = 0.0001
    q("interest component per day (%)", 100 * 3 * i8, "0.03")
    q("interest component annualised, simple (%)", 100 * 1095 * i8, "10.95")
    q("intervals per year at 8 hours", 3 * 365, "1,095")
    q("annualised simple yield at 0.03% per 8h (%)", 100 * 0.0003 * 1095, "32.85")
    q("annualised simple yield at 0.02% per 8h (%)", 100 * 0.0002 * 1095, "21.90")
    q("BitMEX-style interest rate (0.06% - 0.03%) / 3 per 8h (%)", 100 * (0.0006 - 0.0003) / 3, "0.01")


def example_1() -> None:
    print("Example 1: $1,000,000 cash-and-carry at $60,000 BTC, 0.025% per 8h for 30 days")
    capital, price, f8, days = 1_000_000.0, 60_000.0, 0.00025, 30
    qty = 500_000.0 / price
    q("BTC bought", qty, "8.3333")
    notional = qty * price
    q("per-day funding (bps)", 1e4 * 3 * f8, "7.5")
    intervals = 3 * days
    q("funding intervals in 30 days", intervals, "90")
    cash = 0.0
    for _ in range(intervals):
        cash += notional * f8  # mark held at entry for the illustration
    q("funding collected", cash, "11,250")
    q("funding as a share of the perp notional (%)", 100 * cash / notional, "2.25")
    q("30-day return on capital (%)", 100 * cash / capital, "1.125")
    q("365 / 30", 365 / days, "12.167")
    q("annualised simple yield on capital (%)", 100 * cash / capital * 365 / days, "13.69")
    mmr, collateral = 0.005, 500_000.0
    closed = price * (1 + collateral / notional) / (1 + mmr)

    def equity_minus_mm(p: float) -> float:
        return collateral - qty * (p - price) - mmr * qty * p

    liq = bisect(equity_minus_mm, price, 3 * price, tol=1e-9)
    q("liquidation price (bisection)", liq, "119,402.99")
    close("bisection vs closed form", liq, closed, 1e-6)
    wrong = price * (1 + collateral / notional - mmr)
    q("liquidation price if margin is charged on entry notional", wrong, "119,700")
    q("overstatement of the buffer", wrong - closed, "297")
    q("rally to liquidation (%)", 100 * (closed / price - 1), "99.0")


def impermanent_loss() -> None:
    print("Impermanent loss from a simulated constant-product pool")
    x0, y0 = 100.0, 100.0 * 2_000.0  # 100 ETH and 200,000 USDC at a price of 2,000
    p0 = y0 / x0

    def arbitrage(p_target: float) -> tuple[float, float]:
        # no-fee swap: dy in gives x dy / (y + dy) out (and dx in gives y dx / (x + dx) out); size it so the pool price hits p_target
        if p_target >= p0:

            def gap_up(dy: float) -> float:
                return (y0 + dy) / (x0 - x0 * dy / (y0 + dy)) - p_target

            dy = bisect(gap_up, 0.0, 100 * y0, tol=1e-9)
            return x0 - x0 * dy / (y0 + dy), y0 + dy

        def gap_down(dx: float) -> float:
            return (y0 - y0 * dx / (x0 + dx)) / (x0 + dx) - p_target

        dx = bisect(gap_down, 0.0, 100 * x0, tol=1e-12)
        return x0 + dx, y0 - y0 * dx / (x0 + dx)

    def il_sim(ratio: float) -> float:
        p1 = p0 * ratio
        x1, y1 = arbitrage(p1)
        return (x1 * p1 + y1) / (x0 * p1 + y0) - 1

    for ratio, quoted in ((1.25, "-0.62"), (1.5, "-2.02"), (2.0, "-5.72"), (3.0, "-13.40"), (5.0, "-25.46")):
        il = il_sim(ratio)
        q(f"impermanent loss at price ratio {ratio} (%)", 100 * il, quoted)
        close(f"pool simulation vs 2 sqrt(R) / (1 + R) - 1 at R = {ratio}", il, 2 * math.sqrt(ratio) / (1 + ratio) - 1, 1e-10)
        close(f"pool simulation at 1/R vs pool simulation at R = {ratio}", il_sim(1 / ratio), il, 1e-10)


def inverse_contract() -> None:
    print("Inverse (coin-margined) contract: long N USD of contracts, P&L in BTC = N (1/P0 - 1/P1)")
    N, p0 = 10_000.0, 50_000.0

    def pnl(p1: float) -> float:
        return N * (1 / p0 - 1 / p1)

    close("long gain in BTC as the price grows without limit vs cap N / P0", pnl(1e15), N / p0, 1e-9)
    assert abs(pnl(p0 / 2) + N / p0) < 1e-12 and pnl(p0 / 10) < -9 * N / p0 + 1e-12, "long loss in BTC grows without bound as P1 falls"


if __name__ == "__main__":
    funding()
    example_1()
    impermanent_loss()
    inverse_contract()
    print("all perpetual-futures numbers verified")
