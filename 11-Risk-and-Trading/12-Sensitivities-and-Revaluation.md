---
type: concept
track: [quant-research, quant-dev]
tier: advanced
status: draft
prereqs: [risk-factor-modelling, the-greeks]
est_hours: 5
sources: [Antoine Savine - Modern Computational Finance AAD and Parallel Simulations, Paul Glasserman - Monte Carlo Methods in Financial Engineering chapter 7, Bruce Tuckman and Angel Serrat - Fixed Income Securities chapter 15, Basel Committee on Banking Supervision - MAR21 Standardised Approach]
---

# Sensitivities and Revaluation

## TL;DR

Risk engines face a fundamental trade-off between computational latency and mathematical accuracy when pricing portfolios across thousands of simulated scenarios: Full Revaluation versus Sensitivity-Based Proxies.
Full revaluation prices every contract through its complete pricing library under each scenario, ensuring perfect non-linear fidelity at the cost of massive computational burden ($O(K \cdot M)$ for $K$ scenarios and $M$ trades).
Sensitivity proxies approximate scenario P&L via first-order (Delta) or second-order (Delta-Gamma and Cross-Gamma) Taylor expansions, reducing revaluation to vectorized matrix multiplication.
Finite difference bumping requires careful selection of optimal step size $h \approx \epsilon_{\text{mach}}^{1/3} x$ to balance $O(h^2)$ truncation error against catastrophic floating-point cancellation.
Modern quantitative production architectures employ Adjoint Algorithmic Differentiation (AAD) to compute exact analytic Greeks across thousands of factors in runtime equivalent to a single pricing function evaluation, alongside Chebyshev grid interpolation for non-linear exotic books.

## Learning objectives

- Contrast Full Revaluation against Taylor series approximations across computational cost, memory bandwidth, and tail accuracy.
- Derive optimal step sizes for forward, backward, and central finite difference bumping.
- Construct the full Hessian matrix, distinguishing diagonal gamma from off-diagonal cross-gamma terms.
- Formulate the computational principles of Adjoint Algorithmic Differentiation (AAD) and explain how it evaluates gradients in $O(1)$ time relative to pricing.
- Quantify proxy approximation error using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and maximum tail divergence.
- Implement Chebyshev polynomial grid revaluation to accelerate Monte Carlo pricing for non-linear multi-asset portfolios.

## Core concepts

### Full Revaluation vs. Sensitivity Proxies

When evaluating risk for a portfolio of $M$ financial instruments across $K$ simulated market scenarios:

```mermaid
flowchart TD
  Portfolio[Portfolio of M Trades] --> Choice{Revaluation Architecture}
  Choice -->|Exact / Non-linear| FR[Full Revaluation]
  Choice -->|Taylor Expansion| Proxy[Sensitivity Proxies]
  Choice -->|Precomputed Grid| Grid[Grid / Chebyshev Interpolation]
  FR --> FR_Cost[O(K * M) pricing calls / Exact tail fidelity / High CPU/GPU load]
  Proxy --> Proxy_Cost[Vectorized dot products / Ultra-fast / Breaks down on barrier/tail options]
  Grid --> Grid_Cost[Fast spline evaluation / Bounded error / Memory intensive]
```

#### 1. Full Revaluation
In full revaluation, the risk engine executes the full closed-form, tree, PDE, or Monte Carlo pricing function for every trade $i$ under each shocked risk factor vector $\mathbf{x}_k = \mathbf{x}_0 + \Delta \mathbf{x}_k$:

$$\Delta V_{\text{portfolio}}(\Delta \mathbf{x}_k) = \sum_{i=1}^M \left[ V_i(\mathbf{x}_0 + \Delta \mathbf{x}_k) - V_i(\mathbf{x}_0) \right]$$

- **Strengths:** 100% pricing fidelity; natively captures all higher-order Greeks, path dependencies, barrier crossings, and non-smooth payoffs.
- **Weaknesses:** Computationally demanding. For a bank with 500,000 trades evaluated across 10,000 historical or Monte Carlo scenarios, full revaluation requires 5 billion pricing calls, exceeding overnight batch windows unless accelerated by massive GPU clusters.

#### 2. Sensitivity-Based Proxies (Taylor Expansion)
The sensitivity approach precomputes portfolio Greeks at the base state $\mathbf{x}_0$, approximating scenario P&L via polynomial expansion:

- **Delta-Only (Linear) Proxy:**

