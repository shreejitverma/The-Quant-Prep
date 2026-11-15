"""Market making games: every number in `08-Market-Making/10-Market-Making-Games.md`.

Independent routes used here:
- quote values by walking the game tree of `./qp drill mm` (every dice outcome with `fractions.Fraction`,
  every counterparty type and action with its probability, P&L as cash plus position marked at the total),
  never via the closed-form EV formula the note states;
- the maker's best response by brute force over every integer quote of width 1 to 4, in every reachable
  state (every prefix of revealed dice), which backs the "in every round" claims;
- the quoted EVs and the lift posterior again by seeded Monte Carlo through the real game engine
  `tools.qp.drills.MarketMakingGame`, with tolerances of four standard errors;
- dice moments and the maximum of two dice by enumeration.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 08-Market-Making/code/mm_10_market_making_games.py`.
"""

from __future__ import annotations

import itertools
import math
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.qp.drills import MarketMakingGame  # noqa: E402

HALF, THIRD = F(1, 2), F(1, 3)
LOT = 10


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.3f} (quoted {expected}, tolerance {tol:.3f})")


def totals(known: tuple[int, ...], n: int = 4) -> Counter:
    return Counter(sum(known) + sum(r) for r in itertools.product(range(1, 7), repeat=n - len(known)))


def tree_ev(bid: int, ask: int, known: tuple[int, ...]) -> F:
    """Expected P&L of one round for LOT lots, by walking the game tree from the drill's rules."""
    dist = totals(known)
    n = sum(dist.values())
    ev = F(0)
    for t, ways in dist.items():
        p_t = F(ways, n)
        # informed: lifts the ask (we sell) if t > ask, hits the bid (we buy) if t < bid, else passes
        informed = [("sell", F(1))] if t > ask else [("buy", F(1))] if t < bid else [(None, F(1))]
        noise = [("sell", THIRD), ("buy", THIRD), (None, THIRD)]
        for who, actions in ((HALF, informed), (HALF, noise)):
            for side, p_a in actions:
                if side == "sell":
                    pnl = LOT * ask - LOT * t  # cash in, short LOT marked at t
                elif side == "buy":
                    pnl = -LOT * bid + LOT * t
                else:
                    pnl = 0
                ev += p_t * who * p_a * pnl
    return ev


def quotes(known: tuple[int, ...]):
    lo = sum(known) + (4 - len(known))
    hi = sum(known) + 6 * (4 - len(known))
    for bid in range(lo - 6, hi + 6):
        for width in range(1, 5):
            yield bid, bid + width


def best_by_width(known: tuple[int, ...]) -> dict[int, tuple[F, list[tuple[int, int]]]]:
    out: dict[int, tuple[F, list[tuple[int, int]]]] = {}
    for bid, ask in quotes(known):
        ev = tree_ev(bid, ask, known)
        w = ask - bid
        if w not in out or ev > out[w][0]:
            out[w] = (ev, [(bid, ask)])
        elif ev == out[w][0]:
            out[w][1].append((bid, ask))
    return out


def moments() -> None:
    print("Fair value first (cards mm-game-four-dice-moments, mm-game-narration)")
    d = totals(())
    n = sum(d.values())
    mean = F(sum(t * w for t, w in d.items()), n)
    var = F(sum(t * t * w for t, w in d.items()), n) - mean**2
    exact("dice outcomes", n, 1296)
    exact("E[T], four dice", mean, 14)
    exact("Var(T), four dice", var, F(35, 3))
    approx("sd(T)", math.sqrt(var), 3.42, 2)
    approx("sd(T) as narrated", math.sqrt(var), 3.4, 1)
    one = F(sum(k * k for k in range(1, 7)), 6) - F(7, 2) ** 2
    exact("variance of one die", one, F(35, 12))


def example1() -> None:
    print("Example 1: the opening market (cards mm-game-opening-quote, mm-game-max-width-optimal)")
    for (bid, ask), lit in (((12, 16), 0.74), ((13, 16), -2.60), ((13, 15), -5.95), ((14, 15), -9.83)):
        approx(f"EV of {bid} / {ask} per 10 lots", float(tree_ev(bid, ask, ())), lit, 2)
    d = totals(())
    n = sum(d.values())
    loss = F(sum(w * (max(t - 16, 0) + max(12 - t, 0)) for t, w in d.items()), n)
    approx("informed loss per lot at 12 / 16", float(loss), 1.185, 3)
    approx("noise edge per lot at width 4", float(F(4, 3)), 1.333, 3)
    approx("EV per lot at 12 / 16", float(tree_ev(12, 16, ()) / LOT), 0.074, 3)
    for bid, ask in ((13, 17), (11, 15)):
        approx(f"EV of off-centre {bid} / {ask}", float(tree_ev(bid, ask, ())), 0.26, 2)
    approx("cost of 13 / 17 instead of 12 / 16", float(tree_ev(12, 16, ()) - tree_ev(13, 17, ())), 0.48, 2)
    best = best_by_width(())
    exact("best opening quote", best[4][1], [(12, 16)])
    for w in (1, 2, 3):
        assert best[w][0] < 0, (w, best[w])
    print("    every width-1, width-2 and width-3 opening quote loses money")


