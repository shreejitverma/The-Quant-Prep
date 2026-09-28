---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [heavy-tails-and-extreme-value-theory]
est_hours: 3
sources: [Jorion (2006) Value at Risk 3rd ed. McGraw-Hill, Artzner Delbaen Eber and Heath (1999) Coherent measures of risk. Mathematical Finance 9(3) 203-228, McNeil Frey and Embrechts (2015) Quantitative Risk Management revised ed. Princeton, Kupiec (1995) Techniques for verifying the accuracy of risk measurement models. Journal of Derivatives 3(2), Christoffersen (1998) Evaluating interval forecasts. International Economic Review 39(4), Basel Committee (1996) Supervisory framework for the use of backtesting in conjunction with the internal models approach to market risk capital requirements, Basel Committee (2019) Minimum capital requirements for market risk, Gneiting (2011) Making and evaluating point forecasts. Journal of the American Statistical Association 106(494)]
---

# Value at Risk and Expected Shortfall

## TL;DR

- VaR at level $\alpha$ is the $\alpha$-quantile of the loss distribution over a horizon: "99% one-day VaR of 1m" means a loss above 1m is expected on about 1 day in 100; it says nothing about how big that loss is.
- Expected shortfall is the average loss in the worst $1-\alpha$ of outcomes; for a normal, 99% VaR is $2.326\sigma$ and 99% ES is $2.665\sigma$.
- Three ways to compute them: parametric (delta-normal), historical simulation and Monte Carlo with full revaluation; each fails differently (fat tails, short windows, model error).
- VaR is not subadditive, so it can penalise diversification; ES is coherent, which is one reason the Basel market-risk rules (FRTB) moved to 97.5% ES.
- Backtest VaR by counting exceptions: at 99% over 250 days expect 2.5; Kupiec's test checks the count and Christoffersen's also checks clustering.

## Learning objectives

- Compute parametric, historical and Monte Carlo VaR and ES.
- Explain why VaR is not coherent and ES is.
- Backtest a VaR model.

## Core concepts

### Definitions

Let $L$ be the loss (negative P&L) over a fixed horizon.

$$
\text{VaR}_\alpha(L) = \inf\{\ell : P(L \le \ell) \ge \alpha\}, \qquad \text{ES}_\alpha(L) = \frac{1}{1-\alpha}\int_\alpha^1 \text{VaR}_u(L)\,du.
$$

For a continuous loss distribution, $\text{ES}_\alpha = \mathbb{E}[L \mid L \ge \text{VaR}_\alpha]$.
For a normal loss with mean 0 and standard deviation $\sigma$,

$$
\text{VaR}_\alpha = z_\alpha\sigma, \qquad \text{ES}_\alpha = \frac{\varphi(z_\alpha)}{1-\alpha}\,\sigma.
$$

| Level | $z_\alpha$ | ES multiple |
| :--- | ---: | ---: |
| 95% | 1.645 | 2.063 |
| 97.5% | 1.960 | 2.338 |
| 99% | 2.326 | 2.665 |

Under normality, 97.5% ES (2.338) is almost identical to 99% VaR (2.326); the difference shows up only when tails are fat.

### Parametric (delta-normal) VaR

Map the book to risk-factor sensitivities $w$ (dollar deltas) and assume factor returns are normal with covariance $\Sigma$.
Then the P&L is normal with standard deviation $\sigma_P = \sqrt{w^\top\Sigma w}$ and $\text{VaR}_\alpha = z_\alpha\sigma_P$.
It is fast and additive in a useful way: the Euler (component) allocation

$$
\text{CVaR}_i = w_i\,\frac{\partial\,\text{VaR}}{\partial w_i} = z_\alpha\,\frac{w_i(\Sigma w)_i}{\sigma_P}
$$

sums exactly to the total because VaR here is homogeneous of degree one in $w$.
Weaknesses: normal tails, linear payoffs (options need delta-gamma or full revaluation) and a covariance estimate that is stale in a crisis.
Scaling one-day VaR to $h$ days by $\sqrt{h}$ assumes i.i.d. returns and a constant position.

### Historical simulation

Apply each of the last $N$ days of factor moves to today's portfolio, revalue, and read the empirical quantile of the resulting P&L.
With $N = 500$ and $\alpha = 99\%$ there are only 5 tail observations: the estimate is noisy and jumps when a large day enters or leaves the window.
It captures fat tails and nonlinearity that happened in the window, and nothing that did not.
Filtered historical simulation rescales past returns by the ratio of current to past volatility (for example from a GARCH model, see [Volatility Models: GARCH](../02-Statistics-and-Econometrics/09-Volatility-Models-GARCH.md)) to make the window reflect today's regime.

