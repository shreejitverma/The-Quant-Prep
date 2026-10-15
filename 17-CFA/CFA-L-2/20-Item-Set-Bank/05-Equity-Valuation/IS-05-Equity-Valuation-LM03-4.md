---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 3
title: "Pinecrest Hospitality: Reviewing a Valuation File"
los: [los-05-03-c, los-05-03-e, los-05-03-f, los-05-03-h]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Pinecrest Hospitality: Reviewing a Valuation File

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Lucas Ferreira, CFA, is the model-review officer at the Tidewater Public Employees' Pension Fund.
Fund policy requires him to check every valuation file before the investment committee relies on it.
He is reviewing a file on Pinecrest Hospitality Inc., a US restaurant franchisor that reports under US GAAP, prepared by junior analyst Hannah Brooks.
All figures are in USD millions, and Pinecrest's tax rate is 24%.

In 2025 Pinecrest recorded three special items within operating income.
It wrote down goodwill from an earlier acquisition, reversed part of a restructuring provision recognized in 2023, and sold 12 company-owned restaurant sites to franchisees at a gain.
Income tax expense includes a deferred tax charge of 9 arising from temporary differences that Pinecrest expects to reverse within two years.

Exhibit 1: Pinecrest income statement, 2025 (USD millions)

| Item | 2025 |
|---|---|
| Sales (2024: 1,800) | 2,000 |
| Operating income before special items | 410 |
| Goodwill impairment | (40) |
| Reversal of restructuring provision | 12 |
| Gain on sale of restaurant sites | 18 |
| EBIT | 400 |
| Interest expense | 40 |
| Income before tax | 360 |
| Income tax expense (includes deferred tax of 9) | 86.4 |
| Net income | 273.6 |

Exhibit 2: Pinecrest cash flow items, 2025 (USD millions)

| Item | 2025 |
|---|---|
| Depreciation | 90 |
| Capital expenditures | 150 |
| Proceeds from sale of restaurant sites | 50 |
| Working capital investment (excluding cash and debt) | 16 |
| Net repayment of long-term debt | 40 |
| Dividends paid | 110 |
| Increase in cash and equivalents | 107.6 |

Brooks forecasts 2026 FCFF with the sales-based method.
She estimates the incremental fixed capital investment rate as 2025 capital expenditures minus depreciation per dollar of the 2025 increase in sales, treating the sale of the restaurant sites as non-recurring and excluding its proceeds from that rate.
She estimates the incremental working capital investment rate as 2025 working capital investment per dollar of the same increase in sales, and applies both rates to the 2026 sales increase.
She forecasts 2026 sales growth of 8% and a normalized EBIT margin of 21%, and the tax rate stays at 24%.

Brooks's file contains two statements about 2026.

Statement 1: "Pinecrest's board has declared a special dividend of USD 150 million payable in 2026, which will reduce 2026 FCFE by USD 150 million."

Statement 2: "Pinecrest plans to draw a USD 200 million term loan on 2 January 2026. The loan leaves 2026 FCFF unchanged and raises 2026 FCFE by less than USD 200 million, because after-tax interest on the loan reduces FCFE in the same year."

As a cross-check on her FCFE model, Brooks also valued Pinecrest's equity by dividing 2025 EBITDA of USD 490 million by the 4.5% yield on ten-year Treasury notes.
Her note says the cross-check "confirms that the stock is cheap".
Ferreira drafts a comment on the cross-check for the committee.

## Questions

1. Pinecrest's 2025 FCFE is closest to: (LOS: los-05-03-c)
   - A. USD 217.6 million.
   - B. USD 226.6 million.
   - C. USD 277.6 million.
2. Using Brooks's sales-based method, Pinecrest's forecast 2026 FCFF is closest to: (LOS: los-05-03-e)
   - A. USD 211.94 million.
   - B. USD 283.94 million.
   - C. USD 392.80 million.
