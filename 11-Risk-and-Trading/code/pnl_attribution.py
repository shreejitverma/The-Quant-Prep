"""P&L attribution for an option book: Taylor (Greek) explain, full-revaluation waterfall, hedging P&L, PLA metrics.

Backs every number in 11-Risk-and-Trading/06-PnL-Attribution-and-Greek-Risk.md.

Model: Black-Scholes with continuous rate r and no dividends; time t runs forward, so theta = dV/dt = -dV/dT.
Greeks are analytic and are checked against central finite differences of the price.
The PLA metrics follow Basel MAR32.34 to MAR32.42 (Spearman correlation of RTPL and HPL, two-sample KS statistic
with the empirical CDF step of 0.004 = 1/250, green if rho > 0.80 and KS < 0.09, red if rho < 0.70 or KS > 0.12).

Run: python 11-Risk-and-Trading/code/pnl_attribution.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

SQRT2 = math.sqrt(2.0)


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a value and assert it matches the literal quoted in the note to within tol (absolute)."""
    print(f"  {label}: {value:.6f}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, note quotes {expected} (tol {tol})"
    return value


def ncdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def npdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


# ---------------------------------------------------------------------------
# Black-Scholes price and Greeks
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Option:
    kind: str  # "call" or "put"
    strike: float
    expiry: float  # years from today
    qty: float


def bs_price(kind: str, s: float, k: float, vol: float, tau: float, r: float) -> float:
    if tau <= 0.0:
        return max(s - k, 0.0) if kind == "call" else max(k - s, 0.0)
    sq = vol * math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * tau) / sq
    d2 = d1 - sq
    if kind == "call":
        return s * ncdf(d1) - k * math.exp(-r * tau) * ncdf(d2)
    return k * math.exp(-r * tau) * ncdf(-d2) - s * ncdf(-d1)


def bs_greeks(kind: str, s: float, k: float, vol: float, tau: float, r: float) -> dict[str, float]:
    """Analytic Greeks; theta and charm are per year of calendar time moving forward."""
    sq = vol * math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * tau) / sq
    d2 = d1 - sq
    disc = math.exp(-r * tau)
    pdf = npdf(d1)
    gamma = pdf / (s * sq)
    vega = s * pdf * math.sqrt(tau)
    call = kind == "call"
    delta = ncdf(d1) if call else ncdf(d1) - 1.0
    theta_common = -s * pdf * vol / (2.0 * math.sqrt(tau))
    theta = theta_common - r * k * disc * ncdf(d2) if call else theta_common + r * k * disc * ncdf(-d2)
    rho = k * tau * disc * ncdf(d2) if call else -k * tau * disc * ncdf(-d2)
    return {
        "price": bs_price(kind, s, k, vol, tau, r),
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "vanna": -pdf * d2 / vol,
        "volga": vega * d1 * d2 / vol,
        "rho": rho,
        "charm": -pdf * (2.0 * r * tau - d2 * sq) / (2.0 * tau * sq),
    }


def book_value(book: list[Option], s: float, vol: float, t: float, r: float) -> float:
    return sum(o.qty * bs_price(o.kind, s, o.strike, vol, o.expiry - t, r) for o in book)


def book_greeks(book: list[Option], s: float, vol: float, t: float, r: float) -> dict[str, float]:
    out: dict[str, float] = {}
    for o in book:
        for name, v in bs_greeks(o.kind, s, o.strike, vol, o.expiry - t, r).items():
            out[name] = out.get(name, 0.0) + o.qty * v
    return out


def taylor_terms(g: dict[str, float], ds: float, dvol: float, dt: float, dr: float = 0.0) -> dict[str, float]:
    return {
        "delta": g["delta"] * ds,
        "gamma": 0.5 * g["gamma"] * ds * ds,
        "theta": g["theta"] * dt,
        "vega": g["vega"] * dvol,
        "vanna": g["vanna"] * ds * dvol,
        "volga": 0.5 * g["volga"] * dvol * dvol,
        "rho": g["rho"] * dr,
    }


