"""Monte Carlo pricing and variance reduction: every number in 10-Monte-Carlo-Pricing-and-Variance-Reduction.md.

Independent routes used here:
- population quantities (standard deviation of the discounted payoff, the antithetic correlation, the optimal
  control coefficient and its correlation, importance-sampling and likelihood-ratio variances) by Gauss-Legendre
  quadrature of the payoff against the normal density, split at the kinks, cross-checked where possible against
  closed-form lognormal moments (Black-Scholes prices come from ``pricing_core`` and are re-derived by quadrature);
- every efficiency ratio as a ratio of those exact variances, then confirmed by a seeded simulation whose
  estimate must sit within a stated multiple of its own standard error;
- the Bermudan put benchmark by a 5,000-step CRR binomial tree with exercise only on the 50 dates (and the
  2,500- and 10,000-step trees as a convergence check), against Longstaff-Schwartz by simulation;
- the Broadie-Glasserman-Kou constant from zeta(1/2) summed through the alternating eta series, not recalled.

Seeds: 42 for the Example 3 snippet, 0 to 19 for Longstaff-Schwartz, SEED_IS, SEED_GREEKS and SEED_ASIAN below.
Every quoted number is printed as ``label = value`` and asserted at the rounding the note quotes.
Run from the repo root: uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/deriv_10_monte_carlo.py
"""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np
from pricing_core import bs_price, norm_cdf, norm_pdf

S0, K, T, R, SIG = 100.0, 100.0, 1.0, 0.05, 0.20
N_PATHS = 100_000
SEED_SNIPPET = 42  # the Example 3 code block
SEED_IS = 7  # Example 4
SEED_GREEKS = 3  # Example 6
SEED_ASIAN = 5  # geometric control for the arithmetic Asian
DISC = math.exp(-R * T)
SD = SIG * math.sqrt(T)


def q(label: str, value: float, quoted: str) -> float:
    """Print a value and assert it rounds to the literal the note quotes."""
    decimals = len(quoted.split(".")[1]) if "." in quoted else 0
    tol = 0.5 * 10.0**-decimals * (1 + 1e-9)
    print(f"    {label} = {value:.8f}  (quoted {quoted})")
    assert abs(value - float(quoted.replace(",", ""))) <= tol, f"{label}: {value} does not round to {quoted}"
    return value


def close(label: str, a: float, b: float, tol: float) -> None:
    """Assert agreement between two independent routes."""
    print(f"      check {label}: |{a:.6g} - {b:.6g}| = {abs(a - b):.2e} <= {tol:.1e}")
    assert abs(a - b) <= tol, f"{label}: {a} vs {b}"


_X, _W = np.polynomial.legendre.leggauss(200)


def normal_expect(f: Callable[[np.ndarray], np.ndarray], kinks: tuple[float, ...] = ()) -> float:
    """E[f(Z)] for Z ~ N(0, 1) by Gauss-Legendre on [-12, 12], split at the payoff kinks (in z)."""
    pts = [-12.0, *sorted(k for k in kinks if -12 < k < 12), 12.0]
    total = 0.0
    for lo, hi in zip(pts[:-1], pts[1:], strict=True):
        z = 0.5 * (hi - lo) * _X + 0.5 * (hi + lo)
        total += 0.5 * (hi - lo) * float(np.sum(_W * f(z) * np.exp(-0.5 * z * z))) / math.sqrt(2 * math.pi)
    return total


def s_t(z: np.ndarray, s0: float = S0) -> np.ndarray:
    return s0 * np.exp((R - 0.5 * SIG**2) * T + SD * z)


def z_of_strike(k: float) -> float:
    """The normal draw at which S_T = k."""
    return (math.log(k / S0) - (R - 0.5 * SIG**2) * T) / SD


def call_y(z: np.ndarray, k: float = K) -> np.ndarray:
    return DISC * np.maximum(s_t(z) - k, 0.0)


