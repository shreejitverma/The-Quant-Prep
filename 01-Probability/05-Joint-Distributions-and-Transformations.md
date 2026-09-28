---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [expectation-variance-and-linearity]
est_hours: 4
sources: [Blitzstein and Hwang - Introduction to Probability 2nd ed ch 7-8, Casella and Berger - Statistical Inference 2nd ed ch 4, Zhou - A Practical Guide to Quantitative Finance Interviews ch 4]
---

# Joint Distributions and Transformations

## TL;DR

- Marginal: integrate out the other variable; conditional: $f_{Y\mid X}(y\mid x) = f_{X,Y}(x,y)/f_X(x)$; independence means the density factorises on a rectangular (product) support.
- Change of variables: $f_Y(y) = f_X(x)\,\lvert dx/dy\rvert$ summed over preimages; in several dimensions multiply by $\lvert\det\partial(x,y)/\partial(u,v)\rvert$.
- Sum of independent variables: convolution $f_{X+Y}(s) = \int f_X(x)f_Y(s-x)\,dx$; two uniforms give a triangle.
- Bivariate normal: $Y\mid X=x \sim N\big(\mu_Y + \rho\frac{\sigma_Y}{\sigma_X}(x-\mu_X),\ \sigma_Y^2(1-\rho^2)\big)$; the slope $\rho\sigma_Y/\sigma_X$ is the regression coefficient and the hedge ratio.
- $P(X>0, Y>0) = \frac14 + \frac{\arcsin\rho}{2\pi}$ for standard bivariate normal.
- Zero correlation does not imply independence ($X$ and $X^2$); it does for jointly normal variables, but two normal marginals need not be jointly normal.

## Learning objectives

- Move between joint, marginal and conditional densities.
- Apply the change-of-variables formula and the convolution for sums.
- Work with the bivariate normal: conditional mean and variance, regression interpretation.
- Explain why zero correlation does not imply independence, with a counterexample.

## Core concepts

### Joint, marginal and conditional

For a continuous pair, $P((X,Y)\in A) = \iint_A f_{X,Y}(x,y)\,dx\,dy$.
Marginal: $f_X(x) = \int f_{X,Y}(x,y)\,dy$.
Conditional: $f_{Y\mid X}(y\mid x) = f_{X,Y}(x,y)/f_X(x)$, a density in $y$ for each fixed $x$.
Bayes for densities: $f_{X\mid Y}(x\mid y) \propto f_{Y\mid X}(y\mid x)f_X(x)$, the basis of [Bayesian Inference](../02-Statistics-and-Econometrics/07-Bayesian-Inference.md).

Independence: $f_{X,Y}(x,y) = f_X(x)f_Y(y)$ for all $x,y$.
Practical test: the joint density factors as $g(x)h(y)$ and the support is a product set.
A constant density on a triangle does not factor once the indicator of the support is included, so its coordinates are dependent.

### One-dimensional transformations

For $Y = g(X)$ with $g$ strictly monotone and differentiable,

$$
f_Y(y) = f_X\big(g^{-1}(y)\big)\left|\frac{d}{dy}g^{-1}(y)\right|.
$$

If $g$ is not monotone, sum over all preimages, or go through the CDF.
Examples:

- Lognormal: $Y = e^X$ with $X\sim N(\mu,\sigma^2)$ gives $f_Y(y) = f_X(\ln y)/y$ for $y>0$.
- Square of a standard normal: $P(Z^2\le y) = P(-\sqrt y\le Z\le\sqrt y)$, so $f(y) = \frac{1}{\sqrt{2\pi y}}e^{-y/2}$, the $\chi^2_1$ density.
- Location-scale: $Y = a+bX$ gives $f_Y(y) = f_X((y-a)/b)/\lvert b\rvert$.

### Multivariate change of variables

If $(U,V) = T(X,Y)$ is one-to-one and differentiable with inverse $(x(u,v), y(u,v))$,

$$
f_{U,V}(u,v) = f_{X,Y}\big(x(u,v),y(u,v)\big)\left|\det\frac{\partial(x,y)}{\partial(u,v)}\right|.
$$

Polar coordinates for iid standard normals: $x = r\cos\theta$, $y = r\sin\theta$, Jacobian $r$, so

$$
f_{R,\Theta}(r,\theta) = \frac{1}{2\pi}e^{-r^2/2}\,r,
$$

