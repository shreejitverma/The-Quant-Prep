---
type: concept
track: [quant-research]
tier: core
status: solid
prereqs: [linear-regression-ols, point-in-time-data-and-survivorship]
est_hours: 4
sources: [Grinold and Kahn - Active Portfolio Management 2nd ed (1999), Isichenko - Quantitative Portfolio Management (2021), Qian Hua and Sorensen - Quantitative Equity Portfolio Management (2007), Almgren Thum Hauptmann and Li (2005) - Direct Estimation of Equity Market Impact - Risk 18(7)]
---

# Signals, Features and Alpha Decay

## TL;DR

- The information coefficient (IC) is the cross-sectional correlation between a signal at $t$ and returns after $t$; rank IC (Spearman) is the robust default, and typical daily equity ICs are 0.01 to 0.05.
- A signal-weighted book earns roughly $\text{IC}\times\sigma_{cs}\times(\text{scaling})$ per period, and its Sharpe is $\overline{\text{IC}}/\text{sd}(\text{IC})\times\sqrt{\text{periods per year}}$, so IC stability matters as much as its mean.
- IC decay $\text{IC}(k) = \text{corr}(s_t, r_{t+k})$ sets the natural horizon; the IC against $h$-period cumulative returns peaks at an intermediate $h$.
- Signal autocorrelation $\rho$ sets turnover: a signal-proportional book trades about $\sqrt{2(1-\rho)}$ of its gross per rebalance, which with the alpha per period fixes the break-even cost.
- Neutralise by taking the residual of a cross-sectional regression of the signal on sector, beta and style exposures, so the book earns the idiosyncratic part only.
- Capacity falls fast with turnover: under square-root impact, break-even AUM scales like $\alpha^2/T^3$ for daily alpha $\alpha$ and turnover $T$.

## Learning objectives

- Measure signals with information coefficient, rank IC and IC decay.
- Relate signal horizon, turnover and capacity.
- Neutralise signals against known factors.

## Core concepts

### From raw data to a signal

A feature is any point-in-time variable; a signal is a feature transformed into a cross-sectionally comparable forecast of forward (usually residual) return.
Standard pipeline, applied cross-sectionally at each date $t$ using only information known at $t$ ([Point-in-Time Data and Survivorship](02-Point-in-Time-Data-and-Survivorship.md)):

1. Clean: handle missing values, stale prices, corporate actions.
2. Normalise: rank-transform or z-score, then winsorise (for example at $\pm3$) so a few names do not dominate.
3. Neutralise: remove exposures to known factors (below).
4. Combine: blend several signals with weights estimated out of sample.
5. Map to alpha: Grinold's rule $\alpha_i = \text{IC}\cdot\sigma_i\cdot z_i$, residual volatility times IC times score, turns a unit-free score into an expected return.

### Information coefficient

At date $t$, with signal $s_{i,t}$ and forward return $r_{i,t+1}$ over $N$ names,

$$
\text{IC}_t = \text{corr}_i\big(s_{i,t},\, r_{i,t+1}\big), \qquad \text{RankIC}_t = \text{corr}_i\big(\text{rank}(s_{i,t}),\, \text{rank}(r_{i,t+1})\big).
$$

Report the time series, not one pooled number: mean IC, its standard deviation, the IC information ratio $\overline{\text{IC}}/\text{sd}(\text{IC})$, the fraction of positive days and the $t$-stat $\overline{\text{IC}}/\text{sd}(\text{IC})\times\sqrt{n_{\text{dates}}}$ (with overlap corrected if horizons overlap).
Rank IC is invariant to monotone transforms and robust to outliers; Pearson IC is closer to what a linearly weighted book actually earns.
Measure IC against residual returns (after removing market and factor returns) when the book will be factor-neutral, otherwise you credit the signal with factor bets.

### IC to PnL

Let the book hold $w_i = z_i/\sum_j|z_j|$ (gross exposure 1, dollar neutral when $z$ is demeaned) with $z$ the standardised signal.
Then the one-period return is

$$
R_t = \frac{\sum_i z_i r_i}{\sum_j |z_j|} = \frac{N\,\text{cov}(z,r)}{N\,E|z|} \approx \frac{\text{IC}_t\,\sigma_{cs,t}}{E|z|},
$$

where $\sigma_{cs}$ is the cross-sectional dispersion of returns and $E|z| = \sqrt{2/\pi} \approx 0.80$ for Gaussian scores.
Two consequences an interviewer will probe:

