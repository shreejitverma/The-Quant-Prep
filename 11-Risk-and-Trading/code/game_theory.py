"""Game theory for traders: equilibria, auctions, the winner's curse, bargaining, repeated games and puzzles.

Backs every number in ``07-Game-Theory-for-Traders.md``.
Run ``uv run --no-project --with numpy python 11-Risk-and-Trading/code/game_theory.py``;
each printed number is asserted, so drift in the note fails CI.
Simulations use fixed seeds and the note quotes them as "about".
"""

from __future__ import annotations

import itertools
import math

import numpy as np


def check(name: str, value: float, expected: float, tol: float) -> float:
    """Print a named result and assert it is within ``tol`` of the value quoted in the note."""
    print(f"{name:<68s} {value:12.4f}")
    assert abs(value - expected) <= tol, f"{name}: got {value}, expected {expected} +/- {tol}"
    return value


# ---------------------------------------------------------------- 1. Nash equilibria by support enumeration


def support_enumeration(a: np.ndarray, b: np.ndarray, tol: float = 1e-9) -> list[tuple[np.ndarray, np.ndarray]]:
    """All Nash equilibria of a nondegenerate bimatrix game (row payoffs a, column payoffs b) with equal-size supports."""
    m, n = a.shape
    found = []
    for k in range(1, min(m, n) + 1):
        for rows in itertools.combinations(range(m), k):
            for cols in itertools.combinations(range(n), k):
                # column mix y on cols makes the row player indifferent across rows: a[rows, cols] y = u 1, sum y = 1
                lhs = np.zeros((k + 1, k + 1))
                lhs[:k, :k] = a[np.ix_(rows, cols)]
                lhs[:k, k] = -1.0
                lhs[k, :k] = 1.0
                rhs = np.zeros(k + 1)
                rhs[k] = 1.0
                lhs2 = np.zeros((k + 1, k + 1))
                lhs2[:k, :k] = b[np.ix_(rows, cols)].T
                lhs2[:k, k] = -1.0
                lhs2[k, :k] = 1.0
                try:
                    sy = np.linalg.solve(lhs, rhs)
                    sx = np.linalg.solve(lhs2, rhs)
                except np.linalg.LinAlgError:
                    continue
                y, u = sy[:k], sy[k]
                x, v = sx[:k], sx[k]
                if np.any(x < -tol) or np.any(y < -tol):
                    continue
                xf = np.zeros(m)
                yf = np.zeros(n)
                xf[list(rows)] = x
                yf[list(cols)] = y
                # no profitable deviation outside the support
                if np.max(a @ yf) > u + tol or np.max(xf @ b) > v + tol:
                    continue
                found.append((xf, yf))
    return found


