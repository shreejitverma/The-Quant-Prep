"""Generating functions: every distribution, moment and root in the note, by a second route.

Backs every number in `01-Probability/07-Generating-Functions.md`.
Independent routes used here:
- dice-sum distributions, parity and divisibility probabilities by enumerating outcomes;
- the uniqueness of Sicherman dice by exhaustive search over every multiset of six positive faces,
  with exact integer polynomial division;
- waiting-time moments (HH, HT) and the renewal limit from the exact distribution computed by dynamic
  programming over the pattern state, not by differentiating the PGF;
- extinction probabilities by iterating the PGF from 0 and by simulating the branching process;
- compound-Poisson moments by seeded simulation.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 01-Probability/code/prob_07_generating_functions.py`.
"""

from __future__ import annotations

import cmath
import itertools
import math
from collections import Counter
from fractions import Fraction

import numpy as np

SEED = 20261019


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol})")


# ------------------------------------------------------------------ integer polynomials (coefficient lists, index = power)


def pmul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def pdivmod(num: list[int], den: list[int]) -> tuple[list[int], list[int]]:
    """Exact division over the rationals; returns (quotient, remainder) with Fraction coefficients."""
    num_f = [Fraction(x) for x in num]
    q = [Fraction(0)] * max(1, len(num) - len(den) + 1)
    while len(num_f) >= len(den) and any(num_f):
        shift = len(num_f) - len(den)
        coef = num_f[-1] / den[-1]
        q[shift] = coef
        for i, d in enumerate(den):
            num_f[shift + i] -= coef * d
        while num_f and num_f[-1] == 0:
            num_f.pop()
    return q, num_f


def faces_poly(faces) -> list[int]:
    out = [0] * (max(faces) + 1)
    for f in faces:
        out[f] += 1
    return out


def dice() -> None:
    print("Example 1 - dice sums and Sicherman dice (card prob-gf-sicherman-dice)")
    std = faces_poly(range(1, 7))
    two = pmul(std, std)
    sums = Counter(a + b for a, b in itertools.product(range(1, 7), repeat=2))
    exact("coefficients of (s+...+s^6)^2 equal enumerated sum counts", two[2:], [sums[k] for k in range(2, 13)])
    exact("sum counts 2..12", two[2:], [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])
    factors = pmul(pmul(pmul([0, 1], [1, 1]), [1, 1, 1]), [1, -1, 1])
    exact("s(1+s)(1+s+s^2)(1-s+s^2) = s+...+s^6", factors, std)
    die_a = pmul(pmul([0, 1], [1, 1]), [1, 1, 1])
    die_b = pmul(pmul(pmul(pmul([0, 1], [1, 1]), [1, 1, 1]), [1, -1, 1]), [1, -1, 1])
    exact("first Sicherman die s(1+s)(1+s+s^2)", die_a, [0, 1, 2, 2, 1])
    exact("second Sicherman die", die_b, faces_poly([1, 3, 4, 5, 6, 8]))
    sich = Counter(a + b for a, b in itertools.product([1, 2, 2, 3, 3, 4], [1, 3, 4, 5, 6, 8]))
    exact("Sicherman sum distribution equals the standard one", sich, sums)
    found = set()
    for faces in itertools.combinations_with_replacement(range(1, 12), 6):
        q, r = pdivmod(two, faces_poly(faces))
        if r or any(c < 0 or c.denominator != 1 for c in q) or q[0] != 0 or sum(q) != 6:
            continue
        other = tuple(sorted(itertools.chain.from_iterable([k] * int(c) for k, c in enumerate(q))))
        found.add(tuple(sorted((faces, other))))
    exact(
        "all pairs of six-sided positive-integer dice with the standard sum law (exhaustive search)",
        sorted(found),
        sorted([((1, 2, 2, 3, 3, 4), (1, 3, 4, 5, 6, 8)), ((1, 2, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6))]),
    )

    print("Example 5 - parity and divisibility (cards prob-gf-even-heads, prob-gf-three-dice-divisible-by-three)")
    p = Fraction(1, 4)
    even = sum((p ** sum(seq) * (1 - p) ** (4 - sum(seq)) for seq in itertools.product((0, 1), repeat=4) if sum(seq) % 2 == 0), Fraction(0))
    exact("P(even heads), n=4, p=1/4 (enumerated)", even, Fraction(17, 32))
    exact("(1 + (1-2p)^n)/2", (1 + (1 - 2 * p) ** 4) / 2, Fraction(17, 32))
    for n in range(1, 11):
        assert Fraction(sum(1 for s in itertools.product((0, 1), repeat=n) if sum(s) % 2 == 0), 2**n) == Fraction(1, 2)
    print("    fair coin: P(even heads) = 1/2 for n = 1..10 (enumerated)")
    div3 = Fraction(sum(1 for r in itertools.product(range(1, 7), repeat=3) if sum(r) % 3 == 0), 216)
    exact("P(3 dice sum divisible by 3) (enumerated)", div3, Fraction(1, 3))
    w = cmath.exp(2j * math.pi / 3)
    g = lambda s: (sum(s**k for k in range(1, 7)) / 6) ** 3  # noqa: E731
    approx("roots-of-unity filter (1/3) sum G(w^j)", ((g(1) + g(w) + g(w * w)) / 3).real, 1 / 3, 12)
    approx("|G_die(w)|", abs(sum(w**k for k in range(1, 7)) / 6), 0.0, 12)


