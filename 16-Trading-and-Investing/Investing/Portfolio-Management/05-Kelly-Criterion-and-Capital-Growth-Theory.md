---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Kelly (1956) - A New Interpretation of Information Rate, Breiman (1961) - Optimal Gambling Systems for Favorable Games, Thorp (1969) - Optimal Gambling Systems for Favorable Games, Thorp (2006) - The Kelly Criterion in Blackjack Sports Betting and the Stock Market, MacLean Ziemba and Blazenko (1992) - Growth Versus Security in Dynamic Investment Analysis, Chopra and Ziemba (1993) - The Effect of Errors in Means Variances and Covariances on Optimal Portfolio Choice]
---

# Kelly Criterion and Capital Growth Theory

## TL;DR

- John L. Kelly Jr., a physicist at Bell Telephone Laboratories, showed in 1956 how to size repeated favorable bets to maximize the long-run growth rate of capital, by maximizing the expected logarithm of wealth.
- The single-period Bernoulli Kelly fraction is $f^* = \frac{b p - q}{b}$, where $p$ is win probability, $q = 1 - p$ is loss probability, and $b$ is the net payoff odds.
- In continuous diffusion markets, the Kelly fraction is the Merton fraction for logarithmic utility: $f^* = \frac{\mu - r}{\sigma^2}$, with maximum growth $r + \tfrac12 \text{SR}^2$.
- Full Kelly is volatile: the probability of ever falling to half of current wealth is 50%, and of halving before doubling is one-third; Thorp (2006) reports that most bettors and investors prefer half Kelly or nearby, which keeps 75% of the growth rate.
- In the continuous model, betting more than twice Kelly ($f > 2f^*$) makes the growth rate fall below the risk-free rate, so an overestimated edge turns a profitable strategy into a losing one.

## Learning objectives

- Derive the Kelly Criterion from first principles by maximizing expected logarithmic wealth $\mathbb{E}[\ln(W_T)]$.
- Prove that the continuous Kelly fraction equals the Sharpe ratio divided by volatility: $f^* = \frac{\text{SR}}{\sigma}$.
- Analyze the capital growth curve $g(f)$ and prove that excess growth over the risk-free rate becomes negative when allocation exceeds double Kelly ($f > 2f^*$).
- Generalize the Kelly criterion to multiple correlated assets using the covariance inversion matrix $\mathbf{f}^* = \mathbf{\Sigma}^{-1}(\boldsymbol{\mu} - r\mathbf{1})$.
- Formulate Fractional Kelly strategies to balance terminal growth rate against drawdown tolerance and parameter estimation error.

## Core concepts

### 1. Information Theoretic Foundations and Derivation

Kelly (1956, Bell System Technical Journal) connected Shannon's information theory to betting.
A gambler who receives tips over a noisy communication channel and reinvests his winnings can make his capital grow at an exponential rate equal to the channel's information rate; for a binary symmetric channel that rate is the channel capacity.

Consider an investor with wealth $W_0$ facing a repeated game with win probability $p$ and loss probability $q = 1 - p$.
On each trial, the investor allocates fraction $f$ of current wealth.
If the trade wins, the payoff is $b$ times the wager; if the trade loses, the stake is lost:

$$W_{t+1} = \begin{cases} W_t (1 + b f) & \text{with probability } p \\ W_t (1 - f) & \text{with probability } q \end{cases}$$

After $N$ independent trials with $W$ wins and $L = N - W$ losses:

$$W_N = W_0 (1 + b f)^W (1 - f)^L$$

The compound growth rate per trial $g(f)$ is:

$$g(f) = \lim_{N \to \infty} \frac{1}{N} \ln \left(\frac{W_N}{W_0}\right) = p \ln(1 + b f) + q \ln(1 - f)$$

To find the optimal fraction $f^*$ that maximizes asymptotic compound growth, differentiate $g(f)$ with respect to $f$ and set the derivative to zero:

$$\frac{dg}{df} = \frac{p b}{1 + b f} - \frac{q}{1 - f} = 0$$

$$p b (1 - f) - q (1 + b f) = 0$$

$$p b - p b f - q - q b f = 0$$

$$p b - q - b f (p + q) = 0$$

Since $p + q = 1$:

$$f^* = \frac{p b - q}{b} = \frac{p(b + 1) - 1}{b}$$

When payoffs are symmetric ($b = 1$ to 1 odds):