def section_nash() -> None:
    """Backs Examples 1 and 2 and cards risk-game-battle-sexes, risk-game-hawk-dove, risk-game-bertrand-tick."""
    print("\n1. Nash equilibria")
    # prisoner's dilemma, strategies (cooperate, defect), payoffs R = 3, S = 0, T = 5, P = 1
    pd_a = np.array([[3.0, 0.0], [5.0, 1.0]])
    eqs = support_enumeration(pd_a, pd_a.T)
    assert len(eqs) == 1 and eqs[0][0][1] == 1.0 and eqs[0][1][1] == 1.0
    check("prisoner's dilemma: number of equilibria (defect, defect)", len(eqs), 1, 0)
    # matching pennies
    mp = np.array([[1.0, -1.0], [-1.0, 1.0]])
    eqs = support_enumeration(mp, -mp)
    check("matching pennies: P(heads) in the unique equilibrium", eqs[0][0][0], 0.5, 1e-12)
    # battle of the sexes: (2,1) and (1,2) on the diagonal
    bos_a = np.array([[2.0, 0.0], [0.0, 1.0]])
    bos_b = np.array([[1.0, 0.0], [0.0, 2.0]])
    eqs = support_enumeration(bos_a, bos_b)
    check("battle of the sexes: number of equilibria", len(eqs), 3, 0)
    mixed = [e for e in eqs if 0 < e[0][0] < 1][0]
    check("battle of the sexes mixed: row plays first action with prob", mixed[0][0], 2 / 3, 1e-12)
    check("battle of the sexes mixed: row payoff", float(mixed[0] @ bos_a @ mixed[1]), 2 / 3, 1e-12)
    # hawk-dove with prize V = 4, fight cost C = 6: (hawk, dove)
    v, c = 4.0, 6.0
    hd = np.array([[(v - c) / 2, v], [0.0, v / 2]])
    eqs = support_enumeration(hd, hd.T)
    sym = [e for e in eqs if 0 < e[0][0] < 1][0]
    check("hawk-dove: P(hawk) in the symmetric equilibrium = V / C", sym[0][0], 0.6667, 5e-5)
    # weighted rock-paper-scissors, zero-sum: rock beats scissors for 2, other wins 1
    rps = np.array([[0.0, -1.0, 2.0], [1.0, 0.0, -1.0], [-2.0, 1.0, 0.0]])
    eqs = support_enumeration(rps, -rps)
    x = eqs[0][0]
    check("weighted RPS: P(rock)", x[0], 0.25, 1e-12)
    check("weighted RPS: P(paper)", x[1], 0.5, 1e-12)
    check("weighted RPS: P(scissors)", x[2], 0.25, 1e-12)
    check("weighted RPS: game value", float(x @ rps @ eqs[0][1]), 0.0, 1e-12)
    # Bertrand on a tick grid: prices 1..5 ticks, cost 1 tick, 10 lots go to the lower quote, split on ties
    prices = range(1, 6)
    profit = np.zeros((5, 5))
    for i, p in enumerate(prices):
        for j, q in enumerate(prices):
            share = 10.0 if p < q else (5.0 if p == q else 0.0)
            profit[i, j] = (p - 1) * share
    pure = [
        (p, q)
        for i, p in enumerate(prices)
        for j, q in enumerate(prices)
        if profit[i, j] >= profit[:, j].max() - 1e-12 and profit[j, i] >= profit[:, i].max() - 1e-12
    ]
    print("    Bertrand pure equilibria (price ticks):", pure)
    assert pure == [(1, 1), (2, 2), (3, 3)]
    check("Bertrand: highest equilibrium price (ticks)", max(p for p, _ in pure), 3, 0)
    check("Bertrand: profit per player at the (3, 3) equilibrium", profit[2, 2], 10.0, 1e-12)
    check("Bertrand: profit from undercutting (3, 3) to 2 ticks", profit[1, 2], 10.0, 1e-12)


# ---------------------------------------------------------------- 2. auctions with private values


def section_auctions() -> None:
    """Backs Example 3 and cards risk-game-first-price-shade, risk-game-reserve."""
    print("\n2. independent private values, uniform on [0, 1]")
    rng = np.random.default_rng(42)
    surplus = 0.0
    quoted = {2: 0.3333, 5: 0.6666}  # seed-42 simulated revenues as quoted in Example 3
    for n, rev in ((2, 1 / 3), (5, 2 / 3)):
        vals = rng.random((400_000, n))
        srt = np.sort(vals, axis=1)
        first = float(np.mean(srt[:, -1] * (n - 1) / n))
        second = float(np.mean(srt[:, -2]))
        check(f"n = {n}: revenue formula (n - 1)/(n + 1)", (n - 1) / (n + 1), rev, 1e-12)
        check(f"n = {n}: simulated first-price revenue (seed 42)", first, rev, 0.002)
        check(f"n = {n}: simulated second-price revenue (seed 42)", second, rev, 0.002)
        check(f"n = {n}: simulated first-price revenue, as quoted (seed 42)", first, quoted[n], 5e-5)
        check(f"n = {n}: simulated second-price revenue, as quoted (seed 42)", second, quoted[n], 5e-5)
        if n == 2:
            surplus = float(np.mean(srt[:, -1])) - second
    check("n = 2: simulated winner surplus E[max] - revenue (seed 42)", surplus, 1 / 3, 0.002)
    check("n = 2: ex-ante surplus per bidder 1 / (n (n + 1))", 1 / (2 * 3), surplus / 2, 0.001)
    # best response in a two-bidder first-price auction against b(v) = v / 2, own value 0.8
    grid = np.linspace(0, 1, 100_001)
    win = np.minimum(2 * grid, 1.0)  # P(opponent bid v'/2 < b) = P(v' < 2b)
    check("best first-price bid at value 0.8 against b(v) = v/2", float(grid[np.argmax((0.8 - grid) * win)]), 0.4, 1e-9)
    # optimal reserve for uniform values (Myerson): r = 1/2; two-bidder second-price revenue 5/12
    vals = rng.random((1_000_000, 2))
    hi, lo = vals.max(1), vals.min(1)
    rev_r = np.where(hi < 0.5, 0.0, np.maximum(lo, 0.5))
    check("two bidders, reserve 1/2: simulated revenue (seed 42)", float(rev_r.mean()), 0.4167, 0.002)
    check("two bidders, reserve 1/2: simulated revenue, as quoted (seed 42)", float(rev_r.mean()), 0.4165, 5e-5)
    rs = np.linspace(0, 1, 1001)
    exact = 1 / 3 + rs**2 - 4 * rs**3 / 3  # E[revenue] with reserve r, two uniform bidders
    for r in (0.0, 0.25, 0.75):
        sim_r = np.where(hi < r, 0.0, np.maximum(lo, r)).mean()
        assert abs(sim_r - (1 / 3 + r**2 - 4 * r**3 / 3)) < 0.002
    check("revenue-maximising reserve from the exact curve", float(rs[int(np.argmax(exact))]), 0.5, 1e-9)
    check("maximum revenue on the exact curve (5/12)", float(exact.max()), 0.4167, 5e-5)


