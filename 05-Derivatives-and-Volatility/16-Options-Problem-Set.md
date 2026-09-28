---
type: problem-set
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [delta-hedging-and-gamma-scalping, option-strategies-and-volatility-trading]
est_hours: 8
sources: [Sheldon Natenberg - Option Volatility and Pricing, Xinfeng Zhou - A Practical Guide to Quantitative Finance Interviews (Chapter 6 finance), Joshi Denson and Downes - Quant Job Interview Questions and Answers (options chapter), Emanuel Derman and Michael Kamal (1999) - When you cannot hedge continuously - the corrections of Black-Scholes - Risk 12(1), John Hull - Options Futures and Other Derivatives]
---

# Options Problem Set

## TL;DR

- Options interviews at market makers are rapid-fire: parity and arbitrage, Greek signs and shapes, mental prices, and hedged P&L. Say the rule, compute, then sanity-check with a bound or a limit.
- Parity and the strike-arbitrage conditions (monotone, slope within a discount factor, convex) catch almost every "is there an arbitrage" question; always ask about dividends, borrow and American exercise.
- Mental pricing runs on $0.4\,\sigma S\sqrt{T}$ for ATM options, $0.4 S\sqrt T$ for vega per unit vol, $0.4/(S\sigma\sqrt T)$ for gamma, and the rule of 16.
- Hedged P&L is $\tfrac12\Gamma\,dS^2 + \Theta\,dt + \mathcal V\,d\sigma + \text{vanna}\,dS\,d\sigma$; Taylor is fine for a day's move and misleading for a gap.
- Surface questions reduce to three ideas: total variance must increase with maturity, the density must be non-negative, and smile dynamics (sticky strike, delta or local vol) change deltas and P&L attribution.

## Learning objectives

- Answer rapid options questions: parity arbitrage, Greeks signs, mental pricing, hedged P&L.

## Core concepts

A compact toolkit; derivations are in the linked notes.

Parity and bounds ([Option Payoffs and Put-Call Parity](02-Option-Payoffs-and-Put-Call-Parity.md)):

- $C - P = S e^{-qT} - K e^{-rT}$; for American options on a non-dividend stock, $S - K \le C - P \le S - K e^{-rT}$.
- $\max(Se^{-qT} - Ke^{-rT}, 0) \le C \le S e^{-qT}$, $\max(Ke^{-rT} - Se^{-qT}, 0) \le P \le K e^{-rT}$, American put $\ge K - S$.
- Strike arbitrage: $C(K)$ non-increasing, $0 \le C(K_1) - C(K_2) \le (K_2 - K_1)e^{-rT}$, and convex: $(K_3 - K_2)C_1 - (K_3 - K_1)C_2 + (K_2 - K_1)C_3 \ge 0$.

Black-Scholes Greeks with $r = q = 0$ ([The Greeks](05-The-Greeks.md)):

| Greek | Formula | ATM approximation | Shape |
| :--- | :--- | :--- | :--- |
| Price | $S N(d_1) - K N(d_2)$ | $0.4\,\sigma S\sqrt T$ | |
| Delta | $N(d_1)$, put $N(d_1) - 1$ | $0.5 + 0.2\,\sigma\sqrt T$ | S-curve, steepens near expiry |
| Gamma | $\varphi(d_1)/(S\sigma\sqrt T)$ | $0.4/(S\sigma\sqrt T)$ | peaks just below the strike, at $K e^{-1.5\sigma^2 T}$ |
| Vega | $S\varphi(d_1)\sqrt T$ | $0.4\,S\sqrt T$ per unit vol | peaks near ATM, grows like $\sqrt T$ |
| Theta | $-S\varphi(d_1)\sigma/(2\sqrt T)$ | $-0.2\,S\sigma/\sqrt T$ per year | most negative ATM near expiry |
| Vanna | $-\varphi(d_1)d_2/\sigma$ | $\approx 0$ | positive for OTM calls, negative for OTM puts |
| Volga | $\text{vega}\cdot d_1 d_2/\sigma$ | $\approx 0$ | positive in the wings |

