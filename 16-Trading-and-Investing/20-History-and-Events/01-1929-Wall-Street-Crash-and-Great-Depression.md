---
type: guide
title: "Case File 01: 1929 Wall Street Crash and the Great Depression"
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
tags: [market-history, 1929-crash, great-depression, margin-calls, leverage, ticker-lag, case-study]
---

# Case File 01: 1929 Wall Street Crash and the Great Depression

## Executive Summary

Between September 3 and November 13, 1929, the Dow Jones Industrial Average collapsed by 48%, initiating a devastating deflationary bear market that ultimately bottomed in July 1932 at an 89.2% cumulative peak-to-trough decline.
The crash was driven by extreme broker loan credit expansion (10% upfront margin requirements), widespread retail leverage, speculative investment trusts, and a catastrophic microstructural breakdown in information dissemination caused by mechanical ticker tape lag.
The ensuing banking panic destroyed 9,000 commercial banks, collapsed the money supply by one-third, and prompted the foundational modern regulatory architecture of American finance: the Glass-Steagall Act of 1933, the Securities Act of 1933, the Securities Exchange Act of 1934, and the creation of the SEC.

---

## Primary Sources and Chronology

- **September 3, 1929**: The Dow Jones Industrial Average peaks at 381.17 following an unprecedented six-year bull market fueled by cheap call-money lending.
- **September 5, 1929**: Roger Babson delivers his famous "Babson Break" speech at the National Business Conference, warning that a crash of 60 to 80 points is imminent.
- **October 24, 1929 (Black Thursday)**:
  - Opening volume overwhelms the floor, with ticker tape lagging actual floor transactions by more than 90 minutes.
  - At 12:00 PM, Richard Whitney (Vice President of the NYSE and floor broker for J.P. Morgan & Co.) walks onto the floor and visibly places orders to buy 10,000 shares of US Steel at $205, temporarily arresting the panic.
  - Record volume of 12,894,650 shares trades in a single session.
- **October 28, 1929 (Black Monday)**:
  - Massive margin calls go unanswered over the weekend as commercial banks and regional brokers refuse to extend call-money loans.
  - The Dow Jones Industrial Average plunges 38.33 points (-12.82%), closing at 260.64 on 9,212,800 shares.
- **October 29, 1929 (Black Tuesday)**:
  - Complete panic liquidation takes hold with 16,410,030 shares traded, a volume record that stands unbroken for nearly 40 years until May 1968.
  - The Dow falls another 30.57 points (-11.73%), closing at 230.07 with leading blue chips trading at price discounts exceeding 40%.
- **November 13, 1929**: The initial crash sequence bottoms temporarily at 198.69 before an intermediate bear market rally.
- **July 8, 1932**: The multi-year bear market reaches its ultimate depression nadir with the Dow closing at 41.22, erasing three decades of capital accumulation.

---

## Market Backdrop and Structural Vulnerabilities

### 1. Excessive Margin Lending (10% Down)
In 1929, retail investors could purchase equities with as little as 10% equity collateral, borrowing the remaining 90% from brokerage houses via broker loans (call money).
Brokers financed these loans by borrowing directly from commercial banks and non-financial corporations (such as Standard Oil of New Jersey and Bethlehem Steel), who deposited billions in cash into the New York call money market to earn 12% to 20% annualized overnight interest.
Total broker loans peaked at $8.54 billion in October 1929, representing an astonishing proportion of total US bank credit and rendering the entire market hyper-vulnerable to price drawdowns.

### 2. Ticker Tape Lag and Information Asymmetry
Stock prices were communicated to regional brokerage offices and the public via the Western Union and New York Quotation Company telegraphic ticker tapes.
The electromechanical ticker machines could print at a maximum speed of roughly 285 characters per minute.
On Black Thursday and Black Tuesday, trading volume exceeded printer bandwidth by an order of magnitude, causing the tape to lag floor trading by up to two and a half hours.
Traders outside the physical exchange floor had no accurate knowledge of prevailing bid-ask prices, sparking blind panic selling to exit positions before collateral was completely wiped out.

### 3. Investment Trust Pyramiding
The late 1920s witnessed the explosion of leveraged closed-end investment trusts (such as Goldman Sachs Trading Corporation and Shenandoah Corporation).
Trusts issued debt, preferred stock, and common stock to purchase shares of other investment trusts, creating extreme structural leverage.
When underlying equity values declined by 10%, the equity tranches of these layered investment pyramids suffered 100% total losses.