# ---------------------------------------------------------------------------
# PLA metrics (MAR32.34 to MAR32.42)
# ---------------------------------------------------------------------------


def ranks(x: np.ndarray) -> np.ndarray:
    """Ranks 1..n (MAR32.36); ties are measure-zero for continuous P&L."""
    order = np.argsort(x, kind="mergesort")
    out = np.empty(len(x))
    out[order] = np.arange(1, len(x) + 1)
    return out


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = ranks(a), ranks(b)
    return float(np.corrcoef(ra, rb)[0, 1])


def ks_statistic(a: np.ndarray, b: np.ndarray) -> float:
    """Largest gap between the two empirical CDFs (MAR32.39 to MAR32.41), evaluated at every observed value."""
    grid = np.sort(np.concatenate([a, b]))
    fa = np.searchsorted(np.sort(a), grid, side="right") / len(a)
    fb = np.searchsorted(np.sort(b), grid, side="right") / len(b)
    return float(np.max(np.abs(fa - fb)))


def kolmogorov_q(lam: float) -> float:
    """P(K > lam) for the Kolmogorov distribution: 2 sum_{j>=1} (-1)^(j-1) exp(-2 j^2 lam^2)."""
    return 2.0 * sum((-1) ** (j - 1) * math.exp(-2.0 * j * j * lam * lam) for j in range(1, 200))


def ks_exact_tail(c: int, n: int) -> float:
    """Exact P(D >= c/n) for two samples of equal size n: 1 - (lattice paths with |i - j| < c) / C(2n, n)."""
    row = np.zeros(n + 1)
    row[0] = 1.0
    for j in range(1, n + 1):
        row[j] = row[j - 1] if j < c else 0.0
    for i in range(1, n + 1):
        new = np.zeros(n + 1)
        for j in range(n + 1):
            if abs(i - j) < c:
                new[j] = row[j] + (new[j - 1] if j > 0 else 0.0)
        row = new
    return 1.0 - row[n] / math.comb(2 * n, n)


def pla_zone(rho: float, ks: float) -> str:
    if rho > 0.80 and ks < 0.09:
        return "green"
    if rho < 0.70 or ks > 0.12:
        return "red"
    return "amber"


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------


def section_greeks_and_pde() -> None:
    print("\n[Core concepts: analytic Greeks against finite differences, and the Black-Scholes PDE]")
    s, k, vol, tau, r = 100.0, 100.0, 0.20, 0.5, 0.05
    for kind in ("call", "put"):
        g = bs_greeks(kind, s, k, vol, tau, r)

        def p(ss: float = s, vv: float = vol, tt: float = tau, rr: float = r, kd: str = kind) -> float:
            return bs_price(kd, ss, k, vv, tt, rr)

        hs, hv, ht = 1e-3, 1e-4, 1e-5
        fd = {
            "delta": (p(ss=s + hs) - p(ss=s - hs)) / (2 * hs),
            "gamma": (p(ss=s + hs) - 2 * p() + p(ss=s - hs)) / hs**2,
            "vega": (p(vv=vol + hv) - p(vv=vol - hv)) / (2 * hv),
            "theta": -(p(tt=tau + ht) - p(tt=tau - ht)) / (2 * ht),
            "rho": (p(rr=r + hv) - p(rr=r - hv)) / (2 * hv),
            "vanna": (p(ss=s + hs, vv=vol + hv) - p(ss=s + hs, vv=vol - hv) - p(ss=s - hs, vv=vol + hv) + p(ss=s - hs, vv=vol - hv))
            / (4 * hs * hv),
            "volga": (p(vv=vol + 1e-3) - 2 * p() + p(vv=vol - 1e-3)) / 1e-6,
        }
        for name, v in fd.items():
            assert abs(v - g[name]) < 2e-4 * max(1.0, abs(g[name])), f"{kind} {name}: analytic {g[name]} vs FD {v}"
        pde = g["theta"] + 0.5 * vol**2 * s**2 * g["gamma"] + r * s * g["delta"] - r * g["price"]
        assert abs(pde) < 1e-10, f"Black-Scholes PDE residual {pde}"
    print("  analytic delta, gamma, vega, theta, rho, vanna, volga match central differences; PDE residual < 1e-10")
    g = bs_greeks("call", s, k, vol, tau, r)
    check("call theta per year, S=K=100, vol 20%, 6m, r 5%", g["theta"], -8.1160, 5e-5)
    check("of which -1/2 vol^2 S^2 gamma", -0.5 * vol**2 * s**2 * g["gamma"], -5.4717, 5e-5)
    check("of which -r S delta + r V (financing)", -r * s * g["delta"] + r * g["price"], -2.6442, 5e-5)


