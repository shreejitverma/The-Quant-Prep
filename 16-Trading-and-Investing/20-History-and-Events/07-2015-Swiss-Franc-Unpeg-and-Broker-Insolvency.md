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

On Thursday, January 15, 2015, at 10:30 CET (Central European Time), the Swiss National Bank (SNB) announced that it was discontinuing the minimum exchange rate of CHF 1.20 per euro that it had enforced since September 6, 2011, and cut its interest rate on sight deposits above the exemption threshold to -0.75%.
EUR/CHF immediately fell nearly 30 percent before partly recovering over the following days (Federal Reserve Bank of New York); a 30% fall in EUR/CHF is a 42.86% rise in the franc against the euro.
Liquidity in the franc collapsed, and stop-loss orders placed just below 1.20 were filled far below their trigger prices.
Leveraged retail clients lost more than their deposits: FXCM reported client debit balances of about $225 million and took a $300 million rescue loan from Leucadia National on January 16, and Alpari (UK) Limited entered special administration on January 19.
European and UK regulators later capped retail leverage on contracts for difference (CFDs), including FX, and required negative balance protection.

---

## Primary Sources and Chronology

Sources used on this page: SNB press releases of September 6, 2011, December 18, 2014 and January 15, 2015; Federal Reserve Bank of New York, *Foreign Exchange Operations* quarterly report for January to March 2015; Bank of England, *Gauging Market Dynamics Using Trade Repository Data* (Financial Stability Paper, 2017), for the time of the announcement; FXCM Inc. announcements and Form 8-K of January 2015; FCA statement "News for customers of Alpari (UK) Limited" (January 2015); ESMA product intervention decision on CFDs (March 27, 2018); FCA Policy Statement PS19/18 (2019); ECB press release of January 22, 2015.

- **September 6, 2011**: The SNB sets a minimum exchange rate of CHF 1.20 per euro, stating that it "will enforce this minimum rate with the utmost determination and is prepared to buy foreign currency in unlimited quantities".
- **December 18, 2014**: The SNB imposes an interest rate of -0.25% on sight deposit balances above an exemption threshold and reaffirms the minimum exchange rate as "the key instrument" of its policy.
- **Thursday, January 15, 2015, 10:30 a.m. CET**: The SNB announces that it is discontinuing the minimum exchange rate, lowering the sight deposit rate to -0.75%, and moving the three-month Libor target range to between -1.25% and -0.25%.
  - EUR/CHF immediately depreciates nearly 30 percent before partly recovering (New York Fed).
  - FXCM announces that client debit balances of about $225 million have left it short of regulatory capital.
- **Friday, January 16, 2015**: Leucadia National agrees a $300 million two-year term loan to FXCM.
- **Monday, January 19, 2015**: Alpari (UK) Limited enters special administration, with KPMG partners appointed as joint special administrators (FCA).
- **January 22, 2015**: The ECB announces an expanded asset purchase programme of €60 billion a month.

---

## Market Backdrop and Structural Vulnerabilities

### 1. The Peg Illusion
With the SNB committed to buying "foreign currency in unlimited quantities" at 1.20, many traders treated the floor as a hard limit on the downside of a long EUR/CHF position.
A common retail trade was to buy EUR/CHF just above 1.20 with a tight stop just below it, which looks like a small, well-defined risk.
That risk was only small while the floor held; once it was removed, the stop became a trigger to sell into a market with almost no bids.

### 2. The SNB's Reasons
The January 15, 2015 press release explains the decision directly: the minimum rate was introduced during a period of exceptional overvaluation, the overvaluation had decreased, and "divergences between the monetary policies of the major currency areas have increased significantly"; with the euro weakening against the dollar, the SNB concluded that "enforcing and maintaining the minimum exchange rate ... is no longer justified".
The rate cut to -0.75% was intended to keep the move from tightening monetary conditions too much.

### 3. Retail Broker Leverage and Negative Balances
Retail FX brokers offered leverage of up to several hundred to one, and some passed client orders to bank liquidity providers while others took the other side themselves.
If the price gaps through a client's stop, the loss is the full gap times the notional, which can far exceed the margin deposited:
$$\text{Realized Loss} = \text{Notional} \times \Delta P$$
When clients cannot or will not pay the deficit, the broker bears it, and a large enough total destroys the broker's capital.

---

## Microstructure Breakdown and Liquidity Evaporation

```
+-----------------------------------------------------------------------+
|                    THE 2015 EUR/CHF LIQUIDITY EVAPORATION             |
+-----------------------------------------------------------------------+
| 1. SNB Press Release (10:30 a.m. CET)                                 |
|    The 1.20 floor is discontinued with immediate effect               |
|                                                                       |
| 2. Order Book Vacuum                                                  |
|    Bids below 1.20 thin out as liquidity providers step back          |
|                                                                       |
| 3. Gap Execution                                                      |
|    Stops just below 1.20 fill far lower                               |
|                                                                       |
| 4. Retail Deficits                                                    |
|    A 200:1 position losing 20% loses 40x the deposit,                 |
|    leaving a deficit equal to 39x the client's deposited capital      |
|                                                                       |
| 5. Broker Losses                                                      |
|    Brokers must settle their hedges while clients owe deficits        |
|                                                                       |
| 6. Insolvency or Rescue                                               |
|    Alpari UK enters special administration; FXCM needs a loan         |
+-----------------------------------------------------------------------+
```

