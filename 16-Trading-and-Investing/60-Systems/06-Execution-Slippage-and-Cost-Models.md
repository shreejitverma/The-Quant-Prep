---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Almgren and Chriss (2000) - Optimal Execution of Portfolio Transactions - Journal of Risk 3(2), Kissell (2013) - The Science of Algorithmic Trading and Portfolio Management, Perold (1988) - The Implementation Shortfall: Paper Versus Reality - Journal of Portfolio Management 14(3), Torre and Ferrari (1997) - The Barra Market Impact Model]
---

# Execution Slippage and Cost Models

## TL;DR

- Total transaction friction decomposes into explicit costs (brokerage commissions, exchange fees, clearing taxes) and implicit costs (bid-ask spread, market impact, delay cost, opportunity cost).
- Implementation Shortfall (Perold 1988) measures the total drag between theoretical paper decision prices and actual executed child fills.
- Market impact splits fundamentally into temporary impact (transitory liquidity concession) and permanent impact (information leakage permanently shifting equilibrium prices).
- The universal square-root law of market impact establishes that price impact scales with daily volatility and the square root of order size relative to daily volume ($I \propto \sigma \sqrt{Q / V}$).
- Strategy capacity is bounded by market impact; because costs scale super-linearly with assets under management (AUM), net Sharpe ratios decay toward zero at institutional scale.
- Algorithmic execution engines slice parent orders into child orders using Time-Weighted Average Price (TWAP), Volume-Weighted Average Price (VWAP), or Percentage of Volume (POV) schedules.

## Learning objectives

- Deconstruct the complete transaction cost taxonomy from order decision to settlement.
- Calculate Implementation Shortfall, execution slippage, and opportunity cost of unfilled orders.
- Formulate the Almgren-Chriss optimal execution model balancing market impact against price volatility risk.
- Apply the square-root law of market impact to estimate strategy capacity and AUM scaling limits.
- Evaluate execution performance against TWAP, VWAP, and arrival price benchmarks.

## Core concepts

### 1. The Transaction Cost Taxonomy and Implementation Shortfall

André Perold (1988) formulated **Implementation Shortfall (IS)** to capture the complete economic gap between theoretical paper backtests and actual live portfolio returns:

$$\text{Implementation Shortfall} = \text{Paper Return} - \text{Realized Live Return}$$

Total execution drag decomposes into explicit and implicit components:

```
+-----------------------------------------------------------------------+
|                    TRANSACTION COST DECOMPOSITION                     |
+-----------------------------------------------------------------------+
| 1. EXPLICIT COSTS                                                     |
|    - Broker commissions (per share or basis points)                   |
|    - Exchange access fees & SEC Section 31 fees                       |
|    - Clearing, settlement, and transaction stamp taxes                |
+-----------------------------------------------------------------------+
| 2. IMPLICIT COSTS                                                     |
|    - Half-Spread: Paying the ask on buys, hitting the bid on sells    |
|    - Delay Cost (Slippage): Price drift from decision to order arrival|
|    - Market Impact: Price distortion caused by the order's own volume |
|    - Opportunity Cost: Lost alpha on unexecuted or canceled shares    |
+-----------------------------------------------------------------------+
```

Mathematically, for a buy order of $S$ shares decided at timestamp $t_d$ with benchmark decision price $P_d$:
- Total executed shares: $S_n \le S$ with individual fill prices $p_j$ and fill quantities $q_j$.
- Unexecuted shares: $S_u = S - S_n$.
- Arrival price when first order enters market: $P_0$.
- Terminal market price when order completes or cancels: $P_T$.
- Total explicit fees: $F$.

$$\text{IS} = \underbrace{\sum_{j} q_j (p_j - P_d)}_{\text{Execution Cost}} + \underbrace{S_u (P_T - P_d)}_{\text{Opportunity Cost}} + \underbrace{F}_{\text{Explicit Fees}}$$

Breaking down execution cost:
- **Delay Cost**: $S_n (P_0 - P_d)$.
- **Realized Spread and Market Impact**: $\sum_j q_j (p_j - P_0)$.

### 2. Temporary vs Permanent Market Impact

Market impact reflects the adverse price movement induced by executing an order:

```
Price
  ^
  |                     Peak Price (Arrival + Temp + Perm)
  |                         /\
  |                        /  \  <- Temporary Impact Decay (Liquidity Refill)
  |                       /    \
  |                      /      \------------------ Permanent Impact Equilibrium
  |                     /
  |                    /
  |  P_0 -------------/  <- Arrival Price
  +--------------------------------------------------> Time
```

1. **Temporary Market Impact ($I_{\text{temp}}$)**:
   - The instantaneous price concession demanded by liquidity providers to absorb immediacy.
   - It is transitory; as limit order book depth replenishes, the temporary price distortion dissipates.
   - Modeled as a function of instantaneous execution speed $\nu_t = \frac{dq}{dt}$:
     $$I_{\text{temp}}(\nu_t) = \eta \cdot \nu_t^{\alpha} \quad (\text{typically } \alpha \approx 0.5 - 1.0)$$
2. **Permanent Market Impact ($I_{\text{perm}}$)**:
   - The persistent price change caused by the order that does not decay after execution completes.
   - It reflects the market's assessment of the informational content of the order flow (Kyle's lambda).
   - Modeled as a linear function of total accumulated order size $Q$:
     $$I_{\text{perm}}(Q) = \gamma \cdot Q$$

### 3. The Universal Square-Root Law of Market Impact

Extensive empirical research across global equity and futures markets (Barra, Kissell, Bouchaud et al., 2012) demonstrates that the per-share price impact scales with the square root of relative order size:

$$I = Y \cdot \sigma_{\text{daily}} \cdot \sqrt{\frac{Q}{V_{\text{ADV}}}}$$

Where:
- $Y$: Dimensionless constant of proportionality, empirically estimated between $0.5$ and $0.7$ across global venues.
- $\sigma_{\text{daily}}$: Daily realized asset volatility ($\frac{\sigma_{\text{ann}}}{\sqrt{252}}$).
- $Q$: Total shares to be executed.
- $V_{\text{ADV}}$: Average daily volume (ADV) in shares.

The square root makes impact concave in size: the per-share price impact still grows as order size grows, but less than proportionally.
Executing $1\%$ of ADV instead of $0.01\%$ is $100$ times the size, so the per-share impact rises by $\sqrt{100} = 10$ times.
Total impact cost in dollars is size times per-share impact, so it scales as $Q^{3/2}$ and rises by $100^{3/2} = 1000$ times.

### 4. Strategy Capacity and the Sharpe Ratio Decay Curve

Strategy capacity is the maximum capital an alpha strategy can manage before execution friction completely consumes gross returns.

Let $A$ denote Assets Under Management (AUM), and $\tau$ denote annual portfolio turnover:
- Total annual volume traded: $V_{\text{traded}} = 2 \cdot \tau \cdot A$.
- Gross alpha return is constant in percentage terms: $\text{Gross PnL} = \alpha_0 \cdot A$.
- By the square-root impact law, total transaction costs scale super-linearly:
  $$\text{Impact Cost} \propto \sigma \sqrt{\frac{V_{\text{traded}}}{V_{\text{market}}}} \cdot V_{\text{traded}} \propto A^{1.5}$$
- Net strategy return in percentage terms:
  $$R_{\text{net}}(A) = \alpha_0 - c \cdot \tau \cdot \sqrt{A}$$

```
Sharpe Ratio
  ^
  |  \
  |   \
  |    \  Net Sharpe Curve (Decays as AUM scales)
  |     \
  |------\------------------------------------ Hurdle Rate (e.g. SR = 0.50)
  |       \
  |        \  <- Critical Capacity Limit A*
  +---------------------------------------------> AUM
```

As AUM grows, transaction costs accelerate faster than gross alpha, dragging net Sharpe downward until it breaches the institutional hurdle rate at critical capacity $A^*$.

### 5. Algorithmic Execution Benchmarks

Institutional order routers dispatch parent orders to algorithmic execution strategies:
- **TWAP (Time-Weighted Average Price)**:
  Slices the parent order into equal-sized child slices dispatched at uniform clock intervals throughout the day.
  Simple to execute, but ignores intra-day volume variation (U-shaped volume curve).