which factorises: $\Theta\sim U(0,2\pi)$ independent of $R$, and $R^2\sim\text{Exp}(1/2)$ (mean 2).
This gives $\int e^{-x^2/2}dx = \sqrt{2\pi}$ and the Box-Muller sampler $Z = \sqrt{-2\ln U_1}\cos(2\pi U_2)$.
For linear maps $\mathbf Y = A\mathbf X + \mathbf b$: $E[\mathbf Y] = AE[\mathbf X]+\mathbf b$ and $\text{Cov}(\mathbf Y) = A\,\Sigma\,A^\top$, the formula behind every portfolio variance (see [Mean-Variance Portfolio Construction](../09-Alpha-Research-and-Portfolio/10-Mean-Variance-Portfolio-Construction.md)).

### Sums: convolution

For independent $X$ and $Y$, $f_{X+Y}(s) = \int f_X(x)f_Y(s-x)\,dx$ (discrete: $P(X+Y=s) = \sum_x P(X=x)P(Y=s-x)$).
Two $U(0,1)$: $f(s) = s$ on $[0,1]$ and $2-s$ on $[1,2]$, the triangle.
Two Exp$(\lambda)$: $\int_0^s\lambda e^{-\lambda x}\lambda e^{-\lambda(s-x)}dx = \lambda^2 s e^{-\lambda s}$, which is Gamma$(2,\lambda)$.
Independent normals: normal with added means and variances.
Convolutions become products under generating functions, the subject of [Generating Functions](07-Generating-Functions.md).

### The bivariate normal

Construct it: with $X, Z$ iid $N(0,1)$, set $Y = \rho X + \sqrt{1-\rho^2}\,Z$; then $\text{Var}(Y)=1$ and $\text{Corr}(X,Y) = \rho$.
Scaling to general means and variances gives

$$
Y\mid X=x\ \sim\ N\Big(\mu_Y + \rho\frac{\sigma_Y}{\sigma_X}(x-\mu_X),\ \ \sigma_Y^2(1-\rho^2)\Big).
$$

- The conditional mean is linear in $x$ with slope $\beta = \rho\sigma_Y/\sigma_X = \text{Cov}(X,Y)/\text{Var}(X)$, the OLS slope and the minimum-variance hedge ratio.
- The conditional variance does not depend on $x$; the fraction of variance explained is $\rho^2$.
- Regression to the mean: in standard units the predicted $Y$ is $\rho$ times the observed $X$, so extreme observations are followed by less extreme predictions.
- Any linear combination of jointly normal variables is normal, and for jointly normal variables uncorrelated means independent.

Orthant probability (Sheppard): for standard bivariate normal with correlation $\rho$, $P(X>0,Y>0) = \frac14 + \frac{\arcsin\rho}{2\pi}$.
Proof: in polar form $X = R\cos\theta$ and $Y = R\sin(\theta+\varphi)$ with $\sin\varphi = \rho$, and $\theta$ is uniform; $X>0$ and $Y>0$ is an arc of length $\pi/2+\varphi$, giving $(\pi/2+\arcsin\rho)/(2\pi)$.

### Correlation versus dependence

Correlation measures only linear association.

- $X\sim U(-1,1)$ and $Y = X^2$: $\text{Cov}(X,Y) = E[X^3] = 0$, but $Y$ is a function of $X$.
- $X\sim N(0,1)$, $S = \pm1$ with probability $1/2$ independent of $X$, $W = SX$: $W$ is $N(0,1)$ and $\text{Cov}(X,W) = E[S]E[X^2] = 0$, but $\lvert W\rvert = \lvert X\rvert$.
  $X+W$ equals 0 with probability $1/2$, so $(X,W)$ is not bivariate normal: normal marginals do not make a normal pair.
The dependence that correlation misses is what copulas and tail-dependence measures are for; it matters most in stress, when correlations of normal times break down.

## Worked examples

### Example 1 - sum of two uniforms

"$U,V$ iid $U(0,1)$. What is $P(U+V < 1.5)$?"

Draw the unit square; the complement $\{U+V\ge1.5\}$ is the corner triangle with legs $0.5$, area $0.5^2/2 = 1/8$.
So $P = 7/8$.
The density of $U+V$ is the triangle $f(s) = \min(s, 2-s)$ on $[0,2]$; integrating it gives the same answer and is the answer if they ask for the distribution.

### Example 2 - product of two uniforms

"$U,V$ iid $U(0,1)$. What is $P(UV\le\tfrac12)$?"

