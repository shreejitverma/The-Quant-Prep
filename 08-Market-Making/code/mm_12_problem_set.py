"""Market making problem set: every number in `08-Market-Making/12-Market-Making-Problem-Set.md`.

Independent routes used here:
- dice markets by enumerating all 36 outcomes and every counterparty action with `fractions.Fraction`,
  with the informed trader deciding from its own enumerated conditional value;
- Glosten-Milgrom quotes by Bayes over the two values and the trader types, not the half-spread formula;
- the Avellaneda-Stoikov reservation price as the CARA indifference price (Gauss-Hermite expectations
  and bisection), and the spread's liquidity term by maximising e^(-k d)(1 - e^(-gamma d)) on a grid;
- thresholds and sizes by bisection or brute force over integers;
- gamma by finite differences of the Black-Scholes price, gamma-scalping P&L and the hedging-frequency
  scaling by seeded simulation with tolerances from standard errors;
- the conversion by its payoff on a grid of terminal prices.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 08-Market-Making/code/mm_12_problem_set.py`.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction as F

import numpy as np

SEED = 20261114


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, expected {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (expected {expected}, tolerance {tol:.4f})")


def bisect(f, lo: float, hi: float, n: int = 100) -> float:
    """Root of f on [lo, hi] where f changes sign once."""
    flo = f(lo)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return 0.5 * (lo + hi)


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call(S: float, K: float, T: float, vol: float) -> float:
    sd = vol * math.sqrt(T)
    d1 = math.log(S / K) / sd + 0.5 * sd
    return S * norm_cdf(d1) - K * norm_cdf(d1 - sd)


def example1() -> None:
    print("Example 1: max of two dice with a counterparty who may have peeked (cards mm-pset-quoting-*)")
    rolls = list(itertools.product(range(1, 7), repeat=2))
    fair = F(sum(max(r) for r in rolls), 36)
    exact("E[max]", fair, F(161, 36))
    approx("E[max]", float(fair), 4.47, 2)
    exact("P(max = m), m = 1..6", [F(sum(max(r) == m for r in rolls), 36) for m in range(1, 7)], [F(2 * m - 1, 36) for m in range(1, 7)])
    cond = {x: F(sum(max(x, y) for y in range(1, 7)), 6) for x in range(1, 7)}
    for x, lit in zip(range(1, 7), (3.50, 3.67, 4.00, 4.50, 5.17, 6.00), strict=True):
        approx(f"E[max | x = {x}]", float(cond[x]), lit, 2)
    bid, ask = 4, 5

    def informed_pnl(x: int, y: int, b: float, a: float) -> F:
        v = cond[x]  # the informed trader acts on its own conditional value
        if v > a:
            return F(a) - max(x, y)
        if v < b:
            return max(x, y) - F(b)
        return F(0)

    inf = sum((informed_pnl(x, y, bid, ask) for x, y in rolls), F(0)) / 36
    exact("expected P&L per informed interaction", inf, F(-1, 3))
    uninf = sum((F(1, 2) * (ask - max(r)) + F(1, 2) * (max(r) - bid) for r in rolls), F(0)) / 36
    exact("expected P&L per uninformed interaction", uninf, F(1, 2))
    pi = bisect(lambda p: float((1 - p) * uninf + p * inf), 0.0, 1.0)
    approx("break-even informed share", pi, 0.6, 9)
    wide = sum((informed_pnl(x, y, F(7, 2), 6) for x, y in rolls), F(0)) / 36
    exact("informed P&L against 3.5 / 6", wide, 0)
    best_vs_informed = max(
        sum((informed_pnl(x, y, F(b, 6), F(a, 6)) for x, y in rolls), F(0)) / 36 for b in range(0, 37) for a in range(b + 1, 43)
    )
    exact("best informed P&L over every quote on a 1/6 grid", best_vs_informed, 0)

    # lifted at 5, half informed: likelihood of a buy given x, then the posterior
    like = {x: F(1, 2) * (cond[x] > ask) + F(1, 2) * F(1, 2) for x in range(1, 7)}
    exact("P(buy | x), x = 1..6", [like[x] for x in range(1, 7)], [F(1, 4)] * 4 + [F(3, 4)] * 2)
    post = sum(like[x] * max(x, y) for x, y in rolls) / sum(like[x] for x, _ in rolls)
    exact("posterior fair value after a lift", post, F(59, 12))
    approx("posterior fair value", float(post), 4.92, 2)
    w = {x: F(1, 2) * (x >= 5) + F(1, 4) for x in cond}
    exact("snippet output", (sum(cond.values()) / 6, sum(w[x] * cond[x] for x in cond) / sum(w.values())), (F(161, 36), F(59, 12)))
    exact("ratio of buy likelihoods, x >= 5 against x <= 4", like[5] / like[4], 3)


def cara_value(x: float, q: float, s: float, gamma: float, var: float) -> float:
    """E[-exp(-gamma (x + q S_T))] with S_T ~ N(s, var), by Gauss-Hermite quadrature."""
    nodes, weights = np.polynomial.hermite_e.hermegauss(80)
    st = s + math.sqrt(var) * nodes
    return float(np.sum(weights * -np.exp(-gamma * (x + q * st))) / math.sqrt(2 * math.pi))


def example2() -> None:
    print("Example 2: Avellaneda-Stoikov quotes with inventory (cards mm-pset-inventory-as-*)")
    s, q, gamma, sigma, tau, k = 100.0, 5, 0.1, 2.0, 0.5, 1.5
    var = sigma * sigma * tau

    def reservation(qq: int) -> float:
        base = cara_value(0.0, qq, s, gamma, var)
        r_bid = bisect(lambda p: cara_value(-p, qq + 1, s, gamma, var) - base, 90.0, 110.0)
        r_ask = bisect(lambda p: cara_value(p, qq - 1, s, gamma, var) - base, 90.0, 110.0)
        return 0.5 * (r_bid + r_ask)

    r = reservation(q)
    approx("reservation price (indifference)", r, 99.00, 6)
    grid = np.linspace(1e-6, 5.0, 2_000_001)
    obj = np.exp(-k * grid) * (1 - np.exp(-gamma * grid))
    delta_star = float(grid[np.argmax(obj)])
    close_form = math.log(1 + gamma / k) / gamma
    assert abs(delta_star - close_form) < 1e-5, (delta_star, close_form)
    approx("liquidity term 2 delta*", 2 * delta_star, 1.291, 3)
    spread = gamma * var + 2 * delta_star
    approx("total spread", spread, 1.491, 3)
    approx("bid", r - spread / 2, 98.25, 2)
    approx("ask", r + spread / 2, 99.75, 2)
    approx("half-spread", spread / 2, 0.745, 3)
    r0 = reservation(0)
    approx("flat bid", r0 - spread / 2, 99.25, 2)
    approx("flat ask", r0 + spread / 2, 100.75, 2)
    approx("ask minus mid when long 5", r + spread / 2 - s, -0.25, 2)
    approx("shift when inventory doubles to 10", s - reservation(10), 2.0, 6)


def example3() -> None:
    print("Example 3: hedge now or wait? (cards mm-pset-inventory-hedge-threshold, mm-pset-inventory-threshold-vol)")
    c, t, gamma = 0.005, 60.0, 0.02
    for sigma, lit, dec in ((0.004, 521, 0), (0.008, 130, 0)):
        q_star = bisect(lambda qq, sg=sigma: 0.5 * gamma * sg * sg * qq * qq * t - c * qq, 1.0, 1e5)
        approx(f"threshold at sigma = {sigma}", q_star, lit, dec)


def example4() -> None:
    print("Example 4: sizing an over-quote in a pro-rata market (card mm-pset-quoting-prorata-size)")
    others = 8000
    s_max = max(s for s in range(0, 20_000) if 5000 * s / (s + others) <= 1500)
    exact("maximum size", s_max, 3428)
    approx("shown working: 12,000,000 / 3,500", 12_000_000 / 3500, 3428.6, 1)
    for size, small_lit, big_lit, avg_lit in ((3400, 60, 1491, 346), (1500, 32, 789, 183)):
        small, big = 200 * size / (size + others), 5000 * size / (size + others)
        approx(f"fill from a 200-lot at {size}", small, small_lit, 0)
        approx(f"fill from a 5,000-lot at {size}", big, big_lit, 0)
        approx(f"average fill at {size}", 0.8 * small + 0.2 * big, avg_lit, 0)


def example5(rng: np.random.Generator) -> None:
    print("Example 5: gamma scalping P&L (cards mm-pset-options-gamma-scalp, mm-pset-options-breakeven-move)")
    S, T, vol = 100.0, 0.25, 0.20
    h = 0.01
    gamma = (bs_call(S + h, S, T, vol) - 2 * bs_call(S, S, T, vol) + bs_call(S - h, S, T, vol)) / h**2
    approx("ATM gamma by finite differences", gamma, 0.0398, 4)
    pos = 500 * 100 * 2 * gamma
    approx("position gamma", pos, 3984, 0)
    theta = 0.5 * pos * S**2 * vol**2 / 252
    approx("daily theta cost", theta, 3162, 0)
    gamma_pnl = 0.5 * pos * S**2 * 0.30**2 / 252
    approx("daily gamma P&L at 30% realised", gamma_pnl, 7115, 0)
    approx("net", gamma_pnl - theta, 3953, 0)
    approx("shown working: 0.5 x 3984 x 1e4 x 0.05 / 252", 0.5 * 3984 * 1e4 * 0.05 / 252, 3952, 0)
    n = 1_000_000
    moves = S * 0.30 / math.sqrt(252) * rng.standard_normal(n)
    sample = 0.5 * pos * moves**2
    simulated("simulated mean daily gamma P&L", float(sample.mean()), round(gamma_pnl), 4 * float(sample.std()) / math.sqrt(n))
    approx("break-even daily move", S * vol / math.sqrt(252), 1.26, 2)
    approx("sqrt(252)", math.sqrt(252), 15.87, 2)


def example6() -> None:
    print("Example 6: implied earnings move from two straddles (card mm-pset-options-event-straddles)")
    total, base = 6.00 / 0.8, 2.50 / 0.8
    approx("total weekly sd", total, 7.5, 1)
    approx("base weekly sd", base, 3.125, 3)
    event = math.sqrt(total**2 - base**2)
    approx("event sd", event, 6.82, 2)
    approx("implied mean absolute event move", 0.8 * event, 5.45, 2)
    approx("naive difference of straddles", 6.00 - 2.50, 3.50, 2)
    approx("sqrt(2/pi), the exact straddle-to-sd factor", math.sqrt(2 / math.pi), 0.8, 1)


def example7() -> None:
    print("Example 7: stale quotes (card mm-pset-systems-stale-cost)")
    cost = 1000 * 20 * 0.3 * 500 * 0.005
    approx("daily cost", cost, 15_000, 0)
    saved = cost - 1000 * 20 * 0.1 * 500 * 0.005
    approx("saving at a 10% loss rate", saved, 10_000, 0)
    approx("annual saving over 250 days", 250 * saved, 2_500_000, 0)


def cards_quoting_and_inventory() -> None:
    print("Quoting and inventory cards")
    exact("join EV", F(35, 100) * (2 - F(15, 10)), F(175, 1000))
    exact("improve EV", F(7, 10) * (1 - F(8, 10)), F(14, 100))
    theo = F(100008, 1000)
    exact("bid edge at 100.00 (cents)", (theo - 100) * 100, F(8, 10))
    exact("ask edge at 100.01 (cents)", (F(10001, 100) - theo) * 100, F(2, 10))
    exact("ask edge at 100.02 (cents)", (F(10002, 100) - theo) * 100, F(12, 10))
    approx("half-life ln 0.5 / ln 0.9", math.log(0.5) / math.log(0.9), 6.58, 2)
    half = bisect(lambda m: 0.9**m - 0.5, 0.0, 50.0)
    approx("half-life by bisection on 0.9^m = 0.5", half, 6.6, 1)


def cards_adverse_selection() -> None:
    print("Adverse selection cards")
    approx("break-even informed share (percent)", 100 * 0.7 / 3, 23, 0)
    mu = F(3, 10)
    p_buy = {110: mu + (1 - mu) / 2, 90: (1 - mu) / 2}
    p_sell = {110: (1 - mu) / 2, 90: mu + (1 - mu) / 2}
    ask = sum(v * p_buy[v] for v in p_buy) / sum(p_buy.values())
    bid = sum(v * p_sell[v] for v in p_sell) / sum(p_sell.values())
    exact("Glosten-Milgrom ask", ask, 103)
    exact("Glosten-Milgrom bid", bid, 97)
    exact("client A net", F(1) + F(-2), -1)
    exact("client B net", F(3, 10) + F(-1, 10), F(2, 10))


def hedging_frequency(rng: np.random.Generator) -> tuple[float, float, float, float]:
    """Discrete delta hedge of a short ATM call.

    Returns the error sd ratio N/2N and the traded-shares ratio 2N/N, each with its standard error from
    40 independent batches of paths.
    """
    S0, T, vol, paths = 100.0, 0.25, 0.20, 40_000

    def run(steps: int, z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        dt = T / steps
        s = np.full(paths, S0)
        cash = np.full(paths, bs_call(S0, S0, T, vol))
        held = np.zeros(paths)
        traded = np.zeros(paths)
        for i in range(steps):
            tau = T - i * dt
            d1 = np.log(s / S0) / (vol * math.sqrt(tau)) + 0.5 * vol * math.sqrt(tau)
            delta = 0.5 * (1.0 + np.vectorize(math.erf)(d1 / math.sqrt(2.0)))
            if i > 0:  # rebalancing trades only; the initial hedge is the same at any frequency
                traded += np.abs(delta - held)
            cash -= (delta - held) * s
            held = delta
            s = s * np.exp(-0.5 * vol * vol * dt + vol * math.sqrt(dt) * z[:, i])
        pnl = cash + held * s - np.maximum(s - S0, 0.0)
        return pnl, traded

    z_fine = rng.standard_normal((paths, 64))
    z_coarse = (z_fine[:, 0::2] + z_fine[:, 1::2]) / math.sqrt(2.0)  # same paths, half the rebalances
    pnl_c, traded_c = run(32, z_coarse)
    pnl_f, traded_f = run(64, z_fine)
    batches = 40
    err_b = [c.std(ddof=1) / f.std(ddof=1) for c, f in zip(np.split(pnl_c, batches), np.split(pnl_f, batches), strict=True)]
    cost_b = [f.mean() / c.mean() for c, f in zip(np.split(traded_c, batches), np.split(traded_f, batches), strict=True)]
    err = float(pnl_c.std(ddof=1) / pnl_f.std(ddof=1))
    cost = float(traded_f.mean() / traded_c.mean())
    return err, float(np.std(err_b, ddof=1)) / math.sqrt(batches), cost, float(np.std(cost_b, ddof=1)) / math.sqrt(batches)


def cards_hedging(rng: np.random.Generator) -> None:
    print("Hedging cards")
    approx("futures contracts", 1.2 * 1_000_000 / (50 * 5000), 4.8, 1)
    approx("residual vol (percent)", 30 * math.sqrt(1 - 0.36), 24, 0)
    err_ratio, err_se, cost_ratio, cost_se = hedging_frequency(rng)
    # Kamal (1998) gives sd proportional to 1/sqrt(N); with proportional costs each trade shrinks by sqrt(2)
    approx("sqrt(2)", math.sqrt(2), 1.41, 2)
    simulated("hedging error sd, 32 over 64 rebalances, against sqrt(2)", err_ratio, math.sqrt(2), 4 * err_se)
    for label, ratio, se in (("hedging error sd", err_ratio, err_se), ("shares traded", cost_ratio, cost_se)):
        approx(f"{label} ratio, lower 4-SE bound, at one decimal", ratio - 4 * se, 1.4, 1)
        approx(f"{label} ratio, upper 4-SE bound, at one decimal", ratio + 4 * se, 1.4, 1)
    excess = (cost_ratio - math.sqrt(2)) / cost_se
    assert excess > 2, excess
    print(f"    shares traded ratio above sqrt(2) by {excess:.1f} standard errors (finite-N excess)")
    assert cost_ratio < 1.6, cost_ratio
    print("    proportional cost rises by about sqrt(2), far from doubling")


def cards_options() -> None:
    print("Options cards")
    approx("shown working: straddle approximation 0.8 x 0.2 x 0.5 x 100", 0.8 * 0.2 * 0.5 * 100, 8, 0)
    exact_straddle = 2 * bs_call(100, 100, 0.25, 0.2)  # r = 0, so put = call at the money
    approx("exact Black-Scholes straddle", exact_straddle, 7.98, 2)
    terminal = np.linspace(0.0, 300.0, 3001)
    payoff = -np.maximum(terminal - 100, 0) + np.maximum(100 - terminal, 0) + terminal
    cost = -5.20 + 4.80 + 100.0
    profit = payoff - cost
    assert np.allclose(profit, profit[0])
    approx("conversion profit at every terminal price", float(profit[0]), 0.40, 2)


def cards_markouts() -> None:
    print("Markout and P&L cards")
    exact("total P&L", 12_000 - 7_000 - 3_000 - 1_500 + 800, 1300)
    exact("quoting after selection", 12_000 - 7_000, 5000)
    exact("fills x markout before", F(1000) * F(3, 10), 300)
    exact("fills x markout after", F(2000) * F(1, 10), 200)
    approx("annualised Sharpe", 20_000 / 10_000 * math.sqrt(252), 31.7, 1)
    approx("annualised Sharpe, rounded", 20_000 / 10_000 * math.sqrt(252), 32, 0)
    exact("worst-case position", 6000 + 3000 + 2000, 11_000)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    example1()
    example2()
    example3()
    example4()
    example5(rng)
    example6()
    example7()
    cards_quoting_and_inventory()
    cards_adverse_selection()
    cards_hedging(rng)
    cards_options()
    cards_markouts()
    print("all problem set checks passed")
