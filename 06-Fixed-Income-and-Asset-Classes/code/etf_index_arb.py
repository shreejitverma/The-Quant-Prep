"""ETF creation and redemption arbitrage, leveraged-ETF decay, index futures fair value and index arbitrage.

Backs 06-Fixed-Income-and-Asset-Classes/08-ETFs-and-Index-Arbitrage.md.
All prices, fees and sizes are hypothetical round numbers chosen for the examples, not market data.
The one contract term used, the E-mini S&P 500 multiplier of 50 USD per index point, is CME's.

1. NAV from a creation basket, premium and discount, AP creation P&L and the no-arbitrage band.
2. Leveraged and inverse ETF path dependence (daily reset).
3. Index futures fair value with discrete dividends, implied financing rate, and the arbitrage band.
4. Index arbitrage P&L held to expiry and unwound early.
5. Index inclusion: predictable passive demand in days of volume.

Run: uv run --no-project --with numpy python 06-Fixed-Income-and-Asset-Classes/code/etf_index_arb.py
"""

from __future__ import annotations

import sys

CALIBRATING: list[str] = []


def check(label: str, value: float, expected: float | None, tol: float, fmt: str = ".4f") -> None:
    """Print `label = value` and assert it matches the literal the note quotes, to `tol` and when formatted.

    An expected 0 in scientific format is an identity check: only the tolerance applies.
    """
    printed = f"{value:{fmt}}"
    if float(printed) == 0:
        printed = printed.removeprefix("-")
    print(f"{label} = {printed}")
    if expected is None:
        CALIBRATING.append(label)
        return
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected} +/- {tol}"
    if not (expected == 0 and fmt.endswith("e")):
        assert printed == f"{expected:{fmt}}", f"{label}: prints {printed}, note quotes {expected:{fmt}}"


# ---------------------------------------------------------------------------
# 1. NAV, premium and the AP creation trade
# ---------------------------------------------------------------------------

CU_SHARES = 50_000  # ETF shares per creation unit
BASKET = {"A": (12_000, 95.00), "B": (6_000, 136.75), "C": (20_000, 26.25)}  # shares per unit, last price
CASH_COMPONENT = 19_500.0  # USD per creation unit
CREATION_FEE = 500.0  # USD per creation unit, charged by the fund
BASKET_COST_BP = 3.0  # half-spread plus commission to buy or sell the basket, bp of basket value


