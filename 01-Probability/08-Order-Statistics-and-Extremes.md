---
type: concept
track: [quant-trader, quant-research]
tier: advanced
status: solid
prereqs: [joint-distributions-and-transformations]
est_hours: 3
sources: [Blitzstein and Hwang - Introduction to Probability (2nd ed.), Zhou - A Practical Guide to Quantitative Finance Interviews, Grimmett and Stirzaker - Probability and Random Processes, David and Nagaraja - Order Statistics (3rd ed.)]
---

# Order Statistics and Extremes

## TL;DR

- For i.i.d. $X_1,\dots,X_n$ with CDF $F$: $P(\max \le x) = F(x)^n$ and $P(\min > x) = (1-F(x))^n$; start every max/min question from these two lines.
- The $k$-th smallest of $n$ uniforms is $\text{Beta}(k, n-k+1)$ with mean $k/(n+1)$: the $n$ points cut $[0,1]$ into $n+1$ exchangeable spacings, each of mean $1/(n+1)$.
- For discrete variables use the tail sum $E[M] = \sum_{k \ge 1} P(M \ge k)$; the expected max of two dice is $161/36$.
- The min of independent exponentials is exponential with the summed rate, and by memorylessness the max of $n$ i.i.d. $\text{Exp}(1)$ has mean $H_n = 1 + 1/2 + \dots + 1/n$.
- Maxima of light-tailed samples grow very slowly: the max of $n$ standard normals is about $\sqrt{2 \ln n}$, so extremes are driven by the tail, not the variance.

## Learning objectives

- Derive the distribution of the min, max and $k$-th order statistic of i.i.d. samples.
- Know the expected order statistics of uniforms ($k/(n+1)$) and use spacings arguments.
- Solve "expected maximum of $n$ dice" and "best of $n$ offers" style questions.
- Use memorylessness to handle order statistics of exponentials, and state the growth rate of Gaussian maxima.

## Core concepts

### Max and min

Let $X_1,\dots,X_n$ be i.i.d. with CDF $F$ and density $f$, and write $X_{(1)} \le \dots \le X_{(n)}$ for the sorted sample.
The max is at most $x$ exactly when every observation is, and the min exceeds $x$ exactly when every observation does:

$$
F_{X_{(n)}}(x) = F(x)^n, \qquad P(X_{(1)} > x) = (1 - F(x))^n .
$$

Differentiate for densities: $f_{X_{(n)}}(x) = n F(x)^{n-1} f(x)$ and $f_{X_{(1)}}(x) = n (1-F(x))^{n-1} f(x)$.

### The k-th order statistic

For $X_{(k)}$ to sit in $[x, x+dx]$ we need one point there, $k-1$ points below and $n-k$ above.
Counting which point plays which role gives the multinomial coefficient:

$$
f_{X_{(k)}}(x) = \frac{n!}{(k-1)!\,(n-k)!}\, F(x)^{k-1} (1-F(x))^{n-k} f(x).
$$

Equivalently $P(X_{(k)} \le x) = P(\text{Bin}(n, F(x)) \ge k)$, which is often the faster route.
The joint density of the whole sorted sample is $n! \prod_i f(x_i)$ on $x_1 < \dots < x_n$.

### Uniforms, spacings and Beta laws

For $U_i \sim U(0,1)$ the formula gives $U_{(k)} \sim \text{Beta}(k, n-k+1)$, so

$$
E[U_{(k)}] = \frac{k}{n+1}, \qquad \operatorname{Var}(U_{(k)}) = \frac{k(n-k+1)}{(n+1)^2 (n+2)} .
$$

The spacings argument makes the mean obvious.
Put $n$ uniform points on $[0,1]$; they create $n+1$ gaps.
The gaps are exchangeable (equivalently, drop $n+1$ uniform points on a circle and cut at one of them), so each has mean $1/(n+1)$, and $U_{(k)}$ is the sum of the first $k$ gaps.
Consequences worth memorising: $E[\max] = n/(n+1)$, $E[\min] = 1/(n+1)$, $E[\text{range}] = (n-1)/(n+1)$.
For any continuous $F$, $F(X_{(k)})$ is the $k$-th uniform order statistic, so these results transfer through the probability integral transform.

