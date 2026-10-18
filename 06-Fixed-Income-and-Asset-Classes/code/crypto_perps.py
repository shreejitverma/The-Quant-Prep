"""Crypto market structure: perpetual funding, basis trades, margin, inverse contracts and AMM mechanics.

Backs 06-Fixed-Income-and-Asset-Classes/10-Crypto-Market-Structure.md.
Prices, fees, leverage and pool sizes are hypothetical and chosen for the examples, not market data.
Rule inputs and their sources (as of 2026-10):
- Funding rate F = P + clamp(I - P, -0.05%, +0.05%), I = 0.01% per 8-hour interval, payments every 8 hours,
  longs pay shorts when F > 0, payment = position notional at mark x F (Binance Futures funding-rate FAQ).
- Constant-product AMM x * y = k with a 0.30% fee taken from the input (Uniswap v2 Core whitepaper, March 2020).

1. Premium index and funding rate, the dead band, a funding payment, the baseline annualised rate.
2. Perpetual and dated-futures cash-and-carry.
3. Liquidation distance of the short leg (simplified isolated-margin model).
4. Inverse (coin-margined) contracts: double exposure for longs, a synthetic dollar for shorts.
5. Constant-product AMM: execution price, price impact, a sandwich, impermanent loss and LVR.
6. Cross-venue arbitrage with pre-funded inventory.

Run: uv run --no-project --with numpy python 06-Fixed-Income-and-Asset-Classes/code/crypto_perps.py
"""

from __future__ import annotations

import math
import sys

import numpy as np

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


INTEREST = 0.0001  # 0.01% per 8-hour interval
CLAMP = 0.0005  # +/- 0.05%


def premium_index(impact_bid: float, impact_ask: float, index: float) -> float:
    return (max(0.0, impact_bid - index) - max(0.0, index - impact_ask)) / index


def funding_rate(premium: float) -> float:
    return premium + min(max(INTEREST - premium, -CLAMP), CLAMP)


# ---------------------------------------------------------------------------
# 1. Funding
# ---------------------------------------------------------------------------


def section_funding() -> None:
    print("\n== 1. Premium index and funding ==")
    p = premium_index(60045.0, 60060.0, 60000.0)
    # fi-crypto-premium-index, Worked example 1
    check("premium index, impact bid 60045 vs index 60000 (%)", p * 100, 0.0750, 1e-9, ".4f")
    check("interest minus premium before the clamp (%)", (INTEREST - p) * 100, -0.065, 1e-9, ".3f")
    check("funding rate at premium 0.075% (%)", funding_rate(p) * 100, 0.0250, 1e-9, ".4f")
    # fi-crypto-funding-clamp
    check("funding rate at premium 0.03% (%)", funding_rate(0.0003) * 100, 0.0100, 1e-9, ".4f")
    check("funding rate at premium -0.02% (%)", funding_rate(-0.0002) * 100, 0.0100, 1e-9, ".4f")
    check("interest minus premium at premium -0.10% (%)", (INTEREST + 0.0010) * 100, 0.11, 1e-9, ".2f")
    check("funding rate at premium -0.10% (%)", funding_rate(-0.0010) * 100, -0.0500, 1e-9, ".4f")
    # Brute force the dead band: premiums (in 0.001% steps) where funding equals the interest rate exactly.
    grid = [i / 1e5 for i in range(-300, 301)]
    band = [x for x in grid if abs(funding_rate(x) - INTEREST) < 1e-15]
    check("dead band lower edge (premium, %)", min(band) * 100, -0.04, 1e-9, ".2f")
    check("dead band upper edge (premium, %)", max(band) * 100, 0.06, 1e-9, ".2f")
    # fi-crypto-baseline-funding-apr
    check("baseline funding annualised, 3 x 365 intervals (%)", INTEREST * 3 * 365 * 100, 10.95, 1e-9, ".2f")
    check("baseline funding compounded (%)", ((1 + INTEREST) ** (3 * 365) - 1) * 100, 11.57, 0.005, ".2f")
    check("funding on 1m USD at +0.03% (USD)", 1e6 * 0.0003, 300.0, 1e-9, ".0f")
    pay = 2 * 60000.0 * funding_rate(0.0003)
    check("funding paid by a 2 BTC long at mark 60000, premium 0.03% (USD)", pay, 12.00, 1e-6, ".2f")


# ---------------------------------------------------------------------------
# 2. Cash-and-carry
# ---------------------------------------------------------------------------


