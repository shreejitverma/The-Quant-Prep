"""Commodity futures curves: carry, convenience yield, roll yield, calendar spreads and storage arbitrage.

Backs 06-Fixed-Income-and-Asset-Classes/09-Commodities-and-Futures-Curves.md.
Every curve, rate and cost below is hypothetical and chosen for the examples; none is market data.
The one contract term used, 1,000 barrels per NYMEX WTI futures contract, is from the CFTC interim staff
report on the April 20, 2020 WTI episode (2020-11-23).

1. Implied convenience yield from adjacent futures.
2. Roll yield on an unchanged curve, in backwardation and contango, and a 12-month rolling index.
3. Exact decomposition of a rolled futures position into spot return plus roll return.
4. Full-carry bound and cash-and-carry with storage (the April 2020 "super contango" logic).
5. Calendar spread P&L, and a seasonal gas storage trade.

Run: uv run --no-project --with numpy python 06-Fixed-Income-and-Asset-Classes/code/commodity_curves.py
"""

from __future__ import annotations

import math
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


# Hypothetical monthly curves, USD per barrel, front month first.
BACKWARDATED = [80.00, 79.40, 78.85, 78.35, 77.90, 77.50, 77.15, 76.85, 76.60, 76.40, 76.25, 76.15]
CONTANGO = [70.00, 70.70, 71.35, 71.95, 72.50, 73.00, 73.45, 73.85, 74.20, 74.50, 74.75, 74.95]
R = 0.045  # continuously compounded financing rate
U = 0.030  # storage cost as a continuous yield on value
BBL_PER_CONTRACT = 1000  # NYMEX WTI (CFTC interim staff report, 2020-11-23)


# ---------------------------------------------------------------------------
# 1. Implied convenience yield
# ---------------------------------------------------------------------------


def implied_conv_yield(f_near: float, f_far: float, dt: float) -> float:
    """y from F_far = F_near exp((r + u - y) dt)."""
    return R + U - math.log(f_far / f_near) / dt


