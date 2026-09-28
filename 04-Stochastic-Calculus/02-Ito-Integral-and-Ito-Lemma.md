---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [brownian-motion, calculus-and-taylor-expansions]
est_hours: 5
sources: [Shreve - Stochastic Calculus for Finance II (Springer 2004) chapter 4, Oksendal - Stochastic Differential Equations (Springer 6th edition) chapters 3-4, Zhou - A Practical Guide to Quantitative Finance Interviews chapter 5]
---

# Ito Integral and Ito's Lemma

## TL;DR

- The Ito integral $\int_0^T H_t\,dW_t$ is the $L^2$ limit of left-endpoint sums $\sum H_{t_i}(W_{t_{i+1}} - W_{t_i})$ with $H$ adapted; the left endpoint makes it a mean-zero martingale.
- Ito isometry: $E\big[(\int_0^T H\,dW)^2\big] = E\big[\int_0^T H^2\,dt\big]$; for deterministic $f$, $\int_0^T f\,dW \sim N(0, \int_0^T f^2\,dt)$.
- Ito's lemma: $df(t, X_t) = f_t\,dt + f_x\,dX_t + \tfrac12 f_{xx}\,(dX_t)^2$ with $dW\,dW = dt$ and $dt\,dW = dt\,dt = 0$.
- $\int_0^T W\,dW = \tfrac12(W_T^2 - T)$, not $\tfrac12 W_T^2$; the $-T/2$ is quadratic variation.
- To compute $E[f(W_t)]$: apply Ito, drop the $dW$ term, integrate the $dt$ term; e.g. $E[W_t^4] = 3t^2$.

## Learning objectives

- Explain the Ito integral as a limit of non-anticipating sums and its isometry.
- Apply Ito's lemma to functions of Brownian motion and of Ito processes.
- Compute expectations and variances of stochastic integrals.

## Core concepts

### Why a new integral

A Brownian path has infinite total variation, so $\int H\,dW$ cannot be defined path by path as a Stieltjes integral.
Worse, the answer depends on where in each interval you evaluate the integrand:

$$
\sum_i W_{t_{i+1}}\Delta W_i - \sum_i W_{t_i}\Delta W_i = \sum_i (\Delta W_i)^2 \to T.
$$

Ito picks the left endpoint.
This is the financially correct choice: $H_{t_i}$ is the position you hold over $[t_i, t_{i+1})$, decided before the price move $\Delta W_i$ is revealed.

### Construction and properties

For a simple adapted integrand $H_t = H_{t_i}$ on $[t_i, t_{i+1})$, define $I_T = \sum_i H_{t_i}\Delta W_i$.
Because $H_{t_i}$ is known at $t_i$ and $\Delta W_i$ is independent of $\mathcal{F}_{t_i}$ with mean 0 and variance $\Delta t_i$:

- $E[I_T] = \sum E[H_{t_i}]E[\Delta W_i] = 0$;
- cross terms vanish: for $i < j$, $E[H_{t_i}\Delta W_i H_{t_j}\Delta W_j] = E[H_{t_i}\Delta W_i H_{t_j}\,E[\Delta W_j \mid \mathcal{F}_{t_j}]] = 0$;
- so $E[I_T^2] = \sum E[H_{t_i}^2]\Delta t_i = E\int_0^T H_t^2\,dt$.

This isometry lets the integral be extended by $L^2$ limits to every adapted $H$ with $E\int_0^T H^2\,dt < \infty$.
For such $H$ the integral $I_t = \int_0^t H\,dW$:

| Property | Statement |
| :--- | :--- |
| Mean | $E[I_t] = 0$ |
| Isometry | $E[I_t^2] = E\int_0^t H_s^2\,ds$ |
| Covariance | $E[\int_0^t H\,dW \int_0^t G\,dW] = E\int_0^t H_s G_s\,ds$ |
| Martingale | $I_t$ is a continuous martingale |
| Quadratic variation | $[I]_t = \int_0^t H_s^2\,ds$ (pathwise, random if $H$ is) |
| Deterministic $f$ | $\int_0^t f\,dW \sim N(0, \int_0^t f^2\,ds)$ |

If only $\int_0^T H^2\,dt < \infty$ almost surely, the integral still exists but is merely a local martingale; its mean need not be zero.

### Ito processes and the multiplication table

