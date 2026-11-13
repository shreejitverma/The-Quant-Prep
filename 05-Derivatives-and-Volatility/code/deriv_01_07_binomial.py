"""Binomial trees: every number in 03-Binomial-Trees.md.

1. One- and two-step examples in exact rational arithmetic (fractions), with the replicating portfolio checked in every state.
2. CRR convergence table by backward induction, confirmed by the closed-form binomial sum (log-gamma coefficients)
   and compared with Black-Scholes from pricing_core.
3. American put on CRR trees and its early-exercise premium.
4. Delta, gamma and theta read off the first two steps of the tree, against Black-Scholes closed forms.

Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/deriv_01_07_binomial.py
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
from pricing_core import bs_price, norm_cdf, norm_pdf

S0, K, T, R, SIG = 100.0, 100.0, 1.0, 0.05, 0.20


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"{label:62s} {float(value):14.8f}  quoted {quoted}")
    assert abs(float(value) - float(quoted)) <= tol, f"{label}: {float(value)} does not round to {quoted}"
    return float(value)


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"  check {label:56s} |diff| = {abs(a - b):.2e} (tol {tol:.0e})")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def crr_tree(S: float, K: float, T: float, r: float, sigma: float, n: int, call: bool = True, american: bool = False):
    """CRR backward induction; returns the root value and the first three time slices for tree Greeks."""
    dt = T / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    disc = math.exp(-r * dt)

    def payoff(s: np.ndarray) -> np.ndarray:
        return np.maximum(s - K, 0.0) if call else np.maximum(K - s, 0.0)

    v = payoff(S * u ** (n - 2.0 * np.arange(n + 1)))
    slices = {}
    for i in range(n - 1, -1, -1):
        v = disc * (p * v[:-1] + (1 - p) * v[1:])
        if american:
            v = np.maximum(v, payoff(S * u ** (i - 2.0 * np.arange(i + 1))))
        if i <= 2:
            slices[i] = v.copy()
    return float(v[0]), slices, u, dt


def crr_binomial_sum(S: float, K: float, T: float, r: float, sigma: float, n: int) -> float:
    """European call as the discounted binomial expectation, sum_j C(n, j) p^(n-j) (1-p)^j payoff (no backward induction)."""
    dt = T / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    total = 0.0
    for j in range(n + 1):
        s_t = S * u ** (n - 2 * j)
        if s_t <= K:
            continue
        log_w = math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) + (n - j) * math.log(p) + j * math.log(1 - p)
        total += math.exp(log_w) * (s_t - K)
    return math.exp(-r * T) * total


def main() -> None:
    print("Example 1: one step, S = 100, u = 1.2, d = 0.8, K = 100 call (exact fractions)")
    u, d = Fraction(6, 5), Fraction(4, 5)
    for gross, quoted_p, quoted_v in ((Fraction(1), "0.5", "10"), (Fraction(105, 100), "0.625", "11.90")):
        delta = Fraction(20 - 0) / (120 - 80)
        bond = (u * 0 - d * 20) / ((u - d) * gross)  # B = (u V_d - d V_u) / ((u - d) R)
        price = delta * 100 + bond
        p = (gross - d) / (u - d)
        assert delta * 120 + bond * gross == 20 and delta * 80 + bond * gross == 0  # replicates both states exactly
        assert price == (p * 20 + (1 - p) * 0) / gross  # replication cost equals risk-neutral expectation
        q(f"  R = {float(gross):g}: risk-neutral p", p, quoted_p)
        q(f"  R = {float(gross):g}: price", price, quoted_v)
        q(f"  R = {float(gross):g}: delta", delta, "0.5")
    q("  bond at R = 1 (borrow 40)", (u * 0 - d * 20) / (u - d), "-40")
    q("  PV of the 40 borrowed at R = 1.05", Fraction(40) / Fraction(105, 100), "38.10")

    print("\nExample 2: two-step American put, u = 1.1, d = 1/1.1, R = 1.02 (exact fractions)")
    u, gross = Fraction(11, 10), Fraction(102, 100)
    d = 1 / u
    p = (gross - d) / (u - d)
    q("risk-neutral p", p, "0.5810")
    q("1 - p", 1 - p, "0.4190")
    q("p (card, three decimals)", p, "0.581")
    q("1 - p (card, three decimals)", 1 - p, "0.419")
    q("d = 1/1.1", d, "0.9091")
    q("up-up stock", 100 * u * u, "121")
    q("up stock (table)", 100 * u, "110.00")
    q("middle step-2 stock (table)", 100 * u * d, "100.00")
    pay_dd = 100 - 100 * d * d
    q("terminal down-down put payoff", pay_dd, "17.36")
    q("terminal down-down stock", 100 * d * d, "82.64")
    cont_down = (1 - p) * pay_dd / gross
    q("down node continuation", cont_down, "7.13")
    ex_down = 100 - 100 * d
    q("down node exercise", ex_down, "9.09")
    q("down node stock", 100 * d, "90.91")
    am = (1 - p) * max(cont_down, ex_down) / gross
    eu = (1 - p) * cont_down / gross
    q("American put", am, "3.73")
    q("European put", eu, "2.93")
    q("American (more digits)", am, "3.735")
    q("European (more digits)", eu, "2.929")
    q("early-exercise premium", am - eu, "0.806")
    hedge = (0 - cont_down) / (110 - 100 * d)
    bond = eu - hedge * 100
    q("root hedge delta for the European put", hedge, "-0.373")
    q("bond lent", bond, "40.28")
    assert hedge * 110 + bond * gross == 0 and hedge * 100 * d + bond * gross == cont_down
    print("  check the root hedge replicates the European put in both step-1 states exactly")

    print("\nExample 3: CRR convergence, S = K = 100, T = 1, r = 5%, 20% vol")
    c_bs = q("Black-Scholes call", bs_price(S0, K, T, R, SIG), "10.4506")
    q("Black-Scholes call, two decimals (card)", c_bs, "10.45")
    table = {1: ("12.1623", "1.7117"), 2: ("9.5405", "-0.9101"), 5: ("10.8059", "0.3554"), 10: ("10.2534", "-0.1972")}
    table |= {50: ("10.4107", "-0.0399"), 51: ("10.4850", "0.0344"), 100: ("10.4306", "-0.0200"), 101: ("10.4680", "0.0174")}
    table |= {1000: ("10.4486", "-0.0020")}
    prices = {}
    for n, (qp, qe) in table.items():
        v, _, _, _ = crr_tree(S0, K, T, R, SIG, n)
        close(f"N = {n}: backward induction vs binomial sum", v, crr_binomial_sum(S0, K, T, R, SIG, n), 1e-9)
        prices[n] = q(f"  CRR call N = {n}", v, qp)
        q(f"  error N = {n}", v - c_bs, qe)
    assert all(np.sign(prices[n] - c_bs) == (1 if n % 2 else -1) for n in table)
    print("  check the error is positive for every odd N and negative for every even N in the table")
    ratio = (prices[50] - c_bs) / (prices[100] - c_bs)
    q("error ratio N = 50 over N = 100 (halves when N doubles)", ratio, "2.0")
    q("average of N = 100 and N = 101", 0.5 * (prices[100] + prices[101]), "10.4493")
    assert abs(0.5 * (prices[100] + prices[101]) - c_bs) < abs(prices[1000] - c_bs)
    q("u for N = 1", math.exp(0.2), "1.2214")
    q("d for N = 1", math.exp(-0.2), "0.8187")
    p1 = (math.exp(0.05) - math.exp(-0.2)) / (math.exp(0.2) - math.exp(-0.2))
    q("p for N = 1", p1, "0.5775")
    q("u S - K for N = 1", 100 * math.exp(0.2) - 100, "22.14")
    close("one-step call e^{-r} p (uS - K) vs tree", math.exp(-0.05) * p1 * (100 * math.exp(0.2) - 100), prices[1], 1e-12)
    q("one-step call", prices[1], "12.16")
    q("average minus Black-Scholes", 0.5 * (prices[100] + prices[101]) - c_bs, "-0.0013")

    print("\nExample 4 and card deriv-american-put-premium-size: American put")
    p_bs = q("Black-Scholes European put", bs_price(S0, K, T, R, SIG, call=False), "5.5735")
    am = {}
    for n, qv in ((100, "6.0824"), (500, "6.0888"), (2000, "6.0900")):
        am[n] = q(f"  CRR American put N = {n}", crr_tree(S0, K, T, R, SIG, n, call=False, american=True)[0], qv)
    q("card: American put, two decimals", am[2000], "6.09")
    q("card: European put, two decimals", p_bs, "5.57")
    prem = q("early-exercise premium (N = 2000)", am[2000] - p_bs, "0.52")
    q("premium as a percent of the American value", 100 * prem / am[2000], "8.5")

    print("\nExample 5: Greeks from the first two steps of a 500-step tree (call)")
    n = 500
    v0, sl, u_, dt = crr_tree(S0, K, T, R, SIG, n)
    s1 = np.array([S0 * u_, S0 / u_])
    s2 = np.array([S0 * u_**2, S0, S0 / u_**2])
    delta_tree = (sl[1][0] - sl[1][1]) / (s1[0] - s1[1])
    d_up = (sl[2][0] - sl[2][1]) / (s2[0] - s2[1])
    d_dn = (sl[2][1] - sl[2][2]) / (s2[1] - s2[2])
    gamma_tree = (d_up - d_dn) / (0.5 * (s2[0] - s2[2]))
    theta_tree = (sl[2][1] - v0) / (2 * dt)
    sd = SIG * math.sqrt(T)
    d1 = (math.log(S0 / K) + (R + 0.5 * SIG**2) * T) / sd
    delta_bs = norm_cdf(d1)
    gamma_bs = norm_pdf(d1) / (S0 * sd)
    theta_bs = -S0 * norm_pdf(d1) * SIG / (2 * math.sqrt(T)) - R * K * math.exp(-R * T) * norm_cdf(d1 - sd)
    q("tree delta", delta_tree, "0.6368")
    q("Black-Scholes delta", delta_bs, "0.6368")
    q("tree gamma", gamma_tree, "0.01879")
    q("Black-Scholes gamma", gamma_bs, "0.01876")
    q("tree theta per year", theta_tree, "-6.42")
    q("Black-Scholes theta per year", theta_bs, "-6.41")

    print("\nCRR p approximation (r = 5%, 20% vol, N = 100)")
    dt = T / 100
    p_exact = (math.exp(R * dt) - math.exp(-SIG * math.sqrt(dt))) / (math.exp(SIG * math.sqrt(dt)) - math.exp(-SIG * math.sqrt(dt)))
    p_approx = 0.5 + (R - 0.5 * SIG**2) * math.sqrt(dt) / (2 * SIG)
    q("exact p", p_exact, "0.5075")
    close("exact p vs 1/2 + (r - sigma^2/2) sqrt(dt) / (2 sigma)", p_exact, p_approx, 2e-4)
    print("\nAll binomial checks passed.")


if __name__ == "__main__":
    main()
