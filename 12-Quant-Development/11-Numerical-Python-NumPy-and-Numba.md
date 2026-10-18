---
type: concept
track: [quant-research, quant-dev]
tier: core
status: solid
prereqs: []
est_hours: 3
sources: [Harris et al. - Array programming with NumPy - Nature 585 (2020), NumPy documentation - Broadcasting and Copies and views and numpy.sum notes (numpy.org), Numba documentation - A ~5 minute guide and Automatic parallelization and Performance tips (numba.readthedocs.io), Numba 0.59.0 release notes - removal of object mode fall-back, pandas 3.0.0 release notes - Copy-on-Write (January 2026), Python documentation - built-in sum changed in 3.12, Goldberg - What Every Computer Scientist Should Know About Floating-Point Arithmetic - ACM Computing Surveys 23(1) (1991), Higham - Accuracy and Stability of Numerical Algorithms 2nd ed (SIAM 2002) ch 2 and 4, Welford - Note on a Method for Calculating Corrected Sums of Squares and Products - Technometrics 4(3) (1962)]
---

# Numerical Python: NumPy, pandas and Numba

## TL;DR

- An ndarray is a raw buffer plus dtype, shape and strides; basic slicing returns a view of the same buffer, while fancy and boolean indexing always copy, and `np.shares_memory` settles any doubt.
- Vectorising moves the loop from the interpreter into compiled code over contiguous memory: a sum of squares over $10^6$ floats ran about 150 to 300 times faster with `np.dot` than with a Python loop on the author's machine (machine-dependent).
- Broadcasting aligns shapes from the right; each dimension must be equal or 1; use `keepdims=True` or `[:, None]` to make the intent explicit.
- Floating point is the main source of silent bugs: $0.1 + 0.2 \ne 0.3$, the one-pass variance formula can return a negative variance, sequential float32 accumulation of $10^7$ values is off by 8.79%, and fixed-width integers wrap without warning in arrays.
- Recursions with state (EWMA, path-dependent payoffs, order-book updates) do not vectorise safely; compile the loop with Numba's `@njit` or move it to C++.

## Learning objectives

- Vectorise correctly and understand memory layout, views and copies.
- Profile Python and move hot loops to Numba or C++.
- Apply broadcasting rules and predict result shapes and temporary memory.
- Choose summation and variance algorithms that do not lose precision, and pick dtypes that do not overflow.
- Recognise computations that cannot be vectorised safely and know the compiled alternatives.

## Core concepts

### The ndarray memory model

An ndarray is a pointer to a buffer, a dtype (bytes per element), a shape and strides (bytes to step along each axis).
Element $(i, j)$ lives at `base + i*strides[0] + j*strides[1]`.

| Array | Shape | Strides (bytes) | Contiguous |
| :--- | :--- | :--- | :--- |
| `np.zeros((1000, 1000))` (C order, float64) | (1000, 1000) | (8000, 8) | C |
| `np.zeros((1000, 1000), order="F")` | (1000, 1000) | (8, 8000) | F |
| `c.T` | (1000, 1000) | (8, 8000) | F (a view, no copy) |
| `c[:, ::2]` | (1000, 500) | (8000, 16) | neither |

