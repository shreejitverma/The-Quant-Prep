"""Fixed income problem set: every number in the worked problems and cards, recomputed.

Backs every number in `06-Fixed-Income-and-Asset-Classes/25-Fixed-Income-Problem-Set.md` (Problems 1 to 22 and their cards).
Independent checks: bond yields are verified by repricing, the bootstrap by repricing every par bond, the Vasicek bond by
numerical integration of the short-rate distribution moments, the Hull-White option by put-call parity on the forward bond,
the CDS hazard by solving the premium and protection legs, SABR alpha by round trip, and the WAL by summing principal.
Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 06-Fixed-Income-and-Asset-Classes/code/fi_problem_set.py`.
"""

from __future__ import annotations

import math
from statistics import NormalDist

QUOTED: list[str] = []
N01 = NormalDist()


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


def bisect(fn, lo: float, hi: float, iters: int = 200) -> float:
    f_lo = fn(lo)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        f_mid = fn(mid)
        if (f_mid > 0.0) == (f_lo > 0.0):
            lo, f_lo = mid, f_mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def problem1() -> None:
    print("  Problem 1: accrued interest, dirty price, yield")
    f = 61 / 184
    quoted("accrual fraction", f, 0.331522, 6)
    ai = 2.25 * f
    quoted("accrued interest", ai, 0.745924, 6)
    dirty = 99.25 + ai
    quoted("dirty price", dirty, 99.995924, 6)

    def pv(y: float) -> float:
        v = 1.0 / (1.0 + y / 2.0)
        return sum(2.25 * v ** (1.0 - f + k) for k in range(10)) + 100.0 * v ** (1.0 - f + 9)

    y = bisect(lambda yy: pv(yy) - dirty, 0.0, 0.2)
    quoted("yield (% semi-annual)", y * 100.0, 4.674, 3)
    quoted("first coupon in periods", 1.0 - f, 0.668478, 6)
    assert abs(pv(y) - dirty) < 1e-9


def problem2() -> None:
    print("  Problem 2: Macaulay and modified duration, DV01")
    cfs = [50.0, 50.0, 1050.0]
    pvs = [c / 1.05 ** (i + 1) for i, c in enumerate(cfs)]
    for i, e in enumerate((47.6190, 45.3515, 907.0295)):
        quoted(f"PV year {i + 1}", pvs[i], e, 4)
    d_mac = sum((i + 1) * p for i, p in enumerate(pvs)) / sum(pvs)
    quoted("Macaulay duration", d_mac, 2.8594, 4)
    d_mod = d_mac / 1.05
    quoted("modified duration", d_mod, 2.72325, 5)
    quoted("DV01 per $10mm", 10_000_000.0 * d_mod * 1e-4, 2723.25, 2)
    # Independent: central difference of the price.
    price = lambda y: sum(c / (1.0 + y) ** (i + 1) for i, c in enumerate(cfs))  # noqa: E731
    numeric = (price(0.05 - 1e-6) - price(0.05 + 1e-6)) / (2e-6) / price(0.05)
    assert abs(numeric - d_mod) < 1e-6


def problem3() -> None:
    print("  Problem 3: duration and convexity approximation")
    quoted("duration term +150 bp", -7.5 * 100.0 * 0.015, -11.250, 3)
    conv = 0.5 * 68.0 * 100.0 * 0.015**2
    quoted("convexity term", conv, 0.765, 3)
    quoted("estimate +150 bp", -11.25 + conv, -10.485, 3)
    quoted("estimate -150 bp", 11.25 + conv, 12.015, 3)


