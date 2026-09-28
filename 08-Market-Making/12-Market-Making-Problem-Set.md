---
type: problem-set
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [quote-management-skew-width-and-size, market-making-games]
est_hours: 5
sources: [Lebron (2019) The Laws of Trading. Wiley, Cartea Jaimungal and Penalva (2015) Algorithmic and High-Frequency Trading. Cambridge University Press, Avellaneda and Stoikov (2008) High-frequency trading in a limit order book. Quantitative Finance 8(3) 217-224, Glosten and Milgrom (1985) Journal of Financial Economics 14(1) 71-100, Natenberg (2015) Option Volatility and Pricing 2nd edition. McGraw-Hill, Sinclair (2013) Volatility Trading 2nd edition. Wiley]
---

# Market Making Problem Set

## TL;DR

- Most market-making interview questions reduce to one expected-value inequality: half-spread plus rebate against the expected adverse move, the inventory risk charge and the hedge cost.
- When someone trades with you, update: a fill is information, so move your fair value toward the side that traded before quoting again.
- Inventory is managed by skew first and hedging second; hedge when the risk cost of holding exceeds the cost of crossing.
- Options questions are volatility questions: price in vol, think in gamma versus theta, and bucket vega.
- Systems questions test whether you can bound the worst case: open orders plus in-flight orders plus position, stale quotes, feed gaps and kill switches.

## Learning objectives

- Answer market-making interview questions on quoting, inventory, adverse selection and hedging.

## Core concepts

The toolkit this set draws on, with the notes that derive each piece:

- Break-even against informed flow: $h + r \ge \pi J$, where $\pi$ is the informed share of fills and $J$ the informed move; see [Market Making Fundamentals](01-Market-Making-Fundamentals.md).
- Glosten-Milgrom quotes: $\text{ask} = \mathbb{E}[V \mid \text{buy}]$, $\text{bid} = \mathbb{E}[V \mid \text{sell}]$; with two values the half-spread is $\mu (V_H - V_L)/2$; see [Adverse Selection and Flow Toxicity](../07-Market-Microstructure/05-Adverse-Selection-and-Flow-Toxicity.md).
- Avellaneda-Stoikov: reservation price $r = s - q\gamma\sigma^2(T - t)$ and total spread $\gamma\sigma^2(T - t) + \frac{2}{\gamma}\ln(1 + \gamma/k)$; see [Inventory Risk and Avellaneda-Stoikov](03-Inventory-Risk-and-Avellaneda-Stoikov.md).
- Quote EV: $P(\text{fill}) \times (h + r - \mathbb{E}[\text{adverse} \mid \text{fill}])$; see [Quote Management: Skew, Width and Size](05-Quote-Management-Skew-Width-and-Size.md).
- Hedge-or-hold: hedge when $\tfrac{1}{2}\gamma\sigma^2 q^2 t_{\text{hold}} > c|q|$, i.e. $|q| > 2c/(\gamma\sigma^2 t_{\text{hold}})$; see [Hedging and Risk for Market Makers](06-Hedging-and-Risk-for-Market-Makers.md).
- Options: ATM straddle $\approx 0.8\,\sigma\sqrt{T}\,S$; delta-hedged P&L $\approx \tfrac{1}{2}\Gamma S^2(\sigma_{\text{realised}}^2 - \sigma_{\text{implied}}^2)\Delta t$; event variance adds to base variance; see [Options Market Making](07-Options-Market-Making.md).
- Attribution: edge at fill + adverse selection to $\tau$ + inventory drift + hedge cost + fees; see [Market Making P&L Attribution and Markouts](09-Market-Making-PnL-Attribution-and-Markouts.md).

The interview habit that matters most: state the fair value, state the width and why, then say what you would do after each possible trade.

## Worked examples

### Example 1: a market on the maximum of two dice, with a counterparty who may have peeked

Make a market on the maximum of two fair dice.
Fair value: $P(\max \le m) = (m/6)^2$, so $\mathbb{E}[\max] = \sum_{m=1}^{6} m\,\frac{2m - 1}{36} = 161/36 \approx 4.47$.
You quote 4 bid, 5 offer.

