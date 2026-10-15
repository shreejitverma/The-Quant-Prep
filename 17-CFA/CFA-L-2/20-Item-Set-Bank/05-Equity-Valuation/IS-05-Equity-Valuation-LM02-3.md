---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 2
title: "Halcyon Mutual: Growth Value in a Consumer Equity Sleeve"
los: [los-05-02-g, los-05-02-h, los-05-02-p]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Halcyon Mutual: Growth Value in a Consumer Equity Sleeve

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Priya Natarajan, CFA, is an equity analyst at Halcyon Mutual Insurance, a US property and casualty insurer that runs a consumer equity sleeve inside its general account.
On 30 June 2026 she is preparing the quarterly report on the sleeve's three largest holdings for Halcyon's investment committee.
The committee chair, Graham Holt, has asked her to show how much of each holding's price reflects growth opportunities rather than assets in place, and whether the growth assumptions in her models are sustainable.

Exhibit 1: Consumer holdings as of 30 June 2026

| | Marlowe Beverages | Tessaly Cosmetics | Orwin Snacks |
|---|---|---|---|
| Share price | USD 72.00 | USD 41.00 | USD 33.00 |
| Trailing EPS ($E_0$) | USD 4.38 | USD 1.97 | USD 1.22 |
| Forecast EPS ($E_1$) | USD 4.60 | USD 2.10 | USD 1.30 |
| Required return | 8.5% | 9.5% | 7.5% |
| Most recent payout ratio | 62% | 35% | 35% |
| Expected long-run payout ratio | 55% | 40% | n/a |
| Long-run dividend growth rate | 5.0% | 6.5% | n/a |

Natarajan values Marlowe and Tessaly with the Gordon growth model, using the expected long-run payout ratios, and values Orwin with a multistage model because of its current growth rate.
She assumes the market prices in Exhibit 1 equal intrinsic value when she computes the present value of growth opportunities.

Holt asks her to explain Orwin's growth using a DuPont decomposition of its latest fiscal year.

Exhibit 2: Orwin Snacks, fiscal year 2025 (USD millions)

| Item | Amount |
|---|---|
| Net income | 260 |
| Sales | 3,250 |
| Average total assets | 2,600 |
| Shareholders' equity, beginning of year | 1,625 |
| Shareholders' equity, end of year | 1,794 |
| Dividends declared | 91 |

Orwin issued and repurchased no shares during the year, and its leverage has been constant for five years.

Holt is also concerned about Marlowe.
He notes that Marlowe's ROE of 24% has been achieved with an equity multiplier of 3.2, far above the industry, after a debt-funded buyback program.
He asks Natarajan to estimate Marlowe's mature sustainable growth rate by replacing Marlowe's own ratios with industry benchmark components and using its expected long-run payout ratio.

Exhibit 3: Marlowe Beverages DuPont components

| Component | Marlowe, 2025 | Industry benchmark |
|---|---|---|
| Net profit margin | 6.0% | 7.5% |
| Total asset turnover | 1.25 | 0.95 |
| Equity multiplier | 3.20 | 1.60 |

Natarajan's draft report states that Marlowe "trades roughly in line with its justified leading multiple" and that Tessaly "trades at a premium to its justified trailing multiple that the Gordon model cannot explain."

## Questions

1. Based on Exhibit 1, the holding with the largest present value of growth opportunities per share is: (LOS: los-05-02-g)
   - A. Marlowe Beverages.
   - B. Tessaly Cosmetics.
   - C. Orwin Snacks.
2. The component of Orwin's leading P/E attributable to its present value of growth opportunities is closest to: (LOS: los-05-02-g)
   - A. 12.05.
   - B. 13.33.
   - C. 25.38.
3. Marlowe's justified leading P/E based on the Gordon growth model is closest to: (LOS: los-05-02-h)
   - A. 15.71.
   - B. 16.50.
   - C. 17.71.
4. Tessaly's justified trailing P/E, and the conclusion it supports, are closest to: (LOS: los-05-02-h)
   - A. 13.33; overvalued.
   - B. 14.20; overvalued.
   - C. 14.20; undervalued.
5. Using Exhibit 2, Orwin's sustainable growth rate is closest to: (LOS: los-05-02-p)
   - A. 5.60%.
   - B. 9.42%.
   - C. 10.40%.
6. Using the approach Holt requests, Marlowe's mature sustainable growth rate is closest to: (LOS: los-05-02-p)
   - A. 5.13%.
   - B. 6.27%.
   - C. 10.80%.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** PVGO $= P_0 - E_1/r$.
