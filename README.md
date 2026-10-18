# The Quant Prep

A complete, self-tracking preparation system for senior **quant trader**, **quant researcher** and **quant developer** interviews at proprietary trading firms, market makers, HFT firms and multi-manager hedge funds (Jane Street, Optiver, Citadel and Citadel Securities, Two Sigma, DRW, Squarepoint, Radix, Akuna, SIG, Millennium, Balyasny, HRT, Jump, IMC, Tower, Five Rings, D. E. Shaw and AQR), and for **quant risk and strats** roles at banks: desk quants, market risk and FRTB, counterparty risk and XVA, model validation and risk technology.

It is three things over one set of Markdown notes:

- **A syllabus**: more than 200 topics in 15 subjects, each with learning objectives, prerequisites, tier (core, advanced, senior), study hours, and spaced-repetition question cards; `./qp syllabus` and each section README give live counts.
- **A progress platform**: the `qp` command line and a local web dashboard for readiness by track and by firm, a prerequisite-ordered weekly plan, daily card review, and timed drills (arithmetic sprint, 80-in-8 numerical test, market-making game).
- **An Obsidian vault**: open the folder in Obsidian to read; question cards are collapsible callouts.

[Trading and Investing](16-Trading-and-Investing/README.md) adds the Markets Mastery OS curriculum, persona-based study planning, mastery scoring, and an interactive trading lab to the `qp` platform.

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
| 06 | [Fixed Income and Asset Classes](06-Fixed-Income-and-Asset-Classes/README.md) | Curves, duration, day counts, money markets and repo, swaps, multi-curve and curve risk, Treasury futures, short-rate models, credit, CDS indices and tranches, inflation, mortgages and securitized products, P&L attribution and relative value, FX, ETFs, commodities, crypto. |
| 07 | [Market Microstructure](07-Market-Microstructure/README.md) | Order books, spread models, impact, execution, Reg NMS, microprice. |
| 08 | [Market Making](08-Market-Making/README.md) | Fair value, inventory models, quoting, hedging, options MM, games, systems. |
| 09 | [Alpha Research and Portfolio](09-Alpha-Research-and-Portfolio/README.md) | Research process, signals, factors, backtesting, overfitting, portfolio construction. |
| 10 | [Machine Learning for Finance](10-Machine-Learning-for-Finance/README.md) | Leakage-safe validation, ensembles, deep and reinforcement learning, NLP. |
| 11 | [Risk and Trading](11-Risk-and-Trading/README.md) | Kelly, betting, VaR and ES, stress testing, drawdowns and limits, P&L attribution and Greek risk, risk factors, scenario generation, sensitivities and revaluation, trading judgement. |
| 12 | [Quant Development](12-Quant-Development/README.md) | Order books, feed handlers, backtesters, pricing libraries, risk checks; bridges to SDE-Interview-Prep. |
| 13 | [Interview Playbook](13-Interview-Playbook/README.md) | Formats, mental math, brainteasers, estimation, trading games, behavioural, senior expectations. |
| 17 | [Regulatory Capital, Basel, and FRTB](17-Regulatory-Capital-Basel-and-FRTB/README.md) | Capital and RWA, credit SA and IRB, SA-CCR, CVA capital, FRTB standardised and internal models, liquidity, IRRBB, stress testing, BCBS 239. |
| 18 | [Pricing and Risk Systems](18-Pricing-and-Risk-Systems/README.md) | Front-to-back architecture, trade and market data, curve and pricing services, risk, P&L, FRTB and XVA engines, EOD batch, governance. |
| 14 | [Firms](14-Firms/README.md) | One guide per firm: roles, process, what they test, a focused plan. |
| 15 | [Resources](15-Resources/README.md) | Books, papers, datasets and tools. |

Each section README carries a generated table of its topics with status and card counts.
Notes marked `seed` are the writing backlog: objectives and references exist, full content does not yet.

## Runnable code

