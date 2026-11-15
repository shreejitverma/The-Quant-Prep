---
type: concept
track: [quant-trader]
tier: core
status: solid
prereqs: [hedging-and-risk-for-market-makers, implied-volatility-and-the-smile]
est_hours: 5
sources: [Natenberg (2015) Option Volatility and Pricing 2nd edition. McGraw-Hill, Sinclair (2013) Volatility Trading 2nd edition. Wiley, Hull (2021) Options Futures and Other Derivatives 11th edition. Pearson, Cartea Jaimungal and Penalva (2015) Algorithmic and High-Frequency Trading. Cambridge University Press, Derman (1999) Regimes of volatility. Risk April 1999, Pool Stoll and Whaley (2008) Failure to exercise call options. Journal of Financial Markets 11(1) 1-35, OCC Rule 805, FINRA Rule 2360(b)(23), Cboe Exchange Rule 5.52]
---

# Options Market Making

## TL;DR

- An options market maker quotes in volatility: a fitted surface gives a theo vol per strike and expiry, Black-Scholes (or the relevant model) turns it into a price, and the width in vol points times vega gives the width in price.
- Delta is hedged almost immediately in the underlying or future; what the book actually carries is gamma, theta, vega by expiry, and skew risk, and quotes are leaned (surface shifted) to attract flow that reduces those.
- Every quote must be consistent across strikes, expiries and put-call parity, or a faster trader will arbitrage the chain against you.
- Expiration brings pin risk (not knowing whether short options near the strike will be assigned) and early-exercise decisions, especially calls before dividends and deep puts when rates are high.
- Around scheduled events, price the event as extra variance, widen and shrink size, and expect implied vol to collapse after the release.

## Learning objectives

- Quote an options chain from a volatility surface and theoretical edge.
- Manage portfolio Greeks, pin risk and expiration.
- Price and quote around events, and handle early exercise and dividends.

## Core concepts

### From surface to quotes

The pipeline for one option:

1. Forward: from the future, or from the underlying with rates, dividends and borrow; it is often implied from put-call parity on liquid strikes.
2. Theo vol: from a surface parameterised per expiry by level, skew and curvature (for example SVI), fitted to market mids and your views; see [Volatility Surface Construction](../05-Derivatives-and-Volatility/08-Volatility-Surface-Construction.md).
3. Theo price and Greeks from the pricing model (Black-Scholes-Merton for European, a tree or approximation for American exercise).
4. Width: a half-width in vol $\Delta\sigma$ converts to price through vega, $h \approx \text{vega} \times \Delta\sigma$, floored by costs:

$$
h \ge \text{fees} + |\Delta| \cdot h_{\text{underlying}} + \text{AS} + \text{min edge}.
$$

The $|\Delta| h_{\text{underlying}}$ term is the expected cost of delta-hedging the fill by crossing the underlying's spread.

5. Round to the tick: bids down, asks up, and check the result against the venue's market-maker obligations.
   As of November 2026, Cboe Options Rule 5.52 sets continuous-quoting obligations for Market-Makers' electronic quotes (time and series coverage, not a maximum width) and leaves bid/ask width requirements for open-outcry quotes to the exchange class by class (Rule 5.52(e)(2)).

Consistency constraints the quoter must enforce:

- Put-call parity: calls and puts at the same strike and expiry are quoted off one vol and one forward, otherwise conversions and reversals trade against you.
- No static arbitrage: call prices decreasing and convex in strike (no negative butterflies), total variance increasing in expiry (no calendar arbitrage).
- Cross-venue: the same option often lists on several exchanges, and a stale quote on one is picked off.

### Moving quotes with the underlying

Between surface refits, theo updates with the underlying through the Greeks:

$$
\Delta C \approx \Delta \cdot \Delta S + \tfrac{1}{2}\Gamma (\Delta S)^2 + \text{vega} \cdot \Delta\sigma(K; \Delta S).
$$

The last term depends on the smile dynamics you assume.

- Sticky strike: each strike keeps its vol, $\Delta\sigma = 0$.
- Sticky moneyness (sticky delta): the smile moves with the underlying, so after a move from $S_0$ to $S_1$ strike $K$ takes the vol that strike $K S_0/S_1$ had before; with a downward skew a rise in the stock raises every fixed strike's vol.

Derman (1999) describes markets switching between these regimes (and a third, sticky implied tree) rather than following one rule; the choice changes your effective delta, which is why desks measure and hedge a smile-adjusted delta.

### Portfolio Greeks and leaning

