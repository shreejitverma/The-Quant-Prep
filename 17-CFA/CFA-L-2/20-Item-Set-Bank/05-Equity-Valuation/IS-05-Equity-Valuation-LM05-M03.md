---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 5
title: "Kaiapoi Aggregates: Valuing a Quarry With a Closing Date"
los: [los-05-05-a, los-05-05-c, los-05-05-j]
difficulty: 3
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Kaiapoi Aggregates: Valuing a Quarry With a Closing Date

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Hemi Parata, CFA, is an analyst at Rangiora Value Fund, a New Zealand fund that buys listed companies trading below their estimated intrinsic value.
He is reviewing Kaiapoi Aggregates Ltd, which operates a single gravel and sand quarry near Christchurch.
Kaiapoi's resource consent to extract gravel expires in four years and will not be renewed.
The board has announced that at the end of Year 4 Kaiapoi will redeem its preferred shares at par, settle its remaining liabilities, and distribute all remaining common equity to ordinary shareholders before the company is wound up.

Parata first checks whether Kaiapoi earned its cost of common equity in the fiscal year just ended, using the data in Exhibit 1.

Exhibit 1: Kaiapoi, fiscal year just ended (NZD millions unless stated)

| Item | Value |
|---|---|
| Total assets, beginning of year | 960 |
| Interest-bearing debt, beginning of year | 300 |
| 7% perpetual preferred shares at par, beginning of year | 100 |
| Common shareholders' equity, beginning of year | 380 |
| EBIT | 150 |
| Pretax cost of debt | 6.5% |
| Tax rate | 28% |
| Cost of common equity | 11.0% |
| Common shares outstanding (millions) | 40 |
| Share price (NZD) | 12.40 |

The difference between total assets and the sum of debt, preferred shares and common equity consists of trade payables and a provision for quarry rehabilitation.
Preferred dividends are not tax deductible and were paid in full during the year.

Parata then values Kaiapoi's common shares.
Current book value is NZD 10.00 per common share.
He uses the 11.0% cost of common equity for every year and assumes that the clean surplus relation holds.
His forecasts are shown in Exhibit 2.

Exhibit 2: Parata's forecasts per common share (NZD)

| Year | EPS | DPS |
|---|---|---|
| 1 | 2.40 | 1.00 |
| 2 | 2.60 | 1.20 |
| 3 | 2.30 | 1.30 |
| 4 | 1.80 | 15.60 |

EPS is stated after preferred dividends.
The Year 4 dividend is the final distribution and includes the return of all remaining common equity, so book value per common share is zero at the end of Year 4.

Parata's colleague Grace Whitaker, CFA, reviews the draft valuation.
The discussion produces three statements.

Statement 1 (Whitaker): "A residual income model is a poor choice for Kaiapoi, because most of its value will come from a terminal value that is difficult to estimate."

Statement 2 (Whitaker): "Because Kaiapoi will distribute all of its remaining book value in Year 4, a dividend discount model using your forecasts will give a higher value than your residual income model."

Statement 3 (Parata): "A weakness of the residual income model for Kaiapoi is that it relies on accounting earnings, and Kaiapoi's reported earnings depend heavily on management's estimate of the quarry rehabilitation provision."

## Questions

1. Kaiapoi's residual income to common shareholders for the fiscal year just ended is closest to: (LOS: los-05-05-a)
   - A. NZD 34.16 million.
   - B. NZD 45.16 million.
   - C. NZD 52.16 million.
2. Kaiapoi's forecast residual income per common share for Year 3 is closest to: (LOS: los-05-05-c)
   - A. NZD 0.892.
   - B. NZD 1.046.
   - C. NZD 1.200.
3. Parata's residual income estimate of Kaiapoi's intrinsic value per common share is closest to: (LOS: los-05-05-c)
   - A. NZD 12.92.
   - B. NZD 13.10.
   - C. NZD 14.79.
4. Which of the three statements about using a residual income model for Kaiapoi is correct? (LOS: los-05-05-j)
   - A. Statement 1.
   - B. Statement 2.
   - C. Statement 3.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Interest expense $= 0.065 \times 300 = 19.50$, so pretax income $= 150 - 19.50 = 130.50$ and net income $= 130.50 \times (1 - 0.28) = 93.96$.
