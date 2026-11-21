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
Gross trading revenue is eroded by adverse selection, queue slippage, exchange fees, and financing costs.
Quantitative performance measurement relies on post-trade markout curves and attribution rather than gross daily returns.
Mark-to-market PnL splits exactly into spread capture, inventory PnL, net fees and financing:
$$\text{Total PnL} = \text{Spread Capture} + \text{Inventory PnL} + \text{Net Rebates and Fees} - \text{Financing}$$
Adverse selection is not a separate term: it is the part of inventory PnL earned in a short window $\tau$ after each fill, so subtracting it on top of inventory PnL would count it twice.

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
   - Return profile: many small gains per trade, with the risk concentrated in adverse selection and inventory shocks.

2. **Proprietary Quantitative Trading (QT / Alpha Desks)**:
   - Deploy automated directional signals derived from statistical anomalies, cross-asset lead-lag relationships, and order flow imbalances.
   - Primary edge: Faster predictive feature extraction and optimal execution.
   - Holding periods: Intraday (minutes to hours) or multi-day (statistical arbitrage).
   - Longer holding periods mean fewer independent bets per year, and by the fundamental law of active management (Grinold 1989, $IR \approx IC \sqrt{\text{breadth}}$) fewer bets give a lower information ratio for the same per-bet skill.

3. **Quantitative Research (QR)**:
   - Mathematical modelers who formulate hypothesis-driven predictive signals from market data.
   - Responsible for feature engineering, regularized estimation, cross-validation, and backtest deflated Sharpe calculation.
   - QR outputs the mathematical logic executed by QT engines.

4. **Execution Desks (Agency and Institutional TCA)**:
   - Execute large parent orders on behalf of internal portfolio managers or external institutional clients.
   - Goal: Minimize Implementation Shortfall relative to benchmarks such as Volume Weighted Average Price (VWAP) or Arrival Price.
   - Measure performance via Transaction Cost Analysis (TCA).

### 2. The Comprehensive PnL Attribution Identity

Start a session flat with cash $X_0 = 0$ and inventory $q_0 = 0$.
Fill $i$ has signed size $n_i$ ($+$ for a buy, $-$ for a sell), price $P_i$ and prevailing mid $S_{t_i}$.
Mark-to-market PnL at the end of the session, $X_T + q_T S_T$, splits exactly into:

$$\text{PnL}_{\text{total}} = \text{PnL}_{\text{spread}} + \text{PnL}_{\text{inv}} + \text{Rebates} - \text{Fees} - \text{Cost}_{\text{funding}}$$

Where:

- **Spread Capture ($\text{PnL}_{\text{spread}}$)**:
  The edge of each fill relative to the mid at the moment of the fill, positive for a passive fill and negative for an aggressive one:
  $$\text{PnL}_{\text{spread}} = \sum_{i} n_i \, (S_{t_i} - P_i)$$
- **Inventory PnL ($\text{PnL}_{\text{inv}}$)**:
  The mark-to-market gain or loss from holding a net non-zero position $q_t$ as the mid-price evolves:
  $$\text{PnL}_{\text{inv}} = \int_{0}^{T} q_t \, dS_t = \sum_{i} n_i \, (S_T - S_{t_i})$$
- **Adverse Selection (inside inventory PnL)**:
  Split each fill's inventory PnL at a post-trade horizon $\tau$:
  $$\text{PnL}_{\text{inv}} = \underbrace{\sum_{i} n_i \, (S_{t_i + \tau} - S_{t_i})}_{-\text{Adverse Selection}(\tau)} + \underbrace{\sum_{i} n_i \, (S_T - S_{t_i + \tau})}_{\text{later drift}}$$
  The first sum is the mid-to-mid adverse selection component; it is negative when the desk trades against informed flow.
  Adding each fill's spread capture $n_i (S_{t_i} - P_i)$ to its adverse selection component gives the fill-price markout of Section 3.
  Reporting adverse selection as a separate cost is fine only if the later drift is reported next to it, otherwise the same mid moves are counted twice.
- **Rebates and Fees**:
  Exchange access fees paid on aggressive fills and liquidity rebates earned on passive fills.
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

A high-frequency market-making desk completes three trades in a single minute on an asset starting at mid-price $S_0 = \$100.00$ (all inputs hypothetical).
Exchange maker rebate is $\$0.0020$ per share, and taker fee is $\$0.0030$ per share.
The position is marked at $t = 40\text{s}$, immediately after Trade 3, at the $\$99.97$ mid.

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

