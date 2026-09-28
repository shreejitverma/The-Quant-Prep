import yfinance as yf
from datetime import datetime

REPORT_DIR = "16-Trading-and-Investing/Investing/Macro & Micro Economics"

def fetch_indicator(ticker, label):
    try:
        data = yf.Ticker(ticker)
        # Use 5 days to ensure we get the last trading day even on weekends/holidays
        hist = data.history(period="5d")
        if hist.empty: return f"| {label} | N/A | N/A |"
        
        price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else price
        change = ((price - prev_close) / prev_close) * 100
        return f"| {label} | {price:.2f} | {change:+.2f}% |"
    except Exception as e:
        return f"| {label} | N/A | N/A |"

def generate_macro_report():
    print("Generating Global Macro Report...")
    indicators = [
        ("^TNX", "US 10-Year Treasury Yield"),
        ("^TYX", "US 30-Year Treasury Yield"),
        ("UUP", "US Dollar Index Proxy (UUP)"),
        ("^VIX", "CBOE Volatility Index (VIX)"),
        ("^GSPC", "S&P 500 (US)"),
        ("^NSEI", "Nifty 50 (India)"),
        ("^STOXX50E", "Euro Stoxx 50 (Europe)"),
        ("^N225", "Nikkei 225 (Japan)"),
        ("000001.SS", "SSE Composite (China)")
    ]
    
    rows = [fetch_indicator(t, l) for t, l in indicators]
    
    content = f"""# Global Macro Economic Report
**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Key Market Indicators
| Indicator | Value | Day Change |
| :--- | :--- | :--- |
{chr(10).join(rows)}

## Macro Context
- **Interest Rates**: The 10Y Yield is the "gravity" of all valuations. Rising yields compress P/E multiples.
- **Volatility**: VIX measures "fear." High VIX (>30) often indicates value opportunities.
- **Currency**: Dollar strength (UUP) impacts global trade and multinational earnings.

---
[[Dashboard|Back to Dashboard]]
"""
    with open(f"{REPORT_DIR}/Global Macro Report.md", 'w', encoding='utf-8') as f:
        f.write(content)

def generate_micro_report():
    print("Generating Micro & Sector Report...")
    commodities = [
        ("CL=F", "Crude Oil (WTI)"),
        ("GC=F", "Gold"),
        ("SI=F", "Silver"),
        ("HG=F", "Copper (Dr. Copper)"),
        ("ZC=F", "Corn (Agriculture Proxy)"),
        ("BTC-USD", "Bitcoin (Digital Gold/Liquidity)")
    ]
    
    rows = [fetch_indicator(t, l) for t, l in commodities]
    
    content = f"""# Micro, Sector & Commodity Report
**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Commodity & Sector Proxies
| Asset | Price | Day Change |
| :--- | :--- | :--- |
{chr(10).join(rows)}

## Sector Logic
- **Copper**: "Dr. Copper" often predicts global industrial health.
- **Oil**: Impacts input costs for almost every physical business.
- **Gold/BTC**: Measures debasement risk and liquidity levels.

---
[[Dashboard|Back to Dashboard]]
"""
    with open(f"{REPORT_DIR}/Sector & Commodity Report.md", 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    import os
    os.makedirs(REPORT_DIR, exist_ok=True)
    generate_macro_report()
    generate_micro_report()
    print("Economic Reports Fixed.")
