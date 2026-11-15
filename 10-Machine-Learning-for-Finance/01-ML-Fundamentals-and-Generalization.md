---
type: concept
track: [quant-research, quant-dev]
tier: core
status: solid
prereqs: [linear-regression-ols, regularization-ridge-lasso]
est_hours: 4
sources: [Hastie Tibshirani and Friedman - The Elements of Statistical Learning (2nd ed.) ch 2 3 7, Murphy - Probabilistic Machine Learning - An Introduction (2022) ch 4 5, Gu Kelly and Xiu (2020) - Empirical Asset Pricing via Machine Learning - Review of Financial Studies 33(5), Campbell and Thompson (2008) - Predicting Excess Stock Returns Out of Sample - Review of Financial Studies 21(4), Grinold and Kahn - Active Portfolio Management (2nd ed.), Lopez de Prado - Advances in Financial Machine Learning (2018)]
---

# ML Fundamentals and Generalization

## TL;DR

- Expected squared prediction error $=$ irreducible noise $+$ bias$^2$ $+$ variance; regularisation trades a little bias for a large cut in variance.
- In finance the noise term dominates: a daily return predictor with $R^2 = 0.25\%$ (correlation 0.05) is already worth an annualised Sharpe of about 0.8 when traded.
- At that signal-to-noise ratio the variance term decides everything, so heavy shrinkage, few effective parameters, simple models and ensembles win; even predicting zero can beat an unbiased estimator.
- Pure-noise features give in-sample $R^2 \approx p/(n-1)$ and out-of-sample $R^2 \approx -(1-R^2)\,p/(n-p-1)$ for OLS; with 50 pure-noise features and 500 observations that is $+10\%$ in sample and $-11\%$ out.
- Pick the loss to match the use: MSE for sizing continuous forecasts (robustified for fat tails), ranking losses and IC for cross-sectional selection; judge by out-of-sample $R^2$ against a zero forecast, IC and the Sharpe of the implied portfolio, not accuracy.

## Learning objectives

- Explain the bias-variance trade-off and regularisation.
- Choose losses and metrics that match the trading objective.
- Explain why low signal-to-noise changes model choice.

## Core concepts

### Risk, empirical risk and the generalisation gap

With data $(x, y) \sim P$ and loss $L$, the goal is low risk $R(f) = E[L(y, f(x))]$.
Training minimises empirical risk $\hat R_n(f) = \frac1n\sum_i L(y_i, f(x_i))$ over a model class, so $\hat R_n(\hat f)$ is biased downward: the fit has seen the noise.
The generalisation gap $R(\hat f) - \hat R_n(\hat f)$ grows with model flexibility and shrinks with $n$.
For OLS with $p$ parameters the expected optimism of training error (in-sample prediction error, same $x$ with fresh noise, minus training error) is $2p\sigma^2/n$, the correction behind Mallows' $C_p$ and AIC (ESL section 7.4); with $n = 500$, $p = 50$ and $\sigma = 1$ it is $0.2$.

### Bias-variance decomposition

For $y = f(x) + \varepsilon$ with $E[\varepsilon] = 0$, $\text{Var}(\varepsilon) = \sigma^2$, and an estimator $\hat f$ trained on a random sample,

$$
E\big[(y - \hat f(x))^2\big] = \underbrace{\sigma^2}_{\text{noise}} + \underbrace{\big(f(x) - E\hat f(x)\big)^2}_{\text{bias}^2} + \underbrace{\text{Var}\big(\hat f(x)\big)}_{\text{variance}}.
$$

Proof: expand around $E\hat f(x)$; cross terms vanish because $\varepsilon$ is independent of the training sample and $\hat f - E\hat f$ has mean zero.
A check by enumeration: with $y = \tfrac12 + \varepsilon$, $\varepsilon = \pm1$ equally likely, and $\hat f = \tfrac12\bar y$ over $n = 3$ draws, averaging the loss over all $2^3$ training samples and both test draws gives exactly $55/48$, which is $1 + (\tfrac14)^2 + \tfrac1{12}$: noise plus bias squared plus variance.
Flexible models lower bias and raise variance; regularisation (ridge, lasso, early stopping, pruning, dropout) and averaging (bagging, ensembles) lower variance.

### Low signal-to-noise changes the answer

