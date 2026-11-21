"""Trading psychology: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/05-Trading-Psychology-and-Performance.md`.
Independent routes used here:
- prospect-theory values V(1,000) and V(-1,000) from the Tversky-Kahneman (1992) median parameters
  (alpha = beta = 0.88, lambda = 2.25, cited constants), computed through logarithms and checked against
  direct powers;
- the disposition example in exact fractions, checked by a seeded simulation of 400,000 trades per
  regime within five standard errors;
- the equity-curve claim: independent trades are simulated, each trade is tagged by whether equity sat
  below its 20-trade moving average when it was entered, and the mean R of the tagged trades must equal
  the unconditional mean within five standard errors (the filter changes exposure, not expectancy).
Run it with `python 16-Trading-and-Investing/code/mkt_trd_05_psychology.py`.
"""

from __future__ import annotations

import math
from decimal import Decimal, localcontext
from fractions import Fraction

import numpy as np

SEED = 1979


def check(label: str, value: float, expected: str) -> None:
    body = expected.replace(",", "")
    decimals = len(body.split(".")[1]) if "." in body else 0
    shown = f"{value:,.{decimals}f}" if "," in expected else f"{value:.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def prospect_values() -> None:
    alpha, beta, lam, x = 0.88, 0.88, 2.25, 1000.0
    x_loss = -x
    gain = x**alpha
    loss = -lam * (-x_loss) ** beta
    with localcontext() as ctx:
        ctx.prec = 40
        gain_dec = Decimal(10) ** (3 * Decimal("0.88"))
        loss_dec = -Decimal("2.25") * Decimal(10) ** (3 * Decimal("0.88"))
    assert abs(gain - float(gain_dec)) < 1e-9 and abs(loss - float(loss_dec)) < 1e-9
    check("V(1,000)", gain, "436.5")
    check("V(-1,000)", loss, "-982.2")
    # With alpha = beta the ratio is lambda by definition, so it is printed as a cited constant, not asserted.
    print(f"cited: loss-aversion coefficient lambda = {lam} (Tversky and Kahneman 1992)")
    print(f"cited: curvature alpha = beta = {alpha} (Tversky and Kahneman 1992)")
    # Value-function chart: drawn to scale over x in [-4, 10].
    print("input: value-function chart range x = -4 to 10")
    check("chart V(10)", 10.0**alpha, "7.6")
    check("chart V(-4)", -lam * 4.0**beta, "-7.6")
    # Shape claims by midpoint tests (independent of the slope formula): concave gains, convex losses.
    assert 5.0**alpha > (0.0 + 10.0**alpha) / 2, "gain branch must be concave"
    assert -lam * 2.0**beta < (0.0 - lam * 4.0**beta) / 2, "loss branch must be convex"
    print("cited: Odean (1998) 10,000 discount-brokerage accounts, 1987-1993")
    print("cited: Kahneman and Tversky (1979); Shefrin and Statman (1985); Barber and Odean (2001)")
    print("cited: Arnsten (2009); Coates and Herbert (2008); Kahneman, Knetsch and Thaler (1990)")
    print("cited: Samuelson and Zeckhauser (1988); Douglas (2000); Steenbarger (2006)")
    print("input: tilt rule-of-thumb example: cut size by half")
    print("input: equity-curve filter moving average = 20 trades; Example 1 = 100 trades at a 50% win rate")


def disposition(rng: np.random.Generator) -> None:
    half = Fraction(1, 2)
    regimes = {"disciplined": (Fraction(2), Fraction(-1)), "distorted": (Fraction(1), Fraction(-18, 10))}
    quoted = {"disciplined": ("0.50", "50"), "distorted": ("-0.40", "-40")}
    totals = {}
    n = 400_000
    for name, (win, loss) in regimes.items():
        ev = half * win + half * loss
        wins = rng.random(n) < 0.5
        sample = np.where(wins, float(win), float(loss))
        se = sample.std(ddof=1) / math.sqrt(n)
        assert abs(sample.mean() - float(ev)) < 5 * se, (name, sample.mean(), float(ev), se)
        check(f"win term, {name} (R)", float(half * win), {"disciplined": "1.0", "distorted": "0.5"}[name])
        check(f"loss term, {name} (R)", float(half * loss), {"disciplined": "-0.50", "distorted": "-0.90"}[name])
        check(f"expected R per trade, {name}", float(ev), quoted[name][0])
        check(f"expected R over 100 trades, {name}", float(100 * ev), quoted[name][1])
        totals[name] = 100 * ev
    check("swing over 100 trades (R)", float(totals["disciplined"] - totals["distorted"]), "90")
    check("disciplined total over 100 trades, one decimal (R)", float(totals["disciplined"]), "50.0")


def equity_curve_filter(rng: np.random.Generator) -> None:
    trades, paths, window = 400, 2_000, 20
    outcomes = np.where(rng.random((paths, trades)) < 0.5, 2.0, -1.0)
    equity = np.cumsum(outcomes, axis=1)
    below = []
    above = []
    for t in range(window, trades):
        ma = equity[:, t - window : t].mean(axis=1)
        state_below = equity[:, t - 1] < ma  # decided before trade t is taken
        below.append(outcomes[state_below, t])
        above.append(outcomes[~state_below, t])
    below_r = np.concatenate(below)
    above_r = np.concatenate(above)
    diff = below_r.mean() - above_r.mean()
    se = math.sqrt(below_r.var(ddof=1) / below_r.size + above_r.var(ddof=1) / above_r.size)
    print(f"mean R when below the MA = {below_r.mean():.4f}, above = {above_r.mean():.4f}, se of gap = {se:.4f}")
    assert abs(diff) < 5 * se, "with independent trades the filter state must not predict the next trade"
    print("check: independent trades -> filter state carries no information about the next trade's R")


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    prospect_values()
    disposition(rng)
    equity_curve_filter(rng)
    print("all trading-psychology numbers check out")
