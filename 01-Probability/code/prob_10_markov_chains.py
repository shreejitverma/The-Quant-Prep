"""Markov chains: every number in the note, recomputed by exact linear solves and enumeration.

Backs `01-Probability/10-Markov-Chains.md`.
Independent routes:
- stationary laws by an exact rational solve of pi P = pi, return times by a separate first-step solve of hitting times;
- pattern waiting times by building the suffix-prefix automaton and solving its first-step equations in exact rationals,
  compared with the casino (prefix-equals-suffix) closed form from the martingale note;
- Penney races by an exact solve on the joint automaton and a seeded simulation;
- knight, king and clock return times by a first-step solve on the full board, not via pi = deg/2|E|;
- the cycle's last-visited vertex and cover time by an exact solve on (visited arc, position) states.
Simulation tolerances are five standard errors; the seed is fixed.
Run it with `python 01-Probability/code/prob_10_markov_chains.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261019
RNG = np.random.default_rng(SEED)


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")
    return value


def exact(label: str, value: Fraction | int, expected: Fraction | int) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def solve_exact(a: list[list[Fraction]], b: list[Fraction]) -> list[Fraction]:
    """Gauss-Jordan elimination in exact rationals."""
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


def next_state(state: str, ch: str, prefixes: set[str]) -> str:
    """Longest suffix of state + ch that is a prefix of some pattern."""
    s = state + ch
    while s not in prefixes:
        s = s[1:]
    return s


def pattern_wait_automaton(pattern: str, probs: dict[str, Fraction]) -> Fraction:
    """Expected trials until pattern appears: first-step equations on the suffix-prefix automaton."""
    prefixes = {pattern[:k] for k in range(len(pattern) + 1)}
    states = [pattern[:k] for k in range(len(pattern))]
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    a = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    b = [Fraction(1)] * n
    for s in states:
        for ch, p in probs.items():
            t = next_state(s, ch, prefixes)
            if t != pattern:
                a[idx[s]][idx[t]] -= p
    return solve_exact(a, b)[idx[""]]


def pattern_wait_casino(pattern: str, probs: dict[str, Fraction]) -> Fraction:
    total = Fraction(0)
    for k in range(1, len(pattern) + 1):
        if pattern[:k] == pattern[-k:]:
            total += 1 / math.prod(probs[c] for c in pattern[:k])
    return total


def race(patterns: list[str], probs: dict[str, Fraction]) -> list[Fraction]:
    """Probability each pattern appears first: exact solve on the joint automaton."""
    prefixes = {p[:k] for p in patterns for k in range(len(p) + 1)}
    states = sorted(s for s in prefixes if s not in patterns)
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    out = []
    for target in patterns:
        a = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
        b = [Fraction(0)] * n
        for s in states:
            for ch, p in probs.items():
                t = next_state(s, ch, prefixes)
                done = next((q for q in patterns if t.endswith(q)), None)
                if done is not None:
                    b[idx[s]] += p * int(done == target)
                else:
                    a[idx[s]][idx[t]] -= p
        out.append(solve_exact(a, b)[idx[""]])
    return out


def simulate_race(patterns: list[str], n_games: int) -> np.ndarray:
    wins = np.zeros(len(patterns))
    flips = RNG.random((n_games, 200)) < 0.5
    for g in range(n_games):
        s = ""
        for f in flips[g]:
            s = (s + ("H" if f else "T"))[-3:]
            hit = [i for i, q in enumerate(patterns) if s.endswith(q)]
            if hit:
                wins[hit[0]] += 1
                break
    return wins / n_games


COIN = {"H": Fraction(1, 2), "T": Fraction(1, 2)}
DIE = {str(k): Fraction(1, 6) for k in range(1, 7)}


def two_state() -> None:
    print("Worked example: two-state regime model (a = 0.1, b = 0.3 are inputs)")
    a, b = Fraction(1, 10), Fraction(3, 10)
    p = [[1 - a, a], [b, 1 - b]]
    # Solve pi (P - I) = 0 with pi_C + pi_V = 1.
    pi = solve_exact([[p[0][0] - 1, p[1][0]], [Fraction(1), Fraction(1)]], [Fraction(0), Fraction(1)])
    exact("pi_C", pi[0], Fraction(3, 4))
    exact("pi_V", pi[1], Fraction(1, 4))
    assert pi == [b / (a + b), a / (a + b)]
    # Return time to C by first-step: k_V = 1 + (1-b) k_V, m_C = 1 + a k_V; does not use pi.
    k_v = solve_exact([[1 - p[1][1]]], [Fraction(1)])[0]
    m_c = 1 + a * k_v
    exact("mean return time to calm (first-step)", m_c, Fraction(4, 3))
    assert m_c == 1 / pi[0]
    quoted("mean volatile spell 1/b (days)", float(k_v), 3.3, 1)
    ev = sorted(np.linalg.eigvals(np.array(p, dtype=float)).real)
    quoted("second eigenvalue 1 - a - b", ev[0], 0.6, 12)
    quoted("half-life ln 2 / -ln 0.6 (days)", math.log(2) / -math.log(ev[0]), 1.4, 1)
    pn = np.linalg.matrix_power(np.array(p, dtype=float), 20)
    assert abs(pn[1, 0] - 0.75) < 0.6**20, "P^n converges to pi at rate 0.6^n"


def pattern_waits() -> None:
    print("Pattern waiting times: automaton solve versus casino closed form")
    cases = [
        ("66", DIE, 42, "card prob-mc-double-six-waiting"),
        ("12", DIE, 36, "card prob-mc-one-then-two-waiting"),
        ("HHH", COIN, 14, "card prob-mc-hhh-waiting"),
        ("HHT", COIN, 8, "Penney example"),
        ("HTT", COIN, 8, "Penney example"),
    ]
    for pat, probs, want, where in cases:
        auto = pattern_wait_automaton(pat, probs)
        exact(f"E[wait for {pat}] ({where})", auto, Fraction(want))
        assert auto == pattern_wait_casino(pat, probs)
    exact("prefix-suffix rule for 66: 6 + 36", Fraction(6 + 36), pattern_wait_automaton("66", DIE))
    for n in range(1, 8):
        assert pattern_wait_automaton("H" * n, COIN) == 2 ** (n + 1) - 2
    print("    n heads in a row = 2^(n+1) - 2 for n = 1..7")
    # Hand derivation of 66: E0 = 1 + 5/6 E0 + 1/6 E1, E1 = 1 + 5/6 E0.
    e = solve_exact([[Fraction(1, 6), Fraction(-1, 6)], [Fraction(-5, 6), Fraction(1)]], [Fraction(1), Fraction(1)])
    exact("E_0 from the two first-step equations", e[0], Fraction(42))


def penney() -> None:
    print("Penney races: exact joint-automaton solve and simulation")
    hht, htt = race(["HHT", "HTT"], COIN)
    exact("P(HHT before HTT) (card prob-mc-penney-hht-vs-htt)", hht, Fraction(2, 3))
    assert hht + htt == 1
    thh, hhh = race(["THH", "HHH"], COIN)
    exact("P(THH before HHH) (card prob-mc-penney-thh-vs-hhh)", thh, Fraction(7, 8))
    sim = simulate_race(["HHT", "HTT"], 40_000)
    se = math.sqrt(2 / 9 / 40_000)
    assert abs(sim[0] - 2 / 3) <= 5 * se, sim
    print(f"    simulated P(HHT before HTT) = {sim[0]:.4f} (se {se:.4f})")
    # Hand equations: a_H = 1/2 + 1/2 a_HT, a_HT = 1/2 a_H.
    a = solve_exact([[Fraction(1), Fraction(-1, 2)], [Fraction(-1, 2), Fraction(1)]], [Fraction(1, 2), Fraction(0)])
    exact("a_H from the hand equations", a[0], Fraction(2, 3))


def return_time_by_first_step(adj: list[list[int]], start: int) -> float:
    """E_start[T_start^+] from first-step hitting times to start (does not use the stationary law)."""
    n = len(adj)
    others = [v for v in range(n) if v != start]
    pos = {v: i for i, v in enumerate(others)}
    a = np.eye(len(others))
    for v in others:
        for w in adj[v]:
            if w != start:
                a[pos[v], pos[w]] -= 1.0 / len(adj[v])
    k = np.linalg.solve(a, np.ones(len(others)))
    return 1.0 + sum(k[pos[w]] for w in adj[start]) / len(adj[start])


def board_graph(moves: list[tuple[int, int]]) -> list[list[int]]:
    adj = []
    for r in range(8):
        for c in range(8):
            adj.append([8 * (r + dr) + c + dc for dr, dc in moves if 0 <= r + dr < 8 and 0 <= c + dc < 8])
    return adj


def random_walk_returns() -> None:
    print("Worked example and cards: return times by first-step solves on the board")
    knight = board_graph([(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)])
    deg = sum(len(x) for x in knight)
    exact("knight degree sum", deg, 336)
    exact("knight edges", deg // 2, 168)
    exact("knight corner degree", len(knight[0]), 2)
    quoted("knight return time to a corner (card prob-mc-knight-corner-return)", return_time_by_first_step(knight, 0), 168, 9)
    king = board_graph([(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr, dc) != (0, 0)])
    degs = [len(x) for x in king]
    exact("king degree sum", sum(degs), 420)
    exact("king degree counts (3, 5, 8)", (degs.count(3), degs.count(5), degs.count(8)), (4, 24, 36))
    quoted("king return time to a corner (card prob-mc-king-corner-return)", return_time_by_first_step(king, 0), 140, 9)
    clock = [[(v - 1) % 12, (v + 1) % 12] for v in range(12)]
    quoted("clock frog return time to 12 (card prob-mc-clock-frog-return)", return_time_by_first_step(clock, 0), 12, 9)


def cycle_cover(n: int) -> tuple[list[Fraction], Fraction]:
    """Exact P(vertex k is last visited) and E[cover time] for the walk on an n-cycle from 0.

    State: (l, r, x) with visited arc {-l, ..., r} and position x in it; the walk is absorbed when the arc covers n - 1
    vertices and steps onto the last one. Solved by first-step equations in exact rationals.
    """
    states = [(lft, r, x) for lft in range(n) for r in range(n) if lft + r <= n - 2 for x in range(-lft, r + 1)]
    idx = {s: i for i, s in enumerate(states)}
    m = len(states)
    half = Fraction(1, 2)
    probs = []
    for k in range(1, n):
        a = [[Fraction(int(i == j)) for j in range(m)] for i in range(m)]
        b = [Fraction(0)] * m
        for lft, r, x in states:
            i = idx[(lft, r, x)]
            for y in (x - 1, x + 1):
                nl, nr = max(lft, -y), max(r, y)
                if nl + nr == n - 1:
                    b[i] += half * int(y % n == k)
                else:
                    a[i][idx[(nl, nr, y)]] -= half
        probs.append(solve_exact(a, b)[idx[(0, 0, 0)]])
    a = [[Fraction(int(i == j)) for j in range(m)] for i in range(m)]
    b = [Fraction(1)] * m
    for lft, r, x in states:
        for y in (x - 1, x + 1):
            nl, nr = max(lft, -y), max(r, y)
            if nl + nr != n - 1:
                a[idx[(lft, r, x)]][idx[(nl, nr, y)]] -= half
    return probs, solve_exact(a, b)[idx[(0, 0, 0)]]


def cycle_last_vertex() -> None:
    print("Worked example: random walk on a cycle")
    for n in (5, 6, 7):
        probs, cover = cycle_cover(n)
        assert all(p == Fraction(1, n - 1) for p in probs), probs
        assert cover == Fraction(n * (n - 1), 2)
        print(f"    n = {n}: every vertex last with probability 1/{n - 1}; cover time {cover}")
    _, cover6 = cycle_cover(6)
    exact("hexagon cover time (n(n-1)/2)", cover6, Fraction(15))


def doubly_stochastic_and_lazy() -> None:
    print("Cards: doubly stochastic chains and the lazy bipartite walk")
    p = np.array([[0.2, 0.5, 0.3], [0.3, 0.2, 0.5], [0.5, 0.3, 0.2]])
    w, v = np.linalg.eig(p.T)
    pi = np.real(v[:, np.argmin(np.abs(w - 1))])
    pi /= pi.sum()
    assert np.allclose(pi, 1 / 3), pi
    print("    doubly stochastic 3x3 example: stationary law is uniform")
    cyc = np.zeros((4, 4))
    for v_ in range(4):
        cyc[v_, (v_ + 1) % 4] = cyc[v_, (v_ - 1) % 4] = 0.5
    p50, p51 = np.linalg.matrix_power(cyc, 50), np.linalg.matrix_power(cyc, 51)
    assert p50[0, 1] == 0 and p51[0, 0] == 0, "period 2: P^n alternates"
    lazy = np.linalg.matrix_power((np.eye(4) + cyc) / 2, 200)
    assert np.allclose(lazy, 0.25), "lazy chain converges to the same uniform law"
    print("    4-cycle: P^n alternates; the lazy chain (I + P)/2 converges to uniform")
    # Fundamental matrix on fair gambler's ruin 0..5: N 1 gives i(N - i).
    q = np.zeros((4, 4))
    for i in range(4):
        for j in (i - 1, i + 1):
            if 0 <= j < 4:
                q[i, j] = 0.5
    t = np.linalg.solve(np.eye(4) - q, np.ones(4))
    assert np.allclose(t, [i * (5 - i) for i in range(1, 5)])
    print("    fundamental matrix on fair ruin with N = 5: absorption times i(5 - i)")


if __name__ == "__main__":
    two_state()
    pattern_waits()
    penney()
    random_walk_returns()
    cycle_last_vertex()
    doubly_stochastic_and_lazy()
    print("All Markov chain checks passed.")
