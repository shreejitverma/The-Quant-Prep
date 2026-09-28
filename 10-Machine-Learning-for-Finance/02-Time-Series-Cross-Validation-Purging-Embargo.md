---
type: concept
track: [quant-research]
tier: core
status: solid
prereqs: [ml-fundamentals-and-generalization]
est_hours: 3
sources: [Lopez de Prado - Advances in Financial Machine Learning (2018) ch 4 7 12, Bailey Borwein Lopez de Prado and Zhu (2017) - The Probability of Backtest Overfitting - Journal of Computational Finance 20(4), Hastie Tibshirani and Friedman - The Elements of Statistical Learning (2nd ed.) sec 7.10, Arlot and Celisse (2010) - A Survey of Cross-Validation Procedures for Model Selection - Statistics Surveys 4, Hansen and Hodrick (1980) - Forward Exchange Rates as Optimal Predictors of Future Spot Rates - Journal of Political Economy 88(5), Newey and West (1987) - A Simple Positive Semi-Definite Heteroskedasticity and Autocorrelation Consistent Covariance Matrix - Econometrica 55(3)]
---

# Time-Series Cross-Validation: Purging and Embargo

## TL;DR

- Standard shuffled k-fold assumes iid rows; financial rows are serially correlated and their labels overlap in time, so test information leaks into training and CV scores are inflated.
- Give every sample an information interval $[t_0, t_1]$ from feature time to label end; purging removes training samples whose interval overlaps the test set's span, and an embargo also drops training samples that start just after the test span.
- Lopez de Prado's purged k-fold uses contiguous test folds, purges on both sides, and embargoes after the test fold by about $0.01T$.
- Walk-forward (expanding or rolling) with a gap of at least the label horizon is the deployment-faithful scheme, but gives one path; purged k-fold and CPCV use more data and give more paths.
- $h$-day labels sampled daily share up to $(h-1)/h$ of their returns: effective sample size is about $T/h$, naive $t$-stats are inflated by about $\sqrt h$, and uniqueness weights correct the training loss.

## Learning objectives

- Explain leakage from overlapping labels and serial correlation.
- Implement purged k-fold with embargo and walk-forward splits.

## Core concepts

### Why shuffled k-fold leaks

K-fold cross-validation estimates generalisation error by fitting on $k-1$ folds and scoring on the held-out one, which is unbiased only if the held-out rows are independent of the training rows.
In finance two mechanisms break this:

- Overlapping labels: a label such as the 20-day forward return at $t$ shares 19 daily returns with the label at $t+1$, so a training row next to a test row nearly contains the test answer.
- Serially correlated features: persistent features (valuations, slow moving averages, regimes) make time-adjacent rows near neighbours in feature space, so a flexible model can look up the adjacent training label.

Together they let a model with no real skill score well: it memorises "what happened around this date", which is unavailable in live trading.
Hyperparameter search then selects the model that exploits the leak best.

### Information intervals

For sample $i$ let $t_{0,i}$ be the time the features are observed (the decision time) and $t_{1,i}$ the time the label is resolved: $t_0 + h$ for a fixed horizon, or the first barrier touch for triple-barrier labels ([Labeling](06-Labeling-Triple-Barrier-and-Meta-Labeling.md)).
Sample $i$ depends on market data over $[t_{0,i}, t_{1,i}]$ (and on the past for its features).
For a test fold, its span is $[\min_{i\in\text{test}} t_{0,i},\ \max_{i\in\text{test}} t_{1,i}]$.

### Purging

Remove from the training set every sample $j$ whose interval intersects the test span:

$$
t_{0,j} \le \max_{\text{test}} t_1 \quad\text{and}\quad t_{1,j} \ge \min_{\text{test}} t_0.
$$

This drops training samples just before the test fold whose labels resolve inside it, and samples just after it whose features are observed while test labels are still unresolved.
With fixed horizon $h$ and one sample per bar, purging removes about $h$ samples on each side of an interior fold.

### Embargo

Features are often serially correlated beyond the label horizon (for instance a 60-day moving average), so training samples soon after the test fold still carry information about it.
The embargo drops training samples with $t_{0,j} \in (\max_{\text{test}} t_1,\ \max_{\text{test}} t_1 + e]$.
Lopez de Prado applies it only after the test fold, because training rows before the test fold cannot see test-period information through backward-looking features, and suggests $e \approx 0.01T$ as a default; make it at least the longest feature lookback that could straddle the boundary.

