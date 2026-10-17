---
type: concept
title: "Volatility Trading Strategies: Gamma Scalping, VRP, and Dispersion"
track: [quant-trader, quant-research]
tier: advanced
status: solid
est_hours: 1.5
tags: [options, volatility-trading, gamma-scalping, vrp, dispersion, earnings-crush, calendar-spreads, risk-reversal]
prereqs: []
---

# Volatility Trading Strategies: Gamma Scalping, VRP, and Dispersion

Professional volatility trading approaches options not as directional wagers on underlying stock price, but as dedicated asset classes for trading implied versus realized volatility, correlation, and market structure inefficiencies.
By constructing delta-neutral portfolios, quantitative options desks eliminate first-order directional exposure and isolate higher-order non-linear risk premia.
This note formalizes the primary institutional volatility trading strategies: dynamic gamma scalping, systematic harvesting of the variance risk premium (VRP), index-constituent dispersion trading, and event-driven earnings volatility trading.

---

## TL;DR

Volatility strategies monetize discrepancies between priced implied volatility and subsequent realized volatility.
Gamma scalping holds long options, maintains delta neutrality through continuous underlying rebalancing, and profits when realized volatility exceeds implied volatility ($\sigma_{\text{realized}} > \sigma_{\text{implied}}$).
The Variance Risk Premium (VRP) strategy systematically sells implied volatility (via delta-hedged straddles, variance swaps, or options collars) to harvest the historical $2\%$ to $4\%$ premium of implied over realized volatility, managing severe negative skew and tail-risk blowups.
Dispersion trading exploits the structural mispricing between index implied volatility and component stock implied volatilities, selling expensive index options while buying cheap component options to trade implied correlation.
Event-driven earnings strategies monetize pre-announcement volatility run-up and post-announcement volatility crush, calibrated against the ATM straddle implied move.

---

## Learning objectives

- Formulate the mathematical mechanics of delta-neutral gamma scalping and evaluate optimal rebalancing thresholds.
- Quantify the Variance Risk Premium (VRP) and design robust tail-risk hedging overlays.
- Structure and execute an equity dispersion trade, calculating index versus constituent implied correlation.
- Model pre-earnings implied volatility run-ups and post-earnings volatility crush dynamics.
- Formulate relative-value volatility trades across skew (risk reversals, ratio spreads) and term structure (calendar and diagonal spreads).

---

## Core concepts

### 1. Delta-Neutral Gamma Scalping

Gamma scalping is the process of holding a long options position (positive Gamma $\Gamma$, negative Theta $\Theta$), neutralizing Delta with underlying stock, and dynamically trading the underlying asset as spot moves to capture realized price oscillations.

1. **The Fundamental PnL Equation**:
   As proved by Carr and Madan (1998), the cumulative mark-to-market PnL of a delta-hedged option position over horizon $[0, T]$ with zero interest rates expands to:
   $$\text{PnL} = \frac{1}{2} \int_0^T \Gamma_t S_t^2 (\sigma_{\text{realized}, t}^2 - \sigma_{\text{implied}, t}^2) dt - \text{Transaction Costs}$$
   - If realized volatility along the actual asset path exceeds the implied volatility paid to enter the position ($\sigma_{\text{realized}} > \sigma_{\text{implied}}$), gross gamma gains exceed theta decay costs, producing positive net PnL.
   - If realized volatility falls short of implied volatility ($\sigma_{\text{realized}} < \sigma_{\text{implied}}$), daily theta bleed exceeds gamma gains, resulting in an overall loss.

2. **Rebalancing Disciplines**:
   - **Periodic Rebalancing**: The desk rebalances Delta at fixed time intervals (e.g., hourly, daily at market close).
   - Downside: If the market oscillates intensely within the interval, gamma gains are missed; if the market trends smoothly, transaction costs are incurred with minimal gamma capture.
   - **Threshold Rebalancing (Band Hedging)**: The desk defines a tolerance band $[-\bar{\Delta}, +\bar{\Delta}]$.
   - Stock is traded only when portfolio delta breaches the band:
     $$\Delta S_{\text{trigger}} = \pm \frac{\bar{\Delta}}{\Gamma}$$
   - This discipline minimizes transaction costs while guaranteeing that stock is bought or sold only after meaningful price oscillations occur.

