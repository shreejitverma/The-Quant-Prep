---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [random-variables-and-distributions]
est_hours: 4
sources: [Casella and Berger - Statistical Inference 2nd ed ch 7 10, Wasserman - All of Statistics ch 6 9, Merton (1980) - On Estimating the Expected Return on the Market - Journal of Financial Economics, Hansen (1982) - Large Sample Properties of Generalized Method of Moments Estimators - Econometrica]
---

# Estimation: MLE and Method of Moments

## TL;DR

- An estimator is a function of the data; judge it by bias, variance and $\text{MSE} = \text{bias}^2 + \text{Var}$, not by unbiasedness alone.
- Method of moments: set sample moments equal to population moments and solve; simple, consistent, often inefficient.
- MLE: maximise $\ell(\theta) = \sum_i \log f(x_i;\theta)$; under regularity it is consistent, asymptotically normal with variance $I_n(\theta)^{-1}$, and invariant ($\widehat{g(\theta)} = g(\hat\theta)$).
- Cramer-Rao: an unbiased estimator of $\theta$ has $\text{Var} \ge 1/I_n(\theta)$, with $I_n = -E[\ell''(\theta)] = n I_1(\theta)$; it fails when the support depends on $\theta$ (uniform, German tank).
- Finance punchline: with daily data, volatility is estimated to a few percent in a year, but the mean return has a standard error equal to the annual volatility over $\sqrt{T}$ years; means are the hard part.

## Learning objectives

- Derive MLEs for common families and state their asymptotic properties.
- Compare bias, variance and mean squared error of estimators.
- Use Fisher information and the Cramer-Rao bound.

## Core concepts

### Estimators and their quality

An estimator $\hat\theta = T(X_1,\dots,X_n)$ is a random variable; its distribution over repeated samples is the sampling distribution.
Bias is $E[\hat\theta]-\theta$, and mean squared error decomposes as

$$
\text{MSE}(\hat\theta) = E[(\hat\theta-\theta)^2] = \text{Var}(\hat\theta) + \text{bias}(\hat\theta)^2 .
$$

Consistency means $\hat\theta \to \theta$ in probability as $n\to\infty$; bias and variance both going to zero is sufficient.
A small bias is often worth a large variance cut, which is the whole idea behind shrinkage ([Regularization](06-Regularization-Ridge-Lasso.md)).

### Method of moments

Match the first $k$ sample moments $\frac1n\sum x_i^j$ to $E_\theta[X^j]$ and solve for the $k$ parameters.
For a Gamma with shape $k$ and scale $s$: $E[X] = ks$ and $\text{Var}(X) = ks^2$, so $\hat s = \hat\sigma^2/\bar x$ and $\hat k = \bar x^2/\hat\sigma^2$.
Method-of-moments estimators are consistent by the law of large numbers plus continuity, but they ignore the shape of the likelihood and can be far from efficient.
The generalisation to more moment conditions than parameters, weighted optimally, is GMM (Hansen 1982), the workhorse of asset-pricing tests.

### Maximum likelihood

The likelihood is $L(\theta) = \prod_i f(x_i;\theta)$ and the log-likelihood is $\ell(\theta) = \sum_i\log f(x_i;\theta)$.
The score is $S(\theta) = \ell'(\theta)$, with $E_\theta[S(\theta)] = 0$ at the true parameter.
Fisher information is

$$
I_n(\theta) = \text{Var}(S(\theta)) = -E[\ell''(\theta)] = n\,I_1(\theta).
$$

Standard results:

| Family | MLE | $I_1(\theta)$ |
| :--- | :--- | :--- |
| Bernoulli($p$) | $\bar x$ | $1/(p(1-p))$ |
| Poisson($\lambda$) | $\bar x$ | $1/\lambda$ |
| Exponential(rate $\lambda$) | $1/\bar x$ | $1/\lambda^2$ |
| Normal($\mu,\sigma^2$) | $\bar x$, $\frac1n\sum(x_i-\bar x)^2$ | $1/\sigma^2$ for $\mu$, $1/(2\sigma^4)$ for $\sigma^2$ |
| Uniform($0,\theta$) | $\max_i x_i$ | not regular |

Under regularity (support free of $\theta$, smooth log-density, true value interior):

$$
\sqrt{n}(\hat\theta_{\text{MLE}}-\theta) \xrightarrow{d} N\big(0, I_1(\theta)^{-1}\big).
$$

