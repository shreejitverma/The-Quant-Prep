---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [forwards-futures-and-carry]
est_hours: 3
sources: [John Hull - Options Futures and Other Derivatives (properties of stock options and trading strategies chapters), Sheldon Natenberg - Option Volatility and Pricing (synthetics conversions reversals and boxes), R. C. Merton (1973) - Theory of rational option pricing - Bell Journal of Economics 4(1), Breeden and Litzenberger (1978) - Prices of state-contingent claims implicit in option prices - Journal of Business 51(4)]
---

# Option Payoffs and Put-Call Parity

## TL;DR

- European put-call parity: $C - P = S e^{-qT} - K e^{-rT} = e^{-rT}(F - K)$; long call plus short put is a forward struck at $K$.
- Every synthetic follows from parity: stock = call $-$ put $+$ bond; covered call = short put $+$ bond; a box pays $K_2 - K_1$ for sure and so is a zero-coupon bond.
- Model-free bounds: $\max(S e^{-qT} - K e^{-rT}, 0) \le C \le S e^{-qT}$ and $\max(K e^{-rT} - S e^{-qT}, 0) \le P \le K e^{-rT}$.
- Call prices are decreasing and convex in strike with slope in $[-e^{-rT}, 0]$; a negative butterfly or a call spread worth more than the discounted strike gap is an arbitrage.
- Never exercise an American call early on a non-dividend stock; exercise can be optimal just before an ex-dividend date, and for deep in-the-money American puts because of interest on the strike.
- On a desk, parity is how you quote: conversions and reversals price the forward (financing, dividends, borrow), and $-\partial C/\partial K$ is the digital while $\partial^2 C/\partial K^2$ is the risk-neutral density.

## Learning objectives

- Draw payoff diagrams for any combination of calls, puts and stock.
- Derive put-call parity and use it to find arbitrage, synthetic positions and boxes.
- State model-free bounds on option prices, convexity in strike, and monotonicity.
- Explain when early exercise of an American call or put is optimal.

## Core concepts

### Payoffs

At expiry, with $x^+ = \max(x, 0)$:

| Position | Payoff at $T$ | Shape |
| :--- | :--- | :--- |
| Long call | $(S_T - K)^+$ | flat then slope $+1$ |
| Long put | $(K - S_T)^+$ | slope $-1$ then flat |
| Straddle (call + put, same $K$) | $\lvert S_T - K \rvert$ | V at $K$ |
| Strangle ($K_1 < K_2$, put at $K_1$, call at $K_2$) | $(K_1 - S_T)^+ + (S_T - K_2)^+$ | flat-bottomed V |
| Bull call spread (long $K_1$, short $K_2$ call) | $\min((S_T - K_1)^+, K_2 - K_1)$ | ramp capped at $K_2 - K_1$ |
| Butterfly (long $K-h$, short 2 $K$, long $K+h$ calls) | tent of height $h$ at $K$ | peak at $K$ |
| Risk reversal (long call $K_2$, short put $K_1$) | $(S_T - K_2)^+ - (K_1 - S_T)^+$ | slope $+1$ in both wings |
| Covered call (long stock, short call) | $\min(S_T, K)$ | slope $+1$ then flat |

To draw any combination, add slopes: each long call adds $+1$ to the right of its strike, each long put adds $-1$ to the left, stock adds $+1$ everywhere.
Evaluate the payoff at one point, then walk strike by strike.

### Put-call parity

Portfolio A: one call plus a bond paying $K$ at $T$.
Portfolio B: one put plus $e^{-qT}$ shares (dividends reinvested so you hold one share at $T$).
Both pay $\max(S_T, K)$ at $T$, so for European options they must cost the same today:

$$
C + K e^{-rT} = P + S e^{-qT} \quad\Longleftrightarrow\quad C - P = e^{-rT}(F - K).
$$

Consequences a trader uses constantly:

- ATM-forward ($K = F$) call and put have the same price.
- Parity is model-free: it holds whatever the volatility or smile, so calls and puts at the same strike and expiry must have the same implied volatility (if the forward is right).
- Synthetics: long stock $=$ long call $-$ put $+ K e^{-rT}$; long call $=$ long put $+$ stock $- K e^{-rT}$; short put $=$ covered call $- K e^{-rT}$.
- A conversion is long stock, long put, short call (a synthetic short stock against real stock); a reversal is the opposite.
  Their prices are how option market makers trade the forward, and hence financing, dividend expectations and borrow cost.
