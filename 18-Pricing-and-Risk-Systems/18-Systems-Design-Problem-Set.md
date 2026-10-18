---
type: problem-set
track: [quant-dev, quant-risk]
tier: senior
status: solid
prereqs: [industry-landscape]
est_hours: 4
sources: [Alex Xu and Sahn Lam - System Design Interview: An Insider's Guide (Volume 2 Byte Byte Go 2022), Martin Kleppmann - Designing Data-Intensive Applications: The Big Ideas Behind Reliable Scalable and Maintainable Systems (O'Reilly Media 2017), Christian Voigt - Financial Systems Architecture: High Performance Trading and Risk Systems (Palgrave Macmillan 2020), Antoine Savine - Modern Computational Finance: AAD and Parallel Simulations (John Wiley & Sons 2018), Basel Committee on Banking Supervision - Minimum Capital Requirements for Market Risk (Bank for International Settlements d457 2019)]
---

# Systems Design Problem Set: Quantitative Financial Infrastructure

## TL;DR

This comprehensive system design problem set tests the architectural, quantitative, and software engineering skills required to design enterprise financial infrastructure.
It presents five end-to-end quantitative systems design case studies:
1. **Design an Enterprise FRTB Standardised Approach (SbM) Aggregation Engine** (evaluating 20 million Greeks, 105 risk buckets, and 3 supervisory correlation regimes within an interactive SLA).
2. **Design an Ultra-Low Latency Pre-Deal Incremental XVA Quoting Service** (delivering incremental portfolio CVA in microseconds via second-order Taylor expansion proxies).
3. **Design a Resilient End-of-Day Risk Batch Orchestrator** (evaluating Critical Path Method schedules, task floats, and dynamic sub-DAG recovery for late trade bookings).
4. **Design a Reactive Multi-Curve and Volatility Surface Engine** (comparing reader contention between shared mutexes and lock-free atomic pointer exchanges).
5. **Model Electronic Trading Gateway Queueing Latencies under Non-Linear Load Spikes** ($M/M/1$ queueing models analyzing average and $p99$ tail latencies under $70\%$ versus $95\%$ utilization).
All numerical models in this note are verified by [sys_problem_set.py](code/sys_problem_set.py).

## Learning objectives

- Formulate end-to-end system designs for complex capital markets pricing and risk infrastructure.
- Establish architectural boundaries, latency budgets, data schemas, and compute scaling strategies.
- Design low-latency pre-deal analytics pipelines delivering incremental portfolio Greek and XVA quotes in microseconds.
- Apply queueing theory ($M/M/1$) to calculate average and tail ($p99$) latencies in high-throughput electronic gateways.
- Architect enterprise-scale batch orchestration engines capable of self-healing from node crashes and data anomalies using Critical Path Method analysis.
- Analyze trade-offs between accuracy, compute cost, memory footprint, and network serialization overhead.
- Master senior-level quantitative software architecture interview questions and design presentations.

## Core concepts

### 1. The Standard System Design Framework for Capital Markets

When presenting a financial system design:
1. **Scope & Requirements:**
   - Functional: What business flows, products, and metrics must be computed?
   - Non-Functional: Latencies (p50, p99), throughput (trades/sec), precision (IEEE 754 determinism), SLAs, data retention, regulatory compliance (SR 11-7, BCBS 239).
2. **High-Level Architecture:**
   - Data ingestion, calculation core, caching tier, and downstream consumers.
3. **Deep Dives:**
   - Algorithmic complexity, concurrency models (lock-free vs actor), data models, network protocols (gRPC, Aeron, Kafka).
4. **Failure Modes & Bottlenecks:**
   - Network partitions, memory exhaustion, floating-point drift, cache stampedes.

---

## Worked examples

### Case Study 1: Enterprise FRTB Standardised Approach (SbM) Grid Sizing and Bandwidth

A global dealer bank designs an FRTB Sensitivities-Based Method (SbM) engine aggregating market risk across the enterprise trading book:
- **Portfolio Scale:** $P = 500,000$ active trading positions across rates, credit, equities, and FX.
- **Sensitivity Density:** Each derivative position generates on average $m = 40$ non-zero Delta and Vega Greek sensitivities across risk pillars.
- **Total Sensitivity Volume:**
  $$\text{Sensitivities} = 500,000 \times 40 = 20,000,000\text{ sensitivities}$$
