---
type: concept
track: [quant-trader, quant-research]
tier: advanced
status: draft
prereqs: [bonds-duration-and-convexity, curve-risk-and-hedging]
est_hours: 5
sources: [Bruce Tuckman and Angel Serrat - Fixed Income Securities chapters 5 and 6, Moorad Choudhry - The Repo and Modern Markets Handbook, Antti Ilmanen - Expected Returns chapters 4 and 5]
---

# Fixed Income P&L Attribution and Relative Value

## TL;DR

Fixed income portfolio performance is decomposed into distinct, orthogonal risk drivers: carry, roll-down, parallel curve shift (delta), slope (twist), curvature (butterfly), spread/basis movements, and higher-order convexity (gamma) and time decay (theta).
Relative value (RV) trading exploits pricing discrepancies along the yield curve rather than taking directional rate bets.
Key RV structures include curve steepeners and flatteners (distinguished by bull and bear regimes) and butterfly spreads (weighting wings against the body via 50-50 DV01 or empirical regression betas).
Asset swaps (ASW) package bonds with interest rate swaps to extract credit, funding, and repo mispricings across cash and synthetic markets.
Rigorous daily P&L attribution reconciles realized trading gains against predicted risk-factor contributions, exposing unhedged residual curve risks and funding leakage.

## Learning objectives

- Formulate the fixed income daily P&L attribution equation across carry, roll-down, delta, twist, butterfly, spread, and convexity components.
- Calculate carry and roll-down returns under unchanged yield curve assumptions.
- Construct curve steepener and flattener positions under bull and bear market regimes.
- Design duration-neutral and regression-weighted butterfly trades (e.g., 2s-5s-10s and 5s-10s-30s).
- Structure par-par and market-value asset swaps to isolate asset-swap spreads (ASW).
- Compute empirical hedge ratios using PCA or yield regression beta to prevent curve twist leakage in butterfly portfolios.

## Core concepts

### The Fixed Income P&L Attribution Framework

A comprehensive fixed income P&L attribution decomposes total dollar P&L over holding period $\Delta t$ into deterministic (time-driven) and stochastic (market-driven) components:

$$\Delta \text{P\&L}_{\text{total}} = \text{Carry} + \text{Roll-down} + \text{Delta} + \text{Twist} + \text{Curvature} + \text{Convexity} + \text{Theta} + \text{Spread/Basis} + \epsilon$$

where:

1. **Carry:** The net cash flow earned over the holding period assuming static yield levels. For a financed bond position with coupon $c$, repo funding rate $r_{\text{repo}}$, and purchase price $P$:

$$\text{Carry} = (c - r_{\text{repo}} \cdot P) \cdot \Delta t$$

2. **Roll-down:** The capital appreciation that occurs as the bond approaches maturity along an upward-sloping yield curve, assuming the spot curve remains unchanged:

$$\text{Roll-down} \approx -D_{\text{mod}} \cdot P \cdot (y(T - \Delta t) - y(T))$$

If the curve is upward sloping, $y(T - \Delta t) < y(T)$, so the yield drops as the bond rolls down, generating positive capital gain.
The combined metric **Carry + Roll-down** represents the expected horizon return under static market conditions:

$$\text{Expected P\&L}_{\text{static}} = \text{Carry} + \text{Roll-down}$$

3. **Delta (Parallel Shift):** The first-order P&L impact of a uniform shift $\Delta y_{\text{parallel}}$ across all key rate tenors:

$$\text{P\&L}_{\text{Delta}} = -\text{DV01}_{\text{portfolio}} \cdot \Delta y_{\text{parallel}} \times 10,000$$

4. **Slope / Twist:** The impact of curve steepening or flattening, typically defined by the change in the 2s10s or 5s30s spread:

$$\text{P\&L}_{\text{Twist}} = -\sum_{i} \text{DV01}_i \cdot \Delta y_{i, \text{slope}}$$

5. **Curvature / Butterfly:** The impact of intermediate tenors flexing relative to the curve wings (measured via principal component 3 or butterfly spreads):

$$\text{P\&L}_{\text{Curvature}} = -\sum_{i} \text{DV01}_i \cdot \Delta y_{i, \text{curvature}}$$

6. **Convexity (Gamma):** The second-order Taylor expansion term capturing non-linear yield sensitivity:

$$\text{P\&L}_{\text{Convexity}} = \frac{1}{2} \cdot \text{Convexity}_{\$} \cdot (\Delta y)^2$$

where $\text{Convexity}_{\$} = P \cdot \text{Convexity}$.

7. **Theta:** The passage-of-time decay on embedded options or forward bond contracts:

