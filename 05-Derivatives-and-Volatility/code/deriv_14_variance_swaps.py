"""Variance swaps and volatility products: every number in 14-Variance-Swaps-and-Volatility-Products.md.

Independent routes used here:
- the fair variance strike as the 2/T-weighted 1/K^2 option strip (Gauss-Legendre in log-strike) and, separately,
  as Gatheral's density-free form K_var = int phi(z) w(k(z)) dz with z = -d2(k) (The Volatility Surface, ch. 11),
  which uses only the smile and never prices an option; a flat smile must return sigma^2 exactly;
- the strip's constant dollar gamma checked by integrating S^2 Gamma(K) / K^2 over strikes at several spots;
- the replication identity int sigma^2 dt = 2 int dS/S - 2 ln(S_T/S_0) checked on simulated GBM paths;
- the Cboe discretised formula (Cboe Volatility Index Mathematics Methodology, v5.0, February 2026, eq. 1)
  against the continuous strip, and its convergence order measured on four grids;
- the vol-swap convexity adjustment against the exact lognormal E[sqrt V] and a seeded simulation of it;
- notional arithmetic, forward variance and the seasoned mark with exact rationals (fractions.Fraction).
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/deriv_14_variance_swaps.py
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
from pricing_core import bs_price, norm_pdf

_X, _W = np.polynomial.legendre.leggauss(100)
SEED_ITO = 14
SEED_LOGNORMAL = 15


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"    {label} = {value:.8f}  (quoted {quoted})")
    assert abs(value - float(quoted.replace(",", ""))) <= tol, f"{label}: {value} does not round to {quoted}"
    return value


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: {value} != {expected}"
    print(f"    {label} = {value}")


def close(label: str, a: float, b: float, tol: float) -> None:
    print(f"      check {label}: |{a:.10g} - {b:.10g}| = {abs(a - b):.1e} <= {tol:.0e}")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


def gl(f, a: float, b: float, panels: int = 80) -> float:
    """Composite Gauss-Legendre on [a, b]."""
    edges = np.linspace(a, b, panels + 1)
    total = 0.0
    for lo, hi in zip(edges[:-1], edges[1:], strict=True):
        t = 0.5 * (hi - lo) * _X + 0.5 * (hi + lo)
        total += 0.5 * (hi - lo) * float(np.sum(_W * f(t)))
    return total


def svi_w(k: np.ndarray) -> np.ndarray:
    """The note's SVI total variance at T = 1: 0.03 + 0.1 (-0.7 k + sqrt(k^2 + 0.01))."""
    return 0.03 + 0.1 * (-0.7 * k + np.sqrt(k * k + 0.01))


def strip(F: float, T: float, r: float, vol, k_lo: float = -8.0, k_hi: float = 8.0) -> tuple[float, float]:
    """(2 e^{rT} / T) x [int P / K^2 over K < F, int C / K^2 over K > F], in log-strike k = ln(K / F)."""
    S = F * math.exp(-r * T)
    put = lambda k: bs_price(S, F * np.exp(k), T, r, vol(F * np.exp(k)), call=False) * np.exp(-k) / F  # noqa: E731
    call = lambda k: bs_price(S, F * np.exp(k), T, r, vol(F * np.exp(k))) * np.exp(-k) / F  # noqa: E731
    c = 2 * math.exp(r * T) / T
    return c * gl(put, k_lo, 0.0), c * gl(call, 0.0, k_hi)


def gatheral_kvar(w, T: float) -> float:
    """K_var = (1/T) int phi(z) w(k(z)) dz, where z = -d2(k) = k / sqrt(w) + sqrt(w) / 2 is solved for k by bisection."""

    def k_of_z(z: np.ndarray) -> np.ndarray:
        lo, hi = np.full_like(z, -30.0), np.full_like(z, 30.0)
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            sw = np.sqrt(w(mid))
            above = mid / sw + 0.5 * sw > z  # -d2 is increasing in k
            hi, lo = np.where(above, mid, hi), np.where(above, lo, mid)
        return 0.5 * (lo + hi)

    return gl(lambda z: norm_pdf(z) * w(k_of_z(z)), -10.0, 10.0) / T


