---
type: concept
track: [quant-research]
tier: senior
status: draft
prereqs: [short-rate-models, rates-volatility-and-sabr]
est_hours: 6
sources: [Brigo and Mercurio - Interest Rate Models chapters 5 and 6, Leif Andersen and Vladimir Piterbarg - Interest Rate Modeling volume 2]
---

# Term Structure Models: HJM, LGM, and LMM

## TL;DR

Single-factor short-rate models force 100% correlation across all bond yields, making them incapable of pricing or hedging multi-point curve risk.
The Heath-Jarrow-Morton (HJM) framework resolves this by modeling the entire instantaneous forward rate curve $f(t, T)$ simultaneously, proving that no-arbitrage uniquely dictates forward rate drifts from their volatility structures.
Because generic HJM models are non-Markovian and computationally intractable, practitioners rely on separable volatility kernels that collapse the term structure into finite-dimensional state models like the Linear Gauss-Markov (LGM) and Cheyette frameworks.
For exotic multi-rate derivatives, the Libor Market Model (LMM / BGM) models observable discrete market forward rates directly, matching caplet and swaption volatility surfaces with rank-reduced correlation matrices.
In post-LIBOR markets, these frameworks have adapted to backward-looking compounded risk-free rates (SOFR, ESTER).

## Learning objectives

- Formulate the Heath-Jarrow-Morton (HJM) framework and derive the no-arbitrage HJM drift condition under the risk-neutral measure.
- Explain why generic HJM models are path-dependent (non-Markovian) and identify the separable volatility condition that yields Markovian representations.
- Implement the Linear Gauss-Markov (LGM) / Cheyette model and evaluate zero-coupon bond pricing formulas in terms of state variables.
- Formulate the Libor Market Model (LMM / BGM) and derive the drift change between forward measures and the terminal measure.
- Apply PCA and parametric correlation structures to reduce factor dimensionality in multi-rate models.
- Contrast instantaneous forward models with modern post-LIBOR backward-looking compounded SOFR market models.

## Core concepts

### 1. The Heath-Jarrow-Morton (HJM) Framework

David Heath, Robert Jarrow, and Andrew Morton (1992) revolutionized interest rate modeling by taking the entire observed initial forward curve $T \mapsto f(0, T)$ as a fundamental state variable.
Instead of specifying a process for the short rate $r(t)$ and deducing bond prices, HJM models the continuous evolution of instantaneous forward rates $f(t, T)$ directly.

Under the risk-neutral measure $\mathbb{Q}$ driven by a $d$-dimensional standard Brownian motion $W(t)$:
$$df(t, T) = \alpha(t, T) dt + \sigma(t, T) \cdot dW(t)$$
where:
- $\alpha(t, T)$ is the forward rate drift.
- $\sigma(t, T) = (\sigma_1(t, T), \dots, \sigma_d(t, T))$ is the volatility vector of the forward rate.
- $f(0, T)$ is observed from the market at time 0.

#### The No-Arbitrage HJM Drift Condition
The money-market account is $B(t) = \exp(\int_0^t r(u) du)$, where the instantaneous short rate is $r(t) = f(t, t)$.
The discounted price of any zero-coupon bond $Z(t, T) = \frac{P(t, T)}{B(t)}$ must be a martingale under the risk-neutral measure $\mathbb{Q}$.
Using $P(t, T) = \exp(-\int_t^T f(t, u) du)$ and applying Ito's Lemma, setting the drift of $Z(t, T)$ to zero yields the fundamental **HJM drift condition**:
$$\alpha(t, T) = \sigma(t, T) \cdot \int_t^T \sigma(t, u) du = \sum_{k=1}^d \sigma_k(t, T) \int_t^T \sigma_k(t, u) du$$

This result demonstrates that in an arbitrage-free market, the drift $\alpha(t, T)$ is not an independent parameter; it is completely and uniquely determined by the volatility structure $\sigma(t, T)$.
Once the volatility surface is specified, the risk-neutral evolution of the entire yield curve is locked.

### 2. The Markovian Problem and Separable Volatilities

Integrating the forward rate dynamics yields:
$$f(t, T) = f(0, T) + \int_0^t \alpha(s, T) ds + \int_0^t \sigma(s, T) \cdot dW(s)$$
Setting $T = t$ gives the short rate:
$$r(t) = f(0, t) + \int_0^t \alpha(s, t) ds + \int_0^t \sigma(s, t) \cdot dW(s)$$

