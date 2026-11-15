"""Signals, features and alpha decay: every IC, turnover, horizon, neutralisation and capacity number in the note.

Backs every number in `09-Alpha-Research-and-Portfolio/03-Signals-Features-and-Alpha-Decay.md`.
Independent routes used here:
- book return and Sharpe by seeded simulation of a 2,000-name cross-section with a stated IC,
  against the closed forms IC sigma_cs / E|z| and mean(IC)/sd(IC) sqrt(252);
- turnover by seeded simulation of an AR(1) standardised signal and a signal-proportional book;
- horizon IC by simulating a signal against twenty lagged returns, and the geometric sums in exact
  `fractions.Fraction` arithmetic by enumeration rather than the closed-form series;
- the neutralisation regression by solving the normal equations in exact rational arithmetic;
- Pearson IC exactly and rank IC from the Spearman d^2 formula;
- capacity by bisection and golden-section search on the net-PnL curve, not the closed form.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 09-Alpha-Research-and-Portfolio/code/alpha_03_signals.py`.
"""

from __future__ import annotations

import math
from fractions import Fraction

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


def standardise(z: np.ndarray) -> np.ndarray:
    z = z - z.mean(axis=1, keepdims=True)
    return z / z.std(axis=1, keepdims=True)


def simulate_book(rng: np.random.Generator, ic_mean: float, ic_sd: float, names: int, days: int, disp: float):
    """Daily book returns w = z / sum|z| and realised daily ICs for a cross-section with true IC_t ~ N(ic_mean, ic_sd)."""
    book, ics = [], []
    for start in range(0, days, 252):
        d = min(252, days - start)
        ic = np.clip(ic_mean + ic_sd * rng.standard_normal((d, 1)), -0.99, 0.99)
        z = standardise(rng.standard_normal((d, names)))
        r = disp * (ic * z + np.sqrt(1 - ic * ic) * rng.standard_normal((d, names)))
        book.append((z * r).sum(axis=1) / np.abs(z).sum(axis=1))
        rc = r - r.mean(axis=1, keepdims=True)
        ics.append((z * rc).mean(axis=1) / rc.std(axis=1))
    return np.concatenate(book), np.concatenate(ics)


def ic_to_pnl(rng: np.random.Generator) -> None:
    print("IC to PnL (worked example 1, cards alpha-signal-ic-to-sharpe and alpha-signal-ic-pnl-dispersion)")
    e_abs = math.sqrt(2 / math.pi)
    approx("E|z| for Gaussian scores", e_abs, 0.80, 2)
    approx("E|z| (3 dp)", e_abs, 0.798, 3)
    zz = rng.standard_normal(4_000_000)
    simulated("E|z|, simulated", float(np.abs(zz).mean()), 0.798, 4 * 0.6028 / math.sqrt(zz.size) + 0.0005)
    daily = 0.03 * 0.02 / e_abs
    approx("expected daily return on gross (%)", daily * 100, 0.075, 3)
    approx("per year before costs (%)", daily * 252 * 100, 19, 0)
    approx("gross Sharpe at sd(IC) = 0.10", 0.03 / 0.10 * math.sqrt(252), 4.8, 1)
    approx("gross Sharpe at sd(IC) = 0.10 (card, 2 dp)", 0.03 / 0.10 * math.sqrt(252), 4.76, 2)
    approx("sqrt(2000 x 252)", math.sqrt(2000 * 252), math.sqrt(504_000), 9)
    naive = 0.03 * math.sqrt(504_000)
    approx("naive IC sqrt(N x 252)", naive, 21, 0)

    names, days = 2000, 30_240
    # true-IC volatility chosen so the realised daily IC has sd 0.10 (sampling noise adds about 1/N)
    book, ics = simulate_book(rng, 0.03, math.sqrt(0.10**2 - 1 / names), names, days, 0.02)
    sharpe = book.mean() / book.std(ddof=1) * math.sqrt(252)
    se = math.sqrt((1 + (sharpe / math.sqrt(252)) ** 2 / 2) / days) * math.sqrt(252)
    simulated("realised sd(IC)", float(ics.std(ddof=1)), 0.10, 0.003)
    simulated("book mean daily return (%)", float(book.mean() * 100), 0.075, 4 * book.std() / math.sqrt(days) * 100)
    simulated("book Sharpe with time-varying IC", float(sharpe), 4.76, 4 * se)
    ic_ir = ics.mean() / ics.std(ddof=1) * math.sqrt(252)
    simulated("book Sharpe matches mean(IC)/sd(IC) sqrt(252) on the same panel", float(sharpe), float(ic_ir), 0.1)

    book0, _ = simulate_book(rng, 0.03, 0.0, names, 5040, 0.02)
    s0 = book0.mean() / book0.std(ddof=1) * math.sqrt(252)
    se0 = math.sqrt((1 + (s0 / math.sqrt(252)) ** 2 / 2) / 5040) * math.sqrt(252)
    simulated("book Sharpe with constant IC and iid residuals", float(s0), naive, 4 * se0)
    approx("book Sharpe with constant IC, 'about 21'", float(s0), 21, 0)