Financial returns are mostly noise: monthly stock-level out-of-sample $R^2$ in Gu, Kelly and Xiu (2020, Table 1) peaks at $0.40\%$, for their three-layer neural network.
Consequences:

- The variance term dominates bias, so the optimal model is far more regularised than in vision or language tasks.
- The best shrinkage target is often zero: an estimate that is unbiased but noisy loses to one that shrinks hard toward "no predictability".
- Nonstationarity shortens the useful history, so the effective $n$ is smaller than the row count, and overlapping labels shrink it further ([Purging and Embargo](02-Time-Series-Cross-Validation-Purging-Embargo.md)).
- Every hyperparameter search is a multiple test ([Overfitting and Deflated Sharpe](../09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md)).
- Tiny $R^2$ is still valuable: if forecast $f$ and return $r$ are standard bivariate normal with correlation $\rho$ and you hold position $f$, the per-period Sharpe is $E[fr]/\text{sd}(fr) = \rho/\sqrt{1+\rho^2} \approx \rho$, because $E[f^2r^2] = 1 + 2\rho^2$ (Isserlis) and so $\text{Var}(fr) = 1 + \rho^2$.

### Regularisation

- Ridge: $\hat\beta = (X^\top X + \lambda I)^{-1}X^\top y$, shrinks along small-singular-value directions; effective degrees of freedom $\sum_j d_j^2/(d_j^2 + \lambda)$.
- Lasso: $\ell_1$ penalty, sparse solutions, unstable with correlated features; elastic net mixes both.
- Early stopping, weight decay, dropout and tree depth or leaf-size limits play the same role for nonlinear models.
- For a random Gaussian design and a rotation-invariant signal, the MSE-optimal ridge penalty on unscaled $X^\top X$ is $\lambda^* = p\sigma^2/\|\beta\|^2$, the posterior mean under the prior $\beta \sim N(0, I\|\beta\|^2/p)$; it is huge when signal is weak.

See [Regularization: Ridge and Lasso](../02-Statistics-and-Econometrics/06-Regularization-Ridge-Lasso.md) for the derivations.

### Losses and metrics that match the objective

| Use of the forecast | Training loss | Evaluation metric |
| :--- | :--- | :--- |
| Size positions in one asset | MSE, Huber if fat-tailed | OOS $R^2$ versus zero, Sharpe of $f\cdot r$ |
| Rank a cross-section | MSE on ranks or vol-scaled returns, pairwise or listwise ranking loss | Spearman IC per date, long-short decile Sharpe |
| Decide trade or no trade | Log loss, weighted by return size | Expected PnL per trade, precision at the traded threshold |
| Forecast volatility or risk | QLIKE or MSE on variance | QLIKE, VaR exceptions |

Rules of thumb:

- Accuracy and hit rate ignore payoff size; a 55% hit rate loses money if average losses are 1.5 times average wins.
- Out-of-sample $R^2$ should be measured against a zero forecast, $R^2_{OS} = 1 - \sum(y - \hat y)^2/\sum y^2$, not against the in-sample mean, which is itself a noisy forecast (Gu, Kelly and Xiu 2020; Campbell and Thompson 2008 benchmark against the historical mean).
- IC is scale-free, so a forecast can have good IC and terrible MSE; sizing needs calibration, selection does not.
- MSE is dominated by the few largest returns; winsorise or vol-scale targets, or use Huber loss.
- Evaluate net of costs and turnover; a model that flips signs daily can win on IC and lose on PnL.
- The standard error of an IC over $N$ independent observations is about $1/\sqrt N$, so a single-date IC across 500 stocks has se 0.045 under the null.

### Validation discipline

Split data into train, validation (for hyperparameters and early stopping) and a final test set touched once.
In time series the splits must respect time and label overlap ([Time-Series Cross-Validation](02-Time-Series-Cross-Validation-Purging-Embargo.md)).
Fit every preprocessing step (scalers, PCA, feature selection, target encoding) inside the training fold only.

## Worked examples

### 1. Shrinking a mean return

Estimate a stock's expected daily return from one year ($n = 252$) of data: true $\mu = 4$ bp, daily vol $\sigma = 1\%$.
Consider $c\,\bar x$ for $c \in [0,1]$: $\text{MSE}(c) = (1-c)^2\mu^2 + c^2\sigma^2/n$.

