"""Time-series cross-validation, purging and embargo: every number in the note, by an independent route.

Backs every number in `10-Machine-Learning-for-Finance/02-Time-Series-Cross-Validation-Purging-Embargo.md`.
Independent routes used here:
- purge and embargo counts from the vectorised splitter in the note checked against a brute-force loop over every
  pair of training and test information intervals;
- the kNN leakage study rerun exactly as printed in the note (seed 0), then over 100 seeded datasets;
- overlapping-label autocorrelations by counting shared returns and by simulation, the variance inflation of the mean
  by summing the exact covariance matrix, and the naive t-stat inflation by simulation;
- uniqueness weights with exact fractions from a bar-by-bar concurrency count;
- CPCV splits and paths by enumerating every combination of test groups;
- the walk-forward schedule by enumerating its windows.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 10-Machine-Learning-for-Finance/code/ml_02_purged_cv.py`.
"""

from __future__ import annotations

import itertools
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
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, expected {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (expected {expected:.4f}, tolerance {tol:.4f})")


# ------------------------------------------------------------------ the splitters printed in the note


def purged_kfold(t0, t1, n_splits=5, embargo=0):
    idx = np.arange(len(t0))
    for test in np.array_split(idx, n_splits):
        lo, hi = t0[test].min(), t1[test].max()
        overlap = (t0 <= hi) & (t1 >= lo)
        embargoed = (t0 > hi) & (t0 <= hi + embargo)
        yield idx[~overlap & ~embargoed], test


def shuffled_kfold(n, n_splits=5, seed=0):
    perm = np.random.default_rng(seed).permutation(n)
    for test in np.array_split(perm, n_splits):
        yield np.setdiff1d(perm, test), test


def knn_predict(x_train, y_train, x_test, k=10):
    d = np.abs(x_test[:, None] - x_train[None, :])
    return y_train[np.argpartition(d, k, axis=1)[:, :k]].mean(axis=1)


def cv_ic(x, y, splits, demean_folds=False):
    pred, true = [], []
    for tr, te in splits:
        p, t = knn_predict(x[tr], y[tr], x[te]), y[te]
        if demean_folds:  # control: remove each fold's own mean before pooling
            p, t = p - p.mean(), t - t.mean()
        pred.append(p)
        true.append(t)
    return np.corrcoef(np.concatenate(pred), np.concatenate(true))[0, 1]


def dataset(rng: np.random.Generator, T: int = 2000, h: int = 20):
    r = rng.standard_normal(T + h)
    y = np.array([r[t + 1 : t + 1 + h].sum() for t in range(T)])
    x = np.zeros(T)
    for t in range(1, T):
        x[t] = 0.99 * x[t - 1] + rng.standard_normal()
    return x, y


# ------------------------------------------------------------------ sections


def purge_counts() -> None:
    print("Worked example 1: purged and embargoed counts (card ml-cv-purge-count)")
    T, h, e = 1000, 5, 10
    exact("embargo 0.01 T", round(0.01 * T), e)
    t0 = np.arange(T)
    t1 = t0 + h
    folds = list(purged_kfold(t0, t1, embargo=e))
    sizes = []
    for k, (train, test) in enumerate(folds):
        lo, hi = int(t0[test].min()), int(t1[test].max())
        # brute force: classify every non-test sample by looping over the test samples' intervals
        purged_before, purged_after, embargoed = [], [], []
        keep = []
        for j in range(T):
            if lo <= j <= int(test.max()):
                continue
            overlaps = any(t0[j] <= t1[i] and t1[j] >= t0[i] for i in test)
            if overlaps and j < lo:
                purged_before.append(j)
            elif overlaps:
                purged_after.append(j)
            elif hi < t0[j] <= hi + e:
                embargoed.append(j)
            else:
                keep.append(j)
        assert keep == train.tolist(), k
        sizes.append(len(train))
        if k == 1:
            exact("fold 2 test samples", (int(test.min()), int(test.max())), (200, 399))
            exact("fold 2 span", (lo, hi), (200, 404))
            exact("fold 2 purged before", purged_before, list(range(195, 200)))
            exact("their label ends", [int(t1[j]) for j in purged_before], list(range(200, 205)))
            exact("fold 2 purged after", purged_after, list(range(400, 405)))
            exact("fold 2 embargoed", embargoed, list(range(405, 415)))
            exact("counts", (len(purged_before), len(purged_after), len(embargoed)), (5, 5, 10))
    exact("training sizes, folds 1 to 5", sizes, [785, 780, 780, 780, 795])
    exact("interior loss 2h + e", 2 * h + e, 20)


def knn_leak() -> None:
    print("Worked example 2: the kNN leak (card ml-cv-knn-leak)")
    T, h = 2000, 20
    t0, t1 = np.arange(T), np.arange(T) + h
    rng = np.random.default_rng(0)  # exactly the snippet in the note
    x, y = dataset(rng, T, h)
    approx("seed 0: shuffled k-fold IC", float(cv_ic(x, y, shuffled_kfold(T))), 0.139, 3)
    approx("seed 0: contiguous k-fold IC", float(cv_ic(x, y, purged_kfold(t0, t0, embargo=0))), -0.093, 3)
    approx("seed 0: purged + embargo IC", float(cv_ic(x, y, purged_kfold(t0, t1, embargo=20))), -0.059, 3)
    shuffled, contiguous, purged, purged_dm, shuffled_dm = [], [], [], [], []
    for s in range(1, 101):
        x, y = dataset(np.random.default_rng(SEED + s), T, h)
        shuffled.append(cv_ic(x, y, shuffled_kfold(T, seed=s)))
        shuffled_dm.append(cv_ic(x, y, shuffled_kfold(T, seed=s), demean_folds=True))
        contiguous.append(cv_ic(x, y, purged_kfold(t0, t0, embargo=0)))
        purged.append(cv_ic(x, y, purged_kfold(t0, t1, embargo=20)))
        purged_dm.append(cv_ic(x, y, purged_kfold(t0, t1, embargo=20), demean_folds=True))
    shuffled, contiguous, purged = np.array(shuffled), np.array(contiguous), np.array(purged)
    purged_dm, shuffled_dm = np.array(purged_dm), np.array(shuffled_dm)
    approx("100 datasets: mean shuffled IC", float(shuffled.mean()), 0.12, 2)
    exact("100 datasets: shuffled IC positive", int((shuffled > 0).sum()), 100)
    approx("100 datasets: mean contiguous IC", float(contiguous.mean()), -0.03, 2)
    approx("100 datasets: mean purged + embargo IC", float(purged.mean()), -0.03, 2)
    approx("100 datasets: sd of purged + embargo IC", float(purged.std(ddof=1)), 0.07, 2)
    se = purged.std(ddof=1) / math.sqrt(len(purged))
    assert purged.mean() < -3 * se, (purged.mean(), se)
    print(f"    pooled purged IC is below zero by more than 3 standard errors ({se:.4f})")
    # control, one change: demean predictions and labels within each fold before pooling
    se_dm = purged_dm.std(ddof=1) / math.sqrt(len(purged_dm))
    approx("purged + embargo, demeaned within folds: mean IC", float(purged_dm.mean()), -0.002, 3)
    approx("its standard error", float(se_dm), 0.006, 3)
    simulated("demeaned purged mean IC against the true IC 0", float(purged_dm.mean()), 0.0, 3 * se_dm)
    approx("shuffled, demeaned within folds: mean IC (the leak survives)", float(shuffled_dm.mean()), 0.12, 2)
    assert shuffled.mean() > 10 * shuffled.std(ddof=1) / math.sqrt(len(shuffled))
    print("    shuffled mean IC is more than 10 standard errors above zero")


def overlap_stats() -> None:
    print("Worked example 3 and the overlap cards (ml-cv-overlap-correlation, ml-cv-overlap-tstat)")
    h = 21
    exact("non-overlapping labels in 2520 days", 2520 // h, 120)
    exact("shared returns, adjacent and 5 apart", (Fraction(h - 1, h), Fraction(h - 5, h)), (Fraction(20, 21), Fraction(16, 21)))
    approx("16/21 in percent", 100 * 16 / 21, 76, 0)
    # counting: labels t and t+k share the returns t+k+1 .. t+h
    for hh, k, q in ((20, 5, Fraction(15, 20)), (21, 5, Fraction(16, 21))):
        shared = len(set(range(1, hh + 1)) & set(range(k + 1, k + hh + 1)))
        exact(f"h = {hh}, lag {k}: shared / h", Fraction(shared, hh), q)
    approx("15/20", 15 / 20, 0.75, 2)
    rng = np.random.default_rng(SEED)
    r = rng.standard_normal(2_000_000 + 20)
    c = np.cumsum(np.concatenate([[0.0], r]))
    y20 = c[20:] - c[:-20]
    simulated("simulated lag-5 autocorrelation of 20-day sums", float(np.corrcoef(y20[:-5], y20[5:])[0, 1]), 0.75, 0.005)
    # exact variance of the sum of T overlapping labels from the covariance (h - |s-t|)^+ of iid unit returns
    T = 2520
    lags = np.arange(-(h - 1), h)
    var_sum = float(sum((T - abs(k)) * (h - abs(k)) for k in lags))
    ratio = var_sum / (T * h)
    approx("exact variance inflation of the mean, T = 2520, h = 21", ratio, 21, 0)
    approx("exact variance inflation of the mean, one decimal", ratio, 20.9, 1)
    approx("long-run factor 1 + 2 sum (h-k)/h", 1 + 2 * sum(Fraction(h - k, h) for k in range(1, h)), 21, 12)
    approx("sqrt(21)", math.sqrt(21), 4.6, 1)
    approx("6 / sqrt(21)", 6 / math.sqrt(21), 1.3, 1)
    # naive t-stat of the mean of overlapping labels under the null, by simulation
    reps = 4000
    tstats = np.empty(reps)
    t_iid = np.empty(reps)
    for i in range(reps):
        rr = rng.standard_normal(T + h)
        cc = np.cumsum(np.concatenate([[0.0], rr]))
        lab = cc[h + 1 : T + h + 1] - cc[1 : T + 1]
        tstats[i] = lab.mean() / (math.sqrt(h) / math.sqrt(T))  # t with the true label sd, so only the overlap acts
        # control, one change: regress the same labels on an iid regressor instead of a constant
        xr = rng.standard_normal(T)
        xc = xr - xr.mean()
        slope = xc @ lab / (xc @ xc)
        resid = lab - lab.mean() - slope * xc
        t_iid[i] = slope / math.sqrt(resid @ resid / (T - 2) / (xc @ xc))
    sd = float(tstats.std())
    simulated("sd of the iid-formula t under the null, T = 2520, h = 21", sd, math.sqrt(ratio), 4 * sd / math.sqrt(2 * reps))
    sd_iid = float(t_iid.std())
    simulated("sd of naive slope t on an iid regressor (factor 1)", sd_iid, 1.0, 4 * sd_iid / math.sqrt(2 * reps))


def uniqueness() -> None:
    print("Worked example 4: uniqueness weights (card ml-cv-uniqueness)")
    labels = {"A": (1, 3), "B": (2, 4), "C": (4, 5)}
    conc = {b: sum(1 for lo, hi in labels.values() if lo <= b <= hi) for b in range(1, 6)}
    exact("concurrency, bars 1 to 5", [conc[b] for b in range(1, 6)], [1, 2, 2, 2, 1])
    u = {k: sum((Fraction(1, conc[b]) for b in range(lo, hi + 1)), Fraction(0)) / (hi - lo + 1) for k, (lo, hi) in labels.items()}
    exact("uniqueness A, B, C", (u["A"], u["B"], u["C"]), (Fraction(2, 3), Fraction(1, 2), Fraction(3, 4)))
    avg = sum(u.values(), Fraction(0)) / 3
    exact("average uniqueness", avg, Fraction(23, 36))
    approx("average uniqueness", float(avg), 0.64, 2)
    approx("effective labels 3 x average", float(3 * avg), 1.9, 1)
    for h in (5, 21):
        T = 300
        spans = [(t, t + h - 1) for t in range(T)]
        conc2 = np.zeros(T + h)
        for lo, hi in spans:
            conc2[lo : hi + 1] += 1
        mid = [np.mean(1 / conc2[lo : hi + 1]) for lo, hi in spans[h : T - h]]
        approx(f"steady-state uniqueness for h = {h}, min over labels", float(np.min(mid)), 1 / h, 12)
        approx(f"steady-state uniqueness for h = {h}, max over labels", float(np.max(mid)), 1 / h, 12)


def cpcv() -> None:
    print("CPCV splits and paths (cards ml-cv-cpcv-paths and ml-pset-cpcv-paths)")
    for n_groups in range(2, 11):
        for k in range(1, n_groups):
            splits = list(itertools.combinations(range(n_groups), k))
            per_group = [sum(1 for s in splits if g in s) for g in range(n_groups)]
            assert len(set(per_group)) == 1
            assert per_group[0] == math.comb(n_groups - 1, k - 1) == Fraction(k, n_groups) * math.comb(n_groups, n_groups - k)
    splits = list(itertools.combinations(range(6), 2))
    exact("N = 6, k = 2: splits", len(splits), 15)
    exact("N = 6, k = 2: times each group is tested (paths)", sum(1 for s in splits if 0 in s), 5)
    splits = list(itertools.combinations(range(10), 2))
    exact("N = 10, k = 2: splits and paths", (len(splits), sum(1 for s in splits if 0 in s)), (45, 9))


def walk_forward() -> None:
    print("Worked example 5: walk-forward schedule (card ml-cv-walk-forward-gap)")
    starts = []
    s = Fraction(3)
    while s + Fraction(1, 2) <= 10:
        starts.append(s)
        s += Fraction(1, 2)
    exact("first and last test start (years)", (float(starts[0]), float(starts[-1])), (3.0, 9.5))
    exact("number of test windows", len(starts), 14)
    exact("years out of sample", len(starts) * Fraction(1, 2), 7)


def main() -> None:
    purge_counts()
    knn_leak()
    overlap_stats()
    uniqueness()
    cpcv()
    walk_forward()
    print("All purged cross-validation numbers verified.")


if __name__ == "__main__":
    main()
