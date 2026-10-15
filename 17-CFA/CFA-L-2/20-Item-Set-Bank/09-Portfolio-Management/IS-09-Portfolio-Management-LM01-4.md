---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 1
title: "Aldgate Macro Partners: Pricing Assets with a Two-State Model"
los: [los-09-01-a, los-09-01-b, los-09-01-c, los-09-01-h]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Aldgate Macro Partners: Pricing Assets with a Two-State Model

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Priya Raman is the chief strategist at Aldgate Macro Partners, a global macro hedge fund that publishes a quarterly research note for its investors.
For the next note she wants to show how default-free bonds, equities, and a defensive asset are priced off the same model of investor preferences.
She asks her junior analyst, Tomas Eklund, to build a one-period, two-state model for the real economy.

In Eklund's model, the marginal investor's inter-temporal rate of substitution between consumption one year from now and consumption today takes one value in a bad state and another in a good state.
All payoffs are in real terms, so inflation plays no role.
Exhibit 1 shows the model's inputs.

Exhibit 1: Two-state model inputs (values one year from now, per unit)

| Item | Bad state | Good state |
|---|---|---|
| Probability | 0.45 | 0.55 |
| Inter-temporal rate of substitution | 0.9860 | 0.9530 |
| Price of a two-year default-free real zero-coupon bond (one year remaining) | 0.9010 | 0.9420 |
| Value of an equity index claim | 0.80 | 1.18 |
| Value of Asset H | 1.08 | 0.97 |
| Real GDP growth in the state | -1.2% | 3.1% |

Asset H is a defensive strategy that tends to pay off when the economy contracts.
Eklund plans to price every asset in two ways: first, by discounting its expected value one year from now at the one-year real default-free rate, and second, by taking the expectation of its state values multiplied by the inter-temporal rate of substitution.
He notes that the second method should give the market price, while the first gives a risk-neutral value.

When they review the model, Raman and Eklund discuss the recent market reaction to a GDP release.
Exhibit 2 summarizes the release.

Exhibit 2: Quarterly real GDP release (annualized)

| Item | Value |
|---|---|
| Aldgate's own forecast | 2.9% |
| Consensus forecast before the release | 3.4% |
| Actual reported growth | 3.2% |
| Equity index change on the day of release | -1.8% |

Eklund: "The number beat our own 2.9% forecast, yet the index fell 1.8%, so the market reaction shows that our pricing model does not describe how investors behave."

Raman: "I would not draw that conclusion from one day's move."

Raman then turns to the outlook section of the note.
She expects real GDP growth to run above its trend rate over the next two years, with no change in the volatility of growth, inflation expectations, or risk appetite.
She wants the note to state clearly what that forecast implies for the aggregate value of the domestic equity market.

Eklund proposes one sentence for the note: "Above-trend growth raises expected earnings, so equity values must rise."
Raman asks him to check that sentence against the fundamental pricing equation before the note is sent to investors.

## Questions

1. The one-year real default-free interest rate implied by Eklund's model is closest to: (LOS: los-09-01-c)
   - A. 3.15%.
   - B. 3.22%.
   - C. 3.32%.
2. The market price today of the two-year default-free real zero-coupon bond is closest to: (LOS: los-09-01-a)
   - A. 0.8651.
   - B. 0.8935.
   - C. 0.8939.
3. The expected one-year return on the equity index claim is closest to: (LOS: los-09-01-h)
   - A. 2.99%.
   - B. 3.32%.
   - C. 3.65%.
4. Relative to its risk-neutral value, the market price of Asset H is most likely: (LOS: los-09-01-h)
   - A. higher, so its expected return is about 3.23%.
   - B. lower, so its expected return is about 3.42%.
   - C. equal, so its expected return is about 3.32%.
5. The most likely explanation of the market reaction described in Exhibit 2 is that: (LOS: los-09-01-b)
   - A. reported growth fell 0.2 percentage points short of the consensus that was already reflected in prices.
   - B. reported growth exceeded Aldgate's forecast by 0.3 percentage points, so the fall shows the pricing model has failed.
   - C. higher reported growth raised real interest rates, and a higher discount rate always outweighs higher expected cash flows.
6. With regard to Eklund's proposed sentence, the effect of Raman's growth forecast on aggregate equity values is best described as: (LOS: los-09-01-a)
   - A. positive, because only the expected cash flows in the numerator change.
   - B. negative, because higher growth raises the real default-free rate in the denominator.
   - C. ambiguous, because higher growth raises both expected cash flows and the real default-free rate.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** $E_t(\tilde m_{t,1}) = 0.45 \times 0.9860 + 0.55 \times 0.9530 = 0.4437 + 0.52415 = 0.967850$, which is the price of a one-year real default-free bond.
