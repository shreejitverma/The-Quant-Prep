---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: []
est_hours: 3
sources: [John Hull - Options Futures and Other Derivatives (futures mechanics and forward pricing and interest rate futures chapters), Cox Ingersoll and Ross (1981) - The relation between forward prices and futures prices - Journal of Financial Economics 9(4)]
---

# Forwards, Futures and Cost of Carry

## TL;DR

- No-arbitrage forward price: $F_0 = S_0 e^{(r - q)T}$, or $S_0 e^{(r + u - y)T}$ for commodities with storage $u$ and convenience yield $y$; with discrete dividends $F_0 = (S_0 - PV(D))e^{rT}$.
- The forward price is not a forecast: it is the spot price plus the net cost of carrying the asset until delivery.
- If $F$ is too high do cash-and-carry (borrow, buy spot, sell forward); if too low do reverse cash-and-carry (short spot, lend, buy forward).
- Futures settle daily; with deterministic rates futures and forward prices are equal, and when the underlying is positively correlated with rates the futures price is higher.
- Rate futures need a convexity adjustment: forward rate $\approx$ futures rate $- \tfrac12 \sigma^2 T_1 T_2$ under Ho-Lee.
- Desks read futures as a financing market: the basis tells you the implied repo rate or implied dividend, and trading the basis is trading carry.

## Learning objectives

- Price forwards by no-arbitrage with dividends, storage and convenience yield.
- Explain futures versus forwards, daily settlement and the convexity adjustment.
- Trade the basis and understand cash-and-carry arbitrage.

## Core concepts

### Forward contracts and the replication argument

A forward is an agreement today to buy the asset at time $T$ for price $K$, with no cash exchanged at inception.
The payoff at $T$ is $S_T - K$ for the long.

Replicate it: buy one unit of the asset today for $S_0$ and borrow $S_0$ at the risk-free rate $r$ (continuous compounding).
At $T$ you own the asset and owe $S_0 e^{rT}$, so you hold a synthetic long forward struck at $S_0 e^{rT}$.
Any other forward price is an arbitrage, so for an asset with no income:

$$
F_0 = S_0 e^{rT}.
$$

The general cost-of-carry rule adds everything you pay to hold the asset and subtracts everything it pays you:

| Asset | Carry | Forward price |
| :--- | :--- | :--- |
| Non-dividend stock | financing $r$ | $S_0 e^{rT}$ |
| Index with dividend yield $q$ | $r - q$ | $S_0 e^{(r-q)T}$ |
| Stock with discrete dividends | financing minus dividends | $(S_0 - PV(D))e^{rT}$ |
| Currency (foreign rate $r_f$) | $r_d - r_f$ | $S_0 e^{(r_d - r_f)T}$ (covered interest parity) |
| Commodity with storage $u$ and convenience yield $y$ | $r + u - y$ | $S_0 e^{(r + u - y)T}$ |
| Short stock with borrow fee $b$ | $r - q - b$ | $S_0 e^{(r - q - b)T}$ |

The value at time $t$ of an existing long forward struck at $K$ is the discounted difference between today's forward and the strike:

$$
f_t = (F_t - K) e^{-r(T-t)} = S_t e^{-q(T-t)} - K e^{-r(T-t)}.
$$

### Convenience yield, contango and backwardation

For consumption commodities (oil, gas, grains) you cannot short the physical easily, so the arbitrage is one-sided: $F_0 \le S_0 e^{(r+u)T}$.
The shortfall is expressed as a convenience yield $y$, the benefit of physically holding inventory when supply is tight.
A curve is in contango when futures rise with maturity (carry $r + u - y > 0$) and in backwardation when they fall (tight inventory, high $y$).
A long futures position rolled forward earns roll yield when the curve is backwardated (buy cheap far contracts that roll up to spot) and pays it in contango.

### Futures versus forwards

