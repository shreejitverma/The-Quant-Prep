"""NSE and BSE microstructure: every number in 02-Indian-Markets/01-NSE-BSE-Microstructure-and-Derivatives-Architecture.md.

Rates, lot sizes and timings are cited constants (circulars named in the note, as of November 2026); this script checks
the arithmetic built on them.
Independent routes used here:
- the closing VWAP is computed from the cluster values and volumes;
- per-crore charges are converted to percentages and the cost of selling one option lot is built charge by charge;
- the minimum-contract-size check compares lot x index level with SEBI's Rs 15 lakh floor;
- the max-pain strike is found by brute force over every listed strike and checked against a direct payout table.
Run: uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_india_01_nse.py
"""

from __future__ import annotations

import numpy as np
from mkt_assets_lib import close, q

NIFTY_LOT = 65  # NSE/FAOP/70616, October 3, 2025, from the January 2026 expiries


def closing_vwap() -> None:
    print("Example 1: a stock's 30-minute closing VWAP (hypothetical trades) and an index option payoff")
    prices = [2451.0, 2449.5, 2452.0]
    vols = [1_000_000, 1_500_000, 2_500_000]
    vwap = sum(p * v for p, v in zip(prices, vols, strict=True)) / sum(vols)
    q("cluster 1 value (Rs lakh)", prices[0] * vols[0] / 1e5, "24,510")
    q("cluster 2 value (Rs lakh)", prices[1] * vols[1] / 1e5, "36,742.5")
    q("cluster 3 value (Rs lakh)", prices[2] * vols[2] / 1e5, "61,300")
    q("total value (Rs lakh)", sum(p * v for p, v in zip(prices, vols, strict=True)) / 1e5, "122,552.5")
    q("total volume (lakh shares)", sum(vols) / 1e5, "50")
    q("closing VWAP", vwap, "2,451.05")
    settle, strike = 24_510.50, 24_500.0
    q("24,500 CE settlement value per unit", max(settle - strike, 0.0), "10.50")
    q("per lot of 65", max(settle - strike, 0.0) * NIFTY_LOT, "682.50")


def charges() -> None:
    print("Charges: per-crore rates to percentages, and the cost of selling one NIFTY option lot at Rs 100 premium")
    crore = 1e7
    q("NSE cash transaction charge, Rs 307 per crore (%)", 100 * 307 / crore, "0.00307")
    q("NSE futures transaction charge, Rs 183 per crore (%)", 100 * 183 / crore, "0.00183")
    q("NSE options transaction charge, Rs 3,553 per crore of premium (%)", 100 * 3553 / crore, "0.03553")
    q("SEBI fee, Rs 10 per crore (%)", 100 * 10 / crore, "0.0001")
    premium = 100.0 * NIFTY_LOT
    q("premium turnover of one lot", premium, "6,500")
    stt = 0.0015 * premium
    txn = 3553 / crore * premium
    sebi = 10 / crore * premium
    gst = 0.18 * (txn + sebi)  # no brokerage assumed; stamp duty is charged to the buyer only
    q("STT at 0.15% of premium", stt, "9.75")
    q("exchange transaction charge", txn, "2.31")
    q("SEBI fee", sebi, "0.0065")
    q("GST at 18% on exchange charge and SEBI fee", gst, "0.42")
    total = stt + txn + sebi + gst
    q("total statutory cost for the seller", total, "12.48")
    q("as a share of premium (%)", 100 * total / premium, "0.19")
    assert stt / total > 0.75, "STT is more than three quarters of the statutory cost"


def contract_size() -> None:
    print("SEBI minimum contract value of Rs 15 lakh vs the NIFTY lot")
    level = 24_500.0
    value = NIFTY_LOT * level
    q("NIFTY lot value at 24,500 (Rs lakh)", value / 1e5, "15.93")
    assert value >= 15e5
    q("index level at which a 65 lot is worth exactly Rs 15 lakh", 15e5 / NIFTY_LOT, "23,077")


def max_pain() -> None:
    print("Max pain on a hypothetical chain")
    strikes = np.array([24_300, 24_400, 24_500, 24_600, 24_700], dtype=float)
    call_oi = np.array([20, 35, 60, 90, 70], dtype=float)  # lakh units, hypothetical
    put_oi = np.array([80, 95, 70, 30, 15], dtype=float)
    payouts = []
    for s in strikes:
        pay = float(np.sum(np.maximum(strikes - s, 0) * put_oi) + np.sum(np.maximum(s - strikes, 0) * call_oi))
        payouts.append(pay)
    best = strikes[int(np.argmin(payouts))]
    q("max-pain strike", best, "24,500")
    q("writers' payout at 24,500 (index points x lakh units)", payouts[2], "13,500")
    direct = 100 * 30 + 200 * 15 + 100 * 35 + 200 * 20  # puts above 24,500 and calls below it
    close("payout at 24,500 by a direct table vs the loop", payouts[2], direct, 1e-9)


if __name__ == "__main__":
    closing_vwap()
    charges()
    contract_size()
    max_pain()
    print("all NSE and BSE numbers verified")