- Expected PnL scales with IC and with cross-sectional dispersion, which is regime dependent (high in crises, low in quiet markets).
- The Sharpe of the book is approximately $\overline{\text{IC}}/\text{sd}(\text{IC}) \times \sqrt{252}$ for daily rebalancing.
  The fundamental-law value $\text{IC}\sqrt{N}$ is an upper bound that assumes uncorrelated residuals and constant IC; common factors and time variation in IC make realised $\text{sd}(\text{IC})$ far larger than $1/\sqrt{N}$ ([Performance Metrics and the Fundamental Law](09-Performance-Metrics-and-Fundamental-Law.md)).

### IC decay and horizon

Define the marginal IC at lag $k$ as $\text{IC}(k) = \text{corr}(s_t, r_{t+k})$, the correlation with the single-period return $k$ periods ahead.
If per-period returns are roughly uncorrelated with equal variance, the IC against the cumulative $h$-period return is

$$
\text{IC}_{[1,h]} = \frac{1}{\sqrt h}\sum_{k=1}^{h}\text{IC}(k).
$$

The numerator stops growing once $\text{IC}(k)$ has decayed while the denominator keeps growing, so $\text{IC}_{[1,h]}$ peaks at an intermediate horizon.
With geometric decay $\text{IC}(k) = \text{IC}(1)\,\delta^{k-1}$, the half-life is $\ln 2/\ln(1/\delta)$ and the total harvestable IC is $\text{IC}(1)/(1-\delta)$.
Signal half-life should match the trading horizon: trading a 3-day half-life signal monthly throws most of it away, trading a 6-month signal daily pays costs for nothing.
Delay tests are the practical form of this: shift the signal by one extra period (trade at $t+1$ instead of $t$) and measure how much IC survives; a signal that dies with one bar of delay is a latency or data-timing artefact until proven otherwise.

### Turnover and autocorrelation

If the signal is standardised each period and its cross-sectional autocorrelation between rebalances is $\rho$, then $z_t - z_{t-1}$ has standard deviation $\sqrt{2(1-\rho)}$.
For Gaussian scores $E|z_t - z_{t-1}|/E|z_t| = \sqrt{2(1-\rho)}$, so a signal-proportional book trades that fraction of its gross per rebalance.
Break-even one-way cost per unit traded is (alpha per period)/(turnover per period); anything above it makes the signal a net loser.
Smoothing the signal (exponential moving average) or trading only partway toward the target raises $\rho$, cutting cost at the price of some IC; the optimal trade-off is part of portfolio construction with costs ([Transaction Costs and Turnover](13-Transaction-Costs-and-Turnover.md)).

### Capacity

Square-root impact (Almgren et al. 2005): trading $Q$ dollars in a name with daily volume $V$ costs a fraction of about $Y\sigma\sqrt{Q/V}$, with $\sigma$ daily volatility and $Y$ of order one.
A book of size $A$ with daily turnover $T$ trades $TA$ per day and earns $\alpha A$, so

$$
\text{net PnL} \approx \alpha A - TA \cdot Y\sigma\sqrt{TA/V}, \qquad A_{\text{break-even}} = \frac{V\,\alpha^2}{Y^2\sigma^2T^3}.
$$

Holding alpha per unit traded fixed ($\alpha = aT$) gives $A \propto a^2/T$: fast signals have small capacity, which is why high-turnover alphas are run in small books and slow factor portfolios can absorb billions.
The profit-maximising size is below break-even; with this cost curve it is $(2/3)^2 = 4/9$ of the break-even AUM.

### Neutralisation

Regress the signal cross-sectionally on the exposures you do not want and keep the residual:

$$
s = X b + e, \qquad s^{\perp} = e = (I - X(X^\top X)^{-1}X^\top)s,
$$

where the columns of $X$ are sector dummies, market beta, size and other style factors ([Cross-Sectional Factor Models](04-Cross-Sectional-Factor-Models.md)).
The residual is orthogonal to every column of $X$, so a book proportional to it has zero net exposure to each sector and zero beta (exactly for the regression weights used; use a risk model and an optimiser for exact risk neutrality).
Sector demeaning is the special case with only sector dummies.
Neutralise before measuring IC, otherwise a "value" signal that is secretly 90% sector bet looks brilliant in a year when that sector rallies.

## Worked examples

### 1. From IC to daily return and break-even cost

Setup: 2,000 names, daily rank IC 0.03, cross-sectional return dispersion 2% per day, book $w = z/\sum|z|$.

