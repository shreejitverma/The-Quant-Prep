import os
import re
import yfinance as yf
from datetime import datetime

VAULT_ROOT = "16-Trading-and-Investing/Investing/Stock Research"

TICKER_MAP = {
    "BRK.B": "BRK-B", "RELIANCE": "RELIANCE.NS", "HDFCBANK": "HDFCBANK.NS", "TCS": "TCS.NS",
    "ASIANPAINT": "ASIANPAINT.NS", "TITAN": "TITAN.NS", "INFY": "INFY.NS",
    "ICICIBANK": "ICICIBANK.NS", "BAJFINANCE": "BAJFINANCE.NS",
    "7203": "7203.T", "6758": "6758.T", "6861": "6861.T", "7974": "7974.T",
    "RAA": "RAA.DE", "SY1": "SY1.DE", "FPE3": "FPE3.DE", "SAP": "SAP.DE", "ASML": "ASML.AS",
    "WEGE3": "WEGE3.SA", "RADL3": "RADL3.SA", "ITUB4": "ITUB4.SA",
    "600519": "600519.SS", "D05": "D05.SI", "BBCA": "BBCA.JK",
    "INVE.B": "INVE-B.ST", "ATCO.A": "ATCO-A.ST", "ASSA.B": "ASSA-B.ST", "HEXA.B": "HEXA-B.ST"
}

def extract_ticker(filename):
    match = re.search(r'\(([^)]+)\)', filename)
    return match.group(1) if match else None

def solve_implied_growth(price, fcf, shares, r=0.10, terminal_g=0.03, n=10):
    """
    Reverse DCF: Solves for growth rate 'g' such that:
    Price = Sum(FCF * (1+g)^i / (1+r)^i) + TerminalValue / (1+r)^n
    This is a simplified linear approximation.
    """
    if price <= 0 or fcf <= 0 or shares <= 0: return 0
    fcf_per_share = fcf / shares
    
    # Simple search for growth rate
    for g in range(-50, 100):
        growth = g / 100
        val = 0
        current_fcf = fcf_per_share
        for i in range(1, n + 1):
            current_fcf *= (1 + growth)
            val += current_fcf / ((1 + r) ** i)
        
        # Add Terminal Value
        tv = (current_fcf * (1 + terminal_g)) / (r - terminal_g)
        val += tv / ((1 + r) ** n)
        
        if val >= price:
            return g
    return 0

def update_implied_growth(file_path, original_ticker):
    try:
        yf_ticker = TICKER_MAP.get(original_ticker, original_ticker)
        stock = yf.Ticker(yf_ticker)
        info = stock.info
        
        price = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        fcf = info.get('freeCashflow') or info.get('operatingCashflow', 0)
        shares = info.get('sharesOutstanding', 1)
        
        implied_g = solve_implied_growth(price, fcf, shares)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update metadata
        new_metric = f"  implied_growth_rate: {implied_g}%"
        
        if "value_metrics:" in content:
            if "implied_growth_rate:" in content:
                content = re.sub(r'implied_growth_rate:.*', f'implied_growth_rate: {implied_g}%', content)
            else:
                content = content.replace("value_metrics:", f"value_metrics:\n{new_metric}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Goal Seeked {yf_ticker}: {implied_g}% growth priced in.")

    except Exception as e:
        print(f"Failed Reverse DCF for {original_ticker}: {e}")

def main():
    print(f"Automating Reverse DCF Goal Seeking...")
    for root, dirs, files in os.walk(VAULT_ROOT):
        if "Historical" in root: continue
        for file in files:
            if file.endswith(".md") and "(" in file:
                ticker = extract_ticker(file)
                if ticker:
                    update_implied_growth(os.path.join(root, file), ticker)
    print("Valuations Complete.")

if __name__ == "__main__":
    main()
