"""Fixed Income Credit Advanced CDS Indices and Tranches Reference Engine.

Asserts every quantitative figure quoted in Note 23
(23-Credit-Advanced-CDS-Indices-and-Tranches.md) to within half a unit
in the last quoted decimal place using standard-library pure Python.
"""

import math

SQRT_TWO = math.sqrt(2.0)
SQRT_TWO_PI = math.sqrt(2.0 * math.pi)


def norm_cdf(x: float) -> float:
    """Cumulative distribution function for standard normal N(0, 1)."""
    return 0.5 * (1.0 + math.erf(x / SQRT_TWO))


def norm_pdf(x: float) -> float:
    """Probability density function for standard normal N(0, 1)."""
    return math.exp(-0.5 * x * x) / SQRT_TWO_PI


def norm_inv(p: float) -> float:
    """Acklam's approximation for inverse standard normal CDF."""
    if p <= 0.0 or p >= 1.0:
        raise ValueError("Probability must be strictly between 0 and 1.")

    a = [
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    ]
    b = [
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464968e00,
        2.938163982698783e00,
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e00,
        3.754408661907416e00,
    ]

    q_low = 0.02425
    q_high = 1.0 - q_low

    if q_low <= p <= q_high:
        q = p - 0.5
        r = q * q
        return (
            (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5])
            * q
            / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0)
        )
    elif p < q_low:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0
        )
    else:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0
        )


def cds_index_upfront(
    par_spread: float,
    coupon: float,
    rpv01: float,
    notional: float,
) -> tuple[float, float, float]:
    """Calculate upfront fee fraction, upfront cash payment, and quoted dollar price.

    Returns:
        (upfront_fraction, upfront_cash, dollar_price)
    """
    upfront_fraction = (par_spread - coupon) * rpv01
    upfront_cash = upfront_fraction * notional
    dollar_price = 100.0 - (upfront_fraction * 100.0)
    return upfront_fraction, upfront_cash, dollar_price


def cds_index_basis(index_spread: float, single_name_spreads: list[float]) -> float:
    """Calculate CDS index basis: S_index - (1/N) * sum(S_i)."""
    avg_spread = sum(single_name_spreads) / len(single_name_spreads)
    return index_spread - avg_spread


def conditional_default_prob(p: float, rho: float, m: float) -> float:
    """Evaluate conditional default probability in one-factor Gaussian copula.

    p(m) = Phi( (Phi^{-1}(p) - sqrt(rho) * m) / sqrt(1 - rho) )
    """
    k = norm_inv(p)
    return norm_cdf((k - math.sqrt(rho) * m) / math.sqrt(1.0 - rho))


def tranche_loss_given_portfolio_loss(
    portfolio_loss: float,
    attachment: float,
    detachment: float,
) -> float:
    """Evaluate realized tranche loss fraction for tranche [A, D]."""
    width = detachment - attachment
    if width <= 0.0:
        return 0.0
    absorbed = min(detachment, max(attachment, portfolio_loss)) - attachment
    return absorbed / width


def gaussian_copula_loss_quadrature(
    p: float,
    rho: float,
    recovery: float,
    n_pts: int = 1000,
    m_range: float = 5.0,
) -> list[tuple[float, float]]:
    """Generate discrete (loss, weight) probability distribution under LHP."""
    lgd = 1.0 - recovery
    dm = 2.0 * m_range / n_pts
    distribution = []
    for i in range(n_pts):
        m = -m_range + (i + 0.5) * dm
        weight = norm_pdf(m) * dm
        cond_p = conditional_default_prob(p, rho, m)
        distribution.append((lgd * cond_p, weight))
    return distribution


def tranche_expected_loss(
    loss_dist: list[tuple[float, float]],
    attachment: float,
    detachment: float,
) -> float:
    """Calculate expected percentage loss of tranche [A, D] across loss distribution."""
    width = detachment - attachment
    if width <= 0.0:
        return 0.0
    total_expected = 0.0
    for loss, prob in loss_dist:
        t_loss = min(width, max(0.0, loss - attachment)) / width
        total_expected += t_loss * prob
    return total_expected


