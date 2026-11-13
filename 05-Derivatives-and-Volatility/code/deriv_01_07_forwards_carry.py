"""Forwards, futures and cost of carry: every number in 01-Forwards-Futures-and-Carry.md.

Each quoted value is computed one way and, where the note calls it a check, confirmed by a second route:

1. Forward prices from the closed form and from an explicit replication (discrete dividend reinvestment
   compounded over a million steps, or the cash-flow schedule of the carry trade).
2. Cash-and-carry and reverse cash-and-carry in gold: the locked-in P&L is the same in every simulated terminal state.
3. Value of an existing forward: discounted spot minus strike, and an offsetting forward at today's price.
4. Implied dividend and implied repo by bisection on F(q) and F(r), not by the log formula.
5. Ho-Lee convexity adjustment from Gaussian moments of the integrated short rate, by quadrature.
6. Variation margin on E-mini S&P futures, day by day.
7. Covered interest parity by replicating a forward purchase of euros.

Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/deriv_01_07_forwards_carry.py
"""

from __future__ import annotations

import math

import numpy as np

SEED = 20261019


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes (half a unit in the last quoted digit)."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"{label:62s} {value:16.8f}  quoted {quoted}")
    assert abs(value - float(quoted)) <= tol, f"{label}: {value} does not round to {quoted}"
    return value


def close(label: str, a: float, b: float, tol: float) -> None:
    """Assert two independently computed values agree."""
    print(f"  check {label:56s} |diff| = {abs(a - b):.2e} (tol {tol:.0e})")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def forward_closed(S: float, r: float, T: float, q_: float = 0.0, u: float = 0.0, y: float = 0.0, pv_div: float = 0.0) -> float:
    """Cost-of-carry forward price with continuous rates."""
    return (S - pv_div) * math.exp((r - q_ + u - y) * T)


def forward_by_replication(S: float, r: float, carry_out: float, T: float, n: int = 1_000_000) -> float:
    """Buy x shares, reinvest the yield each step so x grows to one share at T, and finance at r compounded per step.

    carry_out is the yield the asset pays (dividend yield) minus any proportional cost of holding it (storage).
    As n grows this tends to S exp((r - carry_out) T) without using that formula.
    """
    dt = T / n
    x = 1.0 / (1.0 + carry_out * dt) ** n
    return x * S * (1.0 + r * dt) ** n