Rules of thumb: daily move $\approx \sigma/16$; straddle $\approx 0.8\,\sigma S\sqrt T$; gamma P&L $= \tfrac12\Gamma\,dS^2$ and the break-even move solves $\tfrac12\Gamma\,dS^2 = -\Theta_{day}$; theta and gamma of a delta-hedged option satisfy $\Theta = -\tfrac12\sigma^2 S^2\Gamma$ (with $r = 0$).
Hedging error with $N$ rebalances (Derman-Kamal): standard deviation $\approx \sqrt{\pi/4}\,\mathcal V\sigma/\sqrt N$.
Smile dynamics ([Implied Volatility and the Smile](07-Implied-Volatility-and-the-Smile.md)): $\Delta = \Delta_{BS} + \mathcal V\,\partial\sigma/\partial S$, with $\partial\sigma/\partial S = 0$ (sticky strike), $\approx -\partial\sigma/\partial K$ (sticky delta) or $\approx +\partial\sigma/\partial K$ (local vol).

## Worked examples

### Example 1: an unequal-strike butterfly arbitrage

Same-expiry calls: 90 at 13.00, 95 at 10.50, 110 at 2.00.
Check the obvious conditions first: prices fall with strike, and each call spread (2.50 for 5 points, 8.50 for 15 points) is below its width, so nothing yet.
Convexity with unequal spacing: the 95 strike sits at $\lambda = (110 - 95)/(110 - 90) = 0.75$ of the way from 110 to 90, so $C(95) \le 0.75\,C(90) + 0.25\,C(110) = 9.75 + 0.50 = 10.25$.
The market's 10.50 violates it by 0.25.
Trade: buy 3 of the 90 calls, sell 4 of the 95s, buy 1 of the 110s (weights $15 : 20 : 5$ divided by 5).
Cash: $-39 + 42 - 2 = +1.00$ received today.
Payoff: 0 below 90, rises with slope 3 to 15 at 95, falls with slope $-1$ to 0 at 110, and is flat at 0 above: never negative.
So you collect 1.00 for a non-negative payoff.

### Example 2: reading rates and dividends off parity

Stock 50, six-month 50-strike European options, $r = 4\%$: call 3.10, put 3.00.
Parity with discrete dividends: $C - P = S - \text{PV}(D) - K e^{-rT}$.
$K e^{-rT} = 50 e^{-0.02} = 49.010$, so $\text{PV}(D) = 50 - 49.010 - 0.10 = 0.89$.
The market is pricing about 0.89 of dividends (or, for a hard-to-borrow name, dividends plus borrow cost) over six months.
The same identity backs out a rate: with no dividends, $S = K = 100$, one year, call 12 and put 7, $e^{-r} = 0.95$ and $r = 5.13\%$, the box or conversion financing rate.

### Example 3: mental pricing with carry

Price a one-year ATM-spot call, $S = K = 100$, $\sigma = 20\%$, $r = 5\%$, in your head.
Split it into forward intrinsic value and time value: the forward is in the money by $S - K e^{-rT} = 4.88$, and roughly half of that carries into the call, 2.44 (delta near 0.5).
Time value is about $0.4\,\sigma S\sqrt T = 8.00$.
Total 10.44; Black-Scholes gives 10.45.
For a one-week straddle on a 200 stock at 32%: $0.8 \times 0.32 \times 200/\sqrt{52} = 7.10$, against the exact 7.08.

### Example 4: attributing a day's P&L on a hedged straddle

Long one 30-day 100-strike straddle at 25% vol, delta-hedged at the close.
Greeks: gamma 0.111, vega 0.229 per point, theta $-0.095$ per day, vanna 0.0011 per point and volga essentially zero (ATM).
Overnight spot falls to 97 and implied vol rises 2 points.
Taylor: gamma $\tfrac12 \times 0.111 \times 9 = 0.501$, vega $0.229 \times 2 = 0.457$, theta $-0.095$, vanna $0.0011 \times (-3) \times 2 = -0.007$, total $+0.856$ on the hedged position.
Full revaluation gives $+0.820$.
The 0.036 gap is higher order, chiefly zomma: ATM gamma scales like $1/\sigma$, so at the higher vol the move earns less gamma ($-\tfrac12 \times 9 \times 0.111/0.25 \times 0.02 = -0.040$).

### Example 5: when Taylor fails - a short straddle through a gap