After delta hedging, the book's P&L over a short interval is approximately

$$
\text{P\&L} \approx \tfrac{1}{2}\Gamma S^2 \left( \frac{\Delta S}{S} \right)^2 + \Theta \, \Delta t + \sum_{\text{expiries}} \text{vega}_T \, \Delta\sigma_T + \text{edge from new fills}.
$$

For a delta-hedged option, gamma and theta offset: $\Theta \approx -\tfrac{1}{2}\Gamma S^2 \sigma_{\text{implied}}^2$, so long gamma earns when realised volatility exceeds implied; see [Delta Hedging and Gamma Scalping](../05-Derivatives-and-Volatility/06-Delta-Hedging-and-Gamma-Scalping.md).

Risk is bucketed because vols of different expiries do not move together:

- Vega by expiry bucket (front-month and back-month vols move by different amounts).
- Skew and curvature exposure (what happens if the 25-delta put vol rises relative to at-the-money).
- Gamma by expiry and near strikes, which becomes violent close to expiry.

The main tool is the quote itself.
If the book is short vega in one expiry, raise that expiry's vols by a small amount per unit of position, so your bid becomes the best and your offer less attractive; flow then reduces the exposure.
Beyond a limit, hedge directly with other options or spreads.

### Expiration and pin risk

Near expiry, gamma of at-the-money options explodes and theta concentrates.
At expiration, a short option whose strike is close to the closing price creates pin risk: you do not know until after the close whether you will be assigned, so you do not know your stock position over the weekend or overnight.
In US listed equity options (as of November 2026), OCC Rule 805(d) treats every expiring contract that is at least 0.01 in the money at the close as exercised unless the clearing member instructs otherwise.
Under FINRA Rule 2360(b)(23)(A) holders have until 5:30 p.m. ET on the expiration day to give exercise instructions, including instructions not to exercise an in-the-money option, so news after the 4:00 p.m. close can change who exercises.
Mitigations: reduce short near-the-money positions into expiry, buy back cheap short options, and hedge to the expected assignment.

### Early exercise and dividends

For American options on stock:

- A call is only worth exercising early just before an ex-dividend date.
  By put-call parity after the dividend, exercise the night before is optimal when

$$
D > K\left(1 - e^{-r\tau}\right) + P(K, \tau),
$$

  with $\tau$ the remaining time and $P$ the put at the same strike: the dividend beats the interest on the strike plus the put's insurance value.
- A put can be worth exercising early when deep in the money and rates are high.
  With no dividends before expiry, exercising beats holding the European put only if $K(1 - e^{-r\tau}) > C(K, \tau)$.
  That condition is necessary but not sufficient, because the American put is worth more than the European one, so the exercise boundary needs a tree.
  Example: $K = 40$, $r = 5\%$, vol 30%, 30 days.
  At $S = 35$ the interest on the strike (0.164) exceeds the call (0.093), yet a binomial tree values the American put at 5.018, above its 5.00 exercise value, so you hold; at $S = 34$ the tree value equals the 6.00 exercise value, so you exercise.

For a market maker the risk is the counterparty's decision.
If you are short in-the-money calls before an ex-date you should expect assignment; if you are long them and fail to exercise, you give away the dividend.
As of November 2026, OCC Rule 803 assigns exercise notices to clearing members at random under OCC's procedures, and FINRA Rule 2360(b)(23)(C) requires brokers to pass them on to customers first in first out or by random selection.
Assignments therefore land across all short positions in proportion on average, so a trader who buys and sells a large equal number of deep in-the-money calls and exercises the long side before the ex-date is assigned on only part of the short side, and keeps the dividends that non-exercising holders leave behind.
Pool, Stoll and Whaley (2008) found that more than half of the long positions that should have been exercised went unexercised, costing call holders over 491 million dollars over ten years, and that market makers captured most of it with these dividend spread trades.

### Events

A scheduled event (earnings, a central bank decision, a data release, a trial result) adds a jump.
Model it as extra variance on the event date:

$$
\sigma_{\text{implied}}^2 T = \sigma_{\text{base}}^2 T + \sigma_{\text{event}}^2,
$$

where $\sigma_{\text{event}}$ is the standard deviation of the one-day event move.
This produces the familiar kink in the term structure, lets you compare the market's implied move with the history of moves, and predicts the vol crush after the event.
Operationally: widen and shrink size into the release, pull or re-center at the release, and refit the surface immediately after.

## Worked examples

### Example 1: quoting one option

