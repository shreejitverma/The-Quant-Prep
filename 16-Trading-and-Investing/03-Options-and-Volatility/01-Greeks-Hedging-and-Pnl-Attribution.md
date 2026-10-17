---
type: concept
title: "Options Greeks, Dynamic Hedging, and PnL Attribution"
track: [quant-trader, quant-research]
tier: advanced
status: solid
est_hours: 1.5
tags: [options, greeks, delta-hedging, gamma, vega, theta, vanna, volga, pnl-attribution]
prereqs: []
---

# Options Greeks, Dynamic Hedging, and PnL Attribution

Options are non-linear derivatives whose values depend simultaneously on underlying spot price, elapsed time, implied volatility, interest rates, and dividend yields.
Rather than treating options as directional leverage, quantitative derivatives desks decompose portfolio sensitivity into orthogonal risk dimensions known as the Greeks.
Mastering analytical Greek formulas, second-order cross sensitivities, and Taylor series PnL attribution is the mathematical foundation of options market making and volatility trading.

---

## TL;DR

The Greeks measure the partial derivatives of an option's theoretical pricing model with respect to its underlying parameters.
Delta ($\Delta$) and Gamma ($\Gamma$) govern directional and curvature risk; Theta ($\Theta$) measures time decay; Vega ($\mathcal{V}$) quantifies volatility sensitivity.
Second-order cross Greeks - Vanna ($\frac{\partial \Delta}{\partial \sigma}$) and Volga ($\frac{\partial \mathcal{V}}{\partial \sigma}$) - dictate risk during extreme volatility spikes.
The PnL of an options book decomposes via Taylor expansion into:
$$\Delta \text{PnL} \approx \Delta \cdot \Delta S + \frac{1}{2} \Gamma (\Delta S)^2 + \mathcal{V} \cdot \Delta \sigma + \Theta \cdot \Delta t + \text{Vanna} \cdot \Delta S \Delta \sigma + \frac{1}{2} \text{Volga} (\Delta \sigma)^2$$

---

## Learning objectives

- Formulate the closed-form Black-Scholes-Merton equations for first-order and second-order Greeks.
- Implement finite difference approximations to verify analytical Greek derivatives.
- Apply Taylor series expansion to execute exact PnL attribution across multi-asset options books.
- Quantify cross Greeks (Vanna, Volga, Charm) and explain their impact on dealer hedging flows.
- Formulate dynamic delta-neutral hedging schedules and measure hedging error under discrete rebalancing.

---

## Core concepts

### 1. First-Order Greeks Under Black-Scholes-Merton

In the standard Black-Scholes-Merton (BSM) framework with spot price $S$, strike $K$, risk-free rate $r$, dividend yield $q$, volatility $\sigma$, and time to maturity $T$:

$$d_1 = \frac{\ln(S / K) + (r - q + \frac{1}{2}\sigma^2)T}{\sigma \sqrt{T}}, \quad d_2 = d_1 - \sigma \sqrt{T}$$

1. **Delta ($\Delta = \frac{\partial V}{\partial S}$)**:
   - Measures the rate of change of option value with respect to spot price:
     $$\Delta_{\text{call}} = e^{-q T} N(d_1) \in [0, 1]$$
     $$\Delta_{\text{put}} = -e^{-q T} N(-d_1) = \Delta_{\text{call}} - e^{-q T} \in [-1, 0]$$
   - Serves as the continuous hedge ratio: to neutralize directional risk, a desk holding long calls sells $\Delta$ shares of stock.

2. **Theta ($\Theta = \frac{\partial V}{\partial t} = -\frac{\partial V}{\partial T}$)**:
   - Measures the decay of option value as time elapses toward expiration:
     $$\Theta_{\text{call}} = -\frac{S e^{-q T} \phi(d_1) \sigma}{2 \sqrt{T}} - r K e^{-r T} N(d_2) + q S e^{-q T} N(d_1)$$
     $$\Theta_{\text{put}} = -\frac{S e^{-q T} \phi(d_1) \sigma}{2 \sqrt{T}} + r K e^{-r T} N(-d_2) - q S e^{-q T} N(-d_1)$$
   - Always negative for long plain-vanilla options; options lose value simply through the passage of time.

