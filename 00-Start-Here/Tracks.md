---
type: guide
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
sources: []
---

# Tracks

Every topic is tagged with the tracks that need it: T (quant trader), R (quant researcher), D (quant developer).
Set yours with `./qp profile --tracks quant-trader quant-research` (any combination); plans, review queues and readiness all follow it.

## Quant trader

What the job is: pricing and trading risk in real time, usually as a market maker or on a proprietary desk (Jane Street, Optiver, SIG, IMC, Akuna, DRW, Citadel Securities, Five Rings).
What interviews test: mental arithmetic speed, probability and expected value under pressure, market-making and betting games, options intuition, and how you reason about risk and sizing out loud.

Priorities, in order:

1. [Probability](../01-Probability/README.md) to problem-set speed, and [Mental Math](../13-Interview-Playbook/02-Mental-Math.md) daily.
2. [Market Making Games](../08-Market-Making/10-Market-Making-Games.md) and [Trading Games in Interviews](../13-Interview-Playbook/05-Trading-Games-in-Interviews.md).
3. Options: [Put-Call Parity](../05-Derivatives-and-Volatility/02-Option-Payoffs-and-Put-Call-Parity.md), [The Greeks](../05-Derivatives-and-Volatility/05-The-Greeks.md), [Delta Hedging and Gamma Scalping](../05-Derivatives-and-Volatility/06-Delta-Hedging-and-Gamma-Scalping.md).
4. [Market Making](../08-Market-Making/README.md) fundamentals, inventory and quoting.
5. [Kelly and Position Sizing](../11-Risk-and-Trading/01-Kelly-Criterion-and-Position-Sizing.md) and [Expected Value and Betting](../11-Risk-and-Trading/02-Expected-Value-and-Betting-Decisions.md).

Senior traders are additionally asked about P&L attribution, risk limits, how they sized and exited real positions, and what they would change in a desk's process.

## Quant researcher

What the job is: finding, validating and combining predictive signals, and turning them into portfolios (Two Sigma, Citadel, Squarepoint, Millennium and Balyasny pods, D. E. Shaw, HRT and Radix research).
What interviews test: probability and statistics depth, regression and time series, ML with honest validation, research judgement about overfitting, and coding in Python.

Priorities, in order:

1. [Probability](../01-Probability/README.md) and [Statistics and Econometrics](../02-Statistics-and-Econometrics/README.md), especially [Linear Regression](../02-Statistics-and-Econometrics/04-Linear-Regression-OLS.md).
2. [Linear Algebra and Optimization](../03-Linear-Algebra-and-Optimization/README.md) core.
3. [Alpha Research](../09-Alpha-Research-and-Portfolio/README.md): process, signals, backtesting, overfitting, portfolio construction.
4. [ML for Finance](../10-Machine-Learning-for-Finance/README.md): time-series cross-validation and tree ensembles first.
5. [Stochastic Calculus](../04-Stochastic-Calculus/README.md) and [Derivatives](../05-Derivatives-and-Volatility/README.md) for derivatives-focused research roles.

Senior researchers are additionally asked to walk through a past research programme end to end, defend its statistics, and explain capacity, decay and costs without revealing proprietary detail.

## Quant developer

What the job is: building the trading, research and risk systems, from low-latency order paths to pricing libraries and data platforms (HRT, Jump, Tower, Citadel Securities, Jane Street, Radix, Optiver, IMC).
What interviews test: coding (data structures and algorithms), C++ or the firm's language in depth, systems and networking, concurrency, and enough finance to talk to traders.

Priorities, in order:

1. Data structures and algorithms, and C++, from SDE-Interview-Prep (see the [link map](SDE-Link-Map.md)).
2. [Quant Development](../12-Quant-Development/README.md): order books, feed handlers, backtesters, risk checks, testing.
3. [Market Microstructure](../07-Market-Microstructure/README.md) basics and [Market Making Systems Architecture](../08-Market-Making/11-Market-Making-Systems-Architecture.md).
4. The [low-latency systems vault](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/00%20Home.md) for HFT roles.
5. Probability basics: [Counting](../01-Probability/01-Counting-and-Combinatorics.md), [Conditional Probability](../01-Probability/02-Conditional-Probability-and-Bayes.md) and [Expectation](../01-Probability/04-Expectation-Variance-and-Linearity.md), which quant firms ask developers too.

Senior developers are additionally asked to design whole systems (an exchange, a market data platform, a risk engine), reason about latency budgets and failure modes, and describe systems they owned in production.
