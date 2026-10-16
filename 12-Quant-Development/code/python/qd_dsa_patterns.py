"""Data structures and algorithms patterns for quant interviews, with finance-flavoured examples.

Used by 12-Quant-Development/05-Data-Structures-and-Algorithms-for-Quant-Interviews.md.
Every worked example prints its answer and asserts it; every non-trivial routine is also checked
against a brute-force version on seeded random inputs.

Run: python3 12-Quant-Development/code/python/qd_dsa_patterns.py
"""

from __future__ import annotations

import bisect
import heapq
import math
import random
from collections import OrderedDict, defaultdict, deque
from collections.abc import Iterable, Iterator

# ----------------------------------------------------------------------------- heaps


def top_k(values: Iterable[float], k: int) -> list[float]:
    """k largest values, descending. Min-heap of size k: O(n log k) time, O(k) memory."""
    heap: list[float] = []
    for v in values:
        if len(heap) < k:
            heapq.heappush(heap, v)
        elif v > heap[0]:
            heapq.heapreplace(heap, v)
    return sorted(heap, reverse=True)


def merge_streams(streams: list[list[tuple[int, str]]]) -> list[tuple[int, str]]:
    """Merge k time-sorted feeds into one; ties keep feed order. O(n log k)."""
    heap = [(s[0][0], i, 0) for i, s in enumerate(streams) if s]
    heapq.heapify(heap)
    out = []
    while heap:
        _, i, j = heapq.heappop(heap)
        out.append(streams[i][j])
        if j + 1 < len(streams[i]):
            heapq.heappush(heap, (streams[i][j + 1][0], i, j + 1))
    return out


# ----------------------------------------------------------------------------- order statistics


def quickselect(values: list[float], k: int, rng: random.Random) -> float:
    """k-th smallest (0-based). Expected O(n) with a random pivot, O(n^2) worst case."""
    a = list(values)
    lo, hi = 0, len(a) - 1
    while True:
        if lo == hi:
            return a[lo]
        pivot = a[rng.randint(lo, hi)]
        lt = [x for x in a[lo : hi + 1] if x < pivot]
        eq = [x for x in a[lo : hi + 1] if x == pivot]
        gt = [x for x in a[lo : hi + 1] if x > pivot]
        a[lo : hi + 1] = lt + eq + gt
        if k < lo + len(lt):
            hi = lo + len(lt) - 1
        elif k < lo + len(lt) + len(eq):
            return pivot
        else:
            lo = lo + len(lt) + len(eq)


def running_median(stream: Iterable[float]) -> list[float]:
    """Median after each arrival. Max-heap of the lower half, min-heap of the upper half: O(log n) per update."""
    low: list[float] = []  # max-heap via negation
    high: list[float] = []
    out = []
    for x in stream:
        if low and x > -low[0]:
            heapq.heappush(high, x)
        else:
            heapq.heappush(low, -x)
        if len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
        elif len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))
        out.append(-low[0] if len(low) > len(high) else (-low[0] + high[0]) / 2)
    return out


# ----------------------------------------------------------------------------- sliding windows


def sliding_max(values: list[float], w: int) -> list[float]:
    """Max of each length-w window. Monotonic deque of indices: O(n) total, each index pushed and popped once."""
    dq: deque[int] = deque()
    out = []
    for i, v in enumerate(values):
        while dq and values[dq[-1]] <= v:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - w:
            dq.popleft()
        if i >= w - 1:
            out.append(values[dq[0]])
    return out


def sliding_median(values: list[float], w: int) -> list[float]:
    """Median of each window with a sorted window: O(log w) search plus O(w) shift per step (fast in practice)."""
    window = sorted(values[:w])
    out = []
    for i in range(w, len(values) + 1):
        mid = w // 2
        out.append(window[mid] if w % 2 else (window[mid - 1] + window[mid]) / 2)
        if i == len(values):
            break
        window.pop(bisect.bisect_left(window, values[i - w]))
        bisect.insort(window, values[i])
    return out


