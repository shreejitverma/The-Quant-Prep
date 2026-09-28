---
type: concept
track: [quant-research]
tier: core
status: solid
prereqs: [linear-regression-ols]
est_hours: 3
sources: [Hastie Tibshirani and Friedman - The Elements of Statistical Learning 2nd ed ch 3 7, Hastie Tibshirani and Wainwright - Statistical Learning with Sparsity ch 2 4, Hoerl and Kennard (1970) - Ridge Regression - Technometrics, Tibshirani (1996) - Regression Shrinkage and Selection via the Lasso - JRSS B, Zou and Hastie (2005) - Regularization and Variable Selection via the Elastic Net - JRSS B]
---

# Regularization: Ridge, Lasso and Elastic Net

## TL;DR

- Ridge minimises $\|y-X\beta\|^2 + \lambda\|\beta\|_2^2$ and has the closed form $(X^\top X+\lambda I)^{-1}X^\top y$, which exists for every $\lambda>0$ even when $p > n$.
- In the SVD $X = UDV^\top$, ridge shrinks the component along the $j$-th principal direction by $d_j^2/(d_j^2+\lambda)$: low-variance (collinear) directions are shrunk most; effective degrees of freedom are $\sum_j d_j^2/(d_j^2+\lambda)$.
- Lasso minimises $\frac12\|y-X\beta\|^2 + \lambda\|\beta\|_1$; for an orthonormal design it soft-thresholds OLS, $\text{sign}(\hat\beta_j)(|\hat\beta_j|-\lambda)_+$, so it sets coefficients exactly to zero.
- Bayesian view: ridge is the posterior mode (and mean) under a Gaussian prior with $\lambda = \sigma^2/\tau^2$; lasso is the posterior mode under a Laplace prior.
- For a coefficient with $t$-stat around 1, optimal shrinkage halves the MSE; this is why signal weights, betas and covariances in finance are shrunk by default.
- Standardise features, leave the intercept unpenalised, and choose $\lambda$ by time-ordered cross-validation with purging.

## Learning objectives

- Derive ridge in closed form and explain its shrinkage in the eigenbasis.
- Explain lasso sparsity geometrically and choose penalties by cross-validation.
- Give the Bayesian interpretation of each penalty.

## Core concepts

### Why regularise

OLS is unbiased but its variance $\sigma^2(X^\top X)^{-1}$ explodes when regressors are collinear or $p$ is close to $n$, and it is undefined for $p > n$.
Trading some bias for less variance lowers mean squared error ([Estimation](01-Estimation-MLE-and-Method-of-Moments.md)).
Hoerl and Kennard (1970) proved that for any true $\beta$ there is some $\lambda>0$ for which ridge has strictly lower total MSE than OLS; the catch is that the best $\lambda$ depends on the unknown $\beta$.

### Ridge: closed form and eigenbasis

The gradient of $\|y-X\beta\|^2 + \lambda\|\beta\|^2$ is $-2X^\top(y-X\beta) + 2\lambda\beta$, which vanishes at

$$
\hat\beta_{\text{ridge}} = (X^\top X+\lambda I)^{-1}X^\top y .
$$

$X^\top X+\lambda I$ has eigenvalues $d_j^2+\lambda>0$, so it is always invertible and better conditioned.
With the thin SVD $X = UDV^\top$,

$$
X\hat\beta_{\text{ridge}} = \sum_j u_j\,\frac{d_j^2}{d_j^2+\lambda}\,u_j^\top y ,
$$

so ridge projects onto the principal directions like OLS but shrinks each by $d_j^2/(d_j^2+\lambda)$.
Directions with small $d_j$ (little variation in the data, typically the difference between collinear signals) are shrunk most, which is exactly where OLS variance comes from.
Principal-components regression is the hard-threshold version: keep factor 1 for the top $k$ directions and 0 for the rest.
Effective degrees of freedom $\text{df}(\lambda) = \text{tr}\big(X(X^\top X+\lambda I)^{-1}X^\top\big) = \sum_j d_j^2/(d_j^2+\lambda)$ fall from $p$ at $\lambda = 0$ towards 0.
For an orthonormal design ($X^\top X = I$) ridge is simply $\hat\beta_{\text{OLS}}/(1+\lambda)$: uniform proportional shrinkage, never exactly zero.

### Lasso and sparsity

