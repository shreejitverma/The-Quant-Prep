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

On the afternoon of Thursday, May 6, 2010, US equity markets experienced the most rapid and severe intraday dislocation in history.
Between 02:40 PM and 03:00 PM EST, the Dow Jones Industrial Average plummeted nearly 1,000 points (-9.2%), with 600 points of that collapse occurring within just five minutes, evaporating approximately $1 trillion in market value before recovering almost all of the loss by 03:08 PM.
The disruption originated in the CME E-mini S&P 500 futures market, triggered by a mutual fund management firm (Waddell & Reed) executing an automated algorithmic sell program for 75,000 E-mini contracts ($4.1 billion notional) programmed to target volume participation without regard to price or market impact.
As the selling overwhelmed the order book, High-Frequency Trading (HFT) firms rapidly hit internal inventory risk limits, flipped from market making to aggressive short selling, and withdrew liquidity quotes altogether.
Cross-market arbitrage transmitted the futures crash instantly into cash equity exchanges, where fragmented routing and liquidity voids caused hundreds of securities to trade at absurd "stub quotes" (such as blue-chip consulting giant Accenture trading at $0.01 per share, and Apple trading at $100,000 per share).
The event demonstrated that in algorithmic electronic markets, liquidity is transient, non-linear, and capable of vanishing in milliseconds under systemic adverse selection.

---

## Primary Sources and Chronology

- **Macro Backdrop (May 6, 2010)**: Global markets trade nervously over the European sovereign debt crisis; street protests and riots in Athens over Greek austerity measures dominate headlines.
- **02:32 PM EST**:
  - Mutual fund firm Waddell & Reed initiates an automated algorithmic sell program to hedge equity portfolio risk by selling 75,000 E-mini S&P 500 futures contracts (representing roughly 9% of total daily E-mini volume).
  - The algorithm is programmed to execute via a simple percentage-of-volume (POV) parameter: targeting a constant 9% of the trading volume executed over the previous minute, with no price boundaries or time limits.
- **02:41 PM EST**:
  - The massive influx of sell contracts rapidly consumes all available passive resting buy limit orders in the CME E-mini order book.
  - High-frequency market-making algorithms buy from the mutual fund and immediately turn around to sell to other market participants; this rapid churning artificially inflates total market volume, deceiving the POV algorithm into accelerating its selling rate even faster.
- **02:45:13 - 02:45:28 PM EST**:
  - E-mini market depth falls from approximately $6 billion to under $40 million (a 99% collapse in resting bid liquidity).
  - The E-mini contract drops 3% in four seconds.
  - At 02:45:27 PM, the CME Stop Logic Function automatically halts trading in the E-mini for five seconds to allow incoming orders to replenish the depleted book.
- **02:45:28 - 02:47:00 PM EST**:
  - While the CME futures market pauses for five seconds, the wave of panic selling spreads across the fragmented cash equity landscape (NASDAQ, NYSE Arca, BATS, Direct Edge).
  - Internalizers and dark pools divert order flow to public lit exchanges; automated routing algorithms send market orders into empty order books.
  - Over 20,000 trades execute at prices more than 60% away from fair value; roughly 30 stocks and 160 ETFs trade down to $0.01.
  - Accenture, an investment-grade firm capitalized at $30 billion, trades down from $40.00 to $0.01 across thousands of shares.
  - Sotheby's and Apple experience trades at $100,000 per share as market buy orders match against dormant stub asks.
- **02:48 - 03:08 PM EST**:
  - The CME futures market resumes trading with fresh liquidity; quantitative statistical arbitrage algorithms detect historic cash-futures valuation discrepancies and step in with massive buy orders.
  - By 03:08 PM, the market recovers roughly 600 points of the intraday drop.
- **September 30, 2010**: The Joint CFTC-SEC Advisory Committee issues its definitive 104-page investigation: *Findings Regarding the Market Events of May 6, 2010*.
- **April 21, 2015**: The US Department of Justice arrests British day trader Navinder Singh Sarao in London, charging him with wire fraud and market manipulation for placing massive phantom "spoofing" sell orders in the E-mini order book on May 6, 2010.

