---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [ito-integral-and-ito-lemma]
est_hours: 4
sources: [Shreve - Stochastic Calculus for Finance II (Springer 2004) chapters 4 and 6, Oksendal - Stochastic Differential Equations (Springer 6th edition) chapter 5, Glasserman - Monte Carlo Methods in Financial Engineering (Springer 2003) chapters 3 and 6, Cox Ingersoll and Ross - A Theory of the Term Structure of Interest Rates (Econometrica 1985)]
---

# Stochastic Differential Equations

## TL;DR

- GBM $dS = \mu S\,dt + \sigma S\,dW$ solves to $S_t = S_0\exp\big((\mu - \sigma^2/2)t + \sigma W_t\big)$: mean $S_0e^{\mu t}$, median $S_0e^{(\mu - \sigma^2/2)t}$.
- OU $dX = \kappa(\theta - X)\,dt + \sigma\,dW$ solves with the integrating factor $e^{\kappa t}$: Gaussian, mean reverts at rate $\kappa$ (half-life $\ln 2/\kappa$), stationary law $N(\theta, \sigma^2/(2\kappa))$.
- CIR $dr = \kappa(\theta - r)\,dt + \sigma\sqrt{r}\,dW$ has the OU mean, stays non-negative, and never hits 0 iff the Feller condition $2\kappa\theta \ge \sigma^2$ holds; its stationary law is Gamma.
- Euler-Maruyama has strong order 1/2 and weak order 1; Milstein adds $\tfrac12 bb'((\Delta W)^2 - \Delta t)$ and reaches strong order 1.

## Learning objectives

- Solve the GBM and Ornstein-Uhlenbeck SDEs explicitly.
- Know the CIR process and its Feller condition.
- Simulate SDEs with Euler-Maruyama and Milstein and state their convergence orders.

## Core concepts

### What an SDE means

$dX_t = a(t, X_t)\,dt + b(t, X_t)\,dW_t$ is shorthand for the integral equation

$$
X_t = X_0 + \int_0^t a(s, X_s)\,ds + \int_0^t b(s, X_s)\,dW_s,
$$

with the second integral in the Ito sense.
If $a$ and $b$ are Lipschitz in $x$ and grow at most linearly, there is a unique strong solution (a process adapted to the given Brownian motion).
CIR's $\sqrt{r}$ is not Lipschitz at 0, but it is Holder-1/2, which is enough for pathwise uniqueness in one dimension (Yamada-Watanabe).

Two solution techniques cover almost every interview SDE:

- transform to remove the state dependence of the noise (take $\log$ for GBM), then integrate;
- for linear drift, multiply by an integrating factor $e^{\kappa t}$ and use the product rule.

### Geometric Brownian motion

