---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 2
title: "Delacroix Family Office: Sizing a Mid-Cap Sleeve"
los: [los-09-02-a, los-09-02-b, los-09-02-c]
difficulty: 3
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Delacroix Family Office: Sizing a Mid-Cap Sleeve

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Amara Osei, CFA, runs the in-house equity desk of the Delacroix Family Office in Geneva.
The desk manages an active sleeve benchmarked to a pan-European mid-cap index.
Osei takes active positions in only five index constituents and holds every other constituent at its benchmark weight.
She assumes that the active returns of the five stocks are uncorrelated, that forecasts are made once a year, and that each annual forecast is independent of the last.

At the start of 2025, Osei ranks the five stocks with standardized scores that have a cross-sectional mean of zero and a variance of 1.
She converts scores into forecasts of active return with the Grinold rule, using an information coefficient of 0.10.
Her target active risk for the sleeve is 4.0%.

Exhibit 1: Five active positions, start of 2025

| Stock | Score $S_i$ | Active (residual) risk $\sigma_i$ | Total volatility | Benchmark weight | Actual portfolio weight | 2025 total return |
|---|---|---|---|---|---|---|
| Aldermoor Pharma | +1.5 | 24% | 32% | 4% | 9% | 18.0% |
| Bexley Instruments | +0.5 | 30% | 38% | 6% | 9% | -4.0% |
| Corvina Foods | 0.0 | 18% | 25% | 5% | 5% | 9.0% |
| Dunmore Rail | -0.5 | 20% | 27% | 3% | 0% | -6.0% |
| Eskdale Energy | -1.5 | 36% | 45% | 5% | 0% | 2.5% |

The mid-cap benchmark returned 7.2% in 2025.
The sleeve is long-only, so Osei cannot underweight a stock by more than its benchmark weight.

Henri Delacroix, the family's principal, reviews the desk on 16 January 2026.
He asks Osei to confirm three things: the forecast the Grinold rule produced for Aldermoor, the unconstrained optimal active weight the desk should have targeted for Dunmore Rail, and the value the five active positions added in 2025.
Osei reminds him that stocks held at benchmark weight add nothing to value added, whatever they return.

Delacroix also wants to discuss the family's separate holding in the Quillon Market Neutral Fund.
Quillon runs a dollar-neutral long-short book and reports its performance against the Treasury bill rate.
Osei's forecasts for Quillon are an expected return of 6.1% and a volatility of 4.0%.
The Treasury bill rate is 3.5%, and the family office can borrow and lend at that rate through its prime broker.
Quillon's realized return in 2025 was 7.4%.

Delacroix says: "Quillon's volatility is too low to matter in our total portfolio.
I would like our position to run at 10.0% volatility, funded by borrowing at the bill rate."

Osei replies: "Leverage changes the level of risk and return, but not the reward per unit of risk.
Because Quillon's benchmark is the bill rate, its Sharpe ratio and its information ratio are the same number, and borrowing will not change either one."

Delacroix asks for the expected return of the levered Quillon position before the next meeting.
Osei notes that the desk's figures should be stated before fees, which are negligible for this exercise.

## Questions

1. Using the Grinold rule, the forecast active return for Aldermoor Pharma is closest to: (LOS: los-09-02-c)
   - A. 2.40%.
   - B. 3.60%.
   - C. 4.80%.
2. The unconstrained mean-variance optimal active weight for Dunmore Rail at the 4.0% target active risk is closest to: (LOS: los-09-02-c)
   - A. -4.47%.
   - B. -3.31%.
   - C. -2.00%.
3. The value added by the sleeve's five active positions in 2025 is closest to: (LOS: los-09-02-a)
   - A. 0.05%.
   - B. 0.73%.
   - C. 0.84%.