- Expected return on gross: $0.03 \times 0.02 / 0.798 = 0.075\%$ per day, about 19% of gross per year before costs.
- If $\text{sd}(\text{IC}) = 0.10$ day to day, the gross Sharpe is $0.03/0.10\times\sqrt{252} = 4.8$.
- The naive $\text{IC}\sqrt{N\cdot252} = 0.03\sqrt{504{,}000} = 21$ is what you would get if residuals were independent and IC constant; a simulation with iid residuals reproduces about 21, real data never does.

### 2. Turnover from autocorrelation

The same signal has day-to-day autocorrelation $\rho = 0.9$.

- Daily turnover: $\sqrt{2(1-0.9)} = 0.447$ of gross (simulation: 0.446).
- At 5 bp one-way cost, daily cost is $0.447 \times 5 = 2.24$ bp against 7.5 bp of alpha, leaving 5.3 bp.
- Break-even cost: $7.52/0.447 = 16.8$ bp per unit traded.
- At $\rho = 0.99$ turnover falls to $0.141$; the question is how much IC the slower version keeps.

### 3. Choosing the horizon from IC decay

Marginal IC decays geometrically: $\text{IC}(1) = 0.03$, $\delta = 0.8$.

- Half-life: $\ln 2/\ln 1.25 = 3.1$ days.
- Cumulative-horizon IC: $h=1$: 0.030; $h=2$: $0.054/\sqrt2 = 0.038$; $h=5$: $0.1008/\sqrt5 = 0.045$; $h=10$: $0.1339/\sqrt{10} = 0.042$; $h=20$: 0.033.
- The IC is maximised near $h = 5$, and the total harvestable IC is $0.03/0.2 = 0.15$.

So target a roughly weekly holding period and check that the implied turnover leaves positive net alpha.

### 4. Neutralising against sector and beta

Six stocks, the first three in tech.
Raw signal $s = (2.0, 1.5, 1.0, 0.0, -0.5, -1.0)$, betas $(1.4, 1.2, 1.0, 0.8, 0.7, 0.9)$.
The raw signal has correlation 0.93 with the tech dummy: it is mostly a sector bet.

- Regress $s$ on [tech dummy, non-tech dummy, beta]: coefficients $(-0.3, -1.7, 1.5)$.
- Residual: $s^{\perp} = (0.20, 0.00, -0.20, 0.50, 0.15, -0.65)$.
- Check: it sums to zero within each sector and $\sum_i\beta_i s^{\perp}_i = 0.28 - 0.20 + 0.40 + 0.105 - 0.585 = 0$.

Sector demeaning alone would give $(0.5, 0, -0.5, 0.5, 0, -0.5)$, which still carries beta exposure inside tech.

```python
import numpy as np
s = np.array([2.0, 1.5, 1.0, 0.0, -0.5, -1.0])
tech = np.array([1, 1, 1, 0, 0, 0])
beta = np.array([1.4, 1.2, 1.0, 0.8, 0.7, 0.9])
X = np.column_stack([tech, 1 - tech, beta])
coef, *_ = np.linalg.lstsq(X, s, rcond=None)
print(coef, s - X @ coef)  # [-0.3 -1.7 1.5] [0.2 0. -0.2 0.5 0.15 -0.65]
```

### 5. Pearson versus rank IC with one outlier

Signal $(0.1, 0.2, 0.3, 0.4, 0.5, 5.0)$, next-day returns $(-1\%, 0, 1\%, 2\%, 3\%, -5\%)$.
Pearson IC is $-0.83$ because one extreme score met one bad return; rank IC is $+0.14$.
Winsorise or rank the signal before trading it, or the book will be driven by that one name.

## Pitfalls

- Measuring IC against raw returns for a book that will be factor-neutral, so factor luck is credited to the signal.
- Pooling IC over all dates and names into one correlation, which hides regime dependence and overweights high-dispersion days.
- Using overlapping $h$-day returns daily and computing the IC $t$-stat as if the observations were independent; the effective sample is about $n/h$.
- Normalising with full-sample means or volatilities (look-ahead) instead of expanding or rolling estimates.
- Picking the horizon with the best in-sample IC among many horizons without counting it as a search.
- Forgetting that a signal's IC is measured on the whole universe while the book trades only liquid names, where IC is usually lower.
- Treating the naive $\text{IC}\sqrt N$ Sharpe as achievable: correlated residuals and IC volatility dominate.

## Interview questions

> [!question]- alpha-signal-ic-definition | Define the information coefficient and rank IC.
> IC is the cross-sectional correlation at date $t$ between the signal and subsequent returns; rank IC uses the ranks of both.
> Report the time series of daily ICs: mean, standard deviation, their ratio and the fraction positive, not a single pooled number.

