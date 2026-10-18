"""Counterparty exposure profiles: EE, ENE, PFE, EPE, Effective EE and Effective EPE by Monte Carlo, with netting and
collateral (margin period of risk), checked against closed forms.

Backs every number in 11-Risk-and-Trading/14-Counterparty-Credit-Risk-Analytics.md; risk_xva_pricing.py and risk_problem_set.py
import the simulation from here.

Models (labelled illustrative inputs, not market data):
- Forward on a lognormal asset: closed-form EE and PFE, so the Monte Carlo can be checked exactly.
- Interest rate swaps under a one-factor Hull-White model fitted to an upward-sloping zero curve
  z(t) = 2% + 1.5% (1 - exp(-t / 3)) (continuously compounded), mean reversion 5% and short-rate volatility 1%.
  Bond prices are exact functions of the state, the state and the integral of the short rate are simulated exactly
  on the grid, and the discounted EE of a swap at each reset date is checked against the price of the corresponding
  European swaption from Jamshidian's decomposition.
- Collateral: variation margin with a margin period of risk (MPOR) delta, so the collateral held at t is the value
  at t - delta (Gregory, The xVA Challenge, 4th edition, chapter on collateral).
Regulatory quantities follow CRE53.12 to CRE53.14 (Effective EE, Effective EPE, alpha) and CRE52 (SA-CCR).
Simulations use fixed seeds; the note quotes them as "about".

Run: python 11-Risk-and-Trading/code/risk_ccr_analytics.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

SQRT2 = math.sqrt(2.0)


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a value and assert it matches the literal quoted in the note to within tol (absolute)."""
    print(f"  {label}: {value:.10g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, note quotes {expected} (tol {tol})"
    return value


def ncdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def ninv(p: float) -> float:
    """Inverse standard normal CDF by bisection on ncdf (accurate to about 1e-13)."""
    lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if ncdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Hull-White one-factor model fitted to today's zero curve
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HullWhite:
    z_short: float = 0.02  # zero rate at t = 0, continuously compounded
    z_slope: float = 0.015  # z(t) = z_short + z_slope (1 - exp(-t / z_scale))
    z_scale: float = 3.0
    a: float = 0.05  # mean reversion
    sigma: float = 0.01  # short-rate volatility (100bp a year, normal)

    def p0(self, t: float | np.ndarray) -> float | np.ndarray:
        if isinstance(t, np.ndarray):
            return np.exp(-(self.z_short + self.z_slope * (1.0 - np.exp(-t / self.z_scale))) * t)
        return math.exp(-(self.z_short + self.z_slope * (1.0 - math.exp(-t / self.z_scale))) * t)

    def b(self, t: float, big_t: float) -> float:
        return (1.0 - math.exp(-self.a * (big_t - t))) / self.a

    def var_x(self, t: float) -> float:
        return self.sigma**2 * (1.0 - math.exp(-2.0 * self.a * t)) / (2.0 * self.a)

    def var_int(self, t: float) -> float:
        """Variance of the integral of x over [0, t]."""
        a, s = self.a, self.sigma
        return s * s / (a * a) * (t - 2.0 * (1.0 - math.exp(-a * t)) / a + (1.0 - math.exp(-2.0 * a * t)) / (2.0 * a))

    def zcb(self, t: float, big_t: float, x: np.ndarray) -> np.ndarray:
        """P(t, T) given the state x_t = r_t - alpha(t) (Brigo and Mercurio, Interest Rate Models, chapter 3)."""
        a, s = self.a, self.sigma
        bb = self.b(t, big_t)
        conv = s * s / (4.0 * a) * (1.0 - math.exp(-2.0 * a * t)) * bb * bb + bb * s * s / (2.0 * a * a) * (1.0 - math.exp(-a * t)) ** 2
        return (self.p0(big_t) / self.p0(t)) * np.exp(-bb * x - conv)

    def simulate(self, grid: np.ndarray, n_paths: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
        """Exact joint simulation of (x_t, integral of x) on the grid.  Returns states x[k, path] and stochastic
        discount factors D[k, path] = exp(-integral of r over [0, t_k]) = P(0, t_k) exp(-V(t_k)/2 - I_k)."""
        a, s = self.a, self.sigma
        rng = np.random.default_rng(seed)
        x = np.zeros((len(grid), n_paths))
        integ = np.zeros(n_paths)
        disc = np.ones((len(grid), n_paths))
        for k in range(1, len(grid)):
            h = grid[k] - grid[k - 1]
            e = math.exp(-a * h)
            bh = (1.0 - e) / a
            v1 = s * s * (1.0 - e * e) / (2.0 * a)
            v2 = s * s / (a * a) * (h - 2.0 * bh + (1.0 - e * e) / (2.0 * a))
            c12 = s * s / (2.0 * a * a) * (1.0 - e) ** 2
            l11 = math.sqrt(v1)
            l21 = c12 / l11
            l22 = math.sqrt(v2 - l21 * l21)
            z1 = rng.standard_normal(n_paths)
            z2 = rng.standard_normal(n_paths)
            integ = integ + x[k - 1] * bh + l21 * z1 + l22 * z2
            x[k] = x[k - 1] * e + l11 * z1
            disc[k] = self.p0(grid[k]) * np.exp(-0.5 * self.var_int(grid[k]) - integ)
        return x, disc

    def zbp(self, t: float, big_t: float, strike: float) -> float:
        """Price today of a European put expiring at t on the zero-coupon bond maturing at T."""
        sp = self.sigma * self.b(t, big_t) * math.sqrt((1.0 - math.exp(-2.0 * self.a * t)) / (2.0 * self.a))
        h = math.log(self.p0(big_t) / (self.p0(t) * strike)) / sp + 0.5 * sp
        return strike * self.p0(t) * ncdf(-h + sp) - self.p0(big_t) * ncdf(-h)

    def zbc(self, t: float, big_t: float, strike: float) -> float:
        sp = self.sigma * self.b(t, big_t) * math.sqrt((1.0 - math.exp(-2.0 * self.a * t)) / (2.0 * self.a))
        h = math.log(self.p0(big_t) / (self.p0(t) * strike)) / sp + 0.5 * sp
        return self.p0(big_t) * ncdf(h) - strike * self.p0(t) * ncdf(h - sp)


@dataclass(frozen=True)
class Swap:
    notional: float
    fixed: float
    pay_dates: tuple[float, ...]  # fixed and floating payments on the same dates, accrual tau between them
    payer: bool = True  # pay fixed, receive floating

    @property
    def maturity(self) -> float:
        return self.pay_dates[-1]

    def value_at_reset(self, hw: HullWhite, t: float, x: np.ndarray) -> np.ndarray:
        """Value at a reset date t just after that date's exchange: the floating leg is worth par."""
        rem = [d for d in self.pay_dates if d > t + 1e-12]
        if not rem:
            return np.zeros_like(x)
        prev = t
        fixed_leg = np.zeros_like(x)
        for d in rem:
            fixed_leg = fixed_leg + self.fixed * (d - prev) * hw.zcb(t, d, x)
            prev = d
        v = self.notional * (1.0 - hw.zcb(t, rem[-1], x) - fixed_leg)
        return v if self.payer else -v

    def swaption_today(self, hw: HullWhite, t: float) -> float:
        """Jamshidian: E[D(t) max(V(t), 0)] as a portfolio of zero-coupon bond options (puts for a payer)."""
        rem = [d for d in self.pay_dates if d > t + 1e-12]
        if not rem or t <= 0.0:
            return 0.0
        prev = t
        coupons = []
        for d in rem:
            coupons.append(self.fixed * (d - prev))
            prev = d
        coupons[-1] += 1.0

        def bond(xs: float) -> float:
            return sum(c * float(hw.zcb(t, d, np.array([xs]))[0]) for c, d in zip(coupons, rem, strict=True))

        lo, hi = -1.0, 1.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if bond(mid) > 1.0:
                lo = mid
            else:
                hi = mid
        xs = 0.5 * (lo + hi)
        price = 0.0
        for c, d in zip(coupons, rem, strict=True):
            k = float(hw.zcb(t, d, np.array([xs]))[0])
            price += c * (hw.zbp(t, d, k) if self.payer else hw.zbc(t, d, k))
        return self.notional * price


def par_rate(hw: HullWhite, dates: tuple[float, ...]) -> float:
    prev, ann = 0.0, 0.0
    for d in dates:
        ann += (d - prev) * float(hw.p0(d))
        prev = d
    return (1.0 - float(hw.p0(dates[-1]))) / ann


def quarterly(maturity: float) -> tuple[float, ...]:
    return tuple(0.25 * i for i in range(1, int(round(maturity * 4)) + 1))


@dataclass
class Profile:
    grid: np.ndarray
    ee: np.ndarray  # E[max(V, 0)], undiscounted, risk-neutral
    dee: np.ndarray  # E[D max(V, 0)], discounted
    dene: np.ndarray  # E[D max(-V, 0)]
    pfe95: np.ndarray
    values: np.ndarray  # V[k, path]


def profile(values: np.ndarray, disc: np.ndarray, grid: np.ndarray) -> Profile:
    pos = np.maximum(values, 0.0)
    return Profile(
        grid=grid,
        ee=pos.mean(axis=1),
        dee=(disc * pos).mean(axis=1),
        dene=(disc * np.maximum(-values, 0.0)).mean(axis=1),
        pfe95=np.quantile(pos, 0.95, axis=1),
        values=values,
    )


def effective_ee(ee: np.ndarray, current_exposure: float) -> np.ndarray:
    """CRE53.12: Effective EE_tk = max(Effective EE_tk-1, EE_tk), with Effective EE_t0 = current exposure."""
    out = np.empty_like(ee)
    out[0] = current_exposure
    for k in range(1, len(ee)):
        out[k] = max(out[k - 1], ee[k])
    return out


def effective_epe(grid: np.ndarray, eee: np.ndarray, maturity: float) -> float:
    """CRE53.13: sum over t_k up to min(1 year, maturity) of Effective EE_tk x (t_k - t_k-1), divided by that horizon."""
    horizon = min(1.0, maturity)
    total = 0.0
    for k in range(1, len(grid)):
        if grid[k] > horizon + 1e-12:
            break
        total += eee[k] * (grid[k] - grid[k - 1])
    return total / horizon


def time_average(grid: np.ndarray, prof: np.ndarray) -> float:
    return float(np.sum(0.5 * (prof[1:] + prof[:-1]) * np.diff(grid)) / (grid[-1] - grid[0]))


HW = HullWhite()
GRID = np.array([0.25 * k for k in range(21)])
N_PATHS = 50_000
SEED = 20261018


def swap_book(hw: HullWhite = HW) -> tuple[Swap, Swap]:
    k5 = par_rate(hw, quarterly(5.0))
    k2 = par_rate(hw, quarterly(2.0))
    payer5 = Swap(10e6, k5, quarterly(5.0), payer=True)
    receiver2 = Swap(10e6, k2, quarterly(2.0), payer=False)
    return payer5, receiver2


def simulate_book(hw: HullWhite = HW, n_paths: int = N_PATHS, seed: int = SEED) -> dict[str, np.ndarray]:
    x, disc = hw.simulate(GRID, n_paths, seed)
    payer5, receiver2 = swap_book(hw)
    v5 = np.array([payer5.value_at_reset(hw, t, x[k]) for k, t in enumerate(GRID)])
    v2 = np.array([receiver2.value_at_reset(hw, t, x[k]) for k, t in enumerate(GRID)])
    return {"x": x, "disc": disc, "v5": v5, "v2": v2}


# ---------------------------------------------------------------------------
# Core concepts "Exposure of a forward": closed form against Monte Carlo (cards risk-forward-ee-closed-form,
# risk-potential-future-exposure-definition, risk-swap-vs-forward-exposure-geometry)
# ---------------------------------------------------------------------------


def forward_ee_closed(t: float, n: float, s0: float, vol: float, r: float) -> float:
    """EE of a par forward V(t) = N (S_t / S0 - e^{rt}): N e^{rt} (2 Phi(sigma sqrt(t) / 2) - 1)."""
    return n * math.exp(r * t) * (2.0 * ncdf(0.5 * vol * math.sqrt(t)) - 1.0)


def forward_pfe_closed(t: float, n: float, vol: float, r: float, q: float) -> float:
    """q-quantile of max(V, 0) when P(V <= 0) < q: N e^{rt} (exp(-sigma^2 t / 2 + sigma sqrt(t) z_q) - 1)."""
    return n * math.exp(r * t) * (math.exp(-0.5 * vol * vol * t + vol * math.sqrt(t) * ninv(q)) - 1.0)


def section_forward() -> None:
    print("\n[Par forward, N = 1m, sigma = 20%, r = 3%: EE and PFE closed form against 200,000 paths]")
    n, s0, vol, r = 1e6, 100.0, 0.20, 0.03
    rng = np.random.default_rng(7)
    out = {}
    for t in (1.0, 5.0):
        st = s0 * np.exp((r - 0.5 * vol * vol) * t + vol * math.sqrt(t) * rng.standard_normal(200_000))
        v = n * (st / s0 - math.exp(r * t))
        pos = np.maximum(v, 0.0)
        out[t] = (pos.mean(), np.quantile(pos, 0.95), pos.std(ddof=1) / math.sqrt(len(pos)))
        print(f"  t = {t}: MC EE {out[t][0]:,.0f} (se {out[t][2]:,.0f}), PFE95 {out[t][1]:,.0f}")
    check("EE(1) closed form", forward_ee_closed(1.0, n, s0, vol, r), 82_082, 1.0)
    check("EE(5) closed form", forward_ee_closed(5.0, n, s0, vol, r), 205_571, 1.0)
    check("PFE95(1) closed form", forward_pfe_closed(1.0, n, vol, r, 0.95), 373_048, 1.0)
    check("PFE95(5) closed form", forward_pfe_closed(5.0, n, vol, r, 0.95), 1_031_891, 1.0)
    for t in (1.0, 5.0):
        assert abs(out[t][0] - forward_ee_closed(t, n, s0, vol, r)) < 3 * out[t][2], f"forward EE({t}) Monte Carlo off"
    check("MC PFE95(5) relative to closed form", out[5.0][1] / forward_pfe_closed(5.0, n, vol, r, 0.95), 1.0, 0.01)
    ratio = forward_ee_closed(5.0, n, s0, vol, r) / forward_ee_closed(1.0, n, s0, vol, r)
    check("EE(5) / EE(1), close to sqrt(5) = 2.236", ratio, 2.5045, 5e-4)


# ---------------------------------------------------------------------------
# Worked example 2: swap exposure profile, regulatory metrics (cards risk-swap-exposure-hump-shape, risk-effective-epe-basel-rationale,
# risk-swap-ee-equals-swaption, risk-imm-vs-saccr-ead)
# ---------------------------------------------------------------------------


def section_swap_profile() -> None:
    print("\n[Hull-White checks: martingale test and par rates]")
    payer5, receiver2 = swap_book()
    check("5y quarterly par rate", payer5.fixed, 0.032091, 5e-7)
    check("2y quarterly par rate", receiver2.fixed, 0.027337, 5e-7)
    sim = simulate_book()
    x, disc = sim["x"], sim["disc"]
    k = 12  # t = 3
    mart = float((disc[k] * HW.zcb(3.0, 5.0, x[k])).mean()) / float(HW.p0(5.0))
    check("E[D(3) P(3, 5)] / P(0, 5)", mart, 1.0, 2e-3)
    check("E[D(5)] / P(0, 5)", float(disc[20].mean()) / float(HW.p0(5.0)), 1.0, 2e-3)

    print("\n[Worked example 2: 10m 5y payer swap, quarterly, Hull-White, 50,000 paths]")
    prof = profile(sim["v5"], disc, GRID)
    closed = np.array([payer5.swaption_today(HW, t) for t in GRID])
    se = (disc * np.maximum(sim["v5"], 0.0)).std(axis=1, ddof=1) / math.sqrt(N_PATHS)
    print("  t | EE (undiscounted) | discounted EE MC | swaption closed form | PFE95")
    for kk in (2, 4, 6, 8, 10, 12, 16, 19):
        print(f"  {GRID[kk]:.2f} | {prof.ee[kk]:,.0f} | {prof.dee[kk]:,.0f} | {closed[kk]:,.0f} | {prof.pfe95[kk]:,.0f}")
        assert abs(prof.dee[kk] - closed[kk]) < 3.5 * se[kk], f"discounted EE at {GRID[kk]} off the Jamshidian price"
    check("Jamshidian discounted EE at 1y", closed[4], 171_439, 1.0)
    check("Jamshidian discounted EE at 2y", closed[8], 186_310, 1.0)
    for kk, exp_c in ((2, 129_704), (6, 187_394), (12, 149_934), (16, 84_065), (19, 22_317)):
        check(f"Jamshidian discounted EE at {GRID[kk]}y", closed[kk], exp_c, 1.0)
    for kk, exp_p in ((2, 471_600), (4, 617_000), (8, 669_600), (12, 566_000), (16, 337_700)):
        check(f"PFE95 at {GRID[kk]}y, MC (about)", prof.pfe95[kk], exp_p, 1_500)
    check("peak undiscounted EE, MC (about)", float(prof.ee.max()), 199_300, 400)
    check("time of the peak undiscounted EE, MC", GRID[int(np.argmax(prof.ee))], 1.75, 0.0)
    tt = np.linspace(0.0, 5.0, 50_001)
    check("peak of the shape sqrt(t) (T - t), numerically", float(tt[np.argmax(np.sqrt(tt) * (5.0 - tt))]), 1.6667, 1e-4)
    peak = int(np.argmax(closed))
    check("peak of discounted EE (closed form), years", GRID[peak], 1.75, 0.0)
    check("peak discounted EE (closed form)", closed[peak], 188_641, 1.0)
    check("EE(1) undiscounted, MC (about)", prof.ee[4], 176_300, 300)
    check("PFE95 at 1.75y, MC (about)", prof.pfe95[7], 676_800, 1_000)
    check("max PFE95 over the life, MC (about)", float(prof.pfe95.max()), 676_800, 1_000)
    eee = effective_ee(prof.ee, 0.0)
    eepe = effective_epe(GRID, eee, 5.0)
    epe = time_average(GRID, prof.ee)
    check("EPE over 5 years (about)", epe, 136_800, 300)
    check("Effective EPE, first year (about)", eepe, 139_300, 300)
    check("IMM-style EAD = 1.4 x Effective EPE (about)", 1.4 * eepe, 195_000, 400)
    # SA-CCR on the same trade at inception (CRE52): RC = 0, multiplier 1, supervisory duration over 5 years
    sd = (1.0 - math.exp(-0.05 * 5.0)) / 0.05
    addon = 0.005 * 10e6 * sd
    check("SA-CCR supervisory duration, 5y", sd, 4.4240, 5e-5)
    check("SA-CCR add-on", addon, 221_199, 1.0)
    check("SA-CCR EAD = 1.4 x add-on", 1.4 * addon, 309_679, 1.0)
    check("SA-CCR EAD / IMM-style EAD (about)", 1.4 * addon / (1.4 * eepe), 1.59, 0.01)

    print("\n[Netting: add a 10m 2y receiver swap to the same netting set]")
    net = sim["v5"] + sim["v2"]
    pn = profile(net, disc, GRID)
    p2 = profile(sim["v2"], disc, GRID)
    gross = prof.ee + p2.ee
    check("EE(1) netted (about)", pn.ee[4], 121_500, 300)
    check("EE(1) sum of trade EEs (about)", gross[4], 200_200, 400)
    check("expected net-to-gross at 1y (about)", pn.ee[4] / gross[4], 0.607, 0.002)
    check("Effective EPE netted (about)", effective_epe(GRID, effective_ee(pn.ee, 0.0), 5.0), 87_900, 300)
    check("EE netted at 3y equals the 5y swap alone (2y swap has matured)", pn.ee[12] - prof.ee[12], 0.0, 1e-9)


# ---------------------------------------------------------------------------
# Worked example 3: collateral and the margin period of risk (cards risk-margin-period-of-risk-mpor, risk-collateralised-ee-sqrt-mpor,
# risk-threshold-effect-on-exposure)
# ---------------------------------------------------------------------------


def collateralised_ee_closed(n: float, vol: float, mpor_years: float) -> float:
    """r = 0, V(t) = N (S_t / S0 - 1), collateral = V(t - delta): EE = N (2 Phi(sigma sqrt(delta) / 2) - 1) for t >= delta."""
    return n * (2.0 * ncdf(0.5 * vol * math.sqrt(mpor_years)) - 1.0)


def section_collateral() -> None:
    print("\n[Worked example 3: forward, N = 1m, sigma = 20%, r = 0, exposure at 1 year with variation margin]")
    n, vol, t = 1e6, 0.20, 1.0
    rng = np.random.default_rng(99)
    m = 400_000
    unc = collateralised_ee_closed(n, vol, t)
    check("uncollateralised EE(1)", unc, 79_656, 1.0)
    res = {}
    for days in (10, 20):
        d = days / 250.0
        s_lag = 100.0 * np.exp(-0.5 * vol * vol * (t - d) + vol * math.sqrt(t - d) * rng.standard_normal(m))
        s_t = s_lag * np.exp(-0.5 * vol * vol * d + vol * math.sqrt(d) * rng.standard_normal(m))
        v_t, v_lag = n * (s_t / 100.0 - 1.0), n * (s_lag / 100.0 - 1.0)
        for th in (0.0, 50_000.0):
            coll = np.sign(v_lag) * np.maximum(np.abs(v_lag) - th, 0.0)
            e = np.maximum(v_t - coll, 0.0)
            res[(days, th)] = (float(e.mean()), float(np.quantile(e, 0.95)), float(e.std(ddof=1) / math.sqrt(m)))
        ee0, pfe0, ee50 = res[(days, 0.0)][0], res[(days, 0.0)][1], res[(days, 50_000.0)][0]
        print(f"  MPOR {days} days: EE TH=0 {ee0:,.0f}, PFE95 {pfe0:,.0f}; TH=50k EE {ee50:,.0f}")
    c10 = collateralised_ee_closed(n, vol, 10 / 250)
    c20 = collateralised_ee_closed(n, vol, 20 / 250)
    check("collateralised EE closed form, MPOR 10 days", c10, 15_957, 1.0)
    check("collateralised EE closed form, MPOR 20 days", c20, 22_565, 1.0)
    check("ratio 20-day to 10-day", c20 / c10, 1.4141, 5e-4)
    check("collateralised / uncollateralised, 10 days", c10 / unc, 0.2003, 5e-4)
    for days, cf in ((10, c10), (20, c20)):
        assert abs(res[(days, 0.0)][0] - cf) < 3 * res[(days, 0.0)][2], f"collateralised EE Monte Carlo off for MPOR {days}"
    check("PFE95 with MPOR 10 days (about)", res[(10, 0.0)][1], 67_760, 200)
    check("PFE95 with MPOR 20 days (about)", res[(20, 0.0)][1], 96_400, 300)
    check("PFE95 / EE with MPOR 10 days (about)", res[(10, 0.0)][1] / c10, 4.25, 0.02)
    check("EE with MPOR 20 days and threshold 50k (about)", res[(20, 50_000.0)][0], 28_000, 100)
    check("EE with MPOR 10 days and threshold 50k (about)", res[(10, 50_000.0)][0], 23_900, 100)


# ---------------------------------------------------------------------------
# Worked example 1: netting and the standardised initial margin schedule (cards risk-net-to-gross-ratio-ngr,
# risk-close-out-netting-cherry-picking)
# ---------------------------------------------------------------------------


def section_netting_ngr() -> None:
    print("\n[Worked example 1: three swaps with one counterparty, MGN20.16 to MGN20.17 standardised initial margin]")
    mtm = np.array([12e6, -8.5e6, 1.5e6])
    notionals = np.array([100e6, 80e6, 50e6])
    rates = np.array([0.04, 0.02, 0.01])  # MGN20.16: interest rate 5+ year, 2-5 year, 0-2 year duration
    gross = float(np.maximum(mtm, 0.0).sum())
    net = max(float(mtm.sum()), 0.0)
    ngr = net / gross
    gross_im = float((notionals * rates).sum())
    net_im = (0.4 + 0.6 * ngr) * gross_im
    check("gross replacement cost", gross, 13_500_000, 0.0)
    check("net replacement cost", net, 5_000_000, 0.0)
    check("NGR", ngr, 0.370370, 5e-7)
    check("reduction from netting", 1.0 - ngr, 0.629630, 5e-7)
    check("gross standardised IM", gross_im, 6_100_000, 1e-6)
    check("factor 0.4 + 0.6 x NGR", 0.4 + 0.6 * ngr, 0.622222, 5e-7)
    check("net standardised IM", net_im, 3_795_556, 1.0)


def main() -> None:
    section_netting_ngr()
    section_forward()
    section_swap_profile()
    section_collateral()
    print("\nAll exposure profile checks passed.")


if __name__ == "__main__":
    main()
