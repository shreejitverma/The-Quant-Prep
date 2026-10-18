---
type: concept
track: [quant-research, quant-risk]
tier: advanced
status: solid
prereqs: [stochastic-differential-equations, swaps-and-curve-building]
est_hours: 5
sources: [Brigo and Mercurio - Interest Rate Models: Theory and Practice 2nd ed. (Springer 2006) chapter 3, Vasicek - An Equilibrium Characterization of the Term Structure - Journal of Financial Economics 5(2) 1977, Cox Ingersoll and Ross - A Theory of the Term Structure of Interest Rates - Econometrica 53(2) 1985, Ho and Lee - Term Structure Movements and Pricing Interest Rate Contingent Claims - Journal of Finance 41(5) 1986, Hull and White - Pricing Interest-Rate-Derivative Securities - Review of Financial Studies 3(4) 1990, Hull and White - Numerical Procedures for Implementing Term Structure Models I - Journal of Derivatives 2(1) 1994, Jamshidian - An Exact Bond Option Formula - Journal of Finance 44(1) 1989, Glasserman - Monte Carlo Methods in Financial Engineering (Springer 2004) section 3.4, Lord Koekkoek and van Dijk - A comparison of biased simulation schemes for stochastic volatility models - Quantitative Finance 10(2) 2010]
---

# Short-Rate Models

## TL;DR

- A short-rate model specifies $dr = \mu(t,r)\,dt + s(t,r)\,dW$ under the risk-neutral measure and prices every bond as $P(t,T) = \mathbb{E}_t[e^{-\int_t^T r\,du}]$; affine drift and variance make $P = A(t,T)e^{-B(t,T)r}$ with $A, B$ from Riccati ODEs.
- Vasicek (Gaussian, mean-reverting) and CIR (square-root, non-negative) are equilibrium models with a handful of constant parameters, so they cannot match today's curve; Hull-White adds a deterministic $\theta(t)$ that fits any curve exactly.
- Every closed form here has an independent check: Vasicek and Hull-White against Monte Carlo, CIR against a Crank-Nicolson PDE solve; the Hull-White $\theta(t)$ is verified by simulating with it and recovering the market discount factor.
- In one-factor models all bond prices are monotone in one state variable, which gives Jamshidian's exact swaption formula and also forces instantaneous correlation 1 between all rates.
- CIR needs $2k\theta \ge \sigma^2$ (Feller) for zero to be unattainable; simulation needs a scheme that never takes the square root of a negative number.

## Learning objectives

- Differentiate equilibrium models from no-arbitrage term structure models.
- Formulate the Vasicek and CIR SDEs and derive and evaluate their zero-coupon bond formulas.
- Derive the time-dependent drift $\theta(t)$ in the Hull-White one-factor model that matches the initial forward curve, and verify it numerically.
- Price zero-bond options and, by Jamshidian's decomposition, European swaptions in Hull-White.
- State the Feller condition $2k\theta \ge \sigma^2$ for CIR and explain simulation failure modes when it is violated.
- Analyse the structural limits of one-factor models: correlation, volatility shape, negative rates.

## Core concepts

### Equilibrium versus no-arbitrage

Equilibrium (endogenous) models treat $r$ as a time-homogeneous state variable, so the whole curve $T \mapsto P(0,T)$ is an output of three or four constants: Vasicek (1977) and Cox, Ingersoll and Ross (1985).
They cannot reprice an arbitrary market curve, which rules them out for pricing anything hedged with the curve.
No-arbitrage (exogenous) models take today's curve as an input and fit it with a deterministic function of time: Ho and Lee (1986), $dr = \theta(t)dt + \sigma dW$, and Hull and White (1990), $dr = (\theta(t) - a r)dt + \sigma dW$.
The curve is then matched by construction and the remaining parameters (mean reversion $a$ and volatility $\sigma$) are free for option calibration.

### The affine machinery

By Feynman-Kac ([note](../04-Stochastic-Calculus/06-Feynman-Kac-and-Pricing-PDEs.md)) a bond price solves
$$\partial_t P + \mu\,\partial_r P + \tfrac12 s^2\,\partial_{rr} P - rP = 0, \qquad P(T,T) = 1.$$
If $\mu$ and $s^2$ are affine in $r$, try $P = A(\tau)e^{-B(\tau)r}$ with $\tau = T - t$ and match the terms in $r^0$ and $r^1$:

| Model | $dr$ | $B'(\tau)$ | $(\ln A)'(\tau)$ |
| :--- | :--- | :--- | :--- |
| Vasicek | $k(\theta - r)dt + \sigma dW$ | $1 - kB$ | $-k\theta B + \tfrac12\sigma^2 B^2$ |
| CIR | $k(\theta - r)dt + \sigma\sqrt{r}\,dW$ | $1 - kB - \tfrac12\sigma^2 B^2$ | $-k\theta B$ |

with $B(0) = 0$, $\ln A(0) = 0$; Vasicek's $B$ is linear and solves to $B = (1 - e^{-k\tau})/k$, CIR's is a Riccati equation.

### Vasicek

$dr = k(\theta - r)dt + \sigma dW$ is an Ornstein-Uhlenbeck process:
$$r(T) = r(t)e^{-k\tau} + \theta(1 - e^{-k\tau}) + \sigma\int_t^T e^{-k(T-u)}dW_u,$$
Gaussian with mean $r(t)e^{-k\tau} + \theta(1 - e^{-k\tau})$ and variance $\frac{\sigma^2}{2k}(1 - e^{-2k\tau})$.
The integral $I = \int_t^T r\,du$ is Gaussian too, with mean $\theta\tau + (r - \theta)B$ and variance $\frac{\sigma^2}{k^2}\left(\tau - B - \frac{k}{2}B^2\right)$, so $P = \mathbb{E}[e^{-I}] = e^{-\mathbb{E}I + \frac12 \text{Var}\,I}$, which gives
$$P(t,T) = A\,e^{-Br}, \qquad B = \frac{1 - e^{-k\tau}}{k}, \qquad \ln A = \left(\theta - \frac{\sigma^2}{2k^2}\right)(B - \tau) - \frac{\sigma^2}{4k}B^2.$$
As $\tau \to \infty$ the yield tends to $\theta - \frac{\sigma^2}{2k^2}$: the long end sits below the long-run mean by a convexity term, because $e^{-I}$ is convex in $I$.
The weakness is the Gaussian distribution: $\mathbb{P}(r(T) < 0) = \Phi(-\mathbb{E}r_T/\text{sd}\,r_T) > 0$, which is a feature in negative-rate markets and a bug for anything that needs $r > 0$.

### Cox-Ingersoll-Ross

$dr = k(\theta - r)dt + \sigma\sqrt{r}\,dW$ keeps $r \ge 0$: the diffusion vanishes at zero while the drift $k\theta$ pushes up.
**Feller condition.** If $2k\theta \ge \sigma^2$, zero is never reached; if $2k\theta < \sigma^2$, the process hits zero and is instantaneously reflected (Feller 1951 for the boundary classification).
**Distribution.** With $c = \frac{2k}{\sigma^2(1 - e^{-k\tau})}$, $2c\,r(T)$ given $r(t)$ is non-central chi-square with $d = 4k\theta/\sigma^2$ degrees of freedom and non-centrality $2c\,r(t)e^{-k\tau}$; that is what exact simulation samples (Glasserman 2004, section 3.4).
**Bond price.** With $\gamma = \sqrt{k^2 + 2\sigma^2}$:
$$B = \frac{2(e^{\gamma\tau} - 1)}{(\gamma + k)(e^{\gamma\tau} - 1) + 2\gamma}, \qquad A = \left(\frac{2\gamma\,e^{(k+\gamma)\tau/2}}{(\gamma + k)(e^{\gamma\tau} - 1) + 2\gamma}\right)^{2k\theta/\sigma^2}.$$
**Simulation.** Plain Euler can step below zero and then needs $\sqrt{r}$ of a negative number; fixes are full truncation (use $\max(r,0)$ in drift and diffusion, Lord, Koekkoek and van Dijk 2010) or exact non-central chi-square sampling.

### Hull-White one factor

