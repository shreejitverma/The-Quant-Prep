---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [black-scholes-derivation, binomial-trees]
est_hours: 4
sources: [John Hull - Options Futures and Other Derivatives (Black-Scholes-Merton model chapter), Sheldon Natenberg - Option Volatility and Pricing (volatility and theoretical pricing chapters), Black and Scholes (1973) - The pricing of options and corporate liabilities - Journal of Political Economy 81(3), Fischer Black (1976) - The pricing of commodity contracts - Journal of Financial Economics 3(1-2)]
---

# Black-Scholes Formula and Intuition

## TL;DR

- $C = S e^{-qT}N(d_1) - K e^{-rT}N(d_2) = e^{-rT}\left[F N(d_1) - K N(d_2)\right]$ with $d_{1,2} = \dfrac{\ln(F/K) \pm \tfrac12\sigma^2 T}{\sigma\sqrt{T}}$.
- $N(d_2)$ is the risk-neutral probability of finishing in the money; $N(d_1)$ is the same probability under the share measure, and $e^{-qT}N(d_1)$ is the delta.
- The drift $\mu$ never appears; only total variance $\sigma^2 T$, the forward and the discount factor matter.
- ATM-forward: $C = P \approx 0.4\, e^{-rT} F\sigma\sqrt{T}$ and the straddle $\approx 0.8\, S\sigma\sqrt{T}$, the expected absolute move.
- Rule of 16: a daily one-standard-deviation move is annual vol divided by 16 ($\sqrt{252} \approx 15.87$).
- Off ATM, move along the strike with the digital: $\partial C/\partial K = -e^{-rT}N(d_2) \approx -0.5$ near the money.

## Learning objectives

- Interpret N(d1) and N(d2) and the forward-price form of the formula.
- Use the ATM approximation C = 0.4 * sigma * sqrt(T) * S to price in your head.
- Compute option prices mentally for quick interview estimates.

## Core concepts

### The formula

Assume $dS/S = \mu\,dt + \sigma\,dW$, constant $r$, $q$, $\sigma$, frictionless trading.
The derivation (PDE by delta hedging, or risk-neutral expectation) is in [Black-Scholes Derivation](../04-Stochastic-Calculus/07-Black-Scholes-Derivation.md).
With $F = S e^{(r-q)T}$:

$$
C = e^{-rT}\left[F N(d_1) - K N(d_2)\right], \qquad P = e^{-rT}\left[K N(-d_2) - F N(-d_1)\right],
$$

$$
d_1 = \frac{\ln(F/K) + \tfrac12\sigma^2 T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}.
$$

Black (1976) is the same formula written on a futures or forward price $F$, which is how rates, commodities and index options desks actually price: take $F$ from the futures market and discount at $r$.

### What the pieces mean

Under the risk-neutral measure $\ln S_T \sim \mathcal{N}(\ln F - \tfrac12\sigma^2 T, \sigma^2 T)$.

- $N(d_2) = Q(S_T > K)$: the risk-neutral probability of exercise, and $e^{-rT}N(d_2)$ is the price of a cash-or-nothing digital.
- $S e^{-qT}N(d_1)$ is the price of an asset-or-nothing call (receive the share if $S_T > K$); $N(d_1)$ is the probability of exercise under the measure with the share as numeraire.
- So the call is "receive the stock if in the money" minus "pay the strike if in the money".
- $\partial C/\partial S = e^{-qT}N(d_1)$: the terms from differentiating $d_1$ and $d_2$ cancel because $F\varphi(d_1) = K\varphi(d_2)$.
- $N(d_1) > N(d_2)$, so delta exceeds the probability of exercise: in the states where you exercise, the stock is higher, which the share measure overweights.
- $\partial C/\partial K = -e^{-rT}N(d_2)$: moving the strike up by 1 costs the digital.

### Why the drift is missing

The option is replicated by trading the stock and the bond, so its price is the cost of the hedge, which depends on how much the stock wiggles ($\sigma$), not where it is expected to go ($\mu$).
Views on direction are already in $S$.
This is also why an options trader thinks in volatility: the price is a monotone function of $\sigma$, so implied volatility is just a quoting convention for price.

### Limits and sanity checks

