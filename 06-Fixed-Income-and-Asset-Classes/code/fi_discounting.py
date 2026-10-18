"""Discount factors, compounding, forwards, par yields, bootstrapping and interpolation.

Backs every number in note 01 (Discounting and Yield Curves).
Each `q(...)` call computes a value independently (closed form, solve or enumeration),
asserts it against the literal the note quotes at the note's rounding, and prints it,
so a change to either the code or the note fails CI.
Run with `python 06-Fixed-Income-and-Asset-Classes/code/fi_discounting.py`.
"""

from __future__ import annotations

import math


def q(tag: str, label: str, value: float, text: str) -> None:
    """Assert that `value` rounds to the quoted `text` (half a unit of its last decimal) and print it."""
    decimals = len(text.split(".")[1]) if "." in text else 0
    literal = float(text.replace(",", ""))
    assert abs(value - literal) <= 0.5 * 10.0**-decimals + 1e-12, f"[{tag}] {label}: computed {value!r}, note quotes {text}"
    print(f"  [{tag}] {label} = {text}")


# ------------------------------------------------------------ compounding conversions


def df_from_rate(rate: float, t: float, m: int | None) -> float:
    """Discount factor for a zero rate compounded m times a year (m=None: continuous)."""
    if m is None:
        return math.exp(-rate * t)
    return (1.0 + rate / m) ** (-m * t)


def rate_from_df(p: float, t: float, m: int | None) -> float:
    """Zero rate compounded m times a year (m=None: continuous) that reproduces the discount factor p."""
    if m is None:
        return -math.log(p) / t
    return m * (p ** (-1.0 / (m * t)) - 1.0)


def simple_forward(p1: float, p2: float, tau: float) -> float:
    """Simply compounded forward over an accrual tau: (P1/P2 - 1)/tau."""
    return (p1 / p2 - 1.0) / tau


def bond_price(coupon: float, dfs: list[float]) -> float:
    """Price per 100 of an annual-coupon bullet given discount factors at years 1..n."""
    return 100.0 * (coupon * sum(dfs) + dfs[-1])


def par_coupon(dfs: list[float]) -> float:
    """Annual par coupon c_n = (1 - P_n) / sum P_i."""
    return (1.0 - dfs[-1]) / sum(dfs)


def ytm_annual(price: float, coupon: float, n: int) -> float:
    """Annual-compounded yield to maturity by bisection; price is strictly decreasing in yield."""
    lo, hi = -0.5, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        p = 100.0 * (sum(coupon / (1 + mid) ** i for i in range(1, n + 1)) + 1 / (1 + mid) ** n)
        if p > price:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def bootstrap_par(par: list[float]) -> list[float]:
    """Discount factors at years 1..n from annual par yields: P_n = (1 - c_n sum_{i<n} P_i) / (1 + c_n)."""
    dfs: list[float] = []
    for c in par:
        dfs.append((1.0 - c * sum(dfs)) / (1.0 + c))
    return dfs


# ------------------------------------------------------------ interpolation


def loglinear_df(times: list[float], dfs: list[float], t: float) -> float:
    """Log-linear interpolation of discount factors (piecewise-constant instantaneous forwards); pillars include t=0."""
    for i in range(len(times) - 1):
        t1, t2 = times[i], times[i + 1]
        if t1 <= t <= t2:
            w = (t - t1) / (t2 - t1)
            return math.exp((1 - w) * math.log(dfs[i]) + w * math.log(dfs[i + 1]))
    raise ValueError("t outside pillars")


def linear_zero(times: list[float], zeros: list[float], t: float) -> tuple[float, float]:
    """Linear interpolation of continuous zero rates; returns (z(t), z'(t)) using the segment containing t (left-closed)."""
    for i in range(len(times) - 1):
        t1, t2 = times[i], times[i + 1]
        if t1 <= t < t2 or (i == len(times) - 2 and t == t2):
            slope = (zeros[i + 1] - zeros[i]) / (t2 - t1)
            return zeros[i] + slope * (t - t1), slope
    raise ValueError("t outside pillars")


