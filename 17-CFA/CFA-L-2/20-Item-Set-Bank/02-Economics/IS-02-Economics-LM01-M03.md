---
type: cfa-itemset
topic: "Economics"
topic_code: "02"
topic_slug: "02-Economics"
lm: 1
title: "Harrowgate Global Bond Fund Yen Hedge Book"
los: [los-02-01-c, los-02-01-d, los-02-01-e, los-02-01-g]
difficulty: 3
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/economics]
---

# Harrowgate Global Bond Fund Yen Hedge Book

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Harrowgate Capital manages the Harrowgate Global Bond Fund, a US-domiciled fund whose base currency is the US dollar (USD).
The fund's policy is to hedge all non-USD bond exposure back to USD with currency forward contracts.
Portfolio manager Rebecca Tolland has asked analyst Kenji Arima to review the fund's Japanese yen (JPY) hedge book before the quarterly risk meeting.
All forward quotes come from the fund's prime broker, and all interest rates are annualized market reference rates (MRRs) on an Actual/360 basis.

**Exhibit 1: JPY/USD Quotes from the Prime Broker**

| Quote | Bid | Offer |
|---|---|---|
| Spot | 147.82 | 147.86 |
| 3-month (90-day) forward points | -145.6 | -143.2 |
| 6-month (180-day) forward points | -276.4 | -273.6 |

**Exhibit 2: Market Reference Rates**

| Currency | 90-day | 180-day |
|---|---|---|
| USD | 4.40% | 4.30% |
| JPY | 0.45% | 0.50% |

**Exhibit 3: Consensus Expected Inflation, Next 12 Months**

| Country | Expected inflation |
|---|---|
| United States | 2.6% |
| Japan | 1.8% |

Arima has three tasks.
First, a holding of Japanese government bonds matures in 180 days, and the fund will then receive JPY 1,800,000,000 in principal and final coupon.
Tolland wants the USD value of that receipt locked in today with a 6-month forward contract from the prime broker.

Second, 90 days ago the fund sold JPY 4,000,000,000 six months forward against USD at an all-in rate of JPY/USD 149.35 to hedge a different bond position.
The yen has strengthened since the contract was written, and the risk report must show the contract's current mark-to-market value.

Third, Tolland is considering moving part of the fund's USD cash buffer into 180-day Japanese treasury bills that yield the 180-day JPY MRR.
The position would be fully hedged by selling the bills' maturity value forward for USD at the 180-day forward rate.
She asks Arima for the annualized USD return on the hedged position, computed from mid-market spot and forward rates.

Arima notes in his working papers that the forward points in Exhibit 1 are expressed in yen pips, so that one point equals JPY 0.01.

On 4 March, Tolland sets out her view for the currency committee.
She says: "Over a six-month horizon, I believe there are enough risk-neutral investors in the market that expected returns on USD and JPY money market deposits are equalized.
Purchasing power parity matters to me only at horizons of five years or more.
I also reject the idea that the best forecast of any exchange rate is simply today's spot rate."

Arima prepares three candidate forecasts of the JPY/USD spot rate 180 days ahead for the committee, one based on each of the approaches Tolland mentions, using the midpoint of the spot quote together with Exhibits 1, 2, and 3.
Tolland asks him to present only the forecast that is consistent with her 4 March statement.

## Questions

1. The USD amount that the fund can lock in today for the JPY 1,800,000,000 receipt is closest to: (LOS: los-02-01-c)
   - A. USD 12,175,931.
   - B. USD 12,403,186.
   - C. USD 12,409,001.
2. The mark-to-market value of the fund's JPY 4,000,000,000 forward contract is closest to: (LOS: los-02-01-d)
   - A. -USD 528,640.
   - B. -USD 540,455.
   - C. -USD 546,400.
3. The annualized USD return on Tolland's fully hedged Japanese treasury bill position is closest to: (LOS: los-02-01-e)
   - A. 0.50%.
   - B. 2.15%.
   - C. 4.30%.
4. The 180-day forecast of the JPY/USD spot rate that is most consistent with Tolland's 4 March statement is closest to: (LOS: los-02-01-g)
   - A. 145.09.
   - B. 147.25.
   - C. 147.84.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** USD is the base currency of the JPY/USD quote, and selling JPY forward means buying USD forward, so the fund pays the offer on both spot and points (V2 p.16).
