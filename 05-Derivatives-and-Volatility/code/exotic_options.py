"""Exotic options: closed forms checked by Monte Carlo, and the risk numbers a desk looks at.

Backs the note 05-Derivatives-and-Volatility/12-Exotic-Options.md.
Every number the note quotes is printed here and asserted against the literal at the note's quoted rounding
(half a unit of the last quoted digit); simulations use fixed seeds, and bounds are asserted as bounds.

Sections
1. Digitals: cash and asset legs, call-spread overhedge, skew-adjusted digital, Greeks near expiry.
2. Barriers: all eight Reiner-Rubinstein (Haug) closed forms, in-out parity, Monte Carlo with and without
   the Brownian-bridge correction, the Broadie-Glasserman-Kou shift, Greeks of a reverse knock-out.
3. Asians: discrete geometric closed form and the arithmetic Asian with a geometric control variate.
4. Lookbacks: Goldman-Sosin-Gatto floating-strike formulas checked with exact Brownian-bridge extremes.
5. Autocallable: fair memory coupon, path statistics, dealer vega and dividend sensitivity by bumps with common random numbers.
6. Forward starts and a locally capped, globally floored cliquet.

Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/exotic_options.py
"""

from __future__ import annotations

import math

import numpy as np
from pricing_core import bs_price, bs_vega, norm_cdf, norm_pdf

