---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 1
title: "Keller Brandt Family Office: Equity Forward and Equity Swap Overlay"
los: [los-07-01-a, los-07-01-b, los-07-01-g]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Keller Brandt Family Office: Equity Forward and Equity Swap Overlay

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Lucia Ferraro, CFA, is an investment analyst at Keller Brandt Family Office, which manages the concentrated equity holdings of a founding family.
The family holds a large block of Tarrant Mining Ltd. shares that it cannot sell before a lock-up expires in nine months.
Anton Keller, the chief investment officer, asks Ferraro to evaluate a forward sale of part of the block and to review an existing equity swap.
Ferraro assumes no transaction costs, unrestricted short selling, and borrowing and lending at the risk-free rate.

Exhibit 1: Tarrant Mining forward inputs (today)

| Item | Value |
|---|---|
| Share price | 64.20 |
| Declared dividend, paid in 4 months | 1.10 per share |
| Forward expiration | 9 months |
| Risk-free rate, annual compounding | 3.20% |
| Risk-free rate, continuous compounding | 3.15% |
| Dealer A bid for a 9-month forward | 65.40 |
| Sell-side consensus 9-month target price | 71.00 |

Ferraro notes that Dealer A's bid is well above the price she derives from the carry model.
Rather than accept that bid, the family office sells 50,000 shares forward to Dealer B at the no-arbitrage price, with delivery in nine months.

Five months later, the dividend has been paid as scheduled, Tarrant shares trade at 66.80, and the annually compounded risk-free rate is still 3.20%.
Keller asks Ferraro for the per-share value of the forward sale for the quarterly family report.

At an investment committee meeting, Keller makes two statements.

Statement 1: "If Tarrant had declared the same dividend payable in month 8 instead of month 4, the no-arbitrage nine-month forward price would have been lower, because the dividend would arrive closer to expiration."

Statement 2: "Futures on the Veridian 400 index, whose continuous dividend yield is 4.10% while the six-month continuously compounded rate is 3.10%, should trade below the index level and converge to it from below."

The family office also holds a three-year equity swap on the Veridian 400 index, in which it receives the index price return and pays a fixed rate.
The swap was used to add index exposure without buying the constituent shares.

Exhibit 2: Veridian 400 equity swap terms

| Term | Value |
|---|---|
| Position of the family office | Receive equity return, pay fixed |
| Notional amount ($NA_E$), equal to par | 8,000,000 |
| Fixed rate (annualized) | 2.60% |
| Reset and settlement frequency | Semiannual |
| Index level at initiation (14 months ago) | 1,760.00 |
| Index level at the most recent reset (2 months ago) | 1,812.40 |
| Index level today | 1,851.10 |

Exhibit 3: Current present value factors for the remaining swap settlement dates

| Months from today | Spot rate (add-on) | PV factor |
|---|---|---|
| 4 | 3.30% | 0.989120 |
| 10 | 3.45% | 0.972053 |
| 16 | 3.55% | 0.954806 |
| 22 | 3.65% | 0.937280 |
| Sum | | 3.853259 |

Keller is concerned about liquidity at the next reset.
He asks Ferraro what the family office would owe or receive on the next settlement date if the Veridian 400 price return over the current six-month period turned out to be -3.5%.
He also asks for the swap's current value to the family office.

## Questions

1. Based on Exhibit 1, the no-arbitrage price of the nine-month Tarrant forward is closest to: (LOS: los-07-01-a)
   - A. 65.73.
   - B. 64.62.
   - C. 66.85.
2. Given Dealer A's bid, the arbitrage strategy and the present value of the riskless profit per share are best described as: (LOS: los-07-01-b)
   - A. buy the forward, short the shares, and lend the proceeds, earning 0.76.
   - B. sell the forward, borrow, and buy the shares, earning 0.78.
   - C. sell the forward, borrow, and buy the shares, earning 0.76.
3. Five months after initiation, the value per share of the family office's forward sale to Dealer B is closest to: (LOS: los-07-01-a)
   - A. -2.88.
   - B. -1.77.
   - C. -2.85.
4. Which of Keller's statements is correct? (LOS: los-07-01-b)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.
5. If the Veridian 400 price return over the current period is -3.5%, the family office's net settlement on the next reset date is closest to: (LOS: los-07-01-g)
   - A. a payment of 384,000.
   - B. a payment of 488,000.
   - C. a payment of 176,000.
6. The current value of the equity swap to the family office is closest to: (LOS: los-07-01-g)
   - A. -271,844.
   - B. 271,844.
   - C. 515,112.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The dividend is a carry benefit, compounded only from its payment date to expiration.
