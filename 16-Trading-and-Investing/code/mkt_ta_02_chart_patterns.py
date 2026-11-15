"""Chart patterns and statistical edge: every number in the note, by an independent route.

Backs every number in
`16-Trading-and-Investing/07-Trading-Styles/Technical-Analysis/02-Chart-Patterns-and-Statistical-Edge.md`.
Independent routes used here:
- the head-and-shoulders and double-bottom arithmetic (height, target, risk, reward, ratio, trough mismatch,
  share of the measured move) in exact rational arithmetic (Fraction);
- the pattern labels themselves by running the Lo-Mamaysky-Wang style detector on a synthetic price path that
  passes through the worked-example extrema: Nadaraya-Watson smoothing with a Gaussian kernel, local extrema
  from sign changes of the smoothed slope, the actual price extreme taken within the kernel window, and the
  geometric inequalities applied to the detected values (so a wrong extremum or a wrong inequality fails);
- the detector is also run on a seeded driftless random walk to show it labels head-and-shoulders shapes in
  pure noise: the count is printed (it is seed-specific and quoted only as "can"), and the assert is only that
  the detector is not trivially silent or trivially always-on.
Aronson (2006) and Lo, Mamaysky and Wang (2000) study facts are cited constants printed for reference.
Every quoted number is printed as ``label = value`` and asserted at the precision the note quotes.
Run it with `python 16-Trading-and-Investing/code/mkt_ta_02_chart_patterns.py`.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

SEED = 2


def check(label: str, value: float, expected: str) -> None:
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    shown = f"{value:,.{decimals}f}"
    assert shown == expected, f"{label}: computed {shown}, quoted {expected}"
    print(f"{label} = {shown}")


def path_through(points: list[float], steps: int = 20) -> np.ndarray:
    """Piecewise-linear daily path through successive pivot prices."""
    legs = [np.linspace(a, b, steps, endpoint=False) for a, b in zip(points[:-1], points[1:], strict=True)]
    return np.concatenate([*legs, [points[-1]]])


def kernel_smooth(prices: np.ndarray, h: float) -> np.ndarray:
    t = np.arange(len(prices), dtype=float)
    w = np.exp(-0.5 * ((t[:, None] - t[None, :]) / h) ** 2)
    return (w @ prices) / w.sum(axis=1)


def extrema(prices: np.ndarray, h: float) -> list[tuple[str, float]]:
    """Kernel extrema, each replaced by the actual price extreme within +/- h days (Lo-Mamaysky-Wang)."""
    m = kernel_smooth(prices, h)
    slope = np.sign(np.diff(m))
    out: list[tuple[str, float]] = []
    win = max(1, int(round(h)))
    for i in range(1, len(slope)):
        if slope[i - 1] > 0 and slope[i] < 0:
            lo, hi = max(0, i - win), min(len(prices), i + win + 1)
            out.append(("peak", float(prices[lo:hi].max())))
        elif slope[i - 1] < 0 and slope[i] > 0:
            lo, hi = max(0, i - win), min(len(prices), i + win + 1)
            out.append(("trough", float(prices[lo:hi].min())))
    return out


def is_head_and_shoulders(e: list[tuple[str, float]], eps: float) -> bool:
    kinds = [k for k, _ in e]
    if kinds != ["peak", "trough", "peak", "trough", "peak"]:
        return False
    v = [x for _, x in e]
    return v[2] > v[0] and v[2] > v[4] and abs(v[0] - v[4]) <= eps * v[0] and abs(v[1] - v[3]) <= eps * v[1]


def head_and_shoulders_example() -> None:
    ls, lt, head, rt, rs = (Fraction(x) for x in (150, 135, 165, 135, 148))
    neckline = Fraction(135)
    height = head - neckline
    target = neckline - height
    check("H&S height ($)", float(height), "30.00")
    check("H&S target ($)", float(target), "105.00")
    entry = Fraction(134)
    risk = rs - entry
    reward = entry - target
    check("H&S risk to right-shoulder stop ($)", float(risk), "14.00")
    check("H&S reward to target ($)", float(reward), "29.00")
    check("H&S reward-to-risk", float(reward / risk), "2.07")
    shoulder_gap = abs(ls - rs) / ls
    check("H&S shoulder mismatch (%)", float(100 * shoulder_gap), "1.33")
    # Detector on a synthetic path through the five pivots (with flat lead-in and lead-out legs).
    path = path_through([140.0, 150.0, 135.0, 165.0, 135.0, 148.0, 140.0])
    found = extrema(path, h=2.0)
    print(f"H&S detected extrema = {found}")
    assert is_head_and_shoulders(found, eps=0.02), "detector should label the worked example a head-and-shoulders"
    assert not is_head_and_shoulders(found, eps=0.01), "a 1% tolerance must reject 1.33% shoulder mismatch"


def double_bottom_example() -> None:
    e1, e2, e3 = Fraction(100), Fraction(115), Fraction("100.50")
    mismatch = abs(e1 - e3) / e1
    check("double-bottom trough mismatch (%)", float(100 * mismatch), "0.5")
    assert mismatch <= Fraction(2, 100)
    breakout = Fraction(116)
    assert breakout > e2
    height = e2 - e1
    target = e2 + height
    check("double-bottom height ($)", float(height), "15.00")
    check("double-bottom target ($)", float(target), "130.00")
    peak = Fraction(128)
    captured = (peak - e2) / (target - e2)
    check("share of measured move captured (%)", float(100 * captured), "86.7")
    path = path_through([108.0, 100.0, 115.0, 100.5, 128.0, 120.0])
    found = extrema(path, h=2.0)
    print(f"double-bottom detected extrema = {found}")
    kinds = [k for k, _ in found]
    assert kinds[:3] == ["trough", "peak", "trough"], kinds
    t1, p1, t2 = (x for _, x in found[:3])
    assert abs(t1 - t2) <= 0.02 * t1 and p1 > max(t1, t2)


def noise_patterns(n_paths: int = 400, length: int = 63) -> None:
    rng = np.random.default_rng(SEED)
    hits = 0
    for _ in range(n_paths):
        path = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, length)))
        e = extrema(path, h=2.5)
        hits += any(is_head_and_shoulders(e[i : i + 5], eps=0.015) for i in range(len(e) - 4))
    print(f"random-walk windows labelled head-and-shoulders (seed {SEED}) = {hits} of {n_paths}")
    assert 0 < hits < n_paths


if __name__ == "__main__":
    head_and_shoulders_example()
    double_bottom_example()
    noise_patterns()
    print("cited: Aronson (2006) = 6,402 rules, S&P 500 Nov 1980 to Jul 2005, none significant at 0.05")
    print("cited: Lo-Mamaysky-Wang (2000) = 10 patterns, US stocks 1962-1996")
    print("all chart-pattern numbers check out")
