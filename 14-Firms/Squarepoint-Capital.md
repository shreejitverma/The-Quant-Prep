---
type: firm
track: [quant-research, quant-dev]
tier: core
status: draft
firm_type: hedge-fund
focus: [probability-problem-set, statistics-problem-set, linear-regression-ols, hypothesis-testing-and-multiple-comparisons, regression-diagnostics-and-robust-inference, research-case-studies-and-take-homes, signals-features-and-alpha-decay, backtesting-methodology-and-pitfalls, cross-sectional-factor-models, ml-fundamentals-and-generalization, tree-ensembles-and-gradient-boosting, numerical-python-numpy-and-numba, data-structures-and-algorithms-for-quant-interviews]
sources: []
---

# Squarepoint Capital

> [!info] Draft
> Facts below were gathered from the sources listed at the end on 2026-09-27.
> Firms change their processes often; verify anything that matters with your recruiter.

## Snapshot

- Squarepoint describes itself as a global investment manager running a diversified portfolio of systematic and quantitative strategies for clients.
- Its origins go back to nQuant, founded in 2000 inside Lehman Brothers in Tokyo, which moved to Barclays and spun out as the partner-owned Squarepoint in December 2014.
- It is led by its four founding partners.
- The firm says it is present in seventeen cities; its timeline mentions Tokyo, New York, London, Singapore, Montreal, Hong Kong and Bangalore.
- It says it executes millions of trades a day across multiple asset classes.
- Headcount and assets under management are not published on the pages consulted.

## Roles

- Quantitative researcher: develops systematic signals and models within the firm's multi-strategy platform.
- Desk quant or quantitative developer: builds research and trading tooling close to a strategy team; reports suggest more programming and financial intuition in these interviews.
- Software engineer: builds the technology and data platform that Squarepoint calls the enabler between research and trading.

## Interview process

> [!warning] Commonly reported, verify with your recruiter
> Round counts and formats vary by role, office and year.

- Candidate reports commonly describe early technical rounds with algorithmic coding, a probability question and statistics on regression and hypothesis testing.
- A distinctive reported element for junior researchers is a long onsite data exercise: build a predictive model on a provided dataset, then present it to a researcher.
- Final rounds reportedly include a more finance-oriented conversation with a senior researcher.
- The process is often described as more practical and less puzzle-heavy than some prop trading firms.

## What they test

- Probability and statistics: [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md), [Statistics Problem Set](../02-Statistics-and-Econometrics/14-Statistics-Problem-Set.md), [Linear Regression (OLS)](../02-Statistics-and-Econometrics/04-Linear-Regression-OLS.md), [Regression Diagnostics](../02-Statistics-and-Econometrics/05-Regression-Diagnostics-and-Robust-Inference.md), [Hypothesis Testing](../02-Statistics-and-Econometrics/03-Hypothesis-Testing-and-Multiple-Comparisons.md).
- The data exercise: [Research Case Studies and Take-Homes](../13-Interview-Playbook/08-Research-Case-Studies-and-Take-Homes.md), [ML Fundamentals](../10-Machine-Learning-for-Finance/01-ML-Fundamentals-and-Generalization.md), [Tree Ensembles and Gradient Boosting](../10-Machine-Learning-for-Finance/03-Tree-Ensembles-and-Gradient-Boosting.md), [Numerical Python](../12-Quant-Development/11-Numerical-Python-NumPy-and-Numba.md).
- Systematic research judgement: [Signals, Features and Alpha Decay](../09-Alpha-Research-and-Portfolio/03-Signals-Features-and-Alpha-Decay.md), [Backtesting Methodology and Pitfalls](../09-Alpha-Research-and-Portfolio/07-Backtesting-Methodology-and-Pitfalls.md), [Cross-Sectional Factor Models](../09-Alpha-Research-and-Portfolio/04-Cross-Sectional-Factor-Models.md).
- Coding: [Data Structures and Algorithms](../12-Quant-Development/05-Data-Structures-and-Algorithms-for-Quant-Interviews.md).

## Preparation plan

1. Week 1: run `./qp firms squarepoint-capital`; work the [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md).
2. Week 2: regression and inference, ending with the [Statistics Problem Set](../02-Statistics-and-Econometrics/14-Statistics-Problem-Set.md).
3. Week 3: two timed practice data exercises of several hours each, following [Research Case Studies and Take-Homes](../13-Interview-Playbook/08-Research-Case-Studies-and-Take-Homes.md), then present each result aloud.
4. Week 4: [Signals, Features and Alpha Decay](../09-Alpha-Research-and-Portfolio/03-Signals-Features-and-Alpha-Decay.md) and [Backtesting Methodology and Pitfalls](../09-Alpha-Research-and-Portfolio/07-Backtesting-Methodology-and-Pitfalls.md).
5. Week 5: medium-level coding problems; clear `./qp review --track quant-research` and `./qp mark <id> 3` as topics firm up.

## Culture and what they value

- Squarepoint describes collaboration across all teams and a culture of ownership and accountability.
- It presents technology as the integration layer between research and trading.

## Senior hire notes

- Experienced researchers should expect scrutiny of prior strategies' performance and robustness; prepare what you can share without breaching confidentiality.
- Non-compete and garden-leave terms, especially in the UK and Europe, can be long; review your contract with counsel.
- See [Senior-Level Expectations](../13-Interview-Playbook/12-Senior-Level-Expectations.md).

## Sources

- https://www.squarepoint-capital.com/ (accessed 2026-09-27)
- https://www.squarepoint-capital.com/about (accessed 2026-09-27)
- https://www.glassdoor.com/Interview/Squarepoint-Capital-Junior-Quant-Researcher-Interview-Questions-EI_IE1442647.0,19_KO20,43.htm (accessed 2026-09-27)
