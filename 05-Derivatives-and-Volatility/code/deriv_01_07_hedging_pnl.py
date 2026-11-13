"""Delta hedging and gamma scalping P&L: every number in 06-Delta-Hedging-and-Gamma-Scalping.md.

1. The two-day straddle scalp: second-order estimate against exact Black-Scholes revaluation.
2. Monte Carlo of a discretely delta-hedged long call: hedging at realised versus implied vol, with and without drift.
3. The gamma-theta identity on simulated hedged paths: per-path P&L against sum of 0.5 Gamma S^2 [(dS/S)^2 - sigma^2 dt].
4. Discrete hedging noise against the sqrt(pi/4) vega sigma / sqrt(N) rule, and a replication of Table 1 of the
   Goldman Sachs note that states it (one-month ATM put, r = 5%, 50,000 paths in the note).
5. Proportional transaction costs: Monte Carlo cost with common random numbers against the sqrt(N) formula; Leland's vol.

All simulations use numpy's default_rng with the seeds named below and exact lognormal steps.

Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/deriv_01_07_hedging_pnl.py
"""

from __future__ import annotations

import math

import numpy as np
from pricing_core import bs_price, bs_vega, norm_cdf, norm_pdf

SEED_TABLE = 11  # Example 2
SEED_NOISE = 12  # Examples 4 and 5 (common random numbers with and without costs)
SEED_IDENTITY = 13  # Example 3, gamma-theta identity
SEED_KAMAL = 14  # replication of the Goldman Sachs table


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


def call_delta(S: np.ndarray, K: float, tau: float, r: float, sigma: float) -> np.ndarray:
    sd = sigma * math.sqrt(tau)
    return np.asarray(norm_cdf((np.log(S / K) + (r + 0.5 * sigma**2) * tau) / sd))


def call_gamma(S: np.ndarray, K: float, tau: float, r: float, sigma: float) -> np.ndarray:
    sd = sigma * math.sqrt(tau)
    return np.asarray(norm_pdf((np.log(S / K) + (r + 0.5 * sigma**2) * tau) / sd)) / (S * sd)


def hedge_sim(
    sig_real: float,
    sig_hedge: float,
    sig_implied: float,
    n_steps: int,
    paths: int,
    seed: int,
    mu: float = 0.0,
    r: float = 0.0,
    cost: float = 0.0,
    T: float = 1.0,
    S0: float = 100.0,
    K: float = 100.0,
    long_call: bool = True,
    track_identity: bool = False,
):
    """Buy (or sell) one call at sig_implied, delta-hedge at sig_hedge n_steps times, cash at r; return P&L at T.

    The stock follows exact lognormal steps with drift mu and vol sig_real.
    Proportional cost `cost` is paid on every share traded, including the entry and the final unwind.
    With track_identity, also returns sum_i 0.5 Gamma_i S_i^2 [(dS_i / S_i)^2 - sig_hedge^2 dt] (r = 0 only).
    """
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    sign = 1.0 if long_call else -1.0
    S = np.full(paths, S0)
    h = sign * call_delta(S, K, T, r, sig_hedge)  # shares held short against the option: position is option - h shares
    cash = -sign * bs_price(S0, K, T, r, sig_implied) + h * S - cost * np.abs(h) * S
    gt_sum = np.zeros(paths)
    for i in range(1, n_steps + 1):
        z = rng.standard_normal(paths)
        S_new = S * np.exp((mu - 0.5 * sig_real**2) * dt + sig_real * math.sqrt(dt) * z)
        if track_identity:
            g = call_gamma(S, K, T - (i - 1) * dt, r, sig_hedge)
            gt_sum += 0.5 * g * S**2 * ((S_new / S - 1.0) ** 2 - sig_hedge**2 * dt)
        S = S_new
        cash *= math.exp(r * dt)
        h_new = sign * call_delta(S, K, T - i * dt, r, sig_hedge) if i < n_steps else np.zeros(paths)
        cash += (h_new - h) * S - cost * np.abs(h_new - h) * S
        h = h_new
    pnl = cash + sign * np.maximum(S - K, 0.0)
    return (pnl, gt_sum) if track_identity else pnl


