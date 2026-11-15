---
type: concept
title: "Fair Value, Microprice, and Order Flow Imbalance"
track: [quant-trader, quant-research]
tier: core
status: solid
est_hours: 1.5
tags: [fair-value, microprice, order-flow-imbalance, stoikov, microstructure, lead-lag]
prereqs: []
---

# Fair Value, Microprice, and Order Flow Imbalance

In liquid electronic markets, the simple arithmetic mid-price between the national best bid and offer is a crude and delayed estimator of true short-term value.
Quantitative market makers and high-frequency traders construct continuous estimates of fair value by incorporating depth imbalance, queue dynamics, and cross-asset lead-lag relationships.
Understanding the mathematical formulation of the microprice and Order Flow Imbalance (OFI) is essential for predicting price drift over sub-second horizons.

---

## TL;DR

The quoted mid-price ignores the relative quantity of shares resting on the bid versus the ask.
The volume-weighted mid adds Level 1 book imbalance, but it is not a martingale; Stoikov's (2018) micro-price is defined as the limit of expected future mids given imbalance and spread, so it is a martingale by construction.
Order Flow Imbalance (OFI) measures the net change in available liquidity at the best quotes; Cont, Kukanov and Stoikov (2014) found a linear relation between OFI and contemporaneous mid-price changes, with a slope inversely proportional to depth.
In multi-asset frameworks, fair value is anchored to the venue that leads price discovery; for the S&P 500, Hasbrouck (2003) found most price discovery happens in the E-mini futures, not the SPY ETF.

---

## Learning objectives

- Formulate the classical volume-weighted microprice and Stoikov's Markov-chain microprice framework.
- Derive the Cont-Kukanov-Stoikov (2014) Order Flow Imbalance (OFI) equation from discrete order book events.
- Calibrate the linear price impact parameter connecting OFI to tick price changes.
- Implement cross-asset fair value models exploiting lead-lag dynamics between index futures and ETFs.
- Identify the failure modes of order book imbalance signals in the presence of iceberg orders and latency arbitrage.

---

## Core concepts

### 1. Limits of the Simple Mid-Price

The standard mid-price $S_t$ is defined as the arithmetic mean of the National Best Bid ($P_b$) and National Best Offer ($P_a$):

$$S_t = \frac{P_a + P_b}{2}$$

While $S_t$ represents the midpoint of the quoted spread $w = P_a - P_b$, it treats an order book with 100 shares at the bid and 10,000 shares at the ask identically to one with 10,000 shares at the bid and 100 shares at the ask.
In the latter scenario, buying pressure heavily outweighs selling pressure, making an upward price tick significantly more probable than a downward tick.

### 2. The Classical Volume-Weighted Microprice

The simplest adjustment weights the bid and ask prices inversely by their resting queue sizes $Q_b$ and $Q_a$:

$$P_{\text{micro}} = \frac{Q_b P_a + Q_a P_b}{Q_b + Q_a} = S_t + \left(\frac{Q_b - Q_a}{Q_b + Q_a}\right) \frac{w}{2}$$

Defining the Level 1 order book imbalance ratio as:

$$I = \frac{Q_b - Q_a}{Q_b + Q_a} \in [-1, 1]$$

The microprice shifts linearly away from the heavy side toward the thin side:

$$P_{\text{micro}} = S_t + I \cdot \frac{w}{2}$$

- When $Q_b \gg Q_a$, $I \to +1$, and $P_{\text{micro}} \to P_a$.
- When $Q_a \gg Q_b$, $I \to -1$, and $P_{\text{micro}} \to P_b$.
- When the book is symmetric ($Q_b = Q_a$), $I = 0$, and $P_{\text{micro}} = S_t$.

### 3. Stoikov's Markov-Chain Microprice (2018)

Sasha Stoikov (2018) pointed out that the volume-weighted mid is not a martingale: its expected future value differs from its current value, so it is a biased forecast of future mids.
Stoikov defines the micro-price as the limit of expected mid-prices at successive mid-price changes:

