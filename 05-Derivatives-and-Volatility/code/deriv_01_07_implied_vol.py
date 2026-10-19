"""Implied volatility and the smile: every number in 07-Implied-Volatility-and-the-Smile.md.

1. A safeguarded Newton solver: Newton steps from the Manaster-Koehler start, kept inside a bisection bracket that shrinks
   on every evaluation. It stops when the price residual is below 1e-10 (about 1e5 times the double-precision noise of a
   price near 10) or the bracket is narrower than 1e-12, so the converged vol does not depend on platform rounding.
   Each result is confirmed by pricing_core.implied_vol, an 80-step bisection that shares no code with the solver.
2. The plain-Newton iterates the note quotes, at the precision it quotes them.
3. Smile-adjusted deltas: closed-form vega adjustment against a finite difference of the price under each smile rule.
4. A digital from the skew: vega correction against a tight call spread on the smile.
5. FX wing vols, forward variance and the calendar check.

Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/deriv_01_07_implied_vol.py
"""

from __future__ import annotations

import math

from pricing_core import bs_price, bs_vega, implied_vol, norm_cdf

PRICE_TOL = 1e-10
BRACKET_TOL = 1e-12


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"{label:66s} {value:14.8f}  quoted {quoted}")
    assert abs(value - float(quoted)) <= tol, f"{label}: {value} does not round to {quoted}"
    return value


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"  check {label:60s} |diff| = {abs(a - b):.2e} (tol {tol:.0e})")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def solve_iv(price: float, S: float, K: float, T: float, r: float, q_: float = 0.0, call: bool = True) -> float:
    """Safeguarded Newton for Black-Scholes implied vol (call or put)."""
    F, df = S * math.exp((r - q_) * T), math.exp(-r * T)
    lower = df * max(F - K, 0.0) if call else df * max(K - F, 0.0)
    upper = df * F if call else df * K
    if not lower < price < upper:
        raise ValueError(f"price {price} outside the no-arbitrage bounds ({lower}, {upper})")
    lo, hi = 1e-8, 10.0
    sigma = math.sqrt(2 * abs(math.log(F / K)) / T) or 0.2  # Manaster-Koehler start: the inflection point of C(sigma)
    sigma = min(max(sigma, lo), hi)
    for _ in range(200):
        diff = bs_price(S, K, T, r, sigma, q_, call) - price
        if abs(diff) < PRICE_TOL:  # residual check first, before any bracket logic
            return sigma
        if diff > 0:
            hi = sigma
        else:
            lo = sigma
        if hi - lo < BRACKET_TOL:
            return 0.5 * (lo + hi)
        vega = bs_vega(S, K, T, r, sigma, q_)
        step = sigma - diff / vega if vega > 0 else -1.0
        sigma = step if lo < step < hi else 0.5 * (lo + hi)
    raise RuntimeError("implied vol did not converge")


def newton_path(price: float, S: float, K: float, T: float, r: float, sigma0: float, n: int) -> list[float]:
    """Unsafeguarded Newton iterates, to show the overshoot."""
    path, sigma = [], sigma0
    for _ in range(n):
        sigma = sigma - (bs_price(S, K, T, r, sigma) - price) / bs_vega(S, K, T, r, sigma)
        path.append(sigma)
    return path


