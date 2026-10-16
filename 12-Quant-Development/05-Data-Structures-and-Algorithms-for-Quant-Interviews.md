---
type: concept
track: [quant-research, quant-dev]
tier: core
status: solid
prereqs: []
est_hours: 20
sources: [Cormen Leiserson Rivest and Stein - Introduction to Algorithms 4th ed (MIT Press 2022) ch 6 9 14 19 20-22, Skiena - The Algorithm Design Manual 3rd ed (Springer 2020), Sedgewick and Wayne - Algorithms 4th ed (Addison-Wesley 2011) ch 1.5 and 2.4 and 5.2, Knuth - The Art of Computer Programming vol 2 3rd ed (1997) section 4.2.2 (Welford update), Welford - Note on a Method for Calculating Corrected Sums of Squares and Products (Technometrics 1962), Hoare - Algorithm 65 Find (CACM 1961), Tarjan - Efficiency of a Good But Not Linear Set Union Algorithm (JACM 1975), Kahn - Topological Sorting of Large Networks (CACM 1962)]
---

# Data Structures and Algorithms for Quant Interviews

## TL;DR

- Quant coding rounds are LeetCode-medium problems in a trading costume: heaps for top-k and merging feeds, two heaps or a monotonic deque for streaming statistics, sweeps for intervals, hash maps for O(1) lookups, DP for trade sequencing, graphs for dependencies and currency arbitrage.
- State the complexity before coding, and say why the structure achieves it: a heap of size $k$ makes top-$k$ O(n log k); a monotonic deque makes sliding max O(n) because each index enters and leaves once.
- Streams are the quant twist: you see each tick once, so the answer must update in O(log n) or O(1) per event with bounded memory (running median, rolling max, Welford variance).
- Numerical care is part of correctness: the naive one-pass variance of 1e9 + (4, 7, 13, 16) returns -128.0 (a negative variance) in float64 while Welford's update returns the exact 22.5.
- Test against brute force on random inputs before claiming correctness; every routine here is cross-checked that way in [qd_dsa_patterns.py](code/python/qd_dsa_patterns.py).

## Learning objectives

- Solve LeetCode medium problems fluently in C++ or Python.
- Recognise the patterns quant firms favour: heaps, intervals, streaming statistics, order books, simulation.
- Quote time and space complexity for every standard structure and justify it.
- Implement order statistics, sliding-window statistics, interval sweeps, LRU caches, tries, union-find and graph traversals from memory.
- Solve the classic DP families (trading with constraints, knapsack, coin change, longest increasing subsequence) and recognise "binary search on the answer".

## Core concepts

### Complexity cheat sheet

| Structure or algorithm | Operation | Time | Notes |
| :--- | :--- | :--- | :--- |
| Dynamic array | Index, append | O(1), O(1) amortised | Append doubles capacity; contiguous, cache friendly |
| Hash map | Get, put | O(1) expected, O(n) worst | Rehash on growth; adversarial keys can degrade it |
| Balanced BST (`std::map`) | Insert, find, min | O(log n) | Ordered iteration; pointer chasing |
| Binary heap | Push, pop, peek | O(log n), O(log n), O(1) | `heapq` is a min-heap; negate for max |
| Monotonic deque | Sliding max or min | O(1) amortised per step | Each index pushed and popped once |
| Union-find | Union, find | Near O(1) amortised | Path compression plus union by size: inverse Ackermann |
| Trie | Insert, prefix lookup | O(length of key) | Memory heavy; good for symbol and prefix search |
| Sort | Comparison sort | O(n log n) | Lower bound for comparison sorting |
| Quickselect | k-th smallest | O(n) expected, O(n^2) worst | Median of medians gives O(n) worst case |
| BFS, DFS | Traversal | O(V + E) | BFS gives fewest-edge paths |
| Topological sort (Kahn) | Order a DAG | O(V + E) | Fails if and only if there is a cycle |
| Dijkstra (binary heap) | Shortest paths, non-negative weights | O((V + E) log V) | Not valid with negative edges |
| Bellman-Ford | Shortest paths, negative cycle detection | O(V E) | Finds currency arbitrage on $-\ln(\text{rate})$ weights |

### Heaps: top-k, merging feeds, running median

