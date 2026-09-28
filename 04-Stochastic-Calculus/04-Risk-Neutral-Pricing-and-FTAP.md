---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [stochastic-differential-equations, conditional-probability-and-bayes]
est_hours: 4
sources: [Shreve - Stochastic Calculus for Finance I (Springer 2004) chapter 1, Shreve - Stochastic Calculus for Finance II (Springer 2004) chapters 5 and 9, Harrison and Pliska - Martingales and Stochastic Integrals in the Theory of Continuous Trading (Stochastic Processes and their Applications 1981), Delbaen and Schachermayer - A General Version of the Fundamental Theorem of Asset Pricing (Mathematische Annalen 1994), Geman El Karoui and Rochet - Changes of Numeraire Changes of Probability Measure and Option Pricing (Journal of Applied Probability 1995), Breeden and Litzenberger - Prices of State-Contingent Claims Implicit in Option Prices (Journal of Business 1978)]
---

# Risk-Neutral Pricing and the FTAP

## TL;DR

- If a payoff can be replicated by a self-financing portfolio, its price is the cost of that portfolio; anything else is an arbitrage.
- First FTAP: no arbitrage (precisely, no free lunch with vanishing risk) iff there is an equivalent measure $Q$ under which discounted prices are martingales.
- Second FTAP: the market is complete (every claim replicable) iff that measure is unique; otherwise no-arbitrage only gives a price interval.
- Pricing rule with numeraire $N$: $V_0 = N_0\,E^{N}[V_T/N_T]$; with the bank account, $V_0 = E^Q[e^{-rT}V_T]$.
- The real-world drift $\mu$ never enters: hedging removes exposure to it, and changing to $Q$ changes the drift to $r$ but leaves volatility (quadratic variation) untouched.

## Learning objectives

- State the fundamental theorems of asset pricing and explain replication.
- Price by expectation under the risk-neutral measure with a chosen numeraire.
- Explain why real-world drift does not enter option prices.

## Core concepts

### Arbitrage and the law of one price

An arbitrage is a self-financing strategy with zero initial cost, non-negative terminal value almost surely, and a strictly positive terminal value with positive probability.
If two portfolios have the same payoff in every state, no-arbitrage forces them to have the same price (law of one price), and prices are linear in payoffs.
A derivative whose payoff equals a traded portfolio's payoff in every state therefore has a price fixed without any view on probabilities.

### One-period binomial model

A stock worth $S_0$ moves to $uS_0$ or $dS_0$; cash grows by $R = e^{r\Delta t}$.
No arbitrage requires $d < R < u$ (otherwise borrow cash to buy stock, or short stock into cash).
Replicate a claim paying $V_u$ or $V_d$ with $\Delta$ shares and $B$ in cash:

$$
\Delta = \frac{V_u - V_d}{(u - d)S_0}, \qquad V_0 = \Delta S_0 + B = \frac{1}{R}\big(q V_u + (1 - q)V_d\big), \qquad q = \frac{R - d}{u - d}.
$$

The real probability $p$ of the up move appears nowhere.
The weights $q, 1 - q$ are positive (by no arbitrage), sum to 1, and make the stock earn the risk-free rate on average: $q u S_0 + (1-q) d S_0 = R S_0$.
That is the risk-neutral measure: not a belief, but the unique set of weights consistent with the traded prices.
Multi-period trees (see [Binomial Trees](../05-Derivatives-and-Volatility/03-Binomial-Trees.md)) apply this one step at a time backwards.

### State prices

In a finite model, the price of the Arrow-Debreu security paying 1 in state $\omega$ is the state price $\psi_\omega$.
Any payoff is a bundle of these, so $V_0 = \sum_\omega \psi_\omega V(\omega)$.
No arbitrage is equivalent to all state prices being strictly positive, and then $Q(\omega) = \psi_\omega R$ is a probability measure with $V_0 = E^Q[V]/R$.
In continuous strike space the state price density is recovered from call prices (Breeden-Litzenberger):

$$
\frac{\partial^2 C}{\partial K^2}(K, T) = e^{-rT} q_T(K),
$$

where $q_T$ is the risk-neutral density of $S_T$; a butterfly spread with wings $\pm h$ costs about $h^2 e^{-rT}q_T(K)$.

### The fundamental theorems

- First FTAP: a market has no arbitrage iff there exists an equivalent martingale measure $Q \sim P$ under which every discounted traded price $S_t/B_t$ is a martingale.
  In finite discrete time this is exact (Harrison-Pliska, Dalang-Morton-Willinger); in continuous time "no arbitrage" is strengthened to "no free lunch with vanishing risk" (Delbaen-Schachermayer).