def straddle_book() -> tuple[list[Option], float, float, float]:
    """Long 100,000 one-month 100-strike calls and puts, delta-hedged with stock; S=100, vol 40%, r=0."""
    book = [Option("call", 100.0, 30.0 / 365.0, 100_000.0), Option("put", 100.0, 30.0 / 365.0, 100_000.0)]
    return book, 100.0, 0.40, 0.0


def section_example_1() -> dict[str, float]:
    print("\n[Worked example 1: earnings night on a delta-hedged long straddle]")
    book, s0, v0, r = straddle_book()
    g = book_greeks(book, s0, v0, 0.0, r)
    hedge = -g["delta"]  # shares held so the package is delta neutral
    for name in ("price", "delta", "gamma", "vega", "theta", "vanna", "volga"):
        print(f"  book {name:<6} {g[name]:>16,.2f}")
    print(f"  stock hedge {hedge:,.2f} shares")
    check("book value", g["price"], 914_484.46, 0.01)
    check("book delta before hedge", g["delta"], 4_572.42, 0.01)
    check("book gamma", g["gamma"], 6_946.27, 0.01)
    check("book vega per unit vol", g["vega"], 2_283_706.81, 0.01)
    check("book theta per year", g["theta"], -5_557_019.92, 0.01)
    check("book vanna", g["vanna"], 11_418.53, 0.01)
    check("book volga", g["volga"], -18_770.19, 0.01)
    ds, dvol, dt = 5.0, -0.10, 1.0 / 365.0
    full = book_value(book, s0 + ds, v0 + dvol, dt, r) - book_value(book, s0, v0, 0.0, r) + hedge * ds
    terms = taylor_terms({**g, "delta": 0.0}, ds, dvol, dt)
    explained = sum(terms.values())
    for name, v in terms.items():
        print(f"  {name:<6} {v:>14,.2f}")
    print(f"  explained {explained:,.2f}; full revaluation {full:,.2f}; unexplained {full - explained:,.2f}")
    check("gamma P&L", terms["gamma"], 86_828.44, 0.01)
    check("theta P&L, one calendar day", terms["theta"], -15_224.71, 0.01)
    check("vega P&L", terms["vega"], -228_370.68, 0.01)
    check("vanna P&L", terms["vanna"], -5_709.27, 0.01)
    check("volga P&L", terms["volga"], -93.85, 0.01)
    check("explained total", explained, -162_570.08, 0.01)
    check("full revaluation P&L", full, -134_084.90, 0.01)
    check("unexplained", full - explained, 28_485.18, 0.01)
    out = {"full": full, "explained": explained}
    # Unexplained is third order: scale the (spot, vol) move by k with no time step, and watch it grow like k^3.
    unexp = []
    for scale in (0.25, 0.5, 1.0, 2.0):
        f = book_value(book, s0 + scale * ds, v0 + scale * dvol, 0.0, r) - g["price"] + hedge * scale * ds
        e = sum(taylor_terms({**g, "delta": 0.0}, scale * ds, scale * dvol, 0.0).values())
        unexp.append(f - e)
    ratios = [unexp[i + 1] / unexp[i] for i in range(3)]
    print(
        f"  unexplained at move scales 0.25, 0.5, 1, 2 (no time step): {[round(u, 2) for u in unexp]}"
        f", ratios {[round(x, 3) for x in ratios]}"
    )
    check("unexplained at scale 0.25", unexp[0], 320.72, 0.01)
    check("unexplained at scale 2", unexp[3], 196_525.45, 0.01)
    for x in ratios:
        assert 7.5 < x < 9.5, "doubling the move must multiply the unexplained by about 2^3"
    # The same day explained by sequential full revaluation (waterfall) in two factor orders.
    v_00 = book_value(book, s0, v0, 0.0, r)
    spot_first = book_value(book, s0 + ds, v0, 0.0, r) - v_00 + hedge * ds
    vol_after_spot = book_value(book, s0 + ds, v0 + dvol, 0.0, r) - book_value(book, s0 + ds, v0, 0.0, r)
    vol_first = book_value(book, s0, v0 + dvol, 0.0, r) - v_00
    spot_after_vol = book_value(book, s0 + ds, v0 + dvol, 0.0, r) - book_value(book, s0, v0 + dvol, 0.0, r) + hedge * ds
    time_last = book_value(book, s0 + ds, v0 + dvol, dt, r) - book_value(book, s0 + ds, v0 + dvol, 0.0, r)
    print(f"  waterfall spot->vol->time: spot {spot_first:,.2f}, vol {vol_after_spot:,.2f}, time {time_last:,.2f}")
    print(f"  waterfall vol->spot->time: vol {vol_first:,.2f}, spot {spot_after_vol:,.2f}, time {time_last:,.2f}")
    check("waterfall sums to full revaluation", spot_first + vol_after_spot + time_last, full, 1e-6)
    check("spot step, spot first", spot_first, 83_468.05, 0.01)
    check("spot step, vol first", spot_after_vol, 104_397.56, 0.01)
    check("order effect on the spot bucket", spot_after_vol - spot_first, 20_929.51, 0.01)
    check("time step at the new spot and vol", time_last, -10_025.73, 0.01)
    check("unexplained as a share of the full P&L", (full - explained) / abs(full), 0.2124, 5e-5)
    check("vega per vol point", g["vega"] / 100.0, 22_837.07, 0.01)
    # Third-order terms (no time step), by central differences of the analytic book gamma, vanna and volga.
    hs_, hv_ = 1e-3, 1e-5

    def bg(name: str, s: float = s0, v: float = v0) -> float:
        return book_greeks(book, s, v, 0.0, r)[name]

    speed = (bg("gamma", s=s0 + hs_) - bg("gamma", s=s0 - hs_)) / (2 * hs_)
    zomma = (bg("gamma", v=v0 + hv_) - bg("gamma", v=v0 - hv_)) / (2 * hv_)
    vanna_vol = (bg("vanna", v=v0 + hv_) - bg("vanna", v=v0 - hv_)) / (2 * hv_)
    ultima = (bg("volga", v=v0 + hv_) - bg("volga", v=v0 - hv_)) / (2 * hv_)
    third = {
        "speed": speed * ds**3 / 6.0,
        "zomma": 0.5 * zomma * ds**2 * dvol,
        "vanna-vol": 0.5 * vanna_vol * ds * dvol**2,
        "ultima": ultima * dvol**3 / 6.0,
    }
    for name, v in third.items():
        print(f"  third-order {name:<9} {v:>12,.2f}")
    print(f"  sum of third-order terms {sum(third.values()):,.2f} against the no-time-step unexplained {unexp[2]:,.2f}")
    check("zomma term", third["zomma"], 21_778.47, 0.05)
    check("speed term", third["speed"], -2_170.71, 0.05)
    check("sum of third-order terms", sum(third.values()), 19_613.21, 0.05)
    assert max(third, key=lambda kk: abs(third[kk])) == "zomma", "zomma must be the largest third-order term"
    check("waterfall vol bucket, spot first", vol_after_spot, -207_527.22, 0.01)
    check("waterfall vol bucket, vol first", vol_first, -228_456.73, 0.01)
    return out


