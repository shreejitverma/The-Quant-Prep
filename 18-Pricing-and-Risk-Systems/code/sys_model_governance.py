"""Model governance: an illustrative tiering scheme, a challenger-model validation and the 2012 CIO VaR model error.

Backs every number in `18-Pricing-and-Risk-Systems/15-Model-Governance.md`.

1. An illustrative firm tiering scheme (weights and thresholds are a hypothetical firm policy, not a regulatory rule):
   the worked score, and the share of all 625 score combinations that land in each tier, by enumeration.
2. Challenger benchmarking of a Bermudan put (monthly exercise, Black-Scholes dynamics):
   - challenger: Cox-Ross-Rubinstein binomial tree, itself validated on the European put against Black-Scholes and
     checked for convergence by doubling the steps;
   - candidate: Longstaff-Schwartz Monte Carlo, with exercise rules fitted on one path set and priced on an independent
     set (seeds fixed), compared with the tree in units of its standard error;
   - a candidate with a planted bug (no discounting between exercise dates), which the comparison must flag.
3. The 2012 JPMorgan CIO VaR model: the published VaR figures (Senate PSI report) and the sum-versus-average error
   described in the JPMorgan Task Force report, reproduced on a hypothetical hazard-rate history.

Every quoted number is printed as ``label = value`` and asserted to within half a unit of its last quoted decimal.
Run it with `python 18-Pricing-and-Risk-Systems/code/sys_model_governance.py`.
"""

from __future__ import annotations

import itertools
import math
from statistics import NormalDist

import numpy as np

QUOTED: list[str] = []


def quoted(label: str, value: float, expected: float, decimals: int) -> float:
    """Print a number the note quotes and assert it rounds to the quoted figure (half a unit in the last place)."""
    tol = 0.5 * 10.0**-decimals + 1e-9
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    QUOTED.append(label)
    print(f"    {label} = {value:,.{decimals}f}")
    return value


# ============================================================================
# 1. Illustrative tiering
# ============================================================================

WEIGHTS = (0.35, 0.25, 0.25, 0.15)  # exposure, complexity, purpose (regulatory or risk use), client impact
WEIGHTS_PCT = (35, 25, 25, 15)  # the same weights in integer percent, so tier boundaries are exact


def tier(scores: tuple[int, ...]) -> int:
    """Tier 1 if the weighted score >= 3.75, Tier 2 if >= 2.50, else Tier 3 (computed in integer hundredths)."""
    hundredths = sum(w * s for w, s in zip(WEIGHTS_PCT, scores, strict=True))
    if hundredths >= 375:
        return 1
    if hundredths >= 250:
        return 2
    return 3


def test_tiering() -> None:
    print("  1. Illustrative tiering scheme (hypothetical firm policy)")
    scores = (5, 4, 5, 4)
    parts = [w * s for w, s in zip(WEIGHTS, scores, strict=True)]
    for name, part, exp in zip(("exposure", "complexity", "purpose", "client"), parts, (1.75, 1.00, 1.25, 0.60), strict=True):
        quoted(f"weighted {name} score", part, exp, 2)
    total = sum(parts)
    quoted("composite score", total, 4.60, 2)
    assert tier(scores) == 1
    # Sensitivity: the purpose score dropping from 5 to 3 still leaves Tier 1.
    quoted("composite score with purpose 3", total - 2 * WEIGHTS[2], 4.10, 2)
    # Enumerate every combination of 1-5 scores (5^4 = 625).
    counts = {1: 0, 2: 0, 3: 0}
    for combo in itertools.product(range(1, 6), repeat=4):
        counts[tier(combo)] += 1
    assert sum(counts.values()) == 625
    quoted("combinations in Tier 1 (%)", 100.0 * counts[1] / 625, 17.1, 1)
    quoted("combinations in Tier 2 (%)", 100.0 * counts[2] / 625, 57.9, 1)
    quoted("combinations in Tier 3 (%)", 100.0 * counts[3] / 625, 25.0, 1)


# ============================================================================
# 2. Challenger benchmarking of a Bermudan put
# ============================================================================

S0, K, R, SIG, T, M = 100.0, 100.0, 0.05, 0.20, 1.0, 12  # monthly exercise; hypothetical contract and market


def bs_put() -> float:
    n = NormalDist()
    d1 = (math.log(S0 / K) + (R + 0.5 * SIG * SIG) * T) / (SIG * math.sqrt(T))
    d2 = d1 - SIG * math.sqrt(T)
    return K * math.exp(-R * T) * n.cdf(-d2) - S0 * n.cdf(-d1)


def crr_put(steps: int, bermudan: bool) -> float:
    """CRR binomial tree; with bermudan=True exercise is allowed at the 12 monthly dates (not at time 0)."""
    dt = T / steps
    u = math.exp(SIG * math.sqrt(dt))
    d = 1.0 / u
    p = (math.exp(R * dt) - d) / (u - d)
    disc = math.exp(-R * dt)
    j = np.arange(steps + 1)
    v = np.maximum(K - S0 * u ** (steps - j) * d**j, 0.0)
    every = steps // M
    for i in range(steps - 1, -1, -1):
        v = disc * (p * v[:-1] + (1.0 - p) * v[1:])
        if bermudan and i > 0 and i % every == 0:
            k = np.arange(i + 1)
            v = np.maximum(v, K - S0 * u ** (i - k) * d**k)
    return float(v[0])


