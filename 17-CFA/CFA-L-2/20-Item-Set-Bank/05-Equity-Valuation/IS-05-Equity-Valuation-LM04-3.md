---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 4
title: "Corvina Outfitters: A Retail Peer Group Decision"
los: [los-05-04-f, los-05-04-h, los-05-04-j, los-05-04-l, los-05-04-m, los-05-04-r]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Corvina Outfitters: A Retail Peer Group Decision

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Leah Brandt, CFA, manages the Juniper Ridge US Consumer Fund, a long-only fund benchmarked against a broad US consumer index.
On 14 April 2026 she asks her analyst, Samuel Achebe, whether the fund should add Corvina Outfitters, Inc., a mid-sized specialty apparel retailer, or one of its four listed peers.
Achebe assembles the data in Exhibit 1.

Exhibit 1: Corvina and peer data (USD)

| Company | Price | Trailing EPS | Forward EPS | Forward P/E | Five-year EPS growth | Beta |
|---|---|---|---|---|---|---|
| Ardenne Apparel | 22.00 | 1.85 | 2.00 | 11.0 | 7.0% | 0.95 |
| Blue Heron Stores | 48.00 | 3.70 | 4.00 | 12.0 | 6.0% | 0.90 |
| Calyx Collective | 60.00 | -0.75 | 1.50 | 40.0 | 32.0% | 1.45 |
| Dunmore Denim | 26.00 | 1.90 | 2.00 | 13.0 | 8.0% | 1.05 |
| Corvina Outfitters | 36.00 | 2.40 | 2.70 | 13.3 | 11.0% | 1.00 |

Calyx, a fast-growing online-first chain, reported a loss last year because of store-closure costs but is expected to be profitable this year.
Corvina pays out 30% of its earnings as dividends; its growth forecast is supported by a new loyalty program and has a consensus range similar to those of the peers.

Brandt explains her benchmark preference: "I want a central tendency for the peers' forward P/Es that reduces the pull of Calyx's 40 times without throwing Calyx out of the sample altogether."
She adds that the fund's policy is to treat the peer benchmark as fairly priced unless there is evidence that the whole retail sector is mispriced.

Achebe also supplies a cross-sectional regression estimated on 48 US specialty retailers at 31 March 2026:

$$
\widehat{P/E}_{\text{trailing}} = 8.40 + 4.10\,\text{DPR} - 1.90\,\beta + 72.0\,\text{EGR}
$$

In the regression, DPR is the dividend payout ratio and EGR is the five-year EPS growth rate, both entered as decimals, and the dependent variable is the trailing P/E.
The regression's $R^2$ is 0.58.
Achebe cautions that the coefficients were estimated at a single date, that they have shifted materially in the three prior annual re-estimations, and that payout and growth are correlated across the sample.

Brandt raises two further points.
First, she notices that Blue Heron trades below Dunmore and Corvina on forward earnings and asks Achebe what most likely explains that discount, given the data in Exhibit 1.
Second, she wants a quick screen that ranks all five companies on trailing earnings, including Calyx, because the fund's compliance system flags any stock whose trailing valuation cannot be ranked.

Achebe prefers to compare growth-adjusted forward multiples before recommending a purchase, using consensus five-year growth in percentage points.

## Questions

1. The peer benchmark that meets Brandt's stated preference is closest to: (LOS: los-05-04-r)
   - A. 12.5.
   - B. 14.5.
   - C. 19.0.
2. Relative to the benchmark in Question 1, Corvina's shares are most likely: (LOS: los-05-04-l)
   - A. undervalued.
   - B. fairly valued.
   - C. overvalued.
3. Based on the forward P/E-to-growth ratio, the most attractively priced of the five companies is: (LOS: los-05-04-j)
   - A. Ardenne.
   - B. Calyx.
   - C. Corvina.
4. Corvina's predicted trailing P/E from Achebe's regression is closest to: (LOS: los-05-04-h)
   - A. 15.7.
   - B. 17.3.
   - C. 19.5.
5. The factor in Exhibit 1 that most likely explains Blue Heron's forward P/E discount to Dunmore and Corvina is its: (LOS: los-05-04-m)
   - A. lower beta.
   - B. lower expected earnings growth.
   - C. membership in a peer group that may be overvalued as a whole.
6. For Brandt's trailing-earnings screen, the most appropriate metric and its implication are: (LOS: los-05-04-f)
   - A. trailing P/E; Calyx ranks as the least expensive stock.
   - B. trailing E/P; Corvina ranks as the most expensive stock.
   - C. trailing E/P; Calyx ranks as the most expensive stock.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** A measure that dampens a large outlier without removing it is the harmonic mean.