- Second FTAP: an arbitrage-free market is complete iff the equivalent martingale measure is unique.
  In a tree, completeness means each node has at most as many branches as there are non-redundant traded assets.

Equivalence ($Q$ and $P$ agree on which events have probability zero) is what makes the theorem economically meaningful: $Q$ can reweight scenarios but cannot invent or delete them.

### Continuous time: Black-Scholes market

Under $P$, $dS_t = \mu S_t\,dt + \sigma S_t\,dW_t$ and $dB_t = rB_t\,dt$.
Define the market price of risk $\lambda = (\mu - r)/\sigma$ and $W^Q_t = W_t + \lambda t$.
By Girsanov (see [Change of Measure and Girsanov](05-Change-of-Measure-and-Girsanov.md)), $W^Q$ is a Brownian motion under

$$
\frac{dQ}{dP}\Big|_{\mathcal{F}_T} = \exp\big(-\lambda W_T - \tfrac12\lambda^2 T\big),
$$

and $dS_t = rS_t\,dt + \sigma S_t\,dW^Q_t$, so $e^{-rt}S_t$ is a $Q$-martingale.
The self-financing hedge (martingale representation) replicates any $\mathcal{F}_T$-measurable payoff, so this $Q$ is unique and

$$
V_t = E^Q\big[e^{-r(T - t)}V_T \mid \mathcal{F}_t\big].
$$

Equivalently $V_0 = E^P[\xi_T V_T]$ with the state price deflator $\xi_T = e^{-rT}\,dQ/dP$: you can price under $P$, but only with a stochastic discount factor, never by discounting at $\mu$.

### Why $\mu$ does not enter

- Replication: the hedge ratio is set so the portfolio has no $dW$ exposure, hence no exposure to how fast the stock drifts; its value is pinned by the cost of the hedge.
- Measure change: Girsanov shifts the drift but keeps the diffusion coefficient, since quadratic variation $[\log S]_T = \sigma^2 T$ is a pathwise quantity and the same under any equivalent measure.
- Economically: a high $\mu$ comes with a high risk premium; the option price already reflects the stock price, which is where the investor's view on $\mu$ lives.

### Change of numeraire

Any strictly positive traded asset $N$ can serve as numeraire.
There is a measure $Q^N$ under which every traded price divided by $N$ is a martingale, related to $Q$ by

$$
\frac{dQ^N}{dQ} = \frac{N_T/N_0}{B_T/B_0}, \qquad V_0 = N_0\,E^{N}\Big[\frac{V_T}{N_T}\Big].
$$

| Numeraire | Measure | Typical use |
| :--- | :--- | :--- |
| Bank account $B_t = e^{rt}$ | risk-neutral $Q$ | equity and FX derivatives |
| Stock $S_t$ | share measure $Q^S$ | asset-or-nothing legs, $N(d_1)$ |
| Zero-coupon bond $P(t, T)$ | $T$-forward measure | options with stochastic rates, caplets |
| Annuity | swap measure | swaptions |

Choosing the numeraire that appears in the payoff usually turns a hard expectation into a probability.

### Incomplete markets

With more sources of risk than hedging instruments (jumps, stochastic volatility without traded options, trinomial steps), there are many equivalent martingale measures.
Each gives an arbitrage-free price, and the set of such prices is an interval whose ends are the sub- and super-replication costs.
Picking one price requires extra input: a utility, a calibration to traded options, or a risk premium for the unhedgeable factor.

## Worked examples

### One-period binomial call

"Stock at 100 goes to 120 or 90, rate 0. Price a call struck at 100."
Replicate: the payoff is 20 or 0, so $\Delta = \frac{20 - 0}{120 - 90} = \frac23$.
Cash: $\frac23 \cdot 90 + B = 0$ gives $B = -60$.
Price: $\frac23 \cdot 100 - 60 = 6.67$.
Risk-neutral check: $q = \frac{1 - 0.9}{1.2 - 0.9} = \frac13$ and $\frac13 \cdot 20 = 6.67$.
"If you believed the up move had probability 0.9 and quoted $0.9 \times 20 = 18$, I would sell you the call, buy $\frac23$ shares and borrow 60, and lock in 11.33 in every state."

### Trinomial model: incomplete, so a price range