def section_breakeven() -> None:
    print("\n[Core concepts: break-even move of a delta-hedged long option, full revaluation]")
    book, s0, v0, r = straddle_book()
    g = book_greeks(book, s0, v0, 0.0, r)
    hedge = -g["delta"]
    for label, dt in (("trading day 1/252", 1.0 / 252.0), ("calendar day 1/365", 1.0 / 365.0)):
        formula = v0 * s0 * math.sqrt(dt)

        def pnl(ds: float, dt: float = dt) -> float:
            return book_value(book, s0 + ds, v0, dt, r) - g["price"] + hedge * ds

        lo, hi = 0.1, 10.0
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if pnl(mid) < 0.0 else (lo, mid)
        up = 0.5 * (lo + hi)
        lo, hi = -10.0, -0.1
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            lo, hi = (lo, mid) if pnl(mid) < 0.0 else (mid, hi)
        down = 0.5 * (lo + hi)
        print(f"  {label}: formula vol S sqrt(dt) = {formula:.4f}; full revaluation break-evens {down:+.4f} / {up:+.4f}")
        if dt == 1.0 / 252.0:
            check("formula, 1/252", formula, 2.5198, 5e-5)
            check("rule of 16: vol S / 16", v0 * s0 / 16.0, 2.5, 1e-12)
            check("full-revaluation up break-even, 1/252", up, 2.5412, 5e-5)
            check("full-revaluation down break-even, 1/252", down, -2.4782, 5e-5)
        else:
            check("formula, 1/365", formula, 2.0937, 5e-5)
            check("full-revaluation up break-even, 1/365", up, 2.1097, 5e-5)
            check("full-revaluation down break-even, 1/365", down, -2.0662, 5e-5)