$$\Delta V_k \approx \mathbf{\delta}^T \Delta \mathbf{x}_k = \sum_{j=1}^N \delta_j \cdot \Delta x_{j, k}$$

- **Delta-Gamma (Quadratic) Proxy:**

$$\Delta V_k \approx \mathbf{\delta}^T \Delta \mathbf{x}_k + \frac{1}{2} \Delta \mathbf{x}_k^T \mathbf{\Gamma} \Delta \mathbf{x}_k = \sum_{j=1}^N \delta_j \Delta x_{j, k} + \frac{1}{2}\sum_{i=1}^N \sum_{j=1}^N \Gamma_{ij} \Delta x_{i, k} \Delta x_{j, k}$$

- **Strengths:** Extreme speed. Revaluation reduces to standard matrix-vector operations executed in milliseconds using BLAS libraries.
- **Weaknesses:** Truncation error. For large market moves (3+ standard deviations), Taylor approximations diverge significantly, particularly for discontinuous payoffs (digitals, barrier options) and deep OTM optionality.

### Finite Difference Bumping Mechanics

When analytical formulas for sensitivities are unavailable, quants estimate derivatives numerically via finite difference bumping:

1. **Forward Difference:**

$$\delta_i \approx \frac{V(x_i + h) - V(x_i)}{h}, \quad \text{Truncation Error} = O(h)$$

2. **Central Difference:**

$$\delta_i \approx \frac{V(x_i + h) - V(x_i - h)}{2h}, \quad \text{Truncation Error} = O(h^2)$$

3. **Second Derivative (Diagonal Gamma):**

$$\Gamma_{ii} \approx \frac{V(x_i + h) - 2V(x_i) + V(x_i - h)}{h^2}, \quad \text{Truncation Error} = O(h^2)$$

4. **Cross-Derivative (Cross-Gamma):**

$$\Gamma_{ij} \approx \frac{V(x_i + h_i, x_j + h_j) - V(x_i + h_i, x_j - h_j) - V(x_i - h_i, x_j + h_j) + V(x_i - h_i, x_j - h_j)}{4 h_i h_j}$$

Evaluating the full $N \times N$ Hessian matrix requires $2N$ bumps for diagonal terms and $4 \times \frac{N(N-1)}{2} = 2N(N-1)$ bumps for off-diagonal terms, totaling $2N^2$ pricing evaluations.

#### Optimal Bump Size Selection
Selecting bump size $h$ involves balancing two opposing error sources:
- **Truncation Error:** Increases with larger $h$ (due to neglected higher-order Taylor terms).
- **Floating-Point Cancellation Error:** Increases with smaller $h$ as subtracting two nearly identical floating-point numbers loses significant digits:

$$\text{Roundoff Error} \sim \frac{\epsilon_{\text{mach}} |V|}{h}$$

where $\epsilon_{\text{mach}} \approx 2.22 \times 10^{-16}$ for standard IEEE 754 64-bit floating point.
Minimizing total error yields the optimal bump sizes:
- For **Central Difference First Derivative**:

$$h_{\text{opt}} \approx \epsilon_{\text{mach}}^{1/3} \cdot x \approx (2.22 \times 10^{-16})^{1/3} \cdot x \approx 6.06 \times 10^{-6} \cdot x$$

- For **Second Derivative (Gamma)**:

$$h_{\text{opt, gamma}} \approx \epsilon_{\text{mach}}^{1/4} \cdot x \approx (2.22 \times 10^{-16})^{1/4} \cdot x \approx 1.22 \times 10^{-4} \cdot x$$

In financial practice, traders adopt standardized basis point bumps: $1 \text{ bp}$ ($0.0001$) for rates and credit, $0.1\%$ to $1.0\%$ relative for spot equities, and $0.01$ ($1\text{ vol point}$) for implied volatility.

### Adjoint Algorithmic Differentiation (AAD)

For complex computational graphs (e.g., multi-curve fixed income trees or Monte Carlo XVA simulations), finite difference bumping scales linearly with factor count ($O(N)$ revaluations for gradient, $O(N^2)$ for Hessian).
Adjoint Algorithmic Differentiation (AAD) applies the reverse chain rule to the execution graph of the pricing function.
Instead of propagating perturbations forward, AAD records the forward execution trace (the "tape") and sweeps backward, propagating adjoints (sensitivities $\bar{x} = \frac{\partial V}{\partial x}$) from the output scalar back to all inputs simultaneously.

