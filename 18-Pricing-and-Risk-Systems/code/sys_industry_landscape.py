"""Industry landscape: buy-versus-build cost arithmetic and XVA simulation sizing.

Backs every number in `18-Pricing-and-Risk-Systems/17-Industry-Landscape.md`.

1. Five-year cost of a vendor platform versus an in-house build versus a hybrid, from labelled-hypothetical cash flows:
   upfront costs at time 0 and recurring costs at the end of each year; nominal totals, present values at 8%, and the
   discount rate at which the vendor and in-house options cost the same (found by bisection and checked by
   re-discounting).
2. Sensitivity: how many in-house engineers make the build cost the same as the vendor at 8%.
3. Monte Carlo exposure sizing for an XVA run: valuations, core-hours, wall time, and the memory of netting-set versus
   trade-level exposure cubes, from labelled-hypothetical inputs.

No figure here is a vendor price or a vendor performance number; all inputs are hypothetical teaching values.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_industry_landscape.py`.
"""

from __future__ import annotations

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure (half a unit in the last place)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


YEARS = 5
ENGINEER_COST = 0.3  # $ million per engineer-year, fully loaded (hypothetical)


def option_cash_flows(upfront: float, recurring: float) -> list[float]:
    """Cash outflows in $ million at t = 0, 1, ..., 5."""
    return [upfront] + [recurring] * YEARS


def vendor() -> list[float]:
    licence, implementation = 12.0, 18.0
    maintenance, engineers, infra = 4.5, 15, 1.5
    return option_cash_flows(licence + implementation, maintenance + engineers * ENGINEER_COST + infra)


def in_house(engineers: float = 45) -> list[float]:
    build, infra = 14.0, 2.0
    return option_cash_flows(build, engineers * ENGINEER_COST + infra)


def hybrid() -> list[float]:
    # Vendor platform for post-trade processing, in-house pricing and XVA on open-source libraries.
    back_licence, back_engineers = 1.2, 4
    front_build, front_engineers, front_infra = 5.0, 20, 1.2
    recurring = back_licence + back_engineers * ENGINEER_COST + front_engineers * ENGINEER_COST + front_infra
    return option_cash_flows(front_build, recurring)


def pv(cfs: list[float], r: float) -> float:
    return sum(cf / (1.0 + r) ** t for t, cf in enumerate(cfs))


def test_costs() -> None:
    print("  1. Five-year cost ($ million; upfront at t = 0, recurring at year ends; hypothetical)")
    options = {"vendor": vendor(), "in-house": in_house(), "hybrid": hybrid()}
    expected = {
        "vendor": (30.0, 10.5, 82.5, 71.92),
        "in-house": (14.0, 15.5, 91.5, 75.89),
        "hybrid": (5.0, 9.6, 53.0, 43.33),
    }
    for name, cfs in options.items():
        up, rec, nominal, pv8 = expected[name]
        quoted(f"{name}: upfront", cfs[0], up, 1)
        quoted(f"{name}: recurring per year", cfs[1], rec, 1)
        quoted(f"{name}: five-year nominal", sum(cfs), nominal, 1)
        quoted(f"{name}: present value at 8%", pv(cfs, 0.08), pv8, 2)
    v, b = options["vendor"], options["in-house"]
    quoted("vendor minus in-house, upfront", v[0] - b[0], 16.0, 1)
    quoted("in-house minus vendor, per year", b[1] - v[1], 5.0, 1)
    quoted("in-house minus vendor, nominal", sum(b) - sum(v), 9.0, 1)
    quoted("in-house minus vendor, present value at 8%", pv(b, 0.08) - pv(v, 0.08), 3.96, 2)
    # Discount rate at which both cost the same: 16 more upfront for the vendor against 5 more a year in-house.
    lo, hi = 0.0, 1.0
    diff = [x - y for x, y in zip(b, v, strict=True)]
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if pv(diff, mid) > 0.0:
            lo = mid
        else:
            hi = mid
    r_star = 0.5 * (lo + hi)
    assert abs(pv(b, r_star) - pv(v, r_star)) < 1e-9  # re-discounting both options confirms the root
    quoted("break-even discount rate (%)", 100.0 * r_star, 16.99, 2)
    quoted("hybrid saving versus vendor, nominal", sum(v) - sum(options["hybrid"]), 29.5, 1)


def test_engineer_sensitivity() -> None:
    print("  2. In-house team size that matches the vendor's present value at 8%")
    target = pv(vendor(), 0.08)
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if pv(in_house(mid), 0.08) < target:
            lo = mid
        else:
            hi = mid
    n_star = 0.5 * (lo + hi)
    assert abs(pv(in_house(n_star), 0.08) - target) < 1e-9
    quoted("break-even in-house engineers", n_star, 41.7, 1)


def test_xva_sizing() -> None:
    print("  3. Monte Carlo exposure sizing (hypothetical portfolio and timings)")
    trades, netting_sets, paths, dates = 5_000, 12, 10_000, 80
    valuations = trades * paths * dates
    quoted("trade valuations (billions)", valuations / 1e9, 4.0, 1)
    micros = 50.0  # hypothetical average cost of one trade valuation on one core
    core_seconds = valuations * micros / 1e6
    quoted("core-seconds", core_seconds, 200_000, 0)
    quoted("core-hours", core_seconds / 3600.0, 55.6, 1)
    quoted("wall time on 128 cores (minutes)", core_seconds / 128 / 60.0, 26.0, 1)
    quoted("wall time on 1,024 cores (minutes)", core_seconds / 1024 / 60.0, 3.3, 1)
    ns_bytes = netting_sets * dates * paths * 8
    quoted("netting-set exposure cube (MB, decimal)", ns_bytes / 1e6, 76.8, 1)
    quoted("netting-set exposure cube (MiB)", ns_bytes / 2**20, 73.2, 1)
    trade_bytes = trades * dates * paths * 8
    quoted("trade-level exposure cube (GB, decimal)", trade_bytes / 1e9, 32.0, 1)


def main() -> None:
    print("Industry landscape checks")
    test_costs()
    test_engineer_sensitivity()
    test_xva_sizing()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All industry landscape checks passed.")


if __name__ == "__main__":
    main()
