"""Counting and combinatorics: every count and probability in the note, checked by brute force.

Backs every number in `01-Probability/01-Counting-and-Combinatorics.md`.
Each closed form the note quotes is compared with an independent route: exhaustive enumeration of the
finite sample space (itertools), a memoised recursion that never uses the closed form, exact rational
arithmetic with `fractions.Fraction`, or, where the space is too large to enumerate, a seeded simulation
with a stated tolerance.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 01-Probability/code/prob_01_counting.py`.
"""

from __future__ import annotations

import itertools
import math
import random
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction
from functools import cache

SEED = 20261019


def exact(label: str, value: Fraction | int, expected: Fraction | int) -> None:
    """Assert an exact count or rational probability and print it."""
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    """Assert a value rounds to the figure the note quotes (half a unit in the last decimal)."""
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    """Assert a seeded Monte Carlo estimate lies within `tol` of the quoted value."""
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol})")


# ------------------------------------------------------------------ the four basic counts, multinomial


def basic_counts() -> None:
    print("The four basic counts (n=5, k=3), each by enumeration")
    items, k = range(5), 3
    exact("ordered with replacement n^k", sum(1 for _ in itertools.product(items, repeat=k)), 5**3)
    exact("ordered without replacement n!/(n-k)!", sum(1 for _ in itertools.permutations(items, k)), math.factorial(5) // 2)
    exact("unordered without replacement C(n,k)", sum(1 for _ in itertools.combinations(items, k)), math.comb(5, 3))
    exact("unordered with replacement C(n+k-1,k)", sum(1 for _ in itertools.combinations_with_replacement(items, k)), math.comb(7, 3))
    two_dice = Counter(tuple(sorted(r)) for r in itertools.product(range(1, 7), repeat=2))
    exact("two dice: P({1,2}) / P({1,1}) (multisets not equally likely)", Fraction(two_dice[(1, 2)], two_dice[(1, 1)]), 2)

    @cache
    def arrangements(counts: tuple[int, ...]) -> int:
        """Distinct words with the given letter counts, by choosing the first letter (no multinomial)."""
        if sum(counts) == 0:
            return 1
        return sum(arrangements(counts[:i] + (c - 1,) + counts[i + 1 :]) for i, c in enumerate(counts) if c > 0)

    letters = Counter("MISSISSIPPI")
    exact("MISSISSIPPI arrangements (recursion)", arrangements(tuple(sorted(letters.values()))), 34650)
    exact(
        "MISSISSIPPI arrangements (multinomial)",
        math.factorial(11) // (math.factorial(4) * math.factorial(4) * math.factorial(2)),
        34650,
    )

    # circular seatings of 5: permutations modulo rotation, then modulo reflection as well
    def canonical_rotation(p: tuple[int, ...]) -> tuple[int, ...]:
        return min(p[i:] + p[:i] for i in range(len(p)))

    perms = list(itertools.permutations(range(5)))
    rotations = {canonical_rotation(p) for p in perms}
    exact("circular seatings of 5 (rotations identified) = (n-1)!", len(rotations), math.factorial(4))
    bracelets = {min(canonical_rotation(p), canonical_rotation(p[::-1])) for p in perms}
    exact("circular seatings of 5 (rotations and reflections identified) = (n-1)!/2", len(bracelets), math.factorial(4) // 2)


# ------------------------------------------------------------------ stars and bars, dice sums


def stars_and_bars() -> None:
    print("Stars and bars (card prob-count-stars-bars-nonnegative)")
    nonneg = sum(1 for x in itertools.product(range(11), repeat=3) if sum(x) == 10)
    positive = sum(1 for x in itertools.product(range(1, 11), repeat=3) if sum(x) == 10)
    exact("nonnegative solutions of x1+x2+x3=10", nonneg, 66)
    exact("C(12,2)", math.comb(12, 2), 66)
    exact("positive solutions of x1+x2+x3=10", positive, 36)

    print("Example 3 - three dice summing to 10 (card prob-count-three-dice-sum-ten)")
    sums = Counter(sum(r) for r in itertools.product(range(1, 7), repeat=3))
    unbounded = sum(1 for y in itertools.product(range(8), repeat=3) if sum(y) == 7)
    over = sum(1 for y in itertools.product(range(8), repeat=3) if sum(y) == 7 and max(y) >= 6)
    exact("unbounded solutions of y1+y2+y3=7 (stars and bars C(9,2))", unbounded, 36)
    exact("solutions with some y_i >= 6 (3 * C(3,2))", over, 9)
    exact("ordered outcomes with sum 10 (enumerated)", sums[10], 27)
    exact("ordered outcomes with sum 11 (enumerated)", sums[11], 27)
    exact("P(sum = 10)", Fraction(sums[10], 6**3), Fraction(1, 8))
    exact("most likely sums are 10 and 11", sorted(s for s, c in sums.items() if c == max(sums.values())), [10, 11])


# ------------------------------------------------------------------ inclusion-exclusion, surjections, derangements


def surjections_and_derangements() -> None:
    print("Surjections of 5 balls onto 3 boxes (card prob-count-surjections-five-into-three)")
    onto = sum(1 for f in itertools.product(range(3), repeat=5) if len(set(f)) == 3)
    exact("onto functions 5 -> 3 (enumerated)", onto, 150)
    terms = [(-1) ** j * math.comb(3, j) * (3 - j) ** 5 for j in range(4)]
    exact("inclusion-exclusion terms 3^5, 3*2^5, 3*1^5", (terms[0], -terms[1], terms[2]), (243, 96, 3))
    exact("inclusion-exclusion sum", sum(terms), 150)

    def set_partitions(n: int, k: int) -> int:
        """Count restricted growth strings with exactly k blocks (each is one set partition)."""
        count = 0
        for rgs in itertools.product(range(k), repeat=n):
            if rgs[0] == 0 and all(rgs[i] <= max(rgs[:i]) + 1 for i in range(1, n)) and max(rgs) == k - 1:
                count += 1
        return count

    exact("S(5,3) by enumerating set partitions", set_partitions(5, 3), 25)
    exact("3! S(5,3)", math.factorial(3) * set_partitions(5, 3), 150)

    print("Derangements (Example 2, card prob-count-derangement-hat-check)")
    brute = {n: sum(1 for p in itertools.permutations(range(n)) if all(p[i] != i for i in range(n))) for n in range(1, 9)}
    for n, d in zip((3, 4, 5, 6), (2, 9, 44, 265), strict=True):
        exact(f"D_{n} (enumerated)", brute[n], d)
    d = {1: 0, 2: 1}
    for n in range(3, 21):
        d[n] = (n - 1) * (d[n - 1] + d[n - 2])
    for n in range(1, 9):
        assert d[n] == brute[n], f"recurrence D_{n}={d[n]} disagrees with enumeration {brute[n]}"
    print("    recurrence D_n = (n-1)(D_{n-1}+D_{n-2}) matches enumeration for n = 1..8")
    getcontext().prec = 60
    e = Decimal(1).exp()
    for n in range(1, 21):
        nearest = int((Decimal(math.factorial(n)) / e).to_integral_value())
        assert nearest == d[n], f"D_{n}={d[n]} is not the nearest integer to n!/e ({nearest})"
    print("    D_n is the nearest integer to n!/e for n = 1..20 (60-digit arithmetic)")
    p4 = Fraction(brute[4], math.factorial(4))
    exact("P(no own hat), n=4", p4, Fraction(3, 8))
    exact("D_4 / 4! = 1 - 1 + 1/2 - 1/6 + 1/24", sum(Fraction((-1) ** j, math.factorial(j)) for j in range(5)), Fraction(9, 24))
    approx("P(no own hat), n=6", brute[6] / 720, 0.368, 3)
    approx("1/e", math.exp(-1), 0.368, 3)
    approx("1/e (4 dp)", math.exp(-1), 0.3679, 4)
    approx("P(no own hat), n=5 (does not yet agree to 3 dp)", brute[5] / 120, 0.367, 3)
    for n in range(1, 8):
        fixed = Fraction(sum(sum(p[i] == i for i in range(n)) for p in itertools.permutations(range(n))), math.factorial(n))
        assert fixed == 1, f"expected fixed points for n={n} is {fixed}"
    print("    expected number of own hats = 1 exactly for n = 1..7 (enumerated)")


# ------------------------------------------------------------------ reflection, ballot, Catalan


def ballot_and_catalan() -> None:
    print("Example 4 - ballot counting (card prob-count-ballot-always-ahead)")

    def always_ahead(order: tuple[int, ...]) -> bool:
        lead = 0
        for step in order:
            lead += step
            if lead <= 0:
                return False
        return True

    def orders(a: int, b: int) -> list[tuple[int, ...]]:
        n = a + b
        out = []
        for b_positions in itertools.combinations(range(n), b):
            bs = set(b_positions)
            out.append(tuple(-1 if i in bs else 1 for i in range(n)))
        return out

    all_orders = orders(6, 4)
    good = sum(always_ahead(o) for o in all_orders)
    starts_a = [o for o in all_orders if o[0] == 1]
    exact("equally likely counting orders C(10,4)", len(all_orders), 210)
    exact("orders keeping A strictly ahead (enumerated)", good, 42)
    exact("orders starting with an A vote = C(9,5)", len(starts_a), 126)
    exact("orders starting with A that later touch 0 = C(9,6)", len(starts_a) - good, 84)
    exact("P(A strictly ahead throughout)", Fraction(good, len(all_orders)), Fraction(1, 5))
    for a in range(1, 9):
        for b in range(a):
            obs = orders(a, b)
            assert Fraction(sum(always_ahead(o) for o in obs), len(obs)) == Fraction(a - b, a + b), (a, b)
    print("    ballot theorem P = (a-b)/(a+b) holds by enumeration for all 0 <= b < a <= 8")

    print("Catalan numbers (card prob-count-catalan-parentheses)")

    def balanced(n: int) -> int:
        count = 0
        for opens in itertools.combinations(range(2 * n), n):
            s = set(opens)
            depth = 0
            for i in range(2 * n):
                depth += 1 if i in s else -1
                if depth < 0:
                    break
            else:
                count += 1
        return count

    enumerated = [balanced(n) for n in range(8)]
    exact("C_0..C_7 by enumerating parenthesis strings", enumerated, [1, 1, 2, 5, 14, 42, 132, 429])
    for n in range(8):
        assert enumerated[n] == math.comb(2 * n, n) - math.comb(2 * n, n + 1) == math.comb(2 * n, n) // (n + 1)
    print("    C_n = C(2n,n) - C(2n,n+1) = C(2n,n)/(n+1) matches enumeration for n = 0..7")
    exact("C(10,5)", math.comb(10, 5), 252)
    exact("C_5 = 252/6", Fraction(math.comb(10, 5), 6), 42)
    for n in range(7):
        assert enumerated[n + 1] == sum(enumerated[i] * enumerated[n - i] for i in range(n + 1))
    print("    C_{n+1} = sum C_i C_{n-i} matches enumeration for n = 0..6")


# ------------------------------------------------------------------ poker, bridge, decks


@cache
def _hands_by_ranks() -> dict[tuple[int, ...], int]:
    """Number of five-card hands with each sorted rank multiset (rank 0 is the ace)."""
    out = {}
    for ranks in itertools.combinations_with_replacement(range(13), 5):
        mult = Counter(ranks)
        if max(mult.values()) <= 4:
            out[ranks] = math.prod(math.comb(4, m) for m in mult.values())
    return out


def poker_and_cards() -> None:
    print("Example 1 - poker hands, by enumerating all 6188 rank multisets (cards prob-count-full-house-probability, two pair)")
    pattern_count: Counter[tuple[int, ...]] = Counter()
    for ranks, ways in _hands_by_ranks().items():
        pattern_count[tuple(sorted(Counter(ranks).values(), reverse=True))] += ways
    total = sum(pattern_count.values())
    exact("total five-card hands", total, 2598960)
    full_house = pattern_count[(3, 2)]
    two_pair = pattern_count[(2, 2, 1)]
    exact("full houses (enumerated)", full_house, 3744)
    exact("full houses = 13*4*12*6", 13 * 4 * 12 * 6, full_house)
    exact("C(13,2) pair ranks", math.comb(13, 2), 78)
    exact("two-pair hands (enumerated)", two_pair, 123552)
    exact("two pair = 78*36*44", 78 * 36 * 44, two_pair)
    exact("P(full house)", Fraction(full_house, total), Fraction(6, 4165))
    approx("P(full house) in %", 100 * full_house / total, 0.144, 3)
    approx("P(two pair) in %", 100 * two_pair / total, 4.75, 2)
    wrong = 13 * 4 * 12 * 6 // 2  # C(13,2) instead of 13*12 for the full house ranks
    assert wrong != full_house
    print("    choosing full-house ranks with C(13,2) undercounts by half")
    print("At least one ace (card prob-count-at-least-one-ace, Pitfalls)")
    no_ace = sum(c for ranks, c in _hands_by_ranks().items() if 0 not in ranks)
    with_ace = total - no_ace
    exact("hands with no ace = C(48,5) (enumerated)", no_ace, 1712304)
    exact("hands with at least one ace (enumerated)", with_ace, 886656)
    naive = math.comb(4, 1) * math.comb(51, 4)
    exact("naive C(4,1)C(51,4)", naive, 999600)
    weighted = sum(c * ranks.count(0) for ranks, c in _hands_by_ranks().items())
    exact("naive count = sum over hands of (number of aces)", weighted, naive)

    print("Example 5 - four aces one per bridge hand (card prob-count-four-aces-one-each)")
    hits = sum(1 for slots in itertools.combinations(range(52), 4) if len({s // 13 for s in slots}) == 4)
    p = Fraction(hits, math.comb(52, 4))
    exact("P(each hand one ace), enumerating all C(52,4) ace positions", p, Fraction(2197, 20825))
    exact("sequential route 39*26*13/(51*50*49)", Fraction(39 * 26 * 13, 51 * 50 * 49), p)

    def multinomial(n: int, parts: list[int]) -> int:
        out, left = 1, n
        for part in parts:
            out *= math.comb(left, part)
            left -= part
        return out

    exact("multinomial route 4! M(48;12^4)/M(52;13^4)", Fraction(24 * multinomial(48, [12] * 4), multinomial(52, [13] * 4)), p)
    approx("P(each hand one ace)", float(p), 0.1055, 4)

    print("First ace position (card prob-count-first-ace-position)")
    total_pos = sum(min(slots) + 1 for slots in itertools.combinations(range(52), 4))
    exact("E[position of first ace], enumerated", Fraction(total_pos, math.comb(52, 4)), Fraction(53, 5))
    approx("E[position of first ace]", 53 / 5, 10.6, 1)

    print("Exchangeability: P(2nd card is an ace)")
    second = Fraction(sum(1 for c1, c2 in itertools.permutations(range(52), 2) if c2 < 4), 52 * 51)
    exact("P(2nd card is an ace), enumerating ordered pairs", second, Fraction(1, 13))

    print("Round table (card prob-count-round-table-adjacent)")
    adjacent = sum(1 for a, b in itertools.permutations(range(10), 2) if (a - b) % 10 in (1, 9))
    exact("P(two given people adjacent), 10 seats", Fraction(adjacent, 90), Fraction(2, 9))
    for n in range(4, 8):
        seats = list(itertools.permutations(range(n)))
        adj = sum(1 for s in seats if (s.index(0) - s.index(1)) % n in (1, n - 1))
        assert Fraction(adj, len(seats)) == Fraction(2, n - 1)
    print("    full seat enumeration confirms 2/(n-1) for n = 4..7")


# ------------------------------------------------------------------ identities, birthdays, de Mere


def identities_birthdays_de_mere() -> None:
    print("Double counting identities (card prob-count-committee-chair-identity)")
    for n in range(13):
        subsets = list(itertools.product((0, 1), repeat=n))
        pairs = sum(sum(s) for s in subsets)  # (committee, chair) pairs: one chair per member
        assert pairs == (n * 2 ** (n - 1) if n else 0)
        for m in range(6):
            for k in range(n + m + 1):
                assert sum(math.comb(m, j) * math.comb(n, k - j) for j in range(k + 1)) == math.comb(m + n, k)
        for r in range(n + 1):
            assert sum(math.comb(i, r) for i in range(r, n + 1)) == math.comb(n + 1, r + 1)
    print("    sum k C(n,k) = n 2^(n-1) by enumerating subsets; Vandermonde and hockey stick hold for n <= 12")

    print("Birthday problem (card prob-count-birthday-twenty-three)")

    def all_distinct(n: int) -> Fraction:
        return math.prod((Fraction(365 - i, 365) for i in range(n)), start=Fraction(1))

    smallest = next(n for n in range(1, 366) if all_distinct(n) < Fraction(1, 2))
    exact("smallest group with P(shared) > 1/2", smallest, 23)
    approx("P(shared birthday), n=23", float(1 - all_distinct(23)), 0.507, 3)
    approx("P(all distinct), n=22", float(all_distinct(22)), 0.524, 3)
    approx("P(shared birthday), n=22", float(1 - all_distinct(22)), 0.476, 3)
    approx("approximation exp(-n(n-1)/730) at n=23", math.exp(-23 * 22 / 730), 0.500, 3)
    rng = random.Random(SEED)
    trials = 100_000
    shared = sum(len({rng.randrange(365) for _ in range(23)}) < 23 for _ in range(trials))
    simulated("P(shared birthday), n=23, seeded simulation", shared / trials, 0.507, 0.006)

    print("De Mere's bets (card prob-count-de-mere-bets)")
    six_in_four = Fraction(sum(1 for r in itertools.product(range(6), repeat=4) if 5 in r), 6**4)
    exact("P(at least one six in 4 rolls), enumerated", six_in_four, 1 - Fraction(5, 6) ** 4)
    approx("P(at least one six in 4 rolls)", float(six_in_four), 0.518, 3)
    double_six = 1 - Fraction(35, 36) ** 24
    approx("P(at least one double six in 24 rolls)", float(double_six), 0.491, 3)
    trials = 200_000
    hits = sum(any(rng.randrange(36) == 0 for _ in range(24)) for _ in range(trials))
    simulated("P(at least one double six in 24 rolls), seeded simulation", hits / trials, 0.491, 0.004)


def main() -> None:
    basic_counts()
    stars_and_bars()
    surjections_and_derangements()
    ballot_and_catalan()
    poker_and_cards()
    identities_birthdays_de_mere()
    print("All counting checks passed.")


if __name__ == "__main__":
    main()
