"""Sequences and numerical reasoning: every next term, difference table, growth rate and guessing value in the note.

Backs every number in `13-Interview-Playbook/06-Sequences-and-Numerical-Reasoning.md`.
Independent routes used here:
- each stated rule is coded as a generator and must reproduce every shown term before its next term is accepted;
- difference tables are built mechanically, and next terms from them are compared with the closed forms;
- every sequence is also extended by the unique lowest-degree polynomial through all its shown terms
  (exact Lagrange extrapolation with `fractions.Fraction`), which flags where a second defensible rule
  gives a different answer;
- circle regions are counted by Euler's formula on the chord arrangement, not by the binomial closed form;
- growth and guessing values with exact `Fraction` arithmetic, AM >= GM checked on seeded random paths.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 13-Interview-Playbook/code/interview_06_sequences.py`.
"""

from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

SEED = 20261112


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def diffs(seq: list) -> list:
    return [b - a for a, b in itertools.pairwise(seq)]


def lagrange_eval(seq: list, x: int) -> Fraction:
    """Value at x of the lowest-degree polynomial through (1, s1), ..., (n, sn)."""
    n = len(seq)
    total = Fraction(0)
    for i in range(1, n + 1):
        w = Fraction(1)
        for j in range(1, n + 1):
            if j != i:
                w *= Fraction(x - j, i - j)
        total += w * Fraction(seq[i - 1])
    return total


def poly_next(seq: list) -> Fraction:
    """Next term of the lowest-degree polynomial through the shown terms, by exact Lagrange extrapolation."""
    return lagrange_eval(seq, len(seq) + 1)


def look_and_say(s: str) -> str:
    return "".join(f"{len(list(g))}{d}" for d, g in itertools.groupby(s))


def circle_regions(n: int) -> int:
    """Regions inside a circle cut by all chords between n points in general position, via Euler's formula.

    Vertices: n boundary points plus one interior crossing per 4 points. Edges: each chord is cut into
    (crossings on it + 1) pieces, plus n boundary arcs. Interior faces = E - V + 1.
    """
    if n == 1:
        return 1
    pts = list(range(n))
    chords = list(itertools.combinations(pts, 2))

    def crosses(c: tuple[int, int], d: tuple[int, int]) -> bool:
        a, b = c
        return len({*c, *d}) == 4 and ((a < d[0] < b) != (a < d[1] < b))

    crossings = sum(1 for c, d in itertools.combinations(chords, 2) if crosses(c, d))
    v = n + crossings
    pieces = sum(1 + sum(1 for d in chords if crosses(c, d)) for c in chords)
    e = pieces + n
    return e - v + 1


