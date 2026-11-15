---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [SEBI circular SEBI/HO/MRD/TPD-1/P/CIR/2024/132 (1 Oct 2024), SEBI circular SEBI/HO/MRD/TPD-1/P/CIR/2025/76 (26 May 2025), NSE circular NSE/FAOP/70616 (3 Oct 2025) - lot sizes, SEBI Master Circular for Stock Exchanges and Clearing Corporations (30 Dec 2024), SEBI circular SEBI/HO/MRD2/DCAP/CIR/P/2020/127 - peak margin, Finance Bill 2026 - STT, FIA - 2025 exchange volume rankings]
---

# NSE and BSE Microstructure and Derivatives Architecture

## TL;DR

- The National Stock Exchange of India (NSE) was the world's largest derivatives exchange by contracts traded in 2025 (34.67 billion contracts, FIA full-year 2025 data), almost all of them NIFTY index options; BSE was second, driven by SENSEX options.
- NSE runs an electronic limit order book (NEAT, the National Exchange for Automated Trading), publishes tick-by-tick (TBT) feeds and offers member co-location at its data centre.
- Index derivatives are cash-settled and European; stock derivatives have been physically settled since the October 2019 expiry, and the settlement and closing-price rules were reworked in 2026 (a closing auction for F&O stocks from August 3, 2026, and new timings from December 7, 2026).
- SEBI's October 1, 2024 circular reshaped index options: one weekly-expiry benchmark per exchange, a minimum contract value of Rs 15 lakh, upfront premium collection and an extra 2% ELM on short options on expiry day; since September 2025 NSE expiries fall on Tuesday and BSE expiries on Thursday.
- Every trade pays statutory friction: Securities Transaction Tax (raised for F&O from April 1, 2026), exchange transaction charges, stamp duty, SEBI fees and 18% GST.

All rules, rates, lot sizes and timings below are stated as of November 2026 and cite the circular that set them; they change often, so re-check the latest NSE and SEBI circulars before relying on them.

## Learning objectives

- Analyze NSE's order-book architecture, co-location, and the pre-open and closing auction sessions.
- Calculate a closing VWAP and the cash settlement of an expiring index option.
- Deconstruct the four-quadrant Open Interest (OI) matrix and know which of its readings are conventions rather than facts.
- Model the complete transaction friction schedule across delivery equity, intraday equity, futures, and options.
- Formulate risk compliance under SEBI's SPAN, Extreme Loss Margin (ELM), and intraday peak margin snapshot rules.

## Core concepts

### 1. Exchange Infrastructure and Trading Sessions

NSE operates an electronic limit order book (LOB) with price-time priority.
Its equity session, as of November 2026, is (NSE circulars on the pre-open revision effective September 7, 2026 and the closing auction session, NSE/CMTR/75479):

```
+-----------------------------------------------------------------------+
|           NSE EQUITY SESSION, AS OF NOVEMBER 2026 (IST)               |
+-----------------------------------------------------------------------+
| 09:00 - 09:05 | Pre-open order entry (limit and market orders)        |
| 09:05 - 09:10 | Pre-open order entry, limit orders only; random close |
|               | between 09:08 and 09:10                               |
| 09:10 - 09:12 | Order matching at the equilibrium price               |
| 09:12 - 09:15 | Transition to the continuous market                  |
| 09:15 onward  | Continuous trading                                    |
| 15:15 - 15:35 | Closing auction session for stocks with derivatives  |
|               | (continuous trading in those stocks ends at 15:15)    |
| 15:30         | Continuous trading ends for other stocks              |
| 15:50 - 16:00 | Post-close session                                    |
+-----------------------------------------------------------------------+
```

1. **Pre-Open Call Auction (09:00 - 09:15 IST)**:
   - Orders are collected, the order-entry window closes at a random moment to deter last-second gaming, and a single equilibrium price that maximises traded quantity is computed.
   - All eligible crossing orders execute at that price before continuous trading opens at 09:15.
   - Since December 8, 2025 there is also a pre-open session for current-month stock and index futures (options are excluded).

2. **Continuous Trading and the Close**:
   - For stocks without derivatives, the closing price is still the VWAP of the last 30 minutes of trading (15:00 to 15:30).
   - For stocks with derivatives, SEBI's January 16, 2026 circular introduced a closing auction session, live on NSE from August 3, 2026: continuous trading ends at 15:15 and the closing price comes from a 15:15 to 15:35 auction; F&O contracts trade until 15:40.
   - SEBI's October 15, 2026 circular moves the timings from December 7, 2026: continuous trading to 15:30, the auction from 15:30 to 15:40, and stock and index derivatives trading to 15:45 (expiring index contracts stop at 15:30).

