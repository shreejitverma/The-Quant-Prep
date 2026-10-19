---
type: concept
track: [quant-research, quant-risk]
tier: senior
status: solid
prereqs: [short-rate-models, rates-volatility-and-sabr]
est_hours: 6
sources: [David Heath - Robert Jarrow and Andrew Morton - Bond Pricing and the Term Structure of Interest Rates - Econometrica 1992, Damiano Brigo and Fabio Mercurio - Interest Rate Models 2nd edition chapters 5 and 6, Leif Andersen and Vladimir Piterbarg - Interest Rate Modeling volume 2 - 2010, Alan Brace - Dariusz Gatarek and Marek Musiela - The Market Model of Interest Rate Dynamics - Mathematical Finance 1997, Andrei Lyashenko and Fabio Mercurio - Looking Forward to Backward-Looking Rates - SSRN 2019]
---

# Term Structure Models: HJM, LGM, and LMM

## TL;DR

- HJM models the whole forward curve $f(t, T)$; absence of arbitrage fixes the risk-neutral drift as $\alpha(t, T) = \sigma(t, T) \cdot \int_t^T \sigma(t, u) du$, so only volatilities are modelling choices.
- Generic HJM is path-dependent; separable (Ritchken-Sankarasubramanian or Cheyette) volatilities give a finite Markov state, and with deterministic volatility the one-factor case is Hull-White.
- LGM (Hagan) writes the same Gaussian model as a driftless state $x(t)$ with variance $\zeta(t)$ and bond prices in closed form, which makes PDE and quadrature pricing of Bermudans simple.
- The LIBOR (forward) market model makes each simple forward lognormal under its own forward measure, so Black's caplet formula holds exactly; under a common measure every rate picks up a state-dependent drift from its covariance with the numeraire.
- Backward-looking RFR coupons (SOFR, ESTR, SONIA) are fixed only at the end of their accrual period, which the forward market model of Lyashenko and Mercurio (2019) handles by extending each rate's dynamics through its accrual period.

## Learning objectives

- Formulate the Heath-Jarrow-Morton (HJM) framework and derive the no-arbitrage HJM drift condition under the risk-neutral measure.
- Explain why generic HJM models are path-dependent (non-Markovian) and identify the separable volatility condition that yields Markovian representations.
- Implement the Linear Gauss-Markov (LGM) model and evaluate zero-coupon bond prices in terms of its state variable.
- Formulate the LIBOR market model (LMM / BGM) and derive the drift under the terminal and spot measures.
- Apply PCA and parametric correlation structures to reduce factor dimensionality in multi-rate models.
- Contrast forward-looking LIBOR market models with backward-looking compounded RFR models.

## Core concepts

### 1. The HJM framework

Heath, Jarrow and Morton (Econometrica, 1992) take the initial forward curve $T \mapsto f(0, T)$ as given and model its evolution under the risk-neutral measure with a $d$-dimensional Brownian motion:
$$df(t, T) = \alpha(t, T) dt + \sigma(t, T) \cdot dW(t), \qquad P(t, T) = \exp\left(-\int_t^T f(t, u) du\right), \qquad r(t) = f(t, t).$$

**Drift condition.**
Let $X(t) = \ln P(t, T) = -\int_t^T f(t, u) du$.
Differentiating (the lower limit contributes $+f(t, t) dt = r\, dt$):
$$dX = \left(r(t) - \int_t^T \alpha(t, u) du\right) dt - \Sigma(t, T) \cdot dW, \qquad \Sigma(t, T) = \int_t^T \sigma(t, u) du.$$
By Ito, $dP/P = dX + \frac{1}{2}|\Sigma|^2 dt$, so $d(P/B)/(P/B) = \left(-\int_t^T \alpha(t, u) du + \frac{1}{2}|\Sigma(t, T)|^2\right) dt - \Sigma \cdot dW$.
The discounted bond is a martingale for every $T$ only if $\int_t^T \alpha(t, u) du = \frac{1}{2}|\Sigma(t, T)|^2$; differentiating in $T$:
$$\alpha(t, T) = \sigma(t, T) \cdot \int_t^T \sigma(t, u) du.$$
Under the risk-neutral measure the drift is not a free parameter: the volatility function determines the whole model, together with the initial curve, which is matched by construction.