$$f^* = p - q = 2p - 1$$

If an edge is $p = 0.55$ with even money payoffs, the Kelly allocation is exactly $2(0.55) - 1 = 0.10$ (10% of portfolio equity), and the growth rate is $g(0.10) = 50.08 \times 10^{-4}$ per bet.
In this discrete game the growth curve is not exactly symmetric: $g(0.20) = -1.38 \times 10^{-4}$ per bet, and growth turns negative at $f = 0.1987$, just below $2f^*$.

```
+-----------------------------------------------------------------------+
|                    THE KELLY CAPITAL GROWTH CURVE g(f)                |
+-----------------------------------------------------------------------+
| Growth Rate g(f)                                                      |
|       ^                                                               |
| g_max |                    *  [Peak: Full Kelly f*]                   |
|       |                 *     *                                       |
|       |              *           *                                    |
| 0.75g |           * [Half Kelly]    *                                 |
|       |        *                       *                              |
|       |     *                             *                           |
|   0   +---*----------------------------------*------------------> f   |
|       |  f=0                                f=2f* [Double Kelly]      |
|       |                                        *                      |
| -inf  |                                           * [Certain Ruin]    |
+-----------------------------------------------------------------------+
```

### 2. Continuous-Time Gaussian Kelly Formulation

In continuous financial markets, asset returns follow Geometric Brownian Motion:

$$\frac{dS_t}{S_t} = \mu dt + \sigma dZ_t$$

Let an investor allocate fraction $f$ of portfolio wealth $W_t$ to the risky asset and $(1 - f)$ to the risk-free rate $r$:

$$\frac{dW_t}{W_t} = [r + f(\mu - r)] dt + f \sigma dZ_t$$

Applying Ito's Lemma to the logarithmic utility function $U(W_t) = \ln W_t$:

$$d\ln W_t = \left[ r + f(\mu - r) - \frac{1}{2} f^2 \sigma^2 \right] dt + f \sigma dZ_t$$

The expected continuous growth rate $g(f)$ is:

$$g(f) = \mathbb{E}\left[\frac{d\ln W_t}{dt}\right] = r + f(\mu - r) - \frac{1}{2} f^2 \sigma^2$$

Differentiating with respect to $f$:

$$\frac{dg}{df} = (\mu - r) - f \sigma^2 = 0 \implies f^* = \frac{\mu - r}{\sigma^2}$$

The maximum compound growth rate achieved at $f^*$ is:

$$g(f^*) = r + \frac{(\mu - r)^2}{2\sigma^2} = r + \frac{1}{2} \text{SR}^2$$

where $\text{SR} = \frac{\mu - r}{\sigma}$ is the Sharpe ratio of the asset.
Continuous Kelly demonstrates that the asymptotic growth rate depends quadratically on the Sharpe ratio.
For a hypothetical asset with $\mu - r = 10\%$ and $\sigma = 20\%$, $f^* = 2.5$ and the maximum excess growth is 12.5% a year.

### 3. The Hazard of Overbetting: Double Kelly and Variance Decay

Evaluating the growth rate function at multiples of $f^*$:

- **Zero Allocation ($f = 0$)**: $g(0) = r$
- **Half Kelly ($f = 0.5 f^*$)**: $g(0.5 f^*) = r + \frac{3}{8} \frac{(\mu - r)^2}{\sigma^2} = r + 0.75 (g(f^*) - r)$
- **Full Kelly ($f = f^*$)**: $g(f^*) = r + \frac{1}{2} \frac{(\mu - r)^2}{\sigma^2}$
- **Double Kelly ($f = 2 f^*$)**: $g(2 f^*) = r + 2\frac{(\mu - r)^2}{\sigma^2} - \frac{1}{2}(4)\frac{(\mu - r)^2}{\sigma^2} = r$
- **Over-Kelly ($f > 2 f^*$)**: $g(f) < r$; compound growth is less than the risk-free rate and becomes negative for large $f$.

In general, at $f = c f^*$ the excess growth is $(2c - c^2)$ times its maximum.