$S = 100$, $K = 105$, $T = 0.25$, $r = q = 0$, surface vol 25%.
Black-Scholes gives call theo 2.99, delta 0.372, gamma 0.0302, vega 0.189 per vol point, theta -0.026 per calendar day.
Quoting 24.5 / 25.5 vol gives 2.897 / 3.086, a price width of 0.19, which is vega times one vol point.
Rounded outward to a 0.05 tick (a tick size assumed for the example): bid down to 2.85, ask up to 3.10.
Check the floor: if hedging costs half a cent per share in the stock, $0.372 \times 0.005 \approx 0.002$ per share, small against the 0.125 half-width of the rounded market.

### Example 2: the underlying ticks up

The stock moves to 100.50.
Full reprice at 25%: theo 3.181, up 0.190; the Taylor estimate $0.372 \times 0.5 + \tfrac{1}{2} \times 0.0302 \times 0.25 = 0.190$ agrees.
If the skew slopes down at 0.2 vol points per dollar of strike and you assume sticky moneyness, the 105 strike now behaves like the $105 \times 100/100.5 \approx 104.5$ strike did, so its vol rises by about 0.1 point to 25.1%.
Theo becomes 3.201, a further 0.019 (vega times 0.1).
The two smile assumptions differ by about 10% of the move, which is exactly the kind of error a faster, better-calibrated competitor picks off.

### Example 3: portfolio Greeks and a lean

Book on a 100 stock, contract multiplier 100, rates zero, theta per calendar day:

| Position | Vol | Delta | Gamma | Vega | Theta/day |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Long 200 calls, K 100, 3 months | 26% | 0.526 | 0.0306 | 0.199 | -0.028 |
| Short 300 calls, K 105, 3 months | 25% | 0.372 | 0.0302 | 0.189 | -0.026 |
| Short 100 puts, K 95, 6 months | 28% | -0.360 | 0.0189 | 0.265 | -0.020 |

Aggregating (position times Greek times 100): delta +2,974 shares, gamma -484 shares per dollar, vega -4,336 dollars per vol point (-1,690 in 3 months, -2,646 in 6 months), theta +413 dollars per day.
Sell 2,974 shares to be delta flat.
The book is short gamma: a one-dollar move costs about $\tfrac{1}{2} \times 484 \times 1^2 \approx 242$ dollars before re-hedging, paid for by the 413 dollars of daily theta.
It is short vega mostly in 6 months, so lean: raise the 6-month vols by a fraction of a point to buy vega from customers, and less so in 3 months.

### Example 4: implied event move and vol crush

A stock at 100 reports earnings tomorrow; the 30-day option expiring after the report trades at 45% implied, and its normal (ex-event) vol is 25%.
Event variance $= (0.45^2 - 0.25^2) \times 30/365 \approx 0.0115$, so the implied one-day move has standard deviation $\approx 10.7\%$ and mean absolute move $\approx 10.7\% \times \sqrt{2/\pi} \approx 8.6\%$.
The at-the-money straddle costs 10.29 (close to $0.8\sigma\sqrt{T}S = 10.32$).
If the stock does not move, the next day it is worth 5.62 at 25% vol for 29 days: a 4.67 vol crush.
The market maker who sold the straddle wins if the realised move is smaller than priced; compare 8.6% with the stock's history of earnings moves before leaning either way.

### Example 5: pin risk

You are short 1,000 calls struck at 50 (100 shares each) and the stock closes at 50.02 on expiry Friday.
The calls are 0.02 in the money, so they will be auto-exercised unless holders say otherwise, but some holders may decide not to exercise after hearing news after the close.
You could be short anywhere from 0 to 100,000 shares on Monday.
A 2% gap is 1 dollar per share, so the unknown position is worth up to 100,000 dollars of P&L either way.
Buying back the calls before the close replaces that ambiguity with a known cost; compare the two before expiry, not after.

### Example 6: exercise before the dividend

A call with $K = 40$, stock at 50, a 0.50 dividend going ex tomorrow, 30 days to expiry, $r = 5\%$, vol 30%.
Interest on the strike $= 40(1 - e^{-0.05 \times 30/365}) \approx 0.164$; the 40 put after the dividend is worth about 0.007.
Threshold $0.171 < 0.50$, so exercise tonight.
Check directly: exercising is worth 10.00 now; holding gives a call worth about 9.67 on the 49.50 ex-dividend stock.
The 0.33 difference equals $0.50 - 0.171$.
If you are short these calls and not assigned, you keep 0.33 per share, which is why being assigned is the base case to plan for.

