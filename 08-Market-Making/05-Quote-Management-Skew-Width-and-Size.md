---
type: concept
track: [quant-trader]
tier: core
status: solid
prereqs: [inventory-risk-and-avellaneda-stoikov]
est_hours: 3
sources: [Cartea Jaimungal and Penalva (2015) Algorithmic and High-Frequency Trading. Cambridge University Press, Lebron (2019) The Laws of Trading. Wiley, Avellaneda and Stoikov (2008) High-frequency trading in a limit order book. Quantitative Finance 8(3) 217-224, Glosten and Milgrom (1985) Journal of Financial Economics 14(1) 71-100]
---

# Quote Management: Skew, Width and Size

## TL;DR

- A quote is four numbers (bid price, bid size, ask price, ask size) built as theo minus and plus an edge, and every one of them is a risk decision.
- Width must cover fees net of rebates, expected adverse selection (the markout) and a charge for inventory risk over the expected holding time, and it is capped by competition.
- Skew moves the centre of the market away from your inventory: long means lower both quotes, or quote the selling side more aggressively and the buying side less.
- Size each side so that a full fill at the worst plausible move stays within the loss budget and the position limit; size down the side that adds to inventory.
- Pull when edge falls below the minimum, when your information is stale, or around scheduled events; improve only when the extra fills are worth more than the lost half-spread and worse selection.

## Learning objectives

- Set width from volatility, adverse selection and competition.
- Skew quotes for inventory and signals, and size quotes for risk.
- Decide when to pull, fade or improve a quote.

## Core concepts

### The quote as a function

A market maker's quoting engine maps state to quotes:

$$
p^b = \text{theo} - h - \text{skew}, \qquad p^a = \text{theo} + h - \text{skew},
$$

with half-width $h$, an inventory skew that is positive when long, and sizes $n^b, n^a$.
Theo already contains the signal views (see [Fair Value and Theoretical Pricing](02-Fair-Value-and-Theoretical-Pricing.md)); skew handles the inventory you hold.
Keeping the two separate makes each testable: markouts by signal state test theo, and inventory half-life tests skew.

### Width

A useful decomposition of the minimum half-width is

$$
h_{\min} = (\text{fee} - \text{rebate}) + \text{AS}(\tau) + \kappa \, \sigma \sqrt{\tau_{\text{hold}}},
$$

where $\text{AS}(\tau)$ is the expected adverse move after a fill at your markout horizon, $\sigma\sqrt{\tau_{\text{hold}}}$ is the price risk over the expected time to offload the position, and $\kappa$ is your price per unit of risk.
The Avellaneda-Stoikov spread has the same shape: an inventory-risk term plus a term driven by how quickly fill probability falls with distance.
See [Inventory Risk and Avellaneda-Stoikov](03-Inventory-Risk-and-Avellaneda-Stoikov.md).

Three forces then shape the actual width.

- Volatility: width scales roughly with $\sigma$, so width should react to realised and implied volatility regimes, not stay fixed.
- Toxicity: when the share of informed flow rises (news, data releases, opening auctions, a sweep across venues, a known sharp counterparty), the adverse-selection term rises and the width that maximises total edge moves out.
  This is the Glosten-Milgrom logic applied in real time; see [Adverse Selection and Flow Toxicity](../07-Market-Microstructure/05-Adverse-Selection-and-Flow-Toxicity.md).
- Competition: if others quote tighter, your wide quote does not trade.
  In a one-tick-wide stock the width is fixed by the tick, and the real decision becomes whether to be at the touch at all, with what size, and when to step back.

### Skew

Inventory skew shifts both quotes against your position.
A linear rule is $\text{skew} = c \, q$, which is Avellaneda-Stoikov's $c = \gamma\sigma^2(T-t)$.
Linear skew can become extreme at large positions, so desks often damp and cap it, for example

$$
\text{skew}(q) = S_{\max} \tanh\left(\beta \frac{q}{Q_{\max}}\right),
$$

which is steeper than linear near zero (for $\beta > 1$) and saturates at $S_{\max}$.
There are two ways to implement skew:

- Price skew: move both prices, which changes fill probabilities on both sides.
- Size skew: keep prices, show more size on the side that reduces inventory and less on the side that adds to it.

Size skew preserves queue position on the reducing side, which matters in one-tick markets where moving a price means joining the back of a new queue.
When skew would push a quote through the far touch, stop skewing and hedge actively instead (see [Hedging and Risk for Market Makers](06-Hedging-and-Risk-for-Market-Makers.md)).

### Size

Size is a risk decision, not a volume decision.
Two constraints bind:

- Loss budget: size times a plausible adverse jump (for example a 3-sigma move over your reaction time, or the historical worst move after a fill) must fit within the loss you accept per event.
- Position headroom: a full fill must not breach the position limit, so the side that adds to inventory shows at most the remaining headroom.