An Ito process is $dX_t = \mu_t\,dt + \sigma_t\,dW_t$, meaning $X_t = X_0 + \int_0^t \mu_s\,ds + \int_0^t \sigma_s\,dW_s$.
Its quadratic variation is $d[X]_t = (dX_t)^2 = \sigma_t^2\,dt$, computed with

| $\times$ | $dt$ | $dW$ | $dB$ |
| :--- | :---: | :---: | :---: |
| $dt$ | 0 | 0 | 0 |
| $dW$ | 0 | $dt$ | $\rho\,dt$ |
| $dB$ | 0 | $\rho\,dt$ | $dt$ |

where $B$ is a second Brownian motion with $d[W, B]_t = \rho\,dt$.

### Ito's lemma

For $f(t, x)$ with $f \in C^{1,2}$, a second-order Taylor expansion keeps $(dX)^2$ because it is of order $dt$:

$$
df(t, X_t) = f_t\,dt + f_x\,dX_t + \tfrac12 f_{xx}\,(dX_t)^2 = \Big(f_t + \mu f_x + \tfrac12\sigma^2 f_{xx}\Big)dt + \sigma f_x\,dW_t.
$$

Heuristic derivation: over a step $\Delta t$, $\Delta X = \mu\Delta t + \sigma\Delta W$ and $(\Delta X)^2 = \sigma^2(\Delta W)^2 + o(\Delta t)$; summing $(\Delta W)^2$ over many steps gives $\Delta t$ in the limit (quadratic variation, see [Brownian Motion](01-Brownian-Motion.md)).
Third-order terms are $O(\Delta t^{3/2})$ and vanish.

Multidimensional form, for $f(t, X, Y)$:

$$
df = f_t\,dt + f_x\,dX + f_y\,dY + \tfrac12 f_{xx}\,d[X] + f_{xy}\,d[X,Y] + \tfrac12 f_{yy}\,d[Y].
$$

The product rule is the special case $f = xy$: $d(XY) = X\,dY + Y\,dX + d[X, Y]$.
Integrating it gives stochastic integration by parts.

### Recipe for expectations

Write $df(t, W_t) = a_t\,dt + b_t\,dW_t$.
If $E\int_0^t b_s^2\,ds < \infty$, the $dW$ term has zero mean and $\frac{d}{dt}E[f(t, W_t)] = E[a_t]$.
A process is a martingale exactly when (under this integrability) its $dt$ term vanishes: $f_t + \tfrac12 f_{xx} = 0$ for $f(t, W_t)$.

### Stratonovich integral

The midpoint rule gives the Stratonovich integral $\int H \circ dW = \int H\,dW + \tfrac12 [H, W]_T$.
Ordinary calculus rules hold for it ($\int_0^T W \circ dW = \tfrac12 W_T^2$), which is why physicists use it, but it is not a martingale and it looks ahead within each step, so finance uses Ito.

### Simulation check

```python
import numpy as np
rng = np.random.default_rng(0)
N, n, T = 200_000, 400, 1.0
dW = rng.standard_normal((N, n)) * np.sqrt(T / n)
W = np.cumsum(dW, axis=1)
W_left = np.hstack([np.zeros((N, 1)), W[:, :-1]])
I = (W_left * dW).sum(1)                       # Ito sum for int W dW
print(np.abs(I - (W[:, -1]**2 - T) / 2).mean())  # ~0.03, shrinks as n grows
print(I.var(), T**2 / 2)                         # 0.498 vs 0.5
print((W[:, -1]**4).mean(), 3 * T**2)            # 2.99 vs 3
```

## Worked examples

### $\int_0^T W_t\,dW_t$ two ways

"Guess from ordinary calculus: $\tfrac12 W_T^2$.
Check with Ito on $f(x) = x^2$: $d(W_t^2) = 2W_t\,dW_t + \tfrac12 \cdot 2\,(dW_t)^2 = 2W_t\,dW_t + dt$.
Integrate: $W_T^2 = 2\int_0^T W\,dW + T$, so

$$
\int_0^T W_t\,dW_t = \tfrac12 (W_T^2 - T).
$$