Key AAD performance advantages:
- **Dimension Independence:** Computing the full gradient vector $\nabla V = [\frac{\partial V}{\partial x_1}, \dots, \frac{\partial V}{\partial x_N}]$ takes a constant multiple of a single forward pricing run (typically $3\times$ to $5\times$ cost of $V$), completely independent of factor dimension $N$.
- **Zero Truncation Error:** AAD computes mathematically exact floating-point derivatives, eliminating finite difference step-size tuning and cancellation errors.

### Grid Revaluation and Polynomial Interpolation

For portfolios containing exotic options with localized non-linearities, sensitivity proxies fail while full revaluation is too slow.
Production risk engines deploy grid-based proxy models:
1. Define a bounded multidimensional domain around base factor values (e.g., $\pm 4$ standard deviations).
2. Precompute exact prices on a structured grid of Chebyshev collocation nodes.
3. Fit multidimensional Chebyshev polynomials or tensor-product cubic splines.
4. During scenario revaluation, evaluate the analytic polynomial representation in microseconds per scenario, achieving $100\times$ speedups with bounded approximation error ($< 0.1\%$).

## Worked examples

### Example 1: Finite Difference Bump Size Optimization

An equity derivatives desk computes the Gamma of an at-the-money call option with underlying spot price $S = \$100.00$.
The pricing function returns double precision floating-point numbers ($\epsilon_{\text{mach}} \approx 2.22 \times 10^{-16}$).
1. Calculate the theoretically optimal central difference bump size $h_{\text{opt}}$ for Delta.
2. Calculate the optimal bump size $h_{\text{gamma}}$ for Gamma.
3. Demonstrate the effect of an excessively small bump size ($h = 10^{-10}$) versus optimal bump ($h = 0.01$).

**Solution:**

Step 1: Optimal Delta bump size:

$$h_{\text{opt, delta}} = \epsilon_{\text{mach}}^{1/3} \times S \approx (2.22 \times 10^{-16})^{1/3} \times 100 \approx 6.06 \times 10^{-6} \times 100 \approx 0.000606 \quad (\$0.06 \text{ cents})$$

In practice, a $\$0.01$ (1 cent) or $\$0.05$ bump is standard.

Step 2: Optimal Gamma bump size:

$$h_{\text{opt, gamma}} = \epsilon_{\text{mach}}^{1/4} \times S \approx (2.22 \times 10^{-16})^{1/4} \times 100 \approx 1.22 \times 10^{-4} \times 100 \approx 0.0122 \quad (\$1.22 \text{ cents})$$

Gamma requires a larger bump size because dividing by $h^2$ squares any floating-point cancellation error.

Step 3: Numerical cancellation demonstration:
Suppose $V(100) = 10.450583572186$.
With $h = 10^{-10}$, $V(100 + h) = 10.450583572249$.
Subtracting the two numbers:

$$V(100 + h) - V(100) = 0.000000000063$$

The top 10 significant digits completely canceled out, leaving only 2 reliable digits of precision.
Dividing by $h = 10^{-10}$ yields $0.63$, introducing massive numerical noise.
With $h = 0.01$, subtraction preserves 12+ digits of precision, providing a clean, stable derivative.

### Example 2: Revaluation Comparison Diagnostics

Using the reference implementation in `code/risk_analytics.py`, compare Full Revaluation against a Delta-Gamma Taylor proxy for a portfolio across 2,000 correlated scenarios.
The portfolio Greeks at base factors are:
- Spot $S = 100.0$, Delta $\delta = 0.6368$, Gamma $\Gamma = 0.0188$.
- Base option value $V_0 = 10.4506$.
Under 2,000 generated Monte Carlo scenarios:
- Mean Absolute Error (MAE): $0.1193$
- Root Mean Squared Error (RMSE): $0.4038$
- 99% Full Revaluation VaR: $\$10.68$
- 99% Delta-Gamma Proxy VaR: $\$9.01$
- 99% Full Revaluation Expected Shortfall: $\$11.80$
- 99% Delta-Gamma Proxy Expected Shortfall: $\$10.33$

Analyze the error metrics and explain why the Taylor proxy understates 99% VaR.

**Solution:**

Step 1: Analyze Error Diagnostics:
- The MAE across all 2,000 scenarios is low ($\$0.12$ on a $\$10.45$ option, $\approx 1.1\%$), confirming that for small and moderate moves ($\pm 1$ standard deviation), the Delta-Gamma expansion tracks full revaluation with high fidelity.
- The RMSE ($\$0.40$) is noticeably higher than MAE, indicating that errors are concentrated in the tails.

