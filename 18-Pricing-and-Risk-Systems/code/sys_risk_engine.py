"""Risk engine: sensitivities against full revaluation, VaR and ES conventions, aggregation, Euler allocation and sizing.

Backs every number in `18-Pricing-and-Risk-Systems/07-Risk-Engine.md`.
Books, P&L vectors, volatilities, correlations and platform sizes are labelled-hypothetical teaching inputs.
Random data use fixed seeds of Python's Mersenne Twister, so every platform prints the same values.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Where a result has a second, independent route (numerical integration against a closed form, a finite difference
against an analytic derivative, a brute-force quantile integral against an order-statistic formula), both are computed
and compared.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_risk_engine.py`.
"""

from __future__ import annotations

import math
import random

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure (half a unit in the last place)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


# ============================================================================
# 1. Sensitivities against full revaluation (Black-Scholes call book)
# ============================================================================


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def norm_ppf(p: float) -> float:
    """Inverse normal CDF by bisection on erf (exact to 1e-12, adequate for quantile constants)."""
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def bs_call(s: float, k: float, t: float, r: float, vol: float) -> float:
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / (vol * math.sqrt(t))
    d2 = d1 - vol * math.sqrt(t)
    return s * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d2)


def bs_delta_gamma(s: float, k: float, t: float, r: float, vol: float) -> tuple[float, float]:
    d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / (vol * math.sqrt(t))
    return norm_cdf(d1), norm_pdf(d1) / (s * vol * math.sqrt(t))


def call_by_integration(s: float, k: float, t: float, r: float, vol: float, n: int = 20_000) -> float:
    """Discounted expected call payoff under the lognormal law, by Simpson's rule in the normal variable.

    An independent route to the Black-Scholes price: no closed form, only the payoff and the density.
    """
    a, b = -10.0, 10.0
    h = (b - a) / n
    total = 0.0
    for i in range(n + 1):
        z = a + i * h
        st = s * math.exp((r - 0.5 * vol * vol) * t + vol * math.sqrt(t) * z)
        f = max(st - k, 0.0) * norm_pdf(z)
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        total += w * f
    return math.exp(-r * t) * total * h / 3.0


# ============================================================================
# 2. Historical-simulation VaR and ES conventions
# ============================================================================


def student_t_pnl(n: int, df: int, scale: float, seed: int) -> list[float]:
    """P&L draws from a Student-t with `df` degrees of freedom rescaled to standard deviation `scale`."""
    rng = random.Random(seed)
    unit = math.sqrt(df / (df - 2.0))
    out = []
    for _ in range(n):
        z = rng.gauss(0.0, 1.0)
        chi2 = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(df))
        out.append(scale * z / math.sqrt(chi2 / df) / unit)
    return out


def t_pdf(x: float, df: int) -> float:
    c = math.gamma((df + 1) / 2) / (math.sqrt(df * math.pi) * math.gamma(df / 2))
    return c * (1.0 + x * x / df) ** (-(df + 1) / 2)


def t4_quantile_closed_form(p: float) -> float:
    """Upper quantile of Student-t(4), p > 0.5, from the closed form of the four-degree-of-freedom CDF."""
    a = 4.0 * p * (1.0 - p)
    q = math.cos(math.acos(math.sqrt(a)) / 3.0) / math.sqrt(a)
    return 2.0 * math.sqrt(q - 1.0)


def simpson(f, a: float, b: float, n: int = 20_000) -> float:
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        total += (4 if i % 2 else 2) * f(a + i * h)
    return total * h / 3.0


def t4_quantile_numeric(p: float) -> float:
    """Quantile of Student-t(4) by bisection on the numerically integrated density."""
    lo, hi = 0.0, 50.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        cdf = 0.5 + simpson(lambda x: t_pdf(x, 4), 0.0, mid, 4_000)
        lo, hi = (mid, hi) if cdf < p else (lo, mid)
    return 0.5 * (lo + hi)


