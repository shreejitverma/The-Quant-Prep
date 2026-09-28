---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [limit-order-books-and-order-types]
est_hours: 3
sources: [Harris (2003) Trading and Exchanges: Market Microstructure for Practitioners. Oxford University Press, Cartea Jaimungal and Penalva (2015) Algorithmic and High-Frequency Trading. Cambridge University Press, Glosten and Milgrom (1985) Bid ask and transaction prices in a specialist market with heterogeneously informed traders. Journal of Financial Economics 14(1) 71-100, Lebron (2019) The Laws of Trading. Wiley]
---

# Market Making Fundamentals

## TL;DR

- A market maker sells immediacy: it posts a bid and an ask, earns the spread from traders who need to trade now, and bears the risk of trading with people who know more.
- Every dollar of market-making P&L falls into four buckets: spread capture, adverse selection (measured by markouts), inventory P&L, and fees net of rebates.
- The break-even condition is that the half-spread plus rebate must cover the expected adverse move per fill: $h + r \ge \pi J$ in the simplest informed-flow model.
- Fill rate is a vanity metric: fills are negatively selected, so the quotes that fill most often are frequently the ones that lose most after the fill.
- Designated and registered market makers accept quoting obligations (continuous two-sided quotes within set bounds) in exchange for benefits such as fee tiers, rebates or allocation priority.

## Learning objectives

- Decompose market-maker P&L into spread capture, adverse selection, inventory P&L, fees and rebates.
- Explain why market makers exist and what obligations designated market makers carry.
- Explain why fill rate alone is a misleading metric.

## Core concepts

### Why market makers exist

Buyers and sellers rarely arrive at the same moment.
A market maker bridges that gap by standing ready to trade on both sides, holding inventory in between.
The service is immediacy, and its price is the bid-ask spread.
Harris frames the spread as compensation for three costs: order-processing costs, inventory (risk-bearing) costs, and adverse-selection costs from trading against better-informed traders.
In modern electronic markets the order-processing component is small, so competition compresses spreads until they roughly cover adverse selection and inventory risk net of exchange fees and rebates.

### The counterparties

It helps to classify the flow you trade against.

- Uninformed (noise or liquidity) flow: index rebalances, retail orders, hedgers.
  Its future price impact is close to zero, so you keep the half-spread.
- Informed flow: traders whose orders predict the next price move, whether from fundamental information, a faster read of a related market, or a better short-term model.
  You lose to them on average.
- Other market makers and arbitrageurs: they trade with you when your quote is stale relative to their fair value, which makes them informed in the short-horizon sense.

The Glosten-Milgrom model makes this precise: the spread exists even with zero costs and a risk-neutral market maker, because the ask must equal the expected value conditional on someone buying.
See [Spread Models: Roll and Glosten-Milgrom](../07-Market-Microstructure/03-Spread-Models-Roll-and-Glosten-Milgrom.md) and [Adverse Selection and Flow Toxicity](../07-Market-Microstructure/05-Adverse-Selection-and-Flow-Toxicity.md).

### The P&L identity

Let fill $i$ happen at time $t_i$ at price $p_i$ with side $d_i = +1$ for a buy and $-1$ for a sell, size $n_i$, and let $m_t$ be the mid (or your fair value).
Pick a markout horizon $\tau$ (for example 1 second or 1 minute).
Marking the final position at $m_T$, trading P&L before fees is

$$
\text{P\&L} = \sum_i n_i d_i (m_T - p_i)
= \underbrace{\sum_i n_i d_i (m_{t_i} - p_i)}_{\text{spread capture}}
+ \underbrace{\sum_i n_i d_i (m_{t_i+\tau} - m_{t_i})}_{\text{adverse selection}}
+ \underbrace{\sum_i n_i d_i (m_T - m_{t_i+\tau})}_{\text{inventory P\&L}}.
$$

The identity is exact because the three brackets telescope.
Add rebates earned on passive fills and subtract exchange, clearing and regulatory fees to get net P&L.

