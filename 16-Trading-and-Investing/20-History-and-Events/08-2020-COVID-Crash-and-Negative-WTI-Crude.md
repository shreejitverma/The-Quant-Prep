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

On Monday, April 20, 2020, the May 2020 West Texas Intermediate (WTI) Light Sweet Crude Oil futures contract (CLK20) traded on the New York Mercantile Exchange (NYMEX) collapsed into negative territory for the first time in history, plunging to an intraday low of -$40.32 per barrel and settling at -$37.63 per barrel.
The event was driven by a collision between unprecedented physical market reality and financial derivatives mechanics.
The onset of the global COVID-19 pandemic and government-mandated travel lockdowns eradicated approximately 30 million barrels per day (30%) of global oil demand.
Concurrently, an ill-timed price war between Saudi Arabia and Russia flooded the world with excess physical crude, rapidly filling commercial storage facilities.
Because the NYMEX WTI contract requires physical delivery of 1,000 barrels of crude oil at Cushing, Oklahoma, financial traders holding expiring contracts faced a binary choice on the penultimate day of trading: sell the contract at any price or take physical delivery of railcars and pipelines of crude oil.
With commercial storage at Cushing 100% booked by midstream pipeline operators, financial market participants were physically unable to store the oil.
Selling turned into a panic rout into an empty bid book, forcing sellers to pay buyers $37.63 per barrel to take the oil off their hands.
The event broke automated trading systems and brokerage software worldwide (including Interactive Brokers, which absorbed a $104 million customer deficit loss because its systems could not display or execute negative asset prices).

---

## Primary Sources and Chronology

- **January - February 2020**: COVID-19 virus spreads globally; Chinese manufacturing halts and international commercial aviation contracts sharply.
- **March 6, 2020**: OPEC+ negotiations in Vienna collapse when Russia refuses to agree to Saudi Arabia's proposed production cuts; Saudi Arabia responds by slashing official selling prices and announcing maximum production capacity increases.
- **Monday, March 9, 2020 (Black Monday 2020)**: WTI crude prices plunge 24.6% in a single session; US equity markets trigger Level 1 circuit breakers minutes after the opening bell.
- **March 11 - 18, 2020**: Global financial panic triggers four separate NYSE market-wide circuit breaker halts in eight trading sessions; S&P 500 bottoms on March 23, down 35.4% in 22 trading days.
- **Mid-April 2020**:
  - Global oil demand drops by 30 million barrels per day as billions of people are placed under lockdown.
  - The United States Oil Fund (USO), a $4 billion retail ETF, accumulates up to 25% of the entire outstanding open interest in front-month WTI contracts.
  - Cushing, Oklahoma (the designated physical delivery hub for NYMEX WTI) reaches maximum operational working storage capacity.
- **Thursday, April 16, 2020**: CME Group issues an urgent advisory notice (Notice 20-160) alerting market participants that its trading and clearing systems have been updated to support negative prices and negative strike options.
- **Monday, April 20, 2020 (Penultimate Day of Trading for May 2020 Contract)**:
  - 09:00 AM EST: May contract trades at $10.01 per barrel.
  - 01:00 PM EST: The contract breaches $5.00, and commercial storage operators confirm that zero spot storage is available in Cushing at any price.
  - 02:00 PM EST: May WTI contract trades at $0.00; algorithmic stop-loss and margin liquidation orders trigger simultaneously across retail and institutional brokerages.
  - 02:08 PM EST: Price drops below zero for the first time in petroleum history, hitting -$1.00.
  - 02:29 PM EST: Contract trades at its all-time intraday low of -$40.32 per barrel.
  - 02:30 PM EST: NYMEX settlement window closes; the official daily settlement price is established at -$37.63 per barrel (down $55.90, or -306% on the day).
- **Tuesday, April 21, 2020 (Expiration Day)**: May 2020 contract expires quietly at +$10.01 per barrel as remaining positions settle; June 2020 contract trades at $11.57.
- **November 2020**: The US Commodity Futures Trading Commission (CFTC) releases its *Interim Staff Report on Trading in the May 2020 WTI Crude Oil Futures Contract*.

---

## Market Backdrop and Structural Vulnerabilities

### 1. Physical Delivery vs Cash Settlement
Unlike financial futures (such as S&P 500 E-mini or Eurodollar futures) which settle in cash, NYMEX WTI Crude Oil (symbol CL) is a **physical delivery contract**:
- Each contract represents 1,000 barrels (42,000 gallons) of light sweet crude oil.
- Delivery must take place Free-on-Board (FOB) at any pipeline or storage facility in Cushing, Oklahoma with pipeline access to Enterprise, Enbridge, or Plains All American terminals.
- If a market participant holds an open long contract past the close of trading on the third business day prior to the 25th calendar day of the month, they are legally obligated to receive 1,000 physical barrels of crude.
Financial traders (hedge funds, retail commodity investors, index funds) have no intention of ever taking physical delivery.
They must roll their positions forward to the next contract month prior to expiration.

### 2. Physical Storage Saturation at Cushing
Cushing, Oklahoma is the pipeline crossroads of North America, possessing approximately 76 million barrels of working storage capacity.
By mid-April 2020, Cushing tanks held over 60 million barrels of physical oil, with the remaining 16 million barrels 100% leased under long-term commercial contracts to oil refiners and physical traders.
If a financial trader without a pre-existing leased storage contract was assigned physical oil on expiration, pipeline operators would physically refuse the barrels, and the buyer would face catastrophic demurrage and environmental regulatory penalties exceeding hundreds of thousands of dollars per day.

