---
type: concept
title: "Volatility Surfaces, Skew, and Term Structure"
track: [quant-trader, quant-research]
tier: advanced
status: solid
est_hours: 1.5
tags: [options, volatility, surface, skew, smile, term-structure, svi, sabr, sticky-strike, sticky-delta]
prereqs: []
---

# Volatility Surfaces, Skew, and Term Structure

In the classical Black-Scholes-Merton model, volatility is assumed to be a constant parameter across all strike prices and expiration dates.
Empirical financial markets severely violate this assumption.
Following the October 1987 stock market crash, options markets price out-of-the-money (OTM) puts at a substantial implied volatility premium relative to at-the-money (ATM) and out-of-the-money calls.
This persistent non-flat relationship across strike prices forms the implied volatility smile or skew, while variation across maturities generates the volatility term structure.
Together, moneyness and maturity span the two-dimensional volatility surface $\sigma_{IV}(K, T)$.

---

## TL;DR

The volatility surface models implied volatility as a function of strike $K$ and expiration $T$.
Equity index options exhibit a persistent downward-sloping "smirk" or "skew" driven by downside crash hedging demand and structural leverage.
Commodity and FX options frequently display symmetric "smiles" reflecting fat-tailed jump risks.
The term structure reflects market expectations of forward volatility, trading in contango during quiet bull regimes and backwardation during market panics.
Desks model surface dynamics under two primary delta-hedging conventions: sticky strike (implied volatility remains constant at a fixed strike) and sticky delta / sticky moneyness (implied volatility shifts with the underlying asset price).
Parametric models such as Gatheral's SVI (Stochastic Volatility Inspired) and the Hagan SABR model calibrate the surface while enforcing absence of static arbitrage (butterfly and calendar arbitrage).

---

## Learning objectives

- Analyze the economic and structural drivers of the volatility smirk, skew, and smile across asset classes.
- Formulate the term structure of implied volatility and evaluate forward variance from market quotes.
- Contrast the hedging implications of sticky strike versus sticky delta surface dynamics.
- Derive the conditions for absence of static arbitrage across the strike slice and term structure.
- Calibrate parametric volatility models (SVI, SABR) to observed market quotes and quantify skew risk.

---

## Core concepts

### 1. Anatomy of the Volatility Surface

The implied volatility surface is the mapping:

$$\sigma_{IV}: (K, T) \mapsto \mathbb{R}^+$$

where $\sigma_{IV}(K, T)$ is the Black-Scholes implied volatility inverted from market prices:

$$C_{\text{market}}(K, T) = C_{\text{BSM}}(S, K, T, r, q, \sigma_{IV}(K, T))$$

1. **The Strike Dimension (Skew and Smile)**:
   - **Equity Index Skew (Smirk)**: Out-of-the-money puts ($K < S$) trade at significantly higher implied volatilities than ATM or OTM calls.
   - This asymmetry originated following the October 19, 1987 crash, reflecting institutional demand for portfolio insurance ("crash-phobia") and the leverage effect (falling equity prices increase corporate debt-to-equity ratios, boosting equity volatility).
   - **FX Smiles**: Currency options typically display symmetric smiles centered near ATM, driven by leptokurtic return distributions (fat tails) and two-sided central bank intervention risk.
   - **Commodity Inverted Skews**: Agricultural and energy options (e.g., natural gas, crude oil) frequently exhibit positive skew (OTM calls trade at higher IV than OTM puts) due to physical supply shortages and upside price spikes.

2. **The Time Dimension (Term Structure)**:
   - **Contango**: In normal, calm market environments, short-dated implied volatility is lower than long-dated implied volatility ($\frac{\partial \sigma_{IV}}{\partial T} > 0$).
   - Long-dated options price in long-run macroeconomic uncertainty and mean-reverting baseline volatility.
   - **Backwardation**: During market crises or preceding high-impact macro announcements (CPI, FOMC, elections), short-dated IV spikes violently above long-dated IV ($\frac{\partial \sigma_{IV}}{\partial T} < 0$).
   - This inversion reflects intense demand for immediate tail-risk protection.

### 2. Forward Volatility and Variance Swaps

The relationship between spot implied volatilities of two maturities $T_1$ and $T_2$ ($T_1 < T_2$) defines the forward implied volatility $\sigma(T_1, T_2)$:

$$(T_2 - T_1) \sigma^2(T_1, T_2) = T_2 \sigma^2(T_2) - T_1 \sigma^2(T_1)$$

Solving for forward volatility yields:

$$\sigma(T_1, T_2) = \sqrt{\frac{T_2 \sigma^2(T_2) - T_1 \sigma^2(T_1)}{T_2 - T_1}}$$

For the forward variance to be positive, total implied variance $w(T) = \sigma^2(T) T$ must be strictly non-decreasing in maturity:

$$\frac{\partial w}{\partial T} \ge 0$$

A downward slope in total variance implies calendar arbitrage, where a calendar spread produces negative forward variance.

### 3. Surface Dynamics: Sticky Strike vs Sticky Delta

When the underlying spot price $S$ moves, how does the implied volatility surface respond?
Quantitative desks model this behavior under two competing operational regimes:

1. **Sticky Strike (Sticky Price)**:
   - Implied volatility is assumed to be an invariant function of the absolute strike price $K$:
     $$\sigma_{IV}(K, S) = f(K)$$
   - When the underlying price $S$ rises or falls, the implied volatility at strike $K$ does not change ($\frac{\partial \sigma_{IV}}{\partial S} = 0$).
   - Under sticky strike, the effective delta of an option equals the model Black-Scholes delta:
     $$\Delta_{\text{sticky strike}} = \frac{\partial V_{\text{BSM}}}{\partial S} = \Delta_{\text{BSM}}$$

