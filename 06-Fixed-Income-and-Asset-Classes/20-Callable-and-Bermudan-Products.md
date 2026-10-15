---
type: concept
track: [quant-research]
tier: senior
status: draft
prereqs: [term-structure-models-hjm-lgm-lmm, monte-carlo-pricing-and-variance-reduction]
est_hours: 5
sources: [Francis Longstaff and Eduardo Schwartz - Valuing American Options by Simulation 2001, Leif Andersen and Vladimir Piterbarg - Interest Rate Modeling volume 3]
---

# Callable and Bermudan Products

## TL;DR

Callable bonds and Bermudan swaptions embed multiple early exercise rights, enabling the holder to enter into or terminate a fixed income position at discrete dates across the life of the trade.
Because the issuer can redeem a callable bond when interest rates fall, its price caps at the call strike, creating a pronounced region of negative convexity where duration shortens as rates drop.
Valuing Bermudan exercise requires backward induction to compare immediate exercise value with the expected continuation value.
Low-dimensional models (1-factor Hull-White, LGM) evaluate continuation values using trinomial trees or finite difference PDEs.
Multi-factor models (2-factor LGM, Libor Market Model) require the Longstaff-Schwartz Least-Squares Monte Carlo (LSMC) algorithm, which estimates conditional expectations via cross-sectional polynomial regressions.

## Learning objectives

- Decompose callable bonds into straight bonds and embedded options and quantify their negative convexity profile.
- Define the Option-Adjusted Spread (OAS) and explain why OAS is model-dependent.
- Formulate the backward induction dynamic programming equation for Bermudan swaptions.
- Compare co-terminal swaption structures with fixed-tenor Bermudan swaptions.
- Implement the Longstaff-Schwartz (LSMC) regression algorithm for multi-factor early exercise pricing.
- Design vega hedging strategies for Bermudan swaptions using co-terminal European swaption matrices.

## Core concepts

### 1. Callable Bonds and Negative Convexity

A callable bond grants the issuer the legal option to redeem the bond prior to maturity at specified call dates, typically at par ($100$) or a predetermined call schedule.
The value of a callable bond decomposes into:
$$\text{Price}(\text{Callable Bond}) = \text{Price}(\text{Straight Bond}) - \text{Price}(\text{Call Option})$$
The bondholder is long a straight bond and short an embedded call option to the issuer.

#### The Price-Yield Relationship and Negative Convexity
1. **High Interest Rates:** When yields are significantly above the coupon rate, the probability of the issuer calling the bond is near zero.
The call option is deep out of the money ($\text{Price}(\text{Call Option}) \approx 0$), and the callable bond trades like a standard straight bond with positive convexity:
$$\frac{\partial^2 P}{\partial y^2} > 0$$
2. **Low Interest Rates:** As yields decline, the call option moves deep into the money.
The bond price cannot exceed the call strike $K_{\text{call}}$ (or does so only by the present value of near-term coupons).
The price curve flattens and curves downward:
$$\frac{\partial^2 P}{\partial y^2} < 0$$
This phenomenon is known as **negative convexity**.

#### Practical Consequences of Negative Convexity
- **Asymmetric Duration Risk:** When rates fall, duration shrinks (the bond behaves like a short-dated instrument maturing at the first call date).
When rates rise, duration lengthens (the bond behaves like an uncallable 30-year bond).
The investor suffers full downside risk when rates rise, but is capped on upside appreciation when rates fall.
- **Hedging Challenges:** Investors hedging callable bonds (such as mortgage-backed security desks) must dynamically sell Treasuries as rates rally and buy Treasuries as rates sell off, generating negative gamma decay (whipsaw losses).

### 2. Option-Adjusted Spread (OAS)

A standard yield spread (Z-spread) over the benchmark curve prices the bond as if its cash flows were fixed and deterministic.
For a callable bond, using the Z-spread confuses credit/liquidity risk with the embedded call option premium.

