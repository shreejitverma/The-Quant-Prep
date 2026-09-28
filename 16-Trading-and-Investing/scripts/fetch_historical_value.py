import os
import re
import yfinance as yf
from datetime import datetime

VAULT_ROOT = "16-Trading-and-Investing/Investing/Stock Research"

# Refined Ticker Map for Global Markets
TICKER_MAP = {
    # US
    "BRK.B": "BRK-B", "BRK.A": "BRK-A",
    # India (NSE)
    "RELIANCE": "RELIANCE.NS", "HDFCBANK": "HDFCBANK.NS", "TCS": "TCS.NS",
    "ASIANPAINT": "ASIANPAINT.NS", "TITAN": "TITAN.NS", "INFY": "INFY.NS",
    "ICICIBANK": "ICICIBANK.NS", "BAJFINANCE": "BAJFINANCE.NS",
    "PIDILITIND": "PIDILITIND.NS", "NESTLEIND": "NESTLEIND.NS",
    "HINDUNILVR": "HINDUNILVR.NS", "MARICO": "MARICO.NS", "LT": "LT.NS",
    "SUNPHARMA": "SUNPHARMA.NS",
    # Japan (TSE)
    "7203": "7203.T", "6758": "6758.T", "6861": "6861.T", "7974": "7974.T",
    "6954": "6954.T", "9983": "9983.T", "4063": "4063.T", "6981": "6981.T",
    "7741": "7741.T",
    # Germany (XETRA)
    "RAA": "RAA.DE", "SY1": "SY1.DE", "FPE3": "FPE3.DE", "SRT3": "SRT3.DE",
    "NEM": "NEM.DE", "EVD": "EVD.DE", "SIX2": "SIX2.DE", "AFX": "AFX.DE",
    "SIE": "SIE.DE", "SAP": "SAP.DE", "ASML": "ASML.AS",
    # Brazil (B3)
    "WEGE3": "WEGE3.SA", "RADL3": "RADL3.SA", "ITUB4": "ITUB4.SA",
    "RENT3": "RENT3.SA", "EQTL3": "EQTL3.SA",
    # China (Shanghai/HK)
    "600519": "600519.SS", "0700.HK": "0700.HK", "3690.HK": "3690.HK", "1211.HK": "1211.HK",
    # Singapore/SE Asia
    "D05": "D05.SI", "BBCA": "BBCA.JK", "CPALL": "CPALL.BK", "PBBANK": "PBBANK.KL",
    "SE": "SE", "MELI": "MELI", "SHOP": "SHOP",
    # Australia
    "CSL.AX": "CSL.AX", "CBA.AX": "CBA.AX",
    # Sweden
    "INVE.B": "INVE-B.ST", "ATCO.A": "ATCO-A.ST", "ASSA.B": "ASSA-B.ST", "HEXA.B": "HEXA-B.ST"
}

def extract_ticker(filename):
    # Only match what looks like a ticker (shorter, uppercase/digits/dots/hyphens)
    match = re.search(r'\(([^)]+)\)', filename)
    if match:
        candidate = match.group(1)
        if len(candidate) <= 10 and candidate.upper() == candidate:
            return candidate
    return None

def get_cagr(history, years):
    if history.empty or len(history) < 20: return 0
    end_price = history['Close'].iloc[-1]
    start_price = history['Close'].iloc[0]
    if start_price <= 0: return 0
    return ((end_price / start_price) ** (1 / years) - 1) * 100