- **Packed Binary Struct Serialization:**
  Sensitivities are streamed from pricing worker nodes to the risk aggregator as packed 24-byte binary structs:
  ```cpp
  struct __attribute__((packed)) SensitivityRecord {
      int64_t trade_id;        // 8 bytes: unique trade identifier
      int32_t risk_factor_id;  // 4 bytes: indexed curve pillar / vol bucket
      int16_t bucket_id;       // 2 bytes: supervisory regulatory bucket (1..120)
      double  s_k;             // 8 bytes: net Greek sensitivity value
      uint16_t padding;        // 2 bytes: 64-bit memory alignment padding
  };                           // Total = 24 bytes
  ```
- **Network Ingestion Payload:**
  $$\text{Payload} = 20,000,000 \times 24\text{ bytes} = 480,000,000\text{ bytes} = 480.0\text{ MB}$$
- **Network Transfer Time:**
  Streaming over a dedicated $10\text{ Gbps}$ optical fabric ($1,250\text{ MB/sec}$ wire throughput):
  $$\text{Ingestion Latency} = \frac{480.0\text{ MB}}{1,250.0\text{ MB/sec}} = 0.384\text{ seconds}$$
- **Across-Bucket Correlation Aggregation:**
  - Across $7$ asset classes with an average of $15$ regulatory buckets each, the firm maintains $105$ total bucket exposure sums $S_b = \sum_{k \in b} WS_k$.
  - SbM requires evaluating capital across three correlation regimes: Medium ($\mathbf{\Omega}_{\text{med}}$), High ($\mathbf{\Omega}_{\text{high}}$), and Low ($\mathbf{\Omega}_{\text{low}}$).
  - Total across-bucket quadratic multiplications:
    $$\text{FLOPs} = 3\text{ scenarios} \times 105^2 = 3 \times 11,025 = 33,075\text{ multiplications}$$
  - Evaluated on modern AVX-512 vector units in less than $0.05\text{ milliseconds}$, enabling real-time capital aggregation upon sensitivity receipt.

---

### Case Study 2: Ultra-Low Latency Pre-Deal Incremental XVA Analytical Proxy

An automated RFQ quoting gateway must evaluate incremental counterparty exposure $\Delta\text{XVA}$ in under $50\text{ milliseconds}$:
- **Netting Set Baseline Distribution:**
  - Overnight Monte Carlo batch pre-calculates the uncollateralized netting set exposure: mean $\mathbb{E}[V_{\text{base}}] = \$15,000,000$ and volatility $\sigma_{\text{base}} = \$8,000,000$.
  - Standardized distance to the money:
    $$Z_{\text{base}} = \frac{\mathbb{E}[V_{\text{base}}]}{\sigma_{\text{base}}} = \frac{\$15,000,000}{\$8,000,000} = 1.875$$
  - Probability metrics: $\phi(1.875) = 0.068786$, $\Phi(1.875) = 0.969604$.
  - Baseline Expected Positive Exposure (EPE):
    $$\text{EPE}_{\text{base}} = \sigma_{\text{base}} [Z_{\text{base}} \Phi(Z_{\text{base}}) + \phi(Z_{\text{base}})] = 8,000,000 \times [1.875 \times 0.969604 + 0.068786] = \$15,094,345$$
- **Incoming Trade Quote:**
  - A client requests a quote for a $10$-year interest rate swap with forward standalone value $v_{\text{trade}} = \$1,500,000$.
- **Second-Order Taylor Series Incremental Exposure:**
  $$\Delta\text{EPE}_{\text{Taylor}} \approx \Phi(Z_{\text{base}}) v_{\text{trade}} + \frac{1}{2} \frac{\phi(Z_{\text{base}})}{\sigma_{\text{base}}} v_{\text{trade}}^2$$
  - First-order linear sensitivity:
    $$\text{Term}_1 = 0.969604 \times \$1,500,000 = \$1,454,405$$
  - Second-order convexity adjustment:
    $$\text{Term}_2 = \frac{1}{2} \times \frac{0.068786}{8,000,000} \times (1,500,000)^2 = \$9,673$$
  - Total Taylor approximation:
    $$\Delta\text{EPE}_{\text{Taylor}} = \$1,454,405 + \$9,673 = \$1,464,079$$