$$\text{P\&L}_{\text{Theta}} = \frac{\partial P}{\partial t} \cdot \Delta t$$

8. **Spread / Basis:** The change in yield spread relative to the benchmark government or swap curve (e.g., Z-spread, OAS, or asset swap spread):

$$\text{P\&L}_{\text{Spread}} = -\text{DV01} \cdot \Delta s \times 10,000$$

### Curve Trading: Steepeners and Flatteners

Curve trades take a view on the yield spread between two tenors $T_1$ and $T_2$ (where $T_1 < T_2$):

$$\text{Spread} = y(T_2) - y(T_1)$$

To construct a duration-neutral curve trade, positions are weighted inversely to their DV01:

$$\text{DV01}_1 \cdot N_1 + \text{DV01}_2 \cdot N_2 = 0 \implies \frac{N_1}{N_2} = -\frac{\text{DV01}_2}{\text{DV01}_1}$$

#### 1. Steepener Trade
A curve steepener profits when $y(T_2) - y(T_1)$ increases (curve widens).
The trader goes **Long Front End** ($T_1$) and **Short Back End** ($T_2$).
Steepeners behave differently depending on the macro environment:
- **Bull Steepener:** Driven by central bank rate cuts. Front-end yields fall faster than back-end yields ($y_1 \downarrow\downarrow, y_2 \downarrow$).
- **Bear Steepener:** Driven by rising inflation expectations, expanding fiscal deficits, or term premium expansion. Back-end yields surge while the front end remains pinned by monetary policy ($y_1 \uparrow, y_2 \uparrow\uparrow$).

#### 2. Flattener Trade
A curve flattener profits when $y(T_2) - y(T_1)$ decreases (curve narrows or inverts).
The trader goes **Short Front End** ($T_1$) and **Long Back End** ($T_2$).
- **Bull Flattener:** Driven by a flight-to-safety bid or long-term growth slowdown. Long-end yields fall faster than front-end yields ($y_1 \downarrow, y_2 \downarrow\downarrow$).
- **Bear Flattener:** Driven by central bank rate-hiking cycles. Front-end yields jump rapidly as short rates are raised, while long-end yields rise more slowly ($y_1 \uparrow\uparrow, y_2 \uparrow$).

### Butterfly Spreads: Wings vs. Body

A butterfly spread is a three-legged curve structure combining two outer tenors ("wings", $T_1$ and $T_3$) and an intermediate tenor ("body", $T_2$, where $T_1 < T_2 < T_3$).
Common benchmark butterflies include 2s-5s-10s and 5s-10s-30s.
The butterfly spread yield is defined as:

$$\text{Fly Spread} = 2 \cdot y(T_2) - (y(T_1) + y(T_3))$$

When the fly spread increases, the curve becomes more convex (the body cheapens relative to the wings).

#### Weighting Schemes: 50-50 DV01 vs. Regression Beta
A trader executing a long butterfly goes **Long the Wings and Short the Body**:

1. **50-50 DV01 Weighting:**
Each wing contributes exactly half of the total hedging DV01 of the body:

$$\text{DV01}_{\text{wing 1}} = \frac{1}{2} \text{DV01}_{\text{body}}, \quad \text{DV01}_{\text{wing 2}} = \frac{1}{2} \text{DV01}_{\text{body}}$$

While 50-50 DV01 weighting ensures zero exposure to a uniform parallel curve shift ($\Delta y_1 = \Delta y_2 = \Delta y_3$), it leaves significant residual exposure to curve rotation (twist).
Because yield volatility is typically higher at the front end ($\sigma_1 > \sigma_3$), a parallel-neutral 50-50 butterfly incurs large directional P&L when the curve steepens or flattens.

2. **Regression Beta Weighting (Duration-Weighted PCA / Regression):**
To immunize against both parallel shift and curve slope, the trader estimates the historical beta of yield changes from a regression:

$$\Delta y_2 = \beta_1 \Delta y_1 + \beta_3 \Delta y_3 + \epsilon$$

The weights $(w_1, w_2, w_3)$ on notional are selected such that:

$$\sum_{i=1}^3 w_i \cdot \text{DV01}_i = 0 \quad \text{and} \quad \sum_{i=1}^3 w_i \cdot \text{DV01}_i \cdot \text{Factor}_{\text{slope}, i} = 0$$

Under regression weighting, the shorter wing typically receives a smaller DV01 allocation than the longer wing to offset the higher yield volatility of the front end.

### Asset Swap Spreads (ASW)

An asset swap transforms a fixed-rate bond into a synthetic floating-rate note (or vice versa), separating the issuer's credit and liquidity spread from underlying interest rate risk.

