---
type: cfa-itemset
topic: "Alternative Investments"
topic_code: "08"
topic_slug: "08-Alternative-Investments"
lm: 1
title: "Kestrel Ridge Commodity Fund: Return Attribution"
los: [los-08-01-e, los-08-01-f, los-08-01-g, los-08-01-h]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/alternative-investments]
---

# Kestrel Ridge Commodity Fund: Return Attribution

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Daniela Okafor is a performance analyst at Kestrel Ridge Capital, which manages the Kestrel Ridge Commodity Fund.
The fund holds only fully collateralized long futures positions; collateral equal to the full notional value is invested in Treasury bills.
Okafor is preparing the attribution report for the four-month period ended 30 April, and her supervisor, Marcus Fenwick, CFA, reviews her work.

The fund's soybean position was established on 1 January at a futures price of 1,184.0 cents per bushel.
On 30 April, the fund rolled the entire position from the expiring contract into the next contract.
Treasury bills earned 4.8% annualized over the period, and the fund's management fee is 1.2% annualized.

Exhibit 1: Soybean roll, 30 April (cents per bushel)

| Contract | Price |
|---|---|
| Expiring (near) contract | 1,212.5 |
| Next (far) contract | 1,201.0 |

The fund also runs a sleeve that replicates a commodity index that rolls its crude oil exposure over five business days, 20% of the position per day.
On the third day of the most recent roll, the expiring contract settled at USD 78.40 per barrel and the next contract at USD 79.35 per barrel.

The fund's copper position has a dollar exposure of USD 18,900,000.
Copper futures cover 25,000 pounds per contract.
The expiring contract trades at USD 4.20 per pound and the next contract at USD 4.32 per pound, and Okafor must roll the position while keeping the dollar exposure constant.

Fenwick asks Okafor to explain the aluminum curve using the theory of storage.
She gathers the data in Exhibit 2.

Exhibit 2: Aluminum market data, 30 April (USD per metric ton)

| Item | Value |
|---|---|
| Spot price | 2,450 |
| Six-month futures price | 2,478 |
| Direct storage costs over six months (rent and insurance) | 61 |
| Annual warehouse load-out fee (not incurred if metal is not moved) | 18 |

Okafor's draft report includes two statements about spot and futures prices.

Statement 1: "On 30 April the aluminum basis was negative, indicating that the aluminum market was in contango."

Statement 2: "Because our lean hog futures contract is cash settled, its price is guaranteed to converge fully to the spot price at expiration."

While reviewing the report, Fenwick proposes adding a new sector to the fund.
He says: "I want the sector whose futures curves have historically been most likely to generate positive roll returns, so that roll return adds to price return rather than subtracting from it."
Okafor notes that most commodity sectors have shown statistically negative mean roll returns over long periods, and that roll return has had a correlation of only about 3% with price return.

## Questions

1. The four-month total return on the soybean position is closest to: (LOS: los-08-01-g)
   - A. 3.06%.
   - B. 4.96%.
   - C. 8.16%.
2. The index sleeve's crude oil roll return on the third day of the roll is closest to: (LOS: los-08-01-g)
   - A. -1.21%.
   - B. -0.24%.
   - C. +0.24%.
3. To maintain constant dollar exposure after the copper roll, the number of contracts held should: (LOS: los-08-01-h)
   - A. decrease from 180 to 175.
   - B. increase from 180 to 185.
   - C. remain at 180.
4. Based on Exhibit 2 and the theory of storage, the implied six-month convenience yield of aluminum is closest to: (LOS: los-08-01-f)
   - A. USD 28 per ton.
   - B. USD 33 per ton.
   - C. USD 89 per ton.
5. Which of Okafor's statements about spot and futures prices is correct? (LOS: los-08-01-e)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both statements.
6. The sector that best meets Fenwick's criterion is: (LOS: los-08-01-h)
   - A. precious metals, because gold can be stored indefinitely at low cost.
   - B. energy, because it is consumed nearly in real time with limited inventories, so its curves have been the most prone to backwardation.
   - C. livestock, because live animals cannot be stored indefinitely, so its curves are persistently in backwardation.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Price return $= (1{,}212.5 - 1{,}184.0)/1{,}184.0 = 2.4071\%$.
