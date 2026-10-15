---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 1
title: "Harrowgate Savings Bank: Repricing the Curve for a Recession"
los: [los-09-01-d, los-09-01-e, los-09-01-f]
difficulty: 4
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Harrowgate Savings Bank: Repricing the Curve for a Recession

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Ines Calder, CFA, runs the treasury at Harrowgate Savings Bank, a regional deposit-taker that holds a liquidity portfolio of government and corporate zero-coupon bonds.
The bank's asset-liability committee, chaired by Marcus Oyelaran, has asked her to stress the portfolio against the house economist's recession scenario.
The scenario assumes that once the recession is confirmed, the central bank cuts its policy rate aggressively and markets reprice immediately.

Exhibit 1 shows today's government zero-coupon yields and the scenario's immediate changes.

Exhibit 1: Government zero-coupon yields (annual compounding)

| Maturity | Yield today | Scenario change |
|---|---|---|
| 3 months | 4.10% | -1.75 percentage points |
| 2 years | 3.40% | -1.60 percentage points |
| 5 years | 3.50% | -0.90 percentage points |
| 10 years | 3.70% | -0.35 percentage points |

Calder notes that the committee has always favored the maturity with the largest expected fall in yield when it expects easing.
She wants to show that ranking positions by yield change alone can mislead.

The bank also holds index-linked government bonds.
The 5-year index-linked zero yields 1.10% real today, and the economist expects that yield to fall to 0.70% under the scenario as expected real growth weakens.
She estimates today's 5-year inflation-uncertainty premium at 0.35% and expects it to rise by 0.10 percentage points under the scenario, because investors will become less sure of the inflation path once policy eases sharply.
Oyelaran asks what inflation rate the market would then be expecting over five years.

Calder's credit desk holds two 3-year zero-coupon corporate bonds.
Pellow Water is a regulated utility rated Aa, and Brackmoor Steel is a steel producer rated B.
Exhibit 2 decomposes the 3-year discount rates and gives the scenario changes.

Exhibit 2: 3-year discount rate components (annual compounding)

| Component | Today | Scenario change |
|---|---|---|
| Real default-free rate | 0.85% | -0.40 percentage points |
| Expected inflation | 2.30% | -0.70 percentage points |
| Inflation-uncertainty premium | 0.30% | +0.10 percentage points |
| Credit premium, Pellow Water (Aa) | 0.70% | +0.50 percentage points |
| Credit premium, Brackmoor Steel (B) | 4.20% | +2.60 percentage points |
| Pellow Water pre-tax interest coverage | 11.4x | not given |

The committee measures relative performance as the difference between two bonds' price returns under the immediate repricing.

After the stress results are presented, Calder and Oyelaran discuss what the curve will say once the scenario has played out.

Calder: "After the repricing, the curve will slope upward from 1.80% at two years to 3.35% at ten years, and that slope will tell us that the market expects the central bank to raise rates again."

Oyelaran: "Even if the market expected short rates to stay where they are, the curve would still slope upward, because long-dated government bonds hedge bad economic times less well than short-dated ones."

## Questions

1. Under the scenario, the highest price return among the 2-year, 5-year, and 10-year government zero-coupon bonds is closest to: (LOS: los-09-01-d)
   - A. 3.17%.
   - B. 3.44%.
   - C. 4.46%.
2. Under the scenario, the market's expected rate of inflation over the next five years is closest to: (LOS: los-09-01-e)
   - A. 1.45%.
   - B. 1.55%.
   - C. 1.90%.
3. Under the scenario, the amount by which the Pellow Water bond's price return exceeds the Brackmoor Steel bond's price return is closest to: (LOS: los-09-01-f)
   - A. 1.95 percentage points.
   - B. 5.48 percentage points.
   - C. 5.78 percentage points.
4. Regarding the statements made by Calder and Oyelaran about the post-scenario curve, which is correct? (LOS: los-09-01-d)
   - A. Calder's statement only.
   - B. Oyelaran's statement only.
   - C. Both statements.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** The price return on a zero is $\left(\frac{1 + y_0}{1 + y_1}\right)^n - 1$.
