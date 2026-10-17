---
type: concept
title: "Desk Roles, Economics, and PnL Decomposition"
track: [quant-trader, quant-research]
tier: core
status: solid
est_hours: 1.5
tags: [trading-desk, market-making, prop-trading, pnl-attribution, microstructure, markouts]
prereqs: []
---

# Desk Roles, Economics, and PnL Decomposition

Trading desks at quantitative prop firms, market makers, and institutional hedge funds operate as highly specialized business units.
Each desk possesses a distinct mandate, capital structure, horizon, and edge mechanism.
Mastery of trading requires an exact understanding of desk economics, revenue streams, and the mathematical decomposition of profit and loss.

---

## TL;DR

Trading desks generate revenue through four distinct mechanisms: spread capture, structural arbitrage, risk warehousing, and directional forecasting.
Gross trading revenue is always eroded by adverse selection, queue slippage, exchange fees, and financing costs.
Quantitative performance measurement relies on post-trade markout curves and attribution rather than gross daily returns.
Every quantitative desk measures its edge through the fundamental PnL identity:
$$\text{Total PnL} = \text{Spread Capture} + \text{Inventory PnL} - \text{Adverse Selection} - \text{Exchange Fees} - \text{Financing}$$

---

## Learning objectives

- Distinguish the structural roles and revenue models of Market Makers (MM), Prop Traders (QT), Quantitative Researchers (QR), and Execution Desks.
- Formulate the mathematical PnL decomposition identity separating pure spread from inventory drift and adverse selection.
- Calculate post-trade markout curves at microsecond to second horizons to isolate toxic informed order flow.
- Evaluate desk risk-adjusted metrics including annualized Sharpe, Sortino, Calmar, and Return on Max Drawdown (RoMaD).
- Analyze exchange fee schedules, maker-taker pricing models, and asymmetric rebate economics.

---

## Core concepts

### 1. Desk Taxonomy and Operating Models

Institutional trading operations divide responsibilities into specialized functional seats:

1. **Market Making Desks (Automated Liquidity Provision)**:
   - Provide continuous two-sided quotes (bids and asks) in lit order books and alternative trading venues.
   - Primary edge: Fast cancellation upon signal arrival, queue priority, and collecting maker fee rebates.
   - Holding periods: Milliseconds to minutes.
   - Target Sharpe Ratio: Typically $> 4.0$, characterized by high win rates ($> 55\%$) and small average profits per trade.

2. **Proprietary Quantitative Trading (QT / Alpha Desks)**:
   - Deploy automated directional signals derived from statistical anomalies, cross-asset lead-lag relationships, and order flow imbalances.
   - Primary edge: Faster predictive feature extraction and optimal execution.
   - Holding periods: Intraday (minutes to hours) or multi-day (statistical arbitrage).
   - Target Sharpe Ratio: $1.5$ to $3.0$.

3. **Quantitative Research (QR)**:
   - Mathematical modelers who formulate hypothesis-driven predictive signals from market data.
   - Responsible for feature engineering, regularized estimation, cross-validation, and backtest deflated Sharpe calculation.
   - QR outputs the mathematical logic executed by QT engines.

4. **Execution Desks (Agency and Institutional TCA)**:
   - Execute large parent orders on behalf of internal portfolio managers or external institutional clients.
   - Goal: Minimize Implementation Shortfall relative to benchmarks such as Volume Weighted Average Price (VWAP) or Arrival Price.
   - Measure performance via Transaction Cost Analysis (TCA).

### 2. The Comprehensive PnL Attribution Identity

A market maker or prop trader's instantaneous profit and loss over a discrete session decomposes into five orthogonal terms:

$$\text{PnL}_{\text{total}} = \text{PnL}_{\text{spread}} + \text{PnL}_{\text{inv}} - \text{PnL}_{\text{adverse}} - \text{Fees}_{\text{exchange}} - \text{Cost}_{\text{funding}}$$

Where:

- **Spread Capture ($\text{PnL}_{\text{spread}}$)**:
  The theoretical half-spread earned on every executed transaction relative to the prevailing mid-price $S_t$:
  $$\text{PnL}_{\text{spread}} = \sum_{i=1}^{N_{\text{sells}}} (P_{i,\text{ask}} - S_{t_i}) \cdot Q_i + \sum_{j=1}^{N_{\text{buys}}} (S_{t_j} - P_{j,\text{bid}}) \cdot Q_j$$
