---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [expectation-variance-and-linearity]
est_hours: 3
sources: [Kelly (1956) A New Interpretation of Information Rate. Bell System Technical Journal 35(4) 917-926, Thorp (2006) The Kelly criterion in blackjack sports betting and the stock market. Handbook of Asset and Liability Management Vol 1, MacLean Thorp and Ziemba (eds.) (2011) The Kelly Capital Growth Investment Criterion. World Scientific, Merton (1969) Lifetime portfolio selection under uncertainty. Review of Economics and Statistics 51(3)]
---

# Kelly Criterion and Position Sizing

## TL;DR

- Kelly maximises the expected log of wealth, which is the long-run growth rate; for a binary bet paying $b$ to 1 with win probability $p$, $f^* = p - q/b$.
- For continuous returns with excess drift $\mu$ and volatility $\sigma$, $f^* = \mu/\sigma^2$ and the maximal excess growth rate is $\mu^2/(2\sigma^2) = \text{SR}^2/2$.
- Growth is a parabola in the fraction: a fraction $c$ of Kelly earns $c(2-c)$ of the maximum growth with $c$ times the volatility, so half Kelly keeps 75% of growth at half the risk, and twice Kelly grows at zero.
- Estimation error in $\mu$ is the dominant practical problem: with Sharpe 1 and one year of data, full Kelly on the estimate has zero expected excess growth and half Kelly is optimal.
- For many assets, $f^* = \Sigma^{-1}\mu$: the same vector as the tangency portfolio, scaled to the leverage that maximises growth.

## Learning objectives

- Derive the Kelly fraction for binary bets and for continuous returns (mu / sigma^2).
- Explain fractional Kelly and the growth-volatility trade-off.
- Size positions under parameter uncertainty.

## Core concepts

### Why log wealth

Bet a fraction $f$ of wealth on each of $n$ independent trials.
Wealth multiplies, $W_n = W_0 \prod_i (1 + f X_i)$, so $\frac1n \log(W_n/W_0) \to \mathbb{E}[\log(1 + fX)] =: g(f)$ by the law of large numbers.
Maximising $g$ maximises the almost-sure long-run growth rate and the median of terminal wealth.
Maximising expected wealth instead means betting everything on every positive-edge bet, which ends in ruin with probability 1.
Kelly is not a utility assumption you have to believe; it is the answer to "what fraction compounds fastest", and a trader can choose to bet less than it for risk reasons but should never bet more.

### Binary bets

A bet wins $b$ per unit staked with probability $p$ and loses the stake with probability $q = 1 - p$.

$$
g(f) = p \log(1 + bf) + q \log(1 - f), \qquad g'(f) = \frac{pb}{1 + bf} - \frac{q}{1 - f} = 0 \;\Rightarrow\; f^* = p - \frac{q}{b} = \frac{bp - q}{b}.
$$

Read it as edge over odds: $bp - q$ is the expected profit per unit staked, and $b$ is what you win.
If the edge is zero or negative, $f^* \le 0$: do not bet (or take the other side if you can).

### Continuous returns

Over a short interval the excess return is $\mu\,dt + \sigma\,dB$.
Holding a fraction $f$ of wealth in the risky asset, Ito's lemma gives the log-wealth drift

$$
g(f) = r + f\mu - \tfrac12 f^2\sigma^2, \qquad f^* = \frac{\mu}{\sigma^2}, \qquad g(f^*) - r = \frac{\mu^2}{2\sigma^2} = \frac{\text{SR}^2}{2}.
$$

The $-\frac12 f^2\sigma^2$ term is volatility drag: the arithmetic mean return exceeds the geometric one by half the variance.
The same answer falls out of the binary formula for small bets: $g(f) \approx f\,\mathbb{E}[X] - \frac12 f^2\,\mathbb{E}[X^2]$, so $f^* \approx \text{mean}/\text{second moment}$.
This is Merton's portfolio rule for a log-utility investor.

### Fractional Kelly

Bet $f = c f^*$.
Substituting into the continuous growth rate,

$$
g(cf^*) - r = c(2 - c)\,\frac{\mu^2}{2\sigma^2}, \qquad \text{volatility} = c\,\frac{\mu}{\sigma}.
$$

| Fraction $c$ | Growth as share of max | Volatility as share of Kelly |
| :--- | ---: | ---: |
| 0.25 | 44% | 25% |
| 0.5 | 75% | 50% |
| 1 | 100% | 100% |
| 1.5 | 75% | 150% |
| 2 | 0% | 200% |

