---
type: concept
track: [quant-trader]
tier: core
status: solid
prereqs: [kelly-criterion-and-position-sizing]
est_hours: 3
sources: [Lebron (2019) The Laws of Trading. Wiley, Zhou (2008) A Practical Guide to Quantitative Finance Interviews, Feller (1968) An Introduction to Probability Theory and Its Applications Vol 1 3rd ed. Wiley (gambler's ruin), Thorp (2006) The Kelly criterion in blackjack sports betting and the stock market. Handbook of Asset and Liability Management Vol 1]
---

# Expected Value and Betting Decisions

## TL;DR

- First question for any bet: what is the expected value per unit risked, and against whom are you betting (if they offered it, why)?
- Second question: how big is the variance relative to your bankroll; a positive-EV bet sized too large can still ruin you, and the long-run growth rate of a small bet is about $\text{edge}^2/(2\,\text{variance})$.
- Risk of ruin with a fixed bet size and edge $\mu$, standard deviation $\sigma$ per bet and a bankroll of $B$ is about $e^{-2\mu B/\sigma^2}$; with a 51% even-money bet and 50 units it is 13.5%.
- Sequential games are solved by backward induction: continue while the value of continuing exceeds the value of stopping, and write down the recursion before guessing.
- Fair games stay fair under any bounded stopping rule (optional stopping), so edge comes from the odds, never from when you quit.

## Learning objectives

- Decide quickly whether a bet has edge and how much to wager.
- Balance edge against variance and risk of ruin.
- Play sequential betting games optimally.

## Core concepts

### Edge first

The expected value of a bet is $\sum_i p_i x_i$; its edge is EV divided by the amount at risk.
Compute it with linearity and indicator variables (see [Expectation, Variance and Linearity](../01-Probability/04-Expectation-Variance-and-Linearity.md)) and say it out loud before anything else.
Then ask why the bet exists.
If a counterparty offers you a bet, their willingness is information: in a market, the price you can trade at is conditioned on someone else choosing to trade with you (adverse selection, see [Market Making Games](../08-Market-Making/10-Market-Making-Games.md)).
Lebron frames this as knowing why you are doing a trade; the interview version is "what does the other side know that I do not?"

### Edge versus variance

Two bets with the same EV are not equally good.
For a bet of fixed size with mean $\mu$ and standard deviation $\sigma$, three numbers matter:

- The per-bet Sharpe ratio $\mu/\sigma$: after $n$ independent bets, the probability of being ahead is about $\Phi(\sqrt{n}\,\mu/\sigma)$.
- The growth rate when optimally sized: $g^* \approx \mu^2/(2\sigma^2)$ per bet (see [Kelly Criterion and Position Sizing](01-Kelly-Criterion-and-Position-Sizing.md)), so what compounds is squared Sharpe, not EV.
- The bankroll needed for an acceptable risk of ruin, which scales as $\sigma^2/\mu$.

### Risk of ruin

Bet one unit at a time on a game that wins with probability $p > 1/2$, starting with $B$ units against an opponent with unlimited capital.
The classic gambler's-ruin result (see [Random Walks and Gambler's Ruin](../01-Probability/11-Random-Walks-and-Gamblers-Ruin.md)) is

$$
P(\text{ruin}) = \left(\frac{q}{p}\right)^{B}.
$$

For general bets with mean $\mu$ and variance $\sigma^2$ per unit, the Brownian approximation gives

$$
P(\text{ruin}) \approx \exp\!\left(-\frac{2\mu B}{\sigma^2}\right), \qquad B_{\text{needed}} = \frac{\sigma^2}{2\mu}\ln\frac{1}{P_{\text{target}}}.
$$

Ruin probability falls exponentially in bankroll measured in units of $\sigma^2/\mu$.
Doubling the edge halves the bankroll you need; doubling the volatility quadruples it.
Betting a constant fraction of wealth (Kelly or a fraction of it) makes literal ruin impossible, but drawdowns remain; the constant-size case is how most real risk limits behave.

### Utility, bankroll and when to refuse a positive-EV bet

EV is the right criterion only when the bet is small relative to wealth.
For large bets, compare certainty equivalents under a concave utility such as log.
A risk-neutral trading desk is a good approximation when each position is small relative to firm capital, which is why market makers take many small positive-EV bets and decline large ones.
Saying "the EV is positive but I would size it down because it is a large fraction of my bankroll" is a better interview answer than accepting or refusing outright.

### Sequential games and backward induction

Most trader-interview betting games are optimal stopping problems.
Define the value $V(s)$ of each state as the larger of the stop payoff and the expected value of continuing, and solve from the end backwards:

$$
V(s) = \max\Big(\text{stop}(s),\; \mathbb{E}[V(s') \mid s]\Big).
$$

A one-step comparison (stop if the expected gain from one more step is negative) is optimal when the problem is monotone: once stopping is right, it stays right.
Options to continue have value: a reroll is a free option on a better outcome, so the value with $k$ rerolls rises with $k$.
If every step is a fair bet, the running total is a martingale and no bounded stopping rule changes its expectation ([Martingales and Optional Stopping](../01-Probability/12-Martingales-and-Optional-Stopping.md)); doubling strategies need unbounded capital to "work".

### Replication in betting

When you can bet only on intermediate events, work backwards from the payoff you want, exactly like delta hedging in a binomial tree.
The stake at each node is half the difference between the target values in the two successor states.

## Worked examples

### Example 1: a die with rerolls

"Roll a die and receive its face value in dollars. You may reroll up to twice, keeping only the last roll. What is the game worth?"
With no rerolls, 3.5.
With one reroll left, keep a first roll only if it beats 3.5, so keep 4, 5, 6: $V_1 = \frac{3.5 \times 3 + 4 + 5 + 6}{6} = 4.25$.
With two rerolls left, keep a roll only if it beats 4.25, so keep 5 and 6: $V_2 = \frac{4.25 \times 4 + 5 + 6}{6} = 14/3 \approx 4.67$.
The threshold is always the value of continuing; say that sentence and the recursion writes itself.

### Example 2: accumulate or lose everything

"Roll a die repeatedly. Each roll of 2 to 6 adds its face value to your total; a 1 wipes the total to zero and ends the game. You may stop at any time. When do you stop?"
With current total $S$, one more roll changes the expected total by $\frac56 \times 4 - \frac16 S = \frac{20 - S}{6}$.
Keep rolling while $S < 20$ and stop at 20 or more (at exactly 20 you are indifferent).
The problem is monotone (the total only grows until a wipe), so the one-step rule is optimal.

### Example 3: risk of ruin on a small edge

"You bet one unit at a time at even money with a 51% win probability, starting with 50 units. What is the chance you ever go broke?"
Exact: $(0.49/0.51)^{50} \approx 0.135$.
Diffusion: $\mu = 0.02$, $\sigma^2 \approx 1$, $e^{-2 \times 0.02 \times 50} = e^{-2} \approx 0.135$.
For a 1% ruin probability you need $B = \frac{\ln 100}{2 \times 0.02} \approx 115$ units.
And to be 95% sure of being ahead you need $n$ with $0.02\sqrt{n} = 1.645$, about 6,800 bets: a 2% edge is real money but slow to show.

### Example 4: which bet would you rather have?

Bet A has mean +1 and standard deviation 10; bet B has mean +0.5 and standard deviation 2, both per play, and you can scale either.
A has per-bet Sharpe 0.1 and optimal growth $1/(2 \times 100) = 0.005$ per play.
B has per-bet Sharpe 0.25 and optimal growth $0.25/(2 \times 4) \approx 0.031$ per play, over six times A's.
Prefer B unless you are capped in size and A cannot be scaled down, and even then only if your bankroll is large relative to $\sigma_A^2/\mu_A = 100$.

### Example 5: betting on a series with game-by-game bets

"You want to bet 100 at even money that team A wins a best-of-seven series, but the bookmaker only takes even-money bets on single games. How much do you bet on game 1?"
Target payoff: +100 if A wins the series, -100 otherwise.
Before game 1 the payoff is 0 in expectation under fair 50-50 games, and after a win the target value is $100 \times (2P(\text{A wins series} \mid 1\text{-}0) - 1)$.
From 1-0, A wins the series with probability $P(\text{at least 3 wins in the next 6}) = 42/64$, so the value is $100 \times (84 - 64)/64 = 31.25$.
By symmetry the value after a loss is $-31.25$, so bet 31.25 on game 1: equivalently $100 \binom{6}{3}/2^6$.
Each later stake is found the same way at every node of the tree.

### Example 6: stop any time in a red-black deck

"A shuffled deck has 26 red and 26 black cards. Turn them one by one; each red pays +1 and each black costs -1. You may stop at any time. What is the game worth?"
The state is (reds left, blacks left); with $r$ reds and $b$ blacks,

$$
V(r, b) = \max\!\Big(0,\; \tfrac{r}{r+b}\big(1 + V(r-1, b)\big) + \tfrac{b}{r+b}\big(-1 + V(r, b-1)\big)\Big),
$$

with $V(0, b) = 0$ and $V(r, 0) = r$.
$V(1,1) = 1/2$, $V(2,2) = 2/3$, and $V(26,26) \approx 2.62$.
Contrast the related game "stop at any time and bet that the next card is red": that one is worth exactly its starting fair value, because the fraction of reds remaining is a martingale.

```python
from fractions import Fraction
from functools import lru_cache

@lru_cache(None)
def value(r, b):
    if r == 0:
        return Fraction(0)
    if b == 0:
        return Fraction(r)
    go = Fraction(r, r + b) * (1 + value(r - 1, b)) + Fraction(b, r + b) * (-1 + value(r, b - 1))
    return max(Fraction(0), go)

print(float(value(26, 26)))  # 2.6245
```

### Example 7: a million on a coin or 400,000 for sure

With wealth 100,000 and log utility, the gamble's certainty equivalent is $\sqrt{1{,}100{,}000 \times 100{,}000} - 100{,}000 \approx 231{,}700$, so take the 400,000.
With wealth 10,000,000 the certainty equivalent is about 488,100, close to the EV of 500,000, so take the gamble.
Same bet, opposite answers: size relative to bankroll decides.

## Pitfalls

- Answering "is it positive EV" without asking why the other side offers the bet.
- Ranking bets by EV alone instead of EV per unit of variance.
- Ignoring bankroll: a positive-EV bet that risks a large fraction of capital can have negative log utility.
- Guessing stopping thresholds instead of setting up $V(s) = \max(\text{stop}, \text{continue})$.
- Using a one-step rule in a non-monotone problem, where stopping now can be wrong even when the next step looks bad.
- Believing a stopping rule or a doubling scheme can turn a fair game into a winning one.
- Forgetting that the number of bets needed to show a small edge grows as $(\sigma/\mu)^2$.

## Interview questions

> [!question]- risk-ev-reroll-die | You roll a die and get its face value, with up to two rerolls keeping the last roll. What is the game worth?
> $14/3 \approx 4.67$.
> With one reroll keep 4 or more ($V_1 = 4.25$); with two, keep only 5 or 6: $(4.25 \times 4 + 11)/6 = 14/3$.

> [!question]- risk-ev-pig-threshold | You accumulate die faces 2 to 6 but a 1 wipes your total. At what total do you stop?
> Stop at 20 or more.
> The expected change from one more roll is $\frac56 \cdot 4 - \frac16 S = (20 - S)/6$.

> [!question]- risk-ev-ruin-51 | Even-money bets of one unit, win probability 0.51, bankroll 50 units. What is the probability of ruin?
> About 13.5%.
> $(0.49/0.51)^{50} \approx 0.135$, matching the diffusion approximation $e^{-2\mu B/\sigma^2} = e^{-2}$.

> [!question]- risk-ev-ruin-scaling | How does the bankroll needed for a given ruin probability scale with edge and volatility?
> As $\sigma^2/\mu$: double the edge and you need half the bankroll, double the volatility and you need four times as much.
> From $P(\text{ruin}) \approx \exp(-2\mu B/\sigma^2)$.

> [!question]- risk-ev-edge-vs-variance | Bet A has mean 1 and sd 10; bet B has mean 0.5 and sd 2, both scalable. Which do you prefer?
> B.
> Optimal growth is about $\mu^2/(2\sigma^2)$: 0.005 per play for A and 0.031 for B; B also has the higher per-bet Sharpe (0.25 against 0.1).

> [!question]- risk-ev-series-replication | You want +100 or -100 on a best-of-seven series but can only bet even money per game. What is your first bet?
> 31.25.
> After a game-1 win the series is worth $100(2 \times 42/64 - 1) = 31.25$ to you and after a loss $-31.25$; equivalently $100\binom63/2^6$.

> [!question]- risk-ev-red-black-stop | 26 red cards pay +1 and 26 black cost -1, turned one at a time; you may stop any time. Is the game worth more than zero?
> Yes, about 2.62.
> Playing to the end guarantees 0, and stopping whenever you are ahead does strictly better; backward induction on (reds, blacks) gives 2.6245.

> [!question]- risk-ev-next-card-red | You may stop at any time and bet at even money that the next card is red. Is there a strategy with positive EV in a full deck?
> No; every strategy wins with probability exactly 1/2.
> The proportion of reds remaining is a martingale, so by optional stopping its value at your stopping time has expectation 1/2.

> [!question]- risk-ev-bankroll-utility | Would you take a coin flip for 1,000,000 or nothing over 400,000 for sure?
> It depends on wealth: with 100,000 and log utility take the 400,000 (the gamble's certainty equivalent is about 232,000); with 10,000,000 take the gamble.
> EV is the right criterion only when the bet is small relative to your bankroll.

> [!question]- risk-ev-doubling | Can doubling after every loss beat a fair even-money game?
> No: with finite capital or a finite horizon the expected profit is exactly zero.
> The strategy wins a small amount with high probability and loses the whole stake with small probability; optional stopping forbids positive EV under bounded stopping.

> [!question]- risk-ev-bets-to-show-edge | How many even-money bets with a 2% edge do you need to be 95% sure of being ahead?
> About 6,800.
> Need $0.02\sqrt{n} \ge 1.645$, so $n \ge (1.645/0.02)^2 \approx 6{,}765$.

> [!question]- risk-ev-who-offers | Someone offers you a bet that looks positive EV. What do you ask first?
> Why they are offering it: what they know, and whether the price already reflects information you lack.
> Condition on the offer itself; a bet chosen by an informed counterparty is adversely selected.

## Further reading

- Agustin Lebron, *The Laws of Trading* (2019).
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews* (2008), the chapters on probability games and dynamic programming.
- William Feller, *An Introduction to Probability Theory and Its Applications*, Vol 1, on gambler's ruin.
- Edward Thorp (2006), The Kelly criterion in blackjack, sports betting and the stock market.