Suppose the counterparty has seen one die, with value $x$.
Their conditional fair value is $\mathbb{E}[\max(x, Y)] = (x^2 + \sum_{y > x} y)/6$:

| $x$ | 1 | 2 | 3 | 4 | 5 | 6 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| $\mathbb{E}[\max \mid x]$ | 3.50 | 3.67 | 4.00 | 4.50 | 5.17 | 6.00 |

An informed counterparty buys at 5 when $x \in \{5, 6\}$ and sells at 4 when $x \in \{1, 2\}$.
Your expected P&L per interaction is $-\frac{1}{6}(0.167 + 1 + 0.5 + 0.333) = -1/3$.
Against an uninformed counterparty who buys or sells with equal probability you earn $\frac{1}{2}(5 - 4.47) + \frac{1}{2}(4.47 - 4) = 0.5$.
Break-even informed share: $(1 - \pi) \times 0.5 = \pi \times \frac{1}{3}$, so $\pi = 0.6$.
Against a pure informed trader no finite width wins: you only break even by quoting 3.5 / 6, where nobody trades.

Now you are lifted at 5 and believe half your counterparties are informed.
A buy has probability $\frac{1}{2} \cdot \mathbb{1}\{x \ge 5\} + \frac{1}{4}$ given $x$: 0.25 for $x \le 4$ and 0.75 for $x \ge 5$.
Posterior fair value $= \frac{0.25(3.5 + 3.67 + 4 + 4.5) + 0.75(5.17 + 6)}{2.5} = 59/12 \approx 4.92$.
Move the market up, for example to 4.6 / 5.4, rather than showing the same 4 / 5 again.

### Example 2: Avellaneda-Stoikov quotes with inventory

$s = 100$, $q = 5$ long, $\gamma = 0.1$, $\sigma = 2$, $T - t = 0.5$, $k = 1.5$.
Reservation price $r = 100 - 5 \times 0.1 \times 4 \times 0.5 = 99.00$.
Total spread $= 0.1 \times 4 \times 0.5 + 20 \ln(1 + 0.1/1.5) = 0.2 + 1.291 = 1.491$.
Quotes: bid $99.00 - 0.745 = 98.25$, ask $99.00 + 0.745 = 99.75$.
Flat, the same spread sits around 100: 99.25 / 100.75.
Being long 5 lowers both quotes by a full point, so the ask is now 0.25 below the mid: you are keen to sell.
Doubling inventory doubles the shift and leaves the spread unchanged, because in this model the spread does not depend on $q$.

### Example 3: hedge now or wait for passive fills?

You are long $q$ shares.
Crossing the spread to hedge costs $c = 0.005$ dollars per share.
Waiting to offload passively takes about $t = 60$ seconds, the stock's volatility is $\sigma = 0.004$ dollars per share per $\sqrt{\text{s}}$, and your risk aversion is $\gamma = 0.02$ per dollar.
Risk cost of waiting $\tfrac{1}{2}\gamma\sigma^2 q^2 t$ against hedge cost $cq$ gives the threshold

$$
q^* = \frac{2c}{\gamma\sigma^2 t} = \frac{2 \times 0.005}{0.02 \times 1.6 \times 10^{-5} \times 60} \approx 521 \text{ shares}.
$$

Below about 500 shares, skew and wait; above it, hedge at least the excess.
The threshold falls with the square of volatility: if $\sigma$ doubles, $q^*$ falls to about 130 shares, which is why desks hedge more aggressively in fast markets.

### Example 4: sizing an over-quote in a pro-rata market

Others show 8,000 lots at the bid.
Aggressors are 200 lots 80% of the time and 5,000 lots 20% of the time.
You never want more than 1,500 lots from a single aggressor.
With your size $S$, a 5,000-lot fills $5000 S/(S + 8000)$, so $5000 S \le 1500(S + 8000)$ gives $S \le 3{,}428$.
Show 3,400: a 200-lot fills you about 60 lots and a 5,000-lot about 1,491 lots, an average of about 346 per aggressor.
Quoting 1,500 would have been safe but earned far fewer fills; the pro-rata rule rewards size up to the point where the tail fill hits your limit.

### Example 5: gamma scalping P&L