Step 2: Tail Divergence Analysis:
- Full 99% VaR is $\$10.68$, while Proxy 99% VaR is $\$9.01$, underestimating tail risk by $\$1.67$ ($15.6\%$).
- Expected Shortfall is similarly underestimated ($\$11.80$ full vs $\$10.33$ proxy).
- Economic cause: A long call option has bounded downside (maximum loss is the premium $\$10.45$). When underlying spot drops heavily, full revaluation price converges asymptotically to $0$. However, a quadratic Taylor polynomial $V_0 + \delta \Delta S + \frac{1}{2}\Gamma (\Delta S)^2$ is a parabola: for very large negative $\Delta S$, the positive $\frac{1}{2}\Gamma (\Delta S)^2$ term begins turning upward, artificially reducing estimated losses and understating true tail VaR.

## Pitfalls

- **Catastrophic Cancellation from Microscopic Bumps:** Setting bump size $h = 10^{-9}$ or smaller in finite difference routines causes catastrophic floating-point cancellation, injecting pure random roundoff noise into Greeks.
- **Ignoring Cross-Gamma in Multi-Asset Books:** Relying on diagonal-only gammas in multi-asset baskets assumes risk factors interact independently, completely missing large cross-factor P&L shifts ($\frac{\partial^2 V}{\partial x_i \partial x_j} \Delta x_i \Delta x_j$).
- **Taylor Breakdown on Discontinuous Payoffs:** Applying Delta-Gamma proxies to digital options, barrier options, or structured credit tranches produces catastrophic pricing errors near barrier trigger levels.
- **AAD Memory Bloat (Tape Exhaustion):** In unoptimized reverse-mode AAD engines, recording every intermediate floating-point operation in long Monte Carlo paths can exhaust RAM, requiring checkpointing to trade recomputation against memory.
- **Unadjusted Sticky-Strike Assumptions:** When bumping spot price, assuming implied volatility remains fixed (sticky-strike) ignores market smile dynamics (sticky-delta or local volatility), introducing hedge ratio slippage.

## Interview questions

> [!question]- full-revaluation-vs-taylor-tradeoff | What are the core computational and mathematical trade-offs between Full Revaluation and Taylor series proxy models in enterprise risk engines?
> Full Revaluation revalues every trade using its exact pricing library under all scenarios, guaranteeing 100% pricing accuracy and capturing non-linearities, but incurs high computational cost ($O(K \cdot M)$). Taylor series proxies approximate P&L via precomputed Greeks (Delta, Gamma, Vega), executing millions of scenario evaluations in milliseconds via matrix multiplication, but suffer from truncation error in extreme tails and break down for non-smooth payoffs.

> [!question]- optimal-finite-difference-bump-size | Derive the optimal step size $h$ for central difference first derivatives, balancing truncation and cancellation error.
> Central difference truncation error is $O(h^2) \approx c_1 h^2$. Floating-point roundoff cancellation error is $O(\epsilon_{\text{mach}} / h) \approx c_2 \frac{\epsilon_{\text{mach}}}{h}$. Total error $E(h) = c_1 h^2 + c_2 \frac{\epsilon_{\text{mach}}}{h}$ is minimized by setting $\frac{dE}{dh} = 2 c_1 h - c_2 \frac{\epsilon_{\text{mach}}}{h^2} = 0 \implies h^3 \propto \epsilon_{\text{mach}} \implies h_{\text{opt}} \sim \epsilon_{\text{mach}}^{1/3} \cdot x \approx 10^{-5}$ to $10^{-6} \cdot x$.

> [!question]- aad-adjoint-algorithmic-differentiation | What is Adjoint Algorithmic Differentiation (AAD), and why is it revolutionary for quantitative risk management?
> AAD is an exact analytical differentiation technique based on the reverse chain rule. Instead of revaluing the pricing model $N$ times via finite difference bumps ($O(N)$ runtime), AAD records the forward execution tape and sweeps backward once, calculating all partial derivatives with respect to all $N$ input factors simultaneously in $O(1)$ runtime (typically $3-5\times$ the cost of a single pricing call).

