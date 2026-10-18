---
type: concept
title: "Order Flow Dynamics, Glosten-Milgrom, and Adverse Selection"
track: [quant-trader, quant-research]
tier: core
status: solid
est_hours: 1.5
tags: [adverse-selection, glosten-milgrom, kyle-lambda, roll-model, lee-ready, microstructure]
prereqs: []
---

# Order Flow Dynamics, Glosten-Milgrom, and Adverse Selection

In financial market microstructure, the bid-ask spread is not merely a toll for processing orders or renting capital.
It is fundamentally an economic risk premium demanded by liquidity providers to protect against trading with better-informed counterparties.
Understanding the classic theoretical foundations - Glosten-Milgrom (1985), Kyle (1985), and Roll (1984) - provides the mathematical tools required to measure, mitigate, and price adverse selection risk.

---

## TL;DR

Adverse selection arises because market makers face an asymmetric information dilemma: uninformed noise traders generate revenue, while informed traders extract wealth.
The Glosten-Milgrom sequential trading model proves that the bid-ask spread must be strictly positive even with zero transaction costs.
Kyle's lambda models continuous price impact as a linear function of order size and private information variance.
Roll's model demonstrates that effective spreads can be inferred directly from the negative serial covariance of transaction returns.

---

## Learning objectives

- Derive the bid and ask quotes under the Glosten-Milgrom sequential Bayesian trade framework.
- Formulate Kyle's lambda model of informed trading and market depth.
- Calculate the Roll (1984) implied effective spread from price covariance sequences.
- Apply the Lee-Ready (1991) trade classification algorithm to identify buyer- and seller-initiated order flow.
- Decompose the quoted bid-ask spread into order processing costs, inventory holding costs, and adverse selection.

---

## Core concepts

### 1. The Glosten-Milgrom (1985) Information Asymmetry Model

Glosten and Milgrom formulated a discrete sequential trading framework where an asset has a true terminal value $V$ that is either high ($V_H$) or low ($V_L$) with prior probability:

$$\mathbb{P}(V = V_H) = p_0, \quad \mathbb{P}(V = V_L) = 1 - p_0$$

The unconditional expected value is $S_0 = p_0 V_H + (1 - p_0) V_L$.
Trading occurs sequentially.
At each step $t$, an incoming trader is either:
- **Informed** with probability $\alpha$: Knows the true value $V$ with certainty.
  If $V = V_H$, they buy; if $V = V_L$, they sell.
- **Uninformed (Noise)** with probability $1 - \alpha$: Buys with probability $\frac{1}{2}$ and sells with probability $\frac{1}{2}$, driven purely by exogenous liquidity needs.

A competitive, risk-neutral market maker posts bid $P_b$ and ask $P_a$ to earn zero expected economic profit conditional on an order arrival:

$$P_a = \mathbb{E}[V \mid \text{Buy}], \quad P_b = \mathbb{E}[V \mid \text{Sell}]$$

Applying Bayes' rule:

$$\mathbb{P}(V = V_H \mid \text{Buy}) = \frac{\mathbb{P}(\text{Buy} \mid V = V_H) \mathbb{P}(V = V_H)}{\mathbb{P}(\text{Buy})}$$

A buy arrives from an informed trader only in the high state, and from a noise trader in either state, so:

$$\mathbb{P}(\text{Buy} \mid V = V_H) = \alpha + \frac{1 - \alpha}{2} = \frac{1 + \alpha}{2}, \quad \mathbb{P}(\text{Buy} \mid V = V_L) = \frac{1 - \alpha}{2}$$

Where the total probability of an incoming buy is:

$$\mathbb{P}(\text{Buy}) = p_0 \frac{1 + \alpha}{2} + (1 - p_0) \frac{1 - \alpha}{2} = \frac{1 + \alpha (2 p_0 - 1)}{2}$$

Thus:

$$\mathbb{P}(V = V_H \mid \text{Buy}) = \frac{p_0 (1 + \alpha)}{1 + \alpha (2 p_0 - 1)} > p_0, \quad \mathbb{P}(V = V_H \mid \text{Sell}) = \frac{p_0 (1 - \alpha)}{1 - \alpha (2 p_0 - 1)} < p_0$$

The ask price is therefore strictly higher than the prior expectation:

$$P_a = V_L + (V_H - V_L) \cdot \frac{p_0 (1 + \alpha)}{1 + \alpha (2 p_0 - 1)} = S_0 + (V_H - S_0) \cdot \frac{2 \alpha p_0}{1 + \alpha (2 p_0 - 1)}$$