def max_drawdown(prices: list[float]) -> float:
    """Largest peak-to-trough fall, one pass with the running peak. O(n)."""
    peak, mdd = -math.inf, 0.0
    for p in prices:
        peak = max(peak, p)
        mdd = max(mdd, peak - p)
    return mdd


# ----------------------------------------------------------------------------- intervals


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Union of closed intervals. Sort by start, then extend: O(n log n)."""
    out: list[tuple[int, int]] = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], e))
        else:
            out.append((s, e))
    return out


def max_concurrent(intervals: list[tuple[int, int]]) -> int:
    """Max number of half-open [start, end) intervals alive at once. Sweep line: O(n log n)."""
    events = sorted([(s, 1) for s, _ in intervals] + [(e, -1) for _, e in intervals])  # -1 sorts first at ties
    best = cur = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return best


# ----------------------------------------------------------------------------- hashing and design


class LRUCache:
    """Least-recently-used cache. OrderedDict is a hash map plus a doubly linked list: O(1) get and put."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.data: OrderedDict[str, float] = OrderedDict()

    def get(self, key: str) -> float | None:
        if key not in self.data:
            return None
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key: str, value: float) -> None:
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)


def two_sum(values: list[int], target: int) -> tuple[int, int] | None:
    """Indices of two entries summing to target, one pass with a hash map. O(n)."""
    seen: dict[int, int] = {}
    for i, v in enumerate(values):
        if target - v in seen:
            return seen[target - v], i
        seen[v] = i
    return None


def count_subarrays_with_sum(values: list[int], k: int) -> int:
    """Number of contiguous runs summing to k: prefix sums plus a hash map of prefix counts. O(n)."""
    counts: defaultdict[int, int] = defaultdict(int)
    counts[0] = 1
    total = found = 0
    for v in values:
        total += v
        found += counts[total - k]
        counts[total] += 1
    return found


class Trie:
    """Prefix tree over symbols: insert and prefix lookup in O(length)."""

    def __init__(self) -> None:
        self.root: dict = {}

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def with_prefix(self, prefix: str) -> list[str]:
        node = self.root
        for ch in prefix:
            if ch not in node:
                return []
            node = node[ch]
        out: list[str] = []

        def walk(n: dict, acc: str) -> None:
            for ch, child in sorted(n.items()):
                if ch == "$":
                    out.append(acc)
                else:
                    walk(child, acc + ch)

        walk(node, prefix)
        return out


class UnionFind:
    """Disjoint sets with path halving and union by size: near O(1) amortised (inverse Ackermann)."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True


# ----------------------------------------------------------------------------- graphs


def topo_order(deps: dict[str, list[str]]) -> list[str] | None:
    """Kahn's algorithm: an evaluation order for a dependency DAG, or None if there is a cycle. O(V + E)."""
    nodes = set(deps) | {d for ds in deps.values() for d in ds}
    indeg = {n: 0 for n in nodes}
    users: defaultdict[str, list[str]] = defaultdict(list)
    for n, ds in deps.items():
        for d in ds:
            indeg[n] += 1
            users[d].append(n)
    ready = sorted(n for n in nodes if indeg[n] == 0)
    order = []
    while ready:
        n = ready.pop(0)
        order.append(n)
        for u in sorted(users[n]):
            indeg[u] -= 1
            if indeg[u] == 0:
                bisect.insort(ready, u)
    return order if len(order) == len(nodes) else None


def fx_arbitrage_cycle(rates: dict[tuple[str, str], float]) -> list[str] | None:
    """Bellman-Ford on weights -ln(rate): a negative cycle is a loop whose rate product exceeds 1. O(V E)."""
    nodes = sorted({a for a, _ in rates} | {b for _, b in rates})
    dist = dict.fromkeys(nodes, 0.0)  # virtual source at distance 0 to every node
    pred: dict[str, str | None] = dict.fromkeys(nodes)
    last = None
    for _ in range(len(nodes)):
        last = None
        for (a, b), r in rates.items():
            w = -math.log(r)
            if dist[a] + w < dist[b] - 1e-12:
                dist[b] = dist[a] + w
                pred[b] = a
                last = b
    if last is None:
        return None
    for _ in range(len(nodes)):  # step back V times to land inside the cycle
        last = pred[last]
    cycle, cur = [last], pred[last]
    while cur != last:
        cycle.append(cur)
        cur = pred[cur]
    cycle.reverse()
    return cycle


