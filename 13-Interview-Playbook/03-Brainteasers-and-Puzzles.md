---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: []
est_hours: 6
sources: [Xinfeng Zhou - A Practical Guide to Quantitative Finance Interviews (2008), Timothy Crack - Heard on the Street: Quantitative Questions from Wall Street Job Interviews, Peter Winkler - Mathematical Puzzles: A Connoisseur's Collection (2004)]
---

# Brainteasers and Puzzles

## TL;DR

- Most puzzles yield to six tools: small cases, working backwards, symmetry, invariants (parity, mod $k$, colouring), information counting, and pigeonhole.
- Count information before designing a strategy: $w$ weighings with three outcomes distinguish at most $3^w$ cases.
- Solve the $n=1,2,3$ cases out loud, spot the pattern, then argue it by induction.
- When a process looks complicated, look for a quantity it cannot change.
- Answer first, then the shortest convincing argument, then a sanity check; interviewers score the reasoning as much as the answer.

## Learning objectives

- Solve logic, weighing, river-crossing and invariant puzzles.
- Use symmetry, invariants, induction and working backwards.

## Core concepts

### Why firms still ask them

A brainteaser is a compressed test of structured thinking under mild pressure.
The interviewer watches whether you clarify the rules, try small cases, notice structure, and communicate.
Known puzzles are commonly followed by a variation, so memorising answers without the argument does not survive the follow-up.

### The toolbox

**Small cases and induction.**
Shrink the problem until it is trivial, solve $n = 1, 2, 3$, guess the pattern and prove it by induction.
Pirate puzzles, egg drops and many games fall this way.

**Working backwards.**
In sequential games, solve from the final state: the last mover's choice is obvious, which fixes the second-to-last, and so on.
This is backward induction, the same logic as pricing an American option on a tree.

**Symmetry.**
If two options are interchangeable, they have equal value; if a strategy can mirror the opponent, the second player cannot lose.
Collisions of identical ants are equivalent to the ants passing through each other.

**Invariants and monovariants.**
Find a quantity the allowed moves cannot change (parity, a residue mod $k$, a colouring count) and compare start and target.
A monovariant only moves one way and proves termination.

**Information counting.**
A balance weighing has 3 outcomes, a yes or no question has 2.
If there are $N$ possibilities you need at least $\lceil \log_3 N \rceil$ weighings or $\lceil \log_2 N \rceil$ questions.
The counting bound is also the design rule: split each step into near-equal thirds or halves.

**Pigeonhole.**
$n+1$ objects in $n$ boxes forces a shared box; it proves existence without construction.

### How to run the conversation

1. Restate the problem and ask about ambiguous rules (can I use a pan more than once, are the agents rational, do ties pass?).
2. Say which tool you are trying and why.
3. Work a small case on paper where the interviewer can see it.
4. State the answer, then verify it against a boundary or the small case.
5. If stuck, say what you have ruled out; a hint taken well scores better than silence.

## Worked examples

### Example 1: twelve coins, three weighings

One of 12 coins is counterfeit, heavier or lighter, unknown which.
Find it and whether it is heavy or light in three weighings.

Count first: there are $12 \times 2 = 24$ cases and $3^3 = 27$ outcomes, so it is possible in principle but tight.
Weigh $\{1,2,3,4\}$ against $\{5,6,7,8\}$.

- **Balanced.** The fake is in $\{9,\dots,12\}$ (8 cases).
  Weigh $\{9,10,11\}$ against the genuine $\{1,2,3\}$.
  If balanced, 12 is fake; weigh it against coin 1 to get the direction.
  If the left side is heavy, one of 9, 10, 11 is heavy; weigh 9 against 10, and the heavier is fake, or 11 if they balance (symmetric if light).
- **Left heavy.** Either one of 1-4 is heavy or one of 5-8 is light (8 cases).
  Weigh $\{1,2,5\}$ against $\{3,6,9\}$, where 9 is known genuine.
  Balanced leaves 4 heavy, 7 light or 8 light: weigh 7 against 8; the lighter is fake, and if they balance 4 is heavy.
  Left heavy leaves 1 heavy, 2 heavy or 6 light: weigh 1 against 2; the heavier is fake, or 6 is light if they balance.
  Right heavy leaves 3 heavy or 5 light: weigh 3 against a genuine coin.

Each second weighing splits 8 cases into groups of at most 3, which one weighing resolves.
In general $w$ weighings handle at most $(3^w - 3)/2$ coins when the direction is unknown and must be reported, which is 12 for $w=3$.

### Example 2: five pirates and 100 coins

Pirates ranked A (most senior) to E propose splits in order; a proposal passes with at least half the votes, otherwise the proposer is thrown overboard.
Pirates are rational, greedy, and prefer throwing someone overboard when indifferent.

Work backwards.

- Two pirates (D, E): D proposes $(100, 0)$ and his own vote is half, so it passes.
- Three (C, D, E): C needs one more vote; E gets 0 under D, so 1 coin buys E: $(99, 0, 1)$.
- Four (B, C, D, E): B needs one more vote; D gets 0 under C: $(99, 0, 1, 0)$.
- Five (A to E): A needs two more votes; C and E get 0 under B, so 1 coin each buys them: $(98, 0, 1, 0, 1)$.

The answer is A keeps 98, C and E get 1 each.
The follow-up usually changes the tie rule or the number of pirates; redo the backward induction rather than pattern-matching.

### Example 3: 100 prisoners and hats

100 prisoners stand in a line, each wearing a black or white hat, each seeing all hats in front.
From the back, each calls out a colour; a correct call saves that prisoner.
Maximise the guaranteed number saved.

The back prisoner calls "black" if he sees an odd number of black hats, "white" otherwise.
He is saved with probability $1/2$, but every other prisoner can now deduce his own hat: he knows the parity of the 99 hats in front of the back prisoner, sees the hats ahead of him, and has heard the calls (all correct) from behind.
The difference in parity is his own hat.
Guaranteed: 99 saved, and the 100th with probability $1/2$.
No strategy guarantees 100, because the back prisoner's own hat is independent of everything he can observe.

### Example 4: two eggs, 100 floors

Find the highest safe floor with the fewest worst-case drops using two identical eggs.

With $k$ drops available, drop the first egg from floor $k$; if it breaks, check floors $1, \dots, k-1$ with the second egg.
If not, you have $k-1$ drops left, so the next drop goes $k-1$ floors higher, and so on.
$k$ drops cover $k + (k-1) + \dots + 1 = k(k+1)/2$ floors.
$13 \cdot 14 / 2 = 91 < 100 \le 105 = 14 \cdot 15 / 2$, so the answer is 14 drops, starting at floors 14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100.

### Example 5: chameleons (an invariant)

An island has 13 red, 15 green and 17 blue chameleons.
When two of different colours meet, both turn into the third colour.
Can all 45 end up the same colour?

A meeting changes the counts by $(-1, -1, +2)$ in some order, so every pairwise difference changes by $0$ or $\pm 3$.
Pairwise differences mod 3 are therefore invariant.
All one colour means two counts are 0, so some difference is $0 \bmod 3$.
Initially the differences are $2, 4, 2$, which are $2, 1, 2 \bmod 3$, none zero.
So it is impossible.

## Pitfalls

- Starting to compute before counting the information available; the counting bound often reveals the design.
- Giving a memorised answer to a changed variation (ties failing instead of passing, a known versus unknown direction).
- Assuming a greedy strategy is optimal in a sequential game instead of working backwards.
- Ignoring a rule detail: whether the balance can be reused, whether the torch must return, whether agents are perfectly rational.
- Stating a construction without showing it is optimal, or a bound without showing it is achievable.
- Silence; say what you are trying even when it fails.

## Interview questions

> [!question]- int-bt-twelve-coins-three-weighings | Twelve coins, one fake that is heavier or lighter. Can you find it and its direction in three weighings?
> Yes. There are 24 cases and $3^3 = 27$ outcomes; weigh 4 against 4, then split each branch of 8 cases into groups of at most 3 (for example $\{1,2,5\}$ against $\{3,6,9\}$). Three weighings handle at most $(3^3-3)/2 = 12$ coins.

> [!question]- int-bt-eight-balls-two-weighings | Eight balls, one heavier. Minimum number of weighings to find it?
> 2. Weigh 3 against 3; if balanced it is among the other 2 (one more weighing), otherwise among the heavy 3 (weigh 1 against 1). Lower bound: 8 cases need $\lceil \log_3 8 \rceil = 2$.

> [!question]- int-bt-ropes-45-minutes | Two ropes each burn in exactly 60 minutes but unevenly. Measure 45 minutes.
> Light rope A at both ends and rope B at one end. A finishes at 30 minutes; then light B's other end, and its remaining 30 minutes of burn take 15, finishing at 45.

> [!question]- int-bt-five-pirates | Five pirates split 100 coins; a proposal passes with at least half the votes. What does the most senior pirate propose?
> $(98, 0, 1, 0, 1)$. By backward induction: 2 pirates $(100,0)$; 3 pirates $(99,0,1)$; 4 pirates $(99,0,1,0)$; with 5, the pirates who would get 0 under the next proposer (third and fifth) are bought with 1 coin each.

> [!question]- int-bt-hats-in-a-line | 100 prisoners in a line with black or white hats call their colour from the back. How many can be guaranteed saved?
> 99. The last prisoner announces the parity of black hats he sees; each subsequent prisoner deduces his own hat from that parity, the hats ahead and the calls behind. The first caller is saved with probability $1/2$.

> [!question]- int-bt-hundred-lockers | 100 closed lockers; pass $k$ toggles every $k$-th locker for $k = 1..100$. How many are open at the end?
> 10. Locker $n$ is toggled once per divisor; divisors pair up except for perfect squares, so only the 10 squares $1, 4, \dots, 100$ have an odd count.

> [!question]- int-bt-two-eggs-100-floors | Two eggs, 100 floors: minimum worst-case drops to find the critical floor?
> 14. With $k$ drops you can cover $k(k+1)/2$ floors by dropping first at $k$, then $k-1$ floors higher, and so on; $14 \cdot 15/2 = 105 \ge 100$ while $13 \cdot 14/2 = 91 < 100$.

> [!question]- int-bt-trailing-zeros-100-factorial | How many trailing zeros does $100!$ have?
> 24. Count factors of 5: $\lfloor 100/5 \rfloor + \lfloor 100/25 \rfloor = 20 + 4 = 24$, and 2s are more plentiful.

> [!question]- int-bt-mutilated-chessboard | Remove two opposite corners of a chessboard. Can 31 dominoes tile the remaining 62 squares?
> No. Opposite corners share a colour, leaving 32 of one colour and 30 of the other, but each domino covers one of each.

> [!question]- int-bt-bridge-and-torch | Four people cross a bridge in 1, 2, 5 and 10 minutes; at most two cross at once with one torch that must be carried. Minimum total time?
> 17 minutes. 1 and 2 cross (2), 1 returns (1), 5 and 10 cross (10), 2 returns (2), 1 and 2 cross (2). Sending the two slowest together is the key.

> [!question]- int-bt-jugs-3-and-5 | With a 3-litre and a 5-litre jug, measure exactly 4 litres.
> Fill the 5, pour into the 3 (2 left), empty the 3, pour the 2 into it, fill the 5, top up the 3 (uses 1), leaving 4 in the 5. Possible because $\gcd(3,5) = 1$.

> [!question]- int-bt-poisoned-wine | 1000 bottles, one poisoned; poison acts in 24 hours. How many testers to find it in one round?
> 10. Label bottles in binary; tester $i$ drinks from every bottle whose bit $i$ is 1. The set of testers who fall ill spells the bottle's number, and $2^{10} = 1024 \ge 1000$.

> [!question]- int-bt-mislabelled-boxes | Three boxes labelled apples, oranges and mixed are all wrongly labelled. Drawing one fruit from one box, how do you fix all labels?
> Draw from the box labelled mixed. It must hold a single type, say apples; the box labelled oranges cannot be oranges or apples now, so it is mixed, and the remaining box is oranges.

> [!question]- int-bt-ants-on-a-stick | 100 ants on a 1 m stick walk at 1 cm/s in random directions and reverse on collision. Longest time until all fall off?
> 100 seconds. A collision is equivalent to the ants passing through each other, so each "ant path" walks straight off, and the longest path is the full metre.

> [!question]- int-bt-knockout-matches | How many matches does a single-elimination tournament with 64 players need?
> 63. Every match eliminates exactly one player and all but one must be eliminated; this works for any $n$ ($n-1$ matches) even with byes.

> [!question]- int-bt-light-switches | Three switches outside a room control one of three bulbs inside; you may enter once. Which switch is which?
> Turn on switch 1 for a few minutes, turn it off, turn on switch 2, enter. The lit bulb is 2, the warm unlit bulb is 1, the cold unlit bulb is 3.

> [!question]- int-bt-heavy-pill-jar | Ten jars of 10 g pills, but one jar has 11 g pills. Identify it with one weighing.
> Take $k$ pills from jar $k$ and weigh them all. The excess over $550$ g equals the number of the heavy jar.

> [!question]- int-bt-coins-blindfold | 100 coins lie on a table, exactly 10 heads up. Blindfolded, split them into two piles with equal numbers of heads.
> Take any 10 coins as one pile and flip all of them. If that pile had $h$ heads, the other pile has $10-h$, and after flipping the small pile also has $10-h$.

> [!question]- int-bt-handshake-parity | Prove that at any party the number of people who shook an odd number of hands is even.
> The degrees sum to twice the number of handshakes, which is even; the even-degree terms contribute an even amount, so the odd-degree terms must be even in number.

> [!question]- int-bt-chameleons | 13 red, 15 green, 17 blue chameleons; two of different colours meeting both turn the third colour. Can all become one colour?
> No. Each meeting shifts pairwise differences by 0 or $\pm 3$, so differences mod 3 are invariant; initially they are $2, 1, 2 \bmod 3$, but a monochrome end state needs a difference of $0 \bmod 3$.

> [!question]- int-bt-coins-in-a-row | An even number of coins of different values lie in a row; players alternately take an end coin. Can the first player guarantee at least half the total?
> Yes. Colour positions odd and even; the first player can always take all odd-position coins or all even-position coins, because after each of his picks the opponent faces two ends of the other parity. He picks the larger colour class.

> [!question]- int-bt-nim-100-take-1-to-10 | 100 coins; players alternately take 1 to 10; whoever takes the last coin wins. Do you go first, and what do you take?
> Go first and take 1. Multiples of 11 are losing positions for the player to move; leave 99, then answer any take $t$ with $11 - t$.

> [!question]- int-bt-frobenius-3-and-5 | With only 3 and 5 unit coins, what is the largest amount you cannot pay exactly?
> 7. $8 = 3+5$, $9 = 3 \cdot 3$, $10 = 5 \cdot 2$, and adding 3 to each covers every larger amount by induction; 7 is not a non-negative combination. In general $ab - a - b$ for coprime $a, b$.

> [!question]- int-bt-clock-overlaps | How many times do the hour and minute hands overlap in 24 hours?
> 22. The minute hand gains a full lap on the hour hand every $12/11$ hours, so there are 11 overlaps in 12 hours.

> [!question]- int-bt-clock-angle-3-15 | What is the angle between the hands at 3:15?
> $7.5$ degrees. The minute hand is at $90$ degrees; the hour hand is at $90 + 15 \times 0.5 = 97.5$ degrees.

> [!question]- int-bt-snail-in-well | A snail climbs 3 ft each day and slips 2 ft each night in a 30 ft well. On which day does it get out?
> Day 28. After 27 days and nights it is at 27 ft, and on day 28 it climbs to 30 before slipping.

> [!question]- int-bt-train-and-fly | Two trains 100 miles apart approach at 50 mph each; a fly shuttles between them at 75 mph. How far does it fly?
> 75 miles. The trains meet in 1 hour, and the fly flies for that hour; no series needed.

> [!question]- int-bt-three-daughters-ages | Three daughters' ages multiply to 36; their sum is the house number, which does not settle it; the eldest likes chocolate. Ages?
> 2, 2 and 9. Only sum 13 is ambiguous, from $(1,6,6)$ and $(2,2,9)$; "the eldest" rules out twins at the top.

> [!question]- int-bt-last-digit-7-power | What is the last digit of $7^{2026}$?
> 9. Last digits of powers of 7 cycle $7, 9, 3, 1$ with period 4, and $2026 \equiv 2 \pmod 4$.

> [!question]- int-bt-squares-on-chessboard | How many squares of any size are on an $8 \times 8$ chessboard?
> 204. There are $(9-k)^2$ squares of side $k$, so $\sum_{j=1}^{8} j^2 = 204$.

> [!question]- int-bt-rectangles-on-chessboard | How many rectangles (including squares) are on an $8 \times 8$ chessboard?
> 1296. Choose 2 of the 9 vertical lines and 2 of the 9 horizontal lines: $\binom{9}{2}^2 = 36^2$.

> [!question]- int-bt-truth-liar-guards | Two doors, two guards; one always lies and one always tells the truth. One question to find the safe door?
> Ask either guard "Which door would the other guard say is safe?" and take the other door. Both paths through the question pass through exactly one lie.

> [!question]- int-bt-staircase-one-or-two | In how many ways can you climb 10 stairs taking 1 or 2 steps at a time?
> 89. $f(n) = f(n-1) + f(n-2)$ with $f(1) = 1$, $f(2) = 2$ gives Fibonacci numbers, and $f(10) = 89$.

## Further reading

- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews* (2008), chapter 2 on brainteasers.
- Timothy Crack, *Heard on the Street: Quantitative Questions from Wall Street Job Interviews*.
- Peter Winkler, *Mathematical Puzzles: A Connoisseur's Collection* (2004).
- [Sequences and Numerical Reasoning Tests](06-Sequences-and-Numerical-Reasoning.md) for pattern spotting under time pressure.
