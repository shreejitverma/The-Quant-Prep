---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Blitzstein and Hwang - Introduction to Probability 2nd ed ch 1, Zhou - A Practical Guide to Quantitative Finance Interviews ch 4, Mosteller - Fifty Challenging Problems in Probability, Feller - An Introduction to Probability Theory and Its Applications Vol 1 ch 2-3]
---

# Counting and Combinatorics

## TL;DR

- Decide two things first: does order matter, and is sampling with or without replacement; that picks one of $n^k$, $n!/(n-k)!$, $\binom{n}{k}$, $\binom{n+k-1}{k}$.
- Stars and bars: nonnegative integer solutions of $x_1+\dots+x_k=n$ number $\binom{n+k-1}{k-1}$; add upper bounds with inclusion-exclusion.
- Derangements: $D_n = n!\sum_{j=0}^{n}(-1)^j/j!$, the nearest integer to $n!/e$, so $P(\text{no fixed point}) \to 1/e \approx 0.368$.
- Reflection gives the ballot theorem, $P(\text{A always strictly ahead}) = (a-b)/(a+b)$, and the Catalan numbers $C_n = \binom{2n}{n}/(n+1)$: 1, 1, 2, 5, 14, 42, 132.
- Before counting anything big, look for a symmetry or a bijection; it usually removes most of the work.

## Learning objectives

- Count arrangements with permutations, combinations and multinomial coefficients without formula lookup.
- Apply stars and bars, inclusion-exclusion and complementary counting.
- Derive derangement counts and the ballot / Catalan numbers.
- Recognise when symmetry removes most of the counting.

## Core concepts

### Equally likely outcomes

When every outcome in a finite sample space $\Omega$ is equally likely, $P(A) = |A|/|\Omega|$.
Most interview counting errors come from counting $A$ and $\Omega$ under different conventions (ordered in one, unordered in the other).
Pick one convention and use it for both; ordered is usually safer because every ordered outcome is equally likely.

### The four basic counts

Choosing $k$ items from $n$ distinct items:

| | Order matters | Order does not matter |
| :--- | :--- | :--- |
| With replacement | $n^k$ | $\binom{n+k-1}{k}$ |
| Without replacement | $n!/(n-k)!$ | $\binom{n}{k} = \dfrac{n!}{k!(n-k)!}$ |

The unordered with-replacement count is a multiset count and is not a probability model with equally likely outcomes: rolling two dice, $\{1,2\}$ is twice as likely as $\{1,1\}$.

Multinomial: the number of ways to split $n$ distinct items into labelled groups of sizes $n_1,\dots,n_r$ is

$$
\binom{n}{n_1,\dots,n_r} = \frac{n!}{n_1!\,n_2!\cdots n_r!}.
$$

It also counts distinct arrangements of a word with repeated letters: MISSISSIPPI has $11!/(4!\,4!\,2!\,1!) = 34650$.
If the groups are unlabelled and of equal size, divide by the number of ways to permute the groups.

Circular arrangements of $n$ people: $(n-1)!$, because rotations are the same seating; divide by 2 again if reflections are identified (necklaces).

### Stars and bars

Nonnegative integer solutions of $x_1+\dots+x_k = n$: place $n$ stars and $k-1$ bars in a row, giving $\binom{n+k-1}{k-1}$.
Positive solutions: substitute $y_i = x_i - 1$, giving $\binom{n-1}{k-1}$.
Upper bounds $x_i \le m$: subtract the solutions where some $x_i \ge m+1$ by inclusion-exclusion (shift that variable down by $m+1$).

### Inclusion-exclusion

$$
\Big|\bigcup_{i=1}^n A_i\Big| = \sum_i |A_i| - \sum_{i<j}|A_i\cap A_j| + \sum_{i<j<k}|A_i\cap A_j\cap A_k| - \dots + (-1)^{n+1}|A_1\cap\dots\cap A_n|.
$$

It pays off when the intersections are symmetric, so each layer is $\binom{n}{j}$ times one number.
Onto functions (surjections) from an $n$-set to a $k$-set: let $A_i$ be the functions that miss value $i$, so

$$
\#\text{surjections} = \sum_{j=0}^{k} (-1)^j \binom{k}{j}(k-j)^n = k!\,S(n,k),
$$

where $S(n,k)$ is a Stirling number of the second kind (partitions of an $n$-set into $k$ nonempty blocks).

### Derangements

A derangement is a permutation with no fixed point.
With $A_i$ = permutations fixing $i$, $|A_{i_1}\cap\dots\cap A_{i_j}| = (n-j)!$, so

