"""Neural networks by hand in numpy: backprop, gradient checks, low-SNR training, RNN/LSTM gradients and attention.

Backs 10-Machine-Learning-for-Finance/05-Neural-Networks-and-Sequence-Models.md.

1. Backprop for a one-hidden-unit tanh network, every intermediate quantity.
2. A two-layer MLP: analytic gradients against central finite differences.
3. Low signal-to-noise training: ridge, an over-parameterised MLP with no regularisation, and a small MLP with
   weight decay and early stopping on a later validation block; then five seeds and their ensemble.
4. Vanishing gradients in a scalar tanh RNN.
5. An LSTM cell (with forget gate) and backpropagation through time, gradient-checked; parameter count;
   the cell-state path dc_T/dc_0 against the product of forget gates.
6. Scaled dot-product attention: why divide by sqrt(d_k); a causal mask makes outputs blind to future inputs.

Run: uv run --no-project --with numpy python 10-Machine-Learning-for-Finance/code/nn_backprop_lstm.py
"""

from __future__ import annotations

import cmath
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
    """Assert an error-type quantity is below the bound the note quotes."""
    print(f"{label} = {value:.2e}")
    print(f"{label} bound = {bound:g}")
    assert value < bound, f"{label}: {value} is not below {bound}"


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


# ---------------------------------------------------------------------------
# 1. Backprop by hand
# ---------------------------------------------------------------------------


def section_tiny_backprop() -> None:
    # Backs: Worked example 1; cards ml-nn-tiny-net, ml-nn-gradient-check.
    print("\n== 1. Backprop for a 1-1-1 tanh network ==")
    x, y, w1, b1, w2, b2 = 1.0, 1.0, 0.5, 0.0, 2.0, 0.0

    def loss(w1_: float, w2_: float) -> float:
        return 0.5 * (w2_ * math.tanh(w1_ * x + b1) + b2 - y) ** 2

    z = w1 * x + b1
    h = math.tanh(z)
    yhat = w2 * h + b2
    d_yhat = yhat - y
    d_w2 = d_yhat * h
    d_h = d_yhat * w2
    d_z = d_h * (1 - h * h)
    d_w1 = d_z * x
    # Intermediates are quoted to enough digits that the card's chained products reproduce each rounded answer.
    check("tiny net h = tanh(0.5)", h, 0.462117, 5e-7, ".6f")
    check("tiny net prediction", yhat, 0.924234, 5e-7, ".6f")
    check("tiny net loss", loss(w1, w2), 0.00287, 5e-6, ".5f")
    check("tiny net dL/dyhat", d_yhat, -0.075766, 5e-7, ".6f")
    check("tiny net dL/dw2", d_w2, -0.0350, 5e-5)
    check("tiny net dL/dh", d_h, -0.15153, 5e-6, ".5f")
    check("tiny net tanh derivative 1 - h^2", 1 - h * h, 0.786448, 5e-7, ".6f")
    check("tiny net dL/dw1", d_w1, -0.1192, 5e-5)
    # The note's chain from its quoted (rounded) intermediates must land on the same rounded answers.
    assert f"{-0.075766 * 0.462117:.4f}" == "-0.0350" and f"{-0.075766 * 2:.5f}" == "-0.15153"
    assert f"{-0.15153 * 0.786448 * x:.4f}" == "-0.1192" and f"{0.5 - 0.5 * -0.1192:.4f}" == "0.5596"
    # Worked example 1: the four-decimal intermediates do not chain to the right answers.
    assert f"{-0.0758 * 2:.4f}" == "-0.1516" and f"{-0.1515 * 0.7864:.4f}" == "-0.1191"
    eps = 1e-6
    fd_w1 = (loss(w1 + eps, w2) - loss(w1 - eps, w2)) / (2 * eps)
    fd_w2 = (loss(w1, w2 + eps) - loss(w1, w2 - eps)) / (2 * eps)
    check_below("tiny net |analytic - finite difference|, w1 and w2", max(abs(fd_w1 - d_w1), abs(fd_w2 - d_w2)), 1e-9)
    check("tiny net w1 after one step at lr 0.5", w1 - 0.5 * d_w1, 0.5596, 5e-5)


