"""Statement Forensics Drills: every number in the six worked solutions.

Backs every number in `16-Trading-and-Investing/30-Drills/Statement-Forensics-Drills.md`.
Independent routes used here:
- Drill 1 accruals: the Sloan (1996) balance-sheet accrual from line-item deltas, checked against the change in
  the level of non-cash operating working capital, both in exact `fractions.Fraction` arithmetic;
- Drill 2 DSO: the prior-year fourth-quarter revenue implied by differencing the trailing-twelve-month row,
  checked against the quarterly table, so the year-over-year growth uses an input the table itself implies;
- Drill 3 capitalised costs: gross margins and the adjusted cash flows recomputed from the table inputs;
- Drill 4 M-score: exact rational sum of the eight weighted terms, checked against a float dot product;
- Drill 5 absorption costing: gross profit by unit cost times units sold, checked against total production cost
  less the cost left in ending inventory, and against variable-costing profit plus the deferred overhead;
- Drill 6 valuation allowance: net income and the effective tax rate recomputed from the tax lines.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_drill_02_statement_forensics.py`.
"""

from __future__ import annotations

from fractions import Fraction as F

import numpy as np


def approx(label: str, value, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(float(value) - expected) <= tol, f"{label}: computed {float(value)!r}, quoted {expected}"
    print(f"    {label} = {float(value):.{decimals}f}")


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def drill1() -> None:
    print("Drill 1: Sloan accruals")
    prev = {"ta": F(1000), "ni": F(80), "cash": F(100), "ca": F(350), "cl": F(150), "std": F(20), "cfo": F(75)}
    cur = {"ta": F(1250), "ni": F(140), "cash": F(90), "ca": F(520), "cl": F(170), "std": F(25), "dep": F(45), "cfo": F(60)}
    d = {k: cur[k] - prev[k] for k in ("ca", "cash", "cl", "std")}
    exact("change in current assets", d["ca"], F(170))
    exact("change in cash", d["cash"], F(-10))
    exact("change in current liabilities", d["cl"], F(20))
    exact("change in short-term debt", d["std"], F(5))
    exact("change in operating current liabilities", d["cl"] - d["std"], F(15))
    acc_bs = (d["ca"] - d["cash"]) - (d["cl"] - d["std"]) - cur["dep"]

    # Route B: level of non-cash operating working capital in each year.
    def nowc(y: dict) -> F:
        return (y["ca"] - y["cash"]) - (y["cl"] - y["std"])

    assert nowc(cur) - nowc(prev) - cur["dep"] == acc_bs
    exact("change in non-cash current assets", d["ca"] - d["cash"], F(180))
    exact("balance-sheet accruals", acc_bs, F(120))
    acc_cf = cur["ni"] - cur["cfo"]
    exact("cash-flow accruals", acc_cf, F(80))
    avg_ta = (prev["ta"] + cur["ta"]) / 2
    exact("average total assets", avg_ta, F(1125))
    approx("scaled BS accruals (percent)", 100 * acc_bs / avg_ta, 10.67, 2)
    approx("scaled CF accruals (percent)", 100 * acc_cf / avg_ta, 7.11, 2)
    approx("net income growth (percent)", 100 * (cur["ni"] / prev["ni"] - 1), 75.0, 1)
    approx("CFO change (percent)", 100 * (cur["cfo"] / prev["cfo"] - 1), -20.0, 1)


def drill2() -> None:
    print("Drill 2: DSO")
    rev = [F(200), F(210), F(220), F(280)]
    ar = [F(130), F(150), F(185), F(270)]
    ttm = [F(800), F(820), F(850), F(910)]
    for i, q in enumerate([58.5, 64.3, 75.7, 86.8]):
        approx(f"DSO Q{i + 1}", ar[i] / rev[i] * 90, q, 1)
    exact("TTM at Q4 equals the four quarters", sum(rev), ttm[3])
    # TTM(Q4) - TTM(Q3) = Q4 - prior-year Q4.
    prior_q4 = rev[3] - (ttm[3] - ttm[2])
    exact("prior-year Q4 revenue implied by the TTM row", prior_q4, F(220))
    prior_ar = F(135)
    approx("Q4 revenue growth (percent)", 100 * (rev[3] / prior_q4 - 1), 27.3, 1)
    approx("Q4 receivables growth (percent)", 100 * (ar[3] / prior_ar - 1), 100.0, 1)
    approx("receivables growth / revenue growth", (ar[3] / prior_ar - 1) / (rev[3] / prior_q4 - 1), 3.7, 1)


def drill3() -> None:
    print("Drill 3: capitalised line costs")
    rev = [F(500), F(520), F(540)]
    line = [F(220), F(180), F(120)]
    for i, q in enumerate([56.0, 65.4, 77.8]):
        approx(f"gross margin year {i + 1} (percent)", 100 * (1 - line[i] / rev[i]), q, 1)
    approx("baseline line cost share of revenue (percent)", 100 * line[0] / rev[0], 44.0, 1)
    approx("PP&E growth years 1 to 3 (percent)", 100 * (F(680) / F(400) - 1), 70.0, 1)
    true_line = F(44, 100) * rev[2]
    approx("true line cost year 3", true_line, 237.6, 1)
    improper = true_line - line[2]
    approx("improperly capitalised", improper, 117.6, 1)
    adj_cfo = F(240) - improper
    adj_capex = F(230) - improper
    approx("adjusted CFO", adj_cfo, 122.4, 1)
    approx("adjusted capex", adj_capex, 112.4, 1)
    approx("adjusted FCF", adj_cfo - adj_capex, 10.0, 1)
    approx("reported FCF", F(240) - F(230), 10.0, 1)
    approx("CFO overstatement (percent)", 100 * (F(240) / adj_cfo - 1), 96.1, 1)


def drill4() -> None:
    print("Drill 4: Beneish M-score")
    coef = {"const": F(-484, 100), "DSRI": F(920, 1000), "GMI": F(528, 1000), "AQI": F(404, 1000), "SGI": F(892, 1000)}
    coef |= {"DEPI": F(115, 1000), "SGAI": F(-172, 1000), "TATA": F(4679, 1000), "LVGI": F(-327, 1000)}
    x = {"DSRI": F(145, 100), "GMI": F(128, 100), "AQI": F(135, 100), "SGI": F(132, 100)}
    x |= {"DEPI": F(82, 100), "SGAI": F(118, 100), "TATA": F(8, 100), "LVGI": F(112, 100)}
    quoted_terms = {"DSRI": 1.3340, "GMI": 0.6758, "AQI": 0.5454, "SGI": 1.1774}
    quoted_terms |= {"DEPI": 0.0943, "SGAI": -0.2030, "TATA": 0.3743, "LVGI": -0.3662}
    terms = {k: coef[k] * x[k] for k in x}
    for k, q in quoted_terms.items():
        approx(f"term {k}", terms[k], q, 4)
    m = coef["const"] + sum(terms.values())
    names = list(x)
    flt = -4.84 + float(np.dot([float(coef[k]) for k in names], [float(x[k]) for k in names]))
    assert abs(flt - float(m)) < 1e-12
    exact("M-score (exact)", m, F(-12079, 10000))
    approx("M-score", m, -1.2079, 4)
    approx("sum of the rounded terms", -4.84 + sum(quoted_terms.values()), -1.2080, 4)
    approx("M-score rounded", m, -1.21, 2)
    assert m > F(-178, 100)
    top = sorted(terms, key=lambda k: terms[k], reverse=True)[:3]
    exact("three largest weighted terms", top, ["DSRI", "SGI", "GMI"])


def drill5() -> None:
    print("Drill 5: absorption costing")
    price, var, fixed = F(100), F(40), F(30_000_000)
    produced, sold = [F(1_000_000), F(1_500_000)], [F(1_000_000), F(900_000)]
    unit = [var + fixed / p for p in produced]
    exact("fixed overhead per unit year 1", fixed / produced[0], F(30))
    exact("fixed overhead per unit year 2", fixed / produced[1], F(20))
    exact("unit cost year 1", unit[0], F(70))
    exact("unit cost year 2", unit[1], F(60))
    gp = []
    for i in range(2):
        revenue = sold[i] * price
        cogs = sold[i] * unit[i]
        # Route B: total production cost less the cost carried in ending inventory.
        ending_units = produced[i] - sold[i] + (produced[0] - sold[0] if i == 1 else 0)
        cogs_b = var * produced[i] + fixed - ending_units * unit[i]
        assert cogs == cogs_b
        gp.append(revenue - cogs)
        exact(f"revenue year {i + 1}", revenue, [F(100_000_000), F(90_000_000)][i])
        exact(f"COGS year {i + 1}", cogs, [F(70_000_000), F(54_000_000)][i])
        exact(f"gross profit year {i + 1}", gp[i], [F(30_000_000), F(36_000_000)][i])
        approx(f"gross margin year {i + 1} (percent)", 100 * gp[i] / revenue, [30.0, 40.0][i], 1)
    exact("ending inventory units", produced[1] - sold[1], F(600_000))
    approx("unit sales change (percent)", 100 * (sold[1] / sold[0] - 1), -10.0, 1)
    approx("gross profit change (percent)", 100 * (gp[1] / gp[0] - 1), 20.0, 1)
    deferred = (produced[1] - sold[1]) * fixed / produced[1]
    exact("fixed overhead deferred into inventory", deferred, F(12_000_000))
    # Route C: variable costing profit plus deferred overhead equals absorption profit.
    var_gp = sold[1] * (price - var) - fixed
    assert var_gp + deferred == gp[1]


def drill6() -> None:
    print("Drill 6: valuation allowance release")
    exact("gross DTA from losses at 25%", F(200) * F(25, 100), F(50))
    release = F(50) - F(20)
    exact("allowance release ($M)", release, F(30))
    pretax, current_tax, deferred_tax = F(15), F(0), -release
    ni = pretax - (current_tax + deferred_tax)
    exact("reported net income ($M)", ni, F(45))
    exact("net income / pre-tax income", ni / pretax, F(3))
    approx("effective tax rate (percent)", 100 * (current_tax + deferred_tax) / pretax, -200.0, 1)
    approx("release share of net income (percent)", 100 * release / ni, 66.7, 1)


def main() -> None:
    drill1()
    drill2()
    drill3()
    drill4()
    drill5()
    drill6()
    print("all statement forensics numbers verified")


if __name__ == "__main__":
    main()
