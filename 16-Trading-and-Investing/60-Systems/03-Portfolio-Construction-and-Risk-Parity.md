---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Ledoit and Wolf (2004) - A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices - Journal of Multivariate Analysis 88(2), Lopez de Prado (2016) - Building Diversified Portfolios that Outperform Out of Sample - Journal of Portfolio Management 42(4), Markowitz (1952) - Portfolio Selection - Journal of Finance 7(1), Michaud (1989) - The Markowitz Optimization Enigma: Is 'Optimized' Optimal? - Financial Analysts Journal 45(1), Roncalli (2013) - Introduction to Risk Parity and Budgeting, Ledoit and Wolf (2003) - Improved Estimation of the Covariance Matrix of Stock Returns - Journal of Empirical Finance 10(5), Ledoit and Wolf (2004) - Honey I Shrunk the Sample Covariance Matrix - Journal of Portfolio Management 30(4), Maillard Roncalli and Teiletche (2010) - The Properties of Equally Weighted Risk Contribution Portfolios - Journal of Portfolio Management 36(4), DeMiguel Garlappi and Uppal (2009) - Optimal Versus Naive Diversification - Review of Financial Studies 22(5), Choueifaty and Coignard (2008) - Toward Maximum Diversification - Journal of Portfolio Management 35(1)]
---

# Portfolio Construction and Risk Parity

## TL;DR

- Portfolio construction transforms raw alpha signals and risk forecasts into executable capital allocations while obeying real-world constraints.
- Unconstrained Mean-Variance Optimization (MVO) acts as an "error maximizer" (Michaud 1989), overweighting securities with overstated expected returns or understated risk.
- Sample covariance matrices for large asset universes are singular when $N \ge T$ and ill-conditioned when $N$ is close to $T$; Ledoit-Wolf shrinkage stabilizes inversion by pulling the sample covariance toward a structured target.
- Equal Risk Contribution (Risk Parity) sizes assets so each contributes the same amount to total portfolio volatility, removing equity-dominated risk concentration.
- Hierarchical Risk Parity (HRP) uses hierarchical clustering to allocate capital across asset clusters without inverting the covariance matrix.
- Real-world production optimizers enforce linear factor bounds, minimum lot constraints, and turnover penalties directly within quadratic programming objectives.

## Learning objectives

- Diagnose the failure modes of unconstrained Markowitz mean-variance optimization.
- Apply Ledoit-Wolf covariance shrinkage and interpret condition numbers in matrix stability.
- Derive and calculate Marginal Risk Contribution (MRC) and Total Risk Contribution (TRC).
- Implement Equal Risk Contribution (ERC) risk parity portfolios and solve for optimal weights.
- Construct Hierarchical Risk Parity (HRP) portfolios using tree clustering, quasi-diagonalization, and recursive bisection.

## Core concepts

### 1. Markowitz Mean-Variance Optimization and Error Maximization

Harry Markowitz (1952) established the foundational framework of quantitative portfolio selection:

$$\min_{\mathbf{w}} \frac{1}{2} \mathbf{w}^T \mathbf{\Sigma} \mathbf{w} - \lambda \mathbf{w}^T \boldsymbol{\mu} \quad \text{s.t.} \quad \mathbf{w}^T \mathbf{1} = 1, \quad \mathbf{w} \ge 0$$

Where $\boldsymbol{\mu}$ is the vector of expected asset returns, $\mathbf{\Sigma}$ is the asset return covariance matrix, and $\lambda$ is risk aversion.

Richard Michaud (1989) argued that standard MVO acts as an "error maximizer".
Because the optimizer treats sample estimates $\hat{\boldsymbol{\mu}}$ and $\hat{\mathbf{\Sigma}}$ as ground truth without estimation error, it systematically over-allocates capital to assets whose expected returns are overestimated and whose risks or correlations are underestimated.
DeMiguel, Garlappi, and Uppal (2009) found that none of the 14 sample-based optimizers they tested consistently beat the naive equal-weighted $1/N$ portfolio out of sample.

### 2. Covariance Matrix Estimation and Ledoit-Wolf Shrinkage

