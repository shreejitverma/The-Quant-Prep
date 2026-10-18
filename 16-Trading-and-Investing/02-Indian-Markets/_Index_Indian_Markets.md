---
type: moc
title: "Indian Markets Pillar Index"
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
tags: [indian-markets, nse, bse, nifty, banknifty, options, sebi, moc]
---

# Indian Markets Pillar Index

The Indian Markets pillar covers the complete microstructure, derivatives architecture, and regulatory framework of the National Stock Exchange of India (NSE) and Bombay Stock Exchange (BSE).
It combines cash equity execution with high-volume index and stock derivatives, addressing structural peculiarities such as weekly expirations, peak margin rules, and Securities Transaction Tax (STT).

---

## Learning Objectives

- Master the exchange trading architecture of NSE and BSE, including tick-by-tick (TBT) feeds, co-location facilities, and the NEAT trading system.
- Understand the mechanics of Indian cash equity settlement, including T+1 rolling settlement and optional same-day T+0 settlement cycles.
- Analyze index derivatives across NIFTY 50, BANKNIFTY, FINNIFTY, and MIDCPNIFTY.
- Deconstruct the transaction friction structure: Securities Transaction Tax (STT), Goods and Services Tax (GST), exchange turnover charges, SEBI turnover fees, and stamp duty.
- Utilize Open Interest (OI) profiling, Put-Call Ratio (PCR), and Max Pain models for directional and non-directional execution.
- Navigate SEBI regulatory mandates, including peak margin reporting, circuit breakers, and Additional Surveillance Measures (ASM / GSM).

---

## Core Topics

### 1. Market Architecture and Microstructure
- **Exchange Infrastructure**: NSE NEAT and BSE BOLT systems, multicast market data (TBT), co-location facilities at BKC Mumbai, and sponsored direct market access (DMA).
- **Trading Hours and Sessions**: Pre-open auction session (09:00 to 09:15 IST) with equilibrium price determination, continuous trading (09:15 to 15:30 IST), and post-close session (15:40 to 16:00 IST).
- **Circuit Breakers and Price Bands**: Nationwide market-wide index circuit breakers (10%, 15%, 20%) with trading halts, individual stock dynamic price bands, and absence of price bands for F&O-traded securities.

### 2. Derivatives Contracts and Specifications
- **Index Options and Futures**: NIFTY 50, BANKNIFTY, and FINNIFTY index futures and options, lot size revisions, tick size (0.05 INR), and cash settlement against the 30-minute volume-weighted average price (VWAP).
- **Stock Derivatives**: European-style single stock options with physical delivery on expiration for in-the-money (ITM) options, and stock futures with physical delivery obligations.
- **Weekly vs Monthly Expiration Cycles**: Expiration schedule dynamics across exchange offerings, weekend theta decay, and concentrated institutional liquidity on expiration days.

### 3. Open Interest (OI) and Derivatives Analytics
- **Open Interest Interpretation**: Four-quadrant analysis correlating price and OI changes (Long Buildup, Short Covering, Short Buildup, Long Unwinding).
- **Put-Call Ratio (PCR)**: PCR of total volume versus PCR of total open interest as a contrarian indicator at market extremes.
- **Max Pain Theory**: Mechanics of the option strike where option writers (sellers) incur the minimum cumulative financial payout upon expiration.
- **Rollover Analysis**: Tracking percentage rollover and rollover cost from near-month to next-month contracts during expiry week.

### 4. Regulatory Framework and Transaction Economics
- **SEBI Margin Framework**: Standard Portfolio Analysis of Risk (SPAN) margin, Extreme Loss Margin (ELM), calendar spread margin benefits, and intraday peak margin snapshot reporting.
- **Taxation and Trading Friction**:
  - Securities Transaction Tax (STT): Differential rates on equity delivery, equity intraday, futures turnover, and options premium / exercised options.
  - Stamp duty, SEBI regulatory turnover fees, exchange transaction charges, and 18% GST on brokerage and transaction fees.
- **Surveillance Frameworks**: Graded Surveillance Measures (GSM) and Additional Surveillance Measures (ASM) criteria based on high-low variation, client concentration, and PE multiples.

---

## Concept Notes

- [[16-Trading-and-Investing/02-Indian-Markets/01-NSE-BSE-Microstructure-and-Derivatives-Architecture|01 NSE BSE Microstructure and Derivatives Architecture]] (32 flashcards)

---

## Trading Lab Engines

- `opt_desk`: Real-time Greeks and PnL attribution calibrated to NSE lot sizes and strike intervals.
- `pos_sizing`: Dynamic position sizing engine accounting for SEBI peak margin rules and asymmetric option buying vs writing risk.
- `fut_desk`: Futures calendar spreads, cost-of-carry, and cash-and-carry basis arbitrage engine.

---

## Navigation

- **Master Hub**: [[16-Trading-and-Investing/MARKETS_HUB|Markets Mastery OS Master Hub]]
- **Options and Volatility Pillar**: [[16-Trading-and-Investing/03-Options-and-Volatility/_Index_Options_Volatility|Options and Volatility Index]]
- **Execution Microstructure**: [[16-Trading-and-Investing/08-Execution-Microstructure/_Index_Execution|Execution and Order Routing]]
