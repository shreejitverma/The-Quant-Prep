---
type: concept
track: [quant-research]
tier: core
status: solid
prereqs: [ml-fundamentals-and-generalization]
est_hours: 4
sources: [Hastie Tibshirani and Friedman (2009) The Elements of Statistical Learning 2nd ed. Springer, Breiman (1996) Bagging predictors. Machine Learning 24(2) 123-140, Breiman (2001) Random forests. Machine Learning 45(1) 5-32, Friedman (2001) Greedy function approximation: a gradient boosting machine. Annals of Statistics 29(5) 1189-1232, Friedman (2002) Stochastic gradient boosting. Computational Statistics and Data Analysis 38(4), Chen and Guestrin (2016) XGBoost: a scalable tree boosting system. KDD, Ke et al. (2017) LightGBM: a highly efficient gradient boosting decision tree. NeurIPS, Lopez de Prado (2018) Advances in Financial Machine Learning. Wiley, Strobl Boulesteix Zeileis and Hothorn (2007) Bias in random forest variable importance measures. BMC Bioinformatics 8(25)]
---

# Tree Ensembles and Gradient Boosting

## TL;DR

- A single deep tree has low bias and high variance; bagging and random forests average many decorrelated trees to cut variance, and boosting adds many shallow trees sequentially to cut bias.
- The variance of an average of $B$ trees with pairwise correlation $\rho$ is $\rho\sigma^2 + (1-\rho)\sigma^2/B$, so beyond a few hundred trees only lowering $\rho$ (random feature subsets) helps.
- Gradient boosting fits each new tree to the negative gradient of the loss; XGBoost uses second-order information, giving leaf weight $-G/(H+\lambda)$.
- On low signal-to-noise financial data, default boosted trees overfit badly: in a simulation with true $R^2$ of 1%, a depth-6, 500-tree model had in-sample $R^2$ of 0.90 and out-of-sample $-0.13$.
- Regularise hard (shallow trees, large leaves, small learning rate with early stopping on a time-ordered validation set), and do not trust out-of-bag scores when labels overlap in time.

## Learning objectives

- Explain bagging, random forests and gradient boosting and their hyperparameters.
- Diagnose overfitting in boosted models on financial data.

## Core concepts

### Decision trees

A regression or classification tree recursively splits the feature space on one feature at a time, choosing the split that most reduces impurity:

- squared error for regression, with each leaf predicting the mean of its targets;
- Gini impurity $1 - \sum_k p_k^2$ or entropy $-\sum_k p_k\log p_k$ for classification.

Trees are invariant to monotone transformations of features, need no scaling, handle interactions and missing values naturally, and are cheap to evaluate.
Their weakness is instability: a small change in the data changes an early split and the whole tree below it.
Growing to full depth gives low bias and very high variance.

### Bagging

Bootstrap aggregation (Breiman 1996) fits $B$ trees to bootstrap samples and averages them.
A bootstrap sample of size $n$ contains about $1 - (1-1/n)^n \approx 1 - e^{-1} \approx 63.2\%$ of the distinct observations; the remaining 36.8% are out-of-bag (OOB) for that tree and give a free validation estimate when observations are independent.
If each tree's prediction has variance $\sigma^2$ and pairwise correlation $\rho$,

$$
\operatorname{Var}\!\left(\frac1B\sum_{b=1}^{B}T_b\right) = \rho\sigma^2 + \frac{1-\rho}{B}\sigma^2.
$$

The second term vanishes as $B$ grows; the first is a floor set by how correlated the trees are.

### Random forests

Random forests (Breiman 2001) lower $\rho$ by considering only a random subset of $m$ of the $p$ features at each split.
Common defaults from ESL: $m = \lfloor\sqrt p\rfloor$ for classification and $m = \lfloor p/3 \rfloor$ for regression, with minimum leaf sizes of 1 and 5 respectively; on noisy data much larger leaves are better.
Main hyperparameters:

- `n_estimators`: more trees never overfit; they only reduce Monte Carlo noise, with diminishing returns.
- `max_features` ($m$): lower means less correlated trees but weaker individual trees.
- `min_samples_leaf` and `max_depth`: the real complexity controls.
- `max_samples`: bootstrap sample size; smaller samples further decorrelate trees.

### Gradient boosting

Boosting builds an additive model $F_M(x) = F_0(x) + \eta\sum_{m=1}^{M} h_m(x)$ stagewise.
At stage $m$, compute pseudo-residuals, the negative gradient of the loss at the current fit,

$$
r_i = -\left.\frac{\partial L(y_i, F)}{\partial F}\right|_{F = F_{m-1}(x_i)},
$$