The **Option-Adjusted Spread (OAS)** is the constant parallel spread added to the discount curve (or the short-rate paths of an interest rate tree) such that the model-generated expected present value equals the observed market price:
$$\text{Market Price} = \mathbb{E}_{\mathbb{Q}}\left[ \sum_{i=1}^\tau C_i \exp\left(-\int_0^{t_i} (r(u) + \text{OAS}) du\right) \right]$$
where $\tau$ is the optimal exercise stopping time determined by backward induction.

#### Properties of OAS
- **Pure Compensation:** OAS strips out the value of the embedded option, isolating compensation for credit risk, liquidity risk, and funding costs.
- **Model Dependence:** OAS is not a market-observable quote; it depends directly on the interest rate model and the volatility surface used in the tree or Monte Carlo engine.
Two desks using different volatility assumptions will report different OAS values for the same bond price.

### 3. Bermudan Swaptions

A European swaption can be exercised only on a single expiry date.
An American swaption can be exercised continuously at any time up to maturity.
A **Bermudan swaption** can be exercised on a discrete schedule of dates:
$$\mathcal{T}_{\text{exercise}} = \{T_1, T_2, \dots, T_K\}$$

#### Co-Terminal vs Fixed-Tenor Swaptions
- **Co-Terminal Bermudan:** Every exercise date $T_m$ delivers a swap that matures on the same fixed final maturity date $T_N$.
As time progresses, the remaining tenor of the underlying swap shrinks ($T_N - T_m$).
This is the standard market convention in the interbank swaption market, mirroring callable debt structures.
- **Fixed-Tenor Bermudan:** Exercise at any date $T_m$ delivers a swap of a fixed maturity length $M$ (e.g. always delivering a 5-year swap maturing at $T_m + 5\text{y}$).

#### Dynamic Programming Formulation
Let $V(t, x)$ be the value of the Bermudan swaption given state vector $x$.
At each exercise date $T_m$, the holder compares the immediate intrinsic value of entering the swap with the continuation value of holding the option:
$$V(T_m, x) = \max\left( \text{SwapNPV}(T_m, x), V_{\text{cont}}(T_m, x) \right)$$
where the continuation value is the risk-neutral expected value of tomorrow's option price discounted to today:
$$V_{\text{cont}}(T_m, x) = \mathbb{E}\left[ \exp\left(-\int_{T_m}^{T_{m+1}} r(u) du\right) V(T_{m+1}, x(T_{m+1})) \;\Bigg|\; \mathcal{F}_{T_m} \right]$$
At the final exercise date $T_K$:
$$V(T_K, x) = \max\left( 0, \text{SwapNPV}(T_K, x) \right)$$

### 4. Valuation Techniques

#### 1. Trinomial Trees (Hull-White 1-Factor)
For 1-factor Gaussian models, a recombining trinomial tree provides an exact, stable discretization.
1. Build the tree forward to calibrate state prices to the initial discount curve $P(0, T)$.
2. Roll backward from terminal maturity $T_N$:
   At each node $(m, j)$, compute continuation value $C_{m, j} = \sum_{k \in \{-1, 0, 1\}} p_k e^{-r_j \Delta t} V_{m+1, j+k}$.
   If $T_m$ is an exercise date, set $V_{m, j} = \max(C_{m, j}, \text{SwapNPV}_{m, j})$.
Because the tree recombines in 1D ($O(N^2)$ complexity), pricing takes under 50 milliseconds.

#### 2. Finite Difference PDEs (LGM 1F / 2F)
The Linear Gauss-Markov model expresses bond prices in terms of zero-drift Gaussian states $x(t)$.
The pricing PDE is a standard backward parabolic equation:
$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma(t)^2 \frac{\partial^2 V}{\partial x^2} - r(t, x) V = 0$$
Using Crank-Nicolson finite differences with early-exercise projected SOR (Successive Over-Relaxation) yields fast, accurate Greeks.
However, PDE methods become computationally intractable when the number of state factors $d \ge 3$ due to the curse of dimensionality ($O(M^d)$ grid nodes).

