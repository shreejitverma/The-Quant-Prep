---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 4
title: "Bellweather Credit Partners: Default Timing in a High-Yield Sleeve"
los: [los-06-04-a, los-06-04-e, los-06-04-g]
difficulty: 3
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Bellweather Credit Partners: Default Timing in a High-Yield Sleeve

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Oluwaseun Adeyemi, CFA, is a credit analyst at Bellweather Credit Partners, a hedge fund that runs a long-short high-yield sleeve.
His portfolio manager, Clara Ventimiglia, asks him to review three candidate bonds for a one-year trade and one bond for a longer holding.

For the one-year trade, Adeyemi summarizes his credit assumptions in Exhibit 1.
Recovery rates are stated as a percentage of the exposure.
The differences in exposure arise from differences in coupon rates, and the three bonds have similar yields to maturity.

Exhibit 1: Candidate bonds for the one-year trade (per 100 of par)

| Bond | Issuer | Exposure | Recovery rate | Probability of default | Agency rating |
|---|---|---|---|---|---|
| X | Arcadia Hotels | 106.00 | 40% | 1.20% | BB- |
| Y | Quillon Mining | 99.00 | 30% | 1.05% | BB |
| Z | Stellan Pharma | 94.00 | 20% | 1.00% | BB+ |

For the longer holding, Adeyemi analyzes a senior unsecured bond issued by Pemberton Freight Rail.
The bond has three years to maturity, pays a 5.25% coupon annually, and trades at 105.50 per 100 of par.
He assumes that the government bond yield curve is flat at 2.25%, that there is no interest rate volatility, and that default can occur only on coupon dates.
The fund's credit research group supplies a risk-neutral annual (hazard) probability of default of 1.80% and a recovery rate of 45% of the exposure.
Adeyemi notes that the historical one-year default rate for issuers with Pemberton's rating is 0.90% and that the bond's modified duration is 2.77.

Exhibit 2: Inputs for the Pemberton bond (per 100 of par)

| Date | Exposure | Discount factor |
|---|---|---|
| 1 | 111.0534 | 0.977995 |
| 2 | 108.1840 | 0.956474 |
| 3 | 105.2500 | 0.935427 |

Ventimiglia asks Adeyemi to show what the fund would earn on the Pemberton bond, bought at its market price, if Pemberton defaults on Date 2 and bondholders receive the assumed recovery on that date.
She wants the committee to see how widely the outcomes spread across default dates.

Finally, Ventimiglia compares the credit spread curves of two other issuers.
Helmsley Water, an AA rated regulated utility, has a spread curve that is flat to slightly upward sloping, rising from 35 bps at two years to 55 bps at ten years.
Draxton Steel, a BB rated producer, has an inverted spread curve, with 520 bps at two years and 390 bps at ten years.
The steel industry is at a cyclical trough, and industry forecasters expect demand and margins to recover over the next three years.
Draxton's bonds trade between 88 and 92 per 100 of par, well above any plausible recovery value, and Draxton has no debt maturing for four years.

## Questions

1. Ranked from highest to lowest credit risk over the next year, the three candidate bonds in Exhibit 1 are: (LOS: los-06-04-a)
   - A. X, Z, Y.
   - B. X, Y, Z.
   - C. Z, Y, X.
2. The fair value of the Pemberton bond and the conclusion Adeyemi should draw at its market price are closest to: (LOS: los-06-04-e)
   - A. 105.59; the bond is undervalued.
   - B. 105.45; the bond is overvalued.
   - C. 108.61; the bond is undervalued.
3. If the fund buys the Pemberton bond at 105.50 and Pemberton defaults on Date 2, the annual rate of return is closest to: (LOS: los-06-04-a)
   - A. -22.37%.
   - B. -29.54%.
   - C. -32.15%.
4. The most appropriate interpretation of Draxton Steel's inverted spread curve is that: (LOS: los-06-04-g)
   - A. all of Draxton's bonds trade near their recovery value, so the inversion is an optical effect of annualizing the same loss over different horizons.
   - B. investors expect Draxton's credit quality to improve as the industry recovers, so near-term default risk is priced above longer-term default risk.
   - C. longer-maturity bonds of any issuer carry less credit risk, which is why Helmsley's curve would also invert if its rating fell.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Credit risk combines the probability of default with the loss given default, so rank on expected loss $= \text{exposure} \times (1 - RR) \times POD$.
