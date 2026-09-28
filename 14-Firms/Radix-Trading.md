---
type: firm
track: [quant-research, quant-dev]
tier: core
status: draft
firm_type: hft
focus: [probability-problem-set, statistics-problem-set, brainteasers-and-puzzles, signals-features-and-alpha-decay, order-book-imbalance-and-microprice, limit-order-books-and-order-types, latency-arbitrage-and-speed, ml-fundamentals-and-generalization, cpp-for-trading-systems, low-latency-engineering, concurrency-lock-free-and-memory-pools, data-structures-and-algorithms-for-quant-interviews, system-design-for-trading]
sources: []
---

# Radix Trading

> [!info] Draft
> Facts below were gathered from the sources listed at the end on 2026-09-27.
> Firms change their processes often; verify anything that matters with your recruiter.

## Snapshot

- Radix calls itself "a research firm powered by technology and monetized through trading", using statistical research and machine learning rather than competing on speed alone.
- It is privately funded and does not accept external investment.
- Offices are in Chicago, New York and Amsterdam, and it trades electronic markets in North America, Europe and Asia.
- Wikipedia states it was founded in 2012 by Benjamin Blander and Michael Rauchman; verify against a primary source.
- Headcount is not published on the pages consulted.

## Roles

- Quantitative researcher: statistical and ML research on market data to build trading strategies; Radix says its researchers include PhDs, postdocs and professors.
- Quantitative technologist or software engineer: builds the automated research platform and trading systems; Radix says it hires engineers from major tech companies and supercomputer specialists.

## Interview process

> [!warning] Commonly reported, verify with your recruiter
> Round counts and formats vary by role, office and year.
> Public reports on Radix are sparse.

- Candidate reports commonly describe online tests, then one or two live technical interviews with a researcher or engineer, then a final round.
- Researcher reports mention probability and statistics questions and, in some cases, a data take-home on market data.
- Engineer reports stress C++ depth, including the memory model, cache behaviour and performance reasoning, alongside algorithms and system design.

## What they test

- Probability and statistics: [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md), [Statistics Problem Set](../02-Statistics-and-Econometrics/14-Statistics-Problem-Set.md), [Brainteasers and Puzzles](../13-Interview-Playbook/03-Brainteasers-and-Puzzles.md).
- Short-horizon research: [Limit Order Books](../07-Market-Microstructure/01-Limit-Order-Books-and-Order-Types.md), [Order Book Imbalance and Microprice](../07-Market-Microstructure/11-Order-Book-Imbalance-and-Microprice.md), [Latency Arbitrage and Speed](../07-Market-Microstructure/10-Latency-Arbitrage-and-Speed.md), [Signals, Features and Alpha Decay](../09-Alpha-Research-and-Portfolio/03-Signals-Features-and-Alpha-Decay.md), [ML Fundamentals](../10-Machine-Learning-for-Finance/01-ML-Fundamentals-and-Generalization.md).
- Engineering: [C++ for Trading Systems](../12-Quant-Development/02-Cpp-for-Trading-Systems.md), [Low-Latency Engineering](../12-Quant-Development/03-Low-Latency-Engineering.md), [Concurrency, Lock-Free and Memory Pools](../12-Quant-Development/04-Concurrency-Lock-Free-and-Memory-Pools.md), [Data Structures and Algorithms](../12-Quant-Development/05-Data-Structures-and-Algorithms-for-Quant-Interviews.md), [System Design for Trading](../12-Quant-Development/06-System-Design-for-Trading.md).

## Preparation plan

1. Week 1: run `./qp firms radix-trading`; work the [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md) and the [Statistics Problem Set](../02-Statistics-and-Econometrics/14-Statistics-Problem-Set.md).
2. Week 2 (researchers): order-book signals, [Order Book Imbalance and Microprice](../07-Market-Microstructure/11-Order-Book-Imbalance-and-Microprice.md) and [Signals, Features and Alpha Decay](../09-Alpha-Research-and-Portfolio/03-Signals-Features-and-Alpha-Decay.md); (engineers) [C++ for Trading Systems](../12-Quant-Development/02-Cpp-for-Trading-Systems.md).
3. Week 3: researchers do a timed tick-data exercise; engineers do [Low-Latency Engineering](../12-Quant-Development/03-Low-Latency-Engineering.md) and [Concurrency, Lock-Free and Memory Pools](../12-Quant-Development/04-Concurrency-Lock-Free-and-Memory-Pools.md).
4. Week 4: algorithms under time pressure from [Data Structures and Algorithms](../12-Quant-Development/05-Data-Structures-and-Algorithms-for-Quant-Interviews.md); engineers add [System Design for Trading](../12-Quant-Development/06-System-Design-for-Trading.md).
5. Week 5: clear `./qp review` and `./qp mark <id> 3` for topics you can explain from first principles.

## Culture and what they value

- Radix emphasises openness and "research through open, collaborative innovation", with fast idea-to-execution cycles.
- It describes a mix of academics and experienced engineers, and recruits both from universities and industry.

## Senior hire notes

- Radix actively recruits experienced professionals; expect deep technical probing of past systems or research.
- HFT firms commonly use non-compete agreements; review your current terms with counsel before accepting.
- Be precise about what you can share from prior employers' strategies and code.
- See [Senior-Level Expectations](../13-Interview-Playbook/12-Senior-Level-Expectations.md).

## Sources

- https://www.radixtrading.com/ (accessed 2026-09-27)
- https://en.wikipedia.org/wiki/Radix_Trading (accessed 2026-09-27)
- https://www.glassdoor.com/Interview/Radix-Trading-Interview-Questions-E1681590.htm (accessed 2026-09-27)