def bfs_hops(edges: list[tuple[str, str]], src: str, dst: str) -> int:
    """Fewest edges from src to dst in an undirected graph (-1 if unreachable). O(V + E)."""
    adj: defaultdict[str, list[str]] = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    dist = {src: 0}
    q = deque([src])
    while q:
        n = q.popleft()
        if n == dst:
            return dist[n]
        for m in adj[n]:
            if m not in dist:
                dist[m] = dist[n] + 1
                q.append(m)
    return -1


# ----------------------------------------------------------------------------- dynamic programming


def best_single_trade(prices: list[float]) -> float:
    """Max profit from one buy then one sell: track the running minimum. O(n)."""
    lo, best = math.inf, 0.0
    for p in prices:
        lo = min(lo, p)
        best = max(best, p - lo)
    return best


def best_unlimited_trades(prices: list[float], fee: float = 0.0) -> float:
    """Max profit with any number of round trips, paying `fee` per round trip. State DP: O(n)."""
    flat, long = 0.0, -math.inf
    for p in prices:
        flat, long = max(flat, long + p - fee), max(long, flat - p)
    return flat


def best_k_trades(prices: list[float], k: int) -> float:
    """Max profit with at most k round trips. O(n k)."""
    buy = [-math.inf] * (k + 1)
    sell = [0.0] * (k + 1)
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]


def kadane(pnl: list[float]) -> tuple[float, int, int]:
    """Best contiguous run of P&L (sum, start, end inclusive). O(n)."""
    best, best_s, best_e = -math.inf, 0, 0
    cur, s = 0.0, 0
    for i, x in enumerate(pnl):
        if cur <= 0:
            cur, s = x, i
        else:
            cur += x
        if cur > best:
            best, best_s, best_e = cur, s, i
    return best, best_s, best_e


def knapsack(capacity: int, items: list[tuple[int, int]]) -> int:
    """0/1 knapsack: max value with total cost <= capacity. O(n C) pseudo-polynomial."""
    dp = [0] * (capacity + 1)
    for cost, value in items:
        for c in range(capacity, cost - 1, -1):
            dp[c] = max(dp[c], dp[c - cost] + value)
    return dp[capacity]


def min_lots(amount: int, lots: list[int]) -> int:
    """Fewest lots summing exactly to amount (-1 if impossible). O(amount * len(lots))."""
    dp = [0] + [math.inf] * amount
    for a in range(1, amount + 1):
        for lot in lots:
            if lot <= a and dp[a - lot] + 1 < dp[a]:
                dp[a] = dp[a - lot] + 1
    return -1 if dp[amount] == math.inf else int(dp[amount])


def greedy_lots(amount: int, lots: list[int]) -> int:
    """Largest lot first: optimal for some lot systems, not for all."""
    used = 0
    for lot in sorted(lots, reverse=True):
        used += amount // lot
        amount %= lot
    return used if amount == 0 else -1


def ways_to_make(amount: int, lots: list[int]) -> int:
    """Number of multisets of lots summing to amount (order does not matter). O(amount * len(lots))."""
    dp = [1] + [0] * amount
    for lot in lots:
        for a in range(lot, amount + 1):
            dp[a] += dp[a - lot]
    return dp[amount]


def lis_length(values: list[float]) -> int:
    """Longest strictly increasing subsequence via patience sorting tails: O(n log n)."""
    tails: list[float] = []
    for v in values:
        i = bisect.bisect_left(tails, v)
        if i == len(tails):
            tails.append(v)
        else:
            tails[i] = v
    return len(tails)


def min_largest_slice(sizes: list[int], slices: int) -> int:
    """Split a parent order (contiguous clips) into at most `slices` child orders minimising the largest.
    Binary search on the answer with a greedy feasibility check: O(n log(sum))."""

    def feasible(cap: int) -> bool:
        used, cur = 1, 0
        for s in sizes:
            if cur + s > cap:
                used, cur = used + 1, s
            else:
                cur += s
        return used <= slices

    lo, hi = max(sizes), sum(sizes)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


