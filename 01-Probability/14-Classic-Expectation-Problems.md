---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [expectation-variance-and-linearity, markov-chains]
est_hours: 3
sources: [Zhou - A Practical Guide to Quantitative Finance Interviews, Mosteller - Fifty Challenging Problems in Probability, Crack - Heard on the Street, Blitzstein and Hwang - Introduction to Probability (2nd ed.), Ferguson - Who Solved the Secretary Problem? (Stat. Sci. 1989)]
---

# Classic Expectation Problems

## TL;DR

- Four tools solve nearly every classic: indicators with linearity, first-step conditioning, tail sums $E[N] = \sum_{n \ge 0} P(N > n)$, and symmetry.
- Coupon collector: $n H_n$ draws to see all $n$ types ($14.7$ rolls for a die), as a sum of geometric waits.
- Birthday: 23 people give a $50.7\%$ chance of a shared birthday; the expected number of matching pairs is $\binom{k}{2}/365$.
- Hat check: the expected number of fixed points of a random permutation is 1, the variance is 1, and $P(\text{none}) \to 1/e$.
- Optimal stopping by backward induction: a die with up to 3 rolls is worth $14/3$; the secretary rule (skip $n/e$, then take the first record) succeeds with probability about $1/e$.

## Learning objectives

- Solve coupon collector, birthday and matching (hat-check) problems, including variances.
- Compare waiting times for patterns such as HH versus HT and explain the difference.
- Solve the secretary problem and optimal stopping variants.
- Solve dice games with optimal continuation (re-roll decisions) by backward induction.

## Core concepts

### The toolkit

1. Indicators: write the count as $\sum_i \mathbf{1}_{A_i}$ and use $E[\sum \mathbf{1}_{A_i}] = \sum P(A_i)$; no independence needed. Variances need the pairwise terms $P(A_i \cap A_j)$.
2. First-step analysis: condition on the first move and solve the resulting linear equations (see [Markov Chains](10-Markov-Chains.md)).
3. Tail sums: for non-negative integer $N$, $E[N] = \sum_{n \ge 0} P(N > n)$.
4. Symmetry and exchangeability: "each of the 48 non-aces is equally likely to be in any of the 5 slots cut by the 4 aces".
5. Backward induction for optimal stopping: the value with $k$ chances left is $V_k = E[\max(X, V_{k-1})]$.

See [Expectation, Variance and Linearity](04-Expectation-Variance-and-Linearity.md) for the underlying identities.

### Coupon collector

With $n$ equally likely types, once $k-1$ types are collected the wait for a new one is geometric with success probability $(n - k + 1)/n$.
So the total time $T$ is a sum of independent geometrics:

$$
E[T] = \sum_{k=1}^{n} \frac{n}{k} = n H_n \approx n \ln n + 0.577n, \qquad \operatorname{Var}(T) = n^2 \sum_{k=1}^{n} \frac{1}{k^2} - n H_n .
$$

For a die, $E[T] = 14.7$ and $\operatorname{Var}(T) = 38.99$ (standard deviation about $6.2$).
The number of distinct types seen in $m$ draws has mean $n(1 - (1 - 1/n)^m)$ by indicators.

### Birthday problem

$P(\text{all } k \text{ distinct}) = \prod_{j=0}^{k-1} (1 - j/365) \approx e^{-k^2/730}$.
It drops below $1/2$ at $k = 23$ ($P(\text{match}) \approx 0.507$).
Expected number of matching pairs among $k$ people is $\binom{k}{2}/365$ ($1.19$ for 30 people), which is why intuition fails: the number of pairs grows quadratically.
The expected number of people until the first repeat is about $24.6$.
Contrast: to have a better than even chance that someone shares your birthday you need 253 others, since that is $1 - (364/365)^k > 1/2$.

### Matching (hat check)

Let $F$ be the number of fixed points of a uniform random permutation of $n$.
Indicators give $E[F] = n \cdot (1/n) = 1$.
For the variance, $P(i \text{ and } j \text{ fixed}) = 1/(n(n-1))$, so each pair has covariance $1/(n^2(n-1))$ and

