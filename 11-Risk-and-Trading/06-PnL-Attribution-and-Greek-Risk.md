---
type: concept
track: [quant-trader, quant-dev]
tier: core
status: draft
prereqs: [the-greeks]
est_hours: 4
sources: [Sheldon Natenberg - Option Volatility and Pricing chapters 6-12, John Hull - Options Futures and Other Derivatives chapters 19 and 25, Emanuel Derman and Michael Kamal - When You Cannot Hedge Continuously (1999), Peter Carr and Dilip Madan - Towards a Theory of Volatility Trading]
---

# P&L Attribution and Greek Risk

## TL;DR

Daily Profit and Loss (P&L) attribution for derivatives portfolios decomposes total dollar performance into orthogonal Greek risk factor contributions: delta (underlying price shift), gamma (curvature), theta (time decay), vega (implied volatility shift), vanna (cross price-volatility), and volga (volatility convexity).
For a delta-hedged options portfolio, the Black-Scholes partial differential equation links theta decay directly to gamma: $\Theta + \frac{1}{2}\sigma_{\text{imp}}^2 S^2 \Gamma = 0$.
A long gamma position pays a daily theta rent, requiring underlying price fluctuations $|\Delta S|$ to exceed the break-even threshold $\sigma_{\text{imp}} S \sqrt{\Delta t}$ to generate net profit.
Cumulative delta-hedged P&L is fundamentally an arbitrage between realized asset volatility and implied volatility: $\text{P\&L} \approx \frac{1}{2}\int S^2 \Gamma (\sigma_{\text{realized}}^2 - \sigma_{\text{implied}}^2) dt$.
Unexplained P&L ($\epsilon$) isolates model leakage, discrete hedging error, financing slippage, and dividend jumps, providing an essential diagnostic for trading desk integrity.

## Learning objectives

- Formulate the full multi-factor Taylor series P&L attribution equation across first, second, and cross-order Greeks.
- Derive the relationship between Theta and Gamma under the Black-Scholes partial differential equation.
- Compute the daily break-even asset move for a delta-hedged long options position.
- Relate delta-hedged options P&L to the variance spread $(\sigma_{\text{realized}}^2 - \sigma_{\text{implied}}^2)$.
- Attribute higher-order volatility surface risks: Vanna ($\partial \Delta / \partial \sigma$), Volga ($\partial \mathcal{V} / \partial \sigma$), and Charm ($\partial \Delta / \partial t$).
- Identify and troubleshoot the primary sources of unexplained residual P&L ($\epsilon$), including discrete rebalancing latency and bid-ask friction.
- Construct actionable daily risk ladder reports and matrix revaluations for options market making.

## Core concepts

### The Derivative P&L Attribution Framework

Let $\Pi(S, \sigma, t, r)$ represent the market value of a derivatives portfolio dependent on underlying price $S$, implied volatility $\sigma$, calendar time $t$, and risk-free interest rate $r$.
Over a discrete holding interval $\Delta t$, the underlying asset moves by $\Delta S$, implied volatility shifts by $\Delta \sigma$, and interest rates shift by $\Delta r$.
A second-order multivariate Taylor expansion decomposes the total observed dollar change $\Delta \Pi_{\text{actual}}$ into theoretical Greek contributions plus an unexplained residual $\epsilon$:

$$\Delta \Pi_{\text{actual}} = \Delta \Pi_{\text{Delta}} + \Delta \Pi_{\text{Gamma}} + \Delta \Pi_{\text{Theta}} + \Delta \Pi_{\text{Vega}} + \Delta \Pi_{\text{Vanna}} + \Delta \Pi_{\text{Volga}} + \Delta \Pi_{\text{Rho}} + \epsilon$$

where the individual risk factor contributions are defined as:

1. **Delta P&L (Linear Underlying Price Risk):**

$$\Delta \Pi_{\text{Delta}} = \Delta \cdot \Delta S = \frac{\partial \Pi}{\partial S} \cdot \Delta S$$

2. **Gamma P&L (Curvature / Convexity Gain):**

$$\Delta \Pi_{\text{Gamma}} = \frac{1}{2} \Gamma \cdot (\Delta S)^2 = \frac{1}{2} \frac{\partial^2 \Pi}{\partial S^2} \cdot (\Delta S)^2$$