### 2. Harvesting the Variance Risk Premium (VRP)

The Variance Risk Premium is the structural spread between implied volatility and realized volatility:

$$\text{VRP} = \mathbb{E}^{\mathbb{Q}}[\sigma] - \mathbb{E}^{\mathbb{P}}[\sigma] \approx \sigma_{\text{implied}} - \sigma_{\text{realized}}$$

1. **Economic Origin**:
   - Institutional portfolio managers pay an insurance premium to hedge equity market crashes.
   - Market makers and volatility sellers require an expected positive return to bear catastrophic left-tail jump risk.
   - Empirically, in the S&P 500, implied volatility exceeds subsequent realized volatility in approximately $85\%$ of rolling 30-day periods, averaging a premium of $2.0\%$ to $4.5\%$ volatility points.

2. **Payoff Profile and Left-Tail Catastrophe Risk**:
   - Systematically selling ATM straddles or variance swaps generates a high Sharpe ratio (often $> 1.2$) characterized by steady daily theta accrual.
   - However, the strategy exhibits massive negative skewness and extreme excess kurtosis.
   - Unhedged volatility selling funds face catastrophic liquidation during sudden market panics (e.g., Black Monday 1987, Volmageddon in February 2018, COVID-19 crash in March 2020).
   - Institutional VRP funds implement strict tail-risk overlays: buying far-out-of-the-money (5-delta) puts, utilizing dynamic leverage caps, and maintaining stop-out triggers based on VIX term structure inversion.

### 3. Dispersion Trading (Correlation Trading)

Dispersion trading exploits the mathematical relationship between the volatility of an index $\sigma_I$ and the volatilities of its individual constituent stocks $\sigma_i$:

$$\sigma_I^2 = \sum_{i=1}^N w_i^2 \sigma_i^2 + 2 \sum_{i=1}^N \sum_{j < i} w_i w_j \sigma_i \sigma_j \rho_{ij}$$

Assuming an average pairwise implied correlation $\bar{\rho}_{\text{implied}}$ across all pairs, the equation simplifies to:

$$\sigma_I^2 \approx \bar{\sigma}_{\text{comp}}^2 \left(\frac{1 - \bar{\rho}}{N} + \bar{\rho}\right) \approx \bar{\sigma}_{\text{comp}}^2 \bar{\rho}$$

1. **Trade Structure**:
   - **Sell Index Options**: Short index (e.g., S&P 500) straddles or variance swaps.
   - **Buy Component Options**: Long weighted straddles or variance swaps on the underlying single stocks (e.g., top 50 S&P constituents).
   - **Delta Neutrality**: Both index and component positions are delta-hedged.

2. **The Economic Rationale**:
   - Index options carry an enormous correlation premium because institutional investors hedge portfolios at the macro index level rather than buying individual single-stock puts.
   - Consequently, implied correlation $\bar{\rho}_{\text{implied}}$ systematically exceeds realized correlation $\bar{\rho}_{\text{realized}}$.
   - When constituent stocks move independently (idiosyncratic earnings dispersion), single-stock gamma gains explode while index gamma remains subdued, generating substantial net profit.
   - **The Crisis Failure Mode**: During a systemic market crash, all constituent stocks drop simultaneously ($\rho_{\text{realized}} \to 1.0$).
   - The short index options position loses heavily, while single-stock diversification benefits vanish.

### 4. Earnings Volatility Trading

Corporate quarterly earnings announcements introduce discrete event jump risk into individual equity options:

1. **Pre-Earnings Volatility Run-Up**:
   - In the weeks preceding earnings, uncertainty intensifies while speculative options buying surges.
   - Near-term implied volatility inflates steadily, peaking on the final trading session prior to the release.
   - Pre-earnings strategy: Buy options 14 to 21 days before earnings and exit immediately before the announcement to capture the pure vega expansion without holding through the earnings gap.

