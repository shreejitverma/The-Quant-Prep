"""Probability problem set: every number in the worked examples and cards, recomputed by an independent route.

Backs `01-Probability/15-Probability-Problem-Set.md`.
Finite questions are settled by brute-force enumeration of the whole sample space (dice, cards, coins, children,
revolver chambers, vote orders, permutations) in exact rationals; Markov and pattern questions by exact first-step
solves on an automaton; the airplane and prisoner puzzles by exhaustive enumeration at small n plus an exact
recursion or simulation at n = 100; continuous questions by seeded simulation or numerical integration.
Simulation tolerances are five standard errors; the seed is fixed.
Run it with `python 01-Probability/code/prob_15_problem_set.py`.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction
from statistics import NormalDist

import numpy as np

SEED = 20261019
RNG = np.random.default_rng(SEED)
N_SIM = 1_000_000
PHI = NormalDist()


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")
    return value


def exact(label: str, value: Fraction | int | tuple, expected: Fraction | int | tuple) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def sim_mean(label: str, samples: np.ndarray, target: float) -> None:
    est = float(samples.mean())
    se = float(samples.std(ddof=1)) / math.sqrt(samples.size)
    assert abs(est - target) <= 5.0 * se + 1e-12, f"{label}: simulated {est} (se {se}), target {target}"
    print(f"    {label}: simulated {est:.5g} (se {se:.2g}) vs {target:.5g}")


def simpson(f, a: float, b: float, n: int = 4000) -> float:
    h = (b - a) / n
    s = f(a) + f(b)
    s += 4.0 * sum(f(a + (2 * k - 1) * h) for k in range(1, n // 2 + 1))
    s += 2.0 * sum(f(a + 2 * k * h) for k in range(1, n // 2))
    return s * h / 3.0


def prob(events) -> Fraction:
    events = list(events)
    return Fraction(sum(events), len(events))


DECK = [(rank, suit) for rank in range(13) for suit in range(4)]  # suit 0 is hearts, rank 12 is the ace


def counting() -> None:
    print("Counting and basic probability")
    dice2 = list(itertools.product(range(1, 7), repeat=2))
    exact("at least one six in two dice (card prob-ps-at-least-one-six-two-dice)", prob(6 in d for d in dice2), Fraction(11, 36))
    dice3 = list(itertools.product(range(1, 7), repeat=3))
    sums = [sum(d) for d in dice3]
    exact("outcomes summing to 10", sums.count(10), 27)
    exact("P(sum of three dice = 10) (card prob-ps-sum-three-dice-ten)", Fraction(sums.count(10), 216), Fraction(1, 8))
    top = max(sums.count(s) for s in range(3, 19))
    exact("modal sums", tuple(s for s in range(3, 19) if sums.count(s) == top), (10, 11))
    hands3 = list(itertools.combinations(DECK, 3))
    exact("three hearts (card prob-ps-three-hearts)", prob(all(c[1] == 0 for c in h) for h in hands3), Fraction(11, 850))
    quoted("11/850", 11 / 850, 0.0129, 4)
    hands4 = itertools.combinations(DECK, 4)
    four = prob(len({c[1] for c in h}) == 4 for h in hands4)
    exact("four different suits (card prob-ps-four-different-suits)", four, Fraction(2197, 20825))
    quoted("2197/20825", float(four), 0.105, 3)
    exact("sequential form 39/51 * 26/50 * 13/49", Fraction(39, 51) * Fraction(26, 50) * Fraction(13, 49), four)
    full = 0
    total = 0
    ranks = [r for r, _ in DECK]
    for h in itertools.combinations(range(52), 5):
        a, b, c, d, e = (ranks[i] for i in h)  # sorted by card index, so ranks are non-decreasing
        total += 1
        if (a == b == c and d == e and c != d) or (a == b and c == d == e and b != c):
            full += 1
    exact("five-card hands", total, 2_598_960)
    exact("full houses", full, 3744)
    exact("P(full house) (card prob-ps-full-house)", Fraction(full, total), Fraction(6, 4165))
    quoted("6/4165", 6 / 4165, 0.00144, 5)
    p4 = prob(6 in d for d in itertools.product(range(1, 7), repeat=4))
    quoted("de Mere: at least one six in 4 rolls (card prob-ps-de-mere)", float(p4), 0.518, 3)
    p24 = 1 - (35 / 36) ** 24
    quoted("de Mere: at least one double six in 24 rolls", p24, 0.491, 3)
    rolls = RNG.integers(1, 7, size=(400_000, 24, 2))
    sim_mean("simulated double six in 24 rolls", ((rolls[:, :, 0] == 6) & (rolls[:, :, 1] == 6)).any(axis=1).astype(float), p24)
    p50 = math.comb(100, 50) / 2**100
    quoted("P(exactly 50 heads in 100) (card prob-ps-exactly-fifty-heads)", p50, 0.0796, 4)
    quoted("Stirling 1/sqrt(50 pi)", 1 / math.sqrt(50 * math.pi), 0.0798, 4)


def bayes() -> None:
    print("Conditional probability and Bayes")
    kids = list(itertools.product("BG", repeat=2))
    cond = [k for k in kids if "B" in k]
    exact("two children, at least one boy: both boys (card prob-ps-boy-girl)", prob(k == ("B", "B") for k in cond), Fraction(1, 3))
    # Monty Hall: enumerate car position, first pick, and the host's choice among allowed doors.
    win_switch = Fraction(0)
    for car in range(3):
        for pick in range(3):
            allowed = [d for d in range(3) if d not in (car, pick)]
            for opened in allowed:
                switch_to = next(d for d in range(3) if d not in (pick, opened))
                win_switch += Fraction(1, 9) * Fraction(1, len(allowed)) * (switch_to == car)
    exact("Monty Hall, P(win by switching) (card prob-ps-monty-hall)", win_switch, Fraction(2, 3))
    prev, sens, spec = Fraction(1, 100), Fraction(99, 100), Fraction(99, 100)
    tp, fp = 10_000 * prev * sens, 10_000 * (1 - prev) * (1 - spec)
    exact("true positives per 10,000", tp, Fraction(99))
    exact("false positives per 10,000", fp, Fraction(99))
    exact("P(disease | positive) (card prob-ps-disease-test-bayes)", tp / (tp + fp), Fraction(1, 2))
    joint = [(coin, seq) for coin in ("fair", "double") for seq in itertools.product("HT", repeat=3)]
    weight = {("fair", s): Fraction(1, 16) for s in itertools.product("HT", repeat=3)}
    weight.update({("double", s): Fraction(1, 2) * (s == ("H", "H", "H")) for s in itertools.product("HT", repeat=3)})
    hhh = [j for j in joint if j[1] == ("H", "H", "H")]
    post = sum(weight[j] for j in hhh if j[0] == "double") / sum(weight[j] for j in hhh)
    exact("double-headed given HHH (card prob-ps-double-headed-coin)", post, Fraction(8, 9))
    pairs = list(itertools.combinations(DECK, 2))
    aces = [p for p in pairs if any(c[0] == 12 for c in p)]
    exact("hands with at least one ace", len(aces), 198)
    exact("both aces given at least one (card prob-ps-two-aces-given-one)", prob(all(c[0] == 12 for c in p) for p in aces), Fraction(1, 33))
    spade = [p for p in pairs if (12, 3) in p]
    exact("both aces given the ace of spades", prob(all(c[0] == 12 for c in p) for p in spade), Fraction(1, 17))
    # Revolver: chambers 0 and 1 loaded, cylinder advances by one.
    empty_first = [s for s in range(6) if s not in (0, 1)]
    exact("fire again, survive (card prob-ps-revolver-spin)", prob((s + 1) % 6 not in (0, 1) for s in empty_first), Fraction(3, 4))
    exact("spin again, survive", Fraction(4, 6), Fraction(2, 3))
    k, n = 3, 5
    num = simpson(lambda p: p ** (k + 1) * (1 - p) ** (n - k), 0.0, 1.0)
    den = simpson(lambda p: p**k * (1 - p) ** (n - k), 0.0, 1.0)
    quoted("Laplace rule, k = 3 of n = 5, by integrating the posterior (card prob-ps-laplace-rule)", num / den, (k + 1) / (n + 2), 10)
    types = list(itertools.product("BG", range(7)))  # day 1 is Tuesday
    fam = list(itertools.product(types, repeat=2))
    exact("ordered (sex, day) pairs", len(fam), 196)
    tue = [f for f in fam if ("B", 1) in f]
    exact("pairs with a Tuesday boy", len(tue), 27)
    exact("of which both boys", sum(f[0][0] == f[1][0] == "B" for f in tue), 13)
    exact("P(both boys | a Tuesday boy) (card prob-ps-tuesday-boy)", prob(f[0][0] == f[1][0] == "B" for f in tue), Fraction(13, 27))
    # Protocol caveat: the parent describes a uniformly chosen child, and it happens to be a Tuesday boy.
    num = sum(Fraction(1, 196) * Fraction(1, 2) * (f[i] == ("B", 1)) * (f[0][0] == f[1][0] == "B") for f in fam for i in (0, 1))
    den = sum(Fraction(1, 196) * Fraction(1, 2) * (f[i] == ("B", 1)) for f in fam for i in (0, 1))
    exact("volunteered description of a random child", num / den, Fraction(1, 2))


def expectation() -> None:
    print("Expectation and linearity")
    faces = range(1, 7)
    e2 = Fraction(sum(f * f for f in faces), 6)
    exact("E[X^2] for a die (card prob-ps-die-squared)", e2, Fraction(91, 6))
    quoted("91/6", float(e2), 15.17, 2)
    var1 = e2 - Fraction(7, 2) ** 2
    exact("variance of a die", var1, Fraction(35, 12))
    exact("variance of 100 dice (card prob-ps-variance-hundred-dice)", 100 * var1, Fraction(3500, 12))
    quoted("3500/12", float(100 * var1), 291.7, 1)
    quoted("sd of 100 dice", math.sqrt(100 * var1), 17.1, 1)
    flips = RNG.random((400_000, 60)) < 0.5
    differs = flips[:, 1:] != flips[:, :1]
    assert differs.any(axis=1).all()
    sim_mean("flips until both faces (card prob-ps-flips-until-both-faces)", (differs.argmax(axis=1) + 2).astype(float), 3.0)
    seqs = list(itertools.product((0, 1), repeat=10))
    runs = Fraction(sum(1 + sum(s[i] != s[i + 1] for i in range(9)) for s in seqs), len(seqs))
    exact("expected runs in 10 flips (card prob-ps-expected-runs)", runs, Fraction(11, 2))
    # Red-then-black pairs: exact DP over (reds left, blacks left, last colour).
    memo: dict[tuple[int, int, int], Fraction] = {}

    def rb(r: int, b: int, last: int) -> Fraction:
        if r + b == 0:
            return Fraction(0)
        key = (r, b, last)
        if key not in memo:
            val = Fraction(0)
            if r:
                val += Fraction(r, r + b) * rb(r - 1, b, 1)
            if b:
                val += Fraction(b, r + b) * (int(last == 1) + rb(r, b - 1, 0))
            memo[key] = val
        return memo[key]

    exact("red immediately followed by black, by DP (card prob-ps-deck-red-then-black)", rb(26, 26, 0), Fraction(13))
    total = 0
    for s in itertools.product(range(6), repeat=7):
        seen = set()
        for i, f in enumerate(s):
            if f in seen:
                total += i + 1
                break
            seen.add(f)
    exact(
        "rolls until a repeat, by enumerating 6^7 sequences (card prob-ps-rolls-until-repeat-face)",
        Fraction(total, 6**7),
        Fraction(1223, 324),
    )
    quoted("1223/324", 1223 / 324, 3.77, 2)
    p = 0.3
    coin = RNG.random((200_000, 200)) < p
    pairs = coin[:, 0::2] != coin[:, 1::2]
    assert pairs.any(axis=1).all()
    sim_mean(
        "von Neumann flips at p = 0.3: 1/(pq) (card prob-ps-von-neumann-fair-coin)", 2.0 * (pairs.argmax(axis=1) + 1), 1 / (p * (1 - p))
    )
    out = coin[np.arange(coin.shape[0]), 2 * pairs.argmax(axis=1)]
    sim_mean("von Neumann output is fair", out.astype(float), 0.5)


def continuous() -> None:
    print("Continuous distributions and geometry")
    u = RNG.random((N_SIM, 3))
    quoted("1 - 0.9^3 (card prob-ps-max-three-uniforms-tail)", 1 - 0.9**3, 0.271, 3)
    sim_mean("simulated P(max of 3 > 0.9)", (u.max(axis=1) > 0.9).astype(float), 0.271)
    sim_mean("P(X + Y > 1.5) (card prob-ps-sum-two-uniforms-tail)", (u[:, 0] + u[:, 1] > 1.5).astype(float), 1 / 8)
    life = RNG.exponential(3.0, N_SIM)
    sim_mean("residual life given > 2 (card prob-ps-exponential-remaining-life)", life[life > 2] - 2, 3.0)
    cut = u[:, 0]
    sim_mean("piece containing the midpoint (card prob-ps-piece-containing-midpoint)", np.maximum(cut, 1 - cut), 0.75)
    x, y = RNG.standard_normal(N_SIM), RNG.standard_normal(N_SIM)
    corr = np.corrcoef(x, x + y)[0, 1]
    assert abs(corr - 1 / math.sqrt(2)) < 0.003, corr
    print(f"    corr(X, X + Y) simulated {corr:.4f} vs 1/sqrt 2 = {1 / math.sqrt(2):.4f} (card prob-ps-correlation-x-and-sum)")
    half = simpson(lambda z: z * math.exp(-z * z / 2) / math.sqrt(2 * math.pi), 0.0, 12.0) / 0.5
    quoted("E[Z | Z > 0] by integration (card prob-ps-half-normal-mean)", half, math.sqrt(2 / math.pi), 10)
    quoted("sqrt(2/pi)", math.sqrt(2 / math.pi), 0.798, 3)
    emax = simpson(lambda z: 2 * z * PHI.pdf(z) * PHI.cdf(z), -12.0, 12.0)
    quoted("E[max(Z1, Z2)] by integrating the density 2 phi Phi (card prob-ps-max-two-normals)", emax, 1 / math.sqrt(math.pi), 10)
    quoted("1/sqrt(pi)", 1 / math.sqrt(math.pi), 0.564, 3)
    sim_mean("P(X > Y + Z) for uniforms", (u[:, 0] > u[:, 1] + u[:, 2]).astype(float), 1 / 6)
    srt = np.sort(u, axis=1)
    tri = (srt[:, 2] < srt[:, 0] + srt[:, 1]).astype(float)
    sim_mean("three uniform lengths form a triangle (card prob-ps-three-uniform-lengths-triangle)", tri, 0.5)
    for rho, want in ((0.5, Fraction(1, 3)), (0.0, Fraction(1, 4))):
        z1, z2 = RNG.standard_normal(N_SIM), RNG.standard_normal(N_SIM)
        yy = rho * z1 + math.sqrt(1 - rho * rho) * z2
        formula = 0.25 + math.asin(rho) / (2 * math.pi)
        quoted(f"1/4 + arcsin({rho})/(2 pi)", formula, float(want), 12)
        sim_mean(
            f"simulated orthant probability, rho = {rho} (card prob-ps-bivariate-orthant)", ((z1 > 0) & (yy > 0)).astype(float), formula
        )
    quoted("rho = 1 limit", 0.25 + math.asin(1.0) / (2 * math.pi), 0.5, 12)
    quoted("rho = -1 limit", 0.25 + math.asin(-1.0) / (2 * math.pi), 0.0, 12)


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


def race(patterns: list[str]) -> Fraction:
    """P(first pattern appears before the others) for a fair coin, by an exact automaton solve."""
    prefixes = {p[:k] for p in patterns for k in range(len(p) + 1)}
    states = sorted(s for s in prefixes if s not in patterns)
    idx = {s: i for i, s in enumerate(states)}
    a = [[Fraction(int(i == j)) for j in range(len(states))] for i in range(len(states))]
    b = [Fraction(0)] * len(states)
    for s in states:
        for ch in "HT":
            t = s + ch
            while t not in prefixes:
                t = t[1:]
            done = next((q for q in patterns if t.endswith(q)), None)
            if done is None:
                a[idx[s]][idx[t]] -= Fraction(1, 2)
            else:
                b[idx[s]] += Fraction(1, 2) * (done == patterns[0])
    return solve_exact(a, b)[idx[""]]


def wait_for(pattern: str) -> Fraction:
    prefixes = {pattern[:k] for k in range(len(pattern) + 1)}
    states = [pattern[:k] for k in range(len(pattern))]
    idx = {s: i for i, s in enumerate(states)}
    a = [[Fraction(int(i == j)) for j in range(len(states))] for i in range(len(states))]
    for s in states:
        for ch in "HT":
            t = s + ch
            while t not in prefixes:
                t = t[1:]
            if t != pattern:
                a[idx[s]][idx[t]] -= Fraction(1, 2)
    return solve_exact(a, [Fraction(1)] * len(states))[0]


def chains() -> None:
    print("Markov chains, random walks and martingales")
    p_alt = sum((Fraction(1, 2) * Fraction(1, 4) ** k for k in range(200)), Fraction(0))
    assert abs(p_alt - Fraction(2, 3)) < Fraction(1, 4**199)
    exact(
        "alternating first head, from p = 1/2 + p/4 (card prob-ps-alternating-first-head)",
        solve_exact([[Fraction(3, 4)]], [Fraction(1, 2)])[0],
        Fraction(2, 3),
    )
    print("    series sum over A's turns agrees to 4^-199")
    exact(
        "first six, from p = 1/6 + (5/6)^2 p (card prob-ps-first-to-roll-six)",
        solve_exact([[1 - Fraction(25, 36)]], [Fraction(1, 6)])[0],
        Fraction(6, 11),
    )
    sixes = RNG.integers(1, 7, size=(400_000, 200)) == 6
    assert sixes.any(axis=1).all()
    sim_mean("simulated P(A wins the six race)", (sixes.argmax(axis=1) % 2 == 0).astype(float), 6 / 11)
    walks = list(itertools.product((-1, 1), repeat=4))
    exact("fair walk at 0 after 4 steps (card prob-ps-walk-returns-at-four)", prob(sum(w) == 0 for w in walks), Fraction(3, 8))
    n_top, start = 10, 3
    idx = range(1, n_top)
    mat = [[Fraction(int(i == j)) - Fraction(1, 2) * int(abs(i - j) == 1) for j in idx] for i in idx]
    h = solve_exact(mat, [Fraction(0)] * (n_top - 2) + [Fraction(1, 2)])
    d = solve_exact(mat, [Fraction(1)] * (n_top - 1))
    exact("fair walk from 3: P(hit 10) (card prob-ps-fair-walk-exit-time)", h[start - 1], Fraction(3, 10))
    exact("fair walk from 3: expected duration", d[start - 1], Fraction(21))
    p, q = Fraction(3, 5), Fraction(2, 5)
    mat = [[Fraction(int(i == j)) - (p if j == i + 1 else q if j == i - 1 else 0) for j in range(1, 4)] for i in range(1, 4)]
    h = solve_exact(mat, [Fraction(0), Fraction(0), p])
    exact("p = 0.6: hit +2 before -2 from 0 (card prob-ps-biased-walk-plus-two)", h[1], Fraction(9, 13))
    exact("1/(1 + r^2) with r = 2/3", 1 / (1 + (q / p) ** 2), h[1])
    exact("P(HTH before HHT) (card prob-ps-hth-before-hht)", race(["HTH", "HHT"]), Fraction(1, 3))
    a = solve_exact([[Fraction(1), Fraction(-1, 2)], [Fraction(-1, 2), Fraction(1)]], [Fraction(0), Fraction(1, 2)])
    exact("a_H from the card's equations a_H = a_HT/2, a_HT = 1/2 + a_H/2", a[0], Fraction(1, 3))
    exact("E[wait for HTHH] (card prob-ps-expected-hthh-waiting)", wait_for("HTHH"), Fraction(18))
    exact("casino: 16 + 2", Fraction(16 + 2), wait_for("HTHH"))


def poisson() -> None:
    print("Poisson processes")
    t = np.cumsum(RNG.exponential(0.5, size=(N_SIM, 20)), axis=1)  # rate 2
    n1 = (t <= 1.0).sum(axis=1)
    two = n1 == 2
    sim_mean("given 2 events in [0, 1], both before 1/2 (card prob-ps-poisson-both-in-first-half)", (t[two, 1] < 0.5).astype(float), 0.25)
    p3 = math.exp(-2) * 2**3 / 6
    quoted("P(3 trades), rate 2 per minute (card prob-ps-poisson-three-events)", p3, 0.180, 3)
    sim_mean("simulated P(N(1) = 3)", (n1 == 3).astype(float), p3)
    quoted("e^-5 (card prob-ps-poisson-quiet-period)", math.exp(-5), 0.0067, 4)
    sim_mean("simulated P(Exp(10) > 0.5)", (RNG.exponential(0.1, N_SIM) > 0.5).astype(float), math.exp(-5))


def airplane_exact(n: int) -> list[Fraction]:
    """P(passenger k gets own seat), k = 1..n, by exhaustive enumeration of every random choice."""
    out = [Fraction(0)] * n

    def board(k: int, free: frozenset[int], p: Fraction) -> None:
        if k == n:
            return
        if k > 0 and k in free:
            out[k] += p
            board(k + 1, free - {k}, p)
            return
        for s in free:
            if s == k:
                out[k] += p / len(free)
            board(k + 1, free - {s}, p / len(free))

    board(0, frozenset(range(n)), Fraction(1))
    return out


def airplane_recursion(n: int) -> Fraction:
    """P(last passenger gets her seat): passenger 1 picks seat 1 (done), seat n (lost) or seat k (size n-k+1)."""
    f = {2: Fraction(1, 2)}
    for m in range(3, n + 1):
        f[m] = Fraction(1, m) + sum((Fraction(1, m) * f[m - k + 1] for k in range(2, m)), Fraction(0))
    return f[n]


def hard_classics() -> None:
    print("Hard classics")
    for n in range(1, 11):
        a_heads = [math.comb(n + 1, i) for i in range(n + 2)]
        b_heads = [math.comb(n, j) for j in range(n + 1)]
        more = sum(a_heads[i] * b_heads[j] for i in range(n + 2) for j in range(n + 1) if i > j)
        assert Fraction(more, 2 ** (2 * n + 1)) == Fraction(1, 2)
    print("    A with n+1 coins beats B with n: exactly 1/2 for n = 1..10 (card prob-ps-n-plus-one-coins)")
    num = sum((n * Fraction(1, 3) ** (n - 1) * Fraction(1, 6) for n in range(1, 120)), Fraction(0))
    den = sum((Fraction(1, 3) ** (n - 1) * Fraction(1, 6) for n in range(1, 120)), Fraction(0))
    assert abs(num / den - Fraction(3, 2)) < Fraction(1, 10**50)
    print("    rolls until six given all even: series gives 3/2 to 1e-50 (card prob-ps-rolls-until-six-given-even)")
    rolls = RNG.integers(1, 7, size=(200_000, 200))
    is_six = rolls == 6
    assert is_six.any(axis=1).all()
    six = is_six.argmax(axis=1)
    before = np.arange(rolls.shape[1])[None, :] < six[:, None]
    all_even = ~((rolls % 2 == 1) & before).any(axis=1)
    sim_mean("simulated rolls given all even", (six[all_even] + 1).astype(float), 1.5)
    for n in range(2, 9):
        probs = airplane_exact(n)
        assert probs[-1] == Fraction(1, 2), (n, probs)
        assert all(probs[k - 1] == Fraction(n - k + 1, n - k + 2) for k in range(2, n + 1))
    print("    airplane: last passenger 1/2 and passenger k (n-k+1)/(n-k+2), every n = 2..8 by enumeration")
    exact("airplane, n = 100, by recursion (card prob-ps-airplane-seat)", airplane_recursion(100), Fraction(1, 2))
    for n in (6, 8):
        fail = Fraction(0)
        perms = list(itertools.permutations(range(n)))
        for perm in perms:
            seen, longest = [False] * n, 0
            for i in range(n):
                length, j = 0, i
                while not seen[j]:
                    seen[j] = True
                    j = perm[j]
                    length += 1
                longest = max(longest, length)
            fail += longest > n // 2
        h = sum((Fraction(1, k) for k in range(n // 2 + 1, n + 1)), Fraction(0))
        assert Fraction(fail, len(perms)) == h, n
    print("    prisoners: P(longest cycle > n/2) = sum_{k > n/2} 1/k by enumeration, n = 6 and 8")
    fail100 = sum((Fraction(1, k) for k in range(51, 101)), Fraction(0))
    quoted("H_100 - H_50", float(fail100), 0.688, 3)
    quoted("prisoners success (card prob-ps-hundred-prisoners)", float(1 - fail100), 0.312, 3)
    quoted("1 - ln 2", 1 - math.log(2), 0.307, 3)
    perms = np.argsort(RNG.random((20_000, 100)), axis=1)
    longest = np.zeros(perms.shape[0], dtype=int)
    own = np.zeros(perms.shape[0], dtype=int)
    for r in range(perms.shape[0]):
        perm, seen = perms[r], np.zeros(100, dtype=bool)
        for i in range(100):
            if seen[i]:
                continue
            length, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                length += 1
            longest[r] = max(longest[r], length)
            if i == 0:
                own[r] = length
    sim_mean("simulated prisoner success", (longest <= 50).astype(float), float(1 - fail100))
    sim_mean("one prisoner alone succeeds", (own <= 50).astype(float), 0.5)
    u = RNG.random((N_SIM, 14))
    dec = np.diff(u, axis=1) < 0
    assert dec.any(axis=1).all()
    sim_mean("uniforms until the first decrease (card prob-ps-uniforms-first-decrease)", (dec.argmax(axis=1) + 2).astype(float), math.e)
    z = RNG.standard_normal((400_000, 4, 3))
    pts = z / np.linalg.norm(z, axis=2, keepdims=True)
    a = np.concatenate([np.transpose(pts, (0, 2, 1)), np.ones((pts.shape[0], 1, 4))], axis=1)
    rhs = np.zeros((pts.shape[0], 4, 1))
    rhs[:, 3, 0] = 1.0
    lam = np.linalg.solve(a, rhs)[:, :, 0]
    sim_mean("tetrahedron contains the centre (card prob-ps-sphere-four-points)", np.all(lam > 0, axis=1).astype(float), 1 / 8)
    sq = RNG.random((N_SIM, 2)) - 0.5
    closer = (np.hypot(sq[:, 0], sq[:, 1]) < 0.5 - np.abs(sq).max(axis=1)).astype(float)
    target = (4 * math.sqrt(2) - 5) / 3
    quoted("(4 sqrt 2 - 5)/3 (card prob-ps-closer-to-centre)", target, 0.219, 3)
    sim_mean("simulated closer to centre than to the boundary", closer, target)
    quoted("upper limit of y in the one-eighth region", (math.sqrt(2) - 1) / 2, 0.2071, 4)


if __name__ == "__main__":
    counting()
    bayes()
    expectation()
    continuous()
    chains()
    poisson()
    hard_classics()
    print("All problem set checks passed.")
