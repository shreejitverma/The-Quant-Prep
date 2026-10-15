---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 2
title: "Vellmar Brewing: What the Share Price Already Assumes"
los: [los-05-02-f, los-05-02-g, los-05-02-m, los-05-02-p]
difficulty: 4
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Vellmar Brewing: What the Share Price Already Assumes

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Dmitri Albescu, CFA, manages the European dividend strategy at Corvina Income Partners, a Luxembourg asset manager whose funds hold minority stakes in listed consumer staples companies.
On 11 September 2026 he is reviewing Vellmar Brewing Group SE, a mature brewer with operations in Germany, Poland and the Baltic states.
Vellmar's shares trade at EUR 62.40, and the annual dividend of EUR 2.40 per share was paid last week.
Management has published a three-year dividend plan that raises the payout ratio gradually while a brewery consolidation program is completed.
Albescu treats the dividends in the plan as known and assumes that dividends grow at a constant rate forever after year 3.
Rather than impose his own terminal growth rate, he first wants to know what growth rate the market price already assumes.

Exhibit 1: Vellmar per-share data and forecasts (EUR)

| | Year 0 (actual) | Year 1 | Year 2 | Year 3 |
|---|---|---|---|---|
| Earnings per share | 3.95 | 4.20 | 4.40 | 4.60 |
| Dividend per share | 2.40 | 2.52 | 2.70 | 2.85 |

Exhibit 2: Market and benchmark data

| Input | Value |
|---|---|
| Risk-free rate | 2.5% |
| Vellmar beta | 0.90 |
| Equity risk premium | 5.0% |
| Vellmar ROE, fiscal 2025 | 12.0% |
| Vellmar equity multiplier, fiscal 2025 | 2.8 |
| Industry median ROE, mature European brewers | 7.5% |
| Management's long-run target payout ratio | 55% |
| Peer median trailing P/E | 16.0 |
| Peer median leading P/E | 15.0 |

Albescu estimates Vellmar's required return with the CAPM.
Because Vellmar's recent ROE was achieved with leverage well above the sector's, Corvina's policy is to set mature ROE equal to the industry median when analyzing growth after an explicit forecast period.
Albescu also wants to report how much of the current price reflects growth opportunities rather than the value of Vellmar's existing assets, using the market price as the estimate of value.

His colleague Sigrid Hollis, who covers the same sector, reviews his working papers on 12 September 2026.
She prefers to anchor terminal values in peer multiples and makes three statements.

Statement 1: "Because the Gordon terminal value at the end of year 3 is calculated from the year-4 dividend, it should be discounted four periods to today."

Statement 2: "Applying the peer median trailing P/E to Vellmar's year-3 EPS gives a terminal value that implies a higher perpetual dividend growth rate than the rate embedded in today's share price."

Statement 3: "Setting the terminal value with a peer multiple rather than the Gordon model removes the need to make any assumption about Vellmar's growth after year 3."

Albescu notes that whatever terminal value is used will account for most of the estimated value of a mature company such as Vellmar.

## Questions

1. The perpetual dividend growth rate after year 3 that is implied by Vellmar's current share price is closest to: (LOS: los-05-02-f)
   - A. 2.96%.
   - B. 2.68%.
   - C. 2.80%.
2. Under Corvina's policy for mature ROE, the long-run payout ratio consistent with the market-implied growth rate, and the conclusion Albescu should draw given management's target payout, are closest to: (LOS: los-05-02-p)
   - A. 35.8%; undervalued.
   - B. 64.2%; overvalued.
   - C. 64.2%; undervalued.
3. Vellmar's present value of growth opportunities per share and the component of its leading P/E attributable to growth opportunities are closest to: (LOS: los-05-02-g)
   - A. EUR 2.40 and 0.57.
   - B. EUR 5.97 and 1.42.
   - C. EUR 2.40 and 14.29.
4. Which of Hollis's statements is most accurate? (LOS: los-05-02-m)
   - A. Statement 1.
   - B. Statement 2.
   - C. Statement 3.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** CAPM: $r = 2.5\% + 0.90 \times 5.0\% = 7.0\%$.
