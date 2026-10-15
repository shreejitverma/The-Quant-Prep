---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 5
title: "Kestrel Mutual: Historical Tail Losses and Capital Hurdles"
los: [los-09-05-b, los-09-05-c, los-09-05-d, los-09-05-e, los-09-05-k, los-09-05-l]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Kestrel Mutual: Historical Tail Losses and Capital Hurdles

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Amara Osei, CFA, is chief risk officer of Kestrel Mutual Insurance, a Canadian property and casualty insurer.
Kestrel's CAD 400 million investment portfolio holds government bonds, investment-grade corporate bonds, privately placed corporate bonds, Canadian equities, catastrophe bonds, and a small book of equity index options.
The private placements are large relative to their trading volume and trade only occasionally.

Kestrel estimates one-day VaR by historical simulation.
The risk system reprices the current portfolio on each of the last 200 trading days, sorts the resulting returns from worst to best, and reads the $x\%$ VaR as the outcome ranked $x\% \times 200$ from the worst.
It computes conditional VaR as the average of the outcomes ranked 1 through $x\% \times 200$.
For comparison, a parametric model run on long-run inputs gives a one-day 5% VaR of CAD 10.9 million.

Exhibit 1: Twelve worst simulated daily returns of the current portfolio, 200-day lookback

| Rank | Return | Rank | Return |
|---|---|---|---|
| 1 | -3.42% | 7 | -2.31% |
| 2 | -2.97% | 8 | -2.22% |
| 3 | -2.81% | 9 | -2.15% |
| 4 | -2.64% | 10 | -2.09% |
| 5 | -2.50% | 11 | -2.02% |
| 6 | -2.38% | 12 | -1.96% |

Kestrel's chief investment officer, Daniel Moreau, expects market volatility over the coming year to be well above the level observed in the lookback period.
He also plans to increase the catastrophe bond and option positions, both of which have markedly non-normal return distributions.
Moreau asks Osei which VaR method Kestrel should adopt given these expectations.

Osei then turns to capital allocation.
Kestrel measures economic capital for each underwriting line at the 99.5% confidence level over one year and requires each line to earn a return on allocated economic capital of at least 12.5%.
Kestrel's cost of equity is estimated at 10.5%.
Kestrel's solvency regulator separately prescribes a capital requirement for each line with a standard formula, which Osei reports alongside her own economic capital estimates.

Exhibit 2: Underwriting lines (CAD millions)

| Line | Expected annual profit | Economic capital | Regulatory capital requirement |
|---|---|---|---|
| Commercial property | 25.2 | 180 | 110 |
| Marine | 7.8 | 60 | 70 |
| Personal auto | 26.4 | 240 | 190 |

Kestrel's board is also evaluating the acquisition of Borealis Life, a life insurer whose liabilities are long-dated annuity and life policies.
A director asks how Borealis's risk measurement would differ from Kestrel's current framework.

Finally, Kestrel's treasurer, Colin Barr, tells the board: "Because our historical simulation reprices the portfolio on actual market prices, our VaR fully reflects what it would cost to sell the private placements in a stressed market."

## Questions

1. Based on Exhibit 1, Kestrel's one-day 5% VaR is closest to: (LOS: los-09-05-c)
   - A. CAD 8.36 million.
   - B. CAD 10.00 million.
   - C. CAD 11.88 million.
2. Based on Exhibit 1, Kestrel's one-day 5% conditional VaR is closest to: (LOS: los-09-05-e)
   - A. CAD 9.82 million.
   - B. CAD 10.20 million.
   - C. CAD 12.78 million.
3. Given Moreau's expectations, the VaR method Osei should recommend is the: (LOS: los-09-05-b)
   - A. parametric method.
   - B. historical simulation method.
   - C. Monte Carlo simulation method.
4. Based on Exhibit 2, capital should be allocated to: (LOS: los-09-05-k)
   - A. commercial property and personal auto only.
   - B. commercial property, marine, and personal auto.
   - C. commercial property and marine only.
5. Compared with Kestrel, Borealis Life's risk measurement is most likely to place greater emphasis on: (LOS: los-09-05-l)
   - A. economic capital and VaR estimates for catastrophe losses.
   - B. asset-liability matching and scenarios that stress market and non-market factors together.
   - C. ex ante tracking error relative to a published market benchmark.
