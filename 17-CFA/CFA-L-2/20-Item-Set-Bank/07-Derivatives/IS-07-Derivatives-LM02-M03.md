---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 2
title: "Halcyon Pension Trust: Put Arbitrage and a Dividend-Paying Utility"
los: [los-07-02-a, los-07-02-b, los-07-02-c, los-07-02-d]
difficulty: 3
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Halcyon Pension Trust: Put Arbitrage and a Dividend-Paying Utility

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Nadia Thibault, CFA, is a derivatives analyst at Halcyon Pension Trust, a Toronto defined benefit plan that reports in Canadian dollars.
Halcyon's investment committee has asked for option values on two equity holdings before it approves an option overlay program.
Thibault reports to Graham Whitlock, the plan's chief investment officer.
She uses recombining binomial trees in which each period is one year and the risk-free rate is 2.00% per period, periodically compounded.

The first holding is Pinecrest Rail, which pays no dividends.
Thibault values a one-period European put on Pinecrest with an exercise price of 46.00.
A dealer quotes that put at 3.80 bid and 3.95 offered.

The second holding is Laurentian Power, a regulated utility that will pay a cash dividend of 2.00 per share at Time 1.
The shares go ex-dividend immediately after the Time 1 prices are observed, so an investor who holds a share at a Time 1 node receives the dividend.
Thibault applies the escrow method: she builds the tree on the share price less the present value of the dividend, and she adds the dividend back when testing for early exercise at Time 1.
She values a two-period American-style call and a two-period European put on Laurentian, each with an exercise price of 56.00.

**Exhibit 1: Binomial inputs**

| Item | Pinecrest Rail | Laurentian Power |
|---|---|---|
| Current share price | 45.00 | 60.00 |
| Up factor, u | 1.20 | 1.20 |
| Down factor, d | 0.80 | 0.85 |
| Number of periods | 1 | 2 |
| Cash dividend | none | 2.00 at Time 1 |
| Halcyon research estimate of the probability of an up move | 0.58 | 0.62 |
| Halcyon required return on the shares | 7.50% | 6.00% |

On 8 May, Whitlock reviews Thibault's draft.
"Our research team spent months on those up-move probabilities, and the committee expects them to drive the option values."
"I also question the American call: nobody exercises a call early, so it should be worth exactly the same as the European call."

Thibault replies on 9 May.
"The option values do not depend on our research probabilities or on our required returns, and the dividend changes the answer on early exercise for Laurentian."

Whitlock also asks Thibault to explain, in terms of trades in Pinecrest shares and the money market, how the put could be manufactured if the dealer's quote proved unattractive.
If the quote is attractive instead, he wants the trades that would lock in the difference without any net investment or price risk.

## Questions

1. For the one-period Pinecrest tree, the risk-neutral probability of an up move and the hedge ratio for the put are closest to: (LOS: los-07-02-a)
   - A. 0.5500 and -0.5556.
   - B. 0.5000 and -0.5556.
   - C. 0.5500 and -1.8000.
2. To exploit the dealer's quote on the Pinecrest put, Halcyon should undertake which set of trades, and what is the Time 0 inflow per put? (LOS: los-07-02-c)
   - A. Buy the put, buy 0.5556 shares, and borrow 29.41; 0.46.
   - B. Sell the put, short sell 0.5556 shares, and lend 29.41; 0.46.
   - C. Buy the put, buy 0.5556 shares, and borrow 30.00; 1.05.
3. The value of the two-period American-style call on Laurentian Power is closest to: (LOS: los-07-02-d)
   - A. 7.79.
   - B. 8.22.
   - C. 9.39.
4. Using the expectations approach, the value of the two-period European put on Laurentian Power is closest to: (LOS: los-07-02-b)
   - A. 1.95.
   - B. 3.22.
   - C. 3.58.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** $\pi = (1 + r - d)/(u - d) = (1.02 - 0.80)/(1.20 - 0.80) = 0.22/0.40 = 0.5500$.