- $\sigma \to 0$ or $T \to 0$: $C \to e^{-rT}(F - K)^+$, discounted intrinsic on the forward.
- $\sigma \to \infty$: $C \to S e^{-qT}$ and $P \to K e^{-rT}$, the upper bounds.
- Homogeneity: $C(\lambda S, \lambda K) = \lambda C(S, K)$, so prices depend on moneyness $K/F$ and total volatility $\sigma\sqrt{T}$ only, which is why vol surfaces are plotted against $\ln(K/F)/(\sigma\sqrt{T})$ or delta.
- Parity holds automatically: $C - P = e^{-rT}(F - K)$.

### ATM approximation

At the money forward ($K = F$), $d_{1,2} = \pm\tfrac12\sigma\sqrt{T}$, so

$$
C_{\text{ATMF}} = e^{-rT}F\left[2N\!\left(\tfrac12\sigma\sqrt{T}\right) - 1\right] \approx e^{-rT}F\,\frac{\sigma\sqrt{T}}{\sqrt{2\pi}} \approx 0.4\, e^{-rT}F\sigma\sqrt{T},
$$

using $N(x) \approx \tfrac12 + x/\sqrt{2\pi}$ and $1/\sqrt{2\pi} = 0.3989$.
The next term makes the approximation too high by a relative $\sigma^2 T/24$: 0.2% at $\sigma\sqrt{T} = 0.2$, 2.7% at $\sigma\sqrt{T} = 0.8$.

The ATM straddle is twice that, $\approx 0.8\, S\sigma\sqrt{T}$, and $0.8 \approx \sqrt{2/\pi}$ is $E\lvert Z \rvert$ for a standard normal.
So the straddle price is the market's expected absolute move to expiry, the most useful single number on an options desk (earnings moves, event pricing, breakevens).

For an option ATM-spot with non-zero rates, add the forward intrinsic with delta about one half:

$$
C_{\text{ATM spot}} \approx 0.4\, S\sigma\sqrt{T} + \tfrac12\left(S - K e^{-rT}\right).
$$

### Mental maths kit

- Time: $\sqrt{T}$ with $T$ in years; one month $\approx 0.29$, three months $0.5$, one week $\approx 0.139$, one trading day $1/15.87 \approx 0.063$.
- Daily standard deviation $\approx \sigma/16$; weekly $\approx \sigma/7.2$; monthly $\approx \sigma/3.5$.
- Moneyness in standard deviations: $\ln(K/F)/(\sigma\sqrt{T})$; beyond about 2 standard deviations the option is worth very little.
- ATM call delta is slightly above 0.5 ($N(\tfrac12\sigma\sqrt{T})$ with $r = 0$), and the ATM probability of exercise slightly below 0.5.
- Near the money, strike by strike: $C(K + \delta K) \approx C(K) - N(d_2)\,\delta K$, with the correction $+\tfrac12\,\Gamma_K\,\delta K^2$ where $\Gamma_K = \partial^2 C/\partial K^2 > 0$.

## Worked examples

### Example 1: the full formula

$S = K = 100$, $T = 1$, $r = 5\%$, $\sigma = 20\%$, $q = 0$.
$d_1 = (0 + 0.05 + 0.02)/0.2 = 0.35$, $d_2 = 0.15$.
$N(0.35) = 0.6368$, $N(0.15) = 0.5596$.
$C = 100 \times 0.6368 - 95.123 \times 0.5596 = 63.68 - 53.23 = 10.45$.
$P = C - (100 - 95.12) = 10.45 - 4.88 = 5.57$.
Reading: delta 0.64, risk-neutral exercise probability 0.56, and the call is 63.68 of expected stock received minus 53.23 of expected strike paid, both in present value.

### Example 2: pricing in your head

Stock 100, 30% vol, three months, zero rates.
ATM call $\approx 0.4 \times 100 \times 0.30 \times 0.5 = 6.00$; exact 5.98.
Straddle $\approx 0.8 \times 100 \times 0.30 \times 0.5 = 12.00$; exact 11.96.

Stock 200, 25% vol, four months: $0.4 \times 200 \times 0.25 \times 0.577 = 11.55$; exact 11.51.

At 80% vol and one year the shortcut gives 32.00 versus 31.08 exact, the $\sigma^2 T/24 \approx 2.7\%$ overestimate.

### Example 3: earnings straddle and implied move