---

## Microstructure Breakdown and Liquidity Evaporation

```
+-----------------------------------------------------------------------+
|                 1929 LIQUIDATION CASCADE FEEDBACK LOOP                |
+-----------------------------------------------------------------------+
| 1. Modest Price Drop (e.g. -5%)                                       |
|    Triggers maintenance margin breaches on 10%-margin retail accounts |
|                                                                       |
| 2. Unanswered Margin Calls                                            |
|    Brokers issue telegram margin calls; borrowers fail to deliver cash|
|                                                                       |
| 3. Forced Market Sell Orders                                          |
|    Brokers seize collateral and dump market-on-open orders on NYSE    |
|                                                                       |
| 4. Information Blackout (Ticker Tape 150 Minutes Late)                |
|    Floor specialists retreat bids; market orders execute into air     |
|                                                                       |
| 5. Severe Price Collapse (-12% in hours)                              |
|    Breaches higher-margin institutional and banking tiers (Contagion) |
+-----------------------------------------------------------------------+
```

Because specialist market makers on the NYSE had limited personal balance sheet capital, they could not absorb the millions of forced market sell orders arriving simultaneously.
Bid quotes collapsed downward in huge discontinuous gaps, clearing trades only at catastrophic discounts.

---

## Quantitative Autopsy

Let initial stock price be $S_0 = 100$, purchased on 10% margin with $10 equity collateral and $90 borrowed call loan debt:
$$\text{Account Equity} = E(S) = S - \text{Debt} = S - 90$$
$$\text{Margin Percentage} = M(S) = \frac{S - 90}{S}$$
When the stock drops by just 10% to $S_1 = 90$, equity drops to:
$$E(90) = 90 - 90 = 0$$
The investor suffers a 100% loss of initial capital on a mere 10% market drawdown.
If the broker is unable to execute a sale immediately due to ticker lag and floor congestion, selling instead at $S_2 = 82$, the account finishes in a deficit balance:
$$E(82) = 82 - 90 = -8$$
The broker absorbs an unsecured credit loss of $8 per share, which is immediately transmitted to the commercial bank that provided the overnight broker loan.

---

## Regulatory and Structural Legacy

The 1929 crash fundamentally reshaped global financial architecture:
1. **Federal Reserve Regulation T (1934)**: Granted the Federal Reserve Board authority to mandate minimum initial margin requirements, raising margin from 10% to 50% (and periodically up to 100%).
2. **Glass-Steagall Banking Act of 1933**: Strictly separated commercial banking (deposit taking) from investment banking (equity underwriting and speculation) and established the FDIC.
3. **Securities Act of 1933 & Securities Exchange Act of 1934**: Mandated standardized registration statements, audited financial reporting, continuous 10-K/10-Q disclosures, and created the Securities and Exchange Commission (SEC).
4. **Pecora Commission Investigation**: Publicly exposed rampant insider market manipulation, pool syndicates, and fraudulent investment trust valuations.

---

## Lessons for Traders and Risk Managers

- **Leverage Inverts Probability**: High leverage turns survivable drawdowns into fatal bankruptcies; any strategy requiring more than 2x leverage to generate acceptable returns possesses negative convexity.
- **Microstructural Bandwidth Bottlenecks**: In severe crises, market data feeds lag, order entry systems reject orders, and market participants trade blind.
- **Credit Contagion Across Asset Classes**: Equity collateral liquidations instantly freeze wholesale short-term money market lending.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-001 | What was the standard retail margin requirement in the US equity markets leading up to the 1929 crash?
> Roughly 10% upfront equity collateral, allowing 10x effective leverage.

> [!question]- mkt-his-002 | How did the electromechanical ticker tape lag amplify the panic during Black Thursday and Black Tuesday?
> The ticker ran up to 150 minutes late, preventing traders outside the floor from knowing real-time prices and triggering blind panic liquidation.

> [!question]- mkt-his-003 | What regulatory authority did the Federal Reserve receive under Regulation T of 1934?
> The authority to set and enforce mandatory minimum initial margin requirements for securities purchases.

> [!question]- mkt-his-004 | What happened to the Dow Jones Industrial Average between its September 1929 peak and July 1932 trough?
> It dropped from 381.17 to 41.22, representing an 89.2% cumulative decline.
