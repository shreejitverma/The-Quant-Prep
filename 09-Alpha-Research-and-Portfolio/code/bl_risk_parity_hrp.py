"""Black-Litterman, equal risk contribution and hierarchical risk parity, with an out-of-sample test.

Backs the numbers in 12-Black-Litterman-Risk-Parity-and-HRP.md.

1. Black-Litterman: reverse optimisation, the posterior in its two algebraically equal forms,
   the He-Litterman "view portfolio halfway" result, tau invariance, and the weight tilt along P'.
2. Equal risk contribution (ERC): two-asset closed form and an N-asset Newton solve of the
   Spinu (2013) convex program, with the volatility ordering GMV <= ERC <= 1/N.
3. Hierarchical risk parity (Lopez de Prado 2016): correlation distance, Euclidean distance of
   distance columns, single linkage, quasi-diagonalisation and recursive bisection.
4. Monte Carlo: true out-of-sample variance and weight stability of GMV, inverse variance, ERC,
   HRP and 1/N estimated from short samples of a block-correlated market.

Every printed number is asserted so drift is caught.

Run: uv run --no-project --with numpy python 09-Alpha-Research-and-Portfolio/code/bl_risk_parity_hrp.py
"""

from __future__ import annotations

import numpy as np


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> None:
    printed, quoted = (s.removeprefix("-") if float(s) == 0 else s for s in (f"{value:{fmt}}", f"{expected:{fmt}}"))
    print(f"{label}: {printed}")
    assert abs(value - expected) <= tol, f"{label}: got {value}, expected {expected} +/- {tol}"
    if expected != 0 or not fmt.endswith("e"):  # zero in scientific format is a bound (tol); all else prints the quoted literal
        assert printed == quoted, f"{label}: prints {printed}, note quotes {quoted}"


def vec(label: str, v: np.ndarray, expected: list[float], fmt: str = ".4f") -> None:
    print(f"{label}: [" + ", ".join(f"{x:{fmt}}" for x in v) + "]")
    got = [f"{x:{fmt}}" for x in v]
    want = [f"{x:{fmt}}" for x in expected]
    assert got == want, f"{label}: prints {got}, note quotes {want}"


# ----------------------------------------------------------------------------
# Black-Litterman
# ----------------------------------------------------------------------------


def bl_posterior_precision_form(pi, sigma, tau, p, q, omega):
    """mu = [(tau S)^-1 + P' O^-1 P]^-1 [(tau S)^-1 pi + P' O^-1 q]; also returns the posterior covariance M."""
    ts_inv = np.linalg.inv(tau * sigma)
    o_inv = np.linalg.inv(omega)
    m = np.linalg.inv(ts_inv + p.T @ o_inv @ p)
    return m @ (ts_inv @ pi + p.T @ o_inv @ q), m


def bl_posterior_update_form(pi, sigma, tau, p, q, omega):
    """mu = pi + tau S P' (P tau S P' + O)^-1 (q - P pi)."""
    ts = tau * sigma
    return pi + ts @ p.T @ np.linalg.solve(p @ ts @ p.T + omega, q - p @ pi)


# ----------------------------------------------------------------------------
# Risk parity
# ----------------------------------------------------------------------------


def risk_contributions(w: np.ndarray, sigma: np.ndarray) -> np.ndarray:
    """Fractions RC_i / sigma_p^2 with RC_i = w_i (Sigma w)_i; they sum to one."""
    rc = w * (sigma @ w)
    return rc / rc.sum()


def erc_weights(sigma: np.ndarray, budget: np.ndarray | None = None, tol: float = 1e-12) -> np.ndarray:
    """Risk-budgeting weights from Newton's method on min 0.5 y'Sy - b' ln y (Spinu 2013), w = y / sum y."""
    n = sigma.shape[0]
    b = np.full(n, 1.0 / n) if budget is None else budget / budget.sum()
    y = 1.0 / np.sqrt(np.diag(sigma))
    y *= np.sqrt(1.0 / (y @ sigma @ y))
    for _ in range(100):
        grad = sigma @ y - b / y
        if np.linalg.norm(grad) < tol:
            return y / y.sum()
        hess = sigma + np.diag(b / y**2)
        step = np.linalg.solve(hess, grad)
        t = 1.0
        while np.any(y - t * step <= 0):  # stay in the positive orthant
            t *= 0.5
        y = y - t * step
    raise RuntimeError("ERC Newton iteration did not converge")