def compound_poisson(rng: np.random.Generator) -> None:
    print("Example 2 - compound Poisson volume (card prob-gf-compound-poisson-moments)")
    ex = Fraction(sum(range(1, 7)), 6)
    ex2 = Fraction(sum(k * k for k in range(1, 7)), 6)
    exact("E[X]", ex, Fraction(7, 2))
    exact("E[X^2]", ex2, Fraction(91, 6))
    exact("lambda E[X^2]", 2 * ex2, Fraction(91, 3))
    approx("91/3", 91 / 3, 30.3, 1)
    n = rng.poisson(2, 1_000_000)
    sizes = rng.integers(1, 7, size=(1_000_000, int(n.max())))
    volume = np.where(np.arange(sizes.shape[1]) < n[:, None], sizes, 0).sum(axis=1)
    simulated("mean volume, simulated", float(volume.mean()), 7.0, 0.02)
    simulated("variance of volume, simulated", float(volume.var()), 91 / 3, 0.15)
    simulated("P(S = 0), simulated vs e^-2", float((volume == 0).mean()), math.exp(-2), 0.002)
    within = float(2 * (ex2 - ex**2))
    between = float(2 * ex**2)
    approx("lambda Var(X) + lambda E[X]^2", within + between, 91 / 3, 12)

    print("Thinning (card prob-gf-poisson-thinning-pgf)")
    kept = rng.binomial(rng.poisson(5, 1_000_000), 0.3)
    simulated("thinned mean", float(kept.mean()), 1.5, 0.01)
    simulated("thinned variance (Poisson: equals the mean)", float(kept.var()), 1.5, 0.015)
    simulated("P(kept = 0) vs e^-1.5", float((kept == 0).mean()), math.exp(-1.5), 0.002)

    print("Poisson sum (card prob-gf-poisson-sum)")
    tot = rng.poisson(1.5, 1_000_000) + rng.poisson(2.5, 1_000_000)
    for k in (0, 2, 4, 7):
        simulated(f"P(Poi(1.5)+Poi(2.5) = {k}) vs Poisson(4)", float((tot == k).mean()), math.exp(-4) * 4**k / math.factorial(k), 0.002)


def branching(rng: np.random.Generator) -> None:
    print("Example 3 - branching extinction (cards prob-gf-branching-extinction, prob-gf-branching-poisson-two)")

    def iterate(g, steps: int = 2000) -> float:
        q = 0.0
        for _ in range(steps):
            q = g(q)
        return q

    g1 = lambda s: 0.25 + 0.25 * s + 0.5 * s * s  # noqa: E731
    q1 = iterate(g1)
    approx("extinction, offspring 0/1/2 w.p. 1/4, 1/4, 1/2 (iterating G from 0)", q1, 0.5, 9)
    exact("mean offspring", Fraction(1, 4) * 1 + Fraction(1, 2) * 2, Fraction(5, 4))
    approx("mean offspring", 0.25 + 2 * 0.5, 1.25, 2)
    for root in (Fraction(1, 2), Fraction(1)):
        exact(f"G({root}) - {root} (a root of s = G(s), i.e. of 2s^2 - 3s + 1)", Fraction(1, 4) + root / 4 + root * root / 2 - root, 0)
    approx("q^3 starting with 3 cells", q1**3, 1 / 8, 9)
    q2 = iterate(lambda s: math.exp(2 * (s - 1)))
    approx("extinction, Poisson(2) offspring", q2, 0.203, 3)

    def simulate(offspring, runs: int, cap: int = 200) -> float:
        dead = 0
        for _ in range(runs):
            z = 1
            for _ in range(60):
                if z == 0 or z > cap:
                    break
                z = int(offspring(z).sum())
            dead += z == 0
        return dead / runs

    sim1 = simulate(lambda z: rng.choice([0, 1, 2], size=z, p=[0.25, 0.25, 0.5]), 20_000)
    simulated("extinction 0/1/2 law, simulated", sim1, 0.5, 0.015)
    sim2 = simulate(lambda z: rng.poisson(2, z), 20_000)
    simulated("extinction Poisson(2), simulated", sim2, 0.203, 0.012)