3. **Trade 3 ($t = 40\text{s}$)**: Desk sends an aggressive market sell of 1,000 shares at bid $\$99.95$ when mid is $\$99.97$.
   - Trades 1 and 2 already left the desk flat, so this sell does not flatten anything; it opens a 1,000-share short.
   - Taker fee paid: $1,000 \times \$0.0030 = -\$3.00$.
   - Spread cost: $(\$99.95 - \$99.97) \times 1,000 = -\$20.00$.

**Net Desk Economics Calculation**:
- Gross Spread Capture: $+\$20.00 + \$20.00 - \$20.00 = +\$20.00$.
- Net Exchange Fees: $+\$2.00 + \$2.00 - \$3.00 = +\$1.00$.
- Inventory Drift: the long 1,000 shares was held from mid $\$100.00$ (Trade 1) to mid $\$100.00$ (Trade 2), so $1,000 \times (\$100.00 - \$100.00) = \$0.00$.
- Adverse Selection split of that $\$0.00$ at $\tau = 1\text{s}$: the one-second adverse selection components are $-\$40.00$ (Trade 1), $\$0.00$ (Trade 2) and $\$0.00$ (Trade 3, marked at once), and the later drift is $+1,000 \times (\$99.97 - \$99.96) - 1,000 \times (\$99.97 - \$100.00) = +\$10.00 + \$30.00 = +\$40.00$.
  The $-\$40.00$ of adverse selection reversed before the position was closed, so here it is a toxicity diagnostic, not a realized loss.
  Adding each fill's spread capture gives the one-second fill-price markouts of Section 3: $-\$20.00$ (Trade 1), $+\$20.00$ (Trade 2) and $-\$20.00$ (Trade 3).
- Cash from trades: $-\$99,980 + \$100,020 + \$99,950 = +\$99,990$.
- Inventory: initial 0, final $0 + 1,000 - 1,000 - 1,000 = -1,000$ shares.
- Mark-to-Market PnL at the $\$99.97$ mid: $+\$99,990 - 1,000 \times \$99.97 + \$1.00 = +\$21.00$.
- Check: spread capture plus inventory drift plus fees is $+\$20.00 + \$0.00 + \$1.00 = +\$21.00$.
- The round trip of Trades 1 and 2 locked in $+\$40.00$ of cash plus $\$4.00$ of rebates, $+\$44.00$; the open short is marked at $-\$20.00 - \$3.00 = -\$23.00$ and carries all of the remaining risk ($\$44.00 - \$23.00 = \$21.00$).

### Example 2: Desk Risk Metrics and Capital Productivity

A prop trading desk (hypothetical inputs) operates with $\$5,000,000$ in allocated equity and $\$20,000,000$ in gross market value (GMV), implying $4\times$ leverage.
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
   $$\sigma_{\text{ann}} = 0.75\% \times \sqrt{252} = 11.906\%$$
3. Annualized Sharpe Ratio:
   $$\text{Sharpe} = \frac{30.0\% - 4.0\%}{11.906\%} = \frac{26.0\%}{11.906\%} = 2.184$$
4. Annualized Sortino Ratio (excess return over the risk-free rate as the minimum acceptable return):
   $$\sigma_{\text{down, ann}} = 0.40\% \times \sqrt{252} = 6.350\%$$
   $$\text{Sortino} = \frac{26.0\%}{6.350\%} = 4.095$$
5. Calmar Ratio / Return on Max Drawdown (RoMaD):
   $$\text{RoMaD} = \frac{30.0\%}{5.0\%} = 6.00$$

---

## Pitfalls

- **Confusing Gross Spread with Net Edge**:
  High quoted spread means nothing if toxic sweeps systematically incur adverse selection larger than half the spread.
- **Ignoring Maker-Taker Tier Sensitivity**:
  Exchange rebates are tiered by monthly volume, so missing a tier cuts the rebate on every passive share; when the rebate is a large share of the net edge per share, a tier change alone can turn a strategy unprofitable.
- **Markout Window Myopia**:
  Measuring markouts at a single short horizon can hide toxicity that only shows up seconds later, or flag as toxic a fill whose markout reverses; look at the whole markout curve.
