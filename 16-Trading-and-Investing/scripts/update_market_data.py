"""Update market data blocks in stock research notes via yfinance.

Uses stock_notes helpers to maintain clean YAML frontmatter,
record data quality accurately, and never misplace blocks below fences.
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


def update_stock_file(file_path: Path, original_ticker: str) -> bool:
    if yf is None:
        raise RuntimeError("yfinance is required to fetch market data; install it with pip or conda.")

    yf_ticker = stock_notes.yahoo_symbol(original_ticker)
    stock = yf.Ticker(yf_ticker)
    info = stock.info or {}

    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    market_cap = info.get("marketCap")
    pe_ratio = info.get("trailingPE")
    div_yield = info.get("dividendYield")
    high_52 = info.get("fiftyTwoWeekHigh")
    low_52 = info.get("fiftyTwoWeekLow")
    currency = info.get("currency", "USD")

    missing = []
    if current_price is None or current_price == 0:
        missing.append("price")
    if market_cap is None or market_cap == 0:
        missing.append("market_cap")

    market_data_block = [
        "market_data:",
        f"  ticker: {yf_ticker}",
        f"  currency: {currency}",
    ]
    if current_price and current_price > 0:
        market_data_block.append(f"  price: {current_price}")
    if market_cap and market_cap > 0:
        market_data_block.append(f"  market_cap: {market_cap}")
    if pe_ratio is not None and pe_ratio > 0:
        market_data_block.append(f"  pe_ratio: {pe_ratio:.2f}")
    if div_yield is not None:
        if current_price and current_price > 0:
            market_data_block.append(f"  dividend_yield: {div_yield:.2f}")
        elif div_yield > 0:
            market_data_block.append(f"  dividend_yield: {div_yield:.2f}")
    if high_52 and high_52 > 0:
        market_data_block.append(f"  52w_high: {high_52}")
    if low_52 and low_52 > 0:
        market_data_block.append(f"  52w_low: {low_52}")

    quality = "missing" if missing else "ok"
    market_data_block.append(f"  data_quality: {quality}")
    if missing:
        market_data_block.append(f"  missing: {' '.join(missing)}")

    content = file_path.read_text(encoding="utf-8")
    fm, body = stock_notes.split_note(content)
    if fm is None:
        print(f"Skipping {file_path}: no frontmatter")
        return False

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fm = stock_notes.set_block(fm, "last_updated", [f"last_updated: {now_str}"])
    fm = stock_notes.set_block(fm, "market_data", market_data_block)

    new_content = stock_notes.join_note(fm, body)
    file_path.write_text(new_content, encoding="utf-8")
    print(f"Updated {yf_ticker} (quality: {quality})")
    return True


def main():
    print(f"Starting Quant OS Market Data Update at {datetime.now()}...")
    if yf is None:
        print("Error: yfinance is not installed in the active environment.")
        sys.exit(1)

    updated = 0
    failed = 0
    for path, ticker in stock_notes.iter_ticker_notes():
        try:
            if update_stock_file(path, ticker):
                updated += 1
        except Exception as e:
            print(f"Failed to update {ticker}: {e}")
            failed += 1

    print(f"Update Complete. Updated: {updated}, Failed: {failed}")


if __name__ == "__main__":
    main()