def discrete_var(dist: dict[float, float], alpha: float) -> float:
    """inf{l : P(L <= l) >= alpha} for a discrete loss distribution {loss: probability}."""
    cum = 0.0
    for loss in sorted(dist):
        cum += dist[loss]
        if cum >= alpha - 1e-12:
            return loss
    raise ValueError("probabilities do not reach alpha")


def discrete_es(dist: dict[float, float], alpha: float) -> float:
    """ES as (1 / (1 - alpha)) times the integral of the quantile function above alpha, piece by piece."""
    cum, total = 0.0, 0.0
    for loss in sorted(dist):
        lo, hi = cum, cum + dist[loss]
        total += loss * max(0.0, hi - max(lo, alpha))
        cum = hi
    return total / (1.0 - alpha)


def es_by_quantile_grid(dist: dict[float, float], alpha: float, n: int = 200_000) -> float:
    """Brute force: average the quantile function on a fine midpoint grid of u in (alpha, 1)."""
    total = 0.0
    for i in range(n):
        u = alpha + (i + 0.5) * (1.0 - alpha) / n
        total += discrete_var(dist, u)
    return total / n


def worst_losses(pnl: list[float]) -> list[float]:
    """Losses (negative P&L) sorted from worst to best."""
    return sorted((-x for x in pnl), reverse=True)


def var_kth_worst(pnl: list[float], k: int) -> float:
    return worst_losses(pnl)[k - 1]


def var_lower_quantile(pnl: list[float], alpha: float) -> float:
    """inf{l : F_L(l) >= alpha} on the empirical loss distribution: the ceil(n alpha)-th smallest loss."""
    losses = sorted(-x for x in pnl)
    return losses[math.ceil(len(losses) * alpha - 1e-12) - 1]


def var_lower_quantile_by_count(pnl: list[float], alpha: float) -> float:
    """Same quantile by scanning candidate losses and counting, with no sorting index arithmetic."""
    losses = [-x for x in pnl]
    n = len(losses)
    return min(c for c in losses if sum(1 for x in losses if x <= c) / n >= alpha - 1e-12)


def var_interpolated(pnl: list[float], alpha: float) -> float:
    """Linear interpolation between order statistics at position (n - 1) alpha (numpy's default 'linear')."""
    losses = sorted(-x for x in pnl)
    pos = (len(losses) - 1) * alpha
    lo = math.floor(pos)
    w = pos - lo
    return losses[lo] * (1 - w) + losses[min(lo + 1, len(losses) - 1)] * w


def tail_weights(n: int, alpha: float) -> list[float]:
    """Weights on the worst losses so that ES is the mean of the worst n (1 - alpha) observations, fractional last."""
    tail = n * (1.0 - alpha)
    full = math.floor(tail + 1e-12)
    w = [1.0 / tail] * full
    frac = tail - full
    if frac > 1e-12:
        w.append(frac / tail)
    return w


def es_fractional(pnl: list[float], alpha: float) -> float:
    losses = worst_losses(pnl)
    return sum(wi * li for wi, li in zip(tail_weights(len(pnl), alpha), losses, strict=False))


def tail_scenarios(pnl: list[float], alpha: float) -> list[tuple[int, float]]:
    """(scenario index, weight) for the ES tail of a P&L vector; ties broken by scenario index."""
    order = sorted(range(len(pnl)), key=lambda i: (pnl[i], i))
    return list(zip(order, tail_weights(len(pnl), alpha), strict=False))


# ============================================================================
# 3. Euler allocation (parametric) and correlated desk P&L vectors
# ============================================================================


def mat_vec(m: list[list[float]], v: list[float]) -> list[float]:
    return [sum(a * b for a, b in zip(row, v, strict=True)) for row in m]


def cholesky(m: list[list[float]]) -> list[list[float]]:
    n = len(m)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = m[i][j] - sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                assert s > 0.0, "matrix is not positive definite"
                low[i][j] = math.sqrt(s)
            else:
                low[i][j] = s / low[j][j]
    return low


