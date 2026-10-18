---
type: concept
title: "Dealer Positioning, Gamma Exposure (GEX), and Flow Dynamics"
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: solid
est_hours: 1.5
tags: [options, gex, gamma-exposure, dealer-positioning, vanna-flows, charm-flows, pin-risk, market-microstructure]
prereqs: []
---

# Dealer Positioning, Gamma Exposure (GEX), and Flow Dynamics

In modern equity derivative markets, options market makers and institutional dealers do not hold speculative directional bets.
Instead, they continuously hedge their portfolio risks in the underlying cash and futures markets to maintain delta neutrality.
Because dealers collectively hold tens of billions of dollars in options gamma across index and single-stock chains, their automated rebalancing flows act as a major structural force governing market liquidity, intraday volatility, and price discovery.
Understanding aggregate Gamma Exposure (GEX), the zero-gamma flip point, and second-order Vanna and Charm flows allows quantitative traders to anticipate systematic institutional order flow.

---

## TL;DR

Gamma Exposure (GEX) quantifies the aggregate dollar value of underlying stock that options dealers must buy or sell for every $1\%$ move in the underlying asset.
When dealers are net Long Gamma (typically when spot trades above major put open interest), their dynamic hedging is counter-cyclical: they buy dips and sell rips, compressing market volatility.
When dealers are net Short Gamma (typically when spot drops below the "zero gamma flip point"), their hedging becomes pro-cyclical: they sell falling markets and buy rising markets, amplifying price swings and liquidity air pockets.
Beyond delta-gamma rebalancing, cross-Greek flows - notably Vanna (delta changes induced by volatility shifts) and Charm (delta changes induced by the passage of time toward expiration) - drive multi-billion-dollar programmatic flows into market closes and expiration Fridays.

---

## Learning objectives

- Formulate and calculate aggregate spot and dollar Gamma Exposure (GEX) across option chains.
- Derive the zero-gamma flip point and evaluate market regime transitions between volatility suppression and acceleration.
- Model dealer dynamic delta rebalancing flows under long gamma and short gamma regimes.
- Quantify second-order Vanna and Charm flows and project their timing around monthly options expiration (OpEx).
- Explain the mechanics of strike pinning on expiration and identify structural limits to GEX modeling.

---

## Core concepts

### 1. Market Maker Inventory Assumptions and GEX Formulation

To calculate aggregate dealer positioning from public exchange open interest (OI), quantitative desks make structural assumptions regarding retail and institutional customer trading behavior:
- **Customers are net buyers of protective puts**: Institutional asset managers systematically purchase out-of-the-money puts for downside portfolio insurance.
  Consequently, options dealers are structurally **short puts**.
- **Customers are net sellers of covered calls and buyers of upside calls**: Retail investors and yield-enhancement funds sell call options against long stock (covered call strategies), while retail speculators purchase out-of-the-money call options.
  On net balance across index chains, dealers are structurally **long calls**.

For a single option contract $i$ on strike $K_i$ with open interest $\text{OI}_i$, underlying spot price $S$, and contract multiplier $M$ (typically $100$ shares):

1. **Spot Gamma Exposure ($\text{GEX}_i$)**:
   $$\text{GEX}_i^{\text{call}} = +\text{OI}_i \times M \times \Gamma_i \times S$$
   $$\text{GEX}_i^{\text{put}} = -\text{OI}_i \times M \times \Gamma_i \times S$$

2. **Total Aggregate Spot GEX**:
   $$\text{GEX}_{\text{spot}} = \sum_{i \in \text{Calls}} \text{OI}_i M \Gamma_i S - \sum_{j \in \text{Puts}} \text{OI}_j M \Gamma_j S$$

3. **Dollar Gamma Exposure ($\text{Dollar GEX}$)**:
   Dollar GEX measures the dollar amount of underlying stock dealers must trade for a $1\%$ ($0.01$) move in spot price:
   $$\text{Dollar GEX} = \text{GEX}_{\text{spot}} \times \frac{S}{100} = \sum_i (\pm \text{OI}_i M \Gamma_i) \times \frac{S^2}{100}$$

### 2. Market Regimes: Long Gamma vs Short Gamma

The net sign of aggregate GEX establishes two fundamentally distinct market regimes:

```
+---------------------------------------------------------------------------------+
|                                 LONG GAMMA REGIME                               |
|                  Spot Price > Zero Gamma Flip Point (Net GEX > 0)               |
|                                                                                 |
|   Spot Rallies (+Delta)  ---> Dealers SELL Stock (Hedging) ---> Market Dampened |
|   Spot Declines (-Delta) ---> Dealers BUY Stock (Hedging)  ---> Market Supported|
|                                                                                 |
|                  Result: Volatility Suppression, Mean Reversion                 |
+---------------------------------------------------------------------------------+
                                         |
                               [ Zero Gamma Threshold ]
                                         |
+---------------------------------------------------------------------------------+
|                                SHORT GAMMA REGIME                               |
|                  Spot Price < Zero Gamma Flip Point (Net GEX < 0)               |
|                                                                                 |
|   Spot Declines (+Short) ---> Dealers SELL Stock (Hedging) ---> Market Plunges  |
|   Spot Rallies (-Short)  ---> Dealers BUY Stock (Hedging)  ---> Market Squeezes |
|                                                                                 |
|                  Result: Volatility Acceleration, Momentum Cascades             |
+---------------------------------------------------------------------------------+
```

1. **Positive Gamma Regime ($\text{GEX} > 0$)**:
   - Dealers hold net positive gamma.
   - When the market rises, dealer delta increases ($\Delta_{\text{portfolio}} > 0$).
   - To return to delta-neutral, dealers must **sell** underlying stock.
   - When the market drops, dealer delta decreases ($\Delta_{\text{portfolio}} < 0$).
   - To restore neutrality, dealers must **buy** underlying stock.
   - Economic outcome: Dealers act as systemic liquidity providers.
   - Realized volatility is compressed below implied volatility, and intraday price action exhibits strong mean reversion.

2. **Negative Gamma Regime ($\text{GEX} < 0$)**:
   - Dealers hold net negative gamma (short put gamma dominates).
   - When the market declines, the short puts gain delta, so the dealer book turns increasingly long delta.
   - To prevent runaway directional losses, dealers must **sell** stock into a falling market.
   - When the market rebounds, dealers must aggressively **buy** stock into the rally.
   - Economic outcome: Dealer hedging becomes pro-cyclical, draining market depth, triggering liquidity cascades, and amplifying realized volatility.

### 3. The Zero Gamma Flip Point

The **Zero Gamma Flip Point** (also known as the Volatility Trigger) is the underlying spot price $S^*$ where aggregate dealer gamma equals zero:

$$\text{GEX}_{\text{total}}(S^*) = \sum_{i \in \text{Calls}} \text{OI}_i M \Gamma_i(S^*) S^* - \sum_{j \in \text{Puts}} \text{OI}_j M \Gamma_j(S^*) S^* = 0$$

- When spot trades comfortably above $S^*$, the market resides in a low-volatility buffer zone.
- When spot breaks below $S^*$, the market transitions into the high-volatility regime.
- Quantitative desks monitor this level as a primary regime-shift indicator for adjusting stop-loss widths, position sizing, and intraday execution strategies.

### 4. Second-Order Flow Dynamics: Vanna and Charm

While gamma hedging responds strictly to changes in spot price ($\Delta S$), second-order Greek exposures trigger massive mechanical rebalancing from changes in volatility ($\Delta \sigma$) and time ($\Delta t$):

1. **Vanna Flows ($\frac{\partial \Delta}{\partial \sigma}$)**:
   - Recall that for an out-of-the-money put ($K < S$, $d_2 > 0$), Vanna $= -e^{-q T} \phi(d_1) d_2 / \sigma$ is negative.
   - When a market sells off, implied volatility surges ($\Delta \sigma > 0$).
   - With negative Vanna, higher IV pushes put deltas further toward $-1.0$, so dealers short those puts must sell more stock.
   - Conversely, when the market stabilizes or rallies, implied volatility drops sharply ($\Delta \sigma < 0$).
   - This volatility collapse causes put deltas to shrink toward zero.
   - Because dealers were short those puts and short stock as a hedge, the vanishing put delta forces dealers to aggressively **buy back their short stock hedges**.
   - This mechanical short-covering feedback loop is known as the **Vanna Rally**.

2. **Charm Flows ($\frac{\partial \Delta}{\partial t}$)**:
   - Charm measures the rate of delta decay over time.
   - As options approach expiration Friday, out-of-the-money option deltas rapidly decay toward zero.
   - Dealers holding stock hedges against OTM options must progressively unwind their cash hedges before expiration.
   - If dealers are short OTM puts, time decay causes put delta to bleed to zero, requiring dealers to buy back stock hedges into the Friday close.
   - These flows generate predictable Market-on-Close (MOC) order imbalances during quarterly triple and quadruple witching dates.

