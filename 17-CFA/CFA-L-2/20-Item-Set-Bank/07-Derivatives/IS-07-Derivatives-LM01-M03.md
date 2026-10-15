---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 1
title: "Ostrava Growth Fund: Index Futures Mispricing and a Seasoned Stock Forward"
los: [los-07-01-a, los-07-01-b]
difficulty: 4
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Ostrava Growth Fund: Index Futures Mispricing and a Seasoned Stock Forward

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Petra Novakova, CFA, runs the derivatives overlay for Ostrava Growth Fund, a long-only equity fund that uses futures and forwards to adjust exposure.
Her junior colleague, Emil Hartig, prepares the inputs each morning.
Novakova assumes no transaction costs, unrestricted short selling with full use of proceeds, and borrowing and lending at the risk-free rate.

The first item on today's agenda is the six-month futures contract on the Norland 100 index.
The index basket can be bought or sold short at the index level, and each futures contract has a multiplier of 50 per index point.

Exhibit 1: Norland 100 futures inputs (today)

| Item | Value |
|---|---|
| Index level | 4,250.00 |
| Continuously compounded dividend yield | 2.40% |
| Continuously compounded risk-free rate, six months | 3.60% |
| Annually compounded risk-free rate, six months | 3.67% |
| Quoted six-month futures price | 4,268.00 |
| Sell-side consensus index level in six months | 4,500.00 |
| Previous day's futures settlement price | 4,251.50 |

Hartig observes that the quoted futures price looks low relative to the carry model and suggests that the fund exploit it on a scale of 20 contracts.

The second item is a forward on Kestrel Pharma shares.
Seven months ago, when Kestrel traded at 52.00 and the annually compounded risk-free rate for all maturities was 4.0%, the fund entered a long one-year forward on Kestrel shares at the no-arbitrage forward price.
At that time Kestrel had declared two dividends: 0.60 per share payable three months after the forward's initiation and 0.65 per share payable nine months after initiation.

Exhibit 2: Kestrel Pharma inputs (today, seven months after initiation)

| Item | Value |
|---|---|
| Share price | 55.40 |
| Dividend paid four months ago | 0.60 |
| Dividend still to be paid (two months from today) | 0.65 |
| Annually compounded risk-free rate, all maturities | 4.5% |
| Months to forward expiration | 5 |

The first dividend was paid as scheduled, and the second dividend has been confirmed with no change in amount or timing.
Novakova needs the no-arbitrage forward price that was locked in at initiation and the current per-share value of the long forward for the fund's monthly valuation report.

At the weekly investment meeting, Hartig makes two statements.

Statement 1: "Because the sell-side consensus expects the Norland 100 to reach 4,500 in six months, the no-arbitrage six-month futures price should sit above the price that the carry model produces from today's index level."

Statement 2: "Holding Kestrel's share price and dividend unchanged, the rise in the risk-free rate from 4.0% to 4.5% since initiation has increased the value of our long Kestrel forward."

Novakova asks Hartig to confirm the arbitrage trade and the valuation figures before the report is circulated.

## Questions

1. Based on Exhibit 1, the arbitrage strategy Hartig should execute and the present value of its riskless profit per futures contract are best described as: (LOS: los-07-01-b)
   - A. buy the futures, short the index basket, and lend the proceeds, earning 372.
   - B. buy the futures, short the index basket, and lend the proceeds, earning 379.
   - C. sell the futures, borrow, and buy the index basket, earning 2,132.
2. The no-arbitrage price of the Kestrel forward at initiation was closest to: (LOS: los-07-01-a)
   - A. 52.81.
   - B. 52.83.
   - C. 54.08.
3. Based on Exhibit 2, the current value per share of the fund's long Kestrel forward is closest to: (LOS: los-07-01-a)
   - A. 2.31.
   - B. 2.91.
   - C. 3.55.
4. Which of Hartig's statements is correct? (LOS: los-07-01-b)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** With continuous compounding, the dividend yield is a carry benefit: $f_0 = 4{,}250\,e^{(0.0360 - 0.0240)(0.5)} = 4{,}250\,e^{0.0060} = 4{,}275.5767$.
> The quoted 4,268.00 is below the model price, so the futures is cheap and the trade is reverse carry arbitrage: buy the futures, short the index basket, and lend the proceeds.
> At expiration the lent proceeds net of the dividends owed on the shorted basket grow to 4,275.5767 while the futures purchase costs 4,268.00, a riskless gain of 7.5767 index points.
> Present value per point is $7.5767\,e^{-0.0360(0.5)} = 7.4415$, so per contract $7.4415 \times 50 = 372.07$.
> B is wrong because it reports the profit at expiration, $7.5767 \times 50 = 378.83$, without discounting it to today.
> C is wrong because it reverses the exponent to $(0.0240 - 0.0360)$, giving a model price of 4,224.5763 that makes the futures look rich; the resulting carry trade value $(4{,}268.00 - 4{,}224.5763)e^{-0.018} \times 50 = 2{,}132.45$ is a phantom.
> The annually compounded rate, the consensus level, and the previous settlement price are decoys.
> 2. **A.** Each dividend is a carry benefit compounded only from its payment date to expiration.
> $\text{FV}(S_0) = 52.00(1.04)^{1} = 54.0800$.
> $\text{FV}(D_1) = 0.60(1.04)^{9/12} = 0.6179$ and $\text{FV}(D_2) = 0.65(1.04)^{3/12} = 0.6564$.
> $F_0 = 54.0800 - 0.6179 - 0.6564 = 52.8057$.
> B is wrong because it subtracts the dividends without compounding them to expiration, $54.08 - 0.60 - 0.65 = 52.83$.
> C is wrong because it ignores both dividends and prices the forward as $\text{FV}(S_0)$ alone.
> 3. **B.** Only the dividend still to be paid is a remaining carry benefit, and the current rate of 4.5% applies.
> $\text{PV}(D_2) = 0.65/(1.045)^{2/12} = 0.6452$, so $F_t = (55.40 - 0.6452)(1.045)^{5/12} = 55.7682$.
> $V_t = (F_t - F_0)/(1.045)^{5/12} = (55.7682 - 52.8057)/1.018508 = 2.9626/1.018508 = 2.9087$.
> A is wrong because it also deducts the dividend already paid when rebuilding the forward price, $F_t = 55.7682 - 0.60(1.045)^{5/12} = 55.1571$, giving 2.3087.
> C is wrong because it ignores the pending dividend, $F_t = 55.40(1.045)^{5/12} = 56.4254$, giving 3.5540.
> 4. **B.** Statement 1 is incorrect: the carry model uses only the index level, the financing rate, the carry benefit, and time, so expectations of the future index level never enter the no-arbitrage price.
> Statement 2 is correct: a higher rate raises the new forward price $F_t$ for the remaining five months, which raises the long's value $\text{PV}[F_t - F_0]$.
> Repricing at 4.0% gives $V_t = 2.8045$, below the 2.9087 obtained at 4.5%.
> A and C accept Statement 1, which substitutes a forecast for the carry model.

## Distractor design

1. B: profit at expiration reported instead of its present value (missing discounting); C: sign of the carry exponent reversed, which turns reverse carry into carry arbitrage.
2. B: dividends subtracted without compounding to expiration; C: carry benefits ignored.
3. A: phantom carry flow, a paid dividend subtracted again from $F_t$; C: pending dividend ignored.
4. A and C: expectations of the future spot level treated as a pricing input; A also misreads the effect of the financing rate on a long forward.
