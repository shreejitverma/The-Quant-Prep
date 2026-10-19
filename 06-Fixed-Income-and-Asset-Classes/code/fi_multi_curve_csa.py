"""Multi-curve pricing, collateral discounting, tenor and cross-currency basis, collateral choice.

Backs every number in `06-Fixed-Income-and-Asset-Classes/13-Multi-Curve-and-CSA-Discounting.md`.
Independent checks: par rates from the closed form are re-derived by a bisection root search on the
swap's cash-flow NPV, the cross-currency basis implied by an FX forward is recovered by bisection and
compared with the input, and the collateral-choice discount factor in closed form is compared with a
seeded Monte Carlo estimate.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_multi_curve_csa.py`.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def bisect(f: Callable[[float], float], lo: float, hi: float, tol: float = 1e-14) -> float:
    flo = f(lo)
    assert flo * f(hi) < 0.0, "root not bracketed"
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if fm == 0.0 or hi - lo < tol:
            return mid
        if (fm < 0.0) == (flo < 0.0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def example_dual_curve() -> None:
    print("  1. Dual-curve versus single-curve par swap rate (2y annual)")
    p_ois = [1.0 / 1.03]
    p_ois.append((1.0 - 0.035 * p_ois[0]) / 1.035)
    annuity = sum(p_ois)
    s_single = (1.0 - p_ois[1]) / annuity
    quoted("P_ois(1)", p_ois[0], 0.970874, 6)
    quoted("P_ois(2)", p_ois[1], 0.933352, 6)
    quoted("OIS annuity", annuity, 1.904226, 6)
    quoted("2y OIS par rate reprices (%)", s_single * 100.0, 3.5000, 4)
    quoted("2y OIS zero rate, annual compounding (%)", (p_ois[1] ** -0.5 - 1.0) * 100.0, 3.5088, 4)
    p_proj = [1.0 / 1.032, 1.0 / 1.037**2]
    fwd = [1.0 / p_proj[0] - 1.0, p_proj[0] / p_proj[1] - 1.0]
    quoted("P_proj(1)", p_proj[0], 0.968992, 6)
    quoted("P_proj(2)", p_proj[1], 0.929913, 6)
    quoted("projected forward 0-1y (%)", fwd[0] * 100.0, 3.2000, 4)
    quoted("projected forward 1-2y (%)", fwd[1] * 100.0, 4.2024, 4)
    pv1, pv2 = p_ois[0] * fwd[0], p_ois[1] * fwd[1]
    quoted("floating coupon 1 PV", pv1, 0.031068, 6)
    quoted("floating coupon 2 PV", pv2, 0.039223, 6)
    quoted("floating leg PV", pv1 + pv2, 0.070291, 6)
    s_dual = (pv1 + pv2) / annuity
    quoted("dual-curve par rate (%)", s_dual * 100.0, 3.6913, 4)
    quoted("dual minus single (bp)", (s_dual - s_single) * 1e4, 19.13, 2)

    def npv(k: float) -> float:  # receive float, pay fixed k, cash flow by cash flow
        return sum(df * (f - k) for df, f in zip(p_ois, fwd, strict=True))

    root = bisect(npv, 0.0, 0.10)
    assert abs(root - s_dual) < 1e-12
    # Discounting the same projected flows on the projection curve (the pre-2008 habit).
    s_proj_disc = sum(df * f for df, f in zip(p_proj, fwd, strict=True)) / sum(p_proj)
    quoted("par rate if discounted on the projection curve (%)", s_proj_disc * 100.0, 3.6909, 4)


def example_tenor_basis() -> None:
    print("  2. 3M versus 6M tenor basis (1y, OIS discounting)")
    p = {t: math.exp(-0.03 * t) for t in (0.25, 0.5, 0.75, 1.0)}
    for t, v in zip((0.25, 0.5, 0.75, 1.0), (0.992528, 0.985112, 0.977751, 0.970446), strict=True):
        quoted(f"P_ois({t})", p[t], v, 6)
    f3 = [0.032, 0.033, 0.034, 0.035]
    f6 = [0.0345, 0.0365]
    a4 = 0.25 * sum(p.values())
    pv3 = 0.25 * sum(p[t] * f for t, f in zip((0.25, 0.5, 0.75, 1.0), f3, strict=True))
    pv6 = 0.5 * (p[0.5] * f6[0] + p[1.0] * f6[1])
    quoted("quarterly annuity", a4, 0.981459, 6)
    quoted("semiannual annuity", 0.5 * (p[0.5] + p[1.0]), 0.977779, 6)
    quoted("PV 3M leg", pv3, 0.032870, 6)
    quoted("PV 6M leg", pv6, 0.034704, 6)
    beta = (pv6 - pv3) / a4

    def npv(b: float) -> float:
        return pv3 + b * a4 - pv6

    assert abs(bisect(npv, -0.01, 0.01) - beta) < 1e-12
    quoted("par basis on the 3M leg (bp)", beta * 1e4, 18.69, 2)
    two_3m = (1 + 0.25 * f3[0]) * (1 + 0.25 * f3[1])
    quoted("two 3M periods compounded, as a 6M rate (%)", (two_3m - 1.0) / 0.5 * 100.0, 3.2632, 4)


def example_xccy() -> None:
    print("  3. EUR/USD cross-currency basis and the FX forward")
    spot, usd, eur, basis, days = 1.1000, 0.0500, 0.0350, -0.0025, 365
    tau = days / 360.0
    fwd_cip = spot * (1.0 + usd * tau) / (1.0 + eur * tau)
    fwd_mkt = spot * (1.0 + usd * tau) / (1.0 + (eur + basis) * tau)
    quoted("EUR notional for 100mm USD", 100_000_000.0 / spot, 90_909_090.91, 2)
    quoted("1y forward with zero basis (USD per EUR)", fwd_cip, 1.116156, 6)
    quoted("1y forward with -25 bp basis (USD per EUR)", fwd_mkt, 1.118895, 6)
    quoted("forward points difference (pips)", (fwd_mkt - fwd_cip) * 1e4, 27.39, 2)

    def gap(b: float) -> float:
        return spot * (1.0 + usd * tau) / (1.0 + (eur + b) * tau) - fwd_mkt

    implied = bisect(gap, -0.02, 0.02)
    quoted("basis implied by the forward (bp)", implied * 1e4, -25.0, 1)
    quoted("all-in synthetic USD cost for EUR funded at the EUR rate (%)", (usd - basis) * 100.0, 5.25, 2)


def example_collateral_option() -> None:
    print("  4. Collateral currency choice (cheapest to deliver)")
    t, c1, mu, sigma = 5.0, 0.04, -0.0010, 0.0030
    df_fixed = math.exp(-c1 * t)
    # Spread s of currency 2 over currency 1 (domestic-equivalent) drawn once, constant thereafter.
    e_opt = norm_cdf(-mu / sigma) + math.exp(-t * mu + 0.5 * t * t * sigma * sigma) * norm_cdf(mu / sigma - t * sigma)
    df_opt = df_fixed * e_opt
    rng = random.Random(20261018)
    n = 400_000
    mc = sum(math.exp(-t * max(rng.gauss(mu, sigma), 0.0)) for _ in range(n)) / n
    assert abs(mc - e_opt) < 5e-5
    quoted("DF posting currency 1 only", df_fixed, 0.818731, 6)
    quoted("DF with the choice (closed form)", df_opt, 0.815635, 6)
    quoted("DF with the choice (Monte Carlo, about)", df_fixed * mc, 0.81563, 5)
    quoted("value of the option per 100 received in 5y", (df_fixed - df_opt) * 100.0, 0.3096, 4)
    quoted("equivalent running spread (bp)", -math.log(df_opt / df_fixed) / t * 1e4, 7.58, 2)

    df_at_mean = df_fixed * math.exp(-t * max(mu, 0.0))
    quoted("value if the spread were fixed at its mean (no optionality)", (df_fixed - df_at_mean) * 100.0, 0.0, 4)


def main() -> None:
    print("=== fi_multi_curve_csa: multi-curve and collateral discounting ===")
    example_dual_curve()
    example_tenor_basis()
    example_xccy()
    example_collateral_option()
    print(f"\nVerified {len(QUOTED)} multi-curve and CSA figures.")


if __name__ == "__main__":
    main()
