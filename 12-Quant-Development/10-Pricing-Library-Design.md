---
type: concept
track: [quant-dev]
tier: advanced
status: seed
prereqs: [cpp-for-trading-systems, monte-carlo-pricing-and-variance-reduction]
est_hours: 4
sources: []
---

# Pricing Library Design

> [!info] Seed note
> Not written yet. The objectives below define what "done" looks like; use the references to study it now.

## Learning objectives

- Separate instruments, market data, models and pricers cleanly.
- Explain calibration, caching and algorithmic differentiation for Greeks.

## Further reading

- Mark Joshi, *C++ Design Patterns and Derivatives Pricing*

## In this repo and SDE-Interview-Prep

- Production pricing library architecture: [Pricing Library Architecture](../18-Pricing-and-Risk-Systems/05-Pricing-Library-Architecture.md).
- Distributed grid compute and cloud pricing: [Pricing at Scale](../18-Pricing-and-Risk-Systems/06-Pricing-at-Scale.md).
- Code: [compile_time_greeks.cpp](code/cpp/compile_time_greeks.cpp).