```python
from math import log, sqrt, exp, erf

def bs_call(S, K, T, vol, r=0.0):
    N = lambda x: 0.5 * (1 + erf(x / sqrt(2)))
    d1 = (log(S / K) + (r + 0.5 * vol * vol) * T) / (vol * sqrt(T))
    return S * N(d1) - K * exp(-r * T) * N(d1 - vol * sqrt(T))

bid, ask = bs_call(100, 105, 0.25, 0.245), bs_call(100, 105, 0.25, 0.255)
print(round(bid, 3), round(ask, 3))  # 2.897 3.086
```

## Pitfalls

- Quoting calls and puts off different forwards or vols, handing out conversions and reversals.
- Updating theo only through delta and forgetting the smile dynamics, so the effective delta is wrong.
- Aggregating vega across expiries into one number and missing a term-structure position.
- Treating theta as income rather than the price of short gamma.
- Carrying short near-the-money options into expiry without a plan for assignment.
- Forgetting ex-dividend dates and optimal early exercise on the calls you are short or long.
- Quoting normal width and size into a scheduled event, or failing to refit immediately after it.
- Ignoring the hedge cost $|\Delta| h_{\text{underlying}}$ when setting the minimum width on high-delta options.

## Interview questions

> [!question]- mm-options-vol-width-to-price | You quote an option 1 vol point wide and its vega is 0.19 per point. How wide is the market in price?
> About 0.19.
> Price width is vega times vol width, then rounded outward to the tick.

> [!question]- mm-options-surface-pipeline | Walk through how you produce a quote for one option.
> Forward from the future or implied from put-call parity, theo vol from the fitted surface, price and Greeks from the model, half-width from vol edge times vega floored by fees, hedge cost and adverse selection, then round outward.
> Finally check arbitrage consistency with neighbouring strikes, expiries and the put.

> [!question]- mm-options-put-call-consistency | Why must calls and puts at a strike be quoted off the same vol and forward?
> Otherwise put-call parity fails and someone trades the conversion or reversal against you risk-free.
> The call minus the put must equal the discounted forward minus the strike in every quote you show.

> [!question]- mm-options-sticky-strike-moneyness | The stock rises 0.50 and skew is -0.2 vol points per dollar of strike. How does a 105-strike call's vol change under sticky strike and sticky moneyness?
> Unchanged under sticky strike; up 0.1 point under sticky moneyness.
> Under sticky moneyness the strike now sits where the 104.5 strike was, which had 0.1 point more vol.

> [!question]- mm-options-lean-on-vega | You are short about 4,300 dollars of vega, mostly in 6 months. How do you use quotes to reduce it?
> Raise the 6-month vols slightly so your bids become the most attractive and your offers less so; customers then sell you vega.
> Lean more where the exposure is, and hedge with spreads once the lean would move you off the market.

> [!question]- mm-options-gamma-theta | A delta-hedged book has gamma of -484 shares per dollar and theta of +413 dollars a day. What is the trade-off?
> A one-dollar move costs about 242 dollars before re-hedging, and the theta pays for roughly a 1.3-dollar move per day.
> $\tfrac{1}{2}\Gamma(\Delta S)^2 = \Theta$ gives the break-even move $\sqrt{2 \times 413/484} \approx 1.31$.

> [!question]- mm-options-pin-risk | What is pin risk?
> Uncertainty at expiry about whether short options near the money will be assigned, which leaves your underlying position unknown until after the close.
> A gap over the weekend then hits a position you did not know you had.

> [!question]- mm-options-early-exercise-call | When is it optimal to exercise an American call on a dividend-paying stock early?
> Only just before an ex-dividend date, when the dividend exceeds the interest on the strike plus the value of the same-strike put: $D > K(1 - e^{-r\tau}) + P$.
> Example: $K = 40$, $D = 0.50$, interest 0.164 and put 0.007 means exercise.

> [!question]- mm-options-early-exercise-put | When can early exercise of an American put be optimal?
> Only when it is deep in the money: with no dividends to come, the interest on the strike $K(1 - e^{-r\tau})$ must exceed the same-strike call.
> That is necessary, not sufficient; a tree finds the boundary (with $K = 40$, 5% rates, 30% vol and 30 days, hold at $S = 35$ although $0.164 > 0.093$, exercise at $S = 34$).
> Higher rates and deeper moneyness make it more likely.

> [!question]- mm-options-event-variance | A 30-day option spanning earnings trades at 45% with base vol 25%. What one-day move is implied?
> A standard deviation of about 10.7%, mean absolute move about 8.6%.
> Event variance $= (0.45^2 - 0.25^2) \times 30/365 \approx 0.0115$; take the square root, and multiply by $\sqrt{2/\pi}$ for the mean absolute move.

