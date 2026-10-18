"""Reinforcement learning for execution and market making: Bellman equations, dynamic programming and tabular Q-learning.

Backs 10-Machine-Learning-for-Finance/08-Reinforcement-Learning-for-Trading.md.

Execution MDP: sell X shares over N periods. State (k, x) = (period, shares left); action n = shares sold now.
Cost of a step: eta * n^2 (temporary impact) + lam * (x' * dP)^2 with dP ~ N(0, sigma^2) and x' = x - n, whose expectation
lam * sigma^2 * x'^2 is the Almgren-Chriss variance penalty; reward = -cost. Shares are integers.

1. Two-period Bellman recursion by hand.
2. Exact DP for X = 10, N = 5 against TWAP, immediate sale and the continuous Almgren-Chriss schedule
   x_k = X sinh(kappa (N - k)) / sinh(kappa N) with cosh(kappa) = 1 + lam sigma^2 / (2 eta).
3. Tabular Q-learning and double Q-learning from simulated episodes, against the DP optimum.
4. Maximisation bias: E[max of 10 iid N(0, 1)].
5. Simulator gap: the policy that is optimal for impact eta = 1, run in a market with eta = 2.
6. A market-making MDP solved by value iteration: optimal quote offsets skew against inventory.

Run: uv run --no-project --with numpy python 10-Machine-Learning-for-Finance/code/rl_execution_q_learning.py
"""

from __future__ import annotations

import itertools
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


ETA, LAM_SIG2 = 1.0, 0.5  # impact coefficient and lam * sigma^2 (sigma = 1, lam = 0.5)


def step_cost(n: int, x_after: int, eta: float = ETA) -> float:
    return eta * n * n + LAM_SIG2 * x_after * x_after


def solve_dp(total: int, periods: int, eta: float = ETA) -> tuple[np.ndarray, np.ndarray]:
    """V[k, x] = minimal expected cost from period k with x shares left; policy[k, x] = optimal sale."""
    v = np.zeros((periods + 1, total + 1))
    v[periods, 1:] = np.inf  # must be done by the end
    pol = np.zeros((periods, total + 1), dtype=int)
    for k in range(periods - 1, -1, -1):
        for x in range(total + 1):
            costs = [step_cost(n, x - n, eta) + v[k + 1, x - n] for n in range(x + 1)]
            pol[k, x] = int(np.argmin(costs))
            v[k, x] = costs[pol[k, x]]
    return v, pol


def schedule_cost(trades: list[float], total: float, eta: float = ETA) -> float:
    x, cost = total, 0.0
    for n in trades:
        x -= n
        cost += eta * n * n + LAM_SIG2 * x * x
    return cost


def greedy_path(pol: np.ndarray, total: int) -> list[int]:
    x, path = total, []
    for k in range(pol.shape[0]):
        n = int(pol[k, x])
        path.append(n)
        x -= n
    return path


def section_bellman_by_hand() -> None:
    # Backs: Worked example 1; card ml-rl-two-period.
    print("\n== 1. Two-period Bellman recursion ==")
    for n1, exp in [(0, 6.0), (1, 2.5), (2, 4.0)]:
        check(f"two periods, X = 2: cost of selling {n1} first", step_cost(n1, 2 - n1) + step_cost(2 - n1, 0), exp, 1e-12, ".2f")
    v, pol = solve_dp(2, 2)
    check("two periods, X = 2: DP optimal first sale", pol[0, 2], 1, 0, ".0f")
    check("two periods, X = 2: DP optimal cost", v[0, 2], 2.50, 1e-12, ".2f")