Ito on $\log S$ gives $d\log S = (\mu - \tfrac12\sigma^2)\,dt + \sigma\,dW$ (derived in [Ito's lemma](02-Ito-Integral-and-Ito-Lemma.md)), so

$$
S_t = S_0\exp\Big(\big(\mu - \tfrac12\sigma^2\big)t + \sigma W_t\Big), \qquad \log S_t \sim N\big(\log S_0 + (\mu - \tfrac12\sigma^2)t,\ \sigma^2 t\big).
$$

| Quantity | Value |
| :--- | :--- |
| $E[S_t]$ | $S_0e^{\mu t}$ |
| $\text{Var}(S_t)$ | $S_0^2e^{2\mu t}(e^{\sigma^2 t} - 1)$ |
| $E[S_t^p]$ | $S_0^p\exp\big(p\mu t + \tfrac12 p(p-1)\sigma^2 t\big)$ |
| Median | $S_0e^{(\mu - \sigma^2/2)t}$ |
| Mode | $S_0e^{(\mu - 3\sigma^2/2)t}$ |
| $P(S_t > S_0)$ | $\Phi\big((\mu - \sigma^2/2)\sqrt{t}/\sigma\big)$ |
| $E\int_0^T S_t\,dt$ | $S_0(e^{\mu T} - 1)/\mu$ |

Mode $<$ median $<$ mean: a typical path underperforms the average, and the gap $\sigma^2/2$ per unit time is volatility drag.
With $\mu = 0$ and large $\sigma^2 t$, $E[S_t] = S_0$ while $S_t \to 0$ almost surely.

### Ornstein-Uhlenbeck and Vasicek

$dX_t = \kappa(\theta - X_t)\,dt + \sigma\,dW_t$ with $\kappa > 0$.
The product rule gives $d(e^{\kappa t}X_t) = \kappa\theta e^{\kappa t}\,dt + \sigma e^{\kappa t}\,dW_t$, so

$$
X_t = \theta + (X_0 - \theta)e^{-\kappa t} + \sigma\int_0^t e^{-\kappa(t - s)}\,dW_s.
$$

The stochastic integral has a deterministic integrand, so $X_t$ is Gaussian with

$$
E[X_t] = \theta + (X_0 - \theta)e^{-\kappa t}, \qquad \text{Var}(X_t) = \frac{\sigma^2}{2\kappa}\big(1 - e^{-2\kappa t}\big).
$$

- Stationary law: $N(\theta, \sigma^2/(2\kappa))$.
- Stationary autocovariance: $\text{Cov}(X_s, X_{s+h}) = \frac{\sigma^2}{2\kappa}e^{-\kappa h}$, so sampled at step $\Delta$ it is an AR(1) with coefficient $e^{-\kappa\Delta}$.
- Half-life of a deviation: $\ln 2/\kappa$.
- Vasicek is OU for the short rate; it is tractable but allows negative rates.

In statistical arbitrage the spread of a cointegrated pair is modelled as OU; $\kappa$ from an AR(1) regression sets the holding period and $\sigma/\sqrt{2\kappa}$ the entry bands.

### Cox-Ingersoll-Ross

$dr_t = \kappa(\theta - r_t)\,dt + \sigma\sqrt{r_t}\,dW_t$.
Taking expectations of the integral form, the mean solves the same ODE as OU, $E[r_t] = \theta + (r_0 - \theta)e^{-\kappa t}$.
Ito on $r^2$ and the same trick give

$$
\text{Var}(r_t) = r_0\frac{\sigma^2}{\kappa}\big(e^{-\kappa t} - e^{-2\kappa t}\big) + \frac{\theta\sigma^2}{2\kappa}\big(1 - e^{-\kappa t}\big)^2.
$$

- The transition law is a scaled non-central chi-squared, so CIR can be simulated exactly.
- Stationary law: Gamma with shape $2\kappa\theta/\sigma^2$ and scale $\sigma^2/(2\kappa)$, mean $\theta$, variance $\theta\sigma^2/(2\kappa)$.
- Feller condition: if $2\kappa\theta \ge \sigma^2$ the process never reaches 0; otherwise 0 is hit but is reflecting, so $r_t \ge 0$ always.
- The same SDE is the Heston variance process (see [Stochastic Volatility](../05-Derivatives-and-Volatility/09-Stochastic-Volatility-Heston-and-SABR.md)), where calibrated parameters often violate Feller.

### Numerical schemes and convergence orders

For $dX = a(X)\,dt + b(X)\,dW$ with step $\Delta$:

- Euler-Maruyama: $X_{n+1} = X_n + a(X_n)\Delta + b(X_n)\Delta W_n$.
- Milstein: add $\tfrac12 b(X_n)b'(X_n)\big((\Delta W_n)^2 - \Delta\big)$, the next term of the Ito-Taylor expansion (it comes from $\int\int dW\,dW = \tfrac12((\Delta W)^2 - \Delta)$).

A scheme has strong order $\gamma$ if $E\lvert X_T - \hat{X}_T\rvert = O(\Delta^\gamma)$ (pathwise error, matters for path-dependent payoffs and hedging simulations) and weak order $\beta$ if $\lvert E f(X_T) - E f(\hat{X}_T)\rvert = O(\Delta^\beta)$ (error in prices).

| Scheme | Strong order | Weak order |
| :--- | :---: | :---: |
| Euler-Maruyama | 1/2 | 1 |
| Milstein (scalar noise) | 1 | 1 |

For additive noise ($b$ constant, e.g. OU) the Milstein term is zero, so Euler already has strong order 1.
In several dimensions Milstein needs Levy areas unless the noise is commutative.
The repo's [Euler-Maruyama solver](code/sde_solver_euler_maruyama.py) simulates GBM and Vasicek paths with the Euler step above.

## Worked examples

### Solve GBM and read off its moments

"Given $dS = \mu S\,dt + \sigma S\,dW$, guess $S = e^{Y}$.
Ito on $\log$: $dY = (\mu - \sigma^2/2)\,dt + \sigma\,dW$, which has constant coefficients, so $Y_t = \log S_0 + (\mu - \sigma^2/2)t + \sigma W_t$.
For the mean, $E[e^{\sigma W_t}] = e^{\sigma^2 t/2}$ cancels the $-\sigma^2/2$, so $E[S_t] = S_0e^{\mu t}$.
For the median, the median of $Y_t$ is its mean, so the median of $S_t$ is $S_0e^{(\mu - \sigma^2/2)t}$."
With $\mu = 10\%$, $\sigma = 30\%$, $t = 2$, $S_0 = 100$: mean $122.14$, median $111.63$, mode $93.24$, and $P(S_2 > 100) = \Phi(0.055\sqrt2/0.3) \approx 0.602$.
A $2 \times 10^6$-path simulation reproduces all four to within $0.1$.

### OU moments and half-life

"A spread follows OU with $\kappa = 2$ per year, $\theta = 1$, $\sigma = 0.5$ and starts at $X_0 = 3$. Describe $X_{0.7}$."
Mean: $1 + 2e^{-1.4} = 1.493$.
Variance: $\frac{0.25}{4}(1 - e^{-2.8}) = 0.0587$, close to the stationary $0.0625$ because $2\kappa t = 2.8$ is already large.
Half-life: $\ln 2/2 \approx 0.35$ years, so after $0.7$ years (two half-lives) a quarter of the initial deviation of 2 remains, matching $2e^{-1.4} = 0.493$.

### Feller condition for a short-rate model

"CIR with $\kappa = 1.5$, $\theta = 4\%$, $\sigma = 0.2$. Can the rate hit zero? What is its long-run distribution?"
Feller: $2\kappa\theta = 0.12 \ge \sigma^2 = 0.04$, so zero is never reached.
Stationary law: Gamma with shape $2\kappa\theta/\sigma^2 = 3$ and scale $\sigma^2/(2\kappa) = 0.0133$, i.e. mean $4\%$ and standard deviation $\sqrt{0.04 \cdot 0.04/3} \approx 2.3\%$.
Starting from $r_0 = 2\%$, after one year the mean is $4\% - 2\%e^{-1.5} = 3.55\%$ and the variance from the formula is $4.14 \times 10^{-4}$; an Euler simulation with 2000 steps gives $3.55\%$ and $4.16 \times 10^{-4}$.

### Milstein for GBM and a convergence check

For GBM, $b(S) = \sigma S$ and $b'(S) = \sigma$, so Milstein is

$$
S_{n+1} = S_n\Big(1 + \mu\Delta + \sigma\Delta W_n + \tfrac12\sigma^2\big((\Delta W_n)^2 - \Delta\big)\Big).
$$

Compare both schemes with the exact solution driven by the same Brownian increments:

```python
import numpy as np
rng = np.random.default_rng(3)
mu, sig, T, N, nf = 0.05, 0.5, 1.0, 20_000, 2**10
dWf = rng.standard_normal((N, nf)) * np.sqrt(T / nf)
exact = np.exp((mu - sig**2 / 2) * T + sig * dWf.sum(1))
for m in [8, 16, 32, 64, 128]:
    dW, h = dWf.reshape(N, m, nf // m).sum(2), T / m
    em = np.ones(N); mil = np.ones(N)
    for i in range(m):
        em *= 1 + mu * h + sig * dW[:, i]
        mil *= 1 + mu * h + sig * dW[:, i] + 0.5 * sig**2 * (dW[:, i]**2 - h)
    print(m, np.abs(em - exact).mean(), np.abs(mil - exact).mean())
```

| Steps | EM strong error | Milstein strong error |
| ---: | ---: | ---: |
| 8 | 0.0521 | 0.00462 |
| 16 | 0.0377 | 0.00255 |
| 32 | 0.0263 | 0.00136 |
| 64 | 0.0186 | 0.00071 |
| 128 | 0.0133 | 0.00036 |

Halving the step divides the Euler error by about $\sqrt{2}$ (order 1/2) and the Milstein error by about 2 (order 1).

### $W_t^2$ as a CIR-type process

"Find the SDE satisfied by $X_t = W_t^2$."
Ito: $dX = 2W\,dW + dt$.
Write $2W\,dW = 2\sqrt{X}\,\text{sgn}(W)\,dW$ and let $B_t = \int_0^t \text{sgn}(W_s)\,dW_s$; it is a continuous martingale with $[B]_t = t$, hence a Brownian motion by Levy's characterisation.
So $dX = dt + 2\sqrt{X}\,dB$: a squared Bessel process of dimension 1.
It has the CIR shape with constant drift $a = 1$ in place of $\kappa(\theta - r)$ and $\sigma = 2$; the Feller-type condition $2a \ge \sigma^2$ reads $2 \ge 4$ and fails, consistent with $W$ returning to 0.

## Pitfalls

- Quoting $E[S_t] = S_0e^{(\mu - \sigma^2/2)t}$; that is the median, the mean is $S_0e^{\mu t}$.
- Forgetting that the OU variance at time $t$ is $\frac{\sigma^2}{2\kappa}(1 - e^{-2\kappa t})$, not the stationary value, when $\kappa t$ is small.
- Writing the Feller condition backwards; the drift must dominate: $2\kappa\theta \ge \sigma^2$.
- Simulating CIR or Heston variance with plain Euler: $r + \dots$ can go negative and $\sqrt{r}$ fails; use full truncation, reflection or exact non-central chi-squared sampling.
- Confusing strong and weak order: for pricing European payoffs Euler's weak order 1 is what matters; Milstein does not improve weak order.
- Using independent random numbers for the "exact" and discretised paths when measuring strong error; the paths must share increments.
- Applying scalar Milstein to multi-factor models with non-commutative noise.

## Interview questions

> [!question]- sc-sde-gbm-solution | Solve $dS = \mu S\,dt + \sigma S\,dW$.
> $S_t = S_0\exp((\mu - \sigma^2/2)t + \sigma W_t)$. Ito on $\log S$ removes the state dependence: $d\log S = (\mu - \sigma^2/2)\,dt + \sigma\,dW$.

> [!question]- sc-sde-gbm-mean-median | For GBM, what are the mean and median of $S_t$, and why do they differ?
> Mean $S_0e^{\mu t}$, median $S_0e^{(\mu - \sigma^2/2)t}$. The log is normal so its median equals its mean; exponentiating a symmetric variable skews it right (Jensen).

> [!question]- sc-sde-gbm-variance | What is $\text{Var}(S_t)$ for GBM?
> $S_0^2e^{2\mu t}(e^{\sigma^2 t} - 1)$. $E[S_t^2] = S_0^2e^{2\mu t + \sigma^2 t}$ from $E[e^{2\sigma W_t}] = e^{2\sigma^2 t}$.

> [!question]- sc-sde-ou-solution | Solve the OU SDE $dX = \kappa(\theta - X)\,dt + \sigma\,dW$.
> $X_t = \theta + (X_0 - \theta)e^{-\kappa t} + \sigma\int_0^t e^{-\kappa(t-s)}\,dW_s$. Multiply by $e^{\kappa t}$ and use the product rule.

> [!question]- sc-sde-ou-variance | What is $\text{Var}(X_t)$ for OU, and the stationary variance?
> $\frac{\sigma^2}{2\kappa}(1 - e^{-2\kappa t})$, tending to $\frac{\sigma^2}{2\kappa}$. Isometry: $\sigma^2\int_0^t e^{-2\kappa(t-s)}\,ds$.

> [!question]- sc-sde-ou-half-life | What is the half-life of an OU process, and how do you estimate $\kappa$ from data?
> $\ln 2/\kappa$. Sampled at step $\Delta$ it is AR(1) with slope $\phi = e^{-\kappa\Delta}$; regress $X_{t+\Delta}$ on $X_t$ and set $\kappa = -\ln\phi/\Delta$.

> [!question]- sc-sde-ou-autocovariance | What is the stationary autocovariance of OU at lag $h$?
> $\frac{\sigma^2}{2\kappa}e^{-\kappa h}$. $X_{s+h} - \theta = e^{-\kappa h}(X_s - \theta) + $ an independent Gaussian term.

> [!question]- sc-sde-cir-feller | State the Feller condition for CIR and what it guarantees.
> $2\kappa\theta \ge \sigma^2$: the process never hits 0. Without it, 0 is reached but reflected, so $r_t \ge 0$ still.

> [!question]- sc-sde-cir-stationary | What is the stationary distribution of CIR?
> Gamma with shape $2\kappa\theta/\sigma^2$ and scale $\sigma^2/(2\kappa)$: mean $\theta$, variance $\theta\sigma^2/(2\kappa)$.

> [!question]- sc-sde-vasicek-vs-cir | Main practical difference between Vasicek and CIR short rates?
> Vasicek is Gaussian and allows negative rates; CIR has volatility $\sigma\sqrt{r}$, stays non-negative, and has a non-central chi-squared transition. Both have the same mean path.

> [!question]- sc-sde-euler-orders | State the strong and weak convergence orders of Euler-Maruyama.
> Strong 1/2, weak 1. Pathwise error scales like $\sqrt{\Delta}$ because the scheme ignores the $\tfrac12 bb'((\Delta W)^2 - \Delta)$ term, which has size $O(\Delta)$ per step and random sign.

> [!question]- sc-sde-milstein-scheme | Write the Milstein step and its strong order.
> $X_{n+1} = X_n + a\Delta + b\Delta W + \tfrac12 bb'((\Delta W)^2 - \Delta)$; strong order 1 for scalar noise.

> [!question]- sc-sde-additive-noise-milstein | Why does Milstein give nothing extra for OU?
> The correction is $\tfrac12 bb'$ and $b = \sigma$ is constant, so $b' = 0$; Euler already has strong order 1 for additive noise.

> [!question]- sc-sde-w-squared-sde | What SDE does $X_t = W_t^2$ satisfy?
> $dX = dt + 2\sqrt{X}\,dB$ with $B = \int\text{sgn}(W)\,dW$ a Brownian motion (Levy). It is a squared Bessel process of dimension 1.

## In this repo and SDE-Interview-Prep

- Code: [sde_solver_euler_maruyama.py](code/sde_solver_euler_maruyama.py).

## Further reading

- Steven Shreve, *Stochastic Calculus for Finance II: Continuous-Time Models*, chapters 4 and 6.
- Bernt Oksendal, *Stochastic Differential Equations*, chapter 5.
- Paul Glasserman, *Monte Carlo Methods in Financial Engineering*, chapter 3 (exact simulation of OU and CIR) and chapter 6 (discretisation schemes and orders).
- J. Cox, J. Ingersoll and S. Ross, "A Theory of the Term Structure of Interest Rates", *Econometrica* 53 (1985).
