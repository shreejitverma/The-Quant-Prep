"""Generate Global Stock Research Map of Content (MOC).

Maintains vault-root relative wikilinks, preserves hand-authored
Quant Suite and Sector Benchmarking links, and restores Implied Growth
in the Dataview superinvestor screener table.
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

    for root, dirs, files in os.walk(VAULT_ROOT):
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

            for sector in sections.keys():
                if sector in full_path.parts:
                    country = "Other"
                    for c in [
                        "US",
                        "India",
                        "Europe",
                        "China",
                        "Japan",
                        "Middle East",
                        "Sweden",
                        "South Korea",
                        "Taiwan",
                        "Brazil",
                        "Singapore",
                        "Indonesia",
                        "Thailand",
                        "Malaysia",
                    ]:
                        if c in full_path.parts:
                            country = c
                            break

                    if country not in sections[sector]:
                        sections[sector][country] = []
                    sections[sector][country].append(f"[[{wiki_path}|{disp_name}]]")
                    break

    content = """---
type: MOC
tags: [moc, investing, stocks, global-research, godhood]
---
# Global Stock Research Map of Content

> "Price is what you pay. Value is what you get." - Warren Buffett

## Quant Suite Intelligence
- **[[16-Trading-and-Investing/Investing/Risk Management/Correlation Matrix|Portfolio Correlation Matrix]]**: Identifying hidden risks and diversification offsets.
- **[[16-Trading-and-Investing/Investing/Macro & Micro Economics/Global Macro Report|Global Macro Report]]**: Live interest rate and volatility tracking.

## Sector Benchmarking Reports
- **[[16-Trading-and-Investing/Investing/Stock Research/Technology/_Sector_Analysis|Technology Benchmark]]** | **[[16-Trading-and-Investing/Investing/Stock Research/Financials/_Sector_Analysis|Financials Benchmark]]**
- **[[16-Trading-and-Investing/Investing/Stock Research/Healthcare/_Sector_Analysis|Healthcare Benchmark]]** | **[[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/_Sector_Analysis|Staples Benchmark]]**
- **[[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/_Sector_Analysis|Discretionary Benchmark]]** | **[[16-Trading-and-Investing/Investing/Stock Research/Industrials/_Sector_Analysis|Industrials Benchmark]]**

## Superinvestor Value Screener
```dataview
TABLE 
  value_metrics.quality.roe as "ROE", 
  value_metrics.implied_growth_rate as "Implied Growth",
  value_metrics.returns.cagr_10y as "10y CAGR",
  value_metrics.valuation.fcf_yield as "FCF Yield",
  value_metrics.valuation.peg_ratio as "PEG"
FROM "16-Trading-and-Investing/Investing/Stock Research"
WHERE value_metrics != null
SORT value_metrics.quality.roe DESC
```

## Sector & Geography Intelligence
"""

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