#### 1. Par-Par Asset Swap
In a par-par asset swap:
- The investor purchases a fixed-rate bond at market price $P$.
- Concurrently, the investor enters an interest rate swap paying the bond's fixed coupons and receiving floating SOFR/Euribor plus a constant spread $s_{\text{ASW}}$ on par notional.
- At inception, if the bond trades at a discount or premium to par ($P \ne 100$), an upfront cash payment $(100 - P)$ is exchanged between the counterparties.

The par-par asset swap spread $s_{\text{ASW}}$ satisfies:

$$s_{\text{ASW}} \approx \frac{y_{\text{bond}} - y_{\text{swap}}}{1 + \frac{100 - P}{100 \cdot \text{PV01}_{\text{swap}}}}$$

#### 2. Market-Value (Proceeds) Asset Swap
To eliminate upfront cash exchange, the interest rate swap notional is set equal to the dirty price of the bond:

$$\text{Swap Notional} = P_{\text{dirty}}$$

The fixed leg pays the actual bond coupons, and the floating leg pays SOFR plus spread on $P_{\text{dirty}}$.
At maturity, the floating leg settles par ($100$), creating a terminal notional mismatch if $P_{\text{dirty}} \ne 100$.

### Relative Value Signals: Z-Score and Mean Reversion

Relative value quants identify mispriced curve points by tracking the rolling time-series Z-score of butterfly spreads or asset swap spreads:

$$Z(t) = \frac{\text{Fly Spread}(t) - \mu_{\text{rolling}}(t)}{\sigma_{\text{rolling}}(t)}$$

- When $Z(t) > +2.0$, the body is unusually cheap relative to wings (fly spread too high). Quants execute a **Short Fly** (buy body, sell wings), which profits when the body richens and the fly spread mean-reverts down.
- When $Z(t) < -2.0$, the body is rich relative to wings (fly spread too low). Quants execute a **Long Fly** (buy wings, sell body), which profits when the body cheapens and the fly spread mean-reverts up.
- Key risk: Regime change. Macro rate cycles or Treasury auction supply can cause spreads to trend persistently, turning statistical RV mean-reversion trades into large drawdowns.

## Worked examples

### Example 1: Daily Fixed Income P&L Attribution

A fund holds $\$100,000,000$ notional of a 10-year Treasury bond trading at a clean price of $98.50$ (dirty price $99.20$).
The bond has a modified duration of $D_{\text{mod}} = 8.20$ years and annual convexity of $C = 78.0$.
The bond yield is $4.20\%$, and its 1-day repo financing rate is $4.00\%$.
Over a 1-day holding period ($\Delta t = 1/360$), the yield curve experiences a parallel rise of $+5$ basis points ($\Delta y = +0.0005$), while the bond rolls down by $-0.3$ basis points along the static yield curve.
Compute the detailed P&L attribution.

**Step 1: Compute portfolio DV01 and Dollar Convexity:**

$$\text{Portfolio Value } P = \$100,000,000 \times 0.9920 = \$99,200,000$$

$$\text{DV01} = P \times D_{\text{mod}} \times 0.0001 = \$99,200,000 \times 8.20 \times 0.0001 = \$81,344 \text{ per bp}$$

$$\text{Dollar Convexity } C_{\$} = P \times C = \$99,200,000 \times 78.0 = \$7,737,600,000$$

**Step 2: Carry P&L:**
Assuming coupon $c = 4.10\%$ ($0.0410$):

$$\text{Carry} = \frac{0.0410 \times \$100,000,000 - 0.0400 \times \$99,200,000}{360} = \frac{\$4,100,000 - \$3,968,000}{360} = \frac{\$132,000}{360} \approx +\$366.67$$

**Step 3: Roll-down P&L:**
The bond yield rolls down by $\Delta y_{\text{roll}} = -0.00003$ (-0.3 bps):

$$\text{Roll-down} = -\text{DV01} \times (-0.3 \text{ bps}) \times 10,000 \times 0.0001 = \$81,344 \times 0.3 = +\$24,403.20$$

Total static horizon return = $\text{Carry} + \text{Roll-down} = \$366.67 + \$24,403.20 = +\$24,769.87$.

**Step 4: Delta P&L (from $+5$ bp shift):**

$$\text{P\&L}_{\text{Delta}} = -\text{DV01} \times 5 = -\$81,344 \times 5 = -\$406,720.00$$

**Step 5: Convexity P&L (Gamma gain):**

