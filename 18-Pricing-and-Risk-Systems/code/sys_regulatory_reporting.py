"""Regulatory reporting pipeline: an SA-CCR service request, a pre-submission ratio check and a GL-to-risk reconciliation.

Backs every number in `18-Pricing-and-Risk-Systems/12-Regulatory-Reporting-Pipeline.md`.
Trades, balances, tolerances and the reconciliation data set are labelled-hypothetical inputs.
SA-CCR is computed here from CRE52 directly and cross-checked against the independently written and verified
implementation in `17-Regulatory-Capital-Basel-and-FRTB/code/basel_credit_saccr.py`.
The reconciliation is a real matching function over a seeded synthetic data set, not arithmetic on literals; it is
tested on data sets whose GL and risk ledgers are built separately from one trade universe and a planted-fault list it
never sees (missing, extra and duplicated rows, ids differing in case or whitespace, differences just inside, at and
just outside the tolerance on small and large values, float noise on small values), its output must equal the
outcome each fault was designed to produce, and the same matcher without id normalisation must fail.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_regulatory_reporting.py`.
"""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def load_reference_saccr():
    path = Path(__file__).resolve().parents[2] / "17-Regulatory-Capital-Basel-and-FRTB" / "code" / "basel_credit_saccr.py"
    spec = importlib.util.spec_from_file_location("basel_credit_saccr_ref", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolve their module through sys.modules
    spec.loader.exec_module(module)
    return module


# ============================================================================
# 1. SA-CCR for an unmargined netting set (CRE52)
# ============================================================================

ALPHA, FLOOR = 1.4, 0.05
SF_IR, SF_FX = 0.005, 0.04  # CRE52.72 supervisory factors


def saccr_two_trades(v_ir: float, v_fx: float) -> dict[str, float]:
    sd = (math.exp(-0.05 * 0.0) - math.exp(-0.05 * 5.0)) / 0.05  # CRE52.34, S = 0, E = 5
    d_ir = 100_000_000.0 * sd  # adjusted notional, payer swap: supervisory delta +1, MF 1 for M >= 1 year
    addon_ir = SF_IR * d_ir  # one trade in one hedging set and one maturity bucket
    d_fx = 50_000_000.0 * 1.10  # EUR notional in USD, MF 1
    addon_fx = SF_FX * d_fx
    addon = addon_ir + addon_fx  # aggregate add-on: sum across asset classes (CRE52.24)
    v = v_ir + v_fx
    rc = max(v, 0.0)  # CRE52.10 with no collateral
    mult = min(1.0, FLOOR + (1 - FLOOR) * math.exp(v / (2 * (1 - FLOOR) * addon)))  # CRE52.23
    pfe = mult * addon
    return {
        "sd": sd,
        "d_ir": d_ir,
        "addon_ir": addon_ir,
        "addon_fx": addon_fx,
        "addon": addon,
        "v": v,
        "rc": rc,
        "mult": mult,
        "pfe": pfe,
        "ead": ALPHA * (rc + pfe),
    }


def check_saccr() -> None:
    print("  1. SA-CCR service request: unmargined netting set with a swap and an FX forward")
    ref = load_reference_saccr()
    base = saccr_two_trades(1_500_000.0, -300_000.0)
    quoted("supervisory duration of the 5-year swap", base["sd"], 4.4240, 4)
    quoted("swap adjusted notional ($)", base["d_ir"], 442_398_434, 0)
    quoted("IR add-on ($)", base["addon_ir"], 2_211_992, 0)
    quoted("FX add-on ($)", base["addon_fx"], 2_200_000, 0)
    quoted("aggregate add-on ($)", base["addon"], 4_411_992, 0)
    quoted("net replacement cost ($)", base["rc"], 1_200_000, 0)
    quoted("PFE multiplier", base["mult"], 1.0, 4)
    quoted("EAD ($)", base["ead"], 7_856_789, 0)
    quoted("RWA at a 100% risk weight ($)", base["ead"] * 1.00, 7_856_789, 0)
    # the same netting set through the reference implementation
    trades = (
        ref.Trade("S1", "IR", "", 100_000_000.0, 1_500_000.0, 5.0, direction=+1, end=5.0, hedging_set="USD"),
        ref.Trade("F1", "FX", "", 55_000_000.0, -300_000.0, 1.0, direction=+1, hedging_set="EURUSD"),
    )
    r = ref.saccr_ead(ref.NettingSet(trades))
    assert abs(r.ead - base["ead"]) < 1e-6 and abs(r.addon_aggregate - base["addon"]) < 1e-6
    # out of the money: the multiplier falls below 1
    otm = saccr_two_trades(-1_700_000.0, -300_000.0)
    r2 = ref.saccr_ead(
        ref.NettingSet(
            (
                ref.Trade("S1", "IR", "", 100_000_000.0, -1_700_000.0, 5.0, direction=+1, end=5.0, hedging_set="USD"),
                ref.Trade("F1", "FX", "", 55_000_000.0, -300_000.0, 1.0, direction=+1, hedging_set="EURUSD"),
            )
        )
    )
    assert abs(r2.ead - otm["ead"]) < 1e-6
    quoted("multiplier with net value -2,000,000", otm["mult"], 0.7984, 4)
    quoted("EAD with net value -2,000,000 ($)", otm["ead"], 4_931_272, 0)
    quoted("margined maturity factor at a 10-day MPOR (CRE52.52)", 1.5 * math.sqrt(10 / 250), 0.3, 1)
    quoted("supervisory duration of a 200-year swap, near its bound of 20", (1 - math.exp(-0.05 * 200)) / 0.05, 20.0, 1)


# ============================================================================
# 2. Pre-submission check: CET1 ratio against its components
# ============================================================================


def check_ratio_validation() -> None:
    print("  2. Pre-submission check of a reported CET1 ratio (hypothetical bank, EUR)")
    cet1, trea, reported = 45_250_000_000.0, 380_000_000_000.0, 0.1185
    implied = cet1 / trea
    quoted("CET1 ratio implied by the reported components (%)", implied * 100, 11.91, 2)
    quoted("difference from the reported 11.85% (bp)", (implied - reported) * 1e4, 5.8, 1)
    tolerance_bp = 1.0  # hypothetical internal tolerance
    assert abs(implied - reported) * 1e4 > tolerance_bp
    quoted("TREA that would give 11.85% (EUR bn)", cet1 / reported / 1e9, 381.86, 2)
    quoted("RWA the ratio was computed on beyond the template (EUR bn)", (cet1 / reported - trea) / 1e9, 1.86, 2)


# ============================================================================
# 3. GL-to-risk reconciliation by trade id
# ============================================================================


@dataclass
class Recon:
    """Break categories keyed by normalised trade id; differences are GL less risk, in dollars."""

    missing: dict[str, float]  # in the GL, not in risk
    extra: dict[str, float]  # in risk, not in the GL
    duplicate: set[str]  # booked more than once in one store; the first row is used
    breaks: dict[str, float]  # value differences above tolerance
    within: dict[str, float]  # non-zero value differences at or within tolerance


def normalise_id(tid: str) -> str:
    return tid.strip().upper()


def reconcile(gl_rows: list[tuple[str, float]], risk_rows: list[tuple[str, float]], tolerance: float, key=normalise_id) -> Recon:
    """Match two stores on normalised trade ids (trimmed, upper-cased) and compare values in whole cents."""
    duplicate: set[str] = set()

    def index(rows: list[tuple[str, float]]) -> dict[str, int]:
        out: dict[str, int] = {}
        for tid, value in rows:
            k = key(tid)
            if k in out:
                duplicate.add(k)
            else:
                out[k] = round(value * 100)
        return out

    gl, risk = index(gl_rows), index(risk_rows)
    tol = round(tolerance * 100)
    diffs = {k: gl[k] - risk[k] for k in gl.keys() & risk.keys() if gl[k] != risk[k]}
    return Recon(
        missing={k: gl[k] / 100 for k in gl.keys() - risk.keys()},
        extra={k: risk[k] / 100 for k in risk.keys() - gl.keys()},
        duplicate=duplicate,
        breaks={k: d / 100 for k, d in diffs.items() if abs(d) > tol},
        within={k: d / 100 for k, d in diffs.items() if abs(d) <= tol},
    )


SPELLINGS = (str.lower, lambda s: f" {s}", lambda s: f"{s.lower()}\t", lambda s: f"{s} ", lambda s: f" {s.lower()} ")

NOISY_TENTHS = [k for k in range(3, 1000) if sum([0.1] * k) != k / 10]  # float sums that miss the decimal value


def injected_faults(seed: int, tolerance: float) -> tuple[list[tuple[str, float]], list[tuple[str, float]], dict]:
    """GL and risk ledgers built separately from one trade universe and a planted-fault list, and the outcome each
    planted fault was designed to produce (differences in cents, GL less risk)."""
    rng = random.Random(seed)
    tol_c = round(tolerance * 100)
    universe = {f"T{i:05d}": round(rng.lognormvariate(13.0, 1.5) * 100) for i in range(400)}  # true values in cents
    picked = rng.sample(list(universe), 27)
    faults: list[tuple[str, str, int]] = [("missing", t, 0) for t in picked[0:4]]
    faults += [("duplicate in GL", t, 0) for t in picked[4:6]] + [("duplicate in risk", t, 0) for t in picked[6:8]]
    faults += [("respelled", t, i) for i, t in enumerate(picked[8:13])]
    sized = ((picked[13:17], "below", tol_c - 1), (picked[17:19], "at", tol_c), (picked[19:23], "above", tol_c + 1))
    for group, kind, size_c in sized:
        for j, t in enumerate(group):
            if j % 2:  # every other one on a notional barely larger than the tolerance
                universe[t] = rng.randint(tol_c + 200, 5 * tol_c)
            faults.append((kind, t, rng.choice((-1, 1)) * size_c))
    for t in picked[23:27]:
        universe[t] = 10 * rng.choice(NOISY_TENTHS)
        faults.append(("float noise", t, 0))
    faults += [("extra", f"X{seed:02d}{j:03d}", round(rng.uniform(1e5, 1e8))) for j in range(4)]

    plan = {t: (kind, arg) for kind, t, arg in faults}
    gl_rows = [(t, c / 100) for t, c in universe.items()]
    gl_rows += [(t, universe[t] / 100) for kind, t, _ in faults if kind == "duplicate in GL"]
    risk_rows: list[tuple[str, float]] = []
    for t, c in universe.items():
        kind, arg = plan.get(t, ("", 0))
        if kind == "missing":
            continue
        tid = SPELLINGS[arg](t) if kind == "respelled" else t
        if kind == "float noise":
            value = sum([0.1] * (c // 10))
        elif kind in ("below", "at", "above"):
            value = c / 100 - arg / 100
        else:
            value = c / 100
        risk_rows += [(tid, value)] * (2 if kind == "duplicate in risk" else 1)
    risk_rows += [(t, arg / 100) for kind, t, arg in faults if kind == "extra"]
    rng.shuffle(risk_rows)

    def ids(*kinds: str) -> set[str]:
        return {t for kind, t, _ in faults if kind in kinds}

    truth = {
        "missing": ids("missing"),
        "extra": ids("extra"),
        "duplicate": ids("duplicate in GL", "duplicate in risk"),
        "breaks": {t: arg for kind, t, arg in faults if kind == "above"},
        "within": {t: arg for kind, t, arg in faults if kind in ("below", "at")},
    }
    return gl_rows, risk_rows, truth


def planted_fault_mismatches(seed: int, tolerance: float, key=normalise_id) -> list[str]:
    """Categories in which reconcile() disagrees with the planted ground truth."""
    gl_rows, risk_rows, truth = injected_faults(seed, tolerance)
    r = reconcile(gl_rows, risk_rows, tolerance, key)
    found = {
        "missing": set(r.missing),
        "extra": set(r.extra),
        "duplicate": r.duplicate,
        "breaks": {k: round(v * 100) for k, v in r.breaks.items()},
        "within": {k: round(v * 100) for k, v in r.within.items()},
    }
    return [name for name in truth if found[name] != truth[name]]


def check_reconcile_against_injected_faults(tolerance: float, seeds: range = range(1, 6)) -> None:
    for seed in seeds:
        bad = planted_fault_mismatches(seed, tolerance)
        assert not bad, f"seed {seed}: reconcile() disagrees with the planted faults in {bad}"
        broken = planted_fault_mismatches(seed, tolerance, key=str)
        assert {"missing", "extra"} <= set(broken), f"seed {seed}: a matcher without id normalisation passed"
    print(f"    reconcile() recovered every planted fault on {len(seeds)} independently generated data sets")
    print("    negative control: the same matcher without id normalisation fails on every one")


def check_reconciliation() -> None:
    print("  3. Month-end reconciliation of derivative asset fair values, GL against risk (seed 239)")
    tolerance = 1_000.0  # per-trade tolerance, hypothetical
    check_reconcile_against_injected_faults(tolerance)
    rng = random.Random(239)
    n = 2_000
    gl = {f"T{i:05d}": round(rng.lognormvariate(14.5, 1.0), 2) for i in range(n)}
    risk = dict(gl)
    for i in range(n - 45, n):  # 45 trades that never reached the risk store
        risk.pop(f"T{i:05d}")
    for i in range(10):  # 10 trades revalued at a different FX fixing in risk
        risk[f"T{i:05d}"] = round(risk[f"T{i:05d}"] * 0.9995, 2)
    r = reconcile(list(gl.items()), list(risk.items()), tolerance)
    total_gap = sum(gl.values()) - sum(risk.values())
    missing = sum(r.missing.values())
    quoted("GL total ($m)", sum(gl.values()) / 1e6, 6_706.95, 2)
    quoted("risk total before investigation ($m)", sum(risk.values()) / 1e6, 6_553.83, 2)
    quoted("total gap ($m)", total_gap / 1e6, 153.12, 2)
    quoted("trades in GL but not in risk", len(r.missing), 45, 0)
    quoted("value of trades missing from risk ($m)", missing / 1e6, 153.11, 2)
    quoted("trades with value breaks above tolerance", len(r.breaks), 3, 0)
    quoted("trades with value breaks within tolerance", len(r.within), 7, 0)
    quoted("sum of breaks above tolerance ($)", sum(r.breaks.values()), 10_112, 0)
    quoted("residual after replaying the missing trades ($)", total_gap - missing, 12_507, 0)


def main() -> None:
    print("Regulatory reporting pipeline checks")
    check_saccr()
    check_ratio_validation()
    check_reconciliation()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All regulatory reporting checks passed.")


if __name__ == "__main__":
    main()
