"""Commodity term structures and storage: every number in 05-Commodities/01-Commodity-Term-Structures-and-Storage-Arbitrage.md.

Independent routes used here:
- the 3:2:1 crack spread is computed from per-barrel product values and, separately, by converting crude to $/gal
  and working per gallon before scaling back to $/bbl;
- the cash-and-carry fair value with a fixed storage charge paid at maturity is checked by an explicit cash-flow
  ledger of the arbitrage (borrow, buy, store, deliver into the short future), and the continuously compounded
  storage rate is checked by plugging it back into the exponential carry formula;
- the EIA Cushing utilisation is recomputed from the barrels and capacity EIA reported.
Run: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_cmdty_01_storage.py
"""

from __future__ import annotations

import math

from mkt_assets_lib import close, q


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
    per_gallon = (2 * rbob + ho) / 3 - wti / gal
    close("per-gallon route x 42 vs per-barrel route", per_gallon * gal, crack, 1e-12)


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
    close("S exp((r + u) T) with that u vs fair value", S * math.exp((r + u) * T), fair, 1e-9)
    # ledger: t = 0 borrow S, buy one barrel, sell one future at F_mkt; t = T deliver, repay loan, pay storage
    ledger_T = F_mkt - S * growth - store
    q("arbitrage profit per barrel", ledger_T, "0.63")
    close("ledger profit vs F_mkt - fair", ledger_T, F_mkt - fair, 1e-12)


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