2. **The ATM Straddle Implied Move**:
   - The market's expectation of the earnings price move is derived from the front-month at-the-money straddle:
     $$\text{Implied Move} \approx \frac{\text{Call}_{\text{ATM}} + \text{Put}_{\text{ATM}}}{S} \approx 0.8 \times \frac{\text{Straddle Price}}{S}$$
   - Over large historical samples, actual post-earnings stock moves fall inside this implied move approximately $65\%$ to $70\%$ of the time.

3. **Post-Earnings Volatility Crush**:
   - Once earnings are released and the forward guidance is public, event uncertainty instantly drops to zero.
   - Front-month implied volatility collapses by $30\%$ to $60\%$ within minutes of market open.
   - Option sellers monetizing the crush sell short iron condors, straddles, or calendars, profiting when the actual move is less than the priced straddle.

### 5. Skew and Term Structure Relative-Value Trades

1. **Risk Reversals (Skew Trading)**:
   - Buy an OTM call and sell an OTM put (or vice versa), delta-hedged with stock.
   - Isolates exposure to changes in the slope of the volatility smile without directional spot risk.

2. **Ratio Spreads**:
   - Buy one closer-to-the-money option and sell two or three farther out-of-the-money options to monetize steep volatility skew.
   - Constructed for zero net premium or a credit; carries naked tail risk if the market gaps through the short strikes.

3. **Calendar and Diagonal Spreads (Term Structure Trading)**:
   - Sell near-dated options (high theta decay) and buy long-dated options (low theta decay).
   - In a contango term structure, the near-dated contract decays faster than the back-month contract, enabling the trader to capture positive time roll-down.

---

## Worked examples

### Example 1: Gamma Scalping PnL Attribution Under Realized Volatility Outperformance

A quantitative options trader purchases an ATM straddle on an index:
- Spot Price: $S = \$5,000.00$.
- Strike: $K = \$5,000.00$.
- Maturity: $T = 30\text{ days} = 0.08219\text{ years}$.
- Implied Volatility Paid: $\sigma_{\text{implied}} = 16.0\%$ ($0.16$).
- Straddle Position Gamma: $\Gamma = 0.00280$ (combined call + put gamma).
- Daily Straddle Theta: $\Theta = -\$1,100.00\text{ per day}$.
- Daily Holding Period: $\Delta t = 1\text{ day} = 1/365\text{ years}$.

Over the subsequent 24-hour trading session, the market experiences high intraday volatility:
- Intraday high: $\$5,080.00$, intraday low: $\$4,940.00$, close: $\$5,060.00$.
- The trader executes two threshold delta hedges:
  1. Hedges at $\$5,050.00$ by selling $140$ shares.
  2. Hedges at $\$4,960.00$ by buying $250$ shares.
  3. Rebalances at the close of $\$5,060.00$ by selling $110$ shares.
- Total gross trading profit captured from underlying shares: $+\$2,450.00$.
- Transaction costs (fees and bid-ask slippage): $-\$120.00$.

1. **Evaluate Net Daily Strategy PnL**:
   $$\text{Net Gamma Gains} = +\$2,450.00 - \$120.00 = +\$2,330.00$$
   $$\text{Theta Bleed Incurred} = -\$1,100.00$$
   $$\text{Net Session PnL} = +\$2,330.00 - \$1,100.00 = +\$1,230.00$$

2. **Analyze Implied vs Realized Volatility**:
   - The realized intraday path generated annualized volatility of approximately $24.0\%$.
   - Because realized volatility ($24\%$) significantly exceeded implied volatility ($16\%$), gross gamma scalping profits exceeded daily theta decay, generating a clean positive return.

### Example 2: Pricing and Weighting a Dispersion Trade

A desk structures a dispersion trade on an index consisting of two equal-weighted mega-cap stocks ($w_1 = 0.5$, $w_2 = 0.5$):
- Component 1 Implied Volatility: $\sigma_1 = 30\%$ ($0.30$).
- Component 2 Implied Volatility: $\sigma_2 = 30\%$ ($0.30$).
- Index Implied Volatility: $\sigma_I = 24\%$ ($0.24$).