"Same stock, but it can go to 120, 100 or 90. What can the call be worth?"
Martingale measures satisfy $120q_u + 100q_m + 90q_d = 100$ with $q_u + q_m + q_d = 1$, i.e. $q_d = 2q_u$ and $q_m = 1 - 3q_u$; all strictly positive iff $0 < q_u < \frac13$.
The call is worth $20q_u$, so any price in $(0, \frac{20}{3})$ is arbitrage-free.
The upper end is the super-replication cost: $\frac23$ shares minus 60 cash pays $20, 6.67, 0$, dominating the call $20, 0, 0$.
Two assets cannot span three states, so the second FTAP's uniqueness fails.

### Forward price by replication

"Non-dividend stock at $S_0$, rate $r$. What is the fair forward price for delivery at $T$?"
Buy the stock now, financed by borrowing $S_0$; at $T$ you own the stock and owe $S_0e^{rT}$.
This replicates a long forward with delivery price $S_0e^{rT}$ at zero cost, so $F = S_0e^{rT}$ (with dividend yield $q$: $S_0e^{(r - q)T}$).
Under $Q$ the same follows from $E^Q[S_T] = S_0e^{rT}$.
No model for $S$ was needed; forwards are priced by static replication and hold even when Black-Scholes fails (see [Forwards, Futures and Carry](../05-Derivatives-and-Volatility/01-Forwards-Futures-and-Carry.md)).

### Digital and asset-or-nothing by numeraire change

Black-Scholes market, $S_0 = 100$, $K = 105$, $T = 0.5$, $r = 5\%$, $\sigma = 25\%$.
The call payoff splits as $(S_T - K)^+ = S_T\mathbf{1}_{S_T > K} - K\mathbf{1}_{S_T > K}$.

- Cash-or-nothing: $e^{-rT}Q(S_T > K) = e^{-rT}N(d_2) = 0.4016$, since $\log S_T$ has $Q$-drift $r - \sigma^2/2$.
- Asset-or-nothing: with the stock as numeraire, $V_0 = S_0\,E^{S}[\mathbf{1}_{S_T > K}] = S_0 N(d_1) = 48.16$, since under $Q^S$ the log-drift is $r + \sigma^2/2$.
- Call: $48.16 - 105 \times 0.4016 = 5.99$, the [Black-Scholes](07-Black-Scholes-Derivation.md) price.

With $\mu = 15\%$ the real-world probability of finishing in the money is $0.524$ versus the risk-neutral $0.412$; the price uses $0.412$.
Discounting the $P$-expected payoff at $\mu$ instead gives $8.31$, which is wrong, while weighting $P$-paths by the deflator $e^{-rT}dQ/dP$ with $\lambda = 0.4$ recovers $5.98$ in a $4 \times 10^6$-path simulation.

### Pricing a power claim

"Price a claim paying $S_T^2$ in the Black-Scholes market."
Under $Q$, $S_T = S_0\exp((r - \sigma^2/2)T + \sigma W^Q_T)$, so $E^Q[S_T^2] = S_0^2\exp(2rT - \sigma^2 T + 2\sigma^2 T) = S_0^2e^{(2r + \sigma^2)T}$.
Price: $e^{-rT}E^Q[S_T^2] = S_0^2e^{(r + \sigma^2)T}$.
With the numbers above: $10^4 e^{(0.05 + 0.0625) \times 0.5} = 10^4 e^{0.05625} = 10578.6$, matched by Monte Carlo.
The claim is worth more than $S_0^2$ grown at $r$ because of convexity: it is long volatility.

## Pitfalls

- Reading $q$ as a forecast; it is a pricing weight that embeds risk aversion, and $Q$ probabilities of crashes are typically higher than $P$ probabilities.
- Thinking "risk-neutral pricing" assumes investors are risk-neutral; it assumes only no arbitrage and replication.
- Discounting expected payoffs under $P$ at $\mu$ or at a guessed risk-adjusted rate; the correct rate depends on the payoff and is not the stock's.
- Forgetting that $Q$ depends on the numeraire: "the" risk-neutral measure means the bank-account numeraire.
- Using drift $r$ for a dividend-paying stock or a currency; the $Q$-drift is $r - q$ (or $r_d - r_f$).
- Quoting a unique price in an incomplete market; without extra assumptions only bounds follow.
- Omitting equivalence: a measure that gives zero weight to a state the real world can reach allows pseudo-arbitrages and is not a valid pricing measure.

## Interview questions

> [!question]- sc-rn-binomial-q | In a one-period binomial model with factors $u, d$ and gross rate $R$, what is the risk-neutral up probability and when is the model arbitrage-free?
> $q = (R - d)/(u - d)$; arbitrage-free iff $d < R < u$, which is exactly $0 < q < 1$.