### Walk-forward

- Expanding window: train on $[0, s)$, test on $[s + g, s + g + m)$, move $s$ forward by $m$.
- Rolling window: train on the most recent $W$ periods only, which adapts to nonstationarity at the cost of variance.
- The gap $g$ must be at least the label horizon so the last training labels resolve before the first test decision.
- Walk-forward mirrors live deployment, and is the right final check, but tests each period only once, uses little data early on, and gives a single path that is easy to overfit by repeated tweaking.

Purged k-fold tests every period with a model trained on the rest (including the future), which is fine for estimating the skill of a stationary relationship but is not a simulation of history.
CPCV generalises it to many test-group combinations and yields $\binom{N-1}{k-1}$ full backtest paths ([Overfitting and Deflated Sharpe](../09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md)).

### Overlapping labels in estimation and training

If daily returns are iid with variance $\sigma^2$, the $h$-day overlapping label $y_t = \sum_{j=1}^h r_{t+j}$ has lag-$k$ autocorrelation $(h-k)/h$ for $k < h$.
The long-run variance of $\bar y$ is about $h$ times the naive one, so naive standard errors are too small by $\sqrt h$; use Hansen-Hodrick or Newey-West with at least $h-1$ lags, or subsample non-overlapping labels.
In training, Lopez de Prado's uniqueness weights down-weight crowded samples: with concurrency $c_t$ = number of labels whose interval contains bar $t$, the uniqueness of sample $i$ is the average of $1/c_t$ over its interval, and the average uniqueness estimates how many effectively independent labels there are.
Sequential bootstrap and bagging with `max_samples` set to average uniqueness use the same idea.

### Other leakage to rule out

- Look-ahead in features: using close prices for a decision made at the close, restated fundamentals, index membership as of today ([Point-in-Time Data and Survivorship](../09-Alpha-Research-and-Portfolio/02-Point-in-Time-Data-and-Survivorship.md)).
- Preprocessing fit on the full sample: scalers, PCA, feature selection, target encoding.
- Cross-sectional leakage: the same date appears in train and test for different assets while labels share a market-wide component; split by date, not by row.
- Hyperparameters tuned on the test folds; keep a final untouched period.

## Worked examples

### 1. Counting purged and embargoed samples

$T = 1000$ daily samples, label horizon $h = 5$ ($t_1 = t_0 + 5$), five contiguous folds of 200, embargo $e = 0.01T = 10$ days.
Test fold 2 is samples 200 to 399; its span is $[200, 404]$.

- Purged before: samples 195 to 199, whose labels end at 200 to 204, inside the span: 5 samples.
- Purged after: samples 400 to 404, observed while test labels are unresolved: 5 samples.
- Embargoed: samples 405 to 414: 10 samples.
- Training set: $800 - 20 = 780$ samples; the first fold trains on 785 (nothing before it) and the last on 795 (nothing after it).

The loss of data is small, $2h + e$ per interior fold, which is why purging should always be on.

### 2. The leak in action

```python
import numpy as np

def purged_kfold(t0, t1, n_splits=5, embargo=0):
    """Yield (train, test) index arrays for contiguous folds.
    Sample i uses information over [t0[i], t1[i]] (feature time to label end); arrays sorted by t0.
    Train samples whose interval overlaps the test span [min t0, max t1] are purged, and
    train samples starting within `embargo` time units after the test span are dropped."""
    idx = np.arange(len(t0))
    for test in np.array_split(idx, n_splits):
        lo, hi = t0[test].min(), t1[test].max()
        overlap = (t0 <= hi) & (t1 >= lo)                 # label interval touches the test span
        embargoed = (t0 > hi) & (t0 <= hi + embargo)
        yield idx[~overlap & ~embargoed], test

def shuffled_kfold(n, n_splits=5, seed=0):
    perm = np.random.default_rng(seed).permutation(n)
    for test in np.array_split(perm, n_splits):
        yield np.setdiff1d(perm, test), test

def knn_predict(x_train, y_train, x_test, k=10):
    d = np.abs(x_test[:, None] - x_train[None, :])
    return y_train[np.argsort(d, axis=1)[:, :k]].mean(axis=1)

def cv_ic(x, y, splits):
    pred, true = [], []
    for tr, te in splits:
        pred.append(knn_predict(x[tr], y[tr], x[te]))
        true.append(y[te])
    return np.corrcoef(np.concatenate(pred), np.concatenate(true))[0, 1]

rng = np.random.default_rng(0)
T, h = 2000, 20
r = rng.standard_normal(T + h)                            # iid returns: nothing is predictable
y = np.array([r[t + 1 : t + 1 + h].sum() for t in range(T)])   # 20-day forward return label
x = np.zeros(T)
for t in range(1, T):
    x[t] = 0.99 * x[t - 1] + rng.standard_normal()        # persistent pure-noise feature
t0, t1 = np.arange(T), np.arange(T) + h

print("shuffled k-fold IC:", round(cv_ic(x, y, shuffled_kfold(T)), 3))                    # 0.139
print("contiguous k-fold IC:", round(cv_ic(x, y, purged_kfold(t0, t0, embargo=0)), 3))    # -0.093
print("purged + embargo IC:", round(cv_ic(x, y, purged_kfold(t0, t1, embargo=20)), 3))    # -0.059
```

