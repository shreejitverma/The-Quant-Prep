"""Expected value and betting decisions: every number in the note.

Backs every number in `11-Risk-and-Trading/02-Expected-Value-and-Betting-Decisions.md`.
Independent routes used here:
- die-reroll values by exhaustive search over every keep-set policy with exact fractions, not the threshold rule;
- the accumulate-or-wipe stopping rule by value iteration on a large truncated state space, plus seeded simulation;
- ruin probabilities by solving the finite absorbing Markov chain, compared with (q/p)^B and the diffusion formula;
- bets needed to show an edge from the exact binomial tail, with the normal quantile found by bisection on erf;
- edge-versus-variance growth by numerically maximising E[log(1 + fX)] for a two-point bet with the same mean and sd;
- the series replication stake by backward induction on the full series tree, and the 42/64 by enumerating outcomes;
- the red-black stopping game by brute force over every Markov policy for small decks and by seeded simulation;
- certainty equivalents by root-finding on log utility; doubling strategies by enumerating every coin path.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 11-Risk-and-Trading/code/risk_02_expected_value.py`.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction
from functools import lru_cache

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
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol})")


def norm_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def norm_ppf(p: float) -> float:
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


# ------------------------------------------------------------------ sections


def rerolls() -> None:
    print("Example 1: a die with up to two rerolls (cards risk-ev-reroll-die, risk-ev-reroll-three)")
    faces = range(1, 7)
    keep_sets = [frozenset(s) for k in range(7) for s in itertools.combinations(faces, k)]

    def best_value(rerolls_left: int) -> Fraction:
        if rerolls_left == 0:
            return Fraction(sum(faces), 6)
        cont = best_value(rerolls_left - 1)
        # exhaustive search over which faces to keep; the policy is not assumed to be a threshold
        return max(sum((Fraction(f) if f in keep else cont) for f in faces) / 6 for keep in keep_sets)

    exact("V0", best_value(0), Fraction(7, 2))
    exact("V1", best_value(1), Fraction(17, 4))
    exact("V2", best_value(2), Fraction(14, 3))
    approx("V2", float(best_value(2)), 4.67, 2)
    exact("V3", best_value(3), Fraction(89, 18))
    approx("V3", float(best_value(3)), 4.94, 2)
    exact("(4.25 x 4 + 11)/6", (Fraction(17, 4) * 4 + 11) / 6, Fraction(14, 3))


def pig(rng: np.random.Generator) -> None:
    print("Example 2: accumulate or lose everything (cards risk-ev-pig-threshold, risk-ev-pig-value)")
    cap = 400  # stopping is optimal far below this cap, so truncation does not bind
    values = [float(s) for s in range(cap + 7)]
    for _ in range(3000):
        values = [max(float(s), sum(values[s + k] for k in range(2, 7)) / 6) if s < cap else float(s) for s in range(cap + 7)]
    cont = [sum(values[s + k] for k in range(2, 7)) / 6 for s in range(cap)]
    keep_rolling = [s for s in range(cap) if cont[s] > s + 1e-9]
    exact("totals at which rolling on is strictly better", keep_rolling, list(range(20)))
    approx("continuation value at a total of 20 (indifferent)", cont[20], 20.0, 9)
    exact("one-step gain (5/6) x 4 - S/6 at S = 20", Fraction(5, 6) * 4 - Fraction(20, 6), Fraction(0))
    exact("(2+3+4+5+6)/6 equals (5/6) x 4", Fraction(20, 6), Fraction(5, 6) * 4)
    approx("value of the game from zero under the optimal rule", values[0], 8.14, 2)
    rule: dict[int, Fraction] = {t: Fraction(t) for t in range(20, 26)}
    for t in range(19, -1, -1):
        rule[t] = sum((rule[t + k] for k in range(2, 7)), Fraction(0)) / 6
    approx("value of the stop-at-20 rule by exact recursion with fractions", float(rule[0]), 8.14, 2)
    n = 400_000
    total = np.zeros(n)
    alive = np.ones(n, dtype=bool)
    while alive.any():
        roll = rng.integers(1, 7, size=n)
        rolling = alive & (total < 20)
        wiped = rolling & (roll == 1)
        total = np.where(rolling & ~wiped, total + roll, total)
        total[wiped] = 0.0
        alive = rolling & ~wiped
    se = float(total.std(ddof=1) / math.sqrt(n))
    simulated("value under stop-at-20, simulated", float(total.mean()), 8.14, 5 * se + 0.005)


def ruin() -> None:
    print("Example 3: ruin on a 51% even-money bet (cards risk-ev-ruin-51, risk-ev-bankroll-one-percent, risk-ev-bets-to-show-edge)")
    p, q, start = 0.51, 0.49, 50
    # absorbing chain on 0..N with a far upper boundary standing in for an opponent with unlimited capital
    big = 4000
    # P(ruin from k) solves P_k = p P_{k+1} + q P_{k-1}; Thomas algorithm on the tridiagonal system
    m = big - 1
    sub, dia, sup, rhs = np.full(m, -q), np.ones(m), np.full(m, -p), np.zeros(m)
    rhs[0] = q  # P_0 = 1
    for i in range(1, m):
        w = sub[i] / dia[i - 1]
        dia[i] -= w * sup[i - 1]
        rhs[i] -= w * rhs[i - 1]
    sol = np.zeros(m)
    sol[-1] = rhs[-1] / dia[-1]
    for i in range(m - 2, -1, -1):
        sol[i] = (rhs[i] - sup[i] * sol[i + 1]) / dia[i]
    chain = float(sol[start - 1])
    approx("P(ruin) from 50 units, Markov-chain solve", chain, 0.135, 3)
    approx("(0.49/0.51)^50", (q / p) ** start, 0.135, 3)
    mu, var = p - q, 1.0 - (p - q) ** 2
    approx("edge per bet", mu, 0.02, 12)
    approx("variance per bet (about 1)", var, 0.9996, 4)
    approx("diffusion exp(-2 mu B / sigma^2)", math.exp(-2 * mu * start / var), 0.135, 3)
    approx("e^-2", math.exp(-2.0), 0.135, 3)
    approx("bankroll for 1% ruin, diffusion with sigma^2 = 1", math.log(100) / (2 * mu), 115.0, 0)
    approx("bankroll for 1% ruin, exact (q/p)^B = 0.01", math.log(100) / math.log(p / q), 115.0, 0)
    approx("bankroll for 1% ruin, exact, one decimal", math.log(100) / math.log(p / q), 115.1, 1)
    approx("sigma per bet", math.sqrt(var), 0.9998, 4)
    z95 = norm_ppf(0.95)
    approx("z_0.95 by bisection on erf", z95, 1.6449, 4)
    n_normal = (z95 * math.sqrt(var) / mu) ** 2
    approx("bets to be 95% sure of being ahead, normal approximation", n_normal, 6761.0, 0)
    # exact: smallest n with P(more wins than losses) >= 0.95
    lp, lq = math.log(p), math.log(q)

    def p_ahead(n: int) -> float:
        return sum(
            math.exp(math.lgamma(n + 1) - math.lgamma(w + 1) - math.lgamma(n - w + 1) + w * lp + (n - w) * lq)
            for w in range(n // 2 + 1, n + 1)
        )

    n = 6000
    while p_ahead(n) < 0.95:
        n += 1
    exact("smallest n with exact binomial P(ahead) >= 0.95", n, 6763)
    exact("P(ahead) at n + 1 falls back below 0.95 (a tie is possible at even n)", p_ahead(n + 1) < 0.95, True)
    even = 6764
    while p_ahead(even) < 0.95:
        even += 2
    exact("smallest even n with P(ahead) >= 0.95", even, 6862)
    odd_run = [p_ahead(k) for k in range(6763, 7001, 2)]
    even_run = [p_ahead(k) for k in range(6862, 7001, 2)]
    assert all(b > a for a, b in itertools.pairwise(odd_run)) and all(b > a for a, b in itertools.pairwise(even_run))
    assert p_ahead(6860) < 0.95 <= p_ahead(6861)
    print("    P(ahead) rises along odd and along even n, so it stays at or above 0.95 from n = 6,861 (checked to 7,000)")
    assert abs(n - 6800) < 100
    print("    both are about 6,800")


def edge_vs_variance() -> None:
    print("Example 4: which bet would you rather have (card risk-ev-edge-vs-variance)")
    growths: dict[str, float] = {}
    for name, mu, sd, sharpe, growth, decimals in [("A", 1.0, 10.0, 0.1, 0.005, 3), ("B", 0.5, 2.0, 0.25, 0.031, 3)]:
        approx(f"per-bet Sharpe of {name}", mu / sd, sharpe, 12)
        approx(f"mu^2/(2 sigma^2) for {name}", mu**2 / (2 * sd**2), growth, decimals)
        # a two-point bet with the same mean and sd, sized by maximising E[log(1 + f X)] numerically
        lo_x, hi_x = mu - sd, mu + sd
        g = lambda f, lo_x=lo_x, hi_x=hi_x: 0.5 * math.log1p(f * hi_x) + 0.5 * math.log1p(f * lo_x)  # noqa: E731
        a, b = 0.0, 0.999 / abs(lo_x)
        for _ in range(200):
            c1, c2 = a + (b - a) / 3, b - (b - a) / 3
            if g(c1) < g(c2):
                a = c1
            else:
                b = c2
        exact_growth = g((a + b) / 2)
        growths[name] = exact_growth
        assert abs(exact_growth / (mu**2 / (2 * sd**2)) - 1) < 0.04, (name, exact_growth)
        print(
            f"    optimal growth of a two-point bet {name} with the same mean and sd = {exact_growth:.4f} (within 4% of mu^2/(2 sigma^2))"
        )
    approx("B growth over A growth, approximation", (0.25 / 8) / 0.005, 6.25, 2)
    assert growths["B"] / growths["A"] > 6
    print(f"    B growth over A growth, two-point bets = {growths['B'] / growths['A']:.2f} (over six)")
    approx("sigma_A^2 / mu_A", 10.0**2 / 1.0, 100.0, 12)


def series() -> None:
    print("Example 5: replicating a series bet with game bets (card risk-ev-series-replication)")
    wins = sum(1 for seq in itertools.product((0, 1), repeat=6) if sum(seq) >= 3)
    exact("outcomes of the next six games with at least 3 wins", wins, 42)

    @lru_cache(None)
    def value(a: int, b: int) -> Fraction:
        if a == 4:
            return Fraction(100)
        if b == 4:
            return Fraction(-100)
        return (value(a + 1, b) + value(a, b + 1)) / 2

    exact("value before game 1", value(0, 0), Fraction(0))
    exact("value after a game-1 win", value(1, 0), Fraction(125, 4))
    exact("value after a game-1 loss", value(0, 1), Fraction(-125, 4))
    exact("first stake (V_up - V_down)/2", (value(1, 0) - value(0, 1)) / 2, Fraction(125, 4))
    exact("100 x (84 - 64)/64", Fraction(100 * (84 - 64), 64), Fraction(125, 4))
    exact("100 C(6,3)/2^6", Fraction(100 * math.comb(6, 3), 2**6), Fraction(125, 4))


@lru_cache(None)
def red_black(r: int, b: int) -> Fraction:
    if r == 0:
        return Fraction(0)
    if b == 0:
        return Fraction(r)
    go = Fraction(r, r + b) * (1 + red_black(r - 1, b)) + Fraction(b, r + b) * (-1 + red_black(r, b - 1))
    return max(Fraction(0), go)


def brute_force_red_black(reds: int, blacks: int) -> Fraction:
    """Best value over every stop/continue rule on (reds left, blacks left), averaged over all orderings."""
    states = [(r, b) for r in range(reds + 1) for b in range(blacks + 1) if r + b > 0]
    orderings = set(itertools.permutations([1] * reds + [-1] * blacks))
    best = Fraction(-(10**9))
    for rule in itertools.product((False, True), repeat=len(states)):
        stop = dict(zip(states, rule, strict=True))
        total = Fraction(0)
        for order in orderings:
            r, b, pay = reds, blacks, 0
            for card in order:
                if stop[(r, b)]:
                    break
                pay += card
                r, b = (r - 1, b) if card == 1 else (r, b - 1)
            total += pay
        best = max(best, total / len(orderings))
    return best


def red_black_games(rng: np.random.Generator) -> None:
    print("Example 6: stop any time in a red-black deck (cards risk-ev-red-black-stop, risk-ev-next-card-red)")
    exact("V(1,1) by brute force over every rule", brute_force_red_black(1, 1), Fraction(1, 2))
    exact("V(2,2) by brute force over every rule", brute_force_red_black(2, 2), Fraction(2, 3))
    exact("V(1,1) and V(2,2) by the recursion", (red_black(1, 1), red_black(2, 2)), (Fraction(1, 2), Fraction(2, 3)))
    exact("V(3,3) brute force equals recursion", brute_force_red_black(3, 3), red_black(3, 3))
    approx("V(26,26) by the recursion", float(red_black(26, 26)), 2.6245, 4)
    approx("V(26,26)", float(red_black(26, 26)), 2.62, 2)
    # play the recursion's policy on seeded shuffles and measure the payoff
    stop = np.zeros((27, 27), dtype=bool)
    for r in range(27):
        for b in range(27):
            if r == 0:
                stop[r, b] = True
            elif b > 0:
                go = Fraction(r, r + b) * (1 + red_black(r - 1, b)) + Fraction(b, r + b) * (-1 + red_black(r, b - 1))
                stop[r, b] = go <= 0
    n = 400_000
    cards = np.where(np.argsort(rng.random((n, 52)), axis=1) < 26, 1, -1)
    r = np.full(n, 26)
    b = np.full(n, 26)
    pays = np.zeros(n)
    alive = np.ones(n, dtype=bool)
    for j in range(52):
        alive &= ~stop[r, b]
        card = cards[:, j]
        pays += np.where(alive, card, 0)
        r -= alive & (card == 1)
        b -= alive & (card == -1)
    se = float(pays.std(ddof=1) / math.sqrt(n))
    simulated("payoff of that policy, simulated", float(pays.mean()), 2.6245, 5 * se)
    approx("simulated mean as quoted in the note", float(pays.mean()), 2.63, 2)
    approx("its standard error", se, 0.003, 3)

    # next-card-red: every rule wins with probability 1/2; exhaustive check on a small deck over every Markov rule
    reds, blacks = 3, 3
    states = [(r, b) for r in range(reds + 1) for b in range(blacks + 1) if r + b > 0]
    orderings = set(itertools.permutations([1] * reds + [0] * blacks))
    win_probs = set()
    for rule in itertools.product((False, True), repeat=len(states)):
        stop = dict(zip(states, rule, strict=True))
        wins = 0
        for order in orderings:
            r, b = reds, blacks
            for i, card in enumerate(order):
                if stop[(r, b)] or i == len(order) - 1:
                    wins += card
                    break
                r, b = (r - 1, b) if card == 1 else (r, b - 1)
        win_probs.add(Fraction(wins, len(orderings)))
    exact("win probabilities of every rule, 3 red and 3 black", win_probs, {Fraction(1, 2)})


def utility() -> None:
    print("Example 7: a million on a coin or 400,000 for sure (card risk-ev-bankroll-utility)")
    for wealth, quoted in [(100_000.0, 231_700.0), (10_000_000.0, 488_100.0)]:
        target = 0.5 * math.log(wealth + 1_000_000.0) + 0.5 * math.log(wealth)
        lo, hi = 0.0, 1_000_000.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if math.log(wealth + mid) < target:
                lo = mid
            else:
                hi = mid
        ce = (lo + hi) / 2
        approx(f"certainty equivalent at wealth {wealth:,.0f}, to the nearest 100", round(ce, -2), quoted, 0)
        if wealth == 100_000.0:
            approx("card: about 232,000", round(ce, -3), 232_000.0, 0)
            assert ce < 400_000
        else:
            assert ce > 400_000
    print("    take the sure 400,000 at 100,000 of wealth and the gamble at 10,000,000")


def doubling() -> None:
    print("Doubling after every loss (card risk-ev-doubling)")
    for capital in (1, 3, 7, 15, 31, 63):
        ev = Fraction(0)
        for path in itertools.product((1, -1), repeat=8):
            prob, cash, stake = Fraction(1, 2**8), 0, 1
            for step in path:
                if stake > capital + cash or cash > 0:
                    break
                cash += step * stake
                stake *= 2
            ev += prob * cash
        assert ev == 0, (capital, ev)
    print("    expected profit is exactly 0 for capital 1 to 63 over every 8-flip path")


def main() -> None:
    rng = np.random.default_rng(SEED)
    rerolls()
    pig(rng)
    ruin()
    edge_vs_variance()
    series()
    red_black_games(rng)
    utility()
    doubling()
    print("All expected-value numbers check.")


if __name__ == "__main__":
    main()