def problem4_5() -> tuple[float, float, float]:
    print("  Problems 4 and 5: bootstrap, par swap rate, swap DV01")
    p1 = 1.0 / 1.03
    p2 = (100.0 - 3.5 * p1) / 103.5
    p3 = (100.0 - 4.0 * (p1 + p2)) / 104.0
    quoted("P(0,1)", p1, 0.970874, 6)
    quoted("P(0,2)", p2, 0.933352, 6)
    quoted("P(0,3)", p3, 0.888299, 6)
    quoted("z3 (% continuous)", -math.log(p3) / 3.0 * 100.0, 3.948, 3)
    quoted("continuous equivalent of a 4% annual rate (%)", math.log(1.04) * 100.0, 3.922, 3)
    for coupon, dfs in ((3.0, [p1]), (3.5, [p1, p2]), (4.0, [p1, p2, p3])):
        assert abs(coupon * sum(dfs) + 100.0 * dfs[-1] - 100.0) < 1e-9, "bootstrap must reprice every par bond"
    annuity = p1 + p2 + p3
    quoted("annuity", annuity, 2.792525, 6)
    quoted("3y par swap rate (%)", (1.0 - p3) / annuity * 100.0, 4.0000, 4)
    quoted("swap PV01 per $100mm", 100_000_000.0 * annuity * 1e-4, 27925.25, 2)
    return p1, p2, p3


def problem6() -> None:
    print("  Problem 6: Vasicek bond")
    a, b, sigma, r0, t = 0.15, 0.05, 0.015, 0.035, 5.0
    big_b = (1.0 - math.exp(-a * t)) / a
    quoted("B(0,5)", big_b, 3.517556, 6)
    term1 = (big_b - t) * (b - sigma**2 / (2.0 * a * a))
    term2 = -(sigma**2) * big_b**2 / (4.0 * a)
    quoted("first term", term1, -0.066710, 6)
    quoted("second term", term2, -0.004640, 6)
    quoted("ln A(0,5)", term1 + term2, -0.071350, 6)
    price = math.exp(term1 + term2 - big_b * r0)
    quoted("P(0,5)", price, 0.82328, 5)
    quoted("yield (%)", -math.log(price) / t * 100.0, 3.889, 3)
    # Independent: the integral of r is Gaussian; compute its mean and variance by quadrature of the OU moments.
    n = 2000
    h = t / n
    mean_int = sum(b + (r0 - b) * math.exp(-a * (i + 0.5) * h) for i in range(n)) * h
    var_int = sum((sigma * (1.0 - math.exp(-a * (t - (i + 0.5) * h))) / a) ** 2 for i in range(n)) * h
    assert abs(math.exp(-mean_int + 0.5 * var_int) - price) < 1e-6


def problem7() -> None:
    print("  Problem 7: Hull-White zero-coupon bond option")
    a, sigma, t1, t2, k, p1, p4 = 0.10, 0.012, 1.0, 4.0, 0.95, 0.96, 0.84
    sigma_p = sigma / a * (1.0 - math.exp(-a * (t2 - t1))) * math.sqrt((1.0 - math.exp(-2.0 * a * t1)) / (2.0 * a))
    quoted("sigma_P", sigma_p, 0.029610, 6)
    fwd = p4 / p1
    quoted("forward bond price", fwd, 0.8750, 4)
    d1 = (math.log(fwd / k) + 0.5 * sigma_p**2) / sigma_p
    quoted("d1", d1, -2.7626, 4)
    quoted("d2", d1 - sigma_p, -2.7922, 4)
    call = p1 * (fwd * N01.cdf(d1) - k * N01.cdf(d1 - sigma_p))
    quoted("call x 1e5", call * 1e5, 2.127, 3)
    put = p1 * (k * N01.cdf(-(d1 - sigma_p)) - fwd * N01.cdf(-d1))
    assert abs((call - put) - (p4 - k * p1)) < 1e-12, "put-call parity on the forward bond"


def problem8() -> None:
    print("  Problem 8: Black-76 caplet")
    f, k, vol, t, tau, df, notional = 0.045, 0.0425, 0.22, 1.0, 0.5, 0.935, 10_000_000.0
    d1 = (math.log(f / k) + 0.5 * vol * vol * t) / (vol * math.sqrt(t))
    quoted("d1", d1, 0.3698, 4)
    quoted("d2", d1 - vol, 0.1498, 4)
    fwd_payoff = f * N01.cdf(d1) - k * N01.cdf(d1 - vol)
    quoted("F N(d1) - K N(d2)", fwd_payoff, 0.005210, 6)
    quoted("caplet ($)", notional * df * tau * fwd_payoff, 24_357.41, 2)


