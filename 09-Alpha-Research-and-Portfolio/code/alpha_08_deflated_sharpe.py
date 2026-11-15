"""Overfitting, deflated Sharpe and multiple testing: every DSR, haircut, MinBTL, CPCV and PBO number in the note.

Backs every number in `09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md`.
Independent routes used here:
- the Euler-Mascheroni approximation to E[max of N normals] against quadrature of N Phi^(N-1) phi and simulation;
- the non-normal Sharpe variance (Mertens 2002, used inside the PSR of Bailey and Lopez de Prado 2012) by seeded
  simulation of a two-normal mixture with skewness -1 and kurtosis 6, against the normal-returns value;
- Harvey-Liu haircuts with p-values from `math.erfc` and t-stats recovered by bisection, not an inverse CDF;
- MinBTL by searching N directly, and the bound 2 ln N;
- CPCV splits and paths by enumerating every split and stitching the paths explicitly;
- PBO by a block-statistics implementation of CSCV, checked equal to the note's snippet on the same data,
  with the null mean checked against 1/2 within simulation error.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 09-Alpha-Research-and-Portfolio/code/alpha_08_deflated_sharpe.py`.
"""

from __future__ import annotations

import itertools
import math
from statistics import NormalDist

import numpy as np

SEED = 20261114
N01 = NormalDist()
EULER_GAMMA = 0.5772156649015329


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


def bracket(n: int) -> float:
    return (1 - EULER_GAMMA) * N01.inv_cdf(1 - 1 / n) + EULER_GAMMA * N01.inv_cdf(1 - 1 / (n * math.e))


def expected_max_quadrature(n: int) -> float:
    x = np.linspace(-12.0, 12.0, 24001)
    phi = np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
    cdf = np.array([N01.cdf(v) for v in x])
    y = x * n * cdf ** (n - 1) * phi
    h = x[1] - x[0]
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))


def psr(sr: float, sr_star: float, t: int, skew: float, kurt: float) -> float:
    """Probabilistic Sharpe ratio, per-period Sharpe, non-excess kurtosis (Bailey and Lopez de Prado 2012)."""
    return N01.cdf((sr - sr_star) * math.sqrt(t - 1) / math.sqrt(1 - skew * sr + (kurt - 1) / 4 * sr * sr))


def expected_max(rng: np.random.Generator) -> None:
    print("Expected maximum of N standard normals (core concepts, cards alpha-dsr-euler-mascheroni and alpha-minbtl)")
    for n, quoted in ((10, 1.57), (100, 2.53), (1000, 3.26)):
        approx(f"bracket N = {n}", bracket(n), quoted, 2)
    for n in (10, 100, 1000):
        print(f"    exact E[max] by quadrature, N = {n}: {expected_max_quadrature(n):.4f} (bracket {bracket(n):.4f})")
    approx("exact E[max of 100] by quadrature", expected_max_quadrature(100), 2.508, 3)
    approx("bracket N = 1000 (3 dp)", bracket(1000), 3.255, 3)
    approx("bracket over exact, N = 100 (% high)", (bracket(100) / expected_max_quadrature(100) - 1) * 100, 1, 0)
    approx("bracket N = 45", bracket(45), 2.236, 3)
    approx("E[max of 45] by quadrature", expected_max_quadrature(45), 2.21, 2)
    draws = rng.standard_normal((200_000, 45)).max(axis=1)
    simulated("E[max of 45] by simulation", float(draws.mean()), 2.21, 4 * draws.std() / math.sqrt(draws.size) + 0.005)