$dr = (\theta(t) - a r)dt + \sigma dW$.
Write $r(t) = x(t) + \varphi(t)$ with $dx = -a x\,dt + \sigma dW$, $x(0) = 0$.
Matching $P(0,T) = \mathbb{E}[e^{-\int_0^T r}]$ for every $T$ forces
$$\varphi(t) = f(0,t) + \frac{\sigma^2}{2a^2}\left(1 - e^{-at}\right)^2, \qquad \theta(t) = \partial_t f(0,t) + a f(0,t) + \frac{\sigma^2}{2a}\left(1 - e^{-2at}\right).$$
The last term is a convexity correction: without it, simulated discount factors miss the curve.
Bond prices are affine in $r(t)$ (Brigo and Mercurio, section 3.3):
$$P(t,T) = \frac{P(0,T)}{P(0,t)}\exp\left(B f(0,t) - \frac{\sigma^2}{4a}\left(1 - e^{-2at}\right)B^2 - B\,r(t)\right), \qquad B = \frac{1 - e^{-a(T-t)}}{a}.$$
**Zero-bond options.** $P(T,S)$ is lognormal under the $T$-forward measure with total volatility
$$\sigma_P = \sigma\sqrt{\frac{1 - e^{-2aT}}{2a}}\,B(T,S),$$
so a call is $P(0,S)\Phi(d_1) - K P(0,T)\Phi(d_2)$ with $d_{1,2} = \frac{\ln\frac{P(0,S)}{K P(0,T)} \pm \frac12\sigma_P^2}{\sigma_P}$, a Black formula on the forward bond price.

### Jamshidian's decomposition

A payer swaption expiring at $T$ on a swap with fixed coupons $c_i = K\tau_i$ (plus 1 at $T_n$) pays $\left(1 - \sum_i c_i P(T,T_i)\right)^+$: a put on a coupon bond struck at 1.
In a one-factor model every $P(T,T_i; r)$ is strictly decreasing in $r$, so there is a unique $r^*$ with $\sum_i c_i P(T,T_i;r^*) = 1$.
Set $K_i = P(T,T_i;r^*)$.
Because all bonds move the same way, $1 - \sum c_i P_i > 0 \iff r > r^* \iff P_i < K_i$ for every $i$ simultaneously, so
$$\Big(1 - \sum_i c_i P_i\Big)^+ = \sum_i c_i\,(K_i - P_i)^+,$$
an exact sum of zero-bond puts (Jamshidian 1989).
The receiver swaption is the matching sum of calls.

### Numerical methods

- Trees: the Hull and White (1994) trinomial tree discretises $x$, then shifts each time slice by $\alpha_m$ found by forward induction on Arrow-Debreu prices so that the tree reprices $P(0,t_{m+1})$ exactly; Bermudans are priced by backward induction.
- PDE: the bond-pricing PDE above, solved by Crank-Nicolson; the CIR boundary at $r = 0$ needs care because the diffusion vanishes there.
- Monte Carlo: exact transitions for Gaussian models, exact or full-truncation schemes for CIR; the control that every simulated discount factor reprices the input curve is the first test.

### Limits of one-factor models

- **Correlation.** All instantaneous bond returns load on one Brownian motion, $dP/P = r\,dt - \sigma B(t,T)\,dW$, so their correlation is 1: the model moves the curve, it cannot twist it on its own.
- **Volatility shape.** With constant $a$ and $\sigma$, forward-rate volatility is $\sigma e^{-a(T-t)}$, monotone in maturity, so a humped volatility term structure needs time-dependent $\sigma(t)$ or more factors.
- **Calibration.** A swap rate's variance is roughly $\sum_{i,j} w_i w_j \rho_{ij}\sigma_i\sigma_j$, which is maximal at $\rho = 1$; a one-factor model calibrated to caplets therefore implies the highest swaption volatility consistent with them, and the choice of calibration instruments (co-terminal swaptions for a Bermudan, caplets for a cap-like product) is part of the model.
- **Negative rates.** Gaussian models allow them, lognormal and square-root models do not.

### How it is implemented

```mermaid
flowchart TD
    C[Today's discount curve] --> T["Fit theta(t) or the tree shifts alpha_m"]
    V[Calibration instruments: swaptions or caplets] --> K["Fit a and sigma, or sigma(t)"]
    T --> M[Calibrated model]
    K --> M
    M --> J{Product}
    J -- European swaption or zero-bond option --> A1[Closed form: Jamshidian, Black on bond]
    J -- Bermudan or callable --> A2[Tree or PDE, backward induction]
    J -- path dependent --> A3[Monte Carlo, exact transitions]
    A1 --> X[Checks: reprice curve, reprice calibration set, convergence in steps or paths]
    A2 --> X
    A3 --> X
```

