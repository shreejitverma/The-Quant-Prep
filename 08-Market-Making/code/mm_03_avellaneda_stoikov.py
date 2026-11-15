"""Avellaneda-Stoikov inventory model: every quote, spread, intensity and simulation number in the note.

Backs every number in `08-Market-Making/03-Inventory-Risk-and-Avellaneda-Stoikov.md`.
Independent routes used here:
- reservation bid and ask by bisection on the frozen-inventory indifference condition, with the expectation
  E[exp(-gamma q S_T)] taken by Gauss-Hermite quadrature, never via the normal MGF or the closed forms;
- each optimal distance by golden-section maximisation of g(delta) = A exp(-k delta)(1 - exp(-gamma(delta - c))),
  never via the log formula; the risk-neutral limit by maximising delta exp(-k delta) the same way;
- the P&L of the inventory and symmetric strategies by an exact forward recursion over the inventory distribution
  (the quotes depend only on q and t, so inventory is a Markov chain independent of the mid), checked against a
  seeded vectorised simulation and against the repo simulator `avellaneda_stoikov_mm.py`, both within a stated
  number of standard errors.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 08-Market-Making/code/mm_03_avellaneda_stoikov.py`.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from avellaneda_stoikov_mm import AvellanedaStoikovSimulator  # noqa: E402

# Parameters of the paper's simulation (Avellaneda and Stoikov 2008, section 3.3), also the repo simulator's defaults.
S0, SIGMA, GAMMA, K, A_RATE, T, DT = 100.0, 2.0, 0.1, 1.5, 140.0, 1.0, 0.005
SEED = 20261114


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, expected {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (expected {expected:.4f}, tolerance {tol:.4f})")


def sd_standard_error(x: np.ndarray) -> float:
    """Delta-method standard error of the sample sd, from the sample fourth central moment (no normality assumed)."""
    centred = x - x.mean()
    m2, m4 = float(np.mean(centred**2)), float(np.mean(centred**4))
    return math.sqrt((m4 - m2**2) / len(x)) / (2.0 * math.sqrt(m2))


# ------------------------------------------------------------------ numerical building blocks

HERMITE_X, HERMITE_W = np.polynomial.hermite.hermgauss(80)


def frozen_log_value(x: float, s: float, q: int, tau: float, gamma: float = GAMMA, sigma: float = SIGMA) -> float:
    """log(-v) for v = E[-exp(-gamma (x + q S_T))], S_T ~ N(s, sigma^2 tau), by Gauss-Hermite quadrature."""
    if q == 0 or tau == 0.0:
        return -gamma * (x + q * s)
    st = s + math.sqrt(2.0 * tau) * sigma * HERMITE_X
    expo = -gamma * q * st
    peak = expo.max()
    return -gamma * x + peak + math.log(float(np.sum(HERMITE_W * np.exp(expo - peak))) / math.sqrt(math.pi))


def bisect(f, lo: float, hi: float) -> float:
    flo = f(lo)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


def reservation_bid(s: float, q: int, tau: float, gamma: float = GAMMA) -> float:
    """Price r with v(x - r, q + 1) = v(x, q), solved numerically."""
    base = frozen_log_value(0.0, s, q, tau, gamma)
    return bisect(lambda r: frozen_log_value(-r, s, q + 1, tau, gamma) - base, s - 50.0, s + 50.0)


def reservation_ask(s: float, q: int, tau: float, gamma: float = GAMMA) -> float:
    """Price r with v(x + r, q - 1) = v(x, q), solved numerically."""
    base = frozen_log_value(0.0, s, q, tau, gamma)
    return bisect(lambda r: frozen_log_value(r, s, q - 1, tau, gamma) - base, s - 50.0, s + 50.0)


def golden_max(f, lo: float, hi: float) -> float:
    invphi = (math.sqrt(5.0) - 1.0) / 2.0
    a, b = lo, hi
    c, d = b - invphi * (b - a), a + invphi * (b - a)
    for _ in range(200):
        if f(c) > f(d):
            b, d = d, c
            c = b - invphi * (b - a)
        else:
            a, c = c, d
            d = a + invphi * (b - a)
    return 0.5 * (a + b)


def optimal_distance_above(c: float, gamma: float = GAMMA, k: float = K) -> float:
    """argmax of A exp(-k delta)(1 - exp(-gamma (delta - c))) by golden section; returns delta - c."""
    return golden_max(lambda d: A_RATE * math.exp(-k * d) * (1.0 - math.exp(-gamma * (d - c))), c, c + 20.0) - c


def numeric_quotes(s: float, q: int, tau: float, gamma: float = GAMMA) -> tuple[float, float, float, float]:
    """(bid, ask, reservation bid, reservation ask), every piece found numerically."""
    rb, ra = reservation_bid(s, q, tau, gamma), reservation_ask(s, q, tau, gamma)
    # bid side: the bid distance from the mid exceeds s - r^b by the same markup as the ask side
    markup = optimal_distance_above(0.0, gamma)
    return rb - markup, ra + markup, rb, ra


# ------------------------------------------------------------------ sections


def section_quotes() -> None:
    print("Examples 1 and 2, cards mm-as-numeric-quotes and mm-as-reservation-bid-derivation")
    markup = optimal_distance_above(0.0)
    approx("liquidity term 2 x argmax markup (20 ln(16/15))", 2 * markup, 1.2908, 4)
    approx("inventory term gamma sigma^2 (T-t)", reservation_ask(S0, 0, 1.0) - reservation_bid(S0, 0, 1.0), 0.4, 4)
    bid0, ask0, _, _ = numeric_quotes(S0, 0, 1.0)
    approx("total spread at q = 0", ask0 - bid0, 1.6908, 4)
    approx("bid at q = 0", bid0, 99.1546, 4)
    approx("ask at q = 0", ask0, 100.8454, 4)
    approx("half-spread at q = 0", S0 - bid0, 0.8454, 4)
    approx("fill intensity at q = 0", A_RATE * math.exp(-K * (S0 - bid0)), 39.39, 2)

    bid3, ask3, rb3, ra3 = numeric_quotes(S0, 3, 1.0)
    approx("reservation price at q = 3", 0.5 * (rb3 + ra3), 98.8, 4)
    approx("theta^2 = (r - s) / (2q) at T-t = 1, against -gamma sigma^2 / 2", (0.5 * (rb3 + ra3) - S0) / 6, -0.2, 6)
    approx("reservation bid at q = 3", rb3, 98.6, 4)
    approx("reservation ask at q = 3", ra3, 99.0, 4)
    approx("total spread at q = 3", ask3 - bid3, 1.6908, 4)
    approx("total spread at q = 3 (card, 3 dp)", ask3 - bid3, 1.691, 3)
    approx("bid at q = 3", bid3, 97.9546, 4)
    approx("ask at q = 3", ask3, 99.6454, 4)
    approx("bid at q = 3 (card, 2 dp)", bid3, 97.95, 2)
    approx("ask at q = 3 (card, 2 dp)", ask3, 99.65, 2)
    approx("half-spread at q = 3 (card, 3 dp)", 0.5 * (ask3 - bid3), 0.845, 3)
    approx("ask below the mid at q = 3", S0 - ask3, 0.3546, 4)
    approx("bid distance at q = 3", S0 - bid3, 2.0454, 4)
    lam_a, lam_b = A_RATE * math.exp(-K * (ask3 - S0)), A_RATE * math.exp(-K * (S0 - bid3))
    approx("ask intensity at q = 3", lam_a, 238.3, 1)
    approx("bid intensity at q = 3", lam_b, 6.51, 2)
    approx("ratio of sell to buy rates", lam_a / lam_b, 37, 0)
    for q in range(-4, 5):  # the derivation in Step 2, for every small inventory
        assert abs(reservation_bid(S0, q, 1.0) - (S0 - (1 + 2 * q) * GAMMA * SIGMA**2 / 2)) < 1e-9, q
        assert abs(reservation_ask(S0, q, 1.0) - (S0 + (1 - 2 * q) * GAMMA * SIGMA**2 / 2)) < 1e-9, q
    print("    numeric indifference prices equal s - (1 + 2q) gamma sigma^2 (T-t)/2 and s + (1 - 2q) gamma sigma^2 (T-t)/2, q = -4..4")
    # the systems companion's sign: (2q - 1) instead of (1 - 2q) would put the ask at q = 3 above the mid
    wrong_ask = S0 + markup + (2 * 3 - 1) * GAMMA * SIGMA**2 / 2
    assert abs(wrong_ask - ask3) > 1.0, wrong_ask
    print(f"    ask with the wrong (2q - 1) sign at q = 3 = {wrong_ask:.4f}, not {ask3:.4f}")


def section_horizon_and_gamma() -> None:
    print("Example 3: the horizon effect at q = 1 (card mm-as-horizon-artefact)")
    for tau, r_quoted, spread_quoted in ((1.0, 99.60, 1.6908), (0.5, 99.80, 1.4908), (0.1, 99.96, 1.3308), (0.0, 100.00, 1.2908)):
        bid, ask, rb, ra = numeric_quotes(S0, 1, tau)
        approx(f"T-t = {tau}: reservation price", 0.5 * (rb + ra), r_quoted, 2)
        approx(f"T-t = {tau}: total spread", ask - bid, spread_quoted, 4)

    print("Example 4: risk aversion (cards mm-as-risk-neutral-limit, mm-as-k-interpretation)")
    for gamma, inv_q, liq_q, tot_q in ((0.01, 0.04, 1.3289, 1.3689), (0.1, 0.4, 1.2908, 1.6908), (1.0, 4.0, 1.0217, 5.0217)):
        inv = reservation_ask(S0, 0, 1.0, gamma) - reservation_bid(S0, 0, 1.0, gamma)
        liq = 2 * optimal_distance_above(0.0, gamma)
        approx(f"gamma = {gamma}: inventory term", inv, inv_q, 4)
        approx(f"gamma = {gamma}: liquidity term", liq, liq_q, 4)
        approx(f"gamma = {gamma}: total", inv + liq, tot_q, 4)
    monopolist = golden_max(lambda d: d * math.exp(-K * d), 0.0, 20.0)
    approx("risk-neutral optimum argmax delta exp(-k delta) = 1/k", monopolist, 1 / K, 6)
    approx("2/k (limit of the liquidity term)", 2 * monopolist, 1.3333, 4)
    approx("liquidity term at gamma = 1e-6", 2 * optimal_distance_above(0.0, 1e-6), 1.3333, 4)
    liq_by_k = [2 * optimal_distance_above(0.0, GAMMA, k) for k in (0.5, 1.0, 1.5, 3.0, 6.0)]
    assert all(a > b for a, b in zip(liq_by_k[:-1], liq_by_k[1:], strict=True)), liq_by_k
    print("    liquidity term decreases in k for k = 0.5, 1, 1.5, 3, 6")

    print("Example 5: first-order condition with c = 0.3 (card mm-as-first-order-condition)")
    delta = 0.3 + optimal_distance_above(0.3)
    approx("argmax of 140 exp(-1.5 d)(1 - exp(-0.1 (d - 0.3)))", delta, 0.94539, 5)
    approx("0.3 + 10 ln(16/15)", 0.3 + 10 * math.log(16 / 15), 0.94539, 5)
    approx("0.3 + 10 ln(1.0667), the rounded input the note no longer uses", 0.3 + 10 * math.log(1.0667), 0.9457, 4)


# ------------------------------------------------------------------ P&L: exact recursion, simulation, repo simulator


def spread_at(tau: float, gamma: float = GAMMA) -> float:
    return gamma * SIGMA**2 * tau + (2.0 / gamma) * math.log1p(gamma / K)


def distances(strategy: str, qs: np.ndarray, tau: float, gamma: float, sym_spread: float) -> tuple[np.ndarray, np.ndarray]:
    """Bid and ask distances from the mid at inventory qs with tau left."""
    if strategy == "inventory":
        r_minus_s = -qs * gamma * SIGMA**2 * tau
        half = spread_at(tau, gamma) / 2
        return half - r_minus_s, r_minus_s + half
    half = np.full(qs.shape, sym_spread / 2)
    return half, half.copy()


def fill_probs(db: np.ndarray, da: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Per-step fill probability A exp(-k delta) dt, capped at 1 as `rng.random() < p` does."""
    cap = math.log(A_RATE * DT) / K  # at or below this distance a fill is certain; clipping avoids overflow
    pb = np.minimum(A_RATE * np.exp(-K * np.maximum(db, cap)) * DT, 1.0)
    pa = np.minimum(A_RATE * np.exp(-K * np.maximum(da, cap)) * DT, 1.0)
    return pb, pa


