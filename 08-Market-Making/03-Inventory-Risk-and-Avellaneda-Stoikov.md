---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [market-making-fundamentals, stochastic-differential-equations]
est_hours: 5
sources: [Avellaneda and Stoikov (2008) High-frequency trading in a limit order book. Quantitative Finance 8(3) 217-224, Cartea Jaimungal and Penalva (2015) Algorithmic and High-Frequency Trading. Cambridge University Press, Gueant Lehalle and Fernandez-Tapia (2013) Dealing with the inventory risk: a solution to the market making problem. Mathematics and Financial Economics 7(4) 477-507]
---

# Inventory Risk and Avellaneda-Stoikov

## TL;DR

- Avellaneda-Stoikov (2008) is the canonical model of a risk-averse market maker: arithmetic Brownian mid, fills arriving at Poisson rate $A e^{-k\delta}$ at distance $\delta$ from the mid, CARA utility with risk aversion $\gamma$.
- The reservation price is $r = s - q\gamma\sigma^2(T-t)$: long inventory lowers the price at which you are indifferent to trading, so you quote both sides lower.
- The optimal total spread is $\gamma\sigma^2(T-t) + \frac{2}{\gamma}\ln\left(1 + \frac{\gamma}{k}\right)$, centred on $r$ and independent of inventory.
- The first term is an inventory-risk charge; the second is a market-power markup that tends to $2/k$ as $\gamma \to 0$.
- Compared with symmetric quoting at the same spread, the strategy gives up a little mean P&L for a much smaller P&L and inventory variance.

## Learning objectives

- Derive the reservation price and optimal spread in the Avellaneda-Stoikov model.
- Explain the role of risk aversion, volatility, horizon and arrival intensity.
- Simulate the strategy and compare it with symmetric quoting.

## Core concepts

### The model

- Mid price: $dS_t = \sigma \, dW_t$, arithmetic Brownian motion with no drift.
- The market maker posts a bid $p^b = S - \delta^b$ and an ask $p^a = S + \delta^a$.
- Market sell orders hit the bid at Poisson intensity $\lambda^b = A e^{-k\delta^b}$ and market buy orders lift the ask at intensity $\lambda^a = A e^{-k\delta^a}$.
  Quoting further away fills less often; $A$ sets the overall rate and $k$ how fast it decays with distance.
- Cash and inventory: each bid fill pays $p^b$ and adds one unit, each ask fill receives $p^a$ and removes one unit.
- Objective: maximise $\mathbb{E}\left[-e^{-\gamma(X_T + q_T S_T)}\right]$, CARA utility of terminal wealth, with risk aversion $\gamma > 0$.

The paper motivates the exponential intensity from a power-law distribution of market order sizes combined with a logarithmic price impact; for interviews treat it as the modelling assumption.
There is no adverse selection in the model: fills are independent of future price moves.
See [Stochastic Differential Equations](../04-Stochastic-Calculus/03-Stochastic-Differential-Equations.md) for the dynamics and [Poisson Processes](../01-Probability/13-Poisson-Processes.md) for the fill model.

### Step 1: the frozen-inventory value

Suppose you hold $q$ units and never trade again.
Terminal wealth is $x + qS_T$ with $S_T \sim N(s, \sigma^2(T-t))$.
Using the normal moment generating function $\mathbb{E}[e^{-\gamma q S_T}] = e^{-\gamma q s + \frac12 \gamma^2 q^2 \sigma^2 (T-t)}$,

$$
v(x, s, q, t) = -\exp(-\gamma x)\,\exp(-\gamma q s)\,\exp\left(\tfrac12 \gamma^2 q^2 \sigma^2 (T-t)\right).
$$

The last factor is the utility cost of carrying inventory risk; it grows with $q^2$, $\sigma^2$ and the time left.

### Step 2: reservation bid, ask and price

The reservation bid $r^b$ is the price at which you are indifferent to buying one more unit: $v(x - r^b, s, q+1, t) = v(x, s, q, t)$.
Taking logs and cancelling,