## Worked examples

Every number below is computed, printed and asserted by `code/fi_short_rate.py`; simulation results are quoted as "about" the seed-stable printed value and checked against the closed form within four standard errors.

### Example 1: Vasicek bond price, checked by simulation

$k = 0.30$, $\theta = 4\%$, $\sigma = 1\%$, $r_0 = 3\%$.
Closed form: $P(0,5) = 0.840865$, a 5-year yield of 3.4665%.
Monte Carlo with 100,000 antithetic paths of the exact OU transition (500 steps, seed 7) gives about 0.84086 with a standard error of 4.1e-6.
The long yield is $\theta - \sigma^2/(2k^2) = 3.9444\%$, and the 100-year yield is already 3.9139%.
$r_5$ has mean 3.7769% and standard deviation 1.2584%, so $\mathbb{P}(r_5 < 0) = 0.1345\%$; the simulation shows about 0.127% of paths below zero.

### Example 2: CIR closed form against a PDE

$k = 0.5$, $\theta = 4\%$, $\sigma = 10\%$, $r_0 = 3\%$; the Feller ratio $2k\theta/\sigma^2 = 4.00$.
Closed form $P(0,5) = 0.835234$; a Crank-Nicolson solve of the bond PDE on $r \in [0, 0.6]$ gives 0.835234, differing by -5e-9.
The non-central chi-square has $d = 8$ degrees of freedom here, and 400,000 exact draws (seed 11) give a mean of about 3.92%, matching the exact conditional mean 3.92%.

### Example 3: violating the Feller condition

$k = 0.20$, $\theta = 5\%$, $\sigma = 15\%$: $2k\theta = 0.020 < 0.0225 = \sigma^2$, so zero is attainable.
The closed form still holds: $P(0,5) = 0.836017$, and the PDE agrees to 8e-7, a larger gap than the -5e-9 of Example 2 on the same grid.
With 50 Euler steps a year, 0.34% of all steps land below zero (counted in the full-truncation run, seed 3); plain Euler would have to take the square root of the negative value on the next step, while full truncation gives a Monte Carlo price of about 0.8360 (standard error 3.1e-4), consistent with the closed form.
Lord, Koekkoek and van Dijk (2010) compare the usual fixes (absorption, reflection, partial and full truncation) and recommend full truncation as the least biased of them.

### Example 4: Hull-White fits any curve, and the convexity term is needed

Market curve: a hypothetical Nelson-Siegel zero curve with a 5-year zero of 4.4179%, $P(0,5) = 0.801800$.
Its instantaneous forward starts at $f(0,0) = 3.5\%$ with slope $\partial_t f(0,0) = 0.01$, so with $a = 0.03$, $\sigma = 1.2\%$ the fitted drift starts at $\theta(0) = 0.01 + 0.03 \times 0.035 = 0.01105$ (the convexity term is zero at $t = 0$).
Simulating $dr = (\theta(t) - ar)dt + \sigma dW$ with that $\theta$ (200,000 antithetic paths, seed 21) gives $\mathbb{E}[e^{-\int_0^5 r}] \approx 0.80180$: the curve is recovered.
On the same paths with the term $\frac{\sigma^2}{2a}(1 - e^{-2at})$ removed from $\theta$, the estimate is about 0.80395: the only change is that term, and it moves the 5-year discount factor by about 22 bp of price.

### Example 5: a zero-bond option

1-year option on the 5-year zero, $a = 0.03$, $\sigma = 1.2\%$:
$B(1,5) = (1 - e^{-0.12})/0.03 = 3.769319$, the variance factor $(1 - e^{-0.06})/0.06 = 0.970591$ with square root 0.985186, so $\sigma_P = 0.012 \times 0.985186 \times 3.769319 = 0.044562$.
On the Nelson-Siegel curve, a call struck at the forward bond price $P(0,5)/P(0,1)$ is worth 0.014253; Monte Carlo (seed 5) gives about 0.01426.

### Example 6: a swaption by Jamshidian

