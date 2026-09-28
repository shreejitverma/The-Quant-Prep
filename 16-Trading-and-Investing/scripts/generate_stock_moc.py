import os
import re

VAULT_ROOT = "16-Trading-and-Investing/Investing/Stock Research"

def generate_moc():
    print("Regenerating Global Stock Research MOC (Final Polish)...")
    
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
        "Utilities": {}
    }
    
    historical = []

    for root, dirs, files in os.walk(VAULT_ROOT):
        for file in files:
            if not file.endswith(".md") or file.startswith("_Index"): continue
            
            rel_path = os.path.relpath(os.path.join(root, file), ".")
            wiki_path = rel_path.replace(".md", "")
            
            if "Historical" in root:
                historical.append(f"- [[{wiki_path}|{file.replace('.md', '')}]]")
                continue
            
            for sector in sections.keys():
                if sector in root:
                    country = "Other"
                    for c in ["US", "India", "Europe", "China", "Japan", "Middle East", "Sweden", "South Korea", "Taiwan", "Brazil", "Singapore", "Indonesia", "Thailand", "Malaysia"]:
                        if c in root:
                            country = c
                            break
                    
                    if country not in sections[sector]:
                        sections[sector][country] = []
                    sections[sector][country].append(f"[[{wiki_path}|{file.replace('.md', '')}]]")
                    break

    content = """---
type: MOC
tags: [moc, investing, stocks, value-investing, godhood]
---
# Global Stock Research Map of Content

> "Price is what you pay. Value is what you get." - Warren Buffett

## Economic Intelligence
- **[[16-Trading-and-Investing/Investing/Macro & Micro Economics/Global Macro Report|Global Macro Report]]**: Interest Rates, Volatility, and Indices.
- **[[16-Trading-and-Investing/Investing/Macro & Micro Economics/Sector & Commodity Report|Sector & Commodity Report]]**: Oil, Gold, and Industrial Metals.

## Superinvestor Value Screener
```dataview
TABLE 
  value_metrics.returns.cagr_10y as "10y CAGR", 
  value_metrics.quality.roe as "ROE", 
  value_metrics.quality.debt_to_equity as "D/E",
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
        if not countries: continue
        content += f"\n### {sector}\n"
        for country in sorted(countries.keys()):
            links = sorted(countries[country])
            content += f"- **{country}**: " + ", ".join(links) + "\n"

    if historical:
        content += "\n### Historical Cautionary Tales\n"
        content += "\n".join(sorted(historical))
        content += "\n"

    content += "\n---\n[[Dashboard|Back to Dashboard]]\n"

    with open(f"{VAULT_ROOT}/_Index_Stock Research.md", 'w', encoding='utf-8') as f:
        f.write(content)
    print("MOC Polished.")

if __name__ == "__main__":
    generate_moc()
