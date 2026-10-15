---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 6
title: "Almendra Gestion: Backtesting a European Earnings Yield Strategy"
los: [los-09-06-b, los-09-06-c, los-09-06-d]
difficulty: 3
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Almendra Gestion: Backtesting a European Earnings Yield Strategy

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Lucia Ferrer, CFA, is head of equity strategies at Almendra Gestion, an asset manager in Madrid.
Almendra is considering a self-financing long-short value fund, and Ferrer has asked quantitative analyst Iker Zubiri to backtest it before it goes to the product committee.

Zubiri states the hypothesis as "stocks that are cheap relative to their trailing earnings outperform stocks that are expensive."
He measures cheapness with trailing earnings yield, defined as the sum of the last four reported quarterly EPS divided by the share price on the rebalancing date.
The investment universe is the point-in-time constituents of the STOXX Europe 600 Index, returns are measured in euros, and the backtest runs from January 2012 to December 2024.
On each rebalancing date, stocks are sorted into quintiles by the signal, and the strategy buys the cheapest quintile and shorts the most expensive quintile, with equal weights within each quintile.
Fundamentals come from a vendor database that records each quarterly EPS figure as first published, together with the date on which it became public.

To check his signal code on the first live rebalancing date, 30 June 2025, Zubiri prints the extract in Exhibit 1.
All four quarterly EPS figures shown for each stock were public by that date.

Exhibit 1: Signal check for selected stocks, 30 June 2025 (EUR)

| Stock | Q2 2024 EPS | Q3 2024 EPS | Q4 2024 EPS | Q1 2025 EPS | Share price | Consensus next-12-month EPS |
|---|---|---|---|---|---|---|
| Arvena | 0.45 | 0.50 | 0.52 | 0.53 | 25.00 | 2.60 |
| Bellcourt | -0.05 | -0.20 | -0.25 | -0.10 | 12.00 | 0.30 |
| Corvia | 0.50 | 0.46 | 0.44 | 0.50 | 20.00 | 1.70 |
| Dalmar | 0.75 | 0.80 | 0.78 | 0.77 | 40.00 | 3.20 |

Exhibit 2: Value at each year-end of EUR 1.000 invested at the start of 2012 (monthly rebalancing, net of transaction costs)

| Year-end | Value | Year-end | Value |
|---|---|---|---|
| Start of 2012 | 1.000 | 2018 | 1.106 |
| 2012 | 1.084 | 2019 | 1.244 |
| 2013 | 1.172 | 2020 | 1.302 |
| 2014 | 1.251 | 2021 | 1.221 |
| 2015 | 1.103 | 2022 | 1.318 |
| 2016 | 1.035 | 2023 | 1.395 |
| 2017 | 0.982 | 2024 | 1.452 |

Ferrer asks whether rebalancing weekly would let the strategy react faster to new earnings.
Zubiri reruns the backtest with weekly rebalancing and reports the annualized statistics in Exhibit 3.

Exhibit 3: Annualized backtest statistics by rebalancing frequency, 2012 to 2024

| Statistic | Monthly rebalancing | Weekly rebalancing |
|---|---|---|
| Return, gross of transaction costs | 5.70% | 6.60% |
| Return, net of transaction costs | 5.40% | 4.95% |
| Volatility of net returns | 7.20% | 7.60% |
| Downside deviation of net returns (target 0%) | 4.50% | 5.10% |
| Average annual one-way turnover | 210% | 1,140% |

Almendra computes Sortino ratios for self-financing long-short strategies on net-of-cost returns with a target return of zero.
The cash rate Almendra assumed for the period averaged 0.5%.

Ferrer then asks Zubiri to extend the backtest back to January 2000.
The vendor's publication dates are available only from 2012 onward.
For 2000 to 2011, Zubiri has a second database that holds EPS as first published but does not record when each figure became public.
He proposes to treat every company's quarterly EPS as available one month after the end of the quarter.

## Questions

1. Which stock in Exhibit 1 ranks cheapest on Zubiri's value signal? (LOS: los-09-06-b)
   - A. Arvena.
   - B. Bellcourt.
   - C. Corvia.
2. Measured on the year-end values in Exhibit 2, the maximum drawdown of the strategy is closest to: (LOS: los-09-06-c)
   - A. -21.5%.
   - B. -32.4%.
   - C. -11.8%.
3. Using Almendra's convention, moving from monthly to weekly rebalancing changes the strategy's Sortino ratio by approximately: (LOS: los-09-06-c)
   - A. -0.10.
   - B. -0.23.
   - C. +0.03.