def average_spread(gamma: float) -> float:
    times = np.linspace(0.0, T, int(round(T / DT)) + 1)
    return float(np.mean([spread_at(T - t, gamma) for t in times[:-1]]))


def exact_moments(strategy: str, gamma: float, q_max: int = 150) -> tuple[float, float, float, float]:
    """Exact mean and sd of terminal P&L, mean and sd of final inventory, for the paper's discrete scheme.

    Wealth changes by delta_b B_b + delta_a B_a + q_i (S_i - S_{i-1}) each step, where B are the fill indicators.
    The quotes depend only on (q, t), so q is a Markov chain independent of the mid increments; the spread income
    is propagated with its first two moments per inventory state, and the inventory term adds sigma^2 dt E[q_i^2].
    """
    steps = int(round(T / DT))
    times = np.linspace(0.0, T, steps + 1)
    sym = average_spread(gamma)
    qs = np.arange(-q_max, q_max + 1)
    p, m1, m2 = np.zeros(len(qs)), np.zeros(len(qs)), np.zeros(len(qs))
    p[q_max] = 1.0
    inventory_var = 0.0
    for i in range(1, steps + 1):
        db, da = distances(strategy, qs, T - times[i - 1], gamma, sym)
        pb, pa = fill_probs(db, da)
        np_, n1, n2 = np.zeros(len(qs)), np.zeros(len(qs)), np.zeros(len(qs))
        for hit in (0, 1):
            for lift in (0, 1):
                w = (pb if hit else 1 - pb) * (pa if lift else 1 - pa)
                inc = hit * db + lift * da
                c0, c1, c2 = w * p, w * (m1 + inc * p), w * (m2 + 2 * inc * m1 + inc**2 * p)
                shift = hit - lift
                src = slice(max(0, -shift), len(qs) - max(0, shift))
                dst = slice(max(0, shift), len(qs) - max(0, -shift))
                assert shift == 0 or c0[len(qs) - 1 if shift > 0 else 0] < 1e-30, "inventory grid too small"
                np_[dst] += c0[src]
                n1[dst] += c1[src]
                n2[dst] += c2[src]
        p, m1, m2 = np_, n1, n2
        inventory_var += SIGMA**2 * DT * float(np.sum(p * qs**2))
    mean = float(m1.sum())
    var = float(m2.sum()) - mean**2 + inventory_var
    eq = float(np.sum(p * qs))
    return mean, math.sqrt(var), eq, math.sqrt(float(np.sum(p * qs**2)) - eq**2)