- Unbiased $c = 1$: MSE $= \sigma^2/n = 3.97\times10^{-7}$.
- Predict zero, $c = 0$: MSE $= \mu^2 = 1.6\times10^{-7}$, less than half.
- Optimal $c^* = \mu^2/(\mu^2 + \sigma^2/n) = 0.287$, MSE $1.14\times10^{-7}$.

The signal's $t$-stat is only $\mu/(\sigma/\sqrt n) = 0.63$, and whenever it is below 1 the zero forecast beats the unbiased one.
This is the one-parameter version of why ridge, James-Stein and Bayesian priors dominate in finance.

### 2. What a tiny $R^2$ is worth

A daily timing signal has correlation $\rho = 0.05$ with next-day returns, i.e. $R^2 = 0.25\%$.
Holding a position proportional to the standardised forecast gives per-period Sharpe $\rho/\sqrt{1+\rho^2} = 0.0499$, annualised $0.0499\times\sqrt{252} = 0.79$ before costs.
At $\rho = 0.10$ ($R^2 = 1\%$) the annualised Sharpe is 1.58.
So an $R^2$ that would be rejected as useless in most ML settings is a good strategy, and the headline target in finance is a stable $\rho$ of a few percent, not a high $R^2$.

### 3. Overfitting pure noise with OLS

$n = 500$ observations, $p = 50$ features.

- If all features are noise, in-sample $R^2$ has a Beta$(p/2, (n-p-1)/2)$ distribution with mean $p/(n-1) = 0.100$.
- If all features are noise, the expected out-of-sample $R^2$ against a zero forecast is $-p/(n-p-1) = -50/449 \approx -11\%$.
- If the true population $R^2$ is 1%, the expected OLS out-of-sample $R^2$ (Gaussian random design, no intercept) is $R^2 - (1-R^2)\,p/(n-p-1) = 0.01 - 0.99\times50/449 = -0.100$, because $E\|\hat\beta - \beta\|^2 = \sigma^2 p/(n-p-1)$.
- OLS breaks even at $n = p + 1 + p(1-R^2)/R^2 = 5001$ observations and beats the zero forecast only beyond that; at $n = 5001$ a simulation of 300 training sets gives an out-of-sample $R^2$ of zero within its standard error.

A 10% in-sample $R^2$ on 50 features is therefore not evidence of anything.

### 4. Ridge at low signal-to-noise

Set-up: $n = 500$ training rows, $p = 50$ standard normal features, unit noise, and $\|\beta\|^2 = 1/99$, so the population $R^2$ is exactly 1%.
Fit ridge $\hat\beta = (X^\top X + \lambda I)^{-1}X^\top y$ and score against a zero forecast, as for returns.
With a Gaussian test design the out-of-sample MSE of $\hat\beta$ is exactly $\sigma^2 + \|\beta - \hat\beta\|^2$, so no test sample is needed.
Averaged over 2,000 simulated training sets (seed 20261119 in the script named below):

| $\lambda$ | In-sample $R^2$ | Out-of-sample $R^2$ |
| :--- | :--- | :--- |
| 0 (OLS) | 11.0% | $-10.0\%$ |
| 100 | 10.6% | $-6.2\%$ |
| 1,000 | 6.0% | $-0.52\%$ |
| 5,000 | 1.9% | $+0.09\%$ |
| 10,000 | 1.0% | $+0.07\%$ |
| 100,000 | 0.1% | $+0.01\%$ |

The OLS row matches the closed forms: in sample about $1 - (1-R^2)(n-p)/n = 10.9\%$, out of sample $-10.0\%$.
The best penalty, on this grid and on a fine grid from 500 to 50,000, is 5,000, next to the theoretical $\lambda^* = p\sigma^2/\|\beta\|^2 = 4950$.
It is so large that in-sample fit almost vanishes, and even then only 0.09 of the achievable 1 percentage point of $R^2$ is captured.
In-sample $R^2$ moves in the wrong direction as a model selection criterion.

### 5. Hit rate is not the objective

A classifier is right 55% of the time; average winning trade $+1.0$, average losing trade $-1.5$.
Expected PnL per trade $= 0.55\times1.0 - 0.45\times1.5 = -0.125$.
Another model with 48% hit rate, $+2.0$ wins and $-1.0$ losses earns $0.96 - 0.52 = +0.44$.
Train with sample weights proportional to $|r|$, or regress on returns directly, so the loss sees payoff size.

## Pitfalls

