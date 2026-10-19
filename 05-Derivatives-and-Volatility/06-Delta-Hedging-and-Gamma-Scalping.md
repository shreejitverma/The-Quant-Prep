---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
prereqs: [the-greeks]
est_hours: 4
sources: [Euan Sinclair - Volatility Trading (hedging and volatility P&L chapters), Sheldon Natenberg - Option Volatility and Pricing (dynamic hedging chapters), Ahmad and Wilmott (2005) - Which free lunch would you like today sir? Delta hedging volatility arbitrage and optimal portfolios - Wilmott Magazine, Michael Kamal (1998) - When you cannot hedge continuously - the corrections to Black-Scholes - Goldman Sachs Quantitative Strategies Research Notes, Emanuel Derman and Michael Miller - The Volatility Smile (discrete hedging error), Leland (1985) - Option pricing and replication with transactions costs - Journal of Finance 40(5), Hull and White (2017) - Optimal delta hedging for options - Journal of Banking and Finance 82]
---

# Delta Hedging and Gamma Scalping P&L

## TL;DR

- A delta-hedged option earns $\tfrac12\Gamma S^2\left[(\delta S/S)^2 - \sigma_i^2\,\delta t\right]$ per step: realised minus implied variance, weighted by dollar gamma.
- Summed over the life: P&L $= \tfrac12\int_0^T e^{-rt}\,\Gamma_t S_t^2(\sigma_r^2 - \sigma_i^2)\,dt$ when hedging at implied vol; to first order the expected profit is vega $\times (\sigma_r - \sigma_i)$.
- Hedging at the implied vol gives smooth daily P&L but a path-dependent total (it depends on where spot was when variance was realised); hedging at the (unknown) realised vol locks $V(\sigma_r) - V(\sigma_i)$ but gives noisy daily marks.
- Gamma scalping: long gamma sells rallies and buys dips, locking $\tfrac12\Gamma\,\delta S^2$ per move against theta; short gamma does the opposite and loses on big moves.
- Discrete hedging adds noise with standard deviation about $\sqrt{\pi/4}\,\mathcal{V}\sigma/\sqrt{N}$ for $N$ rebalances (Kamal, Goldman Sachs 1998), while transaction costs grow like $\sqrt{N}$; the hedge frequency trades one against the other.

## Learning objectives

- Derive the hedged P&L: 0.5 * Gamma * S^2 * (realized variance - implied variance) * dt.
- Compare hedging at implied versus realized volatility and the path dependence of P&L.
- Quantify discrete hedging error and choose a hedging frequency.

## Core concepts

### The hedged P&L derivation

You buy an option at implied vol $\sigma_i$, value it with Black-Scholes at $\sigma_i$, and hold $-\Delta_i$ shares, financing everything at $r$.
The stock actually follows $dS = \mu S\,dt + \sigma_r S\,dW$.
The portfolio $\Pi = V - \Delta_i S$ changes by

$$
d\Pi = dV - \Delta_i\,dS - r(V - \Delta_i S)\,dt.
$$

Itô with the real dynamics: $dV = \Theta\,dt + \Delta_i\,dS + \tfrac12\Gamma_i\sigma_r^2 S^2\,dt$.
The Black-Scholes PDE at $\sigma_i$: $\Theta = rV - rS\Delta_i - \tfrac12\sigma_i^2 S^2\Gamma_i$.
Substituting, the $dS$, $\mu$ and financing terms all cancel:

$$
d\Pi = \tfrac12\Gamma_i S^2\left(\sigma_r^2 - \sigma_i^2\right)dt.
$$

In discrete time replace $\sigma_r^2\,dt$ by the realised squared return $(\delta S/S)^2$:

$$
\text{P\&L}_{\text{step}} \approx \tfrac12\Gamma S^2\left[\left(\frac{\delta S}{S}\right)^2 - \sigma_i^2\,\delta t\right] = \underbrace{\tfrac12\Gamma\,\delta S^2}_{\text{gamma}} + \underbrace{\Theta\,\delta t}_{\text{theta}}.
$$

This is the single most important equation for an options trader.
Every day, long gamma wins if the move exceeded the implied breakeven $S\sigma_i\sqrt{\delta t}$ and loses otherwise.
The direction of the move does not matter; the drift $\mu$ does not appear.

