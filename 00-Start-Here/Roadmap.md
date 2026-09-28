---
type: guide
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
sources: []
---

# Roadmap

A senior quant candidate is judged on three things at once: raw problem-solving speed, depth in the craft of the role, and judgement that only experience gives.
The roadmap trains all three in parallel rather than one after another.

## The weekly rhythm

Every week, whatever the phase:

| Habit | Time | Tool |
| :--- | :--- | :--- |
| Card review | 15-20 min a day | `./qp review` or the dashboard Review page |
| Speed drill | 10 min a day, trader and researcher tracks | `./qp drill arith`, twice a week `./qp drill optiver` |
| Market-making game | 3 games a week, trader track | `./qp drill mm` |
| New topics | the rest of your weekly hours | `./qp next`, `./qp plan` |
| Mastery update | after each study session | `./qp mark <topic> <0-4>` |

Mastery levels mean: 1 studied (read it once), 2 practiced (solved the worked examples yourself), 3 solid (can answer the cards cold), 4 interview-ready (can teach it and handle follow-ups under time pressure).
Mark honestly; readiness scores are only as good as these marks.

## Phases

The phases are ordered by what interviews test first, not by textbook order.
`./qp plan` turns them into dated weeks for your tracks and weekly hours.

### Phase 1: Screening strength (weeks 1-4)

Online assessments and first-round phone screens filter on speed and core probability.

- All of [Probability](../01-Probability/README.md) through [Classic Expectation Problems](../01-Probability/14-Classic-Expectation-Problems.md), then the [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md).
- [Mental Math](../13-Interview-Playbook/02-Mental-Math.md) and [Brainteasers and Puzzles](../13-Interview-Playbook/03-Brainteasers-and-Puzzles.md).
- [How Quant Interviews Work](../13-Interview-Playbook/01-How-Quant-Interviews-Work.md).
- Developers: DSA from SDE-Interview-Prep in parallel (see the [link map](SDE-Link-Map.md)).

Exit bar: a consistent Zetamac-style score you are happy with, and the probability problem set answered cold.

### Phase 2: Role core (weeks 5-12)

- Trader: [Derivatives and Volatility](../05-Derivatives-and-Volatility/README.md) topics 01-07 and 13, [Market Making](../08-Market-Making/README.md) topics 01-06 and 10, [Kelly and sizing](../11-Risk-and-Trading/01-Kelly-Criterion-and-Position-Sizing.md).
- Researcher: [Statistics and Econometrics](../02-Statistics-and-Econometrics/README.md) core topics, [Linear Algebra and Optimization](../03-Linear-Algebra-and-Optimization/README.md) core topics, [Alpha Research](../09-Alpha-Research-and-Portfolio/README.md) topics 01-10, [ML for Finance](../10-Machine-Learning-for-Finance/README.md) topics 01-03.
- Developer: [Quant Development](../12-Quant-Development/README.md) core topics, [Limit Order Books](../07-Market-Microstructure/01-Limit-Order-Books-and-Order-Types.md), [Market Making Systems](../08-Market-Making/11-Market-Making-Systems-Architecture.md), and the options basics in [Derivatives](../05-Derivatives-and-Volatility/README.md) 01-05.

Exit bar: every core topic in your track at mastery 3.

### Phase 3: Depth and differentiation (weeks 13-20)

Advanced-tier topics in your track, plus the adjacent track's core (traders learn microstructure and alpha basics; researchers learn market making and execution; developers learn the pricing and statistics their users need).

### Phase 4: Firm targeting (last 3-4 weeks before interviews)

- Read the [firm guides](../14-Firms/README.md) for your targets and run `./qp firms <firm>` to see the weakest focus topics.
- Senior candidates: [Senior-Level Expectations](../13-Interview-Playbook/12-Senior-Level-Expectations.md).
- Mock interviews daily; review every missed question into a card.

## If you have less time

| Time before interviews | Do |
| :--- | :--- |
| 2 weeks | Probability problem set, mental math drills, the firm guide, and your track's problem set only. |
| 6 weeks | Phase 1, then your track's core from Phase 2 with `./qp plan --core`. |
| 3 months or more | All four phases. |
