---
type: concept
track: [quant-trader, quant-research]
tier: advanced
status: solid
prereqs: [delta-hedging-and-gamma-scalping]
est_hours: 3
sources: [Carr and Madan (1998) - Towards a theory of volatility trading - in Volatility (Risk Books), Demeterfi Derman Kamal and Zou (1999) - A guide to volatility and variance swaps - Journal of Derivatives 6(4), Jim Gatheral - The Volatility Surface - A Practitioner's Guide (Wiley 2006), Cboe - VIX White Paper (Cboe Volatility Index methodology), Sebastien Bossu - Introduction to Variance Swaps - Wilmott (2006)]
---

# Variance Swaps and Volatility Products

## TL;DR

- A variance swap pays $N_{var}(\sigma_R^2 - K_{var})$, with $\sigma_R^2 = \tfrac{252}{n}\sum \ln^2(S_i/S_{i-1})$ in vol points squared; vega notional $N_{vega} = 2 K_{vol} N_{var}$ makes the P&L about $N_{vega}(\sigma_R - K_{vol})$ for small moves.
- It is replicated by a static strip of OTM options weighted $1/K^2$ plus a dynamic delta hedge: $K_{var} = \tfrac{2e^{rT}}{T}\left[\int_0^F \tfrac{P(K)}{K^2}dK + \int_F^\infty \tfrac{C(K)}{K^2}dK\right]$, which is $-\tfrac{2}{T}E_Q[\ln(S_T/F)]$.
- The $1/K^2$ weights make the portfolio's dollar gamma $S^2\Gamma$ constant in spot, so the hedged P&L accrues $\sigma^2$ wherever spot goes; with skew, rich OTM puts push $K_{var}$ above ATM vol.
- The VIX is the square root of a 30-day discretised variance swap rate on SPX options; it is not a vol swap, and a VIX future is not the forward VIX (Jensen: $E[\text{VIX}_T] \le \sqrt{\text{forward variance}}$).
- Vol swaps are not statically replicable and $K_{vol} < \sqrt{K_{var}}$ by the convexity adjustment $\approx \text{Var}(\sigma_R^2)/(8K_{var}^{3/2})$; jumps break the log-contract replication, which is why single-stock variance is capped.

## Learning objectives

- Replicate a variance swap with a strip of options (1/K^2 weights).
- Explain the VIX calculation and the convexity gap between vol and variance swaps.

## Core concepts

### The contract

Realized variance over $n$ daily returns, annualised and in vol points squared:

$$
\sigma_R^2 = \frac{252}{n}\sum_{i=1}^{n}\ln^2\!\frac{S_i}{S_{i-1}} \times 10^4.
$$

The mean is not subtracted, and the divisor is $n$, not $n - 1$.
The payoff at maturity is $N_{var}(\sigma_R^2 - K_{var})$, where $K_{var}$ is quoted as a vol, $K_{var} = K_{vol}^2$.
Trades are sized in vega notional, $N_{vega} = 2K_{vol}N_{var}$, because $\sigma_R^2 - K_{vol}^2 \approx 2K_{vol}(\sigma_R - K_{vol})$ near the strike.
Long variance is convex in realized vol: it gains more on a vol spike than it loses on a quiet period of the same size.

A seasoned swap at time $t$ is worth, per unit variance notional and before discounting,

$$
\frac{t}{T}\sigma_{R,0\to t}^2 + \frac{T - t}{T}K_{var}(t, T) - K_{var}.
$$

Variance is additive in time, so forward variance is model-free: $K_{var}(T_1, T_2) = \frac{T_2 K_{var}(T_2) - T_1 K_{var}(T_1)}{T_2 - T_1}$.

### Replication with a $1/K^2$ strip

Itô on $\ln S$ with $dS/S = \mu\,dt + \sigma\,dW$ gives $d\ln S = dS/S - \tfrac12\sigma^2 dt$, so

$$
\int_0^T \sigma_t^2\,dt = 2\int_0^T \frac{dS_t}{S_t} - 2\ln\frac{S_T}{S_0}.
$$

The first term is a dynamic strategy: hold $2/S_t$ shares, a constant dollar position of 2, rebalanced continuously; under $Q$ it earns $2rT$ in expectation.
The second is a static log contract, which any smooth payoff decomposition (Carr-Madan) writes as a forward plus options:

$$
-\ln\frac{S_T}{F} = -\frac{S_T - F}{F} + \int_0^F \frac{(K - S_T)^+}{K^2}\,dK + \int_F^\infty \frac{(S_T - K)^+}{K^2}\,dK.
$$

Taking expectations gives the fair strike

$$
K_{var} = \frac{2}{T}\left(rT - E_Q\!\left[\ln\frac{S_T}{S_0}\right]\right) = \frac{2e^{rT}}{T}\left[\int_0^F \frac{P(K)}{K^2}\,dK + \int_F^\infty \frac{C(K)}{K^2}\,dK\right].
$$

Why $1/K^2$: for Black-Scholes, homogeneity gives $S^2\,\partial^2 C/\partial S^2 = K^2\,\partial^2 C/\partial K^2$, so a strip with weights $1/K^2$ has dollar gamma $\int S^2\Gamma(K)/K^2\,dK = \int \partial^2 C/\partial K^2\,dK = e^{-rT}$, independent of spot.
A delta-hedged portfolio earns $\tfrac12 S^2\Gamma(\sigma_R^2 - \sigma_{imp}^2)\,dt$; with constant dollar gamma that accrues realized variance regardless of the path, which is exactly a variance swap.
A single option's P&L, in contrast, depends on where spot realises its variance.

What moves the strike:

- Skew: OTM puts carry both high vol and large weights $1/K^2$, so $K_{var}$ sits above ATM vol; for index options the gap is typically a few vol points at one year.
- Wings: the strip integrates to zero and infinity; listed strikes stop, so truncation biases a discrete estimate low, and coarse strike spacing biases it (here) high.
- Jumps: the replication assumed continuous paths. A jump of return $J$ contributes $\ln^2(1+J)$ to realized variance but only $2(J - \ln(1+J))$ to the hedged strip; the difference is $-J^3/3$ to leading order, so down-jumps cost a short variance position hedged with the strip. Single-stock variance swaps are therefore usually capped (commonly at 2.5 times the strike in vol).

### VIX

The Cboe VIX applies a discretised version of the strip to SPX options for two expiries bracketing 30 days:

$$
\sigma^2 = \frac{2}{T}\sum_i \frac{\Delta K_i}{K_i^2}e^{rT}Q(K_i) - \frac{1}{T}\left(\frac{F}{K_0} - 1\right)^2,
$$

with $Q(K_i)$ the OTM mid quote (the average of call and put at $K_0$, the first strike at or below the forward), strikes truncated after two consecutive zero bids, and the two variances interpolated to a constant 30 days; VIX $= 100\sqrt{\sigma^2_{30}}$.
The correction term fixes the use of an in-the-money call between $K_0$ and $F$.
So VIX is the square root of a 30-day variance swap rate (up to discretisation and jumps), not an expected vol.

VIX futures and options:

- A VIX future settles on VIX at expiry, so its fair value is $E_Q[\text{VIX}_T] = E_Q[\sqrt{V_T}] \le \sqrt{E_Q[V_T]}$, the square root of forward 30-day variance from SPX options. The gap is a convexity adjustment set by vol-of-vol.
- The futures curve is usually in contango (upward sloping) because vol mean-reverts up from low levels and sellers demand a premium; long VIX futures products lose the roll most of the time.
- VIX options are priced off the VIX future for their own expiry (Black-76 on the future), not off spot VIX, and show upward (call) skew because vol spikes up.

### Vol swaps and the convexity adjustment

A vol swap pays $N(\sigma_R - K_{vol})$.
Because $\sqrt{\cdot}$ is concave, $K_{vol} = E[\sigma_R] \le \sqrt{E[\sigma_R^2]} = \sqrt{K_{var}}$.
A second-order expansion of $\sqrt{V}$ around $K_{var}$ gives

$$
K_{vol} \approx \sqrt{K_{var}} - \frac{\text{Var}(\sigma_R^2)}{8K_{var}^{3/2}}.
$$

There is no static replication: hedging a vol swap needs a model for vol-of-vol, and the hedge (a variance swap position scaled by $1/(2K_{vol})$) must be rebalanced.
Long variance against short vol swaps (same vega notional) is a long vol-of-vol position.

### The variance risk premium

Index implied variance has on average exceeded subsequent realized variance, so short variance earns a premium, paid for by large losses in crashes (the P&L is convex against the seller).
Desks harvest it with defined tails (capped variance, corridors, spreads against VIX calls), and hedge funds use the relative value between variance strikes, VIX futures and forward variance.

Related contracts: gamma swaps weight each squared return by $S_i/S_0$ (a strip weighted $1/K$, cheaper downside), corridor variance accrues only while spot is inside a band, and conditional variance only on down-days; each is a different strip.

## Worked examples

### Example 1: variance versus vol swap P&L

Vega notional 100,000 at a strike of 20 vol, so $N_{var} = 100{,}000/(2 \times 20) = 2{,}500$ per variance point.

| Realized vol | Variance swap P&L | Vol swap P&L |
| :--- | :--- | :--- |
| 25 | $2{,}500 \times (625 - 400) = +562{,}500$ | $+500{,}000$ |
| 15 | $2{,}500 \times (225 - 400) = -437{,}500$ | $-500{,}000$ |
| 10 | $-750{,}000$ | $-1{,}000{,}000$ |
| 40 | $+3{,}000{,}000$ | $+2{,}000{,}000$ |

The long variance position gains more in the spike and loses less in the lull: it is long convexity in realized vol, which is why a short variance seller needs a premium over the vol-swap strike.

### Example 2: marking a seasoned swap

One-year variance swap struck at 20 vol, $N_{var} = 2{,}500$, three months in: realized so far 25 vol, and the nine-month variance strike is now 22.
Expected final variance: $0.25 \times 625 + 0.75 \times 484 = 519.25$, so the mark is $2{,}500 \times (519.25 - 400) = 298{,}125$ before discounting.
Forward variance works the same way: with 3-month variance at 18 and 6-month at 20, the 3m-6m forward variance is $(0.5 \times 400 - 0.25 \times 324)/0.25 = 476$, a forward vol of 21.8.

### Example 3: pricing the strip

One year, $F = 100$, $r = 0$.
With a flat 20% smile the strip integral returns $K_{var} = 0.0400$, exactly $\sigma^2$.
With an SVI smile (total variance $0.03 + 0.1(-0.7k + \sqrt{k^2 + 0.01})$, $k = \ln(K/F)$) that has ATM 20.0%, 90% strike 22.8%, 80% strike 26.5% and 110% strike 19.3%, the strip gives $K_{var} = 0.06273$, a variance strike of 25.05 vol: five points over ATM.
Puts contribute 0.0444 and calls 0.0183, 71% from the downside.
Truncating the strip to strikes 50-150 drops the answer to 23.9, and to 70-130 to 21.7: the wings matter.

### Example 4: a VIX-style calculation

Thirty days, $S = 100$, $r = 3\%$, $F = 100.247$, $K_0 = 100$, same smile shape, strikes 60 to 140 every 2.5.
The discrete formula gives 20.73, against 20.42 from the continuous strip and an ATM vol of 19.96.
Refining the grid shows the bias: spacing 5 gives 21.63, 2.5 gives 20.73, 1 gives 20.47 and 0.25 gives 20.42.
With a 30-day standard deviation of about 5.7 points, a 2.5 spacing is coarse, and the midpoint sum overweights the kinked region near the money.

```python
import numpy as np
from scipy.stats import norm

def bs(S, K, T, r, sigma, cp):
    sd = sigma * np.sqrt(T)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / sd
    return cp * (S * norm.cdf(cp * d1) - K * np.exp(-r * T) * norm.cdf(cp * (d1 - sd)))

def vix_style_variance(strikes, quotes, F, T, r):
    """CBOE-style variance: OTM quotes, K0 = first strike at or below the forward."""
    K0 = strikes[strikes <= F].max()
    dK = np.gradient(strikes)                     # central differences, one-sided at the ends
    contrib = dK / strikes**2 * np.exp(r * T) * quotes
    return 2 / T * contrib.sum() - (F / K0 - 1) ** 2 / T

S, r, T = 100.0, 0.03, 30 / 365
F = S * np.exp(r * T)
smile = lambda K: np.sqrt(0.03 + 0.1 * (-0.7 * np.log(K / 100) + np.sqrt(np.log(K / 100) ** 2 + 0.01)))
K = np.arange(60.0, 142.5, 2.5)
K0 = K[K <= F].max()
Q = np.where(K < K0, bs(S, K, T, r, smile(K), -1), bs(S, K, T, r, smile(K), 1))
Q[K == K0] = 0.5 * (bs(S, K0, T, r, smile(K0), -1) + bs(S, K0, T, r, smile(K0), 1))
print(100 * np.sqrt(vix_style_variance(K, Q, F, T, r)))  # 20.73 on this grid; 20.42 continuous
```

### Example 5: a crash against a strip-hedged short

A trader is short a one-year variance swap ($N_{var} = 2{,}500$) and long the replicating strip.
A single $-20\%$ day adds $\ln^2(0.8) = 0.04979$ to $\sum \ln^2$, that is 498 variance points on the annualised swap.
The strip plus delta hedge delivers $2(J - \ln(1+J)) = 2(-0.2 + 0.2231) = 0.04629$, or 463 points.
The 35-point shortfall costs $2{,}500 \times 35 = 87{,}650$ on top of the variance P&L.
A $+20\%$ jump goes the other way (332 realized versus 354 replicated), so the error is the third moment: short variance is short the $-J^3/3$ skewness term.

### Example 6: vol swap convexity

Variance strike 20 vol ($K_{var} = 400$) and a standard deviation of realized variance of 150 variance points.
Adjustment: $150^2/(8 \times 400^{1.5}) = 22{,}500/64{,}000 = 0.35$, so the vol swap is worth about 19.65.
If realized variance is lognormal with that mean and standard deviation, the exact $E[\sqrt{V}]$ is 19.67, so the second-order formula is good to 0.02 here.

### Example 7: computing realized variance

Closes 100, 101, 99.5, 100.2, 98.9, 100.4 give log returns $+0.995\%$, $-1.496\%$, $+0.701\%$, $-1.306\%$, $+1.505\%$.
Contract convention: $\tfrac{252}{5}\sum r_i^2 \times 10^4 = 387.7$ variance points, 19.69 vol.
The textbook sample standard deviation (mean removed, divisor $n - 1$) gives 21.97 vol on the same data: on short windows the convention is worth two vol points.

## Pitfalls

- Treating variance and vol as interchangeable; a variance swap is convex in vol and its strike exceeds the vol swap strike.
- Quoting P&L in variance notional when the trade was sized in vega notional, or forgetting the factor $2K_{vol}$ between them.
- Pricing the strip on listed strikes without handling truncation and spacing; the two biases have opposite signs and depend on maturity.
- Believing the replication holds through jumps; it does not, and short variance is short the third moment, hence caps on single-stock swaps.
- Treating VIX futures as forecasts of spot VIX, or pricing VIX options off spot VIX; each expiry has its own forward, below the square root of forward variance.
- Computing realized variance with mean subtraction and $n - 1$ when the contract says neither; on short windows the difference is large.
- Forgetting that a seasoned swap's remaining vega shrinks linearly with time elapsed: only the $(T - t)/T$ fraction is still exposed to implied variance.

## Interview questions

> [!question]- deriv-varswap-payoff-notional | Write the variance swap payoff and the relation between variance and vega notional.
> $N_{var}(\sigma_R^2 - K_{vol}^2)$, with $N_{vega} = 2K_{vol}N_{var}$.
> Near the strike $\sigma_R^2 - K^2 \approx 2K(\sigma_R - K)$, so vega notional is the P&L per vol point for small moves.

> [!question]- deriv-varswap-pnl-example | Vega notional 100k at 20 vol, realized 25. What does the long variance swap make, and a vol swap of the same vega notional?
> Variance swap $2{,}500 \times (625 - 400) = 562{,}500$; vol swap $100{,}000 \times 5 = 500{,}000$.
> The extra 62,500 is convexity: long variance is convex in realized vol.

> [!question]- deriv-varswap-replication-weights | How do you replicate a variance swap, and why are the option weights $1/K^2$?
> Hold OTM puts and calls across all strikes with weights $1/K^2$ (scaled by $2/T$) and delta-hedge with a constant dollar position in the underlying.
> The $1/K^2$ strip is the log contract, and its dollar gamma $S^2\Gamma$ is independent of spot, so the hedged P&L accrues realized variance wherever spot goes.

> [!question]- deriv-varswap-fair-strike-formula | Give the fair variance strike in terms of option prices.
> $K_{var} = \frac{2e^{rT}}{T}\left[\int_0^F P(K)K^{-2}\,dK + \int_F^\infty C(K)K^{-2}\,dK\right]$.
> It equals $-\frac{2}{T}E_Q[\ln(S_T/F)]$, from Itô's $\int\sigma^2 dt = 2\int dS/S - 2\ln(S_T/S_0)$.

> [!question]- deriv-varswap-skew-above-atm | Why does the variance strike exceed ATM implied vol for index options?
> The strip weights every strike by $1/K^2$, and OTM puts have both high implied vol (skew) and larger weights, so the downside dominates.
> In the worked SVI example ATM is 20.0 but the variance strike is 25.05, with 71% of the value from puts.

> [!question]- deriv-varswap-jump-error | Does the option strip replicate a variance swap when the underlying jumps?
> No: a jump of return $J$ adds $\ln^2(1+J)$ to realized variance but the hedged strip earns $2(J - \ln(1+J))$, a gap of about $-J^3/3$.
> A $-20\%$ day leaves a strip-hedged short about 35 variance points behind on a one-year swap, which is why single-stock variance is capped.

> [!question]- deriv-varswap-vol-swap-convexity | Why is a vol swap strike below the square root of the variance swap strike, and by how much?
> Jensen: $E[\sigma_R] = E[\sqrt{V}] \le \sqrt{E[V]}$; the gap is about $\text{Var}(V)/(8K_{var}^{3/2})$.
> With $K_{var} = 400$ and a standard deviation of 150 variance points the vol strike is about 19.65 against 20.

> [!question]- deriv-varswap-vol-swap-replication | Can a vol swap be statically replicated?
> No: $\sqrt{\cdot}$ of realized variance is not a function of the terminal price, so it needs a vol-of-vol model and a dynamically rebalanced variance hedge.
> Variance swaps are special because realized variance equals a static log contract plus a delta hedge.

> [!question]- deriv-varswap-vix-definition | What is the VIX, precisely?
> $100$ times the square root of a 30-day variance swap rate computed from SPX option prices by the Cboe discretised strip formula, interpolating the two expiries that bracket 30 days.
> It is a variance-based index, not an expected vol, and it includes the variance risk premium.

> [!question]- deriv-varswap-vix-futures-convexity | Is a VIX future equal to the square root of forward variance implied by SPX options?
> No, it is lower: $E_Q[\text{VIX}_T] \le \sqrt{E_Q[\text{VIX}_T^2]}$ by Jensen, and the gap grows with vol-of-vol.
> VIX options are therefore priced off the VIX future for their expiry, not off spot VIX or the variance curve.

> [!question]- deriv-varswap-forward-variance | Three-month variance strike 18, six-month 20. What is the 3m-6m forward variance strike?
> 476 variance points, a forward vol of 21.8.
> Variance is additive: $(0.5 \times 400 - 0.25 \times 324)/0.25 = 476$.

> [!question]- deriv-varswap-seasoned-mtm | A one-year swap struck at 20 is three months old, realized 25 so far, and the nine-month strike is 22. What is it worth per variance point?
> $0.25 \times 625 + 0.75 \times 484 - 400 = 119.25$ variance points (before discounting).
> Realized and implied variance combine time-weighted because variance is additive.

> [!question]- deriv-varswap-vix-etp-roll | Why do long VIX futures ETPs lose money most of the time?
> The VIX futures curve is usually in contango, so the product keeps selling cheaper near futures and buying dearer later ones, and each future rolls down toward a lower spot VIX.
> Holders pay the volatility risk premium in exchange for a payoff in sell-offs.

> [!question]- deriv-varswap-realized-convention | How is realized variance computed in a variance swap confirmation, and why does it matter?
> $\tfrac{252}{n}\sum\ln^2(S_i/S_{i-1})$ with no mean subtraction and divisor $n$.
> On short windows the difference from the sample standard deviation is material: five sample returns give 19.7 vol by contract and 22.0 by the textbook formula.

## In this repo and SDE-Interview-Prep

- Prev: [Option Strategies and Volatility Trading](13-Option-Strategies-and-Volatility-Trading.md). Next: [Dispersion and Correlation Trading](15-Dispersion-and-Correlation-Trading.md).
- Why constant dollar gamma earns variance: [Delta Hedging and Gamma Scalping](06-Delta-Hedging-and-Gamma-Scalping.md).

## Further reading

- P. Carr and D. Madan (1998), "Towards a theory of volatility trading", in *Volatility: New Estimation Techniques for Pricing Derivatives*, Risk Books.
- K. Demeterfi, E. Derman, M. Kamal and J. Zou (1999), "A guide to volatility and variance swaps", *Journal of Derivatives* 6(4).
- Jim Gatheral, *The Volatility Surface: A Practitioner's Guide*, chapter on variance and volatility swaps.
- Cboe, *VIX White Paper*, for the index methodology.
- Sebastien Bossu, "Introduction to variance swaps", *Wilmott* (2006).