$$P_{\text{micro}} = \lim_{i \to \infty} \mathbb{E}[M_{\tau_i} \mid M_0, I_0, w_0]$$

Where $M$ is the mid-price and $\tau_1 < \tau_2 < \dots$ are the times at which the mid changes, so $P_{\text{micro}}$ is a martingale by construction.
With imbalance discretized into buckets and the spread into a few tick states, the order book is a Markov chain whose states with an unchanged mid are transient and whose mid-changing moves are absorbing.
If $Q$ is the matrix of one-step transition probabilities among transient states, $R$ the probabilities of moving into each absorbing state and $K$ the mid change attached to each, the first adjustment is
$$g^1 = (\mathbf{1} - Q)^{-1} R K$$
and the micro-price is $M + \sum_{i \ge 1} g^i$, with each later $g^{i+1} = B g^i$ for a matrix $B$ built from the same chain, all estimated from historical book data.

### 4. Cont-Kukanov-Stoikov Order Flow Imbalance (OFI)

Cont, Kukanov, and Stoikov (2014) showed that price changes over discrete intervals $\Delta t$ are driven by the accumulation of net order flow at the best quotes.
Let $P_{b,t}, Q_{b,t}$ and $P_{a,t}, Q_{a,t}$ denote best quotes and sizes at time $t$.
Order Flow Imbalance between $t-1$ and $t$ is formulated as:

$$\text{OFI}_t = e_{b,t} - e_{a,t}$$

Where the bid contribution $e_{b,t}$ is:

$$e_{b,t} = \begin{cases} Q_{b,t} & \text{if } P_{b,t} > P_{b,t-1} \\ Q_{b,t} - Q_{b,t-1} & \text{if } P_{b,t} = P_{b,t-1} \\ -Q_{b,t-1} & \text{if } P_{b,t} < P_{b,t-1} \end{cases}$$

And the ask contribution $e_{a,t}$ is:

$$e_{a,t} = \begin{cases} -Q_{a,t-1} & \text{if } P_{a,t} > P_{a,t-1} \\ Q_{a,t} - Q_{a,t-1} & \text{if } P_{a,t} = P_{a,t-1} \\ Q_{a,t} & \text{if } P_{a,t} < P_{a,t-1} \end{cases}$$

In TAQ data for 50 US stocks, Cont, Kukanov and Stoikov found a linear relation between contemporaneous mid-price changes and OFI:

$$\Delta S_t = \beta \cdot \text{OFI}_t + \epsilon_t$$

The coefficient $\beta$ is a price-impact coefficient, an empirical analogue of Kyle's lambda, in units of price change per share of net order flow; they found it inversely proportional to the depth at the best quotes.

---

## Worked examples

### Example 1: Asymmetric Queue Microprice vs Quoted Mid

Consider an equity trading with a 2-cent spread (hypothetical inputs):
- Best Bid: $P_b = \$50.00$, resting size $Q_b = 8,000$ shares.
- Best Offer: $P_a = \$50.02$, resting size $Q_a = 2,000$ shares.

1. **Calculate the Quoted Mid-Price**:
   $$S_t = \frac{\$50.00 + \$50.02}{2} = \$50.0100$$
2. **Calculate the Imbalance Ratio**:
   $$I = \frac{8,000 - 2,000}{8,000 + 2,000} = \frac{6,000}{10,000} = +0.60$$
3. **Calculate the Classical Microprice**:
   $$P_{\text{micro}} = \$50.0100 + 0.60 \times \frac{\$0.02}{2} = \$50.0100 + \$0.0060 = \$50.0160$$
4. **Trading Implication**:
   The microprice indicates that fair value is 0.6 cents above mid, closer to the ask.
   A market maker quoting symmetrically at $\$50.00$ bid / $\$50.02$ ask is mispricing the book; they should skew quotes upward (e.g. bidding $\$50.01$ or pulling back their ask).

### Example 2: Step-by-Step OFI Calculation Across 3 Ticks