Similarly, the bid price satisfies:

$$P_b = S_0 - (S_0 - V_L) \cdot \frac{2 \alpha (1 - p_0)}{1 - \alpha (2 p_0 - 1)}$$

The resulting bid-ask spread $w = P_a - P_b$ is:

$$w = (V_H - V_L) \cdot 2 \alpha p_0 (1 - p_0) \left[\frac{1}{1 + \alpha (2 p_0 - 1)} + \frac{1}{1 - \alpha (2 p_0 - 1)}\right] = (V_H - V_L) \cdot \frac{4 \alpha p_0 (1 - p_0)}{1 - \alpha^2 (2 p_0 - 1)^2}$$

With a symmetric prior $p_0 = \frac{1}{2}$ this collapses to $w = \alpha (V_H - V_L)$, with the quotes at $S_0 \pm \alpha (V_H - S_0)$.

When $\alpha > 0$, the spread is strictly positive even in the complete absence of exchange fees or processing costs.
The spread widens monotonically with the fraction of informed traders $\alpha$ and the fundamental uncertainty $(V_H - V_L)$.

### 2. Kyle's (1985) Auction Model and Lambda

Albert Kyle formulated a batch auction model featuring three types of participants:
1. A single risk-neutral informed insider who observes true value $v \sim \mathcal{N}(p_0, \Sigma_0)$.
2. Noise traders whose aggregate demand is $u \sim \mathcal{N}(0, \sigma_u^2)$, independent of $v$.
3. Competitive market makers who observe total order flow $y = x + u$ and set clearing price $p(y)$.

The market maker sets a linear pricing rule:

$$p(y) = p_0 + \lambda y$$

Where Kyle's lambda is:

$$\lambda = \frac{\text{Cov}(v, y)}{\text{Var}(y)} = \frac{\sqrt{\Sigma_0}}{2 \sigma_u}$$

And the informed trader's optimal trading strategy is linear in their private information:

$$x(v) = \beta (v - p_0), \quad \text{where } \beta = \frac{\sigma_u}{\sqrt{\Sigma_0}}$$

**Key Microstructure Insights from Kyle's Lambda**:
- **Market Depth**: Defined as $1 / \lambda = 2 \sigma_u / \sqrt{\Sigma_0}$. Deep markets accommodate large orders with minimal price impact.
- **Informed Trading Intensity**: When private information uncertainty $\Sigma_0$ is high, $\lambda$ increases, causing steeper price impact.
- **Noise Trader Protection**: Higher noise trading volume $\sigma_u$ dilutes informed flow, reducing $\lambda$ and narrowing price impact.

### 3. Roll's (1984) Effective Spread Model

Richard Roll derived an elegant method to infer the effective bid-ask spread from transaction price dynamics without requiring order book quotes.
Assuming an efficient market where true fundamental value $m_t$ follows a random walk:

$$m_t = m_{t-1} + \epsilon_t, \quad \epsilon_t \sim \text{i.i.d.}(0, \sigma^2)$$

Observed transaction prices $P_t$ fluctuate between the bid ($m_t - s/2$) and ask ($m_t + s/2$):

$$P_t = m_t + q_t \frac{s}{2}$$

Where $s$ is the effective spread and $q_t \in \{-1, +1\}$ is an independent trade direction indicator with $\mathbb{P}(q_t = +1) = \frac{1}{2}$.
The price change $\Delta P_t = P_t - P_{t-1}$ is:

$$\Delta P_t = \epsilon_t + \frac{s}{2} (q_t - q_{t-1})$$

Calculating the autocovariance of price changes:

$$\text{Cov}(\Delta P_t, \Delta P_{t-1}) = \mathbb{E}\left[ \left(\epsilon_t + \frac{s}{2}(q_t - q_{t-1})\right) \left(\epsilon_{t-1} + \frac{s}{2}(q_{t-1} - q_{t-2})\right) \right]$$

Because $\epsilon$ and $q$ are mutually independent, all cross-terms vanish except $\mathbb{E}[-\frac{s^2}{4} q_{t-1}^2] = -\frac{s^2}{4}$:

$$\text{Cov}(\Delta P_t, \Delta P_{t-1}) = -\frac{s^2}{4}$$

Solving for the effective spread $s$:

$$s_{\text{Roll}} = 2 \sqrt{-\text{Cov}(\Delta P_t, \Delta P_{t-1})}$$

