---
type: concept
track: [quant-trader, quant-research]
tier: advanced
status: solid
prereqs: [expectation-variance-and-linearity]
est_hours: 3
sources: [Grimmett and Stirzaker - Probability and Random Processes ch 5, Blitzstein and Hwang - Introduction to Probability 2nd ed ch 6, Feller - An Introduction to Probability Theory and Its Applications Vol 1 ch 11-13, Wilf - generatingfunctionology]
---

# Generating Functions

## TL;DR

- PGF $G_X(s) = E[s^X]$ for counts, MGF $M_X(t) = E[e^{tX}]$ for moments, characteristic function $\varphi_X(t) = E[e^{itX}]$ always exists.
- Independent sums multiply: $G_{X+Y} = G_XG_Y$, $M_{X+Y} = M_XM_Y$; the convolution becomes a product.
- Moments: $G'(1) = E[X]$, $G''(1) = E[X(X-1)]$, $M^{(k)}(0) = E[X^k]$; cumulants from $\log M$ add across independent summands.
- Random sums compose: $G_{S}(s) = G_N(G_X(s))$ for $S = \sum_{i=1}^N X_i$; compound Poisson has mean $\lambda E[X]$ and variance $\lambda E[X^2]$.
- Branching process extinction probability is the smallest root of $s = G(s)$ in $[0,1]$.
- Recurrences from first-step analysis become algebraic equations for the PGF: waiting for HH has mean 6 and variance 22.

## Learning objectives

- Use probability, moment and characteristic generating functions to get moments and distributions of sums.
- Solve random-sum (compound) problems with generating functions.
- Use generating functions for recurrences in dice and coin problems.

## Core concepts

### Probability generating functions

For $X\in\{0,1,2,\dots\}$, $G_X(s) = E[s^X] = \sum_k P(X=k)s^k$, convergent for $\lvert s\rvert\le1$.

- $G(1) = 1$, $P(X=k) = G^{(k)}(0)/k!$: the PGF determines the distribution.
- $G'(1) = E[X]$, $G''(1) = E[X(X-1)]$, so $\text{Var}(X) = G''(1)+G'(1)-G'(1)^2$.
- $G(0) = P(X=0)$ and $\frac{G(1)+G(-1)}{2} = P(X\text{ even})$.
- Roots-of-unity filter: $P(X\equiv0\bmod m) = \frac1m\sum_{j=0}^{m-1}G(\omega^j)$ with $\omega = e^{2\pi i/m}$.

Standard PGFs:

| Distribution | $G(s)$ |
| :--- | :--- |
| Bernoulli$(p)$ | $1-p+ps$ |
| Binomial$(n,p)$ | $(1-p+ps)^n$ |
| Poisson$(\lambda)$ | $e^{\lambda(s-1)}$ |
| Geometric$(p)$ on $\{1,2,\dots\}$ | $\dfrac{ps}{1-(1-p)s}$ |
| Fair die | $\frac16(s+s^2+\dots+s^6)$ |

### Moment generating functions and cumulants

$M_X(t) = E[e^{tX}]$, when finite on an open interval around 0.
Then $M^{(k)}(0) = E[X^k]$, and the MGF determines the distribution (uniqueness theorem).
Standard MGFs: normal $e^{\mu t+\sigma^2t^2/2}$, Exp$(\lambda)$ $\frac{\lambda}{\lambda-t}$ for $t<\lambda$, Poisson $e^{\lambda(e^t-1)}$, Gamma$(k,\lambda)$ $\big(\frac{\lambda}{\lambda-t}\big)^k$.

Cumulant generating function $K(t) = \log M(t)$: $K'(0) = E[X]$, $K''(0) = \text{Var}(X)$, $K'''(0) = E[(X-\mu)^3]$, and $K^{(4)}(0) = E[(X-\mu)^4]-3\sigma^4$.
Cumulants of independent sums add.
So for a sum of $n$ iid variables, skewness scales as $1/\sqrt n$ and excess kurtosis as $1/n$, which quantifies how fast the CLT kicks in.
The normal is the only distribution with all cumulants beyond the second equal to zero; a Poisson$(\lambda)$ has every cumulant equal to $\lambda$.

When the MGF fails:

- Cauchy: no moments, $M(t) = \infty$ for $t\ne0$, but $\varphi(t) = e^{-\lvert t\rvert}$.
- Lognormal: every moment $E[X^k] = e^{k\mu+k^2\sigma^2/2}$ is finite, yet $M(t) = \infty$ for all $t>0$, and its moments do not determine the distribution (other distributions share them).
  Heavy right tails (and heavy-tailed PnL) break MGF arguments; switch to characteristic functions.

