"""Random walks and gambler's ruin: every number in the note, recomputed by an independent route.

Backs `01-Probability/11-Random-Walks-and-Gamblers-Ruin.md`.
Independent routes:
- ruin probabilities and durations by solving the first-step equations exactly (rational tridiagonal solve),
  compared with the closed forms the note quotes;
- infinite-wealth answers by the same solve with a far absorbing barrier (the error is bounded and asserted);
- ballot, reflection and first-return identities by brute-force enumeration of every path or vote order;
- the Brownian running maximum by a seeded simulation that samples the exact maximum of each Brownian bridge piece;
- the 3D return probability by summing the exact return probabilities P(S_2n = 0) with an asymptotic tail.
Simulation tolerances are five standard errors; the seed is fixed.
Run it with `python 01-Probability/code/prob_11_random_walks.py`.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction
from statistics import NormalDist

import numpy as np

SEED = 20261019
RNG = np.random.default_rng(SEED)


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")
    return value


def exact(label: str, value: Fraction | int, expected: Fraction | int) -> None:
    assert value == expected, f"{label}: computed {value}, quoted {expected}"
    print(f"    {label} = {value}")


def tridiagonal_solve(lower: list, diag: list, upper: list, rhs: list) -> list:
    """Thomas algorithm; works on Fractions (exact) or floats."""
    n = len(diag)
    c, d = [upper[0] / diag[0]], [rhs[0] / diag[0]]
    for i in range(1, n):
        den = diag[i] - lower[i] * c[i - 1]
        c.append(upper[i] / den if i < n - 1 else 0)
        d.append((rhs[i] - lower[i] * d[i - 1]) / den)
    x = [d[-1]]
    for i in range(n - 2, -1, -1):
        x.append(d[i] - c[i] * x[-1])
    return x[::-1]


def ruin_solve(p: Fraction, n_top: int) -> tuple[list[Fraction], list[Fraction]]:
    """First-step equations for h_i = P_i(hit N before 0) and D_i = E_i[duration], i = 1..N-1, solved exactly."""
    q = 1 - p
    m = n_top - 1
    lower, diag, upper = [-q] * m, [Fraction(1)] * m, [-p] * m
    rhs_h = [Fraction(0)] * (m - 1) + [p]
    rhs_d = [Fraction(1)] * m
    h = tridiagonal_solve(lower, diag, upper, rhs_h)
    d = tridiagonal_solve(lower, diag, upper, rhs_d)
    return [Fraction(0), *h, Fraction(1)], [Fraction(0), *d, Fraction(0)]


def closed_h(p: Fraction, i: int, n_top: int) -> Fraction:
    if p == Fraction(1, 2):
        return Fraction(i, n_top)
    r = (1 - p) / p
    return (1 - r**i) / (1 - r**n_top)


def closed_d(p: Fraction, i: int, n_top: int) -> Fraction:
    q = 1 - p
    if p == q:
        return Fraction(i * (n_top - i))
    return Fraction(i) / (q - p) - Fraction(n_top) / (q - p) * closed_h(p, i, n_top)


def ruin() -> None:
    print("Core concepts: ruin probabilities and durations, exact solve versus closed forms")
    for p in (Fraction(1, 2), Fraction(2, 5), Fraction(49, 100), Fraction(3, 5)):
        h, d = ruin_solve(p, 12)
        assert all(h[i] == closed_h(p, i, 12) and d[i] == closed_d(p, i, 12) for i in range(13)), p
    print("    closed forms for h_i and D_i match the exact solve for p in {1/2, 2/5, 49/100, 3/5}, N = 12")
    print("Worked example: fair ruin, start 20, target 100")
    h, d = ruin_solve(Fraction(1, 2), 100)
    exact("P(reach 100)", h[20], Fraction(1, 5))
    exact("expected duration", d[20], Fraction(1600))
    exact("E[S_tau^2] = 100^2 * 1/5", 100**2 * h[20], Fraction(2000))
    exact("E[S_tau^2] - 20^2", 100**2 * h[20] - 400, d[20])
    print("Worked example: house edge, p = 0.49, start 50, target 100")
    h, _ = ruin_solve(Fraction(49, 100), 100)
    quoted("h_50 (card prob-rw-house-edge-50-to-100)", float(h[50]), 0.119, 3)
    quoted("h_50 to two decimals", float(h[50]), 0.12, 2)
    r50 = (Fraction(51, 49)) ** 50
    quoted("(51/49)^50", float(r50), 7.4, 1)
    assert h[50] == 1 / (1 + r50)
    print("Worked example: p = 0.4, start 5, target 10")
    h, d = ruin_solve(Fraction(2, 5), 10)
    exact("P(reach 10) (card prob-rw-biased-duration)", h[5], Fraction(32, 275))
    quoted("P(reach 10)", float(h[5]), 0.116, 3)
    exact("expected duration", d[5], Fraction(211, 11))
    quoted("expected duration", float(d[5]), 19.2, 1)
    _, d = ruin_solve(Fraction(1, 2), 10)
    exact("fair walk from 0 to +-5: a^2 (card prob-rw-hitting-time-plus-minus-a)", d[5], Fraction(25))


def infinite_wealth() -> None:
    print("Infinite-wealth limits via a far barrier (M = 400)")
    m = 400
    # Drunk man: steps away from the cliff (up) with 2/3; falls if he ever goes down 1 from 1.
    h, _ = ruin_solve(Fraction(2, 3), m)
    fall = 1 - h[1]
    assert abs(fall - Fraction(1, 2)) < Fraction(1, 2**390), "far barrier changes the answer by under 2^-390"
    quoted("drunk man falls (card prob-rw-drunk-man-cliff)", float(fall), 0.5, 15)
    f = Fraction(1, 2)
    assert f == Fraction(1, 3) + Fraction(2, 3) * f * f, "1/2 is a root of f = 1/3 + 2/3 f^2"
    h, _ = ruin_solve(Fraction(3, 5), m)
    quoted("p = 0.6 from 1: never ruined (card prob-rw-infinite-wealth-survival)", float(h[1]), 1 / 3, 15)
    # p < q: ever reaching +b from 0 equals (p/q)^b; reach N = b + j before 0 from j, j far.
    p, b = Fraction(2, 5), 3
    h, _ = ruin_solve(p, m)
    quoted("p = 0.4: P(ever up 3) = (2/3)^3", float(h[m - b]), float((p / (1 - p)) ** b), 12)
    # Drift hitting time b/(p - q) for p = 0.6, b = 3: duration from M - 3 with barriers 0 and M.
    _, d = ruin_solve(Fraction(3, 5), m)
    quoted("p = 0.6: E[time to +3] = 3/0.2 (card prob-rw-drift-hitting-time)", float(d[m - b]), 15.0, 9)
    n_paths = 20_000
    steps = np.where(RNG.random((n_paths, 400)) < 0.6, 1, -1).cumsum(axis=1)
    hit = (steps >= b).argmax(axis=1) + 1
    assert (steps >= b).any(axis=1).all()
    tau = hit.astype(float)
    se = tau.std(ddof=1) / math.sqrt(n_paths)
    assert abs(tau.mean() - 15.0) <= 5 * se
    print(f"    simulated E[time to +3] = {tau.mean():.3f} (se {se:.3f})")


def ballot() -> None:
    print("Worked example: ballot problem, a = 6, b = 4, by enumeration of every count order")
    orders = list(set(itertools.permutations("AAAAAABBBB")))
    exact("number of orders", len(orders), math.comb(10, 4))
    exact("orders starting with A", sum(o[0] == "A" for o in orders), 126)
    exact("orders starting with B", sum(o[0] == "B" for o in orders), 84)
    good = 0
    for o in orders:
        lead = 0
        ok = True
        for v in o:
            lead += 1 if v == "A" else -1
            if lead <= 0:
                ok = False
                break
        good += ok
    exact("A strictly ahead throughout", good, 42)
    exact("probability (card prob-rw-ballot-theorem)", Fraction(good, len(orders)), Fraction(6 - 4, 6 + 4))
    for a in range(1, 7):
        for b in range(a):
            seqs = set(itertools.permutations("A" * a + "B" * b))
            g = sum(all(o[: k + 1].count("A") > o[: k + 1].count("B") for k in range(a + b)) for o in seqs)
            assert Fraction(g, len(seqs)) == Fraction(a - b, a + b)
    print("    (a - b)/(a + b) confirmed by enumeration for all 0 <= b < a <= 6")


def reflection_and_returns() -> None:
    print("Worked example and cards: reflection, running max, first returns, by enumerating paths")
    paths = np.array(list(itertools.product((-1, 1), repeat=10)))
    s = paths.cumsum(axis=1)
    count_max = int((s.max(axis=1) >= 3).sum())
    exact("10-step paths with max >= 3", count_max, 352)
    exact("10-step paths with S_10 >= 4", int((s[:, -1] >= 4).sum()), 176)
    exact("P(max >= 3) (card prob-rw-max-ten-step-walk)", Fraction(count_max, 1024), Fraction(11, 32))
    for n in (8, 10, 12):
        pp = np.array(list(itertools.product((-1, 1), repeat=n))).cumsum(axis=1)
        for a in range(1, n + 1):
            lhs = int((pp.max(axis=1) >= a).sum())
            rhs = int((pp[:, -1] >= a).sum() + (pp[:, -1] > a).sum())
            assert lhs == rhs, (n, a)
    print("    P(max >= a) = P(S_n >= a) + P(S_n > a) for n = 8, 10, 12 and every a >= 1")
    for n in range(1, 7):
        pp = np.array(list(itertools.product((-1, 1), repeat=2 * n))).cumsum(axis=1)
        nonzero = int(np.all(pp != 0, axis=1).sum())
        at_zero = int((pp[:, -1] == 0).sum())
        assert nonzero == at_zero == math.comb(2 * n, n)
        positive_excursions = int((np.all(pp[:, :-1] > 0, axis=1) & (pp[:, -1] == 0)).sum())
        assert positive_excursions == math.comb(2 * n - 2, n - 1) // n, n
    print("    #(S_1..S_2n nonzero) = #(S_2n = 0) and positive excursions = Catalan C_(n-1), n = 1..6")
    exact("P(S_1..S_4 nonzero) (card prob-rw-no-return-to-zero)", Fraction(math.comb(4, 2), 16), Fraction(3, 8))
    n = 400
    ratio = math.comb(2 * n, n) / 4**n * math.sqrt(math.pi * n)
    assert abs(ratio - 1) < 1 / (4 * n), "C(2n, n)/4^n ~ 1/sqrt(pi n)"
    print(f"    C(2n, n)/4^n * sqrt(pi n) at n = 400: {ratio:.6f}")


def brownian_max() -> None:
    print("Card prob-rw-brownian-running-max: P(max_[0,1] W >= 1)")
    closed = 2 * (1 - NormalDist().cdf(1.0))
    quoted("2(1 - Phi(1))", closed, 0.317, 3)
    n_paths, n_steps = 200_000, 20
    dt = 1.0 / n_steps
    w = np.zeros(n_paths)
    hit = np.zeros(n_paths, dtype=bool)
    for _ in range(n_steps):
        w_next = w + math.sqrt(dt) * RNG.standard_normal(n_paths)
        # Exact maximum of the Brownian bridge between the grid points.
        u = RNG.random(n_paths)
        bridge_max = 0.5 * (w + w_next + np.sqrt((w_next - w) ** 2 - 2 * dt * np.log(u)))
        hit |= bridge_max >= 1.0
        w = w_next
    est = hit.mean()
    se = math.sqrt(est * (1 - est) / n_paths)
    assert abs(est - closed) <= 5 * se
    print(f"    simulated with exact bridge maxima: {est:.4f} (se {se:.4f})")


def polya_3d() -> None:
    print("Card prob-rw-polya-recurrence: 3D return probability")
    n_max = 300
    lg = [math.lgamma(k + 1) for k in range(2 * n_max + 1)]
    lgv = np.array(lg)
    u = 1.0  # n = 0 term
    for n in range(1, n_max + 1):
        i = np.arange(n + 1)[:, None]
        j = np.arange(n + 1)[None, :]
        k = n - i - j
        mask = k >= 0
        kk = np.where(mask, k, 0)
        logs = lg[2 * n] - 2 * (lgv[i] + lgv[j] + lgv[kk]) - 2 * n * math.log(6)
        u += float(np.exp(logs)[np.broadcast_to(mask, logs.shape)].sum())
    # Tail: P(S_2n = 0) ~ 2 (3/(4 pi n))^(3/2); sum from n_max + 1 by the integral with midpoint correction.
    c = 2 * (3 / (4 * math.pi)) ** 1.5
    u += c * 2 / math.sqrt(n_max + 0.5)
    ret = 1 - 1 / u
    quoted("return probability 1 - 1/u", ret, 0.34, 2)
    assert abs(ret - 0.340537) < 2e-4, "Watson's value 0.340537"
    print(f"    u = {u:.5f}, return probability {ret:.5f}")


def brownian_drift_ruin() -> None:
    print("Core concepts: Brownian ruin with drift solves (sigma^2/2) u'' + mu u' = 0, u(0) = 0, u(N) = 1")
    mu, sigma, n_top = 0.3, 1.5, 4.0  # illustrative inputs
    m = 4000
    h = n_top / m
    # Central finite-difference solve of the ODE, independent of the closed form.
    a, c = sigma**2 / (2 * h * h) - mu / (2 * h), sigma**2 / (2 * h * h) + mu / (2 * h)
    lower = [a] * (m - 1)
    diag = [-(sigma**2) / (h * h)] * (m - 1)
    upper = [c] * (m - 1)
    rhs = [0.0] * (m - 2) + [-c]
    u = tridiagonal_solve(lower, diag, upper, rhs)
    k = 2 * mu / sigma**2
    for x in (0.5, 1.0, 2.0, 3.0):
        closed = (1 - math.exp(-k * x)) / (1 - math.exp(-k * n_top))
        got = u[round(x / h) - 1]
        assert abs(got - closed) < 1e-6, (x, got, closed)
    print("    finite differences match (1 - e^(-2 mu x/sigma^2))/(1 - e^(-2 mu N/sigma^2)) to 1e-6")
    p = 0.51
    assert abs(math.log((1 - p) / p) - (-2 * 0.02)) < 1e-4, "ln r is about -2 mu for a +-1 walk with drift mu = 0.02"
    print("    +-1 walk with p = 0.51 (drift 0.02): ln r = -0.0400, about -2 mu")


if __name__ == "__main__":
    ruin()
    brownian_drift_ruin()
    infinite_wealth()
    ballot()
    reflection_and_returns()
    brownian_max()
    polya_3d()
    print("All random walk checks passed.")
