---
type: concept
track: [quant-trader, quant-research]
tier: advanced
status: solid
prereqs: [market-impact-models, convex-optimization-and-kkt]
est_hours: 4
sources: [Almgren and Chriss (2000) Optimal Execution of Portfolio Transactions. Journal of Risk 3(2) 5-39, Bertsimas and Lo (1998) Optimal Control of Execution Costs. Journal of Financial Markets 1(1) 1-50, Almgren (2003) Optimal Execution with Nonlinear Impact Functions and Trading-Enhanced Risk. Applied Mathematical Finance 10(1) 1-18, Obizhaeva and Wang (2013) Optimal Trading Strategy and Supply/Demand Dynamics. Journal of Financial Markets 16(1) 1-32, Cartea Jaimungal and Penalva (2015) Algorithmic and High-Frequency Trading. Cambridge University Press - chapter 6, Gueant (2016) The Financial Mathematics of Market Liquidity. CRC Press]
---

# Optimal Execution: Almgren-Chriss

## TL;DR

- Selling $X$ shares over $[0, T]$ trades off impact cost (trade slowly) against price risk (trade fast); Almgren-Chriss minimise $\mathbb{E}[\text{cost}] + \lambda\,\text{Var}[\text{cost}]$ with linear temporary and permanent impact.
- The optimal holdings are $x(t) = X\,\sinh(\kappa(T - t))/\sinh(\kappa T)$ with urgency $\kappa = \sqrt{\lambda\sigma^2/\eta}$; $1/\kappa$ is the trade's characteristic time.
- $\lambda = 0$ gives TWAP (a straight line); larger $\lambda$ front-loads; $\lambda \to \infty$ sells immediately.
- Varying $\lambda$ traces a convex efficient frontier of expected cost against risk; at TWAP its slope is zero, so the first unit of risk reduction is free.
- With impact scaled by market volume, the risk-neutral optimum is VWAP, which is why VWAP and TWAP are special cases of the same framework.

## Learning objectives

- Derive the Almgren-Chriss trajectory and the efficient frontier of execution.
- Explain how risk aversion changes the schedule.
- Compute expected cost and variance of a schedule and pick a point on the frontier.
- Show TWAP and VWAP as special cases.

## Core concepts

### The model

Sell $X$ shares by time $T$, in $N$ intervals of length $\tau = T/N$.
Holdings are $x_0 = X, x_1, \dots, x_N = 0$ and $n_k = x_{k-1} - x_k$ shares are sold in interval $k$ at rate $v_k = n_k/\tau$.

- The unaffected price is a random walk with permanent impact: $S_k = S_{k-1} + \sigma\sqrt{\tau}\,\xi_k - \tau\,g(v_k)$ with $g(v) = \gamma v$.
- Each sale also pays a temporary concession: the execution price is $\tilde S_k = S_{k-1} - h(v_k)$ with $h(v) = \varepsilon\,\text{sgn}(v) + \eta v$.

Here $\sigma$ is in dollars per share per square-root time, $\varepsilon$ is a fixed cost per share (half-spread and fees), $\eta$ the temporary and $\gamma$ the permanent impact coefficient.

### Cost of a schedule

The implementation shortfall is $X S_0 - \sum_k n_k \tilde S_k$.
Summing by parts,

$$
\mathbb{E}[\text{IS}] = \tfrac12\gamma X^2 + \varepsilon \sum_k |n_k| + \frac{\tilde\eta}{\tau}\sum_k n_k^2, \qquad \tilde\eta = \eta - \tfrac12\gamma\tau,
$$

$$
\text{Var}[\text{IS}] = \sigma^2 \tau \sum_{k=1}^{N} x_k^2 .
$$

- The permanent term $\tfrac12\gamma X^2$ does not depend on the schedule, so linear permanent impact does not affect the optimal trajectory.
- The temporary term is a sum of squares, minimised for a fixed total by equal slices.
- The variance comes from holding inventory while the price moves, minimised by selling at once.

### Deriving the trajectory

Minimise $U = \mathbb{E}[\text{IS}] + \lambda\,\text{Var}[\text{IS}]$ over $x_1, \dots, x_{N-1}$ (all sales, so $\sum|n_k| = X$ is fixed).
Setting $\partial U/\partial x_k = 0$:

$$
\frac{2\tilde\eta}{\tau}\big(2x_k - x_{k-1} - x_{k+1}\big) + 2\lambda\sigma^2\tau\,x_k = 0
\quad\Longrightarrow\quad
\frac{x_{k-1} - 2x_k + x_{k+1}}{\tau^2} = \tilde\kappa^2 x_k, \qquad \tilde\kappa^2 = \frac{\lambda\sigma^2}{\tilde\eta}.
$$

