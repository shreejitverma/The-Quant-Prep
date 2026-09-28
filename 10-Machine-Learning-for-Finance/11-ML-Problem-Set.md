---
type: problem-set
track: [quant-research]
tier: core
status: solid
prereqs: [time-series-cross-validation-purging-embargo, tree-ensembles-and-gradient-boosting]
est_hours: 5
sources: [Lopez de Prado (2018) Advances in Financial Machine Learning. Wiley, Hastie Tibshirani and Friedman (2009) The Elements of Statistical Learning 2nd ed. Springer, Bailey and Lopez de Prado (2014) The deflated Sharpe ratio. Journal of Portfolio Management 40(5), Bailey Borwein Lopez de Prado and Zhu (2017) The probability of backtest overfitting. Journal of Computational Finance 20(4), Gu Kelly and Xiu (2020) Empirical asset pricing via machine learning. Review of Financial Studies 33(5), Grinold and Kahn (2000) Active Portfolio Management 2nd ed. McGraw-Hill, Strobl Boulesteix Zeileis and Hothorn (2007) Bias in random forest variable importance measures. BMC Bioinformatics 8(25)]
---

# ML Problem Set

## TL;DR

- Start every ML-for-finance answer with the prediction contract: target, horizon, decision time and the information available at that time; most bugs are violations of it.
- Leakage is the default failure: look-ahead features, overlapping labels across the train-test boundary, and preprocessing or tuning on data that includes the test period.
- Validate forward in time: walk-forward or purged k-fold with an embargo, and keep a final untouched holdout.
- At daily-return signal-to-noise levels, complexity costs more than it buys: 50 useless features in OLS on 10 years of daily data turn a true $R^2$ of 0.5% into an expected out-of-sample $R^2$ of about $-1.5\%$.
- Count your trials: the best of many backtests is biased upward, so deflate it (deflated Sharpe, probability of backtest overfitting) and report how many things you tried.

## Learning objectives

- Answer ML-for-finance interview questions on leakage, validation and model choice.

## Core concepts

### A framework for answering

Interviewers ask these questions to see whether you can find the flaw before it costs money.
Answer in this order:

1. Prediction contract: what is predicted, over what horizon, at what timestamp, using which data as it was known then (point-in-time; see [Point-in-Time Data and Survivorship](../09-Alpha-Research-and-Portfolio/02-Point-in-Time-Data-and-Survivorship.md)).
2. Leakage audit: features, labels, preprocessing, universe, and every choice made after looking at test results.
3. Validation design: forward-in-time splits, purging and embargo for overlapping labels (see [Time-Series Cross-Validation: Purging and Embargo](02-Time-Series-Cross-Validation-Purging-Embargo.md)).
4. Model choice given signal-to-noise, sample size, non-stationarity, latency and interpretability.
5. Overfitting control: regularisation, a naive baseline, and a count of trials.
6. Economic evaluation: IC, turnover, costs and capacity, not just a statistical metric (see [Performance Metrics and the Fundamental Law](../09-Alpha-Research-and-Portfolio/09-Performance-Metrics-and-Fundamental-Law.md)).

### Leakage taxonomy

- Feature look-ahead: using a value before it was published (restated fundamentals, vendor backfill, close prices for a decision made before the close, timestamps in the wrong time zone).
- Universe look-ahead: today's index members or surviving stocks applied to the past (survivorship bias).
- Label overlap: a training label whose window overlaps the test period shares information with test labels; purge it.
- Serial correlation: features and labels right after the test block are correlated with it; embargo them.
- Preprocessing leakage: scaling, winsorising, PCA or feature selection fitted on the full sample.
- Selection leakage: any hyperparameter, feature or model chosen by looking at the test set, including "I tried it and it did not work, so I changed it".

### Validation in brief

Walk-forward (expanding or rolling window) mimics live trading but gives one path and uses early data only for training.
Purged k-fold uses all data for testing: drop training samples whose label windows overlap the test fold (purge) and a buffer after it (embargo).
Combinatorial purged CV with $N$ groups and $k$ test groups gives $\binom{N}{k}$ splits and $\frac{k}{N}\binom{N}{k}$ backtest paths, which yields a distribution of performance rather than one number.
Tuning needs a nested scheme: an inner split for hyperparameters inside each outer training set.

### Model choice