```
+-----------------------------------------------------------------------+
|             GROWTH VS RISK TRADEOFF ACROSS KELLY FRACTIONS            |
+-----------------------------------------------------------------------+
| Fraction | % Max Growth | Volatility | P(ever halve) | P(halve<double)|
|----------+--------------+------------+---------------+----------------|
| 0.25 f*  | 43.75%       | 0.25 sigma | 0.78%         | 0.78%          |
| 0.50 f*  | 75.00%       | 0.50 sigma | 12.50%        | 11.11%         |
| 0.75 f*  | 93.75%       | 0.75 sigma | 31.50%        | 23.95%         |
| 1.00 f*  | 100.00%      | 1.00 sigma | 50.00%        | 33.33%         |
| 1.50 f*  | 75.00%       | 1.50 sigma | 79.37%        | 44.25%         |
| 2.00 f*  | 0.00%        | 2.00 sigma | 100.00%       | 50.00%         |
+-----------------------------------------------------------------------+
```

For a Kelly fraction $c = f / f^*$, log wealth in excess of the risk-free growth path is a Brownian motion with $2 \times \text{drift} / \text{variance} = a = 2/c - 1$, so the probability of ever falling to half of the current wealth is $0.5^{a}$ (Thorp 2006, section 7.3).
The probability of halving before doubling is $(1 - 2^{-a}) / (2^{a} - 2^{-a})$, which is one-third at Full Kelly and tends to one-half as $c \to 2$.

Notice that Half Kelly achieves 75% of the theoretical maximum growth rate with only 50% of the volatility and a dramatic reduction in drawdown severity (12.5% versus 50% chance of ever halving, and an 8/9 chance of doubling before halving).
Conversely, betting at $1.5 f^*$ delivers the exact same growth rate as Half Kelly while raising the chance of ever halving from 12.5% to 79.37%, 6.35 times higher.

### 4. Multi-Asset Matrix Kelly Optimization

When trading $N$ correlated assets, the scalar formula extends to matrix form.
Let $\boldsymbol{\mu} \in \mathbb{R}^N$ be the vector of asset expected returns, $r$ be the risk-free rate, $\mathbf{1}$ be the vector of ones, and $\mathbf{\Sigma} \in \mathbb{R}^{N \times N}$ be the covariance matrix.

The expected continuous portfolio growth rate is:

$$g(\mathbf{f}) = r + \mathbf{f}^T (\boldsymbol{\mu} - r\mathbf{1}) - \frac{1}{2} \mathbf{f}^T \mathbf{\Sigma} \mathbf{f}$$

Taking the gradient with respect to $\mathbf{f}$ and setting to zero:

$$\nabla_{\mathbf{f}} g = (\boldsymbol{\mu} - r\mathbf{1}) - \mathbf{\Sigma} \mathbf{f} = \mathbf{0}$$

$$\mathbf{f}^* = \mathbf{\Sigma}^{-1} (\boldsymbol{\mu} - r\mathbf{1})$$

The unconstrained multi-asset Kelly vector is the tangency (maximum Sharpe) portfolio scaled to the leverage chosen by an investor with logarithmic utility, i.e. constant relative risk aversion $\gamma = 1$.

### 5. Parameter Estimation Risk and Epistemic Shrinkage

In real-world quantitative trading, parameters $\mu$ and $\mathbf{\Sigma}$ are not known; they must be estimated from finite, non-stationary historical data.

If true drift is $\mu_{\text{true}}$ but estimated as $\hat{\mu} > \mu_{\text{true}}$, the trader unknowingly overbets (writing $\mu$ for the excess return over $r$):

$$\hat{f} = \frac{\hat{\mu}}{\sigma^2} > \frac{\mu_{\text{true}}}{\sigma^2} = f^*$$

If $\hat{\mu} > 2 \mu_{\text{true}}$, the trader allocates beyond Double Kelly ($f > 2 f^*$), converting a genuinely profitable trading edge into growth below the risk-free rate.
Chopra and Ziemba (1993) find that errors in estimated means do far more damage to mean-variance portfolios than errors in variances or covariances, so practitioners shrink $\hat{\boldsymbol{\mu}}$ toward a prior and size below full Kelly; Thorp (2006) makes the same argument for fractional Kelly when the edge is uncertain.

---

## Flashcard drill bank

> [!question]- mkt-pf-129 | Who authored the original 1956 paper establishing the Kelly Criterion?
> John L. Kelly Jr., a physicist and information theorist at Bell Telephone Laboratories.

> [!question]- mkt-pf-130 | What objective function does the Kelly Criterion maximize?
> The expected value of the logarithm of wealth, E[ln(W_T)], which maximizes asymptotic compound growth.

