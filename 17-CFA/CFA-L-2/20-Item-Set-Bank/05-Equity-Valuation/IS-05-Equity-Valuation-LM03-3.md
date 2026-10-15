---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 3
title: "Tamsin Logistics: Evaluating a Tender Offer"
los: [los-05-03-d, los-05-03-i, los-05-03-j, los-05-03-k, los-05-03-l]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Tamsin Logistics: Evaluating a Tender Offer

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tamsin Logistics plc is a UK contract logistics and warehousing company with 400 million common shares outstanding.
Its shares traded at GBP 18.90 before Halberd Infrastructure Partners announced an unsolicited cash offer of GBP 21.40 per share.
The independent committee of Tamsin's board has engaged Priya Chen, CFA, to advise whether the offer is adequate.

Chen values Tamsin with an FCFF model because the company has preferred shares outstanding and its leverage has varied over time.
Net income in Exhibit 1 is income available to common shareholders, after preferred dividends.
Depreciation is the only noncash charge, and the tax rate is 25%.

Exhibit 1: Tamsin financial data, 2025 (GBP millions)

| Item | 2025 |
|---|---|
| Net income available to common | 300.0 |
| Depreciation | 240.0 |
| Interest expense | 126.0 |
| Preferred dividends | 35.0 |
| Fixed capital investment | 210.0 |
| Working capital investment | 49.5 |
| Common dividends paid | 120.0 |

Exhibit 2: Tamsin capital and market data

| Item | Value |
|---|---|
| Debt, market value (book value 2,050) | GBP 2,100 million |
| Pretax cost of debt | 6.0% |
| Preferred stock, market value | GBP 500 million |
| Required return on preferred | 7.0% |
| Target weights: debt, preferred, common | 35%, 10%, 55% |
| Risk-free rate | 4.0% |
| Tamsin equity beta | 1.10 |
| Equity risk premium | 5.0% |

Chen weights the costs of capital at the target weights.
She expects Tamsin's FCFF to grow at 9% in each of years 1 and 2, as new automated warehouses come on line.
Growth then slows to 7% in year 3 and 5% in year 4 as the contracts mature, and Chen expects FCFF to grow at 3% a year from year 5 onward.

Tamsin owns two assets that do not contribute to operating cash flow.
The first is a plot of surplus land beside its Midlands hub, carried at GBP 45 million and appraised at GBP 120 million.
The second is a portfolio of marketable securities worth GBP 80 million that is not needed for operations.
Neither asset is reflected in Chen's FCFF forecast.

Chen also prepares a sensitivity analysis of value per share, changing one input at a time and holding the others at their base-case values.

Exhibit 3: Sensitivity of value per share (GBP)

| Input | Low estimate | High estimate | Value at low | Value at high |
|---|---|---|---|---|
| Long-term FCFF growth rate | 2.5% | 3.5% | 19.17 | 24.68 |
| Base-year FCFF | GBP 380 million | GBP 440 million | 19.60 | 23.64 |
| WACC | 7.0% | 8.0% | to be computed | to be computed |

At the committee meeting, director Graham Pell comments: "The detail between year 2 and maturity adds nothing. Use a two-stage model with growth dropping straight from 9% to 3% after year 2; the answer will be the same."

The committee plans to recommend rejection of the offer only if Chen's value per share exceeds the offer price.

## Questions

1. Tamsin's WACC is closest to: (LOS: los-05-03-k)
   - A. 7.33%.
   - B. 7.50%.
   - C. 8.03%.
2. Tamsin's 2025 FCFF is closest to: (LOS: los-05-03-d)
   - A. GBP 375.0 million.
   - B. GBP 410.0 million.
   - C. GBP 441.5 million.
3. The value of Tamsin's operating assets is closest to: (LOS: los-05-03-k)
   - A. GBP 10,392.1 million.
   - B. GBP 10,773.4 million.
   - C. GBP 11,046.6 million.
4. Chen's value per common share and her conclusion on the offer are closest to: (LOS: los-05-03-l)
   - A. GBP 21.12; the offer exceeds intrinsic value.
   - B. GBP 21.62; the offer is below intrinsic value.
   - C. GBP 22.87; the offer is below intrinsic value.
5. Once the WACC row of Exhibit 3 is completed, Chen should conclude that value per share is most sensitive to: (LOS: los-05-03-i)
   - A. WACC.
   - B. the long-term FCFF growth rate.
   - C. base-year FCFF.
6. Pell's comment is best evaluated as: (LOS: los-05-03-j)
   - A. correct, because a two-stage model with an abrupt drop gives the same value as a three-stage model.
   - B. incorrect, because Tamsin moves from high growth through a transition of declining growth to maturity, which a three-stage model captures.
   - C. incorrect, because a single-stage model at 3% should be used, since the terminal value dominates.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Cost of equity $= 4.0\% + 1.10(5.0\%) = 9.5\%$.
