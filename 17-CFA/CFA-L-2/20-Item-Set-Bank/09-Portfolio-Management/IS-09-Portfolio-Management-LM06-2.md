---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 6
title: "Meridian Harbour Capital: Compliance Review of a Backtest Deck"
los: [los-09-06-c, los-09-06-d, los-09-06-e]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Meridian Harbour Capital: Compliance Review of a Backtest Deck

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tan Wei Ling, CFA, is head of compliance at Meridian Harbour Capital, a Singapore-based hedge fund manager.
Before a fund launch, she must approve the marketing presentation for two self-financing long-short equity strategies built on the MSCI AC Asia ex Japan universe with returns in US dollars.
Strategy M is a pure price-momentum strategy.
Strategy C combines momentum, value, and quality signals.
The presentation was prepared by quantitative analyst Daniel Koh and covers January 2000 to December 2024 (300 months).

Koh used point-in-time index constituents and monthly rebalancing.
To show how the strategies behaved in different environments, he split the 300 months two ways: into US recession and expansion months using the NBER business-cycle chronology as published today, and into high-volatility and low-volatility months according to whether the VIX was above or below its five-year moving average.

Exhibit 1: Annualized performance by regime, 2000 to 2024

| Regime | Months | Strategy M return | Strategy M volatility | Strategy C return | Strategy C volatility |
|---|---|---|---|---|---|
| Recession | 38 | -6.2% | 18.4% | 3.1% | 7.9% |
| Expansion | 262 | 10.8% | 13.5% | 6.9% | 6.8% |
| High volatility | 96 | 2.4% | 19.6% | 5.4% | 8.8% |
| Low volatility | 204 | 11.6% | 11.2% | 6.9% | 6.1% |

The presentation reports Sharpe ratios as annualized return divided by annualized volatility, because the long-short strategies are self-financing.
Over the full period it shows Sharpe ratios of 0.61 for Strategy M and 0.93 for Strategy C.
The US Treasury bill yield averaged 2.4% over the period.

Koh also presents Strategy C+, a regime-switching overlay that holds Strategy C in months the NBER chronology labels as recession and Strategy M in all other months.
The slide describes C+ as "a dynamic strategy with the best full-period return of the three."

A later slide introduces an "enhanced" version of Strategy C.
Koh explains that he tested 64 variants of Strategy C over the most recent 120 months, varying the signal weights, the rebalancing frequency, and the formation window, and selected the variant with the best statistics.
The selected variant earned a mean monthly return of 0.62% with a monthly standard deviation of 3.10%.
The slide states that the variant is "statistically significant at conventional levels."

The final slide plots the growth of USD 1 invested in Strategy M on a linear vertical axis.
The caption reads: "Performance has accelerated sharply since 2016."
Tan asks Koh whether the chart would look the same on a logarithmic axis.

Tan also asks Koh to add one more piece of historical scenario analysis before the presentation is approved.
Koh lists three candidate tests:

- Test 1: rerun the backtest on the MSCI AC Asia ex Japan large-cap index instead of the broad index.
- Test 2: compare the strategies' Sharpe ratios in months when the US Federal Reserve was raising its policy rate against months when it was cutting or holding the rate.
- Test 3: rerun the fund's Monte Carlo simulation with a multivariate skewed Student's t-distribution instead of a multivariate normal distribution.

Tan's approval memo will state which figures in the deck are reliable, which must be restated, and what disclosures are required.

## Questions

1. The Sharpe ratio of Strategy M in recession months, under the presentation's convention, is closest to: (LOS: los-09-06-e)
   - A. -2.97.
   - B. -0.47.
   - C. -0.34.
2. Based on Exhibit 1, which conclusion from the historical scenario analysis is most appropriate? (LOS: los-09-06-e)
   - A. Strategy M is more robust, because it earns the higher return in the expansion and low-volatility regimes, which together account for most months.
   - B. Strategy C is more robust, because its Sharpe ratio stays positive and between about 0.39 and 1.13 across all four regimes.
   - C. No conclusion is possible, because splitting a backtest by regime is sensitivity analysis rather than scenario analysis.
3. Weighting regimes by number of months, the full-period annual return of Strategy C+ implied by Exhibit 1, and the most appropriate compliance comment, are closest to: (LOS: los-09-06-d)
   - A. 6.95%; the return is overstated by look-ahead bias.
   - B. 9.82%; the return is overstated by look-ahead bias.
   - C. 9.82%; the return is overstated by survivorship bias.
4. The t-statistic of the enhanced variant's mean monthly return, and the most appropriate response, are closest to: (LOS: los-09-06-d)
   - A. 2.19; the variant is not yet acceptable, because selection from 64 variants calls for a hurdle above 3.0 and cross-validation on data not used to select it.
   - B. 2.19; the variant is significant, because 2.19 exceeds the conventional hurdle of 2.0.
   - C. 0.69; the variant should be rejected, because its t-statistic is below 1.0.
5. Which of Koh's candidate tests is a historical scenario analysis? (LOS: los-09-06-e)
   - A. Test 1.
   - B. Test 2.
   - C. Test 3.