fit a small tree $h_m$ to them, and add it scaled by the learning rate $\eta$ (Friedman 2001).
For squared loss the pseudo-residuals are ordinary residuals $y_i - F(x_i)$; for log-loss with $p = \sigma(F)$ they are $y_i - p_i$.
Subsampling rows each round (stochastic gradient boosting, Friedman 2002) adds randomness that regularises and speeds things up.

XGBoost (Chen and Guestrin 2016) takes a second-order Taylor step with gradients $g_i$ and Hessians $h_i$, and an L2 penalty $\lambda$ on leaf weights.
With $G$ and $H$ the sums of $g_i$ and $h_i$ over the samples in a leaf,

$$
w^* = -\frac{G}{H + \lambda}, \qquad \text{Gain} = \frac12\left[\frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{(G_L + G_R)^2}{H_L + H_R + \lambda}\right] - \gamma,
$$

and a split is made only if the gain is positive, so $\gamma$ is a minimum-gain threshold that prunes weak splits.
LightGBM (Ke et al. 2017) bins features into histograms and grows trees leaf-wise, which is faster and fits more aggressively, so `num_leaves` and `min_data_in_leaf` matter more than depth.

Boosting hyperparameters, from most to least important on noisy data:

- learning rate $\eta$ and number of rounds, set jointly with early stopping; smaller $\eta$ with more rounds generalises better;
- tree size (`max_depth` 2 to 4, or `num_leaves`) and minimum leaf size or `min_child_weight`;
- row and column subsampling (0.5 to 0.8);
- L2/L1 penalties on leaf weights and the split threshold $\gamma$.

Unlike random forests, adding rounds to a boosted model eventually overfits.

### Bagging against boosting

Bagging and random forests reduce variance and are hard to break with bad hyperparameters; boosting reduces bias and usually wins on accuracy when tuned, but overfits when the signal is weak and the stopping point is chosen badly.
On tabular data with moderate signal, gradient boosting is the default strong baseline.
On low signal-to-noise financial returns, a well-regularised linear model is often as good, and the job of a tree ensemble is to find robust nonlinearities and interactions, not to fit noise.

### Financial data specifics

- Low signal-to-noise: daily return $R^2$ is typically well under 1%, so the capacity of a default boosted model is spent on noise.
- Overlapping labels: a label built from a 20-day forward return shares information with the next 19 labels.
  Bootstrap samples then contain near-duplicates, trees are more correlated than they look, and the OOB score leaks because an "out-of-bag" row has near-copies in the bag.
  Lopez de Prado recommends setting the bootstrap sample size to the average label uniqueness (or using sequential bootstrapping) and validating with purged, embargoed cross-validation (see [Time-Series Cross-Validation: Purging and Embargo](02-Time-Series-Cross-Validation-Purging-Embargo.md) and [Labeling: Triple Barrier and Meta-Labeling](06-Labeling-Triple-Barrier-and-Meta-Labeling.md)).
- Non-stationarity: early stopping must use a validation block later in time than the training data, never a random split.
- Feature importance: impurity-based importance (MDI) is computed in-sample and is biased toward continuous and high-cardinality features (Strobl et al. 2007); prefer permutation importance on purged out-of-sample folds (see [Feature Importance and Interpretability](07-Feature-Importance-and-Interpretability.md)).
- Extrapolation: trees predict a constant outside the training range of each feature, so a regime with unprecedented feature values gets the prediction of the nearest leaf.

## Worked examples

### Example 1: choosing a split by Gini impurity

A node has 10 samples: 6 up days and 4 down days, Gini $1 - 0.6^2 - 0.4^2 = 0.48$.
Split A sends 4 samples left (4 up, 0 down) and 6 right (2 up, 4 down).
Weighted child Gini is $0.4 \times 0 + 0.6 \times (1 - (1/3)^2 - (2/3)^2) = 0.6 \times 0.444 = 0.267$, a decrease of 0.213.
Split B sends 4 left (3 up, 1 down) and 6 right (3 up, 3 down): $0.4 \times 0.375 + 0.6 \times 0.5 = 0.45$, a decrease of only 0.03.
The tree takes split A.

### Example 2: how much does averaging help?

Each tree's prediction has variance 1.
With $\rho = 0.3$: 10 trees give $0.3 + 0.7/10 = 0.37$ and 500 trees give $0.3014$, so going from 10 to 500 trees cuts variance by less than a fifth.
Lowering the correlation to 0.1 with smaller `max_features` gives a floor of about 0.1 at 500 trees, if individual trees do not get much worse.
With $\rho = 0.8$, typical of trees trained on heavily overlapping financial labels, 500 trees still leave 0.80: the ensemble barely helps.

