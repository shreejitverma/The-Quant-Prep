---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Almgren and Chriss (2000) - Optimal Execution of Portfolio Transactions - Journal of Risk 3(2), Almgren Thum Hauptmann and Li (2005) - Direct Estimation of Equity Market Impact - Risk 18(7), Toth Lemperiere Deremble de Lataillade Kockelkoren and Bouchaud (2011) - Anomalous Price Impact and the Critical Nature of Liquidity in Financial Markets - Physical Review X 1, Kyle (1985) - Continuous Auctions and Insider Trading - Econometrica 53(6), Kissell (2013) - The Science of Algorithmic Trading and Portfolio Management, Perold (1988) - The Implementation Shortfall: Paper Versus Reality - Journal of Portfolio Management 14(3), SEC Regulation SHO Rule 201 - Release 34-61595 (2010)]
---

# Execution Slippage and Cost Models

## TL;DR

- Total transaction friction decomposes into explicit costs (brokerage commissions, exchange fees, clearing taxes) and implicit costs (bid-ask spread, market impact, delay cost, opportunity cost).
- Implementation Shortfall (Perold 1988) measures the total drag between theoretical paper decision prices and actual executed child fills.
- Market impact splits fundamentally into temporary impact (transitory liquidity concession) and permanent impact (information leakage permanently shifting equilibrium prices).
- The empirical square-root law of market impact says that the impact of a metaorder scales with daily volatility and the square root of its size relative to daily volume ($I \propto \sigma \sqrt{Q / V}$); fitted exponents range from about 0.4 to 0.7.
- Strategy capacity is bounded by market impact; because dollar costs grow like $\text{AUM}^{3/2}$ while gross alpha grows like AUM, net returns fall as AUM grows.
- Algorithmic execution engines slice parent orders into child orders using Time-Weighted Average Price (TWAP), Volume-Weighted Average Price (VWAP), or Percentage of Volume (POV) schedules.

## Learning objectives

- Deconstruct the complete transaction cost taxonomy from order decision to settlement.
- Calculate Implementation Shortfall, execution slippage, and opportunity cost of unfilled orders.
- Formulate the Almgren-Chriss optimal execution model balancing market impact against price volatility risk.
- Apply the square-root law of market impact to estimate strategy capacity and AUM scaling limits.
- Evaluate execution performance against TWAP, VWAP, and arrival price benchmarks.

## Core concepts

### 1. The Transaction Cost Taxonomy and Implementation Shortfall

Andre Perold (1988) formulated **Implementation Shortfall (IS)** as the gap between a paper portfolio that trades instantly at decision prices and the real portfolio:

$$\text{Implementation Shortfall} = \text{Paper Return} - \text{Realized Live Return}$$

Total execution drag decomposes into explicit and implicit components:

