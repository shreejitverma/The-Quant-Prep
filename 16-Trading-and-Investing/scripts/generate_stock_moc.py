"""Generate Global Stock Research Map of Content (MOC).

Maintains vault-root relative wikilinks, preserves the hand-authored Quant Suite links,
links every sector benchmark report found on disk, groups notes by the country folder they
live in, and sorts the Dataview superinvestor screener by ROE as a number with missing values last.
"""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VAULT_ROOT = REPO_ROOT / "16-Trading-and-Investing" / "Investing" / "Stock Research"


def generate_moc():
    print("Regenerating Global Stock Research MOC...")

    sections = {
        "Technology": {},
        "Financials": {},
        "Healthcare": {},
        "Consumer Staples": {},
        "Consumer Discretionary": {},
        "Energy": {},
        "Industrials": {},
        "Materials": {},
        "Communication Services": {},
        "Utilities": {},
    }

    historical = []

    for root, _dirs, files in os.walk(VAULT_ROOT):
        for file in sorted(files):
            if not file.endswith(".md") or file.startswith("_"):
                continue

            full_path = Path(root) / file
            rel_to_repo = full_path.relative_to(REPO_ROOT)
            wiki_path = str(rel_to_repo.with_suffix(""))
            disp_name = file.replace(".md", "")

            if "Historical" in full_path.parts:
                historical.append(f"- [[{wiki_path}|{disp_name}]]")
                continue

            parts = full_path.relative_to(VAULT_ROOT).parts
            sector = parts[0]
            if sector in sections:
                country = parts[1] if len(parts) >= 3 else "Other"
                sections[sector].setdefault(country, []).append(f"[[{wiki_path}|{disp_name}]]")

    benchmarks = [
        f"- **[[{path.relative_to(REPO_ROOT).with_suffix('')}|{path.parent.name} Benchmark]]**"
        for path in sorted(VAULT_ROOT.glob("*/_Sector_Analysis.md"))
    ]

    risk = "16-Trading-and-Investing/Investing/Risk Management/Correlation Matrix"
    macro = "16-Trading-and-Investing/Investing/Macro & Micro Economics/Global Macro Report"
    header = [
        "---",
        "type: MOC",
        "tags: [moc, investing, stocks, global-research, godhood]",
        "---",
        "# Global Stock Research Map of Content",
        "",
        '> "Price is what you pay. Value is what you get." - Warren Buffett',
        "",
        "## Quant Suite Intelligence",
        f"- **[[{risk}|Portfolio Correlation Matrix]]**: Identifying hidden risks and diversification offsets.",
        f"- **[[{macro}|Global Macro Report]]**: Live interest rate and volatility tracking.",
        "",
        "## Sector Benchmarking Reports",
        *benchmarks,
        "",
        "## Superinvestor Value Screener",
        "```dataview",
        "TABLE",
        '  value_metrics.quality.roe as "ROE",',
        '  value_metrics.implied_growth_rate as "Implied Growth",',
        '  value_metrics.returns.cagr_10y as "10y CAGR",',
        '  value_metrics.valuation.fcf_yield as "FCF Yield",',
        '  value_metrics.valuation.peg_ratio as "PEG"',
        'FROM "16-Trading-and-Investing/Investing/Stock Research"',
        "WHERE value_metrics != null",
        "SORT number(value_metrics.quality.roe) = null ASC, number(value_metrics.quality.roe) DESC",
        "```",
        "",
        "## Sector & Geography Intelligence",
    ]
    content = "\n".join(header) + "\n"

    for sector in sorted(sections.keys()):
        countries = sections[sector]
        if not countries:
            continue
        content += f"\n### {sector}\n"
        for country in sorted(countries.keys()):
            links = sorted(countries[country])
            content += f"- **{country}**: " + ", ".join(links) + "\n"

    if historical:
        content += "\n### Historical Cautionary Tales\n"
        content += "\n".join(sorted(historical))
        content += "\n"

    content += "\n---\n[[16-Trading-and-Investing/Investing/_Index_Investing|Back to Investing]]\n"

    moc_path = VAULT_ROOT / "_Index_Stock Research.md"
    moc_path.write_text(content, encoding="utf-8")
    print("MOC Polished.")


if __name__ == "__main__":
    generate_moc()