### Hedging at implied versus realised volatility

Hedging at implied $\sigma_i$ (the market-standard choice):

- Total P&L $= \tfrac12\int_0^T e^{-rt}\,\Gamma_i(t, S_t)\,S_t^2(\sigma_r^2 - \sigma_i^2)\,dt$ is path dependent.
  If the realised variance comes while spot is near the strike (high dollar gamma) you earn a lot; if it comes far from the strike you earn little.
  You can be right on volatility and still lose money.
- Daily P&L is smooth and always has the sign of $(\delta S/S)^2 - \sigma_i^2\delta t$, which makes it easy to explain.

Hedging at realised $\sigma_r$ (if you knew it):

- Total P&L is deterministic: $V(\sigma_r) - V(\sigma_i)$ at inception, in present value.
- The mark-to-market along the way is noisy: the option is marked at $\sigma_i$ but hedged with $\Delta_r$, so each day's P&L carries an extra $(\Delta_i - \Delta_r)\,\delta S$ term (Ahmad and Wilmott, 2005).
- In practice $\sigma_r$ is unknown, so this is a benchmark, not a strategy.

To first order in the vol difference both give the same expected profit, vega $\times (\sigma_r - \sigma_i)$.

### Gamma scalping mechanics

Long gamma means your delta rises when spot rises: you are too long after a rally and too short after a sell-off.
Rehedging sells into rallies and buys dips, which mechanically realises the convexity.

- A round trip from $S$ to $S + h$ and back, rehedging at each point, earns about $\Gamma h^2$ (two moves of $\tfrac12\Gamma h^2$).
- Short gamma rehedges by buying rallies and selling dips; it collects theta but loses $\tfrac12\Gamma\,\delta S^2$ on each move, and large gaps are fatal.
- Rehedging rules: fixed time (every close, every hour), fixed delta band (rehedge when net delta exceeds a threshold), or fixed move (every 0.5 or 1 standard deviation).
  Move-based hedging captures scalps in choppy markets; time-based hedging is simpler and easier to explain.
- Long gamma traders like mean-reverting intraday paths (many round trips); short gamma traders prefer trending, quiet days.

### Discrete hedging error

With $N$ equally spaced rebalances and $\sigma_r = \sigma_i$, the hedged P&L has mean near zero and standard deviation (Kamal 1998, a Goldman Sachs Quantitative Strategies note; also in Derman and Miller, *The Volatility Smile*)

$$
\text{sd} \approx \sqrt{\frac{\pi}{4}}\,\frac{\mathcal{V}\,\sigma}{\sqrt{N}},
$$

with $\mathcal{V}$ the vega per 1.00 of vol.
Equivalently, discrete hedging makes the realised volatility you capture uncertain by about $\sqrt{\pi/4}\,\sigma/\sqrt{N}$ vol, since P&L $\approx \mathcal{V} \times$ (vol error).
Quadrupling the hedge frequency halves the noise.

### Transaction costs and hedge frequency

With a one-way proportional cost $\kappa$ (half-spread plus fees as a fraction of price), each rebalance trades about $E\lvert\delta\Delta\rvert = \Gamma S\sigma\sqrt{\delta t}\sqrt{2/\pi}$ shares.
Summing over the life, the expected cost is approximately

$$
\text{cost} \approx \kappa\sqrt{\frac{2}{\pi}}\,\mathcal{V}\sqrt{\frac{N}{T}} + \text{entry and exit trades},
$$

growing like $\sqrt{N}$ while the hedging noise falls like $1/\sqrt{N}$.
Leland (1985) folds the cost into an adjusted volatility for pricing:

$$
\tilde\sigma^2 = \sigma^2 \mp 2\kappa\sigma\sqrt{\frac{2}{\pi\,\delta t}},
$$

minus for a long-gamma position (you should pay a lower vol because hedging costs you) and plus for short gamma.
Optimal-band models (Whalley and Wilmott) show the no-trade band around the target delta should scale with the cube root of the cost and widen where gamma is large relative to your risk appetite.

### Which delta?

