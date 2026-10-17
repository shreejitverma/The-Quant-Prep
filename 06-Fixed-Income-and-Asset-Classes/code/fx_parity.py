"""FX forwards, covered interest parity, cross-currency basis, triangular arbitrage and FX smile quotes.

Backs 06-Fixed-Income-and-Asset-Classes/07-FX-Markets-and-Interest-Rate-Parity.md.
All market inputs are hypothetical round numbers chosen for the examples, not market data.

1. Covered interest parity with money-market day counts (EURUSD 3M, GBPUSD 1Y), forward points.
2. Cross-currency basis implied by a quoted forward, the synthetic dollar rate and the arbitrage P&L.
3. Uncovered interest parity and the carry trade.
4. Triangular arbitrage with bid and ask quotes.
5. Garman-Kohlhagen, delta-neutral ATM, 25-delta strikes from ATM, risk reversal and butterfly.

Run: uv run --no-project --with numpy python 06-Fixed-Income-and-Asset-Classes/code/fx_parity.py
"""

from __future__ import annotations

import math
import sys
from statistics import NormalDist

ND = NormalDist()
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
# 1. Covered interest parity with money-market conventions
# ---------------------------------------------------------------------------

S_EURUSD = 1.0850  # USD per EUR, hypothetical
R_USD = 0.0430  # 3M USD deposit rate, ACT/360, hypothetical
R_EUR = 0.0200  # 3M EUR deposit rate, ACT/360, hypothetical
DAYS = 91


def cip_forward(spot: float, r_quote: float, tau_quote: float, r_base: float, tau_base: float) -> float:
    """Outright forward for a pair quoted as quote-currency units per one base unit, simple money-market rates."""
    return spot * (1 + r_quote * tau_quote) / (1 + r_base * tau_base)


def section_cip() -> float:
    print("\n== 1. Covered interest parity ==")
    tau = DAYS / 360
    fwd = cip_forward(S_EURUSD, R_USD, tau, R_EUR, tau)
    # Independent check: no-arbitrage by explicit cash flows. Start with 1 USD, buy EUR spot, deposit EUR,
    # sell the EUR proceeds forward at F; this must equal depositing the USD directly.
    eur = 1 / S_EURUSD
    usd_via_eur = eur * (1 + R_EUR * tau) * fwd
    check("CIP round trip minus USD deposit (should be 0)", usd_via_eur - (1 + R_USD * tau), 0.0, 1e-12, ".1e")
    # fi-fx-cip-forward-points, Worked example 1
    check("EURUSD 3M outright forward", fwd, 1.09128, 5e-6, ".5f")
    check("EURUSD 3M forward points (pips)", (fwd - S_EURUSD) * 1e4, 62.76, 0.005, ".2f")
    check("forward points, first-order approximation S*(rd-rf)*tau (pips)", S_EURUSD * (R_USD - R_EUR) * tau * 1e4, 63.08, 0.005, ".2f")
    check("annualised forward premium of EUR (%)", (fwd / S_EURUSD - 1) / tau * 100, 2.29, 0.005, ".2f")

    # GBPUSD 1Y: GBP deposits are ACT/365, USD ACT/360 (fi-fx-day-count-gbp)
    s_gbp, r_gbp, days = 1.2700, 0.0400, 365
    fwd_gbp = cip_forward(s_gbp, R_USD, days / 360, r_gbp, days / 365)
    wrong = cip_forward(s_gbp, R_USD, days / 360, r_gbp, days / 360)
    check("GBPUSD 1Y outright forward", fwd_gbp, 1.27439, 5e-6, ".5f")
    check("GBPUSD 1Y forward points (pips)", (fwd_gbp - s_gbp) * 1e4, 43.93, 0.005, ".2f")
    check("GBPUSD 1Y points if GBP wrongly on ACT/360 (pips)", (wrong - s_gbp) * 1e4, 37.12, 0.005, ".2f")
    return fwd


# ---------------------------------------------------------------------------
# 2. Cross-currency basis implied by a quoted forward
# ---------------------------------------------------------------------------

MARKET_POINTS = 69.50  # hypothetical quoted 3M EURUSD forward points


def implied_basis(spot: float, fwd: float, r_usd: float, r_eur: float, tau: float) -> float:
    """Basis b on the EUR leg with F = S (1 + r_usd tau) / (1 + (r_eur + b) tau)."""
    return (spot * (1 + r_usd * tau) / fwd - 1) / tau - r_eur


