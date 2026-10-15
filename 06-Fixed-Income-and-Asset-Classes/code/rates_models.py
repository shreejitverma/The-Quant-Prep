"""Hull-White, Black-76, Bachelier, SABR, and Convexity Adjustments Reference Implementation.

Pure Python 3.10+ standard library implementation of fixed income rates models:
1. Standard normal CDF and PDF, erf-based.
2. Black-76 model for interest rate caps, floors, and European swaptions.
3. Bachelier normal model for low-rate and negative-rate environments.
4. Hagan et al. (2002) SABR asymptotic implied lognormal (Black) vol, plain and shifted.
5. Convexity adjustments (Futures vs Forward, CMS replication / duration adjustment, in-arrears).
6. Hull-White 1-factor model analytics (ZCB options, Jamshidian decomposition for swaptions).
7. Hull-White trinomial tree for Bermudan swaption pricing and early exercise valuation.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

# ============================================================================
# 1. Standard Normal Distribution Utilities
# ============================================================================

SQRT_TWO = math.sqrt(2.0)
SQRT_TWO_PI = math.sqrt(2.0 * math.pi)


def norm_cdf(x: float) -> float:
    """Cumulative distribution function for standard normal N(0, 1)."""
    return 0.5 * (1.0 + math.erf(x / SQRT_TWO))


def norm_pdf(x: float) -> float:
    """Probability density function for standard normal N(0, 1)."""
    return math.exp(-0.5 * x * x) / SQRT_TWO_PI


# ============================================================================
# 2. Black-76 Formula (Interest Rate Options & Swaptions)
# ============================================================================


def black76_price(
    forward: float,
    strike: float,
    vol: float,
    t_exp: float,
    annuity: float,
    is_call: bool = True,
) -> float:
    """Black-76 option price on a forward rate or swap rate.

    Args:
        forward: Forward rate (e.g. 0.04 for 4%).
        strike: Strike rate (e.g. 0.04).
        vol: Lognormal volatility (e.g. 0.20 for 20%).
        t_exp: Expiry in years (e.g. 1.0).
        annuity: Present value of 1 bp or annuity factor A (e.g. sum(tau_i * P(0, T_i))).
        is_call: True for payer swaption / caplet, False for receiver swaption / floorlet.
    """
    if forward <= 0.0 or strike <= 0.0:
        raise ValueError("Forward and strike must be positive in Black-76.")
    if t_exp <= 0.0 or vol <= 0.0:
        intrinsic = max(0.0, forward - strike if is_call else strike - forward)
        return annuity * intrinsic

    std_dev = vol * math.sqrt(t_exp)
    d1 = (math.log(forward / strike) + 0.5 * std_dev * std_dev) / std_dev
    d2 = d1 - std_dev

    if is_call:
        return annuity * (forward * norm_cdf(d1) - strike * norm_cdf(d2))
    else:
        return annuity * (strike * norm_cdf(-d2) - forward * norm_cdf(-d1))


def black76_vega(
    forward: float,
    strike: float,
    vol: float,
    t_exp: float,
    annuity: float,
) -> float:
    """Black-76 vega dV/d(vol)."""
    if forward <= 0.0 or strike <= 0.0 or t_exp <= 0.0 or vol <= 0.0:
        return 0.0
    std_dev = vol * math.sqrt(t_exp)
    d1 = (math.log(forward / strike) + 0.5 * std_dev * std_dev) / std_dev
    return annuity * forward * math.sqrt(t_exp) * norm_pdf(d1)


def black76_delta(
    forward: float,
    strike: float,
    vol: float,
    t_exp: float,
    annuity: float,
    is_call: bool = True,
) -> float:
    """Black-76 delta dV/d(forward)."""
    if forward <= 0.0 or strike <= 0.0:
        raise ValueError("Forward and strike must be positive.")
    std_dev = vol * math.sqrt(t_exp)
    d1 = (math.log(forward / strike) + 0.5 * std_dev * std_dev) / std_dev
    if is_call:
        return annuity * norm_cdf(d1)
    else:
        return -annuity * norm_cdf(-d1)


def _solve_implied_vol(
    price_at: Callable[[float], float],
    vega_at: Callable[[float], float],
    target_price: float,
    lower_bound: float,
    upper_bound: float,
    initial_vol: float,
    max_iter: int,
    tol: float,
) -> float:
    """Safeguarded Newton solve of price_at(vol) = target_price on a bracket [lo, hi].

    The price is increasing in vol, equal to lower_bound at vol = 0 and tending to upper_bound.
    Raises ValueError when the target is outside the no-arbitrage bounds or the solver does not converge.
    """
    if not lower_bound < target_price < upper_bound:
        raise ValueError(f"Target price {target_price} is outside the no-arbitrage bounds ({lower_bound}, {upper_bound}).")
    if initial_vol <= 0.0:
        raise ValueError("Initial volatility must be positive.")

    lo, hi = 0.0, initial_vol
    for _ in range(max_iter):
        if price_at(hi) >= target_price:
            break
        lo, hi = hi, 2.0 * hi
    else:
        raise ValueError(f"Could not bracket the implied volatility for target price {target_price}.")

    vol = hi
    for _ in range(max_iter):
        diff = price_at(vol) - target_price
        if abs(diff) < tol:
            return vol
        if diff > 0.0:
            hi = vol
        else:
            lo = vol
        vega = vega_at(vol)
        newton = vol - diff / vega if vega > 0.0 else lo
        vol = newton if lo < newton < hi else 0.5 * (lo + hi)
    raise ValueError(f"Implied volatility solver did not converge for target price {target_price}.")


def implied_black_vol(
    target_price: float,
    forward: float,
    strike: float,
    t_exp: float,
    annuity: float,
    is_call: bool = True,
    initial_vol: float = 0.20,
    max_iter: int = 100,
    tol: float = 1e-8,
) -> float:
    """Invert Black-76 formula to find implied lognormal volatility.

    Raises ValueError if the price violates A*max(F-K, 0) < price < A*F (call) or
    A*max(K-F, 0) < price < A*K (put), or if the solver does not converge.
    """
    if t_exp <= 0.0 or annuity <= 0.0:
        raise ValueError("Expiry and annuity must be positive to imply a volatility.")
    if is_call:
        lower, upper = annuity * max(forward - strike, 0.0), annuity * forward
    else:
        lower, upper = annuity * max(strike - forward, 0.0), annuity * strike
    return _solve_implied_vol(
        lambda v: black76_price(forward, strike, v, t_exp, annuity, is_call),
        lambda v: black76_vega(forward, strike, v, t_exp, annuity),
        target_price,
        lower,
        upper,
        initial_vol,
        max_iter,
        tol,
    )


# ============================================================================
# 3. Bachelier (Normal) Model (Low & Negative Rates)
# ============================================================================


def bachelier_price(
    forward: float,
    strike: float,
    normal_vol: float,
    t_exp: float,
    annuity: float,
    is_call: bool = True,
) -> float:
    """Bachelier normal option price on a forward or swap rate.

    Args:
        forward: Forward rate (can be negative or zero).
        strike: Strike rate (can be negative or zero).
        normal_vol: Normal volatility in annualized rate units (e.g. 0.0080 for 80 bps/year).
        t_exp: Expiry in years.
        annuity: Present value of annuity factor A.
        is_call: True for payer / call, False for receiver / put.
    """
    if t_exp <= 0.0 or normal_vol <= 0.0:
        intrinsic = max(0.0, forward - strike if is_call else strike - forward)
        return annuity * intrinsic

    std_dev = normal_vol * math.sqrt(t_exp)
    d = (forward - strike) / std_dev

    if is_call:
        return annuity * ((forward - strike) * norm_cdf(d) + std_dev * norm_pdf(d))
    else:
        return annuity * ((strike - forward) * norm_cdf(-d) + std_dev * norm_pdf(d))


def bachelier_vega(
    forward: float,
    strike: float,
    normal_vol: float,
    t_exp: float,
    annuity: float,
) -> float:
    """Bachelier normal vega dV/d(normal_vol)."""
    if t_exp <= 0.0 or normal_vol <= 0.0:
        return 0.0
    std_dev = normal_vol * math.sqrt(t_exp)
    d = (forward - strike) / std_dev
    return annuity * math.sqrt(t_exp) * norm_pdf(d)


def implied_normal_vol(
    target_price: float,
    forward: float,
    strike: float,
    t_exp: float,
    annuity: float,
    is_call: bool = True,
    initial_vol: float = 0.0080,
    max_iter: int = 100,
    tol: float = 1e-9,
) -> float:
    """Invert Bachelier formula to find implied normal volatility (in rate/yr).

    Raises ValueError if the price is not above intrinsic A*max(+/-(F-K), 0) or the solver does not converge.
    """
    if t_exp <= 0.0 or annuity <= 0.0:
        raise ValueError("Expiry and annuity must be positive to imply a volatility.")
    intrinsic = annuity * max(forward - strike if is_call else strike - forward, 0.0)
    return _solve_implied_vol(
        lambda v: bachelier_price(forward, strike, v, t_exp, annuity, is_call),
        lambda v: bachelier_vega(forward, strike, v, t_exp, annuity),
        target_price,
        intrinsic,
        math.inf,
        initial_vol,
        max_iter,
        tol,
    )


# ============================================================================
# 4. Hagan et al. (2002) SABR Model
# ============================================================================


def sabr_lognormal_vol(
    f: float,
    k: float,
    t_exp: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
) -> float:
    """Hagan et al. (2002) asymptotic implied Black volatility for SABR.

    Args:
        f: Forward rate (must be positive).
        k: Strike rate (must be positive).
        t_exp: Expiry in years.
        alpha: SABR initial volatility parameter.
        beta: Elasticity / backbone parameter (0 <= beta <= 1).
        rho: Correlation between asset and volatility (-1 < rho < 1).
        nu: Volatility of volatility parameter (nu >= 0).
    """
    if f <= 0.0 or k <= 0.0:
        raise ValueError("Forward and strike must be positive for standard lognormal SABR.")
    if t_exp <= 0.0:
        return alpha / (f ** (1.0 - beta))

    one_minus_beta = 1.0 - beta

    # ATM special case
    if abs(f - k) < 1e-8:
        fk_mid = f**one_minus_beta
        term1 = alpha / fk_mid
        factor2 = (
            (one_minus_beta**2 / 24.0) * (alpha * alpha) / (f ** (2.0 * one_minus_beta))
            + 0.25 * rho * beta * nu * alpha / (f**one_minus_beta)
            + ((2.0 - 3.0 * rho * rho) / 24.0) * (nu * nu)
        )
        return term1 * (1.0 + factor2 * t_exp)

    log_fk = math.log(f / k)
    fk = f * k
    fk_pow = fk ** (one_minus_beta * 0.5)

    z = (nu / alpha) * fk_pow * log_fk

    # Numerical safeguard for z -> 0
    if abs(z) < 1e-6:
        z_over_x = 1.0
    else:
        arg = math.sqrt(1.0 - 2.0 * rho * z + z * z) + z - rho
        if arg <= 0.0:
            arg = 1e-12
        x_z = math.log(arg / (1.0 - rho))
        z_over_x = z / x_z

    denom = fk_pow * (1.0 + (one_minus_beta**2 / 24.0) * (log_fk**2) + (one_minus_beta**4 / 1920.0) * (log_fk**4))

    factor1 = (alpha / denom) * z_over_x
    factor2 = (
        1.0
        + (
            (one_minus_beta**2 / 24.0) * (alpha * alpha) / (fk**one_minus_beta)
            + 0.25 * (rho * beta * nu * alpha) / fk_pow
            + ((2.0 - 3.0 * rho * rho) / 24.0) * (nu * nu)
        )
        * t_exp
    )

    return factor1 * factor2


def shifted_sabr_lognormal_vol(
    f: float,
    k: float,
    t_exp: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
    shift: float,
) -> float:
    """Shifted SABR implied lognormal volatility for negative or near-zero rates."""
    f_shifted = f + shift
    k_shifted = k + shift
    if f_shifted <= 0.0 or k_shifted <= 0.0:
        raise ValueError("Shifted forward and strike must be strictly positive.")
    return sabr_lognormal_vol(f_shifted, k_shifted, t_exp, alpha, beta, rho, nu)


# ============================================================================
# 5. Convexity Adjustments
# ============================================================================


def futures_rate_convexity_adjustment(sigma: float, t1: float, t2: float) -> float:
    """Ho-Lee convexity adjustment between futures rate and forward rate.

    Under daily cash margining, futures rate exceeds forward rate. This is the
    a -> 0 (Ho-Lee) limit of the Hull-White adjustment, continuously compounded:
    R_fut - R_fwd = 1/2 * sigma^2 * t1 * t2.

    Args:
        sigma: Volatility of the short rate.
        t1: Futures contract expiration date (fixing time) in years.
        t2: Underlying rate maturity date in years.
    """
    return 0.5 * sigma * sigma * t1 * t2


def cms_rate_annuity_adjustment(
    s0: float,
    sigma_s: float,
    t1: float,
    swap_tenor: int,
    freq: int = 1,
) -> float:
    """CMS (Constant Maturity Swap) convexity adjustment via annuity replication / duration.

    For a swap rate S_t fixing at T_1 and paid with payment frequency freq,
    annuity A(s) = sum_{i=1}^{n} (1/freq) / (1 + s/freq)^i.
    Under the forward measure P(t, T_1), the change of numeraire from annuity
    induces a positive convexity adjustment:
    Adj_CMS ≈ s0^2 * sigma_s^2 * t1 * (-A'(s0) / A(s0)).

    Args:
        s0: Forward swap rate (e.g. 0.04).
        sigma_s: Lognormal swap rate volatility (e.g. 0.20).
        t1: Fixation time in years.
        swap_tenor: Underlying swap tenor in years.
        freq: Payments per year (default 1 for annual, 2 for semi-annual).
    """
    n = swap_tenor * freq
    dt = 1.0 / freq
    y = s0 * dt

    # Compute annuity A(s0) and its derivative dA/ds(s0)
    annuity = sum(dt / ((1.0 + y) ** i) for i in range(1, n + 1))
    d_annuity_ds = -sum(dt * (i * dt) / ((1.0 + y) ** (i + 1)) for i in range(1, n + 1))

    rel_duration = -d_annuity_ds / annuity
    adj = (s0 * s0) * (sigma_s * sigma_s) * t1 * rel_duration
    return adj


def in_arrears_convexity_adjustment(
    f0: float,
    sigma_f: float,
    t1: float,
    tau: float,
) -> float:
    """In-arrears fixing rate adjustment for rate paid at T1 instead of T1 + tau.

    When Libor/SOFR is fixing at T1 and paid in-advance at T1:
    E^{T1}[L(T1)] = L0 + tau * L0^2 * sigma_f^2 * T1 / (1 + tau * L0).
    """
    return (tau * f0 * f0 * sigma_f * sigma_f * t1) / (1.0 + tau * f0)


# ============================================================================
# 6. Hull-White 1-Factor Analytical Model
# ============================================================================


@dataclass(frozen=True)
class HW1FParams:
    a: float  # Mean reversion speed (e.g. 0.03)
    sigma: float  # Volatility of short rate (e.g. 0.012 for 1.2%)


def hw_b(a: float, t: float, big_t: float) -> float:
    """Hull-White B(t, T) factor."""
    if abs(a) < 1e-10:
        return big_t - t
    return (1.0 - math.exp(-a * (big_t - t))) / a


def hw_zcb_price_from_state(
    p0_t: float,
    p0_big_t: float,
    t: float,
    big_t: float,
    x: float,
    a: float,
    sigma: float,
) -> float:
    """Hull-White zero-coupon bond P(t, T) given the zero-mean OU state x(t) = r(t) - phi(t).

    With dx = -a x dt + sigma dW, x(0) = 0 (Brigo-Mercurio, section 3.3):
    P(t, T) = P(0, T) / P(0, t) * exp(-B x - B * sigma^2/(2a^2) (1 - e^{-at})^2 - sigma^2/(4a) (1 - e^{-2at}) B^2),
    with B = B(t, T); the a -> 0 limits are sigma^2 t^2 / 2 and sigma^2 t / 2.
    """
    b = hw_b(a, t, big_t)
    if abs(a) < 1e-10:
        drift_shift = 0.5 * sigma * sigma * t * t
        convexity = 0.5 * sigma * sigma * t
    else:
        drift_shift = sigma * sigma / (2.0 * a * a) * (1.0 - math.exp(-a * t)) ** 2
        convexity = sigma * sigma / (4.0 * a) * (1.0 - math.exp(-2.0 * a * t))
    return (p0_big_t / p0_t) * math.exp(-b * x - b * drift_shift - convexity * b * b)


def hw_zcb_option_price(
    p0_t: float,
    p0_s: float,
    strike: float,
    t_exp: float,
    s_mat: float,
    a: float,
    sigma: float,
    is_call: bool = True,
) -> float:
    """European option on zero-coupon bond P(T, S) under Hull-White 1F.

    Args:
        p0_t: Discount factor to option expiry T.
        p0_s: Discount factor to bond maturity S (S > T).
        strike: Strike price of zero bond (e.g. 0.95).
        t_exp: Expiry T in years.
        s_mat: Maturity S of underlying bond in years.
        a: Mean reversion speed.
        sigma: Rate volatility.
        is_call: True for call, False for put.
    """
    b_t_s = hw_b(a, t_exp, s_mat)
    # sigma_p = sigma * sqrt((1 - exp(-2aT)) / (2a)) * B(T, S)
    var_int = (1.0 - math.exp(-2.0 * a * t_exp)) / (2.0 * a) if abs(a) > 1e-10 else t_exp
    sigma_p = sigma * math.sqrt(var_int) * b_t_s

    if sigma_p < 1e-12:
        intrinsic = max(0.0, (p0_s - strike * p0_t) if is_call else (strike * p0_t - p0_s))
        return intrinsic

    d1 = (math.log(p0_s / (strike * p0_t)) + 0.5 * sigma_p * sigma_p) / sigma_p
    d2 = d1 - sigma_p

    if is_call:
        return p0_s * norm_cdf(d1) - strike * p0_t * norm_cdf(d2)
    else:
        return strike * p0_t * norm_cdf(-d2) - p0_s * norm_cdf(-d1)


def hw_swaption_jamshidian(
    discount_curve: Callable[[float], float],
    strike_swap: float,
    t_exp: float,
    swap_tenor: float,
    swap_freq: int,
    a: float,
    sigma: float,
    is_payer: bool = True,
) -> float:
    """Price European swaption via Jamshidian (1989) decomposition under Hull-White 1F.

    A European payer swaption is an option to pay fixed K and receive floating S.
    Payoff at T = max(0, 1 - sum_{i=1}^n c_i P(T, T_i)) where c_i = K * tau (and c_n = 1 + K * tau).
    Jamshidian proves that this decomposes into a sum of zero bond put options!
    """
    dt = 1.0 / swap_freq
    n_coupons = int(round(swap_tenor * swap_freq))
    ti = [t_exp + (i + 1) * dt for i in range(n_coupons)]
    ci = [strike_swap * dt for _ in range(n_coupons)]
    ci[-1] += 1.0  # principal on final coupon

    p0_t = discount_curve(t_exp)
    p0_ti = [discount_curve(t) for t in ti]

    # Find the state x* at expiry T such that sum ci * P(T, T_i; x*) = 1;
    # P(T, T_i; x) is strictly decreasing in x, so bisection on a sign-changing bracket converges.
    def bond_price(i: int, x: float) -> float:
        return hw_zcb_price_from_state(p0_t, p0_ti[i], t_exp, ti[i], x, a, sigma)

    def portfolio_value(x: float) -> float:
        return sum(c * bond_price(i, x) for i, c in enumerate(ci)) - 1.0

    x_low, x_high = -0.50, 0.50
    if portfolio_value(x_low) < 0.0 or portfolio_value(x_high) > 0.0:
        raise ValueError("Jamshidian critical state lies outside [-0.5, 0.5]; strike is unrealistic for this curve.")
    for _ in range(100):
        x_mid = 0.5 * (x_low + x_high)
        if portfolio_value(x_mid) > 0.0:
            x_low = x_mid
        else:
            x_high = x_mid
    x_star = 0.5 * (x_low + x_high)

    # Individual strike prices for zero bonds
    ki = [bond_price(i, x_star) for i in range(n_coupons)]

    # Swaption is portfolio of zero-coupon bond options
    # Payer swaption = Put option on coupon bond = sum of puts on zeros
    # Receiver swaption = Call option on coupon bond = sum of calls on zeros
    swaption_price = 0.0
    for i in range(n_coupons):
        zcb_opt = hw_zcb_option_price(
            p0_t=p0_t,
            p0_s=p0_ti[i],
            strike=ki[i],
            t_exp=t_exp,
            s_mat=ti[i],
            a=a,
            sigma=sigma,
            is_call=(not is_payer),
        )
        swaption_price += ci[i] * zcb_opt

    return swaption_price


# ============================================================================
# 7. Hull-White Trinomial Tree (Bermudan Swaption Valuation)
# ============================================================================


def hw_bermudan_swaption_tree(
    discount_curve: Callable[[float], float],
    strike: float,
    exercise_times: Sequence[float],
    swap_end: float,
    swap_freq: int,
    a: float,
    sigma: float,
    is_payer: bool = True,
    dt: float = 0.25,
) -> tuple[float, float, float]:
    """Valuation of a co-terminal Bermudan swaption vs the European on its first exercise date.

    Uses the Hull-White (1994) trinomial tree on the zero-mean OU state x = r - alpha(t):
    dx = -a x dt + sigma dW, node spacing dx = sigma * sqrt(3 dt), nodes truncated at
    j_max = ceil(0.184 / (a dt)) with the standard edge branching, and alpha_m fitted to the
    discount curve by forward induction on Arrow-Debreu prices. Exercising at t_m enters the
    swap from t_m to swap_end, valued with the analytic bond price hw_zcb_price_from_state.

    Every exercise time must lie on the dt grid and on the swap coupon schedule ending at swap_end.

    Returns:
        (bermudan_price, european_price, early_exercise_premium)
    """
    if a <= 0.0 or sigma <= 0.0 or dt <= 0.0 or swap_freq <= 0:
        raise ValueError("Mean reversion, volatility, time step and swap frequency must be positive.")
    if not exercise_times:
        raise ValueError("At least one exercise time is required.")
    n_steps = int(round(swap_end / dt))
    if n_steps < 1 or abs(n_steps * dt - swap_end) > 1e-9:
        raise ValueError(f"swap_end {swap_end} must be a positive multiple of dt {dt}.")
    tau = 1.0 / swap_freq
    exercise_steps: set[int] = set()
    for t_ex in exercise_times:
        step = int(round(t_ex / dt))
        n_coupons = int(round((swap_end - t_ex) * swap_freq))
        if abs(step * dt - t_ex) > 1e-9 or abs(t_ex + n_coupons * tau - swap_end) > 1e-9 or not 0 < step < n_steps:
            raise ValueError(f"Exercise time {t_ex} must lie strictly inside (0, swap_end) on the dt grid and the coupon schedule.")
        exercise_steps.add(step)
    first_exercise_step = min(exercise_steps)

    dx = sigma * math.sqrt(3.0 * dt)
    j_max = int(math.ceil(0.184 / (a * dt)))

    def node_range(m: int) -> range:
        width = min(m, j_max)
        return range(-width, width + 1)

    # Branching is time-homogeneous: node j maps to (center, p_up, p_mid, p_down).
    # The expected move of x over dt is -a * j * dx * dt; e is that move relative to the center, in units of dx.
    branches: dict[int, tuple[int, float, float, float]] = {}
    for j in node_range(n_steps):
        shift = -1 if j >= j_max else (1 if j <= -j_max else 0)
        e = -a * j * dt - shift
        probs = (1.0 / 6.0 + 0.5 * (e * e + e), 2.0 / 3.0 - e * e, 1.0 / 6.0 + 0.5 * (e * e - e))
        if min(probs) < 0.0:
            raise ValueError(f"Negative branching probability at node {j}; reduce dt for mean reversion a = {a}.")
        branches[j] = (j + shift, *probs)

    # Forward induction: alpha_m makes the tree reprice P(0, t_{m+1}).
    alpha: list[float] = []
    q: dict[int, float] = {0: 1.0}
    for m in range(n_steps):
        sum_q_exp = sum(q_j * math.exp(-j * dx * dt) for j, q_j in q.items())
        alpha_m = math.log(sum_q_exp / discount_curve((m + 1) * dt)) / dt
        alpha.append(alpha_m)
        if m == n_steps - 1:
            break
        q_next = {j: 0.0 for j in node_range(m + 1)}
        for j, q_j in q.items():
            center, p_u, p_m, p_d = branches[j]
            weight = q_j * math.exp(-(alpha_m + j * dx) * dt)
            q_next[center + 1] += weight * p_u
            q_next[center] += weight * p_m
            q_next[center - 1] += weight * p_d
        q = q_next

    # Backward induction; the swap has no value at swap_end.
    val_berm = {j: 0.0 for j in node_range(n_steps)}
    val_euro = {j: 0.0 for j in node_range(n_steps)}
    for m in range(n_steps - 1, -1, -1):
        t_m = m * dt
        is_exercise = m in exercise_steps
        if is_exercise:
            p0_m = discount_curve(t_m)
            coupon_times = [t_m + (i + 1) * tau for i in range(int(round((swap_end - t_m) * swap_freq)))]
            p0_coupons = [discount_curve(t) for t in coupon_times]
        new_berm: dict[int, float] = {}
        new_euro: dict[int, float] = {}
        for j in node_range(m):
            center, p_u, p_m, p_d = branches[j]
            disc = math.exp(-(alpha[m] + j * dx) * dt)
            cont_berm = disc * (p_u * val_berm[center + 1] + p_m * val_berm[center] + p_d * val_berm[center - 1])
            cont_euro = disc * (p_u * val_euro[center + 1] + p_m * val_euro[center] + p_d * val_euro[center - 1])
            if is_exercise:
                x = j * dx
                bonds = [
                    hw_zcb_price_from_state(p0_m, p0_i, t_m, t_i, x, a, sigma) for t_i, p0_i in zip(coupon_times, p0_coupons, strict=True)
                ]
                annuity_val = tau * sum(bonds)
                payer_npv = (1.0 - bonds[-1]) - strike * annuity_val
                intrinsic = max(0.0, payer_npv if is_payer else -payer_npv)
                cont_berm = max(cont_berm, intrinsic)
                if m == first_exercise_step:
                    cont_euro = max(cont_euro, intrinsic)
            new_berm[j] = cont_berm
            new_euro[j] = cont_euro
        val_berm = new_berm
        val_euro = new_euro

    berm_price = val_berm[0]
    euro_price = val_euro[0]
    return berm_price, euro_price, berm_price - euro_price


# ============================================================================
# 8. Self-Testing Verification Suite
# ============================================================================


def run_tests() -> None:
    """Execute rigorous unit tests on all interest rate models."""
    print("Testing Black-76, Bachelier, SABR, Convexity, and Hull-White models...")

    # 1. Black-76 Call & Put parity and Greeks
    f = 0.04
    k = 0.04
    vol = 0.25
    t_exp = 2.0
    annuity = 3.80
    c = black76_price(f, k, vol, t_exp, annuity, is_call=True)
    p = black76_price(f, k, vol, t_exp, annuity, is_call=False)
    # ATM closed form: C = A * F * (2 * Phi(sigma * sqrt(T) / 2) - 1)
    expected_atm_black = annuity * f * (2.0 * norm_cdf(0.5 * vol * math.sqrt(t_exp)) - 1.0)
    assert abs(c - expected_atm_black) < 1e-12, f"Black ATM closed form mismatch: {c} vs {expected_atm_black}"
    assert abs(c - p) < 1e-12, f"ATM call-put parity failed: {c} vs {p}"
    # Put-call parity away from the money: C - P = A * (F - K)
    f_itm = 0.045
    c_itm = black76_price(f_itm, k, vol, t_exp, annuity, is_call=True)
    p_itm = black76_price(f_itm, k, vol, t_exp, annuity, is_call=False)
    assert abs((c_itm - p_itm) - annuity * (f_itm - k)) < 1e-12, f"Black put-call parity failed: {c_itm - p_itm}"

    # Implied vol inverter: round trips, a deep OTM price, and prices outside the no-arbitrage bounds
    imp_vol = implied_black_vol(c, f, k, t_exp, annuity, is_call=True)
    assert abs(imp_vol - vol) < 1e-6, f"Implied vol mismatch: {imp_vol} vs {vol}"
    imp_vol_put = implied_black_vol(p_itm, f_itm, k, t_exp, annuity, is_call=False)
    assert abs(imp_vol_put - vol) < 1e-6, f"Implied put vol mismatch: {imp_vol_put} vs {vol}"
    otm_vol = implied_black_vol(0.0002, 0.04, 0.08, 1.0, 1.0)
    assert abs(black76_price(0.04, 0.08, otm_vol, 1.0, 1.0) - 0.0002) < 1e-8, f"Deep OTM implied vol does not reprice: {otm_vol}"
    for bad_price in (0.05, 0.0, -0.001):
        try:
            implied_black_vol(bad_price, 0.04, 0.08, 1.0, 1.0)
        except ValueError:
            pass
        else:
            raise AssertionError(f"implied_black_vol accepted price {bad_price} outside (0, A*F)")

    # 2. Bachelier Normal Model
    # When rates are zero or negative:
    fn = -0.0020  # -20 bps
    kn = -0.0020
    norm_vol = 0.0080  # 80 bps normal vol
    bn_c = bachelier_price(fn, kn, norm_vol, t_exp, annuity, is_call=True)
    bn_p = bachelier_price(fn, kn, norm_vol, t_exp, annuity, is_call=False)
    assert abs(bn_c - bn_p) < 1e-12, "Bachelier ATM call-put parity failed."
    # Theoretical ATM Bachelier formula: A * sigma_N * sqrt(T) / sqrt(2*pi)
    expected_atm = annuity * norm_vol * math.sqrt(t_exp) / math.sqrt(2.0 * math.pi)
    assert abs(bn_c - expected_atm) < 1e-10, f"Bachelier ATM exact mismatch: {bn_c} vs {expected_atm}"
    imp_norm_vol = implied_normal_vol(bn_c, fn, kn, t_exp, annuity, is_call=True)
    assert abs(imp_norm_vol - norm_vol) < 1e-7, "Bachelier implied normal vol inverter failed."
    # Put-call parity away from the money: C - P = A * (F - K)
    bn_c_otm = bachelier_price(fn, 0.0030, norm_vol, t_exp, annuity, is_call=True)
    bn_p_itm = bachelier_price(fn, 0.0030, norm_vol, t_exp, annuity, is_call=False)
    assert abs((bn_c_otm - bn_p_itm) - annuity * (fn - 0.0030)) < 1e-12, "Bachelier put-call parity failed."
    imp_norm_vol_otm = implied_normal_vol(bn_c_otm, fn, 0.0030, t_exp, annuity, is_call=True)
    assert abs(imp_norm_vol_otm - norm_vol) < 1e-7, f"Bachelier OTM implied vol mismatch: {imp_norm_vol_otm}"
    try:
        implied_normal_vol(0.5 * annuity * 0.0050, 0.0050, 0.0, t_exp, annuity, is_call=True)
    except ValueError:
        pass
    else:
        raise AssertionError("implied_normal_vol accepted a price below intrinsic value")

    # 3. SABR Model (Hagan 2002)
    alpha = 0.035
    beta = 0.5
    rho = -0.25
    nu = 0.40
    atm_vol = sabr_lognormal_vol(0.04, 0.04, 1.0, alpha, beta, rho, nu)
    assert 0.10 < atm_vol < 0.40, f"Unreasonable ATM SABR vol: {atm_vol}"
    low_strike_vol = sabr_lognormal_vol(0.04, 0.02, 1.0, alpha, beta, rho, nu)
    high_strike_vol = sabr_lognormal_vol(0.04, 0.06, 1.0, alpha, beta, rho, nu)
    # With negative rho (-0.25), low strike vol > high strike vol (skew)
    assert low_strike_vol > high_strike_vol, f"SABR negative skew failed: {low_strike_vol} <= {high_strike_vol}"

    # Shifted SABR for negative rates
    shifted_vol = shifted_sabr_lognormal_vol(-0.005, -0.005, 1.0, alpha, beta, rho, nu, shift=0.03)
    assert shifted_vol > 0.0, "Shifted SABR must be positive."

    # 4. Convexity Adjustments
    # Eurodollar / SOFR futures convexity adjustment
    sigma_hw = 0.012  # 1.2% short rate vol
    adj_fut = futures_rate_convexity_adjustment(sigma_hw, t1=2.0, t2=2.25)
    # Expected: 0.5 * (0.012)^2 * 2.0 * 2.25 = 0.000324 = 3.24 bps
    assert abs(adj_fut - 0.000324) < 1e-9, f"Futures convexity mismatch: {adj_fut}"

    # CMS convexity adjustment
    adj_cms = cms_rate_annuity_adjustment(s0=0.04, sigma_s=0.20, t1=5.0, swap_tenor=10, freq=1)
    adj_cms_bps = adj_cms * 10000.0

    # Oracle: closed-form annuity A(s) = (1 - (1 + s)^-n) / s with a central finite-difference derivative
    def closed_form_annuity(s: float) -> float:
        return (1.0 - (1.0 + s) ** -10) / s

    h = 1e-6
    d_annuity_fd = (closed_form_annuity(0.04 + h) - closed_form_annuity(0.04 - h)) / (2.0 * h)
    expected_cms = 0.04**2 * 0.20**2 * 5.0 * (-d_annuity_fd / closed_form_annuity(0.04))
    assert abs(adj_cms - expected_cms) < 1e-10, f"CMS adjustment {adj_cms} vs finite-difference oracle {expected_cms}"

    # In-arrears convexity adjustment
    adj_arrears = in_arrears_convexity_adjustment(f0=0.04, sigma_f=0.25, t1=1.0, tau=0.5)
    assert adj_arrears > 0.0, "In-arrears adjustment must be positive."

    # 5. Hull-White 1F Analytical Swaption (Jamshidian)
    # Flat 4% discount curve: P(0, t) = exp(-0.04 * t)
    def flat_curve(t: float) -> float:
        return math.exp(-0.04 * t)

    hw_swaption = hw_swaption_jamshidian(
        discount_curve=flat_curve,
        strike_swap=0.04,
        t_exp=1.0,
        swap_tenor=5.0,
        swap_freq=1,
        a=0.03,
        sigma=0.012,
        is_payer=True,
    )
    # Model-free swap parity: payer - receiver = P(0, T) - P(0, T_n) - K * A(0)
    for k_par in (0.03, 0.04, 0.05):
        payer = hw_swaption_jamshidian(flat_curve, k_par, 1.0, 5.0, 1, 0.03, 0.012, is_payer=True)
        receiver = hw_swaption_jamshidian(flat_curve, k_par, 1.0, 5.0, 1, 0.03, 0.012, is_payer=False)
        fwd_swap = flat_curve(1.0) - flat_curve(6.0) - k_par * sum(flat_curve(1.0 + i) for i in range(1, 6))
        assert abs((payer - receiver) - fwd_swap) < 1e-10, f"Jamshidian payer-receiver parity failed at K={k_par}"
    # Oracle: Bachelier with the normal vol of the swap rate implied by the HW state (sigma_x * |dS/dx|),
    # a first-order independent approximation; the HW swap rate is close to Gaussian for these parameters.
    var_x = 0.012**2 * (1.0 - math.exp(-2.0 * 0.03 * 1.0)) / (2.0 * 0.03)
    eps = 1e-6

    def hw_swap_rate(x: float) -> float:
        bonds = [hw_zcb_price_from_state(flat_curve(1.0), flat_curve(1.0 + i), 1.0, 1.0 + i, x, 0.03, 0.012) for i in range(1, 6)]
        return (1.0 - bonds[-1]) / sum(bonds)

    ds_dx = (hw_swap_rate(eps) - hw_swap_rate(-eps)) / (2.0 * eps)
    annuity_5y = sum(flat_curve(1.0 + i) for i in range(1, 6))
    fwd_rate_5y = (flat_curve(1.0) - flat_curve(6.0)) / annuity_5y
    bachelier_check = bachelier_price(fwd_rate_5y, 0.04, abs(ds_dx) * math.sqrt(var_x), 1.0, annuity_5y)
    assert abs(hw_swaption - bachelier_check) / bachelier_check < 0.02, f"Jamshidian {hw_swaption} vs Bachelier {bachelier_check}"

    # 6. Hull-White Trinomial Tree Bermudan vs European
    # Oracle: with a single exercise date the tree must converge to the analytic Jamshidian price.
    for k_tree, rel_tol in ((0.04, 0.01), (0.05, 0.04)):
        jamshidian_1y4y = hw_swaption_jamshidian(flat_curve, k_tree, 1.0, 4.0, 1, 0.03, 0.012, is_payer=True)
        berm_single, euro_single, _ = hw_bermudan_swaption_tree(flat_curve, k_tree, [1.0], 5.0, 1, 0.03, 0.012, is_payer=True, dt=0.1)
        assert abs(berm_single - euro_single) < 1e-15, "Single-date Bermudan must equal the European."
        assert abs(euro_single - jamshidian_1y4y) / jamshidian_1y4y < rel_tol, (
            f"Tree European {euro_single} vs Jamshidian {jamshidian_1y4y} at K={k_tree}"
        )
    # Horizon beyond 0.184 / a: nodes are truncated at j_max, so the edge branching is exercised.
    jamshidian_long = hw_swaption_jamshidian(flat_curve, 0.04, 10.0, 10.0, 1, 0.03, 0.012, is_payer=False)
    _, euro_long, _ = hw_bermudan_swaption_tree(flat_curve, 0.04, [10.0], 20.0, 1, 0.03, 0.012, is_payer=False, dt=0.1)
    assert abs(euro_long - jamshidian_long) / jamshidian_long < 0.01, f"Long tree {euro_long} vs Jamshidian {jamshidian_long}"

    ex_times = [1.0, 2.0, 3.0, 4.0]
    berm_p, euro_p, premium = hw_bermudan_swaption_tree(
        discount_curve=flat_curve,
        strike=0.04,
        exercise_times=ex_times,
        swap_end=5.0,
        swap_freq=1,
        a=0.03,
        sigma=0.012,
        is_payer=True,
        dt=0.05,
    )
    # A Bermudan is worth at least every co-terminal European it contains (each priced analytically).
    coterminal = [hw_swaption_jamshidian(flat_curve, 0.04, t, 5.0 - t, 1, 0.03, 0.012, is_payer=True) for t in ex_times]
    assert berm_p >= max(coterminal) * 0.99, f"Bermudan {berm_p} below max co-terminal European {max(coterminal)}"
    assert abs(premium - (berm_p - euro_p)) < 1e-15, "Premium must equal Bermudan minus European."
    try:
        hw_bermudan_swaption_tree(flat_curve, 0.04, [1.1], 5.0, 1, 0.03, 0.012, dt=0.25)
    except ValueError:
        pass
    else:
        raise AssertionError("Off-grid exercise time must be rejected.")

    print(f"Black-76 ATM 2y swaption price (A={annuity}): {c:.6f}")
    print(f"Bachelier normal 2y swaption price (vol=80bp): {bn_c:.6f}")
    print(f"SABR 1y ATM vol: {atm_vol * 100:.2f}%, 2% strike vol: {low_strike_vol * 100:.2f}%, 6% strike: {high_strike_vol * 100:.2f}%")
    print(f"Futures convexity adjustment: {adj_fut * 10000:.2f} bps")
    print(f"CMS 10y in 5y convexity adjustment: {adj_cms_bps:.2f} bps")
    print(f"Hull-White 1F 1y into 5y European swaption (Jamshidian): {hw_swaption:.6f}")
    print(f"Hull-White co-terminal Europeans into 5y (Jamshidian): {', '.join(f'{v:.6f}' for v in coterminal)}")
    print(f"Hull-White tree (dt=0.05) Bermudan 1y..4y into 5y: {berm_p:.6f}, European: {euro_p:.6f}, Premium: {premium:.6f}")
    print("All rates models tests passed successfully!")


if __name__ == "__main__":
    run_tests()