For arbitrary volatility functions $\sigma(s, t)$, $r(t)$ cannot be evaluated from its own current value; it depends on the full path of the Brownian motion from $0$ to $t$.
Generic HJM models are **non-Markovian**.
Pricing exotic path-dependent derivatives or American/Bermudan options requires evaluating an infinite-dimensional state space, which rules out efficient partial differential equations (PDE) and tree algorithms.

#### Separable Volatility Kernels (Cheyette Condition)
To restore a Markovian state representation, the volatility function must be separable:
$$\sigma(t, T) = g(t) h(T)$$
A widely used specification is the exponentially decaying kernel:
$$\sigma(t, T) = \sigma(t) e^{-a(T - t)}$$
When volatility is separable, the term structure can be reconstructed using a low-dimensional Markovian state vector $(x(t), y(t))$:
$$dx(t) = (y(t) - a x(t)) dt + \sigma(t) dW(t)$$
$$dy(t) = (\sigma(t)^2 - 2a y(t)) dt$$
This formulation, developed by Cheyette (1992), enables fast 1D and 2D PDE solvers and recombining trees for Bermudan swaptions while maintaining exact calibration to the initial yield curve.

### 3. The Linear Gauss-Markov (LGM) Model

The Linear Gauss-Markov (LGM) model, popularized by Patrick Hagan, is a practical parameterization of separable Gaussian HJM models.
Instead of tracking instantaneous short rates, LGM defines a single Gaussian state variable $x(t)$ with zero mean and no drift:
$$dx(t) = \sigma(t) dW(t), \quad x(0) = 0$$
where $\sigma(t)$ is a deterministic volatility function.

All zero-coupon bond prices are expressed analytically in terms of $x(t)$:
$$P(t, T) = \frac{P(0, T)}{P(0, t)} \exp\left( -H(t, T) x(t) - \frac{1}{2} H(t, T)^2 \zeta(t) \right)$$
where:
- $H(t, T)$ is a deterministic mean-reversion scale function.
For constant mean reversion $a$: $H(t, T) = \frac{1 - e^{-a(T - t)}}{a}$.
- $\zeta(t) = \int_0^t \sigma(s)^2 e^{-2a(t - s)} ds$ is the cumulative variance of the process.

LGM is functionally equivalent to the 1-factor Hull-White model, but decouples the state variable $x(t)$ from the yield curve baseline $P(0, T)$.
This separation simplifies numerical PDE grids and Monte Carlo simulation paths, making LGM the standard model of choice across Tier-1 investment bank fixed income desks for Bermudan swaptions and callable debt.

### 4. The Libor Market Model (LMM / BGM)

While HJM models continuous instantaneous forward rates $f(t, T)$, real market options (caps, floors, European swaptions) depend on discrete, observable forward rates $L(t; T_{k-1}, T_k)$.
Alan Brace, Dariusz Gatarek, and Marek Musiela (1997), along with Farshid Jamshidian (1997), developed the **Libor Market Model (LMM)** to model market-quoted forward rates directly.

#### Dynamics Under Natural Measures
Let $T_0, T_1, \dots, T_N$ be a discrete tenor structure with accrual fractions $\tau_k = T_k - T_{k-1}$.
Define the forward rate $L_k(t) = L(t; T_{k-1}, T_k)$.
Under its own forward measure $\mathbb{Q}^{T_k}$ (with zero-coupon bond numeraire $P(t, T_k)$), $L_k(t)$ is a martingale:
$$\frac{dL_k(t)}{L_k(t)} = \sigma_k(t) \cdot dW^{T_k}(t)$$
If volatility $\sigma_k(t)$ is deterministic, $L_k(T_{k-1})$ is lognormally distributed, replicating Black's caplet formula exactly by construction.

#### Measure Changes and Terminal Measure Dynamics
To price derivatives whose payoffs span multiple forward rates (such as swaptions, Bermudans, or ratchets), all forward rates $\{L_k(t)\}_{k=1}^N$ must be simulated simultaneously under a single common measure.
Choosing the terminal measure $\mathbb{Q}^{T_N}$ (numeraire $P(t, T_N)$):
The change of measure from $\mathbb{Q}^{T_k}$ to $\mathbb{Q}^{T_N}$ introduces an endogenous drift:
$$\frac{dL_k(t)}{L_k(t)} = \mu_k(t) dt + \sigma_k(t) \cdot dW^{T_N}(t)$$
where the drift is given by:
$$\mu_k(t) = -\sum_{j=k+1}^N \frac{\tau_j L_j(t)}{1 + \tau_j L_j(t)} \sigma_k(t) \cdot \sigma_j(t) \rho_{kj}$$
and $\rho_{kj}$ is the instantaneous correlation between Brownian motions $W_k$ and $W_j$.

