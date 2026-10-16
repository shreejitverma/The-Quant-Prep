---
type: concept
track: [quant-dev, quant-risk]
tier: senior
status: draft
prereqs: [model-governance]
est_hours: 4
sources: [Martin Kleppmann - Designing Data-Intensive Applications (2017), Christian Voigt - High-Reliability Financial Software Architecture (2022), Betsy Beyer et al. - Site Reliability Engineering: How Google Runs Production Systems (2016)]
---

# Non-Functional Architecture and Production Operations

## TL;DR

While functional design focuses on mathematical pricing and risk models, non-functional design determines whether enterprise trading systems survive production stress, regulatory audits, and infrastructure disasters.
Core non-functional pillars include: **Bit-Exact Determinism** (guaranteeing that identical portfolio runs yield identical binary numbers regardless of thread scheduling or CPU architecture); **Bitemporality** (enabling point-in-time reconstruction of historical books as known on any past date); **Security and Chinese Walls** (strictly separating public trading desks from private investment banking data); **Disaster Recovery (DR)** (enforcing zero Recovery Point Objective $\text{RPO} = 0$ for trade capture and $< 15\text{ minutes}$ for risk batches); and **Cloud FinOps** (optimizing the cost per trade evaluated using dynamic spot-instance autoscaling).
Without rigorous non-functional engineering, institutions face regulatory fines, catastrophic trading halts, and unmanageable infrastructure costs.

## Learning objectives

- Guarantee bit-exact floating-point reproducibility across distributed multi-threaded CPU and GPU grids.
- Implement reproducible pseudo-random number generator (PRNG) pipelines for Monte Carlo simulations using deterministic seed leapfrogging.
- Architect bitemporal data repositories and cryptographic audit trails for historical regulatory reconstruction.
- Design Chinese Wall information barriers and Attribute-Based Access Control (ABAC) isolating trading desks from private market information.
- Formulate Disaster Recovery architectures achieving $\text{RPO} = 0$ and $\text{RTO} < 5\text{ minutes}$ across geographic data centers.
- Implement Cloud FinOps cost-governance frameworks tracking compute expenditure per trade and per risk scenario.

## Core concepts

### 1. Non-Functional Pillars for Capital Markets Infrastructure

```
+----------------------------------------------------------------------------------------------------+
| Dimension           | Architectural Mandate                      | Primary Failure Mode            |
+----------------------------------------------------------------------------------------------------+
| Determinism         | IEEE 754 compliance, fixed PRNG seeds      | Phantom PnL breaks between runs |
| Bitemporality       | Valid Time vs. Transaction Time tracking   | Inability to pass historical audit|
| Security & Walls    | ABAC entitlements, Kerberos / mTLS, KMS    | Insider trading, regulatory fine|
| Disaster Recovery   | Synchronous cross-region replication (RPO=0)| Data loss during datacenter outage|
| Observability       | OpenTelemetry traces, Prometheus metrics   | Undetected queue stalls / breaks|
| Cloud FinOps        | Spot autoscaling, per-trade unit economics | Multi-million cloud budget blowup|
+----------------------------------------------------------------------------------------------------+
```

### 2. High-Availability & Disaster Recovery Topology

```mermaid
flowchart TB
    subgraph PrimaryDC["Primary Data Center (New York - Equinix NY4)"]
        Ingress1[Active Order Gateway]
        PrimaryDB[(Primary PostgreSQL / CockroachDB)]
        ComputeGrid1[Active Compute Grid (5,000 Cores)]
    end

    subgraph SyncLink["Ultra-Low Latency Dark Fiber Link"]
        DirectConnect[Synchronous Storage Replication: RPO = 0]
    end

    subgraph SecondaryDC["Secondary DR Site (Chicago - Equinix CH1)"]
        Ingress2[Standby Order Gateway]
        StandbyDB[(Standby Replica DB: Read-Only)]
        ComputeGrid2[Standby Compute Grid (Warm / Burst)]
    end

    subgraph CloudBurst["Public Cloud Burst Tier (AWS / GCP)"]
        SpotWorkers[Ephemeral Spot Grid Workers (50,000 Cores)]
        ObjectStore[(Encrypted S3 Parquet Data Lake)]
    end

    Ingress1 --> PrimaryDB
    PrimaryDB --> ComputeGrid1
    PrimaryDB ==>|Sync WAL Streaming| DirectConnect
    DirectConnect ==> StandbyDB

    StandbyDB -.->|Heartbeat Health Check| Ingress2
    ComputeGrid1 -.->|EOD Burst Workload| SpotWorkers
    SpotWorkers --> ObjectStore
```

