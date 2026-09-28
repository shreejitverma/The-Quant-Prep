---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [limit-order-books-and-order-types, linear-regression-ols]
est_hours: 4
sources: [Stoikov (2018) The micro-price: a high-frequency estimator of future prices. Quantitative Finance 18(12) 1959-1966, Cont Kukanov and Stoikov (2014) The Price Impact of Order Book Events. Journal of Financial Econometrics 12(1) 47-88, Cartea Jaimungal and Penalva (2015) Algorithmic and High-Frequency Trading. Cambridge University Press]
---

# Order Book Imbalance and the Microprice

## TL;DR

- Queue imbalance $I = Q^b/(Q^b + Q^a)$ at the touch is the simplest and one of the strongest short-horizon predictors: a small ask queue tends to be depleted first, so the next mid move tends to be up.
- The weighted mid $I P^a + (1 - I) P^b$ uses that fact but is noisy and not a martingale, so it is a poor fair value.
- Stoikov's microprice is the limit of expected future mids given the current imbalance and spread, $P^{\text{micro}} = M + g(I, S)$, estimated as a Markov chain; by construction it is a martingale-style estimator of where the mid is heading.
- Order flow imbalance (OFI), the net change in queue sizes at the touch, explains contemporaneous price changes almost linearly, with a slope that falls as depth rises.
- Judge these signals by the markouts of the fills they would have changed, not by raw correlation with returns.

## Learning objectives

- Build order book imbalance and order flow imbalance signals.
- Derive the microprice and explain why it beats the mid.
- Evaluate short-horizon signals with markouts rather than returns.

## Core concepts

### Queue imbalance

With best bid $P^b$ of size $Q^b$ and best ask $P^a$ of size $Q^a$, define

$$
I = \frac{Q^b}{Q^b + Q^a} \in [0, 1].
$$

In a large-tick instrument the next mid change usually happens when one of the two touch queues empties.
The smaller queue empties first more often, so $I$ close to 1 predicts an up move and close to 0 a down move.
Variants add deeper levels with decaying weights, use only displayed size, or normalise by typical depth.

The weighted mid

$$
P^{w} = I P^a + (1 - I) P^b = M + \left(I - \tfrac{1}{2}\right) S
$$

(with $M$ the mid and $S$ the spread) puts fair value closer to the side that is about to be taken out.
Its problems: it jumps whenever a single order is added or cancelled, it depends mechanically on the spread, and it is not a martingale, so its own future changes are predictable.
A fair value whose changes are predictable leaves edge on the table and pays it to faster traders.

### The microprice

Stoikov defines the microprice as the limit of expected mids at future mid-change times $\tau_1 < \tau_2 < \dots$:

$$
P^{\text{micro}}_t = \lim_{n \to \infty} \mathbb{E}\big[ M_{\tau_n} \mid I_t, S_t \big] = M_t + \sum_{k=1}^{\infty} g_k(I_t, S_t).
$$

Discretise imbalance into buckets and spreads into a few ticks; the state is $x = (I, S)$.
From event data estimate:

- $Q$: transition probabilities between states with no mid change;
- $T$: transition probabilities into a new state at the moment the mid changes;
- $R$: the corresponding mid changes (for example $\pm$ half a tick when a queue empties and the spread opens).

The first correction is the expected size of the next mid move,

$$
g_1 = (\mathbf{1} - Q)^{-1} R_1, \qquad R_1(x) = \mathbb{E}[\Delta M \,\mathbb{1}\{\text{mid changes on the next event}\} \mid x],
$$

and later corrections follow from $g_{k+1} = B g_k$ with $B = (\mathbf{1} - Q)^{-1} T$.
Stoikov symmetrises the data (swapping bid and ask flips the sign of the adjustment) and shows conditions under which the series converges.
The result depends only on the current state, is cheap to evaluate from a lookup table, and is, by construction, the best estimate of the mid after its next few moves.