def problem9() -> None:
    print("  Problem 9: ATM Bachelier swaption")
    quoted("sigma_N sqrt(T) / sqrt(2 pi) (bp)", 0.0065 / math.sqrt(2.0 * math.pi) * 1e4, 25.93, 2)
    quoted("premium ($)", 50_000_000.0 * 4.45 * 0.0065 / math.sqrt(2.0 * math.pi), 576_970.27, 2)


def cds_legs(hazard: float, rate: float, recovery: float, maturity: float) -> tuple[float, float]:
    """(RPV01, protection PV): quarterly premiums with half-period accrual on default, default settled mid-period."""
    rpv01 = prot = 0.0
    for i in range(int(round(maturity * 4))):
        t0, t1 = i / 4.0, (i + 1) / 4.0
        q0, q1 = math.exp(-hazard * t0), math.exp(-hazard * t1)
        rpv01 += 0.25 * math.exp(-rate * t1) * (q1 + 0.5 * (q0 - q1))
        prot += (1.0 - recovery) * math.exp(-rate * 0.5 * (t0 + t1)) * (q0 - q1)
    return rpv01, prot


def problem10() -> None:
    print("  Problem 10: CDS hazard and upfront")
    spread, recovery, rate = 0.015, 0.40, 0.04
    quoted("credit triangle hazard (%)", spread / (1.0 - recovery) * 100.0, 2.50, 2)
    quoted("survival to 5y at 2.5% (%)", math.exp(-0.025 * 5.0) * 100.0, 88.25, 2)
    hazard = bisect(lambda h: cds_legs(h, rate, recovery, 5.0)[1] - spread * cds_legs(h, rate, recovery, 5.0)[0], 1e-6, 0.5)
    quoted("bootstrapped flat hazard (%)", hazard * 100.0, 2.4875, 4)
    quoted("survival to 5y at that hazard (%)", math.exp(-hazard * 5.0) * 100.0, 88.30, 2)
    rpv01, prot = cds_legs(hazard, rate, recovery, 5.0)
    quoted("RPV01", rpv01, 4.2487, 4)
    upfront = prot - 0.01 * rpv01
    quoted("upfront at a 100 bp coupon (%)", upfront * 100.0, 2.12, 2)
    quoted("upfront on $10mm ($)", upfront * 10_000_000.0, 212_437.0, 0)
    assert abs(upfront - (spread - 0.01) * rpv01) < 1e-12


def problem11() -> None:
    print("  Problem 11: gross basis")
    inv_a, inv_b = 108.5 * 1.085, 108.5 * 1.215
    quoted("invoice A", inv_a, 117.7225, 4)
    quoted("invoice B", inv_b, 131.8275, 4)
    quoted("gross basis A", 118.25 - inv_a, 0.5275, 4)
    quoted("gross basis B", 132.50 - inv_b, 0.6725, 4)


def problem12() -> None:
    print("  Problem 12: rate paid at its fixing date")
    adj = 0.04**2 * 0.2**2 * 0.5 * 2.0 / (1.0 + 0.5 * 0.04)
    quoted("adjustment (bp)", adj * 1e4, 0.63, 2)
    quoted("adjusted rate (%)", (0.04 + adj) * 100.0, 4.0063, 4)


def sabr_atm(alpha: float, f: float, t: float, beta: float, rho: float, nu: float) -> float:
    gamma = (1 - beta) ** 2 / 24 * alpha**2 / f ** (2 - 2 * beta)
    gamma += rho * beta * nu * alpha / (4 * f ** (1 - beta)) + (2 - 3 * rho**2) / 24 * nu**2
    return alpha / f ** (1 - beta) * (1 + gamma * t)


def problem13() -> None:
    print("  Problem 13: SABR ATM vol")
    t1 = 0.25 / 24.0 * 0.02**2 / 0.04
    t2 = 0.25 * (-0.25) * 0.5 * 0.4 * 0.02 / 0.2
    t3 = (2.0 - 3.0 * 0.0625) / 24.0 * 0.16
    quoted("term 1", t1, 0.000104, 6)
    quoted("term 2", t2, -0.001250, 6)
    quoted("term 3", t3, 0.012083, 6)
    quoted("sum", t1 + t2 + t3, 0.0109375, 7)
    quoted("ATM vol (%)", sabr_atm(0.02, 0.04, 2.0, 0.5, -0.25, 0.4) * 100.0, 10.22, 2)