2. **Sticky Delta (Sticky Moneyness)**:
   - Implied volatility is assumed to be an invariant function of moneyness $m = \frac{K}{S}$ or delta $\Delta$:
     $$\sigma_{IV}(K, S) = g\left(\frac{K}{S}\right)$$
   - When the spot price $S$ moves, the entire smile shifts horizontally with it, so the ATM implied volatility stays constant.
   - A fixed-strike option instead slides along the smile as its moneyness changes; when $S$ drops, its moneyness $K/S$ increases and its implied volatility becomes the smile value at the new moneyness:
     $$\frac{\partial \sigma_{IV}}{\partial S} = -\frac{K}{S^2} g'\left(\frac{K}{S}\right)$$
   - By the chain rule, the effective delta of the option includes a skew adjustment term:
     $$\Delta_{\text{sticky delta}} = \frac{\partial V_{\text{BSM}}}{\partial S} + \frac{\partial V_{\text{BSM}}}{\partial \sigma} \frac{\partial \sigma_{IV}}{\partial S} = \Delta_{\text{BSM}} + \mathcal{V} \frac{\partial \sigma_{IV}}{\partial S}$$
   - Equity index skew is downward-sloping in moneyness ($g' < 0$), so $\frac{\partial \sigma_{IV}}{\partial S} = -\frac{K}{S^2} g' > 0$ at every strike.
   - When spot falls, a fixed-strike put moves toward the money and its implied volatility falls toward the unchanged ATM level.
   - The skew term $\mathcal{V} \frac{\partial \sigma_{IV}}{\partial S}$ is therefore positive: sticky-moneyness put deltas are smaller in magnitude than BSM deltas, and call deltas are larger.
   - The two regimes disagree on the hedge ratio, so the choice must be tested against how the surface actually moved, not assumed.

### 4. Static Arbitrage Bounds

A valid implied volatility surface must be free from static arbitrage opportunities:

1. **Calendar Spread Arbitrage (Time Direction)**:
   - Call prices must be monotonic non-decreasing in maturity for zero interest rates:
     $$\frac{\partial C(K, T)}{\partial T} \ge 0$$
   - In terms of total implied variance $w(K, T) = \sigma_{IV}^2(K, T) T$, absence of calendar arbitrage requires:
     $$\partial_T w(K, T) \ge 0$$

2. **Butterfly Arbitrage (Strike Direction)**:
   - Option prices must be convex functions of strike price:
     $$\frac{\partial^2 C(K, T)}{\partial K^2} \ge 0$$
   - By the Breeden-Litzenberger (1978) theorem, the second derivative of call price with respect to strike yields the risk-neutral probability density function (PDF) $q(K)$:
     $$q(K) = e^{r T} \frac{\partial^2 C}{\partial K^2}$$
   - If the volatility smile is too concave, $\frac{\partial^2 C}{\partial K^2} < 0$, which implies negative risk-neutral probabilities.
   - A trader can construct a butterfly spread (buy $K_1$, sell two $K_2$, buy $K_3$) that yields a guaranteed risk-free profit at zero cost.

### 5. Parametric Volatility Models

To interpolate and extrapolate the volatility surface smoothly while preventing static arbitrage, quantitative desks utilize parametric representations:

1. **Gatheral's SVI (Stochastic Volatility Inspired)**:
   - Parameterizes total implied variance $w(k) = \sigma^2(k) T$ as a function of log-moneyness $k = \ln(K / F)$:
     $$w(k) = a + b \left(\rho (k - m) + \sqrt{(k - m)^2 + \sigma^2}\right)$$
   - Parameters:
     - $a \in \mathbb{R}$: Overall level of variance.
     - $b \ge 0$: Angle between the two asymptotic wings.
     - $\rho \in [-1, 1]$: Orientation and skewness of the smile (negative for equities).
     - $m \in \mathbb{R}$: Horizontal translation of the minimum.
     - $\sigma > 0$: Smoothness of the vertex roundness.
   - SVI guarantees strictly hyperbolic asymptotes, matching Roger Lee's Moment Formula for extreme strike tails.

2. **Hagan's SABR Model**:
   - A stochastic volatility model governed by forward price $F_t$ and stochastic vol $\alpha_t$:
     $$dF_t = \alpha_t F_t^\beta dW_{1,t}$$
     $$d\alpha_t = \nu \alpha_t dW_{2,t}, \quad d\langle W_1, W_2 \rangle_t = \rho dt$$
   - Produces an analytical asymptotic formula for implied volatility $\sigma_{\text{SABR}}(K, F)$ widely used in interest rate swaptions and FX options.

---

## Worked examples

### Example 1: Forward Implied Volatility and Calendar Arbitrage Check

An options quantitative analyst extracts at-the-money implied volatilities for two maturities on the S&P 500 index:
- 30-day maturity ($T_1 = 30 / 365 = 0.08219$ years): $\sigma_1 = 18.0\%$ ($0.18$).
- 90-day maturity ($T_2 = 90 / 365 = 0.24658$ years): $\sigma_2 = 22.0\%$ ($0.22$).

1. **Compute Total Implied Variances**:
   $$w_1 = \sigma_1^2 \times T_1 = (0.18)^2 \times 0.08219 = 0.0324 \times 0.08219 = 0.002663$$
   $$w_2 = \sigma_2^2 \times T_2 = (0.22)^2 \times 0.24658 = 0.0484 \times 0.24658 = 0.011934$$

2. **Verify Calendar Arbitrage Bound**:
   $$\Delta w = w_2 - w_1 = 0.011934 - 0.002663 = +0.009271 > 0$$
   Because total variance increases monotonically with maturity, calendar spread arbitrage is absent.

3. **Calculate Forward Implied Volatility over the 60-Day Forward Window**:
   $$\Delta T = T_2 - T_1 = 0.24658 - 0.08219 = 0.16438\text{ years}$$
   $$\sigma_{\text{fwd}}^2 = \frac{w_2 - w_1}{\Delta T} = \frac{0.009271}{0.16438} = 0.05640$$
   $$\sigma_{\text{fwd}} = \sqrt{0.05640} = 0.2375 = 23.75\%$$
   The market is pricing expected annualized volatility of $23.75\%$ between day 30 and day 90.

### Example 2: Skew-Adjusted Delta Under Sticky Moneyness

A market maker is hedging a 25-delta OTM European put on an index:
- Spot: $S = \$5,000.00$.
- Strike: $K = \$4,750.00$ ($m = K / S = 0.95$).
- Time to Expiration: $T = 0.10$ years ($\sqrt{T} = 0.31623$).
- Implied Volatility at the Strike: $\sigma_{IV} = 25\%$; rates and dividends are set to zero.
- Skew Slope: implied volatility rises by $1.2$ volatility points for every $\$50$ ($1\%$ of spot) lower strike, so $\frac{\partial \sigma_{IV}}{\partial K} = -\frac{0.012}{\$50.00} = -0.00024$ per dollar of strike, which in moneyness terms is $g' = -0.00024 \times 5000 = -1.2$.

1. **Compute the BSM Delta and Vega**:
   $$d_1 = \frac{\ln(5000/4750) + 0.5(0.25)^2(0.10)}{0.25 \times 0.31623} = \frac{0.051293 + 0.003125}{0.079057} = 0.6883$$
   $$\Delta_{\text{BSM}} = N(d_1) - 1 = 0.7544 - 1 = -0.2456$$
   $$\mathcal{V}_{\text{raw}} = S \phi(d_1) \sqrt{T} = 5000 \times 0.31479 \times 0.31623 = 497.73\text{ (\$4.98 per 1\% IV change)}$$

2. **Compute the Sticky-Moneyness Vol Sensitivity**:
   $$\frac{\partial \sigma_{IV}}{\partial S} = -\frac{K}{S^2} g' = -\frac{4750}{5000^2} \times (-1.2) = +0.000228\text{ per dollar of spot move}$$
   As spot falls, this strike moves toward the money and its implied volatility falls toward the ATM level.

3. **Calculate the Skew Adjustment Term**:
   $$\text{Adjustment} = \mathcal{V}_{\text{raw}} \times \frac{\partial \sigma_{IV}}{\partial S} = 497.73 \times 0.000228 = +0.1135$$

4. **Compute Effective Delta**:
   $$\Delta_{\text{sticky delta}} = \Delta_{\text{BSM}} + \text{Adjustment} = -0.2456 + 0.1135 = -0.1321$$
   A central finite difference that reprices the put with the smile moving with spot gives the same $-0.1321$.
   Under sticky moneyness, the short put needs a hedge of only $0.132$ delta per option rather than the BSM $0.246$, so hedging with BSM delta would over-hedge if the surface really moves that way.
   Under sticky strike the BSM delta of $-0.2456$ is the right hedge, which is why the choice of regime matters.

---

## Pitfalls

- **Confusing Sticky Strike with Sticky Delta During Crashes**:
  The two regimes give different deltas, and in a sharp equity selloff fixed-strike implied volatilities often rise, which neither rule captures.
  A short put book hedged with sticky-moneyness deltas is the most exposed, because that rule shrinks put deltas exactly when realized put losses grow.
- **Negative Forward Variance From Uncalibrated Raw Quotes**:
  Interpolating implied volatilities across maturities using unconstrained splines frequently produces negative forward variance.
  Every quantitative surface must enforce $\partial_T w \ge 0$ across all strikes.
- **Butterfly Arbitrage From Steep Skew Fits**:
  Over-fitting the downside put wing in low-liquidity strikes can cause $\frac{\partial^2 C}{\partial K^2} < 0$.
  This implies negative probability densities and causes Monte Carlo and PDE pricer instabilities.
- **Ignoring Event Jumps in the Term Structure**:
  Treating an inverted term structure as a pure mean-reverting forward volatility signal ahead of an earnings announcement or central bank decision is dangerous.
  The short-dated premium reflects a discrete jump rather than elevated continuous diffusion.

---

## Interview questions

> [!question]- mkt-opt-033 | What is the implied volatility surface?
> A two-dimensional mapping sigma_IV(K, T) that assigns an implied volatility to every strike price K and time to maturity T.
> It inverts the Black-Scholes formula against observable market option prices.

> [!question]- mkt-opt-034 | What is the implied volatility smile or smirk?
> The non-flat relationship between implied volatility and strike price for a fixed expiration date.
> Equities display a downward-sloping smirk (skew), while FX markets typically display a symmetric smile.

> [!question]- mkt-opt-035 | Why did the equity index volatility skew emerge after October 1987?
> Before the 1987 crash, options traded at relatively flat implied volatilities across strikes.
> Post-1987, intense institutional demand for downside portfolio insurance (crash-phobia) permanently bid up out-of-the-money put implied volatility.

> [!question]- mkt-opt-036 | What is the leverage hypothesis explaining equity volatility skew?
> When a company's stock price falls, its debt-to-equity ratio increases, making the equity riskier.
> This structural increase in financial leverage naturally drives higher expected equity volatility as stock price declines.

> [!question]- mkt-opt-037 | Define term structure of implied volatility.
> The curve plotting implied volatility against time to maturity T for at-the-money options.
> It reveals the market's forward expectations of annualized volatility over varying time horizons.

> [!question]- mkt-opt-038 | Contrast contango and backwardation in volatility term structures.
> Contango is an upward-sloping term structure (short-term IV < long-term IV) typical of calm bull regimes.
> Backwardation is an inverted downward-sloping term structure (short-term IV > long-term IV) observed during market panics or before major catalyst events.

> [!question]- mkt-opt-039 | State the formula for forward implied volatility between maturities T1 and T2.
> sigma(T1, T2) = sqrt((T2 * sigma(T2)^2 - T1 * sigma(T1)^2) / (T2 - T1)).
> It reflects the implied volatility priced by the market across the forward interval [T1, T2].

> [!question]- mkt-opt-040 | What condition on total implied variance w(T) prevents calendar spread arbitrage?
> Total implied variance w(T) = sigma^2(T) * T must be monotonically non-decreasing in maturity: dw/dT >= 0.
> If total variance decreases with maturity, forward variance becomes negative, creating calendar arbitrage.

> [!question]- mkt-opt-041 | What is the Breeden-Litzenberger theorem?
> The risk-neutral probability density function of the underlying asset at maturity T equals: q(K) = exp(r*T) * (d^2 C / dK^2).
> The second derivative of call price with respect to strike recovers the state-price density.

> [!question]- mkt-opt-042 | What is butterfly arbitrage in the strike dimension?
> An arbitrage opportunity arising when the second derivative d^2 C / dK^2 is negative.
> A trader buys strike K1, sells two K2, and buys K3 for a net credit while facing non-negative terminal payoff.

> [!question]- mkt-opt-043 | Explain the sticky strike hypothesis.
> The assumption that implied volatility at a fixed absolute strike K remains unchanged as spot price moves: d sigma_IV / dS = 0.
> Under sticky strike, the trader's dynamic delta hedge matches the standard Black-Scholes delta.

> [!question]- mkt-opt-044 | Explain the sticky delta (sticky moneyness) hypothesis.
> The assumption that implied volatility is a function of moneyness K/S or delta, moving horizontally with spot price.
> As spot price changes, implied volatility at a fixed strike K shifts by: d sigma_IV / dS = -(K / S^2) * g'(K / S).

> [!question]- mkt-opt-045 | State the skew-adjusted delta formula under sticky delta dynamics.
> Delta_effective = Delta_BSM + Vega * (d sigma_IV / dS).
> Because equity skew is downward-sloping in moneyness, d sigma_IV / dS > 0 at a fixed strike, so the adjustment is positive: put deltas shrink in magnitude and call deltas grow.

> [!question]- mkt-opt-046 | What is risk reversal (RR) in volatility quotes?
> The implied volatility difference between an out-of-the-money call and an out-of-the-money put of equal delta: RR_25d = sigma(25d Call) - sigma(25d Put).
> It directly measures the slope or directional skew of the volatility surface.

> [!question]- mkt-opt-047 | What is a butterfly (BF / Strangle) in volatility quotes?
> The average implied volatility of OTM calls and puts relative to ATM volatility: BF_25d = 0.5 * (sigma(25d Call) + sigma(25d Put)) - sigma(ATM).
> It quantifies the smile curvature and market pricing of tail risk (kurtosis).

> [!question]- mkt-opt-048 | State Gatheral's SVI equation for total implied variance.
> w(k) = a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2)).
> It expresses total variance w as a hyperbolic function of log-moneyness k = ln(K / F).

