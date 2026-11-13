---
type: concept
track: [quant-trader, quant-research, quant-dev, quant-risk]
tier: core
status: solid
prereqs: [ito-integral-and-ito-lemma, risk-neutral-pricing-and-ftap]
est_hours: 4
sources: [Black and Scholes - The Pricing of Options and Corporate Liabilities (Journal of Political Economy 1973), Merton - Theory of Rational Option Pricing (Bell Journal of Economics and Management Science 1973), Shreve - Stochastic Calculus for Finance II (Springer 2004) chapters 4 and 5, Hull - Options Futures and Other Derivatives, Leland - Option Pricing and Replication with Transactions Costs (Journal of Finance 1985), Kamal - When You Cannot Hedge Continuously - The Corrections to Black-Scholes (Goldman Sachs Quantitative Strategies Research Notes 1998)]
---

# Black-Scholes Derivation

## TL;DR

- Replicate the option with $\Delta = V_S$ shares and cash in a self-financing portfolio (equivalently, hold the option short $V_S$ shares); Ito's lemma shows the $dW$ terms cancel, so the position is riskless and must earn $r$, which gives $V_t + \tfrac12\sigma^2S^2V_{SS} + rSV_S - rV = 0$.
- Terminal condition $V(T, S) = \text{payoff}(S)$; at $S = 0$ the PDE reduces to $V_t = rV$, so a call has $V(t, 0) = 0$ and $V \sim S - Ke^{-r(T - t)}$ as $S \to \infty$, a put $V(t, 0) = Ke^{-r(T - t)}$ and $V \to 0$.
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

Now build a replicating portfolio: hold $\Delta_t$ shares and put the rest of its value $X_t$ in the bank.
Self-financing means no money enters or leaves after time 0, so every change in value comes from the shares and from interest:

$$
dX = \Delta\,dS + r(X - \Delta S)\,dt = \big(rX + (\mu - r)\Delta S\big)dt + \sigma\Delta S\,dW.
$$

Require $X_t = V(t, S_t)$ for every $t$ (Shreve II, section 4.5) and match the two differentials.
The $dW$ terms give $\Delta = V_S$.
The $dt$ terms give $V_t + \mu SV_S + \tfrac12\sigma^2S^2V_{SS} = rV + (\mu - r)SV_S$, in which the $\mu SV_S$ terms cancel:

$$
V_t + \tfrac12\sigma^2S^2V_{SS} + rSV_S - rV = 0, \qquad V(T, S) = \text{payoff}(S).
$$

The classical shortcut gives the same equation.
Hold the option short $\Delta$ shares, $\Pi = V - \Delta S$, and count its gains over $dt$ as $d\Pi = dV - \Delta\,dS$: rebalancing trades happen at market prices, so they move value between shares and cash without creating any, and there is no $S\,d\Delta$ term.
Then

$$
d\Pi = \Big(V_t + \mu SV_S + \tfrac12\sigma^2S^2V_{SS} - \Delta\mu S\Big)dt + \sigma S(V_S - \Delta)\,dW.
$$

Choosing $\Delta = V_S$ kills the $dW$ term, and the $\mu$ terms cancel with it.
The position is now riskless over $dt$, so no arbitrage forces $d\Pi = r\Pi\,dt = r(V - SV_S)\,dt$, and equating drifts gives the PDE above.

The PDE is linear, so it prices any European payoff; only the terminal and boundary conditions change.
Two quick solution checks: $V = S$ (the stock) and $V = Ke^{-r(T - t)}$ (a bond) both satisfy it.

### Boundary conditions

The terminal condition alone fixes the price among solutions of at most polynomial growth in $S$ (the Feynman-Kac uniqueness class), but a numerical solver on a truncated grid $[S_{\min}, S_{\max}]$ also needs values at the edges.

| Contract | $S \to 0$ | $S \to \infty$ |
| :--- | :--- | :--- |
| Call | $V(t, 0) = 0$ | $V(t, S) - \big(S - Ke^{-r(T - t)}\big) \to 0$, so $V_S \to 1$ |
| Put | $V(t, 0) = Ke^{-r(T - t)}$ | $V(t, S) \to 0$ |

