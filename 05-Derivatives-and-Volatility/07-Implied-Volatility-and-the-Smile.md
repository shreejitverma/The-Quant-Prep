---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [black-scholes-formula-and-intuition, numerical-optimization-and-root-finding]
est_hours: 4
sources: [Jim Gatheral - The Volatility Surface - A Practitioner's Guide (Wiley 2006), Sheldon Natenberg - Option Volatility and Pricing (volatility skews chapter), Emanuel Derman (1999) - Regimes of volatility - Risk 12(4), Manaster and Koehler (1982) - The calculation of implied variances from the Black-Scholes model - Journal of Finance 37(1), Brenner and Subrahmanyam (1988) - A simple formula to compute the implied standard deviation - Financial Analysts Journal 44(5), Peter Jaeckel (2015) - Let's be rational - Wilmott 2015(75), Roger Lee (2004) - The moment formula for implied volatility at extreme strikes - Mathematical Finance 14(3), Lorenzo Bergomi - Stochastic Volatility Modeling (CRC 2016), Uwe Wystup - FX Options and Structured Products (Wiley 2006)]
---

# Implied Volatility and the Smile

## TL;DR

- Implied volatility is the unique $\sigma$ that makes Black-Scholes match the market price; it exists because the call price is strictly increasing in $\sigma$ between its no-arbitrage bounds. It is a quoting convention, not a forecast.
- Solve it with Newton on vega started at the inflection point $\sigma^2 T = 2\lvert\ln(F/K)\rvert$, kept inside a shrinking bisection bracket; plain Newton from 20% blows up on far-from-the-money strikes.
- Equity indices show a downside skew (crash demand, leverage effect, overwriting supply, correlation rising in sell-offs); FX shows a more symmetric smile quoted as ATM, 25-delta risk reversal and butterfly; skew flattens roughly like $1/\sqrt{T}$.
- The smile is the market's risk-neutral density: skew is density skewness, curvature (wings) is kurtosis; $\partial^2 C / \partial K^2 \ge 0$ and total variance non-decreasing in $T$ are the no-arbitrage constraints.
- Smile dynamics set your delta: sticky strike keeps BS delta, sticky moneyness (delta) and local vol shift delta by $\text{vega} \times \partial\sigma/\partial S$ in opposite directions; under local vol the ATM vol moves about twice the skew.

## Learning objectives

- Compute implied volatility robustly with Newton and bisection fallbacks.
- Explain equity skew, FX smiles and term structure, and why they exist.
- Compare sticky-strike, sticky-delta and sticky-moneyness dynamics.

## Core concepts

### Definition and existence

Given a European call price $C_{mkt}$, the implied volatility $\sigma_{imp}$ solves $C_{BS}(S, K, T, r, q, \sigma) = C_{mkt}$.
Because vega $= S e^{-qT} \varphi(d_1)\sqrt{T} > 0$, the Black-Scholes price is strictly increasing in $\sigma$, from the intrinsic forward value $e^{-rT}(F - K)^+$ at $\sigma = 0$ to $S e^{-qT}$ as $\sigma \to \infty$.
So a solution exists and is unique if and only if the price lies strictly inside those bounds.
By put-call parity a put and a call with the same strike and expiry have the same implied vol, provided you use the right forward; desks back the forward out of the call-put pairs first, then compute vols.
A mismatch between call and put vols at the same strike is a wrong forward (dividend, borrow) or an arbitrage, never a "put vol" and a "call vol".

Implied vol is a price in different units.
It embeds the expected realized vol, a variance risk premium (sellers of options want paying for negatively skewed P&L), and supply and demand.
Index implied vol has on average exceeded subsequent realized vol, which is the premium systematic option sellers harvest.

### Computing it

Newton's method: $\sigma_{n+1} = \sigma_n - (C(\sigma_n) - C_{mkt}) / \text{vega}(\sigma_n)$.
Near the money it converges quadratically in two or three steps.
It fails for strikes far from the forward, where vega is tiny at low $\sigma$ and the first step overshoots into a region where the price is flat.

Three facts make it robust:

1. Start at the inflection point. $C(\sigma)$ is convex below and concave above $\sigma^* = \sqrt{2\lvert\ln(F/K)\rvert / T}$ (where $d_1 d_2 = 0$, so volga is zero). Manaster and Koehler show Newton from $\sigma^*$ converges monotonically.
2. Keep a bracket $[\sigma_{lo}, \sigma_{hi}]$ that you shrink with each evaluation, and take a bisection step whenever Newton would leave it.
3. For deep wings, solve in log price or use Jaeckel's "Let's be rational" algorithm, which reaches machine precision in two iterations for any strike; production libraries use it.

A quick ATM approximation (Brenner-Subrahmanyam): for an ATM-forward option $C \approx 0.4\,\sigma\,S\sqrt{T}$ (since $1/\sqrt{2\pi} \approx 0.3989$), so $\sigma \approx C / (0.4\,S\sqrt{T})$ and an ATM straddle is about $0.8\,\sigma S \sqrt{T}$.

### The shape of the smile

Plot $\sigma_{imp}$ against strike, log-moneyness $k = \ln(K/F)$, or delta.

- Equity index: a downward-sloping skew, puts richer than calls. Reasons: the 1987 crash repriced tail risk; realized vol rises when spot falls (leverage effect, spot-vol correlation strongly negative); institutions structurally buy puts for protection while overwriters sell upside calls; index correlation rises in sell-offs, so index downside vol is richer than the single-stock vols imply.
- Single stocks: flatter skew than the index, often with some upside wing; takeover names and biotech carry call-side premium.
- FX: a smile, roughly symmetric for pairs of similar currencies, skewed toward the "crash" currency (for example USDJPY puts, EM currency calls against USD). Quoted by delta: ATM (delta-neutral straddle), 25-delta risk reversal $RR = \sigma_{25C} - \sigma_{25P}$ and butterfly $BF = \tfrac12(\sigma_{25C} + \sigma_{25P}) - \sigma_{ATM}$, so $\sigma_{25C} = \sigma_{ATM} + BF + RR/2$ and $\sigma_{25P} = \sigma_{ATM} + BF - RR/2$ (the simple "smile strangle" convention; brokers' market strangle convention differs, see Wystup).
- Commodities: often upside (call) skew where supply shocks drive prices up (natural gas, grains).

Term structure: ATM vol mean-reverts, so the curve slopes up when vol is low and inverts in a crisis; scheduled events (earnings, central banks) add bumps.
Skew is steepest at short maturities and decays roughly like $T^{-1/2}$ in index options (jump and stochastic-vol models give $T^{-1}$ and roughly flat-then-decaying shapes respectively; empirically between the two).

### Smile and the risk-neutral density

Breeden-Litzenberger: $f_Q(K) = e^{rT}\partial^2 C/\partial K^2$ (see [Option Payoffs and Put-Call Parity](02-Option-Payoffs-and-Put-Call-Parity.md)).
A flat smile is a lognormal density; a downside skew fattens the left tail and thins the right (negative skewness); raised wings on both sides mean excess kurtosis.
Digital prices pick up the slope: with $\sigma = \sigma(K)$,

$$
D(K) = -\frac{dC}{dK} = e^{-rT}N(d_2) - \text{vega}\cdot\frac{\partial\sigma}{\partial K}.
$$

With negative skew, $\partial\sigma/\partial K < 0$, so the digital call is worth more than $e^{-rT}N(d_2)$.

No-arbitrage constraints on a surface:

- Butterfly (strike) arbitrage: call prices convex in $K$, so the implied density is non-negative.
- Calendar arbitrage: total implied variance $w(k, T) = \sigma^2(k, T)\,T$ is non-decreasing in $T$ at fixed forward moneyness $k$.
- Wings: Lee's moment formula bounds the asymptotic slope, $w(k) \le 2\lvert k\rvert$ for large $\lvert k\rvert$, so implied vol can grow at most like $\sqrt{\lvert k\rvert}$.

A useful heuristic (Derman, Gatheral): implied vol at strike $K$ is roughly the average of local vol over the path from spot to $K$, so for a linear local-vol skew the implied skew is half the local skew.

Surface construction and parametrisations (SVI, SABR) are in [Volatility Surface Construction](08-Volatility-Surface-Construction.md) and [Stochastic Volatility](09-Stochastic-Volatility-Heston-and-SABR.md).

### Smile dynamics and the smile-adjusted delta

If $\sigma = \sigma(K, S)$ moves with spot, the delta you should hedge is

$$
\Delta = \Delta_{BS} + \text{vega}\cdot\frac{\partial\sigma(K, S)}{\partial S}.
$$

Let $\beta = \partial\sigma/\partial K$ at the money (negative for equities).

| Regime | Fixed-strike vol as spot moves | ATM vol as spot moves | $\partial\sigma(K)/\partial S$ | Delta vs BS (equity skew) |
| :--- | :--- | :--- | :--- | :--- |
| Sticky strike | unchanged | slides along the skew, $+\beta$ per unit of spot | $0$ | equal |
| Sticky moneyness (sticky delta) | smile moves with spot, $\sigma = f(K/S)$ | unchanged | $-(K/S)\beta \approx -\beta$ | higher |
| Local vol (sticky implied tree) | falls when spot rises | moves by about $2\beta$ | $\approx +\beta$ | lower |

Derman's "regimes of volatility" associates sticky strike with range-bound markets, sticky delta with trending markets and local vol with jumpy, fearful markets.
Bergomi's skew stickiness ratio $R = (\partial\sigma_{ATM}/\partial\ln S)/(\partial\sigma/\partial\ln K)$ summarises it: $R = 0$ sticky delta, $R = 1$ sticky strike, $R = 2$ local vol; index markets typically realise something between 1 and 2.
The choice matters for P&L attribution and for hedging: the minimum-variance delta for an equity index option is below the BS delta, because vol rises as spot falls.

## Worked examples

### Example 1: Newton for an at-the-money option

$S = K = 100$, $T = 0.5$, $r = 3\%$, no dividends, call price 7.00.
Initial guess from Brenner-Subrahmanyam, ignoring carry: $\sigma_0 = \sqrt{2\pi/T}\,C/S = 24.81\%$.
At $\sigma_0$ the price is 7.7087 and vega is 27.79 (per unit vol), so $\sigma_1 = 0.2481 - 0.7087/27.79 = 22.264\%$.
At $\sigma_1$ the price is 7.00003; one more step gives $\sigma = 22.2641\%$ to eight digits.
The guess was 2.5 vols high because it treated the whole premium as time value: with $r > 0$ an ATM-spot call is in the money forward ($S - Ke^{-rT} = 1.49$), and about half of that, 0.72, is carry rather than volatility ($0.3989 \times 0.2226 \times 100 \times \sqrt{0.5} = 6.28$).
The shortcut is accurate only for ATM-forward options.

### Example 2: why plain Newton fails in the wing

$S = 100$, $K = 150$, $T = 0.25$, $r = 0$, call price 0.01 (true implied vol 28.16%).
From $\sigma_0 = 20\%$: price $6.9 \times 10^{-5}$, vega 0.0066, so the Newton step lands at $\sigma_1 = 171\%$, where the price is 20.64.
Newton then crawls back (68%, 48%, ...) and in a less friendly case would go negative.
From the Manaster-Koehler start $\sigma^* = \sqrt{2\ln 1.5/0.25} = 180\%$ Newton decreases monotonically: 68%, 48%, 39%, 33%, 30.2%, 28.6%, 28.19%, converging but slowly because vega shrinks with the price.
The safeguarded solver below handles both cases; for sub-cent wing options use a log-price objective or Jaeckel's method.

```python
import numpy as np
from scipy.stats import norm

def bs_call(S, K, T, r, sigma, q=0.0):
    F = S * np.exp((r - q) * T)
    sd = sigma * np.sqrt(T)
    d1 = np.log(F / K) / sd + 0.5 * sd
    return np.exp(-r * T) * (F * norm.cdf(d1) - K * norm.cdf(d1 - sd))

def implied_vol(price, S, K, T, r, q=0.0, tol=1e-10, max_iter=100):
    """Safeguarded Newton: Newton steps inside a bisection bracket that always shrinks."""
    F, df = S * np.exp((r - q) * T), np.exp(-r * T)
    lower, upper = df * max(F - K, 0.0), df * F          # no-arbitrage bounds for a call
    if not lower < price < upper:
        raise ValueError("price outside no-arbitrage bounds")
    lo, hi = 1e-6, 5.0
    sigma = np.sqrt(2 * abs(np.log(F / K)) / T) or 0.2  # Manaster-Koehler start (inflection point)
    for _ in range(max_iter):
        diff = bs_call(S, K, T, r, sigma, q) - price
        if abs(diff) < tol:
            return sigma
        lo, hi = (lo, sigma) if diff > 0 else (sigma, hi)  # price increases in sigma
        vega = df * F * norm.pdf(np.log(F / K) / (sigma * np.sqrt(T)) + 0.5 * sigma * np.sqrt(T)) * np.sqrt(T)
        step = sigma - diff / vega if vega > 1e-12 else -1.0
        sigma = step if lo < step < hi else 0.5 * (lo + hi)  # fall back to bisection
    raise RuntimeError("no convergence")

print(implied_vol(7.00, 100, 100, 0.5, 0.03))   # 0.22264
print(implied_vol(0.01, 100, 150, 0.25, 0.0))   # 0.28162
```

### Example 3: smile-adjusted delta of an OTM put

$S = 100$, $T = 0.25$, $r = 0$, 90-strike put at $\sigma = 25\%$, local skew $\beta = \partial\sigma/\partial K = -0.004$ (0.4 vol points per strike point).
Black-Scholes: put 1.319, delta $-0.183$, vega 13.24 per unit vol (0.132 per vol point).

- Sticky strike: $\Delta = -0.183$.
- Sticky moneyness: $\partial\sigma/\partial S = -(K/S)\beta = +0.0036$, so $\Delta = -0.183 + 13.24 \times 0.0036 = -0.135$. When spot falls the 90 strike becomes "less OTM" in moneyness terms and takes a lower vol, so the put gains less.
- Local vol: $\partial\sigma/\partial S \approx \beta = -0.004$, so $\Delta = -0.183 - 13.24 \times 0.004 = -0.236$. When spot falls the 90 strike's vol rises, so the put gains more.

The three regimes differ by 0.10 of delta on a 0.18-delta option: on 10,000 puts on a 100 stock (multiplier 100) that is 10,000 shares of hedge disagreement.

### Example 4: a digital priced off the skew

One year, $S = F = 100$, $r = 0$, ATM vol 20%, skew $\partial\sigma/\partial K = -0.002$ per strike point.
$N(d_2) = N(-0.1) = 0.4602$ and vega $= 39.70$.
Digital call $= 0.4602 - 39.70 \times (-0.002) = 0.4602 + 0.0794 = 0.5396$.
A finite-difference call spread on the smile $\sigma(K) = 0.20 - 0.002(K - 100)$ gives 0.53956, confirming it.
Pricing the digital at flat vol would undersell it by 8 points of a 1-unit payout.

### Example 5: FX risk reversal and butterfly to wing vols

One-month EURUSD: ATM 10.0%, 25-delta risk reversal $-1.5$, 25-delta butterfly 0.40.
$\sigma_{25C} = 10.0 + 0.40 - 0.75 = 9.65\%$ and $\sigma_{25P} = 10.0 + 0.40 + 0.75 = 11.15\%$.
The negative risk reversal says EUR puts (USD calls) are bid; the butterfly says both wings sit 0.4 above ATM on average, pricing fat tails.

### Example 6: forward vol and a calendar check

One-month ATM vol 30%, three-month 25%.
Forward variance from 1m to 3m: $(0.25^2 \times 0.25 - 0.30^2/12)/(0.25 - 1/12) = 0.04875$, a forward vol of 22.08%.
If the one-month vol were 45% instead, forward variance would be $-0.0075 < 0$: total variance falls with maturity, a calendar arbitrage (sell the 1m, buy the 3m at the same moneyness), unless an event (earnings) sits inside the short expiry and the variance is genuinely front-loaded, in which case check the strike-matched total variance before trading it.

## Pitfalls

- Reading implied vol as the market's forecast; it includes a variance risk premium and demand pressure, so index implied is usually above subsequent realized.
- Computing put and call vols at the same strike with a stale forward and "seeing" put-call vol spreads; fix the forward (dividends, borrow) first.
- Running Newton from a fixed 20% guess on wing strikes; it overshoots and may go negative. Bracket it.
- Inverting prices below intrinsic or above the upper bound; there is no solution, and a solver that returns one is hiding a bad quote.
- Quoting FX butterflies without stating the convention; the market (broker) strangle and the smile strangle give different wing vols.
- Hedging index options with Black-Scholes delta and calling the residual "vega P&L"; the spot-vol correlation makes it predictable delta P&L.
- Comparing skew across maturities in strike units; normalise by $\sigma\sqrt{T}$ or use delta, because a 10-point OTM put is far in one week and near in two years.

## Interview questions

> [!question]- deriv-iv-existence-uniqueness | Why is implied volatility unique, and when does it fail to exist?
> It is unique because the Black-Scholes price is strictly increasing in $\sigma$ (vega $> 0$); it exists only if the price lies strictly between $e^{-rT}(F - K)^+$ and $S e^{-qT}$.
> Any price outside the bounds is an arbitrage or a bad quote, and has no implied vol.

> [!question]- deriv-iv-call-put-same-strike | Why must a call and a put with the same strike and expiry have the same implied vol?
> Put-call parity is model-free: $C - P = e^{-rT}(F - K)$ holds for Black-Scholes prices at any single $\sigma$ and for market prices, so the $\sigma$ that fits the call also fits the put.
> An apparent difference means the forward (dividends, borrow, rates) is wrong, or American exercise premium is contaminating one side.

> [!question]- deriv-iv-quick-atm-inversion | A three-month ATM call on a 100 stock trades at 4.00 with zero rates. Implied vol in your head?
> About 20%: $\sigma \approx C/(0.4\,S\sqrt{T}) = 4/(0.4 \times 100 \times 0.5) = 0.20$.
> The exact inversion is 20.06%.

> [!question]- deriv-iv-newton-start-point | Newton for implied vol diverges on a far out-of-the-money strike. What do you do?
> Start at the inflection point $\sigma^* = \sqrt{2\lvert\ln(F/K)\rvert/T}$ and keep a bisection bracket, bisecting whenever Newton leaves it (or use Jaeckel's rational method).
> Below $\sigma^*$ the price is convex in $\sigma$ with tiny vega, so a Newton step overshoots; from $\sigma^*$ the iteration is monotone (Manaster-Koehler).

> [!question]- deriv-iv-equity-skew-reasons | Why do equity index options have a downside skew?
> Puts are demanded for crash protection, realized vol rises when spot falls (leverage and spot-vol correlation), and index correlation jumps in sell-offs; supply from call overwriters cheapens the upside.
> Equivalently the risk-neutral density is negatively skewed with a fat left tail, which has been priced since the 1987 crash.

> [!question]- deriv-iv-fx-wing-vols | ATM 10%, 25-delta risk reversal $-1.5$, 25-delta butterfly 0.4. What are the 25-delta call and put vols?
> Call 9.65%, put 11.15%.
> $\sigma_{25C} = ATM + BF + RR/2$ and $\sigma_{25P} = ATM + BF - RR/2$ under the smile-strangle convention.

> [!question]- deriv-iv-smile-density-link | What do skew and smile curvature say about the risk-neutral distribution?
> Negative skew means a negatively skewed density (fat left tail, thin right); curvature (both wings bid) means excess kurtosis.
> The link is exact through Breeden-Litzenberger, $f_Q(K) = e^{rT}\partial^2 C/\partial K^2$; a flat smile is lognormal.

> [!question]- deriv-iv-digital-skew-term | With ATM vol 20%, one year, zero rates and skew $-0.002$ per strike point, price the ATM digital call.
> About 0.540.
> $D = N(d_2) - \text{vega}\cdot\partial\sigma/\partial K = 0.4602 + 39.70 \times 0.002 = 0.5396$; ignoring the skew misprices it by 8 points.

> [!question]- deriv-iv-sticky-regimes | Define sticky strike, sticky delta and local-vol smile dynamics.
> Sticky strike: each strike keeps its vol as spot moves. Sticky delta (moneyness): the smile moves with spot, so vol is a function of $K/S$ and ATM vol is constant. Local vol: fixed-strike vols move with slope about $\partial\sigma/\partial K$, so ATM vol moves about twice the skew.
> They give different deltas via $\Delta = \Delta_{BS} + \text{vega}\,\partial\sigma/\partial S$.

> [!question]- deriv-iv-smile-delta-sign | Equity skew, OTM put: is the local-vol delta more or less negative than Black-Scholes, and than sticky delta?
> More negative than both: local vol gives $\Delta_{BS} + \text{vega}\,\beta$ with $\beta < 0$, sticky delta gives $\Delta_{BS} - \text{vega}\,\beta$.
> In the worked example (90 put, 3m, 25% vol, $\beta = -0.004$): local vol $-0.236$, BS $-0.183$, sticky delta $-0.135$.

> [!question]- deriv-iv-local-vol-twice-skew | Why does the ATM implied vol move by about twice the skew per unit of spot under local vol?
> Implied vol is roughly the average of local vol between spot and strike, so the implied skew is half the local skew; the ATM vol equals local vol at spot, which moves with the full local slope, $2\beta$.
> This is the skew stickiness ratio $R = 2$ (sticky strike is 1, sticky delta is 0).

> [!question]- deriv-iv-skew-term-decay | How does skew scale with maturity, and why?
> It flattens with maturity, roughly like $1/\sqrt{T}$ for index options (jump models give faster, stochastic vol slower, decay).
> Over longer horizons the return distribution aggregates toward normal, and a fixed jump or spot-vol correlation matters less relative to total variance.

> [!question]- deriv-iv-calendar-arbitrage | One-month ATM vol 45%, three-month 25%. Is there an arbitrage?
> Forward variance is $(0.25^2 \times 0.25 - 0.45^2/12)/(1/6) = -0.0075 < 0$, so total variance falls with maturity: a calendar arbitrage at matched forward moneyness.
> The exception to check is a scheduled event in the front expiry, but even then total variance must still be non-decreasing in $T$.

> [!question]- deriv-iv-not-a-forecast | Is implied vol an unbiased forecast of realized vol?
> No: index implied vol has on average exceeded subsequent realized vol, which is the variance risk premium sellers are paid for bearing crash risk.
> Implied vol is a price, and it also moves with demand for protection; use it with a model of realized vol, not as one.

## In this repo and SDE-Interview-Prep

- Prev: [Delta Hedging and Gamma Scalping](06-Delta-Hedging-and-Gamma-Scalping.md). Next: [Volatility Surface Construction](08-Volatility-Surface-Construction.md).
- Trading the smile: [Option Strategies and Volatility Trading](13-Option-Strategies-and-Volatility-Trading.md).

## Further reading

- Jim Gatheral, *The Volatility Surface: A Practitioner's Guide*, chapters on local volatility and smile dynamics.
- Sheldon Natenberg, *Option Volatility and Pricing*, chapter on volatility skews.
- Emanuel Derman (1999), "Regimes of volatility", *Risk* 12(4).
- M. Manaster and G. Koehler (1982), "The calculation of implied variances from the Black-Scholes model", *Journal of Finance* 37(1).
- M. Brenner and M. Subrahmanyam (1988), "A simple formula to compute the implied standard deviation", *Financial Analysts Journal* 44(5).
- Peter Jaeckel (2015), "Let's be rational", *Wilmott*.
- Roger Lee (2004), "The moment formula for implied volatility at extreme strikes", *Mathematical Finance* 14(3).
- Lorenzo Bergomi, *Stochastic Volatility Modeling*, chapter on the skew stickiness ratio.
- Uwe Wystup, *FX Options and Structured Products*, on delta and strangle quoting conventions.
