---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Harris (2003) Trading and Exchanges: Market Microstructure for Practitioners. Oxford University Press, Bouchaud Bonart Donier and Gould (2018) Trades Quotes and Prices. Cambridge University Press, Moallemi and Yuan (2017) A Model for Queue Position Valuation in a Limit Order Book. Working paper Columbia University, Cartea Jaimungal and Penalva (2015) Algorithmic and High-Frequency Trading. Cambridge University Press]
---

# Limit Order Books and Order Types

## TL;DR

- A limit order book is two sorted queues of resting limit orders; the best bid and best ask form the touch, and a trade happens only when an incoming order crosses the spread.
- Price-time (FIFO) priority rewards being first at a price, so speed and queue position are the edge; pro-rata rewards displayed size, so participants over-quote and manage the risk of an oversized fill.
- Know the order types exactly: limit, market, marketable limit, IOC, FOK, post-only, hidden, iceberg (reserve) and pegged, plus what each does to your priority.
- Queue position has value because the front of the queue fills on small, mostly uninformed trades while the back fills mainly when a large, more informed order clears the whole level.
- The same limit order at the same price can have positive expected value at the front of the queue and negative expected value at the back.

## Learning objectives

- Explain price-time priority and pro-rata matching and how each changes quoting incentives.
- Use limit, market, IOC, FOK, post-only, hidden, iceberg and pegged orders correctly.
- Reason about queue position and its value.

## Core concepts

### The book

A limit order book (LOB) holds every resting limit order, grouped by price level.
The highest bid $P^b$ and lowest ask $P^a$ form the touch; the spread is $P^a - P^b$ and the mid is $(P^a + P^b)/2$.
Prices live on a grid set by the tick size $\delta$, so the spread is at least one tick.
Depth is the total size at a level; the queue is the ordered list of orders at that level.

Two regimes matter in practice.

- Large-tick instruments: the spread is almost always one tick and queues are long relative to typical trade size, so price is nearly fixed and competition happens in queue position.
- Small-tick instruments: the spread is several ticks wide, queues are short, and participants compete by improving price.

Bouchaud, Bonart, Donier and Gould use the ratio of the average spread to the tick to separate the two regimes.

### Matching

A trade happens when an incoming order is marketable: a buy priced at or above the best ask, or a sell at or below the best bid.
The incoming order is the aggressor (taker); the resting orders it trades against are passive (makers).
It walks the book from the best price outward until it is filled or its limit price is reached.

Within one price level the venue's allocation rule decides who trades.

- Price-time priority (FIFO): the earliest order at the level fills first.
  Most equity venues use it.
  Incentive: be early at a price, never lose your place by modifying, and value speed after the touch moves, because the first order at a new price level is at the front of its queue.
- Pro-rata: each resting order receives a share of the incoming size proportional to its size, $x_j = X \cdot n_j / \sum_k n_k$, usually with rounding and a minimum allocation.
  Incentive: display more size than you want to trade, because your fill is a fraction of your size.
  The risk is that a large aggressor fills much more of your oversized order than you intended.
- Hybrids: pro-rata with top-order priority (the first order to improve the price gets a guaranteed slice), FIFO with a pro-rata split, or priority for public customers and designated market makers.
  CME Globex assigns an allocation algorithm per product, and many US options exchanges use pro-rata variants with public-customer priority; check each venue's rulebook rather than assuming.

Most venues give displayed orders priority over non-displayed orders at the same price, and any modification that increases size or changes price loses time priority.
A size decrease usually keeps priority.

### Order types

| Type | What it does | Main use |
| :--- | :--- | :--- |
| Limit | Rests at a price or better until filled or cancelled | Passive quoting |
| Market | Trades immediately at whatever prices are available | Urgent execution; unbounded price risk |
| Marketable limit | A limit order priced through the touch, so it trades now but never beyond its limit | Aggressive execution with a price cap |
| IOC (immediate or cancel) | Fills what it can now, cancels the rest | Taking liquidity without leaving a resting order |
| FOK (fill or kill) | Fills the full size now or does nothing | All-or-nothing hedges |
| Post-only (add-liquidity-only) | Rejected, or repriced one tick away, if it would trade on arrival | Guaranteeing maker fees and rebates |
| Hidden | Rests but is not displayed; usually behind displayed orders at the same price | Hiding intent at a priority cost |
| Iceberg (reserve) | Displays a tip; when the tip fills, a new tip is shown with new time priority | Working a large order with partial display |
| Pegged | Price tracks a reference such as the primary touch or the mid | Midpoint liquidity, passive tracking |
| Stop | Becomes a market or limit order once a trigger price trades | Loss limits; can add to momentum |

Time in force (day, good-till-cancelled, IOC) is a separate dimension from the order type on many venues.
In US equities, an intermarket sweep order lets a router trade through a protected quote while simultaneously sending orders to take it; see [Fragmentation, Reg NMS and Routing](09-Fragmentation-Reg-NMS-and-Routing.md).

### Queue position and its value

For a resting order the expected value per share of being at a given queue position is

$$
V = P(\text{fill}) \cdot \big( h + r - \mathbb{E}[\text{adverse move} \mid \text{fill}] \big),
$$