- Futures are exchange-traded and standardised, cleared by a central counterparty, and marked to market daily: gains and losses are paid in cash as variation margin every day.
- Forwards are OTC, bilateral, settle once at maturity and carry counterparty credit risk (mitigated today by collateral agreements).
- Under the risk-neutral measure the futures price is a martingale, $\text{Fut}_t = E^Q[S_T \mid \mathcal{F}_t]$, while the forward price is the expectation under the $T$-forward measure.
- If interest rates are deterministic the two measures give the same expectation, so futures and forward prices coincide (Cox, Ingersoll and Ross 1981).
- If the underlying is positively correlated with rates, a long futures receives margin when rates are high (reinvested at high rates) and pays when rates are low (financed cheaply), so the long prefers futures and $\text{Fut} > F$.
- For equity and FX futures under a few months the difference is negligible; for long-dated rate futures it is material.

### Convexity adjustment for rate futures

A SOFR or legacy Eurodollar future is quoted as $100 -$ rate, so the long loses when rates rise and gains when they fall.
Daily settlement means the short (who gains when rates rise) reinvests those gains at high rates, so the futures rate must exceed the forward rate to compensate.
Under the Ho-Lee model with normal short-rate volatility $\sigma$, for a futures on the rate from $T_1$ to $T_2$:

$$
\text{forward rate} = \text{futures rate} - \tfrac12 \sigma^2 T_1 T_2.
$$

The adjustment grows roughly with the square of maturity, which is why it matters for the back of the strip and not the front.

### Hedging with futures: tailing

Because futures settle daily, a hedge that matches the forward exposure should be scaled down by the discount factor to the delivery date: hedge $N e^{-r(T-t)}$ futures instead of $N$.
Daily variation margin on a gain of $\Delta$ is received now, not at $T$, so it is worth $e^{r(T-t)}$ times more than the same gain on a forward.

### The basis and carry trades

Hull defines basis as spot minus futures; many equity desks quote futures minus spot (the "premium"), so always state the sign.
The basis converges to zero at delivery.
Given a traded futures price, the carry relation can be inverted:

- Implied repo (financing) rate: $r_{\text{impl}} = q + \ln(F/S)/T$, compared with the desk's actual funding to decide whether to do cash-and-carry.
- Implied dividend yield: $q_{\text{impl}} = r - \ln(F/S)/T$, the number options and delta-one desks actually trade.
- A basis trade (long cash index, short futures, or the reverse) is a bet on financing and dividends, not on direction.

## Worked examples

### Example 1: forward on a dividend-paying stock

Stock at 100, $r = 5\%$ continuous, one year to delivery.

With a continuous dividend yield of 2%: $F = 100 e^{0.03} = 103.05$.

With a single cash dividend of 2 paid at six months instead:
$PV(D) = 2 e^{-0.05 \times 0.5} = 1.951$, so $F = (100 - 1.951) e^{0.05} = 103.08$.

Interview narration: "I own the stock financed at 5%, which costs about 5.13 over the year, and I get back a dividend worth 1.95 today, so the forward is spot plus net carry."

### Example 2: cash-and-carry arbitrage in gold

Gold spot 2000, $r = 4\%$, storage cost 0.5% per year as a continuous yield, one-year futures quoted at 2120.

Fair value: $F = 2000 e^{0.045} = 2092.06$.
The futures is 27.94 rich, so:

1. Borrow 2000, buy one ounce of gold, pay storage.
2. Sell the one-year futures at 2120.
3. At expiry deliver the gold for 2120; repay the loan plus storage, which together cost 2092.06.

Locked-in profit: $2120 - 2092.06 = 27.94$ per ounce at $T$.
If instead the futures were quoted at 2050, reverse: borrow and sell gold (or lend out existing inventory), invest the cash, buy the futures, profit $2092.06 - 2050 = 42.06$.
For gold the reverse leg works because large holders lend gold; for crude oil it usually does not, which is why convenience yield exists.

### Example 3: valuing an existing forward

You are long a forward struck at 100 with six months left; spot is now 105, $r = 4\%$, no dividends.

$$
f = S - K e^{-rT} = 105 - 100 e^{-0.02} = 6.98.
$$

Not 5: you also benefit from paying 100 later rather than now.

