"""Feature importance with a numpy random forest: MDI, MDA, drop-column, clustered MDA, SFI and exact Shapley values.

Backs 10-Machine-Learning-for-Finance/07-Feature-Importance-and-Interpretability.md.

Data: y = 0.5 x1 + 0.5 x3 + noise, where x2 is a near copy of x1 (correlation about 0.98), x4 and x6 are continuous
noise and x5 is binary noise. A random forest of regression trees (bootstrap rows, 3 of 6 features tried per split)
is fitted by the code below; no external ML library is used.

1. A two-player Shapley game by hand, and Linear SHAP: for a linear model, exact interventional Shapley values equal
   w_i (x_i - E[x_i]).
2. MDI (impurity decrease), MDA (permutation on a test set), drop-column refits, clustered MDA (x1 and x2 permuted
   together) and single-feature importance, showing the substitution effect.
3. Exact interventional Shapley values for the forest by enumerating all 64 coalitions, with the efficiency check.
4. Importance on a pure-noise target: MDI still sums to one, MDA does not.

Run: uv run --no-project --with numpy python 10-Machine-Learning-for-Finance/code/feature_importance.py
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

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


# ---------------------------------------------------------------------------
# Regression trees and forests in numpy
# ---------------------------------------------------------------------------


@dataclass
class Tree:
    feature: np.ndarray  # -1 for a leaf
    threshold: np.ndarray
    left: np.ndarray
    right: np.ndarray
    value: np.ndarray
    importance: np.ndarray  # total weighted impurity decrease per feature

    def predict(self, x: np.ndarray) -> np.ndarray:
        node = np.zeros(x.shape[0], dtype=np.int64)
        while True:
            feat = self.feature[node]
            active = feat >= 0
            if not active.any():
                return self.value[node]
            rows = np.nonzero(active)[0]
            go_left = x[rows, feat[active]] <= self.threshold[node[active]]
            node[rows] = np.where(go_left, self.left[node[active]], self.right[node[active]])


def build_tree(x: np.ndarray, y: np.ndarray, rng: np.random.Generator, max_depth: int, min_leaf: int, max_features: int) -> Tree:
    n, p = x.shape
    feature, threshold, left, right, value = [], [], [], [], []
    importance = np.zeros(p)
    stack = [(np.arange(n), 0, -1, False)]  # (rows, depth, parent, is_left)
    while stack:
        rows, depth, parent, is_left = stack.pop()
        node = len(feature)
        if parent >= 0:
            (left if is_left else right)[parent] = node
        feature.append(-1)
        threshold.append(0.0)
        left.append(-1)
        right.append(-1)
        yr = y[rows]
        value.append(float(yr.mean()))
        if depth >= max_depth or rows.size < 2 * min_leaf:
            continue
        sse_parent = float(((yr - yr.mean()) ** 2).sum())
        best = (0.0, -1, 0.0, None)
        for f in rng.choice(p, size=max_features, replace=False):
            order = np.argsort(x[rows, f], kind="stable")
            xs, ys = x[rows, f][order], yr[order]
            csum, csq = np.cumsum(ys), np.cumsum(ys * ys)
            k = np.arange(min_leaf, rows.size - min_leaf + 1)  # left child holds the first k sorted rows
            valid = xs[k - 1] < xs[k]
            if not valid.any():
                continue
            k = k[valid]
            sl, ql = csum[k - 1], csq[k - 1]
            sr, qr = csum[-1] - sl, csq[-1] - ql
            sse = (ql - sl * sl / k) + (qr - sr * sr / (rows.size - k))
            j = int(np.argmin(sse))
            gain = sse_parent - float(sse[j])
            if gain > best[0]:
                cut = int(k[j])
                best = (gain, int(f), 0.5 * (xs[cut - 1] + xs[cut]), rows[order[:cut]])
        gain, f, thr, rows_left = best
        if f < 0:
            continue
        feature[node], threshold[node] = f, thr
        importance[f] += gain
        rows_right = np.setdiff1d(rows, rows_left, assume_unique=True)
        stack.append((rows_right, depth + 1, node, False))
        stack.append((rows_left, depth + 1, node, True))
    return Tree(np.array(feature), np.array(threshold), np.array(left), np.array(right), np.array(value), importance)


class Forest:
    def __init__(self, x: np.ndarray, y: np.ndarray, seed: int, n_trees: int = 60, max_depth: int = 6, min_leaf: int = 20):
        rng = np.random.default_rng(seed)
        p = x.shape[1]
        max_features = max(1, math.ceil(p / 2))
        self.trees = []
        for _ in range(n_trees):
            boot = rng.integers(0, x.shape[0], size=x.shape[0])
            self.trees.append(build_tree(x[boot], y[boot], rng, max_depth, min_leaf, max_features))

    def predict(self, x: np.ndarray) -> np.ndarray:
        return np.mean([t.predict(x) for t in self.trees], axis=0)

    def mdi(self) -> np.ndarray:
        """Mean decrease impurity: each tree's importances normalised to sum to one, then averaged."""
        per_tree = [t.importance / t.importance.sum() for t in self.trees if t.importance.sum() > 0]
        return np.mean(per_tree, axis=0)