### 3. Floating-Point Non-Determinism and Reproducibility

In parallel computing, calculating a portfolio sum $S = \sum_{i=1}^N v_i$ using standard multi-threaded reductions produces non-deterministic values:
- Floating-point addition is non-associative: $(a + b) + c \neq a + (b + c)$.
- If thread 1 sums items $[1 \dots 1000]$ and thread 2 sums $[1001 \dots 2000]$, slight variations in thread completion times change the order of addition, altering the least-significant bits.
- This creates "phantom PnL breaks" where rerunning the exact same portfolio produces an unexplained variance of several thousand dollars.
- **Architectural Solution:**
  1. Use deterministic reduction trees with fixed summation topologies.
  2. Implement **Kahan Compensated Summation** or fixed-point integer scaling:

$$\text{Error} = (a + b) - a - b$$

  3. Disable unsafe compiler flags (strictly avoid `-ffast-math`; enforce `-ffp-model=precise`).

### 4. Deterministic Multi-Threaded Random Number Generation

Monte Carlo simulations require trillions of pseudo-random numbers:
- If threads draw numbers from a single shared PRNG with a mutex lock, lock contention collapses performance.
- If threads instantiate separate PRNGs without coordination, overlapping paths introduce statistical bias.
- **Leapfrogging / Block Skipping:**
  Using counter-based generators (such as Philox) or Sobol quasi-random sequence skip algorithms:
  A worker thread $k$ out of $M$ total threads evaluating path $p$ jumps directly to seed index $p \times \text{Steps}$ in $O(1)$ time without evaluating prior paths:

$$\text{State}(p) = \text{State}(0) + p \times \text{Offset}$$

  This guarantees bit-exact, identical Monte Carlo paths regardless of whether 1 core or 1,000 cores are used.

## Worked examples

### Example 1: Kahan Compensated Summation Algorithm

A risk engine sums $1,000,000$ small trade sensitivity contributions ($v_i = 0.0001$) into a large portfolio base ($S = 100,000.00$):
- Standard Summation:
  - Adding $0.0001$ to $100,000.00$ in single precision (24-bit significand) drops the low bits because $100,000 \approx 2^{16.6}$, while $0.0001 \approx 2^{-13.3}$. The scale difference exceeds the 24-bit precision window, causing the addition to vanish: $100,000.0 + 0.0001 = 100,000.0$.
  - After $1,000,000$ additions, the accumulated sum is still $100,000.00$ instead of $100,100.00$ (a $\$100$ error).

Kahan Summation Algorithm (using single precision to match the standard-summation comparison):
```cpp
float sum = 100000.0f;
float c = 0.0f;

for (float val : trades) {
    float y = val - c;
    float t = sum + y;
    c = (t - sum) - y;
    sum = t;
}
```

By tracking low-order rounding error in `c`, Kahan summation can recover contributions that ordinary single-precision addition loses. Its results are more accurate, but bit-for-bit agreement across CPU architectures requires additional controls on execution order, compiler behavior, and hardware.

### Example 2: Sizing Synchronous DR Replication Bandwidth (New York to Chicago)

A Tier-1 broker-dealer requires zero data loss ($\text{RPO} = 0$) for trade executions:
- Primary Data Center: Equinix NY4 (Secaucus, NJ).
- Disaster Recovery Site: Equinix CH1 (Chicago, IL).
- Fiber distance: $\approx 750\text{ miles}$. Speed-of-light round-trip latency: $T_{\text{RTT}} \approx 7.8\text{ milliseconds}$.
- Trading activity during peak market hours:
  - Trade execution rate: $4,500\text{ transactions/second}$.
  - Serialized transaction Write-Ahead Log (WAL) payload size: $1.8\text{ KB/transaction}$.
