---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [conditional-probability-and-bayes]
est_hours: 5
sources: [Blitzstein and Hwang - Introduction to Probability 2nd ed ch 3-8, Ross - A First Course in Probability ch 4-5, Zhou - A Practical Guide to Quantitative Finance Interviews ch 4, Hull - Options Futures and Other Derivatives]
---

# Random Variables and Distributions

## TL;DR

- Know the table below cold: support, mean and variance of the ten or so named distributions, with the parameterisation stated (exponential and gamma by rate).
- Relationships are the real content: Bernoulli sums are binomial, binomial with $np$ fixed tends to Poisson, geometric sums are negative binomial, exponential sums are gamma, a uniform prior on a binomial $p$ gives a uniform count.
- Only the geometric (discrete) and exponential (continuous) are memoryless; the minimum of independent exponentials is exponential with the summed rate, and exponential $i$ wins with probability $\lambda_i/\sum\lambda_j$.
- Normal quantiles from memory: one-sided 1.645 (95%), 1.96 (97.5%), 2.326 (99%), 2.576 (99.5%), 3.09 (99.9%); $\pm1\sigma$ holds 68.3%, $\pm2\sigma$ 95.4%, $\pm3\sigma$ 99.73%.
- A lognormal price with zero drift in its mean has a median below its mean: $e^{\mu+\sigma^2/2}$ is the mean, $e^{\mu}$ is the median.

## Learning objectives

- State mean, variance and support of Bernoulli, binomial, geometric, negative binomial, Poisson, uniform, exponential, normal, lognormal, gamma and beta.
- Know the relationships (sum of exponentials is gamma, Poisson limit of binomial, beta-binomial).
- Use memorylessness of geometric and exponential variables.
- Compute quantiles of the normal from memory (1, 1.645, 1.96, 2.33, 3 sigma).

## Core concepts

### Random variables, PMF, PDF, CDF

A random variable is a function $X:\Omega\to\mathbb{R}$.
Its CDF $F(x) = P(X\le x)$ is nondecreasing, right-continuous, with limits 0 and 1, and always exists.
Discrete: PMF $p(x) = P(X=x)$; continuous: PDF $f = F'$ with $P(a<X\le b) = \int_a^b f$.
A density value is not a probability and can exceed 1.

Probability integral transform: if $F$ is continuous, $F(X)\sim U(0,1)$; conversely $F^{-1}(U)$ has CDF $F$.
That is inverse-transform sampling: $X = -\ln(U)/\lambda$ is $\text{Exp}(\lambda)$, since $P(-\ln U/\lambda > x) = P(U < e^{-\lambda x}) = e^{-\lambda x}$.

### The table

| Distribution | Support | PMF / PDF | Mean | Variance |
| :--- | :--- | :--- | :--- | :--- |
| Bernoulli$(p)$ | $\{0,1\}$ | $p^x(1-p)^{1-x}$ | $p$ | $p(1-p)$ |
| Binomial$(n,p)$ | $0,\dots,n$ | $\binom nk p^k(1-p)^{n-k}$ | $np$ | $np(1-p)$ |
| Geometric$(p)$, trials to first success | $1,2,\dots$ | $(1-p)^{k-1}p$ | $1/p$ | $(1-p)/p^2$ |
| Negative binomial$(r,p)$, trials to $r$-th success | $r,r+1,\dots$ | $\binom{k-1}{r-1}p^r(1-p)^{k-r}$ | $r/p$ | $r(1-p)/p^2$ |
| Poisson$(\lambda)$ | $0,1,\dots$ | $e^{-\lambda}\lambda^k/k!$ | $\lambda$ | $\lambda$ |
| Uniform$(a,b)$ | $[a,b]$ | $1/(b-a)$ | $(a+b)/2$ | $(b-a)^2/12$ |
| Exponential$(\lambda)$, rate | $[0,\infty)$ | $\lambda e^{-\lambda x}$ | $1/\lambda$ | $1/\lambda^2$ |
| Gamma$(k,\lambda)$, shape and rate | $(0,\infty)$ | $\lambda^k x^{k-1}e^{-\lambda x}/\Gamma(k)$ | $k/\lambda$ | $k/\lambda^2$ |
| Normal$(\mu,\sigma^2)$ | $\mathbb R$ | $\frac{1}{\sigma\sqrt{2\pi}}e^{-(x-\mu)^2/2\sigma^2}$ | $\mu$ | $\sigma^2$ |
| Lognormal, $\ln X\sim N(\mu,\sigma^2)$ | $(0,\infty)$ | $\frac{1}{x\sigma\sqrt{2\pi}}e^{-(\ln x-\mu)^2/2\sigma^2}$ | $e^{\mu+\sigma^2/2}$ | $(e^{\sigma^2}-1)e^{2\mu+\sigma^2}$ |
| Beta$(\alpha,\beta)$ | $[0,1]$ | $x^{\alpha-1}(1-x)^{\beta-1}/B(\alpha,\beta)$ | $\frac{\alpha}{\alpha+\beta}$ | $\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$ |