1. **Extract Implied Pairwise Correlation ($\rho_{\text{implied}}$)**:
   $$\sigma_I^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 w_1 w_2 \sigma_1 \sigma_2 \rho$$
   $$(0.24)^2 = (0.5)^2(0.30)^2 + (0.5)^2(0.30)^2 + 2(0.5)(0.5)(0.30)(0.30) \rho$$
   $$0.0576 = 0.25(0.09) + 0.25(0.09) + 0.5(0.09) \rho$$
   $$0.0576 = 0.0225 + 0.0225 + 0.0450 \rho$$
   $$0.0576 = 0.0450 + 0.0450 \rho$$
   $$0.0450 \rho = 0.0576 - 0.0450 = 0.0126$$
   $$\rho_{\text{implied}} = \frac{0.0126}{0.0450} = 0.28 = 28.0\%$$

2. **Trade Execution and Outcome**:
   - The desk determines that fundamental pairwise correlation is historically $12\%$.
   - The market is overpricing correlation at $28\%$.
   - The desk sells index straddles and buys component straddles weighted to achieve vega-neutrality.
   - Over the subsequent month, single stocks move idiosyncratically on earnings while the index remains flat ($\rho_{\text{realized}} = 10\%$).
   - The single-stock options explode in value while index straddles bleed theta, delivering a profitable dispersion harvest.

---

## Pitfalls

- **The Negative Skew Trap in Naked Volatility Selling**:
  Selling ATM straddles to harvest VRP generates attractive Sharpe ratios during calm regimes but guarantees catastrophic drawdown during market jumps.
  A single $4\sigma$ gap event can completely erase multiple years of accumulated theta gains.
- **Over-Hedging Friction in Gamma Scalping**:
  Hedging delta too frequently in choppy sideways markets causes transaction costs and bid-ask spread friction to consume all theoretical gamma gains.
  Desks must calibrate hedging thresholds to market microstructure noise and tick sizes.
- **Correlation Breakdown in Dispersion During Panics**:
  Dispersion is fundamentally a short correlation trade.
  In a macro liquidity crisis, all asset correlations jump toward $1.0$.
  The short index position blows up, while component stock hedges fail to provide offsetting gains.
- **Holding Short Options Through Binary Earnings Gaps**:
  Selling earnings volatility without defined-risk boundaries exposes the trader to ruinous post-earnings gap moves ($> 20\%$).
  Even if the stock price does not move, an unexpectedly wide earnings range can cause Vega to spike rather than crush.

---

## Interview questions

> [!question]- mkt-opt-097 | What is delta-neutral gamma scalping?
> A quantitative options strategy where a long options position is delta-hedged with underlying stock, dynamically buying low and selling high as spot moves.
> It isolates exposure to the spread between realized volatility and implied volatility.

> [!question]- mkt-opt-098 | State the Carr-Madan PnL equation for a delta-hedged option.
> PnL = 0.5 * Integral_0^T Gamma_t * S_t^2 * (sigma_realized^2 - sigma_implied^2) dt - Transaction_Costs.
> The position generates positive net PnL if realized volatility along the path exceeds the implied volatility paid at entry.

> [!question]- mkt-opt-099 | Contrast periodic delta hedging with threshold (band) delta hedging.
> Periodic hedging rebalances delta at fixed time intervals regardless of market movement.
> Threshold hedging rebalances only when position delta breaches a predetermined tolerance band, reducing unnecessary turnover in choppy markets.

> [!question]- mkt-opt-100 | What is the Variance Risk Premium (VRP)?
> The structural empirical spread where implied volatility exceeds subsequent realized volatility: VRP = sigma_implied - sigma_realized.
> It reflects an insurance risk premium paid by hedgers to options sellers for taking on left-tail disaster risk.

> [!question]- mkt-opt-101 | Why is systematic unhedged VRP harvesting considered a "picking up nickels in front of a steamroller" strategy?
> It yields steady small daily gains from theta decay punctuated by rare, catastrophic losses during market crashes.
> The return distribution exhibits severe negative skewness and excess kurtosis.

