---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [conditional-probability-and-bayes, expectation-variance-and-linearity]
est_hours: 5
sources: [Blitzstein and Hwang - Introduction to Probability (2nd ed.), Grimmett and Stirzaker - Probability and Random Processes, Norris - Markov Chains, Levin Peres and Wilmer - Markov Chains and Mixing Times]
---

# Markov Chains

## TL;DR

- A Markov chain is a memoryless state machine: $P(X_{n+1} = j \mid \text{past}) = P_{ij}$, and $n$-step probabilities are the entries of $P^n$.
- First-step analysis solves almost every interview chain: condition on the first move, write one linear equation per state, solve.
- A stationary distribution solves $\pi P = \pi$; for an irreducible finite chain it is unique and the mean return time to $i$ is $1/\pi_i$.
- For a random walk on an undirected graph, $\pi_v = \deg(v)/(2|E|)$, which gives the knight's-tour-style return times instantly.
- Pattern waiting times ("expected rolls until 66") are hitting times of the pattern-matching automaton; the state is the longest suffix that is a prefix of the target.

## Learning objectives

- Set up transition matrices and first-step equations for hitting probabilities and expected hitting times.
- Classify states (recurrent, transient, absorbing, periodic) and know which properties are class properties.
- Compute stationary distributions, use detailed balance, and explain convergence to stationarity.
- Solve "expected rolls until pattern" and Penney's game questions with a state machine.

## Core concepts

### Definitions

A sequence $X_0, X_1, \dots$ on a countable state space is a Markov chain with transition matrix $P$ if

$$
P(X_{n+1} = j \mid X_n = i, X_{n-1}, \dots, X_0) = P_{ij}.
$$

Rows of $P$ sum to 1.
Chapman-Kolmogorov: $P(X_{m+n} = j \mid X_m = i) = (P^n)_{ij}$, and a row vector of initial probabilities $\mu$ evolves as $\mu P^n$.

### First-step analysis

Let $A$ be a target set.
Hitting probabilities $h_i = P_i(\text{hit } A)$ and expected hitting times $k_i = E_i[T_A]$ satisfy

$$
h_i = \sum_j P_{ij} h_j \;(i \notin A), \quad h_i = 1 \;(i \in A); \qquad k_i = 1 + \sum_j P_{ij} k_j \;(i \notin A), \quad k_i = 0 \;(i \in A).
$$