Track three consecutive market updates for a security (hypothetical inputs):

- **Timestamp $t=0$**: Bid $\$100.00$ (size 500), Ask $\$100.05$ (size 500).
- **Timestamp $t=1$**: Limit buy orders arrive at the bid.
  Bid $\$100.00$ (size 900), Ask $\$100.05$ (size 500).
  - Price did not change: $P_{b,1} = P_{b,0}$ and $P_{a,1} = P_{a,0}$.
  - $e_{b,1} = Q_{b,1} - Q_{b,0} = 900 - 500 = +400$.
  - $e_{a,1} = Q_{a,1} - Q_{a,0} = 500 - 500 = 0$.
  - $\text{OFI}_1 = +400 - 0 = +400$.
- **Timestamp $t=2$**: Aggressive buyer sweeps the ask.
  Bid $\$100.05$ (size 200), Ask $\$100.10$ (size 600).
  - Bid price increased: $P_{b,2} > P_{b,1} \implies e_{b,2} = Q_{b,2} = +200$.
  - Ask price increased: $P_{a,2} > P_{a,1} \implies e_{a,2} = -Q_{a,1} = -500$.
  - $\text{OFI}_2 = e_{b,2} - e_{a,2} = +200 - (-500) = +700$.
- **Cumulative OFI over the period**:
  $$\text{OFI}_{\text{total}} = +400 + 700 = +1,100\text{ shares}$$
  Mid-price moved from $\$100.025$ to $\$100.075$ ($\Delta S = +\$0.050$).
  The ratio $\frac{\$0.050}{1,100} = \$0.00004545$ per share ($4.55\text{ cents per 1,000 shares}$) is a one-observation illustration of $\beta$; in practice $\beta$ is estimated by regressing many interval price changes on their OFI.
  In event terms, $t=1$ added 400 shares of bid limit orders and $t=2$ added a new 200-share bid one tick higher and a 500-share buy that emptied the ask queue, so OFI counts $400 + 200 + 500 = 1,100$ shares of net buying pressure.

---

## Pitfalls

- **Ignoring Hidden Liquidity**:
  The microprice computed solely from displayed Level 1 depth produces false signals when a large non-displayed iceberg order rests on the apparently thin side.
- **Latency Arbitrage on Correlated Fair Value**:
  Using a slow polling loop to price ETF components from futures leaves the desk vulnerable to snipers who execute against stale ETF quotes within microseconds of a futures move.
- **Microprice Mean Reversion vs Momentum Regimes**:
  In choppy regimes, microprice deviations from mid mean-revert quickly; in momentum break regimes, extreme imbalance predicts an immediate regime shift through the quote.
- **Asymmetric Tick Sizes**:
  In "thick-book" securities where the spread is constrained to 1 tick ($w = 0.01$), the microprice is highly informative; in "thin-book" wide-spread stocks, Level 1 depth imbalance loses predictive power to Level 2 and Level 3 book curvature.

---

## Interview questions

> [!question]- mkt-pqt-033 | Why is the arithmetic mid-price an inadequate estimator of instantaneous fair value?
> It weights the best bid and ask equally regardless of the volume of resting liquidity at each level.
> When order queues are heavily asymmetric, the probability of an immediate tick in the direction of the thinner side is significantly higher.

> [!question]- mkt-pqt-034 | State the formula for the classical volume-weighted microprice.
> P_micro = (Q_b * P_a + Q_a * P_b) / (Q_b + Q_a), which equals Mid + ((Q_b - Q_a) / (Q_b + Q_a)) * (Spread / 2).
> It interpolates linearly between bid and ask based on the Level 1 queue imbalance ratio.

> [!question]- mkt-pqt-035 | In Sasha Stoikov's 2018 model, how is the microprice formally defined?
> As the limit of expected mid-prices at successive mid-price changes: P_micro = lim over i of E[M_tau_i | M_0, I_0, w_0], where tau_i is the time of the i-th mid change.
> Conditioning on imbalance and spread states of a Markov chain estimated from data makes it a martingale by construction, unlike the volume-weighted mid.