You are long 500 at-the-money straddles (multiplier 100) on a 100 stock, 3 months to expiry, implied vol 20%, delta hedged.
Gamma per option at the money: $\Gamma = \varphi(d_1)/(S\sigma\sqrt{T}) \approx 0.0398$, so the position gamma is $500 \times 100 \times 2 \times 0.0398 \approx 3{,}984$ shares per dollar.
Daily theta cost $\approx \tfrac{1}{2}\Gamma S^2\sigma_{\text{imp}}^2/252 = \tfrac{1}{2} \times 3984 \times 10^4 \times 0.04/252 \approx 3{,}162$ dollars.
If the stock realises 30%, gamma earns $\tfrac{1}{2} \times 3984 \times 10^4 \times 0.09/252 \approx 7{,}115$ dollars a day, net about $+3{,}953$.
The daily break-even move is $S\sigma_{\text{imp}}/\sqrt{252} = 100 \times 0.2/15.87 \approx 1.26$ dollars: move more than that on average and the long-gamma book wins.

### Example 6: implied earnings move from two straddles

A 100 stock reports this week.
The weekly at-the-money straddle costs 6.00; a comparable week without earnings would cost about 2.50.
Using straddle $\approx 0.8 \times$ standard deviation, the total weekly standard deviation is $6.00/0.8 = 7.5$ and the base is $2.50/0.8 = 3.125$.
Variances add, so the event standard deviation is $\sqrt{7.5^2 - 3.125^2} \approx 6.82$, and the implied mean absolute event move is about $0.8 \times 6.82 \approx 5.45$ dollars.
Subtracting straddle prices directly (6.00 - 2.50 = 3.50) understates it, because standard deviations do not add.
Compare 5.45 with the stock's history of earnings-day moves before leaning.

### Example 7: what stale quotes cost and what speed is worth

Across your book, 1,000 times a day a leading instrument moves enough to make 20 of your resting quotes stale.
Each stale quote is 500 shares and is 0.5 cents per share wrong when picked off.
You lose the cancel race 30% of the time.
Expected cost $= 1000 \times 20 \times 0.3 \times 500 \times 0.005 = 15{,}000$ dollars a day.
Cutting the race-loss rate to 10% saves 10,000 dollars a day, about 2.5 million dollars a year over 250 days: that is the budget for the latency work.
Widening every quote to compensate would cost far more in lost edge on benign fills.

```python
from fractions import Fraction as F

# Example 1: conditional fair value of max(x, Y) and the posterior after being lifted
cond = {x: F(x * x + sum(range(x + 1, 7)), 6) for x in range(1, 7)}
w = {x: F(1, 2) * (x >= 5) + F(1, 4) for x in cond}
print(sum(cond.values()) / 6, sum(w[x] * cond[x] for x in cond) / sum(w.values()))  # 161/36 59/12
```

## Pitfalls

- Quoting a fair value and width but not saying what you do after you trade.
- Keeping the same market after being lifted, which invites the informed trader to lift you again.
- Treating fill rate as success; fills are negatively selected.
- Forgetting fees, rebates and the hedge cost in the break-even.
- Adding standard deviations (or straddle prices) where variances add.
- Hedging every share immediately, or never hedging; the threshold depends on cost, volatility and holding time.
- In systems answers, bounding risk by position alone and ignoring open and in-flight orders.
- Over-quoting in pro-rata without a cap on the tail fill.

## Interview questions

### Quoting

> [!question]- mm-pset-quoting-dice-max-fair | Make a market on the maximum of two dice. What is fair value?
> $161/36 \approx 4.47$.
> $P(\max = m) = (2m - 1)/36$, so $\mathbb{E}[\max] = \sum m(2m-1)/36 = 161/36$.

> [!question]- mm-pset-quoting-informed-breakeven | You quote 4 / 5 on the max of two dice. An informed counterparty has seen one die; an uninformed one trades randomly. What informed share breaks you even?
> 60%.
> You lose $1/3$ per informed interaction and earn $1/2$ per uninformed one, so $(1 - \pi)/2 = \pi/3$.

> [!question]- mm-pset-quoting-update-after-lift | Half your counterparties may have seen one die. You are lifted at 5. Where is fair value now?
> About 4.92 ($59/12$).
> A buy is three times as likely when the seen die is 5 or 6, so weight those conditional values 0.75 against 0.25 for the others.

