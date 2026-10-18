"""Update market data blocks in stock research notes via yfinance.

Uses stock_notes helpers to maintain clean YAML frontmatter,
record data quality accurately, and never misplace blocks below fences.
A fetch that returns no price leaves the note untouched, so `last_updated` only moves on real data.
Minor-unit quotes (GBp) are converted to the major unit before they are written.
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

    yf_ticker = stock_notes.fetch_symbol(file_path, original_ticker)
    stock = yf.Ticker(yf_ticker)
    info = stock.info or {}

    raw_currency = info.get("currency")
    current_price, currency = stock_notes.to_major_unit(info.get("currentPrice") or info.get("regularMarketPrice"), raw_currency)
    high_52, _ = stock_notes.to_major_unit(info.get("fiftyTwoWeekHigh"), raw_currency)
    low_52, _ = stock_notes.to_major_unit(info.get("fiftyTwoWeekLow"), raw_currency)
    market_cap = info.get("marketCap")
    pe_ratio = info.get("trailingPE")
    div_yield = info.get("dividendYield")

    if not current_price or current_price <= 0:
        print(f"Skipping {yf_ticker}: fetch returned no price")
        return False

    content = file_path.read_text(encoding="utf-8")
    fm, body = stock_notes.split_note(content)
    if fm is None:
        print(f"Skipping {file_path}: no frontmatter")
        return False

    market_data_block = ["market_data:", f"  ticker: {yf_ticker}"]
    if currency:
        market_data_block.append(f"  currency: {currency}")
    market_data_block.append(f"  price: {current_price}")
    if market_cap and market_cap > 0:
        market_data_block.append(f"  market_cap: {market_cap}")
    if pe_ratio is not None and pe_ratio > 0:
        market_data_block.append(f"  pe_ratio: {pe_ratio:.2f}")
    if div_yield is not None:
        market_data_block.append(f"  dividend_yield: {div_yield:.2f}")
    if high_52 and high_52 > 0:
        market_data_block.append(f"  52w_high: {high_52}")
    if low_52 and low_52 > 0:
        market_data_block.append(f"  52w_low: {low_52}")
    fm = stock_notes.set_block(fm, "market_data", market_data_block)
    fm, missing = stock_notes.normalize_market_data(fm)
    quality = "missing" if missing else "ok"

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fm = stock_notes.set_block(fm, "last_updated", [f"last_updated: {now_str}"])

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
    skipped = 0
    failed = 0
    for path, ticker in stock_notes.iter_ticker_notes():
        try:
            if update_stock_file(path, ticker):
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"Failed to update {ticker}: {e}")
            failed += 1

    print(f"Update Complete. Updated: {updated}, Skipped: {skipped}, Failed: {failed}")


if __name__ == "__main__":
    main()
