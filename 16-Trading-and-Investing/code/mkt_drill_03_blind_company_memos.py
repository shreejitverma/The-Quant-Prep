"""Blind Company Memos: every derived number in the six cases, from the companies' own SEC filings.

Backs every number in `16-Trading-and-Investing/30-Drills/Blind-Company-Memos.md`.
The inputs are cited constants copied from each company's Form 10-K or 10-Q (named next to each block);
the script never downloads anything.
Independent routes used here:
- every ratio, margin, growth rate and valuation multiple is recomputed in exact `fractions.Fraction` arithmetic
  from the filed line items and asserted against the literal the note quotes;
- filed subtotals are re-added from their components where the filing shows them (Amazon 2001 operating cash
  flow from the 17 reconciliation lines, Apple and Costco gross margin from sales less cost of sales,
  Hertz total debt from vehicle plus non-vehicle debt), so a mistyped input fails loudly;
- interim cash flows are recovered by subtraction (Enron Q2-Q4 2000 = full year less Q1).
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_drill_03_blind_company_memos.py`.
"""

from __future__ import annotations

from fractions import Fraction as F


def approx(label: str, value, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(float(value) - expected) <= tol, f"{label}: computed {float(value)!r}, quoted {expected}"
    print(f"    {label} = {float(value):.{decimals}f}")


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def pct(a, b) -> F:
    return 100 * F(a) / F(b)


def case1_enron() -> None:
    # Enron Corp. Form 10-K for 2000 (filed April 2, 2001): Item 6, income statement, cash flow statement,
    # Item 5 price table, Note 16; Form 10-Q for the quarter ended March 31, 2001.
    print("Case 1: Enron (FY1998-FY2000, Q1 2001)")
    rev = {1998: F(31260), 1999: F(40112), 2000: F(100789)}
    ni = {1998: F(703), 1999: F(893), 2000: F(979)}
    cfo = {1998: F(1640), 1999: F(1228), 2000: F(4779)}
    approx("revenue growth 2000 (percent)", pct(rev[2000] - rev[1999], rev[1999]), 151.3, 1)
    approx("total assets growth 2000 (percent)", pct(F(65503) - F(33381), F(33381)), 96.2, 1)
    for y, q in [(1998, 2.33), (1999, 1.38), (2000, 4.88)]:
        approx(f"CFO / net income {y}", cfo[y] / ni[y], q, 2)
    q1_2001_cfo, q1_2001_ni, q1_2000_cfo, q1_2000_ni = F(-464), F(425), F(-457), F(338)
    approx("CFO / net income Q1 2001", q1_2001_cfo / q1_2001_ni, -1.09, 2)
    approx("CFO / net income Q1 2000", q1_2000_cfo / q1_2000_ni, -1.35, 2)
    exact("implied CFO Q2-Q4 2000", cfo[2000] - q1_2000_cfo, F(5236))
    eps_diluted, high_2000 = F(112, 100), F(9075, 100)
    approx("P/E at the 2000 high on diluted EPS", high_2000 / eps_diluted, 81.0, 1)
    bvps = F(11470) / F(752)
    approx("book value per share 2000", bvps, 15.25, 2)
    approx("price / book at the 2000 high", high_2000 / bvps, 5.95, 2)


def case2_amazon() -> None:
    # Amazon.com, Inc. Form 10-K for 2001 (filed January 24, 2002): Item 6, Item 7, balance sheet, cash flow
    # statement, Item 5 price table, cover page share count; Form 10-K for 2002 for the 2002 cash flow.
    print("Case 2: Amazon (FY1999-FY2001)")
    sales = {1999: F(1639839), 2000: F(2761983), 2001: F(3122433)}
    gross = {1999: F(290645), 2000: F(655777), 2001: F(798558)}
    cogs_2001 = F(2323875)
    assert sales[2001] - cogs_2001 == gross[2001]
    for y, q in [(1999, 17.7), (2000, 23.7), (2001, 25.6)]:
        approx(f"gross margin {y} (percent)", pct(gross[y], sales[y]), q, 1)
    cash = {1999: F(133309) + F(572879), 2000: F(822435) + F(278087), 2001: F(540282) + F(456303)}
    for y, q in [(1999, 706), (2000, 1101), (2001, 997)]:
        approx(f"cash and marketable securities {y} ($M)", cash[y] / 1000, q, 0)
    # 2001 operating cash flow from its 17 reconciliation lines (thousands).
    net_loss = F(-567277)
    adjustments = [84709, 4637, 30327, 181033, 73293, -1335, 2141, 26629, 10523]
    working_capital = [30628, 20732, -44438, 50031, 114738, -135808, -345]
    approx("2001 non-cash adjustments ($M)", F(sum(adjustments)) / 1000, 412, 0)
    approx("2001 working-capital changes ($M)", F(sum(working_capital)) / 1000, 36, 0)
    cfo_2001 = net_loss + sum(adjustments) + sum(working_capital)
    exact("2001 operating cash flow (thousands)", cfo_2001, F(-119782))
    capex_2001 = F(50)
    fcf = cfo_2001 / 1000 - capex_2001
    approx("2001 free cash flow ($M)", fcf, -170, 0)
    approx("runway in years at the 2001 burn", cash[2001] / 1000 / -fcf, 5.9, 1)
    inv = (F(143722) + F(174563)) / 2
    ap = (F(444748) + F(485383)) / 2
    dio = inv / cogs_2001 * 365
    dpo = ap / cogs_2001 * 365
    approx("days inventory outstanding 2001", dio, 25.0, 1)
    approx("days payable outstanding 2001", dpo, 73.0, 1)
    approx("inventory days less payable days", dio - dpo, -48.0, 1)
    shares, price = F(373291188), F(8)
    approx("shares outstanding January 10, 2002 (millions)", shares / 1_000_000, 373.3, 1)
    mcap = shares * price / 1_000_000
    approx("market cap at $8.00 ($M)", mcap, 2986, 0)
    ev = mcap + F(2156133) / 1000 - cash[2001] / 1000
    approx("enterprise value at $8.00 ($M)", ev, 4146, 0)
    approx("EV / 2001 sales at $8.00", ev / (sales[2001] / 1000), 1.33, 2)
    approx("price fall from 2000 Q1 high to 2001 Q3 low (percent)", pct(F(9150) - F(597), F(9150)), 93.5, 1)


def case3_valeant() -> None:
    # Valeant Pharmaceuticals International, Inc. Form 10-K for 2015 (filed April 29, 2016; 2014 restated):
    # Item 6, balance sheet, income statement, Item 5 price table; Bausch Health 10-K for 2017 price table.
    print("Case 3: Valeant (FY2013-FY2015)")
    rev = {2013: F(57696, 10), 2014: F(82060, 10), 2015: F(104465, 10)}
    rd = {2013: F(1568, 10), 2014: F(2460, 10), 2015: F(3344, 10)}
    for y, q in [(2013, 2.72), (2014, 3.00), (2015, 3.20)]:
        approx(f"R&D / revenue {y} (percent)", pct(rd[y], rev[y]), q, 2)
    gw_int_2015 = F(230830, 10) + F(185528, 10)
    gw_int_2014 = F(112779, 10) + F(93614, 10)
    approx("goodwill plus intangibles 2015 ($M)", gw_int_2015, 41635.8, 1)
    approx("goodwill plus intangibles 2014 ($M)", gw_int_2014, 20639.3, 1)
    assets_2015, equity_2015, debt_2015 = F(489645, 10), F(59110, 10), F(310884, 10)
    approx("goodwill and intangibles / total assets 2015 (percent)", pct(gw_int_2015, assets_2015), 85.0, 1)
    approx("tangible equity 2015 ($M)", equity_2015 - gw_int_2015, -35724.8, 1)
    approx("debt / equity 2015", debt_2015 / equity_2015, 5.26, 2)
    approx("long-term debt 2015 ($B)", debt_2015 / 1000, 31.1, 1)
    approx("tangible equity 2015 ($B)", (equity_2015 - gw_int_2015) / 1000, -35.7, 1)
    approx("debt growth 2014 to 2015 (percent)", pct(debt_2015 - F(152289, 10), F(152289, 10)), 104.1, 1)
    high, low = F(26381, 100), F(831, 100)
    approx("market value at the 2015 high on 342.9M shares ($B)", high * F(3429, 10) / 1000, 90.5, 1)
    approx("fall from 2015 Q3 high to 2017 Q2 low (percent)", pct(high - low, high), 96.9, 1)


def case4_costco() -> None:
    # Costco Wholesale Corporation Form 10-K for fiscal 2010 (filed October 18, 2010): Item 6, Item 7,
    # balance sheet, cash flow statement, Item 1 membership fees, Item 5 price table.
    print("Case 4: Costco (FY2008-FY2010)")
    sales = {2008: F(70977), 2009: F(69889), 2010: F(76255)}
    merch = {2008: F(63503), 2009: F(62335), 2010: F(67995)}
    for y, q in [(2008, 10.53), (2009, 10.81), (2010, 10.83)]:
        approx(f"merchandise gross margin {y} (percent)", pct(sales[y] - merch[y], sales[y]), q, 2)
    fees, op = F(1691), F(2077)
    approx("membership fees / operating income 2010 (percent)", pct(fees, op), 81.4, 1)
    exact("operating income excluding membership fees 2010 ($M)", op - fees, F(386))
    approx("that as a share of net sales 2010 (percent)", pct(op - fees, sales[2010]), 0.51, 2)
    inv = (F(5638) + F(5405)) / 2
    ap = (F(5947) + F(5450)) / 2
    approx("inventory turnover 2010", merch[2010] / inv, 12.3, 1)
    approx("days inventory 2010", inv / merch[2010] * 365, 29.6, 1)
    approx("days payable 2010", ap / merch[2010] * 365, 30.6, 1)
    approx("accounts payable / inventory at FY2010 end (percent)", pct(F(5947), F(5638)), 105.5, 1)
    debt = {2008: F(134) + 6 + 2206, 2009: F(16) + 80 + 2130, 2010: F(26) + 0 + 2141}
    exact("total debt 2008", debt[2008], F(2346))
    exact("total debt 2009", debt[2009], F(2226))
    exact("total debt 2010", debt[2010], F(2167))
    cash = {2009: F(3157) + 570, 2010: F(3214) + 1535}
    exact("cash and short-term investments 2009", cash[2009], F(3727))
    exact("cash and short-term investments 2010", cash[2010], F(4749))
    eps = F(292, 100)
    approx("P/E at the FY2010 Q4 closing low", F(5361, 100) / eps, 18.4, 1)
    approx("P/E at the FY2010 Q4 closing high", F(5916, 100) / eps, 20.3, 1)


def case5_hertz() -> None:
    # Hertz Global Holdings, Inc. Form 10-K for 2019 (Item 6, cash flow statement), Form 10-Q for Q1 2020
    # (balance sheet, income statement, cash flow statement, liquidity note), Form 10-K for 2020 (ATM program).
    print("Case 5: Hertz (FY2018, FY2019, Q1 2020)")
    vehicle, non_vehicle = F(14438), F(4316)
    exact("total debt March 31, 2020 ($M)", vehicle + non_vehicle, F(18754))
    approx("total debt March 31, 2020 ($B)", (vehicle + non_vehicle) / 1000, 18.8, 1)
    assets, liabilities = F(25842), F(24351)
    exact("total equity March 31, 2020 ($M)", assets - liabilities, F(1491))
    approx("debt / total assets March 31, 2020 (percent)", pct(vehicle + non_vehicle, assets), 72.6, 1)
    approx("vehicle debt share of total debt (percent)", pct(vehicle, vehicle + non_vehicle), 77.0, 1)
    approx("debt / equity March 31, 2020", (vehicle + non_vehicle) / (assets - liabilities), 12.6, 1)
    approx("Q1 2020 revenue change vs Q1 2019 (percent)", pct(F(1923) - F(2107), F(2107)), -8.7, 1)
    exact("peak 2019 fleet, US plus international", 567600 + 204000, 771600)
    approx("ATM net proceeds per share ($)", F(28_000_000) / F(13912368), 2.01, 2)


def case6_apple() -> None:
    # Apple Computer, Inc. Form 10-K for fiscal 2003 (filed December 19, 2003): Item 6, income statement,
    # cash flow statement, net sales and unit table, Item 5 price table, cover page share count.
    print("Case 6: Apple (FY2001-FY2003)")
    sales = {2001: F(5363), 2002: F(5742), 2003: F(6207)}
    cogs = {2001: F(4128), 2002: F(4139), 2003: F(4499)}
    filed_gross = {2001: F(1235), 2002: F(1603), 2003: F(1708)}
    for y, q in [(2001, 23.0), (2002, 27.9), (2003, 27.5)]:
        assert sales[y] - cogs[y] == filed_gross[y]
        approx(f"gross margin {y} (percent)", pct(filed_gross[y], sales[y]), q, 1)
    approx("iPod unit growth FY2003 (percent)", pct(F(939) - F(381), F(381)), 146.5, 1)
    shares, price = F(367734960), F(20)
    approx("shares outstanding December 5, 2003 (millions)", shares / 1_000_000, 367.7, 1)
    mcap = shares * price / 1_000_000
    approx("market cap at $20.00 ($M)", mcap, 7355, 0)
    cash, debt = F(4566), F(304)
    approx("cash / market cap at $20.00 (percent)", pct(cash, mcap), 62.1, 1)
    approx("net cash / market cap at $20.00 (percent)", pct(cash - debt, mcap), 57.9, 1)
    ev = mcap + debt - cash
    approx("enterprise value at $20.00 ($M)", ev, 3093, 0)
    approx("EV / FY2003 sales at $20.00", ev / sales[2003], 0.50, 2)
    approx("net cash per share ($)", (cash - debt) * 1_000_000 / shares, 11.59, 2)


def main() -> None:
    case1_enron()
    case2_amazon()
    case3_valeant()
    case4_costco()
    case5_hertz()
    case6_apple()
    print("all blind company memo numbers verified")


if __name__ == "__main__":
    main()
