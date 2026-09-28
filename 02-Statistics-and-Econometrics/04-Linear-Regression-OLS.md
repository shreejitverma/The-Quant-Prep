---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [estimation-mle-and-method-of-moments, vectors-matrices-and-linear-maps]
est_hours: 6
sources: [Hastie Tibshirani and Friedman - The Elements of Statistical Learning 2nd ed ch 3, Wasserman - All of Statistics ch 13, Greene - Econometric Analysis ch 2 3 4, Angrist and Pischke - Mostly Harmless Econometrics ch 3, Wooldridge - Introductory Econometrics ch 3]
---

# Linear Regression and OLS

## TL;DR

- $\hat\beta = (X^\top X)^{-1}X^\top y$ solves the normal equations $X^\top(y-X\hat\beta) = 0$: residuals are orthogonal to every regressor, and $\hat y = Hy$ is the orthogonal projection onto the column space of $X$.
- With $E[\varepsilon\mid X] = 0$ and $\text{Var}(\varepsilon\mid X) = \sigma^2 I$: $\text{Var}(\hat\beta\mid X) = \sigma^2(X^\top X)^{-1}$, $s^2 = \text{RSS}/(n-p)$ is unbiased, and OLS is BLUE (Gauss-Markov).
- Omitted variable bias: the short-regression slope converges to $\beta_1 + \beta_2\delta$, where $\delta$ is the slope of the omitted $x_2$ on $x_1$.
- $R^2$ never falls when a regressor is added; a pure-noise regressor raises it by $(1-R^2)/(n-p)$ on average, and adjusted $R^2$ rises only if the new $|t| > 1$.
- $\beta_{y\mid x} = \rho\sigma_y/\sigma_x$ and $\beta_{x\mid y} = \rho\sigma_x/\sigma_y$, so $\beta_{y\mid x}\beta_{x\mid y} = \rho^2 = R^2$, not 1.
- Duplicating every row leaves $\hat\beta$ and $R^2$ unchanged but shrinks standard errors by about $\sqrt2$: fake precision.

## Learning objectives

- Derive the OLS estimator in matrix form and its sampling distribution.
- State the Gauss-Markov assumptions and what breaks when each fails.
- Interpret coefficients, R-squared and the effect of adding regressors.
- Explain omitted variable bias and regression to the mean.
- Answer 'regress y on x vs x on y' and 'duplicate the data' interview questions.

## Core concepts

### Matrix derivation

Model $y = X\beta + \varepsilon$ with $X$ of size $n\times p$ (intercept column included) and full column rank.
Minimise $\text{RSS}(\beta) = (y-X\beta)^\top(y-X\beta)$.
The gradient is $-2X^\top(y-X\beta)$; setting it to zero gives the normal equations

$$
X^\top X\hat\beta = X^\top y \quad\Longrightarrow\quad \hat\beta = (X^\top X)^{-1}X^\top y .
$$

The Hessian $2X^\top X$ is positive definite, so this is the unique minimum.
The hat matrix $H = X(X^\top X)^{-1}X^\top$ is symmetric and idempotent; $\hat y = Hy$ and $e = (I-H)y$.
Consequences: $X^\top e = 0$, so with an intercept the residuals sum to zero and the fitted line passes through $(\bar x,\bar y)$.
Simple regression: $\hat\beta_1 = \text{Cov}(x,y)/\text{Var}(x) = \rho\,\sigma_y/\sigma_x$ and $\hat\beta_0 = \bar y - \hat\beta_1\bar x$.
Numerically, solve by QR or `np.linalg.lstsq`, never by forming $(X^\top X)^{-1}$ explicitly ([Numerical Linear Algebra](../03-Linear-Algebra-and-Optimization/06-Numerical-Linear-Algebra.md)).

### Sampling distribution

Substituting $y = X\beta+\varepsilon$ gives $\hat\beta = \beta + (X^\top X)^{-1}X^\top\varepsilon$.
If $E[\varepsilon\mid X]=0$ then $E[\hat\beta\mid X] = \beta$.
If also $\text{Var}(\varepsilon\mid X) = \sigma^2 I$ then

$$
\text{Var}(\hat\beta\mid X) = \sigma^2(X^\top X)^{-1}, \qquad s^2 = \frac{e^\top e}{n-p},\quad E[s^2] = \sigma^2 ,
$$

