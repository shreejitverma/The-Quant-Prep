"""NumPy numerics: broadcasting, memory layout, views and copies, floating point, overflow, rolling windows.

Backs the numbers in 12-Quant-Development/11-Numerical-Python-NumPy-and-Numba.md.
Every value quoted in the note is printed and asserted here. Timings are machine-dependent:
they are printed for illustration and asserted only against loose sanity bounds.

Run: uv run --no-project --with numpy python 12-Quant-Development/code/python/numpy_numerics.py
"""

from __future__ import annotations

import math
import sys
import time

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from pcg_stream import PcgStream


def section(title: str) -> None:
    print(f"\n== {title}")


def broadcasting() -> None:
    section("Broadcasting")
    a = np.arange(3.0).reshape(3, 1)  # shape (3, 1)
    b = np.arange(4.0).reshape(1, 4)  # shape (1, 4)
    c = a + b
    print("(3,1) + (1,4) ->", c.shape)
    assert c.shape == (3, 4) and c[2, 3] == 5.0
    # Demean the columns of a (T, N) returns panel: (T, N) - (N,) broadcasts over rows.
    rng = PcgStream(0)
    r = rng.normal(size=(250, 5))
    d = r - r.mean(axis=0)
    print("max |column mean| after demeaning:", f"{np.abs(d.mean(axis=0)).max():.1e}")
    assert np.abs(d.mean(axis=0)).max() < 1e-15
    # Demean the rows needs keepdims (or [:, None]); r - r.mean(axis=1) fails for T != N.
    try:
        _ = r - r.mean(axis=1)
        raise AssertionError("expected a broadcasting error")
    except ValueError as e:
        print("r - r.mean(axis=1) raises:", str(e).split(" with shapes")[0])
        assert "operands could not be broadcast together" in str(e)
    e2 = r - r.mean(axis=1, keepdims=True)
    assert np.abs(e2.mean(axis=1)).max() < 1e-15
    # Pairwise distance matrix without loops: (n,1,k) - (1,n,k) -> (n,n,k).
    x = rng.normal(size=(100, 3))
    diff = x[:, None, :] - x[None, :, :]
    dist = np.sqrt((diff**2).sum(-1))
    tmp_small = diff.nbytes  # the temporary actually materialised at n = 100
    tmp_big = tmp_small * (100_000 // 100) ** 2  # the (n, n, 3) temporary scales as n^2
    print("pairwise distance matrix shape:", dist.shape, "temporary bytes:", tmp_small, "at n=1e5:", f"{tmp_big / 1e9:.0f} GB")
    assert diff.shape == (100, 100, 3) and tmp_small == 240_000 and f"{tmp_big / 1e9:.0f}" == "240"
    print(f"temporary bytes at n=1e5: {tmp_big:.1e}")
    assert f"{tmp_big:.1e}" == "2.4e+11"
    assert dist.shape == (100, 100) and np.allclose(np.diag(dist), 0.0)


def layout() -> None:
    section("Memory layout and strides")
    c = np.zeros((1000, 1000))
    f = np.zeros((1000, 1000), order="F")
    print("C order strides:", c.strides, " F order strides:", f.strides, " transpose strides:", c.T.strides)
    assert c.strides == (8000, 8) and f.strides == (8, 8000) and c.T.strides == (8, 8000)
    assert c.T.flags["F_CONTIGUOUS"] and not c.T.flags["C_CONTIGUOUS"]
    s = c[:, ::2]
    print("c[:, ::2] shape:", s.shape, "strides:", s.strides, "contiguous:", s.flags["C_CONTIGUOUS"])
    assert s.shape == (1000, 500) and s.strides == (8000, 16) and not s.flags["C_CONTIGUOUS"]
    print("float32 (1000,1000) bytes:", np.zeros((1000, 1000), np.float32).nbytes)
    assert np.zeros((1000, 1000), np.float32).nbytes == 4_000_000


def views_and_copies() -> None:
    section("Views and copies")
    a = np.arange(10)
    v = a[2:8:2]
    print("basic slice shares memory:", np.shares_memory(a, v))
    assert np.shares_memory(a, v)
    v[0] = 99
    assert a[2] == 99  # writing through a view mutates the base
    fancy = a[[1, 3, 5]]
    mask = a[a > 5]
    print("fancy index shares memory:", np.shares_memory(a, fancy), " boolean mask:", np.shares_memory(a, mask))
    assert not np.shares_memory(a, fancy) and not np.shares_memory(a, mask)
    m = np.arange(12).reshape(3, 4)
    print("reshape of contiguous shares:", np.shares_memory(m, m.reshape(4, 3)))
    assert np.shares_memory(m, m.reshape(4, 3))
    t = m.T.reshape(12)  # transpose is not C contiguous, so reshape must copy
    print("reshape of transpose shares:", np.shares_memory(m, t))
    assert not np.shares_memory(m, t)
    print("ravel of contiguous shares:", np.shares_memory(m, m.ravel()), " flatten:", np.shares_memory(m, m.flatten()))
    assert np.shares_memory(m, m.ravel()) and not np.shares_memory(m, m.flatten())
    # In-place operators reuse the buffer; x = x + 1 allocates a new array.
    x = np.ones(5)
    xid = x.__array_interface__["data"][0]
    x += 1
    same = x.__array_interface__["data"][0] == xid
    x = x + 1
    new = x.__array_interface__["data"][0] != xid
    print("x += 1 keeps buffer:", same, " x = x + 1 new buffer:", new)
    assert same and new


def floats() -> None:
    section("Floating point")
    s = 0.1 + 0.2
    print("0.1 + 0.2 =", repr(s), " == 0.3:", s == 0.3, " difference:", repr(s - 0.3))
    assert s != 0.3 and s - 0.3 == 2.0**-54
    assert repr(s) == "0.30000000000000004" and f"{s - 0.3:.2e}" == "5.55e-17"
    print("isclose(0.1 + 0.2, 0.3):", math.isclose(s, 0.3))
    assert math.isclose(s, 0.3)
    e64, e32 = np.finfo(np.float64).eps, np.finfo(np.float32).eps
    print("eps float64:", repr(float(e64)), " eps float32:", repr(float(e32)))
    assert e64 == 2.0**-52 and e32 == 2.0**-23
    assert f"{e64:.2e}" == "2.22e-16" and f"{e32:.2e}" == "1.19e-07"
    print("float32(16777217) =", int(np.float32(16777217)), " float64(2**53 + 1) =", int(np.float64(2**53 + 1)))
    assert int(np.float32(16777217)) == 16777216 and int(np.float64(2**53 + 1)) == 2**53
    # float32 has 24 significand bits: above 131,072 its spacing is 1/64 > 0.01, so neighbouring cent prices collide.
    p = np.float32(123456.78)
    print("float32(123456.78) =", repr(float(p)), " error:", f"{abs(float(p) - 123456.78):.6f}")
    assert float(p) == 123456.78125
    print("1e16 + 1 - 1e16 in float64:", (1e16 + 1.0) - 1e16, " ulp of 1e16:", float(np.spacing(1e16)))
    assert (1e16 + 1.0) - 1e16 == 0.0 and np.spacing(1e16) == 2.0
    gap = float(np.spacing(np.float32(131072.0)))
    print("float32 spacing at 131072:", gap, " at 65536:", float(np.spacing(np.float32(65536.0))))
    assert gap == 0.015625 and float(np.spacing(np.float32(65536.0))) == 0.0078125


def summation() -> None:
    section("Summation error")
    n = 10_000_000
    x = np.full(n, 0.1, dtype=np.float32)
    exact = math.fsum(np.full(n, np.float64(np.float32(0.1))))  # exact sum of the stored float32 values
    seq = float(np.cumsum(x)[-1])  # strictly sequential float32 accumulation
    pair = float(np.sum(x))  # pairwise summation in float32
    print(f"float32 n=1e7 of 0.1: exact {exact:.4f}, sequential {seq:.4f}, pairwise np.sum {pair:.4f}")
    print(f"sequential relative error {100 * (seq - exact) / exact:.2f}%; stored float32(0.1) = {float(np.float32(0.1)):.15f}")
    assert f"{float(np.float32(0.1)):.15f}" == "0.100000001490116"
    assert f"{100 * (seq - exact) / exact:.2f}" == "8.79"
    assert f"{exact:.4f}" == "1000000.0149"
    assert seq == 1087937.0
    # np.sum's blocking (and so its last digits, 1000000.1250 on the author's machine) depends on platform and
    # NumPy version; note 11 labels it so and the script asserts only that its
    # relative error is below 0.01%, against 8.79% for the sequential sum.
    assert abs(pair - exact) / exact < 1e-4
    # float64 with a Python loop versus np.sum versus fsum, on data uniform on +-sqrt(3) * 1e6 (sd 1e6).
    # Uniforms from raw bits times a correctly rounded constant are bit-identical on every platform, which
    # matters here: the loop's error is a sum of a million roundings and changes with any input bit.
    rng = PcgStream(1)
    y = (2.0 * rng.uniform(1_000_000) - 1.0) * (math.sqrt(3.0) * 1e6)
    loop = 0.0
    for v in y.tolist():
        loop += v
    ex = math.fsum(y.tolist())
    print(f"float64 n=1e6: |loop - fsum| {abs(loop - ex):.3e}, |np.sum - fsum| {abs(float(np.sum(y)) - ex):.3e}")
    assert abs(float(np.sum(y)) - ex) <= abs(loop - ex) + 1e-6
    assert f"{abs(loop - ex):.3e}" == "8.076e-06" and f"{abs(loop - ex):.1e}" == "8.1e-06"
    # Since Python 3.12 the built-in sum() of floats is compensated (Neumaier), unlike a += loop.
    tenth = [0.1] * 10
    acc = 0.0
    for v in tenth:
        acc += v
    print(f"sum([0.1] * 10) = {sum(tenth)!r}, += loop = {acc!r}")
    assert acc == 0.9999999999999999
    if sys.version_info >= (3, 12):
        assert sum(tenth) == 1.0


def variance() -> None:
    section("Variance: naive one-pass versus Welford")
    data = 1e9 + np.array([4.0, 7.0, 13.0, 16.0])

    def naive(xs: np.ndarray) -> float:
        n = len(xs)
        s = ss = 0.0
        for v in xs:
            s += v
            ss += v * v
        return (ss - s * s / n) / (n - 1)

    def welford(xs: np.ndarray) -> float:
        mean = m2 = 0.0
        for k, v in enumerate(xs, 1):
            d = v - mean
            mean += d / k
            m2 += d * (v - mean)
        return m2 / (len(xs) - 1)

    nv, wv, tp = naive(data), welford(data), float(np.var(data, ddof=1))
    print(f"true sample variance 30, naive {nv}, Welford {wv}, two-pass np.var {tp}")
    ssd = float(np.sum((data - data.mean()) ** 2))
    print(f"sum of squared deviations {ssd}")
    assert ssd == 90.0
    sum_sq = float(np.sum(data * data))
    print(f"sum of squares {sum_sq:.3e}, its ulp {float(np.spacing(sum_sq))}")
    assert abs(sum_sq - 4.00000008e18) < 1e10 and np.spacing(sum_sq) == 512.0
    assert wv == 30.0 and tp == 30.0 and nv != 30.0
    assert nv == -170.66666666666666 and f"{nv:.2f}" == "-170.67"
    assert f"{sum_sq:.1e}" == "4.0e+18"


def overflow() -> None:
    section("Fixed-width integer overflow")
    a = np.array([2**31 - 1], dtype=np.int32)
    print("int32 max + 1 =", int((a + 1)[0]))
    assert int((a + 1)[0]) == -(2**31)
    # Notional in price ticks of $0.0001 (ITCH Price(4)) times shares overflows int32 quickly.
    price = np.array([2_500_000], dtype=np.int32)  # $250.0000
    print(f"price $250.0000 in Price(4) units: {int(price[0]):,}; times 1,000 shares")
    qty = np.array([1_000], dtype=np.int32)
    wrong = int((price * qty)[0])
    right = int(price.astype(np.int64)[0] * qty.astype(np.int64)[0])
    print(f"int32 notional {wrong}, int64 notional {right} (= ${right / 1e4:,.2f})")
    assert right == 2_500_000_000 and wrong == -1_794_967_296
    assert wrong == right - 2**32  # exactly 2^32 less
    u = np.array([3], dtype=np.uint32) - np.array([5], dtype=np.uint32)
    print("uint32 3 - 5 =", int(u[0]))
    assert int(u[0]) == 4_294_967_294


def rolling() -> None:
    section("Rolling windows")
    rng = PcgStream(2)
    x = rng.normal(size=10_000)
    w = 20
    c = np.cumsum(np.concatenate(([0.0], x)))
    by_cumsum = (c[w:] - c[:-w]) / w
    by_view = sliding_window_view(x, w).mean(axis=1)
    by_loop = np.array([x[i : i + w].mean() for i in range(len(x) - w + 1)])
    err_c = np.abs(by_cumsum - by_loop).max()
    err_v = np.abs(by_view - by_loop).max()
    print(f"rolling mean w=20 n=1e4: max err cumsum {err_c:.1e}, sliding_window_view {err_v:.1e}")
    assert err_c < 1e-14 and err_v < 1e-15
    print("sliding_window_view shape", sliding_window_view(x, w).shape, "shares memory:", np.shares_memory(x, sliding_window_view(x, w)))
    assert np.shares_memory(x, sliding_window_view(x, w))
    # cumsum differences lose precision when the running sum is large relative to the window sum.
    big = 1e8 + rng.normal(size=1_000_000)
    cb = np.cumsum(np.concatenate(([0.0], big)))
    tail = 2000  # the last 2,000 windows, where the running total is near 1e14
    starts = np.arange(len(big) - w + 1 - tail, len(big) - w + 1)
    exact = np.array([math.fsum(big[i : i + w].tolist()) / w for i in starts])
    err_cs = np.abs((cb[starts + w] - cb[starts]) / w - exact)
    err_dir = np.abs(sliding_window_view(big, w)[starts].mean(axis=1) - exact)
    med_cs, p90_cs = float(np.median(err_cs)), float(np.quantile(err_cs, 0.9))
    # Theory: each of the w additions inside a window rounds to the ulp u of a total near 1e14, an error
    # uniform on [-u/2, u/2] with sd u / sqrt(12); summed over w and divided by w the window mean has
    # sd u * sqrt(w / 12) / w, and the median of |N(0, sd)| is 0.674 sd.
    ulp_total = float(np.spacing(cb[-1]))
    sd_theory = ulp_total * math.sqrt(w / 12) / w
    ulp_1e8 = float(np.spacing(1e8))
    print(f"rolling mean of 1e8 + noise, last {tail:,} windows of 1e6 points: cumsum error median {med_cs:.1e}, p90 {p90_cs:.1e}")
    print(f"  theory: ulp of the running total {ulp_total}, error sd {sd_theory:.1e}, median {0.674 * sd_theory:.1e}")
    print(f"  direct window mean error: max {float(err_dir.max()):.1e} = {float(err_dir.max()) / ulp_1e8:.1f} ulps of 1e8 ({ulp_1e8:.1e})")
    # Note 11 example 4 and card qd-np-cumsum-rolling, at the quoted rounding.
    assert ulp_total == 2.0**-6 and f"{sd_theory:.1e}" == "1.0e-03" and f"{0.674 * sd_theory:.1e}" == "6.8e-04"
    assert 0.5 < med_cs / (0.674 * sd_theory) < 2.0 and 0.5 < p90_cs / (1.645 * sd_theory) < 2.0
    assert f"{med_cs:.1e}" == "6.6e-04" and f"{p90_cs:.1e}" == "1.6e-03"
    assert float(err_dir.max()) <= 4 * ulp_1e8 < med_cs / 100 and f"{ulp_1e8:.1e}" == "1.5e-08"
    # Max drawdown is path dependent but still vectorises with a running maximum.
    pnl = np.array([0.0, 3.0, 1.0, 4.0, -2.0, 5.0, 2.0])
    peak = np.maximum.accumulate(pnl)
    mdd = float((peak - pnl).max())
    print("running peak", peak.tolist(), "max drawdown of", pnl.tolist(), "=", mdd)
    assert peak.tolist() == [0.0, 3.0, 3.0, 4.0, 4.0, 5.0, 5.0] and mdd == 6.0


def ewma_closed_form() -> None:
    section("A recursion that does not vectorise safely")
    alpha = 0.1
    # y_t = (1 - alpha) y_{t-1} + alpha x_t has the closed form
    # y_t = (1 - alpha)^t [ y_0 + alpha * sum_{s<=t} x_s (1 - alpha)^{-s} ]
    limit = math.log(np.finfo(np.float64).max) / -math.log(1 - alpha)
    print(f"(1 - alpha)^(-s) overflows float64 for s > {limit:.1f} when alpha = {alpha}")
    assert f"{limit:.1f}" == "6736.7" and f"{limit:,.0f}" == "6,737"

    def loop(x: np.ndarray) -> np.ndarray:
        y = np.empty_like(x)
        acc = x[0]
        for i, v in enumerate(x):
            acc = (1 - alpha) * acc + alpha * v if i else v
            y[i] = acc
        return y

    def closed(x: np.ndarray) -> np.ndarray:
        s = np.arange(len(x))
        with np.errstate(over="ignore", invalid="ignore"):
            w = (1 - alpha) ** (-s.astype(float))
            inner = x[0] + alpha * np.cumsum((x * w)[1:])
            out = np.concatenate(([x[0]], (1 - alpha) ** s[1:] * inner))
        return out

    rng = PcgStream(3)
    short = rng.normal(size=1000)
    long = rng.normal(size=10_000)
    e_short = np.abs(closed(short) - loop(short)).max()
    bad = int(np.count_nonzero(~np.isfinite(closed(long))))
    print(f"closed form vs loop n=1000: max err {e_short:.1e}; n=10000: {bad} non-finite outputs")
    assert e_short < 1e-9 and bad == 3265


def timing() -> None:
    section("Timing (machine-dependent; loose sanity bounds only)")
    rng = PcgStream(4)
    x = rng.normal(size=1_000_000)
    xs = x.tolist()

    def best(fn, reps: int = 3) -> float:
        out = []
        for _ in range(reps):
            t0 = time.perf_counter()
            fn()
            out.append(time.perf_counter() - t0)
        return min(out)

    t_loop = best(lambda: sum(v * v for v in xs))
    t_vec = best(lambda: float(np.dot(x, x)))
    print(f"sum of squares n=1e6: Python loop {t_loop * 1e3:.1f} ms, np.dot {t_vec * 1e3:.2f} ms, ratio {t_loop / t_vec:.0f}x")
    assert t_loop / t_vec > 3.0
    a = rng.normal(size=(2000, 2000))
    t_rows = best(lambda: a.copy())
    t_cols = best(lambda: np.ascontiguousarray(a.T))
    print(f"copy 2000x2000 contiguous {t_rows * 1e3:.1f} ms, transpose copy {t_cols * 1e3:.1f} ms")
    assert t_rows > 0 and t_cols > 0


def main() -> None:
    broadcasting()
    layout()
    views_and_copies()
    floats()
    summation()
    variance()
    overflow()
    rolling()
    ewma_closed_form()
    timing()
    print("\nall assertions passed")


if __name__ == "__main__":
    main()
