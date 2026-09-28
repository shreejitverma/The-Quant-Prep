---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [option-payoffs-and-put-call-parity]
est_hours: 3
sources: [Steven Shreve - Stochastic Calculus for Finance I - The Binomial Asset Pricing Model, John Hull - Options Futures and Other Derivatives (binomial trees chapters), Cox Ross and Rubinstein (1979) - Option pricing - a simplified approach - Journal of Financial Economics 7(3), Leisen and Reimer (1996) - Binomial models for option valuation - examining and improving convergence - Applied Mathematical Finance 3(4), Broadie and Detemple (1996) - American option valuation - Review of Financial Studies 9(4)]
---

# Binomial Trees

## TL;DR

- One step, gross riskless return $R$: replicate with $\Delta = (V_u - V_d)/(S_u - S_d)$ shares and a bond; the price is $V = [pV_u + (1-p)V_d]/R$ with $p = (R - d)/(u - d)$.
- $p$ is a risk-neutral probability, not a forecast: the real-world probability of an up move never enters, and no arbitrage requires $d < R < u$.
- CRR: $u = e^{\sigma\sqrt{\Delta t}}$, $d = 1/u$, $p = (e^{(r-q)\Delta t} - d)/(u - d)$; as $N \to \infty$ prices converge to Black-Scholes with $O(1/N)$ error that oscillates between odd and even $N$.
- American options: at every node take $\max(\text{continuation}, \text{exercise})$; the set of nodes where exercise wins traces the early-exercise boundary.
- Trees are still the desk workhorse for single-stock American options with discrete dividends; delta and gamma come straight from the first two time steps.

## Learning objectives

- Price European and American options on a binomial tree by backward induction.
- Derive the risk-neutral probability and the replicating portfolio.
- Choose tree parameters (CRR) and explain convergence to Black-Scholes.

## Core concepts

### One-period replication

The stock is $S$ today and moves to $uS$ or $dS$; a bond grows by $R$ (for continuous rate $r$ over $\Delta t$, $R = e^{r\Delta t}$).
Find $\Delta$ shares and $B$ in bonds that match the option in both states:

$$
\Delta\, uS + BR = V_u, \qquad \Delta\, dS + BR = V_d.
$$

Subtracting gives the hedge ratio, and back-substituting gives the bond:

$$
\Delta = \frac{V_u - V_d}{(u - d)S}, \qquad B = \frac{uV_d - dV_u}{(u - d)R}.
$$

The option must cost what the replicating portfolio costs, $V = \Delta S + B$, which rearranges to

$$
V = \frac{pV_u + (1 - p)V_d}{R}, \qquad p = \frac{R - d}{u - d}.
$$

Interview points:

- $p \in (0, 1)$ if and only if $d < R < u$; otherwise the stock dominates the bond or vice versa and there is an arbitrage.
- Under $p$ the stock earns the riskless rate: $p\,uS + (1 - p)\,dS = RS$.
  That is why $p$ is called risk-neutral: prices are discounted expectations under the measure that makes discounted prices martingales.
- The real probability of an up move is irrelevant because the option is redundant: its risk is fully hedged by $\Delta$ shares.
- $\Delta$ is the discrete delta; its change across nodes is the discrete gamma.

### Multi-period trees and backward induction

With $N$ steps of length $\Delta t = T/N$, the terminal nodes are $S u^{N-j} d^{j}$, $j = 0, \dots, N$.
Set terminal values to the payoff and roll back one step at a time:

$$
V_{i,j} = e^{-r\Delta t}\left[pV_{i+1,j} + (1 - p)V_{i+1,j+1}\right].
$$

For a European option this collapses to a binomial sum:

$$
V_0 = e^{-rT}\sum_{j=0}^{N}\binom{N}{j}p^{N-j}(1-p)^{j}\,\text{payoff}\left(S u^{N-j}d^{j}\right).
$$

For an American option replace each node value with $\max(V_{i,j}, \text{intrinsic}_{i,j})$ during the roll-back.
The replicating portfolio is rebalanced at every node, which is the discrete version of delta hedging.

### Choosing parameters: CRR and alternatives

Cox, Ross and Rubinstein match the local variance of log returns with a recombining tree:

$$
u = e^{\sigma\sqrt{\Delta t}}, \quad d = e^{-\sigma\sqrt{\Delta t}}, \quad p = \frac{e^{(r-q)\Delta t} - d}{u - d} \approx \frac12 + \frac{(r - q - \sigma^2/2)\sqrt{\Delta t}}{2\sigma}.
$$

- Recombination ($ud = 1$) gives $N + 1$ terminal nodes and $O(N^2)$ work instead of $2^N$.
- Jarrow-Rudd instead sets $p = 1/2$ and puts the drift in $u$ and $d$; both converge to the same limit.
- By the central limit theorem the log terminal price under $p$ tends to a normal with mean $(r - q - \sigma^2/2)T$ and variance $\sigma^2 T$, which is exactly the Black-Scholes risk-neutral distribution, so tree prices converge to Black-Scholes.
- Convergence is $O(1/N)$ but not monotone: the error oscillates with the position of the strike between terminal nodes, and flips sign between odd and even $N$.
- Fixes: average $N$ and $N + 1$; Leisen-Reimer trees (strike-centred, $O(1/N^2)$ for Europeans); replace the last step with Black-Scholes values and apply Richardson extrapolation (the Broadie-Detemple "BBSR" method).
- Need $p \in (0,1)$, which fails if $\Delta t$ is large relative to $\sigma^2/(r - q)^2$; use enough steps.

### Greeks from the tree

- Delta: $(V_{1,0} - V_{1,1})/(S_{1,0} - S_{1,1})$ at the first step.
- Gamma: the change in the two step-2 deltas divided by half the spread of step-2 stock prices.
- Theta: $(V_{2,1} - V_{0,0})/(2\Delta t)$, since the middle step-2 node has the same stock price as today in CRR.
- Vega and rho: bump and reprice with the same $N$ to keep the oscillation error from polluting the difference.

### Dividends

A continuous yield just uses $e^{(r-q)\Delta t}$ in $p$.
A discrete cash dividend breaks recombination if subtracted at nodes; the standard fix is to build the tree on $S - PV(\text{future dividends})$ and add the PV back at each node, which keeps the tree recombining and lets you price the early exercise of calls just before ex-dates.

## Worked examples

### Example 1: one step, replication by hand

$S = 100$, $u = 1.2$, $d = 0.8$, $K = 100$ call, rates zero.
Payoffs: $V_u = 20$, $V_d = 0$.
$\Delta = 20/40 = 0.5$ shares; bond $B = -0.5 \times 80 = -40$ (borrow 40).
Price $= 0.5 \times 100 - 40 = 10$, matching $p = (1 - 0.8)/0.4 = 0.5$ and $0.5 \times 20 = 10$.

With a 5% per-period rate ($R = 1.05$): $p = (1.05 - 0.8)/0.4 = 0.625$ and $V = 0.625 \times 20/1.05 = 11.90$.
The delta is still 0.5; only the financing changes, so $V = 50 - 40/1.05 = 11.90$.
Interview narration: "higher rates make calls worth more because the hedge borrows less in present-value terms".

### Example 2: two-step American put

$S = K = 100$, $u = 1.1$, $d = 1/1.1$, per-step $R = 1.02$, so $p = (1.02 - 0.9091)/(1.1 - 0.9091) = 0.5810$.

Terminal stock prices 121, 100, 82.64 give put payoffs 0, 0, 17.36.

| Node | Stock | Continuation | Exercise | American value |
| :--- | ---: | ---: | ---: | ---: |
| up | 110.00 | 0.00 | 0.00 | 0.00 |
| down | 90.91 | $0.4190 \times 17.36/1.02 = 7.13$ | 9.09 | 9.09 (exercise) |
| root | 100.00 | $0.4190 \times 9.09/1.02 = 3.73$ | 0.00 | 3.73 |

European put: $0.4190 \times 7.13/1.02 = 2.93$.
Early-exercise premium: $3.73 - 2.93 = 0.81$.
Root hedge for the European put: $\Delta = (0 - 7.13)/(110 - 90.91) = -0.373$ and a bond position of $2.93 + 0.373 \times 100 = 40.28$ lent.
Check the up state: $-0.373 \times 110 + 40.28 \times 1.02 = 0$.

### Example 3: CRR convergence to Black-Scholes

$S = K = 100$, $T = 1$, $r = 5\%$, $\sigma = 20\%$, no dividends.
Black-Scholes call: 10.4506.