In practice the standard error is $1/\sqrt{I_n(\hat\theta)}$, or $1/\sqrt{-\ell''(\hat\theta)}$ (observed information).
Invariance: the MLE of $g(\theta)$ is $g(\hat\theta)$, so the MLE of volatility is the square root of the MLE of variance.
The delta method gives its standard error: $\text{Var}(g(\hat\theta)) \approx g'(\theta)^2\,\text{Var}(\hat\theta)$.
With Gaussian errors, the MLE of regression coefficients is exactly OLS ([Linear Regression and OLS](04-Linear-Regression-OLS.md)).

### Cramer-Rao lower bound

For any unbiased estimator $T$ of $\psi(\theta)$, under the same regularity conditions,

$$
\text{Var}(T) \ge \frac{\psi'(\theta)^2}{I_n(\theta)}.
$$

Proof sketch: $\text{Cov}(T, S) = \psi'(\theta)$ by differentiating $E_\theta[T] = \psi(\theta)$ under the integral, then apply Cauchy-Schwarz.
An estimator attaining the bound is efficient; the MLE attains it asymptotically.
The bound says nothing about biased estimators, and it does not apply when the support depends on $\theta$, where estimators can converge at rate $1/n$ instead of $1/\sqrt n$.

### Why means are hard and volatilities are easy

For iid normal returns with per-period volatility $\sigma$ over $n$ periods, $\text{SE}(\hat\mu) = \sigma/\sqrt n$ and $\text{SE}(\hat\sigma) \approx \sigma/\sqrt{2n}$.
Annualise with $T$ years of data: $\text{SE}(\hat\mu_{\text{ann}}) = \sigma_{\text{ann}}/\sqrt{T}$ regardless of sampling frequency, because the drift over the window depends only on the start and end prices.
The volatility error shrinks with the number of observations, so sampling more often helps (Merton 1980).
This asymmetry is why risk models are trusted far more than expected-return models, and why portfolio optimisers that plug in sample means blow up.

## Worked examples

### Example 1 - exponential inter-trade times

"You observe 100 gaps between trades with mean 2.5 seconds. Model them as exponential. Estimate the rate with a 95% interval."

$\ell(\lambda) = n\log\lambda - \lambda\sum x_i$, so $\ell'(\lambda) = n/\lambda - \sum x_i = 0$ gives $\hat\lambda = 1/\bar x = 0.4$ trades per second.
$I_n(\lambda) = n/\lambda^2$, so $\text{SE} = \hat\lambda/\sqrt n = 0.04$ and the Wald interval is $0.4 \pm 1.96\times0.04 = [0.322, 0.478]$.
The MLE is biased: $n\bar x$ is Gamma($n,\lambda$), so $E[1/\bar x] = \frac{n}{n-1}\lambda$; the unbiased version is $\frac{n-1}{n\bar x} = 0.396$.
The mean gap $\bar x$ is unbiased for $1/\lambda$ and attains its Cramer-Rao bound $1/(n\lambda^2)$, illustrating that unbiasedness is not preserved under nonlinear maps.

### Example 2 - uniform(0, theta): method of moments versus MLE

"$X_1,\dots,X_{10}$ iid uniform on $[0,\theta]$ with $\theta = 1$. Compare the MSE of $2\bar X$, $\max X_i$ and $\frac{11}{10}\max X_i$."

Method of moments: $E[X] = \theta/2$ so $\hat\theta = 2\bar X$, unbiased with variance $4\cdot\frac{\theta^2}{12n} = \frac{\theta^2}{3n} = 0.0333$.
MLE: the likelihood is $\theta^{-n}$ for $\theta\ge\max x_i$ and zero otherwise, so it is maximised at $M = \max x_i$.
$P(M\le m) = (m/\theta)^n$ gives $E[M] = \frac{n}{n+1}\theta$ and $\text{Var}(M) = \frac{n\theta^2}{(n+1)^2(n+2)}$.
$\text{MSE}(M) = \frac{1}{121} + \frac{10}{121\cdot12} = \frac{2\theta^2}{(n+1)(n+2)} = 0.0152$.
The bias-corrected $\frac{n+1}{n}M$ is unbiased with variance $\frac{\theta^2}{n(n+2)} = 0.0083$, four times better than moments.
Its variance is $O(1/n^2)$, below any "Cramer-Rao" rate, which is allowed because the support depends on $\theta$.
A simulation with 400,000 samples reproduces 0.0333, 0.0152 and 0.0084.

### Example 3 - which divisor for the sample variance?

"For normal data with $n = 10$, compare the MSE of $\frac{1}{d}\sum(x_i-\bar x)^2$ for $d = n-1, n, n+1$."

$\sum(x_i-\bar x)^2/\sigma^2 \sim \chi^2_{n-1}$, with mean $n-1$ and variance $2(n-1)$.
So the estimator has mean $\frac{n-1}{d}\sigma^2$ and variance $\frac{2(n-1)}{d^2}\sigma^4$.

| Divisor $d$ | Bias$/\sigma^2$ | Var$/\sigma^4$ | MSE$/\sigma^4$ |
| :--- | :--- | :--- | :--- |
| 9 (unbiased) | 0 | 0.2222 | 0.2222 |
| 10 (MLE) | $-0.1$ | 0.18 | 0.19 |
| 11 | $-0.182$ | 0.1488 | 0.1818 |

$d = n+1$ minimises MSE for normal data; unbiasedness costs variance.

### Example 4 - how long to estimate a mean return versus a volatility

"Daily returns have volatility 1%. With one year of data, what are the standard errors of the annualised mean and the annualised volatility? How many years give a 2% standard error on the mean?"

Annual volatility is $1\%\times\sqrt{252} = 15.87\%$.
$\text{SE}(\hat\mu_{\text{ann}}) = 15.87\%/\sqrt{1} = 15.87\%$: one year says almost nothing about the mean.
$\text{SE}(\hat\sigma)/\sigma = 1/\sqrt{2\cdot252} = 4.45\%$, so annual volatility is known to about $\pm0.71$ percentage points.
For a 2% SE on the mean you need $T = (15.87/2)^2 = 63$ years, and sampling hourly instead of daily would not help at all.

### Example 5 - method of moments for a Gamma, and the German tank problem

"Trade sizes have sample mean 2 lots and sample variance 0.8. Fit a Gamma by moments."

$\hat k = \bar x^2/\hat\sigma^2 = 4/0.8 = 5$ and $\hat s = \hat\sigma^2/\bar x = 0.4$.

"Five captured tanks carry serial numbers with maximum 60 (serials $1,\dots,N$, sampled without replacement). Estimate $N$."

The MLE is $m = 60$, biased low; the minimum-variance unbiased estimator is $m + m/k - 1 = 60 + 12 - 1 = 71$.
The correction adds the average gap between observed serials, the discrete version of the $\frac{n+1}{n}M$ fix above.

## Pitfalls

- Treating unbiasedness as the goal; MSE is what matters for forecasting and position sizing.
- Assuming invariance also preserves unbiasedness: $s^2$ is unbiased for $\sigma^2$ but $s$ is biased low for $\sigma$.
- Quoting Cramer-Rao for models whose support depends on the parameter, or for biased estimators.
- Reporting asymptotic MLE standard errors from small samples or near a boundary (a GARCH persistence near 1, a variance near 0).
- Forgetting that the MLE is only as good as the model: a Gaussian likelihood on fat-tailed returns still gives consistent means (quasi-MLE) but wrong standard errors unless you use the sandwich form.
- Believing higher-frequency sampling sharpens the estimate of the mean return; only a longer calendar span does.
- Maximising a likelihood numerically without checking for multiple local maxima or flat directions.

## Interview questions

> [!question]- stat-mle-exponential-rate-estimate | 100 inter-arrival times have mean 2.5 s. What is the MLE of the exponential rate and its standard error?
> $\hat\lambda = 0.4$ per second with SE $0.04$.
> $\ell = n\log\lambda - \lambda\sum x_i$ gives $\hat\lambda = 1/\bar x$; Fisher information $n/\lambda^2$ gives SE $\hat\lambda/\sqrt n$.

> [!question]- stat-mle-uniform-max-bias | For iid uniform(0, theta), what is the MLE of theta and how do you make it unbiased?
> The MLE is the sample maximum $M$; $\frac{n+1}{n}M$ is unbiased.
> $E[M] = \frac{n}{n+1}\theta$ from $P(M\le m) = (m/\theta)^n$; the likelihood $\theta^{-n}$ is decreasing on $\theta\ge M$.

> [!question]- stat-mle-uniform-mom-vs-mle-variance | For uniform(0, theta), compare the variance of 2 x-bar with that of the unbiased max-based estimator.
> $\theta^2/(3n)$ versus $\theta^2/(n(n+2))$; the max-based one is better by a factor of about $n/3$.
> The max converges at rate $1/n$ because the support depends on $\theta$, so Cramer-Rao does not apply.

> [!question]- stat-mle-normal-variance-divisor | For normal data, which divisor of the sum of squared deviations minimises MSE for sigma squared?
> $n+1$.
> With $\chi^2_{n-1}$ scaling, $\text{MSE}(d) = \sigma^4[((n-1)/d-1)^2 + 2(n-1)/d^2]$, minimised at $d = n+1$; the MLE uses $n$, the unbiased estimator $n-1$.

> [!question]- stat-mle-bias-variance-mse | State the bias-variance decomposition of mean squared error.
> $\text{MSE} = \text{Var}(\hat\theta) + \text{bias}^2$.
> Expand $E[(\hat\theta - E\hat\theta + E\hat\theta - \theta)^2]$; the cross term has zero mean.

> [!question]- stat-mle-invariance-property | What is the MLE of volatility if the MLE of variance is 0.0004, and is it unbiased?
> $0.02$; invariance gives $\hat\sigma = \sqrt{\hat\sigma^2}$, but it is biased.
> The MLE of $g(\theta)$ is $g(\hat\theta)$, while Jensen makes $E[\sqrt{V}] < \sqrt{E[V]}$.

> [!question]- stat-mle-fisher-information-definition | Define Fisher information and give it for a Bernoulli(p) sample of size n.
> $I_n(\theta) = \text{Var}(\ell'(\theta)) = -E[\ell''(\theta)]$; for Bernoulli it is $n/(p(1-p))$.
> So $\text{SE}(\hat p) = \sqrt{p(1-p)/n}$, which is $0.0458$ for $p = 0.3$, $n = 100$.

> [!question]- stat-mle-cramer-rao-statement | State the Cramer-Rao bound and when it fails.
> For unbiased $T$ of $\theta$, $\text{Var}(T)\ge 1/I_n(\theta)$.
> It needs regularity (support independent of $\theta$, differentiation under the integral) and says nothing about biased estimators.

> [!question]- stat-mle-asymptotic-normality | What is the asymptotic distribution of the MLE?
> $\sqrt n(\hat\theta-\theta)\to N(0, I_1(\theta)^{-1})$ under regularity.
> Taylor-expand the score around $\theta$: the score is a sum of iid mean-zero terms (CLT) and $-\ell''/n\to I_1$ (LLN).

> [!question]- stat-mle-mean-vs-vol-estimation | Daily vol is 1%. With one year of data, what are the SEs of the annualised mean and annualised vol?
> About 15.9% for the mean and 0.71 percentage points for the vol.
> $\text{SE}(\hat\mu_{\text{ann}}) = \sigma_{\text{ann}}/\sqrt T$; $\text{SE}(\hat\sigma)/\sigma = 1/\sqrt{2n}$ with $n = 252$.

> [!question]- stat-mle-years-for-mean-precision | Annual vol is 15.87%. How many years of data give a 2% standard error on the mean return?
> 63 years.
> $\sigma_{\text{ann}}/\sqrt T = 2\%$ gives $T = 7.94^2$; sampling frequency does not matter for the mean.

> [!question]- stat-mle-method-of-moments-gamma | Sample mean 2, sample variance 0.8. Fit a Gamma(shape k, scale s) by method of moments.
> $k = 5$, $s = 0.4$.
> Solve $ks = 2$ and $ks^2 = 0.8$: $s = 0.8/2$, $k = 2/0.4$.

> [!question]- stat-mle-german-tank | Five serial numbers are observed with maximum 60, sampled without replacement from 1 to N. Unbiased estimate of N?
> 71.
> $m + m/k - 1 = 60 + 12 - 1$: add the average gap between observed serials to the maximum.

> [!question]- stat-mle-gaussian-regression-is-ols | Why is OLS the maximum likelihood estimator in a linear model?
> With iid $N(0,\sigma^2)$ errors, $\ell(\beta) = -\frac{1}{2\sigma^2}\|y-X\beta\|^2 + \text{const}$.
> Maximising it over $\beta$ is minimising the residual sum of squares; the variance MLE is then $\text{RSS}/n$.

## In this repo and SDE-Interview-Prep

- [Random Variables and Distributions](../01-Probability/03-Random-Variables-and-Distributions.md) for the families used here.
- [Confidence Intervals and Sampling](02-Confidence-Intervals-and-Sampling.md) turns these standard errors into intervals.
- [Linear Regression and OLS](04-Linear-Regression-OLS.md) is Gaussian MLE for a linear mean.
- [Covariance Estimation and Shrinkage](../09-Alpha-Research-and-Portfolio/11-Covariance-Estimation-and-Shrinkage.md) for why sample moments need shrinking in high dimension.

## Further reading

- Casella and Berger, *Statistical Inference* (2nd ed.), chapter 7 (point estimation, Cramer-Rao) and chapter 10 (asymptotics).
- Larry Wasserman, *All of Statistics*, chapter 6 (estimation basics) and chapter 9 (MLE, Fisher information, delta method).
- Robert Merton (1980), "On Estimating the Expected Return on the Market", *Journal of Financial Economics*.
- Lars Peter Hansen (1982), "Large Sample Properties of Generalized Method of Moments Estimators", *Econometrica*.
