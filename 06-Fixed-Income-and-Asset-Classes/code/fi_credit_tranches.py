"""CDS indices and tranches: upfront, intrinsic spread, one-factor Gaussian copula, LHP, finite pools, compound and base correlation.

Backs every number in `06-Fixed-Income-and-Asset-Classes/23-Credit-Advanced-CDS-Indices-and-Tranches.md`.
- Example 1 and card fi-cdx-standard-cds-coupons: upfront and price of a CDX HY trade.
- Example 2 and card fi-cdx-credit-index-basis: duration-weighted intrinsic spread versus the simple average.
- Example 3 and card fi-cdx-lhp-approximation-vasicek: conditional default probability and LHP tranche expected losses, computed
  twice: by quadrature over the market factor and, independently, by integrating the Vasicek loss distribution.
- Example 4 and cards fi-cdx-compound-correlation-deficiency and fi-cdx-base-correlation-concept: non-monotone mezzanine loss,
  two compound correlations for one price, base correlation pricing and an implied base correlation.
- Example 5 and card fi-cdx-lhp-vs-finite-pool: a 125-name homogeneous pool by conditional binomial versus the LHP limit.
- Example 6 and card fi-cdx-gaussian-copula-tail-dependence: joint default probability ratio of the Gaussian copula as u falls.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_credit_tranches.py`.
"""

from __future__ import annotations

import math
from statistics import NormalDist

QUOTED: list[str] = []
N01 = NormalDist()


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


P_DEF, RHO, RECOVERY = 0.05, 0.30, 0.40
LGD = 1.0 - RECOVERY
M_GRID = [-8.0 + (i + 0.5) * 16.0 / 4000 for i in range(4000)]  # midpoint rule on [-8, 8]
M_STEP = 16.0 / 4000


def cond_pd(p: float, rho: float, m: float) -> float:
    return N01.cdf((N01.inv_cdf(p) - math.sqrt(rho) * m) / math.sqrt(1.0 - rho))


def tranche_loss(portfolio_loss: float, attach: float, detach: float) -> float:
    return min(max(portfolio_loss - attach, 0.0), detach - attach) / (detach - attach)


def lhp_el_quadrature(attach: float, detach: float, rho: float, p: float = P_DEF) -> float:
    """E[tranche loss] with L(m) = LGD p(m), integrated over the market factor."""
    return sum(tranche_loss(LGD * cond_pd(p, rho, m), attach, detach) * N01.pdf(m) * M_STEP for m in M_GRID)


def vasicek_cdf(x: float, rho: float, p: float = P_DEF) -> float:
    if x <= 0.0:
        return 0.0
    if x >= LGD:
        return 1.0
    return N01.cdf((math.sqrt(1.0 - rho) * N01.inv_cdf(x / LGD) - N01.inv_cdf(p)) / math.sqrt(rho))


def lhp_el_vasicek(attach: float, detach: float, rho: float, n: int = 4000) -> float:
    """E[min(max(L - A, 0), D - A)] = integral from A to D of (1 - F(x)) dx, by the midpoint rule."""
    h = (detach - attach) / n
    return sum(1.0 - vasicek_cdf(attach + (i + 0.5) * h, rho) for i in range(n)) * h / (detach - attach)


def finite_pool_el(attach: float, detach: float, rho: float, names: int, p: float = P_DEF) -> float:
    """Homogeneous pool of `names` credits: conditional on m the number of defaults is binomial."""
    total = 0.0
    for m in M_GRID:
        q = cond_pd(p, rho, m)
        el = sum(
            math.comb(names, k) * q**k * (1.0 - q) ** (names - k) * tranche_loss(LGD * k / names, attach, detach) for k in range(names + 1)
        )
        total += el * N01.pdf(m) * M_STEP
    return total