- **Exact Full Distribution Comparison:**
  - Updated expected portfolio value: $\mathbb{E}[V_{\text{new}}] = \$15,000,000 + \$1,500,000 = \$16,500,000$.
  - Updated standardized score: $Z_{\text{new}} = \frac{16.5}{8.0} = 2.0625$.
  - Exact updated EPE: $\text{EPE}_{\text{new}} = \$16,557,360$.
  - Exact incremental exposure:
    $$\Delta\text{EPE}_{\text{exact}} = \$16,557,360 - \$15,094,345 = \$1,463,015$$
  - Approximation error:
    $$\text{Absolute Error} = |\$1,464,079 - \$1,463,015| = \$1,063$$
    $$\text{Relative Error} = \frac{\$1,063}{\$1,463,015} = 0.07\%$$

The analytical Taylor expansion proxy evaluates in $1.2\mu\text{s}$ while achieving $0.07\%$ accuracy relative to full numerical integration, easily meeting the $50\text{ ms}$ electronic quoting SLA.

---

### Case Study 3: Resilient End-of-Day Risk Batch Orchestrator and Critical Path Method

An investment bank manages a nightly risk batch across $50,000$ virtual cores under a strict $3$-hour ($180\text{ minute}$) SLA:
- **Dependency DAG and Task Durations:**
  1. Task A: Market Data Snap ($15.0\text{ min}$).
  2. Task B: Multi-Curve Calibration ($20.0\text{ min}$, depends on A).
  3. Task C: Trade Extraction & Normalization ($25.0\text{ min}$).
  4. Task D: Pricing & Greek Grid ($50.0\text{ min}$, depends on B and C).
  5. Task E: Monte Carlo VaR/ES Simulation ($35.0\text{ min}$, depends on D).
  6. Task F: FRTB SbM Aggregation ($20.0\text{ min}$, depends on D).
  7. Task G: PnL Explain & Attribution ($25.0\text{ min}$, depends on D).
  8. Task H: General Ledger Sign-off ($15.0\text{ min}$, depends on E, F, and G).
- **Critical Path Method (CPM) Forward Pass:**
  - Path 1: $A \to B \to D \to E \to H = 15.0 + 20.0 + 50.0 + 35.0 + 15.0 = 135.0\text{ minutes}$ ($2.25\text{ hours}$).
  - Path 2: $C \to D \to E \to H = 25.0 + 50.0 + 35.0 + 15.0 = 125.0\text{ minutes}$.
  - The critical path is Path 1 ($135.0\text{ minutes}$).
- **Task Floats (Slack):**
  - Trade Extraction (Task C): Float $= 135.0 - 125.0 = 10.0\text{ minutes}$.
  - FRTB SbM Aggregation (Task F): Float $= 35.0 - 20.0 = 15.0\text{ minutes}$.
  - PnL Explain (Task G): Float $= 35.0 - 25.0 = 10.0\text{ minutes}$.
- **Late Trade Sub-DAG Invalidation and Rerun:**
  - A batch of $500$ late trade amendments arrives while downstream risk simulations are executing.
  - The orchestrator dynamically spawns an incremental sub-DAG on an elastic $4,000$-core cloud burst queue:
    $$\Delta C = 1.0\text{ min}, \quad \Delta D = 3.5\text{ min}, \quad \Delta E = 2.0\text{ min}, \quad \Delta H = 1.0\text{ min}$$
    $$\text{Incremental Rerun Delay} = 1.0 + 3.5 + 2.0 + 1.0 = 7.5\text{ minutes}$$
  - Total batch completion with late-trade recovery:
    $$\text{Total Duration} = 135.0\text{ min} + 7.5\text{ min} = 142.5\text{ minutes}$$
  - Remaining SLA margin:
    $$\text{Slack} = 180.0\text{ min} - 142.5\text{ min} = 37.5\text{ minutes}$$