def section_carry() -> None:
    print("\n== 2. Cash-and-carry ==")
    qty, px, days = 10.0, 60000.0, 30
    notional = qty * px
    intervals = days * 3
    collected = notional * INTEREST * intervals
    fees = 4 * 0.0005 * notional  # taker 0.05% on spot and perp, entry and exit (hypothetical)
    check("taker fee per leg per trade (USD)", 0.0005 * notional, 300.0, 1e-9, ".0f")
    # fi-crypto-perp-carry, Worked example 2
    check("funding collected on 10 BTC short perp over 30 days at 0.01% (USD)", collected, 5400, 1e-6, ".0f")
    check("round-trip taker fees on both legs (USD)", fees, 1200, 1e-6, ".0f")
    check("net carry (USD)", collected - fees, 4200, 1e-6, ".0f")
    check("net carry annualised (%)", (collected - fees) / notional * 365 / days * 100, 8.52, 0.005, ".2f")
    # Simulation on a random mark path. The spot leg is valued from its entry and exit prices only. The perp leg
    # is settled interval by interval from its own cash flows: variation margin on the mark move, then the funding
    # payment on the mark notional at the funding time (the short receives when the rate is positive).
    rng = np.random.default_rng(7)
    path = px * np.exp(np.cumsum(rng.normal(0, 0.01, intervals)))
    path = np.concatenate([[px], path])
    spot_pnl = qty * (path[-1] - px)
    perp_cash = 0.0
    funding = 0.0
    for m0, m1 in zip(path[:-1], path[1:], strict=True):
        payment = qty * m0 * funding_rate(0.0)
        funding += payment
        perp_cash += -qty * (m1 - m0) + payment
    check("spot P&L plus perp cash flows minus funding received, random path (USD)", spot_pnl + perp_cash - funding, 0.0, 1e-6, ".1e")
    check("funding collected on that path (USD, seed 7)", funding, 4829, 0.5, ".0f")
    # Dated future: quarterly at 61500 with 90 days left.
    f, d = 61500.0, 90
    check("annualised basis of a 90-day future at 61500 (%)", (f / px - 1) * 365 / d * 100, 10.14, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 3. Liquidation distance of the short leg
# ---------------------------------------------------------------------------


def short_liq_price(p0: float, lev: float, mm: float) -> float:
    """Isolated short, collateral p0/lev per unit, liquidated when equity equals mm x notional at mark."""
    return p0 * (1 + 1 / lev) / (1 + mm)


def section_liquidation() -> None:
    print("\n== 3. Liquidation of the short leg ==")
    p0, mm = 60000.0, 0.005
    for lev in (3.0, 5.0):
        liq = short_liq_price(p0, lev, mm)
        # Independent check: equity at the liquidation price equals the maintenance requirement.
        equity = p0 / lev - (liq - p0)
        assert abs(equity - mm * liq) < 1e-6
        if lev == 3.0:
            # fi-crypto-short-leg-liquidation
            check("short liquidation price at 3x, mm 0.5% (USD)", liq, 79602, 0.5, ".0f")
            check("rally to liquidation at 3x (%)", (liq / p0 - 1) * 100, 32.67, 0.005, ".2f")
        else:
            check("short liquidation price at 5x, mm 0.5% (USD)", liq, 71642, 0.5, ".0f")
            check("rally to liquidation at 5x (%)", (liq / p0 - 1) * 100, 19.40, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 4. Inverse contracts
# ---------------------------------------------------------------------------


def inverse_pnl_btc(usd_notional: float, p0: float, p1: float, long: bool) -> float:
    sign = 1.0 if long else -1.0
    return sign * usd_notional * (1 / p0 - 1 / p1)


def section_inverse() -> None:
    print("\n== 4. Inverse contracts ==")
    n, p0 = 60000.0, 60000.0
    # fi-crypto-inverse-contract, Worked example 3
    check("inverse long 60000 USD, BTC 60000 to 75000 (BTC P&L)", inverse_pnl_btc(n, p0, 75000.0, True), 0.2000, 1e-9, ".4f")
    check("inverse long 60000 USD, BTC 60000 to 45000 (BTC P&L)", inverse_pnl_btc(n, p0, 45000.0, True), -0.3333, 5e-5, ".4f")
    btc_left = 1 + inverse_pnl_btc(n, p0, 45000.0, True)
    check("BTC left in the account after the fall", btc_left, 0.6667, 5e-5, ".4f")
    eq_long = btc_left * 45000.0
    check("USD equity of 1 BTC collateral plus inverse long at 45000", eq_long, 30000, 1e-6, ".0f")
    check("USD return of that account for a -25% BTC move (%)", (eq_long / 60000.0 - 1) * 100, -50.00, 1e-9, ".2f")
    for p1 in (45000.0, 75000.0, 120000.0):
        eq_short = (1 + inverse_pnl_btc(n, p0, p1, False)) * p1
        check(f"USD equity of 1 BTC collateral plus inverse short at {p1:.0f}", eq_short, 60000.0, 1e-6, ".0f")


# ---------------------------------------------------------------------------
# 5. Constant-product AMM
# ---------------------------------------------------------------------------

FEE = 0.003


def swap_usdc_for_eth(x_eth: float, y_usdc: float, usdc_in: float) -> tuple[float, float, float]:
    """Return (eth_out, new_x, new_y). The fee stays in the pool, as in Uniswap v2."""
    eff = usdc_in * (1 - FEE)
    eth_out = x_eth * eff / (y_usdc + eff)
    return eth_out, x_eth - eth_out, y_usdc + usdc_in


def swap_eth_for_usdc(x_eth: float, y_usdc: float, eth_in: float) -> tuple[float, float, float]:
    eff = eth_in * (1 - FEE)
    usdc_out = y_usdc * eff / (x_eth + eff)
    return usdc_out, x_eth + eth_in, y_usdc - usdc_out


def section_amm() -> None:
    print("\n== 5. Constant-product AMM ==")
    x, y = 1000.0, 3_000_000.0
    out, x1, y1 = swap_usdc_for_eth(x, y, 30_000.0)
    check("USDC input after the 0.30% fee", 30_000.0 * (1 - FEE), 29910.0, 1e-6, ".0f")
    # Invariant check (v2 requires the product not to fall).
    assert x1 * y1 >= x * y
    # fi-crypto-amm-price-impact, Worked example 4
    check("ETH received for 30000 USDC", out, 9.8716, 5e-5, ".4f")
    check("average execution price (USDC per ETH)", 30_000.0 / out, 3039.03, 0.005, ".2f")
    check("cost versus the 3000 pool price (%)", (30_000.0 / out / 3000 - 1) * 100, 1.30, 0.005, ".2f")
    check("pool price after the trade", y1 / x1, 3060.21, 0.005, ".2f")
    # Sandwich: attacker buys 60000 USDC of ETH first, victim trades, attacker sells the ETH back.
    a_eth, xa, ya = swap_usdc_for_eth(x, y, 60_000.0)
    v_eth, xb, yb = swap_usdc_for_eth(xa, ya, 30_000.0)
    a_usdc, _, _ = swap_eth_for_usdc(xb, yb, a_eth)
    # fi-crypto-sandwich
    check("victim ETH received when sandwiched", v_eth, 9.4907, 5e-5, ".4f")
    check("victim shortfall versus no attack (ETH)", out - v_eth, 0.3809, 5e-5, ".4f")
    check("attacker profit before gas (USDC)", a_usdc - 60_000.0, 809.48, 0.005, ".2f")
    # Impermanent loss: closed form against the pool's reserves after no-fee re-arbitrage to the new price.
    for r in (2.0, 0.5, 1.25):
        k = x * y
        p0 = y / x
        p1 = p0 * r
        x_new = math.sqrt(k / p1)
        y_new = math.sqrt(k * p1)
        lp = x_new * p1 + y_new
        hodl = x * p1 + y
        from_reserves = lp / hodl - 1
        closed = 2 * math.sqrt(r) / (1 + r) - 1
        assert abs(from_reserves - closed) < 1e-12
    # fi-crypto-impermanent-loss
    check("impermanent loss at a 2x price move (%)", (2 * math.sqrt(2.0) / 3 - 1) * 100, -5.72, 0.005, ".2f")
    check("impermanent loss at a 0.5x price move (%)", (2 * math.sqrt(0.5) / 1.5 - 1) * 100, -5.72, 0.005, ".2f")
    check("impermanent loss at a 1.25x price move (%)", (2 * math.sqrt(1.25) / 2.25 - 1) * 100, -0.62, 0.005, ".2f")
    # LVR: sigma^2 / 8 of pool value per year. Monte Carlo with hourly arbitrage, no fees, zero drift.
    sigma = 0.60
    check("LVR at sigma 60%, closed form (% of pool value per year)", sigma**2 / 8 * 100, 4.50, 1e-9, ".2f")
    rng = np.random.default_rng(11)
    n_paths, steps, t_years = 4000, 24 * 30, 30 / 365
    dt = t_years / steps
    z = rng.standard_normal((n_paths, steps))
    logp = np.cumsum(sigma * math.sqrt(dt) * z - 0.5 * sigma**2 * dt, axis=1)
    price = 3000.0 * np.exp(np.concatenate([np.zeros((n_paths, 1)), logp], axis=1))
    k = x * y
    eth_held = np.sqrt(k / price)  # pool ETH after arbitrage at each price
    value = 2 * np.sqrt(k * price)
    rebalance_pnl = np.sum(eth_held[:, :-1] * np.diff(price, axis=1), axis=1)
    lvr = rebalance_pnl - (value[:, -1] - value[:, 0])
    lvr_annual_pct = float(np.mean(lvr) / value[0, 0] / t_years * 100)
    check("LVR by Monte Carlo, hourly arbitrage, 30 days (% per year, seed 11)", lvr_annual_pct, 4.50, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 6. Cross-venue arbitrage
# ---------------------------------------------------------------------------


def section_cross_venue() -> None:
    print("\n== 6. Cross-venue arbitrage ==")
    ask_a, bid_b, fee = 60000.0, 60150.0, 0.0005
    pnl = (bid_b - ask_a) - fee * (ask_a + bid_b)
    # fi-crypto-cross-venue
    check("cross-venue P&L per BTC after taker fees (USD)", pnl, 89.925, 1e-6, ".3f")
    # Break-even gap g solves g = fee * (ask + ask + g).
    check("break-even gap at 0.05% taker fees on both venues (USD)", 2 * fee * ask_a / (1 - fee), 60.03, 0.005, ".2f")


if __name__ == "__main__":
    section_funding()
    section_carry()
    section_liquidation()
    section_inverse()
    section_amm()
    section_cross_venue()
    if CALIBRATING:
        sys.exit(f"uncalibrated checks: {CALIBRATING}")
    print("\nAll checks passed.")
