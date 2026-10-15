---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 6
title: "Aldercrest Family Office: Monte Carlo Stress of a Factor Allocation"
los: [los-09-06-b, los-09-06-f, los-09-06-g]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Aldercrest Family Office: Monte Carlo Stress of a Factor Allocation

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Sofia Lindqvist, CFA, heads quantitative research at Aldercrest Family Office, which manages USD 2.8 billion for a single family.
The family's investment committee must choose between two ways of combining seven long-short equity factor sleeves: Value, Size, Momentum, Quality, Low Volatility, Earnings Revision, and Dividend Yield.
The Benchmark (BM) portfolio weights the seven sleeves equally.
The Risk Parity (RP) portfolio sets weights so that each sleeve contributes equally to portfolio risk.

Lindqvist has already run a monthly rolling-window backtest of both portfolios from 1994 to 2024.
She has also run a bootstrapped historical simulation with 2,000 trials.
She now runs two Monte Carlo simulations, each with 2,000 trials.
The first draws the seven sleeve returns jointly from a multivariate normal distribution fitted to the historical data.
Her research shows that five of the seven sleeves have significantly correlated returns, that six have negatively skewed returns, and that all seven have kurtosis above 3.0.
She therefore runs a second Monte Carlo simulation that replaces the multivariate normal with a multivariate skewed Student's t-distribution, keeping everything else the same.

Exhibit 1: RP weights at the latest rebalancing date and first-trial sleeve returns (monthly)

| Sleeve | RP weight | Trial 1, multivariate normal | Trial 1, multivariate skewed t |
|---|---|---|---|
| Value | 9.0% | -1.4% | -2.8% |
| Size | 12.5% | 0.6% | -1.9% |
| Momentum | 7.5% | 2.9% | -6.4% |
| Quality | 18.0% | -0.3% | 0.5% |
| Low Volatility | 24.0% | 0.8% | 1.2% |
| Earnings Revision | 11.0% | 1.7% | -2.2% |
| Dividend Yield | 18.0% | -0.9% | 0.3% |

Exhibit 2: Results by evaluation method (Sharpe ratios annualized; CVaR monthly at 95%)

| Method | BM Sharpe | RP Sharpe | BM CVaR | RP CVaR |
|---|---|---|---|---|
| Rolling-window backtest | 0.92 | 1.78 | -7.4% | -1.2% |
| Historical simulation | 0.95 | 1.81 | -7.1% | -1.1% |
| Monte Carlo, multivariate normal | 1.01 | 1.84 | -4.3% | -1.0% |
| Monte Carlo, multivariate skewed t | 0.97 | 1.79 | -5.6% | -1.2% |

During the committee meeting, the family's financial adviser, Henrik Vass, questions the backtest.
He says the RP weights shown in Exhibit 1 were optimized from the full 1994 to 2024 covariance matrix and then applied to every month of the backtest.
Lindqvist replies that this is not how the backtest was built, and that the RP procedure uses rolling windows in two distinct places.

Vass then makes two statements about the simulations.

Statement 1: "Unlike the historical simulation, the Monte Carlo simulations can generate combinations of sleeve returns that never occurred in 1994 to 2024, but their results depend on the functional form Sofia chose."

Statement 2: "The historical simulation is deterministic because it uses only actual months, whereas the Monte Carlo simulations rely on a random number generator."

Lindqvist's summary for the committee will state how many parameters the multivariate normal model required, whether the RP advantage holds under every method, and which risk measure proved sensitive to the choice of method.

## Questions

1. The number of parameters Lindqvist must estimate to calibrate the multivariate normal distribution (means, standard deviations, and correlations) is closest to: (LOS: los-09-06-g)
   - A. 24.
   - B. 35.
   - C. 63.
2. The RP portfolio's return in the first trial of the skewed t simulation is closest to: (LOS: los-09-06-g)
   - A. -1.61%.
   - B. -0.78%.
   - C. 0.33%.
3. Lindqvist's second Monte Carlo simulation is best described as: (LOS: los-09-06-g)
   - A. sensitivity analysis, which adds estimation error because the skewed t-distribution has more parameters than the normal.
   - B. historical scenario analysis, because it isolates the fat-tailed months of the historical record.
   - C. sensitivity analysis, which removes both specification error and estimation error from the simulation.
4. Relative to the historical simulation, the multivariate normal Monte Carlo understates the BM portfolio's CVaR by approximately: (LOS: los-09-06-f)
   - A. 39.4%, because the normal distribution has no skewness, no excess kurtosis, and no tail dependence.
   - B. 65.1%, because the normal distribution has no skewness, no excess kurtosis, and no tail dependence.
   - C. 39.4%, because the Monte Carlo simulation used fewer trials than the historical simulation.
