"""Dow Theory and trend evidence: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/01-Dow-Theory-and-Trend-Evidence.md`.
Independent routes used here:
- the 200-day SMA, the price-to-SMA gap and the 2.0% drop in exact rational arithmetic (Fraction), with the
  exit and re-entry crossings asserted against the SMA;
- the whipsaw loss by simulating the account (sell all shares, hold cash, buy back) against buy-and-hold, with
  the log-return route as a cross-check of the rounding;
- the SMA lag (N - 1) / 2 as the weight-averaged age of the window and, separately, as the measured delay
  of the SMA behind a linear price ramp;
- the EMA smoothing constant alpha = 2 / (N + 1) as the value whose mean lag (1 - alpha) / alpha, summed from
  the explicit geometric weights, equals the SMA lag;
- the Dow confirmation percentages in exact rational arithmetic.
Study dates (Brock, Lakonishok and LeBaron 1992; Sullivan, Timmermann and White 1999; Lo, Mamaysky and Wang
2000; Brown, Goetzmann and Kumar 1998) are cited constants printed for reference.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_ta_01_dow_trend.py`.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np


def check(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{value:,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def sma_example() -> None:
    close = Fraction(4950)
    window_sum = Fraction(980_000)
    sma_exact = window_sum / 200
    check("SMA_200", float(sma_exact), "4,900.00")
    gap = close / sma_exact - 1
    check("close above SMA_200 (%)", float(100 * gap), "1.02")
    assert close > sma_exact

    # Whipsaw: sell after a 2.0% drop, buy back on the rebound.
    sell = close * Fraction(98, 100)
    check("price after 2.0% drop", float(sell), "4,851.00")
    assert sell < sma_exact, "the drop must cross below the SMA to trigger the exit"
    rebuy = Fraction(4920)
    assert rebuy > sma_exact, "the rebound must cross back above the SMA to trigger re-entry"
    shares, cash = Fraction(1), Fraction(0)
    cash, shares = shares * sell, Fraction(0)
    shares, cash = cash / rebuy, Fraction(0)
    whipsaw = shares - 1  # value at the rebuy price relative to having held one share
    check("whipsaw loss vs holding (%)", float(100 * whipsaw), "-1.4")
    check("whipsaw loss, log route (%)", 100 * float(np.log(float(sell) / float(rebuy))), "-1.4")


def sma_lag(n: int = 200) -> float:
    ages = np.arange(n)
    weighted_age = float(np.mean(ages))
    t = np.arange(5 * n, dtype=float)  # linear ramp P_t = t
    sma = np.convolve(t, np.ones(n) / n, mode="valid")
    measured = float(np.mean(t[n - 1 :] - sma))
    assert abs(weighted_age - measured) < 1e-9
    check(f"SMA({n}) lag, weighted age (days)", weighted_age, "99.5")
    check(f"SMA({n}) lag, ramp delay (days)", measured, "99.5")
    check("200 trading days in months at 21 days per month", n / 21, "9.5")
    return weighted_age


def ema_matching_alpha(n: int) -> float:
    target = (n - 1) / 2
    alpha = 2 / (n + 1)
    k = np.arange(20_000)
    weights = alpha * (1 - alpha) ** k
    mean_lag = float(np.sum(k * weights) / np.sum(weights))
    assert abs(mean_lag - target) < 1e-6, (n, mean_lag, target)
    return alpha


def dow_confirmation() -> None:
    djia = Fraction(39_200, 38_000) - 1
    djta = Fraction(15_750, 16_000) - 1
    check("DJIA May close vs January peak (%)", float(100 * djia), "3.16")
    check("DJTA May close vs January peak (%)", float(100 * djta), "-1.56")
    assert djia > 0 > djta, "non-confirmation needs a new high in one average and not the other"


if __name__ == "__main__":
    sma_example()
    sma_lag()
    for n in (10, 50, 200):
        print(f"EMA alpha matching SMA({n}) lag = {ema_matching_alpha(n):.4f}")
    dow_confirmation()
    cited = {
        "Brock-Lakonishok-LeBaron DJIA sample": "1897-1986, 26 rules, 4 null models",
        "Sullivan-Timmermann-White universe": "7,846 rules, post-sample 1987-1996",
        "Lo-Mamaysky-Wang sample": "US stocks 1962-1996, 10 patterns",
        "Brown-Goetzmann-Kumar Hamilton period": "1902-1929",
        "Rhea secondary reaction": "retraces 33% to 66%, lasts three weeks to three months",
    }
    for key, val in cited.items():
        print(f"cited: {key} = {val}")
    print("all Dow Theory numbers check out")
