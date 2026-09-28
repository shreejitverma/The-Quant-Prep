---
type: problem-set
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [black-scholes-derivation]
est_hours: 5
sources: [Zhou - A Practical Guide to Quantitative Finance Interviews chapter 5, Joshi Denson and Downes - Quant Job Interview Questions and Answers, Shreve - Stochastic Calculus for Finance II (Springer 2004) chapters 3-4, Karatzas and Shreve - Brownian Motion and Stochastic Calculus (Springer 1991) chapter 2]
---

# Stochastic Calculus Problem Set

## TL;DR

- Five tools solve almost every question: Gaussian facts ($W_t \sim N(0,t)$, $\text{Cov} = \min(s,t)$), Ito's lemma, the isometry, optional stopping on $W$, $W^2 - t$ or $e^{\theta W - \theta^2 t/2}$, and the reflection principle.
- Moments: $E[W_t^{2k}] = (2k-1)!!\,t^k$, $E[e^{aW_t}] = e^{a^2t/2}$.
- Martingale test for $f(t, W_t)$: $f_t + \tfrac12 f_{xx} = 0$ (plus integrability).
- Barriers: driftless uses $W$ and $W^2 - t$; drift $\mu$, vol $\sigma$ uses $e^{-2\mu X/\sigma^2}$.
- Always sanity-check: an Ito integral has mean zero, a variance is positive, a probability is in $[0,1]$, and limits ($\mu \to 0$, $t \to 0$) match known cases.

## Learning objectives

- Solve standard Ito, Brownian motion and SDE interview questions quickly and rigorously.

## Core concepts

