---
type: guide
title: "Case File 08: 2020 COVID Crash and Negative WTI Crude"
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: solid
tags: [market-history, covid-crash-2020, negative-oil, wti-crude, cushing-storage, physical-delivery, uso-etf, case-study]
---

# Case File 08: 2020 COVID Crash and Negative WTI Crude

## Executive Summary

On Monday, April 20, 2020, the penultimate trading day of the May 2020 NYMEX WTI Light Sweet Crude Oil futures contract, the price traded below zero for the first time, reached an intraday low of -$40.32 per barrel at 2:29 p.m. ET, and settled at -$37.63, down $55.90 from the previous settlement of $18.27.
The CFTC staff's interim report (November 23, 2020) points to an oversupplied global market, an unprecedented fall in demand from the COVID-19 pandemic, and concern about storage at Cushing, Oklahoma, the delivery point of the physically settled contract, where working storage was near capacity by March 2020.
A holder of a long May contract at expiry must take delivery of crude at Cushing, so a long without storage had to sell before expiry at whatever price was bid.
Systems that assumed positive prices failed: the CFTC found that Interactive Brokers did not display negative prices to customers and that customers could not place orders in negative-priced contracts, and in September 2021 ordered it to pay $82.57 million in restitution and a $1.75 million penalty.

---

## Primary Sources and Chronology

Sources used on this page: CFTC staff, *Interim Staff Report: Trading in NYMEX WTI Crude Oil Futures Contract Leading up to, on, and around April 20, 2020* (November 23, 2020); CME Group notices of April 3, April 8 (Clearing Advisory 20-152) and April 13, 2020, as cited in that report; International Energy Agency, *Oil Market Report*, April 2020; CFTC Release 8432-21 (September 28, 2021) on Interactive Brokers; Interactive Brokers press release of April 21, 2020; S&P 500 closes of February 19 and March 23, 2020.

- **Early March 2020**: OPEC Plus members fail to agree on production cuts and dissolve their existing agreement, adding to downward pressure on prices (CFTC).
- **March 2020**: US equities fall sharply; market-wide circuit breakers halt trading on March 9, 12, 16 and 18, and the S&P 500 falls from its record close of 3,386.15 on February 19 to 2,237.40 on March 23, a decline of 33.92% in 23 trading days.
- **By March 2020**: Working storage available at Cushing is near capacity (CFTC).
- **April 3, 8 and 13, 2020**: CME flags WTI contracts for potential negative-price trading, announces that its clearing house will switch options valuation to the Bachelier model on one day's notice if negative prices occur (Clearing Advisory 20-152), and opens testing of negative and zero prices (CFTC).
- **April 13, 2020**: OPEC Plus announces a cut of 9.7 million barrels per day, the largest single production cut in history, to begin on May 1 (CFTC).
- **Friday, April 17, 2020**: The May contract settles at $18.27 per barrel.
- **Monday, April 20, 2020**:
  - The May contract opens the session at $17.73.
  - At about 2:08 p.m. ET it trades below $0 for the first time, and the fall is most pronounced in the 20 minutes from 2:08 to 2:28 p.m.
  - At 2:29 p.m. ET it reaches its all-time low of -$40.32.
  - It settles at -$37.63 at the end of the 2:28 to 2:30 p.m. settlement period.
- **Tuesday, April 21, 2020**: The May contract expires at a settlement price of $10.01.
- **September 28, 2021**: The CFTC orders Interactive Brokers to pay $82.57 million in restitution to customers and a $1.75 million civil penalty over its systems failures on April 20, 2020.

---

## Market Backdrop and Structural Vulnerabilities

### 1. Physical Delivery vs Cash Settlement
Unlike cash-settled financial futures such as the E-Mini S&P 500, NYMEX WTI crude oil futures (symbol CL) are physically settled:
- Each contract is for 1,000 barrels of light sweet crude oil.
- Delivery is at Cushing, Oklahoma.
- Trading in a contract month ends three business days before the 25th calendar day of the month before the contract month, or four business days before it if the 25th is not a business day (CME contract specifications, as of November 2026), so a long still open at that point must accept delivery.
  For the May 2020 contract, April 25, 2020 was a Saturday, so trading ended four business days earlier, on Tuesday, April 21.
Financial holders who do not want oil must close or roll their positions before expiry.

### 2. Storage Saturation at Cushing
According to EIA figures cited by the CFTC, Cushing has 75.8 million barrels of storage capacity, about 44% of the crude oil working storage capacity in the Midwest (PADD 2) and about 11% of all US commercial crude storage.
By March 2020 the available working storage was near capacity, and some reports indicated that most, if not all, of the empty space had already been committed (CFTC).
A long holder with no access to storage at Cushing cannot take delivery, which makes the last days of trading a forced sale for anyone without storage.

### 3. Demand Collapse
The IEA's April 2020 *Oil Market Report* estimated that April demand would be 29 million barrels per day lower than a year earlier.
The OPEC Plus cut announced on April 13 was not due to start until May 1, so in the near term production continued into a market whose demand had fallen sharply (CFTC).

---

## Microstructure Breakdown and Liquidity Evaporation