- **VWAP (Volume-Weighted Average Price)**:
  Distributes child order sizes according to historical intra-day volume profiles, trading heavily at the market open and close, and lightly during midday lull.
  Minimizes market impact relative to the market's natural liquidity flow.
- **POV (Percentage of Volume)**:
  Dynamically matches a target participation rate (e.g. 5% or 10% of real-time tape volume).
  Speeds up when market volume surges and slows down when volume dries up, eliminating market impact spikes.
- **Almgren-Chriss Optimal Execution**:
  Solves a dynamic programming frontier balancing market impact costs against the price volatility risk of trading slowly over time.

---

## Worked examples

### Example 1: Calculating Implementation Shortfall on a Block Order

A quantitative fund decides to buy $10,000$ shares of an equity asset:
- Decision Price ($P_d$): $\$100.00$.
- Order arrives at exchange 10 minutes later; Arrival Price ($P_0$): $\$100.20$.
- Execution Schedule:
  - Fill 1: $4,000$ shares at $\$100.35$.
  - Fill 2: $4,000$ shares at $\$100.55$.
  - Unfilled: $2,000$ shares canceled at day end when market closes at $P_T = \$101.00$.
- Total broker commissions and exchange fees: $\$40.00$.

1. **Total Executed Shares**: $S_n = 8,000$ shares.
   Total Unexecuted Shares: $S_u = 2,000$ shares.
2. **Gross Execution Cost**:
   $$\text{Fill 1 Cost} = 4,000 \times (\$100.35 - \$100.00) = 4,000 \times \$0.35 = \$1,400$$
   $$\text{Fill 2 Cost} = 4,000 \times (\$100.55 - \$100.00) = 4,000 \times \$0.55 = \$2,200$$
   $$\text{Total Execution Cost} = \$3,600$$
3. **Opportunity Cost**:
   $$\text{Opportunity Cost} = S_u \times (P_T - P_d) = 2,000 \times (\$101.00 - \$100.00) = \$2,000$$
4. **Explicit Fees**: $\$40.00$.
5. **Total Implementation Shortfall**:
   $$\text{IS} = \$3,600 + \$2,000 + \$40 = \$5,640$$
   In basis points relative to total decision capital ($10,000 \times \$100.00 = \$1,000,000$):
   $$\text{IS (bps)} = \frac{\$5,640}{\$1,000,000} \times 10,000 = 56.4 \text{ bps}$$

### Example 2: Estimating Market Impact via the Square-Root Law

A fund needs to execute $Q = 100,000$ shares of a stock over a single trading day:
- Daily Volume: $V_{\text{ADV}} = 2,000,000$ shares.
- Annualized Volatility: $\sigma_{\text{ann}} = 30.0\%$.
- Daily Volatility: $\sigma_{\text{daily}} = \frac{0.30}{\sqrt{252}} = 0.01890$ ($1.89\%$).
- Proportionality constant: $Y = 0.60$.
- Stock Price: $\$50.00$.

1. **Participation Ratio**:
   $$\frac{Q}{V_{\text{ADV}}} = \frac{100,000}{2,000,000} = 0.05 \quad (5.0\% \text{ of ADV})$$
2. **Estimated Market Impact**:
   $$I = Y \cdot \sigma_{\text{daily}} \cdot \sqrt{\frac{Q}{V_{\text{ADV}}}} = 0.60 \times 0.01890 \times \sqrt{0.05}$$
   $$I = 0.01134 \times 0.2236 = 0.002536 \quad (25.36 \text{ bps})$$
3. **Dollar Cost of Impact**:
   $$\text{Total Order Notional} = 100,000 \times \$50.00 = \$5,000,000$$
   $$\text{Impact Cost} = \$5,000,000 \times 0.002536 = \$12,680$$

Trading $5\%$ of daily volume incurs an expected price penalty of $25.4$ basis points ($\$12,680$).

---

## Pitfalls