Short the same straddle, delta-hedged, and the stock gaps up 8% overnight on news, vol unchanged.
Delta-gamma-theta predicts a loss of $\tfrac12 \times 0.111 \times 64 - 0.095 = 3.46$.
Full revaluation: the straddle goes from 5.717 to 9.020, and after the delta hedge gain ($0.029 \times 8$) the loss is 3.07.
Taylor overstates it because gamma falls as spot leaves the strike (0.056 at 108, half the ATM value); for larger gaps the loss becomes linear in the move, not quadratic.
The lesson for risk limits: use full revaluation on scenario grids, not Greeks, for moves beyond about one daily standard deviation.

### Example 6: how noisy is discrete hedging?

Sell a one-year ATM call at 20% vol on a 100 stock (price 7.97, vega 39.7 per unit vol), delta-hedge at 20% vol, and let the stock realise exactly 20%.
The P&L has mean zero but is not zero: Derman-Kamal gives a standard deviation of $\sqrt{\pi/4} \times 39.7 \times 0.2/\sqrt N$, which is 0.44 for daily hedging ($N = 252$) and 0.98 for weekly ($N = 52$).
Simulation agrees (0.44 and 0.96).
So even with perfect vol, a daily-hedged option has P&L noise of about 5.5% of its premium, and halving it needs four times the rebalancing (and four times the transaction costs).

```python
import numpy as np
from scipy.stats import norm

def call_delta_price(S, K, T, sigma):
    sd = sigma * np.sqrt(T)
    d1 = np.log(S / K) / sd + 0.5 * sd
    return S * norm.cdf(d1) - K * norm.cdf(d1 - sd), norm.cdf(d1)

def hedged_short_call(N, paths=20_000, S0=100.0, K=100.0, T=1.0, sigma=0.2, seed=1):
    """Sell a call at sigma, delta-hedge N times at sigma, realised vol = sigma, r = 0."""
    rng = np.random.default_rng(seed)
    dt = T / N
    price, pos = call_delta_price(S0, K, T, sigma)
    S = np.full(paths, S0)
    cash = price - pos * S
    pos = np.full(paths, pos)
    for i in range(1, N + 1):
        S = S * np.exp(-0.5 * sigma**2 * dt + sigma * np.sqrt(dt) * rng.standard_normal(paths))
        if i < N:
            new = call_delta_price(S, K, T - i * dt, sigma)[1]
            cash -= (new - pos) * S
            pos = new
    return cash + pos * S - np.maximum(S - K, 0.0)

vega = 100 * norm.pdf(0.1)                        # ATM vega per unit vol, S = 100, T = 1
for N in (52, 252):
    pnl = hedged_short_call(N)
    print(N, round(pnl.mean(), 3), round(pnl.std(), 3), round(np.sqrt(np.pi / 4) * vega * 0.2 / np.sqrt(N), 3))
# 52: mean 0.01, sd 0.961 vs 0.976; 252: mean -0.002, sd 0.44 vs 0.443
```

## Pitfalls

- Calling an arbitrage before checking dividends, borrow, early exercise and whether the quotes are tradeable (bid versus offer, not mids).
- Checking only equally spaced butterflies; with unequal strikes use the weighted condition.
- Quoting ATM approximations for ATM-spot options with large rates or dividends; add half the forward intrinsic value.
- Applying delta-gamma P&L to large gaps; gamma changes along the move and Taylor overstates losses for short straddles far from the strike.
- Mixing units: vega per unit vol versus per vol point, theta per year versus per calendar or trading day, gamma per dollar versus per 1% move.
- Forgetting that the delta to hedge depends on the smile dynamics you assume.
- Giving a Greek's sign without stating long or short, call or put, and where spot is relative to the strike.

## Interview questions

### Parity and arbitrage

> [!question]- deriv-ps-parity-implied-rate | $S = K = 100$, one year, no dividends; the European call is 12 and the put is 7. What interest rate is implied?
> About 5.13%.
> Parity gives $C - P = S - K e^{-rT}$, so $5 = 100 - 100e^{-r}$, $e^{-r} = 0.95$, $r = -\ln 0.95$.

> [!question]- deriv-ps-parity-implied-dividend | Stock 50, six-month 50-strike call 3.10 and put 3.00, $r = 4\%$. What dividends are priced?
> A present value of about 0.89.
> $\text{PV}(D) = S - K e^{-rT} - (C - P) = 50 - 49.01 - 0.10$; for a hard-to-borrow name this number also contains the borrow cost.

