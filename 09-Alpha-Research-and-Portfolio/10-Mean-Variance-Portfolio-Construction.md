---
type: concept
track: [quant-research]
tier: core
status: solid
prereqs: [convex-optimization-and-kkt, covariance-matrices-and-psd]
est_hours: 4
sources: [Markowitz (1952) - Portfolio Selection - Journal of Finance 7(1) 77-91, Grinold and Kahn - Active Portfolio Management 2nd ed (1999), Boyd and Vandenberghe - Convex Optimization (2004), Michaud (1989) - The Markowitz Optimization Enigma - Financial Analysts Journal 45(1) 31-42, Chopra and Ziemba (1993) - The Effect of Errors in Means Variances and Covariances on Optimal Portfolio Choice - Journal of Portfolio Management 19(2) 6-11, Jagannathan and Ma (2003) - Risk Reduction in Large Portfolios - Journal of Finance 58(4) 1651-1683, Kan and Zhou (2007) - Optimal Portfolio Choice with Parameter Uncertainty - Journal of Financial and Quantitative Analysis 42(3) 621-656, DeMiguel Garlappi and Uppal (2009) - Optimal Versus Naive Diversification - Review of Financial Studies 22(5) 1915-1953, Merton (1980) - On Estimating the Expected Return on the Market - Journal of Financial Economics 8(4) 323-361]
---

# Mean-Variance Portfolio Construction

## TL;DR

- Unconstrained mean-variance utility $\max_w\ w^\top\mu - \tfrac\lambda2 w^\top\Sigma w$ gives $w^* = \tfrac1\lambda\Sigma^{-1}\mu$; every optimal portfolio is a scaled copy of $\Sigma^{-1}\mu$.
- Global minimum variance: $w = \Sigma^{-1}\mathbf 1/(\mathbf 1^\top\Sigma^{-1}\mathbf 1)$ with variance $1/(\mathbf 1^\top\Sigma^{-1}\mathbf 1)$; tangency: $w = \Sigma^{-1}\mu/(\mathbf 1^\top\Sigma^{-1}\mu)$ with Sharpe $\sqrt{\mu^\top\Sigma^{-1}\mu}$ ($\mu$ in excess returns).
- The optimiser is an error maximiser: $\Sigma^{-1}$ amplifies noise along small-eigenvalue directions, errors in $\mu$ matter far more than errors in $\Sigma$, and in-sample Sharpe is biased up by about $N/T$ in squared terms.
- Remedies are all forms of shrinkage: shrink $\mu$ (IC-scaled alphas, Black-Litterman), shrink $\Sigma$ (factor models, Ledoit-Wolf), and constrain weights (long-only, position and turnover limits), which Jagannathan and Ma show acts like covariance shrinkage.
- Costs enter as $-\sum_i c_i|w_i - w_{0,i}|$ (convex, creates a no-trade band) or a quadratic impact term; the problem stays a convex QP or SOCP.

## Learning objectives

- Derive the minimum-variance and tangency portfolios.
- Explain estimation error and why naive mean-variance is unstable.
- Add constraints and costs to the optimizer.

## Core concepts

### The problem and its solution

$N$ assets with expected excess returns $\mu$ and covariance $\Sigma$ (symmetric positive definite, see [Covariance Matrices and PSD](../03-Linear-Algebra-and-Optimization/04-Covariance-Matrices-and-PSD.md)).
Markowitz (1952): choose weights to trade expected return against variance.
Three equivalent formulations trace the same efficient frontier:

- Maximise $w^\top\mu - \frac\lambda2 w^\top\Sigma w$ (risk aversion $\lambda$).
- Minimise $\frac12 w^\top\Sigma w$ subject to $w^\top\mu = m$ (and optionally $\mathbf 1^\top w = 1$).
- Maximise $w^\top\mu$ subject to $w^\top\Sigma w \le \sigma^2_{\max}$.

The utility form has first-order condition $\mu - \lambda\Sigma w = 0$, so $w^* = \lambda^{-1}\Sigma^{-1}\mu$, and the Sharpe of $w^*$ is $\sqrt{\mu^\top\Sigma^{-1}\mu}$ regardless of $\lambda$.

### Frontier with a budget constraint