- Spread capture is positive for passive fills by construction: you buy below the mid and sell above it.
- Adverse selection is the short-horizon move after the fill, signed from your point of view; it is usually negative.
- Inventory P&L is what the position made or lost after the markout horizon; it is the part a hedge or skew controls.

The split between adverse selection and inventory depends on $\tau$, so always quote the horizon when you quote a markout.
The dedicated treatment is in [Market Making P&L Attribution and Markouts](09-Market-Making-PnL-Attribution-and-Markouts.md).

### Markouts

The markout of a fill at horizon $\tau$ is $d_i(m_{t_i+\tau} - p_i)$ per share: spread capture plus adverse selection.
A markout curve plots the average markout against $\tau$ (for example 100 ms, 1 s, 10 s, 60 s, 5 min).
A healthy passive book starts near the half-spread at $\tau = 0$ and decays; the level where it flattens is the true edge per share.
A curve that keeps falling for minutes means you are trading against slow informed flow, and a curve that crosses zero within milliseconds means your quotes are being picked off by faster participants.

### The break-even spread

Suppose a fraction $\pi$ of fills comes from informed traders who move the price by $J$ against you, the rest carry no information, your half-spread is $h$ and the passive rebate is $r$ per share.
Expected P&L per share filled is

$$
(1-\pi)(h + r) + \pi(h + r - J) = h + r - \pi J.
$$

Quoting is profitable only if $h + r > \pi J$.
This one line explains most market-making behaviour: widen when $\pi$ or $J$ rises (news, volatility, a toxic counterparty), tighten when flow is benign, and value rebates because they add directly to $h$.

### Why fill rate misleads

Fills are not a random sample of your quotes.
You are most likely to be filled exactly when your price is wrong: the ask gets lifted just before the price rises.
This is the winner's curse of passive trading.
So a strategy that doubles its fill rate by quoting more aggressively can lose money even though volume and spread capture both rise.
The right objective is total edge, fills times markout at a horizon that reflects your holding period, net of fees and risk.
Queue position matters for the same reason: being first in the queue at a price level gets you the benign fills too, while being last means you are often filled only when the level is about to be traded through.

### Obligations and incentives

Exchanges run programmes for designated or registered market makers.
The common pattern is obligations (maintain continuous two-sided quotes for a minimum fraction of the session, within a maximum width or a percentage band around the national best bid and offer, at a minimum size) in exchange for benefits (lower fees, higher rebates, allocation preferences in some options markets, or a special role in opening and closing auctions).
In US equities, after the May 2010 flash crash, the SEC approved exchange rules that ended "stub quotes" by requiring registered market makers to keep quotes within a set percentage of the NBBO.
The exact parameters differ by venue and change over time, so check the current rulebook before quoting a number in an interview.
The economic point is that obligations force you to quote when you would rather step away, which is when adverse selection is highest, so the benefits must pay for that option you have given up.

### Fees and rebates

Many equity venues are maker-taker: the passive side earns a rebate and the aggressive side pays a fee.
Some are inverted (taker-maker), paying the aggressor and charging the passive side, which attracts orders that want queue priority.
For a market maker the rebate is part of $h$ and can be the whole edge in one-tick-wide names.
See [Exchange Mechanics, Auctions and Fees](../07-Market-Microstructure/02-Exchange-Mechanics-Auctions-and-Fees.md).

## Worked examples

### Example 1: decomposing a three-fill tape

Quotes are 99.99 / 100.01 around a 100.00 mid; each fill is 100 shares; the markout horizon is 1 second; the session ends with the mid at 99.99.

| Fill | Side | Price | Mid at fill | Mid 1 s later |
| :--- | :--- | ---: | ---: | ---: |
| 1 | buy | 99.99 | 100.00 | 99.995 |
| 2 | buy | 99.98 | 99.99 | 99.985 |
| 3 | sell | 100.00 | 99.99 | 99.995 |

