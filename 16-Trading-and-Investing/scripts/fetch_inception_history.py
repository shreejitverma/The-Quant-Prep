import os
import re
import yfinance as yf
import pandas as pd
from datetime import datetime

VAULT_ROOT = "16-Trading-and-Investing/Investing/Stock Research"

TICKER_MAP = {
    "BRK.B": "BRK-B", "BRK.A": "BRK-A",
    "RELIANCE": "RELIANCE.NS", "HDFCBANK": "HDFCBANK.NS", "TCS": "TCS.NS",
    "ASIANPAINT": "ASIANPAINT.NS", "TITAN": "TITAN.NS", "INFY": "INFY.NS",
    "ICICIBANK": "ICICIBANK.NS", "BAJFINANCE": "BAJFINANCE.NS",
    "PIDILITIND": "PIDILITIND.NS", "NESTLEIND": "NESTLEIND.NS",
    "HINDUNILVR": "HINDUNILVR.NS", "MARICO": "MARICO.NS", "LT": "LT.NS",
    "SUNPHARMA": "SUNPHARMA.NS",
    "7203": "7203.T", "6758": "6758.T", "6861": "6861.T", "7974": "7974.T",
    "6954": "6954.T", "9983": "9983.T", "4063": "4063.T", "6981": "6981.T",
    "7741": "7741.T",
    "RAA": "RAA.DE", "SY1": "SY1.DE", "FPE3": "FPE3.DE", "SRT3": "SRT3.DE",
    "NEM": "NEM.DE", "EVD": "EVD.DE", "SIX2": "SIX2.DE", "AFX": "AFX.DE",
    "SIE": "SIE.DE", "SAP": "SAP.DE", "ASML": "ASML.AS",
    "WEGE3": "WEGE3.SA", "RADL3": "RADL3.SA", "ITUB4": "ITUB4.SA",
    "RENT3": "RENT3.SA", "EQTL3": "EQTL3.SA",
    "600519": "600519.SS", "0700.HK": "0700.HK", "3690.HK": "3690.HK", "1211.HK": "1211.HK",
    "D05": "D05.SI", "BBCA": "BBCA.JK", "CPALL": "CPALL.BK", "PBBANK": "PBBANK.KL",
    "INVE.B": "INVE-B.ST", "ATCO.A": "ATCO-A.ST", "ASSA.B": "ASSA-B.ST", "HEXA.B": "HEXA-B.ST"
}

def extract_ticker(filename):
    match = re.search(r'\(([^)]+)\)', filename)
    if match:
        candidate = match.group(1)
        if len(candidate) <= 10 and candidate.upper() == candidate:
            return candidate
    return None

def generate_yearly_performance_table(ticker):
    try:
        yf_ticker = TICKER_MAP.get(ticker, ticker)
        stock = yf.Ticker(yf_ticker)
        # Fetch max period
        hist = stock.history(period="max")
        if hist.empty: return ""

        # Resample to annual frequency (last trading day of year)
        annual = hist['Close'].resample('YE').last()
        returns = annual.pct_change() * 100
        
        # Calculate volatility (annualized stdev of daily returns per year)
        daily_returns = hist['Close'].pct_change()
        volatility = daily_returns.groupby(daily_returns.index.year).std() * (252**0.5) * 100

        # Create Table
        rows = []
        # Reverse to show newest years first
        years = annual.index.year[::-1]
        for year in years:
            price = annual.loc[f"{year}"].iloc[0]
            ret = returns.loc[f"{year}"].iloc[0]
            vol = volatility.get(year, 0)
            
            ret_str = f"{ret:+.2f}%" if not pd.isna(ret) else "N/A"
            rows.append(f"| {year} | {price:,.2f} | {ret_str} | {vol:.2f}% |")

        table = f"""
## Inception-to-Date Yearly Performance
| Year | Close Price | YoY Return | Annual Volatility |
| :--- | :--- | :--- | :--- |
{chr(10).join(rows)}
"""
        return table
    except Exception as e:
        print(f"Error generating table for {ticker}: {e}")
        return ""

def update_file(file_path, ticker):
    table = generate_yearly_performance_table(ticker)
    if not table: return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove existing table if it exists
    content = re.sub(r'## Inception-to-Date Yearly Performance.*', '', content, flags=re.DOTALL)
    
    # Append new table before Cross-Links or at end
    if "## Cross-Links" in content:
        parts = content.split("## Cross-Links")
        new_content = parts[0].strip() + "\n" + table.strip() + "\n\n## Cross-Links" + parts[1]
    else:
        new_content = content.strip() + "\n" + table.strip()

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Injected History: {ticker}")

def main():
    print(f"Starting Deep History Ingestion at {datetime.now()}...")
    for root, dirs, files in os.walk(VAULT_ROOT):
        if "Historical" in root: continue
        for file in files:
            if file.endswith(".md") and "(" in file:
                ticker = extract_ticker(file)
                if ticker:
                    update_file(os.path.join(root, file), ticker)
    print("Deep History Ingestion Complete.")

if __name__ == "__main__":
    main()
