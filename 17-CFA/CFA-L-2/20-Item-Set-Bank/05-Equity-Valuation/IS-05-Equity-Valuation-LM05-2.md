---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 5
title: "Solvang Data Systems: Two Views of Continuing Residual Income"
los: [los-05-05-c, los-05-05-f, los-05-05-h, los-05-05-i]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Solvang Data Systems: Two Views of Continuing Residual Income

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Mara Lindqvist, CFA, and Oskar Brandt, CFA, are equity analysts at Nordhavn Pension Fund in Oslo.
They are valuing Solvang Data Systems ASA, a Norwegian operator of data centers that sells cloud storage and hosting capacity to Nordic companies.
Solvang is midway through a capacity expansion, and its free cash flow to equity is forecast to be negative for each of the next three years.
The company suspended its dividend in two of the last five years and expects to resume payments irregularly.
Solvang's shares trade at NOK 38.00, and its current book value per share is NOK 24.00.

The analysts estimate the required return on equity with the CAPM.
The risk-free rate is 3.0%, Solvang's beta is 1.20, and the equity risk premium is 5.5%.
Solvang's pretax cost of debt is 5.8%, and consensus long-term growth for the Nordic data center industry is 6.0%.
Both analysts use the forecasts in Exhibit 1, and both assume that the clean surplus relation holds.

Exhibit 1: Solvang forecasts (NOK per share)

| Year | EPS | DPS |
|---|---|---|
| 1 | 4.10 | 0.00 |
| 2 | 4.55 | 0.60 |
| 3 | 4.90 | 1.20 |
| 4 | 5.10 | 1.50 |

The analysts disagree about the continuing residual income after Year 4.
Lindqvist expects new entrants to compete away Solvang's excess returns.
She assumes that residual income fades after Year 4 with a persistence factor of 0.55, somewhat below the 0.62 average persistence reported in academic research.
Brandt instead estimates Solvang's share price at the end of Year 4 as 1.6 times its book value per share at that date.

Brandt reviews the company characteristics in Exhibit 2 before challenging Lindqvist's persistence factor.

Exhibit 2: Solvang characteristics noted by Brandt

| Characteristic | Observation |
|---|---|
| Accruals | Operating accruals were in the top decile of listed Nordic companies in each of the last two years |
| Special items | Large one-time gains from sale-and-leaseback transactions on two data centers |
| Dividend payout | Payout has averaged 12% of earnings over the last decade |

The analysts then compare their residual income approach with other present value models.

Lindqvist: "Because Solvang's free cash flow to equity will be negative for three years, an FCFE model would place most of Solvang's value in the terminal value, whereas the residual income model recognizes a large part of the value immediately through current book value."

Brandt: "Even if our forecasts are internally consistent and clean surplus holds, a dividend discount model would still produce a lower value than our residual income model, because the dividend discount model ignores the earnings Solvang retains."

## Questions

1. Solvang's forecast residual income for Year 3 is closest to: (LOS: los-05-05-c)
   - A. NOK 1.47.
   - B. NOK 1.82.
   - C. NOK 2.18.
2. Lindqvist's estimate of Solvang's intrinsic value per share is closest to: (LOS: los-05-05-f)
   - A. NOK 30.89.
   - B. NOK 31.84.
   - C. NOK 41.76.
3. Brandt's estimate of Solvang's intrinsic value per share is closest to: (LOS: los-05-05-f)
   - A. NOK 44.93.
   - B. NOK 46.08.
   - C. NOK 73.36.
4. Which characteristic in Exhibit 2 best supports a persistence factor higher than Lindqvist's 0.55? (LOS: los-05-05-h)
   - A. The level of operating accruals.
   - B. The one-time gains from sale-and-leaseback transactions.
   - C. The average dividend payout.
5. If Brandt valued Solvang with a dividend discount model using the Exhibit 1 dividends and his Year 4 terminal price, the proportion of that value contributed by the present value of the terminal price would be closest to: (LOS: los-05-05-c)
   - A. 35.5%.
   - B. 52.1%.
   - C. 94.7%.
6. Which of the analysts' statements comparing residual income models with other present value models is correct? (LOS: los-05-05-i)
   - A. Lindqvist's statement only.
   - B. Brandt's statement only.
   - C. Both statements.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** $r = 0.03 + 1.20 \times 0.055 = 0.0960$.
