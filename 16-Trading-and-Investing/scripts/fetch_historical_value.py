"""Fetch historical fundamental metrics and superinvestor ratios via yfinance.

Uses stock_notes helpers to maintain clean YAML frontmatter, preserve
all existing fields, guard against cross-currency calculation errors,
and never substitute placeholder 0 or 1 for missing data.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "16-Trading-and-Investing" / "scripts"))

import stock_notes  # noqa: E402

try:
    import yfinance as yf
except ImportError:
    yf = None


def get_cagr(history, years: float) -> str:
    if history is None or history.empty or len(history) < 20 or years <= 0:
        return "N/A"
    end_price = history["Close"].iloc[-1]
    start_price = history["Close"].iloc[0]
    if start_price <= 0:
        return "N/A"
    cagr = ((end_price / start_price) ** (1 / years) - 1) * 100
    return f"{cagr:.2f}%"


def update_value_metrics(file_path: Path, original_ticker: str) -> bool:
    if yf is None:
        raise RuntimeError("yfinance is required to fetch historical value metrics.")

    yf_ticker = stock_notes.yahoo_symbol(original_ticker)
    stock = yf.Ticker(yf_ticker)
    info = stock.info or {}

    hist_10y = stock.history(period="10y")
    if hist_10y.empty:
        hist_10y = stock.history(period="max")
    hist_5y = stock.history(period="5y")

    actual_years_10 = (hist_10y.index[-1] - hist_10y.index[0]).days / 365.25 if not hist_10y.empty else 0
    actual_years_5 = (hist_5y.index[-1] - hist_5y.index[0]).days / 365.25 if not hist_5y.empty else 0

    cagr_10y_str = get_cagr(hist_10y, actual_years_10) if actual_years_10 > 1 else "N/A"
    cagr_5y_str = get_cagr(hist_5y, actual_years_5) if actual_years_5 > 1 else "N/A"

    quote_currency = info.get("currency")
    financial_currency = info.get("financialCurrency") or quote_currency

    roe = info.get("returnOnEquity") or info.get("returnOnEquity_avg")
    roa = info.get("returnOnAssets")
    raw_dte = info.get("debtToEquity")
    debt_to_equity = f"{(raw_dte / 100):.2f}" if raw_dte is not None else "N/A"
    raw_peg = info.get("pegRatio")
    peg_ratio = f"{raw_peg:.2f}" if raw_peg is not None else "N/A"
    gross_margin = info.get("grossMargins")
    fcf = info.get("freeCashflow") or info.get("operatingCashflow")
    market_cap = info.get("marketCap")

    roe_str = f"{roe * 100:.2f}%" if roe is not None else "N/A"
    roa_str = f"{roa * 100:.2f}%" if roa is not None else "N/A"
    gm_str = f"{gross_margin * 100:.2f}%" if gross_margin is not None else "N/A"

    # Currency guard: do not compute cross-currency ratios
    currency_ok = stock_notes.check_currency_guard(financial_currency, quote_currency)
    if not currency_ok:
        fcf_yield_str = "currency_mismatch"
    elif fcf and market_cap and market_cap > 0:
        fcf_yield_str = f"{(fcf / market_cap) * 100:.2f}%"
    else:
        fcf_yield_str = "N/A"

    today_str = datetime.now().strftime("%Y-%m-%d")

    val_block = [
        "value_metrics:",
        f"  last_deep_fetch: {today_str}",
        f"  currency: {quote_currency or 'USD'}",
        "  returns:",
        f"    cagr_10y: {cagr_10y_str}",
        f"    cagr_5y: {cagr_5y_str}",
        "  quality:",
        f"    roe: {roe_str}",
        f"    roa: {roa_str}",
        f"    gross_margin: {gm_str}",
        f"    debt_to_equity: {debt_to_equity}",
        "  valuation:",
        f"    fcf_yield: {fcf_yield_str}",
        f"    peg_ratio: {peg_ratio}",
    ]

    content = file_path.read_text(encoding="utf-8")
    fm, body = stock_notes.split_note(content)
    if fm is None:
        return False

    fm = stock_notes.set_block(fm, "value_metrics", val_block)
    # Re-apply reverse DCF calculation based on the new fcf_yield
    fm, _ = stock_notes.apply_implied_growth(fm, ticker=original_ticker)

    new_content = stock_notes.join_note(fm, body)
    file_path.write_text(new_content, encoding="utf-8")
    print(f"Updated value metrics for {yf_ticker}")
    return True


def main():
    print("Updating historical value metrics...")
    if yf is None:
        print("Error: yfinance is not installed in the active environment.")
        sys.exit(1)

    updated = 0
    for path, ticker in stock_notes.iter_ticker_notes():
        try:
            if update_value_metrics(path, ticker):
                updated += 1
        except Exception as e:
            print(f"Error updating {ticker}: {e}")
    print(f"Completed. Updated {updated} notes.")


if __name__ == "__main__":
    main()