3. **Tick Sizes**:
   - Cash equities have price-linked ticks: Rs 0.01 below Rs 250 (from June 10, 2024), Rs 0.05 from Rs 250 to Rs 1,000, rising in steps to Rs 5.00 above Rs 20,000 (from April 15, 2025, NSE/CMTR/67133), reviewed monthly.
   - Index options trade in Rs 0.05 ticks, and index futures ticks depend on the index level (Rs 0.05 up to 15,000, Rs 0.10 up to 30,000 and Rs 0.20 above, NSE/FAOP/67135).

4. **Circuit Breakers and Price Bands** (SEBI Master Circular for Stock Exchanges and Clearing Corporations, December 30, 2024, Chapter 1):
   Market-wide circuit breakers trigger on a move in the NIFTY 50 or the SENSEX, whichever is breached first, and halt all equity and equity derivatives trading:
   - **10% move**: a 45-minute halt before 13:00; a 15-minute halt between 13:00 and 14:30; no halt at or after 14:30.
   - **15% move**: a 1 hour 45 minute halt before 13:00; a 45-minute halt between 13:00 and 14:00; trading stops for the day at or after 14:00.
   - **20% move**: trading stops for the rest of the day.
   - After a halt, trading resumes with a 15-minute pre-open call auction (SEBI circular CIR/MRD/DP/25/2013).
   Stocks without derivatives carry fixed daily price bands set by the exchange.
   Stocks with derivatives have no fixed band but a dynamic band of 10% of the previous close that is flexed in steps after cooling-off periods.

### 2. Contract Specifications and Settlement Mechanics

```
+-----------------------------------------------------------------------+
|        INDEX OPTIONS ON NSE, AS OF NOVEMBER 2026                      |
+-----------------------------------------------------------------------+
| Parameter           | NIFTY 50 Options           | NIFTY Bank Options |
|---------------------+----------------------------+--------------------|
| Lot Size            | 65 units                   | 30 units           |
| Tick Size           | Rs 0.05                    | Rs 0.05            |
| Expiries            | Weekly and monthly,        | Monthly only, last |
|                     | Tuesday                    | Tuesday            |
| Settlement Type     | Cash settled               | Cash settled       |
| Exercise Style      | European (Call: CE, Put: PE)| European          |
+-----------------------------------------------------------------------+
```

- Lot sizes were set by NSE circular NSE/FAOP/70616 (October 3, 2025), cutting NIFTY from 75 to 65 and NIFTY Bank from 35 to 30 from the January 2026 expiries; FINNIFTY is 60 and MIDCPNIFTY 120.
- SEBI's circular SEBI/HO/MRD/TPD-1/P/CIR/2024/132 (October 1, 2024) set a minimum contract value of Rs 15 lakh at introduction (Rs 15 to 20 lakh on review), allowed one benchmark index with weekly expiry per exchange (from November 20, 2024, so NIFTY Bank weekly options ended), added a 2% ELM on short options expiring that day (November 20, 2024), and required upfront collection of option premium and removed calendar-spread margin benefit on expiry day (both from February 1, 2025).
- SEBI's circular SEBI/HO/MRD/TPD-1/P/CIR/2025/76 (May 26, 2025) limits each exchange to Tuesday or Thursday expiries; NSE moved to Tuesday and BSE to Thursday for contracts expiring from September 1, 2025.

Index options are cash-settled against the final settlement price of the index.
From December 7, 2026 (SEBI circular of October 15, 2026), that price is an index value computed from each constituent's VWAP over the last 30 minutes of continuous trading.
For expiries from August 3 to December 6, 2026, the final settlement price follows the NSE closing auction session circular NSE/CMTR/75479.
A constituent's VWAP over the last 30 minutes is:

$$\text{VWAP} = \frac{\sum_{i=1}^M P_i \cdot V_i}{\sum_{i=1}^M V_i}$$

Stock options and stock futures are physically settled (SEBI circular SEBI/HO/MRD/DP/CIR/P/2018/67 of April 11, 2018 phased this in; all stock derivatives from the October 2019 expiry):
If an in-the-money (ITM) long call expires, the holder must take delivery of the shares by paying the full cash notional (Strike $\times$ Lot Size).
If an ITM long put expires, the holder must deliver the underlying shares.
Brokers typically raise margins on ITM stock positions in expiry week to cover the delivery obligation.

