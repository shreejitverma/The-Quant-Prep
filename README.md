# The Quant Prep
### The Ultimate Roadmap for Quantitative Developers & Researchers

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![C++](https://img.shields.io/badge/C%2B%2B-17%2F20-blue)](https://isocpp.org/)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

**The Quant Prep** is a comprehensive, open-source curriculum designed to bridge the gap between academic theory and the rigorous demands of top-tier financial firms like **Jane Street, Citadel, Hudson River Trading, Optiver, and Two Sigma**.

Whether you are aiming for a **Quantitative Researcher** role (heavy math/stats/ML) or a **Quantitative Developer** role (low-latency C++/systems), this repository provides the code, theory, and interview preparation you need.

---

## 🗺️ The 8-Stage Learning Pathway

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
*   **C++ Mastery:** [Modern C++ Cheatsheet](./06_quantitative_development/cpp_low_latency/modern_cpp_interview.md) covering Smart Pointers, Move Semantics, and Lock-Free programming.
*   **HFT Architecture:** [Hardware & Network](./06_quantitative_development/system_design/architecture_notes/hft_architecture.md) deep dive into FPGA, Kernel Bypass, and Colocation.
*   **Java Performance:** [GC-Free Coding](./06_quantitative_development/java_low_latency/README.md) for firms like IMC/Optiver.
*   **Distributed Systems:** [Grid Computing](./06_quantitative_development/system_design/distributed_compute.md) for massive risk calculations.

### 🧠 Interview Mastery
*   **The Roadmap:** [8-Week Study Plan](./07_interview_preparation/study_roadmap.md) taking you from zero to offer-ready.
*   **Jane Street Guide:** [Probability & Betting](./07_interview_preparation/company_insights/jane_street_guide.md) strategies specifically for prop trading interviews.
*   **Quant Math:** [Green Book Companion](./01_foundations/mathematics/probability/quant_probability_guide.md) and [Linear Algebra Essentials](./01_foundations/mathematics/linear_algebra/linear_algebra_for_quants.md).
*   **Data Structures:** [Quant-Specific Algorithms](./01_foundations/cs_basics/algorithms/quant_data_structures.md) focusing on Order Books and Ring Buffers.

---

## 🚀 Getting Started

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

## 🤝 Contributing

This is a community-driven project. We welcome contributions!
Please read our [Contributing Guidelines](./CONTRIBUTING.md) before submitting a Pull Request.

*   **Bug Reports:** Open an issue if you find a mistake.
*   **New Content:** Have a unique trading strategy or a better explanation of Ito's Lemma? Submit it!

---

**Maintained by:** [Shreejit Verma](https://github.com/shreejitverma)