This linear difference equation has solutions $e^{\pm\kappa t_k}$ with $\frac{2}{\tau^2}(\cosh\kappa\tau - 1) = \tilde\kappa^2$; imposing $x_0 = X$ and $x_N = 0$ gives

$$
\boxed{x_k = X\,\frac{\sinh\big(\kappa(T - t_k)\big)}{\sinh(\kappa T)}, \qquad n_k = \frac{2\sinh(\kappa\tau/2)}{\sinh(\kappa T)}\cosh\big(\kappa(T - t_{k-1/2})\big)X.}
$$

In continuous time the same answer comes from minimising $\int_0^T \big(\eta\,\dot x^2 + \lambda\sigma^2 x^2\big)\,dt$: the Euler-Lagrange equation is $\ddot x = \kappa^2 x$ with $\kappa = \sqrt{\lambda\sigma^2/\eta}$, and $\kappa \to \tilde\kappa$ as $\tau \to 0$.

### Reading the solution

- $\kappa$ measures urgency; $1/\kappa$ (which Almgren and Chriss call the half-life of the trade) is the time over which most of the position is worked off.
  If $T \gg 1/\kappa$ the order is done long before the deadline.
- $\lambda = 0$: $\kappa = 0$ and $x_k = X(1 - t_k/T)$, a straight line (TWAP); this is the Bertsimas and Lo (1998) risk-neutral result with linear impact.
- $\lambda \to \infty$: everything is sold in the first interval.
- Risk aversion only matters through $\lambda\sigma^2/\eta$: higher volatility or lower impact makes you trade faster, exactly like higher risk aversion.

### The efficient frontier

Each $\lambda \ge 0$ gives a schedule with expected cost $E(\lambda)$ and variance $V(\lambda)$.
The curve $\{(V(\lambda), E(\lambda))\}$ is the efficient frontier of execution: no schedule has both lower expected cost and lower variance.
It is smooth and convex, and at the TWAP end $dE/dV = 0$ (TWAP minimises $E$, so the first-order change in $E$ is zero), which means a little risk reduction costs almost nothing.
Choosing $\lambda$ is a business decision: a desk can fix it as a risk-aversion parameter, or pick the schedule minimising a quantile of cost such as $E + 1.645\sqrt{V}$ (a value-at-risk of execution cost).

### TWAP and VWAP as special cases

- TWAP: the risk-neutral solution with constant volatility and time-homogeneous linear impact.
- VWAP: suppose the temporary cost in bucket $k$ scales inversely with expected market volume $V_k$ (trading the same shares is cheaper when the market is busy), so cost is $\sum_k c\,n_k^2/V_k$.
  Minimising subject to $\sum n_k = X$ with a Lagrange multiplier gives $n_k \propto V_k$: VWAP is the risk-neutral optimum in volume time.

### Extensions and how practitioners use it

- Nonlinear temporary impact $h(v) \propto v^{\beta}$ (Almgren 2003) keeps the structure but loses the closed form.
- Transient impact with resilience (Obizhaeva and Wang 2013) produces block trades at the start and end plus continuous trading in between.
- Alpha or short-term drift adds a linear term that tilts the schedule toward or away from the front.
- Implementation-shortfall algorithms at banks and brokers expose an urgency or risk-aversion setting that maps to $\kappa$, add participation caps and limit prices, and re-optimise as fills, volume and volatility come in; the static Almgren-Chriss schedule is the backbone, not the whole algorithm.

## Worked examples

### Example 1: trajectories for four risk aversions

Sell $X = 1{,}000{,}000$ shares over $T = 5$ days in $N = 10$ half-day intervals, with $\sigma = 0.95$ dollars per share per $\sqrt{\text{day}}$ (about 30% annual volatility on a $50 stock), $\varepsilon = 0.0625$, $\eta = 2.5 \times 10^{-6}$ and $\gamma = 2.5 \times 10^{-7}$, so $\tilde\eta = 2.4375 \times 10^{-6}$.
Holdings in thousands of shares:

| $\lambda$ | $\kappa$ (1/day) | $t = 0$ | 0.5 | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 | 5 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 (TWAP) | 0 | 1000 | 900 | 800 | 700 | 600 | 500 | 400 | 300 | 200 | 100 | 0 |
| $10^{-7}$ | 0.1923 | 1000 | 875 | 759 | 649 | 546 | 447 | 353 | 262 | 173 | 86 | 0 |
| $10^{-6}$ | 0.6062 | 1000 | 737 | 542 | 398 | 290 | 210 | 148 | 101 | 62 | 30 | 0 |
| $10^{-5}$ | 1.8568 | 1000 | 395 | 156 | 62 | 24 | 10 | 4 | 1 | 1 | 0 | 0 |