$$
\operatorname{Var}(F) = n \cdot \frac1n\left(1 - \frac1n\right) + n(n-1)\cdot\frac{1}{n^2(n-1)} = 1 .
$$

By inclusion-exclusion $P(F = 0) = \sum_{k=0}^{n} (-1)^k/k! \to 1/e$, and $F \to \text{Poisson}(1)$.
The expected number of cycles is $H_n$.

### Pattern waiting times

HH takes 6 flips on average and HT takes 4.
For $n$ heads in a row it is $2^{n+1} - 2$; with head probability $p$, HH takes $(1 + p)/p^2$.
The general rule (sum of $1/P(\text{prefix})$ over prefixes that are also suffixes) is derived in [Martingales and Optional Stopping](12-Martingales-and-Optional-Stopping.md).

### Secretary problem

$n$ candidates in uniformly random order; you see relative ranks only and must accept or reject on the spot; you win only by picking the best.
Rule: reject the first $r - 1$, then accept the first candidate better than all before.
You win if the best is at position $i \ge r$ and the best of the first $i-1$ is among the first $r-1$:

$$
P(r) = \sum_{i=r}^{n} \frac1n \cdot \frac{r-1}{i-1} \approx x \ln\frac1x, \quad x = \frac{r}{n} .
$$

Maximised at $x = 1/e$ with value $1/e \approx 0.368$.
Exact small cases: $n = 3$, skip 1, win $1/2$; $n = 10$, skip 3, win $0.399$; $n = 100$, skip 37, win $0.371$.

### Dice with continuation

With $k$ rolls allowed and the last roll kept, $V_1 = 3.5$ and $V_{k} = E[\max(X, V_{k-1})]$: keep a roll iff it beats the value of continuing.
$V_2 = 17/4 = 4.25$, $V_3 = 14/3 \approx 4.67$, $V_4 = 89/18 \approx 4.94$.

## Worked examples

### Coupon collector for a die

"I need all six faces. The first roll always gives a new face. Then a new face comes with probability $5/6$, so I wait $6/5$ rolls on average, then $6/4$, and so on."
"Total: $6(1 + 1/2 + 1/3 + 1/4 + 1/5 + 1/6) = 6 \times 49/20 = 14.7$."
"Variance: each wait is geometric with variance $(1-p)/p^2$; summing gives $36 \times 5369/3600 - 14.7 = 38.99$, so the standard deviation is about 6."
"Sanity check: $n \ln n + 0.577n \approx 10.75 + 3.46 = 14.2$, close."

### Hat check

"Ten people take random hats. Expected number who get their own?"
"Indicator for each person, each with probability $1/10$, so the expected count is 1 regardless of $n$."
"Variance is also 1: the pairwise indicators have $P = 1/90$ versus $1/100$ under independence, and the $90$ ordered pairs contribute exactly $90(1/90 - 1/100) = 1/10$, which tops up $10 \times 0.09 = 0.9$ to 1."
"Probability nobody gets their hat: $\sum_{k=0}^{10} (-1)^k/k! \approx 0.36788$, already $1/e$ to six digits."

### HH versus HT

"For HT: wait for the first H (2 flips on average). From then on, any T finishes and any H leaves me with an H, so I wait 2 more: total 4."
"For HH: let $E_0$ be the wait from scratch and $E_1$ after an H. $E_1 = 1 + \frac12 E_0$ because a T destroys progress, and $E_0 = 1 + \frac12 E_1 + \frac12 E_0$."
"So $E_0 = 2 + E_1 = 3 + E_0/2$, giving $E_0 = 6$."
"The asymmetry comes from failure: a failed HT attempt still leaves an H, a failed HH attempt leaves nothing."

### Secretary with three candidates