def gbm_paths(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    dt = T / M
    z = rng.standard_normal((n, M))
    return S0 * np.exp(np.cumsum((R - 0.5 * SIG * SIG) * dt + SIG * math.sqrt(dt) * z, axis=1))


def basis(s: np.ndarray) -> np.ndarray:
    x = s / K
    return np.column_stack([np.ones_like(x), x, x * x, x**3])


def lsm_put(n_fit: int, n_price: int, seed: int, discount_bug: bool = False) -> tuple[float, float]:
    """Longstaff-Schwartz: fit exercise rules on one path set, price on an independent set; returns (price, std error)."""
    dt = T / M
    step_df = 1.0 if discount_bug else math.exp(-R * dt)
    s = gbm_paths(n_fit, seed)
    cf = np.maximum(K - s[:, -1], 0.0)
    betas: list[np.ndarray | None] = [None] * M
    for t in range(M - 2, -1, -1):
        cf = cf * step_df  # value at date t of the cash flow realised later
        ex = np.maximum(K - s[:, t], 0.0)
        itm = ex > 0.0
        b, *_ = np.linalg.lstsq(basis(s[itm, t]), cf[itm], rcond=None)
        betas[t] = b
        hit = np.where(itm)[0][ex[itm] > basis(s[itm, t]) @ b]
        cf[hit] = ex[hit]
    s2 = gbm_paths(n_price, seed + 1)
    pv = np.zeros(n_price)
    alive = np.ones(n_price, dtype=bool)
    for t in range(M - 1):
        ex = np.maximum(K - s2[:, t], 0.0)
        cand = alive & (ex > 0.0)
        beta = betas[t]
        assert beta is not None
        hit = np.where(cand)[0][ex[cand] > basis(s2[cand, t]) @ beta]
        pv[hit] = ex[hit] * step_df ** (t + 1)
        alive[hit] = False
    pv[alive] = np.maximum(K - s2[alive, -1], 0.0) * step_df**M
    return float(np.mean(pv)), float(np.std(pv) / math.sqrt(n_price))


def test_challenger() -> None:
    print("  2. Bermudan put: tree challenger versus Longstaff-Schwartz candidate (S0 = K = 100, r 5%, vol 20%, 1y, monthly)")
    bs = bs_put()
    tree_eu = crr_put(1200, bermudan=False)
    quoted("European put, Black-Scholes", bs, 5.574, 3)
    quoted("European put, CRR tree 1,200 steps", tree_eu, 5.572, 3)
    assert abs(tree_eu - bs) < 0.005  # the challenger reproduces a closed form before it is trusted
    t1200 = crr_put(1200, bermudan=True)
    t2400 = crr_put(2400, bermudan=True)
    quoted("Bermudan put, tree 1,200 steps", t1200, 6.042, 3)
    quoted("Bermudan put, tree 2,400 steps", t2400, 6.042, 3)
    quoted("tree change on doubling steps", abs(t2400 - t1200), 0.0001, 4)
    price, se = lsm_put(100_000, 100_000, 2026)
    quoted("Bermudan put, LSM out-of-sample (100,000 + 100,000 paths)", price, 6.038, 3)
    quoted("LSM standard error", se, 0.023, 3)
    z = (price - t2400) / se
    quoted("difference in standard errors", z, -0.2, 1)
    assert abs(z) < 3.0
    bug_price, bug_se = lsm_put(100_000, 100_000, 2026, discount_bug=True)
    z_bug = (bug_price - t2400) / bug_se
    quoted("buggy candidate (no discounting between dates)", bug_price, 6.220, 3)
    quoted("buggy candidate difference in standard errors", z_bug, 7.3, 1)
    assert z_bug > 3.0  # the challenger flags the planted bug


# ============================================================================
# 3. 2012 CIO VaR model
# ============================================================================


def test_cio_var() -> None:
    print("  3. JPMorgan CIO 2012: published figures and the sum-versus-average error")
    old_var, new_var = 132.0, 66.0  # $ million, Senate PSI report p. 177 (January 27 2012)
    quoted("VaR reduction from the model change (%)", 100.0 * (1.0 - new_var / old_var), 50.0, 1)
    # Relative change of a hazard rate: intended (b - a) / ((a + b) / 2), implemented (b - a) / (a + b).
    a, b = 0.0200, 0.0220  # hypothetical hazard rates on consecutive days
    quoted("rate change b - a", b - a, 0.002, 3)
    quoted("average (a + b) / 2", (a + b) / 2.0, 0.021, 3)
    quoted("sum a + b", a + b, 0.042, 3)
    intended = (b - a) / ((a + b) / 2.0)
    buggy = (b - a) / (a + b)
    quoted("intended relative change", intended, 0.0952, 4)
    quoted("implemented relative change", buggy, 0.0476, 4)
    quoted("ratio implemented / intended", buggy / intended, 0.5, 2)
    # Historical-simulation VaR of a linear position on a hypothetical hazard-rate history.
    rng = np.random.default_rng(12)
    h = 0.02 * np.exp(np.cumsum(0.03 * rng.standard_normal(265)))
    good = (h[1:] - h[:-1]) / ((h[1:] + h[:-1]) / 2.0)
    bad = (h[1:] - h[:-1]) / (h[1:] + h[:-1])
    exposure = 1e9  # dollar P&L per unit relative change (hypothetical)

    def var99(changes: np.ndarray) -> float:
        return float(-np.quantile(exposure * changes, 0.01))

    quoted("VaR with the error / VaR without", var99(bad) / var99(good), 0.5, 2)
    # Published loss and penalty figures (cited inputs, summed here).
    quoted("penalties: SEC, Fed, OCC and FCA (Sept 2013) plus CFTC (Oct 2013), $ million", 920.0 + 100.0, 1020.0, 0)


def main() -> None:
    print("Model governance checks")
    test_tiering()
    test_challenger()
    test_cio_var()
    print(f"  {len(QUOTED)} numbers computed, printed and asserted")
    print("All model governance checks passed.")


if __name__ == "__main__":
    main()
