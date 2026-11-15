---
type: guide
title: "Case File 06: 2010 Flash Crash and LOB Evaporation"
track: [quant-trader, quant-dev, quant-research]
tier: advanced
status: solid
tags: [market-history, flash-crash-2010, hft, limit-order-book, stub-quotes, cross-market-arbitrage, luld, case-study]
---

# Case File 06: 2010 Flash Crash and LOB Evaporation

## Executive Summary

On the afternoon of Thursday, May 6, 2010, major US equity indices in both futures and securities markets, already down over 4% from the prior close, fell a further 5-6% in a matter of minutes before rebounding almost as quickly (SEC-CFTC staff report, September 30, 2010).
At 2:32 p.m. a large fundamental trader, a mutual fund complex, began selling 75,000 E-Mini S&P 500 futures contracts (about $4.1 billion) through an algorithm set to execute at 9% of the previous minute's volume without regard to price or time.
High-frequency traders first absorbed the selling and then passed contracts back and forth, buy-side depth in the E-Mini fell to about $58 million, less than 1% of its morning level, and the CME Stop Logic Functionality paused the E-Mini for five seconds at 2:45:28 p.m.
In individual stocks, liquidity providers paused, internalizers routed orders to the exchanges, and over 20,000 trades across more than 300 securities executed more than 60% away from their prices moments before, some at a penny or less and some as high as $100,000.
By the close, the major indices had recovered to losses of about 3% for the day.

---

## Primary Sources and Chronology

Sources used on this page: *Findings Regarding the Market Events of May 6, 2010*, Report of the Staffs of the CFTC and SEC to the Joint Advisory Committee on Emerging Regulatory Issues (September 30, 2010); SEC Release 34-67091 (May 31, 2012) approving the Limit Up-Limit Down plan; SEC Rule 15c3-5 (adopted November 2010); SEC Rule 613 (adopted July 2012); Dodd-Frank Act section 747; US Department of Justice press release of April 21, 2015 on Navinder Singh Sarao.
The report names the seller only as "a large fundamental trader (a mutual fund complex)"; press reports at the time identified it as Waddell & Reed.

- **Morning, May 6, 2010**: Trading opens to unsettling political and economic news from Europe about the debt crisis; by 2:30 p.m. the Dow Jones Industrial Average is down about 2.5%.
- **2:32 p.m.**: The mutual fund complex starts its sell program of 75,000 E-Mini contracts to hedge an existing equity position.
- **2:32 to 2:45 p.m.**: The Sell Algorithm sells about 35,000 contracts (about $1.9 billion); all fundamental sellers combined sell more than 80,000 contracts net against about 50,000 bought net by fundamental buyers.
- **2:41 to 2:44 p.m.**: High-frequency traders, after accumulating a net long position of about 3,300 contracts, sell about 2,000 contracts to cut it while trading nearly 140,000 contracts, over 33% of volume; the E-Mini falls about 3% in four minutes.
- **2:45:13 to 2:45:27 p.m.**: HFTs trade over 27,000 contracts, about 49% of volume, while buying only about 200 contracts net, the "hot-potato" effect; the E-Mini falls a further 1.7% in 15 seconds to its intraday low of 1056.
- **2:45:28 p.m.**: Fewer than 1,050 contracts of buy-side resting orders remain, and the CME Stop Logic Functionality pauses the E-Mini for five seconds; trading resumes at 2:45:33 p.m. and prices begin to recover.
- **About 2:51 p.m.**: The Sell Algorithm finishes its program as prices rise.
- **2:40 to 3:00 p.m.**: Over 20,000 trades in more than 300 securities, many of them ETFs, execute 60% or more away from their 2:40 p.m. prices; the exchanges later break trades more than 60% away from the reference price.
- **April 21, 2015**: The US Department of Justice announces charges against Navinder Singh Sarao, a London-based futures trader, for manipulating the E-Mini market by spoofing, including on May 6, 2010.

