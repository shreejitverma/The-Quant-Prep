---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 5
title: "Northgate and Riverside: Pricing Two Regional Banks"
los: [los-05-05-d, los-05-05-e, los-05-05-f, los-05-05-g]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Northgate and Riverside: Pricing Two Regional Banks

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Samuel Achterberg is a portfolio manager at Keel Street Capital, a US long-only fund that specializes in financial stocks.
He asks analyst Lucia Ferrante, CFA, to review two regional banks, Northgate Bancorp and Riverside Savings, before the fund's quarterly rebalancing.
Because both banks' balance sheets consist mostly of financial assets carried close to fair value, Ferrante uses single-stage residual income models and price-to-book ratios.
She assumes that each bank's return on equity and growth will remain constant in the long run and that clean surplus accounting holds.

Northgate's published data sheet reports its share price and price-to-book ratio but not its book value per share.
Ferrante estimates Northgate's long-term growth as the sustainable growth rate implied by its payout policy.
For Riverside, she uses management's guidance of 4.0% long-term growth.

Exhibit 1: Selected data for the two banks

| Item | Northgate Bancorp | Riverside Savings |
|---|---|---|
| Share price (USD) | 42.00 | 27.60 |
| Market price-to-book ratio | 1.75 | 0.92 |
| Book value per share (USD) | not reported | 30.00 |
| Trailing EPS (USD) | 3.10 | 2.45 |
| Dividend yield | 4.4% | 3.1% |
| Long-term return on equity | 12.5% | 8.5% |
| Dividend payout ratio | 60% | not used |
| Long-term growth rate | sustainable rate | 4.0% |
| Required return on equity | 10.0% | 9.5% |

Ferrante reports that Northgate's price is above her single-stage estimate.
Achterberg asks her to translate the market price into the assumptions it implies.
First, she solves the single-stage model for the long-term growth rate that equates value with the market price, holding Northgate's return on equity at 12.5%.
Second, she solves for the return on equity that justifies the market price-to-book ratio, holding growth at her own sustainable growth estimate.

For Riverside, Ferrante computes a justified price-to-book ratio and compares it with the market ratio.
She then comments on Riverside's strategy.

Ferrante: "Riverside's management plans to accelerate loan growth so that its long-term growth rate rises from 4% to 6% while return on equity stays at 8.5%.
That plan should narrow the discount to book value at which Riverside trades."

Achterberg, reviewing her work, makes his own comment.

Achterberg: "Your residual income justified price-to-book ratio, one plus the ratio of the return on equity spread to the difference between the required return and growth, will give a different answer for Riverside than the Gordon-growth formula, return on equity minus growth over the required return minus growth, because the residual income version does not depend on the payout ratio."

Ferrante replies that she will reconcile the two expressions before the meeting.

## Questions

1. Ferrante's single-stage residual income estimate of Northgate's intrinsic value per share is closest to: (LOS: los-05-05-f)
   - A. USD 36.00.
   - B. USD 48.00.
   - C. USD 63.00.
2. The long-term growth rate implied by Northgate's market price is closest to: (LOS: los-05-05-g)
   - A. 4.17%.
   - B. 6.67%.
   - C. 8.57%.
3. The return on equity that justifies Northgate's market price-to-book ratio is closest to: (LOS: los-05-05-g)
   - A. 6.25%.
   - B. 13.75%.
   - C. 17.50%.
4. Riverside's justified price-to-book ratio is closest to: (LOS: los-05-05-e)
   - A. 0.82.
   - B. 0.89.
   - C. 0.92.
5. Ferrante's comment about Riverside's growth plan is best described as: (LOS: los-05-05-d)
   - A. correct, because faster growth in book value increases residual income for any bank with positive earnings.
   - B. incorrect, because growth has no effect on value in a single-stage residual income model.
   - C. incorrect, because Riverside's return on equity is below its required return, so faster growth lowers its justified price-to-book ratio.
6. Achterberg's comment is best described as: (LOS: los-05-05-e)
   - A. incorrect, because the two expressions are algebraically identical.
   - B. incorrect, because the residual income version gives a higher ratio whenever return on equity is below the required return.
   - C. correct, because the residual income version is based on book value rather than on dividends.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** $B_0 = P_0/(P/B) = 42.00/1.75 = 24.00$; sustainable growth $g = b \times ROE = (1 - 0.60) \times 0.125 = 0.050$.