#### 3. Longstaff-Schwartz Least-Squares Monte Carlo (LSMC)
When multi-factor term structure models (such as 2-factor Hull-White or the Libor Market Model) are required to capture curve decorrelation, Monte Carlo is the only feasible simulation technique.
Standard Monte Carlo cannot easily price American/Bermudan options because it runs forward, whereas optimal stopping requires backward dynamic programming.

Francis Longstaff and Eduardo Schwartz (2001) solved this dilemma using cross-sectional regression:
1. Simulate $M$ independent paths forward from $t=0$ to $T_K$, storing all state variables $x_k(t_m)$ and discount factors.
2. At the final date $T_K$, evaluate terminal payoffs: $V(T_K, \omega_k) = \max(0, \text{SwapNPV}(T_K, \omega_k))$.
3. Step backward from $m = K-1$ down to 1:
   - Identify in-the-money paths where $\text{SwapNPV}(T_m, \omega_k) > 0$.
   - Approximate the unobservable continuation value by regressing the discounted realized future cash flows $Y_k = D(T_m, T_{m+1}) V(T_{m+1}, \omega_k)$ onto a set of basis functions of today's state variables $\psi(x_m)$:
     $$V_{\text{cont}}(T_m, x) \approx \sum_{r=1}^R \beta_r \psi_r(x)$$
   - Determine early exercise:
     If $\text{SwapNPV}(T_m, \omega_k) > \hat{V}_{\text{cont}}(T_m, \omega_k)$, exercise is optimal:
     Set path cash flow to $\text{SwapNPV}(T_m, \omega_k)$ and zero out future cash flows on that path.
4. Discount all realized optimal cash flows to $t=0$ and average across paths.

### 5. Hedging Bermudan Swaptions

Bermudan swaptions carry complex, state-dependent risks:
1. **Delta Bucketing:** Because the exercise date is uncertain, delta changes dynamically.
If rates drop, delta shifts toward the first call date; if rates rise, delta extends to the final maturity.
Traders compute key-rate deltas across every annual pillar.
2. **Vega Matrix Hedging:** A Bermudan swaption cannot be hedged with a single European swaption.
Traders hedge using a portfolio of **co-terminal European swaptions** (e.g. 1y into 9y, 2y into 8y, 3y into 7y for a 10-year co-terminal structure).
Calibrating the model to reprice all co-terminal European swaptions ensures that the model matches the market marginal distribution at every exercise date.
3. **Correlation Risk:** Because early exercise depends on the relative level of forward rates across multiple periods, Bermudans are short correlation: higher curve correlation reduces the dispersion of exercise choices, reducing Bermudan optionality value.

## Worked examples

### Example 1: Hull-White Trinomial Tree Bermudan Swaption Valuation
Price a 5-year co-terminal European vs Bermudan payer swaption on a flat 4.0% discount curve ($P(0, t) = e^{-0.04t}$).
The swap has fixed strike $K = 4.0\%$ and annual coupons.
The Bermudan swaption can be exercised at $T = 1.0, 2.0, 3.0, 4.0\text{ years}$ into a swap expiring at $T = 5.0\text{ years}$.
The Hull-White parameters are $a = 0.03$ and $\sigma = 0.012$.

Using our reference implementation [`rates_models.py`](code/rates_models.py):
1. **European Swaption (exercise at $T = 1.0$ only):**
$$\text{Price}(\text{European}) = 0.008592 \quad (85.92 \text{ bps})$$
2. **Bermudan Swaption (exercise at $T \in \{1, 2, 3, 4\}$):**
$$\text{Price}(\text{Bermudan}) = 0.014364 \quad (143.64 \text{ bps})$$
3. **Early Exercise Premium:**
$$\text{Premium} = \text{Price}(\text{Bermudan}) - \text{Price}(\text{European}) = 0.014364 - 0.008592 = 0.005772 \quad (57.72 \text{ bps})$$
The flexibility to exercise at years 2, 3, or 4 adds 57.72 bps of value (an increase of over 67% above the European option value).