3. **Vega ($\mathcal{V} = \frac{\partial V}{\partial \sigma}$)**:
   - Measures sensitivity to changes in implied volatility:
     $$\mathcal{V} = S e^{-q T} \phi(d_1) \sqrt{T}$$
   - Identical for European calls and puts.
   - Highest for at-the-money (ATM) options with long maturities.

4. **Rho ($\rho = \frac{\partial V}{\partial r}$)**:
   - Measures sensitivity to the risk-free interest rate:
     $$\rho_{\text{call}} = K T e^{-r T} N(d_2), \quad \rho_{\text{put}} = -K T e^{-r T} N(-d_2)$$

### 2. Second-Order and Cross Greeks

1. **Gamma ($\Gamma = \frac{\partial^2 V}{\partial S^2} = \frac{\partial \Delta}{\partial S}$)**:
   - Measures the curvature of the option price with respect to spot:
     $$\Gamma = \frac{e^{-q T} \phi(d_1)}{S \sigma \sqrt{T}}$$
   - Always positive for long options; dictates how frequently delta hedges must be rebalanced.
   - Concentrates intensely around the strike for near-dated ATM options as $T \to 0$.

2. **Vanna ($\frac{\partial \Delta}{\partial \sigma} = \frac{\partial \mathcal{V}}{\partial S}$)**:
   - Cross sensitivity connecting directional price moves to volatility changes:
     $$\text{Vanna} = -e^{-q T} \phi(d_1) \frac{d_2}{\sigma}$$
   - For OTM puts ($d_2 < 0$), Vanna is positive; when volatility surges during a crash, put delta expands dramatically, forcing dealers to sell additional underlying stock.

3. **Volga / Vomma ($\frac{\partial^2 V}{\partial \sigma^2} = \frac{\partial \mathcal{V}}{\partial \sigma}$)**:
   - Convexity of option price with respect to implied volatility:
     $$\text{Volga} = \mathcal{V} \frac{d_1 d_2}{\sigma}$$
   - Positive for OTM options; explains why OTM tail hedges expand in value non-linearly during severe volatility spikes.

4. **Charm ($\frac{\partial \Delta}{\partial t} = -\frac{\partial \Delta}{\partial T}$)**:
   - Rate of Delta decay over time:
     $$\text{Charm}_{\text{call}} = q e^{-q T} N(d_1) - e^{-q T} \phi(d_1) \left(\frac{2(r - q)T - d_2 \sigma \sqrt{T}}{2 T \sigma \sqrt{T}}\right)$$
   - Drives systematic dealer delta rebalancing flows into expiration Fridays.

### 3. Taylor Series PnL Decomposition

The comprehensive PnL attribution of an options portfolio over a discrete time step $\Delta t$ with underlying spot move $\Delta S$ and volatility shift $\Delta \sigma$ expands to second order:

$$\Delta \text{PnL} \approx \Delta \cdot \Delta S + \frac{1}{2} \Gamma (\Delta S)^2 + \mathcal{V} \cdot \Delta \sigma + \Theta \cdot \Delta t + \text{Vanna} \cdot \Delta S \Delta \sigma + \frac{1}{2} \text{Volga} (\Delta \sigma)^2 + \text{Residual}$$

In a delta-hedged book ($\Delta = 0$), the first term vanishes, leaving the foundational Gamma-Theta trade-off:

$$\Delta \text{PnL}_{\text{hedged}} \approx \frac{1}{2} \Gamma (\Delta S)^2 + \Theta \cdot \Delta t + \mathcal{V} \cdot \Delta \sigma$$

If the realized price change $|\Delta S|$ generates gamma gains exceeding theta decay, the delta-hedged position is net profitable.

---

## Worked examples

### Example 1: Calculating Greeks for an ATM Index Option