When consecutive trades bounce between bid and ask, first-order serial covariance is negative.
A more negative covariance directly implies a wider effective spread.

### 4. Trade Classification: The Lee-Ready (1991) Algorithm

To analyze empirical order flow, researchers must determine whether historical trades were buyer-initiated ($q_t = +1$) or seller-initiated ($q_t = -1$).
The Lee-Ready algorithm assigns trade direction via a two-step hierarchical rule:

1. **Quote Rule**:
   - If trade price $P_t > S_t$ (mid-price of the prevailing NBBO), classify as a **Buy** ($+1$).
   - If trade price $P_t < S_t$, classify as a **Sell** ($-1$).
2. **Tick Rule (Fallback when $P_t = S_t$)**:
   - If the trade occurred at the mid-price, evaluate the sign of the price change relative to the previous different transaction price:
   - If $P_t > P_{t-k}$, classify as a **Buy** ($+1$, an uptick).
   - If $P_t < P_{t-k}$, classify as a **Sell** ($-1$, a downtick).
   - If identical to the previous trade price, carry forward the previous classification.

---

## Worked examples

### Example 1: Glosten-Milgrom Spread Calculation

Consider an asset with binary terminal value:
- Low state: $V_L = \$80.00$.
- High state: $V_H = \$120.00$.
- Symmetric prior: $p_0 = \mathbb{P}(V = V_H) = 0.50$.
- Unconditional expected value: $S_0 = 0.50 \times \$80 + 0.50 \times \$120 = \$100.00$.
- Informed trader fraction: $\alpha = 0.25$ (25% of all incoming traders know $V$ with certainty; 75% are random noise).

1. **Calculate the Ask Price $P_a$**:
   $$\mathbb{P}(\text{Buy} \mid V_H) = \frac{1 + \alpha}{2} = \frac{1 + 0.25}{2} = 0.625, \quad \mathbb{P}(\text{Buy} \mid V_L) = \frac{1 - 0.25}{2} = 0.375$$
   $$\mathbb{P}(\text{Buy}) = 0.50 \times 0.625 + 0.50 \times 0.375 = 0.50$$
   $$\mathbb{P}(V = V_H \mid \text{Buy}) = \frac{0.50 \times 0.625}{0.50} = 0.625$$
   $$P_a = \mathbb{E}[V \mid \text{Buy}] = 0.625 \times \$120.00 + 0.375 \times \$80.00 = \$75.00 + \$30.00 = \$105.00$$

2. **Calculate the Bid Price $P_b$**:
   $$\mathbb{P}(\text{Sell}) = 1 - 0.50 = 0.50$$
   $$\mathbb{P}(V = V_L \mid \text{Sell}) = \frac{0.50 \times 0.625}{0.50} = 0.625$$
   $$\mathbb{P}(V = V_H \mid \text{Sell}) = 0.375$$
   $$P_b = \mathbb{E}[V \mid \text{Sell}] = 0.375 \times \$120.00 + 0.625 \times \$80.00 = \$45.00 + \$50.00 = \$95.00$$

3. **Calculate the Quoted Spread**:
   $$w = P_a - P_b = \$105.00 - \$95.00 = \$10.00$$
   The closed form agrees: $w = \alpha (V_H - V_L) = 0.25 \times \$40.00 = \$10.00$.
   The market maker quotes $\$95.00 \text{ bid} \times \$105.00 \text{ ask}$ around a $\$100.00$ prior.
   An insider who buys at $\$105.00$ in the high state, or sells at $\$95.00$ in the low state, takes $\$15.00$ from the desk; a noise trader pays the desk $\$5.00$ against the prior.
   The desk breaks even: $0.25 \times \$15.00 = 0.75 \times \$5.00 = \$3.75$ per order.

### Example 2: Estimating Roll Effective Spread from Return Series

An analyst collects 5 consecutive transaction prices:
$$P = [\$100.00, \$100.05, \$100.00, \$100.05, \$100.00]$$

1. **Calculate Price Differences $\Delta P_t$**:
   $$\Delta P_1 = \$100.05 - \$100.00 = +0.05$$
   $$\Delta P_2 = \$100.00 - \$100.05 = -0.05$$
   $$\Delta P_3 = \$100.05 - \$100.00 = +0.05$$
   $$\Delta P_4 = \$100.00 - \$100.05 = -0.05$$