DESK_SIGMA = [1.0e6, 0.8e6, 1.2e6]  # hypothetical one-day P&L standard deviations of three desks
DESK_CORR = [[1.0, 0.3, 0.5], [0.3, 1.0, -0.2], [0.5, -0.2, 1.0]]


def desk_cov() -> list[list[float]]:
    return [[DESK_CORR[i][j] * DESK_SIGMA[i] * DESK_SIGMA[j] for j in range(3)] for i in range(3)]


def parametric_var(weights: list[float], cov: list[list[float]], z: float) -> float:
    return z * math.sqrt(sum(w * x for w, x in zip(weights, mat_vec(cov, weights), strict=True)))


def correlated_desk_vectors(n: int, seed: int) -> list[list[float]]:
    """n scenarios of three desks' P&L: Student-t(4) shocks with the DESK_CORR correlation and DESK_SIGMA scales."""
    rng = random.Random(seed)
    low = cholesky(DESK_CORR)
    unit = math.sqrt(4 / 2.0)
    desks: list[list[float]] = [[], [], []]
    for _ in range(n):
        z = [rng.gauss(0.0, 1.0) for _ in range(3)]
        chi2 = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(4))
        scale = 1.0 / math.sqrt(chi2 / 4) / unit  # one common mixing variable: a multivariate t
        x = mat_vec(low, z)
        for d in range(3):
            desks[d].append(DESK_SIGMA[d] * x[d] * scale)
    return desks


# ============================================================================
# 4. Checks
# ============================================================================


def check_example_1() -> None:
    print("  Example 1: sensitivities against full revaluation (hypothetical short call book)")
    s0, k, t, r, vol, qty = 100.0, 100.0, 0.5, 0.03, 0.25, -10_000.0
    price = bs_call(s0, k, t, r, vol)
    assert abs(price - call_by_integration(s0, k, t, r, vol)) < 1e-6, "closed form disagrees with integration"
    quoted("single call price", price, 7.7603, 4)
    d, g = bs_delta_gamma(s0, k, t, r, vol)
    h = 1e-3  # central differences of the closed-form price, an independent route to the Greeks
    fd_delta = (bs_call(s0 + h, k, t, r, vol) - bs_call(s0 - h, k, t, r, vol)) / (2 * h)
    fd_gamma = (bs_call(s0 + h, k, t, r, vol) - 2 * price + bs_call(s0 - h, k, t, r, vol)) / (h * h)
    assert abs(fd_delta - d) < 1e-8 and abs(fd_gamma - g) < 1e-5
    quoted("single call delta", d, 0.56877, 5)
    quoted("single call gamma", g, 0.02223, 5)
    v0 = qty * price
    quoted("book delta (units of underlying)", qty * d, -5_688, 0)
    quoted("book gamma (per unit of spot squared)", qty * g, -222.3, 1)
    rows = {
        -0.25: (73_575, 142_192, 72_719, -69_473, 856),
        -0.10: (45_313, 56_877, 45_761, -11_116, -448),
        -0.01: (5_576, 5_688, 5_577, -111, -1),
        0.01: (-5_798, -5_688, -5_799, -111, 1),
        0.10: (-67_067, -56_877, -67_993, -11_116, 926),
        0.25: (-195_336, -142_192, -211_666, -69_473, 16_330),
    }
    full_by_shock = {}
    for shock, (full_q, delta_q, dg_q, gamma_q, err_q) in rows.items():
        ds = s0 * shock
        full = qty * bs_call(s0 + ds, k, t, r, vol) - v0
        full_by_shock[shock] = full
        delta_pnl = qty * d * ds
        gamma_pnl = 0.5 * qty * g * ds * ds
        dg = delta_pnl + gamma_pnl
        tag = f"{shock:+.0%}"
        quoted(f"spot {tag}: full revaluation P&L", full, full_q, 0)
        quoted(f"spot {tag}: delta P&L", delta_pnl, delta_q, 0)
        quoted(f"spot {tag}: delta-gamma P&L", dg, dg_q, 0)
        quoted(f"spot {tag}: gamma term", gamma_pnl, gamma_q, 0)
        quoted(f"spot {tag}: delta-gamma error (full minus approximation)", full - dg, err_q, 0)
    quoted("+25%: loss the delta-only estimate misses", -full_by_shock[0.25] - qty * d * -25.0, 53_144, 0)
    g125 = bs_delta_gamma(125.0, k, t, r, vol)[1]
    quoted("single call gamma at spot 125 (falls as the call goes into the money)", g125, 0.00644, 5)
    assert g125 < g, "gamma must fall from 100 to 125 for the quadratic to overstate the short book's loss"