Flat 4% continuous curve, 1y into 5y payer at 4%, annual fixed leg, $a = 0.03$, $\sigma = 1.2\%$.
The forward swap rate is 4.0811% on an annuity of 4.267539.
Jamshidian gives 0.021268 per unit notional (212.68 bp); Monte Carlo of the payoff $(1 - \sum c_i P(1,T_i))^+$ (seed 9) gives about 0.02127.

### Example 7: why one factor is not enough

With $a = 0.03$, $\sigma = 1.2\%$ the instantaneous volatility of a 2-year zero is $\sigma B(0,2) = 2.3294\%$ and of a 10-year zero 10.3673%, but both are driven by the same $dW$: a 2s10s steepener cannot happen in this model except through the deterministic drift.

## Pitfalls

- Using naive Euler for CIR when $2k\theta < \sigma^2$: negative rates and a square root of a negative number; use full truncation or exact sampling.
- Fitting $\theta(t)$ without the $\frac{\sigma^2}{2a}(1 - e^{-2at})$ term: the model no longer reprices the curve it was fitted to.
- Differentiating a noisy forward curve to get $\partial_t f(0,t)$: $\theta(t)$ inherits the noise; fit $\varphi(t)$ directly or use a smooth curve.
- Calibrating a one-factor model to caplets and pricing swaptions (or the reverse) without acknowledging the correlation assumption.
- Treating daily recalibrated parameters as if they were constants: the model does not anticipate its own recalibration, and P&L explain shows the jumps.
- Confusing the short rate $r(t)$ with the instantaneous forward $f(t,T)$; in Hull-White $r(t) = x(t) + \varphi(t)$ and $\varphi(t) \ne f(0,t)$.
- Mixing lognormal option formulas with Gaussian rate models when rates can be negative.

## Interview questions

> [!question]- fi-short-rate-vasicek-sde | Write the SDE for the Vasicek model and define all parameters.
> $dr = k(\theta - r)dt + \sigma dW$ under the risk-neutral measure.
> $k > 0$ is the speed of mean reversion, $\theta$ the long-run mean, $\sigma > 0$ the absolute (normal) volatility of the short rate; the solution is Gaussian.

> [!question]- fi-short-rate-vasicek-neg-prob | Why does the Vasicek model allow negative interest rates?
> The diffusion coefficient is constant, so $r(T)$ is Gaussian with support on the whole line and $\mathbb{P}(r_T < 0) = \Phi(-\mathbb{E}r_T/\text{sd}\,r_T) > 0$.
> With $k = 0.3$, $\theta = 4\%$, $\sigma = 1\%$, $r_0 = 3\%$ it is 0.1345% at 5 years.

> [!question]- fi-short-rate-cir-feller | What is the Feller condition in the CIR model and what happens if it is violated?
> $2k\theta \ge \sigma^2$.
> If it holds, zero is unattainable; if not, the process reaches zero and is instantaneously reflected, bond prices are still given by the closed form, but naive Euler simulation produces negative rates and needs full truncation or exact sampling.

> [!question]- fi-short-rate-hw-theta-derivation | Why is $\theta(t)$ in the Hull-White model time-dependent?
> A constant drift gives an endogenous curve with a few degrees of freedom; a deterministic $\theta(t)$ gives one degree of freedom per maturity, enough to match $P(0,T)$ for every $T$.
> The fit is $\theta(t) = \partial_t f(0,t) + a f(0,t) + \frac{\sigma^2}{2a}(1 - e^{-2at})$.

> [!question]- fi-short-rate-jamshidian-trick | Explain the mathematical foundation of Jamshidian's decomposition.
> In a one-factor model every $P(T,T_i;r)$ is strictly decreasing in $r$, so the coupon bond equals the strike at a unique $r^*$ and every bond is above or below its own strike $K_i = P(T,T_i;r^*)$ at the same time.
> Hence $(1 - \sum c_i P_i)^+ = \sum c_i (K_i - P_i)^+$, a sum of zero-bond puts; the note's 1y into 5y payer is 0.021268, confirmed by Monte Carlo.

> [!question]- fi-short-rate-jamshidian-failure | Under what circumstances does Jamshidian's decomposition fail?
> When bond prices are not all monotone in a single state variable: two-factor models (G2++), LMM, stochastic volatility.
> The exercise boundary is then a curve or surface in state space and the max does not distribute over the cash flows.