---

### Case Study 4: Reactive Multi-Curve Engine: Mutex vs. Lock-Free Atomic `shared_ptr`

A central yield curve engine serves $10,000$ real-time pricing queries per second across $64$ concurrent reader threads:
- **Architecture A (Shared Mutex: `std::shared_mutex`):**
  - While reading threads acquire shared ownership, multi-core cache coherency protocols require invalidating the lock's cache line across all CPU sockets upon each acquire/release.
  - Under $64$-thread contention, read acquisition latency spikes from $0.12\mu\text{s}$ to $4.8\mu\text{s}$.
  - Total synchronization CPU tax:
    $$\text{Lock Tax} = \frac{10,000\text{ queries/s} \times 4.8\mu\text{s}}{1,000\mu\text{s/ms}} = 48.0\text{ ms of CPU time per second}$$
- **Architecture B (Lock-Free Atomic Pointer Exchange: `std::atomic_load`):**
  - Calibrated curve snapshots are published as immutable C++ objects wrapped in `std::shared_ptr<const YieldCurve>`.
  - Readers acquire an immutable snapshot via atomic reference counting in $0.025\mu\text{s}$ ($25\text{ nanoseconds}$).
  - Total memory overhead:
    $$\text{Atomic Overhead} = \frac{10,000 \times 0.025\mu\text{s}}{1,000\mu\text{s/ms}} = 0.25\text{ ms of CPU time per second}$$
  - Performance Improvement:
    $$\text{Contention Reduction Factor} = \frac{4.8\mu\text{s}}{0.025\mu\text{s}} = 192.0\times$$

Publishing immutable curves via atomic pointer exchanges eliminates lock contention and yields a $192.0\times$ speedup in snapshot acquisition.

---

### Case Study 5: Pre-Trade Gateway $M/M/1$ Queueing Model and Congestion Sizing

A pre-trade risk gateway evaluates order size, credit headroom, and price bands before routing to exchanges:
- **Baseline Service Metrics:**
  - Dedicated risk check kernel service time: $S = 10.0\mu\text{s}$ per order.
  - Service rate:
    $$\mu = \frac{1,000,000\mu\text{s/s}}{10.0\mu\text{s/order}} = 100,000\text{ orders/second}$$
- **Case A: Normal Trading Conditions ($70\%$ Server Utilization, $\rho = 0.70$):**
  - Arrival rate: $\lambda = 0.70 \times 100,000 = 70,000\text{ orders/second}$.
  - Average total system latency (service time $+$ waiting time):
    $$W = \frac{1}{\mu - \lambda} = \frac{1}{100,000 - 70,000} = \frac{1}{30,000}\text{ s} = 33.3\mu\text{s}$$
  - Average queue wait time:
    $$W_q = W - S = 33.3\mu\text{s} - 10.0\mu\text{s} = 23.3\mu\text{s}$$
  - Tail $p99$ system latency:
    $$t_{p99} = \frac{\ln(100)}{\mu(1 - \rho)} = \frac{4.60517}{30,000}\text{ s} = 153.5\mu\text{s}$$
- **Case B: Market Volatility Spike ($95\%$ Server Utilization, $\rho = 0.95$):**
  - Arrival rate: $\lambda = 0.95 \times 100,000 = 95,000\text{ orders/second}$.
  - Average total system latency:
    $$W = \frac{1}{\mu - \lambda} = \frac{1}{100,000 - 95,000} = \frac{1}{5,000}\text{ s} = 200.0\mu\text{s}$$
  - Average queue wait time:
    $$W_q = 200.0\mu\text{s} - 10.0\mu\text{s} = 190.0\mu\text{s}$$
  - Tail $p99$ system latency:
    $$t_{p99} = \frac{\ln(100)}{\mu(1 - \rho)} = \frac{4.60517}{5,000}\text{ s} = 921.0\mu\text{s}$$
- **Congestion Factor:**
  $$\text{Latency Expansion} = \frac{200.0\mu\text{s}}{33.3\mu\text{s}} = 6.0\times$$