def section_nav() -> None:
    print("\n== 1. NAV and the creation trade ==")
    basket_value = sum(q * p for q, p in BASKET.values())
    nav = (basket_value + CASH_COMPONENT) / CU_SHARES
    # fi-etf-nav-premium, Worked example 1
    check("basket value per creation unit (USD)", basket_value, 2485500, 0.5, ".0f")
    check("NAV per ETF share", nav, 50.10, 1e-9, ".2f")
    bid, ask = 50.22, 50.23  # ETF quote
    mid = (bid + ask) / 2
    check("premium of ETF mid to NAV (bp)", (mid / nav - 1) * 1e4, 24.95, 0.005, ".2f")
    # Creation: buy the basket (pay cost), deliver basket + cash + fee, receive CU_SHARES, sell them at the bid.
    cost_in = basket_value * (1 + BASKET_COST_BP / 1e4) + CASH_COMPONENT + CREATION_FEE
    proceeds = CU_SHARES * bid
    pnl = proceeds - cost_in
    check("ETF sale proceeds per unit at the bid (USD)", proceeds, 2511000.0, 1e-6, ".0f")
    check("cost of creating one unit (USD)", cost_in, 2506245.65, 0.005, ".2f")
    check("creation arbitrage P&L per unit (USD)", pnl, 4754.35, 0.005, ".2f")
    # Break-even ETF bid: proceeds equal cost. Express as a premium of the bid over NAV.
    be_bid = cost_in / CU_SHARES
    check("break-even ETF bid for creation", be_bid, 50.1249, 5e-5, ".4f")
    check("break-even premium of the bid over NAV (bp)", (be_bid / nav - 1) * 1e4, 4.97, 0.005, ".2f")
    # Redemption leg: buy ETF at ask, redeem for basket (pay fee), sell basket (pay cost).
    be_ask = (basket_value * (1 - BASKET_COST_BP / 1e4) + CASH_COMPONENT - CREATION_FEE) / CU_SHARES
    check("break-even ETF ask for redemption", be_ask, 50.0751, 5e-5, ".4f")
    check("break-even discount of the ask to NAV (bp)", (be_ask / nav - 1) * 1e4, -4.97, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 2. Leveraged ETF decay
# ---------------------------------------------------------------------------


def leveraged_path(index_returns: list[float], lev: float) -> float:
    v = 100.0
    for r in index_returns:
        v *= 1 + lev * r
    return v


def section_leveraged() -> None:
    print("\n== 2. Leveraged and inverse ETFs ==")
    up, down = 0.10, 100 / 110 - 1  # +10%, then back to 100
    path = [up, down]
    check("index return on the way back (%)", down * 100, -9.09, 0.005, ".2f")
    check("index after +10% and back", leveraged_path(path, 1.0), 100.00, 1e-9, ".2f")
    # fi-etf-leveraged-decay
    check("2x ETF after the same two days", leveraged_path(path, 2.0), 98.18, 0.005, ".2f")
    check("-2x ETF after the same two days", leveraged_path(path, -2.0), 94.55, 0.005, ".2f")
    # Flat but choppy: ten round trips of +5% then back.
    chop = [0.05, 100 / 105 - 1] * 10
    check("2x ETF after ten +5%/-4.76% round trips", leveraged_path(chop, 2.0), 95.34, 0.005, ".2f")
    # Trending: index +1% for ten days; 2x beats twice the index return.
    trend = [0.01] * 10
    check("index after ten +1% days (%)", leveraged_path(trend, 1.0) - 100, 10.46, 0.005, ".2f")
    check("2x ETF after ten +1% days (%)", leveraged_path(trend, 2.0) - 100, 21.90, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 3. Index futures fair value
# ---------------------------------------------------------------------------

SPOT = 5000.00
R = 0.0430  # ACT/360 financing rate
DAYS = 60
DIVS = [(20, 4.00), (45, 6.50)]  # (day paid, index points), hypothetical
MULT = 50.0  # E-mini S&P 500: 50 USD x index (CME)


def fair_value(spot: float, r: float, days: int, divs: list[tuple[int, float]]) -> float:
    """Simple-interest cost of carry: S (1 + r d/360) minus each dividend carried to expiry."""
    fv_div = sum(d * (1 + r * (days - t) / 360) for t, d in divs)
    return spot * (1 + r * days / 360) - fv_div


def section_fair_value() -> float:
    print("\n== 3. Index futures fair value ==")
    fv = fair_value(SPOT, R, DAYS, DIVS)
    # Cash-flow ledger on a daily schedule: borrow SPOT and buy the index on day 0, receive each dividend on its
    # payment day and lend it, and accrue one day of simple ACT/360 interest on every principal each day.
    paid = dict(DIVS)
    debt, debt_interest, div_principal, div_interest = SPOT, 0.0, 0.0, 0.0
    for day in range(DAYS):
        div_principal += paid.get(day, 0.0)
        debt_interest += debt * R / 360
        div_interest += div_principal * R / 360
    div_cash = div_principal + div_interest
    # Delivering the index against the short future at F repays the loan net of the dividend deposits.
    check("fair value from the daily cash-flow ledger minus the closed form", debt + debt_interest - div_cash - fv, 0.0, 1e-9, ".1e")
    # fi-etf-index-fair-value, Worked example 3
    check("financing cost to expiry (index points)", debt_interest, 35.83, 0.005, ".2f")
    check("dividends carried to expiry (index points)", div_cash, 10.53, 0.005, ".2f")
    check("index futures fair value", fv, 5025.30, 0.005, ".2f")
    check("index futures fair value, four decimals", fv, 5025.3026, 5e-5, ".4f")
    check("fair value basis F - S (index points)", fv - SPOT, 25.30, 0.005, ".2f")
    f_mkt = 5031.00
    # Implied financing rate from the quoted future: solve S (1 + r d/360) - FV(divs, r) = F for r (linear in r).
    a = SPOT * DAYS / 360 - sum(d * (DAYS - t) / 360 for t, d in DIVS)
    r_impl = (f_mkt - SPOT + sum(d for _, d in DIVS)) / a
    check("implied financing rate from a 5031.00 future (%)", r_impl * 100, 4.9843, 5e-5, ".4f")
    check("implied minus actual financing (bp)", (r_impl - R) * 1e4, 68.43, 0.005, ".2f")
    return fv


# ---------------------------------------------------------------------------
# 4. Index arbitrage P&L
# ---------------------------------------------------------------------------

BASKET_COST_IDX_BP = 2.5  # one-way basket cost, bp of index value
FUT_COST_PTS = 0.10  # one-way futures cost (half-spread plus fees), index points


def section_index_arb(fv: float) -> None:
    print("\n== 4. Index arbitrage ==")
    f_mkt = 5031.00
    # Round-trip costs if held to expiry: buy basket now, sell basket in the opening auction that sets
    # the final settlement value, one futures trade (the future cash-settles at expiry).
    basket_rt = 2 * BASKET_COST_IDX_BP / 1e4 * SPOT
    band = basket_rt + FUT_COST_PTS
    check("round-trip basket cost (index points)", basket_rt, 2.50, 1e-9, ".2f")
    check("no-arbitrage half-band around fair value (index points)", band, 2.60, 1e-9, ".2f")
    check("upper band for selling the future", fv + band, 5027.90, 0.005, ".2f")
    check("lower band for buying the future", fv - band, 5022.70, 0.005, ".2f")
    edge = f_mkt - fv
    # fi-etf-index-arb-pnl, Worked example 4
    check("mispricing of a 5031.00 future (index points)", edge, 5.6974, 5e-5, ".4f")
    # Simulate the trade at expiry for three settlement values: P&L must not depend on where the index ends.
    contracts = 100
    pnls = []
    for s_t in (4600.0, 5000.0, 5400.0):
        units = 1.0  # one index unit per index point of futures exposure
        stock_pnl = units * (s_t - SPOT)  # price gain on the basket
        div_income = sum(d * (1 + R * (DAYS - t) / 360) for t, d in DIVS)
        financing = -SPOT * R * DAYS / 360
        fut_pnl = f_mkt - s_t  # short future settles to the final settlement value
        costs = -band
        pnls.append((stock_pnl + div_income + financing + fut_pnl + costs) * MULT * contracts)
    check("P&L at expiry if index ends at 4600 (USD, 100 contracts)", pnls[0], 15487, 0.5, ".0f")
    check("spread of P&L across 4600, 5000, 5400 settlements (USD)", max(pnls) - min(pnls), 0.0, 1e-6, ".1e")
    check("P&L per contract held to expiry (USD)", pnls[1] / contracts, 154.87, 0.005, ".2f")
    # Early unwind after 20 days, when the future is only 1.20 points rich to its new fair value.
    # Exact P&L per contract: basket gain + dividend received on day 20 - 20 days' financing + futures gain - costs.
    # The approximation (entry mispricing - exit mispricing - costs) ignores that financing accrues on the entry price.
    exit_mis, t1 = 1.20, 20
    approx = (edge - exit_mis - basket_rt - 2 * FUT_COST_PTS) * MULT
    check("early-unwind P&L per contract, approximation (USD)", approx, 89.87, 0.005, ".2f")
    exact = []
    for s1 in (4800.0, 5200.0):
        remaining = [(t - t1, d) for t, d in DIVS if t > t1]
        f1 = fair_value(s1, R, DAYS - t1, remaining) + exit_mis
        received = sum(d for t, d in DIVS if t <= t1)
        pts = (s1 - SPOT) + received - SPOT * R * t1 / 360 + (f_mkt - f1) - basket_rt - 2 * FUT_COST_PTS
        exact.append(pts * MULT)
    check("early-unwind P&L per contract, index down to 4800 (USD)", exact[0], 136.69, 0.005, ".2f")
    check("early-unwind P&L per contract, index up to 5200 (USD)", exact[1], 41.14, 0.005, ".2f")
    # Cause of the spread: before expiry dF/dS = 1 + r tau, so one index unit per future leaves a short delta.
    tau1 = (DAYS - t1) / 360
    check("residual delta per future at day 20 with a 1:1 hedge (index units)", 1 - (1 + R * tau1), -0.00478, 5e-6, ".5f")
    # One change: hold h = 1 + r tau1 index units per future (the carry hedge ratio); the spread disappears.
    h = 1 + R * tau1
    hedged = []
    for s1 in (4800.0, 5200.0):
        remaining = [(t - t1, d) for t, d in DIVS if t > t1]
        f1 = fair_value(s1, R, DAYS - t1, remaining) + exit_mis
        received = sum(d for t, d in DIVS if t <= t1)
        pts = h * ((s1 - SPOT) + received - SPOT * R * t1 / 360) + (f_mkt - f1) - basket_rt - 2 * FUT_COST_PTS
        hedged.append(pts * MULT)
    check("early-unwind P&L spread across 4800 and 5200 with the carry hedge ratio (USD)", hedged[1] - hedged[0], 0.0, 1e-6, ".1e")
    check("early-unwind P&L per contract with the carry hedge ratio (USD)", hedged[0], 87.02, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 5. Index inclusion flows
# ---------------------------------------------------------------------------


def section_inclusion() -> None:
    print("\n== 5. Index inclusion demand ==")
    float_cap = 40e9  # added stock, float-adjusted market cap, USD
    passive_share = 0.25  # fraction of the index's float held by funds that track it exactly
    price = 200.0
    adv = 2.5e6  # shares per day
    demand_usd = passive_share * float_cap
    demand_sh = demand_usd / price
    # fi-etf-inclusion-demand, Worked example 5
    check("passive demand (USD bn)", demand_usd / 1e9, 10.0, 1e-9, ".1f")
    check("passive demand (m shares)", demand_sh / 1e6, 50.0, 1e-9, ".1f")
    check("passive demand in days of ADV", demand_sh / adv, 20.0, 1e-9, ".1f")
    # If the trackers buy only at the closing auction on the effective date, and that auction normally prints
    # 8% of daily volume, the inclusion trade is this many times a normal closing auction.
    close_share = 0.08
    check("demand as a multiple of a normal closing auction", demand_sh / (close_share * adv), 250, 1e-9, ".0f")


if __name__ == "__main__":
    section_nav()
    section_leveraged()
    f = section_fair_value()
    section_index_arb(f)
    section_inclusion()
    if CALIBRATING:
        sys.exit(f"uncalibrated checks: {CALIBRATING}")
    print("\nAll checks passed.")