def update_value_metrics(file_path, original_ticker):
    try:
        yf_ticker = TICKER_MAP.get(original_ticker, original_ticker)
        stock = yf.Ticker(yf_ticker)
        info = stock.info
        
        # Use a slightly longer period if 10y fails
        hist_10y = stock.history(period="10y")
        if hist_10y.empty: hist_10y = stock.history(period="max")
        
        hist_5y = stock.history(period="5y")

        # Dynamic period for CAGR if less than 10y available
        actual_years_10 = (hist_10y.index[-1] - hist_10y.index[0]).days / 365.25 if not hist_10y.empty else 0
        actual_years_5 = (hist_5y.index[-1] - hist_5y.index[0]).days / 365.25 if not hist_5y.empty else 0
        
        cagr_10y = get_cagr(hist_10y, actual_years_10) if actual_years_10 > 1 else 0
        cagr_5y = get_cagr(hist_5y, actual_years_5) if actual_years_5 > 1 else 0
        
        # Superinvestor Metrics
        roe = info.get('returnOnEquity') or info.get('returnOnEquity_avg', 0)
        roa = info.get('returnOnAssets', 0)
        debt_to_equity = (info.get('debtToEquity') or 0) / 100 
        peg_ratio = info.get('pegRatio', 0)
        gross_margin = info.get('grossMargins', 0)
        fcf = info.get('freeCashflow') or info.get('operatingCashflow', 0)
        market_cap = info.get('marketCap', 1)
        fcf_yield = (fcf / market_cap) * 100 if fcf else 0
        currency = info.get('currency', 'USD')

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        value_meta = f"""
value_metrics:
  last_deep_fetch: {datetime.now().strftime('%Y-%m-%d')}
  currency: {currency}
  returns:
    cagr_10y: {cagr_10y:.2f}%
    cagr_5y: {cagr_5y:.2f}%
  quality:
    roe: {roe*100:.2f}% if roe else "N/A"
    roa: {roa*100:.2f}% if roa else "N/A"
    gross_margin: {gross_margin*100:.2f}% if gross_margin else "N/A"
    debt_to_equity: {debt_to_equity:.2f}
  valuation:
    fcf_yield: {fcf_yield:.2f}%
    peg_ratio: {peg_ratio:.2f}
"""
        # Cleanup python logic strings in f-string
        roe_str = f"{roe*100:.2f}%" if roe else "N/A"
        roa_str = f"{roa*100:.2f}%" if roa else "N/A"
        gm_str = f"{gross_margin*100:.2f}%" if gross_margin else "N/A"
        
        value_meta = f"""
value_metrics:
  last_deep_fetch: {datetime.now().strftime('%Y-%m-%d')}
  currency: {currency}
  returns:
    cagr_10y: {cagr_10y:.2f}%
    cagr_5y: {cagr_5y:.2f}%
  quality:
    roe: {roe_str}
    roa: {roa_str}
    gross_margin: {gm_str}
    debt_to_equity: {debt_to_equity:.2f}
  valuation:
    fcf_yield: {fcf_yield:.2f}%
    peg_ratio: {peg_ratio:.2f}
"""
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            frontmatter = parts[1]
            # Precise regex to remove previous iterations of metrics
            clean_fm = re.sub(r'market_data:.*?\n(  .*?\n)+', '', frontmatter, flags=re.DOTALL)
            clean_fm = re.sub(r'value_metrics:.*?\n(  .*?\n)+', '', clean_fm, flags=re.DOTALL)
            clean_fm = re.sub(r'last_updated:.*?\n', '', clean_fm)
            
            new_content = "---" + clean_fm.strip() + "\n" + value_meta.strip() + "\n---" + parts[2]
        else:
            new_content = "---" + value_meta.strip() + "\n---\n" + content

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Enhanced {yf_ticker}")

    except Exception as e:
        print(f"Error in {original_ticker}: {e}")

def main():
    print(f"Fixing and Improving Value Metrics at {datetime.now()}...")
    for root, dirs, files in os.walk(VAULT_ROOT):
        # Skip Historical folder for metrics
        if "Historical" in root: continue
        for file in files:
            if file.endswith(".md") and "(" in file:
                ticker = extract_ticker(file)
                if ticker:
                    update_value_metrics(os.path.join(root, file), ticker)
    print("Improvement Complete.")

if __name__ == "__main__":
    main()