def check_subadditivity() -> None:
    print("  Subadditivity: two independent defaultable bonds, 4% default probability, loss 100 each")
    p = 0.04
    single = {0.0: 1 - p, 100.0: p}
    one = discrete_var(single, 0.95)
    pair = {0.0: (1 - p) ** 2, 100.0: 2 * p * (1 - p), 200.0: p * p}
    # independent route to the pair distribution: enumerate the four default outcomes
    enum: dict[float, float] = {}
    for d1 in (0, 1):
        for d2 in (0, 1):
            pr = (p if d1 else 1 - p) * (p if d2 else 1 - p)
            enum[100.0 * (d1 + d2)] = enum.get(100.0 * (d1 + d2), 0.0) + pr
    assert all(abs(enum[x] - pair[x]) < 1e-15 for x in pair)
    quoted("probability that both survive", pair[0.0], 0.9216, 4)
    quoted("probability of exactly one default", pair[100.0], 0.0768, 4)
    quoted("probability of two defaults", pair[200.0], 0.0016, 4)
    quoted("probability that at least one of two defaults", pair[100.0] + pair[200.0], 0.0784, 4)
    two = discrete_var(pair, 0.95)
    quoted("95% VaR of each bond alone", one, 0, 0)
    quoted("95% VaR of the two together", two, 100, 0)
    assert two > 2 * one
    es_one, es_two = discrete_es(single, 0.95), discrete_es(pair, 0.95)
    assert abs(es_one - es_by_quantile_grid(single, 0.95)) < 1e-3
    assert abs(es_two - es_by_quantile_grid(pair, 0.95)) < 1e-3
    quoted("95% ES of each bond alone", es_one, 80.0, 1)
    quoted("95% ES of the two together", es_two, 103.2, 1)
    assert es_two <= 2 * es_one