- Throughput sizing:
  - Average Data Flow: $4,500 \times 1.8\text{ KB} = 8,100\text{ KB/sec} = 8.1\text{ MB/sec}$.
  - Network Bandwidth: $8.1\text{ MB/sec} \times 8 = 64.8\text{ Mbps}$.
  - Applying a $3.0\times$ burst multiplier for market spikes:

$$\text{Required Dedicated Bandwidth} = 64.8\text{ Mbps} \times 3.0 \approx 194.4\text{ Mbps}$$

- Latency & Concurrency:
  - Because replication is **synchronous** ($\text{RPO} = 0$), the primary database will not acknowledge a trade commit to the client until the WAL entry is written to disk in Chicago.
  - Adding $7.8\text{ ms}$ round-trip latency to each synchronous commit throttles single-threaded throughput.
  - Sizing concurrent pipeline connections:
    To support $4,500\text{ commits/sec}$ with $7.8\text{ ms}$ latency:

$$N_{\text{concurrent\_connections}} = 4,500 \times 0.0078\text{ s} \approx 35.1 \implies 40\text{ parallel replication streams}$$

The bank provisions redundant $10\text{ Gbps}$ dedicated dark-fiber connections across 40 parallel WAL sender channels, guaranteeing $\text{RPO} = 0$ with sub-10ms commit confirmations.

### Example 3: Cloud FinOps Unit Economics: On-Demand vs. Spot Bursting

A quantitative risk department evaluates the cloud cost of running an intraday what-if pricing grid on AWS:
- Workload: $50,000$ virtual cores required for an intense 1-hour intraday scenario simulation.
- Option A: Provisioning an On-Premises Compute Cluster:
  - Purchasing 390 128-core AMD EPYC servers: $\$3,500,000$ capital expenditure.
  - Annual data center power, cooling, and maintenance: $\$450,000/\text{year}$.
  - Utilization: Used only 3 hours per day (12.5% utilization); 87.5% idle capacity.
- Option B: Dynamic Cloud Spot Bursting (AWS EC2 Spot Instances - `c7i.16xlarge`, 64 vCPUs):
  - Number of instances needed: $\frac{50,000}{64} = 782\text{ instances}$.
  - On-Demand hourly rate: $\$3.57\text{ per instance-hour}$.
  - Spot hourly rate (typical 68% discount): $\$1.14\text{ per instance-hour}$.
  - Cost for 1-hour simulation:
    $$\text{Hourly Cost} = 782 \times \$1.14 = \$891.48\text{ per run}$$
  - Annual cost for 250 trading days:
    $$\text{Annual Run Cost} = \$891.48 \times 250 = \$222,870\text{ per year}$$
- Financial Comparison:
  - Cloud Spot bursting costs $\$222,870/\text{year}$ versus $\$3,950,000$ in Year 1 on-premises capex/opex.
  - **Financial Savings:** $> 94\%$ reduction in total cost of ownership (TCO).

## Pitfalls

- **Permitting `-ffast-math` in Production Pricing Libraries:** Enabling fast-math reorders floating-point operations and ignores NaNs. It creates non-deterministic Greek sensitivities that vary depending on compiler versions.
- **Assuming Cloud Multi-AZ is Sufficient for Disaster Recovery:** Hosting primary and backup nodes in the same AWS region protects against rack failures but fails completely if a regional network partition or natural disaster strikes. True DR requires multi-region separation ($> 250\text{ miles}$).
- **Neglecting Bitemporal Schema Evolution:** Altering trade database schemas without migrating historical transaction-time audit logs prevents historical replays from parsing older serialized events.
- **Allowing Chinese Wall Breaches via Shared Data Lakes:** Dumping front-office M&A advisory data and flow trading books into the same un-partitioned data lake violates SEC/FINRA information barrier rules, triggering criminal insider trading liability.
- **Relying on Single-Threaded Seed Generators for Multi-Threaded Monte Carlo:** Having all worker threads read from a single shared PRNG instance creates severe lock contention, degrading parallel speedup to near-zero.

## Interview questions

