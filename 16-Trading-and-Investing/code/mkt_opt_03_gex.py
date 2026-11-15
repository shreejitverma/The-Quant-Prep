"""Dealer positioning and GEX: every number in 03-Options-and-Volatility/03-Dealer-Positioning-and-GEX.md.

The GEX sign convention (dealers long the calls and short the puts in open interest) is an assumption stated in the
note, not a fact about who holds what; the script only checks the arithmetic under that assumption.
Independent routes used here:
- dollar GEX from the gamma formula is compared with the dealer hedge trade obtained by repricing the book's delta
  at spot +/- 0.5% (a central finite difference of closed-form deltas, no gamma formula used);
- the zero-gamma flip point of the two-strike book is found by bisection on finite-difference gamma;
- the vanna estimate of the hedge flow is compared with full Black-Scholes revaluation of the put delta, and vanna
  itself with a finite difference of delta in volatility.
Run: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_opt_03_gex.py
"""

from __future__ import annotations

import math

from mkt_assets_lib import bisect, bs_greeks, close, norm_cdf, norm_pdf, q


def example_1() -> None:
    print("Example 1: two-strike book, S = 5000, 14 days, 16% vol, multiplier 100")
    S, T, s, M = 5000.0, 14 / 365, 0.16, 100
    oi_call, oi_put = 50_000, 70_000
    q("T", T, "0.03836")
    q("sqrt(T)", math.sqrt(T), "0.19585")
    q("sigma sqrt(T)", s * math.sqrt(T), "0.031336")
    q("S sigma sqrt(T)", S * s * math.sqrt(T), "156.68")
    gc = bs_greeks(S, 5050.0, T, 0.0, 0.0, s)
    gp = bs_greeks(S, 4950.0, T, 0.0, 0.0, s, call=False)
    q("ln(5000/5050)", math.log(5000 / 5050), "-0.009950")
    q("0.5 sigma^2 T", 0.5 * s * s * T, "0.000491")
    q("ln(5000/4950)", math.log(5000 / 4950), "0.010050")
    q("d1 (5050 call)", gc["d1"], "-0.3019")
    q("phi(d1) (5050 call)", norm_pdf(gc["d1"]), "0.38117")
    q("gamma (5050 call)", gc["gamma"], "0.002433")
    q("d1 (4950 put)", gp["d1"], "0.3364")
    q("phi(d1) (4950 put)", norm_pdf(gp["d1"]), "0.37700")
    q("gamma (4950 put)", gp["gamma"], "0.002406")
    q("gamma (5050 call), five significant figures", gc["gamma"], "0.0024328")
    q("gamma (4950 put), five significant figures", gp["gamma"], "0.0024062")
    call_gex = oi_call * M * gc["gamma"] * S
    put_gex = -oi_put * M * gp["gamma"] * S
    q("call GEX ($m of delta per point)", call_gex / 1e6, "60.82")
    q("put GEX ($m of delta per point)", put_gex / 1e6, "-84.22")
    net = call_gex + put_gex
    q("net GEX ($m per point)", net / 1e6, "-23.40")
    dollar = net * S / 100
    q("net GEX ($m per point), three decimals", net / 1e6, "-23.395")
    q("dollar GEX per 1% move ($m)", dollar / 1e6, "-1,169.8")
    q("dollar GEX in $bn", dollar / 1e9, "-1.17")

    def dealer_delta(spot: float) -> float:
        c = bs_greeks(spot, 5050.0, T, 0.0, 0.0, s)["delta"]
        p = bs_greeks(spot, 4950.0, T, 0.0, 0.0, s, call=False)["delta"]
        return oi_call * M * c - oi_put * M * p  # long calls, short puts (the convention)

    h = 0.005 * S
    flow = -(dealer_delta(S + h) - dealer_delta(S - h)) * S  # $ the dealer must buy for a 1% rally (negative = sell)
    q("dealer buying for a 1% rally from repriced deltas ($bn)", flow / 1e9, "1.167")
    close("dollar GEX vs hedge trade from repriced deltas (relative)", -flow / dollar, 1.0, 3e-3)

    def gamma_fd(spot: float) -> float:
        e = 0.5
        return (dealer_delta(spot + e) - dealer_delta(spot - e)) / (2 * e)

    flip = bisect(gamma_fd, 4950.0, 5100.0, tol=1e-6)
    q("zero-gamma flip point of this book", flip, "5,081")
    assert gamma_fd(5000.0) < 0 < gamma_fd(5100.0)


def example_2() -> None:
    print("Example 2: short 100,000 4800 puts (10,000,000 index units), implied vol 20% -> 17%")
    S, K, T, s, units = 5000.0, 4800.0, 30 / 365, 0.20, 10_000_000
    g = bs_greeks(S, K, T, 0.0, 0.0, s, call=False)
    q("ln(5000/4800)", math.log(S / K), "0.040822")
    q("0.5 sigma^2 T", 0.5 * s * s * T, "0.001644")
    q("d1", g["d1"], "0.7406")
    q("d2", g["d2"], "0.6833")
    q("N(d1)", norm_cdf(g["d1"]), "0.7705")
    q("put delta", g["delta"], "-0.2295")
    q("phi(d1)", norm_pdf(g["d1"]), "0.30325")
    q("vanna", g["vanna"], "-1.0360")
    hv = 1e-5
    fd_vanna = (bs_greeks(S, K, T, 0.0, 0.0, s + hv, call=False)["delta"] - bs_greeks(S, K, T, 0.0, 0.0, s - hv, call=False)["delta"]) / (
        2 * hv
    )
    close("vanna vs finite difference of delta in vol", g["vanna"], fd_vanna, 1e-6)
    d_delta = g["vanna"] * -0.03
    q("vanna x dsigma", d_delta, "0.03108")
    q("put delta after (linear)", g["delta"] + d_delta, "-0.1984")
    q("short-put position delta (thousands)", -units * g["delta"] / 1e3, "2,294.6")
    q("put delta, five decimals", g["delta"], "-0.22946")
    q("vanna x dsigma, six decimals", d_delta, "0.031081")
    q("position delta change, linear (thousands)", -units * d_delta / 1e3, "-310.8")
    q("position delta change, linear (units)", -units * d_delta, "-310,808")
    q("linear buy-back flow ($bn)", units * d_delta * S / 1e9, "1.554")
    g17 = bs_greeks(S, K, T, 0.0, 0.0, 0.17, call=False)
    q("d1 at 17%", g17["d1"], "0.8620")
    q("put delta at 17%", g17["delta"], "-0.1944")
    q("full-revaluation delta change", g17["delta"] - g["delta"], "0.0351")
    q("full-revaluation units (thousands)", units * (g17["delta"] - g["delta"]) / 1e3, "351.1")
    q("full-revaluation flow ($bn)", units * (g17["delta"] - g["delta"]) * S / 1e9, "1.755")
    q("vanna at 17%", g17["vanna"], "-1.3162")


if __name__ == "__main__":
    example_1()
    example_2()
    print("all GEX and flow numbers verified")
