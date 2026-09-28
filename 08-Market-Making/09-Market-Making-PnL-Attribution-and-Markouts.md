---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [market-making-fundamentals, adverse-selection-and-flow-toxicity]
est_hours: 3
sources: [Cartea Jaimungal and Penalva (2015) Algorithmic and High-Frequency Trading. Cambridge University Press, Harris (2003) Trading and Exchanges: Market Microstructure for Practitioners. Oxford University Press, Sinclair (2013) Volatility Trading 2nd edition. Wiley, pandas documentation for merge_asof https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html]
---

# Market Making P&L Attribution and Markouts

## TL;DR

- Split every fill's P&L at two points in time, the fill and the markout horizon $\tau$: edge at fill against theo, adverse selection from fill to $\tau$, and inventory drift from $\tau$ to the close; hedges and fees are separate lines, and the parts must sum exactly to the official P&L.
- Measure against theo (your fair value), not only the mid, so that edge at fill tests the quoting and adverse selection tests what the model missed.
- Build markout curves per segment (venue, counterparty where known, order type, queue position, signal state) at a grid of horizons including negative ones, size-weighted, with standard errors that respect clustering.
- Inventory drift is not alpha: over a day it is mostly noise with a sign set by the market's direction, and it should be judged against the risk taken, not added to edge.
- For options, the same idea becomes edge in vol points times vega at fill, then vega, gamma, theta and hedge P&L after.

## Learning objectives

- Attribute P&L to edge at fill, markout, hedging cost and inventory drift.
- Build markout curves by counterparty, venue and signal state.

## Core concepts

### The attribution identity

Use the notation of [Market Making Fundamentals](01-Market-Making-Fundamentals.md): fill $i$ at time $t_i$, side $d_i$ ($+1$ buy), size $n_i$, price $p_i$, and a reference price $\theta_t$, now your theo rather than the mid.
With the book marked at $\theta_T$ at the end,

$$
\text{P\&L} = \sum_i n_i d_i (\theta_T - p_i) + \text{fees}
= \underbrace{\sum_i n_i d_i (\theta_{t_i} - p_i)}_{\text{edge at fill}}
+ \underbrace{\sum_i n_i d_i (\theta_{t_i+\tau} - \theta_{t_i})}_{\text{adverse selection}}
+ \underbrace{\sum_i n_i d_i (\theta_T - \theta_{t_i+\tau})}_{\text{inventory drift}}
+ \text{fees}.
$$

The identity telescopes, so it holds exactly for any $\tau$; the choice of $\tau$ only moves P&L between the adverse-selection and drift buckets.
Choose $\tau$ close to the typical time it takes to offload or hedge a fill, so that "adverse selection" means the move you could not avoid and "drift" means the risk you chose to hold.

Split fills into two kinds:

- Passive fills: their edge at fill is positive by construction; the question is how much of it survives to $\tau$.
- Hedge and liquidation trades: usually aggressive, with negative edge at fill (you crossed the spread); report their total as hedging cost.

Report fees and rebates per venue and liquidity flag, and use marginal rather than average rates when volume tiers apply: the fee on the next share is what a quoting decision should use.

An attribution system is only trusted if it reconciles: the sum of buckets must equal the official P&L every day, and any unexplained residual (missed fills, corporate actions, stale theo, fees booked late) is investigated, not absorbed.

### Theo versus mid as the reference

- Mid-based markouts are model-free and comparable across desks, but they call your own signal-driven edge "adverse selection" when the mid moves toward your theo.
- Theo-based markouts isolate what your model got wrong: edge at fill is what you intended to earn, and the move from $t_i$ to $t_i + \tau$ is what theo failed to anticipate.

Compute both.
A large gap between them tells you how much of your P&L comes from the signal inside theo.

### Building markout curves

For each fill record: exchange and local timestamps, venue, order type and liquidity flag, queue position or time resting, size, side, theo and signal state at quote time, and counterparty or client where the venue discloses it.
Then:

1. Join each fill to the reference series at $t_i + \tau$ for a grid such as $-10$ s, $-1$ s, 0, 100 ms, 1 s, 10 s, 60 s and 5 min, using an as-of join that takes the last value at or before $t_i + \tau$, never after.
2. Compute $d_i(\theta_{t_i+\tau} - p_i)$ per fill, size-weight within each segment, and express it in ticks or basis points so instruments can be pooled.
3. Plot the curve per segment with confidence bands.