### 5. Strike Pinning Mechanics

On options expiration days, the underlying asset frequently converges toward and "pins" to a major open interest strike price:
- Suppose a massive concentration of open interest resides at strike $K_{\text{pin}}$ and dealers are net **long** gamma there (for example, customers overwrite calls or sell straddles at that strike).
- Gamma at a single strike is identical for its calls and puts, and it peaks near $K_{\text{pin}}$ as expiry approaches.
- If spot drifts slightly above $K_{\text{pin}}$, the long-gamma dealer book gains delta, so dealers sell stock and push spot back down toward $K_{\text{pin}}$.
- If spot drifts slightly below $K_{\text{pin}}$, the book loses delta, so dealers buy stock and lift spot back up toward $K_{\text{pin}}$.
- This bilateral feedback loop traps the spot price in a tight band around the strike until the final minutes of trading.
- The direction depends on the sign of dealer gamma: if dealers are net **short** gamma at the strike (for example, short the puts customers bought), they buy above and sell below the strike, which pushes spot away from it and amplifies the move instead of pinning it.

---

## Worked examples

### Example 1: Aggregate Dollar GEX and Regime Identification

A quantitative analyst evaluates the S&P 500 options chain expiring in 14 days ($T = 14 / 365 = 0.03836$ years).
- Current Spot Price: $S = \$5,000.00$.
- Volatility: $\sigma = 16\%$ ($0.16$).
- Multiplier: $M = 100$.
- The analyst aggregates open interest across two dominant strikes:
  1. **Strike 5050 Call**: $\text{OI} = 50,000\text{ contracts}$.
  2. **Strike 4950 Put**: $\text{OI} = 70,000\text{ contracts}$.
- Rates and dividends are set to zero, so $\Gamma = \phi(d_1) / (S \sigma \sqrt{T})$ with $\sqrt{T} = 0.19585$, $\sigma \sqrt{T} = 0.031336$ and $S \sigma \sqrt{T} = 156.68$.
  1. **5050 Call**: $d_1 = \frac{\ln(5000/5050) + 0.5(0.16)^2(0.03836)}{0.031336} = \frac{-0.009950 + 0.000491}{0.031336} = -0.3019$, $\phi(d_1) = 0.38117$, so $\Gamma_{5050} = 0.38117 / 156.68 = 0.002433$.
  2. **4950 Put**: $d_1 = \frac{\ln(5000/4950) + 0.000491}{0.031336} = \frac{0.010050 + 0.000491}{0.031336} = +0.3364$, $\phi(d_1) = 0.37700$, so $\Gamma_{4950} = 0.37700 / 156.68 = 0.002406$.

1. **Compute Call Gamma Exposure**:
   $$\text{Call GEX} = +50,000 \times 100 \times 0.002433 \times 5000 = +\$60,825,000\text{ per 1 point spot move}$$

2. **Compute Put Gamma Exposure (Dealers Short Puts)**:
   $$\text{Put GEX} = -70,000 \times 100 \times 0.002406 \times 5000 = -\$84,210,000\text{ per 1 point spot move}$$

3. **Calculate Net Spot GEX**:
   $$\text{Net GEX} = +\$60,825,000 - \$84,210,000 = -\$23,385,000\text{ per point}$$

4. **Calculate Dollar GEX per 1% Move**:
   $$\text{Dollar GEX} = \text{Net GEX} \times \frac{S}{100} = -\$23,385,000 \times 50 = -\$1,169,250,000$$

5. **Regime Diagnosis**:
   - The market is in a **Short Gamma Regime** ($\text{Dollar GEX} = -\$1,169.25\text{M}$).
   - For every $1\%$ drop in the index, options dealers are forced to sell approximately $\$1.17\text{B}$ of S&P 500 futures and equities to maintain delta neutrality, accelerating downside momentum.

### Example 2: Quantifying Vanna Hedging Flow on Volatility Drop

Following a major CPI print, the S&P 500 rallies, and the VIX drops by $3.0$ volatility points ($\Delta \sigma = -0.03$).
A market making desk is short $100,000$ contracts of 4800 strike OTM puts ($100,000 \times 100 = 10,000,000$ index units).
- Current Spot: $S = \$5,000.00$.
- Strike: $K = \$4,800.00$.
- Time to Expiry: $T = 30 / 365 = 0.08219$ years ($\sqrt{T} = 0.28669$).
- Implied Volatility Before the Print: $\sigma = 20\%$ ($0.20$); rates and dividends are set to zero.
- Contract Multiplier: $100$.

