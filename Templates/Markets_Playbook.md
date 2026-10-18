---
type: playbook
track: [quant-trader]
tier: advanced
status: draft
curriculum: false
style: discretionary
asset_class: equities
setup_name: "Template Setup Name"
edge_source: "structural-liquidity"
---

# Playbook Setup: {{setup_name}}

Executive summary of the trade setup, market context, and primary edge mechanism.
This playbook defines an actionable, repeatable trade strategy with zero discretionary ambiguity at entry.

---

## 1. Setup Architecture

- **Asset Class & Instruments**: Cash Equities, Index Futures, Options, Perpetual Swaps.
- **Market Regime**: Trending Bull, Trending Bear, Compressed Consolidation, High Volatility Expansion.
- **Timeframe & Holding Period**: Intraday (1m-15m), Swing (1d-5d), Macro Positional (weeks).
- **Core Edge Source**: Auction imbalance, liquidity sweep, earnings drift, volatility risk premium.

---

## 2. Pre-Condition Filters (The Screen)

All conditions must be satisfied before looking for an entry trigger:
1. Higher timeframe key level: Previous Day High/Low, Weekly POC, Anchored VWAP, or major S/R.
2. Market internals alignment: Advance-Decline volume confirmation or sector relative strength.
3. Volatility environment: Daily ATR > threshold; no pending unpriced binary event within the trade window.

---

## 3. Entry Trigger and Invalidation Level

- **Precise Entry Trigger**:
  - Exact event that prompts execution (e.g., reclaim of VWAP after liquidity sweep below IB Low).
  - Order type: Limit order at bid, or aggressive market order upon footprint confirmation.
- **Hard Invalidation (Stop Loss)**:
  - Exact price level where the trade premise is mathematically and auction-wise proven false.
  - Placed beyond structural market pivot, never based on arbitrary monetary pain.

---

## 4. Profit Targets and Trade Management

- **Target 1 (De-Risking)**: Take 50% off at 1.5R to 2.0R or at the next opposing liquidity pool.
- **Target 2 (Runner)**: Trail remaining position using trailing ATR or prior pivot low/high.
- **Time Stop**: If the market fails to expand within N bars, close the position at market.

---

## 5. Position Sizing Rules

- Maximum risk per trade: 1.0% of total portfolio equity.
- Position size formula:
  $$\text{Shares} = \frac{\text{Account Capital} \times \text{Risk Fraction}}{|\text{Entry Price} - \text{Stop Price}|}$$

---

## 6. Post-Trade Review Checklist

- [ ] Was the entry taken strictly according to the documented trigger?
- [ ] Was the stop placed at the pre-planned invalidation level without hesitation?
- [ ] Did execution suffer from emotional FOMO or hesitation slippage?
- [ ] What was the Maximum Adverse Excursion (MAE) and Maximum Favorable Excursion (MFE)?
