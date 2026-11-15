"""Case File 02: 1987 Black Monday, every number on the page.

Backs `16-Trading-and-Investing/20-History-and-Events/02-1987-Black-Monday-and-Portfolio-Insurance.md`.
Independent routes used here:
- index moves are recomputed from the cited closes in exact decimal arithmetic and checked against the
  cited point change and the Brady Report's rounded figures (22.6 percent, 30.6 percent);
- the portfolio-insurance overhang (20 percent of $60 billion) is checked against the Brady Report's
  statement that less than $4 billion had been sold;
- the hypothetical put deltas use the closed form N(d1) - 1 (math.erf) and are checked against a central
  finite difference of a put price obtained by trapezoidal integration of the payoff over the lognormal
  density, a route that never evaluates N(d1).
Every quoted number is printed as ``label = value`` and asserted.
"""

from __future__ import annotations

import math
from decimal import Decimal as D

import numpy as np


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def put_delta_closed_form(s: float, k: float, sigma: float, t: float, r: float = 0.0) -> float:
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
    return norm_cdf(d1) - 1.0


def put_price_by_quadrature(s: float, k: float, sigma: float, t: float, r: float = 0.0) -> float:
    """E[e^{-rT} max(K - S_T, 0)] with log S_T normal, integrated on a fine grid in z."""
    z = np.linspace(-12.0, 12.0, 400_001)
    density = np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
    s_t = s * np.exp((r - 0.5 * sigma**2) * t + sigma * math.sqrt(t) * z)
    payoff = np.maximum(k - s_t, 0.0)
    return math.exp(-r * t) * float(np.trapezoid(payoff * density, z))


def index_moves() -> None:
    print("Index moves (cited closes)")
    prev, close = D("2246.74"), D("1738.74")
    assert prev - close == D("508.00"), "cited 508-point fall must equal the close difference"
    print(f"    Oct 19 point fall = {prev - close}")
    fall = float((prev - close) / prev * 100)
    approx("Oct 19 Dow fall (%)", fall, 22.61, 2)
    approx("Oct 19 Dow fall, Brady rounding (%)", fall, 22.6, 1)
    week = float((D("2505") - D("1738")) / D("2505") * 100)
    approx("Oct 13 to Oct 19 fall (%)", week, 30.62, 2)
    approx("Oct 13 to Oct 19 fall, Brady Study III (%)", week, 30.6, 1)


def overhang() -> None:
    print("Portfolio insurance overhang (Brady Report)")
    dictated = 0.20 * 60.0
    approx("sales dictated by a 10% fall ($bn)", dictated, 12.0, 0)
    assert dictated > 4.0, "Brady: less than $4 billion had in fact been sold"


def deltas() -> None:
    print("Hypothetical put: K = 95, sigma = 20%, T = 0.5, r = 0")
    k, sigma, t = 95.0, 0.20, 0.5
    for s, quoted in ((100.0, -0.3324), (90.0, -0.6223)):
        closed = put_delta_closed_form(s, k, sigma, t)
        h = 0.01
        numeric = (put_price_by_quadrature(s + h, k, sigma, t) - put_price_by_quadrature(s - h, k, sigma, t)) / (2 * h)
        assert abs(closed - numeric) < 1e-5, f"closed form {closed} vs quadrature {numeric}"
        approx(f"put delta at S = {s:g}", closed, quoted, 4)
        approx(f"put delta at S = {s:g} (quadrature)", numeric, quoted, 4)
    approx("hedge at S0 (% of portfolio)", -put_delta_closed_form(100.0, k, sigma, t) * 100, 33.24, 2)
    approx("hedge at S1 (% of portfolio)", -put_delta_closed_form(90.0, k, sigma, t) * 100, 62.23, 2)
    ratio = put_delta_closed_form(90.0, k, sigma, t) / put_delta_closed_form(100.0, k, sigma, t)
    assert 1.8 < ratio < 2.0, f"'close to double': ratio {ratio}"
    print(f"    hedge ratio S1/S0 = {ratio:.3f}")


def main() -> None:
    index_moves()
    overhang()
    deltas()
    print("all 1987 checks passed")


if __name__ == "__main__":
    main()