4. If the family levers its Quillon position to 10.0% volatility as Delacroix proposes, the expected return of the position is closest to: (LOS: los-09-02-b)
   - A. 6.50%.
   - B. 10.00%.
   - C. 15.25%.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The Grinold rule scales a forecast as skill times active risk times score: $\mu_i = IC \times \sigma_i \times S_i = 0.10 \times 24 \times 1.5 = 3.6000\%$.
> The active (residual) risk of 24% is the correct volatility, because the forecast is for active return.
> A is wrong because it omits the score: $0.10 \times 24 = 2.4000\%$.
> C is wrong because it uses the decoy total volatility: $0.10 \times 32 \times 1.5 = 4.8000\%$.
> 2. **A.** Dunmore's forecast is $\mu = 0.10 \times 20 \times (-0.5) = -1.0000\%$.
> Optimal active weight: $\Delta w^{*} = \dfrac{\mu}{\sigma^2} \cdot \dfrac{\sigma_A}{IC\sqrt{BR}} = \dfrac{-0.0100}{0.20^2} \cdot \dfrac{0.040}{0.10\sqrt{5}} = -0.2500 \times 0.1789 = -0.0447$, or $-4.47\%$.
> Breadth is 5 because there are five uncorrelated stocks forecast once a year.
> Under the Grinold rule the IC cancels, so the weight also equals $S\sigma_A/(\sigma\sqrt{BR}) = -0.5 \times 4.0/(20 \times 2.2361) = -4.47\%$.
> The long-only rule caps the actual underweight at the 3% benchmark weight, which is why the actual active weight is only -3%.
> B is wrong because it uses the decoy total volatility of 27%: $\mu = -1.35\%$, and $-0.0135/0.27^2 \times 0.1789 = -3.31\%$.
> C is wrong because it divides by breadth instead of its square root: $-0.2500 \times 0.040/(0.10 \times 5) = -2.00\%$.
> 3. **C.** Active weights are +5%, +3%, 0%, -3%, and -5%, and they sum to zero.
> $R_A = \sum \Delta w_i R_i = 0.05(18.0) + 0.03(-4.0) + 0(9.0) - 0.03(-6.0) - 0.05(2.5) = 0.900 - 0.120 + 0 + 0.180 - 0.125 = 0.8350\%$.
> Because the active weights sum to zero, using active returns against the 7.2% benchmark gives the same 0.8350%.
> The Dunmore underweight added value because the stock lagged, and the Eskdale underweight cost value because the stock rose.
> A is wrong because it multiplies portfolio weights, not active weights, by active returns: $0.09(10.8) + 0.09(-11.2) + 0.05(1.8) = 0.0540\%$.
> B is wrong because it ignores the sign of the underweights and uses absolute active weights: $0.900 - 0.120 - 0.180 + 0.125 = 0.7250\%$.
> 4. **B.** Weight in Quillon $= 10.0/4.0 = 2.50$, funded by borrowing $1.50$ at 3.5%.
> Expected return $= 2.50(6.1) - 1.50(3.5) = 15.25 - 5.25 = 10.0000\%$.
> Check: Sharpe ratio $= (10.00 - 3.50)/10.00 = 0.6500$, the same as Quillon's own $(6.1 - 3.5)/4.0 = 0.6500$, because leverage scales excess return and volatility by the same 2.5.
> With the bill rate as benchmark, excess return equals active return and total risk equals active risk, so the IR is also 0.6500, as Osei says.
> A is wrong because it reports the levered excess return, $2.50 \times 2.6 = 6.50\%$, without adding back the risk-free rate.
> C is wrong because it ignores the cost of the borrowed 1.50: $2.50 \times 6.1 = 15.25\%$.
> The 2025 realized return of 7.4% is not an input to an ex ante forecast.

## Distractor design

1. A: score omitted from the Grinold rule; C: total volatility used instead of active (residual) risk.
2. B: total volatility used instead of active risk; C: breadth used without the square root.
3. A: portfolio weights used in place of active weights; B: signs of underweights ignored (absolute active weights).
4. A: levered excess return reported as total return; C: borrowing cost omitted.
