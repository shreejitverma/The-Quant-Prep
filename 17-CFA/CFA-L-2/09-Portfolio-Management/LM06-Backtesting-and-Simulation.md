---
type: cfa-lm
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
volume: 9
lm: 6
title: "Backtesting and Simulation"
pages: "321-380"
weight_band: "10-15%"
difficulty: 2
los_count: 7
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/portfolio-management]
---

# LM6: Backtesting and Simulation

Difficulty 2 of 5: the arithmetic is light (weighted averages, ratio checks, parameter counts), but the exam lives on precise vocabulary discrimination - survivorship vs. look-ahead vs. data snooping, scenario vs. sensitivity analysis, historical vs. Monte Carlo simulation - and the distractors are always the neighboring term.

## LOS map

- **describe** objectives in backtesting an investment strategy (V9 p.321) ^los-09-06-a
    - Examiner asks: state that backtesting approximates the real-life investment process using historical data to assess the risk-return trade-off, that it serves as an acceptance or rejection criterion, and that its implicit assumption is that the future will at least somewhat resemble the past.
- **describe** and contrast steps and procedures in backtesting an investment strategy (V9 p.321) ^los-09-06-b
    - Examiner asks: order the three steps (strategy design, historical investment simulation, analysis of output), name the key parameters set in design (universe, return definition, rebalancing frequency, start/end dates), and explain why a rolling-window procedure must be run twice for a risk parity strategy.
- **interpret** metrics and visuals reported in a backtest of an investment strategy (V9 p.321) ^los-09-06-c
    - Examiner asks: given a table of VaR, CVaR, max drawdown, standard deviation, skewness and kurtosis for several factor strategies, rank downside risk, identify which strategy a risk-averse investor prefers, and read a log-scale cumulative-wealth chart for structural breaks.
- **identify** problems in a backtest of an investment strategy (V9 p.321) ^los-09-06-d
    - Examiner asks: match a scenario to survivorship bias, look-ahead bias (reporting lag, revisions, index additions), data snooping/p-hacking, or stale data, and name the fix (point-in-time data, reporting lags, a t-statistic hurdle above 3.0, cross-validation).
- **evaluate** and interpret a historical scenario analysis (V9 p.321) ^los-09-06-e
    - Examiner asks: given Sharpe ratios in recession vs. non-recession and high-volatility vs. low-volatility regimes, say which strategy is robust across regimes and recognize that splitting history by regime is scenario analysis, not sensitivity analysis.
- **contrast** Monte Carlo and historical simulation approaches (V9 p.321) ^los-09-06-f
    - Examiner asks: which approach samples with replacement from actual history (bootstrapped historical simulation) versus which fits a functional form and draws from it (Monte Carlo), and the false statement that either is deterministic or avoids random number generation.
- **explain** inputs and decisions in simulation and interpret a simulation; and demonstrate the use of sensitivity analysis (V9 p.321) ^los-09-06-g
    - Examiner asks: walk the eight simulation steps, count the parameters a multivariate normal calibration needs for K factors, compute a trial's portfolio return from simulated factor returns and weights, and identify swapping the multivariate normal for a multivariate skewed t-distribution as sensitivity analysis.

## Core intuition

The module answers one practical question: before committing client money to a strategy, how do you rigorously estimate what its risk and return would look like (V9 p.321, p.322)?
Four techniques form a ladder of increasing generality.
Backtesting asks "how would this strategy have performed if implemented in the past" over a long history (V9 p.322).
Historical scenario analysis (historical stress testing) asks the same question inside discrete regimes, such as recessions or high-volatility periods (V9 p.322, p.350).
Simulation asks how the strategy performs in hypothetical environments, because the past happened only one way and cannot contain every possible future (V9 p.322, p.354).
Sensitivity analysis then shakes the simulation's assumptions to see which conclusions survive (V9 p.322, p.363).

> [!abstract] Idea 1: backtesting is a rejection filter built on one fragile assumption
> Backtesting approximates the real-life investment process with historical data to assess whether a strategy would have produced desirable results, and managers use it as an acceptance or rejection criterion (V9 p.322).
> A good backtest does not guarantee future excess returns, and a failed backtest does not preclude them, but no manager or client will adopt a strategy that failed in the past (V9 p.322).
> The implicit assumption is that the future will at least somewhat resemble history, and everything after the backtesting sections of this module (scenario analysis, simulation, sensitivity analysis) exists to compensate for the ways that assumption fails (V9 p.322, p.354).

Backtesting fits quantitative and systematic styles naturally, but fundamental managers use it too, for example to check whether a screening criterion such as a valuation metric would have added excess return historically (V9 p.322).
The process has exactly three steps: strategy design, historical investment simulation, and analysis of backtesting output (V9 p.323).

Step 1, strategy design, turns a hypothesis ("cheap stocks outperform expensive stocks") into rules plus key parameters (V9 p.323).
The investment universe is the set of securities you can potentially hold; practitioners typically use broad index constituents, such as the Russell 3000 for the United States (V9 p.323, p.324).
The return definition matters once the universe goes global: returns are computed either in a single home currency or in local currencies, with the choice usually following whether the manager hedges currency risk, and a benchmark must be specified if the goal is excess return (V9 p.324).
Rebalancing frequency is typically monthly; higher frequency means more trading and higher transaction costs, plus bid-ask, asynchronous-trading and holiday distortions at daily frequency, and many anomalies vanish once transaction costs are included, so the analyst must disclose whether costs are in (V9 p.324).
Start and end dates should span as long a history as possible for statistical confidence, but long histories are non-stationary, so long-sample results should be supplemented with regime-by-regime scenario analysis (V9 p.324).

Step 2, historical investment simulation, forms the portfolio each period and rebalances it on the pre-determined schedule using rolling windows: calibrate on an in-sample window, trade, record the next out-of-sample period, roll forward, repeat (V9 p.326).
This walk-forward design replicates live investing, where positions adjust as new information arrives; for the value strategy, each month-end the trailing 12-month earnings yield is recomputed and the portfolio re-formed, with the following month recorded out of sample (V9 p.326, p.327).

Step 3, output analysis, computes performance and risk metrics (Sharpe ratio, Sortino ratio, volatility, maximum drawdown) and draws the visuals: return time series, return distributions against the normal, and cumulative performance on a logarithmic scale, where equal percentage changes plot as equal vertical distances (V9 p.327).
Log-scale cumulative plots expose downside risk, performance decay, and structural breaks - regime changes driven by recessions, geopolitical events, monetary and fiscal policy shifts such as QE, and technological change (V9 p.327).

> [!abstract] Idea 2: the long-short hedged quantile portfolio is the laboratory instrument of factor research
> To isolate a factor, sort the universe by the factor metric, split into quantiles (quintiles or deciles), go long the top quantile and short the bottom quantile, with stocks equally weighted or cap weighted inside each quantile (V9 p.327, p.328).
> The spread between the extreme quantiles is a straightforward characterization of the factor's performance, even though the quantiles are not beta-matched and carry exposures to other factors (V9 p.328).
> The Fama-French pioneered design makes the strategy self-financing, which is why the module quotes Sharpe ratios as return over volatility with no explicit risk-free deduction, and its main practical drawback is that not every manager can short stocks (V9 p.327, p.339).
> The portfolio-sort approach is the coarse-grained cousin of the Spearman rank information coefficient used in multifactor model construction: both ask whether the ranking by the factor at the start of the period lines up with the ranking of realized returns (V9 p.327; the rank IC formula itself is LM04 toolkit, not printed in this module).

