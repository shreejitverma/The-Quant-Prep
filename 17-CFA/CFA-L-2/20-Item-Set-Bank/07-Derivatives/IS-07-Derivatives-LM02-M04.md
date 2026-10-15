---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 2
title: "Marlow Building Society: Protecting Mortgage Margin From Falling Rates"
los: [los-07-02-e, los-07-02-j, los-07-02-n]
difficulty: 3
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Marlow Building Society: Protecting Mortgage Margin From Falling Rates

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Owen Pritchard, CFA, is an interest rate risk analyst at Marlow Building Society, a UK mutual lender that reports in pounds sterling (GBP).
Most of Marlow's assets are floating-rate mortgages, while much of its funding comes from fixed-rate retail savings bonds.
The treasurer, Harriet Cole, is concerned that a fall in market rates will compress Marlow's net interest margin.
She asks Pritchard to value three option-based hedges before the asset-liability committee meets.

The first hedge is a two-year European put on the one-year reference rate with an exercise rate of 4.20% and a notional of GBP 25,000,000.
The option pays at Time 2 based on the one-year rate observed at Time 2.
Pritchard values it on the arbitrage-free lattice in Exhibit 1, in which the risk-neutral probability of each move is 0.50 and rates are annually compounded.

**Exhibit 1: One-year reference rate lattice**

| Time | Node | One-year rate |
|---|---|---|
| 0 | Start | 3.80% |
| 1 | Up | 4.70% |
| 1 | Down | 3.30% |
| 2 | Up-up | 5.60% |
| 2 | Up-down | 4.10% |
| 2 | Down-down | 3.00% |

The two-year gilt yield of 3.72% is also shown on Pritchard's screen but is not part of the lattice.

The second hedge addresses a GBP 60,000,000 block of mortgages that reprices in nine months to the three-month reference rate for the following three months.
Pritchard considers a single European interest rate option that expires in nine months, has an exercise rate of 3.75%, and whose payoff is determined at expiry and paid three months later.

**Exhibit 2: Standard market model inputs for the nine-month option**

| Item | Value |
|---|---|
| Current three-month reference rate | 4.25% |
| FRA rate, 9 x 12 months | 3.90% |
| Exercise rate | 3.75% |
| Accrual period | 90/360 |
| Volatility of the FRA rate | 20% |
| $N(d_1)$ | 0.6229 |
| $N(d_2)$ | 0.5556 |
| Continuously compounded risk-free rate, all maturities to five years | 4.00% |

On 2 June, Cole comments on Pritchard's draft.
"The payoff on this option is fixed in nine months, so the discounting should stop at nine months."
Pritchard replies that the discounting horizon must reflect when the payoff is actually paid.

The third hedge concerns a pipeline of new floating-rate mortgages that Marlow intends to convert into fixed-rate income in six months by entering a four-year annual-pay swap in which it receives fixed.
A dealer quotes a six-month European payer swaption on that swap, with an exercise rate of 3.60% on GBP 40,000,000 of notional, at GBP 397,000.
The six-month forward four-year swap rate is 3.70%, and the current four-year swap rate is 3.95%.
The present value annuity factor for the forward swap's four annual settlement dates is 3.5512.
Pritchard wants the value of the matching receiver swaption, with the same exercise rate, expiry, and notional, that is consistent with the dealer's payer quote.

Finally, the same dealer offers to sell Marlow, for GBP 34,500, the nine-month option that hedges the mortgage block repricing, priced off the Exhibit 2 inputs.
Cole's own forecast of the FRA-rate volatility over the next nine months is 17%.

## Questions

1. The value of the two-year European put on the one-year reference rate is closest to: (LOS: los-07-02-e)
   - A. GBP 69,946.
   - B. GBP 81,211.
   - C. GBP 81,526.
2. The nine-month option Marlow should buy for the mortgage block, and its value based on Exhibit 2, are closest to: (LOS: los-07-02-j)
   - A. a floorlet worth GBP 28,220.
   - B. a floorlet worth GBP 28,503.
   - C. a caplet worth GBP 49,838.
3. The value of the receiver swaption that is consistent with the dealer's payer swaption quote is closest to: (LOS: los-07-02-j)
   - A. GBP 237,000.
   - B. GBP 254,952.
   - C. GBP 539,048.
4. Based on the dealer's offer for the nine-month option, the most accurate statement is that the option's implied volatility is: (LOS: los-07-02-n)
   - A. below 20%, so the option is cheap relative to Cole's forecast.
   - B. above 20%, so the option is expensive relative to Cole's forecast.
   - C. above 20%, which establishes that realized FRA-rate volatility will exceed 20% over the option's life.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** A put on the rate pays $\operatorname{Max}(0, R_X - R)$, so the Time 2 payoffs per GBP 1 are $p^{++} = \operatorname{Max}(0, 0.0420 - 0.0560) = 0$, $p^{+-} = 0.0420 - 0.0410 = 0.0010$, and $p^{--} = 0.0420 - 0.0300 = 0.0120$.