> [!question]- mm-pset-quoting-join-or-improve | Joining gives a 35% fill chance at a 2-tick half-spread with 1.5 ticks adverse move; improving gives 70% at 1 tick with 0.8 adverse. Which?
> Join: 0.175 ticks against 0.14.
> $0.35 \times (2 - 1.5)$ versus $0.7 \times (1 - 0.8)$; higher fill rate does not compensate for worse selection.

> [!question]- mm-pset-quoting-one-sided | The market is 100.00 / 100.01, your theo is 100.008 and your minimum edge is 0.4 cents. What do you quote?
> Bid at 100.00 (0.8 cents of edge) and no ask at 100.01 (only 0.2 cents); offer one tick higher or not at all.
> Each side must clear the minimum edge against theo on its own.

> [!question]- mm-pset-quoting-prorata-size | Others show 8,000 at a pro-rata level; the largest aggressor is 5,000 and you accept at most 1,500 from one trade. Maximum size to show?
> About 3,428.
> $5000 S/(S + 8000) \le 1500$ gives $S \le 12{,}000{,}000/3500$.

### Inventory

> [!question]- mm-pset-inventory-as-reservation | Avellaneda-Stoikov with $s = 100$, $q = 5$, $\gamma = 0.1$, $\sigma = 2$, $T - t = 0.5$. Reservation price?
> 99.00.
> $r = s - q\gamma\sigma^2(T-t) = 100 - 5 \times 0.1 \times 4 \times 0.5$.

> [!question]- mm-pset-inventory-as-spread | Same parameters with $k = 1.5$. What is the optimal total spread and the quotes?
> About 1.49, so 98.25 / 99.75.
> $\gamma\sigma^2(T-t) + \frac{2}{\gamma}\ln(1 + \gamma/k) = 0.2 + 1.291$, centred on 99.00.

> [!question]- mm-pset-inventory-doubled | Inventory doubles in Avellaneda-Stoikov. What happens to the skew and to the spread?
> The reservation-price offset doubles; the spread is unchanged.
> The offset is linear in $q$ and the spread formula does not contain $q$.

> [!question]- mm-pset-inventory-hedge-threshold | Hedge cost 0.005 per share, $\sigma = 0.004$ per $\sqrt{\text{s}}$, 60 s to offload passively, $\gamma = 0.02$. Above what position do you hedge?
> About 521 shares.
> Hedge when $\tfrac{1}{2}\gamma\sigma^2 q^2 t > cq$, so $q^* = 2c/(\gamma\sigma^2 t)$.

> [!question]- mm-pset-inventory-threshold-vol | Volatility doubles. What happens to the hedge threshold?
> It falls by a factor of four.
> $q^* \propto 1/\sigma^2$: holding risk grows with variance while the hedge cost per share is unchanged.

> [!question]- mm-pset-inventory-half-life | Under your skew, inventory follows $q_{t+1} = 0.9\,q_t + \varepsilon_t$ per minute. What is its half-life?
> About 6.6 minutes.
> $\ln 0.5/\ln 0.9 \approx 6.58$; compare it with your markout horizon to see how much drift risk you carry.

### Adverse selection

> [!question]- mm-pset-as-breakeven-share | Half-spread 0.5 ticks, rebate 0.2 ticks, informed fills move the price 3 ticks. What informed share of fills breaks you even?
> About 23%.
> $h + r = \pi J$ gives $\pi = 0.7/3$.

> [!question]- mm-pset-as-gm-quotes | Glosten-Milgrom with $V \in \{90, 110\}$ equally likely and 30% informed traders. Quotes?
> 97 bid, 103 ask.
> Half-spread $= \mu(V_H - V_L)/2 = 0.3 \times 10$.

> [!question]- mm-pset-as-alone-at-best | Your quotes fill most when you are alone at the best price, and those fills mark out worst. Why?
> Being alone at the best usually means your theo is the outlier, and the fills tell you the others were right.
> It is the winner's curse of quoting; condition on how far you are from the rest of the market.

