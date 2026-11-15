---
type: guide
title: "Case File 02: 1987 Black Monday and Portfolio Insurance"
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
tags: [market-history, 1987-crash, black-monday, portfolio-insurance, dynamic-hedging, circuit-breakers, case-study]
---

# Case File 02: 1987 Black Monday and Portfolio Insurance

## Executive Summary

On Monday, October 19, 1987, the Dow Jones Industrial Average fell 508 points, from 2,246.74 to 1,738.74, a one-day decline of 22.61% on New York Stock Exchange volume of 604 million shares; the S&P 500 fell about 20 percent and S&P 500 futures fell 29 percent.
Federal Reserve History describes it as the largest one-day stock market decline in history.
The Brady Report (January 1988) found that the selling began with mechanical, price-insensitive selling by institutions using portfolio insurance and by a few mutual fund groups meeting redemptions, and that index arbitrage carried futures selling into the stock market.
Portfolio insurance replicates a protective put by selling stock index futures as prices fall, and $60 to $90 billion of equity assets were under portfolio insurance administration when the market broke.
Order-handling systems were overwhelmed: some NYSE DOT orders backed up for up to one and one quarter hours, and late on October 19 the S&P 500 futures traded at a discount of 20 index points to the cash index.

---

## Primary Sources and Chronology

Sources used on this page: *Report of the Presidential Task Force on Market Mechanisms* (the Brady Report, January 1988), chapters 1 and 3, Study III and Study VI; Mark Carlson, "A Brief History of the 1987 Stock Market Crash with a Discussion of the Federal Reserve Response", Federal Reserve Board FEDS 2007-13 (2007); Donald Bernhardt and Marshall Eckblad, "Stock Market Crash of 1987", Federal Reserve History (2013); SEC Release 34-67090 (May 31, 2012) on market-wide circuit breakers; Dow closes and daily point changes for October 13 to 19, 1987, as reported at the time (contemporary press reports).

- **August 25, 1987**: The Dow reaches a record close of 2,722 (Brady Report, Study III), after gaining 44 percent in seven months (Federal Reserve History).
- **Wednesday, October 14, 1987**: News that the House Ways and Means Committee had filed legislation to remove tax benefits of merger financing, and a worse-than-expected trade deficit, start the decline (Carlson 2007); the Dow falls 95 points on volume of 207 million shares (Brady Report).
- **Friday, October 16, 1987**: Stock index options expire; the Dow falls 108 points (4.6 percent), then the largest one-day point drop ever, on volume of 338 million shares, and the S&P 500 is down over nine percent for the week (Brady Report; Carlson 2007).
- **Monday, October 19, 1987 (Black Monday)**:
  - Many NYSE stocks do not open in the first hour; by 10:00 a.m. 95 S&P 500 stocks representing 30% of the index value had still not opened (SEC report quoted in Carlson 2007).
  - Shortly after 1:00 p.m., a news report of SEC Chairman David Ruder's remarks about a possible "very temporary" halt in trading spreads rumours of an NYSE closure (Carlson 2007; Ruder later testified that he had been misinterpreted).
  - In the last hour and one quarter of stock trading the Dow falls almost 300 points to close at 1,738.74, down 508 points.
- **Tuesday, October 20, 1987**:
  - At 8:41 a.m., before markets open, the Federal Reserve issues its statement: "The Federal Reserve, consistent with its responsibilities as the Nation's central bank, affirmed today its readiness to serve as a source of liquidity to support the economic and financial system" (Carlson 2007).
  - The Fed's open market operations push the federal funds rate down to around 7 percent from over 7.5 percent, and the 10 largest New York banks nearly double their lending to securities firms that week (Carlson 2007; Federal Reserve History).
  - The CBOE suspends stock index options trading at 11:45 a.m. and the CME suspends S&P 500 futures at 12:15 p.m.; at the CME closing the futures discount was more than 46 points, the largest ever (Brady Report, Study III).

---

## Market Backdrop and Structural Vulnerabilities

