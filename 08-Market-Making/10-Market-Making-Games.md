---
type: concept
track: [quant-trader]
tier: core
status: solid
prereqs: [expectation-variance-and-linearity, market-making-fundamentals]
est_hours: 4
sources: [Lebron (2019) The Laws of Trading. Wiley, Zhou (2008) A Practical Guide to Quantitative Finance Interviews, Glosten and Milgrom (1985) Journal of Financial Economics 14(1) 71-100, The-Quant-Prep tools/qp/drills.py MarketMakingGame (rules of qp drill mm)]
---

# Market Making Games and Trading Simulations

## TL;DR

- A make-a-market game tests four things: a calibrated fair value, a width that reflects both uncertainty and the risk that your counterparty knows more, updating on every piece of information (including the trades themselves), and managing your position.
- Start with the expectation and standard deviation; say both out loud, then quote around the expectation with a width you can defend.
- Assume the interviewer is informed: being lifted is evidence the value is higher, being hit is evidence it is lower, and even no trade is evidence it is near your mid.
- In `./qp drill mm` (sum of 4 hidden dice, width 1 to 4, half the counterparties know the total) the widest allowed market centred on your best estimate is the best quote in every round.
- Narrate: "Fair is 14, standard deviation about 3.4; I'm 12 at 16, ten up."

## Learning objectives

- Make a two-sided market on an uncertain quantity and update it as information arrives.
- Manage position and risk across a sequence of trades in an interview game.
- Explain your width, skew and sizing decisions out loud.
- Practise with `qp drill mm` until quoting feels automatic.

## Core concepts

### The format

The interviewer names a quantity with an uncertain value (a dice sum, a card total, a Fermi estimate, a coin-flip count) and asks for a market: a bid, an ask and usually a size.
They may buy at your ask, sell at your bid, or pass, and then reveal more information or ask for a new market.
At the end, positions settle at the true value.
Often the interviewer knows the answer or knows more than you, so every trade they make is potentially informed.
See [Trading Games in Interviews](../13-Interview-Playbook/05-Trading-Games-in-Interviews.md) for the interview mechanics and [Game Theory for Traders](../11-Risk-and-Trading/07-Game-Theory-for-Traders.md) for strategic play.

### Fair value first

Compute the expectation with linearity (see [Expectation, Variance and Linearity](../01-Probability/04-Expectation-Variance-and-Linearity.md)).
For a sum of $n$ fair dice, $\mathbb{E}[T] = 3.5n$ and $\operatorname{Var}(T) = \frac{35}{12}n$.
For quantities you must estimate, give a point estimate and a range you are roughly 80 to 90% confident in, and explain the decomposition.
Quoting an honest centre matters more than any other decision: a mid that is off by more than the half-width hands the counterparty a free trade.

### Width

Width protects you from two things: uncertainty about the value and a counterparty who may know it.
Against uninformed flow, a width of a fraction of a standard deviation earns edge.
Against a fully informed counterparty, any width loses: they trade only when the value is outside your market.
The Glosten-Milgrom logic applies directly: with a fraction $\pi$ of informed counterparties, you need uninformed edge $(1-\pi)\times$ half-width to exceed $\pi\times$ the expected amount by which the value lies beyond your quote.
Too wide looks unhelpful and the interviewer may push you to tighten; too tight looks naive.
Tighten as information arrives and uncertainty shrinks.

### Updating on trades

Treat the counterparty's action as data and apply Bayes (see [Conditional Probability and Bayes](../01-Probability/02-Conditional-Probability-and-Bayes.md)).
If they lift your ask, raise your estimate; if they hit your bid, lower it; if they pass, the value is more likely inside your market.
The size of the update depends on how likely they are to be informed.
Forgetting to update on trades is the most common mistake candidates make in these games.

### Position management

Know your worst case at every point: position times the distance to the extreme possible value.
Skew your market against your position when counterparties respond to price (real markets and most interviewers do).
Do not let the position grow to the point where one more fill makes the worst case unacceptable; reduce size or step back.
In a game where counterparties do not respond to price (like the drill below), skewing away from fair value only gives away edge, so centre on your best estimate and control risk with size instead.

### Communication

Say the fair value, the uncertainty, the market and the size in one breath.
After each trade or reveal, say how your fair value moved and why, then give the new market.
Interviewers score reasoning as much as P&L.

### The repo game: `./qp drill mm`

Run `./qp drill mm` (add `--seed N` to replay a game; `./qp serve` has it in the browser).
The rules, from `tools/qp/drills.py`:

- Four hidden six-sided dice; you quote the final sum.
  There are four rounds, and one die is revealed after each quote.
- Each round you quote an integer bid and ask with width (ask minus bid) from 1 to 4.
- One counterparty arrives per round.
  With probability 1/2 it is informed and knows the total: it buys at your ask if the total is above it, sells at your bid if the total is below it, and otherwise passes.
  Otherwise it is a noise trader that buys, sells or passes with probability 1/3 each.
