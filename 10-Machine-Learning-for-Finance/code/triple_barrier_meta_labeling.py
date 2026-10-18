"""Labeling for financial ML: CUSUM events, fixed-horizon versus triple-barrier labels, uniqueness and meta-labeling.

Backs 10-Machine-Learning-for-Finance/06-Labeling-Triple-Barrier-and-Meta-Labeling.md.

1. Symmetric CUSUM event filter on a short return series, by hand.
2. Triple-barrier label probabilities on a +-1 lattice walk by exact dynamic programming, checked against
   gambler's-ruin closed forms (no vertical barrier) and against Monte Carlo.
3. Fixed-horizon labels with a fixed threshold versus volatility-scaled thresholds in two volatility regimes,
   simulated and in closed form; triple-barrier labels with volatility-scaled barriers.
4. Concurrency and average uniqueness of triple-barrier labels.
5. Meta-labeling: a primary side model, a secondary logistic model fitted by Newton's method, the precision/recall
   trade-off across thresholds, F1, and bet sizing from the predicted probability (Lopez de Prado 2018, ch 10).

Run: uv run --no-project --with numpy python 10-Machine-Learning-for-Finance/code/triple_barrier_meta_labeling.py
"""

from __future__ import annotations

import math

import numpy as np


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> float:
    """Print a result and assert it matches the literal the note quotes, to tolerance and to printed rounding."""
    printed = f"{value:{fmt}}"
    print(f"{label} = {printed}")
    quoted = f"{expected:{fmt}}"
    assert abs(value - expected) <= tol + 1e-12, f"{label}: got {value}, expected {expected} +/- {tol}"
    assert printed.lstrip("-") == quoted.lstrip("-") or printed == quoted, f"{label}: prints {printed}, note quotes {quoted}"
    return value


def check_below(label: str, value: float, bound: float) -> None:
    print(f"{label} = {value:.2e}")
    print(f"{label} bound = {bound:g}")
    assert value < bound, f"{label}: {value} is not below {bound}"


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


# ---------------------------------------------------------------------------
# 1. CUSUM filter
# ---------------------------------------------------------------------------


def cusum_events(returns: np.ndarray, threshold: float) -> list[int]:
    """Symmetric CUSUM filter (Lopez de Prado 2018, ch 2): an event when either running sum crosses the threshold."""
    s_pos = s_neg = 0.0
    events = []
    for t, r in enumerate(returns):
        s_pos, s_neg = max(0.0, s_pos + r), min(0.0, s_neg + r)
        if s_pos > threshold:
            s_pos = 0.0
            events.append(t)
        elif s_neg < -threshold:
            s_neg = 0.0
            events.append(t)
    return events


def section_cusum() -> None:
    # Backs: Core concepts (events) and Worked example 1; card ml-label-cusum.
    print("\n== 1. CUSUM filter by hand ==")
    r = np.array([0.5, 0.4, 0.3, -0.2, -0.9, -0.4, 0.1])  # percent
    ev = cusum_events(r, 1.0)
    s_pos_path = np.cumsum(r[:3])  # S+ before the first event: 0.5, 0.9, 1.2
    check("CUSUM S+ on day 3 (crosses 1.0)", float(s_pos_path[-1]), 1.2, 1e-12, ".1f")
    s_neg = 0.0
    s_neg_path = []
    for x in r:
        s_neg = min(0.0, s_neg + x)
        s_neg_path.append(s_neg)
        if s_neg < -1.0:
            s_neg = 0.0
    check("CUSUM S- on day 5 (crosses -1.0)", s_neg_path[4], -1.1, 1e-12, ".1f")
    check("CUSUM S- on day 6", s_neg_path[5], -0.4, 1e-12, ".1f")
    check("CUSUM S- on day 7", s_neg_path[6], -0.3, 1e-12, ".1f")
    check("CUSUM events, count", len(ev), 2, 0, ".0f")
    check("CUSUM first event (day, 1-based)", ev[0] + 1, 3, 0, ".0f")
    check("CUSUM second event (day, 1-based)", ev[1] + 1, 5, 0, ".0f")
    rng = np.random.default_rng(1)
    rets = rng.standard_normal(100_000)
    for h, exp in [(1.0, 41.93), (2.0, 19.75), (4.0, 7.45)]:
        check(
            f"CUSUM events per 100 bars, threshold {h} sd, iid normal returns",
            100 * len(cusum_events(rets, h)) / rets.size,
            exp,
            5e-3,
            ".2f",
        )