> Marlowe: $72.00 - 4.60/0.085 = 72.00 - 54.1176 = 17.8824$.
> Tessaly: $41.00 - 2.10/0.095 = 41.00 - 22.1053 = 18.8947$.
> Orwin: $33.00 - 1.30/0.075 = 33.00 - 17.3333 = 15.6667$.
> Tessaly's PVGO of USD 18.89 is the largest in currency terms.
> A is wrong because Marlowe has the highest price and the highest no-growth value, not the highest PVGO.
> C is wrong because Orwin has the largest PVGO relative to earnings (Question 2), which is a different ranking from PVGO in dollars.
> 2. **A.** $P_0/E_1 = 1/r + \text{PVGO}/E_1$; for Orwin the growth component is $15.6667/1.30 = 12.0513$, or 12.05.
> Check: $1/0.075 = 13.3333$ and $13.3333 + 12.0513 = 25.3846 = 33.00/1.30$.
> B is wrong because 13.33 is the no-growth component $1/r$, not the growth component.
> C is wrong because 25.38 is the whole leading P/E.
> Orwin's growth component (12.05) exceeds Tessaly's ($18.8947/2.10 = 9.00$) and Marlowe's ($17.8824/4.60 = 3.89$), so the two rankings differ.
> 3. **A.** Justified leading P/E $= (1 - b)/(r - g) = 0.55/(0.085 - 0.050) = 0.55/0.035 = 15.71$, using the expected long-run payout.
> The actual leading P/E is $72.00/4.60 = 15.65$, which supports the draft's statement that Marlowe trades roughly in line.
> B is wrong because it is the trailing form, $0.55 \times 1.05/0.035 = 16.50$.
> C is wrong because it uses the most recent 62% payout, $0.62/0.035 = 17.71$, rather than the forward policy.
> 4. **B.** Justified trailing P/E $= (1 - b)(1 + g)/(r - g) = 0.40 \times 1.065/(0.095 - 0.065) = 0.4260/0.03 = 14.20$.
> The actual trailing P/E is $41.00/1.97 = 20.81$, well above 14.20, so the shares are overvalued on the Gordon model; equivalently the Gordon value is $0.40 \times 2.10/0.03 = 28.00 < 41.00$.
> A is wrong because 13.33 is the leading formula, $0.40/0.03$, reported as the trailing multiple.
> C is wrong because it reverses the direction: an actual multiple above the justified multiple means overvalued.
> 5. **C.** PRAT: retention $= (260 - 91)/260 = 0.65$; margin $= 260/3{,}250 = 0.08$; turnover $= 3{,}250/2{,}600 = 1.25$; leverage $= 2{,}600/1{,}625 = 1.60$.
> $g = 0.65 \times 0.08 \times 1.25 \times 1.60 = 0.104$, or 10.40%; shortcut: retained earnings over beginning equity, $169/1{,}625 = 10.40\%$.
> Orwin's 10.40% exceeds its 7.5% required return, so it cannot be a perpetual Gordon input, which is why Natarajan uses a multistage model.
> A is wrong because it multiplies ROE (16%) by the payout ratio, $0.35 \times 16\% = 5.60\%$.
> B is wrong because it uses ending equity, $169/1{,}794 = 9.42\%$; the sustainable growth identity holds with beginning equity.
> 6. **A.** Mature ROE $= 0.075 \times 0.95 \times 1.60 = 0.1140$; retention $= 1 - 0.55 = 0.45$; $g = 0.45 \times 11.40\% = 5.13\%$.
> This supports Natarajan's 5.0% Gordon growth rate once the leverage-driven ROE is normalized.
> B is wrong because it multiplies the benchmark ROE by the payout ratio, $0.55 \times 11.40\% = 6.27\%$.
> C is wrong because it keeps Marlowe's leverage-inflated 24% ROE, $0.45 \times 24\% = 10.80\%$.

## Distractor design

1. A: highest no-growth value confused with highest PVGO; C: PVGO/$E_1$ ranking substituted for the dollar ranking.
2. B: no-growth P/E component reported; C: total leading P/E reported.
3. B: trailing formula used when leading is asked; C: most recent payout used instead of expected payout.
4. A: leading formula used when trailing is asked; C: direction of the justified versus actual comparison reversed.
5. A: payout used instead of retention; B: ending equity used instead of beginning equity.
6. B: payout used instead of retention; C: historical leverage-inflated ROE not normalized.