- Top-$k$ of a stream: keep a min-heap of size $k$ and replace the root when a larger value arrives; O(n log k) time, O(k) memory, better than sorting when $k \ll n$.
- Merging $k$ time-sorted feeds (one per venue): a heap of the head of each feed; pop the earliest, push that feed's next; O(n log k); breaking ties by feed index makes the merge deterministic, which matters for replay.
- Running median: a max-heap of the lower half and a min-heap of the upper half, rebalanced so their sizes differ by at most one; insert O(log n), median O(1).

### Order statistics

Quickselect partitions around a random pivot and recurses into one side only: expected O(n), worst case O(n^2), O(n) worst case with median-of-medians pivots.
Use it for one percentile of a batch (the median latency of a capture) without a full sort; for many percentiles of a stream, use a histogram (see [Low-Latency Engineering](03-Low-Latency-Engineering.md)).

### Sliding windows

- Rolling max or min over the last $w$ ticks: a deque of indices whose values are decreasing; drop from the back anything not larger than the new value, drop from the front anything outside the window; the front is the max, and the total cost is O(n).
- Rolling median: keep the window sorted (binary search plus insert and delete, O(w) per step from shifting, fast for small windows), or two heaps with lazy deletion for O(log w).
- Max drawdown is a running-peak scan: track the highest value so far and the largest drop below it, O(n).

### Intervals

- Merge overlapping intervals: sort by start, extend the last merged interval while starts overlap; O(n log n).
- Maximum number of simultaneously live intervals (open orders, concurrent sessions, meeting rooms): a sweep over +1 at each start and -1 at each end, processing ends before starts at equal times for half-open intervals; O(n log n).

### Hashing and design questions

