---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [markov-chains]
est_hours: 4
sources: [Grimmett and Stirzaker - Probability and Random Processes, Feller - An Introduction to Probability Theory and Its Applications Vol. 1, Zhou - A Practical Guide to Quantitative Finance Interviews, Shreve - Stochastic Calculus for Finance II]
---

# Random Walks and Gambler's Ruin

## TL;DR

- Fair walk from $i$ absorbed at 0 and $N$: $P(\text{hit } N) = i/N$ and the expected duration is $i(N-i)$.
- Biased walk with up-probability $p$, $q = 1-p$, $r = q/p$: $P(\text{hit } N) = (1 - r^i)/(1 - r^N)$; small edges compound brutally over long games.
- Against an infinitely rich house, a walk with $p < 1/2$ ever gains 1 unit with probability $p/q$; a fair walk hits every level with probability 1 but takes infinite expected time.
- Reflection principle: paths that touch level $a$ and end at $b$ biject with paths ending at the mirror image $2a - b$; this gives the distribution of the running max and the ballot theorem $(a-b)/(a+b)$.
- Scaled walks converge to Brownian motion: $S_{\lfloor nt \rfloor}/\sqrt{n} \to W_t$, and $P(\max_{s \le T} W_s \ge a) = 2P(W_T \ge a)$.

## Learning objectives

- Derive ruin probabilities for fair and biased walks, both by first-step analysis and by martingales.
- Derive the expected duration of the game.
- Apply the reflection principle, the ballot theorem and the first-return (Catalan) identities.
- Connect random walks to Brownian motion scaling and to recurrence in 1, 2 and 3 dimensions.

## Core concepts

### Setup

$S_n = S_0 + \sum_{k \le n} X_k$ with i.i.d. steps $X_k = +1$ with probability $p$ and $-1$ with probability $q = 1-p$.
With absorbing barriers at 0 and $N$ this is the gambler's ruin chain from [Markov Chains](10-Markov-Chains.md).

### Ruin probabilities

Let $h_i = P_i(\text{hit } N \text{ before } 0)$.
First-step analysis gives $h_i = p h_{i+1} + q h_{i-1}$ with $h_0 = 0$, $h_N = 1$.
The characteristic equation $p x^2 - x + q = 0$ has roots $1$ and $r = q/p$.

$$
h_i = \frac{1 - r^i}{1 - r^N} \;(p \ne q), \qquad h_i = \frac{i}{N} \;(p = q).
$$

Letting $N \to \infty$: if $p > q$, the probability of never being ruined from $i$ is $1 - r^i$; if $p \le q$, ruin is certain.
Equivalently, a walk with $p < q$ ever reaches $+b$ with probability $(p/q)^b$.

### Expected duration

Let $D_i$ be the expected number of steps: $D_i = 1 + p D_{i+1} + q D_{i-1}$, $D_0 = D_N = 0$.

$$
D_i = i(N - i) \;(p = q), \qquad D_i = \frac{i}{q - p} - \frac{N}{q - p}\cdot\frac{1 - r^i}{1 - r^N} \;(p \ne q).
$$

A fair walk from 0 takes $a^2$ steps on average to hit $\pm a$ (put $i = a$, $N = 2a$): variance grows linearly, so distance grows like $\sqrt{n}$.
With drift, the time to reach $+b$ from 0 (for $p > q$) has mean $b/(p - q)$ by Wald's identity.
The martingale derivations of both formulas are in [Martingales and Optional Stopping](12-Martingales-and-Optional-Stopping.md).

### Reflection principle

For a simple symmetric walk, the number of $n$-step paths from $a > 0$ to $b > 0$ that touch 0 equals the number of paths from $-a$ to $b$: reflect the segment before the first visit to 0.
Two consequences:

- Running maximum: for $a \ge 1$, $P(\max_{k \le n} S_k \ge a) = 2P(S_n > a) + P(S_n = a) = P(S_n \ge a) + P(S_n > a)$.
- Brownian version: $P(\max_{s \le T} W_s \ge a) = 2 P(W_T \ge a)$, so $\max_{s \le T} W_s \overset{d}{=} |W_T|$.

### Ballot theorem and first returns

If candidate A receives $a$ votes and B receives $b < a$, counted in uniformly random order, then

$$
P(\text{A strictly ahead throughout the count}) = \frac{a - b}{a + b}.
$$

Proof: the first vote must be for A; the bad paths starting with A that touch the diagonal biject by reflection with paths starting with B, and those number $\binom{a+b-1}{a}$; subtracting from $\binom{a+b-1}{a-1}$ and dividing by $\binom{a+b}{a}$ gives the result.
Related identities for the fair walk from 0: $P(S_1, \dots, S_{2n} \ne 0) = P(S_{2n} = 0) = \binom{2n}{n}/4^n \approx 1/\sqrt{\pi n}$, and the number of positive excursions of length $2n$ is the Catalan number $C_{n-1}$.

