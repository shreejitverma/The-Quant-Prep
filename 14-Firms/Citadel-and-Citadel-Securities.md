---
type: firm
track: [quant-trader, quant-research, quant-dev]
tier: core
status: draft
firm_type: hedge-fund
focus: [probability-problem-set, statistics-problem-set, linear-regression-ols, hypothesis-testing-and-multiple-comparisons, backtesting-methodology-and-pitfalls, signals-features-and-alpha-decay, options-market-making, the-greeks, limit-order-books-and-order-types, market-making-fundamentals, data-structures-and-algorithms-for-quant-interviews, cpp-for-trading-systems, low-latency-engineering, system-design-for-trading]
sources: []
---

# Citadel and Citadel Securities

> [!info] Draft
> Facts below were gathered from the sources listed at the end on 2026-09-27.
> Firms change their processes often; verify anything that matters with your recruiter.

## Snapshot

- These are two separate firms founded by Ken Griffin: Citadel, a multi-strategy hedge fund, and Citadel Securities, a market maker.
- Citadel invests client capital across five strategy businesses: Equities, Fixed Income and Macro, Commodities, Credit and Convertibles, and Global Quantitative Strategies (GQS).
- Citadel Securities makes markets in equities, options, fixed income and FX; its site describes it as the largest US options market maker and a leading provider of equities liquidity.
- Both firms moved their headquarters from Chicago to Miami, announced in 2022.
- Headcount figures in public sources conflict, so none is given here.

## Roles

- Citadel quantitative researcher: builds signals and portfolio models, often inside GQS or embedded with fundamental teams.
- Citadel Securities quantitative researcher and trader: builds pricing, quoting and hedging models for market making and runs the resulting risk.
- Software engineer (both firms): builds low-latency trading platforms, research infrastructure and data systems.
- Citadel's campus engineering interviews are run jointly, so one process can lead to either firm.

## Interview process

> [!warning] Commonly reported, verify with your recruiter
> Round counts and formats vary by role, office and year.

- Citadel and Citadel Securities publish campus interview guides for quantitative research and for engineering.
- The published quantitative research process has four steps and begins with a remote video interview that uses a shared coding pad.
- The first technical screen, as described in those guides and candidate reports, mixes maths, probability and a small programming task; later rounds are several hour-long technical and behavioural interviews.
- Research candidates also report statistics questions about evaluating a trading strategy.
- The engineering guide describes a four-step process that it says usually takes about eight weeks.
- Experienced trader and PM hiring is usually via headhunters and differs substantially from campus loops.

## What they test

- Probability and statistics: [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md), [Statistics Problem Set](../02-Statistics-and-Econometrics/14-Statistics-Problem-Set.md), [Linear Regression (OLS)](../02-Statistics-and-Econometrics/04-Linear-Regression-OLS.md), [Hypothesis Testing](../02-Statistics-and-Econometrics/03-Hypothesis-Testing-and-Multiple-Comparisons.md).
- Evaluating strategies: [Backtesting Methodology and Pitfalls](../09-Alpha-Research-and-Portfolio/07-Backtesting-Methodology-and-Pitfalls.md), [Signals, Features and Alpha Decay](../09-Alpha-Research-and-Portfolio/03-Signals-Features-and-Alpha-Decay.md).
- Market making (Citadel Securities): [Market Making Fundamentals](../08-Market-Making/01-Market-Making-Fundamentals.md), [Options Market Making](../08-Market-Making/07-Options-Market-Making.md), [The Greeks](../05-Derivatives-and-Volatility/05-The-Greeks.md), [Limit Order Books](../07-Market-Microstructure/01-Limit-Order-Books-and-Order-Types.md).
- Engineering: [Data Structures and Algorithms](../12-Quant-Development/05-Data-Structures-and-Algorithms-for-Quant-Interviews.md), [C++ for Trading Systems](../12-Quant-Development/02-Cpp-for-Trading-Systems.md), [Low-Latency Engineering](../12-Quant-Development/03-Low-Latency-Engineering.md), [System Design for Trading](../12-Quant-Development/06-System-Design-for-Trading.md).

## Preparation plan

1. Week 1: run `./qp firms citadel-and-citadel-securities`; work the [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md) with `./qp drill arith` for warm-up.
2. Week 2: statistics depth, [Linear Regression (OLS)](../02-Statistics-and-Econometrics/04-Linear-Regression-OLS.md) and the [Statistics Problem Set](../02-Statistics-and-Econometrics/14-Statistics-Problem-Set.md).
3. Week 3 (researchers): [Backtesting Methodology and Pitfalls](../09-Alpha-Research-and-Portfolio/07-Backtesting-Methodology-and-Pitfalls.md) and [Overfitting and Deflated Sharpe](../09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md); (Citadel Securities) [Options Market Making](../08-Market-Making/07-Options-Market-Making.md).
4. Week 4: timed coding practice from [Coding Interviews for Quants](../13-Interview-Playbook/07-Coding-Interviews-for-Quants.md); engineers add [C++ for Trading Systems](../12-Quant-Development/02-Cpp-for-Trading-Systems.md).
5. Week 5: engineers do [System Design for Trading](../12-Quant-Development/06-System-Design-for-Trading.md); everyone rehearses project deep dives and [Behavioral and Fit](../13-Interview-Playbook/09-Behavioral-and-Fit.md).
6. Week 6: clear `./qp review` and `./qp mark <id> 3` the topics you can now teach.

## Culture and what they value

- The published interview guides describe technical interviews as challenging and oriented to practical problem solving.
- Interviewers also ask why you are interested in the firm and about past projects and internships.
- The firms are widely reported as high-performance, high-accountability environments; judge fit from conversations with current staff.

## Senior hire notes

- Multi-strategy hedge funds commonly assess experienced PMs and researchers on a verifiable track record, capacity and risk-adjusted returns; expect detailed questions.
- Non-compete and garden-leave periods are widely reported at large hedge funds and market makers and vary by jurisdiction and seniority; review them with counsel.
- Be precise about what intellectual property you can discuss from prior roles.
- See [Senior-Level Expectations](../13-Interview-Playbook/12-Senior-Level-Expectations.md) and [Offers, Compensation and Negotiation](../13-Interview-Playbook/11-Offers-Compensation-and-Negotiation.md).

## Sources

- https://www.citadel.com/what-we-do/ (accessed 2026-09-27)
- https://www.citadel.com/what-we-do/fixed-income-and-macro/ (accessed 2026-09-27)
- https://www.citadelsecurities.com/what-we-do/ (accessed 2026-09-27)
- https://www.citadelsecurities.com/what-we-do/options/ (accessed 2026-09-27)
- https://www.citadelsecurities.com/careers/career-perspectives/our-quantitative-research-interview-process/ (accessed 2026-09-27)
- https://www.citadel.com/careers/career-perspectives/our-quantitative-research-interview-process/ (accessed 2026-09-27)
- https://www.citadel.com/careers/career-perspectives/our-engineering-interview-process/ (accessed 2026-09-27)
- https://fortune.com/2022/06/23/read-the-memo-ken-griffin-sent-to-citadels-employees-outlining-the-companys-plan-to-leave-chicago-for-miami (accessed 2026-09-27)
- https://www.glassdoor.com/Interview/Citadel-Securities-Quantitative-Researcher-Interview-Questions-EI_IE1443495.0,18_KO19,42.htm (accessed 2026-09-27)
