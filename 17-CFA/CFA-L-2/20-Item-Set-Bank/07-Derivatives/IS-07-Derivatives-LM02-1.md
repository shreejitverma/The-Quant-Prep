---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 2
title: "Kestrel Family Office: Binomial Values for Andes Ridge Mining"
los: [los-07-02-a, los-07-02-b, los-07-02-c, los-07-02-d, los-07-02-e]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Kestrel Family Office: Binomial Values for Andes Ridge Mining

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tomás Vidal, CFA, is a derivatives analyst at Kestrel Family Office, which manages the wealth of a Chilean industrial family.
The family holds a large block of Andes Ridge Mining (ARM), a copper producer that pays no dividends and has announced no plans to start.
Kestrel's chief investment officer, Beatriz Lagos, has asked Vidal to value several options on ARM before deciding whether to overlay the block with derivatives.
Vidal models ARM with a recombining binomial tree in which each period is one year.

Exhibit 1: ARM binomial inputs

| Item | Value |
|---|---|
| Current ARM share price | 80.00 |
| Up factor, u | 1.20 |
| Down factor, d | 0.85 |
| Risk-free rate per period | 3.00% |
| Kestrel research estimate of the probability of an up move | 0.60 |
| Kestrel required return on ARM shares | 9.00% |

Vidal first values a one-period European call on ARM with an exercise price of 80.00.
A dealer is currently offering to buy or sell this call at 8.40.
He then values a one-period European put with the same exercise price, because Lagos wants to understand how such a put could be manufactured from ARM shares and the money market.

On 3 March, Lagos questions Vidal's method.

"Our research team puts the chance of an up move at 60%, and ARM's risk justifies a 9% discount rate."
"An option value that ignores those two numbers ignores our house view."

Vidal replies that the option values in his model do not depend on Kestrel's view of ARM's expected return.

Lagos then asks about longer-dated protection for the block.
Vidal values two-period American-style options on ARM, a put and a call, each with an exercise price of 82.00.
He reminds Lagos that American options cannot be valued from terminal payoffs alone.

Kestrel also carries a EUR 5,000,000 credit line on which interest resets annually to the one-year euro rate.
To study a cap on that exposure, Vidal values a two-year European call on the one-year spot rate with an exercise rate of 3.00% and a notional of EUR 5,000,000.
The option pays at Time 2 on the rate observed at Time 2.
He uses the arbitrage-free lattice in Exhibit 2, in which the risk-neutral probability of each move is 0.50.

Exhibit 2: One-year euro rate lattice

| Time | Node | One-year rate |
|---|---|---|
| 0 | Start | 2.50% |
| 1 | Up | 3.60% |
| 1 | Down | 2.40% |
| 2 | Up-up | 4.90% |
| 2 | Up-down | 3.30% |
| 2 | Down-down | 2.20% |

The current two-year euro swap rate of 2.95% is shown on Vidal's screen but is not part of the lattice.

## Questions

1. Using the expectations approach, the value of the one-period European call with an exercise price of 80.00 is closest to: (LOS: los-07-02-b)
   - A. 7.55.
   - B. 7.99.
   - C. 9.32.
2. To exploit the dealer's price for the one-period call, Kestrel should write the call and: (LOS: los-07-02-c)
   - A. buy 0.5714 ARM shares and borrow 37.73.
   - B. buy 0.5714 ARM shares and borrow 38.86.
   - C. buy 1.7500 ARM shares and borrow 37.73.
3. The portfolio that replicates a long position in the one-period European put with an exercise price of 80.00 is closest to: (LOS: los-07-02-a)
   - A. short 0.4286 ARM shares and lend 39.94.
   - B. buy 0.4286 ARM shares and borrow 39.94.
   - C. short 0.4286 ARM shares and lend 11.65.
4. The value of the two-period American-style put with an exercise price of 82.00 is closest to: (LOS: los-07-02-d)
   - A. 5.57.
   - B. 6.50.
   - C. 6.70.
