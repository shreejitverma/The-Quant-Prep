---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [order-book-imbalance-and-microprice]
est_hours: 3
sources: [Stoikov (2018) The micro-price: a high-frequency estimator of future prices. Quantitative Finance 18(12) 1959-1966, Cartea Jaimungal and Penalva (2015) Algorithmic and High-Frequency Trading. Cambridge University Press, Hull. Options Futures and Other Derivatives. Pearson (cost-of-carry forward pricing)]
---

# Fair Value and Theoretical Pricing

## TL;DR

- Fair value (theo) is your best estimate of where the price is going over your holding horizon; every quote is theo plus or minus an edge, and every hedge is sized from the same model.
- The mid is a poor theo when the book is lopsided; the weighted mid $P_b \frac{Q_a}{Q_b+Q_a} + P_a \frac{Q_b}{Q_b+Q_a}$ and Stoikov's micro-price correct for queue imbalance.
- Related instruments (futures, ETFs, the underlying of an option, a correlated stock) often lead; map their moves into your instrument with a beta or a pricing relationship.
- Blend independent estimates with weights proportional to inverse error variance, and let short-horizon signals decay with a half-life.
- A theo that is wrong by more than your half-spread turns every fill into adverse selection, so theo quality is the first-order driver of markouts.

## Learning objectives

- Build a theoretical value from the microprice, related instruments and lead-lag relationships.
- Blend signals into fair value with sensible weights and decay.
- Explain how fair value drives both quoting and hedging.

## Core concepts

### What theo means

A market maker's theoretical value is the conditional expectation of the future mid (or of the settlement value) at the horizon over which it expects to hold the risk, given everything it can observe now.
Quotes are then built around it: bid $= \text{theo} - e_b$ and ask $= \text{theo} + e_a$, where the edges $e_b, e_a$ come from the width and skew logic in [Quote Management](05-Quote-Management-Skew-Width-and-Size.md).
If the theo is systematically late or biased, your fills will be concentrated on the side where you are wrong, which shows up as negative markouts in [Market Making Fundamentals](01-Market-Making-Fundamentals.md).

### From mid to weighted mid to micro-price

The mid $(P_b + P_a)/2$ ignores the queues.
If the bid queue $Q_b$ is much larger than the ask queue $Q_a$, the ask is more likely to be depleted first and the next mid change is more likely to be up.
Define the imbalance $I = Q_b / (Q_b + Q_a)$.
The weighted mid is

$$
P_w = I \, P_a + (1 - I) \, P_b = m + s\left(I - \tfrac12\right),
$$

where $m$ is the mid and $s$ the spread.
It moves toward the side that is about to be consumed.
Its weakness is that it is noisy: in a one-tick market, a single order changing the queues moves $P_w$ by a sizeable fraction of a tick even though the future mid barely changes.

Stoikov (2018) defines the micro-price as the limit of the expected mid after successive future mid changes, conditional on the current imbalance and spread.
It is estimated from data by discretising imbalance and spread into states, fitting a Markov chain on how states evolve and how the mid jumps, and solving for the limit.
By construction it is a martingale, and in the paper it forecasts short-horizon prices better than the mid or weighted mid.
The practical lesson for interviews: the weighted mid is the first-order idea, the micro-price is the calibrated version, and both are small adjustments that normally stay inside the spread.
See [Order Book Imbalance and Microprice](../07-Market-Microstructure/11-Order-Book-Imbalance-and-Microprice.md).

### Related instruments and lead-lag

Most instruments have a more liquid relative whose price discovery happens first.

- Index futures versus the stocks and ETFs that track the index.
- An option's underlying versus the option: option theo is a model value given the underlying price, vol surface and rates.
- A liquid on-the-run instrument versus less liquid ones on the same curve.
- The same stock on another venue or in another time zone.

The simplest mapping is a regression beta on returns: $\Delta \ln S \approx \beta \, \Delta \ln F$, estimated on a horizon longer than the lag you are exploiting.
For instruments linked by an arbitrage relationship, use the relationship itself: an index future is priced by cost of carry, $F = S e^{(r - q)T}$ in the continuous-dividend approximation, and an ETF's indicative value is the weighted return of its basket.
See [ETFs and Index Arbitrage](../06-Fixed-Income-and-Asset-Classes/08-ETFs-and-Index-Arbitrage.md) and [ETF and Futures Market Making](08-ETF-and-Futures-Market-Making.md).

### Blending estimates

Suppose you have several unbiased estimates $\hat v_k$ of fair value with independent errors of standard deviation $\sigma_k$.
The minimum-variance combination weights each by inverse variance:

$$
\hat v = \frac{\sum_k \hat v_k / \sigma_k^2}{\sum_k 1/\sigma_k^2}, \qquad \operatorname{Var}(\hat v) = \frac{1}{\sum_k 1/\sigma_k^2}.
$$

