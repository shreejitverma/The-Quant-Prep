import yfinance as yf
import pandas as pd
from datetime import datetime

REPORT_DIR = "16-Trading-and-Investing/Investing/Macro & Micro Economics"

def fetch_annual_series(ticker, label):
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period="max")
        if hist.empty: return None

        annual = hist['Close'].resample('YE').last()
        returns = annual.pct_change() * 100
        
        df = pd.DataFrame({
            'Year': annual.index.year,
            'Value': annual.values,
            'Return': returns.values
        }).sort_values('Year', ascending=False)
        
        return df
    except:
        return None

def generate_deep_macro_report():
    print("Generating Deep History Macro Report...")
    factors = [
        ("^GSPC", "S&P 500 (US Market Proxy)"),
        ("^TNX", "US 10-Year Treasury (Interest Rate Proxy)"),
        ("GC=F", "Gold (Debasement Proxy)"),
        ("CL=F", "Crude Oil (Industrial Input Proxy)"),
        ("^VIX", "VIX (Fear Gauge)")
    ]
    
    content = f"""# Inception-to-Date Macro History
**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}

This report tracks the annual performance and values of foundational macro factors since their earliest available digital records. Use this to correlate stock compounding eras with macro regimes (e.g., Volatility, Inflation, Interest Rates).

"""
    
    for ticker, label in factors:
        df = fetch_annual_series(ticker, label)
        if df is not None:
            content += f"## {label}\n"
            content += "| Year | Year-End Value | YoY Change |\n"
            content += "| :--- | :--- | :--- |\n"
            for _, row in df.iterrows():
                ret_str = f"{row['Return']:+.2f}%" if not pd.isna(row['Return']) else "N/A"
                content += f"| {int(row['Year'])} | {row['Value']:,.2f} | {ret_str} |\n"
            content += "\n"

    content += "---\n[[Dashboard|Back to Dashboard]]\n"
    
    with open(f"{REPORT_DIR}/Deep History Macro.md", 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    generate_deep_macro_report()
    print("Deep Macro Report Generated.")
