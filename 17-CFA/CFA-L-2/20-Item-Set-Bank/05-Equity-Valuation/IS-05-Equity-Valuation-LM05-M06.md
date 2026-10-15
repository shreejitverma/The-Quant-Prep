---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 5
title: "Coralbay Veterinary Group: Fading Returns and What the Market Expects"
los: [los-05-05-d, los-05-05-f, los-05-05-g, los-05-05-h]
difficulty: 3
minutes: 12
source: mock-06
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Coralbay Veterinary Group: Fading Returns and What the Market Expects

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Declan Moriarty, CFA, is an equity analyst at Southbank Equity Partners, a long-only Australian equity manager based in Melbourne.
He is valuing Coralbay Veterinary Group Ltd, the largest operator of corporate-owned veterinary clinics in Australia.
Coralbay has never paid a dividend.
It reinvests all of its earnings in acquiring and refurbishing independent clinics, and Moriarty expects that policy to continue.
Shares issued under the employee share plan are expected to be offset by small buybacks, so the share count is stable.

Moriarty estimates Coralbay's required return on equity with the CAPM, using a risk-free rate of 4.0%, a beta of 1.10 and an equity risk premium of 5.0%.
Coralbay's pretax cost of debt is 5.6%.
The current book value of equity is AUD 20.00 per share, and the shares trade at AUD 34.00.
Trailing earnings per share were AUD 3.30, and the median return on equity of listed Australian healthcare services companies is 11%.
Moriarty assumes that the clean surplus relation holds.

Exhibit 1: Moriarty's forecasts for Coralbay

| Year | Return on beginning book value of equity | Dividend per share (AUD) |
|---|---|---|
| 1 | 18% | 0.00 |
| 2 | 17% | 0.00 |
| 3 | 16% | 0.00 |
| 4 | 15% | 0.00 |

Moriarty expects private equity-backed clinic groups to compete away Coralbay's excess returns.
He therefore assumes that residual income is zero from Year 5 onward and that no premium over book value remains at the end of Year 4.
In his draft report he writes:

Moriarty: "Because Coralbay's return on equity falls in every year of the forecast, its residual income also falls in every year, which is consistent with my view that its excess returns will disappear after Year 4."

Head of research Mei Lin Tan, CFA, reviews the draft.
She questions Moriarty's assumption about continuing residual income and lists the characteristics in Exhibit 2.

Exhibit 2: Coralbay characteristics noted by Tan

| Characteristic | Observation |
|---|---|
| Market position | Largest clinic network in the country, about twice the size of the next competitor |
| Dividend payout | Zero since listing; all earnings reinvested |
| Industry history | Residual income of listed clinic consolidators has historically persisted for long periods |
| Operating accruals | Close to the median of listed Australian healthcare services companies |

Tan also wants to know what the market price implies.
She applies a single-stage residual income model to Coralbay, using Moriarty's required return on equity, a long-run return on equity of 13%, and the current book value per share.
She then solves for the constant growth rate in residual income that equates the model value with the current share price.

## Questions

1. Moriarty's estimate of Coralbay's intrinsic value per share is closest to: (LOS: los-05-05-f)
   - A. AUD 24.56.
   - B. AUD 25.62.
   - C. AUD 26.09.
2. Moriarty's statement in his draft report is best described as: (LOS: los-05-05-d)
   - A. correct, because residual income moves in proportion to the spread of return on equity over the required return.
   - B. incorrect, because residual income rises in every year of the forecast, since book value grows every year.
   - C. incorrect, because residual income rises in Years 2 and 3, as growth in book value more than offsets the narrowing of the return on equity spread.
3. Based on Exhibit 2, Moriarty's assumption about continuing residual income is best described as: (LOS: los-05-05-h)
   - A. too conservative, because a zero payout and strong market leadership are associated with high persistence of residual income, so a positive persistence factor would raise the value.
   - B. appropriate, because return on equity will have converged to the required return by the end of Year 4.
   - C. too optimistic, because Coralbay's operating accruals indicate that its residual income is likely to decay faster than average.
4. The long-term growth rate in residual income implied by Coralbay's share price in Tan's single-stage model is closest to: (LOS: los-05-05-g)
   - A. 1.00%.
   - B. 3.29%.
   - C. 4.50%.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** $r = 0.040 + 1.10 \times 0.050 = 0.0950$.
