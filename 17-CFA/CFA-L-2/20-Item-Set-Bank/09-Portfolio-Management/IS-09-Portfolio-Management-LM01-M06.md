---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 1
title: "Varenna State Investment Fund: An Office Bid and the Equity Sleeve"
los: [los-09-01-a, los-09-01-h, los-09-01-j, los-09-01-k]
difficulty: 4
minutes: 12
source: mock-06
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Varenna State Investment Fund: An Office Bid and the Equity Sleeve

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tamsin Holt, CFA, is a senior analyst in the real assets team of the Varenna State Investment Fund, a sovereign fund that invests commodity revenues for future generations.
The fund's head of strategy, Emil Rautio, has asked her to assess a bid for an office building and to review how the fund sets required returns on its listed equities.

The building is Albury Court, let in full to Carden Pharmaceuticals plc.
Exhibit 1 gives the terms.

Exhibit 1: Albury Court

| Item | Value |
|---|---|
| Annual rent, fixed, paid at the end of each year | EUR 2,400,000 |
| Remaining lease term | 6 years |
| Estimated resale value at the end of year 6 | EUR 36,000,000 |
| Asking price | EUR 33,500,000 |
| Initial rental yield at asking price | 7.16% |
| Yield on Carden's 6-year senior unsecured bond | 5.40% |
| 6-year government bond yield | 3.90% |
| Fund's required property risk premium | 0.80% |
| Fund's required liquidity premium | 1.50% |

Holt first wants to know what liquidity premium the seller's asking price offers, given the discount rate components she can observe and the fund's property risk premium.

Rautio then asks her to test the bid against the fund economist's recession scenario, summarized in Exhibit 2.
The scenario is applied to the fund's own required return, which starts from Carden's bond yield plus the two property premiums in Exhibit 1.

Exhibit 2: Recession scenario, changes from today

| Item | Change |
|---|---|
| Real default-free rate | -0.30 percentage points |
| Expected inflation | -0.40 percentage points |
| Inflation-uncertainty premium | unchanged |
| Carden's credit premium | +0.60 percentage points |
| Property risk premium | unchanged |
| Liquidity premium | +0.50 percentage points |
| Estimated resale value at the end of year 6 | -8% |

Rent is contractual and unaffected by the scenario.

Holt turns to the listed equity sleeve.
Exhibit 3 shows three holdings.

Exhibit 3: Selected listed holdings

| Company | Business | Return volatility | Beta to domestic index | Correlation of returns with real consumption growth |
|---|---|---|---|---|
| Brenlow Group | Luxury goods | 24% | 1.35 | +0.65 |
| Hollin Recoveries | Debt collection, revenue rises when defaults rise | 31% | 0.25 | -0.20 |
| Marwick Foods | Packaged staples | 14% | 0.60 | +0.35 |

Rautio remarks that Hollin should carry the highest required return in the sleeve, because its returns are the most volatile.

Finally, the fund's equity strategist has built three macro scenarios for the domestic market.
In each, expected real earnings growth is unchanged.
Exhibit 4 shows the changes in the components of the equity discount rate.

Exhibit 4: Changes in equity discount rate components (percentage points)

| Component | Scenario X | Scenario Y | Scenario Z |
|---|---|---|---|
| Real default-free rate | -0.40 | +0.10 | -0.20 |
| Expected inflation | +0.30 | -0.50 | +0.40 |
| Inflation-uncertainty premium | +0.20 | -0.10 | +0.10 |
| Equity risk premium | -0.30 | +0.30 | -0.10 |

## Questions

1. The liquidity premium implied by the asking price for Albury Court is closest to: (LOS: los-09-01-k)
   - A. 1.98%.
   - B. 2.78%.
   - C. 3.48%.
2. Under the recession scenario, the value of Albury Court at the fund's required return and the resulting decision are closest to: (LOS: los-09-01-a)
   - A. EUR 30,797,897; do not buy.
   - B. EUR 31,816,975; do not buy.
   - C. EUR 33,621,813; buy.
3. Regarding Rautio's remark about Hollin Recoveries, the most accurate response is that, of the three holdings, Hollin should most likely carry: (LOS: los-09-01-h)
   - A. the highest equity risk premium, because its return volatility is the highest.
   - B. the lowest equity risk premium, and its required return could be below the default-free rate.
   - C. the lowest equity risk premium, but its required return must exceed the default-free rate because it is an equity.