def mixture_with(skew: float, kurt: float, p: float = 0.1) -> tuple[float, float, float]:
    """Find d, s so that (1-p) N(0,1) + p N(-d, s^2) has the given skewness and kurtosis (Newton's method)."""

    def moments(d: float, s: float) -> tuple[float, float]:
        ez = [1, 0, 1, 0, 3]

        def raw(mu: float, sd: float, k: int) -> float:
            return sum(math.comb(k, j) * mu ** (k - j) * sd**j * ez[j] for j in range(k + 1))

        m = [(1 - p) * raw(0, 1, k) + p * raw(-d, s, k) for k in range(5)]
        mean = m[1]
        c2 = m[2] - mean**2
        c3 = m[3] - 3 * mean * m[2] + 2 * mean**3
        c4 = m[4] - 4 * mean * m[3] + 6 * mean**2 * m[2] - 3 * mean**4
        return c3 / c2**1.5, c4 / c2**2

    grid = [(i * 0.05, j * 0.05) for i in range(1, 120) for j in range(1, 100)]
    d, s = min(grid, key=lambda g: sum((a - b) ** 2 for a, b in zip(moments(*g), (skew, kurt), strict=True)))
    for _ in range(100):
        f0 = np.array(moments(d, s)) - (skew, kurt)
        h = 1e-7
        jac = np.column_stack(
            [(np.array(moments(d + h, s)) - (skew, kurt) - f0) / h, (np.array(moments(d, s + h)) - (skew, kurt) - f0) / h]
        )
        step = np.linalg.solve(jac, f0)
        d, s = d - step[0], s - step[1]
    assert np.allclose(moments(d, s), (skew, kurt), atol=1e-10)
    return p, d, s


def sample_mixture(rng: np.random.Generator, shape: tuple[int, int], p: float, d: float, s: float) -> np.ndarray:
    """Standardised draws (mean 0, variance 1) from the mixture."""
    mean = -p * d
    var = (1 - p) * 1 + p * (s * s + d * d) - mean**2
    jump = rng.random(shape) < p
    z = rng.standard_normal(shape)
    x = np.where(jump, -d + s * z, z)
    return (x - mean) / math.sqrt(var)


def psr_variance(rng: np.random.Generator) -> None:
    print("Sharpe variance under skewness -1 and kurtosis 6 (core concepts, card alpha-dsr-psr-formula)")
    p, d, s = mixture_with(-1.0, 6.0)
    t, sims = 1260, 20_000
    sr = 2 / math.sqrt(252)
    est = []
    for _ in range(0, sims, 1000):
        x = sr + sample_mixture(rng, (1000, t), p, d, s)
        est.append(x.mean(axis=1) / x.std(axis=1, ddof=1))
    est = np.concatenate(est)
    scaled = float(est.var(ddof=1) * (t - 1))
    mertens = 1 - (-1.0) * sr + (6 - 1) / 4 * sr * sr
    normal = 1 + sr * sr / 2
    approx("Mertens (T-1) Var(SR_hat)", mertens, 1.146, 3)
    approx("normal-returns (T-1) Var(SR_hat)", normal, 1.008, 3)
    approx("daily Sharpe", sr, 0.126, 3)
    tol = 4 * mertens * math.sqrt(2 / sims) * 1.2
    simulated("(T-1) Var(SR_hat), simulated", scaled, round(mertens, 4), tol)
    assert abs(scaled - normal) > 2 * tol, "the simulation must distinguish the non-normal variance from the normal one"
    print(f"    normal-returns value 1 + SR^2/2 = {normal:.4f} is rejected by the simulation")


def deflated() -> None:
    print("Deflating a Sharpe of 2 (worked example 1, card alpha-dsr-example-100-trials)")
    sr = 2 / math.sqrt(252)
    sv = math.sqrt(0.25 / 252)
    approx("daily Sharpe", sr, 0.1260, 4)
    approx("sqrt(V) daily", sv, 0.0315, 4)
    approx("bracket N = 100", bracket(100), 2.531, 3)
    sr0 = sv * bracket(100)
    approx("SR_0 daily", sr0, 0.0797, 4)
    approx("SR_0 annualised", sr0 * math.sqrt(252), 1.27, 2)
    den = math.sqrt(1 + 1 * sr + 5 / 4 * sr * sr)
    approx("PSR denominator", den, 1.0704, 4)
    z = (sr - sr0) * math.sqrt(1259) / den
    approx("z", z, 1.534, 3)
    approx("z (card)", z, 1.53, 2)
    approx("DSR", N01.cdf(z), 0.938, 3)
    approx("DSR (card)", N01.cdf(z), 0.94, 2)
    approx("DSR by the psr function", psr(sr, sr0, 1260, -1, 6), 0.9375, 4)
    approx("z for PSR(0)", sr * math.sqrt(1259) / den, 4.18, 2)
    approx("PSR(0)", psr(sr, 0, 1260, -1, 6), 1.0000, 4)
    sr0_1000 = sv * bracket(1000)
    approx("SR_0 annualised, N = 1000", sr0_1000 * math.sqrt(252), 1.63, 2)
    approx("DSR, N = 1000", psr(sr, sr0_1000, 1260, -1, 6), 0.78, 2)
    approx("DSR, Sharpe 1.5, N = 100", psr(1.5 / math.sqrt(252), sr0, 1260, -1, 6), 0.69, 2)