- For hard-to-borrow stocks the effective forward is lower, so puts look rich against calls; the "violation" is the borrow fee.

For American options on a non-dividend stock parity becomes a band:

$$
S - K \le C - P \le S - K e^{-rT}.
$$

### Boxes

A box is a long $K_1$/$K_2$ call spread plus a short $K_1$/$K_2$ put spread (equivalently a synthetic long forward at $K_1$ and a synthetic short forward at $K_2$).
It pays exactly $K_2 - K_1$ at $T$, so with European exercise its price is $(K_2 - K_1)e^{-rT}$.
Boxes are traded as financing instruments; the box rate is an implied borrowing or lending rate.
With American options (single stocks) a short box can be exercised against you early, which is why boxes are done in European index options.

### Model-free bounds and strike arbitrage

For European options with $C(K)$ and $P(K)$ as functions of strike:

1. Bounds: $\max(S e^{-qT} - K e^{-rT}, 0) \le C \le S e^{-qT}$ and $\max(K e^{-rT} - S e^{-qT}, 0) \le P \le K e^{-rT}$.
2. Monotonicity: $C(K)$ is non-increasing and $P(K)$ is non-decreasing in $K$.
3. Slope: $0 \le C(K_1) - C(K_2) \le (K_2 - K_1)e^{-rT}$ for $K_1 < K_2$ (a call spread is between zero and a bond).
4. Convexity: $C(K - h) - 2C(K) + C(K + h) \ge 0$ (a butterfly has non-negative payoff so non-negative price).
5. Calendar: for American options, and for European options on a non-dividend stock with $r \ge 0$, longer expiry is worth at least as much.

Differentiating in strike gives the two most useful identities in options:

$$
-\frac{\partial C}{\partial K} = e^{-rT} Q(S_T > K) \quad (\text{digital call}), \qquad \frac{\partial^2 C}{\partial K^2} = e^{-rT} f_Q(K) \quad (\text{Breeden-Litzenberger}).
$$

A tight call spread is how desks price and hedge digitals, and a strip of butterflies recovers the risk-neutral density.

### Early exercise

American call, no dividends: never exercise early.
Parity gives $C \ge S - K e^{-rT} > S - K$ for $r > 0$, so selling the call always beats exercising it.
Intuitively, exercising early pays the strike sooner (losing interest) and throws away the put-like protection.

American call, with dividends: exercise can be optimal only immediately before an ex-dividend date.
Exercising just before ex-date $t_i$ captures the dividend $D_i$ but loses interest on the strike until the next exercise opportunity; a necessary condition (Hull) is

$$
D_i > K\left(1 - e^{-r(t_{i+1} - t_i)}\right),
$$

with $t_{i+1}$ the next ex-date or expiry, and the call must be deep enough in the money that its remaining time value is small.

American put: early exercise can be optimal at any time when the put is deep in the money and rates are positive.
Exercising receives $K$ now and earns interest on it; the remaining optionality (the stock rallying back above $K$) is worth little when $S$ is far below $K$.
There is an exercise boundary $S^*(t) < K$ below which you exercise; dividends push it lower (you wait to capture the price drop).

## Worked examples

### Example 1: a conversion arbitrage

$S = 100$, $K = 100$, $T = 1$, $r = 5\%$, no dividends.
Market: call 10.45, put 4.50.
Parity requires $C - P = 100 - 100e^{-0.05} = 4.877$, but the market has $C - P = 5.95$.
The call is rich relative to the put, so sell the call, buy the put, buy the stock (a conversion), financing it by borrowing $K e^{-rT} = 95.12$:

- Cash today: $+10.45 - 4.50 - 100 + 95.12 = +1.07$.
- At expiry the put-call pair delivers the stock for exactly 100 whatever happens, which repays the loan.

Riskless profit 1.07 today.
For reference, Black-Scholes at 20% volatility gives $C = 10.45$, $P = 5.57$, and $5.57 - 4.50 = 1.07$ is the same mispricing.
Before calling it an arbitrage check dividends, borrow cost, and that the options are European.

### Example 2: box spread as a loan

European index options, $K_1 = 95$, $K_2 = 105$, six months, $r = 4\%$.
Fair box value: $10 e^{-0.02} = 9.802$.
If the box trades at 9.75, the implied rate is $-\ln(0.975)/0.5 = 5.06\%$.
Selling the box at 9.75 borrows 9.75 today and repays 10 in six months at 5.06%; buying it lends at 5.06%, which beats 4% so a cash-rich desk buys it.