> X: $106.00 \times 0.60 = 63.6000$, expected loss $= 63.6000 \times 0.0120 = 0.7632$.
> Y: $99.00 \times 0.70 = 69.3000$, expected loss $= 69.3000 \times 0.0105 = 0.7277$.
> Z: $94.00 \times 0.80 = 75.2000$, expected loss $= 75.2000 \times 0.0100 = 0.7520$.
> Ranking by expected loss: X (0.7632), Z (0.7520), Y (0.7277).
> B is wrong because it ranks on the probability of default alone (1.20%, 1.05%, 1.00%), which measures default risk, not credit risk.
> C is wrong because it ranks on loss given default alone (75.20, 69.30, 63.60) and ignores the probability of default.
> The agency ratings order the issuers by default probability, so reading them off reproduces the ranking in B; credit risk needs the loss given default as well.
> 2. **A.** Build the CVA table with conditional PODs: $POD_1 = 1.80\%$; $POD_2 = 1.80\% \times 98.2000\% = 1.7676\%$; $POD_3 = 1.80\% \times 96.4324\% = 1.7358\%$.
> LGD $= 0.55 \times$ exposure: 61.0794, 59.5012, 57.8875.
> Expected losses: $61.0794 \times 0.018000 = 1.0994$; $59.5012 \times 0.017676 = 1.0517$; $57.8875 \times 0.017358 = 1.0048$.
> PV of expected losses: $1.0994 \times 0.977995 = 1.0752$; $1.0517 \times 0.956474 = 1.0060$; $1.0048 \times 0.935427 = 0.9399$.
> $CVA = 1.0752 + 1.0060 + 0.9399 = 3.0211$.
> $VND = 5.25 \times (0.977995 + 0.956474) + 105.25 \times 0.935427 = 108.6097$.
> Fair value $= 108.6097 - 3.0211 = 105.5886$, which exceeds the 105.50 market price by about 0.09, so the bond is slightly undervalued under Adeyemi's assumptions.
> B is wrong because it deducts the undiscounted expected losses ($1.0994 + 1.0517 + 1.0048 = 3.1560$), giving $108.6097 - 3.1560 = 105.4537$, which is below the price and flips the conclusion.
> C is wrong because it reports the value assuming no default and ignores the CVA; the direction happens to match, but the mispricing is overstated by a factor of about 35.
> 3. **B.** If default occurs on Date 2, the fund receives the Date 1 coupon of 5.25 and then the recovery on Date 2, which is 45% of the Date 2 exposure: $108.1840 \times 0.45 = 48.6828$.
> Solve $105.50 = \dfrac{5.25}{1+r} + \dfrac{48.6828}{(1+r)^2}$ for $r = -29.54\%$.
> Calculator: CF0 $= -105.50$, C01 $= 5.25$, C02 $= 48.6828$, IRR CPT gives $-29.54$.
> A is wrong because it uses the loss given default (59.5012) as the Date 2 cash flow instead of the recovery, giving $-22.37\%$.
> C is wrong because it applies the 45% recovery rate to par (45.00) instead of to the exposure, ignoring that the exposure includes the Date 2 coupon and the bond's value above par, giving $-32.15\%$.
> For comparison, with no default the return is the yield to maturity at 105.50, 3.29%, so the dispersion across default dates is the default timing risk that inflates risk-neutral PODs above the 0.90% historical rate.
> 4. **B.** A high-yield issuer at the trough of a cyclical industry can show an inverted spread curve because investors expect its credit quality to improve as the cycle turns, so the market prices a higher hazard in the near term than in later years.
> The absence of near-term maturities and prices far above recovery value rule out the distressed explanation.
> A is wrong because the optical inversion applies when default is expected to be near certain and every bond trades at the recovery price; Draxton's bonds trade at 88 to 92, not at recovery.
> C is wrong because longer maturities do not carry less credit risk as a rule; high-quality curves such as Helmsley's are flat to upward sloping because spreads sit near their lower bound and migration can mostly widen them, and an inversion reflects issuer-specific expectations, not maturity itself.

## Distractor design

1. B: ranking on POD alone (default risk mistaken for credit risk); C: ranking on LGD alone (probability of default ignored).
2. B: undiscounted expected losses deducted as the CVA (discounting step skipped, conclusion flipped); C: VND reported as fair value (CVA ignored).
3. A: LGD used as the Date 2 cash flow instead of the recovery; C: recovery rate applied to par instead of the exposure.
4. A: distressed optical-inversion case applied to an issuer not trading at recovery; C: inversion attributed to maturity itself rather than to expected improvement in credit quality.