- Reporting in-sample or cross-validated $R^2$ without the number of features, trials and hyperparameter settings tried.
- Measuring $R^2_{OS}$ against the in-sample mean when the natural benchmark for returns is zero, or vice versa without saying so.
- Using accuracy, AUC or hit rate as the headline metric for a trading signal.
- Training MSE on raw returns in which a handful of crash days dominate the loss.
- Choosing a deep, flexible model because it wins on benchmark ML datasets; at finance signal-to-noise the variance term usually decides.
- Fitting scalers, PCA or feature selection on the full sample before cross-validation.
- Treating an IC of 0.05 as noise: it is small but, if stable and broad, commercially valuable.
- Believing more features always help: each weak feature adds variance roughly $\sigma^2/n$ to the forecast.

## Interview questions

> [!question]- ml-fundamentals-bias-variance | Write the bias-variance decomposition of expected squared error.
> $E[(y-\hat f(x))^2] = \sigma^2 + (f(x) - E\hat f(x))^2 + \text{Var}(\hat f(x))$.
> Expand around $E\hat f(x)$; the cross terms vanish because the noise is independent of the training sample.

> [!question]- ml-fundamentals-low-snr-model-choice | Why does low signal-to-noise push you toward simpler, more regularised models?
> Because the estimation variance term dominates the error, so reducing variance is worth much more than reducing bias.
> With $R^2$ around 1%, flexible models mostly fit noise; shrinkage, few effective parameters and ensembles generalise better.

> [!question]- ml-fundamentals-zero-beats-mean | True daily mean 4 bp, vol 1%, one year of data. Does the sample mean beat predicting zero in MSE?
> No: MSE of the sample mean is $\sigma^2/n = 3.97\times10^{-7}$, of zero is $\mu^2 = 1.6\times10^{-7}$.
> Zero wins whenever the signal's $t$-stat $\mu\sqrt n/\sigma$ is below 1; here it is 0.63, and the optimal shrinkage factor is 0.29.

> [!question]- ml-fundamentals-r2-to-sharpe | A daily forecast has correlation 0.05 with next-day returns. What Sharpe can you expect from trading it?
> About 0.8 annualised before costs.
> For bivariate normal forecast and return, the Sharpe of $f\cdot r$ is $\rho/\sqrt{1+\rho^2} \approx 0.05$ per day, times $\sqrt{252}$.

> [!question]- ml-fundamentals-noise-r2 | You regress returns on 50 pure-noise features with 500 observations. Expected in-sample $R^2$?
> About $p/(n-1) = 0.10$.
> Under the null (with an intercept) $R^2 \sim \text{Beta}(p/2, (n-p-1)/2)$; out of sample against a zero forecast it would be about $-p/(n-p-1) = -11\%$.

> [!question]- ml-fundamentals-ols-breakeven | Population $R^2$ is 1% with 50 features. Roughly how many observations before OLS beats a zero forecast out of sample?
> About 5,000.
> Expected $R^2_{OS} = R^2 - (1-R^2)p/(n-p-1)$ for a Gaussian design, which is positive only for $n > p + 1 + p(1-R^2)/R^2 = 5001$.

> [!question]- ml-fundamentals-ridge-lambda | For isotropic Gaussian features, what ridge penalty minimises out-of-sample MSE, and what does it imply at low SNR?
> $\lambda^* = p\sigma^2/\|\beta\|^2$, the noise-to-signal ratio times the number of features.
> With $R^2 = 1\%$, $p = 50$, it is $50 \times 99 = 4950$ on unscaled $X^\top X$, far larger than defaults tuned for high-SNR problems.

> [!question]- ml-fundamentals-hit-rate | A model has a 55% hit rate. Is it profitable?
> Not necessarily; profitability depends on payoff sizes.
> With average win 1.0 and average loss 1.5, expectancy is $0.55 - 0.675 = -0.125$ per trade.

> [!question]- ml-fundamentals-r2-oos-benchmark | How should out-of-sample $R^2$ be defined for return forecasts?
> $R^2_{OS} = 1 - \sum(y-\hat y)^2/\sum(y-\bar y_{\text{bench}})^2$ with an explicit benchmark, usually zero for individual returns.
> The historical mean is itself a noisy forecast, so benchmarking against it (Campbell-Thompson) or zero (Gu-Kelly-Xiu) must be stated.