Lasso has no closed form in general; it is a convex problem solved by coordinate descent or LARS.
Its KKT conditions are $x_j^\top(y-X\hat\beta) = \lambda\,\text{sign}(\hat\beta_j)$ for active $j$ and $|x_j^\top(y-X\hat\beta)|\le\lambda$ for $\hat\beta_j = 0$.
So all coefficients are zero once $\lambda\ge\lambda_{\max} = \max_j|x_j^\top y|$, which starts the regularisation path.
For an orthonormal design each coordinate decouples and the solution is soft thresholding, $\text{sign}(\hat\beta_j)(|\hat\beta_j|-\lambda)_+$.
Geometry: in constrained form, minimise RSS subject to $\|\beta\|_1\le t$; the RSS ellipses usually first touch the $\ell_1$ diamond at a corner, where some coordinates are zero, while the $\ell_2$ ball has no corners.
With a group of highly correlated predictors lasso tends to pick one somewhat arbitrarily and its choice is unstable across samples.
The number of non-zero coefficients is an unbiased estimate of the lasso's degrees of freedom.

### Elastic net

Elastic net penalises $\lambda_1\|\beta\|_1 + \lambda_2\|\beta\|_2^2$ (Zou and Hastie 2005).
The $\ell_2$ part gives a grouping effect, so correlated signals enter together with similar weights, and allows more than $n$ non-zero coefficients; the $\ell_1$ part still selects.
It is usually the right default for many correlated alpha features.

### Bayesian interpretation

With $y\mid\beta\sim N(X\beta,\sigma^2I)$ and prior $\beta\sim N(0,\tau^2I)$, the negative log-posterior is $\frac{1}{2\sigma^2}\|y-X\beta\|^2 + \frac{1}{2\tau^2}\|\beta\|^2$.
Multiplying by $2\sigma^2$ gives ridge with $\lambda = \sigma^2/\tau^2$; since the posterior is Gaussian, ridge is both its mode and its mean.
With independent Laplace priors $p(\beta_j)\propto e^{-|\beta_j|/b}$, the posterior mode solves the lasso with $\lambda = \sigma^2/b$ in the $\frac12\|y-X\beta\|^2$ convention.
The lasso estimate is a mode, not the posterior mean, which is never exactly sparse.
A strong prior (small $\tau$ or $b$) means heavy shrinkage; this is the same logic as Black-Litterman and covariance shrinkage.

### Choosing lambda

- Standardise each column to unit variance first, or the penalty punishes features for their units; do not penalise the intercept (centre $y$ and $X$ instead).
- Pick $\lambda$ by $K$-fold cross-validation over a log-spaced grid, and often use the one-standard-error rule: the largest $\lambda$ whose CV error is within one SE of the minimum.
- With time series, folds must respect time: walk-forward or purged, embargoed $K$-fold ([Time-Series Cross-Validation](../10-Machine-Learning-for-Finance/02-Time-Series-Cross-Validation-Purging-Embargo.md)).
- Standardise inside each training fold, using only training data, or the scaler leaks the future.
- Report the CV error curve, not just the chosen point; a flat curve means $\lambda$ hardly matters.

## Worked examples

### Example 1 - ridge versus lasso on an orthonormal design

"With $X^\top X = I$, OLS gives $\hat\beta = (3, 1, -0.5, 0.2)$. Find ridge with $\lambda = 1$ and lasso with $\lambda = 0.8$."

Ridge: divide by $1+\lambda = 2$, giving $(1.5, 0.5, -0.25, 0.1)$; all shrunk by half, none removed.
Lasso: subtract 0.8 from each magnitude and floor at zero, giving $(2.2, 0.2, 0, 0)$.
Lasso removes the small coefficients and shifts the large ones by a constant, which biases large effects; ridge biases every coefficient by the same proportion.
$\lambda_{\max}$ for this lasso is $3$: above it, everything is zero.

### Example 2 - two collinear signals

"Two standardised signals with correlation 0.95 over $n = 250$ observations have $X^\top y = (200, 190)$. Compare OLS, ridge with $\lambda = 12.5$ and lasso with $\lambda = 12.5$."

$X^\top X = 250\begin{pmatrix}1&0.95\\0.95&1\end{pmatrix}$ has eigenvalues $d^2 = 487.5$ (along the average of the signals) and $12.5$ (along their difference).
With unit noise, the OLS standard error of each coefficient is $\sqrt{1/(250(1-0.95^2))} = 0.203$, versus $0.063$ if the signals were uncorrelated.
OLS gives $(0.8, 0)$: all weight on signal 1, driven by a difference that is mostly noise.
Ridge shrinks the average direction by $487.5/500 = 0.975$ and the difference direction by $12.5/25 = 0.5$, giving $(0.59, 0.19)$ with $\text{df} = 1.475$.
Lasso gives $(0.75, 0)$: it keeps one signal, and the KKT check for signal 2 is $|190 - 237.5\times0.75| = 11.9\le12.5$.
Ridge's blend is usually the more robust combination out of sample; lasso's choice would flip if the noise favoured signal 2.

### Example 3 - how much to shrink a noisy coefficient

