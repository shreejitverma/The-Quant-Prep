---
type: moc
title: "Trading Styles and Personas Index"
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
tags: [trading-styles, quant-prop, discretionary, cta, value-investing, moc]
---

# Trading Styles and Personas Index

The Trading Styles pillar defines the theoretical principles, execution workflows, and risk parameters of the four foundational market styles.
Rather than treating these schools as mutually exclusive, Markets Mastery OS teaches each style as a rigorous, self-contained discipline with distinct edge sources and failure modes.

---

## Learning Objectives

- Distinguish the sources of structural edge across high-frequency quant prop trading, discretionary tape reading, systematic trend-following, and value investing.
- Master the math and mental models of each discipline without mixing contradictory rules.
- Identify how discretionary order flow concepts (e.g. Volume Profile, VWAP) correspond directly to quantitative market microstructure models.
- Apply forensic accounting and reverse DCF valuation to protect against value traps and fraud.
- Design systematic risk budgeting and volatility targeting across multi-strategy portfolios.

---

## The Four Trading Styles

```
+-----------------------------------------------------------------------+
|                       THE FOUR TRADING PERSONAS                       |
+-----------------------------------------------------------------------+
|  1. QUANT PROP TRADING          |  2. DISCRETIONARY TRADING           |
|  - Edge: Structural latency,    |  - Edge: Pattern recognition,       |
|    adverse selection control,   |    order flow imbalance,            |
|    statistical mispricing       |    auction context, tape reading    |
|  - Horizon: Milliseconds to hrs |  - Horizon: Minutes to days         |
+---------------------------------+-------------------------------------+
|  3. SYSTEMATIC CTA / MACRO      |  4. VALUE & FUNDAMENTAL             |
|  - Edge: Behavioral momentum,   |  - Edge: Analytical rigor,          |
|    macro trend following,       |    mispriced cash flows,            |
|    volatility-targeted sizing   |    owner earnings, moats            |
|  - Horizon: Weeks to months     |  - Horizon: Months to years         |
+-----------------------------------------------------------------------+
```

---

### Style 1: Quantitative Prop Trading
- **Core Edge**: Statistical anomalies, co-integration in pairs trading, cross-venue latency arbitrage, and market making spread capture.
- **Microstructure Mechanics**: Order queue dynamics, adverse selection risk (trading against informed order flow), inventory risk management, and the Avellaneda-Stoikov market maker framework.
- **Execution**: Algorithmic execution, smart order routing (SOR), fee rebate optimization, and tick-level backtesting.
- **Foundations & Core Curriculum**:
  - [[16-Trading-and-Investing/07-Trading-Styles/Quant-Prop-Trading/01-Desk-Roles-and-Economics|01. Desk Roles, Economics, and PnL Decomposition]]
  - [[16-Trading-and-Investing/07-Trading-Styles/Quant-Prop-Trading/02-Fair-Value-and-Microprice|02. Fair Value, Microprice, and Order Flow Imbalance]]
  - [[16-Trading-and-Investing/07-Trading-Styles/Quant-Prop-Trading/03-Order-Flow-and-Adverse-Selection|03. Order Flow Dynamics, Glosten-Milgrom, and Adverse Selection]]
  - [[16-Trading-and-Investing/07-Trading-Styles/Quant-Prop-Trading/04-Inventory-Risk-and-Skew|04. Inventory Risk, Avellaneda-Stoikov, and Skew Optimization]]
  - [[16-Trading-and-Investing/07-Trading-Styles/Quant-Prop-Trading/05-Quant-and-Prop-Trading-Careers|05. Quantitative and Proprietary Trading Careers: Firm Models, Roles, Compensation, and Interviews]]
- **Lab Engine**: `lob_sim` (Limit Order Book matching) and `mm_quote` (Avellaneda-Stoikov market maker).

---

