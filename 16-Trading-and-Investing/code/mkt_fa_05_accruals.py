"""Sloan accruals and earnings quality: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/Investing/Fundamental-Analysis/05-Forensic-Accounting-Sloan-Accruals-and-Earnings-Quality.md`.
Independent routes used here:
- the statement totals (gross profit, current assets, total assets, current liabilities) re-summed from
  their lines, so the table is internally consistent before any ratio is taken;
- accruals by the cash flow statement method (net income minus CFO) and by Sloan's balance sheet method
  (working-capital changes less depreciation), with the gap between them reconciled line by line to the
  non-cash charges other than depreciation that only the cash flow method captures;
- DSO and DIO in exact fractions, and their year-on-year changes recomputed from the unrounded values.
The Sloan (1996) persistence coefficients and hedge returns are cited constants from the paper
(Table 3 and Table 6), not computed here.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_fa_05_accruals.py`.
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


Y1 = {
    "rev": F(500),
    "cogs": F(275),
    "sga": F(125),
    "ni": F(75),
    "cfo": F(80),
    "cash": F(40),
    "ar": F(60),
    "inv": F(70),
    "oca": F(20),
    "ppe": F(250),
    "ap": F(45),
    "accrued": F(25),
    "std": F(10),
    "dep": F(25),
}
Y2 = {
    "rev": F(650),
    "cogs": F(338),
    "sga": F(152),
    "ni": F(120),
    "cfo": F(45),
    "cash": F(35),
    "ar": F(135),
    "inv": F(110),
    "oca": F(30),
    "ppe": F(280),
    "ap": F(50),
    "accrued": F(28),
    "std": F(15),
    "dep": F(28),
}


def totals(y: dict[str, F]) -> dict[str, F]:
    gp = y["rev"] - y["cogs"]
    ca = y["cash"] + y["ar"] + y["inv"] + y["oca"]
    return {"gp": gp, "ebit": gp - y["sga"], "ca": ca, "ta": ca + y["ppe"], "cl": y["ap"] + y["accrued"] + y["std"]}


def table() -> None:
    print("Titan Technologies: table totals and growth ($M)")
    t1, t2 = totals(Y1), totals(Y2)
    exact("gross profit Y1, Y2", (t1["gp"], t2["gp"]), (225, 312))
    exact("EBIT Y1, Y2", (t1["ebit"], t2["ebit"]), (100, 160))
    exact("current assets Y1, Y2", (t1["ca"], t2["ca"]), (190, 310))
    exact("total assets Y1, Y2", (t1["ta"], t2["ta"]), (440, 590))
    exact("current liabilities Y1, Y2", (t1["cl"], t2["cl"]), (80, 93))
    rounded("gross margin Y1 (percent)", t1["gp"] / Y1["rev"], "45.0", 100)
    rounded("gross margin Y2 (percent)", t2["gp"] / Y2["rev"], "48.0", 100)
    for key, label, quoted in [
        ("rev", "revenue growth", "30.0"),
        ("ni", "net income growth", "60.0"),
        ("cfo", "CFO growth", "-43.8"),
        ("ar", "receivables growth", "125.0"),
        ("inv", "inventory growth", "57.1"),
    ]:
        rounded(f"{label} (percent)", Y2[key] / Y1[key] - 1, quoted, 100)
    rounded("EBIT growth (percent)", t2["ebit"] / t1["ebit"] - 1, "60.0", 100)


def accruals() -> None:
    print("Accruals by two methods ($M)")
    t1, t2 = totals(Y1), totals(Y2)
    avg_ta = (t1["ta"] + t2["ta"]) / 2
    exact("average total assets", avg_ta, F(515))
    cf1 = Y1["ni"] - Y1["cfo"]
    cf2 = Y2["ni"] - Y2["cfo"]
    exact("cash flow accruals Y1", cf1, -5)
    exact("cash flow accruals Y2", cf2, 75)
    rounded("Y1 accrual ratio on Y1 assets (percent)", cf1 / t1["ta"], "-1.14", 100)
    rounded("Y2 accrual ratio on average assets (percent)", cf2 / avg_ta, "14.56", 100)
    d_ca_ex_cash = (t2["ca"] - Y2["cash"]) - (t1["ca"] - Y1["cash"])
    d_cl_ex_std = (t2["cl"] - Y2["std"]) - (t1["cl"] - Y1["std"])
    exact("change in current assets ex cash", d_ca_ex_cash, 125)
    exact("current assets ex cash Y2, Y1", (t2["ca"] - Y2["cash"], t1["ca"] - Y1["cash"]), (275, 150))
    exact("change in current liabilities ex short-term debt", d_cl_ex_std, 8)
    exact("current liabilities ex short-term debt Y2, Y1", (t2["cl"] - Y2["std"], t1["cl"] - Y1["std"]), (78, 70))
    bs = d_ca_ex_cash - d_cl_ex_std - Y2["dep"]
    exact("balance sheet accruals", bs, 89)
    rounded("balance sheet accrual ratio (percent)", bs / avg_ta, "17.28", 100)
    # Reconcile: CFO = NI + dep + other non-cash charges - change in operating working capital.
    cfo_without_other = Y2["ni"] + Y2["dep"] - (d_ca_ex_cash - d_cl_ex_std)
    exact("CFO from net income, depreciation and working capital alone", cfo_without_other, 31)
    other_noncash = Y2["cfo"] - cfo_without_other
    exact("other non-cash charges implied by the reported CFO", other_noncash, 14)
    exact("balance sheet minus cash flow accruals", bs - cf2, other_noncash)


def activity() -> None:
    print("Activity ratios on year-end balances")
    dso1 = Y1["ar"] / Y1["rev"] * 365
    dso2 = Y2["ar"] / Y2["rev"] * 365
    dio1 = Y1["inv"] / Y1["cogs"] * 365
    dio2 = Y2["inv"] / Y2["cogs"] * 365
    rounded("DSO Y1", dso1, "43.8")
    rounded("DSO Y2", dso2, "75.8")
    rounded("DSO change (days)", dso2 - dso1, "32.0")
    rounded("DSO change (percent)", dso2 / dso1 - 1, "73", 100)
    rounded("DIO Y1", dio1, "92.9")
    rounded("DIO Y2", dio2, "118.8")
    rounded("DIO change (days)", dio2 - dio1, "25.9")
    rounded("DIO change (whole days)", dio2 - dio1, "26")
    rounded("DIO change (percent)", dio2 / dio1 - 1, "28", 100)


def sloan_constants() -> None:
    print("Cited constants, Sloan (1996), 40,679 firm-years 1962-1991")
    gamma_accruals, gamma_cash = 0.765, 0.855  # Table 3 pooled persistence coefficients
    hedge = (0.104, 0.048, 0.029)  # Table 6 size-adjusted hedge returns, years t+1 to t+3
    highest = (-0.055, -0.032, -0.022)  # Table 6 highest-accrual decile, years t+1 to t+3
    assert gamma_accruals < gamma_cash
    print(f"    persistence: accruals = {gamma_accruals}, cash flows = {gamma_cash}")
    print(f"    hedge returns t+1, t+2, t+3 = {hedge}")
    print(f"    highest-accrual decile t+1, t+2, t+3 = {highest}")


if __name__ == "__main__":
    table()
    accruals()
    activity()
    sloan_constants()
    print("all accrual numbers check out")