def bisect(fn, lo: float, hi: float, iters: int = 80) -> float:
    f_lo = fn(lo)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if (fn(mid) > 0.0) == (f_lo > 0.0):
            lo, f_lo = mid, fn(mid)
        else:
            hi = mid
    return 0.5 * (lo + hi)


def example1_upfront() -> None:
    print("  1. CDX HY upfront (Example 1, card fi-cdx-standard-cds-coupons)")
    notional, coupon, spread, rpv01 = 50_000_000.0, 0.0500, 0.0420, 4.15
    upfront = (spread - coupon) * rpv01
    quoted("upfront (% of notional)", upfront * 100.0, -3.32, 2)
    quoted("upfront cash ($, negative = paid to the protection buyer)", upfront * notional, -1_660_000.0, 0)
    quoted("quoted price", 100.0 - upfront * 100.0, 103.32, 2)


def flat_rpv01(spread: float, rate: float = 0.04, maturity: float = 5.0) -> float:
    """Continuous-premium risky annuity with a flat hazard spread / LGD (credit triangle)."""
    k = rate + spread / LGD
    return (1.0 - math.exp(-k * maturity)) / k


def example2_intrinsic() -> None:
    print("  2. Intrinsic index spread (Example 2, card fi-cdx-credit-index-basis)")
    spreads = [0.0040, 0.0060, 0.0080, 0.0150, 0.0400]
    simple = sum(spreads) / len(spreads)
    weights = [flat_rpv01(s) for s in spreads]
    intrinsic = sum(s * w for s, w in zip(spreads, weights, strict=True)) / sum(weights)
    quoted("simple average spread (bp)", simple * 1e4, 146.0, 0)
    quoted("RPV01 at 40 bp", weights[0], 4.46, 2)
    quoted("RPV01 at 400 bp", weights[-1], 3.88, 2)
    quoted("duration-weighted intrinsic spread (bp)", intrinsic * 1e4, 139.4, 1)
    quoted("simple average minus intrinsic (bp)", (simple - intrinsic) * 1e4, 6.6, 1)
    quoted("index at 140 bp: basis to simple average (bp)", 140.0 - simple * 1e4, -6.0, 1)
    quoted("index at 140 bp: basis to intrinsic (bp)", 140.0 - intrinsic * 1e4, 0.6, 1)


def example3_lhp() -> None:
    print("  3. One-factor Gaussian copula and the LHP limit (Example 3, card fi-cdx-lhp-approximation-vasicek)")
    quoted("threshold Phi^-1(0.05)", N01.inv_cdf(P_DEF), -1.6449, 4)
    for m, e_pd, e_loss in ((-2.5, 37.09, 22.26), (-2.0, 25.57, 15.34)):
        q = cond_pd(P_DEF, RHO, m)
        quoted(f"p(M = {m}) (%)", q * 100.0, e_pd, 2)
        quoted(f"L(M = {m}) (%)", LGD * q * 100.0, e_loss, 2)
    total = sum(LGD * cond_pd(P_DEF, RHO, m) * N01.pdf(m) * M_STEP for m in M_GRID)
    quoted("p(M = -2.5), 4 dp (%)", cond_pd(P_DEF, RHO, -2.5) * 100.0, 37.0949, 4)
    quoted("expected portfolio loss (%)", total * 100.0, 3.00, 2)
    for (a, d), e in {(0.0, 0.03): 54.11, (0.03, 0.07): 19.58, (0.07, 0.10): 8.78, (0.0, 0.07): 34.38}.items():
        quad = lhp_el_quadrature(a, d, RHO)
        indep = lhp_el_vasicek(a, d, RHO)
        quoted(f"EL [{a:.0%}, {d:.0%}] (%)", quad * 100.0, e, 2)
        assert abs(quad - indep) < 1e-4, f"factor quadrature {quad} vs Vasicek CDF integral {indep}"


