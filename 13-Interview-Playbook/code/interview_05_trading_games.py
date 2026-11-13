"""Trading games: every fair value, ledger, auction, stopping and Kelly number in the note.

Backs every number in `13-Interview-Playbook/05-Trading-Games-in-Interviews.md`.
Independent routes used here:
- dice fair values and standard deviations by enumerating every outcome with `fractions.Fraction`;
- the card-sum variance from the exact covariance of two distinct cards (all 52 x 51 ordered pairs),
  not the finite-population-correction formula, plus seeded simulation of shuffled decks;
- the ledger by replaying fills into cash and position, with edge and inventory terms summed separately;
- the acquirer's auction by exact summation over a fine grid of company values, and a search over bids;
- second-price bidding by exhaustive comparison of every bid against every rival bid on a grid;
- stopping problems by optimising over every keep-set, and the red-card game by exact dynamic programming;
- the Kelly fraction by a grid search of expected log growth;
- the `./qp drill mm` engine's parameters read from `tools/qp/drills.py`, and its edge-plus-inventory split
  rebuilt from each game's history.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 13-Interview-Playbook/code/interview_05_trading_games.py`.
"""

from __future__ import annotations

import itertools
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.qp.drills import MarketMakingGame  # noqa: E402

SEED = 20261112


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol:.4f})")


def dice() -> None:
    print("Three dice (Example 1, cards int-tg-three-dice-fair-value, int-tg-three-dice-after-reveal)")
    rolls = list(itertools.product(range(1, 7), repeat=3))
    sums = [Fraction(sum(r)) for r in rolls]
    mean = sum(sums) / len(sums)
    var = sum((s - mean) ** 2 for s in sums) / len(sums)
    exact("E[sum]", mean, Fraction(21, 2))
    exact("Var[sum]", var, Fraction(35, 4))
    exact("Var of one die", sum((Fraction(k) - Fraction(7, 2)) ** 2 for k in range(1, 7)) / 6, Fraction(35, 12))
    approx("sd", math.sqrt(var), 2.96, 2)
    given = [Fraction(sum(r)) for r in rolls if r[0] == 5]
    exact("E[sum | first die 5]", sum(given) / len(given), 12)
    given2 = [Fraction(sum(r)) for r in rolls if r[:2] == (5, 2)]
    exact("E[sum | 5 then 2]", sum(given2) / len(given2), Fraction(21, 2))
    for n in range(1, 5):
        for k in range(n + 1):
            outs = list(itertools.product(range(1, 7), repeat=n))
            for seen in itertools.product(range(1, 7), repeat=k):
                cond = [sum(o) for o in outs if o[:k] == seen]
                assert Fraction(sum(cond), len(cond)) == sum(seen) + Fraction(7, 2) * (n - k)
    print("    E[sum | first k revealed] = s + 3.5 (n - k) for every reveal with n <= 4")


def ledger() -> None:
    print("Example 1 ledger, replayed fill by fill")
    fv = [Fraction(21, 2), Fraction(12), Fraction(21, 2), Fraction(13)]  # before round 1, after die 1, after die 2, final
    exact("FV after the 5", Fraction(5) + 2 * Fraction(7, 2), fv[1])
    exact("FV after the 2", Fraction(7) + Fraction(7, 2), fv[2])
    exact("final total 5 + 2 + 6", 5 + 2 + 6, 13)
    # fills: (round, our quantity (+ buy), price)
    fills = [(0, -1, Fraction(23, 2)), (1, +2, Fraction(23, 2))]
    cash, pos = Fraction(0), 0
    positions = []
    for rnd in range(3):
        for r, q, px in fills:
            if r == rnd:
                cash -= q * px
                pos += q
        positions.append(pos)
        if rnd == 0:
            exact("position after round 0", pos, -1)
            exact("cash after round 0", cash, Fraction(23, 2))
            exact("mark P&L after die 1", cash + pos * fv[1], Fraction(-1, 2))
        if rnd == 1:
            exact("position after round 1", pos, 1)
            exact("cash after round 1", cash, Fraction(-23, 2))
            exact("mark P&L after die 2", cash + pos * fv[2], -1)
    total = cash + pos * fv[3]
    exact("final P&L", total, Fraction(3, 2))
    edges = [(-q) * (px - fv[r]) for r, q, px in fills]
    exact("edge per fill", edges, [1, 1])
    inventory = [positions[i] * (fv[i + 1] - fv[i]) for i in range(3)]
    exact("inventory terms", inventory, [Fraction(-3, 2), Fraction(-3, 2), Fraction(5, 2)])
    exact("edge total", sum(edges), 2)
    exact("inventory total", sum(inventory), Fraction(-1, 2))
    exact("edge + inventory equals the cash replay", sum(edges) + sum(inventory), total)
    exact("quotes skewed around 12.5 and 10", (Fraction(23 + 27, 4), Fraction(9 + 11, 2)), (Fraction(25, 2), 10))

    print("Ledger card int-tg-ledger-pnl")
    trades = [(+10, 10), (-5, 11), (+5, 12), (-20, Fraction(21, 2))]
    cash = -sum(q * p for q, p in trades)
    pos = sum(q for q, _ in trades)
    exact("cash", cash, 105)
    exact("position", pos, -10)
    exact("P&L at 12", cash + pos * 12, -15)
    exact("shown cash terms", (-100, 55, -60, 210), tuple(-q * p for q, p in trades))