$$
\gamma r^b - \gamma s + \tfrac12\gamma^2\sigma^2(T-t)\left[(q+1)^2 - q^2\right] = 0
\quad\Rightarrow\quad
r^b = s - (1 + 2q)\frac{\gamma\sigma^2(T-t)}{2}.
$$

Similarly $v(x + r^a, s, q-1, t) = v(x, s, q, t)$ gives $r^a = s + (1 - 2q)\frac{\gamma\sigma^2(T-t)}{2}$.
Their average is the reservation (indifference) price

$$
r(s, q, t) = s - q\gamma\sigma^2(T-t),
$$

and their difference is $r^a - r^b = \gamma\sigma^2(T-t)$.
A long position ($q > 0$) pushes $r$ below the mid: you value the asset less because you already hold too much of it.

### Step 3: the optimal distances

With fills, the value function $u(s, x, q, t)$ solves the Hamilton-Jacobi-Bellman equation

$$
u_t + \tfrac12\sigma^2 u_{ss}
+ \max_{\delta^b} \lambda^b(\delta^b)\left[u(s, x - s + \delta^b, q+1, t) - u\right]
+ \max_{\delta^a} \lambda^a(\delta^a)\left[u(s, x + s + \delta^a, q-1, t) - u\right] = 0,
$$

with $u(s, x, q, T) = -e^{-\gamma(x + qs)}$.
CARA utility suggests the ansatz $u = -e^{-\gamma x} e^{-\gamma\theta(s, q, t)}$, and then the reservation prices are $r^b = \theta(s,q+1,t) - \theta(s,q,t)$ and $r^a = \theta(s,q,t) - \theta(s,q-1,t)$.
Substituting, the ask term becomes $e^{-\gamma(x + \theta)}\,\lambda^a(\delta^a)\left[1 - e^{-\gamma(s + \delta^a - r^a)}\right]$, so the ask distance maximises

$$
g(\delta) = A e^{-k\delta}\left(1 - e^{-\gamma(\delta - c)}\right), \qquad c = r^a - s.
$$

Setting $g'(\delta) = 0$ gives $-k\left(1 - e^{-\gamma(\delta - c)}\right) + \gamma e^{-\gamma(\delta - c)} = 0$, so $e^{-\gamma(\delta - c)} = \frac{k}{k + \gamma}$ and

$$
\delta^a = r^a - s + \frac{1}{\gamma}\ln\left(1 + \frac{\gamma}{k}\right), \qquad
\delta^b = s - r^b + \frac{1}{\gamma}\ln\left(1 + \frac{\gamma}{k}\right).
$$

The trade-off is visible in $g$: quoting further out earns more per fill (the bracket) but fills less often (the exponential).

### Step 4: close the approximation and combine

Avellaneda and Stoikov substitute the exponential intensity into the equation for $\theta$ and expand in powers of $q$.
To the order they keep, $\theta$ matches the frozen-inventory value, so the reservation prices are those of Step 2.
Adding the two distances,

$$
\delta^a + \delta^b = \gamma\sigma^2(T-t) + \frac{2}{\gamma}\ln\left(1 + \frac{\gamma}{k}\right),
$$

and the quotes $p^b = r^b - \frac1\gamma\ln(1+\gamma/k)$, $p^a = r^a + \frac1\gamma\ln(1+\gamma/k)$ are centred on $r = (r^a + r^b)/2$.
So the recipe is: compute $r$, then place a symmetric spread of that total width around it.

### Reading the formula

- Inventory term $\gamma\sigma^2(T-t)$: more risk aversion, more volatility or more time left all widen the market and strengthen the skew.
  It vanishes at $T$.
- Liquidity term $\frac{2}{\gamma}\ln(1 + \gamma/k)$: as $\gamma \to 0$ it tends to $2/k$, the spread of a risk-neutral monopolist who maximises $\delta A e^{-k\delta}$ on each side (optimum $\delta = 1/k$).
  Large $k$ means fill probability collapses quickly away from the mid, as in a competitive book, so the spread is tight.