def turnover(rng: np.random.Generator) -> None:
    print("Turnover from autocorrelation (worked example 2, cards alpha-signal-turnover-autocorr, alpha-signal-breakeven-cost)")
    to = math.sqrt(2 * (1 - 0.9))
    approx("sqrt(2(1 - 0.9))", to, 0.447, 3)
    approx("as a percentage of gross", to * 100, 45, 0)
    names, days, rho = 2000, 2000, 0.9
    z = rng.standard_normal(names)
    w_prev = None
    traded = []
    for _ in range(days):
        z = rho * z + math.sqrt(1 - rho * rho) * rng.standard_normal(names)
        s = (z - z.mean()) / z.std()
        w = s / np.abs(s).sum()
        if w_prev is not None:
            traded.append(np.abs(w - w_prev).sum())
        w_prev = w
    traded = np.array(traded)
    simulated("simulated daily turnover of the signal-proportional book", float(traded.mean()), 0.447, 0.003)
    alpha_bp = 0.03 * 0.02 / math.sqrt(2 / math.pi) * 1e4
    approx("alpha (bp per day)", alpha_bp, 7.5, 1)
    approx("alpha (bp per day, 2 dp)", alpha_bp, 7.52, 2)
    approx("daily cost at 5 bp (bp)", to * 5, 2.24, 2)
    approx("net alpha (bp)", alpha_bp - to * 5, 5.3, 1)
    approx("break-even cost (bp)", alpha_bp / to, 16.8, 1)
    approx("card: 7.5 / 0.45 (bp)", 7.5 / 0.45, 16.7, 1)
    approx("turnover at rho = 0.99", math.sqrt(2 * (1 - 0.99)), 0.141, 3)


def horizon(rng: np.random.Generator) -> None:
    print("IC decay and horizon (worked example 3, cards alpha-signal-half-life and alpha-signal-horizon-ic-peak)")
    lo, hi = 0.0, 50.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if 0.8**mid > 0.5 else (lo, mid)
    approx("half-life by bisection on 0.8^h = 1/2", lo, 3.1, 1)
    approx("half-life (2 dp, card)", math.log(2) / math.log(1.25), 3.11, 2)
    ic1, delta = Fraction(3, 100), Fraction(4, 5)
    sums = {}
    running = Fraction(0)
    for k in range(1, 61):
        running += ic1 * delta ** (k - 1)
        sums[k] = running
    exact("sum of IC(k), h = 2", sums[2], Fraction(54, 1000))
    approx("sum of IC(k), h = 5", float(sums[5]), 0.1008, 4)
    approx("sum of IC(k), h = 10", float(sums[10]), 0.1339, 4)
    cum = {h: float(sums[h]) / math.sqrt(h) for h in sums}
    for h, quoted in ((1, 0.030), (2, 0.038), (5, 0.045), (10, 0.042), (20, 0.033)):
        approx(f"IC over [1, {h}]", cum[h], quoted, 3)
    best = max(cum, key=cum.get)
    exact("horizon that maximises the cumulative IC", best, 6)
    approx("IC at h = 6", cum[6], 0.0452, 4)
    approx("IC at h = 5", cum[5], 0.0451, 4)
    approx("IC at h = 7", cum[7], 0.0448, 4)
    approx("closed form 0.15 (1 - 0.8^6) / sqrt(6)", 0.15 * (1 - 0.8**6) / math.sqrt(6), 0.0452, 4)
    approx("total harvestable IC (sum to 60 terms)", float(sums[60]), 0.15, 4)

    n = 2_000_000
    acc = {1: 0.0, 2: 0.0, 5: 0.0, 10: 0.0, 20: 0.0}
    s = rng.standard_normal(n)
    total = np.zeros(n)
    for k in range(1, 21):
        ick = 0.03 * 0.8 ** (k - 1)
        total += ick * s + math.sqrt(1 - ick * ick) * rng.standard_normal(n)
        if k in acc:
            acc[k] = float(np.corrcoef(s, total)[0, 1])
    for h, value in acc.items():
        simulated(f"IC over [1, {h}], simulated", value, round(cum[h], 4), 4 / math.sqrt(n))