because $E[e^\top e] = \sigma^2\,\text{tr}(I-H) = \sigma^2(n-p)$.
With normal errors, $\hat\beta\sim N(\beta,\sigma^2(X^\top X)^{-1})$, $(n-p)s^2/\sigma^2\sim\chi^2_{n-p}$ independently, and $t_j = \hat\beta_j/\text{SE}_j\sim t_{n-p}$ under $\beta_j = 0$.
Without normality the same holds asymptotically.
In simple regression $\text{SE}(\hat\beta_1) = s/\sqrt{\sum(x_i-\bar x)^2}$: spread-out regressors give precise slopes.

### Gauss-Markov and what breaks

| Assumption | If it fails |
| :--- | :--- |
| Linear in parameters, correct specification | Coefficients estimate the best linear approximation, not a causal or structural effect |
| Full column rank | Perfect collinearity: $\beta$ not identified; near-collinearity: huge variances |
| Strict exogeneity $E[\varepsilon\mid X]=0$ | Biased and inconsistent (omitted variables, measurement error, simultaneity, look-ahead) |
| Spherical errors $\text{Var}(\varepsilon\mid X) = \sigma^2I$ | Still unbiased, but not efficient and the usual SEs are wrong: use White or Newey-West ([Regression Diagnostics](05-Regression-Diagnostics-and-Robust-Inference.md)) or GLS |
| Normal errors (not needed for BLUE) | Exact $t$ and $F$ tests become approximate |

Gauss-Markov theorem: under the first four, OLS has the smallest variance among linear unbiased estimators (BLUE).
Proof: any other linear unbiased $\tilde\beta = Cy$ with $CX = I$ can be written $C = (X^\top X)^{-1}X^\top + D$ with $DX = 0$, and then $\text{Var}(\tilde\beta) = \sigma^2(X^\top X)^{-1} + \sigma^2DD^\top$.
Biased estimators such as ridge can beat it on MSE ([Regularization](06-Regularization-Ridge-Lasso.md)).

### Frisch-Waugh-Lovell and partialling out

The coefficient on $x_1$ in a multiple regression equals the slope from regressing $y$ on the residual of $x_1$ after regressing $x_1$ on the other regressors.
A multiple-regression coefficient is the effect of the part of $x_1$ not explained by the controls.
This is what "neutralising a signal against industry and style factors" does before measuring its return.

### Omitted variable bias

True model $y = \beta_0 + \beta_1x_1 + \beta_2x_2 + \varepsilon$, but you regress $y$ on $x_1$ only.
With $\delta = \text{Cov}(x_1,x_2)/\text{Var}(x_1)$,

$$
\text{plim}\,\tilde\beta_1 = \beta_1 + \beta_2\,\delta .
$$

The bias vanishes only if $\beta_2 = 0$ or $x_1$ and $x_2$ are uncorrelated.
Finance example: a signal that loads on market beta will show "alpha" in a regression that omits the market factor.
Measurement error is a special case: if $x^* = x + u$ with noise variance $\sigma_u^2$, the slope is attenuated to $\beta\,\sigma_x^2/(\sigma_x^2+\sigma_u^2)$.

### R-squared behaviour

$R^2 = 1 - \text{RSS}/\text{TSS}$ is the share of variance explained, and equals $\text{corr}(y,\hat y)^2$ when an intercept is included; in simple regression it is $\rho_{xy}^2$.
Adding a regressor enlarges the column space, so RSS cannot increase and $R^2$ cannot fall.
If the new regressor is independent noise, its partial $R^2$ has a Beta$(\frac12,\frac{n-p-1}{2})$ distribution with mean $1/(n-p)$, where $p$ counts the columns before adding it, so

$$
E[\Delta R^2] = \frac{1-R^2}{n-p}.
$$

Adjusted $R^2 = 1 - (1-R^2)\frac{n-1}{n-k}$ with $k$ columns; it rises exactly when the added regressor has $|t| > 1$.
In return forecasting an out-of-sample $R^2$ of 1% can be economically large, and in-sample $R^2$ says nothing about out-of-sample fit.

### y on x versus x on y, and regression to the mean

$\beta_{y\mid x} = \rho\sigma_y/\sigma_x$ and $\beta_{x\mid y} = \rho\sigma_x/\sigma_y$.
Their product is $\rho^2$, both have the sign of $\rho$, and $\beta_{x\mid y} = 1/\beta_{y\mid x}$ only when $|\rho| = 1$.
OLS minimises vertical distances; the two regressions minimise different errors, and total least squares (the first principal component) sits between them.
In standardised units the prediction is $\hat z_y = \rho z_x$: an extreme $x$ predicts a less extreme $y$, which is regression to the mean.
Last year's top-decile fund or signal is expected to be closer to average next year even with no change in skill, simply because part of its outperformance was noise.

