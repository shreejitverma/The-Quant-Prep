---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Qian (2005) - Risk Parity Portfolios: Efficient Portfolios Through True Diversification, Maillard Roncalli and Teiletche (2010) - The Properties of Equally Weighted Risk Contribution Portfolios, Asness Frazzini and Pedersen (2012) - Leverage Aversion and Risk Parity, Bridgewater Associates (2012) - The All Weather Story, Griveau-Billion Richard and Roncalli (2013) - A Fast Algorithm for Computing High-Dimensional Risk Parity Portfolios]
---

# Risk Parity and The All-Weather Framework

## TL;DR

- A 60/40 equity/bond portfolio is balanced in capital, not in risk: with hypothetical volatilities of 16% for equities and 5% for bonds and zero correlation, equities contribute 95.84% of portfolio variance.
- Risk Parity equalizes the Total Risk Contribution (TRC) of every asset class (Qian 2005), so no single asset class dominates portfolio volatility.
- Risk contributions come from Euler's decomposition: $\text{TRC}_i = w_i \frac{(\mathbf{\Sigma}\mathbf{w})_i}{\sigma_p}$, and the Risk Parity condition requires $\text{TRC}_i = \frac{\sigma_p}{N}$ for all $i$.
- Bridgewater's All Weather strategy, launched in 1996, maps asset classes to four economic environments (rising or falling growth, rising or falling inflation, relative to expectations) and puts 25% of the risk in each (Bridgewater, *The All Weather Story*, 2012).
- Equalizing risk overweights low-volatility bonds, so reaching an equity-like return requires leverage, which exposes the strategy to financing costs and to periods when stocks and bonds fall together, as in 2022.

## Learning objectives

- Prove that a capital-weighted 60/40 portfolio concentrates most of its variance in equities.
- Derive Marginal Contribution to Risk (MCR) and Total Risk Contribution (TRC) using Euler's homogeneous function theorem.
- Formulate the convex optimization problem for finding Equal Risk Contribution (ERC) portfolio weights.
- Construct Bridgewater's four-environment All Weather framework matching asset classes to growth and inflation surprises.
- Analyze the structural vulnerabilities of levered risk parity during simultaneous equity and bond drawdowns (such as 2022).

## Core concepts

### 1. The 60/40 Risk Concentration Fallacy

Consider a standard institutional portfolio consisting of 60% equities and 40% government bonds, with hypothetical inputs:

- Equity volatility: $\sigma_E = 16.0\%$
- Bond volatility: $\sigma_B = 5.0\%$
- Correlation: $\rho_{E,B} = 0.0$

Portfolio variance is:

$$\sigma_p^2 = w_E^2 \sigma_E^2 + w_B^2 \sigma_B^2 + 2 w_E w_B \rho_{E,B} \sigma_E \sigma_B$$

$$\sigma_p^2 = (0.60)^2 (0.16)^2 + (0.40)^2 (0.05)^2 + 0 = 0.009216 + 0.000400 = 0.009616$$

$$\sigma_p = \sqrt{0.009616} \approx 9.806\%$$

The proportion of total portfolio variance originating from equities is:

$$\frac{w_E^2 \sigma_E^2}{\sigma_p^2} = \frac{0.009216}{0.009616} = 95.84\%$$

```
+-----------------------------------------------------------------------+
|                    THE 60/40 CAPITAL VS RISK ILLUSION                 |
+-----------------------------------------------------------------------+
| Capital Allocation                    Risk Allocation (Variance)      |
| [========================] Equities 60% [========================] 95.84%
| [================] Bonds 40%           [=] Bonds 4.16%                |
+-----------------------------------------------------------------------+
```

Although the capital allocation appears balanced, the portfolio's ups and downs are almost entirely driven by the equity market.

### 2. Mathematical Formulation of Risk Contributions

Let $\mathbf{w} \in \mathbb{R}^N$ be the portfolio weight vector such that $\sum_{i=1}^N w_i = 1$ and $w_i \ge 0$.
Let $\mathbf{\Sigma} \in \mathbb{R}^{N \times N}$ be the asset covariance matrix.
Portfolio standard deviation is:

$$\sigma_p(\mathbf{w}) = \sqrt{\mathbf{w}^T \mathbf{\Sigma} \mathbf{w}}$$