- **Unhedged Overnight Inventory**:
  Carrying non-zero inventory into market close introduces uncompensated gap risk that wipes out intraday spread gains.

---

## Interview questions

> [!question]- mkt-pqt-001 | What are the primary revenue drivers of an automated market making desk?
> Market makers earn about half the spread per fill (the full spread on a round trip that buys at the bid and sells at the ask) and collect exchange maker rebates.
> They aim for high turnover with short inventory holding times and little adverse selection from informed trades.

> [!question]- mkt-pqt-002 | State the fundamental quantitative PnL attribution identity.
> Total PnL = Spread Capture + Inventory PnL + Rebates - Fees - Financing, where spread capture is sum of n_i * (mid at fill - fill price) and inventory PnL is the integral of q dS.
> Adverse selection is the part of inventory PnL earned in the first tau after each fill, so it is reported inside inventory PnL (next to the later drift), not subtracted a second time.

> [!question]- mkt-pqt-003 | Define adverse selection in the context of limit order execution.
> Adverse selection occurs when a passive limit order is filled by a counterparty possessing superior near-term information.
> Immediately following the execution, the mid-price moves against the market maker's newly acquired inventory.

> [!question]- mkt-pqt-004 | What is a post-trade markout curve and how is it calculated?
> A markout curve plots the signed difference between the mid-price at horizon t0 + tau and the execution price: Markout(tau) = Side * (Mid(t0 + tau) - FillPrice).
> It reveals whether fills capture positive spread or decay into toxic adverse losses over time.

> [!question]- mkt-pqt-005 | How does maker-taker pricing differ from taker-maker (inverted) pricing?
> In maker-taker venues, liquidity providers receive a rebate for resting orders while liquidity takers pay a fee.
> In inverted venues, liquidity providers pay a fee to rest orders, while liquidity takers receive a rebate, which draws fee-sensitive takers and keeps resting queues shorter.

> [!question]- mkt-pqt-006 | What is the economic rationale for quoting on inverted exchanges despite paying maker fees?
> Queue position: because posting costs a fee instead of earning a rebate, queues on inverted venues are shorter, so a resting order fills sooner and more often.
> The trade-off is adverse selection: Battalio, Corwin and Jennings (2016, Journal of Finance) found that limit orders routed to high-rebate venues had lower fill rates and worse execution quality, so paying for priority can be worth more than the rebate given up.

> [!question]- mkt-pqt-007 | How is the annualized Sharpe ratio calculated from daily return statistics?
> Sharpe = (Annualized Mean Return - Risk Free Rate) / Annualized Volatility.
> In daily terms: Sharpe = ((Daily Mean - Rf_daily) / Daily Stdev) * sqrt(252).

> [!question]- mkt-pqt-008 | Why do desks report the Sortino ratio next to the Sharpe ratio for market-making strategies?
> Sortino divides excess return by downside deviation below a minimum acceptable return, so upside variance does not count as risk.
> Market-making returns are often negatively skewed (frequent small gains, occasional large losses), and neither ratio captures that tail fully, so desks also track maximum drawdown and the worst days.

> [!question]- mkt-pqt-009 | What is the Calmar ratio and how is it related to Return on Max Drawdown (RoMaD)?
> Calmar ratio is the annualized rate of return divided by the absolute value of the maximum peak-to-trough drawdown over a specified period.
> It quantifies the return earned per unit of catastrophic capital risk.

> [!question]- mkt-pqt-010 | What is the role of an Execution Desk compared to a Proprietary Trading Desk?
> An Execution Desk acts as an agent to execute client parent orders with minimal Implementation Shortfall against a benchmark.
> A Prop Desk risks firm principal capital to generate absolute alpha and assumes directional or inventory risk.

> [!question]- mkt-pqt-011 | Why does high inventory turnover reduce risk for a market maker?
> Fast turnover minimizes the time window during which the desk is exposed to adverse directional market drift.
> The variance of price drift scales linearly with holding time t: Var(delta S) = sigma^2 * t.

> [!question]- mkt-pqt-012 | What is queue priority and why do high-frequency desks invest heavily in low-latency hardware?
> In price-time priority books, orders at the same price level fill in the sequence they arrived.
> Desks with lower latency secure front-of-queue positions, increasing fill rates on favorable prices and canceling before adverse fills occur.

