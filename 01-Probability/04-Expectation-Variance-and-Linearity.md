---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [random-variables-and-distributions]
est_hours: 5
sources: [Blitzstein and Hwang - Introduction to Probability 2nd ed ch 4 7 9, Zhou - A Practical Guide to Quantitative Finance Interviews ch 4, Ross - A First Course in Probability ch 7, Williams - Probability with Martingales ch 9]
---

# Expectation, Variance and Linearity

## TL;DR

- $E[X+Y] = E[X]+E[Y]$ always, with no independence needed; write a count as a sum of indicators and add their probabilities.
- $\text{Var}(\sum X_i) = \sum\text{Var}(X_i) + 2\sum_{i<j}\text{Cov}(X_i,X_j)$; for indicators $\text{Cov}(I_A,I_B) = P(A\cap B)-P(A)P(B)$.
- Tail sum: for $X\in\{0,1,2,\dots\}$, $E[X] = \sum_{k\ge1}P(X\ge k)$; for $X\ge0$, $E[X] = \int_0^\infty P(X>x)\,dx$.
- Tower law $E[E[X\mid Y]] = E[X]$ and total variance $\text{Var}(X) = E[\text{Var}(X\mid Y)] + \text{Var}(E[X\mid Y])$.
- $E[X\mid Y]$ is the best mean-square predictor of $X$ from $Y$, and its error is uncorrelated with every function of $Y$.
- Random sums: $E[\sum_{i=1}^N X_i] = E[N]E[X]$ and $\text{Var} = E[N]\text{Var}(X) + \text{Var}(N)E[X]^2$ when $N$ is independent of the iid $X_i$.

## Learning objectives

- Solve counting-style expectation problems with indicator variables and linearity.
- Compute variance and covariance of sums, including dependent indicators.
- Apply the laws of total expectation and total variance.
- Interpret conditional expectation as the best mean-square predictor.

## Core concepts

### Expectation and LOTUS

$E[X] = \sum_x x\,P(X=x)$ or $\int x f(x)\,dx$, when the sum or integral converges absolutely.
LOTUS: $E[g(X)] = \sum_x g(x)P(X=x)$; you never need the distribution of $g(X)$ itself.
$E[g(X)] \ne g(E[X])$ in general; the direction of the gap for convex $g$ is Jensen's inequality ([Inequalities and Limit Theorems](06-Inequalities-and-Limit-Theorems.md)).

### Linearity and indicators

$E[aX+bY+c] = aE[X]+bE[Y]+c$ for any random variables, dependent or not, because expectation is a sum (integral) over outcomes and sums are linear.
Indicator method: if $X$ counts how many of the events $A_1,\dots,A_n$ happen, $X = \sum_i I_{A_i}$ and

$$
E[X] = \sum_i P(A_i).
$$

The hard joint distribution of $X$ never has to be found.
Interview pattern: "expected number of ..." almost always means indicators; look for symmetry so all $P(A_i)$ are equal.
More of these problems: [Classic Expectation Problems](14-Classic-Expectation-Problems.md).

### Tail-sum formula

For $X$ taking values in $\{0,1,2,\dots\}$: $X = \sum_{k\ge1} I_{\{X\ge k\}}$, so $E[X] = \sum_{k\ge1}P(X\ge k)$.
For $X\ge0$ continuous: $E[X] = \int_0^\infty P(X>x)\,dx$.
Use it for maxima and minima, where $P(\max\ge k)$ or $P(\min\ge k)$ is easy.

### Variance and covariance

$\text{Var}(X) = E[(X-EX)^2] = E[X^2] - (EX)^2$, and $\text{Var}(aX+b) = a^2\text{Var}(X)$.
$\text{Cov}(X,Y) = E[XY]-E[X]E[Y]$ is bilinear and symmetric, $\text{Cov}(X,X) = \text{Var}(X)$, and

$$
\text{Var}\Big(\sum_i X_i\Big) = \sum_i\text{Var}(X_i) + 2\sum_{i<j}\text{Cov}(X_i,X_j).
$$

Correlation $\rho = \text{Cov}(X,Y)/(\sigma_X\sigma_Y)\in[-1,1]$ by Cauchy-Schwarz.
Independence implies zero covariance, not conversely (see [Joint Distributions and Transformations](05-Joint-Distributions-and-Transformations.md)).