def section_execution_dp() -> None:
    # Backs: Worked example 2; cards ml-rl-ac-kappa, ml-rl-twap-vs-optimal.
    print("\n== 2. Exact DP, X = 10 shares, N = 5 periods ==")
    total, periods = 10, 5
    v, pol = solve_dp(total, periods)
    path = greedy_path(pol, total)
    print(f"DP schedule = {path}")
    check("DP schedule equals [5, 3, 1, 1, 0] (1 = yes)", float(path == [5, 3, 1, 1, 0]), 1, 0, ".0f")
    check("DP optimal expected cost", v[0, total], 51.00, 1e-9, ".2f")
    # Independent of the recursion: enumerate every integer schedule that sells all 10 shares in 5 periods.
    schedules = [t for t in itertools.product(range(total + 1), repeat=periods) if sum(t) == total]
    check("number of integer schedules enumerated (C(14, 4))", len(schedules), 1001, 0, ".0f")
    brute_cost, brute_best = min((schedule_cost(list(t), total), t) for t in schedules)
    check("brute-force optimum is (5, 3, 1, 1, 0) (1 = yes)", float(brute_best == (5, 3, 1, 1, 0)), 1, 0, ".0f")
    check("brute-force optimal expected cost", brute_cost, 51.00, 1e-9, ".2f")
    check("TWAP (2 per period) expected cost", schedule_cost([2] * 5, total), 80.00, 1e-9, ".2f")
    check("TWAP cost / DP cost - 1 (%)", 100 * (schedule_cost([2] * 5, total) / v[0, total] - 1), 56.9, 0.05, ".1f")
    for name, trades_k, exp_imp, exp_risk in [("TWAP", [2] * 5, 20.0, 60.0), ("DP", path, 36.0, 15.0)]:
        left = total - np.cumsum(trades_k)
        check(f"{name} impact part of the cost", float(ETA * np.sum(np.square(trades_k))), exp_imp, 1e-9, ".2f")
        check(f"{name} risk part of the cost", float(LAM_SIG2 * np.sum(np.square(left))), exp_risk, 1e-9, ".2f")
    check("immediate sale expected cost", schedule_cost([10, 0, 0, 0, 0], total), 100.00, 1e-9, ".2f")
    # The continuous optimum solves the tridiagonal first-order conditions x_{k-1} - 2 x_k + x_{k+1} = (lam sigma^2/eta) x_k
    # with x_0 = X and x_N = 0; solve them directly, independently of the sinh closed form.
    a = np.diag(np.full(periods - 1, 2 + LAM_SIG2 / ETA)) - np.diag(np.ones(periods - 2), 1) - np.diag(np.ones(periods - 2), -1)
    rhs = np.zeros(periods - 1)
    rhs[0] = total
    x_lin = np.concatenate(([float(total)], np.linalg.solve(a, rhs), [0.0]))
    check("cosh kappa = 1 + lam sigma^2 / (2 eta)", 1 + LAM_SIG2 / (2 * ETA), 1.25, 1e-12, ".2f")
    kappa = math.acosh(1 + LAM_SIG2 / (2 * ETA))
    check("Almgren-Chriss kappa = acosh(1.25)", kappa, 0.6931, 5e-5, ".4f")
    # acosh(c) = ln(c + sqrt(c^2 - 1)) = ln(1.25 + 0.75) = ln 2: compare with the logarithm, a different function.
    check_below("|acosh(1.25) - ln 2|", abs(kappa - math.log(2)), 1e-12)
    xs = [total * math.sinh(kappa * (periods - k)) / math.sinh(kappa * periods) for k in range(periods + 1)]
    trades = [xs[k] - xs[k + 1] for k in range(periods)]
    exp_trades = [5.015, 2.522, 1.290, 0.704, 0.469]
    for k in range(periods):
        check(f"Almgren-Chriss continuous trade in period {k + 1}", trades[k], exp_trades[k], 5e-4, ".3f")
    ac_cost = schedule_cost(trades, total)
    check("Almgren-Chriss continuous schedule expected cost", ac_cost, 50.15, 5e-3, ".2f")
    check_below("closed form vs tridiagonal solve, max |x_k difference|", float(np.abs(x_lin - np.array(xs)).max()), 1e-12)
    check("integer DP cost above continuous optimum (%)", 100 * (v[0, total] / ac_cost - 1), 1.7, 0.05, ".1f")