> Prices are $S^+ = 45(1.20) = 54.00$ and $S^- = 45(0.80) = 36.00$, so $p^+ = \operatorname{Max}(0, 46 - 54) = 0$ and $p^- = 46 - 36 = 10.00$.
> The put hedge ratio is $h = (p^+ - p^-)/(S^+ - S^-) = (0 - 10)/(54 - 36) = -0.5556$: a long put is replicated by short selling 0.5556 shares and lending.
> B is wrong because it computes the probability from prices alone, $(S - S^-)/(S^+ - S^-) = 9/18 = 0.5000$, leaving out the risk-free growth factor $1 + r$.
> C is wrong because it inverts the hedge ratio, $(S^+ - S^-)/(p^+ - p^-) = 18/(-10) = -1.8000$; a hedge ratio for one put cannot be below $-1$.
> 2. **A.** The put value is $p = hS + PV(-hS^- + p^-) = -0.5556(45) + [0.5556(36) + 10]/1.02 = -25.0000 + 29.4118 = 4.4118$.
> The expectations approach agrees: $p = [0.55(0) + 0.45(10)]/1.02 = 4.4118$.
> The dealer's offer of 3.95 is below 4.4118, so the put is cheap: buy it at the offer and sell the replicating portfolio, which means buying 0.5556 shares and borrowing $30.0000/1.02 = 29.4118$.
> Time 0 cash flow: $-3.95 - 25.0000 + 29.4118 = +0.4618$ per put.
> At Time 1 the position nets zero in both states: up, $0.5556(54) - 29.4118(1.02) + 0 = 30.00 - 30.00 = 0$; down, $0.5556(36) + 10 - 30.00 = 0$.
> B is wrong because it is the trade set for an overpriced put; selling at the 3.80 bid and buying the replicating portfolio costs $3.80 - 4.4118 = -0.6118$, a loss.
> C is wrong because it borrows the Time 1 repayment of 30.00 instead of its present value; the loan then requires $30.00(1.02) = 30.60$ at Time 1, leaving a shortfall of 0.60 in both states, and the present value of that shortfall, $0.60/1.02 = 0.5882$, reduces the apparent 1.05 inflow back to the true arbitrage profit of 0.4618.
> 3. **B.** Escrow: $\hat{S} = 60 - 2/1.02 = 60 - 1.9608 = 58.0392$; $\pi = (1.02 - 0.85)/(1.20 - 0.85) = 0.4857$.
> Tree on $\hat{S}$: $\hat{S}^+ = 69.6471$, $\hat{S}^- = 49.3333$, $\hat{S}^{++} = 83.5765$, $\hat{S}^{+-} = 59.2000$, $\hat{S}^{--} = 41.9333$.
> Payoffs: $c^{++} = 27.5765$, $c^{+-} = 3.2000$, $c^{--} = 0$.
> Time 1 up: model value $[0.4857(27.5765) + 0.5143(3.2000)]/1.02 = 14.7451$, but the cum-dividend exercise value is $69.6471 + 2.00 - 56 = 15.6471$, so the call is exercised to capture the dividend and the node takes 15.6471.
> Time 1 down: model value $0.4857(3.2000)/1.02 = 1.5238$, above the exercise value of zero ($49.3333 + 2 - 56 < 0$).
> Time 0: $C = [0.4857(15.6471) + 0.5143(1.5238)]/1.02 = 8.2193$, above the immediate exercise value $60 - 56 = 4.00$, so the answer is 8.22 and the early exercise premium is $8.2193 - 7.7898 = 0.4295$; Whitlock's claim fails because the dividend creates a reason to exercise early.
> A is wrong because it is the European value, $[0.4857(14.7451) + 0.5143(1.5238)]/1.02 = 7.7898$, which omits the exercise test at the Time 1 up node.
> C is wrong because it ignores the dividend entirely and builds the tree on 60.00 ($S^{++} = 86.40$, $S^{+-} = 61.20$), giving $[0.4857(17.0980) + 0.5143(2.4762)]/1.02 = 9.3904$; the share price will drop by the dividend, which the call holder does not receive unless the call is exercised.
> 4. **C.** The expectations approach weights terminal payoffs by risk-neutral probabilities and discounts at the risk-free rate.
> Put payoffs on the escrowed tree: $p^{++} = p^{+-} = 0$ (83.5765 and 59.2000 are above 56) and $p^{--} = 56 - 41.9333 = 14.0667$.
> $p = (1 - \pi)^2 p^{--}/1.02^2 = 0.264490(14.0667)/1.0404 = 3.5760$.
> A is wrong because it weights the payoff with the research probability, $(1 - 0.62)^2(14.0667)/1.0404 = 0.1444(14.0667)/1.0404 = 1.9524$; the risk-neutral probability is objective and does not depend on anyone's view, and the required returns are equally irrelevant.
> B is wrong because it ignores the dividend and builds the tree on 60.00, so $S^{--} = 43.35$, $p^{--} = 12.65$, and $p = 0.264490(12.65)/1.0404 = 3.2159$; the ex-dividend drop in the share price raises the put's value.

## Distractor design

1. B: risk-neutral probability computed from prices without the interest factor (wrong formula variant); C: inverted hedge ratio (formula variant).
2. B: trade set for an overpriced put (direction error); C: financing leg borrowed at its undiscounted Time 1 amount (period error).
3. A: European value with no exercise test at the dividend node (American vs European); C: dividend ignored and tree built on the cum-dividend price (misread exhibit).
4. A: research probability used instead of the risk-neutral probability (wrong probability); B: dividend ignored in the escrowed tree (misread exhibit).
