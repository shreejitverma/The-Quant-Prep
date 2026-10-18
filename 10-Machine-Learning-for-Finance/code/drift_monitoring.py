"""Monitoring a production model: point-in-time joins, PSI, the KS test, and CUSUM alarms on decaying IC.

Backs 10-Machine-Learning-for-Finance/10-ML-Production-and-Monitoring.md.

1. As-of join by hand: the feature value a model may use at each query time, with and without a publication delay.
2. PSI by hand on four bins; its sampling distribution under no drift (chi-square approximation against
   simulation) for several sample sizes; population PSI of a mean shift.
3. The two-sample Kolmogorov-Smirnov test: statistic by hand, asymptotic critical value, and detection power for a
   0.1 sd mean shift compared with the fixed PSI > 0.1 rule and with a PSI threshold calibrated to the sample size
   (the control that separates "PSI is weak" from "the fixed threshold is wrong").
4. A unit bug (serving a feature in percent instead of decimals) caught by PSI on the prediction distribution.
5. Decaying signal: daily IC drops from 0.05 to 0 on day 500. Page's CUSUM against rolling-mean rules: share of paths
   with a false alarm in the 500 healthy days and detection delay after the change. The simulated CUSUM false-alarm
   shares are checked against an independent Markov-chain computation (Brook and Evans 1972), which also gives the
   average run lengths ARL0 and ARL1.

Run: uv run --no-project --with numpy python 10-Machine-Learning-for-Finance/code/drift_monitoring.py
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


def norm_cdf(x: np.ndarray | float) -> np.ndarray:
    return 0.5 * (1.0 + np.vectorize(math.erf)(np.asarray(x, dtype=float) / math.sqrt(2.0)))


# ---------------------------------------------------------------------------
# 1. As-of join
# ---------------------------------------------------------------------------


def as_of(update_times: np.ndarray, values: np.ndarray, query_times: np.ndarray, delay: float = 0.0) -> np.ndarray:
    """Latest value whose availability time (update + delay) is at or before each query time; NaN if none."""
    idx = np.searchsorted(update_times + delay, query_times, side="right") - 1
    out = np.full(query_times.shape, np.nan)
    ok = idx >= 0
    out[ok] = values[idx[ok]]
    return out


def section_as_of() -> None:
    # Backs: Worked example 1; card ml-prod-asof.
    print("\n== 1. As-of join ==")
    upd = np.array([540.0, 570.0, 615.0])  # minutes after midnight: 09:00, 09:30, 10:15
    val = np.array([1.0, 1.5, 0.8])
    q = np.array([550.0, 570.0, 600.0, 620.0])  # 09:10, 09:30, 10:00, 10:20
    no_delay = as_of(upd, val, q)
    delayed = as_of(upd, val, q, delay=5.0)
    for t, v0, v5, e0, e5 in zip(q, no_delay, delayed, [1.0, 1.5, 1.5, 0.8], [1.0, 1.0, 1.5, 0.8], strict=True):
        hhmm = f"{int(t // 60):02d}:{int(t % 60):02d}"
        check(f"as-of value at {hhmm}, no delay", v0, e0, 1e-12, ".1f")
        check(f"as-of value at {hhmm}, 5-minute publication delay", v5, e5, 1e-12, ".1f")


# ---------------------------------------------------------------------------
# 2. PSI
# ---------------------------------------------------------------------------


def psi_from_props(expected: np.ndarray, actual: np.ndarray, floor: float = 1e-4) -> float:
    e = np.maximum(expected, floor)
    a = np.maximum(actual, floor)
    return float(((a - e) * np.log(a / e)).sum())


def psi_samples(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    edges = np.quantile(reference, np.linspace(0, 1, bins + 1)[1:-1])
    e = np.bincount(np.searchsorted(edges, reference, side="right"), minlength=bins) / reference.size
    a = np.bincount(np.searchsorted(edges, current, side="right"), minlength=bins) / current.size
    return psi_from_props(e, a)


def chi2_cdf(x: float, k: int) -> float:
    """Regularised lower incomplete gamma P(k/2, x/2) by its power series."""
    s, z = k / 2.0, x / 2.0
    term = 1.0 / s
    total = term
    for n in range(1, 500):
        term *= z / (s + n)
        total += term
        if term < 1e-17 * total:
            break
    return total * math.exp(-z + s * math.log(z) - math.lgamma(s))


def chi2_quantile(p: float, k: int) -> float:
    lo, hi = 0.0, 200.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if chi2_cdf(mid, k) < p else (lo, mid)
    return 0.5 * (lo + hi)


def section_psi() -> None:
    # Backs: Worked examples 2, 3 and 4; cards ml-prod-psi-calc, ml-prod-psi-null, ml-prod-psi-threshold.
    print("\n== 2. PSI ==")
    e = np.array([0.25, 0.25, 0.25, 0.25])
    a = np.array([0.20, 0.25, 0.25, 0.30])
    check("PSI by hand, 4 bins", psi_from_props(e, a), 0.0203, 5e-5)
    check("chi-square approximation sum (a - e)^2 / e", float(((a - e) ** 2 / e).sum()), 0.0200, 5e-5)

    q95 = chi2_quantile(0.95, 9)
    check("chi-square 95% quantile, 9 degrees of freedom", q95, 16.919, 5e-4, ".3f")
    rng = np.random.default_rng(12)
    for n, e_mean, e_q95, e_sim_mean, e_sim_q95, e_flag in [
        (200, 0.090, 0.169, 0.091, 0.173, 0.357),
        (1000, 0.018, 0.034, 0.018, 0.033, 0.000),
        (100_000, 0.00018, 0.00034, 0.00018, 0.00034, 0.000),
    ]:
        scale = 1 / n + 1 / n
        check(
            f"null PSI mean, theory 9(1/n + 1/m), n = m = {n}",
            9 * scale,
            e_mean,
            5e-6 if n > 10_000 else 5e-4,
            ".5f" if n > 10_000 else ".3f",
        )
        check(
            f"null PSI 95% quantile, theory, n = m = {n}", q95 * scale, e_q95, 5e-6 if n > 10_000 else 5e-4, ".5f" if n > 10_000 else ".3f"
        )
        reps = 400 if n > 10_000 else 2000
        sims = np.array([psi_samples(rng.standard_normal(n), rng.standard_normal(n)) for _ in range(reps)])
        fmt = ".5f" if n > 10_000 else ".3f"
        tol = 5e-6 if n > 10_000 else 5e-4
        check(f"null PSI mean, simulated, n = m = {n}", float(sims.mean()), e_sim_mean, tol, fmt)
        check(f"null PSI 95% quantile, simulated, n = m = {n}", float(np.quantile(sims, 0.95)), e_sim_q95, tol, fmt)
        check(f"null P(PSI > 0.1), simulated, n = m = {n}", float((sims > 0.1).mean()), e_flag, 5e-4, ".3f")

    # Population PSI of a mean shift, deciles of N(0, 1) as bins.
    inner = np.array([-1.2815515655, -0.8416212336, -0.5244005127, -0.2533471031, 0.0])
    inner = np.concatenate([inner, -inner[3::-1]])  # deciles of N(0, 1)
    cdf_edges = np.concatenate([[0.0], norm_cdf(inner), [1.0]])
    check("decile edges reproduce 10% bins (max error)", float(np.abs(np.diff(cdf_edges) - 0.1).max()), 0.0000, 5e-10, ".4f")
    for shift, exp in [(0.1, 0.0096), (0.25, 0.0598), (0.5, 0.2377)]:
        shifted = np.concatenate([[0.0], norm_cdf(inner - shift), [1.0]])
        check(f"population PSI of a {shift} sd mean shift, deciles", psi_from_props(np.full(10, 0.1), np.diff(shifted)), exp, 5e-5)


# ---------------------------------------------------------------------------
# 3. Kolmogorov-Smirnov
# ---------------------------------------------------------------------------


def ks_stat(a: np.ndarray, b: np.ndarray) -> float:
    grid = np.sort(np.concatenate([a, b]))
    fa = np.searchsorted(np.sort(a), grid, side="right") / a.size
    fb = np.searchsorted(np.sort(b), grid, side="right") / b.size
    return float(np.abs(fa - fb).max())


def kolmogorov_sf(lam: float) -> float:
    return 2 * sum((-1) ** (k - 1) * math.exp(-2 * k * k * lam * lam) for k in range(1, 101))


def section_ks() -> None:
    # Backs: Worked example 4; cards ml-prod-ks, ml-prod-ks-vs-psi, ml-prod-psi-threshold.
    print("\n== 3. Kolmogorov-Smirnov ==")
    check(
        "KS statistic by hand, {1,2,3,4} vs {2.5,3.5,4.5,5.5}",
        ks_stat(np.array([1.0, 2, 3, 4]), np.array([2.5, 3.5, 4.5, 5.5])),
        0.50,
        1e-12,
        ".2f",
    )
    lo, hi = 0.5, 3.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if kolmogorov_sf(mid) > 0.05 else (lo, mid)
    c05 = 0.5 * (lo + hi)
    check("Kolmogorov 5% critical constant c", c05, 1.358, 5e-4, ".3f")
    n = 5000
    d_crit = c05 * math.sqrt(2 / n)
    check("KS 5% critical value, n = m = 5000", d_crit, 0.0272, 5e-5)
    check("population KS distance of a 0.1 sd shift, 2 Phi(0.05) - 1", float(2 * norm_cdf(0.05) - 1), 0.0399, 5e-5)
    # Calibrated PSI threshold: the chi-square 95% quantile scaled by (1/n + 1/m), the 5% test under no drift.
    psi_crit = chi2_quantile(0.95, 9) * (2 / n)
    check("calibrated 5% PSI threshold, 10 bins, n = m = 5000", psi_crit, 0.0068, 5e-5)
    rng = np.random.default_rng(13)
    rng_null = np.random.default_rng(113)  # separate stream so the shifted samples are unchanged by the null control
    ks_hits, psi_hits, psi_cal_hits, psi_vals = 0, 0, 0, []
    ks_null, psi_cal_null = 0, 0
    reps = 400
    for _ in range(reps):
        ref = rng.standard_normal(n)
        cur = rng.standard_normal(n) + 0.1
        ks_hits += ks_stat(ref, cur) > d_crit
        p = psi_samples(ref, cur)
        psi_vals.append(p)
        psi_hits += p > 0.1
        psi_cal_hits += p > psi_crit
    # Same tests on pairs with no shift: both calibrated rules should reject about 5% of the time.
    reps_null = 1000
    for _ in range(reps_null):
        ref0, cur0 = rng_null.standard_normal(n), rng_null.standard_normal(n)
        ks_null += ks_stat(ref0, cur0) > d_crit
        psi_cal_null += psi_samples(ref0, cur0) > psi_crit
    check("detection rate, KS at 5%, 0.1 sd shift, n = m = 5000", ks_hits / reps, 0.990, 5e-4, ".3f")
    check("detection rate, PSI > 0.1, same samples", psi_hits / reps, 0.000, 5e-4, ".3f")
    check("detection rate, PSI > calibrated 5% threshold, same samples", psi_cal_hits / reps, 0.950, 5e-4, ".3f")
    check("false-alarm rate with no shift, KS at 5%", ks_null / reps_null, 0.040, 5e-4, ".3f")
    check("false-alarm rate with no shift, calibrated PSI", psi_cal_null / reps_null, 0.049, 5e-4, ".3f")
    check("mean PSI, 0.1 sd shift, n = m = 5000", float(np.mean(psi_vals)), 0.013, 5e-4, ".3f")


# ---------------------------------------------------------------------------
# 4. Unit bug
# ---------------------------------------------------------------------------


def section_unit_bug() -> None:
    # Backs: Worked example 5; card ml-prod-unit-bug.
    print("\n== 4. Unit bug caught on the prediction distribution ==")
    rng = np.random.default_rng(14)
    beta = np.array([0.5, -0.3, 0.2])
    x_train = rng.standard_normal((20_000, 3)) * np.array([0.01, 0.02, 1.0])  # first two features are returns in decimals
    x_live = rng.standard_normal((2_000, 3)) * np.array([0.01, 0.02, 1.0])
    x_bug = x_live.copy()
    x_bug[:, 0] *= 100  # serving pipeline sends feature 1 in percent
    pred_train, pred_live, pred_bug = x_train @ beta, x_live @ beta, x_bug @ beta
    check("PSI of predictions, healthy live day", psi_samples(pred_train, pred_live), 0.011, 5e-4, ".3f")
    check("PSI of predictions, unit bug in one feature", psi_samples(pred_train, pred_bug), 0.84, 5e-3, ".2f")
    check("PSI of the buggy feature itself", psi_samples(x_train[:, 0], x_bug[:, 0]), 4.62, 5e-3, ".2f")


# ---------------------------------------------------------------------------
# 5. CUSUM on a decaying IC
# ---------------------------------------------------------------------------


def cusum_chain(mu: float, sd: float, k: float, h: float, cells: int = 400) -> tuple[np.ndarray, np.ndarray]:
    """Brook and Evans (1972) Markov chain for S_t = max(0, S_{t-1} + k - X_t), X_t ~ N(mu, sd^2), alarm when S_t > h.

    State 0 is the atom S = 0; states 1..cells are equal cells of (0, h] represented by their midpoints.
    Returns the substochastic transition matrix among non-alarm states and the start vector (S_0 = 0).
    """
    width = h / cells
    starts = np.concatenate([[0.0], (np.arange(cells) + 0.5) * width])
    bounds = np.arange(cells + 1) * width  # cell j covers (bounds[j-1], bounds[j]]
    z = (bounds[None, :] - starts[:, None] - (k - mu)) / sd
    cdf = norm_cdf(z)
    q = np.empty((cells + 1, cells + 1))
    q[:, 0] = cdf[:, 0]  # S_t = 0 when s + k - X <= 0
    q[:, 1:] = np.diff(cdf, axis=1)
    start = np.zeros(cells + 1)
    start[0] = 1.0
    return q, start


def section_cusum_ic() -> None:
    # Backs: Worked example 6 and TL;DR; cards ml-prod-cusum, ml-prod-ic-noise, ml-prod-arl.
    print("\n== 5. Detecting a dead signal ==")
    n_names = 200
    sd_ic = 1 / math.sqrt(n_names)
    check("daily IC standard error, 200 names, 1/sqrt(200)", sd_ic, 0.0707, 5e-5)
    mu0, mu1, k = 0.05, 0.0, 0.025
    rng = np.random.default_rng(15)
    paths, days, change, chunk = 10_000, 1200, 500, 2500
    # (h, simulated false-alarm share, median delay, Markov-chain false-alarm probability, ARL0 to 3 significant
    # figures, ARL1)
    cusum_cases = [
        (0.5, 0.310, 15, 0.311, 1320, 19.3),
        (0.75, 0.026, 24, 0.029, 16400, 29.3),
        (1.0, 0.002, 34, 0.002, 200000, 39.3),
    ]
    windows = [(20, 0.111, 19), (40, 0.001, 38.5), (60, 0.000, 59)]
    # First alarm day per path for each rule. Paths are simulated in chunks of rows to bound memory; the generator
    # fills arrays in row-major order, so the draws are identical to one (paths, days) draw.
    first_cusum = {h: np.full(paths, -1) for h, *_ in cusum_cases}
    first_roll = {w: np.full(paths, -1) for w, *_ in windows}
    mean_path = np.where(np.arange(days) < change, mu0, mu1)
    for lo in range(0, paths, chunk):
        ic = rng.standard_normal((chunk, days)) * sd_ic + mean_path
        # Page's CUSUM for a fall in the mean: S_t = max(0, S_{t-1} + (k - IC_t)), alarm when S_t > h.
        for h in first_cusum:
            s = np.zeros(chunk)
            first = np.full(chunk, -1)
            for t in range(days):
                s = np.maximum(0.0, s + (k - ic[:, t]))
                first[(s > h) & (first < 0)] = t
            first_cusum[h][lo : lo + chunk] = first
        csum = np.concatenate([np.zeros((chunk, 1)), np.cumsum(ic, axis=1)], axis=1)
        for w in first_roll:
            below = (csum[:, w:] - csum[:, :-w]) < 0.0  # column j: mean of days j..j+w-1 below 0, known at day j+w-1
            assert below.any(axis=1).all(), "every path must alarm within the simulated horizon"
            first_roll[w][lo : lo + chunk] = below.argmax(axis=1) + w - 1
    # Delays are measured on paths without a false alarm before the change; day 500 is the first dead day (delay 0).
    arls: dict[float, tuple[float, float]] = {}
    for h, exp_false, exp_delay, exp_chain, exp_arl0, exp_arl1 in cusum_cases:
        first_alarm = first_cusum[h]
        assert (first_alarm >= 0).all(), "every path must alarm within the simulated horizon"
        false_before = first_alarm < change
        delay = first_alarm[first_alarm >= change] - change
        sim_false = float(false_before.mean())
        check(f"CUSUM h {h}: share of paths with a false alarm in the 500 healthy days", sim_false, exp_false, 5e-4, ".3f")
        check(f"CUSUM h {h}: median detection delay (days)", float(np.median(delay)), exp_delay, 0.0, "g")
        # Independent check: probability of an alarm within 500 healthy days from the Brook and Evans chain, which
        # shares only the inputs (mu, sd, k, h) with the simulation.
        q0, start = cusum_chain(mu0, sd_ic, k, h)
        alive = start.copy()
        for _ in range(change):
            alive = alive @ q0
        chain_false = 1.0 - float(alive.sum())
        se = math.sqrt(chain_false * (1 - chain_false) / paths)
        check(f"CUSUM h {h}: Markov-chain P(false alarm in 500 healthy days)", chain_false, exp_chain, 5e-4, ".3f")
        print(f"CUSUM h {h}: simulation standard error = {se:.4f}")
        assert abs(sim_false - chain_false) < 4 * se + 1e-4, f"simulation {sim_false} vs chain {chain_false}"
        arl0 = float(start @ np.linalg.solve(np.eye(q0.shape[0]) - q0, np.ones(q0.shape[0])))
        q1, _ = cusum_chain(mu1, sd_ic, k, h)
        arl1 = float(start @ np.linalg.solve(np.eye(q1.shape[0]) - q1, np.ones(q1.shape[0])))
        arl0_3sf = float(f"{arl0:.3g}")
        assert abs(arl0 - exp_arl0) <= 0.005 * exp_arl0, f"ARL0 {arl0} vs {exp_arl0}"
        check(f"CUSUM h {h}: ARL0, mean days to a false alarm from S = 0 (3 significant figures)", arl0_3sf, exp_arl0, 0.0, ".0f")
        check(f"CUSUM h {h}: ARL1, mean days to detect from S = 0, counting the alarm day", arl1, exp_arl1, 0.05, ".1f")
        # Independent check of ARL1: simulate run lengths with the signal dead from day 0 (separate seed).
        sim_rng = np.random.default_rng(16)
        n_run, horizon = 4000, 400
        s1 = np.zeros(n_run)
        run = np.full(n_run, -1)
        for t in range(horizon):
            s1 = np.maximum(0.0, s1 + (k - (mu1 + sd_ic * sim_rng.standard_normal(n_run))))
            run[(s1 > h) & (run < 0)] = t + 1
        assert (run > 0).all(), "every dead-signal run must alarm within the horizon"
        se_run = float(run.std()) / math.sqrt(n_run)
        print(f"CUSUM h {h}: simulated ARL1 = {run.mean():.1f} (standard error {se_run:.2f})")
        assert abs(run.mean() - arl1) < 4 * se_run, f"simulated ARL1 {run.mean()} vs chain {arl1}"
        arls[h] = (arl0, arl1)
    # Card ml-prod-arl and Worked example 6: raising h by 0.25 multiplies ARL0 by about 12 and adds about 10 days to ARL1.
    for h_lo, h_hi in [(0.5, 0.75), (0.75, 1.0)]:
        check(f"ARL0 ratio, h {h_hi} over h {h_lo}", arls[h_hi][0] / arls[h_lo][0], 12.0, 0.5, ".0f")
        check(f"ARL1 increase, h {h_lo} to h {h_hi} (days)", arls[h_hi][1] - arls[h_lo][1], 10.0, 0.5, ".0f")
    for w, exp_false, exp_delay in windows:
        first = first_roll[w]
        false_roll = first < change
        delay_roll = first[first >= change] - change
        check(f"rolling {w}-day mean IC < 0: share of paths with a false alarm", float(false_roll.mean()), exp_false, 5e-4, ".3f")
        check(f"rolling {w}-day mean IC < 0: median detection delay (days)", float(np.median(delay_roll)), exp_delay, 0.0, "g")


if __name__ == "__main__":
    section_as_of()
    section_psi()
    section_ks()
    section_unit_bug()
    section_cusum_ic()
    print("\nall checks passed")
