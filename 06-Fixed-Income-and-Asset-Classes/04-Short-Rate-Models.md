---
type: concept
track: [quant-research, quant-risk]
tier: advanced
status: draft
prereqs: [stochastic-differential-equations, swaps-and-curve-building]
est_hours: 5
sources: [Brigo and Mercurio - Interest Rate Models chapters 3 and 4, Steven Shreve - Stochastic Calculus for Finance II chapter 10]
---

# Short-Rate Models

## TL;DR

Short-rate models specify the stochastic evolution of the instantaneous risk-free interest rate $r(t)$ under the risk-neutral measure.
Equilibrium models such as Vasicek and Cox-Ingersoll-Ross (CIR) derive the entire yield curve from a small set of stationary parameters, but fail to match the observed market curve today.
No-arbitrage models such as Hull-White (extended Vasicek) introduce time-dependent drift $\theta(t)$ to match the market discount curve exactly.
Under affine Gaussian dynamics, zero-coupon bond prices are exponential-affine in $r(t)$, enabling closed-form zero-coupon bond option pricing and Jamshidian's decomposition for European swaptions.
Single-factor models drive all yield movements via a single Brownian motion, forcing 100% correlation across maturities; capturing curve twists and slope changes requires multi-factor models.

## Learning objectives

- Differentiate equilibrium models from no-arbitrage term structure models.
- Formulate the Vasicek and CIR stochastic differential equations and evaluate their analytical zero-coupon bond pricing formulas.
- Derive the time-dependent drift $\theta(t)$ in the Hull-White 1-factor model that matches the initial instantaneous forward rate curve.
- Implement Jamshidian's decomposition to price European swaptions as portfolios of zero-coupon bond options.
- State the Feller condition $2k\theta \ge \sigma^2$ for CIR and explain simulation failure modes when it is violated.
- Analyze the structural limitations of 1-factor short-rate models regarding terminal correlation and term structure dynamics.

## Core concepts

### 1. Classification: Equilibrium vs No-Arbitrage

Interest rate term structure models fall into two core philosophical traditions.

Equilibrium models treat the short rate $r(t)$ as an economic state variable governed by a time-homogeneous process.
The yield curve $T \mapsto P(0, T)$ is an endogenous output of the model parameters.
Prominent examples include Vasicek (1977) and Cox, Ingersoll, and Ross (1985).
Because equilibrium models possess only 3 or 4 static parameters, they cannot reprice the rich spectrum of liquid market instruments (cash deposits, futures, swaps) without substantial pricing errors.
For market-making and relative value trading, an endogenous mispricing of liquid benchmark bonds is unacceptable.

No-arbitrage models take the observed market discount curve $T \mapsto P(0, T)$ as an exogenous input and calibrate time-dependent functions to match it perfectly.
Ho and Lee (1986) introduced time-dependent drift without mean reversion: $dr(t) = \theta(t)dt + \sigma dW(t)$.
Hull and White (1990) extended Vasicek by incorporating both mean reversion and time-dependent drift: $dr(t) = (\theta(t) - a r(t))dt + \sigma dW(t)$.
No-arbitrage models guarantee that vanilla instruments reprice at par by construction, leaving model volatility and correlation parameters free to calibrate to option surfaces.

### 2. The Vasicek Model

Vasicek (1977) models the instantaneous short rate as an Ornstein-Uhlenbeck process with constant parameters under the risk-neutral measure:
$$dr(t) = k(\theta - r(t))dt + \sigma dW(t)$$
where $k > 0$ is the mean reversion speed, $\theta$ is the long-term mean rate, $\sigma > 0$ is the volatility, and $W(t)$ is a standard Brownian motion.