"An estimated coefficient is $\hat\beta\sim N(\beta, s^2)$ with $\beta = 0.5$ and $s = 0.5$, a $t$-stat around 1. Shrink it to $\hat\beta/(1+\lambda)$. Which $\lambda$ minimises MSE?"

With $c = 1/(1+\lambda)$, $\text{MSE} = c^2s^2 + (1-c)^2\beta^2$, minimised at $c = \beta^2/(\beta^2+s^2)$, that is $\lambda^* = s^2/\beta^2 = 1$.
MSE falls from $0.25$ (OLS) to $0.125$; $\lambda = 0.5$ or $2$ both give $0.139$.
If $\beta = 1$ ($t\approx2$), $\lambda^* = 0.25$ and MSE falls from $0.25$ to $0.20$.
Weak signals should be shrunk hard; strong ones barely.
In practice $\beta$ is unknown, so $\lambda$ is estimated by cross-validation or empirical Bayes (James-Stein).

### Example 4 - from a prior to a penalty

"You believe a standardised signal's coefficient is $N(0, 0.1^2)$ a priori, residual noise is 1, and $x^\top x = n = 400$. What ridge penalty does this imply, and how much is OLS shrunk? What lasso penalty comes from a Laplace prior with the same variance?"

$\lambda = \sigma^2/\tau^2 = 1/0.01 = 100$.
The single-regressor ridge estimate is $x^\top y/(400+100) = 0.8\,\hat\beta_{\text{OLS}}$.
A Laplace prior with variance $2b^2 = 0.01$ has $b = 0.0707$, so $\lambda = \sigma^2/b = 14.1$ and the soft threshold on $\hat\beta_{\text{OLS}}$ is $\lambda/n = 0.035$.
Any OLS estimate smaller in magnitude than 0.035, a $t$-stat below $0.035\sqrt{400} = 0.71$, is set to zero.

## Pitfalls

- Penalising unstandardised features, so the penalty depends on units rather than information.
- Penalising the intercept, which shrinks predictions towards zero instead of towards the mean.
- Fitting the scaler or choosing $\lambda$ on the full sample, including the test period.
- Using shuffled $K$-fold CV on overlapping or autocorrelated financial labels; CV error is then optimistic and $\lambda$ too small.
- Reading lasso's selected set as "the true features"; with correlated predictors the selection is unstable, so check it across bootstrap samples or folds.
- Quoting OLS-style standard errors and p-values for penalised coefficients; they are biased and post-selection inference needs special methods.
- Thinking ridge performs variable selection; it never sets coefficients exactly to zero.

## Interview questions

> [!question]- stat-ridge-closed-form | Derive the ridge estimator.
> $\hat\beta = (X^\top X+\lambda I)^{-1}X^\top y$.
> Set the gradient $-2X^\top(y-X\beta)+2\lambda\beta$ to zero; the matrix is positive definite for $\lambda>0$, so the solution exists and is unique even if $p>n$.

> [!question]- stat-ridge-svd-shrinkage | How does ridge act in the SVD basis of X?
> It shrinks the fit along the $j$-th principal direction by $d_j^2/(d_j^2+\lambda)$.
> Low-variance directions (small $d_j$), typically differences between collinear predictors, are shrunk most.

> [!question]- stat-ridge-effective-dof | What are the effective degrees of freedom of ridge?
> $\sum_j d_j^2/(d_j^2+\lambda)$, the trace of the ridge hat matrix.
> It equals $p$ at $\lambda = 0$ and decreases to 0 as $\lambda\to\infty$.

> [!question]- stat-ridge-orthonormal-ridge-lasso | Orthonormal design, OLS coefficients (3, 1, -0.5, 0.2). Ridge with lambda 1 and lasso with lambda 0.8?
> Ridge $(1.5, 0.5, -0.25, 0.1)$; lasso $(2.2, 0.2, 0, 0)$.
> Ridge divides by $1+\lambda$; lasso soft-thresholds, $\text{sign}(\hat\beta)(|\hat\beta|-\lambda)_+$.

> [!question]- stat-ridge-lasso-why-sparse | Why does the lasso produce exact zeros and ridge does not?
> The $\ell_1$ ball has corners on the axes, so the RSS contours usually touch it where some coordinates are zero; the $\ell_2$ ball is smooth.
> Algebraically, the subgradient of $|\beta_j|$ at 0 is $[-1,1]$, so $\hat\beta_j = 0$ whenever $|x_j^\top r|\le\lambda$.

> [!question]- stat-ridge-gaussian-prior | What prior makes ridge a Bayesian estimator, and how does lambda relate to it?
> $\beta\sim N(0,\tau^2I)$ with Gaussian noise $\sigma^2$ gives ridge with $\lambda = \sigma^2/\tau^2$.
> The negative log-posterior is $\frac{1}{2\sigma^2}\text{RSS} + \frac{1}{2\tau^2}\|\beta\|^2$; ridge is the posterior mean and mode.

