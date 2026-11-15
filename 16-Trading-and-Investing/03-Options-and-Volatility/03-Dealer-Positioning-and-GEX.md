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

Options market makers mostly aim to run delta-neutral books rather than directional bets, hedging in the underlying cash and futures markets.
When their aggregate gamma is large, the rebalancing that hedging requires can be a material source of order flow in the underlying.
Gamma Exposure (GEX), the zero-gamma flip point, and Vanna and Charm flows are models of that hedging flow.
Every one of them rests on an assumption about who is long and who is short the listed open interest, because public data does not say; this note states that assumption explicitly and treats the outputs as estimates, not observations.

---

## TL;DR

Gamma Exposure (GEX) estimates the dollar value of the underlying that options dealers would have to buy or sell for every $1\%$ move in the underlying, under an assumed dealer position.
Under the usual convention (dealers long the calls and short the puts in open interest), a positive estimate means hedging is counter-cyclical: dealers buy dips and sell rallies, which can damp moves.
A negative estimate, which under the convention tends to occur when spot is below the "zero gamma flip point", means hedging is pro-cyclical: dealers sell into declines and buy into rallies, which can amplify moves.
Vanna (delta changes from volatility moves) and Charm (delta changes from the passage of time) add hedging flow even when spot is unchanged; their size depends on the same positioning assumption.

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

Public open interest (OI) reports how many contracts are outstanding, not which side dealers hold, so every GEX estimate starts from an assumption.
The common convention, used throughout this note, is:
- **Assumption: customers are net buyers of puts** (portfolio insurance), so dealers are **short puts**.
- **Assumption: customers are net sellers of calls** (covered calls and overwriting), so dealers are **long calls**.
Both are assumptions, not facts; Garleanu, Pedersen and Poteshman (2009), using signed CBOE volume data, find that end users are net long S&P 500 index options on average, with large net long positions in out-of-the-money puts, which supports the put half of the convention but says nothing that guarantees dealers are long calls.
Change the assumption and the sign and size of every number below change with it.

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
   - The hypothesis is that realized volatility is damped and intraday moves mean-revert more; treat it as a hypothesis to test on your own data, not an established fact.

2. **Negative Gamma Regime ($\text{GEX} < 0$)**:
   - Dealers hold net negative gamma (short put gamma dominates).
   - When the market declines, the short puts gain delta, so the dealer book turns increasingly long delta.
   - To prevent runaway directional losses, dealers must **sell** stock into a falling market.
   - When the market rebounds, dealers must aggressively **buy** stock into the rally.
   - Economic outcome: Dealer hedging becomes pro-cyclical, which can drain market depth and amplify realized volatility when the hedging flow is large relative to available liquidity.

### 3. The Zero Gamma Flip Point

The **Zero Gamma Flip Point** is the spot price $S^*$ at which the estimated aggregate dealer gamma, recomputed at that spot with open interest, volatility and time held fixed, equals zero:

$$\text{GEX}_{\text{total}}(S^*) = \sum_{i \in \text{Calls}} \text{OI}_i M \Gamma_i(S^*) S^* - \sum_{j \in \text{Puts}} \text{OI}_j M \Gamma_j(S^*) S^* = 0$$

- Above $S^*$ the convention implies dealers are net long gamma; below it, net short gamma.
- Whether realized volatility actually differs across $S^*$ is an empirical question; some traders use the level as one input to stop widths and position sizing, and it should be backtested before being relied on.
- The level moves whenever open interest, implied volatility or time to expiry change, so it must be recomputed, not read once.

### 4. Second-Order Flow Dynamics: Vanna and Charm

While gamma hedging responds to changes in spot price ($\Delta S$), Vanna and Charm require rebalancing when volatility ($\Delta \sigma$) or time ($\Delta t$) change even with spot unchanged:

1. **Vanna Flows ($\frac{\partial \Delta}{\partial \sigma}$)**:
   - Recall that for an out-of-the-money put ($K < S$, $d_2 > 0$), Vanna $= -e^{-q T} \phi(d_1) d_2 / \sigma$ is negative.
   - When a market sells off, implied volatility surges ($\Delta \sigma > 0$).
   - With negative Vanna, higher IV pushes put deltas further toward $-1.0$, so dealers short those puts must sell more stock.
   - Conversely, when the market stabilizes or rallies, implied volatility drops sharply ($\Delta \sigma < 0$).
   - This volatility collapse causes put deltas to shrink toward zero.
   - Because dealers were short those puts and short stock as a hedge, the shrinking put delta requires dealers to **buy back part of their short hedges**.
   - Traders call the resulting buying, when it is large, a **Vanna Rally**; Example 2 sizes it for a hypothetical book.

2. **Charm Flows ($\frac{\partial \Delta}{\partial t}$)**:
   - Charm measures the rate of delta decay over time.
   - As options approach expiration Friday, out-of-the-money option deltas rapidly decay toward zero.
   - Dealers holding stock hedges against OTM options must progressively unwind their cash hedges before expiration.
   - If dealers are short OTM puts, time decay causes put delta to bleed to zero, requiring dealers to buy back stock hedges into the Friday close.
   - When and how dealers execute that adjustment (continuously, or with closing-auction orders) is their choice, so the timing of charm flow is not mechanical.

### 5. Strike Pinning Mechanics

On options expiration days, the underlying can converge toward and "pin" to a strike with large open interest; the mechanism is:
- Suppose a massive concentration of open interest resides at strike $K_{\text{pin}}$ and dealers are net **long** gamma there (for example, customers overwrite calls or sell straddles at that strike).
- Gamma at a single strike is identical for its calls and puts, and it peaks near $K_{\text{pin}}$ as expiry approaches.
- If spot drifts slightly above $K_{\text{pin}}$, the long-gamma dealer book gains delta, so dealers sell stock and push spot back down toward $K_{\text{pin}}$.
- If spot drifts slightly below $K_{\text{pin}}$, the book loses delta, so dealers buy stock and lift spot back up toward $K_{\text{pin}}$.
- This bilateral feedback loop traps the spot price in a tight band around the strike until the final minutes of trading.
- The direction depends on the sign of dealer gamma: if dealers are net **short** gamma at the strike (for example, short the puts customers bought), they buy above and sell below the strike, which pushes spot away from it and amplifies the move instead of pinning it.

---

## Worked examples

### Example 1: Aggregate Dollar GEX and Regime Identification

An analyst evaluates a hypothetical index options chain expiring in 14 days ($T = 14 / 365 = 0.03836$ years), under the convention that dealers are long the calls and short the puts.
- Current Spot Price: $S = \$5,000.00$.
- Volatility: $\sigma = 16\%$ ($0.16$).
- Multiplier: $M = 100$.
- The analyst aggregates open interest across two dominant strikes:
  1. **Strike 5050 Call**: $\text{OI} = 50,000\text{ contracts}$.
  2. **Strike 4950 Put**: $\text{OI} = 70,000\text{ contracts}$.
- Rates and dividends are set to zero, so $\Gamma = \phi(d_1) / (S \sigma \sqrt{T})$ with $\sqrt{T} = 0.19585$, $\sigma \sqrt{T} = 0.031336$ and $S \sigma \sqrt{T} = 156.68$.
  1. **5050 Call**: $d_1 = \frac{\ln(5000/5050) + 0.5(0.16)^2(0.03836)}{0.031336} = \frac{-0.009950 + 0.000491}{0.031336} = -0.3019$, $\phi(d_1) = 0.38117$, so $\Gamma_{5050} = 0.38117 / 156.68 = 0.002433$.
  2. **4950 Put**: $d_1 = \frac{\ln(5000/4950) + 0.000491}{0.031336} = \frac{0.010050 + 0.000491}{0.031336} = +0.3364$, $\phi(d_1) = 0.37700$, so $\Gamma_{4950} = 0.37700 / 156.68 = 0.002406$.

The products below use the unrounded gammas ($0.0024328$ and $0.0024062$), which is why they differ slightly from products of the four-significant-figure values.

1. **Compute Call Gamma Exposure**:
   $$\text{Call GEX} = +50,000 \times 100 \times 0.0024328 \times 5000 = +\$60.82\text{M of delta per 1 point spot move}$$

2. **Compute Put Gamma Exposure (Dealers Assumed Short Puts)**:
   $$\text{Put GEX} = -70,000 \times 100 \times 0.0024062 \times 5000 = -\$84.22\text{M per 1 point spot move}$$

