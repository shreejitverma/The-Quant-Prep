"""Three-statement linkages: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/Investing/Fundamental-Analysis/01-Three-Statement-Linkages-and-Cash-Flow-Dynamics.md`.
Independent routes used here:
- the $100 depreciation shock by running a full before-and-after income statement and a direct-method
  cash flow (cash receipts minus cash costs minus cash taxes), checked against the closed forms
  -(1 - t) D for net income and t D for cash, and by posting double-entry journal lines to a ledger
  whose debits must equal its credits;
- the software company's operating cash flow by the direct method (cash collected from customers
  minus cash operating costs minus cash interest and taxes), checked against the indirect-method 200;
- the FCFF-FCFE bridge FCFE = FCFF - interest (1 - t) + net borrowing, by building both from a
  hypothetical income statement and cash flow statement;
- the card transactions (machine purchase, equity issue, dividend, goodwill write-down) by double-entry
  postings that must keep assets equal to liabilities plus equity.
Every quoted number is printed as ``label = value`` and asserted in exact fractions.
Run it with `python 16-Trading-and-Investing/code/mkt_fa_01_three_statements.py`.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    items = value if isinstance(value, tuple) else (value,)
    shown = ", ".join(f"{float(v):g}" if isinstance(v, F) and v.denominator != 1 else str(v) for v in items)
    print(f"    {label} = {shown}")


def pct(label: str, value: F, expected: str) -> None:
    """Assert a percentage at the decimals the note quotes."""
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{float(100 * value):.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}%, quoted {expected}%"
    print(f"    {label} = {shown}%")


class Ledger:
    """Minimal double-entry ledger: debits are positive, credits negative, and every entry nets to zero."""

    ASSETS = {"cash", "ppe", "goodwill", "inventory"}

    def __init__(self) -> None:
        self.bal: dict[str, F] = defaultdict(F)

    def post(self, *lines: tuple[str, F]) -> None:
        assert sum(amount for _, amount in lines) == 0, "unbalanced journal entry"
        for account, amount in lines:
            self.bal[account] += amount

    def assets(self) -> F:
        return sum((v for k, v in self.bal.items() if k in self.ASSETS), F(0))

    def liabilities_and_equity(self) -> F:
        return -sum((v for k, v in self.bal.items() if k not in self.ASSETS), F(0))


def income_and_cash(depreciation: F, t: F) -> tuple[F, F]:
    """Hypothetical firm: $1,000 cash revenue, $600 cash costs, book depreciation equals tax depreciation."""
    revenue, cash_costs = F(1000), F(600)
    pretax = revenue - cash_costs - depreciation
    tax = t * pretax
    net_income = pretax - tax
    cash_flow = revenue - cash_costs - tax  # direct method: receipts minus cash costs minus cash taxes
    return net_income, cash_flow


def depreciation_shock() -> None:
    print("Example 1: a $100 rise in depreciation at a 25% tax rate")
    t, d = F(25, 100), F(100)
    ni0, cf0 = income_and_cash(F(200), t)
    ni1, cf1 = income_and_cash(F(200) + d, t)
    exact("tax expense change", -t * d, -25)
    exact("net income change (full statements)", ni1 - ni0, -75)
    exact("net income change (closed form -(1-t)D)", -(1 - t) * d, -75)
    exact("operating cash change (direct method)", cf1 - cf0, 25)
    exact("operating cash change (closed form tD)", t * d, 25)
    # Ledger: book the extra depreciation and the lower tax bill (paid in cash).
    led = Ledger()
    led.post(("dep_expense", d), ("ppe", -d))
    led.post(("cash", t * d), ("tax_expense", -t * d))
    exact("cash", led.bal["cash"], 25)
    exact("net PP&E", led.bal["ppe"], -100)
    exact("total assets", led.assets(), -75)
    retained = -(led.bal["dep_expense"] + led.bal["tax_expense"])
    exact("retained earnings (equity)", retained, -75)
    exact("assets minus (liabilities + equity)", led.assets() - led.liabilities_and_equity(), 0)


def software_company() -> None:
    print("Example 2: headline versus economic free cash flow ($M)")
    revenue, ebit, ni, da, sbc = F(1000), F(50), F(40), F(30), F(120)
    d_ar, d_defrev, capex = F(40), F(50), F(25)
    cfo_indirect = ni + da + sbc - d_ar + d_defrev
    exact("CFO (indirect)", cfo_indirect, 200)
    # Direct method: cash collected, cash operating costs, cash interest and taxes.
    collected = revenue - d_ar + d_defrev
    cash_opex = revenue - ebit - da - sbc  # opex paid in cash; D&A and SBC are the non-cash charges
    cash_interest_and_tax = ebit - ni
    cfo_direct = collected - cash_opex - cash_interest_and_tax
    exact("cash collected from customers", collected, 1010)
    exact("cash operating costs", cash_opex, 800)
    exact("cash interest and taxes", cash_interest_and_tax, 10)
    exact("CFO (direct)", cfo_direct, 200)
    headline = cfo_direct - capex
    exact("headline FCF", headline, 175)
    pct("headline FCF margin", headline / revenue, "17.5")
    economic = headline - sbc
    exact("economic FCF", economic, 55)
    pct("economic FCF margin", economic / revenue, "5.5")
    share = sbc / headline
    pct("SBC share of headline FCF", share, "68.57")
    assert share > F(68, 100), "note says more than 68%"


def fcff_fcfe_bridge() -> None:
    print("FCFF to FCFE bridge (hypothetical firm, $M)")
    ebit, interest, t, da, capex, d_nwc = F(300), F(40), F(25, 100), F(80), F(120), F(20)
    for net_borrowing in (F(0), F(30), F(50)):
        ni = (ebit - interest) * (1 - t)
        cfo = ni + da - d_nwc  # US GAAP: interest paid sits in CFO
        fcfe = cfo - capex + net_borrowing
        fcff = ebit * (1 - t) + da - capex - d_nwc
        exact(f"FCFF via CFO, net borrowing {net_borrowing}", cfo + interest * (1 - t) - capex, fcff)
        exact(f"FCFE - FCFF, net borrowing {net_borrowing}", fcfe - fcff, net_borrowing - interest * (1 - t))
        # FCFE exceeds FCFF only when net borrowing exceeds after-tax interest (30 here).
        assert (fcfe > fcff) == (net_borrowing > interest * (1 - t))


def card_transactions() -> None:
    print("Cards: double-entry checks")
    led = Ledger()
    led.post(("ppe", F(100)), ("cash", F(-100)))  # CFI -100
    led.post(("cash", F(50)), ("debt", F(-50)))  # CFF +50
    exact("machine: net cash change", led.bal["cash"], -50)
    exact("machine: PP&E", led.bal["ppe"], 100)
    exact("machine: balance check", led.assets() - led.liabilities_and_equity(), 0)
    led = Ledger()
    led.post(("cash", F(100)), ("common_stock_apic", F(-100)))
    exact("equity issue: cash", led.bal["cash"], 100)
    led = Ledger()
    led.post(("retained_earnings", F(10)), ("cash", F(-10)))
    exact("dividend: cash", led.bal["cash"], -10)
    exact("dividend: equity", -led.bal["retained_earnings"], -10)
    led = Ledger()
    led.post(("impairment_expense", F(50)), ("goodwill", F(-50)))
    exact("goodwill write-down: cash", led.bal["cash"], 0)
    exact("goodwill write-down: total assets", led.assets(), -50)


if __name__ == "__main__":
    depreciation_shock()
    software_company()
    fcff_fcfe_bridge()
    card_transactions()
    print("all three-statement numbers check out")