> [!question]- sys-16-01 | Why is floating-point arithmetic non-associative, and how does it threaten risk determinism?
> Floating-point numbers have finite significand precision (53 bits in double precision).
> Reordering additions changes where truncation occurs: $(a + b) + c \neq a + (b + c)$.
> In distributed multi-threaded risk engines, non-deterministic addition order produces phantom PnL noise and breaks golden regression test suites.

> [!question]- sys-16-02 | What is Kahan Compensated Summation?
> Kahan summation is an algorithm that tracks accumulated low-order numerical truncation errors in a separate compensation variable.
> It recovers lost precision during summation, achieving error bounds independent of the number of additions $N$.

> [!question]- sys-16-03 | What is the difference between Recovery Point Objective (RPO) and Recovery Time Objective (RTO)?
> RPO is the maximum acceptable age of data lost when a disaster strikes (e.g., $\text{RPO} = 0$ means zero lost transactions).
> RTO is the maximum acceptable duration of system downtime before service is restored (e.g., $\text{RTO} < 5\text{ minutes}$).

> [!question]- sys-16-04 | How does synchronous replication achieve $\text{RPO} = 0$ and what is its performance penalty?
> Synchronous replication requires the primary database to wait for confirmation that the transaction log has been written to the remote backup site before acknowledging a commit.
> It guarantees zero data loss ($\text{RPO} = 0$), but penalizes latency by adding network round-trip time (e.g., 5-10ms) to every write transaction.

> [!question]- sys-16-05 | What is a "Chinese Wall" in capital markets technology?
> A Chinese Wall is an information barrier that prevents confidential material non-public information (MNPI) held by private-side divisions (e.g., M&A, Corporate Underwriting) from leaking to public-side divisions (e.g., Flow Trading, Market Making).
> It is enforced via strict Attribute-Based Access Control (ABAC), separate database instances, and network segmentation.

> [!question]- sys-16-06 | What is the difference between Role-Based Access Control (RBAC) and Attribute-Based Access Control (ABAC)?
> RBAC grants permissions based on static user job titles (e.g., "Trader").
> ABAC evaluates dynamic contextual attributes: user role, booking entity, trading desk, time of day, client jurisdiction, and security classification, providing fine-grained access control required for regulatory compliance.

> [!question]- sys-16-07 | How does leapfrogging enable deterministic random number generation across parallel threads?
> In leapfrogging, a counter-based PRNG computes the random state for path $p$ and step $s$ directly from an index function: $\text{State} = f(\text{Seed}, p, s)$ without sequential iteration.
> Threads can compute independent path blocks in any order while producing bit-exact identical outputs.

> [!question]- sys-16-08 | What is OpenTelemetry and how is it used in capital markets observability?
> OpenTelemetry is an open-source observability framework providing vendor-neutral APIs, SDKs, and tooling to generate, collect, and export distributed traces, metrics, and logs.
> It traces an order's lifecycle across microsecond network hops, pre-trade risk checks, and matching engines to isolate latency bottlenecks.

> [!question]- sys-16-09 | What is Cloud FinOps and why is it critical for quantitative analytics?
> FinOps is the cultural and operational discipline of managing cloud operational costs.
> It establishes unit economics (e.g., cost per Monte Carlo path or cost per risk report), monitors resource waste, and automates spot instance scheduling to prevent cloud compute budgets from escalating uncontrollably.

> [!question]- sys-16-10 | Why must regulatory audit stores enforce Write-Once-Read-Many (WORM) storage?
> Under SEC Rule 17a-4 and international compliance rules, electronic records of financial transactions must be preserved in an immutable format that prevents altering, overwriting, or deleting historical records for statutory retention periods (typically 7 to 10 years).

## Further reading

- Goldberg, David. *What Every Computer Scientist Should Know About Floating-Point Arithmetic*. ACM Computing Surveys, 1991.
- Federal Reserve Board. *Sound Practices to Strengthen Operational Resilience*. SR Letter 20-24, 2020.
- Higham, Nicholas J. *Accuracy and Stability of Numerical Algorithms*. 2nd Edition, SIAM, 2002.
- Kleppmann, Martin. *Designing Data-Intensive Applications*. O'Reilly Media, 2017.