where $h$ is the distance from your price to fair value (the half-spread at the touch), $r$ is the rebate net of fees, and the adverse move is measured at a markout horizon.
Both factors depend on queue position.

- At the front, small routine trades fill you; these carry little information, so the conditional adverse move is small.
- At the back, you fill only when enough volume trades to clear everyone ahead of you, often a large aggressor that is about to move the price through the level, so the conditional adverse move is large.

Moallemi and Yuan model this explicitly and argue that in large-tick stocks the value of a good queue position can be of the same order as the half-spread.
This is why market makers keep orders resting at levels near the touch, avoid unnecessary cancel-replace, and invest in speed to be first when a new price level forms.

A useful rough estimate of time to fill is the queue ahead that will actually trade divided by the rate of aggressive volume at that level:

$$
\mathbb{E}[T_{\text{fill}}] \approx \frac{Q_{\text{ahead}} (1 - c)}{\lambda_{\text{trade}}},
$$

where $c$ is the fraction of the queue ahead expected to cancel first.
It ignores the chance that the level is cleared or the price moves away before you fill, which is exactly when the estimate matters most, so treat it as a first pass.

## Worked examples

### Example 1: walking the book, IOC and FOK

The book is bid 49.99 and asks 50.01 x 300, 50.02 x 500, 50.03 x 400, 50.05 x 1,000.
A market buy for 1,000 fills 300 at 50.01, 500 at 50.02 and 200 at 50.03.
The average price is $(300 \cdot 50.01 + 500 \cdot 50.02 + 200 \cdot 50.03)/1000 = 50.019$.
Against the mid of 50.00 that is 0.019 per share, or 19 dollars of cost, of which 9 dollars is walking beyond the best ask.
A buy IOC for 1,000 with limit 50.02 fills 800 and cancels 200.
A buy FOK for 1,000 with limit 50.02 does nothing, because only 800 is available within the limit.
A post-only buy at 50.01 would cross the ask, so it is rejected, or on a venue that reprices it, placed at 50.00.

### Example 2: pro-rata allocation and over-quoting

Three orders rest at the bid: A 500, B 300, C 200, total 1,000.
An incoming sell for 400 allocates pro-rata: A 200, B 120, C 80.
If you add a 1,000-lot, the level holds 2,000 and the same 400 allocates A 100, B 60, C 40 and you 200.
You wanted 200 and displayed 1,000 to get it, which is the over-quoting incentive of pro-rata matching.
The cost appears on a big sweep: a 2,000 sell fills all 1,000 of yours.
Rounding matters for small orders: a 333 sell gives $\lfloor 166.5 \rfloor = 166$, $\lfloor 99.9 \rfloor = 99$, $\lfloor 66.6 \rfloor = 66$, total 331, and the 2 leftover lots go by the venue's residual rule (often time priority).

### Example 3: iceberg priority

At the 20.00 bid, orders arrived in this order: an iceberg I showing 100 of 1,000, then B 300, then C 200.
A market sell for 700 fills I 100, then B 300, then C 200.
The iceberg refreshes a new 100-lot tip at the back of the queue, behind C, and fills the last 100.
The iceberg receives 200 of the 700, whereas a fully displayed 1,000-lot at the front would have received all 700.
Hiding size costs priority on every refresh.

### Example 4: the same price, opposite signs

Half-spread 0.5 ticks to fair value, rebate net of fees 0.2 ticks.
At the front of the queue: 55% chance of a fill within 10 seconds, conditional adverse move 0.25 ticks.
At the back: 20% chance, conditional adverse move 0.85 ticks.

$$
V_{\text{front}} = 0.55 \times (0.5 + 0.2 - 0.25) = 0.2475 \text{ ticks}, \qquad
V_{\text{back}} = 0.20 \times (0.5 + 0.2 - 0.85) = -0.03 \text{ ticks}.
$$

The back-of-queue order loses money on average even though it rests at the same price.
The difference, about 0.28 ticks per share per interval, is what speed and queue management buy.

### Example 5: rough time to fill

You join a bid with 3,000 shares ahead; about 40% of those will cancel before your turn, and sells hit this level at 600 shares per second.
$\mathbb{E}[T_{\text{fill}}] \approx 3000 \times 0.6 / 600 = 3$ seconds.
If the mid typically moves within 2 seconds, most of your fills will come from the level being swept, which is the adverse case in Example 4.

```python
def walk_book(levels, qty):
    """levels: list of (price, size) sorted from best. Returns fills and average price."""
    fills, left = [], qty
    for price, size in levels:
        take = min(left, size)
        if take:
            fills.append((price, take))
            left -= take
        if left == 0:
            break
    done = qty - left
    avg = sum(p * s for p, s in fills) / done if done else float("nan")
    return fills, avg

print(walk_book([(50.01, 300), (50.02, 500), (50.03, 400), (50.05, 1000)], 1000))
```

## Pitfalls

