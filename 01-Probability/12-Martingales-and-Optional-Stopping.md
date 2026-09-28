---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [random-walks-and-gamblers-ruin]
est_hours: 5
sources: [Grimmett and Stirzaker - Probability and Random Processes, Williams - Probability with Martingales, Shreve - Stochastic Calculus for Finance I, Li - A Martingale Approach to the Study of Occurrence of Sequence Patterns (Ann. Probab. 1980)]
---

# Martingales and Optional Stopping

## TL;DR

- A martingale is a fair game: $E[M_{n+1} \mid \mathcal{F}_n] = M_n$, so $E[M_n] = M_0$ for every fixed $n$.
- Optional stopping extends this to a stopping time $\tau$, $E[M_\tau] = M_0$, but only under conditions: $\tau$ bounded, or $E[\tau] < \infty$ with bounded increments, or $M_{n \wedge \tau}$ bounded.
- The walk martingales $S_n$, $S_n^2 - n$, $(q/p)^{S_n}$ and $S_n - n(p-q)$ solve gambler's ruin probabilities and durations in two lines each.
- Wald: $E[S_\tau] = E[X]\,E[\tau]$ when $E[\tau] < \infty$; e.g. rolling until the first six gives an expected total of $6 \times 3.5 = 21$.
- The casino (ABRACADABRA) argument gives pattern waiting times as a sum over self-overlaps: HTH takes 10 flips, HHT takes 8.

## Learning objectives

- Define martingales, sub- and supermartingales, and build them from random walks, likelihood ratios and conditional expectations.
- State the optional stopping theorem and the conditions that make it valid; produce the standard counterexamples.
- Use Wald's identities and the ABRACADABRA betting argument for pattern waiting times.
- Explain why no betting system beats a fair game, and use Doob's maximal inequality to bound barrier-hitting probabilities.

## Core concepts

### Definitions

Let $\mathcal{F}_n$ be the information at time $n$ (a filtration).
An adapted, integrable process $M_n$ is a

