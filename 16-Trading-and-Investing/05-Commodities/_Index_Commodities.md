---
type: moc
title: "Commodities Pillar Index"
track: [quant-trader, quant-research]
tier: advanced
status: solid
tags: [commodities, energy, metals, agriculture, term-structure, contango, backwardation, moc]
---

# Commodities Pillar Index

The Commodities pillar covers physical and financial commodity derivatives across Energy, Precious Metals, Industrial Metals, and Agriculture.
Unlike financial assets, commodities are consumption assets defined by physical storage costs, transportation bottlenecks, convenience yields, and seasonal supply-demand cycles.

---

## Learning Objectives

- Master the Theory of Storage and decompose commodity forward prices into spot price, financing cost, storage cost, and convenience yield.
- Analyze the term structure of commodity futures: Contango (negative roll return) versus Backwardation (positive roll return).
- Deconstruct the structural drag in retail commodity ETFs resulting from continuous rolling of front-month contracts.
- Model energy processing margins, specifically the Crude Oil 3:2:1 Crack Spread.
- Understand agricultural seasonal planting and harvest calendars, weather risk models, and USDA WASDE inventory reports.

---

## Core Topics

### 1. Theory of Storage and Term Structure Geometry
- **Cost of Carry Model**: Forward price relationship $F(t, T) = S(t) e^{(r + u - y)(T - t)}$, where $r$ is the interest rate, $u$ is the storage/insurance cost, and $y$ is the convenience yield.
- **Contango and Super-Contango**: Regimes where forward prices exceed spot prices; indicates physical inventory surplus and creates negative roll yield for long investors.
- **Backwardation**: Regimes where spot prices exceed forward prices; driven by physical shortage, high convenience yield, and structural hedger net-short positioning (Keynesian Normal Backwardation).
- **Roll Yield Dynamics**: The positive or negative price convergence experienced as a futures contract moves toward expiration along an upward- or downward-sloping curve.

### 2. Energy Markets
- **Crude Oil Benchmarks**: West Texas Intermediate (WTI, Cushing delivery hub, pipeline-constrained) versus Brent Crude (waterborne, North Sea).
- **Refining Economics and Crack Spreads**: The 3:2:1 crack spread simulating refinery profitability (three barrels of crude oil yield two barrels of gasoline and one barrel of distillate fuel oil).
- **Natural Gas (Henry Hub)**: Extreme weather sensitivity (heating degree days vs cooling degree days), storage injection (April-October) versus withdrawal seasons (November-March), and pipeline compression constraints.

### 3. Precious and Industrial Metals
- **Precious Metals (Gold, Silver, Platinum)**: Gold as a monetary asset with negligible convenience yield and low storage costs; inverse correlation with real Treasury yields and dollar strength.
- **Gold-to-Silver Ratio**: Historical relative-value indicator tracking cyclical industrial activity (silver) versus monetary fear (gold).
- **Industrial Metals (Copper, Aluminum, Zinc)**: Copper ("Doctor Copper") as a leading indicator of global capital expenditure, electrification demand, and Chinese manufacturing cycles.

### 4. Agricultural Commodities and Softs
- **Crop Calendars**: North American and South American planting, pollination, and harvest cycles for Corn, Soybeans, and Wheat.
- **USDA WASDE Reports**: World Agricultural Supply and Demand Estimates; analyzing ending stocks-to-use ratios and yield surprises.
- **Weather and Basis Risk**: Local elevator cash prices versus exchange futures prices; transportation basis driven by rail freight and Mississippi River barge traffic.

---

## Concept Notes

- [[16-Trading-and-Investing/05-Commodities/01-Commodity-Term-Structures-and-Storage-Arbitrage|01 Commodity Term Structures and Storage Arbitrage]] (32 flashcards)

---

## Trading Lab Engines

- `fut_desk`: Commodity futures calendar spread analyzer, term structure shape classifier, and historical roll return calculator.
- `pos_sizing`: Dynamic position sizing engine calibrated to commodity futures margin requirements and high tail risk.
- `port_alloc`: Multi-asset portfolio allocator evaluating commodity risk parity weights and inflation hedging.

---

## Navigation

- **Master Hub**: [[16-Trading-and-Investing/MARKETS_HUB|Markets Mastery OS Master Hub]]
- **Macro, Rates, and FX Pillar**: [[16-Trading-and-Investing/04-Macro-Rates-FX/_Index_Macro_Rates_FX|Macro, Rates, and FX Index]]
- **Futures Desk Lab**: `tools/qp/lab/`