Returns are iid, so the true IC is zero.
Over 100 simulated datasets, shuffled k-fold reported a mean IC of 0.12 and was positive in 98 of them; purged k-fold with embargo averaged $-0.02$ with a standard deviation of 0.08 across datasets.
The nearest neighbours of a test row in feature space are its neighbours in time, whose 20-day labels share most of its returns.
Here plain contiguous folds are already close to purged ones, because only the fold edges leak; the gap widens with longer horizons, more folds and models that can isolate those edge samples.
The 0.08 spread of honest ICs is itself a lesson: with a persistent feature and 2000 rows, the effective sample is small.

### 3. Standard errors with overlapping labels

Ten years of daily data ($T = 2520$) with 21-day forward-return labels.

- Non-overlapping labels available: $2520/21 = 120$.
- Adjacent labels share $20/21$ of their returns; labels 5 days apart share $16/21 = 76\%$.
- The variance of the mean of overlapping labels is about $h = 21$ times the naive iid formula, so naive $t$-stats are inflated by $\sqrt{21} = 4.6$.
- A reported $t = 6$ from an OLS regression on overlapping monthly returns is roughly $t = 1.3$ after the correction.

### 4. Uniqueness weights

Three labels on five bars: A spans bars 1 to 3, B spans 2 to 4, C spans 4 to 5.
Concurrency: bar 1: 1, bar 2: 2, bar 3: 2, bar 4: 2, bar 5: 1.

- Uniqueness of A: $(1 + \tfrac12 + \tfrac12)/3 = 2/3$.
- B: $(\tfrac12+\tfrac12+\tfrac12)/3 = 1/2$.
- C: $(\tfrac12 + 1)/2 = 3/4$.

Average uniqueness $0.64$, so the three labels carry roughly the information of 1.9 independent ones.
In steady state with fixed horizon $h$ and one label per bar, every label has uniqueness $1/h$.

### 5. A walk-forward schedule

Ten years of daily data, 21-day labels, rolling three-year training window, six-month test windows.

- Test windows start at years 3.0, 3.5, ..., 9.5: 14 windows covering 7 years out of sample.
- Each training window ends 21 trading days before its test window starts, so no training label resolves inside the test period.
- Hyperparameters are chosen inside each training window by purged k-fold, never on the test windows.
- The stitched 7-year out-of-sample path is one realisation; report it with the DSR and, if possible, CPCV paths for dispersion.

## Pitfalls

- Using scikit-learn's `KFold(shuffle=True)` or `train_test_split` on time-indexed data.
- Using `TimeSeriesSplit` without a gap, so the last training labels resolve inside the test window.
- Purging by row index when samples are irregular in time (event-based bars); purge by timestamps $t_0$, $t_1$.
- Embargoing too little when features have long lookbacks, or confusing the embargo with the purge.
- Splitting a panel by row so the same date sits in train and test across assets.
- Reporting OLS $t$-stats on overlapping labels without HAC or Hansen-Hodrick errors.
- Tuning hyperparameters on the walk-forward test periods, which turns them into training data.
- Treating purged k-fold as a backtest: it uses future data to train models evaluated on the past, which is fine for skill estimation but not for PnL simulation.

## Interview questions

