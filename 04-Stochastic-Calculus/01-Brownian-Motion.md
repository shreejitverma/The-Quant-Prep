---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
prereqs: [random-walks-and-gamblers-ruin, inequalities-and-limit-theorems]
est_hours: 4
sources: [Shreve - Stochastic Calculus for Finance II (Springer 2004) chapter 3, Karatzas and Shreve - Brownian Motion and Stochastic Calculus (Springer 1991) chapter 2, Zhou - A Practical Guide to Quantitative Finance Interviews chapter 5, Broadie Glasserman and Kou - A Continuity Correction for Discrete Barrier Options (Mathematical Finance 7(4) 1997), Spitzer - A Combinatorial Lemma and its Application to Probability Theory (Transactions of the AMS 82 1956)]
---

# Brownian Motion

## TL;DR

- $W_0 = 0$, independent Gaussian increments $W_t - W_s \sim N(0, t - s)$, continuous paths; equivalently a centred Gaussian process with $\text{Cov}(W_s, W_t) = \min(s, t)$.
- Quadratic variation over $[0, T]$ is $T$ (not 0), total variation is infinite: this is the whole reason $dW\,dW = dt$ and Ito calculus differs from ordinary calculus.
- Reflection principle: $P(\max_{s \le t} W_s \ge a) = 2P(W_t \ge a)$, so $\max_{s \le t} W_s \overset{d}{=} \lvert W_t \rvert$ and $E[\max_{s \le 1} W_s] = \sqrt{2/\pi}$.
- The first hitting time of $a \ne 0$ is finite almost surely but has infinite mean; the exit time of $(-a, b)$ has mean $ab$.
- With drift, $X_t = \mu t + \sigma W_t$: $e^{-2\mu X_t/\sigma^2}$ is a martingale, which gives every barrier probability, e.g. $P(\text{ever hit } a) = e^{-2\lvert\mu\rvert a/\sigma^2}$ when $\mu < 0$.

## Learning objectives

- State the defining properties of Brownian motion and construct it as a scaled random walk limit.
- Compute quadratic variation and explain why it is non-zero.
- Use the reflection principle for the running maximum and hitting times.
- Solve interview questions on Brownian motion with drift hitting barriers.

## Core concepts

### Definition

A standard Brownian motion $(W_t)_{t \ge 0}$ satisfies

1. $W_0 = 0$;
2. independent increments: $W_{t_1} - W_{t_0}, \dots, W_{t_n} - W_{t_{n-1}}$ are independent for $t_0 < t_1 < \dots < t_n$;
3. stationary Gaussian increments: $W_t - W_s \sim N(0, t - s)$ for $s < t$;
4. continuous sample paths.

Equivalently, $W$ is a continuous centred Gaussian process with $\text{Cov}(W_s, W_t) = \min(s, t)$.
The covariance follows from independent increments: for $s < t$, $E[W_s W_t] = E[W_s^2] + E[W_s(W_t - W_s)] = s$.

The Gaussian characterisation is the fastest tool in interviews: any linear functional of the path ($W_1 + W_2$, $\int_0^1 W_t\,dt$, $W_t - \frac{t}{T}W_T$) is Gaussian, so you only need its mean and variance.

### Construction as a random walk limit

Let $S_k$ be a fair $\pm 1$ random walk and set $W^{(n)}_t = S_{\lfloor nt \rfloor}/\sqrt{n}$.
For fixed $t$, $W^{(n)}_t$ has mean 0 and variance $\lfloor nt \rfloor/n \to t$, and by the CLT it is asymptotically $N(0, t)$; increments over disjoint intervals use disjoint coin flips, so they are independent.
Donsker's theorem upgrades this to convergence of the whole path in distribution, which is why random walk answers (ruin probabilities, expected durations) have Brownian analogues with the same form.
Space scales like the square root of time: $n$ steps of size $1/\sqrt{n}$.

### Invariances and martingales

- Scaling: $c^{-1/2} W_{ct}$ is a Brownian motion for $c > 0$; so $W_{4t} \overset{d}{=} 2W_t$, not $4W_t$.
- Symmetry: $-W$ is a Brownian motion.
- Time inversion: $tW_{1/t}$ (with value 0 at 0) is a Brownian motion.
- Markov and strong Markov: after a stopping time $\tau$, $W_{\tau + t} - W_\tau$ is a fresh Brownian motion independent of the past.