Low signal-to-noise and modest effective sample sizes favour simple, heavily regularised models: ridge or elastic net on well-designed features, shallow boosted trees with early stopping, or small ensembles of both.
Deep nets pay off with large cross-sections, rich raw inputs (order books, text) or strong nonlinearity, and still need aggressive regularisation.
Non-stationarity favours models that retrain cheaply and degrade gracefully (see [Online Learning and Linear Models at Scale](04-Online-Learning-and-Linear-Models-at-Scale.md)).
See [Tree Ensembles and Gradient Boosting](03-Tree-Ensembles-and-Gradient-Boosting.md) for tree-specific overfitting.

## Worked examples

### Example 1: out-of-sample R-squared with useless features

OLS with $p = 50$ standardised features on $n = 2{,}520$ daily observations (10 years), where one feature carries a true $R^2$ of 0.5% and 49 are noise.
In-sample $R^2$ is about $0.005 + p/n \approx 0.025$: five times the truth.
For Gaussian features the expected out-of-sample $R^2$ is about

$$
R^2_{\text{true}} - (1 - R^2_{\text{true}})\frac{p}{n - p - 1} = 0.005 - 0.995 \times \frac{50}{2469} \approx -0.015.
$$

A simulation with 200 repetitions gives in-sample 0.024 and out-of-sample $-0.0152$.
The estimation noise in 50 coefficients costs three times the signal: worse than predicting zero.
Remedies: fewer features chosen on prior grounds, ridge shrinkage, or a larger cross-section.

### Example 2: overlapping labels inflate t-statistics

You regress 20-day forward returns, sampled daily over 1,000 days, on a signal.
Adjacent labels share 19 of 20 daily returns, so the effective number of independent observations is about $1000/20 = 50$.
For i.i.d. daily returns, the autocorrelations of the overlapping sums are $(h - k)/h$ at lag $k$, which sum to a variance inflation of $h = 20$, so naive standard errors are too small by $\sqrt{20} \approx 4.5$.
A null signal then produces naive t-statistics with a standard deviation of about 4.5 instead of 1 (a simulation gives 4.57): a naive $t = 3$ means nothing.
Use Newey-West or Hansen-Hodrick standard errors, non-overlapping samples, or sample weights by label uniqueness.

### Example 3: purging and embargo in a concrete split

Daily data indexed 0 to 2,499, labels at day $t$ use returns from $t+1$ to $t+5$, and the test fold is days 500 to 599.
Purge: training samples before the fold whose label windows reach day 500 or later, $t + 5 \ge 500$, so days 495 to 499.
After the fold, the label at day 599 uses returns through day 604, so training samples at days 600 to 603 (whose windows start at $t + 1 \le 604$) overlap it; purge them as well.
Embargo: with a 1% embargo (25 days), also drop days 604 to 628 to cover serial correlation in features.
The training set is days 0 to 494 and 629 onward.

### Example 4: many features, one winner

You test 200 candidate features, all with zero true predictive power, each at the 5% level.
You expect 10 false discoveries, and the probability of at least one is $1 - 0.95^{200} \approx 1$.
The largest absolute t-statistic among 200 independent nulls is about 2.97 on average.
Bonferroni at a 5% family-wise level needs $|t| > 3.66$ (two-sided $p < 0.00025$).
The same logic applies to strategies: report the number of trials and use the deflated Sharpe ratio (see [Overfitting and the Deflated Sharpe Ratio](../09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md)).

### Example 5: ridge as a prior

One standardised feature with $\sum x_i^2 = n = 1{,}000$ and $\sum x_i y_i = 30$, so $\hat\beta_{\text{OLS}} = 0.03$, with residual variance 1.
Ridge gives $\hat\beta = \sum x_i y_i / (\sum x_i^2 + \lambda)$.
Ridge is the posterior mean under a prior $\beta \sim N(0, \tau^2)$ with $\lambda = \sigma^2/\tau^2$.
If you believe true coefficients are about $\tau = 0.02$, then $\lambda = 1/0.0004 = 2{,}500$ and the shrinkage factor is $1000/3500 \approx 0.29$: $\hat\beta \approx 0.0086$.
Heavy shrinkage is correct when the prior says effects are tiny, which in return prediction they are.

### Example 6: is 54% accuracy good?

