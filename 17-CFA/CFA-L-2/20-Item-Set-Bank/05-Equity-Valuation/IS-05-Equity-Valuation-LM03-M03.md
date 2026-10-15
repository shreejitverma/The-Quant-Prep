---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 3
title: "Soganli Home Textiles: A Real-Terms Valuation"
los: [los-05-03-d, los-05-03-i, los-05-03-j, los-05-03-k]
difficulty: 3
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Soganli Home Textiles: A Real-Terms Valuation

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Kerem Aydin, CFA, is an analyst at Halcyon Frontier Partners, a fund that invests in listed emerging-market consumer companies.
He is valuing Soganli Home Textiles A.S., a Turkish maker of towels, bed linen and curtains that sells through its own stores and to European retailers.
Soganli has 200 million shares outstanding, which trade at TRY 52.00.
All company figures are in TRY millions, and Soganli's tax rate is 25%.

Aydin regards 2025 as a normal year for Soganli, with no non-recurring items.
Depreciation is the company's only noncash charge.

Exhibit 1: Soganli income statement and balance sheet data, 2025 (TRY millions)

| Item | 2025 |
|---|---|
| EBITDA | 1,480 |
| Depreciation | 360 |
| Interest expense | 240 |
| Capital expenditures | 520 |
| Increase in cash and equivalents | 48 |
| Increase in accounts receivable | 95 |
| Increase in inventories | 65 |
| Increase in accounts payable | 35 |
| Increase in accrued liabilities | 15 |
| Increase in notes payable | 40 |
| Increase in long-term debt | 60 |

Turkish consumer price inflation has averaged 35% over the past three years, and forecasts for the next three years range from 18% to 45%.
The yield on two-year Turkish government bonds is 28%.
Because nominal rates are so unstable, Aydin values Soganli with a single-stage FCFE model expressed in real terms.
He treats Soganli's 2025 FCFE per share as the normalized base-year FCFE.

Aydin builds the real required return on equity from the fund's estimate of the real required return for the Turkish equity market, adjusted for Soganli's industry, size and leverage.

Exhibit 2: Real required return build-up and growth inputs

| Component | Estimate |
|---|---|
| Real required return, Turkish equity market | 6.20% |
| Industry adjustment (home textiles) | +0.90% |
| Size adjustment (Soganli is larger than the average listed company) | -0.40% |
| Leverage adjustment (Soganli is more leveraged than average) | +0.30% |
| Expected real growth, Turkish economy | 3.2% |
| Expected real growth, Soganli, relative to the economy | 0.4 percentage points lower |

The fund's investment committee asks Aydin to show how the valuation responds to the inputs he is least sure about.
He changes one input at a time between the low and the high estimates in Exhibit 3, holding every other input at its base-case value.

Exhibit 3: Low and high estimates for the sensitivity analysis

| Input | Low estimate | High estimate |
|---|---|---|
| Industry adjustment | +0.30% | +1.50% |
| Soganli real growth rate | 2.3% | 3.3% |
| Normalized FCFE per share | TRY 2.20 | TRY 2.70 |

Aydin's colleague, Deniz Arslan, reviews the model and makes two statements.

Statement 1: "With inflation this high and this volatile, real required returns and real growth rates can be estimated more reliably than nominal ones, and Soganli is a mature business whose real growth should track the Turkish economy indefinitely. A single-stage model in real terms suits it."

Statement 2: "Before applying the real growth rate, the base-year FCFE per share should first be increased by expected inflation, so that next year's cash flow is stated in the lira that will actually be received."

## Questions

1. Soganli's 2025 FCFE per share is closest to: (LOS: los-05-03-d)
   - A. TRY 2.45.
   - B. TRY 3.35.
   - C. TRY 3.80.
2. Aydin's real-terms value per share for Soganli and the resulting conclusion are closest to: (LOS: los-05-03-k)
   - A. TRY 50.37; the shares are overvalued.
   - B. TRY 59.97; the shares are undervalued.
   - C. TRY 66.54; the shares are undervalued.
3. Based on Exhibit 3, the input to which Aydin's value is most sensitive, and the width of its value range, are: (LOS: los-05-03-i)
   - A. the real growth rate; TRY 15.07.
   - B. normalized FCFE per share; TRY 12.24.
   - C. the industry adjustment; TRY 17.49.