def main() -> None:
    print("Example 1: one-month ATM straddle, S = K = 100, 20% vol, zero rates")
    T1 = 1 / 12
    c = bs_price(100, 100, T1, 0.0, 0.2)
    q("straddle price", 2 * c, "4.61")
    g = float(call_gamma(np.array(100.0), 100, T1, 0.0, 0.2))
    theta = -0.5 * 0.04 * 100**2 * g / 365
    q("gamma per option", g, "0.0691")
    q("theta per option per day", theta, "-0.0378")
    q("straddle gamma", 2 * g, "0.138")
    q("straddle theta per day", 2 * theta, "-0.0757")
    q("straddle theta per day, three decimals (card)", 2 * theta, "-0.076")
    q("sqrt(365)", math.sqrt(365), "19")
    q("sqrt(252)", math.sqrt(252), "16")
    q("breakeven daily move", 100 * 0.2 / math.sqrt(365), "1.05")
    q("delta change on a 2-dollar rally, Gamma x 2", 2 * g * 2, "0.276")
    q("scalp profit, 0.276 x 2", 2 * g * 2 * 2, "0.55")
    q("two days of theta", -2 * 2 * theta, "0.15")
    q("net", 2 * g * 2 * 2 + 2 * 2 * theta, "0.40")
    q("gamma P&L of two 0.5 moves", 2 * 0.5 * 2 * g * 0.25, "0.035")

    def straddle_delta(s: float, tau: float) -> float:
        return 2 * float(call_delta(np.array(s), 100, tau, 0.0, 0.2)) - 1

    d0 = q("exact straddle delta at 100 today", straddle_delta(100, T1), "0.023")
    d1 = q("exact straddle delta at 102 one day later", straddle_delta(102, T1 - 1 / 365), "0.294")
    q("exact delta change", d1 - d0, "0.271")
    # Exact two-day P&L of the scalp: straddle revalued, hedge rebalanced to the exact delta each day.
    strad = [2 * bs_price(s, 100, tau, 0.0, 0.2) - (s - 100) for s, tau in ((100, T1), (102, T1 - 1 / 365), (100, T1 - 2 / 365))]
    pnl_exact = (strad[1] - strad[0] - d0 * 2) + (strad[2] - strad[1] - d1 * (-2))
    q("exact two-day hedged P&L", pnl_exact, "0.39")

    print(f"\nExample 2: one-year ATM call bought at 20%, realised 25%, 365 daily rebalances, 20,000 paths (seed {SEED_TABLE})")
    v25, v20 = bs_price(100, 100, 1.0, 0.0, 0.25), bs_price(100, 100, 1.0, 0.0, 0.20)
    q("V(20%)", v20, "7.97")
    q("V(25%)", v25, "9.95")
    q("V(25%) - V(20%)", v25 - v20, "1.98")
    vega = bs_vega(100, 100, 1.0, 0.0, 0.2)
    q("vega", vega, "39.7")
    q("vega x 0.05", vega * 0.05, "1.98")
    runs = [("hedge at realised 25%", 0.25, 0.0, "1.98", "0.45"), ("hedge at implied 20%", 0.20, 0.0, "2.00", "0.96")]
    runs.append(("hedge at implied 20%, drift 10%", 0.20, 0.10, "1.98", "0.95"))
    table = {}
    for label, sh, mu, qm, qs in runs:
        pnl = hedge_sim(0.25, sh, 0.20, 365, 20_000, SEED_TABLE, mu=mu)
        table[(sh, mu)] = pnl
        se = float(pnl.std(ddof=1)) / math.sqrt(len(pnl))
        q(f"{label}: mean P&L", float(pnl.mean()), qm)
        q(f"{label}: std of P&L", float(pnl.std(ddof=1)), qs)
        close(f"{label}: mean within 3 standard errors of V(25%) - V(20%)", float(pnl.mean()), v25 - v20, 3 * se)
    paired = table[(0.20, 0.0)] - table[(0.20, 0.10)]  # same seed, so each path pairs a 0% and a 10% drift run
    q("drift 0% minus 10%, hedged at implied: paired mean difference", float(paired.mean()), "0.015")
    q("paired standard error", float(paired.std(ddof=1)) / math.sqrt(len(paired)), "0.005")
    q("paired mean difference as a share of 1.98 (%)", 100 * float(paired.mean()) / (v25 - v20), "0.8")
    q("drift 0% minus 10%: change in std of P&L", float(table[(0.20, 0.0)].std(ddof=1) - table[(0.20, 0.10)].std(ddof=1)), "0.01")

    print(f"\nExample 3: gamma-theta identity on hedged paths (realised 25%, hedged and marked at 20%, 252 steps, seed {SEED_IDENTITY})")
    pnl, gt = hedge_sim(0.25, 0.20, 0.20, 252, 20_000, SEED_IDENTITY, track_identity=True)
    resid = pnl - gt
    corr = float(np.corrcoef(pnl, gt)[0, 1])
    q("mean hedged P&L", float(pnl.mean()), "1.98")
    q("mean of sum 0.5 Gamma S^2 [(dS/S)^2 - sigma_i^2 dt]", float(gt.mean()), "1.98")
    q("correlation across paths", corr, "0.996")
    q("share of P&L variance explained, corr^2 (%)", 100 * corr**2, "99.2")
    q("std of the residual (higher-order terms)", float(resid.std(ddof=1)), "0.09")
    q("std of the hedged P&L", float(pnl.std(ddof=1)), "1.00")

    print(f"\nExample 4: discrete hedging noise, realised = implied = 20%, 40,000 paths (seed {SEED_NOISE})")
    coef = q("sqrt(pi/4) x vega x sigma", math.sqrt(math.pi / 4) * vega * 0.2, "7.04")
    q("sqrt(pi/4)", math.sqrt(math.pi / 4), "0.886")
    noise = {}
    for n, qf, qmc in ((12, "2.03", "1.93"), (52, "0.98", "0.96"), (252, "0.44", "0.44")):
        q(f"N = {n}: formula sd", coef / math.sqrt(n), qf)
        pnl = hedge_sim(0.2, 0.2, 0.2, n, 40_000, SEED_NOISE)
        noise[n] = pnl
        q(f"N = {n}: Monte Carlo sd", float(pnl.std(ddof=1)), qmc)
        assert abs(float(pnl.mean())) < 3 * float(pnl.std(ddof=1)) / math.sqrt(40_000) + 0.01
    q("weekly noise as a fraction of the 7.97 premium (%)", 100 * float(noise[52].std(ddof=1)) / v20, "12")
    q("weekly noise in vol points, sd / vega", 100 * float(noise[52].std(ddof=1)) / vega, "2.4")

    print(f"\nGoldman Sachs Table 1 replication: one-month ATM put sold, r = 5%, 20% vol (seed {SEED_KAMAL}, 50,000 paths)")
    put0 = bs_price(100, 100, 1 / 12, 0.05, 0.2, call=False)
    q("Black-Scholes put (the note prints 2.512, which is the call)", put0, "2.096")
    q("Black-Scholes call", bs_price(100, 100, 1 / 12, 0.05, 0.2), "2.512")
    vega_pt = bs_vega(100, 100, 1 / 12, 0.05, 0.2) / 100
    q("vega per vol point", vega_pt, "0.115")
    for n, qf, qt in ((21, "0.443", "0.43"), (84, "0.222", "0.22")):
        q(f"N = {n}: formula sqrt(pi/4) vega 20 / sqrt(N)", math.sqrt(math.pi / 4) * vega_pt * 20 / math.sqrt(n), qf)
        # A short put hedged with the put delta has the same P&L distribution, up to sign, as a long put; parity makes
        # put = call - S + K e^{-rT}, so hedging the call with the call delta replicates it exactly.
        pnl = hedge_sim(0.2, 0.2, 0.2, n, 50_000, SEED_KAMAL, r=0.05, T=1 / 12, long_call=False)
        q(f"N = {n}: Monte Carlo sd (the note's Table 1 reports 0.41 and 0.20)", float(pnl.std(ddof=1)), qt)

    print(f"\nExample 5: one-way cost 5bp, same paths as Example 4 (seed {SEED_NOISE}, common random numbers)")
    for n, qf, qmc, qsd in ((12, "0.05", "0.11", "1.93"), (52, "0.11", "0.17", "0.95"), (252, "0.25", "0.31", "0.45")):
        q(f"N = {n}: formula rebalancing cost kappa sqrt(2/pi) vega sqrt(N)", 0.0005 * math.sqrt(2 / math.pi) * vega * math.sqrt(n), qf)
        pnl_c = hedge_sim(0.2, 0.2, 0.2, n, 40_000, SEED_NOISE, cost=0.0005)
        total_cost = float((noise[n] - pnl_c).mean())
        q(f"N = {n}: Monte Carlo total cost", total_cost, qmc)
        q(f"N = {n}: hedge noise sd with costs", float(pnl_c.std(ddof=1)), qsd)
        noise[(n, "cost")] = total_cost
    q("sqrt(2/pi)", math.sqrt(2 / math.pi), "0.798")
    q("initial call delta", float(call_delta(np.array(100.0), 100, 1.0, 0.0, 0.2)), "0.540")
    entry = 0.0005 * float(call_delta(np.array(100.0), 100, 1.0, 0.0, 0.2)) * 100
    q("entry trade cost kappa Delta_0 S_0", entry, "0.027")
    formula_252 = 0.0005 * math.sqrt(2 / math.pi) * vega * math.sqrt(252)
    q("Monte Carlo cost minus formula at N = 252 (entry and exit)", noise[(252, "cost")] - formula_252, "0.05")
    q("extra cost of daily over weekly hedging", noise[(252, "cost")] - noise[(52, "cost")], "0.14")
    le = q("Leland 2 kappa sigma sqrt(2 / (pi dt)), daily", 2 * 0.0005 * 0.2 * math.sqrt(2 * 252 / math.pi), "0.00253")
    q("Leland vol for short gamma (%)", 100 * math.sqrt(0.04 + le), "20.62")
    q("Leland vol for long gamma (%)", 100 * math.sqrt(0.04 - le), "19.36")
    q("Leland widening above 20% (vol points)", 100 * math.sqrt(0.04 + le) - 20, "0.6")
    q("Leland widening below 20% (vol points)", 20 - 100 * math.sqrt(0.04 - le), "0.6")

    print("\nCards")
    q("deriv-discrete-hedging-error: 0.886 x 39.7 x 0.2 / sqrt(52)", coef / math.sqrt(52), "0.98")
    one_gap = 0.5 * 0.10**2
    ten_steps = 10 * 0.5 * 0.01**2
    q("deriv-short-gamma-risk: loss ratio, one 10% gap vs ten 1% steps", one_gap / ten_steps, "10")
    print("\nAll hedging P&L checks passed.")


if __name__ == "__main__":
    main()