## Worked examples

### Example 1 - OLS by hand

"Fit $y$ on $x$ for $x = (1,2,3,4,5)$, $y = (2,4,5,4,5)$. Slope, intercept, $R^2$ and slope $t$-stat?"

$\bar x = 3$, $\bar y = 4$, $S_{xy} = \sum(x-\bar x)(y-\bar y) = 4+0+0+0+2 = 6$, $S_{xx} = 10$, $S_{yy} = 6$.
$\hat\beta_1 = 0.6$ and $\hat\beta_0 = 4 - 1.8 = 2.2$.
Explained sum of squares $\hat\beta_1^2S_{xx} = 3.6$, so $R^2 = 3.6/6 = 0.6$ and $\text{RSS} = 2.4$.
$s^2 = 2.4/3 = 0.8$, $\text{SE}(\hat\beta_1) = \sqrt{0.8/10} = 0.283$, $t = 2.12$ on 3 degrees of freedom, two-sided $p = 0.124$.
Regressing $x$ on $y$ gives slope $S_{xy}/S_{yy} = 1.0$, and $0.6\times1.0 = 0.6 = R^2$ as promised.

### Example 2 - stock beta both ways

"A stock has volatility 30%, the market 15%, correlation 0.6. What are the beta of the stock on the market and of the market on the stock?"

$\beta_{\text{stock}\mid\text{mkt}} = 0.6\times0.30/0.15 = 1.2$.
$\beta_{\text{mkt}\mid\text{stock}} = 0.6\times0.15/0.30 = 0.3$, not $1/1.2 = 0.83$.
The product $1.2\times0.3 = 0.36 = \rho^2$ is the share of the stock's variance explained by the market.
Hedging the stock with 1.2 units of market minimises the hedged variance, leaving $1-0.36 = 64\%$ of the variance as idiosyncratic.

### Example 3 - omitted variable bias in a signal regression

"Returns follow $r = 0.5\,s + 0.3\,m + \varepsilon$, where $s$ is your signal and $m$ the market factor, and the slope of $m$ on $s$ is 0.4. You regress $r$ on $s$ alone. What slope do you get?"

$0.5 + 0.3\times0.4 = 0.62$, so 24% of the apparent signal loading is disguised market exposure.
Controlling for $m$ (or residualising $s$ on $m$, by Frisch-Waugh-Lovell) recovers 0.5.
If instead the omitted variable were negatively related, the signal would look weaker than it is; the sign of $\beta_2\delta$ sets the direction.

### Example 4 - duplicating the data

"You accidentally stack the data set on itself: $n = 50$ becomes 100 rows, $p = 2$. What happens?"

$X^\top X$ and $X^\top y$ both double, so $\hat\beta$ is unchanged, and RSS and TSS both double, so $R^2$ is unchanged.
$s^2_{\text{new}} = 2\,\text{RSS}/(2n-p)$ and $(X^\top X)^{-1}$ halves, so $\text{SE}_{\text{new}}/\text{SE}_{\text{old}} = \sqrt{(n-p)/(2n-p)} = \sqrt{48/98} = 0.700$.
Every $t$-stat is inflated by $1.43$ with no new information.
The same thing happens more subtly with overlapping returns or with a cross-section of highly correlated stocks treated as independent.

```python
import numpy as np
rng = np.random.default_rng(0)
x = rng.normal(size=50); y = 0.3 * x + rng.normal(size=50)
X = np.c_[np.ones(50), x]

def ols_se(X, y):
    beta, rss, *_ = np.linalg.lstsq(X, y, rcond=None)
    s2 = rss[0] / (len(y) - X.shape[1])
    return beta, np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))

b1, se1 = ols_se(X, y)
b2, se2 = ols_se(np.r_[X, X], np.r_[y, y])
print(np.allclose(b1, b2), se2 / se1)   # True [0.6999 0.6999]
```

### Example 5 - adding a noise regressor

"A regression with an intercept and two regressors on $n = 100$ has $R^2 = 0.10$. You add an independent random regressor. What happens to $R^2$ and adjusted $R^2$?"