Condition on $U=u$: $P(V\le t/u) = \min(1, t/u)$.
So $P(UV\le t) = \int_0^t 1\,du + \int_t^1\frac tu\,du = t - t\ln t$.
At $t=1/2$: $\tfrac12 + \tfrac12\ln2\approx0.847$.
Differentiating gives the density $-\ln t$ on $(0,1)$; equivalently $-\ln(UV)$ is Gamma(2,1), a sum of two Exp(1).

### Example 3 - conditional forecast and hedge ratio

"Daily returns of X and Y are bivariate normal, zero mean, $\sigma_X = 2\%$, $\sigma_Y = 3\%$, $\rho = 0.6$. X is up 4% today. What is your forecast for Y, how uncertain is it, and what is the hedge ratio?"

X moved $+2\sigma_X$, so the conditional mean of Y is $\rho\cdot2\sigma_Y = 0.6\cdot2\cdot3\% = 3.6\%$.
Conditional standard deviation: $3\%\sqrt{1-0.36} = 2.4\%$, the same whatever X did.
$P(Y>0\mid X=4\%) = \Phi(3.6/2.4) = \Phi(1.5)\approx0.933$.
Hedge ratio: $\beta = \rho\sigma_Y/\sigma_X = 0.9$ units of X per unit of Y, and hedging removes $\rho^2 = 36\%$ of Y's variance, so the residual volatility is 2.4%.

### Example 4 - both positive

"Two standard normals have correlation $0.5$. What is the probability both are positive?"

Sheppard's formula: $\frac14 + \frac{\arcsin(0.5)}{2\pi} = \frac14 + \frac{\pi/6}{2\pi} = \frac13$.
Sanity checks: $\rho=0$ gives $1/4$ (independent), $\rho=1$ gives $1/2$, $\rho=-1$ gives 0.

### Example 5 - a triangle support

"$(X,Y)$ has density 2 on $\{0<x<y<1\}$. Are X and Y independent? Find $E[X\mid Y]$ and the correlation."

The density looks constant but the support is not a rectangle, so they are dependent: knowing $Y=0.1$ forces $X<0.1$.
Marginals: $f_X(x) = 2(1-x)$, $f_Y(y) = 2y$.
Conditional: $X\mid Y=y$ is uniform on $(0,y)$, so $E[X\mid Y] = Y/2$.
This is the joint law of the min and max of two iid uniforms, whose covariance is $1/36$ with variances $1/18$ each, so the correlation is $1/2$.

## Pitfalls

- Declaring independence because a formula "looks separable" while ignoring the support.
- Forgetting the absolute value of the Jacobian, or using $dy/dx$ instead of $dx/dy$.
- Missing preimages in non-monotone transforms such as $Y = X^2$.
- Assuming normal marginals imply joint normality, and hence that zero correlation implies independence.
- Treating correlation as the full description of dependence; tail dependence can be strong at zero correlation.
- Regressing the wrong way: the slope of $Y$ on $X$ is $\rho\sigma_Y/\sigma_X$, not the reciprocal of the slope of $X$ on $Y$ unless $\lvert\rho\rvert=1$.
- Using a ratio of normals as if it had a mean: $Z_1/Z_2$ is Cauchy, with no finite mean.

## Interview questions

> [!question]- prob-joint-sum-two-uniforms | $U,V$ iid U(0,1). What is the density of $U+V$, and $P(U+V<1.5)$?
> Triangle $f(s)=\min(s,2-s)$ on $[0,2]$; $P = 7/8$.
> Convolution of two boxes; the excluded corner of the unit square has area $0.5^2/2$.

> [!question]- prob-joint-product-two-uniforms | $U,V$ iid U(0,1). Find $P(UV\le t)$ and evaluate at $t=1/2$.
> $t - t\ln t$; at $1/2$ it is $\tfrac12+\tfrac12\ln2\approx0.847$.
> Condition on $U=u$: $P(V\le t/u) = \min(1,t/u)$, then integrate over $u$.

> [!question]- prob-joint-bivariate-normal-orthant | Standard bivariate normal with correlation $\rho$. What is $P(X>0,Y>0)$? Evaluate at $\rho=0.5$.
> $\frac14+\frac{\arcsin\rho}{2\pi}$; $1/3$ at $\rho=0.5$.
> Rotational symmetry: in polar form the positive quadrant becomes an arc of angle $\pi/2+\arcsin\rho$ out of $2\pi$.

> [!question]- prob-joint-bivariate-normal-conditional | For a bivariate normal, what is the distribution of Y given X = x?
> $N\big(\mu_Y+\rho\frac{\sigma_Y}{\sigma_X}(x-\mu_X),\ \sigma_Y^2(1-\rho^2)\big)$.
> Write $Y$ as $\beta X$ plus an independent normal residual with $\beta = \rho\sigma_Y/\sigma_X$.