> [!question]- mkt-opt-102 | What is a dispersion trade in equity options?
> A relative-value volatility strategy that sells index options and buys a basket of underlying constituent stock options.
> It monetizes the structural overpricing of index implied correlation relative to realized correlation.

> [!question]- mkt-opt-103 | How does the mathematical relationship between index volatility and component volatility define implied correlation?
> sigma_Index^2 ~ sum w_i^2 * sigma_i^2 + sum_{i!=j} w_i * w_j * sigma_i * sigma_j * rho_implied.
> If index implied volatility is high relative to component implied volatilities, implied correlation is elevated.

> [!question]- mkt-opt-104 | Why does a dispersion trade lose heavily during a systemic financial crisis?
> In a crisis, stock correlations spike toward 1.0, eliminating constituent diversification.
> The short index options position suffers massive losses that exceed the gains on component long options.

> [!question]- mkt-opt-105 | What is the formula for the ATM straddle implied earnings move?
> Implied Move ~ (Call_ATM + Put_ATM) / Spot ~ 0.8 * Straddle_Price / Spot.
> It estimates the one-standard-deviation price move expected by options markets over the corporate earnings release.

> [!question]- mkt-opt-106 | What is post-earnings volatility crush?
> The immediate, violent collapse in front-month implied volatility once earnings figures are publicly announced.
> The event jump risk premium drops to zero, dramatically deflating option prices.

> [!question]- mkt-opt-107 | How can a trader profit from pre-earnings implied volatility run-up without taking earnings gap risk?
> By buying options 2 to 3 weeks prior to the earnings date and selling them immediately before the announcement.
> The trader captures pure Vega expansion while avoiding overnight gap risk.

> [!question]- mkt-opt-108 | What is a risk reversal options structure?
> An options strategy combining a long out-of-the-money call and a short out-of-the-money put (or vice versa).
> It directly trades the slope or skew of the implied volatility surface.

> [!question]- mkt-opt-109 | What is a vertical ratio spread?
> Buying one closer-to-the-money option and selling multiple farther out-of-the-money options of the same expiration.
> It exploits steep volatility skew to enter the position for zero net debit or a net credit.

> [!question]- mkt-opt-110 | What is the primary tail risk of a 1x2 ratio put spread?
> If the underlying asset drops far below the short put strikes, the position exhibits naked short put exposure.
> Losses accelerate linearly toward catastrophic levels as the stock approaches zero.

> [!question]- mkt-opt-111 | What is a calendar spread (time spread)?
> Selling a short-dated option and buying a long-dated option with the same strike price.
> It profits from faster theta decay in the front-month contract under a contango term structure.

> [!question]- mkt-opt-112 | What is a diagonal spread?
> An options strategy combining contracts with different strike prices and different expiration dates.
> It combines the horizontal time decay of a calendar spread with the directional skew of a vertical spread.

> [!question]- mkt-opt-113 | Why does a calendar spread perform poorly during a sudden volatility spike?
> Front-month implied volatility surges far more than back-month volatility (term structure inverts to backwardation).
> The short near-dated option expands in value faster than the long back-month option, creating a net loss.

> [!question]- mkt-opt-114 | What is a variance swap?
> An over-the-counter forward contract on annualised realized variance with a linear payoff in variance: Payoff = N * (sigma_realized^2 - K_var).
> Unlike standard options, a variance swap provides pure exposure to volatility without requiring delta hedging.

> [!question]- mkt-opt-115 | How is the strike of a variance swap replicated using vanilla options?
> By holding a static, continuous strip of OTM calls and puts weighted inversely by strike squared (1 / K^2): K_var = (2 / T) * Integral (1 / K^2) * Option(K) dK.
> This replicates the log-contract payoff derived by Neuberger (1994) and Demeterfi et al. (1999).

> [!question]- mkt-opt-116 | What is a volatility swap and how does it differ from a variance swap?
> A contract whose payoff is linear in volatility (sigma_realized - K_vol) rather than variance.
> Replicating a volatility swap requires dynamic trading because volatility is non-linear in options prices.

