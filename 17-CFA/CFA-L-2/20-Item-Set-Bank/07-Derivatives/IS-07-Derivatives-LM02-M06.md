---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 2
title: "Aldgate Volatility Partners: Rebalancing a Short Put Book"
los: [los-07-02-k, los-07-02-l, los-07-02-m, los-07-02-n]
difficulty: 3
minutes: 12
source: mock-06
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Aldgate Volatility Partners: Rebalancing a Short Put Book

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Kofi Mensah, CFA, is the risk manager at Aldgate Volatility Partners, a London options market maker that trades US-listed equity options in US dollars.
Earlier today the desk sold 600 three-month put contracts on Calloway Biosystems, with an exercise price of 76.00, to a hedge fund client.
Each contract covers 100 shares, and the desk has not yet hedged the position.
Calloway pays no dividends, and its shares trade at 80.00.

Aldgate's pricing system values Calloway options with the Black-Scholes-Merton model, using each option's own implied volatility, a 4.00% continuously compounded risk-free rate, and three months to expiration.
Exhibit 1 reproduces the desk's risk screen.

**Exhibit 1: Calloway options, desk risk screen (share price 80.00)**

| Measure | 76 put | 86 call | 80 call |
|---|---|---|---|
| Implied volatility | 34% | 29% | 31% |
| Model value | 3.22 | 2.63 | 5.33 |
| Delta | -0.3280 | 0.3604 | 0.5565 |
| Gamma | 0.0266 | 0.0323 | 0.0318 |
| Vega (per volatility point) | 0.1445 | 0.1497 | 0.1580 |
| Theta (per calendar day) | -0.0237 | -0.0267 | -0.0311 |
| Rho (per 1% change in rate) | -0.0736 | 0.0655 | 0.0980 |

The 30-day historical volatility of Calloway returns is 27%.

Aldgate's policy requires any large short option position to be made gamma neutral and then delta neutral before the close.
The head trader, Dana Rusk, proposes to neutralize gamma by trading the 86 calls and then to neutralize the remaining delta by trading Calloway shares.
She rejects using the 80 calls because the exchange has imposed a position limit on that series.

Before the hedges are placed, Mensah wants to understand the exposure of the unhedged short put position to factors other than the share price.
The client has told the desk that it expects implied volatility on the 76 puts to rise by 2.5 volatility points over the next three calendar days, ahead of a regulatory decision on Calloway's lead drug.
Mensah asks for an estimate of the change in value of the unhedged position if that happens with the share price unchanged.

On 21 March, Rusk and a junior trader, Theo Lang, discuss the implied volatilities in Exhibit 1.

Rusk: "Quoting both options in volatility terms removes the effect of their different strikes, and the higher implied volatility on the 76 puts tells us the market is paying more for downside protection than a constant-volatility model would justify."

Lang: "The 76 put costs 3.22 and the 86 call only 2.63, so the premiums alone prove that the put has the higher implied volatility."

Lang adds that, because the historical volatility is 27%, the desk should mark every Calloway option at 27% rather than at its own implied volatility.

## Questions

1. To make the short put position gamma neutral using the 86 calls, the desk should: (LOS: los-07-02-m)
   - A. buy calls on 49,412 shares.
   - B. sell calls on 49,412 shares.
   - C. sell calls on 54,606 shares.
2. After the trade in Question 1, to make the combined position delta neutral the desk should: (LOS: los-07-02-l)
   - A. sell 1,872 shares.
   - B. sell 19,680 shares.
   - C. sell 37,488 shares.
3. Using vega and theta, the estimated change in value of the unhedged short put position under the client's volatility scenario is closest to: (LOS: los-07-02-k)
   - A. -USD 25,941.
   - B. -USD 21,675.
   - C. -USD 17,409.
4. Regarding the discussion of implied volatility, the most accurate statement is: (LOS: los-07-02-n)
   - A. Rusk is correct, because implied volatility puts options with different strikes on a common basis and the skew reflects the market's departure from constant volatility.
   - B. Lang is correct, because the higher premium of the 76 put is sufficient to show that it carries the higher implied volatility.
   - C. Lang is correct, because implied and historical volatility measure the same quantity, so all options should be marked at 27%.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The position is short puts on $600 \times 100 = 60{,}000$ shares, so its gamma is $-60{,}000 \times 0.0266 = -1{,}596$.
> Stock has zero gamma, so gamma must be set first with options: $N_H = -(-1{,}596)/0.0323 = 49{,}411.76$, buy calls on about 49,412 shares (roughly 494 contracts).
> Buying any option adds gamma, which is what a short option book needs.
> B is wrong because it drops the sign of $N_H$; selling calls would make portfolio gamma twice as negative.
> C is wrong because it sizes the call trade on delta rather than gamma, $19{,}680/0.3604 = 54{,}606$, and sells the calls, which is a delta hedge that leaves the book deeply short gamma.
> 2. **C.** The short puts have delta $-60{,}000 \times (-0.3280) = +19{,}680$, and the calls bought in Question 1 add $49{,}412 \times 0.3604 = 17{,}808.08$.
> Combined delta $= 19{,}680 + 17{,}808.08 = 37{,}488.08$, so $N_H = -37{,}488/1$: sell 37,488 shares.
> Because shares have zero gamma, the stock trade leaves gamma at $-1{,}596 + 49{,}412(0.0323) = 0.0076$, effectively neutral.
> A is wrong because it subtracts the call delta from the put position's delta, $19{,}680 - 17{,}808 = 1{,}872$, a sign error on the long calls.
> B is wrong because it hedges only the original put delta and ignores the delta added by the gamma-neutralizing calls.
> 3. **C.** Per share, a long 76 put changes by $\text{Vega} \times \Delta\sigma + \text{Theta} \times \Delta t = 0.1445(2.5) + (-0.0237)(3) = 0.36125 - 0.07110 = 0.29015$.
> The desk is short 60,000 puts, so the position changes by $-60{,}000 \times 0.29015 = -17{,}409$.
> The short position loses on the rise in volatility (short vega) but earns three days of time decay (theta works for the writer).
> A is wrong because it treats time decay as a cost to the writer, $-60{,}000 \times (0.36125 + 0.07110) = -25{,}941$.
> B is wrong because it ignores theta, $-60{,}000 \times 0.36125 = -21{,}675$.
> 4. **A.** Implied volatility is the volatility that makes the model reproduce the market price, and quoting in volatility units lets traders compare options across strikes and maturities.
> BSM assumes a single constant volatility, so a flat line across strikes is its prediction; higher implied volatility on the lower-strike puts is a skew showing that the market prices downside moves more heavily.
> B is wrong because premiums differ with moneyness and option type; the 76 put and the 86 call are not comparable in price terms, which is exactly why traders quote volatility.
> C is wrong because historical volatility looks backward at realized returns, whereas implied volatility is forward-looking and extracted from current prices, so marking at 27% would misstate the book's market value.

## Distractor design

1. B: sign of $N_H$ ignored (sign); C: hedge sized on delta instead of gamma (wrong Greek).
2. A: delta of the long calls subtracted instead of added (sign); B: delta added by the gamma hedge ignored (sequence error).
3. A: theta treated as a loss for the option writer (sign); B: theta omitted (missing term).
4. B: premium level confused with implied volatility (moneyness ignored); C: implied and historical volatility treated as the same measure (concept confusion).
