---
type: cfa-itemset
topic: "Alternative Investments"
topic_code: "08"
topic_slug: "08-Alternative-Investments"
lm: 4
title: "Whitcombe University Endowment Crisis Exposure Study"
los: [los-08-04-b, los-08-04-e, los-08-04-h, los-08-04-i]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/alternative-investments]
---

# Whitcombe University Endowment Crisis Exposure Study

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Helena Marsh, CFA, is director of risk at the Whitcombe University Endowment, which holds a 60/40 portfolio of global equities and investment-grade bonds.
The investment committee intends to move 20% of the portfolio into a single hedge fund strategy, producing a 48/32/20 mix.
Marsh first studies how three candidate funds behaved in stress periods, using a conditional linear factor model estimated on monthly returns.
The model includes normal-period factors (SNP500, CREDIT, USD, VIX) and crisis-period factors (DSNP500, DCREDIT, DUSD, DVIX), where each crisis factor equals the normal factor multiplied by a dummy variable that is 1 from June 2007 to February 2009 and 0 otherwise.
A coefficient is treated as significant when the absolute value of its t-statistic exceeds 2.0.

**Exhibit 1: Conditional factor model estimates (t-statistics in parentheses)**

| Coefficient | Fund P (long/short equity) | Fund R (fund of funds, equity) | Fund S (systematic futures) |
|---|---|---|---|
| Alpha (monthly, %) | 0.28 (2.40) | 0.09 (0.85) | 0.21 (1.60) |
| SNP500 | 0.46 (8.10) | 0.31 (5.20) | 0.04 (0.70) |
| CREDIT | -0.27 (-2.10) | -0.19 (-1.95) | 0.03 (0.45) |
| USD | -0.09 (-1.35) | -0.04 (-0.90) | 0.11 (1.40) |
| VIX | 0.01 (0.40) | -0.01 (-0.35) | 0.02 (0.55) |
| DSNP500 | 0.18 (2.31) | -0.07 (-0.60) | -0.26 (-2.60) |
| DCREDIT | -0.14 (-1.30) | -0.11 (-0.85) | -0.06 (-0.55) |
| DUSD | -0.22 (-2.05) | -0.05 (-0.70) | 0.14 (1.10) |
| DVIX | -0.03 (-1.12) | -0.09 (-2.45) | 0.05 (1.30) |
| Adjusted R-squared | 0.71 | 0.58 | 0.12 |

Fund P's latest report shows gross long positions of 88% of NAV and gross short positions of 38% of NAV.
Fund S trades 60 futures markets across equities, bonds, currencies, and commodities.
It goes long any market with a positive trailing 12-month return and short any market with a negative trailing 12-month return, sizing each position inversely to that market's volatility.

Exhibit 2 shows simulated statistics for the current portfolio and for 48/32/20 portfolios built with each candidate strategy.

**Exhibit 2: Simulated portfolio statistics, 2000 to the present**

| Portfolio | Standard deviation | Sharpe ratio | Sortino ratio | Maximum drawdown |
|---|---|---|---|---|
| Current 60/40 | 9.20% | 0.55 | 0.98 | 17.40% |
| With equity market neutral | 7.70% | 0.70 | 1.22 | 14.90% |
| With systematic futures | 8.05% | 0.78 | 1.46 | 13.60% |
| With merger arbitrage | 8.20% | 0.71 | 1.18 | 11.40% |
| With long/short equity | 8.62% | 0.74 | 1.50 | 17.10% |

The committee has set three conditions for the allocation.
First, the variance of the combined portfolio must be no more than 85% of the variance of the current portfolio.
Second, the combined portfolio's maximum drawdown must be lower than the current portfolio's.
Third, among the portfolios that meet the first two conditions, the committee will choose the one with the best risk-adjusted return, bearing in mind that it expects large negative events over the investment horizon.

At the committee meeting on 22 October, trustee Colin Abara comments: "Fund R spreads its capital across many managers, so it cannot have picked up any volatility exposure in the crisis that it did not have in normal markets."
A second trustee, Ruth Okafor, adds: "Fund S's appeal is that it behaves like our bond book, earning steady returns when markets are calm and mean-reverting."

## Questions

1. Fund P's total equity market exposure during the crisis period is closest to: (LOS: los-08-04-h)
   - A. 0.18
   - B. 0.46
   - C. 0.64
2. Regarding Abara's comment, Fund R's estimates most likely indicate that during the crisis, Fund R: (LOS: los-08-04-h)
   - A. had no meaningful volatility exposure, because its normal-period VIX coefficient is not significant, so Abara is correct.
   - B. became significantly short volatility, with a total VIX exposure of about -0.10, so Abara is incorrect.
   - C. became long volatility, which hedged its equity exposure, so Abara is incorrect.
3. Fund P's net exposure and the strategy it is consistent with are best described as: (LOS: los-08-04-b)
   - A. 50% net long, which is typical of long/short equity.
   - B. 126% net long, which suggests a levered long-only fund.
   - C. 50% net short, which is typical of a short-biased fund.
4. The maximum standard deviation of the combined portfolio permitted by the committee's first condition is closest to: (LOS: los-08-04-i)
   - A. 6.65%
   - B. 7.82%
   - C. 8.48%