def problem14_15() -> None:
    print("  Problems 14 and 15: TIPS and prepayment")
    quoted("exact breakeven (%)", (1.0425 / 1.0185 - 1.0) * 100.0, 2.3564, 4)
    quoted("index ratio", 315.0 / 300.0, 1.0500, 4)
    quoted("TIPS coupon on $100k ($)", 0.01 * 100_000.0 * 315.0 / 300.0, 1050.00, 2)
    quoted("CPR from SMM 0.5% (%)", (1.0 - 0.995**12) * 100.0, 5.84, 2)
    quoted("100 PSA month 10 (%)", 0.2 * 10, 2.0, 1)
    quoted("150 PSA month 30 (%)", 1.5 * 6.0, 9.0, 1)


def problem16() -> None:
    print("  Problem 16: copula stress and P&L")
    p, rho = 0.05, 0.30
    q = N01.cdf((N01.inv_cdf(p) - math.sqrt(rho) * -2.0) / math.sqrt(1.0 - rho))
    quoted("p(M = -2) (%)", q * 100.0, 25.57, 2)
    quoted("conditional loss (%)", 0.6 * q * 100.0, 15.34, 2)
    gamma = 0.5 * 3_500_000_000.0 * 0.0008**2
    quoted("gamma P&L ($)", gamma, 1120.00, 2)
    quoted("total P&L ($)", -35_000.0 * 8.0 + gamma + 1200.0, -277_680.00, 2)


def problem17() -> None:
    print("  Problem 17: SABR alpha from an ATM quote")
    f, t, beta, rho, nu, target = 0.03, 2.0, 0.5, -0.30, 0.50, 0.20
    alpha = bisect(lambda a: sabr_atm(a, f, t, beta, rho, nu) - target, 1e-6, 0.2)
    quoted("first guess sigma_ATM F^(1-beta)", target * math.sqrt(f), 0.034641, 6)
    quoted("alpha", alpha, 0.033647, 6)
    quoted("1 + Gamma T at that alpha", target * math.sqrt(f) / alpha, 1.029543, 6)
    assert abs(sabr_atm(alpha, f, t, beta, rho, nu) - target) < 1e-12


def problem18() -> None:
    print("  Problem 18: HJM and LMM drifts")
    drift = 0.01**2 / 0.05 * math.exp(-0.25) * (1 - math.exp(-0.25))
    quoted("Hull-White HJM drift, sigma 1%, a 0.05, T - t = 5 (x 1e4)", drift * 1e4, 3.4454, 4)
    mu = -(0.5 * 0.05 / 1.025) * 0.25 * 0.20 * 0.9
    quoted("LMM terminal drift per year (%)", mu * 100.0, -0.1098, 4)


def problem19() -> None:
    print("  Problem 19: pool WAL at 200 PSA")
    balance, wac, coupon = 100.0, 0.06, 0.055
    principal = []
    for month in range(1, 361):
        rate = wac / 12.0
        payment = balance * rate / (1.0 - (1.0 + rate) ** -(361 - month))
        sched = payment - balance * rate
        cpr = min(month, 30) * 0.002 * 2.0
        prepay = (1.0 - (1.0 - cpr) ** (1.0 / 12.0)) * (balance - sched)
        principal.append(sched + prepay)
        balance -= sched + prepay
    quoted("SMM at 12% CPR (%)", (1.0 - 0.88 ** (1.0 / 12.0)) * 100.0, 1.0596, 4)
    quoted("WAL at 200 PSA (years)", sum((m + 1) / 12.0 * x for m, x in enumerate(principal)) / sum(principal), 7.67, 2)
    assert abs(sum(principal) - 100.0) < 1e-6 and coupon < wac