### 2. The Markov problem and separable volatilities

Integrating, $r(t) = f(0, t) + \int_0^t \alpha(s, t) ds + \int_0^t \sigma(s, t) \cdot dW(s)$: for a general $\sigma(s, t)$ the short rate depends on the whole Brownian path, so a lattice or PDE would need an unbounded state.

Ritchken and Sankarasubramanian (Mathematical Finance, 1995) and Cheyette (Journal of Fixed Income, 1992) showed that one-factor volatilities of the form
$$\sigma(t, T) = \sigma_r(t) \exp\left(-\int_t^T \kappa(u) du\right)$$
(separable, $g(t) h(T)$) give a two-variable Markov state; with constant $\kappa = a$ and $x(t) = r(t) - f(0, t)$:
$$dx = (y - a x) dt + \sigma_r dW, \qquad dy = (\sigma_r^2 - 2 a y) dt.$$
If $\sigma_r$ is deterministic, $y$ is deterministic and the model is one-factor Hull-White; the auxiliary $y$ matters when $\sigma_r$ depends on the state (the quasi-Gaussian or Cheyette local-volatility models used to fit the skew).
With $m$ separable terms the Gaussian state has $m$ components.

### 3. The Linear Gauss-Markov (LGM) model

Hagan's LGM model uses a driftless Gaussian state under its own numeraire:
$$dx(t) = \sigma(t) dW(t), \quad x(0) = 0, \qquad \zeta(t) = \int_0^t \sigma(s)^2 ds,$$
$$N(t, x) = \frac{1}{P(0, t)} \exp\left( H(t) x + \frac{1}{2} H(t)^2 \zeta(t) \right), \qquad \frac{P(t, T)}{N(t, x)} = P(0, T) \exp\left( -H(T) x - \frac{1}{2} H(T)^2 \zeta(t) \right).$$
The reduced bond price on the right is a martingale (it is the exponential martingale of a Gaussian), so
$$P(t, T) = \frac{P(0, T)}{P(0, t)} \exp\left( -(H(T) - H(t)) x - \frac{1}{2} (H(T)^2 - H(t)^2) \zeta(t) \right).$$
$H$ encodes mean reversion; constant reversion $a$ gives $H(T) = (1 - e^{-aT})/a$, and $\sigma(s) = \sigma_{HW} e^{as}$ gives $\zeta(t) = \sigma_{HW}^2 (e^{2at} - 1)/(2a)$, which is Hull-White with constant $(a, \sigma_{HW})$.
LGM and one-factor Hull-White are the same model in different coordinates; the LGM coordinates make a Bermudan a sequence of Gaussian convolutions of $V/N$, used in [Callable and Bermudan Products](20-Callable-and-Bermudan-Products.md).
LGM is invariant to two transformations ($H \to H + c$, and scaling $H$ by $k$ with $\zeta$ by $1/k^2$), so calibrations must fix a normalisation.

### 4. The LIBOR market model

Brace, Gatarek and Musiela (Mathematical Finance, 1997), Jamshidian (Finance and Stochastics, 1997) and Miltersen, Sandmann and Sondermann (Journal of Finance, 1997) model the simple forwards $L_k(t) = L(t; T_{k-1}, T_k)$ on a tenor grid with accruals $\tau_k$.
$L_k = \frac{1}{\tau_k}\left(\frac{P(t, T_{k-1})}{P(t, T_k)} - 1\right)$ is a ratio of a traded asset to $P(t, T_k)$, so it is a martingale under the $T_k$-forward measure:
$$\frac{dL_k}{L_k} = \sigma_k(t) dW_k^{T_k}(t).$$
With deterministic $\sigma_k$, $L_k(T_{k-1})$ is lognormal and Black's caplet formula is exact.

