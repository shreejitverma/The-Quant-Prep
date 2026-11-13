"""Estimation and Fermi problems: every product, interval and anchor in the note.

Backs every number in `13-Interview-Playbook/04-Estimation-and-Fermi-Problems.md`.
Inputs are of two kinds and are labelled as such below:
- cited figures (Chicago population and households, golf-ball diameter, random close packing, populations,
  Earth's radius, life expectancy), each with its source in the note;
- stated assumptions (piano share, tuning rate, bus size, heart rate, ...), which only illustrate the method.
Independent routes used here:
- the quadrature rule for combining factor errors against seeded log-normal simulation of the product's quantiles;
- the golf-ball count against a lattice count of whole balls along each edge of the bus;
- interval endpoints by multiplying the factor bounds directly, compared with the quadrature interval;
- the log-normal median and mean against simulation.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 13-Interview-Playbook/code/interview_04_estimation.py`.
"""

from __future__ import annotations

import math

import numpy as np

SEED = 20261112
Z90 = 1.6448536269514722  # standard normal 95th percentile, so a central 90% interval is +/- Z90 sigma
Z80 = 1.2815515655446004  # 90th percentile, for central 80% intervals


def exact(label: str, value, expected) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def sig(label: str, value: float, expected: float, figures: int) -> None:
    """Assert `value` rounds to `expected` at `figures` significant figures."""
    rounded = float(f"{value:.{figures}g}")
    assert rounded == expected, f"{label}: computed {value!r} rounds to {rounded}, quoted {expected}"
    print(f"    {label} = {value:,.6g} (quoted {expected:,.{max(figures, 1)}g})")


