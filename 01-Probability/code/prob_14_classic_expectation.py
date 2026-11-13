"""Classic expectation problems: every number in the note, recomputed by an independent route.

Backs `01-Probability/14-Classic-Expectation-Problems.md`.
Independent routes:
- coupon collector mean and variance by inclusion-exclusion tail sums in exact rationals (not the geometric sum);
- distinct faces, hat-check moments, derangements and cycle counts by brute-force enumeration;
- birthday numbers by direct products and a tail sum, cross-checked by simulation;
- pattern waits by an exact first-step solve on the suffix-prefix automaton;
- the secretary formula against exhaustive enumeration of every arrival order for small n, then by simulation;
- dice continuation values by enumerating every threshold policy and taking the best;
- first-ace position, empty boxes and uniform-sum stopping by exact distributions, DP or simulation.
Simulation tolerances are five standard errors; the seed is fixed.
Run it with `python 01-Probability/code/prob_14_classic_expectation.py`.
"""

from __future__ import annotations

import itertools
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


def sim_mean(label: str, samples: np.ndarray, target: float) -> None:
    est = float(samples.mean())
    se = float(samples.std(ddof=1)) / math.sqrt(samples.size)
    assert abs(est - target) <= 5.0 * se + 1e-12, f"{label}: simulated {est} (se {se}), target {target}"
    print(f"    {label}: simulated {est:.5g} (se {se:.2g}) vs {target:.5g}")


def harmonic(n: int) -> Fraction:
    return sum((Fraction(1, k) for k in range(1, n + 1)), Fraction(0))


def coupon() -> None:
    print("Coupon collector, n = 6")
    n = 6
    # P(T > m) = sum_{k>=1} (-1)^(k+1) C(n,k) (1 - k/n)^m; sum m^0 and (2m+1) weights in closed form.
    e_t, e_t2 = Fraction(0), Fraction(0)
    for k in range(1, n + 1):
        sign = (-1) ** (k + 1) * math.comb(n, k)
        x = Fraction(n - k, n)
        e_t += sign / (1 - x)  # sum_m x^m
        e_t2 += sign * (2 * x / (1 - x) ** 2 + 1 / (1 - x))  # sum_m (2m + 1) x^m
    var = e_t2 - e_t**2
    exact("E[T] by inclusion-exclusion tail sums", e_t, Fraction(147, 10))
    exact("6 H_6 = 6 * 49/20", 6 * harmonic(6), e_t)
    exact("sum 1/k^2, k = 1..6", sum((Fraction(1, k * k) for k in range(1, 7)), Fraction(0)), Fraction(5369, 3600))
    exact("Var(T) by tail sums", var, Fraction(3899, 100))
    exact("n^2 sum 1/k^2 - n H_n", 36 * Fraction(5369, 3600) - 6 * harmonic(6), var)
    quoted("sd(T)", math.sqrt(var), 6.2, 1)
    quoted("n ln n", 6 * math.log(6), 10.75, 2)
    quoted("0.577 n", 0.577 * 6, 3.46, 2)
    quoted("n ln n + 0.577 n", 6 * math.log(6) + 0.577 * 6, 14.2, 1)
    rolls = RNG.integers(0, 6, size=(100_000, 150))
    seen = np.zeros((rolls.shape[0], 6), dtype=bool)
    t = np.zeros(rolls.shape[0])
    for j in range(rolls.shape[1]):
        seen[np.arange(rolls.shape[0]), rolls[:, j]] = True
        t += ~seen.all(axis=1)
    t += 1
    assert seen.all()
    sim_mean("simulated E[T] (card prob-classic-coupon-die-all-faces)", t, 14.7)
    sim_mean("simulated E[(T - 14.7)^2] (card prob-classic-coupon-variance)", (t - 14.7) ** 2, 38.99)
    distinct = Fraction(sum(len(set(s)) for s in itertools.product(range(6), repeat=6)), 6**6)
    exact("E[distinct faces in 6 rolls] by enumerating 6^6 sequences", distinct, 6 * (1 - Fraction(5, 6) ** 6))
    quoted("distinct faces (card prob-classic-distinct-faces)", float(distinct), 3.99, 2)


