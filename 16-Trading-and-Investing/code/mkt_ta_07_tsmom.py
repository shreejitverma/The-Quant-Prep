"""Time-series momentum sizing and signal arithmetic: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/07-Time-Series-Momentum-and-Trend-Following.md`.
Independent routes used here:
- each position's target notional and contract count against the dollar volatility it actually carries
  (contracts x contract notional x volatility) compared with the instrument's risk budget;
- the portfolio volatility of N equal risk budgets in closed form against a seeded simulation of N
  uncorrelated instruments, with a tolerance of five standard errors of the sample volatility;
- the equal-weight multi-horizon signal by enumerating every combination of four lookback signs;
- the EWMA centre of mass delta / (1 - delta) by summing the weights explicitly;
- the identity t / sqrt(t^2 + df) = sample correlation of price with time, with t from an OLS fit and its
  residual standard error and the correlation from numpy.corrcoef, on seeded random paths;
- instrument counts cited from Moskowitz, Ooi and Pedersen (2012) and Hurst, Ooi and Pedersen (2017),
  checked to add up to the totals the papers state.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_ta_07_tsmom.py`.
"""

from __future__ import annotations

import itertools
import math

import numpy as np

SEED = 7


def check(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{value:,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def sizing() -> None:
    capital, n_instr, target = 10_000_000, 20, 0.12
    print(f"input: capital ${capital:,}, {n_instr} instruments, {100 * target:.0f}% volatility target per sleeve")
    print("input: Example 1 crude oil at $80 with 30% volatility; Example 2 at $100 with 60% volatility")
    print("cited: NYMEX CL contract = 1,000 barrels")
    sleeve = capital / n_instr
    budget = sleeve * target  # dollar volatility the crude-oil sleeve may carry
    check("capital per instrument", sleeve, "500,000.00")
    check("dollar-volatility budget per instrument", budget, "60,000")
    multiplier = 1_000  # NYMEX CL: 1,000 barrels per contract
    # Example 1: price 80, volatility 30%.
    notional = sleeve * target / 0.30
    check("vol scalar 0.12 / 0.30", target / 0.30, "0.40")
    check("notional as a share of the allocation, percent", 100 * target / 0.30, "40")
    check("target notional at 30% vol", notional, "200,000.00")
    check("contract notional at $80", 80 * multiplier, "80,000.00")
    contracts = notional / (80 * multiplier)
    check("contracts implied", contracts, "2.5")
    held = math.floor(contracts)
    check("contracts bought (rounded down)", held, "2")
    check("notional held", held * 80 * multiplier, "160,000")
    check("dollar volatility held at 30% vol", held * 80 * multiplier * 0.30, "48,000")
    assert held * 80 * multiplier * 0.30 <= budget < (held + 1) * 80 * multiplier * 0.30
    # Example 2: price 100, volatility 60%.
    notional2 = sleeve * target / 0.60
    check("vol scalar 0.12 / 0.60", target / 0.60, "0.20")
    check("target notional at 60% vol", notional2, "100,000.00")
    check("contracts implied at $100", notional2 / (100 * multiplier), "1.0")
    check("dollar volatility of 2 contracts at $100 and 60% vol", 2 * 100 * multiplier * 0.60, "120,000")
    check("dollar volatility of 1 contract at $100 and 60% vol", 1 * 100 * multiplier * 0.60, "60,000")
    assert 1 * 100 * multiplier * 0.60 == budget


def portfolio_vol(rng: np.random.Generator) -> None:
    n, target = 20, 0.12
    per_instr = target / n
    check("annual volatility per instrument sleeve, percent of capital", 100 * per_instr, "0.60")
    closed_uncorr = per_instr * math.sqrt(n)
    check("portfolio volatility if the 20 sleeves are uncorrelated, percent", 100 * closed_uncorr, "2.68")
    check("portfolio volatility if they are perfectly correlated, percent", 100 * per_instr * n, "12.00")
    years = 200_000
    sleeves = rng.normal(0.0, per_instr, size=(years, n))
    port = sleeves.sum(axis=1)
    sd = port.std(ddof=1)
    se = sd / math.sqrt(2 * (years - 1))
    assert abs(sd - closed_uncorr) < 5 * se, f"simulated {sd} vs closed form {closed_uncorr}"
    print(f"simulated uncorrelated portfolio volatility (seed {SEED}) = {100 * sd:.3f}% +/- {100 * se:.3f}%")
    scale = target / closed_uncorr
    check("leverage on every sleeve to reach 12% when uncorrelated (sqrt 20)", scale, "4.47")


def multi_horizon() -> None:
    weights = [0.25] * 4
    values: dict[float, int] = {}
    for signs in itertools.product((-1, 1), repeat=4):
        v = round(sum(w * s for w, s in zip(weights, signs, strict=True)), 10)
        values[v] = values.get(v, 0) + 1
    assert values == {-1.0: 1, -0.5: 4, 0.0: 6, 0.5: 4, 1.0: 1}, values
    print("equal-weight 1/3/6/12-month signal takes only -1, -0.5, 0, +0.5, +1 (counts 1, 4, 6, 4, 1 of 16)")


def ewma_centre_of_mass() -> None:
    i = np.arange(0, 20_000)
    for delta, quoted in ((60 / 61, "60.0"), (0.94, "15.7")):
        w = (1 - delta) * delta**i
        com = float(np.sum(i * w) / np.sum(w))
        assert abs(com - delta / (1 - delta)) < 1e-6
        check(f"centre of mass of EWMA weights, delta = {delta:.5f}, days", com, quoted)
    check("delta for a 60-day centre of mass (60 / 61)", 60 / 61, "0.9836")
    check("RiskMetrics 1 - lambda", 1 - 0.94, "0.06")


def trend_t_identity(rng: np.random.Generator) -> None:
    for _ in range(5):
        n = int(rng.integers(30, 300))
        time = np.arange(n, dtype=float)
        price = np.cumsum(rng.normal(0.05, 1.0, size=n))
        x = time - time.mean()
        slope = np.sum(x * (price - price.mean())) / np.sum(x * x)
        resid = price - price.mean() - slope * x
        se = math.sqrt(np.sum(resid**2) / (n - 2) / np.sum(x * x))
        t = slope / se
        r = np.corrcoef(time, price)[0, 1]
        assert abs(t / math.sqrt(t * t + n - 2) - r) < 1e-10
    print("t / sqrt(t^2 + (n - 2)) equals the price-time correlation on 5 random paths")


def cited_counts() -> None:
    mop = {"commodities": 24, "currency pairs": 12, "equity indices": 9, "bond futures": 13}
    hop = {"commodities": 29, "equity indices": 11, "bond markets": 15, "currency pairs": 12}
    check("Moskowitz-Ooi-Pedersen instruments", sum(mop.values()), "58")
    check("Hurst-Ooi-Pedersen markets", sum(hop.values()), "67")
    check("years in 1880 to 2016 inclusive", 2016 - 1880 + 1, "137")
    check("years in the MOP strategy sample, 1985 to 2009 inclusive", 2009 - 1985 + 1, "25")
    print("cited: MOP 52 of 58 significant at 5%, TSMOM alpha on XSMOM t = 5.90; HOP 10% vol target, 2-and-20 fees")
    print("cited: MOP diversified TSMOM alpha over cross-sectional momentum 76 bp a month (t = 5.90)")
    print("cited: HOP positive in 8 of the 10 largest US 60/40 drawdowns since 1880, which lasted about 15 months on average")
    print("cited: HOP gross Sharpe ratio per market about 0.4")
    print("cited: MOP diversified TSMOM portfolio Sharpe ratio above one, 1985 to 2009")
    print("cited: MOP size each instrument to 40% annualized ex-ante volatility; HOP combined portfolio 10%")
    print("cited: Lemperiere et al. (2014) trend t-statistic about 5 since 1960 and about 10 since 1800")
    print("cited: trailing 12-month crude oil return +35.0% (Example 1 input), US portfolio 60/40, S&P 500")


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    sizing()
    portfolio_vol(rng)
    multi_horizon()
    ewma_centre_of_mass()
    trend_t_identity(rng)
    cited_counts()
    print("all time-series momentum numbers check out")
