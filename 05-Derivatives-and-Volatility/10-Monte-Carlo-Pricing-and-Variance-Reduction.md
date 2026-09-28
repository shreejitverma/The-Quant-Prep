---
type: concept
track: [quant-research, quant-dev]
tier: core
status: solid
prereqs: [risk-neutral-pricing-and-ftap]
est_hours: 5
sources: [Paul Glasserman - Monte Carlo Methods in Financial Engineering (Springer 2003), Longstaff and Schwartz (2001) - Valuing American options by simulation - a simple least-squares approach - Review of Financial Studies 14(1), Broadie Glasserman and Kou (1997) - A continuity correction for discrete barrier options - Mathematical Finance 7(4), Andersen and Broadie (2004) - Primal-dual simulation algorithm for pricing multidimensional American options - Management Science 50(9), Broadie and Glasserman (1996) - Estimating security price derivatives using simulation - Management Science 42(2), Kemna and Vorst (1990) - A pricing method for options based on average asset values - Journal of Banking and Finance 14(1)]
---

# Monte Carlo Pricing and Variance Reduction

## TL;DR

- A Monte Carlo price is a sample mean of discounted payoffs under $Q$; report it with a standard error $\hat s/\sqrt{N}$, and remember that halving the error costs four times the paths.
- Simulate GBM exactly in log space; time-step bias only enters for path-dependent payoffs and non-GBM dynamics, and discrete monitoring must match the contract (Broadie-Glasserman-Kou shifts a barrier by $e^{\pm 0.5826\,\sigma\sqrt{\Delta t}}$).
- Variance reduction: antithetics help monotone payoffs (about 2x for an ATM call), control variates cut variance by $1 - \rho^2$ (geometric Asian for arithmetic Asian, $S_T$ for vanillas), importance sampling rescues rare events (100x for a deep OTM call), and quasi-random (Sobol plus Brownian bridge) improves the rate toward $1/N$.
- American options: Longstaff-Schwartz regresses discounted continuation value on basis functions of the state over in-the-money paths; the estimated policy is suboptimal, so the price is biased low (duality gives an upper bound).
- Greeks: bump with common random numbers, pathwise differentiation for Lipschitz payoffs (lowest variance), likelihood ratio for discontinuous payoffs (digitals, barriers) at the cost of higher variance.

## Learning objectives

- Price path-dependent payoffs by simulation with correct error bars.
- Apply antithetic, control variate, importance sampling and quasi-random methods.
- Price American options with Longstaff-Schwartz.
- Compute Greeks by bumping, pathwise and likelihood-ratio methods.

## Core concepts

### The estimator and its error

Price $V = E_Q[e^{-rT} h(S)]$ is estimated by $\hat V_N = \frac1N\sum_i Y_i$ with $Y_i = e^{-rT}h(S^{(i)})$ iid.
By the central limit theorem $\hat V_N \approx \mathcal N(V, s^2/N)$, so a 95% interval is $\hat V_N \pm 1.96\,\hat s/\sqrt N$.
The error is $O(N^{-1/2})$ regardless of dimension, which is why Monte Carlo wins for path-dependent and multi-asset payoffs where PDE grids explode.
Compare methods by efficiency, variance times cost per sample: a trick that halves variance but triples runtime loses.
The iid unit must be what you average: for antithetic pairs or batches, compute the standard error across pairs or batches, not across correlated individual paths.

### Simulating the paths

GBM has an exact scheme, so use it rather than Euler:

$$
S_{t+\Delta t} = S_t \exp\!\left((r - q - \tfrac12\sigma^2)\Delta t + \sigma\sqrt{\Delta t}\,Z\right).
$$

For a European payoff one step to $T$ suffices.
For SDEs without exact solutions (local vol, Heston) Euler has weak order 1: price bias $O(\Delta t)$.
The total error then balances statistical error $O(N^{-1/2})$ against bias $O(\Delta t)$; with a fixed budget, cutting steps to buy paths is often right.
In Heston the variance can go negative under Euler; use full truncation or Andersen's QE scheme.