> [!question]- mkt-pf-131 | What is the single-period Bernoulli Kelly formula with odds b, win probability p, and loss probability q?
> f* = (b * p - q) / b.

> [!question]- mkt-pf-132 | In an even-money bet (b = 1), what is the Kelly fraction?
> f* = p - q = 2p - 1.

> [!question]- mkt-pf-133 | What is the continuous Gaussian Kelly fraction for an asset with drift mu, risk-free rate r, and volatility sigma?
> f* = (mu - r) / sigma^2.

> [!question]- mkt-pf-134 | How is the continuous Kelly growth rate expressed in terms of the Sharpe ratio (SR)?
> g(f*) = r + 0.5 * SR^2.

> [!question]- mkt-pf-135 | What happens to the compound growth rate if an investor sizes positions at Double Kelly (2 * f*)?
> In the continuous model the growth rate falls back to the risk-free rate: excess growth is zero, so the extra risk earns nothing.

> [!question]- mkt-pf-136 | What occurs when position sizing exceeds Double Kelly (f > 2 * f*)?
> The growth rate falls below the risk-free rate, and becomes negative for large enough f, so log wealth drifts down relative to cash despite a genuine edge.

> [!question]- mkt-pf-137 | Why do professional hedge funds use Fractional Kelly rather than Full Kelly?
> To protect against parameter estimation error, model misspecification, and extreme drawdowns.

> [!question]- mkt-pf-138 | What proportion of maximum growth does Half Kelly (0.5 * f*) achieve?
> Exactly 75% of the maximum theoretical growth rate.

> [!question]- mkt-pf-139 | How does the volatility of Half Kelly compare to Full Kelly?
> Half Kelly has exactly 50% of the volatility of Full Kelly.

> [!question]- mkt-pf-140 | What is the multi-asset Kelly allocation vector formula?
> f* = Sigma^(-1) * (mu - r * 1), where Sigma is the covariance matrix.

> [!question]- mkt-pf-141 | What is the probability of a 50% drawdown under a Full Kelly sizing strategy?
> The probability of ever halving is 0.5^(2/c - 1) = 50% at c = 1, while the probability of halving before doubling is exactly one-third (33.3%).

> [!question]- mkt-pf-142 | What is the utility function implicitly maximized by the Kelly Criterion?
> Logarithmic utility: U(W) = ln(W).

> [!question]- mkt-pf-143 | What is the Arrow-Pratt constant relative risk aversion (CRRA) coefficient for logarithmic utility?
> Gamma = 1.

> [!question]- mkt-pf-144 | How does Ed Thorp's application of Kelly at Princeton Newport Partners illustrate practical sizing?
> Thorp's public writing does not give a Princeton Newport sizing rule; what he does report (Thorp 2006, section 7.3) is that most bettors and investors prefer half Kelly or nearby, giving up a quarter of the growth rate for a much lower chance of a large loss, and that fractional Kelly is prudent when the edge is uncertain.

> [!question]- mkt-pf-145 | Why does the arithmetic mean return mislead investors compared to the geometric mean return?
> Arithmetic mean ignores the compounding penalty of volatility; geometric mean measures the actual path-dependent wealth accumulation.

> [!question]- mkt-pf-146 | In the Kelly framework, what is the asymptotic relationship between time to reach a target wealth and bet size?
> Full Kelly minimizes the expected time required to reach any predetermined high wealth threshold, asymptotically as the threshold grows (Breiman 1961).

> [!question]- mkt-pf-147 | What is the Breiman (1961) theorem regarding the Kelly criterion?
> Kelly betting asymptotically outperforms any essentially different strategy with probability 1 as the number of trials approaches infinity.

> [!question]- mkt-pf-148 | If a quantitative trader estimates Sharpe ratio as 1.0 but true Sharpe is 0.4, what happens under Full Kelly?
> With volatility known, sizing at the estimated Kelly fraction puts the trader at 2.5 times the true optimal fraction (over Double Kelly), so excess growth is (2c - c^2) = -1.25 times the true maximum: below the risk-free rate.

> [!question]- mkt-pf-149 | What is 'optimal f' as defined by Ralph Vince?
> The fixed fraction of account equity to risk on a trade that maximizes the terminal wealth relative (TWR) for empirical trade distributions.

> [!question]- mkt-pf-150 | Why is the empirical distribution of financial returns more hazardous for Kelly than Gaussian distributions?
> Financial returns exhibit fat tails (leptokurtosis) and negative skewness; occasional extreme drops cause immediate ruin under naive Gaussian Kelly.