def cards(rng: np.random.Generator) -> None:
    print("Ten cards (Example 2, cards int-tg-ten-cards-fair-value, int-tg-ten-cards-after-king)")
    deck = [v for v in range(1, 14) for _ in range(4)]
    exact("deck total", sum(deck), 364)
    exact("4 x 91", 4 * 91, 364)
    mean = Fraction(sum(deck), 52)
    exact("card mean", mean, 7)
    exact("FV of 10 cards", 10 * mean, 70)
    var1 = sum((Fraction(v) - mean) ** 2 for v in deck) / 52
    exact("variance of one card", var1, 14)
    cov = sum((Fraction(deck[i]) - mean) * (deck[j] - mean) for i in range(52) for j in range(52) if i != j) / (52 * 51)
    exact("covariance of two distinct cards (all ordered pairs)", cov, Fraction(-14, 51))
    var10 = 10 * var1 + 90 * cov
    exact("Var of the 10-card sum", var10, Fraction(10 * 14 * 42, 51))
    approx("Var of the 10-card sum", float(var10), 115.3, 1)
    approx("sd", math.sqrt(var10), 10.7, 1)
    n = 200_000
    draws = np.array([rng.permutation(deck)[:10] for _ in range(n)])
    s = draws.sum(axis=1)
    simulated("simulated mean", float(s.mean()), 70.0, 4 * 10.74 / math.sqrt(n))
    simulated("simulated sd", float(s.std()), 10.737, 4 * 10.74 / math.sqrt(2 * n))
    rest = list(deck)
    rest.remove(13)
    exact("remaining average after a King", Fraction(sum(rest), 51), Fraction(351, 51))
    exact("364 - 13", 364 - 13, 351)
    fv_k = 13 + 9 * Fraction(sum(rest), 51)
    exact("FV after a King", fv_k, Fraction(1274, 17))
    approx("FV after a King", float(fv_k), 74.94, 2)
    exact("naive 13 + 63", 13 + 9 * 7, 76)
    kings = draws[draws[:, 0] == 13].sum(axis=1)
    se = 10.7 / math.sqrt(len(kings))
    simulated("simulated FV given first card King", float(kings.mean()), float(fv_k), 4 * se)


def auctions() -> None:
    print("Acquirer's auction (Example 3, card int-tg-acquirer-auction)")
    grid = [Fraction(k, 100) for k in range(10_000)]  # V on a 0.01 grid of [0, 100), midpoint-free exact sums

    def profit(b: Fraction) -> Fraction:
        return sum((Fraction(3, 2) * v - b for v in grid if v <= b), Fraction(0)) / len(grid)

    for b in (Fraction(20), Fraction(50), Fraction(75), Fraction(100)):
        p = profit(b)
        closed = -(b**2) / 400
        assert abs(p - closed) < Fraction(1, 50), (b, float(p), float(closed))
        print(f"    profit at bid {b}: grid {float(p):.3f}, -b^2/400 = {float(closed):.3f}")
    exact("-75^2/400", -Fraction(75**2, 400), Fraction(-225, 16))
    for b in (Fraction(120), Fraction(150)):
        exact(f"profit at bid {b} (always accepted)", profit(b), Fraction(3, 2) * sum(grid, Fraction(0)) / len(grid) - b)
        assert abs(profit(b) - (75 - b)) < Fraction(1, 50)
    print("    a bid above 100 loses about b - 75")
    bids = [Fraction(k, 2) for k in range(0, 301)]
    best = max(bids, key=lambda b: (sum((Fraction(3, 2) * v - b for v in grid[::20] if v <= b), Fraction(0)), -b))
    exact("best bid on a grid of 0 to 150", best, 0)
    exact("value if accepted at b: E[1.5 V | V <= b] / b", Fraction(3, 2) * Fraction(1, 2), Fraction(3, 4))
    exact("naive 1.5 x 50", Fraction(3, 2) * 50, 75)

    print("Second-price auction (card int-tg-vickrey-bid), every bid against every rival bid")
    for v, b, h in itertools.product(range(11), repeat=3):

        def pay(bid: int, val: int = v, rival: int = h) -> Fraction:
            if bid > rival:
                return Fraction(val - rival)
            if bid == rival:
                return Fraction(val - rival, 2)  # tie broken by a fair coin
            return Fraction(0)

        assert pay(v) >= pay(b)
    print("    truthful bidding is weakly dominant on the 11 x 11 x 11 grid")