> $V_0 = B_0 + (ROE - r)B_0/(r - g) = 24.00 + (0.125 - 0.10) \times 24.00/(0.10 - 0.05) = 24.00 + 0.60/0.05 = 24.00 + 12.00 = 36.00$.
> Price of 42.00 exceeds 36.00, so on Ferrante's assumptions Northgate is overvalued.
> B is wrong because it uses the payout ratio instead of the retention ratio to estimate growth, $g = 0.60 \times 0.125 = 0.075$: $24.00 + 0.60/0.025 = 48.00$.
> C is wrong because it uses price in place of book value: $42.00 + 0.025 \times 42.00/0.05 = 63.00$.
> 2. **B.** Set price equal to value: $42.00 - 24.00 = 0.025 \times 24.00/(0.10 - g)$, so $0.10 - g = 0.60/18.00 = 0.0333$ and $g = 0.0667$.
> The market prices in more growth than the 5.0% sustainable rate, which is why price is above the 36.00 estimate.
> A is wrong because it uses price rather than book value in the numerator: $0.10 - 0.025 \times 42.00/18.00 = 0.10 - 0.0583 = 0.0417$.
> C is wrong because it drops $B_0$ from the left-hand side: $0.10 - 0.60/42.00 = 0.10 - 0.0143 = 0.0857$.
> 3. **B.** $P/B = 1 + (ROE - r)/(r - g)$, so $ROE = r + (P/B - 1)(r - g) = 0.10 + 0.75 \times 0.05 = 0.1375$.
> Check: $(0.1375 - 0.05)/(0.10 - 0.05) = 0.0875/0.05 = 1.75$.
> A is wrong because it subtracts the premium term: $0.10 - 0.75 \times 0.05 = 0.0625$, which would imply a P/B below one.
> C is wrong because it multiplies by $r$ instead of $r - g$: $0.10 + 0.75 \times 0.10 = 0.175$.
> 4. **A.** $P/B = (ROE - g)/(r - g) = (0.085 - 0.04)/(0.095 - 0.04) = 0.045/0.055 = 0.8182$, equivalently $1 + (0.085 - 0.095)/0.055 = 1 - 0.1818 = 0.8182$.
> The justified ratio is below the market ratio of 0.92, so Riverside looks overvalued on Ferrante's assumptions, and a ratio below one is consistent with negative expected residual income ($RI_1 = (0.085 - 0.095) \times 30.00 = -0.30$).
> B is wrong because it computes $ROE/r = 0.085/0.095 = 0.8947$, which is the justified ratio only at zero growth.
> C is wrong because it is the market ratio, $27.60/30.00 = 0.92$, not the justified ratio.
> 5. **C.** The fundamental drivers of residual income are book value and the spread of return on equity over the required return.
> Riverside's spread is negative ($0.085 - 0.095 = -0.01$), so each additional dollar of book value earns less than its cost and growth destroys value.
> At 6% growth the justified ratio falls to $1 - 0.01/(0.095 - 0.06) = 1 - 0.2857 = 0.7143$, from 0.8182 at 4% growth, so the discount to book widens rather than narrows.
> A is wrong because positive earnings are not enough; growth adds value only when return on equity exceeds the required return.
> B is wrong because growth enters the denominator $r - g$; it has no effect only when return on equity equals the required return.
> 6. **A.** Substituting $D_1 = (1 - b) ROE \times B_0$ and $g = b \times ROE$ into the Gordon model gives $P_0/B_0 = (ROE - g)/(r - g)$, and $(ROE - g)/(r - g) = [(r - g) + (ROE - r)]/(r - g) = 1 + (ROE - r)/(r - g)$.
> For Riverside both give 0.8182, so Achterberg is incorrect.
> B is wrong because the two expressions are identical at every value of return on equity.
> C is wrong because the residual income version still depends on payout through $g = b \times ROE$; the basis of the formula does not change the number.

## Distractor design

1. B: payout ratio used for the retention ratio in $g = b \times ROE$; C: price used in place of book value.
2. A: price in the numerator instead of book value; C: $B_0$ dropped from the left-hand side of the implied growth equation.
3. A: sign error on the premium term; C: $r$ used instead of $r - g$ when solving for ROE.
4. B: ROE over $r$ (the zero-growth ratio) used despite positive growth; C: market ratio reported as the justified ratio (misread exhibit).
5. A: positive earnings confused with a positive ROE spread; B: growth treated as irrelevant (true only when ROE equals $r$).
6. B: a spurious difference between two identical formula variants; C: an incorrect reason accepted for a difference that does not exist.