### Example 2: Negative Convexity in a Callable Bond
Consider a 30-year bond with a 6.0% annual coupon, callable at par ($100$) in 5 years.
Compare its price sensitivity when market yields shift from 8% down to 4%:
- **At 8% Yield:** The bond trades at a deep discount ($P \approx 77.4$).
The call option is far out of the money.
Modified duration is approximately $11.5\text{ years}$.
A 100 bp drop in yields increases price by $\approx 11.5\%$.
- **At 4% Yield:** Straight bond price would be $134.6$, but the callable bond is capped near $100$ plus near-term coupon value ($P \approx 108.9$).
Effective duration collapses from $11.5\text{ years}$ to $3.8\text{ years}$ (approaching the 5-year call maturity).
The second derivative $\frac{\partial^2 P}{\partial y^2}$ turns negative: price appreciation slows as yields continue to fall.

### Example 3: Longstaff-Schwartz Regression Step
Consider 4 simulated paths at exercise date $T_1$ with state variable $x \in \{0.02, 0.03, 0.04, 0.05\}$:
- Intrinsic exercise values: $\text{SwapNPV} = \{0.06, 0.03, 0.00, -0.02\}$.
Only paths 1, 2 are in-the-money ($\text{SwapNPV} > 0$).
- Discounted future realized payoffs from $T_2$: $Y = \{0.045, 0.038\}$.
- Fitting linear regression $Y = \beta_0 + \beta_1 x$ on the in-the-money paths:
$$\hat{V}_{\text{cont}}(x) = 0.059 - 0.70 x$$
- For Path 1 ($x = 0.02$): $\hat{V}_{\text{cont}} = 0.059 - 0.014 = 0.045$.
$\text{SwapNPV} = 0.06 > 0.045 \implies$ **Exercise immediately!**
- For Path 2 ($x = 0.03$): $\hat{V}_{\text{cont}} = 0.059 - 0.021 = 0.038$.
$\text{SwapNPV} = 0.03 < 0.038 \implies$ **Continue holding!**
The regression separates optimal immediate exercise from continuation across simulated paths.

## Pitfalls

- **Pricing Bermudans with European Black formulas:** Attempting to price a Bermudan swaption by taking the maximum of European swaption prices across exercise dates severely underestimates value; a Bermudan swaption is always worth more than any individual European swaption because the holder decides whether to exercise based on conditional future state information.
- **Overfitting basis functions in LSMC:** Using high-order polynomials (e.g. 10th-degree polynomials) in the Longstaff-Schwartz regression produces in-sample overfitting; the estimated continuation value fits noise rather than true expectation, leading to sub-optimal exercise decisions and negatively biased prices out of sample.
- **Ignoring correlation in multi-callable structures:** 1-factor trees assume perfect correlation across maturities, which distorts the continuation value when the yield curve twists; a 2-factor model (or Cheyette/LMM) is mandatory when the exercise schedule spans multiple economic regimes.
- **Comparing OAS across different pricing models:** Because OAS absorbs residual model errors, comparing the OAS of a bond calculated from a 1-factor Hull-White model with the OAS of a bond calculated from a 2-factor LGM model is invalid; OAS comparisons are meaningful only within a consistent modeling framework.
- **Neglecting exercise notice periods:** In market contracts, exercise notifications must be delivered 2 to 5 business days prior to the swap effective date; failing to model this notice lag grants the option holder an unearned multi-day lookback option.

## Interview questions

> [!question]- fi-callable-bermudan-definition | What is a Bermudan swaption and how does it differ from American and European swaptions?
> A European swaption has a single exercise date; an American swaption can be exercised continuously at any time up to maturity.
> A Bermudan swaption can be exercised on a discrete set of multiple dates (e.g., annually or semi-annually on coupon reset dates).

> [!question]- fi-callable-bermudan-negative-convexity | Why do callable bonds exhibit negative convexity at low interest rates?
> As interest rates decline, the embedded call option moves deep into the money because the issuer can refinance at lower rates.
> The bond price is capped near the call price, forcing the price-yield curve to flatten and become concave ($\partial^2 P / \partial y^2 < 0$).