1. **Compute the Put Delta and Vanna Before the Print**:
   $$d_1 = \frac{\ln(5000/4800) + 0.5(0.20)^2(0.08219)}{0.20 \times 0.28669} = \frac{0.040822 + 0.001644}{0.057338} = 0.7406$$
   $$d_2 = 0.7406 - 0.0573 = 0.6833$$
   $$\Delta_{\text{put}} = N(d_1) - 1 = 0.7705 - 1 = -0.2295$$
   $$\text{Vanna} = -\phi(d_1) \frac{d_2}{\sigma} = -0.30325 \times \frac{0.6833}{0.20} = -1.0361\text{ per 1.00 of volatility}$$
   Vanna is negative because $d_2 > 0$ for this OTM put.

2. **Compute the Delta Change per Option**:
   $$\Delta (\text{Delta}) \approx \text{Vanna} \times \Delta \sigma = -1.0361 \times (-0.03) = +0.03108$$
   The put delta rises from $-0.2295$ toward zero, to about $-0.1984$.

3. **Compute the Dealer Hedge Trade**:
   The short put book has position delta $-10,000,000 \times (-0.2295) = +2,295,000$, hedged with $2,295,000$ shares of short index exposure.
   After the volatility drop, the position delta changes by $-10,000,000 \times 0.03108 = -310,800$.
   To stay neutral, the desk buys back $310,800$ units of its short hedge.

4. **Compute Total Dollar Inflow**:
   $$\text{Dollar Flow} = 310,800 \times \$5,000.00 = +\$1,554,000,000$$
   The $3.0$ point drop in implied volatility forces about $\$1.55\text{B}$ of systematic buying, the mechanism behind a Vanna rally.
   Full Black-Scholes revaluation at $\sigma = 17\%$ gives $d_1 = 0.8620$ and $\Delta_{\text{put}} = -0.1944$, a change of $+0.0351$ and a flow of $351,000 \times \$5,000 = \$1.755\text{B}$.
   The linear Vanna estimate understates the flow because Vanna itself grows in magnitude as volatility falls (it is $-1.3162$ at $\sigma = 17\%$).

---

## Pitfalls

- **Assuming Open Interest Equals Dealer Positioning**:
  Open interest data reports gross outstanding contracts but does not reveal whether trades were customer buys or sells.
  Treating all puts as customer buys and all calls as customer sells is a heuristic; during retail meme-stock manias, retail traders aggressively buy OTM calls, flipping dealer call gamma to short.
- **Ignoring Non-Cleared OTC and Institutional Swaps**:
  Public exchange open interest excludes over-the-counter (OTC) structured products, total return swaps, and dispersion books.
  In single stocks and non-US indices, OTC dealer positions can completely overwhelm listed exchange GEX signals.
- **Static GEX Fallacy in Rapidly Moving Markets**:
  GEX is not a static constant; option gamma shifts dynamically as spot moves, volatility changes, and time passes.
  Calculating GEX once at the market open and assuming it holds during an intraday $3\%$ selloff leads to catastrophic risk miscalculations.
- **Netting Index GEX Against Single-Stock Options**:
  Market makers frequently delta-hedge index options using single-stock equities rather than index futures.
  Failing to account for single-stock dispersion and cross-asset hedging flows produces incomplete liquidity projections.

---

## Interview questions

> [!question]- mkt-opt-065 | What is Gamma Exposure (GEX)?
> An aggregate metric estimating the dollar value of underlying stock options dealers must buy or sell per 1% move in spot price to maintain delta neutrality.
> It quantifies the structural feedback loop between derivatives hedging and underlying market liquidity.

> [!question]- mkt-opt-066 | What structural assumption is made regarding institutional options positioning when calculating GEX?
> That market participants are net buyers of protective puts (dealers are short puts) and net sellers of covered calls (dealers are long calls).
> This maps positive gamma to calls and negative gamma to puts in aggregate formulas.

> [!question]- mkt-opt-067 | How do dealers behave in a positive gamma regime when the underlying price drops?
> Dealers buy underlying shares as price falls because their long-gamma book loses delta on the way down.
> This programmatic buying provides liquidity and dampens downside price momentum.