5. Based on all three of the committee's conditions, the most suitable strategy is: (LOS: los-08-04-i)
   - A. equity market neutral.
   - B. systematic futures.
   - C. long/short equity.
6. The best response to Okafor's comment is that Fund S's role in the portfolio most likely comes from: (LOS: los-08-04-e)
   - A. its tendency to deliver positive right-tail skewness in periods of market stress, because it needs trends and volatility rather than mean reversion.
   - B. its structurally market-neutral book, because it ranks markets against each other and holds equal long and short positions.
   - C. its steady returns in calm, mean-reverting markets, as Okafor states.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** The crisis coefficient is an increment to the normal beta, not a replacement for it: $\beta_{\text{crisis,total}} = \beta_{\text{normal}} + \beta_D = 0.46 + 0.18 = 0.64$.
> Both coefficients are significant (t-statistics 8.10 and 2.31), so Fund P's long equity exposure rose in the crisis, exactly when it hurt.
> A is wrong because it treats the DSNP500 coefficient alone as the crisis exposure.
> B is wrong because it ignores the significant crisis increment and reports only the normal-period beta.
> 2. **B.** Fund R's normal VIX coefficient ($-0.01$, t $= -0.35$) is insignificant, but its DVIX coefficient ($-0.09$, t $= -2.45$) is significant, so a short volatility exposure emerged only in the crisis.
> Total crisis VIX exposure is about $-0.01 + (-0.09) = -0.10$, so Fund R lost as the VIX spiked; this is the footprint of leverage embedded in its underlying funds, and spreading capital across managers did not prevent it.
> A is wrong because it reads only the normal-period coefficient and ignores the significant crisis increment.
> C is wrong because it misreads the sign: a negative loading on the change in VIX means returns fall when volatility rises, which is short volatility, not long volatility.
> 3. **A.** Net exposure $= 88\% - 38\% = 50\%$ net long, and gross exposure is $88\% + 38\% = 126\%$.
> A 50% net long position lies inside the typical 40% to 60% band for long/short equity, and the significant SNP500 beta of 0.46 is consistent with that net long positioning.
> B is wrong because 126% is the gross exposure; adding the short positions to the longs does not give net exposure.
> C is wrong because it reverses the sign; the fund holds more long than short positions.
> 4. **C.** The condition caps variance, not standard deviation: $\sigma^2_{\max} = 9.20^2 \times 0.85 = 84.64 \times 0.85 = 71.944$, so $\sigma_{\max} = \sqrt{71.944} = 8.4820\%$, or about 8.48%.
> Equivalently, $\sigma_{\max} = \sqrt{0.85} \times 9.20 = 0.9220 \times 9.20 = 8.48\%$.
> A is wrong because it multiplies the standard deviation by the square of the fraction: $9.20 \times 0.85^2 = 6.647\%$.
> B is wrong because it multiplies the standard deviation, rather than the variance, by 0.85: $9.20 \times 0.85 = 7.82\%$.
> 5. **B.** First condition (standard deviation of 8.48% or less): equity market neutral (7.70%), systematic futures (8.05%), and merger arbitrage (8.20%) pass; long/short equity fails at 8.62% (variance $74.3044 > 71.944$).
> Second condition (drawdown below 17.40%): all three survivors pass, with drawdowns of 14.90%, 13.60%, and 11.40%.
> Third condition: because large negative events are expected, rank the survivors on the Sortino ratio, which penalizes only downside deviation; systematic futures (1.46) beats equity market neutral (1.22) and merger arbitrage (1.18).
> A is wrong because it follows from the wrong ceiling of 7.82%, under which only equity market neutral (7.70%) survives.
> C is wrong because long/short equity has the highest Sortino ratio (1.50) but fails the variance condition.
> Merger arbitrage, with the smallest drawdown, is the other tempting choice, but drawdown is a pass-or-fail condition here, not the risk-adjusted measure.
> 6. **A.** Fund S is a time-series momentum managed futures fund: it judges each market alone on its own absolute trailing return, so it can be net long or net short a whole asset class.
> Such strategies need directional trends and volatility; mean-reverting, low-volatility markets are their weakest environment, and in stress periods they have delivered positive right-tail skewness (for example, short equity futures and long bond futures in 2007 to 2009).
> Fund S's significant negative DSNP500 coefficient ($-0.26$, t $= -2.60$) against an insignificant normal equity beta is consistent with going short equities as the crisis trend developed.
> B is wrong because a structurally market-neutral book that ranks assets against each other is cross-sectional momentum; Fund S's absolute signals can leave it heavily net long or net short.
> C is wrong because it describes the environment in which trend followers struggle; steady returns in calm, mean-reverting markets are the profile of relative value strategies.

## Distractor design

- Q1: A treats the crisis increment as the total (replacement instead of increment); B ignores the significant increment.
- Q2: A reads only the normal-period coefficient; C is a sign error on the VIX loading.
- Q3: B reports gross exposure as net exposure; C is a sign error on net exposure.
- Q4: A squares the fraction; B scales the standard deviation instead of the variance (wrong formula variant).
- Q5: A follows from the wrong standard deviation ceiling in Q4; C ignores the variance condition in favor of the best Sortino ratio.
- Q6: B swaps time-series for cross-sectional momentum; C gives an opportunistic strategy the mean-reversion profile of relative value strategies.