An options trader evaluates a 30-day European call on an index:
- Spot: $S = \$5,000.00$.
- Strike: $K = \$5,000.00$ (ATM).
- Time to Expiry: $T = 30 / 365 = 0.08219$ years ($\sqrt{T} = 0.28669$).
- Implied Volatility: $\sigma = 0.20$ ($20\%$).
- Risk-Free Rate: $r = 0.04$ ($4\%$).
- Dividend Yield: $q = 0.015$ ($1.5\%$).

1. **Calculate $d_1$ and $d_2$**:
   $$\ln(S / K) = \ln(1.0) = 0.0000$$
   $$r - q + 0.5 \sigma^2 = 0.04 - 0.015 + 0.5(0.04) = 0.025 + 0.020 = 0.045$$
   $$d_1 = \frac{0.045 \times 0.08219}{0.20 \times 0.28669} = \frac{0.0036986}{0.057338} = +0.0645$$
   $$d_2 = 0.0645 - 0.057338 = +0.00716$$

2. **Evaluate Standard Normal Functions**:
   $$N(d_1) = N(0.0645) = 0.5257$$
   $$\phi(d_1) = \frac{1}{\sqrt{2\pi}} e^{-0.5(0.0645)^2} = 0.39894 \times 0.99792 = 0.39811$$
   $$e^{-q T} = e^{-0.015 \times 0.08219} = e^{-0.001233} = 0.99877$$

3. **Calculate Analytical Greeks**:
   - **Delta**:
     $$\Delta_{\text{call}} = 0.99877 \times 0.5257 = +0.5251$$
   - **Gamma**:
     $$\Gamma = \frac{0.99877 \times 0.39811}{5000 \times 0.20 \times 0.28669} = \frac{0.39762}{286.69} = 0.001387$$
   - **Vega (per 1% Volatility Move)**:
     $$\mathcal{V}_{\text{unit}} = 5000 \times 0.99877 \times 0.39811 \times 0.28669 = 569.95$$
     $$\mathcal{V}_{1\%} = \frac{569.95}{100} = \$5.70\text{ per option contract}$$
   - **Theta (Daily Calendar Decay)**:
     $$\Theta_{\text{ann}} \approx -\frac{5000 \times 0.99877 \times 0.39811 \times 0.20}{2 \times 0.28669} = -\frac{397.62}{0.57338} = -\$693.47\text{ per year}$$
     $$\Theta_{\text{daily}} = \frac{-\$693.47}{365} = -\$1.90\text{ per day}$$

### Example 2: Discrete Delta Hedging PnL Attribution

A trader sells 100 call contracts ($10,000$ shares equivalent) with the parameters above.
- Initial Position Delta: $-10,000 \times 0.5251 = -5,251\text{ shares}$.
- Initial Hedge: Buy $5,251$ shares of index stock at $\$5,000.00$ to achieve zero net delta.
- Over the next 24 hours ($\Delta t = 1/365$):
  - Spot price rallies to $\$5,050.00$ ($\Delta S = +\$50.00$).
  - Implied volatility drops from $20\%$ to $19\%$ ($\Delta \sigma = -1.0\%$).

**PnL Component Breakdown**:
1. **Delta Contribution**:
   $$\text{PnL}_{\Delta} = \Delta_{\text{net}} \times \Delta S = 0 \times \$50.00 = \$0.00$$
2. **Gamma Contribution**:
   $$\Gamma_{\text{position}} = -10,000 \times 0.001387 = -13.87$$
   $$\text{PnL}_{\Gamma} = \frac{1}{2} \Gamma (\Delta S)^2 = \frac{1}{2} \times (-13.87) \times (50.00)^2 = -6.935 \times 2,500 = -\$17,337.50$$
3. **Theta Contribution**:
   $$\Theta_{\text{position}} = -10,000 \times (-\$1.90) = +\$19,000\text{ per day}$$
   $$\text{PnL}_{\Theta} = +\$19,000.00$$