# ---------------------------------------------------------------------------
# 3. Q-learning and double Q-learning
# ---------------------------------------------------------------------------


def run_q_learning(total: int, periods: int, episodes: int, eps: float, seed: int, double: bool) -> tuple[list, list]:
    rng = np.random.default_rng(seed)
    explore = rng.random((episodes, periods)).tolist()
    pick = rng.random((episodes, periods)).tolist()
    noise = rng.standard_normal((episodes, periods)).tolist()
    coin = rng.random((episodes, periods)).tolist()
    qa = [[[0.0] * (x + 1) for x in range(total + 1)] for _ in range(periods)]
    qb = [[[0.0] * (x + 1) for x in range(total + 1)] for _ in range(periods)]
    na = [[[0] * (x + 1) for x in range(total + 1)] for _ in range(periods)]
    nb = [[[0] * (x + 1) for x in range(total + 1)] for _ in range(periods)]
    for e in range(episodes):
        x = total
        for k in range(periods):
            if k == periods - 1:
                n = x
            elif explore[e][k] < eps:
                n = int(pick[e][k] * (x + 1))
            else:
                row = [a + b for a, b in zip(qa[k][x], qb[k][x], strict=True)] if double else qa[k][x]
                n = row.index(max(row))
            x_next = x - n
            reward = -(ETA * n * n + LAM_SIG2 * (x_next * noise[e][k]) ** 2)
            update_a = (not double) or coin[e][k] < 0.5
            q, q_other, cnt = (qa, qb, na) if update_a else (qb, qa, nb)
            if k + 1 == periods:
                future = 0.0
            elif k + 1 == periods - 1:  # the last period has one legal action: sell everything left
                future = q_other[k + 1][x_next][x_next] if double else q[k + 1][x_next][x_next]
            else:
                nxt = q[k + 1][x_next]
                if double:
                    future = q_other[k + 1][x_next][nxt.index(max(nxt))]
                else:
                    future = max(nxt)
            cnt[k][x][n] += 1
            q[k][x][n] += (reward + future - q[k][x][n]) / cnt[k][x][n]
            x = x_next
    return qa, qb


def section_q_learning() -> None:
    # Backs: Worked example 3; card ml-rl-model-vs-rl.
    print("\n== 3. Tabular Q-learning ==")
    total, periods = 10, 5
    v, pol = solve_dp(total, periods)
    for double, tag, exp_bias in [(False, "Q-learning", 0.08), (True, "double Q-learning", 0.05)]:
        qa, qb = run_q_learning(total, periods, episodes=200_000, eps=0.2, seed=5, double=double)
        q = [[[a + b for a, b in zip(ra, rb, strict=True)] for ra, rb in zip(ka, kb, strict=True)] for ka, kb in zip(qa, qb, strict=True)]
        if double:
            q = [[[0.5 * val for val in row] for row in kq] for kq in q]
        x, path = total, []
        for k in range(periods):
            row = q[k][x]
            n = x if k == periods - 1 else row.index(max(row))
            path.append(n)
            x -= n
        print(f"{tag} greedy schedule = {path}")
        check(f"{tag}: greedy schedule matches DP (1 = yes)", float(path == greedy_path(pol, total)), 1.0, 0, ".0f")
        v_hat = max(q[0][total])
        check(f"{tag}: learned value of the start state minus true value (-V*)", v_hat - (-v[0, total]), exp_bias, 5e-3, ".2f")


# ---------------------------------------------------------------------------
# 4. Maximisation bias
# ---------------------------------------------------------------------------