$$\text{P\&L}_{\text{Convexity}} = \frac{1}{2} \times C_{\$} \times (\Delta y)^2 = \frac{1}{2} \times \$7,737,600,000 \times (0.0005)^2 = \frac{1}{2} \times \$7,737,600,000 \times 2.5 \times 10^{-7} = +\$967.20$$

**Step 6: Total Predicted P&L:**

$$\Delta \text{P\&L}_{\text{predicted}} = \$366.67 + \$24,403.20 - \$406,720.00 + \$967.20 = -\$380,982.93$$

The roll-down and positive convexity partially softened the $\$406,720$ delta loss.

### Example 2: Structuring a 2s-5s-10s Butterfly Trade

A trader constructs a duration-neutral 2s-5s-10s butterfly spread using Treasury notes with the following parameters:
- 2-year note: $\text{DV01}_2 = \$19.50$ per $\$100,000$ notional.
- 5-year note: $\text{DV01}_5 = \$44.20$ per $\$100,000$ notional.
- 10-year note: $\text{DV01}_{10} = \$81.50$ per $\$100,000$ notional.

The trader shorts $\$100,000,000$ notional of the 5-year body ($\text{DV01}_{\text{body}} = \$44,200$).
Structure a 50-50 DV01 weighted long butterfly by computing the required notionals for the 2-year and 10-year wings.

**Step 1: Allocate target DV01 to each wing:**
Under 50-50 DV01 weighting:

$$\text{Target DV01}_2 = 0.50 \times \text{DV01}_{\text{body}} = 0.50 \times \$44,200 = \$22,100$$

$$\text{Target DV01}_{10} = 0.50 \times \text{DV01}_{\text{body}} = 0.50 \times \$44,200 = \$22,100$$

**Step 2: Compute 2-year wing notional:**

$$N_2 = \frac{\$22,100}{\$19.50} \times \$100,000 \approx \$113,333,333$$

**Step 3: Compute 10-year wing notional:**

$$N_{10} = \frac{\$22,100}{\$81.50} \times \$100,000 \approx \$27,116,564$$

**Step 4: Check duration neutrality:**

$$\text{Total Wing DV01} = \$22,100 + \$22,100 = \$44,200$$

$$\text{Net DV01} = \text{Total Wing DV01} - \text{Body DV01} = \$44,200 - \$44,200 = \$0$$

The trade is strictly immune to a parallel yield curve shift.

## Pitfalls

- **Confusing Parallel DV01 Neutrality with Curve Neutrality:** A 50-50 DV01 butterfly is immunized against parallel shifts, but highly sensitive to curve twist (steepening/flattening) due to volatility asymmetry across tenors.
- **Ignoring Negative Carry on Rich Butterflies:** Entering a butterfly trade with positive mean-reversion expectations can be unprofitable if financing costs and roll-down decay (negative carry) exceed the expected convergence gain.
- **Repo Specialness Squeeze:** Relative value cash-bond legs can become "on special" in the repo market, dramatically lowering the repo rate earned and squeezing short financing.
- **Settlement Lag Mismatch:** Mixing Treasury cash bonds (T+1 settlement) with interest rate swaps (T+2 spot start) creates unhedged overnight delta exposure unless forward start dates are synchronized.
- **Neglecting On-The-Run Liquidity Premia:** Rolling from off-the-run to on-the-run benchmarks causes artificial jumps in yield spreads that do not represent genuine relative value mispricings.

## Interview questions

> [!question]- fi-rv-pnl-carry-vs-rolldown | Explain the distinction between Carry and Roll-down in fixed income performance attribution.
> Carry is the net cash flow earned over time assuming yield levels remain constant, consisting of coupon accrued minus the financing/repo cost. Roll-down is the price appreciation that occurs as the bond ages toward maturity along an upward-sloping yield curve, capturing the lower yield assigned to shorter maturities under an unchanged spot curve.

> [!question]- fi-rv-bull-vs-bear-steepeners | Contrast a Bull Steepener with a Bear Steepener in terms of macro drivers and relative yield shifts.
> A Bull Steepener occurs when front-end yields decline faster than back-end yields, typically triggered by central bank rate cuts during monetary easing. A Bear Steepener occurs when long-end yields rise faster than short-end yields, driven by rising inflation expectations, supply pressures, or expanding fiscal deficits while short rates remain anchored.

> [!question]- fi-rv-butterfly-spread-definition | Define a yield curve butterfly spread (body vs. wings) and explain what a widening butterfly indicates.
> A butterfly spread combines two outer tenors ("wings", $T_1$ and $T_3$) and an intermediate tenor ("body", $T_2$): $\text{Fly} = 2 \cdot y(T_2) - (y(T_1) + y(T_3))$. A widening butterfly spread means the body yield is rising relative to the wings, indicating that intermediate maturities are cheapening and curve curvature is increasing.