> $\text{FV}(S_0) = 64.20(1.032)^{9/12} = 65.7347$ and $\text{FV}(D) = 1.10(1.032)^{5/12} = 1.1145$.
> $F_0 = 65.7347 - 1.1145 = 64.6202$.
> A is wrong because it ignores the dividend and prices the forward as $\text{FV}(S_0)$ alone (65.7347).
> C is wrong because it adds the dividend's future value as if it were a carry cost, $65.7347 + 1.1145 = 66.8492$.
> The consensus target of 71.00 is irrelevant because expectations of the future share price never enter the carry model.
> 2. **C.** Dealer A's bid of 65.40 exceeds the no-arbitrage price of 64.6202, so the forward is rich and the trade is carry arbitrage: sell the forward to Dealer A, borrow 64.20, buy the shares, and invest the dividend when received.
> At expiration, delivering the share for 65.40 and repaying the loan net of the dividend's future value leaves $65.40 - 64.6202 = 0.7798$ per share with no risk.
> Its value today is $0.7798/(1.032)^{9/12} = 0.7616$.
> A is wrong because reverse carry arbitrage is the trade when the forward is cheap; buying a forward at 65.40 that is worth 64.6202 locks in a loss.
> B is wrong because 0.78 is the profit at expiration, not its present value.
> 3. **C.** The dividend has already been paid, so no carry benefit remains between now and expiration.
> The price of a new forward with four months left is $F_t = 66.80(1.032)^{4/12} = 67.5051$.
> The short position's value is $\text{PV}[F_0 - F_t] = (64.6202 - 67.5051)/(1.032)^{4/12} = -2.8849/1.010555 = -2.8547$ with unrounded inputs (the rounded figures shown give -2.8548; both round to -2.85).
> A is wrong because it stops at the undiscounted difference $F_0 - F_t = -2.8849$, which is received only at expiration.
> B is wrong because it subtracts the paid dividend again when rebuilding the new forward price, $F_t = 66.80(1.032)^{4/12} - 1.10 = 66.4051$, giving $(64.6202 - 66.4051)/1.010556 = -1.7662$.
> 4. **B.** Statement 1 is incorrect: a dividend paid in month 8 earns interest for only one month, so $\text{FV}(D) = 1.10(1.032)^{1/12} = 1.1029$ and $F_0 = 65.7347 - 1.1029 = 64.6318$, which is higher than 64.6202.
> Statement 2 is correct: $f_0 = S_0 e^{(r_c - CB)T}$ with a negative exponent of $3.10\% - 4.10\% = -1.00\%$, so the futures price is below spot and converges up to spot at expiration.
> A and C accept Statement 1, which reverses the effect of dividend timing on the future value of the carry benefit.
> 5. **A.** The equity return is already a six-month return and must not be annualized, but the fixed rate is annualized and accrues by $AP = 0.5$, so the periodic fixed payment is $0.5 \times 2.60\% = 1.30\%$.
> Net to the family office: $8{,}000{,}000 \times (-0.035 - 0.013) = -384{,}000$, so it pays 384,000.
> With a negative index return the receive-equity party pays both the equity decline and the fixed leg, which is the liquidity risk Keller is worried about.
> B is wrong because it charges the full annual fixed rate for a half-year period: $8{,}000{,}000 \times (-0.035 - 0.026) = -488{,}000$.
> C is wrong because it nets the equity decline against the fixed leg as if the family office received the fixed rate: $8{,}000{,}000 \times (0.035 - 0.013) = 176{,}000$ in magnitude.
> 6. **B.** Value the swap from the receive-fixed, pay-equity side first, then negate.
> The implied fixed-rate bond pays $8{,}000{,}000 \times 0.5 \times 0.026 = 104{,}000$ on each remaining date plus par at month 22.
> $V_{FIX} = 104{,}000 \times 3.853259 + 8{,}000{,}000 \times 0.937280 = 400{,}738.94 + 7{,}498{,}240.00 = 7{,}898{,}978.94$.
> The equity leg grows from the most recent reset: $(1{,}851.10/1{,}812.40) \times 8{,}000{,}000 = 1.021353 \times 8{,}000{,}000 = 8{,}170{,}823.22$.
> $V_{EQ,t} = 7{,}898{,}978.94 - 8{,}170{,}823.22 - 0 = -271{,}844.28$ to the receive-fixed party, so the family office (receive equity) holds $+271{,}844$.
> A is wrong because it reports the value to the counterparty that receives fixed and pays the equity return.
> C is wrong because it grows the equity leg from the initiation level: $(1{,}851.10/1{,}760.00) \times 8{,}000{,}000 = 8{,}414{,}090.91$, giving $8{,}414{,}090.91 - 7{,}898{,}978.94 = 515{,}111.97$, but the equity leg was trued back to notional at the reset two months ago.

## Distractor design

1. A: carry benefit ignored; C: dividend treated as a carry cost (sign error).
2. A: carry and reverse carry arbitrage swapped; B: profit at expiration reported instead of its present value (missing discounting).
3. A: undiscounted difference in forward prices; B: phantom carry flow, a dividend already paid subtracted again from $F_t$.
4. A and C: dividend timing effect on $\text{FV}(D)$ reversed.
5. B: annualized fixed rate not scaled by the accrual period; C: sign error on the fixed leg for the receive-equity party.
6. A: value reported for the wrong party (sign); C: equity leg grown from initiation instead of the last reset.
