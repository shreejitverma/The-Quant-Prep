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
The Variance Risk Premium (VRP) strategy systematically sells implied volatility (via delta-hedged straddles or variance swaps) to harvest the average excess of implied over subsequently realized variance, while managing severe negative skew and tail-risk losses.
Dispersion trading sells index volatility and buys constituent volatility, a bet that realized correlation will come in below the correlation implied by index and constituent option prices.
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
   Carr and Madan (1998) and El Karoui, Jeanblanc-Picque and Shreve (1998) show that, for an option delta-hedged at the implied volatility with zero interest rates, the cumulative P&L over $[0, T]$ is:
   $$\text{PnL} = \frac{1}{2} \int_0^T \Gamma_t S_t^2 (\sigma_{\text{realized}, t}^2 - \sigma_{\text{implied}, t}^2) dt - \text{Transaction Costs}$$
   - If realized volatility along the actual asset path exceeds the implied volatility paid to enter the position ($\sigma_{\text{realized}} > \sigma_{\text{implied}}$), gross gamma gains exceed theta decay costs, producing positive net PnL.
   - If realized volatility falls short of implied volatility ($\sigma_{\text{realized}} < \sigma_{\text{implied}}$), daily theta bleed exceeds gamma gains, resulting in an overall loss.

2. **Rebalancing Disciplines**:
   - **Periodic Rebalancing**: The desk rebalances Delta at fixed time intervals (e.g., hourly, daily at market close).
   - Downside: If the market oscillates intensely within the interval, gamma gains are missed; if the market trends smoothly, transaction costs are incurred with minimal gamma capture.
   - **Threshold Rebalancing (Band Hedging)**: The desk defines a tolerance band $[-\bar{\Delta}, +\bar{\Delta}]$.
   - Stock is traded only when portfolio delta breaches the band:
     $$\Delta S_{\text{trigger}} = \pm \frac{\bar{\Delta}}{\Gamma}$$
   - This discipline trades less often than fixed-interval hedging in choppy markets, at the cost of larger delta drift between trades.

### 2. Harvesting the Variance Risk Premium (VRP)

The Variance Risk Premium is the gap between risk-neutral and physical expected realized variance:

$$\text{VRP} = \mathbb{E}^{\mathbb{Q}}[\sigma^2_{\text{realized}}] - \mathbb{E}^{\mathbb{P}}[\sigma^2_{\text{realized}}]$$

In practice it is often proxied by implied volatility (or the variance-swap rate) minus subsequently realized volatility.

1. **Economic Origin**:
   - Institutional portfolio managers pay an insurance premium to hedge equity market crashes.
   - Market makers and volatility sellers require an expected positive return to bear catastrophic left-tail jump risk.
   - For equity indices the premium has been positive on average; its size depends on the sample period and the measure, so quote a figure only with its source and dates.

2. **Payoff Profile and Left-Tail Catastrophe Risk**:
   - Systematically selling ATM straddles or variance swaps produces steady accrual in calm periods, so its Sharpe ratio measured over a calm sample can look high.
   - The return distribution has strong negative skewness and excess kurtosis, which a Sharpe ratio does not capture.
   - Short-volatility positions take their largest losses in sudden volatility spikes such as October 1987, February 2018 and March 2020.
   - Common risk controls include buying far-out-of-the-money puts as a tail overlay, capping leverage and cutting exposure when the term structure inverts.

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
   - Index options embed a correlation risk premium: Driessen, Maenhout and Vilkov (2009) find that index options are expensive relative to constituent options, which they attribute to a priced correlation risk.
   - Implied correlation has therefore tended to exceed subsequently realized correlation, which is what the trade harvests.
   - When constituent stocks move independently (idiosyncratic earnings dispersion), the long single-stock gamma earns while the short index gamma costs little, so the trade profits.
   - **The Crisis Failure Mode**: During a systemic market crash, all constituent stocks drop simultaneously ($\rho_{\text{realized}} \to 1.0$).
   - The short index options position loses heavily, while single-stock diversification benefits vanish.

