"""Conditional probability and Bayes: every posterior in the note, by exact enumeration and simulation.

Backs every number in `01-Probability/02-Conditional-Probability-and-Bayes.md`.
Each posterior is computed by enumerating the joint sample space of the stated protocol with exact
`fractions.Fraction` weights (never by plugging into the odds formula the note derives), and the
protocol-dependent puzzles (Monty Hall, Monty Fall, the rare-disease test) are also simulated with a
fixed seed and a stated tolerance.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 01-Probability/code/prob_02_bayes.py`.
"""

from __future__ import annotations

import itertools
import math
from collections import defaultdict
from fractions import Fraction

import numpy as np

SEED = 20261019


def exact(label: str, value: Fraction | int, expected: Fraction | int) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol})")


def posterior(joint: dict[tuple, Fraction], hypothesis, evidence) -> Fraction:
    """P(hypothesis | evidence) by summing the joint distribution over outcomes (no Bayes formula)."""
    num = sum((w for o, w in joint.items() if evidence(o) and hypothesis(o)), Fraction(0))
    den = sum((w for o, w in joint.items() if evidence(o)), Fraction(0))
    return num / den


# ------------------------------------------------------------------ Example 1: rare condition


def rare_condition(rng: np.random.Generator) -> None:
    print("Example 1 - rare condition (cards prob-bayes-rare-condition-positive-test, prob-bayes-second-positive-test)")
    prev, sens, spec = Fraction(1, 1000), Fraction(99, 100), Fraction(95, 100)
    joint: dict[tuple, Fraction] = defaultdict(Fraction)
    for sick in (True, False):
        p_status = prev if sick else 1 - prev
        p_pos = sens if sick else 1 - spec
        for t1, t2 in itertools.product((True, False), repeat=2):
            joint[(sick, t1, t2)] += p_status * (p_pos if t1 else 1 - p_pos) * (p_pos if t2 else 1 - p_pos)
    one = posterior(joint, lambda o: o[0], lambda o: o[1])
    two = posterior(joint, lambda o: o[0], lambda o: o[1] and o[2])
    exact("people with it out of 100,000", 100_000 * prev, 100)
    exact("true positives out of 100,000", 100_000 * prev * sens, 99)
    exact("false positives out of 100,000", 100_000 * (1 - prev) * (1 - spec), 4995)
    exact("P(condition | +)", one, Fraction(99, 99 + 4995))
    approx("P(condition | +) in %", 100 * float(one), 1.94, 2)
    approx("P(condition | +) in % (card)", 100 * float(one), 1.9, 1)
    exact("P(+) = 0.00099 + 0.04995", sum((w for o, w in joint.items() if o[1]), Fraction(0)), Fraction(5094, 100_000))
    approx("P(+)", float(sum((w for o, w in joint.items() if o[1]), Fraction(0))), 0.05094, 5)
    approx("likelihood ratio sens/(1-spec)", float(sens / (1 - spec)), 19.8, 1)
    approx("posterior odds after two positives, numerator against 999", float(two / (1 - two) * 999), 392.04, 2)
    approx("P(condition | +, +) in %", 100 * float(two), 28.2, 1)
    half = posterior(_test_joint(Fraction(1, 100), Fraction(99, 100)), lambda o: o[0], lambda o: o[1])
    exact("1% prevalence, 99% sensitivity and specificity", half, Fraction(1, 2))
    n = 10_000_000
    sick = rng.random(n) < 0.001
    pos = np.where(sick, rng.random(n) < 0.99, rng.random(n) < 0.05)
    simulated("P(condition | +), seeded simulation of 10,000,000 people", sick[pos].mean(), 0.0194, 0.0015)


def _test_joint(prev: Fraction, acc: Fraction) -> dict[tuple, Fraction]:
    """Joint law of (sick, positive) for a test whose sensitivity and specificity both equal `acc`."""
    joint: dict[tuple, Fraction] = {}
    for sick, positive in itertools.product((True, False), repeat=2):
        p_pos = acc if sick else 1 - acc
        joint[(sick, positive)] = (prev if sick else 1 - prev) * (p_pos if positive else 1 - p_pos)
    return joint


# ------------------------------------------------------------------ Example 2: Monty Hall and Monty Fall