- $A$ does not appear in the quotes; it only scales how often you trade.
- The spread does not depend on $q$ in this approximation; inventory only moves the centre.
  The skew is linear in $q$.
- Units: $\gamma$ is per dollar, $\sigma^2(T-t)$ is dollars squared, $k$ is per dollar.
  Re-express all three consistently when you calibrate to a real instrument.

### Limitations that interviewers probe

- The finite horizon $T$ is artificial: skew and the inventory term shrink to zero at $T$, so behaviour depends on a parameter with no economic meaning for a continuous business.
  Practitioners often freeze $T - t$ at a constant.
- No inventory bounds; the Gueant-Lehalle-Fernandez-Tapia solution adds them and gives an asymptotic spread and skew that do not depend on $T$.
  See [Gueant-Lehalle and Extensions](04-Gueant-Lehalle-and-Extensions.md).
- No adverse selection: fills are independent of future moves, which is exactly what markouts show to be false.
- Constant $\sigma$, $A$ and $k$; continuous prices with no tick size; arithmetic Brownian motion.
- Large skew can push a quote through the mid ($\delta < 0$); a real system caps the skew or switches to active hedging.

## Worked examples

All examples use the defaults of the repo simulator [avellaneda_stoikov_mm.py](code/avellaneda_stoikov_mm.py): $s = 100$, $\sigma = 2$, $\gamma = 0.1$, $k = 1.5$, $A = 140$, and $T - t = 1$ unless stated.

### Example 1: flat inventory

With $q = 0$, $r = 100$.
Inventory term: $0.1 \times 4 \times 1 = 0.4$.
Liquidity term: $20 \ln(1 + 0.1/1.5) = 20 \ln(1.0667) \approx 1.2908$.
Total spread $\approx 1.6908$, so bid $\approx 99.1546$ and ask $\approx 100.8454$.
Each side sits 0.8454 from the mid and fills at intensity $140 e^{-1.5 \times 0.8454} \approx 39.39$ per unit time.

### Example 2: long three units

With $q = 3$, $r = 100 - 3 \times 0.4 = 98.8$; the spread is unchanged at 1.6908.
Bid $\approx 97.9546$ and ask $\approx 99.6454$.
The reservation bid and ask are $r^b = 100 - 7 \times 0.2 = 98.6$ and $r^a = 100 - 5 \times 0.2 = 99.0$.
The ask is now 0.3546 below the mid, so its intensity is $140 e^{1.5 \times 0.3546} \approx 238.3$ while the bid's falls to $140 e^{-1.5 \times 2.0454} \approx 6.51$.
The market maker sells about 37 times as fast as it buys until inventory comes down.
Note that the ask has crossed the mid: in a real book this would be an aggressive order, one of the model's known artefacts.

### Example 3: the horizon effect

Hold $q = 1$ and let time run out.

| $T - t$ | $r$ | total spread |
| ---: | ---: | ---: |
| 1.0 | 99.60 | 1.6908 |
| 0.5 | 99.80 | 1.4908 |
| 0.1 | 99.96 | 1.3308 |
| 0.0 | 100.00 | 1.2908 |

Both the skew and the inventory part of the spread decay linearly to zero, leaving only the liquidity term.

### Example 4: risk aversion

At $T - t = 1$ the total spread splits as follows.

| $\gamma$ | inventory term | liquidity term | total |
| ---: | ---: | ---: | ---: |
| 0.01 | 0.04 | 1.3289 | 1.3689 |
| 0.1 | 0.4 | 1.2908 | 1.6908 |
| 1 | 4 | 1.0217 | 5.0217 |

As $\gamma \to 0$ the liquidity term tends to $2/k = 1.3333$.
Higher risk aversion shrinks the liquidity term slightly and inflates the inventory term a lot, so the market widens overall.