def section_conv_yield() -> None:
    print("\n== 1. Implied convenience yield ==")
    dt = 1 / 12
    y_b = implied_conv_yield(BACKWARDATED[0], BACKWARDATED[1], dt)
    y_c = implied_conv_yield(CONTANGO[0], CONTANGO[1], dt)
    # Independent check: rebuild M2 from M1 and the implied yield.
    check("M2 rebuilt from M1 and y, minus M2", BACKWARDATED[0] * math.exp((R + U - y_b) * dt) - BACKWARDATED[1], 0.0, 1e-9, ".1e")
    # fi-cmdty-convenience-yield, Worked example 1
    check("implied convenience yield M1-M2, backwardated curve (%)", y_b * 100, 16.53, 0.005, ".2f")
    check("implied convenience yield M1-M2, contango curve (%)", y_c * 100, -4.44, 0.005, ".2f")
    y_b_back = implied_conv_yield(BACKWARDATED[10], BACKWARDATED[11], dt)
    check("implied convenience yield M11-M12, backwardated curve (%)", y_b_back * 100, 9.07, 0.005, ".2f")
    check("12-month slope of backwardated curve (M12/M1 - 1, %)", (BACKWARDATED[11] / BACKWARDATED[0] - 1) * 100, -4.81, 0.005, ".2f")
    check("12-month slope of contango curve (M12/M1 - 1, %)", (CONTANGO[11] / CONTANGO[0] - 1) * 100, 7.07, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 2. Roll yield on an unchanged curve
# ---------------------------------------------------------------------------


def roll_yield_one_month(curve: list[float]) -> float:
    """Hold M2 for a month; if the curve is unchanged it becomes M1. Return (M1 - M2) / M2."""
    return curve[0] / curve[1] - 1


def section_roll() -> None:
    print("\n== 2. Roll yield ==")
    rb = roll_yield_one_month(BACKWARDATED)
    rc = roll_yield_one_month(CONTANGO)
    # fi-cmdty-roll-yield, Worked example 2
    check("one-month roll yield, backwardated (%)", rb * 100, 0.756, 0.0005, ".3f")
    check("one-month roll yield, contango (%)", rc * 100, -0.990, 0.0005, ".3f")
    check("annualised roll yield, backwardated (% compounded)", ((1 + rb) ** 12 - 1) * 100, 9.45, 0.005, ".2f")
    check("annualised roll yield, contango (% compounded)", ((1 + rc) ** 12 - 1) * 100, -11.26, 0.005, ".2f")

    # Brute force: a long position that buys M2, holds a month, sells it as M1 and rebuys M2, for 12 months,
    # with the spot (M1) and the whole curve unchanged. Spot return is zero; the whole P&L is roll.
    def rolled_wealth(curve: list[float]) -> float:
        wealth = 1.0
        for _ in range(12):
            wealth = wealth / curve[1] * curve[0]  # buy M2 with all wealth, sell it a month later as M1
        return wealth

    check("12-month rolling excess return, backwardated, spot unchanged (%)", (rolled_wealth(BACKWARDATED) - 1) * 100, 9.45, 0.005, ".2f")
    check("12-month rolling excess return, contango, spot unchanged (%)", (rolled_wealth(CONTANGO) - 1) * 100, -11.26, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 3. Spot plus roll decomposition with a moving curve
# ---------------------------------------------------------------------------


def section_decomposition() -> None:
    print("\n== 3. Spot plus roll decomposition ==")
    shape = [p / CONTANGO[0] for p in CONTANGO]  # curve = spot x fixed shape
    spot_path = [70.0, 74.0, 69.0, 72.0, 77.0, 75.0, 71.0]  # hypothetical monthly M1 prices
    log_fut = 0.0
    log_spot = 0.0
    log_roll = 0.0
    for s0, s1 in zip(spot_path[:-1], spot_path[1:], strict=True):
        f_buy = s0 * shape[1]  # buy M2
        f_sell = s1 * shape[0]  # one month later it is M1
        log_fut += math.log(f_sell / f_buy)
        log_spot += math.log(s1 / s0)
        log_roll += math.log(shape[0] / shape[1])
    # fi-cmdty-spot-plus-roll
    check("futures log return minus (spot + roll) log return", log_fut - (log_spot + log_roll), 0.0, 1e-12, ".1e")
    check("6-month spot return, M1 70 to 71 (%)", (math.exp(log_spot) - 1) * 100, 1.43, 0.005, ".2f")
    check("6-month rolled futures return in contango (%)", (math.exp(log_fut) - 1) * 100, -4.45, 0.005, ".2f")
    check("6-month roll return in contango (%)", (math.exp(log_roll) - 1) * 100, -5.80, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 4. Full carry and storage arbitrage
# ---------------------------------------------------------------------------


def section_full_carry() -> None:
    print("\n== 4. Full-carry bound ==")
    m1 = 70.00
    storage_per_month = 0.50  # USD per barrel per month, hypothetical leased tank cost
    full_carry = m1 * math.exp(R / 12) + storage_per_month
    # fi-cmdty-full-carry, Worked example 3
    check("full-carry M2 price (USD/bbl)", full_carry, 70.76, 0.005, ".2f")
    check("full-carry M2-M1 spread (USD/bbl)", full_carry - m1, 0.76, 0.005, ".2f")
    m2_quote = 71.20
    edge = m2_quote - full_carry
    check("cash-and-carry profit per barrel at M2 = 71.20", edge, 0.44, 0.005, ".2f")
    check("cash-and-carry profit per contract (USD)", edge * BBL_PER_CONTRACT, 437, 0.5, ".0f")
    # Same spread with storage at 2.00 per barrel-month (tanks almost full): no arbitrage.
    tight = m1 * math.exp(R / 12) + 2.00
    check("full-carry M2 with storage at 2.00 per barrel-month", tight, 72.26, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 5. Calendar spread and seasonal storage
# ---------------------------------------------------------------------------


def section_spreads() -> None:
    print("\n== 5. Calendar spreads and seasonal storage ==")
    spread0 = BACKWARDATED[0] - BACKWARDATED[1]
    # fi-cmdty-calendar-spread, Worked example 4
    check("M1-M2 spread, backwardated curve (USD/bbl)", spread0, 0.60, 1e-9, ".2f")
    spread1 = 1.10  # after a supply shock the front tightens
    pnl = (spread1 - spread0) * BBL_PER_CONTRACT * 10  # long 10 spreads: long M1, short M2
    check("P&L of long 10 M1-M2 spreads when the spread widens to 1.10 (USD)", pnl, 5000, 0.5, ".0f")
    # Outright exposure: a parallel 5 USD fall in the whole curve leaves the spread unchanged.
    m1_new, m2_new = BACKWARDATED[0] - 5, BACKWARDATED[1] - 5
    check("spread P&L from a parallel 5 USD shift (USD)", ((m1_new - m2_new) - spread0) * BBL_PER_CONTRACT * 10, 0.0, 1e-6, ".1e")

    # Seasonal gas: buy April, inject, withdraw and sell January (9 months). Prices in USD per MMBtu.
    apr, jan = 2.80, 3.90
    storage_fee = 0.45  # per MMBtu for the season, hypothetical
    fuel_loss = 0.01  # fraction of gas used in injection and withdrawal
    fin = math.exp(R * 9 / 12) - 1
    cost = apr * (1 + fin) + storage_fee
    revenue = jan * (1 - fuel_loss)
    # fi-cmdty-gas-storage, Worked example 5
    check("gas calendar spread Jan - Apr (USD/MMBtu)", jan - apr, 1.10, 1e-9, ".2f")
    check("financing cost on April gas for 9 months (USD/MMBtu)", apr * fin, 0.096, 0.0005, ".3f")
    check("January revenue net of 1% fuel loss (USD/MMBtu)", revenue, 3.861, 1e-9, ".3f")
    check("seasonal storage profit (USD/MMBtu)", revenue - cost, 0.515, 0.0005, ".3f")
    check("break-even Jan - Apr spread (USD/MMBtu)", cost / (1 - fuel_loss) - apr, 0.580, 0.0005, ".3f")


if __name__ == "__main__":
    section_conv_yield()
    section_roll()
    section_decomposition()
    section_full_carry()
    section_spreads()
    if CALIBRATING:
        sys.exit(f"uncalibrated checks: {CALIBRATING}")
    print("\nAll checks passed.")
