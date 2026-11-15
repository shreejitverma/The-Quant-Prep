---
type: concept
track: [quant-research, quant-dev]
tier: core
status: solid
prereqs: [point-in-time-data-and-survivorship]
est_hours: 5
sources: [Lopez de Prado - Advances in Financial Machine Learning (2018) ch 7 11 12, Chan - Algorithmic Trading Winning Strategies and Their Rationale (2013) ch 1, Isichenko - Quantitative Portfolio Management (2021), Bailey Borwein Lopez de Prado and Zhu (2014) - Pseudo-Mathematics and Financial Charlatanism - Notices of the AMS 61(5) 458-471, D'Avolio (2002) - The Market for Borrowing Stock - Journal of Financial Economics 66(2-3) 271-306]
---

# Backtesting Methodology and Pitfalls

## TL;DR

- A backtest is a simulation of what you could have known, decided and executed at each timestamp; every number must be stamped with when it became available, not the period it describes.
- Positions decided with information up to $t$ earn returns from $t$ to $t+1$ at a realistic fill; in vectorised code that is `position.shift(1) * return`, and forgetting the shift turns pure noise into a Sharpe of about 21.
- Costs are part of the strategy: net Sharpe $= (\mu - \text{turnover}\times\text{cost}\times252)/\sigma$, and a 1.5 gross Sharpe with 30% daily turnover falls to 1.2 at 4 bp.
- Survivorship, look-ahead, restated fundamentals, unrealistic fills, ignoring borrow and capacity, and repeated tuning on the same history are the classic failures.
- Evaluate walk-forward or with purged and embargoed cross-validation; purge training labels that overlap the test window and embargo a buffer after it.
- A backtest is a filter for bad ideas, not proof of good ones: its Sharpe must be deflated by the search that produced it.

## Learning objectives

- Design an event-driven backtest with realistic fills, costs and latency.
- List and avoid the classic pitfalls: look-ahead, survivorship, overfitting, ignoring costs.
- Use walk-forward evaluation.

## Core concepts

### Vectorised versus event-driven

A **vectorised** backtest computes signals, positions and returns as arrays: fast, ideal for research on daily or slower cross-sectional signals, but it makes timing implicit and hides path dependence (stops, limit orders, partial fills, capital constraints).
An **event-driven** backtest replays a time-ordered stream of events (market data, signals, orders, fills) through the same components used in production: data handler, strategy, portfolio and risk, execution simulator.
It is slower but enforces causality by construction, supports order-level logic and can share code with the live system, which removes a whole class of research-to-production discrepancies.
Rule of thumb: research the alpha vectorised, then confirm the final strategy event-driven with the real execution logic before capital.

The repo's [simple_event_driven.py](code/simple_event_driven.py) shows the event loop skeleton (MarketEvent to SignalEvent to OrderEvent to FillEvent).
Its execution handler fills each order at the next bar's price plus slippage and commission, never on the bar that generated the signal; that is the minimum defence against look-ahead, and a real simulator replaces it with the latency, queue and fill model below.

### Timing and the information set

For every input, store the time it became knowable (the "as-of" or knowledge timestamp), not only the period it describes.
Earnings for the quarter ending 31 March are not known on 31 March; index membership changes are announced before they take effect; vendor data is often backfilled or restated ([Point-in-Time Data and Survivorship](02-Point-in-Time-Data-and-Survivorship.md)).
The decision at time $t$ may use only $\mathcal{F}_t$, and the order it produces reaches the market at $t + \text{latency}$.
Common convention for daily research: signal from the close of day $t$, trade at the next open or a VWAP over day $t+1$, earn returns from the fill price onward.
Trading at the same close that generated the signal is only defensible if you can compute the signal and participate in the closing auction, and then you must use auction volumes and imbalance, not the last print.

### Fill and cost model

Net return per period is gross return minus costs:

$$
r^{\text{net}}_t = \sum_i w_{i,t-1} r_{i,t} - \sum_i |w_{i,t} - w_{i,t-1}|\,c_{i,t} - \text{financing and borrow}_t .
$$

The per-unit cost $c_{i,t}$ has three parts: half-spread (crossing the book), market impact (grows with participation, roughly as $\sigma\sqrt{Q/V}$), and fees or rebates.
Fill-model realism by order type:

- Market orders: fill at the touch plus impact; never at mid, never at the close print you used for the signal.
- Limit orders: you fill only when the market trades through your price or you reach the front of the queue, and fills are adversely selected (you get filled when the price is about to move against you); assuming fills whenever the price touches your level is a large, systematic bias.
- Shorts: need locate and borrow cost, and loans can be recalled.
  D'Avolio (2002) finds that 91% of the stocks lent out in his sample cost less than 1% a year (value-weighted mean fee 17 bp), while the 9% "specials" averaged 4.3% a year, so a short book concentrated in hard-to-borrow names pays far more than general-collateral rates.

### Walk-forward evaluation

Walk-forward fits on a window, trades the next block out of sample, then rolls:

- **Rolling window:** fixed-length training window, adapts to regime change, higher variance.
- **Expanding window:** all history to date, more stable, slower to adapt.

Every hyperparameter choice (window length, refit frequency, regularisation) must itself be chosen inside the training window, or selected once and logged as a trial.
Only the concatenated out-of-sample blocks form the performance record.
Walk-forward tests a single historical path, so its Sharpe is noisy and easy to overfit by repeating it; combinatorial purged cross-validation generates many paths from the same data (see [Overfitting and Deflated Sharpe](08-Overfitting-and-Deflated-Sharpe.md)).

### Purging and embargo

When labels span time (for example a 10-day forward return), a training sample near the test block shares return days with test samples, which leaks information.
Lopez de Prado's remedy in *Advances in Financial Machine Learning* chapter 7 ("Cross-Validation in Finance"):

- **Purge:** drop training samples whose label interval overlaps any test label interval, on both sides of the test block.
- **Embargo:** also drop a buffer of training samples immediately after the test block (this note uses 1% of the sample as an example), because features such as moving averages carry test-period information forward.

Details and code are in [Time-Series Cross-Validation, Purging and Embargo](../10-Machine-Learning-for-Finance/02-Time-Series-Cross-Validation-Purging-Embargo.md).

### A pre-flight checklist

Before believing a backtest, confirm each item explicitly.

1. Universe is point-in-time and includes dead names with their delisting returns.
2. Every input is joined as of its knowledge time; corporate actions are applied correctly.
3. Signal at $t$, trade at $t+$latency, realistic fill price.
4. Costs, borrow, financing and position or participation limits are applied.
5. The number of variants tried is logged, and the reported Sharpe is deflated.
6. Performance is stable across subperiods, sectors and parameter neighbourhoods, not driven by a handful of days or names.
7. A delay test (one extra bar) and a cost stress test (costs doubled) do not destroy the result.

## Worked examples

### 1. Cost drag on a high-turnover strategy

Gross annual return 15%, volatility 10% (gross Sharpe 1.5), daily turnover 30% of capital, one-way cost 4 bp.

- Annual cost: $0.30 \times 252 \times 0.0004 = 3.02\%$.
- Net Sharpe: $(15 - 3.02)/10 = 1.20$.
- Cost sensitivity: at 2 bp the net Sharpe is 1.35, at 6 bp 1.05, at 8 bp 0.90.

A 4 bp error in the cost model moves the Sharpe by 0.3; report net results under a range of costs and state the assumed participation rate.
Simulating 4,000 years of daily gross returns and charging $0.30\times4$ bp each day gives the same net Sharpe within sampling error.

### 2. The missing shift

Pure noise daily returns, "strategy" long when today's return is positive.

```python
import numpy as np, pandas as pd
rng = np.random.default_rng(2)
ret = pd.Series(rng.normal(0, 0.01, 2520))           # pure noise daily returns
pos = np.sign(ret)                                    # "signal" computed from today's close
sharpe = lambda x: x.mean() / x.std() * np.sqrt(252)
print(sharpe(pos * ret))             # look-ahead: about 21
print(sharpe(pos.shift(1) * ret))    # correct: noise, 0.25 in this draw
```

The look-ahead version earns $|r_t|$ every day.
For Gaussian returns $E|r|/\text{sd}(|r|) = \sqrt{2/\pi}/\sqrt{1-2/\pi} = 1.32$, so its Sharpe is $1.32\sqrt{252} = 21.0$.
The script checks 21.0 by quadrature and by a 10-million-day simulation, and runs the snippet above exactly as printed.
Real look-ahead bugs are subtler (a full-sample z-score, a same-day fundamental join) and give plausible-looking Sharpes rather than 21, which is why they survive review.

### 3. Survivorship bias in an equal-weight backtest

Each year 5% of the universe delists after a final-year return of $-60\%$; surviving names return 10%.

- True equal-weight return: $0.95 \times 10\% + 0.05 \times (-60\%) = 6.5\%$.
- A survivors-only database reports 10%, a bias of $0.05 \times (10\% + 60\%) = 3.5\%$ per year.

For a strategy that buys recent losers (reversal, deep value), delisting names are concentrated in the long leg and the bias is larger than the universe-wide figure.

### 4. How much data purging and embargo cost

Daily data, $T = 2500$ samples, 5-fold purged cross-validation, labels are 10-day forward returns (sample $t$ uses the returns of days $t+1$ to $t+10$), embargo 1% of $T$.

- Each test fold has 500 samples; the embargo is $0.01 \times 2500 = 25$ samples.
- A test fold starting at sample $s$ has labels covering return days $s+1$ to $s+509$.
  Training samples $s-9$ to $s-1$ share return days with it, and so do samples $s+500$ to $s+508$ after it, so purging drops 9 on each side.
  Sample $s-10$ uses days $s-9$ to $s$ and does not overlap; counting it would be an off-by-one error.
- Embargo 25 more samples after the purged ones: $9 + 9 + 25 = 43$ samples lost.
- Training set for an interior fold: $2500 - 500 - 43 = 1957$ samples instead of 2000; the first fold keeps 1966 and the last 1991, since each loses only one side.

The script enumerates every sample's return days and tests overlap directly, so the count does not depend on this hand reasoning.

The cost in data is small; skipping it lets the model memorise returns it will be tested on.

## Pitfalls

- Look-ahead: same-bar execution, full-sample normalisation, restated fundamentals, future index membership, timezone mismatches between data sources.
- Survivorship: universes built from today's constituents, missing delisting returns.
- Fill optimism: filling at mid or the signal-generating close, assuming limit orders fill on touch, ignoring queue position and adverse selection.
- Ignoring shorting constraints (locates, borrow fees, recalls, uptick rules) and financing costs.
- Capacity blindness: trading 20% of a microcap's daily volume at the quoted spread.
- Repeatedly re-running walk-forward with tweaks until it looks good; the out-of-sample period has become in-sample.
- Reporting a single aggregate Sharpe with no subperiod breakdown, no turnover and no cost sensitivity.
- Mismatched compounding: summing simple returns across time or averaging log returns across names.

## Interview questions

> [!question]- alpha-bt-shift-rule | In a vectorised backtest, how should positions and returns be aligned?
> Position decided with information up to $t$ multiplies the return from $t$ to $t+1$: `position.shift(1) * returns`.
> Without the shift the strategy is credited with the return that produced its own signal, which on pure noise gives a Sharpe near 21.

> [!question]- alpha-bt-noise-lookahead-sharpe | Why does a same-bar sign strategy on iid Gaussian noise show a Sharpe of about 21?
> It earns $|r_t|$ every day, and $E|r|/\text{sd}|r| = \sqrt{2/\pi}/\sqrt{1-2/\pi} \approx 1.32$ per day.
> Annualised: $1.32\sqrt{252} \approx 21$.

> [!question]- alpha-bt-cost-drag | Gross Sharpe 1.5 on 10% vol, 30% daily turnover, 4 bp one-way cost. Net Sharpe?
> About 1.2.
> Annual cost $0.3\times252\times4$ bp $= 3.02\%$, so net Sharpe $= (15-3.02)/10$.

> [!question]- alpha-bt-event-vs-vector | When is an event-driven backtest worth its cost over a vectorised one?
> When execution details or path dependence matter: intraday timing, limit orders, partial fills, stops, capital or risk constraints.
> It enforces causality by construction and can share code with production; vectorised is fine for researching slow cross-sectional signals.

> [!question]- alpha-bt-limit-fill-bias | Why is "a limit order fills when the price touches it" a biased assumption?
> It ignores queue position and adverse selection.
> In reality you fill only when the market trades through your level or your queue is reached, and you fill most often when price is about to move against you.

> [!question]- alpha-bt-survivorship | 5% of names delist per year after a $-60\%$ final year and survivors return 10%. How biased is a survivors-only equal-weight backtest?
> About 3.5% per year.
> True return $0.95\times10\% + 0.05\times(-60\%) = 6.5\%$ versus 10% reported.

> [!question]- alpha-bt-purge-embargo | What do purging and embargo do in time-series cross-validation?
> Purging removes training samples whose label interval overlaps a test label interval; embargo removes an extra buffer of training samples right after the test block.
> Both stop overlapping labels and serially dependent features from leaking test information into training.

> [!question]- alpha-bt-walk-forward-types | Rolling or expanding window in walk-forward: what is the trade-off?
> Rolling adapts to regime change but has higher estimation variance; expanding is more stable but slow to adapt.
> Choose the window inside the training data or log it as a trial, because picking it on the out-of-sample record is overfitting.

> [!question]- alpha-bt-knowledge-time | Why must fundamentals be joined on knowledge time rather than fiscal period end?
> Because the numbers were not public on the period end date, and later restatements were never available at all.
> Joining on period end (or using restated data) lets the backtest trade on information weeks or years before it existed.

> [!question]- alpha-bt-delay-and-cost-stress | Name two quick robustness tests you run on any promising backtest.
> A one-bar delay test and a doubled-cost test.
> If one extra bar of latency or twice the assumed costs wipes out the result, the edge is probably a timing artefact or too thin to survive execution.

> [!question]- alpha-bt-walk-forward-overfit | Your walk-forward result looks great after 30 iterations of tweaks. What is wrong?
> The out-of-sample periods have been used for selection 30 times and are now in-sample.
> Count those iterations as trials, deflate the Sharpe accordingly, and validate on a sealed period or with many-path methods like CPCV.

> [!question]- alpha-bt-short-constraints | Which frictions on the short side do naive backtests ignore?
> Locate availability, borrow fees, recall risk and short-sale rules.
> Specials are a minority of loaned stocks but cost far more (in D'Avolio's 2002 sample, a 4.3% mean fee against 17 bp for general collateral), so ignoring borrow overstates the net return of any short book concentrated in such names.

> [!question]- alpha-bt-purge-count | 2,500 daily samples, 5 folds, 10-day forward-return labels, embargo 1%. How many training samples does an interior fold keep?
> 1957.
> Purging drops the 9 samples on each side whose label windows share return days with the test fold, and the embargo drops 25 more after it: $2500 - 500 - 43$.

> [!question]- alpha-bt-cost-sensitivity | A strategy has 15% gross return, 10% volatility and 30% daily turnover. What is its net Sharpe at 8 bp one-way cost?
> About 0.90.
> Annual cost is $0.30\times252\times8$ bp $= 6.05\%$, so the net Sharpe is $(15 - 6.05)/10$; each basis point of cost removes 0.076 of Sharpe.

> [!question]- alpha-bt-survivorship-direction | Why does survivorship bias hurt a reversal or deep-value backtest more than the market average?
> Those strategies buy recent losers, and in the example the delisting names are exactly the ones that fell 60% in their final year.
> A survivors-only database drops those long-leg names with the worst final returns, so the bias in the long leg exceeds the universe-wide figure.

## In this repo and The-Distinguished-Engineer

- Code: [`code/alpha_07_backtesting.py`](code/alpha_07_backtesting.py) prints and asserts every number on this page: cost drag and survivorship in exact fractions and the cost drag again by simulating daily returns, the look-ahead Sharpe by quadrature and a large simulation (plus the snippet run as printed), and purging and embargo by enumerating every sample's return days.
- Code: [simple_event_driven.py](code/simple_event_driven.py) and [performance_metrics.py](code/performance_metrics.py).

## Further reading

- Marcos Lopez de Prado, *Advances in Financial Machine Learning* (2018), chapters 7 ("Cross-Validation in Finance"), 11 ("The Dangers of Backtesting") and 12 ("Backtesting through Cross-Validation").
- Ernest Chan, *Algorithmic Trading: Winning Strategies and Their Rationale* (2013).
- Michael Isichenko, *Quantitative Portfolio Management* (2021).
- David H. Bailey, Jonathan Borwein, Marcos Lopez de Prado and Qiji Jim Zhu, "Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance", *Notices of the AMS* 61(5) (2014), 458-471.
- Gene D'Avolio, "The Market for Borrowing Stock", *Journal of Financial Economics* 66(2-3) (2002), 271-306.