3. **Theta P&L (Deterministic Time Decay):**

$$\Delta \Pi_{\text{Theta}} = \Theta \cdot \Delta t = \frac{\partial \Pi}{\partial t} \cdot \Delta t$$

4. **Vega P&L (Implied Volatility Shift):**

$$\Delta \Pi_{\text{Vega}} = \mathcal{V} \cdot \Delta \sigma = \frac{\partial \Pi}{\partial \sigma} \cdot \Delta \sigma$$

5. **Vanna P&L (Cross Price-Volatility Risk):**

$$\Delta \Pi_{\text{Vanna}} = \text{Vanna} \cdot \Delta S \cdot \Delta \sigma = \frac{\partial^2 \Pi}{\partial S \partial \sigma} \cdot \Delta S \cdot \Delta \sigma$$

6. **Volga / Vomma P&L (Volatility Convexity):**

$$\Delta \Pi_{\text{Volga}} = \frac{1}{2} \text{Volga} \cdot (\Delta \sigma)^2 = \frac{1}{2} \frac{\partial^2 \Pi}{\partial \sigma^2} \cdot (\Delta \sigma)^2$$

7. **Rho P&L (Interest Rate Sensitivity):**

$$\Delta \Pi_{\text{Rho}} = \rho \cdot \Delta r = \frac{\partial \Pi}{\partial r} \cdot \Delta r$$

8. **Unexplained P&L ($\epsilon$):**
The residual difference between realized book P&L and predicted Greek P&L:

$$\epsilon = \Delta \Pi_{\text{actual}} - \Delta \Pi_{\text{predicted}}$$

A well-specified risk system requires that $|\epsilon|$ remain within $5\%$ to $10\%$ of total P&L under normal market conditions.

### The Black-Scholes PDE Identity: Theta vs. Gamma

The fundamental Black-Scholes partial differential equation for a derivative price $V(S, t)$ with zero risk-free rate ($r = 0$) and zero dividend yield ($q = 0$) states:

$$\frac{\partial V}{\partial t} + \frac{1}{2} \sigma_{\text{imp}}^2 S^2 \frac{\partial^2 V}{\partial S^2} = 0 \iff \Theta + \frac{1}{2} \sigma_{\text{imp}}^2 S^2 \Gamma = 0$$

For a delta-neutral portfolio ($\Pi_{\text{hedged}} = V - \Delta \cdot S$), the portfolio delta is zero ($\Delta_{\text{net}} = 0$).
Substituting the PDE identity into the 1-day P&L attribution equation (assuming $\Delta \sigma = 0$):

$$\Delta \Pi_{\text{hedged}} = \frac{1}{2} \Gamma \cdot (\Delta S)^2 + \Theta \cdot \Delta t = \frac{1}{2} \Gamma \cdot (\Delta S)^2 - \frac{1}{2} \sigma_{\text{imp}}^2 S^2 \Gamma \cdot \Delta t = \frac{1}{2} \Gamma \left[ (\Delta S)^2 - \sigma_{\text{imp}}^2 S^2 \Delta t \right]$$

This equation exposes the central economic trade-off in options trading:
- **Gamma Gain:** Positive whenever the stock moves ($(\Delta S)^2 > 0$).
- **Theta Rent:** A continuous, non-negotiable cash decay paid to hold the option position.

#### The Daily Break-Even Move
Setting $\Delta \Pi_{\text{hedged}} = 0$ yields the daily break-even price movement:

$$(\Delta S)^2 = \sigma_{\text{imp}}^2 S^2 \Delta t \implies |\Delta S_{\text{break-even}}| = \sigma_{\text{imp}} S \sqrt{\Delta t}$$

For a 1-day holding period ($\Delta t = 1/252$), using the Rule of 16 ($\sqrt{252} \approx 15.87 \approx 16$):

$$|\Delta S_{\text{break-even}}| \approx \frac{\sigma_{\text{imp}}}{16} \times S$$

If the stock moves by more than $\sigma_{\text{imp}}/16$ of its price over a day, the long gamma position profits; if it moves by less, theta decay dominates and the position incurs a net loss.

### Realized vs. Implied Volatility P&L

