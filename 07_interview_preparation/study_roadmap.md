# 🗓️ The 8-Week Quant Interview Study Roadmap

This roadmap is designed to take you from "competent coder" to "Quant Developer/Researcher" ready for interviews at top firms.

## Phase 1: Foundations (Weeks 1-2)
**Goal:** Solidify Math and Basic CS.

*   **Week 1: Mathematics Refresher**
    *   **Probability:** Review "Green Book" questions (Expected Value, Bayes, Markov Chains).
    *   **Linear Algebra:** Eigenvectors, PCA, Cholesky Decomposition.
    *   **Stats:** OLS, Hypothesis Testing, Confidence Intervals.
    *   *Action:* Solve 5 probability puzzles daily from `07_interview_preparation/quant_math`.

*   **Week 2: Core CS & Python**
    *   **Algorithms:** Sliding Window, Heaps (Priority Queues), HashMaps.
    *   **Python:** Generators, Decorators, `pandas` optimization (vectorization).
    *   *Action:* Implement a Limit Order Book in Python.

## Phase 2: Financial Engineering & ML (Weeks 3-5)
**Goal:** Understand the domain and modeling.

*   **Week 3: Options & Stochastic Calculus**
    *   **Concepts:** Brownian Motion, Ito's Lemma, Black-Scholes Derivation.
    *   **Greeks:** Delta, Gamma, Vega hedging.
    *   *Action:* Code a Monte Carlo pricer in Python `03_financial_engineering`.

*   **Week 4: Machine Learning**
    *   **Classical ML:** Linear Regression, Ridge/Lasso, Random Forests, PCA.
    *   **Time Series:** ARIMA, GARCH, Cointegration.
    *   *Action:* Build a stock price predictor using Random Forest (avoiding look-ahead bias).

*   **Week 5: System Design (Quant Dev focus)**
    *   **Topics:** Distributed Systems, UDP/TCP, Multicasting.
    *   **Low Latency:** Lock-free programming, Cache locality.
    *   *Action:* Read `06_quantitative_development/system_design/distributed_compute.md`.

## Phase 3: Advanced & C++ (Weeks 6-7)
**Goal:** High-performance computing and C++ specific prep.

*   **Week 6: Modern C++**
    *   **Topics:** Smart Pointers, Move Semantics, Templates, STL containers.
    *   **Multithreading:** `std::thread`, Mutexes, Atomics, Memory Order.
    *   *Action:* Implement a thread-safe Queue in C++.

*   **Week 7: Advanced Finance & Strategies**
    *   **Strategies:** Arbitrage (Stat Arb), Market Making basics.
    *   **Market Microstructure:** Order types, Matching engines, Latency arbitrage.

## Phase 4: Mock & Final Polish (Week 8)
**Goal:** Simulate interview conditions.

*   **Mock Interviews:**
    *   Do 3 full-length mock interviews (1 hr Probability/Math, 1 hr Coding/C++, 1 hr System Design).
*   **Behavioral:** "Why this firm?", "Tell me about a time you optimized code."
*   **Review:** Go over your weak spots from the mocks.

## 📚 Daily Habits
1.  **Read Market News:** Bloomberg, FT (Know where the S&P 500 is).
2.  **One LeetCode:** Focus on Medium/Hard arrays/strings/DP.
3.  **Mental Math:** Practice 2-digit multiplication.