### Example 5: checking the first-order condition numerically

With $c = 0.3$, maximising $g(\delta) = 140 e^{-1.5\delta}(1 - e^{-0.1(\delta - 0.3)})$ on a grid or with a bounded optimiser gives $\delta \approx 0.94539$, matching $0.3 + 10\ln(1.0667) \approx 0.94539$.

### Example 6: simulation against symmetric quoting

Run the repo simulator for 1,000 paths and compare it with a strategy that uses the same spread but centres it on the mid instead of $r$.
With `np.random.seed(7)` before each batch, one run gave:

| Strategy | mean terminal P&L | sd of P&L | sd of final inventory |
| :--- | ---: | ---: | ---: |
| Avellaneda-Stoikov | 65.03 | 6.86 | 2.87 |
| Symmetric around mid | 67.73 | 13.44 | 8.16 |

The inventory strategy gives up about 4% of mean P&L to halve the P&L standard deviation, the same qualitative result as the paper's table.
Exact numbers depend on the seed.

```python
import numpy as np
from avellaneda_stoikov_mm import AvellanedaStoikovSimulator  # needs numpy and matplotlib

np.random.seed(7)
final = [AvellanedaStoikovSimulator().run()[3][-1] for _ in range(1000)]
print(np.mean(final), np.std(final, ddof=1))
```

The symmetric variant is the same loop with `bid = S[i-1] - spread/2` and `ask = S[i-1] + spread/2`.
The simulator's mid is an arithmetic random walk, matching the model, even though a comment in the file mentions geometric Brownian motion.

## Pitfalls

- Centring the spread on the mid and adding skew separately with a different scale; in the model the whole spread moves with $r$.
- Forgetting the sign: long inventory lowers both quotes.
- Believing the spread depends on inventory in the basic model; only the centre does.
- Mixing units: $\sigma$ per unit time with $T-t$ in different time units, or $\gamma$ calibrated on a different price scale.
- Treating the finite-horizon behaviour (vanishing skew near $T$) as a feature rather than an artefact.
- Using the model's no-adverse-selection spread as the real spread; real width must also cover markouts.
- Writing $r^a = s + (2q - 1)\gamma\sigma^2(T-t)/2$; the correct sign is $(1 - 2q)$.

## Interview questions

> [!question]- mm-as-reservation-price | State the Avellaneda-Stoikov reservation price and explain its sign.
> $r = s - q\gamma\sigma^2(T-t)$.
> Long inventory ($q > 0$) lowers the price at which you are indifferent to trading, because more inventory adds variance to terminal wealth and CARA utility penalises that.

> [!question]- mm-as-optimal-spread | What is the optimal total spread in Avellaneda-Stoikov?
> $\gamma\sigma^2(T-t) + \frac{2}{\gamma}\ln\left(1 + \frac{\gamma}{k}\right)$, centred on the reservation price.
> The first term is the inventory-risk charge and the second the market-power markup from the exponential fill intensity.

> [!question]- mm-as-assumptions | List the assumptions of the Avellaneda-Stoikov model.
> Arithmetic Brownian mid $dS = \sigma dW$; Poisson fills with intensity $A e^{-k\delta}$ at distance $\delta$; CARA utility $-e^{-\gamma W_T}$; finite horizon $T$; one unit per fill; no adverse selection or inventory bounds.

> [!question]- mm-as-reservation-bid-derivation | Derive the reservation bid from the frozen-inventory value function.
> $r^b = s - (1 + 2q)\gamma\sigma^2(T-t)/2$.
> Set $v(x - r^b, q+1) = v(x, q)$ with $v = -e^{-\gamma x}e^{-\gamma q s}e^{\gamma^2 q^2 \sigma^2 (T-t)/2}$; logs give $\gamma r^b - \gamma s + \frac12\gamma^2\sigma^2(T-t)(2q + 1) = 0$.