def birthday() -> None:
    print("Birthday problem")

    def p_distinct(k: int) -> float:
        return math.prod(1 - j / 365 for j in range(k))

    k_min = next(k for k in range(1, 100) if 1 - p_distinct(k) > 0.5)
    exact("smallest k with P(match) > 1/2 (card prob-classic-birthday-23)", k_min, 23)
    quoted("P(match) at 23", 1 - p_distinct(23), 0.507, 3)
    quoted("P(all distinct) at 23", p_distinct(23), 0.493, 3)
    exact("pairs among 23", math.comb(23, 2), 253)
    exact("expected matching pairs among 30", Fraction(math.comb(30, 2), 365), Fraction(435, 365))
    quoted("435/365 (card prob-classic-birthday-expected-pairs)", 435 / 365, 1.19, 2)
    tail = sum(p_distinct(n) for n in range(0, 367))
    quoted("expected people until the first repeat (tail sum)", tail, 24.6, 1)
    days = RNG.integers(0, 365, size=(100_000, 40))
    sim_mean("simulated P(match) among 23", np.array([len(set(r[:23])) < 23 for r in days], dtype=float), 1 - p_distinct(23))
    k_mine = next(k for k in range(1, 1000) if 1 - (364 / 365) ** k > 0.5)
    exact("others needed to share my birthday (card prob-classic-birthday-share-mine)", k_mine, 253)
    quoted("ln 2 / -ln(364/365)", math.log(2) / -math.log(364 / 365), 252.7, 1)


def hat_check() -> None:
    print("Hat check: brute force over every permutation")
    for n in range(2, 9):
        fixed = [sum(p[i] == i for i in range(n)) for p in itertools.permutations(range(n))]
        m = Fraction(sum(fixed), len(fixed))
        v = Fraction(sum(f * f for f in fixed), len(fixed)) - m * m
        assert m == 1 and v == 1, (n, m, v)
    print("    E[F] = 1 and Var(F) = 1 for n = 2..8 (cards prob-classic-hat-check-expected, -variance)")
    perms4 = list(itertools.permutations(range(4)))
    der4 = sum(all(p[i] != i for i in range(4)) for p in perms4)
    exact("derangements of 4", der4, 9)
    exact("P(no fixed point), n = 4 (card prob-classic-hat-check-none)", Fraction(der4, 24), Fraction(3, 8))
    d = [1, 0]
    for k in range(2, 11):
        d.append((k - 1) * (d[-1] + d[-2]))
    p10 = Fraction(d[10], math.factorial(10))
    incl_excl = sum((Fraction((-1) ** k, math.factorial(k)) for k in range(11)), Fraction(0))
    exact("inclusion-exclusion sum to 10 equals D_10 / 10!", incl_excl, p10)
    quoted("P(no fixed point), n = 10", float(p10), 0.36788, 5)
    assert abs(float(p10) - math.exp(-1)) < 5e-7, "agrees with 1/e to six decimals"
    quoted("1/e", math.exp(-1), 0.368, 3)
    exact("pair probability 1/90 for n = 10", Fraction(math.factorial(8), math.factorial(10)), Fraction(1, 90))
    exact("90 (1/90 - 1/100)", 90 * (Fraction(1, 90) - Fraction(1, 100)), Fraction(1, 10))
    exact("10 * (1/10)(9/10)", 10 * Fraction(1, 10) * Fraction(9, 10), Fraction(9, 10))
    for n in range(1, 8):
        cycles = 0
        for p in itertools.permutations(range(n)):
            seen = [False] * n
            for i in range(n):
                if not seen[i]:
                    cycles += 1
                    j = i
                    while not seen[j]:
                        seen[j] = True
                        j = p[j]
        assert Fraction(cycles, math.factorial(n)) == harmonic(n)
    print("    expected cycles = H_n for n = 1..7 by enumeration (card prob-classic-permutation-cycles)")


