# Data Structures & Algorithms for Quants

Quant coding interviews differ from Big Tech. They focus less on "invert a binary tree" and more on structures used in **Trading Engines** and **Data Analysis**.

## ⚡ Critical Data Structures

### 1. Hash Maps (Dictionaries)
*   **Use Case:** Order ID lookup, Symbol mapping.
*   **Complexity:** O(1) average insert/lookup.
*   **Pitfall:** Worst case O(n) with collisions. In Low Latency C++, we use "Open Addressing" to avoid pointer chasing (cache misses).

### 2. Priority Queues (Heaps)
*   **Use Case:** **The Limit Order Book (LOB)**.
    *   *Bids* are a Max-Heap (Highest price is best).
    *   *Asks* are a Min-Heap (Lowest price is best).
*   **Complexity:** O(log n) to add/remove an order. O(1) to peek top.
*   **Alternative:** Balanced Binary Search Trees (TreeMap) allow O(log n) cancellation of *any* order, not just the top.

### 3. Ring Buffers (Circular Arrays)
*   **Use Case:** Lock-free queues (SPSC/MPMC) for passing messages between threads (e.g., Network -> Strategy).
*   **Why?** No dynamic memory allocation (no `new`/`malloc`), no GC. Constant memory footprint.

### 4. 1D Arrays (Vectors)
*   **Use Case:** Time Series data.
*   **Optimization:** **Cache Locality**. Iterating over a contiguous array is orders of magnitude faster than a Linked List due to CPU prefetching.

## 🧮 Essential Algorithms

### 1. Sliding Window
*   **Problem:** "Calculate the 10-day Moving Average."
*   **Optimization:** Don't re-sum the whole window. `Sum_new = Sum_old - x_leaving + x_entering`. O(1).

### 2. Median Maintenance
*   **Problem:** "Compute the running median of a stream of prices."
*   **Solution:** Two Heaps.
    *   Max-Heap for the lower half.
    *   Min-Heap for the upper half.
    *   Balance them so size diff <= 1. Median is top of larger heap (or average of tops).

### 3. Quickselect
*   **Problem:** "Find the k-th largest element (e.g., 95th percentile Latency)."
*   **Complexity:** O(n) average.

## 🛠️ Practice
*   Implement a **Matching Engine**: Takes Buy/Sell orders and executes matches.
*   Implement a **Moving Median** class.
