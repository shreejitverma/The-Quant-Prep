---
type: risk-analysis
tags: [quant, risk, correlation]
---
# Portfolio Correlation Matrix (2-Year Daily)

This matrix identifies hidden dependencies between your consistent compounders.

## Matrix
| | PG | JPM | NVDA | ASML.AS | MSFT | GOOGL | MA | WMT | KO | BRK-B | AAPL | V |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **AAPL** | 1.00 | 0.17 | 0.33 | 0.44 | 0.35 | 0.11 | 0.38 | 0.40 | 0.38 | 0.16 | 0.36 | 0.27 |
| **ASML.AS** | 0.17 | 1.00 | -0.04 | 0.25 | 0.16 | -0.12 | -0.02 | 0.17 | 0.35 | -0.12 | -0.02 | 0.04 |
| **BRK-B** | 0.33 | -0.04 | 1.00 | 0.12 | 0.53 | 0.28 | 0.51 | 0.14 | 0.05 | 0.29 | 0.50 | 0.27 |
| **GOOGL** | 0.44 | 0.25 | 0.12 | 1.00 | 0.31 | -0.09 | 0.20 | 0.35 | 0.40 | -0.03 | 0.22 | 0.15 |
| **JPM** | 0.35 | 0.16 | 0.53 | 0.31 | 1.00 | 0.01 | 0.49 | 0.31 | 0.31 | 0.02 | 0.48 | 0.23 |
| **KO** | 0.11 | -0.12 | 0.28 | -0.09 | 0.01 | 1.00 | 0.22 | -0.15 | -0.23 | 0.58 | 0.20 | 0.29 |
| **MA** | 0.38 | -0.02 | 0.51 | 0.20 | 0.49 | 0.22 | 1.00 | 0.30 | 0.17 | 0.25 | 0.87 | 0.28 |
| **MSFT** | 0.40 | 0.17 | 0.14 | 0.35 | 0.31 | -0.15 | 0.30 | 1.00 | 0.49 | -0.10 | 0.28 | 0.13 |
| **NVDA** | 0.38 | 0.35 | 0.05 | 0.40 | 0.31 | -0.23 | 0.17 | 0.49 | 1.00 | -0.18 | 0.16 | 0.07 |
| **PG** | 0.16 | -0.12 | 0.29 | -0.03 | 0.02 | 0.58 | 0.25 | -0.10 | -0.18 | 1.00 | 0.22 | 0.32 |
| **V** | 0.36 | -0.02 | 0.50 | 0.22 | 0.48 | 0.20 | 0.87 | 0.28 | 0.16 | 0.22 | 1.00 | 0.28 |
| **WMT** | 0.27 | 0.04 | 0.27 | 0.15 | 0.23 | 0.29 | 0.28 | 0.13 | 0.07 | 0.32 | 0.28 | 1.00 |

## Risk Management Logic
- **High Correlation (>0.70)**: These stocks tend to move together. Diversification benefit is low.
- **Low Correlation (<0.30)**: These stocks provide true risk offsets.
- **Diversification**: Aim for a mix of high-quality assets with varying correlation scores across different sectors and geographies.

---
[[16-Trading-and-Investing/Investing/Stock Research/_Index_Stock Research|Back to Global Research]] | [[Dashboard|Back to Dashboard]]
