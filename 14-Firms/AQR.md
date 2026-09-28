---
type: firm
track: [quant-research, quant-dev]
tier: core
status: draft
firm_type: hedge-fund
focus: [probability-problem-set, statistics-problem-set, linear-regression-ols, hypothesis-testing-and-multiple-comparisons, cross-sectional-factor-models, momentum-mean-reversion-and-carry, point-in-time-data-and-survivorship, backtesting-methodology-and-pitfalls, overfitting-and-deflated-sharpe, performance-metrics-and-fundamental-law, mean-variance-portfolio-construction, covariance-estimation-and-shrinkage, black-litterman-risk-parity-and-hrp, transaction-costs-and-turnover, research-case-studies-and-take-homes]
sources: []
---

# AQR Capital Management

> [!info] Draft
> Facts below were gathered from the sources listed at the end on 2026-09-28.
> Firms change their processes often; verify anything that matters with your recruiter.

## Snapshot

- AQR stands for Applied Quantitative Research.
- It was founded in 1998 by Cliff Asness, David Kabiller, Robert Krail and John Liew, starting with a single multi-strategy hedge fund.
- Headquarters is in Greenwich, Connecticut, where it moved from New York in 2004; other offices are Sydney, London, Hong Kong, Bengaluru, Munich and Dubai.
- The firm offers long-only and alternative strategies spanning equity, macro, arbitrage and multi-strategy, plus tax-aware strategies, mutual funds (from 2009) and UCITS funds (from 2012).
- It describes itself as working at the nexus of economics, behavioural finance, data and technology.
- Its research is best known for systematic style premia; Wikipedia summarises the core styles as value, momentum, defensive and carry, and notes AQR was one of the first managers to offer risk parity.

## Roles

- The Greenwich summer internship lists five teams: Research and Portfolio Management; Portfolio Implementation, Trading and Portfolio Finance; Business Development; Engineering; and Risk.
- Research and Portfolio Management interns work with researchers and portfolio managers on statistical and economic research.
- Portfolio Implementation covers construction, optimisation and management of the systematic portfolios, and trade execution.
- Engineering interns may join client-facing technology, cloud or middle-office teams.
- The internship runs 10 weeks from early June to mid-August; per the firm's page, applications open June 30 and interviews run through September.

## Interview process

> [!warning] Commonly reported, verify with your recruiter
> Round counts and formats vary by role, office and year.

- Candidate reports for quantitative research describe rounds with two interviewers each, mixing finance, programming, mathematics and statistics.
- Given the firm's published research, prepare to discuss why value, momentum, carry and defensive premia might exist and how you would test them; this is preparation advice, not a reported question list.
- Be ready to defend a backtest: data snapshots, look-ahead bias, multiple testing and transaction costs.

## What they test

- Probability and statistics: [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md), [Statistics Problem Set](../02-Statistics-and-Econometrics/14-Statistics-Problem-Set.md), [Linear Regression (OLS)](../02-Statistics-and-Econometrics/04-Linear-Regression-OLS.md), [Hypothesis Testing and Multiple Comparisons](../02-Statistics-and-Econometrics/03-Hypothesis-Testing-and-Multiple-Comparisons.md).
- Factor research: [Cross-Sectional Factor Models](../09-Alpha-Research-and-Portfolio/04-Cross-Sectional-Factor-Models.md), [Momentum, Mean Reversion and Carry](../09-Alpha-Research-and-Portfolio/05-Momentum-Mean-Reversion-and-Carry.md), [Point-in-Time Data and Survivorship](../09-Alpha-Research-and-Portfolio/02-Point-in-Time-Data-and-Survivorship.md).
- Research rigour: [Backtesting Methodology and Pitfalls](../09-Alpha-Research-and-Portfolio/07-Backtesting-Methodology-and-Pitfalls.md), [Overfitting and Deflated Sharpe](../09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md), [Performance Metrics and the Fundamental Law](../09-Alpha-Research-and-Portfolio/09-Performance-Metrics-and-Fundamental-Law.md).
- Portfolio construction: [Mean-Variance Portfolio Construction](../09-Alpha-Research-and-Portfolio/10-Mean-Variance-Portfolio-Construction.md), [Covariance Estimation and Shrinkage](../09-Alpha-Research-and-Portfolio/11-Covariance-Estimation-and-Shrinkage.md), [Black-Litterman, Risk Parity and HRP](../09-Alpha-Research-and-Portfolio/12-Black-Litterman-Risk-Parity-and-HRP.md), [Transaction Costs and Turnover](../09-Alpha-Research-and-Portfolio/13-Transaction-Costs-and-Turnover.md).

## Preparation plan

1. Week 1: run `./qp firms aqr`; work the [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md) and the [Statistics Problem Set](../02-Statistics-and-Econometrics/14-Statistics-Problem-Set.md).
2. Week 2: regression and multiple testing; be able to derive the OLS standard error and explain why a t-statistic of 2 is not enough after many trials.
3. Week 3: factor models and the style premia; for each style, state the risk-based and behavioural explanation and one way it fails.
4. Week 4: backtesting, point-in-time data and the deflated Sharpe ratio; rehearse critiquing a backtest out loud.
5. Week 5: portfolio construction, covariance shrinkage, risk parity and turnover control.
6. Week 6: a timed take-home rehearsal from [Research Case Studies and Take-Homes](../13-Interview-Playbook/08-Research-Case-Studies-and-Take-Homes.md); clear `./qp review --track quant-research`.

## Culture and what they value

- The firm stresses applying rigorous research to its investment process and challenging the status quo.
- Its founders met in the University of Chicago finance PhD programme, and the firm publishes research openly; read a few of its papers before interviewing.
- AQR states it was named a Pensions and Investments Best Place to Work for the ninth year in a row in 2025.

## Senior hire notes

- Senior researchers should expect to discuss their own factor or portfolio research in depth; prepare what you can share without breaching confidentiality.
- Read the pay range on the specific US listing rather than relying on aggregated figures.
- Non-compete terms from your current employer may affect timing; review them with counsel.
- See [Senior-Level Expectations](../13-Interview-Playbook/12-Senior-Level-Expectations.md).

## Sources

- https://www.aqr.com/About-Us/OurFirm (accessed 2026-09-28)
- https://www.aqr.com/Our-Firm/Greenwich-Internships (accessed 2026-09-28)
- https://en.wikipedia.org/wiki/AQR_Capital_Management (accessed 2026-09-28)
- https://www.glassdoor.com/Interview/AQR-Capital-Management-Quantitative-Research-Interview-Questions-EI_IE213435.0,22_KO23,44.htm (accessed 2026-09-28)