### Example 3: butterfly arbitrage

Same-expiry calls: $K = 90$ at 14.00, $K = 100$ at 8.00, $K = 110$ at 1.50.
Butterfly cost: $14.00 - 2 \times 8.00 + 1.50 = -0.50$.
Buying it receives 0.50 today for a payoff that is never negative (a tent of height 10 at 100), so it is a pure arbitrage.
Check the other constraint too: call spread 90/100 costs 6.00, within $[0, 10e^{-rT}]$, fine; the 100/110 spread costs 6.50, also fine; the violation is convexity only.

### Example 4: deep in-the-money American put

$S = 10$, $K = 100$, $r = 5\%$, one year, no dividends.
Exercising now yields 90.
A European put is worth $K e^{-rT} - S + C$ by parity, and the call is worthless here (Black-Scholes at 20% volatility gives a put of 85.12 to the cent), so the European put is $95.12 - 10 = 85.12$.
So the American put is worth 90 (exercise), and holding it would give up $90 - 85.12 = 4.88$ of interest on the strike.

### Example 5: dividend and the American call

$K = 100$, $r = 5\%$, a dividend of 2 goes ex in three months' time with no further dividend before expiry three months later.
Threshold: $K(1 - e^{-0.05 \times 0.25}) = 1.24$.
The dividend 2 exceeds 1.24, so early exercise just before the ex-date can be optimal.
To decide, compare exercising ($S - K$) with holding: after the ex-date the call is worth, by parity, $(S - D) - K e^{-r\tau} + P$, where $P$ is the European put on the ex-dividend stock.
Exercise if and only if $P < D - K(1 - e^{-r\tau}) = 2 - 1.24 = 0.76$, which happens when the call is deep enough in the money that the put is cheap.
With a dividend of 1 the right-hand side is negative and early exercise is never optimal.

```python
from math import exp, log

def parity_gap(C, P, S, K, r, T, q=0.0):
    """Market C - P minus the parity value; positive means calls rich (sell conversion)."""
    return (C - P) - (S * exp(-q * T) - K * exp(-r * T))

print(parity_gap(10.45, 4.50, 100, 100, 0.05, 1.0))  # 1.07
print(-log(9.75 / 10) / 0.5)                          # box implied rate 0.0506
print(14.00 - 2 * 8.00 + 1.50)                        # butterfly -0.50: arbitrage
```

## Pitfalls

- Forgetting to discount the strike: parity uses $K e^{-rT}$, and the ATM options with equal prices are ATM-forward, not ATM-spot.
- Calling a parity gap on a single stock an arbitrage without checking dividends, borrow fees and early exercise; most apparent violations are hard-to-borrow names or dividend risk.
- Applying European parity to American options; it only holds as the band $S - K \le C - P \le S - K e^{-rT}$.
- Saying "never exercise an American option early"; true for calls without dividends, false for deep ITM puts and for calls before a large dividend.
- Missing the dividend-exercise risk in a short call: if a counterparty fails to exercise before ex-date, the short gains; if you forget, you lose the dividend.
- Checking convexity only on equally spaced strikes; with unequal spacing the butterfly weights must be adjusted: $(K_3 - K_2)C_1 - (K_3 - K_1)C_2 + (K_2 - K_1)C_3 \ge 0$.
- Treating a short American box as riskless; early exercise of a short leg can leave you with stock and margin calls.

## Interview questions

> [!question]- deriv-put-call-parity-statement | State European put-call parity with a continuous dividend yield $q$.
> $C - P = S e^{-qT} - K e^{-rT} = e^{-rT}(F - K)$.
> A call plus a bond paying $K$ and a put plus $e^{-qT}$ shares both pay $\max(S_T, K)$ at expiry.

> [!question]- deriv-parity-atm-forward | Which strike makes the European call and put prices equal?
> $K = F = S e^{(r-q)T}$, the forward.
> Parity gives $C - P = e^{-rT}(F - K)$, which is zero only at the forward, not at spot.

> [!question]- deriv-conversion-arbitrage | $S = 100$, $K = 100$, $T = 1$, $r = 5\%$, no dividends; call 10.45, put 4.50. What do you trade and what do you make?
> Sell the call, buy the put, buy the stock financed by borrowing 95.12 (a conversion); lock in 1.07 today.
> Parity needs $C - P = 4.88$ but the market has 5.95, so the call is rich versus the put.