def section_max_bias() -> None:
    # Backs: Worked example 4; cards ml-rl-max-bias, ml-rl-double-q.
    print("\n== 4. Maximisation bias ==")
    grid = np.linspace(-10, 10, 400_001)
    phi = np.exp(-0.5 * grid**2) / math.sqrt(2 * math.pi)
    cdf = 0.5 * (1 + np.vectorize(math.erf)(grid / math.sqrt(2)))
    dens = 10 * phi * cdf**9
    check("E[max of 10 iid N(0,1)] by quadrature", float(np.trapezoid(grid * dens, grid)), 1.5388, 5e-5)
    rng = np.random.default_rng(6)
    check("E[max of 10 iid N(0,1)] simulated, 200k draws", float(rng.standard_normal((200_000, 10)).max(axis=1).mean()), 1.538, 5e-4, ".3f")

    # Sutton and Barto (2nd ed.) Example 6.7: from A, "right" ends with reward 0; "left" goes to B with reward 0, where
    # each of 10 actions ends with reward N(-0.1, 1). Going left is a mistake, but max over noisy B-values looks positive.
    runs, episodes, eps, alpha = 2000, 300, 0.1, 0.1
    for double, tag, exp in [(False, "Q-learning", 0.378), (True, "double Q-learning", 0.117)]:
        r = np.random.default_rng(7)
        qa = np.zeros((2, runs, 2))  # [table, run, action at A]: 0 = left, 1 = right
        qb = np.zeros((2, runs, 10))
        left_count = np.zeros(episodes)
        idx = np.arange(runs)
        for e in range(episodes):
            tot_a = qa[0] + qa[1] if double else qa[0]
            greedy = np.where(tot_a[:, 0] == tot_a[:, 1], r.integers(0, 2, runs), np.argmax(tot_a, axis=1))
            act = np.where(r.random(runs) < eps, r.integers(0, 2, runs), greedy)
            left = act == 0
            left_count[e] = left.mean()
            tot_b = qb[0] + qb[1] if double else qb[0]
            noise_tb = tot_b + 1e-9 * r.random((runs, 10))  # random tie-break
            b_greedy = np.argmax(noise_tb, axis=1)
            b_act = np.where(r.random(runs) < eps, r.integers(0, 10, runs), b_greedy)
            reward_b = -0.1 + r.standard_normal(runs)
            which = (r.random(runs) < 0.5).astype(int) if double else np.zeros(runs, dtype=int)
            other = 1 - which
            # Update at A (reward 0 for both actions).
            if double:
                best_b = np.argmax(qb[which, idx], axis=1)
                future = np.where(left, qb[other, idx, best_b], 0.0)
            else:
                future = np.where(left, qb[0].max(axis=1), 0.0)
            qa[which, idx, act] += alpha * (future - qa[which, idx, act])
            # Update at B for runs that went left (terminal next state).
            sel = idx[left]
            qb[which[sel], sel, b_act[sel]] += alpha * (reward_b[sel] - qb[which[sel], sel, b_act[sel]])
        check(f"{tag}: share of left actions from A, episodes 1-300 (optimal 0.05)", float(left_count.mean()), exp, 5e-4, ".3f")


# ---------------------------------------------------------------------------
# 5. Simulator gap
# ---------------------------------------------------------------------------


def evaluate_policy(pol: np.ndarray, total: int, eta: float) -> float:
    x, cost = total, 0.0
    for k in range(pol.shape[0]):
        n = int(pol[k, x])
        x -= n
        cost += step_cost(n, x, eta)
    return cost


def section_sim_gap() -> None:
    # Backs: Worked example 5; card ml-rl-sim-gap.
    print("\n== 5. Simulator gap ==")
    total, periods = 10, 5
    _, pol_sim = solve_dp(total, periods, eta=1.0)
    v_true, pol_true = solve_dp(total, periods, eta=2.0)
    print(f"optimal schedule when eta = 2: {greedy_path(pol_true, total)}")
    cost_sim_policy = evaluate_policy(pol_sim, total, eta=2.0)
    check("true-market (eta 2) cost of the eta-1 policy", cost_sim_policy, 87.00, 1e-9, ".2f")
    check("true-market (eta 2) optimal cost", v_true[0, total], 80.50, 1e-9, ".2f")
    schedules = [t for t in itertools.product(range(total + 1), repeat=periods) if sum(t) == total]
    brute_cost, brute_best = min((schedule_cost(list(t), total, eta=2.0), t) for t in schedules)
    check("eta 2 brute-force optimum is (4, 2, 2, 1, 1) (1 = yes)", float(brute_best == (4, 2, 2, 1, 1)), 1, 0, ".0f")
    check("eta 2 brute-force optimal expected cost", brute_cost, 80.50, 1e-9, ".2f")
    check("eta 2 cost of (5, 3, 1, 1, 0) by direct summation", schedule_cost([5, 3, 1, 1, 0], total, eta=2.0), 87.00, 1e-9, ".2f")
    check("excess cost from the simulator gap (%)", 100 * (cost_sim_policy / v_true[0, total] - 1), 8.1, 0.05, ".1f")


