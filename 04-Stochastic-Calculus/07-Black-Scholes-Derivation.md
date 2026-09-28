---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [ito-integral-and-ito-lemma, risk-neutral-pricing-and-ftap]
est_hours: 4
sources: [Black and Scholes - The Pricing of Options and Corporate Liabilities (Journal of Political Economy 1973), Merton - Theory of Rational Option Pricing (Bell Journal of Economics and Management Science 1973), Shreve - Stochastic Calculus for Finance II (Springer 2004) chapters 4 and 5, Hull - Options Futures and Other Derivatives, Leland - Option Pricing and Replication with Transactions Costs (Journal of Finance 1985)]
---

# Black-Scholes Derivation

## TL;DR

- Hold the option and short $\Delta = V_S$ shares; Ito's lemma shows the $dW$ terms cancel, so the portfolio is riskless and must earn $r$, which gives $V_t + \tfrac12\sigma^2S^2V_{SS} + rSV_S - rV = 0$.
- The PDE has no $\mu$: the hedge removes all exposure to the stock's direction.
- Feynman-Kac turns the PDE into $V_0 = e^{-rT}E^Q[\text{payoff}(S_T)]$ with $dS = rS\,dt + \sigma S\,dW^Q$.
- Computing that expectation gives $C = S_0N(d_1) - Ke^{-rT}N(d_2)$, with $d_{1,2} = \frac{\ln(S_0/K) + (r \pm \sigma^2/2)T}{\sigma\sqrt{T}}$.
- The PDE is a Greeks identity, $\Theta + \tfrac12\sigma^2S^2\Gamma + rS\Delta = rV$: a delta-hedged option earns $\tfrac12\Gamma S^2(\sigma_{\text{realised}}^2 - \sigma_{\text{implied}}^2)\,dt$.

## Learning objectives

- Derive the Black-Scholes PDE by delta hedging.
- Derive the call price as a risk-neutral expectation.
- State every model assumption and which ones fail in practice.

## Core concepts

### Assumptions

1. The stock follows GBM, $dS = \mu S\,dt + \sigma S\,dW$, with constant $\mu$ and $\sigma$.
2. The risk-free rate $r$ is constant and you can borrow and lend any amount at it.
3. No dividends during the option's life (a known continuous yield $q$ is an easy extension).
4. Trading is continuous, frictionless (no transaction costs, taxes or bid-ask spread), and allows short sales and fractional shares.
5. No arbitrage.
6. The option is European.

Nothing is assumed about investors' risk preferences or about $\mu$.

### Derivation 1: delta hedging