The Black-Scholes delta assumes the option's implied vol does not move when spot moves (sticky strike).
If the smile moves with spot (sticky moneyness or sticky delta) the hedge ratio changes by vega $\times\,\partial\sigma/\partial S$.
In equity indices vol rises when spot falls, and the empirically minimum-variance delta (Hull and White, 2017) is below the Black-Scholes delta for both calls and puts.
Getting this wrong shows up as systematic delta P&L in the attribution.

## Worked examples

Every number below is printed and asserted by [deriv_01_07_hedging_pnl.py](code/deriv_01_07_hedging_pnl.py).
Simulations use exact lognormal steps and numpy's `default_rng` with the seed named in each example, so they are quoted as "about" the printed value.

### Example 1: a two-day gamma scalp

Long one one-month ATM straddle: $S = K = 100$, $\sigma_i = 20\%$, zero rates, price 4.61.
Per option $\Gamma = 0.0691$ and $\Theta = -0.0378$ per day, so the straddle has $\Gamma = 0.138$ and $-0.0757$ per day.
Breakeven daily move: $100 \times 0.2/\sqrt{365} = 1.05$.

- Day 1: spot rallies to 102.
  Straddle delta rises by about $0.138 \times 2 = 0.276$; sell 0.276 shares at 102.
- Day 2: spot falls back to 100 and delta returns to where it started; buy back 0.276 shares at 100.

Scalp profit $0.276 \times 2 = 0.55$, against two days of theta, $2 \times 0.0757 = 0.15$: net about $+0.40$.
Same answer from the formula: two moves of $\tfrac12 \times 0.138 \times 2^2 = 0.276$ each.
If instead spot had drifted 0.5 each day, gamma would have earned $2 \times \tfrac12 \times 0.138 \times 0.25 = 0.035$ against 0.15 of theta.
Exact revaluation: the straddle delta goes from 0.023 at 100 to 0.294 at 102 a day later, a change of 0.271 rather than 0.276, and the exact two-day hedged P&L (straddle revalued, hedge reset to the exact delta each day) is 0.39 against the 0.40 estimate.

### Example 2: right on volatility, and how you hedge

Buy a one-year ATM call ($S = K = 100$, zero rates) at $\sigma_i = 20\%$, price 7.97; the stock then realises $\sigma_r = 25\%$.
Value at 25% is 9.95, so the target profit is $V(25\%) - V(20\%) = 1.98$, and vega $\times$ 5 vol points $= 39.7 \times 0.05 = 1.98$.

Monte Carlo, 20,000 paths, 365 daily rebalances, seed 11 (all three rows use the same random numbers, so each row changes one thing):

| Hedge vol | Mean P&L | Std of P&L |
| :--- | ---: | ---: |
| Realised (25%) | 1.98 | 0.45 |
| Implied (20%) | 2.00 | 0.96 |
| Implied (20%), stock drift 10% | 1.98 | 0.95 |

Each mean is within three standard errors of 1.98.
Hedging at realised vol leaves only discrete-hedging noise (0.45); hedging at implied vol doubles the dispersion, because the payoff then depends on how much dollar gamma you held while the variance was realised.
Adding a 10% drift with everything else fixed leaves the mean and the dispersion where they were, as the derivation says.

### Example 3: the gamma-theta identity on simulated paths

Same trade, 252 daily rebalances, 20,000 paths, seed 13.
For each path the script computes the actual hedged P&L and, separately, $\sum_i \tfrac12\Gamma_i S_i^2\left[(\delta S_i/S_i)^2 - \sigma_i^2\,\delta t\right]$ with $\Gamma_i$ the Black-Scholes gamma at 20% at the start of each day.

| Quantity | Value |
| :--- | ---: |
| Mean hedged P&L | 1.98 |
| Mean of the gamma-theta sum | 1.98 |
| Correlation across paths | 0.996 |
| Std of hedged P&L | 1.00 |
| Std of the difference | 0.09 |

