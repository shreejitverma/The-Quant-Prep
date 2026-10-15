---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 6
title: "Hallim Teachers' Pension Fund: Volatility Regimes and a Bootstrapped Tail"
los: [los-09-06-e, los-09-06-f, los-09-06-g]
difficulty: 3
minutes: 12
source: mock-06
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Hallim Teachers' Pension Fund: Volatility Regimes and a Bootstrapped Tail

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Park Ji-woo, CFA, is a risk analyst at the Hallim Teachers' Pension Fund in Seoul.
The fund's investment committee is reviewing a USD 1.2 billion allocation to an internally managed Multifactor Sleeve.
The sleeve is a self-financing long-short portfolio that holds five equity factor portfolios (value, quality, momentum, low volatility, and dividend yield) in fixed weights and is rebalanced monthly.
Park already has a 240-month rolling-window backtest of the sleeve and has been asked to add historical scenario analysis and simulation evidence.

For the scenario analysis, Park classifies each month as high volatility if the month-end VIX is above its five-year moving average and as low volatility otherwise.
Her colleague Oh Tae-yang suggests a fixed threshold instead, labelling every month with a VIX above 20 as high volatility, because that is the level the fund's trading desk calls stressed.
Park keeps the moving-average rule.
Before running the full analysis, she checks her classification code on the ten-month excerpt in Exhibit 1.

Exhibit 1: Excerpt from the backtest used to check the regime classification

| Month | Month-end VIX | VIX five-year moving average | Sleeve return |
|---|---|---|---|
| 1 | 18.4 | 22.9 | 0.8% |
| 2 | 21.6 | 22.9 | 0.5% |
| 3 | 25.8 | 22.8 | -1.6% |
| 4 | 23.4 | 22.8 | -0.4% |
| 5 | 20.9 | 22.7 | 0.3% |
| 6 | 17.2 | 22.7 | 1.0% |
| 7 | 16.5 | 22.6 | 0.7% |
| 8 | 24.7 | 22.6 | -1.1% |
| 9 | 22.1 | 22.6 | 0.2% |
| 10 | 19.3 | 22.5 | 0.6% |

For the simulation, Park runs a bootstrapped historical simulation with 1,000 trials.
Each trial uses a random number generator to select one of the 240 historical months, with replacement, and applies the sleeve's fixed weights to the five factor returns of that month.
She sorts the 1,000 trial returns from worst to best.
She reports VaR (95%) as the loss in the 50th-worst trial and CVaR (95%) as the average of the 50 worst trial returns.

Exhibit 2: The 50 worst trials of the historical simulation

| Trials ranked by return | Number of trials | Average return of the group |
|---|---|---|
| 1st to 10th worst | 10 | -9.8% |
| 11th to 25th worst | 15 | -6.4% |
| 26th to 50th worst | 25 | -4.2% |

The 50th-worst trial return is -3.3%, and the median trial return is 0.6%.
Park's research also shows that the five factor returns are correlated, that four of them are negatively skewed, and that all five have kurtosis above 3.0.
She plans to follow the historical simulation with a Monte Carlo simulation that draws the five factor returns from a multivariate normal distribution fitted to the same 240 months.

Before the full historical simulation, Park ran two pilot versions with 100 trials each, using different random seeds.
The pilots produced CVaR (95%) estimates of -4.1% and -7.6%.
The chief investment officer, Kang Min-seo, comments: "If the answer changes every time we run it, the simulation is not reliable.
We should rely only on the rolling-window backtest, which gives the same answer every time."

## Questions

1. For the ten months in Exhibit 1, the sleeve's mean monthly return in the high-volatility regime, as Park defines it, is closest to: (LOS: los-09-06-e)
   - A. -0.35%.
   - B. 0.59%.
   - C. -1.03%.
2. The CVaR (95%) of the sleeve from Park's historical simulation is closest to: (LOS: los-09-06-g)
   - A. -3.30%.
   - B. -5.98%.
   - C. -6.80%.
3. Which statement comparing Park's two simulation approaches is most accurate? (LOS: los-09-06-f)
   - A. The historical simulation takes all five factor returns in a trial from the same actual month, so it requires no functional form but assumes that the 240 months span the range of future outcomes.
   - B. Because it samples with replacement, the historical simulation can generate combinations of monthly factor returns that never occurred in the 240 months.
   - C. The Monte Carlo simulation will reproduce the history's negative skewness and fat tails, because the multivariate normal is fitted to the same 240 months.
