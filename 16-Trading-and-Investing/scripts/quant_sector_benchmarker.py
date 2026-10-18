"""Write a benchmarking report per sector from each ticker note's `value_metrics`.

Missing values stay missing: a note without a figure shows N/A, and ROE ranks it last.
Notes that cannot be benchmarked are listed under "Not benchmarked" with the reason, never dropped.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "16-Trading-and-Investing" / "scripts"))

import stock_notes  # noqa: E402

VAULT_ROOT = stock_notes.STOCK_ROOT

# Report column to dotted `value_metrics` field.
FIELDS = {
    "roe": "quality.roe",
    "cagr_10y": "returns.cagr_10y",
    "debt_equity": "quality.debt_to_equity",
    "fcf_yield": "valuation.fcf_yield",
}
_ABSENT = ("N/A", "n/a", "None", "null", "")


def extract_metrics(text: str) -> dict[str, str | None]:
    """Report fields from a note's `value_metrics`; None marks a missing value.

    Raises NoteFormatError when the note has no frontmatter or no `value_metrics` block.
    """
    fm, _ = stock_notes.split_note(text)
    if fm is None:
        raise stock_notes.NoteFormatError("no frontmatter")
    block = stock_notes.get_block(fm, "value_metrics")
    if block is None:
        raise stock_notes.NoteFormatError("no value_metrics block")
    fields = stock_notes.block_fields(block)
    return {name: (None if fields.get(key, "") in _ABSENT else fields[key]) for name, key in FIELDS.items()}


def roe_sort_key(row: tuple[str, dict[str, str | None]]) -> tuple[bool, float, str]:
    """Highest ROE first; a missing or non-numeric ROE sorts after every number."""
    name, metrics = row
    roe = stock_notes.parse_percent(metrics["roe"])
    return (roe is None, -(roe or 0.0), name)


def collect_sector(sector_path: Path) -> tuple[list[tuple[str, dict[str, str | None]]], list[tuple[str, str]]]:
    """Return (rows sorted by ROE, skipped notes with reasons) for one sector folder."""
    rows: list[tuple[str, dict[str, str | None]]] = []
    skipped: list[tuple[str, str]] = []
    for path in sorted(sector_path.rglob("*.md")):
        if path.name.startswith("_"):
            continue
        try:
            rows.append((path.stem, extract_metrics(path.read_text(encoding="utf-8"))))
        except (stock_notes.NoteFormatError, OSError, UnicodeDecodeError) as e:
            skipped.append((path.stem, str(e)))
    rows.sort(key=roe_sort_key)
    return rows, skipped


def render_report(sector: str, rows: list[tuple[str, dict[str, str | None]]], skipped: list[tuple[str, str]]) -> str:
    def cell(value: str | None) -> str:
        return stock_notes.MISSING if value is None else value

    content = f"""---
type: sector-analysis
tags: [quant, benchmark, {sector.lower()}]
---
# {sector} Global Benchmarking Report

## Quality Rankings (Sorted by ROE)
| Company | ROE (%) | 10y CAGR | D/E | FCF Yield |
| :--- | :--- | :--- | :--- | :--- |
"""
    for name, m in rows:
        content += f"| {name} | {cell(m['roe'])} | {cell(m['cagr_10y'])} | {cell(m['debt_equity'])} | {cell(m['fcf_yield'])} |\n"

    if skipped:
        content += "\n## Not benchmarked\n"
        for name, reason in skipped:
            content += f"- {name}: {reason}\n"

    content += """
## Investment Logic
- **Quality Dominance**: Higher ROE combined with low Debt/Equity indicates a strong structural moat ([Economic Moat](obsidian://open?vault=shreejit-verma-obsidian&file=Mental%20Models%2FWarren%20Buffett%2FEconomic%20Moat)).
- **Growth Gap**: Compare 10y CAGR with current ROE to identify if the company is effectively reinvesting its capital.

---
[[16-Trading-and-Investing/Investing/Stock Research/_Index_Stock Research|Back to Global Research]]
"""
    return content


def generate_sector_reports(root: Path = VAULT_ROOT) -> None:
    sectors = sorted(d for d in root.iterdir() if d.is_dir() and d.name != "Historical")
    for sector_path in sectors:
        print(f"Benchmarking Sector: {sector_path.name}...")
        rows, skipped = collect_sector(sector_path)
        for name, reason in skipped:
            print(f"  Skipped {name}: {reason}")
        if not rows:
            print(f"  No benchmarkable notes in {sector_path.name}; report not written")
            continue
        report = render_report(sector_path.name, rows, skipped)
        (sector_path / "_Sector_Analysis.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    generate_sector_reports()
    print("Sector Benchmarking Complete.")