def main() -> None:
    print("Example 1: S = K = 100, T = 0.5, r = 3%, call 7.00")
    s0 = q("Brenner-Subrahmanyam guess sqrt(2 pi / T) C / S (%)", 100 * math.sqrt(2 * math.pi / 0.5) * 7 / 100, "24.81") / 100
    q("price at the guess", bs_price(100, 100, 0.5, 0.03, s0), "7.7087")
    q("vega at the guess", bs_vega(100, 100, 0.5, 0.03, s0), "27.79")
    path = newton_path(7.0, 100, 100, 0.5, 0.03, s0, 2)
    q("first Newton step (%)", 100 * path[0], "22.264")
    q("price after one step", bs_price(100, 100, 0.5, 0.03, path[0]), "7.00003")
    iv1 = q("safeguarded solver (%)", 100 * solve_iv(7.0, 100, 100, 0.5, 0.03), "22.2641") / 100
    q("guess as a decimal", s0, "0.2481")
    q("price error at the guess", bs_price(100, 100, 0.5, 0.03, s0) - 7.0, "0.7087")
    q("solution as a decimal", iv1, "0.2226")
    q("how far the guess was high (vol points)", 100 * (s0 - iv1), "2.55")
    q("1/sqrt(2 pi)", 1 / math.sqrt(2 * math.pi), "0.3989")
    close("solver vs pricing_core bisection", iv1, implied_vol(7.0, 100, 100, 0.5, 0.03), 1e-8)
    q("forward intrinsic S - K e^{-rT}", 100 - 100 * math.exp(-0.03 * 0.5), "1.49")
    tv = q("time-value proxy 0.3989 x sigma x 100 x sqrt(0.5)", 100 * iv1 * math.sqrt(0.5) / math.sqrt(2 * math.pi), "6.28")
    q("carry part of the premium, 7 - 6.28", 7 - tv, "0.72")

    print("\nExample 2: S = 100, K = 150, T = 0.25, r = 0, call 0.01")
    iv2 = q("true implied vol (%)", 100 * solve_iv(0.01, 100, 150, 0.25, 0.0), "28.16") / 100
    close("solver vs pricing_core bisection", iv2, implied_vol(0.01, 100, 150, 0.25, 0.0), 1e-8)
    q("price at 20% (x 1e5)", 1e5 * bs_price(100, 150, 0.25, 0.0, 0.2), "6.9")
    q("vega at 20%", bs_vega(100, 150, 0.25, 0.0, 0.2), "0.0066")
    plain = newton_path(0.01, 100, 150, 0.25, 0.0, 0.2, 3)
    q("plain Newton from 20%: step 1 (%)", 100 * plain[0], "171")
    q("price at step 1", bs_price(100, 150, 0.25, 0.0, plain[0]), "20.64")
    q("step 2 (%)", 100 * plain[1], "68")
    q("step 3 (%)", 100 * plain[2], "48")
    mk0 = q("Manaster-Koehler start sqrt(2 ln 1.5 / 0.25) (%)", 100 * math.sqrt(2 * math.log(1.5) / 0.25), "180") / 100
    mk = newton_path(0.01, 100, 150, 0.25, 0.0, mk0, 7)
    for k, (v, qt) in enumerate(zip(mk, ("68", "48", "39", "33", "30.2", "28.6", "28.19"), strict=True), start=1):
        q(f"Newton from the inflection point, step {k} (%)", 100 * v, qt)
    assert all(a > b for a, b in zip(mk, mk[1:], strict=False)) and mk[-1] > iv2
    print("  check the iterates from the inflection point decrease monotonically toward the root")
    try:
        solve_iv(0.0, 100, 150, 0.25, 0.0)
        raise AssertionError("a zero price must be rejected")
    except ValueError:
        print("  check a price on the no-arbitrage bound is rejected")

    print("\nCards: quick inversion and parity")
    q("deriv-iv-quick-atm-inversion: 4 / (0.4 x 100 x 0.5) (%)", 100 * 4 / (0.4 * 100 * 0.5), "20")
    q("deriv-iv-quick-atm-inversion: exact (%)", 100 * solve_iv(4.0, 100, 100, 0.25, 0.0), "20.06")
    c = bs_price(100, 100, 1.0, 0.05, 0.25, q=0.02)
    p = bs_price(100, 100, 1.0, 0.05, 0.25, q=0.02, call=False)
    iv_c, iv_p = solve_iv(c, 100, 100, 1.0, 0.05, 0.02), solve_iv(p, 100, 100, 1.0, 0.05, 0.02, False)
    close("call and put implied vols with the right forward", iv_c, iv_p, 1e-9)
    q("deriv-iv-wrong-forward-split: call vol ignoring a 2% yield (%)", 100 * solve_iv(c, 100, 100, 1.0, 0.05), "21.8")
    q("deriv-iv-wrong-forward-split: put vol ignoring a 2% yield (%)", 100 * solve_iv(p, 100, 100, 1.0, 0.05, call=False), "27.0")
    split = solve_iv(p, 100, 100, 1.0, 0.05, call=False) - solve_iv(c, 100, 100, 1.0, 0.05)
    q("put minus call vol from the wrong forward (vol points)", 100 * split, "5.2")

    print("\nExample 3: smile-adjusted delta, 90 put, S = 100, T = 0.25, 25% vol, beta = -0.004")
    S, K, T, sig, beta = 100.0, 90.0, 0.25, 0.25, -0.004
    put = q("put", bs_price(S, K, T, 0.0, sig, call=False), "1.319")
    d_bs = q("Black-Scholes delta", -norm_cdf(-(math.log(S / K) / (sig * math.sqrt(T)) + 0.5 * sig * math.sqrt(T))), "-0.183")
    vega = q("vega per unit vol", bs_vega(S, K, T, 0.0, sig), "13.24")
    q("vega per vol point", vega / 100, "0.132")
    q("sticky moneyness d sigma / dS = -(K/S) beta", -(K / S) * beta, "0.0036")
    d_sm = q("sticky-moneyness delta", d_bs + vega * (-(K / S) * beta), "-0.135")
    d_lv = q("local-vol delta", d_bs + vega * beta, "-0.236")
    q("spread between regimes", d_sm - d_lv, "0.10")
    q("size of the Black-Scholes delta", -d_bs, "0.18")
    q("hedge disagreement on 1,000 contracts x multiplier 100 (shares)", (d_sm - d_lv) * 1_000 * 100, "10062")
    rules = {
        "sticky strike": lambda k, s: sig + beta * (k - K),
        "sticky moneyness": lambda k, s: sig + beta * S * (k / s - K / S),
        "local vol": lambda k, s: sig + beta * (k - K) + beta * (s - S),
    }
    h = 1e-3
    for name, expected in (("sticky strike", d_bs), ("sticky moneyness", d_sm), ("local vol", d_lv)):
        rule = rules[name]
        fd = (bs_price(S + h, K, T, 0.0, rule(K, S + h), call=False) - bs_price(S - h, K, T, 0.0, rule(K, S - h), call=False)) / (2 * h)
        close(f"{name}: vega-adjusted delta vs finite difference on the smile rule", expected, fd, 2e-3)
    assert abs(put - bs_price(S, K, T, 0.0, rules["local vol"](K, S), call=False)) < 1e-12

    print("\nExample 4 and card deriv-iv-digital-skew-term: digital off the skew (1y, S = F = 100, r = 0, ATM 20%, skew -0.002)")
    nd2 = q("N(d2) = N(-0.1)", norm_cdf(-0.1), "0.4602")
    v = q("vega", bs_vega(100, 100, 1.0, 0.0, 0.2), "39.70")
    dig = q("digital = N(d2) - vega x skew", nd2 - v * (-0.002), "0.5396")
    q("skew correction", v * 0.002, "0.0794")
    q("digital, three decimals (card)", dig, "0.540")

    def smile(k: float) -> float:
        return 0.2 - 0.002 * (k - 100)

    hh = 0.01
    spread = (bs_price(100, 100 - hh, 1.0, 0.0, smile(100 - hh)) - bs_price(100, 100 + hh, 1.0, 0.0, smile(100 + hh))) / (2 * hh)
    q("call spread on the smile", spread, "0.53956")
    close("vega formula vs call spread", dig, spread, 1e-6)

    print("\nExample 5 and card deriv-iv-fx-wing-vols: ATM 10%, RR -1.5, BF 0.40")
    q("25-delta call vol", 10.0 + 0.40 - 1.5 / 2, "9.65")
    q("25-delta put vol", 10.0 + 0.40 + 1.5 / 2, "11.15")

    print("\nExample 6 and card deriv-iv-calendar-arbitrage: forward variance")
    fv = q("forward variance 1m to 3m, 30% then 25%", (0.25**2 * 0.25 - 0.30**2 / 12) / (0.25 - 1 / 12), "0.04875")
    q("forward vol (%)", 100 * math.sqrt(fv), "22.08")
    q("forward vol as a decimal (card)", math.sqrt(fv), "0.2208")
    q("forward variance with 45% one-month vol", (0.25**2 * 0.25 - 0.45**2 / 12) / (0.25 - 1 / 12), "-0.0075")
    print("\nAll implied volatility checks passed.")


if __name__ == "__main__":
    main()