Discrete versus continuous monitoring is a contract question, not a numerical one.
A continuously monitored barrier simulated on a daily grid misses crossings between dates, so knock-out options come out too expensive.
Broadie-Glasserman-Kou: a discretely monitored barrier $H$ is approximately a continuous barrier at $H e^{\pm\beta\sigma\sqrt{\Delta t}}$ with $\beta = -\zeta(1/2)/\sqrt{2\pi} \approx 0.5826$, shifted away from spot (up for an up barrier, down for a down barrier).
Alternatively, keep the grid and use the Brownian-bridge crossing probability $\exp(-2\ln(H/S_i)\ln(H/S_{i+1})/(\sigma^2\Delta t))$ between steps.

### Variance reduction

Antithetic variates: pair each $Z$ with $-Z$ and average.
The pair's variance is $\tfrac{s^2}{2}(1 + \rho)$ with $\rho = \text{corr}(Y(Z), Y(-Z))$, versus $s^2/2$ for two independent draws.
It helps when the payoff is monotone in $Z$ ($\rho < 0$) and hurts for symmetric payoffs such as a straddle, where $\rho > 0$.

Control variates: if $X$ has known mean $\mu_X$, use $Y - b(X - \mu_X)$.
The optimal $b^* = \text{Cov}(Y, X)/\text{Var}(X)$ (a regression slope) gives variance $s^2(1 - \rho_{XY}^2)$.
Estimating $b$ from the same paths introduces an $O(1/N)$ bias, negligible in practice.
Classic controls: the discounted terminal price (mean $S_0 e^{-qT}$), the Black-Scholes price of a related vanilla, and for arithmetic Asians the geometric Asian, which has a closed form because a geometric average of lognormals is lognormal (Kemna-Vorst), with $\rho$ above 0.99.
Controls are the Monte Carlo version of hedging: $Y - bX$ is the payoff minus a hedge, and variance falls by the hedge's $R^2$.

Importance sampling: sample from a density $g$ instead of $f$ and weight by the likelihood ratio $f/g$.
For a Gaussian driver, shifting $Z \to Z + \mu$ gives weight $w = e^{-\mu Y + \mu^2/2}$ evaluated at the shifted draw $Y$.
Choose $\mu$ so that paths land where the payoff lives, for example at the strike of a deep out-of-the-money option; a bad shift can increase variance without bound, so validate against a plain run.

Stratification and quasi-Monte Carlo: stratify the terminal draw (for example the Brownian endpoint), or replace pseudo-random numbers with a low-discrepancy sequence (Sobol) whose error behaves like $O((\log N)^d/N)$.
QMC needs a good ordering: build the path with a Brownian bridge or PCA so that the first, best-distributed coordinates carry most of the variance.
Randomised QMC (scrambled Sobol, several independent replications) restores honest error bars.

### American options: Longstaff-Schwartz

On a grid of exercise dates, the holder exercises when intrinsic value beats the continuation value $C(t, S_t) = E[\text{discounted future cash flow} \mid S_t]$.
Longstaff-Schwartz estimates $C$ by least-squares regression of realised discounted cash flows on basis functions (polynomials, Laguerre functions, or the European price) across paths, backwards in time:

1. Simulate paths; set each path's cash flow to its expiry payoff.
2. At each earlier date, discount cash flows one step and regress them on basis functions of $S_t$ using only in-the-money paths.
3. Exercise where intrinsic exceeds the fitted continuation; replace that path's cash flow with intrinsic.
4. The price is the average discounted cash flow (compared with immediate exercise at $t = 0$).

Only in-the-money paths enter the regression because only there is the decision live, and it makes the fit far better.
The regression is used for the decision, but realised cash flows (not fitted values) are what get averaged, which limits the error.
Any estimated policy is suboptimal, so a price computed on independent paths is a lower bound; the Andersen-Broadie dual method builds an upper bound from a martingale, and the gap measures policy quality.
Using the same paths for regression and pricing adds a small upward foresight bias.