> Time 1 up, discounted at that node's own rate: $p^+ = 0.5(0 + 0.0010)/1.047 = 0.0004776$.
> Time 1 down: $p^- = 0.5(0.0010 + 0.0120)/1.033 = 0.0062924$.
> Time 0: $p = 0.5(0.0004776 + 0.0062924)/1.038 = 0.0032610$, or $0.0032610 \times 25{,}000{,}000 = $ GBP 81,526.
> A is wrong because it treats the up-down payoff as zero, as if 4.10% were above the 4.20% exercise rate; $p^- = 0.5(0.0120)/1.033 = 0.0058083$ and $p = 0.5(0.0058083)/1.038 = 0.0027978$, GBP 69,946.
> B is wrong because it discounts the expected terminal payoff $0.25(0) + 0.5(0.0010) + 0.25(0.0120) = 0.0035$ for two periods at the Time 0 rate, $0.0035/1.038^2 = 0.0032484$, GBP 81,211, instead of node by node at each node's own rate.
> 2. **A.** A lender whose mortgage income falls when rates fall needs an interest rate put, a floorlet, whose underlying is the 9 x 12 FRA rate of 3.90%.
> $N(-d_1) = 1 - 0.6229 = 0.3771$ and $N(-d_2) = 1 - 0.5556 = 0.4444$.
> Bracket: $R_X N(-d_2) - FRA \cdot N(-d_1) = 0.0375(0.4444) - 0.0390(0.3771) = 0.0166650 - 0.0147069 = 0.0019581$.
> Because the payoff is set at expiry and paid three months later, discounting runs to $t_{j-1} + t_m = 0.75 + 0.25 = 1.00$ year: $e^{-0.04 \times 1.00} = 0.960789$.
> Value: $60{,}000{,}000 \times 0.25 \times 0.960789 \times 0.0019581 = $ GBP 28,220, so Pritchard's reply to Cole is correct.
> B is wrong because it follows Cole's comment and discounts only to expiry, $e^{-0.04 \times 0.75} = 0.970446$, giving $15{,}000{,}000 \times 0.970446 \times 0.0019581 = $ GBP 28,503.
> C is wrong because a caplet pays when rates rise, the opposite of Marlow's exposure; its value is $15{,}000{,}000 \times 0.960789 \times [0.0390(0.6229) - 0.0375(0.5556)] = 15{,}000{,}000 \times 0.960789 \times 0.0034581 = $ GBP 49,838.
> Parity confirms both values: caplet minus floorlet $= 15{,}000{,}000 \times 0.960789 \times (0.0390 - 0.0375) = 21{,}618 = 49{,}838 - 28{,}220$.
> 3. **B.** A long receiver swaption plus a short payer swaption at the same exercise rate is a forward swap receiving the fixed rate $R_X$, so $PAYSWN - RECSWN = (AP)(PVA)(R_{FIX} - R_X) \times \text{Notional}$.
> With annual payments $AP = 1$: $40{,}000{,}000 \times 3.5512 \times (0.0370 - 0.0360) = 142{,}048$.
> $RECSWN = 397{,}000 - 142{,}048 = $ GBP 254,952; the receiver is cheaper because its 3.60% strike is below the 3.70% forward swap rate, so it is out of the money.
> As a cross-check, a Black-model value of about GBP 397,432 for the payer corresponds to roughly 22% forward swap rate volatility, and the receiver at that volatility is GBP 255,384; the small gap comes only from the dealer's rounded quote.
> A is wrong because it replaces the annuity factor with the undiscounted count of four annual payments, $397{,}000 - 40{,}000{,}000 \times 4 \times 0.0010 = 237{,}000$.
> C is wrong because it adds the forward swap value instead of subtracting it, $397{,}000 + 142{,}048 = 539{,}048$.
> The current four-year swap rate of 3.95% is a decoy; the swaption's underlying is the forward swap rate, and using 3.95% would produce a negative receiver value, which is impossible.
> 4. **B.** At 20% volatility the model value is GBP 28,220 (Question 2), below the dealer's GBP 34,500 offer, and option value rises monotonically with volatility, so the implied volatility must exceed 20%.
> Cole forecasts 17%, below both the model input and the implied level, so the option is priced rich relative to her view; implied volatility lets Marlow compare the quote directly with its own volatility forecast.
> A is wrong because it reverses the mapping between price and implied volatility.
> C is wrong because implied volatility is the market's forward-looking assessment extracted from the price, not a guarantee of the volatility that will actually be realized.

## Distractor design

1. A: in-the-money up-down payoff dropped (misread exhibit); B: flat Time 0 discounting instead of node-specific rates (wrong formula variant).
2. B: discounting stops at option expiry instead of the settlement date (period error); C: caplet chosen for a falling-rate exposure (direction error).
3. A: annuity factor replaced by the undiscounted number of payments (present value omitted); C: sign of the forward swap term reversed in swaption parity (sign).
4. A: implied volatility direction reversed (price-volatility mapping); C: implied volatility treated as a certain forecast of realized volatility (concept confusion).