4. Zubiri's proposal for the 2000 to 2011 data is best described as: (LOS: los-09-06-d)
   - A. adequate, because figures stored as first published cannot create look-ahead bias whatever availability date is assumed.
   - B. likely to create stale data for most companies, because a one-month lag is longer than European companies typically take to publish.
   - C. likely to leave look-ahead bias, because a lag of about two to three months best replicates point-in-time results for European companies.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Trailing earnings yield $= \text{trailing 12-month EPS} / \text{price}$, where trailing EPS is the sum of the last four reported quarters.
> Arvena: $0.45 + 0.50 + 0.52 + 0.53 = 2.00$; $2.00/25.00 = 8.0000\%$.
> Bellcourt: $-0.05 - 0.20 - 0.25 - 0.10 = -0.60$; $-0.60/12.00 = -5.0000\%$.
> Corvia: $0.50 + 0.46 + 0.44 + 0.50 = 1.90$; $1.90/20.00 = 9.5000\%$.
> Dalmar: $0.75 + 0.80 + 0.78 + 0.77 = 3.10$; $3.10/40.00 = 7.7500\%$.
> Corvia has the highest trailing earnings yield, so it is the cheapest stock and a candidate for the long quintile.
> A is wrong because it ranks on consensus forward EPS, which is not Zubiri's trailing signal: Arvena's forward yield is $2.60/25.00 = 10.4000\%$ against Corvia's $1.70/20.00 = 8.5000\%$.
> B is wrong because it ranks on the lowest P/E: Bellcourt's P/E is $12.00/(-0.60) = -20.0$, the lowest number only because its earnings are negative, which is exactly why the curriculum prefers earnings yield (here $-5.00\%$, correctly ranked last) to P/E.
> 2. **A.** Maximum drawdown is the worst percentage fall from a running peak to a later trough.
> The running peak of 1.251 (end of 2014) is followed by a trough of 0.982 (end of 2017), so $\text{MDD} = (0.982 - 1.251)/1.251 = -0.2690/1.251 = -21.5028\%$, or about -21.5%.
> No later decline from a running peak is larger; the 2021 fall from 1.302 to 1.221 is $-6.2212\%$.
> B is wrong because it pairs the lowest value with the highest value, which comes after the trough: $(0.982 - 1.452)/1.452 = -32.3691\%$.
> A drawdown must be measured from a peak that precedes the trough.
> C is wrong because it takes the largest single-year loss, 2015: $(1.103 - 1.251)/1.251 = -11.8305\%$, and ignores that the decline continued for two more years.
> 3. **B.** Sortino ratio $= (r_p - r_{\text{target}})/\sigma_{\text{downside}}$ with a target of 0% and net-of-cost returns.
> Monthly: $5.40/4.50 = 1.2000$.
> Weekly: $4.95/5.10 = 0.9706$.
> Change $= 0.9706 - 1.2000 = -0.2294$, or about -0.23, so weekly rebalancing makes the strategy worse because the extra trading costs outweigh the gain from faster signals.
> Gross returns rise by $6.60 - 5.70 = 0.90$ percentage points, but costs rise from $0.30$ to $1.65$ percentage points a year.
> A is wrong because it uses Sharpe-style total volatility instead of downside deviation: $5.40/7.20 - 4.95/7.60 = 0.7500 - 0.6513 = 0.0987$, a fall of about 0.10.
> C is wrong because it uses gross-of-cost returns: $6.60/5.10 - 5.70/4.50 = 1.2941 - 1.2667 = +0.0275$; many strategies that look better at higher frequencies fail once transaction costs are included.
> The 0.5% cash rate is not deducted, because Almendra's target return is zero.
> 4. **C.** Using EPS figures before they were actually public is look-ahead bias.
> Where point-in-time publication dates are unavailable, a reporting lag is applied, and the lag that best replicates point-in-time results is about two to three months for Europe and the United Kingdom.
> A one-month lag therefore treats many companies' results as known before they were published, and the backtest will still use unavailable information.
> A is wrong because storing figures as first published removes the revision problem but not the timing problem; the signal still depends on when the figure is assumed to be known.
> B is wrong because it reverses the direction: a stale-data problem arises when the uniform lag is too long (for example, four months for fast-reporting large caps), not when it is shorter than typical European reporting delays.

## Distractor design

1. A: forward (consensus) EPS used instead of the trailing signal; B: stocks ranked by lowest P/E, which puts a loss-making stock first.
2. B: trough paired with a peak that occurs after it; C: largest single-period loss mistaken for the peak-to-trough loss.
3. A: total volatility (Sharpe ratio) used instead of downside deviation; C: gross-of-cost returns used, ignoring transaction costs.
4. A: first-published data assumed to fix timing as well as revisions; B: look-ahead (lag too short) confused with stale data (lag too long).
