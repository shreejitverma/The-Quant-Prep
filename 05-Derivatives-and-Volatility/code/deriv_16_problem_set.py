"""Options problem set: every number in 16-Options-Problem-Set.md.

Independent routes used here:
- arbitrage trades by exact rational arithmetic (fractions.Fraction) on the cash flows and by evaluating the
  payoff on a fine grid of terminal prices, never by restating the convexity inequality;
- Black-Scholes prices from ``pricing_core`` re-derived by Gauss-Legendre quadrature of the payoff;
- Greeks from closed forms cross-checked by central finite differences of the price, and every scenario P&L by
  full revaluation against its Taylor estimate;
- the gamma peak by a grid search over spot, not the d1 = -sigma sqrt(T) condition;
- the discrete-hedging noise rule of Kamal (1998, Goldman Sachs Quantitative Strategies) against a seeded
  simulation of the hedged short call (seed SEED_HEDGE, 20,000 paths).
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/deriv_16_problem_set.py
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
from pricing_core import bs_price, norm_cdf, norm_pdf

SEED_HEDGE = 1
_X, _W = np.polynomial.legendre.leggauss(200)


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"    {label} = {value:.8f}  (quoted {quoted})")
    assert abs(value - float(quoted.replace(",", ""))) <= tol, f"{label}: {value} does not round to {quoted}"
    return value


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: {value} != {expected}"
    print(f"    {label} = {value}")


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"      check {label}: |{a:.8g} - {b:.8g}| = {abs(a - b):.1e} <= {tol:.0e}")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def quad_price(S: float, K: float, T: float, r: float, sig: float, call: bool = True) -> float:
    """European price by quadrature over the normal driver, split at the strike."""
    sd = sig * math.sqrt(T)
    zk = (math.log(K / S) - (r - 0.5 * sig * sig) * T) / sd
    total = 0.0
    for lo, hi in ((-12.0, zk), (zk, 12.0)):
        z = 0.5 * (hi - lo) * _X + 0.5 * (hi + lo)
        st = S * np.exp((r - 0.5 * sig * sig) * T + sd * z)
        pay = np.maximum(st - K, 0.0) if call else np.maximum(K - st, 0.0)
        total += 0.5 * (hi - lo) * float(np.sum(_W * pay * np.exp(-0.5 * z * z))) / math.sqrt(2 * math.pi)
    return math.exp(-r * T) * total


def straddle(S: float, T: float, sig: float, K: float = 100.0) -> float:
    return float(bs_price(S, K, T, 0.0, sig) + bs_price(S, K, T, 0.0, sig, call=False))


def straddle_greeks(T: float, sig: float) -> dict[str, float]:
    """ATM straddle (S = K = 100, r = 0): gamma, vega and vanna per vol point, theta per calendar day."""
    sd = sig * math.sqrt(T)
    d1 = 0.5 * sd
    return {
        "delta": 2 * norm_cdf(d1) - 1,
        "gamma": 2 * norm_pdf(d1) / (100 * sd),
        "vega": 2 * 100 * norm_pdf(d1) * math.sqrt(T) / 100,
        "theta": -2 * 100 * norm_pdf(d1) * sig / (2 * math.sqrt(T)) / 365,
        "vanna": 2 * (-norm_pdf(d1) * (d1 - sd) / sig) / 100,
    }


def hedged_short_call(n: int, paths: int = 20_000, sigma: float = 0.2, seed: int = SEED_HEDGE) -> np.ndarray:
    """Sell a one-year ATM call at sigma, delta-hedge n times at sigma, realized vol = sigma, r = 0."""
    rng = np.random.default_rng(seed)
    dt = 1.0 / n

    def delta(s: np.ndarray, tau: float) -> np.ndarray:
        sd = sigma * math.sqrt(tau)
        return np.asarray(norm_cdf(np.log(s / 100.0) / sd + 0.5 * sd))

    S = np.full(paths, 100.0)
    pos = delta(S, 1.0)
    cash = bs_price(100.0, 100.0, 1.0, 0.0, sigma) - pos * S
    for i in range(1, n + 1):
        S = S * np.exp(-0.5 * sigma**2 * dt + sigma * math.sqrt(dt) * rng.standard_normal(paths))
        if i < n:
            new = delta(S, 1.0 - i * dt)
            cash -= (new - pos) * S
            pos = new
    return cash + pos * S - np.maximum(S - 100.0, 0.0)


def main() -> None:
    print("Example 1 and card deriv-ps-unequal-fly-arbitrage: calls 90 / 95 / 110 at 13.00 / 10.50 / 2.00")
    c90, c95, c110 = Fraction(13), Fraction(21, 2), Fraction(2)
    exact("call spread 90/95", c90 - c95, Fraction(5, 2))
    exact("call spread 95/110", c95 - c110, Fraction(17, 2))
    lam = Fraction(110 - 95, 110 - 90)
    exact("lambda", lam, Fraction(3, 4))
    exact("0.75 C(90) + 0.25 C(110)", lam * c90 + (1 - lam) * c110, Fraction(41, 4))
    exact("0.75 x 13", lam * c90, Fraction(39, 4))
    exact("violation", c95 - (lam * c90 + (1 - lam) * c110), Fraction(1, 4))
    weights = {90: 3, 95: -4, 110: 1}
    exact("weights 15 : 20 : 5 divided by 5", (15 // 5, 20 // 5, 5 // 5), (3, 4, 1))
    cash = -sum(w * c for w, c in zip(weights.values(), (c90, c95, c110), strict=True))
    exact("cash received today", cash, Fraction(1))
    grid = np.linspace(0, 200, 400_001)
    payoff = sum(w * np.maximum(grid - k, 0.0) for k, w in weights.items())
    assert payoff.min() >= -1e-9, payoff.min()
    exact("payoff at 95", float(payoff[grid == 95.0][0]), 15.0)
    q("payoff at 110 and above (max)", float(np.abs(payoff[grid >= 110]).max()), "0.000")
    print("    payoff is non-negative on 0-200 (step 0.0005)")

    print("Example 2: parity with dividends and the implied rate")
    q("K e^{-rT} = 50 e^{-0.02}", 50 * math.exp(-0.02), "49.010")
    q("PV(D) = 50 - 49.010 - 0.10", 50 - 50 * math.exp(-0.02) - 0.10, "0.89")
    r_impl = q("implied rate (%)", -100 * math.log(0.95), "5.13")
    close("parity re-check: 100 - 100 e^{-r} = 5", 100 - 100 * math.exp(-r_impl / 100), 5.0, 1e-9)

    print("Example 3 and card deriv-ps-mental-atm-spot-rates: mental pricing with carry")
    fwd_itm = q("S - K e^{-rT}", 100 - 100 * math.exp(-0.05), "4.88")
    q("K e^{-rT}", 100 * math.exp(-0.05), "95.12")
    q("half the forward intrinsic", fwd_itm / 2, "2.44")
    q("0.4 sigma S sqrt T", 0.4 * 0.2 * 100, "8.00")
    q("mental total", 8.0 + fwd_itm / 2, "10.44")
    bs = q("Black-Scholes", bs_price(100, 100, 1.0, 0.05, 0.2), "10.45")
    close("Black-Scholes by quadrature", quad_price(100, 100, 1.0, 0.05, 0.2), bs, 1e-9)
    q("one-week straddle shortcut 0.8 x 0.32 x 200 / sqrt(52)", 0.8 * 0.32 * 200 / math.sqrt(52), "7.10")
    wk = q("one-week straddle exact", straddle(200, 1 / 52, 0.32, 200), "7.08")
    close("weekly straddle by quadrature", quad_price(200, 200, 1 / 52, 0, 0.32) + quad_price(200, 200, 1 / 52, 0, 0.32, False), wk, 1e-9)
    q("expected absolute move priced (%)", 100 * wk / 200, "3.5")

    print("Example 4: a day's P&L on a hedged 30-day 100 straddle at 25%, spot to 97, vol +2")
    T1 = 30 / 365
    g = straddle_greeks(T1, 0.25)
    h = 0.01
    close(
        "gamma by finite differences",
        (straddle(100 + h, T1, 0.25) - 2 * straddle(100, T1, 0.25) + straddle(100 - h, T1, 0.25)) / h**2,
        g["gamma"],
        1e-5,
    )
    close("vega by finite differences", (straddle(100, T1, 0.2501) - straddle(100, T1, 0.2499)) / 0.0002 / 100, g["vega"], 1e-8)
    close("theta by finite differences", straddle(100, T1 - 0.5 / 365, 0.25) - straddle(100, T1 + 0.5 / 365, 0.25), g["theta"], 1e-5)
    dd = lambda v: (straddle(100 + h, T1, v) - straddle(100 - h, T1, v)) / (2 * h)  # noqa: E731
    close("vanna by finite differences", (dd(0.2501) - dd(0.2499)) / 0.0002 / 100, g["vanna"], 1e-7)
    q("gamma", g["gamma"], "0.111")
    q("vega per point", g["vega"], "0.229")
    q("theta per day", g["theta"], "-0.095")
    q("vanna per point", g["vanna"], "0.0011")
    gam_pnl = q("gamma P&L 0.5 x 0.111 x 9", 0.5 * g["gamma"] * 9, "0.501")
    vega_pnl = q("vega P&L 0.229 x 2", g["vega"] * 2, "0.457")
    vanna_pnl = q("vanna P&L 0.0011 x (-3) x 2", g["vanna"] * -3 * 2, "-0.007")
    taylor = q("Taylor total", gam_pnl + vega_pnl + g["theta"] + vanna_pnl, "0.856")
    q("Taylor total, four decimals", taylor, "0.8557")
    full = straddle(97, T1 - 1 / 365, 0.27) - straddle(100, T1, 0.25) - g["delta"] * (-3)
    q("full revaluation", full, "0.820")
    q("full revaluation, four decimals", full, "0.8205")
    q("gap", taylor - full, "0.035")
    q("zomma estimate -0.5 x 9 x (0.111 / 0.25) x 0.02", -0.5 * 9 * g["gamma"] / 0.25 * 0.02, "-0.040")
    gamma_at = lambda v: straddle_greeks(T1, v)["gamma"]  # noqa: E731
    q("exact gamma change term 0.5 x 9 x (Gamma(27%) - Gamma(25%))", 0.5 * 9 * (gamma_at(0.27) - gamma_at(0.25)), "-0.037")

    print("Example 5 and card deriv-ps-short-straddle-gap: short the straddle through an 8% gap")
    q("Taylor loss 0.5 x 0.111 x 64 - 0.095", 0.5 * g["gamma"] * 64 + g["theta"], "3.46")
    q("Taylor loss with the rounded Greeks", 0.5 * 0.111 * 64 - 0.095, "3.46")
    p108 = q("straddle at 108, one day later", straddle(108, T1 - 1 / 365, 0.25), "9.020")
    q("straddle today", straddle(100, T1, 0.25), "5.717")
    q("delta", g["delta"], "0.029")
    q("full-revaluation loss", p108 - straddle(100, T1, 0.25) - g["delta"] * 8, "3.07")
    sd108 = 0.25 * math.sqrt(T1 - 1 / 365)
    gam108 = q("gamma at 108", 2 * norm_pdf(math.log(1.08) / sd108 + 0.5 * sd108) / (108 * sd108), "0.056")
    q("gamma at 108 relative to ATM", gam108 / g["gamma"], "0.50")

    print(f"Example 6 and card deriv-ps-discrete-hedge-noise: one-year ATM call at 20%, seed {SEED_HEDGE}")
    prem = q("premium", bs_price(100, 100, 1.0, 0.0, 0.2), "7.97")
    vega = q("vega per unit vol", 100 * norm_pdf(0.1), "39.7")
    q("sqrt(pi / 4)", math.sqrt(math.pi / 4), "0.886")
    rule = {n: math.sqrt(math.pi / 4) * vega * 0.2 / math.sqrt(n) for n in (52, 252)}
    q("rule, daily (N = 252)", rule[252], "0.44")
    q("rule, daily, three decimals", rule[252], "0.443")
    q("rule, weekly (N = 52)", rule[52], "0.98")
    q("noise as a share of premium, daily (%)", 100 * rule[252] / prem, "5.6")
    for n, quoted in ((252, "0.44"), (52, "0.96")):
        pnl = hedged_short_call(n)
        sd = float(pnl.std(ddof=1))
        q(f"simulated sd, N = {n}", sd, quoted)
        assert abs(float(pnl.mean())) < 4 * sd / math.sqrt(len(pnl)), "hedged P&L mean is not zero"
        close(f"simulated sd within 5% of the rule, N = {n}", sd, rule[n], 0.05 * rule[n])

    print("Cards: parity and arbitrage")
    q("deriv-ps-longer-put-cheaper: one-year put", bs_price(20, 100, 1.0, 0.05, 0.2, call=False), "75.12")
    q("deriv-ps-longer-put-cheaper: two-year put", bs_price(20, 100, 2.0, 0.05, 0.2, call=False), "70.48")
    close("two-year put by quadrature", quad_price(20, 100, 2.0, 0.05, 0.2, False), bs_price(20, 100, 2.0, 0.05, 0.2, call=False), 1e-8)
    exact("deriv-ps-american-put-below-intrinsic: cost 8 + 90, receive 100", 100 - (8 + 90), 2)
    exact("deriv-ps-put-spread-above-width: width", 110 - 100, 10)

    print("Cards: Greeks")
    spots = np.linspace(80, 110, 300_001)
    sd = 0.2
    gam = norm_pdf(np.log(spots / 100) / sd + 0.5 * sd) / (spots * sd)
    peak = float(spots[np.argmax(gam)])
    q("deriv-ps-gamma-peak-spot: argmax of gamma by grid search", peak, "94.2")
    close("peak against K exp(-1.5 sigma^2 T)", peak, 100 * math.exp(-1.5 * 0.04), 2e-4)
    q("deriv-ps-atm-vega-tenor-ratio: vega(1y) / vega(3m) at 20%", norm_pdf(0.1) / (0.5 * norm_pdf(0.05)), "1.99")
    q("deriv-ps-straddle-direction: 30-day straddle delta", g["delta"], "0.03")

    print("Cards: mental pricing")
    c40 = q("deriv-ps-mental-atm-40-vol: exact", bs_price(50, 50, 1.0, 0.0, 0.4), "7.93")
    close("quadrature", quad_price(50, 50, 1.0, 0.0, 0.4), c40, 1e-9)
    q("deriv-ps-mental-atm-40-vol: 0.4 x 0.40 x 50", 0.4 * 0.4 * 50, "8.0")
    q("deriv-ps-mental-atm-digital: N(-0.1)", norm_cdf(-0.1), "0.46")
    q("deriv-ps-mental-atm-digital: 0.5 - 0.4 x 0.1", 0.5 - 0.4 * 0.1, "0.46")
    dig = (bs_price(100, 99.995, 1.0, 0.0, 0.2) - bs_price(100, 100.005, 1.0, 0.0, 0.2)) / 0.01
    close("digital as a tight call spread", dig, norm_cdf(-0.1), 1e-6)
    q("deriv-ps-mental-atm-vega: per point", norm_pdf(0.1), "0.397")
    q("deriv-ps-mental-atm-gamma", norm_pdf(0.1) / 20, "0.0198")
    q("deriv-ps-mental-atm-theta: exact per year", -100 * norm_pdf(0.1) * 0.2 / 2, "-3.97")
    q("deriv-ps-mental-atm-theta: -4 / 365", -4 / 365, "-0.011")
    q("deriv-ps-mental-atm-theta: -4 / 252", -4 / 252, "-0.016")
    q("deriv-ps-mental-atm-theta: -0.5 x 0.04 x 10^4 x 0.02", -0.5 * 0.04 * 1e4 * 0.02, "-4")
    q("deriv-ps-mental-vol-bump: 0.40 x 2", 0.40 * 2, "0.80")
    q("deriv-ps-mental-vol-bump: 8 + 0.8", 8 + 0.8, "8.8")
    q("deriv-ps-mental-vol-bump: exact change", bs_price(100, 100, 1.0, 0.0, 0.22) - bs_price(100, 100, 1.0, 0.0, 0.2), "0.79")

    print("Cards: hedged P&L")
    q("deriv-ps-gamma-theta-day", 0.5 * 5000 * 2**2 - 6000, "4000")
    q("deriv-ps-book-breakeven-move: x", math.sqrt(2 * 5000 / 10_000), "1")
    q("deriv-ps-book-breakeven-move: annual vol for a 2% daily sd (%)", 2 * math.sqrt(252), "32")
    q("deriv-ps-sold-vol-pnl: straddle at 25% minus at 20%", straddle(100, T1, 0.25) - straddle(100, T1, 0.20), "1.14")
    q("deriv-ps-sold-vol-pnl: 0.229 x 5", g["vega"] * 5, "1.14")
    q("deriv-ps-vanna-pnl", 2000 * -3 * 2, "-12000")

    print("Cards: strategies")
    exact("deriv-ps-butterfly-profile: max profit", Fraction(5) - Fraction(6, 5), Fraction(19, 5))
    exact("deriv-ps-butterfly-profile: break-evens", (95 + Fraction(6, 5), 105 - Fraction(6, 5)), (Fraction(481, 5), Fraction(519, 5)))
    st = np.linspace(80, 120, 40_001)
    fly = np.maximum(st - 95, 0) - 2 * np.maximum(st - 100, 0) + np.maximum(st - 105, 0) - 1.2
    assert abs(fly.max() - 3.8) < 1e-9 and abs(fly.min() + 1.2) < 1e-9
    exact("deriv-ps-call-spread-as-digital: 50 x (101 - 99)", 50 * (101 - 99), 100)
    exact("deriv-ps-call-spread-as-digital: 50 x (100 - 98)", 50 * (100 - 98), 100)
    ratio = np.maximum(st - 100, 0) - 2 * np.maximum(st - 110, 0)
    exact("deriv-ps-ratio-spread-risk: payoff at 110 (before credit)", float(ratio[st == 110.0][0]), 10.0)
    exact("deriv-ps-ratio-spread-risk: payoff at 120 (before credit)", float(ratio[st == 120.0][0]), 0.0)

    print("Cards: vol surface")
    q("deriv-ps-atm-vol-after-drop: sticky strike, 0.3 x 5", 0.3 * 5, "1.5")
    q("deriv-ps-atm-vol-after-drop: local vol, 2 x 0.3 x 5", 2 * 0.3 * 5, "3")
    q("deriv-ps-local-vs-implied-skew: 2 x -0.2", 2 * -0.2, "-0.4")
    print("All problem set checks passed.")


if __name__ == "__main__":
    main()