Each sinh trajectory matches the solution of the first-order linear system computed directly.
For $\lambda = 10^{-6}$ the continuous approximation $\sqrt{\lambda\sigma^2/\eta} = 0.6008$ is close to the discrete 0.6062, and $1/\kappa \approx 1.65$ days.

### Example 2: the frontier

| Schedule | Expected cost ($) | Std of cost ($) |
| :--- | ---: | ---: |
| TWAP ($\lambda = 0$) | 675,000 | 1,134,047 |
| $\lambda = 10^{-7}$ | 682,733 | 1,060,448 |
| $\lambda = 10^{-6}$ | 945,216 | 723,822 |
| $\lambda = 10^{-5}$ | 2,300,817 | 288,990 |
| Sell all in the first interval | 5,062,500 | 0 |

TWAP's expected cost decomposes as permanent $\tfrac12\gamma X^2 = 125{,}000$, fixed $\varepsilon X = 62{,}500$ and temporary $\tilde\eta X^2/T = 487{,}500$.
Moving from TWAP to $\lambda = 10^{-7}$ cuts the standard deviation by 73,599 dollars for 7,733 dollars of expected cost; the frontier is flat near TWAP.
At $\lambda = 10^{-9}$ the cost rises by only 0.915 dollars while the standard deviation falls by 807.5 dollars.

### Example 3: choose the schedule by a cost quantile

Search $\lambda$ on a log grid to minimise $E + 1.645\,\text{sd}$.
The minimum is at $\lambda \approx 1.2023 \times 10^{-6}$, with expected cost 1,005,856, standard deviation 684,581 and $E + 1.645\,\text{sd} = 2{,}131{,}992$ dollars, against 2,540,507 for TWAP.
"I accept about 331,000 dollars more expected cost to cut the 95% cost quantile by about 409,000 dollars."

### Example 4: VWAP from a volume-scaled cost

A ten-bucket volume profile of 16, 11, 8, 7, 6, 6, 7, 9, 12 and 18% of the day, and cost $\sum_k c\,n_k^2/V_k$.
Solving the KKT system gives $n_k = X V_k$: 160,000 shares in the first bucket and 60,000 in the quiet midday bucket.
Under this cost model, equal slices (TWAP) would cost 1.1475 times as much as the VWAP schedule.

## Pitfalls

- Using annual volatility with time measured in days, or $\sigma$ in percent when the model wants dollars per share; keep units consistent.
- Forgetting $\tilde\eta = \eta - \tfrac12\gamma\tau$ in the discrete model, or the $\cosh$ relation between $\kappa$ and $\tilde\kappa$ when $\kappa\tau$ is not small.
- Thinking permanent impact changes the optimal schedule; with linear permanent impact it adds a constant.
- Presenting the static schedule as the algorithm: real algorithms re-plan on fills, volume and price, cap participation and respect limit prices.
- Picking $\lambda$ without units: it is in inverse dollars, and its sensible range depends on order size and volatility.
- Ignoring that linear temporary impact is a simplification; with concave impact the cost of speeding up is smaller than the model says.
- Using mean-variance on a single order in isolation when the portfolio's other positions hedge part of the risk.

## Interview questions

> [!question]- ms-ac-objective | What does Almgren-Chriss optimise?
> $\mathbb{E}[\text{IS}] + \lambda\,\text{Var}[\text{IS}]$ over the liquidation schedule.
> Slow trading lowers impact cost; fast trading lowers price risk.

> [!question]- ms-ac-trajectory | State the optimal Almgren-Chriss trajectory.
> $x(t) = X\sinh(\kappa(T - t))/\sinh(\kappa T)$ with $\kappa = \sqrt{\lambda\sigma^2/\eta}$.
> It solves $\ddot x = \kappa^2 x$ with $x(0) = X$, $x(T) = 0$.

> [!question]- ms-ac-euler-lagrange | Derive the ODE behind the trajectory.
> Minimise $\int(\eta\dot x^2 + \lambda\sigma^2x^2)\,dt$; the Euler-Lagrange equation $\frac{d}{dt}(2\eta\dot x) = 2\lambda\sigma^2 x$ gives $\ddot x = \kappa^2 x$.

> [!question]- ms-ac-expected-cost | Write the expected cost of a discrete schedule with linear impact.
> $\tfrac12\gamma X^2 + \varepsilon\sum|n_k| + (\tilde\eta/\tau)\sum n_k^2$ with $\tilde\eta = \eta - \tfrac12\gamma\tau$.
> The variance is $\sigma^2\tau\sum x_k^2$.

> [!question]- ms-ac-permanent-irrelevant | Why does linear permanent impact not affect the optimal schedule?
> Its total contribution is $\tfrac12\gamma X^2$ whatever the schedule.
> Each share sold depresses the price for all later shares by the same amount per share, regardless of timing.