Minimise $\frac12 w^\top\Sigma w$ subject to $w^\top\mu = m$ and $\mathbf 1^\top w = 1$.
The Lagrangian stationarity condition is $\Sigma w = \ell_1\mu + \ell_2\mathbf 1$, so $w = \Sigma^{-1}(\ell_1\mu + \ell_2\mathbf 1)$ (KKT details in [Convex Optimization and KKT](../03-Linear-Algebra-and-Optimization/08-Convex-Optimization-and-KKT.md)).
Define

$$
A = \mathbf 1^\top\Sigma^{-1}\mathbf 1, \quad B = \mathbf 1^\top\Sigma^{-1}\mu, \quad C = \mu^\top\Sigma^{-1}\mu, \quad D = AC - B^2 > 0.
$$

Substituting into the two constraints gives $\ell_1 = (Am - B)/D$, $\ell_2 = (C - Bm)/D$ and the frontier

$$
\sigma^2(m) = \frac{A m^2 - 2Bm + C}{D},
$$

a parabola in $(m, \sigma^2)$ and a hyperbola in $(\sigma, m)$.

**Global minimum variance (GMV).** Drop the return constraint: $w_{\text{GMV}} = \Sigma^{-1}\mathbf 1/A$, variance $1/A$, mean $B/A$.
It needs no expected returns, which is why it is a robust benchmark.

**Tangency.** With a risk-free asset and $\mu$ in excess returns, the portfolio maximising $w^\top\mu/\sqrt{w^\top\Sigma w}$ with $\mathbf 1^\top w = 1$ is

$$
w_{\text{tan}} = \frac{\Sigma^{-1}\mu}{\mathbf 1^\top\Sigma^{-1}\mu}, \qquad SR_{\text{tan}} = \sqrt{\mu^\top\Sigma^{-1}\mu} = \sqrt C,
$$

valid when $B > 0$.
Two-fund separation: every investor holds the tangency portfolio levered or de-levered with cash, differing only in $\lambda$.

### In active management

Grinold and Kahn apply the same algebra to residual alphas and residual risk: maximise $h^\top\alpha - \lambda h^\top\Sigma h$ over active weights $h$, with $\alpha = \text{IC}\cdot\sigma\cdot z$ already shrunk by the forecast's IC ([Signals, Features and Alpha Decay](03-Signals-Features-and-Alpha-Decay.md)).
Using IC-scaled alphas instead of raw forecasts is the single most important guard against the optimiser betting on noise.
Constraints added in practice: dollar and beta neutrality, sector and factor exposure limits, position limits as a fraction of ADV, gross leverage, turnover, and a tracking error or volatility target.

### Why naive mean-variance is unstable

- **Amplification by $\Sigma^{-1}$.** With eigendecomposition $\Sigma = \sum_k d_k v_kv_k^\top$, the optimal direction is $\Sigma^{-1}\mu = \sum_k (v_k^\top\mu/d_k)v_k$, so directions with tiny eigenvalues (long-short spreads between highly correlated assets) get huge weight, and those are exactly the directions where $\mu$ is least reliable.
- **Errors in means dominate.** Chopra and Ziemba (1993) find errors in means are over ten times as damaging as errors in variances and over twenty times as damaging as errors in covariances, with the gap widening at higher risk tolerance; means are also far harder to estimate (the standard error of an annual mean is $\sigma/\sqrt{Y}$, and Merton 1980 shows that sampling more often does not help, only a longer history does).
- **Michaud's "error maximisation".** Michaud (1989) describes mean-variance optimisation's tendency to maximise the effects of errors in the input assumptions: the optimiser overweights assets whose returns are overestimated and risks underestimated, so optimised portfolios systematically underperform their in-sample promise.
- **In-sample Sharpe bias.** With $\Sigma$ known and sample mean $\hat\mu$ from $T$ periods, $E[\hat\mu^\top\Sigma^{-1}\hat\mu] = \mu^\top\Sigma^{-1}\mu + N/T$; with the sample covariance (divisor $T-1$) the expectation is further multiplied by $(T-1)/(T-N-2)$ (Kan and Zhou 2007 analyse the consequences).
- **Naive diversification benchmark.** DeMiguel, Garlappi and Uppal (2009) find that none of the 14 models they evaluate across seven datasets is consistently better than $1/N$ out of sample, and estimate that about 3000 months of data would be needed for sample mean-variance to beat it with 25 assets.