- **Inventory PnL ($\text{PnL}_{\text{inv}}$)**:
  The mark-to-market gain or loss from holding a net non-zero position $q_t$ as the asset mid-price evolves:
  $$\text{PnL}_{\text{inv}} = \int_{0}^{T} q_t \, dS_t$$
- **Adverse Selection ($\text{PnL}_{\text{adverse}}$)**:
  The systematic price move against the desk immediately following an execution, caused by trading against informed counterparty flow:
  $$\text{PnL}_{\text{adverse}} = \sum_{k=1}^{N} Q_k \cdot \text{Dir}_k \cdot (S_{t_k + \tau} - S_{t_k})$$
  where $\text{Dir}_k = +1$ for a buy fill and $-1$ for a sell fill, evaluated at post-trade horizon $\tau$.
- **Exchange Fees ($\text{Fees}_{\text{exchange}}$)**:
  Net exchange access fees minus liquidity provider rebates across tiers.
- **Funding and Borrow ($\text{Cost}_{\text{funding}}$)**:
  Overnight financing charges (SOFR/Repo), margin interest, and short-stock hard-to-borrow fees.

### 3. Post-Trade Markout Curves

The markout curve is the primary diagnostic used by quantitative desks to detect whether their fills are toxic or profitable.
For any execution at price $P_{\text{fill}}$ and timestamp $t_0$, the markout at horizon $\tau$ is defined as:

$$\text{Markout}(\tau) = \text{Side} \cdot (S_{t_0 + \tau} - P_{\text{fill}})$$

Where $\text{Side} = +1$ if the desk bought, and $-1$ if the desk sold.

- **Healthy Passive Desk**:
  The markout drops initially due to local queue depletion, then rebounds as the mid-price mean-reverts, settling at a positive long-term spread.
- **Adversely Selected Desk (Toxic Fills)**:
  The markout drops continuously below zero across $10\text{ms}, 100\text{ms}, 1\text{s}$, and $10\text{s}$.
  This indicates the desk is systematically quoting in front of informed sweeps.

---

## Worked examples

### Example 1: Multi-Trade PnL Attribution

A high-frequency market-making desk completes three trades in a single minute on an asset starting at mid-price $S_0 = \$100.00$.
Exchange maker rebate is $\$0.0020$ per share, and taker fee is $\$0.0030$ per share.

1. **Trade 1 ($t = 10\text{s}$)**: Desk passive limit buy fills 1,000 shares at bid $\$99.98$ (prevailing mid $\$100.00$).
   - Mid immediately moves to $\$99.96$ at $t = 11\text{s}$ due to an informed institutional sweep.
   - Spread captured relative to arrival mid: $(\$100.00 - \$99.98) \times 1,000 = +\$20.00$.
   - Adverse selection at $1\text{s}$: $(\$99.96 - \$100.00) \times 1,000 = -\$40.00$.
   - Rebate earned: $1,000 \times \$0.0020 = +\$2.00$.

2. **Trade 2 ($t = 25\text{s}$)**: Desk passive limit sell fills 1,000 shares at ask $\$100.02$ (prevailing mid $\$100.00$).
   - Mid remains at $\$100.00$ at $t = 26\text{s}$ (uninformed noise trade).
   - Spread captured: $(\$100.02 - \$100.00) \times 1,000 = +\$20.00$.
   - Adverse selection at $1\text{s}$: $\$0.00$.
   - Rebate earned: $+\$2.00$.

3. **Trade 3 ($t = 40\text{s}$)**: Desk aggressively unloads net flat using a market sell of 1,000 shares at bid $\$99.95$ when mid is $\$99.97$.
   - Taker fee paid: $1,000 \times \$0.0030 = -\$3.00$.
   - Spread cost: $(\$99.95 - \$99.97) \times 1,000 = -\$20.00$.

**Net Desk Economics Calculation**:
- Gross Spread Capture: $+\$20.00 + \$20.00 - \$20.00 = +\$20.00$.
- Adverse Selection Loss: $-\$40.00$.
- Net Exchange Fees: $+\$2.00 + \$2.00 - \$3.00 = +\$1.00$.
- Inventory Mark-to-Market: Starting cash was $-\$99,980 + \$100,020 + \$99,950 = +\$99,990$.
- Initial inventory was 0, final inventory is 0.
- Net Realized PnL: $-\$19.00$.

