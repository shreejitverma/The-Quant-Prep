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
The microprice incorporates Level 1 book imbalance to produce a superior, martingale estimate of the next transaction price.
Order Flow Imbalance (OFI) measures the net change in available liquidity at the best quotes and exhibits a strong linear relationship with contemporaneous price changes.
In multi-asset frameworks, fair value is anchored to high-volume price leaders (such as index futures) that lead cash equities by milliseconds.

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

Sasha Stoikov (2018) established that the classical volume-weighted microprice is not a martingale with respect to the order book filtration because it fails to account for spread width regimes and transition probabilities.
Stoikov defines fair value as the expected mid-price at the arrival of the next mid-price move:

$$P_{\text{micro}}^*(s, I, w) = \lim_{t \to \tau} \mathbb{E}[S_t \mid S_0 = s, I_0 = I, w_0 = w]$$

Where $\tau$ is the first stopping time at which $S_\tau \neq S_0$.
By discretizing imbalance into finite states $k \in \{1, \dots, K\}$ and spread into ticks $w \in \{1, 2\}$, the microprice solves the Poisson linear system:

$$P_{\text{micro}}^* = S + G \cdot \Delta S$$

where $G = (I - Q)^{-1} R$, $Q$ is the transition rate matrix among non-absorbing states, and $R$ represents transition rates into mid-change absorbing states.

### 4. Cont-Kukanov-Stoikov Order Flow Imbalance (OFI)

Cont, Kukanov, and Stoikov (2014) showed that price changes over discrete intervals $\Delta t$ are driven by the accumulation of net order flow at the best quotes.
Let $P_{b,t}, Q_{b,t}$ and $P_{a,t}, Q_{a,t}$ denote best quotes and sizes at time $t$.
Order Flow Imbalance between $t-1$ and $t$ is formulated as:

$$\text{OFI}_t = e_{b,t} - e_{a,t}$$

Where the bid contribution $e_{b,t}$ is:

$$e_{b,t} = \begin{cases} Q_{b,t} & \text{if } P_{b,t} > P_{b,t-1} \\ Q_{b,t} - Q_{b,t-1} & \text{if } P_{b,t} = P_{b,t-1} \\ -Q_{b,t-1} & \text{if } P_{b,t} < P_{b,t-1} \end{cases}$$

And the ask contribution $e_{a,t}$ is:

$$e_{a,t} = \begin{cases} -Q_{a,t-1} & \text{if } P_{a,t} > P_{a,t-1} \\ Q_{a,t} - Q_{a,t-1} & \text{if } P_{a,t} = P_{a,t-1} \\ Q_{a,t} & \text{if } P_{a,t} < P_{a,t-1} \end{cases}$$

Empirically, contemporaneous price changes follow a strong linear relation:

$$\Delta S_t = \beta \cdot \text{OFI}_t + \epsilon_t$$

