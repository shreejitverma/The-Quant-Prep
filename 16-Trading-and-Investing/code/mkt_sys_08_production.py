"""Production architecture and decision ledger: every number in the note, by an independent route.

Backs every number in `16-Trading-and-Investing/60-Systems/08-Production-Architecture-and-Decision-Ledger.md`.
Independent routes used here:
- the price collar in exact decimal arithmetic, and the approve/reject decisions by evaluating the rule;
- Brinson-Fachler effects in exact fractions, checked against the active return computed directly from the
  portfolio and benchmark totals, and against the Brinson-Hood-Beebower allocation total;
- the ledger hash by SHA-256 over the canonical JSON of the stated parameters, and the empty-input hash.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 16-Trading-and-Investing/code/mkt_sys_08_production.py`.
"""

from __future__ import annotations

import hashlib
import json
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def collar() -> None:
    print("Example 1: pre-trade price collar (cards mkt-sys-227, mkt-sys-251)")
    bid, ask = Decimal("49.98"), Decimal("50.00")
    mid = (bid + ask) / 2
    exact("midpoint", mid, Decimal("49.99"))
    lower = mid * Decimal("0.97")
    upper = mid * Decimal("1.03")
    exact("lower collar exact", lower, Decimal("48.4903"))
    exact("upper collar exact", upper, Decimal("51.4897"))
    cent = Decimal("0.01")
    exact("lower collar (cents)", lower.quantize(cent, ROUND_HALF_UP), Decimal("48.49"))
    exact("upper collar (cents)", upper.quantize(cent, ROUND_HALF_UP), Decimal("51.49"))
    exact("scenario A, $50.25 approved", lower <= Decimal("50.25") <= upper, True)
    exact("scenario B, $55.00 approved", lower <= Decimal("55.00") <= upper, False)


def brinson() -> None:
    print("Example 2: Brinson-Fachler attribution (cards mkt-sys-234, mkt-sys-235)")
    f = Fraction
    wb = {"T": f(1, 2), "H": f(1, 2)}
    wp = {"T": f(7, 10), "H": f(3, 10)}
    rb = {"T": f(10, 100), "H": f(2, 100)}
    rp = {"T": f(12, 100), "H": f(1, 100)}
    r_b = sum(wb[s] * rb[s] for s in wb)
    r_p = sum(wp[s] * rp[s] for s in wp)
    exact("benchmark return (percent)", 100 * r_b, 6)
    exact("portfolio return (percent)", 100 * r_p, f(87, 10))
    exact("active return (percent)", 100 * (r_p - r_b), f(27, 10))
    alloc = {s: (wp[s] - wb[s]) * (rb[s] - r_b) for s in wb}
    sel = {s: wb[s] * (rp[s] - rb[s]) for s in wb}
    inter = {s: (wp[s] - wb[s]) * (rp[s] - rb[s]) for s in wb}
    exact("A_T, A_H (percent)", (100 * alloc["T"], 100 * alloc["H"]), (f(8, 10), f(8, 10)))
    exact("S_T, S_H (percent)", (100 * sel["T"], 100 * sel["H"]), (1, f(-1, 2)))
    exact("I_T, I_H (percent)", (100 * inter["T"], 100 * inter["H"]), (f(4, 10), f(2, 10)))
    totals = (100 * sum(alloc.values()), 100 * sum(sel.values()), 100 * sum(inter.values()))
    exact("allocation, selection, interaction totals (percent)", totals, (f(16, 10), f(1, 2), f(6, 10)))
    exact("effects sum to the active return", sum(totals), 100 * (r_p - r_b))
    bhb = {s: (wp[s] - wb[s]) * rb[s] for s in wb}
    exact("BHB allocation by sector (percent)", (100 * bhb["T"], 100 * bhb["H"]), (2, f(-4, 10)))
    exact("BHB and BF allocation totals agree", sum(bhb.values()), sum(alloc.values()))


def ledger_hash() -> None:
    print("Decision ledger hash (cards mkt-sys-243, mkt-sys-267)")
    params = {"vol_target": 0.10, "max_single_weight": 0.03, "turnover_penalty": 0.0005}
    canonical = json.dumps(params, sort_keys=True, separators=(",", ":"))
    exact("canonical parameters", canonical, '{"max_single_weight":0.03,"turnover_penalty":0.0005,"vol_target":0.1}')
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    exact("parameters_hash", digest, "0856a9e158520eafc41bf4bd9de82a8ac9a9789f73a29e5cd7ec42baad482289")
    exact("SHA-256 of zero bytes", hashlib.sha256(b"").hexdigest(), "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")


if __name__ == "__main__":
    collar()
    brinson()
    ledger_hash()
    print("all production-architecture numbers check out")
