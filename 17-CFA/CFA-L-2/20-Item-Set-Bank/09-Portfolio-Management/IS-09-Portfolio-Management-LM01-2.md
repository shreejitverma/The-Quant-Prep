---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 1
title: "Castellane Mutual: Credit Premium Compliance Review"
los: [los-09-01-a, los-09-01-e, los-09-01-f, los-09-01-g]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Castellane Mutual: Credit Premium Compliance Review

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Daniel Osei is a credit analyst in the general account of Castellane Mutual, a property and casualty insurer that invests its reserves mainly in short-dated government and investment-grade corporate bonds.
Castellane's chief risk officer, Helena Marsh, must sign off on every new corporate purchase against the insurer's investment policy statement.
One clause of that statement reads as follows.

"A new corporate bond purchase must offer an implied credit premium that exceeds the issuer's one-year expected loss by at least 1.50 percentage points."

Osei is reviewing a proposed purchase of a one-year zero-coupon bond issued by Solent Cruises, a cruise ship operator.
Because the policy is written in terms of premiums rather than yields, he first has to isolate the premium for inflation uncertainty from a government bond of the same maturity.
Exhibit 1 shows the market data he gathered.

Exhibit 1: One-year zero-coupon bonds (face value 100)

| Item | Value |
|---|---|
| Government zero-coupon bond price | 96.40 |
| Solent Cruises zero-coupon bond price | 93.40 |
| One-year real default-free interest rate | 1.10% |
| Expected inflation over the next year | 2.30% |
| Three-month government bill yield | 3.05% |

Osei treats the inflation-uncertainty premium embedded in the government bond as applicable to the Solent bond as well.
Castellane's credit models provide the default estimates in Exhibit 2.

Exhibit 2: Solent Cruises credit data

| Item | Value |
|---|---|
| Senior unsecured rating | BB |
| One-year probability of default | 2.4% |
| Expected recovery rate, senior unsecured | 40% |
| Pre-tax interest coverage | 2.1x |

Marsh asks Osei to widen the review to two other BB and A issuers that the insurer already holds, because the insurer's economist expects a recession within the next year.
Exhibit 3 summarizes the three issuers.

Exhibit 3: Issuer comparison

| Issuer | Business | Rating | Pre-tax interest coverage | Current spread |
|---|---|---|---|---|
| Solent Cruises | Leisure cruises, discretionary demand | BB | 2.1x | 3.40% |
| Tarn Water | Regulated water supply, tariffs set by regulator | BB | 2.0x | 2.10% |
| Arden Motors | Premium passenger cars | A | 6.5x | 1.30% |

In the risk committee meeting, Marsh and Osei discuss how the portfolio should be positioned over the cycle.

Marsh: "Once this recession ends and spreads start to narrow, I expect our BB holdings to outperform our A-rated holdings."

Osei: "The recession should also help us on recoveries, because recovery rates on senior unsecured bonds rise during downturns, which reduces loss rates."

Marsh closes by asking Osei to explain, in writing, why Tarn Water and Solent Cruises carry the same rating but very different spreads.
She notes that interest coverage cannot be the reason, because the two ratios are nearly identical.

## Questions

1. The implied premium for inflation uncertainty in the government zero-coupon bond is closest to: (LOS: los-09-01-e)
   - A. 0.33%.
   - B. 2.63%.
   - C. 3.73%.
2. The implied credit premium in the Solent Cruises zero-coupon bond is closest to: (LOS: los-09-01-a)
   - A. 3.33%.
   - B. 3.67%.
   - C. 5.97%.
3. Relative to the investment policy clause, the Solent Cruises purchase offers a credit premium in excess of expected loss that is closest to: (LOS: los-09-01-f)
   - A. 0.93%, so the purchase fails the clause.
   - B. 1.89%, so the purchase meets the clause.
   - C. 2.37%, so the purchase meets the clause.
4. Regarding the statements made by Marsh and Osei during the risk committee meeting, which is correct? (LOS: los-09-01-f)
   - A. Marsh's statement only.
   - B. Osei's statement only.
   - C. Both statements.
5. If the economist's recession forecast is realized, the spread that will most likely widen the most is that of: (LOS: los-09-01-g)
   - A. Solent Cruises.
   - B. Tarn Water.
   - C. Arden Motors.
6. The best explanation Osei could give Marsh for the difference between the Tarn Water and Solent Cruises spreads is that: (LOS: los-09-01-g)
   - A. demand for Tarn's regulated, essential service is stable across the cycle, whereas demand for cruises is discretionary and procyclical.
   - B. Tarn's interest coverage is stronger than Solent's, which supports its credit quality in a downturn.
   - C. Tarn's higher rating signals a lower probability of default, so its spread responds less to the cycle.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The government bond's yield is $100/96.40 - 1 = 3.7344\%$.