Integrating the linear SDE yields the conditional distribution of $r(T)$ given $r(t)$:
$$r(T) = r(t)e^{-k(T-t)} + \theta(1 - e^{-k(T-t)}) + \sigma \int_t^T e^{-k(T-u)}dW(u)$$
The conditional distribution is Gaussian:
$$\mathbb{E}[r(T) \mid r(t)] = r(t)e^{-k(T-t)} + \theta(1 - e^{-k(T-t)})$$
$$\text{Var}(r(T) \mid r(t)] = \frac{\sigma^2}{2k}\left(1 - e^{-2k(T-t)}\right)$$

The zero-coupon bond price is given by $P(t, T) = \mathbb{E}_t\left[\exp\left(-\int_t^T r(u)du\right)\right]$.
Because $\int_t^T r(u)du$ is normally distributed, evaluation of its moment-generating function yields an exponential-affine form:
$$P(t, T) = A(t, T)\exp(-B(t, T)r(t))$$
where:
$$B(t, T) = \frac{1 - e^{-k(T-t)}}{k}$$
$$A(t, T) = \exp\left( \left(\theta - \frac{\sigma^2}{2k^2}\right)(B(t, T) - (T-t)) - \frac{\sigma^2}{4k}B(t, T)^2 \right)$$

The yield to maturity $y(t, T) = -\frac{\ln P(t, T)}{T - t} = \frac{B(t, T)}{T - t}r(t) - \frac{\ln A(t, T)}{T - t}$ is affine in $r(t)$.
As maturity $T \to \infty$, the asymptotic yield approaches:
$$y_\infty = \theta - \frac{\sigma^2}{2k^2}$$
The term $-\frac{\sigma^2}{2k^2}$ is the Jensen convexity adjustment on long-term bond yields.

The major drawback of Vasicek is that $r(T)$ is normally distributed, meaning $r(T)$ can become negative with non-zero probability:
$$\mathbb{P}(r(T) < 0) = \Phi\left( -\frac{\mathbb{E}[r(T)]}{\sqrt{\text{Var}(r(T))}} \right)$$

### 3. The Cox-Ingersoll-Ross (CIR) Model

To prevent negative interest rates, Cox, Ingersoll, and Ross (1985) introduced a square-root diffusion term:
$$dr(t) = k(\theta - r(t))dt + \sigma \sqrt{r(t)} dW(t)$$

Key properties of CIR include:
1. **Feller condition:** If $2k\theta \ge \sigma^2$, the upward drift at near-zero rates dominates diffusion, making the boundary $r=0$ strictly inaccessible.
If $2k\theta < \sigma^2$, the rate can reach zero, where it is instantaneously reflected back into positive territory.
2. **Distribution:** The transition density of $2c r(T)$ given $r(t)$ (where $c = \frac{2k}{\sigma^2(1 - e^{-k(T-t)})}$) follows a non-central chi-square distribution $\chi^2(d, \lambda)$ with degrees of freedom $d = \frac{4k\theta}{\sigma^2}$ and non-centrality parameter $\lambda = 2c r(t)e^{-k(T-t)}$.
3. **Affine bond prices:** Zero-coupon bond prices retain the affine structure $P(t, T) = A(t, T)e^{-B(t, T)r(t)}$, where:
$$B(t, T) = \frac{2(e^{\gamma(T-t)} - 1)}{(\gamma + k)(e^{\gamma(T-t)} - 1) + 2\gamma}$$
$$A(t, T) = \left( \frac{2\gamma e^{(k+\gamma)(T-t)/2}}{(\gamma + k)(e^{\gamma(T-t)} - 1) + 2\gamma} \right)^{2k\theta / \sigma^2}$$
with $\gamma = \sqrt{k^2 + 2\sigma^2}$.

The primary drawback of CIR in practice is analytical rigidity.
It cannot match the initial term structure of interest rates, and discrete Euler-Maruyama simulations can step into negative values if not handled with specialized schemes (such as absorbing boundaries, reflection, or exact non-central chi-square sampling).

### 4. The Hull-White One-Factor Model (Extended Vasicek)