**Drift under a common measure.**
Changing numeraire from $P(t, T_k)$ to $P(t, T_{k+1})$ adds $-\frac{\tau_{k+1} L_{k+1}}{1 + \tau_{k+1} L_{k+1}} \sigma_k \sigma_{k+1} \rho_{k,k+1} dt$, because $P(t, T_k)/P(t, T_{k+1}) = 1 + \tau_{k+1} L_{k+1}$ has relative volatility $\frac{\tau_{k+1} L_{k+1}}{1 + \tau_{k+1} L_{k+1}}\sigma_{k+1}$.
Chaining to the terminal measure $\mathbb{Q}^{T_N}$:
$$\frac{dL_k}{L_k} = -\sum_{j=k+1}^N \frac{\tau_j L_j}{1 + \tau_j L_j} \rho_{kj} \sigma_k \sigma_j\, dt + \sigma_k dW_k^{T_N}.$$
Under the spot LIBOR measure (numeraire: roll over the front bond at each reset, $q(t)$ the index of the first rate not yet fixed) the drift is positive and sums over the rates from the first unfixed one up to $k$, so every live rate, the front one included, drifts:
$$\frac{dL_k}{L_k} = \sum_{j=q(t)}^{k} \frac{\tau_j L_j}{1 + \tau_j L_j} \rho_{kj} \sigma_k \sigma_j\, dt + \sigma_k dW_k^{\text{spot}}.$$
The drifts depend on the simulated rates, so the model is simulated by Monte Carlo; a log-Euler step that freezes the drift at the start of the step has a discretization error that grows with the step length, and predictor-corrector schemes (Hunter, Jaeckel and Joshi, Risk 2001) re-evaluate the drift at a predicted end state to reduce it.

### 5. Factor reduction and correlation