4. The most appropriate response to Kang's comment is to: (LOS: los-09-06-g)
   - A. rely on the rolling-window backtest, because a deterministic method produces the most reliable estimate of tail risk.
   - B. replace the historical simulation with the Monte Carlo simulation, because drawing from a fitted distribution does not depend on random numbers.
   - C. keep the simulation and increase the number of trials, because estimates become more stable as the number of trials rises, with 1,000 to 10,000 trials typical.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Under Park's rule a month is high volatility when the month-end VIX exceeds its five-year moving average.
> That is true only in Month 3 ($25.8 > 22.8$), Month 4 ($23.4 > 22.8$) and Month 8 ($24.7 > 22.6$).
> Mean return $= (-1.6 - 0.4 - 1.1)/3 = -3.1/3 = -1.0333\%$, or about -1.03%.
> The other seven months average $(0.8 + 0.5 + 0.3 + 1.0 + 0.7 + 0.2 + 0.6)/7 = 4.1/7 = 0.5857\%$, so the sleeve's returns deteriorate sharply in high-volatility months, which is the kind of regime dependence scenario analysis is designed to reveal.
> A is wrong because it applies Oh's fixed threshold of 20, which adds Months 2, 5 and 9 (VIX above 20 but below the moving average): $(0.5 - 1.6 - 0.4 + 0.3 - 1.1 + 0.2)/6 = -2.1/6 = -0.3500\%$.
> B is wrong because it reverses the classification and averages the low-volatility months, $0.5857\%$.
> 2. **B.** CVaR (95%) is the average of all outcomes at or beyond the VaR threshold, here the 50 worst of 1,000 trials (5%).
> Weighting each group by its number of trials: $(10 \times -9.8 + 15 \times -6.4 + 25 \times -4.2)/50 = (-98.0 - 96.0 - 105.0)/50 = -299.0/50 = -5.9800\%$.
> A is wrong because $-3.30\%$ is the 50th-worst trial, which is Park's VaR (95%), not the average loss beyond it.
> C is wrong because it takes the simple average of the three group averages, $(-9.8 - 6.4 - 4.2)/3 = -6.8000\%$, ignoring that the groups hold 10, 15 and 25 trials.
> The median return of 0.6% plays no part in either tail measure.
> 3. **A.** Historical simulation draws actual months, so each trial carries a set of factor returns that occurred together, and no statistical distribution has to be specified.
> Its key assumption is that sampling the historical record provides sufficient guidance about future returns.
> Monte Carlo simulation, by contrast, requires the analyst to choose and calibrate a functional form, here a multivariate normal that preserves the correlations.
> B is wrong because sampling with replacement only lets the same actual month be selected many times; every trial is still a month that occurred, and generating outcomes outside the historical record is what Monte Carlo simulation does.
> C is wrong because a multivariate normal has zero skewness, no excess kurtosis and no tail dependence whatever data it is fitted to, so it will understate the downside risk of negatively skewed, fat-tailed factor returns; testing that assumption with, for example, a multivariate skewed t-distribution is sensitivity analysis.
> 4. **C.** With only 100 trials, each pilot's CVaR rests on the 5 worst draws, so the estimate varies widely from seed to seed.
> The choice of the number of trials is a simulation input: more trials give more stable estimates, and practice typically uses 1,000 to 10,000, which is why the full run uses 1,000.
> A is wrong because the backtest is deterministic only because it replays the one path history took; it cannot show the range of outcomes the simulation is meant to explore.
> B is wrong because Monte Carlo simulation also uses a random number generator, so it too needs enough trials to give stable estimates.

## Distractor design

1. A: fixed VIX threshold of 20 used instead of the five-year moving-average rule; B: regime classification reversed.
2. A: VaR (the threshold) reported as CVaR; C: unweighted average of group averages instead of a trial-weighted average.
3. B: bootstrapping mistaken for generating new outcomes (the Monte Carlo property); C: a fitted normal assumed to inherit the data's skewness and tails.
4. A: deterministic output mistaken for reliability; B: Monte Carlo simulation wrongly treated as not using random numbers.