3. **Calculate Net Spot GEX**:
   $$\text{Net GEX} = +\$60.82\text{M} - \$84.22\text{M} = -\$23.40\text{M per point}$$

4. **Calculate Dollar GEX per 1% Move**:
   $$\text{Dollar GEX} = \text{Net GEX} \times \frac{S}{100} = -\$23.395\text{M} \times 50 = -\$1,169.8\text{M}$$
   As an independent check, repricing every option's delta at spot $\pm 0.5\%$ gives a hedge trade of $\$1.167\text{B}$ for a $1\%$ move, within $0.3\%$ of the gamma estimate (the gap is the change in gamma across the move).

5. **Regime Diagnosis**:
   - Under the convention, this book is **short gamma** ($\text{Dollar GEX} \approx -\$1.17\text{B}$).
   - For every $1\%$ drop in the index, dealers positioned this way would need to sell about $\$1.17\text{B}$ of index exposure to stay delta neutral, and buy about as much in a $1\%$ rally.
   - Recomputing the book's gamma at other spot levels (open interest, volatility and expiry held fixed) puts the zero-gamma flip point at about $5,081$: above it the call strike's gamma dominates and the book turns long gamma.

### Example 2: Quantifying Vanna Hedging Flow on Volatility Drop

Suppose a macro release lifts the index and the 4800 put's implied volatility falls by $3.0$ points ($\Delta \sigma = -0.03$); all inputs are hypothetical.
A market making desk is short $100,000$ contracts of 4800 strike OTM puts ($100,000 \times 100 = 10,000,000$ index units).
- Current Spot: $S = \$5,000.00$ (held fixed to isolate the vanna effect).
- Strike: $K = \$4,800.00$.
- Time to Expiry: $T = 30 / 365 = 0.08219$ years ($\sqrt{T} = 0.28669$).
- Implied Volatility Before the Release: $\sigma = 20\%$ ($0.20$); rates and dividends are set to zero.
- Contract Multiplier: $100$.

1. **Compute the Put Delta and Vanna Before the Release**:
   $$d_1 = \frac{\ln(5000/4800) + 0.5(0.20)^2(0.08219)}{0.20 \times 0.28669} = \frac{0.040822 + 0.001644}{0.057338} = 0.7406$$
   $$d_2 = 0.7406 - 0.0573 = 0.6833$$
   $$\Delta_{\text{put}} = N(d_1) - 1 = 0.7705 - 1 = -0.2295$$
   $$\text{Vanna} = -\phi(d_1) \frac{d_2}{\sigma} = -0.30325 \times \frac{0.6833}{0.20} = -1.0360\text{ per 1.00 of volatility}$$
   Vanna is negative because $d_2 > 0$ for this OTM put.

2. **Compute the Delta Change per Option**:
   $$\Delta (\text{Delta}) \approx \text{Vanna} \times \Delta \sigma = -1.0360 \times (-0.03) = +0.03108$$
   The put delta rises from $-0.2295$ toward zero, to about $-0.1984$.

3. **Compute the Dealer Hedge Trade**:
   The short put book has position delta $-10,000,000 \times (-0.22946) = +2,294,600$ units, hedged with the same amount of short index exposure.
   After the volatility drop, the position delta changes by $-10,000,000 \times 0.031081 = -310,800$ units.
   To stay neutral, the desk buys back about $310,800$ units of its short hedge.

4. **Compute Total Dollar Inflow**:
   $$\text{Dollar Flow} = 310,808 \times \$5,000.00 = +\$1.554\text{B}$$
   The $3.0$ point drop in implied volatility requires about $\$1.55\text{B}$ of buying from this one hypothetical book, the mechanism traders call a Vanna rally.
   Full Black-Scholes revaluation at $\sigma = 17\%$ gives $d_1 = 0.8620$ and $\Delta_{\text{put}} = -0.1944$, a change of $+0.0351$, about $351,100$ units, and a flow of $\$1.755\text{B}$.
   The linear Vanna estimate understates the flow because Vanna itself grows in magnitude as volatility falls (it is $-1.3162$ at $\sigma = 17\%$).

---

## Pitfalls