def base_correlation_loss(
    loss_0_to_d: float,
    loss_0_to_a: float,
    attachment: float,
    detachment: float,
) -> float:
    """Decompose tranche [A, D] expected loss into base tranches [0, D] and [0, A]."""
    return (detachment * loss_0_to_d - attachment * loss_0_to_a) / (detachment - attachment)


def main() -> None:
    # 1. CDS Index Upfront and Dollar Price (Example 1)
    notional = 50_000_000.0
    coupon = 0.0500  # 500 bps
    par_spread = 0.0420  # 420 bps
    rpv01 = 4.15
    upfront_frac, upfront_cash, dollar_price = cds_index_upfront(par_spread, coupon, rpv01, notional)

    assert round(upfront_frac * 100, 2) == -3.32, f"Expected -3.32%, got {upfront_frac * 100}"
    assert round(upfront_cash, 2) == -1_660_000.00, f"Expected -$1,660,000, got {upfront_cash}"
    assert round(dollar_price, 2) == 103.32, f"Expected 103.32, got {dollar_price}"

    # 2. CDS Index Basis
    idx_spread = 0.0065  # 65 bps
    single_names = [0.0060, 0.0065, 0.0070, 0.0075, 0.0070]  # mean 68 bps
    basis = cds_index_basis(idx_spread, single_names)
    assert round(basis * 10000, 1) == -3.0, f"Expected -3.0 bps, got {basis * 10000}"

    # 3. Gaussian Copula Stress Realization (Example 2)
    p = 0.05
    rho = 0.30
    recovery = 0.40
    lgd = 1.0 - recovery  # 0.60
    m_shock = -2.5

    cond_p = conditional_default_prob(p, rho, m_shock)
    assert round(cond_p * 100, 2) == 37.09, f"Expected 37.09%, got {cond_p * 100}"

    cond_loss = lgd * cond_p
    assert round(cond_loss * 100, 2) == 22.26, f"Expected 22.26%, got {cond_loss * 100}"

    # Tranche losses under M = -2.5
    eq_loss_realized = tranche_loss_given_portfolio_loss(cond_loss, 0.0, 0.03)
    sr_loss_realized = tranche_loss_given_portfolio_loss(cond_loss, 0.07, 0.10)
    assert eq_loss_realized == 1.0, f"Equity tranche should be 100% loss, got {eq_loss_realized}"
    assert sr_loss_realized == 1.0, f"Senior tranche should be 100% loss, got {sr_loss_realized}"

    # 4. Unconditional Expected Losses via Quadrature
    loss_dist = gaussian_copula_loss_quadrature(p, rho, recovery, n_pts=2000, m_range=5.0)

    # Total expected portfolio loss = p * lgd = 0.05 * 0.60 = 0.0300 (3.00%)
    total_loss = sum(loss * weight for loss, weight in loss_dist)
    assert round(total_loss * 100, 2) == 3.00, f"Expected 3.00%, got {total_loss * 100}"

    eq_exp = tranche_expected_loss(loss_dist, 0.0, 0.03)
    sr_exp = tranche_expected_loss(loss_dist, 0.07, 0.10)
    mezz_exp = tranche_expected_loss(loss_dist, 0.03, 0.07)

    assert round(eq_exp * 100, 2) == 54.11, f"Expected 54.11%, got {eq_exp * 100}"
    assert round(mezz_exp * 100, 2) == 19.58, f"Expected 19.58%, got {mezz_exp * 100}"
    assert round(sr_exp * 100, 2) == 8.78, f"Expected 8.78%, got {sr_exp * 100}"

    # 5. Base Correlation Decomposition Check
    # Tranche [3, 7%] from base [0, 7%] and [0, 3%]
    base_0_3 = tranche_expected_loss(loss_dist, 0.0, 0.03)
    base_0_7 = tranche_expected_loss(loss_dist, 0.0, 0.07)
    mezz_from_base = base_correlation_loss(base_0_7, base_0_3, 0.03, 0.07)
    assert abs(mezz_from_base - mezz_exp) < 1e-9, f"Base correlation decomposition mismatch: {mezz_from_base} vs {mezz_exp}"

    print("All fi_credit_tranches assertions passed successfully.")


if __name__ == "__main__":
    main()
