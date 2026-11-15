"""Case File 08: COVID crash and negative WTI, every number on the page.

Backs `16-Trading-and-Investing/20-History-and-Events/08-2020-COVID-Crash-and-Negative-WTI-Crude.md`.
Independent routes used here:
- the WTI changes are recomputed from the CFTC's cited prices in exact decimal arithmetic, and the
  open-to-low fall is checked against the CFTC's separately stated $58.05;
- the S&P 500 drawdown is recomputed from the cited closes;
- the trading-day count from February 19 to March 23, 2020 uses numpy.busday_count and is checked by an
  explicit loop over calendar dates (there are no NYSE holidays in that window);
- the May 2020 last trading day is derived from the CME rule (three business days before the 25th of the
  prior month, four if the 25th is not a business day) and must equal the CFTC's expiry date, April 21.
Every quoted number is printed as ``label = value`` and asserted.
"""

from __future__ import annotations

import datetime as dt
from decimal import Decimal as D

import numpy as np


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def wti() -> None:
    print("May 2020 WTI (CFTC interim staff report)")
    prev_settle, settle, open_, low = D("18.27"), D("-37.63"), D("17.73"), D("-40.32")
    change = prev_settle - settle
    approx("settlement-to-settlement fall ($/bbl)", float(change), 55.90, 2)
    approx("fall as % of prior settlement", float(change / prev_settle * 100), 305.97, 2)
    open_to_low = open_ - low
    assert open_to_low == D("58.05"), "CFTC: the May contract fell $58.05 from the open to the low"
    print(f"    open-to-low fall ($/bbl) = {open_to_low}")


def is_business_day(day: dt.date) -> bool:
    return day.weekday() < 5  # no exchange holidays fall in the windows used here


def last_trading_day(contract_year: int, contract_month: int) -> dt.date:
    prior = dt.date(contract_year, contract_month, 1) - dt.timedelta(days=1)
    the_25th = dt.date(prior.year, prior.month, 25)
    steps = 3 if is_business_day(the_25th) else 4
    day = the_25th
    while steps:
        day -= dt.timedelta(days=1)
        if is_business_day(day):
            steps -= 1
    return day


def expiry() -> None:
    print("CME last trading day rule")
    ltd = last_trading_day(2020, 5)
    assert dt.date(2020, 4, 25).weekday() == 5, "April 25, 2020 was a Saturday"
    assert ltd == dt.date(2020, 4, 21), f"rule gives {ltd}, CFTC says April 21"
    print(f"    May 2020 last trading day = {ltd.isoformat()}")


def equities() -> None:
    print("S&P 500, February 19 to March 23, 2020")
    approx("drawdown (%)", float((1 - D("2237.40") / D("3386.15")) * 100), 33.92, 2)
    n_np = int(np.busday_count("2020-02-19", "2020-03-23"))
    n_loop, day = 0, dt.date(2020, 2, 19)
    while day < dt.date(2020, 3, 23):
        n_loop += is_business_day(day)
        day += dt.timedelta(days=1)
    assert n_np == n_loop == 23, f"busday_count {n_np}, loop {n_loop}"
    print(f"    trading days = {n_np}")


def main() -> None:
    wti()
    expiry()
    equities()
    print("all WTI checks passed")


if __name__ == "__main__":
    main()
