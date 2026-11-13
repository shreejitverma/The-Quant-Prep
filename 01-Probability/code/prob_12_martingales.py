"""Martingales and optional stopping: every number in the note, recomputed by an independent route.

Backs `01-Probability/12-Martingales-and-Optional-Stopping.md`.
Independent routes:
- pattern waiting times (HTH, HHT, HH, HT, 66, ABRACADABRA) by an exact first-step solve on the suffix-prefix
  automaton, compared with the casino closed form;
- Wald's die example by a first-step equation for the remaining sum and by simulation;
- Wald's second identity by an exact solve of the exit-time equations;
- the Polya urn law by exact enumeration of every draw sequence and its limit by simulation;
- the doubling strategy with a credit cap by exact enumeration;
- Doob's bound for driftless GBM by the hitting probability of Brownian motion with drift and by a simulation that
  samples the exact maximum of each Brownian bridge piece.
Simulation tolerances are five standard errors; the seed is fixed.
Run it with `python 01-Probability/code/prob_12_martingales.py`.
"""

from __future__ import annotations

import itertools
import math
import string
from fractions import Fraction

import numpy as np

SEED = 20261019
RNG = np.random.default_rng(SEED)


def exact(label: str, value: Fraction | int, expected: Fraction | int) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")
    return value


def sim_mean(label: str, samples: np.ndarray, target: float) -> None:
    est = float(samples.mean())
    se = float(samples.std(ddof=1)) / math.sqrt(samples.size)
    assert abs(est - target) <= 5.0 * se + 1e-12, f"{label}: simulated {est} (se {se}), target {target}"
    print(f"    {label}: simulated {est:.4f} (se {se:.4f}) vs {target:.4f}")