_ERF = np.frompyfunc(math.erf, 1, 1)


def _call_delta_gamma(s: np.ndarray, k: float, vol: float, tau: float) -> tuple[np.ndarray, np.ndarray]:
    """Vectorised Black-Scholes call delta and gamma with r = 0 (exact erf, element by element)."""
    sq = vol * math.sqrt(tau)
    d1 = (np.log(s / k) + 0.5 * vol * vol * tau) / sq
    delta = 0.5 * (1.0 + _ERF(d1 / SQRT2).astype(float))
    gamma = np.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi) / (s * sq)
    return delta, gamma


def hedge_simulation(sig_real: float, sig_hedge: float, n_steps: int, n_paths: int, seed: int) -> dict[str, np.ndarray]:
    """Long one 1-month ATM call bought at implied 20%, delta-hedged n_steps times at sig_hedge.

    Real-world paths are driftless GBM at sig_real, r = 0.  Also accumulates the Taylor prediction
    1/2 sum Gamma_i S_i^2 ((dS/S)^2 - sig_hedge^2 dt) with Gamma at the hedging vol.
    """
    s0, k, t, sig_imp = 100.0, 100.0, 1.0 / 12.0, 0.20
    rng = np.random.default_rng(seed)
    dt = t / n_steps
    s = np.full(n_paths, s0)
    cash = np.full(n_paths, -bs_price("call", s0, k, sig_imp, t, 0.0))
    pred = np.zeros(n_paths)
    delta, gamma = _call_delta_gamma(s, k, sig_hedge, t)
    shares = -delta
    cash -= shares * s
    for i in range(n_steps):
        s_new = s * np.exp(-0.5 * sig_real**2 * dt + sig_real * math.sqrt(dt) * rng.standard_normal(n_paths))
        pred += 0.5 * gamma * s**2 * (((s_new - s) / s) ** 2 - sig_hedge**2 * dt)
        s = s_new
        if i < n_steps - 1:
            delta, gamma = _call_delta_gamma(s, k, sig_hedge, t - (i + 1) * dt)
            cash -= (-delta - shares) * s
            shares = -delta
    pnl = np.maximum(s - k, 0.0) + shares * s + cash
    return {"pnl": pnl, "pred": pred}