### 3. Open Interest (OI) Four-Quadrant Analysis

Every derivatives contract has a buyer and a seller, so a change in Open Interest reflects the net creation or closing of contracts.
Indian traders commonly read price and OI changes with the four-quadrant convention below; it is an interpretation, because OI alone does not show who initiated the trades:

```
+-----------------------------------------------------------------------+
|                    THE FOUR-QUADRANT OPEN INTEREST MATRIX             |
+-----------------------------------------------------------------------+
| Price Direction  | Open Interest Change | Conventional Reading        |
|------------------+----------------------+-----------------------------|
| Price RISING     | OI RISING            | LONG BUILDUP                |
|                  |                      | New longs opening           |
|------------------+----------------------+-----------------------------|
| Price RISING     | OI FALLING           | SHORT COVERING              |
|                  |                      | Shorts closing              |
|------------------+----------------------+-----------------------------|
| Price FALLING    | OI RISING            | SHORT BUILDUP               |
|                  |                      | New shorts opening          |
|------------------+----------------------+-----------------------------|
| Price FALLING    | OI FALLING           | LONG UNWINDING              |
|                  |                      | Longs closing               |
+-----------------------------------------------------------------------+
```

Additional widely used indicators:

1. **Put-Call Ratio (PCR)**:
   $$\text{PCR}_{\text{OI}} = \frac{\sum \text{Total Put Open Interest}}{\sum \text{Total Call Open Interest}}$$
   A common heuristic reads a very high PCR as heavy put writing (support) and a very low PCR as heavy call writing (resistance), and uses extremes as contrarian signals; the thresholds traders quote are conventions, not established results, so backtest them before use.

2. **Max Pain**:
   The Max Pain strike is the settlement level at which option writers would pay out the least to option buyers at expiry.
   For each candidate settlement level $K$, puts pay out when they finish below their strikes and calls pay out when they finish above theirs:
   $$\text{Payout}(K) = \sum_{i} \max(0, K_{P,i} - K) \cdot \text{OI}_{P,i} + \sum_{j} \max(0, K - K_{C,j}) \cdot \text{OI}_{C,j}$$
   The Max Pain strike is $\arg\min_K \text{Payout}(K)$ over the listed strikes.
   The claim that the index drifts toward Max Pain into expiry is folklore without a sound mechanism or evidence in this note's sources; treat it as a hypothesis.

### 4. Transaction Economics and Statutory Friction Schedule

```
+-------------------------------------------------------------------------------------+
|            INDIAN TRANSACTION FRICTION, NSE, AS OF NOVEMBER 2026                     |
+-------------------------------------------------------------------------------------+
| Tax / Fee            | Equity Delivery  | Equity Intraday | Futures     | Options        |
|----------------------+------------------+-----------------+-------------+----------------|
| STT                  | 0.1% (buy, sell) | 0.025% (sell)   | 0.05% (sell)| 0.15% of premium (sell)|
| NSE Transaction Fee  | 0.00307%         | 0.00307%        | 0.00183%    | 0.03553% of premium |
| Stamp Duty (buy side)| 0.015%           | 0.003%          | 0.002%      | 0.003% of premium |
| SEBI Fee             | Rs 10 per crore  | Rs 10 per crore | Rs 10/crore | Rs 10 per crore |
| GST                  | 18% on brokerage, exchange transaction charges and SEBI fees     |
+-------------------------------------------------------------------------------------+
```

- STT is levied by the Government through the Finance Acts, not by SEBI: futures STT rose to 0.02% and options STT to 0.1% from October 1, 2024, and again to 0.05% and 0.15% from April 1, 2026 (Finance Bill 2026, clause 143), with exercised options at 0.15% of intrinsic value.
- NSE transaction charges are Rs 307, Rs 183 and Rs 3,553 per crore (per side) for cash, futures and options premium (NSE/FA/64323 from October 1, 2024; the March 1, 2026 revision NSE/FA/73061 left these totals unchanged).
- Stamp duty is charged on the buyer only, at the rates in force since July 1, 2020.

### 5. SEBI Margin Architecture and Peak Margin Enforcement