- Every trade is 10 lots, and the position settles at the true sum.
- The summary splits P&L into edge at fill (trade price versus the dice-only fair value at the time) and the remainder, adverse selection plus inventory.

Per lot and per round, with fair value $v$, quote $(b, a)$ and informed share $\pi = 1/2$, the expected P&L is

$$
(1 - \pi)\,\frac{a - b}{3} \;-\; \pi\left(\mathbb{E}[(T - a)^+] + \mathbb{E}[(b - T)^+]\right).
$$

The noise edge $(a - b)/3$ does not depend on where you centre the market, but the informed loss does, and it is smallest when the market is centred on the distribution of $T$.

## Worked examples

### Example 1: the opening market in the drill

Nothing is revealed: $\mathbb{E}[T] = 14$, $\operatorname{Var}(T) = 4 \times 35/12 = 35/3$, standard deviation about 3.42.
Expected P&L of each candidate first-round quote, per 10 lots, computed exactly over the 1,296 dice outcomes:

| Quote | Width | EV (10 lots) |
| :--- | ---: | ---: |
| 12 / 16 | 4 | +0.74 |
| 13 / 16 | 3 | -2.60 |
| 13 / 15 | 2 | -5.95 |
| 14 / 15 | 1 | -9.83 |

For 12 / 16: noise edge per lot is $4/3$, informed loss per lot is $\mathbb{E}[(T-16)^+] + \mathbb{E}[(12-T)^+] \approx 1.185$, so EV per lot is $\frac12(1.333) - \frac12(1.185) \approx 0.074$.
Every narrower quote loses money, and so do off-centre width-4 quotes (13 / 17 and 11 / 15 each earn about +0.26).
The best opening is 12 at 16.

### Example 2: later rounds

The best quotes as dice are revealed (dice 6, then 2, then 5):

| Revealed | Fair value | Best quote | EV (10 lots) |
| :--- | ---: | :--- | ---: |
| none | 14 | 12 / 16 | +0.74 |
| 6 | 16.5 | 15 / 19 or 14 / 18 | +2.13 |
| 6, 2 | 15 | 13 / 17 | +3.89 |
| 6, 2, 5 | 16.5 | 15 / 19 or 14 / 18 | +5.83 |

The best width is the maximum, 4, in every round: noise traders here trade regardless of width, so widening gains noise edge and loses less to informed traders at the same time.
The edge rises as uncertainty falls because the informed counterparty's advantage shrinks.
With a half-integer fair value, the two width-4 markets straddling it are equally good.
In the last round, width 3 at 15 / 18 earns +3.33 and width 2 at 16 / 18 earns exactly 0.

### Example 3: updating on being lifted

In round 1 you quote 12 / 16 and are lifted (you sell 10 at 16).
An informed trader lifts only if $T \ge 17$, which has probability $155/648 \approx 0.239$; a noise trader lifts with probability 1/3.
So $P(\text{informed} \mid \text{lift}) = \frac{0.5 \times 0.239}{0.5 \times 0.239 + 0.5 \times 0.333} \approx 0.42$.
Weighting each total by its likelihood of producing a lift gives $\mathbb{E}[T \mid \text{lift}] \approx 15.87$, almost 1.9 above the prior of 14.
If the first die then shows 3, the dice-only fair value is 13.5, but conditioning on the lift as well gives about 14.97.
Centre the round-2 market near 15, not 13.5: the drill's summary measures edge against the dice-only value, so it will not credit you for this, but the final P&L will.
A pass is informative too: it makes totals inside your market more likely.

### Example 4: a verbal game with position risk

"Make me a market on the maximum of two dice."
$\mathbb{E}[\max] = \sum_k k\,\frac{2k-1}{36} = 161/36 \approx 4.47$, and $P(\max = 6) = 11/36$.
Quote 4 at 5.
The interviewer buys at 5 repeatedly: each lift is evidence of a 6, so raise your market (for example to 5 at 6) rather than keep selling at 5.
If you end short 20 lots with one die still to be revealed in a dice-sum game, your P&L standard deviation from that die alone is $20 \times \sqrt{35/12} \approx 34.2$; say so, and cut size before you add to the position.

```python
from itertools import product
from fractions import Fraction

def round_ev(bid, ask, known, n=4, p_informed=Fraction(1, 2)):
    """Exact expected P&L per lot of one qp-drill round (dice-only information)."""
    u = n - len(known)
    outcomes = [sum(known) + sum(r) for r in product(range(1, 7), repeat=u)]
    p = Fraction(1, len(outcomes))
    informed_loss = sum(p * (max(t - ask, 0) + max(bid - t, 0)) for t in outcomes)
    return (1 - p_informed) * Fraction(ask - bid, 3) - p_informed * informed_loss

print(float(10 * round_ev(12, 16, [])))  # 0.74
```