```
+-----------------------------------------------------------------------+
|                 NEGATIVE OIL LIQUIDATION FEEDBACK LOOP                |
+-----------------------------------------------------------------------+
| 1. Demand Collapses                                                   |
|    Lockdowns cut fuel use; inventories build                          |
|                                                                       |
| 2. Cushing Storage Near Capacity                                      |
|    Little uncommitted storage at the delivery point                   |
|                                                                       |
| 3. Expiry Approaches (Last Trade April 21)                            |
|    Longs without storage must sell before settlement                  |
|                                                                       |
| 4. Bids Thin Out                                                      |
|    Buyers with storage are few                                        |
|                                                                       |
| 5. Sellers Face a Binary Choice                                       |
|    Take delivery they cannot store, or sell at any price              |
|                                                                       |
| 6. Price Below Zero (settles at -$37.63/bbl)                          |
|    Sellers pay buyers to take the contract                            |
+-----------------------------------------------------------------------+
```

Valuation models built on lognormal prices cannot handle a negative underlying:
$$S(t) = S_0 e^{(\mu - \frac{1}{2}\sigma^2)t + \sigma W_t} > 0$$
The CFTC report notes that the Black-Merton-Scholes model relies on logarithms and cannot price an option on a negative underlying, which is why CME Clearing planned to switch to the Bachelier model, which does not.
Software built on the same assumption failed in the same way: the CFTC found that Interactive Brokers' platform did not display negative prices and did not accept orders at negative prices on April 20.

---

## Quantitative Autopsy

The theory of storage (Kaldor 1939; Working 1949) links the futures price $F(t, T)$ to the spot price $S(t)$ through the cost of carry:
$$F(t, T) = S(t) e^{(r + u - y)(T - t)}$$
where $r$ is the interest rate, $u$ the storage and insurance cost per unit time, and $y$ the convenience yield.
When storage is plentiful, $u$ is small and stable; as storage approaches capacity, the marginal cost of storing one more barrel rises steeply, and for a holder with no storage at all the effective cost of holding to delivery is unbounded.
A seller who must dispose of a barrel it cannot store will pay up to that disposal cost to be rid of it, so the price of the expiring contract can be negative:
$$S_{\text{expiring}} = -\text{(cost of disposal)} < 0$$
The next contract month, with time to arrange storage, stayed positive: only the May contract showed negative prices (CFTC).

The settlement arithmetic from the CFTC's figures: from the April 17 settlement of $18.27 to the April 20 settlement of -$37.63 is a fall of $55.90, or 305.97% of the starting price; from the April 20 opening price of $17.73 to the low of -$40.32 is a fall of $58.05, as the CFTC reports.

---

## Regulatory and Structural Legacy

1. **Negative-price readiness**: CME prepared its trading and clearing systems for negative prices in early April 2020 and planned a switch to Bachelier option pricing for affected energy options (CFTC, citing CME notices).
2. **Broker systems**: The CFTC's 2021 order against Interactive Brokers found failures to deploy system changes before negative prices occurred and a margin-calculation failure for WTI contracts.
3. **Interactive Brokers' losses**: On April 21, 2020, Interactive Brokers reported a provisional loss of approximately $88 million from meeting variation margin on behalf of customers whose accounts went into deficit.
4. **Commodity funds near expiry**: Funds that hold front-month futures must roll before expiry, and the May 2020 contract showed that the roll date itself carries risk when storage is scarce.

---

## Lessons for Traders and Risk Managers

- **Physical Contracts Carry Physical Obligations**: Do not hold a physically delivered future into its delivery window without the means to take delivery.
- **Prices Can Go Below Zero**: When holding an asset carries storage or disposal costs that exceed its value, the price can be negative.
- **Software Assumptions Are Risks**: Code that assumes positive prices is a single point of failure in an extreme market.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-029 | What was the official daily settlement price of the May 2020 WTI crude oil futures contract on April 20, 2020?
> -$37.63 per barrel, down $55.90 from the April 17 settlement of $18.27, a fall of 305.97%; the intraday low was -$40.32 (CFTC interim staff report).

> [!question]- mkt-his-030 | Why could financial traders not simply hold their expiring May 2020 WTI crude oil contracts to maturity?
> NYMEX WTI is physically settled at Cushing, Oklahoma, and working storage there was near capacity and largely committed, so a long without storage could not take delivery and had to sell before expiry.

> [!question]- mkt-his-031 | What pricing model did derivatives exchanges adopt following the negative oil event to handle zero and negative prices?
> The Bachelier (normal) model, which does not use logarithms and allows negative underlying prices; CME Clearing announced on April 8, 2020 (Clearing Advisory 20-152) that it would switch affected energy options to it if negative prices occurred.

> [!question]- mkt-his-032 | Why did Interactive Brokers absorb customer losses following the April 20, 2020 oil crash?
> Its systems did not display negative prices or accept orders at negative prices, and customers' accounts went into deficit; it reported a provisional loss of about $88 million on April 21, 2020, and the CFTC later ordered $82.57 million in restitution and a $1.75 million penalty.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_hist_08_negative_wti.py`](../code/mkt_hist_08_negative_wti.py) prints and asserts every number on this page: the WTI changes are recomputed from the CFTC's settlement, opening and low prices in exact decimal arithmetic and checked against the CFTC's stated $58.05 fall, the S&P 500 drawdown is recomputed from the cited closes, and the trading-day count is computed with the NumPy business-day calendar and checked by an explicit loop over calendar dates.
- Related notes: [Case File 07: 2015 SNB Unpeg](07-2015-Swiss-Franc-Unpeg-and-Broker-Insolvency.md).