def section_hedging() -> None:
    print("\n[Core concepts: delta-hedged P&L, realized against implied variance, and discrete hedging error]")
    s0, k, t = 100.0, 100.0, 1.0 / 12.0
    vega = bs_greeks("call", s0, k, 0.20, t, 0.0)["vega"]
    check("vega of the 1-month ATM call per unit vol", vega, 11.5117, 5e-5)
    print("  discrete hedging error, realized = implied = 20%, against sqrt(pi/4) vega sigma / sqrt(N):")
    for n, want_sd in ((21, 0.4289), (84, 0.2165), (252, 0.1260)):
        res = hedge_simulation(0.20, 0.20, n, 8000, seed=50 + n)
        dk = math.sqrt(math.pi / 4.0) * vega * 0.20 / math.sqrt(n)
        print(
            f"  N = {n:>3}: MC mean {res['pnl'].mean():+.4f}, MC sd {res['pnl'].std():.4f}"
            f", formula {dk:.4f}, ratio {res['pnl'].std() / dk:.4f}"
        )
        check(f"MC sd of hedging P&L, N = {n} (seed {50 + n})", float(res["pnl"].std()), want_sd, 5e-4)
        assert abs(res["pnl"].std() / dk - 1.0) < 0.05, "Derman-Kamal must hold to within 5% here"
        assert abs(res["pnl"].mean()) < 3.0 * res["pnl"].std() / math.sqrt(8000), "hedging at the true vol has zero mean P&L"
    check("formula, N = 21", math.sqrt(math.pi / 4.0) * vega * 0.20 / math.sqrt(21), 0.4452, 5e-5)
    print("  worked example 2 (vega 100,000 per unit vol, sigma 30%):")
    for n, want in ((21, 5801.71), (84, 2900.86)):
        check(f"sqrt(pi/4) x 100,000 x 0.30 / sqrt({n})", math.sqrt(math.pi / 4.0) * 100_000.0 * 0.30 / math.sqrt(n), want, 0.01)
    print("  realized 25% against implied 20%, 1,000 rebalances, 4,000 paths, seed 41:")
    at_real = hedge_simulation(0.25, 0.25, 1000, 4000, seed=41)
    at_imp = hedge_simulation(0.25, 0.20, 1000, 4000, seed=41)
    target = bs_price("call", s0, k, 0.25, t, 0.0) - bs_price("call", s0, k, 0.20, t, 0.0)
    corr = float(np.corrcoef(at_imp["pnl"], at_imp["pred"])[0, 1])
    print(f"  BS(25%) - BS(20%) = {target:.4f}")
    print(f"  hedged at 25%: mean {at_real['pnl'].mean():.4f}, sd {at_real['pnl'].std():.4f}")
    print(f"  hedged at 20%: mean {at_imp['pnl'].mean():.4f}, sd {at_imp['pnl'].std():.4f}, corr with Taylor sum {corr:.4f}")
    check("BS(25%) - BS(20%)", target, 0.5755, 5e-5)
    check("mean P&L hedged at realized vol", float(at_real["pnl"].mean()), 0.5742, 5e-4)
    check("sd hedged at realized vol", float(at_real["pnl"].std()), 0.0797, 5e-4)
    check("mean P&L hedged at implied vol", float(at_imp["pnl"].mean()), 0.5775, 5e-4)
    check("sd hedged at implied vol", float(at_imp["pnl"].std()), 0.2531, 5e-4)
    check("corr(P&L hedged at implied, gamma-weighted variance spread)", corr, 0.9992, 5e-4)
    check("sd ratio, implied hedge / realised hedge", float(at_imp["pnl"].std() / at_real["pnl"].std()), 3.17, 5e-3)