4. Holding all else constant, the equilibrium P/E of the domestic market is most likely to rise under: (LOS: los-09-01-j)
   - A. Scenarios X and Y only.
   - B. Scenarios X and Z only.
   - C. Scenario Y only.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** At the asking price, the internal rate of return solves $33{,}500{,}000 = \sum_{t=1}^{6} 2{,}400{,}000/(1+r)^t + 36{,}000{,}000/(1+r)^6$, giving $r = 8.1769\%$ (calculator: N = 6, PV = -33,500,000, PMT = 2,400,000, FV = 36,000,000, CPT I/Y).
> Carden's bond yield of 5.40% already contains $l_{t,s} + \theta_{t,s} + \pi_{t,s} + \gamma^i_{t,s}$, so the implied liquidity premium is $\phi^i_{t,s} = 8.1769\% - 5.40\% - 0.80\% = 1.9769\%$, above the fund's 1.50% requirement.
> B is wrong because it does not subtract the property risk premium $\kappa^i_{t,s}$, attributing all of the excess over the tenant's yield to liquidity: $8.1769\% - 5.40\% = 2.78\%$.
> C is wrong because it starts from the government yield and so omits the tenant's credit premium: $8.1769\% - 3.90\% - 0.80\% = 3.48\%$.
> The 7.16% initial rental yield is a decoy; it ignores the resale value and is not a discount rate.
> 2. **B.** Today's required return is $5.40\% + 0.80\% + 1.50\% = 7.70\%$, which values the building at EUR 34,264,525, above the asking price.
> The scenario moves all three channels: default-free rates ($-0.30 - 0.40 + 0.00 = -0.70$), risk premiums ($+0.60 + 0.00 + 0.50 = +1.10$), and expected cash flows (resale cut to $36{,}000{,}000 \times 0.92 = 33{,}120{,}000$).
> The new rate is $7.70\% - 0.70\% + 1.10\% = 8.10\%$.
> Present values at 8.10%: 2,220,167; 2,053,808; 1,899,915; 1,757,553; 1,625,859; and year 6 gives $35{,}520{,}000/1.081^6 = 22{,}259{,}674$, for a total of EUR 31,816,975.
> That is below the EUR 33,500,000 asking price, so the fund should not buy under the scenario.
> A is wrong because it applies only the premium changes and ignores the fall in default-free rates, discounting at 8.80%.
> C is wrong because it applies the discount rate change but not the cash flow channel, keeping the EUR 36,000,000 resale value, which flips the decision to buy.
> 3. **B.** The equity risk premium depends on how an asset's payoff covaries with bad times, not on its standalone volatility.
> Hollin's returns are negatively correlated with consumption growth, so it pays off when the marginal utility of consumption is high; its covariance with the inter-temporal rate of substitution is positive, its risk premium is negative or small, and its required return can sit below the default-free rate.
> Brenlow, with the strongest positive correlation with consumption, is the worst consumption hedge and should carry the highest premium.
> A is wrong because it prices total volatility rather than covariance with bad times, which is Rautio's error.
> C is wrong because it assumes every risky asset must earn more than the default-free rate, ignoring that a consumption hedge carries a negative premium.
> 4. **A.** With expected real earnings growth unchanged, the equilibrium P/E rises when the total discount rate $l + \theta + \pi + \lambda$ falls.
> Scenario X: $-0.40 + 0.30 + 0.20 - 0.30 = -0.20$, so the P/E rises.
> Scenario Y: $+0.10 - 0.50 - 0.10 + 0.30 = -0.20$, so the P/E rises.
> Scenario Z: $-0.20 + 0.40 + 0.10 - 0.10 = +0.20$, so the P/E falls.
> B is wrong because it ignores the inflation components and sums only the real rate and equity risk premium (X $-0.70$, Y $+0.40$, Z $-0.30$).
> C is wrong because it judges each scenario by the direction of expected inflation alone (X $+0.30$, Y $-0.50$, Z $+0.40$).

## Distractor design

1. B: property risk premium not subtracted (component omitted); C: government yield used in place of the tenant's bond yield (credit premium omitted).
2. A: default-free rate channel ignored (one channel dropped); C: cash flow channel ignored, resale value not revised (other channel dropped).
3. A: standalone volatility treated as priced risk (wrong risk concept); C: required return floored at the default-free rate (sign of the hedge premium).
4. B: inflation components omitted from the discount rate (real vs nominal); C: expected inflation used as the only driver (one component only).