The Hull-White 1-factor model generalizes Vasicek by allowing the drift parameter $\theta(t)$ to be a deterministic function of time:
$$dr(t) = (\theta(t) - a r(t))dt + \sigma dW(t)$$
where $a > 0$ is the constant mean-reversion speed and $\sigma > 0$ is the constant short-rate volatility.

#### Calibration of $\theta(t)$ to the Initial Term Structure
Let $f(0, t) = -\frac{\partial \ln P(0, t)}{\partial t}$ be the instantaneous market forward rate observed at time 0.
To match $P(0, T)$ exactly for all maturities $T$, the drift function must satisfy:
$$\theta(t) = \frac{\partial f(0, t)}{\partial t} + a f(0, t) + \frac{\sigma^2}{2a}\left(1 - e^{-2at}\right)$$

#### Zero-Coupon Bond Pricing Under Hull-White
The bond price formula is exponential-affine:
$$P(t, T) = A(t, T)\exp(-B(t, T)r(t))$$
where:
$$B(t, T) = \frac{1 - e^{-a(T-t)}}{a}$$
$$\ln A(t, T) = \ln \frac{P(0, T)}{P(0, t)} + B(t, T)f(0, t) - \frac{\sigma^2}{4a}\left(1 - e^{-2at}\right)B(t, T)^2$$

Equivalently, expressing the bond price in terms of the initial discount curve directly:
$$P(t, T) = \frac{P(0, T)}{P(0, t)}\exp\left( -B(t, T)(r(t) - f(0, t)) - \frac{\sigma^2}{4a}(1 - e^{-2at})B(t, T)^2 \right)$$

#### Zero-Coupon Bond Options
Hull-White provides an exact closed-form solution for European options on zero-coupon bonds.
Consider a European call option with strike $K$ expiring at time $T$ on a zero-coupon bond maturing at $S > T$.
The price at time $t=0$ is:
$$\text{Call}(0) = P(0, S)\Phi(d_1) - K P(0, T)\Phi(d_2)$$
$$\text{Put}(0) = K P(0, T)\Phi(-d_2) - P(0, S)\Phi(-d_1)$$
where:
$$\sigma_P = \sigma \sqrt{\frac{1 - e^{-2aT}}{2a}} B(T, S) = \frac{\sigma}{a}\left(1 - e^{-a(S-T)}\right)\sqrt{\frac{1 - e^{-2aT}}{2a}}$$
$$d_1 = \frac{\ln\left(\frac{P(0, S)}{K P(0, T)}\right) + \frac{1}{2}\sigma_P^2}{\sigma_P}$$
$$d_2 = d_1 - \sigma_P$$

### 5. Jamshidian's Decomposition

A European swaption can be viewed as an option on a coupon-bearing bond.
Consider a payer swaption with expiry $T$, swap maturity $T_n$, coupon frequency $\tau$, and fixed strike $R_K$.
At expiry $T$, the payer swaption payoff is:
$$\text{Payoff}(T) = \max\left(0, 1 - \sum_{i=1}^n c_i P(T, T_i)\right)$$
where $c_i = R_K \tau$ for $i < n$ and $c_n = 1 + R_K \tau$.

Because $P(T, T_i) = A(T, T_i)\exp(-B(T, T_i)r(T))$ and $B(T, T_i) > 0$, each zero-coupon bond price is a strictly monotonically decreasing function of the short rate $r(T)$.
Consequently, the portfolio value $\Psi(r) = \sum_{i=1}^n c_i P(T, T_i; r)$ is also strictly decreasing in $r$.
There exists a unique critical short rate $r^*$ such that:
$$\sum_{i=1}^n c_i P(T, T_i; r^*) = 1$$
The swaption exercise condition $\Psi(r(T)) < 1$ is equivalent to $r(T) > r^*$.