- **Assuming Open Interest Equals Dealer Positioning**:
  Open interest data reports gross outstanding contracts but does not reveal whether trades were customer buys or sells.
  Treating all puts as customer buys and all calls as customer sells is a heuristic; where customers are heavy net buyers of OTM calls, dealers are short those calls and the convention gets the call sign wrong.
- **Ignoring Non-Cleared OTC and Institutional Swaps**:
  Public exchange open interest excludes over-the-counter (OTC) structured products, total return swaps, and dispersion books.
  Where OTC books are large relative to listed open interest, they can dominate the true dealer gamma, and a listed-only GEX estimate can have the wrong sign.
- **Static GEX Fallacy in Rapidly Moving Markets**:
  GEX is not a static constant; option gamma shifts dynamically as spot moves, volatility changes, and time passes.
  Calculating GEX once at the market open and assuming it holds through a large intraday move misstates the hedging flow; recompute it at the new spot, as the flip-point calculation in Example 1 does.
- **Netting Index GEX Against Single-Stock Options**:
  Index option hedges can be executed in futures, ETFs or baskets of constituents, and single-stock option books are hedged in the stocks themselves.
  Adding index and single-stock GEX into one number ignores where each hedge actually trades, so keep them separate.

---

## Interview questions

> [!question]- mkt-opt-065 | What is Gamma Exposure (GEX)?
> An aggregate metric estimating the dollar value of underlying stock options dealers must buy or sell per 1% move in spot price to maintain delta neutrality.
> It quantifies the structural feedback loop between derivatives hedging and underlying market liquidity.

> [!question]- mkt-opt-066 | What structural assumption is made regarding institutional options positioning when calculating GEX?
> The usual convention assumes customers are net buyers of puts (dealers short puts) and net sellers of calls (dealers long calls).
> It maps positive gamma to calls and negative gamma to puts; it is an assumption, because open interest does not reveal which side dealers hold.

> [!question]- mkt-opt-067 | How do dealers behave in a positive gamma regime when the underlying price drops?
> Dealers buy underlying shares as price falls because their long-gamma book loses delta on the way down.
> Under the convention this hedging buys into declines, which can damp downside moves when it is large relative to market depth.

> [!question]- mkt-opt-068 | How do dealers behave in a negative gamma regime when the underlying price drops?
> Dealers sell underlying shares into the decline to hedge rapidly expanding short put deltas.
> That hedging sells into declines, which can amplify them when it is large relative to market depth.

> [!question]- mkt-opt-069 | Define the zero-gamma flip point.
> The critical underlying spot price where aggregate dealer gamma across all strikes equals zero: sum GEX = 0.
> Under the positioning convention it separates the region where dealers are estimated net long gamma from the region where they are estimated net short; it moves as open interest, volatility and time change.

> [!question]- mkt-opt-070 | Why does realized volatility tend to fall below implied volatility when spot trades far above the zero gamma level?
> The hypothesis is that dealers who are long gamma buy dips and sell rallies, damping realized moves, and implied volatility then drifts down toward the lower realized volatility.
> It is a hypothesis about flows estimated under a positioning assumption, so test it on data before trading it.

> [!question]- mkt-opt-071 | What is Vanna in the context of dealer flow modeling?
> The cross derivative dDelta / dsigma measuring how option delta responds to changes in implied volatility.
> It dictates how much underlying stock dealers must rebalance when volatility expands or collapses.

> [!question]- mkt-opt-072 | Explain the mechanics of a Vanna rally.
> When the market stabilizes and implied volatility drops, short put delta shrinks toward zero.
> Dealers who were short the underlying as a hedge must buy part of it back; Example 2 sizes this at about $1.55B for one hypothetical book and a 3-point volatility drop.

> [!question]- mkt-opt-073 | What is Charm in the context of dealer flow modeling?
> The rate of change of option delta with respect to the passage of time: -dDelta / dT.
> It quantifies the natural delta decay of options as expiration approaches.

> [!question]- mkt-opt-074 | How do Charm flows influence market-on-close (MOC) trading into expiration Friday?
> As out-of-the-money options bleed delta toward zero into expiration, dealers systematically unwind their cash hedges.
> If dealers are short OTM puts hedged with short stock, charm shrinks the hedge they need, so they buy some back as expiry approaches; when they execute it is their choice.