> $WACC = w_d r_d(1-t) + w_p r_p + w_e r = 0.35(6.0\%)(0.75) + 0.10(7.0\%) + 0.55(9.5\%) = 1.575\% + 0.700\% + 5.225\% = 7.50\%$.
> A is wrong because it also applies the tax factor to the preferred cost, which is not tax deductible: $1.575\% + 0.525\% + 5.225\% = 7.325\%$.
> C is wrong because it omits the tax shield on debt: $2.100\% + 0.700\% + 5.225\% = 8.025\%$.
> 2. **B.** With preferred stock, $FCFF = NI + NCC + Int(1-t) + \text{Preferred dividends} - FCInv - WCInv$.
> $FCFF = 300.0 + 240.0 + 126.0(0.75) + 35.0 - 210.0 - 49.5 = 300.0 + 240.0 + 94.5 + 35.0 - 259.5 = 410.0$.
> Common dividends are a use of free cash flow and play no part.
> A is wrong because it omits the preferred dividend add-back: $410.0 - 35.0 = 375.0$.
> C is wrong because it adds back the full interest instead of the after-tax amount: $410.0 + 126.0(0.25) = 441.5$.
> 3. **C.** FCFF path: $FCFF_1 = 410.0(1.09) = 446.9$, $FCFF_2 = 487.121$, $FCFF_3 = 487.121(1.07) = 521.2195$, $FCFF_4 = 521.2195(1.05) = 547.2804$, $FCFF_5 = 547.2804(1.03) = 563.6989$.
> PV at 7.50% of years 1 to 4 $= 415.7209 + 421.5217 + 419.5611 + 409.8039 = 1{,}666.6076$.
> $TV_4 = FCFF_5/(WACC - g) = 563.6989/(0.075 - 0.03) = 12{,}526.6413$; PV $= 12{,}526.6413/1.075^4 = 9{,}379.9556$.
> Operating asset value $= 1{,}666.6076 + 9{,}379.9556 = 11{,}046.5632$.
> A is wrong because it discounts the terminal value five periods: $1{,}666.6076 + 12{,}526.6413/1.075^5 = 10{,}392.1477$.
> B is wrong because it capitalizes $FCFF_4$ without a year of stable growth: $547.2804/0.045 = 12{,}161.7867$, giving $1{,}666.6076 + 9{,}106.7523 = 10{,}773.3599$.
> 4. **B.** Firm value adds the non-operating assets at market value: $11{,}046.5632 + 120 + 80 = 11{,}246.5632$.
> Common equity $= 11{,}246.5632 - 2{,}100 - 500 = 8{,}646.5632$; per share $= 8{,}646.5632/400 = 21.62$.
> The GBP 21.40 offer is below the GBP 21.62 intrinsic value, so on this analysis the committee would recommend rejection.
> A is wrong because it ignores the land and securities: $(11{,}046.5632 - 2{,}600)/400 = 21.12$, which reverses the recommendation.
> C is wrong because it fails to subtract preferred stock: $(11{,}246.5632 - 2{,}100)/400 = 22.87$.
> 5. **A.** At a WACC of 7.0%, the same cash flows give operating assets of 12,437.2008 and a value per share of $(12{,}437.2008 + 200 - 2{,}600)/400 = 25.09$; at 8.0%, operating assets are 9,934.1621 and value per share is 18.84.
> The WACC range is $25.09 - 18.84 = 6.26$, wider than the growth range of $24.68 - 19.17 = 5.51$ and the base-year FCFF range of $23.64 - 19.60 = 4.04$.
> WACC dominates here because it both discounts the explicit-period flows and sets the terminal-value denominator, and its band is as wide as the growth band.
> B is wrong because it relies on the rule of thumb that growth usually dominates instead of computing the WACC row.
> C is wrong because value scales with base-year FCFF, but the plausible range for that input is the narrowest in value terms.
> 6. **B.** Tamsin's growth passes through three phases: a high-growth phase at 9%, a transition in which growth declines (7%, then 5%), and a mature phase at 3%, which is the profile a three-stage model is built for.
> Replacing the transition with an abrupt drop to 3% after year 2 removes two years of above-mature growth and lowers value, so the answer is not the same.
> A is wrong for that reason.
> C is wrong because a large terminal value does not justify ignoring four years of forecast growth above the long-run rate.

## Distractor design

1. A: preferred cost tax-adjusted (before-tax vs after-tax); C: debt tax shield omitted (before-tax vs after-tax).
2. A: preferred dividend add-back omitted (wrong formula variant); C: full interest added (before-tax vs after-tax).
3. A: terminal value discounted $n + 1$ periods (period); B: terminal value built from $FCFF_n$ rather than $FCFF_{n+1}$ (period).
4. A: non-operating assets omitted (misread exhibit), which flips the decision; C: preferred stock not deducted from firm value (wrong formula variant).
5. B: rule of thumb used without computing the missing row (misread exhibit); C: proportional scaling confused with the widest range (wrong criterion).
6. A: abrupt-drop two-stage treated as equivalent to a gradual transition (wrong model variant); C: single-stage model chosen because the terminal value is large (wrong model variant).