### Monte Carlo

Simulate factor moves from a fitted model (multivariate normal, Student-$t$, copula plus fat-tailed marginals), revalue the whole book in every scenario, and take the empirical quantile and tail mean.
It handles options and path dependence and lets you choose tail behaviour, at the cost of compute and model risk.
The standard error of a tail quantile estimate is roughly $\sqrt{\alpha(1-\alpha)/n}/f(\text{VaR})$, so far-tail estimates need many scenarios.

### Fat tails

Real daily returns have excess kurtosis (see [Heavy Tails and Extreme Value Theory](../02-Statistics-and-Econometrics/13-Heavy-Tails-and-Extreme-Value-Theory.md)).
A Student-$t$ with 4 degrees of freedom, rescaled to unit variance, has 99% VaR 2.649 (normal 2.326) and 99% ES 3.692 (normal 2.665).
At 99.9% the gap widens to 5.07 against 3.09.
Matching the variance does not match the tail: the further out you look, the more the normal understates.

### Coherence

Artzner, Delbaen, Eber and Heath call a risk measure $\rho$ coherent if it is

- monotone: $L_1 \le L_2$ implies $\rho(L_1) \le \rho(L_2)$;
- translation invariant: $\rho(L + c) = \rho(L) + c$;
- positively homogeneous: $\rho(\lambda L) = \lambda\rho(L)$ for $\lambda \ge 0$;
- subadditive: $\rho(L_1 + L_2) \le \rho(L_1) + \rho(L_2)$.

VaR satisfies the first three but not subadditivity: combining two positions can raise VaR above the sum, which punishes diversification and invites splitting a book to game limits.
VaR is subadditive for elliptical distributions such as the multivariate normal; the failures come from discrete, skewed or very heavy-tailed losses (credit, short options).
ES is coherent for all distributions.
The catch is that ES is not elicitable (Gneiting 2011): there is no scoring function whose expected value is minimised by the true ES, which makes ES harder to backtest directly than VaR.

### Backtesting

Record each day whether the realised loss exceeded that day's VaR (an exception).
Under a correct 99% model, exceptions are i.i.d. Bernoulli(0.01).

- Kupiec proportion-of-failures test: with $x$ exceptions in $T$ days and $\hat p = x/T$,
  $\text{LR}_{\text{POF}} = -2\ln\frac{(1-p)^{T-x}p^x}{(1-\hat p)^{T-x}\hat p^x} \sim \chi^2_1$.
- Christoffersen's independence test checks that an exception today does not make one tomorrow more likely; clustered exceptions mean the model reacts too slowly to volatility.
- The Basel traffic light for 99% VaR over 250 days: 0 to 4 exceptions green, 5 to 9 yellow (capital multiplier add-on), 10 or more red.

Backtest against clean P&L (the P&L of the start-of-day portfolio, excluding intraday trading and fees), otherwise you are testing the wrong thing.

## Worked examples

### Example 1: parametric VaR and ES

A 10m position with daily volatility 1.5%, P&L assumed normal with zero mean.
$\sigma_P = 150{,}000$.
99% one-day VaR is $2.326 \times 150{,}000 \approx 349{,}000$.
99% one-day ES is $2.665 \times 150{,}000 \approx 400{,}000$.
Ten-day VaR by the square-root rule is $349{,}000 \times \sqrt{10} \approx 1.10\text{m}$, valid only if returns are i.i.d. and the position is held unchanged.

### Example 2: two positions and component VaR

Positions of 6m (daily vol 2%) and 4m (daily vol 1%), correlation 0.3.
Dollar volatilities are 120,000 and 40,000, and

$$
\sigma_P = \sqrt{120{,}000^2 + 40{,}000^2 + 2(0.3)(120{,}000)(40{,}000)} \approx 137{,}400.
$$

99% VaR is $2.326 \times 137{,}400 \approx 319{,}700$, against standalone VaRs of 279,200 and 93,100 that sum to 372,200.
The diversification benefit is about 52,600.
Component VaRs are about 268,200 and 51,500, summing to 319,700: the first position is 84% of the risk.

