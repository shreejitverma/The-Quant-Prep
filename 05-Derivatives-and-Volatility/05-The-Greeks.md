---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [black-scholes-formula-and-intuition]
est_hours: 5
sources: [Sheldon Natenberg - Option Volatility and Pricing (risk measurement chapters), John Hull - Options Futures and Other Derivatives (Greek letters chapter), Nassim Taleb - Dynamic Hedging (Greeks and higher-order risks)]
---

# The Greeks

## TL;DR

- Black-Scholes Greeks (dividend yield $q$): $\Delta_C = e^{-qT}N(d_1)$, $\Gamma = e^{-qT}\varphi(d_1)/(S\sigma\sqrt{T})$, $\mathcal{V} = S e^{-qT}\varphi(d_1)\sqrt{T}$; gamma and vega are the same for calls and puts.
- ATM rules of thumb: $\Gamma \approx 0.4/(S\sigma\sqrt{T})$, vega $\approx 0.4\,S\sqrt{T}$ per 1.00 of vol (divide by 100 per vol point), theta $\approx -0.2\,S\sigma/\sqrt{T}$ per year.
- Gamma-theta: $\Theta + \tfrac12\sigma^2 S^2\Gamma + (r-q)S\Delta - rV = 0$, so with zero rates $\Theta = -\tfrac12\sigma^2 S^2 \Gamma$: long gamma pays theta, and the breakeven daily move is $S\sigma/\sqrt{365}$.
- Vega $= \sigma S^2 T\,\Gamma$: short-dated options are gamma, long-dated options are vega, which is why gamma hedges with short options leave vega.
- Desk units: delta in shares or dollars, gamma as dollar delta per 1% move, vega per vol point, theta per day, rho per 1% rate.
- P&L explain: $\delta V \approx \Delta\,\delta S + \tfrac12\Gamma\,\delta S^2 + \mathcal{V}\,\delta\sigma + \Theta\,\delta t + \text{vanna}\,\delta S\,\delta\sigma + \tfrac12\text{volga}\,\delta\sigma^2$.

## Learning objectives

- Define and compute delta, gamma, vega, theta and rho, plus vanna, volga and charm.
- Sketch each Greek against spot and time to expiry.
- Explain the gamma-theta relationship and why long gamma pays theta.
- Aggregate Greeks at the portfolio level and in dollar terms.

## Core concepts

### Formulas

With $\tau = T - t$, $d_1 = [\ln(S/K) + (r - q + \tfrac12\sigma^2)\tau]/(\sigma\sqrt{\tau})$, $d_2 = d_1 - \sigma\sqrt{\tau}$ and $\varphi$ the standard normal density:

| Greek | Definition | Call | Put |
| :--- | :--- | :--- | :--- |
| Delta | $\partial V/\partial S$ | $e^{-q\tau}N(d_1)$ | $-e^{-q\tau}N(-d_1)$ |
| Gamma | $\partial^2 V/\partial S^2$ | $e^{-q\tau}\varphi(d_1)/(S\sigma\sqrt{\tau})$ | same |
| Vega | $\partial V/\partial\sigma$ | $S e^{-q\tau}\varphi(d_1)\sqrt{\tau}$ | same |
| Theta | $\partial V/\partial t$ | $-\dfrac{S e^{-q\tau}\varphi(d_1)\sigma}{2\sqrt{\tau}} - rK e^{-r\tau}N(d_2) + qS e^{-q\tau}N(d_1)$ | $-\dfrac{S e^{-q\tau}\varphi(d_1)\sigma}{2\sqrt{\tau}} + rK e^{-r\tau}N(-d_2) - qS e^{-q\tau}N(-d_1)$ |
| Rho | $\partial V/\partial r$ | $K\tau e^{-r\tau}N(d_2)$ | $-K\tau e^{-r\tau}N(-d_2)$ |
| Vanna | $\partial^2 V/\partial S\,\partial\sigma$ | $-e^{-q\tau}\varphi(d_1)\,d_2/\sigma$ | same |
| Volga (vomma) | $\partial^2 V/\partial\sigma^2$ | $\mathcal{V}\,d_1 d_2/\sigma$ | same |
| Charm | $\partial\Delta/\partial t$ | with $r = q = 0$: $\varphi(d_1)\,d_2/(2\tau)$ | same when $r = q = 0$ |