2. **Calculate the First-Order Serial Covariance**:
   The mean of $\Delta P$ is $0.00$.
   $$\text{Cov}(\Delta P_t, \Delta P_{t-1}) \approx \frac{1}{3} \sum_{t=2}^{4} (\Delta P_t)(\Delta P_{t-1})$$
   $$= \frac{1}{3} [(-0.05 \times +0.05) + (+0.05 \times -0.05) + (-0.05 \times +0.05)]$$
   $$= \frac{1}{3} [-0.0025 - 0.0025 - 0.0025] = -0.0025$$

3. **Calculate the Roll Implied Spread**:
   $$s_{\text{Roll}} = 2 \sqrt{-\text{Cov}} = 2 \sqrt{-(-0.0025)} = 2 \sqrt{0.0025} = 2 \times 0.05 = \$0.10$$
   The estimate is 10 cents, but the quoted spread in this sample is only 5 cents ($\$100.05 - \$100.00$), so the estimator overstates it by a factor of 2.
   Roll's derivation assumes independent trade signs, under which a 5-cent spread gives an expected covariance of $-s^2/4 = -0.05^2/4 = -0.000625$.
   This sample reverses direction on every trade, the extreme case, so each product is $-s^2 = -0.0025$, four times the expected value, which doubles the implied spread.
   Four price changes are far too few for the estimator; it needs long samples in which trade signs are close to independent.

---

## Pitfalls

- **The Positive Covariance Breakdown in Roll's Model**:
  In trending markets, serial covariance of price changes can be positive due to momentum or auto-correlated order flow.
  In this case, $-\text{Cov} < 0$, making $\sqrt{-\text{Cov}}$ mathematically undefined; practitioners truncate $s$ to zero or use extended Roll estimators.
- **SIP Latency Warping in Lee-Ready Classification**:
  If trade records from direct exchange feeds are compared against delayed SIP quotes, a trade executed at the ask appears to have occurred above the stale ask, distorting trade sign accuracy.
- **Assuming Informed Traders Trade Immediately**:
  Kyle's model assumes informed traders trade patiently to minimize market impact; Glosten-Milgrom assumes immediate execution.
  In reality, institutional algorithms slice orders into TWAP/VWAP child orders that mimic noise traders.
- **Ignoring Inventory Shading**:
  If a market maker skews their quotes to reduce inventory, trades hitting their skewed quote do not represent informed flow, yet a simple adverse selection model will falsely classify them as toxic.

---

## Interview questions

> [!question]- mkt-pqt-065 | What is the fundamental conclusion of the Glosten-Milgrom (1985) model?
> The bid-ask spread is fundamentally an information asymmetry cost rather than an operational processing fee.
> A positive spread exists in equilibrium even under zero transaction costs and perfect market maker competition to offset losses to informed traders.

> [!question]- mkt-pqt-066 | How does an increase in the proportion of informed traders alpha affect the bid-ask spread?
> The spread widens monotonically as alpha increases.
> Market makers face higher expected losses to informed counterparties, forcing them to widen quotes to extract larger compensating profits from noise traders.

> [!question]- mkt-pqt-067 | In Kyle's (1985) continuous auction model, what is Kyle's lambda?
> Lambda is the price impact parameter measuring the change in market clearing price per unit of net order flow: P(y) = P_0 + lambda * y.
> It equals sqrt(Sigma_0) / (2 * sigma_u), where Sigma_0 is asset variance and sigma_u is noise trader variance.

> [!question]- mkt-pqt-068 | What is market depth in Kyle's framework and how is it related to lambda?
> Market depth is defined as the reciprocal of Kyle's lambda: Depth = 1 / lambda = 2 * sigma_u / sqrt(Sigma_0).
> It represents the order volume required to move the market price by one dollar.

> [!question]- mkt-pqt-069 | How does noise trader volatility affect Kyle's lambda and market liquidity?
> Higher noise trader volatility sigma_u increases market depth and decreases lambda.
> Noise flow camouflages the informed trader's orders, enabling market makers to quote tighter spreads without incurring excessive adverse selection.

> [!question]- mkt-pqt-070 | State the Roll (1984) model equation for effective bid-ask spread.
> Spread = 2 * sqrt(-Cov(Delta P_t, Delta P_{t-1})).
> It derives the unobservable effective spread from the negative serial autocovariance of successive transaction price changes.

> [!question]- mkt-pqt-071 | What causes the negative first-order serial covariance in transaction prices assumed by Roll?
> The bid-ask bounce: successive trades bouncing randomly between buyer-initiated trades at the ask and seller-initiated trades at the bid.
> This bounce creates negative serial correlation even if the underlying fundamental value follows a pure random walk.