### Exponentials and memorylessness

If $X_i \sim \text{Exp}(\lambda_i)$ are independent, then $\min_i X_i \sim \text{Exp}(\sum \lambda_i)$ and $P(X_j \text{ is the min}) = \lambda_j / \sum_i \lambda_i$, independently of the value of the min.
For $n$ i.i.d. $\text{Exp}(\lambda)$, the first failure takes $\text{Exp}(n\lambda)$; then by memorylessness $n-1$ fresh exponentials race, and so on (the Renyi representation):

$$
X_{(k)} \overset{d}{=} \sum_{j=1}^{k} \frac{E_j}{\lambda (n-j+1)}, \qquad E[X_{(n)}] = \frac{H_n}{\lambda}.
$$

### Discrete maxima

For integer-valued $M \ge 0$, $E[M] = \sum_{k \ge 1} P(M \ge k)$.
For the max of $n$ fair dice, $P(M \le k) = (k/6)^n$, so

$$
E[M] = \sum_{k=0}^{5} \left(1 - (k/6)^n\right) = 6 - \sum_{k=1}^{5} (k/6)^n .
$$

### Records

Among i.i.d. continuous draws, the $j$-th is a record (larger than all before it) with probability $1/j$ by symmetry, and record indicators are independent.
So the expected number of records in $n$ draws is $H_n \approx \ln n + 0.577$.

### Extremes

For the max of $n$ i.i.d. $N(0,1)$, $E[X_{(n)}] \sim \sqrt{2 \ln n}$ as $n \to \infty$, but convergence is slow: the exact mean is about $1.54$ at $n=10$ and $2.51$ at $n=100$, versus $\sqrt{2\ln n} = 2.15$ and $3.03$.
The Fisher-Tippett-Gnedenko theorem says a normalised max can only converge to a Gumbel (light tails: normal, exponential), Frechet (power tails: Student-t, Pareto) or Weibull (bounded support: uniform) law.
This matters for risk: tail estimation belongs to [Heavy Tails and Extreme Value Theory](../02-Statistics-and-Econometrics/13-Heavy-Tails-and-Extreme-Value-Theory.md), and the fat-tailed case makes maxima grow polynomially in $n$, not like $\sqrt{\ln n}$.

## Worked examples

### Expected maximum of two and three dice

"Let $M$ be the max of two dice. $P(M \le k) = k^2/36$, so $P(M = k) = (2k-1)/36$."
"Then $E[M] = \sum_k k(2k-1)/36 = (1 + 6 + 15 + 28 + 45 + 66)/36 = 161/36 \approx 4.47$."
"Check with the tail sum: $6 - (1 + 4 + 9 + 16 + 25)/36 = 6 - 55/36 = 161/36$."
"By symmetry the min is $7 - 161/36 = 91/36 \approx 2.53$, since $\min(X,Y) = 7 - \max(7-X, 7-Y)$."
"For three dice the tail sum gives $6 - (1 + 8 + 27 + 64 + 125)/216 = 6 - 225/216 = 119/24 \approx 4.96$."

### Correlation of the min and max of two uniforms

"Let $U, V$ be i.i.d. uniform, $m = \min$, $M = \max$. From the Beta laws, $E[m] = 1/3$, $E[M] = 2/3$ and both variances are $1 \cdot 2/(9 \cdot 4) = 1/18$."
"The trick for the cross moment: $mM = UV$ always, so $E[mM] = 1/4$."
"So $\operatorname{Cov}(m, M) = 1/4 - 2/9 = 1/36$ and the correlation is $(1/36)/(1/18) = 1/2$."
"Sanity check: positive, because a large min forces a large max."