Parameterisation traps: some texts define the geometric as failures before the first success (mean $(1-p)/p$), the exponential and gamma by scale $\theta = 1/\lambda$, and the negative binomial as failures before the $r$-th success.
State yours before answering.

Derivation worth being able to do at the board: $\text{Var}(U(0,1)) = E[U^2] - E[U]^2 = 1/3 - 1/4 = 1/12$, and scaling by $b-a$ multiplies variance by $(b-a)^2$.

### Relationships

- Sum of $n$ independent Bernoulli$(p)$ is Binomial$(n,p)$.
- Binomial$(n,p)$ with $n\to\infty$, $np\to\lambda$ tends to Poisson$(\lambda)$, because $\binom nk p^k(1-p)^{n-k} \to e^{-\lambda}\lambda^k/k!$.
- Sum of $r$ independent Geometric$(p)$ is Negative binomial$(r,p)$.
- Independent Poissons add: Poisson$(\lambda_1)$ + Poisson$(\lambda_2)$ = Poisson$(\lambda_1+\lambda_2)$, and given the total $n$, the first is Binomial$(n,\lambda_1/(\lambda_1+\lambda_2))$.
- Thinning: if each event of a Poisson$(\lambda)$ count is kept independently with probability $p$, kept and discarded counts are independent Poisson$(\lambda p)$ and Poisson$(\lambda(1-p))$.
- Sum of $n$ independent Exp$(\lambda)$ is Gamma$(n,\lambda)$: the time of the $n$-th arrival of a Poisson process (see [Poisson Processes](13-Poisson-Processes.md)).
- Exponential is the continuous limit of the geometric: time steps of length $\Delta$ with success probability $\lambda\Delta$.
- $\sum_{i=1}^k Z_i^2 \sim \chi^2_k = \text{Gamma}(k/2, 1/2)$, mean $k$, variance $2k$.
- Order statistics of $n$ iid $U(0,1)$: $U_{(k)}\sim\text{Beta}(k, n+1-k)$ (see [Order Statistics and Extremes](08-Order-Statistics-and-Extremes.md)).
- Beta-binomial: if $p\sim\text{Beta}(\alpha,\beta)$ and $X\mid p\sim\text{Bin}(n,p)$, the posterior is $\text{Beta}(\alpha+X,\beta+n-X)$; with the uniform prior $\alpha=\beta=1$, $X$ is uniform on $\{0,\dots,n\}$.
- If $G_a\sim\text{Gamma}(a,\lambda)$ and $G_b\sim\text{Gamma}(b,\lambda)$ are independent, $G_a/(G_a+G_b)\sim\text{Beta}(a,b)$.
- Independent normals add: means add and variances add; products of independent lognormals are lognormal.

### Memorylessness

$P(X > s+t\mid X > s) = P(X > t)$ for all $s,t\ge0$.
For the exponential: $e^{-\lambda(s+t)}/e^{-\lambda s} = e^{-\lambda t}$.
The exponential is the only continuous memoryless distribution (the survival function must satisfy $G(s+t) = G(s)G(t)$), and the geometric is the only discrete one.
Consequences: the residual life of an exponential clock does not depend on how long you have waited; the minimum of independent exponentials $\text{Exp}(\lambda_i)$ is $\text{Exp}(\sum\lambda_i)$, and it is clock $i$ with probability $\lambda_i/\sum_j\lambda_j$, independent of the minimum's value.

### The normal and the lognormal

Standardise: $Z = (X-\mu)/\sigma$.

| $z$ | $\Phi(z)$ | $P(\lvert Z\rvert \le z)$ | Upper tail $1-\Phi(z)$ |
| :--- | :--- | :--- | :--- |
| 1 | 0.8413 | 0.6827 | 0.1587 |
| 1.645 | 0.9500 | 0.9000 | 0.0500 |
| 1.96 | 0.9750 | 0.9500 | 0.0250 |
| 2 | 0.9772 | 0.9545 | 0.0228 |
| 2.326 | 0.9900 | 0.9800 | 0.0100 |
| 2.576 | 0.9950 | 0.9900 | 0.0050 |
| 3 | 0.99865 | 0.9973 | 0.00135 |

