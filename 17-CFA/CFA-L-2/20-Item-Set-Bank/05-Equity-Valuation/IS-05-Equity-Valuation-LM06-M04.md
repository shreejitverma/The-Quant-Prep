---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 6
title: "Tarnside Hydraulic Systems: Pricing an Employee Option Grant"
los: [los-05-06-c, los-05-06-e, los-05-06-h, los-05-06-i]
difficulty: 3
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Tarnside Hydraulic Systems: Pricing an Employee Option Grant

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tarnside Hydraulic Systems Ltd. is a private Canadian manufacturer of hydraulic cylinders for forestry and snow-clearing equipment.
The company is owned by three members of the Brennock family, none of whom works in the business, and is run by a professional management team.
The board plans to grant share options to 40 senior employees and has engaged Ashcombe Valuation Partners to estimate the value of Tarnside's common equity as the basis for the exercise price.
Priya Venkataraman, CFA, leads the engagement.

Tarnside's revenue has grown at a steady 2% to 4% a year for a decade, and management expects that pattern to continue.
The statements are audited, and no normalization adjustments are required.
Management has supplied a one-year forecast, which Venkataraman plans to test against her own analysis before using it.

Venkataraman searches for guideline public companies to support a beta estimate.
The only listed hydraulics firm in Canada is Halvard Fluid Power Inc., which has a levered beta of 1.25 but is fifteen times Tarnside's size and sells mainly to the aerospace industry.
She concludes that Halvard is not a credible comparable and estimates the required return on equity with the build-up approach instead.
Because demand for snow-clearing and forestry equipment is defensive, her industry research supports an industry risk discount rather than a premium.

Exhibit 1: Required return and capital inputs for Tarnside

| Input | Value |
|---|---|
| Risk-free rate | 3.5% |
| Equity risk premium | 5.5% |
| Small-stock premium | 3.0% |
| Industry risk premium (discount) | -0.5% |
| Company-specific risk premium | 2.0% |
| Pre-tax cost of debt | 6.0% |
| Tax rate | 26% |
| Debt to total capital, actual | 15% |
| Market value of debt | CAD 16.0 million |

Because the options are a minority position and no change of control is contemplated, Venkataraman weights the cost of capital at Tarnside's actual capital structure.
She values the firm with the capitalized cash flow method using management's forecast of next year's EBIT of CAD 14.0 million and a perpetual growth rate of 3.0%.
She estimates the reinvestment needed to sustain growth from the relation implied by the method, assuming value-neutral reinvestment at the WACC.

As a cross-check, Venkataraman applies the guideline public company method using five listed North American industrial component makers that she considers broadly comparable in size and end markets.
She uses the median multiple, because one of the five was the subject of an unsolicited takeover bid at the measurement date.
Tarnside's EBITDA for the most recent year was CAD 16.8 million.

Exhibit 2: Guideline public company EV/EBITDA multiples

| Company | EV/EBITDA |
|---|---|
| Company 1 | 5.2 |
| Company 2 | 5.8 |
| Company 3 | 5.5 |
| Company 4 (takeover bid) | 11.6 |
| Company 5 | 6.0 |

Her junior colleague, Evan Tsui, asks why she intends to test management's forecast so carefully.
"The managers are the people who know the business best," Tsui says, "and the audit gives us comfort on the numbers."

## Questions

1. Venkataraman's estimate of Tarnside's required return on equity is closest to: (LOS: los-05-06-e)
   - A. 13.50%.
   - B. 14.50%.
   - C. 14.88%.
2. Using Venkataraman's approach, Tarnside's equity value based on the capitalized cash flow method is closest to: (LOS: los-05-06-h)
   - A. CAD 69.33 million.
   - B. CAD 85.33 million.
   - C. CAD 97.34 million.
3. The most appropriate response to Tsui is that management's forecast for this engagement is most likely to be biased: (LOS: los-05-06-c)
   - A. upward, because managers generally prefer a higher value for the business they run.
   - B. downward, because the managers receiving options benefit from a lower exercise price.
   - C. in neither direction, because the audit confirms the reliability of the forecast.
4. Tarnside's equity value based on Venkataraman's guideline public company cross-check is closest to: (LOS: los-05-06-i)
   - A. CAD 81.44 million.
   - B. CAD 97.44 million.
   - C. CAD 98.58 million.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The build-up approach adds the full equity risk premium without any beta, plus the size, industry, and company-specific adjustments.
> $r_e = 3.5\% + 5.5\% + 3.0\% + (-0.5\%) + 2.0\% = 13.50\%$.
> B is wrong because it treats the industry discount as a premium ($3.5 + 5.5 + 3.0 + 0.5 + 2.0 = 14.50\%$).
> C is wrong because it scales the equity risk premium by Halvard's beta, which Venkataraman rejected as non-comparable ($3.5 + 1.25 \times 5.5 + 3.0 - 0.5 + 2.0 = 14.875\%$).
> 2. **A.** After-tax cost of debt $= 6.0\% \times (1 - 0.26) = 4.44\%$.
> $WACC = 0.15 \times 4.44\% + 0.85 \times 13.50\% = 0.666\% + 11.475\% = 12.141\%$.
> Reinvestment rate $= g / WACC = 3.0 / 12.141 = 0.2471$.
> $FCFF_1 = EBIT_1(1 - t)(1 - RIR) = 14.0 \times 0.74 \times (1 - 0.2471) = 10.3600 \times 0.7529 = 7.8001$ million.
> Firm value $= 7.8001 / (0.12141 - 0.03) = 7.8001 / 0.09141 = 85.3307$ million.
> Equity value $= 85.3307 - 16.0 = 69.3307$, or about CAD 69.33 million.
> B is wrong because it reports firm value and does not subtract the market value of debt.
> C is wrong because it capitalizes after-tax EBIT without deducting the reinvestment needed for growth ($10.36 / 0.09141 - 16.0 = 97.3355$), which overstates free cash flow.
> 3. **B.** Management forecasts in private company valuations can be biased in a direction that depends on the purpose of the valuation.
> For incentive option grants, a lower equity value lowers the exercise price and raises the payoff to the managers receiving the options, so their forecasts tend to understate value.
> A is wrong because upward bias is the concern in settings such as goodwill impairment testing, where a higher value avoids a write-down.
> C is wrong because an audit gives assurance on historical statements, not on forecasts, and does not remove the managers' incentive.
> 4. **A.** The median of the five multiples is 5.8.
> $EV = 5.8 \times 16.8 = 97.44$ million; equity value $= 97.44 - 16.0 = 81.44$ million.
> B is wrong because it stops at enterprise value and does not subtract debt.
> C is wrong because it uses the mean multiple, which the takeover-inflated outlier distorts ($34.1 / 5 = 6.82$; $6.82 \times 16.8 - 16.0 = 98.576$).

## Distractor design

1. B: sign error on an industry risk discount; C: beta applied in the build-up approach (expanded CAPM confused with build-up, decoy beta used).
2. B: firm value reported as equity value (debt not subtracted); C: reinvestment rate omitted from the EBIT form of the CCM (after-tax EBIT treated as FCFF).
3. A: bias direction taken from the impairment-testing case; C: assurance on historical statements confused with forecast reliability.
4. B: enterprise value reported as equity value; C: mean used instead of the stated median (misread exhibit, outlier not screened).