4. **Vega Contribution**:
   $$\mathcal{V}_{\text{position}} = -10,000 \times (-\$5.70\text{ per 1%}) \dots \text{Short option position Vega is negative}:$$
   $$\mathcal{V}_{\text{net}} = -10,000 \times \$5.70 = -\$57,000\text{ per 1%}$$
   $$\text{PnL}_{\mathcal{V}} = -\$57,000 \times (-1.0\%) = +\$57,000.00$$
5. **Total Attributed PnL**:
   $$\Delta \text{PnL} \approx \$0.00 - \$17,337.50 + \$19,000.00 + \$57,000.00 = +\$58,662.50$$
   The massive gain from implied volatility crush ($+\$57,000$) and theta decay ($+\$19,000$) easily absorbed the gamma loss ($-\$17,338$) from the spot rally.

---

## Pitfalls

- **The Discrete Rebalancing Gamma Leak**:
  Theoretical delta hedging assumes continuous trading; in reality, hedges are rebalanced discretely (e.g. hourly or daily).
  Discrete rebalancing creates an unhedged residual tracking error that scales with $\Gamma \sigma^2 \Delta t$.
- **Ignoring Higher-Order Greeks in Large Market Moves**:
  Second-order delta-gamma approximations fail during market gap openings ($> 3\sigma$).
  Third-order Greeks (Speed $\frac{\partial \Gamma}{\partial S}$, Zomma $\frac{\partial \Gamma}{\partial \sigma}$) must be incorporated during crash modeling.
- **The Weekend Theta Trap**:
  Theta does not decay linearly over weekends; market makers price in weekend decay by closing Friday afternoon, causing implied volatility to drop before the weekend rather than Monday morning.
- **Pin Risk Near Expiration**:
  For near-expiry options trading within pennies of the strike, Gamma approaches infinity and Delta oscillates violently between 0.0 and 1.0.
  Holding unclosed short options through expiration creates extreme overnight assignment uncertainty.

---

## Interview questions

> [!question]- mkt-opt-001 | State the Black-Scholes formula for European Call Delta.
> Delta_call = exp(-q * T) * N(d1).
> For a non-dividend paying stock (q = 0), Call Delta equals N(d1), bounded strictly between 0.0 and 1.0.

> [!question]- mkt-opt-002 | How are Call Delta and Put Delta related under European Put-Call Parity?
> Delta_call - Delta_put = exp(-q * T).
> For a non-dividend asset, Delta_call - Delta_put = 1.0; a 0.60 Delta call corresponds to an identical-strike -0.40 Delta put.

> [!question]- mkt-opt-003 | Why is Gamma identical for European Call and Put options with identical strikes and maturities?
> Put-Call parity states that C - P = S * exp(-q * T) - K * exp(-r * T).
> Taking the second derivative with respect to S yields d^2C/dS^2 - d^2P/dS^2 = 0, proving Gamma_call = Gamma_put.

> [!question]- mkt-opt-004 | What happens to Gamma as an at-the-money option approaches expiration (T -> 0)?
> Gamma concentrates heavily at the strike and approaches infinity: lim_{T -> 0} Gamma_ATM = infinity.
> A minute move in spot price flips Delta discontinuously between 0.0 and 1.0.

> [!question]- mkt-opt-005 | State the Taylor series PnL attribution equation for an options book.
> Delta_PnL ~ Delta * Delta_S + 0.5 * Gamma * (Delta_S)^2 + Vega * Delta_sigma + Theta * Delta_t.
> Second-order cross terms include Vanna * Delta_S * Delta_sigma and 0.5 * Volga * (Delta_sigma)^2.

> [!question]- mkt-opt-006 | What is the fundamental Gamma-Theta trade-off in a delta-neutral book?
> A delta-neutral long options position possesses positive Gamma but negative Theta.
> The position pays daily theta decay in exchange for convex gamma profits when realized spot moves exceed implied volatility.

> [!question]- mkt-opt-007 | Define Vanna and explain its economic significance.
> Vanna is the cross derivative dDelta / dsigma = dVega / dS = -exp(-q*T) * phi(d1) * (d2 / sigma).
> It measures how an option's hedge ratio shifts when implied volatility changes, driving dealer hedging flows during market selloffs.