With respect to its own filtration, $W_t$, $W_t^2 - t$ and $e^{\theta W_t - \theta^2 t/2}$ are martingales.
These three drive almost every hitting-time calculation via optional stopping (see [Martingales and Optional Stopping](../01-Probability/12-Martingales-and-Optional-Stopping.md)).

### Quadratic variation

Partition $[0, T]$ into $n$ steps of length $\Delta = T/n$ and let $\Delta W_i$ be the increments.

$$
Q_n = \sum_{i=1}^n (\Delta W_i)^2, \qquad E[Q_n] = n\Delta = T, \qquad \text{Var}(Q_n) = n \cdot 2\Delta^2 = \frac{2T^2}{n} \to 0.
$$

So $Q_n \to T$ in $L^2$: the quadratic variation $[W]_T = T$ is deterministic.
For a differentiable function $f$, $\sum (\Delta f)^2 \le \max \lvert\Delta f\rvert \sum \lvert\Delta f\rvert \to 0$, so a non-zero quadratic variation proves Brownian paths are not differentiable (in fact nowhere differentiable).
The first variation explodes: $E\sum \lvert\Delta W_i\rvert = n\sqrt{2\Delta/\pi} = \sqrt{2nT/\pi} \to \infty$.
Infinite total variation is why $\int H\,dW$ cannot be a pathwise Riemann-Stieltjes integral, and $[W]_t = t$ is the rule $dW\,dW = dt$ used in [Ito's lemma](02-Ito-Integral-and-Ito-Lemma.md).

### Reflection principle and the running maximum

Let $M_t = \max_{s \le t} W_s$ and $\tau_a = \inf\{t : W_t = a\}$ for $a > 0$.
On $\{\tau_a \le t\}$, reflect the path after $\tau_a$ about the level $a$; by the strong Markov property and symmetry this is a bijection between paths ending above $a$ and paths that touched $a$ and end below $a$.
Hence

$$
P(M_t \ge a) = P(\tau_a \le t) = 2P(W_t \ge a) = 2\left(1 - \Phi\!\left(\frac{a}{\sqrt{t}}\right)\right).
$$

Consequences:

- $M_t \overset{d}{=} \lvert W_t \rvert$, so $E[M_t] = \sqrt{2t/\pi}$ and $E[M_t^2] = t$.
- Joint law: for $a > 0$ and $b \le a$, $P(M_t \ge a, W_t \le b) = P(W_t \ge 2a - b)$.
- Hitting-time density: $f_{\tau_a}(t) = \frac{a}{\sqrt{2\pi t^3}} e^{-a^2/(2t)}$, with Laplace transform $E[e^{-\lambda \tau_a}] = e^{-a\sqrt{2\lambda}}$.
- $P(\tau_a < \infty) = 1$ but $E[\tau_a] = \infty$, since the density decays like $t^{-3/2}$.

The reflection argument needs a symmetric, continuous process; with drift it fails and you use a Girsanov reweighting or the exponential martingale below.

### Brownian motion with drift and barrier problems

Let $X_t = \mu t + \sigma W_t$ and $\theta = 2\mu/\sigma^2$.
Then $e^{-\theta X_t}$ is a martingale, because $E[e^{-\theta X_t}] = e^{-\theta\mu t + \theta^2\sigma^2 t/2} = 1$.
Stopping at $\tau$, the first exit from $(-b, a)$ with $a, b > 0$, and applying optional stopping (the stopped martingale is bounded):

$$
P(X_\tau = a) = \frac{e^{\theta b} - 1}{e^{\theta b} - e^{-\theta a}}, \qquad E[\tau] = \frac{a P(X_\tau = a) - b P(X_\tau = -b)}{\mu},
$$

the second from the martingale $X_t - \mu t$.
Useful limits:

| Quantity | Answer | Argument |
| :--- | :--- | :--- |
| $P$(driftless BM hits $a$ before $-b$) | $b/(a+b)$ | $W$ is a martingale |
| $E$[exit time of $(-b, a)$], driftless | $ab$ | $W_t^2 - t$ is a martingale |
| $P$(ever hit $a > 0$), $\mu < 0$ | $e^{-2\lvert\mu\rvert a/\sigma^2}$ | let $b \to \infty$ |
| $E[\tau_a]$, $\mu > 0$ | $a/\mu$ | $X_t - \mu t$ is a martingale |
| $P$(ever hit $a > 0$), $\mu \ge 0$ | $1$ | recurrence or positive drift |

These are the continuous versions of [gambler's ruin](../01-Probability/11-Random-Walks-and-Gamblers-Ruin.md), with $(q/p)^{S_n}$ replaced by $e^{-2\mu X_t/\sigma^2}$.

### Brownian bridge

Conditioning on $W_T = 0$ gives the Brownian bridge $B_t = W_t - \frac{t}{T}W_T$.
It is Gaussian with mean 0 and $\text{Cov}(B_s, B_t) = s(T - t)/T$ for $s \le t$, so $\text{Var}(B_t) = t(T-t)/T$, maximal at $T/2$.
$B$ is independent of $W_T$ (they are jointly Gaussian and uncorrelated), which is how bridges are used to fill in paths in Monte Carlo and to correct discretely monitored barriers.

### Simulation check

Simulating the running maximum on a grid is biased low, because the path can peak between grid points.
The script [`code/stoch_01_brownian_motion.py`](code/stoch_01_brownian_motion.py) separates the two effects on $[0, 1]$:

- Exact continuous maximum: between grid points, sample the maximum of the Brownian bridge from $x$ to $y$ over a step $h$ as $\tfrac12\big(x + y + \sqrt{(y - x)^2 - 2h\ln U}\big)$ with $U$ uniform.
  This is exact for any step, and $10^6$ paths reproduce $P(M_1 \ge 1) = 2(1 - \Phi(1)) = 0.3173$, $E[M_1] = \sqrt{2/\pi} = 0.7979$ and $E[M_1^2] = 1$ within four standard errors.
- Grid maximum with 400 steps: Spitzer's identity $E[\max_{0 \le k \le n} S_k] = \sum_{k=1}^n E[S_k^+]/k$ gives the exact grid mean $\frac{1}{\sqrt{2\pi n}}\sum_{k=1}^{n} k^{-1/2} = 0.7693$, below the continuous $0.7979$.

Since $\sum_{k \le n} k^{-1/2} = 2\sqrt{n} + \zeta(1/2) + O(n^{-1/2})$, the gap is $\beta\sqrt{\Delta t}$ to leading order with $\beta = -\zeta(1/2)/\sqrt{2\pi} = 0.5826$, here $0.029$.
Broadie, Glasserman and Kou use the same constant for discretely monitored barriers: a grid-monitored barrier at $a$ behaves like a continuous one at $a + \beta\sigma\sqrt{\Delta t}$.
For the 400-step grid that predicts $P(\text{grid max} \ge 1) \approx 2\big(1 - \Phi(1 + 0.5826/20)\big) = 0.3034$ against the continuous $0.3173$, and a 100,000-path grid simulation agrees within four standard errors.

## Worked examples

### Probability that $W_1$ and $W_2$ are both positive

"We need $P(W_1 > 0, W_2 > 0)$.
$W_1$ and $W_2$ are jointly Gaussian with variances 1 and 2 and covariance $\min(1,2) = 1$, so the correlation is $\rho = 1/\sqrt{2}$.
For a centred bivariate normal, $P(X > 0, Y > 0) = \frac14 + \frac{\arcsin\rho}{2\pi}$ (Sheppard's formula).
With $\arcsin(1/\sqrt2) = \pi/4$ this is $\frac14 + \frac18 = \frac38$."
A direct argument: write $W_2 = W_1 + Z$ with $Z$ independent standard normal; the event is $\{W_1 > 0, Z > -W_1\}$, a wedge of angle $\pi/2 + \pi/4 = 3\pi/4$ in the rotationally symmetric $(W_1, Z)$ plane, and $\frac{3\pi/4}{2\pi} = \frac38$.
Then $P(W_2 > 0 \mid W_1 > 0) = \frac{3/8}{1/2} = \frac34$.

### Distribution and mean of the running maximum

"What is $E[\max_{0 \le t \le T} W_t]$?
By reflection, $P(M_T \ge a) = 2P(W_T \ge a) = P(\lvert W_T\rvert \ge a)$ for every $a \ge 0$, so $M_T$ has the law of $\lvert W_T \rvert$.
Hence $E[M_T] = E\lvert W_T\rvert = \sqrt{T}\,E\lvert Z\rvert = \sqrt{2T/\pi} \approx 0.80\sqrt{T}$."
A trader's reading: a driftless asset with 1% daily volatility (treated as arithmetic Brownian motion) has an expected 20-day high $\sqrt{2/\pi} \times \sqrt{20} = 3.57\%$ above today's price.
The probability it touches $+2$ standard deviations of the horizon move at some point is $2(1 - \Phi(2)) = 4.55\%$, double the terminal probability of $2.28\%$.

### Two-sided barrier with drift

"A log-price follows $X_t = 0.5t + W_t$.
What is the probability it reaches $+1$ before $-1$, and how long does that take on average?"
Take $\theta = 2\mu/\sigma^2 = 1$.
$e^{-X_t}$ is a bounded martingale up to exit, so $p e^{-1} + (1-p)e^{1} = 1$, giving

$$
p = \frac{e - 1}{e - e^{-1}} = \frac{1}{1 + e^{-1}} \approx 0.731.
$$

For the time, $X_t - 0.5t$ is a martingale and the exit time has finite mean, so $0.5\,E[\tau] = E[X_\tau] = p - (1-p) = 2p - 1$, giving $E[\tau] = 2(2p-1) \approx 0.924$.
Two independent checks in the script: a finite-difference solution of $\tfrac12 u'' + 0.5u' = 0$ (for $p$) and $= -1$ (for $E[\tau]$) on $(-1, 1)$ gives $0.731$ and $0.924$, and a 400,000-path simulation with step $0.01$ that detects crossings between grid points by the Brownian-bridge crossing probability $e^{-2(1 - x)(1 - y)/h}$ reproduces $p$ within four standard errors.
Without that bridge correction a grid simulation detects exits late.

### Expected exit time of a symmetric interval

"Standard Brownian motion starts at 0; how long until it first hits $\pm 1$?"
$W_t^2 - t$ is a martingale and $W_{t \wedge \tau}^2 \le 1$ is bounded, so $E[W_\tau^2] = E[\tau]$.
Since $\lvert W_\tau\rvert = 1$, $E[\tau] = 1$.
For the asymmetric interval $(-b, a)$ the same argument gives $E[\tau] = a^2\frac{b}{a+b} + b^2\frac{a}{a+b} = ab$.

### Will a stock with negative log drift ever double?

"Under the real measure a stock is GBM with $\mu = 2\%$ and $\sigma = 30\%$. What is the probability it ever doubles?"
The log-price $\log(S_t/S_0) = \nu t + \sigma W_t$ has drift $\nu = \mu - \sigma^2/2 = -2.5\% < 0$.
The probability of ever reaching $\log 2$ is $e^{2\nu \log 2/\sigma^2} = 2^{2\nu/\sigma^2} = 2^{2\mu/\sigma^2 - 1} \approx 0.680$, which a finite-difference solution of $\tfrac12\sigma^2u'' + \nu u' = 0$ on $(-60, \log 2)$ confirms.
With $\mu = 0$ this is $1/2$, the bound $P(\sup_t S_t \ge 2S_0) \le 1/2$ from Doob's maximal inequality for a positive martingale, attained because paths are continuous.

## Pitfalls

- Treating $W_s$ and $W_t$ as independent: increments are independent, levels are correlated with $\text{Cov} = \min(s,t)$.
- Scaling time and space the same way: $W_{ct} \overset{d}{=} \sqrt{c}\,W_t$.
- Confusing quadratic variation (a pathwise limit equal to $T$) with variance (an expectation that also equals $T$); the point is that $[W]_T$ is not random.
- Using the reflection principle with drift; reflection needs symmetry, so for $\mu \ne 0$ use the exponential martingale or Girsanov.
- Saying "the hitting time is finite, so its mean is finite": for driftless Brownian motion $E[\tau_a] = \infty$.
- Treating "the time of the maximum" as a stopping time; it depends on the future.
- Simulating barrier or maximum problems on a coarse grid and forgetting the $O(\sqrt{\Delta t})$ underestimation of the maximum; sample the bridge maximum between grid points or apply the Broadie-Glasserman-Kou shift.

## Interview questions

> [!question]- sc-bm-definition | State the defining properties of standard Brownian motion.
> $W_0 = 0$; independent increments; $W_t - W_s \sim N(0, t-s)$ for $s < t$; continuous paths. Equivalently a continuous centred Gaussian process with covariance $\min(s,t)$.

> [!question]- sc-bm-covariance-levels | What is $\text{Cov}(W_s, W_t)$, and what is $\text{Var}(W_1 + W_2)$?
> $\min(s,t)$; $\text{Var}(W_1 + W_2) = 1 + 2 + 2 \cdot 1 = 5$. Write $W_t = W_s + (W_t - W_s)$ and use independence of the increment.

> [!question]- sc-bm-scaling | Is $W_{4t}$ equal in law to $2W_t$ or $4W_t$? Is $tW_{1/t}$ a Brownian motion?
> $2W_t$, since $c^{-1/2}W_{ct}$ is Brownian. Yes: $tW_{1/t}$ is a centred Gaussian process with covariance $st\min(1/s,1/t) = \min(s,t)$, and it is continuous at 0.

> [!question]- sc-bm-random-walk-limit | How do you get Brownian motion from a coin-flip random walk?
> $W^{(n)}_t = S_{\lfloor nt \rfloor}/\sqrt{n}$ converges in law to $W$ (Donsker). Variance $\lfloor nt\rfloor/n \to t$, CLT gives normality, disjoint flips give independent increments.

> [!question]- sc-bm-quadratic-variation | Why is the quadratic variation of $W$ on $[0,T]$ equal to $T$?
> $T$. $\sum(\Delta W_i)^2$ has mean $n\Delta = T$ and variance $2n\Delta^2 = 2T^2/n \to 0$, so it converges to the constant $T$.

> [!question]- sc-bm-total-variation | What is the total variation of a Brownian path, and why does it matter?
> Infinite: $E\sum\lvert\Delta W_i\rvert = \sqrt{2nT/\pi} \to \infty$. So $\int H\,dW$ cannot be defined pathwise as a Stieltjes integral, which is why the Ito integral is built as an $L^2$ limit.

> [!question]- sc-bm-reflection-max | What is $P(\max_{s \le T} W_s \ge a)$ for $a > 0$?
> $2(1 - \Phi(a/\sqrt{T}))$. Reflect each path after it first hits $a$: paths that touched $a$ and end below it pair with paths ending above it.

> [!question]- sc-bm-expected-max | What is $E[\max_{0 \le t \le 1} W_t]$?
> $\sqrt{2/\pi} \approx 0.798$. By reflection the maximum has the law of $\lvert W_1\rvert$.

> [!question]- sc-bm-hitting-time-mean | Brownian motion starts at 0. Is the first hitting time of 1 finite? What is its mean?
> Finite almost surely, mean infinite. $P(\tau_1 \le t) = 2(1-\Phi(1/\sqrt t)) \to 1$, but the density decays like $t^{-3/2}$ so $E[\tau_1] = \infty$.

> [!question]- sc-bm-exit-time-interval | Expected time for standard Brownian motion to leave $(-a, b)$?
> $ab$. Optional stopping on $W_t^2 - t$: $E[\tau] = E[W_\tau^2] = a^2\frac{b}{a+b} + b^2\frac{a}{a+b}$.

> [!question]- sc-bm-drift-exponential-martingale | For $X_t = \mu t + \sigma W_t$, which exponential of $X_t$ is a martingale with no time term?
> $e^{-2\mu X_t/\sigma^2}$. $E[e^{-\theta X_t}] = e^{t(-\theta\mu + \theta^2\sigma^2/2)} = 1$ exactly when $\theta = 2\mu/\sigma^2$.

> [!question]- sc-bm-negative-drift-ever-hit | $X_t = -t + W_t$. Probability that $X$ ever reaches $+1$?
> $e^{-2} \approx 0.135$. $e^{2X_t}$ is a martingale; stop at $+1$ or $-b$ and let $b \to \infty$: $P = e^{-2\lvert\mu\rvert a/\sigma^2}$.

> [!question]- sc-bm-positive-drift-hit-time | $X_t = \mu t + \sigma W_t$ with $\mu > 0$. Expected time to first hit $a > 0$?
> $a/\mu$. $X_t - \mu t$ is a martingale and $\tau_a$ has finite mean, so $a = \mu E[\tau_a]$; $\sigma$ does not matter.

> [!question]- sc-bm-both-positive | What is $P(W_1 > 0, W_2 > 0)$?
> $3/8$. Correlation is $1/\sqrt{2}$ and $P = \frac14 + \frac{\arcsin\rho}{2\pi} = \frac14 + \frac18$.

> [!question]- sc-bm-bridge-variance | What is the variance of the Brownian bridge $W_t - \frac{t}{T}W_T$ at time $t$?
> $t(T-t)/T$. $\text{Var} = t - 2\frac{t}{T}t + \frac{t^2}{T^2}T = t - t^2/T$.

> [!question]- sc-bm-discrete-monitoring-bias | You estimate $E[\max W]$ by simulating on a grid of step $\Delta t$. Which way is the bias, and how big?
> Downward, of order $\sqrt{\Delta t}$: about $0.5826\sqrt{\Delta t}$ for standard Brownian motion, because the true path peaks between grid points.
> The constant is $-\zeta(1/2)/\sqrt{2\pi}$, from Spitzer's identity; with 400 steps on $[0, 1]$ the exact grid mean is $0.7693$ against $\sqrt{2/\pi} = 0.7979$.

> [!question]- sc-bm-exact-max-simulation | How do you simulate the running maximum of Brownian motion without grid bias?
> Sample the maximum of the Brownian bridge on each step exactly: between $x$ and $y$ over time $h$, $M = \tfrac12\big(x + y + \sqrt{(y - x)^2 - 2h\ln U}\big)$ with $U$ uniform.
> It inverts $P(M \ge m \mid x, y) = e^{-2(m - x)(m - y)/h}$, so the path maximum is exact on any grid.

> [!question]- sc-bm-hitting-laplace | What is $E[e^{-\lambda\tau_a}]$ for the first hitting time of $a > 0$ by standard Brownian motion?
> $e^{-a\sqrt{2\lambda}}$.
> Optional stopping on the bounded martingale $e^{\theta W_{t \wedge \tau_a} - \theta^2 (t \wedge \tau_a)/2}$ with $\theta = \sqrt{2\lambda}$ gives $E[e^{\theta a - \lambda\tau_a}] = 1$.

## In this repo and The-Distinguished-Engineer

- Code: [`code/stoch_01_brownian_motion.py`](code/stoch_01_brownian_motion.py) prints and asserts every number on this page: covariances and the bridge variance in exact rational arithmetic, the reflection law by exact continuous-maximum (bridge) simulation, the hitting-time law by quadrature, the grid bias by Spitzer's identity with $\zeta(1/2)$ from Euler-Maclaurin, and every barrier probability and exit time by a finite-difference ODE solve and bridge-corrected simulation.
- Related notes: [Martingales and Optional Stopping](../01-Probability/12-Martingales-and-Optional-Stopping.md), [Random Walks and Gambler's Ruin](../01-Probability/11-Random-Walks-and-Gamblers-Ruin.md), [Ito Integral and Ito's Lemma](02-Ito-Integral-and-Ito-Lemma.md).

## Further reading

- Steven Shreve, *Stochastic Calculus for Finance II: Continuous-Time Models*, chapter 3 (Brownian motion, quadratic variation, reflection).
- Ioannis Karatzas and Steven Shreve, *Brownian Motion and Stochastic Calculus*, chapter 2.
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 5.
- M. Broadie, P. Glasserman and S. Kou, "A Continuity Correction for Discrete Barrier Options", *Mathematical Finance* 7(4) (1997), 325-349.
- F. Spitzer, "A Combinatorial Lemma and its Application to Probability Theory", *Transactions of the American Mathematical Society* 82 (1956), 323-339.
