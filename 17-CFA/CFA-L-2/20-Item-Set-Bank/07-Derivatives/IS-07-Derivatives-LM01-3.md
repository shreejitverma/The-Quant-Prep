---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 1
title: "Harbourline Assurance: Bond Futures and Cross-Currency Swap Review"
los: [los-07-01-d, los-07-01-f]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Harbourline Assurance: Bond Futures and Cross-Currency Swap Review

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Harbourline Assurance plc is a UK life insurer whose investment mandate requires every derivative trade to be pre-cleared by the risk and compliance function.
Fiona Mackintosh, a fixed-income portfolio manager, submits two proposals, and Rajiv Menon, CFA, the head of investment risk, reviews them.
Menon assumes no transaction costs, unrestricted short selling, and borrowing and lending at the risk-free rate.

Mackintosh's first proposal concerns a government bond futures contract.
The cheapest-to-deliver bond pays a 3.50% annual coupon semiannually on a 180-day coupon period.

Exhibit 1: Bond futures inputs (per 100 par)

| Item | Value |
|---|---|
| Quoted (clean) price of the deliverable bond | 101.40 |
| Days since the last coupon | 120 |
| Days until the next coupon | 60 |
| Futures expiration | 150 days (5 months) |
| Conversion factor | 0.8740 |
| Quoted futures price | 118.10 |
| Risk-free rate to expiration, annual compounding | 2.80% |
| Yield to maturity of the deliverable bond | 3.18% |

Mackintosh believes the quoted futures price is out of line with the carry model and proposes a trade to capture the difference.

Her second proposal is a one-year fixed-for-fixed currency swap with quarterly settlements.
Harbourline would pay GBP 80,000,000 to the dealer at initiation and receive the equivalent US dollar notional, which it would invest in US dollar corporate bonds.
Each quarter Harbourline would pay US dollar fixed and receive sterling fixed, and at maturity the notionals would be re-exchanged.
The spot exchange rate is US$1.2650 per GBP 1.

Exhibit 2: Spot rates today (add-on, actual/360)

| Days | 90 | 180 | 270 | 360 |
|---|---|---|---|---|
| US dollar | 4.52% | 4.46% | 4.40% | 4.33% |
| Sterling | 4.18% | 4.14% | 4.09% | 4.02% |

Menon wants to test how the swap would be reported if markets moved sharply after execution.
He builds a scenario 90 days after initiation, immediately after the first quarterly exchange of fixed payments, in which the spot exchange rate is US$1.2410 per GBP 1.

Exhibit 3: Scenario spot rates 90 days after initiation (add-on, actual/360)

| Days | 90 | 180 | 270 |
|---|---|---|---|
| US dollar | 4.68% | 4.63% | 4.57% |
| Sterling | 3.96% | 3.90% | 3.84% |

In his review memo, Menon records two statements.

Statement 1: "Because the dollar notional is set by converting our sterling notional at the initial spot rate, the two fixed swap rates also depend on that exchange rate and would change if it moved before execution."

Statement 2: "The notionals are exchanged at initiation and again at maturity, and the quarterly fixed payments are not netted because they are made in different currencies."

Menon notes that Harbourline reports in sterling, so the scenario value must be stated in GBP.

## Questions

1. Based on Exhibit 1, the full spot price of the deliverable bond is closest to: (LOS: los-07-01-d)
   - A. 101.98.
   - B. 102.57.
   - C. 103.73.
2. Based on Exhibit 1, the equilibrium quoted futures price is closest to: (LOS: los-07-01-d)
   - A. 115.69.
   - B. 116.70.
   - C. 117.71.
3. The arbitrage trade that Menon should approve, and its present value per 100 par, are best described as: (LOS: los-07-01-d)
   - A. sell the futures, borrow, and buy the bond, earning 2.08.
   - B. buy the futures, short the bond, and lend the proceeds, earning 2.08.
   - C. sell the futures, borrow, and buy the bond, earning 2.38.
4. Based on Exhibit 2, the annualized fixed rate on the sterling leg of the currency swap is closest to: (LOS: los-07-01-f)
   - A. 0.99%.
   - B. 3.96%.
   - C. 5.26%.
5. In Menon's scenario, the value of the currency swap to Harbourline is closest to: (LOS: los-07-01-f)
   - A. -GBP 1,300,900.
   - B. -GBP 1,276,219.
   - C. GBP 1,300,900.
