---
type: moc
title: "Trading Drills and Deliberate Practice Index"
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
tags: [drills, practice, mental-math, market-making, options, srs, moc]
---

# Trading Drills and Deliberate Practice Index

The Drills pillar provides the deliberate practice machinery for Markets Mastery OS.
In professional trading, conceptual knowledge without high-speed execution under pressure is insufficient.
This bank contains timed drills, interactive exercises, hidden-answer recall decks, and quantitative games designed to build automaticity.

---

## Learning Objectives

- Build split-second mental arithmetic accuracy for price conversions, basis points, option premiums, and implied moves.
- Master fast market-making estimation under asymmetric information and adverse selection.
- Develop instant recall of option payoff profiles, Greeks signs, and multi-leg spread structures.
- Practice rapid tape reading and volume profile level identification.

---

## Drill Categories

### 1. Rapid-Fire Mental Math Drills
- Fast conversion between percentage returns, basis points, and log returns.
- Standard deviation scaling: $\sigma_{\text{daily}} \times \sqrt{252} \approx \sigma_{\text{annual}}$.
- Rule of 16 for instantaneous daily volatility estimation: $\sigma_{\text{daily}} \approx \frac{\sigma_{\text{annual}}}{16}$.
- Expected value calculations with asymmetric payoffs and probability trees.

### 2. Market Making and Quoting Games
- Two-sided bid-ask quotation under inventory skew.
- Setting wide spreads during high-volatility news events and tightening during calm consolidation.
- Managing toxic order flow and detecting informed counterparties.
- Interactive CLI drill: `./qp drill mm` (the Optiver-style market making simulation).

### 3. Options Greeks and Payoff Drills
- Visual identification of option spreads (Verticals, Calendars, Diagonals, Straddles, Strangles, Iron Condors, Butterflies).
- Greeks sign identification: Sign of Delta, Gamma, Theta, Vega for each leg and net portfolio.
- Volatility crush estimation following scheduled corporate earnings announcements.
- Dynamic delta-hedging rebalancing calculation given an underlying tick move.

### 4. Chart Replay and Tape Reading Drills
- Identifying Value Area High (VAH), Value Area Low (VAL), and Point of Control (POC) on unlabelled Volume Profiles.
- Spotting absorption versus exhaustion on footprint and Level 2 depth charts.
- Formulating trade setups with pre-defined invalidation levels before revealing subsequent price action.

---

## Practice Workflows

1. **Daily Warmup**: Run 5 minutes of `./qp drill arith` to sharpen numerical fluency.
2. **Weekly Review**: Review due cards in Spaced Repetition using `./qp review --track quant-trader`.
3. **Simulated Tape Session**: Execute 20 simulated trades in `replay_chart` before touching paper or live accounts.

---

## Navigation

- **Master Hub**: [[16-Trading-and-Investing/MARKETS_HUB|Markets Mastery OS Master Hub]]
- **Trading Styles**: [[16-Trading-and-Investing/07-Trading-Styles/_Index_Trading_Styles|Trading Styles Index]]
- **Trade Journaling System**: `16-Trading-and-Investing/Private/README.md`
