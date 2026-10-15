---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 6
title: "Kestrel Provincial Pension Plan: Reviewing a Manager Backtest"
los: [los-09-06-a, los-09-06-b, los-09-06-c, los-09-06-d]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Kestrel Provincial Pension Plan: Reviewing a Manager Backtest

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Amelie Fortin, CFA, is a senior analyst at the Kestrel Provincial Pension Plan, a Canadian defined benefit plan with CAD 41 billion in assets.
The plan is considering a CAD 600 million allocation to Harrowgate Quantitative Partners, an external manager that runs long-short factor strategies in Canadian equities.
Harrowgate has submitted backtests of three strategies, and Fortin must recommend to the investment committee whether any of them should be funded.

Harrowgate describes its process as follows.
The investment universe for every strategy is the list of companies that were constituents of the S&P/TSX Composite Index on 31 December 2024, and that list is applied to the entire backtest period of January 1995 to December 2024 (360 months).
Portfolios are rebalanced monthly, and transaction costs of 12 basis points per side are deducted.
Each strategy is a long-short hedged quintile portfolio with equally weighted stocks in each quintile.

- The Low-Vol LS strategy ranks stocks by the standard deviation of their trailing 36 monthly returns, buys the lowest-volatility quintile, and shorts the highest-volatility quintile.
- The Quality LS strategy ranks stocks by return on equity and accruals, using fundamentals from a vendor database that stores each company's latest restated financial history; no reporting lag is applied.
- The Blend strategy combines Low-Vol LS and Quality LS with weights set so that each contributes equally to portfolio risk.

To illustrate its procedure, Harrowgate notes that the Low-Vol LS portfolio formed on 30 June 2019 was built from trailing volatility estimates, and its performance was then recorded for the following period before the portfolio was re-formed.

Exhibit 1: Harrowgate backtest statistics, January 1995 to December 2024 (monthly figures)

| Statistic | Low-Vol LS | Quality LS | Blend |
|---|---|---|---|
| Mean monthly return | 0.42% | 0.55% | 0.47% |
| Monthly standard deviation | 1.10% | 1.85% | 1.05% |
| Skewness | 0.35 | -1.20 | -0.10 |
| Kurtosis | 4.10 | 9.60 | 4.80 |
| VaR (95%) | -1.45% | -2.60% | -1.30% |
| CVaR (95%) | -2.05% | -6.10% | -2.35% |
| Maximum drawdown | 14.8% | 31.5% | 12.6% |
| Average annual turnover | 310% | 145% | 220% |

Harrowgate reports Sharpe ratios using annualized return divided by annualized volatility, with no risk-free deduction, because the long-short portfolios are self-financing.
The average Canadian Treasury bill yield over the period was 2.3%.
Fortin annualizes monthly means by multiplying by 12 and monthly standard deviations by multiplying by the square root of 12.

At the committee's pre-meeting, trustee Raymond Okafor comments: "If Harrowgate's backtested Sharpe ratio clears our 0.75 hurdle, the strategy will beat its benchmark once we fund it."
Fortin replies: "The backtest is our acceptance or rejection screen.
It approximates how the strategy would have been run on historical data, and its value depends on the future resembling the past at least to some degree."

Fortin's own review raises two concerns.
First, she notes that many small, volatile TSX companies were delisted between 1995 and 2024 through bankruptcy, takeover, or index deletion.
Second, she observes that the Quality LS signal on each rebalancing date uses financial statements that Canadian companies typically file four to six weeks after quarter-end, and that some of those figures were later restated.

## Questions

1. Whose statement about the role of backtesting is most accurate? (LOS: los-09-06-a)
   - A. Okafor's statement only.
   - B. Fortin's statement only.
   - C. Both Okafor's and Fortin's statements.
2. For the Low-Vol LS portfolio formed on 30 June 2019, the in-sample estimation window and the out-of-sample month are most likely: (LOS: los-09-06-b)
   - A. July 2016 to June 2019 in-sample; July 2019 out-of-sample.
   - B. July 2016 to June 2019 in-sample; June 2019 out-of-sample.
   - C. August 2016 to July 2019 in-sample; July 2019 out-of-sample.
3. Using Harrowgate's reporting convention, the annualized Sharpe ratio of the Quality LS strategy is closest to: (LOS: los-09-06-c)
   - A. 0.30.
   - B. 1.03.
   - C. 3.57.
4. Which conclusion about Exhibit 1 is most accurate? (LOS: los-09-06-c)
   - A. Quality LS offers the best risk-adjusted performance, because it has the highest mean monthly return.
   - B. The skewness and kurtosis of Quality LS indicate that its return surprises are more likely to be positive than negative.
   - C. Low-Vol LS has the smallest downside risk measured by the average loss in the worst 5% of months, even though Blend has the smallest VaR and maximum drawdown.
5. Given Fortin's first concern, Harrowgate's universe definition most likely causes the backtested performance of the Low-Vol LS strategy to be: (LOS: los-09-06-d)
   - A. overstated, because survivorship bias removes the delisted losers that the strategy would have held long.
   - B. understated, because survivorship bias removes the delisted high-volatility losers that the strategy would have held short.
   - C. unaffected, because survivorship bias affects only fundamental signals such as Quality LS.