> [!question]- deriv-ps-call-above-stock | A call trades above the stock price. What do you do?
> Sell the call and buy the stock: you pocket the difference and the stock covers any exercise.
> The upper bound $C \le S e^{-qT}$ holds because the share dominates the call payoff.

> [!question]- deriv-ps-put-spread-above-width | A European 100/110 put spread (long 110, short 100) costs 11 with positive rates. Arbitrage?
> Yes: sell it for 11; it pays at most 10 at expiry, worth at most $10e^{-rT}$ today.
> A spread can never cost more than the discounted strike gap.

> [!question]- deriv-ps-longer-put-cheaper | Can a longer-dated European put be cheaper than a shorter-dated one with the same strike?
> Yes, when it is deep in the money and rates are positive: with $S = 20$, $K = 100$, $r = 5\%$, $\sigma = 20\%$ the one-year put is 75.12 and the two-year put 70.48.
> The put is close to $K e^{-rT} - S$, which falls with $T$; American puts cannot show this because they can be exercised.

> [!question]- deriv-ps-unequal-fly-arbitrage | Calls at 90, 95, 110 trade at 13, 10.5, 2. Is there an arbitrage, and how do you trade it?
> Yes: convexity requires $C(95) \le 0.75 \times 13 + 0.25 \times 2 = 10.25$.
> Buy 3 90-calls, sell 4 95-calls, buy 1 110-call: receive 1.00 today for a payoff that is never negative.

> [!question]- deriv-ps-digital-bounds-from-spreads | Bound the price of a digital call at $K$ using call spreads with strike step $h$.
> $\frac{C(K) - C(K + h)}{h} \le D(K) \le \frac{C(K - h) - C(K)}{h}$.
> The right-hand spread pays at least the digital in every state and the left-hand one at most, so no-arbitrage sandwiches the digital.

> [!question]- deriv-ps-american-put-below-intrinsic | An American put with strike 100 trades at 8 while the stock is at 90. What do you do?
> Buy the put and the stock, and exercise immediately: pay 98, receive 100, lock in 2.
> An American option can never trade below its intrinsic value.

### Greeks signs and shapes

> [!question]- deriv-ps-gamma-peak-spot | Where, as a function of spot, is a vanilla option's gamma highest?
> Slightly below the strike, at $S = K e^{-(r - q + 1.5\sigma^2)T}$; for $K = 100$, $\sigma = 20\%$, one year, zero rates, at about 94.2.
> Setting $\partial\ln\Gamma/\partial S = 0$ gives $d_1 = -\sigma\sqrt T$; near expiry the peak converges to the strike.

> [!question]- deriv-ps-positive-theta-long-option | Can a long option have positive theta?
> Yes: a deep in-the-money European put with positive rates (it drifts up toward $K e^{-r\tau}$ as time passes) and a deep in-the-money European call on a high-dividend-yield stock.
> Near the money, long options always pay theta.

> [!question]- deriv-ps-atm-vega-tenor-ratio | How does the vega of a one-year ATM option compare with a three-month ATM option on the same stock?
> About twice as large: ATM vega is $\approx 0.4\,S\sqrt T$, and $\sqrt{1/0.25} = 2$.
> Exactly 1.99 at 20% vol; long-dated options are vega instruments.

> [!question]- deriv-ps-gamma-near-expiry | What happens to gamma of ATM and OTM options as expiry approaches?
> ATM gamma blows up like $1/\sqrt T$, OTM and ITM gamma collapse to zero.
> The payoff kink becomes concentrated at the strike, which is where pin risk comes from.

> [!question]- deriv-ps-call-put-delta-gap | How are the call and put deltas at the same strike related?
> $\Delta_C - \Delta_P = e^{-qT}$ (1 with no dividends).
> Differentiate parity $C - P = S e^{-qT} - K e^{-rT}$ with respect to $S$; so a 30-delta call pairs with a $-70$-delta put.

> [!question]- deriv-ps-otm-call-vanna-sign | What is the sign of vanna for an OTM call, and what does it mean?
> Positive: when implied vol rises, the OTM call's delta rises toward 0.5 (and its vega rises with spot).
> OTM puts have negative vanna; ATM vanna is near zero.

