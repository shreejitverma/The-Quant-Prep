---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 5
title: "Tidewell Ridge Partners: Risk on a Long/Short Book"
los: [los-09-05-b, los-09-05-c, los-09-05-d, los-09-05-l]
difficulty: 3
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Tidewell Ridge Partners: Risk on a Long/Short Book

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tomasz Wierzbicki, CFA, is the risk manager of Tidewell Ridge Partners, a long/short equity hedge fund with net asset value (NAV) of USD 500 million.
The fund's portfolio manager is Celeste Arnaud.
Through risk decomposition, Wierzbicki maps the fund to two risk factors: its long book, with exposure of 130% of NAV, and its short book, with exposure of 80% of NAV.
The fund therefore runs gross exposure of 210% and net exposure of 50% of NAV.

Wierzbicki estimates a one-day 5% VaR with the parametric method, assuming normal distributions, 250 trading days per year, and the annual inputs in Exhibit 1.
The expected return shown for the short book is the expected return on the stocks sold short.

Exhibit 1: Annual risk-factor inputs

| Input | Long book | Short book |
|---|---|---|
| Exposure (% of NAV) | 130% | 80% |
| Expected return of the stocks held or sold short | 11.0% | 9.0% |
| Standard deviation | 19.0% | 17.0% |
| Beta relative to the broad equity index | 1.05 | 1.20 |
| Correlation between the two books, three-year lookback | 0.88 | 0.88 |

The fund's investor reports include maximum drawdown, which the fund defines as the largest peak-to-trough decline in month-end NAV per share.
Wierzbicki is preparing the annual report from the data in Exhibit 2.

Exhibit 2: Month-end NAV per share (USD), last calendar year

| Month | NAV | Month | NAV |
|---|---|---|---|
| January | 100.0 | July | 94.1 |
| February | 104.2 | August | 97.0 |
| March | 108.6 | September | 109.2 |
| April | 101.3 | October | 103.0 |
| May | 96.8 | November | 105.5 |
| June | 99.5 | December | 107.8 |

Arnaud is considering adding an overlay of long index put options to protect the long book.
She and Wierzbicki discuss whether the fund should keep its current VaR method.

Arnaud: "If we add the put overlay, we should move away from the parametric method, because the truncated payoffs of the puts make the portfolio's returns non-normal; historical simulation or Monte Carlo simulation can reprice the puts directly."

Wierzbicki: "Historical simulation would still require us to estimate the standard deviations of the two books and their correlation from the lookback period, so it would suffer from the same parameter-estimation problem as the parametric method."

Early this year, a wave of short covering drove the fund's most heavily shorted stocks sharply higher on the same days that its long holdings sold off.
Over that episode the realized correlation between the long and short books fell to about 0.60, and on the worst day the fund lost USD 14.2 million, far more than its reported VaR.
Arnaud asks Wierzbicki to recompute the one-day 5% VaR with all Exhibit 1 inputs unchanged except the correlation, which he should set at 0.60, and to identify which limitation of VaR the episode best illustrates.

## Questions

1. Using the lookback inputs in Exhibit 1, the fund's one-day 5% parametric VaR is closest to: (LOS: los-09-05-c)
   - A. USD 4.37 million.
   - B. USD 7.31 million.
   - C. USD 19.00 million.
2. Based on Exhibit 2, the maximum drawdown Wierzbicki should report is closest to: (LOS: los-09-05-l)
   - A. -5.90%.
   - B. -6.72%.
   - C. -13.35%.
3. Regarding the VaR method statements, which is correct? (LOS: los-09-05-b)
   - A. Arnaud's statement only.
   - B. Wierzbicki's statement only.
   - C. Both statements.
4. Arnaud's recomputed one-day 5% VaR, and the limitation of VaR the short-covering episode best illustrates, are closest to: (LOS: los-09-05-d)
   - A. USD 10.19 million; VaR disregards the right tail of the distribution.
   - B. USD 10.19 million; VaR relies on correlations that can change sharply in stressed markets.
   - C. USD 17.63 million; VaR relies on correlations that can change sharply in stressed markets.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The short book enters with a weight of $-0.80$, so the covariance term is negative and the short book's expected return is subtracted.
