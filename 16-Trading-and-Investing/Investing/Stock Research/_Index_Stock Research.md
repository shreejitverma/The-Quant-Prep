---
type: MOC
tags: [moc, investing, stocks, global-research, godhood]
---
# Global Stock Research Map of Content

> "Price is what you pay. Value is what you get." - Warren Buffett

## Quant Suite Intelligence
- **[[16-Trading-and-Investing/Investing/Risk Management/Correlation Matrix|Portfolio Correlation Matrix]]**: Identifying hidden risks and diversification offsets.
- **[[16-Trading-and-Investing/Investing/Macro & Micro Economics/Global Macro Report|Global Macro Report]]**: Live interest rate and volatility tracking.

## Sector Benchmarking Reports
- **[[16-Trading-and-Investing/Investing/Stock Research/Technology/_Sector_Analysis|Technology Benchmark]]** | **[[16-Trading-and-Investing/Investing/Stock Research/Financials/_Sector_Analysis|Financials Benchmark]]**
- **[[16-Trading-and-Investing/Investing/Stock Research/Healthcare/_Sector_Analysis|Healthcare Benchmark]]** | **[[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/_Sector_Analysis|Staples Benchmark]]**
- **[[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/_Sector_Analysis|Discretionary Benchmark]]** | **[[16-Trading-and-Investing/Investing/Stock Research/Industrials/_Sector_Analysis|Industrials Benchmark]]**

## Superinvestor Value Screener
```dataview
TABLE 
  value_metrics.quality.roe as "ROE", 
  value_metrics.implied_growth_rate as "Implied Growth",
  value_metrics.returns.cagr_10y as "10y CAGR",
  value_metrics.valuation.fcf_yield as "FCF Yield",
  value_metrics.valuation.peg_ratio as "PEG"
FROM "16-Trading-and-Investing/Investing/Stock Research"
WHERE value_metrics != null
SORT value_metrics.quality.roe DESC
```

## Sector & Geography Intelligence
[... (rest of the MOC content) ...]