3. Which of Brooks's statements is (are) correct? (LOS: los-05-03-f)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.
4. Ferreira's most appropriate comment on the EBITDA cross-check is that it: (LOS: los-05-03-h)
   - A. is acceptable once EBITDA is reduced by the depreciation tax shield.
   - B. overstates equity value, because EBITDA is a pre-tax flow before reinvestment that belongs to all capital providers, and the Treasury yield is a riskless rate.
   - C. understates equity value, because EBITDA excludes the depreciation tax shield that adds to cash flow.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Net noncash charges: depreciation and the impairment are added back; the gain and the restructuring reversal raised income without cash and are subtracted; the deferred tax is expected to reverse soon, so it is not added back.
> $NCC = 90 + 40 - 18 - 12 = 100$.
> FCInv is capital expenditures net of sale proceeds: $150 - 50 = 100$; net borrowing $= -40$.
> $FCFE = NI + NCC - FCInv - WCInv + \text{Net borrowing} = 273.6 + 100 - 100 - 16 - 40 = 217.6$.
> Check from uses: $\Delta \text{Cash} + \text{Dividends} = 107.6 + 110 = 217.6$.
> B is wrong because it adds back the deferred tax charge of 9 even though the differences reverse within two years: $217.6 + 9 = 226.6$.
> C is wrong because it adds back the gain and the reversal instead of subtracting them: $273.6 + (90 + 40 + 18 + 12) - 100 - 16 - 40 = 277.6$.
> 2. **B.** Incremental fixed capital rate $= (\text{Capex} - \text{Dep})/\Delta \text{Sales} = (150 - 90)/200 = 30\%$; incremental working capital rate $= 16/200 = 8\%$.
> 2026 sales $= 2{,}000(1.08) = 2{,}160$, an increase of 160; EBIT $= 0.21(2{,}160) = 453.6$; $EBIT(1-t) = 453.6(0.76) = 344.736$.
> $FCFF = 344.736 - (0.30 + 0.08)(160) = 344.736 - 60.8 = 283.936$.
> A is wrong because it uses gross capital expenditures in the fixed capital rate ($150/200 = 75\%$): $344.736 - (0.75 + 0.08)(160) = 211.936$.
> C is wrong because it deducts the investments from pre-tax EBIT: $453.6 - 60.8 = 392.8$.
> 3. **B.** Statement 1 is incorrect: dividends are a use of FCFE, not a determinant, so the special dividend changes how FCFE is spent, not how much is generated.
> Statement 2 is correct: borrowing is a financing flow that leaves FCFF unchanged, adds 200 to FCFE through net borrowing, and, because the loan is drawn at the start of the year, 2026 after-tax interest on it reduces 2026 FCFE.
> A is wrong because it accepts the dividend claim and rejects the leverage effect, the reverse of the correct analysis.
> C is wrong because it treats the special dividend as reducing free cash flow.
> 4. **B.** EBITDA ignores taxes, ignores the fixed and working capital investment a growing franchisor needs, and is a flow to all capital providers, so it ignores interest and debt flows owed before equity; dividing it by a riskless Treasury yield also treats a risky stream as risk-free and as a level perpetuity.
> Every one of these errors pushes the estimate up, so the cross-check overstates equity value and cannot confirm that the stock is cheap.
> A is wrong because adjusting for the depreciation tax shield alone leaves the taxes, reinvestment, capital structure and discount rate errors in place; in the FCFF identity from EBITDA the tax shield is added, not deducted.
> C is wrong because the omitted tax shield is small relative to the omitted taxes and investment, so the net bias is upward.

## Distractor design

1. B: deferred tax added back despite expected reversal (noncash item treatment); C: gain and reversal added instead of subtracted (sign).
2. A: gross capex used instead of capex net of depreciation (wrong formula variant); C: investments deducted from pre-tax EBIT (before-tax vs after-tax).
3. A: dividends treated as a determinant and leverage effect denied (use vs determinant, financing effect ignored); C: dividends treated as a determinant (use vs determinant).
4. A: one partial fix treated as sufficient, with the sign of the tax-shield adjustment reversed (sign); C: minor omission taken as the net bias (direction of error).
