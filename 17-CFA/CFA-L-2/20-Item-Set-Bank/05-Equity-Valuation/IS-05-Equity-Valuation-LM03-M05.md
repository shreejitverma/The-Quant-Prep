---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 3
title: "Ostrander Precision Castings: Paying Down the Acquisition Debt"
los: [los-05-03-a, los-05-03-c, los-05-03-d, los-05-03-l]
difficulty: 3
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Ostrander Precision Castings: Paying Down the Acquisition Debt

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Naomi Achebe, CFA, is a portfolio manager at Ridgeview Asset Management, which runs a US mid-cap value fund.
She is reviewing Ostrander Precision Castings Inc., a US producer of investment-cast turbine and pump components that reports under US GAAP.
Ostrander has 90 million shares outstanding, and the shares trade at USD 30.00.
All figures are in USD millions, and the tax rate is 25%.

In 2024 Ostrander bought a competitor with a large bridge loan, which lifted its debt to 55% of total capital at market values by the end of that year.
Management has since announced a plan to reduce debt to 35% of total capital at market values and then to hold it there, and the large 2025 repayment was the first and largest step.

Exhibit 1: Ostrander statement of cash flows, 2025 (USD millions)

| Item | 2025 |
|---|---|
| Net income | 210 |
| Depreciation and amortization | 185 |
| Increase in accounts receivable | (40) |
| Increase in inventories | (25) |
| Increase in accounts payable | 18 |
| Cash flow from operating activities | 348 |
| Capital expenditures | (260) |
| Proceeds from sale of equipment | 20 |
| Cash flow from investing activities | (240) |
| Repayment of long-term debt | (400) |
| Increase in notes payable | 50 |
| Issuance of common shares under employee plans | 30 |
| Dividends paid | (60) |
| Cash flow from financing activities | (380) |
| Net change in cash | (272) |

Interest paid of USD 120 million is included in cash flow from operating activities.
The equipment was sold at its carrying amount, so no gain or loss was recognized.
Achebe considers 2025 operating results and investment representative of the company's normal level.

Exhibit 2: Ostrander capital and market data

| Item | Value |
|---|---|
| Debt, book value | USD 1,550 million |
| Debt, market value | USD 1,480 million |
| Pretax cost of debt | 6.4% |
| Risk-free rate | 4.0% |
| Equity beta | 1.20 |
| Equity risk premium | 5.5% |
| Weights at the end of 2024: debt, equity | 55%, 45% |
| Target weights after the plan: debt, equity | 35%, 65% |

Achebe first reconstructs 2025 FCFF and FCFE from the cash flow statement.
She then discusses the choice of model with Rhys Holloway, a colleague on the fund's research team.

Holloway says: "FCFE was negative in 2025 only because Ostrander used cash to repay debt, which is a financing choice. Discounting FCFF at WACC avoids having to forecast the repayment schedule year by year, and WACC is less sensitive to the leverage change than the cost of equity is."

Achebe decides to use a single-stage FCFF model.
She expects FCFF to grow at 4.0% a year indefinitely from its 2025 level.
Because the model is a perpetuity, she weights the costs of capital at the capital structure Ostrander will hold for the long run, and she estimates the cost of equity with the CAPM.
The fund buys only shares whose estimated value exceeds the market price.

## Questions

1. Ostrander's 2025 FCFF is closest to: (LOS: los-05-03-c)
   - A. USD 151 million.
   - B. USD 198 million.
   - C. USD 228 million.
2. Ostrander's 2025 FCFE is closest to: (LOS: los-05-03-d)
   - A. USD -292 million.
   - B. USD -242 million.
   - C. USD -212 million.
3. Holloway's statement is best described as: (LOS: los-05-03-a)
   - A. correct.
   - B. incorrect, because FCFF for a levered company must be discounted at the required return on equity.
   - C. incorrect, because a company with negative FCFE should be valued with a dividend discount model rather than a free cash flow model.
