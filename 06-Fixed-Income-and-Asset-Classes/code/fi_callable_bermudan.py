"""Callable bonds and Bermudan swaptions: tree, Gaussian convolution, exercise boundary, LSM and negative convexity.

Backs every number in `06-Fixed-Income-and-Asset-Classes/20-Callable-and-Bermudan-Products.md`.
- Example 1: Hull-White trinomial tree (rates_models.py) for a 5y co-terminal Bermudan payer, cross-checked by a second method,
  backward induction by Gaussian convolution in LGM coordinates, and by Jamshidian for each co-terminal European.
- Example 2 and card fi-callable-bermudan-exercise-boundary: the exercise boundary as a critical swap rate per exercise date.
- Example 3 and card fi-callable-bermudan-lsmc-bias: Longstaff-Schwartz with an out-of-sample pricing set.
- Example 4 and card fi-callable-bermudan-negative-convexity: straight bond yield metrics, yield-to-worst, and a 10y callable bond
  priced in the same model at three rate levels, with effective duration and convexity.
- Example 5: the toy Longstaff-Schwartz regression step.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_callable_bermudan.py`.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np
from rates_models import hw_bermudan_swaption_tree, hw_swaption_jamshidian

QUOTED: list[str] = []

A_MR, SIGMA_HW = 0.03, 0.012


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


class LGM:
    """Hull-White in LGM coordinates on a flat continuously compounded curve; prices by Gaussian convolution of V / N."""

    def __init__(self, level: float, a: float = A_MR, sigma: float = SIGMA_HW, n_grid: int = 2001, half_width: float = 0.4) -> None:
        self.level, self.a, self.sigma = level, a, sigma
        self.x = np.linspace(-half_width, half_width, n_grid)
        self.dx = float(self.x[1] - self.x[0])

    def disc(self, t: float) -> float:
        return math.exp(-self.level * t)

    def h(self, t: float) -> float:
        return (1.0 - math.exp(-self.a * t)) / self.a

    def zeta(self, t: float) -> float:
        return self.sigma**2 * (math.exp(2.0 * self.a * t) - 1.0) / (2.0 * self.a)

    def bond(self, t: float, big_t: float, x: np.ndarray) -> np.ndarray:
        ht, hb, z = self.h(t), self.h(big_t), self.zeta(t)
        return self.disc(big_t) / self.disc(t) * np.exp(-(hb - ht) * x - 0.5 * (hb * hb - ht * ht) * z)

    def numeraire(self, t: float, x: np.ndarray) -> np.ndarray:
        return np.exp(self.h(t) * x + 0.5 * self.h(t) ** 2 * self.zeta(t)) / self.disc(t)

    def convolve(self, u: np.ndarray, t_from: float, t_to: float) -> np.ndarray:
        """E[U(t_to, x') | x(t_from) = x] on the grid, with x' - x ~ N(0, zeta(t_to) - zeta(t_from)) (trapezoid on the grid)."""
        sd = math.sqrt(self.zeta(t_to) - self.zeta(t_from))
        z = (self.x[None, :] - self.x[:, None]) / sd
        kernel = np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi) * self.dx / sd
        return kernel @ u

    def value_at_zero(self, u: np.ndarray, t: float) -> float:
        sd = math.sqrt(self.zeta(t))
        weights = np.exp(-0.5 * (self.x / sd) ** 2) / math.sqrt(2.0 * math.pi) * self.dx / sd
        return float(weights @ u)


def payer_value(model: LGM, t: float, swap_end: float, strike: float, x: np.ndarray) -> np.ndarray:
    """Value at t of paying fixed `strike` annually and receiving floating until swap_end (single curve)."""
    pay_times = [t + i + 1.0 for i in range(int(round(swap_end - t)))]
    annuity = sum(model.bond(t, tp, x) for tp in pay_times)
    return 1.0 - model.bond(t, swap_end, x) - strike * annuity


def par_swap_rate(model: LGM, t: float, swap_end: float, x: np.ndarray) -> np.ndarray:
    pay_times = [t + i + 1.0 for i in range(int(round(swap_end - t)))]
    annuity = sum(model.bond(t, tp, x) for tp in pay_times)
    return (1.0 - model.bond(t, swap_end, x)) / annuity


def bermudan_by_convolution(model: LGM, exercise: Sequence[float], swap_end: float, strike: float) -> tuple[float, dict[float, float]]:
    """Bermudan payer by backward induction of V / N; returns the price and the critical swap rate per exercise date."""
    u = None
    t_next = None
    boundary: dict[float, float] = {}
    for t in sorted(exercise, reverse=True):
        intrinsic = np.maximum(payer_value(model, t, swap_end, strike, model.x), 0.0) / model.numeraire(t, model.x)
        cont = np.zeros_like(model.x) if u is None else model.convolve(u, t, t_next)
        gain = intrinsic - cont
        exercise_region = (gain > 0.0) & (intrinsic > 0.0)
        # Exercise is optimal above a single critical state; interpolate the sign change of the gain.
        i = int(np.argmax(exercise_region))
        x_star = model.x[i - 1] + (model.x[i] - model.x[i - 1]) * (-gain[i - 1]) / (gain[i] - gain[i - 1]) if u is not None else None
        if x_star is None:  # last date: exercise whenever the swap is in the money
            pv = payer_value(model, t, swap_end, strike, model.x)
            j = int(np.argmax(pv > 0.0))
            x_star = model.x[j - 1] + (model.x[j] - model.x[j - 1]) * (-pv[j - 1]) / (pv[j] - pv[j - 1])
        boundary[t] = float(par_swap_rate(model, t, swap_end, np.array([x_star]))[0])
        u = np.maximum(intrinsic, cont)
        t_next = t
    return model.value_at_zero(u, t_next), boundary


def example1_bermudan() -> None:
    print("  1. Bermudan payer: tree, convolution and Jamshidian (Example 1)")

    def discount_curve(t: float) -> float:
        return math.exp(-0.04 * t)

    strike, exercises, swap_end = 0.04, [1.0, 2.0, 3.0, 4.0], 5.0
    p_berm, p_eur, p_prem = hw_bermudan_swaption_tree(discount_curve, strike, exercises, swap_end, 1, A_MR, SIGMA_HW, dt=0.05)
    quoted("tree European 1y into 4y", p_eur, 0.0176082, 7)
    quoted("tree Bermudan", p_berm, 0.0232815, 7)
    quoted("tree premium (bp)", p_prem * 1e4, 56.73, 2)
    jam = {t: hw_swaption_jamshidian(discount_curve, strike, t, swap_end - t, 1, A_MR, SIGMA_HW) for t in exercises}
    for t, e in zip(exercises, (0.017568, 0.017794, 0.014075, 0.007912), strict=True):
        quoted(f"Jamshidian {int(t)}y into {int(swap_end - t)}y", jam[t], e, 6)
    quoted("tree European error vs Jamshidian (%)", (p_eur / jam[1.0] - 1.0) * 100.0, 0.23, 2)

    model = LGM(0.04)
    euro_conv, _ = bermudan_by_convolution(model, [1.0], swap_end, strike)
    berm_conv, boundary = bermudan_by_convolution(model, exercises, swap_end, strike)
    quoted("convolution European 1y into 4y", euro_conv, 0.017568, 6)
    assert abs(euro_conv - jam[1.0]) < 2e-6, "convolution must reproduce Jamshidian"
    quoted("convolution Bermudan", berm_conv, 0.023232, 6)
    quoted("convolution premium (bp)", (berm_conv - euro_conv) * 1e4, 56.6, 1)
    quoted("premium over European (%)", (berm_conv / euro_conv - 1.0) * 100.0, 32.2, 1)
    quoted("tree Bermudan above convolution (%)", (p_berm / berm_conv - 1.0) * 100.0, 0.21, 2)
    assert berm_conv > max(jam.values()), "a Bermudan is worth at least its most valuable European"
    assert berm_conv < sum(jam.values()), "and less than the sum of the Europeans"
    quoted("sum of the four Europeans", sum(jam.values()), 0.057350, 6)
    quoted("value missed by the best European (%)", (1.0 - max(jam.values()) / berm_conv) * 100.0, 23.4, 1)
    quoted("annual par swap rate of the curve (%)", (math.exp(0.04) - 1.0) * 100.0, 4.08, 2)

    print("  2. Exercise boundary as a critical par swap rate (Example 2, card fi-callable-bermudan-exercise-boundary)")
    for t, e in zip(exercises, (4.74, 4.56, 4.33, 4.00), strict=True):
        quoted(f"critical swap rate at t = {int(t)} (%)", boundary[t] * 100.0, e, 2)
    quoted("year-1 exercise margin over the strike (bp)", (boundary[1.0] - strike) * 1e4, 74.0, 0)


def example3_lsm() -> None:
    print("  3. Longstaff-Schwartz with an out-of-sample pricing set (Example 3, card fi-callable-bermudan-lsmc-bias)")
    model = LGM(0.04)
    exercises, swap_end, strike = [1.0, 2.0, 3.0, 4.0], 5.0, 0.04

    def simulate(seed: int, n: int) -> dict[float, np.ndarray]:
        rng = np.random.default_rng(seed)
        out, x, t_prev = {}, np.zeros(n), 0.0
        for t in exercises:
            x = x + math.sqrt(model.zeta(t) - model.zeta(t_prev)) * rng.standard_normal(n)
            out[t], t_prev = x.copy(), t
        return out

    def basis(t: float, x: np.ndarray) -> np.ndarray:
        s = par_swap_rate(model, t, swap_end, x)
        return np.vstack([np.ones_like(s), s, s * s]).T

    # Fit exercise rules on one set of paths ...
    train = simulate(1, 100_000)
    coefs: dict[float, np.ndarray] = {}
    cash = np.maximum(payer_value(model, exercises[-1], swap_end, strike, train[exercises[-1]]), 0.0) / model.numeraire(
        exercises[-1], train[exercises[-1]]
    )
    for t in reversed(exercises[:-1]):
        ev = np.maximum(payer_value(model, t, swap_end, strike, train[t]), 0.0) / model.numeraire(t, train[t])
        itm = ev > 0.0
        coefs[t], *_ = np.linalg.lstsq(basis(t, train[t][itm]), cash[itm], rcond=None)
        cont = basis(t, train[t][itm]) @ coefs[t]
        idx = np.where(itm)[0][ev[itm] > cont]
        cash[idx] = ev[idx]
    in_sample = float(cash.mean())
    # ... and apply them, unchanged, to independent paths: any fixed rule gives a low-biased estimate.
    test = simulate(2, 100_000)
    paid = np.zeros(100_000, dtype=bool)
    value = np.zeros(100_000)
    for t in exercises:
        ev = np.maximum(payer_value(model, t, swap_end, strike, test[t]), 0.0) / model.numeraire(t, test[t])
        if t == exercises[-1]:
            stop = ev > 0.0
        else:
            stop = (ev > 0.0) & (ev > basis(t, test[t]) @ coefs[t])
        new = stop & ~paid
        value[new] = ev[new]
        paid |= stop
    out_sample = float(value.mean())
    stderr = float(value.std()) / math.sqrt(100_000)
    quoted("LSM in-sample, seed-stable", in_sample, 0.0231, 4)
    quoted("LSM out-of-sample, seed-stable", out_sample, 0.0232, 4)
    quoted("LSM out-of-sample standard error", stderr, 0.0001, 4)
    assert out_sample < 0.023232 + 3.0 * stderr, "a fixed exercise rule cannot beat the optimal value beyond noise"


def bond_price_and_duration(coupon: float, yield_rate: float, years: int) -> tuple[float, float]:
    """Price per 100 and modified duration of an annual-pay bond at a flat annual yield."""
    price = weighted = 0.0
    for t in range(1, years + 1):
        cf = coupon + (100.0 if t == years else 0.0)
        df = (1.0 + yield_rate) ** (-t)
        price += cf * df
        weighted += t * cf * df
    return price, weighted / price / (1.0 + yield_rate)


def callable_bond_price(model: LGM, coupon: float, maturity: int, call_dates: Sequence[int]) -> float:
    """Annual coupon bond per 1 face, callable at par (after the coupon) on call_dates; the issuer calls when that lowers the value."""
    u = np.full_like(model.x, 1.0 + coupon) / model.numeraire(float(maturity), model.x)
    t_next = float(maturity)
    for t in range(maturity - 1, 0, -1):
        cont = model.convolve(u, float(t), t_next)
        if t in call_dates:
            cont = np.minimum(cont, 1.0 / model.numeraire(float(t), model.x))
        u = cont + coupon / model.numeraire(float(t), model.x)
        t_next = float(t)
    return model.value_at_zero(u, t_next)


def example4_negative_convexity() -> None:
    print("  4. Straight bond metrics, yield-to-worst, and a model-priced callable (Example 4)")
    p8, d8 = bond_price_and_duration(6.0, 0.08, 30)
    p7, _ = bond_price_and_duration(6.0, 0.07, 30)
    quoted("30y 6% price at 8%", p8, 77.48, 2)
    quoted("modified duration at 8%", d8, 11.79, 2)
    quoted("price at 7%", p7, 87.59, 2)
    quoted("gain on the 100 bp rally (%)", (p7 / p8 - 1.0) * 100.0, 13.0, 1)
    p4, _ = bond_price_and_duration(6.0, 0.04, 30)
    p4_call, d4_call = bond_price_and_duration(6.0, 0.04, 5)
    quoted("price to maturity at 4%", p4, 134.58, 2)
    quoted("price to the 5y call at 4%", p4_call, 108.90, 2)
    quoted("modified duration to the call at 4%", d4_call, 4.32, 2)

    coupon, maturity, calls = 0.05, 10, list(range(2, 10))
    expected = {
        0.03: (116.63, 102.61, 14.03, 3.10, -80.0),
        0.05: (99.02, 94.39, 4.63, 5.33, -84.0),
        0.07: (84.37, 83.28, 1.09, 6.97, -1.0),
        0.09: (72.16, 71.97, 0.20, 7.48, 48.0),
    }
    bump = 0.0025
    for level, (e_straight, e_call, e_opt, e_dur, e_conv) in expected.items():
        straight_model = sum(coupon * math.exp(-level * t) for t in range(1, maturity + 1)) + math.exp(-level * maturity)
        straight_conv = callable_bond_price(LGM(level), coupon, maturity, [])
        assert abs(straight_conv - straight_model) < 1e-6, "the convolution must reprice the straight bond off the curve"
        p0 = callable_bond_price(LGM(level), coupon, maturity, calls)
        p_up = callable_bond_price(LGM(level + bump), coupon, maturity, calls)
        p_dn = callable_bond_price(LGM(level - bump), coupon, maturity, calls)
        eff_dur = (p_dn - p_up) / (2.0 * p0 * bump)
        eff_conv = (p_up + p_dn - 2.0 * p0) / (p0 * bump * bump)
        tag = f"curve {level * 100:.0f}%"
        quoted(f"{tag}: straight bond", straight_model * 100.0, e_straight, 2)
        quoted(f"{tag}: callable bond", p0 * 100.0, e_call, 2)
        quoted(f"{tag}: issuer call option", (straight_model - p0) * 100.0, e_opt, 2)
        quoted(f"{tag}: effective duration", eff_dur, e_dur, 2)
        quoted(f"{tag}: effective convexity", eff_conv, e_conv, 0)


def example5_regression_step() -> None:
    print("  5. Toy Longstaff-Schwartz regression step (Example 5)")
    x_itm = [0.02, 0.03, 0.035]
    y_itm = [0.045, 0.038, 0.037]
    n = len(x_itm)
    mx, my = sum(x_itm) / n, sum(y_itm) / n
    sxx = sum((x - mx) ** 2 for x in x_itm)
    beta1 = sum((x - mx) * (y - my) for x, y in zip(x_itm, y_itm, strict=True)) / sxx
    beta0 = my - beta1 * mx
    quoted("slope beta1", beta1, -0.5571, 4)
    quoted("intercept beta0", beta0, 0.0558, 4)
    fitted = [beta0 + beta1 * x for x in x_itm]
    for i, (f, e) in enumerate(zip(fitted, (0.0446, 0.0391, 0.0363), strict=True), start=1):
        quoted(f"path {i} fitted continuation", f, e, 4)


def main() -> None:
    print("=== fi_callable_bermudan: Callable Bonds and Bermudan Swaptions ===")
    example1_bermudan()
    example3_lsm()
    example4_negative_convexity()
    example5_regression_step()
    print(f"\nSuccessfully verified {len(QUOTED)} callable and Bermudan figures.")


if __name__ == "__main__":
    main()