The coefficient $\beta$ represents the market depth parameter (inverse Kyle's lambda) in units of price change per contract of net order flow.

---

## Worked examples

### Example 1: Asymmetric Queue Microprice vs Quoted Mid

Consider an equity trading with a 2-cent spread:
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

Track three consecutive market updates for a security:

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
  Empirical price impact $\beta = \frac{\$0.050}{1,100} = \$0.00004545$ per share ($4.55\text{ cents per 1,000 shares}$).

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
> As the conditional expectation of the mid-price at the first future stopping time tau when the mid-price changes: P_micro = E[S_tau | S_0, I_0, w_0].
> This martingale formulation accounts for transition rates across spread and imbalance states.

> [!question]- mkt-pqt-036 | What is Order Flow Imbalance (OFI) as defined by Cont, Kukanov, and Stoikov (2014)?
> OFI measures the net change in shares available at the best bid and offer across discrete market updates.
> It quantifies the net balance between newly placed limit orders, market order fills, and order cancellations.

> [!question]- mkt-pqt-037 | What is the mathematical relationship between contemporaneous price change and OFI?
> Delta S_t = beta * OFI_t + epsilon_t.
> Contemporaneous price changes exhibit an exceptionally tight linear relationship with net order flow imbalance.

> [!question]- mkt-pqt-038 | What does the regression slope beta represent in the OFI price impact equation?
> Beta represents the inverse of market depth, measuring the dollar price impact per share of net order flow imbalance.
> Higher beta indicates lower market liquidity and greater vulnerability to market sweeps.

> [!question]- mkt-pqt-039 | Why does the E-mini S&P 500 futures contract lead the SPY ETF in price discovery?
> The futures market has higher leverage, lower transaction fees, centralized 24-hour trading, and higher institutional volume.
> Information reflects in the futures order book microseconds before arbitrageurs propagate it to the fragmented cash equity market.

> [!question]- mkt-pqt-040 | How do quantitative desks exploit lead-lag relationships in ETF market making?
> They calculate a synthetic fair value for the ETF by multiplying the real-time index futures price by the hedge ratio.
> When the ETF quoted mid deviates from synthetic fair value, they quote aggressively to capture the expected convergence.

> [!question]- mkt-pqt-041 | What is a "thick book" versus a "thin book" stock in market microstructure?
> A thick book has a bid-ask spread constrained to the minimum tick size ($0.01) with deep queues (thousands of shares) at the best quotes.
> A thin book has a wide spread (multiple ticks) with sparse queues that frequently gap across price levels.

> [!question]- mkt-pqt-042 | Why is the Level 1 microprice more predictive in thick books than in thin books?
> In thick books, price cannot adjust continuously through the spread, so queue size exhaustion is the sole mechanism preceding a price move.
> In thin books, quote cancellations and wider spreads introduce multi-level dynamics that Level 1 imbalance fails to capture.

> [!question]- mkt-pqt-043 | How do iceberg orders undermine the predictive power of the volume-weighted microprice?
> Iceberg orders conceal substantial non-displayed size, making a queue appear artificially thin.
> The microprice predicts a price break toward the thin side, only for aggressive orders to be repeatedly absorbed by the hidden tranche.

> [!question]- mkt-pqt-044 | What is the Cancel-to-Trade Ratio (CTR) and what does a high ratio signify?
> CTR is the number of order cancellations divided by the number of executed trades, often exceeding 20:1 in modern electronic markets.
> A high CTR signifies intense latency competition and rapid quote shading rather than durable liquidity provision.

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
> Rule 612 of SEC Regulation NMS prohibits sub-penny quotes for stocks priced above $1.00, enforcing a strict 1-cent minimum tick size.
> This constraint artificially widens spreads on low-priced liquid stocks, creating massive queue backlogs and high adverse selection.

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
> Fills with persistently positive post-trade drift indicate high information content (toxic flow).

> [!question]- mkt-pqt-057 | Why does cross-venue consolidation introduce latency jitter into fair value calculations?
> Market data feeds from NASDAQ, NYSE, and Cboe arrive asynchronously over microwave and fiber links.
> A consolidated quote engine must resolve race conditions where one venue's tick arrives milliseconds out of chronological sequence.

> [!question]- mkt-pqt-058 | What is the role of a Securities Information Processor (SIP) versus direct market feeds?
> The SIP consolidates and publishes the official NBBO across all exchanges, but incurs 10 to 50 microseconds of aggregation latency.
> HFT prop desks bypass the SIP and construct their own proprietary consolidated tape from direct multicast exchange feeds.

> [!question]- mkt-pqt-059 | What is the Trade-Through Rule (Rule 611 of Regulation NMS)?
> Rule 611 requires trading venues to establish policies preventing the execution of orders at price levels inferior to protected quotes on other exchanges.
> It enforces national price priority across lit US trading centers.

> [!question]- mkt-pqt-060 | How does an inverted exchange exploit queue priority?
> Traders who are unwilling to wait at the back of a 50,000-share queue on a maker-taker exchange route to an inverted venue where queues are short.
> They pay a taker fee or accept a lower maker rebate to achieve immediate queue execution.

> [!question]- mkt-pqt-061 | In statistical arbitrage, how is the cointegration spread used as a fair value anchor?
> For two cointegrated assets X and Y, their long-term spread S = Y - beta * X is stationary with a constant mean.
> When S deviates significantly from its historical mean, the desk prices fair value expecting mean reversion.

> [!question]- mkt-pqt-062 | What happens to the microprice during an institutional market order sweep?
> The microprice violently jumps through the opposite quote as resting depth on the target side is completely annihilated in zero microseconds.
> Algorithms monitoring microprice velocity trigger defensive quote cancellations before their resting orders are filled.

> [!question]- mkt-pqt-063 | What is a markout ratio and how does it diagnose quote shading efficiency?
> The markout ratio compares the net PnL captured at 1 second to the theoretical half-spread quoted at trade time.
> A markout ratio above 0.50 indicates that quote shading successfully absorbed flow without conceding excessive adverse selection.

> [!question]- mkt-pqt-064 | Why does the predictive power of OFI decay rapidly beyond a 5-second horizon?
> Order flow imbalance at the top of the book is a high-frequency, localized phenomenon.
> Beyond several seconds, macroeconomic releases, institutional algorithmic scheduling, and broader liquidity replenishment dominate price discovery.

---

## Further reading

- Cont, R., Kukanov, A., & Stoikov, S. (2014). *The price impact of order book events*. Journal of Financial Econometrics, 12(1), 47-88.
- Stoikov, S. (2018). *The micro-price: a high-frequency estimator of future prices*. Quantitative Finance, 18(12), 1959-1966.
- Easley, D., López de Prado, M. M., & O'Hara, M. (2012). *Flow toxicity and liquidity in a high-frequency world*. The Review of Financial Studies, 25(5), 1457-1493.
- Gould, M. D., Porter, M. A., Williams, S., McDonald, M., Fenn, D. J., & Howison, S. D. (2013). *Limit order books*. Quantitative Finance, 13(5), 757-786.