- **Assuming Zero Market Impact in Backtests**: Testing strategies with high turnover ($> 500\%$ annually) under flat zero-slippage assumptions, generating fantasy Sharpe ratios that turn negative in live execution.
- **Ignoring the Square-Root Non-Linearity**: Using a fixed per-share slippage model (e.g. $\$0.01$/share), massively understating impact for large block rebalances.
- **Underestimating Delay Cost**: Ignoring the time elapsed between alpha signal computation and order dispatch; in fast-moving markets, prices drift significantly before arrival.
- **Over-Aggressive Child Slicing**: Setting POV participation rates above $20\%$ of tape volume, signaling institutional presence and triggering predatory algorithms to trade ahead.
- **Neglecting Unfilled Order Opportunity Cost**: Evaluating execution algorithms solely by average fill price relative to arrival price, ignoring orders that failed to execute because the market ran away.

---

## Interview questions

> [!question]- mkt-sys-161 | Define Implementation Shortfall (Perold 1988).
> Implementation Shortfall is the difference in return between a theoretical paper portfolio executing instantly at decision prices and the actual realized portfolio executing in live markets.

> [!question]- mkt-sys-162 | State the primary components of Implementation Shortfall.
> The components are explicit fees (commissions, taxes), delay cost (price movement from decision to arrival), market impact and spread, and opportunity cost of unfilled shares.

> [!question]- mkt-sys-163 | What is the difference between temporary and permanent market impact?
> Temporary impact is a transitory price concession caused by immediate liquidity demand that decays as the book refills; permanent impact is the persistent price shift reflecting information content.

> [!question]- mkt-sys-164 | State the universal square-root law of market impact.
> Market impact scales proportionally with daily volatility and the square root of order size relative to daily volume: I = Y * sigma_{daily} * sqrt(Q / V_{ADV}), with Y ~ 0.5 to 0.7.

> [!question]- mkt-sys-165 | Why does market impact exhibit square-root rather than linear scaling with order size?
> Because liquidity providers adjust quotes concavely and hidden order depth replenishes dynamically, dampening price displacement relative to a naive linear order book model.

> [!question]- mkt-sys-166 | What is opportunity cost in trade execution?
> The unrealized profit or avoided loss on shares that were never executed because limit prices were not reached before the market moved away or the order expired.

> [!question]- mkt-sys-167 | What is the trade-off in the Almgren-Chriss optimal execution model?
> The trade-off between market impact (trading fast causes high temporary impact) and market risk (trading slow leaves the position exposed to adverse market volatility).

> [!question]- mkt-sys-168 | What is TWAP and when is it suitable?
> Time-Weighted Average Price divides orders into equal slices at uniform time intervals; suitable for liquid assets with stable volume or low-impact passive rebalancing.

> [!question]- mkt-sys-169 | What is VWAP and how does it account for intra-day liquidity?
> Volume-Weighted Average Price slices orders proportionally to historical intra-day volume curves (higher at open and close, lower midday), minimizing market impact.

> [!question]- mkt-sys-170 | What is Percentage of Volume (POV) algorithmic execution?
> An execution strategy that dynamically trades a fixed percentage (e.g. 5-10%) of actual real-time tape volume, adjusting speed automatically to live market liquidity.

> [!question]- mkt-sys-171 | What is the U-shaped intra-day volume profile in equity markets?
> Trading volume is heavily concentrated in the first 30 minutes after market open and the final 30 minutes before market close, with muted volume during the midday session.

> [!question]- mkt-sys-172 | How does strategy turnover affect transaction cost drag?
> Higher portfolio turnover trades a multiple of portfolio AUM each year, multiplying cumulative market impact and explicit costs and rapidly consuming gross alpha.

> [!question]- mkt-sys-173 | Why does net strategy Sharpe ratio decay as AUM increases?
> Because market impact costs scale super-linearly with AUM (~ AUM^{1.5}) while gross alpha scales linearly (~ AUM), compressing net percentage returns.

> [!question]- mkt-sys-174 | Define strategy capacity.
> Strategy capacity is the maximum capital a quantitative strategy can deploy before market impact and execution costs reduce net return below an investor's hurdle rate.

> [!question]- mkt-sys-175 | What is arrival price in execution benchmarking?
> The midpoint of the bid-ask spread at the exact timestamp when an order is released to the broker or execution algorithm for trading.

> [!question]- mkt-sys-176 | What is slippage in algorithmic execution?
> The difference between the expected execution price (decision or arrival price) and the actual average filled price across all executed child orders.