> [!question]- mkt-pqt-036 | What is Order Flow Imbalance (OFI) as defined by Cont, Kukanov, and Stoikov (2014)?
> OFI measures the net change in shares available at the best bid and offer across discrete market updates.
> It quantifies the net balance between newly placed limit orders, market order fills, and order cancellations.

> [!question]- mkt-pqt-037 | What is the mathematical relationship between contemporaneous price change and OFI?
> Delta S_t = beta * OFI_t + epsilon_t.
> Cont, Kukanov and Stoikov (2014) found this linear relation in TAQ data for 50 US stocks, stable across stocks and time scales, and less noisy than the relation between price changes and traded volume.

> [!question]- mkt-pqt-038 | What does the regression slope beta represent in the OFI price impact equation?
> Beta represents the inverse of market depth, measuring the dollar price impact per share of net order flow imbalance.
> Higher beta indicates lower market liquidity and greater vulnerability to market sweeps.

> [!question]- mkt-pqt-039 | Why does the E-mini S&P 500 futures contract lead the SPY ETF in price discovery?
> Hasbrouck (2003, Journal of Finance) found that most S&P 500 and Nasdaq-100 price discovery occurs in the E-mini futures, with the ETFs playing a smaller role.
> The usual explanations are cheaper leverage, a single central order book, and a large share of institutional hedging flow; arbitrageurs then carry the futures move into SPY and the cash stocks.

> [!question]- mkt-pqt-040 | How do quantitative desks exploit lead-lag relationships in ETF market making?
> They calculate a synthetic fair value for the ETF by multiplying the real-time index futures price by the hedge ratio.
> When the ETF quoted mid deviates from synthetic fair value, they quote aggressively to capture the expected convergence.

> [!question]- mkt-pqt-041 | What is a "thick book" versus a "thin book" stock in market microstructure?
> A thick book has a bid-ask spread constrained to the minimum tick size ($0.01) with deep queues (thousands of shares) at the best quotes.
> A thin book has a wide spread (multiple ticks) with sparse queues that frequently gap across price levels.

> [!question]- mkt-pqt-042 | Why is the Level 1 microprice more predictive in thick books than in thin books?
> In thick books, the spread is pinned at one tick, so the mid moves mainly when one of the two best queues is exhausted, and the relative queue sizes carry most of the short-horizon information.
> In thin books, quote cancellations and wider spreads introduce multi-level dynamics that Level 1 imbalance fails to capture.

> [!question]- mkt-pqt-043 | How do iceberg orders undermine the predictive power of the volume-weighted microprice?
> Iceberg orders conceal substantial non-displayed size, making a queue appear artificially thin.
> The microprice predicts a price break toward the thin side, only for aggressive orders to be repeatedly absorbed by the hidden tranche.

> [!question]- mkt-pqt-044 | What is the Cancel-to-Trade Ratio (CTR) and what does a high ratio signify?
> CTR is the number of order cancellations divided by the number of executed trades.
> A high CTR indicates that most displayed orders are repriced or withdrawn before they trade, typical of fast quote updating by market makers; displayed size is then a weaker guide to the size you can actually trade.

> [!question]- mkt-pqt-045 | Explain how queue cancellation can generate a negative OFI contribution at the bid.
> If the bid price remains unchanged (P_b,t = P_b,t-1) but resting volume drops (Q_b,t < Q_b,t-1) without an execution, e_b,t is negative.
> Liquidity withdrawal reduces buying support, shifting net order flow imbalance in the bearish direction.

> [!question]- mkt-pqt-046 | What is the difference between static order book imbalance and Order Flow Imbalance?
> Static imbalance measures resting queue depth at a single instant: (Q_b - Q_a) / (Q_b + Q_a).
> OFI measures the dynamic flux of volume entering and exiting the order book over a discrete time window.