A $35.7\%$ increase in order flow (from $70\text{k}$ to $95\text{k}$ orders/sec) triggers a $6.0\times$ non-linear explosion in average latency and expands $p99$ tail latency from $153.5\mu\text{s}$ to $921.0\mu\text{s}$.
This demonstrates why electronic gateways must provision capacity for peak burst loads to prevent queue buildup.

---

## Pitfalls

- **Designing Without Stated Latency and Volume Assumptions:** Proposing complex Monte Carlo architectures for high-frequency flow trading or proposing single-node memory structures for massive cross-asset portfolios fails system design interviews immediately.
- Always state volumes, packet sizes, and latencies first.
- **Neglecting Failure Modes:** A system design that only explains the "happy path" without detailing handling of network partitions, database deadlocks, straggling workers, and data corruption is incomplete.
- **Conflating Asynchronous Messaging with Low Latency:** While Kafka is excellent for high-throughput durable event streaming, introducing multi-broker disk-flush overhead into an in-line sub-50 microsecond pre-trade risk gateway creates unacceptable latency.
- Use kernel-bypass shared memory or Aeron IPC instead.
- **Ignoring Data Gravity and Cloud Egress Costs:** Designing a hybrid architecture where raw scenario grids are computed in the cloud and streamed uncompressed back to on-prem databases creates multi-million dollar annual bandwidth invoices.
- Aggregate in the cloud before egress.
- **Failing to Enforce Idempotency in Distributed Queues:** Distributed queues guarantee "at-least-once" delivery, not "exactly-once".
- Failing to deduplicate tasks via unique idempotency keys leads to double-counted trades and corrupted risk aggregations.

## Interview questions

> [!question]- sys-18-01 | How do you size the compute grid for an FRTB Sensitivities-Based Method (SbM) engine?
> Sizing requires multiplying: $\text{Positions} \times \text{Risk Factors} \times \text{Greeks per position}$.
> Using Adjoint Algorithmic Differentiation (AAD), generating all Delta and Vega sensitivities takes a constant multiple ($\approx 3\times$ to $4\times$) of base pricing runtime.
> Curvature requires two revaluations per risk factor.
> Dividing total core-seconds by the target batch window SLA determines the required core count.

> [!question]- sys-18-02 | How can pre-deal incremental XVA ($\Delta\text{XVA}$) be evaluated in under 50 milliseconds?
> Pre-deal engines do not re-run full Monte Carlo simulations across entire netting sets during client RFQs.
> They pre-calculate and cache baseline netting set exposure distributions overnight, evaluate the candidate trade analytically forward in time, and use second-order Taylor expansions or pre-trained machine learning surrogates to approximate incremental exposure.

> [!question]- sys-18-03 | In a reactive curve service, how do you achieve lock-free thread safety across thousands of reader threads?
> By publishing immutable calibrated curves through atomic shared-pointer operations.
> Recalibrations execute on background threads, and once verified, an atomic store updates the active reference.
> Readers avoid application-managed mutexes, but the standard does not guarantee atomic shared-pointer operations are lock-free; measure contention and latency on the target implementation.

> [!question]- sys-18-04 | What is the Critical Path Method (CPM) and how does it prevent EOD risk batch SLA breaches?
> CPM identifies the longest sequence of dependent tasks that have zero float (slack).
> It reveals the true operational bottlenecks; optimizing tasks off the critical path yields zero SLA reduction, so cluster resources must be prioritized for critical path tasks.

> [!question]- sys-18-05 | What is the difference between Single-Instruction Multiple-Data (SIMD) and Single-Instruction Multiple-Threads (SIMT)?
> SIMD (used in CPU AVX-512) executes an identical instruction on multiple data elements packed into wide CPU vector registers.
> SIMT (used in NVIDIA GPUs) executes instructions across independent threads organized into warps, where each thread has its own register state, enabling massive scale for Monte Carlo path generation.

> [!question]- sys-18-06 | How does an event-sourced trade repository recover from corrupted state?
> Because state is stored as an immutable log of events (Booked, Amended, Novated) rather than destructive in-place updates, corrupted state is resolved by replaying the event log from genesis (or from the latest verified snapshot) up to the target timestamp, bypassing bad events.