> [!question]- mkt-sys-177 | What is delay cost (slippage due to latency)?
> The price change that occurs between the portfolio optimization decision timestamp and the physical receipt of the order at the exchange matching engine.

> [!question]- mkt-sys-178 | What is an iceberg order and why is it used?
> A limit order that publicly displays only a small fraction of its total size in the order book, hiding the remaining volume to avoid alerting predatory market participants.

> [!question]- mkt-sys-179 | How do maker-taker fee models influence smart order routing (SOR)?
> SOR engines route limit orders to maker-rebate venues to earn liquidity credits and route aggressive market orders to taker-fee venues with the cheapest access charges.

> [!question]- mkt-sys-180 | What is adverse selection in passive limit order execution?
> Getting filled on passive limit orders primarily when prices are moving violently against the position, leaving the trader with an immediate mark-to-market loss.

> [!question]- mkt-sys-181 | What is predatory trading (order flow front-running)?
> Algorithmic traders detecting institutional order slicing (e.g. via tape footprints or exchange leaks) and trading ahead in the same direction, expanding market impact.

> [!question]- mkt-sys-182 | Why does short selling incur higher execution friction than buying?
> Short selling requires locating shares, paying prime broker borrow fees, and navigating uptick rules (Regulation SHO Rule 201) during market declines.

> [!question]- mkt-sys-183 | What is SEC Section 31 transaction fee?
> A regulatory fee assessed by the SEC on all equity and options sales transactions on US exchanges to fund regulatory oversight, passed through by brokers.

> [!question]- mkt-sys-184 | What is the half-spread cost formula?
> Half-spread cost = 0.5 * (Ask - Bid) per share, representing the immediate cost of crossing the spread to obtain liquidity.

> [!question]- mkt-sys-185 | How does daily volatility sigma_{daily} modulate market impact in the square-root law?
> Higher volatility wide-spreads bid-ask quotations and induces greater market maker risk aversion, scaling market impact proportionally with sigma_{daily}.

> [!question]- mkt-sys-186 | What is liquidity consumption vs liquidity provision in portfolio execution?
> Consuming liquidity uses aggressive market orders that cross the spread, paying impact for certainty; providing liquidity posts passive limit orders, risking non-execution.

> [!question]- mkt-sys-187 | How does the bid-ask spread behave during market stress or earnings announcements?
> Spreads widen dramatically as market makers price in heightened adverse selection risk, multiplying execution costs for strategies attempting to trade during announcements.

> [!question]- mkt-sys-188 | What is Kyle's lambda (lambda_K)?
> Kyle's lambda measures price impact per unit of order flow: dP = lambda_K * Q; it reflects the degree of asymmetric information in the market.

> [!question]- mkt-sys-189 | Why does cross-sectional rebalancing at the market close minimize tracking error?
> Because official mutual fund and index NAVs are benchmarked against official exchange closing prices; trading into the closing auction eliminates intra-day price tracking error.

> [!question]- mkt-sys-190 | What is the closing cross (auction) and how does it reduce market impact?
> The closing cross matches buy and sell interest multilaterally at a single clearing price without bid-ask spreads, allowing large blocks to cross with minimal impact.

> [!question]- mkt-sys-191 | What is the participation rate rule of thumb to avoid signaling market presence?
> Slicing parent orders to remain strictly below 5% to 10% of continuous tape volume to minimize adverse selection and algorithmic footprint detection.

> [!question]- mkt-sys-192 | How does turnover constraint in portfolio optimization prevent transaction cost ruin?
> Enforcing a maximum periodic turnover constraint or quadratic cost penalty restricts rebalancing to high-conviction alpha trades that comfortably exceed execution hurdles.

---

## Further reading

- Almgren, R., & Chriss, N. (2000). Optimal execution of portfolio transactions. *Journal of Risk*, 3(2), 5-40.
- Kissell, R. (2013). *The Science of Algorithmic Trading and Portfolio Management*. Academic Press.
- Perold, A. F. (1988). The implementation shortfall: Paper versus reality. *The Journal of Portfolio Management*, 14(3), 4-9.
- Torre, N., & Ferrari, M. (1997). *The Barra Market Impact Model*. Barra Inc.
