---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 2
title: "Harborview Securities: Risk Review of a Short Call Book"
los: [los-07-02-k, los-07-02-l, los-07-02-m, los-07-02-n]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Harborview Securities: Risk Review of a Short Call Book

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Priya Raman, CFA, is a market risk officer at Harborview Securities, a US broker-dealer that makes markets in listed equity options.
Before the desk's risk limits are renewed, Raman must confirm that the options desk reports its Greeks correctly and hedges within policy.
The desk head, Marcus Osei, has just sold 400 three-month call contracts on Corvex Semiconductor to a pension fund client.
Each contract covers 100 shares, and the desk has not yet hedged the position.
Corvex pays no dividends.

Harborview's pricing system values Corvex options with the Black-Scholes-Merton model, using the 30% historical volatility of Corvex returns, a 5.00% continuously compounded risk-free rate, and three months to expiration.
Exhibit 1 reproduces the desk's risk report.

Exhibit 1: Corvex options, desk risk report (share price 52.00, exercise price 50.00)

| Measure | Call | Put |
|---|---|---|
| Model value (30% volatility) | 4.52 | 1.90 |
| Market price | 4.85 | 2.23 |
| Delta | 0.6627 | -0.3373 |
| Gamma | 0.0468 | -0.0468 |
| Vega (per volatility point) | 0.0950 | 0.0950 |
| Theta (per calendar day) | -0.0197 | -0.0129 |
| Rho (per 1% change in rate) | 0.0749 | -0.0486 |
| Open interest (contracts) | 12,400 | 9,850 |

Raman's first task is to check Exhibit 1 for any figure that cannot be correct under option theory.
She then reviews Osei's two hedging proposals.

Proposal 1: Delta hedge the short call position by trading Corvex shares.

Proposal 2: Delta hedge the short call position by trading the three-month Corvex puts in Exhibit 1 instead of shares, so that no stock inventory is needed.

Corvex reports quarterly earnings after the close tomorrow, and its shares have moved by roughly USD 4 on each of its last three earnings nights.
Raman asks Osei to estimate the call price if the shares open at 56.00 tomorrow with all other inputs unchanged.

On 14 October, Osei makes two statements about the stock hedge in Proposal 1.

"Once we are delta neutral, the book has no exposure to the Corvex share price, so the earnings move does not concern me."
"If you want even more protection, we can buy extra shares after the announcement."

Raman disagrees and notes that the policy manual says residual exposure of a delta-neutral book must be managed with the appropriate instruments.

Finally, Raman compares the pricing system's values with the market prices in Exhibit 1.
She notes that the market call price is above the model value and wants to know what that says about the volatility the market is pricing.
The desk's own volatility forecast for Corvex over the next three months is 28%, and Osei asks whether the desk should add to its short call position or buy calls back at the current market price.

## Questions

1. Which figure in Exhibit 1 is inconsistent with option pricing theory? (LOS: los-07-02-k)
   - A. The put gamma.
   - B. The put rho.
   - C. The put theta.
2. Under Proposal 1, to make the position delta neutral the desk should: (LOS: los-07-02-l)
   - A. buy 26,508 shares.
   - B. buy 40,000 shares.
   - C. sell 26,508 shares.
3. Under Proposal 2, to make the position delta neutral the desk should: (LOS: los-07-02-l)
   - A. buy puts on 78,589 shares.
   - B. sell puts on 8,941 shares.
   - C. sell puts on 78,589 shares.
4. Using delta and gamma, the estimated Corvex call price if the shares open at 56.00 is closest to: (LOS: los-07-02-k)
   - A. 7.17.
   - B. 7.55.
   - C. 7.92.
5. Regarding Osei's statements about the hedged book in Proposal 1, Raman should most likely conclude that the book will: (LOS: los-07-02-m)
   - A. gain if the shares jump up and lose if they jump down, so the earnings exposure is balanced.
   - B. lose if the shares jump in either direction, and this exposure can be reduced only by buying options.
   - C. lose if the shares jump in either direction, and this exposure can be removed by buying additional shares.
6. Based on Exhibit 1 and the desk's forecast, the implied volatility of the call and the appropriate action are best described as: (LOS: los-07-02-n)
   - A. below 30%, and the desk should buy calls back.
   - B. above 30%, and the desk should buy calls back.
   - C. above 30%, and the desk should add to its short call position.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Gamma is the rate of change of delta with respect to the share price; it is always non-negative and is identical for a call and its matching put, because put-call parity makes their deltas differ by a constant.