$E[\Delta R^2] = (1-0.10)/(100-3) = 0.0093$, so $R^2$ rises to about $0.109$ on average and never falls.
Adjusted $R^2$ before: $1 - 0.9\times99/97 = 0.0814$; after, at the average increase: $1 - 0.8907\times99/96 = 0.0814$, unchanged on average, because the expected increase corresponds to $|t| = 1$ exactly.
A simulation of 20,000 draws gives a mean partial $R^2$ of $0.0103$ versus the theoretical $1/97 = 0.0103$.
The other coefficients move slightly and their SEs rise slightly, since one degree of freedom is spent.

## Pitfalls

- Reading a coefficient as causal when exogeneity is doubtful; OLS gives the best linear predictor, not the effect of an intervention.
- Inverting $\beta_{y\mid x}$ to get $\beta_{x\mid y}$; hedge ratios and pairs-trading spreads depend on which variable is on the left.
- Trusting $t$-stats from overlapping, autocorrelated or heteroskedastic residuals; the point estimate is fine, the SE is not.
- Choosing models by in-sample $R^2$, which rewards every added regressor.
- Dropping an "insignificant" control that is correlated with the regressor of interest, and so introducing omitted variable bias.
- Using a noisy regressor (estimated betas, noisy signals) and not expecting attenuation towards zero.
- Forgetting the intercept, which makes $R^2$ uncentred and breaks the residuals-sum-to-zero property.
- Computing $(X^\top X)^{-1}$ explicitly on ill-conditioned data instead of using QR or SVD.

## Interview questions

> [!question]- stat-ols-normal-equations-derivation | Derive the OLS estimator in matrix form.
> $\hat\beta = (X^\top X)^{-1}X^\top y$.
> Differentiate $(y-X\beta)^\top(y-X\beta)$ to get $-2X^\top(y-X\beta) = 0$; $X^\top X$ is positive definite when $X$ has full column rank, so this is the unique minimum.

> [!question]- stat-ols-sampling-variance | What is the variance of the OLS estimator and the unbiased estimator of sigma squared?
> $\text{Var}(\hat\beta\mid X) = \sigma^2(X^\top X)^{-1}$ and $s^2 = \text{RSS}/(n-p)$.
> $\hat\beta-\beta = (X^\top X)^{-1}X^\top\varepsilon$; $E[\text{RSS}] = \sigma^2\text{tr}(I-H) = \sigma^2(n-p)$.

> [!question]- stat-ols-gauss-markov-assumptions | State the Gauss-Markov assumptions and the conclusion.
> Linearity, full rank, $E[\varepsilon\mid X] = 0$, $\text{Var}(\varepsilon\mid X) = \sigma^2I$; then OLS is BLUE.
> Normality is not required; it only makes finite-sample $t$ and $F$ tests exact.

> [!question]- stat-ols-heteroskedasticity-consequence | What happens to OLS if errors are heteroskedastic?
> Coefficients remain unbiased and consistent, but OLS is no longer efficient and the usual SEs are wrong.
> Use White (or Newey-West with autocorrelation) standard errors, or GLS if the variance structure is known.

> [!question]- stat-ols-y-on-x-vs-x-on-y | Is the slope of x on y the reciprocal of the slope of y on x?
> No: $\beta_{y\mid x} = \rho\sigma_y/\sigma_x$ and $\beta_{x\mid y} = \rho\sigma_x/\sigma_y$.
> Their product is $\rho^2$, so they are reciprocal only when $|\rho| = 1$; OLS minimises vertical errors, which differ in the two regressions.

> [!question]- stat-ols-product-of-slopes-r2 | Regressing y on x gives slope 0.5, x on y gives slope 0.8. What are R squared and the correlation?
> $R^2 = 0.4$ and $\rho = +\sqrt{0.4}\approx0.632$.
> $\beta_{y\mid x}\beta_{x\mid y} = \rho^2$, and both slopes share the sign of $\rho$.

> [!question]- stat-ols-impossible-slope-pair | Can y on x have slope 2 while x on y has slope 0.6?
> No.
> The product would be $\rho^2 = 1.2 > 1$; slopes of opposite signs are impossible too.

> [!question]- stat-ols-stock-beta-from-vols | Stock vol 30%, market vol 15%, correlation 0.6. Beta of stock on market, and market on stock?
> 1.2 and 0.3.
> $\rho\sigma_y/\sigma_x$ each way; product $0.36 = R^2$.

> [!question]- stat-ols-duplicate-data | You duplicate every row of a regression data set. What happens to the coefficients, R squared and standard errors?
> Coefficients and $R^2$ unchanged; SEs shrink by $\sqrt{(n-p)/(2n-p)}\approx1/\sqrt2$, so $t$-stats grow by about 1.41.
> $X^\top X$, $X^\top y$, RSS and TSS all double; the degrees of freedom claim information that is not there.