> [!question]- mm-as-risk-neutral-limit | What does the Avellaneda-Stoikov spread tend to as gamma goes to 0, and why?
> $2/k$.
> $\frac{2}{\gamma}\ln(1 + \gamma/k) \to 2/k$ and the inventory term vanishes; a risk-neutral quoter maximises $\delta A e^{-k\delta}$ per side, optimum $\delta = 1/k$.

> [!question]- mm-as-first-order-condition | With fill intensity A e^{-k delta}, what is the optimal ask distance given reservation ask r^a?
> $\delta^a = r^a - s + \frac{1}{\gamma}\ln(1 + \gamma/k)$.
> Maximise $A e^{-k\delta}(1 - e^{-\gamma(\delta - c)})$ with $c = r^a - s$; the FOC gives $e^{-\gamma(\delta - c)} = k/(k + \gamma)$.

> [!question]- mm-as-numeric-quotes | s = 100, sigma = 2, gamma = 0.1, k = 1.5, T - t = 1, q = 3. Give the quotes.
> About 97.95 bid, 99.65 ask.
> $r = 100 - 3 \times 0.4 = 98.8$ and the spread is $0.4 + 20\ln(1 + 1/15) \approx 1.691$, so quotes are $98.8 \pm 0.845$.

> [!question]- mm-as-role-of-A | Why does the base intensity A not appear in the optimal quotes?
> Because it multiplies the whole objective term for each side and cancels in the first-order condition.
> It changes how often you trade, not where you should quote.

> [!question]- mm-as-k-interpretation | What does a larger k mean, and how does it change the spread?
> Fill probability decays faster with distance from the mid, as in a competitive book, so the optimal spread is tighter.
> The liquidity term $\frac{2}{\gamma}\ln(1 + \gamma/k)$ decreases in $k$.

> [!question]- mm-as-horizon-artefact | What happens to the Avellaneda-Stoikov quotes as t approaches T, and why is it a problem?
> The skew and the inventory part of the spread shrink linearly to zero.
> Real market makers have no terminal date, so this behaviour is driven by an arbitrary parameter; GLFT or a frozen $T - t$ fix it.

> [!question]- mm-as-vs-symmetric | How does Avellaneda-Stoikov compare with symmetric quoting at the same spread?
> Slightly lower mean P&L, much lower P&L and inventory variance.
> Skewing mean-reverts inventory, trading a little expected profit for less risk; in a 1,000-path run of the repo simulator the P&L sd fell from about 13.4 to 6.9 with mean 65.0 versus 67.7.

> [!question]- mm-as-no-adverse-selection | Which real-world effect is missing from Avellaneda-Stoikov that dominates actual market-making P&L?
> Adverse selection: fills are independent of future price moves in the model.
> Real width must also cover the expected post-fill move measured by markouts.

## In this repo and SDE-Interview-Prep

- Code: [avellaneda_stoikov_mm.py](code/avellaneda_stoikov_mm.py).
- Systems companion with the same formulas: [Quantitative Models and Strategies](Quant-Dev-MM-Guide/03_Quantitative_Models_and_Strategies.md).
  Its section 1.1 writes the quotes with inventory terms $(2q - 1)$ and $(2q + 1)$ of the wrong sign.
  With $\delta^* = \frac{2}{\gamma}\ln(1 + \gamma/k)$ the quotes derived above are $p^a = s + \frac{\delta^*}{2} + (1 - 2q)\frac{\gamma\sigma^2(T-t)}{2}$ and $p^b = s - \frac{\delta^*}{2} - (1 + 2q)\frac{\gamma\sigma^2(T-t)}{2}$, which reproduce Example 2.

## Further reading

- Avellaneda and Stoikov (2008), High-frequency trading in a limit order book, *Quantitative Finance* 8(3).
- Gueant, Lehalle and Fernandez-Tapia (2013), Dealing with the inventory risk: a solution to the market making problem, *Mathematics and Financial Economics* 7(4).
- Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015), chapter on market making.