Let $V(t, S)$ be the option value.
By [Ito's lemma](02-Ito-Integral-and-Ito-Lemma.md), with $(dS)^2 = \sigma^2S^2\,dt$,

$$
dV = \Big(V_t + \mu SV_S + \tfrac12\sigma^2S^2V_{SS}\Big)dt + \sigma SV_S\,dW.
$$

Form $\Pi = V - \Delta S$, holding $\Delta$ fixed over $dt$ (self-financing).
Then

$$
d\Pi = \Big(V_t + \mu SV_S + \tfrac12\sigma^2S^2V_{SS} - \Delta\mu S\Big)dt + \sigma S(V_S - \Delta)\,dW.
$$

Choosing $\Delta = V_S$ kills the $dW$ term, and the $\mu$ terms cancel with it.
The portfolio is now riskless over $dt$, so no arbitrage forces $d\Pi = r\Pi\,dt = r(V - SV_S)\,dt$.
Equating the drifts:

$$
V_t + \tfrac12\sigma^2S^2V_{SS} + rSV_S - rV = 0, \qquad V(T, S) = \text{payoff}(S).
$$

The PDE is linear, so it prices any European payoff; only the terminal condition changes.
Two quick solution checks: $V = S$ (the stock) and $V = Ke^{-r(T - t)}$ (a bond) both satisfy it.

### Reduction to the heat equation

Set $\tau = T - t$, $x = \ln S + (r - \tfrac12\sigma^2)\tau$ and $V = e^{-r\tau}u(x, \tau)$.
Substituting ($V_S = e^{-r\tau}u_x/S$, $V_{SS} = e^{-r\tau}(u_{xx} - u_x)/S^2$) cancels every first-order term and leaves

$$
u_\tau = \tfrac12\sigma^2u_{xx}, \qquad u(x, 0) = \text{payoff}(e^x).
$$

The heat equation is solved by convolving the initial data with a Gaussian of variance $\sigma^2\tau$:
$u(x, \tau) = E[\text{payoff}(e^{x + \sigma\sqrt{\tau}Z})]$, which is exactly the risk-neutral expectation below.
This is the Feynman-Kac link (see [Feynman-Kac and Pricing PDEs](06-Feynman-Kac-and-Pricing-PDEs.md)).

### Derivation 2: risk-neutral expectation

By [risk-neutral pricing](04-Risk-Neutral-Pricing-and-FTAP.md), $C = e^{-rT}E^Q[(S_T - K)^+]$ with $S_T = S_0\exp\big((r - \tfrac12\sigma^2)T + \sigma\sqrt{T}Z\big)$ and $Z \sim N(0,1)$.
The option is in the money iff $Z > -d_2$, where $d_2 = \frac{\ln(S_0/K) + (r - \sigma^2/2)T}{\sigma\sqrt{T}}$.
Split the expectation:

- Strike leg: $E^Q[K\mathbf{1}_{Z > -d_2}] = KN(d_2)$.
- Stock leg: $E^Q[S_T\mathbf{1}_{Z > -d_2}] = S_0e^{rT}\int_{-d_2}^\infty e^{\sigma\sqrt{T}z - \sigma^2T/2}\varphi(z)\,dz$.
  Completing the square, $e^{\sigma\sqrt{T}z - \sigma^2T/2}\varphi(z) = \varphi(z - \sigma\sqrt{T})$, so the integral is $P(Z + \sigma\sqrt{T} > -d_2) = N(d_2 + \sigma\sqrt{T}) = N(d_1)$.

Therefore

$$
C = S_0N(d_1) - Ke^{-rT}N(d_2), \qquad d_1 = d_2 + \sigma\sqrt{T}.
$$

Put-call parity $C - P = S_0 - Ke^{-rT}$ gives $P = Ke^{-rT}N(-d_2) - S_0N(-d_1)$.
Interpretations: $N(d_2)$ is the $Q$-probability of exercise, $N(d_1)$ is the delta and also the exercise probability under the share measure, and $S_0N(d_1)$ is the asset-or-nothing leg.
For intuition and the full set of Greeks, see [Black-Scholes Formula and Intuition](../05-Derivatives-and-Volatility/04-Black-Scholes-Formula-and-Intuition.md) and [The Greeks](../05-Derivatives-and-Volatility/05-The-Greeks.md).

### The PDE as a Greeks identity and the hedger's P&L

In Greek notation the PDE reads $\Theta + \tfrac12\sigma^2S^2\Gamma + rS\Delta - rV = 0$.
For a delta-hedged long option (take $r = 0$ for clarity), $\Theta = -\tfrac12\sigma_i^2S^2\Gamma$ at the implied volatility $\sigma_i$.
If the stock actually moves with realised variance $\sigma_r^2$, then $(dS)^2 = \sigma_r^2S^2\,dt$ and the hedged P&L over $dt$ is

$$
\tfrac12\Gamma(dS)^2 + \Theta\,dt = \tfrac12\Gamma S^2\big(\sigma_r^2 - \sigma_i^2\big)dt.
$$

Long gamma pays theta and profits when realised volatility exceeds implied; that is the whole business of [gamma scalping](../05-Derivatives-and-Volatility/06-Delta-Hedging-and-Gamma-Scalping.md).
The P&L is path-dependent: it is weighted by $\Gamma S^2$, so realised volatility near the strike close to expiry matters most.

### Which assumptions fail, and what happens

| Assumption | Reality | Consequence |
| :--- | :--- | :--- |
| Constant $\sigma$ | Volatility is stochastic and differs by strike | Implied volatility smile and skew; one $\sigma$ cannot fit all strikes |
| Continuous paths | Jumps and gaps | Unhedgeable gap risk; OTM puts richer than Black-Scholes |
| Continuous hedging | Discrete rebalancing | Hedging error with standard deviation about $\sqrt{\pi/4}\,\sigma\,\text{vega}/\sqrt{N}$ for $N$ rebalances |
| No transaction costs | Spreads and impact | Leland: effectively widen or narrow $\sigma$; trade off hedge frequency against cost |
| Constant $r$, free borrowing | Stochastic rates, borrow fees, funding spreads | Matters for long-dated options and hard-to-borrow names |
| No dividends | Discrete dividends | Adjust the forward; early exercise of American calls |

Despite this, the formula survives as a quoting convention: prices are quoted as implied volatilities, and the smile encodes everything the model misses.

## Worked examples

### Numerical price with a Monte Carlo check

"Price a call with $S_0 = 100$, $K = 105$, $T = 0.5$, $r = 5\%$, $\sigma = 25\%$."
$\sigma\sqrt{T} = 0.1768$ and $\ln(100/105) = -0.0488$.
$d_1 = \frac{-0.0488 + (0.05 + 0.03125)(0.5)}{0.1768} = -0.0462$ and $d_2 = -0.2230$.
$N(d_1) = 0.4816$, $N(d_2) = 0.4118$, so $C = 48.16 - 105e^{-0.025}(0.4118) = 5.99$.
Parity gives the put: $5.99 - 100 + 105e^{-0.025} = 8.40$.

```python
import numpy as np
from scipy.stats import norm
S, K, T, r, s = 100, 105, 0.5, 0.05, 0.25
d1 = (np.log(S / K) + (r + s**2 / 2) * T) / (s * np.sqrt(T)); d2 = d1 - s * np.sqrt(T)
print(S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))       # 5.9885
z = np.random.default_rng(4).standard_normal(4_000_000)
ST = S * np.exp((r - s**2 / 2) * T + s * np.sqrt(T) * z)
print(np.exp(-r * T) * np.maximum(ST - K, 0).mean())              # 5.984
```

A central finite-difference check of the PDE at $t = 0.1$ gives a residual of order $10^{-7}$.

### At-the-money approximation

"Quick price for an at-the-money-forward call?"
With $K = S_0e^{rT}$, $d_{1,2} = \pm\tfrac12\sigma\sqrt{T}$, and $N(x) - N(-x) \approx 2x\varphi(0)$ for small $x$ gives

$$
C \approx S_0\,\frac{\sigma\sqrt{T}}{\sqrt{2\pi}} \approx 0.4\,\sigma S_0\sqrt{T}.
$$

For $S_0 = K = 100$, $r = 0$, $\sigma = 20\%$, $T = 1$: exact $7.966$, approximation $7.979$ (or $8.0$ with the rounded $0.4$).
The price is linear in volatility at the money, which is why ATM vega is about $0.4S_0\sqrt{T}$ per unit of volatility.

### Which powers of $S$ solve the PDE?

"Find all $p$ such that $V = S^p$ (no time dependence) solves the Black-Scholes PDE."
Substitute: $\tfrac12\sigma^2p(p - 1)S^p + rpS^p - rS^p = 0$, i.e. $\tfrac12\sigma^2p^2 + (r - \tfrac12\sigma^2)p - r = 0$.
The roots are $p = 1$ and $p = -2r/\sigma^2$.
$p = 1$ is the stock itself; $S^{-2r/\sigma^2}$ is the building block for perpetual American puts and barrier reflections.
For $r = 5\%$, $\sigma = 25\%$, $p = -1.6$, and the residual is zero to machine precision.

### Discrete hedging error

"You sell an at-the-money one-year call ($\sigma = 20\%$, $r = 0$, $S_0 = 100$) and delta-hedge $N$ times at the true volatility. How big is the hedging error?"
Each rebalance leaves an error $\tfrac12\Gamma S^2((\Delta S/S)^2 - \sigma^2\Delta t)$, which has mean zero and standard deviation of order $\Gamma S^2\sigma^2\Delta t$.
Summing $N$ independent errors gives a total of order $1/\sqrt{N}$; the standard approximation is $\sqrt{\pi/4}\,\sigma\,\text{vega}/\sqrt{N}$.
A 40,000-path simulation gives:

| Rebalances $N$ | Simulated s.d. | $\sqrt{\pi/4}\,\sigma\,\text{vega}/\sqrt{N}$ |
| ---: | ---: | ---: |
| 21 | 1.48 | 1.54 |
| 84 | 0.75 | 0.77 |
| 252 | 0.44 | 0.44 |

The mean P&L is zero within noise; quadrupling the hedge frequency only halves the error, so option desks hedge on thresholds rather than on a clock.

## Pitfalls

- Treating $\Delta$ as varying during $dt$ in the derivation; the self-financing argument holds $\Delta$ fixed over each step, which is why $d\Pi$ has no $S\,d\Delta$ term.
- Saying the hedged portfolio is riskless forever; it is instantaneously riskless and must be rebalanced continuously.
- Writing the PDE with $\mu$ in the $V_S$ term; after hedging the coefficient is $r$.
- Confusing $N(d_2)$ (risk-neutral exercise probability) with the real-world probability, or $N(d_1)$ with an exercise probability under $Q$.
- Using $\sigma$ as the annual volatility with $T$ in days; units must match.
- Believing the smile means Black-Scholes is useless; the formula is a map from price to implied volatility, and hedging with implied volatility still works if realised volatility is close.
- Forgetting that the PDE derivation needs $V \in C^{1,2}$; at expiry the payoff kink makes gamma explode, which is where discrete-hedging error concentrates.

## Interview questions

> [!question]- sc-bs-pde | Write the Black-Scholes PDE and its terminal condition.
> $V_t + \tfrac12\sigma^2S^2V_{SS} + rSV_S - rV = 0$ with $V(T, S) = \text{payoff}(S)$.

> [!question]- sc-bs-hedge-ratio | In the hedging derivation, how many shares do you short and why is the result riskless?
> $\Delta = \partial V/\partial S$. Ito gives $dV$ a $dW$ coefficient $\sigma SV_S$, which the short $\Delta$ shares cancel exactly over $dt$.

> [!question]- sc-bs-no-mu | Where does $\mu$ go in the delta-hedging derivation?
> It cancels: $V$ has drift term $\mu SV_S$ and the short stock has $-\Delta\mu S = -\mu SV_S$. What remains is priced by no arbitrage at $r$.

> [!question]- sc-bs-call-formula | State the Black-Scholes call price.
> $C = S_0N(d_1) - Ke^{-rT}N(d_2)$, $d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}$, $d_2 = d_1 - \sigma\sqrt{T}$.