> [!question]- mkt-pqt-072 | What is the primary limitation of Roll's effective spread estimator in empirical data?
> Empirical price change autocovariance is frequently positive in trending markets or during institutional sweeps.
> When Cov(Delta P_t, Delta P_{t-1}) > 0, the term under the square root is negative, causing the basic Roll formula to fail.

> [!question]- mkt-pqt-073 | Explain the two rules comprising the Lee-Ready (1991) trade classification algorithm.
> 1. Quote Rule: Trades executed above the prevailing midpoint are buys (+1); trades below the midpoint are sells (-1).
> 2. Tick Rule: Trades at the midpoint are buys if the price is higher than the previous different trade price (uptick), and sells if lower (downtick).

> [!question]- mkt-pqt-074 | What is the 5-second quote delay convention in historical Lee-Ready implementations?
> Historically, exchange quote reporting suffered transmission delays relative to trade prints.
> Researchers matched trades against quotes posted 5 seconds prior to avoid misclassifying trades against quotes that adjusted post-trade.

> [!question]- mkt-pqt-075 | What are the three classic components of the quoted bid-ask spread?
> 1. Order Processing Costs: Clearing, exchange fees, technology, and labor expenses.
> 2. Inventory Holding Costs: Financing margin and the risk of adverse price drift while warehousing inventory.
> 3. Adverse Selection Costs: Losses suffered by trading against informed counterparties.

> [!question]- mkt-pqt-076 | How does Hasbrouck's Vector Autoregression (VAR) framework decompose price discovery?
> It models trade arrivals and quote revisions jointly as a bivariate VAR system.
> The permanent price impact of a trade innovation measures the true private information content, while transient impact measures inventory noise.

> [!question]- mkt-pqt-077 | What is the difference between temporary and permanent price impact?
> Temporary impact is a transient price displacement caused by local liquidity depletion that mean-reverts over time.
> Permanent impact reflects the private information conveyed by the trade, causing a permanent shift in the asset's fundamental fair value.

> [!question]- mkt-pqt-078 | What is the Square-Root Law of market impact?
> The empirical finding that the total transaction price impact of an execution scales with the square root of the trade size normalized by daily volume: Impact ~ Y * sigma * sqrt(Q / V).
> It holds universally across equities, fixed income, futures, and crypto.

> [!question]- mkt-pqt-079 | Why does the Square-Root Law exhibit sub-linear rather than linear price impact?
> Large institutional orders are executed via endogenous algorithmic scheduling that slows down execution when liquidity is scarce.
> Furthermore, latent supply and demand in the broader market enters the book non-linearly as prices reach attractive levels.

> [!question]- mkt-pqt-080 | How does high market fragmentation (e.g. 16 US equity exchanges) impact adverse selection?
> Fragmentation increases adverse selection risk for passive market makers.
> An informed trader sweeps liquidity across all venues simultaneously, filling resting limit orders on every exchange before quotes can cancel.

> [!question]- mkt-pqt-081 | What is a trade-through and which SEC regulation prohibits it?
> A trade-through occurs when an exchange executes an order at a price inferior to the National Best Bid or Offer displayed on another exchange.
> SEC Regulation NMS Rule 611 (Order Protection Rule) strictly prohibits trade-throughs on protected quotes.

> [!question]- mkt-pqt-082 | What is a locked or crossed market and why is it unstable?
> A locked market occurs when the best bid equals the best offer; a crossed market occurs when the best bid exceeds the best offer.
> It represents an instantaneous arbitrage opportunity that high-frequency algorithms immediately eliminate by crossing the spread.

> [!question]- mkt-pqt-083 | What is a toxic quote snipe?
> An aggressive marketable order sent to pick off a stale resting limit order that has not yet updated to reflect new external information.
> The market maker is filled at an obsolete price and immediately incurs an adverse markout loss.

> [!question]- mkt-pqt-084 | What is the Tick Size Pilot program conducted by the SEC in 2016?
> An experimental regulatory trial that widened minimum quoting and trading ticks from $0.01 to $0.05 for selected small-cap US equities.
> It resulted in significantly wider quoted spreads and higher execution costs for retail investors without improving market depth.

> [!question]- mkt-pqt-085 | How does asymmetric information decay over time in the Glosten-Milgrom framework?
> As successive trades occur, Bayesian market makers observe order flow signs and update their posterior belief p_t toward the true state.
> The spread progressively collapses toward zero as the market maker's uncertainty is eliminated by the order history.

