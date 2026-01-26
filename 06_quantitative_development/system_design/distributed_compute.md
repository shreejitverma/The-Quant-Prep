# Distributed Computing in Finance

Quantitative firms run massive simulations (e.g., VaR, Greeks) that cannot fit on a single machine.

##  Core Architectures

### 1. The Compute Grid (HTC)
*   **High Throughput Computing:** Unlike HPC (tightly coupled MPI), Finance uses loose coupling.
*   **Master-Worker Pattern:**
    *   **Master:** Splits a portfolio into thousands of trades/scenarios.
    *   **Workers:** Calculate `PV` (Present Value) and `Greeks` for sub-portfolios.
    *   **Aggregation:** Master sums up the results (MapReduce style).

### 2. DAG (Directed Acyclic Graph) Schedulers
*   Pricing complex derivatives involves dependencies (e.g., Calibrate Curve -> Price Swap).
*   Tools: **Airflow**, **Luigi**, or proprietary graph engines.

### 3. Data Locality
*   **The Problem:** Moving terabytes of tick data to compute nodes is slow.
*   **Solution:** Move compute to data. Use distributed filesystems (HDFS, S3) or columnar stores (KDB+, Parquet).

##  Caching & Memoization
*   **Memoization:** If inputs (Spot, Vol, Time) haven't changed, don't re-price the option. Return cached Greeks.
*   **Dependency Graph:** Only re-calculate downstream nodes affected by an upstream market data change.

##  Key Interview Question
*"Design a system to calculate the real-time VaR (Value at Risk) of a global multi-asset portfolio with 1 million trades."*
*   **Hint:** Sharding by Asset Class vs Sharding by Risk Factor.