# ---------------------------------------------------------------------------
# 2. Triple barrier on a lattice walk: exact DP
# ---------------------------------------------------------------------------


def lattice_triple_barrier(p_up: float, upper: int, lower: int, horizon: int) -> tuple[float, float, float, float]:
    """+-1 walk from 0 with P(up) = p_up. Barriers at +upper and -lower, vertical barrier after `horizon` steps.

    Returns P(upper first), P(lower first), P(vertical), E[min(T, horizon)].
    """
    width = upper + lower - 1  # interior states -lower+1 .. upper-1
    dist = np.zeros(width)
    dist[lower - 1] = 1.0  # position 0
    p_hi = p_lo = exp_t = 0.0
    for step in range(1, horizon + 1):
        new = np.zeros(width)
        new[1:] += p_up * dist[:-1]
        new[:-1] += (1 - p_up) * dist[1:]
        hit_hi = p_up * dist[-1]
        hit_lo = (1 - p_up) * dist[0]
        p_hi += hit_hi
        p_lo += hit_lo
        exp_t += step * (hit_hi + hit_lo)
        dist = new
    p_v = float(dist.sum())
    return p_hi, p_lo, p_v, exp_t + horizon * p_v


def gamblers_ruin_up(p_up: float, upper: int, lower: int) -> float:
    if p_up == 0.5:
        return lower / (upper + lower)
    r = (1 - p_up) / p_up
    return (1 - r**lower) / (1 - r ** (upper + lower))


def section_lattice() -> None:
    # Backs: Worked examples 2 and 5; cards ml-label-gamblers-ruin, ml-label-drifted-ruin, ml-label-hit-rate-trap, ml-label-vertical-share.
    print("\n== 2. Triple barrier on a lattice walk ==")
    for p_up, tag, exp_closed in [(0.5, "0.50", 0.5), (0.55, "0.55", 0.6461)]:
        hi, lo, v, et = lattice_triple_barrier(p_up, 3, 3, 4000)
        check(f"gambler's ruin P(upper first), p {tag}, barriers +-3", gamblers_ruin_up(p_up, 3, 3), exp_closed, 5e-5)
        check_below(f"DP with horizon 4000 vs gambler's ruin, p {tag}", abs(hi - gamblers_ruin_up(p_up, 3, 3)), 1e-12)
    _, _, _, et = lattice_triple_barrier(0.5, 3, 3, 4000)
    check("expected hitting time, symmetric walk, barriers +-3 (theory a*b = 9)", et, 9.00, 1e-9, ".2f")
    check("gambler's ruin P(upper first), p 0.5, barriers +2 and -4", gamblers_ruin_up(0.5, 2, 4), 0.6667, 5e-5)
    hi24, lo24, _, _ = lattice_triple_barrier(0.5, 2, 4, 4000)
    check("P(lower first), barriers +2 and -4, from DP", lo24, 0.3333, 5e-5)
    check("expected payoff +2 / -4 barriers, no edge (from DP)", 2 * hi24 - 4 * lo24, 0.0, 1e-9, ".4f")
    for p_up, tag, exp in [(0.5, "0.50", (0.3418, 0.3418, 0.3164, 6.785)), (0.55, "0.55", (0.4497, 0.2463, 0.3039, 6.710))]:
        hi, lo, v, et = lattice_triple_barrier(p_up, 3, 3, 10)
        check(f"triple barrier +-3, horizon 10, p {tag}: P(upper)", hi, exp[0], 5e-5)
        check(f"triple barrier +-3, horizon 10, p {tag}: P(lower)", lo, exp[1], 5e-5)
        check(f"triple barrier +-3, horizon 10, p {tag}: P(vertical)", v, exp[2], 5e-5)
        check(f"triple barrier +-3, horizon 10, p {tag}: E[holding period]", et, exp[3], 5e-4, ".3f")
    # Monte Carlo check of the drifted case.
    rng = np.random.default_rng(2)
    steps = np.where(rng.random((200_000, 10)) < 0.55, 1, -1)
    paths = np.cumsum(steps, axis=1)
    first_hi = np.where((paths >= 3).any(axis=1), (paths >= 3).argmax(axis=1), 99)
    first_lo = np.where((paths <= -3).any(axis=1), (paths <= -3).argmax(axis=1), 99)
    check("Monte Carlo P(upper), p 0.55, 200k paths", float((first_hi < first_lo).mean()), 0.449, 5e-4, ".3f")