Accumulating discrete 1-day delta-hedged revaluations over the full life of the option $[0, T]$:
Let $S_t$ follow a continuous diffusion with instantaneous realized volatility $\sigma_{\text{realized}}(t)$:

$$(dS_t)^2 = \sigma_{\text{realized}}^2(t) S_t^2 dt$$

The cumulative P&L of a continuously delta-hedged option position is given by:

$$\text{P\&L}_{\text{cumulative}} = \frac{1}{2} \int_0^T S_t^2 \Gamma_t \left( \sigma_{\text{realized}}^2(t) - \sigma_{\text{implied}}^2 \right) dt$$

This fundamental theorem of volatility trading proves that:
- A long option position is economically equivalent to buying realized variance $\sigma_{\text{realized}}^2$ and selling implied variance $\sigma_{\text{implied}}^2$.
- The dollar profit earned is weighted by the dollar gamma $S_t^2 \Gamma_t$ at each point along the price path.
- If realized volatility exceeds implied volatility, the delta-hedged position generates positive P&L regardless of whether the stock moves up or down.

### Higher-Order Volatility Surface Greeks

As market volatility surfaces shift dynamically, second-order cross Greeks become critical drivers of desk P&L:

- **Vanna ($\frac{\partial^2 V}{\partial S \partial \sigma} = \frac{\partial \Delta}{\partial \sigma} = \frac{\partial \mathcal{V}}{\partial S}$):** Measures how delta changes when volatility moves, or how vega changes when the underlying price moves.
  - OTM call options have positive vanna; OTM put options have negative vanna.
  - When the market crashes and volatility spikes ($\Delta S < 0, \Delta \sigma > 0$), vanna generates significant directional delta shifts that require immediate re-hedging.
- **Volga / Vomma ($\frac{\partial^2 V}{\partial \sigma^2} = \frac{\partial \mathcal{V}}{\partial \sigma}$):** Measures the convexity of option price with respect to implied volatility.
  - Always positive for vanilla options; peaks in out-of-the-money wings.
  - Volga explains why long OTM wings gain value disproportionately when market volatility explodes.
- **Charm / Delta Decay ($-\frac{\partial \Delta}{\partial t}$):** Measures how option delta decays over time toward expiry.
  - An ITM call delta drifts toward 1.0; an OTM call delta drifts toward 0.0.
  - Traders must rebalance hedges over weekends and holidays due to charm decay even if asset prices remain unchanged.

### Sources of Unexplained P&L ($\epsilon$)

When daily P&L attribution reports a large unexplained residual $\epsilon$, quant developers and risk managers inspect standard operational leakages:

1. **Discrete Rebalancing Error (Hedging Latency):** Continuous delta hedging is an idealized abstraction. If a trader rebalances once per day, large intraday trends or gaps introduce discrete variance error:

$$\text{Var}(\text{Hedging Error}) \approx \frac{\pi}{4} \frac{\mathcal{V}^2 \sigma^2}{N} \quad (\text{Derman-Kamal formula})$$

2. **Bid-Ask Spread and Execution Slippage:** Rebalancing delta requires crossing the bid-ask spread on underlying cash shares or futures, generating steady negative cash flow drag.
3. **Volatility Surface Non-Parallel Shifts (Smile Twist):** If implied volatility shifts heterogeneously across strikes (skew steepening or flattening), a single flat-vega metric fails, requiring bucketed vega matrix attribution.
4. **Borrow Costs and Dividend Discrete Jumps:** Stocks paying unannounced special dividends or experiencing hard-to-borrow repo fee surges create jumps in options prices unaccounted for by continuous-rate Greeks.
5. **Cross-Asset Volatility Leakage:** In multi-asset correlation books, cross-gamma terms ($\frac{\partial^2 \Pi}{\partial S_1 \partial S_2}$) produce large unexplained P&L if the attribution system only computes single-asset diagonal gammas.

## Worked examples

### Example 1: Full Daily Greek P&L Attribution

