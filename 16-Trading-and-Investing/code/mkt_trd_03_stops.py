"""Stop logic and trade management: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/03-Stop-Logic-and-Trade-Management.md`.
Independent routes used here:
- true range and the Wilder ATR step in exact fractions, against a float Wilder recursion run over a
  two-bar series whose second bar is the example bar;
- Turtle pyramid losses by replaying unit entries and trailing stops on an explicit price path that rises
  and then falls to the stop, against the closed-form sums 4.5N and 5.0N;
- Example 2 totals from an explicit 100-trade ledger per style, standard deviations from the exact outcome
  distribution in fractions checked against numpy on the ledger;
- the drawdown claim by a seeded simulation of 20,000 random orderings of the 100 trades: Style B's mean
  maximum drawdown must sit below Style A's by more than five standard errors of the difference.
Run it with `python 16-Trading-and-Investing/code/mkt_trd_03_stops.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SEED = 3


def check(label: str, value: float, expected: str) -> None:
    body = expected.replace(",", "")
    decimals = len(body.split(".")[1]) if "." in body else 0
    shown = f"{value:,.{decimals}f}" if "," in expected else f"{value:.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def wilder_recursion(highs, lows, closes, n: int, seed_atr: float) -> float:
    atr = seed_atr
    for t in range(1, len(closes)):
        tr = max(highs[t] - lows[t], abs(highs[t] - closes[t - 1]), abs(lows[t] - closes[t - 1]))
        atr = ((n - 1) * atr + tr) / n
    return atr


def atr_example() -> None:
    print("input: Example 1 C(t-1) = $105.00, H = $108.50, L = $103.00, prior 14-period ATR = $4.00, entry $107.00")
    prev_close, high, low = Fraction("105.00"), Fraction("108.50"), Fraction("103.00")
    parts = (high - low, abs(high - prev_close), abs(low - prev_close))
    for label, part, lit in zip(("H - L", "|H - C_prev|", "|L - C_prev|"), parts, ("5.50", "3.50", "2.00"), strict=True):
        check(f"true range component {label}", float(part), lit)
    tr = max(parts)
    check("true range", float(tr), "5.50")
    exact = (13 * Fraction(4) + tr) / 14
    recursion = wilder_recursion([0.0, 108.50], [0.0, 103.00], [105.00, 107.00], 14, 4.00)
    assert abs(float(exact) - recursion) < 1e-12
    check("13 x prior ATR", float(13 * Fraction(4)), "52.00")
    check("numerator", float(13 * Fraction(4) + tr), "57.50")
    check("ATR", float(exact), "4.1071")
    stop = Fraction("107.00") - 2 * exact
    check("2 x ATR", float(2 * exact), "8.2143")
    check("stop with unrounded ATR", float(stop), "98.79")
    check("stop with ATR rounded to 4.11 first", 107.00 - 2 * 4.11, "98.78")


def turtle_replay(units_to_add: int) -> float:
    """Loss per unit of size when the trend reverses to the trailing stop after the last addition."""
    n = 1.0
    p0 = 100.0
    entries = []
    stop = None
    price_path = [p0 + 0.5 * n * k for k in range(units_to_add)]  # rises in 0.5N steps
    for price in price_path:
        entries.append(price)
        stop = price - 2 * n  # all units' stop trails to 2N below the latest entry
    exit_price = stop  # then price falls straight to the stop
    return sum(entry - exit_price for entry in entries) / n


def turtle() -> None:
    print("cited: Faith (2007) Turtle rules: initial stop 2N, add a unit every +0.5N, cap of 4 units, N = ATR")
    check("unit 2 stop, in N below P0", -(0.5 - 2.0), "1.5")
    check("loss after unit 3 reverses (N)", turtle_replay(3), "4.5")
    check("loss after unit 4 reverses (N)", turtle_replay(4), "5.0")
    check("unit 4 loss / initial 2N risk", turtle_replay(4) / turtle_replay(1), "2.5")
    assert turtle_replay(1) == 2.0
    assert abs(turtle_replay(3) - (1.0 + 1.5 + 2.0)) < 1e-12


def styles() -> tuple[np.ndarray, np.ndarray]:
    risk = 1000
    print(f"input: Example 2 100 trades split 40 reversing, 20 trending, 40 failing; R = ${risk:,}")
    a = [Fraction(0)] * 40 + [Fraction(3)] * 20 + [Fraction(-1)] * 40
    b = [Fraction(1, 2)] * 40 + [Fraction(2)] * 20 + [Fraction(-1)] * 40
    check("style A reversing trades ($)", float(sum(a[:40]) * risk), "0")
    check("style A trending trades ($)", float(sum(a[40:60]) * risk), "60,000")
    check("style A failing trades ($)", float(sum(a[60:]) * risk), "-40,000")
    check("style A net ($)", float(sum(a) * risk), "20,000")
    check("style B reversing trades ($)", float(sum(b[:40]) * risk), "20,000")
    check("style B trending trades ($)", float(sum(b[40:60]) * risk), "40,000")
    check("style A per trending trade ($)", float(a[40] * risk), "3,000")
    check("style A per failing trade ($)", float(a[60] * risk), "-1,000")
    half = Fraction(1, 2)
    check("style B half closed at +1R ($)", float(half * 1 * risk), "500")
    check("style B half closed at +3R ($)", float(half * 3 * risk), "1,500")
    check("style B per reversing trade ($)", float(b[0] * risk), "500")
    check("style B per trending trade ($)", float(b[40] * risk), "2,000")
    check("style B net ($)", float(sum(b) * risk), "20,000")
    for name, book in (("A", a), ("B", b)):
        mean = sum(book) / len(book)
        var = sum((x - mean) ** 2 for x in book) / len(book)
        sd_np = float(np.std(np.array([float(x) for x in book])))
        assert abs(math.sqrt(var) - sd_np) < 1e-12
        check(f"style {name} expectancy (R)", float(mean), "0.20")
        check(f"style {name} per-trade sd (R)", math.sqrt(var), {"A": "1.47", "B": "1.12"}[name])
    check("trades of expected profit in one 5R loss", 5 / 0.20, "25")
    check("closing half at +1R with the rest at break-even (R)", 0.5 * 1.0 + 0.5 * 0.0, "0.5")
    return np.array([float(x) for x in a]), np.array([float(x) for x in b])


def max_drawdown(paths: np.ndarray) -> np.ndarray:
    equity = np.cumsum(paths, axis=1)
    equity = np.concatenate([np.zeros((paths.shape[0], 1)), equity], axis=1)
    peak = np.maximum.accumulate(equity, axis=1)
    return (peak - equity).max(axis=1)


def drawdowns(a: np.ndarray, b: np.ndarray, rng: np.random.Generator) -> None:
    sims = 20_000
    order = np.argsort(rng.random((sims, a.size)), axis=1)
    # The same shuffle for both styles: trade i keeps its type, only the management differs.
    dd_a = max_drawdown(a[order])
    dd_b = max_drawdown(b[order])
    diff = dd_a - dd_b
    se = diff.std(ddof=1) / math.sqrt(sims)
    print(f"mean max drawdown A = {dd_a.mean():.2f}R, B = {dd_b.mean():.2f}R (seed {SEED})")
    print(f"difference = {diff.mean():.3f}R, standard error = {se:.3f}R")
    assert diff.mean() > 5 * se, "style B must have a smaller mean max drawdown by > 5 se"


def cards() -> None:
    print("input: time stop example M = 5 trading days; stop buffer example 0.5 x ATR")
    print("input: slippage pitfall stop $50.00, hypothetical fill $48.50")
    print("input: card mkt-trd-076 hypothetical 90% of winners within 1.5 x ATR, stop at 1.8 x ATR")
    print("input: card mkt-trd-077 hypothetical MFE stall near 2.5R, target 2.3R")
    print("input: card mkt-trd-089 runner 25% to 33% of the position; card mkt-trd-095 daily loss limit 3R")
    print("input: card mkt-trd-075 buffer k = 0.5 to 1.0 x ATR; stop multiplier examples k = 1.0 and 2.0 to 3.0")
    print("input: volatility stop example 2.0 x ATR14; accounting stop examples 2% and $500; trailing example 5%")
    print("input: scale-out example 50% at T1 = +1R; widened-stop examples 3R and 5R")
    print("cited: Wilder (1978) true range and ATR; Osler (2003) stop clusters beyond round numbers")
    check("card 091 gap loss / intended loss", (100 - 80) / (100 - 95), "4")
    check("card 093 5% stop in daily sigmas, 1% vol stock", 5 / 1, "5")
    check("card 093 5% stop in daily sigmas, 10% vol asset", 5 / 10, "0.5")


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    atr_example()
    turtle()
    a, b = styles()
    drawdowns(a, b, rng)
    cards()
    print("all stop-logic numbers check out")