Characteristic functions: $\varphi(t) = E[e^{itX}]$ always exists with $\lvert\varphi\rvert\le1$, determines the distribution, and Levy's continuity theorem turns convergence of $\varphi_n$ into convergence in distribution.
Fourier option pricing is built on this ([Finite Differences and Fourier Pricing](../05-Derivatives-and-Volatility/11-Finite-Differences-and-Fourier-Pricing.md)).

CLT sketch: for iid mean-zero, variance-one $X_i$, $K_X(t) = t^2/2 + O(t^3)$, so the standardised sum has $K(t) = nK_X(t/\sqrt n) = t^2/2 + O(n^{-1/2})\to t^2/2$, the normal CGF (use $\varphi$ instead of $M$ to avoid assuming the MGF exists).

### Random sums

Let $N$ be independent of iid $X_i$, and $S = \sum_{i=1}^N X_i$.
Conditioning on $N$: $E[s^S\mid N] = G_X(s)^N$, so

$$
G_S(s) = G_N\big(G_X(s)\big), \qquad M_S(t) = G_N\big(M_X(t)\big).
$$

Differentiating recovers $E[S] = E[N]E[X]$ and $\text{Var}(S) = E[N]\text{Var}(X)+\text{Var}(N)E[X]^2$ from [Expectation, Variance and Linearity](04-Expectation-Variance-and-Linearity.md).
Compound Poisson ($N\sim$ Poisson$(\lambda)$): $G_S(s) = e^{\lambda(G_X(s)-1)}$, with $E[S] = \lambda E[X]$ and $\text{Var}(S) = \lambda E[X^2]$.
Thinning is the special case $X\sim$ Bernoulli$(p)$: $G_S(s) = e^{\lambda p(s-1)}$, Poisson$(\lambda p)$.
Compound Poisson is the standard model for aggregate order volume, insurance claims and jump components ([Jump Processes and Levy Models](../04-Stochastic-Calculus/08-Jump-Processes-and-Levy-Models.md)).

### Branching processes

Each individual independently has offspring count with PGF $G$ and mean $m = G'(1)$.
The generation-$n$ size $Z_n$ has PGF $G_n = G\circ G\circ\dots\circ G$ ($n$ times), and $E[Z_n] = m^n$.
Extinction probability $q = \lim P(Z_n=0)$ is the smallest root of $s = G(s)$ in $[0,1]$: condition on the first generation, each of whose lines must die out independently.
$q = 1$ if $m\le1$ (excluding the trivial case of exactly one child always), and $q<1$ if $m>1$.

### Recurrences

