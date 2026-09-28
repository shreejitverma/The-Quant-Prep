---
type: concept
track: [quant-trader]
tier: core
status: solid
prereqs: [market-making-games]
est_hours: 3
sources: [Agustin Lebron - The Laws of Trading (2019), Xinfeng Zhou - A Practical Guide to Quantitative Finance Interviews (2008), J. L. Kelly Jr. - A New Interpretation of Information Rate (Bell System Technical Journal 1956)]
---

# Trading Games in Interviews

## TL;DR

- Formats you should expect: make-a-market on an uncertain number, card and dice games with information revealed over time, auctions, and sequential betting.
- Keep a written ledger every round: fair value, your quote, each fill, position, cash, and mark-to-fair P&L.
- Fair value is the conditional expectation given everything revealed, including what the counterparty's trades tell you.
- Quote around fair value, widen when the counterparty may be informed, and skew both sides away from your inventory.
- P&L splits into edge captured at the fill and the mark-to-market of inventory afterwards; interviewers watch the first and your control of the second.

## Learning objectives

- Know the common formats: make-a-market, card and dice games, auction games, sequential betting.
- Keep a running position, P&L and fair value while talking.

## Core concepts

### Why firms run trading games

Market-making firms commonly include a game in trader interviews because it tests, at once, expectation under uncertainty, fast arithmetic, risk control and communication.
Formats and scoring vary by firm and change over time; see the firm guides in [14-Firms](../14-Firms/README.md) for what has been reported, and treat those reports as anecdotes.
The theory behind quoting, width and skew is in [Market Making Games and Trading Simulations](../08-Market-Making/10-Market-Making-Games.md); this note is the interview-room checklist.

### The formats

**Make a market.**
"Make me a market on X": you quote a bid and an ask (and sometimes size); the interviewer may buy at your ask, sell at your bid, or ask you to tighten.
X may be a dice total, a card sum, or a Fermi quantity (see [Estimation and Fermi Problems](04-Estimation-and-Fermi-Problems.md)).

**Card and dice games.**
A random quantity is revealed piece by piece (one die per round, one card per round); you re-quote after each reveal.
Fair value is known cards plus the expected value of the unknown ones, with draws without replacement conditioned on what has been seen.

**Auctions.**
Sealed-bid or open auctions on an item of uncertain value.
The key idea is the winner's curse: conditional on winning, your estimate was probably too high, so shade your bid.
In a second-price (Vickrey) auction with private values, bidding your true value is a dominant strategy.

**Sequential betting.**
You are offered a series of favourable bets and choose stakes, or you choose when to stop.
Sizing is Kelly-like: bet a fraction of wealth that maximises expected log growth; stopping problems are solved by backward induction.

### Fair value

- Fair value is $E[X \mid \text{information}]$.
  For $n$ fair dice with $k$ revealed summing to $s$: $s + 3.5(n-k)$.
- Without replacement, the unseen cards shift the mean of the rest: after seeing a King in a 52-card deck with $A=1$ to $K=13$, each remaining card averages $(364-13)/51$.
- The counterparty's actions are information: being lifted repeatedly means your ask is probably too low.
  How much to move depends on how informed the counterparty is likely to be; in `./qp drill mm` half the counterparties know the answer.

### Width and skew

- Width compensates for adverse selection: the more likely the counterparty is informed and the larger your uncertainty, the wider.
- Skew moves both bid and ask in the same direction to shed inventory: when long, lower both so you are more likely to sell; when short, raise both.
- Size: quote smaller when uncertain or when position is already large; many games let you state size explicitly.

### The ledger

Write a row per round, and say it out loud when you update it:

| Round | Info | Fair value | Quote | Fill | Position | Cash | Mark P&L |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

Mark P&L is $\text{cash} + \text{position} \times \text{fair value}$.
Total P&L decomposes as
$$
\text{P\&L} = \underbrace{\sum_{\text{fills}} \pm(\text{price} - \text{FV at fill}) \times q}_{\text{edge}} + \underbrace{\sum_{\text{rounds}} \text{position} \times \Delta \text{FV}}_{\text{inventory}},
$$
with the sign positive for sells and negative for buys in the first term.
The drill `./qp drill mm` reports exactly this split.

### Practising with `./qp drill mm`