> [!question]- ml-fundamentals-ic-vs-mse | When would you optimise IC rather than MSE?
> When the forecast is used only to rank a cross-section and positions are set by a separate sizing step.
> IC is scale-free and robust to calibration; MSE matters when forecast magnitude directly sets position size.

> [!question]- ml-fundamentals-fat-tail-loss | Why is plain MSE on raw returns a poor training loss, and what do you do instead?
> A few extreme days dominate the squared loss, so the model fits outliers.
> Use Huber loss, winsorise, rank-transform or vol-scale the target, and check that the evaluation metric matches.

> [!question]- ml-fundamentals-preprocessing-leak | You standardise features using the full-sample mean and variance before cross-validation. What is wrong?
> Information from the test folds leaks into training, and in time series it is look-ahead.
> Fit every transform inside each training fold and apply it to the test fold.

> [!question]- ml-fundamentals-optimism | For OLS with $p$ parameters and noise variance $\sigma^2$, how much lower is training error than in-sample prediction error on average?
> By $2p\sigma^2/n$, the optimism (ESL section 7.4).
> The fit's summed covariance with the noise is $\sigma^2\operatorname{tr}(H) = p\sigma^2$ for the hat matrix $H$; with $n = 500$, $p = 50$ and $\sigma = 1$ it is $0.2$, which $C_p$ and AIC add back.

> [!question]- ml-fundamentals-sharpe-derivation | Forecast $f$ and return $r$ are standard bivariate normal with correlation $\rho$. Derive the Sharpe of holding $f$.
> $\rho/\sqrt{1+\rho^2}$ per period.
> $E[fr] = \rho$ and, by Isserlis, $E[f^2r^2] = 1 + 2\rho^2$, so $\text{Var}(fr) = 1 + \rho^2$; at $\rho = 0.10$ that is $1.58$ annualised over 252 days.

> [!question]- ml-fundamentals-noise-oos-r2 | 50 pure-noise features, 500 observations, OLS without intercept. What out-of-sample $R^2$ against a zero forecast do you expect?
> $-p/(n-p-1) = -50/449 \approx -11\%$.
> The test MSE is $\sigma^2 + \|\hat\beta\|^2$ and $E\|\hat\beta\|^2 = \sigma^2p/(n-p-1)$ for a Gaussian design.

> [!question]- ml-fundamentals-ic-standard-error | What is the standard error of a single-date IC across 500 stocks under the null?
> About $1/\sqrt{500} = 0.045$.
> So a single-date IC of 0.05 is about one standard error; only an average over many dates can establish a signal of that size.

## In this repo and The-Distinguished-Engineer

- Code: [`code/ml_01_generalization.py`](code/ml_01_generalization.py) prints and asserts every number on this page: the bias-variance identity by exhaustive enumeration with exact fractions and by simulation for ridge, the optimism by simulation against the hat-matrix trace, the forecast Sharpe by Gauss-Hermite quadrature and simulation, the shrunk mean by simulation and a golden-section search, the noise-feature and break-even results by simulation against the closed forms, and the ridge table by simulation cross-checked against the expected loss with the noise integrated exactly.
- Related notes: [Regularization: Ridge and Lasso](../02-Statistics-and-Econometrics/06-Regularization-Ridge-Lasso.md), [Time-Series Cross-Validation](02-Time-Series-Cross-Validation-Purging-Embargo.md), [Tree Ensembles and Gradient Boosting](03-Tree-Ensembles-and-Gradient-Boosting.md).

## Further reading

- Hastie, Tibshirani and Friedman, *The Elements of Statistical Learning* (2nd ed., 2009), chapters 2, 3 and 7 (section 7.4 for the optimism).
- Kevin Murphy, *Probabilistic Machine Learning: An Introduction* (2022).
- Gu, Kelly and Xiu (2020), Empirical Asset Pricing via Machine Learning, *Review of Financial Studies* 33(5), 2223-2273; Table 1 for out-of-sample $R^2$ by model.
- Campbell and Thompson (2008), Predicting Excess Stock Returns Out of Sample: Can Anything Beat the Historical Average?, *Review of Financial Studies* 21(4), 1509-1531.
- Grinold and Kahn, *Active Portfolio Management*, on IC and the fundamental law ([Performance Metrics and Fundamental Law](../09-Alpha-Research-and-Portfolio/09-Performance-Metrics-and-Fundamental-Law.md)).
- Marcos Lopez de Prado, *Advances in Financial Machine Learning*.