> 2-year: $(1.0340/1.0180)^2 - 1 = 3.1681\%$.
> 5-year: $(1.0350/1.0260)^5 - 1 = 4.4636\%$.
> 10-year: $(1.0370/1.0335)^{10} - 1 = 3.4386\%$.
> The 5-year bond wins: its yield falls less than the 2-year's but it has 2.5 times the maturity, and it falls more than twice as far as the 10-year's.
> The recession pattern, a large cut at the short end with long yields falling less because policy is expected to normalize, steepens the curve, but relative performance depends on yield change and maturity together.
> A is wrong because it picks the bond with the largest yield fall (the 2-year, 3.17%) and ignores maturity, which is the committee's habit.
> B is wrong because it picks the longest maturity (the 10-year, 3.44%) and ignores how little its yield moves in a steepening.
> The 3-month bill, with the largest yield change of all, returns only $(1.0410/1.0235)^{0.25} - 1 = 0.4247\%$, which is outside the comparison the stem asks for.
> 2. **A.** The 5-year nominal yield after the scenario is $3.50\% - 0.90\% = 2.60\%$, so the break-even inflation rate becomes $2.60\% - 0.70\% = 1.90\%$ (from $3.50\% - 1.10\% = 2.40\%$ today).
> $BEI = \theta_{t,s} + \pi_{t,s}$, and the premium becomes $0.35\% + 0.10\% = 0.45\%$, so $\theta_{t,5} = 1.90\% - 0.45\% = 1.45\%$, down from $2.40\% - 0.35\% = 2.05\%$ today.
> B is wrong because it subtracts today's 0.35% premium instead of the scenario's 0.45%: $1.90\% - 0.35\% = 1.55\%$.
> C is wrong because it reads the break-even rate as a pure inflation forecast and ignores the inflation-uncertainty premium.
> 3. **C.** The 3-year default-free component is $0.85\% + 2.30\% + 0.30\% = 3.45\%$ today and falls by $-0.40 - 0.70 + 0.10 = -1.00$ percentage point, to 2.45%.
> Pellow: yield moves from $3.45\% + 0.70\% = 4.15\%$ to $2.45\% + 1.20\% = 3.65\%$, so the return is $(1.0415/1.0365)^3 - 1 = +1.4542\%$.
> Brackmoor: yield moves from $3.45\% + 4.20\% = 7.65\%$ to $2.45\% + 6.80\% = 9.25\%$, so the return is $(1.0765/1.0925)^3 - 1 = -4.3296\%$.
> The difference is $1.4542\% - (-4.3296\%) = 5.7837$ percentage points, about 5.78, which is the quality outperformance expected as the cycle turns down and the quality spread widens.
> A is wrong because it treats the bonds as 1-year instruments and drops the exponent: $(1.0415/1.0365 - 1) - (1.0765/1.0925 - 1) = 0.4824\% + 1.4645\% = 1.95$ points.
> B is wrong because it applies only the credit premium changes and ignores the fall in default-free rates: Pellow $(1.0415/1.0465)^3 - 1 = -1.4265\%$, Brackmoor $(1.0765/1.1025)^3 - 1 = -6.9093\%$, difference 5.48 points.
> 4. **B.** Longer-dated government bonds are less negatively correlated with bad times than short-dated bonds, so investors demand a bond risk premium that rises with maturity, and a curve can slope upward even with flat rate expectations.
> Because the slope mixes rate expectations with maturity-increasing premiums, it cannot on its own reveal that the market expects hikes; expectations are indeterminate, so Calder is wrong.
> A is wrong because it reads rate expectations directly off an upward slope.
> C is wrong because Calder's statement claims more than the slope can support.

## Distractor design

1. A: largest yield change chosen without regard to maturity (misread exhibit, duration ignored); B: longest maturity chosen without regard to the small yield change (one driver dropped).
2. B: today's premium used with the scenario break-even rate (period mismatch); C: break-even rate read as expected inflation (premium ignored).
3. A: 3-year zeros priced as 1-year instruments (period); B: only credit premium changes applied, default-free channel ignored (component omitted).
4. A: upward slope read as expected rate rises (premium ignored); C: accepts Calder's claim (expectations treated as determinate).
