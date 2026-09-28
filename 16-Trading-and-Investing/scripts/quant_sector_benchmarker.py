import os
import re
import yaml

VAULT_ROOT = "16-Trading-and-Investing/Investing/Stock Research"

def extract_metrics(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'value_metrics:.*?\n(  .*?\n)+', content, flags=re.DOTALL)
    if not match: return None
    
    try:
        # Simplified parsing of the value_metrics block
        metrics = {}
        data = match.group(0)
        metrics['cagr_10y'] = re.search(r'cagr_10y: (.*?)%', data).group(1) if '%' in data else "0"
        metrics['roe'] = re.search(r'roe: (.*?)%', data).group(1) if 'roe' in data else "0"
        metrics['debt_equity'] = re.search(r'debt_to_equity: (.*?)\n', data).group(1) if 'debt_to_equity' in data else "0"
        metrics['fcf_yield'] = re.search(r'fcf_yield: (.*?)%', data).group(1) if 'fcf_yield' in data else "0"
        return metrics
    except:
        return None

def generate_sector_reports():
    sectors = [d for d in os.listdir(VAULT_ROOT) if os.path.isdir(os.path.join(VAULT_ROOT, d)) and d != "Historical"]
    
    for sector in sectors:
        print(f"Benchmarking Sector: {sector}...")
        sector_path = os.path.join(VAULT_ROOT, sector)
        stats = []

        for root, dirs, files in os.walk(sector_path):
            for file in files:
                if file.endswith(".md") and not file.startswith("_"):
                    m = extract_metrics(os.path.join(root, file))
                    if m:
                        name = file.replace(".md", "")
                        stats.append((name, m))

        if not stats: continue

        # Sort by ROE (Quality)
        stats.sort(key=lambda x: float(x[1]['roe'].replace(',', '')), reverse=True)

        content = f"""---
type: sector-analysis
tags: [quant, benchmark, {sector.lower()}]
---
# {sector} Global Benchmarking Report

## Quality Rankings (Sorted by ROE)
| Company | ROE (%) | 10y CAGR | D/E | FCF Yield |
| :--- | :--- | :--- | :--- | :--- |
"""
        for name, m in stats:
            content += f"| {name} | {m['roe']}% | {m['cagr_10y']}% | {m['debt_equity']} | {m['fcf_yield']}% |\n"

        content += f"""
## Investment Logic
- **Quality Dominance**: Higher ROE combined with low Debt/Equity indicates a strong structural moat ([[Economic Moat]]).
- **Growth Gap**: Compare 10y CAGR with current ROE to identify if the company is effectively reinvesting its capital.

---
[[16-Trading-and-Investing/Investing/Stock Research/_Index_Stock Research|Back to Global Research]]
"""
        with open(os.path.join(sector_path, "_Sector_Analysis.md"), 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    generate_sector_reports()
    print("Sector Benchmarking Complete.")