> The put gamma should read +0.0468.
> B is wrong because put rho is negative: a higher rate lowers the present value of the exercise price the put holder receives.
> C is wrong because a smaller (less negative) put theta than call theta is normal for a non-dividend stock with a positive rate; Python on the vignette inputs gives $-0.0197$ and $-0.0129$ per day.
> 2. **A.** Portfolio delta $= -40{,}000 \times 0.6627 = -26{,}508$ (400 contracts of 100 shares, sign flipped because the calls are short).
> With stock (delta 1) as the hedging instrument, $N_H = -(-26{,}508)/1 = +26{,}508$: buy 26,508 shares.
> B is wrong because it hedges the share count rather than the delta-weighted exposure.
> C is wrong because it forgets to flip the sign for a short position, doubling the exposure to $-53{,}016$.
> 3. **C.** $N_H = -\text{Portfolio delta}/\text{Delta}_H = -(-26{,}508)/(-0.3373) = -78{,}589$.
> A negative $N_H$ means sell the hedging instrument: sell puts on 78,589 shares, about 786 contracts.
> Selling puts adds positive delta of $78{,}589 \times 0.3373 = 26{,}508$, offsetting the short calls.
> A is wrong because it drops the sign of $N_H$; buying puts adds negative delta and doubles the exposure.
> B is wrong because it multiplies by the put delta instead of dividing, $26{,}508 \times 0.3373 = 8{,}941$.
> 4. **B.** With $\Delta S = +4.00$: delta effect $0.6627(4) = 2.6508$ and gamma effect $\frac{0.0468}{2}(4^2) = 0.3744$.
> Estimated price $= 4.52 + 2.6508 + 0.3744 = 7.5452$, about 7.55; Python's full BSM reprice at 56.00 is 7.5046, much closer to 7.55 than the delta-only estimate is.
> A is wrong because it uses delta alone, $4.52 + 2.6508 = 7.1708$, which ignores the convexity that matters for a large earnings move.
> C is wrong because it omits the one-half in the gamma term, $4.52 + 2.6508 + 0.0468(16) = 7.9196$.
> 5. **B.** A short call book is short gamma, and stock has zero gamma, so the delta-neutral book loses on a large move in either direction: its delta turns negative as the price rises and positive as it falls, the wrong way both times.
> The approximate loss for a USD 4 jump is $\frac{1}{2}(-40{,}000 \times 0.0468)(4^2) = -14{,}976$; Python full revaluation gives $-13{,}389$ for a jump up and $-16{,}194$ for a jump down.
> Only option trades change portfolio gamma, so the desk must buy calls or puts to reduce gamma, then re-hedge delta with stock.
> A is wrong because it treats the hedged book as linear, which is Osei's first statement; delta neutrality holds only for very small moves.
> C is wrong because it is Osei's second statement: extra shares change delta but add no gamma, so they cannot remove the jump exposure.
> 6. **C.** The market call price of 4.85 is above the 4.52 model value at 30% volatility, and option value rises monotonically with volatility, so the implied volatility must be above 30% (Python solves it at 33.46%).
> The desk forecasts 28%, below the implied volatility, so the calls are rich relative to its view; it should sell volatility by adding to the short call position (short vega), accepting that the extra gamma must be managed.
> A is wrong because it reverses the price-to-volatility mapping.
> B is wrong because it identifies the implied volatility correctly but then buys volatility priced above the desk's own forecast.

## Distractor design

1. B: correct negative put rho flagged as an error (sign); C: correct put theta flagged because it differs from call theta (Greek property misread).
2. B: hedge sized on contracts times 100 instead of delta (wrong formula variant); C: short-position sign not flipped (sign).
3. A: sign of $N_H$ ignored (sign); B: multiplied by the hedge instrument's delta instead of dividing (wrong formula variant).
4. A: delta-only estimate for a large move (missing second-order term); C: gamma term without the one-half (wrong formula variant).
5. A: delta-neutral book treated as immune to jumps (gamma ignored); C: stock treated as a source of gamma (instrument property misread).
6. A: implied volatility direction reversed (price-volatility mapping); B: direction correct but trade fights the desk's forecast (decision error).