The drill hides 4 dice, you quote the final sum with integer bid and ask and a width between 1 and 4, and one die is revealed after each round.
Each round one counterparty arrives: with probability $1/2$ it knows the total and trades against you if your quote is wrong, otherwise it buys, sells or passes at random; each fill is 10 contracts.
Score yourself on edge at fill and on the inventory term, not just total P&L, which is noisy over one game.

## Worked examples

### Example 1: a full three-dice game with a ledger

You make markets on the sum of 3 dice, 1 unit per trade, and one die is revealed after each round.

- Round 0: FV $= 10.5$, standard deviation $\sqrt{3 \times 35/12} \approx 2.96$.
  Quote $9.5$ at $11.5$.
  The interviewer buys 1 at $11.5$: position $-1$, cash $+11.5$, edge $+1$.
- Die 1 is a 5: FV $= 5 + 7 = 12$.
  Mark P&L $= 11.5 - 12 = -0.5$.
  You are short, so skew up: quote $11.5$ at $13.5$ around $12.5$.
  The interviewer sells 2 at $11.5$: position $+1$, cash $11.5 - 23 = -11.5$, edge $2 \times 0.5 = +1$.
- Die 2 is a 2: FV $= 7 + 3.5 = 10.5$.
  Mark P&L $= -11.5 + 10.5 = -1$.
  Long 1, so skew down: quote $9$ at $11$.
  No trade.
- Die 3 is a 6: total 13.
  Final P&L $= -11.5 + 13 = +1.5$.

Decomposition: edge $+2$, inventory $-1.5$ (short through a $+1.5$ move) $-1.5$ (long through a $-1.5$ move) $+2.5$ (long through a $+2.5$ move) $= -0.5$; total $+1.5$.
Say the decomposition aloud at the end: it shows you know which part was skill.

### Example 2: ten cards from a deck

"Make a market on the sum of 10 cards drawn without replacement, $A=1$ to $K=13$."
The deck sums to $4 \times 91 = 364$, so each card averages $7$ and FV $= 70$.
The standard deviation with the finite-population correction is $\sqrt{10 \times 14 \times 42/51} \approx 10.7$.
A starting market of $66$ at $74$ is reasonable.
The first card is a King: FV $= 13 + 9 \times 351/51 = 1274/17 \approx 74.94$, not $13 + 63 = 76$, because the remaining deck is now slightly weaker.

### Example 3: the acquirer's auction (winner's curse)

A company is worth $V \sim U(0,100)$ to its owner and $1.5V$ to you; the owner accepts any bid $b \ge V$; you bid once without knowing $V$.
If accepted, $V$ is uniform on $[0, b]$, so $E[V \mid \text{accept}] = b/2$ and your value is $0.75 b$.
Expected profit $= (b/100)(0.75 b - b) = -b^2/400 < 0$ for every $b > 0$.
Bid 0.
The naive answer ($1.5 \times 50 = 75$, so bid up to 75) ignores that acceptance is informative.

### Example 4: sequential betting and stopping

"You roll a die and may take the face value in dollars or re-roll, up to three rolls in total."
With one roll left the value is $3.5$.
With two, keep a first roll of 4 or more: value $(4+5+6)/6 + (3/6)(3.5) = 4.25$.
With three, keep 5 or 6: value $(5+6)/6 + (4/6)(4.25) = 14/3 \approx 4.67$.
"Now you are offered a coin that lands heads $60\%$ of the time at even odds, repeatedly."
Kelly stake $f^* = p - q = 0.2$ of wealth, with expected log growth $0.6 \ln 1.2 + 0.4 \ln 0.8 \approx 0.0201$ per bet.

## Pitfalls

- Losing track of position or cash; write every fill, and state position before each new quote.
- Quoting a market centred on the unconditional mean after information has been revealed.
- Keeping the same quote after being lifted or hit repeatedly; that is the textbook way to be run over by an informed counterparty.
- Skewing the wrong way (raising the bid when already long).
- Refusing to trade, or quoting absurdly wide; a market that never trades earns nothing and signals fear.
- Chasing total P&L in a short game where luck dominates, instead of making positive-edge decisions and explaining them.
- Ignoring the winner's curse in common-value auctions.

## Interview questions

> [!question]- int-tg-three-dice-fair-value | Make a market on the sum of three dice. What is the fair value and standard deviation?
> $10.5$ and about $2.96$. Each die has mean $3.5$ and variance $35/12$, so the sum has variance $35/4$.