First-step analysis turns a waiting-time problem into a linear equation for its PGF.
For a sequence $a_n$ defined by a linear recurrence, $A(s) = \sum a_ns^n$ is rational, and partial fractions give closed forms and asymptotics (the approach of [Markov Chains](10-Markov-Chains.md) and [Random Walks and Gambler's Ruin](11-Random-Walks-and-Gamblers-Ruin.md), made mechanical).
Renewal example: with $u_n = P(\text{partial sums of die rolls hit } n \text{ exactly})$, $u_n = \frac16\sum_{k=1}^6u_{n-k}$ and $U(s) = 1/(1-G(s))$; the pole at $s=1$ gives $u_n\to1/E[X] = 2/7$.

## Worked examples

### Example 1 - dice sums and Sicherman dice

"Find the distribution of the sum of two dice. Is there another pair of dice with positive integer faces giving the same distribution?"

$(s+s^2+\dots+s^6)^2 = s^2+2s^3+3s^4+4s^5+5s^6+6s^7+5s^8+\dots+s^{12}$, giving counts $1,2,\dots,6,\dots,1$ out of 36.
Factor: $s+\dots+s^6 = s(1+s)(1+s+s^2)(1-s+s^2)$.
The square has two copies of each factor; redistribute them so each die still has $G(1) = 6$ faces and a factor $s$ (no zero face): one die gets $s(1+s)(1+s+s^2) = s+2s^2+2s^3+s^4$, the other $s(1+s)(1+s+s^2)(1-s+s^2)^2 = s+s^3+s^4+s^5+s^6+s^8$.
So faces $\{1,2,2,3,3,4\}$ and $\{1,3,4,5,6,8\}$ give exactly the same sum distribution, and this is the only alternative.

### Example 2 - compound Poisson volume

"Trades arrive at 2 per minute (Poisson) and each has a size uniform on $\{1,\dots,6\}$ lots, independent. Mean and variance of volume in one minute?"

$E[X] = 3.5$ and $E[X^2] = 91/6$.
$E[S] = \lambda E[X] = 7$ lots and $\text{Var}(S) = \lambda E[X^2] = 91/3\approx30.3$.
Note the variance uses $E[X^2]$, not $\text{Var}(X)$: randomness in the count adds $\text{Var}(N)E[X]^2 = \lambda E[X]^2$ on top of $\lambda\text{Var}(X)$.
The full distribution is $G_S(s) = \exp\big(2(\tfrac16(s+\dots+s^6)-1)\big)$ if a follow-up asks for $P(S=0) = e^{-2}$.

### Example 3 - extinction of a branching process

"Each cell dies with probability 1/4, survives unchanged with probability 1/4, or splits in two with probability 1/2. Starting with one cell, what is the probability the population dies out?"

$G(s) = \tfrac14+\tfrac14s+\tfrac12s^2$, with mean $m = 1.25>1$, so extinction is not certain.
Solve $s = G(s)$: $2s^2-3s+1 = 0$, roots $s = 1/2$ and $s = 1$.
The extinction probability is the smaller root, $q = 1/2$.
Starting with $k$ cells it is $q^k = 2^{-k}$, since the lines are independent.

### Example 4 - waiting for HH

"Flip a fair coin until you see two heads in a row. Find the mean and variance of the number of flips."

First-step analysis on the PGF $G(s) = E[s^T]$: the first flip is T (prob $\tfrac12$, restart after 1 flip), or HT (prob $\tfrac14$, restart after 2), or HH (prob $\tfrac14$, done in 2):

$$
G(s) = \tfrac12sG(s)+\tfrac14s^2G(s)+\tfrac14s^2 \quad\Rightarrow\quad G(s) = \frac{s^2/4}{1-s/2-s^2/4}.
$$

$G'(1) = 6$ and $\text{Var}(T) = G''(1)+G'(1)-G'(1)^2 = 22$.
For HT the answer is a sum of two independent Geometric$(1/2)$ (wait for H, then wait for T), mean 4 and variance 4: HH self-overlaps, so a failure after H sends you back to the start.

### Example 5 - even number of heads

"$n$ flips of a coin with $P(H) = p$. Probability of an even number of heads?"

$G(s) = (1-p+ps)^n$, and $P(\text{even}) = \frac{G(1)+G(-1)}{2} = \frac{1+(1-2p)^n}{2}$.
For a fair coin it is exactly $1/2$ for all $n\ge1$; for $p = 1/4$, $n = 4$ it is $(1+2^{-4})/2 = 17/32$.
The same filter with cube roots of unity shows the sum of three dice is divisible by 3 with probability $1/3$, because each die is uniform mod 3.

## Pitfalls

- Using the MGF for heavy-tailed variables (lognormal, Pareto, Cauchy) where it is infinite; use the characteristic function.
- Believing that all moments determine a distribution: they do not for the lognormal.
- Evaluating PGF moments at $s = 0$ instead of $s = 1$, or forgetting $G''(1)$ is the factorial moment $E[X(X-1)]$.
- Composing random sums in the wrong order: $G_N(G_X(s))$, not $G_X(G_N(s))$.
- Applying the product rule for sums to dependent summands.
- Taking the larger root, 1, as the extinction probability when $m>1$.
- In pattern-waiting problems, restarting from scratch after a partial match without checking self-overlap.

## Interview questions

> [!question]- prob-gf-pgf-moments | How do you get the mean and variance of X from its PGF G?
> $E[X] = G'(1)$ and $\text{Var}(X) = G''(1)+G'(1)-G'(1)^2$.
> $G''(1) = E[X(X-1)]$, the second factorial moment.

> [!question]- prob-gf-poisson-sum | Use MGFs to show the sum of independent Poisson($\lambda$) and Poisson($\mu$) is Poisson.
> It is Poisson$(\lambda+\mu)$.
> $e^{\lambda(e^t-1)}e^{\mu(e^t-1)} = e^{(\lambda+\mu)(e^t-1)}$ and the MGF determines the distribution.

> [!question]- prob-gf-normal-mgf | What is the MGF of $N(\mu,\sigma^2)$, and what is $E[e^Z]$ for standard normal Z?
> $e^{\mu t+\sigma^2t^2/2}$; $E[e^Z] = e^{1/2}$.
> Complete the square in the Gaussian integral; set $t = 1$.

> [!question]- prob-gf-random-sum-composition | S is the sum of N iid copies of X, with N independent of them. What is the PGF of S?
> $G_S(s) = G_N(G_X(s))$.
> Given $N=n$ it is $G_X(s)^n$; average over $N$.

> [!question]- prob-gf-compound-poisson-moments | Trades arrive Poisson at rate 2 per minute with sizes uniform on 1 to 6 lots. Mean and variance of one-minute volume?
> Mean 7, variance $91/3\approx30.3$.
> Compound Poisson: $\lambda E[X]$ and $\lambda E[X^2]$ with $E[X^2] = 91/6$.

> [!question]- prob-gf-poisson-thinning-pgf | Each event of a Poisson($\lambda$) count is kept independently with probability p. Distribution of the kept count?
> Poisson$(\lambda p)$.
> $G_N(G_X(s)) = e^{\lambda((1-p+ps)-1)} = e^{\lambda p(s-1)}$.

> [!question]- prob-gf-branching-extinction | Offspring are 0, 1 or 2 with probabilities 1/4, 1/4, 1/2. Starting from one individual, extinction probability?
> $1/2$.
> Smallest root in $[0,1]$ of $s = \tfrac14+\tfrac14s+\tfrac12s^2$, i.e. of $2s^2-3s+1 = 0$.

> [!question]- prob-gf-branching-poisson-two | Offspring are Poisson(2). Extinction probability?
> About $0.203$.
> Smallest root of $s = e^{2(s-1)}$; iterate $q\leftarrow e^{2(q-1)}$ from 0.

> [!question]- prob-gf-even-heads | n flips with P(H) = p. Probability of an even number of heads?
> $\frac{1+(1-2p)^n}{2}$.
> $\frac{G(1)+G(-1)}{2}$ with $G(s) = (1-p+ps)^n$.

> [!question]- prob-gf-sicherman-dice | Find two dice with positive integer faces, not both standard, whose sum has the same distribution as two standard dice.
> Faces $\{1,2,2,3,3,4\}$ and $\{1,3,4,5,6,8\}$ (Sicherman dice).
> Factor $s+\dots+s^6 = s(1+s)(1+s+s^2)(1-s+s^2)$ and move both $(1-s+s^2)$ factors to one die.

> [!question]- prob-gf-hh-waiting-time | Fair coin: mean and variance of the number of flips until HH?
> Mean 6, variance 22.
> First-step analysis gives $G(s) = \frac{s^2/4}{1-s/2-s^2/4}$; differentiate at 1.

> [!question]- prob-gf-ht-waiting-time | Fair coin: mean and variance of the number of flips until HT?
> Mean 4, variance 4.
> Wait for the first H (Geometric(1/2)), then for the first T after it (another Geometric(1/2)); independent, so means and variances add.

> [!question]- prob-gf-three-dice-divisible-by-three | Three dice are rolled. Probability the sum is divisible by 3?
> $1/3$.
> Each die is uniform mod 3, so the sum is uniform mod 3; the roots-of-unity filter $\frac13\sum_j G(\omega^j)$ gives the same because $G(\omega) = G(\omega^2) = 0$.

> [!question]- prob-gf-cauchy-characteristic-function | Does a Cauchy variable have an MGF? What replaces it?
> No; $E[e^{tX}] = \infty$ for $t\ne0$. Use the characteristic function $e^{-\lvert t\rvert}$.
> The characteristic function always exists and shows the mean of $n$ iid Cauchys is Cauchy.

> [!question]- prob-gf-lognormal-moments-no-mgf | Does a lognormal variable have all moments? Does it have an MGF?
> All moments are finite, $E[X^k] = e^{k\mu+k^2\sigma^2/2}$, but the MGF is infinite for every $t>0$.
> $e^{tx}$ outgrows the lognormal tail; the moments also fail to determine the distribution.

> [!question]- prob-gf-cumulant-scaling | How do skewness and excess kurtosis of a sum of n iid variables scale with n?
> Skewness as $1/\sqrt n$, excess kurtosis as $1/n$.
> Cumulants add: $\kappa_3\to n\kappa_3$ over $(n\sigma^2)^{3/2}$, and $\kappa_4\to n\kappa_4$ over $(n\sigma^2)^2$.

> [!question]- prob-gf-die-sum-hits-n | You keep rolling a die and track the running total. For large n, what is the probability the total ever equals exactly n?
> $2/7$.
> Renewal: $U(s) = 1/(1-G(s))$ has a simple pole at 1 with residue giving $u_n\to1/E[X] = 1/3.5$.

## Further reading

- Geoffrey Grimmett and David Stirzaker, *Probability and Random Processes*, chapter 5 (generating functions, random sums, branching processes, characteristic functions).
- Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), chapter 6 (moments and MGFs).
- William Feller, *An Introduction to Probability Theory and Its Applications*, Vol. 1, chapters 11-13 (generating functions, compound distributions, recurrent events).
- Herbert Wilf, *generatingfunctionology* (combinatorial generating functions).
- Next: [Markov Chains](10-Markov-Chains.md) and [Poisson Processes](13-Poisson-Processes.md).