6. If Strategy M had earned a constant 8.0% every year from 2000 to 2024, the vertical rise of its wealth line during 2024, relative to its rise during 2000, would be closest to: (LOS: los-09-06-c)
   - A. 1.00 on a linear axis and 6.34 on a logarithmic axis.
   - B. 6.85 on both a linear axis and a logarithmic axis.
   - C. 6.34 on a linear axis and 1.00 on a logarithmic axis.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Under the presentation's convention, Sharpe ratio $= -6.2 / 18.4 = -0.3370$, or about -0.34.
> A is wrong because it inverts the ratio, dividing volatility by return: $18.4 / (-6.2) = -2.9677$.
> B is wrong because it deducts the 2.4% Treasury bill yield from a self-financing long-short return: $(-6.2 - 2.4)/18.4 = -0.4674$.
> 2. **B.** Regime Sharpe ratios for Strategy C are $3.1/7.9 = 0.3924$, $6.9/6.8 = 1.0147$, $5.4/8.8 = 0.6136$ and $6.9/6.1 = 1.1311$: positive in every regime.
> For Strategy M they are $-6.2/18.4 = -0.3370$, $10.8/13.5 = 0.8000$, $2.4/19.6 = 0.1224$ and $11.6/11.2 = 1.0357$, so M collapses in recessions and in high-volatility months.
> Strategy C's risk-adjusted performance is robust across regimes, and it beats M's Sharpe ratio in all four regimes.
> A is wrong because it ranks on raw return in the favourable regimes and ignores the risk-adjusted collapse in the adverse ones.
> C is wrong because splitting history into regimes is exactly historical scenario analysis; sensitivity analysis changes a model input or assumption.
> 3. **B.** C+ earns Strategy C's return in the 38 recession months and Strategy M's return in the 262 expansion months.
> Return $= (38 \times 3.1 + 262 \times 10.8)/300 = (117.8 + 2{,}829.6)/300 = 9.8247\%$, against $8.6467\%$ for Strategy M and $6.4187\%$ for Strategy C on the same weighting.
> The rule uses the NBER chronology as published today, but NBER identifies turning points only with a long lag (the December 2007 peak was announced in December 2008), so the switching dates were not knowable in real time and the 9.82% is inflated by look-ahead bias.
> A is wrong because it weights the two regimes equally, $(3.1 + 10.8)/2 = 6.95\%$, instead of by the number of months.
> C is wrong because it names the wrong member of the bias family; the universe uses point-in-time constituents, and the problem is the timing of the regime information, not survivors.
> 4. **A.** Standard error $= 3.10/\sqrt{120} = 3.10/10.9545 = 0.2830\%$; $t = 0.62/0.2830 = 2.1909$.
> The t-statistic of 2.19 passes the single-test hurdle of 2.0, but the variant was chosen as the best of 64 after the results were seen, which is data snooping.
> Multiple testing inflates the best t-statistic, so the module's defenses are a hurdle above 3.0 and cross-validation on data not used in selection, such as earlier years or other markets.
> B is wrong because it applies the single-test hurdle to the winner of 64 trials.
> C is wrong because it scales by $\sqrt{12}$ instead of $\sqrt{n}$: $0.62 \times 3.4641 / 3.10 = 0.6928$.
> 5. **B.** Historical scenario analysis compares performance across structural regimes; Fed tightening versus easing is a regime split of the same history.
> A is wrong because changing the investment universe changes no structural regime, so it is neither scenario nor sensitivity analysis.
> C is wrong because swapping the distributional assumption in a simulation is sensitivity analysis.
> 6. **C.** On a linear axis the rise in year $t$ is $0.08 \times 1.08^{t-1}$.
> The rise in 2000 (year 1) is 0.0800 and in 2024 (year 25) is $0.08 \times 1.08^{24} = 0.08 \times 6.3412 = 0.5073$, a ratio of 6.3412.
> On a logarithmic axis the rise every year is $\ln(1.08) = 0.0770$, a ratio of 1.00, which is why the module plots cumulative performance on a log scale: equal percentage changes plot as equal vertical distances, so a constant return does not look like acceleration.
> A is wrong because it swaps the two axes.
> B is wrong because it uses the whole-period growth factor $1.08^{25} = 6.8485$ for both axes, treating the log axis as if it magnified late gains too.

## Distractor design

1. A: ratio inverted (volatility over return); B: risk-free rate deducted from a self-financing return.
2. A: robustness judged on raw return in favourable regimes; C: scenario analysis mislabelled as sensitivity analysis.
3. A: regimes weighted equally rather than by months; C: correct figure but look-ahead bias misnamed as survivorship bias.
4. B: single-test hurdle applied after multiple testing; C: $\sqrt{12}$ used in place of $\sqrt{n}$ in the standard error.
5. A: universe change mistaken for a regime split; C: distribution change (sensitivity analysis) mistaken for scenario analysis.
6. A: linear and log axes swapped; B: whole-period growth factor used and log scaling ignored.