For a sum of indicators, $\text{Var}(I_A) = p(1-p)$ and $\text{Cov}(I_A,I_B) = P(A\cap B) - P(A)P(B)$.
Example: the number of aces in a 5-card hand is hypergeometric.
With $I_i$ = "card $i$ is an ace", $P = 1/13$ and $P(\text{cards } i,j \text{ both aces}) = \frac{4\cdot3}{52\cdot51}$, so

$$
\text{Var} = 5\cdot\tfrac1{13}\cdot\tfrac{12}{13} + 20\Big(\tfrac{12}{2652}-\tfrac1{169}\Big) = \tfrac{940}{2873}\approx0.327,
$$

which is the binomial variance times the finite-population correction $(52-5)/(52-1)$.
Sampling without replacement makes indicators negatively correlated and shrinks the variance.

### Conditional expectation, tower law and total variance

$E[X\mid Y]$ is a function of $Y$, hence a random variable.
Tower law (Adam's law): $E[E[X\mid Y]] = E[X]$, the continuous version of "condition on the first step".
Total variance (Eve's law):

$$
\text{Var}(X) = \underbrace{E[\text{Var}(X\mid Y)]}_{\text{within-group}} + \underbrace{\text{Var}(E[X\mid Y])}_{\text{between-group}}.
$$

Random sum $S = \sum_{i=1}^N X_i$ with $N$ independent of iid $X_i$ (mean $\mu$, variance $\sigma^2$): $E[S\mid N] = N\mu$, $\text{Var}(S\mid N) = N\sigma^2$, so

$$
E[S] = \mu E[N], \qquad \text{Var}(S) = \sigma^2E[N] + \mu^2\text{Var}(N).
$$

The first identity (Wald) also holds when $N$ is a stopping time with finite mean, which [Martingales and Optional Stopping](12-Martingales-and-Optional-Stopping.md) makes precise.

### Best mean-square predictor

For any function $g$,

$$
E[(X-g(Y))^2] = E[(X-E[X\mid Y])^2] + E[(E[X\mid Y]-g(Y))^2],
$$

because the cross term $E[(X-E[X\mid Y])(E[X\mid Y]-g(Y))]$ vanishes: condition on $Y$ and the first factor has conditional mean zero.
So $E[X\mid Y]$ minimises mean-squared error, and the residual $X - E[X\mid Y]$ is orthogonal to every function of $Y$.
Restricting $g$ to be linear gives the regression line $a + bY$ with $b = \text{Cov}(X,Y)/\text{Var}(Y)$; the two coincide when $(X,Y)$ is bivariate normal.
Geometrically, $E[X\mid Y]$ is the orthogonal projection of $X$ onto the space of functions of $Y$; this is the setting for [Linear Regression and OLS](../02-Statistics-and-Econometrics/04-Linear-Regression-OLS.md).

## Worked examples

### Example 1 - fixed points of a random permutation

"Shuffle $n$ cards labelled 1 to $n$. What are the mean and variance of the number of cards in their own position?"

Let $I_i$ indicate card $i$ is in position $i$; $P(I_i=1) = 1/n$, so $E[X] = n\cdot\frac1n = 1$ for every $n$.
For $i\ne j$, $P(I_i=I_j=1) = \frac{1}{n(n-1)}$, so $\text{Cov}(I_i,I_j) = \frac{1}{n(n-1)}-\frac1{n^2} = \frac{1}{n^2(n-1)}$.
$\text{Var}(X) = n\cdot\frac1n\big(1-\frac1n\big) + n(n-1)\cdot\frac{1}{n^2(n-1)} = 1-\frac1n+\frac1n = 1$.
Mean and variance both 1, matching the Poisson(1) limit, which is also why $P(\text{no fixed point})\to e^{-1}$.

### Example 2 - coupon collector with a die

"How many rolls do you expect to need to see all six faces?"

Split the wait into stages: after seeing $k-1$ distinct faces, each roll is new with probability $(7-k)/6$, so stage $k$ is Geometric with mean $6/(7-k)$.
$E = 6\big(1+\tfrac12+\tfrac13+\tfrac14+\tfrac15+\tfrac16\big) = 6H_6 = 14.7$.
Stages are independent, so the variance adds: $\sum_{k=1}^{6}\frac{1-p_k}{p_k^2}$ with $p_k = (7-k)/6$, which is $38.99$.
In general $E = nH_n \approx n\ln n + 0.577n$.

### Example 3 - a random number of dice

"Roll a die to get $N$, then roll $N$ dice and sum them. Mean and variance of the sum?"

Each die has $\mu = 7/2$, $\sigma^2 = 35/12$, and $N$ has the same mean and variance.
$E[S] = \mu E[N] = 49/4 = 12.25$.
$\text{Var}(S) = \sigma^2E[N] + \mu^2\text{Var}(N) = \frac{35}{12}\cdot\frac72 + \frac{49}{4}\cdot\frac{35}{12} = \frac{735}{16}\approx 45.94$.
The second term, uncertainty about how many dice, dominates: that is the between-group part of the total variance, and the same decomposition drives PnL variance when both trade count and trade size are random.

### Example 4 - maximum of two dice by tail sums

"Two dice are rolled. What is the expected maximum?"

$P(\max\ge k) = 1 - P(\text{both}\le k-1) = 1 - \frac{(k-1)^2}{36}$.
$E[\max] = \sum_{k=1}^{6}\Big(1-\frac{(k-1)^2}{36}\Big) = 6 - \frac{0+1+4+9+16+25}{36} = 6-\frac{55}{36} = \frac{161}{36}\approx 4.47$.
Check with symmetry: $E[\min] = 7 - 161/36 = 91/36$ because $\max+\min$ is the sum of the dice, mean 7.

### Example 5 - sum of rolls until the first six

"Roll a die until you get a 6. What is the expected total of all rolls, including the 6?"

Wald: the number of rolls $N$ is a stopping time with $E[N] = 6$, and each roll has mean $3.5$, so $E = 6\times3.5 = 21$.
Direct check: there are on average 5 non-six rolls, and given a roll is not a six its mean is $(1+\dots+5)/5 = 3$, so $5\cdot3 + 6 = 21$.
The trap is to say "$E[N]$ times the conditional mean given not six", which ignores the final 6; the two routes agreeing is the sanity check.

## Pitfalls

- Believing linearity needs independence; it never does (variance of a sum does).
- Computing $E[g(X)]$ as $g(E[X])$, for example $E[1/X]$ or $E[X^2]$.
- Forgetting covariance terms when adding variances of dependent indicators.
- Applying $E[\sum^N X_i] = E[N]E[X]$ when $N$ depends on future values of $X$ (not a stopping time), or using the random-sum variance formula when $N$ and the $X_i$ are dependent.
- Tail-sum off-by-one: for integer $X\ge0$ it is $\sum_{k\ge1}P(X\ge k)$, equivalently $\sum_{k\ge0}P(X>k)$.
- Treating $E[X\mid Y]$ as a number rather than a function of $Y$.
- Assuming the best predictor is linear; it is linear only in special cases such as jointly normal variables.

## Interview questions

> [!question]- prob-exp-fixed-points-mean-variance | A deck of n cards is shuffled. Mean and variance of the number of cards left in their original position?
> Both equal 1 (for $n\ge2$).
> Indicators with $P=1/n$ give mean 1; pairwise $\text{Cov} = \frac{1}{n^2(n-1)}$ adds exactly $1/n$ to the $1-1/n$ from the diagonal.

> [!question]- prob-exp-coupon-collector-die | Expected number of die rolls to see every face at least once?
> $6H_6 = 14.7$.
> Stage $k$ is Geometric with success probability $(7-k)/6$, so the stage means are $6/6, 6/5, \dots, 6/1$.

> [!question]- prob-exp-random-sum-of-dice | Roll a die to get N, then sum N dice. Mean and variance of the sum?
> Mean $49/4 = 12.25$, variance $735/16\approx45.94$.
> $E[S]=\mu E[N]$; $\text{Var}(S) = \sigma^2E[N]+\mu^2\text{Var}(N)$ with $\mu=7/2$, $\sigma^2=35/12$ for both.

> [!question]- prob-exp-max-two-dice | What is the expected maximum of two fair dice?
> $161/36 \approx 4.47$.
> Tail sum: $\sum_{k=1}^6\big(1-(k-1)^2/36\big) = 6-55/36$.

> [!question]- prob-exp-shared-birthday-pairs | Among 30 people, what is the expected number of pairs sharing a birthday (365 equally likely days)?
> $435/365\approx1.19$.
> $\binom{30}{2}=435$ pair indicators, each with probability $1/365$.

> [!question]- prob-exp-empty-boxes | n balls are thrown uniformly into n boxes. Expected number of empty boxes?
> $n(1-1/n)^n \approx n/e$; for $n=10$ it is about $3.49$.
> Each box is empty with probability $(1-1/n)^n$; add the indicators.

> [!question]- prob-exp-sum-until-first-six | Roll a die until the first 6. Expected sum of all rolls including the 6?
> 21.
> Wald: $E[N]\cdot E[X] = 6\cdot3.5$; or 5 expected non-sixes with conditional mean 3, plus the final 6.

> [!question]- prob-exp-runs-in-coin-flips | A fair coin is flipped n times. Expected number of runs (maximal blocks of equal outcomes)?
> $(n+1)/2$.
> Runs = 1 + number of positions $i\ge2$ where flip $i$ differs from flip $i-1$, each with probability $1/2$.

> [!question]- prob-exp-overlapping-hh-count | In 10 fair coin flips, what is the expected number of occurrences of HH, counting overlaps?
> $9/4$.
> Nine adjacent pairs, each HH with probability $1/4$; overlap creates dependence but linearity ignores it.

> [!question]- prob-exp-distinct-faces-six-rolls | Roll a die six times. Expected number of distinct faces seen?
> $6\big(1-(5/6)^6\big)\approx3.99$.
> Each face appears at least once with probability $1-(5/6)^6$.

> [!question]- prob-exp-abs-diff-uniforms | $U_1,U_2$ iid uniform on [0,1]. What is $E|U_1-U_2|$?
> $1/3$.
> By symmetry $2\int_0^1\int_0^x(x-y)\,dy\,dx = 2\int_0^1 x^2/2\,dx = 1/3$.

> [!question]- prob-exp-total-variance-mixture | With probability 1/2 draw from N(0,1), otherwise from N(2,1). What is the variance of the draw?
> 2.
> Total variance: $E[\text{Var}\mid\text{component}] = 1$ plus $\text{Var}(\text{component mean}) = \text{Var}$ of a fair $\{0,2\}$ variable $=1$.

> [!question]- prob-exp-best-mse-predictor | Which function of Y minimises $E[(X-g(Y))^2]$, and why?
> $g(Y) = E[X\mid Y]$.
> Expanding around $E[X\mid Y]$ leaves a cross term that is zero by the tower law, so any other $g$ adds $E[(E[X\mid Y]-g(Y))^2]\ge0$.

> [!question]- prob-exp-hypergeometric-aces-variance | What is the variance of the number of aces in a 5-card hand?
> $940/2873\approx0.327$.
> Binomial variance $5\cdot\frac1{13}\cdot\frac{12}{13}$ times the finite-population factor $47/51$; the indicators are negatively correlated.

> [!question]- prob-exp-linearity-dependent | Why does $E[X+Y]=E[X]+E[Y]$ hold even when X and Y are dependent?
> Expectation is a weighted sum over outcomes.
> $\sum_\omega (X(\omega)+Y(\omega))P(\omega)$ splits into two sums; the joint distribution never enters, unlike $E[XY]$ or $\text{Var}(X+Y)$.

## Further reading

- Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), chapter 4 (expectation, indicators), chapter 7 (covariance), chapter 9 (conditional expectation, Adam's and Eve's laws).
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 4 (expected value, variance and covariance).
- Sheldon Ross, *A First Course in Probability*, chapter 7.
- David Williams, *Probability with Martingales*, chapter 9 (conditional expectation as projection).
- Next: [Joint Distributions and Transformations](05-Joint-Distributions-and-Transformations.md) and [Classic Expectation Problems](14-Classic-Expectation-Problems.md).