> Book value roll-forward with $B_t = B_{t-1} + E_t - D_t$: $B_1 = 24.00 + 4.10 - 0.00 = 28.10$; $B_2 = 28.10 + 4.55 - 0.60 = 32.05$; $B_3 = 32.05 + 4.90 - 1.20 = 35.75$.
> $RI_3 = E_3 - rB_2 = 4.90 - 0.096 \times 32.05 = 4.90 - 3.0768 = 1.8232$.
> A is wrong because it charges the cost of equity on ending book value: $4.90 - 0.096 \times 35.75 = 1.4680$.
> C is wrong because it omits beta from the CAPM, $r = 0.03 + 0.055 = 0.085$, giving $4.90 - 0.085 \times 32.05 = 2.1758$.
> 2. **A.** Residual income: $RI_1 = 4.10 - 0.096 \times 24.00 = 1.7960$; $RI_2 = 4.55 - 0.096 \times 28.10 = 1.8524$; $RI_3 = 1.8232$; $RI_4 = 5.10 - 0.096 \times 35.75 = 1.6680$.
> Present values of Years 1 to 3: $1.7960/1.096 = 1.6387$, $1.8524/1.096^2 = 1.5421$, $1.8232/1.096^3 = 1.3848$, sum $4.5656$.
> With $T = 4$ and $\omega = 0.55$, the terminal term is $RI_4/[(1 + r - \omega)(1 + r)^{T-1}] = 1.6680/[(1.096 - 0.55) \times 1.096^3] = 1.6680/(0.546 \times 1.3165) = 2.3204$.
> $V_0 = 24.00 + 4.5656 + 2.3204 = 30.8861$, below the NOK 38.00 price, so on Lindqvist's view Solvang is overvalued.
> B is wrong because it sums the explicit stage through $T$ (5.7216) and then also discounts the persistence term $T$ periods: $24.00 + 5.7216 + 1.6680/(0.546 \times 1.096^4) = 24.00 + 5.7216 + 2.1172 = 31.8388$.
> C is wrong because it ignores the fade and treats residual income as a perpetuity ($\omega = 1$): $24.00 + 4.5656 + 1.6680/(0.096 \times 1.3165) = 24.00 + 4.5656 + 13.1976 = 41.7632$.
> 3. **B.** $B_4 = 35.75 + 5.10 - 1.50 = 39.35$; $P_4 = 1.6 \times 39.35 = 62.96$; premium over book $P_4 - B_4 = 23.61$; present value $= 23.61/1.096^4 = 23.61/1.4429 = 16.3627$.
> The explicit stage now runs through Year 4: $1.6387 + 1.5421 + 1.3848 + 1.6680/1.096^4 (= 1.1560) = 5.7216$.
> $V_0 = 24.00 + 5.7216 + 16.3627 = 46.0843$, above the NOK 38.00 price, so on Brandt's view Solvang is undervalued.
> A is wrong because it stops the explicit stage at Year 3, as the persistence formula does, while using a price-based premium that requires the full four years: $24.00 + 4.5656 + 16.3627 = 44.9283$.
> C is wrong because it discounts the full terminal price rather than the premium over book value, double counting book value: $24.00 + 5.7216 + 62.96/1.4429 = 24.00 + 5.7216 + 43.6337 = 73.3554$.
> 4. **C.** Low dividend payout is associated with higher persistence of residual income, together with high historical industry persistence and strong market leadership.
> A 12% average payout therefore argues for a factor above 0.55.
> A is wrong because extreme accruals are associated with lower persistence.
> B is wrong because large special items are also associated with lower persistence; both A and B support Lindqvist's below-average factor rather than a higher one.
> 5. **C.** Present value of dividends: $0.00 + 0.60/1.096^2 + 1.20/1.096^3 + 1.50/1.096^4 = 0.4995 + 0.9115 + 1.0396 = 2.4505$.
> Present value of the terminal price $= 62.96/1.096^4 = 43.6337$.
> DDM value $= 2.4505 + 43.6337 = 46.0843$, the same as Brandt's residual income value because the forecasts are consistent and clean surplus holds.
> Terminal share under the DDM $= 43.6337/46.0843 = 0.9468$, or about 94.7%.
> A is wrong because it is the terminal premium's share of the residual income value, $16.3627/46.0843 = 0.3551$, the measure of how little the RI model depends on the terminal value.
> B is wrong because it is current book value's share of the residual income value, $24.00/46.0843 = 0.5208$.
> 6. **A.** Lindqvist is correct: residual income models recognize value earlier, with current book value carrying a large share of value, so they are well suited to companies with negative near-term free cash flow, whereas an FCFE model with negative early flows depends heavily on its terminal value.
> Brandt is incorrect: with internally consistent forecasts and clean surplus accounting, the DDM, FCFE and residual income models give the same value, as the Question 5 calculation shows (46.0843 both ways).
> The residual income model is the DDM rewritten using $D_t = E_t + B_{t-1} - B_t$, so retained earnings are not ignored in the DDM; they reappear as higher future dividends and a higher terminal price.
> B and C are wrong because they accept Brandt's claim that the two models give different values under consistent assumptions.

## Distractor design

1. A: equity charge on ending rather than beginning book value; C: CAPM with beta omitted (misread of the rate inputs).
2. B: explicit stage summed through T and persistence term discounted T periods (period error); C: persistence factor ignored, perpetuity used (wrong continuing-RI case).
3. A: explicit stage stopped at T - 1 under a price-based terminal value (formula variant mixed up); C: full terminal price discounted instead of the premium over book value.
4. A and B: markers of low persistence chosen when the question asks for a marker of high persistence (direction reversed).
5. A: RI terminal premium share substituted for the DDM terminal share; B: book value share under RI substituted (value recognition confused across models).
6. B and C: accepting that consistent DDM and RI forecasts give different values.
