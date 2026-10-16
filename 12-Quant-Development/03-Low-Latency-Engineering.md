---
type: concept
track: [quant-dev]
tier: core
status: solid
prereqs: [cpp-for-trading-systems]
est_hours: 10
sources: [Hennessy and Patterson - Computer Architecture - A Quantitative Approach 6th ed (Morgan Kaufmann 2017) ch 2 and appendix B, Drepper - What Every Programmer Should Know About Memory (2007), Gregg - Systems Performance 2nd ed (Addison-Wesley 2020) ch 6-7 and 10, Dean and Barroso - The Tail at Scale (CACM 2013), Tene - How NOT to Measure Latency (talk 2015) and HdrHistogram, Commission Delegated Regulation (EU) 2017/574 (RTS 25) Annex Table 2, IEEE 1588-2019 Precision Time Protocol, DPDK Programmer's Guide (dpdk.org), AMD Solarflare OpenOnload and ef_vi documentation, Linux kernel admin-guide kernel-parameters (isolcpus nohz_full rcu_nocbs), Intel 64 and IA-32 Architectures Software Developer Manual vol 3 - Time-Stamp Counter and invariant TSC]
---

# Low-Latency Engineering

## TL;DR

- Tick-to-trade latency is a budget across wire, NIC, kernel or bypass, decode, book, strategy, risk and encode; you can only cut what you measure, stage by stage, as percentiles.
- Memory dominates: a dependent load that hits L1 cost about 1.1 ns on the test machine, one that misses to DRAM about 110 to 120 ns; keep the hot working set small and contiguous.
- Data written by different threads must live on different cache lines; on the test machine two threads incrementing counters 8 bytes apart ran about 3 times slower than counters 256 bytes apart.
- Predictable branches are nearly free and unpredictable ones cost several nanoseconds each; the same loop ran 12 times faster on sorted data.
- Remove the OS from the hot path: isolate and pin cores, busy-poll, kernel bypass (DPDK, OpenOnload, ef_vi), huge pages, locked memory, no interrupts on trading cores.
- Report p50, p99, p99.9 and max from a histogram, timestamp at the wire (hardware or PTP-disciplined clocks), and beware coordinated omission: a closed-loop benchmark understated the p99 of a stalled server by a factor of 28,601 in the simulation below.

## Learning objectives

- Explain cache hierarchy, false sharing, branch prediction and NUMA effects.
- Tune the OS: core isolation, pinning, huge pages, interrupts.
- Measure latency correctly: percentiles, coordinated omission, timestamping.
- Build a tick-to-trade latency budget and reason about which stage to attack.
- Describe kernel bypass accurately (DPDK, OpenOnload, ef_vi) and when each is used.

## Core concepts

### Anatomy of tick-to-trade

Tick-to-trade is the time from the last bit of a market-data packet arriving at the NIC to the first bit of the resulting order leaving it.

```mermaid
flowchart LR
    W[Wire in] --> N[NIC RX and timestamp]
    N --> K[Kernel stack or kernel bypass]
    K --> D[Decode feed message]
    D --> B[Update order book]
    B --> S[Strategy decision]
    S --> R[Pre-trade risk checks]
    R --> E[Encode order]
    E --> T[NIC TX]
    T --> O[Wire out]
```

An illustrative software budget (every input is an assumption chosen to show the method, not a measurement of any firm), from [qd_latency_budget.py](code/python/qd_latency_budget.py):

| Stage | ns | Share |
| :--- | ---: | ---: |
| NIC to user space via kernel bypass | 800 | 40.0% |
| Decode one market-data message | 100 | 5.0% |
| Update order book | 150 | 7.5% |
| Strategy decision | 500 | 25.0% |
| Pre-trade risk checks | 200 | 10.0% |
| Encode order and hand to NIC | 250 | 12.5% |
| Total | 2000 | 100% |

The method matters more than the numbers: instrument every boundary, attack the largest share first, and remember that the wire itself costs time.
Serialization delay is the time to clock a frame onto the wire, $(\text{frame} + 20\ \text{bytes of preamble and inter-frame gap}) \times 8 / \text{rate}$:

| Frame | 1 GbE | 10 GbE | 25 GbE |
| :--- | ---: | ---: | ---: |
| 64 bytes | 672.00 ns | 67.20 ns | 26.88 ns |
| 1500 bytes | 12,160.00 ns | 1,216.00 ns | 486.40 ns |

A store-and-forward switch adds a full serialization per hop; cut-through switches start forwarding after the header.
Propagation in fibre with a group index of 1.468 is 4.897 µs per km, against 3.336 µs per km in free space, so a line-of-sight radio path saves 31.9% of the fibre delay over the same distance (more in practice, because fibre routes are longer than the straight line).

### The memory hierarchy

Each level is larger and slower; a miss at one level costs the latency of the next.
The pointer-chasing benchmark in [latency_lab.cpp](code/cpp/latency_lab.cpp) builds a random single cycle (Sattolo's algorithm) through a working set, one node per 128-byte block, so every load depends on the previous one and the prefetcher cannot help.
Measured on an Apple M3 Pro (performance-core L1D 128 KiB and shared L2 16 MiB, 128-byte cache lines and 16 KiB pages, as reported by `sysctl`), Apple clang 21 at `-O2`, one run:

| Working set | ns per dependent load | Where it lives |
| ---: | ---: | :--- |
| 16 KiB | 1.13 | L1 |
| 64 KiB | 1.13 | L1 |
| 256 KiB | 5.13 | L2 |
| 1 MiB | 7.57 | L2 |
| 4 MiB | 37.08 | L2, shared with other work |
| 16 MiB | 111.69 | L2 capacity exceeded, DRAM |
| 64 MiB | 119.05 | DRAM plus TLB misses |
| 256 MiB | 120.50 | DRAM plus TLB misses |

The 4 MiB point varied between about 10 and 80 ns across runs on the same machine, because the L2 is shared with every other process on the cluster: on a shared host your cache is not yours.
Rules that follow: keep the per-message working set in L1 and L2; prefer arrays and struct-of-arrays to pointer-based structures; preallocate and reuse (a freed, recently used slot is cache-warm); avoid touching cold data on the hot path, including logging buffers.

### TLBs and huge pages

Virtual addresses are translated through page tables, cached in the TLB.
TLB reach is entries times page size: a hypothetical 1536-entry TLB covers 6 MiB with 4 KiB pages, 24 MiB with 16 KiB pages, 3 GiB with 2 MiB pages and 1536 GiB with 1 GiB pages.
Large order books, hash maps and memory pools spread over many 4 KiB pages pay a page walk on top of the cache miss.
On Linux, back hot allocations with explicit huge pages (`hugetlbfs`, `mmap` with `MAP_HUGETLB`) or `madvise(MADV_HUGEPAGE)`; transparent huge pages in `always` mode can cause latency spikes when the kernel compacts memory in the background, so trading hosts usually set them to `madvise` or `never`.
Lock memory with `mlockall(MCL_CURRENT | MCL_FUTURE)` and touch every page at startup so no page fault happens during trading.

### False sharing

Caches keep lines coherent: before a core writes a line it must own it exclusively, invalidating copies elsewhere.
Two threads writing different variables in the same line therefore bounce the line between cores although they share no data.
Measured by [latency_lab.cpp](code/cpp/latency_lab.cpp) (two threads, relaxed `fetch_add` on their own counter, median of 5 runs, same machine):

| Distance between the counters | ns per increment |
| ---: | ---: |
| 8 bytes | 7.80 |
| 64 bytes | 3.62 |
| 128 bytes | 2.75 |
| 256 bytes | 2.45 |

On this machine most of the penalty disappears at 64 bytes and the rest at 128.
Pad to 128 bytes in portable code: it covers Apple Silicon's reported 128-byte line and x86's adjacent-line prefetcher, which fetches 64-byte lines in pairs.
Do not use `std::hardware_destructive_interference_size` in a header or a wire format: its value differs between compilers.

### Branch prediction

Modern cores predict branch outcomes and speculate; a misprediction flushes the pipeline.
The benchmark sums the bytes that are at least 128 in a 4 MiB array, with an empty `asm volatile` in the taken branch so the compiler must keep a real branch:

| Variant | ns per element |
| :--- | ---: |
| Branchy, random data | 3.850 |
| Branchy, sorted data | 0.314 |
| Branchless (mask arithmetic, vectorised by the compiler) | 0.057 |

Same instructions, same data values, about 12 times slower when the outcome is random.
Remedies: make the common case straight-line; replace data-dependent branches with arithmetic or conditional selects; batch work by type so branches become predictable; use `[[likely]]` only when a profile shows mispredictions.

### NUMA and PCIe locality

On multi-socket servers each socket has its own memory controllers and PCIe lanes.
A thread on socket 0 reading memory attached to socket 1, or a NIC on socket 1 delivering packets to a thread on socket 0, pays an inter-socket hop on every access.
Pin the trading threads, allocate their memory (`numactl --cpunodebind --membind`, or first-touch from the pinned thread) and place the NIC on the same socket.

### Taking the operating system out of the hot path

| Technique | Mechanism | Purpose |
| :--- | :--- | :--- |
| Core isolation | Boot parameters `isolcpus`, `nohz_full`, `rcu_nocbs` | Keep the scheduler, timer ticks and RCU callbacks off trading cores |
| Pinning | `sched_setaffinity`, `taskset`, `pthread_setaffinity_np` | One trading thread per isolated core; no migrations |
| Interrupt steering | `/proc/irq/*/smp_affinity`, `irqbalance` off | Device interrupts land on housekeeping cores |
| Busy polling | Spin on the NIC ring or on a queue instead of blocking | No wake-up latency; costs a whole core |
| Frequency and idle states | Performance governor, shallow C-states only | Avoid the exit latency of deep sleep states and frequency ramps |
| Memory | Huge pages, `mlockall`, prefault | No TLB storms or page faults during trading |
| Scheduling class | `SCHED_FIFO` for the trading thread | Never preempted by normal tasks; a busy-looping FIFO thread can starve kernel work on that core, so isolate first |

### Kernel bypass

The kernel network stack costs system calls, copies, interrupts and context switches per packet.
Kernel bypass maps NIC queues into the process so user code reads and writes packets directly.

- DPDK (Data Plane Development Kit, a Linux Foundation project): user-space poll-mode drivers for many NICs; the application owns whole cores that poll RX rings, and implements or links its own protocol processing.
- OpenOnload (Solarflare, now AMD): a user-space TCP/UDP stack that accelerates unmodified BSD-sockets applications, typically launched with the `onload` wrapper; the application keeps using `recv` and `send`.
- ef_vi (Solarflare, now AMD): the low-level layer-2 API under OpenOnload, giving direct access to NIC descriptor rings and raw Ethernet frames; lowest software latency, but the application handles framing, multicast filters and recovery itself.
- AF_XDP: a Linux socket type that delivers frames from an XDP program straight to a user-space ring, staying inside the kernel's driver model.

Beyond software, FPGA NICs run feed parsing and order generation in hardware for the latency-critical subset of decisions.

### Clocks and timestamping

`rdtsc` reads the x86 timestamp counter; on CPUs with an invariant TSC (`constant_tsc` and `nonstop_tsc` flags) it ticks at a fixed rate regardless of frequency scaling and sleep states, but it must be calibrated to nanoseconds and is not ordered with surrounding instructions (`rdtscp`, or `lfence` before `rdtsc`, orders it).
On AArch64 the equivalent is the generic timer, `cntvct_el0`, with its frequency in `cntfrq_el0`.
Measured on the test machine: `steady_clock::now()` cost 14.7 ns per call with libc++ and advanced in steps of 42 ns; the same call through Homebrew GCC's libstdc++ cost 14.0 ns but advanced in steps of 1000 ns; the raw counter reported a nominal 1000 MHz, cost 9.2 ns per read, and also advanced in steps of 42 ticks.
So a single reading on this Mac cannot resolve anything shorter than about 42 ns: time batches, or use a platform with a finer counter.
Always measure your clock before measuring anything with it.

Across machines, clocks are disciplined by PTP (IEEE 1588) from a GPS-referenced grandmaster, with NICs that timestamp packets in hardware (`SO_TIMESTAMPING` on Linux).
Regulation sets a floor: under MiFID II RTS 25 (Commission Delegated Regulation (EU) 2017/574, Annex Table 2), a trading-venue member using a high-frequency algorithmic trading technique must keep business clocks within 100 microseconds of UTC with timestamp granularity of 1 microsecond or better (as of 2026-10).

### Measuring latency correctly

- Report percentiles (p50, p99, p99.9, max), never only the mean: in the jitter test below the mean was 863.8 ns while p99.9 was 9,375 ns.
- Record into a histogram, not a growing vector: the repo's `LatencyHistogram` in [microbenchmark_utils.hpp](code/cpp/microbenchmark_utils.hpp) is log-linear in the style of HdrHistogram, with O(1) allocation-free `record()` and a reported value never below the true one by more than 1/64 relative.
- Measure under load and on production-like hardware: an idle core, a warm cache and a microbenchmark loop flatter everything.
- Tails compound across stages: if each of $k$ independent stages exceeds its own p99 with probability 1%, the path hits at least one stage's p99 with probability $1 - 0.99^k$, which is 4.90% for $k = 5$, 9.56% for $k = 10$ and 63.40% for $k = 100$ (Dean and Barroso's "tail at scale").
- Keep headroom: in an M/M/1 queue with 300 ns service time, mean time in system is 600 ns at 50% utilization, 750 ns at 60%, 3,000 ns at 90% and 30,000 ns at 99%; latency explodes long before throughput saturates.

### Coordinated omission

A closed-loop load generator waits for each response before sending the next request.
When the system stalls, the generator stalls with it, so the requests that would have been sent during the stall, and would have waited, are never measured.
The simulation in [qd_coordinated_omission.py](code/python/qd_coordinated_omission.py) runs a server with 50 µs service time and one 2 s freeze at $t = 30$ s, under a generator that intends one request per millisecond for 60 s:

| Measurement | Samples | Mean | p99 | p99.9 | Max | Over 10 ms |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Closed loop (naive) | 58,000 | 0.0845 ms | 0.0500 ms | 0.0500 ms | 2000.0500 ms | 1 |
| Open loop (from intended send time) | 60,000 | 35.1544 ms | 1430.0500 ms | 1943.0500 ms | 2000.0500 ms | 2,095 |

The naive p99 is too low by a factor of 28,601.
Fix it by issuing load on a schedule and measuring each request from its intended start time, or by correcting the histogram for missed intervals (HdrHistogram's `recordValueWithExpectedInterval`).
In production, timestamp at the wire on both sides rather than inside the process under test.

## Worked examples

### Serialization versus propagation

"A 64-byte order leaves on 10 GbE and crosses 1000 km of fibre. Which term dominates?"
Serialization: $(64 + 20) \times 8 / 10 = 67.2$ ns.
Propagation: $1000 \times 4.897\ \mu s = 4.897$ ms, 72,868 times larger (computed from the unrounded propagation delay).
Inside a data centre, with metres of cable, the order flips and serialization plus switch hops dominate, which is why colocation and faster NICs matter there and geography and radio links matter between data centres.

### Reading a cache ladder

"Your book update is several times slower at p50 in production than in the benchmark. Why?"
The benchmark's book fits in L1 and L2 (1.13 to 7.57 ns per dependent load on the test machine); in production the book, the order-id hash map and the strategy state compete with everything else, and a few DRAM misses at about 110 to 120 ns each explain the gap.
Check with hardware counters (`perf stat -e cache-misses`), then shrink and colocate the hot data.

### Diagnosing false sharing

"Two threads each update their own statistics counter in a shared struct, and throughput halves when the second thread starts."
The counters share a cache line, which moves between the cores on every write.
On the test machine, 8 bytes apart cost 7.80 ns per increment and 256 bytes apart 2.45 ns.
Fix with `alignas(128)` per counter or per-thread structs, and keep read-mostly data on separate lines from written data.

### The mean that lied

The jitter test times a fixed 1000-step dependent arithmetic chain 200,000 times on the test machine: p50 833 ns, p90 834 ns, p99 1,167 ns, p99.9 9,375 ns, max 219,833 ns, mean 863.8 ns.
The mean says "about 860 ns"; one call in a thousand took more than 9 µs and the worst took 220 µs, from interrupts, preemption and frequency changes on an untuned desktop OS.
Those tails are what core isolation, pinning and interrupt steering remove.

### Coordinated omission in one sentence

"Our load test says p99 is 50 µs, but users see second-long stalls."
With a closed-loop tester, a 2 s freeze becomes one slow sample among 58,000; measured from the intended send times, 2,095 of 60,000 requests took over 10 ms and the p99 is 1430.05 ms.

## Pitfalls

- Optimising without a per-stage breakdown: speeding up the strategy by 100 ns is pointless if the kernel stack costs 5 µs.
- Averaging latencies, or computing percentiles of per-batch means and calling them per-message percentiles.
- Trusting a clock you have not characterised (resolution, cost, monotonicity, cross-core consistency).
- Benchmarking on a laptop or shared VM and quoting the numbers as production numbers.
- Padding to 64 bytes and assuming false sharing is solved on every platform.
- Turning on `SCHED_FIFO` busy loops without isolating the core, and starving kernel threads.
- Leaving transparent huge pages in `always` mode on a trading host.
- Measuring with a closed-loop generator and ignoring the requests a stall prevented you from sending.
- Assuming kernel bypass makes everything fast: one cache-missing hash lookup can cost more than the bypass saved.

## Interview questions

> [!question]- qd-lowlat-tick-to-trade | Define tick-to-trade latency and list its stages.
> Time from the market-data packet arriving at the NIC to the order leaving it: NIC receive, kernel or bypass, decode, book update, strategy, risk checks, encode, NIC transmit. Measure each boundary, ideally with wire timestamps on both ends.

> [!question]- qd-lowlat-serialization | How long does a 64-byte frame take to serialize at 10 GbE?
> 67.2 ns: (64 + 20 bytes of preamble and inter-frame gap) x 8 bits / 10 Gbit/s. At 1 GbE it is 672 ns, at 25 GbE 26.88 ns.

> [!question]- qd-lowlat-fibre-vs-radio | Why do HFT firms use microwave links between data centres?
> Light in fibre travels at about c/1.468, 4.897 µs per km, versus 3.336 µs per km in air: a 31.9% saving over the same distance, and radio paths are also straighter than fibre routes.

> [!question]- qd-lowlat-cache-numbers | Roughly what does a dependent load cost from L1, L2 and DRAM?
> Order of 1 ns, several ns, and around 100 ns. Measured on an Apple M3 Pro: 1.13 ns (16 KiB set), 5 to 8 ns (256 KiB to 1 MiB), 110 to 120 ns (16 MiB and up). Always measure on your hardware.

> [!question]- qd-lowlat-pointer-chase | How do you measure memory latency rather than bandwidth?
> Pointer chasing: a random single cycle through the working set so each load's address depends on the previous load, defeating prefetchers and out-of-order overlap; divide time by the number of loads.

> [!question]- qd-lowlat-false-sharing | What is false sharing and how do you fix it?
> Two threads write different variables on the same cache line, so the line ping-pongs between cores. Measured: 7.80 ns per increment 8 bytes apart vs 2.45 ns 256 bytes apart. Fix with alignment and padding (128 bytes is the safe value) or per-thread data.

> [!question]- qd-lowlat-why-128 | Why pad to 128 bytes rather than 64?
> Apple Silicon reports 128-byte cache lines, and x86 adjacent-line prefetchers pull 64-byte lines in pairs, so 64-byte padding can still interfere. 128 is safe on both; `hardware_destructive_interference_size` varies by compiler.

> [!question]- qd-lowlat-branch-sorted | Why does summing elements above a threshold run faster on sorted data?
> The branch becomes predictable (long runs of not-taken then taken), so there are almost no mispredictions. Measured: 3.850 ns per element random vs 0.314 sorted; a branchless version ran at 0.057.

> [!question]- qd-lowlat-huge-pages | Why use huge pages for trading processes?
> TLB reach is entries times page size; 2 MiB pages cover 512 times more memory per entry than 4 KiB pages (a 1536-entry TLB: 6 MiB vs 3 GiB), avoiding page walks on large books and pools. Use explicit huge pages or `madvise`; avoid THP `always`.

> [!question]- qd-lowlat-numa | What is the NUMA rule for a trading thread?
> Thread, its memory and the NIC it reads from must be on the same socket; pin the thread, bind or first-touch its memory locally, and put the NIC in a PCIe slot attached to that socket.

> [!question]- qd-lowlat-isolcpus | Which Linux settings isolate a core for a trading thread?
> Boot with `isolcpus`, `nohz_full` and `rcu_nocbs` for the core, steer IRQs elsewhere via `smp_affinity`, pin the thread with `sched_setaffinity`, set the performance governor and shallow C-states, and lock memory with `mlockall`.

> [!question]- qd-lowlat-kernel-bypass | Compare DPDK, OpenOnload and ef_vi.
> DPDK: user-space poll-mode drivers, the application owns polling cores and protocol processing. OpenOnload: user-space TCP/UDP stack that accelerates unmodified socket applications. ef_vi: Solarflare's raw layer-2 ring API under Onload, lowest latency, all framing and recovery done by the application.

> [!question]- qd-lowlat-busy-poll | What is the trade-off of busy polling?
> No wake-up or interrupt latency, at the cost of a dedicated core at 100% and higher power; it only pays when that core is isolated and the latency matters.

> [!question]- qd-lowlat-rdtsc | What do you need to know before using `rdtsc` for timing?
> Whether the TSC is invariant (constant rate across frequency and sleep states), its frequency for conversion to ns, that it is not serializing (use `rdtscp` or `lfence`), and whether TSCs are synchronized across cores if you compare readings between threads.

> [!question]- qd-lowlat-clock-resolution | Your timer returns nanoseconds. Is its resolution 1 ns?
> Not necessarily. On the test Mac, `steady_clock` advanced in 42 ns steps with libc++ and 1000 ns steps with libstdc++. Measure the modal step between back-to-back reads before trusting single-event timings.

> [!question]- qd-lowlat-mifid-clock | What clock accuracy does MiFID II require of an HFT firm?
> RTS 25 (Delegated Regulation 2017/574) Annex Table 2: maximum divergence from UTC of 100 microseconds and timestamp granularity of 1 microsecond or better for high-frequency algorithmic trading.

> [!question]- qd-lowlat-percentiles | Why report p99.9 and max instead of the mean?
> Trading losses come from the slow events (missed fills, stale quotes), and latency distributions are heavily right-skewed. In the jitter test the mean was 863.8 ns while p99.9 was 9,375 ns and max 219,833 ns.

> [!question]- qd-lowlat-tail-at-scale | Each of 10 independent stages exceeds its p99 1% of the time. How often does a request hit at least one slow stage?
> $1 - 0.99^{10} = 9.56\%$. With 100 stages it is 63.40%: tails compound, so per-stage tails must be far tighter than the end-to-end target.

> [!question]- qd-lowlat-utilization | Service time is 300 ns. What is mean latency at 60% and 99% utilization in an M/M/1 model?
> $W = S / (1 - \rho)$: 750 ns at 60%, 30,000 ns at 99%. Queueing, not processing, dominates near saturation, so size for bursts with headroom.

> [!question]- qd-lowlat-coordinated-omission | What is coordinated omission?
> A closed-loop tester that waits for responses stops sending during a stall, so the delayed requests are never recorded. In the simulation, a 2 s stall left the naive p99 at 0.05 ms while the true p99 was 1430.05 ms. Measure from intended send times.

> [!question]- qd-lowlat-histogram | How do you record latencies on the hot path without distorting them?
> Into a preallocated log-linear histogram (HdrHistogram style): O(1) `record`, no allocation, bounded relative error, percentiles read off afterwards; or copy raw timestamps to a ring drained by another thread.

## In this repo and SDE-Interview-Prep

- Code: [latency_lab.cpp](code/cpp/latency_lab.cpp) (clock, cache ladder, false sharing, branches, jitter), [microbenchmark_utils.hpp](code/cpp/microbenchmark_utils.hpp) (portable counters, percentiles, `LatencyHistogram`) with [tests/test_microbenchmark_utils.cpp](code/cpp/tests/test_microbenchmark_utils.cpp), [qd_latency_budget.py](code/python/qd_latency_budget.py), [qd_coordinated_omission.py](code/python/qd_coordinated_omission.py).
- Related: [Latency Arbitrage and Speed](../07-Market-Microstructure/10-Latency-Arbitrage-and-Speed.md), [Concurrency, Lock-Free Queues and Memory Pools](04-Concurrency-Lock-Free-and-Memory-Pools.md), [Market Data Feed Handlers and Protocols](08-Market-Data-Feed-Handlers-and-Protocols.md).
- [Low-latency systems vault (home) (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/00%20Home.md)
- [Latency numbers every trading engineer knows (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/04%20-%20Hardware%20Mechanical%20Sympathy/Latency%20Numbers%20Every%20Trading%20Engineer%20Knows.md)
- [False sharing and cache contention (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/04%20-%20Hardware%20Mechanical%20Sympathy/False%20Sharing%20and%20Cache%20Contention.md)
- [Kernel boot parameters for core isolation (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/05%20-%20OS%20%26%20Kernel%20Tuning/Kernel%20Boot%20Parameters%20for%20Core%20Isolation.md)
- [Kernel bypass technologies overview (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/06%20-%20Networking/Kernel%20Bypass%20Technologies%20Overview.md)
- [Clock sources and hardware timestamping (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/07%20-%20Time%20%26%20Measurement/Clock%20Sources%20and%20Hardware%20Timestamping.md)
- [Coordinated omission (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/07%20-%20Time%20%26%20Measurement/Coordinated%20Omission%20in%20Low%20Latency%20Systems.md)
- [Performance engineering (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/12-Performance-Engineering/README.md)

## Further reading

- John Hennessy and David Patterson, *Computer Architecture: A Quantitative Approach*, 6th edition (Morgan Kaufmann, 2017), chapter 2 and appendix B (memory hierarchy).
- Ulrich Drepper, "What Every Programmer Should Know About Memory" (2007).
- Brendan Gregg, *Systems Performance*, 2nd edition (Addison-Wesley, 2020), chapters 6 (CPUs), 7 (memory) and 10 (network).
- Jeffrey Dean and Luiz Andre Barroso, "The Tail at Scale", *Communications of the ACM* 56(2), 2013.
- Gil Tene, "How NOT to Measure Latency" (talk, 2015), and the HdrHistogram library.
- Commission Delegated Regulation (EU) 2017/574 (RTS 25) on the accuracy of business clocks.
- IEEE 1588-2019, Precision Time Protocol.
- DPDK Programmer's Guide (dpdk.org) and the AMD Solarflare OpenOnload and ef_vi user guides.