Forty quarterly forwards have $\frac{40 \times 39}{2} = 780$ pairwise correlations, more than any history estimates reliably.
Litterman and Scheinkman (Journal of Fixed Income, 1991) found that three factors, which they called level, steepness and curvature, explain most of the variation in US Treasury returns, which justifies low-rank models.
A rank-$d$ correlation is built from unit-length loadings, $\rho_{kj} = \sum_{m=1}^d b_{km} b_{jm}$ with $\sum_m b_{km}^2 = 1$; this is positive semi-definite with a unit diagonal by construction (Rebonato's angle parametrization is one way to choose the $b$).
Parametric full-rank forms such as $\rho_{kj} = \rho_\infty + (1 - \rho_\infty) e^{-\beta |T_k - T_j|}$, or the Schoenmakers-Coffey (2003) family, keep the matrix valid and smooth in a few parameters.
Caplet prices depend only on the $\sigma_k$; swaption prices depend on the covariance $\sigma_k \sigma_j \rho_{kj}$, so the correlation is pinned (if at all) by swaptions, not caps.

### 6. Backward-looking RFR coupons

A compounded RFR coupon $R_k = \frac{1}{\tau_k}\left(\prod_{d} (1 + r_d \Delta_d) - 1\right)$ is known only at the end of its accrual period $T_k$, unlike a LIBOR fixing known at $T_{k-1}$.
Lyashenko and Mercurio (2019) define the forward $R_k(t)$ as the $T_k$-forward expectation of the compounded rate; it is a martingale under $\mathbb{Q}^{T_k}$ like a LIBOR forward, and their forward market model keeps it stochastic inside $[T_{k-1}, T_k]$ with a volatility that decays to zero at $T_k$.
The LMM drift formulas carry over with that extended volatility; HJM and short-rate models need no change, because the compounded rate is a functional of the short-rate path.

## Worked examples

### Example 1: the Ho-Lee drift
With constant volatility $\sigma(t, T) = \sigma$, $\alpha(t, T) = \sigma \int_t^T \sigma du = \sigma^2 (T - t)$, so $df(t, T) = \sigma^2 (T - t) dt + \sigma dW$: the continuous-time Ho-Lee model.
Every forward moves by the same $\sigma dW$ (parallel shifts only), and the drift grows linearly with maturity.
With $\sigma = 1.5\%$ and $T - t = 2$: $\alpha = 0.015^2 \times 2 = 0.000450$, or $4.5$ bp per year.

### Example 2: the Hull-White drift
With $\sigma(t, T) = \sigma e^{-a(T - t)}$:
$$\int_t^T \sigma e^{-a(u - t)} du = \frac{\sigma}{a}\left(1 - e^{-a(T - t)}\right), \qquad \alpha(t, T) = \frac{\sigma^2}{a} e^{-a(T - t)} \left(1 - e^{-a(T - t)}\right).$$
With $\sigma = 1.2\%$, $a = 0.03$, $T - t = 2$: $\alpha = 0.000263$.
Forward volatility decays with maturity: the forward 10 years ahead has $e^{-0.3} = 0.7408$ of the short-end volatility, so mean reversion lowers the vols of long-tenor swaptions relative to short-tenor ones.

Independent check in [`code/fi_term_structure.py`](code/fi_term_structure.py): $\ln(P(t, T)/B(t))$ is Gaussian with mean $\ln P(0, T) - A$ and variance $V$, where $A$ integrates the drift and $V$ integrates the squared volatility; with the closed-form drift, nested Simpson quadrature gives $A = V/2 = 12.7973 \times 10^{-4}$ for $t = 1$, $T = 5$, so $E[P(t, T)/B(t)] = P(0, T)$, while pairing the Ho-Lee drift with this volatility breaks the equality.

### Example 3: LGM bond price
Flat 4% continuously compounded curve, $a = 0.03$, $\sigma_{HW} = 1.2\%$, $t = 1$, $T = 5$:
$H(1) = 0.985149$, $H(5) = 4.643067$, $\zeta(1) = 1.4841 \times 10^{-4}$, $P(0, 5)/P(0, 1) = 0.852144$, and
$$P(1, 5; x = 0) = 0.852144 \times \exp\left(-\tfrac{1}{2}(4.643067^2 - 0.985149^2) \times 1.4841 \times 10^{-4}\right) = 0.850843.$$
The value at $x = 0$ is not the forward price: the forward price is the expectation of $P(1, 5)$ under the 1-year forward measure, not its value at one state.
Integrating $P(1, 5; x)/N(1, x)$ over $x \sim N(0, \zeta(1))$ with 40-point Gauss-Hermite gives $0.818731 = P(0, 5)$, the martingale property in numbers.

### Example 4: two-rate LMM drift
Quarterly forwards $L_1$ (from $0.25$ to $0.5$ years) and $L_2$ (from $0.5$ to $0.75$, $\tau_2 = 0.25$), $L_1 = L_2 = 4\%$, $\sigma_1 = 20\%$, $\sigma_2 = 18\%$, $\rho_{12} = 0.85$, terminal measure $\mathbb{Q}^{T_2}$:
$$\mu_1 = -\frac{0.25 \times 0.04}{1.01} \times 0.20 \times 0.18 \times 0.85 = -0.009901 \times 0.0306 = -0.000303 \text{ per year},$$
an absolute drift of $0.04 \times (-0.000303)$, or $-0.12$ bp per year: negligible here, but it scales with $\tau L$, the vols and the number of later rates.

Monte Carlo test of an LMM drift implementation: under $\mathbb{Q}^{T_2}$, $P(t, T_0)/P(t, T_2) = (1 + \tau L_1)(1 + \tau L_2)$ must keep its initial expectation.
With exaggerated inputs ($\tau = 1$, $L = 10\%$, vols $50\%$, $\rho = 0.9$, horizon 2 years, 200,000 paths, 50 log-Euler steps, seed 1997) the target is $1.21$; with the drift the simulated mean is $-0.4$ standard errors from it, and without the drift it is $13.0$ standard errors too high.
The same test under the spot measure, before the first reset, uses the numeraire $P(t, T_0)$, so $P(t, T_1)/P(t, T_0) = 1/(1 + \tau L_1)$ must keep its initial expectation $0.9091$.
With the front-rate drift $\frac{\tau L_1}{1 + \tau L_1}\sigma_1^2$ the simulated mean is $0.9$ standard errors from it, and with $L_1$ driftless it is $33.1$ standard errors too high, so even the front rate drifts under the spot measure.

## Pitfalls

- **Large Euler steps in LMM:** freezing a state-dependent drift over a long step (for example one step to each exercise date) biases prices; use small steps or predictor-corrector, and test with the martingale check of Example 4.
- **Non-separable HJM volatilities:** a general $\sigma(t, T)$ forces the simulation to carry the whole curve and rules out low-dimensional lattices and PDEs.
- **Expecting caps to pin correlation:** caplets depend on each $\sigma_k$ alone; correlation enters only through swaptions and other multi-rate products, and a correlation matrix fitted entry by entry to swaptions can fail to be positive semi-definite.
- **Lognormal LMM with low or negative rates:** $dL/L$ cannot produce negative forwards; use a displaced-diffusion or normal LMM.
- **Measure choice without thought:** under the terminal measure every short-dated rate carries a drift summed over all later rates; the spot measure sums only over rates from the first unfixed one up to $k$; both are arbitrage-free, but their discretization errors and Monte Carlo variances differ, so test the one you use.
- **LGM normalisation:** $H$ and $\zeta$ are identified only up to the two LGM invariances; fix them before comparing calibrated parameters across systems.

## Interview questions

> [!question]- fi-tsm-hjm-drift-condition | State the Heath-Jarrow-Morton (HJM) drift condition and explain its economic significance.
> $\alpha(t, T) = \sigma(t, T) \cdot \int_t^T \sigma(t, u) du$ under the risk-neutral measure.
> It comes from requiring $P(t, T)/B(t)$ to be a martingale for every $T$: the drift integral $\int_t^T \alpha$ must equal half the squared bond volatility $\frac{1}{2}|\int_t^T \sigma|^2$, so once volatilities and the initial curve are chosen the model is fully specified.

> [!question]- fi-tsm-hjm-non-markovian | Why is a generic HJM model non-Markovian?
> $r(t) = f(0, t) + \int_0^t \alpha(s, t) ds + \int_0^t \sigma(s, t) \cdot dW(s)$ weights past shocks by $\sigma(s, t)$, which in general cannot be updated from a finite set of current variables.
> Unless the volatility is separable, the state is the whole curve, which rules out low-dimensional PDEs and recombining trees.

> [!question]- fi-tsm-cheyette-separable | What condition on volatility makes an HJM model Markovian?
> Separability: in one factor $\sigma(t, T) = \sigma_r(t) e^{-\int_t^T \kappa(u) du}$ (equivalently $g(t) h(T)$), which gives the two-variable Ritchken-Sankarasubramanian or Cheyette state $(x, y)$ with $dx = (y - a x)dt + \sigma_r dW$ and $dy = (\sigma_r^2 - 2 a y)dt$.
> With deterministic $\sigma_r$, $y$ is deterministic and the model is Hull-White; $y$ is a genuine second state when $\sigma_r$ depends on the rate.

> [!question]- fi-tsm-lmm-bgm-definition | What is the Libor Market Model (LMM / BGM) and what was its main advantage over HJM?
> It models the market's discrete simple forwards $L(t; T_{k-1}, T_k)$ instead of unobservable instantaneous forwards.
> Each $L_k$ is a martingale under its own $T_k$-forward measure, so with deterministic volatility it is lognormal and Black's caplet formula holds exactly, which makes calibration to caps immediate.

> [!question]- fi-tsm-lmm-terminal-drift | Write the drift of forward rate $L_k(t)$ under the terminal measure $\mathbb{Q}^{T_N}$ in LMM.
> $\mu_k = -\sum_{j=k+1}^N \frac{\tau_j L_j}{1 + \tau_j L_j} \rho_{kj} \sigma_k \sigma_j$.
> Each term is the covariance of $L_k$ with $P(t, T_{j-1})/P(t, T_j) = 1 + \tau_j L_j$, the factors that link $L_k$'s own numeraire $P(t, T_k)$ to $P(t, T_N)$.

> [!question]- fi-tsm-pca-three-factors | What are the three primary factors discovered by PCA on interest rate curves?
> Level (all yields move together), slope or steepness (short and long ends move in opposite directions), and curvature (the belly moves against both ends).
> Litterman and Scheinkman (1991) found that these three explain most of the variation in US Treasury returns, with level by far the largest.

> [!question]- fi-tsm-lgm-vs-hw | How does the Linear Gauss-Markov (LGM) model differ from the 1-factor Hull-White model?
> It is the same Gaussian model: $H(T) = (1 - e^{-aT})/a$ and $\zeta(t) = \sigma_{HW}^2 (e^{2at} - 1)/(2a)$ reproduce Hull-White.
> LGM uses a driftless state $x$ with variance $\zeta(t)$ under the numeraire $N(t, x)$, so bond prices are closed-form in $x$ and pricing a Bermudan reduces to Gaussian convolutions of $V/N$, which is why it is convenient for PDE and quadrature engines.

> [!question]- fi-tsm-predictor-corrector | Why is a predictor-corrector scheme necessary when simulating LMM?
> The drift depends on the forwards themselves, so a log-Euler step that freezes it at the start of the step makes an error that grows with the step size.
> Predictor-corrector evaluates the drift again at a predicted end-of-step state and averages, which allows long steps (for example straight to each exercise date) with a much smaller bias.

> [!question]- fi-tsm-rank-reduction-why | Why do quants reduce the rank of the correlation matrix in LMM?
> A full 40 by 40 matrix has 780 correlations that history cannot estimate reliably, and edits to it can break positive semi-definiteness.
> A rank-2 or rank-3 structure with unit-length loadings is positive semi-definite by construction, captures level, slope and curvature, and cuts the number of Brownian motions per step.

> [!question]- fi-tsm-sofr-vs-libor-modeling | How has term structure modeling changed in the post-LIBOR SOFR era?
> A LIBOR fixing was known at the start of its period; a compounded SOFR coupon is known only at the end, so the forward rate keeps moving through its accrual period.
> The forward market model of Lyashenko and Mercurio (2019) extends each LMM forward through its accrual period with a volatility decaying to zero at the period end; short-rate and HJM models need no change because the compounded rate is a function of the short-rate path.

> [!question]- fi-tsm-hjm-ho-lee-numeric | In a one-factor HJM model with constant volatility 1.5%, what is the risk-neutral drift of the forward 2 years ahead?
> $\sigma^2 (T - t) = 0.015^2 \times 2 = 0.00045$, or $4.5$ bp per year.
> This is Ho-Lee: constant volatility, parallel moves, drift linear in maturity.

> [!question]- fi-tsm-spot-vs-terminal-measure | How does the LMM drift of $L_k$ differ between the spot and the terminal measures?
> Under the terminal measure it is $-\sum_{j > k} \frac{\tau_j L_j}{1 + \tau_j L_j}\rho_{kj}\sigma_k\sigma_j$, negative and summed over later rates; under the spot LIBOR measure it is $+\sum_{j=q(t)}^{k} \frac{\tau_j L_j}{1 + \tau_j L_j}\rho_{kj}\sigma_k\sigma_j$, positive and summed over the live rates up to and including $k$.
> A rate $L_k$ is driftless only under its own forward measure $\mathbb{Q}^{T_k}$: under the terminal measure only the last rate is driftless, and under the spot measure every live rate, the front one included, has a positive drift.

> [!question]- fi-tsm-lmm-drift-test | How would you unit-test the drift of an LMM Monte Carlo engine?
> Check martingales: under $\mathbb{Q}^{T_N}$ every $P(t, T_i)/P(t, T_N) = \prod_{j > i}(1 + \tau_j L_j)$ must keep its initial expectation, within a few standard errors.
> With exaggerated inputs (rates 10%, vols 50%, 2 years) the correct drift passes at $-0.4$ standard errors while omitting it fails at $13.0$, so the test has power.

> [!question]- fi-tsm-hw-forward-vol-decay | In Hull-White with mean reversion 0.03, how volatile is the forward 10 years out relative to the short rate, and why does it matter?
> $e^{-0.03 \times 10} = 0.7408$ of the short-rate volatility, since $\sigma(t, T) = \sigma e^{-a(T - t)}$.
> Mean reversion sets how long-dated forwards move relative to short ones, so it controls the ratio of long-tenor to short-tenor swaption vols and the value of switching between exercise dates in a Bermudan.

> [!question]- fi-tsm-lgm-martingale-check | In LGM, what identity would you check numerically to validate a bond pricing function, and what does it look like for $P(1, 5)$?
> $E[P(t, T; x)/N(t, x)] = P(0, T)$ with $x(t) \sim N(0, \zeta(t))$.
> On a flat 4% curve with $a = 0.03$ and $\sigma_{HW} = 1.2\%$, Gauss-Hermite integration gives $0.818731 = e^{-0.2}$, while the price at $x = 0$ alone is $0.850843$ against a forward price of $0.852144$.

## Further reading

- David Heath, Robert Jarrow, and Andrew Morton, *Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation*, Econometrica, 1992.
- Peter Ritchken and L. Sankarasubramanian, *Volatility Structures of Forward Rates and the Valuation of Interest Rate Contingent Claims*, Mathematical Finance, 1995.
- Alan Brace, Dariusz Gatarek, and Marek Musiela, *The Market Model of Interest Rate Dynamics*, Mathematical Finance, 1997.
- Damiano Brigo and Fabio Mercurio, *Interest Rate Models - Theory and Practice*, 2nd edition, Springer, 2006, chapter 5 (HJM, including the Ritchken-Sankarasubramanian framework) and chapter 6 (LIBOR and swap market models).
- Leif Andersen and Vladimir Piterbarg, *Interest Rate Modeling*, Volume 2: Term Structure Models, Atlantic Financial Press, 2010.
- Patrick Hagan, *Evaluating and Hedging Exotic Swap Instruments via LGM*, unpublished manuscript.
- Andrei Lyashenko and Fabio Mercurio, *Looking Forward to Backward-Looking Rates: A Modeling Framework for Term Rates Replacing LIBOR*, SSRN working paper, 2019.
- Robert Litterman and Jose Scheinkman, *Common Factors Affecting Bond Returns*, Journal of Fixed Income, 1991.

## In this repo and SDE-Interview-Prep

- Code: [`code/fi_term_structure.py`](code/fi_term_structure.py) asserts every number here, including the HJM quadrature check, the LGM Gauss-Hermite check and the LMM martingale test; [`code/rates_models.py`](code/rates_models.py) has Hull-White bond, Jamshidian swaption and trinomial tree pricers.
- Prereq: [Short-Rate Models](04-Short-Rate-Models.md), [Rates Volatility and SABR](18-Rates-Volatility-and-SABR.md).
- Next: [Callable and Bermudan Products](20-Callable-and-Bermudan-Products.md).