### Best of n offers and second-price auctions

"Offers arrive i.i.d. uniform on $[0,1]$ and I can compare all $n$ before choosing, so I take the max, worth $n/(n+1)$ on average."
"In a second-price auction with $n$ bidders whose values are uniform and who bid truthfully, the seller gets the second highest value, $E[U_{(n-1)}] = (n-1)/(n+1)$; with 4 bidders that is $3/5$."
"The winner's expected surplus is $E[U_{(n)} - U_{(n-1)}] = 1/(n+1)$, one spacing."
"If offers instead arrive one at a time and must be accepted or rejected on the spot, this becomes the secretary problem in [Classic Expectation Problems](14-Classic-Expectation-Problems.md)."

### Waiting for the last of n lightbulbs

"Three bulbs with i.i.d. $\text{Exp}(1)$ lifetimes, mean 1 year. How long until all are dead?"
"The first failure is the min of three, $\text{Exp}(3)$, mean $1/3$."
"By memorylessness the survivors are as good as new, so the next gap is $\text{Exp}(2)$, mean $1/2$, then $\text{Exp}(1)$, mean 1."
"Total $1/3 + 1/2 + 1 = 11/6$ years."
"Note this is much more than the mean of 1 but only logarithmic in $n$: for $n$ bulbs it is $H_n$."

### Distribution of the median of three uniforms

"The median is below $x$ when at least two of three points are, so $P(U_{(2)} \le x) = 3x^2(1-x) + x^3 = 3x^2 - 2x^3$."
"Differentiating, the density is $6x(1-x)$, which is $\text{Beta}(2,2)$ as the general formula predicts, with mean $1/2$ and variance $1/20$."
"At $x = 0.3$ this gives $0.27 - 0.054 = 0.216$."

## Pitfalls

- Using $F(x)^n$ for the min: that is the max; the min uses the survival function, $1 - (1-F(x))^n$.
- Forgetting independence: $F^n$ needs i.i.d. draws; correlated assets need the joint law.
- Saying $E[U_{(k)}] = k/n$; the correct denominator is $n+1$ because there are $n+1$ gaps.
- Computing $E[\max]$ of dice as $\max$ of expectations or by averaging $P(M = k)$ incorrectly; the tail sum is the fastest reliable route.
- Quoting $\sqrt{2\ln n}$ as a number for moderate $n$: it overstates the Gaussian max by about 0.5 at $n = 100$.
- Treating order statistics as independent: $U_{(1)}$ and $U_{(n)}$ are positively correlated; what is independent is the set of spacings of exponentials, and the identity of the argmin versus the value of the min.

## Interview questions

> [!question]- prob-os-expected-max-two-dice | What is the expected value of the maximum of two fair dice?
> $161/36 \approx 4.47$. $P(M \ge k) = 1 - ((k-1)/6)^2$, and summing over $k = 1..6$ gives $6 - 55/36 = 161/36$.

> [!question]- prob-os-expected-min-two-dice | What is the expected value of the minimum of two fair dice?
> $91/36 \approx 2.53$. By the reflection $X \to 7 - X$, $E[\min] = 7 - E[\max] = 7 - 161/36$; or $E[\min] = \sum_k ((7-k)/6)^2 = 91/36$.

> [!question]- prob-os-expected-max-three-dice | What is the expected maximum of three fair dice?
> $119/24 \approx 4.96$. Tail sum: $6 - \sum_{k=1}^{5} (k/6)^3 = 6 - 225/216$.

> [!question]- prob-os-kth-uniform-order-stat | What is the distribution and mean of the $k$-th smallest of $n$ i.i.d. $U(0,1)$ variables?
> $\text{Beta}(k, n-k+1)$ with mean $k/(n+1)$. The $n$ points create $n+1$ exchangeable gaps of mean $1/(n+1)$ each, and $U_{(k)}$ is the sum of the first $k$.