### 4. Earnings Volatility Trading

Corporate quarterly earnings announcements introduce discrete event jump risk into individual equity options:

1. **Pre-Earnings Volatility Run-Up**:
   - In the weeks preceding earnings, uncertainty intensifies while speculative options buying surges.
   - Near-term implied volatility inflates steadily, peaking on the final trading session prior to the release.
   - One pre-earnings approach is to buy options some weeks before the release and sell them before the announcement, aiming to capture the rise in implied volatility without holding through the gap; the entry timing is a choice to backtest, not a rule.

2. **The ATM Straddle Implied Move**:
   - The front-month at-the-money straddle prices the risk-neutral expected absolute move:
     $$\frac{\mathbb{E}|S_T - S|}{S} \approx \frac{\text{Call}_{\text{ATM}} + \text{Put}_{\text{ATM}}}{S}$$
   - Under a normal approximation the straddle equals $\sqrt{2/\pi} \approx 0.80$ times the one-standard-deviation move, so the one-sd move is about $1.25$ times the straddle.
   - Under that same normal model a move smaller than the straddle happens $57.5\%$ of the time and a move within one standard deviation $68.3\%$ of the time; real earnings moves are fat-tailed, so check the hit rate on your own sample.

3. **Post-Earnings Volatility Crush**:
   - Once earnings are released and the forward guidance is public, event uncertainty instantly drops to zero.
   - Front-month implied volatility typically falls sharply at the first trade after the release, by an amount that depends on how much event variance was priced.
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

A quantitative options trader purchases $1,000$ units of an ATM straddle on an index (for example $10$ contracts with a $100$ multiplier; all inputs hypothetical):
- Spot Price: $S = \$5,000.00$.
- Strike: $K = \$5,000.00$.
- Maturity: $T = 30\text{ days} = 0.08219\text{ years}$ ($\sqrt{T} = 0.28669$).
- Implied Volatility Paid: $\sigma_{\text{implied}} = 16.0\%$ ($0.16$); rates and dividends are set to zero.
- Daily Holding Period: $\Delta t = 1\text{ day} = 1/365\text{ years}$.

1. **Compute the Straddle Greeks**:
   $$d_1 = 0.5 \sigma \sqrt{T} = 0.5 \times 0.16 \times 0.28669 = 0.02294, \quad \phi(d_1) = 0.39884$$
   $$\Gamma_{\text{unit}} = \frac{2 \phi(d_1)}{S \sigma \sqrt{T}} = \frac{0.79767}{229.35} = 0.0034779, \quad \Gamma_{\text{position}} = 1,000 \times 0.0034779 = 3.4779$$
   With zero rates, theta is exactly the gamma rent at implied volatility:
   $$\Theta_{\text{daily}} = -\frac{1}{2} \Gamma_{\text{position}} S^2 \sigma_{\text{implied}}^2 \Delta t = -0.5 \times 3.4779 \times 5000^2 \times 0.0256 / 365 = -\$3,049.15$$
   Rounding gamma to $3.478$ first would give $-\$3,049.21$; the closed-form theta agrees with the unrounded figure.
   The entry delta of $1,000 \times (2 N(d_1) - 1) = 18.3$ is neutralized at entry, so later hedges only offset the gamma-driven delta $\Gamma_{\text{position}} \times (S - 5000)$.

Over the subsequent 24-hour trading session, the market experiences high intraday volatility:
- The trader rebalances to delta-neutral at $\$5,050.00$, at $\$4,960.00$ and at the close of $\$5,060.00$.
  1. At $\$5,050.00$ the straddle delta is $3.4779 \times 50 = +173.9$, so the trader sells $174$ units.
  2. At $\$4,960.00$ it is $3.4779 \times (-40) = -139.1$ against a hedge of $-174$, so the trader buys $313$ units.
  3. At the close of $\$5,060.00$ it is $3.4779 \times 60 = +208.7$ against a hedge of $+139$, so the trader sells $348$ units, ending short $209$ units.