> [!question]- mkt-opt-049 | In Gatheral's SVI model, what is the role of parameter rho?
> rho controls the skewness and orientation of the smile wings.
> For equity index markets, rho is strongly negative (-0.7 to -0.9), producing a steep downside put wing.

> [!question]- mkt-opt-050 | In Gatheral's SVI model, what does parameter b control?
> b controls the angle and steepness of the asymptotic wings as log-moneyness approaches +/- infinity.
> Higher b increases the smile curvature in extreme tails.

> [!question]- mkt-opt-051 | What is Roger Lee's Moment Formula?
> A theorem establishing that total implied variance grows asymptotically at most linearly in log-moneyness: lim_{|k| -> infinity} w(k) / |k| <= 2.
> It links the slope of extreme volatility wings to the highest finite moment of the underlying asset price.

> [!question]- mkt-opt-052 | What is Dupire's local volatility formula?
> A mathematical equation recovering instantaneous local volatility sigma_loc(S, t) from market option prices: sigma_loc^2(K, T) = (dC/dT + (r - q)K dC/dK + qC) / (0.5 * K^2 * d^2C/dK^2).
> It generates a state-dependent diffusion process that perfectly reprices the entire market surface.

> [!question]- mkt-opt-053 | What is a major limitation of Dupire's local volatility model?
> Local volatility predicts that the implied volatility surface flattens as the underlying moves, contradicting empirical sticky delta behavior.
> It systematically underestimates forward volatility smile dynamics.