An options trader holds a long straddle on stock $XYZ$:
- Current stock price $S = \$100.00$.
- Implied volatility $\sigma = 25.0\%$ ($0.250$).
- Total portfolio Greeks:
  - $\Delta = 0.0$ (delta neutral).
  - $\Gamma = +1,200 \text{ per } \$1 \text{ move}$.
  - $\Theta = -\$1,562.50 \text{ per day}$ ($\Delta t = 1/252$).
  - $\mathcal{V} = +\$6,250 \text{ per } 1\% \text{ vol point}$ ($+\$625,000 \text{ per unit vol}$).
  - $\text{Vanna} = +\$25,000 \text{ per } \$1 \text{ stock move per unit vol}$.
  - $\text{Volga} = +\$1,250,000 \text{ per unit vol squared}$.

Overnight, corporate earnings are announced:
- Stock price jumps from $\$100.00$ to $\$104.00$ ($\Delta S = +\$4.00$).
- Implied volatility collapses from $25.0\%$ to $21.0\%$ ($\Delta \sigma = -0.040$, a 4-point drop).
- Elapsed time $\Delta t = 1 \text{ day}$.
- Realized change in portfolio market value: $\Delta \Pi_{\text{actual}} = -\$13,500$.

Perform the full Greek P&L attribution and calculate the unexplained residual.

**Solution:**

Step 1: Delta P&L:

$$\Delta \Pi_{\text{Delta}} = \Delta \times \Delta S = 0 \times \$4.00 = \$0.00$$

Step 2: Gamma P&L (Convexity Gain):

$$\Delta \Pi_{\text{Gamma}} = \frac{1}{2} \Gamma (\Delta S)^2 = \frac{1}{2} \times 1,200 \times (4.00)^2 = 600 \times 16.0 = +\$9,600.00$$

Step 3: Theta P&L (Time Decay):

$$\Delta \Pi_{\text{Theta}} = \Theta \times 1 = -\$1,562.50$$

Step 4: Vega P&L (Vol Crush):

$$\Delta \Pi_{\text{Vega}} = \mathcal{V} \times \Delta \sigma = \$625,000 \times (-0.040) = -\$25,000.00$$

Step 5: Vanna P&L (Cross Term):

$$\Delta \Pi_{\text{Vanna}} = \text{Vanna} \times \Delta S \times \Delta \sigma = \$25,000 \times 4.00 \times (-0.040) = -\$4,000.00$$

Step 6: Volga P&L (Vol Convexity):

$$\Delta \Pi_{\text{Volga}} = \frac{1}{2} \text{Volga} \times (\Delta \sigma)^2 = \frac{1}{2} \times \$1,250,000 \times (-0.040)^2 = \$625,000 \times 0.0016 = +\$1,000.00$$

Step 7: Total Predicted P&L:

$$\Delta \Pi_{\text{predicted}} = \$0 + \$9,600 - \$1,562.50 - \$25,000 - \$4,000 + \$1,000 = -\$19,962.50$$

Step 8: Compute Unexplained P&L ($\epsilon$):

$$\epsilon = \Delta \Pi_{\text{actual}} - \Delta \Pi_{\text{predicted}} = -\$13,500.00 - (-\$19,962.50) = +\$6,462.50$$

Explanation: The 4-point stock move generated a $+\$9,600$ gamma profit, but the 4-vol-point post-earnings volatility crush caused a $-\$25,000$ vega loss and $-\$4,000$ vanna drag.
The $+\$6,462.50$ positive residual arose because the option was deeply non-linear over a $\$4.00$ gap, causing higher-order speed and vol cross-derivatives to cushion the loss relative to second-order Taylor estimates.

### Example 2: Discrete Hedging Error Estimation (Derman-Kamal)

A trader delta hedges a portfolio of 1-month ATM options ($T = 1/12 \approx 0.0833$ years).
The underlying stock trades at $S = \$50.00$ with annual volatility $\sigma = 30\%$ ($0.30$).
The total portfolio vega is $\mathcal{V} = \$100,000 \text{ per unit vol}$ ($\$1,000 \text{ per point}$).
The trader rebalances delta once per day ($N = 21$ trading days).
Estimate the standard deviation of hedging error over the 1-month life of the position.

**Solution:**

Step 1: Apply Derman and Kamal's discrete hedging error formula:

$$\sigma_{\text{hedge}} \approx \sqrt{\frac{\pi}{4}} \times \frac{\mathcal{V} \cdot \sigma}{\sqrt{N}}$$

Step 2: Evaluate constant factor:

$$\sqrt{\frac{\pi}{4}} = \sqrt{0.785398} \approx 0.886227$$