Negative horizons are diagnostic: if the reference had already moved toward your price before the fill ($d_i(\theta_{t_i} - \theta_{t_i - \tau}) < 0$), you were filled because your quote became stale, which points to latency or update logic rather than toxic counterparties.

Standard errors: fills cluster in bursts that share one future price path, so treat each burst (or each time bucket) as one observation, or bootstrap by day.
Event-time horizons (the next $k$ trades or mid changes) are a useful complement in instruments whose activity varies a lot through the day.

### Segments that usually matter

- Venue and fee model: a venue whose rebate is high may carry worse markouts; compare net of fees.
- Counterparty or client, where disclosed: the basis for tiered pricing in RFQ and streaming markets.
- Order type of the aggressor: sweeps and IOCs versus single-venue marketable orders.
- Queue position at fill: back-of-queue fills are typically worse; see [Limit Order Books and Order Types](../07-Market-Microstructure/01-Limit-Order-Books-and-Order-Types.md).
- Signal state: imbalance, microprice minus mid, time since last theo change; see [Order Book Imbalance and the Microprice](../07-Market-Microstructure/11-Order-Book-Imbalance-and-Microprice.md).

Each segment's curve feeds a pricing decision: width, skew, size, or not quoting that segment at all; see [Quote Management: Skew, Width and Size](05-Quote-Management-Skew-Width-and-Size.md).

### Options

For an options book, express edge at fill in vol points: $\text{edge} = n \cdot m \cdot \text{vega} \cdot (\sigma_{\text{trade}} - \sigma_{\text{theo}}) \cdot d'$, with $m$ the contract multiplier and $d'$ the sign that makes selling above theo positive.
After the fill, the delta-hedged position's P&L is explained by the Greeks:

$$
\text{P\&L} \approx \text{edge} + \sum \text{vega}\,\Delta\sigma + \Theta\,\Delta t + \tfrac{1}{2}\Gamma \sum_k (\Delta S_k)^2 + \text{hedge cost} + \text{residual}.
$$

Markouts for options are usually taken on the theo vol at the strike (did the surface move against the fill?) as well as on price.
See [Options Market Making](07-Options-Market-Making.md) and [P&L Attribution and Greek Risk](../11-Risk-and-Trading/06-PnL-Attribution-and-Greek-Risk.md).

## Worked examples

### Example 1: attributing a short session

Theo path: 100.00 at $t = 0$, 99.99 at 1 s, 99.97 at 5 s, 99.975 at 6 s, 99.96 from 10 s to the close. Markout horizon $\tau = 1$ s.

| Trade | Type | Edge at fill | Adverse selection | Inventory drift | Fee |
| :--- | :--- | ---: | ---: | ---: | ---: |
| Buy 100 at 99.98, $t = 0$ | passive | $100 \times 0.02 = +2.00$ | $100 \times (-0.01) = -1.00$ | $100 \times (-0.03) = -3.00$ | +0.20 |
| Sell 50 at 99.99, $t = 5$ | passive | $50 \times 0.02 = +1.00$ | $-50 \times 0.005 = -0.25$ | $-50 \times (-0.015) = +0.75$ | +0.10 |
| Sell 50 at 99.95, $t = 10$ | hedge, aggressive | $-50 \times 0.01 = -0.50$ | 0 | 0 | -0.15 |

Rebate 0.002 per share on passive fills, taker fee 0.003 on the hedge.
Totals: passive edge +3.00, adverse selection -1.25, inventory drift -2.25, hedge cost -0.50, fees +0.15, sum -0.85.
Cash check: $-100 \times 99.98 + 50 \times 99.99 + 50 \times 99.95 = -1.00$, plus fees 0.15, equals -0.85 with a flat position.
Reading it: quoting earned 3.00 and lost 1.25 to selection, so the quotes themselves made +1.75; the loss came from holding a long position for 10 seconds while theo fell, and then paying to hedge.
The action item is hedging speed or skew, not width.

### Example 2: venue curves net of fees

Markouts in ticks per fill, before fees:

| Venue | Fills | 100 ms | 1 s | 10 s | 60 s | Fee (+ rebate) | Net at 10 s |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 40,000 | +0.5 | +0.2 | -0.1 | -0.2 | +0.25 | +0.15 |
| B | 10,000 | +0.5 | 0.0 | -0.4 | -0.6 | -0.10 | -0.50 |