> [!question]- alpha-signal-ic-to-sharpe | A daily-rebalanced signal has mean IC 0.03 and IC standard deviation 0.10. What is its approximate gross Sharpe?
> About 4.8.
> A signal-weighted book's daily return is proportional to that day's IC, so Sharpe $\approx 0.03/0.10\times\sqrt{252} = 4.76$.

> [!question]- alpha-signal-ic-pnl-dispersion | Why does the same IC produce different PnL in different regimes?
> Book return is about $\text{IC}\times\sigma_{cs}/E|z|$ per unit gross, so it scales with cross-sectional return dispersion.
> Dispersion is high in stressed markets and low in quiet ones, so constant IC does not mean constant PnL.

> [!question]- alpha-signal-turnover-autocorr | A standardised signal has autocorrelation 0.9 between rebalances. Roughly what fraction of gross does a signal-proportional book trade each time?
> About 45%.
> $z_t - z_{t-1}$ has standard deviation $\sqrt{2(1-\rho)} = \sqrt{0.2} = 0.447$ relative to $z_t$, and for Gaussian scores the ratio of mean absolute values equals that.

> [!question]- alpha-signal-breakeven-cost | A book earns 7.5 bp of gross per day and turns over 45% of gross daily. What is the break-even one-way cost?
> About 16.7 bp per unit traded.
> Break-even cost = alpha per day / turnover per day $= 7.5/0.45$.

> [!question]- alpha-signal-half-life | Marginal IC decays by a factor of 0.8 per day. What is the half-life?
> About 3.1 days.
> Solve $0.8^h = 0.5$: $h = \ln 2/\ln 1.25 = 3.11$.

> [!question]- alpha-signal-horizon-ic-peak | Why does IC against $h$-period cumulative returns peak at an intermediate horizon?
> The numerator $\sum_{k\le h}\text{IC}(k)$ saturates once the signal has decayed, while return volatility keeps growing like $\sqrt h$.
> So $\text{IC}_{[1,h]} = \sum_{k\le h}\text{IC}(k)/\sqrt h$ rises then falls.

> [!question]- alpha-signal-neutralise-method | How do you neutralise a signal against sectors and beta?
> Regress the signal cross-sectionally on sector dummies and beta each date and keep the residual.
> The residual is orthogonal to every regressor, so a book proportional to it has zero net sector and beta exposure under those weights; use a risk model in the optimiser for exact neutrality.

> [!question]- alpha-signal-rank-vs-pearson | When should you prefer rank IC over Pearson IC?
> When the signal or returns have outliers or you care only about ordering.
> Rank IC is invariant to monotone transforms and one extreme score cannot flip its sign; Pearson IC better matches a linearly weighted book once the signal is winsorised.

> [!question]- alpha-signal-capacity-turnover | Under square-root impact, how does break-even capacity scale with turnover at fixed daily alpha?
> Like $1/T^3$.
> Cost is $TA\cdot Y\sigma\sqrt{TA/V}$ and alpha is $\alpha A$; equating gives $A = V\alpha^2/(Y^2\sigma^2T^3)$.

> [!question]- alpha-signal-delay-test | What is a signal delay test and what does failure indicate?
> Lag the signal by one extra period before trading and remeasure IC and PnL.
> If performance collapses with one bar of delay, suspect timestamp leakage or an unrealistic execution assumption before believing the alpha is just very fast.

> [!question]- alpha-signal-grinold-alpha | How does Grinold turn a z-score into an expected return?
> $\alpha_i = \text{IC}\times\sigma_i\times z_i$.
> This is the conditional mean of residual return given the score when score and return are jointly normal with correlation IC; it shrinks weak signals toward zero automatically.

## In this repo and SDE-Interview-Prep

- Related notes: [Cross-Sectional Factor Models](04-Cross-Sectional-Factor-Models.md), [Transaction Costs and Turnover](13-Transaction-Costs-and-Turnover.md), [Linear Regression OLS](../02-Statistics-and-Econometrics/04-Linear-Regression-OLS.md).

## Further reading

- Grinold and Kahn, *Active Portfolio Management*
- Michael Isichenko, *Quantitative Portfolio Management*
- Qian, Hua and Sorensen, *Quantitative Equity Portfolio Management* (2007).
- Almgren, Thum, Hauptmann and Li (2005), Direct Estimation of Equity Market Impact, Risk.