For each individual maturity $T_i$, define the strike price:
$$K_i = P(T, T_i; r^*)$$
Then for any $r(T)$:
$$\max\left(0, 1 - \sum_{i=1}^n c_i P(T, T_i; r(T))\right) = \sum_{i=1}^n c_i \max(0, K_i - P(T, T_i; r(T)))$$
A European payer swaption decomposes exactly into a portfolio of $n$ European put options on zero-coupon bonds with strikes $K_i$.
A European receiver swaption decomposes into a portfolio of $n$ European call options on zero-coupon bonds.
This result, discovered by Farshid Jamshidian (1989), turns a complex multi-cash-flow swaption pricing problem into an exact sum of analytic Black-style bond options.

### 6. Limitations of 1-Factor Models

Single-factor short-rate models are subject to structural constraints:
1. **Terminal correlation is 1:** Because all zero-coupon bond prices are deterministic functions of a single state variable $r(t)$, instantaneous returns on bonds of all maturities are perfectly correlated:
$$\text{Corr}\left(\frac{dP(t, T_1)}{P(t, T_1)}, \frac{dP(t, T_2)}{P(t, T_2)}\right) = 1.0$$
The model can capture parallel shifts, but cannot generate steepening, flattening, or butterfly curvature shocks autonomously.
2. **Implied volatility term structure:** With constant $a$ and $\sigma$, the volatility of forward rates $f(t, T)$ decays exponentially as $e^{-a(T-t)}$.
This monotonic decay cannot fit humped swaption volatility curves without time-dependent volatility $\sigma(t)$.
3. **Hedging basis risk:** Hedging multi-leg products (such as curve spread options or CMS spread options) using 1-factor models severely misstates residual variance because basis decorrelation is zero by assumption.

## Worked examples

### Example 1: Hull-White B(t, T) and Volatility Factor
Calculate the factor $B(0, 5)$ and the bond option volatility $\sigma_P$ for a 1-year option on a 5-year zero-coupon bond, given $a = 0.03$ and $\sigma = 0.012$ (120 bps).

First, calculate $B(1, 5)$:
$$B(1, 5) = \frac{1 - e^{-0.03 \times (5 - 1)}}{0.03} = \frac{1 - e^{-0.12}}{0.03} = \frac{1 - 0.886920}{0.03} = 3.769318$$

Next, compute the integrated variance factor for $T = 1$:
$$V = \frac{1 - e^{-2 \times 0.03 \times 1}}{2 \times 0.03} = \frac{1 - e^{-0.06}}{0.06} = \frac{1 - 0.941765}{0.06} = 0.970591$$
$$\sqrt{V} = \sqrt{0.970591} = 0.985186$$

Finally, evaluate $\sigma_P$:
$$\sigma_P = \sigma \times \sqrt{V} \times B(1, 5) = 0.012 \times 0.985186 \times 3.769318 = 0.044561$$
The implied volatility of the zero-coupon bond price is approximately 4.456%.

### Example 2: Jamshidian Swaption Pricing Verification
Consider a flat 4.0% continuously compounded yield curve where $P(0, t) = e^{-0.04t}$.
We price a 1y into 5y European payer swaption (strike $R_K = 4.0\%$, annual coupons at $t = 2, 3, 4, 5, 6$) with Hull-White parameters $a = 0.03$ and $\sigma = 0.012$.

Using our reference implementation [`rates_models.py`](code/rates_models.py):
1. The 1-year discount factor is $P(0, 1) = e^{-0.04} = 0.960789$.
2. The root-finding step identifies the critical short rate deviation $r^* - f(0, 1)$ that equates the coupon bond value to 1.0.
3. For each of the 5 coupon cash flows, the individual zero-bond put strike $K_i$ is evaluated.
4. The sum of the 5 zero-bond put option values yields:
$$\text{Swaption Price} = 0.021268 \quad (212.68 \text{ bps})$$
This matches the analytic Jamshidian formula implemented in `hw_swaption_jamshidian`.

