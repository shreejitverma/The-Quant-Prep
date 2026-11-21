"""Position sizing and ruin: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/02-Position-Sizing-and-Ruin.md`.
Independent routes used here:
- the Kelly fraction as the argmax of the growth curve on a fine grid, against the closed form p - q / b;
- growth rates g(f) by compounding an explicit ledger of 40 wins and 60 losses (log of terminal wealth
  over 100 bets), and by a seeded simulation of 400,000 bets within five standard errors;
- zero-growth crossings by bisection on g, then compared with 2 f*;
- ruin probabilities by solving the absorbing gambler's-ruin Markov chain with a far upper barrier as a
  linear system, against the closed form (q / p)^C;
- the continuous-time Kelly drawdown law P(wealth ever hits x) = x^(2 / c - 1) by a finite-difference
  solution of the hitting-probability equation (s^2 / 2) u'' + m u' = 0;
- recovery gains in exact fractions, recovery years by bisection on (1.1)^t (1 - D) = 1;
- the martingale losing-streak probability by dynamic programming over run lengths, checked by a seeded
  simulation within five standard errors.
Run it with `python 16-Trading-and-Investing/code/mkt_trd_02_sizing_ruin.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 20261115


def check(label: str, value: float, expected: str) -> None:
    body = expected.replace(",", "")
    decimals = len(body.split(".")[1]) if "." in body else 0
    shown = f"{value:,.{decimals}f}" if "," in expected else f"{value:.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def bisect(fn, lo: float, hi: float, iters: int = 200) -> float:
    flo = fn(lo)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        fmid = fn(mid)
        if (fmid > 0) == (flo > 0):
            lo, flo = mid, fmid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def growth_formula(p: float, b: float, f: float) -> float:
    return p * math.log(1 + b * f) + (1 - p) * math.log(1 - f)


def growth_ledger(wins: int, losses: int, b: float, f: float) -> float:
    """Average log growth per bet from compounding an explicit sequence of bets."""
    wealth = 1.0
    for outcome in [1] * wins + [0] * losses:
        stake = f * wealth
        wealth += b * stake if outcome else -stake
    return math.log(wealth) / (wins + losses)


def kelly_example(rng: np.random.Generator) -> None:
    p, b = 0.40, 2.50
    print(f"input: Example 1 win rate p = {p:.2f}, payoff ratio b = {b:.2f}")
    grid = np.linspace(0.0005, 0.9, 900_000)
    g_grid = p * np.log1p(b * grid) + (1 - p) * np.log1p(-grid)
    f_grid = float(grid[np.argmax(g_grid)])
    f_star = p - (1 - p) / b
    assert abs(f_grid - f_star) < 1e-5
    check("Kelly fraction f*, grid argmax", f_grid, "0.160")
    check("Kelly fraction f* (%)", 100 * f_grid, "16.0")
    n = 400_000
    wins = rng.random(n) < p
    quoted = {0.16: "0.0300", 0.08: "0.0229", 0.32: "0.0037", 0.35: "-0.0070"}
    for f, lit in quoted.items():
        led = growth_ledger(40, 60, b, f)
        assert abs(led - growth_formula(p, b, f)) < 1e-12
        logs = np.where(wins, math.log1p(b * f), math.log1p(-f))
        se = logs.std(ddof=1) / math.sqrt(n)
        assert abs(logs.mean() - led) < 5 * se, f"simulated g({f}) off by more than 5 se"
        check(f"g({f}) from the 100-bet ledger", led, lit)
        pct = {0.16: "3.00", 0.08: "2.29", 0.32: "0.37", 0.35: "-0.70"}[f]
        check(f"g({f}) per trade (%)", 100 * led, pct)
    full, half = growth_ledger(40, 60, b, 0.16), growth_ledger(40, 60, b, 0.08)
    check("g(0.16) unrounded", full, "0.029977")
    check("g(0.08) unrounded", half, "0.022900")
    check("half Kelly share of maximum growth (%)", 100 * half / full, "76.4")
    check("g(0.32) / g(0.16)", growth_ledger(40, 60, b, 0.32) / full, "0.12")
    cross = bisect(lambda f: growth_formula(p, b, f), 0.2, 0.9)
    check("zero-growth crossing", cross, "0.331")
    check("crossing / f*", cross / f_star, "2.07")
    check("continuous share of max growth at half Kelly (%)", 100 * (2 * 0.5 - 0.5**2), "75")

    def trade_variance(f: float) -> float:
        mean = p * b * f - (1 - p) * f
        return p * (b * f - mean) ** 2 + (1 - p) * (-f - mean) ** 2

    check("half Kelly variance / full Kelly variance (%)", 100 * trade_variance(0.08) / trade_variance(0.16), "25")
    # Each ln term and weighted term quoted in the worked example.
    terms = {
        0.16: ("0.3365", "-0.1744", "0.1346", "0.1046"),
        0.08: ("0.1823", "-0.0834", "0.0729", "0.0500"),
        0.32: ("0.5878", "-0.3857", "0.2351", "0.2314"),
        0.35: ("0.6286", "-0.4308", "0.25144", "0.25847"),
    }
    for f, (ln_up, ln_down, w_up, w_down) in terms.items():
        check(f"ln(1 + 2.5 x {f})", math.log1p(b * f), ln_up)
        check(f"ln(1 - {f})", math.log1p(-f), ln_down)
        check(f"0.40 ln(1 + 2.5 x {f})", p * math.log1p(b * f), w_up)
        check(f"0.60 |ln(1 - {f})|", -(1 - p) * math.log1p(-f), w_down)


def ruin_markov(p: float, units: int, upper: int = 3000) -> float:
    """Ruin probability from `units`, absorbing at 0 and at `units + upper`, by a linear solve."""
    top = units + upper
    a = np.zeros((top + 1, top + 1))
    rhs = np.zeros(top + 1)
    a[0, 0], rhs[0] = 1.0, 1.0
    a[top, top] = 1.0
    for i in range(1, top):
        a[i, i] = 1.0
        a[i, i + 1] = -p
        a[i, i - 1] = -(1 - p)
    return float(np.linalg.solve(a, rhs)[units])


def ruin() -> None:
    for p, units, lit in ((0.55, 50, "0.0044"), (0.52, 50, "1.8"), (0.51, 50, "13.5")):
        markov = ruin_markov(p, units)
        closed = ((1 - p) / p) ** units
        assert abs(markov - closed) < 1e-9 * max(closed, 1e-6) + 1e-12
        check(f"ruin probability, p = {p}, C = {units} (%)", 100 * markov, lit)
    check("C = 1 / f at 2% risk", 1 / 0.02, "50")


def hitting_probability_fd(drift: float, var: float, a: float, upper: float, below: int = 4000) -> float:
    """P(log wealth hits -a before about +upper) from 0, by finite differences with 0 on the grid."""
    h = a / below
    n = below + math.ceil(upper / h)
    x = -a + h * np.arange(n + 1)
    lower_coef = var / (2 * h * h) - drift / (2 * h)
    diag_coef = -var / (h * h)
    upper_coef = var / (2 * h * h) + drift / (2 * h)
    # Thomas algorithm for the interior points with u(-a) = 1, u(upper) = 0.
    m = n - 1
    sub = np.full(m, lower_coef)
    dia = np.full(m, diag_coef)
    sup = np.full(m, upper_coef)
    rhs = np.zeros(m)
    rhs[0] -= lower_coef * 1.0
    for i in range(1, m):
        w = sub[i] / dia[i - 1]
        dia[i] -= w * sup[i - 1]
        rhs[i] -= w * rhs[i - 1]
    u = np.zeros(m)
    u[-1] = rhs[-1] / dia[-1]
    for i in range(m - 2, -1, -1):
        u[i] = (rhs[i] - sup[i] * u[i + 1]) / dia[i]
    zero = below - 1  # interior index of the grid point x = 0
    assert abs(x[zero + 1]) < 1e-9
    return float(u[zero])


def kelly_drawdowns() -> None:
    sharpe = 0.5  # any positive Sharpe ratio gives the same answer
    for c, x, lit in ((1.0, 0.5, "50"), (0.5, 0.5, "12.5"), (1.0, 0.1, "10")):
        drift = c * sharpe**2 - 0.5 * (c * sharpe) ** 2
        var = (c * sharpe) ** 2
        fd = hitting_probability_fd(drift, var, math.log(1 / x), upper=40.0)
        closed = x ** (2 / c - 1)
        assert abs(fd - closed) < 1e-4, (fd, closed)
        check(f"P(wealth ever reaches {x} of start) at {c} Kelly (%)", 100 * fd, lit)


def recovery_table() -> None:
    rows = {
        "5": ("5.26", "0.54"),
        "10": ("11.11", "1.11"),
        "20": ("25.00", "2.34"),
        "30": ("42.86", "3.74"),
        "50": ("100.00", "7.27"),
        "75": ("300.00", "14.55"),
        "90": ("900.00", "24.16"),
    }
    for pct, (gain_lit, years_lit) in rows.items():
        d = Fraction(int(pct), 100)
        gain = 1 / (1 - d) - 1
        assert (1 - d) * (1 + gain) == 1
        years = bisect(lambda t, d=float(d): 1.1**t * (1 - d) - 1, 0.0, 100.0)
        check(f"recovery gain after {pct}% drawdown (%)", float(100 * gain), gain_lit)
        check(f"years to recover {pct}% at 10% a year", years, years_lit)
    check("recovery gain after 80% drawdown (%)", float(100 * (1 / (1 - Fraction(4, 5)) - 1)), "400")


def atr_example() -> None:
    equity, risk_pct, entry, atr = 100_000, 1.5, 150.00, 3.50
    print(f"input: Example 2 equity ${equity:,}, risk {risk_pct}%, entry ${entry:.2f}, ATR ${atr:.2f}, stop 2 x ATR")
    print("input: gap open $130.00; fixed-dollar sizing example $10,000 per trade; fixed-fraction example f = 1.0%")
    budget = equity * risk_pct / 100
    check("risk budget, 1.5% of 100,000", budget, "1,500")
    stop = entry - 2 * atr
    check("stop price", stop, "143.00")
    check("stop distance", entry - stop, "7.00")
    raw = budget / (entry - stop)
    shares = math.floor(raw)
    check("raw share count", raw, "214.29")
    check("shares", shares, "214")
    check("position value", shares * entry, "32,100")
    check("position share of equity (%)", 100 * shares * entry / 100_000, "32.1")
    check("dollar risk at the stop", shares * (entry - stop), "1,498.00")
    check("gap loss per share (open at 130)", entry - 130.00, "20")
    check("gap loss in R (open at 130)", (entry - 130.00) / (entry - stop), "2.86")
    print("input: worst-case gap example = 20%; ATR period = 14")
    check("static sizing risk, $20 stock, $0.50 stop", 1000 * 0.50, "500")
    check("static sizing risk, $400 stock, $10 stop", 1000 * 10, "10,000")
    check("five correlated 1.5% risks (%)", 5 * 1.5, "7.5")


def martingale(rng: np.random.Generator) -> None:
    n, k = 1000, 10
    dist = np.zeros(k)
    dist[0] = 1.0
    hit = 0.0
    for _ in range(n):
        new = np.zeros(k)
        new[0] = 0.5 * dist.sum()
        new[1:] = 0.5 * dist[:-1]
        hit += 0.5 * dist[-1]
        dist = new
    paths = 20_000
    losses = rng.random((paths, n)) < 0.5
    run = np.zeros(paths, dtype=int)
    best = np.zeros(paths, dtype=int)
    for t in range(n):
        run = np.where(losses[:, t], run + 1, 0)
        best = np.maximum(best, run)
    sim = float(np.mean(best >= k))
    se = math.sqrt(sim * (1 - sim) / paths)
    assert abs(sim - hit) < 5 * se, (sim, hit, se)
    check("P(run of 10+ losses in 1,000 fair bets) (%)", 100 * hit, "38.5")
    check("units lost after 10 doublings", sum(2**i for i in range(k)), "1,023")
    check("next stake after 10 losses", 2**k, "1,024")


def cards() -> None:
    cov = np.diag([1.0, 1.0])
    w = np.array([0.5, 0.5])
    check("equal-weight vol of two uncorrelated assets / sigma", math.sqrt(w @ cov @ w), "0.707")
    check("break-even win rate at 2R (%)", float(100 * Fraction(1, 3)), "33.3")
    for w in (Fraction(35, 100), Fraction(45, 100)):
        assert w * 2 - (1 - w) > 0, "card 053: 35% to 45% at 2R must be profitable before costs"
    for d, lit in ((Fraction(1, 10), "11.1"), (Fraction(1, 5), "25"), (Fraction(1, 2), "100")):
        check(f"card 064 recovery after a {float(100 * d):.0f}% drawdown (%)", float(100 * (1 / (1 - d) - 1)), lit)
    print("cited: US market-wide circuit breakers: 7% (Level 1) and 13% (Level 2) halt 15 minutes before 3:25 pm")
    print("cited: Level 3 at 20% halts for the day (NYSE Rule 7.12); LULD single-stock pauses (NYSE Rule 7.11), 2013")
    print("input: hypothetical ADV participation cap = 1%; accounting-stop examples USD 500 and 2%")


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    kelly_example(rng)
    ruin()
    kelly_drawdowns()
    recovery_table()
    atr_example()
    martingale(rng)
    cards()
    print("all position-sizing and ruin numbers check out")