### Remedies

1. **Better $\mu$:** IC-scaled alphas, Bayesian shrinkage toward an equilibrium prior (Black-Litterman), or dropping $\mu$ entirely (GMV, risk parity); see [Black-Litterman, Risk Parity and HRP](12-Black-Litterman-Risk-Parity-and-HRP.md).
2. **Better $\Sigma$:** a factor model (few parameters, well conditioned) or Ledoit-Wolf shrinkage ([Covariance Estimation and Shrinkage](11-Covariance-Estimation-and-Shrinkage.md)).
3. **Constraints:** Jagannathan and Ma (2003) show a no-short-sale constraint in the minimum-variance problem is equivalent to using the sample covariance with its large elements reduced: when the constraint binds for asset $i$ with multiplier $\lambda_i$, its covariances are reduced by $\lambda_i + \lambda_j$ and its variance by $2\lambda_i$, which explains why "wrong" constraints often help out of sample.
4. **Regularisation:** add $\gamma\|w - w_{\text{ref}}\|_2^2$ (ridge toward a reference portfolio) or an $\ell_1$ penalty.
5. **Resampling or robust optimisation:** average weights across bootstrap samples, or optimise against the worst case in an uncertainty set for $\mu$.

### Costs and constraints in the optimiser

A standard single-period formulation, solved as a convex QP or SOCP ([Quadratic Programming and Portfolio Solvers](../03-Linear-Algebra-and-Optimization/09-Quadratic-Programming-and-Portfolio-Solvers.md)):

$$
\max_w\ \alpha^\top w - \frac\lambda2 w^\top\Sigma w - \sum_i c_i|w_i - w_{0,i}| - \sum_i k_i|w_i - w_{0,i}|^{3/2}
$$

subject to $\mathbf 1^\top w = 0$ (dollar neutral), $B^\top w = 0$ (factor neutral), $|w_i| \le u_i$, $\sum_i|w_i - w_{0,i}| \le \tau$.
The linear term models half-spread and fees, the $3/2$-power term models square-root impact, and both are convex.
The absolute value is handled by splitting trades into buys and sells, $w - w_0 = b - s$ with $b, s \ge 0$.

**The no-trade region.** With only linear costs, the KKT condition for asset $i$ (one asset, or uncorrelated assets) is that you do not trade while $|\alpha_i - \lambda(\Sigma w)_i| \le c_i$.
Holdings inside a band around the frictionless target are left alone; outside it you trade only to the nearest edge of the band, not all the way to the target.
Costs and alpha must be in the same horizon units: amortise the one-off cost over the expected holding period of the position.

## Worked examples

### 1. Two-asset minimum variance

$\sigma_1 = 20\%$, $\sigma_2 = 30\%$, $\rho = 0.2$, so $\sigma_{12} = 0.012$.

- $w_1 = \dfrac{\sigma_2^2 - \sigma_{12}}{\sigma_1^2 + \sigma_2^2 - 2\sigma_{12}} = \dfrac{0.09 - 0.012}{0.04 + 0.09 - 0.024} = \dfrac{0.078}{0.106} = 0.736$, $w_2 = 0.264$.
- Portfolio volatility: $\sqrt{1/A} = 18.06\%$, below the lower of the two asset volatilities.

### 2. Two-asset tangency

Same risks, excess returns $\mu = (5\%, 8\%)$, individual Sharpes 0.25 and 0.267.

- $\Sigma^{-1}\mu$ normalised to sum to one: $w_{\text{tan}} = (0.577, 0.423)$.
- Return $6.27\%$, volatility $18.79\%$, Sharpe $0.334 = \sqrt{\mu^\top\Sigma^{-1}\mu}$.
- With risk aversion $\lambda = 4$ the utility-optimal holding is $\Sigma^{-1}\mu/4 = (0.256, 0.188)$, 44% invested and the rest in cash: the same portfolio, scaled.

### 3. Instability with correlated assets

Two assets with 20% volatility and correlation 0.9; eigenvalues of $\Sigma$ are 0.076 and 0.004 (condition number 19).