def example4_correlation() -> None:
    print("  4. Compound and base correlation (Example 4)")
    for rho, e in ((0.01, 6.18), (0.10, 17.16), (0.30, 19.58), (0.50, 17.77), (0.90, 10.24)):
        quoted(f"mezz [3%, 7%] EL at rho = {rho:.2f} (%)", lhp_el_quadrature(0.03, 0.07, rho) * 100.0, e, 2)
    grid = [0.01 * i for i in range(1, 100)]
    mezz = [lhp_el_quadrature(0.03, 0.07, r) for r in grid]
    peak = max(range(len(grid)), key=lambda i: mezz[i])
    quoted("rho maximizing mezz EL on a 0.01 grid", grid[peak], 0.26, 2)
    quoted("maximum mezz EL (%)", mezz[peak] * 100.0, 19.67, 2)
    equity = [lhp_el_quadrature(0.0, 0.03, r) for r in grid]
    assert all(x > y for x, y in zip(equity, equity[1:], strict=False)), "equity EL must fall as correlation rises"
    target = 0.17
    low = bisect(lambda r: lhp_el_quadrature(0.03, 0.07, r) - target, 0.01, grid[peak])
    high = bisect(lambda r: lhp_el_quadrature(0.03, 0.07, r) - target, grid[peak], 0.99)
    quoted("compound correlation for mezz EL 17%, low root", low, 0.097, 3)
    quoted("compound correlation for mezz EL 17%, high root", high, 0.557, 3)
    # Base correlation: price [3%, 7%] from two equity tranches with their own correlations.
    el03, el07 = lhp_el_quadrature(0.0, 0.03, 0.20), lhp_el_quadrature(0.0, 0.07, 0.30)
    quoted("EL [0%, 3%] at base correlation 0.20 (%)", el03 * 100.0, 62.77, 2)
    quoted("EL [0%, 7%] at base correlation 0.30 (%)", el07 * 100.0, 34.38, 2)
    quoted("EL [3%, 7%] from the two base tranches (%)", (0.07 * el07 - 0.03 * el03) / 0.04 * 100.0, 13.09, 2)
    implied = bisect(lambda r: lhp_el_quadrature(0.0, 0.03, r) - 0.50, 0.01, 0.99)
    quoted("base correlation implied by an equity EL of 50%", implied, 0.353, 3)


def example5_finite() -> None:
    print("  5. 125 names versus the LHP limit (Example 5, card fi-cdx-lhp-vs-finite-pool)")
    for (a, d), e in {(0.0, 0.03): 52.14, (0.03, 0.07): 20.09, (0.07, 0.10): 9.21}.items():
        quoted(f"125-name EL [{a:.0%}, {d:.0%}] (%)", finite_pool_el(a, d, RHO, 125) * 100.0, e, 2)
    quoted(
        "LHP minus 125-name equity EL (points)", (lhp_el_quadrature(0.0, 0.03, RHO) - finite_pool_el(0.0, 0.03, RHO, 125)) * 100.0, 1.96, 2
    )


def example6_tail() -> None:
    print("  6. Gaussian copula tail dependence (Example 6, card fi-cdx-gaussian-copula-tail-dependence)")
    for u, e in ((0.05, 0.1427), (0.01, 0.0556), (0.001, 0.0149)):
        c = N01.inv_cdf(u)
        joint = sum(N01.cdf((c - math.sqrt(RHO) * m) / math.sqrt(1.0 - RHO)) ** 2 * N01.pdf(m) * M_STEP for m in M_GRID)
        quoted(f"P(U1 < u | U2 < u) at u = {u}", joint / u, e, 4)


def main() -> None:
    print("=== fi_credit_tranches: CDS Indices and Tranches ===")
    example1_upfront()
    example2_intrinsic()
    example3_lhp()
    example4_correlation()
    example5_finite()
    example6_tail()
    print(f"\nSuccessfully verified {len(QUOTED)} credit index and tranche figures.")


if __name__ == "__main__":
    main()