---

## Market Backdrop and Structural Vulnerabilities

### 1. High-Frequency Trading (HFT) and Automated Market Making
By 2010, electronic high-frequency trading firms (such as Citadel Securities, Getco, Virtu, and Tradebot) had largely replaced traditional exchange specialists.
HFTs operated on market-making algorithms that held virtually zero overnight inventory, capturing fractions of a penny on the bid-ask spread across millions of trades.
These algorithms were governed by strict intraday inventory constraints: if net position exposure exceeded a tight threshold (e.g. $5 million or 200 contracts), the algorithm instantly stopped quoting passive bids and aggressively unloaded inventory using aggressive market orders.

### 2. The Algorithmic Feedback Loop of Volume-Targeted Orders
Waddell & Reed's execution algorithm was fundamentally flawed for large-order execution.
Standard institutional execution of a 75,000-contract parent order typically spans several hours or days, incorporating price-limit floors to pause execution if price impact becomes severe.
Waddell & Reed's POV algorithm had no price limit; it simply executed 9% of the volume traded in the trailing 60 seconds:

```
+-----------------------------------------------------------------------+
|                 FLASH CRASH HFT RECYCLING FEEDBACK LOOP               |
+-----------------------------------------------------------------------+
| 1. Mutual Fund Algorithm Sells 75,000 Contracts at 9% POV             |
|                                                                       |
| 2. HFT Market Makers Buy Contracts from Algorithm                     |
|                                                                       |
| 3. HFTs Immediately Sell Contracts into the Book to Shed Inventory   |
|                                                                       |
| 4. Total Trading Volume Spikes Dramatically                           |
|                                                                       |
| 5. POV Algorithm Observes Higher Volume and ACCELERATES Selling Rate  |
|                                                                       |
| 6. HFTs Hit Risk Limits, Pull All Bids, and Become Net Sellers       |
|                                                                       |
| 7. Order Book Depth Evaporates -> Discontinuous Price Freefall        |
+-----------------------------------------------------------------------+
```

Between 02:41 PM and 02:44 PM, HFTs bought 264,000 contracts and sold 270,000 contracts, rapidly trading the same inventory back and forth.
This hot-potato volume illusion tricked the POV algorithm into dumping more than 35,000 contracts in just four minutes.

### 3. Stub Quotes and Market Order Vulnerability
Market maker regulations required registered market makers to maintain continuous two-sided quotes in assigned stocks.
To satisfy this regulatory quotation obligation while minimizing inventory exposure during extreme market volatility, market makers posted dummy placeholder quotes known as **stub quotes** (such as a bid of $0.01 and an ask of $100,000.00).
These quotes were never intended to execute; they were legal fictions.
However, when automated stop-loss orders and retail market-sell orders arrived during the liquidity void, matching engines paired incoming market orders against the nearest available quote: the $0.01 stub bids.

---

## Microstructure Breakdown and Liquidity Evaporation

The breakdown illustrated the fragmentation of the US equity market under Regulation NMS:
1. **Cross-Market Contagion**: Index arbitrageurs and high-frequency statistical arbitrage algorithms continuously hedge the price relationship between the CME E-mini futures and the 500 underlying S&P cash equities.
   When the E-mini price collapsed, arbitrage algorithms automatically dumped physical equities across all 13 US equity exchanges.
2. **Internalizer Ejection**: Broker-dealers that internalize retail order flow typically execute orders against their own internal balance sheets.
   When volatility surged beyond internal risk limits, internalizers abruptly routed all incoming retail market orders onto lit public exchanges, overwhelming lit books with aggressive sell volume.
3. **Information Uncertainty**: Because trade reporting feeds lagged and crossed prices flashed across disparate venues, market-making algorithms shut down entirely, choosing to take zero risk until pricing consensus was restored.

---

## Quantitative Autopsy

