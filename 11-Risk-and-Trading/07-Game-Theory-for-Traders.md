---
type: concept
track: [quant-trader]
tier: advanced
status: solid
prereqs: [expected-value-and-betting-decisions]
est_hours: 3
sources: [Dixit and Nalebuff - Thinking Strategically (Norton 1991), Osborne and Rubinstein - A Course in Game Theory (MIT Press 1994) chapters 2 3 6 7 and 8, Krishna - Auction Theory (Academic Press 2nd edition 2010) chapters 2 and 6, Vickrey (1961) Counterspeculation auctions and competitive sealed tenders. Journal of Finance 16(1), Myerson (1981) Optimal auction design. Mathematics of Operations Research 6(1), Rubinstein (1982) Perfect equilibrium in a bargaining model. Econometrica 50(1), Nash (1950) The bargaining problem. Econometrica 18(2), Samuelson and Bazerman (1985) The winner's curse in bilateral negotiations. Research in Experimental Economics 3, Capen Clapp and Campbell (1971) Competitive bidding in high-risk situations. Journal of Petroleum Technology 23(6), Nagel (1995) Unraveling in guessing games. American Economic Review 85(5)]
---

# Game Theory for Traders

## TL;DR

- A Nash equilibrium is a profile where no player gains by deviating alone; mixed equilibria are found by making the opponent indifferent, and support enumeration finds all of them in small games.
- Private-value auctions: second price is truthful; first price bids $\frac{n-1}{n}v$ with uniform values; both raise $\frac{n-1}{n+1}$ (revenue equivalence).
- Common-value auctions carry a winner's curse: winning means your estimate was the highest, so condition on it; with $n$ uniform errors on $[-a, a]$ the winner overpays by $a\frac{n-1}{n+1}$ if it bids its signal.
- Bargaining rewards patience (Rubinstein: proposer gets $\frac{1 - \delta_2}{1 - \delta_1\delta_2}$); repeated play sustains cooperation when the future matters enough (grim trigger needs $\delta \ge \frac{T - R}{T - P}$).
- In trading, the opponent is the other side of your fill: an RFQ win, a lift of your offer and a "free" bet are all information, and the right response is to price what the counterparty knows.

## Learning objectives

- Find Nash equilibria in simple games and auctions.
- Explain the winner's curse and adverse selection in auctions.
- Reason about bluffing and information in trading games.
- Use backward induction in bargaining, repeated games and interview puzzles.

## Core concepts

### Games, best responses and Nash equilibrium

A normal-form game lists players, strategies and payoffs.
A strategy is dominated if another does better against everything the opponent might do; iterated deletion of dominated strategies solves some games outright (the prisoner's dilemma, the beauty contest).
A Nash equilibrium is a strategy profile in which each strategy is a best response to the others.
Every finite game has one in mixed strategies (Nash's existence theorem).

Finding mixed equilibria: in equilibrium each player's mix makes the other indifferent among the strategies they play with positive probability.
For a 2x2 game with row payoffs $a_{ij}$, the column player's probability $y$ on column 1 solves $a_{11}y + a_{12}(1 - y) = a_{21}y + a_{22}(1 - y)$.
Support enumeration generalises this: for every pair of equal-size supports, solve the indifference equations, keep the solution if the probabilities are non-negative and no strategy outside the support does better.

| Game | Structure | Equilibria |
| :--- | :--- | :--- |
| Prisoner's dilemma | defect dominates | (defect, defect), worse for both than cooperating |
| Matching pennies | pure conflict | mixed 50/50, value 0 |
| Battle of the sexes | coordination with conflict | two pure, one mixed in which each plays its favourite with probability 2/3 |
| Hawk-dove | prize $V$, fight cost $C > V$ | two asymmetric pure, one symmetric mixed with $P(\text{hawk}) = V/C$ |
| Bertrand with a tick | two quoters undercut each other | prices pushed towards cost, but a tick size can support prices above it |

Zero-sum games have a value: the minimax theorem says the row player's best guaranteed payoff equals the column player's best guaranteed loss.

### Auctions with private values

$n$ bidders with independent private values drawn uniform on $[0, 1]$:

- Second-price (Vickrey) and English auctions: bidding your value is weakly dominant, because your bid only decides whether you win, never what you pay.
  Expected revenue is the expected second-highest value, $\frac{n-1}{n+1}$.
- First-price and Dutch auctions: you shade.
  Guess $b(v) = cv$; against opponents using it, bidding $b$ wins with probability $(b/c)^{n-1}$, and maximising $(v - b)(b/c)^{n-1}$ gives $b = \frac{n-1}{n}v$, so $c = \frac{n-1}{n}$.
  Expected revenue is $\frac{n-1}{n}\mathbb{E}[v_{(n)}] = \frac{n-1}{n}\cdot\frac{n}{n+1} = \frac{n-1}{n+1}$, the same.
- Revenue equivalence: any standard auction that gives the item to the highest value and leaves the lowest type zero surplus raises the same expected revenue under independent private values and risk neutrality.
- A seller can do better with a reserve price: Myerson (1981) shows the optimal reserve for regular value distributions solves $r = \frac{1 - F(r)}{f(r)}$, which is $\frac12$ for uniform values, regardless of $n$.

### Common values and the winner's curse

In a common-value auction the item is worth the same $V$ to everyone, and bidders hold noisy estimates $s_i = V + \varepsilon_i$.
Winning is news: it tells you every other estimate was below yours, so your estimate was probably too high.
With a diffuse prior and $\varepsilon_i$ uniform on $[-a, a]$,

$$
\mathbb{E}[V \mid s_i = s, \ s_i \text{ is the highest}] = s - \mathbb{E}[\varepsilon_{(n)}] = s - a\frac{n-1}{n+1},
$$

because the maximum of $n$ uniforms on $[-a, a]$ has mean $a\frac{n-1}{n+1}$.
More bidders mean a bigger correction: competition makes winning worse news.
Capen, Clapp and Campbell (1971) described the effect in oil-lease bidding; Samuelson and Bazerman (1985) showed it in the "acquire a company" bargaining experiment.

For traders:

- RFQ markets: when $n$ dealers price a bond with independent valuation errors, the dealer who wins is the one whose error was most in the client's favour; the expected size of that error is $\sigma\,\mathbb{E}[\max_n Z]$.
- Being lifted on your offer, or filled first on a new level, is the same conditioning; see [Adverse Selection and Flow Toxicity](../07-Market-Microstructure/05-Adverse-Selection-and-Flow-Toxicity.md) and [Spread Models: Roll and Glosten-Milgrom](../07-Market-Microstructure/03-Spread-Models-Roll-and-Glosten-Milgrom.md).
- IPO and block allocations: you get the most of the deals other investors want least.

### Bargaining

- Ultimatum game: with money divisible to one unit, the subgame-perfect equilibrium has the proposer offer the smallest unit and the responder accept; experiments show far more generous offers, because real responders reject unfair splits.
- Rubinstein (1982) alternating offers with discount factors $\delta_1$ (proposer) and $\delta_2$ (responder): the unique subgame-perfect split gives the first proposer $\frac{1 - \delta_2}{1 - \delta_1\delta_2}$, agreed immediately.
  Patience is bargaining power; so is the ability to make the first offer.
- Nash (1950) bargaining solution: maximise $(x_1 - d_1)(x_2 - d_2)$ over feasible splits; with a surplus $S$ to share and disagreement payoffs $d_1, d_2$ it gives player 1 $\frac{S + d_1 - d_2}{2}$.
  Outside options are what move the split.

### Repeated games and reputation

In the one-shot prisoner's dilemma (temptation $T$, reward $R$, punishment $P$, sucker $S$, with $T > R > P > S$) defection is dominant.
Repeated indefinitely with discount factor $\delta$, cooperation can be an equilibrium:

- Grim trigger (cooperate until the other defects, then defect forever): cooperating is worth $\frac{R}{1 - \delta}$ and deviating $T + \frac{\delta P}{1 - \delta}$, so cooperation holds iff $\delta \ge \frac{T - R}{T - P}$.
- Tit-for-tat against a one-period deviation (defect once, then return to cooperation): $R + \delta R \ge T + \delta S$, so $\delta \ge \frac{T - R}{R - S}$.
- Finite and known horizon: backward induction unravels cooperation from the last round.

Trading relationships are repeated games: a dealer who backs away from quotes, or a client who leaks RFQs, is punished by being shown worse prices or no prices.
That is why reputation, last-look policies and "who do we show this to" decisions are game-theoretic.

### Bluffing and information

In a simplified river poker decision with pot $P$ and bet $B$:

- The bettor's bluffs make the caller indifferent when bluffs are a share $\frac{B}{P + 2B}$ of the betting range: calling then wins $P + B$ against a bluff and loses $B$ against value, and those balance.
- The caller makes bluffs indifferent by calling with frequency $\frac{P}{P + B}$: a bluff then wins $P$ when called too rarely and loses $B$ when called.

Bigger bets need more value behind them and can be called less often.
In trading games the same logic says: if you never bluff, every aggressive action reveals your hand; an interviewer's quote request or a trade you are offered carries information about what the other side holds.

### Interview puzzles that are really games

- Guess two-thirds of the average (Keynes' beauty contest): iterated elimination drives the equilibrium to 0; Nagel (1995) found real players stop after one to three steps of reasoning, so the winning guess depends on the population, not the equilibrium.
- Pirate game: five ranked pirates split 100 coins, the most senior proposes, the plan passes with at least half the votes (proposer included), otherwise the proposer is thrown overboard; backward induction gives 98, 0, 1, 0, 1.
- Dollar auction and wars of attrition: sunk costs drive escalation; the right move is to recognise the game before entering.
- Market-making games are information games too; see [Market Making Games and Trading Simulations](../08-Market-Making/10-Market-Making-Games.md).

## Worked examples

All numbers are printed and asserted by [game_theory.py](code/game_theory.py); simulations use fixed seeds.

### Example 1: equilibria by indifference

"Battle of the sexes with payoffs (2, 1) and (1, 2) on the diagonal and 0 off it.
Two pure equilibria are obvious.
For the mixed one, the row player makes the column player indifferent: $1 \cdot x = 2(1 - x)$, so $x = 2/3$ on the row player's favourite; by symmetry the column player puts 2/3 on its own favourite, and each expects $2/3$, less than either pure equilibrium."
Hawk-dove with $V = 4$, $C = 6$: indifference gives $P(\text{hawk}) = V/C \approx 0.6667$.
Weighted rock-paper-scissors in which rock beats scissors for 2 (other wins pay 1): support enumeration gives rock 0.25, paper 0.5, scissors 0.25 and value 0.
"Making rock's win bigger makes paper, the counter to rock, more frequent, and leaves rock itself at only 1/4."

### Example 2: Bertrand on a tick grid

Two market makers quote a price of 1 to 5 ticks for 10 lots with cost 1 tick; the lower quote gets all 10 lots, ties split.
The pure equilibria are (1, 1), (2, 2) and (3, 3).
At (3, 3) each earns $2 \times 5 = 10$, and undercutting to 2 earns $1 \times 10 = 10$, no better.
"With a continuous price competition drives the price to cost; with a tick, a price one or two ticks above cost can be stable because undercutting by a whole tick costs as much as it gains."
This is one reason tick-size changes move quoted spreads.

### Example 3: first-price versus second-price revenue

Uniform values, $n = 2$: the first-price equilibrium bid is $v/2$, and against an opponent bidding $v'/2$ a bidder with value 0.8 maximises $(0.8 - b)\min(2b, 1)$ at $b = 0.4$.
Both formats raise $\frac{n-1}{n+1} = \frac13$; simulating 400,000 auctions (seed 42) gives about 0.3333 for both, and about 0.6666 for both at $n = 5$ (exact $\frac23$).
The winner's surplus at $n = 2$ is about $\frac13$, so $\frac16$ per bidder before values are drawn.
With a reserve of $\frac12$ the two-bidder revenue curve is $\frac13 + r^2 - \frac43r^3$, maximised at $r = \frac12$ with revenue $\frac5{12} \approx 0.4167$; the simulation gives about 0.4165.

### Example 4: the acquire-a-company problem

A firm is worth $V$ uniform on $[0, 100]$ to its owner, who knows $V$, and $1.5V$ to you; the owner accepts a bid $b$ iff $b \ge V$.
"The naive view: average value 50, worth 75 to me, so bid up to 75.
But a bid of $b$ is accepted only when $V \le b$, so the value conditional on acceptance is $1.5 \times b/2 = 0.75b < b$.
Expected profit is $\frac{b}{100}(0.75b - b) = -\frac{b^2}{400}$: a bid of 60 loses 9 on average, a bid of 100 loses 25, and the only non-losing bid is 0."
A two-million-draw simulation (seed 7) gives about $-9.0031$ for a bid of 60.

### Example 5: a common-value auction and an RFQ

Five bidders see $V + \varepsilon_i$ with $\varepsilon_i$ uniform on $[-10, 10]$.
"The winner holds the largest error, whose mean is $10 \times \frac46 \approx 6.6667$; bidding your signal overpays by that much on average."
The simulation (seed 7) gives about 6.6615.
For an RFQ to five dealers whose valuation errors are normal with sd 4 cents, $\mathbb{E}[\max_5 Z] \approx 1.1630$ (simulation about 1.1633; for two dealers it is $1/\sqrt\pi \approx 0.5642$), so the winning dealer's price is on average about 4.6519 cents too generous unless it shades for the number of competitors.

### Example 6: bargaining

With $\delta_1 = \delta_2 = 0.9$ the first proposer gets $\frac{0.1}{0.19} \approx 0.5263$; iterating backward induction over 400 rounds converges to the same number.
If the proposer is patient ($\delta_1 = 0.95$) and the responder is not ($\delta_2 = 0.8$), the proposer gets about 0.8333.
Nash bargaining over 100 with disagreement payoffs 20 and 10: maximise $(x - 20)(90 - x)$, so player 1 gets 55.

### Example 7: when does cooperation survive?

Prisoner's dilemma with $T = 5$, $R = 3$, $P = 1$, $S = 0$.
"Grim trigger: cooperate forever is worth $3/(1 - \delta)$, cheat once and get punished is $5 + \delta/(1 - \delta)$; they cross at $\delta = (5 - 3)/(5 - 1) = 0.5$."
Against tit-for-tat a one-period deviation needs $\delta \ge (5 - 3)/(3 - 0) \approx 0.6667$ to be unprofitable.
Scanning discount factors numerically finds the same two thresholds.

### Example 8: puzzles

Guess two-thirds of the average on $[0, 100]$: after $k$ rounds of elimination the bound is $100(2/3)^k$, which first drops below 1 at $k = 12$.
Pirates: with 5 pirates the senior keeps 98 and pays 1 coin each to pirates 3 and 5; with 10 pirates the senior keeps 96.
Bluffing with a pot-sized bet: bluffs should be 1/3 of the betting range and the caller should defend 1/2 of the time; with a half-pot bet, bluffs are 1/4 and the call rate 2/3.

## Pitfalls

- Looking only for pure equilibria; many trading-relevant games have only mixed ones.
- Checking a mixed equilibrium by your own indifference: each player's mix is pinned by the other player's indifference.
- Bidding your estimate in a common-value auction or RFQ, and shading less as competition grows when you should shade more.
- Assuming revenue equivalence with risk-averse bidders, correlated values or asymmetric bidders; it fails there.
- Applying backward induction to people who do not play it (ultimatum, beauty contest): equilibrium is a benchmark, the population sets the payoff.
- Forgetting that a finite, known horizon unravels cooperation.
- Treating an offered bet or an easy fill as free money instead of asking what the counterparty knows.

## Interview questions

> [!question]- risk-game-nash-definition | What is a Nash equilibrium?
> A strategy profile in which no player can gain by changing strategy alone.
> Each strategy is a best response to the others; every finite game has one in mixed strategies.

> [!question]- risk-game-mixed-indifference | How do you find a mixed equilibrium in a 2x2 game?
> Choose each player's mix to make the other indifferent between their two strategies.
> Your own mix is pinned by your opponent's payoffs, not yours.

> [!question]- risk-game-battle-sexes | Battle of the sexes with (2,1) and (1,2) on the diagonal and 0 off it: find all equilibria.
> Two pure (both at each player's favourite) and one mixed in which each plays its own favourite with probability 2/3.
> In the mixed equilibrium each expects 2/3, worse than either pure one.

> [!question]- risk-game-hawk-dove | Hawk-dove with prize 4 and fight cost 6: symmetric equilibrium?
> Hawk with probability $V/C = 2/3$.
> Indifference: $\frac{V - C}{2}p + V(1 - p) = \frac V2(1 - p)$ gives $p = V/C$.

> [!question]- risk-game-bertrand-tick | Two market makers undercut each other on a tick grid with cost 1 tick, prices 1 to 5, 10 lots to the lower quote. Equilibria?
> (1, 1), (2, 2) and (3, 3).
> At 3 ticks each earns $2 \times 5 = 10$ and undercutting to 2 earns $1 \times 10 = 10$, so no gain; at 4 undercutting pays.

> [!question]- risk-game-second-price-truthful | Why is bidding your value optimal in a second-price auction?
> Your bid only decides whether you win, not what you pay.
> Bidding above your value adds only wins at a price above value; bidding below loses only wins that were profitable.

> [!question]- risk-game-first-price-shade | Uniform private values, n bidders, first-price auction. Equilibrium bid and revenue?
> $b(v) = \frac{n-1}{n}v$ and revenue $\frac{n-1}{n+1}$.
> Maximise $(v - b)(\frac{bn}{n-1})^{n-1}$; revenue equals the expected second-highest value, as in second price.

> [!question]- risk-game-revenue-equivalence | State revenue equivalence and one way it fails.
> Standard auctions that allocate to the highest value and give the lowest type zero surplus raise the same expected revenue with independent private values and risk-neutral bidders.
> With risk-averse bidders first price raises more; with affiliated values English beats first price.

> [!question]- risk-game-reserve | Two bidders with uniform values: optimal reserve and revenue?
> Reserve 1/2, revenue 5/12 (about 0.417 against 1/3 without).
> Myerson: $r = (1 - F(r))/f(r)$; revenue $\frac13 + r^2 - \frac43r^3$.

> [!question]- risk-game-winners-curse | What is the winner's curse and how big is it with 5 bidders and uniform errors on [-10, 10]?
> Winning a common-value auction means your estimate was the highest, so it was probably too high.
> The winner's error averages $a\frac{n-1}{n+1} = 10 \times \frac46 \approx 6.67$; bid your signal minus that just to break even.

> [!question]- risk-game-acquire-company | A firm is worth V ~ U[0,100] to its informed owner and 1.5V to you; the owner sells iff your bid is at least V. What should you bid?
> Zero.
> Given acceptance $V \sim U[0, b]$, so you get $0.75b$ of value for $b$; expected profit $-b^2/400$ (bid 60 loses 9).

> [!question]- risk-game-rfq-curse | You win an RFQ against 4 other dealers whose valuation errors, like yours, are N(0, 4 cents). How much should you have shaded?
> About 4.65 cents on average.
> The winner has the most favourable error, $\sigma\,\mathbb{E}[\max_5 Z] \approx 4 \times 1.163$; more competitors means more shading.

> [!question]- risk-game-rubinstein | Alternating-offer bargaining with discount factors 0.9 and 0.9. First proposer's share?
> About 0.526.
> $\frac{1 - \delta_2}{1 - \delta_1\delta_2} = 0.1/0.19$; the responder accepts at once because waiting costs it a factor $\delta_2$.

> [!question]- risk-game-nash-bargaining | Split 100 when disagreement gives you 20 and the other side 10. Nash bargaining outcome?
> 55 to you, 45 to them.
> Maximise $(x - 20)(90 - x)$: split the 70 of surplus equally on top of the outside options.

> [!question]- risk-game-grim-trigger | Repeated prisoner's dilemma with T = 5, R = 3, P = 1. When does grim trigger sustain cooperation?
> For $\delta \ge \frac{T - R}{T - P} = 0.5$.
> Cooperate forever $\frac{3}{1 - \delta}$ against cheat once and be punished $5 + \frac{\delta}{1 - \delta}$.

> [!question]- risk-game-finite-horizon | Why does cooperation unravel in a prisoner's dilemma repeated a known, finite number of times?
> In the last round there is no future, so both defect; then the second-to-last round has no future worth protecting, and so on back to round one.
> Uncertainty about the end, or about the opponent's type, restores cooperation.

> [!question]- risk-game-two-thirds | Everyone guesses a number in [0, 100]; closest to 2/3 of the average wins. Equilibrium and what you actually guess?
> Equilibrium 0 by iterated elimination ($100(2/3)^k$ falls below 1 after 12 rounds).
> In practice guess what the population will do: experiments (Nagel 1995) find one to three levels of reasoning, so the winning number is well above 0.

> [!question]- risk-game-pirates | Five pirates split 100 coins; seniority proposes, at least half the votes needed. What does the senior pirate propose?
> 98 for himself, 0, 1, 0, 1 for the others in order of seniority.
> Backward induction: with two pirates the senior takes all, so the junior-most will accept 1, and so on.

> [!question]- risk-game-bluff-ratio | Pot 1, you bet 1 on the river with a polarised range. What share of your bets should be bluffs, and how often should the caller call?
> Bluffs one third of bets; the caller defends half the time.
> Bluff share $\frac{B}{P + 2B}$ makes calls break even; call rate $\frac{P}{P + B}$ makes bluffs break even.

> [!question]- risk-game-counterparty | Someone offers to trade with you at a price that looks great. How do you think about it game-theoretically?
> Condition on the offer: they chose to trade with you at that price, so price what they would need to know for it to be good for them.
> It is the winner's curse and adverse selection in one; size small or ask for a two-way price.

## In this repo and SDE-Interview-Prep

- Code: [game_theory.py](code/game_theory.py) (support enumeration, auction simulations, winner's curse, bargaining, repeated games, puzzles).
- Related: [Expected Value and Betting Decisions](02-Expected-Value-and-Betting-Decisions.md), [Trading Intuition and Judgement](09-Trading-Intuition-and-Judgement.md), [Market Making Games and Trading Simulations](../08-Market-Making/10-Market-Making-Games.md), [Exchange Mechanics, Auctions and Fees](../07-Market-Microstructure/02-Exchange-Mechanics-Auctions-and-Fees.md) and [Order Statistics and Extremes](../01-Probability/08-Order-Statistics-and-Extremes.md).

## Further reading

- Avinash Dixit and Barry Nalebuff, *Thinking Strategically* (1991).
- Martin Osborne and Ariel Rubinstein, *A Course in Game Theory* (1994), chapters 2 and 3 (Nash and mixed equilibria), 6 and 7 (extensive games and bargaining) and 8 (repeated games).
- Vijay Krishna, *Auction Theory*, 2nd edition (2010), chapters 2 (private values) and 6 (common values and the winner's curse).
- William Vickrey, "Counterspeculation, auctions, and competitive sealed tenders", *Journal of Finance* 16(1) (1961).
- Roger Myerson, "Optimal auction design", *Mathematics of Operations Research* 6(1) (1981).
- Ariel Rubinstein, "Perfect equilibrium in a bargaining model", *Econometrica* 50(1) (1982).
- John Nash, "The bargaining problem", *Econometrica* 18(2) (1950).
- William Samuelson and Max Bazerman, "The winner's curse in bilateral negotiations", *Research in Experimental Economics* 3 (1985).
- E. C. Capen, R. V. Clapp and W. M. Campbell, "Competitive bidding in high-risk situations", *Journal of Petroleum Technology* 23(6) (1971).
- Rosemarie Nagel, "Unraveling in guessing games: an experimental study", *American Economic Review* 85(5) (1995).