S0, K, T, R, Q, SIG = 100.0, 100.0, 1.0, 0.05, 0.0, 0.20
BETA_BGK = 0.5826  # -zeta(1/2) / sqrt(2 pi), Broadie-Glasserman-Kou (1997); checked in main()


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a labelled value and assert it is within tol of the quoted number."""
    print(f"{label}: {value:.6g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected} +/- {tol}"
    return value


def zeta_borwein(s: float, n: int = 40) -> float:
    """Riemann zeta for real s > 0, s != 1, from the Dirichlet eta function by Borwein's (2000) algorithm 2:
    eta(s) = -1/d_n sum_{k<n} (-1)^k (d_k - d_n) / (k + 1)^s, zeta(s) = eta(s) / (1 - 2^{1 - s})."""
    terms = [math.factorial(n + i - 1) * 4**i / (math.factorial(n - i) * math.factorial(2 * i)) for i in range(n + 1)]
    d = [n * sum(terms[: k + 1]) for k in range(n + 1)]
    eta = -sum((-1) ** k * (d[k] - d[n]) / (k + 1) ** s for k in range(n)) / d[n]
    return eta / (1.0 - 2.0 ** (1.0 - s))


# ---------------------------------------------------------------------------
# 1. Digitals
# ---------------------------------------------------------------------------


def d1d2(S: float, K_: float, T_: float, r: float, sigma: float, q: float = 0.0) -> tuple[float, float]:
    sd = sigma * math.sqrt(T_)
    d1 = (math.log(S / K_) + (r - q + 0.5 * sigma**2) * T_) / sd
    return d1, d1 - sd


def cash_digital(S: float, K_: float, T_: float, r: float, sigma: float, q: float = 0.0) -> float:
    return math.exp(-r * T_) * norm_cdf(d1d2(S, K_, T_, r, sigma, q)[1])


def cash_digital_delta_gamma(S: float, K_: float, T_: float, r: float, sigma: float) -> tuple[float, float]:
    d1, d2 = d1d2(S, K_, T_, r, sigma)
    sd = sigma * math.sqrt(T_)
    delta = math.exp(-r * T_) * norm_pdf(d2) / (S * sd)
    gamma = -math.exp(-r * T_) * norm_pdf(d2) * d1 / (S**2 * sd**2)
    return delta, gamma


# ---------------------------------------------------------------------------
# 2. Barriers (Reiner and Rubinstein 1991, in the notation of Haug 2007), no rebate
# ---------------------------------------------------------------------------


def barrier_price(kind: str, S: float, X: float, H: float, T_: float, r: float, q: float, sigma: float) -> float:
    """Continuously monitored single-barrier option, zero rebate, spot not yet beyond the barrier.

    kind: c|p, d|u, i|o, e.g. "cdo" = down-and-out call.
    """
    b = r - q
    sst = sigma * math.sqrt(T_)
    mu = (b - 0.5 * sigma**2) / sigma**2
    x1 = math.log(S / X) / sst + (1 + mu) * sst
    x2 = math.log(S / H) / sst + (1 + mu) * sst
    y1 = math.log(H * H / (S * X)) / sst + (1 + mu) * sst
    y2 = math.log(H / S) / sst + (1 + mu) * sst
    phi = 1.0 if kind[0] == "c" else -1.0
    eta = 1.0 if kind[1] == "d" else -1.0
    fs, fx = S * math.exp((b - r) * T_), X * math.exp(-r * T_)
    hs1, hs0 = (H / S) ** (2 * (mu + 1)), (H / S) ** (2 * mu)
    A = phi * fs * norm_cdf(phi * x1) - phi * fx * norm_cdf(phi * x1 - phi * sst)
    B = phi * fs * norm_cdf(phi * x2) - phi * fx * norm_cdf(phi * x2 - phi * sst)
    C = phi * fs * hs1 * norm_cdf(eta * y1) - phi * fx * hs0 * norm_cdf(eta * y1 - eta * sst)
    D = phi * fs * hs1 * norm_cdf(eta * y2) - phi * fx * hs0 * norm_cdf(eta * y2 - eta * sst)
    above = X > H
    table = {
        "cdi": C if above else A - B + D,
        "cui": A if above else B - C + D,
        "pdi": B - C + D if above else A,
        "pui": A - B + D if above else C,
        "cdo": A - C if above else B - D,
        "cuo": 0.0 if above else A - B + C - D,
        "pdo": A - B + C - D if above else 0.0,
        "puo": B - D if above else A - C,
    }
    return table[kind]


def barrier_mc(kind: str, H: float, n_steps: int, n_paths: int, seed: int, bridge: bool) -> tuple[float, float]:
    """Knock-out call or put on a grid of n_steps; with bridge=True each step carries the exact probability of
    not having crossed the barrier between grid points (continuous monitoring), otherwise the barrier is only
    checked on the grid (discrete monitoring). The vanilla payoff is a control variate (known Black-Scholes mean).
    Returns (price, standard error)."""
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    nu = (R - Q - 0.5 * SIG**2) * dt
    h = math.log(H)
    down = kind[1] == "d"
    call = kind[0] == "c"
    ko, van = [], []
    for _ in range(n_paths // 25_000):
        z = rng.standard_normal((25_000, n_steps))
        x = np.concatenate([np.full((25_000, 1), math.log(S0)), math.log(S0) + np.cumsum(nu + SIG * math.sqrt(dt) * z, axis=1)], axis=1)
        dist = (x - h) if down else (h - x)  # distance to the barrier, positive while alive
        alive = np.all(dist[:, 1:] > 0, axis=1).astype(float)
        if bridge:
            cross = np.exp(-2.0 * dist[:, :-1] * dist[:, 1:] / (SIG**2 * dt))
            alive = alive * np.prod(1.0 - cross, axis=1)
        st = np.exp(x[:, -1])
        payoff = math.exp(-R * T) * (np.maximum(st - K, 0.0) if call else np.maximum(K - st, 0.0))
        ko.append(payoff * alive)
        van.append(payoff)
    y, c = np.concatenate(ko), np.concatenate(van)
    b = np.cov(y, c)[0, 1] / np.var(c, ddof=1)
    est = y - b * (c - bs_price(S0, K, T, R, SIG, Q, call=call))
    return float(est.mean()), float(est.std(ddof=1) / math.sqrt(len(est)))


def barrier_greeks(kind: str, S: float, H: float, sigma: float = SIG) -> tuple[float, float, float, float]:
    """Price, delta, gamma (central differences, h = 0.01) and vega per vol point of a barrier option."""
    hs = 0.01

    def p(s: float, sig: float = sigma) -> float:
        return barrier_price(kind, s, K, H, T, R, Q, sig)

    v0 = p(S)
    delta = (p(S + hs) - p(S - hs)) / (2 * hs)
    gamma = (p(S + hs) - 2 * v0 + p(S - hs)) / hs**2
    vega = (p(S, sigma + 0.005) - p(S, sigma - 0.005)) / 1.0  # per 1 vol point
    return v0, delta, gamma, vega


# ---------------------------------------------------------------------------
# 3. Asians
# ---------------------------------------------------------------------------


def geometric_asian_call(S: float, K_: float, T_: float, r: float, q: float, sigma: float, n: int) -> float:
    """Discretely monitored geometric-average call, fixings at t_i = i T / n, i = 1..n."""
    t = T_ * np.arange(1, n + 1) / n
    mu = math.log(S) + (r - q - 0.5 * sigma**2) * t.mean()
    var = sigma**2 * np.minimum.outer(t, t).sum() / n**2
    sd = math.sqrt(var)
    d1 = (mu - math.log(K_) + var) / sd
    return math.exp(-r * T_) * (math.exp(mu + 0.5 * var) * norm_cdf(d1) - K_ * norm_cdf(d1 - sd))


# ---------------------------------------------------------------------------
# 4. Lookbacks (Goldman, Sosin and Gatto 1979; formulas as in Haug 2007), b = r - q != 0
# ---------------------------------------------------------------------------


def lookback_float_call(S: float, s_min: float, T_: float, r: float, q: float, sigma: float) -> float:
    """Pays S_T - min S over [0, T]; s_min is the running minimum so far."""
    b = r - q
    sst = sigma * math.sqrt(T_)
    a1 = (math.log(S / s_min) + (b + 0.5 * sigma**2) * T_) / sst
    a2 = a1 - sst
    term = (S / s_min) ** (-2 * b / sigma**2) * norm_cdf(-a1 + 2 * b / sigma * math.sqrt(T_)) - math.exp(b * T_) * norm_cdf(-a1)
    return (
        S * math.exp((b - r) * T_) * norm_cdf(a1)
        - s_min * math.exp(-r * T_) * norm_cdf(a2)
        + S * math.exp(-r * T_) * sigma**2 / (2 * b) * term
    )


def lookback_float_put(S: float, s_max: float, T_: float, r: float, q: float, sigma: float) -> float:
    """Pays max S over [0, T] - S_T; s_max is the running maximum so far."""
    b = r - q
    sst = sigma * math.sqrt(T_)
    b1 = (math.log(S / s_max) + (b + 0.5 * sigma**2) * T_) / sst
    b2 = b1 - sst
    term = -((S / s_max) ** (-2 * b / sigma**2)) * norm_cdf(b1 - 2 * b / sigma * math.sqrt(T_)) + math.exp(b * T_) * norm_cdf(b1)
    return (
        s_max * math.exp(-r * T_) * norm_cdf(-b2)
        - S * math.exp((b - r) * T_) * norm_cdf(-b1)
        + S * math.exp(-r * T_) * sigma**2 / (2 * b) * term
    )


def lookback_mc(n_paths: int, seed: int) -> tuple[float, float, float, float]:
    """Exact simulation of (S_T, min, max) over one step: the extremes of a Brownian bridge between the
    endpoints are sampled in closed form, so no time grid is needed. Returns call and put prices with errors."""
    rng = np.random.default_rng(seed)
    x0 = math.log(S0)
    sst = SIG * math.sqrt(T)
    xt = x0 + (R - Q - 0.5 * SIG**2) * T + sst * rng.standard_normal(n_paths)
    jump = xt - x0
    u1, u2 = rng.random(n_paths), rng.random(n_paths)
    xmin = 0.5 * (x0 + xt - np.sqrt(jump**2 - 2 * SIG**2 * T * np.log(u1)))
    xmax = 0.5 * (x0 + xt + np.sqrt(jump**2 - 2 * SIG**2 * T * np.log(u2)))
    disc = math.exp(-R * T)
    call = disc * (np.exp(xt) - np.exp(xmin))
    put = disc * (np.exp(xmax) - np.exp(xt))
    se = math.sqrt(n_paths)
    return float(call.mean()), float(call.std() / se), float(put.mean()), float(put.std() / se)


# ---------------------------------------------------------------------------
# 5. Autocallable
# ---------------------------------------------------------------------------

AC = {"S0": 100.0, "r": 0.03, "q": 0.02, "sigma": 0.25, "years": 3, "obs_per_year": 4, "trigger": 1.0, "ki": 0.6}


def autocall_legs(sigma: float, q: float, z: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Per path: discounted principal leg, discounted coupon count (coupon c per period with memory paid at the
    call date), the call index (0 if never called) and the final spot. Common random numbers z across bumps."""
    r = AC["r"]
    dt = 1.0 / AC["obs_per_year"]
    paths = AC["S0"] * np.exp(np.cumsum((r - q - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * z, axis=1))
    above = paths >= AC["trigger"] * AC["S0"]
    called = above.any(axis=1)
    k_call = np.where(called, above.argmax(axis=1) + 1, 0)  # first observation at or above the trigger
    t_call = k_call * dt
    st = paths[:, -1]
    principal_mat = np.where(st >= AC["ki"] * AC["S0"], 100.0, 100.0 * st / AC["S0"])
    principal = np.where(called, 100.0 * np.exp(-r * t_call), principal_mat * math.exp(-r * AC["years"]))
    coupons = np.where(called, k_call * np.exp(-r * t_call), 0.0)  # number of coupons paid, discounted
    return principal, coupons, k_call, st


# ---------------------------------------------------------------------------
# 6. Forward start and cliquet
# ---------------------------------------------------------------------------


def forward_start_call(S: float, t1: float, T_: float, r: float, q: float, sigma: float, moneyness: float = 1.0) -> float:
    """Rubinstein (1991): call struck at moneyness * S_{t1}, set at t1, expiring T. Homogeneity gives
    S e^{-q t1} C_BS(1, moneyness, T - t1)."""
    return S * math.exp(-q * t1) * bs_price(1.0, moneyness, T_ - t1, r, sigma, q)


CLQ = {"n": 12, "cap": 0.03, "floor": -0.03, "global_floor": 0.02, "notional": 100.0}


def cliquet_mc(sigma: float, z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Monthly returns R_i clipped to [floor, cap]; pays notional * max(global floor, sum) at T = 1.
    Returns discounted payoff with and without the global floor."""
    dt = T / CLQ["n"]
    rets = np.exp((R - Q - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * z) - 1.0
    total = np.clip(rets, CLQ["floor"], CLQ["cap"]).sum(axis=1)
    disc = math.exp(-R * T) * CLQ["notional"]
    return disc * np.maximum(CLQ["global_floor"], total), disc * total


def cliquet_no_floor_closed_form(sigma: float) -> float:
    """E[sum clip(R_i, f, c)] discounted: each clipped return is R - (R - c)^+ + (f - R)^+, a forward-start
    combination; independence of the returns makes every term a one-period Black-Scholes price."""
    dt = T / CLQ["n"]
    growth = math.exp(R * dt)
    e_r = math.exp((R - Q) * dt) - 1.0
    e_call = growth * bs_price(1.0, 1.0 + CLQ["cap"], dt, R, sigma, Q)
    e_put = growth * bs_price(1.0, 1.0 + CLQ["floor"], dt, R, sigma, Q, call=False)
    return math.exp(-R * T) * CLQ["notional"] * CLQ["n"] * (e_r - e_call + e_put)


def main() -> None:
    # 1. Digitals. Backs note sections "Digitals", Examples 1-2 and cards deriv-digital-skew-adjustment,
    #    deriv-digital-overhedge, deriv-digital-pin-risk, deriv-digital-asset-cash.
    print("1. digitals (S 100, K 100, T 1, r 5%, sigma 20%)")
    vanilla = bs_price(S0, K, T, R, SIG)
    d1, d2 = d1d2(S0, K, T, R, SIG)
    cash = cash_digital(S0, K, T, R, SIG)
    asset = S0 * norm_cdf(d1)
    check("cash-or-nothing e^{-rT} N(d2)", cash, 0.5323, 5e-5)
    check("asset-or-nothing S N(d1)", asset, 63.68, 5e-3)
    check("asset - K cash = vanilla call", asset - K * cash, 10.4506, 5e-5)
    for h, exp_spread in ((2.0, 0.5511), (1.0, 0.5417), (0.5, 0.5370)):
        spread = (bs_price(S0, K - h, T, R, SIG) - bs_price(S0, K, T, R, SIG)) / h
        check(f"overhedge call spread (K-{h:g}, K) per unit width", spread, exp_spread, 5e-5)
        check(f"  overhedge cost over the digital, width {h:g}", spread - cash, {2.0: 0.0188, 1.0: 0.0094, 0.5: 0.0047}[h], 5e-5)
    density = math.exp(-R * T) * norm_pdf(d2) / (K * SIG * math.sqrt(T))
    check("discounted risk-neutral density at K (overhedge cost per unit width x 2)", density, 0.01876, 5e-6)
    # skewed smile, three-month digital
    t3, atm, skew = 0.25, 0.20, -0.004

    def smile(k: float) -> float:
        return atm + skew * (k - 100.0)

    flat = cash_digital(S0, K, t3, R, atm)
    vega3 = bs_vega(S0, K, t3, R, atm)
    with_skew = flat - vega3 * skew
    tight = (bs_price(S0, K - 0.01, t3, R, smile(K - 0.01)) - bs_price(S0, K + 0.01, t3, R, smile(K + 0.01))) / 0.02
    check("3m digital at flat 20% vol", flat, 0.5233, 5e-5)
    check("3m vega per unit vol", vega3, 19.64, 5e-3)
    check("3m skew term -vega * dsigma/dK", -vega3 * skew, 0.0786, 5e-5)
    check("3m digital with skew -0.004 per strike point", with_skew, 0.6019, 5e-5)
    check("3m digital as 0.02-wide call spread on the smile", tight, 0.6019, 5e-5)
    check("  skew term in points of payout (per 100)", -100 * vega3 * skew, 8, 0.5)
    print("digital Greeks at the strike near expiry, payout 1,000,000")
    for label, tt, ex_delta in (("1 month", 1 / 12, 68_700), ("1 week", 1 / 52, 143_700), ("1 day", 1 / 252, 316_600)):
        delta, _ = cash_digital_delta_gamma(S0, K, tt, R, SIG)
        check(f"  delta at S = K, {label} (shares)", 1e6 * delta, ex_delta, 50)
        if label == "1 day":
            check("  1 day delta in dollars of stock at S = 100 (millions)", 1e6 * delta * S0 / 1e6, 31.66, 5e-3)
    _, g_lo = cash_digital_delta_gamma(99.0, K, 1 / 252, R, SIG)
    _, g_hi = cash_digital_delta_gamma(101.0, K, 1 / 252, R, SIG)
    check("  1 day gamma at S = 99 (shares per point)", 1e6 * g_lo, 145_800, 50)
    check("  1 day gamma at S = 101 (shares per point)", 1e6 * g_hi, -145_300, 50)
    assert min(abs(1e6 * g_lo), abs(1e6 * g_hi)) > 145_000, "gamma flips by more than 145,000 shares per point"
    print()

    # 2. Barriers. Backs "Barriers", Examples 3-4 and cards deriv-barrier-in-out-parity, deriv-barrier-bridge,
    #    deriv-barrier-bgk, deriv-barrier-reverse-greeks, deriv-barrier-delta-jump, deriv-barrier-regular-delta.
    print("2. barriers (K 100, down barrier 90, up barrier 120)")
    expected = {
        "cdo": 8.6655,
        "cdi": 1.7851,
        "cuo": 1.1761,
        "cui": 9.2745,
        "pdo": 0.1512,
        "pdi": 5.4223,
        "puo": 5.3601,
        "pui": 0.2134,
    }
    put_vanilla = bs_price(S0, K, T, R, SIG, call=False)
    check("vanilla call", vanilla, 10.4506, 5e-5)
    check("vanilla put", put_vanilla, 5.5735, 5e-5)
    for kind, ex in expected.items():
        H = 90.0 if kind[1] == "d" else 120.0
        check(f"{kind} H={H:g}", barrier_price(kind, S0, K, H, T, R, Q, SIG), ex, 5e-5)
    for c in ("c", "p"):
        for d, H in (("d", 90.0), ("u", 120.0)):
            pair = barrier_price(c + d + "i", S0, K, H, T, R, Q, SIG) + barrier_price(c + d + "o", S0, K, H, T, R, Q, SIG)
            assert abs(pair - (vanilla if c == "c" else put_vanilla)) < 1e-10, (c, d, pair)
    print("in + out = vanilla within 1e-10 for all four pairs: ok")
    mu_r = (R - Q - 0.5 * SIG**2) / SIG**2
    reflected = bs_price(S0, K, T, R, SIG, Q) - (90.0 / S0) ** (2 * mu_r) * bs_price(90.0**2 / S0, K, T, R, SIG, Q)
    check("reflection C_BS(S) - (H/S)^{2 mu} C_BS(H^2/S) for the down-and-out call", reflected, 8.6655, 5e-5)
    # r = q gives mu = -1/2 and the classic C_BS(S, K) - (S/H) C_BS(H^2/S, K); at S = H the two terms cancel.
    rq = barrier_price("cdo", S0, K, 90.0, T, R, R, SIG)
    classic = bs_price(S0, K, T, R, SIG, R) - S0 / 90.0 * bs_price(90.0**2 / S0, K, T, R, SIG, R)
    assert abs(rq - classic) < 1e-10, (rq, classic)
    assert abs(barrier_price("cdo", 90.0, K, 90.0, T, R, Q, SIG)) < 1e-12
    print("r = q reflection matches C_BS(S) - (S/H) C_BS(H^2/S); price at S = H is 0: ok")
    mc_cases = {
        # kind, barrier, steps, bridge: price, standard error (seed 11, 200,000 paths)
        ("cdo", 90.0, 252, True): (8.6815, 0.0123),
        ("cdo", 90.0, 252, False): (8.9316, 0.0117),
        ("cdo", 90.0, 12, False): (9.5789, 0.0087),
        ("cuo", 120.0, 252, True): (1.1794, 0.0069),
        ("cuo", 120.0, 252, False): (1.3314, 0.0076),
        ("cuo", 120.0, 12, True): (1.1813, 0.0063),
    }
    mc_res = {}
    for (kind, H, steps, bridge), (ex, ex_se) in mc_cases.items():
        price, se = barrier_mc(kind, H, steps, 200_000, seed=11, bridge=bridge)
        key = f"{kind}{steps}{'T' if bridge else 'F'}"
        check(f"  MC {kind} H={H:g} steps={steps} bridge={bridge}", price, ex, 5e-5)
        check(f"  MC {kind} H={H:g} steps={steps} bridge={bridge} standard error", se, ex_se, 5e-5)
        if bridge:  # the bridge estimator targets the continuous closed form on any grid
            cf_ = barrier_price(kind, S0, K, H, T, R, Q, SIG)
            assert abs(price - cf_) < 2 * se, ("bridge vs closed form", key, price, cf_, se)
        mc_res[key] = (price, se)
    print("  every bridge row is within two standard errors of its closed form: ok")
    cdo_cf = barrier_price("cdo", S0, K, 90.0, T, R, Q, SIG)
    check("daily grid-only overpricing of the down-and-out", mc_res["cdo252F"][0] - cdo_cf, 0.27, 0.005)
    check("monthly grid-only overpricing of the down-and-out", mc_res["cdo12F"][0] - cdo_cf, 0.91, 0.005)
    shift = BETA_BGK * SIG * math.sqrt(1 / 252)
    check("BGK beta = -zeta(1/2) / sqrt(2 pi)", -zeta_borwein(0.5) / math.sqrt(2 * math.pi), BETA_BGK, 5e-5)
    check("BGK shift beta sigma sqrt(dt), daily", shift, 0.00734, 5e-6)
    check("BGK shift in percent", 100 * shift, 0.734, 5e-4)
    check("shifted down barrier 90 e^{-shift}", 90 * math.exp(-shift), 89.34, 5e-3)
    bgk_dn = barrier_price("cdo", S0, K, 90 * math.exp(-shift), T, R, Q, SIG)
    bgk_up = barrier_price("cuo", S0, K, 120 * math.exp(shift), T, R, Q, SIG)
    assert abs(bgk_dn - mc_res["cdo252F"][0]) < 2 * mc_res["cdo252F"][1], "BGK vs daily simulation (down)"
    assert abs(bgk_up - mc_res["cuo252F"][0]) < 2 * mc_res["cuo252F"][1], "BGK vs daily simulation (up)"
    check(
        "BGK: daily down-and-out = continuous at 90 e^{-shift}",
        barrier_price("cdo", S0, K, 90 * math.exp(-shift), T, R, Q, SIG),
        8.9139,
        5e-5,
    )
    check(
        "BGK: daily up-and-out = continuous at 120 e^{+shift}",
        barrier_price("cuo", S0, K, 120 * math.exp(shift), T, R, Q, SIG),
        1.3321,
        5e-5,
    )
    print("up-and-out call K 100 H 120: price, delta, gamma, vega per vol point")
    uoc_expected = {
        90.0: (1.1323, 0.0306, -0.0044, -0.0821),
        100.0: (1.1761, -0.0237, -0.0055, -0.1326),
        110.0: (0.7033, -0.0654, -0.0023, -0.0903),
        118.0: (0.1402, -0.0711, 0.0008, -0.0179),
    }
    for s_, ex in uoc_expected.items():
        got = barrier_greeks("cuo", s_, 120.0)
        print(f"  S={s_:g}: " + " ".join(f"{g:+.4f}" for g in got))
        for g, e in zip(got, ex, strict=True):
            assert abs(g - e) <= 5e-5, (s_, got, ex)
    uoc100 = barrier_greeks("cuo", 100.0, 120.0)
    check("up-and-out price at 100, two decimals", uoc100[0], 1.18, 5e-3)
    check("vanilla call, two decimals", vanilla, 10.45, 5e-3)
    check("up-and-out vega at 100, two decimals", uoc100[3], -0.13, 5e-3)
    check("up-and-out delta at 118, two decimals", barrier_greeks("cuo", 118.0, 120.0)[1], -0.07, 5e-3)
    vanilla_delta = norm_cdf(d1)
    check("vanilla call delta at 100", vanilla_delta, 0.6368, 5e-5)
    print("down-and-out call K 100 H 90 near the barrier: price, delta")
    for s_, (ex_p, ex_d) in {91.0: (0.9320, 0.9202), 95.0: (4.4688, 0.8562)}.items():
        p_, dlt, _, _ = barrier_greeks("cdo", s_, 90.0)
        check(f"  S={s_:g} price", p_, ex_p, 5e-5)
        check(f"  S={s_:g} delta", dlt, ex_d, 5e-5)
        check(f"  S={s_:g} vanilla delta", norm_cdf(d1d2(s_, K, T, R, SIG)[0]), {91.0: 0.4516, 95.0: 0.5373}[s_], 5e-5)
    print()

    # 3. Asians. Backs "Asians", Example 5 and cards deriv-asian-control-variate, deriv-asian-geometric-formula.
    print("3. Asian call, 12 monthly fixings")
    n_fix = 12
    geo = geometric_asian_call(S0, K, T, R, Q, SIG, n_fix)
    check("geometric Asian closed form", geo, 5.9402, 5e-5)
    rng = np.random.default_rng(5)
    n_paths = 200_000
    dt = T / n_fix
    z = rng.standard_normal((n_paths, n_fix))
    paths = S0 * np.exp(np.cumsum((R - Q - 0.5 * SIG**2) * dt + SIG * math.sqrt(dt) * z, axis=1))
    disc = math.exp(-R * T)
    arith = disc * np.maximum(paths.mean(axis=1) - K, 0.0)
    geom = disc * np.maximum(np.exp(np.log(paths).mean(axis=1)) - K, 0.0)
    b_cv = np.cov(arith, geom)[0, 1] / np.var(geom, ddof=1)
    cv = arith - b_cv * (geom - geo)
    se_plain = arith.std(ddof=1) / math.sqrt(n_paths)
    se_cv = cv.std(ddof=1) / math.sqrt(n_paths)
    # G <= arithmetic mean on every path (AM-GM), so the geometric payoff never exceeds the arithmetic one.
    assert np.all(geom <= arith), "geometric payoff above arithmetic payoff"
    check("MC geometric (check of closed form)", geom.mean(), 5.9472, 5e-5)
    check("arithmetic plain MC", arith.mean(), 6.1624, 5e-5)
    check("arithmetic plain MC standard error", se_plain, 0.0190, 5e-5)
    check("arithmetic with geometric control variate", cv.mean(), 6.1552, 5e-5)
    check("control-variate standard error", se_cv, 0.00053, 5e-6)
    check("correlation arithmetic vs geometric payoff", np.corrcoef(arith, geom)[0, 1], 0.9996, 5e-5)
    check("variance reduction factor", (se_plain / se_cv) ** 2, 1301, 0.5)
    assert (se_plain / se_cv) ** 2 > 1000, "variance reduction above 1000x"
    check("control coefficient b", b_cv, 1.031, 5e-4)
    check("equivalent plain paths (millions)", (se_plain / se_cv) ** 2 * n_paths / 1e6, 260, 0.5)
    check("arithmetic Asian / vanilla", cv.mean() / vanilla, 0.589, 5e-4)
    t_fix = T * np.arange(1, n_fix + 1) / n_fix
    var_ratio = np.minimum.outer(t_fix, t_fix).sum() / n_fix**2 / T
    check("geometric log-variance / terminal log-variance", var_ratio, 0.376, 5e-4)
    # sum_{i,j} min(i, j) = n(n + 1)(2n + 1)/6, so the ratio is (n + 1)(2n + 1)/(6 n^2) -> 1/3 (Kemna-Vorst limit).
    assert abs(var_ratio - (n_fix + 1) * (2 * n_fix + 1) / (6 * n_fix**2)) < 1e-12
    n_big = 2000
    t_big = T * np.arange(1, n_big + 1) / n_big
    check("ratio with 2000 fixings (continuous limit 1/3)", np.minimum.outer(t_big, t_big).sum() / n_big**2 / T, 1 / 3, 5e-4)
    print()

    # 4. Lookbacks. Backs "Lookbacks", Example 6 and cards deriv-lookback-exact-sim, deriv-lookback-value.
    print("4. floating-strike lookbacks at inception")
    lc = lookback_float_call(S0, S0, T, R, Q, SIG)
    lp = lookback_float_put(S0, S0, T, R, Q, SIG)
    check("lookback call S_T - min (GSG)", lc, 17.2168, 5e-5)
    check("lookback put max - S_T (GSG)", lp, 14.2906, 5e-5)
    mc_c, se_c, mc_p, se_p = lookback_mc(1_000_000, seed=3)
    print(f"  exact-bridge MC call {mc_c:.4f} (se {se_c:.4f}), put {mc_p:.4f} (se {se_p:.4f})")
    assert abs(mc_c - lc) < 3.5 * se_c and abs(mc_p - lp) < 3.5 * se_p
    check("exact-bridge MC call", mc_c, 17.2220, 5e-5)
    check("exact-bridge MC put", mc_p, 14.2714, 5e-5)
    rng = np.random.default_rng(8)
    zz = rng.standard_normal((100_000, 252))
    x = np.cumsum((R - Q - 0.5 * SIG**2) / 252 + SIG * math.sqrt(1 / 252) * zz, axis=1)
    s_path = S0 * np.exp(x)
    daily_call = math.exp(-R * T) * (s_path[:, -1] - np.minimum(s_path.min(axis=1), S0))
    check("daily-monitored lookback call (MC)", daily_call.mean(), 16.6653, 5e-5)
    check("continuous minus daily lookback", lc - daily_call.mean(), 0.55, 0.005)
    check("exact-bridge MC call standard error", se_c, 0.0146, 5e-5)
    check("exact-bridge MC put standard error", se_p, 0.0098, 5e-5)
    print()

    # 5. Autocallable. Backs "Autocallables", Example 7 and cards deriv-autocall-structure, deriv-autocall-dealer-risk,
    #    deriv-autocall-coupon-illusion.
    print("5. autocallable: 3y, quarterly, trigger 100%, memory coupon, European knock-in 60%")
    rng = np.random.default_rng(21)
    n_obs = AC["years"] * AC["obs_per_year"]
    z = rng.standard_normal((400_000, n_obs))
    principal, coupons, k_call, st = autocall_legs(AC["sigma"], AC["q"], z)

    def fair_coupon(principal: np.ndarray, coupons: np.ndarray) -> tuple[float, float]:
        """Coupon that prices the note at par, and its delta-method standard error as a ratio of means."""
        c = float((100.0 - principal.mean()) / coupons.mean())
        se = float(np.std(100.0 - principal - c * coupons, ddof=1) / (math.sqrt(principal.size) * coupons.mean()))
        return c, se

    fair_c, se_fair = fair_coupon(principal, coupons)
    check("fair quarterly coupon (% of notional 100)", fair_c, 3.8805, 5e-5)
    check("fair quarterly coupon standard error", se_fair, 0.0165, 5e-5)
    principal2, coupons2, _, _ = autocall_legs(AC["sigma"], AC["q"], np.random.default_rng(22).standard_normal((400_000, n_obs)))
    fair_c2, se_fair2 = fair_coupon(principal2, coupons2)
    check("fair quarterly coupon, independent seed 22", fair_c2, 3.8950, 5e-5)
    assert abs(fair_c2 - fair_c) < 4 * math.hypot(se_fair, se_fair2), "seeds 21 and 22 disagree beyond 4 standard errors"
    check("fair coupon per annum (%)", 4 * fair_c, 15.52, 5e-3)
    check("fair coupon per annum (%), one decimal", 4 * fair_c, 15.5, 0.05)
    check("P(called at first observation)", float(np.mean(k_call == 1)), 0.4827, 5e-5)
    check("P(called by the end of year 1)", float(np.mean((k_call >= 1) & (k_call <= 4))), 0.7031, 5e-5)
    life = np.where(k_call > 0, k_call / AC["obs_per_year"], AC["years"])
    check("expected life (years)", float(life.mean()), 1.0328, 5e-5)
    loss = (k_call == 0) & (st < AC["ki"] * AC["S0"])
    check("P(capital loss at maturity)", float(loss.mean()), 0.0836, 5e-5)
    check("P(capital loss at maturity) in percent", 100 * float(loss.mean()), 8.36, 5e-3)
    avg_loss = float(100 - (100 * st[loss] / AC["S0"]).mean())
    check("expected loss given loss (% of notional)", avg_loss, 52.62, 5e-3)
    check("expected loss given loss, whole percent", avg_loss, 53, 0.5)

    # The knock-in put leg the dealer holds: pathwise, a higher dividend yield lowers every path (common z), which
    # removes early calls and lowers S_T, so the leg value rises.
    def ki_put(q: float) -> float:
        _, _, kc, s_t = autocall_legs(AC["sigma"], q, z)
        pay = np.where((kc == 0) & (s_t < AC["ki"] * AC["S0"]), 100.0 - 100.0 * s_t / AC["S0"], 0.0)
        return float(math.exp(-AC["r"] * AC["years"]) * pay.mean())

    assert ki_put(AC["q"] + 0.005) > ki_put(AC["q"] - 0.005), "knock-in put should gain value with dividends"
    print("  knock-in put leg rises with the dividend yield: ok")

    def note_pv(sigma: float, q: float) -> float:
        p_, c_, _, _ = autocall_legs(sigma, q, z)
        return float(p_.mean() + fair_c * c_.mean())

    vega_note = note_pv(AC["sigma"] + 0.01, AC["q"]) - note_pv(AC["sigma"] - 0.01, AC["q"])
    div_note = note_pv(AC["sigma"], AC["q"] + 0.005) - note_pv(AC["sigma"], AC["q"] - 0.005)
    check("note vega per vol point (investor, per 100)", vega_note / 2, -0.3982, 5e-5)
    check("note dividend sensitivity per 1% yield (investor)", div_note, -0.6843, 5e-5)
    print("  dealer (short the note) is therefore long vega and long dividends")
    print()

    # 6. Forward start and cliquet. Backs "Cliquets and forward starts", Example 8 and cards deriv-cliquet-forward-start,
    #    deriv-cliquet-forward-skew.
    print("6. forward start and cliquet")
    fs = forward_start_call(S0, 1.0, 2.0, R, Q, SIG)
    check("ATM forward-start call, set at 1y, expiring 2y (q = 0)", fs, 10.4506, 5e-5)
    rng = np.random.default_rng(9)
    zz = rng.standard_normal((1_000_000, 2))
    s1 = S0 * np.exp((R - 0.5 * SIG**2) + SIG * zz[:, 0])
    s2 = s1 * np.exp((R - 0.5 * SIG**2) + SIG * zz[:, 1])
    fs_pay = math.exp(-2 * R) * np.maximum(s2 - s1, 0.0)
    check("forward-start MC", float(fs_pay.mean()), 10.4368, 5e-5)
    check("forward-start MC standard error", float(fs_pay.std() / math.sqrt(len(fs_pay))), 0.0152, 5e-5)
    check("forward-start with q = 2%: e^{-q t1} times spot-start", forward_start_call(S0, 1.0, 2.0, R, 0.02, SIG), 9.0443, 5e-5)
    rng = np.random.default_rng(13)
    zc = rng.standard_normal((400_000, CLQ["n"]))
    with_floor, no_floor = cliquet_mc(SIG, zc)
    cf = cliquet_no_floor_closed_form(SIG)
    check("cliquet without global floor, closed form", cf, 1.1971, 5e-5)
    check("cliquet without global floor, MC", float(no_floor.mean()), 1.1976, 5e-5)
    se_nf = float(no_floor.std(ddof=1) / math.sqrt(len(no_floor)))
    assert abs(float(no_floor.mean()) - cf) < 2 * se_nf, ("strip closed form vs MC", cf, no_floor.mean(), se_nf)
    print("  strip closed form within two standard errors of its simulation: ok")
    check("cliquet with 2% global floor, MC", float(with_floor.mean()), 4.9459, 5e-5)
    check("value of the global floor", float(with_floor.mean() - no_floor.mean()), 3.7483, 5e-5)
    v_up = cliquet_mc(SIG + 0.01, zc)[0].mean()
    v_dn = cliquet_mc(SIG - 0.01, zc)[0].mean()
    check("cliquet vega per vol point (Black-Scholes)", float((v_up - v_dn) / 2), -0.0303, 5e-5)
    cf_up = cliquet_no_floor_closed_form(SIG + 0.01)
    cf_dn = cliquet_no_floor_closed_form(SIG - 0.01)
    check("vega of the locally capped/floored strip alone", (cf_up - cf_dn) / 2, -0.1299, 5e-5)
    check("vega of the global floor (difference)", float((v_up - v_dn) / 2) - (cf_up - cf_dn) / 2, 0.0996, 5e-5)


if __name__ == "__main__":
    main()