Sanity checks: the mean is $\tfrac12(T - T) = 0$, as an Ito integral must be; the variance by isometry is $\int_0^T E[W_t^2]\,dt = T^2/2$, and directly $\tfrac14\text{Var}(W_T^2) = \tfrac14(3T^2 - T^2) = T^2/2$."
Discretely, $\sum W_{t_i}\Delta W_i = \tfrac12\big(W_T^2 - \sum(\Delta W_i)^2\big)$ by telescoping $W_{t_{i+1}}^2 - W_{t_i}^2 = 2W_{t_i}\Delta W_i + (\Delta W_i)^2$, which makes the $-T/2$ visible.

### Fourth moment and all moments of $W_t$ via Ito

"Apply Ito to $W^4$: $d(W_t^4) = 4W_t^3\,dW_t + 6W_t^2\,dt$.
Take expectations (the $dW$ term has mean zero): $E[W_t^4] = 6\int_0^t E[W_s^2]\,ds = 6\int_0^t s\,ds = 3t^2$."
In general $d(W^n) = nW^{n-1}dW + \binom{n}{2}W^{n-2}dt$, so $E[W_t^n] = \binom{n}{2}\int_0^t E[W_s^{n-2}]\,ds$.
This recursion gives $E[W_t^{2k}] = (2k-1)!!\,t^k$ (1, 3, 15, 105 times $t^k$) and zero for odd $n$.

### Log of geometric Brownian motion

"Let $dS_t = \mu S_t\,dt + \sigma S_t\,dW_t$ and $f(x) = \log x$, so $f' = 1/x$, $f'' = -1/x^2$.
Then, using $(dS_t)^2 = \sigma^2 S_t^2\,dt$,"

$$
d\log S_t = \frac{dS_t}{S_t} - \frac{1}{2}\frac{(dS_t)^2}{S_t^2} = \Big(\mu - \frac{\sigma^2}{2}\Big)dt + \sigma\,dW_t.
$$

So $\log S_T$ is normal and $S_T = S_0\exp\big((\mu - \sigma^2/2)T + \sigma W_T\big)$.
The $-\sigma^2/2$ is the gap between arithmetic and geometric mean return (volatility drag); it drives the solution in [Stochastic Differential Equations](03-Stochastic-Differential-Equations.md).

### Time integral of Brownian motion

"Find the distribution of $A_T = \int_0^T W_t\,dt$."
Product rule: $d(tW_t) = W_t\,dt + t\,dW_t$, so $TW_T = A_T + \int_0^T t\,dW_t$ and

$$
A_T = \int_0^T (T - t)\,dW_t \sim N\Big(0, \int_0^T (T-t)^2\,dt\Big) = N(0, T^3/3).
$$

Also $\text{Cov}(W_T, A_T) = \int_0^T (T - t)\,dt = T^2/2$ by the covariance form of the isometry.
This is the variance input for arithmetic Asian option approximations.

### Finding a martingale: $e^{at}\cos W_t$

"For which $a$ is $M_t = e^{at}\cos W_t$ a martingale?"
With $f(t, x) = e^{at}\cos x$: $f_t = a e^{at}\cos x$ and $\tfrac12 f_{xx} = -\tfrac12 e^{at}\cos x$.
The drift vanishes iff $a = \tfrac12$, and the $dW$ coefficient $-e^{t/2}\sin W_t$ is bounded on bounded time intervals, so $e^{t/2}\cos W_t$ is a true martingale.
Corollary: $E[\cos W_t] = e^{-t/2}$, which is also the real part of the characteristic function $E[e^{iW_t}] = e^{-t/2}$.

## Pitfalls

