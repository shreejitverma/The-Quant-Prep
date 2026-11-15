"""Commodity term structures and storage: every number in 05-Commodities/01-Commodity-Term-Structures-and-Storage-Arbitrage.md.

Independent routes used here:
- the 3:2:1 crack spread is computed from per-barrel product values;
- the cash-and-carry fair value with a fixed storage charge paid at maturity is checked by stepping a month-by-month
  ledger of the arbitrage (borrow to buy one barrel, accrue financing and storage each month, deliver into the short
  future) and comparing its terminal cost and profit with the quoted fair forward and arbitrage profit;
- the EIA Cushing utilisation is recomputed from the barrels and capacity EIA reported.
Run: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_cmdty_01_storage.py
"""

from __future__ import annotations

import math

from mkt_assets_lib import q


def crack_spread() -> None:
    print("3:2:1 crack spread (hypothetical prices)")
    wti, rbob, ho, gal = 75.00, 2.50, 2.80, 42
    q("RBOB per barrel", rbob * gal, "105.00")
    q("heating oil per barrel", ho * gal, "117.60")
    out = 2 * rbob * gal + ho * gal
    q("product output value", out, "327.60")
    q("crude feedstock cost", 3 * wti, "225.00")
    q("net crack value per 3 barrels", out - 3 * wti, "102.60")
    crack = (out - 3 * wti) / 3
    q("3:2:1 crack spread per barrel", crack, "34.20")


def cash_and_carry() -> None:
    print("Example 1: cash-and-carry with storage of $0.60 per barrel per month paid at maturity")
    S, F_mkt, r, T, store = 70.00, 76.00, 0.05, 0.5, 0.60 * 6
    q("storage paid at T", store, "3.60")
    growth = math.exp(r * T)
    q("exp(r T)", growth, "1.02532")
    q("financed spot", S * growth, "71.77")
    fair = S * growth + store
    q("no-arbitrage futures price", fair, "75.37")
    q("no-arbitrage futures price, three decimals", fair, "75.372")
    q("annual storage cost 0.60 x 12", 0.60 * 12, "7.20")
    simple = store * 2 / S
    q("storage as a simple annual rate (%)", 100 * simple, "10.29")
    q("exponent (r + u_simple) T", (r + simple) * T, "0.07643")
    q("price using the simple rate in the exponential", S * math.exp((r + simple) * T), "75.56")
    u = 2 * math.log(fair / S) - r
    q("consistent continuously compounded storage rate (%)", 100 * u, "9.79")
    # ledger: t = 0 borrow S, buy one barrel, sell one future at F_mkt; each month the loan accrues interest and
    # $0.60 of storage falls due (paid at T); at T deliver the barrel, repay the loan and pay the storage
    loan, storage_due = S, 0.0
    for _ in range(6):
        loan *= math.exp(r / 12)
        storage_due += 0.60
    q("ledger cost of delivering at T (fair forward)", loan + storage_due, "75.372")
    q("ledger arbitrage profit per barrel", F_mkt - loan - storage_due, "0.63")


def cushing_2020() -> None:
    print("EIA: Cushing crude in tank farms vs working capacity, April 17, 2020")
    q("utilisation (%)", 100 * 58 / 76, "76")
    print("CME CL contract: tick value")
    q("1,000 barrels x $0.01 tick ($ per contract)", 1000 * 0.01, "10")


if __name__ == "__main__":
    crack_spread()
    cash_and_carry()
    cushing_2020()
    print("all commodity numbers verified")
