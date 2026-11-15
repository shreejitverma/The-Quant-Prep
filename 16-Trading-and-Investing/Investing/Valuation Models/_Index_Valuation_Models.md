---
type: moc
title: "Valuation Models and Expectations Analysis Index"
track: [quant-trader, quant-research]
tier: core
status: solid
tags: [valuation, dcf, reverse-dcf, multiples, sotp, net-net, expectations-investing, moc]
---

# Valuation Models and Expectations Analysis Index

The Valuation Models and Expectations Analysis curriculum establishes the quantitative engineering tools required to determine the intrinsic value of corporate enterprises, evaluate market-implied expectations, and exploit asset mispricings.
It equips analysts to move fluidly between discounted cash flow first principles, expectations investing reverse engineering, relative multiples discipline, conglomerate sum-of-the-parts dissection, and liquidation floor forensics.

---

## Learning Objectives

- Derive and project Free Cash Flow to Firm (FCFF) and Free Cash Flow to Equity (FCFE) across multi-stage forecast horizons.
- Estimate the Weighted Average Cost of Capital (WACC) using bottom-up asset betas, implied equity risk premiums, and synthetic debt ratings.
- Avoid the five fatal terminal value traps by modeling the fundamental link between perpetual growth and capital reinvestment.
- Execute Reverse DCF models to solve for market-implied growth rates and construct two-dimensional Expectations Grids.
- Benchmark enterprise-level and equity-level valuation multiples while eliminating numerator-denominator mismatch errors.
- Dissect corporate conglomerates using Sum-of-the-Parts (SOTP) models while capitalizing unallocated corporate overhead drag.
- Audit distressed entities using Benjamin Graham's Net-Net Working Capital and Bruce Greenwald's Asset Reproduction Cost.
- Apply specialized valuation architectures for commercial banks, cyclical commodity producers, and high-growth SaaS loss-makers.
- Synthesize business storytelling with quantitative financial drivers and execute Gary Klein Pre-Mortems with pre-registered kill criteria.

---

## Valuation Models Curriculum Map

The valuation track comprises eight comprehensive concept notes containing 266 verified practice questions and problem cards:

1. [[16-Trading-and-Investing/Investing/Valuation Models/01-DCF-First-Principles-and-Cash-Flow-Forecasting|01. DCF First Principles and Cash Flow Forecasting]]
   - The foundations of intrinsic value: John Burr Williams' present worth of future dividends and his law of the conservation of investment value.
   - FCFF vs FCFE: cash flow formulations, discount rate matching, and the equity bridge.
   - Multi-stage forecasting engines: revenue decomposition, operating leverage, and capital intensity.
   - Mid-year discounting mechanics and mathematical present value adjustments.
   - Terminal value Gordon Growth versus exit multiples cross-checks.
   - Cards: `mkt-val-001` through `mkt-val-032`, plus `mkt-val-257` and `mkt-val-258`.

2. [[16-Trading-and-Investing/Investing/Valuation Models/02-Cost-of-Capital-WACC-and-Terminal-Value-Traps|02. Cost of Capital, WACC, and Terminal Value Traps]]
   - Weighted Average Cost of Capital (WACC) formulation and market value weighting.
   - Cost of Equity ($K_e$), CAPM, and bottom-up unlevered betas via Hamada's equation.
   - Synthetic credit ratings and marginal pre-tax cost of debt.
   - The Five Fatal Terminal Value Traps: GDP ceiling, zero-reinvestment fallacy, infinite ROIC, spread sensitivity, and negative terminal cash flow.
   - The McKinsey Key Value Driver formula: linking terminal value directly to Return on New Invested Capital (RONIC).
   - Cards: `mkt-val-033` through `mkt-val-064`, plus `mkt-val-259` and `mkt-val-260`.

3. [[16-Trading-and-Investing/Investing/Valuation Models/03-Reverse-DCF-and-Expectations-Investing|03. Reverse DCF and Expectations Investing]]
   - Alfred Rappaport and Michael Mauboussin's Expectations Investing framework.
   - Inverting the valuation equation: solving for market-implied revenue growth and operating margins.
   - Numerical root-finding algorithms (bisection and Newton-Raphson) in reverse DCF.
   - Constructing the 2-Way Expectations Matrix and testing implied growth against industry TAM.
   - Identifying expectation triggers, revisions, and forming asymmetric variant perceptions.
   - Cards: `mkt-val-065` through `mkt-val-096`, plus `mkt-val-261`.