### Greeks by simulation

- Bump and revalue: $(V(S_0 + h) - V(S_0 - h))/(2h)$, with the same random numbers in both runs (common random numbers). Without them, the variance of the difference is $O(1/h^2)$ and the estimate is useless.
- Pathwise: differentiate inside the expectation, $\partial_{S_0} E[h(S_T)] = E[h'(S_T)\,\partial S_T/\partial S_0]$. For a call, $\Delta = E[e^{-rT}\mathbf 1\{S_T > K\} S_T/S_0]$. Unbiased and lowest variance, but needs a payoff that is continuous (Lipschitz) in the parameter, so it fails for digitals and for gamma of a vanilla.
- Likelihood ratio: differentiate the density instead, $\partial_{S_0} E[h] = E[h(S_T)\,\partial_{S_0}\ln f(S_T)]$. For GBM, $\Delta = E[e^{-rT}h(S_T)\,Z/(S_0\sigma\sqrt T)]$. Works for any payoff, including digitals and barriers, but has higher variance, badly so for short maturities.
- Adjoint algorithmic differentiation (AAD) computes all pathwise sensitivities for a few times the cost of one price; it is the production answer for large books.

## Worked examples

All examples use $S_0 = 100$, $K = 100$, $T = 1$, $r = 5\%$, $\sigma = 20\%$, no dividends, where Black-Scholes gives 10.4506, unless stated.

### Example 1: error bars and the path budget

The discounted payoff has standard deviation $s = 14.72$ (exact, by quadrature).
With $N = 100{,}000$ paths the standard error is $14.72/\sqrt{10^5} = 0.0465$, a 95% half-width of 0.091, so a run giving 10.42 is consistent with 10.45.
To quote to $\pm 1$ cent at 95% you need $(1.96 \times 14.72/0.01)^2 \approx 8.3$ million paths.
That is why variance reduction matters more than hardware.

### Example 2: antithetic variates

The correlation between $Y(Z)$ and $Y(-Z)$ for this call is $\rho = -0.50$.
So an antithetic pair has variance $(1 + \rho) = 0.50$ times that of two independent paths: at equal payoff evaluations, antithetics halve the variance.
With 100,000 pairs the 95% half-width is 0.046, versus 0.092 for 100,000 plain paths (but the pairs cost 200,000 evaluations).
For a straddle, which is symmetric in $Z$ near the money, $\rho$ is positive and antithetics make things worse.

### Example 3: the terminal price as a control variate

Control $X = e^{-rT}S_T$ with known mean $S_0 = 100$.
On 100,000 paths $\hat b = 0.674$ (close to the call delta 0.637, as the hedging interpretation predicts) and $\rho = 0.924$, so variance falls by $1 - \rho^2 = 0.146$, a factor of 6.8.
The estimate is $10.467 \pm 0.035$ versus $10.42 \pm 0.092$ plain.

```python
import numpy as np

S0, K, T, r, sigma, N = 100.0, 100.0, 1.0, 0.05, 0.2, 100_000
rng = np.random.default_rng(42)
z = rng.standard_normal(N)
disc = np.exp(-r * T)
ST = lambda z: S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)

plain = disc * np.maximum(ST(z) - K, 0.0)
anti = 0.5 * (plain + disc * np.maximum(ST(-z) - K, 0.0))   # one iid sample per pair
X = disc * ST(z)                                            # control with known mean S0
b = np.cov(plain, X)[0, 1] / np.var(X, ddof=1)
cv = plain - b * (X - S0)

for name, y in [("plain", plain), ("antithetic", anti), ("control", cv)]:
    print(f"{name:10s} {y.mean():.4f} +/- {1.96 * y.std(ddof=1) / np.sqrt(len(y)):.4f}")
# plain 10.4205 +/- 0.0917, antithetic 10.4763 +/- 0.0459, control 10.4668 +/- 0.0350; BS 10.4506
```

### Example 4: importance sampling for a deep out-of-the-money call

Strike 160, same parameters: Black-Scholes price 0.1590.
Plain Monte Carlo with 100,000 paths: only 1.4% of paths finish in the money and the standard error is 0.0062, a 4% relative error.
Shift the normal draw by $\mu = (\ln(K/S_0) - (r - \tfrac12\sigma^2)T)/(\sigma\sqrt T) = 2.20$ so that the median path ends at the strike, and weight each payoff by $e^{-\mu Y + \mu^2/2}$.
The standard error drops to 0.00059: a variance reduction of about 111x, worth 11 million plain paths.

### Example 5: Longstaff-Schwartz American put

The Longstaff-Schwartz test case: $S_0 = 36$, $K = 40$, $r = 6\%$, $\sigma = 20\%$, $T = 1$, 50 exercise dates.
European put: 3.844.
A 5,000-step binomial tree with exercise allowed only on the 50 dates gives the Bermudan benchmark 4.478.
LSM with a quadratic basis and 100,000 paths (50,000 antithetic pairs) gives 4.466 with standard error 0.006; over 20 seeds the mean is 4.463.
The 0.015 shortfall is the low bias from a suboptimal exercise rule estimated with a three-term basis; the early-exercise premium is about 0.63.

```python
import numpy as np

def lsm_american_put(S0, K, r, sigma, T, steps=50, paths=100_000, seed=0):
    """Longstaff-Schwartz with basis 1, x, x^2 on in-the-money paths."""
    rng = np.random.default_rng(seed)
    dt = T / steps
    z = rng.standard_normal((paths // 2, steps))
    z = np.vstack([z, -z])                                   # antithetic pairs
    S = S0 * np.exp(np.cumsum((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z, axis=1))
    cash = np.maximum(K - S[:, -1], 0.0)                     # value if held to expiry
    for t in range(steps - 2, -1, -1):
        cash *= np.exp(-r * dt)                              # discount one step back to t
        itm = K - S[:, t] > 0
        x = S[itm, t] / K
        coef = np.polyfit(x, cash[itm], 2)                   # regress continuation value
        exercise = K - S[itm, t] > np.polyval(coef, x)
        idx = np.flatnonzero(itm)[exercise]
        cash[idx] = K - S[idx, t]
    cash *= np.exp(-r * dt)
    pairs = 0.5 * (cash[: paths // 2] + cash[paths // 2 :])    # antithetic pairs are the iid units
    price = max(pairs.mean(), K - S0)
    return price, pairs.std(ddof=1) / np.sqrt(len(pairs))

print(lsm_american_put(36, 40, 0.06, 0.2, 1.0))  # about (4.466, 0.006)
```

### Example 6: three ways to compute delta

True Black-Scholes delta 0.6368; 100,000 paths each.

- Pathwise, $e^{-rT}\mathbf 1\{S_T > K\}S_T/S_0$: 0.6345, standard error 0.0018.
- Likelihood ratio, $e^{-rT}(S_T - K)^+ Z/(S_0\sigma\sqrt T)$: 0.6391, standard error 0.0047, about 7x the variance.
- Central bump $h = 1$ with common random numbers: 0.6346, standard error 0.0018. With independent draws for the up and down runs: 0.593, standard error 0.033, useless.

For a digital call the pathwise estimator is identically zero (the payoff is flat almost everywhere), while likelihood ratio gives 0.01869 against the exact $e^{-rT}\varphi(d_2)/(S_0\sigma\sqrt T) = 0.01876$.

### Example 7: discrete barrier correction

A daily-monitored up-and-out barrier at 120 with $\sigma = 20\%$: $\beta\sigma\sqrt{\Delta t} = 0.5826 \times 0.2 \times \sqrt{1/252} = 0.00734$.
Price it as a continuously monitored barrier at $120\,e^{0.00734} = 120.88$.
Simulating on a daily grid with a continuous-barrier contract, you would instead need the Brownian-bridge crossing check, or the knock-out would be missed between fixings and the option overpriced.

## Pitfalls

- Reporting a Monte Carlo price without an error bar, or computing the error across correlated samples (antithetic halves, paths sharing a regression) instead of iid units.
- Bumping Greeks with fresh random numbers; always use common random numbers, and for discontinuous payoffs smooth the payoff or use likelihood ratio.
- Using pathwise derivatives for digitals, barriers or vanilla gamma; the derivative of an indicator is zero almost everywhere and the estimator is silently wrong.
- Simulating GBM with Euler in price space; it adds bias and can go negative when the exact log scheme is free.
- Confusing discrete and continuous monitoring, or calibrating on one and pricing the other.
- Calling an LSM price "the" American price; it is a lower bound whose bias depends on the basis, so benchmark against a tree or PDE or report a dual upper bound.
- Seeding the random generator differently between base and bumped runs in a parallel job, or reusing the same stream across threads.
- Using quasi-random numbers with naive incremental path construction, or computing a sample standard deviation from a single QMC run; use Brownian bridge ordering and randomised replications.

## Interview questions

> [!question]- deriv-mc-error-scaling | A Monte Carlo price has a standard error of 4 cents with 10,000 paths. How many paths for 1 cent?
> 160,000 paths: the error scales as $1/\sqrt N$, so reducing it 4x needs 16x the paths.
> This quadratic cost is why variance reduction beats brute force.

> [!question]- deriv-mc-antithetic-when | When do antithetic variates help, and when do they hurt?
> They help when the payoff is monotone in the driving normal, making $Y(Z)$ and $Y(-Z)$ negatively correlated; they hurt for symmetric payoffs such as straddles, where the correlation is positive.
> Pair variance is $\tfrac{s^2}{2}(1 + \rho)$; for an ATM call $\rho \approx -0.5$, halving variance at equal cost.

> [!question]- deriv-mc-control-variate-optimal | What is the optimal control variate coefficient and how much variance does it remove?
> $b^* = \text{Cov}(Y, X)/\text{Var}(X)$, and the variance falls to $(1 - \rho^2)$ of the original.
> It is a regression of payoff on control; for an ATM call on $e^{-rT}S_T$, $\rho = 0.92$ removes 85% of the variance and $b^*$ is close to the delta.

> [!question]- deriv-mc-geometric-asian-control | What control variate do you use for an arithmetic Asian option, and why does it work so well?
> The geometric-average Asian with the same fixings, which has a closed form because a product of lognormals is lognormal.
> The two averages are almost perfectly correlated (above 0.99), so the residual variance is tiny.

> [!question]- deriv-mc-importance-sampling | How would you price a deep out-of-the-money option by simulation efficiently?
> Importance sampling: shift the normal driver by $\mu$ so paths end near the strike, and weight each payoff by $e^{-\mu Y + \mu^2/2}$.
> For a 160 call on 100 at 20% vol this cuts variance about 100x; plain simulation lands only 1.4% of paths in the money.

> [!question]- deriv-mc-lsm-algorithm | Describe Longstaff-Schwartz for an American put.
> Simulate paths, set cash flows to the expiry payoff, then step backwards: regress discounted future cash flows on basis functions of $S_t$ over in-the-money paths, exercise where intrinsic exceeds the fitted continuation, and overwrite those paths' cash flows.
> The price is the average discounted cash flow, compared with immediate exercise.

> [!question]- deriv-mc-lsm-bias | Is a Longstaff-Schwartz price biased, and in which direction?
> Low: any estimated exercise rule is suboptimal, so priced on independent paths it is a lower bound (in-sample reuse adds a small upward foresight bias).
> An upper bound comes from the Andersen-Broadie dual; in the 36/40 put example LSM gives about 4.46 against a benchmark of 4.478.

> [!question]- deriv-mc-lsm-itm-only | Why does Longstaff-Schwartz regress only on in-the-money paths?
> The exercise decision only exists where intrinsic value is positive, and fitting the continuation function there concentrates the basis where it matters.
> Including out-of-the-money paths wastes regression capacity on a region where the answer (continue) is known.

> [!question]- deriv-mc-pathwise-vs-lr | Pathwise versus likelihood-ratio Greeks: when do you use each?
> Pathwise when the payoff is Lipschitz in the parameter (vanilla delta, vega): unbiased and low variance. Likelihood ratio when it is discontinuous (digitals, barriers, gamma): it differentiates the density, not the payoff, at the cost of higher variance.
> For a call delta the LR variance is about 7x the pathwise one.

> [!question]- deriv-mc-pathwise-digital-fails | What does the pathwise delta estimator give for a digital option, and why?
> Zero on every path, so the estimate is zero: the payoff's derivative with respect to spot is zero almost everywhere and the delta lives in the discontinuity.
> Use likelihood ratio, a smoothed payoff, or a tight call spread.

> [!question]- deriv-mc-common-random-numbers | Why must bump-and-revalue Greeks use common random numbers?
> With independent draws, the difference of two noisy prices has variance $O(1/h^2)$ that swamps the signal; with common numbers the noise cancels and the variance is $O(1)$ for smooth payoffs.
> In the call example, independent bumps give a standard error of 0.033 on delta versus 0.0018 with common numbers.

> [!question]- deriv-mc-discrete-barrier | You simulate a continuously monitored barrier option on a daily grid. What goes wrong and how do you fix it?
> Crossings between grid dates are missed, so knock-outs are overpriced and knock-ins underpriced.
> Use the Brownian-bridge crossing probability between steps, or price a discretely monitored contract via the BGK shift $H e^{\pm 0.5826\sigma\sqrt{\Delta t}}$.

> [!question]- deriv-mc-qmc | Why does quasi-Monte Carlo beat pseudo-random sampling, and what can go wrong?
> Low-discrepancy points fill space evenly, giving error close to $O(1/N)$ rather than $O(1/\sqrt N)$ for smooth, effectively low-dimensional integrands.
> It degrades in high effective dimension and gives no error bar on its own; use Brownian-bridge path construction and randomised (scrambled) replications.

> [!question]- deriv-mc-euler-bias | What is the bias of an Euler scheme and how do you balance steps against paths?
> Weak order 1: price bias $O(\Delta t)$, while the statistical error is $O(N^{-1/2})$.
> For a fixed budget, balance them so the bias is comparable to the standard error; for GBM use the exact log scheme and avoid the bias entirely.

## In this repo and SDE-Interview-Prep

- Prev: [Stochastic Volatility: Heston and SABR](09-Stochastic-Volatility-Heston-and-SABR.md). Next: [Finite Differences and Fourier Pricing](11-Finite-Differences-and-Fourier-Pricing.md).
- Payoffs priced this way: [Exotic Options](12-Exotic-Options.md).

## Further reading

- Paul Glasserman, *Monte Carlo Methods in Financial Engineering*, chapters on variance reduction, quasi-Monte Carlo, Greeks and American options.
- F. Longstaff and E. Schwartz (2001), "Valuing American options by simulation: a simple least-squares approach", *Review of Financial Studies* 14(1).
- M. Broadie, P. Glasserman and S. Kou (1997), "A continuity correction for discrete barrier options", *Mathematical Finance* 7(4).
- L. Andersen and M. Broadie (2004), "Primal-dual simulation algorithm for pricing multidimensional American options", *Management Science* 50(9).
- M. Broadie and P. Glasserman (1996), "Estimating security price derivatives using simulation", *Management Science* 42(2).
- A. Kemna and A. Vorst (1990), "A pricing method for options based on average asset values", *Journal of Banking and Finance* 14(1).