> [!question]- fi-rv-fifty-fifty-dv01-limitation | Why is a 50-50 DV01 weighted butterfly vulnerable to yield curve slope changes (twist risk)?
> A 50-50 DV01 weighting allocates equal DV01 to the short and long wings. However, yield volatility is substantially higher at short tenors ($\sigma_2 > \sigma_{10}$). If the curve steepens, the front-end yield drops more than the long-end yield rises, causing the short wing to gain more than the long wing loses, leaving the portfolio exposed to directional curve tilt.

> [!question]- fi-rv-regression-beta-butterfly | How does regression beta weighting improve butterfly immunization compared to simple 50-50 DV01?
> Regression beta weighting estimates the statistical sensitivity $\Delta y_2 = \beta_1 \Delta y_1 + \beta_3 \Delta y_3$ from historical data or principal component analysis. The wing notionals are weighted to simultaneously immunize against both a parallel shift ($\sum \text{DV01}_i = 0$) and a slope rotation ($\sum \text{DV01}_i \cdot \text{Slope}_i = 0$), eliminating first-order twist leakage.

> [!question]- fi-rv-asset-swap-spread-asw | What is an Asset Swap Spread (ASW), and what risks does it isolate?
> An asset swap combines a fixed-rate bond with an interest rate swap that pays the bond's fixed coupons and receives floating benchmark rates (SOFR/Euribor) plus a constant spread $s_{\text{ASW}}$. ASW isolates the credit risk, liquidity premium, and financing basis of the specific bond by stripping out underlying benchmark interest rate duration.

> [!question]- fi-rv-par-par-vs-market-value-asw | Distinguish between a Par-Par Asset Swap and a Market-Value (Proceeds) Asset Swap.
> In a par-par asset swap, the swap notional equals the bond par value, and an upfront cash exchange of $(100 - P)$ reconciles any bond price premium or discount. In a market-value asset swap, the swap notional equals the dirty purchase price of the bond, eliminating initial cash exchange but introducing a terminal notional mismatch at maturity when the bond redeems at par.

> [!question]- fi-rv-repo-specialness-impact | How does a bond trading "on special" in the repo market affect relative value trading strategies?
> When a bond is on special, high demand to borrow it drives its repo financing rate well below general collateral (GC) rates (sometimes near zero or negative). A trader shorting the special bond must pay a punitive borrowing fee, which eats into trade profitability and can force premature liquidation of basis or relative value positions.

> [!question]- fi-rv-zscore-relative-value-risks | Why can relying solely on rolling Z-scores of curve spreads be dangerous for relative value hedge funds?
> Z-scores assume that curve spreads fluctuate around a stationary, mean-reverting mean. During macroeconomic regime shifts, central bank policy overhauls, or sovereign debt supply surges, spreads can trend structurally away from historical averages. A Z-score strategy will continue doubling down into widening divergence, causing severe drawdowns.

> [!question]- fi-rv-box-trade-mechanics | What is a yield curve box trade, and how is it used to exploit spread dislocations?
> A box trade combines two curve spread trades across different tenor pairs (e.g., long 2s5s steepener and long 10s30s flattener). It isolates changes in the spread of spreads ($[y_5 - y_2] - [y_{30} - y_{10}]$), hedging out both level and general slope to capture localized curve kinks, supply imbalances, or segmented investor demand.

## Further reading

- Bruce Tuckman and Angel Serrat, *Fixed Income Securities: Tools for Today's Markets*, Chapter 5: "Yield Curve Trades" and Chapter 6: "Relative Value and Arbitrage".
- Moorad Choudhry, *The Repo and Modern Markets Handbook: Master Guide to Repo, Derivatives, and Fixed Income Relative Value*.
- Antti Ilmanen, *Expected Returns: An Investor's Guide to Harvesting Market Rewards*, Chapter 4: "Bond Risk Premia".
- P. Veronesi, *Fixed Income Securities: Valuation, Risk, and Risk Management*, Chapter 8: "Trading and Hedging Strategies".

## In this repo and SDE-Interview-Prep

- Discounting and yield curve foundations: [Discounting and Yield Curves](01-Discounting-and-Yield-Curves.md).
- Duration, convexity, and immunization mathematics: [Bonds, Duration, and Convexity](02-Bonds-Duration-and-Convexity.md).
- Advanced credit indices and tranche trading: [Credit Advanced: CDS Indices and Tranches](23-Credit-Advanced-CDS-Indices-and-Tranches.md).