def monty(rng: np.random.Generator) -> None:
    print("Example 2 - Monty Hall (cards prob-bayes-monty-hall-switch, prob-bayes-monty-fall-random-host)")
    hall: dict[tuple, Fraction] = defaultdict(Fraction)
    fall: dict[tuple, Fraction] = defaultdict(Fraction)
    for car in (1, 2, 3):
        goats = [d for d in (2, 3) if d != car]
        for opened in goats:  # knowing host: uniform over goat doors he may open
            hall[(car, opened)] += Fraction(1, 3) / len(goats)
        for opened in (2, 3):  # random host: uniform over the two other doors
            fall[(car, opened)] += Fraction(1, 3) * Fraction(1, 2)
    exact("weight car at 1 and host opens 3", hall[(1, 3)], Fraction(1, 6))
    exact("weight car at 2 and host opens 3", hall[(2, 3)], Fraction(1, 3))
    exact("knowing host: P(car at 2 | opens 3)", posterior(hall, lambda o: o[0] == 2, lambda o: o[1] == 3), Fraction(2, 3))
    exact(
        "random host: P(car at 2 | opens 3, goat shown)",
        posterior(fall, lambda o: o[0] == 2, lambda o: o[1] == 3 and o[0] != 3),
        Fraction(1, 2),
    )
    n = 1_000_000
    car = rng.integers(1, 4, n)
    coin = rng.integers(0, 2, n)
    opened = np.where(car == 1, 2 + coin, np.where(car == 2, 3, 2))
    switch_to = 5 - opened  # the unopened door among 2 and 3
    simulated("knowing host: switching wins, simulated", (switch_to == car).mean(), 2 / 3, 0.003)
    random_open = 2 + rng.integers(0, 2, n)
    shows_goat = random_open != car
    simulated("random host: switching wins given a goat, simulated", ((5 - random_open) == car)[shows_goat].mean(), 0.5, 0.003)

    print("Monty Hall with 100 doors (card prob-bayes-monty-hall-hundred-doors)")
    # host opens 98 goat doors among 2..100, leaving one other door closed; by symmetry fix which door stays shut
    weights: dict[tuple, Fraction] = {}
    for car_door in range(1, 101):
        for kept in range(2, 101):
            if car_door != 1 and kept != car_door:
                continue  # host must keep the car door shut
            weights[(car_door, kept)] = Fraction(1, 100) * (Fraction(1, 99) if car_door == 1 else 1)
    exact("weight: car at 1 and door 57 kept shut", weights[(1, 57)], Fraction(1, 9900))
    exact("weight: car at 57 and door 57 kept shut", weights[(57, 57)], Fraction(1, 100))
    exact(
        "P(win by switching | host keeps door 57 shut)", posterior(weights, lambda o: o[0] == o[1], lambda o: o[1] == 57), Fraction(99, 100)
    )


# ------------------------------------------------------------------ Examples 3 to 5