def solve_exact(a: list[list[Fraction]], b: list[Fraction]) -> list[Fraction]:
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        inv = 1 / m[col][col]
        m[col] = [v * inv for v in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [vr - f * vc for vr, vc in zip(m[r], m[col], strict=True)]
    return [m[i][n] for i in range(n)]


def automaton_wait(pattern: str, probs: dict[str, Fraction]) -> Fraction:
    prefixes = {pattern[:k] for k in range(len(pattern) + 1)}
    states = [pattern[:k] for k in range(len(pattern))]
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    a = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for s in states:
        for ch, p in probs.items():
            t = s + ch
            while t not in prefixes:
                t = t[1:]
            if t != pattern:
                a[idx[s]][idx[t]] -= p
    return solve_exact(a, [Fraction(1)] * n)[0]


def casino_wait(pattern: str, probs: dict[str, Fraction]) -> Fraction:
    return sum(
        (1 / math.prod(probs[c] for c in pattern[:k]) for k in range(1, len(pattern) + 1) if pattern[:k] == pattern[-k:]),
        Fraction(0),
    )


def patterns() -> None:
    print("Pattern waiting times: automaton solve (exact) versus the casino argument")
    coin = {"H": Fraction(1, 2), "T": Fraction(1, 2)}
    die = {str(k): Fraction(1, 6) for k in range(1, 7)}
    for pat, probs, want, where in (
        ("HTH", coin, 10, "card prob-mart-hth-waiting"),
        ("HHT", coin, 8, "card prob-mart-hth-waiting"),
        ("HH", coin, 6, "worked example"),
        ("HT", coin, 4, "worked example"),
        ("66", die, 42, "worked example"),
    ):
        auto = automaton_wait(pat, probs)
        exact(f"E[wait for {pat}] ({where})", auto, Fraction(want))
        assert auto == casino_wait(pat, probs)
    letters = {c: Fraction(1, 26) for c in string.ascii_uppercase}
    word = "ABRACADABRA"
    auto = automaton_wait(word, letters)
    exact("ABRACADABRA by automaton (card prob-mart-abracadabra)", auto, Fraction(26**11 + 26**4 + 26))
    exact("ABRACADABRA keystrokes", auto, Fraction(3_670_344_487_444_778))
    overlaps = [word[:k] for k in range(1, len(word) + 1) if word[:k] == word[-k:]]
    exact("prefixes that are also suffixes", tuple(overlaps), ("A", "ABRA", "ABRACADABRA"))
    # Occurrence rate of HTH is 1/8 per flip despite the longer wait: count in a long simulated sequence.
    flips = RNG.random(2_000_000) < 0.5
    hth = flips[:-2] & ~flips[1:-1] & flips[2:]
    sim_mean("occurrences of HTH per position", hth.astype(float), 1 / 8)


def wald() -> None:
    print("Worked example: Wald's identity with dice")
    # First-step on the remaining sum V: V = sum_x (x + [x != 6] V)/6, independent of Wald.
    v = solve_exact([[1 - Fraction(5, 6)]], [Fraction(sum(range(1, 7)), 6)])[0]
    exact("E[sum until first six] by first-step", v, Fraction(21))
    exact("Wald: 3.5 * 6", Fraction(7, 2) * 6, v)
    exact("6 + E[tau - 1] * 3", 6 + (6 - 1) * Fraction(3), v)
    exact("mean of a non-six roll", Fraction(sum(range(1, 6)), 5), Fraction(3))
    n = 200_000
    rolls = RNG.integers(1, 7, size=(n, 120))
    first6 = (rolls == 6).argmax(axis=1)
    assert (rolls == 6).any(axis=1).all()
    mask = np.arange(120)[None, :] <= first6[:, None]
    sim_mean("simulated sum until first six (card prob-mart-wald-die-until-six)", (rolls * mask).sum(axis=1).astype(float), 21.0)
    print("Card prob-mart-wald-second-identity: exit time of a fair walk from (-a, b), a = 3, b = 5")
    a_, b_ = 3, 5
    n_top = a_ + b_
    idx = range(1, n_top)
    mat = [[Fraction(int(i == j)) - Fraction(1, 2) * int(abs(i - j) == 1) for j in idx] for i in idx]
    t = solve_exact(mat, [Fraction(1)] * (n_top - 1))
    exact("E[exit time] by exact solve", t[a_ - 1], Fraction(a_ * b_))
    hit_b = solve_exact(mat, [Fraction(0)] * (n_top - 2) + [Fraction(1, 2)])
    exact("P(exit at +b)", hit_b[a_ - 1], Fraction(a_, a_ + b_))
    exact("Wald II: b^2 a/(a+b) + a^2 b/(a+b)", Fraction(b_**2 * a_ + a_**2 * b_, a_ + b_), t[a_ - 1])


def compensators() -> None:
    print("Cards: compensators, the exponential martingale and likelihood ratios")
    paths = np.array(list(itertools.product((-1, 1), repeat=8))).cumsum(axis=1)
    for n in range(1, 8):
        for s_val in np.unique(paths[:, n - 1]):
            sel = paths[:, n - 1] == s_val
            assert float((paths[sel, n] ** 2).mean()) == s_val**2 + 1
    print("    fair walk: E[S_(n+1)^2 | S_n] = S_n^2 + 1 on every node, n = 1..7 (card prob-mart-square-compensator)")
    for p in (Fraction(2, 5), Fraction(3, 5), Fraction(49, 100)):
        r = (1 - p) / p
        assert p * r + (1 - p) / r == 1
    print("    p r + q / r = 1 at r = q/p for p in {2/5, 3/5, 49/100} (card prob-mart-biased-exponential)")
    x = RNG.standard_normal((400_000, 5))
    lr = np.exp((0.5 * x - 0.125).sum(axis=1))  # g = N(0.5, 1), f = N(0, 1)
    sim_mean("E_f[L_5] for g = N(0.5, 1) over f = N(0, 1) (card prob-mart-likelihood-ratio)", lr, 1.0)


def doubling() -> None:
    print("Core concepts: doubling with a credit cap of ten losses (bankroll 1023)")
    k = 10
    outcomes = {}
    for seq in itertools.product((0, 1), repeat=k):
        stake, pnl = 1, 0
        for win in seq:
            if win:
                pnl += stake
                break
            pnl -= stake
            stake *= 2
        outcomes[pnl] = outcomes.get(pnl, Fraction(0)) + Fraction(1, 2**k)
    exact("P(win 1)", outcomes[1], Fraction(1023, 1024))
    exact("P(lose 1023)", outcomes[-1023], Fraction(1, 1024))
    exact("expected P&L", sum(v * p for v, p in outcomes.items()), Fraction(0))


def polya() -> None:
    print("Worked example: Polya urn")
    for n in range(1, 9):
        dist = [Fraction(0)] * (n + 1)
        for seq in itertools.product((0, 1), repeat=n):
            red, blue, p = 1, 1, Fraction(1)
            for draw in seq:
                if draw:
                    p *= Fraction(red, red + blue)
                    red += 1
                else:
                    p *= Fraction(blue, red + blue)
                    blue += 1
            dist[sum(seq)] += p
        assert all(d == Fraction(1, n + 1) for d in dist), (n, dist)
        k = n // 2
        seq_prob = Fraction(math.factorial(k) * math.factorial(n - k), math.factorial(n + 1))
        assert dist[k] == math.comb(n, k) * seq_prob
    print("    number of reds in n draws is uniform on 0..n for n = 1..8 (card prob-mart-polya-urn-distribution)")
    urns, steps = 50_000, 2_000
    red = np.ones(urns)
    for t in range(steps):
        red += RNG.random(urns) < red / (t + 2)
    frac = red / (steps + 2)
    sim_mean("limit fraction: mean 1/2", frac, 0.5)
    sim_mean("limit fraction: P(frac < 0.25) for U(0,1) (card prob-mart-polya-urn-limit)", (frac < 0.25).astype(float), 0.25)
    sim_mean("limit fraction: P(frac < 0.8)", (frac < 0.8).astype(float), 0.8)


def biased_ruin() -> None:
    print("Worked example: biased ruin by martingales against an exact first-step solve (p = 0.4, i = 5, N = 10)")
    p, i, n_top = Fraction(2, 5), 5, 10
    q = 1 - p
    r = q / p
    idx = range(1, n_top)
    mat = [[Fraction(int(a == b)) - (p if b == a + 1 else q if b == a - 1 else 0) for b in idx] for a in idx]
    h = solve_exact(mat, [Fraction(0)] * (n_top - 2) + [p])[i - 1]
    d = solve_exact(mat, [Fraction(1)] * (n_top - 1))[i - 1]
    exact("h from the r^S martingale equals the solve", (1 - r**i) / (1 - r**n_top), h)
    exact("E[tau] = (N h - i)/(p - q) equals the solve", (n_top * h - i) / (p - q), d)
    print("Card prob-mart-drift-duration: p = 0.6, b = 3, E[tau] = b/(p - q) = 15")
    steps = np.where(RNG.random((20_000, 400)) < 0.6, 1, -1).cumsum(axis=1)
    assert (steps >= 3).any(axis=1).all()
    sim_mean("simulated E[time to +3]", ((steps >= 3).argmax(axis=1) + 1).astype(float), 15.0)


def doob_gbm() -> None:
    print("Worked example: probability a driftless GBM from 100 ever reaches 200")
    s0, barrier = 100.0, 200.0
    exact("Doob bound S_0/a", Fraction(100, 200), Fraction(1, 2))
    # log S = log S0 - t/2 + W_t (sigma = 1); BM with drift -mu hits a > 0 with probability exp(-2 mu a).
    a = math.log(barrier / s0)
    p_hit = math.exp(-2 * 0.5 * a)
    quoted("P(hit) from the drifted-Brownian hitting law", p_hit, 0.5, 12)
    paths, dt, horizon = 100_000, 0.05, 60.0
    x = np.zeros(paths)
    hit = np.zeros(paths, dtype=bool)
    for _ in range(int(horizon / dt)):
        x_next = x - 0.5 * dt + math.sqrt(dt) * RNG.standard_normal(paths)
        bridge_max = 0.5 * (x + x_next + np.sqrt((x_next - x) ** 2 - 2 * dt * np.log(RNG.random(paths))))
        hit |= bridge_max >= a
        x = x_next
    sim_mean("simulated P(ever reach 200) (card prob-mart-doob-maximal-doubling)", hit.astype(float), 0.5)


if __name__ == "__main__":
    patterns()
    wald()
    compensators()
    doubling()
    biased_ruin()
    polya()
    doob_gbm()
    print("All martingale checks passed.")