def vix_style(dk: float, S: float, r: float, T: float, smile, lo: float = 60.0, hi: float = 140.0) -> float:
    """Cboe single-term variance (eq. 1): OTM quotes, K0 the first strike at or below F, Q(K0) the put-call average,
    Delta K half the gap to the neighbours and one-sided at the ends."""
    F = S * math.exp(r * T)
    K = np.arange(lo, hi + dk / 2, dk)
    K0 = K[K <= F].max()
    Q = np.where(K < K0, bs_price(S, K, T, r, smile(K), call=False), bs_price(S, K, T, r, smile(K)))
    Q[K == K0] = 0.5 * (bs_price(S, K0, T, r, smile(K0), call=False) + bs_price(S, K0, T, r, smile(K0)))
    dK = np.empty_like(K)
    dK[1:-1] = 0.5 * (K[2:] - K[:-2])
    dK[0], dK[-1] = K[1] - K[0], K[-1] - K[-2]
    return 2 / T * float(np.sum(dK / K**2 * math.exp(r * T) * Q)) - (F / K0 - 1) ** 2 / T


def main() -> None:
    print("Example 1: variance against vol swap P&L, vega notional 100,000 at 20 vol")
    n_var = Fraction(100_000, 2 * 20)
    exact("N_var = N_vega / (2 K_vol)", n_var, Fraction(2500))
    for vol, var_pnl, vol_pnl in ((25, 562_500, 500_000), (15, -437_500, -500_000), (10, -750_000, -1_000_000), (40, 3_000_000, 2_000_000)):
        exact(f"realized {vol}: variance swap P&L", n_var * (vol**2 - 400), var_pnl)
        exact(f"realized {vol}: vol swap P&L", 100_000 * (vol - 20), vol_pnl)
    exact("convexity at 25: 562,500 - 500,000", 562_500 - 500_000, 62_500)
    n_card = Fraction(50_000, 2 * 25)
    exact("card deriv-varswap-vega-to-variance-notional: N_var", n_card, Fraction(1000))
    exact("card: variance swap P&L at 30", n_card * (30**2 - 25**2), Fraction(275_000))
    exact("card: vol swap P&L at 30", 50_000 * (30 - 25), 250_000)
    exact("card: convexity", 275_000 - 250_000, 25_000)
    exact("Cboe minutes in a 365-day year", 365 * 1440, 525_600)

    print("Example 2: seasoned swap and forward variance")
    mark = Fraction(1, 4) * 625 + Fraction(3, 4) * 484
    exact("expected final variance", mark, Fraction(51925, 100))
    exact("per variance point, 519.25 - 400", mark - 400, Fraction(11925, 100))
    exact("mark 2,500 x 119.25", n_var * (mark - 400), Fraction(298125))
    fwd = (Fraction(1, 2) * 400 - Fraction(1, 4) * 324) / Fraction(1, 4)
    exact("3m-6m forward variance", fwd, Fraction(476))
    q("forward vol", math.sqrt(476), "21.8")

    print(f"Replication identity on simulated paths (seed {SEED_ITO}, 2,000 paths, 10,000 steps, sigma 20%)")
    rng = np.random.default_rng(SEED_ITO)
    n_steps, sig = 10_000, 0.2
    dt = 1.0 / n_steps
    logret = (0.05 - 0.5 * sig**2) * dt + sig * math.sqrt(dt) * rng.standard_normal((2_000, n_steps))
    lhs = np.sum(logret**2, axis=1)  # realized variance of one year, divisor-free
    rhs = 2 * np.sum(np.expm1(logret), axis=1) - 2 * np.sum(logret, axis=1)  # 2 sum dS/S - 2 ln(S_T / S_0)
    print(f"    max |sum ln^2 - (2 sum dS/S - 2 ln S_T/S_0)| across paths = {np.max(np.abs(lhs - rhs)):.2e}")
    assert np.max(np.abs(lhs - rhs)) < 2e-4

    print("Constant dollar gamma of the 1/K^2 strip (flat 20%, one year, r = 0)")
    for spot in (60.0, 100.0, 150.0):

        def dollar_gamma_density(k: np.ndarray, s: float = spot, power: int = 2) -> np.ndarray:
            """S^2 Gamma(K) / K^power x dK/dk, with K = e^k and d1 = (ln(S/K) + sigma^2 T / 2) / sigma."""
            gamma = norm_pdf((math.log(s) - k + 0.02) / 0.2) / (s * 0.2)
            return s * s * gamma / np.exp(k) ** power * np.exp(k)

        lo, hi = math.log(spot) - 3.0, math.log(spot) + 3.0
        close(f"int S^2 Gamma(K) / K^2 dK at S = {spot:.0f} equals e^(-rT) = 1", gl(dollar_gamma_density, lo, hi), 1.0, 1e-9)
        gamma_swap = gl(lambda k, s=spot: dollar_gamma_density(k, s, 1), lo, hi)
        close(f"a 1/K strip (gamma swap) has dollar gamma S at S = {spot:.0f}", gamma_swap, spot, 1e-6)

    print("Example 3: pricing the strip, one year, F = 100, r = 0")
    put, call = strip(100.0, 1.0, 0.0, lambda K: 0.2 + 0 * K)
    q("flat 20% smile: K_var", put + call, "0.0400")
    svi_vol = lambda K: np.sqrt(svi_w(np.log(K / 100.0)))  # noqa: E731
    for m, quoted in ((1.0, "20.0"), (0.9, "22.8"), (0.8, "26.5"), (1.1, "19.3")):
        q(f"SVI vol at {100 * m:.0f}% strike (%)", 100 * float(svi_vol(np.array(100 * m))), quoted)
    K = np.linspace(20, 400, 38_001)
    density = np.diff(bs_price(100.0, K, 1.0, 0.0, svi_vol(K)), 2)
    assert density.min() > -1e-12, "SVI smile has negative butterflies"
    print("    no butterfly arbitrage on 20-400: every discrete second difference of call prices is non-negative")
    put, call = strip(100.0, 1.0, 0.0, svi_vol)
    kvar = q("K_var by the strip", put + call, "0.06273")
    close("K_var by Gatheral's z-integral (no option prices)", gatheral_kvar(svi_w, 1.0), kvar, 1e-9)
    q("variance strike in vol", 100 * math.sqrt(kvar), "25.05")
    q("gap over ATM (vol points)", 100 * math.sqrt(kvar) - 20, "5")
    q("puts", put, "0.0444")
    q("calls", call, "0.0183")
    q("share from puts (%)", 100 * put / kvar, "71")
    for lo, hi, quoted in ((50, 150, "23.9"), (70, 130, "21.7")):
        p, c = strip(100.0, 1.0, 0.0, svi_vol, math.log(lo / 100), math.log(hi / 100))
        q(f"strip truncated to {lo}-{hi}, vol", 100 * math.sqrt(p + c), quoted)

    print("Example 4: a VIX-style calculation, 30 days, S = 100, r = 3%")
    S, r, T = 100.0, 0.03, 30 / 365
    F = q("forward", S * math.exp(r * T), "100.247")
    p, c = strip(F, T, r, svi_vol, -6.0, 6.0)
    cont = q("continuous strip, vol", 100 * math.sqrt(p + c), "20.42")
    q("ATM-forward vol", 100 * float(svi_vol(np.array(F))), "19.96")
    errs = {}
    for dk, quoted in ((5.0, "21.63"), (2.5, "20.73"), (1.0, "20.47"), (0.25, "20.42")):
        v = q(f"discrete formula, spacing {dk}", 100 * math.sqrt(vix_style(dk, S, r, T, svi_vol)), quoted)
        errs[dk] = v - cont
    q("error ratio, spacing 5 against 2.5", errs[5.0] / errs[2.5], "3.9")
    q("error ratio, spacing 2.5 against 1", errs[2.5] / errs[1.0], "6.2")
    q("(2.5 / 1)^2, the second-order prediction", 6.25, "6.25")
    q("30-day standard deviation, 20% sqrt(30/365) (points)", 20 * math.sqrt(T), "5.7")

    print("Example 5: a 20% jump against a strip-hedged short")
    lj = math.log(0.8)
    q("ln(0.8)", lj, "-0.2231")
    q("ln^2(0.8)", lj**2, "0.04979")
    q("realized variance points", 1e4 * lj**2, "498")
    q("2(J - ln(1 + J))", 2 * (-0.2 - lj), "0.04629")
    q("replicated variance points", 1e4 * 2 * (-0.2 - lj), "463")
    gap = q("shortfall (variance points)", 1e4 * (lj**2 - 2 * (-0.2 - lj)), "35.06")
    q("shortfall, two figures", gap, "35")
    q("cost 2,500 x 35.06", 2500 * 35.06, "87650")
    close("cost from the unrounded shortfall", 2500 * gap, 87650, 5)
    lu = math.log(1.2)
    q("+20%: realized points", 1e4 * lu**2, "332")
    q("+20%: replicated points", 1e4 * 2 * (0.2 - lu), "354")
    for j in (0.01, -0.01, 0.001):
        lnj = math.log1p(j)
        close(f"(ln^2(1+J) - 2(J - ln(1+J))) / (-J^3/3) at J = {j}", (lnj**2 - 2 * (j - lnj)) / (-(j**3) / 3), 1.0, 0.02)

    print("Example 6: vol swap convexity, K_var = 400, sd(V) = 150")
    adj = q("150^2 / (8 x 400^1.5)", 150**2 / (8 * 400**1.5), "0.35")
    exact("400^1.5 x 8", 8 * 400**1.5, 64000.0)
    q("approximate vol strike", 20 - adj, "19.65")
    s2 = math.log(1 + (150 / 400) ** 2)
    e_sqrt = q("exact lognormal E[sqrt V]", 20 * math.exp(-s2 / 8), "19.67")
    q("exact lognormal E[sqrt V], three decimals", e_sqrt, "19.674")
    q("approximate vol strike, three decimals", 20 - adj, "19.648")
    q("approximation error", e_sqrt - (20 - adj), "0.03")
    rng = np.random.default_rng(SEED_LOGNORMAL)
    v = np.exp(math.log(400) - s2 / 2 + math.sqrt(s2) * rng.standard_normal(1_000_000))
    se = float(np.sqrt(v).std(ddof=1)) / 1000
    close("simulated E[sqrt V] within 4 standard errors", float(np.sqrt(v).mean()), e_sqrt, 4 * se)
    close("simulated sd(V) near 150", float(v.std(ddof=1)), 150.0, 1.5)

    print("Example 7: realized variance of five closes")
    closes = np.array([100, 101, 99.5, 100.2, 98.9, 100.4])
    lr = np.diff(np.log(closes))
    for got, quoted in zip(100 * lr, ("0.995", "-1.496", "0.701", "-1.306", "1.505"), strict=True):
        q("log return (%)", float(got), quoted)
    rv = q("contract variance points", 252 / 5 * float(np.sum(lr**2)) * 1e4, "387.7")
    q("contract vol", math.sqrt(rv), "19.69")
    q("contract vol, card", math.sqrt(rv), "19.7")
    sample = 100 * float(lr.std(ddof=1)) * math.sqrt(252)
    q("sample standard deviation vol", sample, "21.97")
    q("sample standard deviation vol, card", sample, "22.0")
    q("difference (vol points)", sample - math.sqrt(rv), "2")
    print("All variance swap checks passed.")


if __name__ == "__main__":
    main()