> [!question]- deriv-box-spread-value | What is a European 90/110 box worth with one year to expiry and $r = 5\%$?
> $20 e^{-0.05} = 19.02$.
> Long call spread plus short put spread pays exactly $K_2 - K_1 = 20$ in every state, so it is a zero-coupon bond.

> [!question]- deriv-call-price-bounds | Give model-free lower and upper bounds on a European call.
> $\max(S e^{-qT} - K e^{-rT}, 0) \le C \le S e^{-qT}$.
> The call is worth at least the forward-struck payoff (by parity, since $P \ge 0$) and at most the share, which dominates the payoff.

> [!question]- deriv-butterfly-convexity | Calls at strikes 90, 100, 110 trade at 14, 8, 1.5. Is there an arbitrage?
> Yes: the butterfly costs $14 - 16 + 1.5 = -0.5$, so buy it and receive 0.50 for a non-negative payoff.
> Call prices must be convex in strike.

> [!question]- deriv-call-spread-slope-bound | Why must $C(K_1) - C(K_2) \le (K_2 - K_1)e^{-rT}$ for $K_1 < K_2$?
> The call spread pays at most $K_2 - K_1$, so it cannot cost more than a bond paying that amount.
> Equivalently $\partial C/\partial K \ge -e^{-rT}$, since $-\partial C/\partial K$ is a digital price bounded by the discount factor.

> [!question]- deriv-digital-from-call-spread | How do you price a European digital call paying 1 if $S_T > K$ using vanillas?
> It is $-\partial C/\partial K = e^{-rT}Q(S_T > K)$, replicated by a tight call spread $[C(K - h) - C(K + h)]/(2h)$.
> With a smile the digital also picks up a skew term, $-\partial C_{BS}/\partial K - \text{vega} \cdot \partial\sigma/\partial K$.

> [!question]- deriv-breeden-litzenberger | How do you extract the risk-neutral density from option prices?
> $f_Q(K) = e^{rT}\,\partial^2 C/\partial K^2$ (Breeden-Litzenberger).
> A butterfly centred at $K$ with wings $h$ and scaled by $1/h^2$ pays approximately a unit density at $K$.

> [!question]- deriv-american-call-no-early-exercise | Why is it never optimal to exercise an American call on a non-dividend stock early?
> Because $C \ge S - K e^{-rT} > S - K$ when $r > 0$, so selling (or holding) the call is worth more than exercising.
> Early exercise pays the strike sooner, losing interest, and gives up the protection of the implicit put.

> [!question]- deriv-american-call-dividend-exercise | When can early exercise of an American call be optimal, and what is the necessary condition?
> Only just before an ex-dividend date, when $D > K(1 - e^{-r\tau})$ with $\tau$ the time to the next ex-date or expiry, and the call is deep in the money.
> You gain the dividend but lose interest on the strike and the remaining time value.

> [!question]- deriv-american-put-early-exercise | Why can it be optimal to exercise an American put early even with no dividends?
> Deep in the money, receiving $K$ now and earning interest on it outweighs the small remaining optionality.
> Example: $S = 10$, $K = 100$, $r = 5\%$, $T = 1$: exercise gives 90 while the European put (no exercise before $T$) is worth about $95.12 - 10 = 85.12$.

> [!question]- deriv-american-parity-band | What does put-call parity become for American options on a non-dividend stock?
> $S - K \le C - P \le S - K e^{-rT}$.
> The American call equals the European call, while the American put is worth at least the European put, which moves the equality into a band.

> [!question]- deriv-covered-call-synthetic | What is a covered call equivalent to?
> A short put at the same strike plus a bond paying $K$ (cash-secured short put).
> By parity, $S - C = K e^{-rT} - P$; both pay $\min(S_T, K)$.

## In this repo and SDE-Interview-Prep

- Prev: [Forwards, Futures and Carry](01-Forwards-Futures-and-Carry.md). Next: [Binomial Trees](03-Binomial-Trees.md).
- Strategies built from these payoffs: [Option Strategies and Volatility Trading](13-Option-Strategies-and-Volatility-Trading.md).

## Further reading

- John Hull, *Options, Futures, and Other Derivatives*, chapters on properties of stock options and trading strategies involving options.
- Sheldon Natenberg, *Option Volatility and Pricing*, chapters on synthetics, conversions, reversals and boxes, and early exercise.
- R. C. Merton (1973), "Theory of rational option pricing", *Bell Journal of Economics and Management Science* 4(1).
- D. T. Breeden and R. H. Litzenberger (1978), "Prices of state-contingent claims implicit in option prices", *Journal of Business* 51(4).