4. [[16-Trading-and-Investing/Investing/Valuation Models/04-Relative-Valuation-Multiples-Done-Right|04. Relative Valuation and Multiples Done Right]]
   - Multiples as condensed DCF models: mathematical derivation of forward P/E and EV/EBIT.
   - The Golden Rule of consistent multiples: Enterprise Value vs Equity Value numerators and denominators.
   - Calculating Enterprise Value: operating leases, non-controlling interests, and equity affiliates.
   - EBITDA critiques: why depreciation is a real economic expense and capital intensity distortions.
   - Price-to-Book (P/B) and its fundamental link to Return on Equity (ROE).
   - The PEG ratio heuristic versus fundamental reality.
   - Cards: `mkt-val-097` through `mkt-val-128`, plus `mkt-val-262`.

5. [[16-Trading-and-Investing/Investing/Valuation Models/05-Sum-of-the-Parts-and-Corporate-Conglomerates|05. Sum-of-the-Parts (SOTP) and Corporate Conglomerates]]
   - Sum-of-the-parts methodology for multi-business enterprises.
   - Mining Item 8 / ASC 280 segment footnotes and eliminating intercompany transfers.
   - The essential corporate overhead capitalization deduction to prevent SOTP overvaluation.
   - The Conglomerate Discount (13% to 15% on average in Berger and Ofek 1995, US 1986-1991) and Holding Company discounts.
   - Corporate restructuring catalysts: tax-free spinoffs (Section 355), equity carve-outs, split-offs, and asset sales.
   - Cards: `mkt-val-129` through `mkt-val-160`.

6. [[16-Trading-and-Investing/Investing/Valuation Models/06-Asset-Based-Liquidation-and-Net-Net-Valuation|06. Asset-Based, Liquidation, and Net-Net Valuation]]
   - Benjamin Graham's Net Current Asset Value (NCAV) and the two-thirds rule.
   - Conservative Net-Net Working Capital (NNWC) haircut schedules across receivables, inventory, and cash.
   - Orderly Liquidation Value (OLV) vs Forced Liquidation Value (FLV) and off-balance-sheet claims.
   - Bruce Greenwald's Asset Reproduction Cost vs Earnings Power Value (EPV) moat analysis.
   - The Graham Number and the 22.5 product rule it comes from.
   - The 'Melting Ice Cube' trap: operational burn rate exhausting net cash buffers.
   - Cards: `mkt-val-161` through `mkt-val-192`, plus `mkt-val-263`.

7. [[16-Trading-and-Investing/Investing/Valuation Models/07-Specialized-Valuation-Financials-Cyclicals-and-Loss-Makers|07. Specialized Valuation: Financials, Cyclicals, and High-Growth Loss-Makers]]
   - Why traditional enterprise DCF models fail for commercial banks and insurance companies.
   - The Bank Valuation Matrix: Return on Tangible Common Equity (ROTCE) vs Price-to-Tangible Book Value (P/TBV).
   - Dividend Discount Models constrained by Basel Common Equity Tier 1 (CET1) capital ratios.
   - The inverse cyclical multiple trap for commodity producers and mid-cycle earnings normalization.
   - Unit economics for high-growth software: Customer Lifetime Value (LTV), Customer Acquisition Cost (CAC), and the Rule of 40.
   - Risk-adjusted Net Present Value (rNPV) models for clinical-stage biotechnology pipelines.
   - Cards: `mkt-val-193` through `mkt-val-224`, plus `mkt-val-264` and `mkt-val-265`.

8. [[16-Trading-and-Investing/Investing/Valuation Models/08-Narrative-and-Numbers-Valuation-Synthesis|08. Narrative and Numbers: Valuation Synthesis and Pre-Mortems]]
   - Aswath Damodaran's five-step Narrative-to-Numbers framework.
   - Damodaran's narrative test: is it Possible, Plausible, and Probable?
   - Translating qualitative business stories into quantitative financial inputs.
   - Detecting narrative breaks and managing corporate lifecycle phase transitions.
   - Gary Klein's Valuation Pre-Mortem: independent failure mapping and establishing pre-registered kill criteria.
   - Cards: `mkt-val-225` through `mkt-val-256`, plus `mkt-val-266`.

---

## Integration with Research and Lab Suite

Every concept note in this track is backed by a script that prints and asserts its numbers, and connects to the research tools and drills:
- `code/mkt_val_01_dcf.py` through `code/mkt_val_08_narrative.py` check every worked example and card number in notes 01 to 08.
- `scripts/quant_reverse_dcf.py` solves for the growth rate implied by each stock note's price and free cash flow per share, by bisection.
- Valuation Rebuild Drills in `30-Drills/` provide blind financial statements to test model construction under timed constraints.
- The Stage 2 gate in the [Learning Path](../../00-Curriculum/Learning-Path.md) asks for three complete company reverse DCF models in `Investing/Stock Research/`.