> [!question]- mkt-opt-008 | Define Volga (Vomma) and explain why out-of-the-money tail options have high Volga.
> Volga is the second derivative of option price with respect to volatility: dVega / dsigma = Vega * (d1 * d2 / sigma).
> Far OTM options have low initial Vega but high Volga, causing their prices to explode non-linearly during sudden volatility spikes.

> [!question]- mkt-opt-009 | What is Charm and how does it influence market-on-close dealer rebalancing?
> Charm is the rate of Delta decay over time: -dDelta / dT.
> As expiration approaches, OTM options bleed Delta toward zero, forcing options dealers to unwind underlying stock hedges before the close.

> [!question]- mkt-opt-010 | What is Vega and at what moneyness strike is it maximized?
> Vega measures the change in option price per 1% change in implied volatility: Vega = S * exp(-q*T) * phi(d1) * sqrt(T).
> Vega is strictly maximized for at-the-money (ATM) options where d1 is close to zero.

> [!question]- mkt-opt-011 | Why does Vega increase with time to maturity while Gamma decreases?
> Vega scales with sqrt(T), meaning long-dated options have greater cumulative sensitivity to volatility uncertainty.
> Gamma scales with 1 / (S * sigma * sqrt(T)), meaning near-dated options have far higher localized price curvature.

> [!question]- mkt-opt-012 | What is Speed in higher-order Greeks?
> Speed is the third derivative of option price with respect to spot: dGamma / dS = d^3V / dS^3.
> It quantifies how rapidly Gamma itself changes during large directional market moves.

> [!question]- mkt-opt-013 | What is Zomma in higher-order Greeks?
> Zomma is the cross derivative dGamma / dsigma = dVega / dS^2.
> It measures the sensitivity of Gamma to changes in implied volatility.

> [!question]- mkt-opt-014 | What is color (Charm derivative) in higher-order Greeks?
> Color is the rate of change of Gamma over time: dGamma / dt.
> It models how dynamic hedging risk accelerates as maturity approaches.

> [!question]- mkt-opt-015 | How does discrete rebalancing introduce gamma leak in delta-hedging?
> Because delta is rebalanced at discrete time steps delta_t rather than continuously, the desk is temporarily unhedged between intervals.
> The variance of hedging error scales with 0.5 * Gamma^2 * S^2 * sigma^4 * delta_t.

> [!question]- mkt-opt-016 | What is the Black-Scholes partial differential equation (PDE)?
> dV/dt + 0.5 * sigma^2 * S^2 * d^2V/dS^2 + r * S * dV/dS - r * V = 0.
> It equates the risk-free return on a delta-hedged portfolio to the balance between theta decay and gamma convexity.

> [!question]- mkt-opt-017 | Why is Rho positive for European calls and negative for European puts?
> Buying a call allows the investor to defer paying the strike price until maturity, earning interest on the cash (positive Rho).
> Buying a put delays receiving the strike cash, incurring an opportunity cost of forgone interest (negative Rho).

> [!question]- mkt-opt-018 | How do dividends impact Call Delta and Put Delta?
> Dividends reduce the forward price of the underlying asset by exp(-q * T).
> Dividend yield q decreases Call Delta and increases Put Delta (makes put delta more negative).

> [!question]- mkt-opt-019 | What is the Carr-Madan formula for the variance of hedging error?
> It shows that the cumulative PnL of a delta-hedged option equals the integrated path: Integral_0^T exp(-r*t) * 0.5 * Gamma_t * S_t^2 * (sigma_realized^2 - sigma_implied^2) dt.
> Delta-hedged options PnL is purely a bet on realized volatility versus implied volatility.

> [!question]- mkt-opt-020 | What is pin risk in options market making?
> The risk that the underlying asset closes exactly at the strike price on expiration Friday.
> The market maker cannot know with certainty whether counterparty options will be exercised, leaving their delta hedge exposed to overnight gap risk.