5. Lindqvist's reply to Vass most likely refers to using rolling windows to: (LOS: los-09-06-b)
   - A. form each factor sleeve every month, and then split the full sample once into an in-sample period and an out-of-sample period.
   - B. form each factor sleeve every month, and separately estimate a trailing covariance matrix at each rebalancing date to set the RP weights.
   - C. estimate the RP weights on the full sample, and separately bootstrap the months used for the out-of-sample test.
6. Which of Vass's statements is correct? (LOS: los-09-06-f)
   - A. Only Statement 1.
   - B. Only Statement 2.
   - C. Both Statement 1 and Statement 2.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** A $K$-variable multivariate normal needs $K$ means, $K$ standard deviations and $K(K-1)/2$ correlations.
> With $K = 7$: $7 + 7 + 7 \times 6/2 = 7 + 7 + 21 = 35$.
> All seven sleeves enter the joint distribution, including the two whose correlations with the others are not significant.
> A is wrong because it counts correlations only for the five significantly correlated sleeves: $7 + 7 + 5 \times 4/2 = 24$.
> C is wrong because it counts every cell of the $7 \times 7$ matrix, $7 + 7 + 49 = 63$, double counting symmetric pairs and treating the diagonal as extra parameters.
> 2. **B.** $r_{RP} = \sum w_i r_i$ with the skewed t column:
> $0.090(-2.8) + 0.125(-1.9) + 0.075(-6.4) + 0.180(0.5) + 0.240(1.2) + 0.110(-2.2) + 0.180(0.3)$
> $= -0.2520 - 0.2375 - 0.4800 + 0.0900 + 0.2880 - 0.2420 + 0.0540 = -0.7795\%$, or about -0.78%.
> A is wrong because it equal-weights the sleeves, which is the BM portfolio's return: $-11.3/7 = -1.6143\%$.
> C is wrong because it applies the RP weights to the multivariate normal column: $-0.1260 + 0.0750 + 0.2175 - 0.0540 + 0.1920 + 0.1870 - 0.1620 = 0.3295\%$.
> 3. **A.** Changing an input assumption, here the distribution in Step 4, and observing how the target variable responds is sensitivity analysis.
> The skewed t-distribution captures skewness and fat tails that the normal misses, reducing specification error, but it requires more parameters, so estimation error rises: the bias-variance trade-off.
> B is wrong because the rerun draws hypothetical outcomes from a fitted distribution; it does not split history into structural regimes.
> C is wrong because a richer distribution trades specification error for estimation error; it cannot remove both.
> 4. **A.** Understatement $= (7.1 - 4.3)/7.1 = 2.8/7.1 = 0.3944$, or about 39.4% of the historical simulation's CVaR.
> The sleeves are negatively skewed and fat tailed and tend to crash together, but a multivariate normal has zero skewness, zero excess kurtosis and zero tail dependence, so it understates the BM portfolio's left tail.
> The RP portfolio's CVaR is almost unchanged across methods (-1.0% to -1.2%), and RP's Sharpe ratio advantage holds under all four methods, so the Sharpe conclusion is robust while BM's CVaR is method sensitive.
> B is wrong because it divides by the Monte Carlo figure instead of the historical simulation figure: $2.8/4.3 = 0.6512$.
> C is wrong because both simulations used 2,000 trials, and the gap comes from the assumed functional form, not the trial count.
> 5. **B.** Backtesting the RP strategy needs the rolling-window procedure twice: once to form the factor sleeves each month from information then available, and once to estimate the trailing covariance matrix from which the equal-risk-contribution weights are optimized at each rebalancing date.
> Optimizing the weights on the full 1994 to 2024 covariance matrix, as Vass describes, would give every historical month weights based on future data, which is look-ahead bias.
> A is wrong because a single in-sample and out-of-sample split is not a rolling window, and it leaves the weights estimated once.
> C is wrong because full-sample weights are the look-ahead error, and bootstrapping belongs to historical simulation, not to the backtest.
> 6. **A.** Statement 1 is correct: Monte Carlo simulation draws from a specified, calibrated distribution, so it can produce outcomes outside the historical record, and its results depend on the functional form chosen.
> Statement 2 is wrong because historical simulation is also non-deterministic: it uses a random number generator to select historical months, with replacement.
> The deterministic method is the rolling-window backtest.
> B is wrong because it accepts the false claim that historical simulation is deterministic.
> C is wrong because it accepts Statement 2 along with Statement 1.

## Distractor design

1. A: correlations counted only for the correlated subset; C: full $K \times K$ matrix counted, double counting pairs.
2. A: equal weights used (the BM return) instead of RP weights; C: RP weights applied to the wrong simulation column.
3. B: sensitivity analysis mislabelled as scenario analysis; C: bias-variance trade-off ignored.
4. B: understatement divided by the Monte Carlo figure instead of the historical figure; C: correct size but attributed to trial count instead of functional form.
5. A: single sample split mistaken for rolling windows; C: full-sample weights (look-ahead) and bootstrapping confused with the backtest.
6. B: historical simulation mislabelled as deterministic; C: both statements accepted.