"Three candidates, random order. If I take the first I win with probability $1/3$."
"Skip the first and take the next one better than it: the six orders by rank (1 is best) are 123, 132, 213, 231, 312, 321."
"I win on 213 and 312 (the best arrives second and beats the first), and on 231 (the 3 at position 2 is worse than the 2, so I wait and take the 1)."
"I lose on 123 and 132 (the best was skipped) and on 321 (the 2 at position 2 beats the 3, so I stop too early)."
"Three wins out of six: $1/2$, better than $1/3$, and the formula gives $\frac13 \cdot 1 \cdot (1 + 1/2) = 1/2$."

### Dice with up to three rolls

"I can roll up to three times and keep the last roll. Work backwards."
"With one roll left the value is 3.5. With two rolls left, I keep 4, 5, 6 and re-roll 1, 2, 3: value $(4 + 5 + 6)/6 + \frac36 \times 3.5 = 17/4$."
"With three rolls left, I keep only 5 or 6 (since $4 < 4.25$): value $(5 + 6)/6 + \frac46 \times \frac{17}{4} = 14/3$."
"Variant: unlimited re-rolls but each costs \$1. The value $V$ solves $V = E[\max(X, V - 1)]$; keeping 4 or better gives $V/2 = 15/6 - 1/2$, so $V = 4$, and keeping 3 or better also gives 4 (at 3 you are indifferent)."

### Expected number of uniforms to exceed 1

"Draw $U_1, U_2, \dots$ uniform until the running sum exceeds 1. Let $N$ be the number drawn."
"$N > n$ iff the first $n$ sum to less than 1, which is the simplex volume $1/n!$."
"Tail sum: $E[N] = \sum_{n \ge 0} 1/n! = e$."
"The same answer holds for 'draw until the sequence first decreases', because $P(U_1 < \dots < U_n) = 1/n!$ too."

## Pitfalls

- Multiplying probabilities in birthday or hat-check problems as if events were independent; linearity handles expectations, but variances and "none" probabilities need the dependence.
- Confusing "some pair shares a birthday" (23 people) with "someone shares my birthday" (253 people).
- Arguing HH and HT must have equal waiting times because $P(HH) = P(HT)$ per pair of flips; overlap changes waiting times, not frequencies.
- Forgetting in re-roll games that the continuation value changes with the number of rolls left; the threshold is not fixed.
- In the secretary problem, optimising for expected rank instead of the probability of the best: they give different rules.

## Interview questions

> [!question]- prob-classic-coupon-die-all-faces | Expected number of die rolls to see all six faces?
> $14.7$. Sum of geometric waits: $6(1 + 1/2 + \dots + 1/6) = 6 H_6$.

> [!question]- prob-classic-coupon-variance | What is the variance of the coupon collector time for $n$ types, and its value for a die?
> $n^2\sum_{k \le n} 1/k^2 - nH_n$; for $n = 6$ it is $38.99$ (sd about 6.2). Sum of independent geometric variances $(1-p)/p^2$.

> [!question]- prob-classic-distinct-faces | Six rolls of a die. Expected number of distinct faces seen?
> $6(1 - (5/6)^6) \approx 3.99$. Indicator per face: it is missed with probability $(5/6)^6$.

> [!question]- prob-classic-birthday-23 | How many people are needed for a better than even chance that two share a birthday?
> $23$, giving $P \approx 0.507$. $\prod_{j<23}(1 - j/365) \approx 0.493$; there are $253$ pairs.

> [!question]- prob-classic-birthday-expected-pairs | Among 30 people, expected number of pairs sharing a birthday?
> $\binom{30}{2}/365 = 435/365 \approx 1.19$. Indicator for each pair, probability $1/365$.

> [!question]- prob-classic-birthday-share-mine | How many other people are needed for a better than even chance that someone shares your birthday?
> $253$. Need $1 - (364/365)^k > 1/2$, i.e. $k > \ln 2/(-\ln(364/365)) \approx 252.7$.

> [!question]- prob-classic-hat-check-expected | $n$ people pick up hats at random. Expected number who get their own?
> $1$. $n$ indicators each with probability $1/n$.