def stopping() -> None:
    print("Re-roll games (Example 4, cards int-tg-dice-reroll-two, int-tg-dice-reroll-three), every keep-set")

    def best_value(cont: Fraction) -> tuple[Fraction, tuple[int, ...]]:
        best = (Fraction(-1), ())
        for r in range(7):
            for keep in itertools.combinations(range(1, 7), r):
                val = sum((Fraction(k, 6) for k in keep), Fraction(0)) + Fraction(6 - r, 6) * cont
                best = max(best, (val, keep))
        return best

    one = Fraction(7, 2)
    two, keep2 = best_value(one)
    exact("one roll", one, Fraction(7, 2))
    exact("two rolls", two, Fraction(17, 4))
    exact("keep set with two rolls", keep2, (4, 5, 6))
    three, keep3 = best_value(two)
    exact("three rolls", three, Fraction(14, 3))
    exact("keep set with three rolls", keep3, (5, 6))
    approx("three rolls", float(three), 4.67, 2)

    print("Red card game (card int-tg-red-card-stopping), exact DP")
    v = {}
    for r in range(27):
        for b in range(27):
            if r + b == 0:
                continue
            now = Fraction(r, r + b)
            wait = Fraction(0)
            if r:
                wait += Fraction(r, r + b) * v.get((r - 1, b), Fraction(0))
            if b:
                wait += Fraction(b, r + b) * v.get((r, b - 1), Fraction(0))
            if r + b == 1:
                wait = now  # must call on the last card
            v[(r, b)] = max(now, wait)
            assert v[(r, b)] == now
    exact("optimal win probability from a full deck", v[(26, 26)], Fraction(1, 2))

    print("Kelly (Example 4, card int-tg-kelly-sixty-forty), grid search")
    f = np.linspace(0, 0.99, 99_001)
    g = 0.6 * np.log1p(f) + 0.4 * np.log1p(-f)
    approx("argmax f", float(f[np.argmax(g)]), 0.2, 4)
    exact("p - q", Fraction(6, 10) - Fraction(4, 10), Fraction(1, 5))
    approx("growth per bet at f = 0.2", 0.6 * math.log(1.2) + 0.4 * math.log(0.8), 0.0201, 4)


def drill(rng: random.Random) -> None:
    print("./qp drill mm engine (tools/qp/drills.py)")
    g = MarketMakingGame(seed=1)
    exact("hidden dice", g.n_dice, 4)
    exact("max width", g.max_width, 4)
    exact("probability a counterparty is informed", g.p_informed, 0.5)
    exact("contracts per fill", g.lot, 10)
    for seed in range(300):
        game = MarketMakingGame(seed=seed)
        fvs = []
        while not game.finished:
            fv = game.fair_value
            fvs.append(fv)
            mid = int(fv) + rng.choice((-2, -1, 0, 1, 2))
            w = rng.randint(1, 4)
            game.quote(mid - w // 2, mid - w // 2 + w)
        fvs.append(Fraction(game.total))
        edge = Fraction(0)
        inventory = Fraction(0)
        pos = 0
        for i, h in enumerate(game.history):
            t = h["trade"]
            if t:
                sign = 1 if t["side"] == "sell" else -1
                edge += sign * (t["price"] - fvs[i]) * t["qty"]
                pos += -sign * t["qty"]
            inventory += pos * (fvs[i + 1] - fvs[i])
        summary = game.summary()
        assert edge + inventory == game.pnl()
        assert math.isclose(summary["edge_at_fill"], float(edge), abs_tol=0.01)
        assert math.isclose(summary["adverse_and_inventory"], float(inventory), abs_tol=0.01)
    print("    over 300 seeded games the engine's edge and remainder equal the edge and inventory sums rebuilt here")


def main() -> None:
    rng = np.random.default_rng(SEED)
    dice()
    ledger()
    cards(rng)
    auctions()
    stopping()
    drill(random.Random(SEED))
    print("All trading-game checks passed.")


if __name__ == "__main__":
    main()