Because $\sigma_p(\mathbf{w})$ is a linearly homogeneous function of degree 1 (i.e., $\sigma_p(c\mathbf{w}) = c \sigma_p(\mathbf{w})$ for $c > 0$), Euler's homogeneous function theorem applies:

$$\sigma_p(\mathbf{w}) = \sum_{i=1}^N w_i \frac{\partial \sigma_p(\mathbf{w})}{\partial w_i}$$

The Marginal Contribution to Risk ($\text{MCR}_i$) of asset $i$ is:

$$\text{MCR}_i = \frac{\partial \sigma_p(\mathbf{w})}{\partial w_i} = \frac{(\mathbf{\Sigma} \mathbf{w})_i}{\sqrt{\mathbf{w}^T \mathbf{\Sigma} \mathbf{w}}} = \frac{\text{Cov}(R_i, R_p)}{\sigma_p}$$

The Total Risk Contribution ($\text{TRC}_i$) of asset $i$ is:

$$\text{TRC}_i = w_i \cdot \text{MCR}_i = w_i \frac{(\mathbf{\Sigma} \mathbf{w})_i}{\sigma_p}$$

The sum of all total risk contributions equals total portfolio volatility:

$$\sum_{i=1}^N \text{TRC}_i = \frac{\mathbf{w}^T \mathbf{\Sigma} \mathbf{w}}{\sigma_p} = \sigma_p$$

The Equal Risk Contribution (ERC) or Risk Parity condition requires:

$$\text{TRC}_i = \text{TRC}_j = \frac{\sigma_p}{N} \quad \forall i, j$$

In percentage terms, the relative risk contribution of each asset must be identical:

$$\% \text{TRC}_i = \frac{\text{TRC}_i}{\sigma_p} = \frac{1}{N}$$

### 3. Convex Optimization for Risk Parity Weights

Unlike Mean-Variance Optimization, which requires forecasting expected returns $\boldsymbol{\mu}$, Risk Parity requires only the covariance matrix $\mathbf{\Sigma}$.
Maillard, Roncalli, and Teiletche (2010) showed that the Equal Risk Contribution portfolio can be found by solving a strictly convex optimization problem:

$$\mathbf{x}^* = \arg\min_{\mathbf{x}} \left\{ \frac{1}{2} \mathbf{x}^T \mathbf{\Sigma} \mathbf{x} - c \sum_{i=1}^N \ln(x_i) \right\}$$

subject to $x_i > 0$, where $c > 0$ is an arbitrary scaling constant.
The gradient of the objective function is:

$$\nabla_{\mathbf{x}} f = \mathbf{\Sigma} \mathbf{x} - \frac{c}{\mathbf{x}} = \mathbf{0} \implies x_i (\mathbf{\Sigma} \mathbf{x})_i = c \quad \forall i$$

This condition precisely matches the unnormalized risk parity requirement.
The final normalized weights are obtained by:

$$w_i = \frac{x_i^*}{\sum_{j=1}^N x_j^*}$$

When assets are mutually uncorrelated ($\rho_{i,j} = 0$), or more generally when all pairwise correlations are equal, the risk parity weight is simply inversely proportional to asset volatility:

$$w_i \propto \frac{1}{\sigma_i}$$

When correlations differ, the solution gives less weight to assets that are more correlated with the rest of the portfolio.

### 4. Bridgewater's All Weather Framework

Bridgewater Associates' own account, *The All Weather Story* (2012), says that Ray Dalio, Bob Prince, Greg Jensen, Dan Bernstein and others developed All Weather over decades, that it was launched in 1996 for Dalio's trust assets, and that it is passive.
Its premise is that asset prices move mainly on surprises in economic growth and inflation relative to what is discounted, so the strategy maps each asset class to the environments it is biased toward and puts equal risk in each:

```
+-----------------------------------------------------------------------+
|        ALL WEATHER: FOUR ENVIRONMENTS (relative to expectations)      |
+-----------------------------------------------------------------------+
|                     |  RISING                 |  FALLING              |
+---------------------+-------------------------+-----------------------+
| GROWTH              |  25% of risk            |  25% of risk          |
|                     |  Equities, Commodities, |  Nominal Bonds,       |
|                     |  Corporate Credit,      |  IL Bonds             |
|                     |  EM Credit              |                       |
+---------------------+-------------------------+-----------------------+
| INFLATION           |  25% of risk            |  25% of risk          |
|                     |  IL Bonds, Commodities, |  Equities,            |
|                     |  EM Credit              |  Nominal Bonds        |
+---------------------+-------------------------+-----------------------+
```

(IL Bonds are inflation-linked bonds such as TIPS.)
Every asset class has an environmental bias in this map:
- **Equities** do well when growth rises and when inflation falls.
- **Nominal government bonds** do well when growth falls and when inflation falls.
- **Inflation-linked bonds** do well when growth falls and when inflation rises.
- **Commodities** do well when growth rises and when inflation rises.

Because each environment holds 25% of the risk, the portfolio does not depend on predicting which environment comes next.
Bridgewater also notes that the boxes do not cancel completely: the assets earn a positive return over cash over time, which is what the portfolio collects.

### 5. Leverage Mechanics and The 2022 Vulnerability

Because government bonds have low volatility compared to equities and commodities, an unlevered risk parity portfolio holds most of its capital in bonds.
With the hypothetical volatilities of 16% (equities), 5% (Treasuries) and 20% (commodities) and zero correlations, inverse-volatility weights put 64% of capital in Treasuries and give a portfolio volatility of only 5.54%.
Reaching a 10% volatility target therefore needs about 1.80 times leverage on these inputs.

```
        LEVERED RISK PARITY STRUCTURE
        
Investor Capital ($100) ------------------------+
                                                |
Borrow Cash ($100 at Cash Rate r) ----+         |
                                      |         |
                                      v         v
                     Total Exposure ($200: 2.0x Leverage)
                                      |
         +----------------------------+----------------------------+
         |                            |                            |
         v                            v                            v
    $40 Equities                 $128 Treasuries              $32 Commodities
   (Risk: 33.3%)                 (Risk: 33.3%)                 (Risk: 33.3%)
```

The split uses inverse-volatility weights with the volatilities above (16%, 5%, 20%), which equalize risk contributions when pairwise correlations are equal.
Weights are proportional to $1/0.16 = 6.25$, $1/0.05 = 20$ and $1/0.20 = 5$, which sum to 31.25, so equities get $200 \times 6.25 / 31.25 = \$40$, Treasuries $\$128$ and commodities $\$32$.
Each sleeve then carries the same standalone dollar volatility: $40 \times 16\% = 128 \times 5\% = 32 \times 20\% = \$6.40$.

Levered risk parity depends on bonds diversifying equities and on cheap financing, so it has three main failure modes:

1. **Correlation Breakdown ($\rho_{E,B} > 0$)**:
   When inflation surprises upward and central banks tighten, stocks and nominal bonds can fall together, which removes the diversification the leverage relies on; US stocks and Treasuries both fell in calendar 2022.

2. **Cost of Leverage Spike**:
   Leverage is financed at short rates; the Federal Reserve raised its federal funds target range from 0-0.25% before March 2022 to 5.25-5.50% in July 2023 (FOMC statements), which raised the cost of carrying levered bond positions.

3. **Forced Deleveraging Spirals**:
   If both stocks and bonds suffer drawdowns while market volatility rises, risk-parity volatility-targeting rules mandate selling assets into a falling market to preserve risk targets.

---

## Flashcard drill bank

> [!question]- mkt-pf-161 | What is the primary conceptual flaw of a traditional 60/40 capital allocation?
> Equity volatility dominates bond volatility, so equities generate most of the portfolio's variance: 95.84% with hypothetical volatilities of 16% and 5% at zero correlation.

> [!question]- mkt-pf-162 | What is the core objective of a Risk Parity strategy?
> To allocate capital such that every asset class contributes an equal amount to total portfolio risk.

> [!question]- mkt-pf-163 | What mathematical theorem allows portfolio standard deviation to be decomposed into additive risk contributions?
> Euler's homogeneous function theorem, because standard deviation is linearly homogeneous of degree 1 with respect to asset weights.