- Transaction costs (fees and bid-ask slippage): $-\$120.00$.

2. **Evaluate the Hedge and Option Legs**:
   $$\text{Hedge Cash} = 174 \times 5050 - 313 \times 4960 + 348 \times 5060 = 878,700 - 1,552,480 + 1,760,880 = +\$1,087,100$$
   $$\text{Hedge PnL} = 1,087,100 - 209 \times 5060 = 1,087,100 - 1,057,540 = +\$29,560$$
   $$\text{Option Convexity on the Net Move} = 0.5 \times 3.4779 \times 60^2 = +\$6,260.29$$
   $$\text{Gross Gamma Gains} = 29,560 + 6,260.29 = +\$35,820.29$$
   This matches the leg-by-leg sum $0.5 \times 3.4779 \times (50^2 + 90^2 + 100^2) = 0.5 \times 3.4779 \times 20,600 = \$35,822.75$ to within the $\$2.46$ lost by rounding hedges to whole units.
   Both are the second-order (gamma) approximation; the option's own theta for the day is charged separately below.

3. **Evaluate Net Daily Strategy PnL**:
   $$\text{Net Session PnL} = 35,820.29 - 120.00 - 3,049.15 = +\$32,651.14$$

4. **Analyze Implied vs Realized Volatility**:
   - The hedged path has $\sum (\Delta S)^2 = 20,600$, an annualized realized volatility of $\sqrt{20,600 \times 365} / 5000 = 54.8\%$.
   - The breakeven daily move at $16\%$ implied is $S \sigma \sqrt{\Delta t} = 5000 \times 0.16 \times \sqrt{1/365} = 41.87$ points.
   - Because realized volatility ($54.8\%$) far exceeded implied volatility ($16\%$), gamma scalping gains were $11.7$ times the theta paid.

### Example 2: Pricing and Weighting a Dispersion Trade

A desk structures a dispersion trade on an index consisting of two equal-weighted stocks ($w_1 = 0.5$, $w_2 = 0.5$; all inputs hypothetical):
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
   - The desk's own forecast of realized correlation is $12\%$ (a hypothetical input).
   - If that forecast is right, the market is overpricing correlation at $28\%$.
   - The backing script confirms the implied correlation independently: simulating two $30\%$-volatility stocks with correlation $0.28$ gives an equal-weight index volatility of $24\%$ within four standard errors.
   - The desk sells index straddles and buys component straddles weighted to achieve vega-neutrality.
   - Over the subsequent month, single stocks move idiosyncratically on earnings while the index remains flat ($\rho_{\text{realized}} = 10\%$).
   - The long single-stock straddles earn more gamma than their theta while the short index straddles lose less gamma than the theta they collect, so the trade profits.

---

## Pitfalls

- **The Negative Skew Trap in Naked Volatility Selling**:
  Selling ATM straddles to harvest VRP can show attractive Sharpe ratios over calm samples but exposes the book to large drawdowns in market jumps.
  A single gap can erase many months of accumulated theta, because losses grow with the square of the move while theta accrues linearly in time.
- **Over-Hedging Friction in Gamma Scalping**:
  Hedging delta too frequently in choppy sideways markets causes transaction costs and bid-ask spread friction to consume all theoretical gamma gains.
  Desks must calibrate hedging thresholds to market microstructure noise and tick sizes.
- **Correlation Breakdown in Dispersion During Panics**:
  Dispersion is fundamentally a short correlation trade.
  In a macro liquidity crisis, all asset correlations jump toward $1.0$.
  The short index position blows up, while component stock hedges fail to provide offsetting gains.
- **Holding Short Options Through Binary Earnings Gaps**:
  Selling earnings volatility without defined-risk boundaries exposes the trader to post-earnings gaps far larger than the implied move.
  Implied volatility can also stay high after the release if the report raises uncertainty (for example vague guidance) instead of resolving it.

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
> The gap between risk-neutral and physical expected realized variance, often proxied by implied minus subsequently realized volatility.
> It reflects an insurance risk premium paid by hedgers to options sellers for taking on left-tail disaster risk.