Step 3: Evaluate numerator ($\mathcal{V} \cdot \sigma$):

$$\mathcal{V} \cdot \sigma = \$100,000 \times 0.30 = \$30,000$$

Step 4: Evaluate denominator ($\sqrt{N}$):

$$\sqrt{N} = \sqrt{21} \approx 4.582576$$

Step 5: Compute standard deviation of discrete hedging P&L:

$$\sigma_{\text{hedge}} \approx 0.886227 \times \frac{\$30,000}{4.582576} \approx 0.886227 \times \$6,546.54 \approx \$5,801.71$$

Due to discrete daily rebalancing, the delta-hedged position will exhibit a standard deviation of approximately $\pm \$5,802$ around its theoretical Black-Scholes P&L.
Increasing rebalancing frequency to 4 times per day ($N = 84$) reduces standard error by half to $\approx \$2,901$.

## Pitfalls

- **Ignoring the Vanna Cross Term in Fast Markets:** When both price and volatility move simultaneously (e.g., an equity sell-off accompanied by a VIX surge), attributing P&L using only independent Delta and Vega terms produces massive unexplained residual errors.
- **Double Counting Cash Carry and Theta:** Option pricing libraries often bundle interest rate financing into theta; combining model theta with separate money market funding P&L double counts interest carry.
- **Assuming Homogeneous Implied Volatility Shifts:** Applying a single parallel vega shock to a portfolio spanning multiple strikes and expirations ignores term structure skew twists and skew steepening.
- **Misinterpreting High Unexplained P&L:** Treating a large residual $\epsilon$ as statistical noise rather than actively investigating trade booking mismatches, dividend timing errors, or corrupted market data feeds.
- **Treating Delta as Static Over Intraday Gaps:** In fast-moving gap markets, relying on morning start-of-day delta to compute delta P&L without gamma integration produces severe misattribution.

## Interview questions

> [!question]- pnl-attribution-equation | State the second-order Taylor expansion P&L attribution equation for an equity options portfolio.
> Total P&L is decomposed into first, second, and cross-order Greeks: $\Delta \Pi = \Delta \cdot \Delta S + \frac{1}{2}\Gamma \cdot (\Delta S)^2 + \Theta \cdot \Delta t + \mathcal{V} \cdot \Delta \sigma + \text{Vanna} \cdot \Delta S \Delta \sigma + \frac{1}{2}\text{Volga} \cdot (\Delta \sigma)^2 + \rho \cdot \Delta r + \epsilon$, where $\epsilon$ represents unexplained residual leakage.

> [!question]- theta-gamma-pde-relationship | What is the relationship between Theta and Gamma in the Black-Scholes model for a delta-neutral portfolio?
> Under the Black-Scholes PDE with zero interest rates and dividends, $\Theta + \frac{1}{2}\sigma_{\text{imp}}^2 S^2 \Gamma = 0$, meaning $\Theta = -\frac{1}{2}\sigma_{\text{imp}}^2 S^2 \Gamma$. Theta and Gamma are perfect economic mirror images: positive gamma (convexity) requires paying continuous negative theta (time decay), while positive theta income requires accepting negative gamma risk.

> [!question]- daily-breakeven-move-rule | Derive the daily break-even asset move for a delta-hedged options position using the Rule of 16.
> Setting daily delta-hedged P&L $\frac{1}{2}\Gamma (\Delta S)^2 + \Theta \Delta t = 0$ yields $(\Delta S)^2 = \sigma_{\text{imp}}^2 S^2 \Delta t$. Taking the square root for a 1-day horizon ($\Delta t = 1/252$) and applying $\sqrt{252} \approx 16$ gives $|\Delta S_{\text{break-even}}| \approx \frac{\sigma_{\text{imp}}}{16} \times S$. The underlying asset must move by more than $\sigma/16$ percent in a day for gamma gains to outpace theta decay.

> [!question]- variance-spread-pnl | How does the cumulative P&L of a delta-hedged option relate to realized and implied volatility?
> The cumulative P&L equals the dollar-gamma-weighted integral of the variance spread: $\text{P\&L} \approx \frac{1}{2}\int_0^T S_t^2 \Gamma_t (\sigma_{\text{realized}}^2(t) - \sigma_{\text{implied}}^2) dt$. If realized volatility exceeds implied volatility over the option's life, the delta-hedged position generates a net profit, confirming that delta-hedged options trading is an arbitrage on variance.