> [!question]- fi-callable-bermudan-oas-meaning | What is Option-Adjusted Spread (OAS) and what risk does it isolate?
> OAS is the constant spread added to the model's short rate or discount curve that equates the model-generated expected present value of the callable bond to its observed market price.
> It isolates pure credit, liquidity, and funding spread by explicitly removing the price impact of the embedded early exercise option.

> [!question]- fi-callable-bermudan-lsmc-algorithm | Explain the core mechanism of the Longstaff-Schwartz algorithm.
> Standard Monte Carlo cannot value early exercise because conditional expectations require backward induction.
> Longstaff-Schwartz runs paths forward, then steps backward: at each exercise date, it performs cross-sectional ordinary least squares regression of future realized discounted cash flows onto basis functions of current state variables to approximate the continuation value.

> [!question]- fi-callable-bermudan-continuation-vs-intrinsic | What is the decision rule at each exercise date in dynamic programming for Bermudans?
> Exercise immediately if and only if $\text{Intrinsic Value} > \text{Continuation Value}$.
> Intrinsic value is the immediate payoff from entering the swap; continuation value is the risk-neutral expected value of retaining the option into future periods.

> [!question]- fi-callable-bermudan-coterminal-vs-fixed | Distinguish between a co-terminal and a fixed-tenor Bermudan swaption.
> In a co-terminal Bermudan, all exercise dates deliver into swaps that mature on the same fixed final date (the swap tenor shrinks over time).
> In a fixed-tenor Bermudan, exercising at any date delivers a swap of constant duration (e.g., always 5 years).

> [!question]- fi-callable-bermudan-lsmc-bias | Is the basic Longstaff-Schwartz price estimate a lower bound or an upper bound on the true price?
> It is a lower bound (sub-optimal exercise policy).
> Any estimated exercise rule determined by finite regression is sub-optimal compared to the true unknown optimal stopping boundary; exercising on a sub-optimal policy generates an expected payoff less than or equal to the true supremum.

> [!question]- fi-callable-bermudan-vega-hedging | How is a Bermudan swaption typically vega hedged in practice?
> Using a portfolio of co-terminal European swaptions matching each possible exercise date.
> By calibrating the model to the co-terminal European swaption matrix and bucket-hedging vega across the diagonal, the desk immunizes the position against shifts in forward volatility.

> [!question]- fi-callable-bermudan-correlation-impact | If the correlation between short and long rates increases, does a Bermudan swaption increase or decrease in value?
> It decreases in value.
> Bermudan swaptions benefit from curve dispersion and slope volatility, which create diverse early exercise opportunities; higher correlation reduces curve twists, diminishing the optionality value.

> [!question]- fi-callable-bermudan-notice-period | What is an exercise notice period and how does it affect Bermudan pricing?
> An exercise notice period requires the option holder to notify the counterparty several business days (typically 2 to 5 days) before the swap start date.
> It acts as a lag on decision-making: the holder must commit to exercising based on market rates on the notice date, exposing the trade to market drift during the intervening days.

## Further reading

- Francis Longstaff and Eduardo Schwartz, *Valuing American Options by Simulation: A Simple Least-Squares Approach*, The Review of Financial Studies, 2001.
- Leif Andersen and Vladimir Piterbarg, *Interest Rate Modeling*, Volume 3: "Products and Risk Management", Atlantic Financial Press, 2010.
- Bruce Tuckman and Angel Serrat, *Fixed Income Securities: Tools for Today's Markets*, Chapter 19: "Bermudan Swaptions and Callable Bonds".
- Mark Broadie and Paul Glasserman, *Pricing American-style Securities Using Simulation*, Journal of Economic Dynamics and Control, 1997.

## In this repo and SDE-Interview-Prep

- Code: [`code/rates_models.py`](code/rates_models.py) (Hull-White trinomial tree pricing for Bermudan vs European swaptions).
- Prereqs: [Term Structure Models: HJM, LGM, and LMM](19-Term-Structure-Models-HJM-LGM-LMM.md), [Short-Rate Models](04-Short-Rate-Models.md).
- Next: Inflation-Linked Products (planned note 21 in Wave 4).