def problem20() -> None:
    print("  Problem 20: asset swap of a premium bond")
    swap, years, cpn, y = 0.035, 5, 5.0, 0.042
    dfs = [(1.0 + swap) ** -(i + 1) for i in range(years)]
    annuity = sum(dfs)
    price = sum(cpn / (1.0 + y) ** (i + 1) for i in range(years)) + 100.0 / (1.0 + y) ** years
    p_swap = sum(cpn * d for d in dfs) + 100.0 * dfs[-1]
    quoted("bond price", price, 103.5415, 4)
    quoted("price on the swap curve", p_swap, 106.7726, 4)
    quoted("annuity", annuity, 4.5151, 4)
    par_par = (p_swap - price) / (100.0 * annuity)
    quoted("par-par spread (bp)", par_par * 1e4, 71.56, 2)
    quoted("market-value spread (bp)", par_par * 100.0 / price * 1e4, 69.11, 2)


def problem21() -> None:
    print("  Problem 21: carry and roll-down breakeven")
    carry_bp = (0.0400 - 0.0350) * 0.25 / 4.5 * 1e4
    roll_bp = 10.0 * 0.25
    quoted("carry in yield bp", carry_bp, 2.78, 2)
    quoted("roll-down in yield bp", roll_bp, 2.50, 2)
    quoted("breakeven yield rise (bp)", carry_bp + roll_bp, 5.28, 2)


def problem22() -> None:
    print("  Problem 22: lognormal to normal vol")
    f, vol, t = 0.02, 0.25, 4.0
    quoted("sigma_B F (bp)", vol * f * 1e4, 50.00, 2)
    approx = vol * f * (1.0 - vol * vol * t / 24.0)
    quoted("second-order normal vol (bp)", approx * 1e4, 49.48, 2)
    sd = vol * math.sqrt(t)
    black_atm = f * (2.0 * N01.cdf(0.5 * sd) - 1.0)
    exact = black_atm / math.sqrt(t / (2.0 * math.pi))
    quoted("exact normal vol (bp)", exact * 1e4, 49.48, 2)