| $\mu$ | tangency weights | Sharpe |
| :--- | :--- | :--- |
| (5%, 6%) | $(-0.36, 1.36)$ | 0.303 |
| (5%, 7%) | $(-1.08, 2.08)$ | 0.380 |
| (6%, 6%) | $(0.50, 0.50)$ | 0.308 |

A one-point change in one expected return swings the weights by 72 points per asset, although the difference is far inside the estimation error of any mean.
Under a long-only constraint the first case becomes $(0, 1)$ with Sharpe 0.300, only 0.0035 below the unconstrained 0.303: the objective is flat along the spread direction, so the constraint costs almost nothing in-sample and removes the noisiest bet.

### 4. In-sample Sharpe inflation

$N = 50$ assets, $T = 60$ monthly observations, true maximum Sharpe 0.2 monthly (0.69 annualised), $\Sigma$ known.

- $E[\hat\theta^2] = 0.2^2 + 50/60 = 0.873$, so the in-sample tangency Sharpe is about $\sqrt{0.873} = 0.93$ monthly, 3.2 annualised.
- With the sample covariance too, the expectation is multiplied by $(T-1)/(T-N-2) = 59/8$, giving $\hat\theta^2 \approx 6.4$.

With $N = 10$ and $T = 60$ the formulas give $0.2^2 + 10/60 = 0.207$ (known $\Sigma$) and $\tfrac{59}{48}\times0.207 = 0.254$ (estimated $\Sigma$).
The script simulates 20,000 samples with identity covariance for both cases and matches each formula within four standard errors; it also checks $N = 50$ with known $\Sigma$.
The true (out-of-sample) Sharpe of the estimated tangency portfolio averages about 0.08 in that simulation, far below the true 0.2, and by construction it can never exceed 0.2.

### 5. A no-trade band from linear costs

One asset, $\mu = 5\%$, $\sigma = 20\%$, $\lambda = 5$, linear cost $c = 1\%$ per unit traded (amortised to the same horizon as $\mu$).

- Frictionless target: $w^* = \mu/(\lambda\sigma^2) = 0.05/0.2 = 0.25$.
- KKT band: trade only if $|\mu - \lambda\sigma^2 w_0| > c$, giving the no-trade region $[(\mu - c)/(\lambda\sigma^2), (\mu + c)/(\lambda\sigma^2)] = [0.20, 0.30]$.
- Starting at $w_0 = 0.10$: buy up to 0.20, not to 0.25.
- Starting at $w_0 = 0.27$: do nothing.

## Pitfalls

- Feeding raw return forecasts or historical means into the optimiser instead of IC-scaled alphas.
- Inverting a sample covariance with $N$ close to $T$ (or $N > T$, where it is singular) instead of using a factor model or shrinkage.
- Reporting the in-sample Sharpe of an optimised portfolio as if it were achievable.
- Mixing horizons: annual alphas with one-off costs, or daily covariances with annual alphas.
- Forgetting that the tangency formula needs $\mathbf 1^\top\Sigma^{-1}\mu > 0$; otherwise the normalisation flips the portfolio to the inefficient branch.
- Adding many hard constraints until the optimiser has no freedom, so the "optimal" book is set by the constraints (low transfer coefficient) and the alpha barely matters.
- Rebalancing all the way to the frictionless target every period, which pays costs to chase noise.

## Interview questions

> [!question]- alpha-mv-utility-solution | Solve $\max_w w^\top\mu - \tfrac\lambda2 w^\top\Sigma w$.
> $w^* = \lambda^{-1}\Sigma^{-1}\mu$.
> The objective is strictly concave for positive definite $\Sigma$; setting the gradient $\mu - \lambda\Sigma w$ to zero gives the unique maximiser, and its Sharpe $\sqrt{\mu^\top\Sigma^{-1}\mu}$ does not depend on $\lambda$.

> [!question]- alpha-mv-gmv | What are the global minimum variance weights and variance?
> $w = \Sigma^{-1}\mathbf 1/(\mathbf 1^\top\Sigma^{-1}\mathbf 1)$ with variance $1/(\mathbf 1^\top\Sigma^{-1}\mathbf 1)$.
> From the Lagrangian of $\min\frac12w^\top\Sigma w$ subject to $\mathbf 1^\top w = 1$: $\Sigma w = \ell\mathbf 1$, then normalise.