> [!question]- mkt-pqt-047 | How is Kyle's lambda related to the market depth parameter beta in OFI models?
> Kyle's lambda measures price change as a function of total signed order volume: Delta P = lambda * Q.
> The OFI beta is an empirical analog that conditions on changes in the limit order book rather than aggregate traded volume.

> [!question]- mkt-pqt-048 | What is VPIN (Volume-Synchronized Probability of Toxicity)?
> VPIN measures the historical imbalance between buyer-initiated and seller-initiated volume across equal-volume clock bars.
> Developed by Easley, Lopez de Prado, and O'Hara (2012), it serves as a real-time toxicity gauge for market makers.

> [!question]- mkt-pqt-049 | Why do volume clock bars improve toxicity estimation compared to chronological time bars?
> Trade arrivals are clustered and non-stationary; chronological time bins over-sample quiet periods and under-sample volatile panics.
> Volume clocks sample the market at a rate proportional to trading intensity, normalizing the information arrival rate.

> [!question]- mkt-pqt-050 | How does a quantitative desk use the microprice to shade its quoting spreads?
> When the microprice is above mid, the desk skews its quotes upward by raising both its bid and ask.
> This deters toxic buys of their ask while increasing the probability of filling passive limit buys at their higher bid.

> [!question]- mkt-pqt-051 | What is the effect of sub-penny pricing on US lit exchanges?
> As of November 2026, Rule 612 of Regulation NMS bars quotes in increments below $0.01 for NMS stocks quoted at $1.00 or more ($0.0001 below $1.00).
> The SEC's 2024 amendments add a $0.005 increment for stocks whose time-weighted average quoted spread is $0.015 or less, but SEC Release 34-105656 (June 11, 2026) deferred compliance to the first business day of November 2027.
> For low-priced liquid stocks the 1-cent floor binds: the spread sits at one tick and long queues form at the best quotes.

> [!question]- mkt-pqt-052 | How does dark pool midpoint crossing interact with the lit exchange microprice?
> Dark pools execute trades at the lit NBBO midpoint, providing price improvement over lit quotes.
> However, if the lit microprice is skewed, executing at the simple midpoint transfers economic edge to the informed counterparty.

> [!question]- mkt-pqt-053 | What is quote stuffing in high-frequency market microstructure?
> Flooding an exchange with massive volumes of rapid limit orders and immediate cancellations to congest competitor order processing engines.
> The resulting latency delay allows the offending firm to trade on price changes before competitors process the book update.

> [!question]- mkt-pqt-054 | Explain the concept of book skewness across multiple price levels (Level 2/3).
> Book skewness evaluates the volume profile slope across levels 1 through 5 on both sides of the book.
> If the cumulative depth on the bid decays slower than the ask, institutional demand extends deeper into the book.

> [!question]- mkt-pqt-055 | What is a phantom liquidity trap?
> Liquidity displayed by latency arbitrageurs across multiple venues that is cancelled the microsecond a market order hits the first venue.
> An execution algorithm attempting to sweep the displayed size receives fills on only a fraction of the quoted depth.

> [!question]- mkt-pqt-056 | How does a market maker measure the information content of a trade fill?
> By computing the correlation between the fill direction and subsequent price movements at multiple horizons (10ms, 100ms, 1s, 5s).
> Fills followed by persistent drift in the direction the counterparty traded indicate high information content (toxic flow).

> [!question]- mkt-pqt-057 | Why does cross-venue consolidation introduce latency jitter into fair value calculations?
> Market data feeds from NASDAQ, NYSE, and Cboe arrive asynchronously over microwave and fiber links.
> A consolidated quote engine must resolve race conditions where one venue's tick arrives milliseconds out of chronological sequence.

> [!question]- mkt-pqt-058 | What is the role of a Securities Information Processor (SIP) versus direct market feeds?
> The SIP consolidates exchange quotes and publishes the official NBBO, but its data must travel to a central processor and be aggregated before it is redistributed, so it arrives later than each exchange's direct feed.
> Latency-sensitive desks build their own consolidated book from direct exchange feeds.