> [!question]- mkt-opt-068 | How do dealers behave in a negative gamma regime when the underlying price drops?
> Dealers sell underlying shares into the decline to hedge rapidly expanding short put deltas.
> This programmatic selling drains liquidity and accelerates market declines.

> [!question]- mkt-opt-069 | Define the zero-gamma flip point.
> The critical underlying spot price where aggregate dealer gamma across all strikes equals zero: sum GEX = 0.
> It marks the boundary separating volatility suppression regimes from volatility acceleration regimes.

> [!question]- mkt-opt-070 | Why does realized volatility tend to fall below implied volatility when spot trades far above the zero gamma level?
> In deep positive gamma territory, continuous dealer rebalancing (buying dips and selling rips) suppresses realized intraday price dispersion.
> Options implied volatility decays as actual market moves remain tightly constrained.

> [!question]- mkt-opt-071 | What is Vanna in the context of dealer flow modeling?
> The cross derivative dDelta / dsigma measuring how option delta responds to changes in implied volatility.
> It dictates how much underlying stock dealers must rebalance when volatility expands or collapses.

> [!question]- mkt-opt-072 | Explain the mechanics of a Vanna rally.
> When the market stabilizes and implied volatility drops, short put delta shrinks toward zero.
> Options dealers who were short stock as a hedge must buy back massive volumes of shares, fueling a mechanical market rally.

> [!question]- mkt-opt-073 | What is Charm in the context of dealer flow modeling?
> The rate of change of option delta with respect to the passage of time: -dDelta / dT.
> It quantifies the natural delta decay of options as expiration approaches.

> [!question]- mkt-opt-074 | How do Charm flows influence market-on-close (MOC) trading into expiration Friday?
> As out-of-the-money options bleed delta toward zero into expiration, dealers systematically unwind their cash hedges.
> If dealers are short OTM puts, Charm forces mechanical buying of underlying stock into Friday afternoon.

> [!question]- mkt-opt-075 | What is strike pinning on options expiration day?
> The empirical tendency for an underlying asset price to close exactly at a strike with massive open interest.
> When dealers are net long gamma at that strike, their hedging sells above and buys below it, pulling spot back toward the strike whenever it drifts away.

> [!question]- mkt-opt-076 | What is the Call Wall in market maker positioning?
> The specific strike price with the single highest concentration of net positive call gamma exposure.
> It acts as a formidable structural resistance level because dealer selling intensifies as spot approaches the strike.

> [!question]- mkt-opt-077 | What is the Put Wall in market maker positioning?
> The specific strike price with the single highest concentration of net put open interest and negative gamma exposure.
> It serves as a major structural support level or, if breached, the trigger for violent liquidity cascades.

> [!question]- mkt-opt-078 | Why does a breach of the Put Wall often lead to a rapid market selloff?
> Below the Put Wall, deep OTM puts flip to at-the-money, causing dealer negative gamma to peak.
> Dealers must dump enormous quantities of underlying stock into thin market depth to maintain delta neutrality.

> [!question]- mkt-opt-079 | What is the Volatility Trigger in GEX terminology?
> An alternative term for the zero-gamma flip point.
> It indicates the inflection price below which market volatility is expected to trigger an expansion.

> [!question]- mkt-opt-080 | How does high short interest interact with short dealer gamma?
> If a heavily shorted stock triggers a short squeeze while dealers are short call gamma, dealers must aggressively buy shares alongside short sellers.
> This dual buying force creates parabolic "gamma squeeze" upside explosions.

> [!question]- mkt-opt-081 | Why did retail options buying in 2021 invalidate standard institutional GEX assumptions?
> Retail traders aggressively purchased out-of-the-money call options, forcing market makers into massive short call gamma positions.
> Instead of dampening rallies, dealer hedging amplified upside moves into extreme parabolic spikes.

> [!question]- mkt-opt-082 | What happens to aggregate GEX immediately following a monthly options expiration (OpEx)?
> Expiring options contracts are extinguished, removing their associated gamma from the market.
> Aggregate GEX drops sharply, "un-pinning" the underlying asset and frequently initiating large directional trend moves.

> [!question]- mkt-opt-083 | What is OpEx week seasonality and why does it occur?
> The tendency for equity markets to exhibit compressed volatility during the days leading up to monthly OpEx.
> Large concentrations of near-dated gamma force market makers into active volatility-dampening hedging.