The parabola is flat at the top, so under-betting costs little growth and removes a lot of risk, while over-betting costs growth and adds risk.
That asymmetry, plus estimation error, is why practitioners run half Kelly or less.

A clean drawdown result: in the continuous model with fraction $c$ of Kelly, the probability that wealth ever falls to a fraction $x$ of its starting value is $x^{2/c - 1}$.
Full Kelly halves your capital at some point with probability 1/2; half Kelly with probability $0.5^3 = 12.5\%$.
Full Kelly is a very volatile ride even when the model is right.

### Parameter uncertainty

You never know $\mu$; you estimate it with standard error $s$ (for annual drift from $T$ years of data, $s = \sigma/\sqrt{T}$).
Suppose you bet $f = k\hat\mu/\sigma^2$ with $\hat\mu \sim N(\mu, s^2)$.
Because $g$ is quadratic in $f$,

$$
\mathbb{E}[g] - r = \frac{k\mu^2}{\sigma^2} - \frac{k^2(\mu^2 + s^2)}{2\sigma^2}, \qquad k^* = \frac{\mu^2}{\mu^2 + s^2}.
$$

The optimal shrinkage is the squared signal over signal plus noise.
If $s = \mu$ (a t-statistic of 1 on the drift), $k^* = 1/2$: half Kelly is exactly optimal.
Model error in $\sigma$ and fat tails push the same way, since the true second moment is larger than the Gaussian estimate suggests.
In practice you plug in a haircut to $\mu$ and an inflated $\sigma$, then take a fraction of the result.

### Many assets

With excess return vector $\mu$ and covariance $\Sigma$, maximise $f^\top\mu - \frac12 f^\top\Sigma f$:

$$
f^* = \Sigma^{-1}\mu, \qquad g^* - r = \tfrac12\,\mu^\top\Sigma^{-1}\mu = \tfrac12\,\text{SR}_{\text{tan}}^2.
$$

This is the tangency portfolio of [Mean-Variance Portfolio Construction](../09-Alpha-Research-and-Portfolio/10-Mean-Variance-Portfolio-Construction.md) scaled to growth-optimal leverage.
Correlation matters: sizing each asset with its own $\mu_i/\sigma_i^2$ over-bets positively correlated positions.
$\Sigma^{-1}$ amplifies estimation error in $\mu$ along small-eigenvalue directions, so shrink $\Sigma$ (see [Covariance Estimation and Shrinkage](../09-Alpha-Research-and-Portfolio/11-Covariance-Estimation-and-Shrinkage.md)) before inverting it.

### Where Kelly sits in a real risk process

Kelly gives a ceiling, not a target.
Desks size to risk limits (VaR, stress loss, drawdown) that are usually binding well below Kelly; see [Drawdowns and Risk Limits](05-Drawdowns-and-Risk-Limits.md).
The useful interview reflex is: size proportional to edge divided by variance, never above Kelly, and shrink for uncertainty and for correlation with the rest of the book.

## Worked examples

### Example 1: a biased coin at even money

"A coin lands heads 60% of the time and pays even money. How much of your bankroll do you bet on heads?"
Edge per unit is $0.6 - 0.4 = 0.2$ and $b = 1$, so $f^* = 0.6 - 0.4/1 = 0.2$: bet 20%.
Growth per flip is $g(0.2) = 0.6\ln 1.2 + 0.4\ln 0.8 \approx 0.0201$.
The small-bet approximation $\text{mean}^2/(2\,\mathbb{E}[X^2]) = 0.04/2 = 0.02$ is almost exact.
Over 100 flips, median wealth is $e^{100 \times 0.0201} \approx 7.5$ times the start.

| Fraction | Growth per flip | Median wealth after 100 flips |
| :--- | ---: | ---: |
| 10% | 0.0150 | 4.50x |
| 20% | 0.0201 | 7.49x |
| 30% | 0.0147 | 4.37x |
| 40% | -0.0024 | 0.78x |

Betting 40% has twice the expected profit per flip of betting 20%, yet the median player loses money.
In the discrete bet the growth crosses zero at about $f = 0.389$, slightly below $2f^*$.

### Example 2: a long-odds bet

