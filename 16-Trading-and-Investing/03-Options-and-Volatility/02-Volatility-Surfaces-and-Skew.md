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
Since the October 1987 stock market crash, equity index options have priced out-of-the-money (OTM) puts at an implied volatility premium to at-the-money (ATM) and out-of-the-money calls (Rubinstein 1994 documents the change).
This persistent non-flat relationship across strike prices forms the implied volatility smile or skew, while variation across maturities generates the volatility term structure.
Together, moneyness and maturity span the two-dimensional volatility surface $\sigma_{IV}(K, T)$.

---

## TL;DR

The volatility surface models implied volatility as a function of strike $K$ and expiration $T$.
Equity index options exhibit a persistent downward-sloping "smirk" or "skew" driven by downside crash hedging demand and structural leverage.
Many FX options, especially between currencies of similar standing, display more symmetric "smiles", while commodity smiles can tilt toward upside strikes when supply shocks dominate.
The term structure reflects market expectations of forward volatility, trading in contango during quiet bull regimes and backwardation during market panics.
Desks model surface dynamics under two primary delta-hedging conventions: sticky strike (implied volatility remains constant at a fixed strike) and sticky delta / sticky moneyness (implied volatility shifts with the underlying asset price).
Parametric models such as Gatheral's SVI (Stochastic Volatility Inspired) and the Hagan SABR model fit the surface smoothly, but neither is arbitrage-free for every parameter set, so butterfly and calendar arbitrage must still be checked after calibration.

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
   - The asymmetry became persistent after the October 19, 1987 crash (Rubinstein 1994); the usual explanations are demand for downside protection ("crash-o-phobia") and the leverage effect (falling equity prices raise debt-to-equity ratios, raising equity volatility).
   - **FX Smiles**: Options on pairs of similar-standing currencies tend to show more symmetric smiles, reflecting fat tails in both directions; pairs with a safe-haven or emerging-market leg are often skewed toward one side.
   - **Commodity Call Skews**: Options on commodities exposed to supply shocks (natural gas and many agricultural contracts, for example) can show positive skew (OTM calls above OTM puts), because shortages produce upside price spikes; the sign of a commodity's skew is not fixed and should be read from the market.

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
   - With zero interest rates and dividends, call prices at a fixed strike must be non-decreasing in maturity (in general the statement holds at fixed forward moneyness):
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
   - SVI is a hyperbola in $k$, so its wings are asymptotically linear with slopes $b(1 + \rho)$ and $b(1 - \rho)$, the shape Roger Lee's moment formula allows; Lee's bound $\limsup w(k)/|k| \le 2$ then requires $b(1 + |\rho|) \le 2$.

2. **Hagan's SABR Model**:
   - A stochastic volatility model governed by forward price $F_t$ and stochastic vol $\alpha_t$:
     $$dF_t = \alpha_t F_t^\beta dW_{1,t}$$
     $$d\alpha_t = \nu \alpha_t dW_{2,t}, \quad d\langle W_1, W_2 \rangle_t = \rho dt$$
   - Produces an analytical asymptotic formula for implied volatility $\sigma_{\text{SABR}}(K, F)$ widely used in interest rate swaptions and FX options.

---

## Worked examples

### Example 1: Forward Implied Volatility and Calendar Arbitrage Check

An options quantitative analyst extracts at-the-money implied volatilities for two maturities on an equity index (hypothetical inputs):
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
   The market is pricing annualized volatility of $23.75\%$ between day 30 and day 90, in the risk-neutral sense of variance-swap strikes.
   The backing script reaches the same $23.75\%$ independently, by replicating each maturity's variance swap with a quadrature over a strip of out-of-the-money option prices.

### Example 2: Skew-Adjusted Delta Under Sticky Moneyness

A market maker is hedging a roughly 25-delta OTM European put on an index (hypothetical inputs):
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
> Rubinstein (1994, Journal of Finance) shows S&P 500 index option smiles were close to flat before October 1987 and persistently skewed afterward, and calls the leading explanation "crash-o-phobia".
> The usual reading is that the crash taught investors to pay up for downside protection, so out-of-the-money puts have carried higher implied volatility since.

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
> For equity index smiles the fitted rho is negative, which makes the downside (put) wing steeper than the upside wing.

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
> Hagan, Kumar, Lesniewski and Woodward (2002) show that local volatility predicts the smile moves in the opposite direction to the underlying, whereas markets see it move with the underlying, so local-vol deltas and hedges are wrong.
> Local volatility also produces forward smiles that are too flat, which misprices forward-starting and cliquet products.