> [!question]- mkt-opt-054 | What are the core parameters of Hagan's SABR model?
> Alpha (initial volatility), Beta (CEV exponent linking spot to volatility), Rho (spot-vol correlation), and Nu (volatility of volatility).
> SABR is widely used to calibrate interest rate swaptions and FX options smiles.

> [!question]- mkt-opt-055 | Why do commodity markets often exhibit positive volatility skew?
> Supply constraints cannot be solved instantaneously; physical inventory shortages create explosive upside price spikes.
> OTM calls trade at a premium to OTM puts in energy, metals, and agricultural options.

> [!question]- mkt-opt-056 | What is the variance risk premium (VRP)?
> The persistent structural spread between implied volatility and subsequent realized volatility: VRP = sigma_implied - sigma_realized.
> In equity indices, implied volatility trades on average 2-4 points above realized volatility, compensating options sellers for crash risk.

> [!question]- mkt-opt-057 | What is the ATM 30-day implied volatility index (VIX)?
> A model-free calculation developed by the CBOE that aggregates a continuous strip of OTM SPX calls and puts to estimate 30-day expected variance.
> It computes: sigma_VIX^2 = (2 / T) * sum_i (Delta K_i / K_i^2) * exp(r*T) * Q(K_i) - (1 / T) * (F / K_0 - 1)^2.