## Pitfalls

- Quoting before computing the expectation, or anchoring on the first number that comes to mind.
- Ignoring the information in the counterparty's trades and passes.
- Quoting too tight against someone who knows the answer; with half the flow informed, a width-1 market loses in every round of the drill.
- Skewing away from fair value in a game where counterparties do not respond to price, which gives away edge.
- Letting the position grow without stating the worst case.
- Going silent: interviewers need to hear fair value, uncertainty and the reason for each change.
- Changing the market wildly after one trade; the update should be proportional to how informative that trade is.

## Interview questions

> [!question]- mm-game-four-dice-moments | What are the mean and standard deviation of the sum of four fair dice?
> Mean 14, standard deviation about 3.42.
> Each die has mean 3.5 and variance 35/12, so the sum has variance $35/3$.

> [!question]- mm-game-opening-quote | In qp drill mm, what is the best opening market and its expected P&L per 10 lots?
> 12 at 16, about +0.74.
> Noise edge per lot is $4/3$ and the informed loss per lot is about 1.185; each is weighted by 1/2.

> [!question]- mm-game-max-width-optimal | Why is the maximum width best in every round of qp drill mm?
> Because noise traders trade with the same probability whatever your width, widening raises the noise edge $(a-b)/3$ and also shrinks the informed loss, so nothing is given up.
> In real markets uninformed flow falls as you widen, which creates an interior optimum; exact enumeration confirms narrower quotes lose money in round 1 and earn less in every later round of the drill.

> [!question]- mm-game-noise-edge-centre | In qp drill mm, why does the centre of your quote not affect expected edge from noise traders?
> A noise trader buys or sells with probability 1/3 each regardless of price, so its expected edge is $\frac13(a - v) + \frac13(v - b) = (a - b)/3$.
> Only the informed loss depends on the centre, which is why you centre on your best estimate.

> [!question]- mm-game-lift-update | Round 1, you quote 12 at 16 and are lifted. What is your new fair value?
> About 15.87, up from 14.
> Totals of 17 or more produce a lift with probability $\frac12 + \frac16$, other totals with $\frac16$; reweighting the prior by these likelihoods gives 15.87.

> [!question]- mm-game-informed-posterior | Same lift at 16: what is the probability the counterparty was informed?
> About 0.42.
> $\frac{0.5 \times 155/648}{0.5 \times 155/648 + 0.5 \times 1/3}$.

> [!question]- mm-game-pass-is-information | The counterparty passes on your market. Does that tell you anything?
> Yes: an informed trader passes only when the value is inside your market, so a pass raises the probability of central values.
> Your fair value moves toward your mid and your uncertainty falls.

> [!question]- mm-game-max-two-dice | Make a market on the maximum of two dice. What is fair?
> About 4.47, so 4 at 5 is a sensible market.
> $\mathbb{E}[\max] = \sum_k k(2k-1)/36 = 161/36$.

> [!question]- mm-game-width-principle | What two things does your width protect you from in a trading game?
> Uncertainty about the value and the chance that your counterparty knows it.
> Widen as either rises and tighten as information reduces both.

> [!question]- mm-game-position-risk | You are short 20 lots with one die left in a dice-sum game. What is your risk?
> P&L standard deviation about 34 from that die: $20 \times \sqrt{35/12} \approx 34.2$.
> State it, then reduce size or skew if counterparties respond to price.

> [!question]- mm-game-skew-when-price-insensitive | Should you skew away from fair value to reduce a short position in qp drill mm?
> No: noise traders ignore price, so skewing does not change their flow, and moving the centre off fair value only increases the informed loss.
> Control risk with size in such a game; skew works in real markets because counterparties respond to price.

> [!question]- mm-game-narration | How should you phrase a market in an interview?
> State fair value, uncertainty, market and size together, for example "fair 14, sd about 3.4, 12 at 16, ten up".
> After each trade or reveal, say how fair value moved and why before giving the new market.

## In this repo and SDE-Interview-Prep

- Practice: `./qp drill mm`, implemented in `tools/qp/drills.py` (`MarketMakingGame`).
- Interview mechanics: [Trading Games in Interviews](../13-Interview-Playbook/05-Trading-Games-in-Interviews.md).
- Theory behind the width: [Market Making Fundamentals](01-Market-Making-Fundamentals.md) and [Spread Models: Roll and Glosten-Milgrom](../07-Market-Microstructure/03-Spread-Models-Roll-and-Glosten-Milgrom.md).

## Further reading

- Agustin Lebron, *The Laws of Trading* (2019).
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews* (2008).
- Glosten and Milgrom (1985), Bid, ask and transaction prices in a specialist market with heterogeneously informed traders, *Journal of Financial Economics* 14(1).