def example2() -> None:
    print("Example 2: later rounds (cards mm-game-max-width-optimal, mm-game-later-round)")
    rows = (((6,), 16.5, [(14, 18), (15, 19)], 2.13), ((6, 2), 15, [(13, 17)], 3.89), ((6, 2, 5), 16.5, [(14, 18), (15, 19)], 5.83))
    for known, fair, best_q, lit in rows:
        exact(f"fair value after {known}", sum(known) + F(7, 2) * (4 - len(known)), F(fair))
        best = best_by_width(known)
        exact(f"best width-4 quotes after {known}", sorted(best[4][1]), best_q)
        approx(f"best EV after {known}", float(best[4][0]), lit, 2)
    # the noise edge of a width-4 quote is the same every round, so the rise in EV is a fall in informed loss
    losses = []
    for known, _, best_q, _ in rows:
        bid, ask = best_q[0]
        d = totals(known)
        losses.append(F(sum(w * (max(t - ask, 0) + max(bid - t, 0)) for t, w in d.items()), sum(d.values())))
        assert tree_ev(bid, ask, known) == LOT * (HALF * F(ask - bid, 3) - HALF * losses[-1])
    assert losses[0] > losses[1] > losses[2]
    for x, lit in zip(losses, (0.907, 0.556, 0.167), strict=True):
        approx("informed loss per lot at the best quote", float(x), lit, 3)
    print(f"    informed loss per lot at the best quote = {[round(float(x), 3) for x in losses]} (falling)")
    approx("last round, 15 / 18", float(tree_ev(15, 18, (6, 2, 5))), 3.33, 2)
    exact("last round, 16 / 18", tree_ev(16, 18, (6, 2, 5)), 0)

    print("Every reachable state: the best quote has width 4 and every width-1 quote loses")
    states = 0
    for r in range(4):
        for known in itertools.product(range(1, 7), repeat=r):
            best = best_by_width(known)
            top = max(best[w][0] for w in best)
            assert best[4][0] == top, (known, best)
            assert all(best[w][0] < best[4][0] for w in (1, 2, 3)), known
            assert best[1][0] < 0, known
            states += 1
    exact("states checked", states, 1 + 6 + 36 + 216)


def example3() -> None:
    print("Example 3: updating on being lifted (cards mm-game-lift-update, mm-game-informed-posterior, mm-game-lift-then-reveal)")
    d = totals(())
    n = sum(d.values())
    p_hi = F(sum(w for t, w in d.items() if t > 16), n)
    exact("P(T >= 17)", p_hi, F(155, 648))
    approx("P(T >= 17)", float(p_hi), 0.239, 3)
    p_lift = HALF * p_hi + HALF * THIRD
    approx("P(informed | lift)", float(HALF * p_hi / p_lift), 0.42, 2)

    def like(t: int) -> F:
        return HALF * (1 if t > 16 else 0) + HALF * THIRD

    exact("lift likelihood ratio, totals >= 17 against the rest", like(17) / like(16), 4)
    post = F(sum(w * like(t) * t for t, w in d.items()), sum(w * like(t) for t, w in d.items()))
    approx("E[T | lift]", float(post), 15.87, 2)
    approx("shift from the prior", float(post - 14), 1.9, 1)
    rest = [3 + sum(r) for r in itertools.product(range(1, 7), repeat=3)]
    post3 = F(sum(like(t) * t for t in rest), sum(like(t) for t in rest))
    exact("dice-only fair value after a 3", F(3) + 3 * F(7, 2), F(27, 2))
    approx("E[T | lift, first die 3]", float(post3), 14.97, 2)


def engine_monte_carlo() -> None:
    print("Monte Carlo through tools.qp.drills.MarketMakingGame (seeds 0..N-1)")
    n = 200_000
    pnl_sum = pnl_sq = 0.0
    lifts = lift_total = informed_lifts = 0
    for seed in range(n):
        g = MarketMakingGame(seed=seed)
        ev = g.quote(12, 16)
        t = g.total
        trade = ev["trade"]
        pnl = 0
        if trade:
            pnl = LOT * (16 - t) if trade["side"] == "sell" else LOT * (t - 12)
            if trade["side"] == "sell":
                lifts += 1
                lift_total += t
                informed_lifts += trade["counterparty"] == "informed"
        pnl_sum += pnl
        pnl_sq += pnl * pnl
    mean = pnl_sum / n
    se = math.sqrt((pnl_sq / n - mean * mean) / n)
    simulated("engine EV of 12 / 16 per 10 lots", mean, 0.74, 4 * se)
    p_inf = informed_lifts / lifts
    simulated("engine P(informed | lift)", p_inf, 0.42, 4 * math.sqrt(p_inf * (1 - p_inf) / lifts) + 0.005)
    simulated("engine E[T | lift]", lift_total / lifts, 15.87, 4 * 3.0 / math.sqrt(lifts) + 0.005)


def example4() -> None:
    print("Example 4: a verbal game with position risk (cards mm-game-max-two-dice, mm-game-position-risk)")
    rolls = list(itertools.product(range(1, 7), repeat=2))
    exact("E[max of two dice]", F(sum(max(r) for r in rolls), 36), F(161, 36))
    approx("E[max of two dice]", 161 / 36, 4.47, 2)
    exact("P(max = 6)", F(sum(max(r) == 6 for r in rolls), 36), F(11, 36))
    approx("20 x sd of one die", 20 * math.sqrt(35 / 12), 34.2, 1)


if __name__ == "__main__":
    moments()
    example1()
    example2()
    example3()
    engine_monte_carlo()
    example4()
    print("all market making game checks passed")