def simulate(strategy: str, gamma: float, paths: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Vectorised Monte Carlo of the same scheme; returns terminal P&L and final inventory per path."""
    steps = int(round(T / DT))
    times = np.linspace(0.0, T, steps + 1)
    sym = average_spread(gamma)
    s = np.full(paths, S0)
    q = np.zeros(paths)
    cash = np.zeros(paths)
    for i in range(1, steps + 1):
        s_prev = s
        s = s + SIGMA * math.sqrt(DT) * rng.standard_normal(paths)
        db, da = distances(strategy, q, T - times[i - 1], gamma, sym)
        pb, pa = fill_probs(db, da)
        hit = rng.random(paths) < pb
        lift = rng.random(paths) < pa
        cash = cash - hit * (s_prev - db) + lift * (s_prev + da)
        q = q + hit - lift
    return cash + q * s, q


def section_simulation() -> None:
    print("Example 6 and card mm-as-vs-symmetric: inventory strategy against symmetric quoting at the average spread")
    grid = np.linspace(0.0, T, int(round(T / DT)) + 1)
    approx("mean time left T - t over the 200 quoting steps", float(np.mean(T - grid[:-1])), 0.5025, 4)
    approx("average spread of the inventory strategy, gamma = 0.1", average_spread(0.1), 1.4918, 4)
    approx("paper's printed average spread", average_spread(0.1), 1.49, 2)
    rows = {
        "inventory": (64.89, 6.54, 2.93),
        "symmetric": (68.22, 13.46, 8.40),
    }
    exact = {}
    for strategy, (mean_q, sd_q, sdq_q) in rows.items():
        mean, sd, eq, sdq = exact_moments(strategy, 0.1)
        exact[strategy] = (mean, sd, sdq)
        approx(f"{strategy}: exact mean terminal P&L", mean, mean_q, 2)
        approx(f"{strategy}: exact sd of P&L", sd, sd_q, 2)
        approx(f"{strategy}: exact sd of final inventory", sdq, sdq_q, 2)
        assert abs(eq) < 1e-9, eq
    give_up = 1 - exact["inventory"][0] / exact["symmetric"][0]
    approx("share of mean P&L given up", 100 * give_up, 5, 0)
    approx("sd ratio inventory / symmetric", exact["inventory"][1] / exact["symmetric"][1], 0.49, 2)

    rng = np.random.default_rng(SEED)
    paths = 20_000
    for strategy, (mean, sd, sdq) in exact.items():
        pnl, qf = simulate(strategy, 0.1, paths, rng)
        se = sd / math.sqrt(paths)
        simulated(f"{strategy}: simulated mean P&L, {paths} paths", float(pnl.mean()), mean, 4 * se)
        simulated(f"{strategy}: simulated sd of P&L", float(pnl.std(ddof=1)), sd, 4 * sd_standard_error(pnl))
        simulated(f"{strategy}: simulated sd of final q", float(qf.std(ddof=1)), sdq, 4 * sd_standard_error(qf))

    print("The repo simulator avellaneda_stoikov_mm.py (inventory strategy), 400 seeded paths")
    finals = []
    for seed in range(400):
        _, _, qpath, wealth = AvellanedaStoikovSimulator(seed=seed).run()
        finals.append((wealth[-1], qpath[-1]))
    w = np.array(finals)
    mean, sd, sdq = exact["inventory"]
    simulated("repo simulator mean P&L", float(w[:, 0].mean()), mean, 4 * sd / math.sqrt(len(w)))
    simulated("repo simulator sd of final q", float(w[:, 1].std(ddof=1)), sdq, 4 * sd_standard_error(w[:, 1]))

    print("The paper's tables (1,000 paths each) against the exact values for gamma = 0.01, 0.1 and 1")
    paper = {  # Avellaneda and Stoikov (2008), Tables 1-3: average spread, profit, sd(profit), sd(final q)
        0.1: {"spread": 1.49, "inventory": (65.0, 6.6, 2.9), "symmetric": (68.4, 12.7, 8.4)},
        0.01: {"spread": 1.35, "inventory": (68.6, 8.7, 5.1), "symmetric": (68.8, 12.8, 8.7)},
        1.0: {"spread": 3.02, "inventory": (31.4, 5.0, 1.7), "symmetric": (44.0, 11.0, 5.1)},
    }
    for gamma, table in paper.items():
        assert abs(average_spread(gamma) - table["spread"]) < 0.015, (gamma, average_spread(gamma))
        for strategy in ("inventory", "symmetric"):
            mean, sd, _, sdq = exact_moments(strategy, gamma)
            pm, psd, psdq = table[strategy]
            z = (abs(pm - mean) / (sd / math.sqrt(1000)), abs(psd - sd) / (sd / math.sqrt(2000)), abs(psdq - sdq) / (sdq / math.sqrt(2000)))
            assert max(z) <= 3.0, (gamma, strategy, z)  # normal-theory standard errors for one run of 1,000 paths
            zs = ", ".join(f"{v:.1f}" for v in z)
            print(f"    gamma = {gamma}, {strategy}: exact {mean:.2f}, {sd:.2f}, {sdq:.2f}; paper {pm}, {psd}, {psdq}; z = {zs}")
    z_sym_sd = abs(12.7 - exact["symmetric"][1]) / (exact["symmetric"][1] / math.sqrt(2000))
    approx("paper's symmetric sd of P&L (12.7), standard errors below the exact value", z_sym_sd, 2.5, 1)
    print("    every paper figure lies within three normal-theory standard errors of the exact value")


if __name__ == "__main__":
    section_quotes()
    section_horizon_and_gamma()
    section_simulation()
