---
type: firm
track: [quant-trader, quant-research, quant-dev]
tier: core
status: draft
firm_type: hft
focus: [random-variables-and-distributions, expectation-variance-and-linearity, hypothesis-testing-and-multiple-comparisons, linear-regression-ols, signals-features-and-alpha-decay, backtesting-methodology-and-pitfalls, limit-order-books-and-order-types, order-book-imbalance-and-microprice, numerical-python-numpy-and-numba, cpp-for-trading-systems, low-latency-engineering, data-structures-and-algorithms-for-quant-interviews, system-design-for-trading]
sources: []
---

# Tower Research Capital

> [!info] Draft
> Facts below were gathered from the sources listed at the end on 2026-09-28.
> Firms change their processes often; verify anything that matters with your recruiter.

## Snapshot

- Tower Research Capital is a quantitative trading firm founded in 1998 by Mark Gorton, who is listed as chairman.
- It describes itself as "a team of teams": "dozens of trading and research pods" build strategies independently on a shared platform.
- The central platform provides market access, data, research, compute infrastructure, risk management and compliance.
- It says its teams trade "across any time horizon, any market, and any asset class".
- Its business areas include Quantitative Trading, Engineering, Liquidity Provision and Ventures.
- Headcount and office count are not published on the pages consulted.

## Roles

- Quantitative trader inside a trading team: designs, implements and deploys trading algorithms, analyses market data, builds pattern-detection tools and writes production code; Tower's quant-internship page describes this work.
- Quantitative researcher: builds models and signals inside a trading team.
- Core engineering: builds the shared platform, including machine learning, low-latency systems and trading infrastructure; Tower says engineering runs "more like a software company", with the trading teams as clients.
- Because teams are semi-independent, the tools, style and horizon of a quant role depend heavily on which team hires you.

## Interview process

> [!warning] Commonly reported, verify with your recruiter
> Round counts and formats vary by team, role and year.

- Tower's careers page says it aims for a straightforward process with "no gotcha questions, random logic problems, or abstract, overly academic discussions".
- It describes interviews as "a thoughtful conversation to learn more about you, your past roles, and what you can achieve at Tower".
- For quantitative traders, Tower's own guidance says to be fluent in probability and statistics basics (distributions, expectation, variance, interpreting noisy results) and to program in C++, Python or R.
- Candidate reports commonly describe a coding assessment, technical interviews with members of the hiring team, and a final round; team-specific loops vary.
- Engineering candidates report C++, systems and algorithm questions.

## What they test

- Probability and statistics basics, per Tower's own guidance: [Random Variables and Distributions](../01-Probability/03-Random-Variables-and-Distributions.md), [Expectation, Variance and Linearity](../01-Probability/04-Expectation-Variance-and-Linearity.md), [Hypothesis Testing and Multiple Comparisons](../02-Statistics-and-Econometrics/03-Hypothesis-Testing-and-Multiple-Comparisons.md), [Linear Regression (OLS)](../02-Statistics-and-Econometrics/04-Linear-Regression-OLS.md).
- Research: [Signals, Features and Alpha Decay](../09-Alpha-Research-and-Portfolio/03-Signals-Features-and-Alpha-Decay.md), [Backtesting Methodology and Pitfalls](../09-Alpha-Research-and-Portfolio/07-Backtesting-Methodology-and-Pitfalls.md).
- Microstructure: [Limit Order Books and Order Types](../07-Market-Microstructure/01-Limit-Order-Books-and-Order-Types.md), [Order Book Imbalance and Microprice](../07-Market-Microstructure/11-Order-Book-Imbalance-and-Microprice.md).
- Programming: [Numerical Python](../12-Quant-Development/11-Numerical-Python-NumPy-and-Numba.md), [C++ for Trading Systems](../12-Quant-Development/02-Cpp-for-Trading-Systems.md), [Low-Latency Engineering](../12-Quant-Development/03-Low-Latency-Engineering.md), [Data Structures and Algorithms](../12-Quant-Development/05-Data-Structures-and-Algorithms-for-Quant-Interviews.md), [System Design for Trading](../12-Quant-Development/06-System-Design-for-Trading.md).

## Preparation plan

1. Week 1: run `./qp firms tower-research-capital`; ask which team is hiring and what horizon and markets it trades.
2. Week 2: probability and statistics basics, [Expectation, Variance and Linearity](../01-Probability/04-Expectation-Variance-and-Linearity.md) and [Hypothesis Testing](../02-Statistics-and-Econometrics/03-Hypothesis-Testing-and-Multiple-Comparisons.md); practise judging whether a noisy result is real.
3. Week 3: [Signals, Features and Alpha Decay](../09-Alpha-Research-and-Portfolio/03-Signals-Features-and-Alpha-Decay.md) and [Order Book Imbalance and Microprice](../07-Market-Microstructure/11-Order-Book-Imbalance-and-Microprice.md).
4. Week 4: production-quality coding in Python and C++; engineers add [Low-Latency Engineering](../12-Quant-Development/03-Low-Latency-Engineering.md) and [System Design for Trading](../12-Quant-Development/06-System-Design-for-Trading.md).
5. Week 5: prepare a clear walk-through of your past work, since Tower frames interviews as a conversation about it; clear `./qp review`.

## Culture and what they value

- Tower lists its values as excellence, respect, innovation, integrity and teamwork.
- Its careers page asks for "entrepreneurial spirit", clear communication and "calm and focus when the unexpected occurs".
- It describes trading teams as working in a "results-oriented environment" with autonomy on a shared platform.
- A Tower essay argues that humility beats genius in quant work.

## Senior hire notes

- Tower says it hires "the world's best quantitative traders and systematic portfolio managers", so experienced teams and individuals can join as their own pod on the platform.
- Senior candidates should expect a detailed conversation about past roles and results; keep a prior employer's proprietary strategies and code out of it.
- Ask how P&L, costs and platform charges are shared with your team, and what the team's risk limits are.
- Non-compete and garden-leave terms are common in HFT and vary by jurisdiction; check your contract.
- See [Senior-Level Expectations](../13-Interview-Playbook/12-Senior-Level-Expectations.md).

## Sources

- https://tower-research.com/ (accessed 2026-09-28)
- https://tower-research.com/about-us/ (accessed 2026-09-28)
- https://tower-research.com/careers/ (accessed 2026-09-28)
- https://tower-research.com/quant-internships-quant-trading-vs-quant-research-vs-quant-engineering/ (accessed 2026-09-28)
- https://tower-research.com/engineering/ (accessed 2026-09-28)
- https://tower-research.com/the-myth-of-the-quant-god-why-humility-beats-genius/ (accessed 2026-09-28)
