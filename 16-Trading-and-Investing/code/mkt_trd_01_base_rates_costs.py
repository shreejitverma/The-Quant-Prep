"""Retail base rates and costs: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/01-Retail-Base-Rates-and-Costs.md`.
Independent routes used here:
- Example 1 friction by an explicit fill-by-fill cash ledger (buy at the ask plus slippage, sell at the
  bid, fees debited) for all 1,260 round trips, checked against the per-trade cost formula;
- break-even win rates by bisection on the expectancy function, checked against exact rational
  arithmetic with fractions.Fraction;
- expectancy and 200-trade totals from an enumerated trade list with the stated win counts;
- win-rate standard errors from the exact variance of the binomial sampling distribution (a sum over
  every possible count), checked against sqrt(p(1 - p) / N), and the 95% quantile z by bisection on the
  normal tail;
- card arithmetic (80% win-rate example, profit factor, leverage, borrow fee, hurdle) from enumerated
  trade lists or exact fractions.
Study figures (Barber-Odean, SEBI, Chague et al.) are cited constants; only their arithmetic is checked.
Run it with `python 16-Trading-and-Investing/code/mkt_trd_01_base_rates_costs.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction


def check(label: str, value: float, expected: str) -> None:
    """Format value at the precision of the quoted literal and require an exact match."""
    body = expected.replace(",", "")
    decimals = len(body.split(".")[1]) if "." in body else 0
    shown = f"{value:,.{decimals}f}" if "," in expected else f"{value:.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def bisect(fn, lo: float, hi: float, iters: int = 200) -> float:
    flo = fn(lo)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if (fn(mid) > 0) == (flo > 0):
            lo, flo = mid, fn(mid)
        else:
            hi = mid
    return 0.5 * (lo + hi)


def example_1_ledger() -> None:
    days, trips_per_day, shares = 252, 5, 500
    mid, spread, slippage, fees = 100.00, 0.02, 0.01, 1.50
    equity = 25_000.0
    print(f"input: Example 1 equity ${equity:,.0f}, mid ${mid:.2f}, spread ${spread:.2f}, slippage ${slippage:.2f}, fees ${fees:.2f}")
    print(f"input: Example 1 {shares} shares, {trips_per_day} round trips a day, {days} days")
    cash = 0.0
    trips = 0
    for _day in range(days):
        for _trip in range(trips_per_day):
            buy_price = mid + spread / 2 + slippage  # market buy at the ask, slippage on the fill
            sell_price = mid - spread / 2  # market sell at the bid; gross skill is zero
            cash -= buy_price * shares
            cash += sell_price * shares
            cash -= fees
            trips += 1
    per_trade_formula = 2 * (spread / 2) * shares + slippage * shares + fees
    check("round trips per year", trips, "1,260")
    check("gross market value", shares * mid, "50,000")
    check("leverage (gross market value / equity)", shares * mid / equity, "2")
    check("spread cost per round trip", 2 * (spread / 2) * shares, "10.00")
    check("slippage cost per round trip", slippage * shares, "5.00")
    check("friction per round trip, ledger", -cash / trips, "16.50")
    check("friction per round trip, formula", per_trade_formula, "16.50")
    check("annual friction, ledger", -cash, "20,790")
    check("annual friction / starting equity (%)", 100 * -cash / equity, "83.16")


def example_2_expectancy() -> None:
    win_r, cost = Fraction(2), Fraction(35, 500)
    check("c_R", float(cost), "0.07")

    def e_r(p: float, c: float) -> float:
        return p * float(win_r) - (1 - p) - c

    be0 = bisect(lambda p: e_r(p, 0.0), 0.0, 1.0)
    be1 = bisect(lambda p: e_r(p, float(cost)), 0.0, 1.0)
    assert abs(be0 - float(Fraction(1, 3))) < 1e-12
    assert abs(be1 - float((1 + cost) / (1 + win_r))) < 1e-12
    check("break-even numerator 1 + c_R", float(1 + cost), "1.07")
    for p, lit_win, lit_loss in ((Fraction(40, 100), "0.80", "0.60"), (Fraction(35, 100), "0.70", "0.65")):
        check(f"win term at p = {float(p)}", float(p * win_r), lit_win)
        check(f"loss term at p = {float(p)}", float(1 - p), lit_loss)
    check("break-even win rate, no friction (%)", 100 * be0, "33.33")
    check("break-even win rate, with friction (%)", 100 * be1, "35.67")
    p_hi, p_lo = Fraction(40, 100), Fraction(35, 100)
    check("win-rate drop from 40% to 35% (percentage points)", float(100 * (p_hi - p_lo)), "5")
    assert e_r(float(p_hi), float(cost)) > 0 > e_r(float(p_lo), float(cost))
    assert float(p_lo) < be1 < float(p_hi), "the friction break-even must sit inside the 5-point drop"
    for wins, quoted_e, quoted_total, quoted_dollars in ((80, "0.13", "26", "13,000"), (70, "-0.02", "-4", "-2,000")):
        trades = [win_r - cost] * wins + [Fraction(-1) - cost] * (200 - wins)
        total = sum(trades)
        check(f"E_R per trade at {wins / 2:.0f}% win rate", float(total / 200), quoted_e)
        check(f"total over 200 trades at {wins / 2:.0f}% win rate (R)", float(total), quoted_total)
        check(f"total over 200 trades at {wins / 2:.0f}% win rate ($)", float(total * 500), quoted_dollars)


def binomial_se(p: float, n: int) -> float:
    """Standard error of the observed proportion from the exact binomial distribution."""
    mean = 0.0
    second = 0.0
    for k in range(n + 1):
        pmf = math.comb(n, k) * p**k * (1 - p) ** (n - k)
        mean += pmf * k / n
        second += pmf * (k / n) ** 2
    return math.sqrt(second - mean**2)


def sampling_error() -> None:
    z = bisect(lambda x: 2 * (1 - 0.5 * (1 + math.erf(x / math.sqrt(2)))) - 0.05, 0.0, 5.0)
    check("two-sided 95% normal quantile z", z, "1.96")
    p30 = 20 / 30
    se30 = binomial_se(p30, 30)
    assert abs(se30 - math.sqrt(p30 * (1 - p30) / 30)) < 1e-12
    check("observed win rate, 20 of 30 (%)", 100 * p30, "66.7")
    check("standard error, N = 30 (%)", 100 * se30, "8.6")
    check("95% interval low, N = 30 (%)", 100 * (p30 - z * se30), "49.8")
    check("95% interval high, N = 30 (%)", 100 * (p30 + z * se30), "83.5")
    assert p30 - z * se30 < 0.5, "the interval must include a coin-flip win rate"
    se50 = binomial_se(0.5, 50)
    check("95% interval low, N = 50, p = 50% (%)", 100 * (0.5 - z * se50), "36")
    check("95% interval high, N = 50, p = 50% (%)", 100 * (0.5 + z * se50), "64")


def cards() -> None:
    print("input: card mkt-trd-021 hypothetical 50% annual borrow fee; card mkt-trd-024 40% wins at 1.65R, 1.0R losses")
    print("input: card mkt-trd-025 $100,000 GMV on $25,000 equity, 10 bp round trip")
    print("input: card mkt-trd-029 hypothetical 4% bill yield, 6% gross return, 3% fees and taxes")
    trades = [100] * 8 + [-500] * 2
    check("card 011 gross wins ($)", sum(t for t in trades if t > 0), "800")
    check("card 011 gross losses ($)", -sum(t for t in trades if t < 0), "1,000")
    check("card 011 net ($)", sum(trades), "-200")

    check("card 013 STT round trip on delivery (bp)", 2 * 0.1 * 100, "20")

    loss, regain = Fraction(1, 2), Fraction(1, 1)
    assert (1 - loss) * (1 + regain) == 1
    check("card 017 gain needed after a 50% loss (%)", float(100 / (1 - loss) - 100), "100")

    check("card 021 daily cost of a 50% annual borrow fee (%)", 50 / 365, "0.137")

    win, loss_r = Fraction(165, 100), Fraction(1)
    book = [win] * 40 + [-loss_r] * 60
    pf = sum(t for t in book if t > 0) / -sum(t for t in book if t < 0)
    check("card 024 gross profit per trade (R)", float(Fraction(40, 100) * win), "0.66")
    check("card 024 gross loss per trade (R)", float(Fraction(60, 100) * loss_r), "0.60")
    check("card 024 profit factor", float(pf), "1.10")
    check("card 024 expectancy (R)", float(sum(book) / len(book)), "0.06")
    extra = Fraction(6, 100)
    assert sum(t - extra for t in book) == 0, "an extra 0.06R per trade must reach break-even"

    gmv, equity, cost_bp = 100_000, 25_000, 10
    check("card 025 leverage", gmv / equity, "4")
    check("card 025 round-trip cost ($)", gmv * cost_bp / 10_000, "100")
    check("card 025 cost / equity (%)", 100 * gmv * cost_bp / 10_000 / equity, "0.40")

    check("card 029 net return (%)", 6 - 3, "3")


def cited_arithmetic() -> None:
    check("Barber-Odean average shortfall (points)", 17.9 - 16.4, "1.5")
    check("Barber-Odean top-quintile shortfall (points)", 17.9 - 11.4, "6.5")
    check("SEBI FY 2022 profitable share (%)", 100 - 89, "11")
    check("SEBI FY 2022 traders (lakh -> million)", 45.2 * 100_000 / 1e6, "4.5")
    check("SEBI average loss per loss-maker (lakh -> rupees)", 1.1 * 100_000, "110,000")
    check("SEBI follow-up traders (crore -> million)", 1 * 10_000_000 / 1e6, "10")
    check("Example 1 round trips, 5 a day for 252 days", 5 * 252, "1,260")
    print("cited: Barber-Odean (2000) households = 66,465, 1991-1996; average turnover 75% a year")
    print("cited: Barber-Odean (2000) net returns: average 16.4%, market 17.9%, most active 11.4%")
    print("cited: Barber-Lee-Liu-Odean (2009) Taiwan 1995-1999: losses 2.2% of GDP, 2.8% of personal income")
    print("cited: Barber-Lee-Liu-Odean (2009) institutional gain about 1.5 points a year")
    print("cited: Chague-De-Losso-Giovannetti (2019) 2013-2015 cohort, at least 300 days: 97% lost money")
    print("cited: Chague-De-Losso-Giovannetti (2019) 0.4% beat USD 54 a day; best USD 310 a day, sd USD 2,560")
    print("cited: SEBI (January 2023) FY 2022: 45.2 lakh traders, top 10 brokers, 89% loss-makers")
    print("cited: SEBI (January 2023) average loss about 1.1 lakh, average profit about 1.5 lakh rupees")
    print("cited: SEBI (January 2023) costs: 28% extra on losses, 15% to 50% of profits")
    print("cited: SEBI PR 37/2024 (23 September 2024) FY 2022-FY 2024: 93% of over 1 crore lost, about 2 lakh each")
    print("cited: India STT as of November 2026: delivery 0.1% a side, futures 0.05% of sale, options 0.15% of premium")
    print("cited: US tax as of November 2026: top rate 37%, NIIT 3.8%, loss offset USD 3,000 (USD 1,500 separate)")
    print("cited: FINRA Notice 26-10: old PDT rule 4 day trades in 5 business days, USD 25,000 minimum")
    print("cited: Odean (1998) 10,000 accounts, 1987-1993; wash-sale window 30 days")
    print("cited: Barber-Odean (2001) men traded 45% more; net return cost 2.65 points men, 1.72 points women")
    print("input: zero-commission example order fee = 20 rupees per order (illustrative)")
    print("cited: FINRA Notice 26-10 approved in SEC Exchange Act Release No. 105226 (14 April 2026)")
    print("cited: intraday margin standards effective 4 June 2026; phase-in until 20 October 2027")
    print("cited: India STT derivative rates raised from 1 April 2026 (Finance Act 2026, Union Budget 2026-27)")
    print("cited: earlier India STT increases in 2023 and from 1 October 2024")
    print("cited: Thaler and Johnson (1990) house-money and break-even effects; Osler (2003) round-number order clusters")
    print("input: card mkt-trd-011 win-rate example 80%; card mkt-trd-030 round-number examples $100 and $50")
    print("input: R-multiple examples +2.5R, -1.0R and +0.5R")


if __name__ == "__main__":
    example_1_ledger()
    example_2_expectancy()
    sampling_error()
    cards()
    cited_arithmetic()
    print("all retail base-rate and cost numbers check out")