def section_basis(cip_fwd: float) -> None:
    print("\n== 2. Cross-currency basis ==")
    tau = DAYS / 360
    f_mkt = S_EURUSD + MARKET_POINTS / 1e4
    b = implied_basis(S_EURUSD, f_mkt, R_USD, R_EUR, tau)
    check("quoted 3M EURUSD outright forward", f_mkt, 1.09195, 5e-6, ".5f")
    # Independent check of the closed form: plug b back into the parity formula and recover the quote.
    check(
        "forward rebuilt from the implied basis minus quote", cip_forward(S_EURUSD, R_USD, tau, R_EUR + b, tau) - f_mkt, 0.0, 1e-12, ".1e"
    )
    # fi-fx-basis-from-forward, Worked example 2
    check("market minus CIP forward points (pips)", (f_mkt - cip_fwd) * 1e4, 6.74, 0.005, ".2f")
    check("implied EURUSD cross-currency basis (bp)", b * 1e4, -24.53, 0.005, ".2f")
    synth_usd = ((f_mkt / S_EURUSD) * (1 + R_EUR * tau) - 1) / tau
    check("synthetic USD rate via EUR and FX swap (%)", synth_usd * 100, 4.5469, 5e-5, ".4f")
    check("synthetic minus direct USD rate (bp)", (synth_usd - R_USD) * 1e4, 24.69, 0.005, ".2f")
    # Arbitrage: borrow 100m USD at R_USD, sell USD spot for EUR, deposit EUR at R_EUR, sell EUR forward at f_mkt.
    usd = 100e6
    eur_back = usd / S_EURUSD * (1 + R_EUR * tau)
    pnl = eur_back * f_mkt - usd * (1 + R_USD * tau)
    check("arbitrage P&L at 3M on 100m USD borrowed (USD)", pnl, 62402, 1.0, ".0f")
    check("arbitrage P&L annualised (bp of notional)", pnl / usd / tau * 1e4, 24.69, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 3. Uncovered interest parity and the carry trade
# ---------------------------------------------------------------------------


def section_uip(cip_fwd: float) -> None:
    print("\n== 3. UIP and carry ==")
    tau = DAYS / 360

    # Carry trade: hold USD (high yield) funded in EUR (low yield), unhedged. Return in USD per EUR borrowed.
    # Borrow 1 EUR at R_EUR, sell for S USD, deposit at R_USD, at 3M buy back 1 + R_EUR tau EUR at spot S_T.
    def carry_pnl(s_t: float) -> float:
        return S_EURUSD * (1 + R_USD * tau) - (1 + R_EUR * tau) * s_t

    # fi-fx-uip-carry
    check("carry P&L if spot unchanged (USD per EUR borrowed)", carry_pnl(S_EURUSD), 0.00631, 5e-6, ".5f")
    check("carry P&L if spot ends at the forward (USD)", carry_pnl(cip_fwd), 0.0, 1e-12, ".1e")
    breakeven = S_EURUSD * (1 + R_USD * tau) / (1 + R_EUR * tau)
    check("break-even EURUSD at 3M for the carry trade", breakeven, 1.09128, 5e-6, ".5f")
    check("EUR appreciation that wipes out the carry (%)", (breakeven / S_EURUSD - 1) * 100, 0.58, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 4. Triangular arbitrage
# ---------------------------------------------------------------------------


def section_triangle() -> None:
    print("\n== 4. Triangular arbitrage ==")
    eurusd = (1.0848, 1.0850)  # bid, ask: USD per EUR
    usdjpy = (151.20, 151.22)  # JPY per USD
    eurjpy = (164.10, 164.14)  # JPY per EUR, market quote
    implied_bid = eurusd[0] * usdjpy[0]  # sell EUR for USD at bid, sell USD for JPY at bid
    implied_ask = eurusd[1] * usdjpy[1]  # buy EUR with USD at ask, buy USD with JPY at ask
    # fi-fx-triangular-arb, Worked example 3
    check("implied EURJPY bid", implied_bid, 164.02, 0.005, ".2f")
    check("implied EURJPY ask", implied_ask, 164.07, 0.005, ".2f")
    # Market bid 164.10 is above the implied ask: buy EUR synthetically, sell EUR in EURJPY.
    notional_eur = 1e6
    jpy_in = notional_eur * eurjpy[0]
    usd_needed = notional_eur * eurusd[1]
    jpy_out = usd_needed * usdjpy[1]
    check("JPY paid for the USD leg (m JPY)", jpy_out / 1e6, 164.0737, 5e-5, ".4f")
    profit = jpy_in - jpy_out
    check("triangular arbitrage profit on 1m EUR (JPY)", profit, 26300, 0.5, ".0f")
    check("profit in USD at the USDJPY ask", profit / usdjpy[1], 173.92, 0.005, ".2f")
    # Brute force: try all 8 direction combinations around the triangle and keep the best round trip.
    best = 0.0
    for start_ccy_pnl in (
        eurjpy[0] / (eurusd[1] * usdjpy[1]),  # EUR->JPY at bid, JPY->USD at ask, USD->EUR at ask
        (eurusd[0] * usdjpy[0]) / eurjpy[1],  # EUR->USD at bid, USD->JPY at bid, JPY->EUR at ask
    ):
        best = max(best, start_ccy_pnl - 1)
    check("best round-trip return around the triangle (bp)", best * 1e4, 1.60, 0.005, ".2f")


# ---------------------------------------------------------------------------
# 5. Garman-Kohlhagen and the smile quotes
# ---------------------------------------------------------------------------

T_OPT = 0.25
RD_C, RF_C = 0.0430, 0.0200  # continuously compounded USD and EUR rates, hypothetical
SIG_ATM, RR25, BF25 = 0.0750, -0.0060, 0.0025  # hypothetical quotes


def gk(spot: float, k: float, t: float, rd: float, rf: float, sig: float, call: bool) -> float:
    fwd = spot * math.exp((rd - rf) * t)
    d1 = (math.log(fwd / k) + 0.5 * sig * sig * t) / (sig * math.sqrt(t))
    d2 = d1 - sig * math.sqrt(t)
    if call:
        return math.exp(-rd * t) * (fwd * ND.cdf(d1) - k * ND.cdf(d2))
    return math.exp(-rd * t) * (k * ND.cdf(-d2) - fwd * ND.cdf(-d1))


def fwd_delta(fwd: float, k: float, t: float, sig: float, call: bool) -> float:
    d1 = (math.log(fwd / k) + 0.5 * sig * sig * t) / (sig * math.sqrt(t))
    return ND.cdf(d1) if call else -ND.cdf(-d1)


def strike_from_fwd_delta(fwd: float, delta: float, t: float, sig: float, call: bool) -> float:
    srt = sig * math.sqrt(t)
    if call:
        return fwd * math.exp(-srt * ND.inv_cdf(delta) + 0.5 * sig * sig * t)
    return fwd * math.exp(srt * ND.inv_cdf(-delta) + 0.5 * sig * sig * t)


def section_smile() -> None:
    print("\n== 5. FX options: Garman-Kohlhagen and smile quotes ==")
    fwd = S_EURUSD * math.exp((RD_C - RF_C) * T_OPT)
    check("EURUSD 3M forward, continuous rates", fwd, 1.09126, 5e-6, ".5f")
    k_atm = fwd * math.exp(0.5 * SIG_ATM**2 * T_OPT)
    check("delta-neutral ATM strike", k_atm, 1.09202, 5e-6, ".5f")
    # Independent check: call and put forward deltas at the DNS strike sum to zero.
    dsum = fwd_delta(fwd, k_atm, T_OPT, SIG_ATM, True) + fwd_delta(fwd, k_atm, T_OPT, SIG_ATM, False)
    check("call delta + put delta at the DNS strike", dsum, 0.0, 1e-12, ".1e")
    c_atm = gk(S_EURUSD, k_atm, T_OPT, RD_C, RF_C, SIG_ATM, True)
    p_atm = gk(S_EURUSD, k_atm, T_OPT, RD_C, RF_C, SIG_ATM, False)
    check("ATM call premium (USD pips per EUR)", c_atm * 1e4, 157.79, 0.005, ".2f")
    check("put-call parity residual C - P - DF*(F - K)", c_atm - p_atm - math.exp(-RD_C * T_OPT) * (fwd - k_atm), 0.0, 1e-12, ".1e")
    check("ATM call premium (% of EUR notional)", c_atm / S_EURUSD * 100, 1.45, 0.005, ".2f")
    # Smile from ATM, 25-delta risk reversal and (smile) butterfly: fi-fx-rr-bf-vols
    sig_c = SIG_ATM + BF25 + RR25 / 2
    sig_p = SIG_ATM + BF25 - RR25 / 2
    check("25-delta call vol (%)", sig_c * 100, 7.45, 1e-9, ".2f")
    check("25-delta put vol (%)", sig_p * 100, 8.05, 1e-9, ".2f")
    k_c = strike_from_fwd_delta(fwd, 0.25, T_OPT, sig_c, True)
    k_p = strike_from_fwd_delta(fwd, -0.25, T_OPT, sig_p, False)
    check("25-delta call strike", k_c, 1.11980, 5e-6, ".5f")
    check("25-delta put strike", k_p, 1.06289, 5e-6, ".5f")
    # Independent check: recompute the deltas at the solved strikes.
    check("forward delta at the 25-delta call strike", fwd_delta(fwd, k_c, T_OPT, sig_c, True), 0.2500, 1e-12, ".4f")
    check("forward delta at the 25-delta put strike", fwd_delta(fwd, k_p, T_OPT, sig_p, False), -0.2500, 1e-12, ".4f")


if __name__ == "__main__":
    f = section_cip()
    section_basis(f)
    section_uip(f)
    section_triangle()
    section_smile()
    if CALIBRATING:
        sys.exit(f"uncalibrated checks: {CALIBRATING}")
    print("\nAll checks passed.")