def coins_and_children() -> None:
    print("Example 3 - double-headed coin (card prob-bayes-double-headed-coin)")
    joint: dict[tuple, Fraction] = {}
    for coin in ("double", "fair"):
        prior = Fraction(1, 1000) if coin == "double" else Fraction(999, 1000)
        for flips in itertools.product("HT", repeat=11):
            p = prior
            for f in flips:
                p *= (1 if f == "H" else 0) if coin == "double" else Fraction(1, 2)
            if p:
                joint[(coin, flips)] = p
    ten_heads = lambda o: all(f == "H" for f in o[1][:10])  # noqa: E731
    p_double = posterior(joint, lambda o: o[0] == "double", ten_heads)
    exact("P(double-headed | 10 heads)", p_double, Fraction(1024, 2023))
    approx("P(double-headed | 10 heads)", float(p_double), 0.506, 3)
    approx("P(fair | 10 heads)", float(1 - p_double), 0.494, 3)
    nxt = posterior(joint, lambda o: o[1][10] == "H", ten_heads)
    exact("P(11th flip H | 10 heads)", nxt, Fraction(3047, 4046))
    approx("P(11th flip H | 10 heads)", float(nxt), 0.753, 3)

    print("Example 4 - boy-girl (cards prob-bayes-boy-girl-at-least-one, prob-bayes-boy-born-tuesday)")
    kids = list(itertools.product(itertools.product("BG", range(7)), repeat=2))
    uniform = {k: Fraction(1, len(kids)) for k in kids}
    both_boys = lambda o: o[0][0] == "B" and o[1][0] == "B"  # noqa: E731
    exact("(sex, day) pairs", len(kids), 14**2)
    exact("P(BB | at least one boy)", posterior(uniform, both_boys, lambda o: "B" in (o[0][0], o[1][0])), Fraction(1, 3))
    tuesday = lambda o: ("B", 1) in o  # noqa: E731
    exact("pairs with a Tuesday boy = 14^2 - 13^2", sum(1 for k in kids if tuesday(k)), 27)
    exact("of which two boys = 7^2 - 6^2", sum(1 for k in kids if tuesday(k) and both_boys(k)), 13)
    exact("P(BB | a boy born on Tuesday)", posterior(uniform, both_boys, tuesday), Fraction(13, 27))
    met = {(k, i): w / 2 for k, w in uniform.items() for i in (0, 1)}  # meet one child chosen at random
    exact(
        "P(BB | a randomly met child is a boy)", posterior(met, lambda o: both_boys(o[0]), lambda o: o[0][o[1]][0] == "B"), Fraction(1, 2)
    )

    print("Example 5 - fair or 0.6 coin, 7 heads in 10 (card prob-bayes-biased-coin-seven-of-ten)")
    joint5: dict[tuple, Fraction] = defaultdict(Fraction)
    for coin, p in (("fair", Fraction(1, 2)), ("biased", Fraction(3, 5))):
        for seq in itertools.product((0, 1), repeat=10):
            h = sum(seq)
            joint5[(coin, h)] += Fraction(1, 2) * p**h * (1 - p) ** (10 - h)
    post = posterior(joint5, lambda o: o[0] == "biased", lambda o: o[1] == 7)
    lr = post / (1 - post)
    approx("likelihood ratio 1.2^7 * 0.8^3", float(lr), 1.835, 3)
    approx("P(biased | 7 of 10)", float(post), 0.647, 3)
    approx("1 + likelihood ratio", 1 + float(lr), 2.835, 3)
    approx("log-odds added by a head", math.log(1.2), 0.18, 2)
    approx("log-odds removed by a tail", -math.log(0.8), 0.22, 2)
    approx("log 1.2 (3 dp)", math.log(1.2), 0.182, 3)
    approx("-log 0.8 (3 dp)", -math.log(0.8), 0.223, 3)
    lo, hi = 0.0, 1.0  # find the head fraction where the log likelihood ratio changes sign, by bisection
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if mid * math.log(1.2) + (1 - mid) * math.log(0.8) < 0 else (lo, mid)
    approx("break-even head fraction", lo, 0.55, 2)
    approx("break-even head fraction (3 dp)", lo, 0.550, 3)


# ------------------------------------------------------------------ independence, succession, small cards