| Code | Where |
| :--- | :--- |
| Price-time order book and matching engine, lock-free SPSC queue, object pool, multicast receiver, compile-time N(x) table, multithreaded Monte Carlo (C++20) | [12-Quant-Development/code/cpp](12-Quant-Development/code/cpp/) |
| ITCH parser, Python benchmarking | [12-Quant-Development/code/python](12-Quant-Development/code/python/) |
| Linear maps, eigendecomposition and SVD, covariance PSD repair and PCA, numerical linear algebra, Taylor expansions, KKT and QP portfolio solvers, root finding and implied volatility, problem-set checks | [03-Linear-Algebra-and-Optimization/code](03-Linear-Algebra-and-Optimization/code/) |
| Day counts, schedules, bond pricing and risk, overnight-rate compounding, curve bootstrapping, dual-curve swap pricing, Jacobian par risk, Treasury futures basis, CDS hazard bootstrap, TIPS indexation, mortgage prepayment, Gaussian copula tranche loss, covered interest parity and the cross-currency basis, ETF fair value and index arbitrage, futures curves and roll yield, crypto perpetual funding and basis | [06-Fixed-Income-and-Asset-Classes/code](06-Fixed-Income-and-Asset-Classes/code/) |
| Call-auction uncross and fee economics, Roll and Glosten-Milgrom spreads, Kyle equilibrium, square-root and propagator impact, Almgren-Chriss optimal execution, TWAP, VWAP, POV and implementation shortfall, Reg NMS routing, latency-arbitrage races | [07-Market-Microstructure/code](07-Market-Microstructure/code/) |
| Avellaneda-Stoikov market-making simulator | [08-Market-Making/code](08-Market-Making/code/) |
| Event-driven backtester (next-bar fills), performance metrics, point-in-time and survivorship biases, cross-sectional factor models, momentum and carry, pairs and residual stat arb, covariance shrinkage, Black-Litterman, risk parity and HRP, transaction costs and turnover, alternative-data evaluation, end-to-end research case studies | [09-Alpha-Research-and-Portfolio/code](09-Alpha-Research-and-Portfolio/code/) |
| Finite-difference Greeks bump engine, Taylor revaluation proxies, Cholesky Monte Carlo and filtered historical scenarios, rates stress scenarios, full versus proxy VaR and ES | [11-Risk-and-Trading/code](11-Risk-and-Trading/code/) |
| Interview coding problems tested against brute force (streaming statistics, order book, FIX parser), a mini research take-home on synthetic data, offer arithmetic, track-record statistics and calibration | [13-Interview-Playbook/code](13-Interview-Playbook/code/) |
| Euler-Maruyama SDE solver, Girsanov and numeraire changes (Margrabe, forward and annuity measures, quanto), Feynman-Kac pricing PDEs (affine bonds, barriers, perpetual American put, one-touch, range accrual), Merton, Kou and variance gamma jump models | [04-Stochastic-Calculus/code](04-Stochastic-Calculus/code/) |
| SVI, SSVI and Dupire local vol, Heston and SABR with calibration, finite-difference and Fourier (Carr-Madan, COS) pricers, digitals, barriers, Asians, lookbacks, autocallables and cliquets, dispersion and implied correlation, Greeks visualisation | [05-Derivatives-and-Volatility/code](05-Derivatives-and-Volatility/code/) |
| LSTM baseline | [10-Machine-Learning-for-Finance/code](10-Machine-Learning-for-Finance/code/) |
| Basel credit SA and IRB, SA-CCR, FRTB sensitivities-based method, DRC and RRAO, FRTB IMA (ES, NMRF, backtesting, PLA), liquidity and IRRBB | [17-Regulatory-Capital-Basel-and-FRTB/code](17-Regulatory-Capital-Basel-and-FRTB/code/) |
| Reference pricing and risk engine | [18-Pricing-and-Risk-Systems/code](18-Pricing-and-Risk-Systems/code/) |

Every example must run cleanly in CI; examples that assert their numbers also fail CI when a quoted number drifts.
Run them all with `python tools/run_examples.py` (needs numpy, pandas and matplotlib; `--list` shows them), or one at a time with `python <file>.py`.
Build a C++ example with `g++ -std=c++20 -O2 -pthread <file>.cpp`.

## Repository layout

```
00-Start-Here/     tracks, roadmap, platform guide, note conventions, SDE link map
01-..15-           the syllabus (Markdown notes, code/ folders beside the notes that use them)
16-, 17-CFA/       Obsidian libraries outside the syllabus: trading and investing; the CFA Level II platform
17-, 18-           regulatory capital (Basel, FRTB) and pricing and risk systems, inside the syllabus
tools/qp/          the qp CLI, local server and dashboard (standard library only)
tools/run_examples.py  runs every Python example (CI does too)
tools/tests/       platform tests
_archive/          the pre-2026 notebook collection and superseded drafts, outside the curriculum
```

## Contributing

Read [Note Conventions](00-Start-Here/Note-Conventions.md) and [CONTRIBUTING](CONTRIBUTING.md).
Before a pull request, run the checks listed in [CONTRIBUTING](CONTRIBUTING.md#workflow), including the secret scan.

Maintained by [Shreejit Verma](https://github.com/shreejitverma). MIT licence.