# ---------------------------------------------------------------------------
# 3. Fixed-horizon versus volatility-scaled labels
# ---------------------------------------------------------------------------


def section_fixed_vs_scaled() -> None:
    # Backs: TL;DR, Core concepts and Worked example 3; cards ml-label-fixed-horizon-flaws, ml-label-dynamic-threshold, ml-label-uniqueness.
    print("\n== 3. Fixed-horizon labels across volatility regimes ==")
    h, tau = 5, 0.01
    for vol, tag, exp in [(0.005, "low vol 0.5%", 0.371), (0.02, "high vol 2%", 0.823)]:
        sd_h = vol * math.sqrt(h)
        check(f"closed form P(|5-day return| > 1%), {tag}", 2 * (1 - norm_cdf(tau / sd_h)), exp, 5e-4, ".3f")
    check("closed form P(|5-day return| > 1 sd)", 2 * (1 - norm_cdf(1.0)), 0.317, 5e-4, ".3f")

    rng = np.random.default_rng(3)
    n = 200_000
    regime = (np.arange(n) // 2_000) % 2  # alternate 2,000-day blocks of low and high volatility
    vol = np.where(regime == 0, 0.005, 0.02)
    r = vol * rng.standard_normal(n)
    fwd = np.convolve(r, np.ones(h), "valid")[1:]  # r_{t+1} + ... + r_{t+h}
    t_idx = np.arange(fwd.size)
    # EWMA volatility known at t (uses returns up to and including t), span 100 as a typical choice.
    alpha = 2 / (100 + 1)
    ew = np.empty(n)
    var = vol[0] ** 2
    for t in range(n):
        var = (1 - alpha) * var + alpha * r[t] ** 2
        ew[t] = math.sqrt(var)
    for reg, tag, exp_fixed, exp_scaled, exp_ctrl in [(0, "low vol", 0.372, 0.297, 0.318), (1, "high vol", 0.819, 0.325, 0.314)]:
        mask = regime[t_idx] == reg
        check(
            f"simulated fraction labelled +-1, fixed 1% threshold, {tag}", float((np.abs(fwd[mask]) > tau).mean()), exp_fixed, 5e-4, ".3f"
        )
        scaled = np.abs(fwd[mask]) > ew[t_idx][mask] * math.sqrt(h)
        check(f"simulated fraction labelled +-1, 1 sd EWMA-scaled threshold, {tag}", float(scaled.mean()), exp_scaled, 5e-4, ".3f")
        # Control: the same rule with the true (known) volatility instead of the lagging EWMA estimate.
        oracle = np.abs(fwd[mask]) > vol[t_idx][mask] * math.sqrt(h)
        check(f"simulated fraction labelled +-1, 1 sd true-vol threshold (control), {tag}", float(oracle.mean()), exp_ctrl, 5e-4, ".3f")

    # Triple barrier with EWMA-scaled horizontal barriers at +-1 sd*sqrt(h) and a 5-day vertical barrier.
    m = n - h - 1
    path = np.cumsum(np.lib.stride_tricks.sliding_window_view(r[1:], h)[:m], axis=1)
    width = (ew[:m] * math.sqrt(h))[:, None]
    up = path >= width
    dn = path <= -width
    first_up = np.where(up.any(axis=1), up.argmax(axis=1), h)
    first_dn = np.where(dn.any(axis=1), dn.argmax(axis=1), h)
    label = np.where(first_up < first_dn, 1, np.where(first_dn < first_up, -1, 0))
    hold = np.minimum(first_up, first_dn) + 1
    # A fixed-horizon label at the same width implies a barrier touch: |final| > width means the path reached the barrier.
    fixed_nonzero = np.abs(path[:, -1]) > width[:, 0]
    check(
        "fixed-horizon non-zero labels that are also triple-barrier touches (%)",
        100 * float((up | dn)[fixed_nonzero].any(axis=1).mean()),
        100.0,
        1e-12,
        ".1f",
    )
    for reg, tag, exp in [(0, "low vol", 0.411), (1, "high vol", 0.448)]:
        mask = regime[:m] == reg
        check(f"triple barrier fraction touching a horizontal barrier, {tag}", float((label[mask] != 0).mean()), exp, 5e-4, ".3f")
    check("triple barrier mean holding period (days), all events", float(hold.mean()), 4.84, 5e-3, ".2f")
    uniqueness_report(hold)


# ---------------------------------------------------------------------------
# 4. Uniqueness
# ---------------------------------------------------------------------------


def uniqueness_report(hold: np.ndarray) -> None:
    print("\n== 4. Concurrency and uniqueness of triple-barrier labels ==")
    n = hold.size
    start = np.arange(n) + 1  # label i spans bars start_i .. start_i + hold_i - 1
    end = start + hold - 1
    conc = np.zeros(n + 10)
    np.add.at(conc, start, 1)
    np.add.at(conc, end + 1, -1)
    conc = np.cumsum(conc)
    inv = np.concatenate([[0.0], np.cumsum(np.where(conc > 0, 1.0 / np.maximum(conc, 1), 0.0))])
    uniq = (inv[end + 1] - inv[start]) / hold
    check("average uniqueness, daily triple-barrier events (5-day vertical barrier)", float(uniq.mean()), 0.212, 5e-4, ".3f")
    check("average concurrency", float(conc[1 : n + 1].mean()), 4.84, 5e-3, ".2f")
    # Fixed 5-day labels for comparison: every label lasts 5 bars and concurrency is 5 in steady state.
    check("uniqueness of fixed 5-day labels in steady state, 1/h", 1 / 5, 0.20, 1e-12, ".2f")


# ---------------------------------------------------------------------------
# 5. Meta-labeling
# ---------------------------------------------------------------------------


def logistic_newton(x: np.ndarray, y: np.ndarray, iters: int = 25) -> np.ndarray:
    beta = np.zeros(x.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-x @ beta))
        grad = x.T @ (y - p)
        hess = (x * (p * (1 - p))[:, None]).T @ x
        beta += np.linalg.solve(hess, grad)
    return beta


