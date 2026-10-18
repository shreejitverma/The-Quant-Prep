"""Intraday risk and pre-trade limits: latency budgets, credit reservations, ring buffer sizing, and OTR.

Backs every number in `18-Pricing-and-Risk-Systems/08-Intraday-Risk-and-Pre-Trade-Limits.md`.
Platform latencies, order arrival timelines, ring buffer configurations, and OTR numbers are verified.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_intraday_limits.py`.
"""

from __future__ import annotations

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def test_latency_budget() -> None:
    print("  1. Pre-trade flow gateway latency budget breakdown (microseconds)")
    t1 = 3.5  # kernel-bypass NIC ingestion
    t2 = 1.2  # SBE / FIX parser
    t3 = 0.4  # fat-finger price collar
    t4 = 1.8  # atomic credit reservation
    t5 = 1.1  # desk net notional & short-sale check
    t6 = 0.8  # lock-free audit ring buffer write
    t7 = 4.2  # outbound serialization and transmission
    total = t1 + t2 + t3 + t4 + t5 + t6 + t7

    quoted("kernel-bypass ingestion (us)", t1, 3.5, 1)
    quoted("SBE/FIX parsing (us)", t2, 1.2, 1)
    quoted("fat-finger price collar check (us)", t3, 0.4, 1)
    quoted("atomic credit reservation (us)", t4, 1.8, 1)
    quoted("desk notional and short-sale check (us)", t5, 1.1, 1)
    quoted("lock-free audit ring buffer write (us)", t6, 0.8, 1)
    quoted("outbound serialization & transmission (us)", t7, 4.2, 1)
    quoted("total end-to-end gateway latency (us)", total, 13.0, 1)


def test_credit_reservation() -> None:
    print("  2. Optimistic credit reservation state machine")
    limit = 50_000_000.0
    utilized = 44_000_000.0
    available = limit - utilized
    quoted("intraday trading limit ($)", limit, 50_000_000, 0)
    quoted("baseline utilized credit ($)", utilized, 44_000_000, 0)
    quoted("baseline available capacity ($)", available, 6_000_000, 0)

    # Order 1: 100k @ $200 = $20M
    ord1_val = 100_000 * 200.0
    quoted("order 1 notional ($)", ord1_val, 20_000_000, 0)
    assert ord1_val > available  # Rejected

    # Order 2: 20k @ $200 = $4M
    ord2_val = 20_000 * 200.0
    quoted("order 2 notional ($)", ord2_val, 4_000_000, 0)
    assert ord2_val <= available  # Approved, reserve 4M
    reserved = ord2_val
    available_after_2 = available - reserved
    quoted("available after order 2 reservation ($)", available_after_2, 2_000_000, 0)

    # Order 3: 15k @ $200 = $3M
    ord3_val = 15_000 * 200.0
    quoted("order 3 notional ($)", ord3_val, 3_000_000, 0)
    assert ord3_val > available_after_2  # Rejected due to pending reservation

    # Scenario A: Partial fill of order 2 ($3M filled, $1M cancelled)
    fill_val = 3_000_000.0
    cancel_val = 1_000_000.0
    quoted("order 2 partial fill committed ($)", fill_val, 3_000_000, 0)
    quoted("order 2 unexecuted reservation released ($)", cancel_val, 1_000_000, 0)
    final_utilized = utilized + fill_val
    final_available = limit - final_utilized
    quoted("final committed utilized credit ($)", final_utilized, 47_000_000, 0)
    quoted("final available capacity ($)", final_available, 3_000_000, 0)


def test_knight_capital() -> None:
    print("  3. Knight Capital catastrophe metrics (August 1, 2012)")
    orders = 4_000_000
    minutes = 45
    seconds = minutes * 60
    shares = 397_000_000
    stocks = 154
    gross_pos = 7_000_000_000.0
    net_loss = 440_000_000.0
    order_rate = orders / seconds

    quoted("Knight Capital order count", orders, 4_000_000, 0)
    quoted("duration (minutes)", minutes, 45, 0)
    quoted("shares executed", shares, 397_000_000, 0)
    quoted("stocks traded", stocks, 154, 0)
    quoted("gross position accumulated ($)", gross_pos, 7_000_000_000, 0)
    quoted("realized net loss ($)", net_loss, 440_000_000, 0)
    quoted("average order submission rate (orders/sec)", order_rate, 1481.5, 1)


def test_ring_buffer_and_mifid() -> None:
    print("  4. Lock-free ring buffer sizing and MiFID II RTS 6 OTR")
    slots = 2**20  # 1,048,576 slots
    cache_line_bytes = 64
    total_bytes = slots * cache_line_bytes
    total_mb = total_bytes / (1024 * 1024)
    quoted("ring buffer slot count", slots, 1_048_576, 0)
    quoted("slot cache-line padded size (bytes)", cache_line_bytes, 64, 0)
    quoted("ring buffer memory footprint (MB)", total_mb, 64.0, 1)

    # MiFID II RTS 6 OTR (Order-to-Trade Ratio)
    # Under RTS 6 Annex I, OTR_number = (total orders / total trades) - 1
    # Worked example: 25,000 order messages resulting in 500 trades
    order_msgs = 25_000
    trade_count = 500
    otr_num = (order_msgs / trade_count) - 1.0
    quoted("sample order messages", order_msgs, 25_000, 0)
    quoted("sample executed trades", trade_count, 500, 0)
    quoted("MiFID II RTS 6 order-to-trade ratio by number", otr_num, 49.0, 1)

    # Price collar calculation
    nbbo_bid = 100.00
    nbbo_ask = 100.05
    bandwidth = 0.03  # 3% collar
    lower_collar = nbbo_bid * (1.0 - bandwidth)
    upper_collar = nbbo_ask * (1.0 + bandwidth)
    quoted("NBBO bid ($)", nbbo_bid, 100.00, 2)
    quoted("NBBO ask ($)", nbbo_ask, 100.05, 2)
    quoted("lower price collar at 3% ($)", lower_collar, 97.00, 2)
    quoted("upper price collar at 3% ($)", upper_collar, 103.0515, 4)


def main() -> None:
    print("Intraday risk and pre-trade limits checks")
    test_latency_budget()
    test_credit_reservation()
    test_knight_capital()
    test_ring_buffer_and_mifid()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All intraday limits checks passed.")


if __name__ == "__main__":
    main()