---

## Market Backdrop and Structural Vulnerabilities

### 1. Execution by Volume Alone
The report contrasts the May 6 program with an earlier sell program by the same trader, which used a mix of manual trading and algorithms that took price, time and volume into account and took more than 5 hours to sell its first 75,000 contracts.
On May 6 the algorithm targeted only volume, and it executed the program in about 20 minutes.
The report adds that the sell program was the largest net change in daily E-Mini position of any trader since the start of 2010.

### 2. High-Frequency Intermediaries
HFTs bought the first batches of the sell program and then sold to reduce their inventory, consistent with their typical practice of trading very large volumes without holding more than three to four thousand contracts in either direction (SEC-CFTC report).
Their rapid trading raised reported volume, and the Sell Algorithm, which keyed off volume, increased its selling rate even though earlier orders had not been absorbed by fundamental buyers.
The report concludes that in times of significant volatility, high trading volume is not necessarily a reliable indicator of market liquidity.

```
+-----------------------------------------------------------------------+
|                 FLASH CRASH HOT-POTATO FEEDBACK LOOP                  |
+-----------------------------------------------------------------------+
| 1. Sell Algorithm Targets 9% of Last Minute's Volume                  |
|                                                                       |
| 2. HFTs and Intermediaries Buy the First Orders                       |
|                                                                       |
| 3. HFTs Resell to Cut Inventory                                       |
|                                                                       |
| 4. Contracts Pass Back and Forth; Reported Volume Rises               |
|                                                                       |
| 5. Higher Volume Makes the Algorithm Sell Faster                      |
|                                                                       |
| 6. Fundamental Buyers and Arbitrageurs Cannot Keep Up                 |
|                                                                       |
| 7. Buy-Side Depth Falls Below 1% of Morning Level -> Price Gap        |
+-----------------------------------------------------------------------+
```

### 3. Stub Quotes and Market Orders
Stub quotes are quotes at unrealistically low or high prices that fulfil a market maker's quoting obligation without any intention to trade (SEC-CFTC report).
When liquidity providers withdrew, market orders and stop orders that reached empty books executed against these quotes, which is how trades printed at a penny or at $100,000.

---

## Microstructure Breakdown and Liquidity Evaporation

1. **Cross-market transmission**: Cross-market arbitrageurs who bought the E-Mini sold equivalent amounts in the equity markets, such as SPY or baskets of S&P 500 stocks, so SPY also fell about 3% from 2:41 to 2:44 p.m.
2. **Liquidity providers pause**: Automated systems at many liquidity providers paused when prices moved beyond pre-set limits, and firms then weighed data reliability, risk limits, P&L and the chance of trades being broken before resuming.
3. **Internalizers route to the exchanges**: Some internalizers reduced or halted internalization of sell orders as their limits were reached and sent the orders to the public exchanges, adding to the selling there.

---

## Quantitative Autopsy

The report's figures fix the price level: 75,000 contracts at the E-Mini multiplier of $50 per index point worth about $4.1 billion implies an average index level of $4.1 \text{ billion} / (75{,}000 \times 50) = 1{,}093.33$.
The other cited pairs agree: 35,000 contracts for $1.9 billion implies 1,085.71 and 40,000 contracts for $2.2 billion implies 1,100.00, all close to the intraday low of 1056 and the pre-crash levels.

Let $D(p)$ be the resting buy depth per unit of price below the mid-price $P_0$.
A sell order of size $Q$ walks the book down to the price $P_{\text{low}}$ where:
$$\int_{P_{\text{low}}}^{P_0} D(p)\, dp = Q$$
so the marginal price impact is:
$$\frac{\partial P}{\partial Q} = \frac{1}{D(p)}$$
When liquidity providers withdraw, $D(p) \to 0$ over a range of prices and the impact per contract becomes very large, so the price jumps until it reaches the next resting orders, which on May 6 were sometimes stub quotes.
On the report's numbers, buy-side depth falling from its morning level to less than 1% of it multiplies the price impact of each contract sold by more than 100 times.

