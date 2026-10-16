---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [limit-order-books-and-order-types, conditional-probability-and-bayes]
est_hours: 4
sources: [Roll (1984) A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market. Journal of Finance 39(4) 1127-1139, Glosten and Milgrom (1985) Bid Ask and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders. Journal of Financial Economics 14(1) 71-100, Glosten and Harris (1988) Estimating the Components of the Bid/Ask Spread. Journal of Financial Economics 21(1) 123-142, Huang and Stoll (1997) The Components of the Bid-Ask Spread - A General Approach. Review of Financial Studies 10(4) 995-1034, Madhavan Richardson and Roomans (1997) Why Do Security Prices Change? A Transaction-Level Analysis of NYSE Stocks. Review of Financial Studies 10(4) 1035-1064, Hasbrouck (2007) Empirical Market Microstructure. Oxford University Press - chapters 3 to 5, O'Hara (1995) Market Microstructure Theory. Blackwell - chapters 2 and 3]
---

# Spread Models: Roll and Glosten-Milgrom

## TL;DR

- Roll: if trades bounce between bid and ask around a random-walk value, consecutive price changes are negatively correlated with $\text{Cov}(\Delta p_t, \Delta p_{t-1}) = -c^2$, so the half-spread is $c = \sqrt{-\text{Cov}}$.
- Roll breaks when trade signs are persistent (it then estimates $c(1 - \rho)$), when quotes move with trades (adverse selection), or in short samples where the autocovariance is positive and the estimator is undefined.
- Glosten-Milgrom: a competitive, risk-neutral market maker facing some informed traders sets ask $= \mathbb{E}[V \mid \text{buy}]$ and bid $= \mathbb{E}[V \mid \text{sell}]$; the spread exists purely because trades carry information.
- In Glosten-Milgrom the market maker breaks even: losses to informed traders equal gains from uninformed ones, quotes are martingales, and the spread narrows as trades reveal the value.
- Empirically the spread splits into an order-processing (transitory) part and an adverse-selection (permanent) part, which a regression of price changes on current and lagged trade signs separates.

## Learning objectives

- Derive the Roll estimator of the effective spread.
- Solve the Glosten-Milgrom model and explain the adverse-selection spread.
- Decompose the spread into order-processing, inventory and adverse-selection components.
- Implement the Roll estimator and recover the spread from simulated trades, and know when it fails.

## Core concepts

### Why spreads exist

Three costs are compensated by the bid-ask spread.

| Component | Source | Effect on prices after a trade |
| :--- | :--- | :--- |
| Order processing | Fixed costs of operating, fees, compensation for immediacy | Transitory: the price bounces back |
| Inventory | The dealer's risk from holding an unwanted position | Transitory: quotes shade to rebalance, then revert |
| Adverse selection | Some counterparties know more about value | Permanent: the trade moves the expected value |

Roll's model has only the first, Glosten-Milgrom only the third, and the empirical decompositions measure their mix.

### The Roll model

Let the efficient price follow a random walk and trades occur at the bid or the ask:

$$
m_t = m_{t-1} + u_t, \quad u_t \sim (0, \sigma^2) \text{ iid}, \qquad p_t = m_t + c\, q_t, \quad q_t \in \{-1, +1\} \text{ iid, equally likely, independent of } u.
$$

Then $\Delta p_t = u_t + c(q_t - q_{t-1})$, and since $\mathbb{E}[q_t q_s] = 0$ for $t \ne s$:

$$
\text{Var}(\Delta p_t) = \sigma^2 + 2c^2, \qquad \text{Cov}(\Delta p_t, \Delta p_{t-1}) = c^2\, \mathbb{E}[(q_t - q_{t-1})(q_{t-1} - q_{t-2})] = -c^2 .
$$

All higher-lag autocovariances are zero.
The Roll estimator is therefore

$$
\hat c = \sqrt{-\widehat{\text{Cov}}(\Delta p_t, \Delta p_{t-1})}, \qquad \widehat{S} = 2\hat c,
$$

an estimate of the effective spread from trade prices alone, with no quote data.
That is its practical value: it works on historical data, daily closes and markets without quote records, and it underlies modern low-frequency estimators (Hasbrouck's Gibbs-sampler version of the Roll model, and high-low estimators such as Corwin and Schultz).

Failure modes interviewers probe:

- Persistent order flow.
  If $q_t$ is a Markov chain with autocorrelation $\rho$, then $\text{Cov}(\Delta p_t, \Delta p_{t-1}) = c^2(2\rho - 1 - \rho^2) = -c^2(1-\rho)^2$, so Roll estimates $c(1 - \rho)$, biased down.
  Trade signs are strongly positively autocorrelated in real markets because large orders are split, so this bias is the norm.
- Adverse selection.
  If each trade moves the efficient price, $m_t = m_{t-1} + \theta q_t + u_t$ and $p_t = m_t + \phi q_t$, the autocovariance is $-\phi(\theta + \phi)$, so Roll returns $\sqrt{\phi(\theta+\phi)}$, between the transitory part $\phi$ and the half-spread $\theta + \phi$.
- Sampling error.
  When $\sigma$ is large relative to $c$, the sample autocovariance is often positive in short windows and the estimator is undefined; practitioners set it to zero or switch to a Bayesian version.

### The Glosten-Milgrom model

Value $V \in \{V_L, V_H\}$ with $P(V = V_H) = \pi$.
Traders arrive one at a time; with probability $\mu$ the trader is informed and buys if $V = V_H$, sells if $V = V_L$; otherwise the trader is uninformed and buys or sells with probability one half.
A competitive, risk-neutral market maker with no costs posts a bid and an ask before each trade and earns zero expected profit on each, so

$$
a = \mathbb{E}[V \mid \text{buy}], \qquad b = \mathbb{E}[V \mid \text{sell}].
$$

Bayes' rule with $P(\text{buy} \mid V_H) = \mu + \tfrac{1-\mu}{2}$ and $P(\text{buy} \mid V_L) = \tfrac{1-\mu}{2}$ gives

$$
P(V_H \mid \text{buy}) = \frac{\pi\,(1 + \mu)}{\pi(1+\mu) + (1-\pi)(1-\mu)}, \qquad P(V_H \mid \text{sell}) = \frac{\pi\,(1 - \mu)}{\pi(1-\mu) + (1-\pi)(1+\mu)},
$$

and $a = V_L + (V_H - V_L) P(V_H \mid \text{buy})$, $b = V_L + (V_H - V_L) P(V_H \mid \text{sell})$.
At $\pi = \tfrac12$ the quotes are symmetric around $\bar V$ with half-spread $\mu (V_H - V_L)/2$, the result in [Adverse Selection and Flow Toxicity](05-Adverse-Selection-and-Flow-Toxicity.md).

Properties worth stating in an interview:

- The spread is positive whenever $0 < \mu$ and $0 < \pi < 1$, even with zero costs and risk neutrality: it is pure adverse selection.
- It widens with the share of informed traders $\mu$ and the value uncertainty $V_H - V_L$.
- The market maker breaks even only on average: it loses to informed traders and gains the same amount from uninformed ones, so uninformed traders pay for the information.
- Transaction prices are martingales with respect to public information: each trade prints at $\mathbb{E}[V \mid \text{history including this trade}]$, so trade-price changes are serially uncorrelated and a Roll estimator applied to Glosten-Milgrom prices sees no bounce at all (pure adverse selection is the $\phi = 0$ case above).
- After each trade the prior $\pi$ updates and both quotes move toward the trade's side; the quote midpoint is not in general a martingale, because the market maker's expectation sits off-centre between bid and ask whenever $\pi \ne \tfrac12$.
- With repeated trading the posterior converges to the truth and the spread converges to zero.
- In the basic model uninformed traders trade whatever the quotes, so the market operates for any $\mu < 1$; with price-elastic uninformed demand (an extension Glosten and Milgrom discuss) a large enough informed share widens the spread until the uninformed withdraw and the market shuts down.

### Spread decomposition

Write $q_t$ for the trade sign, $\phi$ for the transitory half-spread (order processing and inventory) and $\theta$ for the permanent impact per trade:

$$
m_t = m_{t-1} + \theta q_t + u_t, \qquad p_t = m_t + \phi q_t \quad\Longrightarrow\quad \Delta p_t = (\theta + \phi)\, q_t - \phi\, q_{t-1} + u_t .
$$

Regressing $\Delta p_t$ on $q_t$ and $q_{t-1}$ recovers both: the coefficient on $q_{t-1}$ is $-\phi$ and the sum of coefficients is $\theta$.
This is the iid-sign special case of Madhavan, Richardson and Roomans (1997), who add autocorrelation in $q_t$, and close to Glosten and Harris (1988).
Huang and Stoll (1997) separate the inventory component from order processing by using the autocorrelation of trade signs: inventory-driven quote shading makes the next trade more likely to be on the opposite side.

In practice desks use the closely related effective, realized and price-impact spreads measured against quotes, because quote data are available; see [Adverse Selection and Flow Toxicity](05-Adverse-Selection-and-Flow-Toxicity.md).
The model-based decomposition is what you reach for when you only have trades, or when an interviewer asks why prices move after trades.

## Worked examples

### Example 1: recover the spread from simulated trades

Simulate 200,000 trades with $c = 0.05$, $\sigma = 0.10$ and iid signs (seed 1).
Theory: $\text{Var}(\Delta p) = 0.01 + 2 \times 0.0025 = 0.015$ and $\text{Cov} = -0.0025$.
The sample gives $\text{Var} \approx 0.01491$ and $\text{Cov} \approx -0.00247$, so $\hat c \approx 0.0497$ and $\widehat S \approx 0.0994$ against a true spread of 0.10.

```python
import numpy as np

rng = np.random.default_rng(1)
n, c, sigma = 200_000, 0.05, 0.10
p = 100 + np.cumsum(sigma * rng.standard_normal(n)) + c * rng.choice([-1.0, 1.0], n)
d = np.diff(p) - np.diff(p).mean()
print(2 * np.sqrt(-np.mean(d[1:] * d[:-1])))  # about 0.0994
```

### Example 2: three ways Roll goes wrong

- Persistent flow, $\rho = 0.5$: theory says Roll returns $c(1 - \rho) = 0.025$; the simulation returns about 0.0249, half the true half-spread.
- Adverse selection, $\theta = 0.02$, $\phi = 0.03$: Roll returns $\sqrt{0.03 \times 0.05} = 0.0387$ (simulated about 0.0387) against a true half-spread of 0.05.
- Short windows: with $c = 0.02$ and $\sigma = 0.10$, about 34.5% of 50-trade windows have a non-negative first-order autocovariance (20,000 windows), so the estimator is undefined a third of the time.

### Example 3: Glosten-Milgrom quotes with an asymmetric prior

"$V \in \{95, 105\}$, $P(V_H) = 0.4$, 25% of traders informed."
The prior mean is 99.
$P(\text{buy} \mid V_H) = 0.625$ and $P(\text{buy} \mid V_L) = 0.375$, so $P(V_H \mid \text{buy}) = 0.25/0.475 = 0.5263$ and the ask is $95 + 10 \times 0.5263 = 100.263$.
$P(V_H \mid \text{sell}) = 0.15/0.525 = 0.2857$, so the bid is 97.857.
The spread is 2.406, and it is asymmetric around the prior mean: 1.263 above and 1.143 below, because a buy is more surprising when $V_H$ is less likely.
Zero profit check: uninformed traders lose $(1 - \mu) \times \tfrac12 \times 2.406 = 0.902$ per trade on average, exactly what the informed gain, and the market maker's expected profit is zero.

### Example 4: learning in Glosten-Milgrom

Same parameters, true value $V_H$, 20,000 simulated trade sequences (seed 2):

| Trades | Mean $P(V_H)$ | Mean spread |
| ---: | ---: | ---: |
| 0 | 0.4000 | 2.4060 |
| 10 | 0.6504 | 1.5996 |
| 25 | 0.8225 | 0.8565 |
| 50 | 0.9340 | 0.3242 |

The spread collapses as order flow reveals the value: informed trading is self-limiting because it teaches the market maker.

### Example 5: decompose the spread from trades

Simulate $\theta = 0.02$, $\phi = 0.03$, $\sigma_u = 0.03$ (seed 3) and regress $\Delta p_t$ on $q_t, q_{t-1}$.
The coefficients are about 0.0500 and -0.0300, so $\hat\phi \approx 0.0300$, $\hat\theta \approx 0.0199$, and adverse selection is about 39.9% of the half-spread.
A market maker facing this flow keeps $\phi$ per trade on average and loses $\theta$ to the permanent move.

## Pitfalls

- Applying Roll to data with persistent trade signs (split orders) and reading the downward-biased number as the true spread.
- Reporting a Roll spread of zero when the autocovariance is positive as if it were a measurement; it is undefined, and any convention (set to zero, Bayesian version) must be stated.
- Using quote midpoints in Roll; it needs transaction prices, because the bounce is the signal.
- Saying Glosten-Milgrom spreads come from risk aversion or inventory; the model has neither.
- Forgetting the asymmetry: with an unequal prior the quotes are not symmetric around the prior mean.
- Treating the market maker's zero expected profit as zero profit per trade; it loses on every informed trade.
- Interpreting the regression coefficient on $q_t$ as the adverse-selection component; it is $\theta + \phi$.

## Interview questions

> [!question]- ms-spread-roll-derivation | Derive the Roll estimator.
> With $p_t = m_t + c q_t$, $m$ a random walk and iid equally likely signs, $\Delta p_t = u_t + c(q_t - q_{t-1})$ and $\text{Cov}(\Delta p_t, \Delta p_{t-1}) = -c^2$.
> So $c = \sqrt{-\text{Cov}}$ and the spread is $2c$.

> [!question]- ms-spread-roll-variance | In the Roll model, what is $\text{Var}(\Delta p_t)$?
> $\sigma^2 + 2c^2$.
> The bounce adds $c^2 \text{Var}(q_t - q_{t-1}) = 2c^2$ to the efficient-price variance.

> [!question]- ms-spread-roll-numeric | First-order autocovariance of trade price changes is $-0.0004$. What spread does Roll imply?
> 0.04: $c = \sqrt{0.0004} = 0.02$, spread $2c$.

> [!question]- ms-spread-roll-positive-cov | The sample autocovariance is positive. What do you report?
> The Roll estimator is undefined; do not report zero.
> Use a longer window, a Bayesian (Gibbs) version, or a different estimator such as a high-low estimator.

> [!question]- ms-spread-roll-persistence | Trade signs have autocorrelation $\rho$. What does Roll estimate?
> $c(1 - \rho)$, because the autocovariance becomes $-c^2(1 - \rho)^2$.
> With $\rho = 0.5$ it reports half the true half-spread.

> [!question]- ms-spread-roll-adverse | With permanent impact $\theta$ and transitory half-spread $\phi$ per trade, what does Roll return?
> $\sqrt{\phi(\theta + \phi)}$, between $\phi$ and the true half-spread $\theta + \phi$.
> Permanent impact does not bounce back, so it is invisible to a reversal-based estimator.

> [!question]- ms-spread-gm-quotes | State the Glosten-Milgrom quoting rule.
> Ask $= \mathbb{E}[V \mid \text{buy}]$ and bid $= \mathbb{E}[V \mid \text{sell}]$.
> A competitive, risk-neutral market maker breaks even on each side given the information in the trade itself.

> [!question]- ms-spread-gm-symmetric | $V \in \{48, 52\}$ equally likely, 40% informed. Quotes?
> Bid 49.2, ask 50.8.
> Half-spread $\mu (V_H - V_L)/2 = 0.4 \times 2 = 0.8$.

> [!question]- ms-spread-gm-asymmetric | $V \in \{95, 105\}$, $P(V_H) = 0.4$, 25% informed. What is the ask?
> About 100.263.
> $P(V_H \mid \text{buy}) = 0.4 \times 0.625 / (0.4 \times 0.625 + 0.6 \times 0.375) = 0.5263$.

> [!question]- ms-spread-gm-zero-profit | Who pays for the informed traders' profits in Glosten-Milgrom?
> The uninformed traders, through the spread.
> The market maker's losses to the informed equal its gains from the uninformed, so its expected profit is zero.

> [!question]- ms-spread-gm-why-no-risk | Why is there a spread in Glosten-Milgrom even with a risk-neutral, cost-free market maker?
> Because a buy is more likely when value is high, the expected value conditional on a buy exceeds that conditional on a sell.
> The spread prices adverse selection alone.

> [!question]- ms-spread-gm-learning | What happens to Glosten-Milgrom spreads over a sequence of trades?
> They narrow toward zero as the posterior converges to the true value.
> In the simulated example the mean spread falls from 2.406 to about 0.324 after 50 trades.

> [!question]- ms-spread-gm-martingale | Are Glosten-Milgrom transaction prices predictable?
> No: each trade prints at the market maker's updated expectation of $V$ given all trades so far, so transaction prices form a martingale and their changes are serially uncorrelated.
> There is no Roll-style bounce (Roll would estimate a zero spread), even though the quoted spread is positive; the midpoint itself need not be a martingale when the posterior is not one half.

> [!question]- ms-spread-components | Name the three components of the spread and how each shows up after a trade.
> Order processing and inventory are transitory (prices revert); adverse selection is permanent (the expected value moves).
> The split is estimated from how much of the post-trade move reverses.

> [!question]- ms-spread-mrr-regression | $\Delta p_t$ regressed on $q_t$ and $q_{t-1}$ gives 0.06 and -0.04. Decompose the half-spread.
> Transitory $\phi = 0.04$, permanent $\theta = 0.02$, half-spread 0.06, adverse-selection share one third.
> The lag coefficient is $-\phi$ and the sum of coefficients is $\theta$.

> [!question]- ms-spread-inventory-identification | How do Huang and Stoll separate inventory from order-processing costs?
> Through the autocorrelation of trade signs: a dealer who shades quotes to unload inventory makes the next trade more likely to be on the opposite side.
> Without that extra moment the two transitory components cannot be separated.

> [!question]- ms-spread-roll-use-case | When would you use Roll in practice rather than quoted or effective spreads?
> When there are no quote data, for example historical, daily or OTC trade data, or as a cross-check.
> It needs only transaction prices, but it is biased by persistent flow and adverse selection.

## In this repo and SDE-Interview-Prep

- Code: [spread_models.py](code/spread_models.py) reproduces every number above (`python spread_models.py`).
- [Price discovery and microstructure noise (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/01%20-%20Market%20%26%20Microstructure%20Fundamentals/Price%20Discovery%20and%20Microstructure%20Noise.md)

## Further reading

- Richard Roll (1984), A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market, *Journal of Finance* 39(4).
- Glosten and Milgrom (1985), Bid, Ask and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders, *Journal of Financial Economics* 14(1).
- Glosten and Harris (1988), Estimating the Components of the Bid/Ask Spread, *Journal of Financial Economics* 21(1).
- Huang and Stoll (1997), The Components of the Bid-Ask Spread: A General Approach, *Review of Financial Studies* 10(4).
- Madhavan, Richardson and Roomans (1997), Why Do Security Prices Change?, *Review of Financial Studies* 10(4).
- Joel Hasbrouck, *Empirical Market Microstructure* (Oxford University Press, 2007), chapters 3 to 5.
- Maureen O'Hara, *Market Microstructure Theory* (Blackwell, 1995), chapters 2 and 3.
- Related notes: [Kyle Model and Informed Trading](04-Kyle-Model-and-Informed-Trading.md), [Adverse Selection and Flow Toxicity](05-Adverse-Selection-and-Flow-Toxicity.md).