When universe size $N$ approaches or exceeds sample length $T$ ($N \ge T$), the sample covariance matrix $\mathbf{S} = \frac{1}{T-1}\mathbf{X}^T\mathbf{X}$ becomes rank-deficient, singular, and non-invertible.
Even when $T > N$, sample covariance matrices suffer from extreme eigenvalue dispersion: small eigenvalues are underestimated and large eigenvalues are overestimated.

The condition number $\kappa(\mathbf{\Sigma}) = \frac{\lambda_{\max}}{\lambda_{\min}}$ quantifies matrix inversion sensitivity.
A high condition number means small estimation errors in the inputs produce large swings in optimal portfolio weights.

Ledoit and Wolf introduced linear shrinkage, which gives a well-conditioned, invertible covariance matrix:

$$\mathbf{\Sigma}_{\text{LW}} = (1 - \delta^*) \mathbf{S} + \delta^* \mathbf{F}$$

Where:
- $\mathbf{S}$: Sample covariance matrix.
- $\mathbf{F}$: Structured shrinkage target: a single-index (market model) covariance (Ledoit and Wolf 2003), the constant-correlation matrix (Ledoit and Wolf 2004, *Journal of Portfolio Management*), or a scaled identity (Ledoit and Wolf 2004, *Journal of Multivariate Analysis*).
- $\delta^* \in [0, 1]$: Shrinkage intensity estimated from the data to minimize the expected squared Frobenius distance to the true covariance.

### 3. Risk Parity and Equal Risk Contribution (ERC)

Traditional "60/40" asset allocation (60% equities, 40% bonds) looks balanced in dollar terms, but with illustrative volatilities of $16\%$ for equities and $5\%$ for bonds, equities contribute $95.8\%$ of portfolio risk at zero correlation and $90.9\%$ at a correlation of $0.3$.

Risk Parity re-conceptualizes allocation in units of risk rather than units of capital.
Total portfolio volatility is:

$$\sigma_p(\mathbf{w}) = \sqrt{\mathbf{w}^T \mathbf{\Sigma} \mathbf{w}}$$

The Marginal Risk Contribution (MRC) of asset $i$ measures how total portfolio risk shifts with a marginal increase in weight $w_i$:

$$\text{MRC}_i = \frac{\partial \sigma_p}{\partial w_i} = \frac{(\mathbf{\Sigma} \mathbf{w})_i}{\sigma_p}$$

By Euler's homogeneous function theorem, total portfolio risk decomposes into the sum of asset Total Risk Contributions (TRC):

$$\sigma_p = \sum_{i=1}^N w_i \frac{\partial \sigma_p}{\partial w_i} = \sum_{i=1}^N \text{TRC}_i$$

An **Equal Risk Contribution (ERC)** portfolio satisfies:

$$\text{TRC}_i = \text{TRC}_j = \frac{\sigma_p}{N} \quad \forall i, j$$

$$w_i (\mathbf{\Sigma} \mathbf{w})_i = w_j (\mathbf{\Sigma} \mathbf{w})_j \quad \forall i, j$$

Because lower-volatility assets (e.g. government bonds) receive larger capital allocations to match the risk of volatile assets (e.g. equities), unlevered risk parity has low volatility, so risk parity funds typically apply leverage to reach a return target (Maillard, Roncalli, and Teiletche 2010 study the properties of ERC portfolios).

### 4. Hierarchical Risk Parity (HRP)

Marcos Lopez de Prado (2016) introduced Hierarchical Risk Parity (HRP) to address both the instability of MVO and the way standard risk parity ignores the correlation structure.
HRP never inverts the full covariance matrix ($\mathbf{\Sigma}^{-1}$), so it works even when $\mathbf{\Sigma}$ is singular.

HRP executes in three sequential stages:
1. **Tree Clustering**:
   - Define correlation distance: $d_{i, j} = \sqrt{\frac{1}{2}(1 - \rho_{i, j})}$.
   - Apply hierarchical agglomerative clustering (the paper uses single linkage on distances between the columns of $d$) to build a dendrogram.
2. **Quasi-Diagonalization**:
   - Reorder the rows and columns of the covariance matrix so that highly correlated assets are grouped adjacently along the primary diagonal.