> With no dividends, book value grows at the full return on equity: $B_1 = 20.00 \times 1.18 = 23.6000$; $B_2 = 23.6000 \times 1.17 = 27.6120$; $B_3 = 27.6120 \times 1.16 = 32.0299$.
> Residual income is $(ROE_t - r)B_{t-1}$: $RI_1 = 0.085 \times 20.00 = 1.7000$; $RI_2 = 0.075 \times 23.6000 = 1.7700$; $RI_3 = 0.065 \times 27.6120 = 1.7948$; $RI_4 = 0.055 \times 32.0299 = 1.7616$.
> Present values at 9.5%: $1.5525 + 1.4762 + 1.3670 + 1.2254 = 5.6211$.
> Zero residual income after Year 4 and no premium over book at Year 4 mean no terminal term, so $V_0 = 20.00 + 5.6211 = 25.6211$.
> This is below the AUD 34.00 price, so on Moriarty's assumptions Coralbay is overvalued.
> A is wrong because it holds book value at AUD 20.00 in every year, as if all earnings were paid out: RI of $1.70, 1.50, 1.30, 1.10$ with present values summing to $4.5588$, so $V_0 = 24.5588$.
> C is wrong because it omits beta from the CAPM, $r = 0.040 + 0.050 = 0.0900$, which gives $V_0 = 26.0944$.
> Charging the required return on ending rather than beginning book value would give 24.3537, a further error that the options do not use.
> 2. **C.** From Question 1, residual income is $1.7000$, $1.7700$, $1.7948$ and $1.7616$, so it rises by $0.0700$ in Year 2 and $0.0248$ in Year 3 and falls by $0.0331$ in Year 4.
> Residual income is driven by two fundamentals, the return on equity spread and the book value to which it is applied, so $RI_t/RI_{t-1} = (\text{spread}_t/\text{spread}_{t-1}) \times (B_{t-1}/B_{t-2})$.
> Year 2: $(0.075/0.085) \times 1.18 = 0.8824 \times 1.18 = 1.0412$; Year 3: $(0.065/0.075) \times 1.17 = 0.8667 \times 1.17 = 1.0140$; Year 4: $(0.055/0.065) \times 1.16 = 0.8462 \times 1.16 = 0.9815$.
> With nothing paid out, book value compounds at the full return on equity, which more than offsets the one-point cut in the spread in Years 2 and 3 but not in Year 4, when the same cut removes a larger fraction of a smaller spread.
> A is wrong because it considers only the spread and ignores growth in the book value base.
> B is wrong because it considers only book value; residual income falls in Year 4 even though book value keeps growing.
> 3. **A.** Moriarty's assumption is the case in which residual income drops to zero immediately after the horizon, equivalent to a persistence factor of zero.
> Low dividend payout, strong market leadership and high historical persistence in the industry are all associated with higher persistence of residual income, and Coralbay has all three.
> A higher persistence factor always raises value: with $\omega = 0.60$ the terminal term would be $RI_4/[(1 + r - \omega)(1 + r)^3] = 1.7616/(0.495 \times 1.3129) = 2.7106$ instead of the Year 4 present value of 1.2254, giving $V_0 = 20.00 + 1.5525 + 1.4762 + 1.3670 + 2.7106 = 27.1063$.
> B is wrong because Year 4 return on equity is still 15%, well above the 9.5% required return, so convergence has not occurred; setting continuing residual income to zero is justified only when the explicit forecast has already run until return on equity reaches the required return.
> C is wrong because it misreads Exhibit 2: extreme accruals are associated with low persistence, but Coralbay's accruals are close to the median, so they give no reason to lower persistence.
> 4. **C.** Set the single-stage value equal to price: $34.00 = 20.00 + (0.13 - 0.095) \times 20.00/(0.095 - g)$.
> So $14.00 = 0.70/(0.095 - g)$, $0.095 - g = 0.0500$, and $g = 0.0450$, or 4.50%.
> Check: $20.00 + 0.70/0.050 = 34.00$, and the implied price-to-book ratio is $(0.13 - 0.045)/(0.095 - 0.045) = 1.70 = 34.00/20.00$.
> A is wrong because it uses price instead of book value in the numerator: $0.095 - 0.035 \times 34.00/14.00 = 0.095 - 0.0850 = 0.0100$.
> B is wrong because it uses a required return that omits beta, $r = 0.09$: $0.09 - 0.04 \times 20.00/14.00 = 0.09 - 0.0571 = 0.0329$.
> Dropping $B_0$ from the left-hand side, so that price replaces the premium over book, would give $0.095 - 0.70/34.00 = 0.095 - 0.0206 = 0.0744$.
> The market's 4.50% is well below the 13% that full retention at a 13% return on equity would sustain, so the price is consistent with Coralbay eventually paying out much of its earnings or earning less on new investment.

## Distractor design

1. A: book value held constant despite full retention (clean surplus roll-forward skipped); C: CAPM with beta omitted (misread rate inputs).
2. A: spread treated as the only driver of residual income; B: book value treated as the only driver.
3. B: zero continuing residual income justified by convergence that has not happened (Year 4 ROE misread); C: a neutral accruals observation read as a low-persistence marker (misread exhibit).
4. A: price used in place of book value in the numerator; B: required return without beta carried into the implied growth equation.