6. The main flaw in Barr's statement is that: (LOS: los-09-05-d)
   - A. VaR does not capture the liquidity risk of positions that are large relative to their trading volume.
   - B. historical simulation assumes that returns are normally distributed.
   - C. VaR cannot be estimated for fixed-income positions with different durations.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The 5% VaR is the outcome ranked $0.05 \times 200 = 10$ from the worst, a return of $-2.09\%$.
> VaR $= 0.0209 \times 400{,}000{,}000 = \text{CAD } 8{,}360{,}000$, about CAD 8.36 million.
> B is wrong because it reads "5%" as the fifth-worst outcome: $0.0250 \times 400\text{m} = \text{CAD } 10.00$ million.
> C is wrong because it takes the second-worst outcome, rank $0.01 \times 200 = 2$, which is the 1% VaR: $0.0297 \times 400\text{m} = \text{CAD } 11.88$ million.
> The historical VaR sits below the CAD 10.9 million parametric figure, consistent with a lookback calmer than the long-run inputs.
> 2. **B.** CVaR averages the 10 outcomes in the 5% tail: sum $= -25.49\%$, average $= -2.5490\%$.
> CVaR $= 0.025490 \times 400{,}000{,}000 = \text{CAD } 10{,}196{,}000$, about CAD 10.20 million.
> A is wrong because it averages all 12 rows in the exhibit, including two outcomes outside the tail: average $-2.4558\%$, CAD 9.82 million.
> C is wrong because it averages only the two worst outcomes, which is the 1% CVaR: average $-3.1950\%$, CAD 12.78 million.
> 3. **C.** Monte Carlo simulation lets the user specify any distribution and any parameters, so Osei can impose the higher volatility Moreau expects and the non-normal payoffs of the catastrophe bonds and options.
> A is wrong because the parametric method assumes normality, which fits option and catastrophe bond returns poorly, and is hostage to its parameter estimates.
> B is wrong because historical simulation is tied to a lookback that Moreau expects to understate future volatility.
> 4. **C.** Return on allocated economic capital: property $25.2/180 = 14.0\%$; marine $7.8/60 = 13.0\%$; auto $26.4/240 = 11.0\%$.
> Against the 12.5% hurdle, property and marine qualify and auto does not, despite auto's larger absolute profit.
> A is wrong because it divides by the regulatory capital requirement instead of the economic capital the policy names: property $22.9\%$, marine $11.1\%$, auto $13.9\%$, which reverses the marine and auto results.
> B is wrong because it compares returns with the 10.5% cost of equity rather than the 12.5% hurdle rate.
> 5. **B.** Life insurers have long, discount-rate-sensitive liabilities, so they emphasize closer asset-liability matching and scenarios that stress market factors together with non-market factors such as longevity and mortality.
> A is wrong because economic capital and VaR for catastrophe losses are characteristic of property and casualty lines like Kestrel's own.
> C is wrong because ex ante tracking error against a market benchmark is the core measure of long-only asset managers, not of an insurer's balance sheet.
> 6. **A.** VaR does not account for liquidity: a large position that trades rarely could not be sold at the prices used in the simulation, so VaR can understate the risk even in normal markets, and liquidity tends to vanish in the tail events VaR is meant to describe.
> B is wrong because historical simulation relies on no distributional assumption at all.
> C is wrong because a well-built VaR does adjust for bonds of different durations.

## Distractor design

1. B: percentile misread as a rank (5th worst instead of rank 10); C: wrong threshold (1% VaR at rank 2).
2. A: misread exhibit (all 12 listed rows averaged, including outcomes outside the tail); C: wrong threshold (1% tail of two observations).
3. A: normality assumed for non-normal payoffs; B: method tied to an unrepresentative lookback.
4. A: wrong denominator (regulatory capital requirement instead of economic capital); B: wrong benchmark rate (cost of equity instead of hurdle rate).
5. A: property and casualty measures assigned to a life insurer; C: asset manager measure assigned to an insurer.
6. B: normality attributed to historical simulation; C: a non-limitation (duration handling) offered as the flaw.
