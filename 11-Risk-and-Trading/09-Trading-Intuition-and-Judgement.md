---
type: concept
track: [quant-trader]
tier: core
status: solid
prereqs: [expected-value-and-betting-decisions]
est_hours: 3
sources: [Lebron (2019) The Laws of Trading. Wiley, Harris (2003) Trading and Exchanges: Market Microstructure for Practitioners. Oxford University Press, Duke (2018) Thinking in Bets. Portfolio, Bailey and Lopez de Prado (2014) The deflated Sharpe ratio. Journal of Portfolio Management 40(5)]
---

# Trading Intuition and Judgement

## TL;DR

- A trade pitch has six parts: the view and fair value, the source of edge, who is on the other side and why, the size, the exit, and what would prove you wrong.
- "Who is on the other side?" is the core question: either they are forced or paying for something (immediacy, hedging, a mandate), or they know something you do not.
- Size by edge over variance, capped by Kelly and by liquidity and risk limits; say the worst case in money, not percent.
- Judge decisions by process, not outcome: a Sharpe of 1 needs about four years of data for a t-statistic of 2, and 100 traders with no skill produce a best one-year Sharpe of about 2.5.
- Re-underwrite every position each day with "would I put this on now, at this price, at this size?"; the entry price is sunk.

## Learning objectives

- Articulate a trade idea: edge, risk, sizing, exit.
- Separate luck from skill when reviewing trades.
- Know the laws of trading: understand why you are trading and who is on the other side.

## Core concepts

### The trade pitch

Interviewers ask "pitch me a trade" or "you see X; what do you do?" to test structured judgement, not a market call.
A complete answer covers, in order:

1. View and fair value: what you think the price should be and on what horizon.
2. Edge: why the market price differs from your fair value and why the gap should close.
3. Counterparty: who is selling to you (or buying from you) and why they accept a worse price.
4. Risk: what else moves the P&L (market beta, sector, rates, event risk) and how you hedge what you are not paid for.
5. Size: expected profit, standard deviation, worst case, capacity relative to liquidity.
6. Exit: profit target, stop or thesis-invalidation trigger, time stop, and the cost of getting out.

Close with what would change your mind.
A pitch that skips the counterparty and the exit sounds like a retail tip, however good the view is.

### Where edge comes from

Most trading profit falls into a few families:

- Liquidity provision and risk transfer: someone wants to trade now and pays a spread or a price concession for immediacy (market making, block trades, index rebalances).
- Structural or constraint-driven flow: participants who must trade for non-price reasons, such as index funds on rebalance dates, hedgers, funds with mandate or rating constraints, and option sellers hedging gamma.
- Information and analysis: a better forecast from data, research or faster processing of public news.
- Risk premia: being paid to hold a risk others want to shed (carry, volatility selling); this is compensation, not free edge, and it comes with crash risk.

Harris's taxonomy is a useful lens: utilitarian traders trade for reasons other than profit (hedging, investing, liquidity needs) and are the natural counterparties of profit-motivated traders.
A central theme of Lebron's *The Laws of Trading* is knowing why you are doing a trade and which risks you are being paid to take.
If you cannot name why the other side is trading, assume the answer is that they know more than you (see [Market Making Games](../08-Market-Making/10-Market-Making-Games.md) on adverse selection).

### Sizing and risk

Use the tools from [Kelly Criterion and Position Sizing](01-Kelly-Criterion-and-Position-Sizing.md) and [Expected Value and Betting Decisions](02-Expected-Value-and-Betting-Decisions.md).
Size proportional to expected edge divided by variance, take a fraction of Kelly because the edge is an estimate, and then apply hard caps: risk limits (see [Drawdowns and Risk Limits](05-Drawdowns-and-Risk-Limits.md)), stress loss (see [Stress Testing and Scenario Analysis](04-Stress-Testing-and-Scenarios.md)) and liquidity (a position you cannot exit in a few days of normal volume is a different trade).
State the worst case in money and check correlation with what you already hold: two "independent" long-volatility-selling trades are one trade.

### Exits

Decide the exit before entry.
A stop loss is a risk tool, not a forecast: it caps the damage when your thesis is wrong in a way you did not anticipate.
Better than a price stop is a thesis stop: "if the index announcement is reversed, or if the spread widens past its 2008 level, the reason for the trade is gone."
A time stop matters for event and flow trades: if the catalyst has passed and the price has not moved, the edge has expired even if you are flat on P&L.

### Luck versus skill

Outcome is process plus noise, and the noise is large.
Classify each decision on two axes: was the process good (positive expected value given the information at the time), and was the outcome good?
Good process with a bad outcome is bad luck; bad process with a good outcome is the dangerous case, because it gets repeated.
Duke calls judging decisions by their outcomes "resulting".