> [!question]- mkt-pqt-013 | What is a toxic order flow sweep?
> A large aggressive order that crosses the spread and sweeps multiple price levels simultaneously across fragmented venues.
> Resting limit orders filled during a sweep are adversely selected: the price moves through them right after the fill.

> [!question]- mkt-pqt-014 | What are exchange access fee caps under US SEC Regulation NMS Rule 610?
> As of November 2026, Rule 610(c) caps the fee for accessing a protected quotation at $0.003 (30 mils) per share for NMS stocks priced at $1.00 or more.
> The SEC's September 2024 amendments (Release 34-101070) cut the cap to $0.001 per share, but SEC Release 34-105656 (June 11, 2026) extended the compliance exemption to the first business day of November 2027.
> Because rebates are funded from access fees, the cap also bounds maker rebates in practice.

> [!question]- mkt-pqt-015 | How does a desk hedge residual inventory when the primary asset lacks immediate liquidity?
> The desk shorts or buys a highly correlated proxy instrument, such as an index ETF or front-month futures contract.
> The hedge ratio is determined by beta: Hedge Qty = -beta * Primary Qty * (Price_primary / Price_hedge).

> [!question]- mkt-pqt-016 | What is basis risk in cross-asset proxy hedging?
> Basis risk is the variance of the spread between the primary asset and the hedging proxy.
> During market stress, historical correlations can break down, and both legs of the hedged trade can lose money at once.

> [!question]- mkt-pqt-017 | Explain the concept of internal crossing on a multi-strategy desk.
> Matching offsetting buy and sell orders from different internal strategies without routing to an external exchange.
> Crossing at the mid saves each side the half-spread it would pay to trade aggressively, and saves exchange fees on both legs.

> [!question]- mkt-pqt-018 | What is Payment for Order Flow (PFOF) and why do internalizers pay for retail orders?
> Wholesale market makers pay retail brokers cash rebates to route unexecuted retail client orders directly to them.
> Retail orders are small and, on average, less informed about short-horizon price moves than institutional or proprietary flow, so filling them carries less adverse selection.

> [!question]- mkt-pqt-019 | What is latency floor / speed bump implementation and how does it affect market makers?
> An intentional delay on inbound messages; IEX's is 350 microseconds, produced by coiled fiber between its point of presence and matching engine, and it applies to cancels as well as orders.
> IEX reprices its own pegged orders from market data that does not pass through the delay, so those pegged orders move before a latency arbitrageur's order arrives; it does not let outside market makers cancel faster.

> [!question]- mkt-pqt-020 | How does a hard-to-borrow (HTB) fee impact short directional prop trading?
> Prime brokers charge an annualized borrow fee on short equity positions that are in short supply.
> A hypothetical 25% annual borrow rate is a carrying cost that the short's expected return must exceed before the trade makes money.

> [!question]- mkt-pqt-021 | What is the difference between Gross Market Value (GMV) and Net Market Value (NMV)?
> GMV is the sum of the absolute value of all long and short positions: GMV = |Long| + |Short|.
> NMV is the directional net exposure: NMV = Long - Short.

> [!question]- mkt-pqt-022 | Why do risk managers enforce GMV limits alongside NMV limits?
> Even with zero NMV (dollar neutrality), high GMV exposes the desk to liquidity crises, borrow recalls, and asymmetric margin shocks.
> Liquidation cost grows faster than linearly in gross size: with square-root impact the total cost of liquidating a position scales as size to the power 1.5.

> [!question]- mkt-pqt-023 | What is a mark-to-market (MTM) margin call?
> A demand by a clearing broker or exchange for additional collateral when adverse price movements reduce account equity below maintenance margin requirements.
> Failure to satisfy an MTM call can lead to forced liquidation of desk positions, often at unfavourable prices.

> [!question]- mkt-pqt-024 | What is capacity of a quantitative strategy?
> The maximum capital a strategy can deploy before market impact and slippage erode alpha below the cost of capital.
> High-frequency market-making strategies often have high Sharpe ratios but limited dollar capacity.

> [!question]- mkt-pqt-025 | Explain the difference between primary and secondary market liquidity in ETFs.
> Primary liquidity occurs through Authorized Participants creating or redeeming ETF creation units directly with the issuer at NAV.
> Secondary liquidity is the continuous intraday trading of ETF shares on lit exchanges among market participants.