def main() -> None:
    rng = random.Random(SEED)

    print("Difference table and cubic (Core concepts, Example 1, card int-seq-cubic-third-differences)")
    seq = [2, 12, 36, 80, 150]
    d1, d2, d3 = diffs(seq), diffs(diffs(seq)), diffs(diffs(diffs(seq)))
    exact("1st differences", d1, [10, 24, 44, 70])
    exact("2nd differences", d2, [14, 20, 26])
    exact("3rd differences", d3, [6, 6])
    nd2 = d2[-1] + d3[-1]
    nd1 = d1[-1] + nd2
    exact("extend: 2nd, 1st, next", (nd2, nd1, seq[-1] + nd1), (32, 102, 252))
    exact("n^3 + n^2 for n = 1..6", [n**3 + n**2 for n in range(1, 7)], seq + [252])
    exact("n^2 (n + 1) at n = 6", 6**2 * 7, 252)
    for k in range(1, 6):
        for lead in range(1, 4):
            terms = [lead * n**k + 2 * n ** (k - 1) + 1 for n in range(1, k + 4)]
            t = terms
            for _ in range(k):
                t = diffs(t)
            assert set(t) == {lead * math.factorial(k)}, (k, lead, t)
    print("    k-th differences of a degree-k polynomial equal k! times its leading coefficient, k = 1..5")

    print("Next-term cards: each rule regenerates every shown term")
    cases = [
        ("int-seq-pronic", [2, 6, 12, 20, 30], lambda n: n * (n + 1), 42),
        ("int-seq-double-minus-one", [3, 5, 9, 17, 33], lambda n: 2**n + 1, 65),
        ("int-seq-squares-plus-one", [2, 5, 10, 17, 26], lambda n: n * n + 1, 37),
        ("int-seq-reversed-squares", [1, 4, 9, 61, 52, 63], lambda n: int(str(n * n)[::-1]), 94),
        ("int-seq-alternating-ops", [7, 10, 8, 11, 9, 12], lambda n: 7 + (n - 1) // 2 + 3 * ((n - 1) % 2), 10),
        ("int-seq-interleaved-doubling", [3, 4, 6, 8, 12, 16, 24], lambda n: (3 if n % 2 else 4) * 2 ** ((n - 1) // 2), 32),
        ("int-seq-geometric-one-point-five", [4, 6, 9, Fraction(27, 2)], lambda n: 4 * Fraction(3, 2) ** (n - 1), Fraction(81, 4)),
        ("int-seq-factorials", [1, 2, 6, 24, 120], math.factorial, 720),
    ]
    alternatives = {}
    for card, shown, rule, answer in cases:
        n = len(shown)
        assert [rule(k) for k in range(1, n + 1)] == shown, card
        exact(f"{card}: next term", rule(n + 1), answer)
        alt = poly_next(shown)
        alternatives[card] = alt
        print(f"      lowest-degree polynomial through the shown terms continues with {alt}")
    exact("3,5,9,17,33 by a(n+1) = 2a(n) - 1", 2 * 33 - 1, 65)
    exact("differences of 3,5,9,17,33", diffs([3, 5, 9, 17, 33]), [2, 4, 8, 16])
    exact("differences of 2,6,12,20,30", diffs([2, 6, 12, 20, 30]), [4, 6, 8, 10])
    exact("differences of 2,5,10,17,26", diffs([2, 5, 10, 17, 26]), [3, 5, 7, 9])
    exact("ratios of 1,2,6,24,120", [b // a for a, b in itertools.pairwise([1, 2, 6, 24, 120])], [2, 3, 4, 5])
    terms = list(itertools.accumulate(range(4), lambda s, _: look_and_say(s), initial="1"))
    exact("look-and-say terms", terms, ["1", "11", "21", "1211", "111221"])
    exact("look-and-say next", look_and_say("111221"), "312211")
    exact("1, 10, 2, 20, 3, 30 interleaved", [k if i == 0 else 10 * k for k in (1, 2, 3) for i in (0, 1)], [1, 10, 2, 20, 3, 30])
    exact("4, 6, 9, 13.5 ratios", [b / a for a, b in itertools.pairwise([4, 6, 9, 13.5])], [1.5, 1.5, 1.5])

    print("When more than one rule fits (cards int-seq-circle-regions, int-seq-geometric-or-cubic, int-seq-any-next-term)")
    exact("polynomial continuation of 3,5,9,17,33 (one 4th difference, no evidence)", alternatives["int-seq-double-minus-one"], 63)
    exact("cubic through 4, 6, 9, 13.5", alternatives["int-seq-geometric-one-point-five"], 20)
    exact("doubling continuation of 1,2,4,8,16", 2 * 16, 32)
    regions = [circle_regions(n) for n in range(1, 8)]
    exact("circle regions for n = 1..7 points, Euler's formula", regions, [1, 2, 4, 8, 16, 31, 57])
    exact("C(n,4) + C(n,2) + 1 at n = 6", math.comb(6, 4) + math.comb(6, 2) + 1, 31)
    exact("quartic through 1,2,4,8,16", poly_next([1, 2, 4, 8, 16]), 31)
    for target in (0, 17, 100):
        ext = [3, 5, 9, 17, 33, target]
        assert all(lagrange_eval(ext, x) == ext[x - 1] for x in range(1, 7))
    print("    a degree-5 polynomial fits 3, 5, 9, 17, 33 followed by any chosen sixth term")

    print("Numerical reasoning (Example 3, cards int-seq-cagr-trap, int-seq-percent-vs-points)")
    exact("yearly changes 100 -> 150 -> 120", (Fraction(150 - 100, 100), Fraction(120 - 150, 150)), (Fraction(1, 2), Fraction(-1, 5)))
    exact("arithmetic mean of +50% and -20%", (Fraction(1, 2) + Fraction(-1, 5)) / 2, Fraction(3, 20))
    cagr = math.sqrt(120 / 100) - 1
    approx("CAGR, %", 100 * cagr, 9.5, 1)
    assert (1 + cagr) ** 2 * 100 - 120 < 1e-9
    for _ in range(2000):
        rates = [rng.uniform(-0.5, 1.0) for _ in range(rng.randint(2, 10))]
        geo = math.prod(1 + r for r in rates) ** (1 / len(rates)) - 1
        assert geo <= sum(rates) / len(rates) + 1e-12
    print("    compound rate <= arithmetic mean on 2000 seeded paths")
    exact("4% -> 5% in points", 5 - 4, 1)
    exact("4% -> 5% relative", Fraction(5 - 4, 4), Fraction(1, 4))
    for a, b in ((Fraction(1, 10), Fraction(1, 20)), (Fraction(-1, 5), Fraction(1, 4))):
        A, B = Fraction(100), Fraction(40)
        assert (A * (1 + a)) / (B * (1 + b)) / (A / B) == (1 + a) / (1 + b)

    print("Guessing (Example 4, card int-seq-guessing-penalty)")

    def blind(k: int, c: Fraction) -> Fraction:
        outcomes = [Fraction(1)] + [-c] * (k - 1)  # one right option, k - 1 wrong ones, each equally likely
        return sum(outcomes) / k

    exact("5 options, -0.25 per wrong", blind(5, Fraction(1, 4)), 0)
    exact("0.2 - 0.8 x 0.25", Fraction(1, 5) - Fraction(4, 5) * Fraction(1, 4), 0)
    four = blind(4, Fraction(1, 4))
    exact("after eliminating one option", four, Fraction(1, 16))
    approx("after eliminating one option", float(four), 0.06, 2)
    exact("0.25 - 0.75 x 0.25", Fraction(1, 4) - Fraction(3, 4) * Fraction(1, 4), Fraction(1, 16))
    print("All sequence checks passed.")


if __name__ == "__main__":
    main()