### Style 2: Discretionary Trading and Tape Reading
- **Core Edge**: Real-time order flow imbalances, market participant positioning, liquidity absorption at key inflection points, and structural auction dynamics.
- **Auction Market Theory**: Market Profile structures, Value Area High (VAH), Value Area Low (VAL), Point of Control (POC), Initial Balance (IB) extensions, and responsive versus initiative auction activity.
- **Volume Profile and VWAP**: Anchored Volume Weighted Average Price (AVWAP), standard deviation bands, volume nodes (High Volume Nodes vs Low Volume Nodes), and liquidity void fills.
- **Tape Reading**: Level 2 order book depth, Time and Sales tape speed, iceberg order detection, and spoofing/layering identification.
- **Foundations & Core Curriculum**:
  - [[16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/01-Retail-Base-Rates-and-Costs|01. Retail Base Rates, Transaction Friction, and Expectancy]]
  - [[16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/02-Position-Sizing-and-Ruin|02. Position Sizing, Volatility Targeting, and Risk of Ruin]]
  - [[16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/03-Stop-Logic-and-Trade-Management|03. Stop Logic, Trade Management, and Dynamic Invalidation]]
  - [[16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/04-Setup-Taxonomy-and-Evidence|04. Trade Setup Taxonomy, Evidence Grading, and Academic Verification]]
  - [[16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/05-Trading-Psychology-and-Performance|05. Trading Psychology, Emotional Regulation, and Peak Performance]]
  - [[16-Trading-and-Investing/07-Trading-Styles/Discretionary-Trading/06-Probability-and-Decision-Making|06. Probability, Cognitive Biases, and Decision-Making Under Uncertainty]]
- **Lab Engine**: `replay_chart` (Bar-by-bar tape reading and order execution) and `journal_stats` (Trade performance and tilt analytics).

---

### Style 3: Systematic CTA and Macro Trend Following
- **Core Edge**: Exploiting institutional behavioral under-reaction and delayed capital reallocation across global asset classes.
- **Signal Formulation**: Time-series momentum (absolute momentum), cross-sectional momentum (relative momentum), moving average crossovers, and breakout filters (Donchian channels).
- **Portfolio Construction**: Equal risk contribution, volatility targeting (scaling position sizes inversely to rolling realized volatility), and correlation diversification.
- **Statistical Rigor**: Mitigating backtest overfitting, Deflated Sharpe Ratio (Bailey-Lopéz de Prado), and walk-forward out-of-sample testing.
- **Pillar Curriculum**: [[16-Trading-and-Investing/60-Systems/_Index_Systems|Systematic Trading Systems Pillar (8 Notes, 256 Cards)]]
- **Lab Engine**: `overfit_trap` (Overfitting and multiple testing penalty calculator) and `port_alloc` (Risk parity allocator).

---

### Style 4: Value and Fundamental Investing
- **Core Edge**: Deep business analysis, forensic balance sheet auditing, economic moat assessment, and disciplined reverse DCF valuation.
- **Lineage**: Benjamin Graham (margin of safety), Warren Buffett (economic moats and pricing power), Charlie Munger (mental models and multidisciplinary thinking).
- **Forensic Accounting**: Beneish M-Score for earnings manipulation, Altman Z-Score for insolvency risk, and Sloan Accruals anomaly for cash flow quality.
- **Valuation Framework**: Reverse Discounted Cash Flow (DCF) to isolate the market's implied revenue growth rate, Return on Invested Capital (ROIC) versus Weighted Average Cost of Capital (WACC), and owner earnings calculation.
- **Lab Engine**: `quant_reverse_dcf.py` (Reverse DCF solver) and `quant_sector_benchmarker.py` (Sector peer comparative benchmarking).

---

## Navigation

- **Master Hub**: [[16-Trading-and-Investing/MARKETS_HUB|Markets Mastery OS Master Hub]]
- **Technical Analysis Pillar**: [[16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/_Index_Technical_Analysis|Technical Analysis and Price Action Index]]
- **Stock Research Database**: [[16-Trading-and-Investing/Investing/Stock Research/_Index_Stock Research|Global Stock Research Vault]]
- **Execution Microstructure**: [[16-Trading-and-Investing/08-Execution-Microstructure/_Index_Execution|Execution and Microstructure Index]]