Smaller size near the touch and more size deeper in the book is common, because deeper quotes are only reached after a move and carry more edge.
Displayed size also leaks information and affects how others trade against you, which is why many venues offer reserve or iceberg orders.

### Pull, fade, improve, join

- Pull (cancel) when the edge versus theo falls below the minimum, when market data or your own state is stale (feed gap, lost connection, unacknowledged orders), around scheduled events, or when a limit is close.
- Fade means moving quotes away after being traded on: after your bid is hit you lower both quotes, because the fill both added inventory and told you something.
- Improve (step ahead of the best price) when the queue at the touch is long and the half-spread one tick inside still clears your minimum edge; you gain priority but give up half-spread and trade with everyone who wanted immediacy.
- Join when queue position has value: the front of a long queue gets the benign small fills.

### Update discipline

Every cancel-replace loses queue priority and costs messages.
Use thresholds and hysteresis: only move a quote when theo has moved by more than a set fraction of a tick, and cancel immediately only when edge turns negative.
Venues monitor message traffic and some apply order-to-trade ratio limits or fees, so churn has a direct cost.

## Worked examples

### Example 1: is a one-tick market worth quoting?

A 40 dollar stock has 1.5% daily volatility over a 6.5 hour session, so per-second volatility is $40 \times 0.015 / \sqrt{23400} \approx 0.00392$ dollars.
You expect to hold a fill for 30 seconds, so $\sigma\sqrt{30} \approx 0.0215$ dollars, and you charge $\kappa = 0.25$ of that: about 0.0054.
Fees are 0.0003, the rebate is 0.0020 and the 1-second markout says adverse selection is 0.0040 per share.
$h_{\min} = 0.0003 - 0.0020 + 0.0040 + 0.0054 \approx 0.0077$ dollars.
The stock trades one cent wide, so the half-spread available is 0.005: less than $h_{\min}$.
Quoting both sides at the touch all day loses on average; quote only when conditions improve the numbers (front of queue, calm period, signal agrees with the side) or quote one tick behind.

### Example 2: damped skew

Position limit $Q_{\max} = 10{,}000$ shares, maximum skew 2 ticks, $\beta = 1.5$.

| Position | tanh skew (ticks) | linear $2q/Q_{\max}$ (ticks) |
| ---: | ---: | ---: |
| 3,000 | 0.84 | 0.60 |
| 6,000 | 1.43 | 1.20 |
| 9,000 | 1.75 | 1.80 |
| 10,000 | 1.81 | 2.00 |

The damped rule leans harder on small positions, which keeps inventory mean-reverting early, and flattens at large ones, where you should be hedging rather than skewing further.

### Example 3: join or improve

The market is 99.98 / 100.02 (four ticks wide, mid 100.00).
Joining the bid at 99.98 gives a 2-tick half-spread, a 30% chance of a fill in the next interval, and an expected adverse move of 1.2 ticks given a fill: EV $= 0.3 \times (2 - 1.2) = 0.24$ ticks.
Improving to 99.99 gives a 1-tick half-spread, an 80% fill chance and a 0.9-tick adverse move: EV $= 0.8 \times (1 - 0.9) = 0.08$ ticks.
Join.
If the improved quote's adverse move were only 0.5 ticks, its EV would be $0.8 \times 0.5 = 0.40$ ticks, and improving would win.
The decision is driven by how much worse the selection gets inside the spread, not by the fill probability.

### Example 4: sizing from a loss budget

You accept at most 5,000 dollars of loss from a single adverse event, and the plausible post-fill jump in this name is 0.25 dollars.
Loss budget allows $5000 / 0.25 = 20{,}000$ shares.
You are long 3,000 against a 10,000 limit, so the bid can show at most 7,000 shares.
Show $\min(20{,}000, 7{,}000) = 7{,}000$ on the bid.
The ask can show up to the loss-budget size, since selling reduces the position; if a full ask fill would flip you to a large short, cap it at $3{,}000 + 10{,}000 = 13{,}000$ shares.

### Example 5: width against toxicity

Informed traders move the price 3 ticks and trade whenever your half-spread is below that.
Uninformed fills per hour fall with half-spread $h$: 100 at 1 tick, 30 at 2 ticks, 10 at 3 ticks.

| Informed fills per hour | $h = 1$ | $h = 2$ | $h = 3$ |
| ---: | ---: | ---: | ---: |
| 20 (calm) | 60 | 40 | 30 |
| 60 (toxic) | -20 | 0 | 30 |