def automaton_wait(pattern: str, probs: dict[str, Fraction]) -> Fraction:
    prefixes = {pattern[:k] for k in range(len(pattern) + 1)}
    states = [pattern[:k] for k in range(len(pattern))]
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    m = [[Fraction(int(i == j)) for j in range(n)] + [Fraction(1)] for i in range(n)]
    for s in states:
        for ch, p in probs.items():
            t = s + ch
            while t not in prefixes:
                t = t[1:]
            if t != pattern:
                m[idx[s]][idx[t]] -= p
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        inv = 1 / m[col][col]
        m[col] = [v * inv for v in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [vr - f * vc for vr, vc in zip(m[r], m[col], strict=True)]
    return m[0][n]


def patterns() -> None:
    print("Pattern waiting times by exact automaton solve")
    coin = {"H": Fraction(1, 2), "T": Fraction(1, 2)}
    exact("HH (card prob-classic-hh-vs-ht)", automaton_wait("HH", coin), Fraction(6))
    exact("HT", automaton_wait("HT", coin), Fraction(4))
    for n in range(1, 8):
        assert automaton_wait("H" * n, coin) == 2 ** (n + 1) - 2
        if n > 1:
            assert automaton_wait("H" * n, coin) == 2 * automaton_wait("H" * (n - 1), coin) + 2
    print("    n heads in a row: 2^(n+1) - 2 and E_n = 2 E_(n-1) + 2 for n = 1..7 (card prob-classic-n-heads-in-a-row)")
    for p in (Fraction(1, 3), Fraction(1, 2), Fraction(3, 4)):
        biased = {"H": p, "T": 1 - p}
        assert automaton_wait("HH", biased) == (1 + p) / p**2
    third = {"H": Fraction(1, 3), "T": Fraction(2, 3)}
    exact("biased HH at p = 1/3 (card prob-classic-biased-hh)", automaton_wait("HH", third), Fraction(12))


def secretary_formula(n: int, skip: int) -> Fraction:
    r = skip + 1
    if skip == 0:
        return Fraction(1, n)
    return sum((Fraction(1, n) * Fraction(r - 1, i - 1) for i in range(r, n + 1)), Fraction(0))


def secretary_brute(n: int, skip: int) -> Fraction:
    wins = 0
    for order in itertools.permutations(range(n)):  # 0 is the best candidate
        bar = min(order[:skip]) if skip else n
        pick = next((c for c in order[skip:] if c < bar), None)
        wins += pick == 0
    return Fraction(wins, math.factorial(n))


def secretary() -> None:
    print("Secretary problem")
    for n in range(2, 9):
        for skip in range(n):
            assert secretary_brute(n, skip) == secretary_formula(n, skip), (n, skip)
    print("    formula equals exhaustive enumeration for every n = 2..8 and every skip")
    exact("n = 3, skip 1 (card prob-classic-secretary-three)", secretary_brute(3, 1), Fraction(1, 2))
    exact("n = 3, take the first", secretary_brute(3, 0), Fraction(1, 3))
    wins3 = []
    for order in itertools.permutations((1, 2, 3)):
        pick = next((c for c in order[1:] if c < order[0]), None)
        if pick == 1:
            wins3.append("".join(map(str, order)))
    exact("winning orders, rank 1 best", tuple(wins3), ("213", "231", "312"))
    for n, skip, want in ((10, 3, 0.399), (100, 37, 0.371)):
        best = max(range(n), key=lambda s, n=n: secretary_formula(n, s))
        exact(f"optimal skip for n = {n}", best, skip)
        quoted(f"P(win), n = {n}, skip {skip}", float(secretary_formula(n, skip)), want, 3)
        ranks = np.argsort(RNG.random((100_000, n)), axis=1)  # each row a random order of ranks 0..n-1
        bar = ranks[:, :skip].min(axis=1)
        later = ranks[:, skip:]
        better = later < bar[:, None]
        first = better.argmax(axis=1)
        picked = np.where(better.any(axis=1), later[np.arange(later.shape[0]), first], -1)
        sim_mean(f"simulated P(win), n = {n}, skip {skip}", (picked == 0).astype(float), float(secretary_formula(n, skip)))
    quoted("1/e (card prob-classic-secretary-rule)", math.exp(-1), 0.368, 3)
    x = np.linspace(0.01, 0.99, 9801)
    quoted("argmax of x ln(1/x)", float(x[np.argmax(-x * np.log(x))]), math.exp(-1), 4)


def dice_policies(rolls_left: int) -> Fraction:
    """Best expected value over every threshold policy, by exact enumeration of outcomes."""
    best = Fraction(0)
    for thresholds in itertools.product(range(1, 8), repeat=rolls_left - 1):
        value = Fraction(0)
        for faces in itertools.product(range(1, 7), repeat=rolls_left):
            for i, f in enumerate(faces):
                if i == rolls_left - 1 or f >= thresholds[i]:
                    value += Fraction(f, 6**rolls_left)
                    break
        best = max(best, value)
    return best


def dice() -> None:
    print("Dice with continuation: best threshold policy by exhaustive enumeration")
    v = {1: Fraction(7, 2), 2: Fraction(17, 4), 3: Fraction(14, 3), 4: Fraction(89, 18)}
    for k in (1, 2, 3, 4):
        exact(f"V_{k}", dice_policies(k), v[k])
    print("    cards prob-classic-die-two-rolls (17/4) and prob-classic-die-three-rolls (14/3)")
    quoted("V_2", float(v[2]), 4.25, 2)
    quoted("V_3", float(v[3]), 4.67, 2)
    quoted("V_4", float(v[4]), 4.94, 2)
    exact("V_3 = 11/6 + 4/6 * 17/4", Fraction(11, 6) + Fraction(4, 6) * Fraction(17, 4), v[3])
    # Pay $1 per re-roll, unlimited: value iteration in exact rationals converges to 4.
    val = Fraction(0)
    for _ in range(200):
        val = sum((max(Fraction(f), val - 1) for f in range(1, 7)), Fraction(0)) / 6
    assert abs(val - 4) < Fraction(1, 10**30)
    print(f"    pay-to-reroll value iteration: {float(val):.12f} (card prob-classic-die-pay-to-reroll)")
    for keep in (3, 4):
        first = RNG.integers(1, 7, size=(200_000, 60))
        ok = first >= keep
        idx = ok.argmax(axis=1)
        assert ok.any(axis=1).all()
        payoff = first[np.arange(first.shape[0]), idx] - idx
        sim_mean(f"simulated payoff, keep >= {keep}", payoff.astype(float), 4.0)


def uniforms_and_cards() -> None:
    print("Uniform sum, first ace and empty boxes")
    u = RNG.random((400_000, 12))
    n_sum = (np.cumsum(u, axis=1) <= 1).sum(axis=1) + 1
    sim_mean("draws until the sum exceeds 1 (card prob-classic-uniform-sum-exceeds-one)", n_sum.astype(float), math.e)
    dec = np.diff(u, axis=1) < 0
    n_dec = dec.argmax(axis=1) + 2
    assert dec.any(axis=1).all()
    sim_mean("draws until the first decrease", n_dec.astype(float), math.e)
    quoted("sum of 1/n! (n = 0..20)", sum(1 / math.factorial(k) for k in range(21)), math.e, 14)
    pos = sum((k * Fraction(math.comb(52 - k, 3), math.comb(52, 4)) for k in range(1, 50)), Fraction(0))
    exact("expected position of the first ace (card prob-classic-first-ace-position)", pos, Fraction(53, 5))
    exact("1 + 48/5", 1 + Fraction(48, 5), pos)
    # Empty boxes: DP over balls on the number of occupied boxes, exact.
    n = 10
    dist = {0: Fraction(1)}
    for _ in range(n):
        nxt: dict[int, Fraction] = {}
        for occ, p in dist.items():
            nxt[occ] = nxt.get(occ, Fraction(0)) + p * Fraction(occ, n)
            nxt[occ + 1] = nxt.get(occ + 1, Fraction(0)) + p * Fraction(n - occ, n)
        dist = nxt
    empty = sum((p * (n - occ) for occ, p in dist.items()), Fraction(0))
    exact("E[empty boxes], n = 10, by occupancy DP", empty, n * Fraction(n - 1, n) ** n)
    quoted("E[empty boxes], n = 10 (card prob-classic-empty-boxes)", float(empty), 3.49, 2)
    quoted("n/e", n / math.e, 3.68, 2)


if __name__ == "__main__":
    coupon()
    birthday()
    hat_check()
    patterns()
    secretary()
    dice()
    uniforms_and_cards()
    print("All classic expectation checks passed.")