# ---------------------------------------------------------------------------
# 2. MLP with backprop and gradient check
# ---------------------------------------------------------------------------


def init_mlp(rng: np.random.Generator, p: int, hidden: int) -> dict[str, np.ndarray]:
    return {
        "W1": rng.standard_normal((p, hidden)) / math.sqrt(p),
        "b1": np.zeros(hidden),
        "W2": rng.standard_normal((hidden, 1)) / math.sqrt(hidden),
        "b2": np.zeros(1),
    }


def mlp_forward(params: dict[str, np.ndarray], x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    h = np.tanh(x @ params["W1"] + params["b1"])
    return (h @ params["W2"] + params["b2"])[:, 0], h


def mlp_loss_grad(params: dict[str, np.ndarray], x: np.ndarray, y: np.ndarray, wd: float = 0.0) -> tuple[float, dict[str, np.ndarray]]:
    """Mean squared error / 2 plus wd/2 * |W|^2, and its gradient by backprop."""
    n = x.shape[0]
    yhat, h = mlp_forward(params, x)
    err = yhat - y
    loss = 0.5 * float(err @ err) / n + 0.5 * wd * float((params["W1"] ** 2).sum() + (params["W2"] ** 2).sum())
    d_out = (err / n)[:, None]  # dL/dyhat, shape (n, 1)
    grads = {"W2": h.T @ d_out + wd * params["W2"], "b2": d_out.sum(axis=0)}
    d_pre = (d_out @ params["W2"].T) * (1 - h * h)  # through tanh
    grads["W1"] = x.T @ d_pre + wd * params["W1"]
    grads["b1"] = d_pre.sum(axis=0)
    return loss, grads


def section_mlp_gradcheck() -> None:
    # Backs: Worked examples 1 and 6; cards ml-nn-gradient-check, ml-nn-param-count-mlp.
    print("\n== 2. MLP gradient check ==")
    rng = np.random.default_rng(1)
    x = rng.standard_normal((32, 5))
    y = rng.standard_normal(32)
    params = init_mlp(rng, 5, 8)
    _, grads = mlp_loss_grad(params, x, y, wd=0.01)
    worst = 0.0
    eps = 1e-5
    for name, arr in params.items():
        for idx in np.ndindex(arr.shape):
            old = arr[idx]
            arr[idx] = old + eps
            lp, _ = mlp_loss_grad(params, x, y, wd=0.01)
            arr[idx] = old - eps
            lm, _ = mlp_loss_grad(params, x, y, wd=0.01)
            arr[idx] = old
            fd = (lp - lm) / (2 * eps)
            worst = max(worst, abs(fd - grads[name][idx]))
    check("MLP 5-8-1 parameter count", sum(a.size for a in params.values()), 57, 0, ".0f")
    scale = max(float(np.abs(g).max()) for g in grads.values())
    check_below("MLP max |analytic - finite difference| / max |gradient|", worst / scale, 1e-7)


# ---------------------------------------------------------------------------
# 3. Low signal-to-noise training
# ---------------------------------------------------------------------------


def make_data(rng: np.random.Generator, n: int, p: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = rng.standard_normal((n, p))
    f = 0.2 * x[:, 0] * x[:, 1] + 0.1 * x[:, 2]
    return x, f + rng.standard_normal(n), f


def r2(y: np.ndarray, yhat: np.ndarray) -> float:
    """Out-of-sample R^2 against a zero forecast (y has mean zero by construction)."""
    return 1.0 - float(((y - yhat) ** 2).sum() / (y**2).sum())


def train_adam(
    params: dict[str, np.ndarray],
    x: np.ndarray,
    y: np.ndarray,
    epochs: int,
    lr: float,
    wd: float,
    x_val: np.ndarray | None = None,
    y_val: np.ndarray | None = None,
) -> tuple[dict[str, np.ndarray], int]:
    """Full-batch Adam; with a validation block, return the parameters at the epoch with the lowest validation loss."""
    m = {k: np.zeros_like(v) for k, v in params.items()}
    s = {k: np.zeros_like(v) for k, v in params.items()}
    best, best_epoch, best_params = math.inf, epochs, {k: v.copy() for k, v in params.items()}
    for t in range(1, epochs + 1):
        _, g = mlp_loss_grad(params, x, y, wd)
        for k in params:
            m[k] = 0.9 * m[k] + 0.1 * g[k]
            s[k] = 0.999 * s[k] + 0.001 * g[k] ** 2
            params[k] -= lr * (m[k] / (1 - 0.9**t)) / (np.sqrt(s[k] / (1 - 0.999**t)) + 1e-8)
        if x_val is not None:
            val = float(((mlp_forward(params, x_val)[0] - y_val) ** 2).mean())
            if val < best:
                best, best_epoch, best_params = val, t, {k: v.copy() for k, v in params.items()}
    return (best_params if x_val is not None else params), best_epoch


def section_low_snr() -> None:
    # Backs: Worked example 2; cards ml-nn-low-snr, ml-nn-seed-variance, ml-nn-param-count-mlp.
    print("\n== 3. Low signal-to-noise training ==")
    p = 10
    rng = np.random.default_rng(42)
    x_tr, y_tr, _ = make_data(rng, 3000, p)
    x_va, y_va, _ = make_data(rng, 1000, p)
    x_te, y_te, f_te = make_data(rng, 20000, p)
    check("population R^2 of the true function", 0.05 / 1.05, 0.0476, 5e-5)
    check("population R^2 of the best linear model", 0.01 / 1.05, 0.0095, 5e-5)
    check("test R^2 of the true function (sample)", r2(y_te, f_te), 0.0529, 5e-5)
    # Independent check of the population variance of the signal by Monte Carlo (seed 11, 2 million draws).
    xm = np.random.default_rng(11).standard_normal((2_000_000, 3))
    signal_mc = 0.2 * xm[:, 0] * xm[:, 1] + 0.1 * xm[:, 2]
    check("Monte Carlo variance of 0.2 x1 x2 + 0.1 x3 (theory 0.05)", float(signal_mc.var()), 0.050, 5e-4, ".3f")
    # The best linear predictor is 0.1 x3 (x1 x2 is uncorrelated with every x_j); its test-sample R^2 is the linear ceiling.
    lin_ceiling = r2(y_te, 0.1 * x_te[:, 2])
    check("test R^2 of the oracle linear forecast 0.1 x3 (linear ceiling)", lin_ceiling, 0.0100, 5e-5)

    xa = np.hstack([x_tr, np.ones((x_tr.shape[0], 1))])
    beta = np.linalg.solve(xa.T @ xa + 10.0 * np.eye(p + 1), xa.T @ y_tr)
    pred_te = np.hstack([x_te, np.ones((x_te.shape[0], 1))]) @ beta
    check("ridge train R^2", r2(y_tr, xa @ beta), 0.0141, 5e-5)
    check("ridge test R^2", r2(y_te, pred_te), 0.0017, 5e-5)

    # Capacity without regularisation: a random-feature network (first layer fixed at random, 1000 tanh units)
    # whose output layer is fitted by least squares. The fit is convex, so the numbers do not depend on the optimiser.
    width = 1000
    w_rf = np.random.default_rng(9).standard_normal((p, width)) / math.sqrt(p)
    b_rf = 0.5 * np.random.default_rng(10).standard_normal(width)
    h_tr, h_te = np.tanh(x_tr @ w_rf + b_rf), np.tanh(x_te @ w_rf + b_rf)
    out_ls = np.linalg.solve(h_tr.T @ h_tr, h_tr.T @ y_tr)
    check("random-feature net (1000 units, least squares) train R^2", r2(y_tr, h_tr @ out_ls), 0.363, 5e-4, ".3f")
    check("random-feature net (1000 units, least squares) test R^2", r2(y_te, h_te @ out_ls), -0.539, 5e-4, ".3f")
    out_ridge = np.linalg.solve(h_tr.T @ h_tr + 1000.0 * np.eye(width), h_tr.T @ y_tr)
    check("random-feature net, ridge penalty 1000, train R^2", r2(y_tr, h_tr @ out_ridge), 0.063, 5e-4, ".3f")
    check("random-feature net, ridge penalty 1000, test R^2", r2(y_te, h_te @ out_ridge), 0.018, 5e-4, ".3f")

    check("small MLP 10-16-1 parameter count", sum(a.size for a in init_mlp(np.random.default_rng(0), p, 16).values()), 193, 0, ".0f")
    test_r2 = []
    preds = []
    for seed in range(5):
        small = init_mlp(np.random.default_rng(100 + seed), p, 16)
        small, _ = train_adam(small, x_tr, y_tr, epochs=1500, lr=0.01, wd=1e-3, x_val=x_va, y_val=y_va)
        pred = mlp_forward(small, x_te)[0]
        preds.append(pred)
        test_r2.append(r2(y_te, pred))
    print("small MLP test R^2 by seed: " + ", ".join(f"{v:.4f}" for v in test_r2))
    check("small MLP (16 hidden, wd 1e-3, early stopping) mean test R^2 over 5 seeds", float(np.mean(test_r2)), 0.016, 5e-4, ".3f")
    check("small MLP min test R^2 over 5 seeds", float(np.min(test_r2)), 0.0125, 5e-5)
    check("small MLP max test R^2 over 5 seeds", float(np.max(test_r2)), 0.0221, 5e-5)
    ens = r2(y_te, np.mean(preds, axis=0))
    check("5-seed ensemble test R^2", ens, 0.027, 5e-4, ".3f")
    check("ratio of best to worst seed test R^2", float(np.max(test_r2) / np.min(test_r2)), 1.8, 0.05, ".1f")
    # Beating the linear ceiling can only come from the nonlinear (x1 x2) part of the signal.
    rf_ridge_te = r2(y_te, h_te @ out_ridge)
    assert ens > lin_ceiling and rf_ridge_te > lin_ceiling and min(test_r2) > lin_ceiling, "nonlinear models must beat the linear ceiling"
    print("ensemble, ridge random-feature net and every MLP seed beat the linear ceiling: True")


# ---------------------------------------------------------------------------
# 4. Vanishing gradients in a tanh RNN
# ---------------------------------------------------------------------------


def section_rnn_vanishing() -> None:
    # Backs: Worked example 3 and Core concepts (RNN); card ml-nn-vanishing-rnn.
    print("\n== 4. Vanishing gradients in a scalar tanh RNN ==")
    check("0.9^50 (bound on dh_50/dh_0 for |w| = 0.9)", 0.9**50, 0.00515, 5e-6, ".5f")
    rng = np.random.default_rng(3)
    u = 0.5 * rng.standard_normal(50)

    def rnn_jacobian(w: float, inputs: np.ndarray) -> float:
        h, jac = 0.0, 1.0
        for t in range(50):
            h = math.tanh(w * h + inputs[t])
            jac *= w * (1 - h * h)
        return jac

    for w, exp, tol, exp_geo in [(0.9, 9.11e-12, 5e-15, 0.601), (1.5, 2.40e-10, 5e-13, 0.642)]:
        jac = rnn_jacobian(w, u)
        # Independent check by complex-step differentiation of h_50 in h_0 (no subtraction, so no cancellation at 1e-12).
        hc = complex(0.0, 1e-30)
        for t in range(50):
            hc = cmath.tanh(w * hc + u[t])
        assert abs(hc.imag / 1e-30 - jac) <= 1e-9 * abs(jac), f"RNN Jacobian {jac} disagrees with complex step {hc.imag / 1e-30}"
        check(f"dh_50/dh_0 for recurrent weight {w}", abs(jac), exp, tol, ".2e")
        check(f"geometric mean of the per-step factor w(1 - h_t^2), w = {w}", abs(jac) ** (1 / 50), exp_geo, 5e-4, ".3f")
    # The factor 1.5 (1 - h^2) drops below 1 once |h| exceeds the root of 1.5 (1 - h^2) = 1, found here by bisection.
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if 1.5 * (1 - mid * mid) > 1 else (lo, mid)
    check("|h| above which 1.5 (1 - h^2) < 1", lo, 0.577, 5e-4, ".3f")
    # Control: zero inputs keep h_t = 0, where tanh is linear, so every factor is exactly w and the gradient explodes.
    check("dh_50/dh_0 for recurrent weight 1.5 with zero inputs (= 1.5^50)", rnn_jacobian(1.5, np.zeros(50)), 6.38e8, 5e5, ".2e")
    # Closed form against the recursion above: with h_t = 0 every factor is w, so the product is 1.5^50.
    assert abs(rnn_jacobian(1.5, np.zeros(50)) - 1.5**50) <= 1e-12 * 1.5**50
    print(f"1.5^50 = {1.5**50:.2e} (equals the zero-input recursion)")
    hstar = 0.9
    for _ in range(200):  # fixed point of h = tanh(1.5 h), by iteration
        hstar = math.tanh(1.5 * hstar)
    check("stable fixed point h* of h = tanh(1.5 h)", hstar, 0.8586, 5e-5)
    check("per-step factor at the fixed point, 1.5 (1 - h*^2)", 1.5 * (1 - hstar**2), 0.394, 5e-4, ".3f")


# ---------------------------------------------------------------------------
# 5. LSTM with backpropagation through time
# ---------------------------------------------------------------------------


def lstm_params(rng: np.random.Generator, d: int, hdim: int, forget_bias: float, scale: float) -> dict[str, np.ndarray]:
    """Gates stacked as [input, forget, output, candidate]; W maps [x_t, h_{t-1}, 1] to 4*hdim pre-activations."""
    w = scale * rng.standard_normal((d + hdim + 1, 4 * hdim))
    w[-1, hdim : 2 * hdim] = forget_bias
    return {"W": w}


def lstm_forward(w: np.ndarray, xs: np.ndarray, hdim: int, c0: np.ndarray) -> tuple[np.ndarray, np.ndarray, list]:
    h, c = np.zeros(hdim), c0.copy()
    cache = []
    for x in xs:
        z = np.concatenate([x, h, [1.0]])
        a = z @ w
        i, f, o = sigmoid(a[:hdim]), sigmoid(a[hdim : 2 * hdim]), sigmoid(a[2 * hdim : 3 * hdim])
        g = np.tanh(a[3 * hdim :])
        c_prev = c
        c = f * c_prev + i * g
        h = o * np.tanh(c)
        cache.append((z, i, f, o, g, c_prev, c))
    return h, c, cache


def lstm_loss_grad(w: np.ndarray, xs: np.ndarray, hdim: int, target: np.ndarray, c0: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    """Loss 0.5|h_T - target|^2; returns loss, dL/dW and dL/dc_0 by BPTT."""
    h, _, cache = lstm_forward(w, xs, hdim, c0)
    loss = 0.5 * float((h - target) @ (h - target))
    dw = np.zeros_like(w)
    dh = h - target
    dc = np.zeros(hdim)
    d = xs.shape[1]
    for z, i, f, o, g, c_prev, c in reversed(cache):
        tc = np.tanh(c)
        do = dh * tc
        dc = dc + dh * o * (1 - tc * tc)
        di, df, dg = dc * g, dc * c_prev, dc * i
        da = np.concatenate([di * i * (1 - i), df * f * (1 - f), do * o * (1 - o), dg * (1 - g * g)])
        dw += np.outer(z, da)
        dz = w @ da
        dh = dz[d : d + hdim]
        dc = dc * f  # cell-state path to the previous step
    return loss, dw, dc


def section_lstm() -> None:
    # Backs: Worked examples 3 and 6; cards ml-nn-lstm-params, ml-nn-forget-bias, ml-nn-lstm-why-works.
    print("\n== 5. LSTM and BPTT ==")
    for d, hdim, exp in [(3, 8, 384), (10, 32, 5504)]:
        w = lstm_params(np.random.default_rng(0), d, hdim, 1.0, 0.1)
        check(f"LSTM parameter count, d {d}, h {hdim}", w["W"].size, exp, 0, ".0f")
    # PyTorch's nn.LSTM keeps two bias vectors (b_ih and b_hh), so it reports 4h(d + h + 2).
    torch_shapes = [(4 * 32, 10), (4 * 32, 32), (4 * 32,), (4 * 32,)]  # weight_ih, weight_hh, bias_ih, bias_hh
    torch_count = sum(np.zeros(shape).size for shape in torch_shapes)
    check("LSTM parameter count with two bias vectors (PyTorch convention), d 10, h 32", torch_count, 5632, 0, ".0f")
    rng = np.random.default_rng(4)
    d, hdim, steps = 3, 8, 12
    w = lstm_params(rng, d, hdim, 1.0, 0.3)["W"]
    xs = rng.standard_normal((steps, d))
    target = rng.standard_normal(hdim) * 0.5
    c0 = 0.1 * rng.standard_normal(hdim)
    _, dw, dc0 = lstm_loss_grad(w, xs, hdim, target, c0)
    eps, worst = 1e-5, 0.0
    for idx in np.ndindex(w.shape):
        old = w[idx]
        w[idx] = old + eps
        lp = lstm_loss_grad(w, xs, hdim, target, c0)[0]
        w[idx] = old - eps
        lm = lstm_loss_grad(w, xs, hdim, target, c0)[0]
        w[idx] = old
        fd = (lp - lm) / (2 * eps)
        worst = max(worst, abs(fd - dw[idx]))
    worst_c = 0.0
    for j in range(hdim):
        e = np.zeros(hdim)
        e[j] = eps
        fd = (lstm_loss_grad(w, xs, hdim, target, c0 + e)[0] - lstm_loss_grad(w, xs, hdim, target, c0 - e)[0]) / (2 * eps)
        worst_c = max(worst_c, abs(fd - dc0[j]))
    check_below("LSTM BPTT max |analytic - finite difference| / max |gradient| (weights)", worst / float(np.abs(dw).max()), 1e-7)
    check_below("LSTM BPTT max |analytic - finite difference| / max |gradient| (initial cell)", worst_c / float(np.abs(dc0).max()), 1e-7)

    # Cell-state memory: d c_T / d c_0 (one unit, finite difference) against the product of that unit's forget gates.
    steps = 50
    xs = np.random.default_rng(5).standard_normal((steps, d))
    for bias, exp_sig, exp_prod, exp_fd in [(1.0, 0.7311, 1.63e-07, 7.31e-07), (5.0, 0.9933, 0.709, 1.31)]:
        w = lstm_params(np.random.default_rng(6), d, hdim, bias, 0.05)["W"]
        c0 = np.zeros(hdim)
        _, _, cache = lstm_forward(w, xs, hdim, c0)
        prod_f = float(np.prod([fc[2][0] for fc in cache]))
        # Complex-step derivative of c_50[0] in c_0[0]: exact to rounding even when the derivative is 1e-7.
        e = np.zeros(hdim, dtype=complex)
        e[0] = 1e-30j
        fd = float(lstm_forward(w, xs, hdim, c0 + e)[1][0].imag / 1e-30)
        check(f"forget bias {bias}: sigmoid(bias)", float(sigmoid(np.array(bias))), exp_sig, 5e-5)
        if bias == 1.0:
            # Card ml-nn-forget-bias: a gate pinned at sigmoid(1) for 50 steps keeps this fraction of the memory.
            check("sigmoid(1)^50", float(sigmoid(np.array(1.0))) ** 50, 1.58e-07, 5e-10, ".3g")
        check(f"forget bias {bias}: product of 50 forget gates", prod_f, exp_prod, 5e-3 * exp_prod, ".3g")
        check(f"forget bias {bias}: dc_50/dc_0 by complex step", fd, exp_fd, 5e-3 * exp_fd, ".3g")
        # Control: cut the recurrent rows (h_{t-1} into the gates). Then c_0 reaches c_50 only along the cell path,
        # and the derivative must equal the product of forget gates exactly.
        w_cut = w.copy()
        w_cut[d : d + hdim, :] = 0.0
        _, _, cache_cut = lstm_forward(w_cut, xs, hdim, c0)
        prod_cut = float(np.prod([fc[2][0] for fc in cache_cut]))
        fd_cut = float(lstm_forward(w_cut, xs, hdim, c0 + e)[1][0].imag / 1e-30)
        print(f"forget bias {bias}, recurrent weights cut: dc_50/dc_0 = {fd_cut:.4g}, product of forget gates = {prod_cut:.4g}")
        assert abs(fd_cut - prod_cut) <= 1e-9 * prod_cut, "without the h path, dc_T/dc_0 must equal the product of forget gates"


# ---------------------------------------------------------------------------
# 6. Attention
# ---------------------------------------------------------------------------


def softmax_rows(a: np.ndarray) -> np.ndarray:
    a = a - a.max(axis=-1, keepdims=True)
    e = np.exp(a)
    return e / e.sum(axis=-1, keepdims=True)


def self_attention(x: np.ndarray, wq: np.ndarray, wk: np.ndarray, wv: np.ndarray, causal: bool) -> np.ndarray:
    q, k, v = x @ wq, x @ wk, x @ wv
    scores = q @ k.T / math.sqrt(k.shape[1])
    if causal:
        scores = np.where(np.tril(np.ones_like(scores, dtype=bool)), scores, -np.inf)
    return softmax_rows(scores) @ v


def section_attention() -> None:
    # Backs: Worked examples 4, 5 and 6; cards ml-nn-attention-scaling, ml-nn-causal-mask, ml-nn-transformer-params.
    print("\n== 6. Scaled dot-product attention ==")
    rng = np.random.default_rng(8)
    dk = 64
    q = rng.standard_normal((200_000, dk))
    k = rng.standard_normal((200_000, dk))
    dots = (q * k).sum(axis=1)
    check("sd of q.k for d_k 64, unit-variance entries (theory sqrt(64))", float(dots.std()), 8.0, 0.05, ".1f")
    # Average largest softmax weight over 16 keys, raw versus scaled logits.
    logits = (q[:16_000] * k[:16_000]).sum(axis=1).reshape(1000, 16)
    check("mean max attention weight over 16 keys, unscaled", float(softmax_rows(logits).max(axis=1).mean()), 0.853, 5e-4, ".3f")
    check(
        "mean max attention weight over 16 keys, scaled by 1/sqrt(d_k)",
        float(softmax_rows(logits / 8).max(axis=1).mean()),
        0.245,
        5e-4,
        ".3f",
    )

    t, dm = 10, 8
    x = rng.standard_normal((t, dm))
    wq, wk, wv = (rng.standard_normal((dm, dm)) / math.sqrt(dm) for _ in range(3))
    x2 = x.copy()
    x2[6:] += 5.0 * rng.standard_normal((t - 6, dm))  # change the "future" rows 6..9
    causal_diff = float(np.abs(self_attention(x, wq, wk, wv, True)[:6] - self_attention(x2, wq, wk, wv, True)[:6]).max())
    full_diff = float(np.abs(self_attention(x, wq, wk, wv, False)[:6] - self_attention(x2, wq, wk, wv, False)[:6]).max())
    check("causal attention: max change in outputs 0-5 when inputs 6-9 change", causal_diff, 0.0, 0.0, ".1f")
    check("unmasked attention: max change in outputs 0-5", full_diff, 9.93, 5e-3, ".2f")
    # Build the weight matrices of one layer (4 heads; the head split does not change the count) and count them.
    dmod, heads = 64, 4
    layer = [rng.standard_normal((dmod, dmod // heads)) for _ in range(3 * heads)]  # per-head Q, K, V projections
    layer += [rng.standard_normal((dmod, dmod)), rng.standard_normal((dmod, 4 * dmod)), rng.standard_normal((4 * dmod, dmod))]
    check("transformer layer weights for d_model 64, 4 heads (no biases, no norms)", sum(a.size for a in layer), 49152, 0, ".0f")
    check("12 d^2 for d_model 64", 12 * dmod**2, 49152, 0, ".0f")


if __name__ == "__main__":
    section_tiny_backprop()
    section_mlp_gradcheck()
    section_low_snr()
    section_rnn_vanishing()
    section_lstm()
    section_attention()
    print("\nall checks passed")
