"""Filings forensics case study: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/Investing/Fundamental-Analysis/08-Financial-Filings-Forensics-10K-Footnotes-and-Red-Flags.md`.
Independent routes used here:
- the tax footnote by rebuilding the income statement from pre-tax income downwards (statutory tax less
  the valuation-allowance release) and checking that it lands on the reported net income and tax line;
- the effective tax rate as reported tax over pre-tax income and as the statutory rate less the
  release's rate effect;
- EBITDA from the top (operating profit plus D&A) and from the bottom (net income plus tax, interest and
  D&A), before the add-backs that turn it into "Adjusted EBITDA";
- every percentage change from the opening and closing balances in exact fractions.
The filing deadlines (Form 10-K, 10-Q, 8-K, Form 4) are cited constants from the SEC forms.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_fa_08_filings.py`.
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


def tax_footnote() -> None:
    print("Tax reconciliation ($M)")
    pretax, statutory, release = F(132), F(21, 100), F("15.72")
    expected_tax = statutory * pretax
    exact("expected tax at 21%", expected_tax, F("27.72"))
    reported_tax = expected_tax - release
    exact("reported tax expense", reported_tax, 12)
    exact("net income (pre-tax less reported tax)", pretax - reported_tax, 120)
    etr = reported_tax / pretax
    rounded("effective tax rate (percent)", etr, "9.1", 100)
    rounded("effective rate as statutory less release effect (percent)", statutory - release / pretax, "9.1", 100)
    rounded("release as a share of net income (percent)", release / (pretax - reported_tax), "13.1", 100)


def contract_balances() -> None:
    print("Revenue footnote balances ($M)")
    for label, opening, closing, d_quoted, pct_quoted in [
        ("contract assets", 20, 65, 45, "225.0"),
        ("billed receivables", 100, 120, 20, "20.0"),
        ("deferred revenue", 180, 140, -40, "-22.2"),
        ("RPO", 400, 310, -90, "-22.5"),
    ]:
        exact(f"{label} change", closing - opening, d_quoted)
        rounded(f"{label} change (percent)", F(closing, opening) - 1, pct_quoted, 100)


def compensation() -> None:
    print("Adjusted EBITDA bridge ($M)")
    op_profit, interest, da, sbc, restructuring = F(140), F(8), F(40), F(85), F(25)
    exact("pre-tax income (operating profit less interest)", op_profit - interest, 132)
    ebitda_top = op_profit + da
    ni, tax = F(120), F(12)
    ebitda_bottom = ni + tax + interest + da
    exact("EBITDA from operating profit", ebitda_top, 180)
    exact("EBITDA from net income", ebitda_bottom, 180)
    addbacks = da + sbc + restructuring
    exact("total add-backs to operating profit", addbacks, 150)
    adjusted = op_profit + addbacks
    exact("Adjusted EBITDA", adjusted, 290)
    exact("SBC plus restructuring", sbc + restructuring, 110)
    rounded("uplift over plain EBITDA (percent)", adjusted / ebitda_bottom - 1, "61.1", 100)


def deadlines() -> None:
    print("Cited constants: SEC filing deadlines")
    k10 = {"large accelerated": 60, "accelerated": 75, "non-accelerated": 90}  # Form 10-K Gen. Instr. A
    q10 = {"large accelerated": 40, "accelerated": 40, "non-accelerated": 45}  # Form 10-Q Gen. Instr. A
    print(f"    10-K days after fiscal year-end = {k10}")
    print(f"    10-Q days after quarter-end = {q10}")
    print("    8-K = 4 business days; Form 4 = 2 business days")


if __name__ == "__main__":
    tax_footnote()
    contract_balances()
    compensation()
    deadlines()
    print("all filings numbers check out")
