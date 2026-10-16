"""Reverse DCF goal seeking for stock research notes.

Solves for the implied growth rate priced into a stock using
stock_notes.solve_implied_growth and updates value_metrics in frontmatter.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "16-Trading-and-Investing" / "scripts"))

import stock_notes  # noqa: E402

try:
    import yfinance as yf
except ImportError:
    yf = None


def update_implied_growth(file_path: Path, original_ticker: str) -> bool:
    content = file_path.read_text(encoding="utf-8")
    fm, body = stock_notes.split_note(content)
    if fm is None:
        return False

    val_block = stock_notes.get_block(fm, "value_metrics")
    if val_block is None:
        return False

    # First attempt: if live yfinance is available, solve from live price and FCF
    result = None
    if yf is not None:
        try:
            yf_ticker = stock_notes.yahoo_symbol(original_ticker)
            stock = yf.Ticker(yf_ticker)
            info = stock.info or {}
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            fcf = info.get("freeCashflow") or info.get("operatingCashflow")
            shares = info.get("sharesOutstanding")
            if price and fcf and shares and shares > 0:
                result = stock_notes.solve_implied_growth(price, fcf / shares)
        except Exception as e:
            print(f"Live fetch failed for {original_ticker}: {e}; falling back to stored fcf_yield")

    # Fallback: compute from stored fcf_yield in value_metrics
    if result is None:
        fields = stock_notes.block_fields(val_block)
        fcf_yield = stock_notes.parse_percent(fields.get("valuation.fcf_yield"))
        result = stock_notes.implied_growth_from_fcf_yield(fcf_yield)

    stale = ("implied_growth_rate:", "implied_growth_status:", "implied_growth_basis:")
    val_body = [line for line in val_block[1:] if not line.strip().startswith(stale)]
    new_block = [val_block[0], *stock_notes.implied_growth_lines(result), *val_body]

    fm = stock_notes.set_block(fm, "value_metrics", new_block)
    new_content = stock_notes.join_note(fm, body)
    file_path.write_text(new_content, encoding="utf-8")
    status_str = f"{result.rate * 100:.1f}%" if result.rate is not None else result.status
    print(f"Reverse DCF for {original_ticker}: {status_str}")
    return True


def main():
    print("Running Reverse DCF Goal Seeking...")
    updated = 0
    for path, ticker in stock_notes.iter_ticker_notes():
        try:
            if update_implied_growth(path, ticker):
                updated += 1
        except Exception as e:
            print(f"Failed Reverse DCF for {ticker}: {e}")
    print(f"Valuations Complete. Processed {updated} notes.")


if __name__ == "__main__":
    main()