> [!question]- mkt-pf-164 | What is the formula for the Marginal Contribution to Risk (MCR_i) of asset i?
> MCR_i = (Sigma * w)_i / sigma_p = Cov(R_i, R_p) / sigma_p.

> [!question]- mkt-pf-165 | What is the formula for the Total Risk Contribution (TRC_i) of asset i?
> TRC_i = w_i * MCR_i = w_i * (Sigma * w)_i / sigma_p.

> [!question]- mkt-pf-166 | What is the mathematical condition for an Equal Risk Contribution (ERC) portfolio?
> TRC_i = TRC_j = sigma_p / N for all assets i and j.

> [!question]- mkt-pf-167 | If all assets in a portfolio have zero mutual correlation, how are risk parity weights determined?
> Weights are inversely proportional to individual asset volatilities: w_i proportional to 1 / sigma_i (this also holds when all pairwise correlations are equal).

> [!question]- mkt-pf-168 | What convex optimization problem solves for Equal Risk Contribution weights?
> Minimize 0.5 * x^T * Sigma * x - c * sum(ln(x_i)), followed by normalizing weights w_i = x_i / sum(x_j).

> [!question]- mkt-pf-169 | Who pioneered the All Weather investment strategy?
> Bridgewater Associates: Bridgewater credits Ray Dalio, Bob Prince, Greg Jensen, Dan Bernstein and others, and dates the launch to 1996.

> [!question]- mkt-pf-170 | What are the two primary macroeconomic drivers in the All Weather framework?
> Economic growth and inflation, specifically whether they come in higher or lower than market expectations.

> [!question]- mkt-pf-171 | Which assets perform best in a rising growth and falling inflation regime?
> Equities, which appear in both the rising-growth and the falling-inflation boxes of Bridgewater's map; corporate and EM credit also sit in the rising-growth box.

> [!question]- mkt-pf-172 | Which assets perform best in a falling growth and falling inflation regime?
> Nominal government bonds, which appear in both the falling-growth and the falling-inflation boxes.

> [!question]- mkt-pf-173 | Which assets perform best in a rising inflation and rising growth regime?
> Commodities and EM credit, which appear in both the rising-inflation and the rising-growth boxes of Bridgewater's map.

> [!question]- mkt-pf-174 | Which assets perform best in a stagflation regime (rising inflation and falling growth)?
> Inflation-linked bonds, which appear in both the rising-inflation and the falling-growth boxes; commodities also sit in the rising-inflation box.

> [!question]- mkt-pf-175 | Why does an unlevered Risk Parity portfolio require high capital allocation to government bonds?
> Because government bonds have low volatility, so it takes much more capital in bonds to match the risk of equities; with hypothetical volatilities of 16%, 5% and 20%, Treasuries get 64% of capital.

> [!question]- mkt-pf-176 | Why do institutional Risk Parity funds apply leverage?
> To lift the return of a risk-balanced, bond-heavy portfolio to a target volatility or return comparable with equity-heavy portfolios.

> [!question]- mkt-pf-177 | What typical leverage range is utilized by institutional Risk Parity funds?
> It depends on the target volatility: leverage = target volatility / unlevered volatility, e.g. 10% / 5.54% = 1.80 times for the note's hypothetical three-asset portfolio; no single industry range applies.

> [!question]- mkt-pf-178 | How is leverage typically implemented in risk parity portfolios?
> Through exchange-traded futures contracts (e.g., Treasury futures) and cash repo borrowing.

> [!question]- mkt-pf-179 | What happened to Risk Parity portfolios during the 2022 market downturn?
> Stocks and nominal bonds fell together as inflation surged and policy rates rose, so the bond leg did not hedge the equity leg and levered bond exposure added to losses.

> [!question]- mkt-pf-180 | What is the correlation sign between stocks and nominal bonds during demand-driven recessions?
> Negative correlation (flight to safety), allowing bonds to hedge equities effectively.

> [!question]- mkt-pf-181 | What is the correlation sign between stocks and nominal bonds during supply-driven inflation shocks?
> Positive correlation, meaning bonds fail to hedge equities and both suffer losses.

> [!question]- mkt-pf-182 | How does a rise in short-term interest rates impact a levered Risk Parity fund?
> It increases borrowing costs (repo financing spread) and creates a cash drag that reduces net carry.

