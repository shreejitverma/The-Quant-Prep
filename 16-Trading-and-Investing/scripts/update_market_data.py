import os
import re
import yfinance as yf
from datetime import datetime

VAULT_ROOT = "16-Trading-and-Investing/Investing/Stock Research"

# Map of local tickers to Yahoo Finance tickers
TICKER_MAP = {
    # India
    "RELIANCE": "RELIANCE.NS", "HDFCBANK": "HDFCBANK.NS", "TCS": "TCS.NS",
    "ASIANPAINT": "ASIANPAINT.NS", "TITAN": "TITAN.NS", "INFY": "INFY.NS",
    "ICICIBANK": "ICICIBANK.NS", "BAJFINANCE": "BAJFINANCE.NS",
    "PIDILITIND": "PIDILITIND.NS", "NESTLEIND": "NESTLEIND.NS",
    "HINDUNILVR": "HINDUNILVR.NS", "MARICO": "MARICO.NS", "LT": "LT.NS",
    "SUNPHARMA": "SUNPHARMA.NS",
    # Japan
    "7203": "7203.T", "6758": "6758.T", "6861": "6861.T", "7974": "7974.T",
    "6954": "6954.T", "9983": "9983.T", "4063": "4063.T", "6981": "6981.T",
    "7741": "7741.T",
    # Germany
    "RAA": "RAA.DE", "SY1": "SY1.DE", "FPE3": "FPE3.DE", "SRT3": "SRT3.DE",
    "NEM": "NEM.DE", "EVD": "EVD.DE", "SIX2": "SIX2.DE", "AFX": "AFX.DE",
    "SIE": "SIE.DE",
    # Brazil
    "WEGE3": "WEGE3.SA", "RADL3": "RADL3.SA", "ITUB4": "ITUB4.SA",
    "RENT3": "RENT3.SA", "EQTL3": "EQTL3.SA",
    # Europe (General)
    "MC.PA": "MC.PA", "RMS.PA": "RMS.PA", "OR.PA": "OR.PA", "SU.PA": "SU.PA",
    "AI.PA": "AI.PA", "ITX.MC": "ITX.MC", "NESN.SW": "NESN.SW", "ROG.SW": "ROG.SW",
    "SAP": "SAP.DE", "ASML": "ASML",
    # Singapore/SEA
    "D05": "D05.SI", "BBCA": "BBCA.JK", "CPALL": "CPALL.BK", "PBBANK": "PBBANK.KL",
    "SE": "SE", "MELI": "MELI", "SHOP": "SHOP",
    # Australia
    "CSL.AX": "CSL.AX", "CBA.AX": "CBA.AX",
    # Sweden
    "INVE.B": "INVE-B.ST", "ATCO.A": "ATCO-A.ST", "ASSA.B": "ASSA-B.ST", "HEXA.B": "HEXA-B.ST"
}

def extract_ticker(filename):
    match = re.search(r'\(([^)]+)\)', filename)
    return match.group(1) if match else None

def update_stock_file(file_path, original_ticker):
    try:
        yf_ticker = TICKER_MAP.get(original_ticker, original_ticker)
        stock = yf.Ticker(yf_ticker)
        info = stock.info
        
        current_price = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        market_cap = info.get('marketCap') or 0
        pe_ratio = info.get('trailingPE') or 0
        div_yield = info.get('dividendYield') or 0
        high_52 = info.get('fiftyTwoWeekHigh') or 0
        low_52 = info.get('fiftyTwoWeekLow') or 0
        currency = info.get('currency', 'USD')

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_meta = f"""---
last_updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
market_data:
  ticker: {yf_ticker}
  price: {current_price} {currency}
  market_cap: {market_cap:,} {currency}
  pe_ratio: {pe_ratio:.2f}
  dividend_yield: {div_yield*100:.2f}%
  52w_high: {high_52}
  52w_low: {low_52}
"""
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            # Find existing frontmatter to preserve other tags
            frontmatter = parts[1]
            # Replace market_data block if it exists, else append
            if "market_data:" in frontmatter:
                # Simple replacement for the demo, more robust regex would be better
                content = "---" + new_meta + parts[2]
            else:
                content = "---" + frontmatter.strip() + "\n" + new_meta.replace("---", "").strip() + "\n---" + parts[2]
        else:
            content = "---" + new_meta + "---\n" + content

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {yf_ticker}")

    except Exception as e:
        print(f"Failed to update {original_ticker}: {e}")

def main():
    print(f"Starting Quant OS Market Data Update at {datetime.now()}...")
    for root, dirs, files in os.walk(VAULT_ROOT):
        for file in files:
            if file.endswith(".md") and "(" in file:
                ticker = extract_ticker(file)
                if ticker:
                    file_path = os.path.join(root, file)
                    update_stock_file(file_path, ticker)
    print(f"Update Complete.")

if __name__ == "__main__":
    main()
