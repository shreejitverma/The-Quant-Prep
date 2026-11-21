"""Setup taxonomy and evidence grading: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/04-Setup-Taxonomy-and-Evidence.md`.
Independent routes used here:
- the two-sided p-value of t = 3.0 by the error function and by composite Simpson quadrature of the
  normal density;
- the expected best t-statistic among 100 independent null rules by numerical integration of
  E[max] = integral of x d(Phi(x)^100), checked by a seeded simulation within five standard errors;
- the probability that at least one of 100 null rules shows |t| > 2 by the closed form 1 - (1 - p)^100
  and by the same simulation;
- the VCP target moves and the breakout break-even payoff ratio by bisection on the expectancy.
Study results (Jegadeesh-Titman 12.01%, Aronson's 6,402 rules, Sullivan-Timmermann-White's 7,846) are
cited constants.
Run it with `python 16-Trading-and-Investing/code/mkt_trd_04_setups.py`.
"""

from __future__ import annotations

import math

import numpy as np

SEED = 1993


def check(label: str, value: float, expected: str) -> None:
    body = expected.replace(",", "")
    decimals = len(body.split(".")[1]) if "." in body else 0
    shown = f"{value:,.{decimals}f}" if "," in expected else f"{value:.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def phi(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def simpson(fn, a: float, b: float, n: int = 20_000) -> float:
    h = (b - a) / n
    total = fn(a) + fn(b)
    for i in range(1, n):
        total += (4 if i % 2 else 2) * fn(a + i * h)
    return total * h / 3


def harvey_liu_zhu() -> None:
    p_erf = 2 * (1 - cdf(3.0))
    p_quad = 2 * simpson(phi, 3.0, 40.0)
    assert abs(p_erf - p_quad) < 1e-10
    check("two-sided p-value at t = 3.0", p_quad, "0.0027")


def best_of_null_rules(rng: np.random.Generator) -> None:
    k = 100
    expected_max = simpson(lambda x: x * k * cdf(x) ** (k - 1) * phi(x), -10.0, 10.0)
    sims = 200_000
    draws = rng.standard_normal((sims, k))
    best = draws.max(axis=1)
    se = best.std(ddof=1) / math.sqrt(sims)
    assert abs(best.mean() - expected_max) < 5 * se, (best.mean(), expected_max, se)
    check("expected best t among 100 null rules", expected_max, "2.51")
    p_two = 2 * (1 - cdf(2.0))
    closed = 1 - (1 - p_two) ** k
    sim = float(np.mean(np.abs(draws).max(axis=1) > 2.0))
    se_p = math.sqrt(sim * (1 - sim) / sims)
    assert abs(sim - closed) < 5 * se_p, (sim, closed, se_p)
    check("P(at least one |t| > 2 among 100 null rules) (%)", 100 * closed, "99.1")


def vcp_and_breakouts() -> None:
    check("VCP target move, 3% risk x 3R (%)", 3 * 3, "9")
    check("VCP target move, 5% risk x 5R (%)", 5 * 5, "25")
    p = 0.35
    lo, hi = 0.0, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if p * mid - (1 - p) > 0:
            hi = mid
        else:
            lo = mid
    check("break-even average win at a 35% win rate (R)", lo, "1.86")
    check("intraday net edge (bp)", 8 - 10, "-2")


def inputs() -> None:
    print("input: VCP Example 1 trend filter, price within 15% of the 52-week high, P > SMA50 > SMA150 > SMA200")
    print("input: VCP waves 20% to 25%, 10% to 12%, then 3% to 5% over 3 to 7 days")
    print("input: VCP range contraction ATR14(t) <= 0.50 x ATR14(t - 30); terminal volume < 0.50 x 50-day average")
    print("input: VCP buy trigger volume > 1.50 x 50-day average; stop at the terminal low; targets 3R to 5R")
    print("input: intraday pitfall gross gain 8 bp, round-trip spread and clearing cost 10 bp")
    print("input: breakout win rate 35% (card mkt-trd-108 example)")
    print("input: card mkt-trd-112 hypothetical bull flag, retracement <= 50% of the pole, volume below its 20-day average")
    print("input: card mkt-trd-115 Donchian lookbacks 20 and 55 days")
    print("input: card mkt-trd-122 Darvas Box ceiling and floor hold for three days")
    print("input: card mkt-trd-125 opening range of the first 15 or 30 minutes; initial balance the first hour")


def cited() -> None:
    print("cited: FTSE Russell 1 September 2026 announcement, first December reconstitution effective after the close on 11 December 2026")
    print("cited: Jegadeesh-Titman 6/6 strategy compounded excess return = 12.01% per year")
    print("cited: Aronson (2006) rules tested = 6,402; Sullivan-Timmermann-White (1999) universe = 7,846 rules")
    print("cited: Moskowitz-Ooi-Pedersen (2012) instruments = 58; Brock-Lakonishok-LeBaron (1992) rules = 26")


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    harvey_liu_zhu()
    best_of_null_rules(rng)
    vcp_and_breakouts()
    inputs()
    cited()
    print("all setup-evidence numbers check out")