> [!question]- mkt-opt-075 | What is strike pinning on options expiration day?
> The tendency of an underlying to close at or near a strike with large open interest on expiration day.
> When dealers are net long gamma at that strike, their hedging sells above and buys below it, pulling spot back toward the strike whenever it drifts away.

> [!question]- mkt-opt-076 | What is the Call Wall in market maker positioning?
> Vendor and trader jargon for the strike with the largest estimated call gamma under the positioning convention.
> The claim is that long-gamma dealer hedging sells into rallies near it, so it acts as resistance; that is a hypothesis to test, not an established level.

> [!question]- mkt-opt-077 | What is the Put Wall in market maker positioning?
> Jargon for the strike with the largest estimated put gamma under the positioning convention.
> Traders treat it as support or, once breached, as a level where hedging is estimated to turn most pro-cyclical; both are hypotheses to test.

> [!question]- mkt-opt-078 | Why does a breach of the Put Wall often lead to a rapid market selloff?
> As spot falls to a large put strike those puts move to the money, where their gamma peaks, so a dealer short them is most short gamma there.
> Under the convention, further declines then require the most hedge selling per point, which can accelerate the move when depth is thin.

> [!question]- mkt-opt-079 | What is the Volatility Trigger in GEX terminology?
> A vendor label for an estimated regime-change level near the zero-gamma point; each vendor defines it with its own model, so it is not a standard quantity.
> Treat it as that vendor's estimate of where dealer hedging is assumed to turn pro-cyclical.

> [!question]- mkt-opt-080 | How does high short interest interact with short dealer gamma?
> If a heavily shorted stock triggers a short squeeze while dealers are short call gamma, dealers must aggressively buy shares alongside short sellers.
> The combined buying is what traders call a "gamma squeeze"; whether hedging flow was large enough to matter in a given episode is an empirical question.

> [!question]- mkt-opt-081 | Why did retail options buying in 2021 invalidate standard institutional GEX assumptions?
> Where customers are heavy net buyers of calls, dealers are short calls, the opposite of the "dealers long calls" convention, so a convention-based GEX has the wrong sign.
> Be careful with the folklore, though: the SEC staff report on early-2021 market conditions (October 14, 2021, section 3.4) found no evidence of a gamma squeeze in GameStop in January 2021, noting that market makers were buying rather than writing calls.

> [!question]- mkt-opt-082 | What happens to aggregate GEX immediately following a monthly options expiration (OpEx)?
> Expiring options contracts are extinguished, removing their associated gamma from the market.
> The expired gamma no longer needs hedging, so estimated GEX falls; the claim that this releases a pin and starts trends is a hypothesis, not an established regularity.

> [!question]- mkt-opt-083 | What is OpEx week seasonality and why does it occur?
> The claimed tendency for realized volatility to be lower in the days before monthly expiry and higher after it.
> The proposed mechanism is long dealer gamma in near-dated options; the effect is not established by this note's sources, so treat it as a hypothesis to test.

> [!question]- mkt-opt-084 | What is the difference between spot GEX and dollar GEX?
> Spot GEX measures shares to buy/sell per 1-point move in the underlying asset: sum OI * M * Gamma * S.
> Dollar GEX measures the total dollar value of stock to trade per 1% move: Spot GEX * S / 100.

> [!question]- mkt-opt-085 | How does high interest rate environment impact dealer Rho and forward hedging?
> Higher interest rates increase forward prices (F = S * exp((r - q)*T)), shifting ATM strikes higher.
> Dealers must adjust forward cash financing costs and early exercise boundaries on dividend-paying stocks.

> [!question]- mkt-opt-086 | How does zero-days-to-expiration (0DTE) option volume alter dealer intraday GEX?
> 0DTE options possess astronomical Gamma that appears and vanishes within a single trading day.
> The hedging they need is concentrated within the day, so it can damp or amplify intraday moves depending on the sign of dealer gamma, which open interest alone does not reveal.

> [!question]- mkt-opt-087 | Why are 0DTE options effective instruments for manufactured intraday gamma squeezes?
> Near-expiry options are cheap per contract but have very high gamma near the strike, so a dealer short them must buy quickly as spot rises toward the strike.
> Whether such buying is large enough to move an index is an empirical question; the mechanism is not proof that it does.