def check_example_2() -> None:
    print("  Example 2: VaR and ES conventions on a 500-scenario P&L vector (Student-t 4 df, sd 1m, seed 7)")
    pnl = student_t_pnl(500, 4, 1.0e6, 7)
    worst = worst_losses(pnl)
    for i, q in enumerate((4_788_580, 4_163_702, 4_007_834, 3_798_897, 3_330_749, 3_072_109, 2_797_595), start=1):
        quoted(f"worst loss number {i}", worst[i - 1], q, 0)
    quoted("worst loss number 13", worst[12], 2_140_701, 0)
    quoted("99% VaR as the 5th worst loss", var_kth_worst(pnl, 5), 3_330_749, 0)
    lq = var_lower_quantile(pnl, 0.99)
    assert lq == var_lower_quantile_by_count(pnl, 0.99), "order-statistic index disagrees with counting"
    quoted("99% VaR as the lower quantile inf{l: F(l) >= 0.99} (6th worst)", lq, 3_072_109, 0)
    quoted("5th worst over 6th worst, minus 1 (%)", (var_kth_worst(pnl, 5) / lq - 1.0) * 100.0, 8.4, 1)
    quoted("99% VaR by linear interpolation at position 499 x 0.99", var_interpolated(pnl, 0.99), 3_074_695, 0)
    es = es_fractional(pnl, 0.975)
    quoted("97.5% ES: 12 worst plus half the 13th, over 12.5", es, 3_119_195, 0)
    quoted("97.5% ES as the mean of the 12 worst", sum(worst[:12]) / 12, 3_159_966, 0)
    quoted("97.5% ES as the mean of the 13 worst", sum(worst[:13]) / 13, 3_081_561, 0)
    quoted("normal-equivalent 99% VaR, 2.326 sd", norm_ppf(0.99) * 1.0e6, 2_326_348, 0)
    quoted("normal 99% VaR multiple of sd (card sys-07-02)", norm_ppf(0.99), 2.3263, 4)
    es_norm = norm_pdf(norm_ppf(0.975)) / 0.025
    es_norm_numeric = simpson(lambda x: x * norm_pdf(x), norm_ppf(0.975), 12.0) / 0.025
    assert abs(es_norm - es_norm_numeric) < 1e-9
    quoted("normal 97.5% ES multiple of sd (card sys-07-02)", es_norm, 2.3378, 4)
    quoted("normal-equivalent 97.5% ES, 1m sd", es_norm * 1.0e6, 2_337_803, 0)
    quoted("sample ES over normal ES, minus 1 (%)", (es / (es_norm * 1.0e6) - 1.0) * 100.0, 33.4, 1)
    # population Student-t(4) at unit standard deviation: closed form against numerical integration
    tq = t4_quantile_closed_form(0.975)
    assert abs(tq - t4_quantile_numeric(0.975)) < 1e-6
    es_t_closed = t_pdf(tq, 4) / 0.025 * (4 + tq * tq) / 3.0 * math.sqrt(0.5)
    es_t_numeric = simpson(lambda x: x * t_pdf(x, 4), tq, 2_000.0, 400_000) / 0.025 * math.sqrt(0.5)
    assert abs(es_t_closed - es_t_numeric) < 1e-4
    quoted("population t(4) 97.5% ES at unit sd", es_t_closed, 2.824, 3)
    quoted("population t(4) ES over normal ES, minus 1 (%)", (es_t_closed / es_norm - 1.0) * 100.0, 20.8, 1)


def check_example_3() -> None:
    print("  Example 3: Euler allocation, parametric (hypothetical three desks)")
    z99 = norm_ppf(0.99)
    cov = desk_cov()
    w = [1.0, 1.0, 1.0]
    sigma_p = math.sqrt(sum(a * b for a, b in zip(w, mat_vec(cov, w), strict=True)))
    var_p = z99 * sigma_p
    quoted("99% normal quantile", z99, 2.326348, 6)
    quoted("portfolio sd", sigma_p, 2_091_889, 0)
    quoted("portfolio 99% VaR", var_p, 4_866_462, 0)
    standalone = [z99 * s for s in DESK_SIGMA]
    for i, q in enumerate((2_326_348, 1_861_078, 2_791_617)):
        quoted(f"desk {i + 1} standalone 99% VaR", standalone[i], q, 0)
    quoted("sum of standalone VaRs", sum(standalone), 6_979_044, 0)
    quoted("diversification benefit", sum(standalone) - var_p, 2_112_582, 0)
    cw = mat_vec(cov, w)
    for i, q in enumerate((1.840, 0.688, 1.848)):
        quoted(f"Cov(desk {i + 1}, portfolio) in units of 10^12 dollars squared", cw[i] / 1e12, q, 3)
    comp = [z99 * w[i] * cw[i] / sigma_p for i in range(3)]
    for i, q in enumerate((2_046_227, 765_111, 2_055_124)):
        quoted(f"desk {i + 1} component VaR", comp[i], q, 0)
    # marginal VaR by central difference of the portfolio VaR, independent of the covariance formula
    h = 1e-6
    for i in range(3):
        up = [w[j] + (h if j == i else 0.0) for j in range(3)]
        dn = [w[j] - (h if j == i else 0.0) for j in range(3)]
        fd = (parametric_var(up, cov, z99) - parametric_var(dn, cov, z99)) / (2 * h)
        assert abs(fd - comp[i]) < 1e-3, "analytic marginal VaR disagrees with finite difference"
    marginal2 = z99 * cw[1] / sigma_p
    quoted("desk 2 marginal VaR per unit of scale", marginal2, 765_111, 0)
    w_new = [1.0, 1.1, 1.0]
    var_new = parametric_var(w_new, cov, z99)
    quoted("portfolio VaR with desk 2 scaled by 1.1", var_new, 4_945_883, 0)
    ivar = var_new - var_p
    quoted("incremental VaR of scaling desk 2 by 10%", ivar, 79_422, 0)
    quoted("marginal approximation 0.1 x marginal VaR", 0.1 * marginal2, 76_511, 0)
    quoted("approximation error relative to exact (%)", (1 - 0.1 * marginal2 / ivar) * 100.0, 3.7, 1)