> [!question]- mkt-opt-084 | What is the difference between spot GEX and dollar GEX?
> Spot GEX measures shares to buy/sell per 1-point move in the underlying asset: sum OI * M * Gamma * S.
> Dollar GEX measures the total dollar value of stock to trade per 1% move: Spot GEX * S / 100.

> [!question]- mkt-opt-085 | How does high interest rate environment impact dealer Rho and forward hedging?
> Higher interest rates increase forward prices (F = S * exp((r - q)*T)), shifting ATM strikes higher.
> Dealers must adjust forward cash financing costs and early exercise boundaries on dividend-paying stocks.

> [!question]- mkt-opt-086 | How does zero-days-to-expiration (0DTE) option volume alter dealer intraday GEX?
> 0DTE options possess astronomical Gamma that appears and vanishes within a single trading day.
> Dealers face hyper-concentrated intraday hedging requirements that can trigger sharp intra-day mean reversions or sudden momentum runs.

> [!question]- mkt-opt-087 | Why are 0DTE options effective instruments for manufactured intraday gamma squeezes?
> Because near-expiry options have tiny premiums, retail or algorithmic traders can purchase enormous contract quantities with minimal capital.
> The astronomical gamma forces dealers to buy massive share volumes immediately upon slight price increases.

> [!question]- mkt-opt-088 | What is the primary data limitation when estimating dealer positioning from FINRA/CBOE open interest?
> Open interest is published only once per day (overnight) and reflects settled trades from the prior session.
> It cannot capture massive intraday positioning shifts, opening versus closing trades, or OTC cross-hedges.

> [!question]- mkt-opt-089 | Explain the term "volatility suppression" under large positive GEX.
> The structural dampening of market swings caused by dealers selling into strength and buying into weakness.
> Price distribution becomes leptokurtic with truncated standard deviations.

> [!question]- mkt-opt-090 | What is speed risk for a dealer hedging a book with high gamma concentration?
> Speed is the third derivative dGamma / dS.
> High speed means dealer gamma shifts violently during a market gap, causing delta hedges to rapidly become outdated.

> [!question]- mkt-opt-091 | How does an inverted VIX term structure affect dealer risk appetite?
> Backwardation signals severe immediate market stress and elevated gap risk.
> Dealers widen bid-ask spreads, reduce quoted size, and aggressively derisk inventory, further thinning market liquidity.

> [!question]- mkt-opt-092 | What is shadow gamma in exotic options books?
> Gamma exposure originating from barrier options, autocallables, and structured notes that is not visible in listed exchange open interest.
> When spot crosses an autocall barrier, dealer gamma can vanish instantaneously, causing abrupt market air pockets.

> [!question]- mkt-opt-093 | How do dealers hedge when trading index options against single-stock constituents?
> Dealers trade index options (e.g., SPX) and hedge by buying or selling the 500 underlying component stocks according to their index weights.
> This links single-stock intraday liquidity directly to index options dealer positioning.

> [!question]- mkt-opt-094 | What is the role of market-on-close (MOC) imbalance orders in dealer delta reconciliation?
> Market makers face overnight jump risk and frequently use MOC orders to flatten delta imbalances at guaranteed official closing prices.
> Massive MOC imbalances often reflect late-day Greek unwinds.

> [!question]- mkt-opt-095 | Why does low market depth exacerbate negative gamma cascades?
> In a thin limit order book, dealer market orders consume multiple price levels, causing large market impact.
> The resulting price drop triggers additional short put gamma, creating an endogenous feedback loop.

> [!question]- mkt-opt-096 | How should a quantitative trader adapt trading style when transitioning from positive to negative GEX?
> In positive GEX, favor mean-reversion, range-bound strategies, tight profit targets, and selling premium.
> In negative GEX, favor momentum, breakout strategies, wider stop losses, and purchasing volatility protection.

---

## Further reading

- Breeden, D. T., & Litzenberger, R. H. (1978). *Prices of state-contingent claims implicit in option prices*. Journal of Business, 51(4), 621-651.
- Garleanu, N., Pedersen, L. H., & Poteshman, A. M. (2009). *Demand-based option pricing*. The Review of Financial Studies, 22(10), 4259-4299.
- SqueezeMetrics. (2019). *The implied order book: How derivatives dictate cash market liquidity*. White Paper.
- SpotGamma. (2021). *Gamma Exposure (GEX) and equity market volatility dynamics*. Institutional Research Series.
- Kolanovic, M. (2020). *Market microstructure, systematic flows, and options market maker hedging*. J.P. Morgan Quantitative and Derivatives Strategy.
