"""Regulatory reporting pipeline: an SA-CCR service request, a pre-submission ratio check and a GL-to-risk reconciliation.

Backs every number in `18-Pricing-and-Risk-Systems/12-Regulatory-Reporting-Pipeline.md`.
Trades, balances, tolerances and the reconciliation data set are labelled-hypothetical inputs.
SA-CCR is computed here from CRE52 directly and cross-checked against the independently written and verified
implementation in `17-Regulatory-Capital-Basel-and-FRTB/code/basel_credit_saccr.py`.
The reconciliation is a real matching function over a seeded synthetic data set, not arithmetic on literals; it is
tested on separately generated data sets whose faults (missing, extra and duplicated rows, ids differing in case or
whitespace, differences just inside, at and just outside the tolerance, float noise on small values) it never sees,
and its output must equal the ground truth each fault was built to produce.
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


def reconcile(gl_rows: list[tuple[str, float]], risk_rows: list[tuple[str, float]], tolerance: float) -> Recon:
    """Match two stores on trimmed, upper-cased trade ids and compare values in whole cents."""
    duplicate: set[str] = set()

    def index(rows: list[tuple[str, float]]) -> dict[str, int]:
        out: dict[str, int] = {}
        for tid, value in rows:
            key = tid.strip().upper()
            if key in out:
                duplicate.add(key)
            else:
                out[key] = round(value * 100)
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


def injected_faults(seed: int, tolerance: float) -> tuple[list[tuple[str, float]], list[tuple[str, float]], dict]:
    """GL and risk rows with planted faults, and the categories each fault was built to land in (differences in cents)."""
    rng = random.Random(seed)
    ids = [f"T{i:05d}" for i in range(400)]
    value = {t: round(rng.lognormvariate(13.0, 1.5), 2) for t in ids}
    picked = rng.sample(ids, 26)
    missing, dup, renamed = picked[0:4], picked[4:8], picked[8:13]
    below, at, above, noisy = picked[13:16], picked[16:18], picked[18:22], picked[22:26]
    extra = [f"X{seed:02d}{j:03d}" for j in range(4)]
    tol_c = round(tolerance * 100)
    shift_c: dict[str, int] = {}
    for group, size_c in ((below, tol_c - 1), (at, tol_c), (above, tol_c + 1)):
        for t in group:
            shift_c[t] = rng.choice((-1, 1)) * size_c
    tenths = {t: rng.randint(3, 999) for t in noisy}
    for t in noisy:
        value[t] = round(tenths[t] / 10, 2)
    risk_value = {t: value[t] - shift_c.get(t, 0) / 100 for t in ids}
    for t in noisy:
        risk_value[t] = sum([0.1] * tenths[t])
    assert any(risk_value[t] != value[t] for t in noisy), "float noise must reach the matcher"
    gl_rows = [(t, value[t]) for t in ids] + [(t, value[t]) for t in dup[:2]]
    spellings = (str.lower, lambda s: f" {s}", lambda s: f"{s.lower()}\t", lambda s: f"{s} ", lambda s: s.title())
    risk_rows = [(spellings[renamed.index(t)](t) if t in renamed else t, risk_value[t]) for t in ids if t not in missing]
    risk_rows += [(t, risk_value[t]) for t in dup[2:]] + [(t, rng.uniform(1e3, 1e6)) for t in extra]
    truth = {
        "missing": set(missing),
        "extra": set(extra),
        "duplicate": set(dup),
        "breaks": {t: shift_c[t] for t in above},
        "within": {t: shift_c[t] for t in below + at},
    }
    return gl_rows, risk_rows, truth


def check_reconcile_against_injected_faults(tolerance: float, seeds: range = range(1, 6)) -> None:
    for seed in seeds:
        gl_rows, risk_rows, truth = injected_faults(seed, tolerance)
        r = reconcile(gl_rows, risk_rows, tolerance)
        assert set(r.missing) == truth["missing"], f"seed {seed}: missing"
        assert set(r.extra) == truth["extra"], f"seed {seed}: extra"
        assert r.duplicate == truth["duplicate"], f"seed {seed}: duplicate"
        assert {k: round(v * 100) for k, v in r.breaks.items()} == truth["breaks"], f"seed {seed}: breaks"
        assert {k: round(v * 100) for k, v in r.within.items()} == truth["within"], f"seed {seed}: within"
    print(f"    reconcile() recovered every planted fault on {len(seeds)} independently generated data sets")


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
    assert not r.extra and not r.duplicate
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