def check_example_4() -> None:
    print("  Example 4: historical ES allocation and a what-if trade (multivariate t, 500 scenarios, seed 11)")
    desks = correlated_desk_vectors(500, 11)
    total = [sum(desks[dd][i] for dd in range(3)) for i in range(500)]
    es_total = es_fractional(total, 0.975)
    quoted("bank 97.5% ES from the summed vector", es_total, 4_429_179, 0)
    es_desks = [es_fractional(v, 0.975) for v in desks]
    quoted("sum of desk ES", sum(es_desks), 6_423_317, 0)
    tail = tail_scenarios(total, 0.975)
    comp_es = [-sum(wt * desks[dd][i] for i, wt in tail) for dd in range(3)]
    for i, q in enumerate((1_771_519, 1_216_433, 1_441_227)):
        quoted(f"desk {i + 1} ES contribution in the bank's tail scenarios", comp_es[i], q, 0)
    # Euler check: the contribution is the derivative of bank ES with respect to the desk's scale, re-sorted each time
    h = 1e-4
    for dd in range(3):
        up = [total[i] + h * desks[dd][i] for i in range(500)]
        dn = [total[i] - h * desks[dd][i] for i in range(500)]
        fd = (es_fractional(up, 0.975) - es_fractional(dn, 0.975)) / (2 * h)
        assert abs(fd - comp_es[dd]) < 1e-3, "ES contribution is not the Euler derivative"
    var_base = var_lower_quantile(total, 0.99)
    quoted("bank 99% VaR (lower quantile)", var_base, 4_385_198, 0)
    hedge = [-0.5 * x for x in desks[0]]  # a what-if trade whose P&L is minus half of desk 1 in every scenario
    var_new = var_lower_quantile([a + b for a, b in zip(total, hedge, strict=True)], 0.99)
    quoted("bank 99% VaR with the what-if hedge", var_new, 3_514_364, 0)
    quoted("incremental VaR of the hedge", var_new - var_base, -870_834, 0)


def check_example_5() -> None:
    print("  Example 5: storage sizing (hypothetical bank)")
    trades, scenarios = 400_000, 1_000
    quoted("trade-level P&L vectors per run, float64 (GB)", trades * scenarios * 8 / 1e9, 3.2, 1)
    quoted("same in float32 (GB)", trades * scenarios * 4 / 1e9, 1.6, 1)
    quoted("one year of daily runs at float64 (TB)", trades * scenarios * 8 * 250 / 1e12, 0.8, 1)
    nodes = 5_000 + 400 + 20 + 1
    quoted("hierarchy nodes (books, desks, divisions, entity)", nodes, 5_421, 0)
    quoted("node-level vectors per run (MB)", nodes * scenarios * 8 / 1e6, 43.4, 1)
    quoted("sparse sensitivities, 30 factors per trade at 12 bytes (MB)", trades * 30 * 12 / 1e6, 144, 0)


def run_tests() -> None:
    print("Risk engine checks")
    check_example_1()
    check_subadditivity()
    check_example_2()
    check_example_3()
    check_example_4()
    check_example_5()
    print(f"  {len(QUOTED)} numbers quoted in note 07 computed, printed and asserted")
    print("All risk engine checks passed.")


if __name__ == "__main__":
    run_tests()