- martingale if $E[M_{n+1} \mid \mathcal{F}_n] = M_n$,
- submartingale if $E[M_{n+1} \mid \mathcal{F}_n] \ge M_n$ (favourable game),
- supermartingale if $E[M_{n+1} \mid \mathcal{F}_n] \le M_n$ (casino game from the player's side).

A convex function of a martingale is a submartingale by conditional Jensen: $|S_n|$, $S_n^2$ and $e^{S_n}$ are submartingales for a fair walk.

### Standard martingales

For i.i.d. steps $X_k$ with mean $\mu$, variance $\sigma^2$, and $S_n = \sum_{k \le n} X_k$:

| Martingale | Conditions | Typical use |
| :--- | :--- | :--- |
| $S_n - n\mu$ | $E\lvert X\rvert < \infty$ | Wald, drift hitting times |
| $(S_n - n\mu)^2 - n\sigma^2$ | $\sigma^2 < \infty$ | durations, Wald's second identity |
| $(q/p)^{S_n}$ | $\pm 1$ steps with $P(+1) = p$ | biased ruin probabilities |
| $e^{\theta S_n}/\varphi(\theta)^n$ | $\varphi(\theta) = E[e^{\theta X}] < \infty$ | exponential tilting, hitting time transforms |
| $E[Y \mid \mathcal{F}_n]$ | $E\lvert Y\rvert < \infty$ | Doob martingale: any conditional forecast |
| $\prod_k g(X_k)/f(X_k)$ | $X_k \sim f$ | likelihood ratio, change of measure |

The Doob martingale is why forecasts, fair prices and risk-neutral values are martingales: tomorrow's best estimate cannot be predicted to change today.
In a Polya urn (draw a ball, return it with another of the same colour), the fraction of red balls is a martingale.

### Stopping times and optional stopping

$\tau$ is a stopping time if $\{\tau = n\}$ is determined by information up to time $n$: "the first time the price hits 110" is one, "the day of the maximum price" is not.
The stopped process $M_{n \wedge \tau}$ is a martingale, so $E[M_{n \wedge \tau}] = M_0$ always.
Passing $n \to \infty$ needs one of:

1. $\tau \le K$ almost surely for some constant $K$;
2. $E[\tau] < \infty$ and $|M_{n+1} - M_n| \le C$;
3. $|M_{n \wedge \tau}| \le C$ for all $n$ and $\tau < \infty$ a.s.

Then $E[M_\tau] = M_0$.

Counterexample: a fair walk from 0 with $\tau$ = first hit of $+1$.
$\tau < \infty$ a.s. and $S_\tau = 1$, so $E[S_\tau] = 1 \ne 0$; every condition fails ($E[\tau] = \infty$, and the stopped walk is unbounded below).
The doubling strategy is the same trap: it wins 1 with probability 1 but needs unbounded credit, and the expected loss on the rare losing path exactly offsets the gains once any credit limit is imposed.

### No betting system beats a fair game

If you bet $H_n$ (chosen using $\mathcal{F}_{n-1}$) on the $n$-th fair increment, your wealth $\sum_k H_k (M_k - M_{k-1})$ is again a martingale (a martingale transform).
With bounded time or bounded credit, optional stopping then says the expected final wealth equals the initial wealth: stake sizing and quitting rules change the shape of the P&L distribution, never its mean.
In a subfair game (supermartingale), every such strategy has non-positive expected gain.

### Wald's identities

If $X_k$ are i.i.d. with mean $\mu$ and $\tau$ is a stopping time with $E[\tau] < \infty$:

$$
E[S_\tau] = \mu\, E[\tau], \qquad E[(S_\tau - \tau\mu)^2] = \sigma^2 E[\tau].
$$

### Pattern waiting times: the casino argument

Before each flip a new gambler arrives with \$1 and bets it all on the next letter of the pattern at fair odds, letting it ride through successive letters until they lose or the pattern completes.
The casino's net takings are a martingale, so at the stopping time $E[\text{paid in}] = E[\text{paid out}]$.
Paid in is $\tau$; paid out is deterministic: every gambler still alive holds $1/P(\text{their matched prefix})$.
Therefore

$$
E[\tau] = \sum_{\substack{k:\ \text{prefix of length } k \\ = \text{suffix of length } k}} \frac{1}{P(w_1 \dots w_k)} .
$$

For ABRACADABRA from 26 equiprobable letters, the prefixes that are also suffixes are ABRACADABRA, ABRA and A, so $E[\tau] = 26^{11} + 26^4 + 26$.
Conway's leading numbers extend the argument to Penney's game (which pattern appears first).

### Convergence and maximal inequality

An $L^1$-bounded martingale (in particular a non-negative one) converges almost surely.
Doob's maximal inequality: for a non-negative submartingale, $P(\max_{k \le n} M_k \ge a) \le E[M_n]/a$.
For a non-negative martingale started at $M_0$, $P(\sup_n M_n \ge a) \le M_0/a$, with equality for continuous paths that tend to 0, such as driftless geometric Brownian motion.

## Worked examples

### Biased gambler's ruin in two lines

"Walk with up-probability $p$, start $i$, barriers 0 and $N$. I want a martingale that is a function of $S_n$ only."
"Try $r^{S_n}$: $E[r^{S_{n+1}} \mid S_n] = r^{S_n}(p r + q/r)$, which equals $r^{S_n}$ when $r = q/p$."
"It is bounded up to $\tau$, so $r^i = h\, r^N + (1-h)$, giving $h = (1 - r^i)/(1 - r^N)$."
"For duration, $S_n - n(p - q)$ is a martingale and $E[\tau] < \infty$ with bounded steps, so $i = E[S_\tau] - (p-q)E[\tau] = Nh - (p-q)E[\tau]$."
"Hence $E[\tau] = (Nh - i)/(p - q)$, which matches the formula in [Random Walks and Gambler's Ruin](11-Random-Walks-and-Gamblers-Ruin.md)."

### HTH versus HHT by the casino argument

"For HTH, the prefixes that are also suffixes are HTH itself and H: $E[\tau] = 2^3 + 2^1 = 10$."
"For HHT, only the whole pattern: $E[\tau] = 8$."
"Intuition: HTH overlaps itself, so its occurrences cluster; the average number of occurrences per flip is the same $1/8$, so the gaps between clusters must be longer."
"The same rule gives HH $= 4 + 2 = 6$ and HT $= 4$, and for a die, 66 $= 36 + 6 = 42$."
"Senior follow-up: in ABRACADABRA the waiting time is $26^{11} + 26^4 + 26 = 3{,}670{,}344{,}487{,}444{,}778$ keystrokes."

### Wald's identity with dice

"Roll a die until the first six. What is the expected sum of all rolls, including the six?"
"$\tau$ is geometric with $E[\tau] = 6 < \infty$, so Wald gives $E[S_\tau] = 3.5 \times 6 = 21$."
"Trap: the non-six rolls are not uniform on 1..6 given that they are not six; they are uniform on 1..5 with mean 3."
"Check: $E[S_\tau] = 6 + E[\tau - 1] \times 3 = 6 + 15 = 21$, consistent."

### Polya urn

"Start with one red and one blue ball. Each step, draw a ball and return it with another of the same colour."
"With $R_n$ red out of $n+2$, $E[R_{n+1} \mid \mathcal{F}_n] = R_n + R_n/(n+2)$, so the fraction $R_n/(n+2)$ is a martingale."
"Any specific sequence with $k$ reds among $n$ draws has probability $k!\,(n-k)!/(n+1)!$, so $P(k \text{ reds drawn}) = \binom{n}{k}\frac{k!(n-k)!}{(n+1)!} = \frac{1}{n+1}$: uniform on $0, \dots, n$."
"The bounded martingale converges, and the limit fraction is $U(0,1)$; this is Bayesian updating of a uniform prior on a coin's bias in disguise."

### Probability a stock ever doubles

"Under a zero-rate risk-neutral measure the price is a non-negative martingale starting at \$100. Bound the probability it ever reaches \$200."
"Doob: $P(\sup S \ge 200) \le 100/200 = 1/2$."
"For driftless GBM the bound is exact: stop at 200 or at a low level $\epsilon$, apply optional stopping to the bounded stopped process, and let $\epsilon \to 0$; the path is continuous so there is no overshoot."
"This underlies one-touch option pricing: a zero-rate one-touch paying 1 at barrier $H > S_0$ on driftless GBM is worth $S_0/H$ (with infinite maturity)."

## Pitfalls

- Applying optional stopping to "first time the fair walk hits $+1$" or to a doubling strategy; check one of the three conditions every time.
- Using Wald's identity when $\tau$ depends on the future or when $E[\tau] = \infty$.
- Forgetting the compensator: $S_n^2$ is a submartingale, $S_n^2 - n$ is the martingale.
- Conditioning errors in Wald problems: rolls before the stopping event are not distributed like unconditional rolls.
- Treating "the price at its maximum" or "the last time the walk is at 0" as stopping times.
- Confusing martingale (fair given the past) with independent increments; martingale increments are uncorrelated but can be dependent, e.g. GARCH returns.

## Interview questions

> [!question]- prob-mart-square-compensator | For a fair $\pm 1$ walk, what must you subtract from $S_n^2$ to get a martingale?
> $n$. $E[S_{n+1}^2 \mid \mathcal{F}_n] = S_n^2 + 2S_n E[X] + E[X^2] = S_n^2 + 1$.

> [!question]- prob-mart-biased-exponential | For a $\pm 1$ walk with $P(+1) = p$, which function $r^{S_n}$ is a martingale?
> $r = q/p$. $E[r^{X}] = pr + q/r = 1$ has roots $r = 1$ and $r = q/p$.

> [!question]- prob-mart-ost-conditions | State sufficient conditions for $E[M_\tau] = M_0$.
> Any one of: $\tau$ bounded; $E[\tau] < \infty$ and bounded increments; the stopped process $M_{n \wedge \tau}$ uniformly bounded with $\tau < \infty$ a.s. (More generally, $M_{n\wedge\tau}$ uniformly integrable.)

> [!question]- prob-mart-ost-counterexample | Give a stopping time for a fair walk where optional stopping fails.
> $\tau$ = first hit of $+1$. It is finite a.s. and $S_\tau = 1 \ne 0 = S_0$; $E[\tau] = \infty$ and the stopped walk is unbounded below.

> [!question]- prob-mart-doubling-strategy | Why does the doubling (martingale) betting strategy not beat a fair game?
> It wins 1 almost surely only with unlimited credit and time. With any cap the stopped wealth is bounded, optional stopping applies, and the rare large loss exactly offsets the frequent small wins.

> [!question]- prob-mart-no-betting-system | Why can no stake-sizing or quitting rule create positive expected profit in a fair game?
> Wealth under any predictable stakes is a martingale transform, hence a martingale; with bounded time or credit, optional stopping gives $E[\text{final wealth}] = \text{initial wealth}$.

> [!question]- prob-mart-wald-die-until-six | You roll a die until the first six. What is the expected total of all rolls, including the six?
> $21$. Wald: $E[S_\tau] = E[X]E[\tau] = 3.5 \times 6$. Equivalently $6 + 5 \times 3$, since non-six rolls average 3.

> [!question]- prob-mart-wald-second-identity | State Wald's second identity and use it to get the expected exit time of a fair walk from $(-a, b)$.
> For mean-zero steps with variance $\sigma^2$ and $E[\tau] < \infty$: $E[S_\tau^2] = \sigma^2 E[\tau]$. Exit at $b$ w.p. $a/(a+b)$ gives $E[\tau] = b^2\frac{a}{a+b} + a^2\frac{b}{a+b} = ab$.

> [!question]- prob-mart-abracadabra | A monkey types uniformly random capital letters. Expected keystrokes until ABRACADABRA first appears?
> $26^{11} + 26^4 + 26$. Casino argument: the surviving gamblers at the end hold $26^{11}$ (full word), $26^4$ (ABRA) and $26$ (A).

> [!question]- prob-mart-hth-waiting | Expected fair-coin flips until HTH appears? And HHT?
> HTH takes $10 = 8 + 2$ (self-overlap on H); HHT takes $8$ (no self-overlap).

> [!question]- prob-mart-polya-urn-distribution | An urn has 1 red and 1 blue ball; each draw is returned with an extra ball of the same colour. After $n$ draws, what is the distribution of the number of reds drawn?
> Uniform on $\{0, \dots, n\}$. Each sequence with $k$ reds has probability $k!(n-k)!/(n+1)!$ and there are $\binom{n}{k}$ of them.

> [!question]- prob-mart-polya-urn-limit | In the Polya urn starting with one red and one blue ball, what is the limiting fraction of red?
> $U(0,1)$. The red fraction is a bounded martingale, so it converges a.s.; the limit is uniform because the counts are uniform at every $n$.

> [!question]- prob-mart-doob-maximal-doubling | A stock price is a non-negative martingale starting at 100. Upper bound on the probability it ever reaches 200?
> $1/2$. Doob's maximal inequality $P(\sup M \ge a) \le M_0/a$; it is attained by driftless GBM.

> [!question]- prob-mart-convex-submartingale | If $M_n$ is a martingale, what is $|M_n|$?
> A submartingale. Conditional Jensen with the convex function $|x|$: $E[|M_{n+1}| \mid \mathcal{F}_n] \ge |E[M_{n+1} \mid \mathcal{F}_n]| = |M_n|$.

> [!question]- prob-mart-likelihood-ratio | Under $X_k \sim f$ i.i.d., why is $L_n = \prod_{k \le n} g(X_k)/f(X_k)$ a martingale, and where does it appear in finance?
> $E_f[g(X)/f(X)] = \int g = 1$, so each factor has mean 1. It is the discrete Radon-Nikodym derivative behind change of measure and Girsanov.

> [!question]- prob-mart-drift-duration | For a $\pm 1$ walk with $p > q$ from 0, expected time to hit $+b$?
> $b/(p-q)$. $S_n - n(p-q)$ is a martingale and $E[\tau] < \infty$ with bounded steps, so $b = (p-q)E[\tau]$.

## Further reading

- Grimmett and Stirzaker, *Probability and Random Processes*, chapter 12.
- David Williams, *Probability with Martingales*, chapters 10-12 (including the ABRACADABRA exercise).
- Steven Shreve, *Stochastic Calculus for Finance I: The Binomial Asset Pricing Model*, chapter 2.
- S.-Y. R. Li, "A Martingale Approach to the Study of Occurrence of Sequence Patterns in Repeated Experiments", *Annals of Probability* 8 (1980).
