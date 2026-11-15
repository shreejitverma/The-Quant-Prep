"""Beneish M-score and Piotroski F-score: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/Investing/Fundamental-Analysis/06-Fraud-Detection-Beneish-M-Score-and-Piotroski-F-Score.md`.
Independent routes used here:
- the eight Beneish indices in exact fractions from the raw statement lines, and the M-score both as an
  exact sum and as the sum of the rounded per-term products the note shows (which must agree at the
  quoted three decimals);
- the probit probabilities Phi(M) by the error function and again by trapezoidal integration of the
  standard normal density, for the example and for the -1.78 and -2.22 cut-offs;
- the Piotroski signals from the raw lines, scored by a rule table that is independent of the arithmetic
  that produced each ratio.
The Beneish (1999) coefficients, the Piotroski (2000) results and the Altman (1968) cut-offs are cited
constants from the papers.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_fa_06_beneish_piotroski.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction as F

import numpy as np

COEF = {
    "const": F("-4.84"),
    "DSRI": F("0.920"),
    "GMI": F("0.528"),
    "AQI": F("0.404"),
    "SGI": F("0.892"),
    "DEPI": F("0.115"),
    "SGAI": F("-0.172"),
    "TATA": F("4.679"),
    "LVGI": F("-0.327"),
}  # Beneish (1999), the eight-variable model

Y1 = {
    "sales": F(800),
    "cogs": F(520),
    "sga": F(120),
    "ni": F(90),
    "cfo": F(110),
    "ar": F(80),
    "ca": F(220),
    "ppe": F(300),
    "ta": F(600),
    "cl": F(100),
    "ltd": F(150),
    "shares": F(50),
    "dep": F(30),
}
Y2 = {
    "sales": F(1040),
    "cogs": F(702),
    "sga": F("176.8"),
    "ni": F(85),
    "cfo": F(40),
    "ar": F(160),
    "ca": F(330),
    "ppe": F(350),
    "ta": F(780),
    "cl": F(160),
    "ltd": F(220),
    "shares": F(52),
    "dep": F(25),
}


def rounded(label: str, value, expected: str, scale: float = 1.0) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{float(value) * scale:.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"    {label} = {shown}")


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    items = value if isinstance(value, tuple) else (value,)
    shown = ", ".join(f"{float(v):g}" if isinstance(v, F) and v.denominator != 1 else str(v) for v in items)
    print(f"    {label} = {shown}")


def phi_erf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def phi_quad(x: float) -> float:
    grid = np.linspace(-12.0, x, 400_001)
    pdf = np.exp(-0.5 * grid**2) / math.sqrt(2 * math.pi)
    return float(np.sum((pdf[1:] + pdf[:-1]) * np.diff(grid)) / 2)


def phi(label: str, x: float, expected: str) -> None:
    a, b = phi_erf(x), phi_quad(x)
    assert abs(a - b) < 1e-9, (a, b)
    rounded(label, a, expected, 100)


def beneish() -> None:
    print("Part 1: Beneish M-score for Apex Logistics")
    t, p = Y2, Y1
    idx = {
        "DSRI": (t["ar"] / t["sales"]) / (p["ar"] / p["sales"]),
        "GMI": ((p["sales"] - p["cogs"]) / p["sales"]) / ((t["sales"] - t["cogs"]) / t["sales"]),
        "AQI": (1 - (t["ca"] + t["ppe"]) / t["ta"]) / (1 - (p["ca"] + p["ppe"]) / p["ta"]),
        "SGI": t["sales"] / p["sales"],
        "DEPI": (p["dep"] / (p["dep"] + p["ppe"])) / (t["dep"] / (t["dep"] + t["ppe"])),
        "SGAI": (t["sga"] / t["sales"]) / (p["sga"] / p["sales"]),
        "LVGI": ((t["cl"] + t["ltd"]) / t["ta"]) / ((p["cl"] + p["ltd"]) / p["ta"]),
        "TATA": (t["ni"] - t["cfo"]) / t["ta"],
    }
    rounded("receivables / sales, t", t["ar"] / t["sales"], "0.1538")
    rounded("receivables / sales, t-1", p["ar"] / p["sales"], "0.1000")
    rounded("(CA + PPE) / TA, t", (t["ca"] + t["ppe"]) / t["ta"], "0.8718")
    rounded("(CA + PPE) / TA, t-1", (p["ca"] + p["ppe"]) / p["ta"], "0.8667")
    rounded("SG&A / sales, t-1", p["sga"] / p["sales"], "0.1500")
    rounded("gross margin t-1", (p["sales"] - p["cogs"]) / p["sales"], "0.3500")
    rounded("gross margin t", (t["sales"] - t["cogs"]) / t["sales"], "0.3250")
    rounded("1 - (CA + PPE)/TA, t", 1 - (t["ca"] + t["ppe"]) / t["ta"], "0.12821")
    rounded("1 - (CA + PPE)/TA, t-1", 1 - (p["ca"] + p["ppe"]) / p["ta"], "0.13333")
    rounded("depreciation rate t-1", p["dep"] / (p["dep"] + p["ppe"]), "0.09091")
    rounded("depreciation rate t", t["dep"] / (t["dep"] + t["ppe"]), "0.06667")
    rounded("1 - (CA + PPE)/TA, t (four decimals)", 1 - (t["ca"] + t["ppe"]) / t["ta"], "0.1282")
    rounded("1 - (CA + PPE)/TA, t-1 (four decimals)", 1 - (p["ca"] + p["ppe"]) / p["ta"], "0.1333")
    rounded("depreciation rate t-1 (four decimals)", p["dep"] / (p["dep"] + p["ppe"]), "0.0909")
    rounded("depreciation rate t (four decimals)", t["dep"] / (t["dep"] + t["ppe"]), "0.0667")
    exact("depreciation plus net PP&E, t-1 and t", (p["dep"] + p["ppe"], t["dep"] + t["ppe"]), (330, 375))
    rounded("SG&A / sales, t", t["sga"] / t["sales"], "0.1700")
    rounded("leverage t", (t["cl"] + t["ltd"]) / t["ta"], "0.4872")
    rounded("leverage t-1", (p["cl"] + p["ltd"]) / p["ta"], "0.4167")
    quoted = {
        "DSRI": "1.5385",
        "GMI": "1.0769",
        "AQI": "0.9615",
        "SGI": "1.3000",
        "DEPI": "1.3636",
        "SGAI": "1.1333",
        "LVGI": "1.1692",
        "TATA": "0.0577",
    }
    for name, q in quoted.items():
        rounded(name, idx[name], q)
    rounded("DSRI (two decimals)", idx["DSRI"], "1.54")
    rounded("DEPI (two decimals)", idx["DEPI"], "1.36")
    rounded("SGI (two decimals)", idx["SGI"], "1.30")
    m_exact = COEF["const"] + sum(COEF[k] * v for k, v in idx.items())
    terms = {
        "DSRI": "1.4154",
        "GMI": "0.5686",
        "AQI": "0.3885",
        "SGI": "1.1596",
        "DEPI": "0.1568",
        "SGAI": "-0.1949",
        "TATA": "0.2699",
        "LVGI": "-0.3823",
    }
    for name, q in terms.items():
        rounded(f"term {name}", COEF[name] * idx[name], q)
    m_from_terms = float(COEF["const"]) + sum(float(q) for q in terms.values())
    rounded("M (exact)", m_exact, "-1.458")
    rounded("M (sum of rounded terms)", m_from_terms, "-1.458")
    phi("Phi(M) for the example (percent)", float(m_exact), "7.24")
    phi("Phi(-1.78) (percent)", -1.78, "3.75")
    phi("Phi(-2.22) (percent)", -2.22, "1.32")
    ratio = phi_erf(float(m_exact)) / phi_erf(-1.78)
    assert 1.8 < ratio < 2.2, "note says about twice the cut-off probability"
    print(f"    Phi(M) / Phi(-1.78) = {ratio:.2f} (about twice)")


def piotroski() -> None:
    print("Part 2: Piotroski F-score (year-end assets, as in the note)")
    t, p = Y2, Y1
    roa_t, roa_p = t["ni"] / t["ta"], p["ni"] / p["ta"]
    cfo_t = t["cfo"] / t["ta"]
    lev_t, lev_p = t["ltd"] / t["ta"], p["ltd"] / p["ta"]
    cr_t, cr_p = t["ca"] / t["cl"], p["ca"] / p["cl"]
    gm_t, gm_p = 1 - t["cogs"] / t["sales"], 1 - p["cogs"] / p["sales"]
    at_t, at_p = t["sales"] / t["ta"], p["sales"] / p["ta"]
    rounded("ROA t (percent)", roa_t, "10.9", 100)
    rounded("ROA t-1 (percent)", roa_p, "15.0", 100)
    rounded("CFO / assets t (percent)", cfo_t, "5.1", 100)
    rounded("LTD / assets t (percent)", lev_t, "28.2", 100)
    rounded("LTD / assets t-1 (percent)", lev_p, "25.0", 100)
    rounded("current ratio t", cr_t, "2.06")
    rounded("current ratio t-1", cr_p, "2.20")
    rounded("asset turnover t", at_t, "1.333")
    rounded("asset turnover t-1", at_p, "1.333")
    rules = [
        ("F_ROA", t["ni"] > 0),
        ("F_CFO", t["cfo"] > 0),
        ("F_DROA", roa_t > roa_p),
        ("F_ACCRUAL", cfo_t > roa_t),
        ("F_DLEVER", lev_t < lev_p),
        ("F_DLIQUID", cr_t > cr_p),
        ("F_EQ_OFFER", t["shares"] <= p["shares"]),  # proxy: no new shares issued
        ("F_DMARGIN", gm_t > gm_p),
        ("F_DTURN", at_t > at_p),
    ]
    expected = [1, 1, 0, 0, 0, 0, 0, 0, 0]
    for (name, ok), e in zip(rules, expected, strict=True):
        exact(name, int(ok), e)
    exact("F-score", sum(int(ok) for _, ok in rules), 2)
    exact("share count change (percent)", (t["shares"] / p["shares"] - 1) * 100, 4)
    exact("sales growth (percent)", (t["sales"] / p["sales"] - 1) * 100, 30)
    exact("receivables growth (percent)", (t["ar"] / p["ar"] - 1) * 100, 100)
    exact("gross profit t-1, t", (p["sales"] - p["cogs"], t["sales"] - t["cogs"]), (280, 338))
    exact("EBIT t-1, t", (p["sales"] - p["cogs"] - p["sga"], t["sales"] - t["cogs"] - t["sga"]), (160, F("161.2")))
    rounded("SG&A / sales t-1 (percent)", p["sga"] / p["sales"], "15.0", 100)
    rounded("SG&A / sales t (percent)", t["sga"] / t["sales"], "17.0", 100)


if __name__ == "__main__":
    beneish()
    piotroski()
    print("all Beneish and Piotroski numbers check out")