### 1. The Portfolio Insurance Boom
Portfolio insurance used computer models to compute optimal stock-to-cash ratios at each market level, cutting the stock weight as prices fell (Brady Report; Carlson 2007).
The replication idea is in Mark Rubinstein and Hayne Leland, "Replicating Options with Positions in Stock and Cash", *Financial Analysts Journal* 37(4), 1981, and their firm Leland O'Brien Rubinstein Associates was a leading vendor.
Most insurers traded index futures rather than stocks, because futures were cheaper and several vendors were authorised to trade only futures for their clients (Brady Report).
The Brady Report states that $60 to $90 billion of equity assets were under portfolio insurance administration at the time of the market break, an amount that had more than quadrupled during 1987.

### 2. The Theoretical Premise vs Operational Reality
Portfolio insurance follows the Black-Scholes-Merton (1973) logic of dynamic delta hedging.
To replicate a put option with delta $\Delta(S, t)$, the hedger must sell stock (or short index futures) as the price $S$ falls:
$$\Delta_{\text{put}}(S) = N(d_1) - 1 < 0$$
$$\frac{\partial |\Delta_{\text{put}}|}{\partial S} < 0$$
Because the put delta becomes more negative as prices fall, the hedge requires selling into a declining market.
The replication argument assumes continuous trading, no price impact and no gaps between prices.
When many institutions run the same rule at once, their combined selling becomes a large share of the market and moves the price they are reacting to.
The Brady Report notes that the typical model called for stock sales of more than 20 percent of a portfolio in response to a 10 percent market decline.

### 3. NYSE DOT System Bottlenecks
The Designated Order Turnaround (DOT) system routed member firms' orders electronically to the specialist posts, which made program trading practical (Carlson 2007).
On October 19, orders for 396 million shares were entered into DOT, and the mechanical printers at some posts were overwhelmed (Brady Report).
DOT limit orders to some posts backed up for up to one and one quarter hours at the worst time, and trade executions were reported more than an hour late (Brady Report, Study VI; Carlson 2007).

---

## Microstructure Breakdown and Liquidity Evaporation

```
+-----------------------------------------------------------------------+
|               1987 PORTFOLIO INSURANCE CASCADE FEEDBACK LOOP          |
+-----------------------------------------------------------------------+
| 1. Equity Market Declines                                             |
|    Insurance models call for a lower stock weight                     |
|                                                                       |
| 2. Futures Selling                                                    |
|    Insurers sell S&P 500 futures to cut exposure                      |
|                                                                       |
| 3. Futures Discount Widens                                            |
|    Futures trade well below the cash index                            |
|                                                                       |
| 4. Index Arbitrage                                                    |
|    Arbitrageurs buy futures and sell stocks through DOT               |
|                                                                       |
| 5. DOT and Specialist Overload                                        |
|    Order backlogs; stocks open late or halt                           |
|                                                                       |
| 6. Linkage Breaks                                                     |
|    Arbitrage stops; the futures discount signals further declines     |
|    and the insurance models call for more selling                     |
+-----------------------------------------------------------------------+
```

On the afternoon of October 19, with some index arbitrageurs unwilling to sell stock through DOT, they also stopped buying futures, and the futures fell to a discount of 20 index points (Brady Report).
The large discount itself discouraged buyers in the stock market, and the Dow fell almost 300 points in the last hour and one quarter of trading.
In the futures market, portfolio insurers sold the equivalent of $4 billion of stocks on October 19, over 40 percent of futures volume excluding locals (Brady Report).

---

## Quantitative Autopsy

The overhang is the gap between what the models demanded and what had been sold.
With the market already down 10 percent by Friday, October 16, the models dictated that at least $12 billion (20 percent of $60 billion) of equities should already have been sold, but less than $4 billion had in fact been sold (Brady Report).