Notice that the drift $\mu_k(t)$ depends on the state of all future forward rates $\{L_j(t)\}_{j > k}$.
In a Monte Carlo simulation, a simple Euler step discretizes this drift, but creates significant systemic bias unless a **predictor-corrector** scheme is implemented.

### 5. Factor Reduction and Correlation Structures

In an LMM with 40 quarterly forward rates (a 10-year horizon), a full correlation matrix contains $\frac{40 \times 39}{2} = 780$ pairwise correlations.
Simulating 40 independent Brownian motions is computationally expensive and overfits market noise.

#### Principal Component Analysis (PCA)
Empirical analysis of global yield curves reveals that 3 factors explain over 99% of yield curve variance:
1. **Level (First Principal Component, ~85-90%):** Parallel shift across all tenors.
2. **Slope (Second Principal Component, ~8-12%):** Steepening or flattening of the curve.
3. **Curvature (Third Principal Component, ~2-4%):** Butterfly twisting (short and long ends moving opposite to intermediate tenors).

Practitioners reduce the rank of the correlation matrix to $d = 2$ or $d = 3$ factors:
$$\rho_{kj} = \sum_{m=1}^d b_{km} b_{jm}$$
where the factor loadings $b_{km}$ are normalized such that $\sum_{m=1}^d b_{km}^2 = 1$.
This guarantees that the correlation matrix is positive semi-definite and drastically speeds up Monte Carlo simulations.

#### Parametric Correlation Kernels
A popular parametric correlation formulation is the Rebonato exponential kernel:
$$\rho_{kj} = e^{-\beta |T_k - T_j|}$$
or the two-parameter Schoenmakers-Coffey specification, which ensures that long-dated rates decorrelate smoothly without becoming negative.

### 6. The Post-LIBOR Paradigm: Compounded SOFR Market Models

With the cessation of USD LIBOR and the global adoption of Risk-Free Rates (SOFR, ESTER, SONIA), forward rates are no longer known in advance at $T_{k-1}$.
Instead, floating coupons are determined by **backward-looking overnight compounding**:
$$R_k = \frac{1}{\tau_k}\left( \prod_{d=1}^{M_k} \left(1 + r_d \Delta t_d\right) - 1 \right)$$
Because the rate accumulates daily and is fully determined only at payment date $T_k$, modern market models define:
1. Extended HJM models driven by overnight rate volatilities.
2. Discrete Forward-Looking SOFR models calibrated directly to SOFR swaptions and SOFR futures.
The absence of credit risk between banks also simplifies multi-curve discounting, unifying the pricing and discounting curves under the risk-free overnight index.

## Worked examples

### Example 1: Deriving the Ho-Lee HJM Drift
Consider a 1-factor HJM model with constant volatility $\sigma(t, T) = \sigma$.
Derive the no-arbitrage drift $\alpha(t, T)$ and show that it corresponds to the Ho-Lee model.

Apply the HJM drift condition:
$$\alpha(t, T) = \sigma(t, T) \int_t^T \sigma(t, u) du$$
Because $\sigma$ is constant:
$$\alpha(t, T) = \sigma \int_t^T \sigma du = \sigma [\sigma (T - t)] = \sigma^2 (T - t)$$
The forward rate dynamics are:
$$df(t, T) = \sigma^2 (T - t) dt + \sigma dW(t)$$
This is the continuous-time Ho-Lee term structure model.
Notice that the drift grows linearly with time to maturity $T - t$, reflecting cumulative Jensen convexity.

### Example 2: Deriving the Hull-White HJM Drift
Consider an exponentially decaying volatility structure:
$$\sigma(t, T) = \sigma e^{-a(T - t)}$$
where $\sigma > 0$ and $a > 0$.
Derive the HJM drift $\alpha(t, T)$.