Let limit order book depth $D(p)$ represent the cumulative resting buy limit orders within distance $\Delta p$ of the mid-price $P_0$.
Under normal conditions, depth is thick:
$$D(P_0 - 0.01) \approx \$50,000,000$$
An aggressive sell order of $Q \approx \$4.1 \text{ billion}$ ($75,000$ contracts $\times$ the $\$50$ multiplier at an average index level of $4.1 \text{ billion} / 3.75 \text{ million} \approx 1,093$) arrives at rate $\lambda_{\text{sell}}$.
Its market impact $\Delta P$ is governed by the exhaustion of order book depth:
$$\int_{P_{\text{low}}}^{P_0} D(p) dp = Q$$
During the panic, the effective market-making supply rate $\lambda_{\text{MM}}$ dropped to zero as HFT algorithms withdrew:
$$\lambda_{\text{net}} = \lambda_{\text{sell}} - \lambda_{\text{MM}} \gg 0$$
When depth $D(p) \to 0$, the marginal price impact per contract sold diverges:
$$\frac{\partial P}{\partial Q} = \frac{1}{D(p)} \to \infty$$
The price function transitions from a smooth, continuous curve to a discontinuous cliff, dropping until it hits the artificial boundary condition of the $0.01 stub quote.

---

## Regulatory and Structural Legacy

The 2010 Flash Crash revolutionized electronic trading oversight and market microstructure rules:
1. **Limit-Up / Limit-Down (LULD) Mechanism**: Implemented in 2012 to replace individual stock circuit breakers; establishes dynamic price bands (typically 5%, 10%, or 20% around the trailing 5-minute average price) preventing trades outside the band and triggering automatic 5-minute pauses if the band is tested for 15 seconds.
2. **Elimination of Stub Quotes**: The SEC banned stub quotes in 2010, mandating that registered market makers maintain quotes within specified percentages (e.g. 8% or 20%) of the National Best Bid and Offer (NBBO).
3. **Consolidated Audit Trail (CAT)**: The SEC mandated the creation of CAT, a massive tracking system tracking every quote, order, modification, cancellation, and trade across all US equity and options exchanges from inception to execution.
4. **SEC Rule 15c3-5 (Market Access Rule)**: Required broker-dealers to implement pre-trade risk controls and capital limits on all algorithms, strictly prohibiting unfiltered, direct "naked" sponsored access to exchange matching engines.
5. **Anti-Spoofing Enforcement (Dodd-Frank Section 747)**: Made spoofing (bidding or offering with the intent to cancel before execution) an explicit federal crime, culminating in the criminal prosecution of Sarao and institutional algorithmic trading desks.

---

## Lessons for Traders and Risk Managers

- **Never Use Unconstrained Market Orders**: In an illiquid electronic market, a market order or stop-market order is an open check; always use limit orders or marketable stop-limit orders with explicit maximum slippage tolerances.
- **Liquidity Is Endogenous and Transient**: High-frequency market makers provide liquidity in calm regimes but systematically withdraw in stressful regimes; advertised order book depth can vanish within milliseconds.
- **Volume-Participation Algorithms Can Become Destructive**: POV algorithms can create positive feedback loops when interacting with high-frequency market participants, artificially inflating market volume and driving prices into vacuums.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-021 | What specific algorithmic order triggered the initial liquidity collapse during the May 6, 2010 Flash Crash?
> A mutual fund (Waddell & Reed) sell program executing 75,000 E-mini S&P 500 contracts via a 9% percentage-of-volume (POV) algorithm without price limits.

> [!question]- mkt-his-022 | What was a 'stub quote' in the pre-2010 US equity market?
> An artificial placeholder quote (such as $0.01 bid or $100,000 ask) posted by market makers solely to satisfy nominal regulatory quoting obligations.

> [!question]- mkt-his-023 | What regulatory mechanism was implemented in 2012 to prevent single-stock flash crashes like Accenture trading at $0.01?
> The Limit-Up / Limit-Down (LULD) mechanism, which halts trading if prices breach dynamic percentage bands.

> [!question]- mkt-his-024 | What was the key finding of the CFTC-SEC joint report regarding High-Frequency Traders during the Flash Crash?
> HFTs rapidly hit internal inventory limits and began aggressively dumping contracts back into the book, recycling inventory and withdrawing passive liquidity.