The statistics are sobering.
For a strategy with annualised Sharpe $S$ over $T$ years of roughly i.i.d. returns, the t-statistic of the mean is about $S\sqrt{T}$.
A win rate $\hat p$ over $n$ trades has standard error $\sqrt{p(1-p)/n}$, about $0.5/\sqrt{n}$ near 50%.
Selection makes it worse: the best record among many is biased upward, which is the trading version of multiple testing (see [Overfitting and the Deflated Sharpe Ratio](../09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md)).
Keep a decision journal written before the outcome is known, so you review what you believed rather than what you remember believing.

### Practical judgement

- Re-underwrite positions: if you would not open the position today at this price and size, reduce it.
- Update on price: an adverse move is evidence against your thesis unless you can explain it by something unrelated; do not add to a loser merely because it is cheaper.
- Avoid the disposition effect: selling winners early and holding losers is the opposite of letting the edge play out.
- Separate the forecast from the trade: "the stock is cheap" is a view; "buy 50k shares with a 3% stop into Thursday's close" is a trade.
- Know when you do not know: passing on a trade with no identifiable edge is a correct answer in an interview and at a desk.
- Firms differ in style (market making, prop, systematic, discretionary); in an interview reason from first principles rather than asserting how a particular firm trades.

## Worked examples

### Example 1: pitching an index-inclusion trade

"A mid-cap stock will be added to a major index at the close in five trading days. Pitch a trade."
View: index-tracking funds must buy the stock at or near the close on the effective date, so there is predictable, price-insensitive demand.
Edge: that demand is known in advance and is large relative to normal volume; the funds pay for immediacy at one specific print.
Counterparty: at entry, sellers who are not thinking about the event; at exit, the index funds themselves, who care about tracking error rather than price.
Risk: market and sector beta (hedge with the index or a sector ETF), crowding (many participants know the same event, so much of the move may already be in the price), and announcement risk.
Size: suppose, as illustrative assumptions, an expected residual move of 2% with 1.5% daily idiosyncratic volatility over five days; the standard deviation is $1.5\%\sqrt{5} \approx 3.4\%$, so the expected Sharpe of the trade is about 0.6 per trade and a fraction of Kelly is a modest position.
Exit: sell into the closing auction on the effective date (to the forced buyer); time stop at the effective date regardless of P&L; cut if the inclusion is withdrawn.
What would change my mind: the stock already trading well above pre-announcement levels with heavy volume, which suggests the flow is fully anticipated.

### Example 2: is a 55% win rate skill?

A trader has won 55 of 100 trades of similar size.
The standard error of the win rate under a fair coin is $\sqrt{0.25/100} = 0.05$, so $z = 0.05/0.05 = 1$, one-sided p-value about 0.16: not evidence of skill.
Over 1,000 trades the same rate gives $z = 0.05/\sqrt{0.25/1000} \approx 3.2$: now it is.
Win rate alone is also the wrong metric: a 40% win rate with winners three times the size of losers has EV $0.4 \times 3 - 0.6 = 0.6$ per unit risked, with break-even win rate $1/(1+3) = 25\%$.

### Example 3: how long to trust a Sharpe ratio

With t-statistic about $S\sqrt{T}$, reaching 1.96 needs $T = (1.96/S)^2$ years.

| Annual Sharpe | Years for t = 1.96 |
| ---: | ---: |
| 0.5 | 15.4 |
| 1.0 | 3.8 |
| 2.0 | 1.0 |

This is why high-frequency strategies (high Sharpe, many independent bets) can be validated quickly and macro views cannot.

### Example 4: the best of 100 lucky traders

100 traders with zero skill each run a strategy for one year; their realised annual Sharpe ratios are roughly independent standard normals.
The probability that a given trader shows a Sharpe above 2 is 2.3%, but the probability that at least one of the 100 does is $1 - 0.9772^{100} \approx 90\%$.
The expected best Sharpe is about 2.51.
When you see the best record in a large group, shrink it heavily toward zero, and ask how many records were looked at.

### Example 5: updating on an adverse move

You bought on a thesis you held with probability 0.6, and the stock has since fallen 5%.
Suppose a move like this has probability 0.3 if the thesis is right and 0.6 if it is wrong.
Bayes gives $P(\text{thesis} \mid \text{drop}) = \frac{0.6 \times 0.3}{0.6 \times 0.3 + 0.4 \times 0.6} = 0.18/0.42 \approx 0.43$.
Your edge has probably gone and the position should shrink, unless the fall has an identifiable cause unrelated to the thesis (a market-wide move you are hedged against, for example).
"It is cheaper now, so I will buy more" is only right if your fair value did not move, which is exactly what the price move calls into question.

### Example 6: sizing an asymmetric trade