- Dropping the $\tfrac12 f_{xx}(dX)^2$ term; this is the single most common error and gives $\int W\,dW = W^2/2$.
- Writing $(dX)^2 = \sigma^2\,dW^2$ and stopping there; replace $dW^2$ by $dt$, and keep the cross term $\rho\,dt$ for correlated drivers.
- Using the isometry with a non-adapted integrand such as $\int_0^T W_T\,dW_t$; that is not an Ito integral.
- Assuming every stochastic integral has mean zero; it needs $E\int H^2\,dt < \infty$, otherwise it may be only a local martingale.
- Applying Ito to non-smooth functions like $\lvert x\rvert$ or $(x - K)^+$ without the local-time correction (Tanaka's formula).
- Believing $e^{W_t}$ is a martingale; $E[e^{W_t}] = e^{t/2}$, and the martingale is $e^{W_t - t/2}$.
- Mixing Ito and Stratonovich conventions between a model and its simulation scheme.

## Interview questions

> [!question]- sc-ito-left-endpoint | Why is the Ito integral defined with left-endpoint sums, and what changes with right endpoints?
> Left endpoints make the integrand non-anticipating (you trade before the move), giving a mean-zero martingale. Right endpoints differ by $\sum(\Delta W)^2 \to T$ for $\int W\,dW$.

> [!question]- sc-ito-isometry | State the Ito isometry.
> $E\big[(\int_0^T H\,dW)^2\big] = E\int_0^T H_t^2\,dt$ for adapted $H$ with finite right side. Cross terms vanish because each future increment has conditional mean zero.

> [!question]- sc-ito-lemma-statement | State Ito's lemma for $f(t, X_t)$ with $dX = \mu\,dt + \sigma\,dW$.
> $df = (f_t + \mu f_x + \tfrac12\sigma^2 f_{xx})\,dt + \sigma f_x\,dW$. Taylor to second order and use $(dW)^2 = dt$.

> [!question]- sc-ito-w-dw | Compute $\int_0^T W_t\,dW_t$.
> $\tfrac12(W_T^2 - T)$. Ito on $W^2$: $d(W^2) = 2W\,dW + dt$.

> [!question]- sc-ito-w-dw-variance | What is the variance of $\int_0^T W_t\,dW_t$?
> $T^2/2$. Isometry: $\int_0^T E[W_t^2]\,dt = \int_0^T t\,dt$.

> [!question]- sc-ito-fourth-moment | Use Ito to compute $E[W_t^4]$.
> $3t^2$. $d(W^4) = 4W^3\,dW + 6W^2\,dt$, so $E[W_t^4] = 6\int_0^t s\,ds$.

> [!question]- sc-ito-log-gbm | For $dS = \mu S\,dt + \sigma S\,dW$, what is $d\log S$?
> $(\mu - \sigma^2/2)\,dt + \sigma\,dW$. $f'' = -1/S^2$ contributes $-\tfrac12\sigma^2\,dt$.

> [!question]- sc-ito-product-rule | State the Ito product rule.
> $d(XY) = X\,dY + Y\,dX + d[X, Y]$. For $dX = \sigma_X\,dW$, $dY = \sigma_Y\,dB$ with correlation $\rho$, $d[X,Y] = \rho\sigma_X\sigma_Y\,dt$.

> [!question]- sc-ito-time-integral-distribution | What is the distribution of $\int_0^T W_t\,dt$?
> $N(0, T^3/3)$. Integration by parts gives $\int_0^T (T-t)\,dW_t$, then use $\int_0^T (T-t)^2\,dt$.

> [!question]- sc-ito-deterministic-integrand | What is the law of $\int_0^T t\,dW_t$?
> $N(0, T^3/3)$. A deterministic integrand gives a Gaussian with variance $\int_0^T t^2\,dt$.

> [!question]- sc-ito-cos-martingale | For which $a$ is $e^{at}\cos W_t$ a martingale?
> $a = 1/2$. Drift is $e^{at}\cos W_t\,(a - \tfrac12)$.

> [!question]- sc-ito-exp-martingale | Is $e^{W_t}$ a martingale? What is?
> No: its drift is $\tfrac12 e^{W_t} > 0$ (a submartingale, $E = e^{t/2}$). $e^{\theta W_t - \theta^2 t/2}$ is a martingale.

> [!question]- sc-ito-stratonovich | How do Ito and Stratonovich differ for $\int_0^T W\,dW$?
> Ito gives $\tfrac12(W_T^2 - T)$, Stratonovich (midpoint) gives $\tfrac12 W_T^2$. They differ by $\tfrac12[W,W]_T = T/2$.

> [!question]- sc-ito-local-martingale | When can a stochastic integral $\int H\,dW$ fail to have mean zero?
> When $E\int H^2\,dt = \infty$: it is then only a local martingale (a strict local martingale can have decreasing mean). The isometry and zero-mean property need square integrability.

## In this repo and SDE-Interview-Prep

- See `02_quantitative_data_analysis/misc_notebooks/29. ito's lemma clearly and visually explained` in the legacy archive for a visual walkthrough.

## Further reading

- Steven Shreve, *Stochastic Calculus for Finance II: Continuous-Time Models*, chapter 4.
- Bernt Oksendal, *Stochastic Differential Equations*, chapters 3-4.
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 5.