> [!question]- deriv-ps-volga-atm-vs-wings | Where is volga positive, and why is ATM volga near zero?
> Volga $= \text{vega}\cdot d_1 d_2/\sigma$ is positive in both wings (where $d_1$ and $d_2$ share a sign) and near zero ATM, where $d_1 d_2 \approx 0$.
> ATM option prices are almost linear in vol, OTM prices are convex in vol, which is why wings carry a vol-of-vol premium.

> [!question]- deriv-ps-digital-delta-shape | Sketch the delta and gamma of a digital call against spot.
> Delta is a bump peaking near the strike (it is the density-like $e^{-rT}\varphi(d_2)/(S\sigma\sqrt T)$), and gamma is positive below the strike and negative above.
> Close to expiry both explode at the strike, which is why digitals are risk-managed as tight call spreads.

> [!question]- deriv-ps-charm-otm-call | Spot unchanged, what happens to the delta of an OTM call and an ITM call as time passes?
> The OTM call's delta decays toward 0 and the ITM call's toward 1 (charm).
> Less time means less chance to cross the strike, so the delta converges to the expiry indicator.

> [!question]- deriv-ps-futures-option-rho | What is rho for a European option on a futures contract, priced with Black-76?
> $-T\,V$ for both calls and puts: the price is $e^{-rT}$ times a function of the futures price, so a higher rate only discounts it more.
> Unlike stock options, the forward is the quoted future and does not move with $r$ in this sensitivity.

### Mental pricing

> [!question]- deriv-ps-mental-atm-40-vol | Price a one-year ATM call on a 50 stock at 40% vol with zero rates.
> About 8.0: $0.4 \times 0.40 \times 50 \times 1$.
> Exact Black-Scholes is 7.93; the approximation drifts high as $\sigma\sqrt T$ grows.

> [!question]- deriv-ps-mental-weekly-straddle | A 200 stock has 32% implied vol. What is a one-week ATM straddle worth?
> About 7.1: $0.8 \times 0.32 \times 200/\sqrt{52}$.
> Exact is 7.08, pricing an expected absolute move of about 3.5%.

> [!question]- deriv-ps-mental-atm-digital | One-year ATM digital call, 20% vol, zero rates: price?
> About 0.46.
> It is $N(d_2) = N(-\sigma\sqrt T/2) \approx 0.5 - 0.4 \times 0.1$; any skew adds $-\text{vega}\,\partial\sigma/\partial K$, which raises it for equity skew.

> [!question]- deriv-ps-mental-atm-vega | Vega of a one-year ATM option on a 100 stock?
> About 0.40 per vol point: $0.4\,S\sqrt T/100$.
> Exact at 20% vol is 0.397.

> [!question]- deriv-ps-mental-atm-gamma | Gamma of a one-year ATM option on a 100 stock at 20% vol?
> About 0.02 per dollar: $0.4/(S\sigma\sqrt T) = 0.4/20$.
> Exact is 0.0198; a 1% move changes delta by about 0.02.

> [!question]- deriv-ps-mental-atm-theta | Theta of a one-year ATM call on a 100 stock at 20% vol, zero rates?
> About $-4$ per year: $-S\varphi(0)\sigma/(2\sqrt T) = -100 \times 0.4 \times 0.2/2$, so about $-0.011$ per calendar day or $-0.016$ per trading day.
> Consistent with $\Theta = -\tfrac12\sigma^2S^2\Gamma = -0.5 \times 0.04 \times 10^4 \times 0.02 = -4$.

> [!question]- deriv-ps-mental-vol-bump | A one-year ATM call on 100 is worth about 8 at 20% vol. What is it worth at 22%?
> About 8.8: vega is about 0.40 per point, so two points add 0.80.
> Exact change is 0.79; ATM prices are nearly linear in vol.

> [!question]- deriv-ps-mental-atm-spot-rates | One-year ATM-spot call, $S = 100$, $\sigma = 20\%$, $r = 5\%$: price in your head.
> About 10.44: time value $0.4 \times 0.2 \times 100 = 8.0$ plus half the forward intrinsic $0.5 \times (100 - 95.12) = 2.44$.
> Black-Scholes gives 10.45.

### Hedged P&L