def intermediates() -> None:
    """Intermediate figures shown in the written solutions of Problems 1 to 16."""
    print("  Intermediate figures quoted in the solutions")
    f = 61 / 184
    quoted("P1 first coupon (periods, 4 dp)", 1.0 - f, 0.6685, 4)
    quoted("P1 last cash flow (periods)", 9.0 + 1.0 - f, 9.6685, 4)
    dirty = 99.25 + 2.25 * f
    y = bisect(
        lambda yy: sum(2.25 / (1.0 + yy / 2.0) ** (1.0 - f + k) for k in range(10)) + 100.0 / (1.0 + yy / 2.0) ** (10.0 - f) - dirty,
        0.0,
        0.2,
    )
    quoted("P1 semi-annual yield per period (%)", y / 2.0 * 100.0, 2.337, 3)
    pvs = [50.0 / 1.05, 50.0 / 1.05**2, 1050.0 / 1.05**3]
    quoted("P2 2 x PV2", 2.0 * pvs[1], 90.7029, 4)
    quoted("P2 3 x PV3", 3.0 * pvs[2], 2721.0884, 4)
    quoted("P2 weighted sum", pvs[0] + 2.0 * pvs[1] + 3.0 * pvs[2], 2859.4104, 4)
    quoted("P2 Macaulay (5 dp)", (pvs[0] + 2.0 * pvs[1] + 3.0 * pvs[2]) / 1000.0, 2.85941, 5)
    quoted("P3 0.5 C P", 0.5 * 68.0 * 100.0, 3400.0, 0)
    quoted("P3 dy^2", 0.015**2, 0.000225, 6)
    quoted("P3 price estimate up", 100.0 - 11.25 + 0.765, 89.515, 3)
    quoted("P3 price estimate down", 100.0 + 11.25 + 0.765, 112.015, 3)
    p1 = 1.0 / 1.03
    p2 = (100.0 - 3.5 * p1) / 103.5
    p3 = (100.0 - 4.0 * (p1 + p2)) / 104.0
    quoted("P4 3.5 P(0,1)", 3.5 * p1, 3.398058, 6)
    quoted("P4 100 - 3.5 P(0,1)", 100.0 - 3.5 * p1, 96.601942, 6)
    quoted("P4 P(0,1) + P(0,2)", p1 + p2, 1.904226, 6)
    quoted("P4 4 (P(0,1) + P(0,2))", 4.0 * (p1 + p2), 7.616904, 6)
    quoted("P4 100 - 4 (P(0,1) + P(0,2))", 100.0 - 4.0 * (p1 + p2), 92.383096, 6)
    quoted("P4 ln P(0,3)", math.log(p3), -0.118447, 6)
    quoted("P4 z3", -math.log(p3) / 3.0, 0.039482, 6)
    quoted("P5 1 - P(0,3)", 1.0 - p3, 0.111701, 6)
    a, b, sigma, r0 = 0.15, 0.05, 0.015, 0.035
    big_b = (1.0 - math.exp(-0.75)) / a
    quoted("P6 exp(-0.75)", math.exp(-0.75), 0.472367, 6)
    quoted("P6 1 - exp(-0.75)", 1.0 - math.exp(-0.75), 0.527633, 6)
    quoted("P6 b - sigma^2 / (2 a^2)", b - sigma**2 / (2.0 * a * a), 0.0450, 4)
    quoted("P6 B - T", big_b - 5.0, -1.482444, 6)
    quoted("P6 B^2", big_b**2, 12.3732, 4)
    quoted("P6 sigma^2 B^2", sigma**2 * big_b**2, 0.002784, 6)
    ln_a = (big_b - 5.0) * (b - sigma**2 / (2.0 * a * a)) - sigma**2 * big_b**2 / (4.0 * a)
    quoted("P6 A(0,5)", math.exp(ln_a), 0.931136, 6)
    quoted("P6 -B r0", -big_b * r0, -0.123114, 6)
    quoted("P6 exp(-B r0)", math.exp(-big_b * r0), 0.884162, 6)
    price = math.exp(ln_a - big_b * r0)
    quoted("P6 P(0,5) (6 dp)", price, 0.823275, 6)
    quoted("P6 ln P(0,5)", math.log(price), -0.194464, 6)
    quoted("P6 yield", -math.log(price) / 5.0, 0.038893, 6)
    quoted("P7 exp(-0.30)", math.exp(-0.30), 0.740818, 6)
    quoted("P7 1 - exp(-0.30)", 1.0 - math.exp(-0.30), 0.259182, 6)
    quoted("P7 exp(-0.20)", math.exp(-0.20), 0.818731, 6)
    quoted("P7 1 - exp(-0.20)", 1.0 - math.exp(-0.20), 0.181269, 6)
    quoted("P7 (1 - exp(-0.20)) / 0.20", (1.0 - math.exp(-0.20)) / 0.20, 0.906346, 6)
    quoted("P7 sqrt of that", math.sqrt((1.0 - math.exp(-0.20)) / 0.20), 0.952022, 6)
    quoted("P7 F_B / K", 0.875 / 0.95, 0.921053, 6)
    quoted("P7 ln(F_B / K)", math.log(0.875 / 0.95), -0.082238, 6)
    sp = 0.12 * (1.0 - math.exp(-0.30)) * math.sqrt((1.0 - math.exp(-0.20)) / 0.20)
    quoted("P7 0.5 sigma_P^2", 0.5 * sp * sp, 0.000438, 6)
    quoted("P7 d1 numerator", math.log(0.875 / 0.95) + 0.5 * sp * sp, -0.081800, 6)
    d1 = (math.log(0.875 / 0.95) + 0.5 * sp * sp) / sp
    quoted("P7 N(d1)", N01.cdf(d1), 0.0028671, 7)
    quoted("P7 N(d2)", N01.cdf(d1 - sp), 0.0026174, 7)
    quoted("P7 F_B N(d1)", 0.875 * N01.cdf(d1), 0.0025087, 7)
    quoted("P7 K N(d2)", 0.95 * N01.cdf(d1 - sp), 0.0024865, 7)
    quoted("P7 bracket", 0.875 * N01.cdf(d1) - 0.95 * N01.cdf(d1 - sp), 0.00002216, 8)
    quoted("P8 F / K", 0.045 / 0.0425, 1.058824, 6)
    quoted("P8 ln(F / K)", math.log(0.045 / 0.0425), 0.057158, 6)
    quoted("P8 0.5 sigma^2 T", 0.5 * 0.22**2, 0.024200, 6)
    quoted("P8 d1 numerator", math.log(0.045 / 0.0425) + 0.0242, 0.081358, 6)
    d1c = (math.log(0.045 / 0.0425) + 0.0242) / 0.22
    quoted("P8 N(d1)", N01.cdf(d1c), 0.6442383, 7)
    quoted("P8 N(d2)", N01.cdf(d1c - 0.22), 0.5595431, 7)
    quoted("P8 F N(d1)", 0.045 * N01.cdf(d1c), 0.028990725, 9)
    quoted("P8 K N(d2)", 0.0425 * N01.cdf(d1c - 0.22), 0.023780583, 9)
    quoted("P8 bracket (9 dp)", 0.045 * N01.cdf(d1c) - 0.0425 * N01.cdf(d1c - 0.22), 0.005210142, 9)
    quoted("P8 N x DF x tau", 10_000_000.0 * 0.935 * 0.5, 4_675_000.0, 0)
    quoted("P9 1 / sqrt(2 pi)", 1.0 / math.sqrt(2.0 * math.pi), 0.398942, 6)
    quoted("P9 sigma_N / sqrt(2 pi)", 0.0065 / math.sqrt(2.0 * math.pi), 0.0025931, 7)
    quoted("P10 upfront (6 dp, at RPV01 4.2487)", 0.005 * 4.2487, 0.021244, 6)
    quoted("P12 F^2", 0.04**2, 0.0016, 4)
    quoted("P12 1 + tau F", 1.0 + 0.5 * 0.04, 1.020, 3)
    quoted("P12 adjustment", 0.000064 / 1.02, 0.00006275, 8)
    quoted("P13 (1 - beta)^2 / 24", 0.25 / 24.0, 0.010417, 6)
    quoted("P13 rho beta nu / 4", 0.25 * -0.25 * 0.5 * 0.4, -0.0125, 4)
    quoted("P13 3 rho^2", 3.0 * 0.0625, 0.1875, 4)
    quoted("P13 2 - 3 rho^2", 2.0 - 0.1875, 1.8125, 4)
    quoted("P13 (2 - 3 rho^2) / 24", 1.8125 / 24.0, 0.075521, 6)
    quoted("P13 multiplier", 1.0 + 0.0109375 * 2.0, 1.021875, 6)
    quoted("P14 (1 + y_nom) / (1 + y_real)", 1.0425 / 1.0185, 1.023564, 6)
    quoted("P16 Phi^-1(0.05)", N01.inv_cdf(0.05), -1.644854, 6)
    quoted("P16 sqrt(0.3) x 2", math.sqrt(0.3) * 2.0, 1.095445, 6)
    quoted("P16 numerator", N01.inv_cdf(0.05) + math.sqrt(0.3) * 2.0, -0.549409, 6)
    quoted("P16 sqrt(0.7)", math.sqrt(0.7), 0.836660, 6)
    quoted("P16 argument", (N01.inv_cdf(0.05) + math.sqrt(0.3) * 2.0) / math.sqrt(0.7), -0.656669, 6)
    quoted("P16 p(M = -2), 4 dp", N01.cdf((N01.inv_cdf(0.05) + math.sqrt(0.3) * 2.0) / math.sqrt(0.7)), 0.2557, 4)
    quoted("P16 0.5 C$", 0.5 * 3_500_000_000.0, 1_750_000_000.0, 0)
    quoted("P16 dy^2 x 1e7", 0.0008**2 * 1e7, 6.4, 1)
    quoted("P16 delta P&L", -35_000.0 * 8.0, -280_000.0, 0)
    quoted("P22 1 - sigma^2 T / 24", 1.0 - 0.0625 * 4.0 / 24.0, 0.98958, 5)


def main() -> None:
    print("=== fi_problem_set: Fixed Income Problem Set ===")
    problem1()
    problem2()
    problem3()
    problem4_5()
    problem6()
    problem7()
    problem8()
    problem9()
    problem10()
    problem11()
    problem12()
    problem13()
    problem14_15()
    problem16()
    problem17()
    problem18()
    problem19()
    problem20()
    problem21()
    problem22()
    intermediates()
    print(f"\nSuccessfully verified {len(QUOTED)} problem set figures.")


if __name__ == "__main__":
    main()
