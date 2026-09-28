---
type: concept
track: [quant-trader]
tier: core
status: solid
prereqs: [the-greeks]
est_hours: 4
sources: [Sheldon Natenberg - Option Volatility and Pricing (spreads and volatility trading chapters), Euan Sinclair - Volatility Trading (2nd edition Wiley 2013), John Hull - Options Futures and Other Derivatives (trading strategies involving options chapter), Jim Gatheral - The Volatility Surface - A Practitioner's Guide (Wiley 2006)]
---

# Option Strategies and Volatility Trading

## TL;DR

- Every option position is a bundle of exposures: direction (delta), realized volatility (gamma), implied volatility by expiry (vega term structure), skew (risk reversals, vanna), and wings (butterflies, volga). Build the position that isolates the one you have a view on, and hedge the rest.
- Straddles and strangles trade vol level; risk reversals trade skew; butterflies and vega-neutral strangle-versus-straddle trade the wings; calendars trade term structure (long vega, short gamma).
- The ATM straddle prices the expected absolute move: straddle $\approx 0.8\,\sigma S\sqrt{T}$, and the daily break-even move of a delta-hedged option is $\sigma/\sqrt{252}$ (rule of 16) in trading-day time.
- Long gamma pays theta and earns $\tfrac12\Gamma S^2(\sigma_{real}^2 - \sigma_{imp}^2)\,dt$; the edge is realized versus implied, not direction.
- Event vol: back the event move out of the term structure, $\sigma_i^2 T_i = \sigma_b^2(T_i - \delta) + m^2$ for each expiry spanning the event, then trade the implied move against your estimate of the real one and remember the post-event vol crush.

## Learning objectives

- Construct and explain straddles, strangles, spreads, butterflies, condors, calendars and risk reversals.
- Separate directional, volatility and skew exposures in a position.
- Trade event volatility (earnings) and estimate implied moves.

## Core concepts

### The strategy menu

Payoff shapes are in [Option Payoffs and Put-Call Parity](02-Option-Payoffs-and-Put-Call-Parity.md); here the point is the Greeks, for a long position with spot near the centre strike.

| Strategy | Construction | Delta | Gamma | Vega | Theta | What it expresses |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Straddle | long ATM call + put | $\approx 0$ | $+$ | $+$ | $-$ | vol level, realized > implied |
| Strangle | long OTM put + OTM call | $\approx 0$ | $+$ (lower ATM) | $+$ | $-$ | vol level, cheaper, more volga |
| Call (put) spread | long $K_1$, short $K_2$ | $+$ ($-$) | sign flips across strikes | sign flips | sign flips | capped directional view, cheap |
| Butterfly | long $K - h$, short 2 $K$, long $K + h$ | $\approx 0$ | $-$ | $-$ | $+$ | pin near $K$, low realized vol |
| Iron condor (short) | short strangle, long further wings | $\approx 0$ | $-$ | $-$ | $+$ | range-bound, defined risk |
| Calendar | short near, long far, same strike | $\approx 0$ | $-$ | $+$ | $+$ | term structure, far vol cheap |
| Risk reversal | long OTM call, short OTM put | $+$ | small | $\approx 0$ | small | skew (and direction) |
| Ratio spread | long 1 ATM, short 2 OTM | small | $-$ at short strike | $-$ | $+$ | sell rich wing vol |
| Collar | long stock, long put, short call | $+$ | small | small | small | cheap protection |

Signs of spreads and flies depend on where spot sits relative to the strikes and change as expiry approaches: a butterfly bought far from expiry is nearly Greek-neutral, while in the last week it is sharply short gamma at the body.

### Decomposing a position

A trader thinks in a Taylor expansion of P&L:

$$
dV \approx \Delta\,dS + \tfrac12\Gamma\,dS^2 + \mathcal V\,d\sigma + \Theta\,dt + \text{vanna}\,dS\,d\sigma + \tfrac12\,\text{volga}\,d\sigma^2.
$$

- Directional: net delta, hedged away with the underlying or futures.
- Realized vol: gamma, whose P&L against theta is $\tfrac12\Gamma S^2(\sigma_{real}^2 - \sigma_{imp}^2)\,dt$ (see [Delta Hedging and Gamma Scalping](06-Delta-Hedging-and-Gamma-Scalping.md)).
- Implied vol level: vega, bucketed by expiry because vols do not move in parallel. Short-dated vol moves more than long-dated, roughly in proportion to $1/\sqrt{T}$, so desks look at "weighted vega" $\mathcal V \sqrt{T_{ref}/T}$.
- Skew: vega bucketed by strike or delta, or vanna ($\partial\Delta/\partial\sigma = \partial\mathcal V/\partial S$). A long 25-delta risk reversal is long skew: it gains when calls richen against puts.
- Wings (smile curvature): volga ($\partial\mathcal V/\partial\sigma$). OTM options have positive volga, ATM options almost none, so a vega-neutral long strangle, short straddle position is long vol-of-vol.

Gamma versus vega by maturity: ATM gamma scales like $1/\sqrt{T}$ and vega like $\sqrt{T}$.
Short-dated options are gamma instruments (you are trading realized vol day by day), long-dated options are vega instruments (you are trading implied vol).

### Straddle arithmetic

For an ATM-forward straddle with zero rates, $C + P = 2 S\,[2N(\tfrac12\sigma\sqrt T) - 1] \approx 2 \times 0.3989\,\sigma S\sqrt T \approx 0.8\,\sigma S\sqrt T$.
Since $E\lvert X\rvert = \sigma\sqrt{2/\pi} \approx 0.8\,\sigma$ for a normal, the straddle is the market's price of the expected absolute move.
The break-even daily move of a delta-hedged option solves $\tfrac12\Gamma S^2 (\delta S/S)^2 = -\Theta_{day}$, giving $\delta S/S = \sigma\sqrt{\Delta t}$: $\sigma/16$ per trading day, or $\sigma/\sqrt{365}$ per calendar day if theta is charged over weekends.

### Event volatility

A scheduled event adds a lump of variance on one day.
Model total variance to expiry $i$ as a diffusive part plus the event, $\sigma_i^2 T_i = \sigma_b^2 (T_i - \delta) + m^2$, with $\delta$ one day and $m$ the standard deviation of the event-day return.
Two expiries spanning the event give two equations for $\sigma_b$ and $m$; the expected absolute event move is $m\sqrt{2/\pi}$ if normal.
Practical points:

- The front expiry carries a high implied vol that collapses to $\sigma_b$ the morning after ("vol crush"); a long straddle needs the stock to move more than the implied move just to break even.
- Compare the implied move with the history of realized earnings moves for the name (and peers), and with the distribution shape: earnings moves are fat-tailed and often bimodal, so the straddle can be fair while the wings are mispriced.
- Short event vol is a classic premium harvest with rare large losses; size it by the tail, not by the average.

### How vol traders make money

- Realized versus implied: buy gamma when you expect realized above implied and hedge delta; the P&L path depends on where spot realises its variance relative to the strike (gamma-weighted).
- Implied vol mean reversion: buy vega when term structure is inverted and fear is spiking only if you can carry the theta, sell when it is complacently low only with tail protection.
- Relative value: calendar spreads against the expected term structure, skew trades against realized spot-vol correlation, dispersion (index versus constituents, [Dispersion and Correlation Trading](15-Dispersion-and-Correlation-Trading.md)).
- Flow: market makers earn edge by providing liquidity and then manage the residual Greeks; the book is judged on edge captured minus hedging slippage, not on views.

## Worked examples

### Example 1: anatomy of a one-month straddle

$S = K = 100$, 30 calendar days, $r = 0$, implied vol 25%.
Straddle: 5.717 (the $0.8\,\sigma S\sqrt T$ shortcut gives 5.734).
Break-evens at expiry: 94.28 and 105.72.
Greeks: delta $+0.029$ (ATM-spot, not ATM-forward, so slightly positive), gamma 0.111, vega 0.229 per vol point, theta $-0.095$ per calendar day.
Daily break-even move: $\sqrt{2 \times 0.095/0.111} = 1.31$, which is $25\%/\sqrt{365}$; if weekends are quiet, you need about $25\%/\sqrt{252} = 1.57\%$ on each trading day.

```python
import numpy as np
from scipy.stats import norm

def greeks(S, K, T, sigma, cp, r=0.0):
    """Black-Scholes price, delta, gamma, vega (per vol point), theta (per calendar day)."""
    sd = sigma * np.sqrt(T)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / sd
    d2 = d1 - sd
    disc = np.exp(-r * T)
    price = cp * (S * norm.cdf(cp * d1) - K * disc * norm.cdf(cp * d2))
    delta = cp * norm.cdf(cp * d1)
    gamma = norm.pdf(d1) / (S * sd)
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - cp * r * K * disc * norm.cdf(cp * d2)) / 365
    return np.array([price, delta, gamma, vega, theta])

def book(S, legs):
    """legs: (quantity, strike, expiry in years, vol, +1 call / -1 put)."""
    return sum(q * greeks(S, K, T, v, cp) for q, K, T, v, cp in legs)

names = ["price", "delta", "gamma", "vega", "theta"]
straddle = [(1, 100, 30 / 365, 0.25, 1), (1, 100, 30 / 365, 0.25, -1)]
calendar = [(-1, 100, 1 / 12, 0.20, 1), (1, 100, 0.25, 0.20, 1)]
for label, legs in [("straddle", straddle), ("calendar", calendar)]:
    print(label, {n: round(float(x), 4) for n, x in zip(names, book(100.0, legs))})
# straddle: price 5.7174 delta 0.0286 gamma 0.1113 vega 0.2286 theta -0.0952
# calendar: price 1.6848 delta 0.0084 gamma -0.0292 vega 0.0841 theta 0.016
```

### Example 2: realized versus implied

Same straddle, and the stock realises 30% instead of 25%.
Delta-hedged continuously at the 30% vol, the P&L is deterministic: the straddle's value at 30% minus its cost, $6.860 - 5.717 = 1.143$ per straddle, which is vega times 5 points ($0.229 \times 5 = 1.14$).
Hedged at the 25% implied vol instead, the expected P&L is similar but path-dependent, $\int \tfrac12\Gamma S^2(\sigma_{real}^2 - \sigma_{imp}^2)\,dt$, larger if the variance is realised near the strike and close to expiry where gamma is high.

### Example 3: extracting an earnings move

Earnings is tomorrow.
The weekly expiry (10 trading days) trades at 60% vol, the next monthly (30 trading days) at 40%, and both span the event.
Total variances: $0.60^2 \times 10/252 = 0.014286$ and $0.40^2 \times 30/252 = 0.019048$.
Subtracting removes the event: $\sigma_b^2 = (0.019048 - 0.014286) \times 252/20 = 0.06$, so the ex-event vol is 24.5%.
The event variance is $m^2 = 0.014286 - 0.06 \times 9/252 = 0.012143$, so $m = 11.0\%$ and the expected absolute move is $11.0\% \times 0.798 = 8.8\%$.
On a 100 stock the front ATM straddle costs 9.53.
If the stock does not move, it is worth 3.69 the next day at 24.5% vol with nine days left: the vol crush costs 5.84.
The holder breaks even on a move of about 9.4, so buy it only if you think the name moves more than 9.4% more often than the market implies.

### Example 4: a 25-delta risk reversal

Three months, $S = 100$, $r = 0$; 25-delta put at 24% vol, 25-delta call at 18%.
Strikes: put 92.89, call 106.69.
Buy the call (1.284) and sell the put (1.903): a credit of 0.619.
Greeks: delta $+0.50$, vega exactly zero (with $r = 0$, a 25-delta call and put share $\lvert d_1\rvert$ and so have equal vega, 0.159 each per point), vanna $+0.021$ delta per vol point.
If skew steepens with the put vol up 1 and the call vol down 1, the position loses $2 \times 0.159 = 0.317$.
If spot drops 5 with vols sticky by strike, it loses 2.48, so the skew view comes with a large delta that must be hedged with 0.5 of stock per risk reversal to isolate the skew.
Desks quote and hedge risk reversals delta-hedged for exactly this reason.

### Example 5: a calendar spread and weighted vega

$S = K = 100$, 20% vol, $r = 0$: sell the one-month call (2.303), buy the three-month call (3.988), cost 1.685.
Greeks: vega $+0.084$ per point, gamma $-0.029$, theta $+0.016$ per day.
A parallel 1-point rise in vol makes 0.084.
But if the one-month vol rises $\sqrt{3} = 1.73$ points while the three-month rises 1 (moves proportional to $1/\sqrt{T}$), the P&L is $-0.0002$, essentially zero: ATM vega scales with $\sqrt T$, so the vega ratio is exactly 1.73 and one-for-one ATM calendars are flat in weighted vega.
The calendar is really a short-gamma, long-theta position with a bet that the term structure steepens, not a long-vol trade.

### Example 6: long wings through a vega-neutral fly

Three months, flat 20% vol: the 25-delta strangle (strikes 93.95 and 107.51) has vega 0.318 per point and volga $+0.0072$ per point squared; the ATM straddle has vega 0.398 and volga essentially zero.
Buy 1.254 strangles per straddle sold to be vega-neutral.
A parallel vol move of $-5$ or $+5$ points makes $+0.144$ or $+0.094$: the position is long volga, a bet that vol-of-vol (and hence the smile's wings) is underpriced.
This is the FX "butterfly" trade, and why the quoted butterfly measures the market price of wings.

## Pitfalls

- Buying a straddle because "something will happen"; the straddle already prices the expected move, and the question is whether realized will exceed implied.
- Treating a calendar as a long-vol trade; it is short gamma, and a sharp move near the front expiry loses even if implied vols rise.
- Aggregating vega across expiries as if vols moved in parallel; use weighted vega or vega by bucket.
- Trading a risk reversal unhedged and calling the P&L "skew"; most of it is the 0.5 delta.
- Forgetting the vol crush on event trades, and measuring the implied move with the whole front-expiry straddle when part of it is ordinary diffusive vol.
- Selling iron condors or ratio spreads for "high probability of profit"; the payoff distribution is negatively skewed and the premium is compensation for it.
- Quoting break-even moves in calendar-day vol while hedging only on trading days (or vice versa); weekends matter for theta.

## Interview questions

> [!question]- deriv-strat-straddle-breakeven | A 30-calendar-day ATM straddle on a 100 stock at 25% vol ($r = 0$) costs about 5.72. What are the break-evens and the daily break-even move?
> Expiry break-evens 94.28 and 105.72; the delta-hedged daily break-even is about $25/16 = 1.56\%$ per trading day (1.31% per calendar day).
> The daily figure comes from $\tfrac12\Gamma S^2 x^2 = -\Theta$, which gives $x = \sigma\sqrt{\Delta t}$.

> [!question]- deriv-strat-straddle-vs-strangle | Why would you buy a strangle instead of a straddle?
> It is cheaper and has more volga (long wings), so it pays more on large moves per unit premium and gains if the smile's wings richen; the cost is lower gamma near the money and a wider break-even.
> It expresses a tail-move or vol-of-vol view rather than a pure realized-vol view.

> [!question]- deriv-strat-butterfly-greeks | What are the Greeks of a long call butterfly with spot at the body close to expiry?
> Delta near zero, short gamma, short vega, long theta: it profits if the stock pins near the body.
> Far from expiry the same butterfly is nearly Greek-neutral; the short-gamma profile sharpens as expiry approaches.

> [!question]- deriv-strat-calendar-greeks | What are you long and short in a long ATM calendar spread (short near, long far)?
> Long vega, short gamma, long theta.
> You profit if the stock stays still and far-dated vol holds or rises relative to near-dated vol; a big move near the short expiry hurts.

> [!question]- deriv-strat-weighted-vega | Why do desks use weighted vega, and what does it imply for a 1-for-1 ATM calendar?
> Short-dated vol moves more than long-dated, roughly in proportion to $1/\sqrt{T}$, so raw vega overstates the risk in long-dated options.
> ATM vega scales with $\sqrt{T}$, so under that rule a 1-for-1 ATM calendar has about zero weighted vega.

> [!question]- deriv-strat-risk-reversal-exposure | What does a long 25-delta risk reversal (long call, short put) expose you to?
> Roughly 0.5 delta, near-zero vega and positive vanna: after hedging delta it is a long-skew position that gains when call vols rise relative to put vols.
> With zero rates the two 25-delta options have exactly equal vega, so the parallel vega is zero.

> [!question]- deriv-strat-vega-neutral-fly | How do you trade the wings of the smile without taking a view on the level of vol?
> Buy OTM strangles and sell ATM straddles in a vega-neutral ratio (about 1.25 strangles per straddle at 25-delta, three months, 20% vol).
> The package is long volga, gaining on large vol moves in either direction, which is what the quoted butterfly prices.

> [!question]- deriv-strat-event-variance | Front expiry (10 trading days) at 60% and next expiry (30 days) at 40%, both spanning earnings. What is the ex-event vol and the implied event move?
> Ex-event vol 24.5%, event-day standard deviation 11.0%, expected absolute move about 8.8%.
> Solve $\sigma_i^2 T_i = \sigma_b^2(T_i - 1/252) + m^2$ for both expiries: $\sigma_b^2 = 0.06$ and $m^2 = 0.0121$.

> [!question]- deriv-strat-vol-crush | Why can a long straddle lose money over earnings even when the stock moves?
> The front implied vol collapses to the ex-event level after the announcement, so the straddle loses its event premium; it only profits if the move exceeds the implied move.
> In the worked example the straddle drops from 9.53 to 3.69 with no move, and the break-even is about a 9.4% move.

> [!question]- deriv-strat-gamma-vs-vega-tenor | Which options would you trade to express a view on realized vol, and which for implied vol?
> Short-dated options for realized vol (gamma is large, scaling like $1/\sqrt T$), long-dated options for implied vol (vega is large, scaling like $\sqrt T$).
> A trader with a view that realized vol will pick up but implied will stay flat buys front-month straddles, not one-year ones.

> [!question]- deriv-strat-realized-vs-implied-pnl | You buy a one-month straddle at 25% vol and delta-hedge; the stock realises 30%. Roughly what do you make?
> About vega times 5 points, $0.229 \times 5 \approx 1.14$ per straddle (exactly the Black-Scholes value difference when hedged at the realized vol).
> Hedged at implied vol, the expected P&L is similar but path-dependent: $\int \tfrac12\Gamma S^2(\sigma_{real}^2 - \sigma_{imp}^2)\,dt$.

> [!question]- deriv-strat-short-condor-risk | A strategy sells iron condors every month and wins 85% of the time. What is the catch?
> The P&L is negatively skewed: small frequent gains and rare losses up to the wing width; the high win rate is exactly what the premium pays for.
> Judge it by expected value net of the variance risk premium and by tail size, not by win rate.

> [!question]- deriv-strat-collar | What is a zero-cost collar and what exposure does it leave?
> Long stock, long OTM put, short OTM call with premiums offsetting: downside floored at the put strike, upside capped at the call strike.
> In vol terms the holder is short a risk reversal, so with equity skew the call strike is typically closer to spot than the put strike for zero cost.

## In this repo and SDE-Interview-Prep

- Prev: [Exotic Options](12-Exotic-Options.md). Next: [Variance Swaps and Volatility Products](14-Variance-Swaps-and-Volatility-Products.md).
- Greeks behind these tables: [The Greeks](05-The-Greeks.md); the smile being traded: [Implied Volatility and the Smile](07-Implied-Volatility-and-the-Smile.md).

## Further reading

- Sheldon Natenberg, *Option Volatility and Pricing*, chapters on spreads, volatility spreads and risk considerations.
- Euan Sinclair, *Volatility Trading*, chapters on hedging, event volatility and trade sizing.
- John Hull, *Options, Futures, and Other Derivatives*, chapter on trading strategies involving options.
- Jim Gatheral, *The Volatility Surface: A Practitioner's Guide*, on skew and term-structure dynamics.
