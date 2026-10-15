"""Credit Default Swaps, Hazard Rates, TIPS, and Mortgages Reference Implementation.

Pure Python 3.10+ standard library implementation:
1. Piecewise constant hazard rate bootstrapper from market CDS spreads.
2. CDS pricing, upfront fee (standard 100/500 bp coupons), RPV01, CS01, and JTD.
3. TIPS indexation, deflation floor, and breakeven inflation rate (BEIR).
4. Mortgage prepayment analytics: SMM, CPR, and 100% PSA prepayment schedule.
5. One-factor Gaussian copula portfolio default distribution and CDO tranche loss.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

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

    # Coefficients in rational approximations
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


# ============================================================================
# 1. CDS Hazard Rate Bootstrap
# ============================================================================


@dataclass
class CDSQuote:
    tenor: float  # maturity in years (e.g. 1.0, 3.0, 5.0, 10.0)
    spread: float  # par spread (e.g. 0.0100 for 100 bps)


class CDSHazardCurve:
    """Piecewise constant hazard rate curve bootstrapped from market CDS quotes."""

    def __init__(
        self,
        discount_curve: Callable[[float], float],
        quotes: Sequence[CDSQuote],
        recovery_rate: float = 0.40,
        payment_freq: int = 4,  # quarterly CDS payments
    ) -> None:
        self.discount_curve = discount_curve
        self.recovery_rate = recovery_rate
        self.lgd = 1.0 - recovery_rate
        self.payment_freq = payment_freq
        self.dt = 1.0 / payment_freq

        # Sort quotes by tenor
        self.quotes = sorted(quotes, key=lambda q: q.tenor)
        self.pillars: list[float] = [q.tenor for q in self.quotes]
        self.hazard_rates: list[float] = []

        self._bootstrap()

    def _bootstrap(self) -> None:
        for quote in self.quotes:
            # Solve for hazard rate lambda on (t_prev, t_curr] such that
            # PV_protection == par_spread * RPV01
            def objective(lam_guess: float, q: CDSQuote = quote) -> float:
                trial = self.hazard_rates + [lam_guess]
                rpv01_val, prot_val = self._legs(q.tenor, lambda t: self._survival(t, trial))
                return prot_val - q.spread * rpv01_val

            # Objective increases with lambda; bisect only on a bracketed root
            lam_low, lam_high = 0.0, 1.0
            if objective(lam_low) > 0.0 or objective(lam_high) < 0.0:
                raise ValueError(
                    f"CDS quote at tenor {quote.tenor}y needs a forward hazard rate outside "
                    f"[{lam_low}, {lam_high}]; the spread curve is not arbitrage-free or too distressed."
                )
            for _ in range(80):
                lam_mid = 0.5 * (lam_low + lam_high)
                if objective(lam_mid) > 0.0:
                    lam_high = lam_mid
                else:
                    lam_low = lam_mid
            self.hazard_rates.append(0.5 * (lam_low + lam_high))

    def _survival(self, t: float, hazard_rates: Sequence[float]) -> float:
        """Q(t) for piecewise constant hazards on the leading pillars, flat beyond the last one."""
        if t <= 0.0:
            return 1.0
        log_q = 0.0
        p_prev = 0.0
        for p_curr, lam in zip(self.pillars, hazard_rates, strict=False):
            if t <= p_curr:
                return math.exp(log_q - lam * (t - p_prev))
            log_q -= lam * (p_curr - p_prev)
            p_prev = p_curr
        return math.exp(log_q - hazard_rates[-1] * (t - p_prev))

    def survival_prob(self, t: float) -> float:
        """Evaluate survival probability Q(t) = P(tau > t)."""
        return self._survival(t, self.hazard_rates)

    def _legs(self, tenor: float, survival: Callable[[float], float]) -> tuple[float, float]:
        """(RPV01, PV_protection) with mid-period premium accrual and mid-point default settlement."""
        n_periods = int(round(tenor * self.payment_freq))
        rpv01_val = 0.0
        prot_val = 0.0
        for k in range(1, n_periods + 1):
            t_k = k * self.dt
            t_prev = (k - 1) * self.dt
            q_prev = survival(t_prev)
            q_k = survival(t_k)
            prob_default = q_prev - q_k
            rpv01_val += self.dt * self.discount_curve(t_k) * (q_k + 0.5 * prob_default)
            prot_val += self.lgd * self.discount_curve(0.5 * (t_prev + t_k)) * prob_default
        return rpv01_val, prot_val

    def rpv01(self, tenor: float) -> float:
        """Risky PV01 (present value of 1 basis point running premium per unit notional)."""
        return self._legs(tenor, self.survival_prob)[0]

    def upfront_fee(self, tenor: float, coupon: float) -> float:
        """Upfront fee as a percentage of notional for a standard coupon contract."""
        rpv01_val, prot_val = self._legs(tenor, self.survival_prob)
        # Upfront paid by protection buyer = PV_protection - Coupon * RPV01
        return prot_val - coupon * rpv01_val


# ============================================================================
# 2. TIPS and Inflation Breakeven
# ============================================================================


def breakeven_inflation_rate(nominal_yield: float, real_yield: float) -> float:
    """Exact Fisher-relation breakeven inflation rate: (1 + y_nom) / (1 + y_real) - 1."""
    return (1.0 + nominal_yield) / (1.0 + real_yield) - 1.0


def tips_index_ratio(cpi_ref: float, cpi_base: float) -> float:
    """Index ratio for TIPS principal inflation adjustment."""
    return cpi_ref / cpi_base


def tips_cash_flow(
    coupon_rate: float,
    base_principal: float,
    index_ratio: float,
    is_maturity: bool = False,
    semi_annual: bool = True,
) -> float:
    """Calculate TIPS coupon or principal payment with deflation floor."""
    freq = 2.0 if semi_annual else 1.0
    adj_principal = base_principal * index_ratio
    coupon_pmt = (coupon_rate / freq) * adj_principal
    if not is_maturity:
        return coupon_pmt
    # Deflation floor on redemption principal at maturity
    redemption_principal = max(base_principal, adj_principal)
    return coupon_pmt + redemption_principal


# ============================================================================
# 3. Mortgage Prepayment Mathematics (SMM, CPR, PSA)
# ============================================================================


def smm_to_cpr(smm: float) -> float:
    """Convert Single Monthly Mortality (SMM) to Constant Prepayment Rate (CPR)."""
    return 1.0 - (1.0 - smm) ** 12.0


def cpr_to_smm(cpr: float) -> float:
    """Convert Constant Prepayment Rate (CPR) to Single Monthly Mortality (SMM)."""
    return 1.0 - (1.0 - cpr) ** (1.0 / 12.0)


def psa_cpr(month: int, psa_speed: float = 100.0) -> float:
    """Evaluate CPR for a given month under the PSA benchmark (e.g. 100% PSA)."""
    if month <= 0:
        return 0.0
    base_cpr = 0.06 * (month / 30.0) if month <= 30 else 0.06
    return base_cpr * (psa_speed / 100.0)


# ============================================================================
# 4. One-Factor Gaussian Copula (David X. Li 2000)
# ============================================================================


def gaussian_copula_loss_distribution(
    default_prob: float,
    rho: float,
    recovery_rate: float = 0.40,
    n_quad_pts: int = 61,
) -> list[tuple[float, float]]:
    """Large homogeneous portfolio (N -> infinity) loss distribution under Li's one-factor Gaussian copula.

    Each quadrature node m of the market factor contributes its deterministic conditional
    loss (1 - R) * p(m) with probability weight phi(m) dm; there is no finite-N binomial term.

    Returns:
        List of (loss_fraction, probability) pairs.
    """
    if rho < 0.0 or rho >= 1.0:
        raise ValueError("Correlation rho must be in [0, 1).")
    sqrt_rho = math.sqrt(rho)
    sqrt_one_minus_rho = math.sqrt(1.0 - rho)
    k_thresh = norm_inv(default_prob)

    # Discretize standard normal market factor M via mid-point rule from -4.5 to +4.5
    m_min, m_max = -4.5, 4.5
    dm = (m_max - m_min) / n_quad_pts

    # Large homogeneous portfolio approximation: conditional default rate p(M)
    # p(M) = Phi( (Phi^{-1}(p) - sqrt(rho)*M) / sqrt(1 - rho) )
    loss_pdf: list[tuple[float, float]] = []
    lgd = 1.0 - recovery_rate

    for pt in range(n_quad_pts):
        m_val = m_min + (pt + 0.5) * dm
        weight = norm_pdf(m_val) * dm
        cond_p = norm_cdf((k_thresh - sqrt_rho * m_val) / sqrt_one_minus_rho)
        cond_loss = lgd * cond_p
        loss_pdf.append((cond_loss, weight))

    return loss_pdf


def tranche_expected_loss(
    loss_pdf: Sequence[tuple[float, float]],
    attachment: float,
    detachment: float,
) -> float:
    """Expected percentage loss on a synthetic CDO tranche [A, D]."""
    tranche_width = detachment - attachment
    if tranche_width <= 0.0:
        return 0.0

    exp_loss = 0.0
    for loss, prob in loss_pdf:
        # Tranche loss given portfolio loss L: min(D - A, max(0, L - A))
        t_loss = min(tranche_width, max(0.0, loss - attachment))
        exp_loss += (t_loss / tranche_width) * prob
    return exp_loss


def run_tests() -> None:
    print("Testing CDS bootstrap, TIPS, MBS prepayments, and Gaussian copula...")

    # Flat 4% discount curve
    def discount_curve(t: float) -> float:
        return math.exp(-0.04 * t)

    # 1. CDS Hazard Rate Bootstrap
    quotes = [
        CDSQuote(tenor=1.0, spread=0.0100),  # 100 bps
        CDSQuote(tenor=3.0, spread=0.0120),  # 120 bps
        CDSQuote(tenor=5.0, spread=0.0150),  # 150 bps
    ]
    cds_curve = CDSHazardCurve(discount_curve, quotes, recovery_rate=0.40)
    # Defining property: the bootstrapped curve reprices every input quote to par
    for q in quotes:
        par = cds_curve.upfront_fee(q.tenor, coupon=0.0) / cds_curve.rpv01(q.tenor)
        assert abs(par - q.spread) < 1e-8, f"{q.tenor}y quote not repriced: {par} vs {q.spread}"
    lam_5y = cds_curve.hazard_rates[-1]
    surv_5y = cds_curve.survival_prob(5.0)
    rpv01_5y = cds_curve.rpv01(5.0)
    # Upfront on a 100 bp coupon equals (par spread - coupon) * RPV01 at the 5y pillar
    upfront = cds_curve.upfront_fee(5.0, coupon=0.0100)
    assert abs(upfront - (0.0150 - 0.0100) * rpv01_5y) < 1e-10, f"Upfront fee mismatch: {upfront}"

    # Flat single quote: closed-form constant hazard for quarterly legs with mid-period
    # accrual and mid-point protection. Per period the protection-to-premium ratio is
    # LGD * e^{r dt / 2} * (u - 1) / (dt / 2 * (u + 1)) with u = e^{lambda dt}, so
    # u = (LGD c + s dt / 2) / (LGD c - s dt / 2) with c = e^{r dt / 2}.
    s_flat, dt, lgd = 0.0150, 0.25, 0.60
    c = math.exp(0.5 * 0.04 * dt)
    lam_closed = math.log((lgd * c + 0.5 * s_flat * dt) / (lgd * c - 0.5 * s_flat * dt)) / dt
    flat_curve = CDSHazardCurve(discount_curve, [CDSQuote(tenor=5.0, spread=s_flat)], recovery_rate=0.40)
    assert abs(flat_curve.hazard_rates[0] - lam_closed) < 1e-12, f"Flat hazard mismatch: {flat_curve.hazard_rates[0]}"
    assert abs(flat_curve.survival_prob(5.0) - math.exp(-5.0 * lam_closed)) < 1e-12

    # A spread curve that needs a negative forward hazard must be rejected, not clamped
    try:
        CDSHazardCurve(discount_curve, [CDSQuote(1.0, 0.0300), CDSQuote(2.0, 0.0050)])
    except ValueError:
        pass
    else:
        raise AssertionError("Inverted curve implying a negative forward hazard was not rejected")

    # 2. TIPS and Inflation
    beir = breakeven_inflation_rate(nominal_yield=0.0425, real_yield=0.0185)
    # Expected: (1.0425 / 1.0185) - 1 = 0.023564 = 2.36%
    assert abs(beir - 0.023564) < 1e-4, f"BEIR mismatch: {beir}"
    ir = tips_index_ratio(cpi_ref=315.0, cpi_base=300.0)
    assert abs(ir - 1.05) < 1e-6
    cf = tips_cash_flow(coupon_rate=0.02, base_principal=1000.0, index_ratio=1.05, is_maturity=True)
    # Coupon = 0.02 / 2 * 1050 = 10.50; Principal = 1050; Total = 1060.50
    assert abs(cf - 1060.50) < 1e-4

    # Deflation floor check: if index ratio drops to 0.95
    cf_def = tips_cash_flow(coupon_rate=0.02, base_principal=1000.0, index_ratio=0.95, is_maturity=True)
    # Coupon = 0.02 / 2 * 950 = 9.50; Principal floored at 1000; Total = 1009.50
    assert abs(cf_def - 1009.50) < 1e-4

    # 3. Mortgages: SMM to CPR and PSA
    smm = 0.005  # 0.5% monthly mortality
    cpr = smm_to_cpr(smm)
    # CPR = 1 - (1 - 0.005)^12 = 0.058428 (5.84%)
    assert abs(cpr - 0.058428) < 1e-4
    smm_rec = cpr_to_smm(cpr)
    assert abs(smm_rec - smm) < 1e-6

    # 100% PSA at month 10 = 0.06 * (10 / 30) = 0.02 (2.0% CPR)
    psa_m10 = psa_cpr(10, 100.0)
    assert abs(psa_m10 - 0.02) < 1e-6
    # 150% PSA at month 30 = 0.06 * 1.5 = 0.09 (9.0% CPR)
    psa_m30 = psa_cpr(30, 150.0)
    assert abs(psa_m30 - 0.09) < 1e-6

    # 4. One-Factor Gaussian Copula Tranche Loss
    loss_dist = gaussian_copula_loss_distribution(default_prob=0.05, rho=0.30, recovery_rate=0.40)
    # Total expected portfolio loss = default_prob * (1 - R) = 0.05 * 0.60 = 0.030 (3.0%)
    total_exp_loss = sum(loss * prob for loss, prob in loss_dist)
    assert abs(total_exp_loss - 0.030) < 1e-3, f"Total expected portfolio loss mismatch: {total_exp_loss}"

    # Equity tranche [0%, 3%] expected loss
    eq_loss = tranche_expected_loss(loss_dist, attachment=0.0, detachment=0.03)
    # Senior tranche [7%, 10%] expected loss
    sr_loss = tranche_expected_loss(loss_dist, attachment=0.07, detachment=0.10)
    assert eq_loss > sr_loss, f"Equity tranche loss must exceed senior: {eq_loss} vs {sr_loss}"

    print(f"5y CDS Hazard Rate: {lam_5y * 100:.2f}%, 5y Survival: {surv_5y * 100:.2f}%, 5y RPV01: {rpv01_5y:.2f}")
    print(f"5y CDS Upfront Fee (100bp coupon): {upfront * 100:.2f}% of notional")
    print(f"TIPS Breakeven Inflation Rate: {beir * 100:.2f}%")
    print(f"Mortgage 100% PSA month 10 CPR: {psa_m10 * 100:.1f}%, month 30 (150% PSA): {psa_m30 * 100:.1f}%")
    print(
        f"Gaussian Copula Portfolio Expected Loss: {total_exp_loss * 100:.2f}% "
        f"(Equity Tranche Loss: {eq_loss * 100:.2f}%, Senior: {sr_loss * 100:.2f}%)"
    )
    print("All credit, inflation, and securitized models tests passed!")


if __name__ == "__main__":
    run_tests()