1. **SPAN Margin**: Standard Portfolio Analysis of Risk, which values the portfolio under sixteen price and volatility scenarios and charges the worst loss (SEBI Master Circular, Chapter 5).
2. **Extreme Loss Margin (ELM)**: An add-on beyond SPAN, 2% of notional for index futures and for most index options (3% for index options more than 10% out of the money and 5% for residual maturity beyond nine months), plus the extra 2% on short options on expiry day.
3. **Peak Margin Snapshots**: Under SEBI circular SEBI/HO/MRD2/DCAP/CIR/P/2020/127 (July 20, 2020), clearing corporations take at least four random intraday snapshots of positions, and members must collect upfront margin against the peak; the requirement phased in from 25% in December 2020 to 100% from September 1, 2021.
   Shortfalls attract penalties levied on the clearing or trading member, which brokers often pass on to the client.

---

## Worked examples

### Example 1: A Closing VWAP and an Expiring Index Option
A stock trades in three clusters during the last 30 minutes (hypothetical data):
- Cluster 1: 10 lakh shares at Rs 2,451.00.
- Cluster 2: 15 lakh shares at Rs 2,449.50.
- Cluster 3: 25 lakh shares at Rs 2,452.00.

The 30-minute VWAP is:
$$\text{VWAP} = \frac{(2,451.00 \times 10) + (2,449.50 \times 15) + (2,452.00 \times 25)}{10 + 15 + 25} = \frac{24,510 + 36,742.5 + 61,300}{50} = \frac{122,552.5}{50} = \text{Rs } 2,451.05$$

From December 7, 2026, the index's final settlement value is built from every constituent's VWAP this way and then aggregated by the index methodology.
Suppose the NIFTY 50 final settlement value is 24,510.50.
A 24,500 CE then expires in the money and settles in cash at $24,510.50 - 24,500 = \text{Rs } 10.50$ per unit, or Rs 682.50 per lot of 65 units.
At an index level of 24,500, one lot is worth $65 \times 24,500 = \text{Rs } 15.93$ lakh, just above SEBI's Rs 15 lakh minimum; the lot would fall below it if the index were under about 23,077.

### Example 2: The Statutory Cost of Selling One NIFTY Option Lot
A trader sells one lot (65 units) of a NIFTY option at a premium of Rs 100, a premium turnover of Rs 6,500, with zero brokerage:
- STT at 0.15% of premium: Rs 9.75.
- NSE transaction charge at Rs 3,553 per crore: Rs 2.31.
- SEBI fee at Rs 10 per crore: Rs 0.0065.
- GST at 18% on the transaction charge and SEBI fee: Rs 0.42.
- Stamp duty: nil for the seller (it is charged on the buyer).
The total is Rs 12.48, about 0.19% of the premium collected, before brokerage, and STT is more than three quarters of it.

### Example 3: Max Pain on a Hypothetical Chain
With strikes 24,300 to 24,700 and call OI of 20, 35, 60, 90 and 70 lakh units and put OI of 80, 95, 70, 30 and 15 lakh units, the writers' payout is lowest at a settlement of 24,500.
There it is $100 \times 30 + 200 \times 15 + 100 \times 35 + 200 \times 20 = 13,500$ (index points times lakh units): the 24,600 and 24,700 puts and the 24,400 and 24,300 calls finish in the money.

---

## Pitfalls

- **Neglecting Physical Delivery on Expiring Stock Options**: In-the-money stock options and futures settle by delivery, so a position held into expiry without the cash or shares to settle it faces higher broker margins and forced closure.
- **Using Old Rates and Timings**: STT, lot sizes, expiry days and the closing session all changed between 2024 and 2026, and the closing session changes again on December 7, 2026; a backtest using old values misstates costs and settlement prices.
- **Underestimating Peak Margin Snapshots**: Expanding intraday leverage between planned checks can breach a random snapshot, and the shortfall penalty is levied even if the position is closed by the end of the day.
- **Reading Open Interest as Intent**: The four-quadrant labels are conventions; OI does not reveal who initiated the trades, so treat them as hypotheses.
- **Assuming Fixed Circuit Breakers on F&O Stocks**: Stocks with derivatives have dynamic, flexing price bands rather than fixed daily limits, although market-wide circuit breakers still halt them.

---

## Interview questions

> [!question]- mkt-ind-001 | What does NEAT stand for in the context of the National Stock Exchange of India?
> National Exchange for Automated Trading, the electronic limit order matching system of the NSE.

> [!question]- mkt-ind-002 | What are the trading hours for the regular continuous session on NSE and BSE?
> Continuous trading starts at 09:15 IST; as of November 2026 it ends at 15:30 for stocks without derivatives and at 15:15 for stocks with derivatives, which then go through a 15:15 to 15:35 closing auction (SEBI moves this to 15:30 and 15:30 to 15:40 from December 7, 2026).

