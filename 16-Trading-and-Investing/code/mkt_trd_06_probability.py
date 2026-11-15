"""Probability and decision making: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/06-Probability-and-Decision-Making.md`.
Independent routes used here:
- the expectancy matrix in exact fractions, with each break-even win rate found by bisection on the
  expectancy and checked against |L| / (W + |L|);
- the variance-drag sequences by compounding wealth step by step, against the Taylor approximation
  mu - sigma^2 / 2 computed from the population variance;
- the Brier score directly as a mean squared error and through Murphy's binned decomposition;
- binomial tail probabilities by exact enumeration and by a seeded simulation within five standard errors;
- Kelly growth rates by compounding an explicit 60-win, 40-loss ledger, the zero crossing by bisection;
- ruin probabilities by solving the absorbing gambler's-ruin chain numerically against (q / p)^(1 / f);
- the leveraged-ETF example by daily compounding of the index and of the 3x fund.
Run it with `python 16-Trading-and-Investing/code/mkt_trd_06_probability.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 1950


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


def expectancy_matrix() -> None:
    rows = [
        ("30%", Fraction(3, 10), Fraction(4), Fraction(1), "0.50", "20.00"),
        ("40%", Fraction(4, 10), Fraction(5, 2), Fraction(1), "0.40", "28.57"),
        ("50%", Fraction(5, 10), Fraction(3, 2), Fraction(1), "0.25", "40.00"),
        ("70%", Fraction(7, 10), Fraction(1, 2), Fraction(1), "0.05", "66.67"),
        ("90%", Fraction(9, 10), Fraction(1, 10), Fraction(3, 2), "-0.06", "93.75"),
    ]
    for name, w, win, loss, e_lit, be_lit in rows:
        e = w * win - (1 - w) * loss
        be = bisect(lambda p, win=win, loss=loss: p * float(win) - (1 - p) * float(loss), 0.0, 1.0)
        assert abs(be - float(loss / (win + loss))) < 1e-12
        check(f"expectancy at {name} (R)", float(e), e_lit)
        check(f"break-even win rate at {name} payoffs (%)", 100 * be, be_lit)
    check("card 003 win term (R)", float(Fraction(4, 10) * 3), "1.2")
    check("card 003 loss term (R)", float(Fraction(6, 10) * 1), "0.6")
    check("card 003 EV (R)", float(Fraction(4, 10) * 3 - Fraction(6, 10) * 1), "0.60")
    capital = Fraction(100)
    after_loss = capital * (1 - Fraction(1, 2))
    check("card 005 capital after a 50% loss ($)", float(after_loss), "50")
    check("card 005 gain needed to return to $100 (%)", float(100 * (capital / after_loss - 1)), "100")
    be5 = bisect(lambda p: 5 * p - (1 - p), 0.0, 1.0)
    check("card 015 break-even at 5R (%)", 100 * be5, "16.7")
    check("card 015 EV at 20% win rate (R)", float(Fraction(1, 5) * 5 - Fraction(4, 5)), "0.20")
    trades, tail_losses, win_r, tail_r = 20, 1, Fraction(1, 2), Fraction(20)
    check("pitfall: win rate (%)", 100 * (trades - tail_losses) / trades, "95")
    check("pitfall: tail loss share (%)", 100 * tail_losses / trades, "5")
    wins_total = (trades - tail_losses) * win_r
    check("pitfall: 19 wins of 0.5R (R)", float(wins_total), "9.5")
    assert wins_total < tail_r * tail_losses


def variance_drag() -> None:
    sequences = {"A": (0.10, 0.10), "B": (0.50, -0.30), "C": (1.00, -0.50)}
    quoted_wealth = {"A": "1.210", "B": "1.050", "C": "1.000"}
    results = {}
    for name, rets in sequences.items():
        wealth = 1.0
        for r in rets:
            wealth *= 1 + r
        mean = sum(rets) / len(rets)
        var = sum((r - mean) ** 2 for r in rets) / len(rets)
        geo = wealth ** (1 / len(rets)) - 1
        results[name] = (mean, var, geo)
        check(f"sequence {name} final wealth", wealth, quoted_wealth[name])
    check("sequence A total return (%)", 100 * (1.10 * 1.10 - 1), "21.0")
    check("sequence A arithmetic mean (%)", 100 * results["A"][0], "10.0")
    check("sequence A variance", results["A"][1], "0.0")
    check("sequence B total return (%)", 100 * (1.50 * 0.70 - 1), "5.0")
    check("sequence C total return (%)", 100 * (2.00 * 0.50 - 1), "0.0")
    check("sequence B arithmetic mean (%)", 100 * results["B"][0], "10.0")
    check("sequence B half variance", results["B"][1] / 2, "0.08")
    check("sequence C arithmetic mean (%)", 100 * results["C"][0], "25.0")
    check("sequence B variance", results["B"][1], "0.16")
    check("sequence B standard deviation (%)", 100 * math.sqrt(results["B"][1]), "40")
    check("sequence B approximation mu - var / 2 (%)", 100 * (results["B"][0] - results["B"][1] / 2), "2.00")
    check("sequence B exact geometric rate (%)", 100 * results["B"][2], "2.47")
    check("sequence C variance", results["C"][1], "0.5625")
    check("sequence C approximation mu - var / 2 (%)", 100 * (results["C"][0] - results["C"][1] / 2), "-3.125")
    check("sequence C exact geometric rate (%)", 100 * results["C"][2], "0.00")


def brier() -> None:
    forecasts = np.full(5, 0.70)
    outcomes = np.array([1, 1, 0, 1, 1])
    errors = (forecasts - outcomes) ** 2
    for i, lit in enumerate(("0.09", "0.09", "0.49", "0.09", "0.09")):
        check(f"squared error {i + 1}", errors[i], lit)
    check("sum of squared errors", errors.sum(), "0.85")
    bs = errors.mean()
    obar = outcomes.mean()
    rel = res = 0.0
    for f in np.unique(forecasts):
        mask = forecasts == f
        ok = outcomes[mask].mean()
        rel += mask.mean() * (f - ok) ** 2
        res += mask.mean() * (ok - obar) ** 2
    unc = obar * (1 - obar)
    assert abs((rel - res + unc) - bs) < 1e-12
    check("Brier score", bs, "0.170")
    check("observed frequency (%)", 100 * obar, "80")
    check("reliability", rel, "0.01")
    check("resolution", res, "0")
    check("uncertainty", unc, "0.16")
    check("Brier score from Murphy's decomposition", rel - res + unc, "0.17")


def binomial_tails(rng: np.random.Generator) -> None:
    sims = 400_000
    for p, lit in ((0.7, "52.82"), (0.5, "18.75")):
        exact = sum(math.comb(5, k) * p**k * (1 - p) ** (5 - k) for k in (4, 5))
        sim = float(np.mean(rng.binomial(5, p, sims) >= 4))
        se = math.sqrt(exact * (1 - exact) / sims)
        assert abs(sim - exact) < 5 * se, (p, sim, exact, se)
        check(f"P(at least 4 wins of 5 | p = {p}) (%)", 100 * exact, lit)


def growth_ledger(wins: int, losses: int, f: float) -> float:
    wealth = 1.0
    for outcome in [1] * wins + [0] * losses:
        wealth *= (1 + f) if outcome else (1 - f)
    return math.log(wealth) / (wins + losses)


def kelly() -> None:
    p = 0.60
    check("Kelly fraction 2p - 1", 2 * p - 1, "0.20")
    check("Kelly fraction (% of equity)", 100 * (2 * p - 1), "20")
    check("g(0.20) from a 60/40 ledger", growth_ledger(60, 40, 0.20), "0.0201")
    check("0.60 ln(1.40)", p * math.log(1.40), "0.2019")
    check("0.40 |ln(0.60)|", -(1 - p) * math.log(0.60), "0.2043")
    check("g(0.40) from a 60/40 ledger", growth_ledger(60, 40, 0.40), "-0.0024")
    cross = bisect(lambda f: p * math.log1p(f) + (1 - p) * math.log1p(-f), 0.25, 0.9)
    check("zero-growth crossing", cross, "0.389")


def ruin_markov(p: float, units: int, upper: int = 3000) -> float:
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
    for frac, lit in ((0.02, "0.0044"), (0.10, "13.4")):
        units = round(1 / frac)
        markov = ruin_markov(0.55, units)
        closed = (0.45 / 0.55) ** units
        assert abs(markov - closed) < 1e-9
        check(f"ruin at p = 0.55 risking {frac:.0%} (%)", 100 * markov, lit)


def leveraged_etf() -> None:
    index_moves = [0.10, 1 / 1.10 - 1]
    index = fund = 1.0
    for r in index_moves:
        index *= 1 + r
        fund *= 1 + 3 * r
    assert abs(index - 1.0) < 1e-12
    check("index second-day move (%)", 100 * index_moves[1], "-9.09")
    check("3x fund two-day return (%)", 100 * (fund - 1), "-5.45")
    for d, lit in ((Fraction(1, 2), "100"), (Fraction(9, 10), "900")):
        gain = 1 / (1 - d) - 1
        assert (1 - d) * (1 + gain) == 1
        check(f"drawdown {float(d):.0%} needs gain (%)", float(100 * gain), lit)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    expectancy_matrix()
    variance_drag()
    brier()
    binomial_tails(rng)
    kelly()
    ruin()
    leveraged_etf()
    print("all probability and decision-making numbers check out")
