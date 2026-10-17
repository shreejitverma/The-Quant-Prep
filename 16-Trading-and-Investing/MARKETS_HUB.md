---
type: moc
title: "Markets Mastery OS - Master Hub"
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
tags: [trading, investing, markets, hub, moc]
---

# Markets Mastery OS

Markets Mastery OS is the interactive, practice-first learning and execution operating system for modern financial markets.
It bridges rigorous quantitative financial engineering with discretionary tape reading, systematic strategy research, and fundamental valuation.
Every concept in this curriculum is designed to lead directly to concrete drills, verifiable market simulation, and measurable execution skill.

---

## The Six Market Pillars

The curriculum spans six interconnected asset classes and market structures.
Each pillar contains theoretical foundations, institutional market mechanics, order flow dynamics, and quantitative models.

### 1. Equities and ETFs
- **Overview**: Microstructure, liquidity tiers, factor premia, auction mechanics, market internals, and ETF basket arbitrage.
- **Key Concepts**: Order book dynamics, market breadth, cross-sectional factor momentum, index rebalancing, creation/redemption mechanics.
- **Index**: [[16-Trading-and-Investing/01-Equities-and-ETFs/_Index_Equities|Equities and ETFs Index]]

### 2. Indian Markets
- **Overview**: NSE and BSE market architecture, cash equities, index derivatives (NIFTY 50, BANKNIFTY), SEBI regulatory frameworks, STT taxation, and settlement cycles (T+1).
- **Key Concepts**: Weekly option expirations, strike selection, margin rules, circuit breakers, auction sessions, open interest profiling.
- **Index**: [[16-Trading-and-Investing/02-Indian-Markets/_Index_Indian_Markets|Indian Markets Index]]

### 3. Options and Volatility
- **Overview**: Non-linear derivatives, Black-Scholes-Merton and local/stochastic volatility models, Greeks surfaces, volatility skews, and market maker inventory dynamics.
- **Key Concepts**: Delta, Gamma, Vega, Theta, Vanna, Volga, Gamma exposure (GEX), term structures, dispersion trading, variance swaps.
- **Index**: [[16-Trading-and-Investing/03-Options-and-Volatility/_Index_Options_Volatility|Options and Volatility Index]]

### 4. Macro, Rates, and Foreign Exchange
- **Overview**: Global macro regimes, sovereign yield curves, central bank monetary plumbing, FX crosses, and interest rate parity.
- **Key Concepts**: SOFR/LIBOR transition, yield curve inversion, repo markets, liquidity cycles, triangular FX arbitrage, carry trades.
- **Index**: [[16-Trading-and-Investing/04-Macro-Rates-FX/_Index_Macro_Rates_FX|Macro, Rates, and FX Index]]

### 5. Commodities and Physical Markets
- **Overview**: Physical delivery dynamics, storage economics, term structure geometry (contango vs backwardation), roll yields, and seasonal supply-demand shocks.
- **Key Concepts**: Crude oil crack spreads, gold/silver carry, agriculture weather cycles, basis risk, freight and convenience yield.
- **Index**: [[16-Trading-and-Investing/05-Commodities/_Index_Commodities|Commodities Index]]

### 6. Crypto and Digital Assets
- **Overview**: 24/7 continuous trading, perpetual futures, funding rate mechanics, decentralized automated market makers (AMMs), and on-chain liquidity.
- **Key Concepts**: Funding rate basis arbitrage, constant product AMMs, cross-venue latency arbitrage, liquidations and cascading deleveraging.
- **Index**: [[16-Trading-and-Investing/06-Crypto-and-Digital-Assets/_Index_Crypto|Crypto and Digital Assets Index]]

---

## The Four Trading Styles

Trading skill is domain-specific and style-governed.
Markets Mastery OS develops four distinct trading personas:

```
+-----------------------------------------------------------------------+
|                       MARKETS MASTERY OS STYLES                      |
+-----------------------------------------------------------------------+
|  1. QUANTITATIVE PROP TRADER    |  2. DISCRETIONARY TRADER            |
|  - Statistical arbitrage        |  - Tape reading & Order flow        |
|  - Market making & Inventory    |  - Auction market theory            |
|  - Latency & Execution routing  |  - Volume profile & VWAP            |
+---------------------------------+-------------------------------------+
|  3. SYSTEMATIC CTA / MACRO      |  4. VALUE & FUNDAMENTAL INVESTOR    |
|  - Time-series trend following  |  - Graham-Buffett-Munger lineage    |
|  - Cross-asset carry & momentum |  - Forensic accounting & DCF        |
|  - Volatility-targeted sizing   |  - Capital allocation & Moats       |
+-----------------------------------------------------------------------+
```

- **Detailed Framework**: [[16-Trading-and-Investing/07-Trading-Styles/_Index_Trading_Styles|Trading Styles and Personas Guide]]
- **Execution Microstructure**: [[16-Trading-and-Investing/08-Execution-Microstructure/_Index_Execution|Execution and Microstructure Index]]
- **Existing Research Suite**: [[16-Trading-and-Investing/Investing/Stock Research/_Index_Stock Research|Global Stock Research Vault]]

