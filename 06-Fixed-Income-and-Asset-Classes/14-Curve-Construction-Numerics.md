---
type: concept
track: [quant-research, quant-dev, quant-risk]
tier: advanced
status: solid
prereqs: [multi-curve-and-csa-discounting]
est_hours: 5
sources: [Patrick Hagan and Graeme West - Interpolation Methods for Curve Construction (Applied Mathematical Finance 13(2) 2006 pp 89-129), Leif Andersen and Vladimir Piterbarg - Interest Rate Modeling Volume I (Atlantic Financial Press 2010) - chapter on yield curve construction and risk management, Ferdinando Ametrano and Marco Bianchetti - Everything You Always Wanted to Know About Multiple Interest Rate Curve Bootstrapping but Were Afraid to Ask (SSRN 2013), Luigi Ballabio - Implementing QuantLib (Leanpub) - term structure chapters]
---

# Curve Construction Numerics

## TL;DR

- A curve build turns quotes into a function $P(0,t)$; the interpolation rule decides what the forward curve looks like between pillars, and the forward curve is what traders and models see.
- Log-linear discount factors give piecewise-constant forwards that jump at every pillar (98.55 bp at 1y on the note's curve); linear zero rates give a saw-tooth; natural cubic splines are smooth but non-local, so one quote moves forwards everywhere.
- Hagan and West's monotone convex method interpolates forwards from the discrete forwards so that pillars reprice exactly, forwards are continuous at the pillars, positive when inputs are positive, and a quote change only moves its own and the neighbouring intervals.
- The calibration Jacobian $J = \partial s/\partial z$ maps zero-rate risk to par-quote risk: $\partial PV/\partial s = J^{-T}\partial PV/\partial z$; a 3y par bond has par risk only in the 3y quote, $-100 A_3 = -279.2525$ per unit rate.
- Turns and policy dates go in as explicit jumps: a 2-day 100 bp year-end premium is 28.57 bp on the year-end week, but only 2.19 bp if smeared across the quarter.

## Learning objectives

- Select appropriate market instruments across cash, futures, and swap horizons to build a coherent curve.
- Compare sequential bootstrapping against global optimization and explain their trade-offs in execution speed and stability.
- Derive the implied forward rate shapes for linear zero interpolation, log-linear discount interpolation, and cubic splines.
- Explain the mathematical principles of Hagan and West's monotone convex interpolation.
- Model turn-of-year and central bank meeting jumps without corrupting intermediate forward rates.
- Compute the calibration Jacobian analytically and invert it to map zero rate shocks to market quote shocks.

## Core concepts

### 1. Instruments and the build

Short end: overnight index and short OIS (or deposits); middle: futures (3-month SOFR futures, after a convexity adjustment, see [Convexity Adjustments](17-Convexity-Adjustments.md)) or FRAs; long end: OIS and IRS par quotes at standard tenors.
Overlaps (futures against swaps around 2 to 3 years) are resolved by choosing one instrument per region, and the forward curve across the junction is the first thing to inspect.

### 2. Bootstrapping versus global solving

A bootstrap adds one pillar per instrument in maturity order; when each instrument depends only on pillars up to its own maturity the system is triangular:
$$P(0,T_k) = g_k\big(s_k; P(0,T_1), \dots, P(0,T_{k-1})\big).$$
With annual swaps on annual pillars $g_k$ is closed form; in general each step is a one-dimensional root solve, and interpolation schemes that couple pillars (splines) make even that iterative.
A global build solves all quotes at once, $\mathbf{s}^{mkt} = \mathbf{s}(\boldsymbol\theta)$, by Newton's method $\boldsymbol\theta \leftarrow \boldsymbol\theta - J^{-1}(\mathbf{s}(\boldsymbol\theta) - \mathbf{s}^{mkt})$; it handles non-local interpolation and curves that depend on each other, and the same Jacobian gives the risk.
Fitting methods (Nelson-Siegel-Svensson, smoothing splines) minimise $\sum_i w_i(\pi_i(\boldsymbol\theta) - \pi^{mkt}_i)^2 + \lambda\int f''(t)^2dt$ instead: smooth, robust to noisy quotes, but the inputs do not reprice exactly, so trading desks that hedge with the quoted instruments use exact-fit builds and fitted curves serve relative value and macro analysis.
Whichever method, the acceptance test is that every input reprices.

### 3. What each interpolation does to forwards

With $f(t) = -\partial_t \ln P(0,t)$ and $z(t) = -\ln P(0,t)/t$, so $f = z + t z'$:

| Interpolated | Forward between pillars | Behaviour at pillars | Locality |
| :--- | :--- | :--- | :--- |
| $\ln P$ linear | constant | jumps | local |
| $z$ linear | $z + tz'$, linear | jumps by $T_k \Delta z'$ (saw-tooth) | local |
| $z$ natural cubic spline | smooth | continuous | non-local |
| monotone convex on forwards | quadratic pieces | continuous | local (own and adjacent intervals) |

### 4. Hagan-West monotone convex

Inputs are the discrete forwards $f^d_i = (r_i t_i - r_{i-1}t_{i-1})/(t_i - t_{i-1})$, the average of $f$ over each interval.
Node values are interpolated from the neighbouring averages (Hagan and West 2006, eq. 30): $f_i = \frac{t_i - t_{i-1}}{t_{i+1} - t_{i-1}}f^d_{i+1} + \frac{t_{i+1} - t_i}{t_{i+1} - t_{i-1}}f^d_i$, with end values $f_0 = f^d_1 - \tfrac12(f_1 - f^d_1)$ and $f_n = f^d_n - \tfrac12(f_{n-1} - f^d_n)$.
On each interval the basic interpolant is the quadratic with the right end values and the right average,
$$f(t) = f_{i-1}(1 - 4x + 3x^2) + f_i(-2x + 3x^2) + f^d_i(6x - 6x^2), \qquad x = \frac{t - t_{i-1}}{t_i - t_{i-1}},$$
and where that quadratic would overshoot, a flat segment or a pair of quadratics replaces it (their eqs. 49 to 56) so that the forward is monotone wherever the discrete forwards are.
The integral constraint makes every pillar reprice exactly; a further step bounds the node values to keep forwards positive when all inputs are positive, and an optional amelioration step trades some locality for smoothness (Hagan and West 2006).

### 5. Turns and policy dates

Year-end, quarter-end and central bank meeting dates create genuine steps in overnight forwards.
Model them as explicit jumps added to the smooth curve,
$$-\ln P(0,t) = -\ln P_{smooth}(0,t) + \sum_{k:\,t_k \le t}\Delta_k, \qquad \Delta_k = \text{premium}_k \times \frac{\text{days}_k}{365},$$
so that only periods containing the date see the jump.

### 6. The calibration Jacobian

With par quotes $\mathbf{s}$ and pillar zeros $\mathbf{z}$, $J_{ij} = \partial s_i/\partial z_j$; for annual par swaps on annual pillars, $s_i = (1 - P_i)/A_i$, $A_i = \sum_{k \le i}P_k$, $P_k = e^{-T_k z_k}$ give
$$\frac{\partial s_i}{\partial P_j} = -\frac{s_i}{A_i}\ (j < i), \qquad \frac{\partial s_i}{\partial P_i} = -\frac{1 + s_i}{A_i}, \qquad J_{ij} = \frac{\partial s_i}{\partial P_j}(-T_jP_j),$$
lower triangular because $s_i$ only sees pillars up to $T_i$ (with non-local interpolation it is full).
Then $\partial z/\partial s = J^{-1}$ (forward substitution for a triangular $J$), and par-quote risk is
$$\frac{\partial PV}{\partial \mathbf{s}} = J^{-T}\frac{\partial PV}{\partial \mathbf{z}}.$$
Risk systems either bump each quote and rebuild (simple, $n$ rebuilds) or use the Jacobian (one build plus a linear solve, and exact derivatives with algorithmic differentiation).

### How it is implemented

```mermaid
flowchart LR
    Q[Quotes and conventions] --> I[Instrument objects: cash flows as functions of the curve]
    I --> S{Solver}
    S -- triangular --> B[Bootstrap pillar by pillar]
    S -- coupled --> N[Global Newton on all pillars]
    B --> C[Curve: pillars, interpolator, jump table]
    N --> C
    C --> T{Every quote reprices?}
    T -- no --> S
    T -- yes --> J[Jacobian ds/dz and its inverse]
    J --> R[Par-quote risk and hedges]
```

- Reference implementation: [`code/fi_curve_numerics.py`](code/fi_curve_numerics.py) (forward shapes, monotone convex, locality, Jacobians, turns); [`code/curve_bootstrap.py`](code/curve_bootstrap.py) (`DiscountCurve`, `swap_jacobian`, `map_zero_risk_to_par_risk`).
- System context: [the curve and surface service](../18-Pricing-and-Risk-Systems/04-Curve-and-Surface-Service.md).

## Worked examples

Every number below is computed, printed and asserted by [fi_curve_numerics.py](code/fi_curve_numerics.py); quotes are hypothetical.

### Example 1: forwards under log-linear and linear-zero interpolation

Annual par swaps 3.00%, 3.50%, 4.00% bootstrap to $P(1) = 0.970874$, $P(2) = 0.933352$, $P(3) = 0.888299$ ([Swaps and Curve Building](03-Swaps-and-Curve-Building.md), Example 5).
Log-linear: the forward is $-\ln(P_k/P_{k-1})$ on each interval: 2.9559%, 3.9414%, 4.9474%, jumping 98.55 bp at 1y and 100.60 bp at 2y.
Linear zeros ($z = 2.9559\%, 3.4486\%, 3.9482\%$): just after 1y $f = z_1 + 1 \times (z_2 - z_1) = 3.4486\%$; at 2y the forward jumps from 4.4342% to 4.4478% because the slope changes.

### Example 2: monotone convex on the same curve

Node values $f(0) = 2.7095\%$, $f(1) = 3.4486\%$ and $f(2) = 4.4444\%$ (each the average of the two neighbouring discrete forwards, since the pillars are evenly spaced), $f(3) = 5.1989\%$; the forward is continuous at 1y and 2y, its minimum on $[0, 3]$ is 2.7095% at $t = 0$, and Simpson quadrature of $f$ reproduces all three discount factors to $10^{-12}$.
"Same discount factors, same prices of the inputs, a different forward curve: interpolation is a modelling choice, not a numerical detail."

### Example 3: locality

Continuous zeros 3.00, 3.40, 3.70, 4.00, 4.15, 4.30% at 1, 2, 3, 5, 7, 10 years; bump the 7y zero by 1 bp.

| Change in forward (bp) | at 1.5y | at 2.5y | at 6y |
| :--- | ---: | ---: | ---: |
| monotone convex | 0.0000 | 0.0000 | 4.5217 |
| natural cubic spline on zeros | -0.0063 | 0.0357 | 4.1067 |

An independent implementation (SciPy's natural `CubicSpline`) gives the same three spline numbers, and the bumped monotone convex curve still reprices every pillar.
"A 7y quote should not move the 1.5y forward; with a spline it does, so bucketed risk leaks into tenors the trade does not touch."

### Example 4: the Jacobian and its inverse

Annuities $A_1 = 0.970874$, $A_2 = 1.904226$, $A_3 = 2.792525$.
$\partial s_1/\partial P_1 = -1.03/0.970874 = -1.060900$, so $J_{11} = 1.060900 \times 0.970874 = 1.030000$; likewise $\partial s_2/\partial P_1 = -0.018380$, $\partial s_2/\partial P_2 = -0.543528$, $\partial s_3/\partial P_1 = \partial s_3/\partial P_2 = -0.014324$, $\partial s_3/\partial P_3 = -0.372423$.
$$J = \begin{pmatrix} 1.030000 & 0 & 0 \\ 0.017845 & 1.014606 & 0 \\ 0.013907 & 0.026739 & 0.992468 \end{pmatrix}, \qquad J^{-1} = \begin{pmatrix} 0.970874 & 0 & 0 \\ -0.017076 & 0.985604 & 0 \\ -0.013144 & -0.026554 & 1.007589 \end{pmatrix}.$$
Central finite differences of the par-rate formulas reproduce $J$, and bumping each par quote and re-bootstrapping reproduces $J^{-1}$, both to $10^{-8}$.

### Example 5: zero risk to par risk for a 3y par bond

Cash flows 4, 4, 104: $\partial PV/\partial z_k = -T_k CF_k P_k = -3.8835, -7.4668, -277.1493$.
$\partial PV/\partial s_1 = (-3.8835)(0.970874) + (-7.4668)(-0.017076) + (-277.1493)(-0.013144) = -3.7704 + 0.1275 + 3.6429 = 0.0000$.
$\partial PV/\partial s_2 = -7.3593 + 7.3593 = 0.0000$, and $\partial PV/\partial s_3 = -279.2525 = -100 A_3$.
Bumping each par quote and re-bootstrapping the bond's value gives the same three numbers.
"The zero-risk view says the bond has 1y and 2y exposure; the par view says it is exactly a 3y swap plus cash, which is how you hedge it."

### Example 6: a year-end turn

A 2-day turn with a 100 bp premium: $\Delta = 0.01 \times 2/365 = 0.0000548$.
As an explicit jump, the 1-week forward spanning year end is higher by $\Delta/(7/365) = 28.57$ bp and other weeks are untouched.
Smeared across a quarter, every week of the quarter carries $\Delta/0.25 = 2.19$ bp: the year-end week is underpriced and eleven other weeks overpriced.

## Pitfalls

- Accepting a curve without checking that every input reprices.
- Natural cubic splines on zeros without checking forwards: they are non-local and do not guarantee positive forwards.
- Linear zero interpolation, which gives a saw-tooth forward curve.
- Blending futures and swaps without the futures convexity adjustment.
- Fitted (least-squares) curves on a hedging desk: the hedge instruments show non-zero PV.
- Smoothing through turns and policy dates instead of modelling jumps.
- Recomputing a dense inverse Jacobian for every risk run instead of reusing the factorisation, or bumping zeros and calling it par risk.
- Flat zero extrapolation beyond the last pillar, which makes the forward jump.

## Interview questions

> [!question]- fi-curve-bootstrap-vs-global | Compare sequential bootstrapping to global optimization in yield curve construction. When is each preferred?
> An exact-fit build (bootstrap, or a global Newton solve when interpolation or curve dependencies couple the pillars) reprices every input, which hedging desks need.
> A least-squares fitted curve smooths noisy or redundant quotes but does not reprice them, so it suits relative value, central bank and macro work.

> [!question]- fi-loglinear-discount-flaw | What is the major mathematical defect of log-linear discount factor interpolation?
> The forward is constant between pillars and jumps at each one: 98.55 bp at 1y on the note's curve.
> Anything sensitive to the forward shape (short-dated forwards, caplets, swaption calibration) sees those artificial steps.

> [!question]- fi-cubic-spline-oscillation | Why do natural cubic splines create arbitrage hazards when used on yield curves?
> They are non-local: bumping the 7y zero moves the 2.5y forward by 0.0357 bp in the note's example, and they do not guarantee positive forwards.
> Risk then leaks across buckets and steep curves can produce implausible or negative forwards between pillars.

> [!question]- fi-hagan-west-principles | What three mathematical conditions does the Hagan-West monotone convex method enforce on forward rates?
> $1$. Each interval's forward averages to its discrete forward, so every pillar reprices.
> $2$. The forward is continuous at the pillars (node values interpolated from neighbouring averages).
> $3$. The forward is monotone where the discrete forwards are, and positive when they are positive (with the bounding step).

> [!question]- fi-turn-of-year-jump | How should a curve engine model the turn-of-year overnight rate spike without distorting the surrounding forward curve?
> Add an explicit jump $\Delta = \text{premium} \times \text{days}/365$ in $-\ln P$ at the turn and interpolate the smooth curve separately.
> A 2-day 100 bp turn adds 28.57 bp to the year-end week; smeared over a quarter it would show as 2.19 bp in every week.

> [!question]- fi-calibration-jacobian-def | Define the calibration Jacobian $J_{\mathbf{s}, \mathbf{z}}$ and explain why it is lower triangular for bootstrapped curves.
> $J_{ij} = \partial s_i/\partial z_j$, the sensitivity of each quote to each pillar zero rate.
> With local interpolation each quote depends only on pillars up to its own maturity, so $J_{ij} = 0$ for $j > i$.

> [!question]- fi-jacobian-risk-transformation | Given zero sensitivities $\frac{\partial PV}{\partial \mathbf{z}}$, how do you compute sensitivities to market benchmark quotes $\frac{\partial PV}{\partial \mathbf{s}}$?
> $\partial PV/\partial \mathbf{s} = (J^{-1})^T\partial PV/\partial \mathbf{z}$, because $\partial z_k/\partial s_j = (J^{-1})_{kj}$.
> It is the same as bumping each quote and rebuilding, at the cost of one linear solve.

> [!question]- fi-par-bond-jacobian-zero | Why does a 3-year par bond have zero sensitivity to the 1-year and 2-year market par swap quotes after Jacobian transformation?
> A 4% bond is a receiver 3y swap at 4% plus a floating-rate note, and on a single curve the floater is worth par whatever the curve.
> With the 3y quote held, moving the 1y or 2y quote leaves the bond's value unchanged, so all its risk is in the 3y quote: $-100A_3 = -279.2525$.

> [!question]- fi-futures-convexity-adjustment | Why must futures rates be adjusted downward before being included in a swap yield curve?
> A short futures position gains when rates rise and reinvests those gains at higher rates, so the short is advantaged and futures rates sit above forward rates.
> Ho-Lee gives $F_{fwd} \approx F_{fut} - \tfrac12\sigma^2T_1T_2$ ([Convexity Adjustments](17-Convexity-Adjustments.md)).

> [!question]- fi-curve-extrapolation-hazard | What is the danger of extrapolating zero rates flat beyond the last liquid pillar?
> With $z$ flat, $f = z + tz' = z_{last}$, so the forward jumps at the last pillar: from 4.9474% to 3.9482% on the note's curve.
> Extrapolating the instantaneous forward flat avoids the jump.

> [!question]- fi-monotone-convex-locality | Which intervals change when one quote moves under monotone convex interpolation?
> Its own interval and the adjacent ones, because node values only use neighbouring discrete forwards.
> Bumping the 7y zero leaves the forwards at 1.5y and 2.5y unchanged (0.0000 bp) and moves the 6y forward by 4.5217 bp.

> [!question]- fi-linear-zero-sawtooth | Why does linear interpolation on zero rates produce a saw-tooth forward curve?
> $f = z + tz'$ and $z'$ jumps at each pillar, so $f$ jumps by $T_k$ times the slope change.
> The jump grows with maturity: a small change in slope at 10y moves the forward ten times as much as at 1y.

> [!question]- fi-jacobian-inverse-by-bumping | How can you test an analytic curve Jacobian in production?
> Compare it with central finite differences of the quote-pricing functions, and its inverse with bump-and-rebuild sensitivities of zeros to quotes.
> On the note's curve both agree to $10^{-8}$.

> [!question]- fi-global-newton-multicurve | When is a simultaneous Newton solve necessary rather than a pillar-by-pillar bootstrap?
> When the system is not triangular: non-local interpolation, instruments that depend on later pillars, or curves that depend on each other (a projection curve inside a basis swap used to build the discount curve).
> Newton with the full Jacobian converges quadratically and its Jacobian is reused for risk.

> [!question]- fi-interpolation-choice-pricing | Two curves reprice the same quotes but use different interpolation. Which prices differ?
> Instruments whose cash flows fall between pillars or depend on forward shape: off-pillar swaps, short-dated forwards, FRAs, caplets.
> Instruments on the pillars price identically, which is why interpolation risk hides until a book trades off-pillar dates.

## In this repo and SDE-Interview-Prep

- Code: [`code/fi_curve_numerics.py`](code/fi_curve_numerics.py), [`code/curve_bootstrap.py`](code/curve_bootstrap.py).
- Related notes: [Swaps and Curve Building](03-Swaps-and-Curve-Building.md), [Multi-Curve and CSA Discounting](13-Multi-Curve-and-CSA-Discounting.md), [Curve Risk and Hedging](15-Curve-Risk-and-Hedging.md).

## Further reading

- Patrick Hagan and Graeme West, "Interpolation Methods for Curve Construction", *Applied Mathematical Finance* 13(2), 2006, pp. 89-129.
- Leif Andersen and Vladimir Piterbarg, *Interest Rate Modeling*, Volume I (Atlantic Financial Press 2010), chapter on yield curve construction and risk management.
- Ferdinando Ametrano and Marco Bianchetti, "Everything You Always Wanted to Know About Multiple Interest Rate Curve Bootstrapping but Were Afraid to Ask", SSRN working paper, 2013.
- Luigi Ballabio, *Implementing QuantLib* (Leanpub), term structure chapters.