C order makes the last axis contiguous, so row-wise reductions and copies stream through cache lines; F order (Fortran, also LAPACK's native layout) makes columns contiguous.
A transpose is free (it swaps strides), but the next operation that needs contiguous memory pays for the copy.
Halving precision halves memory: a $1000 \times 1000$ float32 array is 4,000,000 bytes, which matters more for bandwidth than for compute.

### Broadcasting

Two shapes are compatible if, aligned from the right, each pair of dimensions is equal or one of them is 1; the result takes the larger size along each axis and size-1 axes are virtually repeated with stride 0 (no copy of the input).

- `(3, 1) + (1, 4)` gives `(3, 4)`: an outer sum.
- Demeaning columns of a `(T, N)` panel: `r - r.mean(axis=0)` works because `(T, N)` and `(N,)` align on $N$.
- Demeaning rows: `r - r.mean(axis=1)` fails for $T \ne N$ ("operands could not be broadcast together"), and silently does the wrong thing when $T = N$; write `r - r.mean(axis=1, keepdims=True)`.
- Pairwise distances: `x[:, None, :] - x[None, :, :]` on a `(100, 3)` array materialises a `(100, 100, 3)` float64 temporary of 240,000 bytes; at $n = 10^5$ the same expression needs 240 GB, so chunk it or use a matrix identity.

### Views and copies

| Operation | Result | Shares memory |
| :--- | :--- | :--- |
| Basic slice `a[2:8:2]` | view | yes; writes go through to `a` |
| Fancy index `a[[1, 3, 5]]` | copy | no |
| Boolean mask `a[a > 5]` | copy | no |
| `m.reshape(4, 3)` on contiguous `m` | view | yes |
| `m.T.reshape(12)` | copy (strides cannot express it) | no |
| `m.ravel()` / `m.flatten()` | view if possible / always copy | yes / no |
| `x += 1` / `x = x + 1` | in place / new array | same buffer / new buffer |

Two consequences: writing to a slice of a shared array mutates the caller's data, and an innocent-looking reshape or mask inside a hot loop allocates.
In pandas 2.x the same ambiguity produces `SettingWithCopyWarning`; pandas 3.0 (January 2026) makes Copy-on-Write the only behaviour, so every derived object acts as a copy and `SettingWithCopyWarning` is gone: chained assignment such as `df[mask]["b"] = 0` never writes to `df` (pandas warns with `ChainedAssignmentError`), and the fix is one `df.loc[mask, "b"] = 0`.

### Floating point in one table

IEEE 754 binary64 has a 53-bit significand, so machine epsilon (the gap from 1 to the next double) is $2^{-52} \approx 2.22 \times 10^{-16}$; binary32 has a 24-bit significand and epsilon $2^{-23} \approx 1.19 \times 10^{-7}$.

| Fact | Value |
| :--- | :--- |
| `0.1 + 0.2` | `0.30000000000000004`, which exceeds `0.3` by $2^{-54} \approx 5.55 \times 10^{-17}$ |
| Largest integer range exact in float64 | up to $2^{53}$; `float64(2**53 + 1)` is `2**53` |
| Largest integer range exact in float32 | up to $2^{24}$; `float32(16777217)` is `16777216` |
| `float32(123456.78)` | `123456.78125`, off by 0.00125: 123,456.78 lies between 65,536 and 131,072, where the float32 spacing is $1/128 = 0.0078125$; from 131,072 upward it is $1/64 = 0.015625$, so neighbouring cent prices collide |
| `(1e16 + 1) - 1e16` in float64 | `0.0`: the ulp of $10^{16}$ is 2, so adding 1 is a tie that rounds to even |

Compare floats with a tolerance: `math.isclose(a, b, rel_tol=1e-9, abs_tol=...)` or `np.isclose`, and choose the absolute tolerance from the problem's units (see [Testing Trading and Numerical Code](14-Testing-Trading-and-Numerical-Code.md)).
Represent prices as integers in the venue's tick units (ITCH uses 4 implied decimals) and convert to float only for analytics.

### Summation and variance

With unit roundoff $u = \epsilon/2 = 2^{-53}$ and relative to $\sum|x_i|$, naive sequential summation of $n$ terms has a worst-case error bound of about $(n-1)u$, pairwise summation about $u\log_2 n$, and compensated (Kahan) summation $2u + O(nu^2)$, independent of $n$ while $nu \ll 1$; `math.fsum` is correctly rounded (Higham, *Accuracy and Stability of Numerical Algorithms*, chapter 4).
The NumPy documentation for `numpy.sum` notes that it uses partial pairwise summation for floating-point input (always when no axis is given), whereas `np.cumsum` is strictly sequential.
Python's built-in `sum()` has used a compensated (Neumaier) algorithm for floats since Python 3.12, so `sum([0.1] * 10)` is exactly `1.0` while an explicit `+=` loop gives `0.9999999999999999`: a hand-written loop and `sum()` no longer agree.

The one-pass variance $\frac{1}{n-1}(\sum x^2 - (\sum x)^2/n)$ subtracts two nearly equal large numbers when the mean is large relative to the spread, which is the normal case for prices.
Welford's update keeps a running mean and a running sum of squared deviations:

$$
\delta = x_k - \bar{x}_{k-1}, \qquad \bar{x}_k = \bar{x}_{k-1} + \frac{\delta}{k}, \qquad M_k = M_{k-1} + \delta\,(x_k - \bar{x}_k),
$$

with sample variance $M_n/(n-1)$; it is stable and streams (one pass, $O(1)$ memory), which is why it is the standard for online risk and market-data statistics.

### Integer dtypes

NumPy integer arrays wrap modulo $2^{\text{bits}}$ silently (NumPy scalars emit a `RuntimeWarning`, arrays do not).
Notional in ITCH Price(4) units times shares overflows int32 almost immediately: \$250.0000 is 2,500,000 units, and times 1,000 shares is $2.5 \times 10^9 > 2^{31} - 1$.
Unsigned subtraction is worse: `uint32(3) - uint32(5)` is 4,294,967,294, so never store differences (sizes, sequence gaps, PnL) in unsigned types.

### Vectorisation patterns quants use

- Prefix sums: `np.cumsum` for rolling sums and means (fast, but differences of large running totals lose precision on long series).
- Running extrema: `np.maximum.accumulate` for drawdowns and trailing stops.
- Windows: `numpy.lib.stride_tricks.sliding_window_view` returns a read-only strided view `(n - w + 1, w)` with no copy; reductions over it cost $O(nw)$ but stay in C.
- Search: `np.searchsorted` for as-of joins and bucketing ([Tick Data Storage](12-Tick-Data-Storage-and-Time-Series-Databases.md)).
- Masks and `np.where` instead of `if` inside loops; `np.add.at` for unbuffered scatter-add when indices repeat.

### When vectorisation is the wrong tool

A linear recursion like the EWMA $y_t = (1-\alpha)y_{t-1} + \alpha x_t$ has a closed form,

$$
y_t = (1-\alpha)^t\Big[y_0 + \alpha\sum_{s=1}^{t} x_s(1-\alpha)^{-s}\Big],
$$

which vectorises with `cumsum` but needs $(1-\alpha)^{-s}$, which overflows float64 once $s > \ln(\text{DBL\_MAX})/(-\ln(1-\alpha))$.
For a 1,000-point series the closed form matches the loop to within $10^{-9}$; for a 10,000-point series it returns non-finite values.
Nonlinear, branching or stateful loops (barrier monitoring with early exit, order-book updates, inventory-dependent quoting) have no closed form at all.
The options, in order of effort:

- a library routine that already implements the recursion in C (for linear filters, `scipy.signal.lfilter`);
- Numba, compiling the plain Python loop;
- Cython or C++ through pybind11 when the code must be shared with a C++ trading system.

### Numba

Numba (not installed in this repo's environment, so nothing here is run) is a just-in-time compiler that translates a subset of Python and NumPy into machine code through LLVM.
`@njit` (equivalently `@jit(nopython=True)`) compiles in nopython mode, where the function must not touch Python objects; compilation happens on the first call for each new combination of argument types, so the first call is slow and later calls run at compiled speed.
Since Numba 0.59 plain `@jit` also defaults to nopython mode and the old silent fall-back to object mode is removed, so code Numba cannot type fails with a `TypingError` instead of quietly running at interpreter speed.
Passing explicit signatures (`@njit("float64[:](float64[:], float64)")`) compiles eagerly at decoration time and rejects other argument types.
The options that matter in practice:

- `cache=True` writes the compiled code to disk so later processes skip recompilation.
- `parallel=True` with `numba.prange` parallelises loops whose iterations are independent (and recognised reductions such as `acc += ...`).
- `nogil=True` releases the GIL inside the compiled function, so ordinary Python threads can run it concurrently.
- `fastmath=True` turns on LLVM fast-math flags, including reassociation: a sum loop that must otherwise accumulate in strict order can be vectorised with SIMD, but the result changes in the last bits, NaN and infinity handling is no longer guaranteed, and compensated algorithms such as Kahan summation can be optimised away.
Supported: scalar arithmetic, loops, NumPy arrays and many NumPy functions, tuples and typed containers; unsupported: arbitrary Python objects, most of pandas, and most third-party libraries.

```python
import numpy as np
from numba import njit

@njit(cache=True)
def ewma(x, alpha):
    y = np.empty_like(x)
    acc = x[0]
    for i in range(x.shape[0]):
        acc = x[i] if i == 0 else (1.0 - alpha) * acc + alpha * x[i]
        y[i] = acc
    return y
```

The loop body is the same as the reference Python loop in [numpy_numerics.py](code/python/numpy_numerics.py), which is the point: one readable loop, compiled, instead of an unstable closed form.

### Profiling before optimising

- `timeit` (or `time.perf_counter` with the best of several repeats) for micro-benchmarks; report the machine and treat numbers as machine-dependent.
- `cProfile` for where time goes by function; a sampling profiler such as py-spy for production processes; line_profiler for line-level hot spots.
- Measure allocations too: many "slow vectorised" programs are dominated by temporaries, which `out=` arguments and in-place operators remove.

## Worked examples

Every number below is printed and asserted by [numpy_numerics.py](code/python/numpy_numerics.py) unless it is marked as a machine-dependent timing.

### 1. Summing ten million 0.1s in float32

"What does `np.full(10**7, 0.1, dtype=np.float32)` sum to?"
The stored value is $\text{float32}(0.1) \approx 0.100000001490116$, so the exact sum of the stored values is $1000000.0149$.
Sequential accumulation (`np.cumsum(x)[-1]`) returns $1087937.0$, an error of 8.79%: once the running total is large, each added 0.1 is rounded to a multiple of the total's ulp.
`np.sum` (pairwise) printed $1000000.1250$ here; the exact blocking differs by platform and NumPy version, so the script asserts only that its relative error is below 0.01%.
For float64 data uniform with standard deviation $10^6$ and $n = 10^6$, a Python loop is off from `math.fsum` by about $8.1 \times 10^{-6}$ and `np.sum` is at least as accurate.

### 2. Negative variance

"Data $10^9 + \{4, 7, 13, 16\}$: what is the sample variance?"
Deviations from the mean $10^9 + 10$ are $-6, -3, 3, 6$, so the variance is $90/3 = 30$.
The one-pass formula returns $-170.67$ in float64, because $\sum x^2 \approx 4.0 \times 10^{18}$ has an ulp of 512 while the quantity it must resolve, the sum of squared deviations, is 90.
Welford returns exactly $30.0$, as does the two-pass `np.var(data, ddof=1)`.

### 3. Overflowing notional

Price \$250.0000 is 2,500,000 in Price(4) units; times 1,000 shares in int32 gives $-1{,}794{,}967{,}296$ instead of $2{,}500{,}000{,}000$, which is exactly $2^{32}$ less.
Casting either operand to int64 before multiplying fixes it.

### 4. Rolling means three ways

For a window of 20 on 10,000 standard normals, the cumsum difference and `sliding_window_view(x, 20).mean(axis=1)` both agree with a Python loop to better than $10^{-14}$, and the window view shares memory with `x`.
On a series around $10^8$ of length $10^6$, the cumsum version's window means over the last 2,000 windows are off by a median of about $6.6 \times 10^{-4}$ (90th percentile about $1.6 \times 10^{-3}$), while a direct window mean is off by a few ulps of $10^8$ (one ulp is about $1.5 \times 10^{-8}$): prefix-sum differences inherit the rounding error of a running total near $10^{14}$.
That matches theory: the running total's ulp there is $2^{-6}$, each of the 20 additions inside a window rounds by up to half of it, so the window mean's error has standard deviation $2^{-6}\sqrt{20/12}/20 \approx 1.0 \times 10^{-3}$ and median absolute value $0.674$ times that, about $6.8 \times 10^{-4}$.

### 5. When the closed form overflows

For $\alpha = 0.1$, $(0.9)^{-s}$ exceeds the largest double once $s > 6736.7$.
On a 10,000-point series the vectorised closed form returns 3,265 non-finite values, while the loop is fine; this is exactly the loop to hand to Numba.

### 6. Drawdown without a loop

PnL path $[0, 3, 1, 4, -2, 5, 2]$: running peak $[0, 3, 3, 4, 4, 5, 5]$, so the maximum drawdown is $4 - (-2) = 6$, computed as `(np.maximum.accumulate(p) - p).max()`.

### 7. Timings (machine-dependent)

On the author's laptop (Apple silicon, NumPy 2.5), the sum of squares of $10^6$ floats took about 18 to 35 ms as a Python generator expression and about 0.1 ms as `np.dot`, a ratio between about 150 and 300 across runs; copying a $2000 \times 2000$ float64 array took about 1 ms contiguous and about 3.5 ms when transposing.
The script asserts only that the vectorised version is at least 3 times faster, so it passes on slow shared CI machines.

## Pitfalls

- Assuming a slice is a copy and mutating it, or assuming a mask result is a view and expecting writes to propagate.
- Broadcasting a `(T,)` row statistic against a square `(T, T)` matrix along the wrong axis: no error, wrong answer.
- Creating huge temporaries with broadcasting (`(n, n, k)` distance tensors) instead of chunking.
- Using float32 for prices, PnL or long accumulations to save memory.
- Computing variance or covariance with $E[x^2] - E[x]^2$ on un-centred data.
- Storing sizes, sequence numbers or differences in unsigned or 32-bit integers.
- Comparing floats with `==`, or with a relative tolerance alone when the expected value can be zero.
- Long-horizon rolling statistics from cumsum differences without re-anchoring.
- Benchmarking the first call of a JIT-compiled function (it includes compilation) or timing a single run.
- Reaching for Numba or C++ before profiling shows that the loop is the bottleneck.

## Interview questions

> [!question]- qd-np-ndarray-anatomy | What is an ndarray, physically?
> A pointer to a contiguous buffer plus dtype, shape and strides (bytes per step along each axis). Element $(i, j)$ is at base + $i\cdot$strides[0] + $j\cdot$strides[1]; views are new headers over the same buffer.

> [!question]- qd-np-strides-c-f | What are the strides of a C-order and an F-order $1000 \times 1000$ float64 array, and of the transpose of the C-order one?
> C order (8000, 8), F order (8, 8000), and the transpose (8, 8000): transposing swaps strides without copying, so the transpose is F-contiguous.

> [!question]- qd-np-broadcast-rule | State the broadcasting rule and the result shape of `(3, 1) + (1, 4)`.
> Align shapes from the right; each dimension pair must be equal or one of them 1; the result takes the larger. `(3, 1) + (1, 4)` is `(3, 4)`.

> [!question]- qd-np-demean-rows | Why does `r - r.mean(axis=1)` fail for a `(250, 5)` array, and what is the fix?
> `(250, 5)` and `(250,)` align on the last axis (5 vs 250) and are incompatible. Use `r.mean(axis=1, keepdims=True)` (shape `(250, 1)`). For a square array it would not fail, it would silently subtract along the wrong axis.

> [!question]- qd-np-view-or-copy | Which of these share memory with `a`: `a[2:8:2]`, `a[[1, 3, 5]]`, `a[a > 5]`, `a.reshape(...)`?
> The basic slice always; fancy and boolean indexing never (they copy); reshape shares when the strides can express the new shape (contiguous input) and copies otherwise. Check with `np.shares_memory`.

> [!question]- qd-np-inplace | What is the difference between `x += 1` and `x = x + 1` for an ndarray?
> `x += 1` writes into the existing buffer, so every view of it sees the change and no allocation happens. `x = x + 1` allocates a new array and rebinds the name; other references still see the old data.

> [!question]- qd-np-point-one | Why is `0.1 + 0.2 != 0.3` in binary64, and by how much do they differ?
> Neither 0.1 nor 0.2 is representable; the rounded sum is `0.30000000000000004`, which exceeds the double nearest 0.3 by $2^{-54} \approx 5.55 \times 10^{-17}$. Compare with a tolerance.

> [!question]- qd-np-eps | What are the machine epsilons of float64 and float32, and the largest range of exactly representable integers?
> $2^{-52} \approx 2.22 \times 10^{-16}$ and $2^{-23} \approx 1.19 \times 10^{-7}$; integers are exact up to $2^{53}$ and $2^{24}$ respectively, so `float32(16777217)` is 16777216.

> [!question]- qd-np-float32-sum | You accumulate ten million float32 copies of 0.1 sequentially. Roughly what do you get, and why?
> About 1,087,937 instead of about 1,000,000 (an error of 8.79%). As the running total grows its ulp grows, and each added 0.1 is rounded to a multiple of that ulp. Pairwise summation (`np.sum`), float64 accumulation or `math.fsum` fixes it.

> [!question]- qd-np-sum-error-orders | Compare the error growth of sequential, pairwise and compensated summation.
> Worst-case bounds relative to $\sum|x_i|$, with unit roundoff $u = 2^{-53}$: sequential about $(n-1)u$, pairwise about $u\log_2 n$, Kahan $2u + O(nu^2)$, independent of $n$ while $nu \ll 1$. `math.fsum` is correctly rounded.

> [!question]- qd-np-negative-variance | The one-pass formula gives a sample variance of $-170.67$ for $10^9 + \{4, 7, 13, 16\}$. What is the true value and the fix?
> $30$. Catastrophic cancellation: $\sum x^2$ is about $4 \times 10^{18}$ with an ulp of 512, larger than the true difference 90. Use Welford's online update or a two-pass centred formula.

> [!question]- qd-np-welford | Write Welford's update.
> $\delta = x_k - \bar{x}_{k-1}$, $\bar{x}_k = \bar{x}_{k-1} + \delta/k$, $M_k = M_{k-1} + \delta(x_k - \bar{x}_k)$; variance $M_n/(n-1)$. One pass, $O(1)$ memory, numerically stable.

> [!question]- qd-np-int32-notional | A price of \$250.0000 stored as 2,500,000 (four implied decimals) is multiplied by 1,000 shares in int32. What do you get?
> $-1{,}794{,}967{,}296$, which is $2.5 \times 10^9 - 2^{32}$. NumPy arrays wrap silently; cast to int64 before multiplying.

> [!question]- qd-np-uint-diff | Why should sequence gaps and position changes never be stored in unsigned integers?
> Differences can be negative and unsigned arithmetic wraps: `uint32(3) - uint32(5)` is 4,294,967,294, which looks like a huge gap or position instead of an error.

> [!question]- qd-np-cumsum-rolling | What is the trade-off of computing rolling means as differences of a cumsum?
> It is $O(n)$ regardless of window, but each output is a difference of two large running totals, so the absolute error grows with the total: on a long series near $10^8$ it was about $6.6 \times 10^{-4}$ (median over the last 2,000 windows, in line with the theory value $u\sqrt{w/12}/w$ for a total whose ulp is $u$) versus a few ulps of $10^8$ (one ulp is about $1.5 \times 10^{-8}$) for a direct window mean. Re-anchor periodically or use a windowed reduction.

> [!question]- qd-np-sliding-window | What does `sliding_window_view(x, w)` return and what does it cost?
> A read-only strided view of shape `(n - w + 1, w)` that shares memory with `x` (no copy). Reductions over it cost $O(nw)$ arithmetic but run in compiled code.

> [!question]- qd-np-ewma-closed-form | Why can the vectorised closed form of an EWMA break on long series?
> It needs $(1-\alpha)^{-s}$, which overflows float64 once $s > \ln(\text{DBL\_MAX})/(-\ln(1-\alpha))$, about 6,737 for $\alpha = 0.1$. A compiled loop (Numba, C++) or a C filter routine is the robust choice.

> [!question]- qd-np-numba-basics | What does `@njit(cache=True)` do, and what does the first call cost?
> Numba compiles the function in nopython mode to machine code through LLVM for the argument types seen at the first call; `cache=True` stores the compiled code on disk for later processes. The first call includes compilation, so never benchmark it.

> [!question]- qd-np-numba-limits | When is Numba the wrong choice?
> When the code uses arbitrary Python objects, pandas or third-party libraries (nopython mode does not support them), when the logic must be shared with a C++ production system, or when the bottleneck is I/O or memory bandwidth rather than interpreter overhead.

> [!question]- qd-np-numba-fastmath | What does `fastmath=True` buy in Numba, and when must you not use it?
> It enables LLVM fast-math flags, chiefly reassociation, so a strict-order sum loop can be vectorised with SIMD (often a large speed-up for reductions). Do not use it where the exact operation order matters: compensated (Kahan) summation can be simplified away, NaN and infinity checks may be removed, and results change in the last bits, which breaks bit-exact regression tests.

> [!question]- qd-np-numba-nopython-default | A colleague says "`@jit` falls back to object mode if it cannot compile, so it is always safe to add". Is that true today?
> No. Since Numba 0.59 the object-mode fall-back is removed and `@jit` defaults to nopython mode, so an untypeable function raises a `TypingError` at its first call. Before 0.59 the fall-back silently ran the function at interpreter speed, which hid the fact that nothing had been compiled.

> [!question]- qd-np-builtin-sum | In Python 3.12 or later, `sum([0.1] * 10) == 1.0` is `True`, but an explicit `t += x` loop over the same list gives `0.9999999999999999`. Why?
> Since Python 3.12 the built-in `sum()` uses compensated (Neumaier) summation for floats, while the loop rounds after every addition. Do not assume a hand-written loop, `sum()`, `np.sum` (pairwise) and `math.fsum` (correctly rounded) agree to the last bit.

> [!question]- qd-np-drawdown | How do you compute the maximum drawdown of a PnL path without a Python loop?
> `(np.maximum.accumulate(p) - p).max()`. For $[0, 3, 1, 4, -2, 5, 2]$ the running peak is $[0, 3, 3, 4, 4, 5, 5]$ and the maximum drawdown is 6.

> [!question]- qd-np-broadcast-memory | How much memory does `x[:, None, :] - x[None, :, :]` need for a `(100000, 3)` float64 array?
> $10^5 \times 10^5 \times 3 \times 8 = 2.4 \times 10^{11}$ bytes (240 GB) for the temporary; at $n = 100$ it is 240,000 bytes. Chunk the rows or use $\lVert a - b\rVert^2 = \lVert a\rVert^2 + \lVert b\rVert^2 - 2a\cdot b$.

## In this repo and SDE-Interview-Prep

- Code: [numpy_numerics.py](code/python/numpy_numerics.py), run with `uv run --no-project --with numpy python 12-Quant-Development/code/python/numpy_numerics.py`.
- Code: [benchmarking_python.ipynb](code/python/benchmarking_python.ipynb).
- As-of joins with `searchsorted`: [Tick Data Storage and Time-Series Databases](12-Tick-Data-Storage-and-Time-Series-Databases.md); tolerance design for numerical tests: [Testing Trading and Numerical Code](14-Testing-Trading-and-Numerical-Code.md).
- [Ultimate Python advanced guide (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/Python/Ultimate-Python-Advanced-Guide.md)

## Further reading

- Charles R. Harris et al., "Array programming with NumPy", *Nature* 585, 357-362 (2020).
- NumPy documentation: "Broadcasting", "Copies and views", and the notes to `numpy.sum` on pairwise summation (numpy.org/doc).
- Numba documentation: "A ~5 minute guide to Numba" and "Automatic parallelization with @jit" (numba.readthedocs.io).
- Numba 0.59.0 release notes (object-mode fall-back removed, `nopython=True` the default) and the "Performance Tips" page on `fastmath`.
- pandas 3.0.0 release notes, "What's new in 3.0.0" (January 21, 2026): Copy-on-Write and the removal of `SettingWithCopyWarning`.
- David Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic", *ACM Computing Surveys* 23(1) (1991).
- Nicholas J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd edition (SIAM, 2002), chapter 2 (floating point) and chapter 4 (summation).
- B. P. Welford, "Note on a Method for Calculating Corrected Sums of Squares and Products", *Technometrics* 4(3) (1962).