- Treating a market order as having a known cost: it walks the book, and the book can change between decision and arrival.
- Assuming IOC and FOK are the same; FOK is all-or-nothing, IOC keeps partial fills.
- Forgetting that increasing size or changing price loses time priority, while a size decrease usually does not.
- Using an iceberg or hidden order and expecting displayed-order priority.
- Evaluating a passive order by fill probability alone, ignoring that fills at the back of the queue are adversely selected.
- Over-quoting in a pro-rata market without a hard limit on the fill you can absorb.
- Assuming every venue matches the same way; allocation rules are product- and venue-specific.
- Letting a post-only order silently reprice when the strategy assumed a fixed price.

## Interview questions

> [!question]- ms-lob-price-time-rule | What is price-time priority?
> Better prices trade first; at the same price, earlier orders trade first.
> It rewards being early at a level, so queue position and speed become the competitive edge.

> [!question]- ms-lob-pro-rata-incentive | How does pro-rata matching change how market makers quote?
> They display more size than they want to trade, because each fill is a fraction of displayed size.
> The risk is an outsized fill when a large aggressor arrives, so over-quoting needs a hard cap on absorbable size.

> [!question]- ms-lob-pro-rata-numeric | Orders of 500, 300 and 200 rest at a level with pure pro-rata allocation. A 400-lot sell arrives. Who gets what?
> 200, 120 and 80.
> Each gets $400 \times n_j / 1000$.

> [!question]- ms-lob-ioc-vs-fok | A buy for 1,000 with limit 50.02 meets 800 shares at or below 50.02. What happens as an IOC and as a FOK?
> IOC fills 800 and cancels 200; FOK fills nothing.
> FOK requires the whole quantity immediately, IOC accepts partial fills.

> [!question]- ms-lob-walk-the-book-vwap | Asks are 50.01 x 300, 50.02 x 500, 50.03 x 400 and the mid is 50.00. What does a 1,000-share market buy cost versus the mid?
> 19 dollars: the average price is 50.019.
> It takes 300 at 50.01, 500 at 50.02 and 200 at 50.03.

> [!question]- ms-lob-post-only-purpose | Why do market makers use post-only orders?
> To guarantee the order adds liquidity, so it earns the maker fee or rebate and never pays the taker fee by accident.
> If it would cross on arrival it is rejected or repriced, depending on the venue.

> [!question]- ms-lob-iceberg-refresh-priority | Why does an iceberg order get fewer fills than a fully displayed order of the same total size?
> Each refreshed tip goes to the back of the queue with new time priority.
> Other orders that arrived later than the original iceberg trade ahead of each new tip.

> [!question]- ms-lob-hidden-order-priority | Where does a hidden order usually sit relative to displayed orders at the same price?
> Behind them: most venues give displayed orders priority at the same price.
> Hiding intent is paid for with priority.

> [!question]- ms-lob-queue-value-sign | Why can the same limit order have positive value at the front of the queue and negative value at the back?
> The front fills on small, mostly uninformed trades; the back fills mainly when a large aggressor clears the level, which predicts a move through the price.
> $V = P(\text{fill})(h + r - \mathbb{E}[\text{adverse} \mid \text{fill}])$, and the conditional adverse move grows with queue position.

> [!question]- ms-lob-large-tick-competition | In a large-tick stock the spread is almost always one tick. What do market makers compete on?
> Queue position, speed to a new level, and size management, since they cannot improve price inside a one-tick spread.
> Price competition is replaced by time competition.

> [!question]- ms-lob-marketable-limit | Why use a marketable limit order rather than a market order?
> It trades immediately but caps the worst price, so a thin or changing book cannot fill you far away.
> The cost is that part of it may not fill.

> [!question]- ms-lob-modify-priority | You want to change a resting order. Which changes keep time priority on a typical FIFO venue?
> A size decrease usually keeps priority; a price change or size increase loses it.
> An increase is treated as a new order for the added quantity, so venues requeue it.

> [!question]- ms-lob-time-to-fill | 3,000 shares are ahead of you, 40% will cancel first, and sells hit the level at 600 shares per second. Rough expected time to fill?
> About 3 seconds: $3000 \times 0.6 / 600$.
> This ignores the level being cleared or the price moving away, so it is a first estimate only.

## In this repo and SDE-Interview-Prep

- [Limit order book mechanics (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/01%20-%20Market%20%26%20Microstructure%20Fundamentals/Limit%20Order%20Book%20Mechanics.md)
- [Queue position (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/01%20-%20Market%20%26%20Microstructure%20Fundamentals/Order%20Book%20Dynamics%20and%20Queue%20Position.md)

## Further reading

- Larry Harris, *Trading and Exchanges: Market Microstructure for Practitioners* (2003).
- Bouchaud, Bonart, Donier and Gould, *Trades, Quotes and Prices* (2018).
- Moallemi and Yuan (2017), A Model for Queue Position Valuation in a Limit Order Book, working paper.
- Related notes: [Exchange Mechanics, Auctions and Fees](02-Exchange-Mechanics-Auctions-and-Fees.md), [Order Book and Matching Engine](../12-Quant-Development/07-Order-Book-and-Matching-Engine.md), [Market Making Fundamentals](../08-Market-Making/01-Market-Making-Fundamentals.md).