> [!question]- stat-ols-noise-regressor-r2 | You add a pure-noise regressor. What happens to R squared and adjusted R squared?
> $R^2$ weakly rises, by $(1-R^2)/(n-p)$ on average; adjusted $R^2$ rises only if the new $|t| > 1$.
> The column space grows so RSS cannot rise; the noise partial $R^2$ is Beta$(1/2,(n-p-1)/2)$ with mean $1/(n-p)$.

> [!question]- stat-ols-omitted-variable-bias | State the omitted variable bias formula.
> $\text{plim}\,\tilde\beta_1 = \beta_1 + \beta_2\delta$, with $\delta$ the slope of the omitted $x_2$ on $x_1$.
> Substitute the true model into the short-regression formula; bias vanishes if $\beta_2 = 0$ or $\text{Cov}(x_1,x_2) = 0$.

> [!question]- stat-ols-ovb-signal-market | True model r = 0.5 s + 0.3 m + e, and the slope of m on s is 0.4. What slope do you get regressing r on s alone?
> 0.62.
> $0.5 + 0.3\times0.4$: part of the apparent signal is market exposure.

> [!question]- stat-ols-attenuation-bias | Your regressor is measured with noise whose variance equals the true regressor's variance. What happens to the slope?
> It is halved in the limit.
> Errors-in-variables: $\text{plim}\,\hat\beta = \beta\,\sigma_x^2/(\sigma_x^2+\sigma_u^2)$.

> [!question]- stat-ols-regression-to-mean | Explain regression to the mean with a finance example.
> In standard units the best linear prediction is $\hat z_y = \rho z_x$ with $|\rho|<1$, so extremes are followed by less extreme values.
> Top-decile funds or signals partly owe their rank to noise, which does not repeat, so their next-period performance is expected to be closer to average.

> [!question]- stat-ols-fwl-theorem | State the Frisch-Waugh-Lovell theorem and a quant use of it.
> The coefficient on $x_1$ in a multiple regression equals the slope of $y$ on the residuals of $x_1$ regressed on the other regressors.
> It justifies neutralising a signal against factor exposures before measuring its return.

> [!question]- stat-ols-hand-fit | Fit y on x for x = 1..5, y = (2,4,5,4,5). Slope, intercept and R squared?
> Slope 0.6, intercept 2.2, $R^2 = 0.6$.
> $S_{xy} = 6$, $S_{xx} = 10$, $S_{yy} = 6$; $R^2 = S_{xy}^2/(S_{xx}S_{yy})$.

> [!question]- stat-ols-residual-properties | With an intercept, what are the sum of residuals and their correlation with each regressor and with the fitted values?
> All zero.
> The normal equations say $X^\top e = 0$, and $\hat y$ is a linear combination of the columns of $X$.

## In this repo and SDE-Interview-Prep

- [Estimation: MLE and Method of Moments](01-Estimation-MLE-and-Method-of-Moments.md): OLS is the Gaussian MLE.
- [Vectors, Matrices and Linear Maps](../03-Linear-Algebra-and-Optimization/01-Vectors-Matrices-and-Linear-Maps.md) for projections, and [Numerical Linear Algebra](../03-Linear-Algebra-and-Optimization/06-Numerical-Linear-Algebra.md) for QR solves.
- [Regression Diagnostics and Robust Inference](05-Regression-Diagnostics-and-Robust-Inference.md) for robust standard errors and influential points.
- [Regularization: Ridge, Lasso and Elastic Net](06-Regularization-Ridge-Lasso.md) for when OLS variance is too high.
- [Cross-Sectional Factor Models](../09-Alpha-Research-and-Portfolio/04-Cross-Sectional-Factor-Models.md) for factor regressions in practice.

## Further reading

- Hastie, Tibshirani and Friedman, *The Elements of Statistical Learning* (2nd ed.), chapter 3 (linear regression, Gauss-Markov, successive orthogonalisation).
- Larry Wasserman, *All of Statistics*, chapter 13.
- William Greene, *Econometric Analysis*, chapters 2 to 4 (assumptions, OLS algebra, finite-sample properties).
- Joshua Angrist and Jorn-Steffen Pischke, *Mostly Harmless Econometrics*, chapter 3 (regression as best linear approximation, omitted variable bias).
- Jeffrey Wooldridge, *Introductory Econometrics*, chapter 3 (multiple regression, omitted variable bias).