> [!question]- alpha-mv-tangency | Give the tangency portfolio and its Sharpe ratio.
> $w = \Sigma^{-1}\mu/(\mathbf 1^\top\Sigma^{-1}\mu)$ with $\mu$ in excess returns, Sharpe $\sqrt{\mu^\top\Sigma^{-1}\mu}$.
> Maximising the Sharpe ratio is scale invariant, so its solution is proportional to $\Sigma^{-1}\mu$; the formula needs $\mathbf 1^\top\Sigma^{-1}\mu > 0$.

> [!question]- alpha-mv-two-asset-gmv | Two assets with 20% and 30% volatility and correlation 0.2. Minimum-variance weight in the first?
> About 0.736.
> $w_1 = (\sigma_2^2 - \sigma_{12})/(\sigma_1^2 + \sigma_2^2 - 2\sigma_{12}) = 0.078/0.106$, giving portfolio volatility 18.1%.

> [!question]- alpha-mv-frontier | Write the minimum variance for target mean $m$ with a budget constraint.
> $\sigma^2(m) = (Am^2 - 2Bm + C)/D$ with $A = \mathbf 1^\top\Sigma^{-1}\mathbf 1$, $B = \mathbf 1^\top\Sigma^{-1}\mu$, $C = \mu^\top\Sigma^{-1}\mu$, $D = AC - B^2$.
> Stationarity gives $w = \Sigma^{-1}(\ell_1\mu + \ell_2\mathbf 1)$; the two constraints fix $\ell_1 = (Am - B)/D$ and $\ell_2 = (C - Bm)/D$.

> [!question]- alpha-mv-error-maximiser | Why is mean-variance called an error maximiser?
> It overweights assets whose returns are overestimated and risks underestimated.
> $\Sigma^{-1}\mu = \sum_k(v_k^\top\mu/d_k)v_k$, with eigenvalues $d_k$, loads heavily on small-eigenvalue directions, where mean estimates are least reliable, so estimation noise becomes large positions.

> [!question]- alpha-mv-means-vs-cov | Which estimation errors hurt mean-variance portfolios most?
> Errors in expected returns: over ten times as damaging as errors in variances and over twenty times as damaging as errors in covariances (Chopra and Ziemba 1993).
> Means are also the hardest to estimate: the standard error of an annual mean is $\sigma/\sqrt{Y}$, so with a hypothetical 16% volatility even 30 years of data leave a standard error of $16\%/\sqrt{30} = 2.9\%$.

> [!question]- alpha-mv-insample-bias | With known $\Sigma$, how biased is the in-sample squared Sharpe of the estimated tangency portfolio?
> Upward by $N/T$: $E[\hat\mu^\top\Sigma^{-1}\hat\mu] = \mu^\top\Sigma^{-1}\mu + N/T$.
> $\hat\mu \sim N(\mu, \Sigma/T)$, and the quadratic form of the noise has expectation $\text{tr}(\Sigma^{-1}\Sigma/T) = N/T$; estimating $\Sigma$ multiplies it further by $(T-1)/(T-N-2)$.

> [!question]- alpha-mv-long-only-shrinkage | Why do long-only constraints often improve out-of-sample minimum-variance portfolios?
> They act like covariance shrinkage.
> Jagannathan and Ma (2003) show a binding no-short constraint is equivalent to reducing the estimated covariances of the assets the optimiser wanted to short (by $\lambda_i + \lambda_j$, with $\lambda$ the constraint multipliers); those large estimated covariances are likely to be partly estimation error.

> [!question]- alpha-mv-no-trade-band | How do linear transaction costs change the optimal rebalancing rule?
> They create a no-trade band around the frictionless target.
> KKT: do not trade asset $i$ while $|\alpha_i - \lambda(\Sigma w)_i| \le c_i$; outside the band trade only to its nearest edge.

> [!question]- alpha-mv-correlated-instability | Two assets with 20% vol and correlation 0.9 have expected excess returns 5% and 6%. Tangency weights?
> About $(-0.36, 1.36)$.
> $\Sigma^{-1}\mu$ is dominated by the small-eigenvalue spread direction; raising the second mean to 7% moves the weights to $(-1.08, 2.08)$.