### Recurrence and dimension

The fair walk on $\mathbb{Z}$ and $\mathbb{Z}^2$ is recurrent: it returns to the origin with probability 1, but the expected return time is infinite (null recurrence).
On $\mathbb{Z}^3$ it is transient (Polya): the return probability is about $0.34$.
The reason is $\sum_n P(S_{2n} = 0)$: terms decay like $n^{-d/2}$, which is summable only for $d \ge 3$.

### Brownian scaling

By Donsker's theorem, $S_{\lfloor nt \rfloor}/(\sigma\sqrt{n})$ converges to standard Brownian motion.
Ruin probabilities carry over: Brownian motion with drift $\mu$ and volatility $\sigma$ started at $x$ hits $N$ before 0 with probability $(1 - e^{-2\mu x/\sigma^2})/(1 - e^{-2\mu N/\sigma^2})$, the continuous analogue of $r = q/p$ with $\ln r \approx -2\mu/\sigma^2$.
This is the bridge to [Brownian Motion](../04-Stochastic-Calculus/01-Brownian-Motion.md) and barrier option pricing.

## Worked examples

### Fair gambler's ruin

"I have \$20, bet \$1 on fair coin flips, and stop at \$0 or \$100."
"My wealth is a martingale and the game ends a.s., so $20 = 100 \cdot P(\text{win})$, giving $P = 1/5$."
"Duration: $D_i = i(N - i) = 20 \times 80 = 1600$ bets on average."
"Check the duration by the second martingale $S_n^2 - n$: $E[S_\tau^2] = 100^2 \cdot 0.2 = 2000$, and $2000 - 20^2 = 1600$."

### A small edge over a long game

"Same game but the house has an edge: $p = 0.49$. I start at 50 and target 100."
"$r = 0.51/0.49$ and $h_{50} = (1 - r^{50})/(1 - r^{100}) = 1/(1 + r^{50}) \approx 0.119$."
"A 1% edge per bet cuts my chance from $0.5$ to about $0.12$, because the edge compounds over roughly $N^2$ bets."
"Lesson for trading: tiny negative edges are fatal at small bet size relative to the target; bold play (few big bets) is optimal in a subfair game."
"Conversely, from $p = 0.4$, $i = 5$, $N = 10$ the success probability is only $0.116$ and the expected length is about $19.2$ bets."

### The drunk man at the cliff

"A drunk stands one step from a cliff edge; each step goes toward the edge with probability $1/3$, away with $2/3$. Probability he falls?"
"Relabel: he falls if a walk with down-probability $1/3$ ever goes down 1. The ruin probability against infinite wealth is $q/p$ with $q = 1/3$, $p = 2/3$, so $1/2$."
"First-step check: let $f$ be the probability of ever going down by 1. Then $f = \tfrac13 + \tfrac23 f^2$, since going up means he must come down twice independently."
"Roots $f = 1$ and $f = 1/2$; the minimal non-negative root is the answer when drift is away from the cliff, so $1/2$."

### Ballot problem

"A gets 6 votes and B gets 4, counted in random order. Probability A is strictly ahead at every point?"
"Ballot theorem: $(6-4)/(6+4) = 1/5$."
"Check by reflection: of $\binom{10}{4} = 210$ orders, 126 start with A; the bad ones starting with A biject with all orders starting with B, of which there are 84, so good $= 126 - 84 = 42$ and $42/210 = 1/5$."

### Running max of a walk and of Brownian motion

"For a 10-step fair walk, $P(\max \ge 3) = P(S_{10} \ge 3) + P(S_{10} > 3) = P(S_{10} \ge 4) + P(S_{10} \ge 4)$ since $S_{10}$ is even."
"$P(S_{10} \ge 4) = (\binom{10}{7} + \binom{10}{8} + \binom{10}{9} + \binom{10}{10})/1024 = 176/1024$, so the answer is $352/1024 = 11/32$."
"For Brownian motion on $[0,1]$: $P(\max \ge 1) = 2(1 - \Phi(1)) \approx 0.317$, roughly the probability of a 1-sigma move at the end, doubled."

## Pitfalls

- Plugging $p = 1/2$ into the biased formula; it is $0/0$ and the limit is $i/N$.
- Mixing up $r = q/p$ and $p/q$; sanity check that a favourable game ($p > q$) gives $h_i > i/N$.
- Claiming a fair walk hits $+1$ in finite expected time; it hits with probability 1 but $E[\tau] = \infty$, which is why optional stopping fails there.
- Applying the reflection principle to biased walks without a change of measure; the path bijection preserves probability only when $p = q$.
- Forgetting parity: a simple walk is at an even site at even times, which breaks "$2P(S_n > a)$" formulas off by a $P(S_n = a)$ term.
- Treating a Polya-recurrent walk as having a finite expected return time.