> Yen points are divided by 100: all-in offer $= 147.86 + (-273.6/100) = 147.86 - 2.7360 = 145.1240$.
> USD locked in $= 1{,}800{,}000{,}000 / 145.1240 = \text{USD }12{,}403{,}186$ (Python: 12,403,186.24).
> A is wrong because it divides the points by 10,000, the convention for four-decimal quotes: $147.86 - 0.0274 = 147.8326$, giving $1{,}800{,}000{,}000/147.8326 = 12{,}175{,}931$.
> C is wrong because it uses the bid side, the rate at which the broker buys USD: $147.82 - 2.7640 = 145.0560$, giving $12{,}409{,}001$, a better rate than any dealer would give the fund.
> 2. **B.** Selling JPY forward made the fund long USD, the base currency, so it closes the position by selling USD three months forward (the remaining term) at the bid on spot and 3-month points: $147.82 + (-145.6/100) = 147.82 - 1.4560 = 146.3640$ (V2 p.18).
> The JPY legs cancel at settlement, so the net cash flow is in USD: receive $4{,}000{,}000{,}000/149.35 = \text{USD }26{,}782{,}725.14$ under the original contract and pay $4{,}000{,}000{,}000/146.3640 = \text{USD }27{,}329{,}124.65$ under the offset.
> Net settlement cash flow $= 26{,}782{,}725.14 - 27{,}329{,}124.65 = -\text{USD }546{,}399.51$, a loss because the USD the fund is long has depreciated (JPY/USD fell from 149.35 to 146.36).
> Discount 90 days at the USD MRR, the currency of the cash flow: $1 + 0.0440 \times 90/360 = 1.0110$, so $-546{,}399.51/1.0110 = -\text{USD }540{,}455$ (Python: -540,454.51).
> A is wrong because it offsets at the offer side, $147.86 - 1.4320 = 146.4280$, which is the rate for buying USD; the net flow is $-534{,}454.63$ and its present value is $-528{,}640$.
> C is wrong because it stops at the undiscounted settlement cash flow of $-546{,}400$.
> Using the 6-month points for a contract with 90 days left would give $145.0560$ and a present value of $-784{,}206$, which is not offered.
> 3. **C.** Mid spot $= (147.82 + 147.86)/2 = 147.84$; mid 6-month points $= (-276.4 - 273.6)/2 = -275.0$, so mid forward $= 147.84 - 2.7500 = 145.0900$.
> USD 1 buys JPY 147.84, which grows to $147.84 \times (1 + 0.0050 \times 180/360) = 147.84 \times 1.0025 = \text{JPY }148.2096$ and converts back at the forward to $148.2096/145.0900 = \text{USD }1.021501$.
> The 180-day return is $2.1501\%$, and annualized on Actual/360 it is $2.1501\% \times 360/180 = 4.3002\% \approx 4.30\%$, exactly the 180-day USD MRR, as covered interest rate parity requires (V2 p.14, p.27).
> A is wrong because it reports the JPY yield and ignores the gain from selling JPY forward at a premium (the higher-yielding USD trades at a forward discount).
> B is wrong because it reports the 180-day holding period return without annualizing it.
> 4. **A.** Tolland's belief in enough risk-neutral investors to equalize expected returns is uncovered interest rate parity, and with covered interest rate parity enforced by arbitrage, the two together give forward rate parity: the forward rate is the unbiased forecast of the future spot rate (V2 p.26, p.27).
> The forecast is therefore the 180-day mid forward, $147.84 - 2.7500 = 145.09$; the exact parity value is $147.84 \times 1.0025/1.0215 = 145.0902$ (Python), which confirms the quoted points.
> B is wrong because it is the ex ante PPP forecast, $147.84 \times (1 + (0.018 - 0.026) \times 180/360) = 147.84 \times 0.9960 = 147.2486$, which Tolland reserves for horizons of five years or more.
> C is wrong because it is today's mid spot rate, the random walk forecast that Tolland explicitly rejects.

## Distractor design

1. A: divides yen forward points by 10,000 instead of 100 (wrong scaling); C: uses the bid side for a purchase of the base currency (wrong side of the quote).
2. A: closes a long-base position at the offer instead of the bid (wrong side); C: omits discounting at the USD MRR (settlement value versus present value).
3. A: treats the hedge as locking in the foreign deposit rate, ignoring the forward premium (wrong parity logic); B: reports the holding period return instead of the annualized return (period error).
4. B: uses ex ante PPP, the long-horizon method the manager rejects for six months (wrong forecasting assumption); C: uses the random walk forecast (wrong forecasting assumption).
