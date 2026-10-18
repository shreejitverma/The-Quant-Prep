"""Liquidity and model risk: liquidity-adjusted VaR, liquidation horizons, Almgren-Chriss liquidation cost as a risk
number, a margin spiral, and two model-risk measurements (Black against Bachelier near zero prices, continuous against
discrete barrier monitoring).

Backs every number in 11-Risk-and-Trading/16-Liquidity-and-Model-Risk.md (and problems in 17-Risk-Problem-Set.md).
Inputs are labelled illustrative values, not market data.  Formulas: Bangia, Diebold, Schuermann and Stroughair (1999)
for the exogenous cost of liquidation; Almgren and Chriss (2000) for discrete-time optimal liquidation; Broadie,
Glasserman and Kou (1997) for the discrete-monitoring barrier shift.  Simulations use fixed seeds and are quoted
in the note as "about".

Run: python 11-Risk-and-Trading/code/risk_liquidity_model.py
"""

from __future__ import annotations

import math

import numpy as np

SQRT2 = math.sqrt(2.0)
Z99 = 2.3263478740408408


def check(label: str, value: float, expected: float, tol: float) -> float:
    """Print a value and assert it matches the literal quoted in the note to within tol (absolute)."""
    print(f"  {label}: {value:.10g}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, note quotes {expected} (tol {tol})"
    return value


def ncdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def npdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


# ---------------------------------------------------------------------------
# Worked example 1: exogenous liquidity cost and liquidation horizon (cards risk-liquidity-adjusted-var-formulation,
# risk-liquidation-horizon-variance-factor)
# ---------------------------------------------------------------------------


def horizon_variance_factor(days: int) -> float:
    """Variance of the liquidation P&L relative to one day's, selling 1/L of the position at the end of each day for L
    days with i.i.d. returns: sum_{k=1..L} ((L - k + 1) / L)^2 = (L + 1)(2L + 1) / (6L)."""
    return (days + 1) * (2 * days + 1) / (6.0 * days)


def section_lvar() -> None:
    print("\n[Worked example 1: 50m high-yield bond ETF position]")
    value, var1d, s_bar, s_sd = 50e6, 2.2e6, 0.008, 0.004
    col = 0.5 * value * (s_bar + Z99 * s_sd)
    check("relative spread at the 99% level, s_bar + z sigma_s", s_bar + Z99 * s_sd, 0.017305, 5e-7)
    check("cost of liquidation, half spread on 50m", col, 432_635, 1.0)
    check("exogenous L-VaR", var1d + col, 2_632_635, 1.0)
    check("COL as a share of VaR", col / var1d, 0.1967, 5e-5)
    for days, exp_f in ((4, 1.875), (16, 5.84375)):
        check(f"variance factor, L = {days}", horizon_variance_factor(days), exp_f, 1e-12)
    rng = np.random.default_rng(5)
    r = rng.standard_normal((1_000_000, 4))
    w = np.array([1.0, 0.75, 0.5, 0.25])
    sim_factor = float((r @ w).var(ddof=1))
    check("simulated variance factor, L = 4 (about)", sim_factor, 1.875, 0.006)
    m4 = math.sqrt(horizon_variance_factor(4))
    check("sd multiplier, L = 4", m4, 1.3693, 5e-5)
    check("sd multiplier, L = 16", math.sqrt(horizon_variance_factor(16)), 2.4174, 5e-5)
    # Two other conventions, each checked by simulating its own position path over the same returns
    hold_all = float((r @ np.ones(4)).var(ddof=1))
    t_fine = np.linspace(0.0, 1.0, 2001)
    w2 = (1.0 - t_fine) ** 2  # one full day, then continuous linear selling over L - 1 = 3 days (time in units of 3 days)
    cont_factor = 1.0 + 3.0 * float(np.sum(0.5 * (w2[1:] + w2[:-1]) * np.diff(t_fine)))
    check("simulated variance factor, whole position held 4 days (about)", hold_all, 4.0, 0.012)
    check("sd multiplier, first day full then continuous linear over 3 days", math.sqrt(cont_factor), 1.4142, 5e-5)
    check("horizon-scaled VaR, L = 4", var1d * m4, 3_012_474, 1.0)
    check("total L-VaR, L = 4", var1d * m4 + col, 3_445_109, 1.0)
    check("increase over 1-day VaR", (var1d * m4 + col) / var1d - 1.0, 0.5660, 5e-5)


# ---------------------------------------------------------------------------
# Worked example 2: Almgren-Chriss liquidation, cost distribution as a risk measure (cards risk-twap-vs-almgren-chriss-risk,
# risk-almgren-chriss-permanent-vs-temporary, risk-almgren-chriss-urgency-parameter, risk-lvar-almgren-chriss)
# ---------------------------------------------------------------------------

X0, T_DAYS, TAU, SIG = 1e6, 5, 1.0, 1.0  # shares, days, interval (days), dollars per share per sqrt(day)
GAMMA, ETA = 2.5e-7, 1e-6  # permanent ($/share per share), temporary ($/share per share/day)
ETA_T = ETA - 0.5 * GAMMA * TAU


def ac_holdings(lam: float) -> np.ndarray:
    """Discrete Almgren-Chriss holdings x_0..x_N: cosh(kappa tau) = 1 + kappa_tilde^2 tau^2 / 2, kappa_tilde^2 = lam sigma^2 / eta_tilde."""
    t = np.arange(T_DAYS + 1) * TAU
    if lam == 0.0:
        return X0 * (1.0 - t / (T_DAYS * TAU))
    kt2 = lam * SIG**2 / ETA_T
    kappa = math.acosh(1.0 + 0.5 * kt2 * TAU**2) / TAU
    return X0 * np.sinh(kappa * (T_DAYS * TAU - t)) / math.sinh(kappa * T_DAYS * TAU)


def ac_holdings_linear_system(lam: float) -> np.ndarray:
    """Same trajectory from the first-order conditions (eta_tilde / tau)(2 x_k - x_k-1 - x_k+1) + lam sigma^2 tau x_k = 0."""
    n = T_DAYS - 1
    a = np.zeros((n, n))
    rhs = np.zeros(n)
    c = ETA_T / TAU
    for i in range(n):
        a[i, i] = 2.0 * c + lam * SIG**2 * TAU
        if i > 0:
            a[i, i - 1] = -c
        if i < n - 1:
            a[i, i + 1] = -c
    rhs[0] = c * X0
    inner = np.linalg.solve(a, rhs)
    return np.concatenate([[X0], inner, [0.0]])


def ac_moments(x: np.ndarray) -> tuple[float, float]:
    """E[IS] = gamma X^2 / 2 + (eta_tilde / tau) sum n_k^2 (no fixed cost), Var[IS] = sigma^2 tau sum x_k^2."""
    n = -np.diff(x)
    return 0.5 * GAMMA * X0**2 + ETA_T / TAU * float(np.sum(n * n)), SIG**2 * TAU * float(np.sum(x[1:] ** 2))


def ac_simulate(x: np.ndarray, n_paths: int, seed: int) -> np.ndarray:
    """Implementation shortfall by simulation of the Almgren-Chriss price process (S0 = 50)."""
    rng = np.random.default_rng(seed)
    n = -np.diff(x)
    s = np.full(n_paths, 50.0)
    proceeds = np.zeros(n_paths)
    for k in range(len(n)):
        v = n[k] / TAU
        proceeds += n[k] * (s - ETA * v)  # sell n_k at S_{k-1} minus temporary impact
        s = s + SIG * math.sqrt(TAU) * rng.standard_normal(n_paths) - TAU * GAMMA * v
    return X0 * 50.0 - proceeds


def section_almgren_chriss() -> None:
    print("\n[Worked example 2: sell 1m shares over 5 days, daily intervals]")
    lam = 1e-6
    kt2 = lam * SIG**2 / ETA_T
    check("kappa_tilde^2", kt2, 1.142857, 5e-7)
    kappa = math.acosh(1.0 + 0.5 * kt2)
    check("kappa (per day), discrete", kappa, 1.0237, 5e-5)
    check("discrete kappa / continuous sqrt(lam sigma^2 / eta)", kappa / math.sqrt(lam * SIG**2 / ETA), 1.0237, 5e-5)
    x = ac_holdings(lam)
    x_lin = ac_holdings_linear_system(lam)
    check("max |sinh formula - linear system| (shares)", float(np.max(np.abs(x - x_lin))), 0.0, 1e-6)
    sold = -np.diff(x)
    for k in range(T_DAYS):
        print(f"  day {k + 1}: sell {sold[k]:,.0f}, hold {x[k + 1]:,.0f}")
    check("day 1 sale", sold[0], 640_841, 1.0)
    check("day 2 sale", sold[1], 230_374, 1.0)
    check("share sold in the first two days", (sold[0] + sold[1]) / X0, 0.8712, 5e-5)
    e_opt, v_opt = ac_moments(x)
    e_twap, v_twap = ac_moments(ac_holdings(0.0))
    x_now = np.array([X0, 0.0, 0.0, 0.0, 0.0, 0.0])
    e_now, v_now = ac_moments(x_now)
    perm = float(np.sum(-np.diff(x) * GAMMA * np.concatenate([[0.0], np.cumsum(-np.diff(x))[:-1]])))
    check(
        "permanent cost sum n_k gamma sum_{j<k} n_j, optimal schedule", perm, 0.5 * GAMMA * (X0**2 - float(np.sum(np.diff(x) ** 2))), 1e-6
    )
    check("1/2 gamma X^2", 0.5 * GAMMA * X0**2, 125_000, 1e-6)
    check("TWAP expected shortfall", e_twap, 300_000, 1e-6)
    check("TWAP shortfall sd", math.sqrt(v_twap), 1_095_445, 1.0)
    check("optimal expected shortfall", e_opt, 537_867, 1.0)
    check("optimal shortfall sd", math.sqrt(v_opt), 384_538, 1.0)
    check("immediate sale expected shortfall", e_now, 1_000_000, 1e-6)
    sim = ac_simulate(x, 200_000, seed=17)
    check("simulated mean shortfall, optimal (about)", float(sim.mean()), e_opt, 2_500)
    check("simulated sd, optimal (about)", float(sim.std(ddof=1)), math.sqrt(v_opt), 2_000)
    # Liquidation cost as a risk number: E[IS] + z99 sd[IS] along the efficient frontier
    risk = {name: e + Z99 * math.sqrt(v) for name, (e, v) in (("twap", (e_twap, v_twap)), ("opt", (e_opt, v_opt)), ("now", (e_now, v_now)))}
    check("E + z99 sd, TWAP", risk["twap"], 2_848_386, 1.0)
    check("E + z99 sd, lambda = 1e-6", risk["opt"], 1_432_436, 1.0)
    check("E + z99 sd, immediate sale", risk["now"], 1_000_000, 1e-6)
    lams = np.exp(np.linspace(math.log(1e-9), math.log(1e-3), 2001))
    vals = []
    for lv in lams:
        e, v = ac_moments(ac_holdings(float(lv)))
        vals.append(e + Z99 * math.sqrt(v))
    check("smallest E + z99 sd on the frontier for lambda up to 1e-3, minus immediate sale", min(vals) - risk["now"], 505, 1.0)


# ---------------------------------------------------------------------------
# Core concepts "Market and funding liquidity": a margin spiral (card risk-brunnermeier-pedersen-spiral, risk-spiral-amplification)
# ---------------------------------------------------------------------------


def spiral_iterate(q: float, p: float, debt: float, m: float, impact: float, shock: float) -> tuple[float, float]:
    """A fund holds q units at p financed with debt; its margin constraint is q p <= equity / m.  After an exogenous
    price drop it sells just enough to meet the constraint, each unit sold lowering the price by impact.  Iterate to the
    fixed point; return (total price fall, units sold)."""
    price = p - shock
    units = q
    for _ in range(10_000):
        equity = units * price - debt
        target = equity / (m * price)
        sell = units - target
        if sell <= 1e-9:
            break
        units -= sell
        debt -= sell * price  # proceeds repay debt (sold at the pre-impact price for simplicity)
        price -= impact * sell
    return p - price, q - units


def section_spiral() -> None:
    print("\n[Margin spiral: 1m units at 100, margin m, impact 1e-6 per unit sold, exogenous shock 1]")
    q, p, impact, shock = 1e6, 100.0, 1e-6, 1.0
    for m in (0.10, 0.05):
        debt = q * p * (1.0 - m)  # start exactly at the margin constraint
        amp_lin = 1.0 / (1.0 - impact * q * (1.0 / m - 1.0) / p)
        fall, sold = spiral_iterate(q, p, debt, m, impact, shock)
        print(f"  m = {m}: linearised amplification {amp_lin:.4f}, simulated total fall {fall:.4f}, units sold {sold:,.0f}")
        if m == 0.10:
            check("linearised amplification, m = 10%", amp_lin, 1.0989, 5e-5)
            check("simulated total price fall, m = 10%", fall, 1.0991, 5e-4)
        else:
            check("linearised amplification, m = 5%", amp_lin, 1.2346, 5e-5)
            check("simulated total price fall, m = 5%", fall, 1.2270, 5e-4)
    check("critical impact x Q / p for a spiral at m = 5% (1 / 19)", 1.0 / (1.0 / 0.05 - 1.0), 0.052632, 5e-7)


# ---------------------------------------------------------------------------
# Worked example 3: model risk near zero prices, Black against Bachelier (cards risk-negative-oil-options-failure,
# risk-model-reserve-black-bachelier)
# ---------------------------------------------------------------------------


def black_put(f: float, k: float, vol: float, t: float) -> float:
    if k <= 0.0:
        return 0.0  # a lognormal forward never goes below a non-positive strike
    u = vol * math.sqrt(t)
    d1 = (math.log(f / k) + 0.5 * u * u) / u
    return k * ncdf(-(d1 - u)) - f * ncdf(-d1)


def bachelier_put(f: float, k: float, nvol: float, t: float) -> float:
    u = nvol * math.sqrt(t)
    d = (f - k) / u
    return (k - f) * ncdf(-d) + u * npdf(d)


def section_black_bachelier() -> None:
    print("\n[Worked example 3: futures at 20, one month, Black vol 80%, Bachelier vol calibrated to the ATM price]")
    f, t, vol = 20.0, 1.0 / 12.0, 0.80
    atm = black_put(f, f, vol, t)
    lo, hi = 1.0, 50.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if bachelier_put(f, f, mid, t) < atm:
            lo = mid
        else:
            hi = mid
    nvol = 0.5 * (lo + hi)
    check("ATM put, Black", atm, 1.8390, 5e-4)
    check("calibrated Bachelier vol (dollars per year)", nvol, 15.97, 0.01)
    check("calibrated Bachelier vol / (F x sigma_Black)", nvol / (f * vol), 0.9978, 5e-5)
    for k, eb, en in ((10.0, 0.0012, 0.0245), (5.0, 0.0000, 0.0007), (0.0, 0.0, 0.0000)):
        b, n = black_put(f, k, vol, t), bachelier_put(f, k, nvol, t)
        print(f"  strike {k:>4}: Black {b:.4f}, Bachelier {n:.4f}")
        check(f"Black put, strike {k}", b, eb, 5e-5)
        check(f"Bachelier put, strike {k}", n, en, 5e-5)
    for f_low, exp_p in ((20.0, 0.000007), (5.0, 0.1390)):
        check(f"Bachelier P(F_T < 0) from F = {f_low}", ncdf(-f_low / (nvol * math.sqrt(t))), exp_p, 5e-5 if f_low < 10 else 5e-7)
    check("Bachelier put at strike 0 from F = 5", bachelier_put(5.0, 0.0, nvol, t), 0.3258, 5e-4)


# ---------------------------------------------------------------------------
# Worked example 4: implementation against term sheet, discrete barrier monitoring (cards risk-effective-challenge-definition,
# risk-barrier-monitoring-validation)
# ---------------------------------------------------------------------------


def down_and_out_call(s: float, k: float, h: float, r: float, vol: float, t: float) -> float:
    """Continuously monitored down-and-out call, h <= k, no dividends (same formula as risk_sensitivities.py)."""
    if s <= h:
        return 0.0
    u = vol * math.sqrt(t)
    lam = (r + 0.5 * vol * vol) / (vol * vol)
    y = math.log(h * h / (s * k)) / u + lam * u
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / u
    call = s * ncdf(d1) - k * math.exp(-r * t) * ncdf(d1 - u)
    c_di = s * (h / s) ** (2 * lam) * ncdf(y) - k * math.exp(-r * t) * (h / s) ** (2 * lam - 2) * ncdf(y - u)
    return call - c_di


def section_barrier_monitoring() -> None:
    print("\n[Worked example 4: down-and-out call S = K = 100, barrier 90, r = 5%, vol 20%, 1 year, daily closes]")
    s0, k, h, r, vol, t, steps = 100.0, 100.0, 90.0, 0.05, 0.20, 1.0, 252
    cont = down_and_out_call(s0, k, h, r, vol, t)
    beta = 0.5826  # -zeta(1/2) / sqrt(2 pi), Broadie, Glasserman and Kou (1997)
    h_shift = h * math.exp(-beta * vol * math.sqrt(t / steps))
    bgk = down_and_out_call(s0, k, h_shift, r, vol, t)
    rng = np.random.default_rng(31)
    n = 400_000
    dt = t / steps
    logs = np.full(n, math.log(s0))
    alive = np.ones(n, dtype=bool)
    lb = math.log(h)
    for _ in range(steps):
        logs += (r - 0.5 * vol * vol) * dt + vol * math.sqrt(dt) * rng.standard_normal(n)
        alive &= logs > lb
    st = np.exp(logs)
    call_pay = math.exp(-r * t) * np.maximum(st - k, 0.0)
    y = call_pay * alive
    d1 = (math.log(s0 / k) + (r + 0.5 * vol * vol) * t) / (vol * math.sqrt(t))
    call_exact = s0 * ncdf(d1) - k * math.exp(-r * t) * ncdf(d1 - vol * math.sqrt(t))
    cov = np.cov(y, call_pay)
    b = cov[0, 1] / cov[1, 1]
    cv = y - b * (call_pay - call_exact)
    est, se = float(cv.mean()), float(cv.std(ddof=1) / math.sqrt(n))
    check("continuous-monitoring closed form", cont, 8.6655, 5e-5)
    check("shifted barrier 90 exp(-0.5826 sigma sqrt(dt))", h_shift, 89.3418, 5e-4)
    check("BGK-corrected price", bgk, 8.9139, 5e-4)
    check("daily-monitoring Monte Carlo with control variate (about)", est, 8.912, 0.002)
    check("its standard error", se, 0.0084, 3e-4)
    check("model reserve if the system prices continuous monitoring", est - cont, 0.246, 0.002)
    assert abs(est - bgk) < 4 * se, "BGK correction and daily Monte Carlo disagree"


def main() -> None:
    section_lvar()
    section_almgren_chriss()
    section_spiral()
    section_black_bachelier()
    section_barrier_monitoring()
    print("\nAll liquidity and model risk checks passed.")


if __name__ == "__main__":
    main()
