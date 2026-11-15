"""Tree ensembles and gradient boosting: every number in the note, by an independent route.

Backs every number in `10-Machine-Learning-for-Finance/03-Tree-Ensembles-and-Gradient-Boosting.md`.
Independent routes used here:
- Gini impurities with exact fractions from explicit label lists;
- the variance of an average of correlated trees by summing the exact covariance matrix and by simulating a
  common-factor model, against the closed form;
- the out-of-bag fraction by simulating bootstraps, against (1 - 1/n)^n and its limit e^-1;
- the boosting-by-hand stump by brute force over every split, with exact fractions;
- the XGBoost leaf weight and split gains by grid-minimising the second-order objective directly, and the updated
  probability through the logistic function;
- the weak-signal experiment with numpy trees written here (a level-wise vectorised builder), whose splits are first
  checked against an independent recursive builder on a test problem; no external ML library is used.
Every quoted number is printed as ``label = value`` and asserted.
Run it with `python 10-Machine-Learning-for-Finance/code/ml_03_trees.py`.
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
    assert abs(estimate - expected) <= tol, f"{label}: simulated {estimate!r}, expected {expected} +/- {tol}"
    print(f"    {label} ~ {estimate:.4f} (expected {expected:.4f}, tolerance {tol:.4f})")


# ------------------------------------------------------------------ worked examples 1 to 4


def gini(labels: list[int]) -> Fraction:
    n = len(labels)
    return 1 - sum((Fraction(labels.count(c), n) ** 2 for c in set(labels)), Fraction(0))


def gini_split() -> None:
    print("Example 1: Gini split (card ml-trees-gini-split)")
    parent = [1] * 6 + [0] * 4
    exact("parent Gini", gini(parent), Fraction(12, 25))
    a_left, a_right = [1] * 4, [1] * 2 + [0] * 4
    b_left, b_right = [1] * 3 + [0], [1] * 3 + [0] * 3
    wa = Fraction(4, 10) * gini(a_left) + Fraction(6, 10) * gini(a_right)
    wb = Fraction(4, 10) * gini(b_left) + Fraction(6, 10) * gini(b_right)
    approx("Gini of (2 up, 4 down)", float(gini(a_right)), 0.444, 3)
    approx("split A weighted Gini", float(wa), 0.267, 3)
    approx("split A decrease", float(gini(parent) - wa), 0.213, 3)
    exact("Gini of (3, 1) and (3, 3)", (gini(b_left), gini(b_right)), (Fraction(3, 8), Fraction(1, 2)))
    exact("split B weighted Gini", wb, Fraction(45, 100))
    exact("split B decrease", gini(parent) - wb, Fraction(3, 100))


def averaging(rng: np.random.Generator) -> None:
    print("Example 2: variance of an average of correlated trees (card ml-trees-bagging-variance)")

    def by_matrix(rho: float, b: int) -> float:
        cov = np.full((b, b), rho) + (1 - rho) * np.eye(b)
        return float(cov.sum() / b**2)

    for rho, b, quoted, dec in ((0.3, 10, 0.37, 2), (0.3, 500, 0.3014, 4), (0.1, 500, 0.1, 2), (0.8, 500, 0.80, 2)):
        v = by_matrix(rho, b)
        assert abs(v - (rho + (1 - rho) / b)) < 1e-12
        approx(f"rho = {rho}, B = {b}: variance of the average", v, quoted, dec)
    cut = (by_matrix(0.3, 10) - by_matrix(0.3, 500)) / by_matrix(0.3, 10)
    approx("relative cut from 10 to 500 trees (less than a fifth)", cut, 0.185, 3)
    assert cut < 0.2
    reps = 200_000
    common = rng.standard_normal(reps)
    trees = math.sqrt(0.3) * common[:, None] + math.sqrt(0.7) * rng.standard_normal((reps, 10))
    avg = trees.mean(axis=1)
    se = avg.var() * math.sqrt(2 / reps)
    simulated("simulated variance, rho = 0.3, B = 10", float(avg.var()), 0.37, 4 * se)


def oob(rng: np.random.Generator) -> None:
    print("Out-of-bag fraction (card ml-trees-oob-fraction)")
    n = 1000
    approx("(1 - 1/n)^n, n = 1000", (1 - 1 / n) ** n, 0.368, 3)
    approx("e^-1", math.exp(-1), 0.368, 3)
    approx("in-bag fraction 1 - e^-1 (percent)", 100 * (1 - math.exp(-1)), 63.2, 1)
    draws = rng.integers(0, n, size=(2000, n))
    in_bag = np.array([np.unique(d).size for d in draws]) / n
    simulated("simulated out-of-bag fraction", float(1 - in_bag.mean()), (1 - 1 / n) ** n, 4 * in_bag.std() / math.sqrt(2000))


def boosting_by_hand() -> None:
    print("Example 3: boosting by hand with squared loss (card ml-trees-boosting-by-hand)")
    x = [1, 2, 3, 4]
    y = [Fraction(v) for v in (1, 3, 2, 6)]
    f0 = sum(y, Fraction(0)) / 4
    r = [v - f0 for v in y]
    exact("F0 and residuals", (f0, r), (Fraction(3), [Fraction(-2), Fraction(0), Fraction(-1), Fraction(3)]))
    exact("initial squared error", sum((v * v for v in r), Fraction(0)), 14)
    table = {}
    for cut in (Fraction(3, 2), Fraction(5, 2), Fraction(7, 2)):
        left = [ri for xi, ri in zip(x, r, strict=True) if xi <= cut]
        right = [ri for xi, ri in zip(x, r, strict=True) if xi > cut]
        ml, mr = sum(left, Fraction(0)) / len(left), sum(right, Fraction(0)) / len(right)
        sse = sum(((v - ml) ** 2 for v in left), Fraction(0)) + sum(((v - mr) ** 2 for v in right), Fraction(0))
        table[cut] = (ml, mr, sse)
    approx("x <= 1.5: left, right means and SSE", float(table[Fraction(3, 2)][1]), 0.67, 2)
    approx("x <= 1.5: SSE", float(table[Fraction(3, 2)][2]), 8.67, 2)
    exact("x <= 1.5: left mean", table[Fraction(3, 2)][0], -2)
    exact("x <= 2.5: means and SSE", table[Fraction(5, 2)], (-1, 1, 10))
    exact("x <= 3.5: means and SSE", table[Fraction(7, 2)], (-1, 3, 2))
    best = min(table, key=lambda c: table[c][2])
    exact("best cut", best, Fraction(7, 2))
    ml, mr, _ = table[best]
    for eta, quoted_f, quoted_r, quoted_sse in (
        (
            Fraction(1, 10),
            [Fraction(29, 10)] * 3 + [Fraction(33, 10)],
            [Fraction(-19, 10), Fraction(1, 10), Fraction(-9, 10), Fraction(27, 10)],
            Fraction(1172, 100),
        ),
        (Fraction(1), None, None, Fraction(2)),
    ):
        f1 = [f0 + eta * (ml if xi <= best else mr) for xi in x]
        res = [yi - fi for yi, fi in zip(y, f1, strict=True)]
        sse = sum((v * v for v in res), Fraction(0))
        if quoted_f is not None:
            exact(f"eta = {eta}: F1", f1, quoted_f)
            exact(f"eta = {eta}: residuals", res, quoted_r)
        exact(f"eta = {eta}: squared error", sse, quoted_sse)


def xgboost_leaf() -> None:
    print("Example 4: XGBoost leaf and gains for log-loss (cards ml-trees-xgb-leaf-weight, ml-trees-xgb-gain-example)")
    y = np.array([1, 1, 0, 1])
    p = 0.5
    g = p - y
    h = np.full(4, p * (1 - p))
    exact("gradients", g.tolist(), [-0.5, -0.5, 0.5, -0.5])
    exact("Hessians", h.tolist(), [0.25] * 4)
    w_grid = np.linspace(-3, 3, 600_001)

    def leaf_min(idx: list[int], lam: float) -> tuple[float, float]:
        """Minimise sum_i (g_i w + h_i w^2 / 2) + lam w^2 / 2 over a grid: the second-order objective itself."""
        gs, hs = g[idx].sum(), h[idx].sum()
        obj = gs * w_grid + 0.5 * (hs + lam) * w_grid**2
        j = int(np.argmin(obj))
        return float(w_grid[j]), float(obj[j])

    exact("G and H of the single leaf", (float(g.sum()), float(h.sum())), (-1.0, 1.0))
    approx("lambda = 0: w* by grid search", leaf_min([0, 1, 2, 3], 0.0)[0], 1.0, 5)
    w1, obj_root = leaf_min([0, 1, 2, 3], 1.0)
    approx("lambda = 1: w* by grid search", w1, 0.5, 5)
    score = 0.1 * w1
    approx("eta = 0.1: new score", score, 0.05, 5)
    approx("new probability sigmoid(0.05)", 1 / (1 + math.exp(-score)), 0.512, 3)

    def gain(left: list[int], right: list[int]) -> float:
        return -(leaf_min(left, 1.0)[1] + leaf_min(right, 1.0)[1] - obj_root)  # objective reduction from splitting

    exact(
        "split {1,2} | {3,4}: G_L, H_L, G_R, H_R",
        (float(g[:2].sum()), float(h[:2].sum()), float(g[2:].sum()), float(h[2:].sum())),
        (-1.0, 0.5, 0.0, 0.5),
    )
    g1 = gain([0, 1], [2, 3])
    g2 = gain([0, 1, 3], [2])
    approx("gain of {1,2} | {3,4}", g1, 0.083, 3)
    approx("gain of {1,2,4} | {3}", g2, 0.493, 3)
    approx("closed form check 2.25/1.75 + 0.25/1.25 - 0.5, halved", 0.5 * (2.25 / 1.75 + 0.25 / 1.25 - 0.5), 0.493, 3)
    gamma = 0.1
    assert g1 - gamma < 0 < g2 - gamma
    print("    with gamma = 0.1 the first split is pruned and the second kept")


# ------------------------------------------------------------------ numpy regression trees


class Tree:
    def __init__(self) -> None:
        self.feature: list | np.ndarray = []
        self.threshold: list | np.ndarray = []
        self.left: list | np.ndarray = []
        self.right: list | np.ndarray = []
        self.value: list | np.ndarray = []

    def add_node(self, value: float) -> int:
        self.feature.append(-1)
        self.threshold.append(0.0)
        self.left.append(-1)
        self.right.append(-1)
        self.value.append(value)
        return len(self.feature) - 1

    def finish(self) -> Tree:
        self.feature = np.array(self.feature)
        self.threshold = np.array(self.threshold)
        self.left = np.array(self.left)
        self.right = np.array(self.right)
        self.value = np.array(self.value)
        return self

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


def build_tree(x: np.ndarray, y: np.ndarray, max_depth: int | None, min_leaf: int, max_features: int, rng: np.random.Generator) -> Tree:
    """Least-squares regression tree grown level by level; every node of a level is split in one vectorised pass.

    A split must leave at least ``min_leaf`` rows on each side and is made only if it lowers the squared error.
    ``max_features`` features, drawn per node, are searched; ties go to the lower feature index and the left-most cut.
    """
    n, p = x.shape
    tree = Tree()
    tree.add_node(float(y.mean()))
    node_of = np.zeros(n, dtype=np.int64)
    frontier = np.array([0]) if n >= 2 * min_leaf else np.array([], dtype=np.int64)
    depth = 0
    while frontier.size and (max_depth is None or depth < max_depth):
        compact = np.full(len(tree.feature), -1, dtype=np.int64)
        compact[frontier] = np.arange(frontier.size)
        rows = np.nonzero(compact[node_of] >= 0)[0]
        nd = compact[node_of[rows]]
        m = frontier.size
        cnt = np.bincount(nd, minlength=m)
        tot = np.bincount(nd, weights=y[rows], minlength=m)
        fmask = np.ones((m, p), dtype=bool)
        if max_features < p:
            fmask[:] = False
            pick = np.argsort(rng.random((m, p)), axis=1)[:, :max_features]
            np.put_along_axis(fmask, pick, True, axis=1)
        best = np.full(m, -np.inf)
        best_f = np.full(m, -1)
        best_thr = np.zeros(m)
        starts = np.concatenate([[0], np.cumsum(cnt)[:-1]])
        yr = y[rows]
        for f in range(p):
            xf = x[rows, f]
            order = np.lexsort((xf, nd))
            xs, ys, ns = xf[order], yr[order], nd[order]
            cs = np.cumsum(ys)
            base = np.where(starts > 0, cs[starts - 1], 0.0)
            ln = np.arange(rows.size) - starts[ns] + 1
            ls = cs - base[ns]
            rn = cnt[ns] - ln
            rs = tot[ns] - ls
            nxt = np.append(xs[1:], np.inf)
            valid = (ln >= min_leaf) & (rn >= min_leaf) & (xs < nxt) & fmask[ns, f]
            score = np.full(rows.size, -np.inf)
            score[valid] = ls[valid] ** 2 / ln[valid] + rs[valid] ** 2 / rn[valid]  # minus SSE, up to a node constant
            seg_max = np.maximum.reduceat(score, starts)
            first = np.minimum.reduceat(np.where(score == seg_max[ns], np.arange(rows.size), rows.size), starts)
            idx = np.nonzero(seg_max > best)[0]
            best[idx] = seg_max[idx]
            best_f[idx] = f
            best_thr[idx] = 0.5 * (xs[first[idx]] + xs[first[idx] + 1])
        parent = tot * tot / cnt
        split = np.nonzero((best_f >= 0) & (best - parent > 1e-12 * np.maximum(1.0, parent)))[0]
        if not split.size:
            break
        children = []
        for j in split:
            node = int(frontier[j])
            tree.feature[node] = int(best_f[j])
            tree.threshold[node] = float(best_thr[j])
            tree.left[node] = tree.add_node(0.0)
            tree.right[node] = tree.add_node(0.0)
            children += [tree.left[node], tree.right[node]]
        feat = np.array(tree.feature)
        cur = node_of[rows]
        moving = feat[cur] >= 0
        r2, c2 = rows[moving], cur[moving]
        go_left = x[r2, feat[c2]] <= np.array(tree.threshold)[c2]
        node_of[r2] = np.where(go_left, np.array(tree.left)[c2], np.array(tree.right)[c2])
        c_cnt = np.bincount(node_of, minlength=len(tree.feature))
        c_sum = np.bincount(node_of, weights=y, minlength=len(tree.feature))
        nxt_frontier = []
        for cid in children:
            tree.value[cid] = float(c_sum[cid] / c_cnt[cid])
            if c_cnt[cid] >= 2 * min_leaf:
                nxt_frontier.append(cid)
        frontier = np.array(sorted(nxt_frontier), dtype=np.int64)
        depth += 1
    return tree.finish()


def reference_tree_predict(x: np.ndarray, y: np.ndarray, x_new: np.ndarray, max_depth: int, min_leaf: int) -> np.ndarray:
    """Independent recursive builder (plain loops over every cut) used only to check ``build_tree``."""

    def grow(idx: np.ndarray, depth: int):
        mean = float(y[idx].mean())
        if depth >= max_depth or idx.size < 2 * min_leaf:
            return mean
        sse0 = float(((y[idx] - mean) ** 2).sum())
        best = (0.0, None)
        for f in range(x.shape[1]):
            vals = np.unique(x[idx, f])
            for a, b in zip(vals[:-1], vals[1:], strict=True):
                thr = 0.5 * (a + b)
                left, right = idx[x[idx, f] <= thr], idx[x[idx, f] > thr]
                if left.size < min_leaf or right.size < min_leaf:
                    continue
                sse = float(((y[left] - y[left].mean()) ** 2).sum() + ((y[right] - y[right].mean()) ** 2).sum())
                if sse0 - sse > best[0] + 1e-12:
                    best = (sse0 - sse, (f, thr, left, right))
        if best[1] is None:
            return mean
        f, thr, left, right = best[1]
        return (f, thr, grow(left, depth + 1), grow(right, depth + 1))

    def walk(node, row):
        while isinstance(node, tuple):
            f, thr, lo, hi = node
            node = lo if row[f] <= thr else hi
        return node

    root = grow(np.arange(x.shape[0]), 0)
    return np.array([walk(root, row) for row in x_new])


def r2(y: np.ndarray, yhat: np.ndarray) -> float:
    return float(1 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2))


def weak_signal() -> None:
    print("Example 5: overfitting a weak signal (card ml-trees-low-snr-overfit)")
    check = np.random.default_rng(SEED)
    xs = check.standard_normal((300, 3))
    ys = xs[:, 0] - 0.5 * xs[:, 1] ** 2 + check.standard_normal(300)
    x_new = check.standard_normal((200, 3))
    for depth, leaf in ((3, 5), (6, 5), (6, 1)):
        tree = build_tree(xs, ys, depth, leaf, 3, check)
        # same partition of the training rows; new points only where no tie between features can arise
        points = xs if leaf == 1 else np.vstack([xs, x_new])
        assert np.allclose(tree.predict(points), reference_tree_predict(xs, ys, points, depth, leaf), rtol=0, atol=1e-12), (depth, leaf)
    print("    vectorised and recursive builders give the same partition (depth 3 and 6 with leaf 5, depth 6 with leaf 1)")
    print("    (with leaf 1, different features can induce the same split of a tiny node, so only thresholds differ)")

    rng = np.random.default_rng(42)
    x = rng.standard_normal((10_000, 10))
    y = 0.1 * x[:, 0] + rng.standard_normal(10_000)
    xtr, ytr, xte, yte = x[:5000], y[:5000], x[5000:], y[5000:]
    approx("best possible R^2 = 0.01/1.01", 0.01 / 1.01, 0.0099, 4)
    oracle = r2(yte, 0.1 * xte[:, 0])
    approx("test R^2 of the true function", oracle, 0.012, 3)
    rng_models = np.random.default_rng(SEED + 1)
    results = {}

    f_tr, f_te = np.full(5000, ytr.mean()), np.full(5000, ytr.mean())
    for _ in range(500):
        t = build_tree(xtr, ytr - f_tr, 6, 1, 10, rng_models)
        f_tr += 0.1 * t.predict(xtr)
        f_te += 0.1 * t.predict(xte)
    results["boost deep"] = (r2(ytr, f_tr), r2(yte, f_te))

    f_tr, f_te = np.full(5000, ytr.mean()), np.full(5000, ytr.mean())
    for _ in range(100):
        sub = rng_models.choice(5000, 2500, replace=False)
        t = build_tree(xtr[sub], (ytr - f_tr)[sub], 2, 1, 10, rng_models)
        f_tr += 0.05 * t.predict(xtr)
        f_te += 0.05 * t.predict(xte)
    results["boost shallow"] = (r2(ytr, f_tr), r2(yte, f_te))

    for name, depth, leaf, m in (("forest full", None, 1, 10), ("forest regularised", None, 200, 3)):
        p_tr, p_te = np.zeros(5000), np.zeros(5000)
        for _ in range(100):
            boot = rng_models.integers(0, 5000, 5000)
            t = build_tree(xtr[boot], ytr[boot], depth, leaf, m, rng_models)
            p_tr += t.predict(xtr) / 100
            p_te += t.predict(xte) / 100
        results[name] = (r2(ytr, p_tr), r2(yte, p_te))

    quoted = {
        "boost deep": (0.904, -0.129),
        "boost shallow": (0.051, 0.003),
        "forest full": (0.858, -0.023),
        "forest regularised": (0.046, 0.007),
    }
    for name, (q_tr, q_te) in quoted.items():
        approx(f"{name}: train R^2", results[name][0], q_tr, 3)
        approx(f"{name}: test R^2", results[name][1], q_te, 3)
    approx("boost deep: train R^2, two decimals (TL;DR)", results["boost deep"][0], 0.90, 2)
    approx("boost deep: test R^2, two decimals (TL;DR)", results["boost deep"][1], -0.13, 2)
    # the regularised models cannot beat the true function out of sample; the defaults lose to the mean
    for name in ("boost shallow", "forest regularised"):
        assert 0 < results[name][1] <= oracle + 1e-9, name
    for name in ("boost deep", "forest full"):
        assert results[name][1] < 0 and results[name][0] > 0.8, name
    print("    regularised models land between 0 and the true function's test R^2; the defaults fit noise and lose to the mean")
    approx("regularised forest: share of the true function's test R^2", results["forest regularised"][1] / oracle, 0.6, 1)


def main() -> None:
    rng = np.random.default_rng(SEED)
    gini_split()
    averaging(rng)
    oob(rng)
    boosting_by_hand()
    xgboost_leaf()
    weak_signal()
    print("All tree-ensemble numbers verified.")


if __name__ == "__main__":
    main()