Venue A earns $40{,}000 \times 0.15 = 6{,}000$ ticks; venue B loses $10{,}000 \times 0.5 = 5{,}000$ ticks.
Both earn the same half-tick at fill; the difference is what happens in the next ten seconds.
Before cutting B, check whether B fills are concentrated in one signal state or queue position that could be avoided instead.

### Example 3: is the venue difference real?

Per-fill 10-second markout standard deviation is 4 ticks.
Fills come in bursts: about 4,000 independent clusters on A and 1,000 on B.
Standard errors: $4/\sqrt{4000} \approx 0.063$ and $4/\sqrt{1000} \approx 0.126$; the difference's standard error is $\sqrt{0.063^2 + 0.126^2} \approx 0.141$.
The 0.65-tick difference is about 4.6 standard errors: real.
Had you treated all 10,000 B fills as independent, the standard error would have looked about three times smaller than it is, and small differences would have looked significant.

### Example 4: an options day

You sell 100 calls (multiplier 100) at 25.5 vol against a 25.0 theo, vega 0.19 per point, gamma 0.0302, theta -0.026 per day per option; delta is hedged at four checkpoints, each with a 0.60 move in the stock.

| Component | Calculation | Dollars |
| :--- | :--- | ---: |
| Edge at fill | $100 \times 100 \times 0.19 \times 0.5$ | +950 |
| Vega (vol at strike +0.8) | $-100 \times 100 \times 0.19 \times 0.8$ | -1,520 |
| Theta (one day) | $100 \times 100 \times 0.026$ | +260 |
| Gamma | $-\tfrac{1}{2} \times 302 \times 4 \times 0.60^2$ | -217 |
| Total explained | | -527 |

The trade had half a vol point of edge and still lost, because the surface moved 0.8 points against a short-vega position.
The vol markout of this fill (theo vol at the strike 0.8 higher by the close) says the buyer was informed about vol, or the surface was stale: segment by client and by time since the last surface refit before deciding.

### Example 5: a stale-quote diagnosis from negative horizons

For a segment of fills, the theo markout $d_i(\theta_{t_i+\tau} - p_i)$ is $+0.5$ ticks at $\tau = -1$ s, $+0.1$ at 0 and $-0.3$ at $+1$ s.
The curve is already falling before the fill: theo moved 0.4 ticks toward your price in the preceding second, so your quote sat almost on theo when it traded.
The intended half-tick of edge was lost because the quote was late to update, not because the counterparty knew something you could not have known.
The fix is in update latency or thresholds, not in wider quotes for everyone.

```python
import pandas as pd

def markout_curve(fills, mids, horizons, by):
    """fills: ts, side (+1 buy), size, price, segment columns; mids: ts, mid sorted by ts."""
    out = []
    for h in horizons:
        look = fills.assign(ts_h=fills["ts"] + h).sort_values("ts_h")
        # last reference value at or before t + h, never after
        j = pd.merge_asof(look, mids, left_on="ts_h", right_on="ts",
                          suffixes=("", "_mid"), direction="backward")
        j["pnl"] = j["side"] * (j["mid"] - j["price"]) * j["size"]
        g = j.groupby(by)[["pnl", "size"]].sum()
        out.append((g["pnl"] / g["size"]).rename(h))
    return pd.concat(out, axis=1)
```

## Pitfalls

- Attribution buckets that do not sum to the official P&L, so nobody trusts them.
- Reporting only mid-based markouts, so signal-driven edge shows up as adverse selection.
- Picking $\tau$ far longer than the holding time, which buries adverse selection inside inventory noise, or far shorter, which calls temporary impact toxic.
- Lumping hedge trades with passive fills, hiding the cost of hedging.
- Using average fee rates when tiered schedules make the marginal rate different.
- As-of joins that take the first reference value after $t + \tau$ instead of the last one at or before it, or clocks that are not synchronised across venues.
- Treating clustered fills as independent and over-reading small differences between segments.
- Rewarding a trader for positive inventory drift in a trending market; it is risk, not skill, unless it persists after controlling for direction.

## Interview questions

> [!question]- mm-pnl-attribution-identity | Write the P&L attribution for a market maker with theo $\theta$ and markout horizon $\tau$.
> $\sum_i n_i d_i(\theta_{t_i} - p_i) + \sum_i n_i d_i(\theta_{t_i+\tau} - \theta_{t_i}) + \sum_i n_i d_i(\theta_T - \theta_{t_i+\tau}) + \text{fees}$: edge at fill, adverse selection, inventory drift.
> It telescopes to $\sum_i n_i d_i(\theta_T - p_i)$ plus fees, so it holds exactly for any $\tau$.