At $S = 0$ the coefficients $\tfrac12\sigma^2S^2$ and $rS$ vanish, so the PDE itself reduces to $V_t = rV$ and $V(t, 0) = \text{payoff}(0)\,e^{-r(T - t)}$: the boundary value is the discounted payoff of a stock stuck at 0, not a free choice.
For large $S$ the call is exercised with probability close to 1 and is worth the forward $S - Ke^{-r(T - t)}$; note the discounted strike, not $K$.
The script solves the PDE by Crank-Nicolson on $[0, 150]$ with exactly these conditions and recovers the closed-form call and put below to three decimals.
The upper edge is close enough to $S_0 = 100$ that its value matters: imposing $S - K$ there instead of $S - Ke^{-r(T - t)}$ lowers the call by $0.014$, well outside that tolerance.

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
| Constant $\sigma$ | Volatility is stochastic | Implied volatility differs by strike and maturity (smile and skew); one $\sigma$ cannot fit all strikes |
| Continuous paths | Jumps and gaps | Unhedgeable gap risk, and a skew that a diffusion with one $\sigma$ cannot produce (see [Jump Processes](08-Jump-Processes-and-Levy-Models.md)) |
| Continuous hedging | Discrete rebalancing | Hedging error with standard deviation about $\sqrt{\pi/4}\,\sigma\,\text{vega}/\sqrt{N}$ for $N$ rebalances (Kamal 1998) |
| No transaction costs | Spreads and impact | Leland: replicate with a volatility adjusted by a term in $k/(\sigma\sqrt{\Delta t})$ for proportional cost $k$; trade off hedge frequency against cost |
| Constant $r$, free borrowing | Stochastic rates, borrow fees, funding spreads | Matters for long-dated options and hard-to-borrow names |
| No dividends | Discrete dividends | Adjust the forward; early exercise of American calls |

Despite this, the formula survives as a map between prices and implied volatilities, and the smile records everything the model misses.

## Worked examples

### Numerical price with a Monte Carlo check

"Price a call with $S_0 = 100$, $K = 105$, $T = 0.5$, $r = 5\%$, $\sigma = 25\%$."
$\sigma\sqrt{T} = 0.1768$ and $\ln(100/105) = -0.0488$.
$d_1 = \frac{-0.0488 + (0.05 + 0.03125)(0.5)}{0.1768} = -0.0462$ and $d_2 = -0.2230$.
$N(d_1) = 0.4816$, $N(d_2) = 0.4118$, so $C = 48.16 - 105e^{-0.025}(0.4118) = 5.99$.
Parity gives the put: $5.99 - 100 + 105e^{-0.025} = 8.40$.

The script [`code/stoch_07_black_scholes.py`](code/stoch_07_black_scholes.py) reproduces $5.9885$ four ways: the closed form, quadrature of the payoff against the lognormal density, a $4 \times 10^6$-path simulation (within four standard errors), and a Crank-Nicolson solution of the PDE with the boundary conditions above.
A central finite-difference check of the PDE at $t = 0.1$, $S = 100$ gives a residual below $10^{-6}$, which is finite-difference noise.

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
Summing $N$ independent errors gives a total of order $1/\sqrt{N}$; Kamal's approximation (Goldman Sachs, 1998) is $\sqrt{\pi/4}\,\sigma\,\text{vega}/\sqrt{N}$, with vega $= S_0\varphi(d_1)\sqrt{T} = 39.70$ per unit of volatility here.
A 40,000-path simulation of the self-financing hedge (seed in the script) gives:

| Rebalances $N$ | Simulated s.d. | $\sqrt{\pi/4}\,\sigma\,\text{vega}/\sqrt{N}$ |
| ---: | ---: | ---: |
| 21 | 1.48 | 1.54 |
| 84 | 0.75 | 0.77 |
| 252 | 0.44 | 0.44 |

The mean P&L is zero within four standard errors, and the simulated standard deviation sits slightly below the approximation and closes on it as $N$ grows.
The exact standard deviations of this discrete hedge, by quadrature over its orthogonal per-step errors, also round to 1.48, 0.75 and 0.44, and the simulation matches them within four standard errors.
Quadrupling the hedge frequency only roughly halves the error: the approximation's ratio is exactly $\sqrt{84/21} = 2$, the exact ratio is 1.96, and this seed's simulated ratio is 1.98.
That square-root law is the argument for spending rebalances where gamma is large (hedging on moves or bands) rather than on a fixed clock.

## Pitfalls