def solve_exact(a: list[list[Fraction]], b: list[Fraction]) -> list[Fraction]:
    """Gaussian elimination in exact rational arithmetic."""
    m = [row[:] + [rhs] for row, rhs in zip(a, b, strict=True)]
    size = len(m)
    for col in range(size):
        piv = next(r for r in range(col, size) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        for r in range(size):
            if r != col and m[r][col] != 0:
                f = m[r][col] / m[col][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[col], strict=True)]
    return [m[i][size] / m[i][i] for i in range(size)]


def neutralise() -> None:
    print("Neutralising against sector and beta (worked example 4, card alpha-signal-neutralise-method)")
    s = [Fraction(x) for x in ("2", "1.5", "1", "0", "-0.5", "-1")]
    tech = [Fraction(1)] * 3 + [Fraction(0)] * 3
    beta = [Fraction(x) for x in ("1.4", "1.2", "1.0", "0.8", "0.7", "0.9")]
    cols = [tech, [1 - t for t in tech], beta]
    xtx = [[sum(a * b for a, b in zip(ci, cj, strict=True)) for cj in cols] for ci in cols]
    xts = [sum(a * b for a, b in zip(ci, s, strict=True)) for ci in cols]
    coef = solve_exact(xtx, xts)
    exact("coefficients (tech, non-tech, beta)", coef, [Fraction(-3, 10), Fraction(-17, 10), Fraction(3, 2)])
    resid = [si - sum(c * col[i] for c, col in zip(coef, cols, strict=True)) for i, si in enumerate(s)]
    exact("residual", resid, [Fraction(x) for x in ("0.2", "0", "-0.2", "0.5", "0.15", "-0.65")])
    exact("residual sum in tech", sum(resid[:3]), 0)
    exact("residual sum outside tech", sum(resid[3:]), 0)
    terms = [b * e for b, e in zip(beta, resid, strict=True)]
    exact("beta x residual terms", terms, [Fraction(x) for x in ("0.28", "0", "-0.2", "0.4", "0.105", "-0.585")])
    exact("sum of beta x residual", sum(terms), 0)
    mean_s, mean_t = sum(s) / 6, sum(tech) / 6
    cov = sum((a - mean_s) * (b - mean_t) for a, b in zip(s, tech, strict=True))
    var_s = sum((a - mean_s) ** 2 for a in s)
    var_t = sum((b - mean_t) ** 2 for b in tech)
    approx("correlation of the raw signal with the tech dummy", float(cov) / math.sqrt(float(var_s * var_t)), 0.93, 2)
    demeaned = [si - sum(s[:3]) / 3 for si in s[:3]] + [si - sum(s[3:]) / 3 for si in s[3:]]
    exact("sector-demeaned signal", demeaned, [Fraction(x) for x in ("0.5", "0", "-0.5", "0.5", "0", "-0.5")])
    tech_beta = sum(b * d for b, d in zip(beta[:3], demeaned[:3], strict=True))
    exact("beta exposure inside tech after sector demeaning", tech_beta, Fraction(1, 5))
    # cross-check the snippet in the note
    x = np.column_stack([np.array([1, 1, 1, 0, 0, 0.0]), np.array([0, 0, 0, 1, 1, 1.0]), np.array([1.4, 1.2, 1.0, 0.8, 0.7, 0.9])])
    lst, *_ = np.linalg.lstsq(x, np.array([2.0, 1.5, 1.0, 0.0, -0.5, -1.0]), rcond=None)
    assert np.allclose(lst, [float(c) for c in coef])