# ---------------------------------------------------------------------------
# 6. Market-making MDP
# ---------------------------------------------------------------------------


def section_market_making() -> None:
    # Backs: Worked example 6; card ml-rl-mm-mdp.
    print("\n== 6. Market-making MDP by value iteration ==")
    q_max, gamma, phi = 3, 0.99, 0.1
    offsets = [0.5, 1.0, 1.5]
    fill = [math.exp(-d) for d in offsets]  # fill probability A exp(-k delta) with A = k = 1
    inv = list(range(-q_max, q_max + 1))
    v = np.zeros(len(inv))
    for _ in range(5000):
        new = np.empty_like(v)
        best_act = []
        for i, q in enumerate(inv):
            best, arg = -math.inf, None
            for ib, db in enumerate(offsets):
                for ia, da in enumerate(offsets):
                    pb = fill[ib] if q < q_max else 0.0  # cannot buy at the long limit
                    pa = fill[ia] if q > -q_max else 0.0  # cannot sell at the short limit
                    val = 0.0
                    for buy, pbuy in ((1, pb), (0, 1 - pb)):
                        for sell, psell in ((1, pa), (0, 1 - pa)):
                            prob = pbuy * psell
                            if prob == 0.0:
                                continue
                            q2 = q + buy - sell
                            reward = db * buy + da * sell - phi * q2 * q2
                            val += prob * (reward + gamma * v[q2 + q_max])
                    if val > best + 1e-12:
                        best, arg = val, (db, da)
            new[i] = best
            best_act.append(arg)
        diff = float(np.abs(new - v).max())
        v = new
        if diff < 1e-12:
            break
    check_below("value iteration converged, final sup-norm change", diff, 1e-11)
    # At the limits one side is not quoted (its offset is irrelevant), so report the posted side only.
    bids = {q: a[0] for q, a in zip(inv, best_act, strict=True) if q < q_max}
    asks = {q: a[1] for q, a in zip(inv, best_act, strict=True) if q > -q_max}
    exp_bid = {-3: 0.5, -2: 0.5, -1: 0.5, 0: 1.0, 1: 1.5, 2: 1.5}
    exp_ask = {-2: 1.5, -1: 1.5, 0: 1.0, 1: 0.5, 2: 0.5, 3: 0.5}
    for q in bids:
        check(f"optimal bid offset at inventory {q:+d}", bids[q], exp_bid[q], 1e-12, ".1f")
    for q in asks:
        check(f"optimal ask offset at inventory {q:+d}", asks[q], exp_ask[q], 1e-12, ".1f")
    qs = sorted(bids)
    assert all(bids[a] <= bids[b] for a, b in zip(qs, qs[1:], strict=False)), "bid offset should widen as inventory grows"
    qs = sorted(asks)
    assert all(asks[a] >= asks[b] for a, b in zip(qs, qs[1:], strict=False)), "ask offset should tighten as inventory grows"
    check("value at inventory 0 minus value at inventory +3", float(v[q_max] - v[-1]), 2.439, 5e-4, ".3f")


if __name__ == "__main__":
    section_bellman_by_hand()
    section_execution_dp()
    section_q_learning()
    section_max_bias()
    section_sim_gap()
    section_market_making()
    print("\nall checks passed")