This set drills the material of [Brownian Motion](01-Brownian-Motion.md), [Ito's Lemma](02-Ito-Integral-and-Ito-Lemma.md), [SDEs](03-Stochastic-Differential-Equations.md) and [Black-Scholes](07-Black-Scholes-Derivation.md).
The toolkit, in the order to reach for it:

| Question shape | First tool | Key identity |
| :--- | :--- | :--- |
| Linear functional of the path | Gaussianity | mean 0, variance from $\min(s,t)$ or isometry |
| $E[f(W_t)]$ for polynomial or exponential $f$ | Ito, drop $dW$, integrate | $\frac{d}{dt}E f(W_t) = \tfrac12 E f''(W_t)$ |
| "Is $X_t$ a martingale?" | Ito drift | drift $= 0$ and $E\int (\text{diffusion})^2 < \infty$ |
| $\int_0^T g(W)\,dW$ in closed form | Ito on an antiderivative $G$ | $\int g\,dW = G(W_T) - G(0) - \tfrac12\int g'(W)\,dt$ |
| Exit probabilities and times | optional stopping | $W$, $W^2 - t$, $e^{-2\mu X/\sigma^2}$, $X - \mu t$ |
| Running maximum | reflection | $P(M_t \ge a) = 2P(W_t \ge a)$ |
| GBM or OU quantities | explicit solution | lognormal or Gaussian formulas |

The general antiderivative rule in row 4 comes from $dG(W) = g(W)\,dW + \tfrac12 g'(W)\,dt$.

## Worked examples

### All moments of $W_t$

"Find $E[W_t^n]$."
Odd $n$: zero by symmetry.
Even $n$: Ito gives $d(W^n) = nW^{n-1}dW + \binom{n}{2}W^{n-2}dt$, so $E[W_t^n] = \binom{n}{2}\int_0^t E[W_s^{n-2}]\,ds$.
Inductively $E[W_t^2] = t$, $E[W_t^4] = 6 \cdot t^2/2 = 3t^2$, $E[W_t^6] = 15 \cdot 3t^3/3 = 15t^3$: in general $(n-1)!!\,t^{n/2}$.
Cross-check with the MGF $E[e^{aW_t}] = e^{a^2t/2} = \sum_k \frac{a^{2k}t^k}{2^kk!}$: the coefficient of $a^{2k}/(2k)!$ is $\frac{(2k)!}{2^kk!}t^k = (2k-1)!!\,t^k$.

### Ito on $W^3$ and a closed form for $\int W^2\,dW$

"Compute $d(W_t^3)$ and use it to evaluate $\int_0^T W_t^2\,dW_t$."
$d(W^3) = 3W^2\,dW + \tfrac12 \cdot 6W\,(dW)^2 = 3W^2\,dW + 3W\,dt$.
Integrating, $\int_0^T W^2\,dW = \tfrac13 W_T^3 - \int_0^T W_t\,dt$.
Checks: the mean of the right side is $0 - 0 = 0$.
The variance by isometry is $\int_0^T E[W_t^4]\,dt = \int_0^T 3t^2\,dt = T^3$.
Directly: $\text{Var}(\tfrac13 W_T^3) = \tfrac{15}{9}T^3$, $\text{Var}(\int W\,dt) = T^3/3$, and $\text{Cov}(W_T^3, \int_0^T W_t\,dt) = \int_0^T E[W_T^3W_t]\,dt = \int_0^T 3tT\,dt = \tfrac32T^3$, so the total is $\tfrac53T^3 + \tfrac13T^3 - 2 \cdot \tfrac13 \cdot \tfrac32 T^3 = T^3$.
The by-product $W_t^3 - 3\int_0^t W_s\,ds$ is a martingale.

### Maximum above a level but ending below zero

"Find $P(\max_{s \le 1} W_s \ge 1, W_1 \le 0)$."
The joint reflection law is $P(M_t \ge a, W_t \le b) = P(W_t \ge 2a - b)$ for $b \le a$: reflecting after the first hit of $a$ maps endpoints $\le b$ to endpoints $\ge 2a - b$.
With $a = 1$, $b = 0$: $P(W_1 \ge 2) = 1 - \Phi(2) \approx 0.0228$.
Quadrature using the bridge crossing probability $e^{-2a(a - w)}$ gives the same value; a grid simulation gives about $0.021$ because it misses crossings between grid points.

### Barrier race with drift, and how long it takes

"$X_t = \mu t + \sigma W_t$ with $\mu = 1$, $\sigma = 1$. Probability of hitting $+1$ before $-1$? Mean and variance of the first hitting time of $+1$ if there were no lower barrier?"
With $\theta = 2\mu/\sigma^2 = 2$, $e^{-2X_t}$ is a martingale bounded up to exit, so $pe^{-2} + (1-p)e^{2} = 1$, i.e.

$$
p = \frac{e^2 - 1}{e^2 - e^{-2}} = \frac{1}{1 + e^{-2}} \approx 0.881.
$$

Without the lower barrier, $\tau_a$ is inverse Gaussian: $E[\tau_a] = a/\mu$ (optional stopping on $X_t - \mu t$) and $\text{Var}(\tau_a) = a\sigma^2/\mu^3$.
So here $E[\tau_1] = 1$ and $\text{Var}(\tau_1) = 1$.
Quadrature of the hitting-time density $\frac{a}{\sigma\sqrt{2\pi t^3}}e^{-(a - \mu t)^2/(2\sigma^2t)}$ confirms both formulas (e.g. $a = 1$, $\mu = 0.5$, $\sigma = 1$ gives mean 2 and variance 8).

### Mean reversion in numbers

"A spread's daily AR(1) coefficient is $0.9$. Treat it as OU. What are $\kappa$, the half-life, and the stationary standard deviation if the daily residual standard deviation is $0.5$?"
$e^{-\kappa} = 0.9$ gives $\kappa = 0.105$ per day and half-life $\ln 2/\kappa = 6.6$ days.
Stationary variance of AR(1): $\frac{0.5^2}{1 - 0.9^2} = 1.316$, standard deviation $1.15$.
In OU terms the exact discretisation has residual variance $\frac{\sigma^2}{2\kappa}(1 - e^{-2\kappa})$, and the stationary variance $\frac{\sigma^2}{2\kappa}$ is the same number, as it must be.

### Recognising martingales

"Which are martingales: $W_t^3$, $W_t^3 - 3tW_t$, $W_t^4 - 6tW_t^2 + 3t^2$, $e^{t/2}\sin W_t$?"
For $f(t, W_t)$ the drift is $f_t + \tfrac12 f_{xx}$.

- $W^3$: drift $3W \ne 0$, not a martingale.
- $W^3 - 3tW$: $-3W + 3W = 0$, a martingale.
- $W^4 - 6tW^2 + 3t^2$: $(-6W^2 + 6t) + (6W^2 - 6t) = 0$, a martingale.
- $e^{t/2}\sin W$: $\tfrac12 e^{t/2}\sin W - \tfrac12 e^{t/2}\sin W = 0$, a martingale (bounded diffusion coefficient on $[0, T]$).

The polynomial ones are the Hermite polynomials $t^{n/2}He_n(W/\sqrt{t})$, the Taylor coefficients in $\theta$ of $e^{\theta W - \theta^2t/2}$.

## Pitfalls

- Dropping the $\tfrac12 f''$ term, or keeping $(dt)^2$ and $dt\,dW$ terms that are zero.
- Calling $W_t^2$ or $e^{W_t}$ a martingale; they are submartingales.
- Reflecting a drifted process; use the exponential martingale.
- Applying optional stopping to an unbounded stopped process (first hit of $+1$ by driftless $W$).
- Reading a simulated barrier probability as exact; grid monitoring biases it down.
- Confusing $E[S_T]$ with the median for GBM, and $\sigma^2/(2\kappa)$ with the finite-horizon OU variance.

## Interview questions

### Brownian moments and Gaussian facts

> [!question]- sc-ps-bm-moments-general | What is $E[W_t^n]$ for every $n$?
> $0$ for odd $n$; $(n-1)!!\,t^{n/2}$ for even $n$ (so $t$, $3t^2$, $15t^3$). Ito recursion $E[W_t^n] = \binom{n}{2}\int_0^t E[W_s^{n-2}]\,ds$, or expand the MGF.

> [!question]- sc-ps-exp-bm-mean-var | Compute $E[e^{W_t}]$ and $\text{Var}(e^{W_t})$.
> $e^{t/2}$ and $e^{2t} - e^t$. $E[e^{aW_t}] = e^{a^2t/2}$ with $a = 1$ and $a = 2$.

> [!question]- sc-ps-w-exp-w | Compute $E[W_te^{W_t}]$.
> $te^{t/2}$. Gaussian integration by parts (Stein): $E[W_tg(W_t)] = t\,E[g'(W_t)]$.

> [!question]- sc-ps-sum-levels-tail | What is $P(W_1 + W_2 > 2)$?
> $1 - \Phi(2/\sqrt5) \approx 0.186$. $W_1 + W_2 = 2W_1 + (W_2 - W_1)$ has variance $4 + 1 = 5$.

> [!question]- sc-ps-cond-exp-backward | For $s < t$, what are $E[W_t \mid W_s]$ and $E[W_s \mid W_t]$?
> $W_s$ and $\frac{s}{t}W_t$. Forward: martingale. Backward: Gaussian regression with slope $\text{Cov}/\text{Var} = s/t$.

> [!question]- sc-ps-product-squares | For $s < t$, compute $E[W_s^2W_t^2]$.
> $2s^2 + st$. Write $W_t = W_s + D$ with $D$ independent: $E[W_s^4] + E[W_s^2]E[D^2] = 3s^2 + s(t - s)$.

> [!question]- sc-ps-cond-positive | Given $W_1 > 0$, what is the probability that $W_2 > 0$?
> $3/4$. $P(W_1 > 0, W_2 > 0) = \frac14 + \frac{\arcsin(1/\sqrt2)}{2\pi} = \frac38$, divided by $\frac12$.

> [!question]- sc-ps-exp-time-integral | Compute $E\big[\exp\big(\int_0^T W_t\,dt\big)\big]$.
> $e^{T^3/6}$. $\int_0^T W_t\,dt \sim N(0, T^3/3)$ and $E[e^Y] = e^{\text{Var}(Y)/2}$.

> [!question]- sc-ps-exp-w-squared | For which $t$ is $E[e^{W_t^2}]$ finite, and what is it?
> $t < 1/2$, with value $1/\sqrt{1 - 2t}$. The integrand is $e^{x^2(1 - 1/(2t))}/\sqrt{2\pi t}$, integrable iff $1 - 1/(2t) < 0$.

### Ito calculus

> [!question]- sc-ps-ito-w-cubed | Compute $d(W_t^3)$.
> $3W_t^2\,dW_t + 3W_t\,dt$. Ito with $f' = 3x^2$, $\tfrac12 f'' = 3x$.

> [!question]- sc-ps-int-w-dw-identity | Express $\int_0^T W\,dW$ through $W_T$, and give its mean and variance.
> $\tfrac12(W_T^2 - T)$, mean 0, variance $T^2/2$. From $d(W^2) = 2W\,dW + dt$.

> [!question]- sc-ps-int-w-squared-dw | Evaluate $\int_0^T W_t^2\,dW_t$.
> $\tfrac13W_T^3 - \int_0^T W_t\,dt$. From $d(W^3) = 3W^2\,dW + 3W\,dt$.

> [!question]- sc-ps-isometry-w-squared | Compute $E\big[(\int_0^T W_t^2\,dW_t)^2\big]$.
> $T^3$. Isometry: $\int_0^T E[W_t^4]\,dt = \int_0^T 3t^2\,dt$.

> [!question]- sc-ps-ito-exp-w | Compute $d(e^{W_t})$ and hence $E[e^{W_t}]$.
> $e^{W_t}\,dW_t + \tfrac12 e^{W_t}\,dt$. Taking expectations, $m' = m/2$ with $m(0) = 1$, so $E[e^{W_t}] = e^{t/2}$.

> [!question]- sc-ps-d-inverse-gbm | For GBM $dS = \mu S\,dt + \sigma S\,dW$, find $d(1/S)$.
> $\frac1S\big((\sigma^2 - \mu)\,dt - \sigma\,dW\big)$. Ito with $f' = -1/S^2$, $f'' = 2/S^3$. So $1/S$ is GBM with drift $\sigma^2 - \mu$: Siegel's paradox in FX.

> [!question]- sc-ps-cov-terminal-time-integral | Compute $\text{Cov}(W_T, \int_0^T W_t\,dt)$.
> $T^2/2$. $\int_0^T \text{Cov}(W_T, W_t)\,dt = \int_0^T t\,dt$.

> [!question]- sc-ps-ito-product-time | Compute $d(tW_t)$ and use it to write $\int_0^T t\,dW_t$ without a stochastic integral.
> $d(tW_t) = W_t\,dt + t\,dW_t$, so $\int_0^T t\,dW_t = TW_T - \int_0^T W_t\,dt$.

### Martingale checks

> [!question]- sc-ps-mart-w-squared | Is $W_t^2$ a martingale? What is?
> No, it is a submartingale with drift $dt$. $W_t^2 - t$ is a martingale.

> [!question]- sc-ps-mart-w-cubed | Is $W_t^3$ a martingale? Fix it with a correction depending on $t$ and $W_t$.
> No (drift $3W_t$). $W_t^3 - 3tW_t$ is a martingale: $f_t + \tfrac12 f_{xx} = -3W + 3W = 0$.

> [!question]- sc-ps-mart-hermite-four | Is $W_t^4 - 6tW_t^2 + 3t^2$ a martingale?
> Yes. $f_t = -6W^2 + 6t$ and $\tfrac12 f_{xx} = 6W^2 - 6t$ cancel; it is the fourth Hermite martingale.

> [!question]- sc-ps-mart-t-w | Is $tW_t$ a martingale? What about $tW_t - \int_0^t W_s\,ds$?
> $tW_t$ is not (drift $W_t$, mean zero but not conditionally). $tW_t - \int_0^t W_s\,ds = \int_0^t s\,dW_s$ is a martingale.

> [!question]- sc-ps-mart-exp-linear | For which $b$ is $e^{aW_t + bt}$ a martingale?
> $b = -a^2/2$. The drift is $(b + a^2/2)e^{aW_t + bt}$.

> [!question]- sc-ps-mart-sin | Is $e^{t/2}\sin W_t$ a martingale?
> Yes. $f_t = \tfrac12 f$ and $\tfrac12 f_{xx} = -\tfrac12 f$ cancel, and the diffusion $e^{t/2}\cos W_t$ is bounded on $[0,T]$.

> [!question]- sc-ps-mart-discounted-stock | For GBM with drift $\mu$, which discounting makes $S_t$ a martingale under $P$, and which under $Q$?
> $e^{-\mu t}S_t$ under $P$; $e^{-rt}S_t$ under $Q$, where the drift is $r$. Only the $Q$ statement is used for pricing.

### Hitting times and barriers

> [!question]- sc-ps-hit-asymmetric | Standard Brownian motion from 0: probability of hitting $+1$ before $-2$?
> $2/3$. $W$ is a bounded martingale up to exit: $p \cdot 1 + (1-p)(-2) = 0$.

> [!question]- sc-ps-exit-time-asymmetric | Expected time for standard Brownian motion to exit $(-2, 3)$?
> $6$. $E[\tau] = ab$ from the martingale $W_t^2 - t$.

> [!question]- sc-ps-max-and-end-below | Compute $P(\max_{s \le 1}W_s \ge 1,\ W_1 \le 0)$.
> $1 - \Phi(2) \approx 0.0228$. Reflection: $P(M_t \ge a, W_t \le b) = P(W_t \ge 2a - b)$.

> [!question]- sc-ps-hitting-time-cdf | Distribution function of the first hitting time $\tau_a$ of level $a > 0$ by standard Brownian motion?
> $P(\tau_a \le t) = 2(1 - \Phi(a/\sqrt t))$. It equals $P(M_t \ge a)$; the density is $\frac{a}{\sqrt{2\pi t^3}}e^{-a^2/(2t)}$.

> [!question]- sc-ps-drift-symmetric-barrier | $X_t = t + W_t$. Probability it hits $+1$ before $-1$?
> $1/(1 + e^{-2}) \approx 0.881$. $e^{-2X_t}$ is a martingale; for symmetric barriers $p = 1/(1 + e^{-\theta a})$ with $\theta = 2\mu/\sigma^2$.

> [!question]- sc-ps-drift-ever-hit | $X_t = -0.1t + 0.2W_t$. Probability it ever reaches $+0.1$?
> $e^{-0.5} \approx 0.607$. $P = e^{-2\lvert\mu\rvert a/\sigma^2} = e^{-2(0.1)(0.1)/0.04}$.

> [!question]- sc-ps-drift-hit-time-moments | $X_t = \mu t + \sigma W_t$, $\mu > 0$. Mean and variance of the first hitting time of $a > 0$?
> Mean $a/\mu$, variance $a\sigma^2/\mu^3$ (inverse Gaussian). Mean from optional stopping on $X_t - \mu t$; variance from $(X_t - \mu t)^2 - \sigma^2t$.

### Geometric Brownian motion

> [!question]- sc-ps-gbm-prob-up | For GBM, what is $P(S_T > S_0)$?
> $\Phi\big((\mu - \sigma^2/2)\sqrt{T}/\sigma\big)$. $\log(S_T/S_0) \sim N((\mu - \sigma^2/2)T, \sigma^2T)$.

> [!question]- sc-ps-gbm-median-equals-start | For which drift is the median of $S_T$ equal to $S_0$, and what is $E[S_T]$ then?
> $\mu = \sigma^2/2$, giving $E[S_T] = S_0e^{\sigma^2T/2} > S_0$. The median is $S_0e^{(\mu - \sigma^2/2)T}$.

> [!question]- sc-ps-gbm-power-moment | Compute $E[S_T^p]$ for GBM.
> $S_0^p\exp\big(p\mu T + \tfrac12 p(p-1)\sigma^2T\big)$. $S_T^p = S_0^p\exp(p(\mu - \sigma^2/2)T + p\sigma W_T)$.

> [!question]- sc-ps-gbm-ever-double | GBM with $\mu < \sigma^2/2$. Probability the price ever doubles?
> $2^{2\mu/\sigma^2 - 1}$. The log-price has drift $\nu = \mu - \sigma^2/2 < 0$ and $P = e^{2\nu\ln 2/\sigma^2}$; $\mu = 0$ gives $1/2$.

> [!question]- sc-ps-gbm-time-average | For GBM, what is $E\big[\frac1T\int_0^T S_t\,dt\big]$?
> $S_0\frac{e^{\mu T} - 1}{\mu T}$. Fubini and $E[S_t] = S_0e^{\mu t}$.

### Ornstein-Uhlenbeck

> [!question]- sc-ps-ou-conditional-moments | For OU $dX = \kappa(\theta - X)\,dt + \sigma\,dW$, give $E[X_t \mid X_0]$ and $\text{Var}(X_t \mid X_0)$.
> $\theta + (X_0 - \theta)e^{-\kappa t}$ and $\frac{\sigma^2}{2\kappa}(1 - e^{-2\kappa t})$. Integrating factor $e^{\kappa t}$, then isometry.

> [!question]- sc-ps-ou-stationary-corr | In stationarity, what is $\text{Corr}(X_s, X_{s+h})$ for OU?
> $e^{-\kappa h}$. The covariance is $\frac{\sigma^2}{2\kappa}e^{-\kappa h}$ and both variances are $\frac{\sigma^2}{2\kappa}$.

> [!question]- sc-ps-ou-half-life-from-ar1 | A daily series has AR(1) coefficient 0.9. Mean-reversion speed and half-life?
> $\kappa = -\ln 0.9 \approx 0.105$ per day, half-life $\ln 2/\kappa \approx 6.6$ days.

## Further reading

- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 5.
- Mark Joshi, Nick Denson and Andrew Downes, *Quant Job Interview Questions and Answers*, stochastic processes chapter.
- Steven Shreve, *Stochastic Calculus for Finance II: Continuous-Time Models*, chapters 3-4.
- Ioannis Karatzas and Steven Shreve, *Brownian Motion and Stochastic Calculus*, chapter 2 (reflection principle and hitting times).