> [!question]- sc-rn-binomial-call-price | Stock 100 goes to 120 or 90, zero rates. Price of the 100-strike call?
> $20/3 \approx 6.67$. Hedge with $2/3$ shares and $-60$ cash; equivalently $q = 1/3$ times payoff 20.

> [!question]- sc-rn-ftap-first | State the first fundamental theorem of asset pricing.
> No arbitrage (no free lunch with vanishing risk in continuous time) iff there is an equivalent measure under which discounted traded prices are martingales.

> [!question]- sc-rn-ftap-second | State the second fundamental theorem and give an incomplete example.
> An arbitrage-free market is complete iff the equivalent martingale measure is unique. A trinomial step with only stock and cash has a one-parameter family of measures, so option prices lie in an interval.

> [!question]- sc-rn-why-no-mu | Why does the stock's expected return not appear in the Black-Scholes price?
> The option is replicated by a delta hedge whose cost does not depend on $\mu$. Under the change to $Q$ the drift becomes $r$, but volatility is unchanged because quadratic variation is the same under equivalent measures.

> [!question]- sc-rn-market-price-of-risk | What is the market price of risk in Black-Scholes, and how does it define $Q$?
> $\lambda = (\mu - r)/\sigma$. $W^Q = W + \lambda t$ is $Q$-Brownian with $dQ/dP = \exp(-\lambda W_T - \lambda^2 T/2)$.

> [!question]- sc-rn-numeraire-formula | State the general pricing formula with numeraire $N$.
> $V_0 = N_0\,E^N[V_T/N_T]$, where $Q^N$ makes every traded price divided by $N$ a martingale; $dQ^N/dQ = (N_T/N_0)/(B_T/B_0)$.

> [!question]- sc-rn-share-measure-nd1 | What is $N(d_1)$ in the Black-Scholes formula, probabilistically?
> The probability that $S_T > K$ under the share measure (stock as numeraire), where $\log S$ has drift $r + \sigma^2/2$. $S_0N(d_1)$ is the price of the asset-or-nothing call.

> [!question]- sc-rn-digital-price | Price of a cash-or-nothing digital call paying 1 if $S_T > K$ in Black-Scholes?
> $e^{-rT}N(d_2)$. It is the discounted $Q$-probability of finishing in the money.

> [!question]- sc-rn-forward-price | What is the forward price of a non-dividend stock, and does it need a model?
> $S_0e^{rT}$, model-free: buy the stock with borrowed money and deliver it at $T$.

> [!question]- sc-rn-breeden-litzenberger | How do you get the risk-neutral density from option prices?
> $q_T(K) = e^{rT}\,\partial^2 C/\partial K^2$. A butterfly centred at $K$ with wing width $h$ costs about $h^2e^{-rT}q_T(K)$.

> [!question]- sc-rn-state-prices-positive | In a finite-state model, what condition on state prices is equivalent to no arbitrage?
> All state prices strictly positive. Then normalising them by the riskless growth factor gives an equivalent martingale measure.

> [!question]- sc-rn-deflator | Can you price under the real-world measure $P$? How?
> Yes, with a stochastic discount factor: $V_0 = E^P[\xi_T V_T]$ with $\xi_T = e^{-rT}dQ/dP$. Discounting the $P$-expectation at a constant rate is wrong in general.

> [!question]- sc-rn-dividend-drift | What is the risk-neutral drift of a stock with continuous dividend yield $q$, and of an FX rate?
> $r - q$ for the stock, $r_d - r_f$ for the FX rate (domestic per foreign). The total return including dividends or foreign interest must earn $r$ (or $r_d$).

## Further reading

- Steven Shreve, *Stochastic Calculus for Finance I: The Binomial Asset Pricing Model*, chapter 1.
- Steven Shreve, *Stochastic Calculus for Finance II: Continuous-Time Models*, chapter 5 (risk-neutral pricing and the FTAP) and chapter 9 (change of numeraire).
- J. M. Harrison and S. Pliska, "Martingales and Stochastic Integrals in the Theory of Continuous Trading", *Stochastic Processes and their Applications* 11 (1981).
- F. Delbaen and W. Schachermayer, "A General Version of the Fundamental Theorem of Asset Pricing", *Mathematische Annalen* 300 (1994).
- H. Geman, N. El Karoui and J.-C. Rochet, "Changes of Numeraire, Changes of Probability Measure and Option Pricing", *Journal of Applied Probability* 32 (1995).
- D. Breeden and R. Litzenberger, "Prices of State-Contingent Claims Implicit in Option Prices", *Journal of Business* 51 (1978).