> [!question]- mkt-pqt-026 | How do Authorized Participants (APs) keep ETF market prices aligned with NAV?
> If the ETF trades at a premium to NAV, APs buy underlying component stocks, create ETF shares, and sell them in the market.
> If the ETF trades at a discount, APs buy cheap ETF shares, redeem them for component stocks, and sell the components.

> [!question]- mkt-pqt-027 | What is an iceberg order and how do market makers detect its presence?
> An order that displays only a small visible tranche while hiding the bulk of its volume in the exchange matching engine.
> Market makers detect icebergs when consecutive market orders exhaust the displayed bid/ask but the depth instantly replenishes at the identical price.

> [!question]- mkt-pqt-028 | What is the bid-ask bounce effect and how does it distort return autocorrelation?
> Successive transactions bouncing between bid and ask prices create negative first-order serial correlation in observed price returns.
> Researchers commonly remove bounce noise by using mid-prices rather than transaction prices.

> [!question]- mkt-pqt-029 | What is Transaction Cost Analysis (TCA) Implementation Shortfall?
> The difference between the paper return of a portfolio decided at time t0 and the actual realized return after all execution costs and delays.
> Implementation Shortfall = (Execution Cost + Delay Cost + Opportunity Cost + Fees).

> [!question]- mkt-pqt-030 | What is a desk kill switch and what triggers it?
> An automated hardware or software breaker that immediately cancels all open resting orders and blocks new outbound order routing.
> It triggers when hard limits on loss thresholds, max position size, consecutive stale quotes, or exchange socket disconnects are breached.

> [!question]- mkt-pqt-031 | When does market maker profitability decline during volatility spikes despite wider spreads?
> Only when adverse selection, inventory revaluation losses and hedge breakdowns outweigh the wider spreads and higher volume; sweeps that breach inventory limits and force liquidation add to the losses.
> It need not decline: Virtu Financial reported a record first quarter of 2020 and attributed it to heightened volatility, bid-ask spreads and trading volumes (Form 8-K, May 2020).

> [!question]- mkt-pqt-032 | What is return on max drawdown (RoMaD) and why is it crucial for prop firms?
> RoMaD = Net Cumulative Return / Maximum Peak-to-Trough Drawdown.
> It measures return relative to the worst loss the trader actually took, which a prop firm compares with the trader's capital stop.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_pqt_01_desk_economics.py`](../../code/mkt_pqt_01_desk_economics.py) prints and asserts every number on this page: Example 1 PnL from a cash-and-inventory ledger against the attribution terms computed from the mid path, the attribution identity on 2,000 random sessions, and the Example 2 ratios in exact decimal arithmetic with the square-root-of-time scaling checked by a seeded simulation within five standard errors.
- Related notes: [Fair Value and Microprice](02-Fair-Value-and-Microprice.md), [Order Flow and Adverse Selection](03-Order-Flow-and-Adverse-Selection.md), [Inventory Risk and Skew](04-Inventory-Risk-and-Skew.md).

## Further reading

- Battalio, R., Corwin, S. A., & Jennings, R. (2016). *Can brokers have it all? On the relation between make-take fees and limit order execution quality*. The Journal of Finance, 71(5).
- Grinold, R. C. (1989). *The fundamental law of active management*. The Journal of Portfolio Management, 15(3), 30-37.
- Virtu Financial, Inc. (2020). Form 8-K, Exhibit 99.1, first quarter 2020 results press release, May 2020.
- Securities and Exchange Commission (2026). *Order granting temporary exemptive relief from compliance with Rule 600(b)(89)(i)(F), Rule 610(c) and Rule 612 of Regulation NMS, as amended*. Release No. 34-105656, June 11, 2026.
- Glosten, L. R., & Milgrom, P. R. (1985). *Bid, ask and transaction prices in a specialist market with heterogeneously informed traders*. Journal of Financial Economics, 14(1), 71-100.
- Perold, A. F. (1988). *The implementation shortfall: Paper versus reality*. The Journal of Portfolio Management, 14(3), 4-9.
- Harris, L. (2003). *Trading and Exchanges: Market Microstructure for Practitioners*. Oxford University Press.
- Hasbrouck, J. (2007). *Empirical Market Microstructure: The Institutions, Economics, and Econometrics of Securities Trading*. Oxford University Press.