```python
import numpy as np
from scipy.stats import norm

w = np.array([6e6, 4e6]); vol = np.array([0.02, 0.01]); rho = 0.3
cov = np.outer(vol, vol) * np.array([[1, rho], [rho, 1]])
sd = np.sqrt(w @ cov @ w)
z = norm.ppf(0.99)
var = z * sd                          # 319,651
component = z * w * (cov @ w) / sd    # [268,182, 51,469]
```

### Example 3: historical VaR and ES

500 days of historical scenarios on today's book; the six worst losses, in millions, are 4.1, 3.6, 3.2, 2.9, 2.7, 2.5.
The 99% tail holds $500 \times 1\% = 5$ scenarios.
99% VaR is 2.7m (the 5th worst; some systems interpolate toward the 6th, 2.5m, so state your convention).
99% ES is the mean of the five worst, $(4.1 + 3.6 + 3.2 + 2.9 + 2.7)/5 = 3.3\text{m}$.
One large day leaving the window can move either number by a lot; that instability is the price of making no distributional assumption.

### Example 4: VaR is not subadditive

Two independent bonds each lose 100 on default, with default probability 4%, and 0 otherwise.
Each bond alone: $P(L > 0) = 4\% < 5\%$, so 95% VaR is 0.
Both together: $P(L \ge 100) = 1 - 0.96^2 = 7.84\% > 5\%$, so 95% VaR is 100 > 0 + 0.
Expected shortfall behaves: each bond's 95% ES averages the worst 5% of outcomes (4% at 100, 1% at 0), giving 80.
For the pair, $P(L = 200) = 0.16\%$ and $P(L = 100) = 7.68\%$; the worst 5% is 0.16% at 200 and 4.84% at 100, so ES $= (0.0016 \times 200 + 0.0484 \times 100)/0.05 = 103.2 \le 160$.

### Example 5: backtesting with Kupiec

A 99% one-day VaR model shows 8 exceptions in 250 days; 2.5 were expected.
Under the null, $P(X \ge 8) \approx 0.40\%$ for $X \sim \text{Bin}(250, 0.01)$.
With $\hat p = 0.032$, $\text{LR}_{\text{POF}} \approx 7.73 > 3.84$ (the 5% critical value of $\chi^2_1$), p-value about 0.005: reject.
Under the Basel traffic light, 8 is in the yellow zone (5 to 9).
Next check whether the 8 exceptions cluster in one volatile month; if so, the fix is a faster volatility estimate, not a fatter tail.

### Example 6: normal against fat-tailed VaR at the same volatility

A book with daily volatility 1m.
Normal: 99% VaR 2.33m, 99% ES 2.67m, 99.9% VaR 3.09m.
Student-$t_4$ with the same variance: 99% VaR 2.65m, 99% ES 3.69m, 99.9% VaR 5.07m.
At 99% the VaR differs by 14%, but ES differs by 39%: ES sees the shape of the tail and VaR does not.

## Pitfalls

- Reading VaR as the worst case; it is the best of the bad days, and says nothing about the size of losses beyond it.
- Scaling one-day VaR by $\sqrt{h}$ for positions that are traded, hedged or autocorrelated over the horizon.
- Using delta-normal VaR for option books; a short straddle has small delta VaR and large gamma losses.
- Estimating 99% or 99.9% VaR from a few hundred observations and trusting the second digit.
- Forgetting that correlations rise in a crisis; the diversification benefit in Example 2 shrinks when you need it.
- Treating ES as immune to model error; it is only as good as the tail you assume or sample.
- Backtesting against P&L that includes intraday trading and fees rather than the P&L of the fixed start-of-day book.
- Setting limits purely on VaR, which invites positions with small, frequent gains and rare large losses that sit beyond the quantile.

## Interview questions

> [!question]- risk-var-definition | What does a 99% one-day VaR of 5m mean, and what does it not tell you?
> On about 1 day in 100 the loss is expected to exceed 5m.
> It says nothing about how large those tail losses are, which is what expected shortfall measures.

> [!question]- risk-var-normal-multipliers | For a normal P&L with standard deviation sigma, what are the 99% VaR and 99% ES?
> $2.326\sigma$ and $2.665\sigma$.
> ES is $\varphi(z_\alpha)\sigma/(1-\alpha) = 0.02665\sigma/0.01$.

> [!question]- risk-var-parametric-calc | A 10m position has 1.5% daily volatility. What are its 99% one-day VaR and ES under normality?
> VaR about 349,000 and ES about 400,000.
> $2.326 \times 150{,}000$ and $2.665 \times 150{,}000$.