Spread capture: each fill is 0.01 better than the mid, so $3 \times 100 \times 0.01 = 3.00$ dollars.
Adverse selection: fill 1 sees $-0.005$, fill 2 sees $-0.005$, and fill 3 (a sell) sees the mid rise by 0.005, also $-0.005$ from our side, so $-1.50$ dollars in total.
Inventory P&L from 1 s to the close: fill 1 $(99.99 - 99.995) = -0.005$, fill 2 $(99.99 - 99.985) = +0.005$, fill 3 $-(99.99 - 99.995) = +0.005$, so $+0.50$ dollars.
Total: $3.00 - 1.50 + 0.50 = 2.00$ dollars.
Check directly: cash is $-9999 - 9998 + 10000 = -9997$ and the long 100 shares are worth $9999$ at the close, so P&L is $+2.00$.
Half of the captured spread was given back to adverse selection within a second; that ratio is the number a desk watches.

### Example 2: a day of P&L with fees

A desk fills 1,000 passive orders of 100 shares (100,000 shares) at an average half-spread of 0.01 dollars.
The 1-second markout shows an average adverse move of 0.006 dollars per share.
The venue pays a 0.0020 dollars per share maker rebate, clearing and regulatory costs are 0.0005 dollars per share, and the end-of-day inventory lost 150 dollars.

- Spread capture: $100{,}000 \times 0.01 = 1{,}000$.
- Adverse selection: $-100{,}000 \times 0.006 = -600$.
- Rebates: $+200$.
  Costs: $-50$.
- Inventory: $-150$.

Net P&L is $1000 - 600 + 200 - 50 - 150 = 400$ dollars, or 0.4 cents per share.
Note how the rebate (200) is half the final result: in tight names the fee schedule is not a detail.

### Example 3: fill rate versus edge

Strategy A quotes at the touch aggressively and gets 1,000 fills a day, with half-spread 1 tick and a 1-second markout of $-0.8$ ticks per fill.
Strategy B quotes more selectively and gets 300 fills, with half-spread 1 tick and markout $-0.2$ ticks.
A earns $1000 \times (1 - 0.8) = 200$ ticks; B earns $300 \times (1 - 0.2) = 240$ ticks.
B wins with 70% fewer fills and far less inventory risk.
A manager looking at fill rate or volume share would pick A.

### Example 4: break-even half-spread

Flow analysis says 20% of fills are informed and the price then moves 5 ticks against you.
Without rebates the break-even half-spread is $\pi J = 0.2 \times 5 = 1$ tick, so a 2-tick-wide market is exactly break-even.
With a rebate worth 0.3 ticks the break-even half-spread falls to $1 - 0.3 = 0.7$ ticks.
If news raises the informed share to 30% and the jump to 4 ticks, break-even rises to 1.2 ticks and the 2-tick market loses money: widen, reduce size, or pull.

## Pitfalls

- Reporting markouts without a horizon; a 100 ms markout and a 5 minute markout answer different questions.
- Measuring markouts against the last trade price instead of the mid or a fair value; the trade price bounces between bid and ask.
- Treating the rebate as free money: in one-tick markets it is often the only edge, and venues change fee tiers.
- Optimising fill rate or market share instead of edge per share times volume.
- Assuming queue position is irrelevant; fills at the back of a queue are much more toxic than fills at the front.
- Confusing inventory P&L with alpha; a lucky position in a trending market is not repeatable edge.
- Forgetting that obligations bind exactly when quoting is least attractive.

## Interview questions

> [!question]- mm-fund-pnl-four-components | What are the four components of market-maker P&L?
> Spread capture, adverse selection, inventory P&L, and fees net of rebates.
> Spread capture is $d(m_t - p)$ at the fill, adverse selection is the signed mid move over a short markout horizon, inventory P&L is what the position makes after that horizon, and fees and rebates are added per share.

> [!question]- mm-fund-markout-definition | Define the markout of a fill at horizon tau.
> $d(m_{t+\tau} - p)$ per share, where $d=+1$ for a buy and $-1$ for a sell, $p$ is the fill price and $m$ the mid or fair value.
> It equals spread capture $d(m_t - p)$ plus adverse selection $d(m_{t+\tau} - m_t)$.