def main() -> None:
    print("Note 01: Discounting and Yield Curves")

    # --- compounding conversions (Core concepts table, cards fi-compounding-conversion, fi-dc-compounding-equivalents)
    q("fi-compounding-conversion", "3% annual as continuous, %", 100 * rate_from_df(df_from_rate(0.03, 1, 1), 1, None), "2.9559")
    q("Pitfalls", "3% annual minus its continuous equivalent, bp", 1e4 * (0.03 - math.log(1.03)), "4.41")
    q("fi-dc-compounding-equivalents", "3% continuous as annual, %", 100 * (math.exp(0.03) - 1), "3.0455")
    p5 = df_from_rate(0.05, 1, 1)
    q("fi-dc-compounding-equivalents", "5% annual as semiannual, %", 100 * rate_from_df(p5, 1, 2), "4.9390")
    q("fi-dc-compounding-equivalents", "5% annual as monthly, %", 100 * rate_from_df(p5, 1, 12), "4.8889")
    q("fi-dc-compounding-equivalents", "5% annual as continuous, %", 100 * rate_from_df(p5, 1, None), "4.8790")
    # the equivalent rates must reprice the same 10y discount factor
    for m in (2, 12, None):
        assert abs(df_from_rate(rate_from_df(p5, 1, m), 10, m) - 1.05**-10) < 1e-12

    # --- money-market deposit, ACT/360 versus a wrong ACT/365 accrual (Example 4, card fi-dc-day-count-mixing)
    days = 182
    p_mm = 1 / (1 + 0.04 * days / 360)
    p_wrong = 1 / (1 + 0.04 * days / 365)
    q("ex4", "6m 4.00% ACT/360 deposit discount factor", p_mm, "0.980179")
    q("ex4", "continuous zero on ACT/365F time, %", 100 * -math.log(p_mm) / (days / 365), "4.0151")
    q("fi-dc-day-count-mixing", "discount factor with ACT/365 accrual by mistake", p_wrong, "0.980445")
    q("fi-dc-day-count-mixing", "PV error on 100mm paid in 182 days, USD", 1e8 * (p_wrong - p_mm), "26,622")

    # --- Example 1: zero curve to discount factors and forwards (cards fi-forward-from-discount, fi-zero-forward-relation)
    zeros = [0.03, 0.035, 0.04]
    p = [df_from_rate(z, t + 1, 1) for t, z in enumerate(zeros)]
    q("ex1", "P(0,1)", p[0], "0.970874")
    q("ex1", "P(0,2)", p[1], "0.933511")
    q("ex1", "P(0,3)", p[2], "0.888996")
    f12 = simple_forward(p[0], p[1], 1.0)
    f23 = simple_forward(p[1], p[2], 1.0)
    q("fi-forward-from-discount", "1y1y forward, %", 100 * f12, "4.0024")
    q("ex1", "2y1y forward, %", 100 * f23, "5.0073")
    q("ex1", "1 + F(1,2)", 1 + f12, "1.040024")
    q("ex1", "1 + F(2,3)", 1 + f23, "1.050073")
    growth = 1.03 * (1 + f12) * (1 + f23)
    q("ex1", "(1.03)(1+F12)(1+F23)", growth, "1.124864")
    assert abs(growth - 1.04**3) < 1e-12  # the forwards chain back to the 3y zero exactly

    # --- Example 2: price the 3y 4% annual bond on that curve (card fi-dc-ytm-of-curve-bond)
    px = bond_price(0.04, p)
    q("ex2", "3y 4% bond price on the zero curve", px, "100.0732")
    q("ex2", "3y par coupon, %", 100 * par_coupon(p), "3.974")
    y = ytm_annual(px, 0.04, 3)
    q("fi-dc-ytm-of-curve-bond", "yield to maturity of that bond, %", 100 * y, "3.9737")
    # The yield must reprice the bond; and it differs from both the 3y zero (4%) and the par coupon.
    assert abs(100 * (sum(0.04 / (1 + y) ** i for i in (1, 2, 3)) + (1 + y) ** -3) - px) < 1e-9
    q("ex2", "3y par coupon to 6 decimals, %", 100 * par_coupon(p), "3.973810")

    # --- Example 3: bootstrap from par yields (card fi-bootstrap-par-yields, fi-par-vs-zero)
    boot = bootstrap_par([0.03, 0.035])
    q("fi-bootstrap-par-yields", "P(0,1) from 3% par", boot[0], "0.970874")
    q("fi-bootstrap-par-yields", "P(0,2) from 3.5% par", boot[1], "0.933352")
    q("fi-par-vs-zero", "2y zero (annual) from bootstrap, %", 100 * rate_from_df(boot[1], 2, 1), "3.5088")
    # bootstrapped curve reprices both par bonds to exactly 100
    assert abs(bond_price(0.03, boot[:1]) - 100) < 1e-10 and abs(bond_price(0.035, boot) - 100) < 1e-10

    # --- Example 5: interpolation changes the forwards (cards fi-log-linear-interp, fi-dc-interp-forward-jump)
    times = [0.0, 1.0, 2.0, 3.0]
    dfs = [1.0, *p]
    zc = [rate_from_df(pp, t + 1, None) for t, pp in enumerate(p)]
    q("ex5", "continuous zero 1y, %", 100 * zc[0], "2.9559")
    q("ex5", "continuous zero 2y, %", 100 * zc[1], "3.4401")
    q("ex5", "continuous zero 3y, %", 100 * zc[2], "3.9221")
    # log-linear DF: forward on [1,2] and [2,3] is ln(P1/P2) and ln(P2/P3) (continuous)
    f_ll_12 = math.log(p[0] / p[1])
    f_ll_23 = math.log(p[1] / p[2])
    q("ex5", "log-linear: instantaneous forward on (1,2), %", 100 * f_ll_12, "3.9244")
    q("ex5", "log-linear: instantaneous forward on (2,3), %", 100 * f_ll_23, "4.8859")
    q("fi-log-linear-interp", "log-linear forward jump at the 2y pillar, bp", 1e4 * (f_ll_23 - f_ll_12), "96")
    h = 1e-7
    fd_ll = -(math.log(loglinear_df(times, dfs, 2.5 + h)) - math.log(loglinear_df(times, dfs, 2.5 - h))) / (2 * h)
    assert abs(fd_ll - f_ll_23) < 1e-6  # finite-difference forward of the interpolated curve
    # linear zero: f(t) = z(t) + t z'(t); at 2- uses the (1,2) slope, at 2+ the (2,3) slope
    _, s_12 = linear_zero([1.0, 2.0, 3.0], zc, 1.5)
    z_2, s_23 = linear_zero([1.0, 2.0, 3.0], zc, 2.0)
    f_lin_left = z_2 + 2.0 * s_12
    f_lin_right = z_2 + 2.0 * s_23
    q("ex5", "linear zero: forward just below 2y, %", 100 * f_lin_left, "4.4087")
    q("ex5", "linear zero: forward just above 2y, %", 100 * f_lin_right, "4.4040")
    z3, s3 = linear_zero([1.0, 2.0, 3.0], zc, 3.0)
    q("ex5", "linear zero: forward at 3y (end of last segment), %", 100 * (z3 + 3.0 * s3), "5.3679")
    # the two interpolations agree at pillars but not between them
    z25, _ = linear_zero([1.0, 2.0, 3.0], zc, 2.5)
    q("fi-dc-interp-forward-jump", "P(0,2.5) log-linear", loglinear_df(times, dfs, 2.5), "0.910982")
    q("fi-dc-interp-forward-jump", "P(0,2.5) linear zero", math.exp(-z25 * 2.5), "0.912080")

    # --- Example 6: extrapolation to 5y (card fi-dc-flat-forward-extrap)
    q("ex6", "3y continuous zero as a decimal", zc[2], "0.039221")
    q("ex6", "last log-linear forward as a decimal", f_ll_23, "0.048859")
    p5_flat_zero = math.exp(-zc[2] * 5)
    p5_flat_fwd = p[2] * math.exp(-f_ll_23 * 2)
    q("fi-dc-flat-forward-extrap", "P(0,5) flat zero beyond 3y", p5_flat_zero, "0.821927")
    q("fi-dc-flat-forward-extrap", "P(0,5) flat forward beyond 3y", p5_flat_fwd, "0.806234")
    q("fi-dc-flat-forward-extrap", "PV difference per 100mm paid at 5y, USD mm", 100 * (p5_flat_zero - p5_flat_fwd), "1.5693")

    # --- Example 7: negative rates (card fi-dc-negative-df)
    p_neg = df_from_rate(-0.005, 2, 1)
    q("fi-dc-negative-df", "2y discount factor at -0.50% annual", p_neg, "1.010076")
    assert p_neg > 1.0 and math.log(p_neg) > 0.0

    print("All note 01 checks passed.")


if __name__ == "__main__":
    main()
