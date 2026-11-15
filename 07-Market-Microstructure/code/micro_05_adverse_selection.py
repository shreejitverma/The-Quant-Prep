"""Adverse selection and flow toxicity: every markout, spread split, Glosten-Milgrom quote, PIN and VPIN in the note.

Backs every number in `07-Market-Microstructure/05-Adverse-Selection-and-Flow-Toxicity.md`.
Independent routes used here:
- markouts from the fill table in exact `fractions.Fraction` arithmetic, size-weighted and unweighted;
- Glosten-Milgrom quotes by enumerating every (value, trader type, coin) outcome and conditioning on the
  observed order sequence, never via the closed-form half-spread mu (V_H - V_L) / 2;
- PIN by exact arithmetic and by simulating Poisson trade counts over many days;
- the normal CDF for bulk volume classification by Simpson integration of the density, checked against math.erf;
- the markout sample sizes by simulating the sampling distribution of the mean;
- the two-segment pricing example by exact arithmetic, including the break-even share of the toxic segment.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 07-Market-Microstructure/code/micro_05_adverse_selection.py`.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction as F

import numpy as np

SEED = 20261114


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol:.4f})")


def section_markouts() -> None:
    print("Example 1: a markout table (card ms-tox-markout-formula)")
    # side, size, price, mid at fill, mid +1 s, mid +60 s (dollars as exact fractions)
    fills = [
        (+1, 200, "25.00", "25.005", "25.000", "24.99"),
        (-1, 100, "25.02", "25.015", "25.020", "25.03"),
        (+1, 300, "25.01", "25.015", "25.015", "25.02"),
        (-1, 200, "25.03", "25.025", "25.030", "25.04"),
        (+1, 200, "24.99", "24.995", "24.985", "24.97"),
    ]
    total = sum(f[1] for f in fills)
    exact("total size", total, 1000)
    for col, name, per_fill_q, total_q, per_share_q in (
        (3, "at fill", [F(1, 2)] * 5, F(5, 1), F(1, 2)),
        (4, "at 1 s", [F(0), F(0), F(1, 2), F(0), F(-1, 2)], F(50, 1), F(1, 20)),
        (5, "at 60 s", [F(-1), F(-1), F(1), F(-1), F(-2)], F(-600, 1), F(-6, 10)),
    ):
        per_fill = [f[0] * (F(f[col]) - F(f[2])) * 100 for f in fills]  # cents per share
        exact(f"per-fill markouts {name} (cents)", per_fill, per_fill_q)
        weighted_cents = sum(m * f[1] for m, f in zip(per_fill, fills, strict=True))
        if col == 3:
            exact(f"size-weighted per share {name} (cents)", weighted_cents / total, per_share_q)
        else:
            exact(f"size-weighted total {name} (dollars)", weighted_cents / 100, total_q / 100)
            exact(f"size-weighted per share {name} (cents)", weighted_cents / total, per_share_q)
    exact("1 s total = 300 x 0.5 - 200 x 0.5 cents", 300 * F(1, 2) - 200 * F(1, 2), 50)
    exact("60 s total = -2 - 1 + 3 - 2 - 4 dollars", -2 - 1 + 3 - 2 - 4, -6)
    unweighted = sum(f[0] * (F(f[5]) - F(f[2])) * 100 for f in fills) / 5
    exact("unweighted 60 s average (cents)", unweighted, F(-4, 5))


def section_spread_split() -> None:
    print("Example 2: effective, realized and impact (card ms-tox-effective-realized-impact)")
    p, m0, m1 = F("25.02"), F("25.015"), F("25.03")
    eff, real, imp = p - m0, p - m1, m1 - m0
    exact("effective half-spread", eff, F("0.005"))
    exact("realized half-spread", real, F("-0.010"))
    exact("price impact", imp, F("0.015"))
    exact("realized + impact = effective", real + imp == eff, True)
    # the maker sold at p: paid the effective half-spread, lost the impact, net = realized half-spread
    exact("maker paid (cents)", eff * 100, F(1, 2))
    exact("maker lost to impact (cents)", imp * 100, F(3, 2))
    exact("maker net per share (cents)", (eff - imp) * 100, F(-1))


def gm_posterior_quotes(history: list[str], mu: F, v_low: int, v_high: int) -> tuple[F, F]:
    """Glosten-Milgrom bid and ask after `history` by enumerating every outcome path.

    Each trade is informed with probability mu (buys if V = V_H, sells if V = V_L) or uninformed (buys or sells
    with probability 1/2). The ask is E[V | history, next order is a buy]; the bid likewise for a sell.
    """

    def joint(v: int, orders: list[str]) -> F:
        prob = F(1, 2)
        for order in orders:
            # enumerate the trader type and the uninformed coin for this order
            total = F(0)
            for informed, coin in itertools.product((True, False), ("buy", "sell")):
                weight = mu * F(1, 2) if informed else (1 - mu) * F(1, 2)
                action = ("buy" if v == v_high else "sell") if informed else coin
                if action == order:
                    total += weight
            prob *= total
        return prob

    def cond_value(orders: list[str]) -> F:
        num = sum(v * joint(v, orders) for v in (v_low, v_high))
        den = sum(joint(v, orders) for v in (v_low, v_high))
        return num / den

    return cond_value(history + ["sell"]), cond_value(history + ["buy"])


def section_glosten_milgrom() -> None:
    print("Example 3: Glosten-Milgrom quotes and updating (cards ms-tox-gm-half-spread, ms-tox-gm-update-after-buy)")
    mu = F(1, 5)
    bid, ask = gm_posterior_quotes([], mu, 99, 101)
    exact("initial ask", ask, F("100.2"))
    exact("initial bid", bid, F("99.8"))
    exact("P(buy | V_H) = 0.2 + 0.8/2", mu + (1 - mu) / 2, F(3, 5))
    p_high = (F(1, 2) * F(3, 5)) / (F(1, 2) * F(3, 5) + F(1, 2) * F(2, 5))
    exact("P(V_H) after one buy", p_high, F(3, 5))
    bid2, ask2 = gm_posterior_quotes(["buy"], mu, 99, 101)
    exact("next ask = 99 + 2 x 0.36/0.52", ask2, 99 + 2 * F(36, 100) / F(52, 100))
    approx("next ask", float(ask2), 100.385, 3)
    approx("0.36/0.52", 36 / 52, 0.6923, 4)
    exact("next bid", bid2, F(100))


def section_pin(rng: np.random.Generator) -> None:
    print("Example 4: PIN (card ms-tox-pin-formula)")
    alpha, mu, eps = F(2, 5), 50, 100
    pin = alpha * mu / (alpha * mu + 2 * eps)
    exact("PIN", pin, F(20, 220))
    approx("PIN", float(pin), 0.091, 3)
    approx("PIN in percent", 100 * float(pin), 9, 0)
    days = 400_000
    event = rng.random(days) < 0.4
    informed = np.where(event, rng.poisson(50, days), 0)
    uninformed = rng.poisson(100, days) + rng.poisson(100, days)
    share = informed.sum() / (informed.sum() + uninformed.sum())
    total = informed + uninformed
    se = float(np.std(informed - share * total, ddof=1)) / (float(total.mean()) * math.sqrt(days))  # delta method
    simulated("informed share of all trades, simulated", float(share), 0.0909, 5 * se + 5e-5)
    exact("GM half-spread with mu = PIN and half-range 1 dollar (cents)", pin * 1 * 100, F(100, 11))
    approx("GM half-spread (cents)", float(pin * 100), 9, 0)


def phi_simpson(z: float, n: int = 20_000) -> float:
    """Normal CDF by composite Simpson integration of the density from -10 to z."""
    a = -10.0
    h = (z - a) / n
    x = a + h * np.arange(n + 1)
    f = np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
    return float(h / 3 * (f[0] + f[-1] + 4 * f[1:-1:2].sum() + 2 * f[2:-1:2].sum()))


def section_vpin() -> None:
    print("Example 5: VPIN on five buckets (card ms-tox-vpin-definition)")
    v = 10_000
    zs = [0.5, -0.2, 1.5, 0.1, 2.0]
    buys = []
    for z in zs:
        quad = phi_simpson(z)
        assert abs(quad - 0.5 * (1 + math.erf(z / math.sqrt(2)))) < 1e-12, z
        buys.append(v * quad)
    exact("buy volumes, rounded", [round(b) for b in buys], [6915, 4207, 9332, 5398, 9772])
    imb = [abs(2 * b - v) for b in buys]
    exact("absolute imbalances, rounded", [round(x) for x in imb], [3829, 1585, 8664, 797, 9545])
    exact("sum of imbalances, rounded", round(sum(imb)), 24420)
    approx("VPIN", sum(imb) / (5 * v), 0.488, 3)


def section_sample_size(rng: np.random.Generator) -> None:
    print("Example 6: how many fills to trust a markout (card ms-tox-markout-sample-size)")
    n1 = (1.96 * 3 / 0.1) ** 2
    approx("n for a 0.1-tick mean, sd 3", n1, 3457, 0)
    exact("rounded to the nearest hundred for the card", round(n1, -2), 3500)
    n2 = (1.96 * 3 * math.sqrt(2) / 0.3) ** 2
    approx("n per venue for a 0.3-tick difference", n2, 768, 0)
    # check by simulation: with n fills the mean's sd is Delta / 1.96, so a true Delta sits 1.96 standard errors out
    reps = 4000
    means = rng.normal(0.1, 3.0, (reps, 3457)).mean(axis=1)
    simulated("sd of the mean of 3,457 fills, simulated", float(means.std(ddof=1)), 0.1 / 1.96, 5 * (0.1 / 1.96) / math.sqrt(2 * reps))
    diff = rng.normal(0.0, 3.0, (reps, 768)).mean(axis=1) - rng.normal(0.0, 3.0, (reps, 768)).mean(axis=1)
    simulated("sd of a 768-vs-768 difference, simulated", float(diff.std(ddof=1)), 0.3 / 1.96, 5 * (0.3 / 1.96) / math.sqrt(2 * reps))


def section_segments() -> None:
    print("Example 7: pricing two segments (card ms-tox-segment-blended)")
    gross = F(1, 2) + F(1, 10)
    exact("gross edge", gross, F(6, 10))
    blended = F(7, 10) * F(1, 10) + F(3, 10) * F(16, 10)
    exact("blended adverse selection", blended, F(55, 100))
    exact("net edge", gross - blended, F(5, 100))
    exact("segment A", gross - F(1, 10), F(1, 2))
    exact("segment B", gross - F(16, 10), F(-1))
    exact("edge from A alone, per fill", (F(7, 10) * (gross - F(1, 10))) / F(7, 10), F(1, 2))
    breakeven = (gross - F(1, 10)) / (F(16, 10) - F(1, 10))
    exact("break-even share of B", breakeven, F(1, 3))
    approx("break-even share of B, percent", 100 * float(breakeven), 33.3, 1)


if __name__ == "__main__":
    generator = np.random.default_rng(SEED)
    section_markouts()
    section_spread_split()
    section_glosten_milgrom()
    section_pin(generator)
    section_vpin()
    section_sample_size(generator)
    section_segments()