> [!question]- mkt-pqt-086 | Why do market makers widen spreads ahead of scheduled macroeconomic announcements?
> Pre-announcement information uncertainty (V_H - V_L) expands dramatically while noise trading volume contracts.
> Market makers must widen quotes to defend against leakage or rapid algorithmic interpretation by specialized news-feed scrapers.

> [!question]- mkt-pqt-087 | What is an informed trader's optimal trading rate in Kyle's continuous-time formulation?
> The informed trader trades at a constant rate that gradually incorporates their private information into the market price over the trading day.
> Trading too quickly causes severe self-inflicted price impact, while trading too slowly leaves profitable alpha uncaptured at market close.

> [!question]- mkt-pqt-088 | In empirical market microstructure, what is the effective half-spread?
> Effective Half-Spread = q_t * (P_t - S_t), where q_t is the trade direction (+1 for buy, -1 for sell), P_t is transaction price, and S_t is mid-price.
> It measures the actual half-spread paid by the trader relative to the prevailing midpoint at execution time.

> [!question]- mkt-pqt-089 | What is the realized half-spread and how does it measure market maker profit?
> Realized Half-Spread = q_t * (P_t - S_{t + tau}), where tau is a post-trade horizon (e.g. 5 minutes).
> It subtracts the adverse selection price drift (S_{t + tau} - S_t) from the effective spread, isolating the net revenue retained by the liquidity provider.

> [!question]- mkt-pqt-090 | What is price discovery and where does it primarily occur in fragmented equity markets?
> Price discovery is the process through which new information is incorporated into the equilibrium market clearing price.
> It occurs predominantly on lit primary exchanges with deep displayed liquidity and high quote turnover, such as NASDAQ and the NYSE.

> [!question]- mkt-pqt-091 | Why do wholesale internalizers offer price improvement to retail orders?
> Internalizers execute retail trades inside the NBBO (e.g. at $100.005 when the lit quote is $100.00 x $100.01).
> Because retail orders carry zero adverse selection, the internalizer gladly sacrifices a fraction of a cent to capture the remainder of the spread risk-free.

> [!question]- mkt-pqt-092 | What is the inventory effect on quote positioning in market microstructure?
> A market maker with excessive long inventory lowers both its bid and ask quotes below fair value.
> This discourages incoming sellers while incentivizing incoming buyers to relieve the desk of its inventory risk.

> [!question]- mkt-pqt-093 | How does high-frequency trading (HFT) affect the adverse selection component of the spread?
> HFT market makers update quotes within microseconds of information arrivals, reducing their vulnerability to stale quote snipes.
> This allows them to quote narrower spreads during calm regimes, though spreads widen abruptly when volatility surges.

> [!question]- mkt-pqt-094 | What is the Campbell-Grossman-Wang (1993) model of volume and return autocorrelation?
> It shows that stock returns accompanied by high trading volume exhibit greater negative first-order serial correlation (reversal).
> Volume-driven price moves reflect liquidity provision by risk-averse investors who demand price discounts that subsequently mean-revert.

> [!question]- mkt-pqt-095 | Explain the difference between lit market depth and dark pool crossing volume.
> Lit market depth consists of publicly displayed, binding limit orders that establish the NBBO and contribute directly to price discovery.
> Dark pools execute unadvertised child orders pegged to lit midpoints without displaying pre-trade quotes, contributing to volume but not lit depth.

> [!question]- mkt-pqt-096 | How do market makers detect that a single large institutional parent order is active in the market?
> By observing persistent, one-sided Order Flow Imbalance, abnormal fill rates at the ask across multiple venues, and lack of mid-price mean reversion.
> Upon detecting an active institutional algorithm, market makers pull resting passive quotes and shade prices defensively.

---

## Further reading

- Glosten, L. R., & Milgrom, P. R. (1985). *Bid, ask and transaction prices in a specialist market with heterogeneously informed traders*. Journal of Financial Economics, 14(1), 71-100.
- Kyle, A. S. (1985). *Continuous auctions and insider trading*. Econometrica, 53(6), 1315-1335.
- Roll, R. (1984). *A simple implicit measure of the effective bid-ask spread in an efficient market*. The Journal of Finance, 39(4), 1127-1139.
- Lee, C. M., & Ready, M. J. (1991). *Inferring trade direction from intraday data*. The Journal of Finance, 46(2), 733-746.