| $N$ | CRR call | Error |
| ---: | ---: | ---: |
| 1 | 12.1623 | +1.7117 |
| 2 | 9.5405 | $-0.9101$ |
| 5 | 10.8059 | +0.3554 |
| 10 | 10.2534 | $-0.1972$ |
| 50 | 10.4107 | $-0.0399$ |
| 51 | 10.4850 | +0.0344 |
| 100 | 10.4306 | $-0.0200$ |
| 101 | 10.4680 | +0.0174 |
| 1000 | 10.4486 | $-0.0020$ |

The even-$N$ error halves when $N$ doubles ($O(1/N)$), and the sign alternates between odd and even.
Averaging $N = 100$ and $N = 101$ gives 10.4493, better than $N = 1000$ alone.
For $N = 1$: $u = e^{0.2} = 1.2214$, $d = 0.8187$, $p = 0.5775$.

### Example 4: value of early exercise

Same inputs, puts.
Black-Scholes European put: 5.5735.
CRR American put: 6.0824 at $N = 100$, 6.0888 at $N = 500$, 6.0900 at $N = 2000$.
The early-exercise premium is about 0.52, roughly 9% of the option value, which is why pricing an American put with Black-Scholes is a real error at 5% rates.

```python
from math import exp, sqrt

def crr(S, K, T, r, sigma, N, call=True, american=False, q=0.0):
    dt = T / N
    u = exp(sigma * sqrt(dt)); d = 1 / u
    p = (exp((r - q) * dt) - d) / (u - d)
    disc = exp(-r * dt)
    payoff = (lambda s: max(s - K, 0.0)) if call else (lambda s: max(K - s, 0.0))
    V = [payoff(S * u ** (N - j) * d ** j) for j in range(N + 1)]
    for i in range(N - 1, -1, -1):
        V = [disc * (p * V[j] + (1 - p) * V[j + 1]) for j in range(i + 1)]
        if american:
            V = [max(V[j], payoff(S * u ** (i - j) * d ** j)) for j in range(i + 1)]
    return V[0]

print(crr(100, 100, 1, 0.05, 0.2, 100))                              # 10.4306
print(crr(100, 100, 1, 0.05, 0.2, 500, call=False, american=True))   # 6.0888
```

## Pitfalls

- Saying $p$ is the probability the stock goes up; it is the probability that makes the stock earn the riskless rate.
- Forgetting the no-arbitrage condition $d < R < u$, which also bounds how coarse a tree can be for high rates or low volatility.
- Reporting a single $N$ price as converged; always look at $N$ and $N + 1$ or use a smoothed tree.
- Computing vega by bumping $\sigma$ with a different node layout; the strike moves relative to the nodes and the finite difference is dominated by oscillation noise.
- Checking early exercise only at expiry or only at the root; it must be checked at every node.
- Subtracting cash dividends at nodes naively, which destroys recombination and blows up the node count.
- Believing binomial American call and put values differ from Europeans only for puts: calls on dividend payers also carry an early-exercise premium.

## Interview questions

> [!question]- deriv-binomial-risk-neutral-prob | Derive the risk-neutral probability in a one-step tree with up factor $u$, down factor $d$ and gross riskless return $R$.
> $p = (R - d)/(u - d)$.
> Replicate the option with $\Delta = (V_u - V_d)/((u-d)S)$ shares and a bond; the portfolio cost rearranges to $[pV_u + (1-p)V_d]/R$, and $p$ is the probability under which the stock grows at $R$.

> [!question]- deriv-binomial-no-arb-condition | What condition on $u$, $d$ and $R$ rules out arbitrage in a one-step tree?
> $d < R < u$.
> If $R \le d$ the stock beats the bond in every state (borrow and buy stock); if $R \ge u$ the bond dominates (short stock, lend); equivalently $p \in (0, 1)$.

> [!question]- deriv-binomial-real-prob-irrelevant | Why does the real-world probability of an up move not affect the option price?
> Because the option is replicated exactly by shares and bonds, so its price is the cost of that portfolio.
> Any preference or view about the up probability is already in the stock price.

> [!question]- deriv-binomial-one-step-call | $S = 100$, up 120, down 80, $K = 100$ call, zero rates. Price and hedge?
> Price 10; hedge 0.5 shares and borrow 40.
> $\Delta = (20 - 0)/(120 - 80) = 0.5$, and $p = 0.5$ gives $0.5 \times 20 = 10$.

