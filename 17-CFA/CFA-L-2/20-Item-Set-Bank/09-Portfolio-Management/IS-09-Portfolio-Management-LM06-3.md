---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 6
title: "Bramwell Life Assurance: Historical Simulation of a Surplus Portfolio"
los: [los-09-06-f, los-09-06-g]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Bramwell Life Assurance: Historical Simulation of a Surplus Portfolio

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Oliver Pennington is an investment risk analyst at Bramwell Life Assurance, a UK life insurer.
He is evaluating the surplus portfolio that backs Bramwell's excess capital, and his findings will go to the board risk committee as part of the insurer's annual capital planning.
The surplus portfolio holds three asset classes in fixed strategic weights, rebalanced monthly: UK gilts 40%, global equities 45%, and UK commercial property 15%.
All returns are measured in pounds sterling.

Pennington's dataset contains monthly total returns for the three asset classes from January 2005 to December 2024, a total of 240 months, which he numbers from Month 1 (January 2005) to Month 240 (December 2024).
He plans to run a historical simulation with 5,000 trials.
In each trial, a random number generator produces a uniform draw between 0 and 1, and he converts the draw into one historical month by dividing the unit interval into 240 equal slices, so that a draw in the $m$-th slice selects Month $m$.
The asset-class returns for the selected month are then applied to the strategic weights to give that trial's portfolio return.

For the first trial, the random number generator produces a draw of 0.73815.

Exhibit 1: Monthly asset-class returns for selected months

| Month | Calendar month | UK gilts | Global equities | UK commercial property |
|---|---|---|---|---|
| 177 | September 2019 | 0.4% | 1.8% | -0.6% |
| 178 | October 2019 | -0.9% | 2.6% | 1.1% |
| 179 | November 2019 | 0.7% | 2.1% | 0.2% |

Pennington's junior colleague, Grace Adeyemi, has two questions.
First, she asks how 5,000 trials can be run when the dataset contains only 240 months.
Second, she wants to know what changes in the process if the historical simulation is replaced by a Monte Carlo simulation.

Pennington writes down the steps he follows for any simulation:

- Step 1: define the target variable, the monthly return of the surplus portfolio.
- Step 2: specify the key decision variables, the three asset-class returns and their strategic weights.
- Step 3: choose the number of trials, 5,000.
- Step 4: specify the distributional properties of the key decision variables.
- Step 5: draw random numbers for each trial and convert them into values of the key decision variables.
- Step 6: compute the target variable for each trial.
- Step 7: repeat Steps 5 and 6 until all trials are complete.
- Step 8: analyze the 5,000 outcomes using metrics such as the Sharpe ratio, CVaR, and maximum drawdown.

At the risk committee meeting, the chief investment officer, Harriet Doyle, raises a further concern.
"Our dataset starts in 2005," she says, "so it contains no sustained period of high inflation combined with falling real growth.
I want the committee to see how the surplus portfolio would behave in a stagflation environment of the kind the United Kingdom experienced in the 1970s, including combinations of gilt and equity returns that our 20-year history never produced."
Pennington notes that Bramwell's regulator has not required any particular method and that the choice is the committee's.

## Questions

1. For the first trial, the month selected and the trial's portfolio return are closest to: (LOS: los-09-06-g)
   - A. Month 177; 0.88%.
   - B. Month 178; 0.93%.
   - C. Month 178; 0.98%.
2. The most accurate answer to Adeyemi's first question is that the historical simulation: (LOS: los-09-06-f)
   - A. samples months with replacement (bootstrapping), so the same month can be selected in many trials.
   - B. creates additional months by interpolating between adjacent historical observations.
   - C. draws months in chronological order, in the same way as a rolling-window backtest.
3. To address Doyle's concern, the committee should most appropriately use: (LOS: los-09-06-f)
   - A. the historical simulation with 10,000 trials instead of 5,000.
   - B. a Monte Carlo simulation, with the distribution of asset-class returns specified and calibrated to reflect a stagflation environment.
   - C. a rolling-window backtest over the same 240 months.
4. In answer to Adeyemi's second question, replacing the historical simulation with a Monte Carlo simulation changes which of Pennington's steps? (LOS: los-09-06-g)
   - A. Step 2 only, because Monte Carlo simulation uses different key decision variables.
   - B. Steps 4 and 5, because values are drawn from a specified, calibrated distribution rather than from the historical months.
   - C. Step 8 only, because Monte Carlo output cannot be summarized with CVaR or maximum drawdown.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Each slice has width $1/240 = 0.004167$.
> The draw selects Month $m = \lceil 0.73815 \times 240 \rceil = \lceil 177.1560 \rceil = 178$, which is October 2019 (the draw lies between $177/240 = 0.73750$ and $178/240 = 0.74167$); this is the inverse transformation method.
> Portfolio return $= 0.40(-0.9) + 0.45(2.6) + 0.15(1.1) = -0.3600 + 1.1700 + 0.1650 = 0.9750\%$, or about 0.98%.
> A is wrong because it truncates 177.156 to Month 177 instead of rounding up, and then applies the weights to September 2019: $0.40(0.4) + 0.45(1.8) + 0.15(-0.6) = 0.8800\%$.
> B is wrong because it selects the right month but equal-weights the asset classes instead of using the strategic weights: $(-0.9 + 2.6 + 1.1)/3 = 0.9333\%$.
> 2. **A.** When the number of trials needed exceeds the number of historical observations, historical simulation samples with replacement (bootstrapping).
> With 240 months and 5,000 trials, each month is selected about $5{,}000/240 = 20.8$ times on average.
> B is wrong because interpolation manufactures returns that never occurred, which defeats the premise of sampling actual history.
> C is wrong because historical simulation draws months randomly without regard to time order; the chronological, deterministic procedure is the rolling-window backtest.
> 3. **B.** Historical simulation, whatever the number of trials, can only replay months that occurred, so it assumes that the 2005 to 2024 history spans the future.
> Monte Carlo simulation assigns a statistical distribution to the key decision variables, calibrated from data and judgment, and draws from it, so it can produce outcomes and combinations of asset returns that the historical record never contained.
> The cost is complexity and dependence on the chosen functional form, which is why sensitivity analysis usually follows.
> A is wrong because more trials only resample the same 240 months more often.
> C is wrong because a rolling-window backtest is the single realized path of the same history.
> 4. **B.** The two simulation approaches share the target variable, the key decision variables, the number of trials and the analysis of output.
> They differ at Step 4, where Monte Carlo simulation specifies a functional form (for correlated asset classes, a multivariate distribution) and calibrates its parameters, and at Step 5, where the random numbers are converted into draws from that fitted distribution rather than into historical months.
> A is wrong because the key decision variables are still the three asset-class returns and their weights.
> C is wrong because CVaR, maximum drawdown and the Sharpe ratio are computed from the simulated outcomes under either approach.

## Distractor design

1. A: draw truncated to Month 177 instead of rounded up, so the adjacent row of the exhibit is read; B: correct month but equal weights used instead of strategic weights.
2. B: interpolation mistaken for bootstrapping; C: historical simulation confused with the deterministic rolling-window backtest.
3. A: more trials assumed to create outcomes outside history; C: a single historical path offered as a simulation substitute.
4. A: the decision variables wrongly assumed to change; C: output metrics wrongly assumed to be method specific.