> [!question]- mkt-opt-054 | What are the core parameters of Hagan's SABR model?
> Alpha (initial volatility), Beta (CEV exponent linking spot to volatility), Rho (spot-vol correlation), and Nu (volatility of volatility).
> SABR is widely used to calibrate interest rate swaptions and FX options smiles.

> [!question]- mkt-opt-055 | Why do commodity markets often exhibit positive volatility skew?
> Supply cannot respond instantly, so inventory shortages produce upside price spikes and buyers pay up for upside protection.
> When that dominates, OTM calls trade above OTM puts; it is common in natural gas and many agricultural options, but the sign varies by commodity and regime.

> [!question]- mkt-opt-056 | What is the variance risk premium (VRP)?
> The difference between risk-neutral and physical expected variance, VRP = E^Q[realized variance] - E^P[realized variance], often approximated as implied minus subsequently realized volatility.
> For equity indices it has been positive on average, the compensation option sellers earn for bearing crash risk; its size varies by sample period, so quote it only with a source and date.

> [!question]- mkt-opt-057 | What is the VIX, and is it an ATM implied volatility?
> No: it is Cboe's model-free 30-day volatility index, computed from a strip of OTM SPX calls and puts across strikes, not from ATM options alone, to estimate 30-day risk-neutral expected variance.
> It computes: sigma_VIX^2 = (2 / T) * sum_i (Delta K_i / K_i^2) * exp(r*T) * Q(K_i) - (1 / T) * (F / K_0 - 1)^2.

> [!question]- mkt-opt-058 | How does earnings announcement uncertainty distort the short-dated volatility surface?
> Implied volatility for the contract expiring immediately after earnings surges to account for the discrete event jump.
> Term structure heavily inverts (backwardation) and ATM strike volatility elevates relative to farther expiries.

> [!question]- mkt-opt-059 | What is the implied move derived from an ATM straddle prior to earnings?
> The ATM straddle price is the risk-neutral expected absolute move, so Expected |Move| / Spot ~ Straddle / Spot.
> Under a normal approximation the straddle is sqrt(2/pi) ~ 0.80 times the one-standard-deviation move, so the one-sd move is about Straddle / 0.80 ~ 1.25 * Straddle (not 0.8 * Straddle).

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
> Calendar arbitrage means negative forward variance, so local volatility (Dupire's numerator dC/dT) turns negative and the local-vol PDE or Monte Carlo has no valid diffusion coefficient; the engine fails or prices nonsense.
> Surfaces must be smoothed and arbitrage-free before running pricing algorithms.

## In this repo and The-Distinguished-Engineer

- Code: [mkt_opt_02_vol_surface.py](../code/mkt_opt_02_vol_surface.py) prints and asserts every number in this note; forward volatility is re-derived from variance swaps replicated by quadrature over an option strip, the sticky-moneyness delta by a finite difference that moves the smile with spot, and Breeden-Litzenberger, Dupire and the straddle constant by independent numerical routes; run it with `uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_opt_02_vol_surface.py`.
- Syllabus: [Implied Volatility and the Smile](../../05-Derivatives-and-Volatility/07-Implied-Volatility-and-the-Smile.md), [Volatility Surface Construction](../../05-Derivatives-and-Volatility/08-Volatility-Surface-Construction.md).

---

## Further reading

- Breeden, D. T., & Litzenberger, R. H. (1978). *Prices of state-contingent claims implicit in option prices*. Journal of Business, 51(4), 621-651.
- Dupire, B. (1994). *Pricing with a smile*. Risk, 7(1), 18-20.
- Hagan, P. S., Kumar, D., Lesniewski, A. S., & Woodward, D. E. (2002). *Managing smile risk*. Wilmott Magazine, 1, 84-108.
- Gatheral, J. (2004). *A parsimonious arbitrage-free implied volatility parameterization with application to the valuation of volatility derivatives*. Presentation, Global Derivatives & Risk Management, Madrid, May 2004.
- Gatheral, J., & Jacquier, A. (2014). *Arbitrage-free SVI volatility surfaces*. Quantitative Finance, 14(1), 59-71.
- Lee, R. (2004). *The moment formula for implied volatility at extreme strikes*. Mathematical Finance, 14(3), 469-480.
- Rubinstein, M. (1994). *Implied binomial trees*. Journal of Finance, 49(3), 771-818.
- Gatheral, J. (2006). *The Volatility Surface: A Practitioner's Guide*. John Wiley & Sons.