### Example 2: Desk Risk Metrics and Capital Productivity

A prop trading desk operates with $\$5,000,000$ in allocated equity and $\$20,000,000$ in gross market value (GMV), implying $4\times$ leverage.
Over 252 trading days, the desk generates:
- Total net dollar profit: $\$1,500,000$ (30.0% Return on Equity).
- Daily return standard deviation: $\sigma_{\text{daily}} = 0.75\%$.
- Risk-free rate: $4.0\%$ per annum ($R_f / 252 = 0.01587\%$ daily).
- Maximum peak-to-trough realized drawdown: $\$250,000$ (5.0% on equity).
- Downside semi-deviation: $\sigma_{\text{down}} = 0.40\%$.

**Metrics Calculation**:
1. Annualized Mean Return:
   $$\mu_{\text{ann}} = \frac{\$1,500,000}{\$5,000,000} = 30.0\%$$
2. Annualized Volatility:
   $$\sigma_{\text{ann}} = 0.75\% \times \sqrt{252} = 11.905\%$$
3. Annualized Sharpe Ratio:
   $$\text{Sharpe} = \frac{30.0\% - 4.0\%}{11.905\%} = \frac{26.0\%}{11.905\%} = 2.184$$
4. Annualized Sortino Ratio:
   $$\sigma_{\text{down, ann}} = 0.40\% \times \sqrt{252} = 6.350\%$$
   $$\text{Sortino} = \frac{26.0\%}{6.350\%} = 4.094$$
5. Calmar Ratio / Return on Max Drawdown (RoMaD):
   $$\text{RoMaD} = \frac{30.0\%}{5.0\%} = 6.00$$

---

## Pitfalls

- **Confusing Gross Spread with Net Edge**:
  High quoted spread means nothing if toxic sweeps systematically incur adverse selection larger than half the spread.
- **Ignoring Maker-Taker Tier Sensitivity**:
  Firms often drop volume tiers at month-end; a reduction in rebate tier from 25 mils to 18 mils can turn an entire high-frequency strategy unprofitable.
- **Markout Window Myopia**:
  Measuring markouts only at $10\text{ms}$ hides latency arbitrageurs who route through parent exchanges with 200ms delays.
- **Unhedged Overnight Inventory**:
  Carrying non-zero inventory into market close introduces uncompensated gap risk that wipes out intraday spread gains.

---

## Interview questions

> [!question] mkt-pqt-001 | What are the primary revenue drivers of an automated market making desk?
> Market makers earn the bid-ask half-spread on paired transactions and collect exchange maker rebates.
> They maximize order turnover while minimizing inventory holding duration and adverse selection from informed trades.

> [!question] mkt-pqt-002 | State the fundamental quantitative PnL attribution identity.
> Total PnL = Spread Capture + Inventory PnL - Adverse Selection - Exchange Fees - Financing Costs.
> Every basis point of performance must be decomposed into these five components.

> [!question] mkt-pqt-003 | Define adverse selection in the context of limit order execution.
> Adverse selection occurs when a passive limit order is filled by a counterparty possessing superior near-term information.
> Immediately following the execution, the mid-price moves against the market maker's newly acquired inventory.

> [!question] mkt-pqt-004 | What is a post-trade markout curve and how is it calculated?
> A markout curve plots the signed difference between the mid-price at horizon t0 + tau and the execution price: Markout(tau) = Side * (Mid(t0 + tau) - FillPrice).
> It reveals whether fills capture positive spread or decay into toxic adverse losses over time.

> [!question] mkt-pqt-005 | How does maker-taker pricing differ from taker-maker (inverted) pricing?
> In maker-taker venues, liquidity providers receive a rebate for resting orders while liquidity takers pay a fee.
> In inverted venues, liquidity providers pay a fee to rest orders, while liquidity takers receive a rebate, attracting aggressive retail flow.

> [!question] mkt-pqt-006 | What is the economic rationale for quoting on inverted exchanges despite paying maker fees?
> Inverted exchanges attract uninformed, fee-sensitive retail order flow seeking taker rebates.
> The lower adverse selection on inverted venues often exceeds the maker fee paid, resulting in higher net PnL.

