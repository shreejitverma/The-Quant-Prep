"""ROIC decomposition and DuPont analysis: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/Investing/Fundamental-Analysis/04-ROIC-Decomposition-and-DuPont-Analysis.md`.
Independent routes used here:
- invested capital from the asset side (operating approach) and from the funding side (financing
  approach) of a balance sheet that is first checked to balance;
- ROIC as NOPAT over invested capital and as margin times turnover from their own inputs, and ROE as
  net income over equity against the product of the five DuPont factors;
- EVA as NOPAT minus the capital charge and as the rounded spread times invested capital;
- the growth identity g = reinvestment rate x ROIIC by simulating twenty years of a firm that adds the
  reinvested share of NOPAT to its invested capital each year and earns NOPAT as its base NOPAT plus
  ROIIC times the cumulative new capital, then measuring the realized NOPAT growth, and the
  value-destroying 8% case by summing the simulated firm's EVA.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_fa_04_roic_dupont.py`.
"""

from __future__ import annotations

from fractions import Fraction as F


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    items = value if isinstance(value, tuple) else (value,)
    shown = ", ".join(f"{float(v):g}" if isinstance(v, F) and v.denominator != 1 else str(v) for v in items)
    print(f"    {label} = {shown}")


def rounded(label: str, value, expected: str, scale: float = 1.0) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{float(value) * scale:.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"    {label} = {shown}")


def enterprise_corp() -> None:
    print("Enterprise Corp ($M)")
    rev, ebit, interest, t = F(1000), F(150), F(20), F(25, 100)
    ebt = ebit - interest
    tax = t * ebt
    ni = ebt - tax
    exact("EBT", ebt, 130)
    exact("income taxes", tax, F(65, 2))
    exact("net income", ni, F(195, 2))
    cash, op_cash, ar, inv, ppe, gw = F(80), F(20), F(120), F(100), F(400), F(150)
    ap, accrued, std, ltd, equity = F(70), F(130), F(30), F(170), F(450)
    assets = cash + ar + inv + ppe + gw
    funding = ap + accrued + std + ltd + equity
    exact("total assets", assets, 850)
    exact("total liabilities and equity", funding, 850)
    excess = cash - op_cash
    exact("excess cash", excess, 60)
    nopat = ebit * (1 - t)
    exact("NOPAT", nopat, F(225, 2))
    op_ca = op_cash + ar + inv
    nibcl = ap + accrued
    owc = op_ca - nibcl
    exact("operating current assets", op_ca, 240)
    exact("NIBCL", nibcl, 200)
    exact("operating working capital", owc, 40)
    ic_operating = owc + ppe + gw
    exact("invested capital (operating approach)", ic_operating, 590)
    total_debt = std + ltd
    exact("total debt", total_debt, 200)
    ic_financing = total_debt + equity - excess
    exact("invested capital (financing approach)", ic_financing, 590)
    roic = nopat / ic_operating
    rounded("ROIC (percent)", roic, "19.07", 100)
    margin, turnover = nopat / rev, rev / ic_financing
    rounded("NOPAT margin (percent)", margin, "11.25", 100)
    rounded("capital turnover", turnover, "1.6949")
    rounded("margin x turnover (percent)", margin * turnover, "19.07", 100)
    rounded("rounded inputs 11.25% x 1.6949 (percent)", 0.1125 * 1.6949, "19.07", 100)
    wacc = F(9, 100)
    rounded("economic spread (percent)", roic - wacc, "10.07", 100)
    eva = nopat - wacc * ic_operating
    exact("EVA (NOPAT - WACC x IC)", eva, F(594, 10))
    rounded("EVA (rounded spread 10.07% x 590)", F(1007, 10000) * 590, "59.4")
    roe = ni / equity
    rounded("ROE (percent)", roe, "21.67", 100)
    factors = {
        "tax burden": (ni / ebt, "0.7500"),
        "interest burden": (ebt / ebit, "0.8667"),
        "EBIT margin": (ebit / rev, "0.1500"),
        "asset turnover": (rev / assets, "1.1765"),
        "financial leverage": (assets / equity, "1.8889"),
    }
    product = F(1)
    for name, (value, quoted) in factors.items():
        rounded(name, value, quoted)
        product *= value
    rounded("product of the five DuPont factors (percent)", product, "21.67", 100)
    prod_rounded = 1.0
    for _, quoted in factors.values():
        prod_rounded *= float(quoted)
    rounded("product of the rounded factors (percent)", prod_rounded, "21.67", 100)
    rounded("asset turnover (two decimals)", rev / assets, "1.18")
    rounded("financial leverage (two decimals)", assets / equity, "1.89")
    rounded("interest burden (two decimals)", ebt / ebit, "0.87")


def simulate_growth(roiic: float, reinvest: float, years: int = 20) -> float:
    """Firm with base NOPAT 100 that adds a share of NOPAT to capital each year; new capital earns ROIIC."""
    base_nopat, new_capital, history = 100.0, 0.0, []
    for _ in range(years):
        nopat = base_nopat + roiic * new_capital
        history.append(nopat)
        new_capital += reinvest * nopat
    growth = (history[-1] / history[0]) ** (1 / (years - 1)) - 1
    return growth


def growth_identity() -> None:
    print("Growth identity g = reinvestment rate x ROIIC (simulated firm)")
    g = simulate_growth(0.25, 0.60)
    rounded("25% ROIIC, 60% reinvested: realized growth (percent)", g, "15.0", 100)
    g = simulate_growth(0.30, 0.50)
    rounded("card: 30% ROIIC, 50% reinvested (percent)", g, "15.0", 100)
    g = simulate_growth(0.08, 1.00)
    rounded("8% ROIIC, 100% reinvested (percent)", g, "8.0", 100)
    # Value destruction at a 9% WACC: each reinvested dollar earns 8% but costs 9%.
    capital, eva_sum = 1000.0, 0.0
    for _ in range(20):
        nopat = 0.08 * capital
        eva_sum += nopat - 0.09 * capital
        capital += nopat
    assert eva_sum < 0
    print(f"    8% ROIIC against a 9% WACC: 20-year EVA sum = {eva_sum:.1f} (negative)")


def margin_turnover_card() -> None:
    print("Card: halve the margin and double the turnover")
    rev, nopat, ic = F(1000), F(225, 2), F(590)
    half_margin, double_turnover = (nopat / rev) / 2, (2 * rev) / ic
    rounded("Enterprise Corp ROIC at half the margin and twice the turnover (percent)", half_margin * double_turnover, "19.07", 100)


if __name__ == "__main__":
    enterprise_corp()
    growth_identity()
    margin_turnover_card()
    print("all ROIC and DuPont numbers check out")
