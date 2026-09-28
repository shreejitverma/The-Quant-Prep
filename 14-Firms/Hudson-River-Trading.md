---
type: firm
track: [quant-trader, quant-research, quant-dev]
tier: core
status: draft
firm_type: hft
focus: [cpp-for-trading-systems, low-latency-engineering, concurrency-lock-free-and-memory-pools, data-structures-and-algorithms-for-quant-interviews, coding-interviews-for-quants, system-design-for-trading, market-data-feed-handlers-and-protocols, probability-problem-set, expectation-variance-and-linearity, linear-regression-ols, signals-features-and-alpha-decay, limit-order-books-and-order-types, order-book-imbalance-and-microprice, backtesting-methodology-and-pitfalls]
sources: []
---

# Hudson River Trading

> [!info] Draft
> Facts below were gathered from the sources listed at the end on 2026-09-28.
> Firms change their processes often; verify anything that matters with your recruiter.

## Snapshot

- Hudson River Trading (HRT) is an algorithmic and quantitative trading firm that researches and develops automated trading algorithms using "advanced mathematical techniques".
- It was founded in 2002 by partners with computer science and mathematics degrees from Harvard and MIT.
- It describes itself as multi-asset and trading on "nearly all of the world's electronic markets".
- It also lists client-facing businesses: a US Single Dealer Platform and a European Systematic Internaliser (both 2018) and Client Market Making (2022).
- Its site lists 14 offices, including New York, Chicago, Austin, London, Dublin, Singapore, Hong Kong and Mumbai, and "over a thousand" employees.
- HRT describes itself as "built by coders, led by coders".

## Roles

- Algorithm developer (quant research and trading): builds and maintains the models that drive trading, using math, statistics, data analysis and C++ or Python programming to research, backtest and monitor strategies.
- Algo engineer or software engineer: builds the trading systems and works alongside algorithm developers to test and deploy strategies; the careers site lists C++ and Python engineering tracks.
- Hardware engineer and systems and networking engineer: build the low-latency hardware, network and infrastructure.
- Student routes cover full-time and internship roles for undergraduates, master's and PhD students.

## Interview process

> [!warning] Commonly reported, verify with your recruiter
> Round counts and formats vary by role, office and year.

- For software engineers, HRT's own blog describes a timed take-home test, roughly two phone interviews, and a full day of onsite interviews that may be virtual.
- Per that post, phone rounds include a technical discussion (systems knowledge, data structures or problem solving) and a programming round in C++, Python or the candidate's language of choice, depending on role.
- The onsite, per HRT, assesses programming skill, systems knowledge such as "memory, I/O, process management", and problem solving on unfamiliar problems.
- HRT says each stage uses a standardised question set for the season and that needing hints or making mistakes is acceptable.
- Algorithm developer candidates commonly report probability and statistics questions, a coding screen, and data or modelling problems in later rounds.

## What they test

- Engineering depth: [C++ for Trading Systems](../12-Quant-Development/02-Cpp-for-Trading-Systems.md), [Low-Latency Engineering](../12-Quant-Development/03-Low-Latency-Engineering.md), [Concurrency, Lock-Free and Memory Pools](../12-Quant-Development/04-Concurrency-Lock-Free-and-Memory-Pools.md), [Market Data Feed Handlers and Protocols](../12-Quant-Development/08-Market-Data-Feed-Handlers-and-Protocols.md).
- Coding and design: [Data Structures and Algorithms](../12-Quant-Development/05-Data-Structures-and-Algorithms-for-Quant-Interviews.md), [Coding Interviews for Quants](../13-Interview-Playbook/07-Coding-Interviews-for-Quants.md), [System Design for Trading](../12-Quant-Development/06-System-Design-for-Trading.md).
- Probability and statistics for algorithm developers: [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md), [Expectation, Variance and Linearity](../01-Probability/04-Expectation-Variance-and-Linearity.md), [Linear Regression (OLS)](../02-Statistics-and-Econometrics/04-Linear-Regression-OLS.md).
- Short-horizon research: [Limit Order Books and Order Types](../07-Market-Microstructure/01-Limit-Order-Books-and-Order-Types.md), [Order Book Imbalance and Microprice](../07-Market-Microstructure/11-Order-Book-Imbalance-and-Microprice.md), [Signals, Features and Alpha Decay](../09-Alpha-Research-and-Portfolio/03-Signals-Features-and-Alpha-Decay.md), [Backtesting Methodology and Pitfalls](../09-Alpha-Research-and-Portfolio/07-Backtesting-Methodology-and-Pitfalls.md).

## Preparation plan

1. Week 1: run `./qp firms hudson-river-trading`; read HRT's own interview-preparation post and pick your interview language.
2. Week 2: timed algorithm practice from [Data Structures and Algorithms](../12-Quant-Development/05-Data-Structures-and-Algorithms-for-Quant-Interviews.md), testing your code thoroughly as the take-home rewards correctness.
3. Week 3 (engineers): systems depth, [C++ for Trading Systems](../12-Quant-Development/02-Cpp-for-Trading-Systems.md) and [Low-Latency Engineering](../12-Quant-Development/03-Low-Latency-Engineering.md), including memory, I/O and process management.
4. Week 3 (algorithm developers): [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md) and [Linear Regression (OLS)](../02-Statistics-and-Econometrics/04-Linear-Regression-OLS.md).
5. Week 4: [System Design for Trading](../12-Quant-Development/06-System-Design-for-Trading.md) or [Order Book Imbalance and Microprice](../07-Market-Microstructure/11-Order-Book-Imbalance-and-Microprice.md) depending on role; practise thinking aloud, since HRT says it values communication.
6. Week 5: mock onsite day with a partner; clear `./qp review --track quant-dev` or `--track quant-research`.

## Culture and what they value

- HRT emphasises "a foundation of collaboration and openness" and a "culture of sharing".
- Its research page describes "a meritocratic, low-politics culture" where researchers spend nearly all their time on research.
- Its interview advice names collaboration, teachability, communication, and honesty and integrity as things it looks for.

## Senior hire notes

- HRT runs a separate experienced-talent route on its careers site.
- Experienced engineers should expect the same coding and systems bar, plus deeper discussion of systems they have built and the performance trade-offs they made.
- Experienced researchers should expect detailed questions on past strategies; keep a prior employer's proprietary details out of the conversation.
- Non-compete and garden-leave terms are common in HFT and vary by jurisdiction; check your contract before agreeing a start date.
- See [Senior-Level Expectations](../13-Interview-Playbook/12-Senior-Level-Expectations.md).

## Sources

- https://www.hudsonrivertrading.com/about/ (accessed 2026-09-28)
- https://www.hudsonrivertrading.com/careers/ (accessed 2026-09-28)
- https://www.hudsonrivertrading.com/hrtbeat/interview-at-hrt/ (accessed 2026-09-28)
- https://www.hudsonrivertrading.com/hrtbeat/engineering-and-interviewing-at-hrt/ (accessed 2026-09-28)
- https://www.hudsonrivertrading.com/hrt-job/algorithm-developer-quant-researcher-2026-phds/ (accessed 2026-09-28)