> [!question]- mm-pnl-tau-choice | How do you choose the markout horizon for attribution?
> Close to the typical time to offload or hedge a fill.
> Then adverse selection is the move you could not avoid and drift is the risk you chose to hold; $\tau$ only moves P&L between those two buckets.

> [!question]- mm-pnl-theo-vs-mid | Why compute markouts against theo as well as the mid?
> Against the mid, profitable signal-driven edge looks like adverse selection when the mid later moves to your theo.
> Theo-based markouts isolate what your model missed; the gap between the two measures your signal's contribution.

> [!question]- mm-pnl-numeric-session | You buy 100 at 99.98 with theo 100.00, theo is 99.99 one second later and 99.96 at the close, and you hedge nothing. Split the P&L.
> Edge +2.00, adverse selection -1.00, inventory drift -3.00, total -2.00 before fees.
> $100 \times 0.02$, $100 \times (-0.01)$, $100 \times (-0.03)$; the total equals $100 \times (99.96 - 99.98)$.

> [!question]- mm-pnl-hedge-separate | Why report hedge trades as their own bucket?
> They are usually aggressive, so their edge at fill is negative, and mixing them with passive fills hides the true cost of hedging and understates quoting edge.
> Separating them shows whether losses come from quoting or from risk management.

> [!question]- mm-pnl-negative-horizon | Your markout curve is already falling at negative horizons: the markout at -1 s is above the markout at 0. What does that tell you?
> The reference moved toward your price before the fill, so you were filled because your quote was stale.
> That points to update latency or thresholds, not to toxic counterparties.

> [!question]- mm-pnl-cluster-se | Venue B has 10,000 fills in about 1,000 bursts with per-fill standard deviation 4 ticks. What standard error do you use for its mean markout?
> About 0.126 ticks: $4/\sqrt{1000}$.
> Fills in a burst share the same future path, so count clusters, not fills; $4/\sqrt{10000} = 0.04$ would overstate precision threefold.

> [!question]- mm-pnl-venue-net-of-fees | Venue A marks out at -0.1 ticks at 10 s with a 0.25 rebate; venue B at -0.4 with a 0.10 fee. Which is better per fill and by how much?
> A, by 0.65 ticks: +0.15 versus -0.50 net.
> Always compare venues net of the fee or rebate on that liquidity flag.

> [!question]- mm-pnl-inventory-drift-not-alpha | A trader's P&L is mostly inventory drift and it was positive this month. Is that skill?
> Not by itself: drift is mostly the market's direction times the position held, i.e. risk taken.
> It becomes evidence of skill only if it persists after controlling for market direction and the risk used.

> [!question]- mm-pnl-options-edge-vega | You sell 100 calls (multiplier 100) 0.5 vol above theo with vega 0.19; the strike's vol then rises 0.8. Edge and vega P&L?
> Edge +950 dollars, vega P&L -1,520 dollars.
> $100 \times 100 \times 0.19 \times 0.5$ and $-100 \times 100 \times 0.19 \times 0.8$.

> [!question]- mm-pnl-reconcile | What should happen to an unexplained residual in daily attribution?
> Investigate it until it is explained: missed or busted fills, stale theo, corporate actions, late fee bookings.
> Attribution only earns trust if the buckets sum to the official P&L.

> [!question]- mm-pnl-marginal-fee | Why use marginal rather than average fees in markout analysis?
> With tiered fee schedules, the next share's fee or rebate can differ from the average, and quoting decisions are made at the margin.
> Using the average can make a venue look profitable when the marginal fill is not.

> [!question]- mm-pnl-asof-join | What is the key correctness rule when joining fills to future mids for markouts?
> Take the last reference value at or before $t_i + \tau$ with synchronised clocks, and never use a value built from data after that time.
> A forward-looking join or clock skew biases every markout.

## Further reading

- Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015), chapters on market making and adverse selection.
- Larry Harris, *Trading and Exchanges* (2003), chapters on dealers and the components of the spread.
- Euan Sinclair, *Volatility Trading* (2nd edition, 2013), on option P&L and hedging.
- pandas documentation, [merge_asof](https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html).
- Related notes: [Adverse Selection and Flow Toxicity](../07-Market-Microstructure/05-Adverse-Selection-and-Flow-Toxicity.md), [Inventory Risk and Avellaneda-Stoikov](03-Inventory-Risk-and-Avellaneda-Stoikov.md).