> [!question]- prob-os-expected-range-uniforms | What is the expected range (max minus min) of $n$ i.i.d. uniforms on $[0,1]$?
> $(n-1)/(n+1)$. It is $n/(n+1) - 1/(n+1)$, or equivalently $n-1$ interior gaps of mean $1/(n+1)$ each.

> [!question]- prob-os-variance-max-uniforms | What is the variance of the max of $n$ i.i.d. uniforms?
> $n/((n+1)^2(n+2))$. The max is $\text{Beta}(n,1)$ with $E[M] = n/(n+1)$ and $E[M^2] = n/(n+2)$; subtract.

> [!question]- prob-os-min-max-two-uniforms-correlation | $U, V$ are i.i.d. uniform. What is the correlation between $\min(U,V)$ and $\max(U,V)$?
> $1/2$. $E[\min \cdot \max] = E[UV] = 1/4$, so the covariance is $1/4 - (1/3)(2/3) = 1/36$, and each variance is $1/18$.

> [!question]- prob-os-median-three-uniforms | What is the CDF of the median of three i.i.d. uniforms?
> $3x^2 - 2x^3$. The median is below $x$ when at least two points are: $3x^2(1-x) + x^3$; the density $6x(1-x)$ is $\text{Beta}(2,2)$.

> [!question]- prob-os-min-of-exponentials | $X \sim \text{Exp}(\lambda)$ and $Y \sim \text{Exp}(\mu)$ are independent. What is the law of $\min(X,Y)$ and the probability that $X$ is smaller?
> $\min \sim \text{Exp}(\lambda + \mu)$ and $P(X < Y) = \lambda/(\lambda+\mu)$. $P(\min > t) = e^{-\lambda t} e^{-\mu t}$, and $P(X<Y) = \int_0^\infty \lambda e^{-\lambda t} e^{-\mu t}\,dt$.

> [!question]- prob-os-max-of-exponentials | What is the expected maximum of $n$ i.i.d. $\text{Exp}(1)$ variables?
> $H_n = 1 + 1/2 + \dots + 1/n$. The gaps between successive order statistics are independent $\text{Exp}(n), \text{Exp}(n-1), \dots, \text{Exp}(1)$ by memorylessness.

> [!question]- prob-os-second-price-auction-revenue | $n$ bidders have i.i.d. uniform values and bid truthfully in a second-price auction. What is the expected revenue?
> $(n-1)/(n+1)$. Revenue is the second highest value $U_{(n-1)}$, whose mean is $(n-1)/(n+1)$.

> [!question]- prob-os-expected-records | In $n$ i.i.d. continuous draws, what is the expected number of records (draws larger than every earlier draw)?
> $H_n \approx \ln n + 0.577$. Draw $j$ is the max of the first $j$ with probability $1/j$ by symmetry; sum the indicators.

> [!question]- prob-os-max-of-normals-growth | Roughly how large is the max of $n$ i.i.d. standard normals, and how good is the approximation?
> Asymptotically $\sqrt{2 \ln n}$, but it overstates at practical sizes: the true mean is about $2.51$ at $n = 100$ versus $\sqrt{2\ln 100} \approx 3.03$. It follows from $n(1 - \Phi(x)) \approx 1$ with $1 - \Phi(x) \approx \phi(x)/x$.

> [!question]- prob-os-extreme-value-families | What are the three possible limit laws for a normalised maximum, and which applies to Student-t returns?
> Gumbel, Frechet and Weibull (Fisher-Tippett-Gnedenko). Student-t has power-law tails, so its maxima are in the Frechet domain; normals and exponentials are Gumbel, bounded variables are Weibull.

## Further reading

- Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), chapter 8 (order statistics and Beta).
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 4.
- Grimmett and Stirzaker, *Probability and Random Processes*, sections on order statistics and the exponential distribution.
- H. A. David and H. N. Nagaraja, *Order Statistics* (3rd ed.).
