---
type: guide
title: "Case File 07: 2015 Swiss Franc Unpeg and Broker Insolvency"
track: [quant-trader, quant-risk]
tier: core
status: solid
tags: [market-history, swiss-franc-2015, snb-unpeg, currency-pegs, fxcm, alpari, gap-risk, negative-balances, case-study]
---

# Case File 07: 2015 Swiss Franc Unpeg and Broker Insolvency

## Executive Summary

On the morning of Thursday, January 15, 2015, the Swiss National Bank (SNB) stunned global financial markets by abruptly abandoning its three-year-old minimum exchange rate ceiling of 1.20 Swiss Francs per Euro (EUR/CHF).
Within thirteen minutes of the 09:30 AM CET announcement, the Swiss Franc appreciated by over 30% against the Euro, briefly spiking to parity (1.00) and reaching an extreme low of 0.85 EUR/CHF.
The sudden policy reversal vaporized global foreign exchange liquidity: major Tier-1 interbank liquidity providers (Deutsche Bank, UBS, Barclays, Citigroup) pulled all electronic bid quotes, leaving the EUR/CHF order book completely devoid of pricing between 1.1990 and 1.0000.
Stop-loss orders submitted by thousands of leveraged retail traders and institutional funds failed to execute anywhere near their invalidation prices, suffering catastrophic gap slippage of 1,500 to 2,500 pips.
Because retail FX brokers offered leverage ratios ranging from 100-to-1 to 400-to-1, client account balances blew through zero and deep into negative territory within seconds.
The resulting bad-debt shortfalls caused the immediate insolvency and bankruptcy of major retail brokers (including Alpari UK and Excel Markets), while FXCM (the largest retail broker in the US) required an emergency $300 million high-interest rescue loan from Leucadia National to avoid liquidation.

---

## Primary Sources and Chronology

- **September 6, 2011**: The Swiss National Bank introduces a mandatory floor of 1.20 Francs per Euro, declaring it will enforce this minimum exchange rate with "utmost determination" and is prepared to buy foreign currency in unlimited quantities to prevent the deflationary overvaluation of the Franc during the European sovereign debt crisis.
- **December 18, 2014**: The SNB introduces negative interest rates (-0.25% on sight deposit balances exceeding exemption thresholds) to discourage international Franc hoarding.
- **January 12, 2015**: SNB Vice President Jean-Pierre Danthine reaffirms in an interview with Swiss television that the 1.20 floor remains "the cornerstone" of SNB monetary policy.
- **Thursday, January 15, 2015**:
  - 09:30 AM CET (03:30 AM EST): The SNB issues a brief three-paragraph press release: *Swiss National Bank Discontinues Minimum Exchange Rate and Lowers Interest Rate to -0.75%*.
  - 09:30:15 CET: Algorithmic news scanners read the announcement; automated buy orders for CHF hit the interbank electronic matching networks (EBS and Reuters Matching).
  - 09:31:00 CET: The SNB's massive standing limit order buying EUR/CHF at 1.2000 disappears from EBS; interbank market-making algorithms immediately freeze and withdraw all bids.
  - 09:33:00 CET: EBS trading records reveal a complete liquidity void: between 1.1500 and 1.0200, there are zero bids on the order book.
  - 09:43:00 CET: EUR/CHF prints an extreme low of 0.8500 (an intraday currency spike of 41.2%), before stabilizing around 1.0200-1.0400.
  - 03:00 PM EST: Major global investment banks tally massive trading losses: Citigroup loses over $150 million, Deutsche Bank loses $150 million, and Barclays loses over $100 million in unhedged client and prop exposures.
- **Friday, January 16, 2015**:
  - Alpari (UK) Limited officially enters insolvency administration, reporting that catastrophic client negative balances wiped out firm equity.
  - Excel Markets in New Zealand announces it has suffered total loss of operating capital and ceases operations.
  - FXCM announces that retail clients suffered negative balances exceeding $225 million, creating a regulatory net capital deficit; shares plunge 88% before trading is halted.
  - Leucadia National Corporation structures an emergency $300 million secured credit facility with a 10% to 20% coupon to recapitalize FXCM and save it from regulatory shutdown.