- Two-sum and its relatives: one pass with a hash map from value to index, O(n).
- Count contiguous runs with a given sum: prefix sums plus a hash map counting prefix values, O(n); this is how you count P&L windows hitting a target.
- LRU cache: a hash map to nodes of a doubly linked list ordered by recency; get and put are O(1) (Python's `OrderedDict` is exactly this).
- Trie: prefix search over symbols or order-id prefixes in O(length).

### Union-find

Disjoint-set union groups items connected by any chain of pairwise links: assets linked when their correlation exceeds a threshold form clusters, accounts linked by shared identifiers form households.
With path compression and union by size or rank, a sequence of $m$ operations costs $O(m\,\alpha(n))$ (Tarjan), effectively constant.

### Graphs

- BFS finds the fewest-edge path (fewest currency conversions); DFS detects cycles and finds components.
- Kahn's topological sort orders a dependency DAG, such as market data, then curves, then surfaces, then pricers; if it cannot place every node, the graph has a cycle.
- Currency arbitrage: a cycle whose rate product exceeds 1 is a cycle with negative total weight under $w = -\ln(\text{rate})$, because $\prod r_i > 1 \iff \sum -\ln r_i < 0$; Bellman-Ford detects it in O(V E).

### Dynamic programming with a trading flavour

| Problem | State | Recurrence | Complexity |
| :--- | :--- | :--- | :--- |
| One trade (buy then sell) | Running minimum | best = max(best, p - min so far) | O(n) |
| Unlimited trades, fee per round trip | flat, long | flat = max(flat, long + p - fee); long = max(long, flat - p) | O(n) |
| At most $k$ trades | buy[j], sell[j] | buy[j] = max(buy[j], sell[j-1] - p); sell[j] = max(sell[j], buy[j] + p) | O(nk) |
| Best P&L run (Kadane) | Best run ending here | cur = max(x, cur + x) | O(n) |
| Capital allocation (0/1 knapsack) | Best value per budget | dp[c] = max(dp[c], dp[c - cost] + value), $c$ descending | O(nC), pseudo-polynomial |
| Fewest lots to fill a size (coin change) | Fewest lots per amount | dp[a] = min over lots of dp[a - lot] + 1 | O(A L) |
| Ways to make a size | Count per amount | dp[a] += dp[a - lot], lots in the outer loop | O(A L) |
| Longest increasing subsequence | Smallest tail per length | Binary search into tails | O(n log n) |

"Binary search on the answer" covers problems like splitting a parent order into at most $m$ contiguous child orders minimising the largest: the feasibility check "can it be done with largest at most $X$" is greedy and monotone in $X$, so binary search $X$ between the largest clip and the total, O(n log(sum)).

### Streaming statistics

Welford's update keeps count, mean and the sum of squared deviations $M_2$ in one pass:

$$
\delta = x_n - \bar{x}_{n-1}, \qquad \bar{x}_n = \bar{x}_{n-1} + \frac{\delta}{n}, \qquad M_{2,n} = M_{2,n-1} + \delta\,(x_n - \bar{x}_n),
$$

with variance $M_2/n$ (population) or $M_2/(n-1)$ (sample).
The textbook one-pass formula $\big(\sum x^2 - (\sum x)^2/n\big)/n$ subtracts two huge, nearly equal numbers and loses every significant digit when the mean is large relative to the spread, which is exactly the case for prices and timestamps.

### How to run the interview

1. Restate the problem with a tiny example and ask about sizes, ranges, duplicates, ties and streaming versus batch.
2. Give the brute force and its complexity, then the better structure and why it is better.
3. Code the clean version, naming invariants ("the deque holds indices with decreasing values").
4. Test edge cases out loud: empty input, one element, all equal, window equal to length, negative values.
5. State complexity and one extension (streaming, concurrency, memory limits).

## Worked examples

All results below are printed and asserted by [qd_dsa_patterns.py](code/python/qd_dsa_patterns.py).

### Top-k and feed merging

"Return the three largest trade sizes from 120, 5, 300, 42, 300, 7, 999, 18."
Min-heap of size 3; answer `[999, 300, 300]` in O(n log 3).
"Merge three venue feeds sorted by timestamp": NYSE (1, 4, 9), ARCA (2, 4), BATS (3, 10) merge to timestamps 1, 2, 3, 4, 4, 9, 10, with the NYSE 4 before the ARCA 4 because ties break by feed index.

### Median latency and running median

Quickselect on latencies 12, 7, 3, 25, 8, 19, 5, 11, 4 for index 4 of 9 returns 8, the median, without sorting.
The running median of the stream 5, 15, 1, 3 is 5, 10, 5, 4: after 15 the two heaps hold {5} and {15}, so the median is their mean.

### Rolling max, rolling median and drawdown

Prices 1, 3, -1, -3, 5, 3, 6, 7 with window 3: rolling max 3, 3, 5, 5, 6, 7 and rolling median 1, -1, -1, 3, 5, 6.
For the equity curve 100, 104, 101, 108, 97, 99, 110, 103 the max drawdown is 11, from the peak 108 to 97.

### Sessions and live orders

Sessions (in minutes after midnight) 570 to 600, 585 to 660, 780 to 840 and 840 to 900 merge to 570 to 660 and 780 to 900 (closed intervals touching at 840 merge).
Order lifetimes [0, 10), [2, 5), [4, 12), [5, 8), [11, 13) have at most 3 live at once: at time 4 the first three overlap, and at time 5 one ends as another starts.

### LRU, two-sum, prefix sums, trie, union-find

An LRU cache of capacity 2: put AAPL, put MSFT, get AAPL, put NVDA evicts MSFT, leaving AAPL and NVDA.
Notionals 250, 700, 125, 875, 400 with target 1000: indices (2, 3), found in one pass.
The array 1, 1, 1 has 2 contiguous runs summing to 2.
A trie of AAPL, AAL, AMZN, AMD, MSFT, MS returns AAL and AAPL for prefix AA, and MS and MSFT for prefix MS.
Six assets with high-correlation pairs (0, 1), (1, 2), (3, 4) form 3 clusters: {0, 1, 2}, {3, 4} and {5}.

### Dependency order and currency arbitrage

Dependencies: swap pricer needs the OIS and projection curves, the projection curve needs the OIS curve, the OIS curve and the vol surface need fixings.
Kahn's order, breaking ties alphabetically so the result is reproducible: fixings, ois_curve, projection_curve, swap_pricer, vol_surface; a two-node cycle returns no order.
Rates USD to EUR 0.9, EUR to GBP 0.8, GBP to USD 1.4, plus a back-quote EUR to USD 1.1: the product around the loop USD, EUR, GBP is 1.008, so Bellman-Ford on $-\ln$ weights finds the cycle EUR, GBP, USD; the two-leg loop USD, EUR, USD multiplies to 0.99 and is not an arbitrage.
Fewest conversions from CAD to KRW over the edges USD-EUR, EUR-JPY, USD-CAD, JPY-KRW is 4 by BFS.

### Trading DP

Prices 7, 1, 5, 3, 6, 4: one trade earns 5 (buy 1, sell 6); unlimited trades earn 7 (1 to 5, then 3 to 6); unlimited trades with a fee of 2 per round trip earn 3.
Prices 3, 3, 5, 0, 0, 3, 1, 4 with at most 2 trades earn 6 (0 to 3, then 1 to 4).
Daily P&L -2, 1, -3, 4, -1, 2, 1, -5, 4: the best run sums to 6, days 3 to 6 (zero-based).

### Knapsack, lots, LIS and order slicing

Capital 10 across strategies (cost, expected P&L) (5, 10), (4, 40), (6, 30), (3, 50): the best is 90, from the cost-4 and cost-3 strategies.
Lot sizes 1, 5, 10, 25: the fewest lots summing to 63 is 6 (25 + 25 + 10 + 1 + 1 + 1), and there are 242 ways to make 100; with lots 2 and 4, 7 is impossible.
The longest increasing subsequence of 10, 9, 2, 5, 3, 7, 101, 18 has length 4.
Splitting clips 7, 2, 5, 10, 8 into at most 2 contiguous child orders, the smallest possible largest child is 18 (7 + 2 + 5 and 10 + 8).

### Variance that loses every digit

For 2, 4, 4, 4, 5, 5, 7, 9 Welford gives mean 5, population variance 4 and sample variance 4.571429.
For $10^9$ + (4, 7, 13, 16) the naive one-pass formula with plain left-to-right sums returns -128.0, a negative variance, and Welford returns 22.5, the exact population variance of 4, 7, 13, 16.
Even exactly rounded sums (`math.fsum`, or the compensated built-in `sum` of Python 3.12 and later) only improve the naive answer to 0.0: the squares near $10^{18}$ are already rounded to multiples of 128, and the sums near $4 \times 10^{18}$ to multiples of 512, before the subtraction.
The garbage value depends on summation order, so the same formula can print a different wrong number on another machine or library.
The [problem set](15-Quant-Dev-Problem-Set.md) shows -170.67 for the sample variance from the same sums: the numerator is -512 in both, divided by $n - 1 = 3$ there and by $n = 4$ here.

## Pitfalls

- Using a max-heap of all $n$ elements for top-$k$ (O(n log n)) instead of a min-heap of size $k$.
- Forgetting that Python's `heapq` is a min-heap, or comparing tuples whose second field is not comparable.
- Off-by-one window boundaries: decide inclusive or half-open once and test a window equal to the input length.
- Interval sweeps that process a start before an end at the same time and over-count half-open intervals.
- Using Dijkstra with negative weights, or forgetting that arbitrage detection needs the log transform.
- Iterating the knapsack budget upwards in the 1-D 0/1 DP, which silently reuses items (that is the unbounded variant).
- Confusing "number of ways" (combinations: lots in the outer loop) with "number of orderings" (amount in the outer loop).
- The naive variance formula on large-mean data, and floating-point equality in tests.
- Recursion depth limits in Python DFS on large inputs; use an explicit stack.
- Claiming O(1) for hash maps without mentioning worst case and rehashing.

## Interview questions

> [!question]- qd-dsa-top-k | How do you find the top $k$ values of a stream of $n$, and at what cost?
> Min-heap of size $k$: push until full, then replace the root when a larger value arrives. O(n log k) time, O(k) memory; the heap root is the current $k$-th largest.

> [!question]- qd-dsa-merge-k-feeds | Merge $k$ timestamp-sorted venue feeds into one stream. Complexity, and how do you keep it deterministic?
> A heap of the next event from each feed: O(n log k). Break timestamp ties by a fixed key (feed index, then sequence number) so replays produce the same order.

> [!question]- qd-dsa-running-median | Maintain the median of a stream with O(log n) updates.
> Max-heap for the lower half, min-heap for the upper half, sizes differing by at most one. Insert into the correct heap, rebalance, read the median from the roots in O(1).

> [!question]- qd-dsa-quickselect | What is the complexity of quickselect, and how do you make the worst case linear?
> Expected O(n) with random pivots, worst case O(n^2). Median-of-medians pivot selection makes the worst case O(n), with a larger constant.

> [!question]- qd-dsa-sliding-max | Compute the max of every window of length $w$ in O(n).
> Monotonic deque of indices with decreasing values: pop from the back while the back value is not larger than the new one, pop from the front if it left the window; the front is the max. Each index is pushed and popped at most once.

> [!question]- qd-dsa-sliding-median | How would you compute a rolling median over $w$ ticks?
> Keep the window sorted with binary search insert and delete (O(log w) search, O(w) shift, fast for small $w$), or two heaps with lazy deletion for O(log w) per step. For 1, 3, -1, -3, 5, 3, 6, 7 with $w = 3$: 1, -1, -1, 3, 5, 6.

> [!question]- qd-dsa-max-drawdown | Compute maximum drawdown in one pass.
> Track the running peak and the largest peak-minus-current: O(n), O(1) memory. For 100, 104, 101, 108, 97, 99, 110, 103 it is 11.

> [!question]- qd-dsa-merge-intervals | Merge overlapping intervals. Complexity?
> Sort by start, then extend the last merged interval while the next start is within it, else start a new one: O(n log n) for the sort, O(n) for the pass.

> [!question]- qd-dsa-max-concurrent | Given order lifetimes as half-open intervals, find the maximum number of live orders.
> Sweep line: +1 at each start, -1 at each end, ends before starts at equal times, track the running maximum. O(n log n). For [0,10), [2,5), [4,12), [5,8), [11,13) the answer is 3.

> [!question]- qd-dsa-lru | Design an LRU cache with O(1) get and put.
> Hash map from key to a node in a doubly linked list kept in recency order: get moves the node to the front, put inserts at the front and evicts from the back when over capacity.

> [!question]- qd-dsa-subarray-sum-k | Count contiguous subarrays summing to $k$ in O(n).
> Prefix sums with a hash map counting how many times each prefix value occurred; at each position add the count of (prefix - k). For 1, 1, 1 with $k = 2$ the answer is 2.

> [!question]- qd-dsa-union-find | What does union-find do, and what is its complexity with both optimisations?
> Maintains disjoint sets under union and find. With path compression and union by size or rank, $m$ operations cost $O(m\,\alpha(n))$, effectively constant per operation.

> [!question]- qd-dsa-topo-sort | How do you order the evaluation of a pricing dependency graph, and detect a cycle?
> Kahn's algorithm: repeatedly take nodes with no unprocessed dependencies, O(V + E). If some nodes are never taken, the graph has a cycle.

> [!question]- qd-dsa-fx-arbitrage | How do you detect a currency arbitrage loop?
> Weight each conversion by $-\ln(\text{rate})$; a loop with rate product above 1 has negative total weight, so run Bellman-Ford and look for a relaxation in the $V$-th pass. USD to EUR 0.9, EUR to GBP 0.8, GBP to USD 1.4 multiply to 1.008.

> [!question]- qd-dsa-dijkstra-negative | Why can't Dijkstra find the arbitrage loop?
> Dijkstra assumes that once a node is popped its distance is final, which requires non-negative edge weights. Log-rate weights are negative for rates above 1, and a negative cycle has no shortest path at all.

> [!question]- qd-dsa-stock-one-trade | Maximum profit with one buy and one later sell?
> Track the minimum price so far and the best price minus that minimum: O(n). For 7, 1, 5, 3, 6, 4 it is 5.

> [!question]- qd-dsa-stock-fee | Maximum profit with unlimited trades and a fee per round trip?
> Two states: flat = max(flat, long + p - fee) and long = max(long, flat - p), O(n). For 7, 1, 5, 3, 6, 4 with fee 2 it is 3; without the fee it is 7.

> [!question]- qd-dsa-stock-k-trades | Maximum profit with at most $k$ round trips?
> buy[j] = max(buy[j], sell[j-1] - p) and sell[j] = max(sell[j], buy[j] + p) for $j = 1..k$: O(nk) time, O(k) memory. For 3, 3, 5, 0, 0, 3, 1, 4 with $k = 2$ it is 6.

> [!question]- qd-dsa-kadane | Find the best contiguous run of daily P&L.
> Kadane: keep the best sum ending today, max(x, previous + x), and the overall best: O(n). For -2, 1, -3, 4, -1, 2, 1, -5, 4 it is 6 (days 3 to 6).

> [!question]- qd-dsa-knapsack | Allocate a capital budget across indivisible strategies to maximise expected P&L. Complexity?
> 0/1 knapsack DP over budget, iterating the budget downwards: O(nC), pseudo-polynomial in the budget $C$ (the problem is NP-hard in general). Budget 10 with (5, 10), (4, 40), (6, 30), (3, 50) gives 90.

> [!question]- qd-dsa-coin-change | Fewest lots of sizes 1, 5, 10, 25 summing to 63, and why not always use the greedy choice?
> 6 (25, 25, 10, 1, 1, 1). Greedy happens to be optimal for this set but not in general (lots 1, 3, 4 for 6: greedy uses 4, 1, 1; optimal is 3, 3), so use DP in O(amount x lots).

> [!question]- qd-dsa-lis | Length of the longest increasing subsequence in O(n log n)?
> Keep the smallest tail of an increasing subsequence of each length; binary search each value into the tails array. For 10, 9, 2, 5, 3, 7, 101, 18 the length is 4.

> [!question]- qd-dsa-binary-search-answer | Split a parent order into at most $m$ contiguous child orders minimising the largest child. Approach?
> Binary search the answer $X$ between the largest clip and the total; feasibility (greedily pack clips while the sum stays at most $X$) is monotone in $X$. O(n log(sum)). For 7, 2, 5, 10, 8 and $m = 2$ the answer is 18.

> [!question]- qd-dsa-welford | Why use Welford's algorithm for streaming variance?
> The naive $\sum x^2 - (\sum x)^2/n$ cancels catastrophically when the mean is large relative to the spread: for $10^9$ + (4, 7, 13, 16) it gives a population variance of -128.0 with left-to-right sums (0.0 even with exactly rounded sums), while Welford's one-pass update gives the exact 22.5.

> [!question]- qd-dsa-hash-worst-case | When is a hash map not O(1)?
> Worst case O(n) per operation when many keys collide (adversarial input or a weak hash), and an O(n) pause when it rehashes on growth. On a hot path, reserve capacity at startup and use a good hash.

## In this repo and SDE-Interview-Prep

- Code: [qd_dsa_patterns.py](code/python/qd_dsa_patterns.py) (every example above, plus brute-force cross-checks on seeded random inputs).
- Related: [Order Book and Matching Engine](07-Order-Book-and-Matching-Engine.md) (the trading data structure), [Coding Interviews for Quants](../13-Interview-Playbook/07-Coding-Interviews-for-Quants.md).
- [DSA topics (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/03-Data-Structures-Algorithms/01-Topics/README.md)
- [LeetCode quant set (C++) (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/C%2B%2B/LeetCode-Quant-Complete-CPP-Full.md)
- [LeetCode quant set (Python) (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/Python/LeetCode-Quant-Complete-Python-Full.md)
- [NeetCode 150 (C++) (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/C%2B%2B/NeetCode-150-CPP.md)

## Further reading

- Thomas Cormen, Charles Leiserson, Ronald Rivest and Clifford Stein, *Introduction to Algorithms*, 4th edition (MIT Press, 2022): heaps (ch 6), order statistics (ch 9), dynamic programming (ch 14), disjoint sets (ch 19), graphs (ch 20 to 22).
- Steven Skiena, *The Algorithm Design Manual*, 3rd edition (Springer, 2020): the catalogue of problems and how to recognise them.
- Robert Sedgewick and Kevin Wayne, *Algorithms*, 4th edition (Addison-Wesley, 2011): union-find (1.5), priority queues (2.4), tries (5.2).
- B. P. Welford, "Note on a Method for Calculating Corrected Sums of Squares and Products", *Technometrics* 4(3), 1962; Donald Knuth, *The Art of Computer Programming*, vol. 2, 3rd edition, section 4.2.2.
- C. A. R. Hoare, "Algorithm 65: Find", *Communications of the ACM* 4(7), 1961.
- Robert Tarjan, "Efficiency of a Good But Not Linear Set Union Algorithm", *Journal of the ACM* 22(2), 1975.
- A. B. Kahn, "Topological Sorting of Large Networks", *Communications of the ACM* 5(11), 1962.