4. Achebe's estimate of Ostrander's value per share and her conclusion are closest to: (LOS: los-05-03-l)
   - A. USD 28.16; the shares are overvalued.
   - B. USD 33.62; the shares are undervalued.
   - C. USD 50.65; the shares are undervalued.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** From CFO only two adjustments remain, because depreciation and working capital investment are already inside CFO.
> Under US GAAP interest paid is in CFO, so after-tax interest is added back: $120(1 - 0.25) = 90$.
> FCInv is capital expenditures net of disposal proceeds: $260 - 20 = 240$.
> $FCFF = CFO + Int(1-t) - FCInv = 348 + 90 - 240 = 198$.
> A is wrong because it deducts working capital investment a second time: $WCInv = 40 + 25 - 18 = 47$ and $198 - 47 = 151$.
> C is wrong because it adds back the full interest instead of the after-tax amount: $348 + 120 - 240 = 228$.
> 2. **B.** Net borrowing $= 50 - 400 = -350$, counting both notes payable and long-term debt.
> $FCFE = CFO - FCInv + \text{Net borrowing} = 348 - 240 - 350 = -242$.
> Check from FCFF: $198 - 90 - 350 = -242$.
> Check from uses: $FCFE = \Delta \text{Cash} + \text{Dividends} + \text{Net share repurchases} = -272 + 60 - 30 = -242$, where the share issuance is a negative repurchase.
> A is wrong because it omits the increase in notes payable from net borrowing: $348 - 240 - 400 = -292$.
> C is wrong because it treats the share issuance as a source of FCFE: $-242 + 30 = -212$; share issues are transactions with shareholders and do not change free cash flow.
> 3. **A.** FCFF is preferred for a levered company with negative FCFE or a changing capital structure.
> FCFF is before all debt flows, so its growth reflects operating fundamentals rather than a repayment schedule, and WACC is less sensitive to changes in leverage than the cost of equity.
> B is wrong because FCFF belongs to all capital providers and is discounted at WACC; only FCFE is discounted at the required return on equity.
> C is wrong because negative FCFE points to the FCFF approach, not to a dividend model, and dividends that are not linked to capacity would be a poor basis for value.
> 4. **B.** Cost of equity $= 4.0\% + 1.20(5.5\%) = 10.6\%$.
> At the target weights, $WACC = 0.35(6.4\%)(0.75) + 0.65(10.6\%) = 1.68\% + 6.89\% = 8.57\%$.
> Firm value $= 198(1.04)/(0.0857 - 0.04) = 205.92/0.0457 = 4{,}505.9081$.
> Equity $= 4{,}505.9081 - 1{,}480 = 3{,}025.9081$, using the market value of debt; per share $= 3{,}025.9081/90 = 33.62$.
> The estimate exceeds the USD 30.00 price, so the shares are undervalued and qualify for purchase.
> A is wrong because it omits the tax shield on debt: $WACC = 0.35(6.4\%) + 6.89\% = 9.13\%$, firm value $= 205.92/0.0513 = 4{,}014.0351$, and $(4{,}014.0351 - 1{,}480)/90 = 28.16$, which reverses the conclusion.
> C is wrong because it uses the end-2024 55/45 weights instead of the long-run target: $WACC = 0.55(4.8\%) + 0.45(10.6\%) = 7.41\%$, firm value $= 205.92/0.0341 = 6{,}038.7097$, and $(6{,}038.7097 - 1{,}480)/90 = 50.65$.

## Distractor design

1. A: WCInv subtracted from CFO although CFO already contains it (double count); C: full interest added back (before-tax vs after-tax).
2. A: notes payable omitted from net borrowing (missed debt layer); C: share issuance treated as a determinant of FCFE (use vs determinant).
3. B: FCFF matched with the cost of equity (cash flow and discount rate mismatched); C: negative FCFE taken as a reason to abandon free cash flow models (wrong model criterion).
4. A: debt tax shield omitted from WACC (before-tax vs after-tax), which flips the conclusion; C: end-2024 rather than target weights used in a perpetuity (misread exhibit).