Call and put share gamma, vega, vanna and volga because $C - P$ is linear in $S$ and independent of $\sigma$ (put-call parity); $\Delta_C - \Delta_P = e^{-q\tau}$.
The key simplification is $S e^{-q\tau}\varphi(d_1) = K e^{-r\tau}\varphi(d_2)$, which kills the $\partial d_i/\partial S$ terms in delta.

### Shapes against spot and time

- Delta: an S-curve in spot from 0 to $e^{-q\tau}$; it steepens toward a step at $K$ as expiry approaches.
  ATM delta is a little above 0.5 because of the $+\tfrac12\sigma^2$ drift in $d_1$.
- Gamma: a bell centred just below the strike (the maximum in spot is at $S = K e^{-(r - q + 3\sigma^2/2)\tau}$).
  ATM gamma grows like $1/\sqrt{\tau}$ into expiry; OTM and ITM gamma fall to zero.
  Short-dated ATM options are where the gamma is, and where pin risk lives.
- Vega: a bell in spot, maximal where $d_2 = 0$, and growing like $\sqrt{\tau}$; it vanishes at expiry.
- Theta: most negative ATM, and ATM theta grows like $1/\sqrt{\tau}$; deep ITM European puts (and calls with large $q$) can have positive theta because of carry on the strike.
- Vanna: positive for OTM calls, negative for OTM puts (in the formula's sign convention, $-\varphi\,d_2/\sigma$), near zero around the forward; it tells you how delta shifts when vol moves, which matters for skew and for spot-vol correlation.
- Volga: near zero ATM, positive in the wings; long wings are long vol-of-vol, the reason smiles exist.
- Charm: delta decay, the overnight delta change with no spot move; OTM deltas drift to 0 and ITM deltas to 1, fastest near expiry.

### Gamma-theta relationship

The Black-Scholes PDE is

$$
\Theta + \tfrac12\sigma^2 S^2\Gamma + (r - q)S\Delta - rV = 0.
$$

For a delta-hedged position financed at $r$, the last two terms cancel against the financing of the hedge, leaving $\Theta_{\text{hedged}} = -\tfrac12\sigma^2 S^2 \Gamma$.
Over $\delta t$ the delta-hedged P&L is therefore

$$
\tfrac12\Gamma\,\delta S^2 + \Theta\,\delta t = \tfrac12\Gamma S^2\left[\left(\frac{\delta S}{S}\right)^2 - \sigma^2\delta t\right].
$$

Long gamma earns on squared moves and pays theta as rent; the two balance exactly when the realised squared return equals implied variance over the interval.
The breakeven one-day move is $S\sigma\sqrt{1/365}$ with a calendar-day theta, about $S\sigma/19$, or $S\sigma/16$ on a trading-day clock.
Details and path dependence: [Delta Hedging and Gamma Scalping](06-Delta-Hedging-and-Gamma-Scalping.md).

### Vega and gamma are the same risk at different horizons

Comparing the formulas,

$$
\mathcal{V} = \sigma S^2 \tau\,\Gamma.
$$

For the same gamma, a one-year option has four times the vega of a three-month option.
Gamma hedging a long-dated book with short-dated options removes spot convexity but leaves most of the vega, and exposes you to the term structure of volatility.
Desks therefore look at gamma by expiry and vega by expiry (often "weighted vega", scaling longer-dated vega down because long-dated implied vols move less).

### Dollar Greeks and aggregation

Per-option Greeks are in "per share" units; a book needs common units:

- Dollar delta $= \Delta \times S \times$ multiplier $\times$ contracts: the stock-equivalent notional.
- Dollar gamma (1% gamma) $= \Gamma S^2/100 \times$ multiplier $\times$ contracts: the change in dollar delta for a 1% spot move.
  The P&L from a 1% move is $\tfrac12 \times$ dollar gamma $\times 1\%$, and scales with the square of the move.
- Vega per vol point $= \mathcal{V}/100$; theta per day $= \Theta/365$ (or per trading day, $\Theta/252$, on a business-day clock); rho per 1% $= \rho/100$.
- Greeks on the same underlying add linearly.
  Across underlyings, sum dollar deltas beta-weighted to an index, dollar gammas similarly, and vegas by expiry bucket; do not add raw deltas of different stocks.

### P&L explain

A second-order Taylor expansion attributes daily P&L:

$$
\delta V \approx \Delta\,\delta S + \tfrac12\Gamma\,\delta S^2 + \mathcal{V}\,\delta\sigma + \Theta\,\delta t + \text{vanna}\,\delta S\,\delta\sigma + \tfrac12\,\text{volga}\,\delta\sigma^2 + \rho\,\delta r.
$$

A large unexplained residual means a missing risk (a smile move, a dividend change, a wrong vol bump), a jump large enough that third-order terms matter, or a booking error.

## Worked examples

### Example 1: Greeks of a one-year ATM call

$S = K = 100$, $T = 1$, $r = 5\%$, $\sigma = 20\%$, $q = 0$; $d_1 = 0.35$, $d_2 = 0.15$, $\varphi(0.35) = 0.3752$.

| Greek | Call | Put | Desk units |
| :--- | ---: | ---: | :--- |
| Price | 10.4506 | 5.5735 | |
| Delta | 0.6368 | $-0.3632$ | per share |
| Gamma | 0.01876 | 0.01876 | per share per 1.00 of spot |
| Vega | 37.52 | 37.52 | 0.375 per vol point |
| Theta | $-6.414$ | $-1.658$ | $-0.0176$ and $-0.0045$ per calendar day |
| Rho | 53.23 | $-41.89$ | 0.532 and $-0.419$ per 1% |
| Vanna | $-0.281$ | $-0.281$ | $-0.0028$ delta per vol point |
| Volga | 9.85 | 9.85 | per 1.00 of vol squared |

Check the PDE: $-6.414 + \tfrac12(0.04)(10^4)(0.01876) + 0.05 \times 100 \times 0.6368 - 0.05 \times 10.4506 = -6.414 + 3.752 + 3.184 - 0.523 = 0$.
Check the rules of thumb (zero rates version): vega $0.4 \times 100 \times 1 = 40$ versus 39.70; gamma $0.4/(100 \times 0.2) = 0.020$ versus 0.0198.

### Example 2: gamma pays for theta

Zero rates, $S = K = 100$, $\sigma = 20\%$, three months.
$\Gamma = 0.03984$ (rule of thumb $0.4/(100 \times 0.2 \times 0.5) = 0.040$).
$\Theta = -\tfrac12 \times 0.04 \times 10^4 \times 0.03984 = -7.97$ per year, $-0.0218$ per day (rule of thumb $-0.2 \times 100 \times 0.2/0.5 = -8.0$).
Breakeven daily move: $\sqrt{2 \times 0.0218/0.03984} = 1.047$, which is exactly $100 \times 0.2/\sqrt{365}$.
A 2-dollar day earns $\tfrac12 \times 0.03984 \times 4 = 0.0797$ of gamma against 0.0218 of theta.

### Example 3: hedging a book

Zero rates, $S = 100$, $\sigma = 20\%$, multiplier 100.
The book is short 50 one-year ATM calls: delta $-2699$ shares, gamma $-99.2$ per dollar, vega $-1985$ per vol point, theta $+54.4$ per day.

Gamma hedge with three-month ATM calls ($\Gamma = 0.03984$): need $50 \times 0.01985/0.03984 = 24.9$, so buy 25 contracts.
New gamma $+0.37$ per dollar (flat), delta $-2699 + 25 \times 100 \times 0.520 = -1399$, so buy 1399 shares.
Vega is still $-1487$ per vol point, three quarters of the original, and theta is about $-0.20$ per day.
Lesson: short-dated options neutralise gamma but barely touch vega; to hedge vega you need options near the same expiry.

### Example 4: P&L explain

Long one call from Example 1.
Next day: spot 102, vol 21%, one calendar day passes.

| Term | Formula | P&L |
| :--- | :--- | ---: |
| Delta | $0.6368 \times 2$ | 1.2737 |
| Gamma | $\tfrac12 \times 0.01876 \times 4$ | 0.0375 |
| Vega | $37.52 \times 0.01$ | 0.3752 |
| Theta | $-6.414/365$ | $-0.0176$ |
| Vanna | $-0.281 \times 2 \times 0.01$ | $-0.0056$ |
| Volga | $\tfrac12 \times 9.85 \times 0.0001$ | 0.0005 |
| Total explained | | 1.6637 |
| Full revaluation | $C(102, 21\%, T - 1/365) - C(100, 20\%, 1)$ | 1.6610 |

Unexplained $-0.0027$, the third-order terms (speed, and cross terms with time).

### Example 5: dollar gamma

A book is long 100 contracts of the one-year ATM call in Example 1 (10,000 options).
Dollar gamma $= 0.01876 \times 100^2/100 \times 10{,}000 = 18{,}762$ dollars of delta per 1% move.
A 1% move earns $\tfrac12 \times 18{,}762 \times 1\% = 93.8$ dollars; a 3% move earns 9 times that, 844 dollars.

```python
from math import exp, log, sqrt
from statistics import NormalDist

nd = NormalDist()

def greeks(S, K, T, r, sigma, q=0.0):
    sd = sigma * sqrt(T)
    d1 = (log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / sd
    d2 = d1 - sd
    pdf, Nd1, Nd2 = nd.pdf(d1), nd.cdf(d1), nd.cdf(d2)
    vega = S * exp(-q * T) * pdf * sqrt(T)
    return {
        "delta": exp(-q * T) * Nd1,
        "gamma": exp(-q * T) * pdf / (S * sd),
        "vega_pt": vega / 100,
        "theta_day": (-S * exp(-q * T) * pdf * sigma / (2 * sqrt(T))
                      - r * K * exp(-r * T) * Nd2 + q * S * exp(-q * T) * Nd1) / 365,
        "rho_pct": K * T * exp(-r * T) * Nd2 / 100,
        "vanna": -exp(-q * T) * pdf * d2 / sigma,
        "volga": vega * d1 * d2 / sigma,
    }

print(greeks(100, 100, 1.0, 0.05, 0.2))
```

## Pitfalls

- Mixing units: vega per 1.00 versus per vol point, theta per year versus per calendar or trading day; always say which.
- Adding raw deltas across different underlyings; convert to dollar or beta-weighted delta first.
- Thinking theta is a cost you can avoid: in Black-Scholes it is exactly the price of the gamma you own.
- Hedging gamma with a different expiry and assuming vega is hedged too; $\mathcal{V} = \sigma S^2\tau\Gamma$ says it is not.
- Forgetting that Greeks are model and smile dependent: a sticky-strike versus sticky-delta assumption changes delta through the vanna term.
- Using Black-Scholes theta near expiry or around events without adjusting the clock; weekend and holiday theta is a convention, not a law.
- Reading a big P&L-explain residual as noise; it usually signals an unmodelled risk or a data problem.

## Interview questions

> [!question]- deriv-greeks-call-delta-formula | What is the Black-Scholes delta of a call and of a put with dividend yield $q$?
> Call $e^{-q\tau}N(d_1)$, put $-e^{-q\tau}N(-d_1) = e^{-q\tau}(N(d_1) - 1)$.
> Differentiate the price; the $\partial d_i/\partial S$ terms cancel because $S e^{-q\tau}\varphi(d_1) = K e^{-r\tau}\varphi(d_2)$.

> [!question]- deriv-greeks-gamma-same-call-put | Why do a call and a put with the same strike and expiry have the same gamma and vega?
> Put-call parity: $C - P = S e^{-q\tau} - K e^{-r\tau}$ is linear in $S$ and independent of $\sigma$.
> Its second derivative in $S$ and its derivative in $\sigma$ are zero, so the call and put share them.

> [!question]- deriv-gamma-theta-relation | State the gamma-theta relationship and its trading meaning.
> For a delta-hedged option with zero rates, $\Theta = -\tfrac12\sigma^2 S^2\Gamma$.
> Long gamma earns $\tfrac12\Gamma\,\delta S^2$ on moves and pays theta as rent; they balance when realised variance equals implied variance.

> [!question]- deriv-atm-greek-rules-of-thumb | Give quick approximations for ATM gamma, vega and theta.
> $\Gamma \approx 0.4/(S\sigma\sqrt{T})$, vega $\approx 0.4\,S\sqrt{T}$ per 1.00 of vol, $\Theta \approx -0.2\,S\sigma/\sqrt{T}$ per year.
> All come from $\varphi(0) \approx 0.4$ with $d_1 \approx 0$; theta follows from $-\tfrac12\sigma^2S^2\Gamma$.

> [!question]- deriv-vega-gamma-relation | How are vega and gamma related in Black-Scholes, and what does it imply for hedging?
> $\mathcal{V} = \sigma S^2\tau\,\Gamma$.
> For equal gamma, vega scales with time to expiry, so gamma hedging with short-dated options leaves most of the vega of long-dated positions.

> [!question]- deriv-gamma-near-expiry | What happens to the gamma of ATM and OTM options as expiry approaches?
> ATM gamma blows up like $1/\sqrt{\tau}$; OTM and ITM gamma go to zero.
> The payoff kink at $K$ concentrates all the convexity in an ever narrower spot range.

> [!question]- deriv-breakeven-move | A 100 stock, 20% implied vol: what one-day move makes a long ATM straddle's delta-hedged P&L break even?
> About 1.05 dollars, $S\sigma/\sqrt{365}$ on a calendar-day theta (about 1.26, $S\sigma/\sqrt{252}$, on a 252-day clock).
> Setting $\tfrac12\Gamma\,\delta S^2 = -\Theta\,\delta t$ with $\Theta = -\tfrac12\sigma^2S^2\Gamma$ gives $\delta S = S\sigma\sqrt{\delta t}$, independent of gamma.

> [!question]- deriv-vanna-meaning | What is vanna and why does it matter to an options market maker?
> $\partial^2 V/\partial S\,\partial\sigma$: how delta changes when vol moves (equivalently how vega changes with spot).
> With spot-vol correlation (equity skew) vol rises as spot falls, so vanna makes your hedge delta wrong in exactly the moves that matter; OTM calls have positive vanna, OTM puts negative.

> [!question]- deriv-volga-meaning | What is volga and where is it largest?
> $\partial^2 V/\partial\sigma^2 = \mathcal{V}d_1d_2/\sigma$, the convexity of price in vol; near zero ATM and positive in the wings.
> Long wings are long vol-of-vol, so they command a premium, which is one reason implied vol smiles upward away from ATM.

> [!question]- deriv-charm-meaning | What is charm, and which way does an OTM call's delta drift overnight?
> Charm is $\partial\Delta/\partial t$, the delta change from the passage of time with spot fixed; OTM call deltas decay toward 0.
> With $r = q = 0$, $\partial\Delta/\partial t = \varphi(d_1)d_2/(2\tau)$, and $d_2 < 0$ for OTM calls.

> [!question]- deriv-dollar-gamma | Define dollar (1%) gamma and compute the P&L of a 2% move for a book with 50,000 dollars of it.
> Dollar gamma $= \Gamma S^2/100$ (times position size), the change in dollar delta for a 1% move; a 2% move earns $\tfrac12 \times 50{,}000 \times 2 \times 2\% = 1{,}000$ dollars.
> P&L $= \tfrac12\Gamma\,\delta S^2 = \tfrac12 (\Gamma S^2/100)\times 100 \times (\delta S/S)^2$, which is $\tfrac12 \times$ dollar gamma $\times$ (move in percent) $\times$ (move as a fraction).

> [!question]- deriv-pnl-explain-terms | Write the second-order P&L explain for an option position.
> $\delta V \approx \Delta\,\delta S + \tfrac12\Gamma\,\delta S^2 + \mathcal{V}\,\delta\sigma + \Theta\,\delta t + \text{vanna}\,\delta S\,\delta\sigma + \tfrac12\text{volga}\,\delta\sigma^2 + \rho\,\delta r$.
> A large residual versus full revaluation signals a missing risk factor, a big jump, or a booking error.

> [!question]- deriv-positive-theta-option | Can a long European option have positive theta?
> Yes: a deep in-the-money European put (and a deep ITM call with a high dividend yield).
> Its value is close to $K e^{-r\tau} - S$, which rises toward $K - S$ as time passes because the strike is discounted less.

> [!question]- deriv-gamma-hedge-book | You are short 50 one-year ATM calls ($\Gamma = 0.0198$). How many three-month ATM calls ($\Gamma = 0.0398$) flatten gamma, and what happens to vega?
> About 25 contracts; vega only falls by about a quarter.
> $50 \times 0.0198/0.0398 \approx 25$, and each three-month call has half the one-year vega ($\sqrt{0.25}$), so 25 of them cancel $25 \times 0.5 = 12.5$ of the 50 contracts' vega.

## In this repo and SDE-Interview-Prep

- Code: [greeks_visualization.ipynb](code/greeks_visualization.ipynb).
- Uses: [Delta Hedging and Gamma Scalping](06-Delta-Hedging-and-Gamma-Scalping.md), [PnL Attribution and Greek Risk](../11-Risk-and-Trading/06-PnL-Attribution-and-Greek-Risk.md), [Options Market Making](../08-Market-Making/07-Options-Market-Making.md).

## Further reading

- Sheldon Natenberg, *Option Volatility and Pricing*, chapters on option risk measurement and spreads.
- John Hull, *Options, Futures, and Other Derivatives*, chapter on the Greek letters.
- Nassim Nicholas Taleb, *Dynamic Hedging: Managing Vanilla and Exotic Options*, on higher-order Greeks, dollar Greeks and hedging in practice.