A daily direction classifier scores 54% accuracy on 1,000 test days, and 53% of those days were up.
Always predicting "up" scores 53%, so the lift is 1 point, with standard error $\sqrt{0.53 \times 0.47/1000} \approx 0.016$: $z \approx 0.63$, not significant.
Accuracy also ignores magnitudes: a model that is right on small days and wrong on large ones loses money.
Evaluate the information coefficient, the P&L of the implied positions after costs, and compare to the naive baseline.

### Example 7: from IC to information ratio

A cross-sectional signal has an information coefficient of 0.02 and supports about 500 independent bets a year.
The fundamental law gives $\text{IR} \approx \text{IC}\sqrt{\text{breadth}} = 0.02\sqrt{500} \approx 0.45$ before costs.
If the 500 bets are really 50 independent ones because positions are correlated or overlapping, IR falls to about 0.14.
An IC that looks negligible can be valuable with enough genuine breadth, and a high backtest IR can be an artefact of overstated breadth.

## Pitfalls

- Random K-fold cross-validation on time series with overlapping labels.
- Fitting scalers, PCA or feature selection on the full sample before splitting.
- Using a universe that is known only today (survivorship) or data as later revised.
- Reporting the best of many configurations without the number tried.
- Judging a classifier by accuracy against 50% instead of against the majority class, and ignoring magnitudes and costs.
- Trusting in-sample feature importance, or permutation importance with highly correlated features.
- Tuning hyperparameters on the same fold used to report performance.
- Assuming a model that worked in one regime keeps working; monitor for decay (see [ML Production and Monitoring](10-ML-Production-and-Monitoring.md)).

## Interview questions

### Leakage

> [!question]- ml-pset-scaler-leak | You standardise features using the mean and standard deviation of the whole data set, then split into train and test. What is wrong?
> The test-period statistics leak into training features, so the model sees information from the future.
> Fit every preprocessing step (scaling, winsorising, PCA, feature selection) on the training window only, and apply it forward.

> [!question]- ml-pset-close-price-leak | A model predicts the open-to-close return using features that include the day's closing volume. Is that valid?
> No: closing volume is not known at the open, so the feature is look-ahead.
> Every feature needs a timestamp no later than the decision time.

> [!question]- ml-pset-survivorship | You backtest on the current members of an index over 20 years. What bias does that introduce?
> Survivorship bias: you exclude firms that were delisted, went bankrupt or were dropped, which inflates returns and hides crash risk.
> Use point-in-time constituents and include delisting returns.

> [!question]- ml-pset-restated-data | Why do fundamentals from a standard database cause leakage?
> Values are often restated or backfilled, so the number in the database differs from what was known on the announcement date.
> Use point-in-time data with the publication timestamp, and lag it to when you could have traded on it.

> [!question]- ml-pset-selection-leak | You tried 30 feature sets, kept the one with the best test score and reported that score. What is the problem?
> The test set was used for model selection, so its score is optimistically biased.
> Choose on a validation set or nested CV and report once on an untouched holdout, together with the number of trials.

> [!question]- ml-pset-label-overlap-boundary | How can labels leak across the train-test boundary even with a chronological split?
> A training label whose forward-return window extends into the test period shares returns with test labels.
> Purge training samples whose label windows overlap the test period.

### Validation

> [!question]- ml-pset-kfold-timeseries | Why is standard shuffled K-fold wrong for financial time series?
> It trains on the future and on neighbours of test points that share overlapping labels and serially correlated features, so scores are optimistic.
> Use walk-forward or purged k-fold with an embargo.

> [!question]- ml-pset-purge-vs-embargo | What is the difference between purging and embargo?
> Purging drops training samples whose label windows overlap the test labels; embargo also drops a buffer of samples after the test block to cover serial correlation.
> Purging addresses label overlap, embargo addresses leakage through correlated features.

> [!question]- ml-pset-purge-count | Labels at day t use returns t+1 to t+5 and the test fold is days 500 to 599. Which earlier training days must be purged?
> Days 495 to 499.
> Their label windows ($t+5 \ge 500$) reach into the test period.

> [!question]- ml-pset-walk-forward-tradeoff | What does walk-forward validation give up compared with purged k-fold?
> It produces a single path and tests only on later data, so it uses less data for testing and its result depends heavily on one sequence of regimes.
> In exchange it exactly mimics live deployment; purged k-fold or CPCV uses all data for testing and gives a distribution of outcomes.

> [!question]- ml-pset-cpcv-paths | With combinatorial purged CV on 6 groups and 2 test groups, how many splits and backtest paths are there?
> 15 splits and 5 paths.
> $\binom62 = 15$ splits, and each group is tested $\frac{k}{N}\binom{N}{k} = \frac26 \times 15 = 5$ times.

