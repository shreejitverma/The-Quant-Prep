# The Quant Prep
### The Ultimate Roadmap for Quantitative Developers & Researchers

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![C++](https://img.shields.io/badge/C%2B%2B-17%2F20-blue)](https://isocpp.org/)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

**The Quant Prep** is a comprehensive, open-source curriculum designed to bridge the gap between academic theory and the rigorous demands of top-tier financial firms like **Jane Street, Citadel, Hudson River Trading, Optiver, and Two Sigma**.

Whether you are aiming for a **Quantitative Researcher** role (heavy math/stats/ML) or a **Quantitative Developer** role (low-latency C++/systems), this repository provides the code, theory, and interview preparation you need.

---

##  The 8-Stage Learning Pathway

| Stage | Module | Focus Area | Key Topics |
| :--- | :--- | :--- | :--- |
| **01** | [**Foundations**](./01_foundations) | Core Skills | Linear Algebra, Probability, Algorithms, Python for Finance |
| **02** | [**Quant Data Analysis**](./02_quantitative_data_analysis) | Data Science | Time Series (ARIMA/GARCH), Econometrics, Exploratory Analysis |
| **03** | [**Financial Engineering**](./03_financial_engineering) | Mathematics | Derivatives Pricing, Black-Scholes, Stochastic Calculus, Monte Carlo |
| **04** | [**Machine Learning**](./04_machine_learning_and_ai) | AI/Alpha | Classical ML, Deep Learning (LSTM), NLP, Reinforcement Learning |
| **05** | [**Algorithmic Trading**](./05_algorithmic_trading) | Strategy | Backtesting, Market Microstructure, Risk Management, Stat Arb |
| **06** | [**Quant Development**](./06_quantitative_development) | Production | C++ Low Latency, System Design, HFT Architecture, Performance |
| **07** | [**Interview Prep**](./07_interview_preparation) | Cracking It | Coding Puzzles, Quant Math, Brain Teasers, Company Guides |
| **08** | [**Research & Resources**](./08_research_and_resources) | Deep Dives | Seminal Papers, Datasets, External Tools |

---

## 💎 Premium Content Highlights

We have curated specialized resources that target the specific requirements of HFT and Prop Trading interviews.

### ⚡ Low Latency & Systems
*   **C++ Mastery:** [Order Matching Engine](./06_quantitative_development/cpp_low_latency/examples/order_matching_engine.cpp), [Lock-Free Queue](./06_quantitative_development/cpp_low_latency/examples/lock_free_spsc_queue.cpp), & [Memory Pool](./06_quantitative_development/cpp_low_latency/examples/memory_pool.cpp).
*   **Optimization:** [Microbenchmark Utils](./06_quantitative_development/cpp_low_latency/examples/microbenchmark_utils.hpp) (CPU Cycle Counting).
*   **Concurrency:** [Multithreaded Monte Carlo](./06_quantitative_development/cpp_low_latency/examples/multithreaded_monte_carlo.cpp).
*   **Template Metaprogramming:** [Compile-Time Greeks](./06_quantitative_development/cpp_low_latency/examples/compile_time_greeks.cpp).
*   **Architecture:** [HFT Infrastructure](./06_quantitative_development/system_design/architecture_notes/hft_architecture.md).

### 🧠 Interview Mastery
*   **The Roadmap:** [8-Week Study Plan](./07_interview_preparation/study_roadmap.md).
*   **Quant Strategies:** [Avellaneda-Stoikov MM](./05_algorithmic_trading/strategies/market_microstructure/avellaneda_stoikov_mm.py), [Pairs Trading](./05_algorithmic_trading/strategies/systematic_strategies/pairs_trading_stat_arb.ipynb), & [Execution Algos (TWAP/VWAP)](./05_algorithmic_trading/strategies/execution/execution_algos.py).
*   **Visual Intuition:** [Options Greeks Dashboard](./03_financial_engineering/derivatives_pricing/greeks_visualization.ipynb).
*   **AI/ML:** [LSTM Time Series Forecasting](./04_machine_learning_and_ai/deep_learning/lstm_price_prediction.ipynb).
*   **Backtesting:** [Performance Metrics Library](./05_algorithmic_trading/backtesting_frameworks/performance_metrics.py).
*   **Jane Street Guide:** [Probability & Betting](./07_interview_preparation/company_insights/jane_street_guide.md).

---

##  Getting Started

### Prerequisites
Ensure you have `conda` installed.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/shreejitverma/The-Quant-Prep.git
    cd The-Quant-Prep
    ```

2.  **Set Up Environment**
    ```bash
    conda env create -f environment.yml
    conda activate quant_prep_env
    ```

3.  **Run a Backtest**
    Navigate to `05_algorithmic_trading` and try running a sample strategy to verify your setup.

---

##  Contributing

This is a community-driven project. We welcome contributions!
Please read our [Contributing Guidelines](./CONTRIBUTING.md) before submitting a Pull Request.

*   **Bug Reports:** Open an issue if you find a mistake.
*   **New Content:** Have a unique trading strategy or a better explanation of Ito's Lemma? Submit it!

---

**Maintained by:** [Shreejit Verma](https://github.com/shreejitverma)