def independence_and_small_cards() -> None:
    print("Independence (cards prob-bayes-pairwise-not-mutual, prob-bayes-conditional-vs-unconditional-independence)")
    bits = {(x, y, x ^ y): Fraction(1, 4) for x, y in itertools.product((0, 1), repeat=2)}

    def prob(event) -> Fraction:
        return sum((w for o, w in bits.items() if event(o)), Fraction(0))

    for i, j in itertools.combinations(range(3), 2):
        assert prob(lambda o, i=i, j=j: o[i] == 1 and o[j] == 1) == Fraction(1, 4) == prob(lambda o, i=i: o[i] == 1) ** 2
    print("    X, Y, Z = X xor Y: every pair has joint probability 1/4 = (1/2)(1/2)")
    exact("P(X=Y=Z=1)", prob(lambda o: o == (1, 1, 1)), 0)

    coin: dict[tuple, Fraction] = defaultdict(Fraction)
    for kind, ph in (("fair", Fraction(1, 2)), ("two-headed", Fraction(1))):
        for f1, f2 in itertools.product((1, 0), repeat=2):
            coin[(kind, f1, f2)] += Fraction(1, 2) * (ph if f1 else 1 - ph) * (ph if f2 else 1 - ph)
    p_h1 = sum((w for o, w in coin.items() if o[1]), Fraction(0))
    p_h1h2 = sum((w for o, w in coin.items() if o[1] and o[2]), Fraction(0))
    exact("P(H1)", p_h1, Fraction(3, 4))
    exact("P(H1 H2)", p_h1h2, Fraction(5, 8))
    exact("P(H1) P(H2)", p_h1 * p_h1, Fraction(9, 16))

    two = {(x, y): Fraction(1, 4) for x, y in itertools.product("HT", repeat=2)}
    at_least_one = lambda o: "H" in o  # noqa: E731
    exact("P(X=H | at least one head)", posterior(two, lambda o: o[0] == "H", at_least_one), Fraction(2, 3))
    exact(
        "P(X=H | at least one head, Y=H)", posterior(two, lambda o: o[0] == "H", lambda o: at_least_one(o) and o[1] == "H"), Fraction(1, 2)
    )

    print("Rule of succession (card prob-bayes-rule-of-succession), by exact polynomial integration")

    def integral_p_power(a: int, b: int) -> Fraction:
        """Integral over [0,1] of p^a (1-p)^b, expanding (1-p)^b binomially."""
        return sum((Fraction((-1) ** j * math.comb(b, j), a + j + 1) for j in range(b + 1)), Fraction(0))

    def predictive(s: int, n: int) -> Fraction:
        return integral_p_power(s + 1, n - s) / integral_p_power(s, n - s)

    exact("P(next H | 3 of 3)", predictive(3, 3), Fraction(4, 5))
    exact("P(next H | 1 of 1)", predictive(1, 1), Fraction(2, 3))
    for n in range(8):
        for s in range(n + 1):
            assert predictive(s, n) == Fraction(s + 1, n + 2)
    print("    (s+1)/(n+2) matches the integral for all s <= n <= 7")

    print("Three cards and urns (cards prob-bayes-three-cards, prob-bayes-urn-choice)")
    faces = {(card, side): Fraction(1, 6) for card in ("RR", "BB", "RB") for side in (0, 1)}
    exact("P(other side red | red shown)", posterior(faces, lambda o: o[0][1 - o[1]] == "R", lambda o: o[0][o[1]] == "R"), Fraction(2, 3))
    urn_joint: dict[tuple, Fraction] = defaultdict(Fraction)
    for urn, contents in (("A", "RRRB"), ("B", "RBBB")):
        for i, ball in enumerate(contents):
            urn_joint[(urn, i, ball)] += Fraction(1, 8)
    exact("P(urn A | red)", posterior(urn_joint, lambda o: o[0] == "A", lambda o: o[2] == "R"), Fraction(3, 4))

    print("Simpson's paradox, hypothetical fill rates (card prob-bayes-simpson-fill-rates)")
    fills = {"A": {"easy": (18, 20), "hard": (40, 80)}, "B": {"easy": (70, 80), "hard": (9, 20)}}
    for regime in ("easy", "hard"):
        fa, na = fills["A"][regime]
        fb, nb = fills["B"][regime]
        assert Fraction(fa, na) > Fraction(fb, nb)
    exact("A easy fill rate", Fraction(*fills["A"]["easy"]), Fraction(9, 10))
    exact("B easy fill rate", Fraction(*fills["B"]["easy"]), Fraction(7, 8))
    exact("A hard fill rate", Fraction(*fills["A"]["hard"]), Fraction(1, 2))
    exact("B hard fill rate", Fraction(*fills["B"]["hard"]), Fraction(9, 20))
    total = {k: Fraction(sum(f for f, _ in v.values()), sum(n for _, n in v.values())) for k, v in fills.items()}
    approx("B easy fill rate in %", 100 * fills["B"]["easy"][0] / fills["B"]["easy"][1], 87.5, 1)
    approx("B hard fill rate in %", 100 * fills["B"]["hard"][0] / fills["B"]["hard"][1], 45, 0)
    approx("A overall fill rate in %", float(100 * Fraction(18 + 40, 100)), 58, 0)
    approx("B overall fill rate in %", float(100 * Fraction(70 + 9, 100)), 79, 0)
    exact("A overall fill rate", total["A"], Fraction(58, 100))
    exact("B overall fill rate", total["B"], Fraction(79, 100))


def main() -> None:
    rng = np.random.default_rng(SEED)
    rare_condition(rng)
    monty(rng)
    coins_and_children()
    independence_and_small_cards()
    print("All Bayes checks passed.")


if __name__ == "__main__":
    main()