---

## Regulatory and Structural Legacy

1. **Single-stock circuit breakers and Limit Up-Limit Down**: The SEC approved single-stock circuit breakers as a pilot in 2010 and, on May 31, 2012 (Release 34-67091), the Limit Up-Limit Down plan, which prevents trades outside price bands (generally 5%, 10% or 20%, depending on the stock and price) around a reference price based on the average price over the preceding five minutes and pauses trading for five minutes if a stock stays at the band limit for 15 seconds.
2. **Market-wide circuit breakers**: On the same date the SEC approved revised market-wide halts at declines of 7%, 13% and 20% in the S&P 500 (Release 34-67090), citing the May 6 events and the Joint Advisory Committee's recommendations.
3. **Stub quotes**: In November 2010 the SEC approved exchange rules requiring market makers to quote within set percentages of the national best bid or offer, ending the practice of stub quotes.
4. **Consolidated Audit Trail**: SEC Rule 613 (July 2012) required the exchanges and FINRA to build a consolidated audit trail of orders and trades across US equity and options markets.
5. **Market Access Rule**: SEC Rule 15c3-5 (adopted November 2010) requires broker-dealers with market access to have pre-trade risk controls, ending unfiltered "naked" sponsored access.
6. **Spoofing**: Section 747 of the Dodd-Frank Act (2010) made spoofing (bidding or offering with the intent to cancel before execution) a prohibited practice under the Commodity Exchange Act.

---

## Lessons for Traders and Risk Managers

- **Avoid Unconstrained Market Orders**: In a thin electronic market a market or stop-market order has no price limit; use limit or stop-limit orders with an explicit maximum slippage.
- **Liquidity Is Endogenous and Transient**: Intermediaries supply liquidity in calm markets and pause when prices move beyond their limits, so displayed depth can vanish in seconds.
- **Volume Is Not Liquidity**: An algorithm that keys only off volume can accelerate into a market where the volume is intermediaries trading with each other.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-021 | What specific algorithmic order triggered the initial liquidity collapse during the May 6, 2010 Flash Crash?
> A mutual fund complex's program to sell 75,000 E-Mini S&P 500 contracts (about $4.1 billion) through an algorithm targeting 9% of the previous minute's volume without regard to price or time (SEC-CFTC report).

> [!question]- mkt-his-022 | What was a 'stub quote' in the pre-2010 US equity market?
> A quote at an unrealistically low or high price, such as a penny bid, posted by a market maker to meet its quoting obligation without intending to trade; on May 6 some market orders executed against them.

> [!question]- mkt-his-023 | What regulatory mechanism was approved in 2012 to prevent single-stock flash crashes like trades printing at a penny?
> The Limit Up-Limit Down plan (SEC approval May 31, 2012), which blocks trades outside price bands around a five-minute reference price and pauses trading if a stock stays at the band limit.

> [!question]- mkt-his-024 | What was the key finding of the CFTC-SEC joint report regarding High-Frequency Traders during the Flash Crash?
> HFTs first absorbed the selling, then sold to cut their inventory and traded contracts back and forth (over 27,000 contracts in 15 seconds while buying only about 200 net), which inflated volume, fed the volume-based Sell Algorithm, and did not add buy-side depth.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_hist_06_flash_crash.py`](../code/mkt_hist_06_flash_crash.py) prints and asserts every number on this page: the implied index levels are computed from three separately cited contract-value pairs and checked against each other and against the intraday low, the sell program's pieces are checked to add up, and the depth-impact multiple is computed from the report's depth figure.
- Related notes: [Case File 02: 1987 Black Monday](02-1987-Black-Monday-and-Portfolio-Insurance.md), [Case File 09: 2021 GameStop](09-2021-GameStop-Meme-Squeeze-and-DTCC-Margin-Halt.md).
