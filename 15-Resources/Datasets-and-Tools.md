---
type: reference
track: [quant-trader, quant-research, quant-dev]
tier: core
status: draft
sources: []
---

# Datasets and Tools

Data and software for practising research and building projects you can discuss in interviews.
Check each provider's current licence and pricing before relying on it; free tiers change often.

## Practice datasets

| Dataset | What it is good for |
| :--- | :--- |
| Kenneth French Data Library (Dartmouth) | Factor returns and sorted portfolios for factor-model and regression practice. |
| FRED (Federal Reserve Bank of St. Louis) | Rates, inflation and macro series for time-series and macro-awareness work. |
| LOBSTER (lobsterdata.com) | Reconstructed Nasdaq limit order book data for microstructure research (academic licence). |
| Kaggle: Optiver Realized Volatility Prediction | Order book and trade snapshots; realised volatility forecasting. |
| Kaggle: Optiver Trading at the Close | Closing auction order book data; short-horizon prediction. |
| Kaggle: Jane Street Market Prediction and Jane Street Real-Time Market Data Forecasting | Anonymised features and responses; honest validation practice on noisy targets. |
| Exchange public data (for example Binance public market data) | Free high-frequency crypto trades and books for building book-reconstruction and signal code. |
| Nasdaq TotalView-ITCH sample files | Real binary feed data for writing a parser; see the specs in [protocol-specs](../12-Quant-Development/protocol-specs/). |

Institutional sources you will meet on the job: CRSP and Compustat (via WRDS), Bloomberg, Refinitiv, TAQ, OptionMetrics, and direct exchange feeds.

## Python research stack

- numpy, pandas or polars, scipy, statsmodels for data and statistics.
- scikit-learn and LightGBM or XGBoost for classical ML; PyTorch for deep learning.
- QuantLib (with its Python bindings) for rates and derivatives pricing.
- Parquet with DuckDB or Arrow for local tick-data work; kdb+/q and ArcticDB are common in industry.
- `uv` or conda for reproducible environments; this repo's `environment.yml` covers the notebooks.

## C++ and systems

- A modern compiler (GCC or Clang) with C++20, CMake, and the sanitizers (ASan, UBSan, TSan).
- Google Benchmark for microbenchmarks and `perf` or Instruments for profiling.
- The [SDE Link Map](../00-Start-Here/SDE-Link-Map.md) points to the low-latency systems material.