Formally they are the minimal non-negative solutions, which matters only on infinite state spaces (gambler's ruin against an infinitely rich opponent).

### Absorbing chains and the fundamental matrix

Order the states as transient then absorbing, $P = \begin{pmatrix} Q & R \\ 0 & I \end{pmatrix}$.
The fundamental matrix $N = (I - Q)^{-1} = \sum_{n \ge 0} Q^n$ has $N_{ij}$ = expected visits to $j$ starting from $i$.
Expected steps to absorption are $N \mathbf{1}$ and absorption probabilities are $B = N R$.
This is first-step analysis in matrix form, and is how you would code it.

### Classification

- $j$ is accessible from $i$ if $(P^n)_{ij} > 0$ for some $n$; states that reach each other form communicating classes, and a chain with one class is irreducible.
- A state is recurrent if the chain returns to it with probability 1, transient otherwise; recurrent with finite mean return time is positive recurrent.
- The period of $i$ is $\gcd\{n : (P^n)_{ii} > 0\}$; period 1 is aperiodic.
- Recurrence, transience and period are class properties.
- A finite irreducible chain is always positive recurrent; transience and null recurrence need infinite state spaces (simple random walk on $\mathbb{Z}$ is null recurrent, on $\mathbb{Z}^3$ transient).
- An absorbing state has $P_{ii} = 1$.

### Stationary distributions and convergence

$\pi$ is stationary if $\pi P = \pi$ and $\sum_i \pi_i = 1$.
For an irreducible positive recurrent chain it exists, is unique, and

$$
\pi_i = \frac{1}{E_i[T_i^+]}, \qquad \frac{1}{n}\sum_{t < n} \mathbf{1}\{X_t = i\} \to \pi_i \text{ a.s.}
$$

If the chain is also aperiodic, $P^n_{ij} \to \pi_j$ for every $i$; the speed is governed by the second largest eigenvalue modulus of $P$.
Periodic chains have time averages but no limit: a walk on a bipartite graph alternates sides forever, and the lazy chain $(I + P)/2$ fixes this.

Detailed balance $\pi_i P_{ij} = \pi_j P_{ji}$ implies stationarity (sum over $i$) and means the chain is reversible.
It is the easiest way to find $\pi$ when it holds, and it is the design principle behind Metropolis-Hastings.
For a random walk on a connected undirected graph, $\pi_v \propto \deg(v)$ satisfies detailed balance, so $\pi_v = \deg(v)/(2|E|)$.
If $P$ is doubly stochastic (columns also sum to 1), $\pi$ is uniform.

### Pattern automata

To find the expected number of trials until a pattern $w$ appears, let the state be the longest suffix of the history that is a prefix of $w$ (the KMP failure-function idea).
The chain has $|w| + 1$ states and the answer is a hitting time.
The martingale "casino" method in [Martingales and Optional Stopping](12-Martingales-and-Optional-Stopping.md) gives the closed form: sum of $1/P(\text{prefix})$ over every prefix of $w$ that is also a suffix.

## Worked examples

### A two-state regime model

"Calm (C) goes to volatile (V) with probability $a = 0.1$ per day and V goes back with probability $b = 0.3$."
"Stationarity for two states is just flow balance: $\pi_C a = \pi_V b$, so $\pi = (b, a)/(a+b) = (0.75, 0.25)$."
"The volatile regime lasts a geometric number of days with mean $1/b \approx 3.3$, and the mean return time to calm is $1/\pi_C = 4/3$ days."
"The eigenvalues of $P$ are $1$ and $1 - a - b = 0.6$, so $P^n = \mathbf{1}\pi + 0.6^n(\cdot)$; the chain forgets its start at rate $0.6^n$, half-life about 1.4 days."

### Expected rolls until two sixes in a row

"States: 0 (last roll not a six) and 1 (last roll a six). Let $E_0, E_1$ be expected remaining rolls."
"From 0, one roll, then with $1/6$ I move to state 1 and with $5/6$ I stay: $E_0 = 1 + \tfrac{5}{6}E_0 + \tfrac16 E_1$."
"From 1, a six finishes and anything else resets: $E_1 = 1 + \tfrac56 E_0$."
"Substituting, $E_0 = 1 + \tfrac56 E_0 + \tfrac16 + \tfrac{5}{36}E_0$, so $E_0/36 = 7/6$ and $E_0 = 42$."
"Contrast with '1 then 2', which cannot overlap itself: a failed attempt never leaves useful progress except when the next roll is a 1, and the answer is $36$."
"The overlap of 66 with itself is what pushes the wait from 36 to 42."

### Knight's mean return time to a corner

"A knight moves uniformly at random among its legal moves from a corner. Expected moves to return?"
"This is a random walk on the knight graph, so $\pi_v = \deg(v)/\sum_u \deg(u)$."
"Degrees on the $8 \times 8$ board sum to $336$ (twice the 168 knight edges) and the corner has degree 2."
"So $\pi_{\text{corner}} = 2/336$ and the mean return time is $336/2 = 168$."
"The same argument for a king gives degree sum $420$ and corner degree 3, so $140$."

### Penney's game: HHT versus HTT

"Flip a fair coin until HHT or HTT appears. Let $a_s$ be the probability HHT wins from state $s$."
"From HH, H keeps us at HH and T completes HHT, so $a_{HH} = 1$."
"From H: H goes to HH, T goes to HT, so $a_H = \tfrac12 + \tfrac12 a_{HT}$."
"From HT: T completes HTT, H leaves the suffix H, so $a_{HT} = \tfrac12 a_H$."
"Solving, $a_H = \tfrac12 + \tfrac14 a_H$, so $a_H = 2/3$; the start state waits for the first H, so HHT wins with probability $2/3$."
"Both patterns have the same expected waiting time of 8, so faster-on-average and more-likely-first are different questions."

### Random walk on a cycle: which vertex is visited last?

"A walk on a cycle of $n$ vertices starts at 0. Which vertex is most likely to be the last one visited?"
"Vertex $k$ is last iff the walk reaches one of its neighbours, then travels the long way round to the other neighbour before stepping onto $k$."
"From a neighbour, that is gambler's ruin with distance 1 to $k$ and $n-2$ to the far neighbour, success probability $1/(n-1)$, independent of $k$."
"So every vertex other than the start is last with probability $1/(n-1)$: uniform, surprisingly."
"The expected cover time is $n(n-1)/2$, which is 15 for a hexagon."

## Pitfalls

- Using stationary probabilities as if they were probabilities at time $n$ for a periodic chain; they are only time averages.
- Forgetting the pattern-state reset: after HT fails on T in HTH, the state is not "empty" in general; use the longest suffix that is a prefix.
- Claiming a finite chain can be null recurrent or transient-only; every finite chain has at least one recurrent class.
- Writing $k_i = \sum_j P_{ij} k_j$ without the $+1$ for the step just taken.
- Assuming detailed balance holds for every chain; it characterises reversibility, and a chain with a one-way cycle violates it while still having a stationary law.
- Confusing expected waiting time with probability of occurring first (Penney's game).

## Interview questions

> [!question]- prob-mc-two-state-stationary | A two-state chain moves $1 \to 2$ with probability $a$ and $2 \to 1$ with probability $b$. What is its stationary distribution?
> $\pi = (b, a)/(a+b)$. Balance the flow across the cut: $\pi_1 a = \pi_2 b$. The non-unit eigenvalue $1-a-b$ sets the convergence speed.

> [!question]- prob-mc-mean-return-time | How is the mean return time to a state related to the stationary distribution?
> $E_i[T_i^+] = 1/\pi_i$ for an irreducible positive recurrent chain. Over a long run the chain spends fraction $\pi_i$ of time at $i$, so visits are $1/\pi_i$ steps apart on average.

> [!question]- prob-mc-graph-walk-stationary | What is the stationary distribution of a simple random walk on a connected undirected graph?
> $\pi_v = \deg(v)/(2|E|)$. It satisfies detailed balance: $\pi_u P_{uv} = \frac{\deg u}{2|E|}\frac{1}{\deg u} = \frac{1}{2|E|}$, symmetric in $u, v$.

> [!question]- prob-mc-knight-corner-return | A knight random-walks on a chessboard from a corner. Expected moves to return to that corner?
> $168$. Knight degrees sum to $336$ and the corner has degree 2, so $1/\pi = 336/2$.

> [!question]- prob-mc-king-corner-return | A king random-walks on a chessboard from a corner. Expected moves to return?
> $140$. Degree sum is $4 \cdot 3 + 24 \cdot 5 + 36 \cdot 8 = 420$ and the corner has degree 3.

> [!question]- prob-mc-clock-frog-return | A frog on a 12-hour clock face jumps to either neighbouring hour with probability $1/2$. Expected jumps to return to 12?
> $12$. The walk on a cycle is doubly stochastic, so $\pi$ is uniform, $\pi_{12} = 1/12$ and the mean return time is 12.

> [!question]- prob-mc-double-six-waiting | Expected number of die rolls until two consecutive sixes?
> $42$. First-step: $E_0 = 1 + \frac56 E_0 + \frac16 E_1$, $E_1 = 1 + \frac56 E_0$. Also $6 + 36$ from the prefix-suffix rule.

> [!question]- prob-mc-one-then-two-waiting | Expected number of die rolls until a 1 is immediately followed by a 2?
> $36$. The pattern "12" has no self-overlap, so the waiting time is $1/P(\text{12}) = 36$.

> [!question]- prob-mc-hhh-waiting | Expected number of fair coin flips until HHH?
> $14$. Prefix-suffix rule: $2 + 4 + 8$; in general $2^{n+1} - 2$ for $n$ heads in a row.

> [!question]- prob-mc-penney-hht-vs-htt | A fair coin is flipped until HHT or HTT appears. Probability HHT comes first?
> $2/3$. From H: $a_H = \frac12 + \frac12 a_{HT}$ and $a_{HT} = \frac12 a_H$, giving $a_H = 2/3$.

> [!question]- prob-mc-penney-thh-vs-hhh | Probability that THH appears before HHH with a fair coin?
> $7/8$. HHH wins only if the first three flips are HHH; any T earlier means THH must occur before the first HHH.

> [!question]- prob-mc-cycle-last-vertex | A simple random walk on a cycle of $n$ vertices starts at 0. Probability that vertex $k \ne 0$ is the last visited?
> $1/(n-1)$ for every $k$. After first hitting a neighbour of $k$, it must go round to the other neighbour before hitting $k$: gambler's ruin with odds $1:(n-2)$.

> [!question]- prob-mc-bipartite-periodicity | Why does a random walk on a bipartite graph not converge to its stationary distribution, and how do you fix it?
> It has period 2, so $P^n_{ij}$ alternates between 0 and positive values. Use the lazy chain $(I+P)/2$, which is aperiodic with the same $\pi$.

> [!question]- prob-mc-fundamental-matrix | For an absorbing chain with transient block $Q$ and transient-to-absorbing block $R$, how do you get expected absorption times and absorption probabilities?
> $N = (I - Q)^{-1}$ counts expected visits; times are $N\mathbf{1}$ and absorption probabilities are $NR$. It is first-step analysis in matrix form.

> [!question]- prob-mc-finite-chain-recurrence | Can a finite irreducible Markov chain be transient or null recurrent?
> No; it is always positive recurrent. The chain must spend infinite time somewhere, and irreducibility spreads that recurrence to every state with finite mean return time.

> [!question]- prob-mc-doubly-stochastic | What is the stationary distribution of an irreducible chain with a doubly stochastic transition matrix?
> Uniform. If columns sum to 1 then $\mathbf{1}P = \mathbf{1}$, so the uniform vector is stationary and by uniqueness it is the one.

## Further reading

- Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), chapter 11.
- Grimmett and Stirzaker, *Probability and Random Processes*, chapter 6.
- J. R. Norris, *Markov Chains*, chapter 1 (hitting times, recurrence, convergence).
- Levin, Peres and Wilmer, *Markov Chains and Mixing Times*, for convergence rates and cover times.