> $l_{t,1} = 1/E_t(\tilde m_{t,1}) - 1 = 1/0.967850 - 1 = 3.3218\%$, about 3.32%.
> A is wrong because it averages the two state values without probability weights: $1/0.96950 - 1 = 3.15\%$.
> B is wrong because it computes $1 - E_t(\tilde m) = 3.2150\%$, a discount rather than a return, forgetting to divide by the price.
> 2. **B.** By Equation 5 the price is $E_t(\tilde P_{t+1,1}\,\tilde m_{t,1}) = 0.45 \times 0.9010 \times 0.9860 + 0.55 \times 0.9420 \times 0.9530 = 0.399774 + 0.493749 = 0.893523$.
> The risk-neutral value is $E_t(\tilde P_{t+1,1})/(1 + l_{t,1}) = (0.45 \times 0.9010 + 0.55 \times 0.9420)/1.033218 = 0.923550/1.033218 = 0.893858$.
> The difference, $0.893523 - 0.893858 = -0.000335$, is the covariance term: the bond's price is low in the bad state, when the rate of substitution is high, so it hedges poorly and trades at a discount.
> Its expected holding-period return is $0.923550/0.893523 - 1 = 3.3605\%$, a term premium of $3.3605\% - 3.3218\% = 0.0387\%$ over the one-year real rate.
> A is wrong because it discounts the one-year-ahead price for two periods: $0.923550/1.033218^2 = 0.8651$.
> C is wrong because it is the risk-neutral value, which ignores the covariance with the rate of substitution.
> 3. **C.** The expected value is $0.45 \times 0.80 + 0.55 \times 1.18 = 1.009000$, and the price is $0.45 \times 0.80 \times 0.9860 + 0.55 \times 1.18 \times 0.9530 = 0.354960 + 0.618497 = 0.973457$.
> The expected return is $1.009000/0.973457 - 1 = 3.6512\%$, about 3.65%, a risk premium of $3.6512\% - 3.3218\% = 0.3294\%$.
> The claim pays off in the good state, when marginal utility is low, so its covariance with $\tilde m$ is negative ($-0.003104$) and investors demand a positive premium.
> A is wrong because it flips the sign of the premium: $3.3218\% - 0.3294\% = 2.99\%$.
> B is wrong because it prices the claim at its risk-neutral value, so its expected return collapses to the real rate of 3.32%.
> 4. **A.** The expected value is $0.45 \times 1.08 + 0.55 \times 0.97 = 1.019500$, and the price is $0.45 \times 1.08 \times 0.9860 + 0.55 \times 0.97 \times 0.9530 = 0.479196 + 0.508425 = 0.987621$.
> The risk-neutral value is $1.019500/1.033218 = 0.986723$, so the market price is higher by $0.000898$, the positive covariance term.
> The expected return is $1.019500/0.987621 - 1 = 3.2278\%$, about 3.23%, below the 3.32% real rate: a negative premium of $-0.0940\%$ for an asset that pays off in bad times.
> B is wrong because it flips the sign of the covariance and premium: $3.3218\% + 0.0940\% = 3.42\%$.
> C is wrong because it ignores the covariance entirely and prices Asset H as if investors were risk neutral.
> 5. **A.** Prices already reflect anticipated information, so only the surprise relative to the market's expectation moves them.
> The market expected 3.4%, and the actual $3.2\% - 3.4\% = -0.2$ percentage point surprise was bad news relative to prices, even though growth was strong.
> B is wrong because Aldgate's own 2.9% forecast was not the expectation embedded in prices; measuring the surprise against it is misreading the exhibit.
> C is wrong because the net effect of higher growth on equity values is ambiguous, not always negative, and the release was in any case below expectations.
> 6. **C.** In the fundamental pricing equation, above-trend growth raises the expected cash flows in the numerator, but it also raises the real default-free rate $l_{t,s}$ in the denominator, since higher expected growth reduces the desire to save.
> With inflation expectations and risk premiums unchanged, the stated information cannot tell which effect dominates, so the effect on equity values is ambiguous, and Eklund's sentence overstates the case.
> A is wrong because it ignores the discount-rate channel, which is Eklund's error.
> B is wrong because it ignores the cash-flow channel.

## Distractor design

1. A: unweighted average of the state values (probabilities ignored); B: $1 - E(\tilde m)$ reported as a return (discount vs return).
2. A: one-year-ahead price discounted for two periods (period); C: risk-neutral value reported as price (covariance term omitted).
3. A: sign of the risk premium flipped (sign); B: risk-neutral pricing, so return equals the real rate (covariance term omitted).
4. B: sign of the covariance for a bad-times payoff flipped (sign); C: covariance ignored (risk neutrality assumed).
5. B: surprise measured against the firm's forecast rather than the consensus priced in (misread exhibit); C: discount-rate channel assumed always to dominate (one channel only).
6. A: discount-rate channel ignored (one channel only); B: cash-flow channel ignored (other channel only).