> [!question]- prob-joint-conditional-forecast-returns | X and Y are zero-mean bivariate normal, vols 2% and 3%, correlation 0.6. Given X = +4%, what are the mean and sd of Y?
> Mean $3.6\%$, sd $2.4\%$.
> X is $+2\sigma$, so Y's mean is $0.6\cdot2\cdot3\%$; conditional sd $3\%\sqrt{1-0.36}$.

> [!question]- prob-joint-uncorrelated-not-independent | Give two uncorrelated but dependent random variables.
> $X\sim U(-1,1)$ and $Y=X^2$.
> $\text{Cov}(X,X^2) = E[X^3]-E[X]E[X^2] = 0$ by symmetry, but $Y$ is determined by $X$.

> [!question]- prob-joint-normal-marginals-not-jointly-normal | Can two N(0,1) variables be uncorrelated yet dependent?
> Yes: $X$ and $W=SX$ with an independent random sign $S$.
> $W\sim N(0,1)$ and $\text{Cov}(X,W)=0$, but $\lvert W\rvert=\lvert X\rvert$; $X+W$ has an atom at 0, so the pair is not jointly normal.

> [!question]- prob-joint-normal-ratio-cauchy | What is the distribution of $Z_1/Z_2$ for iid standard normals, and what is its mean?
> Standard Cauchy, density $\frac{1}{\pi(1+x^2)}$; it has no mean.
> The ratio is $\tan\Theta$ with $\Theta$ uniform by rotational symmetry; the tails decay like $1/x^2$, so $E\lvert X\rvert=\infty$.

> [!question]- prob-joint-radius-two-normals | $X,Y$ iid N(0,1). What is $P(X^2+Y^2>4)$?
> $e^{-2}\approx0.135$.
> In polar coordinates $R^2\sim\text{Exp}(1/2)$, so $P(R^2>r) = e^{-r/2}$.

> [!question]- prob-joint-triangle-support-dependence | $(X,Y)$ is uniform on $\{0<x<y<1\}$. Independent? What is $E[X\mid Y]$?
> Dependent; $E[X\mid Y] = Y/2$.
> The support is not a rectangle; given $Y=y$, $X$ is uniform on $(0,y)$.

> [!question]- prob-joint-min-max-uniform-correlation | For two iid U(0,1), what is the correlation between the min and the max?
> $1/2$.
> Each has variance $1/18$ and $\text{Cov} = E[UV]-E[\min]E[\max] = \tfrac14-\tfrac13\cdot\tfrac23 = 1/36$.

> [!question]- prob-joint-chi-square-one-density | Derive the density of $Z^2$ for standard normal Z.
> $f(y) = \frac{1}{\sqrt{2\pi y}}e^{-y/2}$ for $y>0$.
> Two preimages $\pm\sqrt y$, each contributing $\varphi(\sqrt y)\cdot\frac{1}{2\sqrt y}$.

> [!question]- prob-joint-lognormal-density | If $X\sim N(\mu,\sigma^2)$, what is the density of $Y=e^X$?
> $f_Y(y) = \frac{1}{y\sigma\sqrt{2\pi}}\exp\big(-(\ln y-\mu)^2/(2\sigma^2)\big)$ for $y>0$.
> Monotone transform: $x=\ln y$ and $\lvert dx/dy\rvert = 1/y$.

> [!question]- prob-joint-two-asset-portfolio-vol | Two positions with daily vols 2% and 3% and correlation 0.6. Vol of their equal-notional sum?
> About $4.49\%$.
> $\sqrt{4+9+2\cdot0.6\cdot2\cdot3} = \sqrt{20.2}$ in percent; this is $w^\top\Sigma w$.

> [!question]- prob-joint-conditional-given-sum | X, Y iid with finite mean. What is $E[X\mid X+Y=s]$?
> $s/2$.
> By symmetry $E[X\mid S] = E[Y\mid S]$, and they add to $S$.

## Further reading

- Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), chapter 7 (joint distributions, bivariate normal) and chapter 8 (transformations, convolutions, beta-gamma).
- George Casella and Roger Berger, *Statistical Inference* (2nd ed.), chapter 4 (multiple random variables, bivariate transformations).
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 4 (joint distributions, bivariate normal).
- Next: [Inequalities and Limit Theorems](06-Inequalities-and-Limit-Theorems.md) and [Order Statistics and Extremes](08-Order-Statistics-and-Extremes.md).