6. The most appropriate remedy for Fortin's second concern is to: (LOS: los-09-06-d)
   - A. rebuild Quality LS on point-in-time fundamentals or, if they are unavailable, apply a reporting lag of about one to two months.
   - B. require the Quality LS strategy to clear a t-statistic hurdle of 3.0 instead of 2.0.
   - C. replace the rolling-window backtest with a bootstrapped historical simulation of Quality LS returns.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Backtesting approximates the real-life investment process with historical data to assess a strategy's risk-return trade-off, and managers use it as an acceptance or rejection criterion.
> Its implicit assumption is that the future will at least somewhat resemble the past, which is what Fortin says.
> A good backtest does not guarantee future excess returns, so Okafor's statement is wrong.
> A is wrong because it treats a passed backtest as a guarantee of live outperformance.
> C is wrong because it endorses Okafor's guarantee along with Fortin's correct description.
> 2. **A.** A rolling window calibrates on data available at the formation date and records the next period out of sample.
> The 36 monthly returns available on 30 June 2019 are July 2016 through June 2019 (12 x 3 = 36 months ending in June 2019), and the portfolio's result is recorded for July 2019.
> B is wrong because June 2019 is inside the estimation window; recording it as the out-of-sample month tests the portfolio on data used to build it.
> C is wrong because an estimation window ending in July 2019 uses returns that were not known on 30 June 2019, which is look-ahead bias in the procedure.
> 3. **B.** Annualized return $= 0.55 \times 12 = 6.6000\%$.
> Annualized volatility $= 1.85 \times \sqrt{12} = 1.85 \times 3.4641 = 6.4086\%$.
> Sharpe ratio $= 6.6000 / 6.4086 = 1.0299$, or about 1.03.
> The 2.3% Treasury bill yield is not deducted, because Harrowgate reports self-financing long-short Sharpe ratios as return over volatility.
> A is wrong because it leaves the ratio monthly, $0.55/1.85 = 0.2973$; annualizing the standard deviation by 12 instead of $\sqrt{12}$ gives the same figure, $6.60/22.20 = 0.2973$.
> C is wrong because it annualizes the mean but leaves the standard deviation monthly: $6.60/1.85 = 3.5676$.
> 4. **C.** CVaR (95%) is the average of the losses beyond the VaR threshold, that is, the average loss in the worst 5% of months.
> Low-Vol LS has the smallest CVaR loss (-2.05% against -2.35% for Blend and -6.10% for Quality LS), while Blend has the smallest VaR (-1.30%) and the smallest maximum drawdown (12.6%), so the rankings depend on which downside measure is used.
> A is wrong because it ranks by mean return rather than risk-adjusted return: the annualized Sharpe ratios are Quality LS $6.60/6.4086 = 1.0299$, Low-Vol LS $5.04/3.8105 = 1.3227$ and Blend $5.64/3.6373 = 1.5506$, so Quality LS is last, not first.
> B is wrong because negative skewness (-1.20) with kurtosis well above 3.0 (9.60) means extreme outcomes are more likely than under the normal distribution and are more likely to be negative.
> 5. **B.** Using the end-2024 constituent list for the whole period is survivorship bias, a special case of look-ahead bias.
> The firms that disappeared were disproportionately small, volatile companies that failed, and those high-volatility stocks sit in the short quintile of Low-Vol LS.
> Removing the short positions that would have collapsed makes the high-volatility short leg look stronger than it really was, so the long-short spread is understated.
> This is the module's low-volatility anomaly result, where the survivor universe flips the result in favour of high-volatility stocks.
> A is wrong because it puts the delisted losers in the long leg; low-volatility stocks are the long leg, and the delisted blowups are high-volatility names.
> C is wrong because survivorship bias affects any strategy built on a survivor universe, whatever the signal.
> 6. **A.** Using restated fundamentals on dates before they were filed is look-ahead bias.
> The fix is point-in-time data; when it is unavailable, a reporting lag is applied, and the lag that best replicates point-in-time results for Canada is about one to two months.
> B is wrong because a higher t-statistic hurdle addresses data snooping (multiple testing), not the use of information that was unavailable at the decision date.
> C is wrong because a historical simulation resamples the same biased returns, so it inherits the look-ahead bias instead of removing it.

## Distractor design

1. A: backtest treated as a guarantee of live excess return; C: the guarantee accepted along with the correct objective.
2. B: out-of-sample month placed inside the in-sample window; C: estimation window shifted forward one month (look-ahead in the rolling window).
3. A: monthly ratio not annualized (or volatility annualized by 12); C: mean annualized but volatility left monthly.
4. A: ranked by mean return instead of Sharpe ratio; B: sign of skewness misread.
5. A: delisted losers assigned to the wrong leg of the long-short portfolio; C: survivorship bias wrongly restricted to fundamental signals.
6. B: data-snooping fix applied to a look-ahead problem; C: resampling mistaken for a bias fix.
