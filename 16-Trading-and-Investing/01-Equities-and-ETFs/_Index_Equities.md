---
type: moc
title: "Equities and ETFs Pillar Index"
track: [quant-trader, quant-research]
tier: core
status: solid
tags: [equities, etfs, stock-market, factors, internals, moc]
---

# Equities and ETFs Pillar Index

The Equities and ETFs pillar covers the full lifecycle of equity trading across liquid global markets.
It spans microstructure foundations, opening and closing cross auctions, cross-sectional factor premia, market breadth internals, and ETF basket arbitrage mechanics.

---

## Learning Objectives

- Understand the auction microstructure of the primary exchanges (NYSE, NASDAQ) and alternative trading systems (ATS / dark pools).
- Master market breadth internals including Advance-Decline volume, Tick indices, and Net New Highs/Lows.
- Deconstruct the multi-factor equity model across Value, Momentum, Quality, Size, and Low Volatility.
- Analyze the creation and redemption arbitrage mechanism governing authorized participants (APs) in ETFs.
- Execute earnings announcement drift and event-driven catalyst strategies.

---

## Core Topics

### 1. Market Architecture and Microstructure
- **Opening and Closing Auctions**: Mechanics of the NYSE Designated Market Maker (DMM) auction, NASDAQ Closing Cross, continuous trading transitions, and Market-on-Close (MOC) order flow.
- **Off-Exchange Liquidity**: Dark pools, Internalizers, Single-Dealer Platforms (SDPs), and retail order routing under Reg NMS Rule 605 and Rule 606.
- **Tick Size and Sub-Penny Regimes**: Impact of tick size constraints, tick-constrained stocks, maker-taker versus inverted fee schedules.

### 2. Market Internals and Breadth
- **NYSE Tick Index ($TICK)**: Measuring real-time market sentiment via sequential upticks versus downticks across all listed securities.
- **Advance-Decline Line ($ADLine)**: Cumulative breadth analysis to identify divergences between cap-weighted indices (e.g. S&P 500) and equal-weighted market participation.
- **Arms Index (TRIN)**: Ratio of advancing/declining stocks to advancing/declining volume as an indicator of aggressive institutional buying or selling pressure.

### 3. Factor Premia and Cross-Sectional Alpha
- **Fama-French Multi-Factor Extensions**: Size (SMB), Value (HML), Profitability (RMW), Investment (CMA), and Momentum (UMD).
- **Residual Momentum**: Isolating idiosyncratic momentum from market and factor beta to reduce crash risk.
- **Short Interest and Crowding**: Days-to-cover, cost of borrow, short-squeeze mechanics, and institutional loan market dynamics.

### 4. ETF Mechanics and Arbitrage
- **Creation and Redemption Mechanism**: How Authorized Participants (APs) keep ETF market prices tightly pegged to the Net Asset Value (NAV) of the underlying basket.
- **Tracking Error and Premium/Discount Dynamics**: Sources of tracking discrepancies including illiquidity, cash drag, management fees, and international market timezone mismatches.
- **Fixed Income and Leveraged ETF Mechanics**: Volatility decay in leveraged ETFs due to daily geometric compounding, and NAV pricing challenges in illiquid underlying bond baskets.

---

## Trading Lab Engines

- `lob_sim`: Limit order book matching engine for simulated stock execution with realistic slippage.
- `event_study`: Pre/post earnings announcement drift calculator with abnormal return tracking.

---

## Navigation

- **Master Hub**: [[16-Trading-and-Investing/MARKETS_HUB|Markets Mastery OS Master Hub]]
- **Stock Research Database**: [[16-Trading-and-Investing/Investing/Stock Research/_Index_Stock Research|100-Stock Research Vault]]
- **Execution Microstructure**: [[16-Trading-and-Investing/08-Execution-Microstructure/_Index_Execution|Execution and Order Routing]]
