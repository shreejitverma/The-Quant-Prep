"""Brainteasers: every answer in the note, checked by brute force, exact search or seeded simulation.

Backs every number in `13-Interview-Playbook/03-Brainteasers-and-Puzzles.md`.
Independent routes used here, never the closed form the note quotes:
- weighing puzzles: the note's decision trees replayed against every possible fake coin, plus an exhaustive
  search over adaptive weighing strategies (Dyson's state space) for the maximum number of coins;
- pirates: full enumeration of every allocation of 100 coins at every stage of the backward induction;
- hats: every deterministic strategy for 3 prisoners, and the parity strategy on seeded random lines of 100;
- egg drop, Nim, staircase and coins-in-a-row: dynamic programming or minimax over every position;
- chameleons, jugs and the bridge: breadth-first or shortest-path search over every reachable state;
- the mutilated chessboard: a broken-profile count of domino tilings (12,988,816 for the full board, 0 mutilated);
- ants and ropes: event-driven simulation with real collisions and random burn profiles;
- counting answers (lockers, zeros, squares, rectangles, daughters, clocks, Frobenius): direct enumeration.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 13-Interview-Playbook/code/interview_03_brainteasers.py`.
"""

from __future__ import annotations

import heapq
import itertools
import math
import random
from collections import deque
from fractions import Fraction
from functools import cache

import numpy as np

SEED = 20261112


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


# ------------------------------------------------------------------ weighing


def balance(left: list[int], right: list[int], fake: int, delta: int) -> int:
    """+1 if the left pan is heavier, -1 if lighter, 0 if balanced; coin `fake` weighs 1 + delta."""

    def w(pan: list[int]) -> int:
        return sum(1 + (delta if c == fake else 0) for c in pan)

    return (w(left) > w(right)) - (w(left) < w(right))


def twelve_coin_tree(fake: int, delta: int) -> tuple[int, int, int]:
    """The note's three-weighing procedure; returns (coin, direction, weighings used)."""
    used = 0

    def weigh(a: list[int], b: list[int]) -> int:
        nonlocal used
        used += 1
        return balance(a, b, fake, delta)

    first = weigh([1, 2, 3, 4], [5, 6, 7, 8])
    if first == 0:
        r = weigh([9, 10, 11], [1, 2, 3])
        if r == 0:
            return 12, weigh([12], [1]), used
        r2 = weigh([9], [10])
        if r2 == 0:
            return 11, r, used
        # r = +1 means one of 9, 10, 11 is heavy, so the heavier of 9 and 10 is fake (mirror if light)
        return (9 if r2 == r else 10), r, used
    heavy_side, light_side = ([1, 2, 3, 4], [5, 6, 7, 8]) if first == 1 else ([5, 6, 7, 8], [1, 2, 3, 4])
    h1, h2, h3, h4 = heavy_side
    l1, l2, l3, l4 = light_side
    r = weigh([h1, h2, l1], [h3, l2, 9])
    if r == 0:  # h4 heavy, l3 light or l4 light
        r2 = weigh([l3], [l4])
        if r2 == 0:
            return h4, +1, used
        return (l3 if r2 == -1 else l4), -1, used
    if r == 1:  # h1 heavy, h2 heavy or l2 light
        r2 = weigh([h1], [h2])
        if r2 == 0:
            return l2, -1, used
        return (h1 if r2 == 1 else h2), +1, used
    # right heavy: h3 heavy or l1 light
    r2 = weigh([h3], [9])
    return (h3, +1, used) if r2 == 1 else (l1, -1, used)