def p_two_sided(t: float) -> float:
    return math.erfc(t / math.sqrt(2))


def t_from_p(p: float) -> float:
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if p_two_sided(mid) > p else (lo, mid)
    return lo


def haircuts(rng: np.random.Generator) -> None:
    print("Harvey-Liu haircuts (worked example 2, cards alpha-haircut-example and alpha-haircut-nonlinear)")
    y = 10
    t = 1.0 * math.sqrt(y)
    approx("t for Sharpe 1 over 10 years", t, 3.16, 2)
    p = p_two_sided(t)
    approx("two-sided p", p, 0.00157, 5)
    for m, pq, tq, srq, cut in ((10, 0.0157, 2.42, 0.76, 24), (100, 0.157, 1.42, 0.45, 55)):
        pm = min(m * p, 1.0)
        tm = t_from_p(pm)
        approx(f"Bonferroni p, M = {m}", pm, pq, 4 if m == 10 else 3)
        approx(f"haircut t, M = {m}", tm, tq, 2)
        approx(f"haircut Sharpe, M = {m}", tm / math.sqrt(y), srq, 2)
        approx(f"haircut (%), M = {m}", (1 - tm / math.sqrt(y) / 1.0) * 100, cut, 0)
    t2 = 2.0 * math.sqrt(y)
    approx("t for Sharpe 2", t2, 6.32, 2)
    p2 = p_two_sided(t2)
    approx("p for Sharpe 2 (x 1e10)", p2 * 1e10, 2.5, 1)
    approx("Bonferroni p, M = 100 (x 1e8)", 100 * p2 * 1e8, 2.5, 1)
    tm2 = t_from_p(100 * p2)
    approx("haircut t, Sharpe 2", tm2, 5.57, 2)
    approx("haircut Sharpe, Sharpe 2", tm2 / math.sqrt(y), 1.76, 2)
    approx("haircut (%), Sharpe 2", (1 - tm2 / math.sqrt(y) / 2.0) * 100, 12, 0)
    t05 = 0.5 * math.sqrt(y)
    approx("t for Sharpe 0.5", t05, 1.58, 2)
    approx("p for Sharpe 0.5", p_two_sided(t05), 0.114, 3)
    exact("Bonferroni p for Sharpe 0.5, M = 100, capped", min(100 * p_two_sided(t05), 1.0), 1.0)

    # Holm's adjusted p-value never exceeds Bonferroni's, on random sets of p-values
    for _ in range(2000):
        ps = np.sort(rng.random(20) ** 3)
        m = ps.size
        holm = np.maximum.accumulate(np.minimum((m - np.arange(m)) * ps, 1.0))
        bonf = np.minimum(m * ps, 1.0)
        assert np.all(holm <= bonf + 1e-15)
    print("    Holm adjusted p <= Bonferroni adjusted p on 2,000 random sets of 20 p-values")


def min_btl() -> None:
    print("Minimum backtest length (worked example 3, TL;DR, card alpha-minbtl)")
    approx("MinBTL, N = 45 (years)", bracket(45) ** 2, 5.0, 1)
    approx("bound 2 ln 45", 2 * math.log(45), 7.6, 1)
    approx("MinBTL, N = 100", bracket(100) ** 2, 6.4, 1)
    approx("MinBTL, N = 1000", bracket(1000) ** 2, 10.6, 1)
    approx("expected best annualised Sharpe, N = 45, 5 years", bracket(45) / math.sqrt(5), 1.0, 2)
    first = next(n for n in range(2, 1000) if bracket(n) / math.sqrt(5) >= 0.9995)
    exact("smallest N whose expected best 5-year Sharpe rounds to 1.00 at three decimals", first, 45)
    assert bracket(46) / math.sqrt(5) > 1.0 > bracket(44) / math.sqrt(5)