> Sum of reciprocals $= 1/11 + 1/12 + 1/40 + 1/13 = 0.0909 + 0.0833 + 0.0250 + 0.0769 = 0.2762$ (unrounded 0.276166); harmonic mean $= 4/0.276166 = 14.4841$, or 14.5.
> A is wrong because the median ($(12.0 + 13.0)/2 = 12.5$) removes the influence of Calyx entirely rather than reducing it.
> C is wrong because the arithmetic mean ($76/4 = 19.0$) is the measure most distorted by the large outlier.
> 2. **A.** Corvina's forward P/E is $36.00/2.70 = 13.3333$, below the harmonic mean benchmark of 14.4841, so the shares are relatively undervalued.
> The fundamentals support rather than explain away the discount: Corvina's 11.0% growth exceeds that of Ardenne, Blue Heron and Dunmore, and its beta of 1.00 is in line with theirs.
> B is wrong because a gap of 1.15 turns of earnings with superior growth and similar risk is not consistent with fair value.
> C is wrong because it follows from the median benchmark of 12.5, which Brandt's preference rules out.
> 3. **C.** PEG $=$ forward P/E divided by growth in percentage points: Ardenne $11.0/7.0 = 1.5714$; Blue Heron $12.0/6.0 = 2.0000$; Calyx $40.0/32.0 = 1.2500$; Dunmore $13.0/8.0 = 1.6250$; Corvina $13.3333/11.0 = 1.2121$.
> Corvina has the lowest PEG and is the most attractive, all else equal.
> A is wrong because Ardenne has the lowest P/E but not the lowest growth-adjusted P/E.
> B is wrong because Calyx is lowest only if Corvina's trailing P/E is used ($15.00/11.0 = 1.3636$), mixing trailing and forward multiples; Calyx's high growth also comes with the highest beta, a risk PEG ignores.
> 4. **A.** $\widehat{P/E} = 8.40 + 4.10(0.30) - 1.90(1.00) + 72.0(0.11) = 8.40 + 1.2300 - 1.9000 + 7.9200 = 15.6500$, or 15.7.
> Corvina's actual trailing P/E is $36.00/2.40 = 15.00$, slightly below the prediction, which is consistent with mild undervaluation; the conclusion is tentative because the regression is sample- and date-specific, its coefficients are unstable over time, and multicollinearity between payout and growth blurs individual coefficients, the three limitations Achebe raises.
> B is wrong because it enters the retention ratio instead of the payout ratio ($8.40 + 4.10(0.70) - 1.90 + 7.92 = 17.29$).
> C is wrong because it adds the beta term instead of subtracting it ($8.40 + 1.23 + 1.90 + 7.92 = 19.45$).
> 5. **B.** Blue Heron's expected growth of 6.0% is the lowest in the group, and lower expected growth justifies a lower P/E, so fundamentals explain much of its discount.
> A is wrong because a lower beta means lower risk, which would justify a higher P/E, not a lower one.
> C is wrong because mispricing of the whole peer group affects every member's absolute valuation and cannot explain one member's discount relative to the others; the fund also treats the benchmark as fairly priced.
> 6. **C.** Calyx's trailing EPS is negative, so its P/E is not meaningful; E/P ranks every stock because price is always positive.
> Trailing E/P: Ardenne $1.85/22 = 8.41\%$; Blue Heron $3.70/48 = 7.71\%$; Dunmore $1.90/26 = 7.31\%$; Corvina $2.40/36 = 6.67\%$; Calyx $-0.75/60 = -1.25\%$.
> The lowest earnings yield marks the most expensive stock per unit of earnings, which is Calyx.
> A is wrong because a negative P/E ($60/(-0.75) = -80$) sorts below every positive P/E and falsely makes Calyx look cheapest.
> B is wrong because Corvina has the lowest positive E/P but not the lowest E/P once Calyx's negative yield is included.

## Distractor design

1. A: median chosen, which removes rather than dampens the outlier; C: arithmetic mean, the measure most pulled by the outlier.
2. B: premium growth ignored; C: median benchmark used instead of the harmonic mean.
3. A: lowest P/E read as cheapest without growth adjustment; B: trailing P/E for Corvina mixed with forward P/Es for peers.
4. B: retention ratio entered for DPR; C: sign of the beta coefficient ignored.
5. A: direction of the risk adjustment reversed; C: absolute mispricing of the group confused with a relative discount.
6. A: negative P/E ranked numerically; B: negative-EPS stock dropped from the E/P ranking.