Apply the drift condition:
$$\alpha(t, T) = \sigma e^{-a(T - t)} \int_t^T \sigma e^{-a(u - t)} du$$
Evaluate the integral:
$$\int_t^T e^{-a(u - t)} du = \left[ -\frac{e^{-a(u - t)}}{a} \right]_t^T = \frac{1 - e^{-a(T - t)}}{a}$$
Multiply by the leading term:
$$\alpha(t, T) = \sigma e^{-a(T - t)} \times \sigma \left(\frac{1 - e^{-a(T - t)}}{a}\right) = \frac{\sigma^2}{a} e^{-a(T - t)} \left(1 - e^{-a(T - t)}\right)$$
This volatility structure corresponds to the 1-factor Hull-White (extended Vasicek) model.
The forward rate volatility decays exponentially with maturity, preventing the explosive long-term variance seen in the Ho-Lee model.

### Example 3: 2-Factor LMM Drift Calculation
Consider an LMM with two quarterly forward rates $L_1$ and $L_2$ ($T_1 = 0.5\text{y}$, $T_2 = 0.75\text{y}$, $\tau_2 = 0.25$).
Let $L_2(t) = 4.0\% = 0.04$, with volatility $\sigma_1 = 20.0\%$ and $\sigma_2 = 18.0\%$.
The correlation between $L_1$ and $L_2$ is $\rho_{12} = 0.85$.
Calculate the drift of $L_1(t)$ under the terminal measure $\mathbb{Q}^{T_2}$.

Using the LMM drift formula:
$$\mu_1(t) = -\frac{\tau_2 L_2(t)}{1 + \tau_2 L_2(t)} \sigma_1 \sigma_2 \rho_{12}$$
Compute the denominator:
$$1 + \tau_2 L_2(t) = 1 + 0.25 \times 0.04 = 1.01$$
Compute the numerator:
$$\tau_2 L_2(t) = 0.25 \times 0.04 = 0.01$$
$$\sigma_1 \sigma_2 \rho_{12} = 0.20 \times 0.18 \times 0.85 = 0.0306$$
Evaluate the drift:
$$\mu_1(t) = -\frac{0.01}{1.01} \times 0.0306 = -0.009901 \times 0.0306 = -0.000303 = -3.03 \text{ bps/year}$$
Under the terminal measure $\mathbb{Q}^{T_2}$, the forward rate $L_1(t)$ drifts downward at approximately $3.03\text{ bps}$ per annum due to the covariance with the discounting bond $P(t, T_2)$.

## Pitfalls

- **Euler simulation without predictor-corrector in LMM:** In the Libor Market Model, drifts depend on the state variables $L_j(t)$; standard Euler discretization evaluates drift only at the start of the step, introducing a persistent upward bias in simulated forward rates that misprices multi-callable derivatives.
- **Path-dependent explosion in generic HJM:** Implementing an HJM model with non-separable volatility (e.g. power-law decay) forces simulation paths to retain the entire history of Brownian increments; calculating state transitions becomes computationally prohibitive ($O(N^2)$ memory and time).
- **Inconsistent cap and swaption calibration:** Caplets depend on individual forward rate volatilities $\sigma_k$, while swaptions depend on the joint covariance matrix $\sigma_k \sigma_j \rho_{kj}$; calibrating LMM to caps without regularizing the correlation matrix produces negative eigenvalues and spurious correlation estimates.
- **Ignoring negative rates in lognormal LMM:** Standard BGM assumes lognormal dynamics $\frac{dL}{L} = \dots$; in negative or near-zero rate environments, this produces division-by-zero errors; models must be reformulated as Displaced Diffusion LMM or Normal LMM.
- **Confounding terminal measure with spot measure:** Simulating a 30-year swap under the terminal measure $\mathbb{Q}^{T_{120}}$ produces extreme variance in short-dated cash flows because numeraire volatility is high; simulating under the spot money-market measure $\mathbb{Q}^*$ stabilizes variance across all horizons.

## Interview questions

> [!question]- fi-tsm-hjm-drift-condition | State the Heath-Jarrow-Morton (HJM) drift condition and explain its economic significance.
> The condition is $\alpha(t, T) = \sigma(t, T) \cdot \int_t^T \sigma(t, u) du$.
> It proves that in an arbitrage-free market, the drift of every instantaneous forward rate under the risk-neutral measure is completely determined by its volatility structure; quants do not calibrate drift independently.

> [!question]- fi-tsm-hjm-non-markovian | Why is a generic HJM model non-Markovian?
> Integrating forward rate dynamics reveals that the short rate $r(t) = f(t, t)$ depends on the entire path of Brownian motion from time $0$ to $t$.
> Unless the volatility kernel is separable, $r(t)$ cannot be summarized by a finite number of state variables, preventing the use of standard PDEs or trees.