### Example 3: CIR Feller Condition Check
Let a CIR process have parameters $k = 0.20$, $\theta = 0.05$, and $\sigma = 0.15$.
Evaluate whether the process can reach zero.

Compute the Feller ratio:
$$2k\theta = 2 \times 0.20 \times 0.05 = 0.020$$
$$\sigma^2 = (0.15)^2 = 0.0225$$
Comparing the values:
$$2k\theta = 0.020 < 0.0225 = \sigma^2$$
The Feller condition is violated ($2k\theta < \sigma^2$).
The origin $r = 0$ is accessible.
When simulated using a standard Euler discretization, the short rate will regularly produce negative numbers.
A simple clipping $\max(0, r)$ creates an artificial probability mass at zero, distorting the pricing of deep out-of-the-money options.

## Pitfalls

- **Ignoring the Feller condition in CIR simulations:** Using naive Euler-Maruyama discretization when $2k\theta < \sigma^2$ generates negative rate values, causing `math.sqrt(r)` to throw domain errors; practitioners must use full-truncation schemes or exact non-central chi-square simulation.
- **Calibrating Hull-White to market caps without accounting for correlation:** Caps are portfolios of caplets, each dependent on a single forward rate, whereas swaptions depend on the joint distribution of multiple forward rates.
Calibrating a 1-factor model to caps will overprice swaptions because the model forces terminal correlation to 1.0.
- **Static vs dynamic calibration:** A time-dependent parameter set $(\theta(t), \sigma(t))$ that perfectly fits today's market prices will experience parameter instability over time, generating dynamic arbitrage if recalibrated daily without regularizing constraints.
- **Negative rates under Gaussian models:** Gaussian models (Vasicek, Hull-White) assign positive probability to negative rates; while realistic in post-2014 EUR or JPY markets, pricing lognormal derivatives directly on Gaussian short rates produces undefined quantities.
- **Confusing short rate $r(t)$ with forward rate $f(t, T)$:** The short rate $r(t)$ is instantaneous spot rate at time $t$, whereas $f(t, T)$ is the forward rate agreed at $t$ for instant $T$.
In Hull-White, $r(t) = f(0, t) + x(t) + \alpha(t)$, requiring explicit separation of stochastic and deterministic components.

## Interview questions

> [!question]- fi-short-rate-vasicek-sde | Write the SDE for the Vasicek model and define all parameters.
> The SDE is $dr(t) = k(\theta - r(t))dt + \sigma dW(t)$.
> Here $k > 0$ is the mean-reversion speed, $\theta$ is the long-term equilibrium rate, $\sigma > 0$ is the volatility of the short rate, and $W(t)$ is standard Brownian motion under the risk-neutral measure.

> [!question]- fi-short-rate-vasicek-neg-prob | Why does the Vasicek model allow negative interest rates?
> Because the diffusion coefficient $\sigma$ is constant, the conditional distribution of $r(T)$ given $r(t)$ is Gaussian with support on $(-\infty, \infty)$.
> The probability of negative rates is $\Phi\left(-\frac{\mathbb{E}[r(T)]}{\sqrt{\text{Var}(r(T))}}\right)$, which is strictly positive for any finite parameters.

> [!question]- fi-short-rate-cir-feller | What is the Feller condition in the CIR model and what happens if it is violated?
> The condition is $2k\theta \ge \sigma^2$.
> If satisfied, the upward mean-reverting drift at low rates dominates the diffusion term $\sigma\sqrt{r}$, guaranteeing that the boundary $r=0$ is strictly inaccessible.
> If violated, the process can touch zero, where it is reflected back into the positive domain.

> [!question]- fi-short-rate-hw-theta-derivation | Why is $\theta(t)$ in the Hull-White model time-dependent?
> In equilibrium models with constant drift, the model yields an endogenous term structure that cannot fit arbitrary market discount curves.
> Making $\theta(t)$ time-dependent provides the infinite-dimensional degree of freedom necessary to match the initial market forward curve $f(0, t)$ and discount factors $P(0, T)$ exactly for all maturities.