> [!question]- mkt-pqt-059 | What is the Trade-Through Rule (Rule 611 of Regulation NMS)?
> Rule 611 requires trading centers to maintain written policies reasonably designed to prevent trade-throughs of protected quotations on other venues, with exceptions such as intermarket sweep orders.
> As of November 2026 it is in force, but on June 11, 2026 the SEC proposed rescinding Rule 611 and the locked-and-crossed-markets rule, Rule 610(e).

> [!question]- mkt-pqt-060 | How does an inverted exchange exploit queue priority?
> Traders who do not want to wait at the back of a long queue on a maker-taker exchange post the same price on an inverted venue, where queues are shorter.
> They pay a fee to post instead of earning a rebate, in exchange for a higher probability of being filled sooner.

> [!question]- mkt-pqt-061 | In statistical arbitrage, how is the cointegration spread used as a fair value anchor?
> For two cointegrated assets X and Y, their long-term spread S = Y - beta * X is stationary with a constant mean.
> When S deviates significantly from its historical mean, the desk prices fair value expecting mean reversion.

> [!question]- mkt-pqt-062 | What happens to the microprice during an institutional market order sweep?
> As the sweep consumes the queue on one side, the imbalance moves toward that side's extreme and the volume-weighted mid moves toward the quote being consumed; once the level empties, the mid itself jumps.
> Market makers watching the imbalance cancel or reprice their resting orders on the threatened side before the sweep reaches them, if they are fast enough.

> [!question]- mkt-pqt-063 | What is a markout ratio and how does it diagnose quote shading efficiency?
> The markout ratio compares the PnL per share retained at a horizon (for example 1 second) with the half-spread captured at the fill.
> A ratio near 1 means little of the spread was lost to adverse selection; a ratio near or below 0 means the flow was toxic; comparing it before and after a change in quote shading shows whether the change helped.

> [!question]- mkt-pqt-064 | Why is OFI mainly a contemporaneous explanatory variable rather than a long-horizon forecast?
> The Cont-Kukanov-Stoikov relation links OFI to price changes over the same interval; once the queues are refilled, past OFI says little about later moves.
> Any forecasting power must be tested out of sample at each horizon, because new order flow, news and replenishment of the book soon dominate.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_pqt_02_microprice_ofi.py`](../../code/mkt_pqt_02_microprice_ofi.py) prints and asserts every number on this page: the Example 1 mid, imbalance and microprice in exact rational arithmetic from the weighted-average definition, and the Example 2 OFI two ways, from the Cont-Kukanov-Stoikov indicator formula on book snapshots and by summing the limit, cancel and market-order events that produced those snapshots.
- Related notes: [Desk Roles and Economics](01-Desk-Roles-and-Economics.md), [Order Flow and Adverse Selection](03-Order-Flow-and-Adverse-Selection.md).

## Further reading

- Hasbrouck, J. (2003). *Intraday price formation in U.S. equity index markets*. The Journal of Finance, 58(6), 2375-2400.
- Securities and Exchange Commission (2026). Release No. 34-105656 (June 11, 2026), temporary exemptive relief from the amended Rules 610(c) and 612 of Regulation NMS until the first business day of November 2027.
- Cont, R., Kukanov, A., & Stoikov, S. (2014). *The price impact of order book events*. Journal of Financial Econometrics, 12(1), 47-88.
- Stoikov, S. (2018). *The micro-price: a high-frequency estimator of future prices*. Quantitative Finance, 18(12), 1959-1966.
- Easley, D., López de Prado, M. M., & O'Hara, M. (2012). *Flow toxicity and liquidity in a high-frequency world*. The Review of Financial Studies, 25(5), 1457-1493.
- Gould, M. D., Porter, M. A., Williams, S., McDonald, M., Fenn, D. J., & Howison, S. D. (2013). *Limit order books*. Quantitative Finance, 13(11), 1709-1742.