```
+-----------------------------------------------------------------------+
|                    TRANSACTION COST DECOMPOSITION                     |
+-----------------------------------------------------------------------+
| 1. EXPLICIT COSTS                                                     |
|    - Broker commissions (per share or basis points)                   |
|    - Exchange access fees and SEC Section 31 fees                     |
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
     $$I_{\text{temp}}(\nu_t) = \eta \cdot \nu_t^{\alpha}$$
   - Almgren and Chriss (2000) take $\alpha = 1$ (linear) for tractability; Almgren, Thum, Hauptmann, and Li (2005) estimate $\alpha \approx 0.6$ on US equity orders executed by Citigroup.
2. **Permanent Market Impact ($I_{\text{perm}}$)**:
   - The persistent price change caused by the order that does not decay after execution completes.
   - It reflects the market's assessment of the informational content of the order flow (Kyle's lambda, Kyle 1985).
   - Modeled as a linear function of total accumulated order size $Q$:
     $$I_{\text{perm}}(Q) = \gamma \cdot Q$$

### 3. The Square-Root Law of Market Impact

Empirical studies of metaorders across equities and futures find that the average price change from the first to the last fill of a metaorder scales roughly with the square root of its size relative to daily volume (Toth et al. 2011, who report fitted exponents between 0.4 and 0.7 across studies; Almgren et al. 2005 fit 0.6):

$$I = Y \cdot \sigma_{\text{daily}} \cdot \sqrt{\frac{Q}{V_{\text{ADV}}}}$$

Where:
- $Y$: Dimensionless constant of proportionality, of order one (Toth et al. 2011); it must be estimated for each market and execution style.
- $\sigma_{\text{daily}}$: Daily realized asset volatility ($\frac{\sigma_{\text{ann}}}{\sqrt{252}}$).
- $Q$: Total shares to be executed.
- $V_{\text{ADV}}$: Average daily volume (ADV) in shares.

The square root makes impact concave in size: the per-share price impact still grows as order size grows, but less than proportionally.
Executing $1\%$ of ADV instead of $0.01\%$ is $100$ times the size, so the per-share impact rises by $\sqrt{100} = 10$ times.
Total impact cost in dollars is size times per-share impact, so it scales as $Q^{3/2}$ and rises by $100^{3/2} = 1000$ times.
With $Y = 1$, trading $1\%$ of daily volume moves the price by $\sqrt{0.01} = 0.1$ daily standard deviations, which Toth et al. (2011) highlight as a surprisingly large effect of a small order.

### 4. Strategy Capacity and the Sharpe Ratio Decay Curve

Strategy capacity is the maximum capital an alpha strategy can manage before execution friction completely consumes gross returns.

Let $A$ denote Assets Under Management (AUM), and $\tau$ denote annual portfolio turnover:
- Total annual volume traded: $V_{\text{traded}} = 2 \cdot \tau \cdot A$.
- Gross alpha return is constant in percentage terms: $\text{Gross PnL} = \alpha_0 \cdot A$.
- By the square-root impact law, with a fixed number of rebalances per year, total dollar transaction costs scale super-linearly:
  $$\text{Impact Cost} \propto \sigma \sqrt{\frac{V_{\text{traded}}}{V_{\text{market}}}} \cdot V_{\text{traded}} \propto \tau^{3/2} A^{3/2}$$
- Net strategy return in percentage terms, with $k \propto \sigma \tau^{3/2}$ collecting the constants:
  $$R_{\text{net}}(A) = \alpha_0 - k \sqrt{A}$$
- Net return reaches a hurdle $h$ at $A^* = \left(\frac{\alpha_0 - h}{k}\right)^2$, and net dollar profit $A(\alpha_0 - k\sqrt{A})$ peaks at $\left(\frac{\alpha_0}{1.5k}\right)^2$, which is $4/9$ of the zero-return capacity.

```
Sharpe Ratio
  ^
  |  \
  |   \
  |    \  Net Sharpe Curve (Decays as AUM scales)
  |     \
  |------\------------------------------------ Hurdle Rate (illustrative)
  |       \
  |        \  <- Critical Capacity Limit A*
  +---------------------------------------------> AUM