> [!question]- ml-pset-nested-cv | How do you tune hyperparameters without biasing the performance estimate?
> Nested validation: tune on inner splits within each outer training window and evaluate the chosen model on the outer test fold.
> Keep a final holdout that no decision has touched.

### Model choice

> [!question]- ml-pset-linear-vs-trees | When would you prefer a regularised linear model over gradient boosting for return prediction?
> When the signal is weak, the effective sample is small, or the relationships are close to monotone; linear models have far lower variance and are easier to monitor.
> Boosting pays off with larger samples and genuine interactions or nonlinearities, and even then needs shallow trees and early stopping.

> [!question]- ml-pset-deep-learning-case | When do neural networks earn their complexity in trading?
> With large data and rich raw inputs where feature engineering is hard: order-book sequences, text, or very large cross-sections.
> On a few hundred engineered daily features over a decade, they rarely beat ridge or shallow boosting out of sample.

> [!question]- ml-pset-classification-vs-regression | Should you predict the sign of returns or their size?
> Usually size, or a probability with a sizing rule, because P&L depends on magnitudes; a sign classifier treats a 0.01% day and a 5% day alike.
> If you classify, weight samples by absolute return or use meta-labeling to size.

> [!question]- ml-pset-nonstationarity-choice | How does non-stationarity affect model choice?
> Favour models that retrain cheaply, weight recent data (rolling windows or decay) and degrade gracefully.
> A complex model fitted to one regime can fail sharply in the next; monitor live performance for decay.

> [!question]- ml-pset-baseline | What baseline should every return model beat?
> The naive forecast: zero (or the historical mean) for returns, the majority class for direction, and a simple linear model on the same features.
> Out-of-sample $R^2$ should be measured against the zero forecast, since the historical mean is itself noisy.

### Overfitting and multiple testing

> [!question]- ml-pset-oos-r2-negative | OLS with 50 features, 2,520 observations and a true R-squared of 0.5%: what out-of-sample R-squared do you expect?
> About $-1.5\%$.
> $R^2_{\text{true}} - (1 - R^2_{\text{true}})\,p/(n-p-1) = 0.005 - 0.995 \times 50/2469$; estimation noise in the coefficients outweighs the signal.

> [!question]- ml-pset-insample-r2 | In the same set-up, what in-sample R-squared do you expect?
> About 2.5%.
> Pure noise features add roughly $p/n = 50/2520 \approx 2\%$ to in-sample $R^2$.

> [!question]- ml-pset-false-discoveries | You test 200 useless features at the 5% level. How many look significant?
> About 10, and at least one almost surely ($1 - 0.95^{200} \approx 1$).
> The largest $|t|$ among 200 nulls averages about 3.0; Bonferroni needs $|t| > 3.66$.

> [!question]- ml-pset-deflated-sharpe | What does the deflated Sharpe ratio correct for?
> Selection bias from many trials, plus non-normal returns and short samples.
> It compares the observed Sharpe with the expected maximum Sharpe of that many unskilled trials rather than with zero.

> [!question]- ml-pset-overlap-tstat | You regress overlapping 20-day returns sampled daily. By how much are naive standard errors wrong?
> Too small by about $\sqrt{20} \approx 4.5$.
> Overlapping sums of i.i.d. returns have variance inflation equal to the overlap $h$; use Newey-West or Hansen-Hodrick errors or non-overlapping samples.

> [!question]- ml-pset-backtest-too-good | A new ML strategy backtests at Sharpe 4 on daily data. What do you check first?
> Leakage: timestamps and point-in-time data, preprocessing fitted on the full sample, label overlap with the test set, and survivorship.
> Then the number of trials, costs and capacity; implausibly high Sharpe at daily frequency is usually a bug.

### Feature importance

> [!question]- ml-pset-mdi-vs-mda | Compare MDI and permutation (MDA) importance.
> MDI sums in-sample impurity decreases from the trees and is biased toward high-cardinality features; MDA measures the drop in out-of-sample score when a feature is shuffled.
> Prefer MDA on purged out-of-sample folds.

> [!question]- ml-pset-correlated-importance | Two features are almost identical. What happens to their permutation importance?
> Both can look unimportant, because shuffling one leaves the other to carry the same information (substitution effect).
> Group correlated features into clusters and permute each cluster together, or report single-feature importance as well.