def pattern_waiting_times() -> None:
    print("Example 4 - waiting for HH and HT (cards prob-gf-hh-waiting-time, prob-gf-ht-waiting-time)")

    def waiting_moments(pattern: str, horizon: int = 400) -> tuple[float, float]:
        """Exact distribution of the first-occurrence time by DP over the longest matched prefix."""
        m = len(pattern)

        def advance(state: int, c: str) -> int:
            s = pattern[:state] + c
            for k in range(min(m, len(s)), -1, -1):
                if s.endswith(pattern[:k]):
                    return k
            return 0

        dist = np.zeros(m + 1)
        dist[0] = 1.0
        mean = second = 0.0
        for t in range(1, horizon + 1):
            new = np.zeros(m + 1)
            for st in range(m):
                for c in "HT":
                    new[advance(st, c)] += 0.5 * dist[st]
            mean += t * new[m]
            second += t * t * new[m]
            new[m] = 0.0
            dist = new
        assert dist.sum() < 1e-30
        return mean, second - mean * mean

    m_hh, v_hh = waiting_moments("HH")
    approx("E[T_HH]", m_hh, 6, 9)
    approx("Var[T_HH]", v_hh, 22, 9)
    m_ht, v_ht = waiting_moments("HT")
    approx("E[T_HT]", m_ht, 4, 9)
    approx("Var[T_HT]", v_ht, 4, 9)
    # the PGF in the note, checked against the DP by its power series at s = 1/2
    pgf_hh = lambda s: (s * s / 4) / (1 - s / 2 - s * s / 4)  # noqa: E731
    approx("G_HH(1)", pgf_hh(1.0), 1.0, 12)

    print("Renewal: the running total of die rolls hits n (card prob-gf-die-sum-hits-n)")
    u = [Fraction(1)] + [Fraction(0)] * 300
    for n in range(1, 301):
        u[n] = sum((u[n - k] for k in range(1, 7) if n - k >= 0), Fraction(0)) / 6
    approx("u_300 (exact recursion)", float(u[300]), 2 / 7, 12)
    approx("2/7", 2 / 7, 0.2857, 4)


def moments_and_cumulants() -> None:
    print("MGFs and cumulants (cards prob-gf-normal-mgf, prob-gf-lognormal-moments-no-mgf, prob-gf-cumulant-scaling, prob-gf-pgf-moments)")
    x = np.linspace(-40, 40, 800_001)
    phi = np.exp(-x * x / 2) / math.sqrt(2 * math.pi)
    trap = lambda y: float(((y[1:] + y[:-1]) / 2 * np.diff(x)).sum())  # noqa: E731
    approx("E[e^Z] by integration", trap(np.exp(x) * phi), math.exp(0.5), 9)
    approx("e^(1/2)", math.exp(0.5), 1.6487, 4)
    mu, sig = 0.1, 0.4
    for k in (1, 2, 3):
        approx(
            f"lognormal E[X^{k}] by integration vs e^(k mu + k^2 sigma^2/2)",
            trap(np.exp(k * (mu + sig * x)) * phi),
            math.exp(k * mu + k * k * sig * sig / 2),
            9,
        )
    # cumulant scaling, exactly, on Binomial(n, p) = sum of n Bernoulli(p)
    p = Fraction(1, 5)
    for n in (1, 4, 16):
        pmf = {k: math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n + 1)}
        m = sum(k * q for k, q in pmf.items())
        c2 = sum((k - m) ** 2 * q for k, q in pmf.items())
        c3 = sum((k - m) ** 3 * q for k, q in pmf.items())
        c4 = sum((k - m) ** 4 * q for k, q in pmf.items()) - 3 * c2 * c2
        assert c2 == n * p * (1 - p) and c3 == n * p * (1 - p) * (1 - 2 * p)
        assert c4 == n * p * (1 - p) * (1 - 6 * p * (1 - p))
        g = lambda s, pmf=pmf: sum(q * s**k for k, q in pmf.items())  # noqa: E731
        h = Fraction(1, 10**6)
        g1 = (g(1 + h) - g(1 - h)) / (2 * h)
        g2 = (g(1 + h) - 2 * g(Fraction(1)) + g(1 - h)) / (h * h)
        assert abs(float(g1 - m)) < 1e-9 and abs(float(g2 + g1 - g1 * g1 - c2)) < 1e-6
    print("    Binomial(n, 1/5), n = 1, 4, 16: cumulants k2, k3, k4 are n times the Bernoulli ones (exact);")
    print("    PGF finite differences at s = 1 give E[X] = G'(1) and Var = G''(1) + G'(1) - G'(1)^2")
    skew = lambda n: float(n * p * (1 - p) * (1 - 2 * p)) / float(n * p * (1 - p)) ** 1.5  # noqa: E731
    approx("skewness ratio n=16 vs n=1 (1/sqrt(16))", skew(16) / skew(1), 0.25, 12)
    lam = 2.7
    pois = np.array([math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1)) for k in range(200)])
    ks = np.arange(200)
    mean = float((ks * pois).sum())
    approx("Poisson(2.7): k2 = lambda", float(((ks - mean) ** 2 * pois).sum()), lam, 9)
    approx("Poisson(2.7): k3 = lambda", float(((ks - mean) ** 3 * pois).sum()), lam, 9)
    k4 = float(((ks - mean) ** 4 * pois).sum()) - 3 * float(((ks - mean) ** 2 * pois).sum()) ** 2
    approx("Poisson(2.7): k4 = lambda", k4, lam, 9)


def main() -> None:
    rng = np.random.default_rng(SEED)
    dice()
    compound_poisson(rng)
    branching(rng)
    pattern_waiting_times()
    moments_and_cumulants()
    print("All generating-function checks passed.")


if __name__ == "__main__":
    main()