> $E(R_p) = 1.30(0.110) - 0.80(0.090) = 0.1430 - 0.0720 = 0.0710$.
> Variance terms: $1.30^2(0.19)^2 = 0.061009$; $0.80^2(0.17)^2 = 0.018496$; $2(1.30)(-0.80)(0.88)(0.19)(0.17) = -0.059122$; sum $0.020383$, so $\sigma_p = 0.142769$.
> Daily: $0.0710/250 = 0.000284$ and $0.142769/\sqrt{250} = 0.142769/15.811388 = 0.009030$.
> VaR $= (1.65 \times 0.009030 - 0.000284) \times 500{,}000{,}000 = (0.014899 - 0.000284) \times 500{,}000{,}000 = 0.014615 \times 500{,}000{,}000 = \text{USD } 7{,}307{,}358$, about USD 7.31 million.
> A is wrong because it uses a one standard deviation move ($z = 1.00$), which is the 16% VaR: $(0.009030 - 0.000284) \times 500\text{m} = \text{USD } 4.37$ million.
> C is wrong because it enters the short book as a long position (+0.80): $E(R_p) = 0.2150$, the covariance term becomes $+0.059122$, $\sigma_p = 0.372326$, daily $0.023548$, and VaR $= (1.65 \times 0.023548 - 0.000860) \times 500\text{m} = \text{USD } 18{,}997{,}089$, about USD 19.00 million.
> The betas in Exhibit 1 are decoys; the parametric VaR uses the factor volatilities and their correlation.
> 2. **C.** The NAV peaks at 108.6 in March and the lowest subsequent value before a new high is 94.1 in July.
> Maximum drawdown $= 94.1/108.6 - 1 = -0.133517$, about $-13.35\%$; the NAV does not recover to a new high until September (109.2), and the later decline from 109.2 to 103.0 is only $-5.68\%$.
> A is wrong because it measures the decline from the January starting value rather than from the peak: $94.1/100.0 - 1 = -5.90\%$.
> B is wrong because it reports the worst single-month return, April's $101.3/108.6 - 1 = -6.72\%$, which is the worst month, not the peak-to-trough decline the fund's definition requires.
> 3. **A.** Arnaud is correct: option payoffs are truncated, so a portfolio with options has non-normal returns that the parametric method handles poorly, while historical simulation and Monte Carlo simulation reprice the options under each simulated outcome.
> Wierzbicki is incorrect: historical simulation reprices the current portfolio on the actual factor returns of each lookback day and reads the percentile from the sorted outcomes, so it never estimates a standard deviation or a correlation.
> Its weakness is instead that the future may not resemble the lookback period.
> B and C are wrong because each accepts Wierzbicki's statement.
> 4. **B.** With $\rho = 0.60$, only the covariance term changes: $2(1.30)(-0.80)(0.60)(0.19)(0.17) = -0.040310$.
> Variance $= 0.061009 + 0.018496 - 0.040310 = 0.039195$, so $\sigma_p = 0.197976$ and the daily value is $0.197976/15.811388 = 0.012521$.
> VaR $= (1.65 \times 0.012521 - 0.000284) \times 500{,}000{,}000 = (0.020660 - 0.000284) \times 500{,}000{,}000 = \text{USD } 10{,}187{,}922$, about USD 10.19 million, up about USD 2.88 million from the lookback figure.
> A long/short book depends on the two books moving together, so the loss came from a correlation that the lookback estimate did not anticipate; this is the correlation-risk limitation of VaR.
> A is wrong because the right-tail limitation concerns ignored gains, whereas the episode is a left-tail loss driven by a correlation shift.
> C is wrong because it repeats the sign error of treating the short book as long: with $+0.80$ the covariance term is $+0.040310$, $\sigma_p = 0.346144$, and VaR $= \text{USD } 17{,}630{,}936$, which wrongly implies that lower correlation reduces the fund's risk from the USD 19.00 million figure.

## Distractor design

1. A: wrong threshold ($z = 1.00$, the 16% VaR, on a 5% question); C: sign error (short book weight entered as positive, so the covariance term and the short book's return are added).
2. A: wrong reference point (decline measured from the starting NAV, not the peak); B: wrong measure (worst single month instead of the defined peak-to-trough decline).
3. B: historical simulation misread as a parameter-based method; C: both statements accepted without checking the historical simulation fingerprint.
4. A: wrong limitation (right tail instead of correlation risk); C: sign error on the short book carried into the stressed correlation.