def cpcv() -> None:
    print("CPCV and CSCV bookkeeping (worked example 4, card alpha-cpcv-paths)")
    for n_groups, k, splits_q, paths_q in ((6, 2, 15, 5), (10, 2, 45, 9)):
        splits = list(itertools.combinations(range(n_groups), k))
        exact(f"splits, N = {n_groups}, k = {k}", len(splits), splits_q)
        # stitch paths: the j-th time a group is tested, its predictions go to path j
        uses = dict.fromkeys(range(n_groups), 0)
        paths: dict[int, list[int]] = {}
        for split in splits:
            for g in split:
                paths.setdefault(uses[g], []).append(g)
                uses[g] += 1
        complete = [p for p in paths.values() if sorted(p) == list(range(n_groups))]
        exact(f"complete paths, N = {n_groups}, k = {k}", len(complete), paths_q)
        assert len(complete) == len(paths)
    exact("CSCV splits, S = 16", sum(1 for _ in itertools.combinations(range(16), 8)), 12_870)
    exact("CSCV splits, S = 10", sum(1 for _ in itertools.combinations(range(10), 5)), 252)


def pbo_blocks(m: np.ndarray, s: int = 10) -> float:
    """CSCV PBO from per-block sums, ranks by argsort (independent of the note's snippet)."""
    blocks = np.array_split(np.arange(m.shape[0]), s)
    s1 = np.array([m[b].sum(axis=0) for b in blocks])
    s2 = np.array([(m[b] ** 2).sum(axis=0) for b in blocks])
    cnt = np.array([len(b) for b in blocks], dtype=float)
    n = m.shape[1]
    below = 0
    total = 0
    for train in itertools.combinations(range(s), s // 2):
        tr = np.zeros(s, dtype=bool)
        tr[list(train)] = True
        stats = []
        for mask in (tr, ~tr):
            mean = s1[mask].sum(axis=0) / cnt[mask].sum()
            var = s2[mask].sum(axis=0) / cnt[mask].sum() - mean**2
            stats.append(mean / np.sqrt(var))
        winner = int(np.argmax(stats[0]))
        rank = int(np.argsort(np.argsort(stats[1]))[winner]) + 1  # 1 = worst out of sample
        omega = rank / (n + 1)
        below += omega <= 0.5
        total += 1
    return below / total


def pbo_note(m: np.ndarray, s: int = 10) -> float:
    """The note's snippet, verbatim."""
    blocks = np.array_split(np.arange(m.shape[0]), s)

    def sharpe(x: np.ndarray) -> np.ndarray:
        return x.mean(0) / x.std(0)

    logits = []
    for train in itertools.combinations(range(s), s // 2):
        test = [b for b in range(s) if b not in train]
        is_sr = sharpe(m[np.concatenate([blocks[b] for b in train])])
        oos_sr = sharpe(m[np.concatenate([blocks[b] for b in test])])
        n_star = np.argmax(is_sr)
        rank = (oos_sr <= oos_sr[n_star]).sum()
        w = rank / (m.shape[1] + 1)
        logits.append(np.log(w / (1 - w)))
    return float(np.mean(np.array(logits) <= 0))


def pbo_simulation(rng: np.random.Generator) -> None:
    print("PBO by simulation (worked example 5)")
    datasets, t, n = 100, 1000, 50
    null, signal = [], []
    for i in range(datasets):
        m = rng.standard_normal((t, n))
        null.append(pbo_blocks(m))
        if i < 3:
            assert abs(pbo_note(m) - null[-1]) < 1e-12, "block implementation must match the note's snippet"
        m[:, 0] += 0.15
        signal.append(pbo_blocks(m))
        if i < 3:
            assert abs(pbo_note(m) - signal[-1]) < 1e-12
    print("    the block-statistics PBO equals the note's snippet on the first three datasets, with and without signal")
    null = np.array(null)
    signal = np.array(signal)
    simulated("mean PBO under the null", float(null.mean()), 0.5, 4 * null.std(ddof=1) / math.sqrt(datasets))
    approx("mean PBO under the null (quoted)", float(null.mean()), 0.48, 2)
    approx("smallest null PBO", float(null.min()), 0.10, 2)
    approx("largest null PBO", float(null.max()), 0.96, 2)
    approx("mean PBO with one configuration at 0.15 sd per day", float(signal.mean()), 0.08, 2)
    approx("annualised Sharpe of that configuration", 0.15 * math.sqrt(252), 2.4, 1)


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    expected_max(rng)
    psr_variance(rng)
    deflated()
    haircuts(rng)
    min_btl()
    cpcv()
    pbo_simulation(rng)
    print("All deflated-Sharpe numbers check.")