### Example 3: boosting by hand with squared loss

Data $x = (1, 2, 3, 4)$ and $y = (1, 3, 2, 6)$.
$F_0 = \bar y = 3$, residuals $r = (-2, 0, -1, 3)$, total squared error 14.
Candidate stumps on the residuals:

| Split | Left mean | Right mean | SSE after |
| :--- | ---: | ---: | ---: |
| $x \le 1.5$ | -2.00 | 0.67 | 8.67 |
| $x \le 2.5$ | -1.00 | 1.00 | 10.00 |
| $x \le 3.5$ | -1.00 | 3.00 | 2.00 |

Take $x \le 3.5$: predict $-1$ on the left and $+3$ on the right.
With $\eta = 0.1$, $F_1 = (2.9, 2.9, 2.9, 3.3)$, new residuals $(-1.9, 0.1, -0.9, 2.7)$ and squared error 11.72.
With $\eta = 1$ the error would drop to 2 in one step, which is exactly how boosting memorises noise; the small step leaves room for later trees to average over many directions.

### Example 4: an XGBoost leaf for log-loss

Four samples with labels $(1, 1, 0, 1)$ start at $F_0 = 0$, so $p = 0.5$.
Gradients $g_i = p - y_i = (-0.5, -0.5, 0.5, -0.5)$, Hessians $h_i = p(1-p) = 0.25$.
In one leaf, $G = -1$ and $H = 1$.
With $\lambda = 0$, $w^* = 1$; with $\lambda = 1$, $w^* = -(-1)/(1 + 1) = 0.5$: the penalty halves the step.
With $\eta = 0.1$ the new score is 0.05 and the predicted probability moves from 0.5 to 0.512.
Splitting $\{1, 2\}$ from $\{3, 4\}$ gives $G_L = -1, H_L = 0.5$ and $G_R = 0, H_R = 0.5$, so with $\lambda = 1$ the gain is $\frac12\left[\frac{1}{1.5} + 0 - \frac{1}{2}\right] \approx 0.083$.
Splitting $\{1, 2, 4\}$ from $\{3\}$ gives gain $\frac12\left[\frac{2.25}{1.75} + \frac{0.25}{1.25} - 0.5\right] \approx 0.493$, the better split; with $\gamma = 0.1$ the first split would be pruned and the second kept.

### Example 5: overfitting a weak signal

Simulate 10 features, of which only the first matters: $y = 0.1\,x_1 + \varepsilon$ with standard normal $x$ and $\varepsilon$, so the best possible $R^2$ is $0.01/1.01 \approx 0.0099$.
Train on 5,000 rows and test on 5,000 new rows (seed 42, scikit-learn 1.9):

| Model | Train $R^2$ | Test $R^2$ |
| :--- | ---: | ---: |
| Boosting, depth 6, 500 rounds, $\eta = 0.1$ | 0.904 | -0.127 |
| Boosting, depth 2, 100 rounds, $\eta = 0.05$, subsample 0.5 | 0.051 | 0.004 |
| Random forest, defaults (full depth) | 0.862 | -0.016 |
| Random forest, min leaf 200, 30% of features | 0.033 | 0.008 |

The default models fit the noise and lose to predicting the mean; the heavily regularised forest recovers most of the attainable 0.0099.
A train $R^2$ far above any plausible true $R^2$ is the diagnostic.

```python
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score

rng = np.random.default_rng(42)
X = rng.standard_normal((10_000, 10))
y = 0.1 * X[:, 0] + rng.standard_normal(10_000)
Xtr, ytr, Xte, yte = X[:5000], y[:5000], X[5000:], y[5000:]
deep = GradientBoostingRegressor(max_depth=6, n_estimators=500, learning_rate=0.1, random_state=0)
deep.fit(Xtr, ytr)
print(r2_score(ytr, deep.predict(Xtr)), r2_score(yte, deep.predict(Xte)))  # about 0.90, -0.13
```

## Pitfalls

- Tuning boosting on a random K-fold split of time-series data; the validation score leaks through overlapping labels and autocorrelation.
- Trusting the random forest OOB score when labels overlap; near-duplicate rows are in the bag.
- Reading MDI importance as causal or even as out-of-sample relevance; it is in-sample and biased toward high-cardinality features.
- Adding boosting rounds without early stopping; unlike forests, boosting overfits as rounds grow.
- Using a large learning rate to save time; it reaches the overfit regime in a handful of rounds.
- Expecting trees to extrapolate; they predict constants beyond the training range.
- Comparing models on in-sample fit or accuracy without a naive baseline such as predicting the mean or the majority class.