The Bank of England's 2017 study of trade repository data notes that trading in the Swiss franc options market practically stopped after the floor was removed, and the New York Fed reports the near-30 percent immediate move.

---

## Quantitative Autopsy

This is a hypothetical account.
A trader with a Swiss franc account of $E_0 = \text{CHF } 10{,}000$ uses 200:1 leverage to buy EUR/CHF at $P_0 = 1.2005$ (CHF per EUR):
$$\text{Position Notional} = \text{CHF } 10{,}000 \times 200 = \text{CHF } 2{,}000{,}000 = €1{,}665{,}972.51 \quad (2{,}000{,}000 / 1.2005)$$
$$\text{Required Margin } (1/200 = 0.50\%) = \text{CHF } 10{,}000$$
The stop is at $P_{\text{stop}} = 1.1985$, 20 pips below entry, and P&L accrues in Swiss francs:
$$\text{Loss at Stop} = €1{,}665{,}972.51 \times (1.2005 - 1.1985) = \text{CHF } 3{,}331.95 \quad (33.32\% \text{ of the account})$$
Even a 20-pip stop risks a third of the account at 200:1.
Suppose instead the stop is filled at $P_{\text{fill}} = 1.0200$:
$$\text{Realized Loss} = €1{,}665{,}972.51 \times (1.2005 - 1.0200) = €1{,}665{,}972.51 \times 0.1805 = \text{CHF } 300{,}708.04$$
$$\text{Account Equity} = \text{CHF } 10{,}000 - \text{CHF } 300{,}708.04 = -\text{CHF } 290{,}708.04$$
The trader owes the broker CHF 290,708.04, 29.07 times the deposit, after a price move of 15.04% ($0.1805 / 1.2005$).
In general, at leverage $L$ a gap of $x$ loses $Lx$ times the deposit, so at $L = 200$ a 20% gap loses 40 times the deposit and leaves a deficit of 39 times it.

---

## Regulatory and Structural Legacy

1. **ESMA product intervention (2018)**: ESMA's decision of March 27, 2018, applying to CFDs sold to retail clients from August 1, 2018, capped initial leverage at 30:1 for major currency pairs and 20:1 for non-major pairs, gold and major indices, and required negative balance protection and a margin close-out rule.
2. **UK permanent rules (2019)**: The FCA made equivalent rules permanent for CFDs sold to UK retail clients in Policy Statement PS19/18, effective August 1, 2019.
3. **Peg risk**: A currency floor or peg is a policy choice, and its removal is a jump risk that a volatility estimate from the pegged period cannot capture.

---

## Lessons for Traders and Risk Managers

- **Do Not Treat a Peg as a Price Floor**: A central bank can abandon a peg whenever maintaining it becomes too costly.
- **Stop Losses Do Not Protect Against Discontinuous Gaps**: A stop is a trigger to submit an order, and the order fills at the first available bid.
- **Leverage Multiplies Gap Risk**: At leverage $L$, a gap larger than $1/L$ leaves a negative balance.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-025 | What minimum exchange rate floor did the Swiss National Bank maintain from September 2011 to January 2015?
> A minimum of CHF 1.20 per euro, set on September 6, 2011 and discontinued on January 15, 2015.

> [!question]- mkt-his-026 | Why did retail FX brokers like Alpari UK collapse following the SNB unpeg event?
> Client stops gapped far below their trigger prices, leveraged clients ended with negative balances the brokers could not collect, and the losses exceeded broker capital; Alpari (UK) entered special administration on January 19, 2015, and FXCM needed a $300 million loan.

> [!question]- mkt-his-027 | How much did the Swiss Franc appreciate intraday against the Euro on January 15, 2015?
> EUR/CHF immediately fell nearly 30 percent (New York Fed), which is a rise of about 43 percent in the franc against the euro, since $1/(1 - 0.30) - 1 = 42.86\%$.

> [!question]- mkt-his-028 | What major retail regulatory reform did ESMA implement in 2018 as a direct consequence of the 2015 Swiss Franc shock?
> Leverage caps on retail CFDs of 30:1 for major currency pairs (20:1 for non-majors), with mandatory negative balance protection and margin close-out, applying from August 1, 2018.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_hist_07_snb_unpeg.py`](../code/mkt_hist_07_snb_unpeg.py) prints and asserts every number on this page: the account example is computed in exact rational arithmetic with the leverage identity $Lx$ evaluated at a 200:1 example, and the franc's appreciation is computed from the EUR/CHF fall.
- Related notes: [Case File 08: 2020 Negative WTI](08-2020-COVID-Crash-and-Negative-WTI-Crude.md), [Case File 06: 2010 Flash Crash](06-2010-Flash-Crash-and-LOB-Evaporation.md).