### Example 4: implied dividend from an index future

Index at 5000, three-month futures at 5030, $r = 5\%$.

$$
q_{\text{impl}} = r - \frac{\ln(5030/5000)}{0.25} = 0.05 - 0.02393 = 2.61\%.
$$

If your dividend forecast is 3%, the futures is too rich (it implies too few dividends): sell futures, buy the basket, and you are long dividends.

### Example 5: convexity adjustment

SOFR future on the three-month rate starting in 5 years ($T_1 = 5$, $T_2 = 5.25$), normal rate volatility 1% (100bp per year).

$$
\tfrac12 \sigma^2 T_1 T_2 = 0.5 \times 0.0001 \times 5 \times 5.25 = 0.00131 = 13.1\text{bp}.
$$

The forward rate is 13.1bp below the futures rate; ignoring this misprices a 5-year swap built off futures.

### Example 6: variation margin

Long 10 E-mini S&P futures (multiplier 50) at 5000.
Day 1 settles at 5030: receive $30 \times 50 \times 10 = 15{,}000$.
Day 2 settles at 4990: pay $40 \times 50 \times 10 = 20{,}000$.
Cumulative P&L of $-5{,}000$ equals $(4990 - 5000) \times 500$, but the timing of cash flows differs from a forward, which is exactly the source of the futures-forward difference.

```python
from math import exp, log

def forward(S, r, q, T, pv_divs=0.0, storage=0.0, conv_yield=0.0):
    """Cost-of-carry forward price with continuous rates."""
    return (S - pv_divs) * exp((r - q + storage - conv_yield) * T)

print(forward(100, 0.05, 0.02, 1.0))                  # 103.05
print(forward(2000, 0.04, 0.0, 1.0, storage=0.005))   # 2092.06
print(0.05 - log(5030 / 5000) / 0.25)                 # implied q 0.0261
```

## Pitfalls

- Treating the forward as the market's forecast of $S_T$; it is pinned by carry, whatever anyone expects.
- Forgetting that the value of a forward at inception is zero, while its price (the delivery price) is not.
- Mixing compounding conventions: $S(1 + rT)$ and $S e^{rT}$ differ, and FX desks quote money-market rates on act/360.
- Applying cash-and-carry in reverse to consumption commodities; you cannot short physical crude, so only the upper bound binds.
- Ignoring stock borrow cost: for hard-to-borrow names the forward (and hence put-call parity) embeds the borrow fee, and apparent "arbitrage" is just the fee.
- Assuming futures equal forwards for long-dated rate contracts; the convexity adjustment is several basis points and grows with $T_1 T_2$.
- Getting the basis sign wrong; say "futures minus spot" or "spot minus futures" explicitly.
- Hedging a forward exposure with an untailed futures position; the daily settlement makes the hedge slightly too large.

## Interview questions

> [!question]- deriv-forward-price-dividend-yield | What is the forward price of an asset with spot $S$, rate $r$ and continuous dividend yield $q$ for delivery at $T$?
> $F = S e^{(r-q)T}$.
> Buy $e^{-qT}$ units, reinvest dividends so you hold one unit at $T$, finance $S e^{-qT}$ at $r$; you owe $S e^{(r-q)T}$ at $T$, so any other forward price is an arbitrage.

> [!question]- deriv-forward-not-forecast | Is the forward price the market's expectation of the future spot price?
> No, it is the spot plus net cost of carry.
> Replication pins it regardless of views; it equals the risk-neutral expectation, not the real-world one, which includes a risk premium.

> [!question]- deriv-cash-and-carry-arb | Spot 100, $r = 5\%$, no dividends, one-year forward trades at 108. What is the arbitrage and the profit?
> Cash-and-carry: borrow 100, buy the asset, sell the forward at 108; profit $108 - 100e^{0.05} = 108 - 105.13 = 2.87$ at $T$.
> At expiry deliver the asset for 108 and repay 105.13.