> [!question]- ml-pset-importance-causal | Does a high feature importance mean the feature causes returns?
> No: importance describes what the fitted model relies on, which can reflect a proxy, a leak or noise.
> A feature that is suddenly the most important is a prompt to check it for look-ahead.

> [!question]- ml-pset-shap | What does SHAP add over permutation importance?
> Per-prediction attributions that sum to the model output minus a baseline, so you can see why a given prediction was made and how effects vary.
> It explains the model, not the data-generating process, and it inherits the model's reliance on correlated features.

### Regularisation

> [!question]- ml-pset-ridge-vs-lasso | When do you prefer ridge to lasso?
> When many features carry small effects or features are correlated: ridge shrinks them together, while lasso picks one of a correlated group arbitrarily and unstably.
> Lasso suits genuinely sparse problems; elastic net blends the two.

> [!question]- ml-pset-ridge-prior | What prior does ridge regression correspond to, and what does it imply for lambda?
> A Gaussian prior $\beta \sim N(0, \tau^2)$, with $\lambda = \sigma^2/\tau^2$.
> Tiny expected effects (small $\tau$) relative to noise justify very large $\lambda$; lasso corresponds to a Laplace prior.

> [!question]- ml-pset-ridge-shrink | One standardised feature, n = 1,000, OLS beta 0.03, noise variance 1, prior sd of beta 0.02. What is the ridge estimate?
> About 0.0086.
> $\lambda = 1/0.02^2 = 2500$, shrinkage $1000/(1000 + 2500) \approx 0.29$, so $0.03 \times 0.29$.

> [!question]- ml-pset-early-stopping | Why is early stopping a form of regularisation, and how should you set it up in finance?
> Stopping before convergence limits how far the model moves from its simple starting point, much like a norm penalty.
> Use a validation block later in time than training, with purging and embargo at the boundary.

### Low signal-to-noise and evaluation

> [!question]- ml-pset-accuracy-baseline | Your classifier has 54% accuracy on 1,000 days, 53% of which were up. Is it useful?
> Not demonstrably: the lift over always predicting "up" is 1 point with standard error about 1.6 points ($z \approx 0.6$).
> Also check whether it is right on the large-move days that drive P&L.

> [!question]- ml-pset-ic-to-ir | An IC of 0.02 with 500 independent bets a year gives what information ratio?
> About 0.45 before costs.
> $\text{IR} \approx \text{IC}\sqrt{\text{breadth}} = 0.02\sqrt{500}$; if the bets are really 50 independent ones, IR falls to about 0.14.

> [!question]- ml-pset-ic-significance | A signal has IC 0.05 over 1,000 independent days. Is it significant?
> Borderline: $t \approx 0.05\sqrt{1000} \approx 1.58$, below 1.96.
> The standard error of a correlation near zero is about $1/\sqrt{n}$.

> [!question]- ml-pset-low-snr-implications | What does a very low signal-to-noise ratio imply for model building?
> Effective sample sizes are small relative to model capacity, so variance dominates: prefer simple, strongly regularised models, economically motivated features and large cross-sections.
> Expect out-of-sample $R^2$ well under 1% for daily returns and judge models by IC and cost-adjusted P&L.

> [!question]- ml-pset-cost-aware | Why can a model with a higher IC be worse to trade?
> If its forecasts change faster, turnover and costs can consume the extra edge.
> Evaluate net-of-cost P&L and capacity, or penalise turnover when fitting.

## Further reading

- Marcos Lopez de Prado, *Advances in Financial Machine Learning* (2018), chapters 4, 7, 8, 11 and 12.
- Hastie, Tibshirani and Friedman, *The Elements of Statistical Learning* (2nd ed., 2009), chapters 3 and 7.
- Bailey and Lopez de Prado (2014), The deflated Sharpe ratio, *Journal of Portfolio Management* 40(5).
- Bailey, Borwein, Lopez de Prado and Zhu (2017), The probability of backtest overfitting, *Journal of Computational Finance* 20(4).
- Gu, Kelly and Xiu (2020), Empirical asset pricing via machine learning, *Review of Financial Studies* 33(5).
- Grinold and Kahn, *Active Portfolio Management* (2nd ed., 2000).
- Strobl, Boulesteix, Zeileis and Hothorn (2007), Bias in random forest variable importance measures, *BMC Bioinformatics* 8.