@cache
def solvable(u: int, h: int, lt: int, g: int, w: int) -> bool:
    """Can w weighings identify the fake and its direction?

    u coins may be heavy or light, h only heavy, lt only light, g are known genuine.
    Exhaustive over every placement of each class on each pan, with genuine coins used only to balance counts.
    """
    cases = 2 * u + h + lt
    if cases <= 1:
        return True
    if cases > 3**w:
        return False
    for u1 in range(u + 1):
        for u2 in range(u - u1 + 1):
            for h1 in range(h + 1):
                for h2 in range(h - h1 + 1):
                    for l1 in range(lt + 1):
                        for l2 in range(lt - l1 + 1):
                            left, right = u1 + h1 + l1, u2 + h2 + l2
                            if left + right == 0 or abs(left - right) > g:
                                continue
                            heavy_left = (0, u1 + h1, u2 + l2)
                            heavy_right = (0, u2 + h2, u1 + l1)
                            bal = (u - u1 - u2, h - h1 - h2, lt - l1 - l2)
                            g_bal = min(g + left + right, 13)
                            g_unb = min(g + (u - u1 - u2) + (h - h1 - h2) + (lt - l1 - l2), 13)
                            if (
                                solvable(*bal, g_bal, w - 1)
                                and solvable(*heavy_left, g_unb, w - 1)
                                and solvable(*heavy_right, g_unb, w - 1)
                            ):
                                return True
    return False