> [!question]- mkt-opt-101 | Why is systematic unhedged VRP harvesting considered a "picking up nickels in front of a steamroller" strategy?
> It yields steady small daily gains from theta decay punctuated by rare, catastrophic losses during market crashes.
> The return distribution exhibits severe negative skewness and excess kurtosis.

> [!question]- mkt-opt-102 | What is a dispersion trade in equity options?
> A relative-value volatility strategy that sells index options and buys a basket of underlying constituent stock options.
> It profits when realized correlation comes in below the correlation implied by index and constituent options, which on average has been the case (Driessen, Maenhout and Vilkov 2009).

> [!question]- mkt-opt-103 | How does the mathematical relationship between index volatility and component volatility define implied correlation?
> sigma_Index^2 ~ sum w_i^2 * sigma_i^2 + sum_{i!=j} w_i * w_j * sigma_i * sigma_j * rho_implied.
> If index implied volatility is high relative to component implied volatilities, implied correlation is elevated.

> [!question]- mkt-opt-104 | Why does a dispersion trade lose heavily during a systemic financial crisis?
> In a crisis, stock correlations spike toward 1.0, eliminating constituent diversification.
> The short index options position suffers massive losses that exceed the gains on component long options.

> [!question]- mkt-opt-105 | What is the formula for the ATM straddle implied earnings move?
> Expected |Move| / Spot ~ (Call_ATM + Put_ATM) / Spot: the straddle prices the risk-neutral expected absolute move.
> Under a normal approximation the one-standard-deviation move is about Straddle / 0.80 ~ 1.25 * Straddle, so 0.8 * Straddle understates it.

> [!question]- mkt-opt-106 | What is post-earnings volatility crush?
> The immediate, violent collapse in front-month implied volatility once earnings figures are publicly announced.
> The event jump risk premium drops to zero, dramatically deflating option prices.

> [!question]- mkt-opt-107 | How can a trader profit from pre-earnings implied volatility run-up without taking earnings gap risk?
> By buying options some weeks before the earnings date and selling them before the announcement (the exact entry is a backtested choice, not a rule).
> The trader aims to capture the rise in implied volatility while avoiding the gap, paying theta and bearing the risk that the run-up does not happen.

> [!question]- mkt-opt-108 | What is a risk reversal options structure?
> An options strategy combining a long out-of-the-money call and a short out-of-the-money put (or vice versa).
> It directly trades the slope or skew of the implied volatility surface.

> [!question]- mkt-opt-109 | What is a vertical ratio spread?
> Buying one closer-to-the-money option and selling multiple farther out-of-the-money options of the same expiration.
> It exploits steep volatility skew to enter the position for zero net debit or a net credit.

> [!question]- mkt-opt-110 | What is the primary tail risk of a 1x2 ratio put spread?
> If the underlying asset drops far below the short put strikes, the position exhibits naked short put exposure.
> Below the lower breakeven the position loses one extra unit per point of decline, linearly, all the way to the underlying reaching zero.

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
> By holding a static strip of OTM puts and calls weighted by 1 / K^2: K_var = (2 / T) * exp(r * T) * Integral Option_OTM(K) / K^2 dK (with the forward as the dividing strike).
> The strip replicates the log contract (Neuberger 1994; Demeterfi, Derman, Kamal and Zou 1999); with a flat volatility surface it returns K_var = sigma^2, which the backing script checks by quadrature.

> [!question]- mkt-opt-116 | What is a volatility swap and how does it differ from a variance swap?
> A contract whose payoff is linear in volatility (sigma_realized - K_vol) rather than variance.
> Volatility is a concave function of variance, so a volatility swap cannot be replicated statically with vanilla options; its fair strike sits below the square root of the variance-swap strike by a convexity adjustment that depends on the volatility of volatility.