> [!question]- mkt-opt-058 | How does earnings announcement uncertainty distort the short-dated volatility surface?
> Implied volatility for the contract expiring immediately after earnings surges to account for the discrete event jump.
> Term structure heavily inverts (backwardation) and ATM strike volatility elevates relative to farther expiries.

> [!question]- mkt-opt-059 | What is the implied move derived from an ATM straddle prior to earnings?
> Implied Move ~ 0.8 * Straddle_Price / Spot_Price.
> It approximates the one-standard-deviation price move expected by options market makers over the announcement.

> [!question]- mkt-opt-060 | What happens to implied volatility immediately following an earnings release?
> Implied volatility collapses violently across strikes, a phenomenon known as volatility crush.
> The event variance drops to zero once the earnings report is public knowledge.

> [!question]- mkt-opt-061 | What is skew risk in market making books?
> The risk that the slope of the volatility smile changes independently of ATM volatility.
> A delta-neutral desk short OTM puts loses heavily if the downside put skew steepens during a market decline.

> [!question]- mkt-opt-062 | How can a trader isolate and trade skew directly?
> By trading a risk reversal: buy OTM calls and sell OTM puts (or vice versa) while delta-hedging the net underlying exposure.
> The position gains if the call-put volatility spread widens regardless of spot direction.

> [!question]- mkt-opt-063 | What is smile curvature risk and how is it traded?
> Trading changes in the convexity of the volatility smile by buying or selling delta-hedged strangles against ATM straddles.
> It isolates exposure to Volga (d Vega / d sigma) and fat-tailed kurtosis moves.

> [!question]- mkt-opt-064 | What is the consequence of calibrating an option model to market quotes with calendar arbitrage?
> Numerical PDE and Monte Carlo engines generate negative probabilities or infinite discounting, causing simulation blowups.
> Surfaces must be smoothed and arbitrage-free before running pricing algorithms.

---

## Further reading

- Breeden, D. T., & Litzenberger, R. H. (1978). *Prices of state-contingent claims implicit in option prices*. Journal of Business, 51(4), 621-651.
- Dupire, B. (1994). *Pricing with a smile*. Risk, 7(1), 18-20.
- Hagan, P. S., Kumar, D., Lesniewski, A. S., & Woodward, D. E. (2002). *Managing smile risk*. Wilmott Magazine, 1, 84-108.
- Gatheral, J. (2004). *A parsimonious fitting of volatility smiles*. Merrill Lynch Presentation, NYU Courant.
- Lee, R. (2004). *The moment formula for implied volatility at extreme strikes*. Mathematical Finance, 14(3), 469-480.
- Gatheral, J. (2006). *The Volatility Surface: A Practitioner's Guide*. John Wiley & Sons.