Applied to trailing earnings yield (chosen over P/E because earnings yield is computable when EPS is zero or negative), the US backtest over January 1986 to May 2019 shows average annual return 9.24%, volatility 12.36%, Sharpe ratio 0.75, and maximum drawdown -41.04%; Europe shows 6.65%, 9.90%, 0.67, and -30.20% (V9 p.325, p.328).
The distribution of the US strategy's returns shows negative skewness and excess kurtosis: surprises are likely, and likely to be negative (V9 p.329, p.330).

Real strategies are multifactor.
The module builds two: a benchmark (BM) portfolio equally weighting eight fundamental factor portfolios (earnings yield, book-to-market, EPS growth, momentum, earnings revision, ROE, debt/equity, earnings quality), and a risk parity (RP) portfolio weighting the same eight so each contributes equal risk (V9 p.331, p.332).
Backtesting the RP strategy needs the rolling-window procedure twice: once to form the eight factor portfolios monthly, and a second time to estimate the trailing five-year covariance matrix from which the equal-risk-contribution weights are optimized, precisely to avoid look-ahead bias in the weights (V9 p.332, p.333).
The punch line of the output analysis is diversification arithmetic: the RP portfolio's cumulative return is lower, but its volatility is less than half the BM portfolio's, so its Sharpe ratio is nearly twice as high, and every downside-risk measure (VaR, CVaR, maximum drawdown) is dramatically better (V9 p.333, p.335, p.336, p.338).
Six of eight factor portfolios and the BM portfolio are negatively skewed, and all show kurtosis above 3.0, so normal-distribution intuition understates their tail risk (V9 p.335, p.336).

> [!abstract] Idea 3: every backtesting sin is a way of knowing the future
> Survivorship bias draws conclusions from only the entities that survived to today: backtesting on current index constituents assumes you knew in 1986 which firms would still exist in 2019, and it silently excludes the delisted firms - the bankruptcies, acquisitions and demotions whose bad returns the survivors never show (V9 p.340, p.341, p.342).
> Look-ahead bias, the most common practitioner mistake, uses any information unavailable at the historical decision date; survivorship bias is a special case, and its other forms are reporting lags, data revisions, and vendors backfilling history when adding companies (V9 p.343, p.344).
> Data snooping (p-hacking) makes the inference after seeing the statistics: run many strategies, keep the winner, and the "significance" is manufactured by multiple testing rather than by any real effect (V9 p.346).

The low-volatility anomaly makes survivorship bias vivid: on point-in-time Russell 3000 constituents, low-volatility stocks beat high-volatility stocks over three decades, but on the survivor universe the result inverts and high-volatility stocks win by about 5.5 times, because the excluded delisted firms were disproportionately the high-volatility blowups (V9 p.342, p.343).
Point-in-time data - the most complete data as it existed at each prior date - is the fix for both survivorship and look-ahead bias, but not for data snooping, since you can snoop on point-in-time data just as easily (V9 p.342, p.344, p.349).
Where point-in-time data is unavailable, analysts add reporting lags; the lag that best replicates point-in-time results is one to two months in the US, Canada and Japan, two to three in Europe, the UK and ANZ, and three months in Asia ex-Japan, LATAM and emerging EMEA, and a uniform lag inevitably makes some large-cap data stale (V9 p.344).
With no lag at all, look-ahead bias inflated the US value strategy's performance by almost 100% (V9 p.344).

The defenses against data snooping are behavioral and statistical.
Raise the significance hurdle to a t-statistic above 3.0 rather than the usual 2.0, which is the practical expression of the deflated Sharpe ratio idea: after many trials, the best in-sample Sharpe ratio is biased upward by luck, so the threshold for believing it must rise with the number of tests (V9 p.346).
And cross-validate: test the model built on training data against separate validation data, either by rolling windows (a deterministic, non-random form of cross-validation) or across geographies, as when the risk parity result was confirmed in 10 global markets with lower volatility in all 10 and higher Sharpe ratio in 7 (V9 p.346, p.347, p.348).
These pitfalls are behavioral at root: analysts want the strategy to work, so they unconsciously select samples, models and metrics that flatter it, which is why the module frames survivorship and look-ahead bias as behavioral issues to guard against in interpretation (V9 p.369).