> [!question]- mm-fund-break-even-half-spread | A fraction pi of fills is informed and moves the price J against you. What half-spread h breaks even, with rebate r?
> $h = \pi J - r$.
> Expected P&L per share is $(1-\pi)(h+r) + \pi(h+r-J) = h + r - \pi J$, which is zero at that $h$.

> [!question]- mm-fund-fill-rate-misleading | Why is a high fill rate not evidence of a good market-making strategy?
> Because fills are adversely selected: you get filled most when your quote is wrong.
> A more aggressive quote raises fills and gross spread capture but can lower markouts by more, so total edge (fills times net markout) can fall.

> [!question]- mm-fund-why-spread-exists | Name the three classical components of the bid-ask spread.
> Order-processing costs, inventory (risk-bearing) costs and adverse-selection costs.
> In electronic markets processing costs are small, so competition pushes the spread towards adverse selection plus inventory risk net of fees.

> [!question]- mm-fund-telescoping-identity | Why does spread capture plus adverse selection plus inventory P&L exactly equal trading P&L?
> Because $d(m_t - p) + d(m_{t+\tau} - m_t) + d(m_T - m_{t+\tau}) = d(m_T - p)$ for each fill, and summing $d(m_T - p)$ over fills is cash plus final position marked at $m_T$.
> The split between the last two terms depends on the chosen horizon $\tau$.

> [!question]- mm-fund-markout-curve-shape | Your average markout is +0.5 ticks at 0 ms and -0.3 ticks at 50 ms. What does that tell you?
> You are being picked off by faster participants: your quotes are stale and trade just before the price moves through them.
> The fix is latency, faster cancel logic or wider quotes around predictable events, not a different long-horizon model.

> [!question]- mm-fund-rebate-share-of-pnl | Half-spread 0.5 cents, rebate 0.2 cents, 1-second adverse move 0.6 cents per share. Edge per share?
> $+0.1$ cents per share.
> $0.5 + 0.2 - 0.6 = 0.1$; without the rebate the strategy would lose 0.1 cents per share.

> [!question]- mm-fund-dmm-obligations | What do designated or registered market makers typically commit to, and why is it costly?
> Continuous two-sided quotes for a minimum share of the session, within a maximum width or band around the NBBO, at a minimum size.
> It is costly because it removes the option to step away exactly when adverse selection is highest, so it must be paid for with fee, rebate or allocation benefits.

> [!question]- mm-fund-queue-position-toxicity | Why are fills at the back of a queue more toxic than fills at the front?
> A back-of-queue order only fills when the whole level is being consumed, which is often just before the price moves through it.
> Front-of-queue orders also collect small, uninformed trades that do not clear the level.

> [!question]- mm-fund-maker-taker-inverted | What is the difference between a maker-taker and an inverted venue for a market maker?
> Maker-taker pays the passive side a rebate and charges the aggressor; inverted venues charge the passive side and pay the aggressor.
> Inverted venues trade off a worse fee for better queue position and fill probability.

> [!question]- mm-fund-inventory-vs-alpha | Your desk made most of its P&L from inventory P&L this month. Is that good?
> Not necessarily: inventory P&L is directional exposure, not market-making edge.
> Check whether it is repeatable (a real signal driving skew) or luck in a trending market, and whether the risk taken was within limits.

## In this repo and SDE-Interview-Prep

- Systems and regulation companion: [Quant Dev Market Making Guide](Quant-Dev-MM-Guide/README.md), including [Quantitative Models and Strategies](Quant-Dev-MM-Guide/03_Quantitative_Models_and_Strategies.md).
- Next: [Fair Value and Theoretical Pricing](02-Fair-Value-and-Theoretical-Pricing.md) and [Inventory Risk and Avellaneda-Stoikov](03-Inventory-Risk-and-Avellaneda-Stoikov.md).

## Further reading

- Larry Harris, *Trading and Exchanges: Market Microstructure for Practitioners* (2003), chapters on dealers and bid-ask spreads.
- Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015), chapters on market making.
- Glosten and Milgrom (1985), Bid, ask and transaction prices in a specialist market with heterogeneously informed traders, *Journal of Financial Economics* 14(1).
- Agustin Lebron, *The Laws of Trading* (2019).