> [!question]- mkt-opt-117 | What is convexity in variance swaps?
> Because variance is volatility squared (sigma^2), a variance swap has positive convexity with respect to volatility.
> Large volatility spikes produce exponential profits for the long variance holder.

> [!question]- mkt-opt-118 | What is the correlation swap?
> An over-the-counter derivative with a payoff proportional to the difference between realized average pairwise correlation and a fixed strike correlation.
> It provides a direct, pure instrument for trading dispersion without delta-hedging single stocks.

> [!question]- mkt-opt-119 | What is Vega neutrality in dispersion trading?
> Structuring the ratio of single-stock options to index options such that the total net Vega of the portfolio equals zero.
> This ensures the trade profits purely from correlation divergence rather than parallel market volatility shifts.

> [!question]- mkt-opt-120 | What is Gamma neutrality in a volatility arbitrage book?
> Designing the options portfolio such that total net Gamma across strikes equals zero.
> It protects the desk against immediate underlying spot price shocks.

> [!question]- mkt-opt-121 | What is an iron condor?
> A defined-risk volatility selling strategy combining an out-of-the-money bull put spread and an out-of-the-money bear call spread.
> It captures premium when the underlying asset remains range-bound between the short strikes.

> [!question]- mkt-opt-122 | What is an iron butterfly?
> An options strategy combining a short at-the-money call, a short at-the-money put, and long out-of-the-money wings.
> It maximizes profit when spot closes exactly at the central strike, collecting high upfront credit.

> [!question]- mkt-opt-123 | How does market microstructure noise affect high-frequency gamma scalping?
> Bid-ask bounce and discrete order book ticks create artificial price oscillations that do not represent true underlying diffusion.
> Scalping inside bid-ask noise burns capital on bid-ask spreads without generating true gamma alpha.

> [!question]- mkt-opt-124 | What is the Derman-Kani volatility smile model?
> An implied tree algorithm that constructs a discrete binomial/trinomial tree matching market smile prices without continuous diffusion assumptions.
> It represents the first discrete-time implementation of local volatility theory.

> [!question]- mkt-opt-125 | What is smile roll-down in calendar spread trading?
> As time passes, back-month options roll down the term structure and smile curve toward near-dated expiries.
> If the term structure is upward sloping, options lose value through time roll-down, generating capital gains for option sellers.

> [!question]- mkt-opt-126 | What is a volatility surface arbitrage engine?
> An automated algorithmic monitor that scans option chains across strikes and expiries for calendar or butterfly arbitrage violations.
> Upon detecting negative butterfly prices, it executes risk-free box or butterfly arbitrage trades.

> [!question]- mkt-opt-127 | What is forward-starting option and where is it used?
> An option whose strike price is determined at a specified future date (e.g., ATM on day T1) and expires at T2.
> It is used to hedge forward implied volatility and forms a core component of cliquet structures.

> [!question]- mkt-opt-128 | How do institutional desks hedge the tail risk of an active VRP short-volatility strategy?
> By allocating 10% to 15% of accumulated premium into continuous rolling deep out-of-the-money (5-delta to 10-delta) put options.
> This caps maximum catastrophic drawdown during sudden market crashes while preserving net positive carry.

---

## Further reading

- Carr, P., & Madan, D. (1998). *Towards a theory of volatility trading*. Volatility: New Estimation Techniques for Pricing and Risk Management, 29(1), 417-427.
- Demeterfi, K., Derman, E., Kamal, M., & Zou, J. (1999). *A guide to variance swaps*. Quantitative Strategies Research Notes, Goldman Sachs.
- Bakshi, G., & Madan, D. (2000). *Spanning and derivative-security valuation*. Journal of Financial Economics, 55(2), 205-238.
- Driessen, J., Maenhout, P. J., & Vilkov, G. (2009). *The price of correlation risk: Evidence from equity options*. The Journal of Finance, 64(3), 1377-1406.
- Natenberg, S. (2014). *Option Volatility and Pricing: Advanced Trading Strategies and Techniques*. McGraw-Hill Education.