Scenario analysis takes the structural breaks seriously instead of averaging over them.
Define regimes - NBER recessions vs. expansions, or VIX above vs. below its five-year moving average for high- vs. low-volatility - and compare strategy performance regime by regime, remembering that recession inflection points are only identified in hindsight (December 2007's recession start was announced in December 2008) (V9 p.350, p.351).
The RP strategy's Sharpe ratio is robust to recession and to both volatility regimes, while the BM strategy struggles in recessions; density plots per regime add the information that both strategies have flatter (higher variance) distributions outside recessions and lower means inside them (V9 p.351, p.352, p.353).

> [!abstract] Idea 4: simulation replaces "the one past" with many possible pasts, and sensitivity analysis stress-tests the distribution you chose
> Historical simulation randomly draws (usually with replacement - bootstrapping) monthly return sets from actual history, ignoring time order: a non-deterministic rolling-window backtest that still assumes history spans the future (V9 p.354, p.355).
> Monte Carlo simulation assigns each key decision variable a statistical distribution, calibrates the parameters from history, and draws from the fitted distribution, so it can generate outcomes history never produced; the cost is complexity, computation, and total dependence on the chosen functional form (V9 p.354, p.359, p.360).
> Because factor returns show negative skewness, excess kurtosis and tail dependence, a multivariate normal fit understates downside risk; sensitivity analysis reruns the simulation under a multivariate skewed Student's t-distribution to see which conclusions depend on the distributional assumption (V9 p.360, p.363, p.364).

The eight-step simulation recipe is exam fodder: (1) define the target variable, typically the strategy return; (2) specify the key decision variables, the underlying asset or factor returns and weights; (3) choose the number of trials N, typically 1,000 to 10,000, with more trials giving more stable estimates; (4) specify the distributional properties, which is where historical and Monte Carlo diverge; (5) draw N random numbers per key decision variable; (6) compute the target variable per trial; (7) repeat to N; (8) analyze the N outcomes with the usual metrics, with CVaR and maximum drawdown preferred for downside risk (V9 p.354, p.355).
In the historical simulation, a uniform draw on [0, 1) is converted to one of the 374 historical months by slicing the interval into widths of 1/374 = 0.00267 - the inverse transformation method, converting a random number into a simulated value of the random variable (V9 p.355, p.379).
In the Monte Carlo version, the multivariate normal is the standard first cut because it needs only K means, K standard deviations and K(K-1)/2 correlations - 44 parameters for K = 8 - while a richer model with more parameters trades specification error for estimation error, the bias-variance trade-off from the big data readings (V9 p.360).
Correlated factors must be modeled jointly with a multivariate distribution, never factor by factor on a standalone basis (V9 p.360).
Tail dependence - the tendency of extreme negative factor returns to arrive together, summarized in the literature by a tail-dependence coefficient measuring the probability of joint extremes - is exactly what the normal fit misses most (V9 p.359, p.360).

The verdict from running all four methods on the BM and RP strategies: Sharpe ratio conclusions are robust to method (RP beats BM everywhere), but CVaR is sensitive - both Monte Carlo variants understate the BM strategy's downside risk relative to backtesting and historical simulation, because equal weighting ignores factor risks and correlations and leaves the BM portfolio exposed to the skewed, fat-tailed reality the fitted distributions fail to capture; the RP strategy, with its symmetric low-kurtosis return distribution, is robust across all methods (V9 p.358, p.362, p.363, p.364, p.365).
When even the skewed t rerun cannot reproduce the left tail, the honest conclusion is to run further sensitivity analyses with other functional forms (V9 p.364).

## Formulas and derivations

**Formula 1: trailing earnings yield** (V9 p.325)
$$
\text{Trailing earnings yield} = \frac{\text{Trailing 12-month EPS}}{\text{Current share price}}
$$
^f-09-06-1

- Trailing 12-month EPS: sum of the last four reported quarterly EPS; current share price: price on the rebalancing date.
- It is the inverse of the P/E, preferred because it remains computable and interpretable when EPS is zero or negative, where P/E breaks down (V9 p.325).
- Higher earnings yield = cheaper stock, so the value strategy buys the top quintile and shorts the bottom quintile of this metric.

**Formula 2: long-short hedged quantile portfolio return** (V9 p.327, p.328)
$$
r_{LS,t} = r_{\text{top quantile},t} - r_{\text{bottom quantile},t}
$$
^f-09-06-2

- $r_{\text{top quantile},t}$: return of the (equally or cap-weighted) basket of stocks in the best quantile by the factor; bottom quantile likewise for the worst.
- Sort the universe by the factor, cut into quintiles or deciles, long the top, short the bottom; the spread isolates the factor payoff without requiring a net cash outlay (V9 p.327).
- The quantiles are not beta-neutral and can carry other factor exposures, so the spread is a characterization, not a pure factor return (V9 p.328).

**Formula 3: portfolio return from constituent weights** (V9 p.354)
$$
r_{p,t} = \sum_{i=1}^{K} \left( \omega_{i,t} \times r_{i,t} \right)
$$
^f-09-06-3

- $\omega_{i,t}$: weight of asset or factor $i$ at time $t$, set by the strategy (0.125 each for the equal-weight BM portfolio; optimized equal-risk-contribution weights for RP); $r_{i,t}$: return of asset or factor $i$; $K$: number of assets.
- This is the target-variable computation inside every simulation trial: draw or simulate the $K$ factor returns, apply the weights, record $r_{p,t}$ (V9 p.354, p.356).

**Formula 4: annualized return from monthly returns** (V9 p.328)
$$
r_{\text{ann}} = \left[ \prod_{t=1}^{12} \left(1 + r_t\right) \right] - 1 \approx 12 \times \bar{r}_{\text{monthly}}
$$
^f-09-06-4

- $r_t$: monthly return; the arithmetic approximation is what turns the BM portfolio's 0.5% monthly mean into roughly 6% per year (V9 p.328, p.335).
- Exhibit 3's "avg annual return" figures (9.24% US, 6.65% Europe) are annualized from the monthly long-short return series (V9 p.328).

**Formula 5: annualized volatility from monthly volatility** (V9 p.328)
$$
\sigma_{\text{ann}} = \sigma_{\text{monthly}} \times \sqrt{12}
$$
^f-09-06-5

- Holds under independent monthly returns, since variances add over time; it converts the BM portfolio's 1.6% monthly standard deviation into about 5.5% annualized (V9 p.328, p.335).

> [!tip] Calculator
> Annualize on the BA II Plus: monthly sd `.016 x 12 SQRT = ` gives 0.0554; annual Sharpe from annual figures: `9.24 / 12.36 = ` gives 0.7476, printed as 0.75.

**Formula 6: Sharpe ratio** (V9 p.327, p.328)
$$
\text{Sharpe ratio} = \frac{r_p - r_f}{\sigma_p}
$$
^f-09-06-6

- $r_p$: annualized strategy return; $r_f$: risk-free rate; $\sigma_p$: annualized volatility.
- For a self-financing long-short portfolio the module quotes return over volatility directly: 9.24/12.36 = 0.75 (US) and 6.65/9.90 = 0.67 (Europe), which Python reproduces as 0.7476 and 0.6717 (V9 p.328).
- It is the headline risk-adjusted metric in every backtest and simulation comparison in the module (V9 p.327, p.362).

**Formula 7: Sortino ratio** (V9 p.327)
$$
\text{Sortino ratio} = \frac{r_p - r_{\text{target}}}{\sigma_{\text{downside}}}
$$
^f-09-06-7

- $\sigma_{\text{downside}}$: standard deviation computed only from returns below the target (often $r_f$ or zero).
- Penalizes only downside volatility, so it rewards positively skewed strategies that the Sharpe ratio treats identically to negatively skewed ones; the module lists it among the standard backtest output metrics (V9 p.327).

**Formula 8: maximum drawdown** (V9 p.327)
$$
\text{MDD} = \min_t \left( \frac{V_t - V_{\text{peak},t}}{V_{\text{peak},t}} \right)
$$
^f-09-06-8

- $V_t$: cumulative wealth at $t$; $V_{\text{peak},t}$: highest cumulative wealth up to $t$; MDD is the worst peak-to-trough loss.
- It is the module's preferred single-number downside metric alongside CVaR; in Exhibit 3 the max drawdown runs just over three times annual volatility in both regions (41.04/12.36 = 3.32; 30.20/9.90 = 3.05) (V9 p.327, p.328, p.330).

**Formula 9: VaR and CVaR at 95%** (V9 p.335, p.338)
$$
\text{VaR}_{95} = -Q_{5\%}(r), \qquad \text{CVaR}_{95} = -\mathbb{E}\left[ r \mid r \le Q_{5\%}(r) \right]
$$
^f-09-06-9

- $Q_{5\%}(r)$: the 5th percentile of the return distribution; VaR says losses will be at least this large 5% of the time; CVaR is the weighted average of all losses beyond the VaR threshold.
- CVaR is the more comprehensive tail measure and the module's preferred downside statistic for simulations, together with maximum drawdown (V9 p.355, p.376).

**Formula 10: skewness and excess kurtosis of returns** (V9 p.335, p.336)
$$
\text{Skew} = \frac{\mathbb{E}\left[(r-\mu)^3\right]}{\sigma^3}, \qquad \text{Excess kurtosis} = \frac{\mathbb{E}\left[(r-\mu)^4\right]}{\sigma^4} - 3
$$
^f-09-06-10

- Negative skew: surprises are more likely negative; kurtosis above 3.0 (positive excess): fat tails, extreme returns more likely than the normal predicts (V9 p.330, p.335).
- Six of the eight factor portfolios and the BM portfolio are negatively skewed and all show kurtosis above 3.0, which is why normal-based Monte Carlo understates their downside risk (V9 p.335, p.363).

**Formula 11: parameters of a multivariate normal calibration** (V9 p.360)
$$
\#\text{params} = \underbrace{K}_{\text{means}} + \underbrace{K}_{\text{std devs}} + \underbrace{\frac{K(K-1)}{2}}_{\text{correlations}}
$$
^f-09-06-11

- For the module's $K = 8$ factors: 8 + 8 + 28 = 44 parameters; the practice problems use $K = 9$ (36 correlations) and $K = 6$ (15) (V9 p.360, p.378).
- Few parameters means low estimation error but possible mis-specification; many parameters fit better but estimate worse - the bias-variance trade-off (V9 p.360).

> [!tip] Calculator
> Correlation count: `K x ( K - 1 ) / 2 =`. For 9 factors: `9 x 8 / 2 = 36`. The trap answer uses only the correlated subset (6 factors gives 15).

**Formula 12: inverse transformation, uniform draw to historical month** (V9 p.355, p.379)
$$
\text{Month } m \text{ selected} \iff \frac{m-1}{N_{\text{months}}} \le u < \frac{m}{N_{\text{months}}}, \quad \text{i.e. } m = \lceil u \times N_{\text{months}} \rceil
$$
^f-09-06-12

- $u$: uniform random draw on [0, 1); $N_{\text{months}}$: size of the historical sample (374 months, April 1988 to May 2019), so each slice has width 1/374 = 0.00267 (V9 p.355).
- A draw between 0 and 0.00267 selects Month 1, between 0.00267 and 0.00535 selects Month 2, and in general the draw divided by 0.00267 rounds up to the month number (V9 p.355, p.356).
- This is the inverse transformation method: converting a randomly generated uniform number into a simulated value of a random variable (V9 p.379).

**Formula 13: Spearman rank information coefficient (background; not printed in this module)** (V9 p.327)
$$
\text{IC}_{\text{rank}} = \rho\left( \text{rank}(f_{i,t}),\ \text{rank}(r_{i,t+1}) \right)
$$
^f-09-06-13

- $f_{i,t}$: factor score of stock $i$ at the rebalancing date; $r_{i,t+1}$: its subsequent out-of-sample return; $\rho$: correlation of the two rank vectors.
- A positive rank IC means the factor's ordering predicted the return ordering; the long-short quantile spread of Formula 2 is the portfolio implementation of the same idea, trading only the extreme ranks (V9 p.327).
- This is LM04 machinery; carry it here because item sets on factor backtests may quote an IC alongside quantile-spread returns.

**Formula 14: tail-dependence coefficient (background; not printed in this module)** (V9 p.359, p.360)
$$
\lambda_L = \lim_{q \to 0^+} P\left( r_2 \le Q_q(r_2) \mid r_1 \le Q_q(r_1) \right)
$$
^f-09-06-14

- $\lambda_L$: lower-tail dependence, the probability that asset 2 crashes into its worst $q$ tail given asset 1 did, in the limit of extreme tails.
- A multivariate normal has $\lambda_L = 0$ for any correlation below 1, which is exactly why it understates joint crash risk in factor returns that empirically exhibit tail dependence (V9 p.359, p.360).

**Formula 15: t-statistic hurdle against data snooping (deflated Sharpe idea)** (V9 p.346)
$$
t = \frac{\hat{\mu}}{\hat{\sigma}/\sqrt{n}} \gtrsim 3.0 \quad \text{(not the usual 2.0)}
$$
^f-09-06-15

- $\hat{\mu}, \hat{\sigma}$: mean and standard deviation of the strategy's excess returns over $n$ periods.
- With many strategies tested, the best one's in-sample t-statistic and Sharpe ratio are inflated by selection, so the acceptance hurdle must rise; requiring t above 3.0 is the curriculum's rule of thumb, and the research literature formalizes the same correction as the deflated Sharpe ratio, which discounts the observed Sharpe for the number of trials, non-normality and sample length (V9 p.346).
- The complementary defense is cross-validation on data not used to build the model, including other geographic markets (V9 p.347).

## Worked examples

**Example 1: strategy design (three knowledge checks)** (V9 p.324, p.325, p.326)
Koh designs a value backtest: goal is superior risk-adjusted absolute return; hypothesis is that cheap stocks (high trailing earnings yield, Formula 1) outperform; universe Russell 3000 plus S&P Europe BMI hedged into USD; period January 1986 to May 2019; monthly rebalancing with transaction costs.
Q1: which design feature should concern the investment committee? B - the long history spans recessions, currency regime changes and varying interest rates, so the data is non-stationary and results must be supplemented with discrete-regime scenario analysis; A fails because nothing in the design assumes dollar appreciation, and C fails because earnings yield is computable whenever EPS and price exist, which is exactly why it was chosen over P/E.
Q2: rebalancing frequency vs. transaction costs? A - moving from monthly to weekly rebalancing means more trading, hence higher costs; B describes lower frequency (quarterly), which cuts costs; C is wrong because rebalancing frequency is the primary driver of trading volume.
Q3: which is NOT a concern of a short backtest period? C - covering multiple business-cycle, inflation and rate regimes is not a short-sample concern, because regimes are multi-year; A and B (limited regimes, findings valid only for the sampled conditions) are the genuine short-sample worries. ^ex-09-06-1

**Example 2: historical investment simulation and output analysis (two knowledge checks)** (V9 p.328, p.329, p.330)
Q1: compare US and Europe value performance from Exhibit 3.
US: average annual return 9.24%, Sharpe 0.75 (Python: 9.24/12.36 = 0.7476); Europe: return lower by roughly 250 bps at 6.65% (Python: the exact gap is 9.24 - 6.65 = 259 bps; the curriculum's "250 bps" is rounded), volatility much lower at 9.90%, so the Sharpe of 0.67 (Python: 0.6717) lands close to the US figure.
In both markets maximum drawdown is just over three times annual volatility (Python: 41.04/12.36 = 3.32 US; 30.20/9.90 = 3.05 Europe), and on balance the strategy performed slightly better in the US.
Q2: cumulative performance and distribution.
Value delivered strong long-run performance in all four markets, strongest in Asia ex-Japan; performance leveled off outside Asia ex-Japan after 2002 and flattened everywhere but Asia ex-Japan since 2016; drawdowns and potential structural breaks appear in the late-1990s tech bubble and the March-May 2009 risk rally.
The US return distribution shows excess kurtosis (fat tails, more extreme surprises) and negative skewness (the surprises skew negative). ^ex-09-06-2

**Text demonstration: reading Exhibits 8 and 9, factor and allocation distributions (1993-2019)** (V9 p.335, p.336, p.338)
BM portfolio: monthly mean 0.5%, standard deviation 1.6%, skewness -2.40, kurtosis 17.78, minimum -10.9%, VaR(95) -2.6%, CVaR(95) -7.9%, max drawdown 22.6%.
RP portfolio: mean 0.4%, standard deviation 0.7%, skewness +0.51, kurtosis 5.37, minimum -2.5%, VaR(95) -0.7%, CVaR(95) -0.9%, max drawdown 3.8%.
Sanity check in Python: annualizing with Formulas 4 and 5 gives BM roughly 6.0% return on 5.5% volatility (Sharpe about 1.1) and RP roughly 4.8% on 2.4% (Sharpe about 2.0), consistent with Exhibit 7's finding that RP's volatility is less than half BM's and its Sharpe ratio nearly twice as high (V9 p.333).
Among single factors, momentum has the worst downside (VaR -8.4%, CVaR -22.9%, MDD 59.7%), then ROE; earnings quality has the smallest downside risk (V9 p.335, p.338). ^ex-09-06-3

**Example 3: risk and return beyond the normal distribution** (V9 p.337)
Q: which of BM and RP suits risk-averse investors?
Means are nearly equal (0.5% vs. 0.4% monthly) but RP dominates on every risk dimension: minimum -2.5% vs. -10.9%, standard deviation 0.7% vs. 1.6%, positive skew 0.51 vs. -2.40, moderate kurtosis 5.37 vs. 17.78, and superior VaR, CVaR and maximum drawdown.
Similar return, less downside, thinner tails, higher chance of positive surprises: the RP portfolio has the more attractive distributional properties for risk-averse investors. ^ex-09-06-4

**Example 4: backtesting factor allocation strategies (four knowledge checks)** (V9 p.337, p.339)
Q1: the inaccurate statement about rolling-window backtesting is A ("the data are divided into just two samples") - rolling windows create many overlapping in-sample/out-of-sample splits; B and C accurately describe the technique (out-of-sample data joins the next in-sample window; repeated train-test mimics live position adjustment).
Q2: the drawback of long-short hedged portfolios is C - not every manager can short stocks; A and B merely describe the construction.
Q3: the non-metric is B - a word cloud; distribution plots (A) and maximum drawdown (C) are genuine backtest outputs.
Q4: for risk parity the rolling-window procedure is used twice (C) - once to estimate factor returns and once to estimate the covariance matrix that sets the equal-risk weights; A misses the second use and B confuses rolling windows with a single split. ^ex-09-06-5

**Example 5: data snooping in investment management** (V9 p.347)
An analyst backtests models with 5 to 10 factors, monthly and quarterly rebalancing, and 5-, 15- and 25-year windows, then recommends the 10-factor monthly model because it produced the best statistics (Sharpe 3.0, volatility 1.0%, t = 2.5, p = 1.3%, the extremes across all trials).
Concerns: were transaction costs and liquidity included; and above all, model selection bias - picking the best of dozens of variants by t-statistic and p-value is data snooping, so the reported significance is inflated.
Mitigations: raise the acceptance hurdle to t above 3.0 (Formula 15) and cross-validate the chosen model on data not used in its construction (V9 p.346, p.347). ^ex-09-06-6

**Example 6: common problems in backtesting (five knowledge checks)** (V9 p.348, p.349, p.350)
Q1: picking the strategy with the highest t-statistic and lowest p-value after dozens of backtests is data snooping (C); reporting lag and survivorship bias describe different problems.
Q2: point-in-time data protects against everything EXCEPT data snooping (A) - you can still make inference after peeking at results; it does fix look-ahead bias and its special case survivorship bias.
Q3: GDP released about 30 days after quarter-end and revised repeatedly is reporting lag (C).
Q4: cross-validation is backtesting with out-of-sample data (B) - testing the hypothesis on data different from the data that formed it; maximum drawdown is a metric and point-in-time data is a bias fix.
Q5: the analyst whose December 2005 and December 1995 "Russell 3000" lists contain only 2,250 and 1,500 of the May 2019 constituents is using today's membership throughout history: look-ahead bias (C), corrected with point-in-time index constituents. ^ex-09-06-7

**Text demonstration: historical simulation of the BM and RP strategies, trial 1** (V9 p.355, p.356, p.357)
Setup per the eight steps: targets are BM and RP returns; decision variables are the eight factor returns; N = 1,000 trials; bootstrapped sampling (with replacement) from 374 months (April 1988 to May 2019); slice width 1/374 = 0.00267 (Formula 12).
The first five uniform draws map to months as follows (Python: draw x 374, rounded up): 0.59163 gives 221.27 so Month 222 (September 2006); 0.32185 gives 120.37 so Month 121 (April 1998); 0.76485 gives 286.05 so Month 287 (February 2012); 0.89474 gives 334.63 so Month 335 (February 2016); 0.45431 gives 169.91 so Month 170 (May 2002); all five match Exhibit 17.
Trial 1 (September 2006 factor returns: EY 2.5%, B/M 0.3%, growth -0.8%, momentum -0.0%, revision -0.8%, ROE 2.5%, D/E 0.5%, quality -0.5%).
BM return = equal-weight average = 0.125 x (2.5 + 0.3 - 0.8 - 0.0 - 0.8 + 2.5 + 0.5 - 0.5)% = 0.4625%, printed as 0.46% (Python: 0.4625).
RP return with May 2019 weights (6.0%, 30.3%, 11.7%, 5.2%, 10.4%, 6.3%, 9.6%, 20.4%) = 0.150 + 0.091 - 0.094 - 0.000 - 0.083 + 0.158 + 0.048 - 0.102 = 0.168%, printed as 0.17% (Python: 0.1676; Exhibit 18's rounded per-factor column sums to the same 0.17%).
Repeat for 1,000 trials, then compute Sharpe, CVaR and distribution plots; the results confirm the backtest ranking (RP beats BM on Sharpe and carries far less CVaR) (V9 p.357, p.358). ^ex-09-06-8

**Text demonstration: Monte Carlo trial 1 under multivariate normal and skewed t** (V9 p.360, p.361, p.364)
Monte Carlo setup differs only at Steps 4 and 5: fit a multivariate normal to the 374 months - 8 means, 8 standard deviations, 28 covariance elements, 44 parameters in all (Formula 11; Python: 8 + 8 + 8x7/2 = 44) - then draw 1,000 joint return sets from the fitted distribution.
Normal trial 1 (EY -3.2%, B/M -3.1%, growth -0.2%, momentum 0.7%, revision 2.3%, ROE -3.3%, D/E -1.7%, quality 1.9%): BM = 0.125 x sum = -0.825%, printed -0.83% (Python: -0.8250); RP with May 2019 weights = -0.863%, printed -0.86% (Python: -0.8626).
Sensitivity rerun swaps Step 4's distribution for a multivariate skewed Student's t and repeats Step 5.
Skewed-t trial 1 (EY 2.0%, B/M 0.3%, growth 1.7%, momentum 3.1%, revision 2.0%, ROE 0.9%, D/E 0.2%, quality -0.5%): BM = 1.2125%, printed 1.21% (Python: 1.2125); RP = 0.753%, printed 0.75% (Python: 0.7529).
All four printed portfolio returns reproduce exactly from the exhibits' factor returns and weights. ^ex-09-06-9

**Example 7: interpreting backtesting vs. historical vs. Monte Carlo results** (V9 p.362, p.363)
Backtesting gives realistic performance assuming the rules were followed through actual history; the two simulations independently verify it by injecting randomness differently - historical simulation bootstraps actual months with equal probability, Monte Carlo draws from a calibrated multivariate distribution.
Exhibit 22 Panel A: Sharpe ratios are insensitive to method, with RP beating BM by a similar margin under all three.
Panel B: CVaR is method-sensitive - Monte Carlo (multivariate normal) understates the BM strategy's downside risk versus both backtesting and historical simulation, because negatively skewed, fat-tailed factor returns violate the normal assumption; the naive equal weighting leaves BM exposed, while RP's risk-based weights make it robust to the non-normality. ^ex-09-06-10

**Example 8: simulating factor allocation strategies (six knowledge checks)** (V9 p.366, p.367, p.368)
Q1: the non-caveat about rolling-window backtesting is C (it is intuitive and mimics real investing - that is a virtue); A (assumes the past repeats) and B (misses market dynamics and extreme risks) are the true caveats.
Q2: data snooping is B - trying many modeling techniques and keeping the best performer without accounting for model selection bias; A (cross-validation across markets on point-in-time data) and C (t hurdle above 3.0) are the defenses.
Q3: least likely scenario analysis is A - switching the universe from Nikkei 225 to TOPIX 1000 changes no structural regime; trade-agreement vs. no-trade-agreement (B) and high- vs. low-volatility (C) are regime splits, hence scenario analysis.
Q4: the false statement is B - both historical and Monte Carlo simulation use a random number generator; A correctly describes bootstrapped historical sampling and C correctly describes calibrated multivariate sampling.
Q5: the false Monte Carlo statement is C - the process is random, not deterministic; A (specify a multivariate distribution for correlated assets) and B (regression and distribution fitting calibrate parameters) are true.
Q6: sensitivity analysis is A - changing the distributional assumption from multivariate normal to skewed t; B and C split history by regime, which is scenario analysis. ^ex-09-06-11

## Item-set patterns

> [!warning] Trap 1: survivorship vs. look-ahead vs. data snooping vs. reporting lag
> The vignette describes one flawed research practice and asks which problem it is.
> Correct mapping: current index members used through history = survivorship bias (a special case of look-ahead); revised or backfilled or unlagged data = look-ahead bias; picking the best of many backtests = data snooping; a uniform multi-month lag = stale data; delayed, revised macro releases = reporting lag (V9 p.340, p.343, p.346, p.377).
> Distractors are always the sibling biases; anchor on WHEN the information became available (look-ahead family) versus HOW the model was selected (snooping).

> [!warning] Trap 2: what point-in-time data does and does not fix
> A stem lists problems and asks which one point-in-time data cannot cure.
> Correct: point-in-time data fixes look-ahead bias and survivorship bias but never data snooping, because inference-after-peeking works on any dataset (V9 p.349).
> The tempting wrong answers exploit the fact that survivorship IS a form of look-ahead, making candidates think one of those two must be the odd one out.

> [!warning] Trap 3: scenario analysis vs. sensitivity analysis
> The vignette describes a rerun of the study and asks what technique it is.
> Correct: splitting by regime (recession/expansion, high/low volatility, trade-agreement/no-agreement) is scenario analysis; changing a model input or assumption, above all the distribution (normal to skewed t), is sensitivity analysis; changing the index universe is neither (V9 p.350, p.363, p.367).
> Distractors present the other label, and "Monte Carlo simulation" appears as a third option to catch candidates who conflate the rerun with the method being rerun.

> [!warning] Trap 4: deterministic or random?
> A statement claims some technique is deterministic or avoids random numbers.
> Correct: rolling-window backtesting is deterministic; historical simulation and Monte Carlo simulation are both non-deterministic and both use a random number generator; historical simulation draws actual months via uniform draws, Monte Carlo draws from a fitted distribution (V9 p.355, p.368, p.377).
> The classic false statement is "neither historical simulation nor Monte Carlo simulation makes use of a random number generator" (V9 p.368).

> [!warning] Trap 5: VaR vs. CVaR vs. maximum drawdown rankings
> An exhibit gives VaR, CVaR and max drawdown for three factors and asks which has the smallest or largest downside risk, sometimes defining the measure in words ("weighted average of all losses that exceed a threshold" = CVaR).
> Correct: match the verbal definition to the right column first, then rank; VaR = minimum loss 5% of the time, CVaR = average loss beyond VaR, MDD = worst peak-to-trough (V9 p.338, p.376).
> Distractors rank by the wrong column - a factor can have the smallest CVaR while carrying the largest max drawdown, exactly the layout of practice Q6 (V9 p.376).

> [!warning] Trap 6: standard deviation is not a downside risk measure substitute
> A junior analyst claims standard deviation makes max drawdown redundant, or that the strategy with the lowest volatility must have the lowest downside risk.
> Correct: volatility is symmetric; drawdown, VaR and CVaR capture the asymmetric left tail, and with negative skew and excess kurtosis the two disagree; both statements in the vignette can be wrong at once (V9 p.374, p.377).
> The tempting option is "only Statement 2 is incorrect" for candidates who accept the volatility-suffices claim.

> [!warning] Trap 7: counting covariance parameters
> A Monte Carlo design with K correlated factors asks how many parameters calibrate the multivariate normal.
> Correct: K means, K standard deviations, K(K-1)/2 covariance elements - for 9 factors that is 36 covariance elements even if only 6 factors are correlated (V9 p.360, p.378).
> The distractor computes the count on the correlated subset only (6x5/2 = 15) or forgets the means and standard deviations when a total is requested.

> [!warning] Trap 8: which distribution and which sampling scheme fits which method
> A concern is stated (correlated factors; skew and kurtosis; more trials than data) and the stem asks for the right design response.
> Correct: correlated factors need a multivariate distribution, never standalone fits; skew and excess kurtosis motivate a skewed t sensitivity rerun; needing more draws than history has means bootstrapping (sampling with replacement) in historical simulation (V9 p.355, p.360, p.363).
> Distractors cross the wires: interpolating fake observations into history, choosing a normal "initial functional form" for a historical simulation, or calling the skewed t rerun an inverse transformation (V9 p.378, p.379).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM06-Backtesting-and-Simulation-Practice-Problems]]

## Cross-links

- [[LM04-Using-Multifactor-Models]]: supplies the factor models being backtested here; the eight fundamental factors, factor portfolio construction, and the rank-IC logic behind quantile sorts all originate there, and this module is the audit process those models must pass.
- [[LM05-Measuring-and-Managing-Market-Risk]]: defines VaR, CVaR and the estimation approaches (historical, parametric, Monte Carlo) that this module reuses as backtest and simulation output metrics; the method-sensitivity of CVaR shown here is the practical face of LM05's model-risk warnings.
- [[LM02-Analysis-of-Active-Portfolio-Management]]: the Sharpe-ratio and information-ratio machinery for judging active strategies; backtested Sharpe ratios feed directly into LM02's fundamental-law thinking about whether a signal is worth deploying.
- [[../01-Quantitative-Methods/LM05-Time-Series-Analysis|LM05-Time-Series-Analysis]] (Quantitative Methods): non-stationarity and regime shifts are why long backtests mislead and why structural breaks demand scenario analysis; the stationarity assumption this module says fails is defined there.
- [[../01-Quantitative-Methods/LM07-Big-Data-Projects|LM07-Big-Data-Projects]] (Quantitative Methods): cross-validation, out-of-sample discipline, overfitting and the bias-variance trade-off invoked when choosing the simulation's functional form are all machine-learning concepts introduced there.

## Self-test

Vignette A for Q1 to Q4: Priya Nair backtests a quality-factor strategy for a Singapore family office.
She sorts the current MSCI World constituents by gross profitability each month from 2001 to 2025, buys the top decile, shorts the bottom decile, and rebalances monthly with no transaction costs.
Her assistant pulls fundamentals from a vendor database with each company's full restated history and applies no reporting lag.
The backtest shows an annualized return of 8.4%, annualized volatility of 7.0%, and maximum drawdown of -12.6%.
Nair also tested 40 variants (different quality metrics, universes and windows) and reports the one with t = 2.6, the highest of all variants.

> [!question] Q1
> The use of current MSCI World constituents throughout the backtest most directly introduces:
> A. survivorship bias, a special case of look-ahead bias.
> B. data snooping, a special case of look-ahead bias.
> C. reporting lag, a special case of stale data.

> [!question] Q2
> The unlagged, restated fundamentals most likely cause the backtest to:
> A. understate performance, because stale data delays signal updates.
> B. overstate performance, because information unavailable at the decision date is used.
> C. leave performance unbiased, because restatements are unbiased corrections.

> [!question] Q3
> The Sharpe ratio of Nair's strategy (risk-free rate 0 for the self-financed long-short book) is closest to:
> A. 0.83.
> B. 1.20.
> C. 1.80.

> [!question] Q4
> Given the 40 variants tested, the most appropriate response to the reported t-statistic of 2.6 is to:
> A. accept the strategy, because 2.6 exceeds the conventional 2.0 hurdle.
> B. reject or re-test the strategy, because multiple testing demands a hurdle above 3.0 and cross-validation on fresh data.
> C. accept the strategy after re-estimating it on the same sample with a longer rolling window.

Vignette B for Q5 to Q7: Marco Deluca simulates a three-factor allocation strategy (factors X, Y, Z) whose monthly returns are correlated, negatively skewed, and fat tailed.
He runs 2,000 trials of a historical simulation over a 250-month sample, then a Monte Carlo simulation under a fitted multivariate normal.
In one historical trial the uniform draw is 0.66200; in that month the factor returns are X 1.8%, Y -0.6%, Z 0.9%, and the strategy weights are 50%/30%/20%.

> [!question] Q5
> The historical month selected by the draw of 0.66200 and the trial's strategy return are closest to:
> A. Month 165 and 0.90%.
> B. Month 166 and 0.90%.
> C. Month 166 and 0.70%.

> [!question] Q6
> The number of parameters Deluca must calibrate for the multivariate normal (means, standard deviations, and correlations) is closest to:
> A. 6.
> B. 9.
> C. 12.

> [!question] Q7
> Relative to the historical simulation, the multivariate normal Monte Carlo will most likely:
> A. overstate CVaR losses, because normal tails are too fat.
> B. understate CVaR losses, because the normal has no excess kurtosis, no skew, and zero tail dependence.
> C. match CVaR, because both methods calibrate to the same history.

Vignette C for Q8 to Q10: A consultant reviews a manager's evaluation report.
Test 1 splits 1990-2025 results into NBER recession months and expansion months and compares Sharpe ratios.
Test 2 reruns the manager's Monte Carlo with a multivariate skewed t-distribution instead of a multivariate normal.
Test 3 re-estimates the strategy on point-in-time European data after developing it on point-in-time US data.
The report also plots cumulative wealth on a linear y-axis and concludes that "growth accelerated dramatically after 2015".

> [!question] Q8
> Tests 1, 2 and 3 are best described, respectively, as:
> A. scenario analysis; sensitivity analysis; cross-validation.
> B. sensitivity analysis; scenario analysis; data snooping.
> C. scenario analysis; simulation calibration; survivorship-bias correction.

> [!question] Q9
> The chart conclusion is most suspect because:
> A. a linear scale exaggerates late-period percentage growth; a logarithmic scale shows equal percentage changes as equal vertical distances.
> B. cumulative wealth charts cannot reveal structural breaks.
> C. performance decay is only visible in return histograms.

> [!question] Q10
> If the recession months were identified using NBER announcement dates as they were published, rather than the final dated chronology, the recession-regime Sharpe ratios would:
> A. be free of look-ahead bias, because announcements are real-time information.
> B. contain look-ahead bias, because announcements lag the cycle turning points they date.
> C. be unchanged, because regime dating does not affect scenario analysis.

> [!success]- Answer key
> Q1: A.
> Backtesting on today's constituents keeps only survivors; membership in 2025 was unknowable in 2001, which is why survivorship bias is a special case of look-ahead bias (V9 p.340, p.343).
> B is wrong because data snooping is a selection-of-results problem, not an information-timing problem; C mislabels the bias entirely.
> Q2: B.
> Restated financials and zero lag both inject information unavailable on the historical decision date; in the module's demonstration, full look-ahead bias inflated the US value strategy's performance by almost 100% (V9 p.344).
> A describes the cost of an overly long lag, the opposite adjustment; C ignores that only the revised figures, not the originals, sit in the database.
> Q3: B.
> Sharpe = 8.4/7.0 = 1.20 (Python: 1.20) with rf = 0 for the self-financing long-short portfolio (V9 p.328).
> A divides drawdown-ish numbers (8.4/10.1-style error) or inverts a ratio; C uses 12.6/7.0, mistaking drawdown for return.
> Q4: B.
> Forty trials mean the best t-statistic is inflated by selection; the module's fix is a hurdle above 3.0 plus cross-validation on data not used in development - the deflated Sharpe idea (V9 p.346, p.347).
> A applies the single-test hurdle to a multiple-test result; C re-uses the same sample, which cannot cure selection bias.
> Q5: B.
> Slice width is 1/250 = 0.004; 0.66200 x 250 = 165.5, which rounds up to Month 166 (draws between 0.660 and 0.664 map there) (Formula 12; V9 p.355).
> Return = 0.5(1.8) + 0.3(-0.6) + 0.2(0.9) = 0.90 - 0.18 + 0.18 = 0.90% (Formula 3; Python confirms).
> A truncates instead of rounding up; C miscomputes the weighted sum by dropping the Z term's sign handling.
> Q6: B.
> K = 3: 3 means + 3 standard deviations + 3x2/2 = 3 correlations = 9 (Formula 11; V9 p.360).
> A counts only means and standard deviations; C double-counts correlations as a full 3x3 matrix.
> Q7: B.
> The multivariate normal has zero excess kurtosis, zero skew, and zero tail dependence, so with negatively skewed fat-tailed factors it understates joint left-tail losses, exactly as Exhibit 22 showed for the BM strategy (V9 p.362, p.363).
> A inverts the direction; C confuses shared calibration inputs with shared tail behavior.
> Q8: A.
> Regime splits are scenario analysis; changing the distributional assumption is sensitivity analysis; re-testing on a different geography's point-in-time data is cross-validation (V9 p.350, p.363, p.347).
> B swaps the first two labels; C mislabels the second and third tests.
> Q9: A.
> The module recommends logarithmic scaling precisely so equal percentage changes plot equally; on a linear axis a constant growth rate looks like acceleration (V9 p.327).
> B is false - log-scale cumulative charts are the module's tool for spotting structural breaks; C is invented.
> Q10: A.
> Using announcement-date information as it became available is the point-in-time discipline; the module notes NBER dated the December 2007 recession start only in December 2008, so using the final chronology in a tradable strategy is the look-ahead sin, while using announcements as published avoids it (V9 p.350).
> B describes the announcements' lag, which creates staleness, not look-ahead bias; C ignores that regime dating IS the scenario definition.

## Flashcards

#flashcards/cfa-l2/09-Portfolio-Management/lm06

Main objective of backtesting::To understand the risk-return trade-off of an investment strategy by approximating the real-life investment process with historical data (V9 p.322).
Implicit assumption of backtesting::The future will at least somewhat resemble history (V9 p.322).
Three steps of backtesting::Strategy design, historical investment simulation, analysis of backtesting output (V9 p.323).
Key parameters set in strategy design::Investment universe, return definition, rebalancing frequency, start and end dates (V9 p.323).
Investment universe::All securities in which the strategy can potentially invest, typically broad index constituents (V9 p.323).
Why prefer earnings yield over P/E?::Earnings yield (EPS/price) is computable and interpretable even when EPS is zero or negative (V9 p.325).
Effect of higher rebalancing frequency::More trading, higher transaction costs, plus bid-ask and asynchronous-trading distortions at daily frequency (V9 p.324).
Trade-off in choosing backtest length::Longer samples give statistical confidence but financial data is non-stationary, so supplement with regime-level scenario analysis (V9 p.324).
Rolling-window backtesting::Calibrate on an in-sample window, test on the next out-of-sample period, roll forward and repeat, mimicking live investing (V9 p.326).
Is rolling-window backtesting deterministic or random?::Deterministic; historical and Monte Carlo simulation are the random methods (V9 p.355, p.377).
Long-short hedged portfolio construction::Sort by the factor, go long the top quantile and short the bottom quantile, equal or cap weighted within quantiles (V9 p.327).
Main drawback of long-short hedged portfolios::Not every manager can short stocks (V9 p.339).
Maximum drawdown::The maximum loss from a peak to a trough for an asset or portfolio (V9 p.327).
Why plot cumulative performance on a log scale?::Equal percentage changes appear as equal vertical distances, revealing downside risk, performance decay and structural breaks (V9 p.327).
Four example sources of structural breaks::Recessions/depressions, geopolitical events, major monetary and fiscal policy shifts such as QE, major technological change (V9 p.327).
US value strategy Sharpe check::9.24% return over 12.36% volatility gives 0.75 (V9 p.328).
Rule of thumb linking MDD and volatility in Exhibit 3::Maximum drawdown was just over three times annual volatility in both the US and Europe (V9 p.328, p.330).
Why is the rolling-window procedure applied twice for risk parity?::Once to form the factor portfolios and once to estimate the trailing covariance matrix that sets equal-risk weights, avoiding look-ahead bias (V9 p.332).
Risk parity factor portfolio::Weights factors so each contributes equally to total portfolio risk, using volatilities and correlations (V9 p.332).
BM vs. RP backtest verdict::RP has similar mean return, less than half the volatility, nearly twice the Sharpe ratio, and far smaller VaR, CVaR and drawdown (V9 p.333, p.338).
Signature distribution features of factor returns::Negative skewness, excess kurtosis (fat tails), and tail dependence (V9 p.335, p.371).
What does negative skew plus excess kurtosis imply?::Extreme returns are more likely than normal, and the surprises are more likely to be negative (V9 p.330).
Survivorship bias::Deriving conclusions from data reflecting only entities that survived to the present date (V9 p.341).
Excluded-delisted-firms effect on the low-vol anomaly::On point-in-time data low-vol beats high-vol; on survivors only, high-vol wins by about 5.5x because the delisted high-vol blowups are missing (V9 p.342, p.343).
Look-ahead bias::Using information that was unknown or unavailable during the historical period being tested; the most common practitioner mistake (V9 p.343).
Three common forms of look-ahead bias::Reporting lags, data revisions/restatements, and vendors backfilling history when adding companies (V9 p.343, p.344).
Point-in-time data::The most complete data as it actually existed at each prior date; fixes look-ahead and survivorship bias (V9 p.342).
Which bias can point-in-time data NOT fix?::Data snooping, because inference-after-peeking works on any dataset (V9 p.349).
Cost of a uniform reporting-lag assumption::Stale data for the larger-cap companies that report faster than the lag assumes (V9 p.344).
Regionally appropriate reporting lags::1-2 months for US, Canada, Japan; 2-3 for Europe, UK, ANZ; about 3 for Asia ex-Japan, LATAM, emerging EMEA (V9 p.344).
Data snooping (p-hacking)::Making an inference after looking at statistical results rather than testing a prior inference, e.g. keeping the best of many backtests (V9 p.346).
Two defenses against data snooping::A t-statistic hurdle above 3.0 (the deflated Sharpe idea) and cross-validation on training vs. validation data (V9 p.346).
Cross-validation in backtesting::Testing the model built on one dataset against different data, via rolling windows or other geographic markets (V9 p.346, p.347).
Historical scenario analysis::A type of backtesting that explores strategy performance and risk in different structural regimes and at structural breaks (V9 p.350).
Two common regime pairs for scenario analysis::Recession vs. expansion (NBER) and high vs. low volatility (VIX vs. its five-year moving average) (V9 p.350).
Why do recession dates carry look-ahead risk?::NBER identifies turning points only in hindsight; the December 2007 start was announced in December 2008 (V9 p.350).
Historical simulation::Randomly draws returns from historical periods without regard to time order; a non-deterministic rolling-window backtest (V9 p.354, p.355).
Bootstrapping::Random sampling with replacement, used when the simulations needed exceed the size of the historical dataset (V9 p.355).
Monte Carlo simulation::Assigns each key variable a statistical distribution calibrated to history and draws observations from it (V9 p.354).
Most important decision in Monte Carlo simulation::The choice of functional form for the statistical distribution of the key decision variables (V9 p.369).
Eight simulation steps in order::Target variable; key decision variables; number of trials; distributional properties; random draws; compute target; repeat to N; analyze the N outcomes (V9 p.354, p.355).
Typical number of simulation trials::Between 1,000 and 10,000; more trials give more stable estimates (V9 p.354).
Inverse transformation method::Converting a randomly generated uniform number into a simulated value of a random variable, e.g. mapping a draw to one of 374 months via slices of width 0.00267 (V9 p.355, p.379).
Model calibration::Estimating distribution parameters (mean, sd, skew, kurtosis, covariances) from historical data via regression and distribution fitting (V9 p.360).
Parameters for a K-asset multivariate normal::{{K means, K standard deviations, and K(K-1)/2 correlations}} (V9 p.360).
Parameter count for 8 factors::8 + 8 + 28 = 44; for 9 factors the correlation count alone is 36 (V9 p.360, p.378).
Why model correlated factors jointly?::Standalone fits destroy the correlation structure; a multivariate distribution preserves it (V9 p.360).
Bias-variance trade-off in choosing a distribution::Complex forms fit well but estimate poorly (estimation error); simple forms estimate well but may be mis-specified (V9 p.360).
What does the multivariate normal miss in factor data?::Negative skewness, excess kurtosis, and tail dependence, so it understates downside risk (V9 p.360, p.363).
Tail dependence::The tendency of extreme returns across assets to occur together; the normal distribution implies none (V9 p.359, p.360).
Sensitivity analysis::Exploring how the target variable responds to changes in input assumptions, e.g. swapping multivariate normal for multivariate skewed t (V9 p.363).
Cost of the multivariate skewed t-distribution::More parameters to estimate, hence larger estimation errors, despite capturing skew and kurtosis (V9 p.369).
Which conclusion survived all four evaluation methods?::RP beats BM on Sharpe ratio under backtesting, historical simulation, and both Monte Carlo variants (V9 p.362, p.365).
Which output was method-sensitive?::CVaR for the BM strategy; both Monte Carlo variants understated its downside risk (V9 p.363, p.364).
Preferred downside metrics for simulations::CVaR and maximum drawdown (V9 p.355).
CVaR definition::The weighted average of all loss outcomes that exceed the VaR loss; a more comprehensive tail measure than VaR (V9 p.376).
30-second check: draw 0.59163 with 374 months selects which month?::0.59163 x 374 = 221.3, round up to Month 222; keystrokes `.59163 x 374 =` then take the next integer (V9 p.356).
30-second check: equal-weight BM return for factor returns summing to 3.7%?::3.7% / 8 = 0.4625%, printed as 0.46% (V9 p.356).

## Common mistakes

1. Backtesting on current index constituents and defending it with "you can only buy companies that exist today" - the survivor list was unknowable in advance and is biased toward winners, so use point-in-time constituents including the delisted casualties (V9 p.341, p.342).
2. Confusing the bias family tree: survivorship bias is a special case of look-ahead bias, and data snooping is neither - it is a model-selection sin, immune to point-in-time data (V9 p.343, p.349).
3. Treating standard deviation as a sufficient risk summary and skipping drawdown, VaR and CVaR; with negative skew and kurtosis above 3.0, symmetric volatility hides the left tail (V9 p.335, p.377).
4. Ranking downside risk on the wrong column: read whether the question defines VaR (minimum loss, 5% of the time) or CVaR (average loss beyond VaR) before ranking factors (V9 p.376).
5. Calling a regime split "sensitivity analysis" or a distribution swap "scenario analysis"; regimes = scenario, assumption changes = sensitivity, and a changed universe is neither (V9 p.367).
6. Claiming Monte Carlo or historical simulation is deterministic, or that either avoids random number generators; only rolling-window backtesting is deterministic (V9 p.368, p.377).
7. Fitting correlated factors standalone, or counting covariance parameters only for the correlated subset; all K factors enter the multivariate calibration with K(K-1)/2 correlations (V9 p.360, p.378).
8. Accepting the best of many backtests at t = 2.5 because it beats 2.0; multiple testing demands a hurdle above 3.0 and cross-validation, otherwise the result is a manufactured false positive (V9 p.346).
9. Adding a generous uniform reporting lag and declaring victory over look-ahead bias while quietly introducing stale data for fast-reporting large caps (V9 p.344, p.377).
10. Assuming a multivariate normal Monte Carlo captures downside risk; it carries zero skew, zero excess kurtosis and zero tail dependence, so it understated the BM strategy's CVaR against every history-based method (V9 p.363).
11. Forgetting that transaction costs kill many anomalies: always ask, and state, whether the backtest includes them (V9 p.324).
12. Reading a linear-scale cumulative wealth chart as acceleration; the module plots on a log scale so equal percentage gains look equal (V9 p.327).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "09-06" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