5. The value of the two-year interest rate call on Kestrel's EUR 5,000,000 notional is closest to: (LOS: los-07-02-e)
   - A. EUR 22,366.
   - B. EUR 29,470.
   - C. EUR 29,744.
6. The value of the two-period American-style call with an exercise price of 82.00 is closest to: (LOS: los-07-02-d)
   - A. 8.28.
   - B. 8.53.
   - C. 9.53.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Up and down prices are $S^+ = 80(1.20) = 96.00$ and $S^- = 80(0.85) = 68.00$, so $c^+ = \operatorname{Max}(0, 96 - 80) = 16.00$ and $c^- = 0$.
> The risk-neutral probability is $\pi = (1.03 - 0.85)/(1.20 - 0.85) = 0.18/0.35 = 0.5143$.
> The value is $c = [0.5143(16.00) + 0.4857(0)]/1.03 = 8.2286/1.03 = 7.9889$, about 7.99.
> The no-arbitrage route agrees: $h = 16/28 = 0.5714$ and $c = 0.5714(80) - 0.5714(68)/1.03 = 45.7143 - 37.7254 = 7.9889$.
> A is wrong because it keeps the risk-neutral probability but discounts at Kestrel's 9% required return, $0.5143(16)/1.09 = 7.5491$; the expectations approach discounts at the risk-free rate.
> C is wrong because it weights the payoff with the research probability 0.60, $0.60(16)/1.03 = 9.3204$; the probability must be the risk-neutral one, which does not depend on anyone's view, so Lagos's objection fails on both counts.
> 2. **A.** The model value 7.9889 is below the dealer's 8.40, so the call is overpriced; sell it and buy the replicating portfolio.
> The hedge ratio is $h = (c^+ - c^-)/(S^+ - S^-) = (16 - 0)/(96 - 68) = 0.5714$ shares, costing $0.5714(80) = 45.7143$.
> Borrow the present value of the down-state share value, $0.5714(68)/1.03 = 38.8571/1.03 = 37.7254$.
> The Time 0 net inflow is $8.40 - 45.7143 + 37.7254 = 0.4111$ per call.
> At Time 1 the position nets zero in both states: up, $0.5714(96) - 38.8571 - 16 = 54.8571 - 38.8571 - 16 = 0$; down, $0.5714(68) - 38.8571 - 0 = 0$.
> B is wrong because it borrows the full Time 1 repayment 38.86 instead of its present value, which leaves a loan balance of $38.8571(1.03) = 40.0229$ that the shares cannot repay in the down state.
> C is wrong because it inverts the hedge ratio, $(S^+ - S^-)/(c^+ - c^-) = 28/16 = 1.75$; a hedge ratio for one call cannot exceed 1.
> 3. **A.** Put payoffs are $p^+ = \operatorname{Max}(0, 80 - 96) = 0$ and $p^- = \operatorname{Max}(0, 80 - 68) = 12.00$.
> The hedge ratio is $h = (0 - 12)/(96 - 68) = -0.4286$, so the replication short sells 0.4286 shares for $0.4286(80) = 34.2857$.
> The financing term is $PV(-hS^- + p^-) = [0.4286(68) + 12]/1.03 = (29.1429 + 12)/1.03 = 39.9445$, a positive amount, which is lending.
> The put value is $p = -34.2857 + 39.9445 = 5.6588$, and parity confirms it: $c - S + PV(X) = 7.9889 - 80 + 77.6699 = 5.6588$.
> B is wrong because it reverses both legs, which replicates a short put (the put writer buys shares on margin).
> C is wrong because it lends only $PV(p^-) = 12/1.03 = 11.6505$, dropping the $-hS^-$ term, so the portfolio would pay 12 minus the cost of covering the short sale in the down state rather than 12.
> 4. **C.** Terminal prices are $S^{++} = 115.20$, $S^{+-} = 81.60$, $S^{--} = 57.80$, so $p^{++} = 0$, $p^{+-} = 82 - 81.60 = 0.40$, $p^{--} = 82 - 57.80 = 24.20$.
> Time 1 up: $p^+ = [0.5143(0) + 0.4857(0.40)]/1.03 = 0.1886$; exercise value $82 - 96 < 0$, so hold.
> Time 1 down: model value $p^- = [0.5143(0.40) + 0.4857(24.20)]/1.03 = 11.6117$, but exercise value is $82 - 68 = 14.00$, so exercise and use 14.00.
> Time 0: $P = [0.5143(0.1886) + 0.4857(14.00)]/1.03 = 6.6961$, above the immediate exercise value $82 - 80 = 2.00$, so the answer is 6.70.
> A is wrong because it is the European value, $[0.5143(0.1886) + 0.4857(11.6117)]/1.03 = 5.5699$, which ignores the early exercise at the down node (early exercise premium 1.1263).
> B is wrong because it replaces the down node correctly but then discounts the Time 0 value one period too many, $6.6961/1.03 = 6.5011$.
> 5. **B.** Payoffs per EUR 1 at Time 2: $c^{++} = 0.049 - 0.030 = 0.0190$, $c^{+-} = 0.033 - 0.030 = 0.0030$, $c^{--} = 0$.
> Time 1 up, discounted at that node's own rate: $c^+ = 0.5(0.0190 + 0.0030)/1.036 = 0.0106178$.
> Time 1 down: $c^- = 0.5(0.0030 + 0)/1.024 = 0.0014648$.
> Time 0: $c = 0.5(0.0106178 + 0.0014648)/1.025 = 0.0058940$, or $0.0058940 \times 5{,}000{,}000 = $ EUR 29,470.
> A is wrong because it treats the barely in-the-money up-down payoff (3.30% against 3.00%) as zero, giving $0.5[0.5(0.0190)/1.036]/1.025 = 0.0044731$, EUR 22,366.
> C is wrong because it discounts the expected terminal payoff $0.25(0.0190) + 0.5(0.0030) = 0.00625$ for two periods at the Time 0 rate, $0.00625/1.025^2 = 0.0059488$, EUR 29,744, instead of node by node at each node's own rate.
> 6. **A.** Call payoffs: $c^{++} = 115.20 - 82 = 33.20$, $c^{+-} = \operatorname{Max}(0, 81.60 - 82) = 0$, $c^{--} = 0$.
> Time 1 up: $c^+ = 0.5143(33.20)/1.03 = 16.5770$, above the exercise value $96 - 82 = 14.00$, so no early exercise; $c^- = 0$.
> Time 0: $c = 0.5143(16.5770)/1.03 = 8.2770$, about 8.28, identical to the European value $\pi^2(33.20)/1.03^2 = 8.2770$ because ARM pays no dividends.
> B is wrong because it discounts the two-period expected payoff for only one period, $0.5143^2(33.20)/1.03 = 8.5253$.
> C is wrong because it reads the one-period exercise price of 80.00 from the vignette, giving $c^{++} = 35.20$ and $c^{+-} = 1.60$ and a value of $[0.2645(35.20) + 2(0.5143)(0.4857)(1.60)]/1.03^2 = 9.5291$.

## Distractor design

1. A: risk-neutral probability with a risk-adjusted discount rate (wrong discount rate); C: real-world probability with the risk-free rate (wrong probability).
2. B: undiscounted financing leg (period error); C: inverted hedge ratio (formula variant).
3. B: trade directions reversed, short put replicated instead of long put (sign); C: financing term missing the $-hS^-$ leg (wrong formula variant).
4. A: European value with no exercise test (American vs European); B: correct node replacement discounted one period too many (period error).
5. A: in-the-money middle payoff dropped (misread exhibit); C: flat Time 0 discounting instead of node-specific rates (wrong formula variant).
6. B: one-period discount on a two-period payoff (period error); C: strike of the one-period option applied (misread exhibit).