The identity explains the P&L path by path, not just on average: 99.2% of the variance ($0.996^2$), with the remainder from the higher-order terms (third order in each day's move and the cross terms with time) that the second-order expansion drops.

### Example 4: discrete hedging error

One-year ATM call, $S = K = 100$, $\sigma_r = \sigma_i = 20\%$, zero rates, vega $\mathcal{V} = 39.7$.
The rule: $\sqrt{\pi/4} \times 39.7 \times 0.2/\sqrt{N} = 7.04/\sqrt{N}$.

| Rebalances $N$ | Formula sd | Monte Carlo sd (40,000 paths, seed 12) |
| ---: | ---: | ---: |
| 12 (monthly) | 2.03 | 1.93 |
| 52 (weekly) | 0.98 | 0.96 |
| 252 (daily) | 0.44 | 0.44 |

On a 7.97 option, weekly hedging leaves a one-standard-deviation P&L noise of about 12% of premium, or about 2.4 vol points of vega-equivalent ($0.96/39.7$).
The rule comes from Kamal's 1998 Goldman Sachs note, whose Table 1 (one-month ATM option, $r = 5\%$, 20% vol, 50,000 paths) reports 0.41 and 0.20 for 21 and 84 rebalances against 0.443 and 0.222 from the formula with vega 0.115 per vol point.
The script reruns that case (seed 14) and gets about 0.43 and 0.22.
(The note quotes the option value as 2.512, which is the one-month call; the put is 2.096 by parity, and the hedging-error distribution is the same for both.)

### Example 5: choosing the hedge frequency with costs

Same option, one-way cost $\kappa = 5$bp, same paths as Example 4 with and without costs, so the difference is exactly the cost.
Formula rebalancing cost $0.0005 \times 0.798 \times 39.7 \times \sqrt{N}$:

| $N$ | Formula rebalancing cost | Monte Carlo total cost | Hedge noise sd |
| ---: | ---: | ---: | ---: |
| 12 | 0.05 | 0.11 | 1.93 |
| 52 | 0.11 | 0.17 | 0.95 |
| 252 | 0.25 | 0.31 | 0.45 |

The gap of about 0.05 between the two cost columns is the entry trade ($0.0005 \times 0.540 \times 100 = 0.027$) plus the unwind at expiry.
Going from weekly to daily costs about 0.14 more and cuts the noise from 0.95 to 0.45.
A single large position with an edge of a vol point or two needs daily hedging, or the noise swamps the edge.
A market maker hedges net book delta, so per-line noise partly diversifies and wider bands (fewer trades) are affordable.
Leland at daily hedging: $2 \times 0.0005 \times 0.2 \times \sqrt{2 \times 252/\pi} = 0.00253$, so $\tilde\sigma = \sqrt{0.04 \pm 0.00253}$ is 20.62% or 19.36%: hedging costs alone justify about 0.6 vol points either side of mid.

## Pitfalls

- Thinking a long-vol trade profits whenever realised beats implied; with implied-vol hedging the P&L is weighted by dollar gamma along the path, and a big move far from the strike pays little.
- Forgetting that the theta you pay is set by implied vol, not realised; buying options "because they are cheap" means cheap relative to the variance you expect to realise near the strike.
- Hedging with a stale or wrong delta (ignoring smile dynamics, dividends or borrow) and misreading the resulting delta P&L as vol P&L.
- Rehedging too often with meaningful costs, or too rarely so that noise swamps the edge; size the frequency with the $1/\sqrt{N}$ versus $\sqrt{N}$ trade-off.
- Treating short gamma as free theta; the loss on a gap is $\tfrac12\Gamma\,\delta S^2$ with no chance to rehedge in between.
- Annualising realised vol from close-to-close returns while the book hedges intraday (or vice versa); the variance you capture is the one on your hedging grid.
- Ignoring that weekend and holiday theta is a clock convention; if you charge theta over the weekend but the stock cannot move, you need a trading-day clock.

## Interview questions

> [!question]- deriv-hedged-pnl-formula | Derive the P&L of a delta-hedged long option over a short interval.
> $\tfrac12\Gamma S^2[(\delta S/S)^2 - \sigma_i^2\,\delta t]$.
> Hedged P&L is $\tfrac12\Gamma\,\delta S^2 + \Theta\,\delta t$ (delta cancels, financing cancels), and the Black-Scholes PDE gives $\Theta = -\tfrac12\sigma_i^2S^2\Gamma$ for the hedged position.

> [!question]- deriv-drift-irrelevant-hedged | Does the stock's drift affect the P&L of a delta-hedged option?
> No, to first order the drift drops out; only realised versus implied variance weighted by dollar gamma matters.
> In the derivation the $dS$ terms cancel between option and hedge; a Monte Carlo with 0% and 10% drift gives the same mean P&L.

> [!question]- deriv-hedge-at-implied-vs-realized | You buy at 20% implied and realised turns out 25%. Compare hedging at implied and at realised vol.
> At realised you lock $V(25\%) - V(20\%)$ (about 1.98 on a one-year ATM 100 call) with noisy daily marks; at implied the expected P&L is similar but the total is path dependent with much wider dispersion.
> At implied, P&L $= \tfrac12\int\Gamma_i S^2(\sigma_r^2 - \sigma_i^2)dt$ depends on how much gamma you held when variance was realised.

> [!question]- deriv-right-vol-lose-money | How can you buy options below realised volatility, delta-hedge, and still lose money?
> If you hedge at implied vol and most of the realised variance occurs while spot is far from the strike, where your dollar gamma is small, while you pay theta near the strike.
> P&L weights $\sigma_r^2 - \sigma_i^2$ by $\Gamma S^2$ along the path, not uniformly.

> [!question]- deriv-gamma-scalp-round-trip | You are long gamma $\Gamma$ and spot goes from $S$ to $S + h$ and back, rehedging at each point. What do you make before theta?
> About $\Gamma h^2$.
> At $S + h$ you sell $\Gamma h$ shares; buying them back at $S$ earns $\Gamma h \times h$, equal to two moves of $\tfrac12\Gamma h^2$.

> [!question]- deriv-breakeven-move-scalping | What is the daily breakeven move for a long-gamma position, and does it depend on the position size?
> $S\sigma_i\sqrt{\delta t}$, about $S\sigma_i/19$ on a calendar-day clock or $S\sigma_i/16$ on trading days; independent of the size of gamma.
> Setting $\tfrac12\Gamma\,\delta S^2 = \tfrac12\sigma_i^2S^2\Gamma\,\delta t$ cancels $\Gamma$.

> [!question]- deriv-discrete-hedging-error | Give the Derman-Kamal estimate of the P&L noise from hedging $N$ times, and evaluate it for a one-year ATM 100 call at 20% vol hedged weekly.
> sd $\approx \sqrt{\pi/4}\,\mathcal{V}\sigma/\sqrt{N} = 0.886 \times 39.7 \times 0.2/\sqrt{52} = 0.98$.
> A Monte Carlo gives 0.96; the noise halves when the hedge frequency quadruples.

> [!question]- deriv-hedge-frequency-tradeoff | How do transaction costs and hedging noise scale with the number of rebalances $N$?
> Costs grow like $\sqrt{N}$ (about $\kappa\sqrt{2/\pi}\,\mathcal{V}\sqrt{N/T}$) while the P&L noise falls like $1/\sqrt{N}$.
> Each rebalance trades $\approx\Gamma S\sigma\sqrt{\delta t}\sqrt{2/\pi}$ shares, and there are $N$ of them.

> [!question]- deriv-leland-adjustment | What is Leland's volatility adjustment for transaction costs, and which way does it go for a long option?
> $\tilde\sigma^2 = \sigma^2 \mp 2\kappa\sigma\sqrt{2/(\pi\,\delta t)}$ with one-way cost $\kappa$: lower vol for a long-gamma hedger, higher for short gamma.
> Hedging costs act like extra realised variance working against the hedger; at 5bp, 20% vol and daily hedging it is about $\pm 0.6$ vol points.

> [!question]- deriv-short-gamma-risk | Why is a short-gamma book most exposed to gaps rather than to high realised vol per se?
> Because a gap delivers the whole $\tfrac12\Gamma\,\delta S^2$ loss at once with no chance to rehedge in between, and the loss is quadratic in the move.
> With constant gamma, a 10% move in ten 1% steps rehedged each step costs $10 \times \tfrac12\Gamma S^2(1\%)^2$, ten times less than $\tfrac12\Gamma S^2(10\%)^2$ for the same move as one gap.

> [!question]- deriv-scalp-example-numbers | Long a one-month ATM straddle with total gamma 0.138 and theta $-0.076$ per day. Spot goes 100 to 102 and back over two days. Net P&L after rehedging?
> About $+0.40$: scalp $0.138 \times 2 \times 2 = 0.55$ minus two days of theta 0.15.
> Sell 0.276 shares at 102 and buy them back at 100.

> [!question]- deriv-gamma-theta-simulation | How would you test, on simulated paths, that delta-hedged P&L really is $\sum \tfrac12\Gamma S^2[(\delta S/S)^2 - \sigma_i^2\delta t]$?
> Simulate the stock at the realised vol, hedge daily at the implied-vol delta, and compare each path's actual P&L with the gamma-theta sum computed from the same moves.
> On 20,000 paths (realised 25%, implied 20%, daily, seed 13) both average 1.98, the correlation is 0.996 and the difference has std 0.09 against 1.00 for the P&L: the identity holds path by path, up to higher-order terms.

> [!question]- deriv-hedge-cost-weekly-daily | One-year ATM 100 call at 20%, one-way cost 5bp. What does moving from weekly to daily hedging cost, and what does it buy?
> About 0.14 more in costs (0.17 to 0.31 in total) for a cut in P&L noise from 0.95 to 0.45.
> Rebalancing cost grows like $\kappa\sqrt{2/\pi}\,\mathcal{V}\sqrt{N}$ (0.11 to 0.25) and the noise falls like $1/\sqrt{N}$; the rest of the cost is the entry and unwind trades.

> [!question]- deriv-hedge-noise-vol-points | Weekly hedging of a one-year ATM 100 call at 20% vol leaves P&L noise of about 0.96. Express that in vol points and as a share of premium.
> About 2.4 vol points ($0.96/39.7$ per unit vol) and 12% of the 7.97 premium.
> P&L $\approx$ vega $\times$ vol error, so an edge smaller than about 2.4 vol points is not reliably captured with weekly hedging.

> [!question]- deriv-sticky-strike-delta | Why might an equity-index desk hedge with less than the Black-Scholes delta?
> Because implied vol tends to rise when spot falls, so a spot move carries a predictable vol move whose vega P&L offsets part of the delta P&L.
> The minimum-variance delta is $\Delta_{BS} + \mathcal{V}\,E[\delta\sigma]/\delta S$, and with negative spot-vol correlation the second term is negative.

## In this repo and SDE-Interview-Prep

- Code: [deriv_01_07_hedging_pnl.py](code/deriv_01_07_hedging_pnl.py) prints and asserts every number in this note (straddle scalp, hedged-P&L Monte Carlo, the gamma-theta identity, discrete-hedging noise and the Goldman Sachs table, costs and Leland); run it with `uv run --no-project --with numpy python 05-Derivatives-and-Volatility/code/deriv_01_07_hedging_pnl.py`.
- Prev: [The Greeks](05-The-Greeks.md). Next: [Implied Volatility and the Smile](07-Implied-Volatility-and-the-Smile.md).
- Applications: [Option Strategies and Volatility Trading](13-Option-Strategies-and-Volatility-Trading.md), [Variance Swaps and Volatility Products](14-Variance-Swaps-and-Volatility-Products.md), [Hedging and Risk for Market Makers](../08-Market-Making/06-Hedging-and-Risk-for-Market-Makers.md).

## Further reading

- Euan Sinclair, *Volatility Trading*, chapters on hedging and volatility P&L.
- Sheldon Natenberg, *Option Volatility and Pricing*, chapters on dynamic hedging.
- R. Ahmad and P. Wilmott (2005), "Which free lunch would you like today, sir?: Delta hedging, volatility arbitrage and optimal portfolios", *Wilmott Magazine*.
- M. Kamal (1998), "When you cannot hedge continuously: the corrections to Black-Scholes", Goldman Sachs Quantitative Strategies Research Notes (Equity Derivatives Research, Quantitative Insights), the $\sqrt{\pi/4}\,\kappa\sigma/\sqrt{N}$ rule and its Table 1; a copy is hosted at emanuelderman.com.
- Emanuel Derman and Michael B. Miller, *The Volatility Smile* (Wiley 2016), on hedging error from discrete rebalancing.
- H. E. Leland (1985), "Option pricing and replication with transactions costs", *Journal of Finance* 40(5).
- A. E. Whalley and P. Wilmott (1997), "An asymptotic analysis of an optimal hedging model for option pricing with transaction costs", *Mathematical Finance* 7(3).
- J. Hull and A. White (2017), "Optimal delta hedging for options", *Journal of Banking and Finance* 82.