> [!question]- ms-ac-lambda-zero | What is the optimal schedule for a risk-neutral trader?
> TWAP: equal slices, $x(t) = X(1 - t/T)$.
> With $\lambda = 0$ only $\sum n_k^2$ matters, minimised by equal $n_k$.

> [!question]- ms-ac-twap-cost | $X = 10^6$, $T = 5$ days, $\tilde\eta = 2.4375 \times 10^{-6}$, $\gamma = 2.5 \times 10^{-7}$, $\varepsilon = 0.0625$. TWAP expected cost?
> 675,000 dollars: 125,000 permanent, 62,500 fixed, 487,500 temporary ($\tilde\eta X^2/T$).

> [!question]- ms-ac-urgency-drivers | Which parameters make the optimal schedule more front-loaded?
> Higher risk aversion, higher volatility or lower temporary impact: all raise $\kappa^2 = \lambda\sigma^2/\eta$.

> [!question]- ms-ac-half-life | What does $1/\kappa$ mean?
> The characteristic time of the trade (Almgren and Chriss call it its half-life): the position decays roughly like $e^{-\kappa t}$ when $T \gg 1/\kappa$.
> For $\kappa = 0.606$ per day it is about 1.65 days.

> [!question]- ms-ac-frontier-slope | Why is reducing risk from TWAP almost free?
> TWAP minimises expected cost, so $dE = 0$ to first order while variance falls linearly in the deviation.
> In the example, $\lambda = 10^{-9}$ costs 0.915 dollars and cuts the standard deviation by 807.5 dollars.

> [!question]- ms-ac-var-choice | How can a desk choose $\lambda$ without a utility function?
> Minimise a cost quantile such as $E + 1.645\,\text{sd}$ across the frontier.
> In the example this picks $\lambda \approx 1.2 \times 10^{-6}$ and cuts the 95% cost quantile from about 2.54 to 2.13 million dollars.

> [!question]- ms-ac-vwap-special-case | When is VWAP optimal?
> When temporary impact scales inversely with market volume and the trader is risk-neutral: minimising $\sum c\,n_k^2/V_k$ with $\sum n_k = X$ gives $n_k \propto V_k$.

> [!question]- ms-ac-immediate | What does selling everything in the first interval cost, and when is it optimal?
> Expected cost $\tfrac12\gamma X^2 + \varepsilon X + \tilde\eta X^2/\tau$ with zero variance.
> It is the $\lambda \to \infty$ limit of the frontier.

> [!question]- ms-ac-limitations | Name three limitations of the basic Almgren-Chriss model.
> Linear temporary impact (reality is concave), no impact decay (impact is transient), and a static schedule (real algorithms adapt to fills, volume and price).
> It also ignores alpha, spread dynamics and venue choice.

> [!question]- ms-ac-bertsimas-lo | What did Bertsimas and Lo (1998) show?
> That a risk-neutral trader with linear price impact and no information splits the order equally over time.
> Almgren-Chriss add risk aversion and recover that result at $\lambda = 0$.

> [!question]- ms-ac-transient | How does transient impact (Obizhaeva-Wang) change the optimal strategy?
> It adds discrete block trades at the start and end, with continuous trading in between, because a block's impact partly decays before the next trades.

## In this repo and SDE-Interview-Prep

- Code: [almgren_chriss.py](code/almgren_chriss.py) reproduces every number above and checks the sinh solution against a direct linear solve (`python almgren_chriss.py`).
- Code: [execution_algos.py](code/execution_algos.py) for TWAP, VWAP and POV schedules.
- [Smart order routing and execution algorithms (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/11%20-%20Participant-Side%20Systems/Smart%20Order%20Routing%20and%20Execution%20Algorithms.md)

## Further reading

- Almgren and Chriss (2000), Optimal Execution of Portfolio Transactions, *Journal of Risk* 3(2).
- Bertsimas and Lo (1998), Optimal Control of Execution Costs, *Journal of Financial Markets* 1(1).
- Robert Almgren (2003), Optimal Execution with Nonlinear Impact Functions and Trading-Enhanced Risk, *Applied Mathematical Finance* 10(1).
- Obizhaeva and Wang (2013), Optimal Trading Strategy and Supply/Demand Dynamics, *Journal of Financial Markets* 16(1).
- Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (Cambridge University Press, 2015), chapter 6.
- Olivier Gueant, *The Financial Mathematics of Market Liquidity* (CRC Press, 2016).
- Related notes: [Market Impact Models](06-Market-Impact-Models.md), [Execution Algorithms and TCA](08-Execution-Algorithms-and-TCA.md), [Convex Optimization and KKT](../03-Linear-Algebra-and-Optimization/08-Convex-Optimization-and-KKT.md).
