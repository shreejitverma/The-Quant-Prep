"""Yield curve construction, dual-curve swap pricing, Jacobian risk mapping, and Treasury futures basis.

Reference implementation for the fixed income curve and risk notes.
Run ``python curve_bootstrap.py``: the ``__main__`` block validates every result
with self-checking assertions against derived and closed-form values.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# ---------------------------------------------------------------- linear algebra


def solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    """Solve A x = b via Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(m[r][i]))
        m[i], m[max_row] = m[max_row], m[i]
        pivot = m[i][i]
        if abs(pivot) < 1e-12:
            raise ValueError("Singular matrix in linear solve")
        for j in range(i, n + 1):
            m[i][j] /= pivot
        for r in range(n):
            if r != i:
                factor = m[r][i]
                for c in range(i, n + 1):
                    m[r][c] -= factor * m[i][c]
    return [m[i][n] for i in range(n)]


def invert_matrix(a: list[list[float]]) -> list[list[float]]:
    """Invert square matrix A via column-by-column Gaussian elimination."""
    n = len(a)
    cols: list[list[float]] = []
    for col in range(n):
        unit = [1.0 if i == col else 0.0 for i in range(n)]
        cols.append(solve_linear(a, unit))
    return [[cols[c][r] for c in range(n)] for r in range(n)]


# ---------------------------------------------------------------- discount curve


@dataclass
class DiscountCurve:
    """Zero curve with log-linear discount factor interpolation (piecewise constant forward)."""

    times: list[float]  # sorted pillar maturities in years, e.g. [1.0, 2.0, 3.0]
    dfs: list[float]  # discount factors P(0, T_i)

    def __post_init__(self) -> None:
        if len(self.times) != len(self.dfs):
            raise ValueError("Mismatched times and dfs lengths")
        for i in range(len(self.times) - 1):
            if self.times[i] >= self.times[i + 1]:
                raise ValueError("Times must be strictly increasing")
        for df in self.dfs:
            if df <= 0.0:
                raise ValueError("Discount factors must be positive")

    def df(self, t: float) -> float:
        """Discount factor P(0, t)."""
        if t <= 0.0:
            return 1.0
        if t <= self.times[0]:
            # Extrapolate flat forward from origin to first pillar
            f0 = -math.log(self.dfs[0]) / self.times[0]
            return math.exp(-f0 * t)
        if t >= self.times[-1]:
            # Extrapolate flat forward of the last interval
            dt = self.times[-1] - self.times[-2]
            f_last = -(math.log(self.dfs[-1]) - math.log(self.dfs[-2])) / dt
            return self.dfs[-1] * math.exp(-f_last * (t - self.times[-1]))

        # Binary search for interval
        lo, hi = 0, len(self.times) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.times[mid] <= t:
                lo = mid
            else:
                hi = mid
        t1, t2 = self.times[lo], self.times[hi]
        p1, p2 = self.dfs[lo], self.dfs[hi]
        w = (t - t1) / (t2 - t1)
        return math.exp((1.0 - w) * math.log(p1) + w * math.log(p2))

    def zero_rate(self, t: float) -> float:
        """Continuously compounded zero rate z(t) = -ln(P(t)) / t."""
        if t <= 0.0:
            return -math.log(self.dfs[0]) / self.times[0]
        return -math.log(self.df(t)) / t

    def forward_rate(self, t1: float, t2: float) -> float:
        """Simply compounded forward rate over [t1, t2]: (P(t1)/P(t2) - 1) / (t2 - t1)."""
        if t2 <= t1:
            raise ValueError("t2 must be strictly greater than t1")
        p1 = self.df(t1)
        p2 = self.df(t2)
        return (p1 / p2 - 1.0) / (t2 - t1)


# ---------------------------------------------------------------- swap pricing


def swap_annuity(curve: DiscountCurve, schedule: list[float]) -> float:
    """Annuity A = sum tau_i * P(0, T_i) for a coupon schedule with annual or fractional steps."""
    a = 0.0
    for i in range(len(schedule)):
        t_prev = 0.0 if i == 0 else schedule[i - 1]
        t_curr = schedule[i]
        tau = t_curr - t_prev
        a += tau * curve.df(t_curr)
    return a


def par_swap_rate_single_curve(curve: DiscountCurve, schedule: list[float]) -> float:
    """Single-curve par swap rate S = (P(0, T0) - P(0, Tn)) / Annuity."""
    t0 = 0.0
    tn = schedule[-1]
    annuity = swap_annuity(curve, schedule)
    return (curve.df(t0) - curve.df(tn)) / annuity