def lsm_american_put(S0, K, r, sigma, T, steps=50, paths=100_000, seed=0):
    """Longstaff-Schwartz with basis 1, x, x^2 on in-the-money paths (the note's snippet, verbatim)."""
    rng = np.random.default_rng(seed)
    dt = T / steps
    z = rng.standard_normal((paths // 2, steps))
    z = np.vstack([z, -z])  # antithetic pairs
    S = S0 * np.exp(np.cumsum((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z, axis=1))
    cash = np.maximum(K - S[:, -1], 0.0)  # value if held to expiry
    for t in range(steps - 2, -1, -1):
        cash *= np.exp(-r * dt)  # discount one step back to t
        itm = K - S[:, t] > 0
        x = S[itm, t] / K
        coef = np.polyfit(x, cash[itm], 2)  # regress continuation value
        exercise = K - S[itm, t] > np.polyval(coef, x)
        idx = np.flatnonzero(itm)[exercise]
        cash[idx] = K - S[idx, t]
    cash *= np.exp(-r * dt)
    pairs = 0.5 * (cash[: paths // 2] + cash[paths // 2 :])  # antithetic pairs are the iid units
    price = max(pairs.mean(), K - S0)
    return price, pairs.std(ddof=1) / np.sqrt(len(pairs))


def lsm_out_of_sample(S0, K, r, sigma, T, steps=50, paths=100_000, seed=0) -> tuple[float, float]:
    """Fit the exercise rule on one set of paths and price it on an independent set: a true lower bound."""
    dt = T / steps

    def paths_for(s: int) -> np.ndarray:
        z = np.random.default_rng(s).standard_normal((paths, steps))
        return S0 * np.exp(np.cumsum((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z, axis=1))

    S = paths_for(seed)
    cash = np.maximum(K - S[:, -1], 0.0)
    coefs = {}
    for t in range(steps - 2, -1, -1):
        cash *= np.exp(-r * dt)
        itm = K - S[:, t] > 0
        x = S[itm, t] / K
        coefs[t] = np.polyfit(x, cash[itm], 2)
        exercise = K - S[itm, t] > np.polyval(coefs[t], x)
        idx = np.flatnonzero(itm)[exercise]
        cash[idx] = K - S[idx, t]
    S = paths_for(seed + 1000)
    value = np.zeros(paths)
    alive = np.ones(paths, dtype=bool)
    for t in range(steps - 1):
        intrinsic = K - S[:, t]
        stop = alive & (intrinsic > 0) & (intrinsic > np.polyval(coefs[t], S[:, t] / K))
        value[stop] = intrinsic[stop] * math.exp(-r * dt * (t + 1))
        alive &= ~stop
    value[alive] = np.maximum(K - S[alive, -1], 0.0) * math.exp(-r * T)
    return float(value.mean()), float(value.std(ddof=1) / math.sqrt(paths))


def crr_put(S0, K, r, sigma, T, n, exercise_every: int | None) -> float:
    """CRR binomial put; exercise allowed every `exercise_every` steps (None for every step, i.e. American)."""
    dt = T / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    df = math.exp(-r * dt)
    j = np.arange(n + 1)
    V = np.maximum(K - S0 * u ** (n - j) * d**j, 0.0)
    for i in range(n - 1, 0, -1):
        V = df * (p * V[:-1] + (1 - p) * V[1:])
        if exercise_every is None or i % exercise_every == 0:
            jj = np.arange(i + 1)
            V = np.maximum(V, K - S0 * u ** (i - jj) * d**jj)
    return float(df * (p * V[0] + (1 - p) * V[1]))


def zeta_half() -> float:
    """zeta(1/2) = eta(1/2) / (1 - sqrt 2), eta summed by repeated averaging of alternating partial sums."""
    terms = [(-1) ** (n + 1) / math.sqrt(n) for n in range(1, 41)]
    sums = list(np.cumsum(terms))
    for _ in range(30):  # Euler transform of the partial sums
        sums = [0.5 * (a + b) for a, b in zip(sums[:-1], sums[1:], strict=True)]
    return sums[-1] / (1 - math.sqrt(2))


def main() -> None:
    print("Setup: S0 = K = 100, T = 1, r = 5%, sigma = 20%")
    bs = q("Black-Scholes call", bs_price(S0, K, T, R, SIG), "10.4506")
    zk = z_of_strike(K)
    close("call by quadrature vs closed form", normal_expect(call_y, (zk,)), bs, 1e-9)

    print("Example 1: error bars and the path budget")
    m2 = normal_expect(lambda z: call_y(z) ** 2, (zk,))
    s = math.sqrt(m2 - bs**2)
    # closed-form second moment: E[(S-K)^2 1{S>K}] from lognormal moments, a separate route to s
    F = S0 * math.exp(R * T)
    d1 = math.log(F / K) / SD + 0.5 * SD
    d2 = d1 - SD
    m2_cf = DISC**2 * (F**2 * math.exp(SD**2) * norm_cdf(d1 + SD) - 2 * K * F * norm_cdf(d1) + K * K * norm_cdf(d2))
    close("second moment, quadrature vs lognormal moments", m2, m2_cf, 1e-8)
    q("standard deviation of the discounted payoff s", s, "14.72")
    q("standard error, N = 100,000", s / math.sqrt(N_PATHS), "0.0465")
    q("95% half-width", 1.96 * s / math.sqrt(N_PATHS), "0.091")
    q("paths for a 1-cent 95% half-width (millions)", (1.96 * s / 0.01) ** 2 / 1e6, "8.3")

    print("Example 2: antithetic variates")
    rho_a = (normal_expect(lambda z: call_y(z) * call_y(-z), (zk, -zk)) - bs**2) / s**2
    q("corr(Y(Z), Y(-Z))", rho_a, "-0.50")
    q("pair variance relative to two independent paths, 1 + rho", 1 + rho_a, "0.50")
    hw_anti = 1.96 * math.sqrt(s**2 * (1 + rho_a) / 2 / N_PATHS)
    q("95% half-width, 100,000 pairs", hw_anti, "0.046")
    # a straddle is symmetric near the money, so the pair correlation turns positive
    strad = lambda z: DISC * np.abs(s_t(z) - K)  # noqa: E731
    m_s = normal_expect(strad, (zk,))
    v_s = normal_expect(lambda z: strad(z) ** 2, (zk,)) - m_s**2
    rho_strad = (normal_expect(lambda z: strad(z) * strad(-z), (zk, -zk)) - m_s**2) / v_s
    print(f"    straddle corr(Y(Z), Y(-Z)) = {rho_strad:.4f}")
    assert rho_strad > 0, rho_strad

    print("Example 3: discounted terminal price as a control variate (exact by quadrature)")
    xz = lambda z: DISC * s_t(z)  # noqa: E731
    cov_xy = normal_expect(lambda z: call_y(z) * xz(z), (zk,)) - bs * S0
    var_x = normal_expect(lambda z: xz(z) ** 2) - S0**2
    close("Var(X) by quadrature vs S0^2 (exp(sigma^2 T) - 1)", var_x, S0**2 * math.expm1(SIG**2 * T), 1e-7)
    b_star = q("optimal b* = Cov(Y, X) / Var(X)", cov_xy / var_x, "0.674")
    q("Black-Scholes delta N(d1)", norm_cdf(d1), "0.637")
    q("Black-Scholes delta N(d1), four decimals", norm_cdf(d1), "0.6368")
    rho_cv = q("corr(Y, X)", cov_xy / math.sqrt(s**2 * var_x), "0.925")
    q("corr(Y, X), two decimals (card)", rho_cv, "0.92")
    q("residual variance fraction 1 - rho^2", 1 - rho_cv**2, "0.145")
    q("variance removed (card, %)", 100 * rho_cv**2, "85")
    q("variance reduction factor 1 / (1 - rho^2)", 1 / (1 - rho_cv**2), "6.9")
    print(f"  Seeded snippet, seed {SEED_SNIPPET}")
    rng = np.random.default_rng(SEED_SNIPPET)
    z = rng.standard_normal(N_PATHS)
    plain = call_y(z)
    anti = 0.5 * (plain + call_y(-z))
    X = xz(z)
    b = float(np.cov(plain, X)[0, 1] / np.var(X, ddof=1))
    cv = plain - b * (X - S0)
    for name, y, qm, qh, exact_var in (
        ("plain", plain, "10.4205", "0.0917", s**2),
        ("antithetic", anti, "10.4763", "0.0459", s**2 * (1 + rho_a) / 2),
        ("control", cv, "10.4668", "0.0350", s**2 * (1 - rho_cv**2)),
    ):
        se = float(y.std(ddof=1)) / math.sqrt(len(y))
        q(f"{name} estimate", float(y.mean()), qm)
        q(f"{name} 95% half-width", 1.96 * se, qh)
        close(f"{name} estimate within 3 standard errors of Black-Scholes", float(y.mean()), bs, 3 * math.sqrt(exact_var / N_PATHS))
    q("plain estimate, two decimals", float(plain.mean()), "10.42")
    q("plain half-width, three decimals", 1.96 * float(plain.std(ddof=1)) / math.sqrt(N_PATHS), "0.092")
    q("control estimate, three decimals", float(cv.mean()), "10.467")
    q("control half-width, three decimals", 1.96 * float(cv.std(ddof=1)) / math.sqrt(N_PATHS), "0.035")
    q("sample b-hat", b, "0.674")
    close("sample b-hat within 0.005 of b*", b, b_star, 0.005)

    print("Example 4: importance sampling for the 160 call")
    k_otm = 160.0
    c_otm = q("Black-Scholes 160 call", bs_price(S0, k_otm, T, R, SIG), "0.1590")
    z160 = z_of_strike(k_otm)
    close("160 call by quadrature", normal_expect(lambda z: call_y(z, k_otm), (z160,)), c_otm, 1e-10)
    q("P(S_T > 160) (%)", 100 * norm_cdf(-z160), "1.4")
    v_plain = normal_expect(lambda z: call_y(z, k_otm) ** 2, (z160,)) - c_otm**2
    se_plain = q("plain standard error, 100,000 paths", math.sqrt(v_plain / N_PATHS), "0.0059")
    q("plain relative error (%)", 100 * se_plain / c_otm, "3.7")
    mu = q("shift mu", z160, "2.20")
    # Under the shifted sampler the estimator is Y(Z) w(Z) with w = exp(-mu Z + mu^2 / 2) and Z ~ N(mu, 1);
    # its second moment is E_f[Y^2 w], which quadrature evaluates under the original density.
    v_is = normal_expect(lambda z: call_y(z, k_otm) ** 2 * np.exp(-mu * z + 0.5 * mu * mu), (z160,)) - c_otm**2
    se_is = q("importance-sampled standard error", math.sqrt(v_is / N_PATHS), "0.00059")
    ratio = q("variance reduction factor", v_plain / v_is, "101")
    q("equivalent plain paths (millions)", N_PATHS * ratio / 1e6, "10")
    rng = np.random.default_rng(SEED_IS)
    zs = rng.standard_normal(N_PATHS) + mu
    est = call_y(zs, k_otm) * np.exp(-mu * zs + 0.5 * mu * mu)
    print(f"  seeded run, seed {SEED_IS}: estimate {est.mean():.5f}, standard error {est.std(ddof=1) / math.sqrt(N_PATHS):.6f}")
    close("seeded IS estimate within 4 standard errors of Black-Scholes", float(est.mean()), c_otm, 4 * se_is)
    close("seeded IS standard error within 1% of exact", float(est.std(ddof=1)) / math.sqrt(N_PATHS), se_is, 0.01 * se_is)
    zp = np.random.default_rng(SEED_IS + 1).standard_normal(N_PATHS)
    q("seeded plain fraction of paths in the money (%)", 100 * float(np.mean(s_t(zp) > k_otm)), "1.4")

    print("Example 5: Longstaff-Schwartz, S0 = 36, K = 40, r = 6%, sigma = 20%, T = 1, 50 exercise dates")
    q("European put", bs_price(36, 40, 1.0, 0.06, 0.2, call=False), "3.844")
    berm = crr_put(36, 40, 0.06, 0.2, 1.0, 5000, 100)
    q("Bermudan put, 5,000-step tree, exercise on 50 dates", berm, "4.478")
    for n in (2500, 10000):
        close(f"Bermudan tree convergence, {n} steps", crr_put(36, 40, 0.06, 0.2, 1.0, n, n // 50), berm, 1e-4)
    amer = crr_put(36, 40, 0.06, 0.2, 1.0, 5000, None)
    q("American put (exercise every step), for comparison", amer, "4.487")
    price, se = lsm_american_put(36, 40, 0.06, 0.2, 1.0, seed=0)
    q("LSM price, seed 0", float(price), "4.466")
    q("LSM standard error", float(se), "0.006")
    runs = np.array([lsm_american_put(36, 40, 0.06, 0.2, 1.0, seed=s)[0] for s in range(20)])
    mean20 = q("mean over seeds 0 to 19", float(runs.mean()), "4.463")
    se20 = float(runs.std(ddof=1) / math.sqrt(len(runs)))
    q("shortfall to the Bermudan benchmark", berm - mean20, "0.015")
    assert berm - mean20 > 5 * se20, (berm, mean20, se20)
    q("shortfall in standard errors of the 20-seed mean", (berm - mean20) / se20, "9")
    q("early-exercise premium, Bermudan minus European", berm - bs_price(36, 40, 1.0, 0.06, 0.2, call=False), "0.63")
    oos, oos_se = lsm_out_of_sample(36, 40, 0.06, 0.2, 1.0, seed=0)
    print(f"    out-of-sample policy value = {oos:.4f} (standard error {oos_se:.4f})")
    assert oos < berm, "an estimated policy priced on fresh paths must not beat the optimal Bermudan value"
    q("LSM price, two decimals (card)", float(price), "4.47")

    print("Example 6: three ways to compute delta, 100,000 paths each")
    delta = q("Black-Scholes delta", norm_cdf(d1), "0.6368")
    pw = lambda z: DISC * (s_t(z) > K) * s_t(z) / S0  # noqa: E731
    lr = lambda z: call_y(z) * z / (S0 * SD)  # noqa: E731
    var_pw = normal_expect(lambda z: pw(z) ** 2, (zk,)) - delta**2
    var_lr = normal_expect(lambda z: lr(z) ** 2, (zk,)) - delta**2
    close("pathwise mean by quadrature equals delta", normal_expect(pw, (zk,)), delta, 1e-10)
    close("likelihood-ratio mean by quadrature equals delta", normal_expect(lr, (zk,)), delta, 1e-10)
    q("pathwise standard error (exact)", math.sqrt(var_pw / N_PATHS), "0.0018")
    q("likelihood-ratio standard error (exact)", math.sqrt(var_lr / N_PATHS), "0.0046")
    q("variance ratio LR / pathwise", var_lr / var_pw, "6.5")
    rng = np.random.default_rng(SEED_GREEKS)
    z = rng.standard_normal(N_PATHS)
    est_pw, est_lr = pw(z), lr(z)
    up = DISC * np.maximum(s_t(z, S0 + 1) - K, 0.0)
    dn = DISC * np.maximum(s_t(z, S0 - 1) - K, 0.0)
    bump = (up - dn) / 2
    z2 = rng.standard_normal(N_PATHS)
    up_ind = DISC * np.maximum(s_t(z2, S0 + 1) - K, 0.0)
    bump_ind_mean = (up_ind.mean() - dn.mean()) / 2
    bump_ind_se = math.sqrt(up_ind.var(ddof=1) / N_PATHS + dn.var(ddof=1) / N_PATHS) / 2
    print(f"  seed {SEED_GREEKS}")
    for name, y, qm, qs in (("pathwise", est_pw, "0.6364", "0.0018"), ("likelihood ratio", est_lr, "0.6366", "0.0046")):
        se_y = float(y.std(ddof=1)) / math.sqrt(N_PATHS)
        q(f"{name} estimate", float(y.mean()), qm)
        q(f"{name} standard error", se_y, qs)
        close(f"{name} within 3 standard errors of delta", float(y.mean()), delta, 3 * se_y)
    se_b = float(bump.std(ddof=1)) / math.sqrt(N_PATHS)
    q("bump h = 1, common random numbers", float(bump.mean()), "0.6363")
    q("bump h = 1, common random numbers, standard error", se_b, "0.0018")
    q("bump h = 1, independent draws", bump_ind_mean, "0.631")
    q("bump h = 1, independent draws, standard error", bump_ind_se, "0.033")
    close("independent bump within 3 standard errors of delta", bump_ind_mean, delta, 3 * bump_ind_se)
    exact_bump = (bs_price(S0 + 1, K, T, R, SIG) - bs_price(S0 - 1, K, T, R, SIG)) / 2
    close("CRN bump within 3 standard errors of the exact central difference", float(bump.mean()), exact_bump, 3 * se_b)
    dig_exact = q("digital delta exp(-rT) phi(d2) / (S0 sigma sqrt T)", DISC * norm_pdf(d2) / (S0 * SD), "0.01876")
    dig = lambda z: DISC * (s_t(z) > K) * z / (S0 * SD)  # noqa: E731
    close("digital LR delta by quadrature", normal_expect(dig, (zk,)), dig_exact, 1e-10)
    est_dig = DISC * (s_t(z) > K) * z / (S0 * SD)
    se_dig = float(est_dig.std(ddof=1)) / math.sqrt(N_PATHS)
    q("digital likelihood-ratio estimate", float(est_dig.mean()), "0.01878")
    close("digital LR within 3 standard errors of exact", float(est_dig.mean()), dig_exact, 3 * se_dig)

    print("Example 7: Broadie-Glasserman-Kou shift for a daily barrier at 120")
    beta = -zeta_half() / math.sqrt(2 * math.pi)
    q("zeta(1/2)", zeta_half(), "-1.4604")
    q("beta = -zeta(1/2) / sqrt(2 pi)", beta, "0.5826")
    shift = q("beta sigma sqrt(1/252)", 0.5826 * SIG * math.sqrt(1 / 252), "0.00734")
    q("shifted barrier 120 exp(shift)", 120 * math.exp(shift), "120.88")

    print(f"Geometric control for an arithmetic Asian (12 monthly fixings, 200,000 paths, seed {SEED_ASIAN})")
    rng = np.random.default_rng(SEED_ASIAN)
    dt = T / 12
    logs = np.log(S0) + np.cumsum((R - 0.5 * SIG**2) * dt + SIG * math.sqrt(dt) * rng.standard_normal((200_000, 12)), axis=1)
    arith = DISC * np.maximum(np.exp(logs).mean(axis=1) - K, 0.0)
    geom = DISC * np.maximum(np.exp(logs.mean(axis=1)) - K, 0.0)
    rho_asian = float(np.corrcoef(arith, geom)[0, 1])
    print(f"    corr(arithmetic, geometric) = {rho_asian:.5f}")
    assert rho_asian > 0.99, rho_asian

    print("Cards")
    q("deriv-mc-error-scaling: paths for 1 cent from 4 cents at 10,000", 10_000 * (4 / 1) ** 2, "160000")
    print("All Monte Carlo checks passed.")


if __name__ == "__main__":
    main()