> [!question]- int-tg-three-dice-after-reveal | Three dice; the first is revealed as a 5. New fair value?
> $12$. $5 + 2 \times 3.5$.

> [!question]- int-tg-ten-cards-fair-value | Fair value of the sum of 10 cards drawn without replacement from a deck with $A=1$ to $K=13$?
> $70$. The deck sums to $364$ over 52 cards, an average of 7, and linearity of expectation holds without replacement.

> [!question]- int-tg-ten-cards-after-king | In the 10-card game, the first card is a King. New fair value?
> $1274/17 \approx 74.94$. The other 9 cards average $(364 - 13)/51 = 351/51$ each, so $13 + 9 \times 351/51$.

> [!question]- int-tg-skew-when-long | You are long and want to reduce the position. How do you change your quote?
> Lower both bid and ask by the same amount. The lower ask makes a buyer more likely to lift you, and the lower bid makes it less likely you buy more.

> [!question]- int-tg-lifted-twice | Your offer has been lifted twice in a row on an uncertain quantity. What does it tell you and what do you do?
> Your ask is probably below the value the counterparty believes, and they may be informed. Raise fair value, widen, and reduce size until you learn more.

> [!question]- int-tg-acquirer-auction | A company is worth $V \sim U(0,100)$ to the owner, who accepts any bid $\ge V$, and $1.5V$ to you. What should you bid?
> 0. If a bid $b$ is accepted, $E[V] = b/2$, so you gain $0.75b - b < 0$; expected profit is $-b^2/400$.

> [!question]- int-tg-vickrey-bid | In a sealed-bid second-price auction with private values, what should you bid?
> Your true value. Bidding more only adds wins at prices above your value; bidding less only loses auctions you would have won at a price below your value.

> [!question]- int-tg-kelly-sixty-forty | Repeated even-money bets on a coin with $P(\text{heads}) = 0.6$. What fraction of wealth should you bet?
> $20\%$. Kelly for even odds is $f^* = p - q = 0.6 - 0.4$, maximising $p \ln(1+f) + q \ln(1-f)$.

> [!question]- int-tg-dice-reroll-two | Roll a die and take the face in dollars, or re-roll once and take the second roll. Value and strategy?
> $4.25$. Keep 4, 5 or 6 (worth more than the $3.5$ from re-rolling): $(4+5+6)/6 + (1/2)(3.5) = 4.25$.

> [!question]- int-tg-dice-reroll-three | Same game, but up to three rolls. Value?
> $14/3 \approx 4.67$. Keep a first roll of 5 or 6, since the two-roll continuation is worth $4.25$: $(5+6)/6 + (4/6)(4.25)$.

> [!question]- int-tg-red-card-stopping | Cards are turned over one at a time from a shuffled deck; at any point you may say "next is red" and win if it is. Best win probability?
> $1/2$. The fraction of red cards remaining is a martingale, so every stopping rule has the same expected value as stopping at once.

> [!question]- int-tg-ledger-pnl | You buy 10 at 10, sell 5 at 11, buy 5 at 12, sell 20 at 10.5. The asset settles at 12. Position and P&L?
> Short 10, P&L $-15$. Cash is $-100 + 55 - 60 + 210 = +105$, position $10 - 5 + 5 - 20 = -10$, and $105 - 10 \times 12 = -15$.

> [!question]- int-tg-pnl-decomposition | How do you split a market-making game P&L into skill and luck?
> Edge at fill ($\pm$ price minus fair value at the time, times size) plus inventory P&L (position times each fair-value change). The first reflects quoting; the second is mostly the risk you chose to hold.

## In this repo and SDE-Interview-Prep

- `tools/qp/drills.py` implements `MarketMakingGame`, the engine behind `./qp drill mm`, including the edge and inventory split.

## Further reading

- Agustin Lebron, *The Laws of Trading* (2019), on adverse selection, edge and risk.
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews* (2008), for dice and card expectation problems.
- J. L. Kelly Jr., "A New Interpretation of Information Rate", *Bell System Technical Journal* (1956).
- [Market Making Games and Trading Simulations](../08-Market-Making/10-Market-Making-Games.md) and [Market Making Fundamentals](../08-Market-Making/01-Market-Making-Fundamentals.md).