---

## Interactive Trading Lab

The Trading Lab provides eleven pure-Python standard-library simulation and analytics engines.
Each engine runs locally via the `./qp lab run <engine>` CLI or via the web dashboard at `http://localhost:8765/lab/` under `./qp serve`.

| Engine ID | Name | Core Focus | Command |
|---|---|---|---|
| `games` | Interview Trading Games | Mental arithmetic, market making game, Bayesian probability updates | `./qp lab run games` |
| `lob_sim` | Limit Order Book & Execution (TCA) Simulator | Price-time priority matching, queue position, Almgren-Chriss execution, slippage | `./qp lab run lob_sim` |
| `mm_quote` | Two-Sided Market Maker | Avellaneda-Stoikov inventory control, reservation price, skew | `./qp lab run mm_quote` |
| `pos_sizing` | Position Sizing and Ruin | Kelly criterion, optimal f, Monte Carlo drawdown risk | `./qp lab run pos_sizing` |
| `opt_desk` | Options Volatility Desk | Black-Scholes, Greeks calculation, PnL attribution, dynamic delta hedging | `./qp lab run opt_desk` |
| `replay_chart` | Interactive Chart Replay | Bar-by-bar tape reading, order entry, Murphy Brier score calibration | `./qp lab run replay_chart` |
| `overfit_trap` | Backtest Overfitting Trap | Multiple testing penalty, deflated Sharpe ratio, CSCV PBO | `./qp lab run overfit_trap` |
| `journal_stats` | Trade Journal Analytics | R-multiple expectancy, MAE/MFE, behavioral tilt detection | `./qp lab run journal_stats` |
| `fut_desk` | Futures and Basis Desk | Calendar spreads, cost-of-carry, roll yield tracking, cash-and-carry | `./qp lab run fut_desk` |
| `port_alloc` | Multi-Asset Portfolio Allocator | Risk parity, equal weighting, 60/40, all weather, macro stress | `./qp lab run port_alloc` |
| `event_study` | Market Crisis and Event Study | Abnormal returns, CAR, Patell Z-test, liquidity haircuts, pre-mortems | `./qp lab run event_study` |

---

## Deliberate Practice and Capital Gate

Knowledge without execution is incomplete.
To advance from simulation to real capital deployment, a trader must pass the verifiable capital gate:

1. **Drill Mastery**: Achieve at least 80% accuracy in the rapid-fire mental math, market making, and options Greeks drills in [[16-Trading-and-Investing/30-Drills/_Index_Drills|Trading Drills Bank]].
2. **Standardized Trade Journaling**: Log all simulated and paper trades with pre-trade entry triggers, stop loss invalidation levels, profit targets, and emotional state flags.
3. **The 100-Trade Sample Gate**:
   - Minimum sample size: 100 logged trades executed according to a documented playbook rule.
   - Profit Factor >= 1.50 across the full sample.
   - Maximum realized drawdown <= 10.0% of portfolio equity.
   - Trade rule adherence >= 95% (no revenge trades, no moved stops, no un-sized entries).
4. **Independent Post-Mortem Audit**: Periodic review of Maximum Adverse Excursion (MAE) and Maximum Favorable Excursion (MFE) to calibrate stop placement.

---

## Vault Navigation and Reference Links

- **Progression Dashboard**: [[16-Trading-and-Investing/STUDY_BOARD|Live Study Board & Progression Dashboard]]
- **Trading Styles**: [[16-Trading-and-Investing/07-Trading-Styles/_Index_Trading_Styles|Trading Styles and Personas Guide]]
- **Execution Microstructure**: [[16-Trading-and-Investing/08-Execution-Microstructure/_Index_Execution|Execution and Microstructure Index]]
- **Systematic Trading Systems**: [[16-Trading-and-Investing/60-Systems/_Index_Systems|Systematic Trading Systems Pillar]]
- **Historical Market Crises**: [[16-Trading-and-Investing/20-History-and-Events/_Index_History_Events|Historical Market Crises Index]]
- **Technical Analysis Pillar**: [[16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/_Index_Technical_Analysis|Technical Analysis and Price Action Index]]
- **Stock Research Database**: [[16-Trading-and-Investing/Investing/Stock Research/_Index_Stock Research|Global Stock Research Vault]]
- **Main Curriculum Dashboard**: [[00-Start-Here/Dashboard|Main Curriculum Dashboard]]
- **Fixed Income Syllabus**: [[06-Fixed-Income-and-Asset-Classes/README|Fixed Income Syllabus]]
- **Microstructure Syllabus**: [[07-Market-Microstructure/README|Market Microstructure]]
- **Risk and Trading Models**: [[11-Risk-and-Trading/README|Risk and Trading Models]]
- **Pricing and Risk Systems**: [[18-Pricing-and-Risk-Systems/README|Pricing and Risk Systems Architecture]]
- **Private Trade Journals (Gitignored)**: `16-Trading-and-Investing/Private/README.md`