def par_swap_rate_dual_curve(
    discount_curve: DiscountCurve,
    forward_curve: DiscountCurve,
    schedule: list[float],
) -> float:
    """Dual-curve par swap rate with OIS discounting and index forwarding."""
    annuity = swap_annuity(discount_curve, schedule)
    float_pv = 0.0
    for i in range(len(schedule)):
        t_prev = 0.0 if i == 0 else schedule[i - 1]
        t_curr = schedule[i]
        tau = t_curr - t_prev
        fwd = forward_curve.forward_rate(t_prev, t_curr)
        float_pv += tau * discount_curve.df(t_curr) * fwd
    return float_pv / annuity


# ---------------------------------------------------------------- bootstrap & jacobian


def _require_annual_pillars(maturities: list[float]) -> None:
    """The annual-pay bootstrap and Jacobian need pillars exactly 1, 2, ..., n years."""
    if maturities != [float(k) for k in range(1, len(maturities) + 1)]:
        raise ValueError("Pillars must be consecutive whole years 1, 2, ..., n")


def bootstrap_single_curve(maturities: list[float], par_rates: list[float]) -> DiscountCurve:
    """Bootstrap a single curve from sequential annual par swap rates."""
    _require_annual_pillars(maturities)
    n = len(maturities)
    if len(par_rates) != n:
        raise ValueError("Mismatched maturities and rates")

    dfs: list[float] = []
    for k in range(n):
        s_k = par_rates[k]
        if k == 0:
            # 1-year swap: s_1 * P_1 + P_1 = 1 => P_1 = 1 / (1 + s_1)
            p_k = 1.0 / (1.0 + s_k)
        else:
            # s_k * sum_{i=0}^{k-1} P_i + (1 + s_k) * P_k = 1
            sum_prev = sum(dfs)
            p_k = (1.0 - s_k * sum_prev) / (1.0 + s_k)
        dfs.append(p_k)
    return DiscountCurve(maturities, dfs)


def swap_jacobian(curve: DiscountCurve, maturities: list[float], par_rates: list[float]) -> list[list[float]]:
    """Jacobian matrix J = [ds_i / dz_j] relating par swap quotes to pillar zero rates."""
    _require_annual_pillars(maturities)
    n = len(maturities)
    # Zero rates at pillars: z_j = -ln(P_j) / T_j
    # We compute ds_i / dz_j via chain rule: (ds_i / dP_k) * (dP_k / dz_k)
    p = [curve.df(t) for t in maturities]
    a = [sum(p[: k + 1]) for k in range(n)]

    j_s_z = [[0.0] * n for _ in range(n)]
    for i in range(n):
        s_i = par_rates[i]
        a_i = a[i]
        for k in range(i + 1):
            ds_dp_k = -s_i / a_i if k < i else -(1.0 + s_i) / a_i
            dp_k_dz_k = -maturities[k] * p[k]
            j_s_z[i][k] = ds_dp_k * dp_k_dz_k
    return j_s_z


def map_zero_risk_to_par_risk(d_pv_dz: list[float], j_s_z: list[list[float]]) -> list[float]:
    """Transform zero sensitivities dPV/dz into market par quote sensitivities dPV/ds via J^{-1}."""
    j_z_s = invert_matrix(j_s_z)
    n = len(d_pv_dz)
    return [sum(d_pv_dz[k] * j_z_s[k][i] for k in range(n)) for i in range(n)]


# ---------------------------------------------------------------- treasury futures


def cme_conversion_factor(coupon: float, years: int) -> float:
    """Price of 1 par at a 6% semiannual yield for a maturity of exactly `years` whole years.

    This is only the z = 0 special case of CME's formula and is not rounded; CME rounds the
    remaining maturity down to whole months or quarters and the factor to four decimals, as
    implemented and checked against CME's published examples in `fi_treasury_futures.py`.
    """
    n_semi = 2 * years
    r_semi = 0.03
    return (coupon / 2.0 / r_semi) * (1.0 - (1.0 + r_semi) ** (-n_semi)) + (1.0 + r_semi) ** (-n_semi)


def treasury_futures_basis(
    clean_spot: float,
    accrued_spot: float,
    futures_price: float,
    cf: float,
    accrued_delivery: float,
    days_to_delivery: int,
) -> tuple[float, float, float]:
    """Compute (gross_basis, invoice_price, implied_repo_rate).

    Gross Basis = Clean Spot - Futures Price * CF
    Invoice Price = Futures Price * CF + Accrued Delivery
    Implied Repo Rate = (Invoice Price - Dirty Spot) / Dirty Spot * (360 / days)
    """
    dirty_spot = clean_spot + accrued_spot
    invoice_price = futures_price * cf + accrued_delivery
    gross_basis = clean_spot - futures_price * cf
    irr = ((invoice_price - dirty_spot) / dirty_spot) * (360.0 / days_to_delivery)
    return gross_basis, invoice_price, irr


# ---------------------------------------------------------------- self-check