> [!question]- mm-pset-as-sweep | An IOC sweeps your quote and the same price on three other venues in the same microsecond. How do you react?
> Treat it as informed: fade and widen on your remaining quotes and move theo toward the sweep's side.
> Multi-venue sweeps are expensive to send and usually carry short-horizon information.

> [!question]- mm-pset-as-better-client | Client A pays you 1 tick of spread and marks out -2 ticks at a minute; client B pays 0.3 ticks and marks out -0.1. Who is the better client?
> B: +0.2 ticks per trade against -1 for A.
> Net edge is spread paid plus markout, not spread paid alone.

> [!question]- mm-pset-as-latency-pickoff | Why do ETF quotes get picked off when the index future moves?
> The future often leads; until your quote updates, it is priced off a stale theo, and faster traders take it.
> The cost is the probability of losing the cancel race times size times the stale amount.

### Hedging

> [!question]- mm-pset-hedging-future-contracts | You are long 1 million dollars of a stock with beta 1.2 to an index at 5,000 whose future has a multiplier of 50. How many futures to sell?
> About 5 (4.8).
> Hedge notional is $1.2 \times 1{,}000{,}000$ and each contract is $50 \times 5000 = 250{,}000$.

> [!question]- mm-pset-hedging-residual-vol | Stock vol 30%, correlation with the hedge 0.6, minimum-variance hedge. Residual vol?
> 24%.
> $\sigma\sqrt{1 - \rho^2} = 0.3 \times 0.8$; a cross hedge removes only the correlated part.

> [!question]- mm-pset-hedging-passive-or-aggressive | When do you hedge passively rather than cross the spread?
> When the position is small relative to the hedge threshold, volatility is low, and the passive fill is likely soon; otherwise cross.
> Passive saves the spread but extends holding time, and its fills are themselves adversely selected.

> [!question]- mm-pset-hedging-frequency | You double the frequency of delta rehedging. What happens to hedging error and cost?
> Hedging error standard deviation falls by about $\sqrt{2}$; transaction costs roughly double.
> The variance of discrete-hedging error scales with the rebalancing interval, so frequency has diminishing returns.

> [!question]- mm-pset-hedging-basis | What risks remain when you hedge a stock position with index futures?
> Idiosyncratic risk, basis risk between future and cash, beta estimation error, and roll risk.
> The hedge controls market exposure, not the stock's own moves.

### Options market making

> [!question]- mm-pset-options-straddle-approx | Approximate the price of a 3-month ATM straddle on a 100 stock at 20% vol.
> About 8.
> $0.8\,\sigma\sqrt{T}\,S = 0.8 \times 0.2 \times 0.5 \times 100$.

> [!question]- mm-pset-options-gamma-scalp | Position gamma is 3,984 shares per dollar on a 100 stock; implied 20%, realised 30%. Daily hedged P&L?
> About +3,950 dollars.
> $\tfrac{1}{2}\Gamma S^2(\sigma_r^2 - \sigma_i^2)/252 = \tfrac{1}{2} \times 3984 \times 10^4 \times 0.05/252$.

> [!question]- mm-pset-options-breakeven-move | Break-even daily move for a delta-hedged long option at 20% implied on a 100 stock?
> About 1.26 dollars.
> $S\sigma/\sqrt{252}$: theta equals gamma P&L when the daily move has that size.

> [!question]- mm-pset-options-conversion | Stock 100, 100-strike call 5.20 and put 4.80, zero rates and dividends, European. Is there an arbitrage?
> Yes, 0.40: sell the call, buy the put, buy the stock.
> Parity requires $C - P = S - K = 0$; the conversion locks in the 0.40.

> [!question]- mm-pset-options-pin | Expiry Friday, the stock closes exactly at the strike of 500 calls you are short. What do you do?
> Buy them back cheaply before the close if you can; otherwise hedge to your best estimate of assignment and plan for either outcome.
> Assignment is uncertain, so your Monday position is unknown and exposed to any weekend gap.

> [!question]- mm-pset-options-event-straddles | Weekly straddle with earnings 6.00, without about 2.50. Implied mean absolute earnings move?
> About 5.45.
> Convert to standard deviations (7.5 and 3.125), subtract variances to get 6.82, multiply by 0.8.