> [!question]- mm-options-vol-crush | Why does the at-the-money straddle lose value after earnings even if the stock does not move?
> The event variance leaves the price once the event passes, so implied vol drops back to the base level.
> In the example the 30-day straddle falls from 10.29 to 5.62 with the stock unchanged.

> [!question]- mm-options-hedge-cost-floor | Why do high-delta options need a wider minimum quote than their vega suggests?
> Each fill is delta-hedged by crossing the underlying's spread, which costs about $|\Delta|$ times the underlying half-spread per share.
> Deep in-the-money options have little vega but nearly full delta, so this term dominates.

> [!question]- mm-options-dividend-capture-risk | You are short deep in-the-money calls the day before an ex-date. What should you expect?
> Assignment, and plan the position for it.
> Holders who exercise optimally will call the stock to capture the dividend; failing to be assigned is a windfall, not a plan.

> [!question]- mm-options-book-delta | Long 200 of the 100-strike calls (delta 0.526), short 300 of the 105-strike calls (0.372) and short 100 of the 95-strike puts (-0.360), multiplier 100. What delta hedge?
> Sell about 2,974 shares.
> $100 \times (200 \times 0.526 - 300 \times 0.372 + 100 \times 0.360) \approx 2{,}960$ with the rounded deltas; the unrounded deltas give 2,974.

> [!question]- mm-options-sticky-moneyness-theo | The 105 call (vega 0.189) is repriced after the stock rises from 100 to 100.50. How much more does theo rise under sticky moneyness than under sticky strike, with skew -0.2 vol points per dollar?
> About 0.019.
> The strike takes the vol of strike $105 \times 100/100.5 \approx 104.48$, about 0.1 point higher, and vega times 0.1 is 0.019: about 10% of the 0.190 move.

> [!question]- mm-options-dividend-give-up | Stock 50, call strike 40, dividend 0.50 going ex tomorrow, 30 days left, 5% rates, 30% vol. What does a holder lose by not exercising tonight?
> About 0.33 per share.
> Exercise is worth 10.00; the call held through the ex-date is worth about 9.67 on the 49.50 stock, and $0.50 - (0.164 + 0.007) = 0.33$.

## In this repo and The-Distinguished-Engineer

- Code: [`code/mm_07_options_market_making.py`](code/mm_07_options_market_making.py) prints and asserts every number on this page: option prices by Simpson quadrature of the payoff against the lognormal density (checked against the Black-Scholes closed form), Greeks by finite differences of those prices, the sticky-moneyness vol from the moneyness-equivalent strike, and American exercise by a binomial tree rather than the parity inequalities it tests.
  The snippet above prints the two quotes the script asserts.
- Related notes: [Volatility Surface Construction](../05-Derivatives-and-Volatility/08-Volatility-Surface-Construction.md), [Delta Hedging and Gamma Scalping](../05-Derivatives-and-Volatility/06-Delta-Hedging-and-Gamma-Scalping.md).

## Further reading

- Sheldon Natenberg, *Option Volatility and Pricing* (2nd edition, 2015).
- Euan Sinclair, *Volatility Trading* (2nd edition, 2013).
- John Hull, *Options, Futures, and Other Derivatives*, 11th edition (2021), chapter 11 (Properties of Stock Options: early exercise and dividends).
- Emanuel Derman (1999), Regimes of volatility, *Risk*, April 1999 (sticky strike, sticky delta and sticky implied tree).
- Veronika Krepely Pool, Hans R. Stoll and Robert E. Whaley (2008), Failure to exercise call options: an anomaly and a trading game, *Journal of Financial Markets* 11(1), 1-35.
- OCC Rules, Rule 803 (assignment of exercise notices) and Rule 805 (exercise by exception), and FINRA Rule 2360(b)(23) (exercise deadlines and allocation of assignments), both as of November 2026.
- Cboe Exchange Rules, Rule 5.52 (Market-Maker quoting obligations), as of November 2026.
- Related notes: [Implied Volatility and the Smile](../05-Derivatives-and-Volatility/07-Implied-Volatility-and-the-Smile.md), [The Greeks](../05-Derivatives-and-Volatility/05-The-Greeks.md), [Hedging and Risk for Market Makers](06-Hedging-and-Risk-for-Market-Makers.md), [Market Making P&L Attribution and Markouts](09-Market-Making-PnL-Attribution-and-Markouts.md).