> [!question]- fi-short-rate-one-factor-correlation | What is the correlation between any two zero-coupon bond returns in a 1-factor short-rate model?
> 1.
> $dP(t,T)/P(t,T) = r\,dt - \sigma B(t,T)\,dW$ for every $T$, the same $dW$ with different loadings (2.3294% for a 2y and 10.3673% for a 10y zero in the note's Hull-White).

> [!question]- fi-short-rate-hw-bond-option-vol | What is the volatility $\sigma_P$ of a zero-coupon bond option expiring at $T$ on a bond maturing at $S$ under Hull-White?
> $\sigma_P = \sigma\sqrt{\frac{1 - e^{-2aT}}{2a}}\,B(T,S)$, the standard deviation of $\ln P(T,S)$: rate variance accumulated to expiry times the bond's duration factor.
> For $a = 0.03$, $\sigma = 1.2\%$, $T = 1$, $S = 5$: $0.012 \times 0.985186 \times 3.769319 = 0.044562$.

> [!question]- fi-short-rate-equilibrium-vs-no-arb | Compare the practical uses of equilibrium vs no-arbitrage short-rate models.
> Equilibrium models (Vasicek, CIR) give closed forms and interpretable constant parameters, useful for teaching, scenario generation and studying term-structure shape, but cannot match today's curve.
> No-arbitrage models (Ho-Lee, Hull-White, Black-Karasinski) fit the curve exactly, so they are the ones used to price and hedge instruments against the curve.

> [!question]- fi-short-rate-tree-induction | Describe how the Hull-White trinomial tree is calibrated.
> Build a tree for the driftless OU state $x$ with spacing $\sigma\sqrt{3\Delta t}$ and mean-reverting branching, truncated where probabilities would go negative.
> Then go forward in time: with Arrow-Debreu prices $Q_{m,j}$ at step $m$, solve in closed form for the shift $\alpha_m$ so that $\sum_j Q_{m,j}e^{-(\alpha_m + x_j)\Delta t} = P(0,t_{m+1})$, and propagate $Q$ (Hull and White 1994).

> [!question]- fi-sr-vasicek-long-yield | What does the Vasicek yield converge to at long maturities, and why is it below $\theta$?
> $\theta - \sigma^2/(2k^2)$, 3.9444% for $\theta = 4\%$, $\sigma = 1\%$, $k = 0.3$.
> $P = \mathbb{E}[e^{-I}] = e^{-\mathbb{E}I + \frac12\text{Var}I}$: Jensen's inequality makes bonds worth more than discounting at the mean rate, so yields sit below it, and $\text{Var}\,I$ grows like $\sigma^2\tau/k^2$.

> [!question]- fi-sr-vasicek-bond-derivation | Derive the Vasicek bond price in two lines.
> $I = \int_t^T r\,du$ is Gaussian with mean $\theta\tau + (r - \theta)B$ and variance $\frac{\sigma^2}{k^2}(\tau - B - \frac{k}{2}B^2)$.
> So $P = e^{-\mathbb{E}I + \frac12\text{Var}I}$, which rearranges to $A e^{-Br}$ with $B = (1 - e^{-k\tau})/k$.

> [!question]- fi-sr-affine-riccati | Plug $P = A(\tau)e^{-B(\tau)r}$ into the CIR pricing PDE. What equations do you get?
> $B' = 1 - kB - \frac12\sigma^2B^2$ and $(\ln A)' = -k\theta B$, with $B(0) = 0$, $A(0) = 1$.
> The $r^1$ terms give the Riccati equation for $B$ (the $\sigma^2 r$ variance contributes $B^2$), the $r^0$ terms give $A$.

> [!question]- fi-sr-cir-distribution | What is the transition distribution of CIR and how do you simulate it exactly?
> $2c\,r(T) \sim \chi'^2_d(\lambda)$ with $c = \frac{2k}{\sigma^2(1 - e^{-k\tau})}$, $d = 4k\theta/\sigma^2$, $\lambda = 2c\,r(t)e^{-k\tau}$.
> Draw a non-central chi-square and divide by $2c$; with $k = 0.5$, $\theta = 4\%$, $\sigma = 10\%$, $d = 8$ and the sample mean matches $\theta + (r_0 - \theta)e^{-k\tau}$.

> [!question]- fi-sr-cir-simulation-scheme | Your CIR Monte Carlo crashes with a math domain error. What happened and what do you change?
> An Euler step took $r$ below zero (here 0.34% of steps with $2k\theta < \sigma^2$) and the next step took $\sqrt{r}$.
> Use full truncation, $\max(r,0)$ inside drift and diffusion, or exact non-central chi-square transitions; among the Euler fixes compared by Lord, Koekkoek and van Dijk (2010), full truncation had the smallest bias.

> [!question]- fi-sr-hw-fit-check | How would you test that a Hull-White implementation really fits the input curve?
> Simulate $r$ with the fitted $\theta(t)$ and check $\mathbb{E}[e^{-\int_0^T r}]$ against $P(0,T)$ within a few standard errors (0.80180 against 0.801800 in the note), and in a tree check that Arrow-Debreu prices sum to $P(0,t_m)$.
> A strong negative control: drop the $\frac{\sigma^2}{2a}(1 - e^{-2at})$ term and the same paths give about 0.80395.

> [!question]- fi-sr-mean-reversion-vol-decay | What does mean reversion do to forward-rate and long-bond volatility in Hull-White?
> Forward-rate volatility is $\sigma e^{-a(T-t)}$, so long forwards move less than short ones, and bond volatility $\sigma B(t,T)$ saturates at $\sigma/a$ instead of growing linearly in maturity.
> Mean reversion is therefore a volatility-term-structure parameter, calibrated from how swaption volatilities change with tenor and expiry.

> [!question]- fi-sr-calibration-judgement | You must price a 10y non-call 1y Bermudan swaption with Hull-White. What do you calibrate to and why?
> The co-terminal European swaptions (1y into 9y, 2y into 8y, ..., 9y into 1y); a common setup fits a time-dependent $\sigma(t)$ to them with $a$ fixed or set from the volatility term structure.
> Those are the options the Bermudan holder chooses among; calibrating to unrelated caplets would misprice the switch option, and the result should be checked against the most expensive co-terminal European, a lower bound.

## In this repo and SDE-Interview-Prep

- Code: [`code/fi_short_rate.py`](code/fi_short_rate.py) computes, prints and asserts every number on this page.
- Prereqs: [Stochastic Differential Equations](../04-Stochastic-Calculus/03-Stochastic-Differential-Equations.md), [Feynman-Kac and Pricing PDEs](../04-Stochastic-Calculus/06-Feynman-Kac-and-Pricing-PDEs.md).
- Next: [Rates Options: Caps and Swaptions](05-Rates-Options-Caps-and-Swaptions.md), [Term Structure Models: HJM, LGM, and LMM](19-Term-Structure-Models-HJM-LGM-LMM.md), [Callable and Bermudan Products](20-Callable-and-Bermudan-Products.md).

## Further reading

- Damiano Brigo and Fabio Mercurio, *Interest Rate Models: Theory and Practice*, 2nd edition (Springer 2006), chapter 3 (one-factor short-rate models: Vasicek, CIR, Hull-White, Jamshidian's formula).
- Oldrich Vasicek, "An Equilibrium Characterization of the Term Structure", *Journal of Financial Economics* 5(2), 1977.
- John Cox, Jonathan Ingersoll and Stephen Ross, "A Theory of the Term Structure of Interest Rates", *Econometrica* 53(2), 1985.
- Thomas Ho and Sang-Bin Lee, "Term Structure Movements and Pricing Interest Rate Contingent Claims", *Journal of Finance* 41(5), 1986.
- John Hull and Alan White, "Pricing Interest-Rate-Derivative Securities", *Review of Financial Studies* 3(4), 1990.
- John Hull and Alan White, "Numerical Procedures for Implementing Term Structure Models I: Single-Factor Models", *Journal of Derivatives* 2(1), 1994.
- Farshid Jamshidian, "An Exact Bond Option Formula", *Journal of Finance* 44(1), 1989.
- William Feller, "Two Singular Diffusion Problems", *Annals of Mathematics* 54(1), 1951.
- Paul Glasserman, *Monte Carlo Methods in Financial Engineering* (Springer 2004), section 3.4 (square-root diffusions).
- Roger Lord, Remmert Koekkoek and Dick van Dijk, "A comparison of biased simulation schemes for stochastic volatility models", *Quantitative Finance* 10(2), 2010.