Stock at 50; the one-week ATM straddle that includes earnings is 4.00.
Implied expected absolute move: $4/50 = 8\%$.
A one-standard-deviation move is about $8\%/0.8 = 10\%$.
Annualised with 7 calendar days: $\sigma = 4/(0.8 \times 50 \times \sqrt{7/365}) = 72\%$.
Trader's question: "Has this name historically moved more or less than 8% on earnings?" If it averages 5%, sell the straddle (and hedge); if 11%, buy it.

### Example 4: ATM spot with rates

$S = K = 100$, $T = 1$, $r = 5\%$, $\sigma = 20\%$.
$0.4 \times 100 \times 0.2 + \tfrac12(100 - 95.12) = 8.00 + 2.44 = 10.44$, against 10.45 exact.

### Example 5: sliding along the strike

Zero rates, $S = 100$, $\sigma = 20\%$, $T = 1$: the ATM call is 7.97 and $N(d_2) = N(-0.1) = 0.460$.
Estimate the 102 call: $7.97 - 0.46 \times 2 = 7.05$; exact 7.08.
The linear estimate is low because call prices are convex in strike, and it gets worse further out: at 110 the linear guess is 3.36 against 4.29 exact.

### Example 6: Black-76 on a futures

Crude futures 80, strike 75, six months, $r = 4\%$, $\sigma = 35\%$.
$d_1 = [\ln(80/75) + 0.5 \times 0.1225 \times 0.5]/(0.35\sqrt{0.5}) = 0.385$, $d_2 = 0.137$.
$C = e^{-0.02}[80 \times 0.6497 - 75 \times 0.5545] = 10.18$.

```python
from math import exp, log, sqrt
from statistics import NormalDist

N = NormalDist().cdf

def black(F, K, T, r, sigma, call=True):
    """Black-76 on the forward; for a stock use F = S * exp((r - q) * T)."""
    sd = sigma * sqrt(T)
    d1 = (log(F / K) + 0.5 * sd * sd) / sd
    d2 = d1 - sd
    if call:
        return exp(-r * T) * (F * N(d1) - K * N(d2))
    return exp(-r * T) * (K * N(-d2) - F * N(-d1))

print(black(100 * exp(0.05), 100, 1, 0.05, 0.2))   # 10.4506
print(black(100, 100, 0.25, 0.0, 0.3))             # 5.9785 vs 0.4*100*0.3*0.5 = 6.00
print(black(80, 75, 0.5, 0.04, 0.35))              # 10.1832
```

## Pitfalls

- Using the ATM approximation for an ATM-spot option with large $rT$ or $qT$ and forgetting the forward intrinsic term.
- Reading $N(d_1)$ as the probability of exercise; it is the delta, and $N(d_2)$ is the risk-neutral probability.
- Treating $N(d_2)$ as a real-world probability; it uses the risk-neutral drift and the implied (not realised) volatility.
- Mixing calendar and trading-day time: event and weekend effects mean desks often use a trading-day or weighted clock, and the vol number changes with it.
- Using the 0.4 rule for high total volatility (long-dated or very volatile names) without the downward correction.
- Plugging spot into Black-76 or a futures price into the spot formula; the forward already contains carry.
- Forgetting that Black-Scholes is a quoting device: the smile means a single $\sigma$ does not price all strikes.

## Interview questions

> [!question]- deriv-bs-call-formula | Write the Black-Scholes call price in forward form.
> $C = e^{-rT}[F N(d_1) - K N(d_2)]$, $d_{1,2} = [\ln(F/K) \pm \tfrac12\sigma^2 T]/(\sigma\sqrt{T})$, $F = S e^{(r-q)T}$.
> It is the discounted risk-neutral expectation of $(S_T - K)^+$ with lognormal $S_T$.

> [!question]- deriv-bs-nd2-meaning | What is $N(d_2)$ in Black-Scholes?
> The risk-neutral probability that the call finishes in the money, $Q(S_T > K)$.
> $e^{-rT}N(d_2)$ is the price of a digital call and equals $-\partial C/\partial K$.

> [!question]- deriv-bs-nd1-meaning | What is $N(d_1)$, and why is it larger than $N(d_2)$?
> It is the call delta (times $e^{-qT}$) and the exercise probability under the share measure.
> The share measure reweights states by $S_T/F$, which overweights high-price states where the call is exercised.

> [!question]- deriv-bs-no-drift | Why does the stock's expected return not appear in Black-Scholes?
> Because the option is replicated by dynamic trading in stock and bond, so its price is the cost of replication, which depends only on volatility.
> Any view on drift is already reflected in the stock price.