# ---------------------------------------------------------------- 3. winner's curse


def expected_max_normal(n: int) -> float:
    """E[max of n iid N(0,1)] by numerical integration of 1 - F(x)^n minus F(x)^n tails."""
    x = np.linspace(-10, 10, 400_001)
    cdf = 0.5 * (1 + np.vectorize(math.erf)(x / math.sqrt(2)))
    pdf = np.exp(-(x**2) / 2) / math.sqrt(2 * math.pi)
    return float(np.trapezoid(x * n * cdf ** (n - 1) * pdf, x))


def section_winners_curse() -> None:
    """Backs Examples 4 and 5 and cards risk-game-winners-curse, risk-game-acquire-company, risk-game-rfq-curse."""
    print("\n3. winner's curse")
    # acquire-a-company: V ~ U[0, 100], worth 1.5 V to the buyer, seller accepts iff b >= V
    for b, expected in ((60.0, -9.0), (100.0, -25.0)):
        ev = (b / 100) * (1.5 * b / 2 - b)
        check(f"acquire-a-company expected profit of bid {b:.0f}", ev, expected, 1e-12)
    rng = np.random.default_rng(7)
    v = rng.uniform(0, 100, 2_000_000)
    sim = float(np.mean(np.where(v <= 60, 1.5 * v - 60, 0.0)))
    check("simulated profit of bid 60 (seed 7)", sim, -9.0, 0.05)
    check("simulated profit of bid 60, as quoted (seed 7)", sim, -9.0031, 5e-5)
    check("unconditional naive value of the target 1.5 x 50", 1.5 * float(np.mean(v)), 75.0, 0.05)
    # common value, signals V + U[-a, a], n bidders; the winner holds the highest signal
    a, n = 10.0, 5
    shade = check("E[max of 5 uniform errors on [-10, 10]] = a (n-1)/(n+1)", a * (n - 1) / (n + 1), 6.6667, 5e-5)
    vv = rng.uniform(1000, 2000, 400_000)
    sig = vv[:, None] + rng.uniform(-a, a, (400_000, n))
    loss = float(np.mean(sig.max(1) - vv))
    check("simulated overpayment when bidding your signal (seed 7)", loss, shade, 0.03)
    check("simulated overpayment, printed (seed 7)", loss, 6.6615, 5e-4)
    # RFQ: n dealers with N(0, sigma) valuation errors; the most aggressive quote wins
    em5 = check("E[max of 5 standard normals]", expected_max_normal(5), 1.1630, 5e-5)
    check("E[max of 2 standard normals] = 1 / sqrt(pi)", expected_max_normal(2), 1 / math.sqrt(math.pi), 1e-6)
    check("RFQ, 5 dealers, error sd 4 cents: expected winner's curse (cents)", 4 * em5, 4.6519, 5e-4)
    z = rng.standard_normal((400_000, 5))
    check("simulated E[max of 5 normals] (seed 7)", float(z.max(1).mean()), 1.1633, 5e-4)


# ---------------------------------------------------------------- 4. bargaining