> Net income available to common shareholders $= 93.96 - 0.07 \times 100 = 93.96 - 7.00 = 86.96$.
> Equity charge $= 0.11 \times 380 = 41.80$, so $RI = 86.96 - 41.80 = 45.16$.
> Check with the capital charge approach: $NOPAT = 150 \times 0.72 = 108.00$; capital charge $= 41.80 + 0.065 \times 0.72 \times 300 + 7.00 = 41.80 + 14.04 + 7.00 = 62.84$; $RI = 108.00 - 62.84 = 45.16$.
> Kaiapoi earned a return on common equity of $86.96/380 = 22.88\%$ against an 11.0% cost, so it created value for common shareholders.
> A is wrong because it charges the cost of common equity on preferred as well as common equity after already deducting the preferred dividend: $86.96 - 0.11 \times 480 = 34.16$.
> C is wrong because it omits the preferred dividend from the income available to common shareholders: $93.96 - 41.80 = 52.16$.
> Charging the cost of equity against total assets, the decoy in Exhibit 1, would give $86.96 - 0.11 \times 960 = -18.64$.
> 2. **A.** Book value roll-forward with $B_t = B_{t-1} + E_t - D_t$: $B_1 = 10.00 + 2.40 - 1.00 = 11.40$; $B_2 = 11.40 + 2.60 - 1.20 = 12.80$.
> $RI_3 = E_3 - rB_2 = 2.30 - 0.11 \times 12.80 = 2.30 - 1.408 = 0.892$.
> B is wrong because it rolls book value forward only one year and charges the cost of equity on $B_1$: $2.30 - 0.11 \times 11.40 = 1.046$.
> C is wrong because it charges the cost of equity on current book value, ignoring retention: $2.30 - 0.11 \times 10.00 = 1.200$.
> Charging the cost of equity on ending Year 3 book value of 13.80 would give 0.782.
> 3. **B.** $B_3 = 12.80 + 2.30 - 1.30 = 13.80$ and $B_4 = 13.80 + 1.80 - 15.60 = 0.00$.
> Residual income: $RI_1 = 2.40 - 1.10 = 1.300$; $RI_2 = 2.60 - 1.254 = 1.346$; $RI_3 = 0.892$; $RI_4 = 1.80 - 0.11 \times 13.80 = 1.80 - 1.518 = 0.282$.
> Present values at 11%: $1.1712 + 1.0924 + 0.6522 + 0.1858 = 3.1016$.
> Because the company is wound up, there is no continuing residual income after Year 4, so $V_0 = 10.00 + 3.1016 = 13.1016$.
> DDM check: $1.00/1.11 + 1.20/1.11^2 + 1.30/1.11^3 + 15.60/1.11^4 = 0.9009 + 0.9739 + 0.9505 + 10.2762 = 13.1016$, identical because clean surplus holds.
> The value is above the NZD 12.40 price, so on Parata's forecasts the shares are modestly undervalued.
> A is wrong because it drops Year 4 residual income on the grounds that ending book value is zero; the equity charge uses beginning book value of 13.80, so $RI_4$ is still 0.282: $10.00 + 1.1712 + 1.0924 + 0.6522 = 12.9158$.
> C is wrong because it treats Year 4 residual income as a perpetuity ($\omega = 1$), which is impossible for a company that will be wound up: $10.00 + 2.9158 + 0.282/(0.11 \times 1.11^3) = 10.00 + 2.9158 + 1.8745 = 14.7903$.
> 4. **C.** Statement 3 is correct: residual income models rely on accounting data that management can influence, and a large estimated provision shifts earnings between periods, so the inputs may need adjustment.
> Statement 1 is wrong because residual income models recognize value early: current book value alone is $10.00/13.1016 = 76.3\%$ of Parata's value, and there is no terminal value because the company is wound up.
> Statement 2 is wrong because with consistent forecasts and clean surplus accounting the DDM and residual income model give the same value, 13.1016 in Question 3; the timing of recognition differs, not the total, since the final distribution alone is $10.2762/13.1016 = 78.4\%$ of the DDM value.
> A and B are wrong for these reasons.

## Distractor design

1. A: cost of equity charged on preferred plus common equity (wrong capital base); C: preferred dividend not deducted from income available to common (wrong income measure).
2. B: equity charge on book value rolled forward one year too few (period error); C: equity charge on current book value, retention ignored.
3. A: final-year residual income dropped because ending book value is zero (beginning versus ending book confusion); C: Year 4 residual income capitalized as a perpetuity for a company that will be wound up (wrong continuing-RI case).
4. A: value recognition reversed, terminal value dependence attributed to the RI model; B: DDM and RI assumed to diverge under consistent clean surplus forecasts.