> [!question]- deriv-binomial-two-step-american-put | $S = K = 100$, $u = 1.1$, $d = 1/1.1$, per-step $R = 1.02$, two steps. Price the European and American puts.
> European 2.93, American 3.73.
> $p = 0.581$; at the down node continuation is 7.13 but exercise gives 9.09, so the American exercises there; rolling back gives $0.419 \times 9.09/1.02 = 3.73$ versus $0.419 \times 7.13/1.02 = 2.93$.

> [!question]- deriv-crr-parameters | What are the CRR tree parameters?
> $u = e^{\sigma\sqrt{\Delta t}}$, $d = 1/u$, $p = (e^{(r-q)\Delta t} - d)/(u - d)$.
> They match the variance of log returns per step and make the tree recombine, so $N$ steps need only $N+1$ terminal nodes.

> [!question]- deriv-binomial-convergence-rate | How fast does a CRR tree converge to Black-Scholes, and what does the error look like?
> $O(1/N)$, oscillating in sign between odd and even $N$.
> The strike sits at a different place relative to terminal nodes as $N$ changes; averaging $N$ and $N+1$, Leisen-Reimer trees, or Black-Scholes smoothing with Richardson extrapolation fix it.

> [!question]- deriv-binomial-why-converges | Why does the binomial price converge to the Black-Scholes price?
> The log terminal price is a sum of $N$ i.i.d. steps with mean $(r - q - \sigma^2/2)\Delta t$ and variance $\sigma^2\Delta t$ per step under $p$, so by the CLT it tends to the lognormal risk-neutral distribution.
> Discounted expectations of the payoff then converge to the Black-Scholes integral.

> [!question]- deriv-binomial-american-rule | How do you price an American option on a tree?
> Roll back as for a European, but at every node replace the value with $\max(\text{discounted continuation}, \text{intrinsic})$.
> Nodes where intrinsic wins form the early-exercise region; its edge approximates the exercise boundary.

> [!question]- deriv-binomial-tree-greeks | How do you read delta, gamma and theta off a CRR tree?
> Delta from the two step-1 nodes; gamma from the change of the two step-2 deltas over half the step-2 spot range; theta from $(V_{2,\text{mid}} - V_0)/(2\Delta t)$.
> In CRR the middle step-2 node has the same spot as today, so that difference is pure time decay.

> [!question]- deriv-american-put-premium-size | For $S = K = 100$, $T = 1$, $r = 5\%$, $\sigma = 20\%$, roughly how large is the American put's early-exercise premium?
> About 0.52: the American put is about 6.09 versus 5.57 European.
> Computed with a 2000-step CRR tree; the premium grows with rates and moneyness.

> [!question]- deriv-binomial-discrete-dividends | How do you handle discrete cash dividends in a tree without losing recombination?
> Build the tree on $S - PV(\text{remaining dividends})$ with that process's volatility, and add back the PV of dividends not yet paid at each node.
> Subtracting dividends from node prices directly makes up-then-down differ from down-then-up.

## In this repo and SDE-Interview-Prep

- Prev: [Option Payoffs and Put-Call Parity](02-Option-Payoffs-and-Put-Call-Parity.md). Next: [Black-Scholes Formula and Intuition](04-Black-Scholes-Formula-and-Intuition.md).
- The continuous-time limit: [Risk-Neutral Pricing and FTAP](../04-Stochastic-Calculus/04-Risk-Neutral-Pricing-and-FTAP.md) and [Black-Scholes Derivation](../04-Stochastic-Calculus/07-Black-Scholes-Derivation.md).
- Lattice methods in general: [Finite Differences and Fourier Pricing](11-Finite-Differences-and-Fourier-Pricing.md).

## Further reading

- Steven Shreve, *Stochastic Calculus for Finance I: The Binomial Asset Pricing Model*, chapters 1-4.
- John Hull, *Options, Futures, and Other Derivatives*, chapters on binomial trees and numerical procedures.
- J. C. Cox, S. A. Ross and M. Rubinstein (1979), "Option pricing: a simplified approach", *Journal of Financial Economics* 7(3).
- D. Leisen and M. Reimer (1996), "Binomial models for option valuation - examining and improving convergence", *Applied Mathematical Finance* 3(4).
- M. Broadie and J. Detemple (1996), "American option valuation: new bounds, approximations, and a comparison of existing methods", *Review of Financial Studies* 9(4).