> [!question]- sc-bs-expectation-stock-leg | How do you compute $E^Q[S_T\mathbf{1}_{S_T > K}]$ in the derivation?
> $S_0e^{rT}N(d_1)$. Complete the square: $e^{\sigma\sqrt{T}z - \sigma^2T/2}\varphi(z) = \varphi(z - \sigma\sqrt{T})$, shifting the threshold from $-d_2$ to $-d_1$. Equivalently use the stock as numeraire.

> [!question]- sc-bs-nd2-meaning | What do $N(d_1)$ and $N(d_2)$ mean?
> $N(d_2)$ is the risk-neutral probability of exercise; $N(d_1)$ is the call delta and the exercise probability under the share measure.

> [!question]- sc-bs-heat-equation | Which substitution turns the Black-Scholes PDE into the heat equation?
> $\tau = T - t$, $x = \ln S + (r - \sigma^2/2)\tau$, $V = e^{-r\tau}u$. Then $u_\tau = \tfrac12\sigma^2u_{xx}$ with $u(x, 0) = \text{payoff}(e^x)$.

> [!question]- sc-bs-greeks-identity | Express the Black-Scholes PDE in Greeks, and what does it say for a delta-hedged position at $r = 0$?
> $\Theta + \tfrac12\sigma^2S^2\Gamma + rS\Delta = rV$. At $r = 0$, $\Theta = -\tfrac12\sigma^2S^2\Gamma$: long gamma pays theta at exactly the rate that breaks even when realised equals implied volatility.