def simulated(label: str, estimate: float, expected: float, tol: float) -> None:
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, quoted {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (quoted {expected}, tolerance {tol:.4f})")


def quantile_ratio_by_simulation(rng: np.random.Generator, k: int, f: float, coverage: float, n: int, correlated: bool = False) -> float:
    """Upper-quantile-to-median ratio of a product of k log-normal factors.

    Each factor's central `coverage` interval runs from a factor f below its median to a factor f above.
    """
    z = {0.9: Z90, 0.8: Z80}[coverage]
    sigma = math.log(f) / z
    if correlated:
        logs = k * sigma * rng.standard_normal(n)
    else:
        logs = (sigma * rng.standard_normal((n, k))).sum(axis=1)
    q_hi = np.quantile(logs, 0.5 + coverage / 2)
    return float(math.exp(q_hi - np.median(logs)))


def main() -> None:
    rng = np.random.default_rng(SEED)

    print("Anchors")
    exact("seconds in a 365.25-day year", 365.25 * 86_400, 31_557_600.0)
    sig("seconds in a year", 365.25 * 86_400, 3.16e7, 3)
    approx("pi x 10^7 relative gap, %", 100 * abs(math.pi * 1e7 / 31_557_600 - 1), 0.4, 1)
    exact("hours in a 365-day year", 365 * 24, 8760)
    approx("sqrt(252)", math.sqrt(252), 15.9, 1)
    sig("world population, UN WPP 2024 (cited, 2024)", 8.2e9, 8.2e9, 2)
    sig("US population 341,784,857 on 1 July 2025 (cited)", 341_784_857, 3.4e8, 2)
    sig("US population 341,784,857 in millions", 341_784_857 / 1e6, 341.8, 4)
    sig("US 2020 Census count 331,449,281 in millions (cited)", 331_449_281 / 1e6, 331.4, 4)
    approx("Earth's equatorial circumference from the WGS 84 radius 6378.137 km", 2 * math.pi * 6378.137, 40_075.0, 0)
    sig("rounded", 2 * math.pi * 6378.137, 40_000, 1)

    print("Geometric mean and combining errors")
    exact("sqrt(100 x 10,000)", math.isqrt(100 * 10_000), 1000)
    exact("arithmetic mean of 100 and 10,000", (100 + 10_000) / 2, 5050.0)
    for k, quoted in ((4, 4.0), (9, 8.0)):
        exact(f"2^sqrt({k})", 2 ** math.sqrt(k), quoted)
        n = 400_000
        ratio = quantile_ratio_by_simulation(rng, k, 2.0, 0.9, n)
        # quantile standard error in log space ~ sqrt(p(1-p))/(n f(z)) times the product's log sd; use 6 SE in ratio terms
        sd_log = math.sqrt(k) * math.log(2) / Z90
        se_log = math.sqrt(0.95 * 0.05) / (math.sqrt(n) * math.exp(-(Z90**2) / 2) / math.sqrt(2 * math.pi)) * sd_log
        simulated(f"90% upper/median ratio for {k} factors, each 90% good to x2", ratio, quoted, quoted * 6 * math.sqrt(2) * se_log)
    exact("fully correlated: 2^4", 2**4, 16)
    ratio = quantile_ratio_by_simulation(rng, 4, 2.0, 0.9, 200_000, correlated=True)
    simulated("90% upper/median ratio, 4 perfectly correlated factors", ratio, 16.0, 16 * 0.05)
    approx("sqrt(4) ln 2 = ln 4", math.sqrt(4) * math.log(2) - math.log(4), 0.0, 12)

    print("Example 1: piano tuners in Chicago")
    households = 1_146_547  # cited: ACS 2019-2023 via Census QuickFacts
    sig("Chicago 2020 Census population (cited)", 2_746_388, 2.7e6, 2)
    sig("households (cited)", households, 1.15e6, 3)
    pianos_homes = households / 20  # assumption: 1 in 20 households
    sig("pianos in homes", pianos_homes, 57_000, 2)
    pianos = pianos_homes * 1.10  # assumption: 10% more in institutions
    sig("pianos including institutions", pianos, 63_000, 2)
    per_tuner = 4 * 250  # assumptions: 4 tunings a day, 250 working days
    exact("tunings per tuner per year", per_tuner, 1000)
    tuners = pianos / per_tuner  # assumption: each piano tuned once a year
    sig("tuners", tuners, 63, 2)
    sig("tuners, said aloud", tuners, 60, 1)
    factor = 2 ** math.sqrt(2)  # two independent factors, each an 80% range of x2 either way
    approx("2^sqrt(2)", factor, 2.67, 2)
    sig("80% interval low", tuners / factor, 24, 2)
    sig("80% interval high", tuners * factor, 170, 2)
    ratio = quantile_ratio_by_simulation(rng, 2, 2.0, 0.8, 400_000)
    simulated("80% upper/median ratio for 2 factors by simulation", ratio, 2 ** math.sqrt(2), 0.03)

    print("Example 2: golf balls in a school bus")
    bus_cm3 = 800 * 250 * 200  # assumption: 8 x 2.5 x 2 m interior
    exact("bus interior, cm^3", bus_cm3, 40_000_000)
    d = 4.267  # cited: Rules of Golf minimum diameter 1.680 in = 42.67 mm
    approx("1.680 in in cm", 1.680 * 2.54, 4.267, 3)
    v_ball = 4 / 3 * math.pi * (d / 2) ** 3
    approx("ball volume, cm^3", v_ball, 40.7, 1)
    phi = 0.64  # cited: random close packing, Scott and Kilgour (1969) measured 0.637
    approx("0.637 to two decimals", 0.637, 0.64, 2)
    balls = bus_cm3 * phi / v_ball
    sig("balls before seats", balls, 630_000, 2)
    sig("balls after removing a quarter for seats", balls * 0.75, 470_000, 2)
    approx("cm^3 per ball including gaps", v_ball / phi, 64, 0)
    grid = [math.floor(side / d) for side in (800, 250, 200)]
    exact("whole balls along each edge", grid, [187, 58, 46])
    cubic = math.prod(grid)
    exact("simple cubic stacking count", cubic, 498_916)
    approx("simple cubic packing fraction pi/6", math.pi / 6, 0.524, 3)
    approx("random close packing over cubic", phi / (math.pi / 6), 1.22, 2)
    lattice_route = cubic * phi / (math.pi / 6)
    sig("lattice route, random packing", lattice_route, 610_000, 2)
    approx("gap between the two routes, %", 100 * (1 - lattice_route / balls), 3, 0)
    approx("densest sphere packing pi/(3 sqrt 2)", math.pi / (3 * math.sqrt(2)), 0.7405, 4)

    print("Example 3: heartbeats in a lifetime")
    minutes_per_year = 60 * 24 * 365
    exact("minutes in a 365-day year", minutes_per_year, 525_600)
    beats = 70 * minutes_per_year * 80  # assumptions: 70 bpm, 80 years
    sig("point estimate", beats, 2.9e9, 2)
    approx("OECD 2023 life expectancy at birth, cited", 81.1, 81, 0)
    s_rate = math.log(80 / 60) / 2  # assumption: 60 to 80 bpm is a 90% range
    s_life = math.log(90 / 70) / 2  # assumption: 70 to 90 years is a 90% range
    half = math.hypot(s_rate, s_life)
    approx("log half-width, heart rate: ln(4/3)/2", s_rate, 0.144, 3)
    approx("log half-width, lifespan: ln(9/7)/2", s_life, 0.126, 3)
    approx("combined log half-width", half, 0.19, 2)
    approx("combined factor", math.exp(half), 1.21, 2)
    sig("90% interval low", beats / math.exp(half), 2.4e9, 2)
    sig("90% interval high", beats * math.exp(half), 3.6e9, 2)
    sig("both extremes low (60 bpm, 70 years)", 60 * minutes_per_year * 70, 2.2e9, 2)
    sig("both extremes high (80 bpm, 90 years)", 80 * minutes_per_year * 90, 3.8e9, 2)
    # simulation: 90% ranges as +/- Z90 sigma log-normal factors around the point estimate
    rate = np.exp(np.log(70) + rng.standard_normal(400_000) * s_rate / Z90)
    life = np.exp(np.log(80) + rng.standard_normal(400_000) * s_life / Z90)
    prod = rate * life * minutes_per_year
    lo, hi = np.quantile(prod, [0.05, 0.95])
    simulated("simulated 5% quantile, billions", lo / 1e9, 2.43, 0.02)
    simulated("simulated 95% quantile, billions", hi / 1e9, 3.56, 0.02)
    approx("quote half-width 0.2 / 2.9, %", 100 * 0.2 / 2.9, 7, 0)
    assert 2.7e9 < beats < 3.1e9
    print("    2.7 < 2.94 < 3.1: both sides of the quote have positive edge against an uninformed counterparty")

    print("Example 4 and cards: volatility scaling")
    approx("32% / sqrt(252), %", 32 / math.sqrt(252), 2.0, 1)
    exact("32% / 16, %", 32 / 16, 2.0)
    exact("2% of 50", 0.02 * 50, 1.0)
    approx("16% / sqrt(252), %", 16 / math.sqrt(252), 1.0, 1)

    print("Card int-est-which-mean-to-centre: log-normal median and mean")
    mu, s = 0.0, 0.8
    x = np.exp(mu + s * rng.standard_normal(1_000_000))
    simulated("median", float(np.median(x)), math.exp(mu), 0.005)
    simulated("mean", float(x.mean()), math.exp(mu + s * s / 2), 0.01)
    print("All estimation checks passed.")


if __name__ == "__main__":
    main()