def section_pla() -> None:
    print("\n[Core concepts: PLA test thresholds (MAR32.42) and a simulated desk]")
    lam9, lam12 = 0.09 * math.sqrt(125.0), 0.12 * math.sqrt(125.0)
    check("Kolmogorov tail at KS = 0.09, n = m = 250", kolmogorov_q(lam9), 0.2634, 5e-5)
    check("Kolmogorov tail at KS = 0.12", kolmogorov_q(lam12), 0.0546, 5e-5)
    check("exact P(KS >= 0.120), n = m = 250", ks_exact_tail(30, 250), 0.0546, 5e-5)
    check("exact P(KS >= 0.092), the smallest failing value above 0.09", ks_exact_tail(23, 250), 0.2409, 5e-5)
    check("exact P(KS >= 0.088)", ks_exact_tail(22, 250), 0.2881, 5e-5)
    rng = np.random.default_rng(77)
    n = 250
    s0, v0, r = 100.0, 0.25, 0.0
    book = [Option("call", 100.0, 0.25, -50_000.0), Option("put", 95.0, 0.25, 80_000.0)]
    g0 = book_greeks(book, s0, v0, 0.0, r)
    hedge = -g0["delta"]
    rets = 0.015 * rng.standard_normal(n)
    dvols = -0.7 * 0.01 * (rets / 0.015) + math.sqrt(1 - 0.49) * 0.01 * rng.standard_normal(n)
    hpl, rtpl_full, rtpl_novol, rtpl_taylor = (np.empty(n) for _ in range(4))
    v_base = book_value(book, s0, v0, 0.0, r)
    for i in range(n):
        ds = s0 * rets[i]
        hpl[i] = book_value(book, s0 + ds, v0 + dvols[i], 0.0, r) - v_base + hedge * ds
        rtpl_full[i] = hpl[i]
        rtpl_novol[i] = book_value(book, s0 + ds, v0, 0.0, r) - v_base + hedge * ds
        rtpl_taylor[i] = sum(taylor_terms({**g0, "delta": 0.0}, ds, dvols[i], 0.0).values())
    for label, rt in (("RTPL = HPL", rtpl_full), ("RTPL without vol factor", rtpl_novol), ("RTPL delta-gamma-vega", rtpl_taylor)):
        rho, ks = spearman(hpl, rt), ks_statistic(hpl, rt)
        print(f"  {label:<26}: Spearman {rho:.4f}, KS {ks:.4f}, zone {pla_zone(rho, ks)}")
    rho_nv, ks_nv = spearman(hpl, rtpl_novol), ks_statistic(hpl, rtpl_novol)
    rho_t, ks_t = spearman(hpl, rtpl_taylor), ks_statistic(hpl, rtpl_taylor)
    check("Spearman, vol factor missing", rho_nv, 0.3090, 5e-5)
    check("KS, vol factor missing", ks_nv, 0.4040, 5e-5)
    check("Spearman, delta-gamma-vega", rho_t, 0.9995, 5e-5)
    check("KS, delta-gamma-vega", ks_t, 0.0160, 5e-5)
    assert pla_zone(rho_nv, ks_nv) == "red" and pla_zone(rho_t, ks_t) == "green"
    assert pla_zone(1.0, 0.0) == "green" and pla_zone(0.75, 0.05) == "amber"


def main() -> None:
    section_greeks_and_pde()
    section_example_1()
    section_breakeven()
    section_hedging()
    section_pla()
    print("\nAll P&L attribution checks passed.")


if __name__ == "__main__":
    main()