## Interview questions

> [!question]- prob-rw-fair-ruin-probability | A fair gambler starts with $i$ and plays until reaching $0$ or $N$. Probability of reaching $N$?
> $i/N$. Wealth is a martingale and the game ends a.s. with bounded wealth, so $i = N \cdot P(\text{hit } N)$.

> [!question]- prob-rw-fair-ruin-duration | Expected duration of a fair gambler's ruin game from $i$ with barriers 0 and $N$?
> $i(N-i)$. $S_n^2 - n$ is a martingale, so $E[\tau] = E[S_\tau^2] - i^2 = N^2 \cdot i/N - i^2$.

> [!question]- prob-rw-biased-ruin-probability | Up-probability $p \ne 1/2$, start $i$, barriers 0 and $N$. Probability of hitting $N$ first?
> $(1 - r^i)/(1 - r^N)$ with $r = q/p$. $r^{S_n}$ is a martingale, so $r^i = P(\text{hit } N) r^N + (1 - P)$.

> [!question]- prob-rw-house-edge-50-to-100 | You bet \$1 at a time with win probability $0.49$, starting at \$50 and stopping at \$0 or \$100. Roughly how likely are you to reach \$100?
> About $0.12$. $h_{50} = 1/(1 + (51/49)^{50})$ and $(51/49)^{50} \approx 7.4$.

> [!question]- prob-rw-drunk-man-cliff | A drunk is one step from a cliff and steps toward it with probability $1/3$. Probability he eventually falls?
> $1/2$. The probability of ever dropping one level is the minimal root of $f = q + p f^2$, which is $q/p = (1/3)/(2/3)$.

> [!question]- prob-rw-infinite-wealth-survival | Up-probability $p = 0.6$, you start with \$1 against an infinitely rich opponent. Probability you are never ruined?
> $1/3$. Ruin probability from $i$ is $(q/p)^i = 2/3$ when $p > q$.

> [!question]- prob-rw-hitting-time-plus-minus-a | Expected time for a fair walk from 0 to hit $+a$ or $-a$?
> $a^2$. Optional stopping on $S_n^2 - n$ with $S_\tau^2 = a^2$.

> [!question]- prob-rw-drift-hitting-time | A walk with $p > 1/2$ starts at 0. Expected time to first hit $+b$?
> $b/(p - q)$. Wald's identity: $E[S_\tau] = b = (p - q)E[\tau]$, valid because $E[\tau] < \infty$ when there is positive drift.

> [!question]- prob-rw-fair-hit-plus-one-expected-time | For a fair walk from 0, what is the expected time to first hit $+1$?
> Infinite, although the hit happens with probability 1. If it were finite, Wald would give $1 = E[S_\tau] = 0 \cdot E[\tau] = 0$.

> [!question]- prob-rw-ballot-theorem | A gets $a$ votes, B gets $b < a$, counted in random order. Probability A is strictly ahead throughout?
> $(a - b)/(a + b)$. By reflection, bad sequences that start with A biject with sequences that start with B.

> [!question]- prob-rw-no-return-to-zero | For a fair walk from 0, what is $P(S_1, \dots, S_{2n} \text{ all nonzero})$?
> $\binom{2n}{n}/4^n = P(S_{2n} = 0)$, about $1/\sqrt{\pi n}$. For $n = 2$ it is $3/8$. Proof via the ballot theorem summed over endpoints.

> [!question]- prob-rw-max-ten-step-walk | For a 10-step fair walk from 0, what is $P(\max_k S_k \ge 3)$?
> $11/32$. Reflection: $P(S_{10} \ge 3) + P(S_{10} > 3) = 2P(S_{10} \ge 4) = 2 \cdot 176/1024$.

> [!question]- prob-rw-brownian-running-max | What is $P(\max_{0 \le s \le 1} W_s \ge 1)$ for standard Brownian motion?
> $2(1 - \Phi(1)) \approx 0.317$. Reflect the path after the first hit of 1: $P(\max \ge a) = 2P(W_1 \ge a)$.

> [!question]- prob-rw-polya-recurrence | In which dimensions is the simple random walk recurrent?
> Dimensions 1 and 2 (null recurrent); transient for $d \ge 3$, with return probability about $0.34$ in 3D. $P(S_{2n} = 0) \sim c n^{-d/2}$ is summable only for $d \ge 3$.

## Further reading

- Grimmett and Stirzaker, *Probability and Random Processes*, sections 3.9-3.10 (random walks, reflection, ballot).
- William Feller, *An Introduction to Probability Theory and Its Applications*, Vol. 1, chapter III (fluctuations in coin tossing) and XIV (random walk and ruin).
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 5.
- Steven Shreve, *Stochastic Calculus for Finance II*, chapter 3 (reflection principle for Brownian motion).
