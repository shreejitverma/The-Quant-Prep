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

    result = None
    basis = None

    # First attempt: if live yfinance is available, solve from live price and FCF
    if original_ticker in stock_notes.KNOWN_CURRENCY_MISMATCHES:
        result = stock_notes.ImpliedGrowth(stock_notes.CURRENCY_MISMATCH)
        basis = "currency_mismatch known cross-currency listing"
    elif yf is not None:
        yf_ticker = stock_notes.fetch_symbol(file_path, original_ticker)
        try:
            stock = yf.Ticker(yf_ticker)
            info = stock.info or {}

            price, quote_curr = stock_notes.to_major_unit(info.get("currentPrice") or info.get("regularMarketPrice"), info.get("currency"))
            fin_curr = info.get("financialCurrency") or quote_curr
            fcf = info.get("freeCashflow")
            shares = info.get("sharesOutstanding")
            if not stock_notes.check_currency_guard(fin_curr, quote_curr):
                result = stock_notes.ImpliedGrowth(stock_notes.CURRENCY_MISMATCH)
                basis = f"currency_mismatch financial={fin_curr} quote={quote_curr}"
            elif price and shares and shares > 0:
                basis = (
                    f"fcf_per_share r={stock_notes.DCF_DISCOUNT_RATE:.0%} "
                    f"terminal={stock_notes.DCF_TERMINAL_GROWTH:.0%} "
                    f"years={stock_notes.DCF_YEARS} range={stock_notes.DCF_GROWTH_LOW:.0%} to {stock_notes.DCF_GROWTH_HIGH:.0%}"
                )
                result = stock_notes.implied_growth_from_fcf_yield(None if fcf is None else fcf / shares / price)
        except Exception as e:
            print(f"Live fetch failed for {original_ticker}: {e}; falling back to stored fcf_yield")

    # Fallback: compute from stored fcf_yield in value_metrics
    if result is None:
        stored = stock_notes.block_fields(val_block).get("valuation.fcf_yield")
        result = stock_notes.implied_growth_from_stored_yield(stored, ticker=original_ticker)
        basis = (
            f"fcf_yield r={stock_notes.DCF_DISCOUNT_RATE:.0%} "
            f"terminal={stock_notes.DCF_TERMINAL_GROWTH:.0%} "
            f"years={stock_notes.DCF_YEARS} range={stock_notes.DCF_GROWTH_LOW:.0%} to {stock_notes.DCF_GROWTH_HIGH:.0%}"
        )

    fm = stock_notes.replace_implied_growth(fm, result, basis)
    new_content = stock_notes.join_note(fm, body)
    file_path.write_text(new_content, encoding="utf-8")
    status_str = stock_notes.format_rate(result.rate) if result.rate is not None else result.status
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