Edge per hour is uninformed fills times $h$ plus informed fills times $(h - 3)$.
In calm conditions the tightest quote earns most; when toxicity triples, the widest does.
The optimal width is a function of the toxicity estimate, which is why toxicity models feed straight into the width logic.

```python
import math

def quotes(theo, q, h, s_max, beta, q_max):
    """Symmetric half-width h around theo, shifted by a damped inventory skew."""
    skew = s_max * math.tanh(beta * q / q_max)
    return theo - h - skew, theo + h - skew
```

## Pitfalls

- Setting width once and never tying it to volatility or toxicity.
- Skewing by moving prices when a size skew would keep valuable queue position.
- Letting skew push a quote through the far touch, turning a passive strategy into uncontrolled aggression.
- Sizing both sides equally regardless of position headroom.
- Improving the market because it raises fill rate, without checking markouts of the improved fills.
- Cancel-replacing on every tick of theo, losing queue priority and breaching message-rate limits.
- Quoting through scheduled events with normal width and size.
- Double counting the signal: putting it in theo and again in skew.

## Interview questions

> [!question]- mm-quote-width-components | What must your half-width cover?
> Fees net of rebates, expected adverse selection at your markout horizon, and a charge for inventory risk over the expected holding time.
> Competition caps it from above: if others quote tighter, your wider quote will not trade.

> [!question]- mm-quote-one-tick-width | A stock is one tick wide. What does width management mean there?
> Width is fixed by the tick, so the decision is whether to be at the touch, with how much size, and when to step back or quote one tick behind.
> Queue position and size skew replace price width as the controls.

> [!question]- mm-quote-skew-direction | You are long 5,000 shares. Which way do you skew and how?
> Lower the centre of your market: a lower bid to buy less and a lower or larger ask to sell more.
> Equivalently, show more size on the ask and less on the bid.

> [!question]- mm-quote-damped-skew | Why damp and cap inventory skew rather than use a linear rule?
> Linear skew grows without bound and can push quotes through the far touch at large positions.
> A capped rule such as $S_{\max}\tanh(\beta q/Q_{\max})$ leans early on small positions and hands large ones to active hedging.

> [!question]- mm-quote-size-rule | How do you size the side of your quote that would add to inventory?
> At most the minimum of the loss-budget size (max loss per event divided by the plausible adverse jump) and the remaining position headroom.
> Example: 5,000 dollar budget, 0.25 jump, 7,000 shares headroom gives 7,000.

> [!question]- mm-quote-join-vs-improve | When should you improve the best bid by a tick instead of joining it?
> When fill probability times (smaller half-spread minus the adverse move for improved fills) beats the same product for joining.
> Improving raises fill rate but usually worsens selection, so decide on markouts, not fill rate.

> [!question]- mm-quote-width-vs-toxicity | Why does the optimal width rise when flow becomes more toxic?
> Each informed fill costs $J - h$, and wider quotes both shrink that loss and screen some informed flow out, while the lost uninformed edge matters less.
> With more informed flow the balance tips from earning on many uninformed fills to avoiding informed ones.

> [!question]- mm-quote-pull-triggers | Name situations where you pull quotes rather than widen them.
> Stale or gapped market data, uncertain order state (unacknowledged orders, lost session), a limit about to breach, and the moments around scheduled releases.
> In these cases your theo cannot be trusted at any width.

> [!question]- mm-quote-fade-meaning | What does it mean to fade after being hit on the bid?
> Move both quotes down: the fill added inventory and carries information that the price may fall.
> It combines inventory skew with an update of theo on the trade itself.

> [!question]- mm-quote-hysteresis | Why not update your quotes on every change in theo?
> Each cancel-replace loses queue priority and costs messages, and venues limit or charge for excessive traffic.
> Move quotes only when theo moves by more than a threshold, and cancel immediately only when edge turns negative.

> [!question]- mm-quote-one-tick-breakeven | Half-spread 0.005, rebate 0.002, fee 0.0003, markout 0.004, risk charge 0.0054. Quote at the touch?
> No: the minimum half-width is about 0.0077, above the 0.005 available.
> $0.0003 - 0.002 + 0.004 + 0.0054 = 0.0077$; quote selectively or one tick behind.

## In this repo and SDE-Interview-Prep

- Skew and limit tiers in the systems companion: [Quantitative Models and Strategies](Quant-Dev-MM-Guide/03_Quantitative_Models_and_Strategies.md), section 2.
- Microstructure background: [Order Book Imbalance and Microprice](../07-Market-Microstructure/11-Order-Book-Imbalance-and-Microprice.md).

## Further reading

- Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015), chapters on market making with inventory and adverse selection.
- Agustin Lebron, *The Laws of Trading* (2019).
- Avellaneda and Stoikov (2008), High-frequency trading in a limit order book, *Quantitative Finance* 8(3).
