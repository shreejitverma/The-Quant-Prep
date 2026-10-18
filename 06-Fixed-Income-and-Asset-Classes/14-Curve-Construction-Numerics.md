---
type: concept
track: [quant-research, quant-dev, quant-risk]
tier: advanced
status: solid
prereqs: [multi-curve-and-csa-discounting]
est_hours: 5
sources: [Hagan and West - Interpolation Methods for Curve Construction Applied Mathematical Finance 2006, Andersen and Piterbarg - Interest Rate Modeling Volume 1 Foundations, Le Floc'h - More on the Hagan-West Monotone Convex Interpolator 2014, Ballabio - Implementing QuantLib chapter on term structures]
---

# Curve Construction Numerics

## TL;DR

- Curve construction turns a discrete collection of market benchmark quotes into a continuous term structure of discount factors and forward rates.
- Bootstrapping solves sequentially for discount factors pillar by pillar, whereas global optimization solves simultaneously via least-squares or penalized splines.
- Log-linear discount factor interpolation implies piecewise-constant instantaneous forward rates with unphysical discontinuities at pillar dates.
- Standard cubic splines produce smooth zero curves but create dangerous non-local oscillations, frequently generating negative forward rates and false arbitrage.
- The Hagan-West monotone convex method guarantees positive, continuous, and locally monotone instantaneous forward rates.
- The calibration Jacobian matrix $\frac{\partial \mathbf{s}}{\partial \mathbf{z}}$ enables rapid risk mapping, automated recalibration, and algorithmic differentiation.

## Learning objectives

- Select appropriate market instruments across cash, futures, and swap horizons to build a coherent curve.
- Compare sequential bootstrapping against global optimization and explain their trade-offs in execution speed and stability.
- Derive the implied forward rate shapes for linear zero interpolation, log-linear discount interpolation, and cubic splines.
- Explain the mathematical principles of Hagan and West's monotone convex interpolation.
- Model turn-of-year and central bank meeting jumps without corrupting intermediate forward rates.
- Compute the calibration Jacobian analytically and invert it to map zero rate shocks to market quote shocks.

## Core concepts

### Instrument selection across the curve horizon

Constructing an interest rate curve requires dividing the maturity spectrum into distinct segments populated by the most liquid, transparent instruments:
1. Short end ($0$ to $3$ months): cash deposits, overnight repo, and short-term central bank target rate instruments.
2. Short-to-intermediate segment ($3$ months to $2$ or $3$ years): interest rate futures (e.g., 3-month SOFR futures) or forward rate agreements (FRAs). Futures require a convexity adjustment to convert futures rates into forward rates.
3. Long end ($2$ years to $30$ or $50$ years): par interest rate swaps or OIS swaps at benchmark maturities ($2, 3, 5, 7, 10, 15, 20, 30$ years).
Overlapping segments must be resolved carefully: switching from futures to swaps at year 2 requires checking that the implied forward rates across the junction do not produce artificial spikes or kinks.

### Bootstrapping versus global optimization

In sequential bootstrapping, the curve solver proceeds chronologically from the shortest pillar $T_1$ to the longest pillar $T_n$.
Because each benchmark instrument depends only on discount factors up to its own maturity, the calibration system is triangular:
$$P(0, T_k) = g_k\left( s_k; P(0, T_1), \dots, P(0, T_{k-1}) \right).$$
Bootstrapping reprices all benchmark instruments with exact precision (zero calibration residual) in $O(n)$ time.
However, bootstrapping is sensitive to noise: a misquoted or stale rate at an intermediate pillar distorts all subsequent discount factors.
In global optimization, the solver parameterizes the curve (e.g., via B-splines, Nelson-Siegel-Svensson, or tension splines) and minimizes an objective function balancing pricing error and curve roughness:
$$\min_{\boldsymbol{\theta}} \sum_{i=1}^M w_i \left( \pi_i(\boldsymbol{\theta}) - \pi_i^{\text{mkt}} \right)^2 + \lambda \int_0^{T_{\max}} \left[ f''(t; \boldsymbol{\theta}) \right]^2 dt.$$
Global methods handle over-determined systems and noisy quotes gracefully, but do not reprice benchmark instruments exactly, making them unpopular on linear derivatives trading desks that require exact hedge pricing.

### Interpolation schemes and implied forward rates

The choice of interpolation variable and functional form dictates the shape of the instantaneous forward rate $f(0, t) = -\frac{\partial \ln P(0, t)}{\partial t}$:

| Method | Interpolated Variable | Implied Forward Rate $f(0, t)$ | Properties and Production Pitfalls |
| :--- | :--- | :--- | :--- |
| Log-linear on $P$ | $\ln P(t)$ linear | Piecewise constant | Simple, robust, guarantees $P > 0$; forward rates jump discontinuously at pillars. |
| Linear on $z$ | $z(t) = -\frac{\ln P}{t}$ linear | $f(t) = z(t) + t z'(t)$ piecewise linear | $z'(t)$ jumps at each pillar $T_k$, so forwards jump by $T_k$ times that change, giving a saw-tooth. |
| Natural Cubic Spline | $z(t)$ or $P(t)$ $C^2$ cubic | Smooth cubic (spline on $z$) or rational (spline on $P$) | Visually smooth; non-local oscillations can produce negative forward rates. |
| Monotone Convex | Forward rates $f(t)$ | Continuous, monotone | Hagan-West (2006); eliminates spurious oscillations while preserving monotonicity. |

### The Hagan-West monotone convex method

Hagan and West (2006) demonstrated that standard cubic splines produce disastrous anomalies in interest rate risk management.
A localized shock at the 5-year pillar causes cubic splines to oscillate globally, inducing spurious forward rate ripples at the 2-year and 10-year horizons.
Furthermore, in steep yield curve environments, cubic splines frequently dip below zero between pillars.
The Hagan-West algorithm works directly on the discrete forward rates $F_i = \frac{1}{\tau_i}\int_{T_{i-1}}^{T_i} f(u) du$.
It establishes continuous boundary forward values $f_i = f(T_i)$ using local parabolic or harmonic estimates that preserve local monotonicity:
if $F_i < F_{i+1} < F_{i+2}$, then $f$ must be strictly increasing across the intervals.
Within each interval $[T_{i-1}, T_i]$, $f(t)$ is parameterized as a piecewise quadratic function designed to satisfy:
1. Integral constraint: $\frac{1}{\tau_i} \int_{T_{i-1}}^{T_i} f(u) du = F_i$.
2. Boundary continuity: $f(T_{i-1}) = f_{i-1}$ and $f(T_i) = f_i$.
3. Positivity and monotonicity: $f(t) \ge 0$ everywhere, with no local extrema unless required by the discrete forward rates.

### Turn-of-year effects and event dates

Overnight borrowing rates predictably spike or drop over the final days of December as banks shrink balance sheets for regulatory reporting (e.g., G-SIB score calculations and leverage ratio snapshots).
Similarly, scheduled central bank monetary policy announcements (e.g., FOMC or ECB meetings) introduce sharp step-functions into forward curves.
Treating turn-of-year or policy dates with standard smooth interpolation smears the jump across the entire quarter.
Production curve engines handle event dates explicitly:
$$\ln P(0, t) = \ln P_{\text{smooth}}(0, t) - \sum_{k: \tau_k \le t} \Delta_{\text{jump}}^{(k)},$$
where $\Delta_{\text{jump}}^{(k)}$ is the discrete interest rate jump associated with event date $\tau_k$.

### The calibration Jacobian and algorithmic differentiation

Let $\mathbf{s} = (s_1, \dots, s_n)^T$ be the vector of market par swap quotes and $\mathbf{z} = (z_1, \dots, z_n)^T$ be the zero rates at pillar maturities.
The pricing functions define a mapping $\mathbf{s} = \mathbf{g}(\mathbf{z})$.
The calibration Jacobian is the matrix of partial derivatives:
$$J_{\mathbf{s}, \mathbf{z}} = \left[ \frac{\partial s_i}{\partial z_j} \right].$$
Because par swap rate $s_i$ depends on all cash flows up to maturity $T_i$, the Jacobian is lower triangular: $\frac{\partial s_i}{\partial z_j} = 0$ for $j > i$.
Using the chain rule via discount factors $P_k = \exp(-T_k z_k)$:
$$\frac{\partial s_i}{\partial z_j} = \sum_{k=1}^i \frac{\partial s_i}{\partial P_k} \frac{\partial P_k}{\partial z_j} = \frac{\partial s_i}{\partial P_j} \cdot \left( -T_j P_j \right).$$
For a par swap where $s_i = \frac{1 - P_i}{A_i}$ with $A_i = \sum_{k=1}^i P_k$:
$$\frac{\partial s_i}{\partial P_j} = -\frac{s_i}{A_i} \quad (j < i), \qquad \frac{\partial s_i}{\partial P_i} = -\frac{1 + s_i}{A_i}.$$
Inverting $J_{\mathbf{s}, \mathbf{z}}$ via forward substitution provides $J_{\mathbf{z}, \mathbf{s}} = J_{\mathbf{s}, \mathbf{z}}^{-1} = \left[ \frac{\partial z_i}{\partial s_j} \right]$, which transforms zero sensitivities into market quote sensitivities instantly.

### How it is implemented

- Inputs: sorted pillar maturities, benchmark quotes, interpolation method flag, event date jump table.
- Outputs: calibrated discount curve object, analytical calibration Jacobian, inverse Jacobian.
- Algorithm: triangular forward substitution for bootstrapping; Newton-Raphson iteration with Jacobian if non-linear; analytical evaluation of $P(t)$ and $f(t)$.
- Complexity: $O(n)$ for triangular bootstrap; $O(n^2)$ for analytical Jacobian construction and inversion.
- Reference implementation: [`code/fi_curve_numerics.py`](code/fi_curve_numerics.py) provides verified analytical Jacobian and forward jump calculations; [`code/curve_bootstrap.py`](code/curve_bootstrap.py) provides `DiscountCurve`, `swap_jacobian`, and `map_zero_risk_to_par_risk`.
- System context: [the curve and surface service](../18-Pricing-and-Risk-Systems/04-Curve-and-Surface-Service.md).

## Worked examples

All calculations below match the verified assertions in [`code/fi_curve_numerics.py`](code/fi_curve_numerics.py) and [`code/curve_bootstrap.py`](code/curve_bootstrap.py).

### Example 1: implied forward rate jump under log-linear discount interpolation

Consider the calibrated curve from Note 03:
Pillars at $T_1 = 1.0, T_2 = 2.0, T_3 = 3.0$ with discount factors:
$P(1.0) = 0.970874$, $P(2.0) = 0.933352$, $P(3.0) = 0.888299$.
Under log-linear discount factor interpolation, the instantaneous forward rate $f(t) = -\frac{\partial \ln P}{\partial t}$ is piecewise constant across each interval:
Interval $[0, 1.0]$:
$$f_1 = -\frac{\ln P(1.0) - \ln 1.0}{1.0 - 0.0} = -\ln(0.970874) = 0.029559 = 2.9559\%.$$
Interval $[1.0, 2.0]$:
$$f_2 = -\frac{\ln P(2.0) - \ln P(1.0)}{2.0 - 1.0} = -\ln(0.933352 / 0.970874) = -\ln(0.961352) = 0.039414 = 3.9414\%.$$
Interval $[2.0, 3.0]$:
$$f_3 = -\frac{\ln P(3.0) - \ln P(2.0)}{3.0 - 2.0} = -\ln(0.888299 / 0.933352) = -\ln(0.951730) = 0.049474 = 4.9474\%.$$
At exactly $t = 1.0$, the instantaneous forward rate jumps discontinuously from $2.9559\%$ to $3.9414\%$, a discontinuous step of $98.55\text{ bps}$.
At $t = 2.0$, it jumps from $3.9414\%$ to $4.9474\%$, a step of $100.60\text{ bps}$.
While discount factors remain continuous, forward-looking option models (e.g., caps and swaptions) evaluated across pillar boundaries suffer from artificial volatility distortion.

### Example 2: analytical Jacobian matrix construction

Using the same 3-year curve, compute the elements of the calibration Jacobian $J_{\mathbf{s}, \mathbf{z}} = \left[ \frac{\partial s_i}{\partial z_j} \right]$.
Annuities: $A_1 = 0.970874$, $A_2 = 1.904226$, $A_3 = 2.792525$.
Par rates: $s_1 = 0.030, s_2 = 0.035, s_3 = 0.040$.

Row 1 ($s_1 = 1$-year swap):
$$\frac{\partial s_1}{\partial P_1} = -\frac{1 + s_1}{A_1} = -\frac{1.030}{0.970874} = -1.060900.$$
$$\frac{\partial P_1}{\partial z_1} = -1.0 \times P_1 = -0.970874.$$
$$J_{1,1} = \frac{\partial s_1}{\partial z_1} = (-1.060900) \times (-0.970874) = 1.030000.$$

Row 2 ($s_2 = 2$-year swap):
$$\frac{\partial s_2}{\partial P_1} = -\frac{s_2}{A_2} = -\frac{0.035}{1.904226} = -0.018380 \implies J_{2,1} = (-0.018380) \times (-0.970874) = 0.017845.$$
$$\frac{\partial s_2}{\partial P_2} = -\frac{1 + s_2}{A_2} = -\frac{1.035}{1.904226} = -0.543528 \implies J_{2,2} = (-0.543528) \times (-2.0 \times 0.933352) = 1.014606.$$

Row 3 ($s_3 = 3$-year swap):
$$\frac{\partial s_3}{\partial P_1} = -\frac{0.040}{2.792525} = -0.014324 \implies J_{3,1} = (-0.014324) \times (-0.970874) = 0.013907.$$
$$\frac{\partial s_3}{\partial P_2} = -0.014324 \implies J_{3,2} = (-0.014324) \times (-2.0 \times 0.933352) = 0.026739.$$
$$\frac{\partial s_3}{\partial P_3} = -\frac{1.040}{2.792525} = -0.372423 \implies J_{3,3} = (-0.372423) \times (-3.0 \times 0.888299) = 0.992468.$$

The complete Jacobian matrix is:
$$J_{\mathbf{s}, \mathbf{z}} = \begin{pmatrix} 1.030000 & 0 & 0 \\ 0.017845 & 1.014606 & 0 \\ 0.013907 & 0.026739 & 0.992468 \end{pmatrix}.$$
Notice that all diagonal terms are approximately $1.0$, while off-diagonals reflect the impact of short-end zero rates on longer par swap rates.

### Example 3: inverting the Jacobian to map zero risk to par market risk

Inverting $J_{\mathbf{s}, \mathbf{z}}$ via lower triangular forward substitution yields:
$$J_{\mathbf{z}, \mathbf{s}} = J_{\mathbf{s}, \mathbf{z}}^{-1} = \begin{pmatrix} 0.970874 & 0 & 0 \\ -0.017076 & 0.985604 & 0 \\ -0.013144 & -0.026554 & 1.007589 \end{pmatrix}.$$
Now consider a 3-year par bond with cash flows $[4, 4, 104]$ at $T = 1, 2, 3$.
Zero-rate sensitivities: $\frac{\partial PV}{\partial z_k} = -k \cdot CF_k \cdot P_k$.
$$\frac{\partial PV}{\partial z_1} = -1 \cdot 4 \cdot 0.970874 = -3.8835.$$
$$\frac{\partial PV}{\partial z_2} = -2 \cdot 4 \cdot 0.933352 = -7.4668.$$
$$\frac{\partial PV}{\partial z_3} = -3 \cdot 104 \cdot 0.888299 = -277.1493.$$
Multiply by $J_{\mathbf{z}, \mathbf{s}}$ to find market par quote sensitivities $\frac{\partial PV}{\partial s_i} = \sum_k \frac{\partial PV}{\partial z_k} (J_{\mathbf{z}, \mathbf{s}})_{k, i}$:
$$\frac{\partial PV}{\partial s_1} = (-3.8835)(0.970874) + (-7.4668)(-0.017076) + (-277.1493)(-0.013144) = -3.7704 + 0.1275 + 3.6429 = 0.0000.$$
$$\frac{\partial PV}{\partial s_2} = (-7.4668)(0.985604) + (-277.1493)(-0.026554) = -7.3593 + 7.3593 = 0.0000.$$
$$\frac{\partial PV}{\partial s_3} = (-277.1493)(1.007589) = -279.2525 = -100 \cdot A_3.$$
The Jacobian maps zero risk into exact par market risk: the 3-year par bond has zero sensitivity to 1-year and 2-year market par quotes, and exactly $-A_3 \times 100$ sensitivity to the 3-year market quote.

## Pitfalls

- Using natural cubic splines on zero rates without checking for negative instantaneous forward rates between pillars.
- Neglecting the convexity adjustment when blending eurodollar or SOFR futures with interest rate swaps in the 2-year region.
- Applying global smoothing splines to a trading desk curve, causing benchmark hedging instruments to display artificial non-zero mark-to-market.
- Generating sawtooth forward rates by using linear zero-rate interpolation.
- Smoothing through central bank meeting dates or turn-of-year periods instead of inserting explicit discrete forward rate jumps.
- Re-inverting large Jacobian matrices numerically on every bump rather than exploiting triangular sparsity and analytical formulas.

## Interview questions

> [!question]- fi-curve-bootstrap-vs-global | Compare sequential bootstrapping to global optimization in yield curve construction. When is each preferred?
> Bootstrapping reprices all benchmark instruments with zero error in $O(n)$ triangular time, making it mandatory for linear derivatives desks.
> Global optimization smooths through noisy or over-determined quotes using penalized splines, making it ideal for central banks and macro risk analysis.

> [!question]- fi-loglinear-discount-flaw | What is the major mathematical defect of log-linear discount factor interpolation?
> The implied instantaneous forward rate $f(0, t) = -\partial_t \ln P$ is piecewise constant and jumps discontinuously at every pillar date.
> This creates artificial jumps in sensitivities and distorts pricing for instruments whose payoffs depend on continuous forward rates.

> [!question]- fi-cubic-spline-oscillation | Why do natural cubic splines create arbitrage hazards when used on yield curves?
> Cubic splines exhibit non-local behavior: changing a quote at one pillar causes ripples across the entire curve.
> In steep curve environments, this overshoot frequently drives instantaneous forward rates below zero between liquid pillars.

> [!question]- fi-hagan-west-principles | What three mathematical conditions does the Hagan-West monotone convex method enforce on forward rates?
> $1$. Integral constraint matching discrete forward rates between pillars.
> $2$. Continuity of the forward rate across all pillar boundaries.
> $3$. Monotonicity preservation and strict positivity of instantaneous forward rates.

> [!question]- fi-turn-of-year-jump | How should a curve engine model the turn-of-year overnight rate spike without distorting the surrounding forward curve?
> Model the turn-of-year spike as an explicit discrete jump $\Delta_{\text{jump}}$ on December 31.
> The smooth curve interpolates across the remaining period, preventing the year-end anomaly from smearing across adjacent months.

> [!question]- fi-calibration-jacobian-def | Define the calibration Jacobian $J_{\mathbf{s}, \mathbf{z}}$ and explain why it is lower triangular for bootstrapped curves.
> $J_{\mathbf{s}, \mathbf{z}} = \left[ \frac{\partial s_i}{\partial z_j} \right]$ represents the sensitivity of market par quotes to zero rates.
> It is lower triangular because par swap rate $s_i$ depends only on cash flows and zero rates up to its own maturity $T_i$, so $\frac{\partial s_i}{\partial z_j} = 0$ for $j > i$.

> [!question]- fi-jacobian-risk-transformation | Given zero sensitivities $\frac{\partial PV}{\partial \mathbf{z}}$, how do you compute sensitivities to market benchmark quotes $\frac{\partial PV}{\partial \mathbf{s}}$?
> Multiply by the inverse Jacobian: $\frac{\partial PV}{\partial \mathbf{s}} = \left( J_{\mathbf{s}, \mathbf{z}}^{-1} \right)^T \frac{\partial PV}{\partial \mathbf{z}}$.
> This translates abstract zero-rate curve bumps into actionable hedges in liquid market benchmark instruments.

> [!question]- fi-par-bond-jacobian-zero | Why does a 3-year par bond have zero sensitivity to the 1-year and 2-year market par swap quotes after Jacobian transformation?
> A 3-year par bond is identical to a 3-year par swap plus par return.
> In par quote space, each benchmark instrument represents an independent basis vector, isolating risk entirely to the 3-year quote.

> [!question]- fi-futures-convexity-adjustment | Why must futures rates be adjusted downward before being included in a swap yield curve?
> Futures settle daily in cash (daily variation margin), creating a positive correlation between rate increases and reinvestment gains.
> This daily settlement makes futures rates higher than forward rates, requiring a convexity adjustment: $F_{\text{fwd}} \approx F_{\text{fut}} - \frac{1}{2} \sigma^2 T_1 T_2$.

> [!question]- fi-curve-extrapolation-hazard | What is the danger of extrapolating zero rates flat beyond the last liquid pillar?
> With $z$ flat beyond the last pillar, $z'(t) = 0$, so $f(t) = z_{\text{last}} + t z'(t) = z_{\text{last}}$: the instantaneous forward jumps discontinuously at the last pillar to the flat zero level (down when the curve slopes up, e.g. from $4.9474\%$ to $3.9482\%$ on the Note 03 curve), which alters long-term duration and misprices ultra-long liabilities.
> Best practice extrapolates the instantaneous forward rate flat.

## Further reading

- Hagan and West, "Interpolation Methods for Curve Construction", *Applied Mathematical Finance*, 2006.
- Andersen and Piterbarg, *Interest Rate Modeling: Volume 1*, chapters 5 and 6.
- Le Floc'h, "More on the Hagan-West Monotone Convex Interpolator", 2014.
- Ballabio, *Implementing QuantLib*, chapter on term structures.

## In this repo and SDE-Interview-Prep

- Code: [`code/fi_curve_numerics.py`](code/fi_curve_numerics.py) (numerical verification of forward jumps and Jacobian), [`code/curve_bootstrap.py`](code/curve_bootstrap.py) (`DiscountCurve`, `swap_jacobian`, `map_zero_risk_to_par_risk`).
- Related notes: [Swaps and Curve Building](03-Swaps-and-Curve-Building.md), [Curve Risk and Hedging](15-Curve-Risk-and-Hedging.md), [Multi-Curve and CSA Discounting](13-Multi-Curve-and-CSA-Discounting.md).