> [!question]- sc-bs-hedged-pnl | What is the instantaneous P&L of a delta-hedged long option bought at implied vol $\sigma_i$ when realised vol is $\sigma_r$?
> $\tfrac12\Gamma S^2(\sigma_r^2 - \sigma_i^2)\,dt$ (at $r = 0$). Gamma gains $\tfrac12\Gamma(dS)^2$ and theta costs $\tfrac12\Gamma S^2\sigma_i^2\,dt$.

> [!question]- sc-bs-atm-approx | Quick approximation for an at-the-money-forward option price?
> $C \approx 0.4\,\sigma S_0\sqrt{T}$ (precisely $\sigma S_0\sqrt{T}/\sqrt{2\pi}$). With $\sigma = 20\%$, $T = 1$, $S_0 = 100$: about 8; exact 7.97.

> [!question]- sc-bs-power-solutions | Which $S^p$ solve the Black-Scholes PDE?
> $p = 1$ and $p = -2r/\sigma^2$, the roots of $\tfrac12\sigma^2p(p-1) + rp - r = 0$.

> [!question]- sc-bs-assumptions-fail | Name the Black-Scholes assumptions that fail most in practice and the symptom of each.
> Constant volatility (smile and skew), continuous paths (jumps, rich OTM puts), continuous costless hedging (discrete-hedging error and transaction costs), constant rates and free borrowing (funding and borrow costs).

> [!question]- sc-bs-discrete-hedge-error | How does delta-hedging error scale with the number of rebalances $N$?
> Like $1/\sqrt{N}$: standard deviation about $\sqrt{\pi/4}\,\sigma\,\text{vega}/\sqrt{N}$. Each step contributes an independent mean-zero gamma error of size $O(\Delta t)$.

> [!question]- sc-bs-put-call-parity | Derive the Black-Scholes put from the call.
> $P = Ke^{-rT}N(-d_2) - S_0N(-d_1)$. Parity $C - P = S_0 - Ke^{-rT}$ and $1 - N(x) = N(-x)$.

## Further reading

- F. Black and M. Scholes, "The Pricing of Options and Corporate Liabilities", *Journal of Political Economy* 81 (1973).
- R. Merton, "Theory of Rational Option Pricing", *Bell Journal of Economics and Management Science* 4 (1973).
- Steven Shreve, *Stochastic Calculus for Finance II: Continuous-Time Models*, sections 4.5 (PDE by hedging) and 5.2 (risk-neutral derivation).
- John Hull, *Options, Futures, and Other Derivatives*, the Black-Scholes-Merton chapter.
- H. Leland, "Option Pricing and Replication with Transactions Costs", *Journal of Finance* 40 (1985).