> [!question]- fi-tsm-cheyette-separable | What condition on volatility makes an HJM model Markovian?
> The volatility kernel must be separable: $\sigma(t, T) = \sum_{k=1}^m g_k(t) h_k(T)$.
> Under this condition (such as exponential decay $\sigma e^{-a(T-t)}$), the term structure can be mapped to an $m$-dimensional Markovian state system (Cheyette / LGM model).

> [!question]- fi-tsm-lmm-bgm-definition | What is the Libor Market Model (LMM / BGM) and what was its main advantage over HJM?
> LMM models observable, discrete market forward rates $L(t; T_{k-1}, T_k)$ rather than continuous unobservable instantaneous rates.
> Its main advantage is that under each rate's natural forward measure, the forward rate is lognormal, reproducing the standard Black-76 caplet formula by construction.

> [!question]- fi-tsm-lmm-terminal-drift | Write the drift of forward rate $L_k(t)$ under the terminal measure $\mathbb{Q}^{T_N}$ in LMM.
> $\mu_k(t) = -\sum_{j=k+1}^N \frac{\tau_j L_j(t)}{1 + \tau_j L_j(t)} \sigma_k(t) \cdot \sigma_j(t) \rho_{kj}$.
> The drift is determined by the covariance of $L_k$ with all subsequent forward rates that enter the Radon-Nikodym derivative between measures.

> [!question]- fi-tsm-pca-three-factors | What are the three primary factors discovered by PCA on interest rate curves?
> Level (parallel shift, ~85-90% of variance), Slope (steepening/flattening, ~8-12% of variance), and Curvature (butterfly twist, ~2-4% of variance).

> [!question]- fi-tsm-lgm-vs-hw | How does the Linear Gauss-Markov (LGM) model differ from the 1-factor Hull-White model?
> Mathematically, both span the same Gaussian distribution of zero-coupon bond prices.
> Functionally, LGM formulates the state variable $x(t)$ with zero drift and defines bond prices as closed-form functions of $x(t)$ and initial market discount factors, making numerical PDE boundaries and calibrations significantly simpler.

> [!question]- fi-tsm-predictor-corrector | Why is a predictor-corrector scheme necessary when simulating LMM?
> The drift of each forward rate depends on the forward rates themselves.
> A standard Euler step evaluates the drift only at the current state, accumulating large discretization errors over long paths; predictor-corrector computes an intermediate predicted state to average the drift, removing systemic pricing bias.

> [!question]- fi-tsm-rank-reduction-why | Why do quants reduce the rank of the correlation matrix in LMM?
> Full correlation matrices for 40+ tenors are noisy, overfit historical data, and can fail to be positive semi-definite.
> Reducing the rank to 2 or 3 factors preserves the dominant economic drivers (level, slope, curvature), enforces positive semi-definiteness, and drastically reduces Monte Carlo simulation runtime.

> [!question]- fi-tsm-sofr-vs-libor-modeling | How has term structure modeling changed in the post-LIBOR SOFR era?
> LIBOR forward rates were known at the start of the accrual period (in advance).
> SOFR coupons compound daily overnight in arrears, meaning the final fixing is unknown until the payment date.
> Models now parameterize backward-looking compounded rates directly or use continuous HJM models calibrated to overnight index swaps.

## Further reading

- David Heath, Robert Jarrow, and Andrew Morton, *Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation*, Econometrica, 1992.
- Alan Brace, Dariusz Gatarek, and Marek Musiela, *The Market Model of Interest Rate Dynamics*, Mathematical Finance, 1997.
- Leif Andersen and Vladimir Piterbarg, *Interest Rate Modeling*, Volume 2: "Term Structure Models", Atlantic Financial Press, 2010.
- Patrick Hagan, *Evaluating and Hedging Exotic Swap Instruments via LGM*, Wilmott Magazine, 2005.

## In this repo and SDE-Interview-Prep

- Code: [`code/rates_models.py`](code/rates_models.py) (Hull-White 1F, Jamshidian swaption, and trinomial tree implementation).
- Prereq: [Short-Rate Models](04-Short-Rate-Models.md), [Rates Volatility and SABR](18-Rates-Volatility-and-SABR.md).
- Next: [Callable and Bermudan Products](20-Callable-and-Bermudan-Products.md).