$$
D_n = \sum_{j=0}^{n}(-1)^j\binom{n}{j}(n-j)! = n!\sum_{j=0}^{n}\frac{(-1)^j}{j!}.
$$

Recurrence: element 1 goes to some position $k$ ($n-1$ choices); either $k$ goes to 1 (derange the other $n-2$) or it does not (a derangement of $n-1$ items with $k$ forbidden from slot 1), so $D_n = (n-1)(D_{n-1}+D_{n-2})$ with $D_1=0, D_2=1$.
Values: $D_3=2, D_4=9, D_5=44, D_6=265$.
The alternating series converges so fast that $D_n$ is the nearest integer to $n!/e$ for $n\ge1$.

### Reflection, ballot and Catalan

Encode a vote count or a random walk as a lattice path of $+1$ and $-1$ steps.
Reflection principle: paths from $(x_0, y_0)$ to $(x_1, y_1)$ with $y_0, y_1 > 0$ that touch the axis are in bijection with all paths from $(x_0, -y_0)$ to $(x_1, y_1)$ (reflect the part before the first touch).

Ballot theorem.
Candidate A gets $a$ votes, B gets $b<a$, counted in uniformly random order.
Paths where A is strictly ahead throughout must start with an A vote; from $(1,1)$ there are $\binom{n-1}{a-1}$ paths to the end, and the bad ones (touching 0) reflect to paths from $(1,-1)$, of which there are $\binom{n-1}{a}$.
So the good count is $\binom{n-1}{a-1}-\binom{n-1}{a} = \frac{a-b}{a+b}\binom{n}{a}$ and

$$
P(\text{A strictly ahead throughout}) = \frac{a-b}{a+b}.
$$

Catalan numbers.
Paths of $n$ up and $n$ down steps that never go below 0 (Dyck paths): a bad path first touches $-1$; reflecting everything after that point sends it to a path ending at $-2$, which has $n-1$ ups and $n+1$ downs.
So

$$
C_n = \binom{2n}{n} - \binom{2n}{n+1} = \frac{1}{n+1}\binom{2n}{n}.
$$