The convexity of the hedge can be seen with a hypothetical put: strike $K = 95$, volatility $\sigma = 20\%$, maturity $T = 0.5$ years and zero interest rate, under Black-Scholes:
$$\Delta(S) = N\left(\frac{\ln(S/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}\right) - 1$$
At $S_0 = 100$ the put delta is $-0.3324$, and at $S_1 = 90$ it is $-0.6223$.
A 10% fall in the index therefore raises the hedge from 33.24% to 62.23% of the portfolio, close to double, exactly as liquidity is draining.
The required short futures position for a portfolio of value $V$ is:
$$H(S) = |N(d_1) - 1| \times \frac{V}{S \times \text{Multiplier}}$$
so every institution running the same rule must add short futures at the same moment.

The headline moves follow from the cited closes: $508.00/2{,}246.74 = 22.61\%$ on October 19.
Adding the daily falls of 108.35 (October 16), 57.61 (October 15) and 95.46 (October 14) points back to the October 16 close of 2,246.74 recovers the October 13 close of 2,508.16 (contemporary press reports).
From 2,508.16 to 1,738.74 is a fall of 769.42 points, or 30.68%, which the Brady Report gives as 769 points or 31 percent (chapter 1, p. 1).
Its Study III (p. III-1) works from rounded levels of 2,505 and 1,738 and gives 30.6 percent.

---

## Regulatory and Structural Legacy

1. **Circuit breakers**: The Brady Report recommended that circuit breaker mechanisms (such as price limits and coordinated trading halts) be formulated and implemented, and after the market breaks of October 1987 and October 1989 the NYSE instituted market-wide circuit breakers (Federal Reserve History).
   By 2012 the halts were triggered by declines of 10%, 20% and 30% in the Dow; SEC Release 34-67090 (May 31, 2012) replaced these with declines of 7%, 13% and 20% in the S&P 500.
2. **Unified clearing and consistent margins**: The Brady Report recommended that clearing systems be unified across marketplaces and that margins be made consistent across marketplaces.
3. **Central bank liquidity**: The Federal Reserve's October 20 statement and open market operations, and its encouragement of bank lending to securities firms, became a model for crisis liquidity support (Carlson 2007).
4. **One coordinating agency**: The Brady Report recommended that one agency coordinate the few critical regulatory issues that cut across the stock, options and futures markets.

---

## Lessons for Traders and Risk Managers

- **Endogenous Feedback Loops**: When many participants follow rules that sell into falling prices, their selling becomes the price move they react to.
- **Dynamic Hedging Cannot Handle Gap Risk**: Delta hedging only works if prices move continuously; in a gap, the hedge cannot be rebalanced at model prices.
- **Arbitrage Requires Working Plumbing**: When order routing jams, arbitrage stops and the price link between futures and cash breaks.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-005 | What was the percentage decline of the Dow Jones Industrial Average on Black Monday (October 19, 1987)?
> 22.61%, or 508.00 points from 2,246.74 to 1,738.74, which Federal Reserve History calls the largest one-day stock market decline in history.

> [!question]- mkt-his-006 | What was the mathematical flaw in the Portfolio Insurance strategy developed by Leland and Rubinstein?
> It relied on continuous trading with no price impact; when many insurers sold together, their selling moved prices, gaps appeared, and the hedge could not be rebalanced at model prices.

> [!question]- mkt-his-007 | How did the NYSE DOT system queue congestion amplify the 1987 crash?
> DOT orders backed up for up to one and one quarter hours and executions were reported more than an hour late, so index arbitrageurs could not execute or confirm the stock side of their trades, they stopped buying futures, and the futures fell to a 20-point discount.

> [!question]- mkt-his-008 | What major structural reform did the Brady Commission report recommend that markets later adopted?
> Coordinated circuit breakers (price limits and trading halts) across markets, which the NYSE instituted as market-wide circuit breakers after the 1987 and 1989 market breaks.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_hist_02_1987_crash.py`](../code/mkt_hist_02_1987_crash.py) prints and asserts every number on this page: the index moves are recomputed from the cited closes and checked against the Brady Report's rounded figures, the October 13 close is recovered from the October 14 to 16 daily changes, the overhang is checked as stated, and the put deltas come from the closed-form $N(d_1)$ checked against a central finite difference of a put price obtained by numerical integration of the payoff over the lognormal density.
- Related notes: [Case File 01: 1929 Crash](01-1929-Wall-Street-Crash-and-Great-Depression.md), [Case File 06: 2010 Flash Crash](06-2010-Flash-Crash-and-LOB-Evaporation.md).