> [!question]- fi-short-rate-jamshidian-trick | Explain the mathematical foundation of Jamshidian's decomposition.
> Jamshidian's decomposition prices European options on coupon bonds (swaptions) as sums of options on zero-coupon bonds.
> It works because in a 1-factor model, all zero-coupon bond prices $P(T, T_i; r)$ are strictly decreasing monotonic functions of the single short rate $r(T)$.
> This implies there is a unique threshold $r^*$ where the coupon bond price equals the strike, allowing the global max operator $\max(0, 1 - \sum c_i P_i)$ to distribute across individual cash flows.

> [!question]- fi-short-rate-jamshidian-failure | Under what circumstances does Jamshidian's decomposition fail?
> It fails in multi-factor models (e.g. 2-factor Hull-White, LMM) or stochastic volatility models where bond prices depend on two or more state variables.
> In multi-factor models, the exercise boundary in state space is a curve or surface rather than a single point $r^*$, preventing the payoff operator from distributing into separate 1D zero-coupon options.

> [!question]- fi-short-rate-one-factor-correlation | What is the correlation between any two zero-coupon bond returns in a 1-factor short-rate model?
> The correlation is identically 1.0.
> Because all bond prices $P(t, T) = A(t, T)e^{-B(t, T)r(t)}$ are driven by the single Brownian motion $W(t)$, their stochastic differential terms $dP/P = \mu dt - B(t, T)\sigma dW(t)$ are perfectly collinear.

> [!question]- fi-short-rate-hw-bond-option-vol | What is the volatility $\sigma_P$ of a zero-coupon bond option expiring at $T$ on a bond maturing at $S$ under Hull-White?
> $\sigma_P = \frac{\sigma}{a}(1 - e^{-a(S-T)})\sqrt{\frac{1 - e^{-2aT}}{2a}}$.
> It reflects the rate volatility $\sigma$ scaled by the duration factor $B(T, S)$ and the integrated variance of the mean-reverting process up to option expiry $T$.

> [!question]- fi-short-rate-equilibrium-vs-no-arb | Compare the practical uses of equilibrium vs no-arbitrage short-rate models.
> Equilibrium models (Vasicek, CIR) are used for economic macro modeling and long-term risk management where stationary parameters are desired.
> No-arbitrage models (Hull-White, Black-Karasinski) are required for front-office pricing, market making, and relative value trading because they price vanilla calibration instruments with zero error.

> [!question]- fi-short-rate-tree-induction | Describe how the Hull-White trinomial tree is calibrated.
> Calibration uses forward induction.
> At each time step $m$, the tree calculates Arrow-Debreu state prices $Q(m, j)$ for each node from previous transition probabilities.
> The drift shift $\alpha_m = \alpha(m\Delta t)$ is solved analytically to force the expected discount factor across all nodes at step $m$ to match the market discount factor $P(0, (m+1)\Delta t)$.

## Further reading

- Damiano Brigo and Fabio Mercurio, *Interest Rate Models - Theory and Practice*, Chapter 3: "One-Factor Short-Rate Models".
- Farshid Jamshidian, *An Exact Bond Option Formula for the Heath-Jarrow-Morton Model*, Financial Analysts Journal, 1989.
- John Hull and Alan White, *Pricing Interest-Rate-Derivative Securities*, The Review of Financial Studies, 1990.
- Steven Shreve, *Stochastic Calculus for Finance II: Continuous-Time Models*, Chapter 10: "Term-Structure Models".

## In this repo and SDE-Interview-Prep

- Code: [`code/rates_models.py`](code/rates_models.py) (Hull-White 1F Jamshidian swaption and trinomial tree implementation).
- Next: [Rates Options: Caps and Swaptions](05-Rates-Options-Caps-and-Swaptions.md), [Convexity Adjustments](17-Convexity-Adjustments.md).