def r2(y: np.ndarray, yhat: np.ndarray) -> float:
    return 1.0 - float(((y - yhat) ** 2).sum() / ((y - y.mean()) ** 2).sum())


def make_data(rng: np.random.Generator, n: int, signal: bool = True) -> tuple[np.ndarray, np.ndarray]:
    x1 = rng.standard_normal(n)
    x2 = x1 + 0.2 * rng.standard_normal(n)
    x3 = rng.standard_normal(n)
    x4 = rng.standard_normal(n)
    x5 = (rng.random(n) < 0.5).astype(float)
    x6 = rng.random(n)
    x = np.column_stack([x1, x2, x3, x4, x5, x6])
    y = (0.5 * x1 + 0.5 * x3 if signal else 0.0) + rng.standard_normal(n)
    return x, y


# ---------------------------------------------------------------------------
# 1. Shapley values: a toy game and Linear SHAP
# ---------------------------------------------------------------------------


def shapley_from_values(v: dict[frozenset, np.ndarray], p: int) -> np.ndarray:
    """Exact Shapley values given the value of every coalition (each value may be a vector over explained points)."""
    phi = [0.0] * p
    for k in range(p):
        others = [j for j in range(p) if j != k]
        for size in range(p):
            weight = math.factorial(size) * math.factorial(p - size - 1) / math.factorial(p)
            for s in itertools.combinations(others, size):
                fs = frozenset(s)
                phi[k] = phi[k] + weight * (v[fs | {k}] - v[fs])
    return np.array(phi)


def interventional_values(f, x_explain: np.ndarray, background: np.ndarray) -> dict[frozenset, np.ndarray]:
    """v(S) at each explained point: E over background rows of f(x_S, background_{not S})."""
    n_e, p = x_explain.shape
    n_b = background.shape[0]
    values = {}
    for size in range(p + 1):
        for s in itertools.combinations(range(p), size):
            mask = np.zeros(p, dtype=bool)
            mask[list(s)] = True
            hybrid = np.repeat(background[None, :, :], n_e, axis=0)
            hybrid[:, :, mask] = x_explain[:, None, mask]
            values[frozenset(s)] = f(hybrid.reshape(n_e * n_b, p)).reshape(n_e, n_b).mean(axis=1)
    return values


def section_shapley_basics() -> None:
    # Backs: Worked example 1; cards ml-fi-shapley-game, ml-fi-linear-shap.
    print("\n== 1. Shapley values by hand and Linear SHAP ==")
    game = {frozenset(): 0.0, frozenset({0}): 2.0, frozenset({1}): 1.0, frozenset({0, 1}): 5.0}
    phi = shapley_from_values(game, 2)
    check("toy game Shapley value of player 1", float(phi[0]), 3.0, 1e-12, ".1f")
    check("toy game Shapley value of player 2", float(phi[1]), 2.0, 1e-12, ".1f")

    rng = np.random.default_rng(0)
    w, b = np.array([1.5, -2.0, 0.5]), 0.3
    background = rng.standard_normal((40, 3))
    x_explain = rng.standard_normal((5, 3))
    vals = interventional_values(lambda z: z @ w + b, x_explain, background)
    phi = shapley_from_values(vals, 3)
    linear = (w[:, None] * (x_explain - background.mean(axis=0)).T).astype(float)
    check_below("Linear SHAP: max |exact Shapley - w_i (x_i - mean_i)|", float(np.abs(phi - linear).max()), 1e-12)


# ---------------------------------------------------------------------------
# 2. MDI, MDA, drop-column, clustered MDA and SFI
# ---------------------------------------------------------------------------


def permutation_drop(model: Forest, x: np.ndarray, y: np.ndarray, cols: list[int], rng: np.random.Generator, reps: int = 5) -> float:
    base = r2(y, model.predict(x))
    drops = []
    for _ in range(reps):
        xp = x.copy()
        perm = rng.permutation(x.shape[0])
        xp[:, cols] = x[perm][:, cols]  # one permutation for all columns in the group keeps their joint distribution
        drops.append(base - r2(y, model.predict(xp)))
    return float(np.mean(drops))


NAMES = ["x1", "x2 (copy of x1)", "x3", "x4 (noise)", "x5 (binary noise)", "x6 (noise)"]