> [!question]- ml-cv-why-kfold-fails | Why is shuffled k-fold cross-validation invalid for most financial ML problems?
> Rows are not iid: labels overlap in time and features are serially correlated, so training rows near a test row leak its answer.
> The CV score is inflated and hyperparameter search selects models that exploit the leak.

> [!question]- ml-cv-purging-definition | What is purging in cross-validation?
> Removing training samples whose information interval $[t_0, t_1]$ overlaps the test fold's span.
> Formally drop $j$ with $t_{0,j} \le \max_{\text{test}}t_1$ and $t_{1,j} \ge \min_{\text{test}} t_0$; this removes about $h$ samples on each side for horizon-$h$ labels.

> [!question]- ml-cv-embargo-definition | What is the embargo, where is it applied, and how large is it?
> Dropping training samples that start within a period $e$ after the test fold's span, to cut leakage through serially correlated features.
> Lopez de Prado applies it after the test fold only and suggests $e \approx 0.01T$; it should cover the longest feature lookback.

> [!question]- ml-cv-purge-count | 1000 daily samples, 5-day labels, 5 contiguous folds, embargo 10. How many training samples for an interior fold?
> 780.
> $800$ non-test samples minus 5 purged before, 5 purged after and 10 embargoed.

> [!question]- ml-cv-overlap-correlation | Daily-sampled 20-day forward returns from iid daily returns: what is the correlation between labels 5 days apart?
> $15/20 = 0.75$.
> They share 15 of 20 daily returns; in general $\rho_k = (h-k)/h$ for $k < h$.

> [!question]- ml-cv-overlap-tstat | You regress overlapping 21-day returns sampled daily and get $t = 6$ with OLS errors. Roughly what is the honest $t$?
> About $6/\sqrt{21} \approx 1.3$.
> Overlap inflates the long-run variance by about $h$; use Hansen-Hodrick or Newey-West with at least $h-1$ lags.

> [!question]- ml-cv-uniqueness | Define average uniqueness of a label.
> The mean of $1/c_t$ over the bars in the label's interval, where $c_t$ counts labels active at bar $t$.
> It down-weights crowded samples in the loss and sets the sampling rate for sequential bootstrap and bagging.

> [!question]- ml-cv-walk-forward-gap | In walk-forward validation with 21-day labels, what gap do you need between training and test windows?
> At least 21 trading days, the label horizon.
> Otherwise the last training labels are resolved with returns from inside the test window.

> [!question]- ml-cv-walk-forward-vs-purged | Walk-forward or purged k-fold: when do you use which?
> Purged k-fold (or CPCV) for model selection and skill estimation with more data; walk-forward as the final deployment-faithful check.
> Walk-forward gives a single path that is easy to overfit by iteration; purged k-fold trains on future data so it is not a historical simulation.

> [!question]- ml-cv-knn-leak | A kNN model on a slow-moving noise feature scores IC 0.12 in shuffled 5-fold CV on 20-day labels. Explain.
> Leakage: feature neighbours are time neighbours, whose overlapping labels contain most of the test label.
> With purged k-fold and an embargo the IC falls to about zero, the true value for iid returns.

> [!question]- ml-cv-panel-split | In a cross-sectional stock model, why split folds by date rather than by row?
> Returns on the same date share a common market component, so a row from date $t$ in training leaks the test rows on date $t$.
> Split by date blocks and purge by the label intervals of those dates.

> [!question]- ml-cv-irregular-bars | Your samples are event-driven bars with variable label lengths. How do you purge?
> By timestamps: store $t_0$ and $t_1$ for each sample and purge on interval overlap, not on row counts.
> Row-count purging assumes one sample per unit of time and a fixed horizon.

## Further reading

- Marcos Lopez de Prado, *Advances in Financial Machine Learning*, chapters 4 (sample weights), 7 (cross-validation in finance) and 12 (CPCV).
- Bailey, Borwein, Lopez de Prado and Zhu (2017), The Probability of Backtest Overfitting, Journal of Computational Finance.
- Hastie, Tibshirani and Friedman, *The Elements of Statistical Learning*, section 7.10.
- Arlot and Celisse (2010), A Survey of Cross-Validation Procedures for Model Selection, Statistics Surveys.
- Hansen and Hodrick (1980), Journal of Political Economy, and Newey and West (1987), Econometrica, for standard errors with overlapping observations.