> [!question]- sys-18-07 | Why are Aeron and LMAX Disruptor preferred over RabbitMQ or Kafka in electronic trading gateways?
> RabbitMQ and Kafka introduce TCP socket buffers, context switches, garbage collection pauses, and disk-commit delays, resulting in millisecond latencies.
> Aeron and Disruptor operate over shared memory (IPC) or UDP kernel-bypass with pre-allocated zero-allocation memory buffers, achieving sub-microsecond latencies with zero garbage collection.

> [!question]- sys-18-08 | How does an enterprise risk engine handle a network partition during an EOD batch?
> Compute workers operate with local task timeouts and write completed chunks to durable distributed object storage with unique idempotency hashes.
> Schedulers use heartbeat probes: if a worker becomes unreachable, its incomplete chunk is reassigned to another node while completed chunks remain preserved.

> [!question]- sys-18-09 | What is the "Straggler Problem" in distributed Monte Carlo pricing, and how is it mitigated?
> The straggler problem occurs when a few slow worker nodes delay the entire batch.
> It is mitigated by work-stealing (idle workers pull remaining tasks from lagging queues) and speculative execution (launching duplicate tasks for lagging jobs and taking whichever finishes first).

> [!question]- sys-18-10 | What is the difference between horizontal scaling and vertical scaling in quantitative risk architectures?
> Vertical scaling increases the resources of a single server (faster clock speeds, more RAM, liquid-cooled CPUs), which is essential for low-latency flow trading and single-threaded DAG solvers.
> Horizontal scaling adds more nodes to a cluster, which is ideal for embarrassingly parallel workloads like Monte Carlo path simulation and scenario grid fan-out.

> [!question]- sys-18-11 | Why is data compression essential between the pricing grid and the risk aggregation cube?
> Streaming raw, uncompressed scenario vectors ($500,000\text{ positions} \times 1,000\text{ scenarios} \times 8\text{ bytes} = 4\text{ GB}$) across network interfaces creates severe network congestion.
> Using columnar compression (Gorilla, ZSTD) and zero-copy Apache Arrow formats shrinks network transmission by 80%, accelerating aggregation.

> [!question]- sys-18-12 | How do you prevent cache stampedes (thundering herd) when a benchmark yield curve is recalibrated?
> When a master curve is invalidated, thousands of pricing workers might simultaneously attempt to recalculate it.
> This is mitigated by mutex-locked single-flight evaluation (only the first worker calculates while others wait) or pre-warming caches in the background before retiring old curve versions.

> [!question]- sys-18-13 | What is the purpose of the Weighted To Reference (WTR) ratio in the FRTB Default Risk Charge?
> WTR measures the net hedging efficiency between long and short debt positions of the same obligor but different maturities.
> It penalizes basis risk by reducing the offsetting credit given to short positions if their maturities do not match the long exposure.

> [!question]- sys-18-14 | What is the difference between active-active and active-passive disaster recovery?
> In active-passive, the secondary site sits idle (warm standby) and receives replicated data, taking minutes to hours to activate upon failure.
> In active-active, both data centers process live transactions simultaneously, providing instantaneous failover and zero downtime if one site fails.

> [!question]- sys-18-15 | How does bitemporality resolve regulatory audit inquiries regarding past risk reports?
> It allows querying the database using two timestamps: Valid Time (the economic date being analyzed) and Transaction Time (the date the query is simulated from).
> This guarantees that an auditor can reproduce the exact risk report generated on October 1st, even if trades were retroactively amended on October 5th.

## Further reading

- Xu, Alex and Lam, Sahn. *System Design Interview: An Insider's Guide (Volume 2)*. Byte Byte Go, 2022.
- Kleppmann, Martin. *Designing Data-Intensive Applications: The Big Ideas Behind Reliable Scalable and Maintainable Systems*. O'Reilly Media, 2017.
- Voigt, Christian. *Financial Systems Architecture: High Performance Trading and Risk Systems*. Palgrave Macmillan, 2020.
- Savine, Antoine. *Modern Computational Finance: AAD and Parallel Simulations*. John Wiley & Sons, 2018.
- Basel Committee on Banking Supervision. *Minimum Capital Requirements for Market Risk*. Bank for International Settlements d457, 2019.