> [!question]- vanna-economic-meaning | What is Vanna ($\partial^2 V / \partial S \partial \sigma$), and why is it critical during market sell-offs?
> Vanna measures the sensitivity of delta to shifts in implied volatility (or vega to underlying price). During a market crash, equity prices fall while implied volatility spikes ($\Delta S < 0, \Delta \sigma > 0$). Negative vanna on downside puts causes portfolio delta to become rapidly more short, requiring automated buying to remain delta-neutral and creating significant cross-factor P&L.

> [!question]- volga-economic-meaning | What is Volga (Vomma), and which options positions benefit from it?
> Volga is the second derivative of option value with respect to implied volatility: $\frac{\partial^2 V}{\partial \sigma^2} = \frac{\partial \mathcal{V}}{\partial \sigma}$. It measures volatility convexity. Vanilla options have strictly positive volga, peaking in out-of-the-money options. Long OTM strangle positions benefit heavily from volga when market volatility surges non-linearly.

> [!question]- charm-delta-decay | What is Charm, and why must market makers re-hedge over non-trading weekends?
> Charm is the rate of change of delta with respect to time ($-\partial \Delta / \partial t$). Over a weekend, two full days of time elapse with zero price movement. In-the-money option deltas drift closer to 1.0, while out-of-the-money deltas drift closer to 0.0. Market makers must anticipate this charm decay on Friday afternoon to avoid arriving Monday morning with unwanted directional delta exposure.

> [!question]- unexplained-pnl-root-causes | What are the three most common causes of high unexplained P&L ($\epsilon$) on an equity options desk?
> First, discrete rebalancing latency, where large intraday asset price swings occur between hedging intervals. Second, volatility skew twists, where implied volatilities across strikes move heterogeneously while the risk system applies a single parallel vega shock. Third, inaccurate corporate action data, such as unexpected ex-dividend dates or sudden changes in borrow rates.

> [!question]- derman-kamal-hedging-error | According to the Derman-Kamal formula, how does discrete hedging error scale with rebalancing frequency?
> Discrete hedging error standard deviation scales inversely with the square root of the number of rebalancing intervals: $\sigma_{\text{hedge}} \propto \frac{\mathcal{V} \cdot \sigma}{\sqrt{N}}$. Doubling rebalancing frequency (e.g., from daily to four times a day) reduces tracking variance by half and error standard deviation by $\approx 29\%$.

> [!question]- ladder-risk-reports | What is a Greek ladder risk report, and why is it superior to scalar Greek summary metrics?
> A Greek ladder report revalues the portfolio across a grid of discrete underlying price bumps (e.g., $-10\%, -5\%, -2\%, 0\%, +2\%, +5\%, +10\%$) and volatility shifts (e.g., $-5\text{ pts}, 0, +5\text{ pts}$). It is superior to scalar Greek numbers because it exposes non-linear convexity traps, gamma flips, and vanna interactions that single-point Taylor approximations conceal.

## Further reading

- Sheldon Natenberg, *Option Volatility and Pricing*, Chapters 6-12.
- John Hull, *Options, Futures, and Other Derivatives*, Chapter 19: "The Greek Letters".
- Emanuel Derman and Michael Kamal (1999), "When You Cannot Hedge Continuously: The Corrections to Black-Scholes", *Goldman Sachs Quantitative Strategies Research Notes*.
- Peter Carr and Dilip Madan (1998), "Towards a Theory of Volatility Trading", in *Volatility: New Techniques for Pricing and Hedging*.
- Taleb, N. N., *Dynamic Hedging: Managing Vanilla and Exotic Options*.

## In this repo and SDE-Interview-Prep

- Core Greek definitions and derivations: [The Greeks](../05-Derivatives-and-Volatility/05-The-Greeks.md).
- Python reference implementation of Greeks bump engine: [risk_analytics.py](code/risk_analytics.py).
- Drawdown management and risk thresholds: [Drawdowns and Risk Limits](05-Drawdowns-and-Risk-Limits.md).
- Sensitivity approximations and revaluation: [Sensitivities and Revaluation](12-Sensitivities-and-Revaluation.md).
