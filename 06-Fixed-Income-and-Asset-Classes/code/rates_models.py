"""Hull-White, Black-76, Bachelier, SABR, and Convexity Adjustments Reference Implementation.

Pure Python 3.10+ standard library implementation of fixed income rates models:
1. Standard normal CDF and PDF, erf-based.
2. Black-76 model for interest rate caps, floors, and European swaptions.
3. Bachelier normal model for low-rate and negative-rate environments.
4. Hagan et al. (2002) SABR model asymptotic formulas (lognormal and normal vols).
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
    """Invert Black-76 formula to find implied lognormal volatility."""
    vol = initial_vol
    for _ in range(max_iter):
        p = black76_price(forward, strike, vol, t_exp, annuity, is_call)
        diff = p - target_price
        if abs(diff) < tol:
            return vol
        v = black76_vega(forward, strike, vol, t_exp, annuity)
        if abs(v) < 1e-14:
            break
        vol -= diff / v
        if vol <= 1e-5:
            vol = 1e-5
    return vol


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
    """Invert Bachelier formula to find implied normal volatility (in bp/yr or rate/yr)."""
    vol = initial_vol
    for _ in range(max_iter):
        p = bachelier_price(forward, strike, vol, t_exp, annuity, is_call)
        diff = p - target_price
        if abs(diff) < tol:
            return vol
        v = bachelier_vega(forward, strike, vol, t_exp, annuity)
        if abs(v) < 1e-14:
            break
        vol -= diff / v
        if vol <= 1e-6:
            vol = 1e-6
    return vol


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
    """Hull-White / Ho-Lee convexity adjustment between futures rate and forward rate.

    Under daily cash margining, futures rate exceeds forward rate:
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

    # Find r* at expiry T such that sum ci * P(T, T_i; r*) = 1
    # Under HW1F, P(T, T_i; r) = A(T, T_i) * exp(-B(T, T_i) * r)
    # where A(T, T_i) = (P(0, T_i) / P(0, T)) * exp(B(T, T_i)*f(0,T) - sigma^2/(4a)*(1-exp(-2aT))*B^2)
    # We calibrate r* with root finding:
    b_values = [hw_b(a, t_exp, t) for t in ti]
    var_alpha = (sigma * sigma / (4.0 * a)) * (1.0 - math.exp(-2.0 * a * t_exp)) if abs(a) > 1e-10 else 0.0

    def bond_price(i: int, r_diff: float) -> float:
        # r_diff is (r(T) - f(0, T))
        return (p0_ti[i] / p0_t) * math.exp(-b_values[i] * r_diff - var_alpha * (b_values[i] ** 2))

    def portfolio_value(r_diff: float) -> float:
        return sum(c * bond_price(i, r_diff) for i, c in enumerate(ci)) - 1.0

    # 1D root search for r_diff*
    r_low, r_high = -0.50, 0.50
    for _ in range(100):
        r_mid = 0.5 * (r_low + r_high)
        val = portfolio_value(r_mid)
        if abs(val) < 1e-12:
            break
        if val > 0:  # rates higher -> prices lower -> portfolio value drops
            r_low = r_mid
        else:
            r_high = r_mid
    r_star = 0.5 * (r_low + r_high)

    # Individual strike prices for zero bonds
    ki = [bond_price(i, r_star) for i in range(n_coupons)]

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
    """Valuation of Bermudan swaption vs European swaption via Hull-White trinomial tree.

    Returns:
        (bermudan_price, european_price, early_exercise_premium)
    """
    total_time = swap_end
    n_steps = int(round(total_time / dt))
    dx = sigma * math.sqrt(3.0 * dt)
    j_max = int(math.ceil(0.184 / (a * dt))) if a * dt > 1e-6 else 100

    # Build state variable x_j = j * dx, probabilities
    # Calibration of alpha_m to discount curve P(0, t_m)
    # Q(m, j): Arrow-Debreu state prices
    q_prev = {0: 1.0}
    alpha = [0.0] * n_steps

    for m in range(n_steps):
        t_m = m * dt
        # Match discount factor P(0, t_{m+1})
        # P(0, t_{m+1}) = sum_j Q(m, j) * exp(-(alpha_m + j*dx)*dt)
        # alpha_m = (1/dt) * ln( sum_j Q(m, j) * exp(-j*dx*dt) / P(0, t_{m+1}) )
        p_target = discount_curve(t_m + dt)
        sum_q_exp = sum(q * math.exp(-j * dx * dt) for j, q in q_prev.items())
        alpha_m = (1.0 / dt) * math.log(sum_q_exp / p_target)
        alpha[m] = alpha_m

        if m == n_steps - 1:
            break

        # Advance state prices to m + 1
        q_next: dict[int, float] = {}
        for j, q in q_prev.items():
            discount = math.exp(-(alpha_m + j * dx) * dt)
            # Branching
            eta = -a * j * dt
            k = int(round(eta / dx))
            # Bound k within +/- 1 from current node
            k_eff = max(-1, min(1, k))
            # Standard Hull-White trinomial probabilities
            eta_rel = eta - k_eff * dx
            p_u = 1.0 / 6.0 + 0.5 * (eta_rel * eta_rel / (dx * dx) + eta_rel / dx)
            p_m = 2.0 / 3.0 - (eta_rel * eta_rel / (dx * dx))
            p_d = 1.0 / 6.0 + 0.5 * (eta_rel * eta_rel / (dx * dx) - eta_rel / dx)

            center = j + k_eff
            for delta_node, prob in [(1, p_u), (0, p_m), (-1, p_d)]:
                target_node = center + delta_node
                q_next[target_node] = q_next.get(target_node, 0.0) + q * discount * prob
        q_prev = q_next

    # Backward induction for European and Bermudan
    # Terminal payoff at swap_end is 0
    val_berm: dict[int, float] = {j: 0.0 for j in q_prev}
    val_euro: dict[int, float] = {j: 0.0 for j in q_prev}

    ex_set = set(round(t, 4) for t in exercise_times)
    first_ex = min(exercise_times)

    for m in range(n_steps - 1, -1, -1):
        t_m = m * dt
        alpha_m = alpha[m]
        val_berm_next: dict[int, float] = {}
        val_euro_next: dict[int, float] = {}

        # Check if t_m is an exercise date
        is_exercise = round(t_m, 4) in ex_set
        is_first_ex = abs(t_m - first_ex) < 1e-4

        # For nodes at step m
        all_j = range(-min(m, j_max), min(m, j_max) + 1)
        for j in all_j:
            eta = -a * j * dt
            k = int(round(eta / dx))
            k_eff = max(-1, min(1, k))
            eta_rel = eta - k_eff * dx
            p_u = 1.0 / 6.0 + 0.5 * (eta_rel * eta_rel / (dx * dx) + eta_rel / dx)
            p_m = 2.0 / 3.0 - (eta_rel * eta_rel / (dx * dx))
            p_d = 1.0 / 6.0 + 0.5 * (eta_rel * eta_rel / (dx * dx) - eta_rel / dx)

            center = j + k_eff
            disc = math.exp(-(alpha_m + j * dx) * dt)

            c_berm = disc * (p_u * val_berm.get(center + 1, 0.0) + p_m * val_berm.get(center, 0.0) + p_d * val_berm.get(center - 1, 0.0))
            c_euro = disc * (p_u * val_euro.get(center + 1, 0.0) + p_m * val_euro.get(center, 0.0) + p_d * val_euro.get(center - 1, 0.0))

            if is_exercise:
                # Compute swap intrinsic value at node (m, j)
                # Swap from t_m to swap_end
                # Swap NPV = (1 - P(t_m, swap_end)) - strike * sum dt_i * P(t_m, t_i) for payer
                swap_cf_times = [t_m + (i + 1) * (1.0 / swap_freq) for i in range(int(round((swap_end - t_m) * swap_freq)))]
                r_m = alpha_m + j * dx
                p_t_end = math.exp(-hw_b(a, 0, swap_end - t_m) * (r_m - alpha_m)) * (discount_curve(swap_end) / discount_curve(t_m))
                annuity_val = sum(
                    (1.0 / swap_freq) * math.exp(-hw_b(a, 0, ti - t_m) * (r_m - alpha_m)) * (discount_curve(ti) / discount_curve(t_m))
                    for ti in swap_cf_times
                )
                swap_npv = (1.0 - p_t_end) - strike * annuity_val if is_payer else strike * annuity_val - (1.0 - p_t_end)
                intrinsic = max(0.0, swap_npv)

                val_berm_next[j] = max(c_berm, intrinsic)
                if is_first_ex:
                    val_euro_next[j] = max(c_euro, intrinsic)
                else:
                    val_euro_next[j] = c_euro
            else:
                val_berm_next[j] = c_berm
                val_euro_next[j] = c_euro

        val_berm = val_berm_next
        val_euro = val_euro_next

    berm_price = val_berm[0]
    euro_price = val_euro[0]
    premium = berm_price - euro_price
    return berm_price, euro_price, premium


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
    # Put-call parity: C - P = annuity * (F - K) = 0 when F == K
    assert abs(c - p) < 1e-12, f"ATM call-put parity failed: {c} vs {p}"
    assert c > 0.0, "Option price must be positive."

    # Test implied vol inverter
    imp_vol = implied_black_vol(c, f, k, t_exp, annuity, is_call=True)
    assert abs(imp_vol - vol) < 1e-6, f"Implied vol mismatch: {imp_vol} vs {vol}"

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
    # Exact CMS adjustment for 10y CMS fixing in 5y is ~15.93 bps
    adj_cms_bps = adj_cms * 10000.0
    assert abs(adj_cms_bps - 15.93004) < 1e-3, f"CMS adjustment out of expected range: {adj_cms_bps} bps"

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
    assert hw_swaption > 0.005, f"HW Jamshidian swaption price too small: {hw_swaption}"

    # 6. Hull-White Trinomial Tree Bermudan vs European
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
        dt=0.25,
    )
    assert berm_p >= euro_p, f"Bermudan swaption ({berm_p}) must be >= European ({euro_p})"
    assert premium >= 0.0, f"Early exercise premium must be non-negative: {premium}"

    print(f"Black-76 ATM 2y swaption price (A={annuity}): {c:.6f}")
    print(f"Bachelier normal 2y swaption price (vol=80bp): {bn_c:.6f}")
    print(f"SABR 1y ATM vol: {atm_vol * 100:.2f}%, 2% strike vol: {low_strike_vol * 100:.2f}%, 6% strike: {high_strike_vol * 100:.2f}%")
    print(f"Futures convexity adjustment: {adj_fut * 10000:.2f} bps")
    print(f"CMS 10y in 5y convexity adjustment: {adj_cms_bps:.2f} bps")
    print(f"Hull-White 1F 1y into 5y European swaption (Jamshidian): {hw_swaption:.6f}")
    print(f"Hull-White tree Bermudan 1y..4y into 5y: {berm_p:.6f}, European: {euro_p:.6f}, Premium: {premium:.6f}")
    print("All rates models tests passed successfully!")


if __name__ == "__main__":
    run_tests()