- Writing $d\Pi = dV - \Delta\,dS - S\,d\Delta$; self-financing means rebalancing at market prices creates no value, so the gains are $dV - \Delta\,dS$ (plus interest on the cash, in the replication version).
- Saying the hedged portfolio is riskless forever; it is instantaneously riskless and must be rebalanced continuously.
- Writing the PDE with $\mu$ in the $V_S$ term; after hedging the coefficient is $r$.
- Confusing $N(d_2)$ (risk-neutral exercise probability) with the real-world probability, or $N(d_1)$ with an exercise probability under $Q$.
- Using $\sigma$ as the annual volatility with $T$ in days; units must match.
- Believing the smile means Black-Scholes is useless; the formula is a map from price to implied volatility, and hedging with implied volatility still works if realised volatility is close.
- Forgetting that the PDE derivation needs $V \in C^{1,2}$; at expiry the payoff kink makes gamma explode, which is where discrete-hedging error concentrates.
- Using $S - K$ instead of $S - Ke^{-r(T - t)}$ as the call's upper boundary in a PDE solver, or a non-zero call value at $S = 0$.

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

> [!question]- sc-bs-boundary-conditions | What boundary conditions go with the Black-Scholes PDE for a European call and put, and why is $V(t, 0)$ not a free choice?
> Call: $V(T, S) = (S - K)^+$, $V(t, 0) = 0$, $V \sim S - Ke^{-r(T-t)}$ as $S \to \infty$.
> Put: $V(T, S) = (K - S)^+$, $V(t, 0) = Ke^{-r(T-t)}$, $V \to 0$ as $S \to \infty$.
> At $S = 0$ the $S^2V_{SS}$ and $SV_S$ terms vanish, so the PDE becomes $V_t = rV$ and forces $V(t, 0) = \text{payoff}(0)e^{-r(T-t)}$.

> [!question]- sc-bs-self-financing | In the replication derivation, what does self-financing mean, and what equation does it give?
> No cash is added or withdrawn after time 0, so the portfolio of $\Delta$ shares and cash evolves as $dX = \Delta\,dS + r(X - \Delta S)\,dt$.
> Matching $dX$ to $dV$ from Ito's lemma gives $\Delta = V_S$ from the $dW$ terms and the Black-Scholes PDE from the $dt$ terms; the $\mu$ terms cancel.

## In this repo and The-Distinguished-Engineer

- Code: [`code/stoch_07_black_scholes.py`](code/stoch_07_black_scholes.py) prints and asserts every number on this page: the call and put by closed form, quadrature, simulation and a Crank-Nicolson PDE solve with the stated boundary conditions, the PDE, heat-equation substitution and Greeks identity by finite differences, the power solutions by polynomial roots, and the discrete-hedging table by simulating the self-financing hedge against its exact standard deviation by quadrature and the rule of Kamal (1998).
- Related notes: [Risk-Neutral Pricing and the FTAP](04-Risk-Neutral-Pricing-and-FTAP.md), [Feynman-Kac and Pricing PDEs](06-Feynman-Kac-and-Pricing-PDEs.md), [Delta Hedging and Gamma Scalping](../05-Derivatives-and-Volatility/06-Delta-Hedging-and-Gamma-Scalping.md), [Finite Differences and Fourier Pricing](../05-Derivatives-and-Volatility/11-Finite-Differences-and-Fourier-Pricing.md).

## Further reading

- F. Black and M. Scholes, "The Pricing of Options and Corporate Liabilities", *Journal of Political Economy* 81(3) (1973), 637-654.
- R. Merton, "Theory of Rational Option Pricing", *Bell Journal of Economics and Management Science* 4(1) (1973), 141-183.
- Steven Shreve, *Stochastic Calculus for Finance II: Continuous-Time Models*, sections 4.5 (PDE by hedging) and 5.2 (risk-neutral derivation).
- John Hull, *Options, Futures, and Other Derivatives*, the Black-Scholes-Merton chapter.
- H. Leland, "Option Pricing and Replication with Transactions Costs", *Journal of Finance* 40(5) (1985), 1283-1301.
- M. Kamal, "When You Cannot Hedge Continuously: The Corrections to Black-Scholes", Goldman Sachs Quantitative Strategies Research Notes (1998), equation (1) for $\sigma_{P\&L} \approx \sqrt{\pi/4}\,\sigma\kappa/\sqrt{N}$; [PDF](https://emanuelderman.com/wp-content/uploads/1998/12/risk-non_continuous_hedge.pdf) hosted by Emanuel Derman.