def section_importance() -> None:
    # Backs: Worked example 2; cards ml-fi-mdi-bias, ml-fi-correlated-mda, ml-fi-drop-column, ml-fi-substitution.
    print("\n== 2. MDI, MDA, drop-column, clustered MDA and SFI ==")
    rng = np.random.default_rng(42)
    x_tr, y_tr = make_data(rng, 3000)
    x_te, y_te = make_data(rng, 3000)
    check("correlation of x1 and x2", float(np.corrcoef(x_tr[:, 0], x_tr[:, 1])[0, 1]), 0.981, 5e-4, ".3f")
    check("population R^2 of the true model", 0.5 / 1.5, 0.333, 5e-4, ".3f")
    forest = Forest(x_tr, y_tr, seed=1)
    base = r2(y_te, forest.predict(x_te))
    check("forest test R^2", base, 0.319, 5e-4, ".3f")
    mdi = forest.mdi()
    perm_rng = np.random.default_rng(7)
    exp_mdi = [0.277, 0.202, 0.458, 0.028, 0.004, 0.031]
    exp_mda = [0.121, 0.051, 0.312, -0.002, 0.000, 0.000]
    for j in range(6):
        check(f"MDI {NAMES[j]}", float(mdi[j]), exp_mdi[j], 5e-4, ".3f")
    check("MDI x1 + x2", float(mdi[0] + mdi[1]), 0.479, 5e-4, ".3f")
    for j in range(6):
        check(f"MDA (test R^2 drop) {NAMES[j]}", permutation_drop(forest, x_te, y_te, [j], perm_rng), exp_mda[j], 5e-4, ".3f")
    check("clustered MDA, x1 and x2 permuted together", permutation_drop(forest, x_te, y_te, [0, 1], perm_rng), 0.323, 5e-4, ".3f")

    exp_drop = [0.005, 0.005, 0.165, 0.003, 0.003, 0.002]
    for j in range(6):
        keep = [k for k in range(6) if k != j]
        refit = Forest(x_tr[:, keep], y_tr, seed=1)
        check(f"drop-column importance {NAMES[j]}", base - r2(y_te, refit.predict(x_te[:, keep])), exp_drop[j], 5e-4, ".3f")
    refit = Forest(x_tr[:, 2:], y_tr, seed=1)
    check("drop-column importance of the x1-x2 cluster", base - r2(y_te, refit.predict(x_te[:, 2:])), 0.161, 5e-4, ".3f")

    exp_sfi = [0.146, 0.146, 0.150, -0.004, -0.002, -0.017]
    for j in range(6):
        single = Forest(x_tr[:, [j]], y_tr, seed=1)
        check(f"SFI (test R^2 of a forest on {NAMES[j]} alone)", r2(y_te, single.predict(x_te[:, [j]])), exp_sfi[j], 5e-4, ".3f")

    # 3. Exact interventional Shapley values for the forest.
    print("\n== 3. Exact Shapley values for the forest ==")
    background = x_tr[:50]
    x_explain = x_te[:100]
    vals = interventional_values(forest.predict, x_explain, background)
    phi = shapley_from_values(vals, 6)
    gap = np.abs(phi.sum(axis=0) - (forest.predict(x_explain) - forest.predict(background).mean())).max()
    check_below("Shapley efficiency: max |sum phi - (f(x) - E f)|", float(gap), 1e-10)
    exp_shap = [0.233, 0.141, 0.438, 0.014, 0.003, 0.015]
    for j in range(6):
        check(f"mean |SHAP| {NAMES[j]}", float(np.abs(phi[j]).mean()), exp_shap[j], 5e-4, ".3f")
    check("mean |SHAP of x1 + SHAP of x2|", float(np.abs(phi[0] + phi[1]).mean()), 0.372, 5e-4, ".3f")


# ---------------------------------------------------------------------------
# 4. Pure-noise target
# ---------------------------------------------------------------------------


def section_noise_target() -> None:
    # Backs: Worked example 3; card ml-fi-mdi-noise.
    print("\n== 4. Importance on a pure-noise target ==")
    rng = np.random.default_rng(99)
    x_tr, y_tr = make_data(rng, 3000, signal=False)
    x_te, y_te = make_data(rng, 3000, signal=False)
    forest = Forest(x_tr, y_tr, seed=2)
    mdi = forest.mdi()
    check("noise target: forest test R^2", r2(y_te, forest.predict(x_te)), -0.006, 5e-4, ".3f")
    check("noise target: sum of MDI", float(mdi.sum()), 1.000, 1e-9, ".3f")
    check("noise target: largest MDI", float(mdi.max()), 0.234, 5e-4, ".3f")
    check("noise target: MDI of the binary feature", float(mdi[4]), 0.012, 5e-4, ".3f")
    perm_rng = np.random.default_rng(8)
    mda = [permutation_drop(forest, x_te, y_te, [j], perm_rng) for j in range(6)]
    check("noise target: largest MDA", max(mda), 0.002, 5e-4, ".3f")


if __name__ == "__main__":
    section_shapley_basics()
    section_importance()
    section_noise_target()
    print("\nall checks passed")