> [!question]- deriv-value-existing-forward | You are long a forward struck at $K$; what is it worth at time $t$?
> $f_t = (F_t - K)e^{-r(T-t)} = S_t e^{-q(T-t)} - K e^{-r(T-t)}$.
> Enter an offsetting short forward at today's $F_t$; the locked-in difference $F_t - K$ is received at $T$, so discount it.

> [!question]- deriv-convenience-yield | What is a convenience yield and why do only consumption commodities have one?
> The implied benefit of holding physical inventory, defined by $F = S e^{(r + u - y)T}$.
> For consumption assets you cannot short or lend the physical, so the reverse cash-and-carry fails and futures can sit below full carry; $y$ measures that gap and spikes when inventory is scarce.

> [!question]- deriv-contango-backwardation-roll | A long-only commodity index rolls front-month futures. In which curve shape does it earn positive roll yield?
> Backwardation.
> It buys the next contract below spot and, if the curve is unchanged, that contract rolls up toward spot; in contango it buys above spot and bleeds as the contract rolls down.

> [!question]- deriv-futures-vs-forward-price | When is a futures price above the forward price for the same delivery date?
> When the underlying is positively correlated with interest rates.
> The long futures receives variation margin when rates are high (reinvested at high rates) and pays when rates are low (borrowed cheaply); with deterministic rates the two prices are equal.

> [!question]- deriv-convexity-adjustment-ho-lee | Give the Ho-Lee convexity adjustment between a rate futures and the forward rate, and compute it for $T_1 = 4$, $T_2 = 4.25$, $\sigma = 1\%$.
> Forward rate = futures rate $- \tfrac12\sigma^2 T_1 T_2 = 0.5 \times 0.0001 \times 4 \times 4.25 = 8.5$bp below the futures rate.
> The short futures gains when rates rise and reinvests those gains at high rates, so the futures rate is biased up.

> [!question]- deriv-implied-dividend-from-futures | Index 4000, six-month futures 4030, $r = 4\%$. What dividend yield is implied?
> $q = r - \ln(4030/4000)/0.5 = 0.04 - 0.01496 = 2.50\%$.
> Invert $F = S e^{(r-q)T}$.

> [!question]- deriv-futures-tailing-hedge | Why do you hedge a forward-dated exposure of $N$ units with only $N e^{-r(T-t)}$ futures?
> Because futures gains and losses are paid daily, so each unit of futures P&L arrives earlier and is worth $e^{r(T-t)}$ units of P&L at $T$.
> Tailing scales the hedge by the discount factor so the present values match.

> [!question]- deriv-covered-interest-parity | EURUSD spot 1.10, USD rate 5%, EUR rate 3% (continuous). What is the one-year forward?
> $1.10 e^{0.05 - 0.03} = 1.1222$.
> Covered interest parity: the currency with the higher interest rate trades at a forward discount, so the euro (lower rate) is at a forward premium.

> [!question]- deriv-hard-to-borrow-forward | Why can a hard-to-borrow stock's forward sit well below $S e^{(r-q)T}$ without arbitrage?
> Because the reverse cash-and-carry requires shorting the stock, which costs a borrow fee $b$, so the true carry is $r - q - b$.
> The same fee shows up as puts looking rich versus calls in put-call parity.

## In this repo and SDE-Interview-Prep

- Next: [Option Payoffs and Put-Call Parity](02-Option-Payoffs-and-Put-Call-Parity.md) uses the forward as the anchor for parity.
- Related: [Commodities and Futures Curves](../06-Fixed-Income-and-Asset-Classes/09-Commodities-and-Futures-Curves.md), [FX Markets and Interest Rate Parity](../06-Fixed-Income-and-Asset-Classes/07-FX-Markets-and-Interest-Rate-Parity.md), [ETF and Futures Market Making](../08-Market-Making/08-ETF-and-Futures-Market-Making.md).

## Further reading

- John Hull, *Options, Futures, and Other Derivatives*, chapters on futures markets, forward and futures pricing, and interest rate futures.
- J. C. Cox, J. E. Ingersoll and S. A. Ross (1981), "The relation between forward prices and futures prices", *Journal of Financial Economics* 9(4).