> [!question]- risk-var-sqrt-time | When is scaling one-day VaR by the square root of the horizon valid?
> When daily P&L is i.i.d. with zero mean and the position is held constant over the horizon.
> Autocorrelation, volatility clustering, trading and nonlinearity all break it.

> [!question]- risk-var-not-subadditive | Give an example where VaR is not subadditive.
> Two independent bonds each losing 100 with probability 4%: each has 95% VaR 0, but together $P(L \ge 100) = 7.84\% > 5\%$, so the pair has 95% VaR 100.
> ES is subadditive here: 103.2 for the pair against 80 + 80.

> [!question]- risk-var-coherence-axioms | What are the four coherence axioms and which one does VaR violate?
> Monotonicity, translation invariance, positive homogeneity and subadditivity; VaR can violate subadditivity.
> It holds for elliptical distributions like the normal but fails for discrete or strongly skewed losses.

> [!question]- risk-var-es-backtest-hard | Why is expected shortfall harder to backtest than VaR?
> ES is not elicitable: no scoring function is minimised in expectation by the true ES, and each test depends on the few tail observations.
> VaR backtests just count exceptions, which are Bernoulli under a correct model.

> [!question]- risk-var-kupiec | A 99% VaR model has 8 exceptions in 250 days. Is it acceptable?
> No: the Kupiec statistic is about 7.7 against a 5% critical value of 3.84 (p about 0.005), and 8 is in the Basel yellow zone.
> Expected exceptions are 2.5 and $P(X \ge 8) \approx 0.4\%$ under a correct model.

> [!question]- risk-var-traffic-light | What are the Basel traffic-light zones for a 99% VaR backtest over 250 days?
> Green 0 to 4 exceptions, yellow 5 to 9, red 10 or more.
> Under a correct model $P(X \le 4) \approx 89\%$ and $P(X \le 9) \approx 99.97\%$.

> [!question]- risk-var-historical-es | Historical VaR over 500 days: the five worst losses are 4.1, 3.6, 3.2, 2.9 and 2.7m. What are the 99% VaR and ES?
> VaR 2.7m (the 5th worst, up to convention) and ES 3.3m, the mean of the five.
> The 1% tail of 500 scenarios has 5 observations.

> [!question]- risk-var-component | How do you allocate portfolio VaR to positions so the pieces add up?
> Euler allocation: $\text{CVaR}_i = w_i\,\partial\text{VaR}/\partial w_i = z_\alpha w_i(\Sigma w)_i/\sigma_P$.
> It adds up because parametric VaR is homogeneous of degree one in the weights.

> [!question]- risk-var-fat-tails | At the same variance, how do normal and Student-t(4) 99% VaR and ES compare?
> $t_4$ VaR is 2.65 against 2.33 standard deviations; ES is 3.69 against 2.67.
> ES reacts far more to tail shape, which is why regulators prefer it.

> [!question]- risk-var-frtb-level | Why did FRTB choose 97.5% ES to replace 99% VaR?
> Under normality they are almost equal ($2.338\sigma$ against $2.326\sigma$), so the level keeps capital comparable in calm markets while ES captures tail severity when tails are fat.
> ES is also coherent, so it does not penalise diversification.

> [!question]- risk-var-clustering | Your VaR exceptions all fall in one volatile month. What does that tell you?
> The model is too slow to update volatility; the exceptions are not independent, which Christoffersen's test detects.
> Use a faster volatility estimate (EWMA or GARCH) or filtered historical simulation.

## Further reading

- Philippe Jorion, *Value at Risk* (3rd ed., 2006).
- Artzner, Delbaen, Eber and Heath (1999), Coherent measures of risk, *Mathematical Finance* 9(3).
- McNeil, Frey and Embrechts, *Quantitative Risk Management* (revised ed., 2015).
- Kupiec (1995), Techniques for verifying the accuracy of risk measurement models, *Journal of Derivatives* 3(2).
- Christoffersen (1998), Evaluating interval forecasts, *International Economic Review* 39(4).
- Basel Committee on Banking Supervision (1996), Supervisory framework for the use of backtesting in conjunction with the internal models approach to market risk capital requirements.
- Basel Committee on Banking Supervision (2019), Minimum capital requirements for market risk.
- Gneiting (2011), Making and evaluating point forecasts, *Journal of the American Statistical Association* 106(494).