> [!question]- mkt-opt-088 | What is the primary data limitation when estimating dealer positioning from FINRA/CBOE open interest?
> US listed-options open interest is published by the Options Clearing Corporation (OCC, not FINRA) once per day and reflects positions after the prior session.
> It cannot capture massive intraday positioning shifts, opening versus closing trades, or OTC cross-hedges.

> [!question]- mkt-opt-089 | Explain the term "volatility suppression" under large positive GEX.
> The structural dampening of market swings caused by dealers selling into strength and buying into weakness.
> The hypothesis predicts lower realized volatility and more mean reversion while dealers are long gamma; it does not imply any particular distribution shape.

> [!question]- mkt-opt-090 | What is speed risk for a dealer hedging a book with high gamma concentration?
> Speed is the third derivative dGamma / dS.
> High speed means dealer gamma shifts violently during a market gap, causing delta hedges to rapidly become outdated.

> [!question]- mkt-opt-091 | How does an inverted VIX term structure affect dealer risk appetite?
> Backwardation signals severe immediate market stress and elevated gap risk.
> Dealers widen bid-ask spreads, reduce quoted size, and aggressively derisk inventory, further thinning market liquidity.

> [!question]- mkt-opt-092 | What is shadow gamma in exotic options books?
> Shadow gamma is gamma measured by full revaluation with the volatility surface moving with spot (see mkt-opt-022), and in exotic books it can differ sharply from model gamma near barriers.
> Gamma from barrier options, autocallables and structured notes is also invisible in listed open interest, and it can jump or vanish when a barrier is crossed.

> [!question]- mkt-opt-093 | How do dealers hedge when trading index options against single-stock constituents?
> Index option deltas are usually hedged with index futures or ETFs, and only sometimes with baskets of the constituents.
> Single-stock options are hedged in the stocks, so index and single-stock GEX estimates point to different markets and should not simply be added.

> [!question]- mkt-opt-094 | What is the role of market-on-close (MOC) imbalance orders in dealer delta reconciliation?
> Closing-auction (MOC) orders execute at the official closing price, which is one way a hedger can flatten delta before the overnight gap.
> Published imbalances do not identify their source, so attributing an imbalance to option hedging is an inference, not an observation.

> [!question]- mkt-opt-095 | Why does low market depth exacerbate negative gamma cascades?
> In a thin limit order book, dealer market orders consume multiple price levels, causing large market impact.
> The resulting price drop triggers additional short put gamma, creating an endogenous feedback loop.

> [!question]- mkt-opt-096 | How should a quantitative trader adapt trading style when transitioning from positive to negative GEX?
> A common heuristic: in estimated positive GEX lean toward mean reversion and tighter targets, and in estimated negative GEX toward wider stops, smaller size and protection.
> Backtest the heuristic on your own data first, because the GEX estimate itself rests on a positioning assumption.

## In this repo and The-Distinguished-Engineer

- Code: [mkt_opt_03_gex.py](../code/mkt_opt_03_gex.py) prints and asserts every number in this note under the stated positioning convention; dollar GEX is checked against the hedge trade from repriced deltas, the flip point is found by bisection, and the vanna flow is compared with full revaluation; run it with `uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_opt_03_gex.py`.
- Syllabus: [The Greeks](../../05-Derivatives-and-Volatility/05-The-Greeks.md), [Hedging and Risk for Market Makers](../../08-Market-Making/06-Hedging-and-Risk-for-Market-Makers.md).

---

## Further reading

- Breeden, D. T., & Litzenberger, R. H. (1978). *Prices of state-contingent claims implicit in option prices*. Journal of Business, 51(4), 621-651.
- Garleanu, N., Pedersen, L. H., & Poteshman, A. M. (2009). *Demand-based option pricing*. The Review of Financial Studies, 22(10), 4259-4299.
- SqueezeMetrics. (2016, revised 2017). *Gamma Exposure (GEX): Quantifying hedge rebalancing in SPX options*. White paper.
- SqueezeMetrics. (2020). *The Implied Order Book*. White paper, July 6, 2020.
- Securities and Exchange Commission. (2021). *Staff Report on Equity and Options Market Structure Conditions in Early 2021*. October 14, 2021.