3. **Recursive Bisection**:
   - Split the quasi-diagonally ordered list of assets into two halves (the paper bisects the ordered list, not the dendrogram's own branches).
   - Compute each half's variance $V_j$ using inverse-variance weights within the half.
   - Allocate capital between the two halves inversely to their variances ($\alpha_1 = 1 - \frac{V_1}{V_1 + V_2}$ and $\alpha_2 = \frac{V_1}{V_1 + V_2}$).
   - Repeat within each half until every asset has a weight.

---

## Worked examples

### Example 1: Calculating Risk Contributions in a 2-Asset Portfolio

Consider a portfolio allocated across Equities ($E$) and Bonds ($B$):
- Weights: $w_E = 0.60$, $w_B = 0.40$.
- Volatilities: $\sigma_E = 20.0\%$, $\sigma_B = 5.0\%$.
- Correlation: $\rho_{E, B} = 0.10$.

1. **Covariance Matrix**:
   $$\sigma_{E}^2 = (0.20)^2 = 0.0400$$
   $$\sigma_{B}^2 = (0.05)^2 = 0.0025$$
   $$\sigma_{E, B} = 0.20 \times 0.05 \times 0.10 = 0.0010$$
   $$\mathbf{\Sigma} = \begin{pmatrix} 0.0400 & 0.0010 \\ 0.0010 & 0.0025 \end{pmatrix}$$

2. **Portfolio Variance and Volatility**:
   $$\sigma_p^2 = (0.60)^2(0.0400) + (0.40)^2(0.0025) + 2(0.60)(0.40)(0.0010)$$
   $$\sigma_p^2 = 0.01440 + 0.00040 + 0.00048 = 0.01528$$
   $$\sigma_p = \sqrt{0.01528} = 12.36\%$$

3. **Marginal and Total Risk Contributions**:
   $$(\mathbf{\Sigma} \mathbf{w})_E = 0.60(0.0400) + 0.40(0.0010) = 0.0240 + 0.0004 = 0.0244$$
   $$(\mathbf{\Sigma} \mathbf{w})_B = 0.60(0.0010) + 0.40(0.0025) = 0.0006 + 0.0010 = 0.0016$$
   $$\text{TRC}_E = w_E \frac{(\mathbf{\Sigma} \mathbf{w})_E}{\sigma_p} = 0.60 \times \frac{0.0244}{0.1236} = \frac{0.01464}{0.1236} = 11.84\%$$
   $$\text{TRC}_B = w_B \frac{(\mathbf{\Sigma} \mathbf{w})_B}{\sigma_p} = 0.40 \times \frac{0.0016}{0.1236} = \frac{0.00064}{0.1236} = 0.52\%$$

4. **Percentage Risk Contributions**:
   $$\% \text{Risk}_E = \frac{11.84\%}{12.36\%} = 95.8\%$$
   $$\% \text{Risk}_B = \frac{0.52\%}{12.36\%} = 4.2\%$$

Despite holding 40% of capital in bonds, equities account for nearly $96\%$ of total portfolio risk.

### Example 2: Equal Risk Contribution Allocation (Uncorrelated Case)

For $N$ uncorrelated assets ($\rho_{i, j} = 0$), the ERC condition simplifies to:
$$w_i \sigma_i = w_j \sigma_j = k$$
$$w_i \propto \frac{1}{\sigma_i}$$

For the two assets above ($\sigma_E = 20\%$, $\sigma_B = 5\%$):
- $w_E \propto \frac{1}{20} = 0.05$
- $w_B \propto \frac{1}{5} = 0.20$
- Normalized weights:
  $$w_E = \frac{0.05}{0.05 + 0.20} = 20.0\%$$
  $$w_B = \frac{0.20}{0.05 + 0.20} = 80.0\%$$

Each asset now contributes exactly $50.0\%$ to total portfolio volatility.
For two assets this holds at any correlation: the script solves the ERC equations numerically at $\rho = -0.3, 0, 0.1, 0.5$ and gets $20\%$ and $80\%$ each time, because the cross term $w_E w_B \sigma_{E,B}$ appears in both assets' contributions.
With three or more assets, inverse volatility equals ERC only when all pairwise correlations are equal.

---

## Pitfalls

- **Ignoring Leverage Costs in Risk Parity**: Achieving equity-like returns from a bond-heavy risk parity portfolio requires leverage; higher financing rates erode net excess returns.
- **Inverting Ill-Conditioned Covariance Matrices**: Attempting raw inversion $\mathbf{\Sigma}^{-1}$ without shrinkage when $N \approx T$, generating extreme exploding weights and catastrophic out-of-sample turnover.
- **Correlation Regimes and Risk Parity Concentration**: Risk parity assumes the stock-bond correlation it estimated; in 2022 US stocks and bonds both fell for the calendar year, so the bond allocation that was meant to diversify added to losses.
- **Assuming Expected Returns Equal Zero in MVO**: Running minimum variance without expected return inputs produces concentrated allocations in low-beta, low-volatility sectors (utilities, REITs) that can carry structural business risks.
- **Omitting Turnover Penalty in Rebalancing**: Re-optimizing weights without a turnover penalty, either linear $\lambda_{\text{turn}} \|\mathbf{w}_t - \mathbf{w}_{t-1}\|_1$ for spread-like costs or quadratic for impact-like costs, which hands much of the alpha to trading costs.

---

## Interview questions

> [!question]- mkt-sys-065 | Why did Richard Michaud term Markowitz mean-variance optimization an "error maximizer"?
> Because MVO treats sample estimates as exact truths without error, systematically assigning the largest weights to securities whose expected returns are most overestimated and whose risks are most underestimated.

> [!question]- mkt-sys-066 | What is the condition number of a covariance matrix and what does a high value indicate?
> The condition number is the ratio of the largest eigenvalue to the smallest eigenvalue: kappa = lambda_max / lambda_min; a high value indicates ill-conditioning where small input errors produce massive swings in optimal weights.

> [!question]- mkt-sys-067 | What is Ledoit-Wolf shrinkage and what problem does it solve?
> Ledoit-Wolf shrinkage linearly combines the noisy sample covariance matrix with a structured target matrix to produce a well-conditioned, strictly invertible covariance matrix with reduced estimation error.

> [!question]- mkt-sys-068 | Define Marginal Risk Contribution (MRC) mathematically.
> MRC is the first partial derivative of portfolio volatility with respect to asset weight: MRC_i = d sigma_p / d w_i = (Sigma * w)_i / sigma_p.

> [!question]- mkt-sys-069 | State Euler's risk decomposition theorem for portfolio volatility.
> Because portfolio volatility sigma_p is a linearly homogeneous function of weights w, total risk decomposes exactly into sigma_p = sum_{i=1}^N w_i * (d sigma_p / d w_i) = sum_{i=1}^N TRC_i.

> [!question]- mkt-sys-070 | What is the Equal Risk Contribution (ERC) condition?
> ERC requires that every constituent asset contributes an identical amount of volatility to the portfolio: w_i * (Sigma * w)_i = w_j * (Sigma * w)_j for all i, j.

> [!question]- mkt-sys-071 | Why does a traditional 60/40 equity-bond portfolio have equity-dominated risk?
> Because equity volatility (say 16%) is more than three times bond volatility (say 5%), and variance scales with its square.
> With 60/40 weights, equities carry 95.8% of the risk at zero correlation and 90.9% at a correlation of 0.3.

> [!question]- mkt-sys-072 | How does Risk Parity achieve competitive equity-like returns if heavily weighted in bonds?
> It applies leverage, typically through futures or borrowing, scaling up the low-volatility diversified portfolio to the target volatility or return; the excess return must exceed the financing cost.

> [!question]- mkt-sys-073 | What is Hierarchical Risk Parity (HRP) and who invented it?
> Introduced by Marcos Lopez de Prado (2016, Journal of Portfolio Management), HRP clusters assets hierarchically on correlation distance and allocates top-down by inverse cluster variance, without inverting the covariance matrix.

> [!question]- mkt-sys-074 | State the three stages of the Hierarchical Risk Parity algorithm.
> The three stages are Tree Clustering (hierarchical grouping via correlation distance), Quasi-Diagonalization (reordering the covariance matrix so similar assets sit together), and Recursive Bisection (splitting the ordered list in halves and allocating by inverse cluster variance).

> [!question]- mkt-sys-075 | Why is HRP immune to the singularity problems of Markowitz MVO?
> Because HRP does not invert the covariance matrix (no Sigma^{-1}); it allocates weights top-down using recursive bisection based only on sub-cluster variances, which exist even when Sigma is singular.

> [!question]- mkt-sys-076 | What is correlation distance in hierarchical clustering?
> Correlation distance is defined as d_{i, j} = sqrt(0.5 * (1 - rho_{i, j})), which forms a true metric space satisfying non-negativity, symmetry, and triangle inequality.

> [!question]- mkt-sys-077 | What is the inverse volatility portfolio?
> An allocation where each asset's weight is inversely proportional to its individual volatility: w_i = (1 / sigma_i) / sum_j (1 / sigma_j); it matches ERC only when pairwise correlations are identical.

> [!question]- mkt-sys-078 | What happens to sample covariance rank when universe size N exceeds sample days T?
> When N > T, the sample covariance matrix has rank at most T - 1, creating zero eigenvalues and rendering the matrix singular and non-invertible.

> [!question]- mkt-sys-079 | What is the single-index shrinkage target in Ledoit-Wolf estimation?
> A structured target matrix where asset variances match sample variances, but all pairwise covariances are modeled via a single market factor: Cov(i, j) = beta_i * beta_j * sigma_m^2.

> [!question]- mkt-sys-080 | How does Black-Litterman improve on standard Markowitz optimization?
> Black-Litterman uses reverse optimization to infer the market's implied equilibrium returns, then blends them with investor subjective views using Bayesian probability to produce stable, intuitive weights.

> [!question]- mkt-sys-081 | What is a turnover penalty in quadratic programming portfolio optimization?
> A penalty term lambda_turn * sum_i |w_{i, t} - w_{i, t-1}| added to the objective function that penalizes trades, preventing the optimizer from churning capital for tiny alpha gains.

> [!question]- mkt-sys-082 | What is the de-leveraging spiral in leveraged risk parity funds?
> During market crises when asset correlations spike and volatilities rise, leveraged risk parity funds are forced to liquidate positions to maintain target volatility, exacerbating market selloffs.

> [!question]- mkt-sys-083 | What are box constraints in portfolio optimization?
> Lower and upper bounds on individual asset weights: w_{min} <= w_i <= w_{max}, preventing extreme concentration in single names.

> [!question]- mkt-sys-084 | What is factor neutrality in equity portfolio construction?
> Enforcing linear constraints such that portfolio exposure to common risk factors (e.g. beta, size, value, momentum) is strictly zero: B^T * w = 0.

> [!question]- mkt-sys-085 | What is the minimum variance portfolio (MVP)?
> The portfolio on the efficient frontier that achieves the absolute lowest variance regardless of expected return: w_{MVP} = Sigma^{-1} * 1 / (1^T * Sigma^{-1} * 1).

> [!question]- mkt-sys-086 | Why does equal-weighting (1/N) often beat sample MVO out of sample (DeMiguel et al. 2009)?
> Because 1/N has no estimation error, while sample MVO's estimation errors, especially in expected returns, outweigh its theoretical advantage unless the estimation window is very long; DeMiguel et al. found none of 14 models consistently beat 1/N out of sample.

> [!question]- mkt-sys-087 | How does the Frobenius norm evaluate shrinkage intensity?
> The Frobenius norm measures matrix distance: ||Sigma - Target||_F^2 = sum_{i, j} (Sigma_{i, j} - Target_{i, j})^2; optimal shrinkage minimizes the expected Frobenius loss.

> [!question]- mkt-sys-088 | What is the difference between single linkage and average linkage in HRP?
> Single linkage defines distance between clusters as the minimum pairwise distance, while average linkage takes the average of all pairwise distances, creating more balanced clusters.

> [!question]- mkt-sys-089 | What is quasi-diagonalization in HRP?
> Reordering rows and columns of the covariance matrix according to dendrogram leaf order so that correlated assets cluster together along the diagonal, revealing tree hierarchy.

> [!question]- mkt-sys-090 | What is recursive bisection in HRP?
> Splitting the quasi-diagonally ordered asset list into two halves, assigning capital between them by inverse cluster variance (each half's variance computed with inverse-variance weights inside it), and repeating until every asset has a weight.

> [!question]- mkt-sys-091 | How does portfolio volatility behave when all asset correlations equal 1.0?
> Portfolio volatility equals the weighted sum of individual asset volatilities: sigma_p = sum_i w_i * sigma_i; all diversification benefits completely vanish.

> [!question]- mkt-sys-092 | What is the diversification ratio of a portfolio (Choueifaty and Coignard 2008)?
> The ratio of the weighted average asset volatility to total portfolio volatility: DR(w) = (w^T * sigma) / sqrt(w^T * Sigma * w); higher DR indicates superior diversification.

> [!question]- mkt-sys-093 | How do borrowing rate spreads penalize leveraged risk parity portfolios?
> Investors borrow at rates above the risk-free rate (e.g. SOFR + spread); if the spread exceeds the risk-adjusted excess return of the levered assets, net returns turn negative.

> [!question]- mkt-sys-094 | What is the maximum Sharpe ratio (tangency) portfolio?
> The portfolio on the efficient frontier that maximizes (mu_p - r_f) / sigma_p, formed as w_{tangency} = Sigma^{-1} * (mu - r_f * 1) / (1^T * Sigma^{-1} * (mu - r_f * 1)).

> [!question]- mkt-sys-095 | What is semi-variance optimization and why is it used?
> Measuring risk using only downside deviations below a benchmark or zero, avoiding penalizing upside volatility that benefits investors.

> [!question]- mkt-sys-096 | Why is quadratic programming used to solve constrained portfolio optimization?
> Because portfolio variance is a quadratic function of weights (w^T * Sigma * w) while common real-world constraints (budget, sector bounds, leverage) are linear, fitting quadratic programming algorithms.

> [!question]- mkt-sys-258 | For two assets with volatilities 20% and 5%, does the ERC weighting depend on their correlation?
> No: it is 20% and 80%, inverse volatility, at any correlation.
> Each asset's contribution is w_i^2 sigma_i^2 + w_E w_B sigma_EB, so equal contributions need only w_E sigma_E = w_B sigma_B.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../code/mkt_sys_03_portfolio.py`](../code/mkt_sys_03_portfolio.py) prints and asserts every number on this page: variance by scalar expansion and matrix product, risk contributions by finite differences of portfolio volatility, ERC weights by a cyclical Newton solver, the minimum-variance and tangency formulas against a random search, the correlation-distance triangle inequality, and sample-covariance rank.
- Related notes: [Mean-Variance Portfolio Construction](../../09-Alpha-Research-and-Portfolio/10-Mean-Variance-Portfolio-Construction.md), [Covariance Estimation and Shrinkage](../../09-Alpha-Research-and-Portfolio/11-Covariance-Estimation-and-Shrinkage.md), [Black-Litterman, Risk Parity and HRP](../../09-Alpha-Research-and-Portfolio/12-Black-Litterman-Risk-Parity-and-HRP.md).

## Further reading

- Choueifaty, Y., & Coignard, Y. (2008). Toward maximum diversification. *The Journal of Portfolio Management*, 35(1), 40-51.
- DeMiguel, V., Garlappi, L., & Uppal, R. (2009). Optimal versus naive diversification: How inefficient is the 1/N portfolio strategy? *The Review of Financial Studies*, 22(5), 1915-1953.
- Ledoit, O., & Wolf, M. (2003). Improved estimation of the covariance matrix of stock returns with an application to portfolio selection. *Journal of Empirical Finance*, 10(5), 603-621.
- Ledoit, O., & Wolf, M. (2004). Honey, I shrunk the sample covariance matrix. *The Journal of Portfolio Management*, 30(4), 110-119.
- Ledoit, O., & Wolf, M. (2004). A well-conditioned estimator for large-dimensional covariance matrices. *Journal of Multivariate Analysis*, 88(2), 365-411.
- Lopez de Prado, M. (2016). Building diversified portfolios that outperform out of sample. *The Journal of Portfolio Management*, 42(4), 59-69.
- Markowitz, H. (1952). Portfolio selection. *The Journal of Finance*, 7(1), 77-91.
- Maillard, S., Roncalli, T., & Teiletche, J. (2010). The properties of equally weighted risk contribution portfolios. *The Journal of Portfolio Management*, 36(4), 60-70.
- Michaud, R. O. (1989). The Markowitz optimization enigma: Is 'optimized' optimal? *Financial Analysts Journal*, 45(1), 31-42.
- Roncalli, T. (2013). *Introduction to Risk Parity and Budgeting*. Chapman and Hall/CRC.
