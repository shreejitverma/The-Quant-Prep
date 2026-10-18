"""Migrate stock research notes to fix Phase 0 known defects.

- Relocates misplaced `market_data` and `last_updated` blocks into the frontmatter.
- Drops `market_data` recorded under another symbol (an ADR or an unrelated US listing).
- Normalizes `market_data`: removes placeholder values (None, null, 0) and derives `data_quality` from the fields present.
- Replaces placeholder zeros for D/E, PEG and FCF yield with N/A and blanks FCF yields of known currency mismatches.
- Replaces fake `implied_growth_rate: 0%` with solved rate or explicit failure status (missing_fcf, non_positive_fcf, currency_mismatch).
- Updates note status from `complete` to `status: stub` for boilerplate company notes.
- Strips body inline Dataview fields (status:: ..., priority:: ...) that conflict with frontmatter.
- Repairs corrupted frontmatter in Historical corporate failure case studies.

Every step is idempotent: a second run leaves the notes unchanged.
"""

from __future__ import annotations

import re
from pathlib import Path

import stock_notes

STOCK_ROOT = stock_notes.STOCK_ROOT

HISTORICAL_MAP = {
    "General Electric (The Fall from Godhood).md": ("GE", "General Electric"),
    "IBM (The Innovation Trap).md": ("IBM", "IBM"),
    "Kodak (The Digital Blindness).md": ("KODK", "Kodak"),
    "Nokia (The Platform Burning).md": ("NOK", "Nokia"),
    "Xerox (Missing the Graphic Interface).md": ("XRX", "Xerox"),
}


def migrate_historical_note(path: Path) -> None:
    filename = path.name
    if filename not in HISTORICAL_MAP:
        return
    ticker, company = HISTORICAL_MAP[filename]
    content = path.read_text(encoding="utf-8")

    # Match everything starting at the first Markdown heading '# Stock: ...'
    m_body = re.search(r"(# Stock:.*)", content, flags=re.DOTALL)
    if not m_body:
        return
    body = stock_notes.strip_inline_metadata(m_body.group(1)).strip()

    new_content = f"""---
ticker: {ticker}
company: {company}
tags: [investing, stock-research, historical, case-study]
status: historical-case
priority: low
---
{body}
"""
    path.write_text(new_content, encoding="utf-8")
    print(f"Migrated historical note: {filename}")


def migrate_ticker_note(path: Path, ticker: str) -> dict[str, int]:
    content = path.read_text(encoding="utf-8")

    # 1. Relocate misplaced blocks from body into frontmatter
    text, moved = stock_notes.relocate_misplaced_blocks(content)

    fm, body = stock_notes.split_note(text)
    if fm is None:
        raise stock_notes.NoteFormatError(f"Missing frontmatter in {path}")

    # Strip conflicting inline metadata fields from body
    body = stock_notes.strip_inline_metadata(body)

    # 2. Mark boilerplate company notes as status: stub only if currently complete
    status_block = stock_notes.get_block(fm, "status")
    if status_block is not None:
        curr_status = status_block[0].partition(":")[2].strip()
        if curr_status == "complete":
            fm = stock_notes.set_block(fm, "status", ["status: stub"])
    else:
        fm.append("status: stub")

    # 3. Drop data fetched from another listing, then normalize market data
    rejected = None
    try:
        fm, rejected = stock_notes.drop_foreign_listing_data(fm, stock_notes.fetch_symbol(path, ticker))
    except stock_notes.UnmappedTickerError as e:
        print(f"Not checking listing of {path.name}: {e}")
    if rejected:
        print(f"Dropped market data for {path.name}: recorded under {rejected}")
    fm, missing = stock_notes.normalize_market_data(fm)

    # 4. Replace placeholder zeros, then apply reverse DCF solve with currency check
    fm = stock_notes.normalize_value_metrics(fm, ticker=ticker)
    fm, implied_res = stock_notes.apply_implied_growth(fm, ticker=ticker)

    new_text = stock_notes.join_note(fm, body)
    path.write_text(new_text, encoding="utf-8")

    return {
        "moved": len(moved),
        "missing_price": 1 if "price" in missing else 0,
        "solved_growth": 1 if (implied_res and implied_res.status == "solved") else 0,
        "unsolved_growth": 1 if (implied_res and implied_res.status != "solved") else 0,
    }


def main():
    print("Starting stock research note migration...")
    totals = {
        "notes": 0,
        "moved": 0,
        "missing_price": 0,
        "solved_growth": 0,
        "unsolved_growth": 0,
        "historical": 0,
    }

    # Migrate standard ticker notes
    for path, ticker in stock_notes.iter_ticker_notes(STOCK_ROOT):
        stats = migrate_ticker_note(path, ticker)
        totals["notes"] += 1
        totals["moved"] += 1 if stats["moved"] > 0 else 0
        totals["missing_price"] += stats["missing_price"]
        totals["solved_growth"] += stats["solved_growth"]
        totals["unsolved_growth"] += stats["unsolved_growth"]

    # Migrate historical notes
    hist_dir = STOCK_ROOT / "Historical"
    if hist_dir.exists():
        for path in hist_dir.glob("*.md"):
            migrate_historical_note(path)
            totals["historical"] += 1

    print("Migration finished:")
    for k, v in totals.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