With correlated errors the weights become $w \propto \Sigma^{-1}\mathbf{1}$, the same algebra as the minimum-variance portfolio.
In practice most desks write theo as the mid plus a sum of signal forecasts, $\text{theo} = m + \sum_k \beta_k x_k$, with $\beta_k$ fitted by regressing the future mid change at the chosen horizon on the signals, out of sample and with shrinkage.
The regression automatically handles correlation between signals, which naive addition double counts.

### Decay and horizon

A short-horizon signal is a forecast of a move that happens soon or not at all.
If the forecast was $\alpha_0$ when observed and its half-life is $h$, its current contribution is $\alpha_0 \, 2^{-\Delta t / h}$.
Match the signal horizon to the holding horizon: a signal that predicts a move over 10 minutes should hardly move a quote you expect to be filled on within 200 ms, and vice versa.

### Theo drives hedging too

The model that sets theo also defines what risk you hold.
If your theo for a stock is its own micro-price plus $\beta$ times the futures-implied move, then a long stock position carries $\beta$ units of futures exposure per unit notional, and the natural hedge is a futures short of that size.
For options the same idea is delta: $\partial \text{theo} / \partial S$.
A theo that ignores a relationship produces a hedge that ignores it, so errors in theo show up twice: in markouts and in unhedged residual risk.
See [Hedging and Risk for Market Makers](06-Hedging-and-Risk-for-Market-Makers.md).

## Worked examples

### Example 1: weighted mid

The book is 50.00 bid for 800 shares, 50.01 offered for 200 shares.
The imbalance is $I = 800/1000 = 0.8$.
The weighted mid is $0.8 \times 50.01 + 0.2 \times 50.00 = 50.008$, against a mid of 50.005.
So the ask at 50.01 is only 0.2 cents above theo and the bid is 0.8 cents below it.
A market maker joining both sides of this book has more edge on the bid and should be reluctant to add size on the ask.

### Example 2: futures lead

A 200 dollar stock has a beta of 1.2 to the index future.
The future ticks up 10 points from 5000, a return of $10/5000 = 0.2\%$, while the stock's book has not moved yet.
The futures-implied move in the stock is $200 \times 1.2 \times 0.002 = 0.48$ dollars.
Any offer on the stock more than a few cents below the new implied price is stale; a market maker must cancel or raise its ask before someone buys it.
This is the classic pick-off risk that motivates co-location and fast cancel paths; see [Latency Arbitrage and Speed](../07-Market-Microstructure/10-Latency-Arbitrage-and-Speed.md).

### Example 3: blending two estimates and quoting off the result

The stock's book is 99.99 / 100.01.
Estimate A, from the stock's own micro-price, is 100.004 with error standard deviation 0.02.
Estimate B, from the futures-implied move, is 100.012 with error standard deviation 0.01.
Inverse-variance weights are $w_A = (1/0.02^2)/(1/0.02^2 + 1/0.01^2) = 2500/12500 = 0.2$ and $w_B = 0.8$.
Theo is $0.2 \times 100.004 + 0.8 \times 100.012 = 100.0104$, with error standard deviation $\sqrt{1/12500} \approx 0.0089$.
The resting ask at 100.01 now sits 0.0004 below theo: negative edge, so pull it or move it up.
The bid at 99.99 has 0.0204 of edge, and you can happily keep it or add size.

### Example 4: cost-of-carry theo for an index future

Spot index 5000, rate 5%, dividend yield 1.5%, three months to expiry.
$F = 5000 \, e^{(0.05 - 0.015)(0.25)} = 5000 \, e^{0.00875} \approx 5043.94$.
A market maker in the future quotes around this value plus a basis adjustment it estimates from actual trading, since funding costs and dividend expectations differ across participants.

### Example 5: ETF indicative value

An ETF last valued at 80.00 holds three stocks with weights 50%, 30% and 20%.
Since that valuation the stocks moved $+0.30\%$, $-0.20\%$ and $+0.50\%$.
The basket return is $0.5(0.003) + 0.3(-0.002) + 0.2(0.005) = 0.0019$, so the indicative value is $80 \times 1.0019 = 80.152$.
The ETF market maker quotes around this, adjusted for creation and redemption costs and for the stocks whose quotes are themselves stale.

### Example 6: decaying a signal

A signal forecast a 2-tick up-move with a half-life of 500 ms.
After 200 ms without the move, its remaining contribution is $2 \times 2^{-200/500} \approx 1.52$ ticks.
If the move happened (the mid rose by 2 ticks), the signal has been consumed and should contribute nothing; do not add a stale forecast on top of a price that already reflects it.

