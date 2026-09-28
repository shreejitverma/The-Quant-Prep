import yfinance as yf
import pandas as pd
import os
import re

VAULT_ROOT = "16-Trading-and-Investing/Investing/Stock Research"
REPORT_PATH = "16-Trading-and-Investing/Investing/Risk Management/Correlation Matrix.md"

TICKER_MAP = {
    "RELIANCE": "RELIANCE.NS", "HDFCBANK": "HDFCBANK.NS", "TCS": "TCS.NS",
    "7203": "7203.T", "6758": "6758.T", "BRK.B": "BRK-B", "ASML": "ASML.AS",
    "SAP": "SAP.DE", "NESN.SW": "NESN.SW", "AAPL": "AAPL", "MSFT": "MSFT", 
    "NVDA": "NVDA", "JPM": "JPM", "V": "V", "MA": "MA", "WMT": "WMT", 
    "PG": "PG", "KO": "KO", "TSM": "TSM", "GOOGL": "GOOGL"
}

def extract_ticker(filename):
    match = re.search(r'\(([^)]+)\)', filename)
    return match.group(1) if match else None

def generate_correlation_matrix():
    print("Calculating Correlation Matrix...")
    tickers = []
    
    # Selection: Get top 20 tickers found in vault to ensure data coverage
    for root, dirs, files in os.walk(VAULT_ROOT):
        for file in files:
            if file.endswith(".md") and not file.startswith("_"):
                t = extract_ticker(file)
                if t and t in TICKER_MAP:
                    tickers.append(TICKER_MAP[t])
    
    tickers = list(set(tickers))[:15] # Limit to top 15 for readable matrix
    if not tickers: return

    data = yf.download(tickers, period="2y")['Close']
    corr = data.pct_change().corr()

    # Convert matrix to Markdown
    header = "| | " + " | ".join([t for t in tickers]) + " |"
    divider = "| :--- | " + " | ".join([":---:" for _ in tickers]) + " |"
    rows = []
    for i, row in corr.iterrows():
        row_str = f"| **{i}** | " + " | ".join([f"{val:.2f}" for val in row.values]) + " |"
        rows.append(row_str)

    content = f"""---
type: risk-analysis
tags: [quant, risk, correlation]
---
# Portfolio Correlation Matrix (2-Year Daily)

This matrix identifies hidden dependencies between your consistent compounders.

## Matrix
{header}
{divider}
{chr(10).join(rows)}

## Risk Management Logic
- **High Correlation (>0.70)**: These stocks tend to move together. Diversification benefit is low.
- **Low Correlation (<0.30)**: These stocks provide true risk offsets.
- **Diversification**: Aim for a mix of high-quality assets with varying correlation scores across different sectors and geographies.

---
[[16-Trading-and-Investing/Investing/Stock Research/_Index_Stock Research|Back to Global Research]] | [[Dashboard|Back to Dashboard]]
"""
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    generate_correlation_matrix()
    print("Correlation Engine Complete.")