def gmv(sigma: np.ndarray) -> np.ndarray:
    w = np.linalg.solve(sigma, np.ones(sigma.shape[0]))
    return w / w.sum()


def gmv_long_only(sigma: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    """Long-only minimum variance, min w'Sw s.t. sum w = 1, w >= 0, by a primal active-set method."""
    n = sigma.shape[0]
    w = np.full(n, 1.0 / n)
    fixed = np.zeros(n, dtype=bool)  # working set: weights held at zero
    for _ in range(10 * n):
        free = ~fixed
        x = np.linalg.solve(sigma[np.ix_(free, free)], np.ones(free.sum()))
        target = np.zeros(n)
        target[free] = x / x.sum()
        step = target - w
        if np.abs(step).max() < tol:
            g = sigma @ w
            nu = g[free].mean()
            mult = g - nu  # KKT multipliers of the active bounds
            if not fixed.any() or mult[fixed].min() >= -tol:
                return w
            fixed[np.flatnonzero(fixed)[np.argmin(mult[fixed])]] = False
            continue
        neg = free & (step < -tol)
        ratios = np.full(n, np.inf)
        ratios[neg] = -w[neg] / step[neg]
        alpha = min(1.0, ratios.min())
        w = w + alpha * step
        if alpha < 1.0:
            j = int(np.argmin(ratios))
            fixed[j] = True
            w[j] = 0.0
    raise RuntimeError("active set did not converge")


def inverse_variance(sigma: np.ndarray) -> np.ndarray:
    iv = 1.0 / np.diag(sigma)
    return iv / iv.sum()


# ----------------------------------------------------------------------------
# Hierarchical risk parity (Lopez de Prado 2016)
# ----------------------------------------------------------------------------


def correlation_distance(corr: np.ndarray) -> np.ndarray:
    return np.sqrt(np.clip(0.5 * (1.0 - corr), 0.0, None))


def column_distance(d: np.ndarray) -> np.ndarray:
    """d_tilde_ij = Euclidean distance between columns i and j of the distance matrix."""
    diff = d[:, :, None] - d[:, None, :]
    return np.sqrt(np.sum(diff**2, axis=0))


def single_linkage(dist: np.ndarray) -> list[tuple[int, int, float]]:
    """Single-linkage clustering via its minimum spanning tree (Prim), merged in order of edge length.

    Returns merges (id_a, id_b, height) with scipy-style ids: leaves 0..n-1, the k-th merge creates id n+k.
    """
    n = dist.shape[0]
    in_tree = np.zeros(n, dtype=bool)
    in_tree[0] = True
    best = dist[0].copy()
    parent = np.zeros(n, dtype=int)
    edges = []
    for _ in range(n - 1):
        cand = np.where(in_tree, np.inf, best)
        j = int(np.argmin(cand))
        edges.append((float(cand[j]), int(parent[j]), j))
        in_tree[j] = True
        closer = dist[j] < best
        best = np.where(closer, dist[j], best)
        parent = np.where(closer, j, parent)
    edges.sort()
    root = list(range(n))  # union-find over leaves
    label = list(range(n))  # current cluster id of each union-find root

    def find(i: int) -> int:
        while root[i] != i:
            root[i] = root[root[i]]
            i = root[i]
        return i

    merges = []
    for h, a, b in edges:
        ra, rb = find(a), find(b)
        ida, idb = sorted((label[ra], label[rb]))
        merges.append((ida, idb, h))
        root[rb] = ra
        label[ra] = n + len(merges) - 1
    return merges


def single_linkage_brute(dist: np.ndarray) -> list[tuple[int, int, float]]:
    """Textbook O(n^3) agglomeration, used only to cross-check single_linkage."""
    n = dist.shape[0]
    clusters: dict[int, list[int]] = {i: [i] for i in range(n)}
    merges: list[tuple[int, int, float]] = []
    while len(clusters) > 1:
        ids = sorted(clusters)
        best = (np.inf, -1, -1)
        for ia, a in enumerate(ids):
            for b in ids[ia + 1 :]:
                h = dist[np.ix_(clusters[a], clusters[b])].min()
                if h < best[0]:
                    best = (h, a, b)
        h, a, b = best
        clusters[n + len(merges)] = clusters.pop(a) + clusters.pop(b)
        merges.append((a, b, float(h)))
    return merges


def quasi_diagonal_order(merges: list[tuple[int, int, float]], n: int) -> list[int]:
    """Leaves of the dendrogram in order: recursively replace each cluster by its two children."""
    children = {n + k: (a, b) for k, (a, b, _) in enumerate(merges)}

    def leaves(c: int) -> list[int]:
        if c < n:
            return [c]
        a, b = children[c]
        return leaves(a) + leaves(b)

    return leaves(n + len(merges) - 1)


def cluster_variance(sigma: np.ndarray, idx: list[int]) -> float:
    sub = sigma[np.ix_(idx, idx)]
    w = inverse_variance(sub)
    return float(w @ sub @ w)


def recursive_bisection(sigma: np.ndarray, order: list[int]) -> np.ndarray:
    w = np.ones(sigma.shape[0])
    stack = [order]
    while stack:
        items = stack.pop()
        if len(items) < 2:
            continue
        half = len(items) // 2
        left, right = items[:half], items[half:]
        v_l, v_r = cluster_variance(sigma, left), cluster_variance(sigma, right)
        alpha = 1.0 - v_l / (v_l + v_r)
        w[left] *= alpha
        w[right] *= 1.0 - alpha
        stack += [left, right]
    return w


def hrp_weights(sigma: np.ndarray) -> tuple[np.ndarray, list[int]]:
    sd = np.sqrt(np.diag(sigma))
    corr = sigma / np.outer(sd, sd)
    merges = single_linkage(column_distance(correlation_distance(corr)))
    order = quasi_diagonal_order(merges, sigma.shape[0])
    return recursive_bisection(sigma, order), order


# ----------------------------------------------------------------------------
# Examples
# ----------------------------------------------------------------------------


def four_asset_market() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    vol = np.array([0.16, 0.18, 0.06, 0.20])
    corr = np.array(
        [
            [1.0, 0.8, 0.1, 0.3],
            [0.8, 1.0, 0.1, 0.3],
            [0.1, 0.1, 1.0, 0.0],
            [0.3, 0.3, 0.0, 1.0],
        ]
    )
    w_mkt = np.array([0.4, 0.3, 0.2, 0.1])
    return corr * np.outer(vol, vol), w_mkt, vol


def section_black_litterman() -> None:
    print("== 1. Black-Litterman ==")
    sigma, w_mkt, _ = four_asset_market()
    delta, tau = 2.5, 0.05
    pi = delta * sigma @ w_mkt
    vec("implied excess returns Pi = delta Sigma w_mkt", pi, [0.04576, 0.05058, 0.00357, 0.02770], ".5f")
    for got, exp in zip(pi, [0.04576, 0.05058, 0.00357, 0.02770], strict=True):
        assert abs(got - exp) < 1e-5
    var_m = w_mkt @ sigma @ w_mkt
    check("market volatility", np.sqrt(var_m), 0.1216, 1e-4)
    check("market excess return delta*sigma_m^2", delta * var_m, 0.0370, 1e-4)
    check("implied market Sharpe delta*sigma_m", delta * np.sqrt(var_m), 0.3040, 1e-4)

    p = np.array([[1.0, -1.0, 0.0, 0.0]])
    q = np.array([0.02])
    omega = p @ (tau * sigma) @ p.T  # He-Litterman: view variance equals prior variance of the view portfolio
    check("prior view P Pi (A minus B)", (p @ pi)[0], -0.00482, 1e-8)
    check("view surprise Q - P Pi", (q - p @ pi)[0], 0.0248, 1e-4)
    mu_a, m_post = bl_posterior_precision_form(pi, sigma, tau, p, q, omega)
    mu_b = bl_posterior_update_form(pi, sigma, tau, p, q, omega)
    vec("posterior mean mu_BL", mu_b, [0.04843, 0.04084, 0.00345, 0.02645], ".5f")
    for got, exp in zip(mu_b, [0.048425, 0.040835, 0.003445, 0.026451], strict=True):
        assert abs(got - exp) < 1e-5
    check("max |precision form - update form|", np.max(np.abs(mu_a - mu_b)), 0.0, 1e-12, ".1e")
    check("posterior view P mu_BL", (p @ mu_b)[0], 0.0076, 1e-4)
    check("change in the view portfolio's expected return", (p @ mu_b)[0] - (p @ pi)[0], 0.0124, 1e-4)
    check("halfway between Q and P Pi", (q[0] + (p @ pi)[0]) / 2, 0.0076, 1e-4)

    w_bl = np.linalg.solve(delta * sigma, mu_b)
    vec("BL weights (delta Sigma)^-1 mu_BL", w_bl, [0.8164, -0.1164, 0.2000, 0.1000])
    tilt = (tau / delta) * p.T @ np.linalg.solve(p @ (tau * sigma) @ p.T + omega, q - p @ pi)
    check("max |w_BL - w_mkt - tilt along P'|", np.max(np.abs(w_bl - w_mkt - tilt)), 0.0, 1e-12, ".1e")
    check("BL weight change in A", w_bl[0] - w_mkt[0], 0.4164, 1e-4)
    check("BL weight change in C (not in the view)", w_bl[2] - w_mkt[2], 0.0, 1e-12)
    check("BL weight change in D (not in the view)", w_bl[3] - w_mkt[3], 0.0, 1e-12)

    # He-Litterman with predictive covariance Sigma + M: (1+tau) w - w_mkt lies along P'
    w_hl = np.linalg.solve(delta * (sigma + m_post), mu_b)
    resid = (1 + tau) * w_hl - w_mkt
    check("(1+tau) w_HL - w_mkt in asset C", resid[2], 0.0, 1e-12)
    check("(1+tau) w_HL - w_mkt in asset D", resid[3], 0.0, 1e-12)
    check("(1+tau) w_HL - w_mkt: A plus B", resid[0] + resid[1], 0.0, 1e-12)
    check("sum of He-Litterman weights", w_hl.sum(), 0.9524, 1e-4)

    # with Omega proportional to tau the posterior mean does not depend on tau
    mu_t2 = bl_posterior_update_form(pi, sigma, 0.5, p, q, p @ (0.5 * sigma) @ p.T)
    check("max |mu_BL(tau 0.5) - mu_BL(tau 0.05)| with Omega = P tau Sigma P'", np.max(np.abs(mu_t2 - mu_b)), 0.0, 1e-12, ".1e")
    # confidence: the posterior moves a fraction s/(s + omega) of the way from P Pi to Q
    s_view = (p @ (tau * sigma) @ p.T)[0, 0]
    for scale, frac in [(0.25, 0.8), (4.0, 0.2)]:
        mu_c = bl_posterior_update_form(pi, sigma, tau, p, q, scale * np.array([[s_view]]))
        moved = ((p @ mu_c)[0] - (p @ pi)[0]) / (q[0] - (p @ pi)[0])
        check(f"fraction moved toward the view, Omega = {scale} x prior view variance", moved, frac, 1e-12)

    # naive mean-variance with a one-point mean error versus BL
    mu_noisy = pi + np.array([0.01, -0.01, 0.0, 0.0])
    w_noisy = np.linalg.solve(delta * sigma, mu_noisy)
    vec("naive MV weights after +1%/-1% mean error on A/B", w_noisy, [1.1433, -0.3510, 0.1971, 0.0974])
    check("naive MV weight in A", w_noisy[0], 1.1433, 1e-4)
    check("naive MV weight in B", w_noisy[1], -0.3510, 1e-4)


def section_risk_parity() -> None:
    print("\n== 2. Equal risk contribution ==")
    s2 = np.array([[0.01, 0.5 * 0.1 * 0.2], [0.5 * 0.1 * 0.2, 0.04]])
    w2 = erc_weights(s2)
    check("two assets 10%/20% vol, rho 0.5: ERC weight 1", w2[0], 2 / 3, 1e-10)
    s2b = np.array([[0.01, -0.5 * 0.1 * 0.2], [-0.5 * 0.1 * 0.2, 0.04]])
    check("same with rho -0.5: ERC weight 1 (correlation irrelevant)", erc_weights(s2b)[0], 2 / 3, 1e-10)

    sigma, _, vol = four_asset_market()
    w = erc_weights(sigma)
    vec("ERC weights", w, [0.1494, 0.1328, 0.5681, 0.1496])
    rc = risk_contributions(w, sigma)
    check("max |risk share - 1/4|", np.max(np.abs(rc - 0.25)), 0.0, 1e-10, ".1e")
    for got, exp in zip(w, [0.1494, 0.1328, 0.5681, 0.1496], strict=True):
        assert abs(got - exp) < 1e-4
    iv = (1 / vol) / (1 / vol).sum()
    vec("inverse-volatility weights", iv, [0.1867, 0.1660, 0.4979, 0.1494])
    vec("inverse-volatility risk shares", risk_contributions(iv, sigma), [0.3056, 0.3056, 0.1667, 0.2222])
    vol_gmv = np.sqrt(gmv(sigma) @ sigma @ gmv(sigma))
    vol_erc = np.sqrt(w @ sigma @ w)
    ew = np.full(4, 0.25)
    vol_ew = np.sqrt(ew @ sigma @ ew)
    check("GMV volatility", vol_gmv, 0.0565, 1e-4)
    check("ERC volatility", vol_erc, 0.0728, 1e-4)
    check("1/N volatility", vol_ew, 0.1097, 1e-4)
    assert vol_gmv <= vol_erc <= vol_ew
    w_mkt = np.array([0.4, 0.3, 0.2, 0.1])
    vec("market-weight risk shares", risk_contributions(w_mkt, sigma), [0.4952, 0.4105, 0.0193, 0.0749])
    check("market weights: risk share of A plus B", risk_contributions(w_mkt, sigma)[:2].sum(), 0.9057, 1e-4)
    check("leverage to run ERC at 10% volatility", 0.10 / vol_erc, 1.3736, 1e-4)
    # risk budgeting: half the risk in bonds (asset C)
    b = np.array([1 / 6, 1 / 6, 1 / 2, 1 / 6])
    wb = erc_weights(sigma, b)
    check("risk budget check: max |share - budget|", np.max(np.abs(risk_contributions(wb, sigma) - b)), 0.0, 1e-10, ".1e")


def section_hrp() -> None:
    print("\n== 3. Hierarchical risk parity on the 4-asset market ==")
    sigma, _, vol = four_asset_market()
    corr = sigma / np.outer(vol, vol)
    d = correlation_distance(corr)
    check("d(A,B) = sqrt(0.5*(1-0.8))", d[0, 1], 0.316, 5e-4, ".3f")
    for rho_x, d_exp in [(1.0, 0.0), (0.0, 0.707), (-1.0, 1.0)]:
        d_x = correlation_distance(np.array([[1.0, rho_x], [rho_x, 1.0]]))[0, 1]
        check(f"correlation distance at rho = {rho_x}", d_x, d_exp, 5e-4, ".3f")
    dt = column_distance(d)
    merges = single_linkage(dt)
    for (a, b, h), expected_h in zip(merges, [0.4472, 0.8816, 1.0063], strict=True):
        check(f"merge {a} + {b} at height", h, expected_h, 1e-4)
    order = quasi_diagonal_order(merges, 4)
    print(f"quasi-diagonal order: {order}")
    assert order == [2, 3, 0, 1]
    rng = np.random.default_rng(5)
    x = rng.standard_normal((200, 30)) @ rng.standard_normal((30, 30))
    dt30 = column_distance(correlation_distance(np.corrcoef(x, rowvar=False)))
    fast, slow = single_linkage(dt30), single_linkage_brute(dt30)
    check(
        "single linkage MST versus brute force, 30 assets: max height gap",
        max(abs(f[2] - g[2]) for f, g in zip(fast, slow, strict=True)),
        0.0,
        1e-12,
        ".1e",
    )
    assert [f[:2] for f in fast] == [g[:2] for g in slow]
    w, _ = hrp_weights(sigma)
    vec("HRP weights", w, [0.0637, 0.0503, 0.8128, 0.0732])
    check("HRP weights sum", w.sum(), 1.0, 1e-12)
    vec("HRP risk shares", risk_contributions(w, sigma), [0.0829, 0.0731, 0.7531, 0.0909])
    check("HRP volatility", np.sqrt(w @ sigma @ w), 0.0573, 1e-4)
    # first bisection by hand: left [C, D], right [A, B] in the quasi-diagonal order
    v_l = cluster_variance(sigma, order[:2])
    v_r = cluster_variance(sigma, order[2:])
    check("IVP variance of left cluster [C, D]", v_l, 0.003303, 1e-6, ".6f")
    check("IVP variance of right cluster [A, B]", v_r, 0.025662, 1e-6, ".6f")
    check("first split alpha = 1 - V_left/(V_left+V_right)", 1 - v_l / (v_l + v_r), 0.8860, 1e-4)
    check("split inside [C, D]: share of C", 1 - sigma[2, 2] / (sigma[2, 2] + sigma[3, 3]), 0.9174, 1e-4)
    check("split inside [A, B]: share of A", 1 - sigma[0, 0] / (sigma[0, 0] + sigma[1, 1]), 0.5586, 1e-4)
    w_g = gmv(sigma)
    vec("GMV weights for comparison", w_g, [0.0687, -0.0005, 0.8683, 0.0634])
    vec("GMV risk shares", risk_contributions(w_g, sigma), [0.0687, -0.0005, 0.8683, 0.0634])


def block_market(n: int, n_blocks: int, rng: np.random.Generator) -> np.ndarray:
    block = np.arange(n) % n_blocks
    corr = np.where(block[:, None] == block[None, :], 0.6, 0.1)
    np.fill_diagonal(corr, 1.0)
    vol = rng.uniform(0.10, 0.40, n)
    return corr * np.outer(vol, vol)


def section_monte_carlo() -> None:
    print("\n== 4. Out-of-sample comparison, block-correlated market ==")
    rng = np.random.default_rng(42)
    n, reps = 50, 100
    sigma = block_market(n, 5, rng)
    chol = np.linalg.cholesky(sigma)
    w_star = gmv(sigma)
    v_star = w_star @ sigma @ w_star
    w_lo = gmv_long_only(sigma)
    grad = 2 * sigma @ w_lo
    check("long-only oracle KKT: max gradient gap on the support", np.ptp(grad[w_lo > 1e-8]), 0.0, 1e-8, ".1e")
    assert np.all(grad[w_lo <= 1e-8] >= grad[w_lo > 1e-8].min() - 1e-8)
    check("oracle GMV: number of short positions", float((w_star < 0).sum()), 27.0, 0.0, ".0f")
    check("long-only oracle variance / unconstrained optimum", (w_lo @ sigma @ w_lo) / v_star, 1.96, 0.01, ".2f")
    ew = np.full(n, 1.0 / n)
    check("1/N true variance / optimum", (ew @ sigma @ ew) / v_star, 6.20, 0.01, ".2f")
    iv = inverse_variance(sigma)
    check("true IVP variance / optimum", (iv @ sigma @ iv) / v_star, 3.67, 0.01, ".2f")
    methods = {
        "gmv": gmv,
        "gmv_long_only": gmv_long_only,
        "ivp": inverse_variance,
        "erc": erc_weights,
        "hrp": lambda s: hrp_weights(s)[0],
    }
    expected = {
        60: {"gmv": 6.28, "gmv_long_only": 2.40, "ivp": 3.71, "erc": 4.88, "hrp": 3.73},
        120: {"gmv": 1.70, "gmv_long_only": 2.15, "ivp": 3.69, "erc": 4.84, "hrp": 3.71},
        520: {"gmv": 1.11, "gmv_long_only": 2.00, "ivp": 3.67, "erc": 4.82, "hrp": 3.67},
    }
    expected_l1 = {
        60: {"gmv": 5.62, "gmv_long_only": 0.97, "ivp": 0.20, "erc": 0.26, "hrp": 0.43},
        120: {"gmv": 2.11, "gmv_long_only": 0.71, "ivp": 0.14, "erc": 0.17, "hrp": 0.39},
        520: {"gmv": 0.81, "gmv_long_only": 0.31, "ivp": 0.06, "erc": 0.08, "hrp": 0.33},
    }
    for t, exp in expected.items():
        var = {k: 0.0 for k in methods}
        l1 = {k: 0.0 for k in methods}
        for _ in range(reps):
            ws = []
            for _ in range(2):  # two independent estimation windows give a turnover proxy
                x = rng.standard_normal((t, n)) @ chol.T
                s = np.cov(x, rowvar=False)
                ws.append({k: f(s) for k, f in methods.items()})
            for k in methods:
                w = ws[0][k]
                var[k] += (w @ sigma @ w) / v_star / reps
                l1[k] += np.abs(ws[0][k] - ws[1][k]).sum() / reps
        for k in methods:
            check(f"T={t} {k}: true variance / optimum", var[k], exp[k], 0.02 * exp[k], ".2f")
        for k in methods:
            check(f"T={t} {k}: L1 weight change between windows", l1[k], expected_l1[t][k], 0.02 * max(expected_l1[t][k], 0.5), ".2f")
    # N > T: sample covariance is singular, GMV is undefined, HRP still runs
    x = rng.standard_normal((40, n)) @ chol.T
    s = np.cov(x, rowvar=False)
    check("rank of S with T = 40, N = 50", float(np.linalg.matrix_rank(s)), 39.0, 0.0, ".0f")
    w_h, _ = hrp_weights(s)
    check("HRP with singular S: true variance / optimum", (w_h @ sigma @ w_h) / v_star, 3.57, 0.05, ".2f")


def main() -> None:
    section_black_litterman()
    section_risk_parity()
    section_hrp()
    section_monte_carlo()


if __name__ == "__main__":
    main()