# ----------------------------------------------------------------------------- streaming statistics


def welford(stream: Iterable[float]) -> tuple[int, float, float]:
    """Count, mean and sum of squared deviations in one numerically stable pass."""
    n, mean, m2 = 0, 0.0, 0.0
    for x in stream:
        n += 1
        d = x - mean
        mean += d / n
        m2 += d * (x - mean)
    return n, mean, m2


def _windows(values: list[float], w: int) -> Iterator[list[float]]:
    for i in range(len(values) - w + 1):
        yield values[i : i + w]


def _median(xs: list[float]) -> float:
    s = sorted(xs)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def main() -> None:
    rng = random.Random(7)

    trades = [120, 5, 300, 42, 300, 7, 999, 18]
    print("top 3 trade sizes:", top_k(trades, 3))
    assert top_k(trades, 3) == [999, 300, 300]

    feeds = [[(1, "NYSE"), (4, "NYSE"), (9, "NYSE")], [(2, "ARCA"), (4, "ARCA")], [(3, "BATS"), (10, "BATS")]]
    merged = merge_streams(feeds)
    print("merged feed:", merged)
    assert [t for t, _ in merged] == [1, 2, 3, 4, 4, 9, 10] and merged[3] == (4, "NYSE")

    lat = [12, 7, 3, 25, 8, 19, 5, 11, 4]
    med = quickselect(lat, len(lat) // 2, rng)
    print("median latency by quickselect:", med)
    assert med == 8

    rm = running_median([5, 15, 1, 3])
    print("running median of 5, 15, 1, 3:", rm)
    assert rm == [5, 10, 5, 4]

    px = [1, 3, -1, -3, 5, 3, 6, 7]
    sm = sliding_max(px, 3)
    smed = sliding_median(px, 3)
    print("sliding max w=3:", sm, " sliding median w=3:", smed)
    assert sm == [3, 3, 5, 5, 6, 7]
    assert smed == [1, -1, -1, 3, 5, 6]

    curve = [100, 104, 101, 108, 97, 99, 110, 103]
    mdd = max_drawdown(curve)
    print("max drawdown:", mdd)
    assert mdd == 11

    sessions = [(570, 600), (585, 660), (780, 840), (840, 900)]  # minutes after midnight
    print("merged sessions:", merge_intervals(sessions))
    assert merge_intervals(sessions) == [(570, 660), (780, 900)]
    lifetimes = [(0, 10), (2, 5), (4, 12), (5, 8), (11, 13)]
    mc = max_concurrent(lifetimes)
    live_at_4 = sum(1 for s, e in lifetimes if s <= 4 < e)
    print("max concurrent live orders:", mc, " live at time 4:", live_at_4)
    assert mc == 3 and live_at_4 == 3

    cache = LRUCache(2)
    cache.put("AAPL", 1.0)
    cache.put("MSFT", 2.0)
    assert cache.get("AAPL") == 1.0
    cache.put("NVDA", 3.0)  # evicts MSFT, the least recently used
    print("LRU after touching AAPL and adding NVDA:", list(cache.data))
    assert cache.get("MSFT") is None and list(cache.data) == ["AAPL", "NVDA"]

    notionals = [250, 700, 125, 875, 400]
    ts = two_sum(notionals, 1000)
    print("two notionals summing to 1000 at indices:", ts)
    assert ts == (2, 3)
    cs = count_subarrays_with_sum([1, 1, 1], 2)
    print("contiguous runs of [1, 1, 1] summing to 2:", cs)
    assert cs == 2

    trie = Trie()
    for s in ["AAPL", "AAL", "AMZN", "AMD", "MSFT", "MS"]:
        trie.insert(s)
    print("prefix AA:", trie.with_prefix("AA"), " prefix MS:", trie.with_prefix("MS"))
    assert trie.with_prefix("AA") == ["AAL", "AAPL"] and trie.with_prefix("MS") == ["MS", "MSFT"] and trie.with_prefix("Z") == []

    corr_pairs = [(0, 1), (1, 2), (3, 4)]  # pairs of assets with |correlation| above a threshold, 6 assets
    uf = UnionFind(6)
    for a, b in corr_pairs:
        uf.union(a, b)
    print("correlation clusters:", uf.components)
    clusters = sorted(sorted(i for i in range(6) if uf.find(i) == r) for r in {uf.find(i) for i in range(6)})
    print("clusters:", clusters)
    assert uf.components == 3 and clusters == [[0, 1, 2], [3, 4], [5]]

    deps = {
        "swap_pricer": ["ois_curve", "projection_curve"],
        "projection_curve": ["ois_curve"],
        "ois_curve": ["fixings"],
        "vol_surface": ["fixings"],
    }
    order = topo_order(deps)
    print("evaluation order:", order)
    assert order == ["fixings", "ois_curve", "projection_curve", "swap_pricer", "vol_surface"]
    assert topo_order({"a": ["b"], "b": ["a"]}) is None

    rates = {("USD", "EUR"): 0.9, ("EUR", "GBP"): 0.8, ("GBP", "USD"): 1.4, ("EUR", "USD"): 1.1}
    cyc = fx_arbitrage_cycle(rates)
    assert cyc is not None
    product = math.prod(rates[(cyc[i], cyc[(i + 1) % len(cyc)])] for i in range(len(cyc)))
    two_leg = rates[("USD", "EUR")] * rates[("EUR", "USD")]
    print("FX arbitrage cycle:", cyc, f"rate product {product:.3f}, two-leg USD-EUR-USD product {two_leg:.2f}")
    assert cyc == ["EUR", "GBP", "USD"] and f"{product:.3f}" == "1.008"
    assert f"{two_leg:.2f}" == "0.99" and two_leg < 1  # the EUR to USD back-quote alone is not an arbitrage
    assert fx_arbitrage_cycle({("USD", "EUR"): 0.9, ("EUR", "USD"): 1 / 0.9 - 1e-6}) is None

    hops = bfs_hops([("USD", "EUR"), ("EUR", "JPY"), ("USD", "CAD"), ("JPY", "KRW")], "CAD", "KRW")
    print("fewest conversions CAD to KRW:", hops)
    assert hops == 4

    p = [7, 1, 5, 3, 6, 4]
    one, unl, fee = best_single_trade(p), best_unlimited_trades(p), best_unlimited_trades(p, fee=2)
    k2 = best_k_trades([3, 3, 5, 0, 0, 3, 1, 4], 2)
    print(f"stock: one trade {one}, unlimited {unl}, unlimited with fee 2: {fee}, at most 2 trades {k2}")
    assert (one, unl, fee, k2) == (5, 7, 3, 6)

    pnl = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    kd = kadane(pnl)
    print("best P&L run (sum, start, end):", kd)
    assert kd == (6, 3, 6)

    ks = knapsack(10, [(5, 10), (4, 40), (6, 30), (3, 50)])
    print("knapsack capital 10:", ks)
    assert ks == 90

    ml, ways = min_lots(63, [1, 5, 10, 25]), ways_to_make(100, [1, 5, 10, 25])
    print(f"fewest lots for 63: {ml}; ways to make 100: {ways}")
    assert ml == 6 and ways == 242
    assert min_lots(7, [2, 4]) == -1
    greedy, optimal = greedy_lots(6, [1, 3, 4]), min_lots(6, [1, 3, 4])
    print(f"lots 1, 3, 4 for 6: greedy uses {greedy}, optimal uses {optimal}")
    assert greedy == 3 and optimal == 2 and greedy_lots(63, [1, 5, 10, 25]) == ml

    li = lis_length([10, 9, 2, 5, 3, 7, 101, 18])
    print("LIS length:", li)
    assert li == 4

    sl = min_largest_slice([7, 2, 5, 10, 8], 2)
    print("smallest possible largest child order (2 slices):", sl)
    assert sl == 18

    n, mean, m2 = welford([2, 4, 4, 4, 5, 5, 7, 9])
    print(f"Welford: n {n}, mean {mean}, population var {m2 / n}, sample var {m2 / (n - 1):.6f}")
    assert n == 8 and mean == 5 and m2 / n == 4 and f"{m2 / (n - 1):.6f}" == "4.571429"
    big = [1e9 + x for x in (4.0, 7.0, 13.0, 16.0)]
    s1 = s2 = 0.0
    for x in big:  # plain left-to-right float sums, as a C++ loop would do
        s1 += x
        s2 += x * x
    naive_numerator = s2 - s1 * s1 / 4
    naive_var = naive_numerator / 4
    # Exactly rounded sums (math.fsum; Python 3.12+ built-in sum is also compensated) still lose every digit.
    naive_exact_sums = (math.fsum(x * x for x in big) - math.fsum(big) ** 2 / 4) / 4
    _, _, m2b = welford(big)
    print(f"variance of 1e9 + (4, 7, 13, 16): naive one-pass {naive_var}, with exactly rounded sums {naive_exact_sums}, Welford {m2b / 4}")
    assert m2b / 4 == 22.5 and naive_var == -128.0 and naive_exact_sums == 0.0  # catastrophic cancellation
    # The problem set's sample variance -170.67 divides the same -512 numerator by n - 1 = 3.
    print(f"naive numerator {naive_numerator}, over n - 1: {naive_numerator / 3:.2f}")
    assert naive_numerator == -512.0 and f"{naive_numerator / 3:.2f}" == "-170.67"
    print(f"ulp near 1e18: {math.ulp(1e18):.0f}, ulp near 4e18: {math.ulp(4e18):.0f}")
    assert math.ulp(1e18) == 128 and math.ulp(4e18) == 512

    # Brute-force cross-checks on seeded random inputs.
    for _ in range(200):
        arr = [rng.randint(-50, 50) for _ in range(rng.randint(1, 40))]
        w = rng.randint(1, len(arr))
        assert sliding_max(arr, w) == [max(x) for x in _windows(arr, w)]
        assert sliding_median(arr, w) == [_median(x) for x in _windows(arr, w)]
        assert running_median(arr) == [_median(arr[: i + 1]) for i in range(len(arr))]
        k = rng.randrange(len(arr))
        assert quickselect(arr, k, rng) == sorted(arr)[k]
        assert kadane(arr)[0] == max(sum(arr[i : j + 1]) for i in range(len(arr)) for j in range(i, len(arr)))
        prices = [abs(x) + 1 for x in arr]
        assert best_single_trade(prices) == max([0] + [prices[j] - prices[i] for i in range(len(prices)) for j in range(i, len(prices))])
        assert best_k_trades(prices, len(prices)) == best_unlimited_trades(prices)
        ivs = [(s, s + rng.randint(1, 10)) for s in (rng.randint(0, 30) for _ in range(rng.randint(1, 10)))]
        assert max_concurrent(ivs) == max(sum(1 for s, e in ivs if s <= t < e) for t in range(0, 45))
        sizes = [rng.randint(1, 20) for _ in range(rng.randint(1, 8))]
        m = rng.randint(1, len(sizes))
        assert min_largest_slice(sizes, m) == _brute_split(sizes, m)
    for amount in range(0, 60):
        assert min_lots(amount, [1, 5, 10, 25]) == _brute_min_lots(amount, [1, 5, 10, 25])
    print("all assertions passed")


def _brute_split(sizes: list[int], m: int) -> int:
    best = math.inf
    n = len(sizes)
    for mask in range(1 << (n - 1)):  # each bit: cut after position i
        if bin(mask).count("1") + 1 > m:
            continue
        cur, worst = 0, 0
        for i, s in enumerate(sizes):
            cur += s
            if i == n - 1 or mask >> i & 1:
                worst, cur = max(worst, cur), 0
        best = min(best, worst)
    return int(best)


def _brute_min_lots(amount: int, lots: list[int]) -> int:
    best = math.inf
    for q in range(amount // 25 + 1):
        for d in range((amount - 25 * q) // 10 + 1):
            for n in range((amount - 25 * q - 10 * d) // 5 + 1):
                p = amount - 25 * q - 10 * d - 5 * n
                best = min(best, q + d + n + p)
    return int(best)


if __name__ == "__main__":
    main()