> [!question]- alpha-mv-two-fund | What is two-fund separation?
> With a risk-free asset every mean-variance investor holds the same tangency portfolio, levered or de-levered with cash.
> The optimal risky holding $\lambda^{-1}\Sigma^{-1}\mu$ has direction independent of risk aversion; only its scale changes.

> [!question]- alpha-mv-insample-50-60 | 50 assets, 60 monthly observations, true maximum Sharpe 0.2 monthly, covariance known. What in-sample tangency Sharpe should you expect?
> About 0.93 monthly, 3.2 annualised, against a true 0.69.
> $E[\hat\theta^2] = 0.2^2 + 50/60 = 0.873$; with an estimated covariance the expectation is multiplied again by $(T-1)/(T-N-2) = 59/8$.

> [!question]- alpha-mv-no-trade-numeric | One asset, $\mu = 5\%$, $\sigma = 20\%$, $\lambda = 5$, linear cost 1% per unit traded. What is the no-trade band, and what do you do from a 10% holding?
> The band is $[0.20, 0.30]$ around the target 0.25; from 0.10 buy up to 0.20, not 0.25.
> Do not trade while $|\mu - \lambda\sigma^2 w_0| \le c$, so the edges are $(\mu \mp c)/(\lambda\sigma^2) = 0.04/0.2$ and $0.06/0.2$.

> [!question]- alpha-mv-long-only-cost | Two assets with 20% vol and correlation 0.9 have expected returns 5% and 6%. How much Sharpe does a long-only constraint cost?
> About 0.0035: Sharpe 0.300 for $(0, 1)$ against 0.303 unconstrained at $(-0.36, 1.36)$.
> The objective is flat along the long-short spread direction, so the constraint removes the noisiest bet almost for free.

## In this repo and The-Distinguished-Engineer

- Code: [`code/alpha_10_mean_variance.py`](code/alpha_10_mean_variance.py) prints and asserts every number on this page: minimum-variance, tangency and utility-optimal weights by brute-force grid search, the frontier formula against a direct KKT solve, the in-sample Sharpe bias by simulation, the Jagannathan-Ma shrinkage equivalence by exact active-set enumeration, and the no-trade band by maximising the cost-adjusted utility from each starting weight.
- Code: [black_litterman_model.ipynb](code/black_litterman_model.ipynb) for an equilibrium-prior alternative to raw means.
- Related notes: [Covariance Estimation and Shrinkage](11-Covariance-Estimation-and-Shrinkage.md), [Black-Litterman, Risk Parity and HRP](12-Black-Litterman-Risk-Parity-and-HRP.md), [Quadratic Programming and Portfolio Solvers](../03-Linear-Algebra-and-Optimization/09-Quadratic-Programming-and-Portfolio-Solvers.md).

## Further reading

- Richard C. Grinold and Ronald N. Kahn, *Active Portfolio Management* (2nd ed., 1999).
- Stephen Boyd and Lieven Vandenberghe, *Convex Optimization* (2004).
- Harry Markowitz, "Portfolio Selection", *Journal of Finance* 7(1) (1952), 77-91.
- Richard O. Michaud, "The Markowitz Optimization Enigma: Is 'Optimized' Optimal?", *Financial Analysts Journal* 45(1) (1989), 31-42.
- Vijay K. Chopra and William T. Ziemba, "The Effect of Errors in Means, Variances, and Covariances on Optimal Portfolio Choice", *Journal of Portfolio Management* 19(2) (1993), 6-11.
- Ravi Jagannathan and Tongshu Ma, "Risk Reduction in Large Portfolios: Why Imposing the Wrong Constraints Helps", *Journal of Finance* 58(4) (2003), 1651-1683.
- Raymond Kan and Guofu Zhou, "Optimal Portfolio Choice with Parameter Uncertainty", *Journal of Financial and Quantitative Analysis* 42(3) (2007), 621-656.
- Victor DeMiguel, Lorenzo Garlappi and Raman Uppal, "Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?", *Review of Financial Studies* 22(5) (2009), 1915-1953.
- Robert C. Merton, "On Estimating the Expected Return on the Market: An Exploratory Investigation", *Journal of Financial Economics* 8(4) (1980), 323-361.