> [!question]- deriv-ps-gamma-theta-day | Your hedged book has gamma of 5,000 shares per dollar and theta of $-6{,}000$ per day. The stock moves 2 dollars. P&L?
> About $+4{,}000$: gamma P&L $\tfrac12 \times 5{,}000 \times 2^2 = 10{,}000$ minus 6,000 of theta.
> Vega and higher-order terms are ignored.

> [!question]- deriv-ps-book-breakeven-move | A 50 stock; your book has gamma 10,000 shares per dollar and theta $-5{,}000$ per day. What move do you need to break even?
> 1 dollar, a 2% move: $\tfrac12 \times 10{,}000 \times x^2 = 5{,}000$ gives $x = 1$.
> If the stock's daily standard deviation is below 2% (annual vol below about 32%), the book loses on average.

> [!question]- deriv-ps-discrete-hedge-noise | You sell a one-year ATM call at 20% vol on a 100 stock and hedge daily; realized vol is exactly 20%. What is the standard deviation of your P&L?
> About 0.44 (5.5% of the 7.97 premium), from $\sqrt{\pi/4}\,\mathcal V\sigma/\sqrt N$ with vega 39.7 and $N = 252$.
> Weekly hedging roughly doubles it to about 0.98; the error falls only like $1/\sqrt N$.

> [!question]- deriv-ps-hedge-at-which-vol | Should you delta-hedge at implied vol or at your forecast of realized vol?
> At realized vol the final P&L is locked in (value at realized minus premium) but the mark-to-market path is noisy; at implied vol the P&L accrues smoothly but its total depends on where spot realises variance.
> The expected P&L is roughly the same either way if your forecast is right; traders usually hedge at implied because it keeps daily P&L attribution clean.

> [!question]- deriv-ps-sold-vol-pnl | You sell a 30-day ATM straddle on 100 at 25% vol and hedge; the stock realises 20%. Roughly what do you make?
> About 1.14 per straddle: vega 0.229 per point times 5 points.
> Exactly the Black-Scholes straddle at 25% minus at 20% if you hedge at the realized vol.

> [!question]- deriv-ps-short-straddle-gap | You are short a delta-hedged 30-day ATM straddle (gamma 0.111) and the stock gaps 8%. Is $\tfrac12\Gamma\,dS^2$ a good estimate of the loss?
> No, it overstates it: Taylor gives 3.46 including a day's theta, full revaluation 3.07.
> Gamma halves by the time spot reaches 108, and for bigger gaps the loss grows linearly, so risk scenarios should use full revaluation.

> [!question]- deriv-ps-vanna-pnl | Your hedged book is long vanna of 2,000 shares per vol point. Spot falls 3 dollars and implied vol rises 2 points. What is the vanna P&L?
> $-12{,}000$: vanna P&L is $\text{vanna}\times dS \times d\sigma = 2{,}000 \times (-3) \times 2$.
> With equity spot-vol correlation strongly negative, long vanna bleeds systematically, which is why it trades at a price.

> [!question]- deriv-ps-weekend-theta | Should a short-gamma book collect three days of theta over a weekend?
> In calendar-time pricing yes, but little variance is realised over the weekend, so markets price in trading-time: implied vols are lowered into Friday (or theta is spread over trading days).
> Pricing the weekend theta as if it were free would overpay the short and misstate the break-even move.

### Strategies

> [!question]- deriv-ps-butterfly-profile | A 95/100/105 call butterfly costs 1.20. Maximum profit, maximum loss and break-evens at expiry?
> Maximum profit 3.80 at 100, maximum loss 1.20 outside 95-105, break-evens 96.20 and 103.80.
> The payoff is a tent of height 5 at 100.

> [!question]- deriv-ps-call-spread-as-digital | How do you replicate a digital paying 100 if the stock ends above 100 using listed calls?
> Buy 50 of the 99 calls and sell 50 of the 101 calls: the spread pays 0 below 99, 100 above 101 and ramps in between.
> A seller of the digital hedges conservatively by buying the 98/100 spread (50 lots), which pays at least as much as the digital in every state, and charges for the difference.

> [!question]- deriv-ps-ratio-spread-risk | You buy one 100 call and sell two 110 calls for a small credit. Where is your risk?
> Unlimited on the upside: above 110 the position is net short one call and loses 1 per point, crossing zero around 120 plus the credit.
> Maximum profit is 10 plus the credit at 110; the trade is short upside vol and short gamma near 110.