> [!question]- mkt-ind-003 | What is the purpose of the 09:00 to 09:15 IST pre-open session on Indian exchanges?
> To discover a single equilibrium opening price that maximises traded quantity after overnight news; the order-entry window closes at a random time (between 09:08 and 09:10 since September 7, 2026) to deter gaming.

> [!question]- mkt-ind-004 | What is the minimum tick size for cash equities and index derivatives on the NSE?
> Index options trade in Rs 0.05 ticks, but cash equities have price-linked ticks as of November 2026: Rs 0.01 below Rs 250, Rs 0.05 from Rs 250 to Rs 1,000, and larger ticks above that (NSE/CMTR/67133, from April 15, 2025).

> [!question]- mkt-ind-005 | How is the official daily closing price of an NSE equity or index computed?
> For stocks without derivatives, as the VWAP of trades in the last 30 minutes (15:00 to 15:30); for stocks with derivatives, since August 3, 2026, from the closing auction session.
> An index close is computed from its constituents' closing prices, and from December 7, 2026 index derivatives settle on an index value built from constituents' 30-minute VWAPs.

> [!question]- mkt-ind-006 | What are the three market-wide index circuit breaker percentage thresholds in India?
> 10%, 15%, and 20% movements in the benchmark NIFTY 50 or S&P BSE SENSEX.

> [!question]- mkt-ind-007 | What occurs if the market breaches the 20% circuit breaker threshold at any time?
> Trading in all cash equity and equity derivatives markets is halted for the remainder of the trading day.

> [!question]- mkt-ind-008 | Do individual stocks with active futures and options (F&O) contracts have fixed daily price circuit limits?
> No fixed band: they have a dynamic price band of 10% of the previous close, which the exchange flexes in steps after cooling-off periods when it is hit; market-wide circuit breakers still apply.

> [!question]- mkt-ind-009 | What is the standard settlement cycle for Indian cash equities?
> T+1 rolling settlement (fully implemented from January 27, 2023), with optional T+0 settlement, introduced as a beta for 25 stocks on March 28, 2024 and since widened toward the top 500 stocks.

> [!question]- mkt-ind-010 | What is the exercise style of all index and stock options traded on the NSE?
> European style (can only be exercised at contract expiration).

> [!question]- mkt-ind-011 | What are the symbols used on Indian exchanges to denote European Call and Put options?
> CE denotes Call European and PE denotes Put European.