```

As AUM grows, transaction costs grow faster than gross alpha, dragging net return and net Sharpe ratio down until they breach the hurdle at capacity $A^*$.

### 5. Algorithmic Execution Benchmarks

Institutional order routers dispatch parent orders to algorithmic execution strategies:
- **TWAP (Time-Weighted Average Price)**:
  Slices the parent order into equal-sized child slices dispatched at uniform clock intervals throughout the day.
  Simple to execute, but ignores intra-day volume variation (U-shaped volume curve).
- **VWAP (Volume-Weighted Average Price)**:
  Distributes child order sizes according to historical intra-day volume profiles, trading more near the open and close, where volume is higher, and less at midday.
  It targets the day's volume-weighted average price, so it trades with the market's natural liquidity, but it does not minimize impact or risk.
- **POV (Percentage of Volume)**:
  Dynamically matches a target participation rate (e.g. 5% or 10% of real-time tape volume).
  Speeds up when market volume surges and slows down when volume dries up, keeping participation, though not impact, constant.
- **Almgren-Chriss Optimal Execution**:
  Minimizes $E[\text{cost}] + \lambda \text{Var}[\text{cost}]$ with linear temporary and permanent impact; the optimal holdings follow $x(t) = X \frac{\sinh(\kappa(T - t))}{\sinh(\kappa T)}$, front-loaded with urgency $\kappa$, and varying $\lambda$ traces an efficient frontier of cost against risk.

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
6. **Decomposition and check**: the execution cost splits into delay cost $8,000 \times \$0.20 = \$1,600$ and spread plus impact after arrival $4,000 \times \$0.15 + 4,000 \times \$0.35 = \$2,000$.
   Check against Perold's definition: the paper portfolio gains $10,000 \times \$1.00 = \$10,000$ at $P_T$, the real one gains $4,000 \times \$0.65 + 4,000 \times \$0.45 - \$40 = \$4,360$, and the difference is $\$5,640$.

### Example 2: Estimating Market Impact via the Square-Root Law

A fund needs to execute $Q = 100,000$ shares of a stock over a single trading day (hypothetical inputs):
- Daily Volume: $V_{\text{ADV}} = 2,000,000$ shares.
- Annualized Volatility: $\sigma_{\text{ann}} = 30.0\%$.
- Daily Volatility: $\sigma_{\text{daily}} = \frac{0.30}{\sqrt{252}} = 0.01890$ ($1.89\%$).
- Proportionality constant: $Y = 0.60$.
- Stock Price: $\$50.00$.

1. **Participation Ratio**:
   $$\frac{Q}{V_{\text{ADV}}} = \frac{100,000}{2,000,000} = 0.05 \quad (5.0\% \text{ of ADV})$$
2. **Estimated Market Impact**:
   $$I = Y \cdot \sigma_{\text{daily}} \cdot \sqrt{\frac{Q}{V_{\text{ADV}}}} = 0.60 \times 0.01890 \times \sqrt{0.05}$$
   $$I = 0.011339 \times 0.2236 = 0.002535 \quad (25.35 \text{ bps})$$
3. **Dollar Cost of Impact**:
   $$\text{Total Order Notional} = 100,000 \times \$50.00 = \$5,000,000$$
   $$\text{Impact Cost} = \$5,000,000 \times 0.0025355 = \$12,677$$

Trading $5\%$ of daily volume incurs an expected price penalty of $25.4$ basis points ($\$12,677$).

### Example 3: Almgren-Chriss Trajectory

Sell $X = 1,000,000$ shares over $T = 5$ days in $N = 5$ daily slices (hypothetical inputs): price volatility $\sigma = 0.95$ dollars per share per $\sqrt{\text{day}}$, temporary impact $\eta = 2.5 \times 10^{-6}$, permanent impact $\gamma = 2.5 \times 10^{-7}$, risk aversion $\lambda = 10^{-6}$.
1. Adjusted temporary impact: $\tilde{\eta} = \eta - \frac{\gamma \tau}{2} = 2.375 \times 10^{-6}$ with $\tau = 1$ day.
2. $\tilde{\kappa}^2 = \frac{\lambda \sigma^2}{\tilde{\eta}} = 0.3800$, and the discrete urgency solves $\cosh(\kappa \tau) = 1 + \frac{1}{2}\tilde{\kappa}^2 \tau^2$, giving $\kappa = 0.6071$ per day.
3. Holdings $x_j = X \frac{\sinh(\kappa(T - t_j))}{\sinh(\kappa T)}$ at the end of days 0 to 5: $100\%$, $54.2\%$, $29.0\%$, $14.8\%$, $6.2\%$, $0\%$.

The trader sells $45.8\%$ on day 1 against the $20\%$ a day of TWAP, because risk aversion penalizes the variance of holding inventory; with $\lambda = 0$ the solution is exactly the straight-line TWAP schedule.
The script checks the closed form against a direct numerical minimization of the discrete objective.

### Example 4: Capacity Under Square-Root Costs

A strategy earns gross alpha $\alpha_0 = 4\%$ a year, and its cost drag is $1\%$ a year at $\$100\text{M}$, so $k = 0.01 / \sqrt{10^8} = 10^{-6}$ (hypothetical inputs).
- Net return falls to the $2\%$ hurdle at $A^* = (0.02 / 10^{-6})^2 = \$400\text{M}$.
- Net return reaches zero at $(0.04 / 10^{-6})^2 = \$1.6\text{bn}$.
- Net dollar profit peaks at $(0.04 / (1.5 \times 10^{-6}))^2 = \$711\text{M}$, with a $1.33\%$ net return and $\$9.48\text{M}$ a year of profit.

The manager's profit-maximizing size is far above the size that maximizes the investor's net return, which is one reason capacity is contested.

---

## Pitfalls

- **Assuming Zero Market Impact in Backtests**: Testing strategies with high turnover ($> 500\%$ annually) under flat zero-slippage assumptions, generating fantasy Sharpe ratios that turn negative in live execution.
- **Ignoring the Square-Root Non-Linearity**: Using a fixed per-share slippage model (e.g. $\$0.01$/share), massively understating impact for large block rebalances.
- **Underestimating Delay Cost**: Ignoring the time elapsed between alpha signal computation and order dispatch; in fast-moving markets, prices drift significantly before arrival.
- **Over-Aggressive Child Slicing**: Setting high POV participation rates, which raises impact and makes the order easier for other algorithms to detect and trade ahead of.
- **Neglecting Unfilled Order Opportunity Cost**: Evaluating execution algorithms solely by average fill price relative to arrival price, ignoring orders that failed to execute because the market ran away.

---

## Interview questions

> [!question]- mkt-sys-161 | Define Implementation Shortfall (Perold 1988).
> Implementation Shortfall is the difference in return between a theoretical paper portfolio executing instantly at decision prices and the actual realized portfolio executing in live markets.

> [!question]- mkt-sys-162 | State the primary components of Implementation Shortfall.
> The components are explicit fees (commissions, taxes), delay cost (price movement from decision to arrival), market impact and spread, and opportunity cost of unfilled shares.

> [!question]- mkt-sys-163 | What is the difference between temporary and permanent market impact?
> Temporary impact is a transitory price concession caused by immediate liquidity demand that decays as the book refills; permanent impact is the persistent price shift reflecting information content.

> [!question]- mkt-sys-164 | State the empirical square-root law of market impact.
> The average impact of a metaorder scales with daily volatility and the square root of its size relative to daily volume: I = Y * sigma_{daily} * sqrt(Q / V_{ADV}), with Y of order one (Toth et al. 2011).
> It is empirical: fitted exponents range from about 0.4 to 0.7, and Almgren et al. (2005) fit 0.6 for US equities.

> [!question]- mkt-sys-165 | Why does market impact exhibit square-root rather than linear scaling with order size?
> The mechanism is still debated.
> Toth et al. (2011) argue that latent supply and demand vanish linearly near the current price (a V-shaped latent order book), so absorbing a metaorder of size Q moves the price by an amount proportional to sqrt(Q).

> [!question]- mkt-sys-166 | What is opportunity cost in trade execution?
> The unrealized profit or avoided loss on shares that were never executed because limit prices were not reached before the market moved away or the order expired.

> [!question]- mkt-sys-167 | What is the trade-off in the Almgren-Chriss optimal execution model?
> The trade-off between market impact (trading fast causes high temporary impact) and market risk (trading slow leaves the position exposed to price volatility).
> They minimize E[cost] + lambda Var[cost]; the optimal holdings decay like sinh(kappa (T - t)) with kappa = sqrt(lambda sigma^2 / eta) in the continuous limit.

> [!question]- mkt-sys-168 | What is TWAP and when is it suitable?
> Time-Weighted Average Price divides orders into equal slices at uniform time intervals; suitable for liquid assets with stable volume or low-impact passive rebalancing.

> [!question]- mkt-sys-169 | What is VWAP and how does it account for intra-day liquidity?
> Volume-Weighted Average Price slices orders proportionally to historical intra-day volume curves (higher near the open and close, lower midday), so the fill tracks the day's VWAP benchmark.

> [!question]- mkt-sys-170 | What is Percentage of Volume (POV) algorithmic execution?
> An execution strategy that dynamically trades a fixed percentage (e.g. 5-10%) of actual real-time tape volume, adjusting speed automatically to live market liquidity.

> [!question]- mkt-sys-171 | What is the U-shaped intra-day volume profile in equity markets?
> Intraday volume in US equities is highest near the open and the close and lowest at midday, so a plot of volume by time of day looks like a U (Jain and Joh 1988 document the pattern for NYSE volume).

> [!question]- mkt-sys-172 | How does strategy turnover affect transaction cost drag?
> Higher portfolio turnover trades a multiple of portfolio AUM each year, multiplying cumulative market impact and explicit costs and rapidly consuming gross alpha.

> [!question]- mkt-sys-173 | Why does net strategy Sharpe ratio decay as AUM increases?
> Because dollar impact costs scale like AUM^{1.5} under the square-root law while gross alpha scales like AUM, so the cost drag in percent grows like sqrt(AUM) and compresses net returns.

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
> Short selling requires locating shares, paying borrow fees, and complying with the Regulation SHO Rule 201 price test.
> Under Rule 201 (as of November 2026), once a stock falls 10% or more from the prior close, short sales may not be executed at or below the national best bid for the rest of that day and the next (SEC Release 34-61595, 2010).

> [!question]- mkt-sys-183 | What is SEC Section 31 transaction fee?
> A fee under Section 31 of the Securities Exchange Act that exchanges and FINRA pay to the SEC on covered sales of securities; brokers pass it through to the selling customer.
> The SEC resets the rate each fiscal year to target its appropriation, so look up the current rate rather than memorizing one.

> [!question]- mkt-sys-184 | What is the half-spread cost formula?
> Half-spread cost = 0.5 * (Ask - Bid) per share, representing the immediate cost of crossing the spread to obtain liquidity.

> [!question]- mkt-sys-185 | How does daily volatility sigma_{daily} modulate market impact in the square-root law?
> Impact is measured in units of daily volatility: a given participation moves the price by a fixed number of daily standard deviations, so doubling sigma_{daily} doubles the expected impact in price terms.

> [!question]- mkt-sys-186 | What is liquidity consumption vs liquidity provision in portfolio execution?
> Consuming liquidity uses aggressive market orders that cross the spread, paying impact for certainty; providing liquidity posts passive limit orders, risking non-execution.

> [!question]- mkt-sys-187 | How does the bid-ask spread behave during market stress or earnings announcements?
> Spreads widen dramatically as market makers price in heightened adverse selection risk, multiplying execution costs for strategies attempting to trade during announcements.

> [!question]- mkt-sys-188 | What is Kyle's lambda (lambda_K)?
> Kyle's lambda measures price impact per unit of order flow: dP = lambda_K * Q; it reflects the degree of asymmetric information in the market.

> [!question]- mkt-sys-189 | Why does cross-sectional rebalancing at the market close minimize tracking error?
> Because index levels and fund NAVs are struck at official closing prices; trading in the closing auction fills at that same price, removing the intraday tracking difference.

> [!question]- mkt-sys-190 | What is the closing cross (auction) and how does it reduce market impact?
> The closing cross matches buy and sell interest at a single clearing price, so participants do not pay a bid-ask spread.
> Large one-sided imbalances still move the clearing price, so it reduces, not removes, impact.

> [!question]- mkt-sys-191 | What is the participation rate rule of thumb to avoid signaling market presence?
> There is no universal threshold; treat it as advice.
> Keep participation low enough that expected impact (Y sigma sqrt(Q/V)) and detectability are acceptable, and size the window from the impact model rather than from a fixed percentage.

> [!question]- mkt-sys-192 | How does turnover constraint in portfolio optimization prevent transaction cost ruin?
> Enforcing a maximum periodic turnover constraint or quadratic cost penalty restricts rebalancing to high-conviction alpha trades that comfortably exceed execution hurdles.

> [!question]- mkt-sys-262 | Under the square-root law with Y = 1, how far does trading 1% of daily volume move the price?
> About $0.1$ daily standard deviations, because sqrt(0.01) = 0.1.
> Toth et al. (2011) highlight this as a surprisingly large impact for a small order.

> [!question]- mkt-sys-263 | In the Almgren-Chriss example (X = 1,000,000, 5 days, kappa = 0.6071 per day), what fraction is sold on day 1, and why not 20%?
> About 45.8%, since holdings after day 1 are sinh(4 kappa)/sinh(5 kappa) = 54.2%.
> Risk aversion penalizes holding inventory while the price moves, so the schedule front-loads; with lambda = 0 it is exactly TWAP.

> [!question]- mkt-sys-264 | With net return alpha_0 - k sqrt(A), what AUM maximizes the manager's net dollar profit?
> A = (alpha_0 / (1.5 k))^2, which is 4/9 of the zero-net-return capacity (alpha_0 / k)^2.
> With alpha_0 = 4% and k = 10^-6, that is $711M against $1.6bn.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../code/mkt_sys_06_execution.py`](../code/mkt_sys_06_execution.py) prints and asserts every number on this page: implementation shortfall in exact decimal arithmetic and again as paper minus real portfolio value, square-root impact and its scaling ratios, the Almgren-Chriss closed form against a direct linear-system minimization, and capacity closed forms against a grid search.
- Related notes: [Market Impact Models](../../07-Market-Microstructure/06-Market-Impact-Models.md), [Optimal Execution: Almgren-Chriss](../../07-Market-Microstructure/07-Optimal-Execution-Almgren-Chriss.md), [Execution Algorithms and TCA](../../07-Market-Microstructure/08-Execution-Algorithms-and-TCA.md).

## Further reading

- Almgren, R., & Chriss, N. (2000). Optimal execution of portfolio transactions. *Journal of Risk*, 3(2), 5-39.
- Almgren, R., Thum, C., Hauptmann, E., & Li, H. (2005). Direct estimation of equity market impact. *Risk*, 18(7).
- Jain, P. C., & Joh, G.-H. (1988). The dependence between hourly prices and trading volume. *Journal of Financial and Quantitative Analysis*, 23(3), 269-283.
- Kyle, A. S. (1985). Continuous auctions and insider trading. *Econometrica*, 53(6), 1315-1335.
- Kissell, R. (2013). *The Science of Algorithmic Trading and Portfolio Management*. Academic Press.
- Perold, A. F. (1988). The implementation shortfall: Paper versus reality. *The Journal of Portfolio Management*, 14(3), 4-9.
- Toth, B., Lemperiere, Y., Deremble, C., de Lataillade, J., Kockelkoren, J., & Bouchaud, J.-P. (2011). Anomalous price impact and the critical nature of liquidity in financial markets. *Physical Review X*, 1, 021006.