> [!question]- deriv-ps-pin-risk | What is pin risk, and who bears it?
> At expiry with spot right at a short strike, you do not know whether you will be assigned, so you do not know your stock position on Monday.
> Conversion and reversal traders and anyone short options at that strike bear it; they reduce it by closing the strike before expiry.

> [!question]- deriv-ps-synthetic-stock | Construct a synthetic long stock from options, and say what can make it differ from the real stock.
> Long call, short put at the same strike, plus a bond paying $K$ (lending $K e^{-rT}$).
> It misses dividends and borrow, which sit in the option prices, and American early exercise can break it on single stocks.

> [!question]- deriv-ps-straddle-direction | Is a long straddle delta-neutral when first bought ATM-spot, and does it stay neutral?
> Slightly positive delta at ATM-spot (a call delta above 0.5 with a put delta above $-0.5$), exactly neutral only at the delta-neutral strike, and it becomes directional as soon as spot moves (gamma).
> A 30-day 25%-vol ATM straddle has delta about $+0.03$.

### Vol surface

> [!question]- deriv-ps-atm-vol-after-drop | Skew is $-0.3$ vol points per strike point. Spot drops from 100 to 95. Where is the new ATM vol under sticky strike, sticky delta and local vol?
> Up 1.5 points under sticky strike, unchanged under sticky delta, up about 3 points under local vol.
> Sticky strike reads the old smile at 95; local vol moves ATM vol by about twice the skew.

> [!question]- deriv-ps-total-variance-rule | Which quantity must be non-decreasing in maturity across a vol surface?
> Total implied variance $\sigma^2(k, T)\,T$ at fixed forward moneyness.
> Otherwise a calendar spread struck at the same forward moneyness has negative cost for a non-negative payoff.

> [!question]- deriv-ps-negative-density | A fitted smile produces a negative butterfly price at one strike. What does that mean?
> The implied risk-neutral density is negative there, so the surface admits a static arbitrage (buy the butterfly for a credit).
> Fix the parametrisation (for example SVI with no-butterfly-arbitrage conditions) rather than trading on a fitting artefact.

> [!question]- deriv-ps-crisis-term-structure | What does the ATM vol term structure look like in a sell-off, and why?
> Inverted: short-dated vol jumps far more than long-dated, because vol mean-reverts and the market prices the stress as temporary.
> Long-dated vega therefore hedges short-dated vega poorly, which is why vega is bucketed or weighted by $1/\sqrt T$.

> [!question]- deriv-ps-local-vs-implied-skew | Implied skew is $-0.2$ vol points per strike point near the money. What is the local-vol skew?
> About $-0.4$, twice the implied skew.
> Implied vol is roughly the average of local vol between spot and strike, so it moves half as fast in strike.

> [!question]- deriv-ps-flat-smile-meaning | What would a flat implied vol smile across strikes mean?
> That the market's risk-neutral distribution of $\ln S_T$ is normal (lognormal prices), with no skewness and no excess kurtosis.
> Real equity markets never show it; the smile is the market's correction to Black-Scholes.

> [!question]- deriv-ps-rich-skew-trade | You think index put skew is too steep relative to realized spot-vol correlation. What do you trade?
> Buy the risk reversal (sell OTM puts, buy OTM calls) and delta-hedge, or sell put spreads versus ATM on a vega-neutral basis.
> You are paid if skew flattens or if realized spot-vol behaviour is milder than the skew implies; the risk is a crash, so size to the tail.

## In this repo and SDE-Interview-Prep

- Prev: [Dispersion and Correlation Trading](15-Dispersion-and-Correlation-Trading.md).
- Topic notes behind these questions: [Delta Hedging and Gamma Scalping](06-Delta-Hedging-and-Gamma-Scalping.md), [Option Strategies and Volatility Trading](13-Option-Strategies-and-Volatility-Trading.md), [Variance Swaps and Volatility Products](14-Variance-Swaps-and-Volatility-Products.md).

## Further reading

- Sheldon Natenberg, *Option Volatility and Pricing*.
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*
- Joshi, Denson and Downes, *Quant Job Interview Questions and Answers*
- E. Derman and M. Kamal (1999), "When you cannot hedge continuously: the corrections of Black-Scholes", *Risk* 12(1).
- John Hull, *Options, Futures, and Other Derivatives*.