def outlier_ic() -> None:
    print("Pearson versus rank IC (worked example 5, card alpha-signal-rank-vs-pearson)")
    x = [Fraction(v) for v in ("0.1", "0.2", "0.3", "0.4", "0.5", "5.0")]
    y = [Fraction(v) for v in ("-0.01", "0", "0.01", "0.02", "0.03", "-0.05")]
    mx, my = sum(x) / 6, sum(y) / 6
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y, strict=True))
    vx = sum((a - mx) ** 2 for a in x)
    vy = sum((b - my) ** 2 for b in y)
    approx("Pearson IC", float(cov) / math.sqrt(float(vx * vy)), -0.83, 2)
    rx = [sorted(x).index(v) + 1 for v in x]
    ry = [sorted(y).index(v) + 1 for v in y]
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry, strict=True))
    spearman = 1 - Fraction(6 * d2, 6 * (36 - 1))
    exact("rank IC by the Spearman d^2 formula", spearman, Fraction(1, 7))
    approx("rank IC", float(spearman), 0.14, 2)


def capacity() -> None:
    print("Capacity under square-root impact (core concepts, card alpha-signal-capacity-turnover)")
    vol, sigma, y_const = 5e9, 0.02, 1.0  # hypothetical: total daily dollar volume traded, daily vol, impact constant

    def net(a_size: float, alpha: float, t: float) -> float:
        return alpha * a_size - t * a_size * y_const * sigma * math.sqrt(t * a_size / vol)

    def break_even(alpha: float, t: float) -> float:
        lo, hi = 1.0, 1e15
        for _ in range(400):
            mid = math.sqrt(lo * hi)
            lo, hi = (mid, hi) if net(mid, alpha, t) > 0 else (lo, mid)
        return lo

    def best_size(alpha: float, t: float) -> float:
        lo, hi = 0.0, break_even(alpha, t)
        g = (math.sqrt(5) - 1) / 2
        for _ in range(300):
            a1, a2 = hi - g * (hi - lo), lo + g * (hi - lo)
            lo, hi = (a1, hi) if net(a1, alpha, t) < net(a2, alpha, t) else (lo, a2)
        return 0.5 * (lo + hi)

    alpha, t = 5e-4, 0.2  # hypothetical 5 bp daily alpha on capital, 20% daily turnover
    a_be = break_even(alpha, t)
    closed = vol * alpha**2 / (y_const**2 * sigma**2 * t**3)
    assert abs(a_be / closed - 1) < 1e-9, (a_be, closed)
    print(f"    break-even AUM by bisection = {a_be:.6g}, closed form V alpha^2 / (Y^2 sigma^2 T^3) = {closed:.6g}")
    approx("break-even ratio when turnover doubles at fixed daily alpha", break_even(alpha, 2 * t) / a_be, 1 / 8, 9)
    approx("break-even ratio when turnover doubles at fixed alpha per unit traded", break_even(2 * alpha, 2 * t) / a_be, 1 / 2, 9)
    approx("profit-maximising size over break-even", best_size(alpha, t) / a_be, 4 / 9, 6)
    exact("(2/3)^2", Fraction(2, 3) ** 2, Fraction(4, 9))


def grinold_rule(rng: np.random.Generator) -> None:
    print("Grinold's forecasting rule (card alpha-signal-grinold-alpha)")
    n, ic, sig = 2_000_000, 0.05, 0.02
    z = rng.standard_normal(n)
    r = sig * (ic * z + math.sqrt(1 - ic * ic) * rng.standard_normal(n))
    slope = float((z * r).mean() / (z * z).mean())
    simulated("regression slope of residual return on score, over IC x sigma", slope / (ic * sig), 1.0, 4 / (ic * math.sqrt(n)))


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    ic_to_pnl(rng)
    turnover(rng)
    horizon(rng)
    neutralise()
    outlier_ic()
    capacity()
    grinold_rule(rng)
    print("All signal numbers check.")