---

## Market Backdrop and Structural Vulnerabilities

### 1. The "Free Money" Peg Illusion
For over three years, market participants treated the 1.2000 EUR/CHF floor as a quasi-sovereign guarantee.
Retail traders and systematic algorithmic funds established massive carry trades:
- Buying EUR/CHF at 1.2005 or 1.2010.
- Setting stop-losses tightly at 1.1990 (risking only 15 to 20 pips).
- Collecting the interest rate differential with high leverage (often 200:1 or 400:1).
Traders believed the downside was capped at 1.1990 because the Swiss National Bank was legally committed to buying unlimited Euros at 1.2000.
This moral hazard encouraged unprecedented concentration of long EUR/CHF positions across retail brokers worldwide.

### 2. The SNB's Expanding Balance Sheet Trap
To defend the 1.20 floor throughout 2014, the SNB was forced to print hundreds of billions of Swiss Francs to purchase Euros.
By late 2014, the European Central Bank (ECB), led by Mario Draghi, was preparing to announce a massive sovereign Quantitative Easing (QE) program, which would print over €1 trillion to buy European government bonds.
The SNB realized that maintaining the 1.20 floor against the ECB's incoming QE tidal wave would require purchasing hundreds of billions of additional depreciating Euros.
The SNB's foreign currency reserves had already swelled to 480 billion CHF (nearly 80% of Switzerland's entire annual GDP).
Fearing catastrophic future balance sheet losses, the SNB Governing Board decided to abandon the peg unilaterally before the ECB's formal QE announcement on January 22.

### 3. Retail Broker Asymmetry and Negative Balance Risk
Most retail FX brokers operated as Market Makers (B-Book) or Straight-Through Processors (A-Book / STP):
- In an STP model, the broker executes client orders directly against Tier-1 bank liquidity providers.
- When client stop-loss orders are triggered, the broker closes the client's trade and simultaneously liquidates its corresponding hedge with the liquidity provider.
- Brokers offered leverage up to 400:1 (requiring only 0.25% margin).
If an asset gaps down by 15% or 20% in seconds, the client's loss is not limited to their account balance; the loss extends to the full gap price:
$$\text{Realized Loss} = \text{Notional} \times \Delta P$$
Because retail clients cannot be forced to pay hundreds of thousands of dollars in deficit balances, the broker absorbs the unpaid bad debt as an immediate deduction against regulatory capital.

---

## Microstructure Breakdown and Liquidity Evaporation

```
+-----------------------------------------------------------------------+
|                    THE 2015 EUR/CHF LIQUIDITY EVAPORATION             |
+-----------------------------------------------------------------------+
| 1. SNB Press Release (09:30 AM CET)                                  |
|    SNB terminates 1.20 floor; cancels standing bids on EBS            |
|                                                                       |
| 2. Complete Order Book Vacuum                                         |
|    Tier-1 banks pull algorithmic quotes; bids drop from 1.20 to 1.00  |
|                                                                       |
| 3. Massive Gap Execution Slippage                                     |
|    Stop orders set at 1.1990 fail to execute until 1.0000 or 0.9500   |
|    (producing 2,000 pips of unintended adverse slippage)              |
|                                                                       |
| 4. Catastrophic Retail Deficits                                       |
|    A 200:1 leveraged position losing 20% creates an account deficit   |
|    equal to 40x the client's total deposited capital                  |
|                                                                       |
| 5. Broker Balance Sheet Obliteration                                  |
|    Brokers owe liquidity providers hundreds of millions for executed  |
|    hedges, while clients default on negative balances                 |
|                                                                       |
| 6. Immediate Insolvency and Bankruptcy                                |
|    Alpari UK files for administration; FXCM requires emergency loan   |
+-----------------------------------------------------------------------+
```

On Electronic Broking Services (EBS), the primary institutional interbank platform for EUR/CHF, order books became completely "one-sided".
Traders were attempting to sell Euros, but there were no buyers at any price.
Market spreads that typically measured 1 pip (0.0001) widened to over 1,000 pips (0.1000).
Trades executed at wildly disparate prices across different platforms depending entirely on when the first brave human trader entered a manual bid.