Lognormal in finance: under geometric Brownian motion, $S_T = S_0\exp\big((\mu-\tfrac12\sigma^2)T + \sigma\sqrt T Z\big)$, so $E[S_T] = S_0e^{\mu T}$ while the median is $S_0e^{(\mu-\sigma^2/2)T}$.
The $-\tfrac12\sigma^2$ term is exactly the gap between mean and median in log space and reappears as volatility drag in [Inequalities and Limit Theorems](06-Inequalities-and-Limit-Theorems.md) and in [Ito's lemma](../04-Stochastic-Calculus/02-Ito-Integral-and-Ito-Lemma.md).

## Worked examples

### Example 1 - Poisson approximation

"A desk sends 1000 orders a day, each independently with a 0.1% chance of a fat-finger error. What is the probability of at least one error?"

The count is Binomial$(1000, 0.001)$ with mean 1, so approximate by Poisson(1).
$P(\ge1) \approx 1 - e^{-1} \approx 0.632$; the exact value $1 - 0.999^{1000} \approx 0.6323$ agrees to three decimals.
Rule of thumb to say aloud: Poisson is excellent when $n$ is large and $p$ small, with error of order $p$ (here $10^{-3}$).
Follow-up, probability of exactly two errors: $e^{-1}/2 \approx 0.184$.

### Example 2 - an exponential race

"Buy orders arrive as a Poisson process at 2 per second and sell orders at 1 per second, independently. What is the probability the next order is a buy, how long until the next order, and how long until you have seen at least one of each?"

Waiting times to the next buy and next sell are Exp(2) and Exp(1).
The next order is a buy with probability $2/(2+1) = 2/3$, and the wait for it is Exp(3) with mean $1/3$ second, independent of its side.
For at least one of each: $E[\max] = E[X]+E[Y]-E[\min] = \tfrac12 + 1 - \tfrac13 = 7/6$ seconds.
The memoryless way gives the same: after the first arrival (mean $1/3$), with probability $2/3$ it was a buy and you wait a fresh Exp(1) (mean 1), with probability $1/3$ a sell and you wait Exp(2) (mean $1/2$): $\tfrac13 + \tfrac23 + \tfrac16 = \tfrac76$.

### Example 3 - lognormal mean versus median

"A stock has zero expected return, 20% annual volatility and follows GBM. What is the probability it is above today's price in one year?"

Zero expected return means $E[S_1] = S_0$, so $\ln(S_1/S_0)\sim N(-\sigma^2/2, \sigma^2) = N(-0.02, 0.04)$.
$P(S_1 > S_0) = P(Z > 0.02/0.2) = \Phi(-0.1) \approx 0.460$.
The median price is $S_0e^{-0.02}\approx 0.980\,S_0$, below the mean, because the right skew of the lognormal pulls the mean up.
Traders get this wrong by saying "50%": a fair bet on the mean is not a coin flip on direction.

### Example 4 - Beta-binomial with a uniform prior

"Pick $p$ uniformly on $[0,1]$, then flip a $p$-coin $n$ times. What is the distribution of the number of heads?"

$P(X=k) = \binom nk\int_0^1 p^k(1-p)^{n-k}\,dp = \binom nk\frac{k!\,(n-k)!}{(n+1)!} = \frac{1}{n+1}$.
The no-integral argument (Bayes' billiard balls): throw $n+1$ uniform points on $[0,1]$; the first plays the role of $p$ and each of the others is a "head" if it falls to its left.
The first point's rank among the $n+1$ is uniform, so the number of heads is uniform on $\{0,\dots,n\}$.

## Pitfalls

- Mixing parameterisations (rate versus scale, trials versus failures) between the question and your formula.
- Treating a density value as a probability.
- Using Poisson when the count is bounded and $p$ is not small, or when events cluster (overdispersion: variance well above the mean).
- Forgetting that memorylessness means residual waiting time, not total waiting time; the inspection paradox makes the interval you land in longer than average.
- Assuming the lognormal median equals its mean, or that $E[e^X] = e^{E[X]}$; it is $e^{\mu+\sigma^2/2}$ for normal $X$.
- Using normal tail probabilities for real returns without comment: empirical tails are much fatter, so "3-sigma" days happen far more often than once in about three years.
- Quoting 1.96 for a one-sided 95% bound (that is 1.645) or 2.33 for a two-sided 99% interval (that is 2.576).

## Interview questions

> [!question]- prob-dist-geometric-rolls-to-six | How many rolls of a fair die do you expect to need to see a 6, and what is the variance?
> Mean 6, variance 30.
> Geometric with $p=1/6$: mean $1/p$, variance $(1-p)/p^2 = (5/6)\cdot36$.

> [!question]- prob-dist-negative-binomial-three-sixes | What are the mean and variance of the number of die rolls needed to see three 6s?
> Mean 18, variance 90.
> Sum of three independent Geometric$(1/6)$ variables: $3\cdot6$ and $3\cdot30$.

> [!question]- prob-dist-exponential-memoryless-bus | Bus gaps are exponential with mean 10 minutes. You have already waited 10 minutes. Expected additional wait?
> 10 minutes.
> Memorylessness: $P(X>s+t\mid X>s) = e^{-t/10}$, so the residual is again Exp with mean 10.

> [!question]- prob-dist-exponential-race-winner | Independent $X\sim\text{Exp}(2)$ and $Y\sim\text{Exp}(1)$. Find $P(X<Y)$ and $E[\min(X,Y)]$.
> $2/3$ and $1/3$.
> $P(X<Y) = \lambda_X/(\lambda_X+\lambda_Y)$; $\min\sim\text{Exp}(3)$.

> [!question]- prob-dist-exponential-max-expected | Independent $X\sim\text{Exp}(2)$ and $Y\sim\text{Exp}(1)$. Find $E[\max(X,Y)]$.
> $7/6$.
> $\max+\min = X+Y$, so $E[\max] = \tfrac12 + 1 - \tfrac13$.

> [!question]- prob-dist-poisson-limit-errors | 1000 independent orders each have a 0.1% error probability. Approximate P(at least one error).
> About $0.632 = 1-e^{-1}$.
> Poisson(1) approximation to Binomial(1000, 0.001); the exact value is $1-0.999^{1000}\approx0.6323$.

> [!question]- prob-dist-normal-quantiles | Give the standard normal quantiles for one-sided 95%, 97.5%, 99% and 99.5%.
> $1.645$, $1.960$, $2.326$, $2.576$.
> The 97.5% and 99.5% quantiles give the two-sided 95% and 99% intervals.

> [!question]- prob-dist-three-sigma-down-day | Daily returns are normal with 1% vol and zero mean. How often is a daily loss worse than 3%?
> About $0.135\%$ of days, roughly once every 741 trading days (about 3 years).
> $P(Z<-3)\approx0.00135$; in real markets such moves are much more frequent because returns are fat-tailed.

> [!question]- prob-dist-lognormal-mean-median | If $\ln X\sim N(0,1)$, what are the mean and median of $X$?
> Mean $e^{1/2}\approx1.649$, median $1$.
> $E[e^Z] = e^{\sigma^2/2}$ from the normal MGF; the median maps through the monotone exponential.

> [!question]- prob-dist-beta-binomial-uniform-count | Draw $p\sim U(0,1)$ and flip a $p$-coin $n$ times. What is $P(k \text{ heads})$?
> $1/(n+1)$ for every $k$.
> $\binom nk B(k+1,n-k+1) = 1/(n+1)$, or by the rank of one uniform among $n+1$.

> [!question]- prob-dist-probability-integral-transform | If $X$ has continuous CDF $F$, what is the distribution of $F(X)$, and how do you use it?
> Uniform on $(0,1)$.
> $P(F(X)\le u) = P(X\le F^{-1}(u)) = u$; inverting gives sampling, e.g. $-\ln(U)/\lambda\sim\text{Exp}(\lambda)$.

> [!question]- prob-dist-poisson-thinning-buys | Orders arrive Poisson at 10 per hour and each is a buy with probability 0.3 independently. What is P(no buys in an hour), and are buy and sell counts independent?
> $e^{-3}\approx0.050$; yes, independent.
> Thinning gives buys Poisson(3) and sells Poisson(7), independent of each other.

> [!question]- prob-dist-uniform-variance | Derive the variance of $U(a,b)$.
> $(b-a)^2/12$.
> For $U(0,1)$, $E[U^2]-E[U]^2 = 1/3-1/4 = 1/12$; an affine map $a+(b-a)U$ scales variance by $(b-a)^2$.

> [!question]- prob-dist-chi-square-moments | What are the mean and variance of $\sum_{i=1}^k Z_i^2$ for iid standard normals?
> Mean $k$, variance $2k$.
> $E[Z^2]=1$ and $E[Z^4]=3$, so $\text{Var}(Z^2)=2$; it is $\text{Gamma}(k/2,1/2)$.

## Further reading

- Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), chapters 3-5 and 8 (named distributions, universality of the uniform, beta-gamma relations).
- Sheldon Ross, *A First Course in Probability*, chapters 4-5.
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 4 (discrete and continuous distributions).
- John C. Hull, *Options, Futures, and Other Derivatives*, the lognormal property of stock prices.
- Next: [Expectation, Variance and Linearity](04-Expectation-Variance-and-Linearity.md).