def max_coins(w: int) -> int:
    """Largest n (searched up to the counting bound 2n <= 3^w) that w weighings can resolve with no spare genuine coin."""
    return max(n for n in range(1, 3**w // 2 + 1) if solvable(n, 0, 0, 0, w))


def weighings() -> None:
    print("Twelve coins (Example 1, card int-bt-twelve-coins-three-weighings)")
    exact("cases 12 x 2", 12 * 2, 24)
    exact("outcomes 3^3", 3**3, 27)
    results = [twelve_coin_tree(c, d) for c in range(1, 13) for d in (+1, -1)]
    assert all(res[:2] == (c, d) for res, (c, d) in zip(results, itertools.product(range(1, 13), (+1, -1)), strict=True))
    exact("max weighings used by the tree over all 24 cases", max(r[2] for r in results), 3)
    # the three outcomes of the second weighing in the left-heavy branch split the 8 suspects 3, 3, 2
    suspects = [(c, +1) for c in (1, 2, 3, 4)] + [(c, -1) for c in (5, 6, 7, 8)]
    split = {o: sorted(c * d for c, d in suspects if balance([1, 2, 5], [3, 6, 9], c, d) == o) for o in (0, 1, -1)}
    exact("balanced leaves {4 heavy, 7 light, 8 light}", split[0], [-8, -7, 4])
    exact("left heavy leaves {1 heavy, 2 heavy, 6 light}", split[1], [-6, 1, 2])
    exact("right heavy leaves {3 heavy, 5 light}", split[-1], [-5, 3])
    for w in (2, 3, 4):
        exact(f"max coins in {w} weighings by exhaustive search", max_coins(w), (3**w - 3) // 2)
    exact("(3^3 - 3)/2", (3**3 - 3) // 2, 12)

    print("Eight balls, one heavy (card int-bt-eight-balls-two-weighings)")
    for fake in range(1, 9):
        r = balance([1, 2, 3], [4, 5, 6], fake, 1)
        found = (7 if balance([7], [8], fake, 1) == 1 else 8) if r == 0 else None
        if r != 0:
            group = [1, 2, 3] if r == 1 else [4, 5, 6]
            r2 = balance([group[0]], [group[1]], fake, 1)
            found = group[0] if r2 == 1 else group[1] if r2 == -1 else group[2]
        assert found == fake
    exact("weighings needed, lower bound ceil(log3 8)", math.ceil(math.log(8, 3)), 2)
    exact("one weighing distinguishes only 3 < 8 cases", 3**1 < 8, True)


# ------------------------------------------------------------------ pirates


def pirate_plan(n: int, coins: int = 100) -> tuple[int, ...]:
    """Best plan for the most senior of n pirates by enumerating every allocation (indifferent voters vote no)."""
    if n == 1:
        return (coins,)
    cont = (0, *pirate_plan(n - 1, coins))  # payoff to each pirate if the proposer is thrown overboard (proposer gets 0)
    need = math.ceil(n / 2)
    best: list[tuple[int, ...]] = []
    best_own = -1
    # enumerate every allocation to the n-1 others with numpy over the last coordinate
    for prefix in itertools.product(range(coins + 1), repeat=max(n - 2, 0)):
        rest = coins - sum(prefix)
        if rest < 0:
            continue
        last = np.arange(rest + 1)
        own = rest - last
        yes = 1 + sum(int(prefix[i] > cont[i + 1]) for i in range(n - 2)) + (last > cont[n - 1])
        ok = yes >= need
        if not ok.any():
            continue
        top = int(own[ok].max())
        if top > best_own:
            best_own, best = top, []
        if top == best_own:
            for k in np.flatnonzero(ok & (own == top)):
                best.append((top, *prefix, int(last[k])))
    assert len(best) == 1, (n, best[:5])
    return best[0]


def pirates() -> None:
    print("Pirates (Example 2, card int-bt-five-pirates), every allocation enumerated")
    exact("2 pirates", pirate_plan(2), (100, 0))
    exact("3 pirates", pirate_plan(3), (99, 0, 1))
    exact("4 pirates", pirate_plan(4), (99, 0, 1, 0))
    exact("5 pirates", pirate_plan(5), (98, 0, 1, 0, 1))


# ------------------------------------------------------------------ hats


def hats(rng: random.Random) -> None:
    print("Hats in a line (Example 3, card int-bt-hats-in-a-line)")
    # three prisoners: back sees (m, f), middle sees f and hears back, front hears both; search every strategy
    best = 0
    tables = list(itertools.product((0, 1), repeat=4))
    for sb, sm, sf in itertools.product(tables, repeat=3):
        worst = 3
        for b, m, f in itertools.product((0, 1), repeat=3):
            cb = sb[2 * m + f]
            cm = sm[2 * f + cb]
            cf = sf[2 * cb + cm]
            worst = min(worst, (cb == b) + (cm == m) + (cf == f))
        best = max(best, worst)
    exact("best guaranteed for 3 prisoners over all 4096 strategies", best, 2)
    n, trials, saved_min, back_saved = 100, 5_000, 100, 0
    for _ in range(trials):
        line = [rng.randint(0, 1) for _ in range(n)]  # index 0 is the back
        ahead = list(itertools.accumulate(reversed(line)))[::-1] + [0]  # ahead[i] = black hats at positions >= i
        calls = [ahead[1] % 2]
        heard = 0  # calls of everyone between the back and me, all correct under the strategy
        for i in range(1, n):
            calls.append((calls[0] - ahead[i + 1] - heard) % 2)
            heard += calls[-1]
        saved_min = min(saved_min, sum(c == h for c, h in zip(calls[1:], line[1:], strict=True)))
        back_saved += calls[0] == line[0]
    exact("prisoners 2..100 saved in every one of 5,000 seeded lines", saved_min, 99)
    p = back_saved / trials
    se = math.sqrt(0.25 / trials)
    assert abs(p - 0.5) < 4 * se, p
    print(f"    back prisoner saved ~ {p:.4f} (quoted 1/2, tolerance {4 * se:.4f})")


# ------------------------------------------------------------------ eggs


def eggs() -> None:
    print("Two eggs, 100 floors (Example 4, card int-bt-two-eggs-100-floors)")

    @cache
    def drops(floors: int, eggs_left: int) -> int:
        if floors == 0:
            return 0
        if eggs_left == 1:
            return floors
        return 1 + min(max(drops(x - 1, eggs_left - 1), drops(floors - x, eggs_left)) for x in range(1, floors + 1))

    exact("minimum worst-case drops by DP over every first drop", drops(100, 2), 14)
    exact("13*14/2 and 14*15/2", (13 * 14 // 2, 14 * 15 // 2), (91, 105))
    starts, f, step = [], 0, 14
    while f < 100:
        f = min(f + step, 100)
        starts.append(f)
        step -= 1
    exact("first-egg floors", starts, [14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100])
    worst = 0
    for critical in range(0, 101):  # highest safe floor
        used, prev = 0, 0
        for s in starts:
            used += 1
            if s > critical:  # breaks: scan prev+1 .. s-1 with the second egg
                used += min(critical - prev + 1, s - 1 - prev)
                break
            prev = s
        worst = max(worst, used)
    exact("worst case of that schedule over every critical floor", worst, 14)


# ------------------------------------------------------------------ chameleons


def chameleons() -> None:
    print("Chameleons (Example 5, card int-bt-chameleons)")
    start = (13, 15, 17)
    exact("pairwise differences", (15 - 13, 17 - 13, 17 - 15), (2, 4, 2))
    exact("differences mod 3", ((15 - 13) % 3, (17 - 13) % 3, (17 - 15) % 3), (2, 1, 2))
    seen, queue = {start}, deque([start])
    while queue:
        s = queue.popleft()
        for i, j in ((0, 1), (0, 2), (1, 2)):
            if s[i] and s[j]:
                t = list(s)
                t[i] -= 1
                t[j] -= 1
                t[3 - i - j] += 2
                t = tuple(t)
                if t not in seen:
                    seen.add(t)
                    queue.append(t)
    mono = [s for s in seen if sorted(s)[:2] == [0, 0]]
    print(f"    reachable states = {len(seen)}")
    exact("monochrome states reachable from (13, 15, 17)", mono, [])


# ------------------------------------------------------------------ cards


def tilings(rows: int, cols: int, blocked: set[tuple[int, int]]) -> int:
    """Count domino tilings by a broken-profile DP over cells in row-major order."""
    dp = {0: 1}
    for r in range(rows):
        for c in range(cols):
            nxt: dict[int, int] = {}
            for mask, ways in dp.items():
                bit = 1 << c
                if (r, c) in blocked:
                    if mask & bit:
                        continue
                    nxt[mask] = nxt.get(mask, 0) + ways
                elif mask & bit:  # covered by a vertical domino from above
                    nxt[mask & ~bit] = nxt.get(mask & ~bit, 0) + ways
                else:
                    if r + 1 < rows and (r + 1, c) not in blocked:  # vertical down
                        nxt[mask | bit] = nxt.get(mask | bit, 0) + ways
                    if c + 1 < cols and (r, c + 1) not in blocked and not mask & (bit << 1):  # horizontal right
                        m2 = mask | (bit << 1)
                        # mark the right cell as already covered; it is consumed when the scan reaches it
                        nxt[m2] = nxt.get(m2, 0) + ways
            dp = nxt
    return dp.get(0, 0)


def ants_time(pos: list[int], dirs: list[int], length: int) -> Fraction:
    """Event-driven simulation with real reversals on collision; returns when the last ant falls off."""
    ants = sorted(zip([Fraction(p) for p in pos], dirs, strict=True))
    t = Fraction(0)
    while ants:
        events = []
        for i, (p, d) in enumerate(ants):
            events.append(((length - p) if d == 1 else p, "fall", i))
        for i in range(len(ants) - 1):
            (p, d), (q, e) = ants[i], ants[i + 1]
            if d == 1 and e == -1:
                events.append(((q - p) / 2, "hit", i))
        dt = min(e[0] for e in events)
        t += dt
        ants = [(p + d * dt, d) for p, d in ants]
        for _, _, i in [e for e in events if e[0] == dt and e[1] == "hit"]:
            (p, d), (q, e2) = ants[i], ants[i + 1]
            ants[i], ants[i + 1] = (p, -d), (q, -e2)
        ants = [(p, d) for p, d in ants if 0 < p < length or (p == 0 and d == 1) or (p == length and d == -1)]
    return t


def bridge_min_time(times: tuple[int, ...]) -> int:
    everyone = frozenset(range(len(times)))
    start = (everyone, 0)  # people on the start side, torch side 0
    best = {start: 0}
    heap = [(0, 0, start)]
    counter = 0
    while heap:
        cost, _, (side, torch) = heapq.heappop(heap)
        if not side:
            return cost
        if cost > best[(side, torch)]:
            continue
        here = side if torch == 0 else everyone - side
        for k in (1, 2):
            for group in itertools.combinations(sorted(here), k):
                g = frozenset(group)
                new_side = side - g if torch == 0 else side | g
                state = (new_side, 1 - torch)
                c = cost + max(times[i] for i in group)
                if c < best.get(state, 10**9):
                    best[state] = c
                    counter += 1
                    heapq.heappush(heap, (c, counter, state))
    raise AssertionError("unreachable")


def coins_row_value(vals: list[int]) -> int:
    @cache
    def best(i: int, j: int) -> int:  # best total for the player to move on vals[i..j]
        if i > j:
            return 0
        rest = sum(vals[i : j + 1])
        return rest - min(best(i + 1, j), best(i, j - 1))

    return best(0, len(vals) - 1)


def cards(rng: random.Random) -> None:
    print("Ropes (card int-bt-ropes-45-minutes): random burn profiles")
    for _ in range(200):
        seg = [rng.random() for _ in range(rng.randint(1, 30))]
        scale = 60 / sum(seg)
        seg = [x * scale for x in seg]  # single-flame burn time of each uniform piece
        i, j, a, b, t = 0, len(seg) - 1, 0.0, 0.0, 0.0  # a, b: time already burnt into pieces i and j
        while i < j:
            step = min(seg[i] - a, seg[j] - b)
            t, a, b = t + step, a + step, b + step
            if a >= seg[i] - 1e-12:
                i, a = i + 1, 0.0
            if b >= seg[j] - 1e-12:
                j, b = j - 1, 0.0
        if i == j:
            t += (seg[i] - a - b) / 2  # two flames inside the last piece
        assert abs(t - 30) < 1e-9, t
    print("    a rope lit at both ends finishes at 30 minutes for 200 random profiles; the other then has 30 left, 15 lit at both ends")
    exact("30 + 30/2", 30 + 30 // 2, 45)

    print("Lockers (card int-bt-hundred-lockers)")
    lockers = [False] * 101
    for k in range(1, 101):
        for n in range(k, 101, k):
            lockers[n] = not lockers[n]
    exact("open lockers", [n for n in range(1, 101) if lockers[n]], [k * k for k in range(1, 11)])
    exact("count", sum(lockers), 10)

    print("Trailing zeros of 100! (card int-bt-trailing-zeros-100-factorial)")
    s = str(math.factorial(100))
    exact("trailing zeros by printing 100!", len(s) - len(s.rstrip("0")), 24)
    exact("100//5 + 100//25", (100 // 5, 100 // 25), (20, 4))

    print("Mutilated chessboard (card int-bt-mutilated-chessboard)")
    exact("domino tilings of the full 8x8 board", tilings(8, 8, set()), 12988816)
    exact("domino tilings with opposite corners removed", tilings(8, 8, {(0, 0), (7, 7)}), 0)
    colours = [(r + c) % 2 for r in range(8) for c in range(8) if (r, c) not in {(0, 0), (7, 7)}]
    exact("squares of each colour left", (colours.count(1), colours.count(0)), (32, 30))

    print("Bridge and torch (card int-bt-bridge-and-torch)")
    exact("minimum time by shortest-path search", bridge_min_time((1, 2, 5, 10)), 17)
    exact("2 + 1 + 10 + 2 + 2", 2 + 1 + 10 + 2 + 2, 17)

    print("Jugs 3 and 5 (card int-bt-jugs-3-and-5)")
    a, b = 0, 0
    a, b = a, 5  # fill the 5
    a, b = 3, b - 3  # pour into the 3
    exact("left in the 5 after the first pour", b, 2)
    a = 0  # empty the 3
    a, b = b, 0  # pour the 2 into the 3
    b = 5  # fill the 5
    b -= 3 - a  # top up the 3
    exact("left in the 5 at the end", b, 4)
    reach, q = {(0, 0)}, deque([(0, 0)])
    while q:
        x, y = q.popleft()
        moves = [(3, y), (x, 5), (0, y), (x, 0), (x - min(x, 5 - y), y + min(x, 5 - y)), (x + min(y, 3 - x), y - min(y, 3 - x))]
        for m in moves:
            if m not in reach:
                reach.add(m)
                q.append(m)
    exact("4 litres reachable by search", any(4 in s for s in reach), True)

    print("Poisoned wine (card int-bt-poisoned-wine)")
    for bottle in range(1000):
        ill = [i for i in range(10) if bottle >> i & 1]
        assert sum(1 << i for i in ill) == bottle
    exact("all 1000 bottles decoded uniquely with 10 testers; 2^10", 2**10, 1024)
    exact("9 testers are too few: 2^9 < 1000", 2**9 < 1000, True)

    print("Mislabelled boxes (card int-bt-mislabelled-boxes)")
    contents = ("apples", "oranges", "mixed")
    worlds = [p for p in itertools.permutations(contents) if all(p[i] != contents[i] for i in range(3))]
    exact("arrangements consistent with all labels wrong", len(worlds), 2)
    for w in worlds:
        drawn = w[2]  # draw one fruit from the box labelled mixed; it holds a single type
        assert drawn != "mixed"
        candidates = [v for v in worlds if v[2] == drawn]
        assert candidates == [w]
    print("    drawing from the box labelled mixed identifies the arrangement in both worlds")

    print("Ants on a stick (card int-bt-ants-on-a-stick)")
    for _ in range(300):
        k = rng.randint(1, 12)
        pos = rng.sample(range(1, 100), k)
        dirs = [rng.choice((1, -1)) for _ in range(k)]
        sim = ants_time(pos, dirs, 100)
        through = max((100 - p) if d == 1 else p for p, d in zip(pos, dirs, strict=True))
        assert sim == through, (pos, dirs, sim, through)
    exact("worst case: an ant at 0 cm walking inwards, seconds at 1 cm/s", ants_time([0, 50], [1, -1], 100), 100)

    print("Knockout (card int-bt-knockout-matches)")
    for n in range(1, 130):
        players, matches = n, 0
        while players > 1:
            matches += players // 2
            players = players // 2 + players % 2  # odd player gets a bye
        assert matches == n - 1
    exact("matches for 64 players", 64 - 1, 63)

    print("Light switches (card int-bt-light-switches)")
    for perm in itertools.permutations(range(3)):  # perm[s] = bulb controlled by switch s
        lit = perm[1]
        warm = perm[0]
        observed = {b: ("lit" if b == lit else "warm" if b == warm else "cold") for b in range(3)}
        decoded = {s: next(b for b in range(3) if observed[b] == ("warm", "lit", "cold")[s]) for s in range(3)}
        assert decoded == {s: perm[s] for s in range(3)}
    print("    all 6 wirings decoded")

    print("Heavy pill jar (card int-bt-heavy-pill-jar)")
    exact("baseline grams 10 * (1 + ... + 10)", 10 * sum(range(1, 11)), 550)
    for heavy in range(1, 11):
        weight = sum(k * (11 if k == heavy else 10) for k in range(1, 11))
        assert weight - 550 == heavy

    print("Blindfold coins (card int-bt-coins-blindfold), exhaustive on 12 coins with 4 heads")
    for heads in itertools.combinations(range(12), 4):
        hs = set(heads)
        for pile in itertools.combinations(range(12), 4):
            ps = set(pile)
            after_flip = sum(1 for c in ps if c not in hs)
            other = sum(1 for c in hs if c not in ps)
            assert after_flip == other
    print("    every one of 495 x 495 cases balances")

    print("Handshakes (card int-bt-handshake-parity)")
    for _ in range(500):
        n = rng.randint(1, 15)
        deg = [0] * n
        for i, j in itertools.combinations(range(n), 2):
            if rng.random() < 0.4:
                deg[i] += 1
                deg[j] += 1
        assert sum(d % 2 for d in deg) % 2 == 0
    print("    odd-degree count even on 500 random graphs")

    print("Coins in a row (card int-bt-coins-in-a-row), minimax")
    for _ in range(300):
        n = 2 * rng.randint(1, 6)
        vals = [rng.randint(1, 20) for _ in range(n)]
        v = coins_row_value(vals)
        assert v >= max(sum(vals[0::2]), sum(vals[1::2])) and 2 * v >= sum(vals)
    print("    first player's optimum >= larger parity class >= half, on 300 random rows")

    print("Nim 100, take 1 to 10 (card int-bt-nim-100-take-1-to-10)")
    win = [False] * 101
    for n in range(1, 101):
        win[n] = any(not win[n - t] for t in range(1, 11) if t <= n)
    exact("losing positions up to 100 are the multiples of 11", [n for n in range(101) if not win[n]], list(range(0, 101, 11)))
    exact("winning first takes from 100", [t for t in range(1, 11) if not win[100 - t]], [1])

    print("Frobenius 3 and 5 (card int-bt-frobenius-3-and-5)")
    payable = {3 * i + 5 * j for i in range(40) for j in range(25)}
    exact("largest unpayable amount", max(n for n in range(100) if n not in payable), 7)
    exact("ab - a - b", 3 * 5 - 3 - 5, 7)

    print("Clocks (cards int-bt-clock-overlaps, int-bt-clock-angle-3-15)")
    rel = [((6 * s / 60) - (0.5 * s / 60)) % 360 for s in range(0, 24 * 3600)]  # minute minus hour angle, every second
    wraps = sum(1 for a, b in itertools.pairwise(rel) if b < a) + 1  # overlap at 0:00 plus each wrap
    exact("overlaps in 24 hours, scanned second by second", wraps, 22)
    minute, hour = Fraction(15 * 6), Fraction(3 * 30) + Fraction(15, 2)
    exact("angle at 3:15 in degrees", float(hour - minute), 7.5)

    print("Snail (card int-bt-snail-in-well)")
    h, day = 0, 0
    while True:
        day += 1
        h += 3
        if h >= 30:
            break
        h -= 2
    exact("day out", day, 28)

    print("Train and fly (card int-bt-train-and-fly), summing the zigzag legs")
    gap, total = 100.0, 0.0
    for _ in range(200):
        t = gap / (75 + 50)  # fly meets the oncoming train
        total += 75 * t
        gap -= 100 * t  # both trains closed for time t
    exact("miles flown (rounded)", round(total, 9), 75.0)

    print("Daughters (card int-bt-three-daughters-ages)")
    triples = [t for t in itertools.combinations_with_replacement(range(1, 37), 3) if math.prod(t) == 36]
    sums: dict[int, list[tuple[int, ...]]] = {}
    for t in triples:
        sums.setdefault(sum(t), []).append(t)
    ambiguous = {s: ts for s, ts in sums.items() if len(ts) > 1}
    exact("ambiguous sums", ambiguous, {13: [(1, 6, 6), (2, 2, 9)]})
    exact("unique eldest", [t for t in ambiguous[13] if t[2] > t[1]], [(2, 2, 9)])

    print("Last digit of 7^2026 (card int-bt-last-digit-7-power)")
    exact("pow(7, 2026, 10)", pow(7, 2026, 10), 9)
    exact("cycle of last digits", [pow(7, k, 10) for k in range(1, 5)], [7, 9, 3, 1])
    exact("2026 mod 4", 2026 % 4, 2)

    print("Chessboard counts (cards int-bt-squares-on-chessboard, int-bt-rectangles-on-chessboard)")
    sq = sum(1 for k in range(1, 9) for r in range(9 - k) for c in range(9 - k))
    rect = sum(1 for r1, r2 in itertools.combinations(range(9), 2) for c1, c2 in itertools.combinations(range(9), 2))
    exact("squares by placement", sq, 204)
    exact("rectangles by choosing lines", rect, 1296)
    exact("C(9,2)^2", math.comb(9, 2) ** 2, 36**2)

    print("Truth teller and liar (card int-bt-truth-liar-guards)")
    for liar, safe in itertools.product((0, 1), repeat=2):
        for asked in (0, 1):
            other = 1 - asked
            other_says = safe if other != liar else 1 - safe
            reply = other_says if asked != liar else 1 - other_says
            assert 1 - reply == safe
    print("    taking the other door is right in all 8 cases")

    print("Staircase (card int-bt-staircase-one-or-two)")
    ways = sum(1 for k in range(11) for steps in itertools.product((1, 2), repeat=k) if sum(steps) == 10)
    exact("compositions of 10 into 1s and 2s", ways, 89)


def main() -> None:
    rng = random.Random(SEED)
    weighings()
    pirates()
    hats(rng)
    eggs()
    chameleons()
    cards(rng)
    print("All brainteaser checks passed.")


if __name__ == "__main__":
    main()