---

## Quantitative Autopsy

Consider a retail trader with an account equity $E_0 = \$10,000$ using 200:1 leverage to purchase EUR/CHF at $P_0 = 1.2005$:
$$\text{Position Notional} = \$10,000 \times 200 = \$2,000,000 \quad (€1,666,000)$$
$$\text{Required Initial Margin (0.50%)} = \$10,000$$
The trader sets a prudent stop-loss at $P_{\text{stop}} = 1.1985$ (20 pips risk):
$$\text{Expected Loss at Stop} = €1,666,000 \times (1.2005 - 1.1985) = €333 \approx \$400 \quad (4\% \text{ of account})$$
However, when the peg breaks, there are zero bids in the interbank market until $P_{\text{fill}} = 1.0200$.
The broker's automated liquidation engine finally executes the sell order at 1.0200:
$$\text{Realized Loss} = €1,666,000 \times (1.2005 - 1.0200) = €1,666,000 \times 0.1805 = €300,713 \approx \$361,000$$
The net account balance after liquidation is:
$$\text{Account Equity} = \$10,000 - \$361,000 = -\$351,000$$
The retail trader owes the broker $351,000.
When thousands of clients simultaneously incur six-figure negative balances, the broker faces aggregate claims from its liquidity providers (who executed the other side of the trade at 1.0200) totaling hundreds of millions of dollars.
Because client bad debt is uncollectible, broker equity is destroyed instantly.

---

## Regulatory and Structural Legacy

The 2015 Swiss Franc crisis forced global regulators to crack down on retail derivative leverage:
1. **ESMA Leverage Restrictions (2018)**: The European Securities and Markets Authority (ESMA) capped maximum retail FX leverage at 30:1 for major currency pairs and 20:1 for non-major pairs, eliminating 200:1 and 400:1 leverage across the European Union.
2. **Mandatory Negative Balance Protection**: Regulators in the UK (FCA), Europe (ESMA), and Australia (ASIC) made Negative Balance Protection legally mandatory for retail brokers; brokers can no longer pursue retail clients for losses exceeding their deposited capital.
3. **Re-evaluation of Sovereign Peg Risk**: Institutional risk managers reclassified sovereign currency pegs from "low-volatility anchors" to "extreme non-linear tail-risk binaries".
4. **Stricter Broker Capital Requirements**: Regulators substantially increased minimum regulatory net capital requirements for OTC retail derivatives dealers.

---

## Lessons for Traders and Risk Managers

- **Never Trust a Sovereign Peg**: A currency peg is not a market equilibrium; it is a political price-fixing mechanism that will be abandoned the instant its maintenance becomes economically unbearable for the central bank.
- **Stop Losses Do Not Protect Against Discontinuous Gaps**: A stop loss is simply a trigger to submit an order; if no liquidity exists at your stop price, your order will execute at the first available bid, regardless of how catastrophic the price may be.
- **Leverage Compounds Gap Risk Exponentially**: In continuous markets, leverage amplifies returns linearly; in gapping markets, high leverage guarantees immediate, unrecoverable account insolvency.

---

## Case Study Drills and Review Questions

> [!question] mkt-his-025 | What minimum exchange rate floor did the Swiss National Bank maintain from September 2011 to January 2015?
> A floor of 1.20 Swiss Francs per Euro (EUR/CHF).

> [!question] mkt-his-026 | Why did retail FX brokers like Alpari UK collapse following the SNB unpeg event?
> Extreme gap slippage caused client stop-loss orders to execute at massive losses, creating millions in uncollectible negative client balances that wiped out broker capital.

> [!question] mkt-his-027 | How much did the Swiss Franc appreciate intraday against the Euro on January 15, 2015?
> Over 30% within thirteen minutes, briefly spiking more than 40% to an extreme low of 0.85 EUR/CHF.

> [!question] mkt-his-028 | What major retail regulatory reform did ESMA implement in 2018 as a direct consequence of the 2015 Swiss Franc shock?
> Capping retail foreign exchange leverage at 30:1 and mandating negative balance protection for all retail client accounts.