"You can bet at 2 to 1 on an event you think has probability 40%."
Expected profit per unit is $0.4 \times 2 - 0.6 = 0.2$, the same edge as Example 1.
$f^* = 0.4 - 0.6/2 = 0.1$: half the stake, because the bet is riskier (you lose 60% of the time).
Growth per bet is $0.4\ln 1.2 + 0.6\ln 0.9 \approx 0.0097$, about half of Example 1.
Same edge, more variance, smaller bet: that is the whole content of Kelly.

### Example 3: sizing an index position

Excess return 8% a year, volatility 20%.
$f^* = 0.08/0.04 = 2$, so full Kelly is 200% of capital, with excess growth $0.08^2/(2 \times 0.04) = 8\%$ and portfolio volatility 40%.
Half Kelly (100% invested) earns $0.75 \times 8\% = 6\%$ excess growth at 20% volatility.
Leverage of 4 (twice Kelly) earns $4 \times 8\% - \frac12 \times 16 \times 4\% = 0$: all the extra arithmetic return is eaten by volatility drag.
A candidate who says "Sharpe 0.4, so Kelly leverage is $\text{SR}/\sigma = 0.4/0.2 = 2$" has the fastest route to the number.

### Example 4: how much to shrink for estimation error

A strategy shows Sharpe 1 ($\mu = 20\%$, $\sigma = 20\%$) in backtest.
With one year of data the standard error of $\hat\mu$ is $0.2/\sqrt{1} = 20\%$, as large as $\mu$ itself.
Plug-in full Kelly ($k = 1$) has expected excess growth $\frac{0.04}{0.04} - \frac{0.08}{0.08} = 0$: nothing, despite a true Sharpe of 1.
The optimal multiplier is $k^* = 0.04/(0.04 + 0.04) = 0.5$, which earns $0.25$, half of the true-parameter maximum of $0.5$.
With four years, $s = 10\%$ and $k^* = 0.04/0.05 = 0.8$; with ten years, $k^* \approx 0.91$.
And that is before backtest overfitting, which biases $\hat\mu$ upward rather than just adding noise.

### Example 5: two correlated assets

$\mu = (5\%, 3\%)$, $\sigma = (20\%, 15\%)$, correlation 0.5.

$$
\Sigma = \begin{pmatrix} 0.04 & 0.015 \\ 0.015 & 0.0225 \end{pmatrix}, \qquad f^* = \Sigma^{-1}\mu = \begin{pmatrix} 1.00 \\ 0.67 \end{pmatrix}.
$$

Sized one at a time, the assets would get $0.05/0.04 = 1.25$ and $0.03/0.0225 = 1.33$, total leverage 2.58 instead of 1.67.
Portfolio Sharpe is $\sqrt{\mu^\top\Sigma^{-1}\mu} = \sqrt{0.07} \approx 0.265$ and maximal excess growth is $0.035$.

```python
import numpy as np

mu = np.array([0.05, 0.03])
vol = np.array([0.20, 0.15])
corr = np.array([[1.0, 0.5], [0.5, 1.0]])
cov = np.outer(vol, vol) * corr
f = np.linalg.solve(cov, mu)          # [1.0, 0.667]
growth = 0.5 * mu @ f                 # 0.035
```

## Pitfalls

- Maximising expected wealth instead of expected log wealth; it prescribes all-in bets and certain ruin.
- Treating Kelly as a target rather than a ceiling; the parameters are estimates, and over-betting is punished far more than under-betting.
- Forgetting that $f^*$ scales with $1/\sigma^2$, not $1/\sigma$: doubling volatility quarters the Kelly fraction at the same drift.
- Sizing correlated positions independently; use $\Sigma^{-1}\mu$ for the book.
- Using a raw backtest Sharpe; overfitting biases it upward (see [Overfitting and the Deflated Sharpe Ratio](../09-Alpha-Research-and-Portfolio/08-Overfitting-and-Deflated-Sharpe.md)).
- Applying the Gaussian formula to payoffs with a large loss tail (short options, credit); use the discrete $\mathbb{E}[\log(1 + fX)]$ with the true loss scenarios.
- Forgetting that full Kelly halves capital at some point with probability 1/2 even when the model is exact.

## Interview questions

> [!question]- risk-kelly-binary-formula | What is the Kelly fraction for a bet paying b to 1 with win probability p?
> $f^* = p - q/b = (bp - q)/b$, edge divided by odds.
> Set the derivative of $p\log(1+bf) + q\log(1-f)$ to zero.