def main() -> None:
    # 1. Curve bootstrap from 3 annual par swaps: 3.0%, 3.5%, 4.0%
    pillars = [1.0, 2.0, 3.0]
    par_rates = [0.03, 0.035, 0.04]
    curve = bootstrap_single_curve(pillars, par_rates)

    # Check analytical discount factors
    p1_expected = 1.0 / 1.03
    p2_expected = (1.0 - 0.035 * p1_expected) / 1.035
    p3_expected = (1.0 - 0.04 * (p1_expected + p2_expected)) / 1.04
    assert abs(curve.df(1.0) - p1_expected) < 1e-12
    assert abs(curve.df(2.0) - p2_expected) < 1e-12
    assert abs(curve.df(3.0) - p3_expected) < 1e-12

    # Check par swap rates match quotes exactly
    assert abs(par_swap_rate_single_curve(curve, [1.0]) - 0.03) < 1e-12
    assert abs(par_swap_rate_single_curve(curve, [1.0, 2.0]) - 0.035) < 1e-12
    assert abs(par_swap_rate_single_curve(curve, [1.0, 2.0, 3.0]) - 0.04) < 1e-12

    # Reject pillars other than 1, 2, ..., n years
    for bad_pillars in ([2.0, 5.0, 10.0], [1.0, 2.0, 4.0], [0.5, 1.0, 1.5]):
        try:
            bootstrap_single_curve(bad_pillars, par_rates)
        except ValueError:
            pass
        else:
            raise AssertionError(f"bootstrap_single_curve accepted pillars {bad_pillars}")
        try:
            swap_jacobian(curve, bad_pillars, par_rates)
        except ValueError:
            pass
        else:
            raise AssertionError(f"swap_jacobian accepted pillars {bad_pillars}")

    # Check log-linear interpolation at midpoint 1.5y
    mid_df = curve.df(1.5)
    expected_mid = math.exp(0.5 * math.log(p1_expected) + 0.5 * math.log(p2_expected))
    assert abs(mid_df - expected_mid) < 1e-12

    # 2. Jacobian matrix verification against finite differences
    j_s_z = swap_jacobian(curve, pillars, par_rates)
    h = 1e-6
    for i in range(3):
        for k in range(3):
            # Bump zero rate k
            bumped_dfs = [curve.df(t) for t in pillars]
            bumped_dfs[k] = math.exp(-pillars[k] * (curve.zero_rate(pillars[k]) + h))
            bumped_curve = DiscountCurve(pillars, bumped_dfs)
            s_bumped = par_swap_rate_single_curve(bumped_curve, pillars[: i + 1])
            s_base = par_rates[i]
            fd = (s_bumped - s_base) / h
            assert abs(fd - j_s_z[i][k]) < 1e-4

    # 3. Par risk transformation
    # 3-year par bond (coupon 4%, face 100): cashflows [4, 4, 104]
    p_vec = [curve.df(t) for t in pillars]
    d_pv_dz = [-(k + 1) * cf * p_vec[k] for k, cf in enumerate([4.0, 4.0, 104.0])]
    d_pv_ds = map_zero_risk_to_par_risk(d_pv_dz, j_s_z)

    # A par bond must have 0 sensitivity to earlier benchmark par quotes
    assert abs(d_pv_ds[0]) < 1e-9
    assert abs(d_pv_ds[1]) < 1e-9
    # And sensitivity to its own par quote must equal -Annuity * 100
    annuity_3 = sum(p_vec)
    assert abs(d_pv_ds[2] - (-annuity_3 * 100.0)) < 1e-9

    # 4. Dual-curve swap pricing
    # OIS curve with 3.0%, 3.5% par rates; projection zeros 20bp above those par rates
    ois_curve = DiscountCurve([1.0, 2.0], [p1_expected, p2_expected])
    proj_dfs = [1.0 / 1.032, 1.0 / (1.037**2)]
    proj_curve = DiscountCurve([1.0, 2.0], proj_dfs)
    s_dual = par_swap_rate_dual_curve(ois_curve, proj_curve, [1.0, 2.0])

    # Hand-computed in note 13 Example 1: 0.0702914 / 1.9042259 = 3.69134%.
    assert abs(s_dual - 0.0369134) < 1e-7

    # 5. Treasury futures conversion factor & basis
    cf_4 = cme_conversion_factor(0.04, 10)
    cf_6 = cme_conversion_factor(0.06, 10)
    assert abs(cf_6 - 1.0) < 1e-12
    assert abs(cf_4 - 0.851225) < 1e-5

    gross_basis, invoice, irr = treasury_futures_basis(
        clean_spot=94.00,
        accrued_spot=0.50,
        futures_price=110.00,
        cf=cf_4,
        accrued_delivery=1.50,
        days_to_delivery=90,
    )
    assert abs(gross_basis - 0.3652) < 1e-3
    assert abs(invoice - 95.1348) < 1e-3
    assert abs(irr - 0.02687) < 1e-4

    print("Curve bootstrap, dual-curve swap, Jacobian risk, and Treasury futures tests passed!")


if __name__ == "__main__":
    main()