4. Which of Arslan's statements is (are) correct? (LOS: los-05-03-j)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Working capital investment uses operating items only, so the increase in cash and the increase in notes payable are excluded: $WCInv = 95 + 65 - 35 - 15 = 110$.
> From EBITDA only the depreciation tax shield is added back: $FCFF = EBITDA(1-t) + Dep(t) - FCInv - WCInv = 1{,}480(0.75) + 360(0.25) - 520 - 110 = 1{,}110 + 90 - 630 = 570$.
> Net borrowing counts both debt layers: $40 + 60 = 100$.
> $FCFE = FCFF - Int(1-t) + \text{Net borrowing} = 570 - 240(0.75) + 100 = 570 - 180 + 100 = 490$, or TRY 2.45 per share on 200 million shares.
> Check from net income: $NI = (1{,}480 - 360 - 240)(0.75) = 660$, and $660 + 360 - 520 - 110 + 100 = 490$.
> B is wrong because it adds net borrowing to FCFF without deducting after-tax interest: $(570 + 100)/200 = 3.35$.
> C is wrong because it adds the full depreciation to EBITDA(1 - t), the EBIT template, instead of the tax shield: $FCFF = 1{,}110 + 360 - 630 = 840$ and $FCFE = (840 - 180 + 100)/200 = 3.80$.
> 2. **B.** $r_{real} = 6.20\% + 0.90\% - 0.40\% + 0.30\% = 7.00\%$; $g_{real} = 3.2\% - 0.4\% = 2.8\%$.
> $V_0 = FCFE_0(1 + g_{real})/(r_{real} - g_{real}) = 2.45(1.028)/(0.070 - 0.028) = 2.5186/0.042 = 59.9667$.
> At TRY 59.97 against a price of TRY 52.00, the shares are undervalued.
> A is wrong because it adds the size adjustment instead of subtracting it: $r_{real} = 7.80\%$ and $V_0 = 2.5186/0.050 = 50.3720$, which reverses the conclusion.
> C is wrong because it uses the economy's real growth rate instead of Soganli's: $2.45(1.032)/(0.070 - 0.032) = 2.5284/0.038 = 66.5368$.
> 3. **C.** Base case: $V_0 = 59.9667$.
> Industry adjustment: at +0.30%, $r_{real} = 6.40\%$ and $V_0 = 2.5186/0.036 = 69.9611$; at +1.50%, $r_{real} = 7.60\%$ and $V_0 = 2.5186/0.048 = 52.4708$; range $= 17.4903$.
> Real growth: at 2.3%, $V_0 = 2.45(1.023)/0.047 = 53.3266$; at 3.3%, $V_0 = 2.45(1.033)/0.037 = 68.4014$; range $= 15.0748$.
> Normalized FCFE: at 2.20, $V_0 = 2.20(1.028)/0.042 = 53.8476$; at 2.70, $V_0 = 2.70(1.028)/0.042 = 66.0857$; range $= 12.2381$.
> The industry adjustment band is 120 bp wide against 100 bp for growth, and both move the same denominator, so it produces the widest value range.
> A is wrong because it relies on the rule of thumb that growth usually dominates instead of computing each range.
> B is wrong because value scales one for one with base-year FCFE, but the plausible range of that input produces the narrowest value range.
> 4. **A.** Statement 1 is correct: a real-terms model is useful when inflation is high or volatile, because real required returns and real growth are more reliably estimated, and a single-stage model fits a mature company expected to grow with the economy.
> Statement 2 is incorrect: in a real model the cash flow, the growth rate and the discount rate must all be real; inflating FCFE by expected inflation and then discounting at a real rate mixes nominal cash flows with a real rate and overstates value.
> B is wrong because it accepts the inflation adjustment and rejects the justification for the real-terms model, the reverse of the correct analysis.
> C is wrong because it accepts Statement 2.

## Distractor design

1. B: after-tax interest not deducted in the FCFF-to-FCFE conversion (wrong formula variant); C: full depreciation added to the EBITDA route instead of the tax shield (EBIT vs EBITDA template).
2. A: size adjustment sign reversed in the build-up (sign), which flips the conclusion; C: country growth used instead of company growth (misread exhibit).
3. A: growth assumed to dominate without computing ranges (rule of thumb over calculation); B: proportional scaling confused with the widest range (wrong criterion).
4. B: nominal cash flow mixed with a real discount rate (real vs nominal), and the case for the real model rejected; C: Statement 2 accepted (real vs nominal).