> [!question]- prob-classic-hat-check-variance | What is the variance of the number of fixed points of a random permutation of $n \ge 2$?
> $1$. $n \cdot \frac1n(1 - \frac1n)$ plus $n(n-1)$ pair covariances of $1/(n^2(n-1))$ each.

> [!question]- prob-classic-hat-check-none | Probability that nobody gets their own hat, for $n = 4$ and for large $n$?
> $3/8$ for $n = 4$ ($9$ derangements of $24$); $\sum_k (-1)^k/k! \to 1/e \approx 0.368$ in general.

> [!question]- prob-classic-hh-vs-ht | Expected fair-coin flips until HH, and until HT?
> HH: 6. HT: 4. After an H, a failed HT attempt keeps the H, a failed HH attempt resets to nothing.

> [!question]- prob-classic-n-heads-in-a-row | Expected flips of a fair coin until $n$ heads in a row?
> $2^{n+1} - 2$. $E_n = 2E_{n-1} + 2$ from first-step analysis; or $\sum_{k=1}^n 2^k$ by the casino argument.

> [!question]- prob-classic-biased-hh | A coin lands heads with probability $p$. Expected flips until HH?
> $(1+p)/p^2$. First-step: $E_0 = 1 + pE_1 + qE_0$, $E_1 = 1 + qE_0$. For $p = 1/3$ it is 12.

> [!question]- prob-classic-secretary-rule | What is the optimal strategy and success probability in the secretary problem for large $n$?
> Reject the first $n/e$ (about 37%), then take the first candidate better than all seen; success probability $\to 1/e \approx 0.368$.

> [!question]- prob-classic-secretary-three | Secretary problem with 3 candidates: best strategy and win probability?
> Skip the first, then take the first better one: wins $1/2$ (orders 213, 231, 312 out of 6).

> [!question]- prob-classic-die-two-rolls | You may roll a die and either keep it or roll once more (keeping the second). Expected value with optimal play?
> $17/4 = 4.25$. Re-roll 1, 2, 3 (below 3.5): $(4+5+6)/6 + \frac12 \cdot 3.5$.

> [!question]- prob-classic-die-three-rolls | Same game with up to three rolls?
> $14/3 \approx 4.67$. With two rolls left the value is 4.25, so keep only 5 or 6 on the first roll: $11/6 + \frac46 \cdot \frac{17}{4}$.

> [!question]- prob-classic-die-pay-to-reroll | You receive a die's face value but may pay \$1 to re-roll, as often as you like. Game value?
> $\$4$. $V = E[\max(X, V-1)]$; keeping $\ge 4$ gives $V = 15/6 + \frac12(V - 1)$, so $V = 4$.

> [!question]- prob-classic-uniform-sum-exceeds-one | Expected number of $U(0,1)$ draws until their sum exceeds 1?
> $e$. $P(N > n) = P(U_1 + \dots + U_n < 1) = 1/n!$, then sum the tails.

> [!question]- prob-classic-first-ace-position | Expected position of the first ace in a shuffled deck?
> $53/5 = 10.6$. Each of the 48 non-aces lies before all four aces with probability $1/5$, so $1 + 48/5$.

> [!question]- prob-classic-empty-boxes | $n$ balls go independently into $n$ boxes. Expected number of empty boxes?
> $n(1 - 1/n)^n \approx n/e$. Indicator per box; for $n = 10$ it is about $3.49$.

> [!question]- prob-classic-permutation-cycles | Expected number of cycles in a uniform random permutation of $n$?
> $H_n \approx \ln n$. Building the permutation by the Chinese restaurant process, element $k$ starts a new cycle with probability $1/k$.

## Further reading

- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 4.
- Frederick Mosteller, *Fifty Challenging Problems in Probability*.
- Timothy Crack, *Heard on the Street: Quantitative Questions from Wall Street Job Interviews*.
- Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), chapter 4 (indicators and linearity).
- Thomas Ferguson, "Who Solved the Secretary Problem?", *Statistical Science* 4 (1989).