def bet_size(p: np.ndarray | float) -> np.ndarray:
    """Lopez de Prado (2018) ch 10, two classes: z = (p - 1/2)/sqrt(p(1-p)), size = 2 Phi(z) - 1."""
    p = np.asarray(p, dtype=float)
    z = (p - 0.5) / np.sqrt(p * (1 - p))
    return np.vectorize(lambda v: 2 * norm_cdf(v) - 1)(z)


def section_meta() -> None:
    # Backs: Worked example 4 and bet sizing; cards ml-label-precision-recall, ml-label-f1-objective,
    # ml-label-f1-calc, ml-label-bet-size, ml-label-size-vs-filter.
    print("\n== 5. Meta-labeling ==")
    check("F1 for precision 0.6, recall 0.5", 2 * 0.6 * 0.5 / (0.6 + 0.5), 0.5455, 5e-5)
    check("bet size z statistic at p 0.6", (0.6 - 0.5) / math.sqrt(0.6 * 0.4), 0.2041, 5e-5)
    for p, exp in [(0.55, 0.0801), (0.6, 0.1617), (0.7, 0.3375)]:
        check(f"bet size at p {p}", float(bet_size(p)), exp, 5e-5)

    rng = np.random.default_rng(4)
    n = 40_000
    z = rng.standard_normal(n)  # informative conditioning feature (e.g. a volatility or trend regime)
    w = rng.standard_normal(n)  # irrelevant feature
    p_correct = 1 / (1 + np.exp(-(0.1 + 1.0 * z)))
    correct = rng.random(n) < p_correct  # primary side right means the profit-taking barrier is hit first
    pnl = np.where(correct, 1.0, -1.0)  # symmetric barriers: +1 or -1 per unit bet
    tr, te = slice(0, n // 2), slice(n // 2, n)
    x = np.column_stack([np.ones(n), z, w])
    beta = logistic_newton(x[tr], correct[tr].astype(float))
    check("meta model coefficient on z (true 1.0)", float(beta[1]), 1.021, 5e-4, ".3f")
    check("meta model coefficient on the noise feature (true 0)", float(beta[2]), 0.037, 5e-4, ".3f")
    prob = 1 / (1 + np.exp(-x[te] @ beta))
    y = correct[te]
    pnl_te = pnl[te]
    check("primary model precision (take every bet), test", float(y.mean()), 0.521, 5e-4, ".3f")
    check("primary model mean PnL per bet, test", float(pnl_te.mean()), 0.043, 5e-4, ".3f")
    check("primary model per-event Sharpe (mean/sd), test", float(pnl_te.mean() / pnl_te.std()), 0.043, 5e-4, ".3f")
    expected = {
        0.5: (0.547, 0.679, 0.712, 0.695, 0.358, 0.275),
        0.6: (0.387, 0.735, 0.545, 0.626, 0.470, 0.306),
        0.7: (0.237, 0.787, 0.357, 0.491, 0.573, 0.290),
    }
    for thr, (e_take, e_prec, e_rec, e_f1, e_pnl, e_sr) in expected.items():
        tag = f"{thr}"
        take = prob > thr
        tp = int((take & y).sum())
        precision = tp / int(take.sum())
        recall = tp / int(y.sum())
        f1 = 2 * precision * recall / (precision + recall)
        strat = np.where(take, pnl_te, 0.0)
        check(f"meta threshold {tag}: fraction of bets taken", float(take.mean()), e_take, 5e-4, ".3f")
        check(f"meta threshold {tag}: precision", precision, e_prec, 5e-4, ".3f")
        check(f"meta threshold {tag}: recall", recall, e_rec, 5e-4, ".3f")
        check(f"meta threshold {tag}: F1", f1, e_f1, 5e-4, ".3f")
        check(f"meta threshold {tag}: mean PnL per bet taken", float(pnl_te[take].mean()), e_pnl, 5e-4, ".3f")
        check(f"meta threshold {tag}: per-event Sharpe", float(strat.mean() / strat.std()), e_sr, 5e-4, ".3f")
    sr_primary = float(pnl_te.mean() / pnl_te.std())
    take5 = np.where(prob > 0.5, pnl_te, 0.0)
    check("per-event Sharpe ratio, meta threshold 0.5 over primary", float(take5.mean() / take5.std()) / sr_primary, 6.4, 0.05, ".1f")
    check("primary model F1 (recall 1)", 2 * float(y.mean()) / (float(y.mean()) + 1), 0.685, 5e-4, ".3f")
    size = np.where(prob > 0.5, bet_size(prob), 0.0)
    sized = size * pnl_te
    check("sized by 2 Phi(z) - 1: mean size when betting", float(size[prob > 0.5].mean()), 0.332, 5e-4, ".3f")
    check("sized by 2 Phi(z) - 1: per-event Sharpe", float(sized.mean() / sized.std()), 0.329, 5e-4, ".3f")
    # Oracle: bet only when the true probability exceeds 0.5 (the best any meta model could do with z).
    oracle = np.where(p_correct[te] > 0.5, pnl_te, 0.0)
    check("oracle filter (true p > 0.5): per-event Sharpe", float(oracle.mean() / oracle.std()), 0.278, 5e-4, ".3f")


if __name__ == "__main__":
    section_cusum()
    section_lattice()
    section_fixed_vs_scaled()
    section_meta()
    print("\nall checks passed")
