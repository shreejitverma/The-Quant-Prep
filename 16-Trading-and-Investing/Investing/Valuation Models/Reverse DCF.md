---
status: stable
priority: high
tags: [valuation, quant, framework]
---
# Valuation Model: Reverse DCF (Discounted Cash Flow)

## Definition
A **Reverse DCF** is a valuation technique that starts with the current market price of a stock and works backward to determine what growth rate the market is currently pricing in.

## Perspective (The Quant View)
Unlike a standard DCF, which is highly sensitive to the analyst's potentially biased growth assumptions, a Reverse DCF is a "sanity check." It tells you: *"Does the market expect this company to grow at 10% or 30%? And is that realistic given its history?"*

## Core Principles
1. **Free Cash Flow (FCF):** The starting point is the TTM (Trailing Twelve Months) FCF.
2. **Cost of Capital (WACC):** The discount rate used to bring future cash flows to present value.
3. **Market Cap Implied Value:** Solving for the growth variable `g` that sets the NPV (Net Present Value) equal to the current Market Cap.

## Failure Modes (Anti-Models)
- **Cyclicality:** FCF can vary wildly for cyclical businesses (Energy/Materials); using a single year's peak FCF leads to massive overvaluation.
- **WACC Sensitivity:** Small changes in the discount rate (e.g., 8% vs 10%) can radically change the implied growth rate.

## Practical Application
- **Calculation:** If a stock is trading at $100 and a Reverse DCF shows an implied growth of 25% for the next 10 years, but the industry is only growing at 5%, the stock is likely **Overvalued**.

---
[[16-Trading-and-Investing/Investing/Stock Research/_Index_Stock Research|Back to Stock Research]] | [[Dashboard|Back to Dashboard]]