A trade wins 3 units with probability 0.4 and loses 1 unit with probability 0.6.
EV is $+0.6$ per unit risked; Kelly on the risk budget is $f^* = 0.4 - 0.6/3 = 0.2$.
Because the 40% is an estimate, run half Kelly or less, risking about 10% of the allocated capital, and check that a string of losses (six in a row has probability $0.6^6 \approx 4.7\%$) does not breach a drawdown limit.

## Pitfalls

- Pitching a view without edge, counterparty, size and exit.
- Answering "who is on the other side" with "the market"; name a type of participant and their motive.
- Confusing a risk premium with edge and sizing it as if it had no crash risk.
- Judging a decision by its outcome, in either direction.
- Trusting a short track record or the best of many records.
- Averaging down because a price is lower rather than because fair value is unchanged.
- Letting a position's entry price drive the decision to hold it.
- Making confident claims about how a specific firm trades or what it earns; you cannot verify them and interviewers notice.

## Interview questions

> [!question]- risk-judgement-pitch-structure | What should a trade pitch cover?
> View and fair value, source of edge, who is on the other side and why, risk and hedges, size with worst case, and exit plus what would change your mind.
> The counterparty and exit are what separate a trade from an opinion.

> [!question]- risk-judgement-other-side | Why is "who is on the other side?" the key question?
> Because a counterparty accepting your price is either paid for something (immediacy, hedging, a mandate) or better informed.
> If you cannot name a non-informational motive, assume adverse selection and your apparent edge is illusory.

> [!question]- risk-judgement-edge-sources | Name the main sources of trading edge.
> Liquidity provision and risk transfer, structural or constraint-driven flow, better information or analysis, and speed.
> Risk premia such as carry are compensation for bearing risk rather than free edge.

> [!question]- risk-judgement-win-rate | A trader wins 55 of 100 trades. Is that evidence of skill?
> No: $z = 0.05/\sqrt{0.25/100} = 1$, a one-sided p-value near 0.16.
> The same rate over 1,000 trades gives $z \approx 3.2$; and win rate ignores the size of wins and losses.

> [!question]- risk-judgement-sharpe-years | How many years of data do you need to be confident a Sharpe-1 strategy is real?
> About four years for a t-statistic of 2.
> The t-statistic is roughly $S\sqrt{T}$, so $T = (1.96/1)^2 \approx 3.8$; for Sharpe 0.5 it is about 15 years.

> [!question]- risk-judgement-best-of-many | 100 traders with no skill trade for a year. What is the expected best annual Sharpe?
> About 2.5.
> The expected maximum of 100 independent standard normals is 2.51, and the probability that at least one exceeds 2 is about 90%.

> [!question]- risk-judgement-process-outcome | How do you separate luck from skill when reviewing a trade?
> Judge the decision by the information and reasoning at the time, recorded before the outcome, not by the P&L.
> Good process with a bad result is bad luck; bad process with a good result is the dangerous case to catch.

> [!question]- risk-judgement-asymmetric | A trade wins 3 with probability 0.4 and loses 1 with probability 0.6. EV and Kelly fraction?
> EV +0.6 per unit risked, Kelly 20% of the risk budget.
> $0.4 \times 3 - 0.6 = 0.6$ and $f^* = 0.4 - 0.6/3 = 0.2$; the break-even win rate is 25%.

> [!question]- risk-judgement-adverse-move | Your position is down 5%. Do you add?
> Only if your fair value is unchanged and the move has a cause unrelated to your thesis; otherwise the move is evidence against you and you should cut.
> With prior 0.6 and a move twice as likely if you are wrong (0.6 against 0.3), the posterior falls to about 0.43.

> [!question]- risk-judgement-reunderwrite | What question should you ask about every open position each day?
> "Would I put this on today, at this price and this size?"
> The entry price is sunk; if the answer is no, reduce.

> [!question]- risk-judgement-stop-loss | What is a stop loss for, and what is a better alternative?
> It is a risk control that caps the loss when you are wrong in an unforeseen way, not a forecast.
> Pair it with a thesis stop (exit when the reason for the trade is gone) and a time stop (exit when the catalyst has passed).

> [!question]- risk-judgement-crowding | Your trade idea is based on a widely known event. What is the risk?
> Crowding: much of the move may already be priced, and many holders exiting together create a sharp reversal.
> Check the price and volume since the event became known, and size smaller with a clear exit.

## Further reading

- Agustin Lebron, *The Laws of Trading* (2019).
- Larry Harris, *Trading and Exchanges: Market Microstructure for Practitioners* (2003), the chapters on why people trade.
- Annie Duke, *Thinking in Bets* (2018).
- Bailey and Lopez de Prado (2014), The deflated Sharpe ratio, *Journal of Portfolio Management* 40(5).