The same numbers count balanced parenthesisations, full binary trees with $n+1$ leaves, triangulations of an $(n+2)$-gon and non-crossing handshakes; they satisfy $C_{n+1} = \sum_{i=0}^{n}C_iC_{n-i}$.
The reflection idea reappears for barrier options and the maximum of a random walk in [Random Walks and Gambler's Ruin](11-Random-Walks-and-Gamblers-Ruin.md).

### Symmetry and bijections

- Exchangeability: in a shuffled deck the $k$-th card has the same distribution as the first, so $P(\text{2nd card is an ace}) = 1/13$ with no conditioning.
- Relative order: among any $m$ specified items, each of the $m!$ relative orders is equally likely.
  Example: the expected position of the first ace is $1 + 48/5 = 10.6$, because each of the 48 non-aces precedes all four aces with probability $1/5$.
- Double counting proves identities: counting (committee, chair) pairs two ways gives $\sum_k k\binom{n}{k} = n2^{n-1}$; Vandermonde $\sum_j \binom{m}{j}\binom{n}{k-j} = \binom{m+n}{k}$; hockey stick $\sum_{i=r}^{n}\binom{i}{r} = \binom{n+1}{r+1}$.
- Complementary counting: "at least one" is almost always $1 - P(\text{none})$.

## Worked examples

### Example 1 - poker hands

"What is the probability of a full house in five-card poker?"

Total hands: $\binom{52}{5} = 2{,}598{,}960$, unordered, all equally likely.
A full house is a rank for the triple (13), which three suits ($\binom{4}{3}=4$), a different rank for the pair (12), which two suits ($\binom{4}{2}=6$).
That is $13\cdot4\cdot12\cdot6 = 3744$ hands, so $P = 3744/2598960 = 6/4165 \approx 0.144\%$.
The ranks of triple and pair play different roles, so it is $13\times12$, not $\binom{13}{2}$.

Two pair is the opposite case: the two pair ranks are interchangeable, so choose them with $\binom{13}{2}=78$, suits $6^2=36$, kicker $11\cdot4=44$.
That gives $78\cdot36\cdot44 = 123{,}552$ hands and $P\approx 4.75\%$.
The check to say aloud: "are these two ranks distinguishable by role? If yes, ordered; if no, choose."

### Example 2 - the hat-check problem

"$n$ people drop hats at a cloakroom and get them back in random order. What is the probability nobody gets their own hat?"

This is $D_n/n!$.
By inclusion-exclusion, $P = \sum_{j=0}^{n}(-1)^j/j!$.
For $n=4$: $1 - 1 + 1/2 - 1/6 + 1/24 = 9/24 = 3/8$.
As $n\to\infty$ it tends to $e^{-1}\approx 0.3679$, and already at $n=6$ it agrees to three decimals, so for any realistic $n$ the answer is "about 37%".
The expected number of people who do get their own hat is exactly 1 for every $n$ (linearity, each person with probability $1/n$); see [Expectation, Variance and Linearity](04-Expectation-Variance-and-Linearity.md).

### Example 3 - three dice summing to 10

"Roll three fair dice. What is the probability the sum is 10?"

Write $y_i = x_i - 1 \in \{0,\dots,5\}$, so we need $y_1+y_2+y_3 = 7$.
Stars and bars without the upper bound: $\binom{9}{2} = 36$.
Subtract solutions with some $y_i \ge 6$: set $y_i' = y_i - 6$, leaving a sum of 1 over 3 variables, $\binom{3}{2} = 3$ solutions, for each of 3 choices of $i$, so 9.
Two variables at least 6 would need a sum of at least 12, impossible.
So $36 - 9 = 27$ ordered outcomes and $P = 27/216 = 1/8$.
Sanity check by symmetry: sums 10 and 11 are the two middle values of the symmetric range 3 to 18 and both have 27 ways.

### Example 4 - ballot counting

"In an election A gets 6 votes and B gets 4. Ballots are counted in random order. What is the probability A is strictly ahead at every point of the count?"

By the ballot theorem it is $(6-4)/(6+4) = 1/5$.
Out of $\binom{10}{4} = 210$ equally likely orders, $42$ keep A strictly ahead.
If asked to derive: the first vote must be A; any path from $(1,1)$ that later hits 0 reflects (before the first hit) to a path from $(1,-1)$, so bad paths number $\binom{9}{6} = 84$ and good paths are $\binom{9}{5} - \binom{9}{6} = 126 - 84 = 42$.

### Example 5 - four aces, one per player

"A bridge deck is dealt to four players, 13 each. What is the probability each player gets exactly one ace?"

Think sequentially about where the aces land among the 52 slots.
The first ace goes anywhere.
The second must be in one of the 39 slots belonging to other players, out of 51 remaining: $39/51$.
The third: $26/50$; the fourth: $13/49$.
So $P = \frac{39\cdot26\cdot13}{51\cdot50\cdot49} = \frac{2197}{20825} \approx 0.1055$.
The multinomial route, $4!\,\binom{48}{12,12,12,12}\big/\binom{52}{13,13,13,13}$, gives the same number with much more arithmetic.

## Pitfalls

- Mixing ordered and unordered counts between numerator and denominator.
- Treating multisets as equally likely: $\{1,1\}$ and $\{1,2\}$ are not equally likely on two dice.
- Overcounting interchangeable roles (two pair) or undercounting distinguishable roles (full house).
- Double counting in "at least one" problems: $\binom{4}{1}\binom{51}{4}$ is not the number of hands containing an ace; use the complement.
- Forgetting upper bounds in stars and bars (dice faces stop at 6).
- Stopping inclusion-exclusion after two terms when higher intersections are nonzero.
- Using $n!$ for circular seatings, where rotations are identical.
- Reaching for heavy counting when exchangeability gives the answer in one line.

## Interview questions

> [!question]- prob-count-full-house-probability | What is the probability of being dealt a full house in five-card poker?
> $3744/2598960 = 6/4165 \approx 0.144\%$.
> Triple rank 13, triple suits $\binom43=4$, pair rank 12, pair suits $\binom42=6$: $13\cdot4\cdot12\cdot6=3744$ out of $\binom{52}{5}$.

> [!question]- prob-count-two-pair-probability | What is the probability of two pair in five-card poker?
> $123552/2598960 \approx 4.75\%$.
> Pair ranks $\binom{13}{2}=78$ (interchangeable), suits $6^2$, kicker $11\cdot4=44$: $78\cdot36\cdot44=123552$.

> [!question]- prob-count-derangement-hat-check | Four people get their hats back in random order. What is the probability no one gets their own hat, and what is the limit for large n?
> $9/24 = 3/8$; the limit is $1/e \approx 0.368$.
> Inclusion-exclusion: $D_n/n! = \sum_{j=0}^n (-1)^j/j!$, and $D_4 = 9$.

> [!question]- prob-count-birthday-twenty-three | What is the smallest group size for which a shared birthday is more likely than not (365 equally likely days)?
> 23, with probability about $0.507$.
> $P(\text{all distinct}) = \prod_{i=0}^{n-1}(1-i/365)$ drops below $1/2$ at $n=23$ (it is $0.524$ at 22 people, i.e. shared $0.476$); roughly $e^{-n(n-1)/730}$.

> [!question]- prob-count-stars-bars-nonnegative | How many nonnegative integer solutions does $x_1+x_2+x_3=10$ have? How many positive ones?
> 66 nonnegative, 36 positive.
> Stars and bars: $\binom{10+2}{2}=66$; with $x_i\ge1$ substitute $y_i=x_i-1$ summing to 7: $\binom{9}{2}=36$.

> [!question]- prob-count-three-dice-sum-ten | Three fair dice are rolled. What is the probability the sum is 10?
> $27/216 = 1/8$.
> $y_i=x_i-1\in[0,5]$ sum to 7: $\binom92=36$ minus $3\binom32=9$ solutions with some $y_i\ge6$.

> [!question]- prob-count-ballot-always-ahead | A gets 6 votes and B gets 4, counted in random order. What is the probability A is strictly ahead throughout the count?
> $1/5$.
> Ballot theorem $(a-b)/(a+b)$, proved by reflecting bad paths: $\binom95-\binom96=42$ good orders out of $\binom{10}{4}=210$.

> [!question]- prob-count-catalan-parentheses | How many balanced strings of 5 pairs of parentheses are there?
> 42, the Catalan number $C_5$.
> $C_n=\binom{2n}{n}/(n+1) = 252/6 = 42$; reflection removes the $\binom{2n}{n+1}$ paths that dip below zero.

> [!question]- prob-count-surjections-five-into-three | How many ways can 5 distinct balls go into 3 distinct boxes with no box empty?
> 150.
> Inclusion-exclusion on empty boxes: $3^5 - 3\cdot2^5 + 3\cdot1^5 = 243-96+3 = 150 = 3!\,S(5,3)$ with $S(5,3)=25$.

> [!question]- prob-count-four-aces-one-each | A bridge deck is dealt into four hands of 13. What is the probability each hand has exactly one ace?
> $2197/20825 \approx 0.1055$.
> Place aces one by one: $1\cdot\frac{39}{51}\cdot\frac{26}{50}\cdot\frac{13}{49}$.

> [!question]- prob-count-round-table-adjacent | Ten people sit at random around a round table. What is the probability two particular people sit next to each other?
> $2/9$.
> Seat the first person anywhere; the second is equally likely to be in any of the other 9 seats, 2 of which are adjacent.

> [!question]- prob-count-mississippi-anagrams | How many distinct arrangements of the letters of MISSISSIPPI are there?
> 34650.
> Multinomial $11!/(4!\,4!\,2!\,1!)$ for I, S, P, M.

> [!question]- prob-count-first-ace-position | A standard deck is shuffled. What is the expected position of the first ace?
> $53/5 = 10.6$.
> Each of the 48 non-aces comes before all four aces with probability $1/5$ (symmetry among 5 cards), so $E = 1 + 48/5$.

> [!question]- prob-count-committee-chair-identity | Show that $\sum_{k=0}^n k\binom{n}{k} = n2^{n-1}$ without algebra.
> Count (committee, chair) pairs two ways.
> Choose the committee of size $k$ then a chair from it: $\sum_k k\binom nk$; or choose the chair ($n$ ways) then any subset of the remaining $n-1$: $n2^{n-1}$.

> [!question]- prob-count-de-mere-bets | Which is more likely: at least one six in 4 rolls of a die, or at least one double six in 24 rolls of two dice?
> At least one six in 4 rolls: $1-(5/6)^4 \approx 0.518$ versus $1-(35/36)^{24} \approx 0.491$.
> Complementary counting; the naive "4/6 versus 24/36" proportionality argument is wrong because events overlap.

## Further reading

- Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), chapter 1 (counting, story proofs, inclusion-exclusion).
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 4 (combinatorial analysis section).
- Frederick Mosteller, *Fifty Challenging Problems in Probability*, problems on cards, birthdays and ballots.
- William Feller, *An Introduction to Probability Theory and Its Applications*, Vol. 1, chapters 2-3 (combinatorics, reflection and ballot theorem).
- Next: [Conditional Probability and Bayes](02-Conditional-Probability-and-Bayes.md) and the harder mixed problems in [Probability Problem Set](15-Probability-Problem-Set.md).