> [!question]- risk-kelly-coin-60 | A coin lands heads 60% of the time at even money. What fraction do you bet and what is the growth rate?
> Bet 20% of wealth; growth is about 0.020 per flip.
> $f^* = 0.6 - 0.4 = 0.2$ and $g = 0.6\ln 1.2 + 0.4\ln 0.8 \approx 0.0201$, so the median bankroll grows about 7.5 times over 100 flips.

> [!question]- risk-kelly-long-odds | You get 2 to 1 on an event with probability 0.4. How much do you bet?
> 10% of wealth.
> $f^* = 0.4 - 0.6/2 = 0.1$; the edge per unit (0.2) equals the even-money 60% coin, but the higher variance halves the stake.

> [!question]- risk-kelly-continuous | What is the Kelly leverage for an asset with excess drift mu and volatility sigma, and the resulting growth rate?
> $f^* = \mu/\sigma^2$, with excess growth $\mu^2/(2\sigma^2) = \text{SR}^2/2$.
> Log-wealth drift is $f\mu - \frac12 f^2\sigma^2$, a parabola maximised at $\mu/\sigma^2$.

> [!question]- risk-kelly-index-leverage | Excess return 8%, volatility 20%. What is full Kelly leverage and what happens at twice that?
> Full Kelly is 2x leverage with 8% excess growth; at 4x the growth rate is zero.
> $f^* = 0.08/0.04 = 2$; at $f = 4$, $4(0.08) - \frac12(16)(0.04) = 0$.

> [!question]- risk-kelly-half-kelly | What share of growth and of volatility does half Kelly keep?
> 75% of the growth rate at 50% of the volatility.
> A fraction $c$ of Kelly earns $c(2-c)$ of maximal growth with volatility scaled by $c$.

> [!question]- risk-kelly-overbet | Why is over-betting worse than under-betting by the same fraction?
> Growth is symmetric in $c$ around 1, but volatility and drawdowns keep rising with $c$, so 1.5x Kelly has the growth of 0.5x with three times the volatility.
> Parameter uncertainty also means your estimated Kelly is likely too high, which makes the downside of over-betting larger still.

> [!question]- risk-kelly-param-uncertainty | Your drift estimate has standard error s. By what factor should you shrink the plug-in Kelly bet?
> By $k^* = \mu^2/(\mu^2 + s^2)$.
> Expected growth is $k\mu^2/\sigma^2 - k^2(\mu^2+s^2)/(2\sigma^2)$; when the t-statistic on the drift is 1, $k^* = 1/2$ and full Kelly on the estimate has zero expected excess growth.

> [!question]- risk-kelly-multi-asset | What is the Kelly allocation across several correlated assets?
> $f^* = \Sigma^{-1}\mu$, the tangency portfolio at growth-optimal leverage, with excess growth $\frac12\mu^\top\Sigma^{-1}\mu$.
> Sizing each asset alone by $\mu_i/\sigma_i^2$ over-bets positively correlated positions.

> [!question]- risk-kelly-drawdown | Under full Kelly in a continuous model, what is the probability your wealth ever halves?
> 1/2; at half Kelly it is 1/8.
> The probability of ever reaching a fraction $x$ of starting wealth at fraction $c$ of Kelly is $x^{2/c-1}$.

> [!question]- risk-kelly-vs-ev | Why not just maximise expected wealth?
> Because it says to stake everything on every favourable bet, and repeated all-in bets go broke with probability 1.
> Log wealth is what compounds; maximising it maximises the long-run growth rate and median wealth.

> [!question]- risk-kelly-sigma-scaling | Volatility doubles while expected return is unchanged. What happens to the Kelly position?
> It falls to a quarter, because $f^* = \mu/\sigma^2$.
> Volatility-targeting rules that scale by $1/\sigma$ cut only by half, so they are less aggressive than Kelly in response to a vol spike.

## Further reading

- John Kelly (1956), A New Interpretation of Information Rate, *Bell System Technical Journal* 35(4).
- Edward Thorp (2006), The Kelly criterion in blackjack, sports betting and the stock market, in *Handbook of Asset and Liability Management*.
- MacLean, Thorp and Ziemba (eds.), *The Kelly Capital Growth Investment Criterion* (2011).
- Robert Merton (1969), Lifetime portfolio selection under uncertainty: the continuous-time case, *Review of Economics and Statistics* 51(3).
