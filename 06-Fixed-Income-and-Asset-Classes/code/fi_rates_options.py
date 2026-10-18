"""Black-76 and Bachelier caplets and swaptions: parity, Greeks, vol conversion, stripping, SOFR caplets.

Backs every number in note 05 (Rates Options: Caps and Swaptions).
Closed forms are checked against Monte Carlo of the terminal distribution, finite-difference Greeks,
put-call parity and repricing after stripping; the backward-looking SOFR caplet variance is checked
by simulating the averaged rate.
Each `q(...)` asserts a computed value against the literal quoted in the note and prints it.
Run with `python 06-Fixed-Income-and-Asset-Classes/code/fi_rates_options.py`.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from statistics import NormalDist

import numpy as np

N01 = NormalDist()


def q(tag: str, label: str, value: float, text: str) -> None:
    """Assert that `value` rounds to the quoted `text` (half a unit of its last decimal) and print it."""
    decimals = len(text.split(".")[1]) if "." in text else 0
    literal = float(text.replace(",", ""))
    assert abs(value - literal) <= 0.5 * 10.0**-decimals + 1e-12, f"[{tag}] {label}: computed {value!r}, note quotes {text}"
    print(f"  [{tag}] {label} = {text}")


def black(f: float, k: float, vol: float, t: float, annuity: float, call: bool = True) -> float:
    if f <= 0 or k <= 0:
        raise ValueError("Black-76 needs a positive forward and strike")
    sd = vol * math.sqrt(t)
    d1 = math.log(f / k) / sd + 0.5 * sd
    d2 = d1 - sd
    if call:
        return annuity * (f * N01.cdf(d1) - k * N01.cdf(d2))
    return annuity * (k * N01.cdf(-d2) - f * N01.cdf(-d1))


def bachelier(f: float, k: float, vol_n: float, t: float, annuity: float, call: bool = True) -> float:
    sd = vol_n * math.sqrt(t)
    d = (f - k) / sd
    if call:
        return annuity * ((f - k) * N01.cdf(d) + sd * N01.pdf(d))
    return annuity * ((k - f) * N01.cdf(-d) + sd * N01.pdf(d))


def solve_increasing(fn: Callable[[float], float], target: float, lo: float, hi: float) -> float:
    """Bisection for an increasing function; asserts the bracket."""
    assert fn(lo) < target < fn(hi), (fn(lo), target, fn(hi))
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if fn(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main() -> None:
    print("Note 05: Rates Options: Caps and Swaptions")
    rng = np.random.default_rng(2026)

    # --- Example 1: Black ATM payer swaption (cards fi-rates-options-payer-delta, fi-rates-options-vega-black-vs-norm)
    f, k, vol, t, a = 0.04, 0.04, 0.25, 2.0, 3.80
    sd = vol * math.sqrt(t)
    d1 = 0.5 * sd
    q("ex1", "sigma sqrt(T)", sd, "0.353553")
    q("ex1", "d1", d1, "0.176777")
    q("ex1", "N(d1)", N01.cdf(d1), "0.570158")
    q("ex1", "N(d2)", N01.cdf(-d1), "0.429842")
    payer = black(f, k, vol, t, a)
    q("ex1", "ATM payer swaption", payer, "0.021328")
    q("ex1", "ATM payer swaption, bp of notional", 1e4 * payer, "213.28")
    z = rng.standard_normal(1_000_000)
    s_t = f * np.exp(-0.5 * sd * sd + sd * z)
    mc = a * np.maximum(s_t - k, 0.0)
    q("ex1", "Monte Carlo of the lognormal annuity-measure payoff, seed 2026", float(mc.mean()), "0.02133")
    assert abs(float(mc.mean()) - payer) < 4 * float(mc.std(ddof=1)) / 1000
    delta = a * N01.cdf(d1)
    h = 1e-6
    fd_delta = (black(f + h, k, vol, t, a) - black(f - h, k, vol, t, a)) / (2 * h)
    assert abs(fd_delta - delta) < 1e-6
    q("fi-rates-options-payer-delta", "delta A N(d1)", delta, "2.1666")
    q("fi-rates-options-payer-delta", "delta per bp of swap rate on 100mm, USD", 1e8 * delta * 1e-4, "21,666")
    vega_b = a * f * math.sqrt(t) * N01.pdf(d1)
    fd_vega = (black(f, k, vol + 1e-6, t, a) - black(f, k, vol - 1e-6, t, a)) / 2e-6
    assert abs(fd_vega - vega_b) < 1e-7
    q("fi-rates-options-vega-black-vs-norm", "Black vega per 1 vol point on 100mm, USD", 1e8 * vega_b * 0.01, "84,427")

    # --- Example 2: Bachelier ATM with a negative forward (cards fi-rates-options-bachelier-atm-rule, fi-ro-straddle-price)
    fn, kn, vn = -0.0020, -0.0020, 0.0080
    bn = bachelier(fn, kn, vn, t, a)
    q("ex2", "sigma_N sqrt(T)", vn * math.sqrt(t), "0.011314")
    q("ex2", "sigma_N sqrt(T) / sqrt(2 pi)", vn * math.sqrt(t) / math.sqrt(2 * math.pi), "0.0045135")
    q("ex2", "ATM Bachelier payer", bn, "0.017151")
    q("ex2", "ATM Bachelier payer, bp", 1e4 * bn, "171.51")
    q("fi-rates-options-bachelier-atm-rule", "1/sqrt(2 pi)", 1 / math.sqrt(2 * math.pi), "0.3989")
    mc_n = a * np.maximum(fn + vn * math.sqrt(t) * z - kn, 0.0)
    q("ex2", "Monte Carlo of the normal payoff, seed 2026", float(mc_n.mean()), "0.01714")
    assert abs(float(mc_n.mean()) - bn) < 4 * float(mc_n.std(ddof=1)) / 1000
    q("fi-ro-straddle-price", "ATM straddle = 2 x ATM, Bachelier", 2 * bn, "0.034303")
    vega_n = a * math.sqrt(t) * N01.pdf(0.0)
    q("fi-rates-options-vega-black-vs-norm", "normal vega per 1 bp of normal vol on 100mm, USD", 1e8 * vega_n * 1e-4, "21,439")

    # --- Example 3: put-call parity, payer minus receiver = A (S - K) (card fi-ro-payer-receiver-parity)
    k2 = 0.045
    par = black(f, k2, vol, t, a) - black(f, k2, vol, t, a, call=False)
    q("fi-ro-payer-receiver-parity", "payer minus receiver at K = 4.5%", par, "-0.019000")
    assert abs(par - a * (f - k2)) < 1e-15
    parn = bachelier(fn, 0.003, vn, t, a) - bachelier(fn, 0.003, vn, t, a, call=False)
    assert abs(parn - a * (fn - 0.003)) < 1e-15

    # --- Example 4: normal versus lognormal volatility (cards fi-rates-options-vol-conversion, fi-ro-atm-conversion-exact)
    f4, s_ln = 0.04, 0.20
    q("fi-rates-options-vol-conversion", "rule of thumb F sigma_LN, bp", 1e4 * f4 * s_ln, "80")
    for t4, txt in ((1.0, "79.87"), (10.0, "78.69"), (30.0, "76.17")):
        exact = f4 * math.sqrt(2 * math.pi / t4) * (2 * N01.cdf(0.5 * s_ln * math.sqrt(t4)) - 1)
        q("fi-ro-atm-conversion-exact", f"exact ATM normal vol, T = {t4:g}, bp", 1e4 * exact, txt)
        # matches by construction the two ATM prices; check by repricing
        assert abs(bachelier(f4, f4, exact, t4, 1.0) - black(f4, f4, s_ln, t4, 1.0)) < 1e-15
    # away from the money: invert Black prices to normal vols
    for kk, txt in ((0.03, "69.41"), (0.05, "89.48")):
        p_b = black(f4, kk, s_ln, 1.0, 1.0, call=kk > f4)
        vn_imp = solve_increasing(lambda v, kk=kk: bachelier(f4, kk, v, 1.0, 1.0, call=kk > f4), p_b, 1e-6, 0.1)
        q("fi-ro-atm-conversion-exact", f"normal vol matching Black 20% at K = {kk:.0%}, bp", 1e4 * vn_imp, txt)
    q("ex4", "sqrt(F K) sigma at K = 3%, bp", 1e4 * math.sqrt(0.04 * 0.03) * s_ln, "69.28")
    q("ex4", "sqrt(F K) sigma at K = 5%, bp", 1e4 * math.sqrt(0.04 * 0.05) * s_ln, "89.44")

    # --- Example 5: when no Black vol exists (card fi-ro-black-vol-nonexistence)
    small_f = 0.0010
    price_n = bachelier(small_f, small_f, 0.0080, 2.0, 1.0)
    q("fi-ro-black-vol-nonexistence", "Bachelier ATM price per unit annuity, F = K = 0.10%", price_n, "0.0045135")
    assert price_n > small_f  # a Black call is worth less than A F for every vol, so no Black vol reproduces this price
    shift = 0.02
    vol_shift = solve_increasing(lambda v: black(small_f + shift, small_f + shift, v, 2.0, 1.0), price_n, 1e-6, 5.0)
    q("fi-ro-shifted-lognormal", "shifted (2%) Black vol matching it, %", 100 * vol_shift, "38.57")
    vol_shift_neg = solve_increasing(lambda v: black(fn + shift, kn + shift, v, 2.0, 1.0), bn / a, 1e-6, 5.0)
    q("fi-ro-shifted-lognormal", "shifted (2%) Black vol for Example 2, %", 100 * vol_shift_neg, "45.20")

    # --- Example 6: stripping a caplet volatility (card fi-ro-strip-calc, fi-rates-options-caplet-stripping)
    p1, p2, kc = 0.9615, 0.9200, 0.04
    f2 = p1 / p2 - 1
    q("fi-ro-strip-calc", "forward F(1,2)", f2, "0.045109")
    q("ex6", "price / P(0,2)", 0.0075 / p2, "0.008152")
    sig2 = solve_increasing(lambda v: black(f2, kc, v, 1.0, p2), 0.0075, 1e-4, 3.0)
    q("fi-ro-strip-calc", "stripped caplet vol, %", 100 * sig2, "30.81")
    dd1 = math.log(f2 / kc) / sig2 + 0.5 * sig2
    q("ex6", "d1", dd1, "0.544165")
    q("ex6", "d2", dd1 - sig2, "0.236060")
    q("ex6", "N(d1)", N01.cdf(dd1), "0.706836")
    q("ex6", "N(d2)", N01.cdf(dd1 - sig2), "0.593307")

    # --- Example 7: a cap, a floor and parity; bootstrapping caplet vols from flat cap vols
    dfs = {0: 1.0, 1: 0.9615, 2: 0.9200, 3: 0.8800, 4: 0.8400}  # hypothetical annual discount factors
    fwd = {i: dfs[i - 1] / dfs[i] - 1 for i in (2, 3, 4)}
    for i, txt in zip((2, 3, 4), ("4.5109", "4.5455", "4.7619"), strict=True):
        q("ex7", f"forward F({i - 1},{i}), %", 100 * fwd[i], txt)

    def caplet(i: int, v: float, call: bool = True) -> float:
        return black(fwd[i], kc, v, float(i - 1), dfs[i], call)

    cap = sum(caplet(i, 0.25) for i in (2, 3, 4))
    floor = sum(caplet(i, 0.25, call=False) for i in (2, 3, 4))
    swap = (dfs[1] - dfs[4]) - kc * (dfs[2] + dfs[3] + dfs[4])
    q("fi-rates-options-cap-floor-parity", "4y cap at 4%, flat 25% vol", cap, "0.024699")
    q("fi-rates-options-cap-floor-parity", "4y floor at 4%, flat 25% vol", floor, "0.008799")
    q("fi-rates-options-cap-floor-parity", "forward-starting payer swap value", swap, "0.015900")
    assert abs((cap - floor) - swap) < 1e-15
    flat = {2: 0.30, 3: 0.28, 4: 0.26}  # hypothetical flat cap vols by cap maturity
    stripped: dict[int, float] = {}
    for n in (2, 3, 4):
        target = sum(caplet(i, flat[n]) for i in range(2, n + 1))
        known = sum(caplet(i, stripped[i]) for i in range(2, n))
        stripped[n] = solve_increasing(lambda v, n=n: caplet(n, v), target - known, 1e-4, 3.0)
    for n, txt in zip((2, 3, 4), ("30.00", "26.56", "23.04"), strict=True):
        q("fi-rates-options-caplet-stripping", f"stripped caplet vol for the {n}y caplet, %", 100 * stripped[n], txt)
    for n in (2, 3, 4):  # every cap reprices with the stripped caplet vols
        assert abs(sum(caplet(i, stripped[i]) for i in range(2, n + 1)) - sum(caplet(i, flat[n]) for i in range(2, n + 1))) < 1e-12

    # --- Example 8: backward-looking SOFR caplet (card fi-ro-sofr-caplet-variance)
    ts, te, vol_n, fk = 1.0, 1.25, 0.0100, 0.04
    t_eff = ts + (te - ts) / 3
    q("fi-ro-sofr-caplet-variance", "effective expiry T_s + (T_e - T_s)/3, years", t_eff, "1.0833")
    forward_looking = bachelier(fk, fk, vol_n, ts, 1.0)
    backward_looking = bachelier(fk, fk, vol_n, t_eff, 1.0)
    q("ex8", "forward-looking caplet per unit tau P, bp", 1e4 * forward_looking, "39.89")
    q("ex8", "backward-looking caplet per unit tau P, bp", 1e4 * backward_looking, "41.52")
    n_days = 63
    w_ts = math.sqrt(ts) * rng.standard_normal(200_000)
    incr = rng.standard_normal((200_000, n_days)) * math.sqrt((te - ts) / n_days)
    path = w_ts[:, None] + np.cumsum(incr, axis=1)
    avg = fk + vol_n * path.mean(axis=1)
    pay = np.maximum(avg - fk, 0.0)
    q("ex8", "Monte Carlo of the averaged-rate caplet (63 daily fixings, seed 2026), bp", 1e4 * float(pay.mean()), "41.6")
    se = float(pay.std(ddof=1)) / math.sqrt(pay.size)
    # the discrete daily average has variance ts + (te - ts)(n+1)(2n+1)/(6 n^2), slightly above the continuous 1/3
    t_disc = ts + (te - ts) * (n_days + 1) * (2 * n_days + 1) / (6 * n_days**2)
    assert abs(float(pay.mean()) - bachelier(fk, fk, vol_n, t_disc, 1.0)) < 4 * se
    q("ex8", "discrete-average effective expiry, years", t_disc, "1.0853")

    print("All note 05 checks passed.")


if __name__ == "__main__":
    main()