> [!question]- diagonal-vs-cross-gamma | Contrast diagonal gamma with cross-gamma, and explain the computational penalty of computing full cross-gamma matrices.
> Diagonal gamma $\Gamma_{ii} = \frac{\partial^2 V}{\partial x_i^2}$ measures curvature with respect to a single risk factor in isolation, requiring $2N$ bumps. Cross-gamma $\Gamma_{ij} = \frac{\partial^2 V}{\partial x_i \partial x_j}$ measures interaction between two distinct factors. Evaluating full cross-gamma requires $2N(N-1)$ additional bumps ($O(N^2)$), which becomes computationally prohibitive for books with thousands of risk factors.

> [!question]- taylor-proxy-tail-underestimation | Why does a Delta-Gamma Taylor proxy often underestimate Value at Risk (VaR) for portfolios containing long options?
> For a long call option, losses are bounded by the paid premium, as the price cannot drop below zero. A second-order Taylor expansion is a symmetric parabola: for severe negative asset shocks, the quadratic $\frac{1}{2}\Gamma (\Delta S)^2$ term begins expanding upward, creating artificial gains that soften simulated losses and cause the proxy to understate 99% tail VaR.

> [!question]- chebyshev-grid-revaluation | How does Chebyshev polynomial interpolation accelerate portfolio revaluation while preserving non-linear accuracy?
> Chebyshev interpolation pre-calculates exact full revaluations on a structured multidimensional grid of Chebyshev collocation nodes across a bounding box of risk factors. It fits smooth orthogonal polynomial surfaces that are evaluated in microseconds during Monte Carlo simulations, eliminating 99% of pricing library calls while guaranteeing uniform minimax error bounds.

> [!question]- barrier-options-taylor-failure | Why do sensitivity proxies fail completely for knock-out barrier options?
> Barrier options have discontinuous second derivatives and sharp delta cliffs near the barrier level. A small move can cause the option to knock out, resulting in a step-function price drop to zero. A smooth polynomial Taylor expansion cannot represent discontinuities, predicting moderate linear or quadratic changes when the contract has actually suffered a total loss.

> [!question]- forward-vs-central-difference | Why is central finite difference preferred over forward difference despite requiring twice as many pricing calls?
> Forward difference $\frac{V(x+h) - V(x)}{h}$ has first-order truncation error $O(h)$, requiring a tiny step size that exacerbates roundoff error. Central difference $\frac{V(x+h) - V(x-h)}{2h}$ causes odd-order error terms to cancel out via symmetry, achieving second-order error $O(h^2)$, providing significantly higher accuracy and numerical stability for a modest $2\times$ computational cost.

> [!question]- basel-frtb-curvature-charge | How does the Basel FRTB Standardised Approach (SbM) compute the Curvature risk charge?
> FRTB SbM calculates Curvature risk as the incremental non-linear loss beyond linear delta: $CVR_k = -\min(V(x_k + h_k) - V(x_k) - \delta_k h_k, V(x_k - h_k) - V(x_k) + \delta_k h_k, 0)$, where $h_k$ is the prescribed regulatory stress bump. This requires two full revaluations per risk factor, explicitly isolating non-linear gamma loss.

> [!question]- floating-point-cancellation-definition | What is catastrophic floating-point cancellation in numerical risk calculations?
> Catastrophic cancellation occurs when two nearly equal floating-point numbers are subtracted. The leading identical significant digits cancel out, shifting remaining unrounded bits into high-significance positions and amplifying floating-point representation noise. In finite difference engines with microscopic bumps, this destroys derivative precision.

## Further reading

- Antoine Savine, *Modern Computational Finance: AAD and Parallel Simulations*, Chapters 1-6.
- Paul Glasserman, *Monte Carlo Methods in Financial Engineering*, Chapter 7: "Sensitivity Estimation".
- Bruce Tuckman and Angel Serrat, *Fixed Income Securities: Tools for Today's Markets*, Chapter 15: "Measuring and Hedging Yield Curve Risk".
- Basel Committee on Banking Supervision, *MAR21: Standardised Approach - Sensitivities-based Method*.
- Mike Giles (2008), "An Extended Collection of Matrix Derivative Results for Forward and Reverse Mode Algorithmic Differentiation".

## In this repo and SDE-Interview-Prep

- Risk factor taxonomy and return conventions: [Risk Factor Modelling](10-Risk-Factor-Modelling.md).
- Python reference implementation of bump engine and Taylor proxy comparison: [risk_analytics.py](code/risk_analytics.py).
- Scenario generation and simulation algorithms: [Scenario Generation](11-Scenario-Generation.md).
- Greek definitions and mathematical derivations: [The Greeks](../05-Derivatives-and-Volatility/05-The-Greeks.md).
