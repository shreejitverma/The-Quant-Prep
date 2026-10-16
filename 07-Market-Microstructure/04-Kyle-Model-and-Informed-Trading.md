---
type: concept
track: [quant-research]
tier: advanced
status: solid
prereqs: [spread-models-roll-and-glosten-milgrom]
est_hours: 3
sources: [Kyle (1985) Continuous Auctions and Insider Trading. Econometrica 53(6) 1315-1335, O'Hara (1995) Market Microstructure Theory. Blackwell - chapter 4, Back (1992) Insider Trading in Continuous Time. Review of Financial Studies 5(3) 387-409, Holden and Subrahmanyam (1992) Long-Lived Private Information and Imperfect Competition. Journal of Finance 47(1) 247-270, Hasbrouck (2007) Empirical Market Microstructure. Oxford University Press]
---

# Kyle Model and Informed Trading

## TL;DR

- One insider knows $v \sim N(p_0, \Sigma_0)$, noise traders submit $u \sim N(0, \sigma_u^2)$, and a competitive market maker sees only total flow $y = x + u$ and sets $p = \mathbb{E}[v \mid y]$.
- The linear equilibrium is $x = \beta(v - p_0)$ and $p = p_0 + \lambda y$ with $\beta = \sigma_u/\sqrt{\Sigma_0}$ and $\lambda = \sqrt{\Sigma_0}/(2\sigma_u)$; Kyle's lambda is the price impact per share and $1/\lambda$ is market depth.
- The insider trades exactly as much as the noise traders ($\text{Var}(x) = \sigma_u^2$), so half of the private information enters the price: $\text{Var}(v \mid p) = \Sigma_0/2$.
- Insider expected profit is $\tfrac12\sigma_u\sqrt{\Sigma_0}$, paid entirely by noise traders; more noise means a bigger, better-hidden insider position, deeper markets and more insider profit, with the same price informativeness.
- With many auctions the insider trades gradually; in the continuous limit $\lambda = \sqrt{\Sigma_0}/\sigma_u$ is constant, all information is in the price by the end, and the insider earns $\sigma_u\sqrt{\Sigma_0}$.

## Learning objectives

- Solve the one-period Kyle model and interpret Kyle's lambda.
- Explain how informed traders hide in noise flow.
- Compute price informativeness and the division of profits between insider and noise traders.
- State the multi-period and continuous-time results accurately and reproduce them numerically.

## Core concepts

### Setup

- The asset pays $v \sim N(p_0, \Sigma_0)$, revealed after trading.
- A single risk-neutral insider observes $v$ and submits a market order $x$.
- Noise (liquidity) traders submit $u \sim N(0, \sigma_u^2)$, independent of $v$.
- Competitive risk-neutral market makers observe only $y = x + u$ and set $p = \mathbb{E}[v \mid y]$, so they break even on average.

The insider is strategic: he knows his order moves the price, so he trades less than he would at a fixed price.
This is the key difference from Glosten-Milgrom, where traders take quotes as given and trade one unit.

### Solving for the equilibrium

Conjecture linear strategies $x = \beta(v - p_0)$ and $p = p_0 + \lambda y$.

Insider: given $v$ and $\lambda$, expected profit is

$$
\mathbb{E}[(v - p)\,x \mid v] = x\,(v - p_0 - \lambda x),
$$

because $\mathbb{E}[u] = 0$.
It is concave in $x$; the first-order condition gives $x = (v - p_0)/(2\lambda)$, so

$$
\beta = \frac{1}{2\lambda}.
$$

Market maker: with $v$ and $y$ jointly normal, $\mathbb{E}[v \mid y] = p_0 + \frac{\text{Cov}(v, y)}{\text{Var}(y)} y$, so

$$
\lambda = \frac{\beta\Sigma_0}{\beta^2\Sigma_0 + \sigma_u^2}.
$$

Substitute $\beta = 1/(2\lambda)$: $\lambda\big(\Sigma_0/(4\lambda^2) + \sigma_u^2\big) = \Sigma_0/(2\lambda)$, so $\lambda^2\sigma_u^2 = \Sigma_0/4$ and

$$
\boxed{\lambda = \frac{\sqrt{\Sigma_0}}{2\sigma_u}, \qquad \beta = \frac{\sigma_u}{\sqrt{\Sigma_0}}.}
$$

### What the equilibrium says

- Order flow: $\text{Var}(x) = \beta^2\Sigma_0 = \sigma_u^2$, so the insider's trade is as variable as the noise, and $\text{Var}(y) = 2\sigma_u^2$.
  He hides in the noise by scaling his trade to it.
- Price informativeness: $\text{Var}(v \mid y) = \Sigma_0 - \lambda^2\,\text{Var}(y) = \Sigma_0/2$.
  Half the private information is revealed, regardless of $\sigma_u$.
- Profits: $v - p = \tfrac12(v - p_0) - \lambda u$, so the insider's expected profit is $\mathbb{E}[x(v - p)] = \tfrac12\beta\Sigma_0 = \tfrac12\sigma_u\sqrt{\Sigma_0}$.
  Noise traders lose $\mathbb{E}[u(p - v)] = \lambda\sigma_u^2 = \tfrac12\sigma_u\sqrt{\Sigma_0}$, the same amount; market makers break even.
- Comparative statics: doubling $\sigma_u$ halves $\lambda$ (the market is twice as deep), doubles $\beta$ and the insider's profit, and leaves informativeness unchanged.
  More uninformed trading attracts more informed trading, not less information in prices.
- Depth: $1/\lambda = 2\sigma_u/\sqrt{\Sigma_0}$ shares per unit price move; markets are deep when noise trading is large relative to the value uncertainty.

### Kyle's lambda in practice

Kyle's lambda is the theoretical ancestor of linear price impact.
Empirically it is estimated by regressing price changes on signed order flow over short intervals, $\Delta p_t = \lambda\, \text{OFI}_t + \varepsilon_t$; see [Order Book Imbalance and the Microprice](11-Order-Book-Imbalance-and-Microprice.md) for the order-flow imbalance version.
Desks use it as a liquidity measure (cost per share of net flow), research uses it as a proxy for information asymmetry, and it reappears as the permanent impact coefficient in [Optimal Execution: Almgren-Chriss](07-Optimal-Execution-Almgren-Chriss.md).
Real metaorder impact is concave (square-root), not linear, which is one reason the linear model is a benchmark rather than a cost model; see [Market Impact Models](06-Market-Impact-Models.md).

### Many auctions and continuous trading

Kyle (1985) also solves a sequential-auction model: $N$ auctions at times $t_n = n/N$ on $[0, 1]$, noise variance $\sigma_u^2\,\Delta t_n$ per auction, and an insider who trades $\Delta x_n = \beta_n (v - p_{n-1})\Delta t_n$ against $\Delta p_n = \lambda_n(\Delta x_n + \Delta u_n)$.
The equilibrium solves backward from $\alpha_N = \delta_N = 0$ (with $\Sigma_n$ the posterior variance after auction $n$):

$$
\beta_n\Delta t_n = \frac{1 - 2\alpha_n\lambda_n}{2\lambda_n(1 - \alpha_n\lambda_n)}, \quad \lambda_n = \frac{\beta_n\Sigma_n}{\sigma_u^2}, \quad \Sigma_n = (1 - \beta_n\lambda_n\Delta t_n)\Sigma_{n-1}, \quad \alpha_{n-1} = \frac{1}{4\lambda_n(1 - \alpha_n\lambda_n)}, \quad \delta_{n-1} = \delta_n + \alpha_n\lambda_n^2\sigma_u^2\Delta t_n,
$$

where the insider's value function is $\alpha_{n}(v - p_{n})^2 + \delta_{n}$ and the second-order condition is $\lambda_n(1 - \alpha_n\lambda_n) > 0$.
Each step is a cubic in $\lambda_n$, which the repo code solves by bisection.

As $N \to \infty$ the equilibrium converges to Kyle's continuous auction:

- $\lambda$ is constant over time and equal to $\sqrt{\Sigma_0}/\sigma_u$, twice the one-shot value, so depth is constant;
- the posterior variance falls linearly, $\Sigma(t) = (1 - t)\Sigma_0$, so all private information is in the price at the end;
- the insider trades gradually and his expected profit is $\sigma_u\sqrt{\Sigma_0}$, twice the one-shot profit;
- the price follows a Brownian motion with constant volatility $\sqrt{\Sigma_0}$, so informed trading leaves no predictable pattern in prices.

Extensions worth naming: Back (1992) generalises the continuous-time model to non-normal values; Holden and Subrahmanyam (1992) show that with several competing insiders information is revealed much faster, because each races to trade before the others.

## Worked examples

### Example 1: one-period equilibrium

"$p_0 = 100$, $\sigma_v = 2$ ($\Sigma_0 = 4$), $\sigma_u = 10{,}000$ shares."
$\lambda = 2/(2 \times 10{,}000) = 0.0001$ dollars per share, so 10,000 shares of net flow move the price $1.
$\beta = 10{,}000/2 = 5{,}000$ shares per dollar of mispricing.
Insider expected profit $= \tfrac12 \times 10{,}000 \times 2 = 10{,}000$ dollars, and noise traders lose $\lambda\sigma_u^2 = 10{,}000$.
Posterior variance $\Sigma_0/2 = 2$.

One draw: $v = 103$, $u = -4{,}000$.
The insider buys $x = 5{,}000 \times 3 = 15{,}000$, total flow is $11{,}000$, the price is $100 + 0.0001 \times 11{,}000 = 101.10$, and the insider makes $(103 - 101.10) \times 15{,}000 = 28{,}500$.
The noise traders' selling hid most of his buying: the price moved only 1.1 of the 3 dollars.

### Example 2: why $\beta$ is optimal

Holding $\lambda = 0.0001$, expected profit as a function of trading intensity $b$ is $b\,\Sigma_0 - \lambda b^2 \Sigma_0$.
At $b = \beta = 5{,}000$ it is 10,000; at $b = 2{,}500$ it is 7,500; at $b = 10{,}000$ it is 0, because the extra impact eats all the information rent.

### Example 3: Monte Carlo check

One million draws (seed 4): the regression slope of $v$ on $y$ is about $9.994 \times 10^{-5}$ (theory $10^{-4}$), the insider's mean profit is about 9,982 (theory 10,000), $\text{Var}(v - p)$ is about 1.998 (theory 2) and the squared correlation of price and value is about 0.4997 (theory 0.5).

### Example 4: from one auction to continuous trading

With $\sigma_v = \sigma_u = 1$, the backward recursion gives (profit is $\mathbb{E}[\sum_n \Delta x_n (v - p_n)]$):

| Auctions $N$ | $\lambda_1$ | $\Sigma_N/\Sigma_0$ | Insider profit |
| ---: | ---: | ---: | ---: |
| 1 | 0.5000 | 0.5000 | 0.5000 |
| 2 | 0.6529 | 0.3460 | 0.6206 |
| 4 | 0.7648 | 0.2206 | 0.7307 |
| 10 | 0.8653 | 0.1099 | 0.8439 |
| 100 | 0.9745 | 0.0138 | 0.9714 |
| 1000 | 0.9962 | 0.0014 | 0.9959 |

The first-auction impact rises toward the continuous value $\sigma_v/\sigma_u = 1$, residual uncertainty goes to zero and profit rises toward $\sigma_u\sigma_v = 1$.
Simulating the insider against these $\lambda_n$ gives about 0.6205 for $N = 2$ (2,000,000 paths, seed 5) and about 0.8438 for $N = 10$ (1,000,000 paths, seed 6), confirming the recursion.

## Pitfalls

- Writing $\lambda = \sigma_v/\sigma_u$ for the one-period model; that is the continuous-time value, the one-shot value has a factor $\tfrac12$.
- Saying more noise trading makes prices less informative; in Kyle it leaves informativeness unchanged because the insider scales up.
- Treating Kyle's lambda as a model of large-order cost: it is linear and permanent, while empirical metaorder impact is concave and partly transient.
- Forgetting that the market maker sets price after seeing total flow; there is no bid-ask spread in the model, only a price schedule.
- Confusing the insider's expected profit with realised profit; on any draw he can lose if noise flow moves the price past $v$.
- Assuming the multi-period insider front-loads; in equilibrium he trades gradually so as not to give his information away early, and prices remain a martingale because market makers are competitive.

## Interview questions

> [!question]- ms-kyle-lambda-formula | State Kyle's one-period lambda and beta.
> $\lambda = \sqrt{\Sigma_0}/(2\sigma_u)$, $\beta = \sigma_u/\sqrt{\Sigma_0}$.
> From $\beta = 1/(2\lambda)$ (insider FOC) and $\lambda = \beta\Sigma_0/(\beta^2\Sigma_0 + \sigma_u^2)$ (market maker regression).

> [!question]- ms-kyle-insider-foc | Derive the insider's optimal order given $\lambda$.
> Maximise $x(v - p_0 - \lambda x)$: $x = (v - p_0)/(2\lambda)$.
> He trades half as much as a linear impact would make break-even, the monopolist's quantity.

> [!question]- ms-kyle-mm-pricing | How does the market maker set $\lambda$?
> As the regression coefficient of $v$ on total flow: $\lambda = \text{Cov}(v, y)/\text{Var}(y)$.
> Competition and risk neutrality force $p = \mathbb{E}[v \mid y]$.

> [!question]- ms-kyle-numeric | $\sigma_v = 2$, $\sigma_u = 10{,}000$ shares. What are $\lambda$, depth and insider profit?
> $\lambda = 0.0001$ per share, depth 10,000 shares per dollar, profit 10,000 dollars.
> $\lambda = \sigma_v/(2\sigma_u)$, profit $\tfrac12\sigma_u\sigma_v$.

> [!question]- ms-kyle-realization | Same model, $p_0 = 100$, $v = 103$, $u = -4{,}000$. Where does the price clear?
> 101.10.
> $x = 5{,}000 \times 3 = 15{,}000$, $y = 11{,}000$, $p = 100 + 0.0001 \times 11{,}000$.

> [!question]- ms-kyle-informativeness | How much private information is in the one-period price?
> Half: $\text{Var}(v \mid p) = \Sigma_0/2$, independent of $\sigma_u$.
> The insider's order has the same variance as the noise, so flow is half signal.

> [!question]- ms-kyle-hide-in-noise | What happens when noise trading doubles?
> $\lambda$ halves, $\beta$ and the insider's profit double, informativeness is unchanged.
> The insider scales up to stay hidden, and the extra noise pays him.

> [!question]- ms-kyle-who-pays | Who pays the insider's profit?
> The noise traders: they lose $\lambda\sigma_u^2 = \tfrac12\sigma_u\sqrt{\Sigma_0}$ on average, exactly the insider's gain.
> The market maker breaks even.

> [!question]- ms-kyle-overtrading | Holding $\lambda$ fixed, what does the insider earn if he trades twice the equilibrium intensity?
> Zero in expectation: $b\Sigma_0 - \lambda b^2\Sigma_0$ at $b = 2\beta = 1/\lambda$ vanishes.
> The extra impact consumes the whole information rent.

> [!question]- ms-kyle-order-flow-variance | What is the variance of total order flow in equilibrium?
> $2\sigma_u^2$: the insider contributes $\beta^2\Sigma_0 = \sigma_u^2$.

> [!question]- ms-kyle-continuous-results | What changes in Kyle's continuous-auction limit?
> $\lambda = \sqrt{\Sigma_0}/\sigma_u$ is constant, all information is revealed by the end ($\Sigma(t) = (1-t)\Sigma_0$), and insider profit is $\sigma_u\sqrt{\Sigma_0}$.
> The insider trades gradually and the price is a Brownian motion with constant volatility.

> [!question]- ms-kyle-two-auctions | With two equally spaced auctions and $\sigma_v = \sigma_u = 1$, how does the insider's profit compare with one auction?
> About 0.621 against 0.5.
> Splitting trades across auctions reduces impact per share, and the backward recursion converges to 1 as auctions multiply.

> [!question]- ms-kyle-vs-gm | Contrast Kyle with Glosten-Milgrom.
> Glosten-Milgrom: unit trades arrive sequentially and take quotes as given, producing a bid-ask spread from adverse selection.
> Kyle: a strategic insider chooses size knowing his impact, producing a linear price schedule (lambda) and no spread.

> [!question]- ms-kyle-competing-insiders | What happens with several insiders sharing the same information?
> They compete and trade more aggressively, so information enters prices faster and their total profit falls.
> Holden and Subrahmanyam (1992) show the speed-up in a multi-period model.

> [!question]- ms-kyle-empirical-lambda | How would you estimate Kyle's lambda from data?
> Regress short-interval price changes on signed order flow (or order-flow imbalance); the slope is lambda.
> Use mid-quote changes, sign trades against quotes, and expect the slope to fall with depth and to vary intraday.

> [!question]- ms-kyle-linear-limits | Why is Kyle's lambda a poor model for the cost of a large metaorder?
> It implies linear, permanent impact; measured metaorder impact is concave (roughly square-root in size) and partly decays after execution.
> Use it for small flow and as a benchmark, not for sizing large orders.

## In this repo and SDE-Interview-Prep

- Code: [kyle_model.py](code/kyle_model.py) reproduces every number above, including the sequential-auction recursion (`python kyle_model.py`).

## Further reading

- Albert Kyle (1985), Continuous Auctions and Insider Trading, *Econometrica* 53(6).
- Maureen O'Hara, *Market Microstructure Theory* (Blackwell, 1995), chapter 4.
- Kerry Back (1992), Insider Trading in Continuous Time, *Review of Financial Studies* 5(3).
- Holden and Subrahmanyam (1992), Long-Lived Private Information and Imperfect Competition, *Journal of Finance* 47(1).
- Joel Hasbrouck, *Empirical Market Microstructure* (Oxford University Press, 2007).
- Related notes: [Spread Models: Roll and Glosten-Milgrom](03-Spread-Models-Roll-and-Glosten-Milgrom.md), [Market Impact Models](06-Market-Impact-Models.md).