> [!question]- mkt-opt-117 | What is convexity in variance swaps?
> Because variance is volatility squared (sigma^2), a variance swap has positive convexity with respect to volatility.
> Payoff grows with the square of realized volatility, so a volatility spike pays the long variance holder more than proportionally (quadratically, not exponentially).

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
> An implied binomial tree (Derman and Kani 1994) whose node probabilities are fitted so the tree reprices the market smile.
> It is a discrete counterpart of Dupire's (1994) continuous local volatility model; Rubinstein (1994) published a related implied-tree method the same year.

> [!question]- mkt-opt-125 | What is smile roll-down in calendar spread trading?
> As time passes, back-month options roll down the term structure and smile curve toward near-dated expiries.
> If the term structure is upward sloping, options lose value through time roll-down, generating capital gains for option sellers.

> [!question]- mkt-opt-126 | What is a volatility surface arbitrage engine?
> An automated algorithmic monitor that scans option chains across strikes and expiries for calendar or butterfly arbitrage violations.
> When a butterfly or calendar trades below zero after fees and spreads, it flags an arbitrage that the desk can try to capture, subject to execution and margin risk.

> [!question]- mkt-opt-127 | What is forward-starting option and where is it used?
> An option whose strike price is determined at a specified future date (e.g., ATM on day T1) and expires at T2.
> It is used to hedge forward implied volatility and forms a core component of cliquet structures.

> [!question]- mkt-opt-128 | How do institutional desks hedge the tail risk of an active VRP short-volatility strategy?
> A common approach spends a fixed budget out of collected premium on rolling far-out-of-the-money puts, alongside leverage caps.
> The overlay limits crash losses at the cost of lower carry; the budget is a design choice to test, not a standard percentage.

## In this repo and The-Distinguished-Engineer

- Code: [mkt_opt_04_vol_strategies.py](../code/mkt_opt_04_vol_strategies.py) prints and asserts every number in this note; the scalping P&L is rebuilt from the explicit trade blotter, the implied correlation is confirmed by a seeded simulation, and the variance-swap replication by quadrature over an option strip; run it with `uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_opt_04_vol_strategies.py`.
- Syllabus: [Option Strategies and Volatility Trading](../../05-Derivatives-and-Volatility/13-Option-Strategies-and-Volatility-Trading.md), [Variance Swaps and Volatility Products](../../05-Derivatives-and-Volatility/14-Variance-Swaps-and-Volatility-Products.md), [Dispersion and Correlation Trading](../../05-Derivatives-and-Volatility/15-Dispersion-and-Correlation-Trading.md).

---

## Further reading

- Carr, P., & Madan, D. (1998). *Towards a theory of volatility trading*. In R. Jarrow (Ed.), Volatility: New Estimation Techniques for Pricing Derivatives. Risk Books; reprinted in Option Pricing, Interest Rates and Risk Management (Cambridge University Press, 2001), 458-476.
- El Karoui, N., Jeanblanc-Picque, M., & Shreve, S. E. (1998). *Robustness of the Black and Scholes formula*. Mathematical Finance, 8(2), 93-126.
- Demeterfi, K., Derman, E., Kamal, M., & Zou, J. (1999). *A guide to volatility and variance swaps*. Journal of Derivatives, 6(4), 9-32; the Goldman Sachs research note version is *More than you ever wanted to know about volatility swaps*.
- Derman, E., & Kani, I. (1994). *Riding on a smile*. Risk, 7(2), 32-39.
- Neuberger, A. (1994). *The log contract*. Journal of Portfolio Management, 20(2), 74-80.
- Bakshi, G., & Madan, D. (2000). *Spanning and derivative-security valuation*. Journal of Financial Economics, 55(2), 205-238.
- Driessen, J., Maenhout, P. J., & Vilkov, G. (2009). *The price of correlation risk: Evidence from equity options*. The Journal of Finance, 64(3), 1377-1406.
- Natenberg, S. (2014). *Option Volatility and Pricing: Advanced Trading Strategies and Techniques*. McGraw-Hill Education.