> [!question]- mkt-pf-183 | What is a 'volatility-targeted' Risk Parity strategy?
> A strategy that rescales overall portfolio leverage inversely to realized portfolio volatility to maintain a constant volatility target (e.g., 10% or 12%).

> [!question]- mkt-pf-184 | What is the risk of volatility targeting during a sudden liquidity crisis?
> Deleveraging feedback loops: rising volatility forces the fund to liquidate assets at market bottoms.

> [!question]- mkt-pf-185 | How does Risk Parity differ from Mean-Variance Optimization (Markowitz)?
> Risk Parity ignores expected return estimates (mu) entirely, avoiding the massive parameter estimation error inherent in return forecasting.

> [!question]- mkt-pf-186 | What is the 'Betting Against Beta' (BAB) anomaly documented by Frazzini and Pedersen (2014)?
> High-beta assets deliver low risk-adjusted returns while low-beta assets deliver high risk-adjusted returns, because constrained investors bid up high-beta assets to achieve leverage.

> [!question]- mkt-pf-187 | How does the Betting Against Beta anomaly justify levering low-volatility bonds in Risk Parity?
> Asness, Frazzini and Pedersen (2012) argue that leverage-averse investors overpay for high-risk assets, so levering a risk-balanced portfolio of safer assets has historically earned a higher Sharpe ratio than holding the riskier assets unlevered.

> [!question]- mkt-pf-188 | What is an 'All Weather' portfolio risk budget allocation?
> 25% of total portfolio risk allocated to each of the four macro quadrants: rising growth, falling growth, rising inflation, falling inflation.

> [!question]- mkt-pf-189 | What is the role of gold in an All Weather risk-balanced portfolio?
> Gold is not in Bridgewater's published four-box map; investors who add it usually treat it as a hedge against currency debasement and inflation, which places it with the rising-inflation assets.

> [!question]- mkt-pf-190 | How does asset illiquidity impact risk parity rebalancing?
> Illiquid assets cannot be dynamically rebalanced without prohibitive transaction costs and market impact, distorting targeted risk parity weights.

> [!question]- mkt-pf-191 | What is cyclical coordinate descent in risk parity optimization?
> An iterative numerical optimization algorithm that updates each asset weight sequentially while holding other weights fixed to satisfy the ERC condition (Griveau-Billion, Richard and Roncalli 2013).

> [!question]- mkt-pf-192 | What is the primary operational lesson from Risk Parity theory?
> Diversify by true economic risk contribution across distinct macro environments rather than nominal dollar allocations.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_pm_06_risk_parity.py`](../../code/mkt_pm_06_risk_parity.py) prints and asserts every computed number on this page: the 60/40 variance terms in exact fractions against Euler contributions from a finite-difference gradient and a seeded simulation, equal-risk-contribution weights by Newton's method on the log-barrier problem against cyclical coordinate descent and the inverse-volatility closed form, and the levered sleeves in exact fractions with the unlevered volatility checked by simulation.
- Related notes: [Asset Allocation and The Benchmark to Beat](01-Asset-Allocation-and-The-Benchmark-to-Beat.md) (the 60/40 policy portfolio), [Factor Investing: Evidence, Replication, and Factor Decay](02-Factor-Investing-Evidence-Replication-and-Decay.md) (Betting Against Beta), [Macro Regimes and Debt Cycles](07-Macro-Regimes-and-Debt-Cycles.md) (growth and inflation regimes).

## Further reading

- Asness, C. S., Frazzini, A., & Pedersen, L. H. (2012). *Leverage Aversion and Risk Parity*. Financial Analysts Journal, 68(1), 47-59.
- Bridgewater Associates (2012). *The All Weather Story*. Bridgewater Associates.
- Griveau-Billion, T., Richard, J.-C., & Roncalli, T. (2013). *A Fast Algorithm for Computing High-Dimensional Risk Parity Portfolios*. Working paper.
- Maillard, S., Roncalli, T., & Teiletche, J. (2010). *The Properties of Equally Weighted Risk Contribution Portfolios*. Journal of Portfolio Management, 36(4), 60-70.
- Qian, E. (2005). *Risk Parity Portfolios: Efficient Portfolios Through True Diversification*. PanAgora Asset Management White Paper.