> [!question]- deriv-atm-call-approximation | Approximate an ATM-forward call and derive the constant.
> $C \approx 0.4\, e^{-rT}F\sigma\sqrt{T}$.
> At $K = F$, $C = e^{-rT}F[2N(\sigma\sqrt{T}/2) - 1]$ and $N(x) \approx \tfrac12 + x/\sqrt{2\pi}$ gives $\sigma\sqrt{T}/\sqrt{2\pi}$, with $1/\sqrt{2\pi} = 0.399$.

> [!question]- deriv-atm-straddle-expected-move | What does an ATM straddle price tell you, and how do you approximate it?
> The market's expected absolute move to expiry: straddle $\approx 0.8\, S\sigma\sqrt{T}$.
> $0.8 \approx \sqrt{2/\pi} = E\lvert Z\rvert$ for a standard normal.

> [!question]- deriv-mental-price-atm | Price a three-month ATM call on a 100 stock at 30% vol, zero rates, in your head.
> About 6.00 (exact 5.98).
> $0.4 \times 100 \times 0.3 \times \sqrt{0.25} = 6$.

> [!question]- deriv-rule-of-16 | A stock has 32% implied vol. What daily move does that imply?
> About 2% per day for one standard deviation.
> Divide annual vol by $\sqrt{252} \approx 16$.

> [!question]- deriv-earnings-implied-move | A 50 stock's one-week straddle over earnings costs 4. What move is priced?
> An expected absolute move of about 8% (4 dollars), a one-standard-deviation move of about 10%, about 72% annualised on calendar days.
> Straddle over spot is the expected absolute percentage move; divide by 0.8 for the standard deviation.

> [!question]- deriv-bs-vol-limits | What happens to a Black-Scholes call as $\sigma \to \infty$ and as $\sigma \to 0$?
> $\sigma \to \infty$: $C \to S e^{-qT}$; $\sigma \to 0$: $C \to e^{-rT}(F - K)^+$.
> Infinite volatility puts all mass near zero with a vanishing tail carrying the mean, so the strike is almost never paid; zero volatility makes $S_T = F$.

> [!question]- deriv-atm-delta-above-half | Is an ATM-forward call's delta above or below 0.5, and is its exercise probability above or below 0.5?
> Delta is above 0.5 ($N(\sigma\sqrt{T}/2)$ with $r = q = 0$) and exercise probability below 0.5 ($N(-\sigma\sqrt{T}/2)$).
> With $\sigma\sqrt{T} = 0.8$: delta 0.655, probability 0.345; lognormal skews the median below the forward.

> [!question]- deriv-strike-slide-estimate | Zero rates, spot 100, 20% vol, one year; the 100 call is 7.97. Estimate the 102 call.
> About 7.05 linearly (exact 7.08).
> $\partial C/\partial K = -N(d_2) = -N(-0.1) = -0.46$, so subtract $0.46 \times 2$; convexity in strike makes the linear estimate slightly low.

> [!question]- deriv-black-76-usage | When do you use Black-76, and what goes in for the underlying?
> For options on futures or forwards (commodities, rates, index options priced off futures), with the futures or forward price $F$ as the underlying and discounting at $r$.
> It is Black-Scholes with carry folded into $F$, so no $q$ or cost-of-carry term is needed.

## In this repo and SDE-Interview-Prep

- Derivation: [Black-Scholes Derivation](../04-Stochastic-Calculus/07-Black-Scholes-Derivation.md). Discrete version: [Binomial Trees](03-Binomial-Trees.md).
- Next: [The Greeks](05-The-Greeks.md); when one $\sigma$ is not enough: [Implied Volatility and the Smile](07-Implied-Volatility-and-the-Smile.md).
- Mental arithmetic drills: [Mental Math](../13-Interview-Playbook/02-Mental-Math.md).

## Further reading

- John Hull, *Options, Futures, and Other Derivatives*, chapter on the Black-Scholes-Merton model.
- Sheldon Natenberg, *Option Volatility and Pricing*, chapters on volatility and theoretical pricing models.
- F. Black and M. Scholes (1973), "The pricing of options and corporate liabilities", *Journal of Political Economy* 81(3).
- F. Black (1976), "The pricing of commodity contracts", *Journal of Financial Economics* 3(1-2).