> [!question] mkt-pqt-007 | How is the annualized Sharpe ratio calculated from daily return statistics?
> Sharpe = (Annualized Mean Return - Risk Free Rate) / Annualized Volatility.
> In daily terms: Sharpe = ((Daily Mean - Rf_daily) / Daily Stdev) * sqrt(252).

> [!question] mkt-pqt-008 | Why is Sortino ratio preferred over Sharpe ratio for high-frequency market-making strategies?
> Market-making returns are positively skewed with frequent small gains and occasional large tail losses.
> Sortino penalizes only downside volatility below the minimum acceptable return, ignoring harmless upside variance.

> [!question] mkt-pqt-009 | What is the Calmar ratio and how is it related to Return on Max Drawdown (RoMaD)?
> Calmar ratio is the annualized rate of return divided by the absolute value of the maximum peak-to-trough drawdown over a specified period.
> It quantifies the return earned per unit of catastrophic capital risk.

> [!question] mkt-pqt-010 | What is the role of an Execution Desk compared to a Proprietary Trading Desk?
> An Execution Desk acts as an agent to execute client parent orders with minimal Implementation Shortfall against a benchmark.
> A Prop Desk risks firm principal capital to generate absolute alpha and assumes directional or inventory risk.

> [!question] mkt-pqt-011 | Why does high inventory turnover reduce risk for a market maker?
> Fast turnover minimizes the time window during which the desk is exposed to adverse directional market drift.
> The variance of price drift scales linearly with holding time t: Var(delta S) = sigma^2 * t.

> [!question] mkt-pqt-012 | What is queue priority and why do high-frequency desks invest heavily in low-latency hardware?
> In price-time priority books, orders at the same price level fill in the sequence they arrived.
> Desks with lower latency secure front-of-queue positions, increasing fill rates on favorable prices and canceling before adverse fills occur.

> [!question] mkt-pqt-013 | What is a toxic order flow sweep?
> A large aggressive order that crosses the spread and sweeps multiple price levels simultaneously across fragmented venues.
> Resting limit orders filled during a sweep suffer immediate, severe adverse selection as the price punches through them.

> [!question] mkt-pqt-014 | What are exchange access fee caps under US SEC Regulation NMS Rule 610?
> Rule 610 caps taker access fees on protected quotes at 30 mils ($0.0030) per share for securities priced at $1.00 or more.
> This constraint establishes an upper bound on exchange maker rebates.

> [!question] mkt-pqt-015 | How does a desk hedge residual inventory when the primary asset lacks immediate liquidity?
> The desk shorts or buys a highly correlated proxy instrument, such as an index ETF or front-month futures contract.
> The hedge ratio is determined by beta: Hedge Qty = -beta * Primary Qty * (Price_primary / Price_hedge).

> [!question] mkt-pqt-016 | What is basis risk in cross-asset proxy hedging?
> Basis risk is the variance of the spread between the primary asset and the hedging proxy.
> During market stress, historical correlations decouple, causing both legs of the hedged trade to lose money simultaneously.

> [!question] mkt-pqt-017 | Explain the concept of internal crossing on a multi-strategy desk.
> Matching offsetting buy and sell orders from different internal strategies without routing to an external exchange.
> Internal crossing captures the full bid-ask spread and saves exchange fees on both legs.

> [!question] mkt-pqt-018 | What is Payment for Order Flow (PFOF) and why do internalizers pay for retail orders?
> Wholesale market makers pay retail brokers cash rebates to route unexecuted retail client orders directly to them.
> Retail orders are small and non-directional, carrying virtually zero adverse selection risk and ensuring high spread capture.

> [!question] mkt-pqt-019 | What is latency floor / speed bump implementation and how does it affect market makers?
> An intentional delay (e.g. IEX 350-microsecond coil) applied to all incoming market orders.
> It allows resting market maker quotes pegged to external reference prices to update before stale quotes can be picked off by latency arbitrageurs.

> [!question] mkt-pqt-020 | How does a hard-to-borrow (HTB) fee impact short directional prop trading?
> Prime brokers charge an annualized borrow fee on short equity positions that are in short supply.
> A 25% HTB borrow rate creates an overnight hurdle cost that severely reduces net statistical arbitrage profits.

