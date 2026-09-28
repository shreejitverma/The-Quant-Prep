# The Quant Prep

A complete, self-tracking preparation system for senior **quant trader**, **quant researcher** and **quant developer** interviews at proprietary trading firms, market makers, HFT firms and multi-manager hedge funds: Jane Street, Optiver, Citadel and Citadel Securities, Two Sigma, DRW, Squarepoint, Radix, Akuna, SIG, Millennium, Balyasny, HRT, Jump, IMC, Tower, Five Rings, D. E. Shaw and AQR.

It is three things over one set of Markdown notes:

- **A syllabus**: 162 topics in 13 subjects, each with learning objectives, prerequisites, tier (core, advanced, senior), study hours, and spaced-repetition question cards.
- **A progress platform**: the `qp` command line and a local web dashboard for readiness by track and by firm, a prerequisite-ordered weekly plan, daily card review, and timed drills (arithmetic sprint, 80-in-8 numerical test, market-making game).
- **An Obsidian vault**: open the folder in Obsidian to read; question cards are collapsible callouts.

General software engineering (DSA, C++, system design, low-latency systems) lives in [SDE-Interview-Prep](https://github.com/shreejitverma/SDE-Interview-Prep) and is linked, not copied: see the [SDE Link Map](00-Start-Here/SDE-Link-Map.md).

## Quick start

Python 3.10+ and nothing else:

```sh
git clone https://github.com/shreejitverma/The-Quant-Prep.git && cd The-Quant-Prep
./qp profile --tracks quant-trader --hours 12   # your target role(s) and weekly hours
./qp                                            # readiness, today's reviews, what to study next
./qp serve --open                               # dashboard at http://127.0.0.1:8765/
```

Then read [Start Here](00-Start-Here/README.md): [Tracks](00-Start-Here/Tracks.md), the [Roadmap](00-Start-Here/Roadmap.md) and [Using the Platform](00-Start-Here/Using-the-Platform.md).
Progress is stored outside the repo (`~/.local/share/quant-prep/`, or `$QP_HOME`).

## Syllabus

| # | Subject | Focus |
| :--- | :--- | :--- |
| 01 | [Probability](01-Probability/README.md) | Combinatorics to martingales; the most-tested subject in trader and researcher interviews. |
| 02 | [Statistics and Econometrics](02-Statistics-and-Econometrics/README.md) | Estimation, testing, regression, time series, volatility models, Kalman filters. |
| 03 | [Linear Algebra and Optimization](03-Linear-Algebra-and-Optimization/README.md) | Spectral methods, PCA, covariance, convex optimisation, numerics. |
| 04 | [Stochastic Calculus](04-Stochastic-Calculus/README.md) | Brownian motion, Ito, SDEs, risk-neutral pricing, Black-Scholes. |
| 05 | [Derivatives and Volatility](05-Derivatives-and-Volatility/README.md) | Parity, Greeks, hedging P&L, smiles, surfaces, Monte Carlo, vol trading. |
| 06 | [Fixed Income and Asset Classes](06-Fixed-Income-and-Asset-Classes/README.md) | Curves, duration, swaps, short-rate models, credit, FX, ETFs, commodities, crypto. |
| 07 | [Market Microstructure](07-Market-Microstructure/README.md) | Order books, spread models, impact, execution, Reg NMS, microprice. |
| 08 | [Market Making](08-Market-Making/README.md) | Fair value, inventory models, quoting, hedging, options MM, games, systems. |
| 09 | [Alpha Research and Portfolio](09-Alpha-Research-and-Portfolio/README.md) | Research process, signals, factors, backtesting, overfitting, portfolio construction. |
| 10 | [Machine Learning for Finance](10-Machine-Learning-for-Finance/README.md) | Leakage-safe validation, ensembles, deep and reinforcement learning, NLP. |
| 11 | [Risk and Trading](11-Risk-and-Trading/README.md) | Kelly, betting, VaR and ES, limits, P&L attribution, trading judgement. |
| 12 | [Quant Development](12-Quant-Development/README.md) | Order books, feed handlers, backtesters, pricing libraries, risk checks; bridges to SDE-Interview-Prep. |
| 13 | [Interview Playbook](13-Interview-Playbook/README.md) | Formats, mental math, brainteasers, estimation, trading games, behavioural, senior expectations. |
| 14 | [Firms](14-Firms/README.md) | One guide per firm: roles, process, what they test, a focused plan. |
| 15 | [Resources](15-Resources/README.md) | Books, papers, datasets and tools. |

Each section README carries a generated table of its topics with status and card counts.
Notes marked `seed` are the writing backlog: objectives and references exist, full content does not yet.

## Runnable code

| Code | Where |
| :--- | :--- |
| Price-time order book and matching engine, lock-free SPSC queue, object pool, multicast receiver, compile-time N(x) table, multithreaded Monte Carlo (C++20) | [12-Quant-Development/code/cpp](12-Quant-Development/code/cpp/) |
| ITCH parser, Python benchmarking | [12-Quant-Development/code/python](12-Quant-Development/code/python/) |
| Avellaneda-Stoikov market-making simulator | [08-Market-Making/code](08-Market-Making/code/) |
| Event-driven backtester (next-bar fills), performance metrics, pairs trading, Black-Litterman | [09-Alpha-Research-and-Portfolio/code](09-Alpha-Research-and-Portfolio/code/) |
| Execution algorithms, Euler-Maruyama SDE solver, Greeks visualisation, LSTM baseline | sections [07](07-Market-Microstructure/code/), [04](04-Stochastic-Calculus/code/), [05](05-Derivatives-and-Volatility/code/), [10](10-Machine-Learning-for-Finance/code/) |

Build a C++ example with `g++ -std=c++20 -O2 -pthread <file>.cpp`; run Python examples with the packages in `environment.yml`.

## Repository layout

```
00-Start-Here/     tracks, roadmap, platform guide, note conventions, SDE link map
01-..15-           the syllabus (Markdown notes, code/ folders beside the notes that use them)
tools/qp/          the qp CLI, local server and dashboard (standard library only)
tools/tests/       platform tests
_archive/          the pre-2026 notebook collection and superseded drafts, outside the curriculum
```

## Contributing

Read [Note Conventions](00-Start-Here/Note-Conventions.md) and [CONTRIBUTING](CONTRIBUTING.md).
Before a pull request: `./qp check`, `./qp index`, `python3 -m unittest discover -s tools/tests -t .`, and `ruff check .`.

Maintained by [Shreejit Verma](https://github.com/shreejitverma). MIT licence.