Why it beats the mid: the mid ignores the queues entirely, so in a one-tick market it is stale by up to half a tick whenever the book is lopsided.
Why it beats the weighted mid: it is estimated from how the book actually evolves rather than assumed linear in $I$, and it is designed so that its future changes are unpredictable from the same state.

### Order flow imbalance

Cont, Kukanov and Stoikov measure the net pressure at the touch between book snapshots $n-1$ and $n$:

$$
e_n = \mathbb{1}\{P^b_n \ge P^b_{n-1}\} q^b_n - \mathbb{1}\{P^b_n \le P^b_{n-1}\} q^b_{n-1} - \mathbb{1}\{P^a_n \le P^a_{n-1}\} q^a_n + \mathbb{1}\{P^a_n \ge P^a_{n-1}\} q^a_{n-1}.
$$

Bid additions and ask depletions count positive; bid depletions and ask additions count negative, and a price-level change counts the whole new or old queue.
Summing over an interval gives $\text{OFI}_k = \sum_{n \in k} e_n$, and they find the linear model

$$
\Delta P_k = \beta_k \, \text{OFI}_k + \varepsilon_k
$$

fits well, with $\beta$ roughly inversely proportional to average depth; their stylised model gives $\Delta P \approx \delta \cdot \text{OFI} / (2D)$ for tick $\delta$ and depth $D$ per level.
This is a contemporaneous relation: it explains the price change over the same interval.
Using it to trade requires lagged OFI, which predicts far less.

### Evaluating short-horizon signals

Returns computed from trade prices are contaminated by bid-ask bounce, and mid returns at a sub-second horizon are mostly zero with occasional half-tick jumps.
A market maker cares about something narrower: does the signal improve the fills it actually gets?

- Bucket your passive fills by the signal value at the time of the quote, from the side of the fill (for a bid fill, imbalance on the bid side).
- Compute markouts per bucket at several horizons; see [Adverse Selection and Flow Toxicity](05-Adverse-Selection-and-Flow-Toxicity.md).
- Simulate the rule (pull, skew, resize) and count both the losses avoided and the good fills given up, including queue position lost by cancelling.

For the signal in isolation, regress future microprice or mid changes on the signal with overlapping-horizon-aware standard errors, and check stability across days, volatility regimes and tick-to-price ratios.
The out-of-sample test is the markout improvement, not $R^2$.

## Worked examples

### Example 1: imbalance and weighted mid

Bid 100.00 x 800, ask 100.01 x 200.
$I = 800 / 1000 = 0.8$.
$P^w = 0.8 \times 100.01 + 0.2 \times 100.00 = 100.008$, which is $+0.3$ ticks above the mid of 100.005.
If one 600-lot bid cancels, $I$ becomes $200/400 = 0.5$ and the weighted mid falls back to 100.005 without any trade, which shows how jumpy it is.

### Example 2: a toy microprice

One-tick spread, five imbalance buckets $I \in \{0.1, 0.3, 0.5, 0.7, 0.9\}$.
On each book event from bucket $i$ the mid rises half a tick with probability $u_i$ and falls half a tick with probability $d_i$:

| $I$ | 0.1 | 0.3 | 0.5 | 0.7 | 0.9 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| $u_i$ | 0.02 | 0.05 | 0.10 | 0.18 | 0.30 |
| $d_i$ | 0.30 | 0.18 | 0.10 | 0.05 | 0.02 |

Otherwise the mid stays, and imbalance stays in its bucket with half the remaining probability or moves to each neighbouring bucket with a quarter (reflecting at the ends).
After a mid change assume imbalance restarts from a distribution symmetric around 0.5; then $g_1$ is antisymmetric, $T g_1 = 0$, and all later terms vanish, so $P^{\text{micro}} = M + g_1$.
Solving $g_1 = (\mathbf{1} - Q)^{-1} (u - d) \cdot 0.5$:

| $I$ | 0.1 | 0.3 | 0.5 | 0.7 | 0.9 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Microprice minus mid (ticks) | -0.362 | -0.219 | 0 | +0.219 | +0.362 |
| Weighted mid minus mid (ticks) | -0.4 | -0.2 | 0 | +0.2 | +0.4 |

The microprice is steeper than the weighted mid near balance and flatter at the extremes, where it is capped by the half-tick size of the next move and by the chance that imbalance mean-reverts first.
With real data the table has spread states and many more buckets, but the calculation is the same linear solve.

```python
import numpy as np

u = np.array([0.02, 0.05, 0.10, 0.18, 0.30]); d = u[::-1]
Q = np.zeros((5, 5))
for i in range(5):
    rest = 1 - u[i] - d[i]
    Q[i, i] += 0.5 * rest
    for j in (i - 1, i + 1):
        Q[i, j if 0 <= j < 5 else i] += 0.25 * rest
g1 = np.linalg.solve(np.eye(5) - Q, 0.5 * (u - d))
print(g1.round(3))  # [-0.362 -0.219  0.     0.219  0.362]
```

### Example 3: computing OFI

Snapshots (bid price x size, ask price x size):

| $n$ | Bid | Ask | $e_n$ | Reason |
| ---: | :--- | :--- | ---: | :--- |
| 0 | 100.00 x 500 | 100.01 x 400 | | |
| 1 | 100.00 x 700 | 100.01 x 400 | +200 | Bid queue grew by 200 |
| 2 | 100.00 x 700 | 100.01 x 100 | +300 | Ask queue shrank by 300 |
| 3 | 100.00 x 700 | 100.02 x 600 | +100 | Ask level cleared: the old 100 counts |
| 4 | 100.01 x 200 | 100.02 x 600 | +200 | New better bid: its 200 counts |

$\text{OFI} = 800$.
With average depth $D = 1{,}000$ per level, the stylised relation gives $\Delta P \approx 800 / 2000 = 0.4$ ticks over the interval.
The actual mid went from 100.005 to 100.015, a full tick; the stylised coefficient is an average, and a single interval is noisy.

### Example 4: judging an imbalance rule by markouts

You bucket 10,000 bid fills by bid-side imbalance at quote time, with 5-second markouts in ticks including the half-spread captured:

| Bucket | Fills | Markout per fill | Total |
| :--- | ---: | ---: | ---: |
| $I < 0.3$ | 2,000 | -0.6 | -1,200 |
| $0.3 \le I \le 0.7$ | 5,000 | +0.1 | +500 |
| $I > 0.7$ | 3,000 | +0.4 | +1,200 |

Total edge is $+500$ ticks.
Pulling the bid when $I < 0.3$ removes the $-1{,}200$ bucket and would raise the total to $+1{,}700$ ticks, if the other buckets' fills are unaffected.
Before shipping, check what cancelling costs in queue position when imbalance recovers, and whether the bucket's markout is stable across days; with a per-fill standard deviation of a few ticks, 2,000 fills give a standard error of about 0.05 to 0.1 ticks, so the $-0.6$ is clearly real.

## Pitfalls

- Using the weighted mid as fair value without checking whether its changes are predictable.
- Forgetting that imbalance means different things in large-tick and small-tick instruments; in small-tick names queues are short and noisy.
- Treating the OFI regression as a forecast; it is contemporaneous.
- Evaluating a sub-second signal on trade-price returns, which bounce between bid and ask.
- Ignoring hidden and iceberg liquidity, which makes displayed imbalance misleading.
- Overfitting bucket edges and horizon grids on one period, then reporting in-sample markout improvement.
- Measuring the gain from pulling quotes without counting the lost queue position and good fills.
- Letting others spoof the imbalance: displayed size can be placed to be cancelled, so robust signals weight orders by how long they have rested.

## Interview questions

> [!question]- ms-obi-imbalance-definition | Define queue imbalance and say which way it predicts.
> $I = Q^b/(Q^b + Q^a)$ at the touch; high $I$ predicts an up move.
> The smaller queue is more likely to be depleted first, and in a one-tick market that is what moves the mid.

