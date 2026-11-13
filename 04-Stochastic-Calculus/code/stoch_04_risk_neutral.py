"""Risk-neutral pricing and the FTAP: every price, probability and bound in the note.

Backs every number in `04-Stochastic-Calculus/04-Risk-Neutral-Pricing-and-FTAP.md`.
Independent routes used here:
- binomial prices by solving the replication equations in exact rationals and, separately, by the
  risk-neutral expectation;
- trinomial no-arbitrage bounds by enumerating martingale measures and, separately, by solving the
  super- and sub-replication linear programs exactly (vertex enumeration in rationals);
- digital, asset-or-nothing and call prices by quadrature of the lognormal density, by seeded
  simulation under Q, and by simulation under the share measure (log drift r + sigma^2/2);
- the real-world expectation discounted at mu by quadrature, and the deflator price by simulation under P;
- the power claim by quadrature and simulation; the Breeden-Litzenberger butterfly by finite differences of
  Black-Scholes prices against the lognormal density.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 04-Stochastic-Calculus/code/stoch_04_risk_neutral.py`.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

import numpy as np

SEED = 20261115
S0, K, T, R, SIG, MU = 100.0, 105.0, 0.5, 0.05, 0.25, 0.15


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, se: float, target: float, k: float = 4.0) -> None:
    """Assert a seeded Monte Carlo estimate is within k standard errors of an independently computed target."""
    assert abs(estimate - target) <= k * se, f"{label}: simulated {estimate!r} +/- {se:.2g}, target {target}"
    print(f"    {label} ~ {estimate:.4f} (se {se:.1e}, target {target:.4f}, tolerance {k:g} se)")


def ncdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def mean_se(x: np.ndarray) -> tuple[float, float]:
    return float(x.mean()), float(x.std(ddof=1) / math.sqrt(x.size))


def bs_call(s: float, k: float, t: float, r: float, sig: float) -> float:
    d1 = (math.log(s / k) + (r + 0.5 * sig**2) * t) / (sig * math.sqrt(t))
    return s * ncdf(d1) - k * math.exp(-r * t) * ncdf(d1 - sig * math.sqrt(t))


def expect(g, drift: float, above: float | None = None, below: float | None = None) -> float:
    """E[g(S_T)] for S_T = S0 exp(drift T + sigma sqrt(T) z), z ~ N(0, 1), by the trapezoid rule in z.

    ``above``/``below`` restrict to S_T > above or S_T < below by moving the end of the z grid to that
    level, so an indicator payoff has no kink inside the grid.
    """
    sd = SIG * math.sqrt(T)
    lo = -12.0 if above is None else (math.log(above / S0) - drift * T) / sd
    hi = 12.0 if below is None else (math.log(below / S0) - drift * T) / sd
    z = np.linspace(lo, hi, 1_200_001)
    st = S0 * np.exp(drift * T + sd * z)
    y = g(st) * np.exp(-0.5 * z**2) / math.sqrt(2 * math.pi)
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(z)))


def one(s: np.ndarray) -> np.ndarray:
    return np.ones_like(s)


def binomial() -> None:
    print("One-period binomial call: 100 -> 120 or 90, rate 0, strike 100 (cards sc-rn-binomial-q, sc-rn-binomial-call-price)")
    su, sd, vu, vd, gross = Fraction(120), Fraction(90), Fraction(20), Fraction(0), Fraction(1)
    # replication: delta su + B gross = vu, delta sd + B gross = vd (Cramer's rule)
    det = su * gross - sd * gross
    delta = (vu * gross - vd * gross) / det
    cash = (su * vd - sd * vu) / det
    exact("delta", delta, Fraction(2, 3))
    exact("cash B", cash, Fraction(-60))
    price = delta * 100 + cash
    exact("replication price", price, Fraction(20, 3))
    approx("    as a decimal", float(price), 6.67, 2)
    q = (gross - Fraction(9, 10)) / (Fraction(12, 10) - Fraction(9, 10))
    exact("q = (1 - 0.9)/(1.2 - 0.9)", q, Fraction(1, 3))
    exact("risk-neutral price q * 20 / R", (q * vu + (1 - q) * vd) / gross, price)
    exact("q makes the stock a martingale: q 120 + (1 - q) 90", q * su + (1 - q) * sd, Fraction(100))
    believer = Fraction(9, 10) * vu
    exact("quote at belief p = 0.9", believer, Fraction(18))
    profit = believer - price
    exact("locked-in profit 18 - 20/3", profit, Fraction(34, 3))
    approx("    as a decimal", float(profit), 11.33, 2)
    for state, s_t, payoff in (("up", su, vu), ("down", sd, vd)):  # sell call, buy delta shares, borrow 60: zero in each state
        hedge = delta * s_t + cash
        assert hedge - payoff == 0, state
    print("    sold call plus 2/3 shares minus 60 cash is worth 0 in both states, so 11.33 is kept in every state")
    for u, d, gr in itertools.product(
        (Fraction(11, 10), Fraction(13, 10)),
        (Fraction(8, 10), Fraction(1)),
        (Fraction(9, 10), Fraction(1), Fraction(21, 20), Fraction(12, 10)),
    ):
        qq = (gr - d) / (u - d)
        assert (d < gr < u) == (0 < qq < 1)
    print("    d < R < u iff 0 < q < 1, checked on a grid of (u, d, R)")


def trinomial() -> None:
    print("Trinomial: 100 -> 120, 100 or 90, rate 0, call strike 100 (card sc-rn-trinomial-bounds, worked example)")
    states = [Fraction(120), Fraction(100), Fraction(90)]
    payoff = [Fraction(20), Fraction(0), Fraction(0)]
    prices = []
    for i in range(1, 300):
        qu = Fraction(i, 900)
        qd, qm = 2 * qu, 1 - 3 * qu
        assert qu * 120 + qm * 100 + qd * 90 == 100 and qu + qm + qd == 1
        prices.append(qu * 20)
    exact("q_d = 2 q_u and q_m = 1 - 3 q_u satisfy both constraints", True, True)
    exact("largest price on the grid q_u < 1/3", max(prices), Fraction(299 * 20, 900))
    exact("smallest price on the grid q_u > 0", min(prices), Fraction(20, 900))

    def lp_vertices(sign: int) -> Fraction:
        """Min (sign = 1) or max (sign = -1) of 100 a + b with sign (a s_j + b - payoff_j) >= 0 in every state."""
        best = None
        for i, j in itertools.combinations(range(3), 2):
            a = (payoff[i] - payoff[j]) / (states[i] - states[j])
            b = payoff[i] - a * states[i]
            if all(sign * (a * s + b - p) >= 0 for s, p in zip(states, payoff, strict=True)):
                cost = 100 * a + b
                if best is None or sign * (cost - best) < 0:
                    best = cost
        assert best is not None
        return best

    sup = lp_vertices(1)
    exact("super-replication cost (LP)", sup, Fraction(20, 3))
    exact("sub-replication value (LP)", lp_vertices(-1), Fraction(0))
    a, b = Fraction(2, 3), Fraction(-60)
    exact("super-replicating portfolio payoffs 2/3 S - 60", [a * s + b for s in states], [Fraction(20), Fraction(20, 3), Fraction(0)])
    approx("    middle payoff", float(a * 100 + b), 6.67, 2)


def numeraire_prices(rng: np.random.Generator) -> None:
    print(
        "Digital and asset-or-nothing, S0 = 100, K = 105, T = 0.5, r = 5%, sigma = 25% (cards sc-rn-digital-price, sc-rn-share-measure-nd1)"
    )
    disc = math.exp(-R * T)
    d1 = (math.log(S0 / K) + (R + 0.5 * SIG**2) * T) / (SIG * math.sqrt(T))
    d2 = d1 - SIG * math.sqrt(T)
    digital_q = disc * expect(one, R - 0.5 * SIG**2, above=K)
    approx("cash-or-nothing by quadrature under Q", digital_q, 0.4016, 4)
    approx("    and e^{-rT} N(d2)", disc * ncdf(d2), digital_q, 8)
    aon_q = disc * expect(lambda s: s, R - 0.5 * SIG**2, above=K)
    aon_s = S0 * expect(one, R + 0.5 * SIG**2, above=K)  # share measure: log drift r + sigma^2/2
    approx("asset-or-nothing by quadrature under Q", aon_q, 48.16, 2)
    approx("    and S0 Q^S(S_T > K) under the share measure", aon_s, aon_q, 8)
    approx("    and S0 N(d1)", S0 * ncdf(d1), aon_q, 8)
    call = aon_q - K * digital_q
    approx("call = 48.16 - 105 x 0.4016", call, 5.99, 2)
    approx("    and the Black-Scholes formula", bs_call(S0, K, T, R, SIG), call, 8)
    approx("Q(S_T > K) = N(d2)", ncdf(d2), 0.412, 3)
    p_itm = expect(one, MU - 0.5 * SIG**2, above=K)
    approx("P(S_T > K) with mu = 15%", p_itm, 0.524, 3)
    for lo in (80.0, 90.0):
        qp = expect(one, R - 0.5 * SIG**2, below=lo)
        pp = expect(one, MU - 0.5 * SIG**2, below=lo)
        approx(f"Q(S_T < {lo:g})", qp, {80.0: 0.094, 90.0: 0.258}[lo], 3)
        approx(f"P(S_T < {lo:g})", pp, {80.0: 0.055, 90.0: 0.176}[lo], 3)
    wrong = math.exp(-MU * T) * expect(lambda s: s - K, MU - 0.5 * SIG**2, above=K)
    approx("E^P[payoff] discounted at mu (wrong)", wrong, 8.32, 2)
    lam = (MU - R) / SIG
    approx("market price of risk lambda", lam, 0.4, 12)
    n = 4_000_000
    w = rng.standard_normal(n) * math.sqrt(T)
    st = S0 * np.exp((MU - 0.5 * SIG**2) * T + SIG * w)  # P-paths
    zq = np.exp(-lam * w - 0.5 * lam**2 * T)
    m, se = mean_se(zq)
    simulated("E^P[dQ/dP] (exact 1)", m, se, 1.0)
    m, se = mean_se(disc * zq * np.maximum(st - K, 0.0))
    simulated("deflator price E^P[e^{-rT} dQ/dP payoff], 4e6 P-paths", m, se, call)
    approx("    the simulated deflator price quoted in the note (seed above)", m, 5.995, 3)
    approx("    its standard error", se, 0.004, 3)
    assert abs(m - call) <= 2 * se, "the note says within two standard errors of the formula price"
    wq = rng.standard_normal(n) * math.sqrt(T)
    sq = S0 * np.exp((R - 0.5 * SIG**2) * T + SIG * wq)
    m, se = mean_se(disc * np.maximum(sq - K, 0.0))
    simulated("call by simulation under Q", m, se, call)
    m, se = mean_se(sq)
    simulated("E^Q[S_T] vs the forward S0 e^{rT}", m, se, S0 * math.exp(R * T))
    approx("forward S0 e^{rT}", S0 * math.exp(R * T), 102.53, 2)


def power_claim(rng: np.random.Generator) -> None:
    print("Power claim S_T^2 (worked example)")
    disc = math.exp(-R * T)
    quad = disc * expect(lambda s: s**2, R - 0.5 * SIG**2)
    approx("e^{-rT} E^Q[S_T^2] by quadrature", quad, 10578.6, 1)
    approx("    and S0^2 e^{(r + sigma^2) T} = 1e4 e^{0.05625}", 1e4 * math.exp(0.05625), quad, 6)
    approx("(0.05 + 0.0625) x 0.5", (R + SIG**2) * T, 0.05625, 12)
    approx("S0^2 grown at r, e^{-rT} (S0 e^{rT})^2, smaller by convexity", disc * (S0 * math.exp(R * T)) ** 2, 10253.2, 1)
    w = rng.standard_normal(2_000_000) * math.sqrt(T)
    sq = S0 * np.exp((R - 0.5 * SIG**2) * T + SIG * w)
    m, se = mean_se(disc * sq**2)
    simulated("e^{-rT} E^Q[S_T^2] by simulation", m, se, quad)


def breeden_litzenberger() -> None:
    print("Breeden-Litzenberger butterfly at K = 105, wings +/- 1 (card sc-rn-breeden-litzenberger)")
    h = 1.0
    fly = bs_call(S0, K - h, T, R, SIG) - 2 * bs_call(S0, K, T, R, SIG) + bs_call(S0, K + h, T, R, SIG)
    m_log, s_log = math.log(S0) + (R - 0.5 * SIG**2) * T, SIG * math.sqrt(T)
    dens = math.exp(-((math.log(K) - m_log) ** 2) / (2 * s_log**2)) / (K * s_log * math.sqrt(2 * math.pi))
    approx("risk-neutral density q_T(105)", dens, 0.02097, 5)
    approx("h^2 e^{-rT} q_T(105)", h * h * math.exp(-R * T) * dens, 0.02045, 5)
    approx("butterfly C(104) - 2 C(105) + C(106)", fly, 0.02044, 5)


def main() -> None:
    rng = np.random.default_rng(SEED)
    binomial()
    trinomial()
    numeraire_prices(rng)
    power_claim(rng)
    breeden_litzenberger()
    print("all risk-neutral pricing checks passed")


if __name__ == "__main__":
    main()