> PV of the planned dividends: $2.52/1.07 + 2.70/1.07^2 + 2.85/1.07^3 = 2.3551 + 2.3583 + 2.3264 = 7.0399$.
> The terminal value must supply the rest of the price: $62.40 - 7.0399 = 55.3601$ today, or $55.3601 \times 1.07^3 = 55.3601 \times 1.225043 = 67.8185$ at $t = 3$.
> Solve $V_3 = D_3(1 + g)/(r - g)$ for $g$ with $D_3$ in the role of $D_0$: $g = (V_3 r - D_3)/(V_3 + D_3) = (67.8185 \times 0.07 - 2.85)/(67.8185 + 2.85) = 1.8973/70.6685 = 0.02685$, or 2.68%.
> Check: $7.0399 + 2.85 \times 1.02685/[(0.07 - 0.02685) \times 1.225043] = 62.40$.
> A is wrong because it compounds the residual forward four periods, $55.3601 \times 1.310796 = 72.5658$, which gives $g = 2.96\%$; the terminal value sits at $t = 3$.
> C is wrong because it treats $D_3$ as the next dividend, $g = r - D_3/V_3 = 0.07 - 2.85/67.8185 = 0.07 - 0.042024 = 2.80\%$; the Gordon numerator at $t = 3$ is $D_4 = D_3(1 + g)$.
> 2. **C.** With mature ROE set to the industry median of 7.5%, $g = b \times ROE$ gives retention $= 0.026848/0.075 = 0.3580$ and payout $= 1 - 0.3580 = 64.20\%$.
> The price is consistent with Vellmar paying out 64.2% of earnings in maturity, while management targets 55%.
> At the target, sustainable growth is $0.45 \times 7.5\% = 3.375\%$, above the 2.68% the market prices; because mature ROE (7.5%) exceeds $r$ (7.0%), the extra retention creates value.
> Albescu's value at 3.375% terminal growth is $7.0399 + 2.85 \times 1.03375/[(0.07 - 0.03375) \times 1.225043] = 73.38$, above the 62.40 price, so the shares are undervalued.
> A is wrong because 35.8% is the retention ratio, not the payout ratio.
> B is wrong because it reverses the direction: implied growth below sustainable growth means the market is paying for less growth than Vellmar should deliver, so the shares are undervalued, not overvalued.
> Using Vellmar's leverage-inflated 12.0% ROE instead of the median would give a payout of $1 - 0.026848/0.12 = 77.6\%$, contrary to Corvina's policy.
> 3. **A.** No-growth value $= E_1/r = 4.20/0.07 = 60.00$; PVGO $= P_0 - E_1/r = 62.40 - 60.00 = 2.40$.
> Leading P/E decomposition: $P_0/E_1 = 62.40/4.20 = 14.8571 = 1/r + \text{PVGO}/E_1 = 14.2857 + 0.5714$, so the growth component is 0.57.
> Only $2.40/62.40 = 3.8\%$ of the price reflects growth opportunities, consistent with new investment earning a mature ROE only slightly above the required return.
> B is wrong because it computes the no-growth value with trailing EPS, $62.40 - 3.95/0.07 = 62.40 - 56.4286 = 5.9714$ and $5.9714/4.20 = 1.4218$; the perpetuity of constant earnings starts with $E_1$.
> C is wrong because 14.29 is the no-growth component $1/r$, not the growth component.
> 4. **B.** A trailing multiple is applied to earnings at the terminal date: $V_3 = 16.0 \times 4.60 = 73.60$, above the market-implied $V_3$ of 67.8185 from Question 1.
> The perpetual growth consistent with 73.60 is $(73.60 \times 0.07 - 2.85)/(73.60 + 2.85) = 2.3020/76.45 = 3.01\%$, above the 2.68% implied by the price, so Statement 2 is correct.
> Even the leading multiple misapplied to $E_3$ ($15.0 \times 4.60 = 69.00$, implied $g = 2.76\%$) would exceed 2.68%, so the conclusion does not hinge on that choice.
> A is wrong because $V_3$ is the value at $t = 3$ of all dividends from year 4 onward; it is built from $D_4$ precisely because it sits at $t = 3$, so it is discounted three periods, not four.
> C is wrong because a multiple-based terminal value embeds growth and required return assumptions implicitly, since any P/E is itself a function of $r$, $g$ and payout, and it also imports any mispricing in the peer group.

## Distractor design

1. A: terminal value located at $t = 4$ instead of $t = 3$ when backing it out of price (period error); C: $D_3$ treated as the next dividend in the implied-growth identity ($D_0$ versus $D_1$).
2. A: retention ratio reported as the payout ratio; B: direction of the implied versus sustainable growth comparison reversed.
3. B: trailing EPS used in the no-growth value $E/r$; C: no-growth P/E component $1/r$ reported instead of $\text{PVGO}/E_1$.
4. A: terminal value discounted $n + 1$ periods because it is built from $D_{n+1}$; C: multiple-based terminal value wrongly treated as assumption-free.