> [!question]- ms-obi-weighted-mid-numeric | Bid 100.00 x 800, ask 100.01 x 200. What is the weighted mid?
> 100.008.
> $I = 0.8$, so $0.8 \times 100.01 + 0.2 \times 100.00$; the bid size weights the ask price.

> [!question]- ms-obi-weighted-mid-flaws | Why is the weighted mid a poor fair value?
> It jumps on single adds and cancels, depends mechanically on the spread, and is not a martingale, so its future changes are predictable.
> Predictable fair-value changes are edge given away to faster traders.

> [!question]- ms-obi-microprice-definition | How does Stoikov define the microprice?
> As the limit of expected mid prices at future mid-change times given current imbalance and spread: $\lim_n \mathbb{E}[M_{\tau_n} \mid I, S] = M + \sum_k g_k(I, S)$.
> It is estimated from a Markov chain on discretised (imbalance, spread) states.

> [!question]- ms-obi-microprice-g1 | How do you compute the first microprice correction $g_1$?
> $g_1 = (\mathbf{1} - Q)^{-1} R_1$, where $Q$ is the no-mid-change transition matrix and $R_1$ the expected mid change on the next event.
> It is the expected size of the next mid move, found by the standard absorbing-chain solve; later terms follow from $g_{k+1} = B g_k$.

> [!question]- ms-obi-microprice-vs-mid | Why does the microprice beat the mid in a large-tick stock?
> The mid ignores queue sizes, so with a lopsided book it is predictably wrong by a sizeable fraction of the half tick.
> The microprice conditions on imbalance and spread, so its errors are much less predictable.

> [!question]- ms-obi-ofi-definition | What does order flow imbalance measure?
> The net change in touch queues: bid additions and ask depletions positive, bid depletions and ask additions negative, with whole queues counted when a price level changes.
> Summed over an interval it explains that interval's price change almost linearly.

> [!question]- ms-obi-ofi-depth | How does the OFI price-impact slope depend on depth?
> It falls roughly in inverse proportion to depth; the stylised model gives $\Delta P \approx \delta\,\text{OFI}/(2D)$.
> Deeper books need more net flow to move the price.

> [!question]- ms-obi-ofi-contemporaneous | A colleague reports $R^2$ of 60% for price change on OFI. Can you trade it?
> Not directly: the relation is contemporaneous, so it explains the move while it happens.
> Only lagged OFI can be traded, and its predictive power is much smaller.

> [!question]- ms-obi-evaluate-with-markouts | Why evaluate an imbalance signal with markouts rather than returns?
> A market maker's P&L comes from its fills, so the question is whether the signal improves the markouts of fills it would change, net of lost queue position.
> Sub-second returns are dominated by zeros, half-tick jumps and bid-ask bounce.

> [!question]- ms-obi-pull-rule-gain | Bid fills with $I < 0.3$ mark out at -0.6 ticks over 2,000 fills; total edge is +500. What does pulling in that state gain?
> Up to 1,200 ticks, taking the total to +1,700.
> Subtract the cost of lost queue position and any good fills given up before adopting it.

> [!question]- ms-obi-spoofing-robustness | How do you make an imbalance signal harder to spoof?
> Weight displayed size by how long it has rested, ignore size that appears and cancels quickly, and combine with trade-based flow.
> Spoofed size is placed to be cancelled, so age and fill behaviour reveal it.

## Further reading

- Sasha Stoikov (2018), The micro-price: a high-frequency estimator of future prices, *Quantitative Finance* 18(12).
- Cont, Kukanov and Stoikov (2014), The Price Impact of Order Book Events, *Journal of Financial Econometrics* 12(1).
- Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015).
- Related notes: [Fair Value and Theoretical Pricing](../08-Market-Making/02-Fair-Value-and-Theoretical-Pricing.md), [Limit Order Books and Order Types](01-Limit-Order-Books-and-Order-Types.md).