> Roll return $= (1{,}212.5 - 1{,}201.0)/1{,}212.5 \times 100\% = 0.9485\%$, positive because the market is in backwardation and the whole position is rolled.
> Collateral return $= 4.8\% \times 4/12 = 1.6000\%$.
> Total return $= 2.4071\% + 0.9485\% + 1.6000\% = 4.9555\% \approx 4.96\%$.
> The 1.2% management fee is a fund expense, not a component of the futures position's total return.
> A is wrong because it treats the roll return as negative ($2.4071 - 0.9485 + 1.6000 = 3.0586\%$), applying contango logic to a backwardated market.
> C is wrong because it adds the annualized collateral rate without scaling it to four months ($2.4071 + 0.9485 + 4.8000 = 8.1555\%$).
> 2. **B.** Gross roll return $= (78.40 - 79.35)/78.40 = -1.2117\%$, negative because the market is in contango.
> The index rolls 20% of the position that day, so the roll return is $-1.2117\% \times 0.20 = -0.2423\% \approx -0.24\%$.
> A is wrong because it ignores the percentage of the position rolled and reports the gross figure.
> C is wrong because it reverses the sign; the far contract is dearer, so rolling in contango produces a negative roll return.
> 3. **A.** Near contract value $= 4.20 \times 25{,}000 = 105{,}000$, so the fund holds $18{,}900{,}000 / 105{,}000 = 180$ contracts.
> Far contract value $= 4.32 \times 25{,}000 = 108{,}000$, so it needs $18{,}900{,}000 / 108{,}000 = 175$ contracts.
> The market is in contango, so each far contract is dearer and fewer contracts preserve the same dollar exposure.
> B is wrong because it applies the backwardation rule (buy more contracts when the far contract is cheaper) to a contango market.
> C is wrong because it rolls contract for contract, which would raise the exposure to $180 \times 108{,}000 = 19{,}440{,}000$.
> 4. **B.** Theory of storage: Futures price $=$ Spot price $+$ Direct storage costs $-$ Convenience yield.
> Convenience yield $= 2{,}450 + 61 - 2{,}478 = 33$ per ton.
> The load-out fee is a decoy: it is not incurred while the metal is stored, so it is not a direct storage cost over the six months.
> A is wrong because it treats the futures premium over spot ($2{,}478 - 2{,}450 = 28$) as the convenience yield, ignoring storage costs.
> C is wrong because it adds the storage costs to the futures premium ($2{,}478 - 2{,}450 + 61 = 89$), which moves direct storage costs to the wrong side of the storage equation.
> 5. **A.** Statement 1 is correct: basis $=$ spot $-$ futures $= 2{,}450 - 2{,}478 = -28$, and a negative basis (spot below futures) indicates contango.
> Statement 2 is incorrect: only physical delivery forces spot and futures prices to converge at expiration; cash-settled markets may not converge fully because of trading costs and other factors.
> B is wrong because it accepts the convergence claim for a cash-settled contract.
> C is wrong because Statement 2 misstates convergence for cash-settled contracts.
> 6. **B.** Energy is the only sector that has had a statistical chance of positive roll returns, because it is consumed nearly in real time with minimal storage, so scarce inventories and high convenience yields push its curves toward backwardation.
> A is wrong because gold's ability to be stored indefinitely is exactly why precious metals have persistently negative roll returns: stored commodities tend to trade in contango.
> C is wrong because livestock, along with industrial metals, agriculture, precious metals, and softs, has shown statistically strong negative mean roll returns.

## Distractor design

1. A: roll return sign reversed (contango logic in a backwardated market); C: annualized collateral rate not scaled to the holding period (the fee is a decoy for a further error).
2. A: percentage of the position rolled ignored (gross figure used); C: sign reversed for a contango roll.
3. B: backwardation rule applied to a contango market (direction of contract count reversed); C: contract-for-contract roll ignoring the price change.
4. A: storage costs omitted (futures premium read as convenience yield); C: direct storage costs moved to the wrong side of the storage equation (added to the futures premium instead of into the spot side); load-out fee is a misread-exhibit decoy.
5. B: convergence assumed for a cash-settled contract; C: same error combined with the correct basis reading.
6. A: storability read as favorable to roll return (sign of the storage effect reversed); C: perishability confused with backwardation, contradicting the empirical sector record.