## Interview questions

> [!question]- ml-trees-bagging-variance | What is the variance of an average of B identically distributed trees with pairwise correlation rho?
> $\rho\sigma^2 + (1-\rho)\sigma^2/B$.
> As $B \to \infty$ it falls to $\rho\sigma^2$, so decorrelating trees matters more than adding them.

> [!question]- ml-trees-oob-fraction | What fraction of observations is out-of-bag for a given bootstrap tree?
> About 36.8%.
> Each observation is missed with probability $(1-1/n)^n \to e^{-1}$.

> [!question]- ml-trees-rf-vs-bagging | How does a random forest differ from bagged trees, and why does it help?
> At each split it considers only a random subset of $m$ features.
> That lowers the correlation between trees and so the variance floor $\rho\sigma^2$, at a small cost in individual-tree accuracy.

> [!question]- ml-trees-more-trees-overfit | Does adding more trees overfit a random forest? A boosted model?
> Not a random forest: more trees only reduce Monte Carlo noise.
> A boosted model does overfit as rounds increase, which is why the number of rounds is set by early stopping.

> [!question]- ml-trees-pseudo-residuals | What does each new tree fit in gradient boosting?
> The negative gradient of the loss at the current predictions (pseudo-residuals).
> For squared loss that is $y - F$; for log-loss it is $y - p$.

> [!question]- ml-trees-xgb-leaf-weight | What is the optimal leaf weight in XGBoost and what does lambda do?
> $w^* = -G/(H + \lambda)$, with $G$ and $H$ the summed gradients and Hessians in the leaf.
> $\lambda$ shrinks leaf weights toward zero, most strongly in leaves with little Hessian mass (few samples or confident predictions).

> [!question]- ml-trees-gamma | What does the gamma parameter in XGBoost control?
> The minimum loss reduction needed to make a split.
> A split is kept only if its gain exceeds $\gamma$, which prunes weak splits that mostly fit noise.

> [!question]- ml-trees-lr-rounds | How do learning rate and number of rounds interact?
> They trade off: halving the learning rate needs roughly twice the rounds for the same fit, and usually generalises better.
> Fix a small rate and choose the rounds by early stopping on a later-in-time validation block.

> [!question]- ml-trees-low-snr-overfit | Your boosted model has train R-squared 0.9 on daily returns. What do you conclude?
> It is fitting noise; plausible out-of-sample $R^2$ for daily returns is well under 1%.
> Cut depth, raise minimum leaf size, lower the learning rate, subsample, and validate with purged time-series CV against a mean baseline.

> [!question]- ml-trees-oob-overlap | Why is the OOB score unreliable with overlapping financial labels?
> Out-of-bag rows have near-duplicates (overlapping label windows) inside the bag, so the OOB score leaks and is optimistic.
> Use purged, embargoed CV and set the bootstrap sample size to the average label uniqueness.

> [!question]- ml-trees-mdi-bias | Why is impurity-based (MDI) feature importance misleading?
> It is computed in-sample and favours continuous and high-cardinality features that offer many split points, even when they are noise.
> Prefer permutation importance measured on out-of-sample, purged folds.

> [!question]- ml-trees-extrapolation | How does a tree ensemble predict for feature values outside the training range?
> As a constant: the value of the leaf at the edge of the training range.
> Trees cannot extrapolate trends, which matters when a regime pushes features to new extremes.

> [!question]- ml-trees-gini-split | A node has 6 up and 4 down days. Split A gives (4, 0) and (2, 4); split B gives (3, 1) and (3, 3). Which does a Gini tree choose?
> Split A, with weighted Gini 0.267 against 0.45 for B.
> The parent Gini is 0.48, so A reduces impurity by 0.213 and B by only 0.03.

## Further reading

- Hastie, Tibshirani and Friedman, *The Elements of Statistical Learning* (2nd ed., 2009), chapters 9, 10 and 15.
- Breiman (1996), Bagging predictors, *Machine Learning* 24(2); Breiman (2001), Random forests, *Machine Learning* 45(1).
- Friedman (2001), Greedy function approximation: a gradient boosting machine, *Annals of Statistics* 29(5); Friedman (2002), Stochastic gradient boosting.
- Chen and Guestrin (2016), XGBoost: a scalable tree boosting system, KDD.
- Ke et al. (2017), LightGBM: a highly efficient gradient boosting decision tree, NeurIPS.
- Marcos Lopez de Prado, *Advances in Financial Machine Learning* (2018), chapters 6 to 8.
- Strobl, Boulesteix, Zeileis and Hothorn (2007), Bias in random forest variable importance measures, *BMC Bioinformatics* 8.