> A one-year nominal default-free bond is priced at $l_{t,1} + \theta_{t,1} + \pi_{t,1}$, so $\pi_{t,1} = 1.037344 - (1 + 0.011 + 0.023) = 1.037344 - 1.034000 = 0.3344\%$, about 0.33%.
> B is wrong because it subtracts only the real rate: $3.7344\% - 1.10\% = 2.63\%$, leaving expected inflation inside the premium.
> C is wrong because it reports the whole yield, 3.73%, as the premium.
> 2. **A.** The Solent yield is $100/93.40 - 1 = 7.0664\%$.
> For a credit-risky bond the discount rate is $l_{t,1} + \theta_{t,1} + \pi_{t,1} + \gamma^i_{t,1}$, so $\gamma^i_{t,1} = 7.0664\% - (1.10\% + 2.30\% + 0.3344\%) = 7.0664\% - 3.7344\% = 3.3319\%$, about 3.33%.
> Equivalently, the credit premium is the corporate yield less the government yield of the same maturity: $7.0664\% - 3.7344\% = 3.33\%$.
> B is wrong because it leaves the 0.3344% inflation-uncertainty premium inside the credit premium: $7.0664\% - 3.40\% = 3.67\%$.
> C is wrong because it subtracts only the real rate: $7.0664\% - 1.10\% = 5.97\%$.
> 3. **B.** Expected loss is probability of default times one minus the recovery rate: $0.024 \times (1 - 0.40) = 1.44\%$.
> The excess of the credit premium over expected loss is $3.3319\% - 1.44\% = 1.8919\%$, about 1.89%, which exceeds the 1.50 percentage-point requirement, so the purchase meets the clause.
> The excess is the compensation for the undiversifiable tendency of defaults to cluster in downturns, which risk-averse investors demand on top of expected loss.
> A is wrong because it treats the probability of default itself as the expected loss: $3.3319\% - 2.40\% = 0.93\%$, which would fail the clause.
> C is wrong because it multiplies the probability of default by the recovery rate instead of the loss rate: $0.024 \times 0.40 = 0.96\%$ and $3.3319\% - 0.96\% = 2.37\%$.
> 4. **A.** When spreads narrow, investors discriminate less between weak and strong credits and the weakest payers improve fastest, so lower-rated bonds outperform higher-rated bonds; Marsh is correct.
> Osei is wrong because recovery rates are procyclical: they fall in recessions, so loss rates rise, which is one reason spreads widen in downturns.
> B is wrong because it accepts Osei's reversed recovery cyclicality and rejects the standard narrowing-spread rotation.
> C is wrong because Osei's statement is incorrect.
> 5. **A.** Spread widening in a downturn is largest where a low rating and a cyclical product market stack.
> Solent is BB and sells a discretionary leisure product, so both amplifiers apply.
> B is wrong because Tarn has the same low rating but a non-cyclical, regulated product, which removes the sector amplifier.
> C is wrong because Arden is cyclical but rated A, which removes the rating amplifier.
> 6. **A.** A company's credit quality depends on the market for its products: essential, price-inelastic demand under regulated tariffs keeps Tarn's revenue and cash flow stable in a downturn, while cruise demand is discretionary and falls sharply in recessions.
> Lenders therefore demand more compensation from Solent for the same rating, and its spread is more sensitive to the cycle.
> B is wrong because Exhibit 3 shows Tarn's coverage at 2.0x, slightly below Solent's 2.1x, and Marsh has already ruled coverage out.
> C is wrong because Exhibit 3 shows that both issuers are rated BB.

## Distractor design

1. B: expected inflation left inside the premium (component omitted); C: whole yield reported as the premium (no subtraction).
2. B: inflation-uncertainty premium left inside the credit premium (component omitted); C: only the real rate subtracted (two components omitted).
3. A: probability of default used as expected loss (recovery ignored); C: recovery rate used in place of the loss rate (wrong formula variant).
4. B: recovery-rate cyclicality reversed and quality rotation rejected (direction); C: accepts the reversed recovery claim (direction).
5. B: sector dimension ignored, rating only (one amplifier dropped); C: rating dimension ignored, sector only (other amplifier dropped).
6. B: coverage ratios misread from Exhibit 3 (misread exhibit); C: ratings misread from Exhibit 3 (misread exhibit).