> [!question]- mm-pset-options-no-early-call | Would you exercise an American call on a non-dividend-paying stock early?
> No.
> $C \ge S - Ke^{-rT} > S - K$ for positive rates, so selling the call always beats exercising it.

### Markouts and P&L

> [!question]- mm-pset-markouts-sum | Edge at fill +12,000, adverse selection -7,000, inventory drift -3,000, hedge cost -1,500, fees net +800. Total P&L, and what does it say?
> +1,300.
> Quoting kept 5,000 after selection; most of it went to holding inventory and hedging, so look at skew and hedge timing before width.

> [!question]- mm-pset-markouts-fill-rate-trap | Improving by a tick doubled fills from 1,000 to 2,000 but markout per fill fell from +0.3 to +0.1 ticks. Better?
> No: 200 ticks against 300.
> More fills at worse selection can lower total edge.

> [!question]- mm-pset-markouts-horizon | Your fills mark out positive at 1 s and negative at 5 min; you hold inventory for about 10 s. Which horizon matters?
> The one near your holding time, about 10 s.
> Moves after you have offloaded belong to whoever holds the position then, not to your quoting.

> [!question]- mm-pset-markouts-sharpe | Daily P&L averages 20,000 with a standard deviation of 10,000. Annualised Sharpe?
> About 32.
> $2 \times \sqrt{252} \approx 31.7$; Sharpe ratios this high are plausible for diversified high-turnover market making, where capacity rather than Sharpe is usually the binding constraint.

> [!question]- mm-pset-markouts-queue-segment | Which segment of your passive fills do you expect to mark out worst, by queue position?
> Fills that happen when you were at the back of the queue.
> They occur mainly when a large aggressor clears the level, which predicts a move through it.

### Systems

> [!question]- mm-pset-systems-stale-cost | 1,000 stale-making events a day, 20 quotes each, 500 shares, 0.5 cents stale, 30% race-loss rate. Daily cost?
> 15,000 dollars.
> $1000 \times 20 \times 0.3 \times 500 \times 0.005$; cutting the loss rate to 10% saves 10,000 a day.

> [!question]- mm-pset-systems-worst-case-position | Limit 10,000; you are long 6,000 with 3,000 of resting bids and 2,000 of new bids in flight. Is the limit safe?
> No: the worst case is 11,000.
> Pre-trade checks must count position plus all open and in-flight orders on the adding side.

> [!question]- mm-pset-systems-kill-switch | What should trigger an automatic kill switch on a market-making system?
> Loss or position limit breaches, abnormal fill or message rates, stale or gapped market data, and mismatches between internal state and the exchange drop copy.
> Each means the system's view of its risk can no longer be trusted.

> [!question]- mm-pset-systems-feed-gap | Your feed handler detects a sequence gap on one book. What do you do?
> Pull or stop updating quotes on the affected instruments until the book is recovered from a snapshot or retransmission.
> Quoting off a book you know is wrong invites pick-offs.

> [!question]- mm-pset-systems-throttle | You are near the venue's message-rate limit and theo moves sharply. What gets priority?
> Cancels of quotes that now have negative edge, before any new or replacement orders.
> A rejected cancel leaves a stale quote live; a delayed new quote only costs opportunity.

> [!question]- mm-pset-systems-cancel-on-disconnect | Why enable cancel-on-disconnect at the exchange?
> If your session drops, the venue cancels your resting quotes, so they cannot be picked off while you are blind.
> Without it, quotes stay live with no one able to manage them.

> [!question]- mm-pset-systems-self-match | Two of your strategies quote the same instrument. What control do you need?
> Self-match prevention, at the exchange or in your gateway.
> Trading with yourself pays fees for nothing and can look like wash trading to regulators.

## Further reading

- Agustin Lebron, *The Laws of Trading* (2019).
- Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015).
- Avellaneda and Stoikov (2008), High-frequency trading in a limit order book, *Quantitative Finance* 8(3).
- Sheldon Natenberg, *Option Volatility and Pricing* (2nd edition, 2015).
- Euan Sinclair, *Volatility Trading* (2nd edition, 2013).
- Related notes: [Market Making Games](10-Market-Making-Games.md), [Market Making Systems Architecture](11-Market-Making-Systems-Architecture.md).