> [!question]- mkt-ind-012 | What is the settlement mechanism for Indian index options versus single-stock options?
> Index options are cash settled; stock options and futures have been physically settled since the October 2019 expiry (phased in from July 2018 under SEBI's April 11, 2018 circular).

> [!question]- mkt-ind-013 | What is a 'lot size' in Indian derivatives trading?
> The minimum standardized number of underlying shares or index units that can be traded in a single contract.

> [!question]- mkt-ind-014 | In Open Interest (OI) analysis, what does a rising price accompanied by rising OI indicate?
> By the usual convention, Long Buildup: new long positions are being opened; OI alone cannot confirm who initiated the trades.

> [!question]- mkt-ind-015 | What does a rising price accompanied by falling Open Interest indicate?
> Short Covering: existing short sellers are buying back contracts to close out losing positions.

> [!question]- mkt-ind-016 | What does a falling price accompanied by rising Open Interest indicate?
> Short Buildup: aggressive short sellers are establishing fresh bearish positions.

> [!question]- mkt-ind-017 | What does a falling price accompanied by falling Open Interest indicate?
> Long Unwinding: existing long investors are liquidating or stopping out of long positions.

> [!question]- mkt-ind-018 | What is the Put-Call Ratio (PCR) formula based on Open Interest?
> Total Put Open Interest divided by Total Call Open Interest.

> [!question]- mkt-ind-019 | Why is an extremely high PCR (e.g., > 1.40) interpreted as a bullish contrarian signal?
> The heuristic reads a high PCR as heavy put writing by sellers who expect support, and extremes as crowded positioning likely to reverse; the threshold is a convention and the signal should be backtested, not assumed.

> [!question]- mkt-ind-020 | What is the 'Max Pain' strike in option analytics?
> The strike price at which option buyers collectively lose the maximum amount and option writers incur the minimum payout.

> [!question]- mkt-ind-021 | What is 'rollover' in the Indian derivatives market?
> Carrying forward an open futures or options position from the expiring near-month contract to the next-month contract.

> [!question]- mkt-ind-022 | What is Securities Transaction Tax (STT)?
> A tax levied by the Government of India (Finance (No. 2) Act, 2004) on the value of securities transactions on recognised stock exchanges; as of April 1, 2026 it is 0.05% on futures sales and 0.15% of premium on option sales.

> [!question]- mkt-ind-023 | What rate of Goods and Services Tax (GST) applies to brokerage and exchange transaction fees in India?
> 18% GST.

> [!question]- mkt-ind-024 | What is SPAN margin in the SEBI margin framework?
> Standard Portfolio Analysis of Risk, which values the portfolio under sixteen price and volatility scenarios and charges the worst loss; NSE Clearing still uses it as of November 2026.

> [!question]- mkt-ind-025 | What is Extreme Loss Margin (ELM)?
> An add-on margin beyond SPAN for tail losses: 2% of notional for index futures and most index options as of November 2026, plus an extra 2% on short options on their expiry day.

> [!question]- mkt-ind-026 | What are SEBI's 'Peak Margin' snapshot rules?
> Clearing corporations take at least four random intraday snapshots of positions, and members must hold upfront margin against the peak (100% since September 1, 2021, under SEBI's July 20, 2020 circular); shortfalls are penalised.

> [!question]- mkt-ind-027 | What are Graded Surveillance Measures (GSM) and Additional Surveillance Measures (ASM)?
> Regulatory monitoring frameworks that impose trading curbs, 100% margins, and price bands on highly volatile or manipulated small-cap stocks.

> [!question]- mkt-ind-028 | Where is the primary co-location facility for the National Stock Exchange located?
> In Mumbai, at NSE's data centre; the building is commonly reported as NSE's Exchange Plaza at Bandra Kurla Complex, which this note could not confirm from a primary source.

> [!question]- mkt-ind-029 | What is the tick-by-tick (TBT) market data feed on NSE?
> A multicast broadcast feed transmitting every individual order placement, cancellation, modification, and trade execution.

> [!question]- mkt-ind-030 | What risk does physical settlement pose to an option seller holding an expiring deep in-the-money put?
> The obligation to buy the full notional value of physical shares, requiring 100% cash funding or triggering broker auction liquidation.

> [!question]- mkt-ind-031 | What is the Bank Nifty index composition?
> A free-float market-capitalisation-weighted index of 14 banking stocks as of November 2026 (12 until Union Bank and Yes Bank joined on December 31, 2025, after SEBI's May 29, 2025 circular required at least 14 constituents for indices with derivatives).

> [!question]- mkt-ind-032 | What is the primary golden rule of quantitative execution on Indian exchanges?
> Model the full statutory friction schedule (STT, GST, stamp duty) and peak margin limits before evaluating gross backtest alpha.

## In this repo and The-Distinguished-Engineer

- Code: [mkt_india_01_nse.py](../code/mkt_india_01_nse.py) prints and asserts every computed number in this note; the VWAP is rebuilt from individual prints, the option-selling cost charge by charge, and max pain by brute force over every strike, while rates, lots and timings are cited constants; run it with `uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_india_01_nse.py`.
- Related: [Regulation, Tax, and Trading Operations](../08-Execution-Microstructure/02-Regulation-Tax-and-Trading-Operations.md) for Indian F&O taxation and the audit turnover rule.

---

## Further reading

- Futures Industry Association. (2026). Full-year 2025 exchange-traded derivatives volume rankings (FIA, February 2026).
- Government of India. (2026). *Finance Bill 2026, Memorandum Explaining the Provisions* (STT, clause 143).
- National Stock Exchange of India. (2025). Circular NSE/FAOP/70616, October 3, 2025 (revised lot sizes of index derivatives).
- Securities and Exchange Board of India. (2020). Circular SEBI/HO/MRD2/DCAP/CIR/P/2020/127, July 20, 2020 (collection and reporting of margins, including peak margin snapshots).
- Securities and Exchange Board of India. (2024). *Measures to Strengthen Equity Index Derivatives Framework for Increased Investor Protection and Market Stability*. Circular SEBI/HO/MRD/TPD-1/P/CIR/2024/132, October 1, 2024.
- Securities and Exchange Board of India. (2024). *Master Circular for Stock Exchanges and Clearing Corporations*. December 30, 2024.
- Securities and Exchange Board of India. (2025). Circular SEBI/HO/MRD/TPD-1/P/CIR/2025/76, May 26, 2025 (expiry days for equity derivatives).