> [!question]- mkt-pf-151 | How can downside jump risk be incorporated into Kelly sizing?
> By adding a jump-diffusion Poisson process to the stochastic differential equation, reducing the optimal leverage fraction.

> [!question]- mkt-pf-152 | What is the effect of portfolio borrowing costs on the optimal Kelly leverage fraction?
> Borrowing costs increase the hurdle rate and introduce non-linear financing spreads, lowering the optimal leverage fraction.

> [!question]- mkt-pf-153 | What is the relationship between the Kelly Criterion and the Markowitz efficient frontier?
> The Kelly portfolio is the point on the capital allocation line through the tangency portfolio chosen by an investor with log utility (relative risk aversion gamma = 1).

> [!question]- mkt-pf-154 | What happens to Kelly leverage when asset volatility doubles while drift remains constant?
> The optimal Kelly fraction is cut by a factor of 4 (inversely proportional to variance, sigma^2).

> [!question]- mkt-pf-155 | What is epistemic uncertainty in the context of capital growth theory?
> The fundamental uncertainty about the parameters (probabilities, payoffs, drift, covariance) of the underlying stochastic process.

> [!question]- mkt-pf-156 | Why does Kelly sizing never recommend borrowing infinite leverage even if win probability is 99%?
> Because if loss probability q > 0 and a total loss is possible, ln(1 - f) approaches negative infinity as f approaches 1.0.

> [!question]- mkt-pf-157 | What is the 'Gambler's Fallacy' and how does Kelly theory avoid it?
> The mistaken belief that past independent losses increase future win probability; Kelly treats trials as conditionally independent based on true edge.

> [!question]- mkt-pf-158 | What is the primary operational rule for updating Kelly fractions in a live trading fund?
> Dynamically rescale capital fractions as realized volatility and trailing account equity fluctuate.

> [!question]- mkt-pf-159 | How does transaction cost friction alter the multi-asset Kelly allocation?
> Rebalancing to continuous Kelly creates turnover drag; managers use no-trade buffer bands around optimal weights to preserve capital.

> [!question]- mkt-pf-160 | What is the ultimate takeaway of Capital Growth Theory?
> Growth rate is a quadratic function of leverage: underbetting sacrifices growth, but overbetting leads to irreversible ruin.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_pm_05_kelly.py`](../../code/mkt_pm_05_kelly.py) prints and asserts every computed number on this page: the Bernoulli Kelly fraction by golden-section maximization and the zero of the discrete growth curve by bisection, the share of maximum growth by Gauss-Hermite quadrature of a rebalanced position checked against a seeded simulation, the halving probabilities by a finite-difference solve of the boundary-value problem against the closed forms, and the matrix Kelly vector by gradient ascent.
- Related notes: [Drawdown Mathematics and Risk of Ruin](04-Drawdown-Mathematics-and-Risk-of-Ruin.md) (ruin with fixed bets), [Risk Parity and The All-Weather Framework](06-Risk-Parity-and-The-All-Weather-Framework.md) (leverage choice for a risk-balanced portfolio).

## Further reading

- Breiman, L. (1961). *Optimal Gambling Systems for Favorable Games*. Proceedings of the Fourth Berkeley Symposium on Mathematical Statistics and Probability, Vol. 1. University of California Press.
- Chopra, V. K., & Ziemba, W. T. (1993). *The Effect of Errors in Means, Variances, and Covariances on Optimal Portfolio Choice*. The Journal of Portfolio Management, 19(2), 6-11.
- Kelly, J. L. (1956). *A New Interpretation of Information Rate*. Bell System Technical Journal, 35(4), 917-926.
- MacLean, L. C., Ziemba, W. T., & Blazenko, G. (1992). *Growth Versus Security in Dynamic Investment Analysis*. Management Science, 38(11), 1562-1585.
- Thorp, E. O. (1969). *Optimal Gambling Systems for Favorable Games*. Review of the International Statistical Institute, 37(3), 273-293.
- Thorp, E. O. (2006). *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market*. In S. A. Zenios and W. T. Ziemba (eds.), Handbook of Asset and Liability Management, Vol. 1, chapter 9. Elsevier.
- Vince, R. (1992). *The Mathematics of Money Management: Risk Analysis Techniques for Traders*. John Wiley & Sons.
