---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [expectation-variance-and-linearity]
est_hours: 4
sources: [Blitzstein and Hwang - Introduction to Probability 2nd ed ch 10, Grimmett and Stirzaker - Probability and Random Processes ch 5 and 7, Casella and Berger - Statistical Inference 2nd ed ch 5, Hoeffding 1963 - Probability inequalities for sums of bounded random variables]
---

# Inequalities and Limit Theorems

## TL;DR

- Markov: $P(X\ge a)\le E[X]/a$ for $X\ge0$; Chebyshev: $P(\lvert X-\mu\rvert\ge k\sigma)\le 1/k^2$; Chernoff: $P(X\ge a)\le\inf_{t>0}e^{-ta}E[e^{tX}]$, exponentially tight.
- Jensen: $\varphi(E[X])\le E[\varphi(X)]$ for convex $\varphi$; this is why options have time value and why geometric growth trails arithmetic mean return by about $\sigma^2/2$.
- The law of large numbers needs a finite mean; the sample mean of iid Cauchy variables is again Cauchy and never settles.
- CLT: $\sqrt n(\bar X_n-\mu)/\sigma\Rightarrow N(0,1)$ when $\sigma^2<\infty$; the error of a sum scales like $\sqrt n$, so a mean's error scales like $1/\sqrt n$.
- Delta method: $\sqrt n\,(g(\bar X_n)-g(\mu))\Rightarrow N(0, g'(\mu)^2\sigma^2)$.
- Mental tails: beyond $1\sigma$ one-sided is about 16%, $2\sigma$ 2.3%, $3\sigma$ 0.13%, $4\sigma$ $3\times10^{-5}$.

## Learning objectives

- State and use Markov, Chebyshev, Jensen, Cauchy-Schwarz and Chernoff bounds.
- Explain the weak and strong laws of large numbers and when they fail (Cauchy).
- Apply the central limit theorem and the delta method for approximations.
- Estimate tail probabilities in your head with the normal approximation.

## Core concepts

### Markov and Chebyshev

Markov: for $X\ge0$ and $a>0$, $a\,I_{\{X\ge a\}}\le X$ pointwise; take expectations to get $P(X\ge a)\le E[X]/a$.
Chebyshev: apply Markov to $(X-\mu)^2$:

$$
P(\lvert X-\mu\rvert\ge k\sigma)\le\frac{1}{k^2}.
$$

At least 75% of any distribution lies within $2\sigma$ and at least $8/9\approx88.9\%$ within $3\sigma$; for a normal the figures are 95.4% and 99.7%.
One-sided (Cantelli): $P(X-\mu\ge k\sigma)\le\frac{1}{1+k^2}$.
These bounds are distribution-free, which is their strength and why they are loose.

### Chernoff and Hoeffding

For any $t>0$, Markov applied to $e^{tX}$ gives $P(X\ge a)\le e^{-ta}M_X(t)$; optimise over $t$.
For independent $X_i\in[a_i,b_i]$ and $S = \sum X_i$, Hoeffding's inequality is

$$
P(S-E[S]\ge t)\le\exp\Big(-\frac{2t^2}{\sum_i(b_i-a_i)^2}\Big).
$$

For $n$ fair coin flips this is $P(S-n/2\ge t)\le e^{-2t^2/n}$: exponential decay in $t^2/n$, the same shape as the normal tail, which Chebyshev cannot see.
Moment generating functions are developed in [Generating Functions](07-Generating-Functions.md).

### Jensen and Cauchy-Schwarz

Jensen: for convex $\varphi$, $\varphi(E[X])\le E[\varphi(X)]$ (reverse for concave), with equality only if $X$ is constant or $\varphi$ is linear on its support.
Consequences worth quoting:

- $E[X^2]\ge E[X]^2$, i.e. variance is nonnegative.
- $E[1/X]\ge1/E[X]$ for $X>0$, so averaging prices and averaging inverse prices disagree (dollar-cost averaging).
- $E[\log X]\le\log E[X]$: the expected log return is below the log of the expected gross return; for GBM the growth rate is $\mu-\sigma^2/2$ (volatility drag).
- $E[(S-K)^+]\ge(E[S]-K)^+$: a call is worth at least its intrinsic value on the forward, because the payoff is convex ([Option Payoffs and Put-Call Parity](../05-Derivatives-and-Volatility/02-Option-Payoffs-and-Put-Call-Parity.md)).

Cauchy-Schwarz: $E[XY]^2\le E[X^2]E[Y^2]$.
Applied to centred variables it gives $\lvert\text{Cov}(X,Y)\rvert\le\sigma_X\sigma_Y$, i.e. $\lvert\rho\rvert\le1$, with equality iff $Y$ is an affine function of $X$.
Proof: $E[(X-tY)^2]\ge0$ for all $t$ is a quadratic in $t$ with nonpositive discriminant.

### Laws of large numbers

Weak law: for iid $X_i$ with mean $\mu$, $\bar X_n\to\mu$ in probability.
With finite variance, Chebyshev proves it in one line: $P(\lvert\bar X_n-\mu\rvert\ge\varepsilon)\le\sigma^2/(n\varepsilon^2)\to0$.
Strong law: $\bar X_n\to\mu$ almost surely, requiring only $E\lvert X\rvert<\infty$.
The difference: the weak law says a large deviation at a fixed large $n$ is unlikely; the strong law says that with probability one, the path eventually stays close forever.

Failure: if $X_i$ are iid standard Cauchy, $\bar X_n$ is again standard Cauchy for every $n$ (its characteristic function $e^{-\lvert t\rvert}$ satisfies $(e^{-\lvert t\rvert/n})^n = e^{-\lvert t\rvert}$).
Averaging does nothing because $E\lvert X\rvert=\infty$; single huge observations dominate the sum.
With a finite mean but infinite variance (Pareto tail index between 1 and 2) the LLN holds but convergence is slow and the CLT fails, with stable limits instead.
This matters for PnL of short-option or tail-risk strategies, where the sample mean can look excellent for years.

### Central limit theorem

For iid $X_i$ with mean $\mu$ and variance $\sigma^2<\infty$,

$$
\frac{\sum_{i=1}^n X_i - n\mu}{\sigma\sqrt n}\ \Rightarrow\ N(0,1).
$$

Berry-Esseen bounds the CDF error by $C\,E\lvert X-\mu\rvert^3/(\sigma^3\sqrt n)$ with an absolute constant $C$ below $0.5$, so skewed summands need larger $n$.
For integer-valued sums use the continuity correction: $P(S\ge k)\approx P(Z\ge(k-\tfrac12-n\mu)/(\sigma\sqrt n))$.
The same $\sqrt n$ scaling is why volatility scales with $\sqrt{\text{time}}$ for independent returns: 1% daily is about $1\%\cdot\sqrt{252}\approx15.9\%$ annualised.
The random-walk and Brownian-motion limits are in [Random Walks and Gambler's Ruin](11-Random-Walks-and-Gamblers-Ruin.md) and [Brownian Motion](../04-Stochastic-Calculus/01-Brownian-Motion.md).

### Delta method

If $\sqrt n(\hat\theta_n-\theta)\Rightarrow N(0,\tau^2)$ and $g$ is differentiable with $g'(\theta)\ne0$, then

$$
\sqrt n\big(g(\hat\theta_n)-g(\theta)\big)\Rightarrow N\big(0,\ g'(\theta)^2\tau^2\big).
$$

Derivation: first-order Taylor expansion $g(\hat\theta)\approx g(\theta)+g'(\theta)(\hat\theta-\theta)$.
Multivariate version: variance $\nabla g^\top\Sigma\nabla g$, used for ratios such as the Sharpe ratio ([Performance Metrics](../09-Alpha-Research-and-Portfolio/09-Performance-Metrics-and-Fundamental-Law.md)).

### Normal tails in your head

| Threshold | One-sided tail | Two-sided tail |
| :--- | :--- | :--- |
| $1\sigma$ | 15.9% | 31.7% |
| $2\sigma$ | 2.28% | 4.55% |
| $3\sigma$ | 0.135% | 0.27% |
| $4\sigma$ | $3.2\times10^{-5}$ | $6.3\times10^{-5}$ |
| $5\sigma$ | $2.9\times10^{-7}$ | $5.7\times10^{-7}$ |

Recipe: compute mean and standard deviation of the sum, convert the threshold to a $z$-score, read off the tail, and apply the continuity correction for discrete counts.

## Worked examples

### Example 1 - 10,000 coin flips

"You flip a fair coin 10,000 times. Roughly what is the probability of at least 5,100 heads?"

Mean 5000, standard deviation $\sqrt{10000\cdot\tfrac14} = 50$.
5100 is $2\sigma$ above the mean, so about $2.3\%$.
With continuity correction $z = 99.5/50 = 1.99$, tail $\approx 2.33\%$, which matches the exact binomial value $0.0233$.
Say aloud: "sd of a sum of fair coins is $\sqrt n/2$", then it is one step.

### Example 2 - comparing the bounds

"100 fair coin flips. Bound or estimate $P(\ge70 \text{ heads})$ with Chebyshev, Hoeffding and the CLT, and compare with the truth."

Mean 50, variance 25, deviation 20.
Chebyshev: $P(\lvert S-50\rvert\ge20)\le25/400 = 0.0625$, and the one-sided Cantelli bound is $25/425\approx0.059$.
Hoeffding: $e^{-2\cdot20^2/100} = e^{-8}\approx3.4\times10^{-4}$.
CLT with continuity correction: $z = 19.5/5 = 3.9$, tail $\approx4.8\times10^{-5}$.
Exact: $3.9\times10^{-5}$.
The polynomial bound is off by three orders of magnitude, the exponential bound by one, and the normal approximation is close; in the far tail the CLT's relative error grows, which is why large-deviation bounds exist.

### Example 3 - roulette

"You bet 1 dollar on red 1000 times at American roulette (18 red of 38). What is the probability you are ahead?"

Each bet is $+1$ with probability $p = 18/38$ and $-1$ otherwise, mean $2p-1 = -1/19$.
Expected total $-1000/19\approx-52.6$; per-bet variance $1-(1/19)^2$, so total sd $\approx31.6$.
Normal: $P(S>0)\approx\Phi(-52.6/31.6) = \Phi(-1.67)\approx4.8\%$.
Better, count wins $W\sim\text{Bin}(1000,p)$ with mean 473.7 and sd 15.8; ahead means $W\ge501$; continuity correction gives $z = (500.5-473.7)/15.8\approx1.70$ and $\approx4.5\%$, matching the exact $4.48\%$.
The house edge grows like $n$ while the noise grows like $\sqrt n$, so the probability of being ahead goes to zero.

### Example 4 - how precise is an estimated volatility?

"You estimate annual volatility from one year of daily returns (252 days). What is the standard error of the estimate?"

For normal returns the sample variance $\hat v$ has $\text{Var}(\hat v)\approx2\sigma^4/n$.
Volatility is $g(v) = \sqrt v$ with $g'(v) = 1/(2\sigma)$, so the delta method gives $\text{Var}(\hat\sigma)\approx\frac{2\sigma^4}{n}\cdot\frac{1}{4\sigma^2} = \frac{\sigma^2}{2n}$.
Relative standard error $1/\sqrt{2n} = 1/\sqrt{504}\approx4.5\%$: a 20% vol estimate is $20\%\pm0.9\%$ at one standard error.
Fat tails make it worse, since $\text{Var}(\hat v)$ involves the kurtosis.
Contrast with the mean: the standard error of the annual mean return is $\sigma$ itself for one year of data, which is why volatility is estimable and expected return is not.

### Example 5 - volatility drag

"A strategy has arithmetic mean return 10% a year and volatility 20%, following GBM. What is its typical compounded growth rate?"

$\log S_T$ has drift $(\mu-\sigma^2/2)T$, so the median growth rate is $10\%-\tfrac12(0.2)^2 = 8\%$ per year.
Jensen explains the sign: $\log$ is concave, so $E[\log(1+R)]\le\log(1+E[R])$.
Leverage scales $\mu$ linearly but the drag quadratically, which is the root of the Kelly criterion ([Kelly Criterion and Position Sizing](../11-Risk-and-Trading/01-Kelly-Criterion-and-Position-Sizing.md)).

## Pitfalls

- Using Chebyshev when the question wants an estimate; it is a worst-case bound.
- Applying Markov to a variable that can be negative.
- Getting Jensen backwards: convex $\varphi$ gives $E[\varphi(X)]\ge\varphi(E[X])$.
- Applying the CLT to heavy-tailed data (no finite variance) or to tiny samples of skewed data, and trusting normal approximations deep in the tail.
- Forgetting the continuity correction for small discrete counts.
- Assuming $\sqrt{T}$ scaling of volatility when returns are autocorrelated (mean reversion or momentum change it).
- Treating a sample mean that "has converged" as proof of a finite mean: Cauchy and short-volatility PnL both look stable until they do not.
- Confusing convergence in probability (weak law) with almost sure convergence (strong law).

## Interview questions

> [!question]- prob-limit-markov-bound | X is nonnegative with mean 10. What can you say about $P(X\ge50)$?
> $P(X\ge50)\le0.2$.
> Markov: $P(X\ge a)\le E[X]/a$; tight for $X$ taking values 0 and 50 only.

> [!question]- prob-limit-chebyshev-within-k-sd | What is the smallest fraction of any finite-variance distribution within 2 and 3 standard deviations of the mean?
> $3/4$ and $8/9$.
> Chebyshev: $P(\lvert X-\mu\rvert\ge k\sigma)\le1/k^2$.

> [!question]- prob-limit-jensen-call-intrinsic | Why is a European call worth at least $(F-K)^+$ in forward terms, with $F$ the forward?
> Jensen: the payoff is convex, so $E[(S_T-K)^+]\ge(E[S_T]-K)^+$.
> Under the forward measure $E[S_T]=F$; the gap is time value, which comes from convexity plus uncertainty.

> [!question]- prob-limit-cauchy-schwarz-correlation | Prove that correlation lies in [-1, 1].
> Cauchy-Schwarz on centred variables.
> $E[(\tilde X-t\tilde Y)^2]\ge0$ for all $t$; the discriminant condition is $\text{Cov}^2\le\text{Var}(X)\text{Var}(Y)$.

> [!question]- prob-limit-cauchy-sample-mean | What happens to the sample mean of n iid standard Cauchy variables as n grows?
> It stays standard Cauchy for every n; it never converges.
> The characteristic function $e^{-\lvert t\rvert}$ is invariant under averaging; the LLN fails because $E\lvert X\rvert=\infty$.

> [!question]- prob-limit-weak-vs-strong-law | What is the difference between the weak and strong laws of large numbers?
> Weak: $P(\lvert\bar X_n-\mu\rvert>\varepsilon)\to0$; strong: $\bar X_n\to\mu$ with probability 1.
> The strong law controls the whole tail of the path (eventually close forever); both need only $E\lvert X\rvert<\infty$ for iid data.

> [!question]- prob-limit-clt-coin-5100 | 10,000 fair coin flips. Approximate $P(\text{heads}\ge5100)$.
> About $2.3\%$.
> sd $=\sqrt{10000}/2 = 50$, so 5100 is $2\sigma$ above the mean; the exact value is $0.0233$.

> [!question]- prob-limit-bounds-seventy-heads | For 100 fair flips, compare Chebyshev, Hoeffding and the exact value of $P(\ge70\text{ heads})$.
> Chebyshev $\le0.0625$, Hoeffding $\le e^{-8}\approx3.4\times10^{-4}$, exact $\approx3.9\times10^{-5}$.
> Deviation 20 with variance 25; Hoeffding gives $e^{-2t^2/n}$.

> [!question]- prob-limit-roulette-ahead | You make 1000 one-dollar bets on red at American roulette. Probability of being ahead?
> About $4.5\%$.
> Wins $\sim\text{Bin}(1000,18/38)$, mean 473.7, sd 15.8; need $\ge501$, $z\approx1.70$.

> [!question]- prob-limit-hundred-dice-over-400 | 100 fair dice are rolled. Approximate the probability the sum exceeds 400.
> About $0.15\%$.
> Mean 350, sd $\sqrt{100\cdot35/12}\approx17.1$; $z = 50.5/17.1\approx2.96$; the exact value is $0.151\%$.

> [!question]- prob-limit-sqrt-time-vol | Daily vol is 1% with independent returns. Annualised vol over 252 days?
> About $15.9\%$.
> Variances add, so vol scales with $\sqrt{252}\approx15.87$.

> [!question]- prob-limit-poll-sample-size | How many respondents give a 95% margin of error of plus or minus 3 points on a proportion?
> About 1068.
> Worst case $p=1/2$: $n = (1.96\cdot0.5/0.03)^2\approx1067.1$, rounded up.

> [!question]- prob-limit-delta-method-vol-se | What is the relative standard error of a volatility estimated from n iid normal returns?
> About $1/\sqrt{2n}$; 4.5% for 252 daily returns.
> $\text{Var}(\hat v)\approx2\sigma^4/n$ and the delta method with $g=\sqrt{\cdot}$ gives $\text{Var}(\hat\sigma)\approx\sigma^2/(2n)$.

> [!question]- prob-limit-volatility-drag | GBM with 10% drift and 20% vol. What is the median compound growth rate?
> $8\%$ per year.
> $\log S_T$ has drift $\mu-\sigma^2/2$; Jensen on the concave log.

> [!question]- prob-limit-hoeffding-statement | State Hoeffding's inequality for bounded independent summands.
> $P(S-E[S]\ge t)\le\exp\big(-2t^2/\sum_i(b_i-a_i)^2\big)$ for $X_i\in[a_i,b_i]$.
> Chernoff bound with Hoeffding's lemma $E[e^{s(X-EX)}]\le e^{s^2(b-a)^2/8}$, optimised over $s$.

## Further reading

- Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), chapter 10 (inequalities, LLN, CLT).
- Geoffrey Grimmett and David Stirzaker, *Probability and Random Processes*, chapter 5 (generating functions and the CLT) and chapter 7 (convergence of random variables).
- George Casella and Roger Berger, *Statistical Inference* (2nd ed.), chapter 5 (convergence concepts, delta method).
- Wassily Hoeffding, "Probability inequalities for sums of bounded random variables", *Journal of the American Statistical Association* 58 (1963).
- Next: [Generating Functions](07-Generating-Functions.md) and [Heavy Tails and Extreme Value Theory](../02-Statistics-and-Econometrics/13-Heavy-Tails-and-Extreme-Value-Theory.md).
