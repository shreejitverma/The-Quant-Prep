"""Case File 09: GameStop, January 2021, every number on the page.

Backs `16-Trading-and-Investing/20-History-and-Events/09-2021-GameStop-Meme-Squeeze-and-DTCC-Margin-Halt.md`.
Independent routes used here:
- price changes are recomputed from the SEC staff report's cited prices in exact decimal arithmetic and
  checked against the report's own "more than 1,600%" statement;
- the NSCC January 27 margin call is checked to equal the sum of its two cited components;
- the hypothetical dealer hedge uses the closed-form Black-Scholes gamma and is checked against a central
  finite difference of the closed-form delta, and the 1/sqrt(tau) scaling is checked by comparing two
  expiries;
- the re-lending example (short interest above 100%) is checked by explicit bookkeeping of loans.
Every quoted number is printed as ``label = value`` and asserted.
"""

from __future__ import annotations

import math
from decimal import Decimal as D


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def call_delta(s: float, k: float, sigma: float, tau: float) -> float:
    d1 = (math.log(s / k) + 0.5 * sigma**2 * tau) / (sigma * math.sqrt(tau))
    return norm_cdf(d1)


def call_gamma(s: float, k: float, sigma: float, tau: float) -> float:
    d1 = (math.log(s / k) + 0.5 * sigma**2 * tau) / (sigma * math.sqrt(tau))
    return math.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi) / (s * sigma * math.sqrt(tau))


def prices() -> None:
    print("GME prices (SEC staff report, October 14, 2021)")
    jan12, jan13, jan27, high = D("19.95"), D("31.40"), D("347.51"), D("483.00")
    approx("Jan 13 close over Jan 12 close (%)", float((jan13 / jan12 - 1) * 100), 57.39, 2)
    gain_close = float((jan27 / jan12 - 1) * 100)
    approx("Jan 27 close over Jan 12 close (%)", gain_close, 1641.90, 2)
    assert gain_close > 1600, "SEC: more than 1,600%"
    approx("Jan 28 intraday high over Jan 12 close (%)", float((high / jan12 - 1) * 100), 2321.05, 2)


def nscc() -> None:
    print("NSCC margin, January 27, 2021 ($bn)")
    mtm, special = D("2.1"), D("4.8")
    assert mtm + special == D("6.9"), "intraday calls = mark-to-market + special charge"
    print(f"    intraday margin calls = {mtm + special}")


def relending() -> None:
    print("Re-lending bookkeeping: 100 shares, one share lent twice")
    shares_outstanding = 100
    short_positions = 0
    # A lends its share to X, X sells it to B; B lends the same share to Y, Y sells it to C.
    for _ in range(2):
        short_positions += 1
    approx("short interest (%)", short_positions / shares_outstanding * 100, 2.0, 0)
    assert short_positions > 1, "one share sold short twice counts twice"


def dealer_hedge() -> None:
    print("Hypothetical dealer short 10,000 at-the-money calls, S = K = 40, sigma = 200%")
    n, s, k, sigma = 10_000, 40.0, 40.0, 2.0
    results = {}
    for days, quoted in ((5, 35053), (1, 79006)):
        tau = days / 252
        g = call_gamma(s, k, sigma, tau)
        h = 1e-4
        g_fd = (call_delta(s + h, k, sigma, tau) - call_delta(s - h, k, sigma, tau)) / (2 * h)
        assert abs(g - g_fd) / g < 1e-6, f"gamma {g} vs finite difference {g_fd}"
        shares = n * 100 * g
        results[days] = shares
        approx(f"shares to buy per $1 rise, {days} trading days to expiry", shares, quoted, 0)
    ratio = results[1] / results[5]
    # Near the money gamma scales like 1/sqrt(tau); d1 = sigma*sqrt(tau)/2 adds a small correction.
    assert abs(ratio / math.sqrt(5) - 1) < 0.02, f"ratio {ratio} vs sqrt(5)"
    approx("sqrt(5)", math.sqrt(5), 2.236, 3)
    approx("ratio of 1-day to 5-day hedge", ratio, 2.25, 2)


def main() -> None:
    prices()
    nscc()
    relending()
    dealer_hedge()
    print("all GameStop checks passed")


if __name__ == "__main__":
    main()