> [!question]- stat-ridge-lasso-laplace-prior | What is the Bayesian interpretation of the lasso?
> The posterior mode under independent Laplace (double-exponential) priors on the coefficients.
> $-\log p(\beta_j) = |\beta_j|/b + \text{const}$ gives an $\ell_1$ penalty; the posterior mean is not sparse.

> [!question]- stat-ridge-collinear-lasso-picks-one | Two signals have correlation 0.95. How do ridge and lasso treat them?
> Ridge splits weight between them; lasso tends to keep one and drop the other, unstably.
> Ridge shrinks the noisy difference direction most; elastic net adds the $\ell_2$ grouping effect to lasso.

> [!question]- stat-ridge-optimal-shrinkage-scalar | An estimate has t-stat about 1 (beta = SE = 0.5). What shrinkage factor minimises MSE and how much does it help?
> Shrink by $\beta^2/(\beta^2+s^2) = 1/2$; MSE halves from 0.25 to 0.125.
> $\text{MSE}(c) = c^2s^2+(1-c)^2\beta^2$; the optimum $\lambda^* = s^2/\beta^2 = 1$.

> [!question]- stat-ridge-hoerl-kennard | Is there always a ridge penalty that beats OLS on mean squared error?
> Yes, some $\lambda>0$ always has strictly lower total MSE than OLS (Hoerl and Kennard 1970).
> The derivative of MSE with respect to $\lambda$ at 0 is negative: variance falls at first order while squared bias grows at second order.

> [!question]- stat-ridge-standardize-features | Why standardise features before ridge or lasso, and why not penalise the intercept?
> The penalty is not scale-invariant, so unstandardised features are penalised by their units; penalising the intercept shrinks predictions towards 0 instead of $\bar y$.
> Standardise within each training fold only, to avoid leakage.

> [!question]- stat-ridge-lambda-max | Above what penalty is every lasso coefficient zero?
> $\lambda_{\max} = \max_j|x_j^\top y|$ (with centred data, in the $\frac12$RSS convention).
> The KKT condition $|x_j^\top(y - X\cdot0)|\le\lambda$ then holds for all $j$.

> [!question]- stat-ridge-cv-time-series | How do you choose lambda for a return-forecasting model?
> Time-respecting cross-validation (walk-forward or purged and embargoed K-fold) over a log grid, often with the one-SE rule.
> Shuffled CV leaks information through overlapping labels and autocorrelation and picks too small a penalty.

> [!question]- stat-ridge-elastic-net-purpose | When do you use elastic net instead of lasso?
> When predictors are correlated in groups, or $p>n$ and you want more than $n$ features.
> The $\ell_2$ term stabilises selection and makes correlated features enter together; the $\ell_1$ term still zeroes weak ones.

## In this repo and SDE-Interview-Prep

- [Linear Regression and OLS](04-Linear-Regression-OLS.md) for the unpenalised baseline and Gauss-Markov.
- [SVD and Low-Rank Approximation](../03-Linear-Algebra-and-Optimization/03-SVD-and-Low-Rank-Approximation.md) and [PCA and Factor Structure](../03-Linear-Algebra-and-Optimization/05-PCA-and-Factor-Structure.md) for the eigenbasis view.
- [Bayesian Inference](07-Bayesian-Inference.md) for priors and posteriors.
- [Covariance Estimation and Shrinkage](../09-Alpha-Research-and-Portfolio/11-Covariance-Estimation-and-Shrinkage.md) for the same idea applied to covariance matrices.
- [ML Fundamentals and Generalization](../10-Machine-Learning-for-Finance/01-ML-Fundamentals-and-Generalization.md) and [Time-Series Cross-Validation](../10-Machine-Learning-for-Finance/02-Time-Series-Cross-Validation-Purging-Embargo.md) for choosing penalties honestly.

## Further reading

- Hastie, Tibshirani and Friedman, *The Elements of Statistical Learning* (2nd ed.), section 3.4 (ridge, lasso, SVD view, degrees of freedom) and chapter 7 (cross-validation).
- Hastie, Tibshirani and Wainwright, *Statistical Learning with Sparsity*, chapters 2 and 4 (lasso, elastic net).
- Arthur Hoerl and Robert Kennard (1970), "Ridge Regression: Biased Estimation for Nonorthogonal Problems", *Technometrics*.
- Robert Tibshirani (1996), "Regression Shrinkage and Selection via the Lasso", *Journal of the Royal Statistical Society B*.
- Hui Zou and Trevor Hastie (2005), "Regularization and Variable Selection via the Elastic Net", *Journal of the Royal Statistical Society B*.