> [!question]- mkt-opt-021 | What is implied dividend yield and how can it be extracted from option chains?
> The dividend yield priced into option contracts derived from European Put-Call parity: C - P = S * exp(-q*T) - K * exp(-r*T).
> If options trade at a discount to theoretical forward parity, the market is pricing in an imminent dividend hike.

> [!question]- mkt-opt-022 | What is a shadow Greek?
> Sensitivity of an option model's output to parameters that are not directly observable in market quotes, such as jump intensity or correlation.
> Desks manage shadow Greeks to prevent model misspecification during regime shifts.

> [!question]- mkt-opt-023 | Why does a short gamma position experience negative convexity?
> As the underlying price falls, short gamma forces the desk's delta to become increasingly long, compounding losses.
> As the price rises, delta becomes increasingly short, guaranteeing that the desk sells at the bottom and buys at the top.

> [!question]- mkt-opt-024 | What is the Bleed of an options book?
> The total daily carrying cost combining theta time decay, cash financing margin, and stock borrow fees.
> A long options book must generate sufficient realized gamma scalping gains to exceed its daily bleed rate.

> [!question]- mkt-opt-025 | What is smile curvature and how is it related to Volga?
> Smile curvature is the second derivative of implied volatility with respect to strike: d^2 sigma_IV / dK^2.
> High Volga in OTM options directly drives the steepness of the volatility smile curvature.

> [!question]- mkt-opt-026 | How does a finite difference grid verify an analytical Greek implementation?
> By computing two-sided central differences: Delta_FD = (V(S + eps) - V(S - eps)) / (2 * eps).
> If analytical Greek code differs from finite difference estimates by more than machine epsilon tolerances, a derivation bug exists.

> [!question]- mkt-opt-027 | Why do deep in-the-money (ITM) puts carry negative Theta under high interest rates?
> A deep ITM put has virtually zero time premium and is worth K * exp(-r*T) - S.
> As time passes, the present value of the cash to be received grows, creating positive daily theta for the put owner.

> [!question]- mkt-opt-028 | What is dollar gamma (cash gamma) and how is it calculated?
> Dollar Gamma = 0.5 * Gamma * S^2 / 100.
> It quantifies the dollar change in position delta for a 1% move in the underlying asset, enabling direct comparison across multi-price assets.

> [!question]- mkt-opt-029 | What is Vega weighted by time to maturity (Weighted Vega)?
> Weighting Vega by 1 / sqrt(T) to normalize volatility exposure across contracts with differing maturities.
> It prevents long-dated LEAPS from dominating risk reports when near-dated contracts carry far higher immediate realized volatility risk.

> [!question]- mkt-opt-030 | Explain the term "Delta bleed" in a trending market.
> The continuous shift in a portfolio's net delta caused by the underlying price moving across the gamma curvature.
> In a sharp market rally, short call delta becomes more negative, requiring continuous stock purchases to restore neutrality.

> [!question]- mkt-opt-031 | What is an American option early exercise boundary?
> The critical underlying asset price at which the immediate intrinsic payoff from exercising exceeds the continuation value of holding the option.
> American puts on non-dividend stocks and American calls on high-dividend stocks are vulnerable to early exercise.

> [!question]- mkt-opt-032 | Why must options market makers dynamically hedge Gamma using options rather than underlying stock?
> Stock has zero Gamma (linear delta of 1.0), meaning stock trades can only neutralize Delta, leaving Gamma exposure unchanged.
> To neutralize Gamma, the desk must trade other options contracts with offsetting second-order curvature.

---

## Further reading

- Black, F., & Scholes, M. (1973). *The pricing of options and corporate liabilities*. Journal of Political Economy, 81(3), 637-654.
- Merton, R. C. (1973). *Theory of rational option pricing*. The Bell Journal of Economics and Management Science, 141-183.
- Carr, P., & Madan, D. (1998). *Towards a theory of volatility trading*. Volatility: New Estimation Techniques for Pricing and Risk Management, 29(1), 417-427.
- Natenberg, S. (2014). *Option Volatility and Pricing: Advanced Trading Strategies and Techniques*. McGraw-Hill Education.