### 3. The USO Retail ETF Inflow Distortion
Retail investors seeking to "buy the dip" in cheap oil poured billions of dollars into the United States Oil Fund (USO).
USO's prospectus mandated investing exclusively in the front-month NYMEX contract and rolling to the next month two weeks prior to expiration.
By mid-April, USO held over 150,000 contracts of front-month WTI, representing a dangerous concentration of financial capital in a physical market facing immediate physical storage gridlock.

---

## Microstructure Breakdown and Liquidity Evaporation

```
+-----------------------------------------------------------------------+
|                 NEGATIVE OIL LIQUIDATION FEEDBACK LOOP                |
+-----------------------------------------------------------------------+
| 1. COVID Lockdowns Collapse Demand (-30M bpd)                         |
|    Refineries slash crude runs; storage tanks fill globally           |
|                                                                       |
| 2. Cushing Commercial Storage 100% Exhausted                          |
|    Storage owners refuse to rent capacity at any cost                 |
|                                                                       |
| 3. Mandatory Physical Delivery Approaching (April 21 Expiry)          |
|    Financial longs must liquidate May contract before 02:30 PM        |
|                                                                       |
| 4. Bids Evaporate from Commercial Refiners                            |
|    Refiners cannot take more oil; bid side of the order book vanishes |
|                                                                       |
| 5. Financial Sellers Face Binary Choice:                              |
|    Accept physical delivery (ruin) OR sell at ANY price               |
|                                                                       |
| 6. Price Drops Below Zero (-$37.63/bbl)                               |
|    Financial longs pay physical operators $37.63/bbl to take barrels  |
+-----------------------------------------------------------------------+
```

As the price dropped through $0.00, broker risk engines experienced software errors.
Many algorithmic models were coded with log-normal asset price assumptions:
$$S(t) = S_0 e^{(\mu - \frac{1}{2}\sigma^2)t + \sigma W_t} > 0$$
Because the natural logarithm $\ln(S)$ is undefined for $S \le 0$, valuation engines crashed, automated margin liquidation bots failed to execute, and trading screens displayed blank lines.

---

## Quantitative Autopsy

Under the classic Theory of Storage (Kaldor 1939, Working 1949), the futures price $F(t, T)$ is linked to spot price $S(t)$ by:
$$F(t, T) = S(t) e^{(r + u - y)(T - t)}$$
where $r$ is the interest rate, $u$ is the marginal physical storage and insurance cost per unit time, and $y$ is the convenience yield.
When storage tanks are plentiful, storage cost $u$ is a modest, bounded percentage (e.g. $0.30 per barrel per month, or ~5% annualized).
However, when available physical storage approaches 100% capacity:
$$u \to \infty$$
The convenience yield $y$ (the economic benefit of holding physical inventory) collapses to zero:
$$y = 0$$
If storage capacity is exhausted and a producer has no operational ability to shut down a flowing oil well without permanently damaging the geological reservoir formation, the marginal physical disposal cost is positive and extreme:
$$S_{\text{physical}} = -\text{Disposal Cost} < 0$$
The negative price of -$37.63 represented the economic cost of leasing temporary physical storage on floating supertankers (VLCCs) or railcars, plus the severe penalty charged by physical traders to absorb the delivery obligation.

---

## Regulatory and Structural Legacy

The negative oil event forced lasting structural modifications in commodity derivatives:
1. **Model Upgrades to Bachelier Arithmetic Pricing**: Futures exchanges and risk clearinghouses migrated options and futures models from Black-Scholes log-normal pricing to the Bachelier (1900) normal model, which natively supports zero and negative underlying asset prices.
2. **Retail Commodity ETF Structural Revisions**: USO and other commodity funds restructured their prospectuses, abandoning 100% front-month concentration in favor of spreading assets across 12 forward contract months.
3. **CME Dynamic Price Limits and Circuit Breakers**: CME implemented stricter intraday circuit breaker collars on expiring physical commodity contracts to prevent discontinuous price collapses.
4. **Broker Software Remediation**: Interactive Brokers paid over $104 million to compensate customers whose accounts suffered catastrophic losses due to platform software bugs that prevented customers from closing positions when prices went negative.

---

## Lessons for Traders and Risk Managers

- **Physical Contracts Carry Physical Obligations**: A trader must never trade a physically deliverable futures contract into its expiration cycle without the operational infrastructure and commercial licenses required to receive physical delivery.
- **Asset Prices Can Go Below Zero**: Whenever an asset has physical holding, environmental disposal, or storage costs that exceed its economic value, prices can trade into deep negative territory.
- **Software Architecture Is a Source of Risk**: Mathematical assumptions hardcoded into software (such as assuming prices are strictly positive) become fatal points of failure during extreme regime shifts.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-029 | What was the official daily settlement price of the May 2020 WTI crude oil futures contract on April 20, 2020?
> -$37.63 per barrel (an unprecedented single-day decline of $55.90, or -306%).

> [!question]- mkt-his-030 | Why could financial traders not simply hold their expiring May 2020 WTI crude oil contracts to maturity?
> Because NYMEX WTI is a physically deliverable contract requiring FOB delivery at Cushing, Oklahoma, and all commercial storage capacity was 100% booked.

> [!question]- mkt-his-031 | What pricing model did derivatives exchanges adopt following the negative oil event to handle zero and negative prices?
> The Bachelier normal model, which allows asset prices and strike prices to assume negative values.

> [!question]- mkt-his-032 | Why did Interactive Brokers absorb a $104 million customer loss following the April 20, 2020 oil crash?
> Its trading software was hardcoded to assume asset prices could not go below zero, preventing customers from viewing negative quotes or closing positions.