> [!question] mkt-pqt-021 | What is the difference between Gross Market Value (GMV) and Net Market Value (NMV)?
> GMV is the sum of the absolute value of all long and short positions: GMV = |Long| + |Short|.
> NMV is the directional net exposure: NMV = Long - Short.

> [!question] mkt-pqt-022 | Why do risk managers enforce GMV limits alongside NMV limits?
> Even with zero NMV (dollar neutrality), high GMV exposes the desk to liquidity crises, borrow recalls, and asymmetric margin shocks.
> Liquidity liquidation costs scale quadratically with gross book size.

> [!question] mkt-pqt-023 | What is a mark-to-market (MTM) margin call?
> A demand by a clearing broker or exchange for additional collateral when adverse price movements reduce account equity below maintenance margin requirements.
> Failure to satisfy an MTM call results in forced liquidation of desk positions at fire-sale prices.

> [!question] mkt-pqt-024 | What is capacity of a quantitative strategy?
> The maximum capital a strategy can deploy before market impact and slippage erode alpha below the cost of capital.
> High-frequency market-making strategies have high Sharpe ratios but strictly limited dollar capacity.

> [!question] mkt-pqt-025 | Explain the difference between primary and secondary market liquidity in ETFs.
> Primary liquidity occurs through Authorized Participants creating or redeeming ETF creation units directly with the issuer at NAV.
> Secondary liquidity is the continuous intraday trading of ETF shares on lit exchanges among market participants.

> [!question] mkt-pqt-026 | How do Authorized Participants (APs) keep ETF market prices aligned with NAV?
> If the ETF trades at a premium to NAV, APs buy underlying component stocks, create ETF shares, and sell them in the market.
> If the ETF trades at a discount, APs buy cheap ETF shares, redeem them for component stocks, and sell the components.

> [!question] mkt-pqt-027 | What is an iceberg order and how do market makers detect its presence?
> An order that displays only a small visible tranche while hiding the bulk of its volume in the exchange matching engine.
> Market makers detect icebergs when consecutive market orders exhaust the displayed bid/ask but the depth instantly replenishes at the identical price.

> [!question] mkt-pqt-028 | What is the bid-ask bounce effect and how does it distort return autocorrelation?
> Successive transactions bouncing between bid and ask prices create negative first-order serial correlation in observed price returns.
> Quantitative researchers must filter out bounce noise using mid-prices rather than transaction prices.

> [!question] mkt-pqt-029 | What is Transaction Cost Analysis (TCA) Implementation Shortfall?
> The difference between the paper return of a portfolio decided at time t0 and the actual realized return after all execution costs and delays.
> Implementation Shortfall = (Execution Cost + Delay Cost + Opportunity Cost + Fees).

> [!question] mkt-pqt-030 | What is a desk kill switch and what triggers it?
> An automated hardware or software breaker that immediately cancels all open resting orders and blocks new outbound order routing.
> It triggers when hard limits on loss thresholds, max position size, consecutive stale quotes, or exchange socket disconnects are breached.

> [!question] mkt-pqt-031 | Why does market maker profitability decline during volatility spikes despite wider spreads?
> Wider spreads are overwhelmed by severe adverse selection, violent inventory revaluation losses, and rapid correlation breakdown in hedging instruments.
> Volume sweeps easily breach inventory limits, forcing market makers to liquidate at the worst prices.

> [!question] mkt-pqt-032 | What is return on max drawdown (RoMaD) and why is it crucial for prop firms?
> RoMaD = Net Cumulative Return / Maximum Peak-to-Trough Drawdown.
> It measures capital efficiency relative to the survival boundary, ensuring traders do not blow past their mandatory capital stop.

---

## Further reading

- Glosten, L. R., & Milgrom, P. R. (1985). *Bid, ask and transaction prices in a specialist market with heterogeneously informed traders*. Journal of Financial Economics, 14(1), 71-100.
- Perold, A. F. (1988). *The implementation shortfall: Paper versus reality*. The Journal of Portfolio Management, 14(3), 4-9.
- Harris, L. (2003). *Trading and Exchanges: Market Microstructure for Practitioners*. Oxford University Press.
- Hasbrouck, J. (2007). *Empirical Market Microstructure: The Institutions, Economics, and Econometrics of Securities Trading*. Oxford University Press.