6. Which of Menon's statements is correct? (LOS: los-07-01-f)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Accrued interest runs from the last coupon: $AI_0 = (120/180)(3.50/2) = 1.1667$.
> Full price $= B_0 + AI_0 = 101.40 + 1.1667 = 102.5667$.
> A is wrong because it accrues over the 60 days until the next coupon, $101.40 + (60/180)(1.75) = 101.9833$.
> C is wrong because it accrues the full annual coupon rather than the semiannual coupon, $101.40 + (120/180)(3.50) = 103.7333$.
> 2. **A.** A coupon of 1.75 is paid in 60 days, 90 days before expiration, so it is a carry benefit and accrual restarts after it.
> $\text{FV}(B_0 + AI_0) = 102.5667(1.028)^{5/12} = 103.7536$.
> $FVCI = 1.75(1.028)^{3/12} = 1.7621$ and $AI_T = (90/180)(1.75) = 0.8750$.
> $Q_0 = (1/0.8740)(103.7536 - 0.8750 - 1.7621) = 101.1165/0.8740 = 115.6940$.
> B is wrong because it omits $AI_T$, although the futures settles on the clean price: $(103.7536 - 1.7621)/0.8740 = 116.6951$.
> C is wrong because it omits the future value of the interim coupon: $(103.7536 - 0.8750)/0.8740 = 117.7101$.
> The 3.18% yield to maturity is a decoy; the carry model uses the financing rate.
> 3. **A.** The quoted futures price of 118.10 exceeds the equilibrium 115.6940, so the futures is rich and the trade is carry arbitrage: sell the futures, borrow 102.5667, buy the bond, and reinvest the coupon.
> At expiration, the delivery proceeds are $CF \times Q + AI_T = 0.8740 \times 118.10 + 0.8750 = 104.0944$, against loan repayment net of the coupon of $103.7536 - 1.7621 = 101.9915$, a profit of 2.1029.
> Its present value is $2.1029/(1.028)^{5/12} = 2.0788$ per 100 par.
> B is wrong because reverse carry arbitrage is the trade only when the futures is cheap relative to the carry model.
> C is wrong because it measures the mispricing in quoted futures points without the conversion factor: $(118.10 - 115.6940)/(1.028)^{5/12} = 2.3785$.
> 4. **B.** Sterling PV factors: $1/[1 + 0.0418(0.25)] = 0.989658$, $1/[1 + 0.0414(0.50)] = 0.979720$, $1/[1 + 0.0409(0.75)] = 0.970238$, $1/[1 + 0.0402(1.00)] = 0.961354$, summing to 3.900969.
> $r_{GBP} = (1 - 0.961354)/3.900969 \times (360/90) = 0.9907\% \times 4 = 3.9627\%$.
> A is wrong because it reports the quarterly periodic rate without annualizing.
> C is wrong because it drops the final PV factor from the annuity sum, $(1 - 0.961354)/2.939615 \times 4 = 5.2587\%$.
> 5. **A.** The exchange rate is quoted in US dollars per pound, so currency a is the US dollar and $NA_a = 1.2650 \times 80{,}000{,}000 = \text{US}\$101{,}200{,}000$.
> US dollar PV factors today are 0.988826, 0.978186, 0.968054, 0.958497 (sum 3.893564), so $r_{USD} = (1 - 0.958497)/3.893564 \times 4 = 4.2637\%$, a periodic coupon of 1.0659%.
> Scenario US dollar factors: 0.988435, 0.977374, 0.966861 (sum 2.932670); the US dollar bond is worth $1.0659\% \times 2.932670 + 0.966861 = 0.998121$ per 1, or US\$101,009,870.
> Scenario sterling factors: 0.990197, 0.980873, 0.972006 (sum 2.943076); the sterling bond is worth $0.9907\% \times 2.943076 + 0.972006 = 1.001163$ per 1, or GBP 80,093,033.
> $V_{CS} = 101{,}009{,}870 - 1.2410 \times 80{,}093{,}033 = 101{,}009{,}870 - 99{,}395{,}454 = \text{US}\$1{,}614{,}417$ to the party receiving US dollars, which is the dealer.
> Harbourline receives sterling, so its value is $-1{,}614{,}417/1.2410 = -\text{GBP }1{,}300{,}900$; the pound's depreciation outweighs the gains from higher US dollar rates and lower sterling rates.
> B is wrong because it translates the US dollar value at the initial spot rate, $-1{,}614{,}417/1.2650 = -\text{GBP }1{,}276{,}219$.
> C is wrong because it treats Harbourline as the receiver of currency a and reports the dealer's value.
> 6. **B.** Statement 1 is incorrect: each fixed rate comes from its own currency's term structure, $r = (1 - PV_n)/\sum PV_i \times 1/AP$, and does not depend on the notional or the exchange rate.
> Statement 2 is correct: notionals are exchanged at both ends, and payments in two currencies cannot be netted.
> A and C accept Statement 1, which confuses setting the notionals through $S_0$ with pricing the fixed rates.

## Distractor design

1. A: accrual counted to the next coupon instead of from the last; C: annual coupon used instead of the periodic coupon.
2. B: $AI_T$ omitted (clean versus full price at expiration); C: $FVCI$ omitted (interim coupon ignored).
3. B: carry and reverse carry arbitrage swapped; C: mispricing measured in quoted points without the conversion factor.
4. A: periodic rate not annualized; C: final PV factor dropped from the annuity sum.
5. B: translation at $S_0$ instead of $S_t$; C: currency a misidentified, value reported for the wrong party (sign).
6. A and C: fixed rates wrongly tied to the exchange rate used to set the notionals.