def bisect(f, lo: float, hi: float, tol: float = 1e-13) -> float:
    """Root of a monotone function by bisection; stops on bracket width, which is platform independent."""
    flo = f(lo)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def main() -> None:
    rng = np.random.default_rng(SEED)

    print("Example 1: forward on a dividend-paying stock (S = 100, r = 5%, T = 1)")
    f_yield = q("forward with 2% continuous yield", forward_closed(100, 0.05, 1.0, q_=0.02), "103.05")
    close("closed form vs replication with reinvested dividends", f_yield, forward_by_replication(100, 0.05, 0.02, 1.0), 1e-4)
    pv_d = q("PV of a 2 dividend paid at six months", 2 * math.exp(-0.05 * 0.5), "1.951")
    f_disc = q("forward with the discrete dividend", forward_closed(100, 0.05, 1.0, pv_div=pv_d), "103.08")
    # Cash-flow route: borrow 100 and buy the share; the dividend at 0.5 is invested to T; owe 100 e^{rT}.
    f_cash = 100 * math.exp(0.05) - 2 * math.exp(0.05 * 0.5)
    close("PV route vs future-value cash-flow route", f_disc, f_cash, 1e-12)
    q("financing cost of 100 over the year", 100 * (math.exp(0.05) - 1), "5.13")
    q("dividend worth today (narration)", pv_d, "1.95")
    q("e^0.05 (card deriv-forward-discrete-dividend)", math.exp(0.05), "1.05127")

    print("\nExample 2: gold cash-and-carry (spot 2000, r = 4%, storage 0.5%)")
    fair = q("fair one-year futures", forward_closed(2000, 0.04, 1.0, u=0.005), "2092.06")
    close("closed form vs replication with storage as negative yield", fair, forward_by_replication(2000, 0.04, -0.005, 1.0), 2e-3)
    s_T = 2000 * np.exp(rng.normal(0.0, 0.2, 100_000))  # any terminal prices: the locked-in P&L must not depend on them
    carry_pnl = (2120 - s_T) + s_T - 2000 * math.exp(0.045)  # short futures + gold delivered - loan and storage repaid
    q("cash-and-carry profit at 2120", float(carry_pnl.mean()), "27.94")
    assert float(np.ptp(carry_pnl)) < 1e-9, "cash-and-carry P&L should not depend on the terminal price"
    reverse_pnl = (s_T - 2050) - s_T + 2000 * math.exp(0.045)  # long futures - gold returned + proceeds and saved storage
    q("reverse cash-and-carry profit at 2050", float(reverse_pnl.mean()), "42.06")
    assert float(np.ptp(reverse_pnl)) < 1e-9

    print("\nExample 3: long forward struck at 100, six months left, spot 105, r = 4%")
    value = q("value of the existing forward", 105 - 100 * math.exp(-0.04 * 0.5), "6.98")
    offset = (forward_closed(105, 0.04, 0.5) - 100) * math.exp(-0.04 * 0.5)  # enter a short forward at today's F and discount
    close("discounted spot minus strike vs offsetting forward", value, offset, 1e-12)

    print("\nExample 4 and card deriv-implied-dividend-from-futures: implied dividend yield")
    q_impl = bisect(lambda x: forward_closed(5000, 0.05, 0.25, q_=x) - 5030, -0.5, 0.5)
    q("ln(5030/5000)/0.25", math.log(5030 / 5000) / 0.25, "0.02393")
    q("implied dividend yield, index 5000, futures 5030, r = 5%, 3m (%)", 100 * q_impl, "2.61")
    q("implied dividend yield as a decimal (code comment)", q_impl, "0.0261")
    q_card = bisect(lambda x: forward_closed(4000, 0.04, 0.5, q_=x) - 4030, -0.5, 0.5)
    q("ln(4030/4000)/0.5", math.log(4030 / 4000) / 0.5, "0.01494")
    q("implied dividend yield, index 4000, futures 4030, r = 4%, 6m (%)", 100 * q_card, "2.51")
    r_impl = bisect(lambda x: forward_closed(5000, x, 0.25, q_=0.02) - 5030, -0.5, 0.5)
    q("card deriv-implied-repo-rate: implied repo with q = 2% (%)", 100 * r_impl, "4.39")
    q("card deriv-implied-repo-rate: saving versus 5% funding (%)", 5 - 100 * r_impl, "0.61")
    s_T = 5000 * np.exp(rng.normal(0.0, 0.2, 100_000))  # any terminal index level: the locked-in P&L must not depend on it
    # Sell e^{-qT} basket units (dividends reinvested they would grow to one unit), invest at 5%, buy one futures at 5030.
    basis_pnl = 5000 * math.exp(-0.02 * 0.25) * math.exp(0.05 * 0.25) + (s_T - 5030) - s_T
    assert float(np.ptp(basis_pnl)) < 1e-9, "reverse basis P&L should not depend on the terminal index"
    q("card deriv-implied-repo-rate: three-month P&L in index points", float(basis_pnl.mean()), "7.6")
    q("card deriv-implied-repo-rate: three-month P&L as % of 5000", 100 * float(basis_pnl.mean()) / 5000, "0.15")
    close("basis P&L vs futures price grown at the funding gap", float(basis_pnl.mean()), 5030 * math.expm1((0.05 - r_impl) * 0.25), 1e-9)

    print("\nExample 5 and card deriv-convexity-adjustment-ho-lee: Ho-Lee convexity adjustment")
    for t1, t2, quoted in ((5.0, 5.25, "13.1"), (4.0, 4.25, "8.5")):
        sigma, f0 = 0.01, 0.04
        # Ho-Lee fitted to a flat curve f0: r(t) = f0 + sigma^2 t^2 / 2 + sigma W(t).
        # The continuously compounded rate set at t1 for [t1, t2] is R = -(1/tau) ln E_t1[exp(-int_t1^t2 r ds)].
        # Given r(t1) the integral is Gaussian; its mean and variance are computed by quadrature below.
        tau = t2 - t1
        s = np.linspace(t1, t2, 200_001)
        drift_part = 0.5 * sigma**2 * (s**2 - t1**2)
        mean_shift = float(np.sum(0.5 * (drift_part[1:] + drift_part[:-1]) * np.diff(s)))  # trapezoid
        var_part = (sigma * (s - t1)) ** 2  # Var of int sigma (W(s) - W(t1)) ds = int (sigma (t2 - s))^2 ds by symmetry
        var_int = float(np.sum(0.5 * (var_part[1:] + var_part[:-1]) * np.diff(s)))
        e_r_t1 = f0 + 0.5 * sigma**2 * t1**2  # E^Q[r(t1)]
        futures_rate = (e_r_t1 * tau + mean_shift - 0.5 * var_int) / tau  # E^Q[R], linear in r(t1)
        forward_rate = f0  # flat initial curve
        adj_bp = 1e4 * (futures_rate - forward_rate)
        q(f"futures minus forward rate, T1 = {t1:g}, T2 = {t2:g} (bp)", adj_bp, quoted)
        if quoted == "13.1":
            q("same adjustment as a decimal rate", adj_bp / 1e4, "0.00131")
        close("quadrature vs 0.5 sigma^2 T1 T2", adj_bp, 1e4 * 0.5 * sigma**2 * t1 * t2, 1e-6)

    print("\nExample 6: variation margin, long 10 E-mini S&P (multiplier 50) at 5000")
    settles = [5000.0, 5030.0, 4990.0]
    flows = [(b - a) * 50 * 10 for a, b in zip(settles[:-1], settles[1:], strict=True)]
    q("day 1 variation margin received", flows[0], "15000")
    q("day 2 variation margin paid", -flows[1], "20000")
    q("cumulative P&L", sum(flows), "-5000")
    close("sum of daily flows vs (4990 - 5000) x 500", sum(flows), (4990 - 5000) * 500, 1e-9)

    print("\nCards")
    q("deriv-cash-and-carry-arb: 100 e^0.05", 100 * math.exp(0.05), "105.13")
    q("deriv-cash-and-carry-arb: profit at 108", 108 - 100 * math.exp(0.05), "2.87")
    # Covered interest parity by replication: to own 1 EUR at T, buy e^{-r_EUR} EUR today with borrowed USD.
    usd_owed = 1.10 * math.exp(-0.03) * math.exp(0.05)
    q("deriv-covered-interest-parity: EURUSD one-year forward", usd_owed, "1.1222")
    close("replication vs S exp((r_USD - r_EUR) T)", usd_owed, forward_closed(1.10, 0.05, 1.0, q_=0.03), 1e-12)
    q("deriv-futures-tailing-number: tailed hedge of 1,000,000 units, 6m, r = 4%", 1_000_000 * math.exp(-0.04 * 0.5), "980199")
    print("\nAll forwards and carry checks passed.")


if __name__ == "__main__":
    main()