```python
import numpy as np

def theo(mid, signals, betas, ages_ms, half_lives_ms):
    """Mid plus decayed, regression-weighted signal forecasts (price units)."""
    decay = np.power(2.0, -np.asarray(ages_ms) / np.asarray(half_lives_ms))
    return mid + float(np.dot(betas, np.asarray(signals) * decay))
```

## Pitfalls

- Quoting around the mid in a lopsided one-tick book; the side with the thin queue is the one that gets picked off.
- Treating the weighted mid as exact; it overreacts to single orders and is not a martingale.
- Adding correlated signals as if they were independent; fit them jointly or you double count the same information.
- Using a related instrument's last trade instead of its current fair value, or ignoring its own latency and tick size.
- Estimating a lead-lag beta on the same horizon as the lag; the beta will be biased toward zero by asynchronous prices.
- Forgetting to remove a signal after the move it predicted has happened.
- Using one theo for quoting and a different, inconsistent model for hedging.

## Interview questions

> [!question]- mm-fv-weighted-mid-formula | Write the weighted mid in terms of best prices and queue sizes.
> $P_w = P_a \frac{Q_b}{Q_b + Q_a} + P_b \frac{Q_a}{Q_b + Q_a} = m + s(I - 1/2)$ with $I = Q_b/(Q_b + Q_a)$.
> A large bid queue pulls the estimate toward the ask, because the ask is more likely to be consumed first.

> [!question]- mm-fv-weighted-mid-example | Book is 50.00 x 800 bid, 50.01 x 200 offered. What is the weighted mid?
> 50.008.
> $I = 0.8$, so $0.8 \times 50.01 + 0.2 \times 50.00 = 50.008$, versus a mid of 50.005.

> [!question]- mm-fv-microprice-vs-weighted-mid | How does Stoikov's micro-price improve on the weighted mid?
> It is the limit of the expected future mid conditional on imbalance and spread, estimated from a Markov chain on the order-book state, so it is a martingale and does not overreact.
> The weighted mid is a noisy first-order version that can move a large fraction of a tick on a single order.

> [!question]- mm-fv-inverse-variance-blend | Two unbiased theo estimates have error sd 0.02 and 0.01. What weights, and what is the combined sd?
> Weights 0.2 and 0.8; combined sd about 0.0089.
> Weights are proportional to $1/\sigma^2$: 2500 and 10000; combined variance is $1/12500$.

> [!question]- mm-fv-futures-implied-move | A 200 dollar stock with beta 1.2 to the future; the future rises 0.2%. Implied stock move?
> About 0.48 dollars.
> $200 \times 1.2 \times 0.002 = 0.48$; any offer well below that is stale and will be picked off.

> [!question]- mm-fv-carry-futures-price | Spot 5000, r = 5%, dividend yield 1.5%, T = 0.25. Fair futures price?
> About 5043.94.
> $F = S e^{(r-q)T} = 5000 e^{0.00875}$.

> [!question]- mm-fv-signal-half-life | A 2-tick forecast has a 500 ms half-life. What is it worth after 200 ms if the move has not happened?
> About 1.52 ticks.
> $2 \times 2^{-0.4} \approx 1.516$.

> [!question]- mm-fv-theo-drives-hedge | How does your fair-value model determine your hedge?
> The hedge ratio is the sensitivity of theo to the hedge instrument, for example $\beta$ for a stock priced off a future or delta for an option.
> If theo ignores a relationship, the hedge ignores it too, and the error appears both in markouts and in residual risk.

> [!question]- mm-fv-correlated-signals | Why not just add up the forecasts from several signals?
> Because correlated signals carry overlapping information, so adding them double counts it.
> Fit them jointly (a regression of the future mid change on all signals, with shrinkage) so each coefficient measures its incremental value.

> [!question]- mm-fv-stale-quote-edge | Theo is 100.0104 and your ask rests at 100.01. What do you do?
> Cancel or raise the ask: it has negative edge of about 0.0004.
> A quote below theo is a free option for anyone with the same information; only quote where theo plus required edge sits inside your price.

> [!question]- mm-fv-etf-indicative-value | An ETF at 80.00 holds 50/30/20 in three stocks that move +0.3%, -0.2%, +0.5%. New indicative value?
> 80.152.
> Basket return is $0.0015 - 0.0006 + 0.0010 = 0.0019$ and $80 \times 1.0019 = 80.152$.

## In this repo and SDE-Interview-Prep

- Microstructure background: [Order Book Imbalance and Microprice](../07-Market-Microstructure/11-Order-Book-Imbalance-and-Microprice.md).
- Signal section of the systems companion: [Quantitative Models and Strategies](Quant-Dev-MM-Guide/03_Quantitative_Models_and_Strategies.md).

## Further reading

- Sasha Stoikov (2018), The micro-price: a high-frequency estimator of future prices, *Quantitative Finance* 18(12).
- Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015).
- John Hull, *Options, Futures, and Other Derivatives*, chapter on forward and futures prices.