def section_bargaining() -> None:
    """Backs Example 6 and cards risk-game-rubinstein, risk-game-nash-bargaining."""
    print("\n4. bargaining")
    d1 = d2 = 0.9
    share = check("Rubinstein proposer share (1 - d2)/(1 - d1 d2), d = 0.9", (1 - d2) / (1 - d1 * d2), 0.5263, 5e-5)
    # finite-horizon backward induction converges to the same share
    x = 1.0  # last proposer takes everything
    for _ in range(400):
        x = 1 - d2 * x  # symmetric discounting
    check("backward induction over 400 rounds", x, share, 1e-9)
    check("Rubinstein share, proposer patient d1 = 0.95, responder d2 = 0.8", (1 - 0.8) / (1 - 0.95 * 0.8), 0.8333, 5e-5)
    # Nash bargaining over 100 with disagreement payoffs 20 and 10
    grid = np.linspace(20, 90, 700_001)
    check("Nash bargaining split to player 1 (S + d1 - d2)/2", float(grid[np.argmax((grid - 20) * (90 - grid))]), 55.0, 1e-6)


# ---------------------------------------------------------------- 5. repeated games


def section_repeated() -> None:
    """Backs Example 7 and card risk-game-grim-trigger."""
    print("\n5. repeated prisoner's dilemma, T = 5, R = 3, P = 1, S = 0")
    t, r, p, s = 5.0, 3.0, 1.0, 0.0
    grim = check("grim trigger threshold (T - R)/(T - P)", (t - r) / (t - p), 0.5, 1e-12)
    for d in (0.4, 0.6):
        coop = r / (1 - d)
        dev = t + d * p / (1 - d)
        assert (coop >= dev) == (d >= grim)
    # find the threshold numerically from the present values
    ds = np.linspace(0.01, 0.99, 98_001)
    ok = ds[r / (1 - ds) >= t + ds * p / (1 - ds) - 1e-12]
    check("grim trigger threshold by scanning discount factors", float(ok.min()), 0.5, 1e-4)
    check("tit-for-tat one-shot deviation threshold (T - R)/(R - S)", (t - r) / (r - s), 0.6667, 5e-5)
    ok = ds[r + ds * r >= t + ds * s - 1e-12]
    check("tit-for-tat threshold by scanning", float(ok.min()), 0.6667, 1e-4)


# ---------------------------------------------------------------- 6. interview puzzles


def pirates(n: int, coins: int = 100) -> list[int]:
    """Backward induction: most senior proposes, passes with at least half the votes (proposer votes yes)."""
    alloc = [coins]  # one pirate keeps everything
    for k in range(2, n + 1):
        need = math.ceil(k / 2) - 1  # extra votes the proposer must buy
        prev = alloc  # allocation if the proposer is thrown overboard (pirates 2..k)
        order = sorted(range(k - 1), key=lambda i: prev[i])  # cheapest voters first
        new = [0] * (k - 1)
        for i in order[:need]:
            new[i] = prev[i] + 1
        alloc = [coins - sum(new)] + new
    return alloc


def section_puzzles() -> None:
    """Backs Example 8 and cards risk-game-two-thirds, risk-game-pirates, risk-game-bluff-ratio."""
    print("\n6. puzzles")
    k = 0
    while 100 * (2 / 3) ** k >= 1:
        k += 1
    check("guess 2/3 of the average: rounds of elimination to push the bound below 1", k, 12, 0)
    alloc = pirates(5)
    print("    5 pirates:", alloc)
    assert alloc == [98, 0, 1, 0, 1]
    check("pirate game, 5 pirates: proposer keeps", alloc[0], 98, 0)
    check("pirate game, 10 pirates: proposer keeps", pirates(10)[0], 96, 0)
    # river bluffing: pot P, bet B
    for bet, f_exp, c_exp in ((1.0, 1 / 3, 1 / 2), (0.5, 1 / 4, 2 / 3)):
        # solve the two indifference conditions on a grid, independently of the closed forms
        grid = np.linspace(0, 1, 1_200_001)
        f = float(grid[np.argmin(np.abs(grid * (1 + bet) - (1 - grid) * bet))])  # caller indifferent
        c = float(grid[np.argmin(np.abs(grid * bet - (1 - grid) * 1.0))])  # bluffer indifferent
        check(f"bluff share of betting range B/(P + 2B), B = {bet} pot", f, f_exp, 1e-6)
        check(f"caller defence frequency P/(P + B), B = {bet} pot", c, c_exp, 1e-6)


if __name__ == "__main__":
    section_nash()
    section_auctions()
    section_winners_curse()
    section_bargaining()
    section_repeated()
    section_puzzles()
    print("\nall checks passed")
