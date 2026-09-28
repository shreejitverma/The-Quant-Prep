---
type: firm
track: [quant-trader, quant-research, quant-dev]
tier: core
status: draft
firm_type: prop-trading
focus: [probability-problem-set, conditional-probability-and-bayes, classic-expectation-problems, expected-value-and-betting-decisions, kelly-criterion-and-position-sizing, market-making-games, trading-games-in-interviews, fair-value-and-theoretical-pricing, adverse-selection-and-flow-toxicity, etfs-and-index-arbitrage, mental-math, brainteasers-and-puzzles, coding-interviews-for-quants, data-structures-and-algorithms-for-quant-interviews]
sources: []
---

# Jane Street

> [!info] Draft
> Facts below were gathered from the sources listed at the end on 2026-09-27.
> Firms change their processes often; verify anything that matters with your recruiter.

## Snapshot

- Jane Street describes itself as a global liquidity provider and trading firm and as one of the world's largest market makers, trading on more than 200 electronic exchanges and other venues.
- It trades its own capital; it has no outside investors in the hedge-fund sense.
- The firm made its name in ETFs and now describes itself as a major player in equities, bonds and options, among other markets.
- Trading floors are in New York, London, Hong Kong, Singapore and Amsterdam.
- It was founded in 2000.
- Almost all software, including trading and risk systems, is built in-house in OCaml, a statically typed functional language.
- Bloomberg reported roughly 3,500 employees and record trading revenue for 2025; treat these figures as press reports, not firm disclosures.

## Roles

- Quantitative trader: prices and trades products (ETFs, bonds, options and more), manages risk, and works with researchers and developers on strategies; Jane Street says finance background is optional.
- Quantitative researcher: analyses large datasets with statistical and machine learning methods, builds and tests models, creates trading strategies and writes the code that implements them.
- Software engineer: builds the trading, risk and research infrastructure, mostly in OCaml.
- Jane Street says the lines between trading, research and technology are intentionally porous, so expect overlap between roles.

## Interview process

> [!warning] Commonly reported, verify with your recruiter
> Round counts and formats vary by role, office and year.

- Jane Street publishes interview guidance per role and says applications are reviewed on a rolling basis, with feedback typically within a week of an interview.
- Trading: the firm says interviews test collaborative problem solving, not finance knowledge; candidate accounts commonly describe phone or video rounds on probability and expected value, followed by an onsite day that includes market-making and betting games.
- Research: the firm describes research interviews as a hybrid of the trading and software engineering interviews, so prepare for both.
- Software engineering: coding interviews in the language you know best; OCaml experience is not required.
- The firm encourages reapplying after roughly one year.

## What they test

- Probability and expected value, the core of the firm's own [Probability and Markets guide](https://www.janestreet.com/probability-markets/): [Conditional Probability and Bayes](../01-Probability/02-Conditional-Probability-and-Bayes.md), [Classic Expectation Problems](../01-Probability/14-Classic-Expectation-Problems.md), [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md).
- Making markets and sizing bets: [Market Making Games](../08-Market-Making/10-Market-Making-Games.md), [Trading Games in Interviews](../13-Interview-Playbook/05-Trading-Games-in-Interviews.md), [Expected Value and Betting Decisions](../11-Risk-and-Trading/02-Expected-Value-and-Betting-Decisions.md), [Kelly Criterion and Position Sizing](../11-Risk-and-Trading/01-Kelly-Criterion-and-Position-Sizing.md).
- Pricing intuition and adverse selection when quoting: [Fair Value and Theoretical Pricing](../08-Market-Making/02-Fair-Value-and-Theoretical-Pricing.md), [Adverse Selection and Flow Toxicity](../07-Market-Microstructure/05-Adverse-Selection-and-Flow-Toxicity.md).
- Useful business context rather than tested knowledge: [ETFs and Index Arbitrage](../06-Fixed-Income-and-Asset-Classes/08-ETFs-and-Index-Arbitrage.md).
- Speed and clarity of reasoning: [Mental Math](../13-Interview-Playbook/02-Mental-Math.md), [Brainteasers and Puzzles](../13-Interview-Playbook/03-Brainteasers-and-Puzzles.md).
- Research and engineering: [Coding Interviews for Quants](../13-Interview-Playbook/07-Coding-Interviews-for-Quants.md), [Data Structures and Algorithms for Quant Interviews](../12-Quant-Development/05-Data-Structures-and-Algorithms-for-Quant-Interviews.md).

## Preparation plan

1. Week 1: run `./qp firms jane-street` to see your weakest focus topics, then work the [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md) and read the firm's Probability and Markets guide.
2. Week 2: expected value, betting and sizing; drill `./qp drill arith` daily and study [Expected Value and Betting Decisions](../11-Risk-and-Trading/02-Expected-Value-and-Betting-Decisions.md).
3. Week 3: market making; study [Market Making Games](../08-Market-Making/10-Market-Making-Games.md) and run `./qp drill mm` until your quotes stay consistent under updates.
4. Week 4: talk out loud; practise games and puzzles with a partner, since the firm stresses collaborative problem solving.
5. Weeks 5-6 (research and engineering candidates): add [Coding Interviews for Quants](../13-Interview-Playbook/07-Coding-Interviews-for-Quants.md) and a statistics or ML refresh, then clear the queue with `./qp review` and `./qp mark <id> 3` as topics firm up.

## Culture and what they value

- The firm emphasises collaboration and porous boundaries between trading, research and technology.
- Its interview pages stress problem solving and communication over prior finance knowledge.
- It builds nearly all of its technology in-house.

## Senior hire notes

- Experienced hires are reported to face the same core probability and problem-solving bar, with added depth on their own domain; confirm with the recruiter.
- For experienced researchers and engineers, expect discussion of past projects in detail; be clear about what you can and cannot share from a prior employer.
- Non-compete and garden-leave terms at your current employer may affect start dates; review them with counsel before accepting.
- See [Senior-Level Expectations](../13-Interview-Playbook/12-Senior-Level-Expectations.md).

## Sources

- https://www.janestreet.com/what-we-do/overview/ (accessed 2026-09-27)
- https://www.janestreet.com/join-jane-street/interviewing/ (accessed 2026-09-27)
- https://www.janestreet.com/probability-markets/ (accessed 2026-09-27)
- https://www.janestreet.com/quantitative-research/ (accessed 2026-09-27)
- https://www.bloomberg.com/news/articles/2026-04-24/jane-street-snatches-wall-street-crown-with-record-39-6-billion-trading-haul (accessed 2026-09-27)
- https://www.bloomberg.com/news/articles/2026-05-01/jane-street-pay-pool-hits-9-4-billion-more-than-doubles-in-2025 (accessed 2026-09-27)
